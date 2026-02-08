# Nasdaq TotalView-ITCH 5.0: Technical Guide for Quantitative Developers

**Protocol Version:** 5.0  
**Transport:** UDP/IP (Multicast) / TCP (Snapshot/Recovery)  
**Encoding:** Binary (Big-Endian)  
**Focus:** Ultra-low latency, full market depth (MBO - Market by Order)

---

## 1. Protocol Overview

Nasdaq TotalView-ITCH is the proprietary data feed that provides full order depth for Nasdaq-listed securities. Unlike the SIP (consolidated feed), ITCH allows you to build the **full limit order book** (Level 3 data) by broadcasting every individual order message.

### Key Characteristics
*   **Direct Feed:** Bypasses the SIP for lower latency (~microsecond scale).
*   **Market by Order (MBO):** You see every individual order, not just price levels. This allows for queue position estimation and advanced microstructure signals.
*   **Binary Encoding:** Fixed-length messages (mostly) for efficient parsing.
*   **Big-Endian:** Network byte order. On x86 (Little-Endian) systems, you must byteswap `ntohs` / `ntohl`.
*   **Nanosecond Timestamps:** High-precision timing for event sequencing.

---

## 2. Data Types

| Type | Size | Description |
| :--- | :--- | :--- |
| **Integer** | 2, 4, 6, 8 bytes | Unsigned integers (Big-Endian). |
| **Price (4)** | 4 bytes | Integer. Divide by 10,000 to get decimal price (Fixed Point 4). |
| **Price (8)** | 8 bytes | Integer. Divide by 100,000,000 (Fixed Point 8). Used for high-priced assets. |
| **Alpha** | Variable | Left-justified ASCII string, padded with spaces. |
| **Timestamp** | 6 bytes | Nanoseconds past midnight (ET). |

**Note on Timestamps:** ITCH uses a split timestamp format in some contexts, but usually provides a standard nanosecond offset from midnight.

---

## 3. Message Header Structure

Every ITCH message starts with a standard header or is framed within a transport packet (MoldUDP64). At the application payload level, messages are distinguished by a **1-byte Message Type**.

| Offset | Length | Name | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 1 | Message Type | Alpha | Identifies the message (e.g., 'A' for Add Order). |
| 1 | Variable | Payload | Mix | Message-specific data. |

*Note: In raw UDP capture (MoldUDP64), there is a session header before the message stream.*

---

## 4. Critical Message Types

### 4.1 System Event Message ('S')
Indicates the state of the matching engine.
*   **'O':** Start of Messages.
*   **'S':** Start of System Hours.
*   **'Q':** Start of Market Hours (9:30 AM ET) – Open.
*   **'M':** End of Market Hours (4:00 PM ET) – Close.
*   **'E':** End of System Hours.
*   **'C':** End of Messages.

**Quant Logic:** Use 'Q' and 'M' to trigger trading strategies vs. maintenance mode. Use 'S' to reset books.

### 4.2 Stock Directory Message ('R')
Sent at the start of the day for every tradable symbol. **Crucial for mapping.**
*   **Stock Locate (2 bytes):** An integer ID assigned to the symbol for the day.
*   **Stock (8 bytes):** The ticker symbol (e.g., "AAPL    ").
*   **Market Category:** NYSE, Nasdaq, Amex, etc.

**Optimization Tip:** Do **not** use string comparisons ("AAPL") in your hot path. Map "AAPL" to `Stock Locate ID` (e.g., 1234) at startup. All subsequent order messages use the `Stock Locate ID`. This allows O(1) array indexing for book lookups.

### 4.3 Trading Action Message ('H')
Indicates halts and pauses.
*   **Trading State:**
    *   'H': Halted (Reg NMS, News, etc.).
    *   'P': Paused (LULD volatility pause).
    *   'T': Trading Resumed.

**Risk Check:** Your system **must** immediately block proprietary orders if it receives an 'H' or 'P' for a symbol you trade.

### 4.4 Add Order Message ('A' and 'F')
Adds a new visible order to the book.
*   **'A':** No MPID attribution (Anonymous).
*   **'F':** With MPID attribution (e.g., "GSCO").

**Fields:**
*   **Order Reference Number (8 bytes):** Unique ID for this order. **Key for tracking.**
*   **Buy/Sell Indicator:** 'B' or 'S'.
*   **Shares (4 bytes):** Quantity.
*   **Stock Locate (2 bytes):** Symbol ID.
*   **Price (4 bytes):** Limit price.

**Book Logic:** Insert node `(Price, Time, OrderRef)` into your Order Book data structure.

### 4.5 Order Executed Message ('E')
An order on the book was executed (fully or partially).
*   **Order Reference Number:** Matches the 'A' message.
*   **Executed Shares:** Number of shares traded.
*   **Match Number:** Unique Trade ID.

**Book Logic:** Find the order by `Order Reference Number`. Decrement its size by `Executed Shares`. If size becomes 0, remove it.
**Note:** The price is implied from the original 'A' message.

### 4.6 Order Executed with Price Message ('C')
An order on the book was executed at a price **different** from its display price (e.g., price improvement/slippage due to cross).
*   **Execution Price:** The actual trade price.
*   **Printable:** 'Y' or 'N' (whether it prints to the tape).

**Book Logic:** Same as 'E' (reduce size), but record the trade at the *Execution Price* for volume/signal analysis.

### 4.7 Order Cancel ('X') vs. Order Delete ('D')
*   **Order Cancel ('X'):** Partial reduction.
    *   **Canceled Shares:** Amount to remove.
    *   **Logic:** Decrement size. If 0, remove.
*   **Order Delete ('D'):** Full removal.
    *   **Logic:** Immediately remove order from book.

### 4.8 Order Replace Message ('U')
Efficiency mechanism. Replaces an existing order with a new one (new Order ID, potentially new size/price).
*   **Original Order Reference Number:** Old order.
*   **New Order Reference Number:** New order.
*   **Shares:** New quantity.
*   **Price:** New price.

**Book Logic:** Atomic "Delete Old" + "Add New".
**Important:** The new order loses queue priority (new timestamp).

### 4.9 Net Order Imbalance Indicator ('I') - NOII
Broadcast before the Open (9:28-9:30) and Close (3:50-4:00) to indicate auction state.
*   **Paired Shares:** Shares that can match at current Reference Price.
*   **Imbalance Shares:** Excess buy/sell interest.
*   **Imbalance Direction:** 'B' (Buy side imbalance), 'S' (Sell side), 'N' (No imbalance).
*   **Far Price / Near Price / Current Reference Price:** Auction price scenarios.

**Quant Strategy:** NOII data is the primary signal for "Opening" and "Closing" auction arbitrage strategies (MOC/LOC orders).

---

## 5. Building the Order Book (Developer Logic)

To reconstitute the limit order book from ITCH:

1.  **Initialize:** Create an array of OrderBooks, indexed by `Stock Locate ID`.
    ```cpp
    std::vector<OrderBook> all_books(MAX_STOCK_LOCATE_ID);
    ```

2.  **Mapping:** On 'R' (Directory), map Symbol String -> ID.
    ```cpp
    map_symbol_to_id["AAPL"] = msg.stock_locate;
    ```

3.  **State Management:**
    *   **Map:** `std::unordered_map<uint64_t, Order*> order_map;` (Order Ref -> Order Node).
    *   **Tree/List:** A sorted structure (e.g., Red-Black Tree or Skip List) for Price Levels.

4.  **Processing Loop:**
    *   **'A' (Add):**
        *   Create `Order` object.
        *   Add to `order_map[ref_num]`.
        *   Insert into Price Level in `OrderBook`.
    *   **'E'/'X' (Modify):**
        *   Lookup `Order*` in `order_map[ref_num]`.
        *   Modify size.
        *   If size == 0, delete from Map and Price Level.
    *   **'D' (Delete):**
        *   Lookup and remove immediately.
    *   **'U' (Replace):**
        *   Treat as Delete(Old) + Add(New).

### Code Snippet: Parsing (C++)

```cpp
struct ItchHeader {
    uint16_t length; // Little endian usually if read from network layer wrapper
    char msg_type;
};

struct AddOrderMsg {
    uint32_t timestamp_nanos; // Simplified
    uint64_t order_ref;
    uint8_t  buy_sell_flag;
    uint32_t shares;
    uint16_t stock_locate;
    uint32_t price_4;
};

void process_packet(const char* buffer) {
    char msg_type = buffer[0];
    switch (msg_type) {
        case 'A': {
            // Cast or memcpy to safe struct
            // BSWAP (ntohl) fields if necessary
            // update_book(stock_locate, side, price, size, ref);
            break;
        }
        case 'E': {
            // handle execution
            break;
        }
        // ... handle others
    }
}
```

## 6. Performance Considerations
1.  **Zero-Copy:** Do not copy the buffer into a struct. Cast the pointer (if alignment allows) or use `memcpy` for safe unaligned access.
2.  **Pre-allocation:** Pre-allocate Order nodes in a memory pool to avoid `new`/`delete` latency spikes during high message rates.
3.  **Instruction Cache:** Keep the 'Add', 'Exec', 'Cancel' handlers hot in cache. These make up 95% of traffic.
