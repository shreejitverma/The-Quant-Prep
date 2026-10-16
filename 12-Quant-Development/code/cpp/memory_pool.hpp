// Fixed-size object pool and monotonic arena for low-latency code
// (04-Concurrency-Lock-Free-and-Memory-Pools.md).
//
// Why on a hot path: general-purpose allocators have data-dependent latency (size-class lookup,
// thread-cache refills, occasional trips to the OS for fresh pages) and scatter objects across
// memory. Both structures below pre-allocate at startup so the steady state never calls malloc.
// (malloc does not usually make a system call; the problem is variance, not syscalls.)
//
// ObjectPool<T>: free slots form an intrusive singly linked list threaded through the slots
// themselves, so create/destroy are O(1) and destroy never allocates. Slots are reused LIFO,
// which keeps recently freed (cache-warm) memory in use. Not thread-safe: one pool per thread,
// or a lock-free free list such as qpconc::TaggedIndexStack over slot indices.
//
// Arena: bump-pointer allocation from one buffer, no per-object free, release everything at
// once with reset() (per message batch, per request, per trading day). Destructors are never
// run, so only trivially destructible types may be placed in it.

#pragma once

#include <cassert>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <new>
#include <type_traits>
#include <utility>
#include <vector>

namespace qpmem {

template <typename T, std::size_t SlotsPerBlock = 4096>
class ObjectPool {
    union Slot {
        Slot* next;  // valid while the slot is free
        alignas(T) std::byte storage[sizeof(T)];
    };
    struct Block {
        Slot slots[SlotsPerBlock];
    };

    std::vector<std::unique_ptr<Block>> blocks_;
    Slot* free_ = nullptr;
    std::size_t live_ = 0;

    void grow() {
        auto block = std::make_unique<Block>();
        for (std::size_t i = SlotsPerBlock; i-- > 0;) {  // thread in reverse so slots hand out in address order
            block->slots[i].next = free_;
            free_ = &block->slots[i];
        }
        blocks_.push_back(std::move(block));
    }

public:
    explicit ObjectPool(std::size_t reserve_blocks = 1) {
        blocks_.reserve(reserve_blocks);
        for (std::size_t i = 0; i < reserve_blocks; ++i) grow();
    }
    ~ObjectPool() { assert(live_ == 0 && "objects still alive when the pool is destroyed"); }
    ObjectPool(const ObjectPool&) = delete;
    ObjectPool& operator=(const ObjectPool&) = delete;

    template <typename... Args>
    [[nodiscard]] T* create(Args&&... args) {
        if (free_ == nullptr) grow();  // slow path: only when the reserve is exhausted
        Slot* slot = free_;
        free_ = slot->next;
        T* obj = ::new (static_cast<void*>(slot->storage)) T{std::forward<Args>(args)...};
        ++live_;
        return obj;
    }

    void destroy(T* obj) noexcept {
        if (obj == nullptr) return;
        obj->~T();
        auto* slot = reinterpret_cast<Slot*>(obj);  // storage is the union's first byte
        slot->next = free_;
        free_ = slot;
        --live_;
    }

    [[nodiscard]] std::size_t live() const noexcept { return live_; }
    [[nodiscard]] std::size_t capacity() const noexcept { return blocks_.size() * SlotsPerBlock; }
};

class Arena {
    std::unique_ptr<std::byte[]> buffer_;
    std::size_t capacity_;
    std::size_t used_ = 0;
    std::size_t high_water_ = 0;

public:
    explicit Arena(std::size_t capacity) : buffer_(std::make_unique<std::byte[]>(capacity)), capacity_(capacity) {}
    Arena(const Arena&) = delete;
    Arena& operator=(const Arena&) = delete;

    // Returns nullptr when the arena is exhausted: the caller decides (reject, fall back, alarm).
    // align must be a power of two.
    [[nodiscard]] void* allocate(std::size_t bytes, std::size_t align) noexcept {
        const auto base = reinterpret_cast<std::uintptr_t>(buffer_.get());
        const std::uintptr_t aligned = (base + used_ + (align - 1)) & ~(static_cast<std::uintptr_t>(align) - 1);
        const std::size_t offset = static_cast<std::size_t>(aligned - base);
        if (offset > capacity_ || bytes > capacity_ - offset) return nullptr;
        used_ = offset + bytes;
        if (used_ > high_water_) high_water_ = used_;
        return buffer_.get() + offset;
    }

    template <typename T, typename... Args>
    [[nodiscard]] T* make(Args&&... args) noexcept(std::is_nothrow_constructible_v<T, Args...>) {
        static_assert(std::is_trivially_destructible_v<T>, "the arena never runs destructors");
        void* p = allocate(sizeof(T), alignof(T));
        return p == nullptr ? nullptr : ::new (p) T{std::forward<Args>(args)...};
    }

    void reset() noexcept { used_ = 0; }
    [[nodiscard]] std::size_t used() const noexcept { return used_; }
    [[nodiscard]] std::size_t high_water() const noexcept { return high_water_; }
    [[nodiscard]] std::size_t capacity() const noexcept { return capacity_; }
};

}  // namespace qpmem
