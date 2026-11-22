---
type: concept
title: "Dow Theory, Trend Definition, and Empirical Evidence"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [technical-analysis, dow-theory, trend-following, moving-averages, support-resistance, evidence-based]
prereqs: []
---

# Dow Theory, Trend Definition, and Empirical Evidence

Dow Theory grew out of editorials Charles H. Dow wrote in *The Wall Street Journal* before his death in 1902.
Dow read the averages as a barometer of business conditions rather than as a short-term speculation system.
William Peter Hamilton (*The Stock Market Barometer*, 1922) and Robert Rhea (*The Dow Theory*, 1932) codified the editorials into "Dow Theory," introducing primary trends, confirmation between averages, the role of volume, and trend persistence.
This note states the classical tenets, gives algorithmic trend definitions, and summarizes what the peer-reviewed evidence on trend rules actually found.

---

## TL;DR

Dow Theory asserts that the averages discount known information and move in three concurrent trends: primary (under a year to several years), secondary (reactions of weeks to months), and minor (day-to-day noise).
A valid primary trend requires confirmation between complementary averages (historically, the Dow Jones Industrial Average and the Dow Jones Transportation Average) and confirmation by trading volume.
Modern quantitative definitions model trends as sequences of Higher Highs (HH) and Higher Lows (HL) or through moving average filters (e.g., 50-day and 200-day simple moving averages).
Brock, Lakonishok, and LeBaron (1992) found that on the DJIA from 1897 to 1986, returns after moving-average buy signals exceeded returns after sell signals, inconsistent with four standard null models, before transaction costs.
Sullivan, Timmermann, and White (1999) found the best rule in a 7,846-rule universe survived a data-snooping correction in that sample but did not outperform in the 1987-1996 post-sample decade.

---

## Learning objectives

- Analyze the six tenets commonly used to summarize classical Dow Theory and their economic underpinnings.
- Formulate mathematical and algorithmic definitions of price trends and structural pivot points.
- Evaluate the empirical performance of moving average filters against benchmark buy-and-hold portfolios.
- Evaluate support and resistance structures through market microstructure and behavioral anchoring models.
- Identify the structural failure modes of classical trend rules in sideways and volatile whipsaw environments.

---

## Core concepts

### 1. The Six Tenets of Classical Dow Theory

Textbook summaries condense the writings of Dow, Hamilton (1922), and Rhea (1932) into six tenets:

1. **The Averages Discount Everything**:
   - The averages reflect the combined knowledge and expectations of everyone in the market, so anticipated events are already in the price.
   - Rhea's statement excludes "acts of God" such as fires and earthquakes, which the averages cannot anticipate but appraise quickly once they happen.

2. **The Market Has Three Distinct Trends**:
   - **Primary Trend**: The broad secular tide lasting from under a year to several years, reflecting underlying economic expansions or contractions.
   - **Secondary (Intermediate) Reaction**: Rhea (1932) describes these as corrections against the primary trend that usually last three weeks to three months and retrace $33\%$ to $66\%$ of the primary move since the last reaction.
   - **Minor (Day-to-Day) Fluctuations**: Short-term oscillations lasting hours to days; Dow considered minor moves susceptible to manipulation and essentially random noise.

3. **Primary Trends Have Three Distinct Phases**:
   - **Phase 1: Accumulation**: Astute institutional capital quietly buys from distressed sellers when economic news is grim and valuations are severely depressed.
   - **Phase 2: Public Participation**: Improving corporate earnings and business conditions attract widespread trend followers and retail investors; prices appreciate rapidly.
   - **Phase 3: Distribution**: Informed institutional money begins unwinding positions into peak public optimism as speculative retail participation surges.

4. **The Averages Must Confirm Each Other**:
   - In Dow's era, industrial companies manufactured physical goods, while railroads transported them to markets.
   - A healthy economic expansion required that the Dow Jones Railroad (Transportation) Average confirm a new high set by the Dow Jones Industrial Average.
   - Dow theorists read a divergence (Industrials make a new high while Transports fail to confirm) as a warning that the primary trend may reverse; it is a warning to test, not a forecast with a measured hit rate.

5. **Volume Must Confirm the Trend**:
   - Volume should expand in the direction of the primary trend and contract during counter-trend secondary pullbacks.
   - In a primary bull market, Dow theorists expect volume to rise on advancing sessions and fall on down days, and they read falling volume on new price highs as exhaustion; that reading is a hypothesis, not a tested result.

6. **A Trend Remains in Effect Until Definite Reversal Signals Occur**:
   - The theory presumes a trend persists until the averages give a reversal signal; it does not estimate how likely continuation is.
   - A reversal is not called until both averages break their prior swing lows (in a bull market).

```
+---------------------------------------------------------------------------------+
|                       DOW THEORY PRIMARY BULL TREND STRUCTURE                   |
|                                                                                 |
|                                                HH3                              |
|                                                /\                               |
|                                               /  \                              |
|                                       HH2    /    \                             |
|                                       /\    /                                   |
|                                      /  \  /                                    |
|                              HH1    /    \/                                     |
|                              /\    /     HL2                                    |
|                             /  \  /                                             |
|                            /    \/                                              |
|                           /     HL1                                             |
|                          /                                                      |
|                                                                                 |
|  HH = swing high above the prior high; HL = swing low above the prior low       |
|  Accumulation ---> Public Participation ---> Distribution / Climax              |
+---------------------------------------------------------------------------------+
```

### 2. Algorithmic Trend Definitions and Moving Average Filters

In modern quantitative practice, subjective chart reading is replaced by objective algorithmic rules:

1. **Swing Pivot Highs and Lows**:
   - A bar at time $t$ with high $H_t$ is an $N$-bar swing high if:
     $$H_t > \max(H_{t-N}, \dots, H_{t-1}) \quad \text{and} \quad H_t > \max(H_{t+1}, \dots, H_{t+N})$$
   - An uptrend is strictly defined as a verified sequence where:
     $$\text{High}_k > \text{High}_{k-1} \quad \text{and} \quad \text{Low}_k > \text{Low}_{k-1}$$
   - A structural trend break occurs when price crosses below the most recent verified swing low $\text{Low}_k$.

2. **Simple Moving Average (SMA) Rule**:
   - The $L$-day simple moving average at time $t$ is:
     $$\text{SMA}_t(L) = \frac{1}{L} \sum_{i=0}^{L-1} P_{t-i}$$
   - Binary signal rule:
     $$\text{Signal}_t = \begin{cases} +1 & \text{if } P_t > \text{SMA}_t(L) \\ 0 & \text{if } P_t \le \text{SMA}_t(L) \end{cases}$$
   - A common choice is $L = 200$ trading days, about $9.5$ months at 21 trading days a month (a 10-month SMA on monthly closes is a similar filter).

3. **Dual Moving Average Crossover**:
   - Fast moving average $\text{SMA}(S)$ and slow moving average $\text{SMA}(L)$ ($S < L$, commonly 50-day and 200-day):
     - **Golden Cross**: $\text{SMA}(50)$ crosses above $\text{SMA}(200)$ (bullish signal).
     - **Death Cross**: $\text{SMA}(50)$ crosses below $\text{SMA}(200)$ (bearish signal).

### 3. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                               EVIDENCE LEDGER: DOW & TREND                      |
+---------------------------------------------------------------------------------+
|  Phenomenon: Moving-Average Filters and the Dow Theory Record                   |
|  Evidence Grade: MIXED (in-sample support, weak post-sample)                    |
+---------------------------------------------------------------------------------+
|  Key Empirical Studies:                                                         |
|  1. Brock, Lakonishok, and LeBaron (1992, Journal of Finance):                  |
|     - 26 moving-average and trading-range-break rules on the DJIA, 1897-1986.   |
|     - Buy signals consistently earned more than sell signals; returns after     |
|       sell signals were negative; bootstrap rejected four null models           |
|       (random walk, AR(1), GARCH-M, EGARCH). Returns are before costs.          |
|  2. Lo, Mamaysky, and Wang (2000, Journal of Finance):                          |
|     - Kernel-regression pattern detection on US stocks, 1962-1996: several      |
|       patterns shift the conditional return distribution (incremental info).    |
|  3. Brown, Goetzmann, and Kumar (1998, Journal of Finance):                     |
|     - Re-analysed Hamilton's editorial calls, 1902-1929: positive risk-adjusted |
|       returns, reversing Cowles' conclusion once risk is accounted for.         |
+---------------------------------------------------------------------------------+
|  Counter-Evidence & Caveats:                                                    |
|  1. Cowles (1933, Econometrica):                                                |
|     - Concluded that following Hamilton's editorials did not beat a continuous  |
|       holding of stocks (no adjustment for the lower risk of time in cash).     |
|  2. Sullivan, Timmermann, and White (1999, Journal of Finance):                 |
|     - Best of 7,846 rules survived the data-snooping test in the 1897-1986      |
|       sample but did not outperform in the 1987-1996 post-sample decade.        |
|  3. Whipsaws: in range-bound markets the rule buys high and sells low.          |
+---------------------------------------------------------------------------------+
```

### 4. Mechanics of Support and Resistance

Support and resistance are price levels where buying or selling pressure concentrates sufficiently to halt or reverse price direction:

1. **Behavioral Anchoring**:
   - Traders who bought at a prior peak and suffered a subsequent drawdown experience regret.
   - When price returns to their entry level, some exit "at breakeven," adding supply near the old peak (overhead resistance).
   - Traders who missed an advance may treat previous breakout levels as second-chance entries, adding demand there (support).
   - This is a behavioral hypothesis; Osler (2000, FRBNY Economic Policy Review) found that support and resistance levels published by foreign exchange firms predicted intraday trend interruptions better than arbitrary levels, though the effect was modest.

2. **Order Clustering at Psychological Round Numbers**:
   - Osler (2003, Journal of Finance) found, in a dealing bank's currency order book, that take-profit orders cluster at round numbers and stop-loss orders cluster just beyond them.
   - Her explanation: take-profit clusters tend to halt trends at round numbers, while triggered stop-loss clusters tend to accelerate a move once a round number is crossed.

---

## Worked examples

### Example 1: Calculating 200-Day Moving Average Timing on an Index

An asset allocator tests a 200-day simple moving average timing rule on the S&P 500 index (hypothetical levels):
- Current Index Close: $P_t = \$4,950.00$.
- Sum of prior 200 trading day closing prices: $\sum_{i=0}^{199} P_{t-i} = \$980,000.00$.

1. **Calculate 200-Day Simple Moving Average**:
   $$\text{SMA}_{200} = \frac{\$980,000.00}{200} = \$4,900.00$$

2. **Evaluate Allocation Signal**:
   $$P_t = \$4,950.00 > \text{SMA}_{200} = \$4,900.00$$
   The index trades $+1.02\%$ above its 200-day SMA.
   The model issues a $+1$ (Fully Invested) signal.

3. **Assess Whipsaw Risk**:
   - Assume the SMA stays near $\$4,900.00$ over the next week (one week of closes moves a 200-day average only slightly).
   - If the index drops by $2.0\%$ to $\$4,851.00$, price crosses below the SMA, triggering a shift to $0$ (Cash/T-bills).
   - If the market immediately rebounds to $\$4,920.00$, the strategy repurchases above its sale price: it ends with $4,851 / 4,920$ of a unit, a whipsaw loss of $-1.4\%$ against simply holding.

### Example 2: Dow Theory Intermarket Confirmation Analysis

A macro strategist assesses market health using closing prices across two consecutive quarters (hypothetical levels):
- **Dow Jones Industrial Average (DJIA)**:
  - January Peak: $38,000$.
  - March Retracement: $36,800$.
  - May Rally Close: $39,200$ (New Primary High, $+3.16\%$ above January peak).
- **Dow Jones Transportation Average (DJTA)**:
  - January Peak: $16,000$.
  - March Retracement: $15,200$.
  - May Rally Close: $15,750$ (Fails to breach January peak, $-1.56\%$ below).

1. **Dow Theory Evaluation**:
   - Industrials established a definitive new high ($39,200 > 38,000$).
   - Transports failed to confirm, forming a lower high ($15,750 < 16,000$).
   - **Diagnosis**: Bearish Dow Divergence (Non-Confirmation).
   - Under classical Dow Theory, the new high in Industrials is unconfirmed, so the theory treats the primary uptrend as suspect; this is the theory's reading, not a tested forecast.

---

## Pitfalls

- **The Whipsaw Capital Drain in Consolidation Regimes**:
  In a range-bound market, moving averages oscillate through the center of the price distribution.
  Trend-following rules buy at the top of the range and sell at the bottom, compounding consecutive execution losses.
- **Confirmation Latency (Lagging Indicator Nature)**:
  Dow Theory requires secondary reaction lows to form and break before confirming a primary reversal.
  Consequently, classical Dow signals arrive only after a meaningful part of the new primary trend has already occurred.
- **Obsolescence of the Transports Analogy in Modern Economies**:
  In a service- and software-driven economy, freight is a much smaller part of output than in 1900, so the industrial-transport link is weaker.
  Practitioners who still want cross-market confirmation often look at credit spreads or other cyclical indexes instead; such substitutes need their own testing.
- **Survivorship Bias in Historical Chartist Books**:
  Popular trading literature showcases hand-picked charts where trends persisted cleanly for hundreds of points.
  Without systematic point-in-time backtesting across all failed patterns, chart analysis creates severe overconfidence.
- **Ignoring Transaction Costs and Data-Snooping**:
  Brock, Lakonishok, and LeBaron (1992) report returns before costs; a rule that trades often can lose its in-sample edge to costs and to selection from many rules, as Sullivan, Timmermann, and White (1999) showed post-sample.

---

## Interview questions

> [!question]- mkt-ta-001 | Who originated Dow Theory and what was its original purpose?
> Charles H. Dow, in Wall Street Journal editorials written before his death in 1902; Hamilton (1922) and Rhea (1932) codified them.
> Dow read the averages as a barometer of business conditions, not as a short-term speculation system.

> [!question]- mkt-ta-002 | What are the three orders of market trends identified by Dow Theory?
> Primary trend (under a year to several years), secondary reaction (Rhea: usually three weeks to three months), and minor day-to-day fluctuations.
> The theory treats minor fluctuations as noise that is not worth forecasting.

> [!question]- mkt-ta-003 | Explain the three phases of a Dow Theory primary bull market.
> Accumulation (informed money buys from distressed sellers), public participation (rising earnings attract broad participation), and distribution (informed money unloads into speculative euphoria).

> [!question]- mkt-ta-004 | What is the principle of confirmation in Dow Theory?
> A primary trend signal in one market average must be confirmed by a corresponding move in a complementary average (e.g. Industrials and Transports).
> Divergence between the averages warns of structural trend exhaustion.

> [!question]- mkt-ta-005 | How did Dow Theory explain the economic link between Industrials and Transports?
> Industrial companies produce goods, and transportation companies deliver them to market.
> If goods are being manufactured but freight shipments are falling, goods are accumulating in inventory, which the theory reads as a warning of contraction.

> [!question]- mkt-ta-006 | What is the role of trading volume in Dow Theory?
> Volume must expand in the direction of the primary trend and contract on secondary pullbacks.
> The theory reads diminishing volume on new price highs as waning participation; volume is a secondary confirmation, never a signal on its own.

> [!question]- mkt-ta-007 | What is the mathematical definition of an uptrend in price action?
> A sequential series of Higher Highs (HH) and Higher Lows (HL) in price structure.
> An uptrend remains valid until price breaks below the most recent structural higher low.

> [!question]- mkt-ta-008 | What is the 200-day Simple Moving Average (SMA) rule?
> A binary trend filter that holds the asset when price closes above its 200-day SMA and moves to cash when price closes below.
> It is a common baseline trend rule; Brock, Lakonishok, and LeBaron (1992) included the 1-day/200-day crossover among their 26 rules.

> [!question]- mkt-ta-009 | What did Brock, Lakonishok, and LeBaron (1992) find regarding moving average rules?
> On the DJIA from 1897 to 1986, their 26 moving-average and trading-range-break rules showed buy-signal returns consistently above sell-signal returns, and returns after sell signals were negative.
> Bootstrapped p-values rejected four null models (random walk, AR(1), GARCH-M, EGARCH); the returns are before transaction costs.

> [!question]- mkt-ta-010 | Why does a 200-day SMA timing rule show lower full-period volatility than buy-and-hold even when it has no forecasting skill?
> Mechanically: it sits in cash part of the time, and time in cash contributes almost no variance, so measured volatility falls whatever the timing quality.
> Whether risk-adjusted returns improve depends on whether the out-of-market periods really had lower returns, which needs a test net of costs and data-snooping.

> [!question]- mkt-ta-011 | What did Alfred Cowles (1933) conclude about William Peter Hamilton's Dow Theory editorials, and how was it later revised?
> Cowles concluded that following Hamilton's calls did not beat a continuous holding of stocks.
> Brown, Goetzmann, and Kumar (1998, Journal of Finance) re-analysed the record for 1902 to 1929 and found high Sharpe ratios and positive alphas once the lower risk of time out of the market is accounted for.

> [!question]- mkt-ta-012 | What is a whipsaw in trend following?
> A false breakout or rapid oscillation around a moving average where a trader buys high and sells low in rapid succession.
> Consecutive whipsaw losses create severe equity drawdowns in non-trending regimes.

> [!question]- mkt-ta-013 | What is a Golden Cross and Death Cross?
> A Golden Cross occurs when a fast moving average (e.g. 50-day) crosses above a slow moving average (e.g. 200-day).
> A Death Cross occurs when the fast moving average crosses below the slow moving average.

> [!question]- mkt-ta-014 | Why is support and resistance explained by behavioral anchoring?
> Market participants anchor on past trade prices; traders who suffered drawdowns seek to sell at breakeven, creating resistance.
> Traders who missed an initial advance place limit orders at former breakout levels, creating support.

> [!question]- mkt-ta-015 | What is polarity change in technical analysis?
> The chartist principle that once broken, a major support level becomes future resistance, and broken resistance becomes support.
> The proposed mechanism is anchoring and order clustering at former levels; it is a rule of thumb, not a tested regularity.

> [!question]- mkt-ta-016 | What is order clustering at psychological round numbers?
> The tendency for orders to concentrate at round price levels.
> Osler (2003, Journal of Finance) found take-profit orders clustered at round numbers and stop-loss orders just beyond them in a bank's currency order book, which she used to explain trend reversals at, and accelerations through, round numbers.

> [!question]- mkt-ta-017 | Why do classical trend-following strategies exhibit positive skewness (right-tail asymmetry)?
> By cutting losses quickly on false breakouts and letting profitable trends run, trend followers capture rare large gains while bounding individual losses.
> Fung and Hsieh (2001, Review of Financial Studies) modelled trend-follower returns as portfolios of lookback straddles, which share that convex payoff.

> [!question]- mkt-ta-018 | What is the main structural weakness of using Dow's Transportation Average today?
> Freight transport is a much smaller part of a service-dominated modern economy than of the 1900 economy, so the industrial-transport link is weaker.
> Any substitute confirmation series (credit spreads, other cyclical indexes) has to be tested, not assumed.

> [!question]- mkt-ta-019 | What is a trailing stop in trend trading?
> A dynamic stop-loss order that ratchets higher as the asset advances, maintaining a fixed dollar, percentage, or volatility distance below current market price.
> It protects accumulated profits while allowing the trend to continue unconstrained.

> [!question]- mkt-ta-020 | What is Average True Range (ATR) and how is it used in trend following?
> J. Welles Wilder's (1978) volatility measure: the average of the true range TR = max(H - L, |H - C_prev|, |L - C_prev|), which includes overnight gaps; Wilder used 14 periods.
> Trend traders set stop distances and position sizes as multiples of ATR (for example 2x ATR).

> [!question]- mkt-ta-021 | What did Sullivan, Timmermann, and White (1999) conclude regarding technical trading rules?
> They applied White's Reality Check to a universe of 7,846 technical rules on the Dow Jones Industrial Average.
> Over Brock, Lakonishok, and LeBaron's 1897-1986 sample, the best rule stayed significant even after the data-snooping adjustment.
> Over the 1987-1996 out-of-sample decade, the best rule delivered no statistically significant outperformance.

> [!question]- mkt-ta-022 | What is a trendline and what constitutes a valid algorithmic trendline?
> A line connecting sequential swing lows in an uptrend or swing highs in a downtrend.
> Two pivots define the line; chartists treat a third pivot touching it, with no intervening bar closing through it, as confirmation (pivots on one line are collinear by construction).

> [!question]- mkt-ta-023 | What is a false breakout (bear trap / bull trap)?
> A brief price thrust beyond a well-defined support or resistance boundary that fails to attract sustained volume and violently reverses.
> One documented mechanism is a cluster of triggered stop-loss orders that exhausts itself (Osler 2003); attributing every failed break to deliberate stop-hunting is folklore.

> [!question]- mkt-ta-024 | Explain the difference between an exponential moving average (EMA) and a simple moving average (SMA).
> An SMA assigns equal mathematical weight (1/N) to all observations in the lookback window.
> An EMA assigns exponentially decaying weights, reacting more rapidly to recent price changes: EMA_t = alpha * P_t + (1 - alpha) * EMA_{t-1}.
> With alpha = 2 / (N + 1) the EMA's mean lag, (1 - alpha) / alpha, equals the (N - 1) / 2 lag of an N-period SMA.

> [!question]- mkt-ta-025 | Why does a simple moving average suffer from the "drop-off effect"?
> When a large price spike exits the lookback window N days later, the SMA jumps or drops even if current price is completely stationary.
> EMAs avoid the drop-off effect by smoothly decaying past historical prices.

> [!question]- mkt-ta-026 | What is the lag of a simple moving average?
> The average time delay of an N-period SMA is (N - 1) / 2 periods.
> A 200-day moving average lags a steadily trending price by (200 - 1) / 2 = 99.5 trading days.

> [!question]- mkt-ta-027 | How does Lo, Mamaysky, and Wang (2000) evaluate technical patterns quantitatively?
> They smooth prices with nonparametric kernel regression, detect patterns from the sequence of local extrema, and compare the distribution of returns after each pattern with the unconditional distribution using goodness-of-fit and Kolmogorov-Smirnov tests.
> On US stocks from 1962 to 1996 several patterns provided incremental information; they did not show the patterns are profitable after costs.

> [!question]- mkt-ta-028 | What is time-frame alignment in multi-timeframe trend analysis?
> Requiring that the primary trend (e.g. weekly chart), intermediate trend (daily chart), and execution timeframe (hourly chart) agree in direction before taking a trade.
> It is meant to filter out counter-trend trades; whether it helps a given rule has to be tested.

> [!question]- mkt-ta-029 | What is a secular bull market versus a cyclical bull market?
> A secular bull market is a long, multi-year rise in valuations and prices spanning several business cycles.
> A cyclical bull market is a shorter advance tied to one business cycle, which can occur inside either a secular bull or a secular bear market; neither term has a fixed length.

> [!question]- mkt-ta-030 | Why does a moving average rule underperform during low-volatility grinding bull markets?
> Because the asset remains continuously above its moving average, the timing rule simply matches buy-and-hold while occasionally incurring false exit whipsaws on brief dips.
> Any value a moving average rule adds comes from the periods it is out of the market, mainly prolonged declines.

> [!question]- mkt-ta-031 | What is a Donchian Channel?
> A band plotted using the highest high and lowest low over an N-period lookback window: Upper = max(H, N), Lower = min(L, N).
> A close beyond a band is a classic breakout entry; the Turtle Traders' rules described by Faith (2007) used channel breakouts of this kind.

> [!question]- mkt-ta-032 | What is the risk-adjusted benefit of a trend-following overlay on equity portfolios?
> It can cut exposure during prolonged declines, which shortens the left tail of the portfolio's drawdown distribution.
> The cost is whipsaw losses and late re-entry; the size of the benefit depends on the sample and must be measured net of costs.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_ta_01_dow_trend.py`](../../code/mkt_ta_01_dow_trend.py) prints and asserts every number on this page: the SMA, the price gap, the 2% drop and the Dow confirmation percentages in exact rational arithmetic, the whipsaw loss by simulating the sell-and-rebuy account (cross-checked by log returns), the SMA lag both as the window's weighted age and as the measured delay behind a linear ramp, and the EMA smoothing constant whose explicit geometric weights give the same mean lag, and the bull-trend chart rendered from a swing list on which the higher-high, higher-low rule is asserted; study samples are cited constants.
- Related notes: [Chart Patterns and Statistical Edge](02-Chart-Patterns-and-Statistical-Edge.md), [Time-Series Momentum and Trend Following](07-Time-Series-Momentum-and-Trend-Following.md).

## Further reading

- Dow, C. H. Editorials in *The Wall Street Journal* (written before his death in 1902).
- Hamilton, W. P. (1922). *The Stock Market Barometer*. Harper & Brothers.
- Rhea, R. (1932). *The Dow Theory: An Explanation of Its Development and an Attempt to Define Its Usefulness as an Aid in Speculation*. Barron's.
- Cowles, A. (1933). *Can stock market forecasters forecast?* Econometrica, 1(3), 309-324.
- Brock, W., Lakonishok, J., & LeBaron, B. (1992). *Simple technical trading rules and the stochastic properties of stock returns*. The Journal of Finance, 47(5), 1731-1764.
- Sullivan, R., Timmermann, A., & White, H. (1999). *Data-snooping, technical trading rule performance, and the bootstrap*. The Journal of Finance, 54(5), 1647-1691.
- Lo, A. W., Mamaysky, H., & Wang, J. (2000). *Foundations of technical analysis: Computational algorithms, statistical inference, and empirical implementation*. The Journal of Finance, 55(4), 1705-1765.
- Brown, S. J., Goetzmann, W. N., & Kumar, A. (1998). *The Dow Theory: William Peter Hamilton's track record reconsidered*. The Journal of Finance, 53(4), 1311-1333.
- Osler, C. L. (2000). *Support for resistance: Technical analysis and intraday exchange rates*. Federal Reserve Bank of New York Economic Policy Review, 6(2), 53-68.
- Osler, C. L. (2003). *Currency orders and exchange rate dynamics: An explanation for the predictive success of technical analysis*. The Journal of Finance, 58(5), 1791-1819.
- Fung, W., & Hsieh, D. A. (2001). *The risk in hedge fund strategies: Theory and evidence from trend followers*. The Review of Financial Studies, 14(2), 313-341.
- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*. Trend Research.
- Faith, C. M. (2007). *Way of the Turtle*. McGraw-Hill.
