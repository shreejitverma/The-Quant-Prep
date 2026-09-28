---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [confidence-intervals-and-sampling]
est_hours: 4
sources: [Wasserman - All of Statistics ch 10, Casella and Berger - Statistical Inference 2nd ed ch 8, Harvey Liu and Zhu (2016) - ... and the Cross-Section of Expected Returns - Review of Financial Studies, Benjamini and Hochberg (1995) - Controlling the False Discovery Rate - JRSS B, Holm (1979) - A Simple Sequentially Rejective Multiple Test Procedure - Scandinavian Journal of Statistics, White (2000) - A Reality Check for Data Snooping - Econometrica, Bailey and Lopez de Prado (2014) - The Deflated Sharpe Ratio - Journal of Portfolio Management, Ioannidis (2005) - Why Most Published Research Findings Are False - PLoS Medicine]
---

# Hypothesis Testing and Multiple Comparisons

## TL;DR

- The p-value is $P(\text{statistic at least as extreme as observed}\mid H_0)$; it is not $P(H_0\mid\text{data})$ and not the probability the result is a fluke.
- Type I error rate $\alpha$ is controlled by design; power $1-\beta$ depends on the true effect, the noise and $n$; for a strategy, $t\approx SR_{\text{ann}}\sqrt{T}$.
- Testing $m$ hypotheses at level $\alpha$ each gives $1-(1-\alpha)^m$ chance of at least one false positive: 64% for 20 independent tests.
- Bonferroni and Holm control the family-wise error rate; Benjamini-Hochberg controls the false discovery rate and is far more powerful when many effects are real.
- The best of $N$ zero-edge backtests has an expected Sharpe of about $E[\max_N Z]/\sqrt{T}$, 1.12 for $N=100$ over 5 years; demand $t > 3$ (Harvey, Liu and Zhu) or deflate.

## Learning objectives

- Explain p-values, power, type I and II errors precisely.
- Control family-wise error (Bonferroni, Holm) and false discovery rate (Benjamini-Hochberg).
- Recognise data snooping and p-hacking in research workflows.

## Core concepts

### The testing framework

A test fixes a null $H_0$, an alternative $H_1$, a statistic $T$ and a rejection region $R$ with $P(T\in R\mid H_0)\le\alpha$.

| | $H_0$ true | $H_0$ false |
| :--- | :--- | :--- |
| Reject | Type I error (rate $\alpha$) | Correct (power $1-\beta$) |
| Do not reject | Correct | Type II error (rate $\beta$) |

The p-value is the smallest $\alpha$ at which the observed data would reject; under a continuous null it is uniform on $[0,1]$.
"Not rejecting" is not evidence for $H_0$ when power is low.
Neyman-Pearson: for simple versus simple hypotheses, the likelihood-ratio test is the most powerful at its size.
In large samples the Wald, score and likelihood-ratio tests are equivalent; the LR statistic $2(\ell_1-\ell_0)$ is asymptotically $\chi^2$ with degrees of freedom equal to the number of restrictions.

### Testing a trading signal

For per-period returns with mean $\mu$ and volatility $\sigma$, $t = \bar r/(s/\sqrt n) = \widehat{SR}\sqrt n$, or $\widehat{SR}_{\text{ann}}\sqrt{T}$ in years.
Power of a one-sided level-$\alpha$ test against a true Sharpe $S$:

$$
1-\beta \approx \Phi\big(S\sqrt{T} - z_{1-\alpha}\big).
$$

One-sided tests are appropriate only if the direction was fixed before looking at the data; otherwise use two-sided.
Statistical significance is not economic significance: with enough data a Sharpe of 0.1 is significant and still worthless after costs.

### Base rates and the false-discovery problem

If a fraction $\pi$ of tested ideas are real, the probability that a significant result is real (the positive predictive value) is

$$
\text{PPV} = \frac{\pi(1-\beta)}{\pi(1-\beta) + (1-\pi)\alpha}.
$$

Low priors and low power make most "discoveries" false (Ioannidis 2005), which is the typical regime in alpha research.

### Family-wise error rate

FWER is $P(\text{at least one false rejection})$.
Bonferroni: reject $H_i$ if $p_i\le\alpha/m$; valid under any dependence by the union bound.
Holm step-down: sort $p_{(1)}\le\dots\le p_{(m)}$; reject $H_{(1)},\dots,H_{(k)}$ while $p_{(k)}\le\alpha/(m-k+1)$, stopping at the first failure.
Holm is uniformly more powerful than Bonferroni and still controls FWER under arbitrary dependence.
For correlated strategies, resampling methods (White's reality check, Hansen's SPA test, Romano-Wolf stepdown) test the best performer against the null that none beats the benchmark while using the joint dependence.

### False discovery rate

FDR is $E[V/\max(R,1)]$, the expected fraction of rejections that are false.
Benjamini-Hochberg step-up at level $q$: find the largest $k$ with $p_{(k)}\le kq/m$ and reject $H_{(1)},\dots,H_{(k)}$, even those that individually miss their own threshold.
BH controls FDR at $q\,m_0/m\le q$ for independent or positively dependent tests; Benjamini-Yekutieli divides by $\sum_{i=1}^m 1/i$ for arbitrary dependence.
Use FWER when one false positive is costly (a single flagship strategy); use FDR when screening many candidate signals for a combined book.

### Data snooping in research

- Garden of forking paths: universe, lookback, rebalancing, winsorisation and neutralisation choices multiply the effective number of tests even when only one final backtest is "run".
- Counting trials: record every variant tried (see [Overfitting and Deflated Sharpe](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md)).
- Expected maximum: with $N$ independent null strategies each estimated over $T$ years, $E[\max\widehat{SR}]\approx E[\max_{i\le N}Z_i]/\sqrt{T}$, where $E[\max Z]$ is 1.54, 2.51 and 3.24 for $N = 10, 100, 1000$.
- Harvey, Liu and Zhu (2016) count hundreds of published factors and argue a new factor needs $t > 3$ rather than $t > 2$.
- A holdout period only helps if it is touched once; reusing it turns it into training data.

## Worked examples

### Example 1 - is a Sharpe of 0.8 over five years significant?

$t = 0.8\sqrt5 = 1.789$.
Two-sided $p = 2(1-\Phi(1.789)) = 0.074$; one-sided $p = 0.037$.
So it is significant at 5% only if a positive sign was the pre-registered hypothesis, and it falls well short of Harvey-Liu-Zhu's $t > 3$, which would take $9/0.64 \approx 14$ years at this Sharpe.

### Example 2 - power of a five-year backtest

"True Sharpe 0.5, five years of data, one-sided 5% test. Power?"

$1-\beta = \Phi(0.5\sqrt5 - 1.645) = \Phi(-0.527) = 0.30$.
A genuinely good Sharpe-0.5 strategy is rejected 70% of the time; for Sharpe 1 the power is $\Phi(2.236-1.645) = 0.72$.
Low power is why a failed backtest of a strong prior idea should not be over-read either.

### Example 3 - Bonferroni, Holm and Benjamini-Hochberg on ten signals

"Ten signals give sorted p-values 0.001, 0.0052, 0.012, 0.021, 0.024, 0.041, 0.09, 0.2, 0.5, 0.8. Which survive at 5%?"

Bonferroni threshold $0.05/10 = 0.005$: only 0.001 survives, 1 rejection.
Holm thresholds $0.05/10, 0.05/9, 0.05/8,\dots = 0.005, 0.00556, 0.00625$: 0.001 and 0.0052 pass, 0.012 fails and the procedure stops, 2 rejections.
BH thresholds $k\times0.005$: $0.005, 0.010, 0.015, 0.020, 0.025, 0.030,\dots$
$p_{(4)} = 0.021 > 0.020$ fails its own threshold, but $p_{(5)} = 0.024\le0.025$, so the largest qualifying $k$ is 5 and the first five are rejected.
BH-adjusted p-values ($\min_{j\ge k} p_{(j)}m/j$) are $0.010, 0.026, 0.040, 0.048, 0.048, 0.068,\dots$, confirming 5 below 0.05.

### Example 4 - family-wise error and the best of many backtests

"You test 20 independent useless signals at 5%. Chance of at least one hit? You backtest 100 zero-Sharpe variants over 5 years; what Sharpe do you expect the winner to show?"

$1 - 0.95^{20} = 0.64$; for 100 tests it is $0.994$.
Each annualised Sharpe estimate is roughly $N(0, 1/5)$, so the best is about $2.508/\sqrt5 = 1.12$.
A backtested Sharpe of 1.1 from the best of 100 variants is exactly what pure noise delivers; the deflated Sharpe ratio (Bailey and Lopez de Prado 2014) formalises this correction.

### Example 5 - how many significant signals are real?

"5% of ideas you test are real, your tests have 50% power, and you use $\alpha = 5\%$. What fraction of significant results are real?"

$\text{PPV} = \frac{0.05\times0.5}{0.05\times0.5 + 0.95\times0.05} = \frac{0.025}{0.0725} = 0.345$.
Two out of three "discoveries" are false.
With a 10% prior and 80% power it rises to $0.08/(0.08+0.045) = 0.64$: better priors (economic rationale) and more power (more data, better signal construction) both matter.

## Pitfalls

- Reading a p-value as the probability that the null is true, or $1-p$ as the probability the strategy works.
- Treating $p = 0.06$ and $p = 0.04$ as qualitatively different evidence.
- Choosing one-sided versus two-sided after seeing the sign of the result.
- Counting only the final backtest when dozens of parameterisations were tried; the effective $m$ is what was searched, not what was reported.
- Reusing a holdout set until something passes, and stopping data collection as soon as $p < 0.05$ (optional stopping inflates Type I error).
- Using Bonferroni on hundreds of highly correlated signals and concluding nothing works; it is valid but very conservative there, so use Holm, FDR or a resampling method.
- Applying BH to strongly negatively dependent tests without the Benjamini-Yekutieli correction.
- Confusing significance with size: report the effect (Sharpe, IC, bps per trade) with its interval, not just a p-value.

## Interview questions

> [!question]- stat-ht-p-value-definition | Define a p-value precisely.
> The probability, computed under $H_0$, of a test statistic at least as extreme as the one observed.
> It is not $P(H_0\mid\text{data})$; under a continuous null it is uniform on $[0,1]$.

> [!question]- stat-ht-type-i-ii-errors | Define Type I and Type II errors and power.
> Type I: rejecting a true null (rate $\alpha$); Type II: failing to reject a false null (rate $\beta$); power is $1-\beta$.
> $\alpha$ is set by design; $\beta$ depends on effect size, noise and sample size.

> [!question]- stat-ht-sharpe-t-stat | A strategy has annualised Sharpe 0.8 over 5 years. t-stat and two-sided p-value?
> $t\approx1.79$, $p\approx0.074$.
> $t = SR_{\text{ann}}\sqrt T$ for iid returns; one-sided $p = 0.037$.

> [!question]- stat-ht-power-sharpe-half | True Sharpe 0.5, 5 years of data, one-sided 5% test. What is the power?
> About 30%.
> $\Phi(0.5\sqrt5 - 1.645) = \Phi(-0.53)$.

> [!question]- stat-ht-fwer-twenty-tests | 20 independent tests of true nulls at 5%. Probability of at least one false positive?
> About 64%.
> $1-0.95^{20} = 0.642$.

> [!question]- stat-ht-bonferroni-vs-holm | How does Holm differ from Bonferroni, and which is better?
> Holm compares the $k$-th smallest p-value with $\alpha/(m-k+1)$ and stops at the first failure; Bonferroni uses $\alpha/m$ for all.
> Both control FWER under any dependence, and Holm rejects everything Bonferroni does and sometimes more.

> [!question]- stat-ht-benjamini-hochberg-procedure | Describe the Benjamini-Hochberg procedure.
> Sort p-values, find the largest $k$ with $p_{(k)}\le kq/m$, reject the $k$ smallest.
> It is step-up: a p-value above its own threshold is still rejected if a larger one qualifies; it controls FDR at $q$ under independence or positive dependence.

> [!question]- stat-ht-fdr-vs-fwer | When do you control FDR instead of FWER in research?
> FDR when screening many signals where some false positives are tolerable; FWER when any single false positive is costly.
> FDR bounds the expected share of false discoveries, so it keeps power when many effects are real.

> [!question]- stat-ht-expected-max-null-sharpe | You backtest 100 independent zero-edge strategies over 5 years. Expected best annualised Sharpe?
> About 1.12.
> Each estimate is about $N(0,1/5)$ and $E[\max$ of 100 standard normals$]\approx2.51$, so $2.51/\sqrt5$.

> [!question]- stat-ht-harvey-liu-zhu-threshold | What t-stat hurdle do Harvey, Liu and Zhu suggest for a new factor, and why?
> About 3 rather than 2.
> Hundreds of factors have been tested on the same data, so multiple-testing adjustments (Bonferroni, Holm, BHY) raise the hurdle.

> [!question]- stat-ht-ppv-base-rate | 5% of ideas are real, power is 50%, alpha is 5%. What fraction of significant results are real?
> About 34.5%.
> $0.025/(0.025 + 0.0475)$: false positives from the 95% null ideas outnumber true positives.

> [!question]- stat-ht-p-hacking-examples | Name three forms of p-hacking in quant research.
> Trying many parameterisations and reporting the best; stopping or extending the sample once significant; reusing the holdout set.
> Each raises the effective number of tests while the reported p-value assumes one.

> [!question]- stat-ht-bh-step-up-example | p-values 0.001, 0.0052, 0.012, 0.021, 0.024, then all above 0.04, m = 10, q = 5%. How many BH rejections, and how many Holm?
> BH rejects 5, Holm 2.
> BH: $p_{(5)} = 0.024\le5\times0.005$; Holm stops at $0.012 > 0.05/8$.

> [!question]- stat-ht-significant-vs-important | A signal has p = 1e-6 on 10 million observations. Should you trade it?
> Not on that basis: with huge $n$ a tiny, uneconomic effect becomes significant.
> Check the effect size against costs and capacity, and its stability out of sample.

## In this repo and SDE-Interview-Prep

- [Confidence Intervals and Sampling](02-Confidence-Intervals-and-Sampling.md) for the standard errors used here.
- [Research Process and Hypothesis Discipline](../09-Alpha-Research-and-Portfolio/01-Research-Process-and-Hypothesis-Discipline.md) and [Backtesting Methodology and Pitfalls](../09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md) for the workflow side.
- [Overfitting and Deflated Sharpe](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md) for correcting the best-of-N Sharpe.
- [Order Statistics and Extremes](../01-Probability/08-Order-Statistics-and-Extremes.md) for the expected maximum of normals.

## Further reading

- Larry Wasserman, *All of Statistics*, chapter 10 (p-values, Wald and LR tests, multiple testing).
- Casella and Berger, *Statistical Inference* (2nd ed.), chapter 8.
- Campbell Harvey, Yan Liu and Heqing Zhu (2016), "... and the Cross-Section of Expected Returns", *Review of Financial Studies*.
- Yoav Benjamini and Yosef Hochberg (1995), "Controlling the False Discovery Rate", *Journal of the Royal Statistical Society B*.
- Sture Holm (1979), "A Simple Sequentially Rejective Multiple Test Procedure", *Scandinavian Journal of Statistics*.
- Halbert White (2000), "A Reality Check for Data Snooping", *Econometrica*.
- David Bailey and Marcos Lopez de Prado (2014), "The Deflated Sharpe Ratio", *Journal of Portfolio Management*.
- John Ioannidis (2005), "Why Most Published Research Findings Are False", *PLoS Medicine*.
