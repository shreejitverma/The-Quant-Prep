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

Trading setups fall into four primary structural archetypes: Trend Following Breakouts, Trend Pullbacks, Mean Reversion, and Event-Driven Catalysts.
Markets Mastery OS evaluates every setup using an objective Evidence Grade: STRONG, MIXED, WEAK, REFUTED, or UNTESTED.
Rigorous academic literature confirms that time-series momentum (Moskowitz et al. 2012) and cross-sectional momentum (Jegadeesh & Titman 1993) possess STRONG empirical edge across global asset classes.
Conversely, uncalibrated classical chart patterns frequently fail once subjected to multiple testing corrections and realistic transaction friction (Aronson 2006).

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
   - **Typical Payoff Profile**: Low win rate ($30\%$ to $45\%$), high payoff ratio ($3.0R$ to $10.0R$).

2. **Trend Pullbacks / Continuation**:
   - **Mechanism**: Liquidity replenishment inside an established higher-timeframe trend.
   - **Market Context**: Counter-trend retracement toward institutional support zones (e.g. 20-day EMA, anchored VWAP, prior breakout retest).
   - **Classic Examples**: Bull flags, flat base retests, high-tight flags, moving average pullbacks.
   - **Typical Payoff Profile**: Moderate win rate ($45\%$ to $55\%$), moderate payoff ratio ($2.0R$ to $3.5R$).

3. **Mean Reversion / Range Trading**:
   - **Mechanism**: Compensation for liquidity provision during transient order flow imbalances or inventory exhaustion.
   - **Market Context**: Price reaches extreme statistical boundaries in non-trending or range-bound regimes.
   - **Classic Examples**: Bollinger Band mean reversion, RSI oversold/overbought extremes, statistical arbitrage pairs cointegration.
   - **Typical Payoff Profile**: High win rate ($60\%$ to $75\%$), low payoff ratio ($0.8R$ to $1.5R$), vulnerable to severe left-tail gap risk.

4. **Event-Driven Catalysts / Structural Arbitrage**:
   - **Mechanism**: Liquidity demand created by mandatory institutional mandates or binary information disclosures.
   - **Classic Examples**: Post-Earnings Announcement Drift (PEAD), Russell 2000 annual rebalancing, S&P 500 additions/deletions, biotech PDUFA approvals.
   - **Typical Payoff Profile**: Highly asymmetric, regime-specific, requiring deep fundamental and regulatory modeling.

### 2. The Five-Tier Evidence Grading Framework

Markets Mastery OS assigns every setup a standardized Evidence Grade based on peer-reviewed academic literature and out-of-sample replication:

| Grade | Definition | Academic / Empirical Standard |
|-------|------------|-------------------------------|
| **STRONG** | Robust, persistent anomaly replicated across global markets over 50+ years net of all transaction costs. | Verified across multiple asset classes (equities, bonds, commodities, currencies) by independent researchers; survives multiple testing corrections ($t > 3.0$). |
| **MIXED** | Edge exists in specific asset classes or historical regimes, but decays significantly after costs or during volatility shifts. | Statistically significant gross return, but net edge is marginal ($1.0 < t < 2.0$) or sensitive to parameter choice. |
| **WEAK** | Lacks statistical significance out-of-sample or fails to beat a naive random-walk benchmark after transaction fees. | Marginal academic evidence; performance indistinguishable from data-mining noise ($t < 1.0$). |
| **REFUTED** | Empirically disproven; strategies following the pattern systematically lose money after transaction costs. | Peer-reviewed studies demonstrate zero predictive power or negative post-cost returns. |
| **UNTESTED** | Discretionary folklore lacking formal mathematical definition or backtestable verification. | Promoted in popular retail media without reproducible quantitative evidence. |

### 3. Landmark Academic Evidence on Trading Rules

#### 1. Time-Series Momentum (Moskowitz, Ooi, and Pedersen, 2012) - Grade: STRONG
- Evaluated time-series momentum (trend following) across 58 liquid futures contracts over 25 years.
- Discovered statistically significant positive returns across equity indices, government bonds, currencies, and commodities.
- Past 12-month excess return positively predicts future return over the subsequent 1 to 12 months with $t$-statistics exceeding $4.5$.
- Performance is strongest during extreme market crises (tail hedging property).

#### 2. Cross-Sectional Momentum (Jegadeesh and Titman, 1993) - Grade: STRONG
- Evaluated buying past 3-to-12 month stock winners and shorting past 3-to-12 month losers on US equities from 1965 to 1989.
- Generated an annualized risk-adjusted excess return of approximately 12.0% per year.
- Replicated globally across European, Asian, and emerging markets over subsequent decades.

#### 3. Moving Average Rules and Breakouts (Brock, Lakonishok, and LeBaron, 1992) - Grade: MIXED
- Tested variable-length moving average crossover and trading range breakout rules on the Dow Jones Industrial Average from 1897 to 1986 (90 years).
- Buy signals consistently generated higher returns than sell signals with lower volatility ($t$-statistics $> 2.5$).
- However, subsequent modern replications (e.g. Sullivan, Timmermann, and White, 1999) showed that once high retail transaction costs and data-snooping corrections are applied, net excess return largely vanishes in liquid large caps.

#### 4. Automated Pattern Recognition (Lo, Mamaysky, and Wang, 2000) - Grade: MIXED
- Developed kernel regression algorithms to formally define and detect classical technical patterns (Head and Shoulders, Double Bottoms, Rectangles).
- Across US equities over 1962 to 1996, several patterns imparted incremental statistical information and shifted conditional return distributions.
- However, economic profits after bid-ask spreads and transaction fees were insufficient to support standalone high-turnover trading.

#### 5. Data Snooping and Multiple Testing Bias (Aronson, 2006; Harvey, Liu, and Zhu, 2016)
- David Aronson (2006) tested over 6,400 technical trading rules on the S&P 500 using White's Reality Check.
- When evaluated individually, hundreds of rules showed impressive past returns.
- After correcting for data snooping (the fact that thousands of variants were tested), **not a single rule** demonstrated statistically significant predictive edge.
- Harvey, Liu, and Zhu (2016) established that modern factor research requires a $t$-statistic threshold of $t \ge 3.0$ ($p < 0.0027$) to account for multiple testing snooping across the finance literature.

---

## Worked examples

### Example 1: Formulating a Volatility Contraction Pattern (VCP)

Mark Minervini's Volatility Contraction Pattern (VCP) models institutional absorption prior to an explosive Stage 2 breakout.
A quantitative ruleset converts this discretionary setup into an objective, testable algorithm:

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
   - Initial Risk: Typically tight ($2\%$ to $4\%$), enabling asymmetric sizing ($3R$ to $5R$ target).

### Example 2: Evaluating Evidence Grades Across Setup Candidates

A quantitative discretionary desk audits four proposed trading setups:

1. **Setup A: 12-Month Time-Series Momentum in Crude Oil and S&P 500 Futures**:
   - Academic Evidence: Moskowitz, Ooi, and Pedersen (2012) confirm $t > 4.5$ across 58 futures markets net of costs.
   - Assigned Grade: **STRONG**.
   - Action: Approved for full capital allocation with volatility targeting.

2. **Setup B: 3-Day RSI < 20 Mean Reversion in S&P 500 Cash Equities**:
   - Academic Evidence: Connors (2009) shows high gross win rate ($75\%$), but academic replication shows extreme left-tail crash risk during bear regimes and heavy fee erosion under high turnover.
   - Assigned Grade: **MIXED**.
   - Action: Approved only with strict regime filters (only active when S&P 500 is above 200-day moving average).

3. **Setup C: Head-and-Shoulders Top Chart Pattern on 5-Minute Forex Charts**:
   - Academic Evidence: Lo, Mamaysky, and Wang (2000) show marginal distribution shifts in daily equities; on intraday forex, high spread crossing and noise render net edge zero ($t < 0.5$).
   - Assigned Grade: **REFUTED**.
   - Action: Rejected for live trading.

4. **Setup D: Proprietary Lunar Phase / Fibonacci Time Zone Cycle Reversal**:
   - Academic Evidence: Zero peer-reviewed empirical verification; fails basic statistical hypothesis testing.
   - Assigned Grade: **REFUTED / FOLKLORE**.
   - Action: Permanently discarded.

---

## Pitfalls

- **Data Snooping / Selection Bias**:
  Testing 100 moving average crossover pairs and selecting the one that performed best historically on a single asset guarantees that you have selected random noise rather than edge.
- **Regime Blindness**:
  Trend breakout setups thrive in high-volatility, macro-expansion regimes; they suffer devastating choppy drawdowns in range-bound, low-liquidity summer consolidations.
- **Visual Chart Cherry-Picking**:
  Human visual pattern recognition is hardwired to identify order in random data (pareidolia).
  A chartist who looks at 100 charts will unconsciously remember the 5 textbook winners while forgetting the 95 failed patterns.
- **Ignoring Execution Costs in Intraday Setups**:
  A mean-reversion setup with an average gain of 8 basis points is completely wiped out by a 10-basis-point round-trip spread and clearing cost.

---

## Interview questions

> [!question]- mkt-trd-097 | What are the four foundational structural archetypes of trade setups?
> 1. Trend Following / Momentum Breakouts.
> 2. Trend Pullbacks / Continuation.
> 3. Mean Reversion / Range Trading.
> 4. Event-Driven Catalysts / Structural Arbitrage.

> [!question]- mkt-trd-098 | What are the five tiers of the Markets Mastery OS Evidence Grading Framework?
> STRONG (replicated across markets and decades, t > 3.0 net of costs).
> MIXED (statistically significant gross return, but marginal after costs or regime-sensitive).
> WEAK (lacks statistical significance out-of-sample).
> REFUTED (disproven; systematically loses money net of costs).
> UNTESTED (discretionary folklore lacking quantitative verification).

> [!question]- mkt-trd-099 | What was the central empirical discovery of Moskowitz, Ooi, and Pedersen (2012) regarding Time Series Momentum?
> Past 12-month excess returns positively predict future returns over the subsequent 1 to 12 months across 58 liquid futures contracts with t-statistics exceeding 4.5.
> Time series momentum exhibits exceptional persistence and functions as a powerful crisis hedge during severe market panics.

> [!question]- mkt-trd-100 | What did Jegadeesh and Titman (1993) prove regarding cross-sectional momentum in equities?
> Portfolios buying the top decile of 3-to-12 month past stock winners and shorting the bottom decile of past losers generated approximately 12% annualized excess return.
> The momentum premium is one of the most robust, globally replicated factor anomalies in financial economics.

> [!question]- mkt-trd-101 | What were the findings of Brock, Lakonishok, and LeBaron (1992) regarding technical trading rules on the Dow Jones?
> Simple moving average crossover and trading range breakout rules generated statistically significant gross excess returns over a 90-year test period (1897-1986).
> Buy signals consistently produced higher returns and lower volatility than sell signals.

> [!question]- mkt-trd-102 | Why did Sullivan, Timmermann, and White (1999) question the real-world tradability of Brock et al.'s findings?
> Once historical transaction costs and data-snooping corrections (White's Reality Check) were applied, net out-of-sample excess returns largely vanished.
> The apparent edge was heavily eroded by bid-ask spread crossing and execution fees.

> [!question]- mkt-trd-103 | How did Lo, Mamaysky, and Wang (2000) formalize technical chart pattern analysis?
> They used non-parametric kernel regression to construct mathematical definitions of classical patterns (Head and Shoulders, Double Bottoms).
> They demonstrated that pattern conditioning shifted empirical return distributions, proving technical patterns contain incremental statistical information.

> [!question]- mkt-trd-104 | What is data snooping bias (p-hacking) as documented by David Aronson (2006)?
> Testing thousands of rule variants on the same historical dataset until one appears statistically profitable purely by random chance.
> Without applying multiple testing adjustments (e.g. White's Reality Check or Hansen's SPA), historical backtests are completely spurious.

> [!question]- mkt-trd-105 | What is the t-statistic threshold established by Harvey, Liu, and Zhu (2016) for modern factor discovery?
> t >= 3.0 (corresponding to p < 0.0027), raised from the conventional t >= 2.0 threshold.
> The higher hurdle accounts for the hundreds of candidate factors mined and tested across the financial literature over recent decades.

> [!question]- mkt-trd-106 | What is Mark Minervini's Volatility Contraction Pattern (VCP)?
> A pattern characterized by progressive contractions in price volatility (e.g. 25% drop, then 10%, then 3%) accompanied by drying volume before a breakout.
> It reflects institutional absorption of circulating supply, leaving the stock poised for an explosive expansion upon buying pressure.

> [!question]- mkt-trd-107 | What is the behavioral explanation for the persistence of momentum in financial markets?
> Investor under-reaction to fundamental news due to cognitive conservatism and anchoring, followed by delayed over-reaction driven by herding and FOMO.
> Institutional capital moves slowly over weeks and months, generating persistent directional price drift.

> [!question]- mkt-trd-108 | Why do breakout setups have low win rates (30% to 40%) but high profitability?
> False breakouts and whip-saws are frequent in efficient markets, generating frequent small 1R losses.
> However, genuine breakouts transition into massive multi-month secular trends producing 5R to 15R gains, yielding high net expectancy.

> [!question]- mkt-trd-109 | What is Post-Earnings Announcement Drift (PEAD) discovered by Ball and Brown (1968)?
> The tendency of a stock's cumulative abnormal returns to drift in the direction of an earnings surprise for weeks or months following the announcement date.
> PEAD is a prime example of an event-driven catalyst driven by institutional earnings forecast revisions.

> [!question]- mkt-trd-110 | What is a Stage 2 breakout in Stan Weinstein's market stage framework?
> The transition of a stock from a prolonged sideways consolidation base (Stage 1) into an advancing uptrend (Stage 2) above a rising 30-week moving average.
> Stage 2 breakouts represent the optimal entry window for discretionary trend followers.

> [!question]- mkt-trd-111 | Explain the concept of Anchored VWAP (AVWAP) and why it acts as dynamic support/resistance.
> AVWAP calculates the Volume Weighted Average Price starting from a specific significant historical anchor point (e.g. earnings release, market crash low, 52-week high).
> It represents the exact average dollar-weighted cost basis of all market participants who entered since that critical event.

> [!question]- mkt-trd-112 | What is a bull flag and what are its quantitative criteria?
> A sharp, high-volume upward price thrust (the flagpole) followed by a tight, downward-sloping consolidation on declining volume.
> Quantitative criteria require the pullback to retrace no more than 38.2% to 50% of the flagpole with volume drying up below the 20-day average.

> [!question]- mkt-trd-113 | What is pareidolia in manual discretionary chart analysis?
> The human psychological tendency to perceive meaningful patterns or order in random visual noise.
> Unquantified traders visually identify apparent head-and-shoulders or flag patterns in pure synthetic Geometric Brownian Motion price paths.

> [!question]- mkt-trd-114 | What is the typical payoff profile of a mean-reversion trading strategy?
> High win rate (65% to 75%), small average gains (0.5R to 1.5R), but extreme vulnerability to large left-tail drawdowns.
> When a trend breakout occurs, mean-reversion systems experience persistent, escalating losses without timely exits.

> [!question]- mkt-trd-115 | What is Donchian Channel breakout trading?
> A systematic trend-following rule that buys when price breaks above the highest high of the past N days (e.g. 20 or 55 days) and sells when price breaks the lowest low.
> It forms the core entry engine of the Turtle Trading system, capturing major trend runs with zero discretionary forecasting.

> [!question]- mkt-trd-116 | How does market regime (trending vs range-bound) impact the performance of breakout setups?
> Breakout setups thrive in high-dispersion, strong macro-trending regimes.
> In choppy, range-bound regimes, breakouts suffer severe whipsaws as prices consistently mean-revert from channel boundaries.

> [!question]- mkt-trd-117 | What is the Russell 2000 annual rebalancing anomaly?
> In June, the Russell indices reconstitute their member stocks based on updated market capitalizations.
> Predictable buying of incoming stocks and selling of deletions by passive index tracking funds creates multi-week price distortions exploited by arbitrageurs.

> [!question]- mkt-trd-118 | Why is volume expansion mandatory to confirm a genuine technical breakout?
> Low-volume breakouts represent transient liquidity vacuums easily driven by minor retail orders that quickly reverse.
> Heavy volume expansion proves institutional participation, indicating that large capital is absorbing resting supply at new price levels.

> [!question]- mkt-trd-119 | What is relative strength (RS) in equity momentum trading?
> A measure of an individual stock's price performance compared to a broad benchmark index (e.g. S&P 500) over a 3-to-12 month window.
> Stocks printing new 52-week highs while the broad market is consolidating or declining exhibit leading institutional accumulation.

> [!question]- mkt-trd-120 | What is a false breakout (bull trap) and how does it trap buyers?
> Price punches above a prominent resistance level, triggering retail breakout buy orders and short stop-losses, but immediately fails and closes back inside the range.
> Trapped breakout buyers are forced to liquidate, accelerating a rapid downward reversal.

> [!question]- mkt-trd-121 | In statistical arbitrage, what is the cointegration test used to identify mean-reverting pairs?
> The Engle-Granger two-step method or Johansen test evaluating whether a linear combination of two non-stationary time series is stationary (I(0)).
> Cointegration guarantees that the spread between the two assets has a constant mean and finite variance over time.

> [!question]- mkt-trd-122 | What is a Darvas Box?
> A price consolidation rectangle formed by a new all-time high followed by three consecutive days that fail to breach that high, establishing a ceiling and floor.
> Developed by Nicolas Darvas (1960), buying occurs upon a clean breakout above the box ceiling with a stop set at the box floor.

> [!question]- mkt-trd-123 | What is a moving average crossover whipsaw?
> Successive false trend signals generated when an asset oscillates sideways across the moving average lines.
> Each crossover triggers an entry that is promptly reversed at a loss, causing rapid capital attrition during consolidating regimes.

> [!question]- mkt-trd-124 | What is the economic rationale for the value factor anomaly (Fama and French, 1993)?
> Cheap stocks (low P/E or low P/B) trade at a discount because they face higher financial distress risk, or because investors over-react to past bad news.
> Buying undervalued assets earns a structural risk premium as fundamentals stabilize or mean-revert over multi-year horizons.

> [!question]- mkt-trd-125 | What is an opening range breakout (ORB)?
> Taking a directional position when price breaks above the high or below the low established during the first 15 or 30 minutes of the trading session.
> The initial balance represents early institutional price discovery; a clean break indicates strong initiative order flow for the session.

> [!question]- mkt-trd-126 | Why do candlestick reversal patterns (e.g. hammer, shooting star) have WEAK standalone evidence?
> Standalone 1-bar or 2-bar candlestick formations lack statistical significance over large multi-decade samples when tested without broader trend context.
> After transaction costs, trading raw candlestick signals produces negative net expectancy.

> [!question]- mkt-trd-127 | What is the high-tight flag setup and what is its historical track record?
> An explosive advance of 100% to 120% within 4 to 8 weeks, followed by a tight consolidation of no more than 20% to 25% lasting 3 to 5 weeks.
> Historically documented by Thomas Bulkowski as one of the highest-performing momentum setups, though it occurs rarely.

> [!question]- mkt-trd-128 | Why must every quantitative or discretionary playbook document objective invalidation rules for each setup?
> Without unambiguous invalidation criteria, traders fall prey to narrative rationalization and holding losing trades indefinitely.
> Pre-registered rules ensure disciplined 1R risk containment, preserving capital to capture the next edge-positive trial.

---

## Further reading

- Brock, W., Lakonishok, J., & LeBaron, B. (1992). *Simple technical trading rules and the stochastic properties of stock returns*. The Journal of Finance, 47(5), 1731-1764.
- Jegadeesh, N., & Titman, S. (1993). *Returns to buying winners and selling losers: Implications for stock market efficiency*. The Journal of Finance, 48(1), 65-91.
- Lo, A. W., Mamaysky, H., & Wang, J. (2000). *Foundations of technical analysis: Computational algorithms, statistical inference, and empirical implementation*. The Journal of Finance, 55(4), 1705-1765.
- Moskowitz, T. J., Ooi, Y. H., & Pedersen, L. H. (2012). *Time series momentum*. Journal of Financial Economics, 104(2), 228-250.
- Aronson, D. R. (2006). *Evidence-Based Technical Analysis: Applying the Scientific Method and Statistical Logic to Trading*. John Wiley & Sons.
