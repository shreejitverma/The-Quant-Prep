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
Developed in the 1980s by J. Peter Steidlmayer at the Chicago Board of Trade (CBOT), Auction Market Theory (AMT) and the Market Profile conceptualize financial markets as continuous two-way double auctions whose primary purpose is to facilitate trade between buyers and sellers.
In this framework, price is merely an advertising mechanism, time regulates opportunity, and volume measures market acceptance or rejection.
By mapping volume against price rather than time, Volume Profile and Anchored Volume-Weighted Average Price (AVWAP) reveal the structural liquidity landscape and institutional fair-value consensus.

---

## TL;DR

Auction Market Theory models markets as a dual search process for fair value: exploring higher prices until buyers refuse to transact (buying exhaustion) and exploring lower prices until sellers dry up (selling exhaustion).
Market Profile visualizes this distribution via Time Price Opportunities (TPOs), defining the Point of Control (POC, price with maximum time spent) and the Value Area (the price range containing approximately $70\%$ of trade activity, mirroring one standard deviation in a Gaussian distribution).
Volume Profile measures actual executed shares at price, revealing High Volume Nodes (HVNs, fair-value consolidation zones) and Low Volume Nodes (LVNs, rapid price rejection or liquidity voids).
Volume-Weighted Average Price (VWAP) serves as the primary execution benchmark for institutional order flow; Anchored VWAP (anchored to significant swing lows, highs, earnings gaps, or session opens) acts as dynamic, volume-weighted support and resistance.

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
|                       MARKET PROFILE & VALUE AREA STRUCTURE                     |
+---------------------------------------------------------------------------------+
|  Price                                                                          |
|  105.00 |  A                                   (Single Print / Rejection Wick)  |
|  104.50 |  A B                                                                  |
|  104.00 |  A B C D           <--- Value Area High (VAH, ~70% Upper Bound)       |
|  103.50 |  A B C D E F G                                                        |
|  103.00 |  A B C D E F G H I <--- Point of Control (POC, Maximum Time/Volume)   |
|  102.50 |  B C D E F G H                                                        |
|  102.00 |  C D E F           <--- Value Area Low (VAL, ~70% Lower Bound)        |
|  101.50 |  D E                                                                  |
|  101.00 |  E                 (Single Print / Buying Tail)                       |
+---------------------------------------------------------------------------------+
```

1. **Initial Balance (IB)**:
   - The price range established during the first hour of regular trading (typically brackets A and B).
   - The width of the IB indicates expected session volatility: a wide IB suggests a range-bound, rotation day; a narrow IB suggests an impending explosive trend day.

2. **Point of Control (POC)**:
   - The single price level where the most time (TPO POC) or trading volume (Volume POC / VPOC) was transacted during the session.
   - Acts as a powerful gravitational magnet for price retests in subsequent sessions.

3. **Value Area (VA)**:
   - The price range surrounding the POC containing approximately $68.2\%$ to $70.0\%$ of total session volume (mirroring $\pm 1\sigma$ in a normal distribution).
   - Bounded by **Value Area High (VAH)** and **Value Area Low (VAL)**.
   - The **80% Rule**: If price opens or penetrates outside the Value Area and accepts within it for two consecutive 30-minute brackets, there is an $80\%$ probability of rotating entirely through the Value Area to the opposite boundary.

### 3. Volume Profile: High Volume Nodes vs Low Volume Nodes

While Market Profile measures time spent, **Volume Profile** measures actual traded shares at each price increment across a defined horizontal lookback:

1. **High Volume Node (HVN)**:
   - A price zone characterized by a wide peak in the volume histogram.
   - Represents an area of intense two-way agreement where buyers and sellers transacted large size (fair-value consensus).
   - Price behaves "sluggishly" inside an HVN, exhibiting high friction and mean reversion.
   - Serves as formidable support or resistance on subsequent approaches.

2. **Low Volume Node (LVN)**:
   - A price zone characterized by a thin valley or liquidity void in the volume histogram.
   - Represents an area of rapid price rejection where the auction moved swiftly without finding two-way trade facilitation.
   - When price re-enters an LVN, it encounters minimal resting liquidity and slices through rapidly toward the next HVN.

### 4. Volume-Weighted Average Price (VWAP)

VWAP is the benchmark execution reference utilized by institutional algorithms to minimize market impact:

$$\text{VWAP}_t = \frac{\sum_{i=1}^t P_i \times V_i}{\sum_{i=1}^t V_i}$$

where $P_i$ is the typical price $\frac{H_i + L_i + C_i}{3}$ and $V_i$ is the volume of bar $i$.

1. **VWAP Standard Deviation Bands**:
   $$\sigma_t = \sqrt{\frac{\sum_{i=1}^t V_i (P_i - \text{VWAP}_t)^2}{\sum_{i=1}^t V_i}}$$
   - $\text{Upper Band}_k = \text{VWAP}_t + k \times \sigma_t$.
   - $\text{Lower Band}_k = \text{VWAP}_t - k \times \sigma_t$.
   - For $k = 1, 2, 3$, the bands correspond to volume-weighted standard deviation boundaries.
   - In mean-reverting sessions, moves beyond $\pm 2\sigma$ represent statistical overextension; in trend days, price rides the $\pm 1\sigma$ band as dynamic support/resistance.

2. **Anchored VWAP (AVWAP)**:
   - Classical intraday VWAP resets every morning at market open.
   - **Anchored VWAP** allows the trader to anchor the volume accumulation calculation to any significant market event:
     - Major swing high or swing low.
     - Earnings announcement gap.
     - Central bank interest rate release.
     - Year-to-date (YTD) or month-to-date (MTD) boundary.
   - Represents the exact volume-weighted average price paid by all market participants since that critical inflection point.
   - When an asset tests its AVWAP from above, former buyers are at their average cost basis, providing powerful structural support.

### 5. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                        EVIDENCE LEDGER: AUCTION THEORY & VWAP                   |
+---------------------------------------------------------------------------------+
|  Phenomenon: Volume Profile, VWAP Benchmark & Institutional Absorption          |
|  Evidence Grade: STRONG (Execution & Microstructure), MIXED (Directional Edge)  |
+---------------------------------------------------------------------------------+
|  Key Empirical Studies:                                                         |
|  1. Berkowitz, Logue, and Noser (1988, Journal of Finance):                     |
|     - Proposed VWAP as a benchmark for measuring institutional execution        |
|       cost, the basis of modern transaction cost analysis (TCA).                |
|  2. Madhavan (2000, Journal of Financial Markets):                              |
|     - Evaluated VWAP execution strategies and institutional order flow.         |
|     - Showed institutional desks systematically execute orders using VWAP       |
|       schedules, creating predictable intraday volume smiles (U-shaped volume). |
|  3. Steidlmayer and Koy (1986, Markets and Market Logic):                       |
|     - Documented empirical distribution of CBOT futures prices conforming to    |
|       value area boundaries and rotation rules.                                 |
+---------------------------------------------------------------------------------+
|  Counter-Evidence & Caveats:                                                    |
|  1. Failure of Static Bands in Momentum Regimes:                                |
|     - In strong institutional trend days (Initiative auction), fade strategies   |
|       at the +2 sigma VWAP band suffer catastrophic short squeeze losses.       |
|  2. Profile Subjectivity in Non-Clearing Windows:                               |
|     - 24-hour electronic markets (crypto, FX, Globex) blur traditional RTH session |
|       boundaries, requiring adaptive session filtering.                         |
+---------------------------------------------------------------------------------+
```

---

## Worked examples

### Example 1: Calculating Value Area from a Discrete Volume Histogram

An exchange specialist evaluates the volume distribution of a mini-futures contract across seven 5-point price buckets:
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

3. **Iterative Value Area Expansion**:
   - Start at the POC ($115$): Volume $= 15,000$.
   - Compare two levels immediately above and below:
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

### Example 2: Computing Anchored VWAP from an Earnings Announcement

An algorithmic trader anchors VWAP to an earnings breakout bar that opened with high volume:
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
   The aggregate volume-weighted average price paid by institutional market participants since the earnings release is $\$202.89$.
   If the stock pulls back to $\$203.00$, it tests institutional breakeven, representing a high-probability support zone.

---

## Pitfalls

- **Fading the +2 Sigma VWAP Band on Trend Days**:
  On a strong initiative trend day, institutional algorithms buy continuously throughout the session.
  Treating $+2\sigma$ as an overbought mean-reversion signal results in catastrophic losses as price rides the upper band into the close.
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
> It represents the consensus price of maximum fair-value agreement between buyers and sellers.

> [!question]- mkt-ta-069 | What is the Value Area in Market Profile?
> The price range surrounding the POC that encompasses approximately 70% (one standard deviation) of total trading activity.
> It is bounded by the Value Area High (VAH) and Value Area Low (VAL).

> [!question]- mkt-ta-070 | Explain the Market Profile "80% Rule".
> If the market opens or penetrates outside the prior session's Value Area and then accepts back inside for two consecutive 30-minute brackets, there is an 80% statistical probability of rotating completely to the opposite Value Area boundary.

> [!question]- mkt-ta-071 | Contrast responsive trading with initiative trading.
> Responsive trading acts counter to price extremes, buying below fair value or selling above it to return price to the value area.
> Initiative trading aggressively buys at or above fair value (or sells below), pushing price to establish an entirely new value area.

> [!question]- mkt-ta-072 | What is a High Volume Node (HVN) in Volume Profile?
> A price zone exhibiting a prominent peak in traded volume, indicating extensive fair-value agreement and two-way trade facilitation.
> Price moves slowly through an HVN, acting as high-friction support or resistance on retests.

> [!question]- mkt-ta-073 | What is a Low Volume Node (LVN) in Volume Profile?
> A price zone exhibiting a sharp valley in traded volume, representing rapid price rejection and liquidity voids.
> When price re-enters an LVN, it traverses the zone rapidly due to minimal resting order book resistance.

> [!question]- mkt-ta-074 | State the formula for Volume-Weighted Average Price (VWAP).
> VWAP = sum(Price_i * Volume_i) / sum(Volume_i).
> It computes the true volume-weighted average price of all transactions executed from the anchor point to time t.

> [!question]- mkt-ta-075 | What is Anchored VWAP (AVWAP) and who popularized it?
> A methodology popularized by Brian Shannon that calculates VWAP starting from a specific, user-defined historical event rather than the daily open.
> Common anchors include major swing lows, swing highs, earnings announcement gaps, and year-to-date opens.

> [!question]- mkt-ta-076 | Why does an Anchored VWAP from an earnings release act as strong support on pullbacks?
> It represents the exact breakeven price for all institutional participants who bought or sold stock since the fundamental catalyst.
> Institutional buyers defend their average cost basis by placing supporting limit orders at the AVWAP.

> [!question]- mkt-ta-077 | What are VWAP standard deviation bands?
> Symmetrical envelopes plotted at 1, 2, and 3 volume-weighted standard deviations above and below the VWAP line: Upper_k = VWAP + k * sigma.
> They identify statistical overextension in range-bound markets and dynamic trend channels in momentum markets.

> [!question]- mkt-ta-078 | What is a Trend Day in Market Profile classification?
> A session characterized by strong directional conviction where price opens near one extreme, expands continuously in one direction, and closes at the opposite extreme.
> The Value Area is wide and vertically displaced, with volume distributed evenly along the trend.

> [!question]- mkt-ta-079 | What is a Normal Day in Market Profile classification?
> A session with a wide Initial Balance established in the first hour that contains the vast majority of the day's total range.
> Subsequent trading consists of responsive rotational auctions within the established extremes.

> [!question]- mkt-ta-080 | What is a Normal Variation Day?
> A session where early trading establishes an Initial Balance, followed by a moderate initiative range extension (typically about 0.5x to 1.0x the IB width) during later brackets.
> Activity then settles into rotational balance around the new price level.

> [!question]- mkt-ta-081 | What is a Neutral Day?
> A session where initiative activity expands price beyond both the top and bottom of the Initial Balance, but closes near the center.
> It indicates an aggressive battle between buyers and sellers with no definitive winner, signaling balanced two-way trade.

> [!question]- mkt-ta-082 | What is a Non-Trend Day?
> A session with a tiny Initial Balance and virtually zero subsequent range expansion, forming a narrow, compressed profile on low volume.
> It reflects extreme market indecision, typically preceding major macro announcements or holidays.

> [!question]- mkt-ta-083 | What is an Open-Drive in Market Profile opening types?
> Price opens, aggressively prints in one direction without retracing, and violently drives away from the prior session's value area.
> It reflects massive institutional initiative conviction and signals a high probability of a Trend Day.

> [!question]- mkt-ta-084 | What is an Open-Test-Drive?
> Price opens, briefly tests in one direction to probe for responsive liquidity, finds strong rejection, and then drives aggressively in the opposite direction.
> The initial test confirms lack of counterparty participation, unleashing directional conviction.

> [!question]- mkt-ta-085 | What is an Open-Rejection-Reverse?
> Price opens, probes beyond the prior session's range, encounters fierce responsive counter-orders, and violently reverses back through the open and into the prior value area.
> It represents a classic failed auction and false breakout setup.

> [!question]- mkt-ta-086 | What is an Open-Auction?
> Price opens inside the prior session's value area and oscillates aimlessly with no directional initiative.
> It signals low conviction and favors responsive, mean-reverting scalp strategies.

> [!question]- mkt-ta-087 | What is a single print in Market Profile?
> A price level occupied by only one 30-minute letter bracket during the entire trading session.
> Single prints indicate rapid price rejection and directional velocity, functioning as LVNs that price quickly traverses on retests.

> [!question]- mkt-ta-088 | What is a buying tail or selling tail in Market Profile?
> A vertical sequence of at least two consecutive single prints at the extreme low (buying tail) or extreme high (selling tail) of a session profile.
> It confirms aggressive responsive participation and marks strong institutional support or resistance.

> [!question]- mkt-ta-089 | What is poor high or poor low in Market Profile?
> An extreme price level lacking single prints, ending abruptly with two or more adjacent TPOs at the high or low.
> It indicates that the auction was halted mechanically rather than through natural buyer/seller exhaustion, leaving unfinished business to be repaired.

> [!question]- mkt-ta-090 | What is a naked POC (virgin POC)?
> A Point of Control from a prior session that has not been tested or touched by price in any subsequent trading session.
> Naked POCs represent unvisited fair-value nodes that act as strong magnet targets during future market rotations.

> [!question]- mkt-ta-091 | Why do institutional execution desks target VWAP as a transaction benchmark?
> Executing large parent orders in proportion to historical intraday volume profiles minimizes market impact and prevents adverse selection.
> Portfolio managers evaluate broker performance by comparing execution prices to the full-day VWAP.

> [!question]- mkt-ta-092 | What is the U-shaped intraday volume smile?
> The empirical tendency for equity and futures trading volume to concentrate heavily in the first hour of trading and the final hour of trading, with lower volume during midday.
> VWAP execution algorithms allocate higher order slices to the market open and close.

> [!question]- mkt-ta-093 | How does Anchored VWAP help identify trapped short sellers after an earnings gap?
> If price gaps up on earnings and continues to hold above the AVWAP anchored to the gap, every short seller who initiated positions after earnings is underwater.
> Any subsequent test of the AVWAP triggers short-covering and dip-buying.

> [!question]- mkt-ta-094 | What is composite Volume Profile?
> An aggregated Volume Profile constructed by combining multiple weeks, months, or years of price and volume data into a single master histogram.
> It reveals multi-year structural support, resistance, and secular fair-value nodes.

> [!question]- mkt-ta-095 | What is developing POC (d-POC)?
> The continuous real-time calculation of the Point of Control as volume accumulates throughout an active trading session.
> Shifts in the d-POC indicate intraday price acceptance migrating higher or lower.

> [!question]- mkt-ta-096 | Why is trading Volume Profile superior to traditional horizontal support and resistance lines?
> Traditional support lines rely on subjective visual peaks and ignore transaction size.
> Volume Profile maps exactly where billions of dollars in real institutional capital transacted, removing chartist subjectivity.

---

## Further reading

- Steidlmayer, J. P., & Koy, K. (1986). *Markets and Market Logic*. Porcupine Press.
- Berkowitz, S. A., Logue, D. E., & Noser, E. A. (1988). *The total cost of transactions on the NYSE*. The Journal of Finance, 43(1), 97-112.
- Dalton, J. F., Jones, E. T., & Dalton, R. B. (1993). *Mind Over Markets: Power Trading with Market Generated Information*. Probus Publishing Co.
- Madhavan, A. (2000). *Market microstructure: A survey*. Journal of Financial Markets, 3(3), 205-258.
- Dalton, J. F., Jones, E. T., & Dalton, R. B. (2007). *Markets in Profile: Ways to Profit from the New Auction Market Science*. John Wiley & Sons.
- Shannon, B. (2023). *Maximum Trading Gains with Anchored VWAP*. Alpha Trends.
