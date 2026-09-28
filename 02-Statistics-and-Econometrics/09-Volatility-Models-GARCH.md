---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [time-series-stationarity-and-arma]
est_hours: 4
sources: [Tsay - Analysis of Financial Time Series (3rd ed.) ch 3, Engle (1982) - Autoregressive Conditional Heteroscedasticity - Econometrica 50(4), Bollerslev (1986) - Generalized Autoregressive Conditional Heteroskedasticity - Journal of Econometrics 31(3), J.P. Morgan and Reuters (1996) - RiskMetrics Technical Document (4th ed.), Glosten Jagannathan and Runkle (1993) - Journal of Finance 48(5), Nelson (1991) - Conditional Heteroskedasticity in Asset Returns - Econometrica 59(2), Parkinson (1980) - The Extreme Value Method for Estimating the Variance of the Rate of Return - Journal of Business 53(1), Garman and Klass (1980) - On the Estimation of Security Price Volatilities from Historical Data - Journal of Business 53(1), Andersen Bollerslev Diebold and Labys (2003) - Modeling and Forecasting Realized Volatility - Econometrica 71(2), Zhang Mykland and Ait-Sahalia (2005) - A Tale of Two Time Scales - JASA 100(472), Patton (2011) - Volatility Forecast Comparison Using Imperfect Volatility Proxies - Journal of Econometrics 160(1)]
---

# Volatility Models: EWMA and GARCH

## TL;DR

- Returns are close to uncorrelated but their squares are strongly and persistently autocorrelated: volatility clusters, and conditional variance is forecastable even when the mean is not.
- EWMA: $\sigma_t^2 = \lambda\sigma_{t-1}^2 + (1-\lambda)r_{t-1}^2$ (RiskMetrics daily $\lambda = 0.94$, half-life 11.2 days); it has no long-run level, so its forecast term structure is flat.
- GARCH(1,1): $\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta\sigma_{t-1}^2$; persistence $\alpha+\beta$, long-run variance $\omega/(1-\alpha-\beta)$, shock half-life $\ln 0.5/\ln(\alpha+\beta)$, and forecasts revert geometrically to the long-run level.
- The leverage effect (negative returns raise future volatility more than positive ones) is captured by GJR-GARCH or EGARCH.
- Range estimators (Parkinson, Garman-Klass) are 5 to 7 times more efficient than close-to-close; realized variance from intraday returns is better still until microstructure noise, which biases it by $2n\,\text{Var}(\text{noise})$, dominates.
- Judge variance forecasts with MSE or QLIKE on a noisy proxy; both rank forecasts correctly, MAE on volatility does not.

## Learning objectives

- Estimate volatility with EWMA and GARCH(1,1) and interpret persistence.
- Use realized volatility estimators (close-to-close, Parkinson, Garman-Klass, realized variance).
- Explain volatility clustering and the leverage effect.

## Core concepts

### Stylised facts

- Volatility clustering: large moves follow large moves; the ACF of $r_t^2$ or $|r_t|$ is positive and decays slowly.
- Fat tails: unconditional kurtosis well above 3, partly explained by time-varying variance (a mixture of normals is fat-tailed).
- Mean reversion of volatility: high-vol regimes decay toward a long-run level; implied vol term structures slope toward it.
- Leverage effect: returns are negatively correlated with future volatility, strongest in equity indices.

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
- $\alpha$ is the reaction to news, $\beta$ is memory; typical daily equity fits have $\alpha \approx 0.05$ to $0.10$ and $\alpha + \beta \approx 0.97$ to $0.99$.
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
- The leverage story (falling equity raises financial leverage) explains only part of it; volatility feedback (rising risk premia push prices down) is the other explanation.

### Realized and range-based estimators

Per-day variance estimators, with $O,H,L,C$ the open, high, low and close:

| Estimator | Formula | Efficiency vs close-to-close |
| :--- | :--- | :--- |
| Close-to-close | $\frac{1}{n-1}\sum (r_i - \bar r)^2$ | 1 |
| Parkinson (1980) | $\frac{1}{4\ln 2}\,[\ln(H/L)]^2$ | about 5.2 |
| Garman-Klass (1980) | $\tfrac12[\ln(H/L)]^2 - (2\ln2-1)[\ln(C/O)]^2$ | about 7.4 |
| Rogers-Satchell | $\ln\frac HC\ln\frac HO + \ln\frac LC\ln\frac LO$ | drift-robust |

Efficiency means variance ratio: Parkinson over 20 days is roughly as precise as close-to-close over 100.
Range estimators ignore the overnight gap (add it separately, as Yang-Zhang does) and are biased down by discrete sampling of the path.

Realized variance $RV_t = \sum_{i=1}^n r_{t,i}^2$ over intraday returns converges to integrated variance as $n \to \infty$ in a frictionless market (Andersen, Bollerslev, Diebold and Labys 2003).
With iid microstructure noise of variance $\omega^2$ on observed log prices, $E[RV] = IV + 2n\omega^2$: sampling faster makes the estimate worse.
Remedies are sparse sampling (5 minutes), the two-scales estimator of Zhang, Mykland and Ait-Sahalia (2005), and realized kernels; the volatility signature plot (mean RV against sampling interval) diagnoses the noise.

### Evaluating forecasts

The true variance is unobserved, so forecasts $h_t$ are scored against a noisy proxy $\hat\sigma_t^2$ such as $r_t^2$ or RV.
Patton (2011) shows MSE $(\hat\sigma^2 - h)^2$ and QLIKE $\hat\sigma^2/h - \ln(\hat\sigma^2/h) - 1$ give the same ranking as with the true variance; MAE and MSE on volatility (not variance) do not.
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

```python
import numpy as np
from scipy.optimize import minimize

def garch_filter(r, omega, alpha, beta):
    s2 = np.empty_like(r)
    s2[0] = r.var()                          # initialise at the sample variance
    for t in range(1, len(r)):
        s2[t] = omega + alpha * r[t - 1] ** 2 + beta * s2[t - 1]
    return s2

def neg_loglik(theta, r):
    omega, alpha, beta = theta
    if omega <= 0 or alpha < 0 or beta < 0 or alpha + beta >= 1:
        return np.inf
    s2 = garch_filter(r, omega, alpha, beta)
    return 0.5 * np.sum(np.log(s2) + r**2 / s2)   # Gaussian, constants dropped

rng = np.random.default_rng(1)
T, (omega, alpha, beta) = 5000, (2e-6, 0.08, 0.90)
r, s2 = np.empty(T), omega / (1 - alpha - beta)
for t in range(T):
    r[t] = np.sqrt(s2) * rng.standard_normal()
    s2 = omega + alpha * r[t] ** 2 + beta * s2

fit = minimize(neg_loglik, x0=[r.var() * 0.05, 0.05, 0.90], args=(r,), method="Nelder-Mead",
               options={"xatol": 1e-10, "fatol": 1e-10, "maxiter": 5000})
w, a, b = fit.x
print(w, a, b, a + b, np.sqrt(252 * w / (1 - a - b)))
# about 2.13e-06 0.084 0.895 0.979 0.160
```

On 20 years of simulated daily data the fit recovers persistence 0.979 against a true 0.98 and long-run vol 16.0% against 15.9%.

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
> The range uses the whole intraday path, giving about 5 times the efficiency of squared close-to-close returns for a driftless Brownian motion.

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

## Further reading

- Ruey Tsay, *Analysis of Financial Time Series*, chapter 3.
- Robert Engle (1982), Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation, Econometrica.
- Tim Bollerslev (1986), Generalized Autoregressive Conditional Heteroskedasticity, Journal of Econometrics.
- J.P. Morgan and Reuters (1996), RiskMetrics Technical Document.
- Glosten, Jagannathan and Runkle (1993), On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks, Journal of Finance.
- Parkinson (1980) and Garman and Klass (1980), Journal of Business.
- Andersen, Bollerslev, Diebold and Labys (2003), Modeling and Forecasting Realized Volatility, Econometrica.
- Patton (2011), Volatility Forecast Comparison Using Imperfect Volatility Proxies, Journal of Econometrics.
- Related notes: [Variance Swaps and Volatility Products](../05-Derivatives-and-Volatility/14-Variance-Swaps-and-Volatility-Products.md), [VaR and Expected Shortfall](../11-Risk-and-Trading/03-VaR-and-Expected-Shortfall.md), [Heavy Tails and Extreme Value Theory](13-Heavy-Tails-and-Extreme-Value-Theory.md).
