---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [confidence-intervals-and-sampling]
est_hours: 3
sources: [Wasserman - All of Statistics (2004) ch 8, Hastie Tibshirani and Friedman - The Elements of Statistical Learning (2nd ed.) sec 7.11 and 8.2, Efron (1979) - Bootstrap Methods - Another Look at the Jackknife - Annals of Statistics 7(1), Efron and Tibshirani - An Introduction to the Bootstrap (1993), Kunsch (1989) - The Jackknife and the Bootstrap for General Stationary Observations - Annals of Statistics 17(3), Politis and Romano (1994) - The Stationary Bootstrap - JASA 89(428), Politis and White (2004) - Automatic Block-Length Selection for the Dependent Bootstrap - Econometric Reviews 23(1), Athreya (1987) - Bootstrap of the Mean in the Infinite Variance Case - Annals of Statistics 15(2), White (2000) - A Reality Check for Data Snooping - Econometrica 68(5), Ledoit and Wolf (2008) - Robust Performance Hypothesis Testing with the Sharpe Ratio - Journal of Empirical Finance 15(5)]
---

# Bootstrap and Resampling Methods

## TL;DR

- The bootstrap estimates the sampling distribution of a statistic by recomputing it on samples drawn with replacement from the data, i.e. from the empirical distribution $\hat F_n$ (plug-in principle).
- A bootstrap sample contains each original point with probability $1-(1-1/n)^n \to 1 - e^{-1} \approx 0.632$.
- Use percentile intervals for quick work, BCa or bootstrap-$t$ (studentized) intervals when the statistic is skewed or biased; the studentized version has better coverage accuracy.
- It fails for extremes (the sample maximum), infinite-variance data, parameters on a boundary, and, above all, dependent data resampled as if iid.
- For time series use block bootstraps: moving or circular blocks, or the stationary bootstrap with geometric block lengths of mean $1/p$; block length grows like $n^{1/3}$.
- Permutation tests give exact $p$-values under exchangeability; for strategies, permute or circularly shift the signal relative to returns, and report $p = (1 + \#\{T_b \ge T_{\text{obs}}\})/(B+1)$.

## Learning objectives

- Apply the bootstrap and know when it fails.
- Use block and stationary bootstraps for dependent data.
- Run permutation tests for strategy significance.

## Core concepts

### The plug-in principle

We want the distribution of $\hat\theta = T(X_1,\dots,X_n)$ under the unknown $F$.
The bootstrap replaces $F$ by $\hat F_n$, which puts mass $1/n$ on each observation, and approximates the distribution of $\hat\theta - \theta$ by that of $\hat\theta^* - \hat\theta$ over resamples $X_1^*,\dots,X_n^* \sim \hat F_n$.
In practice draw $B$ resamples (1,000 for standard errors, 5,000 to 10,000 for tail quantiles) and compute $\hat\theta^*_1,\dots,\hat\theta^*_B$.

- Bootstrap standard error: the standard deviation of the $\hat\theta^*_b$.
- Bootstrap bias estimate: $\bar\theta^* - \hat\theta$.
- For the sample mean the ideal ($B \to \infty$) bootstrap SE is $\hat\sigma_{\text{plug-in}}/\sqrt n$ with the $1/n$ variance, slightly smaller than the usual $s/\sqrt n$.

Two sources of error: Monte Carlo error from finite $B$ (reducible) and the gap between $\hat F_n$ and $F$ (not reducible by more resamples).
The number of distinct resamples is $\binom{2n-1}{n}$, which is 126 for $n = 5$ and 92,378 for $n = 10$.

### Confidence intervals

| Interval | Construction | Notes |
| :--- | :--- | :--- |
| Normal | $\hat\theta \pm z_{1-\alpha/2}\,\widehat{se}_{\text{boot}}$ | Fine when the distribution is near normal |
| Percentile | $[\hat\theta^*_{(\alpha/2)}, \hat\theta^*_{(1-\alpha/2)}]$ | Transformation-invariant, first-order accurate |
| Basic (pivotal) | $[2\hat\theta - \hat\theta^*_{(1-\alpha/2)},\ 2\hat\theta - \hat\theta^*_{(\alpha/2)}]$ | Reflects the percentile interval about $\hat\theta$ |
| Bootstrap-$t$ | Quantiles of $(\hat\theta^* - \hat\theta)/\widehat{se}^*$ | Second-order accurate; needs an SE inside each resample |
| BCa | Percentile with bias and skewness (acceleration) corrections | Second-order accurate, transformation-invariant |

Studentized statistics are asymptotically pivotal, which is why bootstrap-$t$ and BCa have coverage error $O(1/n)$ against $O(1/\sqrt n)$ for percentile and normal intervals.
For a Sharpe ratio, Ledoit and Wolf (2008) recommend a studentized circular block bootstrap.

### When the iid bootstrap fails

- Extremes: the bootstrap distribution of $\max X_i^*$ puts mass $1-(1-1/n)^n \approx 0.632$ on the sample maximum itself, while the true distribution of the maximum is continuous.
- Infinite variance: for the mean of a distribution with tail index $\alpha < 2$ the bootstrap distribution does not converge to the right limit (Athreya 1987); use subsampling ($m$ out of $n$).
- Parameters on a boundary, such as a variance component at zero or a constrained weight at a bound.
- Non-smooth statistics such as sample quantiles in very small samples.
- Dependent data: resampling individual observations destroys autocorrelation and volatility clustering, so the SE of a mean is understated by $\sqrt{\sum_k \rho_k}$-type factors; for AR(1) the variance ratio is $(1+\phi)/(1-\phi)$.
- Selection: bootstrapping the winner of a search does not account for the search unless the search is repeated inside every resample.

### Bootstraps for dependent data

- Moving block bootstrap (Kunsch 1989): cut the series into overlapping blocks of length $\ell$, draw $n/\ell$ blocks with replacement and concatenate.
- Circular block bootstrap: wrap the series so every point has equal chance of appearing.
- Stationary bootstrap (Politis and Romano 1994): at each step start a new block at a random point with probability $p$, otherwise continue the current block; block lengths are Geometric with mean $1/p$ and the resampled series is stationary.

Block length trades bias (too short breaks dependence) against variance (too long leaves few distinct blocks).
The MSE-optimal length for variance estimation grows like $n^{1/3}$; Politis and White (2004) give a data-driven rule.
White's (2000) Reality Check and Hansen's SPA test use the stationary bootstrap to test whether the best of many strategies beats a benchmark after accounting for the search.

### Permutation tests

If under $H_0$ the joint distribution is invariant to relabelling, the permutation distribution of a statistic is its exact null distribution.
Two-sample test: pool the observations, reassign labels in all $\binom{n_1+n_2}{n_1}$ ways (or $B$ random ways), and compute the fraction of relabellings whose statistic is at least as extreme as observed.
With random permutations use $p = (1 + \#\{T_b \ge T_{\text{obs}}\})/(B+1)$ so the test is exact and $p$ is never zero.

Strategy framing:

- Null "the signal has no information about future returns": shuffle the signal against returns and recompute the strategy Sharpe.
- Shuffling breaks the autocorrelation of the signal and therefore its turnover; circularly shifting the signal by a random lag preserves both series' dependence and only breaks their alignment.
- Sign-flip (randomisation) tests for a mean of zero assume symmetric returns under the null.

Permutation tests answer "is there any relationship"; bootstrap intervals answer "how large is it and how uncertain".

## Worked examples

### 1. The 0.632 rule

Probability a given observation appears in a bootstrap sample: $1 - (1 - 1/n)^n$.
For $n = 5$: 0.672; $n = 10$: 0.651; $n = 252$: 0.6329; the limit is $1 - e^{-1} = 0.6321$.
Consequences: each resample has about 63% distinct points, the out-of-bag 37% gives a free validation set in bagging and random forests, and the bootstrap maximum equals the sample maximum with probability 0.63.

### 2. Bootstrap SE of a mean by hand

Five daily PnLs: $2, -1, 4, 0, 5$.
Mean 2.0, $s = 2.550$, textbook SE $s/\sqrt5 = 1.140$.
The ideal bootstrap SE uses the plug-in variance: $\hat\sigma = 2.280$, SE $= 2.280/\sqrt5 = 1.020$, smaller by the factor $\sqrt{(n-1)/n} = 0.894$.
With $n = 5$ there are only 126 distinct resamples; the bootstrap cannot manufacture information that five points do not contain.

### 3. A Sharpe ratio confidence interval

Three years of daily returns ($T = 756$) with annualised Sharpe exactly 1.0 and roughly normal returns.

- Analytic (Lo): se of annualised Sharpe $= \sqrt{252}\sqrt{(1 + SR_d^2/2)/(T-1)} = 0.578$, 95% CI $[-0.13, 2.13]$.
- IID bootstrap with $B = 5000$ on a simulated series: se 0.59, percentile CI $[-0.14, 2.17]$, and 4.4% of resampled Sharpes are at or below zero.
- Both agree that three years of Sharpe 1 is only borderline significant: $t = 1.0\times\sqrt3 = 1.73$, one-sided $p \approx 0.04$.

With autocorrelated or fat-tailed returns the analytic formula needs corrections, while a studentized block bootstrap handles both.

### 4. IID versus stationary bootstrap on autocorrelated returns

```python
import numpy as np

def stationary_bootstrap_idx(n, mean_block, rng):
    """Politis-Romano: blocks start at random points, lengths ~ Geometric(1/mean_block), wrap around."""
    idx = np.empty(n, dtype=int)
    idx[0] = rng.integers(n)
    new_block = rng.random(n) < 1.0 / mean_block
    starts = rng.integers(n, size=n)
    for t in range(1, n):
        idx[t] = starts[t] if new_block[t] else (idx[t - 1] + 1) % n
    return idx

def boot_se(x, stat, B=2000, mean_block=None, seed=0):
    rng = np.random.default_rng(seed)
    n = len(x)
    draws = [stat(x[rng.integers(n, size=n)] if mean_block is None
                  else x[stationary_bootstrap_idx(n, mean_block, rng)]) for _ in range(B)]
    return np.std(draws, ddof=1)

rng = np.random.default_rng(42)
n, phi = 1000, 0.3
e = rng.standard_normal(n + 100)
x = np.zeros(n + 100)
for t in range(1, n + 100):
    x[t] = phi * x[t - 1] + e[t]
x = x[100:]
print(x.std() / np.sqrt(n),                      # naive iid formula: 0.034
      boot_se(x, np.mean),                       # iid bootstrap: 0.034
      boot_se(x, np.mean, mean_block=10))        # stationary bootstrap: 0.042
```

The true SE of the mean of an AR(1) with $\phi = 0.3$ and unit innovations is approximately $\frac{1}{\sqrt{1-\phi^2}}\sqrt{\frac{1+\phi}{1-\phi}}\big/\sqrt n = 0.045$.
The iid bootstrap reproduces the naive formula (0.034) and so understates the SE by the factor $\sqrt{1.857} = 1.36$.
The stationary bootstrap with mean block $10 \approx n^{1/3}$ recovers most of the gap (0.042); block methods are slightly biased down because they cut dependence at block joins.

### 5. An exact permutation test for a signal

On four "signal on" days the strategy earned $0.9, 0.4, 1.2, 0.7$ bp; on four "signal off" days $0.1, -0.3, 0.5, 0.2$.
Observed difference in means $= 0.80 - 0.125 = 0.675$.
There are $\binom84 = 70$ ways to label four of the eight days "on".
Only two labellings give a difference of at least 0.675: the observed one, and the one that swaps 0.4 for 0.5.
One-sided $p = 2/70 = 0.029$.
The test assumes the eight days are exchangeable under the null, which fails if, say, "on" days cluster in a high-volatility regime.

### 6. Where the bootstrap of a maximum breaks

Take $n = 252$ daily returns and bootstrap the largest one.
With probability $0.633$ the resample contains the sample maximum, so 63% of the bootstrap distribution sits on a single value and none lies above it.
The true sampling distribution of the maximum is continuous and extends above the observed maximum; tail quantities (VaR at extreme levels, the best-case return) need extreme value theory ([Heavy Tails and Extreme Value Theory](13-Heavy-Tails-and-Extreme-Value-Theory.md)) or $m$-out-of-$n$ subsampling.

## Pitfalls

- Resampling individual days of an autocorrelated or volatility-clustered series and reporting the resulting tight interval.
- Bootstrapping the best strategy from a search without repeating the search in each resample; this ignores selection bias ([Overfitting and Deflated Sharpe](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md)).
- Using too few resamples for tail quantiles: a 99% percentile from $B = 200$ rests on two points.
- Believing the bootstrap fixes a tiny sample; it inherits every quirk of $\hat F_n$.
- Reporting a permutation $p$-value of exactly 0 from random permutations instead of $1/(B+1)$.
- Permuting returns in a test whose statistic depends on their time order (turnover, drawdown), which changes more than the null requires.
- Bootstrapping panel data by rows when the dependence is across assets on the same date; resample dates (or blocks of dates) instead.
- Choosing the block length after looking at which one gives the most significant result.

## Interview questions

> [!question]- stat-boot-plugin-principle | What is the bootstrap, in one sentence?
> Estimating the sampling distribution of a statistic by recomputing it on samples drawn with replacement from the data.
> It replaces the unknown $F$ by the empirical distribution $\hat F_n$ and uses $\hat\theta^* - \hat\theta$ as a proxy for $\hat\theta - \theta$.

> [!question]- stat-boot-632 | What fraction of the original observations appears in a typical bootstrap sample?
> About 63.2%.
> Each point is missed with probability $(1-1/n)^n \to e^{-1} = 0.368$.

> [!question]- stat-boot-fails-max | Why does the bootstrap fail for the sample maximum?
> The resampled maximum equals the sample maximum with probability about 0.632 and can never exceed it.
> The bootstrap distribution has a large atom and no upper tail, unlike the true continuous distribution of the maximum.

> [!question]- stat-boot-failure-cases | Name four settings where the naive iid bootstrap is invalid.
> Dependent data, extremes such as the maximum, infinite-variance data, and parameters on a boundary.
> Also post-selection inference when the selection step is not repeated inside each resample.

> [!question]- stat-boot-iid-on-ar1 | You iid-bootstrap the mean of AR(1) returns with $\phi = 0.3$. By what factor is the SE wrong?
> Understated by about $\sqrt{(1+\phi)/(1-\phi)} = \sqrt{1.857} = 1.36$.
> The iid bootstrap reproduces $\hat\sigma/\sqrt n$, while positive autocorrelation inflates the long-run variance of the mean.

> [!question]- stat-boot-stationary-bootstrap | Describe the stationary bootstrap.
> Build the resample by continuing the current block with probability $1-p$ or jumping to a random start with probability $p$, wrapping at the end.
> Block lengths are Geometric with mean $1/p$, the resampled series is stationary, and $1/p$ should grow like $n^{1/3}$.

> [!question]- stat-boot-block-length | What goes wrong if the block length is too short or too long?
> Too short breaks the dependence and understates variance; too long leaves few distinct blocks and makes the estimate noisy.
> The MSE-optimal length for variance estimation grows like $n^{1/3}$, and Politis-White give a data-driven choice.

> [!question]- stat-boot-percentile-vs-t | Why is a bootstrap-$t$ interval usually more accurate than a percentile interval?
> It bootstraps an asymptotically pivotal studentized statistic, giving coverage error $O(1/n)$ instead of $O(1/\sqrt n)$.
> The cost is an inner standard error for every resample; BCa gets the same order with bias and acceleration corrections.

> [!question]- stat-boot-permutation-pvalue | You run 999 random permutations and none beat the observed statistic. What $p$-value do you report?
> $1/1000 = 0.001$.
> Use $(1 + \#\{T_b \ge T_{\text{obs}}\})/(B+1)$, which counts the observed labelling and keeps the test exact.

> [!question]- stat-boot-permutation-exact | Signal-on days returned 0.9, 0.4, 1.2, 0.7; signal-off days 0.1, -0.3, 0.5, 0.2. Exact one-sided permutation $p$ for the difference in means?
> $2/70 \approx 0.029$.
> Of the $\binom84 = 70$ labellings only the observed one and the swap of 0.4 with 0.5 give a difference of at least 0.675.

> [!question]- stat-boot-strategy-permutation | How would you permutation-test whether a trading signal has predictive power while respecting autocorrelation?
> Circularly shift the signal by random lags relative to returns and recompute the strategy Sharpe each time.
> This keeps each series' own dependence (and the strategy's turnover) and destroys only their alignment, which is exactly the null.

> [!question]- stat-boot-sharpe-3y | Three years of daily data give annualised Sharpe 1.0. Roughly what is the 95% bootstrap interval?
> About $[-0.1, 2.1]$.
> The SE of an annualised Sharpe is about $\sqrt{1/\text{years}} = 0.58$, and a bootstrap of normal-like returns agrees.

> [!question]- stat-boot-bootstrap-vs-permutation | When do you use a permutation test rather than a bootstrap?
> Permutation to test a sharp null of no relationship under exchangeability; bootstrap to estimate the size and uncertainty of an effect.
> Permutation $p$-values are exact under exchangeability; bootstrap tests need resampling under an imposed null.

## Further reading

- Larry Wasserman, *All of Statistics*, chapter 8.
- Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning*, sections 7.11 and 8.2.
- Efron and Tibshirani, *An Introduction to the Bootstrap*.
- Politis and Romano (1994), The Stationary Bootstrap, JASA.
- Kunsch (1989), The Jackknife and the Bootstrap for General Stationary Observations, Annals of Statistics.
- White (2000), A Reality Check for Data Snooping, Econometrica.
- Ledoit and Wolf (2008), Robust Performance Hypothesis Testing with the Sharpe Ratio, Journal of Empirical Finance.
