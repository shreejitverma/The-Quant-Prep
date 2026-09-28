---
type: concept
track: [quant-dev]
tier: core
status: seed
prereqs: [cpp-for-trading-systems]
est_hours: 5
sources: []
---

# Concurrency, Lock-Free Queues and Memory Pools

> [!info] Seed note
> Not written yet. The objectives below define what "done" looks like; use the references to study it now.

## Learning objectives

- Implement an SPSC ring buffer with correct memory orders.
- Build an allocation-free steady state with pools and arenas.
- Explain the C++ memory model precisely.

## In this repo and SDE-Interview-Prep

- Code: [lock_free_spsc_queue.cpp](code/cpp/lock_free_spsc_queue.cpp), [memory_pool.cpp](code/cpp/memory_pool.cpp), [multithreaded_monte_carlo.cpp](code/cpp/multithreaded_monte_carlo.cpp).
- [C++ memory model and memory orders (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/08%20-%20Low-Latency%20Programming/C%2B%2B%20Memory%20Model%20and%20Memory%20Orders.md)
- [Lock-free SPSC ring buffer design (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/08%20-%20Low-Latency%20Programming/Lock-Free%20SPSC%20Ring%20Buffer%20Design.md)
