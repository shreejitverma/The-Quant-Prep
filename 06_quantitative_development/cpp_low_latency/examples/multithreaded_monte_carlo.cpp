#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <thread>
#include <future>
#include <chrono>

/**
 * Multithreaded Monte Carlo Option Pricer.
 * 
 * Demonstrates:
 * 1. Parallel execution using std::async (Task-based parallelism).
 * 2. Thread-local Random Number Generation (avoiding locking contention).
 * 3. Numerical integration for derivatives pricing.
 */

// Function to generate Gaussian noise (Box-Muller transform or std::normal_distribution)
// We use a thread-local generator for performance.
double calculate_payoff_sum(int num_sims, double S, double K, double r, double v, double T) {
    // Thread-local random number engine
    static thread_local std::mt19937 generator(std::hash<std::thread::id>{}(std::this_thread::get_id()));
    std::normal_distribution<double> distribution(0.0, 1.0);

    double payoff_sum = 0.0;
    double drift = (r - 0.5 * v * v) * T;
    double vol_sqrt_T = v * std::sqrt(T);

    for (int i = 0; i < num_sims; ++i) {
        double Z = distribution(generator);
        double S_T = S * std::exp(drift + vol_sqrt_T * Z);
        payoff_sum += std::max(S_T - K, 0.0); // Call Option Payoff
    }
    return payoff_sum;
}

int main() {
    // Option Parameters
    double S = 100.0;  // Spot Price
    double K = 100.0;  // Strike Price
    double r = 0.05;   // Risk-free Rate
    double v = 0.2;    // Volatility
    double T = 1.0;    // Time to Maturity (1 year)
    
    int total_sims = 10'000'000;
    int num_threads = std::thread::hardware_concurrency();
    int sims_per_thread = total_sims / num_threads;

    std::cout << "Pricing Call Option (S=" << S << ", K=" << K << ")...\n";
    std::cout << "Simulations: " << total_sims << " | Threads: " << num_threads << "\n";

    auto start_time = std::chrono::high_resolution_clock::now();

    // Launch tasks
    std::vector<std::future<double>> futures;
    for (int i = 0; i < num_threads; ++i) {
        futures.push_back(std::async(std::launch::async, calculate_payoff_sum, sims_per_thread, S, K, r, v, T));
    }

    // Aggregate results
    double total_payoff = 0.0;
    for (auto& f : futures) {
        total_payoff += f.get();
    }

    double price = (total_payoff / total_sims) * std::exp(-r * T);

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    std::cout << "------------------------------------------------\n";
    std::cout << "Call Price: " << price << "\n";
    std::cout << "Time Taken: " << elapsed.count() << " seconds\n";
    std::cout << "Sims/Sec:   " << total_sims / elapsed.count() << "\n";

    return 0;
}
