#include <atomic>
#include <vector>
#include <iostream>
#include <thread>
#include <chrono>

/**
 * Lock-Free Single-Producer Single-Consumer (SPSC) Queue.
 * 
 * Concept:
 * - Uses a Ring Buffer (circular array).
 * - 'head' is modified by Producer.
 * - 'tail' is modified by Consumer.
 * - 'std::atomic' with 'memory_order_acquire' / 'memory_order_release' ensures
 *   we don't see stale data without needing a full mutex lock.
 * 
 * Usage in HFT:
 * - Thread A (Network): Pushes market data packets.
 * - Thread B (Strategy): Pops packets and processes.
 */

template<typename T, size_t Capacity>
class LockFreeSPSCQueue {
private:
    std::vector<T> buffer;
    alignas(64) std::atomic<size_t> head; // Producer index
    alignas(64) std::atomic<size_t> tail; // Consumer index
    // alignas(64) prevents False Sharing (cache line thrashing)

public:
    LockFreeSPSCQueue() : buffer(Capacity + 1), head(0), tail(0) {}

    bool push(const T& item) {
        size_t current_head = head.load(std::memory_order_relaxed);
        size_t next_head = (current_head + 1) % buffer.size();

        if (next_head == tail.load(std::memory_order_acquire)) {
            return false; // Full
        }

        buffer[current_head] = item;
        head.store(next_head, std::memory_order_release);
        return true;
    }

    bool pop(T& item) {
        size_t current_tail = tail.load(std::memory_order_relaxed);

        if (current_tail == head.load(std::memory_order_acquire)) {
            return false; // Empty
        }

        item = buffer[current_tail];
        tail.store((current_tail + 1) % buffer.size(), std::memory_order_release);
        return true;
    }
};

int main() {
    LockFreeSPSCQueue<int, 1024> queue;

    std::thread producer([&]() {
        for (int i = 0; i < 100; ++i) {
            while (!queue.push(i)) {
                // Busy wait or yield
                std::this_thread::yield();
            }
        }
    });

    std::thread consumer([&]() {
        int val;
        int count = 0;
        while (count < 100) {
            if (queue.pop(val)) {
                // Process val
                count++;
            }
        }
        std::cout << "Consumer finished processing " << count << " items." << std::endl;
    });

    producer.join();
    consumer.join();

    return 0;
}