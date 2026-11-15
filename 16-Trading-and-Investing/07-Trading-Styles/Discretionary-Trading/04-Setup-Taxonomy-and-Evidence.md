---
type: concept
title: "Trade Setup Taxonomy, Evidence Grading, and Academic Verification"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [trade-setups, evidence-grading, momentum, mean-reversion, brock-lakonishok, lo-mamaysky-wang]
prereqs: []
---

# Trade Setup Taxonomy, Evidence Grading, and Academic Verification

Financial markets folklore is crowded with hundreds of named chart patterns, candlestick formations, and discretionary setups.
Most retail trading education presents these patterns as immutable laws of nature without providing empirical proof, sample sizes, or transaction-cost accounting.
A professional quantitative or discretionary trader subjects every setup to rigorous taxonomy and academic evidence grading.
Every claimed pattern must be classified by its structural economic mechanism, tested across decades of out-of-sample data, and graded with complete transparency.

---

## TL;DR

- Trading setups fall into four primary structural archetypes: Trend Following Breakouts, Trend Pullbacks, Mean Reversion, and Event-Driven Catalysts.
- Markets Mastery OS evaluates every setup using an Evidence Grade: STRONG, MIXED, WEAK, REFUTED, or UNTESTED.
- Time-series momentum (Moskowitz, Ooi and Pedersen 2012, 58 futures markets) and cross-sectional momentum (Jegadeesh and Titman 1993 in US stocks; Asness, Moskowitz and Pedersen 2013 across asset classes) have the strongest replicated evidence of the setups here.
- Classical technical rules fare worse once data snooping is accounted for: Aronson (2006) found none of 6,402 rules significant on the S&P 500, and the best of Sullivan, Timmermann and White's (1999) rules did not outperform out of sample.

---

## Learning objectives

- Classify trading setups into the four foundational structural archetypes.
- Apply the Markets Mastery OS five-tier Evidence Grading Framework (STRONG, MIXED, WEAK, REFUTED, UNTESTED).
- Analyze landmark peer-reviewed studies on technical rules (Brock et al. 1992, Lo et al. 2000, Moskowitz et al. 2012).
- Identify the economic drivers (behavioral under-reaction, institutional flow, structural rebalancing) behind genuine market anomalies.
- Formulate testable entry, invalidation, and exit criteria for systematic breakout and pullback setups.

---

## Core concepts

### 1. The Four Foundational Setup Archetypes

Every valid trade setup operates on one of four underlying market mechanisms:

1. **Trend Following / Momentum Breakouts**:
   - **Mechanism**: Exploits institutional capital reallocation and behavioral under-reaction to fundamental news.
   - **Market Context**: Expansion from low-volatility consolidation into an aggressive directional trend.
   - **Classic Examples**: Donchian Channel breakouts, Darvas Boxes, Mark Minervini's Volatility Contraction Pattern (VCP), Stan Weinstein Stage 2 breakouts.
   - **Payoff Profile**: Usually a low win rate with a large average win relative to the average loss (positive skew); measure the actual numbers on your own trades.

2. **Trend Pullbacks / Continuation**:
   - **Mechanism**: Liquidity replenishment inside an established higher-timeframe trend.
   - **Market Context**: Counter-trend retracement toward institutional support zones (e.g. 20-day EMA, anchored VWAP, prior breakout retest).
   - **Classic Examples**: Bull flags, flat base retests, high-tight flags, moving average pullbacks.
   - **Payoff Profile**: Between the other two archetypes: a tighter stop near the pullback low gives a higher reward-to-risk than mean reversion, with a higher win rate than raw breakouts if the trend persists.

3. **Mean Reversion / Range Trading**:
   - **Mechanism**: Compensation for liquidity provision during transient order flow imbalances or inventory exhaustion.
   - **Market Context**: Price reaches extreme statistical boundaries in non-trending or range-bound regimes.
   - **Classic Examples**: Bollinger Band mean reversion, RSI oversold/overbought extremes, statistical arbitrage pairs cointegration.
   - **Payoff Profile**: Usually a high win rate with a small average win relative to the average loss (negative skew), vulnerable to large losses when a range turns into a trend or price gaps.

4. **Event-Driven Catalysts / Structural Arbitrage**:
   - **Mechanism**: Liquidity demand created by mandatory institutional mandates or binary information disclosures.
   - **Classic Examples**: Post-Earnings Announcement Drift (PEAD), Russell 2000 annual rebalancing, S&P 500 additions/deletions, biotech PDUFA approvals.
   - **Payoff Profile**: Event-specific and often asymmetric, requiring fundamental and regulatory modeling of the event itself.

### 2. The Five-Tier Evidence Grading Framework

Markets Mastery OS assigns every setup an Evidence Grade based on peer-reviewed literature and out-of-sample replication.
The grades and their $t$-statistic bands are this curriculum's own convention, not an industry standard; the $t \ge 3.0$ bar follows Harvey, Liu and Zhu (2016):

| Grade | Definition | Academic / Empirical Standard |
|-------|------------|-------------------------------|
| **STRONG** | Persistent anomaly replicated across markets and decades after costs. | Replicated by independent researchers, out of sample and across asset classes where applicable; survives multiple testing corrections ($t \ge 3.0$). |
| **MIXED** | Edge exists in specific asset classes or historical regimes, but decays after costs, out of sample, or with parameter changes. | Statistically significant gross return ($t \ge 2.0$) that falls short of the STRONG bar after costs, out of sample, or across parameters. |
| **WEAK** | Lacks statistical significance out-of-sample or fails to beat a naive random-walk benchmark after transaction fees. | Marginal evidence; performance indistinguishable from data-mining noise ($t < 2.0$ out of sample). |
| **REFUTED** | Empirically disproven; strategies following the pattern systematically lose money after transaction costs. | Peer-reviewed studies demonstrate zero predictive power or negative post-cost returns. |
| **UNTESTED** | Discretionary folklore lacking formal mathematical definition or backtestable verification. | Promoted in popular retail media without reproducible quantitative evidence. |

### 3. Landmark Academic Evidence on Trading Rules

#### 1. Time-Series Momentum (Moskowitz, Ooi, and Pedersen, 2012) - Grade: STRONG
- Documented time-series momentum (trend following) in each of the 58 liquid equity index, currency, commodity and bond futures they studied.
- An instrument's own past 12-month excess return predicts its return over the next 1 to 12 months, with partial reversal at longer horizons.
- A diversified time-series momentum portfolio earned substantial abnormal returns with little exposure to standard asset-pricing factors, and it performed best in extreme markets.

#### 2. Cross-Sectional Momentum (Jegadeesh and Titman, 1993) - Grade: STRONG
- Buying past 3-to-12 month US stock winners and selling past losers (top and bottom deciles) earned significant positive returns over 3 to 12 month holding periods from 1965 to 1989.
- The strategy they examine in most detail (6-month formation, 6-month holding) earned a compounded excess return of 12.01% per year, not explained by systematic risk.
- Rouwenhorst (1998) found the same effect in 12 European markets, and Asness, Moskowitz and Pedersen (2013) found momentum in every asset class they studied.

#### 3. Moving Average Rules and Breakouts (Brock, Lakonishok, and LeBaron, 1992) - Grade: MIXED
- Tested 26 moving average crossover and trading range breakout rules on the Dow Jones Industrial Average from 1897 to 1986.
- Buy signals consistently generated higher returns than sell signals, and returns after buy signals were less volatile than returns after sell signals, a pattern that bootstrapped random-walk, AR(1), GARCH-M and EGARCH null models did not reproduce.
- The study ignored transaction costs and tested an index that cannot itself be traded.
- Sullivan, Timmermann, and White (1999) tested these rules inside a universe of 7,846 rules with White's Reality Check.
- The best rule stayed significant over the 1897-1986 sample even after the data-snooping adjustment, but delivered no significant outperformance over the 1987-1996 out-of-sample decade.

#### 4. Automated Pattern Recognition (Lo, Mamaysky, and Wang, 2000) - Grade: MIXED
- Used kernel regression to define and detect ten classical patterns objectively (head-and-shoulders and its inverse, broadening, triangle, rectangle and double tops and bottoms).
- Across a large sample of US stocks from 1962 to 1996, several patterns shifted the conditional distribution of subsequent returns, so they carried incremental information, especially for Nasdaq stocks.
- The paper measured information content, not trading profits, and computed no returns net of costs, so it does not show the patterns are profitable to trade.

#### 5. Data Snooping and Multiple Testing Bias (Aronson, 2006; Harvey, Liu, and Zhu, 2016)
- David Aronson (2006) tested 6,402 technical trading rules on the S&P 500 index from 1980 to 2005, correcting for data snooping with White's Reality Check and a Monte Carlo permutation test.
- None of the 6,402 rules had a back-tested mean return high enough to reject the null hypothesis of no predictive power at the 5% level once the search over all rules was accounted for.
- Harvey, Liu, and Zhu (2016) argued that, given the hundreds of factors already tested, a newly discovered factor needs a $t$-statistic of at least $3.0$ (two-sided $p = 0.0027$) rather than $2.0$.

---

## Worked examples

### Example 1: Formulating a Volatility Contraction Pattern (VCP)

Mark Minervini's Volatility Contraction Pattern (VCP), described in *Trade Like a Stock Market Wizard* (2013), is a base in which successive pullbacks get smaller and volume dries up before a breakout.
A quantitative ruleset converts this discretionary setup into an objective, testable algorithm.
Every threshold below is this example's illustrative choice, to be tested out of sample, not a value from Minervini or from any study:

1. **Trend Template Filter**:
   - Stock price $P_t > \text{SMA}_{50} > \text{SMA}_{150} > \text{SMA}_{200}$.
   - Current price within $15\%$ of 52-week high.
2. **Contraction Sequence**:
   - Wave 1 (Initial Retracement): Price pulls back from peak by $20\%$ to $25\%$.
   - Wave 2 (Secondary Retracement): Price rallies, then pulls back by $10\%$ to $12\%$.
   - Wave 3 (Terminal Contraction): Price rallies, then pulls back by only $3\%$ to $5\%$ over 3 to 7 days.
   - Range contraction condition: $\text{ATR}_{14}(t) \le 0.50 \times \text{ATR}_{14}(t - 30)$.
3. **Volume Exhaustion**:
   - Volume on the terminal contraction days drops below $50\%$ of the 50-day average volume:
     $$\text{Volume}_t < 0.50 \times \text{SMA}_{50}(\text{Volume})$$
4. **Execution and Invalidation Trigger**:
   - Buy Trigger: Price crosses above the high of the terminal contraction on expanding volume ($> 1.50 \times \text{SMA}_{50}(\text{Volume})$).
   - Invalidation Stop: Set exactly at the low of the terminal contraction ($P_{\text{stop}} = L_{\text{terminal}}$).
   - Initial Risk: The stop sits below a terminal pullback of $3\%$ to $5\%$, so initial risk is a few percent of price; a target of $3R$ to $5R$ then needs a move of only about $9\%$ to $25\%$.

### Example 2: Evaluating Evidence Grades Across Setup Candidates

A quantitative discretionary desk audits four proposed trading setups:

1. **Setup A: 12-Month Time-Series Momentum in Crude Oil and S&P 500 Futures**:
   - Academic Evidence: Moskowitz, Ooi, and Pedersen (2012) document time-series momentum in each of their 58 futures markets, including equity index and commodity futures, and Hurst, Ooi and Pedersen (2017) extend trend-following evidence back to 1880.
   - Assigned Grade: **STRONG**.
   - Action: Approved for allocation with volatility targeting, after the desk's own cost-inclusive backtest.

2. **Setup B: 2-Day RSI < 10 Mean Reversion in S&P 500 Stocks**:
   - Evidence: short-horizon reversal in individual US stocks is documented in peer-reviewed work (Lehmann 1990 for weekly returns, Jegadeesh 1990 for monthly returns), but the specific short-period RSI rules come from practitioner backtests (Connors and Alvarez 2008) that are not peer-reviewed or corrected for data snooping, and short-horizon reversal profits are small relative to trading costs.
   - Assigned Grade: **MIXED**.
   - Action: Approved only for paper trading until the desk's own out-of-sample, cost-inclusive test is done.

3. **Setup C: Head-and-Shoulders Top Chart Pattern on 5-Minute Forex Charts**:
   - Academic Evidence: Lo, Mamaysky, and Wang (2000) tested daily US stock data, not intraday FX, and measured information content, not net profits; no study cited here tests this setup.
   - Assigned Grade: **UNTESTED**.
   - Action: Rejected for live trading until tested; intraday spreads make the bar for net profitability high.

4. **Setup D: Fibonacci Time Zone Cycle Reversal**:
   - Academic Evidence: no peer-reviewed test is known to this curriculum, and the rule's dates are chosen by the chartist, so it is hard to define without look-ahead.
   - Assigned Grade: **UNTESTED**.
   - Action: Discarded unless someone can define it objectively and test it.

---

## Pitfalls

- **Data Snooping / Selection Bias**:
  Testing 100 moving average crossover pairs and selecting the best one on a single asset inflates its apparent edge.
  If all 100 rules have no edge and independent $t$-statistics, the best of them has an expected $t$ of $2.51$, and at least one shows $|t| > 2$ with probability $99.1\%$.
- **Regime Blindness**:
  Trend breakout setups make most of their money in persistent trends and give it back in whipsaws when markets range, so a backtest over one regime says little about the other.
- **Visual Chart Cherry-Picking**:
  People readily see patterns in random data; Roberts (1959) showed that simulated random-walk price charts look like real ones, complete with apparent patterns.
  A chartist who remembers the textbook winners and forgets the failures has run an uncorrected multiple-testing experiment.
- **Ignoring Execution Costs in Intraday Setups**:
  A mean-reversion setup with an average gross gain of 8 basis points loses $8 - 10 = -2$ basis points per trade after a 10-basis-point round-trip spread and clearing cost.

---

## Interview questions

> [!question]- mkt-trd-097 | What are the four foundational structural archetypes of trade setups?
> 1. Trend Following / Momentum Breakouts.
> 2. Trend Pullbacks / Continuation.
> 3. Mean Reversion / Range Trading.
> 4. Event-Driven Catalysts / Structural Arbitrage.

> [!question]- mkt-trd-098 | What are the five tiers of the Markets Mastery OS Evidence Grading Framework?
> STRONG (replicated across markets and decades after costs, t >= 3.0).
> MIXED (significant gross return, t >= 2.0, but short of the STRONG bar after costs, out of sample, or across parameters).
> WEAK (lacks statistical significance out-of-sample, t < 2.0).
> REFUTED (disproven; systematically loses money net of costs).
> UNTESTED (discretionary folklore lacking quantitative verification).

> [!question]- mkt-trd-099 | What was the central empirical discovery of Moskowitz, Ooi, and Pedersen (2012) regarding Time Series Momentum?
> An instrument's own past 12-month excess return predicts its return over the next 1 to 12 months, in each of the 58 liquid equity index, currency, commodity and bond futures studied, with partial reversal at longer horizons.
> A diversified time-series momentum portfolio earned substantial abnormal returns with little exposure to standard factors and performed best during extreme markets.

> [!question]- mkt-trd-100 | What did Jegadeesh and Titman (1993) prove regarding cross-sectional momentum in equities?
> Buying the top decile of 3-to-12 month past US stock winners and selling the bottom decile of past losers earned significant returns over 1965 to 1989; their main 6-month/6-month strategy earned a compounded excess return of 12.01% per year, not explained by systematic risk.
> Later work replicated it in European stocks (Rouwenhorst 1998) and across asset classes (Asness, Moskowitz and Pedersen 2013).

> [!question]- mkt-trd-101 | What were the findings of Brock, Lakonishok, and LeBaron (1992) regarding technical trading rules on the Dow Jones?
> Across 26 moving average and trading range breakout rules on the DJIA from 1897 to 1986, returns after buy signals were consistently higher than after sell signals, and less volatile, before transaction costs.
> Bootstrapped random-walk, AR(1), GARCH-M and EGARCH null models did not reproduce these differences.

> [!question]- mkt-trd-102 | Why did Sullivan, Timmermann, and White (1999) question the real-world tradability of Brock et al.'s findings?
> Inside a universe of 7,846 rules, the best rule survived White's Reality Check over the original 1897-1986 sample.
> It then delivered no statistically significant outperformance over the 1987-1996 out-of-sample decade, so the in-sample edge did not carry forward, and trading costs only widen that gap.

> [!question]- mkt-trd-103 | How did Lo, Mamaysky, and Wang (2000) formalize technical chart pattern analysis?
> They used non-parametric kernel regression to smooth prices and then defined ten classical patterns (such as head-and-shoulders and double bottoms) as rules on the smoothed extrema.
> On US stocks from 1962 to 1996, several patterns shifted the conditional return distribution, evidence of incremental information, but the paper did not test whether trading them is profitable after costs.

> [!question]- mkt-trd-104 | What is data snooping bias (p-hacking) as documented by David Aronson (2006)?
> Testing many rule variants on the same historical dataset and keeping the best, whose apparent performance then overstates its expected future performance.
> Aronson tested 6,402 rules on the S&P 500 (1980 to 2005) and, after correcting for the search with White's Reality Check and a permutation test, found none significant at the 5% level; without such a correction (or Hansen's SPA test) the best backtest is not evidence.

> [!question]- mkt-trd-105 | What is the t-statistic threshold established by Harvey, Liu, and Zhu (2016) for modern factor discovery?
> t >= 3.0 (a two-sided p-value of 0.0027 or less), raised from the conventional t >= 2.0 threshold.
> The higher hurdle accounts for the hundreds of candidate factors mined and tested across the financial literature over recent decades.

> [!question]- mkt-trd-106 | What is Mark Minervini's Volatility Contraction Pattern (VCP)?
> A pattern characterized by progressive contractions in price volatility (e.g. 25% drop, then 10%, then 3%) accompanied by drying volume before a breakout.
> Minervini (2013) reads it as supply being absorbed before a breakout; that reading is practitioner judgment, not a peer-reviewed finding, so the grade is UNTESTED until you test a precise definition.

> [!question]- mkt-trd-107 | What is the behavioral explanation for the persistence of momentum in financial markets?
> Leading models attribute it to under-reaction from conservatism (Barberis, Shleifer and Vishny 1998), overconfidence and biased self-attribution followed by later correction (Daniel, Hirshleifer and Subrahmanyam 1998), or slow diffusion of information across investors (Hong and Stein 1999).
> All three predict continuation over months followed by partial long-run reversal, which matches the evidence.

> [!question]- mkt-trd-108 | Why do breakout setups have low win rates (30% to 40%) but high profitability?
> False breakouts are frequent, so most trades are small 1R losses; the few that become sustained trends produce large multiples of R.
> Profitability needs the average win to clear the break-even ratio: at a 35% win rate the average win must exceed 0.65 / 0.35 = 1.86R before costs.

> [!question]- mkt-trd-109 | What is Post-Earnings Announcement Drift (PEAD) discovered by Ball and Brown (1968)?
> The tendency of a stock's cumulative abnormal returns to drift in the direction of an earnings surprise for weeks or months following the announcement date.
> Ball and Brown (1968) first reported it and Bernard and Thomas (1989) established it as an anomaly, attributing it mainly to a delayed price response to the earnings news.

> [!question]- mkt-trd-110 | What is a Stage 2 breakout in Stan Weinstein's market stage framework?
> The transition of a stock from a prolonged sideways consolidation base (Stage 1) into an advancing uptrend (Stage 2) above a rising 30-week moving average.
> Weinstein (1988, *Secrets for Profiting in Bull and Bear Markets*) recommends buying the Stage 2 breakout; that is his method, not a tested result.

> [!question]- mkt-trd-111 | Explain the concept of Anchored VWAP (AVWAP) and why it acts as dynamic support/resistance.
> AVWAP calculates the Volume Weighted Average Price starting from a specific significant historical anchor point (e.g. earnings release, market crash low, 52-week high).
> It is the average price of all volume traded since the anchor, a rough proxy for the cost basis of recent buyers, not their exact cost basis (every trade has a buyer and a seller, and positions opened earlier are excluded); its role as support or resistance is a practitioner hypothesis.

> [!question]- mkt-trd-112 | What is a bull flag and what are its quantitative criteria?
> A sharp, high-volume upward price thrust (the flagpole) followed by a tight, downward-sloping consolidation on declining volume.
> There is no standard definition; a testable version must fix the numbers, for example (hypothetically) a retracement of at most 50% of the pole with volume below its 20-day average.

> [!question]- mkt-trd-113 | What is pareidolia in manual discretionary chart analysis?
> The human psychological tendency to perceive meaningful patterns or order in random visual noise.
> Roberts (1959, Journal of Finance) showed that charts of simulated random walks display the head-and-shoulders and other "patterns" chartists look for, so seeing a pattern is not evidence of predictability.

> [!question]- mkt-trd-114 | What is the typical payoff profile of a mean-reversion trading strategy?
> Usually a high win rate with average wins smaller than average losses (negative skew), so a run of good months says little about the tail.
> When a range turns into a trend, a mean-reversion system without timely exits keeps fading the move and its losses escalate.

> [!question]- mkt-trd-115 | What is Donchian Channel breakout trading?
> A systematic trend-following rule that buys when price breaks above the highest high of the past N days (e.g. 20 or 55 days) and sells when price breaks the lowest low.
> It is the entry rule of the Turtle system (20-day breakouts in System 1, 55-day in System 2, as published by Faith 2007), a fully mechanical trend-following rule.

> [!question]- mkt-trd-116 | How does market regime (trending vs range-bound) impact the performance of breakout setups?
> Breakout setups earn most of their profit in persistent trends.
> In choppy, range-bound regimes, breakouts suffer whipsaws as prices revert from channel boundaries, so evaluate them over samples that contain both regimes.

> [!question]- mkt-trd-117 | What is the Russell 2000 annual rebalancing anomaly?
> The Russell US indexes reconstitute membership from updated market capitalizations; the event was annual in June, and from 2026 it is semi-annual, in June and December (the first December reconstitution is effective after the close on 11 December 2026, per FTSE Russell's 1 September 2026 announcement).
> Index funds must buy additions and sell deletions on a known date, and Madhavan (2003, Financial Analysts Journal) documented the resulting price pressure around reconstitution, which traders try to anticipate.

> [!question]- mkt-trd-118 | Why is volume expansion mandatory to confirm a genuine technical breakout?
> It is not proven mandatory: volume confirmation is a practitioner filter, and the evidence on volume is indirect.
> Gervais, Kaniel and Mingelgrin (2001, Journal of Finance) found that stocks with unusually high trading volume over a day or week tend to rise over the following month, which supports treating volume as information but does not show that low-volume breakouts fail.

> [!question]- mkt-trd-119 | What is relative strength (RS) in equity momentum trading?
> A measure of an individual stock's price performance compared to a broad benchmark index (e.g. S&P 500) over a 3-to-12 month window.
> George and Hwang (2004, Journal of Finance) found that stocks trading near their 52-week highs subsequently outperform, and that nearness to the 52-week high explains much of momentum's profit.

> [!question]- mkt-trd-120 | What is a false breakout (bull trap) and how does it trap buyers?
> Price punches above a prominent resistance level, triggering retail breakout buy orders and short stop-losses, but immediately fails and closes back inside the range.
> Breakout buyers who now hold losing positions sell at their stops, which can speed the move back down; how often that happens is an empirical question, not a given.

> [!question]- mkt-trd-121 | In statistical arbitrage, what is the cointegration test used to identify mean-reverting pairs?
> The Engle-Granger two-step method or Johansen test evaluating whether a linear combination of two non-stationary time series is stationary (I(0)).
> If the series are cointegrated, the spread is stationary (constant mean, finite variance); the estimated relationship can still break out of sample, so monitor it.

> [!question]- mkt-trd-122 | What is a Darvas Box?
> A consolidation rectangle set by a new high that is not exceeded for three consecutive days (the ceiling) and a low that holds for three days (the floor).
> Described by Nicolas Darvas in *How I Made $2,000,000 in the Stock Market* (1960): buy on a breakout above the ceiling with a stop just below it.

> [!question]- mkt-trd-123 | What is a moving average crossover whipsaw?
> Successive false trend signals generated when an asset oscillates sideways across the moving average lines.
> Each crossover triggers an entry that is promptly reversed at a loss, causing rapid capital attrition during consolidating regimes.

> [!question]- mkt-trd-124 | What is the economic rationale for the value factor anomaly (Fama and French, 1993)?
> Cheap stocks (high book-to-market) earn higher average returns; Fama and French read the premium as compensation for distress risk, while Lakonishok, Shleifer and Vishny (1994) attribute it to investors extrapolating past bad news.
> Either way the premium is earned over multi-year horizons and can be negative for long stretches.

> [!question]- mkt-trd-125 | What is an opening range breakout (ORB)?
> Taking a directional position when price breaks above the high or below the low established during the first 15 or 30 minutes of the trading session.
> The rule assumes the opening range captures early price discovery and that a break signals the session's direction; that is a hypothesis to test, and the Market Profile "initial balance" is a different window (the first hour).

> [!question]- mkt-trd-126 | Why do candlestick reversal patterns (e.g. hammer, shooting star) have WEAK standalone evidence?
> The peer-reviewed tests that exist are negative: Marshall, Young and Rose (2006, Journal of Banking and Finance) found that candlestick trading strategies did not create value for Dow Jones Industrial Average stocks.
> Without a replicated positive result after costs, the grade cannot be higher than WEAK.

> [!question]- mkt-trd-127 | What is the high-tight flag setup and what is its historical track record?
> A very sharp advance (practitioner definitions use roughly a doubling within a few weeks) followed by a short, shallow consolidation; the exact numbers differ between authors.
> Its reputation comes from practitioner books, not peer-reviewed tests, so under this framework it is UNTESTED until a precise definition is backtested after costs.

> [!question]- mkt-trd-128 | Why must every quantitative or discretionary playbook document objective invalidation rules for each setup?
> Without unambiguous invalidation criteria, traders fall prey to narrative rationalization and holding losing trades indefinitely.
> Pre-registered rules keep planned risk at 1R, preserving capital to capture the next edge-positive trial.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_trd_04_setups.py`](../../code/mkt_trd_04_setups.py) prints and asserts every number on this page: the Harvey-Liu-Zhu p-value by the error function and by Simpson quadrature of the normal density, the expected best $t$ among 100 null rules by numerical integration of the maximum's distribution checked by seeded simulation within five standard errors, the chance of at least one $|t| > 2$ by the closed form and by simulation, the VCP target moves, and the break-even payoff ratio by bisection; study results are cited constants.
- Related notes: [Chart Patterns and Statistical Edge](../Technical-Analysis/02-Chart-Patterns-and-Statistical-Edge.md), [Quantitative Rule Validation and Calibration](../Technical-Analysis/08-Quantitative-Rule-Validation-and-Calibration.md), [Time-Series Momentum and Trend Following](../Technical-Analysis/07-Time-Series-Momentum-and-Trend-Following.md).

## Further reading

- Aronson, D. R. (2006). *Evidence-Based Technical Analysis: Applying the Scientific Method and Statistical Inference to Trading Signals*. John Wiley & Sons.
- Asness, C. S., Moskowitz, T. J., & Pedersen, L. H. (2013). *Value and momentum everywhere*. The Journal of Finance, 68(3), 929-985.
- Barberis, N., Shleifer, A., & Vishny, R. (1998). *A model of investor sentiment*. Journal of Financial Economics, 49(3), 307-343.
- Bernard, V. L., & Thomas, J. K. (1989). *Post-earnings-announcement drift: Delayed price response or risk premium?*. Journal of Accounting Research, 27, 1-36.
- Brock, W., Lakonishok, J., & LeBaron, B. (1992). *Simple technical trading rules and the stochastic properties of stock returns*. The Journal of Finance, 47(5), 1731-1764.
- Daniel, K., Hirshleifer, D., & Subrahmanyam, A. (1998). *Investor psychology and security market under- and overreactions*. The Journal of Finance, 53(6), 1839-1885.
- George, T. J., & Hwang, C.-Y. (2004). *The 52-week high and momentum investing*. The Journal of Finance, 59(5), 2145-2176.
- Gervais, S., Kaniel, R., & Mingelgrin, D. H. (2001). *The high-volume return premium*. The Journal of Finance, 56(3), 877-919.
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). *... and the cross-section of expected returns*. The Review of Financial Studies, 29(1), 5-68.
- Hong, H., & Stein, J. C. (1999). *A unified theory of underreaction, momentum trading, and overreaction in asset markets*. The Journal of Finance, 54(6), 2143-2184.
- Jegadeesh, N., & Titman, S. (1993). *Returns to buying winners and selling losers: Implications for stock market efficiency*. The Journal of Finance, 48(1), 65-91.
- Lo, A. W., Mamaysky, H., & Wang, J. (2000). *Foundations of technical analysis: Computational algorithms, statistical inference, and empirical implementation*. The Journal of Finance, 55(4), 1705-1765.
- Marshall, B. R., Young, M. R., & Rose, L. C. (2006). *Candlestick technical trading strategies: Can they create value for investors?*. Journal of Banking and Finance, 30(8), 2303-2323.
- Moskowitz, T. J., Ooi, Y. H., & Pedersen, L. H. (2012). *Time series momentum*. Journal of Financial Economics, 104(2), 228-250.
- Roberts, H. V. (1959). *Stock-market "patterns" and financial analysis: Methodological suggestions*. The Journal of Finance, 14(1), 1-10.
- Rouwenhorst, K. G. (1998). *International momentum strategies*. The Journal of Finance, 53(1), 267-284.
- Sullivan, R., Timmermann, A., & White, H. (1999). *Data-snooping, technical trading rule performance, and the bootstrap*. The Journal of Finance, 54(5), 1647-1691.
