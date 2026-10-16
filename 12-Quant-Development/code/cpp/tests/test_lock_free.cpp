// Unit and stress tests for lock_free.hpp and memory_pool.hpp
// (04-Concurrency-Lock-Free-and-Memory-Pools.md). Framework-free; exits non-zero on failure.
// Run under ThreadSanitizer as well as ASan/UBSan: the stress tests are the interesting part.

#include "lock_free.hpp"
#include "memory_pool.hpp"

#include <algorithm>
#include <atomic>
#include <cstdint>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

namespace {

int g_failures = 0;
int g_total = 0;

#define EXPECT(cond)                                                                            \
    do {                                                                                        \
        ++g_total;                                                                              \
        if (!(cond)) {                                                                          \
            ++g_failures;                                                                       \
            std::cerr << "  FAIL: " << __FILE__ << ":" << __LINE__ << " -> " #cond << std::endl; \
        }                                                                                       \
    } while (0)

// ------------------------------------------------------------------ SPSC
void test_spsc_single_thread_semantics() {
    qpconc::SpscQueue<int, 4> q;
    int out = 0;
    EXPECT(!q.try_pop(out));  // empty
    for (int i = 0; i < 4; ++i) EXPECT(q.try_push(i));
    EXPECT(!q.try_push(99));  // full: all N slots usable, no sacrificial slot
    EXPECT(q.size() == 4);
    for (int i = 0; i < 4; ++i) {
        EXPECT(q.try_pop(out));
        EXPECT(out == i);  // FIFO
    }
    EXPECT(!q.try_pop(out));
    for (int lap = 0; lap < 10; ++lap) {  // wrap the ring many times
        EXPECT(q.try_push(lap));
        EXPECT(q.try_pop(out) && out == lap);
    }
}

void test_spsc_move_only_payload() {
    qpconc::SpscQueue<std::string, 2> q;
    EXPECT(q.try_push(std::string(64, 'x')));
    std::string s;
    EXPECT(q.try_pop(s) && s.size() == 64);
}

void test_spsc_two_threads() {
    constexpr std::uint64_t kN = 100'000;
    qpconc::SpscQueue<std::uint64_t, 64> q;  // small ring: forces many full/empty transitions
    std::thread producer([&] {
        for (std::uint64_t i = 0; i < kN; ++i)
            while (!q.try_push(i)) std::this_thread::yield();
    });
    std::uint64_t next = 0;
    bool in_order = true;
    std::uint64_t v = 0;
    while (next < kN) {
        if (q.try_pop(v)) {
            in_order &= (v == next);
            ++next;
        } else {
            std::this_thread::yield();
        }
    }
    producer.join();
    EXPECT(in_order);
    EXPECT(q.size() == 0);
}

// ------------------------------------------------------------------ MPMC
void test_mpmc_single_thread_semantics() {
    qpconc::MpmcQueue<int, 4> q;
    int out = 0;
    EXPECT(!q.try_pop(out));
    for (int i = 0; i < 4; ++i) EXPECT(q.try_push(i));
    EXPECT(!q.try_push(4));
    for (int i = 0; i < 4; ++i) EXPECT(q.try_pop(out) && out == i);
    EXPECT(!q.try_pop(out));
}

void test_mpmc_many_threads() {
    constexpr int kProducers = 3;
    constexpr int kConsumers = 3;
    constexpr std::uint32_t kPerProducer = 20'000;
    qpconc::MpmcQueue<std::uint64_t, 128> q;
    std::vector<std::atomic<int>> seen(kProducers * kPerProducer);
    std::atomic<std::uint64_t> consumed{0};
    std::vector<std::thread> threads;
    for (int p = 0; p < kProducers; ++p)
        threads.emplace_back([&, p] {
            for (std::uint32_t i = 0; i < kPerProducer; ++i) {
                const std::uint64_t id = static_cast<std::uint64_t>(p) * kPerProducer + i;
                while (!q.try_push(id)) std::this_thread::yield();
            }
        });
    // Per-producer FIFO: each consumer must see one producer's values in increasing order.
    std::atomic<bool> fifo_ok{true};
    for (int c = 0; c < kConsumers; ++c)
        threads.emplace_back([&] {
            std::vector<std::int64_t> last(kProducers, -1);
            std::uint64_t v = 0;
            while (consumed.load(std::memory_order_relaxed) < kProducers * kPerProducer) {
                if (!q.try_pop(v)) {
                    std::this_thread::yield();
                    continue;
                }
                seen[v].fetch_add(1, std::memory_order_relaxed);
                const auto p = static_cast<std::size_t>(v / kPerProducer);
                const auto i = static_cast<std::int64_t>(v % kPerProducer);
                if (i <= last[p]) fifo_ok.store(false);
                last[p] = i;
                consumed.fetch_add(1, std::memory_order_relaxed);
            }
        });
    for (auto& t : threads) t.join();
    EXPECT(consumed.load() == kProducers * kPerProducer);
    EXPECT(std::all_of(seen.begin(), seen.end(), [](const std::atomic<int>& s) { return s.load() == 1; }));  // exactly once
    EXPECT(fifo_ok.load());
}

// ------------------------------------------------------------------ ABA
// Deterministic replay of the classic interleaving on one thread.
// Stack holds 0 -> 1 -> 2 (head 0). Thread 1 starts a pop: observes head 0, next 1, then stalls.
// Thread 2 pops 0, pops 1 (keeps 1 in use), pushes 0 back: head 0 -> 2. Thread 1 resumes.
template <bool UseTag>
std::pair<bool, std::uint32_t> replay_aba() {
    qpconc::TaggedIndexStack<3> s(UseTag);
    const auto t1 = s.prepare_pop();
    const auto a = s.pop();  // thread 2
    const auto b = s.pop();
    s.push(*a);
    const auto stale = s.commit_pop(t1);  // thread 1 resumes with its stale view
    const auto after = s.pop();           // whoever pops next
    (void)b;
    return {stale.has_value(), after.value_or(qpconc::TaggedIndexStack<3>::kNil)};
}

void test_aba_without_tag_corrupts() {
    const auto [stale_succeeded, next_pop] = replay_aba<false>();
    EXPECT(stale_succeeded);  // CAS saw the same bits and succeeded
    EXPECT(next_pop == 1);    // index 1 handed out again while thread 2 still holds it: corruption
}

void test_aba_with_tag_is_detected() {
    const auto [stale_succeeded, next_pop] = replay_aba<true>();
    EXPECT(!stale_succeeded);  // tag moved on: CAS fails, thread 1 would retry
    EXPECT(next_pop == 0);     // stack is intact: 0 -> 2
}

void test_tagged_stack_stress() {
    constexpr std::uint32_t kSlots = 64;
    qpconc::TaggedIndexStack<kSlots> s(true);
    std::vector<std::atomic<int>> owner(kSlots);
    std::atomic<bool> double_alloc{false};
    std::vector<std::thread> threads;
    for (int t = 0; t < 4; ++t)
        threads.emplace_back([&] {
            for (int k = 0; k < 20'000; ++k) {
                const auto idx = s.pop();
                if (!idx) continue;
                if (owner[*idx].exchange(1) != 0) double_alloc.store(true);
                if (owner[*idx].exchange(0) != 1) double_alloc.store(true);
                s.push(*idx);
            }
        });
    for (auto& t : threads) t.join();
    EXPECT(!double_alloc.load());
    std::vector<std::uint32_t> drained;
    while (auto i = s.pop()) drained.push_back(*i);
    std::sort(drained.begin(), drained.end());
    EXPECT(drained.size() == kSlots);
    bool all = drained.size() == kSlots;
    for (std::uint32_t i = 0; all && i < kSlots; ++i) all = drained[i] == i;
    EXPECT(all);  // every slot back exactly once
}

// ------------------------------------------------------------------ pool and arena
struct Node {
    std::int64_t a;
    std::int64_t b;
};

void test_pool_reuse_and_growth() {
    qpmem::ObjectPool<Node, 8> pool;
    std::vector<Node*> v;
    for (int i = 0; i < 20; ++i) v.push_back(pool.create(i, -i));  // forces two extra blocks
    EXPECT(pool.capacity() == 24);
    EXPECT(pool.live() == 20);
    EXPECT(v[19]->a == 19 && v[19]->b == -19);
    Node* freed = v[5];
    pool.destroy(freed);
    Node* again = pool.create(100, 100);
    EXPECT(again == freed);  // LIFO reuse of the warm slot
    v[5] = again;
    for (Node* n : v) pool.destroy(n);
    EXPECT(pool.live() == 0);
}

void test_arena_alignment_and_exhaustion() {
    qpmem::Arena arena(256);
    auto* c = static_cast<char*>(arena.allocate(1, 1));
    EXPECT(c != nullptr);
    auto* d = static_cast<double*>(arena.allocate(sizeof(double), alignof(double)));
    EXPECT(d != nullptr && reinterpret_cast<std::uintptr_t>(d) % alignof(double) == 0);
    EXPECT(arena.used() == 16);  // 1 byte, 7 bytes padding, 8 bytes double (buffer start is 16-aligned)
    EXPECT(arena.allocate(1000, 8) == nullptr);  // exhausted: reported, not UB
    EXPECT(arena.allocate(240, 8) != nullptr);
    EXPECT(arena.used() == 256);
    EXPECT(arena.allocate(1, 1) == nullptr);
    arena.reset();
    EXPECT(arena.used() == 0 && arena.high_water() == 256);
    EXPECT(arena.make<Node>(Node{1, 2})->b == 2);
}

}  // namespace

int main() {
    test_spsc_single_thread_semantics();
    test_spsc_move_only_payload();
    test_spsc_two_threads();
    test_mpmc_single_thread_semantics();
    test_mpmc_many_threads();
    test_aba_without_tag_corrupts();
    test_aba_with_tag_is_detected();
    test_tagged_stack_stress();
    test_pool_reuse_and_growth();
    test_arena_alignment_and_exhaustion();
    std::cout << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
