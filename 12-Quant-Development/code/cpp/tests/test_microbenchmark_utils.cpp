// Unit tests for microbenchmark_utils.hpp (03-Low-Latency-Engineering.md): percentile definition
// and the log-linear latency histogram's bucket mapping and error bound. Framework-free.

#include "microbenchmark_utils.hpp"

#include <cstdint>
#include <iostream>
#include <random>
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

void test_nearest_rank_percentile() {
    std::vector<double> v;
    for (int i = 1; i <= 100; ++i) v.push_back(i);
    EXPECT(qpbench::percentile(v, 50) == 50);
    EXPECT(qpbench::percentile(v, 99) == 99);
    EXPECT(qpbench::percentile(v, 99.5) == 100);
    EXPECT(qpbench::percentile(v, 100) == 100);
    EXPECT(qpbench::percentile(v, 0) == 1);
    EXPECT(qpbench::percentile({}, 50) == 0);
}

void test_bucket_mapping_is_monotone_and_bounded() {
    using H = qpbench::LatencyHistogram<7>;
    std::size_t prev = 0;
    for (std::uint64_t v = 0; v < 1'000'000; ++v) {
        const std::size_t i = H::bucket_index(v);
        if (i < prev) {
            EXPECT(false);
            return;
        }
        prev = i;
        const std::uint64_t up = H::bucket_upper(i);
        if (up < v || (up > v && (up - v) * 64 >= v)) {  // never under-reports; overstates by strictly less than v / 64
            EXPECT(false);
            return;
        }
    }
    EXPECT(H::bucket_index(127) == 127);
    EXPECT(H::bucket_index(128) == 128 && H::bucket_index(129) == 128 && H::bucket_index(130) == 129);
    EXPECT(H::bucket_upper(H::bucket_index(UINT64_MAX)) == UINT64_MAX);
}

void test_histogram_matches_exact_percentiles() {
    qpbench::LatencyHistogram<7> h;
    std::vector<double> exact;
    std::mt19937_64 rng(5);
    std::lognormal_distribution<double> lat(6.5, 0.8);  // ~ hundreds of ns with a long right tail
    for (int i = 0; i < 100'000; ++i) {
        const auto v = static_cast<std::uint64_t>(lat(rng));
        h.record(v);
        exact.push_back(static_cast<double>(v));
    }
    EXPECT(h.count() == 100'000);
    for (double q : {50.0, 90.0, 99.0, 99.9}) {
        const double e = qpbench::percentile(exact, q);
        const auto got = static_cast<double>(h.percentile(q));
        EXPECT(got >= e && got <= e * (1.0 + 1.0 / 64.0));  // never under-reports, within the bucket width
    }
    EXPECT(h.percentile(100) == h.max());
}

}  // namespace

int main() {
    test_nearest_rank_percentile();
    test_bucket_mapping_is_monotone_and_bounded();
    test_histogram_matches_exact_percentiles();
    std::cout << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
