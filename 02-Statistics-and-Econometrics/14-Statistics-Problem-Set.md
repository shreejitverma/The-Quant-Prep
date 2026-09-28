---
type: problem-set
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [linear-regression-ols, hypothesis-testing-and-multiple-comparisons]
est_hours: 6
sources: [Joshi Denson and Downes - Quant Job Interview Questions and Answers, Zhou - A Practical Guide to Quantitative Finance Interviews, Wasserman - All of Statistics (2004), Greene - Econometric Analysis, Tsay - Analysis of Financial Time Series (3rd ed.), Lo (2002) - The Statistics of Sharpe Ratios - Financial Analysts Journal 58(4), Harvey Liu and Zhu (2016) - and the Cross-Section of Expected Returns - Review of Financial Studies 29(1), Ioannidis (2005) - Why Most Published Research Findings Are False - PLoS Medicine 2(8)]
---

# Statistics Problem Set

## TL;DR

- State the estimator, its standard error and the assumption behind that standard error before quoting any number; most interview traps are a wrong standard error, not a wrong point estimate.
- Means are hard to estimate and volatilities are easy: the standard error of a mean falls with calendar time, the standard error of a volatility falls with the number of observations.
- A $t$-stat of 2 means little after a search: count the trials, correct for them, and ask what fraction of ideas were real to begin with.
- In regressions, know the four ways a slope lies: omitted variables, errors in variables, nonstationary levels and overlapping observations.
- Speak the sanity check: sign, order of magnitude, and a limiting case, before and after computing.

## Learning objectives

- Answer rapid-fire regression and inference questions from researcher interviews.
- Diagnose flawed statistical claims in a research write-up.

## Core concepts

This note is a drill set; theory lives in the topic notes: [Estimation](01-Estimation-MLE-and-Method-of-Moments.md), [Confidence Intervals](02-Confidence-Intervals-and-Sampling.md), [Hypothesis Testing](03-Hypothesis-Testing-and-Multiple-Comparisons.md), [OLS](04-Linear-Regression-OLS.md), [Regression Diagnostics](05-Regression-Diagnostics-and-Robust-Inference.md), [Time Series](08-Time-Series-Stationarity-and-ARMA.md), [Volatility Models](09-Volatility-Models-GARCH.md) and [Bootstrap](12-Bootstrap-and-Resampling.md).

Numbers worth knowing cold:

| Quantity | Value |
| :--- | :--- |
| $z$ for 90%, 95%, 99% two-sided | 1.645, 1.960, 2.576 |
| $z$ for 80% power | 0.842 |
| SE of a proportion at $p = 0.5$ | $0.5/\sqrt n$ |
| SE of annualised Sharpe from daily data over $Y$ years | about $1/\sqrt Y$ |
| SE of a sample volatility | about $\sigma/\sqrt{2n}$ |
| SE of a correlation near zero | about $1/\sqrt n$ |
| Efficiency of the median vs the mean (normal data) | $2/\pi = 0.64$ |
| 95% upper bound with zero events in $n$ trials | about $3/n$ |
| Dickey-Fuller 5% critical value, with constant | $-2.86$ |
| Probability a point is in a bootstrap sample | 0.632 |

Checklist for a research write-up:

1. How many things were tried, and is that in the inference?
2. Are the observations independent, or do labels overlap and returns cluster?
3. Is the data point-in-time and survivorship-free?
4. Are variables stationary, or are levels being regressed on levels?
5. Is the effect economically large after costs, not just statistically non-zero?
6. Does it hold out of sample, in subperiods and across assets?

## Worked examples

### 1. How long to prove a Sharpe ratio

A manager claims an annualised Sharpe of 0.5.
How many years of returns are needed to detect it with 80% power at 5% significance?

With $Y$ years of roughly iid returns the $t$-stat of the mean is $SR\sqrt Y$.
Power $1-\beta$ at level $\alpha$ requires $SR\sqrt Y = z_{1-\alpha} + z_{1-\beta}$.
One-sided: $Y = ((1.645 + 0.842)/0.5)^2 = 24.7$ years.
Two-sided: $Y = ((1.960 + 0.842)/0.5)^2 = 31.4$ years.
Sanity check: the requirement scales as $1/SR^2$, so a Sharpe of 2 needs only 1.5 to 2 years, which is why high-frequency strategies can be validated and slow macro strategies cannot.

### 2. Means versus volatilities

A stock has annual expected return 8% and volatility 16%.

- Mean: the standard error of the annual mean after $Y$ years is $16\%/\sqrt Y$, independent of sampling frequency; getting it to 2% needs $Y = (16/2)^2 = 64$ years.
- Volatility: with $n$ daily returns, $\text{se}(\hat\sigma) \approx \sigma/\sqrt{2n}$; one year of daily data gives $16\%/\sqrt{504} = 0.71\%$.

Sampling more often does not help the mean because the total drift over a fixed calendar span is fixed; it helps the variance because each observation carries independent information about $\sigma^2$.
This is why risk models are estimated and alpha is argued.

### 3. What fraction of significant backtests are real

Suppose 10% of the ideas a team tests are real, tests have 50% power, and the threshold is $\alpha = 5\%$.
Out of 1000 ideas: 100 real, of which 50 pass; 900 null, of which 45 pass.
$P(\text{real} \mid \text{significant}) = 50/95 = 0.526$.
Nearly half the "discoveries" are false even with no $p$-hacking; with 5% real ideas and 30% power it drops to $15/(15+47.5) = 0.24$.
This is the argument of Ioannidis (2005) and the reason Harvey, Liu and Zhu (2016) ask for $t > 3$ in factor research.

### 4. Two ways a slope lies

True model: $y = 1.0\,x_1 + 0.5\,x_2 + \varepsilon$, and the regression of $x_2$ on $x_1$ has slope 0.6.

- Omitted variable: regressing $y$ on $x_1$ alone gives $\beta_1 + \beta_2\delta = 1.0 + 0.5\times0.6 = 1.3$, a 30% overstatement, because $x_1$ proxies for the missing $x_2$.
- Errors in variables: if $x_1$ is observed with noise of variance half its own variance, the slope is attenuated by $\text{Var}(x^*)/(\text{Var}(x^*)+\text{Var}(u)) = 1/1.5 = 0.67$ toward zero.

A noisy signal (analyst estimates, sentiment scores) therefore understates its true predictive power, while a signal correlated with a known factor overstates its alpha until the factor is controlled for.

### 5. Annualising a Sharpe with autocorrelation

Monthly returns have Sharpe 0.3 and AR(1) autocorrelation $\rho = 0.2$ (typical of smoothed hedge fund marks).
Naive: $0.3\sqrt{12} = 1.04$.
Lo (2002): $SR_{12} = SR_1 \cdot 12\big/\sqrt{12 + 2\sum_{k=1}^{11}(12-k)\rho^k} = 0.3\times2.88 = 0.86$.
Positive autocorrelation makes annual returns more volatile than $\sqrt{12}$ times monthly, so the naive figure overstates the Sharpe by 20%.

### 6. Reviewing a write-up

"We tested 200 technical signals on the S&P 500 constituents from 2005 to 2024.
The best signal predicts 20-day forward returns with a $t$-stat of 3.1 (daily OLS regression, $R^2 = 0.9\%$).
A regression of the index level on the signal's cumulative PnL has $R^2 = 0.95$, confirming the relationship."

Issues, in the order an interviewer expects:

- Selection: $t = 3.1$ gives two-sided $p = 0.0019$; with 200 tests Bonferroni gives $200\times0.0019 = 0.39$ and the per-test threshold is $t \approx 3.66$.
- Overlap: daily samples of 20-day returns overlap, so OLS standard errors are too small by about $\sqrt{20} = 4.5$; the honest $t$ is near 0.7.
- Survivorship: today's constituents over 2005 to 2024 exclude firms that left the index, biasing any long signal upward.
- Spurious regression: two trending levels give a high $R^2$ regardless of any relationship.
- Missing: costs, turnover, out-of-sample period, subperiod stability.

## Pitfalls

- Quoting $s/\sqrt n$ for data that are autocorrelated, overlapping or clustered.
- Believing that higher-frequency data shortens the time needed to estimate a mean.
- Reading a $p$-value as the probability the null is true.
- Reading a 95% confidence interval as a 95% probability statement about the fixed parameter.
- Using $R^2$ to compare models with different dependent variables (levels versus returns).
- Forgetting that an insignificant result is weak evidence of no effect when power is low.
- Correcting for multiple testing only across the strategies reported, not those tried.

## Interview questions

### Estimation

> [!question]- stat-ps-variance-divisor-bias | What is the expectation of $\frac1n\sum(x_i-\bar x)^2$ for iid data with variance $\sigma^2$?
> $\frac{n-1}{n}\sigma^2$.
> One degree of freedom is used by $\bar x$; dividing by $n-1$ gives an unbiased estimator, though dividing by $n+1$ minimises MSE for normal data.

> [!question]- stat-ps-mle-uniform-max | $X_1,\dots,X_n$ iid Uniform$(0,\theta)$. What is the MLE of $\theta$ and is it unbiased?
> $\hat\theta = \max_i X_i$, biased low: $E[\max] = \frac{n}{n+1}\theta$.
> The likelihood $\theta^{-n}$ is decreasing in $\theta$ on $\theta \ge \max X_i$; $\frac{n+1}{n}\max X_i$ is unbiased.

> [!question]- stat-ps-mle-exponential-rate | MLE of the rate $\lambda$ of an exponential distribution, and its bias?
> $\hat\lambda = 1/\bar x$, biased upward: $E[1/\bar x] = \frac{n}{n-1}\lambda$.
> Jensen: $1/x$ is convex; $\frac{n-1}{n\bar x}$ is unbiased.

> [!question]- stat-ps-median-efficiency | For normal data, how efficient is the sample median relative to the mean?
> About 64%: $\text{Var}(\text{median}) \approx \frac{\pi}{2}\frac{\sigma^2}{n}$, efficiency $2/\pi$.
> For fat-tailed data (Laplace, Student-$t$ with low degrees of freedom) the median can beat the mean.

> [!question]- stat-ps-mean-estimation-years | Expected return 8%, volatility 16%. How many years to estimate the mean to a standard error of 2%?
> 64 years.
> SE of the annual mean is $16\%/\sqrt Y$ regardless of sampling frequency; $(16/2)^2 = 64$.

> [!question]- stat-ps-vol-estimation-se | Standard error of a volatility estimated from one year of daily returns with true vol 16%?
> About 0.7%.
> $\text{se}(\hat\sigma) \approx \sigma/\sqrt{2n} = 16\%/\sqrt{504} = 0.71\%$ for normal returns; fat tails make it larger.

### Confidence intervals

> [!question]- stat-ps-ci-meaning | What does a 95% confidence interval mean?
> The procedure covers the true parameter in 95% of repeated samples.
> A given computed interval either contains the fixed parameter or not; the probability statement is about the procedure, and a Bayesian credible interval is the object with the other reading.

> [!question]- stat-ps-poll-sample-size | How many observations for a 95% margin of error of 3 points on a proportion near 0.5?
> About 1,068.
> $n = (1.96\times0.5/0.03)^2 = 1067.1$, round up.

> [!question]- stat-ps-ci-halve-width | How much more data to halve a confidence interval's width?
> Four times as much.
> Width scales as $1/\sqrt n$ for iid data.

> [!question]- stat-ps-sharpe-ci-4y | Annualised Sharpe 1.5 from four years of daily returns. Approximate 95% CI?
> About $[0.5, 2.5]$.
> SE $\approx 1/\sqrt{4} = 0.5$ (Lo's formula gives 0.501), so $1.5 \pm 1.96\times0.5$.

> [!question]- stat-ps-rule-of-three | A risk model had zero VaR breaches in 100 days. Upper 95% bound on the breach probability?
> About 3%.
> Solve $(1-p)^{100} = 0.05$: $p \approx -\ln 0.05/100 = 3.0/100$, the rule of three.

> [!question]- stat-ps-variance-ci | 30 observations give sample variance $s^2$. What is the 95% CI for $\sigma^2$ under normality?
> $[0.63\,s^2,\ 1.81\,s^2]$.
> $(n-1)s^2/\sigma^2 \sim \chi^2_{29}$, whose 2.5% and 97.5% quantiles are 16.05 and 45.72; the interval is asymmetric.

### Hypothesis testing

> [!question]- stat-ps-pvalue-meaning | Define a $p$-value, and say what it is not.
> The probability, under the null, of a test statistic at least as extreme as the one observed.
> It is not the probability that the null is true, nor the probability the result is a fluke.

> [!question]- stat-ps-coin-60-heads | 60 heads in 100 tosses. Is the coin biased at 5%?
> Borderline: $z = (60-50)/5 = 2.0$, two-sided $p = 0.046$, just significant.
> The exact binomial two-sided $p$ is about 0.057, so the answer depends on the approximation, and that is the point to make.

> [!question]- stat-ps-power-sharpe-years | Years of data to detect a true Sharpe of 0.5 with 80% power at one-sided 5%?
> About 25 years.
> $Y = ((1.645+0.842)/0.5)^2 = 24.7$; two-sided it is 31.4 years.

> [!question]- stat-ps-false-positives-100 | You test 100 useless strategies at 5%. Expected number of false positives and chance of at least one?
> 5 expected; $P(\ge1) = 1 - 0.95^{100} = 0.994$ if independent.
> Correlated strategies give fewer effective tests but the same expected count.

> [!question]- stat-ps-bonferroni-threshold | You test 200 signals and want 5% family-wise error. What per-test $p$ and $t$ thresholds?
> $p < 0.00025$, i.e. $|t| > 3.66$.
> Bonferroni divides $\alpha$ by the number of tests; Holm is uniformly more powerful with the same guarantee.

> [!question]- stat-ps-bayes-discovery-rate | 10% of tested ideas are real, power is 50%, $\alpha = 5\%$. What fraction of significant results are real?
> About 53%.
> $0.1\times0.5/(0.1\times0.5 + 0.9\times0.05) = 0.05/0.095 = 0.526$.

> [!question]- stat-ps-insignificant-not-null | A test of a signal gives $p = 0.3$. Does that show the signal is useless?
> No: absence of evidence is not evidence of absence when power is low.
> Report the confidence interval; if it includes economically large effects the data are simply uninformative.

### Regression

> [!question]- stat-ps-slope-from-correlation | Correlation 0.5, $\sigma_y = 2\%$, $\sigma_x = 1\%$. Slope of $y$ on $x$ and $R^2$?
> Slope 1.0, $R^2 = 0.25$.
> $\beta = \rho\sigma_y/\sigma_x$ and in simple regression $R^2 = \rho^2$.

> [!question]- stat-ps-reverse-regression | Regress $y$ on $x$: slope 0.5. Regress $x$ on $y$: slope 1.2. What is the correlation?
> $\rho^2 = 0.5\times1.2 = 0.6$, so $|\rho| = 0.77$ with positive sign.
> $\beta_{y|x}\beta_{x|y} = \rho^2$; the two slopes are not reciprocals unless $|\rho| = 1$.

> [!question]- stat-ps-omitted-variable | True $y = 1.0x_1 + 0.5x_2$; $x_2$ on $x_1$ has slope 0.6. What does regressing $y$ on $x_1$ alone give?
> 1.3.
> Omitted-variable bias: $\beta_1 + \beta_2\delta = 1 + 0.5\times0.6$.

> [!question]- stat-ps-errors-in-variables | The regressor is measured with noise whose variance is half the true regressor's variance. What happens to the slope?
> It is attenuated toward zero by the factor $1/(1+0.5) = 0.67$.
> $\text{plim}\,\hat\beta = \beta\,\text{Var}(x^*)/(\text{Var}(x^*)+\text{Var}(u))$; noise in $y$ only inflates standard errors.

> [!question]- stat-ps-duplicate-rows | You accidentally duplicate every row of a regression. What happens to $\hat\beta$ and its $t$-stats?
> $\hat\beta$ is unchanged; standard errors shrink by about $\sqrt2$ and $t$-stats rise by about $\sqrt2$.
> OLS thinks it has twice the independent information, the same failure as overlapping labels.

> [!question]- stat-ps-r2-to-tstat | Simple regression with $n = 252$ and $R^2 = 1\%$. Is the slope significant?
> No: $t = \sqrt{(n-2)R^2/(1-R^2)} = 1.59$.
> Equivalently a correlation of 0.1 needs about $n = 400$ observations to reach $t = 2$.

> [!question]- stat-ps-heteroskedasticity | Residual variance rises with the regressor. Is OLS still unbiased, and what breaks?
> Still unbiased and consistent; the usual standard errors are wrong.
> Use White (HC) or, with autocorrelation too, Newey-West standard errors, or reweight by WLS for efficiency.

> [!question]- stat-ps-multicollinearity-vif | Two regressors have correlation 0.9. By what factor are the slope variances inflated?
> About 5.3.
> $\text{VIF} = 1/(1-R_j^2) = 1/(1-0.81)$; coefficients become unstable though predictions may be fine.

> [!question]- stat-ps-hedge-ratio | What is the minimum-variance hedge ratio of asset $y$ with instrument $x$?
> $h^* = \text{Cov}(y,x)/\text{Var}(x)$, the OLS slope of $y$ on $x$.
> The hedged variance is $\sigma_y^2(1-\rho^2)$.

### Time series

> [!question]- stat-ps-ar1-weekly-half-life | A weekly spread has AR(1) coefficient 0.9. Half-life?
> About 6.6 weeks.
> $\ln 0.5/\ln 0.9 = 6.58$.

> [!question]- stat-ps-spurious-levels | Two independent random walks regressed on each other give $t = 8$. Why?
> Spurious regression: with I(1) series the OLS $t$-stat diverges with $n$ even when there is no relationship.
> Regress differences, or test the residual for a unit root (cointegration).

> [!question]- stat-ps-sharpe-autocorrelation | Monthly Sharpe 0.3 with AR(1) autocorrelation 0.2. Annualised Sharpe?
> About 0.86, not $0.3\sqrt{12} = 1.04$.
> Lo's factor is $12/\sqrt{12 + 2\sum_{k=1}^{11}(12-k)0.2^k} = 2.88$.

> [!question]- stat-ps-df-vs-t-critical | Your ADF $t$-stat is $-2.5$. Do you reject a unit root at 5%?
> No: the 5% Dickey-Fuller critical value with a constant is $-2.86$.
> The Student-$t$ value $-1.65$ is wrong because the regressor is nonstationary under the null.

### Volatility

> [!question]- stat-ps-garch-long-run-vol | GARCH(1,1) with $\omega = 10^{-6}$, $\alpha = 0.1$, $\beta = 0.85$ on daily data. Long-run annual vol and shock half-life?
> About 7.1% annualised and 13.5 days.
> $\bar\sigma^2 = 10^{-6}/0.05 = 2\times10^{-5}$ (0.447% daily); half-life $\ln 0.5/\ln 0.95$.

> [!question]- stat-ps-ewma-update | EWMA with $\lambda = 0.94$: yesterday's vol 2%, yesterday's return 5%. Today's vol?
> About 2.29%.
> $\sqrt{0.94\times0.0004 + 0.06\times0.0025} = \sqrt{0.000526}$.

> [!question]- stat-ps-sqrt-time-scaling | When is scaling 1-day VaR by $\sqrt{10}$ to get 10-day VaR wrong?
> When returns are autocorrelated, volatility is expected to change over the horizon, or tails are not preserved under aggregation.
> $\sqrt{h}$ scaling assumes iid returns with a fixed distribution shape; GARCH mean reversion and fat tails both break it.

### Bootstrap and resampling

> [!question]- stat-ps-bootstrap-inclusion | Probability that a specific observation appears in a bootstrap sample of size $n = 1000$?
> About 0.632.
> $1 - (1-1/1000)^{1000} \approx 1 - e^{-1}$.

> [!question]- stat-ps-bootstrap-autocorrelated | Why is an iid bootstrap of daily strategy returns misleading, and what do you use instead?
> It destroys autocorrelation and volatility clustering, so it understates the uncertainty of the mean and Sharpe.
> Use a block, circular or stationary bootstrap with block length growing like $n^{1/3}$.

> [!question]- stat-ps-permutation-zero-p | 1999 random permutations and none exceed the observed statistic. $p$-value?
> $1/2000 = 0.0005$.
> Include the observed labelling: $(1 + 0)/(1999 + 1)$.

### Diagnosing flawed claims

> [!question]- stat-ps-flaw-best-of-200 | "The best of 200 signals has $t = 3.1$." Is it significant?
> Not after correcting for the search: two-sided $p = 0.0019$, Bonferroni-adjusted $0.39$.
> The per-test threshold for 5% family-wise error across 200 tests is $|t| > 3.66$.

> [!question]- stat-ps-flaw-overlapping-daily | "Daily regression of 20-day forward returns on a signal, $t = 3.1$." What is wrong?
> Overlapping labels: adjacent observations share 19 of 20 returns, so OLS standard errors are too small by about $\sqrt{20}$.
> Re-estimate with Hansen-Hodrick or Newey-West errors or non-overlapping samples; the $t$ falls to about 0.7.

> [!question]- stat-ps-flaw-survivorship | "We backtested on the current S&P 500 members since 2005." What bias does this introduce?
> Survivorship and look-ahead bias: firms that failed or were dropped are excluded, and firms are included because of later success.
> Use point-in-time constituents including delisted returns.

> [!question]- stat-ps-flaw-r2-comparison | Model A explains price levels with $R^2 = 0.95$; model B explains returns with $R^2 = 0.02$. Which is better?
> The comparison is meaningless: $R^2$ depends on the variance of the dependent variable.
> A level regression gets high $R^2$ from persistence alone; compare forecasts of the same target out of sample.

## Further reading

- Joshi, Denson and Downes, *Quant Job Interview Questions and Answers*.
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*.
- Larry Wasserman, *All of Statistics*.
- William Greene, *Econometric Analysis*, for omitted variables, errors in variables and robust standard errors.
- Andrew Lo (2002), The Statistics of Sharpe Ratios, Financial Analysts Journal.
- Harvey, Liu and Zhu (2016), ... and the Cross-Section of Expected Returns, Review of Financial Studies.
- John Ioannidis (2005), Why Most Published Research Findings Are False, PLoS Medicine.
