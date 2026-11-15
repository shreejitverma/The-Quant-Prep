---
type: concept
track: [quant-research, quant-trader]
tier: core
status: solid
prereqs: [signals-features-and-alpha-decay]
est_hours: 3
sources: [Grinold and Kahn - Active Portfolio Management 2nd ed (1999), Grinold (1989) - The Fundamental Law of Active Management - Journal of Portfolio Management 15(3) 30-37, Clarke de Silva and Thorley (2002) - Portfolio Constraints and the Fundamental Law of Active Management - Financial Analysts Journal 58(5) 48-66, Lo (2002) - The Statistics of Sharpe Ratios - Financial Analysts Journal 58(4) 36-52, Mertens (2002) - Variance of the IID Estimator in Lo (2002) - working paper University of Basel, Bailey and Lopez de Prado (2012) - The Sharpe Ratio Efficient Frontier - Journal of Risk 15(2) 3-44, Merton (1980) - On Estimating the Expected Return on the Market - Journal of Financial Economics 8(4) 323-361]
---

# Performance Metrics and the Fundamental Law

## TL;DR

- Sharpe $= (\bar r - r_f)/\hat\sigma$ per period, annualised by $\sqrt{q}$ with $q$ periods per year, which is valid only for serially uncorrelated returns; Lo's correction uses $\eta(q) = q/\sqrt{q + 2\sum_{k=1}^{q-1}(q-k)\rho_k}$.
- Standard error of a per-period Sharpe from $T$ iid returns: $\sqrt{(1 + SR^2/2)/T}$ if normal (Lo 2002), $\sqrt{(1 - \gamma_3 SR + \frac{\gamma_4-1}{4}SR^2)/T}$ in general (Mertens 2002); annualised, roughly $1/\sqrt{\text{years}}$.
- Sortino divides by downside deviation $\sqrt{E[\min(r - \tau, 0)^2]}$ over all observations, not by the standard deviation of the negative returns; information ratio is active return over tracking error.
- Fundamental law: $\text{IR} \approx \text{IC}\sqrt{\text{BR}}$, with BR the number of independent bets per year; with constraints $\text{IR} \approx \text{TC}\cdot\text{IC}\sqrt{\text{BR}}$.
- Its assumptions (independent bets, constant IC, unconstrained mean-variance use of $\alpha = \text{IC}\,\sigma z$) are exactly what fails in practice; correlated bets shrink effective breadth dramatically.

## Learning objectives

- Compute Sharpe, Sortino, information ratio, drawdown and turnover correctly (annualisation included).
- State the fundamental law of active management and use it to reason about breadth.
- Know the standard error of a Sharpe ratio estimate.

## Core concepts

### Return conventions

Simple returns aggregate across assets ($r_p = \sum_i w_i r_i$); log returns aggregate across time ($\ln(1+R_{0,T}) = \sum_t \ln(1+r_t)$).
Annualised arithmetic mean is $q\bar r$; the geometric (compound) growth rate is lower by about $\sigma^2/2$ per year, the volatility drag.
State which you report.

### Sharpe ratio and annualisation

$$
\widehat{SR} = \frac{\bar r - r_f}{\hat\sigma}, \qquad \widehat{SR}_{\text{ann}} = \sqrt q\,\widehat{SR} \ \text{(iid returns)}.
$$

The $\sqrt q$ rule follows because the mean scales by $q$ and the standard deviation by $\sqrt q$ when returns are uncorrelated.
For a long-short or dollar-neutral book, $r_f$ is usually dropped because the capital earns (roughly) the cash rate separately; for a long-only fund, subtract it.

**Serial correlation (Lo 2002).**
With autocorrelations $\rho_k$ of the per-period returns, the variance of the $q$-period sum is $\sigma^2[q + 2\sum_{k=1}^{q-1}(q-k)\rho_k]$, so

$$
SR_{\text{ann}} = \eta(q)\,SR, \qquad \eta(q) = \frac{q}{\sqrt{q + 2\sum_{k=1}^{q-1}(q-k)\rho_k}}.
$$

Positive autocorrelation (smoothed or stale marks: private assets, illiquid credit, some hedge fund indices) means $\eta(q) < \sqrt q$ and naive annualisation overstates Sharpe.

### Standard error of a Sharpe estimate

For $T$ iid normal returns, the delta method on $(\hat\mu, \hat\sigma)$ gives (Lo 2002)

$$
\text{Var}(\widehat{SR}) \approx \frac{1 + \tfrac12 SR^2}{T}.
$$

Derivation sketch: $\text{Var}(\hat\mu) = \sigma^2/T$, $\text{Var}(\hat\sigma) \approx \sigma^2/(2T)$ for normal data, they are independent, and $\partial SR/\partial\mu = 1/\sigma$, $\partial SR/\partial\sigma = -\mu/\sigma^2$, so $\text{Var} \approx \frac1T + \frac{\mu^2}{\sigma^4}\frac{\sigma^2}{2T}$.
For non-normal iid returns with skewness $\gamma_3$ and kurtosis $\gamma_4$ (normal $=3$), $\hat\mu$ and $\hat\sigma$ are correlated and $\hat\sigma$ is noisier, giving Mertens' (2002) form, as quoted in Bailey and Lopez de Prado (2012, equation 8)

$$
\text{Var}(\widehat{SR}) \approx \frac{1 + \tfrac12 SR^2 - \gamma_3 SR + \tfrac{\gamma_4 - 3}{4}SR^2}{T} = \frac{1 - \gamma_3 SR + \tfrac{\gamma_4-1}{4}SR^2}{T},
$$

which is the denominator of the probabilistic Sharpe ratio ([Overfitting and Deflated Sharpe](08-Overfitting-and-Deflated-Sharpe.md)).
Everything is per period.
To annualise the standard error, multiply by $\sqrt q$: with daily data the $SR^2$ terms are tiny and $\text{SE}_{\text{ann}} \approx 1/\sqrt{\text{years}}$, the most useful number in this note.

### Other metrics

- **Sortino:** $(\bar r - \tau)/\text{DD}_\tau$ with downside deviation $\text{DD}_\tau = \sqrt{\frac1T\sum_t \min(r_t - \tau, 0)^2}$ over all $T$ observations and target $\tau$ (often 0 or $r_f$).
- **Information ratio:** $\text{IR} = \bar a/\sigma_a$ where $a_t = r_{p,t} - r_{b,t}$ is active return against a benchmark and $\sigma_a$ is tracking error; for a market-neutral book with a cash benchmark, IR and Sharpe coincide.
- **Maximum drawdown:** $\text{MDD} = \min_t \big(V_t/\max_{s\le t}V_s - 1\big)$ on the compounded equity curve; it is path dependent and grows with sample length, so compare drawdowns only over equal horizons ([Drawdowns and Risk Limits](../11-Risk-and-Trading/05-Drawdowns-and-Risk-Limits.md)).
- **Calmar:** annualised return divided by $|\text{MDD}|$ over a stated window; state the window, because the drawdown grows with it.
- **Turnover:** traded value over capital, either $\sum_i|w_{i,t} - w_{i,t-1}|$ (two-sided) or half of that (one-sided, "fraction of the book replaced"); always state which, because cost per unit turnover depends on it.
- **Hit rate and payoff ratio:** win fraction $p$ and average win over average loss $b$; expectancy per trade is $p\,\bar W - (1-p)\bar L$.

### The fundamental law of active management

**Setup (Grinold 1989).** $N$ assets with uncorrelated residual returns of volatility $\sigma_i$, standardised scores $z_i$ ($E z_i^2 = 1$), and alphas from the forecasting rule $\alpha_i = \text{IC}\,\sigma_i z_i$.
The unconstrained mean-variance active portfolio $h_i = \alpha_i/(2\lambda\sigma_i^2)$ has

$$
\text{IR}^2 = \sum_i \frac{\alpha_i^2}{\sigma_i^2} = \text{IC}^2\sum_i z_i^2 \approx \text{IC}^2 N, \qquad \text{IR} \approx \text{IC}\sqrt{\text{BR}},
$$

with breadth BR the number of independent forecasts per year (assets times independent rebalances).

**Assumptions, each a common interview probe:**

1. Bets are independent: residuals uncorrelated and forecast errors uncorrelated across bets and through time.
2. IC is the same for every bet and constant over time.
3. The manager implements the forecasts without constraints (no long-only, no position limits, no costs).
4. The risk model is correct.
5. IC is small (the law is a first-order approximation).

**Transfer coefficient.** Clarke, de Silva and Thorley (2002) generalise the law to constrained portfolios, $\text{IR} \approx \text{TC}\cdot\text{IC}\sqrt{\text{BR}}$, where TC is the cross-sectional correlation between the risk-adjusted forecasts $\alpha_i/\sigma_i$ and the risk-adjusted active weights $h_i\sigma_i$ actually held.
Unconstrained mean-variance weights give $\text{TC} = 1$; any constraint that stops the weights following the forecasts (long-only, position caps, turnover limits) lowers it.

**Breadth is the fragile input.**
Rebalancing monthly does not create 12 independent bets per stock if the signal changes slowly, and 500 stocks are not 500 bets if the positions load on shared industry and style factors, so that the bet payoffs (position times residual return) are correlated.
A useful heuristic is the variance-of-a-mean formula: $N$ bets whose payoffs have pairwise correlation $\rho$ act like $N/(1 + (N-1)\rho)$ independent bets.
Correlated residuals alone do not do this damage: in a dollar-neutral book built from a demeaned signal the common component cancels, which is why neutralisation ([Signals, Features and Alpha Decay](03-Signals-Features-and-Alpha-Decay.md)) protects breadth.

## Worked examples

### 1. Annualising a daily track record

Daily mean return 0.05%, daily standard deviation 1%.

- Sharpe: $0.0005/0.01\times\sqrt{252} = 0.794$.
- Annualised arithmetic return $252\times0.05\% = 12.6\%$, volatility $1\%\sqrt{252} = 15.9\%$.
- The log (continuously compounded) growth rate is roughly $12.6\% - 15.9\%^2/2 = 11.3\%$ per year; integrating $E[\ln(1 + r)]$ for normal daily returns gives the same 11.3%.

### 2. How precise is a 3-year Sharpe of 1.5?

Daily returns for 3 years ($T = 756$), annualised Sharpe 1.5, skewness $-1$, kurtosis 8.

- Per-period Sharpe: $1.5/\sqrt{252} = 0.0945$.
- Normal (Lo): $\text{SE} = \sqrt{(1 + 0.0945^2/2)/756}\times\sqrt{252} = 0.579$ annualised.
- Non-normal (Mertens): $\sqrt{(1 + 0.0945 + \tfrac{7}{4}\times0.0945^2)/756}\times\sqrt{252} = 0.608$.
- 95% interval: $1.5 \pm 1.96\times0.608 = [0.31, 2.69]$; $t = 1.5/0.608 = 2.47$.

Trap: plugging the annualised Sharpe into $\sqrt{(1 + SR^2/2)/Y}$ with $Y = 3$ gives 0.84.
That formula is correct only if you actually observe 3 annual returns; the $SR^2$ term must use the per-period Sharpe at the sampling frequency.
Simulating 756 daily returns reproduces both standard errors: normal returns give 0.579, and a two-normal mixture with skewness $-1$ and kurtosis 8 gives 0.608, a difference the simulation resolves.
With 36 monthly returns the asymptotic formula gives 0.60 (a simulation of 36 normal monthly returns gives about 0.62, the small-sample excess), close to the daily 0.579, because precision of the mean comes from the length of history, not the sampling frequency (Merton 1980 makes this point for the expected market return, while variances do sharpen with finer sampling).

### 3. Autocorrelated monthly returns

Monthly Sharpe 0.3 and first-order autocorrelation 0.2 (higher lags zero).

- Naive: $0.3\sqrt{12} = 1.04$.
- Lo: $\eta(12) = 12/\sqrt{12 + 2\times11\times0.2} = 12/\sqrt{16.4} = 2.963$, so $SR_{\text{ann}} = 0.3\times2.963 = 0.89$.

Naive annualisation overstates the Sharpe by 17% ($1.04/0.89$) from one modest autocorrelation; simulating monthly MA(1) returns with lag-1 autocorrelation 0.2 and taking the Sharpe of annual sums reproduces 0.89.

### 4. The fundamental law in numbers

- Equity stat arb: IC 0.02 on 500 stocks rebalanced monthly with a signal that fully refreshes each month: $\text{BR} = 6000$, $\text{IR} = 0.02\sqrt{6000} = 1.55$.
- Same book long-only with $\text{TC} = 0.5$: $\text{IR} = 0.77$.
- If the 500 bet payoffs within each month have average pairwise correlation 0.05, effective breadth per month is $500/(1 + 499\times0.05) = 19.3$, so $\text{IR} = 0.02\sqrt{12\times19.3} = 0.30$.
- Contrast: if instead only the residual returns share a common component with correlation 0.05 and the signal is demeaned each month, the common part cancels and the simulated IR stays near $0.02\sqrt{6000/0.95} = 1.59$, slightly above 1.55 because the remaining idiosyncratic variance is 0.95.
- A trader making 10 independent even-money bets a day with a 52% hit rate: for a binary forecast $\text{IC} = 2p - 1 = 0.04$ and $\text{BR} = 2520$, so $\text{IR} = 0.04\sqrt{2520} = 2.0$.

Simulating 20,000 months of a 500-name book reproduces the first three lines within sampling error: IR 1.55 for weights $h = \alpha/\sigma^2$, 0.77 when the held risk-adjusted weights have correlation 0.5 with the forecasts, and 0.30 when the bet payoffs are equicorrelated at 0.05.

### 5. Drawdown and Sortino done right

Prices from the demo in [performance_metrics.py](code/performance_metrics.py): 100, 102, 104, 103, 105, 108, 101, 103.

- Returns: $2.00\%, 1.96\%, -0.96\%, 1.94\%, 2.86\%, -6.48\%, 1.98\%$; mean 0.471%, standard deviation 3.29%.
- Max drawdown: peak 108 to trough 101, $101/108 - 1 = -6.48\%$.
- Downside deviation with $\tau = 0$ over all 7 returns: $\sqrt{(0.0096^2 + 0.0648^2)/7} = 2.48\%$ (2.4766% unrounded), so annualised Sortino $= 0.004710/0.024766\times\sqrt{252} = 3.02$; with the inputs rounded to 0.00471 and 0.0248 the product is 3.01.
- The demo's `sortino_ratio` computes exactly this and prints 3.0189. A common bug is to divide by the sample standard deviation of the two negative returns instead (3.90% here), which reports 1.92; that measures dispersion among losses, not downside risk, and it is undefined with fewer than two losing periods.

```python
import numpy as np, pandas as pd
prices = pd.Series([100, 102, 104, 103, 105, 108, 101, 103.0])
r = prices.pct_change().dropna()
downside = np.sqrt((np.minimum(r, 0) ** 2).mean())
print((prices / prices.cummax() - 1).min(), r.mean() / downside * np.sqrt(252))  # -0.0648 3.02
```

## Pitfalls

- Annualising with $\sqrt{252}$ when returns are autocorrelated, or with the wrong $q$ for the sampling frequency (weekly data needs $\sqrt{52}$).
- Quoting a Sharpe without its standard error; one year of Sharpe 1 is statistically indistinguishable from zero.
- Using the annualised Sharpe inside the $SR^2/2$ term of the standard error when data is daily.
- Computing Sortino from the standard deviation of losing periods only, or with a different target in numerator and denominator.
- Comparing max drawdowns across track records of different lengths.
- Mixing one-sided and two-sided turnover conventions when applying a cost per unit traded.
- Counting breadth as assets times rebalances when the signal barely changes between rebalances or the bets share factors.
- Treating the fundamental law as a forecast of realised IR rather than an upper-bound intuition for how IC, breadth and constraints trade off.

## Interview questions

> [!question]- alpha-perf-sharpe-se-iid | What is the standard error of a Sharpe ratio estimated from $T$ iid normal returns?
> $\sqrt{(1 + SR^2/2)/T}$ in per-period units (Lo 2002).
> From the delta method: the mean contributes $1/T$ and the volatility estimate, with variance $\sigma^2/(2T)$, contributes $SR^2/(2T)$.

> [!question]- alpha-perf-sharpe-se-nonnormal | How do skewness and kurtosis change the Sharpe standard error?
> $\text{Var}(\widehat{SR}) \approx (1 - \gamma_3 SR + \tfrac{\gamma_4-1}{4}SR^2)/T$ (Mertens 2002), with $\gamma_4 = 3$ for normal.
> Negative skew and fat tails raise the variance, so crash-prone strategies need longer track records for the same confidence.

> [!question]- alpha-perf-sharpe-se-rule | Roughly what is the standard error of an annualised Sharpe estimated from $Y$ years of daily data?
> About $1/\sqrt{Y}$.
> The per-period $SR^2$ terms are negligible at daily frequency, so $\text{SE}_{\text{ann}} \approx \sqrt{252/(252Y)}$; five years gives about 0.45.

> [!question]- alpha-perf-lo-autocorr | Monthly Sharpe 0.3 with lag-1 autocorrelation 0.2. Annualised Sharpe?
> About 0.89, not 1.04.
> Lo's $\eta(12) = 12/\sqrt{12 + 2\cdot11\cdot0.2} = 2.963$ replaces $\sqrt{12} = 3.464$.

> [!question]- alpha-perf-sortino-correct | How is the Sortino ratio's denominator defined?
> Downside deviation $\sqrt{\frac1T\sum_t\min(r_t - \tau, 0)^2}$ over all $T$ periods.
> It is a lower partial moment about the target, not the standard deviation of the losing returns, which ignores how often losses occur.

> [!question]- alpha-perf-ir-vs-sharpe | What is the difference between the information ratio and the Sharpe ratio?
> IR is mean active return over tracking error relative to a benchmark; Sharpe is mean excess return over total volatility.
> For a market-neutral book benchmarked to cash they coincide; for a long-only manager IR measures skill relative to the index.

> [!question]- alpha-perf-fundamental-law | State the fundamental law of active management.
> $\text{IR} \approx \text{IC}\sqrt{\text{BR}}$, where BR is the number of independent bets per year.
> It follows from $\alpha_i = \text{IC}\,\sigma_i z_i$ and unconstrained mean-variance weights on uncorrelated residuals: $\text{IR}^2 = \sum\alpha_i^2/\sigma_i^2 = \text{IC}^2 N$.

> [!question]- alpha-perf-fl-assumptions | What assumptions does the fundamental law make?
> Independent bets, the same constant IC for each bet, unconstrained implementation of the forecasts, a correct risk model and small IC.
> Violations (correlated bets, long-only constraints, costs, time-varying IC) all reduce realised IR below $\text{IC}\sqrt{\text{BR}}$.

> [!question]- alpha-perf-fl-numeric | IC 0.02 on 500 stocks with a signal that fully refreshes monthly. Fundamental-law IR?
> About 1.55.
> Breadth $500\times12 = 6000$ and $0.02\sqrt{6000} = 1.55$.

> [!question]- alpha-perf-transfer-coefficient | What is the transfer coefficient?
> The correlation between risk-adjusted forecasts and risk-adjusted active weights actually held.
> It enters as $\text{IR} \approx \text{TC}\cdot\text{IC}\sqrt{\text{BR}}$ (Clarke, de Silva and Thorley 2002); it is 1 for unconstrained mean-variance weights, and long-only and other constraints push it below 1.

> [!question]- alpha-perf-hit-rate-ic | A trader wins 52% of even-money bets and makes 10 independent bets a day. What IR does the fundamental law imply?
> About 2.0.
> For a binary forecast $\text{IC} = 2p - 1 = 0.04$, breadth is $10\times252 = 2520$, and $0.04\sqrt{2520} = 2.0$.

> [!question]- alpha-perf-effective-breadth | Why can 500 stocks give far fewer than 500 independent bets?
> When the positions load on shared industry and style factors, the bet payoffs are correlated.
> With average pairwise payoff correlation $\rho$ the effective number is about $N/(1 + (N-1)\rho)$; $\rho = 0.05$ turns 500 into about 19, while correlated residuals under a demeaned, neutralised signal largely cancel.

> [!question]- alpha-perf-mdd-horizon | Why should you not compare maximum drawdowns across track records of different lengths?
> The expected maximum drawdown grows with the length of the path.
> A longer record has more chances to hit a deep trough, so normalise by horizon or compare drawdown distributions from simulation.

> [!question]- alpha-perf-se-nonnormal-numeric | 3 years of daily returns, annualised Sharpe 1.5, skewness $-1$, kurtosis 8. Annualised standard error of the Sharpe?
> About 0.61 (0.608), against 0.579 for normal returns.
> Per-period Sharpe $0.0945$: $\sqrt{(1 + 0.0945 + \tfrac74\times0.0945^2)/756}\times\sqrt{252} = 0.608$, so the 95% interval is roughly $[0.31, 2.69]$.

> [!question]- alpha-perf-log-growth | Daily mean 0.05% and daily volatility 1%. What are the annualised arithmetic return and the log growth rate?
> 12.6% arithmetic and about 11.3% log growth.
> The drag is $\sigma^2/2 = 0.159^2/2 = 1.26\%$ a year; integrating $E[\ln(1 + r)]$ over normal daily returns confirms 11.3%.

## In this repo and The-Distinguished-Engineer

- Code: [`code/alpha_09_performance_metrics.py`](code/alpha_09_performance_metrics.py) prints and asserts every number on this page: the log growth rate by quadrature, Sharpe standard errors by simulating normal and skewed fat-tailed daily returns, Lo's correction by simulating MA(1) monthly returns, the fundamental law, transfer coefficient and effective breadth by simulating 500-name books, the binary-forecast IC by exact enumeration, and the drawdown and Sortino demo in exact fractions and through `performance_metrics.py`.
- Code: [performance_metrics.py](code/performance_metrics.py).

## Further reading

- Richard C. Grinold and Ronald N. Kahn, *Active Portfolio Management* (2nd ed., 1999).
- Richard C. Grinold, "The Fundamental Law of Active Management", *Journal of Portfolio Management* 15(3) (1989), 30-37.
- Roger Clarke, Harindra de Silva and Steven Thorley, "Portfolio Constraints and the Fundamental Law of Active Management", *Financial Analysts Journal* 58(5) (2002), 48-66.
- Andrew W. Lo, "The Statistics of Sharpe Ratios", *Financial Analysts Journal* 58(4) (2002), 36-52 (equations 8-9 for the iid standard error, equation 20 for $\eta(q)$).
- David H. Bailey and Marcos Lopez de Prado, "The Sharpe Ratio Efficient Frontier", *Journal of Risk* 15(2) (2012), 3-44.
- Robert C. Merton, "On Estimating the Expected Return on the Market: An Exploratory Investigation", *Journal of Financial Economics* 8(4) (1980), 323-361.
