#include <iostream>
#include <array>
#include <cmath>

/**
 * Compile-Time Math using C++20 'consteval' / 'constexpr'.
 * 
 * In HFT, we often replace runtime math functions (pow, exp, sqrt) with:
 * 1. Lookup Tables (LUT).
 * 2. Polynomial Approximations.
 * 
 * This example generates a Standard Normal CDF Lookup Table at compile time.
 */

// Approximate CDF of Normal Distribution (Error < 0.0003)
constexpr double normal_cdf(double x) {
    // Constants for approximation
    constexpr double p = 0.2316419;
    constexpr double b1 = 0.319381530;
    constexpr double b2 = -0.356563782;
    constexpr double b3 = 1.781477937;
    constexpr double b4 = -1.821255978;
    constexpr double b5 = 1.330274429;

    if (x < 0.0) return 1.0 - normal_cdf(-x);

    double t = 1.0 / (1.0 + p * x);
    double pdf = (1.0 / 2.50662827463) * std::exp(-0.5 * x * x); // 1/sqrt(2pi)
    
    return 1.0 - pdf * (b1*t + b2*t*t + b3*t*t*t + b4*t*t*t*t + b5*t*t*t*t*t);
}

// Generate LUT at compile time
template<size_t N>
struct NormalCDFTable {
    std::array<double, N> values;
    double min_x;
    double max_x;
    double step;

    constexpr NormalCDFTable(double min_val, double max_val) 
        : values{}, min_x(min_val), max_x(max_val), step((max_val - min_val) / (N - 1)) {
        
        for (size_t i = 0; i < N; ++i) {
            double x = min_x + i * step;
            values[i] = normal_cdf(x);
        }
    }

    // Runtime lookup is O(1) array access
    constexpr double lookup(double x) const {
        if (x <= min_x) return 0.0;
        if (x >= max_x) return 1.0;
        
        size_t index = static_cast<size_t>((x - min_x) / step);
        return values[index];
    }
};

// Create the table in the data segment (zero runtime initialization cost)
constexpr auto cdf_table = NormalCDFTable<1000>(-4.0, 4.0);

int main() {
    // This value is fetched from memory, no calculation performed at runtime.
    std::cout << "N(0.0) = " << cdf_table.lookup(0.0) << std::endl;
    std::cout << "N(1.96) = " << cdf_table.lookup(1.96) << std::endl;
    
    static_assert(cdf_table.lookup(0.0) > 0.49 && cdf_table.lookup(0.0) < 0.51, "Compile time check failed");

    return 0;
}
