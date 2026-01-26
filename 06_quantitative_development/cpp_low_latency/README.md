# C++ for Low Latency Quantitative Development

This module covers the essential C++ concepts required for High Frequency Trading (HFT) and low-latency systems development.

## 📚 Syllabus

1.  **Memory Management**
    *   Stack vs Heap
    *   Smart Pointers (`unique_ptr`, `shared_ptr`)
    *   Custom Allocators (Arena, Pool)
    *   Cache Locality & False Sharing

2.  **Template Metaprogramming (TMP)**
    *   `constexpr` and Compile-time computation
    *   SFINAE & Concepts (C++20)
    *   CRTP (Curiously Recurring Template Pattern) for static polymorphism

3.  **Concurrency & Multithreading**
    *   Memory Order & Fences (`std::memory_order`)
    *   Lock-free Data Structures (Ring Buffers, Queues)
    *   Thread Pinning & Affinity
    *   Spinlocks vs Mutexes

4.  **Network Programming**
    *   TCP vs UDP (Multicast)
    *   Kernel Bypass (Solarflare, DPDK)
    *   Socket Optimization (`SO_BUSYPOLL`)

## 🛠️ Key Libraries
*   **Boost:** Asio, Interprocess
*   **Folly:** Facebook's open-source library
*   **QuickFIX:** For FIX protocol messaging

## 📝 Practice Projects
1.  Implement a Lock-free Ring Buffer.
2.  Build a simple Order Matching Engine.
3.  Create a FIX Message Parser using TMP.
