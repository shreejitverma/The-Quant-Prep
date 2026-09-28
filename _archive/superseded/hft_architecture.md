# High Frequency Trading (HFT) System Architecture

To compete at the microsecond (or nanosecond) level, HFT firms rely on specialized architecture that bypasses standard operating system overheads.

##  The Stack (From Wire to Strategy)

### 1. The Physical Layer (L1)
*   **Colocation:** Servers are physically located in the exchange's data center (e.g., NASDAQ's data center in Carteret, NJ) to minimize the speed of light travel time.
*   **Microwave Towers:** Used for inter-exchange communication (e.g., Chicago to NY) because radio waves through air travel faster than light through fiber optic glass.

### 2. Network Interface (L2/L3)
*   **FPGA (Field Programmable Gate Arrays):** Custom hardware chips that can parse exchange feeds (ITCH/OUCH) directly on the wire before data even reaches the CPU.
    *   *Use case:* Pre-trade risk checks, simple arbitrage logic.
*   **Kernel Bypass (Solarflare / OpenOnload):** Standard OS networking stacks (Linux TCP/IP) are too slow (context switches, interrupts).
    *   *Solution:* Map the Network Interface Card (NIC) memory directly into the user-space application memory (DMA).

### 3. The Feed Handler
*   **Normalization:** Converts exchange-specific protocols (binary, FIX) into a unified internal format.
*   **Book Building:** Reconstructs the Limit Order Book (LOB) from incremental updates (Add, Cancel, Modify messages).

### 4. The Strategy Engine
*   **Single-Threaded Loop:** To avoid locking overhead, the core logic often runs on a single CPU core that is "pinned" (isolated from the OS scheduler).
*   **Lock-Free Queues:** Communication between the Feed Handler thread and Strategy thread happens via shared memory ring buffers (SPSC).

### 5. Execution & Risk (OMS/EMS)
*   **Pre-Trade Risk:** Must check limits (max position, max notional) in nanoseconds.
*   **Smart Order Routing (SOR):** Deciding which venue to send the order to for the best price/rebate.

##  Diagram

```mermaid
graph TD
    Exchange[Exchange Matching Engine] -->|Market Data (UDP Multicast)| FPGA
    FPGA[FPGA / SmartNIC] -->|Filtered/Parsed Data| DMA[Shared Memory Ring Buffer]
    DMA --> FeedHandler[Feed Handler Thread]
    FeedHandler -->|Normalized Book| Strategy[Strategy Logic Thread]
    Strategy -->|Order Request| Risk[Pre-Trade Risk Check]
    Risk -->|Approved Order| Execution[Execution Gateway]
    Execution -->|TCP/Binary Order| Exchange
```

##  Key Optimization Techniques
1.  **Warm-up:** Running dummy loops to keep CPU caches hot.
2.  **Branch Prediction Optimization:** writing code that favors the "happy path" (e.g., `if (unlikely(error))`).
3.  **Zero-Copy:** Never copying data buffers; passing pointers instead.
