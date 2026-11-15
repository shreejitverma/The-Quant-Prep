---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Bailey Borwein Lopez de Prado and Zhu (2014) - Pseudo-Mathematics and Financial Charlatanism - Notices of the AMS 61(5), Bailey and Lopez de Prado (2012) - The Sharpe Ratio Efficient Frontier - Journal of Risk 15(2), Bailey and Lopez de Prado (2014) - The Deflated Sharpe Ratio - Journal of Portfolio Management 40(5), Harvey Liu and Zhu (2016) - ... and the Cross-Section of Expected Returns - Review of Financial Studies 29(1), Harvey and Liu (2015) - Backtesting - Journal of Portfolio Management 42(1), Lo (2002) - The Statistics of Sharpe Ratios - Financial Analysts Journal 58(4), Mertens (2002) - Comments on Variance of the IID Estimator in Lo (2002) - research note, White (2000) - A Reality Check for Data Snooping - Econometrica 68(5), Lopez de Prado and Lewis (2019) - Detection of False Investment Strategies Using Unsupervised Learning Methods - Quantitative Finance 19(9)]
---

# Backtest Overfitting and Multiple Testing

## TL;DR

- Backtest overfitting is a leading reason why strategies with stellar historical performance disappoint in live trading.
- Selecting the best-performing strategy from $N$ trials inflates its in-sample Sharpe ratio even if every trial is pure noise.
- The expected maximum of $N$ independent standard normals grows like $\sqrt{2 \ln N}$, so the best null Sharpe ratio grows with the number of trials.
- For $N=1000$ pure-noise trials over $5$ years of daily data, the expected best annualized Sharpe is about $3.26 / \sqrt{5} \approx 1.46$, with no skill at all.
- The Probabilistic Sharpe Ratio (PSR) accounts for track record length, skewness and kurtosis.
- The Deflated Sharpe Ratio (DSR) is the PSR with the benchmark set to the expected maximum Sharpe across all $N$ trials.
- Harvey, Liu, and Zhu (2016) argued that, given how many factors have been tried, a new factor should clear $t > 3.0$ (two-sided $p < 0.0027$) rather than the usual $1.96$.

## Learning objectives

- Derive the extreme value distribution of the maximum Sharpe ratio under the null hypothesis.
- Calculate the Probabilistic Sharpe Ratio (PSR) correcting for sample length, skewness, and kurtosis.
- Compute the Deflated Sharpe Ratio (DSR) using trial count, variance of Sharpes, and track record duration.
- Apply Harvey-Liu multiple-testing haircuts (Bonferroni, Holm, BHY) to backtest Sharpe ratios.
- Determine the Minimum Backtest Length (MinBTL) required to avoid selection bias for a target Sharpe ratio.

## Core concepts

### 1. The Mechanism of Selection Bias Under the Null Hypothesis

Consider $N$ independent trading strategy variants evaluated on the same historical data.
Assume the null hypothesis $H_0$ holds: every strategy has zero true Sharpe ratio ($SR_{\text{true}} = 0$).
Each estimated Sharpe ratio $\widehat{SR}_n$ is a sample estimate, and $V$ is the variance of the $\widehat{SR}_n$ across trials.

If a researcher selects the top-performing configuration:

$$SR_{\max} = \max_{n=1, \dots, N} \widehat{SR}_n$$

Bailey and Lopez de Prado (2014) approximate the expected maximum of $N$ independent standard normal variables $Z_n$ with an extreme value argument:

$$E\left[\max_{n=1,\dots,N} Z_n\right] \approx (1 - \gamma)\Phi^{-1}\left(1 - \frac{1}{N}\right) + \gamma \Phi^{-1}\left(1 - \frac{1}{N e}\right)$$

Where $\gamma \approx 0.5772$ is the Euler-Mascheroni constant and $\Phi^{-1}$ is the inverse standard normal cumulative distribution function.

As trial count $N$ increases, the approximation gives (exact values by numerical integration in brackets):
- $N = 10 \implies E[\max Z] \approx 1.57$ (exact $1.54$)
- $N = 100 \implies E[\max Z] \approx 2.53$ (exact $2.51$)
- $N = 1000 \implies E[\max Z] \approx 3.26$ (exact $3.24$)
- $N = 10000 \implies E[\max Z] \approx 3.86$ (exact $3.85$)

The cruder asymptote $\sqrt{2 \ln N}$ is $3.72$ at $N = 1000$, so it overstates the maximum at practical trial counts.
Multiplying by $\sqrt{V}$ yields the expected best backtest Sharpe ratio under pure noise.
Reporting only the winner without reporting $N$ and $V$ hides the selection.

### 2. Probabilistic Sharpe Ratio (PSR)

Lo (2002) derived the asymptotic variance of the Sharpe ratio estimator, $(1 + \frac{1}{2}SR^2)/T$ for iid normal returns, and Mertens (2002) extended it to iid non-normal returns.
For a return series with sample length $T$, sample Sharpe ratio $\widehat{SR}$, skewness $\hat{\gamma}_3$, and kurtosis $\hat{\gamma}_4$ (not excess kurtosis), Bailey and Lopez de Prado (2012) use:

$$\text{Var}(\widehat{SR}) \approx \frac{1 - \hat{\gamma}_3 \widehat{SR} + \frac{\hat{\gamma}_4 - 1}{4}\widehat{SR}^2}{T - 1}$$

For normal returns ($\gamma_3 = 0, \gamma_4 = 3$), the variance simplifies to $\frac{1 + 0.5 \widehat{SR}^2}{T - 1}$.
For a positive Sharpe ratio, negative skewness and kurtosis above 3 widen the estimation variance.

Bailey and Lopez de Prado (2012) defined the **Probabilistic Sharpe Ratio (PSR)** as the probability that the true Sharpe ratio exceeds a benchmark threshold $SR^*$:

$$\text{PSR}(SR^*) = \Phi\left( \frac{(\widehat{SR} - SR^*)\sqrt{T - 1}}{\sqrt{1 - \hat{\gamma}_3 \widehat{SR} + \frac{\hat{\gamma}_4 - 1}{4}\widehat{SR}^2}} \right)$$

All parameters must be specified in consistent periodic units (e.g. daily).
A track record with substantial negative skewness (e.g. short options, carry trades) needs a higher headline Sharpe ratio to reach the same PSR.

### 3. Deflated Sharpe Ratio (DSR)

Bailey and Lopez de Prado (2014) combined the expected maximum with the non-normal PSR to create the **Deflated Sharpe Ratio (DSR)**.
Instead of testing against zero ($SR^* = 0$), DSR sets the benchmark equal to $SR_0$, the expected maximum Sharpe ratio from $N$ null trials:

$$SR_0 = \sqrt{V\big[\{\widehat{SR}_n\}\big]} \left( (1 - \gamma)\Phi^{-1}\left(1 - \frac{1}{N}\right) + \gamma \Phi^{-1}\left(1 - \frac{1}{N e}\right) \right)$$

$$\text{DSR} = \text{PSR}(SR_0) = \Phi\left( \frac{(\widehat{SR} - SR_0)\sqrt{T - 1}}{\sqrt{1 - \hat{\gamma}_3 \widehat{SR} + \frac{\hat{\gamma}_4 - 1}{4}\widehat{SR}^2}} \right)$$

DSR answers the due-diligence question:
"What is the probability that the true Sharpe ratio of the selected strategy exceeds what the best of $N$ skill-less trials would show?"
A common choice is to require $\text{DSR} \ge 0.95$, the analogue of a one-sided 5% test; the threshold is a convention you fix in advance, not a rule from the paper.

### 4. Harvey-Liu-Zhu Multiple Testing Haircuts ($t > 3.0$)

Campbell Harvey, Yan Liu, and Heqing Zhu (2016) catalogued hundreds of published factors that claim to explain the cross-section of expected returns.
A single test uses the two-sided 5% critical value $t = 1.96$, often rounded to $2.0$ (two-sided $p = 0.0455$).
When many factors have been tried, single-test thresholds produce many false discoveries.

To correct for multiple testing, Harvey and Liu (2015) convert the annualized Sharpe ratio into a $t$-statistic over $Y$ years of iid returns:

$$t = \widehat{SR}_{\text{ann}} \sqrt{Y}, \quad p = 2(1 - \Phi(t))$$

They apply family-wise error rate (FWER) and false discovery rate (FDR) adjustments to the ordered p-values $p_{(1)} \le \dots \le p_{(M)}$ of $M$ tests:
- **Bonferroni** (FWER): $p^{\text{Bonf}}_{(i)} = \min(1, M p_{(i)})$.
- **Holm** (FWER, less conservative): $p^{\text{Holm}}_{(i)} = \min\left(1, \max_{j \le i} (M - j + 1) p_{(j)}\right)$.
- **Benjamini-Hochberg-Yekutieli** (FDR under arbitrary dependence), with $c(M) = \sum_{j=1}^M \frac{1}{j}$: starting from the largest, $p^{\text{BHY}}_{(M)} = p_{(M)}$ and $p^{\text{BHY}}_{(i)} = \min\left(p^{\text{BHY}}_{(i+1)}, \frac{M c(M)}{i} p_{(i)}\right)$ for $i < M$.

The adjusted $t$-statistic and adjusted Sharpe ratio are:

$$t_{\text{adj}} = \Phi^{-1}\left(1 - \frac{p_{\text{adj}}}{2}\right), \quad \widehat{SR}_{\text{adj}} = \frac{t_{\text{adj}}}{\sqrt{Y}}$$

Harvey, Liu, and Zhu argued that, given the volume of data mining in the field, a newly proposed factor should clear $t > 3.0$ (two-sided $p < 0.0027$).

### 5. Minimum Backtest Length (MinBTL)

Bailey, Borwein, Lopez de Prado, and Zhu (2014, Theorem 3.1) derived the backtest length in years at which the expected best in-sample annualized Sharpe ratio of $N$ independent skill-less strategies equals a level $E[\max_N]$:

$$\text{MinBTL} \approx \left(\frac{(1 - \gamma)\Phi^{-1}\left(1 - \frac{1}{N}\right) + \gamma \Phi^{-1}\left(1 - \frac{1}{N e}\right)}{E[\max_N]}\right)^2 < \frac{2 \ln N}{E[\max_N]^2} \text{ years}$$

If a team tests $N=100$ independent variations and the best shows an annualized Sharpe ratio of $1.0$, the bracket evaluates to $2.53$, so:

$$\text{MinBTL} = \frac{(2.53)^2}{(1.0)^2} \approx 6.4 \text{ years}$$

With less than $6.4$ years of data, the best of $100$ skill-less trials is expected to show an in-sample Sharpe ratio above $1.0$, so seeing $1.0$ proves nothing; the upper bound $2 \ln N$ gives $9.2$ years.
The paper's own example: with only 5 years of data, no more than 45 independent configurations should be tried for an in-sample Sharpe ratio of 1 to mean anything (the bracket at $N = 45$ squared is $5.0$).
MinBTL is a necessary, not a sufficient, condition: a backtest longer than MinBTL can still be overfit.

---

## Worked examples

### Example 1: Calculating Deflated Sharpe Ratio for a Grid Search

A researcher runs a parameter sweep testing $N = 200$ parameter combinations of a momentum filter over $T = 1260$ trading days ($5.0$ years):
- The best variant achieves an annualized Sharpe ratio of $\widehat{SR}_{\text{ann}} = 1.60$ (daily $\widehat{SR} = \frac{1.60}{\sqrt{252}} = 0.10079$).
- Return moments of the winner: skewness $\hat{\gamma}_3 = -0.50$, kurtosis $\hat{\gamma}_4 = 4.50$.
- Cross-trial variance of daily Sharpe estimates, here set to its null value for $T = 1260$ normal returns: $V = \frac{1}{1259} = 0.0007943$ ($\sqrt{V} = 0.028183$).

1. **Expected Maximum Null Sharpe ($N=200$)**:
   $$p_1 = 1 - \frac{1}{200} = 0.995 \implies \Phi^{-1}(0.995) = 2.5758$$
   $$p_2 = 1 - \frac{1}{200e} = 1 - 0.001839 = 0.998161 \implies \Phi^{-1}(0.998161) = 2.9045$$
   $$\text{Bracket} = (1 - 0.5772)(2.5758) + (0.5772)(2.9045) = 1.0890 + 1.6765 = 2.7655$$
   $$SR_{0, \text{daily}} = 0.028183 \times 2.7655 = 0.07794$$
   $$SR_{0, \text{ann}} = 0.07794 \times \sqrt{252} = 1.237$$

2. **Standard Error of Sharpe Estimator**:
   $$\text{Var}(\widehat{SR}) = \frac{1 - (-0.50)(0.10079) + \frac{4.50 - 1}{4}(0.10079)^2}{1259} = \frac{1 + 0.0504 + 0.0089}{1259} = \frac{1.0593}{1259} = 0.0008414$$
   $$\sigma_{SR} = \sqrt{0.0008414} = 0.02901$$

3. **Deflated Sharpe Ratio (DSR)**:
   $$z = \frac{\widehat{SR} - SR_{0, \text{daily}}}{\sigma_{SR}} = \frac{0.10079 - 0.07794}{0.02901} = \frac{0.02285}{0.02901} = 0.788$$
   $$\text{DSR} = \Phi(0.788) = 78.5\%$$

**Verdict**: Because $\text{DSR} = 78.5\% < 95.0\%$, the strategy fails a 95% deflated Sharpe test.
Under the PSR approximation there is a $21.5\%$ probability that its true Sharpe ratio is no better than the best of 200 skill-less trials would show.
The approximation is close: the exact expected best daily Sharpe of 200 null trials is $0.0774$ (confirmed by seeded simulation), about $0.7\%$ below $SR_0$, because the bracket slightly overstates the exact expected maximum.

### Example 2: Harvey-Liu Bonferroni Haircut Calculation

An analyst presents a strategy with an annualized Sharpe of $1.20$ over $Y = 4.0$ years, having tested $M = 50$ strategy ideas:
- Raw $t$-statistic: $t = 1.20 \times \sqrt{4} = 2.40$.
- Raw two-sided $p$-value: $p = 2(1 - \Phi(2.40)) = 2(1 - 0.9918) = 0.0164$.
- Bonferroni adjusted $p$-value:
  $$p_{\text{Bonf}} = \min(1.0, 50 \times 0.0164) = 0.820$$
- Adjusted $t$-statistic:
  $$t_{\text{Bonf}} = \Phi^{-1}\left(1 - \frac{0.820}{2}\right) = \Phi^{-1}(0.590) = 0.228$$
- Adjusted Sharpe ratio:
  $$\widehat{SR}_{\text{Bonf}} = \frac{0.228}{\sqrt{4}} = 0.114$$
- Haircut percentage:
  $$\text{Haircut} = \left(1 - \frac{0.114}{1.20}\right) \times 100\% = 90.5\%$$

The multiple testing haircut cuts the headline Sharpe by over $90\%$, from $1.20$ to $0.11$.
The adjusted $t$-statistic ($0.23$) falls far short of the Harvey-Liu-Zhu $t > 3.0$ threshold.
BHY is no kinder here: if this is the most significant of the 50 tests, its BHY p-value is at most $50 \times c(50) \times 0.0164 = 50 \times 4.4992 \times 0.0164 = 3.69$, capped at $1$.

---

## Pitfalls

- **Hiding Failed Trials in the Research Graveyard**: Testing 500 parameters in private, deleting the failed scripts, and presenting the single surviving backtest as an "a priori hypothesis".
- **Ignoring Return Non-Normality**: Assuming normal returns for short-volatility or credit strategies, drastically underestimating Sharpe estimator variance and inflating PSR.
- **Using Unadjusted In-Sample PnL to Attract Capital**: Marketing a backtest with Sharpe $> 2.0$ without disclosing trial count $N$, backtest length, or DSR.
- **Overfitting Macro Parameters**: Tuning stop-loss, take-profit, and volatility lookbacks on the same historical crisis period (e.g. 2008 Lehman collapse), ensuring zero out-of-sample resilience.
- **Failing the Harvey-Liu-Zhu $t > 3.0$ Rule**: Treating a $t$-statistic of $2.1$ as significant when many similar factors have already been mined.

---

## Interview questions

> [!question]- mkt-sys-097 | What is backtest overfitting?
> Backtest overfitting occurs when a trading strategy's parameters are tuned to historical noise rather than persistent market structure, producing stellar backtests that fail out of sample.

> [!question]- mkt-sys-098 | What is the asymptotic expected maximum Sharpe ratio under the null hypothesis (Bailey and Lopez de Prado 2014)?
> Under the null of zero skill, the expected maximum Sharpe of N independent trials scales with sqrt(V) * [(1 - gamma) * Phi^{-1}(1 - 1/N) + gamma * Phi^{-1}(1 - 1/(N*e))].

> [!question]- mkt-sys-099 | What is the Euler-Mascheroni constant and what is its numerical value?
> It is the limit of the harmonic sum minus the natural logarithm, $\gamma = \lim_{n \to \infty} (\sum_{j=1}^n 1/j - \ln n) \approx 0.5772$.
> It weights the two quantiles in the expected-maximum approximation used by the Deflated Sharpe Ratio.

> [!question]- mkt-sys-100 | How does sample length T affect the variance of the Sharpe ratio estimator (Lo 2002)?
> The variance of the Sharpe estimator is inversely proportional to sample length: Var(SR) ~ (1 + 0.5 * SR^2) / T for iid normal returns (Bailey and Lopez de Prado use T - 1).

> [!question]- mkt-sys-101 | How do negative skewness and high kurtosis impact the standard error of the Sharpe ratio (Mertens 2002)?
> For a positive Sharpe ratio, negative skewness and kurtosis above 3 increase the numerator (1 - gamma_3 * SR + ((gamma_4 - 1)/4) * SR^2), widening the estimation variance and lowering statistical confidence.

> [!question]- mkt-sys-102 | Define the Probabilistic Sharpe Ratio (PSR).
> PSR is the probability that an observed Sharpe ratio exceeds a benchmark threshold SR*, adjusted for track record length, return skewness, and fat-tailed kurtosis.

> [!question]- mkt-sys-103 | Define the Deflated Sharpe Ratio (DSR).
> DSR is the Probabilistic Sharpe Ratio where the benchmark threshold is set equal to the expected maximum Sharpe ratio across N evaluated null trials.

> [!question]- mkt-sys-104 | What is the standard institutional confidence threshold for DSR?
> There is no regulatory or published standard; a common choice is DSR >= 0.95, the analogue of a one-sided 5% test.
> Fix the threshold before running the search, and record N so the DSR can be recomputed.

> [!question]- mkt-sys-105 | Why did Harvey, Liu, and Zhu (2016) recommend raising the factor discovery threshold from t > 2.0 to t > 3.0?
> Because hundreds of factors have been tested and published, multiple-testing adjustments (Bonferroni, Holm, BHY) push the hurdle well above the single-test 1.96; they argued for t > 3.0, a two-sided p-value below 0.0027.

> [!question]- mkt-sys-106 | What is the Bonferroni multiple testing adjustment?
> The Bonferroni correction multiplies the nominal p-value by the total number of tested hypotheses M: p_{Bonf} = min(1.0, M * p), controlling family-wise error rate.

> [!question]- mkt-sys-107 | What is the Benjamini-Hochberg-Yekutieli (BHY) false discovery rate control?
> BHY controls the false discovery rate under arbitrary dependence between tests.
> With p-values sorted ascending, the adjusted values are built from the largest down: p_(M) stays, and p_(i) = min(p_(i+1) adjusted, M * c(M) * p_(i) / i) with c(M) = sum_{j=1}^M 1/j (Harvey and Liu 2015).

> [!question]- mkt-sys-108 | Define Minimum Backtest Length (MinBTL).
> MinBTL is the backtest length in years at which the expected best in-sample Sharpe ratio of N independent skill-less trials falls to the observed level (Bailey, Borwein, Lopez de Prado and Zhu 2014).
> Shorter backtests make that Sharpe ratio expected from noise alone; it is a necessary, not sufficient, condition.

> [!question]- mkt-sys-109 | If an analyst tests N = 1000 random parameter combinations, what in-sample Sharpe can be expected by pure chance?
> For 5 years of daily data the standard error of an annualized Sharpe is about 1 / sqrt(5) = 0.447.
> The expected maximum of 1000 standard normals is about 3.26, so the expected best annualized Sharpe from pure noise is about 3.26 x 0.447 = 1.46.

> [!question]- mkt-sys-110 | What is the "researcher degrees of freedom" problem in quantitative finance?
> It refers to the countless discretionary choices made during research (data cleaning, universe rules, lookback windows, stop losses) that accumulate hidden multiple testing bias.

> [!question]- mkt-sys-111 | Why does parameter grid search exacerbate backtest overfitting?
> Grid searches systematically evaluate thousands of combinations; selecting the highest in-sample point overfits directly to the historical noise realization.

> [!question]- mkt-sys-112 | What is parameter cliff risk (fragility)?
> When a parameter setting produces high Sharpe, but adjacent parameter values produce disastrous performance, indicating an overfitted noise spike rather than a robust economic edge.

> [!question]- mkt-sys-113 | What is a parameter plateau (island of stability)?
> A broad region of parameter space where strategy performance remains consistently positive and stable across adjacent values, indicating structural robustness.

> [!question]- mkt-sys-114 | How does data snooping bias occur without formal code optimization?
> It occurs when a researcher visually inspects past price charts or reads historical market analyses before formulating and backtesting strategy rules.

> [!question]- mkt-sys-115 | What is cross-trial correlation and how does it affect effective trial count N?
> When tested strategy variants are highly correlated, they do not represent independent tests; effective trial count N* is lower than the raw number of backtest runs.

> [!question]- mkt-sys-116 | How does Bailey & Lopez de Prado's DSR handle correlated trials?
> V is measured across the Sharpe estimates of the trials actually run, so correlated trials show a smaller V.
> N should be the effective number of independent trials; Lopez de Prado and Lewis (2019) estimate it by clustering the trials' return series.

> [!question]- mkt-sys-117 | Why do short-volatility and carry strategies exhibit deceptively high in-sample Sharpe ratios?
> Because they experience long periods of steady small gains punctuated by rare catastrophic losses; unadjusted Sharpe ignores this severe negative skewness.

> [!question]- mkt-sys-118 | What is the relationship between t-statistic and annualized Sharpe ratio?
> t = SR_{ann} * sqrt(Y), where Y is the sample length in years under the assumption of iid returns.

> [!question]- mkt-sys-119 | What is a multiple-testing haircut?
> The percentage reduction in headline Sharpe ratio required to adjust for the number of tested hypotheses: Haircut = 1 - SR_{adj} / SR_{obs}.

> [!question]- mkt-sys-120 | Why is out-of-sample (OOS) testing alone insufficient to prevent overfitting?
> If a researcher repeatedly tests against the same "out-of-sample" dataset and tweaks parameters until OOS passes, the OOS data has been overfitted and becomes in-sample.

> [!question]- mkt-sys-121 | What is the file drawer problem (publication bias)?
> Only successful backtests with high Sharpe ratios are published or presented to investment committees, while the hundreds of failed attempts remain hidden in the file drawer.

> [!question]- mkt-sys-122 | How does the number of parameters in a strategy relate to overfitting risk?
> Overfitting risk rises with the number of free parameters, because the number of distinct configurations on a grid multiplies with each added parameter and more of them can fit noise.

> [!question]- mkt-sys-123 | What is White's Reality Check (White 2000)?
> A bootstrap test of whether the best of many candidate strategies beats a benchmark, with the null distribution built from the maximum over all candidates so that data snooping is accounted for (White 2000, Econometrica).

> [!question]- mkt-sys-124 | Why does expanding sample length T reduce the variance of the Sharpe estimator?
> Because the standard error scales inversely with sqrt(T - 1); more independent observations average out noise and tighten confidence intervals around true performance.

> [!question]- mkt-sys-125 | What is the difference between Family-Wise Error Rate (FWER) and False Discovery Rate (FDR)?
> FWER controls the probability of making even one false positive, while FDR controls the expected proportion of false positives among all rejected null hypotheses.

> [!question]- mkt-sys-126 | Why is FDR control (e.g. BHY) preferred over FWER (e.g. Bonferroni) in large-scale factor mining?
> Bonferroni becomes excessively conservative as trials reach thousands, rejecting true discoveries; FDR balances false positive control with discovery power.

> [!question]- mkt-sys-127 | How does the presence of serial autocorrelation in returns affect the Sharpe ratio t-statistic?
> With positive autocorrelation, the variance of multi-period returns exceeds the one-period variance times the horizon, so the iid t-statistic and the square-root-of-time annualized Sharpe ratio are overstated.
> Correct with Newey-West (HAC) standard errors or Lo's (2002) autocorrelation adjustment.

> [!question]- mkt-sys-128 | What is the golden rule of quantitative research discipline?
> Pre-register hypotheses based on sound economic or microstructure theory before touching data, and maintain an immutable research ledger recording every attempted trial.

> [!question]- mkt-sys-259 | With 5 years of data, how many independent strategy configurations can you try before an in-sample Sharpe ratio of 1 is expected from noise alone?
> About 45 (Bailey, Borwein, Lopez de Prado and Zhu 2014).
> MinBTL = bracket(N)^2 / SR^2 years, and the bracket (1 - gamma) Phi^-1(1 - 1/N) + gamma Phi^-1(1 - 1/(N e)) at N = 45 is 2.236, whose square is 5.0.

> [!question]- mkt-sys-260 | How accurate is the expected-maximum approximation inside the Deflated Sharpe Ratio?
> It slightly overstates the exact expected maximum of N standard normals: 1.57 against 1.54 at N = 10 and 3.26 against 3.24 at N = 1000.
> The error is conservative for DSR, because a higher benchmark lowers the deflated Sharpe ratio.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../code/mkt_sys_04_overfitting.py`](../code/mkt_sys_04_overfitting.py) prints and asserts every number on this page: the inverse normal by bisection on `erfc`, the expected maximum against exact numerical integration, the best null Sharpe ratio by seeded simulation of exact sample-Sharpe draws, the Mertens variance by simulating skewed returns, and the DSR, Bonferroni and MinBTL arithmetic.
- Related notes: [Overfitting and Deflated Sharpe](../../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md), [Combinatorial Purged Cross-Validation](05-Combinatorial-Purged-Cross-Validation.md).

## Further reading

- Bailey, D. H., Borwein, J. M., Lopez de Prado, M., & Zhu, Q. J. (2014). Pseudo-mathematics and financial charlatanism: The effects of backtest overfitting on out-of-sample performance. *Notices of the AMS*, 61(5), 458-471.
- Bailey, D. H., & Lopez de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk*, 15(2).
- Bailey, D. H., & Lopez de Prado, M. (2014). The deflated Sharpe ratio: Correcting for selection bias, backtest overfitting and non-normality. *The Journal of Portfolio Management*, 40(5), 94-107.
- Harvey, C. R., & Liu, Y. (2015). Backtesting. *The Journal of Portfolio Management*, 42(1), 13-28.
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). ... and the cross-section of expected returns. *The Review of Financial Studies*, 29(1), 5-68.
- Lo, A. W. (2002). The statistics of Sharpe ratios. *Financial Analysts Journal*, 58(4), 36-52.
- Lopez de Prado, M., & Lewis, M. J. (2019). Detection of false investment strategies using unsupervised learning methods. *Quantitative Finance*, 19(9), 1555-1565.
- Mertens, E. (2002). Comments on variance of the IID estimator in Lo (2002). Research note.
- White, H. (2000). A reality check for data snooping. *Econometrica*, 68(5), 1097-1126.
