# Nasdaq OUCH Protocol Mastery: Order Entry Architecture & Implementation

**Target Audience:** Quantitative Developers, HFT Engineers
**Goal:** Master the low-latency order entry protocol used by Nasdaq and many other exchanges. Understand the *why* behind its design and how to implement a robust, high-performance gateway.

---

## 1. The Philosophy of OUCH

**OUCH (Order Update C... Host?):** Like ITCH, OUCH is designed for speed and simplicity.

### 1.1 "Dumb" by Design
OUCH is a **minimalist** protocol. It does not support complex order types (e.g., Stop Loss, Trailing Stop, OCO). It assumes the *client* (the algorithm) manages all logic.
*   **Exchange Responsibility:** Match orders.
*   **Client Responsibility:** logic, risk, smart routing, conditional triggers.

### 1.2 The "Token" Concept (Client Order ID)
In FIX, you often wait for the exchange to assign an OrderID. In OUCH, **you** assign the ID (Token).
*   **Benefit:** You don't need to parse the acknowledgement to know which order is yours. You already know.
*   **Constraint:** You must guarantee uniqueness.

---

## 2. Protocol Architecture

### 2.1 Transport Layer: TCP/IP
Unlike ITCH (UDP Multicast), OUCH uses **TCP**.
*   **Why?** Order entry requires **guaranteed delivery**. You cannot afford to "drop" a buy order packet.
*   **Session:** Persistent TCP connection. If the connection drops, all open orders are usually canceled (Cancel-on-Disconnect), though this is configurable.

### 2.2 SoupBinTCP (The Session Layer)
OUCH payloads are wrapped in **SoupBinTCP** (or a similar lightweight session wrapper).
*   **Packet Structure:**
    *   `[Packet Length (2)]`
    *   `[Packet Type (1)]` ('U' = Unsequenced, 'S' = Sequenced)
    *   `[OUCH Payload]`
*   **Heartbeats:** Client must send a heartbeat (usually 1 byte) every 1 second if silent. Server responds.
*   **Login:** The first message is a Login Request (User/Pass).

---

## 3. Message Formats (Deep Dive)

All integers are **Big-Endian**. Strings are left-justified, space-padded.

### 3.1 Enter Order ('O') - The Hot Path
This is 90% of your traffic.
*   **Token (14 bytes):** Your ID. e.g., "MMAK-0000001".
*   **Buy/Sell (1 byte):** 'B' / 'S'.
*   **Shares (4 bytes):** Integer.
*   **Stock (8 bytes):** "AAPL    ".
*   **Price (4 bytes):** Fixed Point 4 ($150.00 = 1,500,000).
*   **Time In Force (4 bytes):**
    *   `0`: Day
    *   `99999`: IOC (Immediate or Cancel)
    *   `99998`: Market Hours IOC
*   **Display (1 byte):** 'Y' (Visible) / 'N' (Hidden).
*   **Capacity (1 byte):** 'P' (Principal/Prop) vs 'A' (Agency).

**Optimization:** The payload is fixed length (~48-50 bytes).
*   **Pre-computation:** Construct the static parts (Token Prefix, Stock, Capacity) at startup.
*   **Runtime:** Only memcpy `Price` and `Shares` and `Token Suffix` into the buffer before `send()`.

### 3.2 Order Accepted ('A')
The "Ack".
*   **Timestamp (8 bytes):** Nanoseconds. **CRITICAL** for latency measurement (T_ack - T_sent).
*   **Order Reference Number (8 bytes):** The Exchange's ID (matches ITCH).
*   **State:** The order is now LIVE in the book.

### 3.3 Order Rejected ('J')
*   **Reason Code (1 byte):**
    *   'C': Exchange Closed.
    *   'R': Reg SHO restricted.
    *   'X': Fat finger checks.
*   **ClOrdID:** Tells you *which* order failed.

### 3.4 Cancel Order ('X')
*   **Token (14 bytes):** The ID of the order to cancel.
*   **Shares (4 bytes):** Number of shares to cancel.

### 3.5 Replace Order ('U') - Atomic Modify
*   **Existing Token (14 bytes):** Old order.
*   **New Token (14 bytes):** New ID for the modified order.
*   **Shares / Price:** New values.
*   **Logic:** If the size increases or price changes, you lose queue priority. If size decreases (partial cancel), you *keep* priority (usually).

---

## 4. State Management & Race Conditions

Implementing OUCH is about managing state transitions correctly.

### 4.1 The "Pending" State
1.  **Send 'O' (Enter Order).**
2.  **State:** `PENDING_NEW`.
3.  **Receive 'A' (Accepted).**
4.  **State:** `LIVE`.

**Race Condition:** What if you want to Cancel while `PENDING_NEW`?
*   **Scenario:** You sent Order A. Price moves. You want to Cancel A immediately.
*   **OUCH Rule:** You can send 'X' (Cancel) for Token A even before you get the 'A' (Accept). The exchange will process them in order (Enter -> Cancel).
*   **Exception:** If the Enter failed (Rejected), the Cancel will also fail ("Order Not Found").

### 4.2 The "Phantom Fill"
1.  **Send 'X' (Cancel).** State: `PENDING_CANCEL`.
2.  **Receive 'E' (Executed).**
3.  **Receive 'C' (Canceled).**
*   **Reality:** You got filled *while* the cancel message was on the wire (wire time + processing time).
*   **Result:** You are Long 100 shares. Your algo must handle this inventory immediately.

---

## 5. Performance Tuning

### 5.1 Nagle's Algorithm (TCP_NODELAY)
**MANDATORY:** Disable Nagle's algorithm on the socket.
```cpp
int flag = 1;
setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, (char *)&flag, sizeof(int));
```
If you forget this, the OS will buffer your small 50-byte order packets for 40ms, destroying your strategy.

### 5.2 Optimistic Sending
Don't wait for the OS to tell you the socket is writable. Just call `send()`. If it returns `EAGAIN` (rare in HFT volumes), then buffer.

### 5.3 Sequence Numbers
SoupBinTCP uses sequence numbers.
*   **Inbound:** Track server sequence. If gap -> Request Packet Store.
*   **Outbound:** You don't need to sequence your orders at the session layer usually, but OUCH tokens must be unique.

---

## 6. Implementation Checklist

1.  **Login Sequence:** Connect -> Send Login -> Wait for Login Accept -> Start Heartbeat Thread.
2.  **Token Generator:** High-performance formatter (int -> string).
3.  **Buffer Pool:** Pre-allocated byte arrays for "Enter Order" messages for every symbol universe.
4.  **Parsing:**
    *   Read 2 bytes (Length).
    *   Read Type.
    *   Cast payload to struct.
    *   `ntohl()` fields.
5.  **Recovery:** On disconnect, do you try to "Cancel All" on reconnect? Or assume they are dead? (Check `Cancel-on-Disconnect` settings with the exchange).

---

## 7. Comparison: OUCH vs. FIX

| Feature | OUCH | FIX |
| :--- | :--- | :--- |
| **Format** | Binary (Fixed Length) | ASCII (Tag=Value) |
| **Parsing Cost** | ~10-50 nanoseconds | ~1-5 microseconds |
| **Bandwidth** | Tiny (50 bytes) | Bloated (200+ bytes) |
| **Complexity** | Low (Dumb pipe) | High (Validation, flexible fields) |
| **Use Case** | HFT, Market Making | Client Flow, Care Orders |

---

## References
*   **Nasdaq OUCH 5.0 Specification**
*   **SoupBinTCP 3.0 Specification**
