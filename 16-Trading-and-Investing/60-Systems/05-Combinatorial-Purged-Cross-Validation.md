---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Bailey Borwein Lopez de Prado and Zhu (2017) - The Probability of Backtest Overfitting - Journal of Computational Finance 20(4), Lopez de Prado (2018) - Advances in Financial Machine Learning ch 7 11 12, Pardo (2008) - The Evaluation and Optimization of Trading Strategies]
---

# Combinatorial Purged Cross-Validation

## TL;DR

- Traditional walk-forward backtesting evaluates only a single historical path, creating severe path dependency and recency bias.
- Standard k-fold cross-validation fails catastrophically on financial time series due to serial correlation and overlapping label information leakage.
- Purging eliminates training observations whose forward outcome labels overlap in time with the testing evaluation period.
- Embargoing drops training observations immediately after the testing set to eliminate residual autoregressive memory and post-event spillover.
- Combinatorial Purged Cross-Validation (CPCV) generates $\binom{N-1}{k-1}$ complete historical out-of-sample backtest paths from $\binom{N}{k}$ splits, yielding an empirical distribution of Sharpe ratios.
- Combinatorially Symmetric Cross-Validation (CSCV) computes the Probability of Backtest Overfitting (PBO), quantifying the probability that the best in-sample strategy performs below median out of sample.

## Learning objectives

- Identify the structural failure modes of standard k-fold cross-validation on non-iid financial time series.
- Implement data purging to prevent forward information leakage from overlapping labels.
- Implement data embargoing to eliminate autoregressive serial correlation.
- Formulate Combinatorial Purged Cross-Validation (CPCV) and calculate the number of generated out-of-sample backtest paths.
- Execute Combinatorially Symmetric Cross-Validation (CSCV) and compute the Probability of Backtest Overfitting (PBO).

## Core concepts

### 1. Why Standard K-Fold Cross-Validation Fails in Finance

Standard k-fold cross-validation assumes that observations $(X_t, y_t)$ are independent and identically distributed (iid).
In financial time series, this assumption is completely violated:

1. **Serial Autocorrelation**: Asset prices, volatility regimes, and order book states exhibit strong memory ($\text{Corr}(X_t, X_{t+1}) \gg 0$).
2. **Overlapping Outcome Labels**: When features predict returns over forward horizons (e.g. 5-day holding periods $y_t = \frac{P_{t+5} - P_t}{P_t}$), the label at timestamp $t$ spans across $t+1, t+2, t+3, t+4, t+5$.
If standard k-fold randomly shuffles days into train and test folds, the training set contains information about future prices that were already active during the test set.

This leakage produces massive artificially inflated cross-validation scores that collapse in live trading.

```
Standard Cross-Validation Leakage:
Time ----------------------------------------------------------------->
Folds: [ Train ][ Test ][ Train ][ Test ][ Train ][ Test ]
Overlaps:        <--->           <--->           <--->   (Information Leakage!)
```

### 2. Purging and Embargoing

To restore rigorous cross-validation integrity without destroying time-series structure, Marcos Lopez de Prado (2018) introduced **Purging** and **Embargoing**:

```
+-----------------------------------------------------------------------+
|                    PURGED AND EMBARGOED TRAIN/TEST SPLIT              |
+-----------------------------------------------------------------------+
| ... TRAIN SET ... | PURGED |    TEST SET    | EMBARGO | ... TRAIN SET ... |
+-------------------+--------+----------------+---------+-------------------+
                      <---->                    <----->
                    Overlapping               Autoregressive
                    Holding Labels            Memory Window
+-----------------------------------------------------------------------+
```

1. **Purging**:
   - For every test observation spanning evaluation interval $[t_{0, \text{test}}, t_{1, \text{test}}]$, identify any training observation whose label was determined using prices from within that window.
   - Any training observation with an overlapping label is completely removed from the training fold.
2. **Embargoing**:
   - Because financial market features exhibit autoregressive persistence ($\text{AR}(p)$ memory), training samples immediately following the test set are still contaminated by test-period market shocks.
   - The embargo drops an additional buffer window (e.g. 1% to 5% of sample length, or $h$ trading days) from the training set immediately following the end of the test set.

### 3. Combinatorial Purged Cross-Validation (CPCV)

Walk-forward testing generates only a single historical path and a single point-estimate Sharpe ratio.
A single path cannot differentiate whether a strategy's success was due to genuine structural edge or because the single historical path happened to favor its parameters (path luck).

Combinatorial Purged Cross-Validation (CPCV) solves this limitation:
1. Divide $T$ historical observations into $N$ contiguous, chronological groups.
2. Select all possible combinations of $k$ groups as the test set:
   $$\text{Number of splits} = \binom{N}{k}$$
   The remaining $N - k$ groups form the training set, subject to purging and embargoing.
3. Each individual group appears in exactly $\binom{N-1}{k-1}$ test sets.
4. Testing predictions can be recombined into exactly:
   $$\varphi[N, k] = \frac{k}{N} \binom{N}{k} = \binom{N-1}{k-1}$$
   complete, distinct historical out-of-sample backtest paths.

Rather than a single Sharpe ratio, CPCV generates a full probability distribution of $\binom{N-1}{k-1}$ out-of-sample Sharpe ratios.
The dispersion of this distribution reveals strategy path sensitivity and robustness across diverse historical sequences.

### 4. Combinatorially Symmetric Cross-Validation (CSCV) and PBO

David Bailey, Jonathan Borwein, Marcos Lopez de Prado, and Qiji Jim Zhu (2017) formulated **Combinatorially Symmetric Cross-Validation (CSCV)** to calculate the **Probability of Backtest Overfitting (PBO)**.

CSCV measures whether in-sample optimization ranking carries any predictive power for out-of-sample performance:

1. **Matrix of Configurations**: Form the $T \times M$ matrix $\mathbf{R}$ containing the return series of all $M$ strategy parameter configurations tested.
2. **Contiguous Splitting**: Split the $T$ timeline into an even number of contiguous blocks $S$ (e.g. $S = 6, 8, 10$).
3. **Combinatorial Partitions**: Generate all $C = \binom{S}{S/2}$ combinations of $S/2$ blocks to serve as the in-sample (IS) training set $J$.
The complement $\bar{J}$ of $S/2$ blocks serves as the out-of-sample (OOS) testing set.
4. **Ranking Evaluation**:
   - For each partition $c \in \{1, \dots, C\}$:
     - Find the in-sample winner: $m^* = \arg\max_{m=1,\dots,M} SR_m(J)$.
     - Compute the out-of-sample Sharpe ratio for all $M$ configurations on $\bar{J}$: $\{SR_m(\bar{J})\}_{m=1}^M$.
     - Calculate the relative percentile rank $\bar{\omega}_c \in (0, 1)$ of the in-sample winner $m^*$ among all $M$ configurations out of sample:
       $$\bar{\omega}_c = \frac{\text{Rank}(SR_{m^*}(\bar{J}))}{M + 1}$$
     - Compute the logit:
       $$\lambda_c = \ln\left( \frac{\bar{\omega}_c}{1 - \bar{\omega}_c} \right)$$
5. **Probability of Backtest Overfitting (PBO)**:
   $$\text{PBO} = \frac{1}{C} \sum_{c=1}^C \mathbf{1}(\lambda_c \le 0) = \frac{1}{C} \sum_{c=1}^C \mathbf{1}(\bar{\omega}_c \le 0.50)$$

**Interpreting PBO**:
- $\text{PBO} \approx 0.0$: In-sample ranking translates strongly to out-of-sample performance (high generalization).
- $\text{PBO} \approx 0.50$: The in-sample winner performs like a random coin flip out of sample (selection is pure noise).
- $\text{PBO} > 0.50$: The in-sample winner systematically underperforms the median out of sample (severe overfitted mean-reversion).

---

## Worked examples

### Example 1: Calculating CPCV Paths for $N=6, k=2$

A quantitative team sets up CPCV with $N = 6$ temporal groups and $k = 2$ test groups:
1. **Total Number of Train/Test Splits**:
   $$\binom{N}{k} = \binom{6}{2} = \frac{6 \times 5}{2 \times 1} = 15 \text{ splits}$$
2. **Number of Complete Historical Backtest Paths**:
   $$\varphi[6, 2] = \binom{N-1}{k-1} = \binom{5}{1} = 5 \text{ paths}$$

Each of the 6 groups appears in exactly 5 testing combinations.
By stitching together non-overlapping test predictions, the team constructs 5 complete, distinct out-of-sample equity curves across the entire historical timeline.
If the resulting Sharpe ratios across the 5 paths are $\{1.42, 1.35, 1.38, 1.40, 1.36\}$, the strategy shows minimal path dispersion.
If the Sharpes are $\{2.10, 0.40, -0.30, 1.80, 0.10\}$, the strategy is severely path-dependent and fragile.

### Example 2: Computing PBO from CSCV Partitions

A researcher tests $M = 50$ parameter combinations using CSCV with $S = 6$ blocks:
- Total combinations: $\binom{6}{3} = 20$ partitions.

For each partition $c \in \{1, \dots, 20\}$, the in-sample winner $m^*$ is identified, and its relative rank $\bar{\omega}_c$ out of sample is computed:

| Partition | OOS Rank of IS Winner $\bar{\omega}_c$ | $\lambda_c \le 0$ ($\bar{\omega}_c \le 0.50$) |
|:---:|:---:|:---:|
| 1 | $0.24$ | Yes |
| 2 | $0.42$ | Yes |
| 3 | $0.55$ | No |
| 4 | $0.31$ | Yes |
| 5 | $0.18$ | Yes |
| 6 | $0.62$ | No |
| 7 | $0.48$ | Yes |
| 8 | $0.35$ | Yes |
| 9 | $0.70$ | No |
| 10 | $0.29$ | Yes |
| 11 - 20 (10 splits) | 6 splits $\le 0.50$, 4 splits $> 0.50$ | 6 Yes, 4 No |

Total partitions where the IS winner ranked at or below the OOS median:
$$\text{Count} = 1 + 1 + 0 + 1 + 1 + 0 + 1 + 1 + 0 + 1 + 6 = 13 \text{ partitions}$$

Calculating PBO:
$$\text{PBO} = \frac{13}{20} = 65.0\%$$

**Verdict**: $\text{PBO} = 65.0\% > 50.0\%$.
The selection procedure is severely overfitted.
The in-sample winner actually performs worse than a random choice out of sample $65\%$ of the time.

---

## Pitfalls

- **Shuffling Time Series in Cross-Validation**: Using random k-fold cross-validation on time-series data, leaking future returns into past training sets.
- **Neglecting Label Horizon in Purging**: Purging only the single entry timestamp rather than the full holding horizon $[t, t + \Delta t]$ over which the forward return label was measured.
- **Overlooking Post-Test Autoregressive Memory**: Failing to apply an embargo buffer after test periods, allowing serial correlation from test shocks to bleed into subsequent training folds.
- **Treating Walk-Forward as the Gold Standard**: Relying exclusively on a single walk-forward path, blind to the fact that alternate historical sequences would have devastated the strategy.
- **Ignoring Low PBO with Negative Returns**: Achieving a low PBO ($\text{PBO} \approx 0.10$) merely because the winner consistently performed in the top decile, while the entire universe produced negative returns out of sample.

---

## Interview questions

> [!question]- mkt-sys-129 | Why does standard k-fold cross-validation fail when applied to financial time series?
> Because financial observations violate iid assumptions; serial autocorrelation and overlapping forward return labels leak future information from test sets into training folds.

> [!question]- mkt-sys-130 | What is purging in financial cross-validation (Lopez de Prado 2018)?
> Purging removes training observations whose forward outcome labels overlap in time with the testing evaluation period, preventing lookahead information leakage.

> [!question]- mkt-sys-131 | What is embargoing in financial cross-validation?
> Embargoing removes a buffer of training observations immediately following the test period to eliminate residual autoregressive memory and post-event spillover.

> [!question]- mkt-sys-132 | What is Combinatorial Purged Cross-Validation (CPCV)?
> CPCV splits data into N groups and tests on all subsets of k groups with purging and embargoing, generating a combinatorial distribution of out-of-sample backtest paths.

> [!question]- mkt-sys-133 | How many total splits are generated in CPCV with N groups and k test groups?
> The number of splits equals the binomial coefficient N choose k: C = N! / (k! * (N - k)!).

> [!question]- mkt-sys-134 | How many complete out-of-sample backtest paths does CPCV generate?
> CPCV generates phi[N, k] = (k / N) * binom(N, k) = binom(N - 1, k - 1) complete, distinct historical backtest paths.

> [!question]- mkt-sys-135 | What is the primary advantage of CPCV over traditional walk-forward backtesting?
> Walk-forward produces only a single historical path and point-estimate Sharpe; CPCV generates a full distribution of paths, revealing path dependency and robustness.

> [!question]- mkt-sys-136 | Define Combinatorially Symmetric Cross-Validation (CSCV).
> CSCV divides data into S blocks and evaluates all (S choose S/2) splits to measure how in-sample strategy rankings generalize to out-of-sample testing sets.

> [!question]- mkt-sys-137 | Define the Probability of Backtest Overfitting (PBO) mathematically.
> PBO is the fraction of CSCV partitions in which the in-sample winning strategy achieves an out-of-sample rank at or below the median: PBO = (1/C) * sum 1(omega_bar <= 0.50).

> [!question]- mkt-sys-138 | What does a PBO value of approximately 0.50 signify?
> A PBO of 0.50 signifies that in-sample optimization has zero predictive power; the selected strategy performs like an arbitrary random draw out of sample.

> [!question]- mkt-sys-139 | What does a PBO value greater than 0.50 signify?
> A PBO > 0.50 indicates structural overfitting where in-sample optimization actively selects strategies that underperform the out-of-sample median due to noise chasing.

> [!question]- mkt-sys-140 | What is the logit transformation in CSCV?
> lambda = ln(omega_bar / (1 - omega_bar)), where omega_bar is the relative out-of-sample rank; lambda <= 0 corresponds strictly to omega_bar <= 0.50.

> [!question]- mkt-sys-141 | Why must the number of blocks S in CSCV be an even integer?
> S must be even so the dataset can be split into equal halves of S/2 blocks for training and S/2 blocks for testing, maintaining symmetric cross-validation.

> [!question]- mkt-sys-142 | How does label horizon length determine the required purge window?
> The purge window must equal or exceed the maximum forward holding period Delta t of the prediction labels to guarantee zero temporal overlap.

> [!question]- mkt-sys-143 | What is performance degradation in CSCV?
> The slope of the linear regression of out-of-sample performance on in-sample performance; a negative or near-zero slope indicates severe overfitting.

> [!question]- mkt-sys-144 | What is the probability of loss in CSCV?
> The fraction of CSCV partitions in which the best in-sample strategy produces a negative out-of-sample return or Sharpe ratio: Pr(OOS_winner < 0).

> [!question]- mkt-sys-145 | How does walk-forward backtesting introduce recency bias?
> Walk-forward tests progressively across history, meaning the final model parameters are conditioned heavily on recent market regimes that may not persist.

> [!question]- mkt-sys-146 | Why does cross-validation without shuffling maintain chronological blocks?
> Contiguous chronological blocks preserve intra-block market dynamics, volatility clustering, and microstructure regime persistence within each fold.

> [!question]- mkt-sys-147 | What is the difference between expanding-window and rolling-window walk-forward?
> Expanding window retains all past data from inception, whereas rolling window uses a fixed-length historical lookback and discards older observations.

> [!question]- mkt-sys-148 | How does CPCV prevent testing on future data when training on past data?
> CPCV tests on all combinations of blocks, meaning some training sets occur after test sets; this is statistically valid because purging and embargoing eliminate leakage.

> [!question]- mkt-sys-149 | Why is training on future data to test on past data valid in cross-validation?
> Because if market regimes are stationary and leakage is eliminated via purging, testing model generalizability across historical blocks does not require chronological ordering.

> [!question]- mkt-sys-150 | What is an anchored walk-forward test?
> An anchored walk-forward test fixes the starting date of the training window at inception while extending the training end-point forward at each rebalance step.

> [!question]- mkt-sys-151 | How does increasing the number of CSCV blocks S affect PBO precision?
> Increasing S increases the combinatorial partition count C = binom(S, S/2), providing a denser empirical distribution of relative out-of-sample ranks.

> [!question]- mkt-sys-152 | What is the relationship between PBO and Deflated Sharpe Ratio (DSR)?
> Both quantify overfitting: DSR penalizes the headline Sharpe ratio for trial count and non-normality, while PBO measures the empirical ranking failure rate across cross-validation splits.

> [!question]- mkt-sys-153 | Can a strategy have a low PBO but still fail in live trading?
> Yes; if the entire strategy universe suffers from unmodeled execution costs, regime shifts, or data errors, the winner will beat peers OOS while still losing money.

> [!question]- mkt-sys-154 | What is the optimal value of k in CPCV with N groups?
> Typically k = 2 or k = N / 2, balancing the number of distinct out-of-sample paths generated with adequate training sample size.

> [!question]- mkt-sys-155 | How does serial correlation in returns affect embargo window sizing?
> Stronger return or volatility autocorrelation requires a wider embargo buffer (e.g. several times the autocorrelation decay half-life) to prevent leakage.

> [!question]- mkt-sys-156 | What is the difference between in-sample overfitting and cross-validation overfitting?
> In-sample overfitting fits a model to training data; cross-validation overfitting repeatedly evaluates models on the same validation fold until the validation score is overfitted.

> [!question]- mkt-sys-157 | Why does cross-validation in machine learning finance require event-based sampling?
> Event-based sampling (e.g. volatility spikes, structural breaks) aligns observations with informational events rather than arbitrary clock-time intervals.

> [!question]- mkt-sys-158 | What is the primary computational bottleneck of CPCV?
> Fitting model training algorithms binom(N, k) times; for complex neural networks or large parameter grids, combinatorial re-training requires distributed compute clusters.

> [!question]- mkt-sys-159 | How does CPCV path dispersion inform position sizing?
> A strategy with wide dispersion across CPCV paths indicates high path uncertainty, requiring conservative fractional Kelly or lower volatility target sizing.

> [!question]- mkt-sys-160 | What is the minimum acceptable PBO for institutional strategy approval?
> Institutional allocators typically require PBO <= 0.20 to 0.25 (less than 25% probability of out-of-sample sub-median performance) before committing capital.

---

## Further reading

- Bailey, D. H., Borwein, J. M., Lopez de Prado, M., & Zhu, Q. J. (2017). The probability of backtest overfitting. *Journal of Computational Finance*, 20(4), 39-69.
- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. John Wiley & Sons.
- Pardo, R. (2008). *The Evaluation and Optimization of Trading Strategies*. John Wiley & Sons.
