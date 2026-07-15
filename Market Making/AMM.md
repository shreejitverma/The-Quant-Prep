# Market Making Quant Dev (Equities + Options): Reg NMS + Reg SHO + Feeds/Protocols + System Design
*C++ low-latency core + Python analytics. Built to support exchange MM, wholesaler/internalizer, and multi-venue electronic MM.*

## 1) Scope and regulatory requirements
This document translates Regulation NMS (especially Rule 611) and Regulation SHO (Rules 200/201/203/204) into concrete, production-grade engineering requirements and interview-ready explanations. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
It also maps those requirements onto real market data and connectivity patterns used in equities (e.g., ITCH-style depth feeds) and options (OPRA consolidated data + direct exchange feeds). [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)

### Products + venues (what you’re actually trading)
- **Equities:** NMS stocks across multiple exchanges/ATSs; you must avoid trade-throughs of protected quotes unless an exception applies. [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)
- **Options:** Exchange-traded options with consolidated quotes/trades disseminated by OPRA; you’ll typically consume OPRA plus one or more direct options depth feeds for latency/quality. [sec](https://www.sec.gov/rules-regulations/2005/06/regulation-nms)

### The “must know” rule set (quant-dev framing)
- **Reg NMS / Rule 611 (Order Protection):** trading centers must have written policies/procedures reasonably designed to prevent trade-throughs of protected quotations (with enumerated exceptions), and must surveil and remediate. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- **Reg SHO / Rule 200 (Marking):** orders must be marked long/short/short-exempt. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- **Reg SHO / Rule 201 (Circuit breaker):** triggered by a ≥10% down move; trading centers must prevent execution/display of short sales at impermissible prices for the restriction window. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- **Reg SHO / Rule 203 (Locate):** broker-dealers must have reasonable grounds to believe shares can be borrowed/delivered before effecting a short sale, with documentation. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- **Reg SHO / Rule 204 (Close-out):** requires close-out of failures-to-deliver by purchasing/borrowing like-kind and quantity by specified deadlines (and operationally creates “settlement-driven constraints”). [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- **Options nuance (Rule 201 coverage):** practitioner guidance commonly notes Rule 201’s restriction applies to covered equity securities (NMS stocks) and does not cover options. [ccbjournal](https://ccbjournal.com/articles/short-sales-sec-adopts-modified-uptick-rule-subject-circuit-breaker)

### What “ready for market making” means
You are ready when you can:
- Implement pre-trade gates that *cannot* emit non-compliant orders (by construction), with deterministic audit logs. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- Explain how your SOR avoids trade-throughs and when/how an ISO workflow is used (and logged). [sec](https://www.sec.gov/divisions/marketreg/nmsfaq610-11.htm)
- Explain how short selling is controlled end-to-end: marking → locate/circuit-breaker → execution → settlement/FTD monitoring. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

***

## 2) Feeds and protocols (equities + options)
This section pins down the concrete market data and connectivity assumptions you’d use in a real system and what each feed gives you. The goal is to connect “regulation language” to the exact bytes and fields your code consumes. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)

### Equities market data: direct depth feeds
#### Nasdaq TotalView-ITCH (depth + events)
Nasdaq TotalView-ITCH is a direct market data feed describing order lifecycle events (add/modify/delete/execute), trades/crosses, and administrative messages. [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)
The ITCH specification explicitly notes it is **outbound market data only** and that ITCH does not support order entry. [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)

Key implementation details you should bake into your parser/book:
- **Sequenced messages**; instruments identified by a daily “stock locate” code (assigned each day and distributed via Stock Directory). [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)
- Delivery protocols commonly include **SoupBinTCP** and **MoldUDP64** in the spec’s architecture discussion. [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)
- Timestamps are represented as **nanoseconds since midnight** in the ITCH data types section. [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)
- ITCH includes a **Reg SHO Short Sale Price Test Restricted Indicator** message to convey Rule 201 restriction status (with action values described in the spec). [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)

Practical quant-dev takeaways:
- ITCH gives you the raw material to build a full L2/L3 book and microstructure features (queue position, cancels, executions) with tight latency. [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)
- Because ITCH is market-data-only, you still need separate **order entry** connectivity for Nasdaq execution (exchange-specific order entry protocols, FIX/OUCH/others, depending on venue). [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)

#### NYSE Pillar Integrated Feed (depth + last sale + auction/imbalance)
NYSE Pillar Integrated Feed provides real-time market data “in a unified view of events, in sequence, as they appear on the Pillar matching engines,” including depth-of-book order data, last sale data, and opening/closing imbalance data. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)
The spec defines message types such as Add Order (100), Modify (101), Delete (102), Execution (103), Replace (104), Imbalance (105), and others, and includes time reference/symbol mapping control messages. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)

Key microstructure fields worth calling out:
- Execution messages include a `PrintableFlag` and multiple `TradeCond` fields; one of the `TradeCond2` values corresponds to **Intermarket Sweep Order (ISO)** as a reason for trade-through exemptions in the feed’s execution/trade condition encoding. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)
- The Imbalance message includes an `SSRFilingPrice` field for NYSE non-regulatory imbalances “if a Sell Short Restriction is in effect,” tying auction data to SSR context. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)

Practical quant-dev takeaways:
- NYSE Pillar gives you auction/imbalance signals that matter for market making risk (open/close liquidity events) and for explaining unusual prints/volume. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)
- Trade condition fields are useful for *post-trade compliance analytics* (e.g., ISO-related exemptions) even when compliance decisions occur pre-trade. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)

### Options market data: consolidated + direct
#### OPRA (consolidated options SIP)
OPRA disseminates consolidated last sale and quotation information originating from options exchanges approved by the SEC to list and trade exchange-traded options. [sec](https://www.sec.gov/rules-regulations/2005/06/regulation-nms)
OPRA describes itself as a securities information processor (SIP) registered under Exchange Act Section 11A(b) and notes its members are the participant exchanges that act jointly under the OPRA NMS plan. [sec](https://www.sec.gov/rules-regulations/2005/06/regulation-nms)

Practical quant-dev takeaways:
- OPRA is the consolidated “baseline view,” but many market makers also use direct feeds for depth and latency; your analytics stack should reconcile OPRA vs direct for quality and compliance monitoring. [sec](https://www.sec.gov/rules-regulations/2005/06/regulation-nms)
- OPRA rules around vendors/subscribers matter operationally if your org redistributes data internally/externally (contracting, entitlements, audits). [sec](https://www.sec.gov/rules-regulations/2005/06/regulation-nms)

#### Direct options depth feeds (example: Cboe Options Multicast PITCH)
Cboe provides an options multicast depth feed (Multicast PITCH) and distributes daily archives; the product page references a “Cboe Multicast PITCH Specification (U.S. Equities/Options).” [nasdaqtrader](https://www.nasdaqtrader.com/Trader.aspx?id=regsho)
The archive description includes one file per matching engine unit per exchange per trade date, with file naming patterns and notes about RTH/GTH segments. [nasdaqtrader](https://www.nasdaqtrader.com/Trader.aspx?id=regsho)

Practical quant-dev takeaways:
- For options MM, you typically build a per-exchange book from direct feeds and use OPRA for consolidated monitoring and cross-checks. [nasdaqtrader](https://www.nasdaqtrader.com/Trader.aspx?id=regsho)
- Options market data throughput can be extreme; design your parser to be allocation-free with bounded copy and explicit backpressure behavior.

### Connectivity assumptions (order entry)
- **Market data ↔ order entry separation:** ITCH-style feeds are market-data-only, so order entry must use separate exchange order entry protocols/connectivity. [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)
- **Design stance:** implement an order-entry abstraction that can speak multiple venue protocols behind a unified interface (exchange MM + wholesaler + multi-venue router requirements).

***

## 3) C++ low-latency core design (with Python analytics)
This section gives you a production-style architecture: data plane, decision plane, and control plane, with clear invariants and where compliance gates live. The guiding rule is: the system must still be safe when feeds are stale, clocks drift, or one venue is impaired. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

### 3.1 Process layout (recommended)
- **md-gw (market data gateways):** one process per venue/feed group (Nasdaq ITCH, NYSE Pillar, options direct feeds), doing parse → normalize → publish to shared memory or lock-free bus. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)
- **core (pricing/quoting/routing):** consumes normalized books and produces quotes/orders; runs compliance gates inline on the hot path. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- **risk/compliance (nearline):** consumes the same event stream for surveillance, model calibration, and daily controls; can be Python-first.  
- **replay (offline):** deterministic playback of market + internal events to reproduce decisions.

### 3.2 Data model: unified instrument keys
You need a unified identifier across:
- **Equity symbol** (primary listing + venue symbol mapping). [investopedia](https://www.investopedia.com/terms/r/regsho.asp)
- **Option series key** (underlier + expiry + strike + call/put + multiplier).  
- **Cross-asset linkage:** option series → underlying equity for hedging and risk limits.

### 3.3 Core modules (C++ interfaces)
#### Market data normalization
- Normalize into: top-of-book, full depth (if available), trades, auction/imbalance signals (NYSE), and administrative states (halts, SSR indicators, etc.). [investopedia](https://www.investopedia.com/terms/r/regsho.asp)

#### Pricing/quoting engine
- Fair value: mid-based, microprice, inventory-skew models; for options, implied vol surface + Greeks + hedging cost model.
- Quote controls: max update rate, min resting time (where applicable), cancel/replace budgets, and burst protection.

#### Smart Order Router (SOR)
- Objectives: minimize slippage + fees/rebates + risk; maximize fill probability; maintain compliance constraints.
- Tactics: slicing, venue selection, opportunistic internalization (wholesaler mode), ISO sweep workflow where applicable. [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)

***

## 4) Compliance-by-construction (what you implement, not just “know”)
This section is your “production spec”: explicit gates, state machines, and logs that turn Reg NMS + Reg SHO into code. Your interview advantage comes from being able to describe these as invariants and to explain how they behave under latency/staleness. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

### 4.1 Reg NMS: protected quote view + Rule 611 guard
Rule 611 requires written policies/procedures designed to prevent trade-throughs (unless exceptions apply) and requires surveillance and remediation. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
SEC materials emphasize protected quotes must be immediately/automatically accessible and describe ISO as a commonly used exception mechanism. [sec](https://www.sec.gov/divisions/marketreg/nmsfaq610-11.htm)

**Build these components:**

1) **Protected Quote View (PQV)**
- Inputs: per-venue top-of-book + automation/accessibility flags + timestamps.
- Outputs: best protected bid/ask + contributing venues + staleness score.

2) **Rule 611 trade-through guard**
- API: `check_rule611(side, price, venue, pqv, order_type_flags) -> decision`.
- Decisions:
  - Allow
  - Block (would trade-through)
  - Require ISO sweep plan
  - Allow enumerated exception path (systems issue, auction prints, etc.) [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)

3) **ISO sweep planner**
SEC FAQ materials on Rule 611 discuss ISO as a frequent exception and describe the need to route to protected quotations while sweeping. [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)
Your planner should generate a deterministic set of child orders: (a) ISO to target venue(s), (b) ISO(s) to simultaneously execute against better-priced protected quotes.

**Required logs (for surveillance)**
- PQV snapshot used for decision (prices, venues, timestamps).
- Decision + exception code + sweep plan id (if ISO).
- Child order list + expected protected quote sizes cleared.

### 4.2 Reg SHO: marking, locate, Rule 201, and settlement discipline
SEC’s Reg SHO overview lists marking (Rule 200), circuit breaker (Rule 201), locate (Rule 203), and close-out (Rule 204) as core requirements. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

#### Gate A — Rule 200 marking (hot path)
- Every outgoing sell order is marked `long`, `short`, or `short_exempt`. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- Engineering invariant: marking is derived from a single, race-free “position truth” (net position + pending + locate/borrow state), not from scattered caches.

#### Gate B — Rule 203 locate (hot path)
Before effecting a short sale, broker-dealers must have reasonable grounds to believe shares can be borrowed and delivered, with documentation. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
Engineering invariant: `send_short_order()` requires a valid `locate_id` (unless your policy engine flags a permitted market making exception), and the locate consumption is atomic with the order send.

Suggested locate service design:
- `request_locate(sym, qty) -> grant(approved_qty, expiry, locate_id)`
- `consume_locate(locate_id, qty)` (atomic decrement)
- `reclaim_on_cancel(fill_qty)` for accurate utilization

#### Gate C — Rule 201 circuit breaker (hot path)
Rule 201 is triggered by a ≥10% down move and imposes restrictions for the remainder of the day and the next day per the SEC’s summary. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
Engineering invariant: your equity short-sell routing layer consults a `Rule201State` per symbol and blocks/adjusts orders that would be impermissible during the active window. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

**Equities vs options**
- Implement Rule 201 restriction logic for **equities** (covered securities) and treat options as not directly covered by the rule’s price test, consistent with common guidance. [ccbjournal](https://ccbjournal.com/articles/short-sales-sec-adopts-modified-uptick-rule-subject-circuit-breaker)
- Still, connect options quoting/hedging risk limits to the underlying equity’s Rule 201 state to avoid pathological hedge behavior during an SSR regime.

#### Gate D — Rule 204 close-out / FTD controls (post-trade feeds back into pre-trade)
Rule 204 requires close-out of failures to deliver by purchasing/borrowing like-kind and quantity by specified deadlines, per SEC summary. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
Engineering invariant: settlement state is an input to trading capacity—if your clearing reports show elevated fails or approaching deadlines, your system tightens short permissions and may require pre-borrow workflows.

Minimum FTD monitoring features:
- Per symbol: `ftd_qty`, `age`, `next_deadline`, “restriction mode” boolean
- Alerts: age > threshold, repeated fails, spikes after corporate actions
- Automated controls: reduce max short size, widen quotes, throttle aggressive shorts, require manual approval (policy-driven)

### 4.3 Compliance replay (“prove what happened”)
Because Rule 611 requires written procedures, surveillance, and remediation, your system must be replayable and explainable from logs. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
Build a deterministic replay harness that consumes (1) normalized market data events, (2) internal state events, and (3) order acks/fills, and reproduces gate decisions bit-for-bit.

***

## 5) All-in-one build plan + interview drills (equities + options)
This section is the execution plan: what to implement, in what order, and the exact questions you must be able to answer for market making quant dev roles. It’s intentionally “hands-on,” because interviewers probe for real failure modes (stale feeds, partial cancels, broken clocks, exchange outages). [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)

### 5.1 Repo structure (suggested)
```
mm-platform/
  README.md
  docs/
    reg_nms_rule611.md
    reg_sho_200_201_203_204.md
    protocols/
      nasdaq_totalview_itch_notes.md
      nyse_pillar_integrated_notes.md
      opra_notes.md
  cpp/
    md/
      nasdaq_itch_parser/
      nyse_pillar_parser/
      cboe_pitch_parser/
      normalize/
    core/
      books/
      quoting/
      router/
      compliance/
        nms_rule611/
        sho/
      risk/
    infra/
      shm_bus/
      time/
      logging/
  python/
    research/
    surveillance/
    replay_analysis/
```

### 5.2 Milestones (what to build first)
1) **Market data ingestion + book build (equities)**
- Implement ITCH parser + L3 book; confirm correct sequencing and daily locate mapping behavior per ITCH description. [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)
- Implement NYSE Pillar Integrated parser; confirm message set and auction/imbalance flow per client spec. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)

2) **Market data ingestion + book build (options)**
- Implement OPRA top-of-book ingest for consolidated quotes/trades. [sec](https://www.sec.gov/rules-regulations/2005/06/regulation-nms)
- Add one direct options feed (e.g., Cboe options PITCH) for depth/latency and reconcile vs OPRA. [nasdaqtrader](https://www.nasdaqtrader.com/Trader.aspx?id=regsho)

3) **Compliance gates in the hot path**
- Implement Rule 611 PQV + trade-through guard + ISO sweep planner. [sec](https://www.sec.gov/divisions/marketreg/nmsfaq610-11.htm)
- Implement SHO marking + locate + Rule 201 state machine; wire into router/quote engine. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

4) **Settlement feedback loop**
- Implement FTD monitor + capacity controls tied to Rule 204 close-out discipline. [sec](https://www.sec.gov/investor/pubs/regsho.htm)

5) **Replay + surveillance (Python)**
- Build dashboards: trade-through blocks, ISO sweeps, Rule 201 blocks, locate utilization, FTD aging.
- Build deterministic replay analysis that correlates decisions to PQV snapshots and SHO state.

### 5.3 Interview drill set (you must nail these)
**Reg NMS / Rule 611**
- Explain what Rule 611 requires (policies/procedures to prevent trade-throughs, surveillance/remediation) and how your code enforces it. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)
- Explain what makes a quote “protected” and why automation/accessibility matters. [sec](https://www.sec.gov/divisions/marketreg/rule611faq.pdf)
- Explain ISO workflows and what you log to demonstrate you swept better-priced protected quotes. [sec](https://www.sec.gov/divisions/marketreg/nmsfaq610-11.htm)

**Reg SHO**
- Explain marking (Rule 200), locate (Rule 203), Rule 201 trigger/duration, and Rule 204 close-out discipline. [sec](https://www.sec.gov/investor/pubs/regsho.htm)
- Explain how your system prevents race conditions that could mis-mark an order under bursty fills/cancels.

**Feeds/protocols**
- Describe what ITCH messages represent (adds/modifies/deletes/executions) and why ITCH is market-data-only. [dart.deloitte](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/242-regulations-m-sho-ats-ac/242-regulation-nms-regulation-national-market)
- Describe what NYSE Pillar Integrated includes (depth + last sale + imbalance/auction info) and how execution conditions can encode ISO-related exemptions. [investopedia](https://www.investopedia.com/terms/r/regsho.asp)
- Describe OPRA’s role as the consolidated options quote/trade disseminator and why direct feeds are still used. [sec](https://www.sec.gov/rules-regulations/2005/06/regulation-nms)

***

If you want the next iteration to be even closer to a “real firm design doc,” tell me your assumed colocation/latency budget (e.g., Carteret/Secaucus/Mahwah; µs vs low-ms), and whether you want a **single-process lock-free** design or a **multi-process shared-memory** design with restartable gateways. [law.cornell](https://www.law.cornell.edu/cfr/text/17/242.611)