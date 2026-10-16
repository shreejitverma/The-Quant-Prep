// Multithreaded Monte Carlo pricer for a European call (04-Concurrency-Lock-Free-and-Memory-Pools.md).
//
// Demonstrates:
// 1. Task-based parallelism with std::async: each task owns its inputs and returns its partial
//    sums, so there is no shared mutable state and nothing to lock.
// 2. One random engine per task, seeded from (base seed, task index): reproducible for a fixed
//    task count, and no contention on a shared generator.
// 3. Every path is simulated exactly once (the remainder of total / tasks is spread over the
//    first tasks), and the estimate is checked against the Black-Scholes price within 4 standard
//    errors.
// Build: clang++ -std=c++20 -O2 -pthread multithreaded_monte_carlo.cpp

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <future>
#include <random>
#include <thread>
#include <vector>

namespace {

struct Partial {
    double sum = 0.0;     // sum of payoffs
    double sum_sq = 0.0;  // sum of squared payoffs, for the standard error
};

Partial simulate(std::uint64_t paths, std::uint64_t seed, std::uint64_t task, double S, double K, double r, double v, double T) {
    std::seed_seq seq{static_cast<std::uint32_t>(seed), static_cast<std::uint32_t>(task)};
    std::mt19937_64 rng(seq);
    std::normal_distribution<double> normal(0.0, 1.0);
    const double drift = (r - 0.5 * v * v) * T;
    const double vol_sqrt_t = v * std::sqrt(T);
    Partial p;
    for (std::uint64_t i = 0; i < paths; ++i) {
        const double s_t = S * std::exp(drift + vol_sqrt_t * normal(rng));
        const double payoff = std::max(s_t - K, 0.0);
        p.sum += payoff;
        p.sum_sq += payoff * payoff;
    }
    return p;
}

double norm_cdf(double x) { return 0.5 * std::erfc(-x / std::sqrt(2.0)); }

double black_scholes_call(double S, double K, double r, double v, double T) {
    const double d1 = (std::log(S / K) + (r + 0.5 * v * v) * T) / (v * std::sqrt(T));
    const double d2 = d1 - v * std::sqrt(T);
    return S * norm_cdf(d1) - K * std::exp(-r * T) * norm_cdf(d2);
}

}  // namespace

int main() {
    const double S = 100.0, K = 100.0, r = 0.05, v = 0.2, T = 1.0;
    const std::uint64_t total_paths = 4'000'000;
    const std::uint64_t seed = 20261016;
    const unsigned hw = std::thread::hardware_concurrency();
    const std::uint64_t tasks = hw == 0 ? 4 : hw;  // hardware_concurrency may return 0

    const auto t0 = std::chrono::steady_clock::now();
    std::vector<std::future<Partial>> futures;
    futures.reserve(tasks);
    for (std::uint64_t i = 0; i < tasks; ++i) {
        const std::uint64_t paths = total_paths / tasks + (i < total_paths % tasks ? 1 : 0);
        futures.push_back(std::async(std::launch::async, simulate, paths, seed, i, S, K, r, v, T));
    }
    Partial all;
    for (auto& f : futures) {
        const Partial p = f.get();
        all.sum += p.sum;
        all.sum_sq += p.sum_sq;
    }
    const auto t1 = std::chrono::steady_clock::now();

    const double n = static_cast<double>(total_paths);
    const double disc = std::exp(-r * T);
    const double mean = all.sum / n;
    const double var = all.sum_sq / n - mean * mean;
    const double price = disc * mean;
    const double std_err = disc * std::sqrt(var / n);
    const double bs = black_scholes_call(S, K, r, v, T);
    const double z = (price - bs) / std_err;
    const double secs = std::chrono::duration<double>(t1 - t0).count();

    std::printf("European call S=%.0f K=%.0f r=%.2f vol=%.2f T=%.0f, %llu paths over %llu tasks\n", S, K, r, v, T,
                static_cast<unsigned long long>(total_paths), static_cast<unsigned long long>(tasks));
    std::printf("Monte Carlo %.4f (std err %.4f), Black-Scholes %.4f, z = %.2f\n", price, std_err, bs, z);
    std::printf("%.3f s, %.1f M paths/s (machine-dependent)\n", secs, n / secs / 1e6);
    const bool ok = std::abs(z) < 4.0 && std::abs(bs - 10.4506) < 5e-5;
    std::printf("%s\n", ok ? "within 4 standard errors of Black-Scholes" : "MONTE CARLO CHECK FAILED");
    return ok ? 0 : 1;
}
