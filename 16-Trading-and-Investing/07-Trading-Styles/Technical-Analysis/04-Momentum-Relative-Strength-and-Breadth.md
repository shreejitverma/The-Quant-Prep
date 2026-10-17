---
type: concept
title: "Cross-Sectional Momentum, Relative Strength, and Market Breadth"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [technical-analysis, momentum, relative-strength, market-breadth, advance-decline, mcclellan-oscillator, stage-analysis]
prereqs: []
---

# Cross-Sectional Momentum, Relative Strength, and Market Breadth

While individual asset price patterns are susceptible to market noise, relative performance across securities reveals powerful structural trends in capital allocation.
First documented empirically in asset pricing by Narasimhan Jegadeesh and Sheridan Titman in their landmark 1993 study, cross-sectional momentum - the tendency for assets that outperformed their peers over the past 3 to 12 months to continue outperforming over the subsequent 3 to 12 months - stands as the single most robust empirical anomaly in quantitative finance.
In discretionary technical analysis, this phenomenon is evaluated through Relative Strength (RS) ratio lines and market breadth indicators (Advance-Decline statistics, McClellan Oscillators, and High-Low indices) to diagnose the internal health of broad market trends.

---

## TL;DR

Cross-sectional momentum ranks securities across an investment universe by historical performance (typically 12-month return skipping the most recent month to avoid short-term reversal) and allocates capital to top-quintile "winners" while shorting or avoiding bottom-quintile "losers."
Relative Strength lines ($P_{\text{asset}} / P_{\text{benchmark}}$) and Mansfield Relative Strength quantify whether a stock is outperforming the benchmark index; leading stocks make new highs in RS weeks before breaking out in nominal price.
Market breadth measures the participation of individual constituents within a capitalization-weighted index.
Breadth divergences - where mega-cap indices (e.g. S&P 500, Nasdaq 100) make new record highs driven by a handful of tech giants while the Advance-Decline Line, New Highs-New Lows, and equal-weighted indices deteriorate - serve as institutional early warnings of impending market exhaustion.

---

## Learning objectives

- Formulate and calculate cross-sectional momentum metrics and construct long-short winner-loser portfolios.
- Evaluate the empirical asset pricing evidence for momentum (Jegadeesh-Titman 1993, Asness-Moskowitz-Pedersen 2013).
- Model Relative Strength (RS) ratio charts, Mansfield Relative Strength, and Weinstein Stage Analysis.
- Compute aggregate market breadth indicators: the Cumulative Advance-Decline Line, McClellan Oscillator, and High-Low Index.
- Analyze the mechanics and risk-mitigation techniques for momentum crashes (Barroso and Santa-Clara 2015).

---

## Core concepts

### 1. Cross-Sectional Momentum in Empirical Asset Pricing

In their 1993 *Journal of Finance* paper, Jegadeesh and Titman examined the relative performance of US equities sorted into deciles based on returns over the past $J$ months ($J \in \{3, 6, 9, 12\}$) and held for $K$ months ($K \in \{3, 6, 9, 12\}$):

1. **Portfolio Construction Protocol ($12-1$ Momentum)**:
   - At month $t$, evaluate the cumulative gross return of each asset $i$ from month $t-12$ to month $t-1$:
     $$R_i(t-12, t-1) = \prod_{k=1}^{11} (1 + r_{i, t-k}) - 1$$
   - The most recent month $t-1$ is deliberately skipped ("the 1-month skip") to avoid the well-documented 1-month short-term reversal anomaly driven by bid-ask bounce and liquidity provision (Jegadeesh 1990).
   - Assets are ranked:
     - Long top decile ($P_1$, "Winners").
     - Short bottom decile ($P_{10}$, "Losers").

2. **Empirical Return Distribution**:
   - The $12-1$ Momentum portfolio generates average annualized excess returns of $8\%$ to $12\%$ across global equities.
   - Eugene Fama and Kenneth French (2012) confirmed that the momentum premium cannot be explained by standard market beta, firm size, or value factors, prompting the addition of the UMD (Up Minus Down) factor to the Fama-French factor suite.
   - Asness, Moskowitz, and Pedersen (2013) demonstrated in *Value and Momentum Everywhere* that momentum is pervasive across international equities, government bond markets, currencies, and commodity futures.

```
+---------------------------------------------------------------------------------+
|                         CROSS-SECTIONAL MOMENTUM FORMULATION                    |
|                                                                                 |
|  [ Month t-12 ] ------------ Lookback Window (11 Months) ------------> [ t-1 ]  |
|                                                                        | Skip |
|                                                                        v  1M  |
|  Sort Stocks by Cumulative Return ---> Long Top 10% / Short Bottom 10% [ t ]    |
|                                                                                 |
|  Hold Portfolio for Subsequent 3 to 12 Months ---> Expected Alpha: +8% to +12%  |
+---------------------------------------------------------------------------------+
```

### 2. Relative Strength Metrics in Discretionary Trading

Discretionary market wizards (e.g. Richard Wyckoff, Stan Weinstein, William O'Neil) systematized relative strength as their primary stock selection criterion:

1. **The Relative Strength Ratio**:
   $$\text{RS Ratio}_t = \frac{P_t^{\text{stock}}}{P_t^{\text{benchmark}}}$$
   - When the RS ratio is rising, the stock is outperforming the benchmark index; when falling, it is underperforming.
   - **Key Chartist Principle**: During a broad market correction, a stock whose RS line makes a new high while the market index makes lower lows exhibits powerful institutional accumulation.

2. **Mansfield Relative Strength (RSM)**:
   Developed by Stan Weinstein for Stage Analysis, the Mansfield RS normalizes the ratio around a zero baseline using an $N$-week moving average (typically $N = 30$ or $52$ weeks):
   $$\text{RSM}_t = \left(\frac{R_t}{\frac{1}{N} \sum_{i=0}^{N-1} R_{t-i}} - 1\right) \times 100, \quad \text{where } R_t = \frac{P_t^{\text{stock}}}{P_t^{\text{benchmark}}}$$
   - A stock transitioning from below zero to above zero while breaking out of a multi-month base signals an authentic Weinstein **Stage 2 Breakout**.

3. **William O'Neil's IBD Relative Strength Rating**:
   - A percentile ranking from $1$ to $99$ comparing a stock's performance against all other publicly traded stocks over the trailing 12 months.
   - Weights the most recent quarter by $40\%$ and prior quarters by $20\%$ each:
     $$\text{Score} = 0.40 \times R_{Q1} + 0.20 \times R_{Q2} + 0.20 \times R_{Q3} + 0.20 \times R_{Q4}$$
   - Institutional growth strategies require an RS rating of at least $80$ (top $20\%$ of all stocks).

### 3. Market Breadth and Internal Indicators

Capitalization-weighted indexes (e.g., S&P 500, Nasdaq 100) are dominated by their largest constituent companies.
Market breadth monitors the broad underlying distribution of equities to detect whether rallies are supported by broad participation or disguised by a narrow leadership:

1. **The Advance-Decline (A/D) Line**:
   - Cumulative sum of advancing stocks minus declining stocks on an exchange:
     $$\text{AD Line}_t = \text{AD Line}_{t-1} + (\text{Advancing Issues}_t - \text{Declining Issues}_t)$$
   - In a healthy bull market, the A/D line advances alongside market indexes.
   - **Bearish Breadth Divergence**: If the S&P 500 reaches a new record high while the NYSE A/D line fails to reach a new high and trends downward, market internals are severely decaying.

2. **The McClellan Oscillator and Summation Index**:
   - Developed by Sherman and Marian McClellan (1969), the oscillator applies exponential moving averages to net advancing issues:
     $$\text{Net Advances}_t = \text{Advancing Issues}_t - \text{Declining Issues}_t$$
     $$\text{McClellan Oscillator}_t = \text{EMA}_{19}(\text{Net Advances}_t) - \text{EMA}_{39}(\text{Net Advances}_t)$$
   - The **McClellan Summation Index** is the cumulative sum of daily oscillator values, functioning as a long-term breadth barometer.
   - **Breadth Thrust**: A violent surge in the McClellan Oscillator from deep negative territory ($< -100$) to extreme positive territory ($> +100$) indicates overwhelming institutional accumulation, historically initiating multi-year secular bull advances (Marty Zweig Breadth Thrust).

3. **New 52-Week Highs minus New Lows (NH - NL)**:
   - Measures extreme performance across the market:
     $$\text{Net New Highs}_t = \text{New 52w Highs}_t - \text{New 52w Lows}_t$$
   - A healthy bull market maintains positive net new highs ($> +100$ daily).
   - If market indexes rally while New 52-Week Lows expand above $100$, an internal bear market is underway beneath the surface.

### 4. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                       EVIDENCE LEDGER: MOMENTUM & BREADTH                       |
+---------------------------------------------------------------------------------+
|  Phenomenon: Cross-Sectional Momentum & Market Breadth Divergence               |
|  Evidence Grade: STRONG (Premier Academic Anomaly)                              |
+---------------------------------------------------------------------------------+
|  Key Empirical Studies:                                                         |
|  1. Jegadeesh and Titman (1993, Journal of Finance):                            |
|     - Established 3-12 month momentum producing ~1% monthly excess returns.     |
|     - Verified robust across size, beta, and industry subsamples.               |
|  2. Asness, Moskowitz, and Pedersen (2013, Journal of Finance):                 |
|     - "Value and Momentum Everywhere" confirmed momentum across 8 markets.     |
|     - Negative correlation between value and momentum yields massive multi-style|
|       diversification benefits.                                                 |
|  3. Daniel and Moskowitz (2016, Journal of Financial Economics):                |
|     - "Momentum Crashes": isolated the structural left-tail risk of momentum.   |
|     - Following major market panics, past losers violently rebound while past   |
|       winners lag, triggering severe short squeezes in unhedged momentum.       |
|  4. Barroso and Santa-Clara (2015, Journal of Financial Economics):             |
|     - "Beyond the Carry": dynamic volatility-scaled momentum eliminates         |
|       crash risk and nearly doubles the Sharpe ratio from 0.53 to 0.97.         |
+---------------------------------------------------------------------------------+
|  Counter-Evidence & Failure Modes:                                              |
|  1. High Turnover and Execution Drag:                                           |
|     - Lesmond, Schill, and Zhou (2004) argued momentum returns are concentrated |
|       in illiquid, high-cost small stocks where transaction costs erase alpha.  |
|  2. Factor Crowding and Liquidity Shocks:                                       |
|     - Momentum exhibits sharp deleveraging drawdowns during quantitative factor |
|       unwinds (e.g. Quant Meltdown of August 2007).                             |
+---------------------------------------------------------------------------------+
```

---

## Worked examples

### Example 1: Calculating Cross-Sectional Momentum Return and Ranking

A quantitative equity researcher evaluates three stocks in a universe at month $t$:
- Stock A (Tech): Cumulative Return $t-12$ to $t-1 = +45.0\%$.
- Stock B (Consumer): Cumulative Return $t-12$ to $t-1 = +12.0\%$.
- Stock C (Energy): Cumulative Return $t-12$ to $t-1 = -28.0\%$.
- Benchmark Index: Cumulative Return $= +10.0\%$.

1. **Rank Stocks into Decile Buckets**:
   - Winner ($P_1$): Stock A ($+45.0\%$).
   - Neutral ($P_5$): Stock B ($+12.0\%$).
   - Loser ($P_{10}$): Stock C ($-28.0\%$).

2. **Construct Long-Short Zero-Cost Momentum Portfolio**:
   - Long $\$1,000,000$ in Stock A.
   - Short $\$1,000,000$ in Stock C.

3. **Evaluate Performance Over Subsequent 6 Months**:
   - Stock A gains $+18.0\%$ ($+\$180,000$).
   - Stock C loses $-8.0\%$ (Short position gains $+\$80,000$).
   - **Net Portfolio Spread Alpha**:
     $$\text{Gross Return} = +\$180,000 + \$80,000 = +\$260,000\text{ on } \$1,000,000\text{ capital} = +26.0\%$$
   - The momentum factor generated $+26.0\%$ excess spread independent of market direction.

### Example 2: Diagnosing Bearish Market Breadth Divergence

A chief investment officer assesses market internals during a quarterly S&P 500 advance:
- **Month 1**:
  - S&P 500 Index Close: $4,800.00$.
  - NYSE Daily Advancing Issues: $2,200$, Declining Issues: $800$ (Net: $+1,400$).
  - Cumulative A/D Line: $100,000$.
  - New 52-Week Highs: $250$, New Lows: $20$ (Net: $+230$).
  - Stocks Above 200-Day SMA: $72.0\%$.
- **Month 3**:
  - S&P 500 Index Close: $5,100.00$ (New Record High, $+6.25\%$).
  - Cumulative A/D Line: $96,500$ (Net A/D dropped over the quarter).
  - New 52-Week Highs: $65$, New Lows: $140$ (Net: $-75$, New Lows dominate).
  - Stocks Above 200-Day SMA: $38.0\%$ (Majority of stocks in downtrends).

1. **Internal Health Evaluation**:
   - While the capitalization-weighted index rallied by $+6.25\%$, the majority of underlying stocks declined.
   - Net New Highs flipped negative ($-75$).
   - Only $38\%$ of equities trade above their long-term 200-day moving average.

2. **Synthesis and Strategic Action**:
   - **Diagnosis**: Severe Bearish Breadth Divergence (Narrow Leadership).
   - Capital is concentrating exclusively in top mega-cap constituents while the broad market experiences systemic distribution.
   - The portfolio desk tightens stop losses, reduces gross long exposure, and buys index put options ahead of the inevitable distribution resolution.

---

## Pitfalls

- **The Momentum Crash Hazard**:
  Momentum portfolios short the biggest historical losers.
  Following a violent bear market bottom, high-beta, beaten-down losers rebound parabolically, inflicting catastrophic short squeeze drawdowns on momentum strategies.
  Desks must volatility-scale the portfolio or avoid naked short legs during market panics.
- **Confusing High Beta with True Relative Strength**:
  In a roaring bull market, a volatile $2.0$ beta penny stock will naturally outgain a $1.0$ beta index.
  This is cyclical market sensitivity, not genuine alpha.
  True relative strength outgains the market on advancing days and holds firm or rallies during market down days.
- **Ignoring Sector Concentration in Relative Strength**:
  Sorting stocks purely by momentum frequently concentrates the entire long portfolio in a single trending industry (e.g. Energy in 2022, AI Semiconductors in 2023).
  Unconstrained momentum portfolios inadvertently take on enormous sector risk.
- **Relying on Breadth Timing for Exact Daily Turns**:
  Breadth divergences can persist for months before the capitalization-weighted index finally succumbs.
  Prematurely shorting a market with narrow breadth before price breaks structural support results in heavy carry losses.

---

## Interview questions

> [!question]- mkt-ta-097 | What is cross-sectional momentum in quantitative asset pricing?
> The empirical anomaly where assets that performed best relative to peers over the past 3 to 12 months continue to outperform over the subsequent 3 to 12 months.
> First documented by Jegadeesh and Titman (1993), it forms the basis of the academic UMD factor.

> [!question]- mkt-ta-098 | Why do quantitative researchers skip the most recent month (t-1) when constructing 12-month momentum portfolios?
> To avoid contamination from the 1-month short-term reversal anomaly.
> The 1-month reversal is driven by market microstructure friction, bid-ask bounce, and temporary liquidity shocks rather than true fundamental momentum.

> [!question]- mkt-ta-099 | What was the key finding of Asness, Moskowitz, and Pedersen (2013) in "Value and Momentum Everywhere"?
> Momentum is a universal empirical phenomenon present across 8 diverse asset classes and global geographies.
> Because value and momentum are negatively correlated, combining them creates massive Sharpe ratio diversification benefits.

> [!question]- mkt-ta-100 | What is a momentum crash and under what market conditions does it occur?
> A violent, multi-month drawdown in a long-short momentum portfolio where shorted "losers" rally explosively while long "winners" lag.
> Documented by Daniel and Moskowitz (2016), momentum crashes occur at the transition from panic bear market lows into sharp relief recoveries.

> [!question]- mkt-ta-101 | How did Barroso and Santa-Clara (2015) eliminate momentum crash risk?
> By dynamically scaling portfolio exposure inversely to rolling realized momentum volatility (volatility targeting).
> Volatility-scaled momentum nearly doubled the annualized Sharpe ratio and removed left-tail crash drawdowns.

> [!question]- mkt-ta-102 | What is a Relative Strength (RS) ratio line?
> A plot of the ratio of an individual stock's price divided by a benchmark index price: RS = P_stock / P_benchmark.
> A rising slope indicates outperformance; a falling slope indicates underperformance.

> [!question]- mkt-ta-103 | What is Mansfield Relative Strength (RSM)?
> A normalized relative strength indicator developed by Stan Weinstein that calculates the percentage deviation of the RS ratio from its 30-week moving average.
> A transition above zero confirms a Stage 2 breakout.

> [!question]- mkt-ta-104 | In Weinstein Stage Analysis, what are the four stages of a market cycle?
> Stage 1: Basing (Accumulation), Stage 2: Advancing (Uptrend/Markup), Stage 3: Top Area (Distribution), Stage 4: Declining (Downtrend/Markdown).
> Institutional traders restrict long entries exclusively to early Stage 2 breakouts.

> [!question]- mkt-ta-105 | What is William O'Neil's IBD Relative Strength rating?
> A percentile score from 1 to 99 ranking a stock's 12-month performance against all other stocks, weighting the most recent quarter by 40%.
> Leading growth stocks entering sustained advances typically display an RS rating of 80 or higher.

> [!question]- mkt-ta-106 | What is the Cumulative Advance-Decline (A/D) Line?
> A running cumulative sum of daily advancing stocks minus daily declining stocks on an exchange: AD_t = AD_{t-1} + (Advancing - Declining).
> It measures broad market participation independent of capitalization weighting.

> [!question]- mkt-ta-107 | What is a bearish market breadth divergence?
> A condition where major capitalization-weighted indexes (e.g. S&P 500) reach new record highs while breadth indicators (A/D line, Net New Highs) decline.
> It reveals that the rally is being driven by a narrowing band of mega-caps while the majority of equities are deteriorating.

> [!question]- mkt-ta-108 | What is the McClellan Oscillator?
> The difference between the 19-day EMA and the 39-day EMA of net advancing issues on an exchange.
> It quantifies short-term to intermediate-term momentum in market breadth.

> [!question]- mkt-ta-109 | What is a Zweig Breadth Thrust?
> A rare, powerful market breadth signal where the 10-day moving average of advancing stocks divided by total issues surges from below 40% to above 61.5% within 10 trading sessions.
> Developed by Marty Zweig, it reliably signals the launch of major secular bull markets.

> [!question]- mkt-ta-110 | What is the New Highs - New Lows (NH-NL) Index?
> The daily count of stocks reaching new 52-week highs minus those reaching new 52-week lows.
> Expanding new highs confirms broad market strength; expanding new lows in a rising market warns of impending distribution.

> [!question]- mkt-ta-111 | Why does an equal-weighted index (e.g. RSP) outperforming a cap-weighted index (e.g. SPY) signal healthy breadth?
> An equal-weighted index weights every constituent equally (0.2%), meaning its advance reflects broad-based buying across mid and small constituents rather than mega-cap distortion.

> [!question]- mkt-ta-112 | What is the percentage of stocks trading above their 200-day moving average indicator?
> A structural breadth gauge measuring what percentage of an index's components are in secular uptrends.
> Extreme readings below 15% signal washed-out capitulation, while divergences below 50% during index highs indicate severe internal decay.

> [!question]- mkt-ta-113 | What is behavioral under-reaction and how does it explain the momentum anomaly?
> Investors and equity analysts systematically under-react to new fundamental information (e.g. earnings surprises) due to conservatism and anchoring bias.
> Prices adjust gradually to fair value over several months, creating trending momentum.

> [!question]- mkt-ta-114 | What is the disposition effect and how does it sustain price momentum?
> The behavioral tendency of investors to sell winning stocks prematurely to lock in gains and hold losing stocks to avoid admitting losses.
> Excess selling on winners creates temporary resistance, slowing the advance and prolonging subsequent momentum continuation.

> [!question]- mkt-ta-115 | How does factor crowding impact quantitative momentum funds?
> When many funds simultaneously pile into identical top-momentum names, positions become illiquid.
> An unexpected shock forces simultaneous liquidations, triggering sudden cascading momentum drawdowns.

> [!question]- mkt-ta-116 | What is residual momentum?
> Momentum computed from idiosyncratic returns after regressing stock returns against the Fama-French 3-factor or 5-factor model.
> Residual momentum eliminates industry and factor bias, producing higher Sharpe ratios and lower crash risk than raw momentum.

> [!question]- mkt-ta-117 | How does the Arms Index (TRIN) measure market internals?
> TRIN = (Advancing Issues / Declining Issues) / (Advancing Volume / Declining Volume).
> A TRIN below 1.0 indicates strong buying pressure (volume disproportionately in advancing stocks); TRIN above 1.0 indicates selling pressure.

> [!question]- mkt-ta-118 | What is a TRIN capitulation signal?
> An extreme spike in the intraday Arms Index (e.g. TRIN > 3.0 or 4.0) accompanied by heavy downside volume.
> It indicates indiscriminate panic selling and often marks short-term exhaustion bottoms.

> [!question]- mkt-ta-119 | What is sector rotation in equity markets?
> The systematic movement of institutional capital from one industry sector to another according to the stages of the macroeconomic business cycle.
> Relative strength analysis tracks the migration from early-cycle cyclical tech/consumer names to late-cycle defensive utilities/staples.

> [!question]- mkt-ta-120 | What is the High-Low Logic Index?
> The lesser of the percentage of new 52-week highs and new 52-week lows on a given day.
> A high reading indicates market divergence and confusion where both new highs and new lows are elevated simultaneously.

> [!question]- mkt-ta-121 | Why is Relative Strength a leading indicator at market cycle bottoms?
> Institutional accumulation begins in market leaders while the broad index is still printing final panic lows.
> Stocks that refuse to break support during the final index selloff become the primary leaders of the subsequent bull market.

> [!question]- mkt-ta-122 | What is intermediate-term momentum reversal (mean reversion)?
> The tendency for momentum to reverse after 3 to 5 years, where past long-term winners become overvalued and underperform, reverting toward historical fundamental means.
> Documented by De Bondt and Thaler (1985).

> [!question]- mkt-ta-123 | What is post-earnings announcement drift (PEAD) and how does it relate to momentum?
> The empirical finding that stocks announcing positive earnings surprises continue to drift higher for up to 60 days following the announcement.
> PEAD serves as one of the primary micro-drivers underlying medium-term price momentum.

> [!question]- mkt-ta-124 | How does liquidity affect momentum strategy profitability?
> Momentum is strongest among small-cap and illiquid stocks, but high bid-ask spreads and market impact can consume the theoretical alpha.
> Institutional momentum strategies enforce market capitalization and daily volume filters.

> [!question]- mkt-ta-125 | What is cross-sectional vs time-series momentum?
> Cross-sectional momentum ranks assets against each other (relative winners vs losers, zero-net-investment).
> Time-series momentum evaluates an asset's return against its own past return (absolute trend: long positive trend, short negative trend).

> [!question]- mkt-ta-126 | What is the Up/Down Volume Ratio?
> The ratio of volume traded in advancing stocks divided by volume traded in declining stocks over a specified period (e.g. 50 days).
> An Up/Down volume ratio above 1.2 to 1.5 indicates institutional accumulation.

> [!question]- mkt-ta-127 | What is a "breadth thrust" exhaustion signal?
> When market breadth indicators reach extreme overbought levels (> 90% stocks above 50 DMA) and then abruptly roll over.
> It indicates that buying power has been fully exhausted across the entire universe.

> [!question]- mkt-ta-128 | Why do quantitative asset allocators combine Value and Momentum factors?
> Value buys cheap, beaten-down assets with negative momentum, while Momentum buys expensive, high-performing assets with positive trend.
> Because their return streams have an empirical correlation of -0.4 to -0.6, blending them significantly smooths equity curves.

---

## Further reading

- De Bondt, W. F., & Thaler, R. (1985). *Does the stock market overreact?* The Journal of Finance, 40(3), 793-805.
- McClellan, S., & McClellan, M. (1969). *Patterns for Profit: The McClellan Oscillator and Summation Index*. Trade Signals Inc.
- Jegadeesh, N., & Titman, S. (1993). *Returns to buying winners and selling losers: Implications for stock market efficiency*. The Journal of Finance, 48(1), 65-91.
- Fama, E. F., & French, K. R. (2012). *Size, value, and momentum in international stock returns*. Journal of Financial Economics, 105(3), 457-472.
- Asness, C. S., Moskowitz, T. J., & Pedersen, L. H. (2013). *Value and momentum everywhere*. The Journal of Finance, 68(3), 929-985.
- Barroso, P., & Santa-Clara, P. (2015). *Beyond the carry: Momentum has a volatility bug*. Journal of Financial Economics, 116(1), 111-120.
- Daniel, K., & Moskowitz, T. J. (2016). *Momentum crashes*. Journal of Financial Economics, 122(2), 221-247.
