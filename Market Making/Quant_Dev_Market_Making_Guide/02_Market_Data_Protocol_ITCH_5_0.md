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

### 1.1 Data Flow Architecture

```mermaid
+-------------+       (Multicast UDP)       +----------------+
| Nasdaq Data |  ========================>  |  Feed Handler  |
|   Center    |        [MoldUDP64]          | (FPGA / Kernel)|
+-------------+                             +----------------+
       ^                                            |
       | (TCP Re-Request)                           | (Parsed Updates)
       |                                            v
+-------------+                             +----------------+
| Gap Request |  <------------------------  |   Order Book   |
|   Server    |                             |    Builder     |
+-------------+                             +----------------+
```

---

## 2. Data Types & Encoding

All numeric fields are unsigned integers in Big-Endian format.

### 2.1 Integer Types
| Type | Size | Description | C++ Type |
| :--- | :--- | :--- | :--- |
| **Integer** | 2 bytes | Unsigned short (Big-Endian) | `uint16_t` |
| **Integer** | 4 bytes | Unsigned int (Big-Endian) | `uint32_t` |
| **Integer** | 6 bytes | Custom 48-bit int (Big-Endian) | `char[6]` -> `uint64_t` |
| **Integer** | 8 bytes | Unsigned long long (Big-Endian) | `uint64_t` |

### 2.2 Price Formats
ITCH uses implied decimal points. You must handle two types:
*   **Price (4):** 4-byte Integer.
    *   **Formula:** `Double_Price = Integer / 10,000`
    *   **Max Value:** 200,000.0000
    *   **Usage:** Most equities.
*   **Price (8):** 8-byte Integer.
    *   **Formula:** `Double_Price = Integer / 100,000,000`
    *   **Usage:** High-priced stocks (e.g., BRK.A) or when extreme precision is needed.

### 2.3 Timestamps
*   **Format:** Nanoseconds since midnight (Eastern Time).
*   **Size:** 6 Bytes (48-bit).
*   **Parsing Tip:** Since `uint48_t` isn't a standard C type, interpret as `uint64_t` masked or perform a custom shift:
    ```cpp
    uint64_t parse_ts(const char* buf) {
        return ((uint64_t)ntohl(*(uint32_t*)buf)) << 16 | (uint16_t)ntohs(*(uint16_t*)(buf + 4));
    }
    ```

---

## 3. Message Architecture & Transport

Every ITCH message is framed within a transport packet (usually MoldUDP64).

### 3.1 MoldUDP64 Packet Structure
The payload often contains *multiple* ITCH messages packed together to save bandwidth.

```
[ Session (10) | Sequence (8) | Count (2) ]  <-- Header (20 Bytes)
[ Length (2) | Message 1 Body... ]           <-- Payload 1
[ Length (2) | Message 2 Body... ]           <-- Payload 2
...
```

### 3.2 Sequence Handling (Gap Detection)
*   **Expected Sequence:** `NextSeq = CurrentSeq + MessageCount`.
*   **Gap Detected:** If `IncomingSeq > NextSeq`, you missed packets.
*   **Action:**
    1.  Buffer the new packet (don't process out of order).
    2.  Send **Retransmission Request** to the Recovery Server (TCP).
    3.  Process replayed packets, then flush buffer.

---

## 4. Critical Message Types (Deep Dive)

### 4.1 System Event Message ('S')
Controls the state of the system.
*   **'O':** Start of Messages (Connect).
*   **'S':** Start of System Hours (Pre-market).
*   **'Q':** **Start of Market Hours (9:30 AM ET)**. This is the "Gun" for Open strategies.
*   **'M':** End of Market Hours (4:00 PM ET).
*   **'C':** End of Messages.

### 4.2 Stock Directory Message ('R')
Sent at the start of the day for every tradable symbol.
*   **Stock Locate (2 bytes):** Integer ID. **Crucial:** All subsequent order messages use this ID, not the string "AAPL". You **must** build a map `LocateID -> Symbol` at startup.
*   **Stock (8 bytes):** "AAPL    ".
*   **Financial Status Indicator:** Deficient, Delinquent, etc.
*   **Round Lot Size:** Usually 100.

### 4.3 Trading Action Message ('H')
Indicates halts and pauses.
*   **Trading State:**
    *   'H': Halted (Reg NMS, News, etc.). **Risk:** Stop quoting immediately.
    *   'P': Paused (LULD Volatility Pause).
    *   'T': Trading Resumed.
*   **Cross SRO:** ISO logic requires you to know if *all* markets are halted or just Nasdaq.

### 4.4 Reg SHO Restriction Message ('Y')
*   **Action:**
    *   '0': No Price Test.
    *   '1': **Reg SHO Rule 201 Active.** (Short Sale Price Test).
    *   '2': Rule 201 remains active.
*   **Quant Logic:** If '1', your short sell orders **must** be priced above the National Best Bid (NBB), unless marked Short Exempt.

### 4.5 Add Order Message ('A' and 'F')
Adds a new visible order to the book.
*   **'A':** Anonymous.
*   **'F':** Attributed (MPID).
*   **Fields:**
    *   **Reference Num (8 bytes):** Unique Order ID. **Key for tracking.**
    *   **Buy/Sell:** 'B' or 'S'.
    *   **Shares:** Quantity.
    *   **Price:** Limit Price.

**Book Logic:** Insert node `(Price, Time, OrderRef)` into your Order Book. Time priority is determined by message arrival sequence.

### 4.6 Order Executed Message ('E')
An order on the book was executed (fully or partially).
*   **Reference Num:** Matches 'A' message.
*   **Executed Shares:** Amount traded.
*   **Match Num:** Trade ID.

**Book Logic:** Find Order by `Reference Num`. `NewSize = OldSize - ExecutedShares`. If `NewSize == 0`, delete order.

### 4.7 Order Executed with Price Message ('C')
An order on the book was executed at a price **different** from its display price.
*   **Scenario:** Price Improvement or Cross execution.
*   **Logic:** Reduce size in book, but record trade at the *Execution Price* (not the book price) for volume/signal analysis.

### 4.8 Order Cancel ('X') vs. Order Delete ('D')
*   **Cancel ('X'):** Partial reduction. `NewSize = OldSize - CanceledShares`.
*   **Delete ('D'):** Order removed immediately. `Size = 0`.

### 4.9 Order Replace Message ('U')
Replaces an existing order with a new one.
*   **Original Ref Num:** Old Order.
*   **New Ref Num:** New Order.
*   **Logic:** Atomic `Delete(Old)` + `Add(New)`.
*   **Priority:** The new order goes to the *end* of the queue at the new price level.

### 4.10 Net Order Imbalance Indicator ('I') - NOII
Broadcast before the Open (9:28-9:30) and Close (3:50-4:00).
*   **Paired Shares:** Volume that *would* trade at current Ref Price.
*   **Imbalance:** Remaining volume.
*   **Far/Near/Current Price:** Indicative auction prices.
*   **Quant Strategy:** NOII signals predict the Opening/Closing cross price direction. A "Buy Imbalance" usually predicts an upward price drift into the close.

---

## 5. Building the Order Book (Developer Logic)

To reconstitute the limit order book from ITCH:

1.  **Data Structures:**
    *   `OrderMap`: `Hash<OrderRef, OrderObject>` (O(1) lookup).
    *   `PriceLevels`: `Map<Price, Queue<OrderRef>>` (Sorted Price Levels).
    *   `Book`: `Vector<PriceLevels>` (Indexed by `Stock Locate ID`).

2.  **Startup Routine:**
    *   Read 'R' (Directory) -> Map `StockLocate` to Symbol.
    *   Pre-allocate memory for 10,000 symbols.

3.  **Processing Loop:**
    *   **'A' (Add):** Create Order. Add to Map. Push to back of PriceLevel Queue.
    *   **'E' (Exec):** Lookup Order. Reduce Size. Update Map.
    *   **'U' (Replace):** Lookup Old. Remove from Queue. Create New. Add New to Map/Queue.

### Code Snippet: Parsing (C++)

```cpp
struct AddOrderMsg {
    uint32_t timestamp_nanos_high; // Custom 6-byte handling needed
    uint16_t timestamp_nanos_low;
    uint64_t order_ref;
    uint8_t  buy_sell_flag;
    uint32_t shares;
    uint16_t stock_locate;
    uint32_t price_4;
} __attribute__((packed));

void process_add(const char* buf) {
    // Zero-copy cast
    const auto* msg = reinterpret_cast<const AddOrderMsg*>(buf);
    
    uint16_t locate = ntohs(msg->stock_locate);
    uint64_t ref = ntohll(msg->order_ref);
    uint32_t price = ntohl(msg->price_4);
    uint32_t shares = ntohl(msg->shares);
    bool is_buy = (msg->buy_sell_flag == 'B');
    
    // Update Book
    books[locate].add_order(ref, price, shares, is_buy);
}
```

## 6. Performance Considerations
1.  **Byte Swapping:** `ntohl` can be slow. Use compiler intrinsics like `__builtin_bswap32` or `_byteswap_ulong` (MSVC) for single-cycle swapping.
2.  **Branch Prediction:** Sort your `switch(msg_type)` by frequency. 'A' (Add), 'D' (Delete), 'E' (Exec), 'U' (Replace) are 99% of messages. 'R' (Directory) happens once.
3.  **Memory Layout:** Use a "Pool Allocator" for Order objects to ensure they are contiguous in memory, reducing cache misses during book traversals.

---

## 7. Sequence of Events (Lifecycle)

**Normal Trading Day:**
1.  **04:00:00** - 'S' (Start of System Hours). Books are cleared.
2.  **04:00 - 09:28** - 'R' (Stock Directory) messages stream in. Build Symbol Map.
3.  **09:28:00** - 'I' (NOII) messages start streaming for the Open.
4.  **09:30:00** - 'Q' (Start of Market Hours). Opening Cross trades ('Q' type) occur.
5.  **09:30 - 16:00** - Continuous trading. 'A', 'E', 'D', 'U' flood.
6.  **15:50:00** - 'I' (NOII) messages resume for the Close.
7.  **16:00:00** - 'M' (End of Market Hours). Closing Cross trades.

---

## 8. Version Differences (4.1 vs 5.0)

| Feature | ITCH 4.1 | ITCH 5.0 |
| :--- | :--- | :--- |
| **Order Reference** | 9 digits (Variable) | 8 bytes (64-bit Integer) |
| **Timestamps** | Seconds + Nanoseconds (Split) | 48-bit Nanoseconds (Unified) |
| **Stock Symbol** | 6 bytes | 8 bytes (Better suffix support) |
| **Msg Types** | Separated 'Add' by Attrib | Consolidated Logic |

**Why Upgrade?** Version 5.0 handles the explosion in daily order counts (requiring 64-bit IDs) and simplifies timestamp arithmetic for HFT.

---

## 9. Key Terms Glossary

*   **Locate ID:** The 2-byte integer used to identify a stock symbol (e.g., 1234 = AAPL).
*   **Order Reference Number:** The 64-bit unique ID assigned to every order. Persistent for the life of the order.
*   **MoldUDP64:** The transport protocol wrapping ITCH messages, providing sequencing and packet counting.
*   **MBO (Market-By-Order):** A data feed providing every individual order, as opposed to MBP (aggregated levels).
*   **NOII (Net Order Imbalance Indicator):** Data describing the supply/demand mismatch before an auction (Open/Close).

---

## 10. Official Documentation
*   [Nasdaq TotalView-ITCH 5.0 Specification](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf)
*   [MoldUDP64 Specification](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf)
