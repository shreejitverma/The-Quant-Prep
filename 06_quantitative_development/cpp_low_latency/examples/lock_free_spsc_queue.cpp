#include <atomic>
#include <vector>
#include <iostream>
#include <thread>

/**
 * @brief Lock-Free Single Producer Single Consumer (SPSC) Ring Buffer.
 *
 * Key Concepts for Interviews:
 * 1. std::atomic for thread-safe indices.
 * 2. std::memory_order_acquire/release to ensure visibility without full fences.
 * 3. Cache line padding (false sharing prevention) using alignas.
 */

template<typename T, size_t Size>
class RingBuffer {
public:
    RingBuffer() : head_(0), tail_(0) {}

    bool push(const T& val) {
        size_t head = head_.load(std::memory_order_relaxed);
        size_t next_head = (head + 1) % Size;

        if (next_head == tail_.load(std::memory_order_acquire)) {
            return false; // Buffer full
        }

        buffer_[head] = val;
        head_.store(next_head, std::memory_order_release);
        return true;
    }

    bool pop(T& val) {
        size_t tail = tail_.load(std::memory_order_relaxed);

        if (tail == head_.load(std::memory_order_acquire)) {
            return false; // Buffer empty
        }

        val = buffer_[tail];
        tail_.store((tail + 1) % Size, std::memory_order_release);
        return true;
    }

private:
    std::vector<T> buffer_{Size};

    // Align to cache line size (usually 64 bytes) to prevent false sharing
    alignas(64) std::atomic<size_t> head_;
    alignas(64) std::atomic<size_t> tail_;
};

int main() {
    RingBuffer<int, 1024> rb;

    std::thread producer([&]() {
        for (int i = 0; i < 1000; ++i) {
            while (!rb.push(i)) {
                // Spin wait strategy often used in low latency
                std::this_thread::yield();
            }
        }
    });

    std::thread consumer([&]() {
        int val;
        for (int i = 0; i < 1000; ++i) {
            while (!rb.pop(val)) {
                std::this_thread::yield();
            }
            // std::cout << "Popped: " << val << std::endl; // IO is slow, avoid in HFT loop
        }
    });

    producer.join();
    consumer.join();
    std::cout << "Finished SPSC test." << std::endl;
    return 0;
}
