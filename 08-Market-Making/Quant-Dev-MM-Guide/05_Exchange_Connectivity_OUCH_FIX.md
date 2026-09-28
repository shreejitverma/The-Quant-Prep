# Order Entry Protocols: OUCH & FIX

**Context:** Market Data comes via ITCH. Orders are sent via OUCH or FIX.
**Comparison:**
*   **OUCH:** Native Nasdaq protocol. Fixed length. Lowest latency. Optimized for HFT.
*   **FIX:** Industry standard (ASCII tag=value). Verbose. Higher latency. Used for client flow and non-latency sensitive strategies.

---

## 1. Nasdaq OUCH 5.0

OUCH is a simple, binary protocol that allows you to enter, cancel, and modify orders with minimal overhead.

### 1.1 Architecture
*   **TCP/IP:** Unlike ITCH (Multicast UDP), OUCH uses TCP because order entry requires reliability/delivery guarantees.
*   **Session:** Login -> Sequence Number Negotiation -> Active State.

### 1.2 Message Structure (Binary)
All messages are fixed length (mostly). Big-Endian integers.

**Example: Enter Order Message (Type 'O')**
Total Length: 48 Bytes approx.

| Offset | Field | Type | Description |
| :--- | :--- | :--- | :--- |
| 0 | Message Type | char | 'O' (Enter Order) |
| 1 | Token | char[14] | **Client Order ID**. Must be unique for the day. |
| 15 | Buy/Sell | char | 'B' = Buy, 'S' = Sell |
| 16 | Shares | int | Quantity |
| 20 | Stock | char[8] | Symbol (e.g., "MSFT    ") |
| 28 | Price | int | Limit Price (x 10,000) |
| 32 | TimeInForce | int | 0 = Day, 99998 = IOC |
| ... | ... | ... | Capacity, ISO-flag, etc. |

### 1.3 Optimization Tips for OUCH
1.  **Pre-Serialize:** The "Stock" and "Token" prefixes don't change often. Keep a pre-built buffer of the `Enter Order` message for each symbol. Only memcpy the Price and Shares at the last moment.
2.  **Optimistic Sending:** If you know you want to cancel, send the bytes to the socket buffer immediately.
3.  **Token Management:** Use a monotonically increasing integer for the Token (Client ID), converted to ASCII string efficiently (e.g., [fmtlib/Dragonbox](https://github.com/jk-jeon/dragonbox)).

---

## 2. FIX Protocol (Financial Information eXchange)

Standard version: FIX 4.2 (most common for Equities) or FIX 4.4 / 5.0.

### 2.1 Message Format (Tag=Value)
`8=FIX.4.2|9=65|35=D|49=SENDER|56=TARGET|34=100|52=20231027-12:00:00|11=ORDERID|55=AAPL|54=1|38=100|40=2|44=150.00|10=123|`

*   **Separator:** SOH character (ASCII 0x01), usually represented as `|` in docs.
*   **Tag 35 (MsgType):** 'D' = New Order Single, '8' = Execution Report.

### 2.2 Session Layer
FIX requires a "Heartbeat" mechanism.
*   **Logon (A):** Authenticate.
*   **Heartbeat (0):** Keep-alive every 30s.
*   **Resend Request (2):** If sequence numbers (Tag 34) skip, request replay.

### 2.3 Parsing FIX (The Slower Way)
Parsing `tag=value` involves scanning for delimiters (`=`, `\x01`). This is $O(N)$ and branch-heavy.

### 2.4 Fast FIX Engines (The HFT Way)
1.  **No String Allocation:** Never do `string s = msg.getField(55)`. Return a `string_view` or pointer to the raw buffer.
2.  **Hardcoded Offsets (where possible):** If the counterparty guarantees field order, you can jump to specific offsets (risky but fast).
3.  **FAST Protocol:** Binary compression for FIX (used in Market Data, less common for Order Entry).

---

## 3. Handling Rejects & Race Conditions

### 3.1 In-Flight Orders
1.  You send OUCH 'Enter Order' (Token: A1).
2.  You haven't received the 'Accepted' ack yet.
3.  Signal changes. You want to Cancel A1.
4.  **Problem:** Can you cancel an order the exchange "doesn't know" yet?
5.  **Answer:** In OUCH, usually yes, if the TCP streams are processed in order. But if A1 failed (Reject), your Cancel will also Reject ("Order Not Found").

### 3.2 State Machine
Every order must track state:
*   `PENDING_NEW`: Sent, no Ack.
*   `LIVE`: Ack received.
*   `PENDING_CANCEL`: Cancel sent, no Ack.
*   `DEAD`: Fully filled or Canceled.

**Risk:** Never assume an order is DEAD until you get the specific OUCH/FIX message confirming it. "Phantom Fills" occur when you assume a Cancel worked, but a fill happened milliseconds before.
