---
type: concept
title: "Oscillators, Mean Reversion Regimes, and the Multiple Testing Hazard"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [technical-analysis, oscillators, rsi, macd, bollinger-bands, mean-reversion, overfitting, data-snooping]
prereqs: []
---

# Oscillators, Mean Reversion Regimes, and the Multiple Testing Hazard

Bounded price oscillators - such as the Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), Bollinger Bands, and Stochastics - represent the most heavily utilized technical tools in retail trading.
Designed to identify overextended price moves and predict mean-reverting turning points, oscillators calculate momentum and volatility relative to fixed mathematical bounds.
No study cited in this note shows that fixed overbought and oversold thresholds earn positive risk-adjusted returns after costs, and careful tests of large rule universes show how easily such evidence is manufactured.
Sullivan, Timmermann and White (1999) bootstrapped thousands of simple technical rules on the Dow Jones Industrial Average and found that the best rule's apparent significance did not carry over to their 1987 to 1996 out-of-sample period once the whole search was accounted for.
Two structural problems matter: an oscillator can stay "overbought" or "oversold" for as long as a trend lasts, and every parameter tried adds to the data-snooping bias.
This note formalizes oscillator mathematics, demonstrates how to condition mean reversion on market regimes, and details statistical frameworks for overcoming the multiple testing hazard.

---

## TL;DR

Oscillators quantify where current price sits relative to its recent range (Stochastics), relative price changes (RSI), or moving average spreads (MACD).
Static threshold rules (e.g. buy when RSI $< 30$, sell when RSI $> 70$) have no published support as a stand-alone edge, and a drifting price centres RSI above 50 (about 62.3 for normal changes with mean 0.2 sigma) for as long as the drift lasts.
Regime filters (low ADX, a variance ratio below one, a Hurst exponent $H < 0.5$) are hypotheses to test, and every filter and threshold tried counts as another trial.
Furthermore, backtesting thousands of indicator lookback combinations without adjusting for multiple testing creates illusory alpha; frameworks such as White's Reality Check, Hansen's SPA, and the Deflated Sharpe Ratio (DSR) must be applied to penalize data-mined parameter fits.

---

## Learning objectives

- Formulate the mathematical definitions of RSI, MACD, Bollinger Bands, and the Stochastic Oscillator.
- Analyze the failure modes of static overbought/oversold boundaries in trending market regimes.
- Construct regime-conditioned mean-reversion strategies using the Hurst exponent and Average Directional Index (ADX).
- Quantify data-snooping bias and calculate the Harvey-Liu-Zhu $t$-statistic hurdle ($t > 3.0$) for multiple testing.
- Compute the Deflated Sharpe Ratio (DSR) to evaluate whether an optimized oscillator strategy is genuinely robust.

---

## Core concepts

### 1. Mathematical Formulation of Primary Oscillators

1. **Relative Strength Index (RSI, Wilder 1978)**:
   - Evaluates the ratio of upward price changes to downward price changes over an $N$-period lookback (conventionally $N = 14$):
     $$U_t = \max(0, P_t - P_{t-1}), \quad D_t = \max(0, P_{t-1} - P_t)$$
   - Wilder utilized a modified exponential smoothing (equivalent to an EMA with $\alpha = 1/N$):
     $$\overline{U}_t = \frac{1}{N} U_t + \left(1 - \frac{1}{N}\right) \overline{U}_{t-1}, \quad \overline{D}_t = \frac{1}{N} D_t + \left(1 - \frac{1}{N}\right) \overline{D}_{t-1}$$
   - Relative Strength ($RS$) and the bounded index ($RSI \in [0, 100]$):
     $$RS_t = \frac{\overline{U}_t}{\overline{D}_t}, \quad \text{RSI}_t = 100 - \frac{100}{1 + RS_t} = 100 \times \frac{\overline{U}_t}{\overline{U}_t + \overline{D}_t}$$
   - **Range shift**: Wilder's averages converge to the mean up move $\mathbb{E}[U]$ and mean down move $\mathbb{E}[D]$, so a drifting price shifts the whole RSI range.
     For normal daily changes with mean $0.2\sigma$ (a hypothetical strong trend), $\mathbb{E}[U] = 0.5069\sigma$ and $\mathbb{E}[D] = 0.3069\sigma$, so RSI oscillates around $100 \times 0.5069 / (0.5069 + 0.3069) = 62.3$ rather than 50.
     Practitioner band rules (for example "40 to 80 in a bull market") are heuristics without a published test.

2. **Moving Average Convergence Divergence (MACD, Gerald Appel, late 1970s)**:
   - Measures the difference between two exponential moving averages (conventionally 12-day and 26-day):
     $$\text{MACD Line}_t = \text{EMA}_{12}(P_t) - \text{EMA}_{26}(P_t)$$
   - The **Signal Line** is an EMA of the MACD line (conventionally 9-day):
     $$\text{Signal Line}_t = \text{EMA}_9(\text{MACD Line}_t)$$
   - The **MACD Histogram** plots the spread between the two lines:
     $$\text{Histogram}_t = \text{MACD Line}_t - \text{Signal Line}_t$$
   - A divergence occurs when price makes a higher high while the MACD peak makes a lower high, signaling waning momentum.

3. **Bollinger Bands (John Bollinger, 1980s)**:
   - Envelopes plotted at $k$ standard deviations around an $N$-day simple moving average (conventionally $N = 20, k = 2$); Bollinger specifies the population standard deviation (divide by $N$, not $N - 1$):
     $$\text{Middle Band}_t = \text{SMA}_{20}(P_t)$$
     $$\text{Upper Band}_t = \text{SMA}_{20}(P_t) + 2 \times \sigma_{20}(P_t)$$
     $$\text{Lower Band}_t = \text{SMA}_{20}(P_t) - 2 \times \sigma_{20}(P_t)$$
   - **BandWidth**: Measures relative volatility:
     $$\text{BandWidth}_t = \frac{\text{Upper Band}_t - \text{Lower Band}_t}{\text{Middle Band}_t}$$
   - **The Squeeze**: An extreme contraction in BandWidth marks volatility compression.
     Because volatility clusters and mean-reverts, low volatility tends to be followed by higher volatility, but the squeeze says nothing about the direction of the next move.

4. **Stochastic Oscillator (associated with George Lane)**:
   - Bounded location of closing price within the high-low range over $N$ periods:
     $$\%K_t = \frac{P_t - \min(L_{t-N+1}, \dots, L_t)}{\max(H_{t-N+1}, \dots, H_t) - \min(L_{t-N+1}, \dots, L_t)} \times 100$$
     $$\%D_t = \text{SMA}_3(\%K_t)$$

### 2. The Trend Trap: Why Static Oscillators Fail

```
+---------------------------------------------------------------------------------+
|                       THE STATIC OSCILLATOR TREND TRAP                          |
+---------------------------------------------------------------------------------+
|  Price ($)                                                                      |
|  140 |                                                       / (Parabolic Rally)|
|  130 |                                               /\     /                   |
|  120 |                                       /\     /  \   /                    |
|  110 |                               /\     /  \   /    \ /                     |
|  100 |                       /\     /  \   /    \ /                             |
|   90 |               /\     /  \   /    \ /                                     |
+---------------------------------------------------------------------------------+
|  RSI                                                                            |
|   80 |               ---\---/-------\---/---------\---/----- (Pinned > 70)      |
|   70 | - - - - - - - - - X - - - - - X - - - - - - X - - - - Overbought Line    |
|      |                  [Short 1]   [Short 2]     [Short 3]                     |
|   30 | - - - - - - - - - - - - - - - - - - - - - - - - - - - Oversold Line      |
+---------------------------------------------------------------------------------+
|  Outcome (hypothetical): a trader who shorts each 'overbought' signal is run    |
|  over as price rallies from 100 to 140 (+40%) while RSI stays near 80.          |
+---------------------------------------------------------------------------------+
```

- In a persistent uptrend, up moves outweigh down moves in Wilder's averages, so RSI stays high, and closes near the top of the range keep Stochastics near $100$.
- A high reading therefore describes the trend that has already happened; it is not by itself evidence of a coming reversal.

### 3. Regime Conditioning: Restoring Mean-Reversion Edge

A common design restricts oscillator signals to regimes that look range-bound; whether that restores an edge is an empirical question for each market, tested out of sample:

1. **Hurst Exponent ($H$)**:
   - Evaluates the scaling of the rescaled range $R/S$ against time horizon $n$: $\mathbb{E}[R/S] \propto n^H$.
   - $H = 0.5$: independent increments (a random walk, no memory).
   - $H > 0.5$: persistent increments (trending).
   - $H < 0.5$: anti-persistent increments (mean-reverting).
   - Classical R/S is biased by short-range dependence; Lo (1991) proposed a modified R/S statistic and found little evidence of long-range memory in US stock returns once short-range dependence is allowed for.

2. **Average Directional Index (ADX) Filter**:
   - Developed by J. Welles Wilder (1978), ADX measures trend strength independent of direction ($0$ to $100$).
   - A filter such as "disable fades when ADX is above 25" uses a practitioner threshold, not a tested constant; the threshold is a parameter and counts as a trial.

### 4. The Multiple Testing Hazard & Overfitting Controls

When a researcher tests $N$ indicator variations (varying lookback periods, thresholds, stop losses), standard statistical inference collapses:

1. **The Data-Snooping Fallacy**:
   - At a significance level $\alpha = 0.05$, testing $20$ independent strategies with no edge produces $20 \times 0.05 = 1$ false positive on average, and at least one with probability $1 - 0.95^{20} = 64.2\%$.
   - If a researcher evaluates $1,000$ independent no-edge variants, about $50$ will pass a two-sided test at $|t| > 1.96$.

2. **The Harvey, Liu, and Zhu (2016) Hurdle**:
   - In *... and the Cross-Section of Expected Returns*, Campbell Harvey, Yan Liu, and Heqing Zhu catalogued $316$ published factors.
   - They argue that a newly proposed factor should clear a $t$-statistic above $3.0$ rather than $2.0$ (a two-sided $p$-value below $0.0027$), and that most claimed findings in financial economics are likely false.

3. **Deflated Sharpe Ratio (DSR, Bailey and Lopez de Prado 2014)**:
   - DSR adjusts the estimated Sharpe ratio $\widehat{\text{SR}}$ to account for the number of trials $N$, the variance of trial returns, non-normality (skewness $\gamma_3$, kurtosis $\gamma_4$), and sample length $T$:
     $$\text{DSR} = Z\left(\frac{(\widehat{\text{SR}} - \text{SR}^*) \sqrt{T-1}}{\sqrt{1 - \gamma_3 \widehat{\text{SR}} + \frac{\gamma_4 - 1}{4} \widehat{\text{SR}}^2}}\right)$$
   - where $\gamma_4$ is raw kurtosis ($3$ for a normal distribution), and $\text{SR}^*$ is the expected maximum Sharpe ratio under the null hypothesis of zero true edge across $N$ independent trials whose Sharpe ratios have standard deviation $\sigma_{\text{SR}}$:
     $$\text{SR}^* \approx \sigma_{\text{SR}} \left[(1 - \gamma) \Phi^{-1}\left(1 - \frac{1}{N}\right) + \gamma \Phi^{-1}\left(1 - \frac{1}{N e}\right)\right]$$
   - Here $\gamma \approx 0.5772$ is the Euler-Mascheroni constant and $\Phi^{-1}$ is the inverse standard normal CDF.
   - $\widehat{\text{SR}}$, $\text{SR}^*$ and $\sigma_{\text{SR}}$ must be in the same per-observation units as $T$.
   - At a 95% confidence level, a DSR below $0.95$ means the observed Sharpe ratio is not significantly above what the best of $N$ no-skill trials would show.

---

## Worked examples

### Example 1: Calculating Wilder's 14-Period RSI

An analyst calculates 14-period RSI; the first five closes show how $U$ and $D$ are formed:
- Days 1 to 5 Closes: $\$100.00, \$102.00, \$101.00, \$104.00, \$106.00$.
- Daily Changes:
  - Day 2: $+\$2.00 \implies U = 2.00, D = 0.00$.
  - Day 3: $-\$1.00 \implies U = 0.00, D = 1.00$.
  - Day 4: $+\$3.00 \implies U = 3.00, D = 0.00$.
  - Day 5: $+\$2.00 \implies U = 2.00, D = 0.00$.
- Over the full initial 14-day sample (not shown), suppose the simple averages are:
  - Average Gain: $\overline{U} = \$1.20$.
  - Average Loss: $\overline{D} = \$0.40$.

1. **Calculate Relative Strength ($RS$)**:
   $$RS = \frac{\overline{U}}{\overline{D}} = \frac{1.20}{0.40} = 3.00$$

2. **Compute Bounded RSI**:
   $$\text{RSI} = 100 - \frac{100}{1 + RS} = 100 - \frac{100}{1 + 3.00} = 100 - \frac{100}{4.00} = 100 - 25.00 = 75.00$$
   The asset prints an RSI of $75.00$, above the conventional $70.00$ threshold.

3. **Apply one step of Wilder smoothing** after a further $+\$1.00$ day:
   $$\overline{U} = \frac{13 \times 1.20 + 1.00}{14} = 1.1857, \quad \overline{D} = \frac{13 \times 0.40 + 0}{14} = 0.3714, \quad \text{RSI} = 100 \times \frac{\overline{U}}{\overline{U} + \overline{D}} = 76.15$$

### Example 2: Evaluating Deflated Sharpe Ratio Across Multiple Strategy Trials

A quantitative trader backtests $N = 500$ parameter variations of an RSI and Bollinger Band mean-reversion model on 5 years of daily data ($T = 1,260$ days):
- Best in-sample annualized Sharpe ratio: $\widehat{\text{SR}} = 1.40$ (daily $\widehat{\text{sr}} = \frac{1.40}{\sqrt{252}} = 0.0882$).
- Variance of trial Sharpe ratios: $\sigma_{\text{SR}}^2 = 0.25$ ($\sigma_{\text{SR}} = 0.50$).
- Daily returns exhibit negative skewness ($\gamma_3 = -0.60$) and excess kurtosis of $4.50$, so raw kurtosis is $\gamma_4 = 4.50 + 3 = 7.50$.

1. **Calculate Expected Maximum Sharpe Ratio Under Zero Edge ($\text{SR}^*$)**:
   $$\Phi^{-1}\left(1 - \frac{1}{500}\right) = 2.8782, \quad \Phi^{-1}\left(1 - \frac{1}{500 e}\right) = 3.1802$$
   $$\mathbb{E}[\max] \approx (1 - 0.5772)(2.8782) + 0.5772(3.1802) = 3.0525\text{ standard deviations}$$
   The exact expected maximum of 500 independent standard normals, by numerical integration, is about $3.04$, so the approximation is close.
   Annualized benchmark hurdle:
   $$\text{SR}^*_{\text{ann}} = 0.50 \times 3.0525 = 1.526, \quad \text{SR}^*_{\text{daily}} = \frac{1.526}{\sqrt{252}} = 0.0961$$

2. **Evaluate the Strategy**:
   - The best in-sample Sharpe ratio ($\widehat{\text{SR}} = 1.40$) is **lower** than the expected maximum Sharpe ratio from testing 500 random variations ($\text{SR}^* \approx 1.53$).
   - With $\gamma_3 = -0.60$ and $\gamma_4 = 7.50$, the denominator is $\sqrt{1 + 0.60 \times 0.0882 + \frac{7.50 - 1}{4} \times 0.0882^2} = 1.0323$.
   - $$\text{DSR} = Z\left(\frac{(0.0882 - 0.0961)\sqrt{1,259}}{1.0323}\right) = Z(-0.27) = 0.39$$
   - **Verdict**: The strategy is rejected at the 95% level.
   - The best of 500 trials looks no better than the best of 500 no-skill trials would be expected to look, so the backtest gives no evidence of an edge.

---

## Pitfalls

- **Fading Momentum in Strong Trends**:
  Shorting a stock simply because its RSI is high in a strong trend bets against the very drift that produced the reading.
  A high RSI describes past up moves; it is not by itself evidence of a reversal.
- **Neglecting Transaction Costs in High-Frequency Oscillators**:
  Short-lookback oscillators cross their thresholds often, so they trade often.
  Bid-ask spreads, exchange fees, and execution slippage are paid on every round trip and must be in the backtest.
- **Overfitting Indicator Parameters to Noise**:
  Optimizing lookback windows (for example, a hypothetical finding that 13-day RSI beat 14-day RSI by $2\%$ in-sample) is curve-fitting unless it survives out of sample.
  If a strategy shows profit only at one non-standard parameter, treat the edge as spurious until proven otherwise.
- **Unbounded Divergence Trading**:
  Trading MACD or RSI divergences without defined stop-loss invalidation is hazardous.
  Divergences can persist and cascade through multiple peaks before a reversal occurs.

---

## Interview questions

> [!question]- mkt-ta-129 | What is the mathematical formulation of Wilder's Relative Strength Index (RSI)?
> RSI = 100 - (100 / (1 + RS)), where RS = Average_Gain / Average_Loss smoothed using Wilder's EMA: alpha = 1 / N.
> It bounds momentum on a 0 to 100 scale, measuring relative internal price change velocity.

> [!question]- mkt-ta-130 | Why do static overbought (> 70) and oversold (< 30) RSI rules fail in trending markets?
> A drift makes average up moves larger than average down moves, so Wilder's averages keep RSI high (or low) for as long as the trend lasts.
> Fading each extreme bets against the drift that produced it; with normal daily changes of mean 0.2 sigma, RSI centres near 62.3, not 50.

> [!question]- mkt-ta-131 | What is the RSI range shift, and which part of it is mechanical rather than folklore?
> In a trend RSI oscillates in a shifted band: Wilder's averages converge to the mean up and down moves, so a positive drift centres RSI above 50 (62.3 for normal changes with mean 0.2 sigma).
> Specific practitioner bands such as "40 to 80 in a bull market" are untested heuristics.

> [!question]- mkt-ta-132 | How is the Moving Average Convergence Divergence (MACD) constructed?
> MACD Line = EMA_12 - EMA_26.
> Signal Line = EMA_9(MACD Line).
> MACD Histogram = MACD Line - Signal Line.

> [!question]- mkt-ta-133 | What is a MACD zero-line crossover and what does it indicate?
> When the MACD line crosses above zero, it indicates that the 12-day EMA has crossed above the 26-day EMA (equivalent to a fast moving average golden cross).
> A cross below zero signals that short-term moving average momentum is negative.

> [!question]- mkt-ta-134 | How are Bollinger Bands calculated?
> Middle Band = 20-day SMA.
> Upper Band = Middle Band + 2 * sigma_20.
> Lower Band = Middle Band - 2 * sigma_20, where sigma_20 is the 20-day population standard deviation (divide by N), as Bollinger specifies.

> [!question]- mkt-ta-135 | What is a Bollinger Band Squeeze?
> An extreme compression in BandWidth: (Upper - Lower) / Middle.
> It reflects low recent volatility; because volatility mean-reverts, expansion tends to follow, but the squeeze does not predict direction.

> [!question]- mkt-ta-136 | What is "walking the bands" in Bollinger Band analysis?
> A strong trending condition where price tags and continuously hugs the outer Bollinger Band without reverting to the middle band.
> Fading a band-walking market bets against the trend that is producing the walk.

> [!question]- mkt-ta-137 | What is %B in Bollinger Band indicators?
> %B = (Price - Lower_Band) / (Upper_Band - Lower_Band).
> It quantifies the exact location of price relative to the bands; %B > 1.0 indicates price is above the upper band.

> [!question]- mkt-ta-138 | How does the Stochastic Oscillator measure momentum?
> %K = (Price - Lowest_Low_N) / (Highest_High_N - Lowest_Low_N) * 100.
> It evaluates where the closing price resides relative to the high-low range over the past N periods.

> [!question]- mkt-ta-139 | What is a momentum divergence?
> A disagreement between price and an oscillator: price makes a higher high while the oscillator makes a lower high (bearish divergence), or price makes a lower low while the oscillator makes a higher low (bullish divergence).
> It indicates internal momentum deceleration.

> [!question]- mkt-ta-140 | What is hidden divergence?
> Trend-continuation divergence: price makes a higher low while the oscillator makes a lower low (bullish hidden divergence).
> It signals that pullbacks are experiencing rapid oscillator resets without structural price damage.

> [!question]- mkt-ta-141 | What is data-snooping bias in quantitative technical analysis?
> The statistical artifact where testing many trading rules on the same dataset inevitably identifies rules that performed well purely by random luck.
> In-sample performance reflects sample-specific noise rather than genuine predictive alpha.

> [!question]- mkt-ta-142 | What is White's Reality Check (White 2000)?
> A bootstrap procedure that constructs the empirical distribution of the maximum performance metric under the null hypothesis that no rule has true edge.
> It yields p-values that explicitly penalize for the size of the search universe.

> [!question]- mkt-ta-143 | What is Hansen's Superior Predictive Ability (SPA) test?
> An improvement over White's Reality Check developed by Peter Hansen (2005) that uses a studentized test statistic and centers the distribution.
> It reduces sensitivity to poor, irrelevant benchmark rules in the test universe.

> [!question]- mkt-ta-144 | Why did Harvey, Liu, and Zhu (2016) recommend raising the t-statistic threshold to t > 3.0?
> They catalogued 316 published factors and argued that, given how many have been tried, most claimed findings are likely false at the usual t > 2.0 bar.
> A threshold of t > 3.0 corresponds to a two-sided p-value below 0.0027.

> [!question]- mkt-ta-145 | What is the Deflated Sharpe Ratio (DSR)?
> A metric developed by Bailey and Lopez de Prado (2014) that discounts an observed Sharpe ratio based on the number of trials tested, sample length, skewness, and kurtosis.
> It computes the probability that the observed Sharpe ratio exceeds the expected maximum of random trials.

> [!question]- mkt-ta-146 | How does the Hurst Exponent (H) distinguish trending from mean-reverting regimes?
> H = 0.5 indicates a random walk; H > 0.5 persistent (trending) increments; H < 0.5 anti-persistent (mean-reverting) increments.
> Estimates are noisy and biased by short-range dependence (Lo 1991 modified R/S), so an H filter is a hypothesis to validate, not a guarantee.

> [!question]- mkt-ta-147 | What is the Average Directional Index (ADX) and how is it used as a regime filter?
> A non-directional trend strength indicator developed by Wilder (1978) that measures the magnitude of directional price movement.
> A filter disables mean-reversion fades above a chosen threshold (25 is a common practitioner choice); the threshold is a parameter to validate, not a constant.

> [!question]- mkt-ta-148 | What is the Commodity Channel Index (CCI, Lambert 1980)?
> CCI = (Typical_Price - SMA_20) / (0.015 * Mean_Deviation).
> The 0.015 constant makes the [-100, +100] band equal to 1.5 mean deviations: 1.197 sigma for normal deviations, a band that contains 76.9% of them.

> [!question]- mkt-ta-149 | What is the Williams %R indicator?
> Williams %R = (Highest_High_N - Price) / (Highest_High_N - Lowest_Low_N) * -100.
> It is the fast stochastic shifted down by 100 (%R = %K - 100), bounded between -100 and 0.

> [!question]- mkt-ta-150 | What is the False Discovery Rate (FDR) and the Benjamini-Hochberg procedure?
> A statistical framework that controls the expected proportion of false positive discoveries among all rejected null hypotheses.
> It provides an adaptive significance threshold for ranking large factor libraries.

> [!question]- mkt-ta-151 | What is look-ahead bias in oscillator backtesting?
> Using information from time t or t+1 (such as using the day's close before the bar has completed) to execute orders at time t.
> It produces artificially inflated backtest profits that are impossible to execute live.

> [!question]- mkt-ta-152 | What is survivorship bias and how does it distort technical backtests?
> Testing technical rules only on stocks that currently exist in an index, ignoring companies that went bankrupt or were delisted.
> It creates a massive positive performance bias by omitting catastrophic failure cases.

> [!question]- mkt-ta-153 | What is a parameter cliff in technical strategy optimization?
> When a slight change in an indicator parameter (e.g. changing lookback from 14 to 15) causes backtest performance to collapse.
> Parameter cliffs indicate extreme overfitting to historical noise rather than robust edge.

> [!question]- mkt-ta-154 | What is a parameter plateau?
> A broad region of neighboring parameter values (e.g. lookbacks from 12 to 18) that all yield consistent, stable profitability.
> Plateaus signal a robust structural phenomenon rather than an overfitted artifact.

> [!question]- mkt-ta-155 | How does bid-ask spread friction impact mean-reversion strategies?
> Mean-reversion oscillators trigger high trading frequency with small average profits per trade.
> Paying the bid-ask spread on every entry and exit rapidly consumes all theoretical gross alpha.

> [!question]- mkt-ta-156 | What is the Connors RSI (CRSI)?
> A composite oscillator from Connors Research: the average of a 3-period RSI of price, a 2-period RSI of the current up/down streak length, and the percent rank of the 1-day return over the last 100 days.
> It is designed specifically for short-term equities mean-reversion trading.

> [!question]- mkt-ta-157 | What is an Ornstein-Uhlenbeck (OU) process in mean-reversion modeling?
> A continuous-time stochastic process: dX_t = theta * (mu - X_t) dt + sigma * dW_t.
> It models mean reversion where price drifts back toward mean mu at rate theta.

> [!question]- mkt-ta-158 | What is the half-life of mean reversion?
> The expected time required for a mean-reverting process to decay halfway back to its long-term equilibrium: t_{1/2} = ln(2) / theta.
> Desks use half-life to set maximum holding periods and time-based stops.

> [!question]- mkt-ta-159 | What is probability of backtest overfitting (PBO)?
> A statistical measure developed by Bailey et al. (2017) using Combinatorially Symmetric Cross-Validation (CSCV).
> It quantifies the probability that the best in-sample strategy will underperform the median strategy out-of-sample.

> [!question]- mkt-ta-160 | Why should quantitative traders use walk-forward validation instead of standard cross-validation?
> Standard cross-validation randomly partitions data, so serially correlated observations and overlapping labels leak information between training and test folds.
> Walk-forward validation trains strictly on earlier data and tests on later data; purged and embargoed k-fold or CPCV (Lopez de Prado 2018) remove the leakage while using more of the data.

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_ta_05_oscillators.py`](../../code/mkt_ta_05_oscillators.py) prints and asserts every number on this page: the RSI example by a generic Wilder implementation on a constructed price series against exact fractions, the drift-shifted RSI level from normal partial moments checked by simulation, false-positive counts by the binomial pmf and the normal CDF by erf and quadrature, the expected maximum Sharpe ratio against the exact expected maximum of 500 normals by quadrature and simulation, the Sharpe standard error in the DSR denominator against simulated Sharpe estimates, and the CCI scaling by simulation.
- Related notes: [Quantitative Rule Validation and Calibration](08-Quantitative-Rule-Validation-and-Calibration.md) (PBO, CSCV and minimum track record length).

---

## Further reading

- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*. Trend Research.
- Appel, G. (2005). *Technical Analysis: Power Tools for Active Investors*. FT Prentice Hall.
- Bollinger, J. (2001). *Bollinger on Bollinger Bands*. McGraw-Hill.
- Lo, A. W. (1991). *Long-term memory in stock market prices*. Econometrica, 59(5), 1279-1313.
- Sullivan, R., Timmermann, A., & White, H. (1999). *Data-snooping, technical trading rule performance, and the bootstrap*. The Journal of Finance, 54(5), 1647-1691.
- White, H. (2000). *A reality check for data snooping*. Econometrica, 68(5), 1097-1126.
- Hansen, P. R. (2005). *A test for superior predictive ability*. Journal of Business & Economic Statistics, 23(4), 365-380.
- Bailey, D. H., & Lopez de Prado, M. (2014). *The deflated Sharpe ratio: Correcting for selection bias, backtest overfitting, and non-normality*. The Journal of Portfolio Management, 40(5), 94-107.
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). *... and the cross-section of expected returns*. The Review of Financial Studies, 29(1), 5-68.
- Bailey, D. H., Borwein, J., Lopez de Prado, M., & Zhu, Q. J. (2017). *The probability of backtest overfitting*. Journal of Computational Finance, 20(4), 39-69.
- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. John Wiley & Sons.
