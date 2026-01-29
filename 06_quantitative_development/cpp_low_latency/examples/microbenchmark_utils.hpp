#pragma once

#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

// RDTSC: Read Time-Stamp Counter
// Returns the number of clock cycles since the CPU was powered up.
static inline uint64_t rdtsc() {
    unsigned int lo, hi;
    // 'volatile' prevents compiler reordering
    __asm__ volatile ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

class MicroBenchmark {
private:
    std::vector<uint64_t> measurements;
    const int iterations;

public:
    MicroBenchmark(int iters = 1000) : iterations(iters) {
        measurements.reserve(iters);
    }

    template <typename Func>
    void run(const std::string& name, Func&& func) {
        measurements.clear();
        
        // Warmup (cache loading)
        for (int i = 0; i < 100; ++i) {
            func();
        }

        for (int i = 0; i < iterations; ++i) {
            uint64_t start = rdtsc();
            func();
            uint64_t end = rdtsc();
            measurements.push_back(end - start);
        }

        print_stats(name);
    }

private:
    void print_stats(const std::string& name) {
        if (measurements.empty()) return;

        std::sort(measurements.begin(), measurements.end());

        double avg = std::accumulate(measurements.begin(), measurements.end(), 0.0) / measurements.size();
        uint64_t min = measurements.front();
        uint64_t max = measurements.back();
        uint64_t p50 = measurements[measurements.size() / 2];
        uint64_t p99 = measurements[measurements.size() * 0.99];

        std::cout << "--- Benchmark: " << name << " ---" << std::endl;
        std::cout << "Cycles (Avg): " << avg << std::endl;
        std::cout << "Cycles (Min): " << min << std::endl;
        std::cout << "Cycles (P50): " << p50 << std::endl;
        std::cout << "Cycles (P99): " << p99 << std::endl; // Tail latency
        std::cout << "--------------------------------" << std::endl;
    }
};

/* Example Usage
int main() {
    MicroBenchmark bench;
    int x = 0;
    bench.run("Increment", [&](){
        x++;
    });
    return 0;
}
*/
