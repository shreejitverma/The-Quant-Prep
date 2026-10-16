// Benchmarks for 04-Concurrency-Lock-Free-and-Memory-Pools.md, measured on the machine it runs on:
//   1. queue throughput, one producer and one consumer: SPSC ring vs Vyukov MPMC vs mutex + deque;
//   2. core-to-core round trip through two SPSC rings (ping-pong);
//   3. allocation: operator new/delete vs ObjectPool vs Arena.
// Machine-dependent numbers; only loose orderings are asserted, and sanitizer builds shrink the
// workloads and skip the timing checks.
// Build: clang++ -std=c++20 -O2 -pthread concurrency_bench.cpp

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <memory>
#include <mutex>
#include <thread>
#include <vector>

#include "lock_free.hpp"
#include "memory_pool.hpp"
#include "microbenchmark_utils.hpp"

namespace {

constexpr bool kSan = qpbench::kSanitized;
constexpr std::uint64_t kItems = kSan ? 20'000 : 5'000'000;

class MutexQueue {  // the baseline everyone writes first
    std::mutex m_;
    std::deque<std::uint64_t> q_;
    std::size_t cap_;

public:
    explicit MutexQueue(std::size_t cap) : cap_(cap) {}
    bool try_push(std::uint64_t v) {
        std::scoped_lock lock(m_);
        if (q_.size() == cap_) return false;
        q_.push_back(v);
        return true;
    }
    bool try_pop(std::uint64_t& v) {
        std::scoped_lock lock(m_);
        if (q_.empty()) return false;
        v = q_.front();
        q_.pop_front();
        return true;
    }
};

// ns per item to move kItems from one thread to another; both sides spin (no yield, no sleep).
template <typename Q>
double transfer_ns_per_item(Q& q) {
    std::uint64_t sum = 0;
    const std::uint64_t t0 = qpbench::now_ns();
    std::thread consumer([&] {
        std::uint64_t v = 0;
        for (std::uint64_t got = 0; got < kItems;)
            if (q.try_pop(v)) {
                sum += v;
                ++got;
            }
    });
    for (std::uint64_t i = 0; i < kItems; ++i)
        while (!q.try_push(i)) {
        }
    consumer.join();
    const std::uint64_t t1 = qpbench::now_ns();
    if (sum != kItems * (kItems - 1) / 2) {
        std::printf("transfer lost or duplicated items\n");
        std::exit(EXIT_FAILURE);
    }
    return static_cast<double>(t1 - t0) / static_cast<double>(kItems);
}

struct PingPong {
    double median_rtt_ns;
    double p99_rtt_ns;
};

PingPong ping_pong() {
    qpconc::SpscQueue<std::uint64_t, 64> to_b;
    qpconc::SpscQueue<std::uint64_t, 64> to_a;
    const int batches = kSan ? 20 : 2000;
    constexpr int kPerBatch = 100;
    const std::uint64_t total = static_cast<std::uint64_t>(batches) * kPerBatch;
    std::thread echo([&] {
        std::uint64_t v = 0;
        for (std::uint64_t n = 0; n < total; ++n) {
            while (!to_b.try_pop(v)) {
            }
            while (!to_a.try_push(v + 1)) {
            }
        }
    });
    std::vector<double> rtt;
    rtt.reserve(static_cast<std::size_t>(batches));
    std::uint64_t v = 0;
    bool ok = true;
    for (int b = 0; b < batches; ++b) {
        const std::uint64_t t0 = qpbench::now_ns();
        for (int k = 0; k < kPerBatch; ++k) {
            const std::uint64_t sent = v;
            while (!to_b.try_push(sent)) {
            }
            while (!to_a.try_pop(v)) {
            }
            ok &= (v == sent + 1);
        }
        const std::uint64_t t1 = qpbench::now_ns();
        rtt.push_back(static_cast<double>(t1 - t0) / kPerBatch);
    }
    echo.join();
    if (!ok) {
        std::printf("ping-pong corrupted a value\n");
        std::exit(EXIT_FAILURE);
    }
    return {qpbench::percentile(rtt, 50), qpbench::percentile(rtt, 99)};
}

struct Node {
    std::int64_t a, b, c, d;  // 32 bytes, an order-sized object
};

struct AllocResult {
    double heap, pool, arena;
};

AllocResult allocation() {
    constexpr int kBatch = 1000;
    const int rounds = kSan ? 20 : 2000;
    std::vector<Node*> ptrs(kBatch);
    auto time_rounds = [&](auto&& alloc_all, auto&& free_all) {
        std::vector<double> per_pair;
        for (int r = 0; r < rounds; ++r) {
            const std::uint64_t t0 = qpbench::now_ns();
            alloc_all();
            free_all();
            const std::uint64_t t1 = qpbench::now_ns();
            per_pair.push_back(static_cast<double>(t1 - t0) / kBatch);
        }
        return qpbench::percentile(per_pair, 50);
    };
    std::int64_t sink = 0;
    const double heap = time_rounds(
        [&] {
            for (int i = 0; i < kBatch; ++i) {
                ptrs[static_cast<std::size_t>(i)] = new Node{i, 0, 0, 0};
                qpbench::do_not_optimize(ptrs[static_cast<std::size_t>(i)]);
            }
        },
        [&] {
            for (Node* p : ptrs) {
                sink += p->a;
                delete p;
            }
        });
    qpmem::ObjectPool<Node> pool;
    const double pooled = time_rounds(
        [&] {
            for (int i = 0; i < kBatch; ++i) ptrs[static_cast<std::size_t>(i)] = pool.create(i, 0, 0, 0);
        },
        [&] {
            for (Node* p : ptrs) {
                sink += p->a;
                pool.destroy(p);
            }
        });
    qpmem::Arena arena(kBatch * sizeof(Node));
    const double arena_ns = time_rounds(
        [&] {
            for (int i = 0; i < kBatch; ++i) ptrs[static_cast<std::size_t>(i)] = arena.make<Node>(Node{i, 0, 0, 0});
        },
        [&] {
            for (Node* p : ptrs) sink += p->a;
            arena.reset();
        });
    qpbench::do_not_optimize(sink);
    return {heap, pooled, arena_ns};
}

}  // namespace

int main() {
    qpconc::SpscQueue<std::uint64_t, 1024> spsc;
    qpconc::MpmcQueue<std::uint64_t, 1024> mpmc;
    MutexQueue mutex_q(1024);
    const double t_spsc = transfer_ns_per_item(spsc);
    const double t_mpmc = transfer_ns_per_item(mpmc);
    const double t_mutex = transfer_ns_per_item(mutex_q);
    std::printf("[queues] one producer, one consumer, %llu items, capacity 1024\n", static_cast<unsigned long long>(kItems));
    std::printf("  SPSC ring            %7.2f ns/item  (%6.1f M items/s)\n", t_spsc, 1e3 / t_spsc);
    std::printf("  Vyukov MPMC          %7.2f ns/item  (%6.1f M items/s)\n", t_mpmc, 1e3 / t_mpmc);
    std::printf("  mutex + deque        %7.2f ns/item  (%6.1f M items/s)\n", t_mutex, 1e3 / t_mutex);

    const auto pp = ping_pong();
    std::printf("[ping-pong] round trip through two SPSC rings: median %.1f ns, p99 %.1f ns (batch means of 100)\n", pp.median_rtt_ns,
                pp.p99_rtt_ns);

    const auto al = allocation();
    std::printf("[allocation] 32-byte objects, ns per allocate+free pair (median of rounds of 1000)\n");
    std::printf("  operator new/delete  %7.2f\n  ObjectPool           %7.2f\n  Arena (bump, reset)  %7.2f\n", al.heap, al.pool, al.arena);

    if (kSan) {
        std::printf("sanitized build: timing checks skipped\n");
        return EXIT_SUCCESS;
    }
    bool ok = true;
    ok &= t_spsc < t_mutex;      // no lock, no kernel arbitration
    ok &= al.pool < al.heap;     // a free-list pop beats a general-purpose allocator
    ok &= al.arena < al.heap;
    std::printf("%s\n", ok ? "sanity bounds hold" : "SANITY BOUNDS FAILED");
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
