---
type: problem-set
track: [quant-dev]
tier: core
status: solid
prereqs: [order-book-and-matching-engine, concurrency-lock-free-and-memory-pools, market-data-feed-handlers-and-protocols, backtester-and-simulator-design, risk-checks-and-order-management, testing-trading-and-numerical-code]
est_hours: 6
sources: [Nasdaq - TotalView-ITCH 5.0 Interface Specification (version 5.0 - 03/06/2015), Nasdaq - MoldUDP64 Protocol Specification V1.00, 17 CFR 240.15c3-5 - Risk management controls for brokers or dealers with market access (75 FR 69825 - Nov 15 2010), SEC Release No. 34-70694 - In the Matter of Knight Capital Americas LLC (October 16 2013), FIX Trading Community - FIX 4.4 specification, Higham - Accuracy and Stability of Numerical Algorithms 2nd ed (SIAM 2002) ch 1 2 4, Almgren and Chriss - Optimal Execution of Portfolio Transactions - Journal of Risk 3(2) 2000, Borror - Q for Mortals]
---

# Quant Dev Problem Set

## TL;DR

- Quant-dev interviews test whether you can turn a systems question into numbers: bytes per message, packets per second, bits on the wire, sequence numbers to request, shares ahead in a queue, worst-case exposure, ulps of error.
- State assumptions first, compute with them, then name the assumption most likely to be wrong; every answer here follows that pattern and every number is printed and asserted by [quant_dev_problem_set.py](code/python/quant_dev_problem_set.py).
- Feed handlers: batch to save bandwidth, sequence numbers to find gaps, A/B lines to avoid most retransmissions, snapshots to start late.
- Simulators and pricers: the fill model and the bump size are where naive answers are quietly wrong.
- Risk and testing: check the worst case including open orders, make every handler idempotent, and size test tolerances so a correct build almost never fails.

## Learning objectives

- Answer quant-developer interview questions on C++, systems and trading infrastructure.
- Do back-of-envelope sizing for feeds and tick stores from stated assumptions.
- Work order-book, queue-position, sequencing and order-state problems by hand.
- Reason about numerical error, tolerances and flaky tests quantitatively.

## Core concepts

This note is a problem set over [Market Data Feed Handlers](08-Market-Data-Feed-Handlers-and-Protocols.md), [Backtester and Simulator Design](09-Backtester-and-Simulator-Design.md), [Pricing Library Design](10-Pricing-Library-Design.md), [Numerical Python](11-Numerical-Python-NumPy-and-Numba.md), [Tick Data Storage](12-Tick-Data-Storage-and-Time-Series-Databases.md), [Risk Checks and Order Management](13-Risk-Checks-and-Order-Management.md) and [Testing Trading and Numerical Code](14-Testing-Trading-and-Numerical-Code.md).
The theory lives in those notes; this section collects the formulas and constants the problems use.

### Constants worth knowing cold

| Quantity | Value | Source |
| :--- | :--- | :--- |
| ITCH 5.0 Add Order (`A`) length | 36 bytes | TotalView-ITCH 5.0 spec, section 4.3.1 |
| ITCH 5.0 timestamp | 6 bytes, nanoseconds since midnight | spec, Data Types |
| ITCH 5.0 Price(4) maximum | 200,000.0000 = 0x77359400 = 2,000,000,000 | spec, Data Types |
| MoldUDP64 header | 20 bytes: session 10, sequence 8, count 2 | MoldUDP64 V1.00 |
| MoldUDP64 message block | 2-byte length + message | MoldUDP64 V1.00 |
| MoldUDP64 heartbeat / end of session | count 0 / count 0xFFFF | MoldUDP64 V1.00 |
| IPv4 + UDP headers | 20 + 8 bytes | RFC 791, RFC 768 |
| Ethernet per-frame overhead on the wire | 14 header + 4 FCS + 8 preamble/SFD + 12 inter-frame gap = 38 bytes | IEEE 802.3 |
| float64 machine epsilon $\epsilon$ | $2^{-52} \approx 2.22 \times 10^{-16}$ | IEEE 754 |
| float32 integers exact up to | $2^{24} = 16{,}777{,}216$ | IEEE 754 |

### Formulas used repeatedly

- Messages per packet: $\lfloor (\text{MTU} - 20 - 8 - 20) / (L + 2) \rfloor$ for MoldUDP64 over IPv4 with message length $L$.
- Wire rate: $\text{packets/s} \times (\text{IP bytes} + 38) \times 8$.
- Independent A/B loss: $P(\text{both lose a packet}) = p_A p_B$.
- Square-root impact: $\Delta P / P \approx Y\sigma_{\text{daily}}\sqrt{Q/V}$ with $Y$ of order 1.
- Finite-difference bump: forward error $\approx \tfrac{h}{2}|f''| + \epsilon|f|/h$, optimal $h \sim \sqrt{\epsilon}\,x$; central error $\approx \tfrac{h^2}{6}|f'''| + \epsilon|f|/h$, optimal $h \sim \epsilon^{1/3}x$.
- Worst-case position: $\text{position} + \text{open buys} + \text{new buy}$ for a long limit (sells cannot be assumed to fill).
- Average price: $\text{AvgPx} = \sum q_i p_i / \sum q_i$; $\text{LeavesQty} = \text{OrderQty} - \text{CumQty}$ for a live order.
- Test false-failure rate at a $z$-standard-error tolerance: $P(|Z| > z)$, and for $n$ independent such tests $1 - (1 - P(|Z|>z))^n$.

### How to answer a sizing question

1. Write the assumptions as numbers on the board.
2. Compute the headline (bytes per day, packets per second) to two significant figures.
3. Say which resource saturates first: for market data it is usually packet rate and per-packet CPU, not bits per second.
4. Say what you would measure to replace the weakest assumption.

## Worked examples

### 1. Bandwidth of an ITCH burst

"A burst carries 2,000,000 Add Order messages per second over MoldUDP64. What is the wire rate, and what if every message went in its own packet?"
Each message block is $36 + 2 = 38$ bytes.
A 1500-byte MTU leaves $1500 - 20 - 8 = 1472$ bytes of UDP payload, minus the 20-byte MoldUDP64 header gives 1452, so $\lfloor 1452/38 \rfloor = 38$ messages per packet.
The IP packet is $20 + 8 + 20 + 38 \times 38 = 1492$ bytes and the frame occupies $1492 + 38 = 1530$ bytes of wire time.
Packets per second: $2{,}000{,}000/38 = 52{,}631.6$, so the rate is $52{,}631.6 \times 1530 \times 8 = 0.644$ Gbit/s.
Unbatched, each frame is $20 + 8 + 20 + 38 + 38 = 124$ bytes and the rate is $2 \times 10^6 \times 124 \times 8 = 1.984$ Gbit/s, three times more, at 2 million packets per second.
The bandwidth fits a 10 GbE link either way; the packet rate is what breaks a kernel socket path, which is why feeds batch and why handlers use kernel bypass.

### 2. Gap detection and the retransmission request

"Your handler expects sequence 1001. Packets arrive as (seq 1001, count 3), (1007, 2), then a retransmission (1004, 3), then (1005, 2) from the slower line. What do you do at each step?"
The first packet applies 1001 to 1003, so the next expected is 1004.
The second starts at 1007, so 1004 to 1006 are missing: buffer 1007 and 1008 and send a MoldUDP64 Request Packet with sequence number 1004 and requested message count 3.
The retransmission fills 1004 to 1006; apply them and then drain the buffer, applying 1007 and 1008, so the next expected is 1009.
The last packet carries 1005 and 1006, both below 1009, so both are dropped as duplicates (2 duplicates in total).
Eight messages are applied, each exactly once, in sequence order.

### 3. Book state after an ITCH message sequence

"Replay: A ref 1 buy 100 at 10.0000; A ref 2 buy 200 at 10.0100; A ref 3 sell 300 at 10.0300; A ref 4 sell 150 at 10.0200; E ref 2 executed 50; X ref 3 cancel 100; U ref 1 to new ref 5 with 120 at 10.0150; D ref 4. What is the book?"
Order 2 keeps $200 - 50 = 150$; order 3 keeps $300 - 100 = 200$; the replace removes order 1 and adds order 5 on the buy side (side is inherited, because the Order Replace message does not carry it), 120 at 10.0150; order 4 is deleted.
Bids: 10.0150 x 120, 10.0100 x 150.
Asks: 10.0300 x 200.
Spread 0.0150, mid 10.0225.
The trap is keying the replacement by the old reference number: every later message for this order uses ref 5.

### 4. Queue position with an order-level versus a price-level feed

"You join the bid at 50.00 with 300 shares behind 4,000. Then 1,500 trade at the level, 1,000 ahead of you cancel, 1,200 trade, 600 trade. When do you fill?"
With order-level data you know which cancels are ahead: ahead goes $4000 \to 2500 \to 1500 \to 300$, and the final 600-share trade eats the last 300 ahead and fills your 300 on that event.
With only aggregated level sizes you cannot tell where the cancel came from; the pessimistic rule (cancels come from behind you) leaves ahead at $4000 - 1500 - 1200 - 600 = 700$, so you are not filled, and it takes one more 1,000-share trade to fill you.
The two rules bracket reality; a simulator should say which one it uses and report results under both.

### 5. Optimal finite-difference bump for delta

"Black-Scholes call, $S = K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$. Analytic delta 0.6368. Which bump size?"
Forward difference has truncation $\tfrac{h}{2}\Gamma$ and round-off $\epsilon C/h$, optimal near $\sqrt{\epsilon}S = 1.49 \times 10^{-6}$; central difference has truncation $O(h^2)$, optimal near $\epsilon^{1/3}S = 6.06 \times 10^{-4}$.
Measured errors: forward at its optimal $h$ is $1.7 \times 10^{-8}$, central at its optimal $h$ is $3.0 \times 10^{-11}$.
With $h = 1$ the errors are $9.29 \times 10^{-3}$ (forward, close to $\Gamma/2 = 0.0094$) and $8.60 \times 10^{-5}$ (central).
With $h = 10^{-12}$ the central error explodes to the order of $10^{-2}$ ($8.0 \times 10^{-3}$ on the reference machine; the digits depend on libm rounding), because the two prices agree in almost every digit and the difference is round-off.

### 6. Negative variance from the textbook formula

"Prices are $10^9 + \{4, 7, 13, 16\}$ in some fixed-point unit. Compute the sample variance."
Exact: mean offset 10, squared deviations $36 + 9 + 9 + 36 = 90$, sample variance $90/3 = 30$.
The one-pass formula $(\sum x^2 - (\sum x)^2/n)/(n-1)$ in float64 returns $-170.67$: the sums are near $4 \times 10^{18}$ where one ulp is 512, so the subtraction cancels every meaningful digit.
Welford's update and NumPy's two-pass `np.var(x, ddof=1)` both return exactly 30.

### 7. Worst-case position check

"Limit: 10,000 shares long. Position 3,000 long, open buys 4,000, open sells 2,500. A new buy for 4,000 arrives. Accept?"
Reject.
The worst case is that every buy fills and no sell does: $3000 + 4000 + 4000 = 11{,}000 > 10{,}000$.
Netting the open sells (which would give 8,500) assumes fills you do not control; the SEC found that Knight's position limits "did not account for the firm's exposure from outstanding orders" (Release No. 34-70694, paragraph 22).

### 8. Execution reports and a racing replace

"Buy 1,000. Fills: 300 at 10.00, 200 at 10.02, 500 at 10.05. Give CumQty, LeavesQty and AvgPx after each fill. Separately, you send a replace to quantity 600 while 500 are already filled. What is left?"
After fill 1: 300, 700, 10.0000; fill 2: 500, 500, 10.008; fill 3: 1000, 0, 10.029 with $\text{AvgPx} = (3000 + 2004 + 5025)/1000$.
In FIX, OrderQty on a cancel/replace is the total intended quantity including what has already executed, so after the replace LeavesQty is $600 - 500 = 100$, not 600.

### 9. Why a statistical test suite is flaky

"200 Monte Carlo regression tests each assert the estimate is within 3 standard errors of a reference. How often does a correct build fail CI?"
$P(|Z| > 3) = 0.00270$ per test, so $1 - (1 - 0.0027)^{200} = 0.418$: almost half of all runs fail with no bug.
At 4 standard errors, $P(|Z|>4) = 6.33 \times 10^{-5}$ and the suite fails 0.0126 of the time; better still, fix the seed so the result is deterministic and compare against a golden value, and keep a separate statistical test that runs with fresh seeds and a tight false-alarm budget.
With payoff standard deviation 15 and 100,000 paths the standard error is 0.0474, so a 4-SE tolerance is 0.190.

## Pitfalls

- Sizing a feed by bits per second only; the binding constraint is usually packets per second and per-packet work.
- Treating A/B line losses as independent; shared upstream switches and microbursts make losses correlated, so double losses are more frequent than $p^2$ suggests.
- Requesting retransmission one message at a time instead of one request per contiguous gap.
- Forgetting that ITCH Order Replace assigns a new reference number and omits the side and stock.
- Assuming a resting limit order fills whenever the price touches it; queue position and adverse selection decide.
- Picking a bump size by habit ($h = 0.01$ or $h = 10^{-8}$ for everything) instead of scaling by the input and the difference scheme.
- Netting open sells against open buys in a pre-trade position check.
- Comparing floats with `==` or a single absolute tolerance across quantities of very different magnitude.
- Setting statistical test tolerances per test without accounting for the number of tests in the suite.

## Interview questions

> [!question]- qd-ps-itch-add-order-size | How many bytes is a TotalView-ITCH 5.0 Add Order (`A`) message, and what are its fields?
> 36 bytes: type 1, stock locate 2, tracking number 2, timestamp 6, order reference number 8, buy/sell 1, shares 4, stock 8, price 4. The MPID-attributed `F` variant adds a 4-byte attribution field for 40 bytes.

> [!question]- qd-ps-mold-packing | With MoldUDP64 over IPv4 and a 1500-byte MTU, how many 36-byte ITCH messages fit in one packet?
> 38. UDP payload is $1500 - 20 - 8 = 1472$; minus the 20-byte MoldUDP64 header leaves 1452; each block is $36 + 2 = 38$ bytes, and $\lfloor 1452/38\rfloor = 38$.

> [!question]- qd-ps-burst-bandwidth | 2 million Add Orders per second, batched 38 per packet: what is the wire rate?
> 0.644 Gbit/s. 52,631.6 packets/s of 1492-byte IP packets, plus 38 bytes of Ethernet header, FCS, preamble and inter-frame gap, is 1530 bytes each; $52{,}631.6 \times 1530 \times 8$.

> [!question]- qd-ps-unbatched-bandwidth | Same burst with one message per packet?
> 1.984 Gbit/s at 2 million packets per second. Each frame is $20 + 8 + 20 + 38 + 38 = 124$ bytes on the wire; the bandwidth triples, and the packet rate, not the bandwidth, is what overwhelms a kernel network stack.

> [!question]- qd-ps-gap-request | Expected sequence 1004; a MoldUDP64 packet arrives with sequence 1007 and count 2. What exactly do you send?
> A Request Packet with the session, sequence number 1004 and requested message count 3, to the re-request server. Buffer 1007 and 1008 meanwhile; apply nothing out of order.

> [!question]- qd-ps-gap-duplicates | After applying through 1008, a packet (seq 1005, count 2) arrives from the slower line. What happens?
> Both messages are dropped as duplicates because their sequence numbers are below the next expected (1009). Sequence numbers make A/B merging and retransmission idempotent.

> [!question]- qd-ps-mold-heartbeat | How does a MoldUDP64 listener detect loss when the market is quiet?
> Heartbeat packets (message count 0) carry the next expected sequence number, typically about once per second; if it is ahead of yours, you have a gap. Count 0xFFFF signals end of session.

> [!question]- qd-ps-ab-double-loss | Each line independently loses a packet with probability $10^{-5}$; 20 million packets per day. How often is a packet lost on both lines?
> Expected 0.002 per day, about once per 500 trading days, versus 200 single-line losses per day that arbitration hides. In practice losses are correlated (shared infrastructure, microbursts), so plan for retransmission anyway.

> [!question]- qd-ps-itch-price-range | Does an ITCH Price(4) field fit in a signed 32-bit integer?
> Yes. The maximum is 200,000.0000, raw 2,000,000,000 (0x77359400), below $2^{31} - 1 = 2{,}147{,}483{,}647$; the field is unsigned 32-bit on the wire.

> [!question]- qd-ps-itch-timestamp | Why is a 6-byte nanosecond timestamp enough, and why would 4 bytes not be?
> $2^{48} - 1$ ns is 78.2 hours, more than the $8.64 \times 10^{13}$ ns in a day. A 32-bit nanosecond counter wraps after 4.295 seconds.

> [!question]- qd-ps-seq-wrap | Do you need to handle wraparound of a 64-bit sequence number? A 32-bit one?
> 64-bit: no, at 10 million messages per second it wraps after about 58,454 years. 32-bit: at 1 million per second it wraps after 71.6 minutes, so a 32-bit counter needs explicit wrap or session reset handling.

> [!question]- qd-ps-book-replay | Replay A1 buy 100 at 10.0000, A2 buy 200 at 10.0100, A3 sell 300 at 10.0300, A4 sell 150 at 10.0200, E2 50, X3 100, U1 to ref 5 120 at 10.0150, D4. Best bid and offer?
> Bid 10.0150 x 120, offer 10.0300 x 200, spread 0.0150. Order 2 keeps 150 at 10.0100 behind the new best bid; order 4 was deleted, so 10.0200 is empty.

> [!question]- qd-ps-replace-keying | After an ITCH Order Replace, which reference number and side do later messages use?
> The new order reference number, for all subsequent updates; the side, stock and attribution are not in the Replace message and must be carried over from the original Add Order.

> [!question]- qd-ps-snapshot-merge | You buffer live messages 5,000,100 to 5,000,200 and then receive a snapshot that is current as of sequence 5,000,123. What do you do with the buffer?
> Discard the 24 messages 5,000,100 to 5,000,123 (already reflected in the snapshot) and apply the 77 messages 5,000,124 to 5,000,200 in order. Start buffering before requesting the snapshot so nothing falls between them.

> [!question]- qd-ps-queue-order-level | Joined at 50.00 with 300 behind 4,000; then trade 1,500, cancel 1,000 known to be ahead, trade 1,200, trade 600. Filled?
> Yes, on the 600 trade. Ahead goes 4000, 2500, 1500, 300; the last trade eats 300 ahead and 300 of yours.

> [!question]- qd-ps-queue-level-only | Same events, but you only see aggregated level sizes and assume cancels come from behind you. Filled?
> No: 700 still ahead after the 600 trade, and one more 1,000-share trade is needed. The optimistic and pessimistic rules bracket the true queue; report results under both.

> [!question]- qd-ps-latency-budget | Market data reaches you 15 us after the print, the strategy takes 5 us, order entry takes 30 us to reach the matching engine. When does your order arrive, and what should the simulator do with it?
> At 50 us after the print. The simulator must match it against the book as it stood at 50 us, not at 0, including queue changes and price moves in between.

> [!question]- qd-ps-sqrt-impact | Square-root impact with $Y = 1$, daily volatility 2%, order 500,000 shares, daily volume 10 million: impact in bp and dollars at a 40-dollar stock?
> 44.7 bp, about 89,443 dollars. $0.02\sqrt{0.05} = 0.00447$; times $500{,}000 \times 40$.

> [!question]- qd-ps-bs-known-answer | Known-answer test: Black-Scholes call and put with $S = K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$, no dividends?
> Call 10.4506, put 5.5735. Parity check $C - P = K(1 - e^{-rT}) = 4.8771$. Delta 0.6368, gamma 0.018762, vega 37.524 per unit vol.

> [!question]- qd-ps-bump-size | Optimal bump for forward and central difference delta at $S = 100$?
> Forward about $\sqrt{\epsilon}S = 1.49 \times 10^{-6}$ (error $1.7 \times 10^{-8}$); central about $\epsilon^{1/3}S = 6.06 \times 10^{-4}$ (error $3.0 \times 10^{-11}$). Each balances $O(h)$ or $O(h^2)$ truncation against $\epsilon|f|/h$ round-off.

> [!question]- qd-ps-bump-too-small | What happens to a central-difference delta with $h = 10^{-12}$?
> It is wrong in the third decimal (error of order $10^{-2}$, $8.0 \times 10^{-3}$ on the reference machine). The two prices agree to almost all digits, so the difference is mostly round-off divided by a tiny $h$.

> [!question]- qd-ps-bump-count | A trade depends on 50 curve pillars and 200 vol nodes. How many pricings for bump-and-reprice sensitivities, and what does AAD change?
> 251 one-sided or 501 central pricings. Reverse-mode AAD returns all 250 sensitivities from one forward pass and one backward sweep, at a small constant multiple of one pricing and independent of the number of inputs, at the cost of memory for the tape.

> [!question]- qd-ps-array-bytes | A float64 array of shape (10,000, 5,000): size and strides in C order and of its transpose?
> 400,000,000 bytes (381.47 MiB); strides (40000, 8); the transpose is a view with strides (8, 40000). No data moves.

> [!question]- qd-ps-column-sum-cache | Why is summing one column of that C-order array slow?
> `a[:, 0]` is a view with stride 40,000 bytes, so each of the 10,000 elements sits on its own 64-byte cache line: 640,000 bytes move for 80,000 useful, an 8x amplification, and the prefetcher sees a large stride.

> [!question]- qd-ps-broadcast | What shape does broadcasting (3, 1, 5) with (4, 1) give? And (3, 2) with (3,)?
> (3, 4, 5): align from the right, so (4, 1) acts as (1, 4, 1) and size-1 axes stretch. (3, 2) with (3,) is an error: trailing sizes 2 and 3 differ and neither is 1.

> [!question]- qd-ps-float32-volume | Why must cumulative share volume never be accumulated in float32?
> float32 represents integers exactly only up to $2^{24} = 16{,}777{,}216$; there the ulp is 2, so $2^{24} + 1$ rounds back to $2^{24}$ and single-share updates vanish. Use 64-bit integers.

> [!question]- qd-ps-negative-variance | Sample variance of $10^9 + \{4, 7, 13, 16\}$ by $(\sum x^2 - (\sum x)^2/n)/(n-1)$ in float64?
> $-170.67$ instead of 30: the sums are near $4 \times 10^{18}$, where one ulp is 512, so the subtraction cancels all meaningful digits. Welford or two-pass gives exactly 30.

> [!question]- qd-ps-int32-notional | Price 100.0000 as ITCH Price(4) (1,000,000) times 5,000 shares in int32 arrays: result?
> 705,032,704 instead of 5,000,000,000: NumPy wraps fixed-width integer arithmetic silently ($5 \times 10^9 - 2^{32}$). Widen to int64 before multiplying.

> [!question]- qd-ps-tick-capacity | 400 million messages per day, 40 bytes each, 252 days, 4x compression, 10 years, 3 replicas: storage?
> 16 GB per day raw, 4.032 TB per year raw, 1.008 TB per year compressed, 30.24 TB in total. Say which assumption is weakest (message count grows year on year).

> [!question]- qd-ps-partition-pruning | Ticks partitioned by date and 64 symbol hash buckets. A one-symbol, one-year query reads what fraction?
> 252 of 16,128 partitions, 1/64 of the data. Columnar layout cuts it further: reading 3 of 20 equal-width columns reads 15% of each partition.

> [!question]- qd-ps-asof-join | Trades at t = 10, 25, 40, 55; quotes at t = 5, 20, 30, 50. Backward as-of join with an 8-unit staleness limit: which quote does each trade get?
> Quotes at 5, 20, none, 50. The trade at 40 would match the quote at 30, but it is 10 old, past the limit. A forward join (quotes at 20, 30, 50, none) is look-ahead.

> [!question]- qd-ps-worst-case-position | Long limit 10,000; position 3,000; open buys 4,000; open sells 2,500; new buy 4,000. Accept?
> Reject: worst case $3000 + 4000 + 4000 = 11{,}000$. Never net open sells, because you do not control whether they fill.

> [!question]- qd-ps-collar-notional | Reference price 50.00 with a 5% collar, max notional 1 million dollars. Do a buy at 53.00 and a buy of 10,000 at 250.00 pass?
> Both are rejected. The buy collar upper bound is 52.50, and 10,000 x 250 is 2.5 million dollars of notional.

> [!question]- qd-ps-token-bucket | Token bucket with capacity 20 and refill 100 per second. 50 orders arrive at t = 0 and 15 at t = 0.1 s. How many pass?
> 20 at t = 0 (the burst capacity) and 10 at t = 0.1 s (10 tokens refilled); 35 are rejected. Capacity sets the burst, refill rate sets the sustained rate.

> [!question]- qd-ps-avgpx | Buy 1,000 filled 300 at 10.00, 200 at 10.02, 500 at 10.05. Final CumQty, LeavesQty and AvgPx?
> 1000, 0, 10.029: $(3000 + 2004 + 5025)/1000$. After the second fill AvgPx is 10.008 with LeavesQty 500.

> [!question]- qd-ps-replace-race | A 1,000 order has 500 filled when your replace to OrderQty 600 is accepted. LeavesQty?
> 100. FIX OrderQty on a cancel/replace is the total intended quantity including what has already executed, so leaves = $600 - 500$.

> [!question]- qd-ps-knight-paragraphs | Which parts of Rule 15c3-5 did the SEC find Knight Capital violated?
> (c)(1)(ii) erroneous-order controls, (c)(1)(i) aggregate capital thresholds, (b) twice (inadequate written description of controls, and no technology governance over code deployment and unused code), (e)(1) review, and (e)(2) the defective 2012 CEO certification (SEC Release No. 34-70694).

> [!question]- qd-ps-ulp-03 | How far apart are `0.1 + 0.2` and `0.3` in float64?
> One ulp: their difference is $5.55 \times 10^{-17}$, and adjacent doubles near 0.3 are $5.55 \times 10^{-17}$ apart. Compare with a relative or ulp tolerance, never `==`.

> [!question]- qd-ps-associativity | Compute $(10^{16} + 1) - 10^{16}$ and $(10^{16} - 10^{16}) + 1$ in float64. What does this mean for parallel reductions?
> 0 and 1. The ulp at $10^{16}$ is 2, so the 1 is lost. Parallel sums with a varying reduction order are therefore not bit-reproducible; fix the reduction tree or use compensated summation when results must match exactly.

> [!question]- qd-ps-flaky-suite | 200 tests each assert a Monte Carlo estimate is within 3 standard errors. Probability a correct build fails?
> 0.418. Each fails with probability 0.00270 and $1 - 0.9973^{200}$. At 4 SE it drops to 0.0126; with a fixed seed it is deterministic.

> [!question]- qd-ps-mc-tolerance | Payoff standard deviation 15, 100,000 paths. What tolerance gives a two-sided false-failure rate of $6.33 \times 10^{-5}$?
> 0.190, that is 4 standard errors, with standard error $15/\sqrt{100{,}000} = 0.0474$.

> [!question]- qd-ps-fuzz-odds | A parser bug triggers only when bytes 4 and 5 equal one specific 16-bit value. Chance that 100,000 uniform random inputs find it?
> 0.783: $1 - (1 - 1/65536)^{100000}$. Coverage-guided fuzzers do far better because they keep inputs that reach new branches and mutate them.

> [!question]- qd-ps-naive-sum-bound | Worst-case relative error bound of naive left-to-right summation of $10^6$ float64 terms of one sign?
> About $nu = 10^6 \times 1.11 \times 10^{-16} = 1.11 \times 10^{-10}$ (Higham ch 4, with unit roundoff $u = \epsilon/2$). Pairwise summation, which `np.sum` uses, grows like $u\log_2 n$ instead.

## In this repo and SDE-Interview-Prep

- Code: [quant_dev_problem_set.py](code/python/quant_dev_problem_set.py) computes, prints and asserts every number above.
- [LeetCode quant set (C++) (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/LeetCode-Quant-Complete-CPP-Full.md)
- Concept notes: [08](08-Market-Data-Feed-Handlers-and-Protocols.md), [09](09-Backtester-and-Simulator-Design.md), [10](10-Pricing-Library-Design.md), [11](11-Numerical-Python-NumPy-and-Numba.md), [12](12-Tick-Data-Storage-and-Time-Series-Databases.md), [13](13-Risk-Checks-and-Order-Management.md), [14](14-Testing-Trading-and-Numerical-Code.md).

## Further reading

- Nasdaq, *TotalView-ITCH 5.0 Interface Specification* (in [protocol-specs](protocol-specs/)), sections 3 and 4.
- Nasdaq, *MoldUDP64 Protocol Specification*, version 1.00.
- 17 CFR 240.15c3-5, Risk management controls for brokers or dealers with market access (75 FR 69825, November 15, 2010).
- SEC, *In the Matter of Knight Capital Americas LLC*, Release No. 34-70694 (October 16, 2013).
- Nicholas Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd edition (SIAM 2002), chapters 1, 2 and 4.
- Robert Almgren and Neil Chriss, "Optimal Execution of Portfolio Transactions", *Journal of Risk* 3(2) (2000).
- Jeffry Borror, *Q for Mortals*.
