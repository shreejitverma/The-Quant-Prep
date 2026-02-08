# Trading System Architecture Design

**Goal:** Modular, fault-tolerant, low-latency system.

---

## 1. High-Level Diagram

```
[Exchange]  <--- TCP/IP (Orders) --->  [Order Gateway]
    |                                        ^
    | UDP (Market Data)                      | (Internal Bus / Shm)
    v                                        v
[Feed Handler]  ------------------->  [Strategy Engine]
                                             |
                                             v
                                      [Risk Controller]
```

---

## 2. Components

### 2.1 Feed Handler (Market Data)
*   **Input:** Raw PCAP / UDP Multicast (ITCH).
*   **Role:** Parsing, Normalization, Book Building.
*   **Output:** Normalized `BookUpdate` object (Price, Size, Timestamp).
*   **Optimization:** Thread pinning, Kernel Bypass (onload).

### 2.2 Strategy Engine (The Brain)
*   **Input:** `BookUpdate`.
*   **Logic:**
    1.  Update internal Alpha signals (e.g., OBI, Weighted Midpoint).
    2.  Check Inventory state.
    3.  Run Valuation Model (Avellaneda-Stoikov).
    4.  Diff against current active orders.
    5.  Generate `OrderAction` (Add, Cancel, Replace).
*   **Constraint:** Single-threaded hot path (usually) to avoid lock contention.

### 2.3 Risk Controller (The Brakes)
*   **Location:** Inline with Strategy (Pre-Transmission) or separate thread?
    *   *HFT:* Inline (Minimal checks).
    *   *Mid-Freq:* Separate thread.
*   **Checks:**
    *   **Fat Finger:** Price > 10% from NBBO?
    *   **Max Notional:** Order Value > $1M?
    *   **Max Position:** Inventory > Limit?
    *   **Kill Switch:** Is the global flag `TRADING_ENABLED` true?

### 2.4 Order Gateway (OE)
*   **Role:** Protocol Translation (Strategy Obj -> OUCH/FIX bytes).
*   **State Management:** Tracking Order IDs (ClOrdID -> ExchangeID).
*   **Throttling:** Ensuring we don't exceed exchange message rate limits.

---

## 3. Inter-Process Communication (IPC)

How do components talk?

1.  **Shared Memory (SHM):** Lowest latency. `boost::interprocess` or custom `mmap`.
    *   Ring Buffers in SHM allow Feed Handler to write and Strategy to read with ~100ns latency.
2.  **Network (Loopback):** Easier to debug (tcpdump), but adds ~5-10µs. Too slow for HFT.

---

## 4. Logging & Compliance

**The Golden Rule:** Never block the hot path for logging.

### 4.1 Async Logging
1.  Strategy pushes `LogEntry` (binary struct) to a lock-free queue.
2.  `LoggerThread` pops from queue.
3.  `LoggerThread` formats to ASCII (or keeps binary) and writes to NVMe SSD.

### 4.2 Drop Copy
Regulatory requirement. All orders sent to the exchange must be reported to a "Drop Copy" session (usually FIX) for real-time risk monitoring by the firm's compliance officer.

---

## 5. Failover & Recovery

### 5.1 Process Crash
*   **Watcher Process:** Uses `pidfd_open` or signals to detect crash.
*   **Recovery:**
    1.  Restart Process.
    2.  Re-subscribe to Drop Copy to get "Open Orders".
    3.  Re-build Order Book from ITCH "Snapshot" or replay.
    4.  Enter "Cancel All" mode (safe state).
    5.  Resume Trading.

### 5.2 Exchange Disconnect
*   If heartbeat missed:
    1.  Alert Desk.
    2.  Assume all orders are open (risk).
    3.  Attempt Reconnect.
