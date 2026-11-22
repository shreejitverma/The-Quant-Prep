---
type: concept
title: "Time-Series Momentum, Trend Following, and Crisis Alpha"
track: [quant-trader, quant-research]
tier: advanced
status: solid
est_hours: 1.5
tags: [technical-analysis, time-series-momentum, trend-following, cta, managed-futures, crisis-alpha, volatility-targeting]
prereqs: []
---

# Time-Series Momentum, Trend Following, and Crisis Alpha

While cross-sectional momentum ranks assets against each other in a zero-sum peer tournament, Time-Series Momentum (TSMOM) - commonly referred to in institutional markets as trend following or Managed Futures / Commodity Trading Advisor (CTA) strategies - evaluates each asset exclusively against its own historical price trajectory.
If an asset's past return over a lookback horizon is positive, the strategy goes long; if negative, it goes short or moves to cash.
Named and documented by Tobias Moskowitz, Yao Hua Ooi, and Lasse Heje Pedersen (2012) across 58 futures and forwards, time-series momentum has since been backtested on more than a century of equity, bond, currency and commodity data (Hurst, Ooi and Pedersen 2017) and on two centuries of spot data (Lempérière et al. 2014).

---

## TL;DR

Time-series momentum models absolute price momentum across individual liquid futures contracts.
The foundational formulation scales position size inversely to rolling instrument volatility:
$$w_{i, t} = \frac{\sigma_{\text{target}}}{\sigma_{i, t}} \times \text{sign}(R_{i, t-12, t})$$
Moskowitz, Ooi and Pedersen (2012) found positive 12-month time-series momentum returns in all 58 instruments they studied (52 significant at 5%) over 1985 to 2009, and Hurst, Ooi and Pedersen (2017) report positive gross returns in each decade from 1880 to 2016 for 1-, 3- and 12-month signals.
Fung and Hsieh (2001) showed that trend-follower returns resemble portfolios of lookback straddles, which is why the strategy has done best in large up and down years for equities.
Hurst, Ooi and Pedersen report positive returns in 8 of the 10 largest drawdowns of a US 60/40 portfolio since 1880, which is the evidence behind the "crisis alpha" label.

---

## Learning objectives

- Contrast Time-Series Momentum (absolute trend) with Cross-Sectional Momentum (relative ranking).
- Formulate the Moskowitz, Ooi, and Pedersen (2012) volatility-scaled trend-following model.
- Analyze the century-long evidence (Hurst et al. 2017) on trend following across asset classes, and what it does not show.
- Model the mathematical origins of "Crisis Alpha" and the synthetic straddle payoff profile of trend following.
- Construct multi-horizon trend signal combinations and implement dynamic risk budgeting.

---

## Core concepts

### 1. Mathematical Formulation of Time-Series Momentum

1. **The Pure Signal Rule**:
   - For an asset $i$ at month $t$, evaluate the excess return over a lookback window $L$ (conventionally $L = 12$ months):
     $$R_{i, t-L, t} = \prod_{k=0}^{L-1} (1 + r_{i, t-k}) - 1$$
   - The directional position signal is binary:
     $$\text{Signal}_{i, t} = \text{sign}(R_{i, t-L, t}) = \begin{cases} +1 & \text{if } R_{i, t-L, t} > 0 \\ -1 & \text{if } R_{i, t-L, t} < 0 \end{cases}$$

2. **Volatility Scaling (Volatility Targeting)**:
   - Volatility differs by an order of magnitude across contracts (short-term interest rate futures move far less than crude oil), which is why Moskowitz, Ooi and Pedersen size every position to the same ex-ante volatility.
   - To prevent high-volatility commodities from dominating portfolio risk, positions are scaled inversely to ex-ante annualized volatility $\sigma_{i, t}$:
     $$w_{i, t} = \frac{\sigma_{\text{target}}}{N \times \sigma_{i, t}} \times \text{sign}(R_{i, t-L, t})$$
   - where $\sigma_{\text{target}}$ is the volatility budget and $N$ is the number of instruments; Hurst, Ooi and Pedersen scale their combined portfolio to $10\%$ annualized ex-ante volatility, and Moskowitz, Ooi and Pedersen size each instrument to $40\%$.
   - Dividing the budget by $N$ gives the portfolio $\sigma_{\text{target}}$ only if all positions are perfectly correlated; with $20$ uncorrelated sleeves at $0.60\%$ each, portfolio volatility is $0.60\% \times \sqrt{20} = 2.68\%$, so every sleeve must be levered by $\sqrt{20} = 4.47$ to reach $12\%$.
   - When an asset's volatility rises, its position contracts, so each position's dollar risk stays near its budget.

### 2. Multi-Horizon Trend Aggregation

A common design avoids relying on a single lookback window (Hurst, Ooi and Pedersen combine 1-, 3- and 12-month signals with equal weights) by aggregating signals across multiple horizons:

$$\text{Combined Signal}_{i, t} = \sum_{k=1}^K \omega_k \times \text{sign}(R_{i, t-L_k, t})$$

where $\sum \omega_k = 1.0$ and, in this illustration, the lookbacks are $L_1 = 1$, $L_2 = 3$, $L_3 = 6$ and $L_4 = 12$ months.
With four equal weights the blended signal takes only the five values $-1, -0.5, 0, +0.5, +1$ (in $1, 4, 6, 4, 1$ of the $16$ sign combinations), so it moves in smaller steps than a single sign and changes position less abruptly.

### 3. Crisis Alpha and the Straddle Payoff

Trend following exhibits a return profile structurally distinct from traditional equities and hedge funds:

```
+---------------------------------------------------------------------------------+
|                       TREND FOLLOWING "SMILE" PAYOFF PROFILE                    |
+---------------------------------------------------------------------------------+
|  CTA Strategy Return (%)                                                        |
|         \                                                               /       |
|          \                                                             /        |
|           \                                                           /         |
|            \                                                         /          |
|             \                                                       /           |
|              \                     Base Horizon                    /            |
|               \__________________ (Choppy Whipsaw) _______________/             |
|                                                                                 |
|  <--------------------------- S&P 500 Market Return --------------------------> |
|     Large down years                  Flat years                Large up years  |
+---------------------------------------------------------------------------------+
|  Shape reported by Fung-Hsieh (2001) and Hurst-Ooi-Pedersen (2017): best in     |
|  extreme up or down equity years, weakest in flat, choppy years.                |
+---------------------------------------------------------------------------------+
```

1. **The Synthetic Straddle Payoff**:
   - Fung and Hsieh (2001) showed in *The Risk in Hedge Fund Strategies* that portfolios of lookback straddles explain trend-follower fund returns far better than standard linear factor models; the match is close, not identical.
   - Hurst, Ooi and Pedersen explain the bear-market record by timing: the 10 largest 60/40 drawdowns since 1880 lasted about 15 months on average, long enough for a trend signal to turn short, whereas a crash over a few days (such as October 1987) can be missed.
   - If markets rally for a long time, trend followers stay long.

2. **The Source of Positive Skewness**:
   - A straddle-like payoff (small losses when prices chop, larger gains when they trend) is the usual explanation for the positive skewness reported for trend-following returns.
   - Short-volatility and carry strategies have the opposite, option-seller shape and tend to show negative skewness.

### 4. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                      EVIDENCE LEDGER: TIME-SERIES MOMENTUM                      |
+---------------------------------------------------------------------------------+
|  Phenomenon: Absolute Trend Following Across Multi-Asset Futures                |
|  Evidence: replicated across instruments, decades and independent datasets      |
+---------------------------------------------------------------------------------+
|  Key Empirical Studies:                                                         |
|  1. Moskowitz, Ooi, and Pedersen (2012, Journal of Financial Economics):        |
|     - 58 futures and forwards (24 commodities, 12 currency pairs, 9 equity      |
|       indices, 13 bond futures); strategy results for 1985 to 2009.             |
|     - Returns persist for 1 to 12 months and partially reverse afterwards;      |
|       all 58 had positive 12-month TSMOM returns, 52 significant at 5%.         |
|     - The diversified portfolio's Sharpe ratio exceeded one; its alpha over     |
|       cross-sectional momentum was 76 bp a month (t = 5.90).                    |
|  2. Hurst, Ooi, and Pedersen (2017, Journal of Portfolio Management):           |
|     - 67 markets, 1880 to 2016 (137 years), 1-, 3- and 12-month signals,        |
|       10% volatility target, reported gross and net of costs and 2-and-20.      |
|     - Positive gross returns in each decade for each signal; average Sharpe     |
|       ratio per market about 0.4; low correlation to stocks and bonds.          |
|  3. Fung and Hsieh (2001, Review of Financial Studies):                         |
|     - Lookback-straddle portfolios explain trend-follower returns far better    |
|       than linear factor models: a non-linear, option-like exposure.            |
|  4. Lempérière et al. (2014, Journal of Investment Strategies):                 |
|     - Futures since 1960 and spot series back to 1800: t-statistic of trend     |
|       excess returns about 5 since 1960 and about 10 since 1800, stable         |
|       across time and asset classes; shorter trends have weakened recently.     |
+---------------------------------------------------------------------------------+
|  Counter-Evidence & Structural Frictions:                                       |
|  1. Long flat stretches and fast moves: returns are uneven, and a crash over a  |
|     few days (October 1987) can be missed by a signal built on months of data.  |
|  2. Fees and costs: Hurst, Ooi and Pedersen show net-of-2-and-20 returns        |
|     well below gross; gross academic backtests overstate what investors get.    |
+---------------------------------------------------------------------------------+
```

### 5. Position Sizing and Capital Allocation Mechanics

To execute time-series momentum in live institutional portfolios:

1. **Daily Volatility Estimation**:
   - Exponentially Weighted Moving Average (EWMA) of daily squared returns:
     $$\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1 - \lambda) r_t^2$$
   - RiskMetrics (J.P. Morgan 1996) uses $\lambda = 0.94$ for daily data, a centre of mass of $0.94 / 0.06 = 15.7$ days.
   - Moskowitz, Ooi and Pedersen choose $\lambda$ so the centre of mass $\lambda / (1 - \lambda)$ is $60$ days, which gives $\lambda = 60 / 61 = 0.9836$.

2. **Cash and Margin Management**:
   - Futures require only exchange-set initial margin (performance bond), a fraction of notional that varies by contract and over time.
   - The rest of the capital can be held in short-dated Treasury bills, earning the risk-free rate.
   - Total CTA portfolio return equals:
     $$\text{Total Return} = \text{Futures Trading PnL} + \text{Collateral Yield}$$

---

## Worked examples

### Example 1: Volatility-Targeted Position Sizing for a Commodity Futures Trend

A quantitative CTA desk executes a 12-month time-series momentum model on Crude Oil futures:
- Portfolio Capital: $C = \$10,000,000.00$.
- Portfolio Volatility Target: $\sigma_{\text{target}} = 12.0\%$ annualized ($0.12$).
- Total Instruments in Universe: $N = 20$.
- Capital Allocated per Instrument: $\frac{C}{N} = \frac{\$10,000,000}{20} = \$500,000.00$.
- Crude Oil Current Price: $P = \$80.00\text{ per barrel}$.
- Contract Multiplier: $1,000\text{ barrels}$, the NYMEX WTI Light Sweet Crude Oil (CL) contract unit as of November 2026 (Notional value per contract $= \$80,000.00$).
- Trailing 12-Month Crude Oil Return: $R_{12M} = +35.0\% \implies \text{Signal} = +1\text{ (Long)}$.
- Current Annualized Volatility of Crude Oil: $\sigma_{\text{oil}} = 30.0\%$ ($0.30$).

1. **Calculate Target Notional Exposure for Crude Oil**:
   $$\text{Target Notional} = \text{Allocated Capital} \times \frac{\sigma_{\text{target}}}{\sigma_{\text{oil}}} = \$500,000 \times \frac{0.12}{0.30} = \$500,000 \times 0.40 = \$200,000.00$$

2. **Compute Number of Contracts to Trade**:
   $$\text{Contracts} = \frac{\text{Target Notional}}{\text{Contract Notional}} = \frac{\$200,000.00}{\$80,000.00} = 2.5\text{ contracts} \approx 2\text{ or } 3\text{ contracts}$$
   The desk buys $2$ contracts (Notional $= \$160,000$), carrying $2 \times \$80,000 \times 0.30 = \$48,000$ of annual dollar volatility against a budget of $\$500,000 \times 0.12 = \$60,000$.
   Because oil volatility ($30\%$) is far higher than the target ($12\%$), the notional is scaled down to $40\%$ of the capital allocation.

### Example 2: Dynamic Deleveraging During a Volatility Shock

Over the subsequent month, a geopolitical crisis erupts in the Middle East:
- Crude Oil surges to $\$100.00$ per barrel (Notional per contract $= \$100,000.00$).
- Crude Oil 30-day realized volatility spikes from $30\%$ to $60.0\%$ annualized ($\sigma_{\text{oil}} = 0.60$).
- Signal remains strongly positive ($+1$).

1. **Re-evaluate Target Notional Exposure**:
   $$\text{Target Notional}_{\text{new}} = \$500,000 \times \frac{0.12}{0.60} = \$500,000 \times 0.20 = \$100,000.00$$

2. **Rebalance Contract Quantity**:
   $$\text{Contracts}_{\text{new}} = \frac{\$100,000.00}{\$100,000.00} = 1.0\text{ contract}$$
   - Before trimming, the 2 contracts carry $2 \times \$100,000 \times 0.60 = \$120,000$ of dollar volatility, twice the $\$60,000$ budget.
   - The desk sells $1$ contract, which brings dollar volatility back to $\$100,000 \times 0.60 = \$60,000$.
   - **Key Risk Principle**: volatility targeting holds each position's dollar risk near its budget, so it takes profits and cuts size when volatility jumps; it does not by itself predict what price does next.

---

## Pitfalls

- **The Decadal Plateau Hazard (Central Bank Whipsaw)**:
  Trend following requires persistent directional macro trends to overcome daily transaction friction.
  In range-bound markets the strategy keeps paying whipsaw losses and costs, and multi-year flat or losing stretches have occurred; how long one lasts is not predictable.
- **V-Shaped Market Reversal Squeezes**:
  Trend followers are positioned short during the depths of a bear market.
  If the market executes an abrupt V-shaped bottom, short positions suffer sharp immediate drawdowns before the model can turn around and flip long.
- **Excessive Leverage on Low-Volatility Fixed Income**:
  Because volatility targeting scales inversely to volatility, the largest notional positions sit in the lowest-volatility contracts, such as short-term interest rate futures.
  If a sudden rate shock occurs, this high leverage can cause severe dollar losses despite low percentage price moves.
- **Roll Yield Drag in Contango Curves**:
  Trend followers holding long commodity futures contracts must continuously roll expiring contracts to the next active month.
  In a steep contango market, selling cheap expiring contracts and buying expensive back-month contracts creates severe negative roll yield drag.

---

## Interview questions

> [!question]- mkt-ta-193 | What is Time-Series Momentum (TSMOM) and how does it differ from Cross-Sectional Momentum?
> TSMOM evaluates an asset's past return relative exclusively to its own history (absolute trend: long if positive, short if negative).
> Cross-sectional momentum ranks assets against each other (relative winners vs losers, zero net investment).

> [!question]- mkt-ta-194 | What was the landmark empirical contribution of Moskowitz, Ooi, and Pedersen (2012)?
> Returns persist for 1 to 12 months and partially reverse at longer horizons, across 58 liquid equity index, currency, commodity and bond futures and forwards.
> All 58 had positive 12-month TSMOM returns over 1985 to 2009 (52 significant at 5%), and the diversified portfolio had a Sharpe ratio above one.

> [!question]- mkt-ta-195 | What did Hurst, Ooi, and Pedersen (2017) demonstrate in "A Century of Evidence on Trend-Following"?
> They extended the backtest to 67 markets from 1880 to 2016 (137 years), using 1-, 3- and 12-month signals.
> Each signal earned positive gross returns in every decade, the strategy had low correlation to stocks and bonds, and it was positive in 8 of the 10 largest 60/40 drawdowns.

> [!question]- mkt-ta-196 | What is volatility targeting in managed futures portfolio construction?
> Scaling each position's notional size inversely to its trailing annualized volatility: weight = sigma_target / sigma_asset.
> It equalizes each position's stand-alone volatility (not its contribution to portfolio risk, which also depends on correlations) and trims exposure when volatility rises.

> [!question]- mkt-ta-197 | What is Crisis Alpha?
> The tendency of trend-following strategies to earn positive returns in prolonged equity bear markets: Hurst, Ooi and Pedersen find positive returns in 8 of the 10 largest 60/40 drawdowns since 1880.
> It works when declines unfold over months (about 15 on average for those drawdowns), giving the signal time to turn short; sudden crashes can be missed.

> [!question]- mkt-ta-198 | Why do Fung and Hsieh (2001) describe trend-following returns as synthetic lookback straddles?
> Because portfolios of lookback straddles explain trend-follower fund returns much better than linear factor models: the strategy behaves like an option on large moves in either direction.
> The result is a convex "smile" against market returns, best in large up or down years.

> [!question]- mkt-ta-199 | What is the difference between positive skewness and negative skewness in hedge fund strategies?
> Trend following tends to show positive skewness: frequent small whipsaw losses and occasional large gains, like a long-option position.
> Carry and short-volatility strategies tend to show negative skewness: steady small gains and occasional large losses, like a short-option position.

> [!question]- mkt-ta-200 | What is multi-horizon trend combining?
> Aggregating trend signals across multiple lookback windows (e.g. 1-month, 3-month, 6-month, and 12-month) into a weighted composite signal.
> With four equal weights the signal takes five values (-1, -0.5, 0, 0.5, 1), so it changes in smaller steps and depends less on any one lookback parameter.

> [!question]- mkt-ta-201 | What is roll yield in commodity futures trend following?
> The yield earned or lost from rolling an expiring futures contract into a farther-dated contract: Roll_Yield = (P_near - P_far) / P_near.
> Backwardation generates positive roll yield; contango generates negative roll yield drag.

> [!question]- mkt-ta-202 | What is the usual explanation offered for weak trend-following returns in the 2010s, and how strong is it?
> The usual story is that low rates and central bank intervention damped macro volatility and produced fewer sustained trends and more sharp reversals.
> It is a plausible narrative, not a tested cause; Hurst, Ooi and Pedersen find that the strategy has done best when cross-market correlations are low.

> [!question]- mkt-ta-203 | What is collateral yield in a managed futures portfolio?
> The interest earned on unencumbered cash held in short-term Treasury bills while trading futures on margin.
> In high interest rate environments, collateral yield contributes significantly to total fund returns.

> [!question]- mkt-ta-204 | How does a trend follower handle a sudden V-shaped market bottom?
> Trend followers suffer an initial drawdown because they are positioned short at the market bottom.
> The model flips long only once the trailing return over its lookback turns positive, which takes longer the longer the lookback.

> [!question]- mkt-ta-205 | Why do CTA funds trade liquid futures rather than physical cash equities?
> Futures provide high liquidity, low transaction costs, transparent centralized exchange clearing, and equal ease of shorting without borrow fees.
> Futures also allow capital efficiency through exchange leverage.

> [!question]- mkt-ta-206 | Over which horizons did Moskowitz, Ooi and Pedersen (2012) find time-series momentum?
> Returns persist for 1 to 12 months and partially reverse over longer horizons, with the strongest reversal in the year after the trend.
> Strategies with look-back and holding periods of 12 months or less were the most robust across asset classes.

> [!question]- mkt-ta-207 | What is risk parity in a multi-asset trend portfolio?
> Allocating portfolio risk such that each asset class (commodities, FX, equities, fixed income) contributes an equal percentage to total portfolio variance.
> It prevents high-volatility sectors from dominating overall portfolio swings.

> [!question]- mkt-ta-208 | How does EWMA volatility estimation differ from simple rolling standard deviation?
> EWMA applies exponentially decaying weights, so recent shocks count more than distant ones: RiskMetrics lambda = 0.94 has a centre of mass of 15.7 days, MOP's 60-day centre of mass uses lambda = 0.9836.
> It reacts to volatility spikes faster than an equal-weight window of similar length.

> [!question]- mkt-ta-209 | What is the "whipsaw tax" in trend following?
> The accumulation of small losses from signals that reverse in range-bound markets.
> It is the cost of always being positioned for the trends that do persist.

> [!question]- mkt-ta-210 | What is MACD-based trend following in CTA models?
> Using the sign and size of a volatility-normalized moving-average spread instead of a binary sign; one bounded design is Signal = tanh(MACD / sigma) (an illustration, not a published standard).
> It scales position size with trend strength and caps it for very strong trends.

> [!question]- mkt-ta-211 | Why is a year like 2022 the textbook case for time-series momentum?
> Equities and government bonds both fell for most of the year as rates rose, the US dollar strengthened, and energy prices rose sharply in the first half: moves that lasted long enough for 1- to 12-month signals to align with them.
> A trend follower short bonds and equities and long the dollar would profit; quote any fund or index return only from its published report.

> [!question]- mkt-ta-212 | What is a breakout lookback filter (Donchian rule) in CTA trading?
> Establishing long positions when price exceeds the N-day highest high, and short positions when price breaks below the N-day lowest low.
> Breakout rules of this kind were the core of the Turtle trading rules described by Curtis Faith in *Way of the Turtle* (2007).

> [!question]- mkt-ta-213 | What is portfolio heat in trend trading?
> The total aggregate open risk across all positions in the portfolio, measured as the sum of dollar distances to stop-loss levels divided by total equity.
> A cap on heat limits the loss if every stop is hit at once; the cap is a risk-policy choice, not an industry constant.

> [!question]- mkt-ta-214 | How does correlation among futures contracts impact a trend portfolio?
> Higher correlations mean fewer independent bets, so the same positions carry more portfolio risk.
> Hurst, Ooi and Pedersen find trend following has performed best in low-correlation periods; managers monitor correlations and scale down when they rise.

> [!question]- mkt-ta-215 | What is the difference between slow trend and fast trend strategies?
> Fast trend strategies use short lookbacks (weeks), trading often with more whipsaws but quicker exits.
> Slow trend strategies use long lookbacks (many months), with lower turnover but slower reactions; Lempérière et al. (2014) report that short trends have weakened in recent decades while long trends have not.

> [!question]- mkt-ta-216 | What does the long-run evidence say about trend-following Sharpe ratios and correlations?
> Hurst, Ooi and Pedersen report an average gross Sharpe ratio of about 0.4 per market, with diversification across 67 markets raising the portfolio figure, and net returns well below gross after costs and 2-and-20 fees.
> The main value is low correlation to stocks and bonds and positive returns in most large 60/40 drawdowns.

> [!question]- mkt-ta-217 | What is the difference between cash trend and notional trend exposure?
> Notional exposure is the face value of the underlying assets controlled by futures contracts, which can be several times fund equity.
> Cash exposure is the actual capital deposited in margin and Treasury bills.

> [!question]- mkt-ta-218 | Why do trend followers rarely take profit at target prices?
> Because a fixed target caps the large winning trends that pay for the many small losses.
> Trend followers exit on trailing stops or signal reversal, keeping the right tail open.

> [!question]- mkt-ta-219 | What is backwardation in energy futures and why does it benefit long trend positions?
> When near-dated prices are above deferred futures prices, often because of tight current supply.
> A long position rolls by selling the expiring (higher-priced) contract and buying the deferred (lower-priced) one, and each contract tends to rise toward spot as it nears expiry, giving positive roll yield.

> [!question]- mkt-ta-220 | What is contango in precious metals and how does it penalize long trend positions?
> When forward futures trade at a premium to spot price due to storage and interest financing costs.
> Long positions suffer continuous negative roll yield as contracts roll down toward spot.

> [!question]- mkt-ta-221 | How does trade execution slippage scale with CTA fund assets under management (AUM)?
> As AUM grows into billions, order sizes exceed top-of-book market depth, forcing execution algorithms to slice trades over days.
> Increased market impact slippage degrades net trend alpha for mega-funds.

> [!question]- mkt-ta-222 | What is trend strength filtering using t-statistics?
> Regressing past prices on a linear time trend and scaling position size by the regression t-statistic, bounded as Signal = t / sqrt(t^2 + df) with df = n - 2.
> That transform is exactly the sample correlation between price and time, so it lies in [-1, 1] and weights positions by how clean the trend is rather than by its raw size.

> [!question]- mkt-ta-223 | What is a stop-out protocol during a liquidity flash crash?
> Pre-programmed automated risk limits that liquidate futures positions when intraday drawdown breaches a hard capital threshold.
> It prevents catastrophic deficit balances when market depth evaporates.

> [!question]- mkt-ta-224 | Why is time-series momentum often described as robust across economic history, and what is the caveat?
> It needs no macro or valuation view: it buys what has been rising and shorts what has been falling, and backtests show positive returns across decades, markets and regimes (Hurst, Ooi and Pedersen 2017; Lempérière et al. 2014).
> The caveat is that these are backtests: live returns are net of fees and costs, and flat stretches can last years.

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_ta_07_tsmom.py`](../../code/mkt_ta_07_tsmom.py) prints and asserts every number on this page: each sizing step against the dollar volatility the position actually carries, portfolio volatility of 20 sleeves in closed form against a seeded simulation, the multi-horizon signal by enumerating all 16 sign combinations, EWMA centres of mass by summing the weights, the t-to-correlation identity by OLS against numpy's correlation, and the cited instrument counts against the papers' totals.
- Related notes: [Momentum, Relative Strength and Breadth](04-Momentum-Relative-Strength-and-Breadth.md) (cross-sectional momentum).

---

## Further reading

- Fung, W., & Hsieh, D. A. (2001). *The risk in hedge fund strategies: Theory and evidence from trend followers*. The Review of Financial Studies, 14(2), 313-341.
- Moskowitz, T. J., Ooi, Y. H., & Pedersen, L. H. (2012). *Time series momentum*. Journal of Financial Economics, 104(2), 228-250.
- Lempérière, Y., Deremble, C., Seager, P., Potters, M., & Bouchaud, J. P. (2014). *Two centuries of trend following*. Journal of Investment Strategies, 3(3), 41-61.
- Hurst, B., Ooi, Y. H., & Pedersen, L. H. (2017). *A century of evidence on trend-following investing*. The Journal of Portfolio Management, 44(1), 39-51.
- Greyserman, A., & Kaminski, K. (2014). *Trend Following with Managed Futures: The Search for Crisis Alpha*. John Wiley & Sons.
- Carver, R. (2015). *Systematic Trading: A Unique New Method for Designing Trading and Investing Systems*. Harriman House.
- Faith, C. (2007). *Way of the Turtle*. McGraw-Hill.
- J.P. Morgan and Reuters (1996). *RiskMetrics Technical Document* (4th ed.).
- CME Group, NYMEX Light Sweet Crude Oil (CL) contract specifications (contract unit 1,000 barrels).
