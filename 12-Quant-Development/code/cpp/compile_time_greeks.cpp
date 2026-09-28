// Compile-time lookup table for the standard normal CDF, N(x).
//
// Hot pricing paths often replace transcendental calls with a table plus interpolation.
// Here the table is built entirely at compile time: std::exp is not constexpr before
// C++26, so we supply a constexpr exp, and N(x) uses Abramowitz-Stegun 26.2.17
// (absolute error below 7.5e-8). Build: g++ -std=c++20 -O2 compile_time_greeks.cpp

#include <array>
#include <cmath>
#include <cstddef>
#include <iostream>

// exp(x) for |x| <= ~50: range-reduce by powers of two, then a Taylor series on |r| <= 1/64.
constexpr double cexp(double x) {
    if (x == 0.0) return 1.0;
    int halvings = 0;
    double r = x;
    while (r > 1.0 / 64 || r < -1.0 / 64) {
        r /= 2.0;
        ++halvings;
    }
    double term = 1.0;
    double sum = 1.0;
    for (int k = 1; k < 20; ++k) {
        term *= r / k;
        sum += term;
    }
    for (int i = 0; i < halvings; ++i) sum *= sum;  // exp(x) = exp(x / 2^h)^(2^h)
    return sum;
}

constexpr double normal_cdf(double x) {
    if (x < 0.0) return 1.0 - normal_cdf(-x);
    constexpr double p = 0.2316419;
    constexpr double b1 = 0.319381530, b2 = -0.356563782, b3 = 1.781477937, b4 = -1.821255978, b5 = 1.330274429;
    constexpr double inv_sqrt_2pi = 0.3989422804014327;
    const double t = 1.0 / (1.0 + p * x);
    const double poly = t * (b1 + t * (b2 + t * (b3 + t * (b4 + t * b5))));  // Horner form
    return 1.0 - inv_sqrt_2pi * cexp(-0.5 * x * x) * poly;
}

template <std::size_t N>
struct NormalCdfTable {
    static_assert(N >= 2, "need at least two grid points");
    std::array<double, N> values{};
    double min_x;
    double max_x;
    double step;

    constexpr NormalCdfTable(double lo, double hi) : min_x(lo), max_x(hi), step((hi - lo) / (N - 1)) {
        for (std::size_t i = 0; i < N; ++i) values[i] = normal_cdf(min_x + static_cast<double>(i) * step);
    }

    // O(1) lookup with linear interpolation; clamps to the table's end values outside [min_x, max_x].
    constexpr double operator()(double x) const {
        if (x <= min_x) return values.front();
        if (x >= max_x) return values.back();
        const double pos = (x - min_x) / step;
        const auto i = static_cast<std::size_t>(pos);
        const double w = pos - static_cast<double>(i);
        return values[i] + w * (values[i + 1] - values[i]);
    }
};

// Lives in read-only data: no runtime initialisation, no transcendental calls at lookup time.
constexpr NormalCdfTable<4097> cdf_table(-8.0, 8.0);

static_assert(cdf_table(0.0) > 0.4999999 && cdf_table(0.0) < 0.5000001, "N(0) must be 1/2");
static_assert(cdf_table(1.96) > 0.97499 && cdf_table(1.96) < 0.97501, "N(1.96) must be about 0.975");
static_assert(cexp(1.0) > 2.718281828 && cexp(1.0) < 2.718281829, "constexpr exp is inaccurate");

int main() {
    double worst = 0.0;
    for (double x = -6.0; x <= 6.0; x += 0.001) {
        const double exact = 0.5 * std::erfc(-x / std::sqrt(2.0));
        worst = std::max(worst, std::abs(cdf_table(x) - exact));
    }
    std::cout << "N(0)    = " << cdf_table(0.0) << '\n'
              << "N(1.96) = " << cdf_table(1.96) << '\n'
              << "max |table - erfc| on [-6, 6] = " << worst << '\n';
    return worst < 1e-6 ? 0 : 1;  // table error: A-S 7.5e-8 plus interpolation error h^2/8 * max|N''|
}
