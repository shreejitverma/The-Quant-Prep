# Low Latency Java for HFT

While C++ is King in HFT, Java is widely used in electronic trading (banks, some prop shops) for its rapid development cycle and mature ecosystem.

## 🚀 Key Concepts

1.  **Garbage Collection (GC) Avoidance:**
    *   **Object Pooling:** Reusing objects instead of creating new ones to prevent "Stop-the-world" GC pauses.
    *   **Off-Heap Memory:** Using `ByteBuffer` or `Unsafe` to manage memory outside the JVM heap.

2.  **The LMAX Disruptor:**
    *   A high-performance inter-thread messaging library.
    *   Uses a **Ring Buffer** (pre-allocated array) to pass data between producers and consumers without locks.

3.  **Thread Affinity:**
    *   Binding critical threads (e.g., market data handler) to specific CPU cores to maximize cache hits.

## 📝 Example: GC-Free Ring Buffer Pattern

See `examples/RingBuffer.java` (Mock implementation).

## 📚 Resources
*   [LMAX Disruptor Architecture](https://lmax-exchange.github.io/disruptor/)
*   "Java Performance: The Definitive Guide" by Scott Oaks
