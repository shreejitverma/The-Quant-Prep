// SPSC ring buffer demo: a "network" thread pushes sequenced market-data updates, a "strategy"
// thread pops them and checks that nothing was lost, duplicated or reordered.
// The queue itself lives in lock_free.hpp. Runs clean under ThreadSanitizer.
// Build: clang++ -std=c++20 -O2 -pthread lock_free_spsc_queue.cpp

#include <cstdint>
#include <cstdio>
#include <thread>

#include "lock_free.hpp"

struct Update {
    std::uint64_t seq = 0;
    std::int64_t price = 0;
};

int main() {
    constexpr std::uint64_t kMessages = 200'000;
    qpconc::SpscQueue<Update, 1024> queue;

    std::thread producer([&] {
        for (std::uint64_t i = 1; i <= kMessages; ++i) {
            const Update u{i, static_cast<std::int64_t>(1'000'000 + i % 100)};
            while (!queue.try_push(u)) std::this_thread::yield();  // full: back off (a pinned thread would spin)
        }
    });

    std::uint64_t received = 0;
    std::uint64_t expected_seq = 1;
    std::uint64_t gaps = 0;
    std::int64_t price_sum = 0;
    std::thread consumer([&] {
        Update u;
        while (received < kMessages) {
            if (!queue.try_pop(u)) {
                std::this_thread::yield();
                continue;
            }
            if (u.seq != expected_seq) ++gaps;
            expected_seq = u.seq + 1;
            price_sum += u.price;
            ++received;
        }
    });

    producer.join();
    consumer.join();

    // sum over i = 1..200000 of (1e6 + i mod 100): 2000 full cycles of 0..99 contribute 2000 * 4950.
    const std::int64_t want = static_cast<std::int64_t>(kMessages) * 1'000'000 + 2000 * 4950;
    std::printf("received %llu updates, %llu sequence gaps, price checksum %s\n", static_cast<unsigned long long>(received),
                static_cast<unsigned long long>(gaps), price_sum == want ? "ok" : "MISMATCH");
    return (received == kMessages && gaps == 0 && price_sum == want) ? 0 : 1;
}
