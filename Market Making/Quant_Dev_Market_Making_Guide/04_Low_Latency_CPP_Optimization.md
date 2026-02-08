# Low-Latency C++ Optimization for High-Frequency Trading

**Target:** Sub-microsecond (<1µs) tick-to-trade latency.
**Scope:** C++17/20, Hardware Architecture, Operating System Tuning.

---

## 1. The Critical Path (Hot Path)

In HFT, the "Hot Path" is the code execution path triggered by a market data packet arrival leading to an order submission.

**Goal:** Zero allocations, zero system calls, zero context switches, minimal cache misses.

### 1.1 Do's and Don'ts

| Feature | Hot Path Usage | Reason |
| :--- | :--- | :--- |
| `new` / `malloc` | **NEVER** | Heap allocation involves locks and non-deterministic latency. |
| `std::shared_ptr` | **NEVER** | Atomic reference counting overhead. |
| `std::vector` (resize) | **NEVER** | Reallocation causes copy + free. Use `reserve()` upfront. |
| `std::map` / `unordered_map` | **AVOID** | Node-based cache thrashing. Use flat maps or open-addressing. |
| `try` / `catch` | **AVOID** | Stack unwinding tables bloat binary; throwing is slow. |
| `virtual` functions | **AVOID** | V-table lookup = cache miss + inhibits inlining. Use CRTP. |
| `logging` (IO) | **NEVER** | Disk I/O is slow. Push to a lock-free queue; log from a separate thread. |

---

## 2. Compile-Time Polymorphism (CRTP)

Virtual functions introduce runtime overhead. In HFT, we know our types at compile time.

**Pattern: Curiously Recurring Template Pattern (CRTP)**

```cpp
// SLOW: Runtime Polymorphism
class StrategyBase {
public:
    virtual void on_tick(const Tick& t) = 0; // V-table lookup
};

// FAST: Compile-Time Polymorphism
template <typename Derived>
class StrategyHost {
public:
    void process_tick(const Tick& t) {
        // Direct call, inlined by compiler
        static_cast<Derived*>(this)->on_tick(t);
    }
};

class VWAPStrategy : public StrategyHost<VWAPStrategy> {
public:
    void on_tick(const Tick& t) {
        // logic
    }
};
```

---

## 3. Memory Management & Cache Locality

### 3.1 Custom Allocators (Pool / Arena)
Pre-allocate all necessary objects at startup.

```cpp
template <typename T, size_t Size>
class ObjectPool {
    std::array<T, Size> data_;
    std::vector<T*> free_list_;
public:
    ObjectPool() {
        free_list_.reserve(Size);
        for(auto& item : data_) free_list_.push_back(&item);
    }
    
    T* allocate() {
        if (free_list_.empty()) return nullptr; // Or fallback
        T* ptr = free_list_.back();
        free_list_.pop_back();
        return ptr;
    }
    
    void deallocate(T* ptr) {
        free_list_.push_back(ptr);
    }
};
```

### 3.2 Data Layout (Structure of Arrays)
CPUs fetch memory in Cache Lines (usually 64 bytes).

*   **Bad (OOP):** `struct Order { double price; double size; int id; };`
    *   Array of Orders: `[P S I] [P S I] ...`
    *   Iterating prices loads unnecessary Size/ID data into cache.
*   **Good (DoD):** `struct OrderBook { vector<double> prices; vector<double> sizes; };`
    *   SIMD instructions can process 4-8 prices per cycle.

---

## 4. Multi-Threading & Lock-Free Programming

### 4.1 Thread Pinning (Cpu Isolation)
Prevent the OS from moving your critical thread to a different core (Context Switch).
*   **Isolate Core:** Boot Linux with `isolcpus=2,3`.
*   **Pin Thread:** `pthread_setaffinity_np`.

### 4.2 Lock-Free Queues (SPSC)
For passing data between the Network Thread (Producer) and Strategy Thread (Consumer), use a **Single-Producer Single-Consumer (SPSC)** ring buffer.

```cpp
template<typename T, size_t Capacity>
class RingBuffer {
    std::array<T, Capacity> buffer_;
    std::atomic<size_t> head_{0};
    std::atomic<size_t> tail_{0};
    
public:
    bool push(const T& val) {
        size_t h = head_.load(std::memory_order_relaxed);
        size_t next_h = (h + 1) % Capacity;
        if (next_h == tail_.load(std::memory_order_acquire)) return false; // Full
        buffer_[h] = val;
        head_.store(next_h, std::memory_order_release);
        return true;
    }
    
    bool pop(T& val) {
        size_t t = tail_.load(std::memory_order_relaxed);
        if (t == head_.load(std::memory_order_acquire)) return false; // Empty
        val = buffer_[t];
        tail_.store((t + 1) % Capacity, std::memory_order_release);
        return true;
    }
};
```
*Note: Uses `std::atomic` with memory ordering to avoid full memory barriers.*

---

## 5. Network Optimization (Kernel Bypass)

Standard Linux Networking Stack is slow (Interrupts -> Kernel Space -> User Space Copy).

### 5.1 Solarflare OpenOnload / TCPDirect
*   **Transparent:** Preload library, intercepts socket calls.
*   **Direct:** Maps NIC hardware ring buffers directly to user-space memory.
*   **Benefit:** Reduces latency from ~15µs (Kernel) to ~2µs.

### 5.2 DPDK (Data Plane Development Kit)
*   Complete bypass. You write the driver logic.
*   Poll Mode Driver (PMD): Spin on the NIC ring buffer 100% CPU. No interrupts.

---

## 6. Micro-Optimizations

1.  **Branch Prediction:**
    *   Use `[[likely]]` / `[[unlikely]]` (C++20).
    *   Example: `if (isValid [[likely]]) { ... }`
2.  **Prefetching:**
    *   `_mm_prefetch(ptr, _MM_HINT_T0);`
    *   Pull data into L1 cache before you need it.
3.  **Warmup:**
    *   Run dummy data through the hot path at startup to populate instruction cache and TLB.

---

## 7. Measuring Latency

**RDTSC (Read Time-Stamp Counter):**
CPU cycle counter. Nanosecond precision.

```cpp
inline uint64_t rdtsc() {
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}
```

*   **Histogram:** Do not just measure Average. Measure 99th and 99.9th percentile (tail latency).
