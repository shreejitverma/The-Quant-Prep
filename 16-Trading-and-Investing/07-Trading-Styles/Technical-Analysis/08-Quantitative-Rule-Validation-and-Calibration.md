---
type: concept
title: "Quantitative Rule Validation, Brier Calibration, and Overfitting Control"
track: [quant-trader, quant-research]
tier: advanced
status: solid
est_hours: 1.5
tags: [technical-analysis, rule-validation, brier-score, calibration, overfitting, backtesting, murphy-decomposition]
prereqs: []
---

# Quantitative Rule Validation, Brier Calibration, and Overfitting Control

The primary dividing line between amateur chart reading and institutional quantitative trading is the scientific method.
Subjective chartist analysis relies on selective memory, hindsight rationalization, and narrative fallacy: every historical market top can be fitted with an apparent "Head and Shoulders" pattern after the crash has occurred.
In contrast, quantitative trading demands that every technical hypothesis be translated into an unambiguous, falsifiable algorithmic rule, tested across survivorship-free data, adjusted for multiple testing bias, and scored using mathematically proper calibration rules.
This note formalizes the statistical protocols required to validate technical rules, evaluate probabilistic chart forecasts, and eliminate backtest overfitting.

---

## TL;DR

A valid technical trading rule must possess complete algorithmic specification: exact numerical definitions of inputs, entries, stops, profit targets, and execution friction.
Probabilistic market forecasts (e.g. predicting the probability that price will exceed a resistance level) cannot be evaluated by simple directional hit rate; they must be evaluated using proper scoring rules where truth-telling is strictly optimal.
The Brier score ($B = \frac{1}{N} \sum (f_i - o_i)^2$) decomposes via Murphy's (1973) theorem into Reliability (calibration error), Resolution (discriminative power), and Uncertainty (inherent base rate entropy).
To prevent overfitting, backtesting must employ Combinatorially Symmetric Cross-Validation (CSCV) to compute the Probability of Backtest Overfitting (PBO) and calculate the Deflated Sharpe Ratio (DSR) to discount for the number of variant trials.

---

## Learning objectives

- Translate subjective visual chart patterns into objective, deterministic mathematical algorithms.
- Formulate the Brier score, logarithmic loss, and Murphy's (1973) three-component decomposition.
- Construct and interpret empirical probability calibration curves and compute Expected Calibration Error (ECE).
- Implement walk-forward out-of-sample validation protocols to detect strategy decay and overfitting.
- Calculate the Probability of Backtest Overfitting (PBO) and apply Deflated Sharpe Ratio hurdles.

---

## Core concepts

### 1. Falsifiability and Algorithmic Rule Specification

In the philosophy of science established by Karl Popper, an empirical theory must be falsifiable: there must exist potential observable outcomes that, if realized, prove the theory false.
Subjective chart analysis is frequently non-falsifiable because the chartist can always adjust trendlines or invoke unquantified "intuition" to explain away failed patterns.

```
+---------------------------------------------------------------------------------+
|                       FROM SUBJECTIVE CHARTING TO ALGORITHMIC RULE              |
+---------------------------------------------------------------------------------+
|  SUBJECTIVE CHANCE:                                                             |
|  "Buy when the stock looks like it is bouncing off support on good volume."     |
|                                                                                 |
|                                     |                                           |
|                                     v (Quantitative Translation)                |
|                                                                                 |
|  OBJECTIVE ALGORITHMIC SPECIFICATION:                                           |
|  1. Support Definition: 20-day swing low where Low_t < min(Low_{t-5..t-1})      |
|     and Low_t < min(Low_{t+1..t+5}).                                            |
|  2. Retest Condition: Price drops within 0.5% of Support without closing below. |
|  3. Volume Filter: Daily volume > 1.25 * SMA_50(Volume).                         |
|  4. Execution Trigger: Close > Open and Close > High_{t-1}.                     |
|  5. Stop Loss: Exactly Support - 1.0 * ATR_14(t).                               |
|  6. Target / Exit: +2.0R or trailing stop below 10-day EMA.                     |
+---------------------------------------------------------------------------------+
```

### 2. Proper Scoring Rules: Brier Score and Log Loss

When a trader makes probabilistic forecasts (e.g. "there is a $70\%$ probability that the S&P 500 will close higher over the next 5 days"), evaluating performance simply by win rate is mathematically flawed.
A trader who predicts $99\%$ confidence on a coin toss that happens to win is uncalibrated and reckless.

1. **The Brier Score (Brier 1950)**:
   - Evaluates the mean squared error between forecasted probabilities $f_i \in [0, 1]$ and binary realizations $o_i \in \{0, 1\}$ across $N$ events:
     $$\text{Brier} = \frac{1}{N} \sum_{i=1}^N (f_i - o_i)^2$$
   - Bounds:
     - $\text{Brier} = 0.0$: Perfect foresight (predicts $1.0$ when true and $0.0$ when false).
     - $\text{Brier} = 0.25$: Naive random guessing (predicts $0.50$ for every event).
     - $\text{Brier} = 1.0$: Complete inversion (predicts $1.0$ when false and $0.0$ when true).

2. **Murphy's (1973) Brier Score Decomposition**:
   Allan Murphy proved that the sample Brier score partitions into three orthogonal components:
   $$\text{Brier} = \text{Reliability} - \text{Resolution} + \text{Uncertainty}$$
   - **Uncertainty ($\bar{o}(1 - \bar{o})$)**: Inherent randomness of the event base rate $\bar{o} = \frac{1}{N} \sum o_i$.
     Beyond the forecaster's control; maximized at $0.25$ when outcomes are $50/50$.
   - **Reliability (Calibration Error)**:
     $$\text{Reliability} = \sum_{k=1}^K \frac{n_k}{N} (\bar{f}_k - \bar{o}_k)^2$$
     Measures how close the forecasted probabilities in bin $k$ match the actual observed event frequency $\bar{o}_k$.
     A well-calibrated trader has $\text{Reliability} \approx 0.0$.
   - **Resolution (Discriminative Power)**:
     $$\text{Resolution} = \sum_{k=1}^K \frac{n_k}{N} (\bar{o}_k - \bar{o})^2$$
     Measures how far the conditional outcome frequencies $\bar{o}_k$ deviate from the unconditional base rate $\bar{o}$.
     High resolution means the trader can reliably separate high-probability events from low-probability events.

3. **Logarithmic Score (Cross-Entropy Loss)**:
   $$\text{Log Loss} = -\frac{1}{N} \sum_{i=1}^N \left[o_i \ln(f_i) + (1 - o_i) \ln(1 - f_i)\right]$$
   - Severely penalizes overconfident wrong forecasts: predicting $f = 0.99$ on an event that fails ($o = 0$) incurs a loss of $-\ln(0.01) = 4.605$.

```
+---------------------------------------------------------------------------------+
|                       PROBABILITY CALIBRATION CURVE (RELIABILITY)               |
+---------------------------------------------------------------------------------+
|  Observed Relative Frequency                                                    |
|  1.0 |                                                     / (Perfect Line)     |
|      |                                                 *  /                     |
|  0.8 |                                               *   /                      |
|      |                                             *    /                       |
|  0.6 |                                           *     /                        |
|      |                                         *      /                         |
|  0.4 |                                       *       /                          |
|      |                                     *        /                           |
|  0.2 |                                   *         /                            |
|      |                           *      /                                       |
|  0.0 |__________________________*______/__________________________              |
|      0.0   0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9   1.0          |
|                       Forecasted Probability Bin                                |
+---------------------------------------------------------------------------------+
|  Overconfidence Curve (*): Forecasts 80% confidence, but events happen only 60%  |
|  Expected Calibration Error (ECE) = Weighted average vertical gap to 45 deg line |
+---------------------------------------------------------------------------------+
```

### 3. Out-of-Sample Validation Protocols

To test whether a technical rule has true predictive power, quantitative desks enforce strict validation structures:

1. **Walk-Forward Out-of-Sample Testing**:
   - The dataset is divided into alternating In-Sample (IS, training) and Out-of-Sample (OOS, testing) periods.
   - Parameters are optimized on IS data; the optimized parameters are applied forward to OOS data without changes.
   - The OOS results are concatenated into a contiguous out-of-sample track record.
   - **Degradation Ratio**:
     $$\text{Degradation} = \frac{\text{Sharpe}_{\text{OOS}}}{\text{Sharpe}_{\text{IS}}}$$
     A ratio below $0.50$ indicates severe overfitting.

2. **Combinatorially Symmetric Cross-Validation (CSCV) and PBO**:
   - Developed by David Bailey, Jonathan Borwein, Marcos López de Prado, and Qiji Jim Zhu (2016).
   - Generates $S$ combinations of IS/OOS splits, testing all strategy variants across each combination.
   - **Probability of Backtest Overfitting (PBO)**:
     $$\text{PBO} = \mathbb{P}(\text{Rank of Best IS Strategy in OOS} > \text{Median})$$
   - If $\text{PBO} > 0.50$, the strategy identified as "optimal" in-sample is more likely than not to underperform a random strategy out-of-sample.

### 4. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                       EVIDENCE LEDGER: VALIDATION & OVERFITTING                 |
+---------------------------------------------------------------------------------+
|  Phenomenon: Statistical Calibration & Overfitting Penalization                 |
|  Evidence Grade: METHODOLOGICAL CANON (Mathematical Truth)                      |
+---------------------------------------------------------------------------------+
|  Key Empirical Studies:                                                         |
|  1. Brier (1950, Monthly Weather Review):                                       |
|     - Established mathematically proper scoring rule for probability forecasts. |
|  2. Murphy (1973, Journal of Applied Meteorology):                              |
|     - Proved Brier score partitions into Reliability, Resolution, Uncertainty.  |
|  3. Bailey, Borwein, Lopez de Prado, and Zhu (2016, Mathematical Finance):       |
|     - Established CSCV and PBO framework to quantify backtest overfitting.      |
|  4. Aronson (2006, Evidence-Based Technical Analysis):                          |
|     - Demonstrated that applying bootstrap data-snooping corrections erases     |
|       virtually all reported technical trading alpha.                           |
+---------------------------------------------------------------------------------+
```

---

## Worked examples

### Example 1: Computing Murphy's Brier Score Decomposition

A discretionary chartist logs ten sequential breakout forecasts, predicting the probability that price will hit its profit target before stop loss:
- Group 1 (High Confidence): Five trades with forecasted probability $f = 0.80$.
  - Outcomes: $1, 1, 1, 0, 1$ (4 wins, 1 loss $\implies \bar{o}_1 = 4/5 = 0.80$).
- Group 2 (Low Confidence): Five trades with forecasted probability $f = 0.30$.
  - Outcomes: $0, 0, 1, 0, 0$ (1 win, 4 losses $\implies \bar{o}_2 = 1/5 = 0.20$).
- Total Sample: $N = 10$, total wins $= 5$, unconditional base rate $\bar{o} = 5/10 = 0.50$.

1. **Calculate Uncertainty**:
   $$\text{Uncertainty} = \bar{o}(1 - \bar{o}) = 0.50 \times (1 - 0.50) = 0.2500$$

2. **Calculate Reliability (Calibration Error)**:
   - Bin 1 ($n_1 = 5$): $f_1 = 0.80, \bar{o}_1 = 0.80 \implies (0.80 - 0.80)^2 = 0.00$.
   - Bin 2 ($n_2 = 5$): $f_2 = 0.30, \bar{o}_2 = 0.20 \implies (0.30 - 0.20)^2 = (0.10)^2 = 0.01$.
   $$\text{Reliability} = \frac{5}{10}(0.00) + \frac{5}{10}(0.01) = 0.5(0.01) = 0.0050$$
   The trader exhibits outstanding calibration ($\text{Reliability} = 0.005$).

3. **Calculate Resolution (Discriminative Skill)**:
   - Bin 1: $(\bar{o}_1 - \bar{o})^2 = (0.80 - 0.50)^2 = (0.30)^2 = 0.09$.
   - Bin 2: $(\bar{o}_2 - \bar{o})^2 = (0.20 - 0.50)^2 = (-0.30)^2 = 0.09$.
   $$\text{Resolution} = \frac{5}{10}(0.09) + \frac{5}{10}(0.09) = 0.0900$$

4. **Compute Total Brier Score**:
   $$\text{Brier} = \text{Reliability} - \text{Resolution} + \text{Uncertainty} = 0.0050 - 0.0900 + 0.2500 = 0.1650$$
   The trader's Brier score of $0.1650$ significantly outperforms the naive baseline of $0.2500$, driven by high discriminative resolution ($0.0900$).

### Example 2: Calculating Expected Calibration Error (ECE)

A quantitative analyst evaluates $1,000$ machine learning breakout forecasts across three probability buckets:
- Bucket 1: $f_1 \in [0.0, 0.4]$, Average Forecast $\bar{f}_1 = 0.25$, Count $n_1 = 400$, Observed Frequency $\bar{o}_1 = 0.20$.
- Bucket 2: $f_2 \in [0.4, 0.7]$, Average Forecast $\bar{f}_2 = 0.55$, Count $n_2 = 400$, Observed Frequency $\bar{o}_2 = 0.45$.
- Bucket 3: $f_3 \in [0.7, 1.0]$, Average Forecast $\bar{f}_3 = 0.85$, Count $n_3 = 200$, Observed Frequency $\bar{o}_3 = 0.65$.

1. **Calculate Weighted Absolute Calibration Errors**:
   - Bucket 1: $\frac{400}{1000} \times |0.25 - 0.20| = 0.40 \times 0.05 = 0.020$.
   - Bucket 2: $\frac{400}{1000} \times |0.55 - 0.45| = 0.40 \times 0.10 = 0.040$.
   - Bucket 3: $\frac{200}{1000} \times |0.85 - 0.65| = 0.20 \times 0.20 = 0.040$.

2. **Compute Expected Calibration Error**:
   $$\text{ECE} = 0.020 + 0.040 + 0.040 = 0.100 = 10.0\%$$
   On average, the model's confidence exceeds actual realized frequencies by $10\%$, revealing systemic overconfidence that requires Platt scaling or isotonic regression calibration.

---

## Pitfalls

- **Evaluating Strategies by Win Rate Instead of Expectancy**:
  A technical system with an $85\%$ win rate can easily be unprofitable if the average loss is $10$ times larger than the average win.
  Expectancy in R ($E = \text{Win Rate} \times R_{\text{win}} - \text{Loss Rate} \times R_{\text{loss}}$) is the mandatory evaluation metric.
- **Tweaking Rules After Seeing Out-of-Sample Results**:
  If a researcher modifies an indicator after observing failure on the OOS test set, that OOS set becomes part of the training set.
  Continued adjustments create secondary overfitting that destroys live out-of-sample performance.
- **Ignoring Survivorship and Corporate Actions in Price Series**:
  Testing technical rules on raw stock prices that do not adjust for stock splits, reverse splits, or cash dividends creates phantom moving average crossovers and false gap breakouts.
  Data must be fully split- and dividend-adjusted.
- **Neglecting Execution Delay in Backtest Engines**:
  Assuming a buy order executes at the exact close of the signal bar assumes zero latency.
  Realistic backtests must execute at the next bar's open ($P_{t+1}^{\text{open}}$) with modeled bid-ask spread friction.

---

## Interview questions

> [!question] mkt-ta-225 | What is Karl Popper's criterion of falsifiability and how does it apply to technical trading?
> A theory is scientific only if it makes assertions that can be empirically disproven by observable tests.
> Subjective chart analysis is unscientific if patterns can be arbitrarily adjusted after the fact to excuse failed trades.

> [!question] mkt-ta-226 | What is a mathematically proper scoring rule?
> A loss function for evaluating probability forecasts where the expected penalty is strictly minimized if and only if the forecaster reports their true internal subjective probability.
> Examples include the Brier score and logarithmic score.

> [!question] mkt-ta-227 | State the formula for the Brier score.
> Brier = (1 / N) * sum_{i=1}^N (f_i - o_i)^2, where f_i in [0, 1] is the forecasted probability and o_i in {0, 1} is the binary realization.
> It penalizes deviations between predicted probabilities and actual binary outcomes.

> [!question] mkt-ta-228 | State Murphy's (1973) Brier score decomposition.
> Brier = Reliability - Resolution + Uncertainty.
> Reliability measures calibration error, Resolution measures discriminative sorting power, and Uncertainty measures the inherent entropy of the event base rate.

> [!question] mkt-ta-229 | What is Reliability in Murphy's Brier decomposition?
> The weighted sum of squared differences between average forecasted probabilities and observed frequencies across calibration bins.
> A perfectly calibrated forecaster has a Reliability score of zero.

> [!question] mkt-ta-230 | What is Resolution in Murphy's Brier decomposition?
> The weighted sum of squared differences between conditional bin frequencies and the unconditional base rate.
> Higher resolution indicates a superior ability to identify distinctly high-probability or low-probability opportunities.

> [!question] mkt-ta-231 | What is the logarithmic score (cross-entropy) in probabilistic evaluation?
> Log Loss = -sum [ o_i * ln(f_i) + (1 - o_i) * ln(1 - f_i) ] / N.
> It imposes an infinite penalty on extreme overconfidence that turns out to be wrong (e.g. predicting 100% on an event that fails).

> [!question] mkt-ta-232 | What is a probability calibration curve?
> A scatter plot dividing forecasts into probability deciles (x-axis) and plotting them against the actual observed frequency of success (y-axis).
> An ideal forecaster follows the 45-degree diagonal line: events predicted with 70% probability occur exactly 70% of the time.

> [!question] mkt-ta-233 | What is Expected Calibration Error (ECE)?
> The weighted average of the absolute differences between forecasted probabilities and observed frequencies across all bins: ECE = sum (n_k / N) * |f_k - o_k|.
> It quantifies the expected percentage miscalibration in a model's confidence scores.

> [!question] mkt-ta-234 | What is Platt scaling in probability calibration?
> Fitting a logistic regression model on raw model outputs: P(y=1|s) = 1 / (1 + exp(A * s + B)).
> It transforms uncalibrated raw scores into well-calibrated probabilities.

> [!question] mkt-ta-235 | What is walk-forward validation?
> An out-of-sample backtesting procedure where an algorithm optimizes parameters on historical window [t - M, t], tests on future window [t, t + K], and rolls forward sequentially.
> It simulates real-time deployment without look-ahead bias.

> [!question] mkt-ta-236 | What is the Degradation Ratio in quantitative backtesting?
> The ratio of out-of-sample Sharpe ratio to in-sample Sharpe ratio: Degradation = Sharpe_OOS / Sharpe_IS.
> A ratio below 0.50 signals significant strategy overfitting.

> [!question] mkt-ta-237 | What is Combinatorially Symmetric Cross-Validation (CSCV)?
> A cross-validation technique developed by Bailey et al. (2016) that splits a dataset into N blocks and evaluates all combinations of training and testing subsets.
> It preserves historical time structure while creating a distribution of out-of-sample rankings.

> [!question] mkt-ta-238 | What is the Probability of Backtest Overfitting (PBO)?
> The probability that the trading strategy selected as best in-sample ranks below the median performance out-of-sample across CSCV combinations.
> PBO > 0.50 indicates that optimization is purely fitting historical noise.

> [!question] mkt-ta-239 | What is the Deflated Sharpe Ratio (DSR)?
> An analytical adjustment developed by Bailey and Lopez de Prado (2014) that discounts an observed Sharpe ratio based on the number of trials tested, sample length, skewness, and kurtosis.
> It calculates the probability that an observed Sharpe exceeds the expected maximum of random trials.

> [!question] mkt-ta-240 | What is the minimum backtest length required to achieve statistical confidence in a Sharpe ratio of 1.0?
> For a strategy with annualized Sharpe = 1.0 on daily data with normal returns, approximately 2 to 3 years of data are required to achieve t > 2.0.
> If returns exhibit negative skewness, the required sample length doubles or triples.

> [!question] mkt-ta-241 | What is trade expectancy in R-multiples?
> Expectancy = (Win Rate * Average Win in R) - (Loss Rate * Average Loss in R).
> It quantifies the average expected dollar return per dollar risked on every execution.

> [!question] mkt-ta-242 | Why is the Profit Factor a useful non-parametric performance metric?
> Profit Factor = Gross Profits / Gross Losses.
> Unlike Sharpe ratio, it does not require assumptions of normally distributed returns and directly measures capital efficiency.

> [!question] mkt-ta-243 | What is Maximum Favorable Excursion (MFE)?
> The maximum unrealized profit reached by a trade between entry and exit.
> Comparing MFE to actual realized gain reveals whether a trader is leaving substantial profit on the table or setting unrealistic profit targets.

> [!question] mkt-ta-244 | What is Maximum Adverse Excursion (MAE)?
> The maximum unrealized loss experienced by a trade between entry and exit.
> Analyzing MAE across winning trades allows quantitative desks to optimize stop-loss placement just beyond normal trade noise.

> [!question] mkt-ta-245 | What is execution slippage and how must it be modeled in backtests?
> The difference between the signal price and actual fill price caused by market impact and latency.
> Realistic backtests must deduct at least half the bid-ask spread plus volatility-scaled impact from every simulated fill.

> [!question] mkt-ta-246 | What is the look-ahead bias trap in daily bar data?
> Triggering an entry at day t using closing price P_t, but recording execution at P_t itself without allowing for after-hours market movement.
> Orders can execute only at the next day's open or during the official closing cross.

> [!question] mkt-ta-247 | What is the Bonferroni correction for multiple testing?
> A conservative adjustment that divides the desired significance level alpha by the total number of tested hypotheses: alpha_adjusted = alpha / M.
> It ensures that the overall family-wise error rate across M tests remains below alpha.

> [!question] mkt-ta-248 | Why is the Bonferroni correction often overly conservative in financial backtesting?
> Because financial trading rules are highly correlated (e.g. 14-day RSI and 15-day RSI have correlation > 0.98), violating the independence assumption.
> Frameworks like White's Reality Check or FDR provide more accurate correlation-adjusted thresholds.

> [!question] mkt-ta-249 | What is survivorship bias in technical stock scanning?
> Backtesting technical rules on the current constituents of an index (e.g. current S&P 500) over past decades, ignoring all companies that were delisted.
> It artificially inflates returns by eliminating every catastrophic corporate failure from the test universe.

> [!question] mkt-ta-250 | What is point-in-time data?
> Historical data that reflects exactly what information was publicly known at each historical timestamp, without subsequent revisions or post-event adjustments.
> Backtesting requires point-in-time financial and corporate action records to prevent look-ahead bias.

> [!question] mkt-ta-251 | What is an anchor point in backtesting and why does changing it test robustness?
> The calendar start date of a simulation.
> If shifting the start date by one month causes a profitable strategy to turn into a losing one, the model is fragile and overfitted.

> [!question] mkt-ta-252 | What is Monte Carlo trade sequence resampling?
> Randomly shuffling the sequential order of realized trade returns thousands of times to generate a distribution of simulated equity curves.
> It reveals the true range of potential drawdowns that could occur under different sequencing of wins and losses.

> [!question] mkt-ta-253 | What is a trading rule parameter plateau?
> A wide, continuous range of adjacent parameter values that all produce stable, profitable performance.
> True structural market edges manifest as parameter plateaus, whereas overfitted noise manifests as sharp, isolated parameter spikes.

> [!question] mkt-ta-254 | How does the Brier Skill Score (BSS) evaluate a forecaster against a benchmark?
> BSS = 1 - (Brier_forecaster / Brier_reference).
> A BSS > 0 indicates predictive skill superior to a naive baseline; BSS = 1 represents perfect forecasting.

> [!question] mkt-ta-255 | What is overconfidence bias in probability forecasting?
> The empirical tendency of humans to assign extreme probabilities (e.g. 90% or 95%) to uncertain future events that actually occur far less frequently.
> Calibration feedback trains traders to compress confidence toward realistic base rates.

> [!question] mkt-ta-256 | Why must a quantitative trader never deploy a strategy to live capital without passing the Capital Gate?
> A backtest is a hypothesis, not a guarantee.
> The Capital Gate enforces pre-registered rules, minimum live paper sample validation, fixed stop limits, and strict risk budgeting before real capital is placed at risk.

---

## Further reading

- Brier, G. W. (1950). *Verification of forecasts expressed in terms of probability*. Monthly Weather Review, 78(1), 1-3.
- Murphy, A. H. (1973). *A new vector partition of the probability score*. Journal of Applied Meteorology, 12(4), 595-600.
- Aronson, D. R. (2006). *Evidence-Based Technical Analysis: Applying the Scientific Method and Statistical Inference to Trading Signals*. John Wiley & Sons.
- Bailey, D. H., & Lopez de Prado, M. (2014). *The deflated Sharpe ratio: Correcting for selection bias, backtest overfitting, and non-normality*. The Journal of Portfolio Management, 40(5), 94-107.
- Bailey, D. H., Borwein, J., Lopez de Prado, M., & Zhu, Q. J. (2016). *The probability of backtest overfitting*. Mathematical Finance, 27(4), 987-1014.
- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. John Wiley & Sons.
