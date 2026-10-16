// Benchmarks for 07-Order-Book-and-Matching-Engine.md, measured on the machine it runs on:
//   1. the matching engine (lob_engine.hpp) on a seeded synthetic flow: throughput and per-operation
//      latency percentiles;
//   2. three price-level containers under the same access pattern (most activity near the touch):
//      std::map, a sorted std::vector with the best level at the back, and a tick-indexed array.
// Machine-dependent numbers; only loose orderings are asserted, and sanitizer builds shrink the
// workloads and skip the timing checks.
// Build: clang++ -std=c++20 -O2 lob_bench.cpp

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <map>
#include <random>
#include <vector>

#include "lob_engine.hpp"
#include "microbenchmark_utils.hpp"

namespace {

constexpr bool kSan = qpbench::kSanitized;

// ------------------------------------------------------------------ 1. engine
struct Pcts {
    std::uint64_t p50, p99, p999;
};

struct EngineResult {
    double ns_per_op;
    Pcts by_kind[3];  // passive add, cancel, marketable IOC
    std::uint64_t max;
    std::uint64_t fills;
    std::size_t resting;
};

EngineResult engine_bench() {
    using namespace lob;
    const int ops = kSan ? 20'000 : 2'000'000;
    OrderBook book(1u << 20);
    std::mt19937_64 rng(42);
    std::geometric_distribution<int> depth(0.35);  // passive orders cluster at the touch
    std::vector<OrderId> live;
    live.reserve(1u << 20);
    std::vector<Event> ev;
    ev.reserve(64);
    constexpr Price kMid = 10'000;
    OrderId next = 1;
    std::uint64_t fills = 0;
    std::vector<qpbench::LatencyHistogram<7>> hist(3);
    const double hz = qpbench::cycle_counter_hz();
    // Pre-generate the operations so the timed loop measures the engine, not the generator.
    struct Op {
        int kind;  // 0 passive add, 1 cancel, 2 marketable IOC
        NewOrder o;
        std::uint64_t cancel_pick;
    };
    std::vector<Op> plan(static_cast<std::size_t>(ops));
    for (auto& p : plan) {
        const auto r = rng() % 100;
        const Side s = (rng() & 1) ? Side::Buy : Side::Sell;
        const Price off = 1 + depth(rng);
        if (r < 45) {
            p = {0, NewOrder{0, static_cast<TraderId>(rng() % 50), s, OrdType::Limit, Tif::Day, s == Side::Buy ? kMid - off : kMid + off,
                             static_cast<Qty>(1 + rng() % 10)},
                 0};
        } else if (r < 90) {
            p = {1, {}, rng()};
        } else {
            p = {2, NewOrder{0, static_cast<TraderId>(rng() % 50), s, OrdType::Limit, Tif::Ioc, s == Side::Buy ? kMid + 2 : kMid - 2,
                             static_cast<Qty>(1 + rng() % 15)},
                 0};
        }
    }
    const std::uint64_t t0 = qpbench::now_ns();
    for (auto& p : plan) {
        ev.clear();
        const std::uint64_t c0 = qpbench::cycle_counter();
        if (p.kind == 1) {
            if (!live.empty()) {
                const std::size_t k = p.cancel_pick % live.size();
                book.cancel(live[k], ev);
                live[k] = live.back();  // stale ids (already filled) are cancelled harmlessly: rejected
                live.pop_back();
            }
        } else {
            p.o.id = next++;
            book.submit(p.o, ev);
            if (p.kind == 0) live.push_back(p.o.id);
        }
        const std::uint64_t c1 = qpbench::cycle_counter();
        hist[static_cast<std::size_t>(p.kind)].record(static_cast<std::uint64_t>(static_cast<double>(c1 - c0) * 1e9 / hz));
        for (const auto& e : ev) fills += e.type == EventType::Fill;
    }
    const std::uint64_t t1 = qpbench::now_ns();
    EngineResult out{static_cast<double>(t1 - t0) / ops, {}, 0, fills, book.order_count()};
    for (std::size_t k = 0; k < 3; ++k) {
        out.by_kind[k] = {hist[k].percentile(50), hist[k].percentile(99), hist[k].percentile(99.9)};
        out.max = std::max(out.max, hist[k].max());
    }
    return out;
}

// ------------------------------------------------------------------ 2. level containers (ask side)
// Operation stream: at price best + k (k geometric), either add quantity or remove the whole level.
struct LevelOp {
    std::int64_t offset;
    std::int64_t qty;  // > 0 add, 0 remove
};

struct MapLevels {
    std::map<std::int64_t, std::int64_t> m;
    void add(std::int64_t p, std::int64_t q) { m[p] += q; }
    void remove(std::int64_t p) { m.erase(p); }
    std::int64_t best() const { return m.empty() ? 0 : m.begin()->first; }
};

struct VectorLevels {  // sorted descending, best (lowest ask) at the back: touch updates are near the end
    std::vector<std::pair<std::int64_t, std::int64_t>> v;
    VectorLevels() { v.reserve(4096); }
    auto find(std::int64_t p) {
        return std::lower_bound(v.begin(), v.end(), p, [](const auto& lv, std::int64_t x) { return lv.first > x; });
    }
    void add(std::int64_t p, std::int64_t q) {
        auto it = find(p);
        if (it != v.end() && it->first == p)
            it->second += q;
        else
            v.insert(it, {p, q});
    }
    void remove(std::int64_t p) {
        auto it = find(p);
        if (it != v.end() && it->first == p) v.erase(it);
    }
    std::int64_t best() const { return v.empty() ? 0 : v.back().first; }
};

struct ArrayLevels {  // one slot per tick in a fixed band, plus the index of the best level
    static constexpr std::int64_t kTicks = 1 << 16;
    std::int64_t base;
    std::vector<std::int64_t> qty;
    std::int64_t best_idx = kTicks;
    explicit ArrayLevels(std::int64_t base_price) : base(base_price), qty(static_cast<std::size_t>(kTicks), 0) {}
    void add(std::int64_t p, std::int64_t q) {
        const std::int64_t i = p - base;
        qty[static_cast<std::size_t>(i)] += q;
        best_idx = std::min(best_idx, i);
    }
    void remove(std::int64_t p) {
        const std::int64_t i = p - base;
        qty[static_cast<std::size_t>(i)] = 0;
        if (i == best_idx)
            while (best_idx < kTicks && qty[static_cast<std::size_t>(best_idx)] == 0) ++best_idx;  // scan to the next level
    }
    std::int64_t best() const { return best_idx == kTicks ? 0 : base + best_idx; }
};

template <typename L>
double level_ns_per_op(L& levels, const std::vector<LevelOp>& ops, std::int64_t& checksum) {
    const std::uint64_t t0 = qpbench::now_ns();
    for (const auto& op : ops) {
        const std::int64_t touch = levels.best() == 0 ? 20'000 : levels.best();
        const std::int64_t p = std::max<std::int64_t>(20'000, touch - 1 + op.offset);  // can improve the touch by one tick
        if (op.qty > 0)
            levels.add(p, op.qty);
        else
            levels.remove(p);
        checksum += levels.best();
    }
    const std::uint64_t t1 = qpbench::now_ns();
    return static_cast<double>(t1 - t0) / static_cast<double>(ops.size());
}

}  // namespace

int main() {
    const auto e = engine_bench();
    std::printf("[engine] synthetic flow (45%% passive adds, 45%% cancels, 10%% marketable IOC), seed 42\n");
    std::printf("  %.1f ns/op mean (%.1f M ops/s), fills %llu, resting orders at end %zu\n", e.ns_per_op, 1e3 / e.ns_per_op,
                static_cast<unsigned long long>(e.fills), e.resting);
    const char* kinds[] = {"passive add", "cancel", "marketable IOC"};
    for (std::size_t k = 0; k < 3; ++k)
        std::printf("  %-15s p50 %5llu ns  p99 %6llu ns  p99.9 %7llu ns\n", kinds[k], static_cast<unsigned long long>(e.by_kind[k].p50),
                    static_cast<unsigned long long>(e.by_kind[k].p99), static_cast<unsigned long long>(e.by_kind[k].p999));
    std::printf("  max over all operations %llu ns\n", static_cast<unsigned long long>(e.max));
    // Observed granularity: the median nonzero advance of the raw counter. On Apple M3 the AArch64
    // virtual counter reports 1 GHz but advances in steps of about 42 ns.
    const double hz = qpbench::cycle_counter_hz();
    std::vector<std::uint64_t> steps(1001);
    for (auto& st : steps) {
        const std::uint64_t c0 = qpbench::cycle_counter();
        std::uint64_t c1 = c0;
        while (c1 == c0) c1 = qpbench::cycle_counter();
        st = c1 - c0;
    }
    std::nth_element(steps.begin(), steps.begin() + 500, steps.end());
    std::printf("  latency counter reports %.0f Hz and advances in steps of %.0f ns (median): percentiles are quantised to that step\n",
                hz, static_cast<double>(steps[500]) * 1e9 / hz);

    std::mt19937_64 rng(7);
    std::geometric_distribution<int> depth(0.3);
    std::vector<LevelOp> ops(kSan ? 20'000 : 2'000'000);
    for (auto& op : ops) op = {depth(rng), (rng() % 3 == 0) ? 0 : static_cast<std::int64_t>(1 + rng() % 100)};
    std::int64_t c_map = 0, c_vec = 0, c_arr = 0;
    MapLevels ml;
    VectorLevels vl;
    ArrayLevels al(20'000 - 100);
    const double t_map = level_ns_per_op(ml, ops, c_map);
    const double t_vec = level_ns_per_op(vl, ops, c_vec);
    const double t_arr = level_ns_per_op(al, ops, c_arr);
    std::printf("[levels] %zu add/remove operations near the touch, ns/op\n", ops.size());
    std::printf("  std::map            %6.2f  (%zu levels at end)\n", t_map, ml.m.size());
    std::printf("  sorted std::vector  %6.2f\n", t_vec);
    std::printf("  tick-indexed array  %6.2f\n", t_arr);
    const bool same = c_map == c_vec && c_map == c_arr;
    std::printf("  containers agree on every best price: %s\n", same ? "yes" : "NO");
    if (!same || e.fills == 0) return EXIT_FAILURE;
    if (kSan) {
        std::printf("sanitized build: timing checks skipped\n");
        return EXIT_SUCCESS;
    }
    bool ok = true;
    ok &= t_arr < t_map;          // contiguous, no node allocation, no pointer chasing
    for (const auto& k : e.by_kind) ok &= k.p50 <= k.p999;  // guards the histogram plumbing
    ok &= e.ns_per_op < 10'000;   // a book update is well under 10 us on any modern core
    std::printf("%s\n", ok ? "sanity bounds hold" : "SANITY BOUNDS FAILED");
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
