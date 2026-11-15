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

While individual asset price patterns are susceptible to market noise, relative performance across securities carries information that has survived decades of testing.
Cross-sectional momentum - the tendency for stocks that outperformed their peers over the past 3 to 12 months to keep outperforming over the next 3 to 12 months - was documented by Narasimhan Jegadeesh and Sheridan Titman (1993) and has since been replicated across international equities and other asset classes (Fama and French 2012; Asness, Moskowitz, and Pedersen 2013).
In discretionary technical analysis, this phenomenon is evaluated through Relative Strength (RS) ratio lines and market breadth indicators (Advance-Decline statistics, McClellan Oscillators, and High-Low indices) to diagnose the internal health of broad market trends.

---

## TL;DR

Cross-sectional momentum ranks securities across an investment universe by past performance (the common academic version uses the return from month $t-12$ to $t-2$, skipping the most recent month because of short-term reversal) and buys the top group ("winners") while shorting or avoiding the bottom group ("losers").
Relative Strength lines ($P_{\text{asset}} / P_{\text{benchmark}}$) and Mansfield Relative Strength quantify whether a stock is outperforming the benchmark index; practitioners such as O'Neil look for RS lines making new highs before price does.
Market breadth measures the participation of individual constituents within a capitalization-weighted index.
Breadth divergences - where mega-cap indices (e.g. S&P 500, Nasdaq 100) make new record highs driven by a handful of tech giants while the Advance-Decline Line, New Highs-New Lows, and equal-weighted indices deteriorate - are read by breadth analysts as warnings of a narrowing advance; they can persist for months and are not a timing signal.

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

In their 1993 *Journal of Finance* paper, Jegadeesh and Titman examined the relative performance of US equities sorted into deciles based on returns over the past $J$ months ($J \in \{3, 6, 9, 12\}$) and held for $K$ months ($K \in \{3, 6, 9, 12\}$).
They report each strategy both with formation and holding periods back to back and with a one-week gap between them.
The $12-1$ window below is the later convention used for the UMD factor and by Carhart (1997):

1. **Portfolio Construction Protocol ($12-1$ Momentum)**:
   - At month $t$, evaluate the cumulative gross return of each asset $i$ over the 11 months from $t-12$ through $t-2$:
     $$R_i(t-12, t-2) = \prod_{k=2}^{12} (1 + r_{i, t-k}) - 1$$
   - The most recent month $t-1$ is deliberately skipped ("the 1-month skip") because one-month returns tend to reverse (Jegadeesh 1990); bid-ask bounce and liquidity provision are among the proposed explanations.
   - Assets are ranked:
     - Long top decile ($P_1$, "Winners").
     - Short bottom decile ($P_{10}$, "Losers").

2. **Empirical Evidence**:
   - Jegadeesh and Titman (1993) found significant positive returns to buying past 3-to-12-month winners and selling losers over 3-to-12-month holding periods, not explained by systematic risk, with part of the first-year abnormal return dissipating over the following two years.
   - Carhart (1997) added a one-year momentum factor (PR1YR: the 11-month return lagged one month) to the Fama-French three-factor model, giving the four-factor model; the UMD (Up Minus Down) factor is the standard version of it.
   - Fama and French (2012) found momentum returns in North America, Europe and Asia Pacific, though not Japan, that their market, size and value factors do not explain.
   - Asness, Moskowitz, and Pedersen (2013) found value and momentum premia in eight markets and asset classes (US, UK, European and Japanese stocks, equity index futures, government bonds, currencies and commodity futures), with value and momentum negatively correlated within and across asset classes.

```
+---------------------------------------------------------------------------------+
|                         CROSS-SECTIONAL MOMENTUM FORMULATION                    |
|                                                                                 |
|  [ Month t-12 ] ------------ Lookback Window (11 Months) ------------> [ t-1 ]  |
|                                                                        | Skip | |
|                                                                        v  1M  | |
|  Sort Stocks by Cumulative Return ---> Long Top 10% / Short Bottom 10% [ t ]    |
|                                                                                 |
|  Hold Portfolio for Subsequent 3 to 12 Months (Jegadeesh-Titman horizons)       |
+---------------------------------------------------------------------------------+
```

### 2. Relative Strength Metrics in Discretionary Trading

Discretionary practitioners (e.g. Richard Wyckoff, Stan Weinstein, William O'Neil) made relative strength a central stock selection criterion:

1. **The Relative Strength Ratio**:
   $$\text{RS Ratio}_t = \frac{P_t^{\text{stock}}}{P_t^{\text{benchmark}}}$$
   - When the RS ratio is rising, the stock is outperforming the benchmark index; when falling, it is underperforming.
   - **Chartist Principle**: during a broad market correction, practitioners read a stock whose RS line makes a new high while the index makes lower lows as being under accumulation; this is an interpretation, not a tested result.

2. **Mansfield Relative Strength (RSM)**:
   Named after the Mansfield chart service and used by Stan Weinstein in Stage Analysis (Weinstein 1988), the Mansfield RS normalizes the ratio around a zero baseline using an $N$-week moving average of the ratio ($N$ is a chosen lookback, often $52$ weeks):
   $$\text{RSM}_t = \left(\frac{R_t}{\frac{1}{N} \sum_{i=0}^{N-1} R_{t-i}} - 1\right) \times 100, \quad \text{where } R_t = \frac{P_t^{\text{stock}}}{P_t^{\text{benchmark}}}$$
   - Weinstein looks for a stock moving from below zero to above zero as it breaks out of a multi-month base, which he calls a **Stage 2 Breakout**.

3. **William O'Neil's IBD Relative Strength Rating**:
   - A percentile ranking from $1$ to $99$ comparing a stock's performance against all other publicly traded stocks over the trailing 12 months.
   - Investor's Business Daily says the rating weights the most recent quarter more heavily; the exact formula is proprietary, and the "40% / 20% / 20% / 20%" weighting quoted online is a third-party approximation.
   - O'Neil (*How to Make Money in Stocks*) advises buying stocks with an RS rating of $80$ or higher, the top fifth of the ranking.

### 3. Market Breadth and Internal Indicators

Capitalization-weighted indexes (e.g., S&P 500, Nasdaq 100) are dominated by their largest constituent companies.
Market breadth monitors the broad underlying distribution of equities to detect whether rallies are supported by broad participation or disguised by a narrow leadership:

1. **The Advance-Decline (A/D) Line**:
   - Cumulative sum of advancing stocks minus declining stocks on an exchange:
     $$\text{AD Line}_t = \text{AD Line}_{t-1} + (\text{Advancing Issues}_t - \text{Declining Issues}_t)$$
   - In a healthy bull market, the A/D line advances alongside market indexes.
   - **Bearish Breadth Divergence**: the S&P 500 reaches a new record high while the NYSE A/D line fails to reach a new high and trends downward, meaning the advance is narrowing.

2. **The McClellan Oscillator and Summation Index**:
   - Developed by Sherman and Marian McClellan, the oscillator applies exponential moving averages to net advancing issues:
     $$\text{Net Advances}_t = \text{Advancing Issues}_t - \text{Declining Issues}_t$$
     $$\text{McClellan Oscillator}_t = \text{EMA}_{19}(\text{Net Advances}_t) - \text{EMA}_{39}(\text{Net Advances}_t)$$
   - The 19-day and 39-day EMAs use smoothing constants $0.10$ and $0.05$, from $\alpha = 2 / (N + 1)$, the EMA whose mean lag matches an $N$-day SMA.
   - The **McClellan Summation Index** is the cumulative sum of daily oscillator values, used as a longer-term breadth gauge.
   - **Zweig Breadth Thrust** (Zweig 1986, *Winning on Wall Street*): the 10-day average of advances / (advances + declines) rises from below $40\%$ to above $61.5\%$ within 10 trading days.
   - Zweig presented it as a rare bullish signal; with so few signals in history, its record is anecdotal, and no peer-reviewed test is cited here.

3. **New 52-Week Highs minus New Lows (NH - NL)**:
   - Measures extreme performance across the market:
     $$\text{Net New Highs}_t = \text{New 52w Highs}_t - \text{New 52w Lows}_t$$
   - Breadth analysts read persistently positive net new highs as broad participation.
   - If indexes rally while new 52-week lows expand, they read it as a narrowing, divergent market; the threshold that counts as "expanding" is a parameter, not a known constant.

### 4. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                       EVIDENCE LEDGER: MOMENTUM & BREADTH                       |
+---------------------------------------------------------------------------------+
|  Phenomenon: Cross-Sectional Momentum & Market Breadth Divergence               |
|  Evidence Grade: STRONG for momentum, WEAK/UNTESTED for breadth timing          |
+---------------------------------------------------------------------------------+
|  Key Empirical Studies:                                                         |
|  1. Jegadeesh and Titman (1993, Journal of Finance):                            |
|     - Buying 3-12 month winners and selling losers earns significant returns    |
|       over 3-12 month holds, not explained by systematic risk.                  |
|  2. Asness, Moskowitz, and Pedersen (2013, Journal of Finance):                 |
|     - "Value and Momentum Everywhere": premia in 8 markets and asset classes.   |
|     - Value and momentum are negatively correlated, so a combination            |
|       diversifies.                                                              |
|  3. Daniel and Moskowitz (2016, Journal of Financial Economics):                |
|     - "Momentum Crashes": isolated the structural left-tail risk of momentum.   |
|     - Crashes come in panic states, after market declines and with high         |
|       volatility, as the market rebounds and past losers rally.                 |
|  4. Barroso and Santa-Clara (2015, Journal of Financial Economics):             |
|     - "Momentum Has Its Moments": scaling momentum to constant risk virtually   |
|       eliminates crashes and nearly doubles the Sharpe ratio.                   |
+---------------------------------------------------------------------------------+
|  Counter-Evidence & Failure Modes:                                              |
|  1. High Turnover and Execution Drag:                                           |
|     - Lesmond, Schill, and Zhou (2004) argued momentum returns are concentrated |
|       in illiquid, high-cost small stocks where transaction costs erase alpha.  |
|  2. Factor Crowding and Liquidity Shocks:                                       |
|     - Quant equity long-short strategies suffered sharp losses in the August    |
|       2007 unwind (Khandani and Lo 2011, Journal of Financial Markets).         |
+---------------------------------------------------------------------------------+
```

---

## Worked examples

### Example 1: Calculating Cross-Sectional Momentum Return and Ranking

A quantitative equity researcher illustrates the ranking with three hypothetical stocks at month $t$:
- Stock A (Tech): Cumulative Return $t-12$ to $t-2 = +45.0\%$.
- Stock B (Consumer): Cumulative Return $t-12$ to $t-2 = +12.0\%$.
- Stock C (Energy): Cumulative Return $t-12$ to $t-2 = -28.0\%$.
- Benchmark Index: Cumulative Return $= +10.0\%$.

1. **Rank Stocks**:
   - In a real universe these would fall into deciles; here A stands for the winner decile ($P_1$), B for the middle, and C for the loser decile ($P_{10}$).

2. **Construct Long-Short Zero-Cost Momentum Portfolio**:
   - Long $\$1,000,000$ in Stock A.
   - Short $\$1,000,000$ in Stock C.

3. **Evaluate Performance Over Subsequent 6 Months (hypothetical)**:
   - Stock A gains $+18.0\%$ ($+\$180,000$).
   - Stock C loses $-8.0\%$ (Short position gains $+\$80,000$).
   - **Net Portfolio Spread**:
     $$\text{Gross P\&L} = +\$180,000 + \$80,000 = +\$260,000$$
   - Per dollar long and dollar short that is a spread return of $18.0\% - (-8.0\%) = 26.0\%$ before costs and borrow fees.
   - The spread is market-neutral only if the two legs have equal beta; a high-beta winner leg adds market exposure.

### Example 2: Diagnosing Bearish Market Breadth Divergence

A chief investment officer assesses market internals during a quarterly S&P 500 advance (hypothetical figures):
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
   - While the capitalization-weighted index rallied by $+6.25\%$, the cumulative A/D line fell by $3,500$, so declines outnumbered advances over the quarter.
   - Net New Highs flipped negative ($-75$).
   - Only $38\%$ of equities trade above their long-term 200-day moving average.

2. **Synthesis and Strategic Action**:
   - **Diagnosis**: Severe Bearish Breadth Divergence (Narrow Leadership).
   - The advance is concentrated in the largest constituents while most stocks weaken.
   - A desk that acts on it might tighten stops or hedge; breadth divergences can persist for months, so the reading is about risk, not a dated forecast.

---

## Pitfalls

- **The Momentum Crash Hazard**:
  Momentum portfolios short the biggest historical losers.
  Daniel and Moskowitz (2016) show crashes occur in panic states, after market declines and with high volatility, when beaten-down losers rebound with the market.
  Volatility scaling (Barroso and Santa-Clara 2015) or dynamic weighting (Daniel and Moskowitz 2016) reduces that exposure.
- **Confusing High Beta with True Relative Strength**:
  In a roaring bull market, a volatile $2.0$ beta penny stock will naturally outgain a $1.0$ beta index.
  This is cyclical market sensitivity, not genuine alpha.
  True relative strength outgains the market on advancing days and holds firm or rallies during market down days.
- **Ignoring Sector Concentration in Relative Strength**:
  Sorting stocks purely by momentum can concentrate the long portfolio in a single trending industry.
  Moskowitz and Grinblatt (1999) found that industry momentum accounts for much of individual-stock momentum, so unconstrained portfolios carry large industry bets.
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
> One-month returns tend to reverse (Jegadeesh 1990), an effect commonly attributed to bid-ask bounce and temporary liquidity shocks rather than to information.

> [!question]- mkt-ta-099 | What was the key finding of Asness, Moskowitz, and Pedersen (2013) in "Value and Momentum Everywhere"?
> Value and momentum premia appear in all eight markets and asset classes they study, with a strong common factor structure.
> Value and momentum are negatively correlated within and across asset classes, so combining them improves risk-adjusted returns.

> [!question]- mkt-ta-100 | What is a momentum crash and under what market conditions does it occur?
> A violent, multi-month drawdown in a long-short momentum portfolio where shorted "losers" rally explosively while long "winners" lag.
> Daniel and Moskowitz (2016) show they occur in panic states, following market declines and when volatility is high, contemporaneous with market rebounds.

> [!question]- mkt-ta-101 | How did Barroso and Santa-Clara (2015) reduce momentum crash risk?
> By scaling exposure inversely to the momentum portfolio's recent realized volatility, targeting constant risk.
> They report that this virtually eliminates crashes and nearly doubles the Sharpe ratio of the momentum strategy.

> [!question]- mkt-ta-102 | What is a Relative Strength (RS) ratio line?
> A plot of the ratio of an individual stock's price divided by a benchmark index price: RS = P_stock / P_benchmark.
> A rising slope indicates outperformance; a falling slope indicates underperformance.

> [!question]- mkt-ta-103 | What is Mansfield Relative Strength (RSM)?
> A normalized relative strength indicator, named after the Mansfield chart service and used by Stan Weinstein, that measures the percentage deviation of the RS ratio from its own N-week moving average (52 weeks is a common choice).
> Weinstein looks for a move above zero alongside a Stage 2 breakout.

> [!question]- mkt-ta-104 | In Weinstein Stage Analysis, what are the four stages of a market cycle?
> Stage 1: Basing (Accumulation), Stage 2: Advancing (Uptrend/Markup), Stage 3: Top Area (Distribution), Stage 4: Declining (Downtrend/Markdown).
> Weinstein (1988) advises buying in early Stage 2 and avoiding Stage 4.

> [!question]- mkt-ta-105 | What is William O'Neil's IBD Relative Strength rating?
> A percentile score from 1 to 99 ranking a stock's 12-month performance against all other stocks, with the most recent quarter weighted more heavily (the exact formula is proprietary).
> O'Neil advises buying only stocks rated 80 or higher.

> [!question]- mkt-ta-106 | What is the Cumulative Advance-Decline (A/D) Line?
> A running cumulative sum of daily advancing stocks minus daily declining stocks on an exchange: AD_t = AD_{t-1} + (Advancing - Declining).
> It measures broad market participation independent of capitalization weighting.

> [!question]- mkt-ta-107 | What is a bearish market breadth divergence?
> A condition where major capitalization-weighted indexes (e.g. S&P 500) reach new record highs while breadth indicators (A/D line, Net New Highs) decline.
> It reveals that the rally is being driven by a narrowing band of mega-caps while the majority of equities are deteriorating.

> [!question]- mkt-ta-108 | What is the McClellan Oscillator?
> The difference between the 19-day EMA and the 39-day EMA of net advancing issues on an exchange (smoothing constants 0.10 and 0.05).
> It quantifies short-term to intermediate-term momentum in market breadth.

> [!question]- mkt-ta-109 | What is a Zweig Breadth Thrust?
> Marty Zweig's (1986) signal: the 10-day average of advances / (advances + declines) rises from below 40% to above 61.5% within 10 trading days.
> Zweig presented it as a rare bullish signal; with few signals in history its record is anecdotal, and no peer-reviewed test is cited here.

> [!question]- mkt-ta-110 | What is the New Highs - New Lows (NH-NL) Index?
> The daily count of stocks reaching new 52-week highs minus those reaching new 52-week lows.
> Expanding new highs confirms broad market strength; expanding new lows in a rising market warns of impending distribution.

> [!question]- mkt-ta-111 | Why does an equal-weighted index (e.g. RSP) outperforming a cap-weighted index (e.g. SPY) signal healthy breadth?
> An equal-weighted index gives every constituent the same weight at each rebalance (1/500 = 0.2% in a 500-stock index), so its return reflects the average stock rather than the largest ones.
> Equal-weight beating cap-weight means the average constituent is outperforming the mega-caps, a sign of broader participation.

> [!question]- mkt-ta-112 | What is the percentage of stocks trading above their 200-day moving average indicator?
> A structural breadth gauge measuring what percentage of an index's components are in secular uptrends.
> Very low readings are read as washed-out conditions and a falling reading during index highs as narrowing participation; the cut-offs are parameters to test, not known constants.

> [!question]- mkt-ta-113 | What is behavioral under-reaction and how does it explain the momentum anomaly?
> One explanation (Barberis, Shleifer, and Vishny 1998; Hong and Stein 1999): investors under-react to new information because of conservatism or slow information diffusion.
> Prices then adjust gradually over several months, producing momentum; risk-based explanations compete with this view.

> [!question]- mkt-ta-114 | What is the disposition effect and how does it sustain price momentum?
> The behavioral tendency of investors to sell winning stocks prematurely to lock in gains and hold losing stocks to avoid admitting losses.
> Grinblatt and Han (2005, Journal of Financial Economics) model how this selling pressure keeps winners below fundamental value, so prices underreact and momentum follows.

> [!question]- mkt-ta-115 | How does factor crowding impact quantitative momentum funds?
> When many funds simultaneously pile into identical top-momentum names, positions become illiquid.
> An unexpected shock forces simultaneous liquidations, triggering sudden cascading momentum drawdowns.

> [!question]- mkt-ta-116 | What is residual momentum?
> Momentum computed from residual returns after regressing stock returns on the Fama-French three factors.
> Blitz, Huij, and Martens (2011, Journal of Empirical Finance) found it has much less time-varying factor exposure than total-return momentum and earned higher risk-adjusted profits in their sample.

> [!question]- mkt-ta-117 | How does the Arms Index (TRIN) measure market internals?
> TRIN = (Advancing Issues / Declining Issues) / (Advancing Volume / Declining Volume).
> A TRIN below 1.0 indicates strong buying pressure (volume disproportionately in advancing stocks); TRIN above 1.0 indicates selling pressure.

> [!question]- mkt-ta-118 | What is a TRIN capitulation signal?
> An extreme spike in the Arms Index accompanied by heavy downside volume.
> Practitioners read it as indiscriminate selling and a possible short-term low; the spike level used is a parameter, and no peer-reviewed test is cited here.

> [!question]- mkt-ta-119 | What is sector rotation in equity markets?
> The systematic movement of institutional capital from one industry sector to another according to the stages of the macroeconomic business cycle.
> Relative strength analysis is used to see which sectors are leading; the textbook business-cycle sequence of sector leadership is a stylized model, not a reliable timetable.

> [!question]- mkt-ta-120 | What is the High-Low Logic Index?
> Norman Fosback's indicator: the lesser of new 52-week highs and new 52-week lows, each as a percentage of issues traded, on a given day.
> A high reading means both new highs and new lows are elevated at once, a divided market.

> [!question]- mkt-ta-121 | Why is Relative Strength a leading indicator at market cycle bottoms?
> The practitioner view (O'Neil, Weinstein): stocks that hold up during the final index selloff often lead the next advance.
> That is an observation from practitioner books, not a tested result; momentum crashes (Daniel and Moskowitz 2016) show past losers often lead the first rebound instead.

> [!question]- mkt-ta-122 | What is long-term reversal, and who documented it?
> The tendency for multi-year winners to underperform multi-year losers over the following years.
> De Bondt and Thaler (1985) found that portfolios of prior 36-month losers outperformed prior 36-month winners over the next 36 months, which they attributed to overreaction.

> [!question]- mkt-ta-123 | What is post-earnings announcement drift (PEAD) and how does it relate to momentum?
> The finding that stocks with positive earnings surprises keep drifting up (and negative ones down) after the announcement; Bernard and Thomas (1989) measured it over the 60 trading days that follow.
> Chan, Jegadeesh, and Lakonishok (1996) found that price momentum and earnings momentum each predict returns and are only partly the same effect.

> [!question]- mkt-ta-124 | How does liquidity affect momentum strategy profitability?
> Lesmond, Schill, and Zhou (2004) argued momentum profits concentrate in high-cost stocks, where trading costs can consume them.
> Institutional momentum strategies enforce market capitalization and daily volume filters.

> [!question]- mkt-ta-125 | What is cross-sectional vs time-series momentum?
> Cross-sectional momentum ranks assets against each other (relative winners vs losers, zero-net-investment).
> Time-series momentum evaluates an asset's return against its own past return (absolute trend: long positive trend, short negative trend); Moskowitz, Ooi, and Pedersen (2012) documented it in 58 futures and forward contracts.

> [!question]- mkt-ta-126 | What is the Up/Down Volume Ratio?
> The ratio of volume traded in advancing stocks divided by volume traded in declining stocks over a specified period (e.g. 50 days).
> Practitioners read a ratio persistently above 1 as accumulation; any specific cut-off is a parameter to test.

> [!question]- mkt-ta-127 | What is a "breadth thrust" exhaustion signal?
> When a breadth indicator such as the share of stocks above their 50-day average reaches an extreme high and then rolls over.
> Breadth analysts read it as exhausted buying; the extreme level is a parameter, and no peer-reviewed test is cited here.

> [!question]- mkt-ta-128 | Why do quantitative asset allocators combine Value and Momentum factors?
> Value buys cheap, beaten-down assets with negative momentum, while Momentum buys expensive, high-performing assets with positive trend.
> Asness, Moskowitz, and Pedersen (2013) found their returns negatively correlated within and across asset classes, so a blend has lower volatility than either alone.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_ta_04_momentum_breadth.py`](../../code/mkt_ta_04_momentum_breadth.py) prints and asserts every number on this page: the 12-1 window by enumerating month offsets (with the compounded return checked against a log-return sum on a seeded series), the long-short example by marking explicit share positions on each leg, the breadth arithmetic in exact rational numbers, and the McClellan smoothing constants by matching the EMA's explicit-weight mean lag and its measured delay on a ramp to the SMA lag; Zweig's thresholds are cited constants.
- Related notes: [Time-Series Momentum and Trend Following](07-Time-Series-Momentum-and-Trend-Following.md), [Dow Theory and Trend Evidence](01-Dow-Theory-and-Trend-Evidence.md).

## Further reading

- De Bondt, W. F., & Thaler, R. (1985). *Does the stock market overreact?* The Journal of Finance, 40(3), 793-805.
- Jegadeesh, N. (1990). *Evidence of predictable behavior of security returns*. The Journal of Finance, 45(3), 881-898.
- Bernard, V. L., & Thomas, J. K. (1989). *Post-earnings-announcement drift: Delayed price response or risk premium?* Journal of Accounting Research, 27(Supplement), 1-36.
- Chan, L. K. C., Jegadeesh, N., & Lakonishok, J. (1996). *Momentum strategies*. The Journal of Finance, 51(5), 1681-1713.
- Moskowitz, T. J., & Grinblatt, M. (1999). *Do industries explain momentum?* The Journal of Finance, 54(4), 1249-1290.
- Barberis, N., Shleifer, A., & Vishny, R. (1998). *A model of investor sentiment*. Journal of Financial Economics, 49(3), 307-343.
- Hong, H., & Stein, J. C. (1999). *A unified theory of underreaction, momentum trading, and overreaction in asset markets*. The Journal of Finance, 54(6), 2143-2184.
- Grinblatt, M., & Han, B. (2005). *Prospect theory, mental accounting, and momentum*. Journal of Financial Economics, 78(2), 311-339.
- Lesmond, D. A., Schill, M. J., & Zhou, C. (2004). *The illusory nature of momentum profits*. Journal of Financial Economics, 71(2), 349-380.
- Blitz, D., Huij, J., & Martens, M. (2011). *Residual momentum*. Journal of Empirical Finance, 18(3), 506-521.
- Khandani, A. E., & Lo, A. W. (2011). *What happened to the quants in August 2007? Evidence from factors and transactions data*. Journal of Financial Markets, 14(1), 1-46.
- Moskowitz, T. J., Ooi, Y. H., & Pedersen, L. H. (2012). *Time series momentum*. Journal of Financial Economics, 104(2), 228-250.
- Weinstein, S. (1988). *Stan Weinstein's Secrets for Profiting in Bull and Bear Markets*. Dow Jones-Irwin.
- Zweig, M. (1986). *Winning on Wall Street*. Warner Books.
- Jegadeesh, N., & Titman, S. (1993). *Returns to buying winners and selling losers: Implications for stock market efficiency*. The Journal of Finance, 48(1), 65-91.
- Carhart, M. M. (1997). *On persistence in mutual fund performance*. The Journal of Finance, 52(1), 57-82.
- Fama, E. F., & French, K. R. (2012). *Size, value, and momentum in international stock returns*. Journal of Financial Economics, 105(3), 457-472.
- Asness, C. S., Moskowitz, T. J., & Pedersen, L. H. (2013). *Value and momentum everywhere*. The Journal of Finance, 68(3), 929-985.
- Barroso, P., & Santa-Clara, P. (2015). *Momentum has its moments*. Journal of Financial Economics, 116(1), 111-120.
- Daniel, K., & Moskowitz, T. J. (2016). *Momentum crashes*. Journal of Financial Economics, 122(2), 221-247.
