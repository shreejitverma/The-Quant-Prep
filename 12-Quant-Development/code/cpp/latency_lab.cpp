// Low-latency lab for 03-Low-Latency-Engineering.md: measures, on the machine it runs on,
//   1. the clock: cost of steady_clock::now(), its observed resolution, the user-space counter rate;
//   2. the memory hierarchy: dependent-load latency by working-set size (pointer chasing);
//   3. false sharing: two threads updating counters 8, 64, 128 and 256 bytes apart;
//   4. branch prediction: the same loop over random and over sorted data;
//   5. jitter: the latency distribution of a fixed ~1 us workload (percentiles, not the mean).
// All results are machine-dependent. Only loose qualitative bounds are asserted, and sanitizer
// builds shrink the workloads and skip the timing checks.
// Build: clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror -pthread latency_lab.cpp

#include <algorithm>
#include <atomic>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <memory>
#include <new>
#include <random>
#include <thread>
#include <vector>

#include "microbenchmark_utils.hpp"

namespace {

constexpr bool kSan = qpbench::kSanitized;

// ---------------------------------------------------------------------------------------------
// 1. Clock
// ---------------------------------------------------------------------------------------------
void clock_section() {
    constexpr int n = kSan ? 20'000 : 2'000'000;
    const std::uint64_t t0 = qpbench::now_ns();
    std::uint64_t acc = 0;
    for (int i = 0; i < n; ++i) acc += qpbench::now_ns();
    const std::uint64_t t1 = qpbench::now_ns();
    qpbench::do_not_optimize(acc);
    // The most common non-zero difference between back-to-back reads is the clock's effective
    // resolution (the nominal unit can be much finer than the rate at which the value advances).
    auto modal_step = [](auto read) {
        std::map<std::uint64_t, int> steps;
        std::uint64_t prev = read();
        for (int i = 0; i < n; ++i) {
            const std::uint64_t t = read();
            if (t != prev) ++steps[t - prev];
            prev = t;
        }
        std::uint64_t best = 0;
        int count = 0;
        for (const auto& [d, c] : steps)
            if (c > count) {
                best = d;
                count = c;
            }
        return best;
    };
    const std::uint64_t step_ns = modal_step(qpbench::now_ns);
    const std::uint64_t step_ticks = modal_step(qpbench::cycle_counter);
    const std::uint64_t c0 = qpbench::cycle_counter();
    for (int i = 0; i < n; ++i) acc += qpbench::cycle_counter();
    const std::uint64_t c1 = qpbench::cycle_counter();
    qpbench::do_not_optimize(acc);
    const double hz = qpbench::cycle_counter_hz();
    std::printf("[clock] steady_clock::now(): %.1f ns per call, advances in steps of %llu ns\n", static_cast<double>(t1 - t0) / n,
                static_cast<unsigned long long>(step_ns));
    std::printf("[clock] raw counter: nominal %.3f MHz, %.1f ns per read, advances in steps of %llu ticks (%.1f ns)\n", hz / 1e6,
                static_cast<double>(c1 - c0) / hz * 1e9 / n, static_cast<unsigned long long>(step_ticks),
                static_cast<double>(step_ticks) / hz * 1e9);
}

// ---------------------------------------------------------------------------------------------
// 2. Pointer chasing: a random single cycle through W bytes, one node per 128-byte block, so
// every load depends on the previous one and the prefetcher cannot guess the next address.
// ---------------------------------------------------------------------------------------------
constexpr std::size_t kNodeBytes = 128;
constexpr std::size_t kStride = kNodeBytes / sizeof(std::uint32_t);

double chase_ns_per_load(std::size_t working_set_bytes, std::mt19937_64& rng) {
    const std::size_t nodes = working_set_bytes / kNodeBytes;
    std::vector<std::uint32_t> order(nodes);
    for (std::size_t i = 0; i < nodes; ++i) order[i] = static_cast<std::uint32_t>(i);
    for (std::size_t i = nodes - 1; i > 0; --i) {  // Sattolo: a uniformly random single cycle
        std::uniform_int_distribution<std::size_t> pick(0, i - 1);
        std::swap(order[i], order[pick(rng)]);
    }
    std::vector<std::uint32_t> next(nodes * kStride, 0);
    for (std::size_t i = 0; i < nodes; ++i) next[order[i] * kStride] = static_cast<std::uint32_t>(order[(i + 1) % nodes] * kStride);
    const std::size_t loads = kSan ? (1u << 14) : (1u << 22);
    std::uint32_t p = 0;
    for (std::size_t i = 0; i < nodes; ++i) p = next[p];  // warm: touch every node once
    const std::uint64_t t0 = qpbench::now_ns();
    for (std::size_t i = 0; i < loads; ++i) p = next[p];
    const std::uint64_t t1 = qpbench::now_ns();
    qpbench::do_not_optimize(p);
    return static_cast<double>(t1 - t0) / static_cast<double>(loads);
}

struct LadderResult {
    double smallest;
    double largest;
};

LadderResult cache_section() {
    std::mt19937_64 rng(7);
    const std::size_t sizes_full[] = {16u << 10, 64u << 10, 256u << 10, 1u << 20, 4u << 20, 16u << 20, 64u << 20, 256u << 20};
    const std::size_t sizes_san[] = {16u << 10, 256u << 10, 4u << 20};
    std::printf("[memory] dependent-load latency by working set (one load per %zu-byte block)\n", kNodeBytes);
    LadderResult r{0, 0};
    auto run = [&](std::size_t ws) {
        const double ns = chase_ns_per_load(ws, rng);
        std::printf("  %8zu KiB  %7.2f ns/load\n", ws >> 10, ns);
        if (r.smallest == 0) r.smallest = ns;
        r.largest = ns;
    };
    if (kSan)
        for (auto ws : sizes_san) run(ws);
    else
        for (auto ws : sizes_full) run(ws);
    return r;
}

// ---------------------------------------------------------------------------------------------
// 3. False sharing: two threads each own one counter; only the distance between them changes.
// ---------------------------------------------------------------------------------------------
double false_sharing_ns_per_update(std::size_t distance_bytes) {
    constexpr std::size_t kArena = 1024;
    auto* arena = static_cast<std::byte*>(::operator new(kArena, std::align_val_t{256}));
    auto* a = ::new (arena) std::atomic<std::uint64_t>(0);
    auto* b = ::new (arena + distance_bytes) std::atomic<std::uint64_t>(0);
    const std::uint64_t n = kSan ? 20'000 : 20'000'000;
    std::atomic<int> ready{0};
    auto work = [&](std::atomic<std::uint64_t>* c) {
        ready.fetch_add(1);
        while (ready.load() < 2) {
        }
        for (std::uint64_t i = 0; i < n; ++i) c->fetch_add(1, std::memory_order_relaxed);
    };
    const std::uint64_t t0 = qpbench::now_ns();
    std::thread ta(work, a);
    std::thread tb(work, b);
    ta.join();
    tb.join();
    const std::uint64_t t1 = qpbench::now_ns();
    const bool ok = a->load() == n && b->load() == n;
    a->~atomic();
    b->~atomic();
    ::operator delete(arena, std::align_val_t{256});
    if (!ok) {
        std::printf("false sharing: lost updates\n");
        std::exit(EXIT_FAILURE);
    }
    return static_cast<double>(t1 - t0) / static_cast<double>(n);
}

struct SharingResult {
    double same_line;
    double far_apart;
};

SharingResult false_sharing_section() {
    std::printf("[false sharing] two threads, relaxed fetch_add increments, median of 5 runs\n");
    SharingResult r{0, 0};
    for (std::size_t d : {8u, 64u, 128u, 256u}) {
        std::vector<double> runs;
        for (int k = 0; k < (kSan ? 1 : 5); ++k) runs.push_back(false_sharing_ns_per_update(d));
        const double med = qpbench::percentile(runs, 50.0);
        std::printf("  counters %3zu bytes apart  %6.2f ns per increment\n", d, med);
        if (d == 8) r.same_line = med;
        if (d == 256) r.far_apart = med;
    }
    return r;
}

// ---------------------------------------------------------------------------------------------
// 4. Branch prediction. The empty asm statement in the taken branch has side effects the
// compiler must preserve, so it cannot turn the branch into a conditional select or vectorise it.
// ---------------------------------------------------------------------------------------------
std::uint64_t branchy_sum(const std::vector<std::uint8_t>& v) {
    std::uint64_t s = 0;
    for (std::uint8_t x : v) {
        if (x >= 128) {
            __asm__ volatile("");
            s += x;
        }
    }
    return s;
}

std::uint64_t branchless_sum(const std::vector<std::uint8_t>& v) {
    std::uint64_t s = 0;
    for (std::uint8_t x : v) s += static_cast<std::uint64_t>(x) & (0 - static_cast<std::uint64_t>(x >= 128));
    return s;
}

struct BranchResult {
    double random_ns;
    double sorted_ns;
};

BranchResult branch_section() {
    const std::size_t n = kSan ? (1u << 14) : (1u << 22);
    std::vector<std::uint8_t> data(n);
    std::mt19937_64 rng(11);
    for (auto& x : data) x = static_cast<std::uint8_t>(rng());
    std::vector<std::uint8_t> sorted = data;
    std::sort(sorted.begin(), sorted.end());
    auto time_it = [&](auto f, const std::vector<std::uint8_t>& v) {
        std::vector<double> runs;
        std::uint64_t check = 0;
        for (int k = 0; k < (kSan ? 1 : 7); ++k) {
            const std::uint64_t t0 = qpbench::now_ns();
            check = f(v);
            const std::uint64_t t1 = qpbench::now_ns();
            qpbench::do_not_optimize(check);
            runs.push_back(static_cast<double>(t1 - t0) / static_cast<double>(v.size()));
        }
        return std::pair{qpbench::percentile(runs, 50.0), check};
    };
    const auto [r_rand, s1] = time_it(branchy_sum, data);
    const auto [r_sort, s2] = time_it(branchy_sum, sorted);
    const auto [r_bl, s3] = time_it(branchless_sum, data);
    if (s1 != s2 || s1 != s3) {
        std::printf("branch sums disagree\n");
        std::exit(EXIT_FAILURE);
    }
    std::printf("[branches] sum of bytes >= 128 over %zu bytes\n", n);
    std::printf("  branchy, random data   %6.3f ns/element\n", r_rand);
    std::printf("  branchy, sorted data   %6.3f ns/element\n", r_sort);
    std::printf("  branchless, random     %6.3f ns/element\n", r_bl);
    return {r_rand, r_sort};
}

// ---------------------------------------------------------------------------------------------
// 5. Jitter: time the same fixed workload many times and look at the tail.
// ---------------------------------------------------------------------------------------------
void jitter_section() {
    const int samples = kSan ? 2'000 : 200'000;
    qpbench::LatencyHistogram<7> hist;
    std::vector<double> raw;
    raw.reserve(static_cast<std::size_t>(samples));
    std::uint64_t x = 1;
    for (int i = 0; i < samples; ++i) {
        const std::uint64_t t0 = qpbench::now_ns();
        for (int k = 0; k < 1000; ++k) x = x * 6364136223846793005ULL + 1442695040888963407ULL;  // dependent chain
        const std::uint64_t t1 = qpbench::now_ns();
        qpbench::do_not_optimize(x);
        hist.record(t1 - t0);
        raw.push_back(static_cast<double>(t1 - t0));
    }
    const auto s = qpbench::summarize(raw);
    std::printf("[jitter] %d timings of a fixed 1000-step dependent chain (ns)\n", samples);
    std::printf("  exact:     p50 %.0f  p90 %.0f  p99 %.0f  p99.9 %.0f  max %.0f  mean %.1f\n", s.p50, s.p90, s.p99, s.p999, s.max, s.mean);
    std::printf("  histogram: p50 %llu  p99 %llu  p99.9 %llu  p99.99 %llu  max %llu\n",
                static_cast<unsigned long long>(hist.percentile(50)), static_cast<unsigned long long>(hist.percentile(99)),
                static_cast<unsigned long long>(hist.percentile(99.9)), static_cast<unsigned long long>(hist.percentile(99.99)),
                static_cast<unsigned long long>(hist.max()));
}

}  // namespace

int main() {
    clock_section();
    const auto ladder = cache_section();
    const auto sharing = false_sharing_section();
    const auto branch = branch_section();
    jitter_section();
    if (kSan) {
        std::printf("sanitized build: timing checks skipped\n");
        return EXIT_SUCCESS;
    }
    bool ok = true;
    ok &= ladder.largest > 3.0 * ladder.smallest;         // DRAM-bound chase is much slower than L1-resident
    ok &= sharing.same_line > 1.5 * sharing.far_apart;    // a shared line ping-pongs between cores
    ok &= branch.random_ns > 1.5 * branch.sorted_ns;      // mispredicted branches cost cycles
    std::printf("%s\n", ok ? "sanity bounds hold" : "SANITY BOUNDS FAILED");
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
