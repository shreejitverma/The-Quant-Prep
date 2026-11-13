---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: [time-series-stationarity-and-arma]
est_hours: 4
sources: [Tsay - Analysis of Financial Time Series (3rd ed.) ch 3, Engle (1982) - Autoregressive Conditional Heteroscedasticity - Econometrica 50(4), Bollerslev (1986) - Generalized Autoregressive Conditional Heteroskedasticity - Journal of Econometrics 31(3), J.P. Morgan and Reuters (1996) - RiskMetrics Technical Document (4th ed.), Glosten Jagannathan and Runkle (1993) - Journal of Finance 48(5), Nelson (1991) - Conditional Heteroskedasticity in Asset Returns - Econometrica 59(2), Parkinson (1980) - The Extreme Value Method for Estimating the Variance of the Rate of Return - Journal of Business 53(1), Garman and Klass (1980) - On the Estimation of Security Price Volatilities from Historical Data - Journal of Business 53(1), Andersen Bollerslev Diebold and Labys (2003) - Modeling and Forecasting Realized Volatility - Econometrica 71(2), Zhang Mykland and Ait-Sahalia (2005) - A Tale of Two Time Scales - JASA 100(472), Patton (2011) - Volatility Forecast Comparison Using Imperfect Volatility Proxies - Journal of Econometrics 160(1), Engle and Patton (2001) - What Good Is a Volatility Model - Quantitative Finance 1(2), Cont (2001) - Empirical Properties of Asset Returns - Quantitative Finance 1(2)]
---

# Volatility Models: EWMA and GARCH

## TL;DR

- Returns are close to uncorrelated but their squares are strongly and persistently autocorrelated: volatility clusters, and conditional variance is forecastable even when the mean is not.
- EWMA: $\sigma_t^2 = \lambda\sigma_{t-1}^2 + (1-\lambda)r_{t-1}^2$ (RiskMetrics daily $\lambda = 0.94$, half-life 11.2 days); it has no long-run level, so its forecast term structure is flat.
- GARCH(1,1): $\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta\sigma_{t-1}^2$; persistence $\alpha+\beta$, long-run variance $\omega/(1-\alpha-\beta)$, shock half-life $\ln 0.5/\ln(\alpha+\beta)$, and forecasts revert geometrically to the long-run level.
- The leverage effect (negative returns raise future volatility more than positive ones) is captured by GJR-GARCH or EGARCH.
- Range estimators are about 4.9 (Parkinson) and 7.4 (Garman-Klass) times more efficient than close-to-close; realized variance from intraday returns is better still until microstructure noise, which biases it by $2n\,\text{Var}(\text{noise})$, dominates.
- Judge variance forecasts with MSE or QLIKE on a noisy proxy; both rank forecasts correctly, MAE on volatility does not.

## Learning objectives

- Estimate volatility with EWMA and GARCH(1,1) and interpret persistence.
- Use realized volatility estimators (close-to-close, Parkinson, Garman-Klass, realized variance).
- Explain volatility clustering and the leverage effect.

## Core concepts

### Stylised facts

- Volatility clustering: large moves follow large moves; the ACF of $r_t^2$ or $|r_t|$ is positive and decays slowly (Cont 2001).
- Fat tails: unconditional kurtosis well above 3 (Cont 2001), partly explained by time-varying variance (a mixture of normals is fat-tailed).
- Mean reversion of volatility: high-vol regimes decay toward a long-run level; implied vol term structures slope toward it.
- Leverage effect: returns are negatively correlated with future volatility (Cont 2001).

The modelling set-up is $r_t = \sigma_t z_t$ with $z_t$ iid, mean 0, variance 1, and $\sigma_t^2$ known at $t-1$.

### EWMA

$$
\sigma_t^2 = \lambda\sigma_{t-1}^2 + (1-\lambda)r_{t-1}^2 = (1-\lambda)\sum_{k\ge1}\lambda^{k-1} r_{t-k}^2.
$$

Weights decay geometrically: the most recent squared return gets $1-\lambda$, the half-life of the weights is $\ln 0.5/\ln\lambda$ and the centre of mass is $1/(1-\lambda)$ days.
RiskMetrics uses $\lambda = 0.94$ for daily data (half-life 11.2 days) and 0.97 for monthly forecasts.
EWMA is GARCH(1,1) with $\omega = 0$ and $\alpha + \beta = 1$ (integrated GARCH): $E_t[\sigma_{t+h}^2] = \sigma_{t+1}^2$ for all $h$, so it cannot forecast vol mean reversion.

### ARCH and GARCH

Engle's ARCH(1): $\sigma_t^2 = \omega + \alpha r_{t-1}^2$, unconditional variance $\omega/(1-\alpha)$, and kurtosis $3(1-\alpha^2)/(1-3\alpha^2)$ for Gaussian $z_t$ (finite if $\alpha^2 < 1/3$).
Bollerslev's GARCH(1,1):

$$
\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta \sigma_{t-1}^2, \qquad \omega > 0,\ \alpha,\beta \ge 0.
$$

- Covariance stationary iff $\alpha + \beta < 1$; long-run variance $\bar\sigma^2 = \omega/(1-\alpha-\beta)$.
- Rewriting with $\nu_t = r_t^2 - \sigma_t^2$ (a martingale difference) gives $r_t^2 = \omega + (\alpha+\beta)r_{t-1}^2 + \nu_t - \beta\nu_{t-1}$: squared returns follow an ARMA(1,1), so persistence $\alpha+\beta$ plays the role of the AR coefficient.
- Forecast: $E_t[\sigma^2_{t+h}] = \bar\sigma^2 + (\alpha+\beta)^{h-1}(\sigma^2_{t+1} - \bar\sigma^2)$, with half-life $\ln 0.5/\ln(\alpha+\beta)$.
- The variance forecast for a horizon $H$ is the sum of these daily forecasts, which gives a model term structure of volatility.
- $\alpha$ is the reaction to news, $\beta$ is memory.
  Engle and Patton (2001) fit daily Dow Jones returns from August 1988 to August 2000 and get $\alpha = 0.0399$ and $\beta = 0.9505$: persistence 0.9904 and a half-life of $\ln 0.5/\ln 0.9904 = 71.9$ days (they report about 73, counting the horizon from $t$ rather than $t+1$).
- Gaussian-innovation kurtosis: $3\,[1-(\alpha+\beta)^2]/[1-(\alpha+\beta)^2-2\alpha^2]$, finite when the denominator is positive.

### Estimation

Maximise the Gaussian log-likelihood, dropping constants:

$$
\ell(\omega,\alpha,\beta) = -\frac12\sum_{t}\Big(\ln\sigma_t^2 + \frac{r_t^2}{\sigma_t^2}\Big).
$$

With Gaussian likelihood but fat-tailed $z_t$ the estimates are still consistent (quasi-MLE); use robust (sandwich) standard errors or a Student-$t$ likelihood.
Variance targeting fixes $\omega = \hat\sigma^2(1-\alpha-\beta)$ from the sample variance and leaves two parameters.
The likelihood surface is flat along $\alpha+\beta \approx$ const near 1, so individual $\alpha$ and $\beta$ are less stable than their sum.

### Asymmetry

- GJR-GARCH: $\sigma_t^2 = \omega + (\alpha + \gamma\,\mathbf 1_{r_{t-1}<0})r_{t-1}^2 + \beta\sigma_{t-1}^2$; persistence $\alpha + \gamma/2 + \beta$ for symmetric $z_t$.
- EGARCH (Nelson 1991) models $\ln\sigma_t^2$, so no positivity constraints, with a term in $z_{t-1}$ for the sign effect.
- Black (1976) proposed the leverage explanation (falling equity raises financial leverage); Campbell and Hentschel (1992) model the alternative, volatility feedback (rising risk premia push prices down).

### Realized and range-based estimators

Per-day variance estimators, with $O,H,L,C$ the open, high, low and close:

| Estimator | Formula | Efficiency vs close-to-close |
| :--- | :--- | :--- |
| Close-to-close | $\frac{1}{n-1}\sum (r_i - \bar r)^2$ | 1 |
| Parkinson (1980) | $\frac{1}{4\ln 2}\,[\ln(H/L)]^2$ | 4.91 (exact) |
| Garman-Klass (1980) | $\tfrac12[\ln(H/L)]^2 - (2\ln2-1)[\ln(C/O)]^2$ | about 7.4 |
| Rogers-Satchell | $\ln\frac HC\ln\frac HO + \ln\frac LC\ln\frac LO$ | drift-robust |

Efficiency means variance ratio for a driftless Brownian motion: $\text{Var}(r^2)/\text{Var}(\hat\sigma^2)$ with $\text{Var}(r^2) = 2\sigma^4$.
Parkinson's is exact from the range moments $E[R^2] = 4\ln 2\,\sigma^2$ and $E[R^4] = 9\zeta(3)\sigma^4$, giving $2/0.4073 = 4.91$; Garman-Klass's 7.4 is confirmed by simulating exact Brownian ranges.
So Parkinson over 20 days is roughly as precise as close-to-close over 100.
Range estimators ignore the overnight gap (add it separately, as Yang-Zhang does) and are biased down by discrete sampling of the path.

Realized variance $RV_t = \sum_{i=1}^n r_{t,i}^2$ over intraday returns converges to integrated variance as $n \to \infty$ in a frictionless market (Andersen, Bollerslev, Diebold and Labys 2003).
With iid microstructure noise of variance $\omega^2$ on observed log prices, $E[RV] = IV + 2n\omega^2$: sampling faster makes the estimate worse.
Remedies are sparse sampling (5 minutes), the two-scales estimator of Zhang, Mykland and Ait-Sahalia (2005), and realized kernels; the volatility signature plot (mean RV against sampling interval) diagnoses the noise.

### Evaluating forecasts

The true variance is unobserved, so forecasts $h_t$ are scored against a noisy proxy $\hat\sigma_t^2$ such as $r_t^2$ or RV.
Patton (2011) shows MSE $(\hat\sigma^2 - h)^2$ and QLIKE $\hat\sigma^2/h - \ln(\hat\sigma^2/h) - 1$ give the same ranking as with the true variance; MAE and MSE on volatility (not variance) do not.
With the proxy $r^2 = \sigma^2 z^2$, the expected MSE and QLIKE are both minimised at $h = \sigma^2$, but MAE on volatility is minimised at $h = 0.455\sigma^2$, the median of $z^2$, so it rewards forecasts that are far too low.
QLIKE penalises under-forecasting more, which matches the risk manager's asymmetry.

## Worked examples

### 1. GARCH(1,1) update and long-run level

Daily fit: $\omega = 2\times10^{-6}$, $\alpha = 0.08$, $\beta = 0.90$.

- Persistence $0.98$; long-run variance $2\times10^{-6}/0.02 = 10^{-4}$, i.e. 1.00% daily or $1\%\times\sqrt{252} = 15.9\%$ annualised.
- Shock half-life $\ln 0.5/\ln 0.98 = 34.3$ days.
- Yesterday $\sigma = 1.5\%$ and the return was $-3\%$: $\sigma^2 = 2\times10^{-6} + 0.08\times0.0009 + 0.90\times0.000225 = 2.765\times10^{-4}$, so tomorrow's vol is 1.66% (26.4% annualised).

### 2. EWMA update

RiskMetrics $\lambda = 0.94$, yesterday's vol 1%, yesterday's return $-4\%$.
$\sigma^2 = 0.94\times10^{-4} + 0.06\times16\times10^{-4} = 1.90\times10^{-4}$, vol 1.38%.
A single 4-sigma day lifts vol by 38%; the weight on that day then halves every 11.2 days, and the return from five days ago carries weight $0.06\times0.94^4 = 0.047$.

### 3. Term structure from GARCH versus EWMA

Continue example 1 with $\sigma^2_{t+1} = 2.765\times10^{-4}$ and $\bar\sigma^2 = 10^{-4}$.

- Daily vol forecast at $h = 10$: $\sqrt{10^{-4} + 0.98^9\times1.765\times10^{-4}} = 1.57\%$; at $h = 21$, 1.48%; at $h = 63$, 1.23%.
- One-month (21-day) volatility, from the average of the 21 daily variance forecasts: 1.57% daily, 24.9% annualised.
- One-year volatility: 18.4% annualised, close to the 15.9% long-run level.
- EWMA with the same spot variance forecasts 26.4% at every horizon.

A trader comparing to implied vol should compare like horizons: GARCH says one-month vol is rich above about 25% and one-year vol above about 18%.

### 4. Range estimators on one day

$O = 100$, $H = 103$, $L = 98$, $C = 101$.
$\ln(H/L) = 0.04976$, $\ln(C/O) = 0.00995$.

- Parkinson: $0.04976^2/(4\ln 2) = 8.93\times10^{-4}$, vol 2.99% (47.4% annualised).
- Garman-Klass: $0.5\times0.04976^2 - 0.3863\times0.00995^2 = 1.20\times10^{-3}$, vol 3.46% (55.0% annualised).
- Close-to-close squared return: $0.00995^2 = 9.9\times10^{-5}$, vol 0.995% (15.8% annualised).

The day closed near its open after a 5% range; the close-to-close estimate misses the intraday risk entirely, which is why range estimators are more efficient.

### 5. Microstructure noise in realized variance

True daily integrated variance $10^{-4}$ (1% vol), iid noise with standard deviation 1 bp on log prices ($\omega^2 = 10^{-8}$).

- 5-minute sampling ($n = 78$): bias $2\times78\times10^{-8} = 1.56\times10^{-6}$, 1.6% of IV.
- 1-minute sampling ($n = 390$): bias $7.8\times10^{-6}$, 7.8% of IV.
- 1-second sampling ($n = 23{,}400$): bias $4.68\times10^{-4}$, 4.7 times IV.

This is why the signature plot rises sharply at the finest sampling intervals.

### 6. Unconditional kurtosis from GARCH

For $\alpha = 0.08$, $\beta = 0.90$ with Gaussian $z_t$: $3(1-0.9604)/(1-0.9604-2\times0.0064) = 0.1188/0.0268 = 4.43$.
Time-varying variance alone produces kurtosis 4.4 from normal shocks; empirical daily equity kurtosis is usually higher, which motivates Student-$t$ innovations.
For ARCH(1) with $\alpha = 0.3$: $3(1-0.09)/(1-0.27) = 3.74$.

### 7. Fitting GARCH(1,1) by maximum likelihood

Simulate 5,000 daily returns from the example 1 model with `numpy.random.default_rng(1)`, then maximise the Gaussian log-likelihood above over $(\omega,\alpha,\beta)$ subject to $\omega > 0$, $\alpha,\beta \ge 0$ and $\alpha+\beta < 1$, initialising $\sigma_1^2$ at the sample variance.
The fit gives $\hat\omega = 2.13\times10^{-6}$, $\hat\alpha = 0.084$ and $\hat\beta = 0.895$.
On 20 years of simulated daily data the fit recovers persistence 0.979 against a true 0.98 and long-run vol 16.0% against 15.9%.
[`code/stats_09_garch.py`](code/stats_09_garch.py) runs this fit with a from-scratch Nelder-Mead and checks that no neighbouring parameter vector has a higher likelihood.

## Pitfalls

- Annualising with $\sqrt{252}$ a GARCH forecast of the next day when the question is about the next month; use the horizon-average variance.
- Calling EWMA a mean-reverting model: its forecast is flat at every horizon.
- Reading high persistence ($\alpha+\beta = 0.995$) as a stable parameter; near-integrated fits often signal structural breaks or regime shifts in the sample.
- Comparing GARCH vol to implied vol without the variance risk premium: implied is usually above realized on average ([Implied Volatility and the Smile](../05-Derivatives-and-Volatility/07-Implied-Volatility-and-the-Smile.md)).
- Sampling realized variance at the tick level and ignoring microstructure noise.
- Using Parkinson or Garman-Klass on assets with large overnight gaps without adding the close-to-open component.
- Scoring vol forecasts with MAE or with $R^2$ against squared returns: the proxy is so noisy that a perfect forecast gets a low $R^2$.
- Forgetting positivity and stationarity constraints in the optimiser, which gives negative variances or explosive forecasts.

## Interview questions

> [!question]- stat-garch-long-run-variance | GARCH(1,1) with $\omega = 2\times10^{-6}$, $\alpha = 0.08$, $\beta = 0.90$ on daily returns. Long-run annualised vol?
> About 15.9%.
> $\bar\sigma^2 = \omega/(1-\alpha-\beta) = 10^{-4}$, daily vol 1%, times $\sqrt{252}$.

> [!question]- stat-garch-persistence-half-life | What is persistence in GARCH(1,1), and what is the half-life of a vol shock when it is 0.98?
> Persistence is $\alpha+\beta$, the rate at which the variance forecast reverts; half-life $\ln 0.5/\ln 0.98 = 34$ days.
> $E_t[\sigma^2_{t+h}] - \bar\sigma^2 = (\alpha+\beta)^{h-1}(\sigma^2_{t+1}-\bar\sigma^2)$.

> [!question]- stat-garch-ewma-igarch | How is EWMA related to GARCH, and what is its main forecasting weakness?
> EWMA is GARCH(1,1) with $\omega = 0$ and $\alpha+\beta = 1$ (IGARCH).
> It has no long-run variance, so the forecast term structure is flat and never mean-reverts.

> [!question]- stat-garch-ewma-half-life | What is the half-life of the weights in RiskMetrics daily EWMA?
> About 11.2 days.
> $\lambda = 0.94$ and $\ln 0.5/\ln 0.94 = 11.2$; the centre of mass is $1/(1-\lambda) = 16.7$ days.

> [!question]- stat-garch-update | GARCH(1,1) $\omega = 2\times10^{-6}$, $\alpha = 0.08$, $\beta = 0.9$; yesterday vol 1.5% and return $-3\%$. Today's vol?
> About 1.66%.
> $\sigma^2 = 2\times10^{-6} + 0.08\times0.0009 + 0.9\times0.000225 = 2.765\times10^{-4}$.

> [!question]- stat-garch-clustering-evidence | How do you show volatility clustering in a return series whose ACF is flat?
> Look at the ACF of $r_t^2$ or $|r_t|$, or run Ljung-Box or Engle's ARCH LM test on squared returns.
> Uncorrelated is not independent: the squares are strongly and slowly decaying autocorrelated.

> [!question]- stat-garch-leverage-effect | What is the leverage effect and which models capture it?
> Negative returns raise future volatility more than positive returns of the same size.
> GJR-GARCH adds $\gamma\mathbf 1_{r<0}r^2$; EGARCH models $\ln\sigma^2$ with a signed $z$ term; standard GARCH is symmetric and cannot.

> [!question]- stat-garch-parkinson | Write the Parkinson estimator and say why it beats close-to-close.
> $\hat\sigma^2 = [\ln(H/L)]^2/(4\ln2)$ per day.
> The range uses the whole intraday path, giving 4.91 times the efficiency of squared close-to-close returns for a driftless Brownian motion.

> [!question]- stat-garch-rv-noise | Why does sampling realized variance every second give a worse estimate than every five minutes?
> Microstructure noise adds $2n\omega^2$ to $E[RV]$, so bias grows linearly with the number of returns.
> With 1 bp noise the bias is 1.6% of a 1% daily variance at 5 minutes but 4.7 times it at 1 second.

> [!question]- stat-garch-kurtosis | Can GARCH with Gaussian shocks produce fat-tailed unconditional returns?
> Yes: time-varying variance makes the unconditional distribution a scale mixture of normals.
> For $\alpha = 0.08$, $\beta = 0.9$ the kurtosis is $3(1-0.9604)/(1-0.9604-0.0128) = 4.43$.

> [!question]- stat-garch-term-structure | GARCH spot vol is 26.4% annualised and the long-run level is 15.9% with persistence 0.98. Is 1-month vol closer to 26% or 16%?
> Closer to 26%: about 24.9%.
> The 34-day half-life means little decay within 21 days; the one-year figure is about 18.4%.

> [!question]- stat-garch-forecast-loss | Which loss functions should you use to compare variance forecasts against a noisy proxy like squared returns?
> MSE on variance or QLIKE, $\hat\sigma^2/h - \ln(\hat\sigma^2/h) - 1$.
> Patton (2011) shows these rank forecasts as the true variance would; MAE and losses on volatility are distorted by proxy noise.

> [!question]- stat-garch-stationarity-condition | When does a GARCH(1,1) have a finite unconditional variance?
> When $\alpha + \beta < 1$.
> Taking expectations, $E[\sigma^2] = \omega + (\alpha+\beta)E[\sigma^2]$, which has a finite positive solution only if $\alpha+\beta < 1$.

> [!question]- stat-garch-engle-patton-half-life | Engle and Patton fit daily Dow Jones returns and get alpha = 0.0399 and beta = 0.9505. What is the half-life of a volatility shock?
> About 72 days (71.9 counted from $t+1$; they report about 73, counting from $t$).
> Persistence is $0.0399 + 0.9505 = 0.9904$ and the half-life is $\ln 0.5/\ln 0.9904$.

> [!question]- stat-garch-range-efficiency | How much more efficient are the Parkinson and Garman-Klass estimators than squared close-to-close returns?
> About 4.9 and 7.4 times, for a driftless Brownian motion with no overnight gap.
> Parkinson: $\text{Var} = (9\zeta(3)/(4\ln 2)^2 - 1)\sigma^4 = 0.4073\sigma^4$ against $2\sigma^4$; Garman-Klass adds the open-to-close return to the range.

## In this repo and The-Distinguished-Engineer

- Code: [`code/stats_09_garch.py`](code/stats_09_garch.py) prints and asserts every number on this page: variance forecasts by iterating the expectation recursion and by Monte Carlo, kurtosis by solving the moment recursions, Parkinson efficiency exactly from the range moments and Garman-Klass by simulating exact Brownian ranges, the noise bias by simulating a noisy price path, Patton's loss result by minimising expected losses, and the GARCH fit by a from-scratch Nelder-Mead.
- Related notes: [Variance Swaps and Volatility Products](../05-Derivatives-and-Volatility/14-Variance-Swaps-and-Volatility-Products.md), [VaR and Expected Shortfall](../11-Risk-and-Trading/03-VaR-and-Expected-Shortfall.md), [Heavy Tails and Extreme Value Theory](13-Heavy-Tails-and-Extreme-Value-Theory.md), [Time Series: Stationarity and ARMA](08-Time-Series-Stationarity-and-ARMA.md).

## Further reading

- Ruey Tsay, *Analysis of Financial Time Series*, chapter 3.
- Robert Engle (1982), Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation, Econometrica.
- Tim Bollerslev (1986), Generalized Autoregressive Conditional Heteroskedasticity, Journal of Econometrics.
- J.P. Morgan and Reuters (1996), RiskMetrics Technical Document.
- Glosten, Jagannathan and Runkle (1993), On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks, Journal of Finance.
- Parkinson (1980) and Garman and Klass (1980), Journal of Business.
- Andersen, Bollerslev, Diebold and Labys (2003), Modeling and Forecasting Realized Volatility, Econometrica.
- Patton (2011), Volatility Forecast Comparison Using Imperfect Volatility Proxies, Journal of Econometrics.
- Robert Engle and Andrew Patton (2001), What Good Is a Volatility Model?, Quantitative Finance 1(2), 237-245.
- Rama Cont (2001), Empirical Properties of Asset Returns: Stylized Facts and Statistical Issues, Quantitative Finance 1(2), 223-236.
- Fischer Black (1976), Studies of Stock Price Volatility Changes, Proceedings of the American Statistical Association, Business and Economic Statistics Section.
- John Campbell and Ludger Hentschel (1992), No News Is Good News: An Asymmetric Model of Changing Volatility in Stock Returns, Journal of Financial Economics 31(3).
- L. C. G. Rogers and S. E. Satchell (1991), Estimating Variance from High, Low and Closing Prices, Annals of Applied Probability 1(4).
- Dennis Yang and Qiang Zhang (2000), Drift-Independent Volatility Estimation Based on High, Low, Open, and Close Prices, Journal of Business 73(3).
