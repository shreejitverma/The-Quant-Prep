# Quant Dev (Market Making): Regulation NMS + Regulation SHO
*A practical, production-oriented learning document for U.S. equities market making systems.*

## Table of contents
- [1. Why this matters in market making](#1-why-this-matters-in-market-making)
- [2. Regulation NMS (market structure)](#2-regulation-nms-market-structure)
- [3. Regulation SHO (short selling)](#3-regulation-sho-short-selling)
- [4. Turning regs into system requirements](#4-turning-regs-into-system-requirements)
- [5. Interview readiness checklist](#5-interview-readiness-checklist)
- [6. Practical build exercises](#6-practical-build-exercises)
- [7. Glossary](#7-glossary)
- [8. Source anchors](#8-source-anchors)

***

## 1. Why this matters in market making
As a quantitative developer in market making, you ship systems that (a) quote and hedge continuously, (b) route orders across fragmented venues, and (c) must be **provably compliant** under stress. Reg NMS drives how execution interacts with protected quotes across venues (especially Rule 611), while Reg SHO governs the operational/legal correctness of short sales (marking, locate, circuit breaker, close-out). [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

What hiring managers test: Can you translate regulations into *deterministic runtime gates*, data dependencies, and audit logs that survive latency, feed gaps, and partial failures? [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)

***

## 2. Regulation NMS (market structure)
Regulation NMS is a set of initiatives adopted by the SEC to modernize and strengthen the national market system for equity securities. [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)

### 2.1 The “big four” rules (how to memorize)
A widely used breakdown (also reflected in SEC/industry summaries) is that Reg NMS introduced four key rules: **603, 610, 611, 612**. [sec](https://www.sec.gov/spotlight/emsac/memo-rule-611-regulation-nms.pdf)

- **Rule 603**: distribution, consolidation, and display of market data. [sec](https://www.sec.gov/spotlight/emsac/memo-rule-611-regulation-nms.pdf)
- **Rule 610**: access to quotations; includes a limit on access fees and requires fair/non-discriminatory access (with related SRO obligations around locking/crossing). [sec](https://www.sec.gov/spotlight/emsac/memo-rule-611-regulation-nms.pdf)
- **Rule 611**: order protection / trade-through restrictions (intermarket price protection). [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- **Rule 612**: sub-penny quoting constraints (minimum pricing increment, with exceptions). [sec](https://www.sec.gov/spotlight/emsac/memo-rule-611-regulation-nms.pdf)

### 2.2 Rule 611 (Order Protection): what you must be able to explain
#### Core requirement (text-level)
Rule 611 requires a trading center to establish, maintain, and enforce written policies and procedures reasonably designed to prevent trade-throughs of protected quotations in NMS stocks (unless an exception applies), and to regularly surveil effectiveness and promptly remedy deficiencies. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

#### Exceptions (be able to name examples)
Rule 611 contains enumerated exceptions in paragraph (b), including cases such as systems failure/delay at the trading center displaying the protected quote, non-regular-way contracts, and single-priced opening/reopening/closing transactions, among others. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

#### ISOs (Intermarket Sweep Orders)
Rule 611 also addresses intermarket sweep orders and requires the party responsible for routing an ISO to take reasonable steps to establish that the order meets the definition/requirements referenced in the rule. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

**Quant dev translation:** your SOR must (1) detect trade-through risk vs protected quotes, (2) either re-route/price-adjust or apply a valid exception workflow (commonly an ISO sweep plan), and (3) log the exact quote state and exception rationale. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

### 2.3 Rule 610 (Access): why makers care
SEC staff materials describe Rule 610 as requiring fair and non-discriminatory access to quotations and setting a limit on access fees to harmonize quotation pricing across trading centers, with SRO rule requirements that relate to locking/crossing. [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)

**Quant dev translation:** economics ≠ compliance price. Your router must respect protected quote obligations under Rule 611 while your strategy optimizes *realized* economics net of fees/rebates, queue, and latency. [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)

### 2.4 Rule 612 (Sub-penny): why microstructure changes
Reg NMS summaries explain that Rule 612 confirms minimum pricing increments (generally $0.01 for stocks priced at $1 or more), limiting sub-penny stepping ahead. [sec](https://www.sec.gov/spotlight/emsac/memo-rule-611-regulation-nms.pdf)

**Quant dev translation:** tick constraints shape queue competition, quote placement logic, and fill probability modeling; in many names, “outbidding by $0.0001” simply isn’t permitted, so speed/priority dominate. [sec](https://www.sec.gov/spotlight/emsac/memo-rule-611-regulation-nms.pdf)

***

## 3. Regulation SHO (short selling)
Reg SHO is the SEC’s short sale regulation framework with four “general requirements” commonly summarized as marking (Rule 200), circuit breaker (Rule 201), locate (Rule 203), and close-out (Rule 204). [sec](https://www.sec.gov/investor/pubs/regsho.htm)

### 3.1 Rule 200: marking
Rule 200 requires that orders placed with a broker-dealer be marked “long,” “short,” or “short exempt.” [sec](https://www.sec.gov/investor/pubs/regsho.htm)

**Quant dev translation:** order creation must be coupled to a position/ownership state machine so that retries, child-orders, and partial fills don’t produce inconsistent marks. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

### 3.2 Rule 201: short sale price test circuit breaker
Rule 201 generally requires trading centers to have written policies reasonably designed to prevent execution or display of a short sale at an impermissible price when a stock triggers the circuit breaker by declining at least 10% in one day. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

Once triggered, the price test restriction applies for the remainder of that day and the following day (unless an exception applies). [sec](https://www.sec.gov/investor/pubs/regsho.htm)

**Quant dev translation:** implement a per-symbol Rule-201 state machine (trigger, active window, permitted pricing behavior) and wire it into both quoting and routing. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

### 3.3 Rule 203: locate requirement (pre-trade)
Reg SHO requires a broker-dealer to have reasonable grounds to believe the security can be borrowed and delivered on the delivery date before effecting a short sale in an equity security (locate requirement). [sec](https://www.sec.gov/investor/pubs/regsho.htm)

**Quant dev translation:** you need a locate service (satisfy/deny/partial/expire), a locate cache with utilization accounting, and a hard pre-trade gate that blocks or resizes short orders without a valid locate (unless a narrow exception is applicable in your context). [sec](https://www.sec.gov/investor/pubs/regsho.htm)

### 3.4 Rule 204: close-out requirement (post-trade / settlement)
Rule 204 requires clearing/settling firms to deliver securities by settlement date or to close out failures to deliver by borrowing or purchasing like-kind and quantity by specified deadlines (with timing depending on whether the fail is tied to short or long sales, and including bona fide market making fails in the SEC’s summary). [sec](https://www.sec.gov/investor/pubs/regsho.htm)

**Quant dev translation:** “settlement is part of trading.” Build FTD monitors, escalation, and enforcement hooks because chronic fails can force operational constraints (e.g., effective pre-borrow regimes) that feed back into your strategy capacity. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

### 3.5 SRO conflicts / primacy note (useful in interviews)
SEC staff guidance notes that Reg SHO supplants conflicting SRO short sale rules and that Rule 201(e) prohibits an SRO from having a rule that conflicts with the SEC’s circuit breaker rule. [sec](https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions-8)

**Quant dev translation:** your compliance logic should be anchored in Reg SHO + applicable venue rules that are consistent with it; don’t assume an exchange-specific doc can override Reg SHO mechanics. [sec](https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions-8)

***

## 4. Turning regs into system requirements
This is the “quant dev” heart of the document: implement compliance as explicit services + pre-trade/post-trade gates.

### 4.1 Reference architecture (minimum viable)
- **Market data layer**: direct feeds + consolidated, normalized book, timestamps, staleness flags.  
- **Quote engine**: fair value, spread model, inventory skew, throttles.  
- **SOR / OMS**: child order slicing, venue selection, cancel/replace, self-trade prevention.  
- **Reg NMS compliance**: protected-quote view + trade-through guard + exception workflows (including ISO logic where relevant). [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- **Reg SHO compliance**: marking engine (Rule 200), locate service (Rule 203), Rule-201 state machine, FTD/close-out monitor (Rule 204). [sec](https://www.sec.gov/investor/pubs/regsho.htm)

### 4.2 Runtime compliance gates (what must happen before sending an order)
**Gate A — Marking (Rule 200):** assign long/short/short-exempt based on ownership/position state and current exemptions. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

**Gate B — Locate (Rule 203):** if short, require a valid locate approval (qty + expiry + documentation) before “effecting” the short sale. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

**Gate C — Circuit breaker (Rule 201):** if active, block/adjust impermissible short sale pricing for execution/display according to your implementation scope. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

**Gate D — Trade-through prevention (Rule 611):** verify intended execution won’t trade through a protected quote unless a documented exception workflow is used (including ISO compliance responsibilities where applicable). [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

**Gate E — Settlement/FTD constraints (Rule 204):** integrate FTD/close-out state to tighten short permissions and operational capacity when needed. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

### 4.3 Audit log schema (what you must be able to replay)
Log every order decision with:
- `symbol, side, qty, limit_px, venue, tif, order_type`
- `marking` (long/short/short_exempt) and the state inputs that produced it. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- `locate_id, approved_qty, expiry_ts, utilized_qty` (if short). [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- `rule201_active, trigger_ts, restriction_window_end` (if applicable). [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- `protected_quote_snapshot`: best protected bid/ask, venues, timestamps, and the result of the trade-through guard; if exception used, store exception code and supporting fields. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- `result`: ack/reject/partial/fill/cancel + timestamps.

Interview payoff: you can explain “how we prove we complied” under asynchronous feeds and bursty traffic. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

***

## 5. Interview readiness checklist
### Reg NMS
- Explain Rule 611 requirement: written policies to prevent trade-throughs + surveillance + remediation. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- Name and describe at least two Rule 611 exceptions and when you’d rely on them. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- Describe ISO responsibilities at a high level and how a sweep plan avoids trade-through risk. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- Explain Rule 610’s access fee and fair access concept and how it affects routing economics. [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)

### Reg SHO
- Define and apply marking: long vs short vs short exempt in system terms. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- Explain locate: “reasonable grounds to believe can borrow and deliver” and why it must be pre-trade documented. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- Explain Rule 201 trigger (≥10% down day) and duration (rest of day + next day). [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- Explain Rule 204: what an FTD is, why close-out deadlines matter to capacity, and how your system detects and reacts. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- Mention Reg SHO primacy over conflicting SRO rules (especially around Rule 201). [sec](https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions-8)

***

## 6. Practical build exercises
1. **Protected quote view + staleness**
- Build a module that consumes top-of-book per venue and outputs best protected bid/ask with staleness scoring.

2. **Trade-through guard**
- Implement `would_trade_through(order, protected_quote_view) -> bool` and a policy handler: block, reroute, or exception workflow. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

3. **Locate service simulation**
- Implement locate request/approve/expire/utilize logic with partial approvals. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

4. **Rule 201 state machine**
- Feed synthetic prices; verify trigger at 10% down and enforce restriction window. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

5. **FTD monitor skeleton**
- Simulate settlement statuses, create alerts, and tighten short permissions when close-out risk rises. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

***

## 7. Glossary
- **Protected quotation**: quote protected under Rule 611 conditions; the target of trade-through prevention. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- **Trade-through**: execution at a price worse than a protected quote (per rule definition). [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- **ISO**: order type/workflow tied to Rule 611’s intermarket sweep concept; routing party has responsibilities to ensure compliance with requirements. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- **Locate**: pre-trade determination (documented) that shares can be borrowed for delivery. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- **FTD (failure to deliver)**: settlement failure requiring close-out actions per Rule 204 timelines. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- **Rule 201 circuit breaker**: 10% down trigger that activates short sale price-test restrictions for remainder of day + next day. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

***

## 8. Source anchors
- SEC — Key Points About Regulation SHO (Rules 200, 201, 203, 204 summary; timing; close-out description). [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- 17 CFR § 242.611 — Rule 611 text (policies/procedures, surveillance, exceptions, ISO responsibility). [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- SEC PDF — Rule 611 memo (overview of Reg NMS key rules; Rules 603/610/611/612). [sec](https://www.sec.gov/spotlight/emsac/memo-rule-611-regulation-nms.pdf)
- SEC PDF — Rule 611 / Rule 610 FAQ (overview; describes 610 fair access/fee limit and 611 trade-through prevention). [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)
- SEC Staff guidance/FAQ — notes on Reg SHO and SRO conformity (Rule 201(e) prohibition on conflicting SRO rules). [sec](https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions-8)


***