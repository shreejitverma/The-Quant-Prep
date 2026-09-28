---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [linear-regression-ols]
est_hours: 5
sources: [Tsay - Analysis of Financial Time Series (3rd ed.) ch 2, Hamilton - Time Series Analysis (1994) ch 3 4 17, Box Jenkins Reinsel and Ljung - Time Series Analysis - Forecasting and Control, Dickey and Fuller (1979) - Distribution of the Estimators for Autoregressive Time Series with a Unit Root - JASA 74(366), Kwiatkowski Phillips Schmidt and Shin (1992) - Testing the Null Hypothesis of Stationarity - Journal of Econometrics 54, Ljung and Box (1978) - On a Measure of Lack of Fit in Time Series Models - Biometrika 65(2), Roll (1984) - A Simple Implicit Measure of the Effective Bid-Ask Spread - Journal of Finance 39(4), Granger and Newbold (1974) - Spurious Regressions in Econometrics - Journal of Econometrics 2]
---

# Time Series: Stationarity and ARMA

## TL;DR

- Weak stationarity means constant mean, constant finite variance and autocovariances that depend only on the lag; prices are not stationary, returns and well-built spreads usually are.
- AR(1) $x_t = c + \phi x_{t-1} + \varepsilon_t$ is stationary iff $|\phi| < 1$, with mean $c/(1-\phi)$, variance $\sigma^2/(1-\phi^2)$, ACF $\phi^k$ and half-life $\ln 0.5/\ln\phi$.
- Identification: AR($p$) has a PACF that cuts off after lag $p$ and a decaying ACF; MA($q$) has an ACF that cuts off after lag $q$ and a decaying PACF; ARMA has both decaying.
- Unit-root tests regress $\Delta x_t$ on $x_{t-1}$; the $t$-stat has the Dickey-Fuller distribution (5% critical value $-2.86$ with a constant), and the test has low power for $\phi$ near 1 over short samples.
- ADF and KPSS have opposite nulls (unit root versus stationarity); use both, and remember that failing to reject is not evidence for the null.
- Bid-ask bounce makes observed price changes a negative MA(1); Roll's estimator is $s = 2\sqrt{-\text{Cov}(\Delta p_t, \Delta p_{t-1})}$.

## Learning objectives

- Define weak stationarity and test for unit roots (ADF, KPSS).
- Identify AR and MA structure from ACF and PACF.
- Fit and forecast ARMA models and explain their mean reversion horizon.

## Core concepts

### Stationarity

A process is strictly stationary if the joint law of $(x_{t_1+h},\dots,x_{t_k+h})$ does not depend on $h$.
It is weakly (covariance) stationary if $E[x_t] = \mu$, $\text{Var}(x_t) = \gamma_0 < \infty$ and $\text{Cov}(x_t, x_{t-k}) = \gamma_k$ for all $t$.
The autocorrelation function is $\rho_k = \gamma_k/\gamma_0$.
A random walk $p_t = p_{t-1} + \varepsilon_t$ is not stationary: $\text{Var}(p_t) = t\sigma^2$ grows without bound and shocks never decay.
It is integrated of order one, I(1): its first difference is stationary.
Regressing one I(1) series on another independent I(1) series gives spuriously significant $t$-stats and high $R^2$ (Granger and Newbold 1974), which is why price levels are never regressed on each other without a cointegration argument ([Cointegration and VAR](10-Cointegration-and-VAR.md)).

### AR, MA and ARMA

- AR($p$): $x_t = c + \sum_{i=1}^p \phi_i x_{t-i} + \varepsilon_t$, stationary iff all roots of $1 - \phi_1 z - \dots - \phi_p z^p$ lie outside the unit circle.
  For AR(2) this is $\phi_1 + \phi_2 < 1$, $\phi_2 - \phi_1 < 1$, $|\phi_2| < 1$.
- MA($q$): $x_t = \mu + \varepsilon_t + \sum_{j=1}^q \theta_j \varepsilon_{t-j}$, always stationary; invertible (expressible as a convergent AR($\infty$)) iff the roots of $1 + \theta_1 z + \dots + \theta_q z^q$ lie outside the unit circle.
- ARMA($p,q$) combines both and is parsimonious: a low-order ARMA often replaces a long AR.

AR(1) facts, derived by taking expectations and variances of both sides under stationarity:

$$
\mu = \frac{c}{1-\phi}, \qquad \gamma_0 = \frac{\sigma^2}{1-\phi^2}, \qquad \rho_k = \phi^k, \qquad \text{half-life} = \frac{\ln 0.5}{\ln \phi}.
$$

The AR(1) is the discrete-time Ornstein-Uhlenbeck process: with mean-reversion speed $\kappa$ and step $\Delta t$, $\phi = e^{-\kappa\Delta t}$.

MA(1) facts: $\gamma_0 = (1+\theta^2)\sigma^2$, $\rho_1 = \theta/(1+\theta^2)$, $\rho_k = 0$ for $k \ge 2$.
Since $|\theta/(1+\theta^2)| \le 1/2$, an MA(1) can never produce $|\rho_1| > 0.5$, and $\theta$ and $1/\theta$ give the same ACF; pick the invertible root $|\theta| < 1$.

For AR($p$), the Yule-Walker equations $\rho_k = \sum_i \phi_i \rho_{k-i}$ give the ACF from the coefficients and, inverted, method-of-moments estimates of the coefficients.

### Identification with ACF and PACF

The partial autocorrelation at lag $k$ is the last coefficient in a regression of $x_t$ on $x_{t-1},\dots,x_{t-k}$.

| Model | ACF | PACF |
| :--- | :--- | :--- |
| AR($p$) | Decays geometrically or as a damped sine | Cuts off after lag $p$ |
| MA($q$) | Cuts off after lag $q$ | Decays |
| ARMA($p,q$) | Decays after lag $q$ | Decays after lag $p$ |

Under white noise, sample autocorrelations are approximately $N(0, 1/T)$, so the Bartlett bands are $\pm 1.96/\sqrt T$.
To test many lags jointly use Ljung-Box, $Q(m) = T(T+2)\sum_{k=1}^m \hat\rho_k^2/(T-k) \sim \chi^2_m$ under white noise (use $m - p - q$ degrees of freedom on ARMA residuals).
Choose orders by AIC or BIC and then check that residuals are white; BIC penalises parameters by $\ln T$ and picks smaller models.

### Estimation and forecasting

AR models are fit by OLS of $x_t$ on its lags, which is conditional MLE under Gaussian errors; MA and ARMA need nonlinear MLE because $\varepsilon_t$ is not observed.
The OLS estimate of $\phi$ is biased downward in small samples, roughly $E[\hat\phi] - \phi \approx -(1+3\phi)/T$ with an estimated mean (Kendall), which biases estimated half-lives short.
The AR(1) $h$-step forecast and its error variance are

$$
E_t[x_{t+h}] = \mu + \phi^h (x_t - \mu), \qquad \text{Var}_t(x_{t+h}) = \sigma^2 \frac{1 - \phi^{2h}}{1-\phi^2}.
$$

The forecast decays to the mean at the rate $\phi^h$, and the error variance rises to the unconditional variance.
An MA($q$) forecast reverts to $\mu$ after $q$ steps.

### Unit-root and stationarity tests

Rewrite the AR(1) as $\Delta x_t = \alpha + \gamma x_{t-1} + \varepsilon_t$ with $\gamma = \phi - 1$.
The Dickey-Fuller test is the $t$-stat on $\hat\gamma$ for $H_0: \gamma = 0$ (unit root) against $\gamma < 0$.
Under the null the statistic is not Student-$t$: its asymptotic 5% critical values are $-1.95$ (no constant), $-2.86$ (constant) and $-3.41$ (constant and trend); 1% values are $-2.58$, $-3.43$, $-3.96$.
The augmented DF test adds lagged $\Delta x_{t-i}$ to whiten the residuals, with lag length chosen by AIC or a rule such as $\lfloor 12 (T/100)^{1/4} \rfloor$.
KPSS reverses the null: $H_0$ is (level or trend) stationarity, tested with a statistic built from partial sums of residuals.

| ADF | KPSS | Reading |
| :--- | :--- | :--- |
| Reject | Do not reject | Stationary |
| Do not reject | Reject | Unit root |
| Do not reject | Do not reject | Data too short to tell |
| Reject | Reject | Possible structural break or fractional integration |

Finance framing: a pairs spread with daily $\phi = 0.98$ (half-life 34 days) is tradable but hard to distinguish from a random walk with one year of data.

## Worked examples

### 1. Half-life and forecast of a mean-reverting spread

A spread follows AR(1) with daily $\phi = 0.95$, $\sigma_\varepsilon = 0.10$, and is currently 0.8 above its mean.

- Half-life: $\ln 0.5 / \ln 0.95 = 13.5$ trading days.
- Stationary standard deviation: $0.10/\sqrt{1 - 0.9025} = 0.320$, so the spread is $0.8/0.32 = 2.5$ standard deviations rich.
- Five-day forecast deviation: $0.8 \times 0.95^5 = 0.619$, with forecast error sd $0.10\sqrt{(1-0.95^{10})/(1-0.95^2)} = 0.203$.
- OU speed: $\kappa = -\ln 0.95 \times 252 = 12.9$ per year.

The expected five-day move of $-0.181$ is less than one forecast standard deviation, which is why single mean-reversion trades have low hit rates and the edge comes from repetition.

### 2. MA(1) from an ACF, and the Roll spread

The ACF of a return series is $\hat\rho_1 = -0.4$ and insignificant afterwards: this is MA(1).
Solve $\theta/(1+\theta^2) = -0.4$: $0.4\theta^2 + \theta + 0.4 = 0$, so $\theta = -0.5$ or $\theta = -2$; the invertible choice is $\theta = -0.5$.

Roll (1984) models the observed price as the efficient price plus $\pm s/2$ bid-ask bounce with independent trade signs.
Then $\text{Cov}(\Delta p_t, \Delta p_{t-1}) = -s^2/4$, a negative MA(1) signature.
If the first-order autocovariance of trade-to-trade price changes is $-0.0004$ dollars squared, $s = 2\sqrt{0.0004} = \$0.04$.
Details are in [Spread Models: Roll and Glosten-Milgrom](../07-Market-Microstructure/03-Spread-Models-Roll-and-Glosten-Milgrom.md).

### 3. AR(2) ACF by Yule-Walker

$x_t = 0.5x_{t-1} + 0.3x_{t-2} + \varepsilon_t$.

- Stationary: $\phi_1+\phi_2 = 0.8 < 1$, $\phi_2 - \phi_1 = -0.2 < 1$, $|\phi_2| < 1$ (characteristic roots have moduli 1.17 and 2.84).
- $\rho_1 = \phi_1/(1-\phi_2) = 0.5/0.7 = 0.714$, $\rho_2 = \phi_1\rho_1 + \phi_2 = 0.657$, $\rho_3 = \phi_1\rho_2+\phi_2\rho_1 = 0.543$.
- PACF: lag 2 is $(\rho_2 - \rho_1^2)/(1-\rho_1^2) = 0.3 = \phi_2$, and zero beyond lag 2.

### 4. Dickey-Fuller by hand, and its power

A spread regression gives $\Delta x_t = 0.001 - 0.02\,x_{t-1}$, with standard error 0.009 on the slope, over $T = 250$ days.

- $t = -0.02/0.009 = -2.22$, above the $-2.86$ critical value: do not reject the unit root.
- Yet the point estimate is $\phi = 0.98$, a half-life of 34 days.
- Using the Student-$t$ critical value $-1.65$ would have wrongly rejected.

Simulating AR(1) with a constant (4000 paths each) shows how weak the test is: at $\phi = 0.98$ it rejects 12% of the time with $T = 250$ and 87% with $T = 1000$; at $\phi = 0.95$, $T = 250$, 48%.
Under a true unit root it rejects 5.2% of the time, confirming the critical value.
Conclusion: "ADF did not reject" on one year of data says almost nothing about a slow spread.

### 5. Ljung-Box on a return series

$T = 500$, $\hat\rho_1 = 0.08$, $\hat\rho_2 = -0.05$, $\hat\rho_3 = 0.06$.
$Q(3) = 500 \times 502 \times (0.0064/499 + 0.0025/498 + 0.0036/497) = 6.30$, below $\chi^2_{3,0.95} = 7.81$, $p = 0.098$.
Individually, $\hat\rho_1 = 0.08$ is inside the Bartlett band $\pm 1.96/\sqrt{500} = \pm 0.088$, consistent with the joint result.

### 6. Estimation noise in the half-life

```python
import numpy as np

def fit_ar1(x):
    """OLS of x_t on [1, x_{t-1}]; returns c, phi, residual sd, half-life."""
    X = np.column_stack([np.ones(len(x) - 1), x[:-1]])
    (c, phi), *_ = np.linalg.lstsq(X, x[1:], rcond=None)
    resid = x[1:] - X @ np.array([c, phi])
    return c, phi, resid.std(ddof=2), np.log(0.5) / np.log(phi)

def df_tstat(x):
    """Dickey-Fuller t-stat (constant, no lags): regress dx_t on [1, x_{t-1}]."""
    dx, X = np.diff(x), np.column_stack([np.ones(len(x) - 1), x[:-1]])
    b, *_ = np.linalg.lstsq(X, dx, rcond=None)
    e = dx - X @ b
    cov = (e @ e / (len(dx) - 2)) * np.linalg.inv(X.T @ X)
    return b[1] / np.sqrt(cov[1, 1])   # compare with -2.86 (5%), not -1.645

rng = np.random.default_rng(7)
x = np.full(1000, 1.0)            # start at the mean c/(1-phi) = 1
for t in range(1, 1000):
    x[t] = 0.05 + 0.95 * x[t - 1] + 0.1 * rng.standard_normal()
print(fit_ar1(x), df_tstat(x))    # phi 0.963, half-life 18.2, DF t -4.34
```

The true half-life is 13.5 days, but this path estimates 18.2.
With $T = 1000$ the standard error of $\hat\phi$ is $\sqrt{(1-\phi^2)/T} = 0.0099$, and $\phi \pm 2$ se $= [0.930, 0.970]$ maps to half-lives of 9.6 to 22.5 days.
Report half-lives with intervals; the map $\phi \mapsto \ln 0.5/\ln\phi$ explodes as $\phi \to 1$.

## Pitfalls

- Using Student-$t$ or normal critical values for a unit-root test.
- Treating "fail to reject a unit root" as proof of a random walk, or "fail to reject stationarity" in KPSS as proof of stationarity; both tests have low power in short samples.
- Regressing price levels on price levels and trusting the $t$-stats (spurious regression).
- Fitting ARMA to prices instead of returns, or differencing a series that is already stationary (over-differencing creates an MA unit root, $\rho_1 = -0.5$).
- Reading the ACF of returns without a volatility model: squared returns are strongly autocorrelated even when returns are not ([Volatility Models](09-Volatility-Models-GARCH.md)), and heteroskedasticity makes Bartlett bands too narrow.
- Estimating half-life from one sample and trading it as known; the downward bias of $\hat\phi$ and the convexity of the half-life both matter.
- Ignoring structural breaks: a level shift in a stationary series looks like a unit root to ADF.

## Interview questions

> [!question]- stat-arma-weak-stationarity | Define weak stationarity.
> Constant mean, constant finite variance, and autocovariance $\text{Cov}(x_t, x_{t-k})$ that depends only on the lag $k$.
> Strict stationarity requires the whole joint distribution to be shift-invariant; the two coincide for Gaussian processes.

> [!question]- stat-arma-ar1-moments | For $x_t = c + \phi x_{t-1} + \varepsilon_t$ with $|\phi|<1$, give the mean, variance and ACF.
> Mean $c/(1-\phi)$, variance $\sigma^2/(1-\phi^2)$, $\rho_k = \phi^k$.
> Take expectations and variances of both sides and use stationarity: $\mu = c + \phi\mu$ and $\gamma_0 = \phi^2\gamma_0 + \sigma^2$.

> [!question]- stat-arma-half-life | A daily AR(1) spread has $\phi = 0.95$. What is its half-life?
> About 13.5 days.
> The expected deviation decays as $\phi^h$; solve $0.95^h = 0.5$: $h = \ln 0.5/\ln 0.95 = 13.5$.

> [!question]- stat-arma-acf-pacf-signature | How do you tell AR($p$) from MA($q$) using the ACF and PACF?
> AR($p$): PACF cuts off after lag $p$, ACF decays; MA($q$): ACF cuts off after lag $q$, PACF decays.
> ARMA has both decaying, and orders are then chosen by AIC or BIC with a residual whiteness check.

> [!question]- stat-arma-ma1-max-rho | What is the largest lag-1 autocorrelation an MA(1) can have?
> $0.5$ in absolute value, at $\theta = \pm 1$.
> $\rho_1 = \theta/(1+\theta^2)$ and $1+\theta^2 \ge 2|\theta|$; a sample $\hat\rho_1$ of 0.7 with nothing after needs a different model.

> [!question]- stat-arma-df-critical-value | Why can you not use $-1.65$ as the critical value in a Dickey-Fuller test?
> Under the unit-root null the $t$-stat on $x_{t-1}$ does not have a $t$ distribution; its 5% critical value with a constant is about $-2.86$.
> The regressor $x_{t-1}$ is nonstationary under the null, so the limit is a functional of Brownian motion skewed to the left.

> [!question]- stat-arma-adf-vs-kpss | What are the null hypotheses of ADF and KPSS, and why run both?
> ADF: unit root; KPSS: stationarity.
> Each has low power, so agreement is informative, both failing to reject means the sample is too short, and both rejecting suggests breaks or fractional integration.

> [!question]- stat-arma-df-power | A spread has true daily $\phi = 0.98$. How often does a 5% ADF test reject the unit root with one year of data?
> Only about 12% of the time (simulation, $T = 250$, constant included).
> The alternative is very close to the null; with four years the rejection rate rises to about 87%.

> [!question]- stat-arma-ar1-forecast | AR(1) with $\phi = 0.95$, mean 0, currently at 0.8. What is the 5-step forecast?
> $0.8 \times 0.95^5 = 0.62$.
> $E_t[x_{t+h}] = \mu + \phi^h(x_t - \mu)$, and the forecast error variance is $\sigma^2(1-\phi^{2h})/(1-\phi^2)$.

> [!question]- stat-arma-roll-spread | Trade-to-trade price changes have lag-1 autocovariance $-0.0004$. What spread does the Roll model imply?
> 4 cents.
> Bid-ask bounce gives $\text{Cov}(\Delta p_t,\Delta p_{t-1}) = -s^2/4$, so $s = 2\sqrt{0.0004} = 0.04$.

> [!question]- stat-arma-spurious-regression | You regress one stock's price on another's over ten years and get $R^2 = 0.8$ and $t = 25$. What is wrong?
> Probably a spurious regression between two I(1) series; the $t$-stat is meaningless.
> Test the residual for a unit root (Engle-Granger) or regress returns on returns instead.

> [!question]- stat-arma-ljung-box | State the Ljung-Box statistic and its null distribution.
> $Q(m) = T(T+2)\sum_{k=1}^m \hat\rho_k^2/(T-k)$, approximately $\chi^2_m$ under white noise.
> Use $m-p-q$ degrees of freedom when applied to ARMA($p,q$) residuals.

> [!question]- stat-arma-ou-mapping | How does a discrete AR(1) coefficient relate to the OU mean-reversion speed $\kappa$?
> $\phi = e^{-\kappa \Delta t}$, so $\kappa = -\ln\phi/\Delta t$.
> Daily $\phi = 0.95$ gives $\kappa = 12.9$ per year and a half-life of $\ln 2/\kappa$ years.

> [!question]- stat-arma-overdifferencing | What happens to the ACF if you difference a series that is already white noise?
> The result is an MA(1) with $\theta = -1$ and $\rho_1 = -0.5$.
> $\Delta\varepsilon_t = \varepsilon_t - \varepsilon_{t-1}$ is non-invertible, a sign of over-differencing.

## Further reading

- Ruey Tsay, *Analysis of Financial Time Series*, chapter 2.
- James Hamilton, *Time Series Analysis*, chapters 3, 4 and 17.
- Box, Jenkins, Reinsel and Ljung, *Time Series Analysis: Forecasting and Control*.
- Dickey and Fuller (1979), Distribution of the Estimators for Autoregressive Time Series with a Unit Root, JASA.
- Kwiatkowski, Phillips, Schmidt and Shin (1992), Testing the Null Hypothesis of Stationarity against the Alternative of a Unit Root, Journal of Econometrics.
- Roll (1984), A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market, Journal of Finance.
- Granger and Newbold (1974), Spurious Regressions in Econometrics, Journal of Econometrics.
