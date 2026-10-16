// Portable microbenchmark helpers for the Quant Development notes.
//
// - now_ns(): monotonic nanoseconds from std::chrono::steady_clock (portable; on Apple Silicon
//   it ticks at 24 MHz, so one reading is quantised to 41.67 ns).
// - cycle_counter(): the cheapest monotonic counter the CPU exposes to user space
//   (rdtsc on x86-64, cntvct_el0 on AArch64, steady_clock elsewhere), with its frequency.
// - percentile(): nearest-rank percentile of a sample (sorts a copy).
// - LatencyHistogram: allocation-free log-linear histogram in the style of HdrHistogram,
//   with bounded relative error, for recording millions of latencies on a hot path.
// - MicroBenchmark: warm up, time batches, report percentiles, never just the mean.
//
// Header-only and dependency-free; builds warning-free with -std=c++20 -Wall -Wextra -Wpedantic.

#pragma once

#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

#if defined(__x86_64__) || defined(__i386__)
#include <x86intrin.h>
#endif

// True when built with ASan, UBSan-with-ASan or TSan: benchmarks then shrink their workloads and
// skip timing assertions, because instrumentation changes the very costs being measured.
#if defined(__SANITIZE_ADDRESS__) || defined(__SANITIZE_THREAD__)
#define QP_SANITIZED 1
#elif defined(__has_feature)
#if __has_feature(address_sanitizer) || __has_feature(thread_sanitizer)
#define QP_SANITIZED 1
#endif
#endif
#ifndef QP_SANITIZED
#define QP_SANITIZED 0
#endif

namespace qpbench {

inline constexpr bool kSanitized = QP_SANITIZED != 0;

inline std::uint64_t now_ns() noexcept {
    using namespace std::chrono;
    return static_cast<std::uint64_t>(duration_cast<nanoseconds>(steady_clock::now().time_since_epoch()).count());
}

// Raw user-space counter. On x86-64 the TSC is invariant on modern CPUs but its frequency must be
// calibrated; on AArch64 the generic timer frequency is architecturally readable (cntfrq_el0).
inline std::uint64_t cycle_counter() noexcept {
#if defined(__x86_64__) || defined(__i386__)
    return __rdtsc();
#elif defined(__aarch64__)
    std::uint64_t v;
    __asm__ volatile("isb\n\tmrs %0, cntvct_el0" : "=r"(v) : : "memory");
    return v;
#else
    return now_ns();
#endif
}

// Counter frequency in Hz: read from the register on AArch64, calibrated against steady_clock elsewhere.
inline double cycle_counter_hz() {
#if defined(__aarch64__)
    std::uint64_t f;
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(f));
    return static_cast<double>(f);
#elif defined(__x86_64__) || defined(__i386__)
    const std::uint64_t t0 = now_ns();
    const std::uint64_t c0 = cycle_counter();
    while (now_ns() - t0 < 20'000'000) {
    }
    const std::uint64_t t1 = now_ns();
    const std::uint64_t c1 = cycle_counter();
    return static_cast<double>(c1 - c0) * 1e9 / static_cast<double>(t1 - t0);
#else
    return 1e9;
#endif
}

// Keeps a value alive so the optimiser cannot delete the computation that produced it.
template <typename T>
inline void do_not_optimize(const T& value) noexcept {
    __asm__ volatile("" : : "r,m"(value) : "memory");
}

// Nearest-rank percentile: the smallest sample with at least q percent of the data at or below it.
inline double percentile(std::vector<double> sample, double q) {
    if (sample.empty()) return 0.0;
    std::sort(sample.begin(), sample.end());
    const double rank = q / 100.0 * static_cast<double>(sample.size());
    std::size_t idx = static_cast<std::size_t>(rank);
    if (static_cast<double>(idx) < rank) ++idx;  // ceil
    if (idx == 0) idx = 1;
    return sample[std::min(idx, sample.size()) - 1];
}

// Log-linear histogram over non-negative integer values (e.g. nanoseconds).
// Values below 2^SubBits are recorded exactly; above, each power-of-two range is split into
// 2^(SubBits-1) equal buckets, so the relative error of a reported value is below 2^-(SubBits-1).
// record() is O(1), branch-light and never allocates: suitable for a hot path.
template <unsigned SubBits = 7>
class LatencyHistogram {
    static_assert(SubBits >= 2 && SubBits <= 16);
    static constexpr std::uint64_t kSub = std::uint64_t{1} << SubBits;  // exact region size
    static constexpr std::uint64_t kHalf = kSub / 2;
    static constexpr std::size_t kRanges = 64 - SubBits + 1;
    static constexpr std::size_t kBuckets = kSub + (kRanges - 1) * kHalf;

    std::array<std::uint64_t, kBuckets> counts_{};
    std::uint64_t total_ = 0;
    std::uint64_t max_ = 0;

public:
    static constexpr std::size_t bucket_index(std::uint64_t v) noexcept {
        if (v < kSub) return static_cast<std::size_t>(v);
        const unsigned msb = 63u - static_cast<unsigned>(std::countl_zero(v));  // msb >= SubBits
        const unsigned shift = msb - (SubBits - 1);                             // keep SubBits top bits
        const std::uint64_t top = v >> shift;                                    // in [kHalf, kSub)
        return static_cast<std::size_t>(kSub + (shift - 1) * kHalf + (top - kHalf));
    }
    // Largest value that maps to bucket i (reported value: never under-states a latency).
    static constexpr std::uint64_t bucket_upper(std::size_t i) noexcept {
        if (i < kSub) return i;
        const std::size_t j = i - kSub;
        const unsigned shift = static_cast<unsigned>(j / kHalf) + 1;
        const std::uint64_t top = kHalf + j % kHalf;
        return ((top + 1) << shift) - 1;
    }

    void record(std::uint64_t v) noexcept {
        ++counts_[bucket_index(v)];
        ++total_;
        max_ = std::max(max_, v);
    }
    [[nodiscard]] std::uint64_t count() const noexcept { return total_; }
    [[nodiscard]] std::uint64_t max() const noexcept { return max_; }

    // Nearest-rank percentile, reported as the upper edge of the bucket holding that rank.
    [[nodiscard]] std::uint64_t percentile(double q) const noexcept {
        if (total_ == 0) return 0;
        const double rank_d = q / 100.0 * static_cast<double>(total_);
        auto rank = static_cast<std::uint64_t>(rank_d);
        if (static_cast<double>(rank) < rank_d) ++rank;
        if (rank == 0) rank = 1;
        std::uint64_t seen = 0;
        for (std::size_t i = 0; i < kBuckets; ++i) {
            seen += counts_[i];
            if (seen >= rank) return std::min(bucket_upper(i), max_);
        }
        return max_;
    }
};

struct Summary {
    double p50, p90, p99, p999, max, mean;
};

inline Summary summarize(const std::vector<double>& s) {
    Summary out{};
    if (s.empty()) return out;
    double sum = 0.0;
    for (double x : s) sum += x;
    out.mean = sum / static_cast<double>(s.size());
    out.p50 = percentile(s, 50.0);
    out.p90 = percentile(s, 90.0);
    out.p99 = percentile(s, 99.0);
    out.p999 = percentile(s, 99.9);
    out.max = *std::max_element(s.begin(), s.end());
    return out;
}

// Times `batches` batches of `batch` calls each and reports per-call nanoseconds per batch.
// Batching amortises the clock read and its quantisation; the batch distribution still shows jitter.
class MicroBenchmark {
    std::size_t batches_;
    std::size_t batch_;

public:
    explicit MicroBenchmark(std::size_t batches = 1000, std::size_t batch = 100) : batches_(batches), batch_(batch) {}

    template <typename Func>
    Summary run(const std::string& name, Func&& func, bool print = true) {
        for (std::size_t i = 0; i < batch_ * 10; ++i) func();  // warm caches and branch predictors
        std::vector<double> per_call;
        per_call.reserve(batches_);
        for (std::size_t b = 0; b < batches_; ++b) {
            const std::uint64_t t0 = now_ns();
            for (std::size_t i = 0; i < batch_; ++i) func();
            const std::uint64_t t1 = now_ns();
            per_call.push_back(static_cast<double>(t1 - t0) / static_cast<double>(batch_));
        }
        const Summary s = summarize(per_call);
        if (print) {
            std::printf("%-34s p50 %8.2f  p99 %8.2f  p99.9 %8.2f  max %9.2f  mean %8.2f ns/call\n", name.c_str(), s.p50, s.p99,
                        s.p999, s.max, s.mean);
        }
        return s;
    }
};

}  // namespace qpbench
