---
type: concept
title: "Order Flow Microstructure, Footprint Charts, and Tape Reading"
track: [quant-trader, quant-research]
tier: advanced
status: solid
est_hours: 1.5
tags: [technical-analysis, order-flow, tape-reading, footprint-charts, cvd, cumulative-delta, absorption, microstructure]
prereqs: []
---

# Order Flow Microstructure, Footprint Charts, and Tape Reading

While classical technical analysis interprets processed OHLC bar charts after the close of an interval, order flow analysis inspects the raw, tick-level engine of price discovery: the continuous interaction between resting limit orders and aggressive market orders inside the Limit Order Book (LOB).
Originating from the physical trading pits where floor specialists read the "tape" of executed trades, modern order flow tools - such as Time and Sales feeds, Bid-Ask Footprint charts, and Cumulative Volume Delta (CVD) - quantify buying and selling aggression in real time.
This note formalizes trade classification, works through footprint and absorption arithmetic, and separates what the microstructure literature has established (order flow moves prices over very short horizons) from chart-reading patterns that have no published test.

---

## TL;DR

Every transaction requires a match between a passive resting limit order (liquidity provider) and an aggressive market order (liquidity taker).
The Lee-Ready (1991) trade classification algorithm attributes transactions as buyer-initiated or seller-initiated based on quotes and tick direction.
Footprint charts disaggregate candlestick bars into a bid-ask matrix, displaying traded volume at every price tier within the bar.
Cumulative Volume Delta (CVD) tracks the cumulative sum of aggressive market buying minus market selling:
$$\text{CVD}_t = \sum_{i=1}^t (V_i^{\text{buy}} - V_i^{\text{sell}})$$
Tape readers interpret a new price high with falling CVD as buying exhaustion and passive absorption; no study cited here tests that pattern as a predictor, so treat it as a hypothesis.

---

## Learning objectives

- Formulate the Lee-Ready (1991) tick rule and quote rule for trade direction classification.
- Deconstruct Bid-Ask Footprint charts: volume clusters, bar delta, delta finish, and trapped trader footprints.
- Calculate and interpret Cumulative Volume Delta (CVD) and identify institutional absorption divergences.
- Model the execution mechanics of iceberg orders, spoofing, and queue priority manipulation.
- Analyze what the microstructure literature (Hasbrouck 1991, Cont, Kukanov and Stoikov 2014, O'Hara 2015) does and does not show about order flow and prices.

---

## Core concepts

### 1. The Mechanics of the Limit Order Book (LOB)

The Limit Order Book organizes resting limit orders in price-time priority:
- **Resting Limit Orders (Passive Liquidity)**: Traders place bids below the current price and asks above.
  They commit capital, face adverse selection risk, and earn or pay exchange maker fees/rebates.
- **Market Orders (Aggressive Liquidity)**: Traders execute immediately at the best available quote, paying the bid-ask spread and taker fees.
- **How the best quotes move**:
  Every trade has exactly one buyer and one seller, so "more buyers than sellers" is not the mechanism.
  The best bid or ask moves when a queue is emptied (by market orders or by cancellations) or when a new limit order improves the price inside the spread.
  Cont, Kukanov and Stoikov (2014) show that order flow imbalance, which nets limit orders, cancellations and market orders at the best quotes, explains short-interval price changes better than trade imbalance alone.

```
+---------------------------------------------------------------------------------+
|                       LIMIT ORDER BOOK (LOB) DEPTH & MATCHING                   |
+---------------------------------------------------------------------------------+
|   ASK DEPTH (Limit Sells)                                                       |
|   100.03 | [ 250 contracts ]                                                    |
|   100.02 | [ 180 contracts ]                                                    |
|   100.01 | [  90 contracts ] <--- Best Ask                                      |
|  --------|------------------                                                    |
|   SPREAD = $0.02                                                                |
|  --------|------------------                                                    |
|    99.99 | [ 120 contracts ] <--- Best Bid                                      |
|    99.98 | [ 210 contracts ]                                                    |
|    99.97 | [ 340 contracts ]                                                    |
|   BID DEPTH (Limit Buys)                                                        |
+---------------------------------------------------------------------------------+
|  Incoming Order: Aggressive Market Buy for 150 contracts                        |
|  Execution: Consumes all 90 @ 100.01 + 60 @ 100.02                              |
|  Outcome: Best Ask moves to 100.02 (120 left); last trade 100.02; avg 100.014   |
+---------------------------------------------------------------------------------+
```

### 2. Trade Classification: The Lee-Ready (1991) Algorithm

Tick-level market data feeds report trade price $P_t$, size $V_t$, and timestamp, but historically did not disclose whether the trade was buyer-initiated or seller-initiated.
Charles Lee and Mark Ready (1991) formulated the standard algorithm to classify trade direction; for the 1988 NYSE data they studied they also recommended comparing each trade with the quote in force at least five seconds earlier, because quotes were often recorded ahead of the trades that caused them:

1. **The Quote Rule**:
   - Compare trade price $P_t$ to the prevailing National Best Bid and Offer (NBBO) midpoint $M_t = \frac{\text{Bid}_t + \text{Ask}_t}{2}$:
     $$\text{Direction}_t = \begin{cases} +1\text{ (Buyer-Initiated)} & \text{if } P_t > M_t \\ -1\text{ (Seller-Initiated)} & \text{if } P_t < M_t \end{cases}$$

2. **The Tick Rule (Fallback)**:
   - If the trade executes exactly at the midpoint ($P_t = M_t$):
     $$\text{Direction}_t = \begin{cases} +1 & \text{if } P_t > P_{t-1}\text{ (Uptick)} \\ -1 & \text{if } P_t < P_{t-1}\text{ (Downtick)} \\ \text{sign}(P_t - P_{t-k}) & \text{if } P_t = P_{t-1}\text{ (Zero-Tick)} \end{cases}$$
   - For a zero tick, $P_{t-k}$ is the most recent trade at a different price: a zero-uptick is a buy and a zero-downtick a sell.
     This looks back at price changes, not at the previous trade's classification.

### 3. Footprint Charts and Volume Delta

Footprint charts (also known as Cluster Charts) open up the interior of a candlestick bar, displaying traded volume partitioned into aggressive buying and selling across every price tick:

```
+---------------------------------------------------------------------------------+
|                       BID-ASK FOOTPRINT BAR ARCHITECTURE                        |
+---------------------------------------------------------------------------------+
|  Price  |  Bid Vol  x  Ask Vol  |  Delta  |  Interpretation                     |
|  100.05 |       12  x      140  |   +128  |                                     |
|  100.04 |       45  x      520  |   +475  |  <--- Imbalance (Buying Aggression) |
|  100.03 |      110  x      680  |   +570  |  <--- Bar POC (Highest Traded Size) |
|  100.02 |      250  x      310  |    +60  |                                     |
|  100.01 |      480  x       95  |   -385  |                                     |
|  100.00 |      650  x       20  |   -630  |  <--- Heavy Selling at the Low      |
+---------------------------------------------------------------------------------+
|  Bar Summary: Total Volume = 3,312 | Bar Delta = +218 | Delta % = +6.58%        |
+---------------------------------------------------------------------------------+
```

1. **Diagonal Matching**:
   - Inside the footprint, buyers hitting the ask at price $P$ are paired diagonally against sellers hitting the bid at price $P - \text{tick}$:
     $$\text{Bid Volume}(P - \text{tick}) \quad \times \quad \text{Ask Volume}(P)$$

2. **Order Flow Imbalances**:
   - An imbalance occurs when the volume on one side is at least a user-chosen multiple (charting packages often default to 3 or 4 times) of the opposing diagonal volume.
   - In the bar above, the 3:1 buying imbalances are at 100.05 ($140 / 45 = 3.11$) and 100.04 ($520 / 110 = 4.73$), but not at 100.03 ($680 / 250 = 2.72$); the 3:1 selling imbalance is at 100.00 ($650 / 95 = 6.84$).
   - "Stacked" imbalances (three or more consecutive levels) are read by practitioners as initiative buying or selling; that reading has no published test, and this bar has only two consecutive buying levels.

3. **Cumulative Volume Delta (CVD)**:
   - Evaluates the running net aggression across the session:
     $$\Delta_t = V_t^{\text{ask}} - V_t^{\text{bid}}$$
     $$\text{CVD}_t = \text{CVD}_{t-1} + \Delta_t$$

### 4. Institutional Absorption and Trapped Traders

Absorption is the tape-reading name for heavy aggressive volume that fails to move price because resting (often hidden) depth keeps refilling; the scenario below is hypothetical:

1. **Passive Absorption at Resistance**:
   - A stock rallies to resistance at $\$150.00$.
   - Aggressive market buyers purchase $500,000$ shares at the ask ($\Delta \gg 0$).
   - Despite this enormous buying volume, price fails to tick higher because an institutional iceberg limit sell order absorbs every share.
   - The footprint prints massive ask volume and positive delta, but the price bar closes off its highs with an upper wick.
   - The tape-reading interpretation is that once aggressive buying stops, nothing is left to hold price up; that is a story, not a measured effect.

2. **Trapped Traders**:
   - In the scenario above, aggressive buyers who bought at $\$150.00$ are now underwater as price drops to $\$149.20$.
   - If these "trapped buyers" stop out with market orders, their selling adds to the decline; whether it does depends on where their stops sit, which the tape does not reveal.

### 5. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                       EVIDENCE LEDGER: ORDER FLOW & MICROSTRUCTURE              |
+---------------------------------------------------------------------------------+
|  Phenomenon: Order flow, trade classification and short-horizon price impact    |
|  Evidence: strong for contemporaneous and very short-horizon price impact;      |
|  none cited here for footprint, CVD-divergence or trapped-trader setups.        |
+---------------------------------------------------------------------------------+
|  Key Empirical Studies:                                                         |
|  1. Lee and Ready (1991, Journal of Finance): quote rule, tick-rule fallback    |
|     and the five-second quote lag. Odders-White (2000, Journal of Financial     |
|     Markets) found it classified about 85% of NYSE (TORQ) trades correctly,     |
|     with errors concentrated in small trades and midpoint trades.               |
|  2. Hasbrouck (1991, Journal of Finance):                                       |
|     - A vector autoregression of trades and quote revisions shows that trade    |
|       innovations have a persistent price impact, read as private information.  |
|  3. Cont, Stoikov, and Talreja (2010, Operations Research):                     |
|     - A continuous-time queueing model with Poisson order arrivals.             |
|     Cont, Kukanov, and Stoikov (2014, Journal of Financial Econometrics):       |
|     - Order flow imbalance at the best quotes has an approximately linear       |
|       relation with contemporaneous short-interval price changes in US          |
|       equities, with a slope inversely related to market depth.                 |
|  4. Cartea, Jaimungal, and Penalva (2015, Algorithmic and High-Frequency        |
|     Trading): a textbook treatment of market making and execution models        |
|     that use order flow signals; it is not an empirical validation study.       |
+---------------------------------------------------------------------------------+
|  Counter-Evidence & Real-World Frictions:                                       |
|  1. Dark Pools and Internalization:                                             |
|     - A large and time-varying share of US equity volume executes off-exchange  |
|       (ATSs and wholesalers) and prints to a FINRA Trade Reporting Facility.    |
|  2. Latency Arbitrage and Spoofing:                                             |
|     - High-Frequency Trading (HFT) co-located algorithms cancel and replace     |
|       resting orders faster than a human can react, so displayed depth is       |
|       not a reliable promise of liquidity.                                      |
+---------------------------------------------------------------------------------+
```

---

## Worked examples

### Example 1: Applying the Lee-Ready Trade Classification Algorithm

An equity execution algorithm processes four sequential transactions on an exchange:
- NBBO Quote at $t_0$: $\text{Bid} = \$50.00$, $\text{Ask} = \$50.04$ (Midpoint $M = \$50.02$).
- Trade 1: $P_1 = \$50.04$, Size $= 500\text{ shares}$.
- Trade 2: $P_2 = \$50.00$, Size $= 1,200\text{ shares}$.
- Trade 3: $P_3 = \$50.02$, Size $= 300\text{ shares}$ (Prior trade $P_2 = \$50.00$).
- Trade 4: $P_4 = \$50.02$, Size $= 400\text{ shares}$ (Prior trade $P_3 = \$50.02$).

1. **Classify Trade 1**:
   $$P_1 = \$50.04 > M = \$50.02 \implies \text{Buyer-Initiated (+1)}$$
   $$\text{Delta Contribution} = +500\text{ shares}$$

2. **Classify Trade 2**:
   $$P_2 = \$50.00 < M = \$50.02 \implies \text{Seller-Initiated (-1)}$$
   $$\text{Delta Contribution} = -1,200\text{ shares}$$

3. **Classify Trade 3**:
   $$P_3 = \$50.02 = M = \$50.02 \implies \text{Midpoint Trade, apply Tick Rule}$$
   $$P_3 = \$50.02 > P_2 = \$50.00\text{ (Uptick)} \implies \text{Buyer-Initiated (+1)}$$
   $$\text{Delta Contribution} = +300\text{ shares}$$

4. **Classify Trade 4**:
   $$P_4 = \$50.02 = M = \$50.02 \implies \text{Midpoint Trade, apply Tick Rule}$$
   $$P_4 = P_3\text{ (Zero-Tick)}, \quad P_4 > \$50.00\text{ (last different price)} \implies \text{Zero-Uptick, Buyer-Initiated (+1)}$$
   $$\text{Delta Contribution} = +400\text{ shares}$$

5. **Compute Total Net Bar Delta**:
   $$\Delta_{\text{net}} = +500 - 1200 + 300 + 400 = 0\text{ shares}$$
   The net delta across the four trades is exactly zero.

### Example 2: Reading Absorption at a Prior High (hypothetical)

A tape reader monitors a futures contract testing the previous day's high of $4,500.00$ (all prices and volumes are hypothetical):
- **Wave 1 (Initial Test)**:
  - Price reaches $4,500.00$.
  - Cumulative Delta over Wave 1: $\text{CVD} = +5,000\text{ contracts}$.
  - Price pulls back to $4,492.00$.
- **Wave 2 (Secondary Test)**:
  - Price pushes higher to $4,503.00$ (New Price High, $+3.00$ points).
  - Cumulative Delta over Wave 2 surges by an additional $+12,000$ contracts ($\text{CVD} = +17,000$).
  - Despite $+12,000$ contracts of aggressive market buying, price advances by only $3.00$ points and closes back at $4,498.00$.

1. **Evaluate Order Flow Dynamics**:
   - Aggressive market buyers added $17,000 - 5,000 = 12,000$ contracts of net buying.
   - Price made a new high by only $4,503 - 4,500 = 3$ points and closed back below the breakout level.
   - Every aggressive buy was, by definition, filled by a passive seller; what the reader infers is that resting sell depth kept refilling.
   - Note that CVD made a higher high with price, so this is absorption (large delta per point gained), not the CVD divergence defined above.

2. **Strategic Trade Plan**:
   - **Diagnosis**: bearish absorption, an untested discretionary hypothesis.
   - Enter Short at $4,497.00$.
   - Stop Loss: $4,504.00$ (above the trapped buyer high, Risk $= 7.00$ points).
   - Target: Rotation down to a prior volume point of control at $4,475.00$ (Reward $= 22.00$ points).
   - Reward-to-risk ratio: $\frac{22.00}{7.00} = 3.14$, so the trade needs a hit rate above $7 / 29 = 24.1\%$ to break even before costs.

---

## Pitfalls

- **The Level 2 Phantom Liquidity Illusion (Spoofing)**:
  Displayed depth on Level 2 screens can be cancelled at any moment, and spoofing (orders entered with the intent to cancel before execution) is designed to mislead.
  Large resting bids can disappear just before a trade executes, leaving the trader without the liquidity they saw.
- **Ignoring Hidden Iceberg Orders**:
  A hypothetical institutional order for $100,000$ shares may display only $500$ shares on the order book at any given time.
  Looking only at displayed size fails to reveal the true magnitude of resting institutional absorption.
- **Off-Exchange Dark Pool Blind Spots**:
  In US equities, institutional block trades execute in Alternative Trading Systems (ATS) and print to the Trade Reporting Facility (TRF) with delays.
  Order flow delta captured strictly on lit exchange feeds misses off-exchange block crosses.
- **Latency Disadvantage Against Co-Located Algorithms**:
  Retail order flow feeds travel over the public internet and through vendor servers, while co-located firms receive direct exchange feeds inside the data centre.
  By the time a retail screen updates, faster participants have already seen and reacted to the same events.

---

## Interview questions

> [!question]- mkt-ta-161 | What is the fundamental difference between a passive limit order and an aggressive market order?
> A passive limit order provides liquidity, resting in the book at a specified price and waiting to be matched.
> An aggressive market order takes liquidity, demanding immediate execution at the current best available price and driving price movement.

> [!question]- mkt-ta-162 | Why does price move in continuous double auction markets?
> The best bid or ask moves when its queue is emptied, by market orders or by cancellations, or when a new limit order improves the price inside the spread.
> Cont, Kukanov and Stoikov (2014) show that order flow imbalance at the best quotes, netting all three event types, explains short-interval price changes.

> [!question]- mkt-ta-163 | State the Lee-Ready (1991) trade classification algorithm.
> If trade price is above the NBBO midpoint, it is classified as buyer-initiated; if below, seller-initiated.
> If executed at the midpoint, the tick rule applies: an uptick is buyer-initiated, a downtick is seller-initiated, and a zero tick takes the sign of the last price change (zero-uptick buy, zero-downtick sell).

> [!question]- mkt-ta-164 | What is a Footprint (Cluster) chart?
> A candlestick chart that displays the internal executed volume at each price tick within the bar.
> It breaks down trading into bid volume (selling aggression) and ask volume (buying aggression).

> [!question]- mkt-ta-165 | How are trades matched diagonally in a bid-ask footprint chart?
> Buyers paying the ask at price P are matched diagonally against sellers hitting the bid at price P - 1 tick.
> This reflects the two-sided nature of market orders crossing the spread against opposing resting quotes.

> [!question]- mkt-ta-166 | What is an order flow imbalance in footprint charting?
> A condition where traded volume on one side is at least a user-chosen multiple (charting defaults are often 3 or 4) of the opposing diagonal volume.
> It highlights where aggressive buying or selling concentrated inside the bar; it is a description, not a tested signal.

> [!question]- mkt-ta-167 | What is Cumulative Volume Delta (CVD)?
> The running cumulative sum of aggressive market buying volume minus aggressive market selling volume across a session: CVD_t = sum(V_buy - V_sell).
> It quantifies net directional aggression in the market.

> [!question]- mkt-ta-168 | What is a CVD absorption divergence?
> When price makes a higher high but CVD fails to make a higher high (or vice versa).
> Tape readers read it as waning aggressive buying against passive absorption; no study cited here tests it as a reversal predictor.

> [!question]- mkt-ta-169 | What is institutional absorption in order flow analysis?
> When a large participant places large resting limit orders (often as an iceberg) that absorb aggressive market orders without allowing price to move through the level.
> High volume prints at the level without price advancement.

> [!question]- mkt-ta-170 | What are trapped buyers in market microstructure?
> Aggressive buyers who bought at or near the top of a move, into resting limit sell orders whose owners the tape does not identify.
> If they exit with stop-market orders, that selling can add to the drop; whether it does depends on where their stops sit, and no study cited here measures it.

> [!question]- mkt-ta-171 | What is an iceberg order?
> A large limit order that displays only a small fraction of its total quantity in the public order book (e.g. displaying 100 shares out of a 50,000 share order).
> As each visible slice is filled, the exchange automatically refreshes the displayed quantity until the full parent order is complete.

> [!question]- mkt-ta-172 | What is spoofing in financial markets and is it legal?
> The illegal practice of submitting large non-bona fide resting limit orders with the intention of canceling them before execution.
> Dodd-Frank (2010) section 747 added Commodity Exchange Act section 4c(a)(5)(C), which makes spoofing (bidding or offering with the intent to cancel before execution) unlawful on CFTC-registered markets; in securities markets it is prosecuted as manipulation and fraud.

> [!question]- mkt-ta-173 | What is layering in order book manipulation?
> Submitting multiple fake limit orders at progressive price increments on one side of the book to simulate heavy supply or demand, while executing a real order on the opposite side.
> Once filled, the layered orders are instantly cancelled.

> [!question]- mkt-ta-174 | What did Hasbrouck (1991) demonstrate regarding order flow impact using Vector Autoregressions (VAR)?
> That trade innovations have a persistent impact on quote midpoints in a VAR of trades and quote revisions, larger for smaller firms.
> The persistent impact is interpreted as the private information carried by trades.

> [!question]- mkt-ta-175 | What is Order Flow Imbalance (OFI) as defined by Cont, Kukanov, and Stoikov (2014)?
> A quantitative metric measuring the net change in order book depth: changes in limit order arrivals, cancellations, and market order executions across the best bid and ask.
> OFI has an approximately linear contemporaneous relationship with short-interval price changes, with a slope inversely related to market depth.

> [!question]- mkt-ta-176 | What is Delta Finish (Delta at the extremes) in a footprint bar?
> A vendor-defined reading of the delta printed at a bar's extreme price ticks; definitions differ between charting packages.
> Tape readers read a large negative delta at the low of a bar that closes higher as sellers absorbed by passive bids; that interpretation is untested.

> [!question]- mkt-ta-177 | What is the Bar Point of Control (Bar POC)?
> The specific price tick within an individual footprint bar where the highest total volume was transacted.
> Practitioners watch it as a reference price on later rotations; no published test of it as support or resistance is cited here.

> [!question]- mkt-ta-178 | What is stacked imbalance in footprint analysis?
> Three or more consecutive price levels that all display buying (or all selling) diagonal imbalances.
> Practitioners read them as initiative activity and later support or resistance; that reading has no published test.

> [!question]- mkt-ta-179 | What is exhaustion volume in tape reading?
> A surge in aggressive volume after an extended move, read by tape readers as late buyers meeting large sellers.
> It is identified only in hindsight; no study cited here shows that it marks the end of a move.

> [!question]- mkt-ta-180 | What is market depth (Level 2) and what is its primary limitation for retail traders?
> Level 2 displays the aggregate resting limit order quantity at each price tier across participating exchanges.
> Its primary limitation is that it only shows visible liquidity, hiding dark pools, iceberg orders, and ephemeral HFT quotes.

> [!question]- mkt-ta-181 | What is a sweep order (intermarket sweep order, ISO)?
> A limit order marked as an ISO under Regulation NMS (Rule 600(b) definition); the sender simultaneously routes orders to take out better-priced protected quotes elsewhere, which exempts it from the Rule 611 order protection requirement.
> ISOs let a trader take liquidity at several venues and price levels at once, so they often signal urgency.

> [!question]- mkt-ta-182 | How does dark pool trading affect order flow signals on lit exchanges?
> A large, time-varying share of US equity volume executes off-exchange (ATSs and wholesalers) without pre-trade transparency and prints to a FINRA Trade Reporting Facility.
> Those prints carry no aggressor flag and are reported after execution, so lit-exchange order flow delta is an incomplete picture of total volume.

> [!question]- mkt-ta-183 | What is queue priority in limit order book matching?
> The order execution sequence governed by price-time priority: orders at the best price execute first, and among equal prices, the earliest submitted order fills first.
> Quantitative market makers optimize queue position to capture spread rebates while avoiding adverse selection.

> [!question]- mkt-ta-184 | What is adverse selection risk for a passive limit order trader?
> The risk that a limit order is filled primarily when an informed counterparty possesses superior information, causing the price to move through the order immediately after execution.
> Passive market makers suffer losses when filled by toxic, informed flow.

> [!question]- mkt-ta-185 | What is toxic order flow?
> Aggressive market flow originating from informed traders who possess predictive directional alpha.
> Toxic flow generates heavy adverse selection for market makers, forcing them to widen bid-ask spreads.

> [!question]- mkt-ta-186 | What is the VPIN metric (Volume-Synchronized Probability of Toxicity)?
> A market microstructure metric developed by Easley, López de Prado, and O'Hara (2012) that measures order toxicity based on volume imbalances in equal-volume buckets.
> The authors proposed it as an early-warning indicator of toxicity before the 6 May 2010 flash crash; Andersen and Bondarenko (2014) dispute its predictive power, so treat it as contested.

> [!question]- mkt-ta-187 | How does tape reading detect an institutional iceberg order?
> By observing continuous large volume transactions printing at the ask (or bid) on the Time and Sales feed while the displayed order size on Level 2 never decreases.
> Constant replenishment of displayed size is consistent with a hidden iceberg order, though a series of new limit orders at the same price looks the same on public data.

> [!question]- mkt-ta-188 | What is an unfinished business (unmatched auction) in footprint charts?
> A footprint term for a bar extreme that traded on both the bid and the ask, rather than one side going to zero.
> Practitioners say price tends to revisit such levels; no published probability for that claim is cited here, so treat it as untested.

> [!question]- mkt-ta-189 | What is liquidity replenishment in order book dynamics?
> The speed at which market makers post fresh limit orders after an aggressive trade sweeps a price tier.
> Fast replenishment indicates robust market depth; slow replenishment indicates thin liquidity and high fragility.

> [!question]- mkt-ta-190 | What is slippage in order flow execution?
> The difference between the expected transaction price when a market order is submitted and the actual price at which the trade executes.
> Slippage increases non-linearly with order size relative to available top-of-book depth.

> [!question]- mkt-ta-191 | What is market on close (MOC) imbalance and how does it relate to tape reading?
> Exchange-published closing-auction data (for example the NYSE closing imbalance feed and the Nasdaq Net Order Imbalance Indicator) showing unmatched buy or sell interest for the closing cross.
> Large imbalances invite offsetting orders into the close; their effect on price is an empirical question, not a rule.

> [!question]- mkt-ta-192 | Why is order flow analysis more effective on centralized futures exchanges (CME) than fragmented equity markets?
> Each futures contract trades on one exchange's central limit order book, so there is no fragmentation across venues or wholesalers.
> The main exceptions are privately negotiated block trades (CME Rule 526) and EFRPs (CME Rule 538), which are reported after execution; market-by-order data show every order event in the book.

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_ta_06_order_flow.py`](../../code/mkt_ta_06_order_flow.py) prints and asserts every number on this page: the sweep by a price-time matching routine on the ask ladder, the footprint bar's totals, delta, delta percent, point of control and diagonal ratios in exact integer arithmetic from the bid x ask table, the Lee-Ready example with a tick rule that looks back to the last different price, and the absorption trade's risk and reward as exact fractions with its break-even hit rate by bisection on the expectancy.
- Related notes: [Auction Theory, Volume Profile and VWAP](03-Auction-Theory-Volume-Profile-and-VWAP.md).

---

## Further reading

- Lee, C. M., & Ready, M. J. (1991). *Inferring trade direction from intraday data*. The Journal of Finance, 46(2), 733-746.
- Hasbrouck, J. (1991). *Measuring the information content of stock trades*. The Journal of Finance, 46(1), 179-207.
- Cont, R., Stoikov, S., & Talreja, R. (2010). *A stochastic model for order book dynamics*. Operations Research, 58(3), 549-563.
- Cont, R., Kukanov, A., & Stoikov, S. (2014). *The price impact of order book events*. Journal of Financial Econometrics, 12(1), 47-88.
- Easley, D., López de Prado, M. M., & O'Hara, M. (2012). *Flow toxicity and liquidity in a high-frequency world*. The Review of Financial Studies, 25(5), 1457-1493.
- Andersen, T. G., & Bondarenko, O. (2014). *VPIN and the flash crash*. Journal of Financial Markets, 17, 1-46.
- Odders-White, E. R. (2000). *On the occurrence and consequences of inaccurate trade classification*. Journal of Financial Markets, 3(3), 259-286.
- Cartea, Á., Jaimungal, S., & Penalva, J. (2015). *Algorithmic and High-Frequency Trading*. Cambridge University Press.
- O'Hara, M. (2015). *High frequency market microstructure*. Journal of Financial Economics, 116(2), 257-270.
