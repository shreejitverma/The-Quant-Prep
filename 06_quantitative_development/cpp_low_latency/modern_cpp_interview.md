# Modern C++ for Quant Interviews

Top firms (Jane Street, HRT, Optiver) use Modern C++ (14/17/20). "C with Classes" is not enough.

##  Key Features

### 1. Smart Pointers (`<memory>`)
*   **`std::unique_ptr`:** Exclusive ownership. No overhead vs raw pointer. Use by default.
*   **`std::shared_ptr`:** Shared ownership (Reference counting).
    *   *Warning:* The control block is thread-safe, but the data is not. Reference counting is atomic (slow-ish).
*   **`std::weak_ptr`:** Breaks reference cycles.

### 2. Move Semantics (`std::move`)
*   **Concept:** Transfer ownership of resources (e.g., heap memory) instead of copying.
*   **Performance:** Crucial for avoiding deep copies of large objects (Vectors, Matrices).
*   **Rule of 5:** If you define a destructor/copy-ctor/copy-assign, you probably need move-ctor and move-assign.

### 3. `auto` and `decltype`
*   Use `auto` for iterator types or complex template results. Don't overuse it for simple types (`int`, `double`) where explicit is clearer.

### 4. `constexpr` (Compile-time evaluation)
*   **Quant Use:** Pre-compute lookup tables (e.g., standard normal CDF values) at compile time to remove runtime cost.
*   **C++20:** `consteval` forces compile-time execution.

### 5. Multithreading (`<thread>`, `<atomic>`)
*   **`std::atomic`:** Lock-free operations.
*   **Memory Order:** `memory_order_relaxed`, `memory_order_acquire`, `memory_order_release`.
    *   *Interview Q:* Explain why `volatile` is NOT for thread safety (it's for hardware-mapped I/O).

##  Common Pitfalls
*   **Virtual Functions:** Avoid in the "Hot Path" (execution path). V-table lookups cause cache misses. Use **CRTP (Curiously Recurring Template Pattern)** for static polymorphism.
*   **Exceptions:** Often disabled in HFT (try/catch has overhead). Use error codes or `std::optional`.
*   **Dynamic Allocation:** Avoid `new`/`malloc` in the critical loop. Pre-allocate everything.

##  Practice Question
*"Implement a `shared_ptr` class from scratch, handling the reference count atomically."*
