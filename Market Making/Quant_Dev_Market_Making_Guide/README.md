# Quantitative Developer Guide: Market Making & Microstructure

This repository contains a comprehensive guide for Quantitative Developers specializing in electronic market making. The content covers the regulatory framework, low-latency market data protocols, quantitative models, and system architecture.

## Table of Contents

### 1. [Regulatory Framework (Reg NMS & SHO)](./01_Regulatory_Framework_NMS_SHO.md)
*   **Regulation NMS:** Order Protection Rule (611), Access Rule (610), Sub-Penny Rule (612).
*   **Regulation SHO:** Short sale marking, Locate requirements, Bona Fide Market Maker exceptions, Close-out rules (204).
*   **Compliance Systems:** Designing pre-trade risk checks and compliance monitoring.

### 2. [Market Data Protocol (Nasdaq TotalView-ITCH 5.0)](./02_Market_Data_Protocol_ITCH_5_0.md)
*   **Protocol Specs:** Binary encoding, data types, message structure.
*   **Critical Messages:** Add/Exec/Cancel, System Events, Stock Directory.
*   **Order Book Building:** Algorithms for reconstructing the limit order book from the feed.

### 3. [Quantitative Models & Strategies](./03_Quantitative_Models_and_Strategies.md)
*   **Avellaneda-Stoikov Model:** Optimal quotes, reservation price, inventory risk premium.
*   **Inventory Management:** Skewing logic, damping factors, position limits.
*   **Alpha Signals:** Order Book Imbalance (OBI), VPIN, Lead-Lag correlations.
*   **Backtesting:** Simulator design and fill probability modeling.

### 4. [Low-Latency C++ Optimization](./04_Low_Latency_CPP_Optimization.md)
*   **The Hot Path:** Zero allocations, branch prediction, cache locality.
*   **Memory Management:** Object pools, custom allocators, Data-Oriented Design (DoD).
*   **Concurrency:** Lock-free queues (SPSC), thread pinning, isolation.
*   **Kernel Bypass:** OpenOnload, DPDK basics.

### 5. [Exchange Connectivity (OUCH & FIX)](./05_Exchange_Connectivity_OUCH_FIX.md)
*   **Nasdaq OUCH:** Binary protocol structure, optimization tips, state management.
*   **FIX Protocol:** Session layer, tag-value parsing, fast engines.
*   **Order Lifecycle:** Pending, Live, Reject handling, race conditions.

### 6. [Trading System Architecture](./06_Trading_System_Architecture.md)
*   **Components:** Feed Handler, Strategy Engine, Risk Controller, Order Gateway.
*   **IPC:** Shared memory ring buffers vs. network sockets.
*   **Reliability:** Async logging (NVMe), failover strategies, drop copy integration.

### 7. [ITCH Protocol Mastery: Evolution & Architecture](./07_ITCH_Protocol_Mastery_Guide.md)
*   **Philosophy:** Market-by-Order (MBO) vs. SIP, Determinism.
*   **Evolution:** History from v3.0 (Legacy) to v4.1 (Transitional) to v5.0 (Modern).
*   **Advanced Signals:** Hidden order detection, Queue position theory, Auction imbalances.
*   **Deep Dive:** Transport layers (MoldUDP64) and message lifecycle.

### 8. [OUCH Protocol Mastery: Order Entry Architecture](./08_OUCH_Protocol_Mastery_Guide.md)
*   **Philosophy:** The "Dumb Pipe" design, Client-side Tokens.
*   **Deep Dive:** SoupBinTCP session layer, Binary message formats (Enter, Replace, Cancel).
*   **State Management:** Handling Race Conditions, Phantom Fills, and State Transitions.
*   **Performance:** TCP_NODELAY, Optimistic Sending, and Buffer Management.

### 9. [FIX Protocol Mastery: Architecture & Engines](./09_FIX_Protocol_Mastery_Guide.md)
*   **Philosophy:** Universal compatibility vs. latency.
*   **Architecture:** Session Layer (Admin) vs. Application Layer (Business).
*   **Deep Dive:** Message structure (Tag=Value), critical tags, and parsing challenges.
*   **Optimization:** Zero-copy parsing, custom engines, and handling "Drop Copy" flows.

---

## How to Use This Guide
*   **Study:** Read the modules in order to build a foundation from regulations -> data -> strategy -> implementation.
*   **Implement:** Use the C++/Python code snippets in the modules as a reference for your own projects.
*   **Interview Prep:** Each module is designed to cover standard interview questions for HFT/Market Making roles.
