---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Brier (1950) - Verification of Forecasts Expressed in Terms of Probability, Kelly (1956) - A New Interpretation of Information Rate, Thorp (1969) - Optimal Gambling Systems for Favorable Games, Taleb (2001) - Fooled by Randomness]
---

# Probability and Decision Making

## TL;DR

- Professional trading is the discipline of allocating scarce risk capital under uncertainty where outcomes are probabilistic rather than deterministic.
- Expected Value (EV) defines mathematical edge; a strategy is viable if and only if its cumulative expected value per trade is positive after accounting for execution friction and financing costs.
- Variance Drag mathematically erodes geometric portfolio compound growth relative to arithmetic average returns ($R_{\text{geo}} \approx R_{\text{arith}} - \frac{1}{2}\sigma^2$); managing portfolio volatility is essential for long-term wealth compounding.
- Forecast calibration evaluates whether subjective probability estimates align with empirical frequencies; the Brier Score decomposes forecasting skill into calibration error and resolution.
- The Kelly Criterion derives the mathematically optimal fraction of wealth to allocate to an edge, maximizing geometric compounding while fractional Kelly buffers against parameter estimation error.

## Learning objectives

- Formulate Expected Value (EV), profit factor, and R-multiple expectancy for trading strategies.
- Derive the mathematical formula for variance drag and analyze its non-linear erosion of long-term compounding.
- Calculate and interpret the Brier Score, reliability curves, and probability calibration metrics.
- Apply the Kelly Criterion and Fractional Kelly sizing to single bets and multi-asset portfolios.
- Construct decision trees under uncertainty to evaluate asymmetrical payoff structures and option overlays.

## Core concepts

### 1. Expected Value and R-Multiple Expectancy

Every trade outcome can be expressed as a multiple of the initial risk unit ($R$), where $1R$ is the dollar amount risked between entry price and initial stop invalidation:
$$R = |P_{\text{entry}} - P_{\text{stop}}| \times \text{Position Size}$$
Let a strategy have win rate $W$ (probability of a profitable trade) and loss rate $L = 1 - W$.
Let $\bar{R}_w$ be the average profit on winning trades expressed in $R$, and let $\bar{R}_l$ be the average loss on losing trades (conventionally $-1.0R$ with strict stops).
The **Expectancy** ($E$) per trade is:
$$E = (W \times \bar{R}_w) - (L \times |\bar{R}_l|)$$
For a trade setup to have statistical edge, its Expectancy must be strictly positive: $E > 0$.

```
+-----------------------------------------------------------------------+
|                    EXPECTANCY MATRIX (WIN RATE VS PAYOFF)             |
+-----------------------------------------------------------------------+
| Win Rate (W) | Avg Win (R) | Avg Loss (R) | Expectancy (E) | Break-even W |
|--------------+-------------+--------------+----------------+--------------|
| 30% (Trend)  | 4.0R        | 1.0R         | +0.50R         | 20.00%       |
| 40% (Swing)  | 2.5R        | 1.0R         | +0.40R         | 28.57%       |
| 50% (Equiv)  | 1.5R        | 1.0R         | +0.25R         | 40.00%       |
| 70% (Scalp)  | 0.5R        | 1.0R         | +0.05R         | 66.67%       |
| 90% (Option) | 0.1R        | 1.5R         | -0.06R         | 93.75%       |
+-----------------------------------------------------------------------+
```

The rows are hypothetical; the last column is the win rate at which each payoff pair breaks even, $|\bar{R}_l| / (\bar{R}_w + |\bar{R}_l|)$, and the margin between it and the actual win rate shows how fragile each edge is.
High win-rate strategies with negative skew (e.g. collecting small option premiums while bearing large tail risk) can have negative expected value despite appearing profitable over short samples.

### 2. Variance Drag and the Geometric Mean

Portfolio equity compounds multiplicatively over time rather than additively.
Let a portfolio experience independent, identically distributed annual returns $R_t$ with arithmetic mean $\mu = E[R]$ and variance $\sigma^2 = \text{Var}(R)$.
By Taylor series expansion of the logarithmic growth rate, the compound annual geometric growth rate $R_{\text{geo}}$ is approximately:
$$R_{\text{geo}} = \left(\prod_{t=1}^T (1 + R_t)\right)^{1/T} - 1 \approx \mu - \frac{1}{2}\sigma^2$$
The term $\frac{1}{2}\sigma^2$ is known as **Variance Drag** or **Volatility Drag**:

```
+-----------------------------------------------------------------------+
|                       THE GEOMETRIC EROSION OF VOLATILITY             |
+-----------------------------------------------------------------------+
| Sequence A: Flat Return (+10%, +10%)                                  |
| Arithmetic Return = +10.0%, Variance = 0.0                            |
| Final Wealth = 1.00 * 1.10 * 1.10 = 1.210 (+21.0% Total)              |
|                                                                       |
| Sequence B: Volatile Return (+50%, -30%)                              |
| Arithmetic Return = (+50% - 30%) / 2 = +10.0%                         |
| Variance = 0.16 (standard deviation 40%)                              |
| Final Wealth = 1.00 * 1.50 * 0.70 = 1.050 (+5.0% Total)               |
|                                                                       |
| Sequence C: Extreme Return (+100%, -50%)                              |
| Arithmetic Return = (+100% - 50%) / 2 = +25.0%                        |
| Final Wealth = 1.00 * 2.00 * 0.50 = 1.000 (0.0% Break-even)          |
+-----------------------------------------------------------------------+
```

Even if a strategy exhibits a positive arithmetic return, excessive volatility can reduce its long-term geometric compounding rate to zero or negative.
The approximation is only good for small returns: for Sequence B (population variance 0.16) it gives $0.10 - 0.08 = 2.00\%$ a period against an exact geometric rate of $\sqrt{1.05} - 1 = 2.47\%$, and for Sequence C (variance 0.5625) it gives $-3.125\%$ against an exact $0.00\%$.

### 3. Probability Calibration and the Brier Score

A market forecaster's skill is evaluated through **Calibration**: does an event occur $X\%$ of the time when the forecaster predicts an $X\%$ probability?
Glenn Brier (1950) formulated the **Brier Score** ($BS$) to evaluate probabilistic forecasts:
$$BS = \frac{1}{N} \sum_{i=1}^N (f_i - o_i)^2$$
where $f_i \in [0, 1]$ is the forecasted probability, and $o_i \in \{0, 1\}$ is the realized binary outcome (1 for success, 0 for failure).
The Brier Score ranges from 0.0 (perfect foresight) to 1.0 (completely inaccurate).
Murphy (1973) showed that, when forecasts are grouped by their distinct values, the Brier Score decomposes exactly into three components:
$$BS = \text{Uncertainty} - \text{Resolution} + \text{Reliability}$$
- **Reliability (Calibration Error)**: Measures how close forecast probabilities are to observed conditional frequencies (closer to 0 is better).
- **Resolution**: Measures how much the forecasts deviate from the base rate to distinguish different outcome distributions (higher is better).
- **Uncertainty**: The inherent irreducible variance of the underlying event $\bar{o}(1 - \bar{o})$.

### 4. The Kelly Criterion and Sizing

John L. Kelly Jr. (1956) derived the optimal fraction of wealth ($f^*$) to allocate to a succession of independent bets with edge to maximize the expected logarithm of terminal wealth:
$$f^* = \frac{p \cdot b - q}{b} = \frac{p(b + 1) - 1}{b}$$
where $p$ is the probability of winning, $q = 1 - p$ is the probability of losing, and $b$ is the payoff odds ($b = \frac{\text{Net Win}}{\text{Amount Bet}}$).
For a simple binary bet with 1-to-1 odds ($b = 1$):
$$f^* = p - q = 2p - 1$$
If a trader has a 60% win rate ($p = 0.60$) on an even-money bet, the Kelly optimal fraction is:
$$f^* = 0.60 - 0.40 = 0.20 \quad (20\% \text{ of equity})$$

```
+-----------------------------------------------------------------------+
|                    THE KELLY GROWTH VS OVER-BETTING CLIFF             |
+-----------------------------------------------------------------------+
| Growth Rate g(f)                                                      |
|       ^                                                               |
|       |                     Peak at f* (Full Kelly)                   |
|       |                        *                                      |
|       |                      *   *                                    |
|       |      Half-Kelly    *       *                                  |
|       |         o        *           *                                |
|       |       *   *    *               *                              |
|       |     *       *                    *                            |
|       |   *                                *                          |
|   ----+--------------------------------------+--------------------> f |
|   0.0 |                                      | ~2*f* (Zero Growth)   |
|       v                                      v                        |
+-----------------------------------------------------------------------+
```

Betting beyond the Kelly threshold ($f > f^*$) yields less compound growth while dramatically increasing volatility.
For this bet the growth rate is $g(f) = 0.60 \ln(1 + f) + 0.40 \ln(1 - f)$, which peaks at $g(0.20) = 0.0201$ per bet.
Betting twice Kelly gives $g(0.40) = 0.60 \ln(1.40) + 0.40 \ln(0.60) = 0.2019 - 0.2043 = -0.0024$, and the exact zero crossing is $f \approx 0.389$.
The continuous approximation puts that crossing at exactly $2f^*$; for discrete bets it sits near, not at, $2f^*$.
Past the crossing, log wealth drifts downward and wealth converges to zero with probability 1 even though each bet has a positive edge.
**Fractional Kelly** (for example $0.25f^*$ to $0.50f^*$) is the standard remedy for parameter estimation error and non-stationary markets (Thorp 2006; see [Position Sizing and Ruin](02-Position-Sizing-and-Ruin.md)).

---

## Worked examples

### Example 1: Calculating Brier Score for a Directional Breakout Setup
A quantitative trader evaluates 5 trading predictions where breakout probability was assessed at 70% ($f_i = 0.70$).
The actual binary outcomes were: Trade 1 = Win (1), Trade 2 = Win (1), Trade 3 = Loss (0), Trade 4 = Win (1), Trade 5 = Win (1).
The Brier Score calculation is:
$$\text{Squared Error}_1 = (0.70 - 1)^2 = (-0.30)^2 = 0.09$$
$$\text{Squared Error}_2 = (0.70 - 1)^2 = (-0.30)^2 = 0.09$$
$$\text{Squared Error}_3 = (0.70 - 0)^2 = (0.70)^2 = 0.49$$
$$\text{Squared Error}_4 = (0.70 - 1)^2 = (-0.30)^2 = 0.09$$
$$\text{Squared Error}_5 = (0.70 - 1)^2 = (-0.30)^2 = 0.09$$
$$\text{Sum of Squared Errors} = 0.09 + 0.09 + 0.49 + 0.09 + 0.09 = 0.85$$
$$BS = \frac{0.85}{5} = 0.170$$
The observed empirical frequency is $4 / 5 = 80\%$.
With one forecast value the Murphy decomposition is reliability $(0.70 - 0.80)^2 = 0.01$, resolution $0$ (every forecast is the same) and uncertainty $0.80 \times 0.20 = 0.16$, so $BS = 0.01 - 0 + 0.16 = 0.17$.
Five trades cannot establish calibration: a true 70% setup wins at least 4 of 5 with probability $52.82\%$, but so does a coin flip with probability $18.75\%$.

---

## Pitfalls

- **Neglecting Base Rates**: Forecasting trade success from a vivid chart pattern while ignoring the setup's measured historical hit rate.
- **Full Kelly Over-Betting**: Sizing positions at 100% of the theoretical Kelly formula, exposing capital to catastrophic drawdown when edge parameters are estimated with error.
- **Ignoring Compounding Asymmetry**: Forgetting that recovering from a 50% loss requires a 100% gain, while recovering from a 90% loss requires a 900% gain.
- **Confusing Probability with PnL Expectation**: Assuming a 90% win rate strategy is safe: with hypothetical wins of 0.5R, one 20R tail loss in 20 trades (5%) leaves the other 19 trades, at most $9.5R$, short of covering it.
- **Treating Market Draws as Independent Coin Tosses**: Failing to model the reality that financial market returns exhibit volatility clustering and autocorrelation.

---

## Interview questions

> [!question]- mkt-dec-001 | What is the mathematical definition of Expected Value (EV) in trading?
> The probability-weighted sum of all potential financial outcomes from an investment decision.

> [!question]- mkt-dec-002 | What is an R-multiple in trade risk management?
> The ratio of realized profit or loss on a trade relative to the initial dollar capital risked at entry.

> [!question]- mkt-dec-003 | If a strategy has a 40% win rate and an average win of 3R with a 1R loss, what is its expected value per trade?
> EV = (0.40 * 3.0R) - (0.60 * 1.0R) = 1.2R - 0.6R = +0.60R per trade.

> [!question]- mkt-dec-004 | What is variance drag in portfolio theory?
> The mathematical reduction in long-term geometric compound return caused by portfolio volatility: R_geo approx mu - 0.5 * sigma^2.

> [!question]- mkt-dec-005 | Why is a 50% loss not offset by an equal 50% subsequent gain?
> Because a 50% drop cuts capital in half ($100 to $50), requiring a 100% gain ($50 to $100) to return to original capital.

> [!question]- mkt-dec-006 | What is the Brier Score used for in probabilistic forecasting?
> To measure the accuracy of probabilistic predictions against realized binary outcomes, calculated as the mean squared error.

> [!question]- mkt-dec-007 | What is the range of possible values for a standard Brier Score?
> From 0.0 (perfect foresight and calibration) to 1.0 (completely incorrect forecasts).

> [!question]- mkt-dec-008 | What are the three components of the Murphy decomposition of the Brier Score?
> Uncertainty, Resolution, and Reliability (calibration error).

> [!question]- mkt-dec-009 | What is probability calibration?
> The degree of agreement between estimated forecast probabilities and the actual long-run observed frequencies of the event.

> [!question]- mkt-dec-010 | What is the Kelly Criterion formula for an even-money (1-to-1) bet with win probability p?
> f* = p - q = 2p - 1, where q = 1 - p.

> [!question]- mkt-dec-011 | What happens mathematically if an investor consistently sizes positions at twice the Kelly optimal fraction (2 * f*)?
> Expected log growth falls to about zero: exactly zero in the continuous approximation, slightly negative or positive for a discrete bet (g(0.40) = -0.0024 for an even-money bet with p = 0.60).
> The investor takes double Kelly's volatility for no compound growth, and any fraction past the zero crossing drives wealth to zero with probability 1.

> [!question]- mkt-dec-012 | Why do quantitative funds deploy Fractional Kelly (such as Half-Kelly) rather than Full Kelly?
> To buffer against parameter estimation errors, market regime shifts, and non-Gaussian fat-tailed drawdowns.

> [!question]- mkt-dec-013 | What is Base Rate Neglect in probabilistic reasoning?
> The cognitive tendency to overweight specific case evidence while ignoring the general prior probability of the underlying event.

> [!question]- mkt-dec-014 | What is a decision tree under uncertainty?
> A graphical model branching decision paths with associated conditional probabilities, costs, and terminal payoff values.

> [!question]- mkt-dec-015 | How does asymmetric payoff alter the required win rate for profitability?
> The break-even win rate is 1 / (1 + W_R): at 5R it is 1/6 = 16.7%, so a 20% win rate already earns 0.20 * 5 - 0.80 = +0.20R per trade before costs.

> [!question]- mkt-dec-016 | What is the Profit Factor of a trading track record?
> The ratio of gross trading profits divided by gross trading losses over a given period.

> [!question]- mkt-dec-017 | What is the minimum acceptable Profit Factor for an institutional trading strategy?
> There is no published industry minimum; any threshold such as 1.5 is a house rule.
> What matters is that the profit factor stays above 1.00 after costs, out of sample, by more than its sampling error, which needs enough trades to measure.

> [!question]- mkt-dec-018 | What is the difference between risk and uncertainty according to Frank Knight (1921)?
> Risk has known outcome distributions with calculable probabilities; uncertainty involves outcomes where probabilities cannot be known.

> [!question]- mkt-dec-019 | What is the Gambler's Fallacy in probability?
> Believing that independent random events will compensate for past imbalances (e.g. thinking a coin must land heads after five tails).

> [!question]- mkt-dec-020 | What is the Hot-Hand Fallacy?
> Falsely assuming that a streak of successful random outcomes indicates a higher future probability of success.

> [!question]- mkt-dec-021 | What is the Law of Large Numbers in quantitative trading?
> As the number of independent trades approaches infinity, the realized average return converges to the true theoretical expected value.

> [!question]- mkt-dec-022 | What is a negative skew payoff distribution?
> A distribution characterized by frequent small gains punctuated by occasional catastrophic, unhedged losses.

> [!question]- mkt-dec-023 | What is a positive skew payoff distribution?
> A distribution characterized by frequent small, managed losses offset by infrequent, massive outlier profits (e.g. trend following).

> [!question]- mkt-dec-024 | How does volatility drag affect leveraged ETFs (such as 3x bull funds)?
> Daily rebalancing makes the fund's multi-day return path-dependent: in choppy markets it lags 3x the index return, while in steady trends it can beat it.
> If the index rises 10% and then falls 9.09% (back to where it started), a 3x daily fund ends down 5.45%.

> [!question]- mkt-dec-025 | What is Monte Carlo simulation used for in portfolio risk assessment?
> Resampling or simulating many return paths (for example random reorderings or bootstraps of historical trades) to estimate the distribution of drawdowns and the risk of ruin, not just a single historical path.

> [!question]- mkt-dec-026 | What is the Risk of Ruin in gambling and trading mathematics?
> The statistical probability that an account equity will drop to a level where trading can no longer continue.

> [!question]- mkt-dec-027 | How does increasing position size affect the Risk of Ruin?
> With fixed-dollar even-money bets of a fraction f of starting equity, ruin is R = (q / p)^(1 / f), so it rises steeply with size.
> At p = 0.55, risking 2% gives (0.45 / 0.55)^50 = 0.0044% while risking 10% gives (0.45 / 0.55)^10 = 13.4%.

> [!question]- mkt-dec-028 | What is a calibration curve in probabilistic forecasting?
> A plot of predicted probabilities on the x-axis against observed empirical frequencies on the y-axis; a perfect model traces a 45-degree line.

> [!question]- mkt-dec-029 | What is the Ergodicity Problem in economics and finance (Peters 2019)?
> The time average of an individual wealth path does not equal the ensemble average across an entire population under non-ergodic multiplicative compounding.

> [!question]- mkt-dec-030 | Why is survivorship bias dangerous in historical strategy analysis?
> Because a sample of only surviving funds or stocks excludes the failures, so it overstates the historical return of the strategy.

> [!question]- mkt-dec-031 | What is maximum favorable excursion (MFE)?
> The maximum unrealized profit achieved by a trade prior to position exit, used to optimize profit targets.

> [!question]- mkt-dec-032 | What is the golden rule of probabilistic capital allocation?
> Never risk a non-zero probability of total ruin for an outcome of bounded incremental gain.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_trd_06_probability.py`](../../code/mkt_trd_06_probability.py) prints and asserts every number on this page: the expectancy matrix and break-even win rates in exact fractions checked by bisection, the variance-drag sequences by compounding against the Taylor approximation, the Brier score directly and through Murphy's binned decomposition, the binomial tail probabilities by exact enumeration and by seeded simulation within five standard errors, the Kelly growth rates by compounding a trade ledger with the zero crossing by bisection, ruin probabilities by an absorbing Markov chain, and the leveraged-ETF path by daily compounding.
- Related notes: [Position Sizing and Ruin](02-Position-Sizing-and-Ruin.md), [Retail Base Rates and Costs](01-Retail-Base-Rates-and-Costs.md), [Trading Psychology and Performance](05-Trading-Psychology-and-Performance.md).

## Further reading

- Brier, G. W. (1950). *Verification of Forecasts Expressed in Terms of Probability*. Monthly Weather Review, 78(1), 1-3.
- Kelly, J. L. (1956). *A New Interpretation of Information Rate*. Bell System Technical Journal, 35(4), 917-926.
- Murphy, A. H. (1973). *A New Vector Partition of the Probability Score*. Journal of Applied Meteorology, 12(4), 595-600.
- Knight, F. H. (1921). *Risk, Uncertainty and Profit*. Houghton Mifflin.
- Peters, O. (2019). *The ergodicity problem in economics*. Nature Physics, 15(12), 1216-1221.
- Taleb, N. N. (2001). *Fooled by Randomness: The Hidden Role of Chance in Life and in the Markets*. Texere.
- Thorp, E. O. (2006). *The Kelly criterion in blackjack, sports betting, and the stock market*. In Handbook of Asset and Liability Management, Volume 1 (pp. 385-428). North-Holland.
- Thorp, E. O. (1969). *Optimal Gambling Systems for Favorable Games*. Review of the International Statistical Institute, 37(3), 273-293.
