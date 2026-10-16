// Lock-free building blocks for 04-Concurrency-Lock-Free-and-Memory-Pools.md.
//
//   SpscQueue<T, N>        bounded single-producer single-consumer ring buffer (wait-free)
//   MpmcQueue<T, N>        Dmitry Vyukov's bounded multi-producer multi-consumer queue
//   TaggedIndexStack<N>    Treiber stack of indices with an ABA tag (a lock-free free list)
//   SpinLock               test-and-test-and-set lock (acquire on lock, release on unlock)
//   Seqlock<T>             single-writer sequence lock for a small trivially copyable snapshot
//
// Every memory order below names the happens-before edge it creates. All of them are tested under
// ThreadSanitizer in tests/test_lock_free.cpp.

#pragma once

#include <array>
#include <atomic>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <memory>
#include <optional>
#include <type_traits>
#include <utility>

namespace qpconc {

// Padding that keeps data written by different threads on different cache lines. 128 covers
// Apple Silicon (sysctl hw.cachelinesize reports 128) and x86-64, whose adjacent-line prefetcher
// pulls 64-byte lines in pairs. Not std::hardware_destructive_interference_size: its value differs
// between compilers and GCC warns when it is used in a header.
inline constexpr std::size_t kPad = 128;

template <std::size_t N>
concept PowerOfTwo = N >= 2 && (N & (N - 1)) == 0;

// ---------------------------------------------------------------------------------------------
// SPSC ring. head_ and tail_ are monotonically increasing 64-bit counters (they never wrap in
// practice: 2^64 messages at 1e9 per second is 584 years), the slot is counter & (N - 1), and
// full means head - tail == N, so all N slots are usable.
// Each side keeps a private cached copy of the other side's counter and refreshes it only when
// the queue looks full (producer) or empty (consumer): in steady state neither side reads the
// other's cache line, which removes most of the coherence traffic.
// ---------------------------------------------------------------------------------------------
template <typename T, std::size_t N>
    requires PowerOfTwo<N> && std::is_default_constructible_v<T> && std::is_nothrow_move_assignable_v<T>
class SpscQueue {
    static constexpr std::uint64_t kMask = N - 1;

    struct alignas(kPad) Producer {
        std::atomic<std::uint64_t> head{0};  // next slot to write; stored by the producer only
        std::uint64_t cached_tail = 0;       // producer's last view of tail
    };
    struct alignas(kPad) Consumer {
        std::atomic<std::uint64_t> tail{0};  // next slot to read; stored by the consumer only
        std::uint64_t cached_head = 0;       // consumer's last view of head
    };

    Producer p_;
    Consumer c_;
    std::unique_ptr<T[]> slots_ = std::make_unique<T[]>(N);  // allocated once, at construction

public:
    SpscQueue() = default;
    SpscQueue(const SpscQueue&) = delete;
    SpscQueue& operator=(const SpscQueue&) = delete;

    static constexpr std::size_t capacity() noexcept { return N; }

    // Producer thread only.
    template <typename U>
    [[nodiscard]] bool try_push(U&& value) noexcept(std::is_nothrow_assignable_v<T&, U&&>) {
        const std::uint64_t h = p_.head.load(std::memory_order_relaxed);  // own counter
        if (h - p_.cached_tail == N) {
            // acquire pairs with the consumer's release store of tail: its read of the slot we are
            // about to overwrite happened-before our write (no write-after-read race).
            p_.cached_tail = c_.tail.load(std::memory_order_acquire);
            if (h - p_.cached_tail == N) return false;  // full
        }
        slots_[h & kMask] = std::forward<U>(value);
        // release publishes the slot write: a consumer that acquires head >= h + 1 sees the value.
        p_.head.store(h + 1, std::memory_order_release);
        return true;
    }

    // Consumer thread only.
    [[nodiscard]] bool try_pop(T& out) noexcept {
        const std::uint64_t t = c_.tail.load(std::memory_order_relaxed);  // own counter
        if (t == c_.cached_head) {
            c_.cached_head = p_.head.load(std::memory_order_acquire);  // pairs with the release in try_push
            if (t == c_.cached_head) return false;                     // empty
        }
        out = std::move(slots_[t & kMask]);
        c_.tail.store(t + 1, std::memory_order_release);  // hands the slot back to the producer
        return true;
    }

    // Approximate when called concurrently; exact when both sides are quiescent. The two counters
    // cannot be read at one instant. Reading head first can pair an old head with a newer, larger
    // tail, and the unsigned difference wraps to about 2^64. So tail is read first (a head read
    // afterwards is never smaller: the consumer only advanced tail after seeing head that far), and
    // the result is clamped to N, because both sides may have moved on between the two loads.
    [[nodiscard]] std::size_t size() const noexcept {
        const std::uint64_t t = c_.tail.load(std::memory_order_acquire);
        const std::uint64_t h = p_.head.load(std::memory_order_acquire);
        return static_cast<std::size_t>(h - t < N ? h - t : N);
    }
};

// ---------------------------------------------------------------------------------------------
// Vyukov bounded MPMC queue. Each cell carries a sequence number that says whose turn it is:
// seq == pos means free for the producer claiming position pos; seq == pos + 1 means full for the
// consumer claiming pos. Producers and consumers claim positions with a CAS on their own counter.
// One CAS per operation, no ABA (positions only grow). Not lock-free in the strict sense: a thread
// suspended between claiming a cell and publishing its seq blocks the threads that reach that cell.
// ---------------------------------------------------------------------------------------------
template <typename T, std::size_t N>
    requires PowerOfTwo<N> && std::is_default_constructible_v<T> && std::is_nothrow_move_assignable_v<T>
class MpmcQueue {
    static constexpr std::uint64_t kMask = N - 1;

    struct Cell {
        std::atomic<std::uint64_t> seq;
        T data;
    };

    std::unique_ptr<Cell[]> cells_ = std::make_unique<Cell[]>(N);
    alignas(kPad) std::atomic<std::uint64_t> enqueue_pos_{0};
    alignas(kPad) std::atomic<std::uint64_t> dequeue_pos_{0};

public:
    MpmcQueue() {
        for (std::size_t i = 0; i < N; ++i) cells_[i].seq.store(i, std::memory_order_relaxed);
    }
    MpmcQueue(const MpmcQueue&) = delete;
    MpmcQueue& operator=(const MpmcQueue&) = delete;

    template <typename U>
    [[nodiscard]] bool try_push(U&& value) noexcept(std::is_nothrow_assignable_v<T&, U&&>) {
        std::uint64_t pos = enqueue_pos_.load(std::memory_order_relaxed);
        Cell* cell;
        for (;;) {
            cell = &cells_[pos & kMask];
            // acquire pairs with the consumer's release of seq = pos: its move-out of the
            // previous value happened-before our overwrite.
            const std::uint64_t seq = cell->seq.load(std::memory_order_acquire);
            const auto diff = static_cast<std::int64_t>(seq - pos);
            if (diff == 0) {
                if (enqueue_pos_.compare_exchange_weak(pos, pos + 1, std::memory_order_relaxed)) break;
            } else if (diff < 0) {
                return false;  // the cell still holds the value from one lap ago: full
            } else {
                pos = enqueue_pos_.load(std::memory_order_relaxed);  // another producer took pos
            }
        }
        cell->data = std::forward<U>(value);
        cell->seq.store(pos + 1, std::memory_order_release);  // publish to the consumer of pos
        return true;
    }

    [[nodiscard]] bool try_pop(T& out) noexcept {
        std::uint64_t pos = dequeue_pos_.load(std::memory_order_relaxed);
        Cell* cell;
        for (;;) {
            cell = &cells_[pos & kMask];
            const std::uint64_t seq = cell->seq.load(std::memory_order_acquire);  // pairs with push's release
            const auto diff = static_cast<std::int64_t>(seq - (pos + 1));
            if (diff == 0) {
                if (dequeue_pos_.compare_exchange_weak(pos, pos + 1, std::memory_order_relaxed)) break;
            } else if (diff < 0) {
                return false;  // not yet written: empty
            } else {
                pos = dequeue_pos_.load(std::memory_order_relaxed);
            }
        }
        out = std::move(cell->data);
        cell->seq.store(pos + kMask + 1, std::memory_order_release);  // free for the producer one lap later
        return true;
    }
};

// ---------------------------------------------------------------------------------------------
// Treiber stack over indices 0..N-1 (a lock-free free list for a preallocated pool).
// head_ packs {tag:32, index:32}. Without the tag a pop can suffer ABA: it reads head = A and
// next(A) = B, stalls, another thread pops A and B and pushes A back, and the stalled CAS still
// sees head == A and installs B, which is no longer free. The tag changes on every successful
// push and pop, so that CAS fails. Nodes are indices into a fixed array that is never freed, so
// reading next_ of a node that was just popped elsewhere is a stale read, never a use-after-free.
// The tag can in principle wrap after 2^32 operations between a read and its CAS.
// ---------------------------------------------------------------------------------------------
template <std::uint32_t N>
class TaggedIndexStack {
public:
    static constexpr std::uint32_t kNil = 0xFFFF'FFFFu;

    struct PopAttempt {  // a pop split in two, so tests can interleave threads deterministically
        std::uint64_t observed;
        std::uint32_t next;
    };

    explicit TaggedIndexStack(bool use_tag = true) : tag_step_(use_tag ? 1u : 0u) {
        for (std::uint32_t i = N; i-- > 0;) push(i);  // so pops return 0, 1, 2, ...
    }

    void push(std::uint32_t idx) noexcept {
        std::uint64_t old = head_.load(std::memory_order_relaxed);
        for (;;) {
            next_[idx].store(index_of(old), std::memory_order_relaxed);
            // release: the next_ store above happens-before any pop that acquires this head.
            if (head_.compare_exchange_weak(old, pack(tag_of(old) + tag_step_, idx), std::memory_order_release, std::memory_order_relaxed))
                return;
        }
    }

    [[nodiscard]] std::optional<std::uint32_t> pop() noexcept {
        PopAttempt a = prepare_pop();
        for (;;) {
            if (index_of(a.observed) == kNil) return std::nullopt;
            if (auto got = commit_pop(a)) return got;
            a = prepare_pop();
        }
    }

    // Step 1 of pop: read head (acquire, pairs with push's release) and the would-be new head.
    [[nodiscard]] PopAttempt prepare_pop() const noexcept {
        const std::uint64_t h = head_.load(std::memory_order_acquire);
        const std::uint32_t idx = index_of(h);
        return {h, idx == kNil ? kNil : next_[idx].load(std::memory_order_relaxed)};
    }

    // Step 2 of pop: install next if head is still exactly what we observed.
    [[nodiscard]] std::optional<std::uint32_t> commit_pop(const PopAttempt& a) noexcept {
        std::uint64_t expected = a.observed;
        if (index_of(expected) == kNil) return std::nullopt;
        if (head_.compare_exchange_strong(expected, pack(tag_of(expected) + tag_step_, a.next), std::memory_order_acquire,
                                          std::memory_order_acquire))
            return index_of(a.observed);
        return std::nullopt;
    }

private:
    static constexpr std::uint64_t pack(std::uint32_t tag, std::uint32_t idx) noexcept { return (std::uint64_t{tag} << 32) | idx; }
    static constexpr std::uint32_t index_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h); }
    static constexpr std::uint32_t tag_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h >> 32); }

    std::array<std::atomic<std::uint32_t>, N> next_{};
    alignas(kPad) std::atomic<std::uint64_t> head_{pack(0, kNil)};
    std::uint32_t tag_step_;
};

// ---------------------------------------------------------------------------------------------
// Test-and-test-and-set spin lock. lock() is an acquire RMW, unlock() a release store: everything
// a thread did inside the critical section happens-before whatever the next owner does inside it.
// Waiters spin on a relaxed load (a shared, read-only copy of the line in their own cache) and only
// retry the exchange when the lock looks free, so they do not bounce the line with failed RMWs.
// Only for very short critical sections on dedicated cores: a preempted owner makes everyone spin.
// ---------------------------------------------------------------------------------------------
inline void cpu_relax() noexcept {
#if defined(__x86_64__) || defined(__i386__)
    __builtin_ia32_pause();  // PAUSE: eases the spin-loop exit and frees resources for the SMT sibling
#elif defined(__aarch64__)
    __asm__ volatile("yield");
#endif
}

class SpinLock {
    std::atomic<bool> locked_{false};

public:
    void lock() noexcept {
        for (;;) {
            if (!locked_.exchange(true, std::memory_order_acquire)) return;  // pairs with unlock's release
            while (locked_.load(std::memory_order_relaxed)) cpu_relax();
        }
    }
    [[nodiscard]] bool try_lock() noexcept {
        return !locked_.load(std::memory_order_relaxed) && !locked_.exchange(true, std::memory_order_acquire);
    }
    void unlock() noexcept { locked_.store(false, std::memory_order_release); }
};

// ---------------------------------------------------------------------------------------------
// Seqlock: one writer publishes a small snapshot (top of book, a risk limit set) that many readers
// copy without ever blocking the writer. The sequence is odd while a write is in progress; a reader
// accepts its copy only if it saw the same even sequence before and after reading the data.
// The data words are relaxed-or-stronger atomics, not plain memory: a reader overlapping a write
// would otherwise be a data race (undefined behaviour), even though it discards the torn copy.
// Orders (fence-free variant, Boehm 2012): the writer's data stores are release, so a reader that
// sees any new word also sees the odd sequence stored before it, and its final sequence load
// (kept after the data loads by their acquire) detects the overlap. The reader's first load is
// acquire and pairs with the writer's final release, so an unchanged even sequence means it read
// one complete version. Writer: wait-free. Readers: retry while a write overlaps (not lock-free).
// ---------------------------------------------------------------------------------------------
template <typename T>
    requires std::is_trivially_copyable_v<T> && std::is_default_constructible_v<T>
class Seqlock {
    static constexpr std::size_t kWords = (sizeof(T) + 7) / 8;
    alignas(kPad) std::atomic<std::uint64_t> seq_{0};
    std::array<std::atomic<std::uint64_t>, kWords> words_{};

public:
    // Single writer thread only.
    void store(const T& value) noexcept {
        std::array<std::uint64_t, kWords> buf{};
        std::memcpy(buf.data(), &value, sizeof(T));
        const std::uint64_t s = seq_.load(std::memory_order_relaxed);  // own counter
        seq_.store(s + 1, std::memory_order_relaxed);                   // odd: write in progress
        for (std::size_t i = 0; i < kWords; ++i) words_[i].store(buf[i], std::memory_order_release);
        seq_.store(s + 2, std::memory_order_release);  // even: publishes the complete version
    }

    // Any thread. False if a write overlapped the read; the caller retries or uses its last copy.
    [[nodiscard]] bool try_load(T& out) const noexcept {
        const std::uint64_t s0 = seq_.load(std::memory_order_acquire);
        if (s0 & 1u) return false;
        std::array<std::uint64_t, kWords> buf{};
        for (std::size_t i = 0; i < kWords; ++i) buf[i] = words_[i].load(std::memory_order_acquire);
        if (seq_.load(std::memory_order_relaxed) != s0) return false;
        std::memcpy(&out, buf.data(), sizeof(T));
        return true;
    }

    [[nodiscard]] T load() const noexcept {
        T out{};
        while (!try_load(out)) cpu_relax();
        return out;
    }
};

}  // namespace qpconc
