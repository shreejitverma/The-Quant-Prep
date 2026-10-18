// Measures the per-call cost of dispatch styles and of exceptions vs error codes, for
// 02-Cpp-for-Trading-Systems.md. Numbers are machine-dependent; the program asserts only loose
// sanity bounds, and under sanitizers it shrinks the workload and skips the timing checks.
// Build: clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror dispatch_bench.cpp

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <random>
#include <stdexcept>
#include <vector>

#include "cpp_idioms.hpp"
#include "microbenchmark_utils.hpp"

using namespace qpidioms;

namespace {

constexpr std::size_t kObjects = qpbench::kSanitized ? 256 : 4096;
constexpr int kReps = qpbench::kSanitized ? 3 : 31;

// Median over repetitions of (elapsed ns / calls) for one full pass of `body`.
template <typename F>
double median_ns_per_call(F&& body, std::size_t calls) {
    std::vector<double> samples;
    for (int r = 0; r < kReps; ++r) {
        const std::uint64_t t0 = qpbench::now_ns();
        body();
        const std::uint64_t t1 = qpbench::now_ns();
        samples.push_back(static_cast<double>(t1 - t0) / static_cast<double>(calls));
    }
    return qpbench::percentile(samples, 50.0);
}

}  // namespace

int main() {
    std::mt19937_64 rng(42);
    std::vector<Tick> ticks(kObjects);
    for (auto& t : ticks) t = Tick{static_cast<std::int64_t>(1'000'000 + rng() % 1000), static_cast<std::int64_t>(1 + rng() % 100)};
    std::vector<int> random_kind(kObjects);
    for (auto& k : random_kind) k = static_cast<int>(rng() & 1);

    constexpr int kPasses = qpbench::kSanitized ? 4 : 64;
    const std::size_t calls = kObjects * kPasses;
    std::int64_t sink = 0;

    // 1. CRTP: one concrete type, calls resolved at compile time.
    std::vector<MomentumCrtp> crtp(kObjects);
    const double t_crtp = median_ns_per_call(
        [&] {
            for (int p = 0; p < kPasses; ++p)
                for (std::size_t i = 0; i < kObjects; ++i) sink += crtp[i].on_tick(ticks[i]);
            qpbench::do_not_optimize(sink);
        },
        calls);

    // 2. Virtual, every object the same dynamic type (indirect branch always predicted).
    std::vector<std::unique_ptr<IStrategy>> same;
    for (std::size_t i = 0; i < kObjects; ++i) same.push_back(std::make_unique<MomentumVirtual>());
    const double t_virt_same = median_ns_per_call(
        [&] {
            for (int p = 0; p < kPasses; ++p)
                for (std::size_t i = 0; i < kObjects; ++i) sink += same[i]->on_tick(ticks[i]);
            qpbench::do_not_optimize(sink);
        },
        calls);

    // 3. Virtual, two dynamic types in random order (indirect branch target unpredictable).
    std::vector<std::unique_ptr<IStrategy>> mixed;
    for (std::size_t i = 0; i < kObjects; ++i) {
        if (random_kind[i] == 0)
            mixed.push_back(std::make_unique<MomentumVirtual>());
        else
            mixed.push_back(std::make_unique<MeanReversionVirtual>());
    }
    const double t_virt_mixed = median_ns_per_call(
        [&] {
            for (int p = 0; p < kPasses; ++p)
                for (std::size_t i = 0; i < kObjects; ++i) sink += mixed[i]->on_tick(ticks[i]);
            qpbench::do_not_optimize(sink);
        },
        calls);

    // 4. std::variant + std::visit with the same random mix, objects stored contiguously.
    std::vector<AnyStrategy> variants;
    for (std::size_t i = 0; i < kObjects; ++i) {
        if (random_kind[i] == 0)
            variants.emplace_back(MomentumCrtp{});
        else
            variants.emplace_back(MeanReversionCrtp{});
    }
    const double t_variant_mixed = median_ns_per_call(
        [&] {
            for (int p = 0; p < kPasses; ++p)
                for (std::size_t i = 0; i < kObjects; ++i) sink += on_tick(variants[i], ticks[i]);
            qpbench::do_not_optimize(sink);
        },
        calls);

    // 5. Same mix, sorted by type: the branch predictor now sees long runs.
    std::vector<AnyStrategy> sorted_variants = variants;
    std::stable_sort(sorted_variants.begin(), sorted_variants.end(), [](const AnyStrategy& a, const AnyStrategy& b) { return a.index() < b.index(); });
    const double t_variant_sorted = median_ns_per_call(
        [&] {
            for (int p = 0; p < kPasses; ++p)
                for (std::size_t i = 0; i < kObjects; ++i) sink += on_tick(sorted_variants[i], ticks[i]);
            qpbench::do_not_optimize(sink);
        },
        calls);

    // 6. Errors: every call fails, reported by error code vs by exception.
    const std::size_t err_calls = qpbench::kSanitized ? 200 : 2'000;
    std::vector<std::int64_t> bad_qty(err_calls);  // loaded from memory so the checks cannot be constant-folded
    for (auto& q : bad_qty) q = -static_cast<std::int64_t>(rng() % 7);
    const double t_errcode = median_ns_per_call(
        [&] {
            for (std::size_t i = 0; i < err_calls; ++i) {
                const auto r = validate_order(Price{1'000'000}, bad_qty[i], 1'000'000'000);
                sink += r.has_value() ? r.value() : static_cast<std::int64_t>(r.error()) + 1;
                qpbench::do_not_optimize(sink);
            }
            qpbench::do_not_optimize(sink);
        },
        err_calls);
    const double t_throw = median_ns_per_call(
        [&] {
            for (std::size_t i = 0; i < err_calls; ++i) {
                try {
                    sink += validate_order_or_throw(Price{1'000'000}, bad_qty[i], 1'000'000'000);
                } catch (const std::invalid_argument&) {
                    ++sink;
                }
            }
            qpbench::do_not_optimize(sink);
        },
        err_calls);

    std::printf("dispatch cost, median of %d reps, ns per call (%zu objects):\n", kReps, kObjects);
    std::printf("  CRTP, one type                 %7.2f\n", t_crtp);
    std::printf("  virtual, one dynamic type      %7.2f\n", t_virt_same);
    std::printf("  virtual, two types random      %7.2f\n", t_virt_mixed);
    std::printf("  variant, two types random      %7.2f\n", t_variant_mixed);
    std::printf("  variant, two types sorted      %7.2f\n", t_variant_sorted);
    std::printf("error path, ns per failed call:\n");
    std::printf("  error code                     %7.2f\n", t_errcode);
    std::printf("  throw + catch                  %7.2f\n", t_throw);
    std::printf("ratios: virtual random / CRTP %.1fx, throw / error code %.0fx\n", t_virt_mixed / t_crtp, t_throw / t_errcode);

    if (qpbench::kSanitized) {
        std::printf("sanitized build: timing checks skipped\n");
        return EXIT_SUCCESS;
    }
    // Loose sanity bounds only: the qualitative ordering, not the machine-specific values.
    bool ok = true;
    ok &= t_virt_mixed > t_crtp;     // an unpredictable indirect call never beats an inlined call
    ok &= t_throw > 10.0 * t_errcode;  // a throw costs far more than a compare and branch
    std::printf("%s\n", ok ? "sanity bounds hold" : "SANITY BOUNDS FAILED");
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
