---
type: concept
title: "Auction Market Theory, Volume Profile, and Anchored VWAP"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [technical-analysis, auction-market-theory, volume-profile, market-profile, vwap, anchored-vwap, poc]
prereqs: []
---

# Auction Market Theory, Volume Profile, and Anchored VWAP

Traditional technical analysis focuses almost exclusively on price and time, largely neglecting the critical third dimension of market data: transaction volume.
Developed in the 1980s by J. Peter Steidlmayer, a Chicago Board of Trade (CBOT) floor trader, Auction Market Theory (AMT) and the Market Profile conceptualize financial markets as continuous two-way double auctions whose primary purpose is to facilitate trade between buyers and sellers.
In this framework, price is merely an advertising mechanism, time regulates opportunity, and volume measures market acceptance or rejection.
By mapping volume against price rather than time, Volume Profile and Anchored Volume-Weighted Average Price (AVWAP) show where trading concentrated and the average price paid since a chosen event.

---

## TL;DR

Auction Market Theory models markets as a dual search process for fair value: exploring higher prices until buyers refuse to transact (buying exhaustion) and exploring lower prices until sellers dry up (selling exhaustion).
Market Profile visualizes this distribution via Time Price Opportunities (TPOs), defining the Point of Control (POC, price with maximum time spent) and the Value Area (by convention the range holding $70\%$ of activity, loosely motivated by the $68.27\%$ of a normal distribution within one standard deviation).
Volume Profile measures actual executed shares at price, revealing High Volume Nodes (HVNs, fair-value consolidation zones) and Low Volume Nodes (LVNs, rapid price rejection or liquidity voids).
Volume-Weighted Average Price (VWAP) is a standard benchmark for institutional execution cost (Berkowitz, Logue, and Noser 1988); Anchored VWAP (anchored to swing lows, highs, earnings gaps, or session opens) is used by practitioners as a reference level for support and resistance, a use without peer-reviewed tests cited here.

---

## Learning objectives

- Formulate the core mechanics of Auction Market Theory: Price, Time, and Volume interaction.
- Deconstruct Market Profile architecture: TPOs, Initial Balance, Value Area ($70\%$), and Point of Control.
- Distinguish High Volume Nodes (HVNs) from Low Volume Nodes (LVNs) and model price migration behavior.
- Calculate session VWAP and Anchored VWAP (AVWAP) along with volatility-adjusted standard deviation bands.
- Classify market opening types and profile day structures to anticipate intraday trend versus mean-reversion regimes.

---

## Core concepts

### 1. Principles of Auction Market Theory

Auction Market Theory treats financial markets through the lens of continuous discovery:

1. **The Core Dynamic**:
   - **Price Advertises Opportunity**: Price moves up to discover if buyers are willing to transact at higher levels, and moves down to seek sellers.
   - **Time Regulates Opportunity**: The duration price spends at a particular level indicates market acceptance or rejection.
   - Brief time implies unfair value (rejection); extended time implies consensus (acceptance).
   - **Volume Measures Acceptance**: High volume validates fair value, confirming that two-way trade facilitation is robust.
   - Low volume indicates price rejection and lack of market participant interest.

2. **Responsive vs Initiative Activity**:
   - **Responsive Activity**: Market participants act counter to an extreme move, returning price to perceived fair value.
   - Example: Buying below the Value Area Low (VAL) or selling above the Value Area High (VAH).
   - **Initiative Activity**: Market participants aggressively buy at or above previous fair value, forcing price to discover a new, higher value area.
   - Initiative buying above resistance signals a structural regime shift.

### 2. Market Profile Architecture

Market Profile plots price vertically and time horizontally using 30-minute lettered brackets known as **Time Price Opportunities (TPOs)**:

```
+---------------------------------------------------------------------------------+
|                      MARKET PROFILE & VALUE AREA STRUCTURE                      |
+---------------------------------------------------------------------------------+
|  Price                                                                          |
|  105.00 |  A                 (Single Print / Rejection Wick)                    |
|  104.50 |  A B                                                                  |
|  104.00 |  A B C D           <--- Value Area High (VAH)                         |
|  103.50 |  A B C D E F                                                          |
|  103.00 |  B C D E F G H I   <--- Point of Control (POC, most TPOs)             |
|  102.50 |  B C D E F G H     <--- Value Area Low (VAL)                          |
|  102.00 |  C D E                                                                |
|  101.50 |  C                 (Buying Tail: two single prints)                   |
|  101.00 |  C                                                                    |
+---------------------------------------------------------------------------------+
```

The drawn profile holds 33 TPOs, so the 70% target is 23.1 TPOs.
The single-level rule below starts at the 103.00 POC (8 TPOs) and adds 102.50 (7), then 103.50 (6), then 104.00 (4), stopping at 25 TPOs (75.8%), so VAL = 102.50 and VAH = 104.00.

1. **Initial Balance (IB)**:
   - The price range established during the first hour of regular trading (typically brackets A and B).
   - In the Market Profile day-type taxonomy (Dalton, Jones, and Dalton), a wide IB is typical of range-bound Normal days and a narrow IB leaves room for range extension or a trend day; these are classification heuristics, not measured probabilities.

2. **Point of Control (POC)**:
   - The single price level where the most time (TPO POC) or trading volume (Volume POC / VPOC) was transacted during the session.
   - Profile traders treat prior POCs as levels price is likely to revisit; no peer-reviewed test of that "magnet" claim is cited here.

3. **Value Area (VA)**:
   - The price range surrounding the POC containing $70\%$ of session volume (or TPOs) by convention.
   - The convention is loosely motivated by the normal distribution, but $\pm 1\sigma$ holds $68.27\%$ and $70\%$ needs $\pm 1.04\sigma$; real profiles are rarely normal, so the band is a convention, not a standard deviation.
   - Bounded by **Value Area High (VAH)** and **Value Area Low (VAL)**.
   - The **80% Rule** (Market Profile literature, Dalton, Jones, and Dalton): if price opens outside the prior Value Area and then trades back inside it for two consecutive 30-minute brackets, the rule expects price to rotate through to the opposite boundary.
   - The "80%" is the rule's name; no published statistical test establishing that probability is cited here, so measure it on your own market before relying on it.

### 3. Volume Profile: High Volume Nodes vs Low Volume Nodes

While Market Profile measures time spent, **Volume Profile** measures actual traded shares at each price increment across a defined horizontal lookback:

1. **High Volume Node (HVN)**:
   - A price zone characterized by a wide peak in the volume histogram.
   - Represents an area of intense two-way agreement where buyers and sellers transacted large size (fair-value consensus).
   - Profile traders expect price to move slowly inside an HVN and treat it as support or resistance on later approaches; this is practitioner interpretation, not a tested result.

2. **Low Volume Node (LVN)**:
   - A price zone characterized by a thin valley or liquidity void in the volume histogram.
   - Represents an area of rapid price rejection where the auction moved swiftly without finding two-way trade facilitation.
   - Profile traders expect price re-entering an LVN to move through it quickly toward the next HVN; low past volume at a price does not by itself imply thin resting depth now.

### 4. Volume-Weighted Average Price (VWAP)

VWAP is a standard execution benchmark: Berkowitz, Logue, and Noser (1988) proposed it for measuring the cost of institutional trades, and VWAP algorithms slice orders in proportion to expected volume:

$$\text{VWAP}_t = \frac{\sum_{i=1}^t P_i \times V_i}{\sum_{i=1}^t V_i}$$

where $P_i$ is the typical price $\frac{H_i + L_i + C_i}{3}$ and $V_i$ is the volume of bar $i$.

1. **VWAP Standard Deviation Bands**:
   $$\sigma_t = \sqrt{\frac{\sum_{i=1}^t V_i (P_i - \text{VWAP}_t)^2}{\sum_{i=1}^t V_i}}$$
   - $\text{Upper Band}_k = \text{VWAP}_t + k \times \sigma_t$.
   - $\text{Lower Band}_k = \text{VWAP}_t - k \times \sigma_t$.
   - For $k = 1, 2, 3$, the bands correspond to volume-weighted standard deviation boundaries.
   - The bands measure the volume-weighted dispersion of trade prices since the anchor; they are not confidence intervals for the next price, because prices are serially dependent.
   - Practitioners fade moves beyond $\pm 2\sigma$ in range-bound sessions and use $\pm 1\sigma$ as a trend channel; both are heuristics.

2. **Anchored VWAP (AVWAP)**:
   - Classical intraday VWAP resets every morning at market open.
   - **Anchored VWAP** allows the trader to anchor the volume accumulation calculation to any significant market event:
     - Major swing high or swing low.
     - Earnings announcement gap.
     - Central bank interest rate release.
     - Year-to-date (YTD) or month-to-date (MTD) boundary.
   - It is the volume-weighted average price of all trades since that event, so on average buyers since the anchor are at breakeven when price returns to it.
   - The practitioner claim is that this average cost basis acts as support when tested from above; no peer-reviewed test of AVWAP support is cited here.

### 5. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                        EVIDENCE LEDGER: AUCTION THEORY & VWAP                   |
+---------------------------------------------------------------------------------+
|  Phenomenon: Volume Profile, VWAP Benchmark & Institutional Absorption          |
|  Evidence Grade: STRONG (VWAP as execution benchmark), UNTESTED (profile rules) |
+---------------------------------------------------------------------------------+
|  Key Sources:                                                                   |
|  1. Berkowitz, Logue, and Noser (1988, Journal of Finance):                     |
|     - Proposed VWAP as a benchmark for measuring institutional execution        |
|       cost, the basis of modern transaction cost analysis (TCA).                |
|  2. Jain and Joh (1988, JFQA); Admati and Pfleiderer (1988, RFS):               |
|     - Intraday NYSE volume is higher near the open and close (U-shape);         |
|       Admati-Pfleiderer model why discretionary trading concentrates.           |
|     - VWAP schedules follow this profile; they do not create it.                |
|  3. Steidlmayer and Koy (1986, Markets and Market Logic):                       |
|     - The original statement of Market Profile and its rotation rules; a        |
|       method book, not a statistical test.                                      |
+---------------------------------------------------------------------------------+
|  Counter-Evidence & Caveats:                                                    |
|  1. Failure of Static Bands in Momentum Regimes:                                |
|     - On trend days (initiative auction), fading the +2 sigma VWAP band loses   |
|       as price keeps extending; the bands are not confidence intervals.         |
|  2. Profile Subjectivity in Non-Clearing Windows:                               |
|     - 24-hour electronic markets (crypto, FX, Globex) blur traditional RTH      |
|       session boundaries, requiring adaptive session filtering.                 |
+---------------------------------------------------------------------------------+
```

---

## Worked examples

### Example 1: Calculating Value Area from a Discrete Volume Histogram

An analyst evaluates the (hypothetical) volume distribution of a mini-futures contract across seven 5-point price buckets:
- Level 1 ($100$): $1,000\text{ contracts}$
- Level 2 ($105$): $3,000\text{ contracts}$
- Level 3 ($110$): $7,000\text{ contracts}$
- Level 4 ($115$): $15,000\text{ contracts}$ (Point of Control / POC)
- Level 5 ($120$): $8,000\text{ contracts}$
- Level 6 ($125$): $4,000\text{ contracts}$
- Level 7 ($130$): $2,000\text{ contracts}$

1. **Calculate Total Session Volume ($V_{\text{total}}$)**:
   $$V_{\text{total}} = 1000 + 3000 + 7000 + 15000 + 8000 + 4000 + 2000 = 40,000\text{ contracts}$$

2. **Target Value Area Volume ($70\%$)**:
   $$V_{\text{target}} = 0.70 \times 40,000 = 28,000\text{ contracts}$$

3. **Iterative Value Area Expansion (single-level rule)**:
   - Start at the POC ($115$): Volume $= 15,000$.
   - Compare the next level above with the next level below and add the larger:
     - Above ($120$): $8,000$.
     - Below ($110$): $7,000$.
     - Because $8,000 > 7,000$, add Level 5 ($120$).
     - Running Volume $= 15,000 + 8,000 = 23,000$.
   - Compare next levels:
     - Above ($125$): $4,000$.
     - Below ($110$): $7,000$.
     - Because $7,000 > 4,000$, add Level 3 ($110$).
     - Running Volume $= 23,000 + 7,000 = 30,000$.
   - Target reached ($30,000 \ge 28,000$).
   - **Value Area Range**:
     - $\text{Value Area Low (VAL)} = 110$.
     - $\text{Point of Control (POC)} = 115$.
     - $\text{Value Area High (VAH)} = 120$.
   - Brute force agrees: $110$ to $120$ is the narrowest contiguous range around the POC that holds at least $28,000$ contracts.

4. **The Two-Row Rule Gives a Different Answer**:
   - The CBOT procedure taught with Market Profile compares the sum of the next two levels above with the next two below.
   - Above ($120 + 125$): $12,000$; below ($110 + 105$): $10,000$; add above, running volume $27,000 < 28,000$.
   - Above ($130$): $2,000$; below ($110 + 105$): $10,000$; add below, running volume $37,000$.
   - Value Area $= 105$ to $125$: the rule you choose changes the levels, so state it when you quote a value area.

### Example 2: Computing Anchored VWAP from an Earnings Announcement

An algorithmic trader anchors VWAP to an earnings breakout bar that opened with high volume (hypothetical daily prices and volumes):
- Day 1 (Earnings): Price $= \$200.00$, Volume $= 5,000,000\text{ shares}$.
  $$P_1 \times V_1 = \$200.00 \times 5,000,000 = \$1,000,000,000$$
- Day 2: Price $= \$208.00$, Volume $= 2,500,000\text{ shares}$.
  $$P_2 \times V_2 = \$208.00 \times 2,500,000 = \$520,000,000$$
- Day 3: Price $= \$204.00$, Volume $= 1,500,000\text{ shares}$.
  $$P_3 \times V_3 = \$204.00 \times 1,500,000 = \$306,000,000$$

1. **Calculate Cumulative Traded Dollar Volume**:
   $$\sum P_i V_i = \$1,000,000,000 + \$520,000,000 + \$306,000,000 = \$1,826,000,000$$

2. **Calculate Cumulative Volume**:
   $$\sum V_i = 5,000,000 + 2,500,000 + 1,500,000 = 9,000,000\text{ shares}$$

3. **Compute Anchored VWAP**:
   $$\text{AVWAP} = \frac{\$1,826,000,000}{9,000,000} = \$202.89$$
   The volume-weighted average price of all trades since the earnings release is $\$202.89$.
   If the stock pulls back to $\$203.00$, it is at roughly the average cost of everyone who traded since the release; practitioners watch it as support, but no tested probability attaches to that.

---

## Pitfalls

- **Fading the +2 Sigma VWAP Band on Trend Days**:
  On a strong initiative trend day, buying persists throughout the session.
  Treating $+2\sigma$ as an overbought mean-reversion signal then loses repeatedly as price keeps extending along the upper band.
- **Confusing TPO Profile with Volume Profile**:
  TPO Profile measures time spent at price; Volume Profile measures actual shares transacted.
  A market may spend three hours at a quiet consolidation on tiny volume (high TPO, low volume) and twenty minutes absorbing a massive block trade (low TPO, huge volume).
  Quantitative desks prioritize Volume Profile for liquidity mapping.
- **Neglecting Session Delineation in 24-Hour Markets**:
  Calculating a single continuous 24-hour VWAP dilutes European and US session opens.
  Desks must separate Regular Trading Hours (RTH) from Overnight Extended Hours (ETH) to evaluate institutional participation accurately.
- **Anchoring VWAP to Arbitrary Time Intervals**:
  Anchoring VWAP to arbitrary dates (e.g. random Tuesdays) yields meaningless numbers.
  AVWAP is valid only when anchored to true structural supply-demand shifts (earnings, swing pivots, Fed decisions, session opens).

---

## Interview questions

> [!question]- mkt-ta-065 | What is Auction Market Theory (AMT)?
> A conceptual framework developed by J. Peter Steidlmayer that models financial markets as continuous two-way double auctions whose primary purpose is to facilitate trade.
> Price advertises opportunity, time regulates opportunity, and volume measures market acceptance or rejection.

> [!question]- mkt-ta-066 | What is a Time Price Opportunity (TPO)?
> The basic unit of Market Profile, represented by a letter corresponding to a 30-minute time bracket.
> A TPO is plotted at every price increment where the market traded during that specific 30-minute window.

> [!question]- mkt-ta-067 | Define the Initial Balance (IB) in Market Profile.
> The price range established during the first hour of regular trading (typically the first two 30-minute brackets, A and B).
> It serves as the baseline benchmark against which subsequent initiative or responsive auction activity is evaluated.

> [!question]- mkt-ta-068 | What is the Point of Control (POC)?
> The single price level where the greatest amount of time (TPO POC) or volume (Volume POC) was transacted during the session.
> In auction terms it is the price of greatest two-way agreement in the session.

> [!question]- mkt-ta-069 | What is the Value Area in Market Profile?
> The price range surrounding the POC that holds 70% of trading activity by convention.
> It is bounded by the Value Area High (VAH) and Value Area Low (VAL); the 70% only loosely echoes a normal's one standard deviation, which holds 68.27% (70% needs 1.04 sigma).

> [!question]- mkt-ta-070 | Explain the Market Profile "80% Rule".
> If the market opens outside the prior session's Value Area and then trades back inside it for two consecutive 30-minute brackets, the rule expects a rotation to the opposite Value Area boundary.
> The "80%" is the rule's name in the Market Profile literature, not a probability established by a published test; measure it before trading it.

> [!question]- mkt-ta-071 | Contrast responsive trading with initiative trading.
> Responsive trading acts counter to price extremes, buying below fair value or selling above it to return price to the value area.
> Initiative trading aggressively buys at or above fair value (or sells below), pushing price to establish an entirely new value area.

> [!question]- mkt-ta-072 | What is a High Volume Node (HVN) in Volume Profile?
> A price zone exhibiting a prominent peak in traded volume, indicating extensive fair-value agreement and two-way trade facilitation.
> Profile traders expect price to move slowly through an HVN and treat it as support or resistance on retests (practitioner interpretation).

> [!question]- mkt-ta-073 | What is a Low Volume Node (LVN) in Volume Profile?
> A price zone exhibiting a sharp valley in traded volume, representing rapid price rejection and liquidity voids.
> Profile traders expect price re-entering an LVN to traverse it quickly; low past volume at a price does not by itself prove thin resting depth now.

> [!question]- mkt-ta-074 | State the formula for Volume-Weighted Average Price (VWAP).
> VWAP = sum(Price_i * Volume_i) / sum(Volume_i).
> It computes the true volume-weighted average price of all transactions executed from the anchor point to time t.

> [!question]- mkt-ta-075 | What is Anchored VWAP (AVWAP) and who popularized it?
> A method popularized by Brian Shannon (2023, *Maximum Trading Gains with Anchored VWAP*) that calculates VWAP starting from a specific, user-defined event rather than the daily open.
> Common anchors include major swing lows, swing highs, earnings announcement gaps, and year-to-date opens.

> [!question]- mkt-ta-076 | Why does an Anchored VWAP from an earnings release act as strong support on pullbacks?
> It is the volume-weighted average price of all trades since the catalyst, so the average buyer since then is at breakeven there.
> The practitioner argument is that buyers defend that cost basis; it is a hypothesis, and no peer-reviewed test of AVWAP support is cited here.

> [!question]- mkt-ta-077 | What are VWAP standard deviation bands?
> Symmetrical envelopes plotted at 1, 2, and 3 volume-weighted standard deviations above and below the VWAP line: Upper_k = VWAP + k * sigma.
> Practitioners use them to flag overextension in range-bound sessions and as trend channels in trending ones; they are dispersion measures, not confidence intervals.

> [!question]- mkt-ta-078 | What is a Trend Day in Market Profile classification?
> A session characterized by strong directional conviction where price opens near one extreme, expands continuously in one direction, and closes at the opposite extreme.
> The Value Area is wide and vertically displaced, with volume distributed evenly along the trend.

> [!question]- mkt-ta-079 | What is a Normal Day in Market Profile classification?
> A session with a wide Initial Balance established in the first hour that contains the vast majority of the day's total range.
> Subsequent trading consists of responsive rotational auctions within the established extremes.

> [!question]- mkt-ta-080 | What is a Normal Variation Day?
> A session where early trading establishes an Initial Balance, followed by a moderate initiative range extension beyond it in later brackets.
> Activity then settles into rotational balance around the new price level.

> [!question]- mkt-ta-081 | What is a Neutral Day?
> A session where initiative activity expands price beyond both the top and bottom of the Initial Balance, but closes near the center.
> In auction terms neither side won the session.

> [!question]- mkt-ta-082 | What is a Non-Trend Day?
> A session with a tiny Initial Balance and virtually zero subsequent range expansion, forming a narrow, compressed profile on low volume.
> It reflects a lack of initiative participation, as before a major announcement or holiday.

> [!question]- mkt-ta-083 | What is an Open-Drive in Market Profile opening types?
> Price opens, aggressively prints in one direction without retracing, and violently drives away from the prior session's value area.
> Profile traders read it as strong initiative conviction and a candidate Trend Day (classification heuristic, not a measured probability).

> [!question]- mkt-ta-084 | What is an Open-Test-Drive?
> Price opens, briefly tests in one direction to probe for responsive liquidity, finds strong rejection, and then drives aggressively in the opposite direction.
> The initial test confirms lack of counterparty participation, unleashing directional conviction.

> [!question]- mkt-ta-085 | What is an Open-Rejection-Reverse?
> Price opens, probes beyond the prior session's range, encounters fierce responsive counter-orders, and violently reverses back through the open and into the prior value area.
> Profile traders read it as a failed auction outside value.

> [!question]- mkt-ta-086 | What is an Open-Auction?
> Price opens inside the prior session's value area and oscillates aimlessly with no directional initiative.
> Profile traders read it as low conviction, which favors responsive, mean-reverting trade inside value.

> [!question]- mkt-ta-087 | What is a single print in Market Profile?
> A price level occupied by only one 30-minute letter bracket during the entire trading session.
> Single prints mark prices the market moved through quickly; profile traders treat them like LVNs.

> [!question]- mkt-ta-088 | What is a buying tail or selling tail in Market Profile?
> A vertical sequence of at least two consecutive single prints at the extreme low (buying tail) or extreme high (selling tail) of a session profile.
> Profile traders read a tail as strong responsive activity at the extreme and watch it as support or resistance.

> [!question]- mkt-ta-089 | What is poor high or poor low in Market Profile?
> An extreme price level lacking single prints, ending abruptly with two or more adjacent TPOs at the high or low.
> Profile traders read it as an auction that stopped without a clear rejection, "unfinished business" they expect price to revisit (a heuristic, not a tested result).

> [!question]- mkt-ta-090 | What is a naked POC (virgin POC)?
> A Point of Control from a prior session that has not been tested or touched by price in any subsequent trading session.
> Profile traders use naked POCs as targets on the view that price tends to revisit them; that tendency is not established by a test cited here.

> [!question]- mkt-ta-091 | Why do institutional execution desks target VWAP as a transaction benchmark?
> Trading a large parent order in proportion to the expected intraday volume profile spreads its impact and makes the fill comparable to the day's average price.
> Berkowitz, Logue, and Noser (1988) proposed VWAP for measuring execution cost; VWAP ignores the price at the time of the decision, which is why implementation shortfall (Perold 1988) is also used.

> [!question]- mkt-ta-092 | What is the U-shaped intraday volume smile?
> The tendency for trading volume to be higher near the open and close than at midday, documented for NYSE stocks by Jain and Joh (1988) and modelled by Admati and Pfleiderer (1988).
> VWAP algorithms follow this profile by allocating larger slices near the open and close; they do not create it.

> [!question]- mkt-ta-093 | How does Anchored VWAP help identify trapped short sellers after an earnings gap?
> If price holds above the AVWAP anchored to the earnings gap, the average short seller since the gap is underwater (individual shorts may not be).
> The practitioner expectation is short covering and dip buying on later tests of the AVWAP; that is a hypothesis to test.

> [!question]- mkt-ta-094 | What is composite Volume Profile?
> An aggregated Volume Profile constructed by combining multiple weeks, months, or years of price and volume data into a single master histogram.
> Practitioners use it to find long-horizon high- and low-volume price zones.

> [!question]- mkt-ta-095 | What is developing POC (d-POC)?
> The continuous real-time calculation of the Point of Control as volume accumulates throughout an active trading session.
> Shifts in the d-POC indicate intraday price acceptance migrating higher or lower.

> [!question]- mkt-ta-096 | What does Volume Profile add over drawing support and resistance lines by eye, and what does it not prove?
> It replaces subjective visual peaks with a measured histogram of where volume traded, so levels are reproducible from the data.
> It does not prove those levels predict future reversals; that still needs an out-of-sample test with costs, and the levels depend on the lookback and bucket size chosen.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_ta_03_auction_vwap.py`](../../code/mkt_ta_03_auction_vwap.py) prints and asserts every number on this page: the value area stepped out by the single-level rule and checked against a brute-force search over every contiguous range around the POC, the two-row rule's different answer, the normal-distribution masses by the error function and by Simpson quadrature (with the 70% quantile by bisection), and the anchored VWAP in exact rational arithmetic and as a share-by-share average.
- Related notes: [Order Flow, Tape Reading and Footprint](06-Order-Flow-Tape-Reading-and-Footprint.md), [Dow Theory and Trend Evidence](01-Dow-Theory-and-Trend-Evidence.md).

## Further reading

- Steidlmayer, J. P., & Koy, K. (1986). *Markets and Market Logic*. Porcupine Press.
- Berkowitz, S. A., Logue, D. E., & Noser, E. A. (1988). *The total cost of transactions on the NYSE*. The Journal of Finance, 43(1), 97-112.
- Dalton, J. F., Jones, E. T., & Dalton, R. B. (1990). *Mind Over Markets: Power Trading with Market Generated Information*. Probus Publishing Co. (updated edition, Wiley, 2013).
- Jain, P. C., & Joh, G.-H. (1988). *The dependence between hourly prices and trading volume*. Journal of Financial and Quantitative Analysis, 23(3), 269-283.
- Perold, A. F. (1988). *The implementation shortfall: Paper versus reality*. The Journal of Portfolio Management, 14(3), 4-9.
- Admati, A. R., & Pfleiderer, P. (1988). *A theory of intraday patterns: Volume and price variability*. The Review of Financial Studies, 1(1), 3-40.
- Madhavan, A. (2000). *Market microstructure: A survey*. Journal of Financial Markets, 3(3), 205-258 (background on execution and price formation).
- Dalton, J. F., Jones, E. T., & Dalton, R. B. (2007). *Markets in Profile: Ways to Profit from the New Auction Market Science*. John Wiley & Sons.
- Shannon, B. (2023). *Maximum Trading Gains with Anchored VWAP*. Alpha Trends.
