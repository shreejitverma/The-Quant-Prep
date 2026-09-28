// Fixed-size object pool for low-latency code.
//
// Why pools on a hot path: general-purpose allocators take locks or thread caches, have
// data-dependent latency, and scatter objects across memory. A pool pre-allocates slots
// in large blocks, so steady-state allocate/deallocate is O(1), allocation-free and cache
// friendly. (malloc does not usually make a system call; the cost is variance, not syscalls.)
//
// Design: slots are raw, suitably aligned storage (objects are constructed only when
// handed out), and free slots form an intrusive singly linked list threaded through
// the slots themselves, so deallocate never allocates. Not thread-safe by design: give
// each thread its own pool. Build: g++ -std=c++20 -O2 memory_pool.cpp

#include <cassert>
#include <cstddef>
#include <iostream>
#include <memory>
#include <new>
#include <utility>
#include <vector>

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

struct Order {
    int id;
    double price;
    double qty;
};

int main() {
    ObjectPool<Order> pool;
    Order* o1 = pool.create(1, 100.5, 10.0);
    Order* o2 = pool.create(2, 100.6, 20.0);
    std::cout << "order " << o1->id << " @ " << o1->price << ", order " << o2->id << " @ " << o2->price << '\n';

    const void* freed_slot = o1;  // remember the address, not the dangling pointer
    pool.destroy(o1);
    Order* o3 = pool.create(3, 101.0, 5.0);
    std::cout << "order " << o3->id << " reused the freed slot: " << std::boolalpha << (static_cast<const void*>(o3) == freed_slot)
              << "\nlive " << pool.live() << " of capacity " << pool.capacity() << '\n';

    pool.destroy(o2);
    pool.destroy(o3);
    return pool.live() == 0 ? 0 : 1;
}
