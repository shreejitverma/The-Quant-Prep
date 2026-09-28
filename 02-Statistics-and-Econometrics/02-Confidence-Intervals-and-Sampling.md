---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [inequalities-and-limit-theorems]
est_hours: 3
sources: [Wasserman - All of Statistics ch 6 10, Casella and Berger - Statistical Inference 2nd ed ch 5 9, Lo (2002) - The Statistics of Sharpe Ratios - Financial Analysts Journal, Mertens (2002) - Comments on Variance of the IID Estimator in Lo (2002), Bailey and Lopez de Prado (2012) - The Sharpe Ratio Efficient Frontier - Journal of Risk]
---

# Confidence Intervals and Sampling Distributions

## TL;DR

- A 95% confidence interval is a procedure that covers the true parameter in 95% of repeated samples; any one realised interval either contains it or does not.
- Mean: $\bar x \pm t_{n-1,0.975}\,s/\sqrt n$; widths shrink like $1/\sqrt n$, so halving the width costs four times the data.
- $t$ appears when a normal is divided by an estimated standard deviation, $\chi^2$ for sample variances, $F$ for ratios of variances.
- Sharpe ratio: $\text{SE}(\widehat{SR}) \approx \sqrt{(1+SR^2/2)/n}$ per period (Lo 2002), so an annualised Sharpe has SE about $1/\sqrt{T_{\text{years}}}$.
- Detecting an annual Sharpe of $S$ at $t = 2$ needs about $4/S^2$ years; with 80% power at 5% two-sided, about $7.85/S^2$ years.

## Learning objectives

- Build confidence intervals for means, proportions and Sharpe ratios.
- Know the t, chi-squared and F distributions and when each appears.
- Estimate how many observations are needed to detect an edge of a given size.

## Core concepts

### Sampling distributions and pivots

A statistic's sampling distribution is its distribution over hypothetical repeated samples.
A pivot is a function of data and parameter whose distribution is free of the parameter, for example $(\bar X-\mu)/(\sigma/\sqrt n)\sim N(0,1)$.
Inverting $P(a\le \text{pivot}\le b) = 1-\alpha$ for the parameter gives a $1-\alpha$ confidence interval.
Without a pivot, the CLT supplies an approximate one: $\hat\theta\pm z_{1-\alpha/2}\,\widehat{\text{SE}}$ (the Wald interval).

### The three sampling distributions

For $X_i$ iid $N(\mu,\sigma^2)$, $\bar X$ and $S^2$ are independent, and:

- $\chi^2_k$ is a sum of $k$ squared independent standard normals; $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$.
- $t_k = Z/\sqrt{\chi^2_k/k}$ with independent numerator and denominator; $(\bar X-\mu)/(S/\sqrt n)\sim t_{n-1}$.
- $F_{k,m} = (\chi^2_k/k)/(\chi^2_m/m)$; the ratio of two independent sample variances, and the regression F-test.

$t_k$ has heavier tails than the normal (variance $k/(k-2)$), but $t_{59,0.975} = 2.001$ versus $1.96$ already: for $n$ above 30 or so the choice barely matters compared with non-normality and autocorrelation.
The $\chi^2$ interval for a variance is exact for normal data but very sensitive to fat tails, unlike the $t$ interval for a mean.

### Proportions

For a hit rate $\hat p$ over $n$ independent trades, $\text{SE} = \sqrt{\hat p(1-\hat p)/n}$.
The Wald interval behaves badly near 0 or 1; the Wilson interval (inverting the score test) is the better default.
Rule of three: zero events in $n$ trials gives an approximate 95% upper bound of $3/n$, because $(1-p)^n = 0.05$ at $p\approx -\ln(0.05)/n\approx3/n$.

### Sharpe ratio inference

The per-period Sharpe ratio $\widehat{SR} = \bar r/s$ is a ratio estimator; for iid normal returns the delta method gives

$$
\text{Var}(\widehat{SR}) \approx \frac{1 + SR^2/2}{n}.
$$

The 1 comes from estimating the mean, the $SR^2/2$ from estimating the volatility.
For non-normal iid returns with skewness $\gamma_3$ and kurtosis $\gamma_4$ (normal is 3), Mertens (2002) gives $\big(1-\gamma_3 SR + \frac{\gamma_4-1}{4}SR^2\big)/n$; negative skew and fat tails widen the interval.
Annualising daily estimates multiplies both $SR$ and its SE by $\sqrt{252}$, so $\text{SE}(\widehat{SR}_{\text{ann}}) \approx 1/\sqrt{T}$ with $T$ in years.
Scaling by $\sqrt{q}$ assumes serially uncorrelated returns; with autocorrelation $\rho_k$ Lo's correction is $SR_q = SR\cdot q/\sqrt{q+2\sum_{k=1}^{q-1}(q-k)\rho_k}$.

### Sample size for an edge

A test of zero mean has $t = \widehat{SR}\sqrt{n}$ in per-period units, or $\widehat{SR}_{\text{ann}}\sqrt{T}$ in annual units.
To reach $t$-stat $z$ you need $T = (z/SR_{\text{ann}})^2$ years.
Bailey and Lopez de Prado (2012) call the non-normal version of this the minimum track record length.
To have power $1-\beta$ at two-sided level $\alpha$, you need

$$
n = \left(\frac{z_{1-\alpha/2}+z_{1-\beta}}{\text{effect}/\sigma}\right)^2,
$$

with $z_{0.975}+z_{0.8} = 1.96 + 0.8416 = 2.80$.
The effect size divided by noise is what counts; data frequency only matters through $\sigma$ per observation.
Autocorrelated data carry less information: for AR(1) with coefficient $\rho$ the variance of the mean inflates by $(1+\rho)/(1-\rho)$, so the effective sample size is $n(1-\rho)/(1+\rho)$.
Overlapping returns (a 20-day forward return sampled daily) are the classic case in signal research.

## Worked examples

### Example 1 - is the monthly mean return positive?

"A strategy has 60 monthly returns with mean 1.0% and standard deviation 4%. Give a 95% interval for the mean."

$\text{SE} = 4/\sqrt{60} = 0.516\%$ and $t_{59,0.975} = 2.001$.
Interval: $1.0 \pm 2.001\times0.516 = [-0.03\%, 2.03\%]$, which just includes zero.
The $t$-stat is $1.94$; equivalently the annualised Sharpe is $0.25\sqrt{12} = 0.866$ and $0.866\sqrt5 = 1.94$.
Five years of a Sharpe-0.87 strategy is not statistically distinguishable from luck at 5%.

### Example 2 - confidence interval for a Sharpe ratio

"A strategy has an annualised Sharpe of 1.5 over three years of daily returns. 95% interval?"

Daily Sharpe is $1.5/\sqrt{252} = 0.0945$ with $n = 756$.
$\text{SE}_{\text{daily}} = \sqrt{(1+0.0945^2/2)/756} = 0.03645$, annualised $0.03645\sqrt{252} = 0.579$.
Interval: $1.5\pm1.96\times0.579 = [0.37, 2.63]$.
A simulation of 20,000 three-year paths gives a standard deviation of 0.580 for the annualised estimate.
The shortcut $1/\sqrt{3} = 0.577$ is almost identical, because at daily frequency the volatility term $SR_d^2/2$ is negligible.

### Example 3 - how long to prove an edge

"How many years of live trading are needed to show, at $t = 2$, a Sharpe of 2, 1 and 0.5? And for 80% power at 5% two-sided?"

| True annual Sharpe | Years for $t=2$: $(2/S)^2$ | Years for 80% power: $(2.80/S)^2$ |
| :--- | :--- | :--- |
| 2.0 | 1 | 1.96 |
| 1.0 | 4 | 7.85 |
| 0.5 | 16 | 31.4 |

This is why low-Sharpe strategies are judged on economic priors and out-of-sample consistency rather than on their own track record, and why high-frequency books with Sharpe above 5 can be validated in weeks.

### Example 4 - hit rate and the number of trades needed

"You win 55% of 400 trades. 95% interval for the win rate? How many trades do you need to show that a 52% win rate beats 50%?"

$\text{SE} = \sqrt{0.55\times0.45/400} = 0.0249$, interval $[0.501, 0.599]$; the $z$-stat against 50% is $0.05/\sqrt{0.25/400} = 2.0$.
For 52%, reaching $z = 1.96$ at the observed rate needs $n = (1.96\times0.5/0.02)^2 = 2401$ trades.
For 80% power: $n = \big((1.96\times0.5 + 0.8416\sqrt{0.52\times0.48})/0.02\big)^2 \approx 4904$ trades.
Win rate alone is not edge: the payoff ratio matters as much, so test mean PnL per trade when you can.

### Example 5 - interval for a volatility

"30 daily returns have sample standard deviation 2%. 95% interval for $\sigma$ under normality?"

$\chi^2_{29,0.025} = 16.05$ and $\chi^2_{29,0.975} = 45.72$.
$\sigma\in\big[2\sqrt{29/45.72},\ 2\sqrt{29/16.05}\big] = [1.59\%, 2.69\%]$.
The interval is asymmetric because the $\chi^2$ is skewed; with fat-tailed returns the true coverage is lower, so bootstrap it ([Bootstrap and Resampling](12-Bootstrap-and-Resampling.md)).

## Pitfalls

- Saying "there is a 95% probability that $\mu$ lies in $[a,b]$" about a realised frequentist interval; that is a Bayesian credible-interval statement.
- Annualising a Sharpe ratio by $\sqrt{252}$ when returns are autocorrelated (smoothed marks, illiquid assets); positive autocorrelation overstates it.
- Treating overlapping-horizon observations as independent and quoting $t$-stats that are several times too large.
- Using the $\chi^2$ variance interval on fat-tailed returns; it undercovers badly.
- Using the Wald interval for a rare-event proportion such as a fill-failure rate; use Wilson or exact intervals.
- Reading non-overlapping intervals as the only evidence of a difference: two intervals can overlap while the difference is significant, because $\text{SE}(\hat a-\hat b) < \text{SE}(\hat a)+\text{SE}(\hat b)$.
- Reporting the Sharpe of the best of many backtests with this SE; selection needs the multiple-testing corrections in [Hypothesis Testing](03-Hypothesis-Testing-and-Multiple-Comparisons.md).

## Interview questions

> [!question]- stat-ci-frequentist-interpretation | What does a 95% confidence interval mean?
> The procedure covers the true parameter in 95% of repeated samples.
> The parameter is fixed; the interval is random, so a single realised interval either contains it or not.

> [!question]- stat-ci-halve-width-data | How much more data do you need to halve the width of a confidence interval for a mean?
> Four times as much.
> Width is proportional to $\sigma/\sqrt n$.

> [!question]- stat-ci-monthly-mean-return | 60 monthly returns have mean 1% and sd 4%. Is the mean significantly positive at 5%?
> No, just: $t = 1.94$ and the 95% interval is about $[-0.03\%, 2.03\%]$.
> $\text{SE} = 4/\sqrt{60} = 0.516\%$ and $t_{59,0.975} = 2.001$.

> [!question]- stat-ci-sharpe-standard-error-lo | What is the standard error of an estimated Sharpe ratio from n iid normal returns?
> $\sqrt{(1+SR^2/2)/n}$ in per-period units.
> Delta method on $\bar r/s$: the mean contributes 1, the volatility $SR^2/2$.

> [!question]- stat-ci-sharpe-three-years | Annualised Sharpe 1.5 from three years of daily data. Approximate 95% interval?
> About $[0.37, 2.63]$.
> Annualised SE is about $1/\sqrt{3} = 0.58$; the exact daily formula gives $0.579$.

> [!question]- stat-ci-years-to-detect-sharpe | How many years are needed for a Sharpe-1 strategy to reach a t-stat of 2?
> 4 years.
> $t = SR_{\text{ann}}\sqrt{T}$, so $T = (2/1)^2$; for 80% power at 5% two-sided it is about 7.85 years.

> [!question]- stat-ci-t-distribution-origin | Where does the t distribution come from, and when does it matter?
> A standard normal divided by $\sqrt{\chi^2_k/k}$ independent of it, as when $\sigma$ is replaced by $s$.
> It matters for small $n$; $t_{59,0.975} = 2.00$ versus $1.96$, so beyond about 30 non-normality and dependence matter more.

> [!question]- stat-ci-chi-squared-variance-interval | 30 normal returns have sd 2%. 95% interval for sigma?
> About $[1.59\%, 2.69\%]$.
> $(n-1)s^2/\sigma^2\sim\chi^2_{29}$ with quantiles 16.05 and 45.72; invert and take square roots.

> [!question]- stat-ci-f-distribution-use | When does the F distribution appear?
> As a ratio of independent scaled chi-squared variables, $(\chi^2_k/k)/(\chi^2_m/m)$.
> Comparing two sample variances, and testing joint restrictions in regression.

> [!question]- stat-ci-win-rate-trades-needed | Roughly how many trades are needed to show a 52% win rate differs from 50% at the 5% level?
> About 2,400 for $z = 1.96$ at the observed rate, about 4,900 for 80% power.
> $n = (1.96\times0.5/0.02)^2 = 2401$.

> [!question]- stat-ci-rule-of-three | You see zero failures in 100 independent trials. Approximate 95% upper bound on the failure rate?
> $3/100 = 3\%$.
> Solve $(1-p)^{100} = 0.05$: $p = 1-0.05^{1/100} = 2.95\%$.

> [!question]- stat-ci-effective-sample-size-ar1 | Returns follow AR(1) with rho 0.3. How much information is in 1000 observations for estimating the mean?
> About 538 independent observations' worth.
> The variance of the mean inflates by $(1+\rho)/(1-\rho) = 1.857$, so $n_{\text{eff}} = 1000/1.857$.

> [!question]- stat-ci-overlapping-intervals | Two strategies' 95% intervals for mean return overlap. Can their difference still be significant?
> Yes.
> The SE of a difference of independent estimates is $\sqrt{s_a^2+s_b^2}$, smaller than $s_a+s_b$, so the difference test is stricter than the overlap check.

## In this repo and SDE-Interview-Prep

- [Inequalities and Limit Theorems](../01-Probability/06-Inequalities-and-Limit-Theorems.md) for the CLT behind Wald intervals.
- [Hypothesis Testing and Multiple Comparisons](03-Hypothesis-Testing-and-Multiple-Comparisons.md) for tests built on these intervals.
- [Bootstrap and Resampling](12-Bootstrap-and-Resampling.md) when normality or independence fails.
- [Overfitting and Deflated Sharpe](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md) and [Performance Metrics](../09-Alpha-Research-and-Portfolio/09-Performance-Metrics-and-Fundamental-Law.md) for Sharpe ratios in practice.

## Further reading

- Larry Wasserman, *All of Statistics*, chapter 6 (confidence sets) and chapter 10 (Wald and related intervals).
- Casella and Berger, *Statistical Inference* (2nd ed.), chapter 5 (sampling distributions) and chapter 9 (interval estimation).
- Andrew Lo (2002), "The Statistics of Sharpe Ratios", *Financial Analysts Journal*.
- Elmar Mertens (2002), "Comments on Variance of the IID Estimator in Lo (2002)", working paper.
- David Bailey and Marcos Lopez de Prado (2012), "The Sharpe Ratio Efficient Frontier", *Journal of Risk*.
