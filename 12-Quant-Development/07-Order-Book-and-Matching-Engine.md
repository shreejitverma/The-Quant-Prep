---
type: concept
track: [quant-dev]
tier: core
status: seed
prereqs: [cpp-for-trading-systems, limit-order-books-and-order-types]
est_hours: 5
sources: []
---

# Order Book and Matching Engine Implementation

> [!info] Seed note
> Not written yet. The objectives below define what "done" looks like; use the references to study it now.

## Learning objectives

- Implement a price-time priority limit order book with O(1) cancel.
- Choose data structures for levels and orders and justify them with cache behaviour.

## In this repo and SDE-Interview-Prep

- Code: [order_matching_engine.cpp](code/cpp/order_matching_engine.cpp).
- [Order book data structures (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/03%20-%20Matching%20Engine%20Internals/Order%20Book%20Data%20Structures.md)
- [Lab: intrusive LOB (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/03%20-%20Matching%20Engine%20Internals/Lab%20-%2003%20High-Performance%20Intrusive%20LOB.md)
