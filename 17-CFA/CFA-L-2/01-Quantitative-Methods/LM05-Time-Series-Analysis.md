---
type: cfa-lm
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
volume: 1
lm: 5
title: "Time-Series Analysis"
pages: "109-196"
weight_band: "5-10%"
difficulty: 4
los_count: 15
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/quantitative-methods]
---

# LM5: Time-Series Analysis

Difficulty 4 of 5: fifteen LOS, a dozen distinct formulas, and a decision tree the examiner walks you through one exhibit at a time; the arithmetic is light but every step has a trap (which lag, which sign, which critical value, which test is even valid).

## LOS map

- **calculate** and evaluate the predicted trend value for a time series, modeled as either a linear trend or a log-linear trend, given the estimated trend coefficients (V1 p.113) ^los-01-05-a
    - Examiner asks: given $\hat{b}_0$, $\hat{b}_1$ and the sample length $T$, compute $\hat{y}$ for an out-of-sample month ($t = T + k$), remembering to exponentiate for the log-linear model.
- **describe** factors that determine whether a linear or a log-linear trend should be used with a particular time series and evaluate limitations of trend models (V1 p.116) ^los-01-05-b
    - Examiner asks: constant amount of growth versus constant rate of growth, and reading a Durbin-Watson statistic below $d_l$ as positive serial correlation that invalidates the trend model.
- **explain** the requirement for a time series to be covariance stationary and describe the significance of a series that is not stationary (V1 p.122) ^los-01-05-c
    - Examiner asks: state the three conditions (constant finite mean, constant finite variance, constant finite autocovariance at each lag) and judge a plot or an analyst's "conclusion" against them.
- **describe** the structure of an autoregressive (AR) model of order p and calculate one- and two-period-ahead forecasts given the estimated coefficients (V1 p.124) ^los-01-05-d
    - Examiner asks: plug the most recent value(s) into an AR(1) or AR(2) and chain the one-period forecast into the two-period forecast.
- **explain** how autocorrelations of the residuals can be used to test whether the autoregressive model fits the time series (V1 p.124) ^los-01-05-e
    - Examiner asks: compute $1/\sqrt{T}$, divide each residual autocorrelation by it, compare with the t critical value, and say whether the model is misspecified (and that Durbin-Watson is invalid here).
- **explain** mean reversion and calculate a mean-reverting level (V1 p.127) ^los-01-05-f
    - Examiner asks: $b_0/(1-b_1)$, then whether the next forecast is above or below the current value.
- **contrast** in-sample and out-of-sample forecasts and compare the forecasting accuracy of different time-series models based on the root mean squared error criterion (V1 p.131) ^los-01-05-g
    - Examiner asks: compute RMSE from a short table of out-of-sample errors and pick the model with the smaller RMSE, or reject a model comparison made on in-sample $R^2$.
- **explain** the instability of coefficients of time-series models (V1 p.134) ^los-01-05-h
    - Examiner asks: why a model estimated on a longer sample that spans a regime change can be wrong even if its residuals look clean, and the trade-off of short versus long samples.
- **describe** characteristics of random walk processes and contrast them to covariance stationary processes (V1 p.136) ^los-01-05-i
    - Examiner asks: $b_0 = 0$, $b_1 = 1$, undefined mean-reverting level, variance growing with $t$, best forecast equals the current value, and which of an analyst's statements is consistent with both a random walk and stationarity.
- **describe** implications of unit roots for time-series analysis, explain when unit roots are likely to occur and how to test for them, and demonstrate how a time series with a unit root can be transformed so it can be analyzed with an AR model (V1 p.140) ^los-01-05-j
    - Examiner asks: why a t-test of $b_1 = 1$ is invalid, that first-differencing removes a single unit root, and reading a differenced regression whose coefficients are all insignificant as evidence the original series was a random walk.
- **describe** the steps of the unit root test for nonstationarity and explain the relation of the test to autoregressive time-series models (V1 p.140) ^los-01-05-k
    - Examiner asks: subtract $x_{t-1}$ from both sides, test $H_0: g_1 = 0$ against $H_a: g_1 < 0$ with Dickey-Fuller critical values; the trap is "add a lag" or "change the independent variable".
- **explain** how to test and correct for seasonality in a time-series model and calculate and interpret a forecasted value using an AR model with a seasonal lag (V1 p.149) ^los-01-05-l
    - Examiner asks: spot the significant fourth (quarterly) or twelfth (monthly) residual autocorrelation, add $x_{t-4}$ or $x_{t-12}$, and forecast next quarter's sales in dollars from a log-differenced seasonal model.
- **explain** autoregressive conditional heteroskedasticity (ARCH) and describe how ARCH models can be applied to predict the variance of a time series (V1 p.155) ^los-01-05-m
    - Examiner asks: the test regression $\hat{\varepsilon}_t^2 = a_0 + a_1 \hat{\varepsilon}_{t-1}^2 + u_t$, what a significant $a_1$ implies for the standard errors, and the next-period variance $\hat{a}_0 + \hat{a}_1 \hat{\varepsilon}_t^2$.
- **explain** how time-series variables should be analyzed for nonstationarity and/or cointegration before use in a linear regression (V1 p.159) ^los-01-05-n
    - Examiner asks: the five scenarios (neither has a unit root, one has, both have and are or are not cointegrated) and the Engle-Granger residual test, then which company's regression on oil prices is valid.
- **determine** an appropriate time-series model to analyze a given investment problem and justify that choice (V1 p.163) ^los-01-05-o
    - Examiner asks: from a description (exponential trend, serially correlated trend residuals, no unit root, seasonality) pick the transformation and model, for example "first-differenced log AR(1)".

## Core intuition

> [!abstract] The whole module in one sentence
> Time-series modelling is the repeated act of transforming a series until it is covariance stationary, fitting the shortest autoregression whose residuals show no autocorrelation at any lag (including the seasonal one), checking the residual variance is not itself autoregressive, and only then forecasting (V1 p.164, p.165).

### Why time series break ordinary regression

A time series is the same variable observed in successive periods, so the "independent variable" in the natural model $x_t = b_0 + b_1 x_{t-1} + \varepsilon_t$ is a lagged copy of the dependent variable (V1 p.112).
That single fact is the source of every complication in this module.
In a cross-sectional regression, serially correlated errors leave the coefficient estimates consistent and only distort the standard errors; in an autoregression, serially correlated errors make $\hat{b}_0$ and $\hat{b}_1$ themselves inconsistent (V1 p.112).
And if the mean or variance of the series drifts over time, regression results on that series have no economic meaning at all (V1 p.113, p.123).
So the analyst has two jobs before any forecast: make the series stationary, and make the residuals white noise.
The observations must also be processed in chronological order; scrambling a CPI series destroys the time patterns the model is supposed to capture (V1 p.122).

### Trends: constant amount versus constant rate

The simplest forecast is a trend.
A linear trend, $y_t = b_0 + b_1 t + \varepsilon_t$, says the series grows by the same amount $b_1$ every period regardless of its current level: if $\hat{b}_0 = 5.1$ and $\hat{b}_1 = 2$ the fitted values at $t = 5$ and $t = 6$ are 15.1 and 17.1 (V1 p.113, p.114).
A log-linear trend, $\ln y_t = b_0 + b_1 t + \varepsilon_t$, says the series grows by the same proportion every period, because $y_{t+1}/y_t = e^{b_1}$ and so the growth rate is $e^{b_1} - 1$, a constant (V1 p.116, p.117).
Exponential growth is just compound growth with continuous compounding, and taking logs turns it into something linear regression can estimate (V1 p.117).
The choice between them is a choice about the data-generating process: financial series that compound (sales, prices, index levels) usually want the log-linear form, while a series that moves in level terms without compounding, like an inflation rate, can take the linear form (V1 p.166).
The tell is in the residuals rather than the $R^2$: Starbucks' sales gave a linear trend an $R^2$ of 0.96, but the residuals sat persistently below the line before 2008 and above it afterwards, which is serial correlation and disqualifies the model (V1 p.118, p.119).
Both trend models have one independent variable and one Durbin-Watson test, and both trends in the curriculum fail it: DW of 1.2145 for CPI inflation against $d_l$ above 1.77, and DW of 0.26 for log Starbucks sales against $d_l$ above 1.60 (V1 p.122).
The conclusion is not "trend models are useless" but "the serial correlation they leave behind is information we can use to build a better model" (V1 p.122).

### Covariance stationarity: the licence to run an autoregression

An autoregression regresses the series on its own past.
Because the regressor is random, ordinary least squares gives valid inference only if the series is covariance stationary: constant finite expected value, constant finite variance, and constant finite covariance with itself at each fixed lag (V1 p.123).
The third condition at lag zero is the second condition, which is why the curriculum writes the last two together as $\text{cov}(y_t, y_{t-s}) = \lambda_s$ (V1 p.123).
Break stationarity and the estimate of $b_1$ is biased and every hypothesis test is invalid (V1 p.123).
A plot is the first diagnostic: roughly constant mean and variance and no visible seasonality (V1 p.123).
Any series a trend model fits well is by construction not stationary, because its mean rises with $t$; seasonal series are not stationary because the December mean differs from the January mean; random walks are not stationary because their variance grows without bound (V1 p.124, p.137).
Stationarity in the past does not guarantee stationarity in the future; a regime change can invalidate a model that was correctly specified on its sample (V1 p.124).

> [!abstract] Mean reversion is what stationarity buys you
> A covariance-stationary AR(1) has a finite level $b_0/(1 - b_1)$ at which the forecast equals the current value; above it the series is forecast to fall, below it to rise, and every multi-period forecast slides toward it (V1 p.128).
> A random walk has $b_1 = 1$, so the level is $0/0$: undefined, which is the same statement as "no mean reversion, variance grows with $t$, best forecast is today's value" (V1 p.137).

### Fitting an AR(p): the residual autocorrelation test

The Durbin-Watson statistic is invalid whenever a lagged dependent variable is a regressor, which is every AR model, so the curriculum replaces it with a direct test on residual autocorrelations (V1 p.124).
The logic is a three-step loop: estimate AR(1), compute the residual autocorrelations, test each against zero with standard error $1/\sqrt{T}$ (V1 p.125).
If any lag is significant the model is misspecified; add a lag and repeat until none is (V1 p.126, p.130).
Intel's gross margin passed at AR(1) with 65 observations and a standard error of 0.1240, no residual t-statistic above 1.68 in absolute value (V1 p.126, p.127).
US CPI inflation failed at AR(1) because the second lag had a t-statistic of $-2.80$ against 1.97, and passed at AR(2) (V1 p.130, p.131).
A well-specified model then forecasts one period ahead by plugging in the current value, and two periods ahead by the chain rule: substitute the one-period forecast back into the equation (V1 p.128).
Each link in the chain adds uncertainty, which is why the two-period forecast has a larger variance than the one-period forecast and long-horizon forecasts from short-horizon models become implausible (V1 p.128, p.192).

### Judging forecast quality: out of sample, by RMSE

In-sample errors are residuals; they describe fit, not forecasting power (V1 p.132).
The future is always out of sample, so models are ranked on out-of-sample root mean squared error, the square root of the average squared forecast error, smallest wins (V1 p.132).
For CPI inflation the AR(2) model had the smaller standard error in sample (2.9208 versus 2.9687) and the smaller RMSE out of sample (1.4157 versus 1.9014, a ratio of 74.46%), so it won on both counts (V1 p.132, p.133).
Note the warning: the exchange-rate example shows an $R^2$ of 0.9897 for a model that is invalid and 0.0008 for the model that is correct, so $R^2$ cannot choose between models estimated on different transformations of the data (V1 p.139, p.140).

### Instability and the sample-period decision

Coefficients estimated on different sample periods can differ substantially, and so can the model order (V1 p.134).
There is no theory that settles long versus short samples; the guiding principle is that the sample must be stationary, so do not pool fixed-rate and floating-rate exchange-rate regimes or pre- and post-crisis inflation regimes (V1 p.134).
On 1995 to 2018 data inflation needed an AR(2); on 2008 to 2018 data an AR(1) was well specified and the forecasts differed by 5 bps (V1 p.135).
The standard deviation of monthly inflation was 2.86% before 2008 and 3.54% after, which is the evidence of two regimes; residual autocorrelations alone cannot tell you the right sample period, judgment and knowledge of policy changes must (V1 p.136).

### Random walks, unit roots, and differencing

A random walk is $x_t = x_{t-1} + \varepsilon_t$, an AR(1) with $b_0 = 0$ and $b_1 = 1$ (V1 p.137).
Its best forecast is its current value, its mean-reverting level is undefined, and its variance after $t$ periods is $(t-1)\sigma^2$, which grows without limit (V1 p.137).
A random walk with drift adds $b_0 \neq 0$ and is just as nonstationary (V1 p.140).
Any AR(1) with $|b_1| = 1$ has a unit root; $|b_1| > 1$ is an explosive root (V1 p.141).
The cure is first-differencing: $y_t = x_t - x_{t-1} = \varepsilon_t$ (or $b_0 + \varepsilon_t$ with drift), which is stationary with mean-reverting level $0/(1 - 0) = 0$ and constant variance $\sigma^2$ (V1 p.137).
Modelling the differenced series with an AR(1) does not help forecast, since $b_0 = b_1 = 0$; the value of doing it is the diagnosis that the original series was a random walk (V1 p.138).
For the yen/dollar rate the level regression gave $\hat{b}_1 = 0.9919$ with a t-statistic of 211, and the differenced regression gave nothing significant, exactly the random-walk signature (V1 p.138, p.139).

> [!abstract] Why you cannot just t-test $b_1 = 1$
> If $b_1 = 1$ the series is not stationary, so the t-statistic on $\hat{b}_1$ does not follow the t-distribution and the test is invalid (V1 p.141).
> Dickey and Fuller subtract $x_{t-1}$ from both sides, giving $x_t - x_{t-1} = b_0 + g_1 x_{t-1} + \varepsilon_t$ with $g_1 = b_1 - 1$, and test $H_0: g_1 = 0$ (unit root) against $H_a: g_1 < 0$ (stationary) using their own larger-in-absolute-value critical values (V1 p.141).

### Moving averages: two things with one name

An $n$-period moving average is a smoothing device, the equal-weighted mean of the last $n$ observed values; it lags large moves and gives equal weight to stale data, so it is not a good predictor (V1 p.145, p.147).
A moving-average model, MA(q), is a forecasting model in which $x_t$ is a weighted sum of the current and $q$ past unobservable errors (V1 p.147, p.148).
The diagnostic that separates AR from MA is the pattern of the series' own autocorrelations: AR autocorrelations start large and decay gradually, MA(q) autocorrelations cut off to zero after lag $q$ (V1 p.148).
Monthly returns on the S&P BSE 100 had no significant autocorrelation at any of six lags, so they are MA(0): $x_t = \mu + \varepsilon_t$, unpredictable (V1 p.149).
ARMA(p, q) combines both, but the curriculum warns that its parameters are unstable, that choosing $p$ and $q$ is more art than science, and that even advocates do not use ARMA with fewer than 80 observations (V1 p.156).

### Seasonality

Seasonality shows up as a significant residual autocorrelation at the seasonal lag: lag 4 for quarterly data, lag 12 for monthly (V1 p.150, p.153).
The fix is a seasonal lag term, $x_t = b_0 + b_1 x_{t-1} + b_2 x_{t-4} + \varepsilon_t$ (V1 p.150).
For Starbucks the log-differenced AR(1) had a fourth residual autocorrelation of 0.7630 with t-statistic 6.47; adding the seasonal lag removed it and lifted $R^2$ from 0.2044 to 0.7032 (V1 p.151, p.152).
The forecast made in $t$ for $t+1$ is $\hat{b}_0 + \hat{b}_1 x_t + \hat{b}_2 x_{t-3}$: the seasonal lag of period $t+1$ is period $t-3$, a shift the examiner loves (V1 p.167).
In a log-differenced model every coefficient and forecast is a continuously compounded growth rate, and dollar sales are recovered as $\text{Sales}_t e^{\hat{y}_{t+1}}$ (V1 p.144, p.152).

### ARCH: when the variance is itself autoregressive

All the tests above assume homoskedastic errors.
Engle's ARCH(1) lets the error variance depend on the previous squared error, $\varepsilon_t \sim N(0, a_0 + a_1 \varepsilon_{t-1}^2)$ (V1 p.156).
Test it by regressing squared residuals on their own lag; a significant $a_1$ means the standard errors of the underlying model are wrong and its t-tests are invalid, so use generalized least squares or another correction (V1 p.157, p.158).
The compensating benefit is that the variance becomes forecastable: $\hat{\sigma}_{t+1}^2 = \hat{a}_0 + \hat{a}_1 \hat{\varepsilon}_t^2$, which for CPI inflation gave 6.3626 after a zero error and 6.6380 after a 1% error (V1 p.157, p.159).
ARCH(p) and GARCH generalize this, and GARCH is as finicky as ARMA (V1 p.159).

### Two series at once: unit roots and cointegration

Regressing one time series on another is only safe if the error is stationary.
Test each series for a unit root first (V1 p.159).
Neither has one: regress freely.
Exactly one has one: the error cannot be stationary, the coefficients are inconsistent, the apparent significance is spurious (V1 p.160).
Both have one: they are usable only if cointegrated, meaning a long-run economic relationship keeps them from diverging without bound, such as a shared trend (V1 p.161).
The Engle-Granger procedure regresses $y_t$ on $x_t$ and runs a Dickey-Fuller test on the residuals with Engle-Granger critical values; rejecting the unit root in the residuals means cointegration and consistent long-run coefficients, though the regression may still be a poor model of short-run dynamics (V1 p.161).
With three or more cointegrated unit-root series the modelling is beyond the curriculum, and the advice is to avoid it (V1 p.163).

### The model-selection procedure

The nine suggested steps are the LOS "determine an appropriate model" made concrete (V1 p.164, p.165).

| Step | Question | If yes | If no |
|---|---|---|---|
| 1 | Is a causal regression or a time-series model appropriate? | Use the regression path (LM01 to LM04) | Continue |
| 2 | Plot: does the series look covariance stationary (no trend, no seasonality, no shift)? | Go to step 5 | Note the violation |
| 3 | Does a linear or log-linear trend fit with residuals free of serial correlation (Durbin-Watson)? | Use the trend model | Go to step 4 |
| 4 | Transform: linear trend, first-difference; exponential trend, log then first-difference; shift, split the sample; seasonality, plan seasonal lags | Now stationary | Re-examine |
| 5 | Does AR(1) leave uncorrelated residuals ($t = \hat{\rho}_k \sqrt{T}$ at every lag)? | Use AR(1) | Go to step 6 |
| 6 | Does AR(2), then AR(3), and so on leave uncorrelated residuals? | Use that AR(p) | Keep adding lags |
| 7 | Is the seasonal residual autocorrelation significant? | Add the seasonal lag and retest | Continue |
| 8 | Do squared residuals regress significantly on their lag (ARCH)? | Correct with generalized least squares | Rely on the standard errors |
| 9 | Does out-of-sample RMSE confirm the in-sample choice? | Deploy | Reconsider |

The footnote to step 5 adds the AR-versus-MA check: look at the first five or six autocorrelations of the series; a sudden cut-off after lag $q$ points to MA(q), gradual decay to AR (V1 p.165).

## Formulas and derivations

**Linear trend model, Equation (1)** (V1 p.113)
$$ y_t = b_0 + b_1 t + \varepsilon_t, \quad t = 1, 2, \dots, T $$
^f-01-05-1

- $y_t$: value of the series at time $t$; $t$: the time index, 1 in the first sample period; $b_1$: the trend coefficient, the constant amount added each period; $\varepsilon_t$: random error.
- Estimated by ordinary least squares, minimizing the sum of squared residuals (V1 p.113).
- The predicted change from one period to the next is $\hat{b}_1$ regardless of the level of the series (V1 p.114).

**Linear trend prediction, in sample and out of sample** (V1 p.113)
$$ \hat{y}_t = \hat{b}_0 + \hat{b}_1 t, \qquad \hat{y}_{T+k} = \hat{b}_0 + \hat{b}_1 (T + k) $$
^f-01-05-2

- $T$: last in-sample period; $k$: periods ahead.
- The index must be counted from the first sample observation; for CPI with $T = 294$, June 2020 (12 months after June 2019) is $t = 306$ (V1 p.115).
- CPI example: $2.7845 - 0.0037(306) = 1.6523$ (V1 p.115).

> [!tip] Calculator
> BA II Plus: `0.0037 +/- x 306 = + 2.7845 =` gives $1.6523$.
> Count $t$ by hand first: $t = T + k$, never $k$ alone.

**Exponential growth process, Equation (2)** (V1 p.116)
$$ y_t = e^{b_0 + b_1 t}, \quad t = 1, 2, \dots, T $$
^f-01-05-3

- $e^{b_1}$ is the gross growth factor per period.
- Ratio of consecutive values: $y_{t+1}/y_t = e^{b_0 + b_1(t+1)} / e^{b_0 + b_1 t} = e^{b_1}$, the same in every period, which is the definition of constant-rate growth (V1 p.116, p.117).

**Constant growth rate implied by a log-linear trend** (V1 p.117)
$$ \frac{y_{t+1} - y_t}{y_t} = e^{b_1} - 1 $$
^f-01-05-4

- With $b_1 = 0.05$ the growth rate is $e^{0.05} - 1 = 0.051271$, or 5.13% per period, not 5% (V1 p.117).
- Starbucks: $e^{0.0295} - 1 = 2.99\%$ per quarter (V1 p.120).

**Log-linear trend model, Equation (3), and its level forecast** (V1 p.117)
$$ \ln y_t = b_0 + b_1 t + \varepsilon_t, \qquad \hat{y}_t = e^{\hat{b}_0 + \hat{b}_1 t} $$
^f-01-05-5

- Take natural logs of both sides of the exponential process and add an error; the model is linear in $b_0$ and $b_1$ so OLS applies (V1 p.117).
- The regression predicts $\ln y_t$; the level forecast requires exponentiation because $e^{\ln y_t} = y_t$ (V1 p.117).
- Starbucks $t = 75$: $6.7617 + 0.0295(75) = 8.9742$, $e^{8.9742} = \$7{,}896.7$ million (V1 p.120).

> [!tip] Calculator
> BA II Plus: `0.0295 x 75 = + 6.7617 =` shows $8.9742$; then `2nd LN` (the $e^x$ key) gives $7{,}896.7$.
> Forgetting `2nd LN` returns the log, which is the classic distractor.

**Durbin-Watson decision for a trend model** (V1 p.122)
$$ H_0: \text{no positive serial correlation}; \quad \text{reject if } DW < d_l, \quad DW \approx 2 \text{ under } H_0 $$
^f-01-05-6

- $d_l$: lower critical value from the Durbin-Watson table for $k = 1$ regressor and the sample size (1.77 for the CPI sample, 1.60 for the Starbucks sample, at 5%) (V1 p.122).
- Small DW means positive serial correlation, large DW means negative (V1 p.122).
- The test is valid for trend models because the regressor $t$ is not a lagged dependent variable; it is invalid for every AR model (V1 p.124).

**First-order autoregression AR(1), Equation (4)** (V1 p.123)
$$ x_t = b_0 + b_1 x_{t-1} + \varepsilon_t $$
^f-01-05-7

- The distinction between $y$ and $x$ is dropped because the regressor is the series' own lag (V1 p.123).
- OLS estimation is valid only if $x_t$ is covariance stationary and the errors are uncorrelated (V1 p.124).

**Autoregression of order p, AR(p), Equation (5)** (V1 p.123)
$$ x_t = b_0 + b_1 x_{t-1} + b_2 x_{t-2} + \dots + b_p x_{t-p} + \varepsilon_t $$
^f-01-05-8

- $p$ past values predict the current value; each added lag consumes one observation at the start of the sample when the sample start is fixed (V1 p.123, p.151).

**Covariance stationarity conditions** (V1 p.123)
$$ E(y_t) = \mu, \; |\mu| < \infty; \qquad \text{cov}(y_t, y_{t-s}) = \lambda_s, \; |\lambda_s| < \infty, \; s = 0, \pm 1, \pm 2, \dots $$
^f-01-05-9

- Constant finite mean; constant finite variance ($s = 0$, since $\text{cov}(y_t, y_t) = \text{var}(y_t)$); constant finite autocovariance at every fixed lag (V1 p.123).
- "Weakly stationary" is a synonym; "stationary" in the curriculum means covariance stationary (V1 p.123).
- If violated, $\hat{b}_1$ is biased and all hypothesis tests are invalid (V1 p.123).

**Autocorrelation of a time series at lag k** (V1 p.125)
$$ \rho_k = \frac{\text{cov}(x_t, x_{t-k})}{\sigma_x^2} = \frac{E[(x_t - \mu)(x_{t-k} - \mu)]}{\sigma_x^2} $$
^f-01-05-10

- Because $\text{cov}(x_t, x_{t-k}) \le \sigma_x^2$ with equality at $k = 0$, $|\rho_k| \le 1$ (V1 p.125).

**Estimated autocorrelation at lag k** (V1 p.125)
$$ \hat{\rho}_k = \frac{\sum_{t=k+1}^{T} (x_t - \bar{x})(x_{t-k} - \bar{x})}{\sum_{t=1}^{T} (x_t - \bar{x})^2} $$
^f-01-05-11

- The population mean is replaced by the sample mean; the numerator sums over the $T - k$ overlapping pairs (V1 p.125).
- In a spreadsheet the first-order residual autocorrelation is the correlation of residuals 1 to $T-1$ with residuals 2 to $T$ (V1 p.125).

**Error autocorrelation at lag k** (V1 p.125)
$$ \rho_{\varepsilon, k} = \frac{\text{cov}(\varepsilon_t, \varepsilon_{t-k})}{\sigma_\varepsilon^2} = \frac{E(\varepsilon_t \varepsilon_{t-k})}{\sigma_\varepsilon^2} $$
^f-01-05-12

- The expected error is zero, so the mean-centring terms drop out (V1 p.125).
- A correctly specified model has $\rho_{\varepsilon, k} = 0$ at every lag; estimated with the residual autocorrelations (V1 p.125).

**Residual autocorrelation test** (V1 p.125)
$$ s.e.(\hat{\rho}_k) = \frac{1}{\sqrt{T}}, \qquad t_k = \frac{\hat{\rho}_k}{1/\sqrt{T}} = \hat{\rho}_k \sqrt{T} $$
^f-01-05-13

- $T$: number of observations in the regression; the same standard error applies at every lag (V1 p.125).
- Reject $H_0: \rho_{\varepsilon, k} = 0$ if $|t_k|$ exceeds the t critical value with $T - (p+1)$ degrees of freedom, roughly 1.97 to 2.02 in the examples (V1 p.127, p.130).
- Three-step method: estimate the AR model, compute residual autocorrelations, test each; any rejection means misspecification (V1 p.125).

> [!tip] Calculator
> BA II Plus: `T` then `SQRT` then `1/x` gives the standard error; multiply each autocorrelation by `SQRT(T)` instead to get the t-statistic directly.
> Example: `65 SQRT 1/x =` shows $0.1240$; `0.1308 x 65 SQRT =` shows $1.0545$.

**Mean-reverting level of an AR(1)** (V1 p.128)
$$ x^{*} = \frac{b_0}{1 - b_1} $$
^f-01-05-14

- Set $x_{t+1} = x_t = x^{*}$ in $x_{t+1} = b_0 + b_1 x_t$ and solve: $x^{*}(1 - b_1) = b_0$ (V1 p.128).
- Above the level the forecast falls, below it rises; every covariance-stationary series has a finite level (V1 p.128).
- Intel: $0.1513 / (1 - 0.7462) = 0.5961$ (V1 p.128).
- With a negative $b_1$ the denominator exceeds 1: $-0.0668 / (1 + 0.2320) = -0.0542$ (V1 p.190).
- Derived extension the curriculum states only as "similar results hold for AR(p)" (V1 p.166): setting all lags equal gives $x^{*} = b_0 / (1 - b_1 - b_2 - \dots - b_p)$.

> [!tip] Calculator
> BA II Plus: `1 - 0.7462 = ` then `1/x x 0.1513 =` gives $0.5961$.
> Watch the sign of $b_1$: a negative $b_1$ is subtracted, so the denominator becomes $1 + |b_1|$.

**One-period-ahead AR(1) forecast, Equation (6)** (V1 p.128)
$$ \hat{x}_{t+1} = \hat{b}_0 + \hat{b}_1 x_t $$
^f-01-05-15

- The expected error is zero, so the forecast is the deterministic part evaluated at the latest actual observation (V1 p.127).
- Intel at 63%: $0.1513 + 0.7462(0.63) = 0.6214$ (V1 p.129).

**Two-period-ahead forecast by the chain rule, Equation (7)** (V1 p.128)
$$ \hat{x}_{t+2} = \hat{b}_0 + \hat{b}_1 \hat{x}_{t+1} = \hat{b}_0 + \hat{b}_1(\hat{b}_0 + \hat{b}_1 x_t) $$
^f-01-05-16

- $x_{t+1}$ is unknown at $t$, so its forecast is substituted (V1 p.128).
- Intel: $0.1513 + 0.7462(0.6214) = 0.6150$ (V1 p.129).
- Multi-period forecasts carry the uncertainty of every link, so their variance exceeds the one-period variance (V1 p.128).

**One-period-ahead AR(2) forecast** (V1 p.131)
$$ \hat{x}_{t+1} = \hat{b}_0 + \hat{b}_1 x_t + \hat{b}_2 x_{t-1} $$
^f-01-05-17

- The most recent observation multiplies $b_1$, the one before it multiplies $b_2$; swapping them is the standard distractor (V1 p.131, p.188).
- Inflation at 4% last month and 3% the month before: $1.5996 + 0.4759(4) - 0.1964(3) = 2.91\%$ (V1 p.131).

**Root mean squared error** (V1 p.132)
$$ RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (\text{Actual}_i - \text{Forecast}_i)^2} $$
^f-01-05-18

- $n$: number of out-of-sample forecasts; the sign convention of the error does not matter because it is squared.
- The model with the smallest out-of-sample RMSE is the most accurate; in-sample comparisons use the regression standard error instead (V1 p.132).
- Steps: error, square, sum, divide by $n$, square root (V1 p.191).

> [!tip] Calculator
> BA II Plus statistics worksheet: `2nd DATA`, enter each error as $X$ with $Y = 1$, then `2nd STAT` and read $\sigma_x$ only if the mean error is zero; safer is to square by hand: `0.0029 x^2 + 0.0598 x^2 + 0.0307 x^2 + 0.0263 x^2 = / 4 = SQRT` gives $0.0361$.

**Random walk without drift, Equation (8)** (V1 p.137)
$$ x_t = x_{t-1} + \varepsilon_t, \quad E(\varepsilon_t) = 0, \; E(\varepsilon_t^2) = \sigma^2, \; \text{cov}(\varepsilon_t, \varepsilon_s) = 0 \text{ for } t \ne s $$
^f-01-05-19

- An AR(1) with $b_0 = 0$ and $b_1 = 1$; the best forecast of $x_t$ made at $t - 1$ is $x_{t-1}$, for every horizon (V1 p.137).
- Mean-reverting level $b_0/(1 - b_1) = 0/0$, undefined (V1 p.137).

**Variance of a random walk** (V1 p.137)
$$ \text{var}(x_t) = (t - 1)\sigma^2 \to \infty \text{ as } t \to \infty $$
^f-01-05-20

- Start at $x_1 = 0$; $x_2 = \varepsilon_2$ has variance $\sigma^2$; $x_3 = \varepsilon_2 + \varepsilon_3$ has variance $2\sigma^2$ because the errors are uncorrelated; induction gives $(t-1)\sigma^2$ (V1 p.137).
- Unbounded variance violates the second stationarity condition (V1 p.137).

**First difference of a random walk** (V1 p.137)
$$ y_t = x_t - x_{t-1} = \Delta x_t = \varepsilon_t $$
^f-01-05-21

- $y_t$ is an AR(1) with $b_0 = 0$ and $b_1 = 0$: mean-reverting level $0/1 = 0$, variance $\sigma^2$ in every period, so it is covariance stationary (V1 p.137).
- The best forecast of $y_t$ is zero, that is, no change in $x$ (V1 p.137).

**Random walk with drift, Equation (9)** (V1 p.140)
$$ x_t = b_0 + x_{t-1} + \varepsilon_t, \quad b_1 = 1, \; b_0 \ne 0; \qquad \Delta x_t = b_0 + \varepsilon_t $$
^f-01-05-22

- The series is expected to change by the constant $b_0$ each period; still a unit root, still nonstationary until differenced (V1 p.140).

**Dickey-Fuller unit root regression, Equation (10)** (V1 p.141)
$$ x_t - x_{t-1} = b_0 + g_1 x_{t-1} + \varepsilon_t, \quad g_1 = b_1 - 1; \qquad H_0: g_1 = 0 \;\; (\text{unit root}), \; H_a: g_1 < 0 $$
^f-01-05-23

- Subtract $x_{t-1}$ from both sides of the AR(1): the dependent variable becomes the first difference, the slope becomes $b_1 - 1$, the independent variable is unchanged (V1 p.141, p.192).
- The t-statistic on $\hat{g}_1$ is computed conventionally but compared with Dickey-Fuller critical values, which are larger in absolute value than the t critical values (V1 p.141).
- A conventional t-test of $b_1 = 1$ is invalid because under $H_0$ the series is nonstationary (V1 p.141).

**n-period moving average, Equation (11)** (V1 p.145)
$$ MA_n(t) = \frac{x_t + x_{t-1} + \dots + x_{t-(n-1)}}{n} $$
^f-01-05-24

- Equal weights on the current and previous $n - 1$ observed values; a smoother that lags turning points (V1 p.145, p.147).
- AstraZeneca: $(8{,}490 + 8{,}601 + 8{,}405 + 8{,}872)/4 = \$8{,}592$ million (V1 p.145).

**Moving-average model of order 1, MA(1), Equation (12)** (V1 p.147)
$$ x_t = \varepsilon_t + \theta \varepsilon_{t-1}, \quad E(\varepsilon_t) = 0, \; E(\varepsilon_t^2) = \sigma^2, \; \text{cov}(\varepsilon_t, \varepsilon_s) = 0 \text{ for } t \ne s $$
^f-01-05-25

- $\theta$: the MA parameter; weights of 1 and $\theta$ on two unobservable, uncorrelated errors (V1 p.147).
- Only the first autocorrelation is nonzero: memory of one period (V1 p.148).

**Moving-average model of order q, MA(q), Equation (13)** (V1 p.148)
$$ x_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \dots + \theta_q \varepsilon_{t-q} $$
^f-01-05-26

- The first $q$ autocorrelations are nonzero and all later ones are zero, which identifies $q$ (V1 p.148).
- AR autocorrelations decay gradually; MA autocorrelations cut off abruptly (V1 p.148).

**MA(0) with a nonzero mean, Equation (14)** (V1 p.149)
$$ x_t = \mu + \varepsilon_t $$
^f-01-05-27

- No autocorrelation at any lag: the series is unpredictable, the model early weak-form efficiency studies used for returns (V1 p.149).

**AR(1) with a seasonal lag, Equation (15), and its forecast** (V1 p.150)
$$ x_t = b_0 + b_1 x_{t-1} + b_2 x_{t-4} + \varepsilon_t \quad (\text{quarterly}); \qquad \hat{x}_{t+1} = \hat{b}_0 + \hat{b}_1 x_t + \hat{b}_2 x_{t-3} $$
^f-01-05-28

- The seasonal lag is the value one year earlier: lag 4 for quarterly data, lag 12 for monthly (V1 p.150, p.153).
- Seasonality is detected as a significant residual autocorrelation at the seasonal lag of the model without the seasonal term (V1 p.150).
- The forecast for $t + 1$ uses $x_{t-3}$, because $(t+1) - 4 = t - 3$ (V1 p.167).
- Starbucks: $0.0107 - 0.1540(0.01) + 0.7549(0.02) = 0.0243$ (V1 p.152).

**Level forecast from a log-differenced model** (V1 p.144)
$$ \hat{y}_{t+1} = \ln \text{Sales}_{t+1} - \ln \text{Sales}_t \;\Rightarrow\; \widehat{\text{Sales}}_{t+1} = \text{Sales}_t \, e^{\hat{y}_{t+1}} $$
^f-01-05-29

- $\hat{y}_{t+1}$ is a continuously compounded growth rate; the simple growth rate is $e^{\hat{y}} - 1$ and the difference is usually small (V1 p.144).
- AstraZeneca: $\hat{y} = -0.0075$, so $8{,}872 \times e^{-0.0075} = 8{,}872 \times 0.9925 = \$8{,}805$ million (V1 p.144).

> [!tip] Calculator
> BA II Plus: `8872 / 8405 = LN` gives $y_t = 0.0541$; `x 0.5493 = +/- + 0.0222 =` gives $-0.0075$; `2nd LN x 8872 =` gives $8{,}805$.
> For PoweredUP style questions with five quarters of data, compute the two log differences separately and store them (`STO 1`, `STO 2`) before combining.

**ARMA(p, q) model, Equation (16)** (V1 p.156)
$$ x_t = b_0 + b_1 x_{t-1} + \dots + b_p x_{t-p} + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \dots + \theta_q \varepsilon_{t-q} $$
^f-01-05-30

- $b_i$: autoregressive parameters; $\theta_j$: moving-average parameters (V1 p.156).
- Limitations: unstable parameters, no reliable rule for $p$ and $q$, may forecast poorly, not for fewer than 80 observations (V1 p.156).

**ARCH(1) error process, Equation (17)** (V1 p.156)
$$ \varepsilon_t \sim N\left(0, \; a_0 + a_1 \varepsilon_{t-1}^2\right) $$
^f-01-05-31

- Conditional on last period's error, this period's error is normal with variance $a_0 + a_1 \varepsilon_{t-1}^2$; $a_1 = 0$ gives constant variance $a_0$, $a_1 > 0$ makes a large error raise next period's variance (V1 p.157).

**ARCH(1) test regression, Equation (18)** (V1 p.157)
$$ \hat{\varepsilon}_t^2 = a_0 + a_1 \hat{\varepsilon}_{t-1}^2 + u_t $$
^f-01-05-32

- Regress the squared residuals of the fitted AR, MA or ARMA model on a constant and one lag of themselves; a statistically significant $\hat{a}_1$ means ARCH(1) (V1 p.157).
- Consequence: the standard errors of the original model are wrong, so use generalized least squares or another heteroskedasticity correction (V1 p.158).
- The test uses one fewer observation than the model because of the lag (V1 p.157).

**ARCH(1) variance forecast** (V1 p.157)
$$ \hat{\sigma}_{t+1}^2 = \hat{a}_0 + \hat{a}_1 \hat{\varepsilon}_t^2 $$
^f-01-05-33

- Inflation: $6.3626 + 0.2754(0)^2 = 6.3626$ after a zero error; $6.3626 + 0.2754(1)^2 = 6.6380$ after a 1% error (V1 p.159).
- Square the error before multiplying: the 1% error enters as $1^2$, and an error of 2 would enter as 4.

**ARCH(p) variance** (V1 p.159)
$$ \sigma_t^2 = a_0 + a_1 \varepsilon_{t-1}^2 + \dots + a_p \varepsilon_{t-p}^2 $$
^f-01-05-34

- Linear in the previous $p$ squared errors; GARCH models are the ARMA analogue for the variance and share ARMA's instability (V1 p.159).

**Engle-Granger cointegration test** (V1 p.161)
$$ \text{(1) } y_t = b_0 + b_1 x_t + \varepsilon_t; \quad \text{(2) DF test on } \hat{\varepsilon}_t \text{ with Engle-Granger critical values}; \quad H_0: \text{unit root in } \hat{\varepsilon}_t \text{ (not cointegrated)} $$
^f-01-05-35

- Applies only when both series have a unit root; rejecting $H_0$ means the error is stationary, the series are cointegrated, and the OLS coefficients and standard errors are consistent for the long-run relation (V1 p.161).
- Failing to reject means any regression between the two is spurious (V1 p.161).
- Standard Dickey-Fuller critical values cannot be used because the residuals depend on estimated coefficients (V1 p.161).

| Unit-root outcome | Can we regress $y_t$ on $x_t$? | Why (V1 p.159 to p.161) |
|---|---|---|
| Neither series has a unit root | Yes | Both stationary, error stationary |
| Only the dependent variable has one | No | Error nonstationary, coefficients inconsistent, spurious significance |
| Only the independent variable has one | No | Same |
| Both have one, not cointegrated | No | Error nonstationary, regression meaningless |
| Both have one, cointegrated | Yes, for the long-run relation | Error stationary; short-run dynamics need an error-correction model |

## Worked examples

### Example 1: The trend in the US Consumer Price Index (V1 p.114)

Setting: Lisette Miller fits $y_t = b_0 + b_1 t + \varepsilon_t$ to 294 months of annualized CPI inflation, January 1995 to June 2019.
Exhibit 4 output: $\hat{b}_0 = 2.7845$ (s.e. 0.3732, $t = 7.4611$), $\hat{b}_1 = -0.0037$ (s.e. 0.0022, $t = -1.68$), $R^2 = 0.0099$, DW = 1.2145 (V1 p.114, p.115).

Step 1, significance: with 292 degrees of freedom the 5% critical value is 1.97; the intercept is significant, the trend is not ($|{-1.68}| < 1.97$) (V1 p.114).
Step 2, in-sample fitted values: $\hat{y}_1 = 2.7845 - 0.0037(1) = 2.7808\%$; $\hat{y}_{294} = 2.7845 - 0.0037(294) = 2.7845 - 1.0878 = 1.6967\%$ (the curriculum rounds to 1.697% and mislabels the subscript as 228) (V1 p.115).
Step 3, out-of-sample: June 2020 is 12 months past the sample, $t = 294 + 12 = 306$; $\hat{y}_{306} = 2.7845 - 0.0037(306) = 2.7845 - 1.1322 = 1.6523\%$ (V1 p.115).
Step 4, interpretation: the slope says annualized inflation fell about 0.37 bps per month over the sample, not significantly different from zero; $R^2$ of 0.99% means huge forecast uncertainty (V1 p.115).
Recomputed in Python: 2.7808, 1.6967, 1.6523, all match.
^ex-01-05-1

### Example 2: A linear trend regression for quarterly sales at Starbucks (V1 p.117)

Setting: Ray Benedict fits a linear trend to 74 quarters of Starbucks sales, 2Q FY2001 to 3Q FY2019.
Exhibit 7: $\hat{b}_0 = 137.4213$ ($t = 1.6559$), $\hat{b}_1 = 80.2060$ (s.e. 1.9231, $t = 41.7066$), $R^2 = 0.9603$, DW = 0.40 (V1 p.118).

Step 1: the trend is overwhelmingly significant ($80.2060/1.9231 = 41.71$, recomputed) and $R^2$ is 0.96, so the output "looks" fine.
Step 2: the residual plot (Exhibit 9) is persistently positive 2001 to 2008, negative 2008 to 2015, positive 2017 to 2019 (V1 p.119).
Step 3: persistent residuals are serially correlated errors, a violation of the regression assumption that is serious in time series because the regressor and regressand are not distinct; the model is rejected despite the high $R^2$ (V1 p.119).
Lesson: a linear trend that sits above or below a curving series for years is the visual signature of a series that grows at a constant rate, not a constant amount.
^ex-01-05-2

### Example 3: A log-linear regression for quarterly sales at Starbucks (V1 p.120)

Setting: same 74 quarters, model $\ln y_t = b_0 + b_1 t + \varepsilon_t$.
Exhibit 10: $\hat{b}_0 = 6.7617$ ($t = 206.80$), $\hat{b}_1 = 0.0295$ (s.e. 0.0008, $t = 36.875$), $R^2 = 0.9771$, DW = 0.26 (V1 p.120).

Question 1, forecast for 4Q 2019 ($t = 75$):
$\ln \hat{y}_{75} = 6.7617 + 0.0295(75) = 6.7617 + 2.2125 = 8.9742$.
$\hat{y}_{75} = e^{8.9742} = \$7{,}896.7$ million (Python: 7,896.70) (V1 p.120).
Implied quarterly growth: $e^{0.0295} - 1 = 0.029939$, or 2.99% per quarter (V1 p.120).
Question 2, comparison with the linear trend: $\hat{y}_{75} = 137.4213 + 80.2060(75) = 137.4213 + 6{,}015.45 = \$6{,}152.87$ million, far below the log-linear forecast (V1 p.121).
Why they differ: the linear model adds \$80 million a quarter from a fit anchored to the whole sample, while the log-linear model compounds at 3% from a level already near \$7,700 million; near the end of an exponential series the linear line is well below the data.
Both models still fail the Durbin-Watson test (DW = 0.26 against $d_l$ above 1.60), so neither is the final model (V1 p.122).
^ex-01-05-3

### Example 4: Predicting gross margins for Intel Corporation (V1 p.126)

Setting: Melissa Jones fits AR(1) to 65 quarterly gross margins, 1Q 2003 to 2Q 2019.
Exhibit 12: $\hat{b}_0 = 0.1513$ (s.e. 0.0480, $t = 3.15$), $\hat{b}_1 = 0.7462$ (s.e. 0.0809, $t = 9.2236$), $R^2 = 0.5746$, DW = 1.743; residual autocorrelations 0.1308, $-0.2086$, 0.0382, 0.0608 (V1 p.126).

Step 1, coefficients: 63 degrees of freedom, critical value about 2.0; both coefficients are significant (V1 p.127).
Step 2, are those tests valid: Durbin-Watson cannot be used because the regressor is a lagged dependent variable; test the residual autocorrelations instead (V1 p.127).
Step 3, standard error: $1/\sqrt{65} = 0.1240$ (Python: 0.12403).
Step 4, t-statistics: $0.1308/0.1240 = 1.0545$; $-0.2086/0.1240 = -1.6818$; $0.0382/0.1240 = 0.3080$; $0.0608/0.1240 = 0.4903$; none exceeds 2.0 in absolute value, so the residuals are not serially correlated and the model is correctly specified (V1 p.127).
Step 5, forecasts: from 55%, $0.1513 + 0.7462(0.55) = 0.1513 + 0.4104 = 0.5617$; from 65%, $0.1513 + 0.7462(0.65) = 0.1513 + 0.4850 = 0.6363$ (V1 p.127).
The forecast rises from below and falls from above a level between them, which Example 4's continuation identifies as $0.1513/(1 - 0.7462) = 0.5961$ (V1 p.128).
^ex-01-05-4

### Example 5: Multiperiod prediction of Intel's gross margin (V1 p.129)

Setting: current gross margin 63%, same model.
One period ahead: $\hat{x}_{t+1} = 0.1513 + 0.7462(0.63) = 0.1513 + 0.4701 = 0.6214$.
Two periods ahead by the chain rule: $\hat{x}_{t+2} = 0.1513 + 0.7462(0.6214) = 0.1513 + 0.4637 = 0.6150$, or 61.50% (V1 p.129).
Python: 0.62141 and 0.61499, matching.
Check the direction: 0.63 is above the mean-reverting level 0.5961, so each forecast steps down toward it, and the step shrinks ($0.63 \to 0.6214 \to 0.6150$) because each period moves only $b_1 = 0.7462$ of the remaining gap.
^ex-01-05-5

### Example 6: Modeling US CPI inflation (V1 p.129)

Setting: Miller models annualized monthly CPI inflation, January 1995 to December 2018, starting with AR(1) (287 observations) then AR(2) (286 observations).
Exhibit 13, AR(1): intercept printed as 0.13346 in the table and used as 1.3346 in the text (s.e. 0.2134), $\hat{b}_1 = 0.3984$ (s.e. 0.0544, $t = 7.3235$), $R^2 = 0.1586$, s.e. of regression 2.9687, DW = 1.8442; residual autocorrelations 0.0777, $-0.1653$, $-0.1024$, $-0.0845$ (V1 p.129).
Exhibit 14, AR(2): $\hat{b}_0 = 1.5996$ ($t = 7.1252$), $\hat{b}_1 = 0.4759$ ($t = 8.1636$), $\hat{b}_2 = -0.1964$ ($t = -3.368$), $R^2 = 0.1907$, s.e. 2.9208, DW = 1.9934; residual autocorrelations 0.0032, 0.0042, $-0.0338$, 0.0155 (V1 p.131).

Step 1, AR(1) residual test: $1/\sqrt{287} = 0.0590$; lag-2 t-statistic $-0.1653/0.0590 = -2.80$, beyond the 1.97 critical value, so the AR(1) is misspecified (V1 p.130).
Step 2, AR(2) residual test: $1/\sqrt{286} = 0.0591$; the largest t-statistic in absolute value is $-0.5696$, so no residual autocorrelation is significant and the AR(2) is correctly specified (V1 p.131).
Question, forecast difference given inflation of 4% last month and 3% the month before:
AR(1): $1.3346 + 0.3984(4) = 1.3346 + 1.5936 = 2.93\%$.
AR(2): $1.5996 + 0.4759(4) - 0.1964(3) = 1.5996 + 1.9036 - 0.5892 = 2.91\%$.
The incorrect AR(1) would have forecast about 2 bps higher (V1 p.131).
Python: 2.9282 and 2.9140, matching to rounding.
Discrepancy note: the exhibit prints the AR(1) intercept as 0.13346, which would give $0.13346 + 1.5936 = 1.73\%$; the text and the mean-reverting level ($1.3346/(1 - 0.3984) = 2.22$, consistent with the AR(2) level $1.5996/(1 - 0.4759 + 0.1964) = 2.22$) support 1.3346, while the out-of-sample errors in Exhibit 15 were computed with 0.13346.
On the exam, use the intercept exactly as printed in the exhibit you are given.
^ex-01-05-6

### Example 7: In-sample forecast comparisons of US CPI inflation (V1 p.132)

Setting: compare the AR(1) and AR(2) models of Example 6 in sample.
The in-sample forecast error variance is measured by the regression standard error: AR(1) 2.9687, AR(2) 2.9208 (V1 p.132).
Ratio: $2.9208/2.9687 = 0.9839$, so the AR(2) standard error is 98.39% of the AR(1) standard error, consistent with the AR(2) being preferable (V1 p.132).
Python: 0.98386.
The point of the example is the definition: in-sample forecast errors are the residuals of the fitted model, and the model with the smaller residual variance has the smaller in-sample error (V1 p.132).
^ex-01-05-7

### Example 8: Out-of-sample forecast comparisons of US CPI inflation (V1 p.133)

Setting: the same two models forecast January to September 2019, nine months outside the estimation sample; Exhibit 15 lists each month's error and squared error.

| Month | AR(1) error | Squared | AR(2) error | Squared |
|---|---|---|---|---|
| Jan | 0.1335 | 0.0178 | $-1.6000$ | 2.5599 |
| Feb | $-2.2931$ | 5.2585 | 0.8266 | 0.6833 |
| Mar | $-3.8068$ | 14.4916 | 2.1522 | 4.6320 |
| Apr | $-1.5716$ | 2.4699 | 0.2014 | 0.0406 |
| May | 0.3850 | 0.1482 | $-1.1714$ | 1.3722 |
| Jun | $-0.5924$ | 0.3510 | $-0.2488$ | 0.0619 |
| Jul | $-3.0458$ | 9.2770 | 1.7228 | 2.9680 |
| Aug | 0.3850 | 0.1482 | $-1.8982$ | 3.6030 |
| Sep | 0.6142 | 0.3772 | $-1.4554$ | 2.1181 |

Step 1, average squared error: AR(1) $32.5394/9 = 3.6155$; AR(2) $18.0390/9 = 2.0043$ (V1 p.133).
Step 2, RMSE: AR(1) $\sqrt{3.6155} = 1.9014$; AR(2) $\sqrt{2.0043} = 1.4157$ (V1 p.133).
Step 3, ratio: $1.4157/1.9014 = 74.46\%$, so the AR(2) was more accurate out of sample as well as in sample (V1 p.133).
Python from the listed errors: 1.90144 and 1.41576 (the curriculum's 1.4157 reflects rounding of the squared errors).
Recomputing the errors themselves: the AR(2) column equals Actual minus Forecast with $\hat{b}_0 = 1.5996$ (January: $0 - 1.5996 = -1.5996$), while the AR(1) column equals Forecast minus Actual with the printed intercept 0.13346 (January: $0.13346 + 0.3984(0) - 0 = 0.1335$); the sign convention does not affect RMSE.
Caveat the curriculum itself states: nine observations is a small out-of-sample test, and coefficient stability must also be considered (V1 p.133).
^ex-01-05-8

### Example 9: Instability in time-series models of US inflation (V1 p.134)

Setting: a colleague argues the 1995 to 2018 inflation series has two regimes, before and after the 2008 crisis, so Miller re-estimates AR(1) on January 2008 to December 2018 (132 observations).
Exhibit 16: $\hat{b}_0 = 0.8431$ ($t = 2.8397$), $\hat{b}_1 = 0.5036$ ($t = 6.6438$), $R^2 = 0.2536$; residual autocorrelations 0.0999, $-0.1045$, $-0.1568$, 0.0500 with standard error 0.087 (V1 p.135).

Step 1: $1/\sqrt{132} = 0.0870$ (Python: 0.08704); the largest residual t-statistic is $-1.8051$, below the 1.99 critical value, so the AR(1) is correctly specified on the shorter sample and no AR(2) is needed (V1 p.135).
Step 2, forecast with 4% last month: $0.8431 + 0.5036(4) = 0.8431 + 2.0144 = 2.8575 \approx 2.86\%$ (V1 p.135).
Step 3, compare with the long-sample AR(2) forecast of 2.91%: the shorter sample forecasts 0.05 percentage points lower (V1 p.135).
Step 4, which is right: inflation volatility was 2.86% in 1995 to 2007 and 3.54% in 2008 to 2018, so the full sample is probably not covariance stationary and the shorter-sample model is the better choice (V1 p.136).
Lesson: clean residual autocorrelations on the long sample did not reveal the regime change; judgment about policy regimes did (V1 p.136).
^ex-01-05-9

### Example 10: The yen/US dollar exchange rate (V1 p.138)

Setting: AR(1) on 467 month-end JPY/USD observations, October 1980 to August 2019, then AR(1) on the first difference (466 observations).
Exhibit 18 (levels): $\hat{b}_0 = 0.8409$ ($t = 1.2931$), $\hat{b}_1 = 0.9919$ (s.e. 0.0047, $t = 211.0426$), $R^2 = 0.9897$; residual autocorrelations 0.0302, 0.0741, 0.0427, $-0.0034$ (V1 p.138).
Exhibit 19 (differences): $\hat{b}_0 = -0.2185$ ($t = -1.0200$), $\hat{b}_1 = 0.0287$ ($t = 0.6185$), $R^2 = 0.0008$; residual autocorrelations $-0.0023$, 0.0724, 0.0387, $-0.0062$ (V1 p.139).

Step 1: the level regression looks like a random walk, intercept insignificant and slope near 1, but its t-statistics cannot be trusted because a random walk is not covariance stationary (V1 p.138).
Step 2: if the series is a random walk, the differenced series should give $b_0 = 0$, $b_1 = 0$ and white-noise residuals; with $1/\sqrt{466} = 0.0463$ the largest residual t-statistic is 1.5643, and neither coefficient is significant, which is exactly that signature (V1 p.139).
Step 3, the $R^2$ paradox: 0.9897 for the level model versus 0.0008 for the correct differenced model; a random walk's current value predicts next period's level almost perfectly while changes are unpredictable, so $R^2$ cannot be used to choose between the two (V1 p.139, p.140).
Step 4, investment implication: changes in a random walk are unpredictable, so no strategy that forecasts exchange-rate changes can profit (V1 p.140).
Side calculation: naively applying the mean-reversion formula to the level regression gives $0.8409/(1 - 0.9919) = 103.8$, a number with no meaning because the level series is nonstationary.
^ex-01-05-10

### Example 11: AstraZeneca's quarterly sales (1) (V1 p.141)

Setting: Aron Berglin finds a log-linear trend fits AstraZeneca's quarterly sales better than a linear trend, but DW = 0.7064 rejects uncorrelated errors, so he plans $\ln \text{Sales}_t = b_0 + b_1 \ln \text{Sales}_{t-1} + \varepsilon_t$.
Step 1: before estimating an AR(1) on the log level, he must run a Dickey-Fuller test on the 48 quarterly log observations (2000 to 2011) (V1 p.141).
Step 2: the test might fail to reject the null of a unit root, which would mean the log of sales is not covariance stationary and the AR(1) on levels would be invalid (V1 p.142).
Step 3: the remedy is to model the first-differenced series as an autoregression, which Example 12 does (V1 p.142).
Lesson: a serially correlated trend model does not automatically license an AR(1) on the same series; the unit-root check comes first.
^ex-01-05-11

### Example 12: AstraZeneca's quarterly sales (2) (V1 p.142)

Setting: $y_t = \ln \text{Sales}_t - \ln \text{Sales}_{t-1}$ modelled as AR(1), 48 quarterly observations, January 2000 to December 2011.
Exhibit 22: $\hat{b}_0 = 0.0222$ (s.e. 0.0071, $t = 3.1268$), $\hat{b}_1 = -0.5493$ (s.e. 0.1236, $t = -4.4442$), $R^2 = 0.3005$; residual autocorrelations 0.2809, $-0.0466$, 0.0081, 0.2647 with standard error 0.1443 (V1 p.143).

Step 1, specification: $1/\sqrt{48} = 0.1443$ (Python: 0.14434); the largest residual t-statistic is 1.9466, below the critical value above 2.0 for 46 degrees of freedom, so the model is well specified (V1 p.143, p.144).
Question 1, interpretation: if sales did not change this quarter ($y_t = 0$), sales grow 2.22% next quarter; otherwise growth is 2.22% minus 0.5493 times this quarter's growth, and 2.22% is an exponential growth rate (V1 p.144).
Question 2, forecast 1Q 2012 from 3Q 2011 sales of \$8,405 million and 4Q 2011 sales of \$8,872 million:
$\ln 8{,}405 = 9.0366$; $\ln 8{,}872 = 9.0907$; $y_t = 9.0907 - 9.0366 = 0.0541$.
$\hat{y}_{t+1} = 0.0222 - 0.5493(0.0541) = 0.0222 - 0.0297 = -0.0075$.
$\widehat{\text{Sales}}_{t+1} = 8{,}872 \times e^{-0.0075} = 8{,}872 \times 0.9925 = \$8{,}805$ million (V1 p.144).
Python: $y_t = 0.05407$, $\hat{y}_{t+1} = -0.00750$, sales 8,805.7, matching.
Why sales fall: growth of 5.41% this quarter is far above the mean-reverting growth rate $0.0222/(1 + 0.5493) = 0.0143$, and with a negative $b_1$ the model overshoots below it next quarter.
^ex-01-05-12

### Example 13: AstraZeneca's quarterly sales (3) (V1 p.145)

Setting: four-quarter moving average of sales as of the start of 1Q 2012 from 1Q 2011 to 4Q 2011 sales of 8,490, 8,601, 8,405 and 8,872.
$MA_4 = (8{,}490 + 8{,}601 + 8{,}405 + 8{,}872)/4 = 34{,}368/4 = \$8{,}592$ million (V1 p.145).
Python: 8,592.0.
Contrast with Example 12: the moving average (8,592) is a smoother of the past, not a forecast; the AR(1) forecast (8,805) is a model of the future, and the two are different objects with the same name (V1 p.145, p.147).
^ex-01-05-13

### Example 14: A time-series model for monthly returns on the S&P BSE 100 Index (V1 p.148)

Setting: 168 monthly returns, January 2000 to December 2013; Exhibit 25 autocorrelations 0.1103, $-0.0045$, 0.0327, 0.0370, $-0.0218$, 0.0191, each with standard error 0.0772 (V1 p.149).
Step 1: $1/\sqrt{168} = 0.0772$ (Python: 0.07715); the largest t-statistic is $0.1103/0.0772 = 1.4288$, below the 1.98 critical value (V1 p.148).
Step 2: an MA(q) series would show $q$ significant autocorrelations; none is significant, so $q = 0$ and the returns follow $x_t = \mu + \varepsilon_t$, unpredictable (V1 p.149).
Step 3: an AR(1) would have shown a significant first autocorrelation followed by gradual decay; not even the first is significant, which rules out any AR(p) as well (V1 p.149).
Lesson: the autocorrelations of the series itself, not of residuals, are the tool for choosing between AR and MA and for identifying $q$.
^ex-01-05-14

### Example 15: Seasonality in sales at Starbucks (V1 p.150)

Setting: log-differenced quarterly Starbucks sales, AR(1) without and with a seasonal lag.
Exhibit 26, AR(1) on 72 observations: $\hat{b}_0 = 0.0469$ ($t = 5.8625$), $\hat{b}_1 = -0.4533$ ($t = -4.2404$), $R^2 = 0.2044$; residual autocorrelations 0.0051, $-0.1676$, $-0.0130$, 0.7630 with standard error 0.1179 (V1 p.150, p.151).
Exhibit 27, with seasonal lag on 69 observations: $\hat{b}_0 = 0.0107$ ($t = 1.8136$), $\hat{b}_1 = -0.1540$ ($t = -2.1125$), $\hat{b}_2 = 0.7549$ ($t = 10.4847$), $R^2 = 0.7032$; residual autocorrelations 0.0135, $-0.0171$, 0.1589, $-0.1498$ with standard error 0.1204 (V1 p.152).

Step 1, detect: $1/\sqrt{72} = 0.1179$; the fourth residual autocorrelation has $t = 0.7630/0.1179 = 6.47$, far above 1.99, so the quarterly AR(1) is misspecified by seasonality (V1 p.151).
Step 2, correct: add $(\ln \text{Sales}_{t-4} - \ln \text{Sales}_{t-5})$; the sample shrinks to 69 because five lags are needed and the sample start is fixed (V1 p.151).
Step 3, re-test: $1/\sqrt{69} = 0.1204$; the largest residual t-statistic is 1.3198, so no autocorrelation remains and the F-test is significant at 1% (V1 p.152).
Step 4, interpret and forecast: with constant sales in both reference quarters growth is 1.07%; with 1% growth last quarter and 2% four quarters ago, $0.0107 - 0.1540(0.01) + 0.7549(0.02) = 0.0107 - 0.00154 + 0.015098 = 0.0243$, or 2.43% (V1 p.152).
Python: 0.024258.
Step 5: $R^2$ rose from 0.2044 to 0.7032, more than threefold, because the seasonal lag explains the regular quarterly pattern (V1 p.152).
^ex-01-05-15

### Example 16: Retail sales growth (V1 p.153)

Setting: annualized monthly growth in Canadian furniture and home furnishing store sales, January 1995 to December 2012, 216 observations, AR(1) then AR(1) with the 12th lag (prior observations used for lags, so the sample size does not shrink).
Exhibit 28, AR(1): $\hat{b}_0 = 1.0518$ ($t = 7.7055$), $\hat{b}_1 = -0.2252$ ($t = -3.3865$), $R^2 = 0.0509$; twelfth residual autocorrelation 0.7620, $t = 11.2059$; lags 2, 6, 7 and 10 also significant (V1 p.153, p.154).
Exhibit 29, with seasonal lag: $\hat{b}_0 = 0.2371$ ($t = 2.6344$), $\hat{b}_1 = -0.0792$ ($t = -1.9899$), $\hat{b}_2 = 0.7798$ ($t = 20.0979$), $R^2 = 0.6724$; twelfth residual autocorrelation $-0.1168$, $t = -1.7176$, none of the twelve significant (V1 p.155).

Step 1: $1/\sqrt{216} = 0.0680$; $0.7620/0.0680 = 11.21$ against 1.97 for 214 degrees of freedom, so the seasonal (12th) autocorrelation is significant and the AR(1) is misspecified (V1 p.153).
Step 2: after adding $\text{Sales growth}_{t-12}$ no residual autocorrelation exceeds 1.97 in absolute value, so the model can be used (V1 p.153).
Step 3, forecast: with zero growth last month and 12 months ago, growth is 0.2371, about 23.7% annualized; with 10% last month and 5% a year ago, $0.2371 - 0.0792(0.10) + 0.7798(0.05) = 0.2371 - 0.00792 + 0.03899 = 0.2682$, or 26.8% (V1 p.154).
Python: 0.26817.
Note the monthly analogue of the quarterly rule: the seasonal lag for a monthly series is lag 12, and $R^2$ rose from 0.0509 to 0.6724 (V1 p.153).
^ex-01-05-16

### Example 17: Testing for ARCH(1) in monthly inflation (V1 p.157)

Setting: Miller regresses squared residuals of the AR(1) inflation model on their first lag, for the full sample (286 observations) and the 2008 to 2018 sample (131 observations).
Exhibit 30 (1995 to 2018): $\hat{a}_0 = 6.3626$ ($t = 4.2622$), $\hat{a}_1 = 0.2754$ (s.e. 0.0570, $t = 4.8316$), $R^2 = 0.0759$ (V1 p.157, p.158).
Exhibit 31 (2008 to 2018): $\hat{a}_0 = 6.2082$ ($t = 2.7142$), $\hat{a}_1 = 0.3336$ (s.e. 0.0830, $t = 4.0229$), $R^2 = 0.1113$ (V1 p.158).

Step 1: in both samples the coefficient on the lagged squared residual is significant (t of 4.83 and 4.02), so the errors are ARCH(1) and the t-statistics of the underlying AR(1) models cannot be relied on (V1 p.157, p.158).
Step 2, variance forecast from Exhibit 30: after a 0% error, $6.3626 + 0.2754(0)^2 = 6.3626$; after a 1% error, $6.3626 + 0.2754(1)^2 = 6.6380$ (V1 p.159).
Python: 6.3626 and 6.6380; for a 2% error the forecast would be $6.3626 + 0.2754(4) = 7.4642$.
Step 3, consequences: correct the standard errors with generalized least squares, and use the ARCH equation to forecast the error variance (V1 p.158).
Note the sample sizes: 286 for the ARCH test versus 287 for the AR(1), one observation lost to the lag (V1 p.157).
^ex-01-05-17

### Example 18: Unit roots and the Fisher effect (V1 p.159)

Setting: researchers regress T-bill returns on expected inflation using 181 quarterly observations, 4Q 1968 to 4Q 2013.
Step 1: the regression is valid only if both series are covariance stationary, so run a Dickey-Fuller test on each (V1 p.160).
Step 2: if both null hypotheses of a unit root are rejected, linear regression is appropriate and the Fisher-effect estimates are valid (V1 p.160).
Step 3: if only one series has a unit root the error is nonstationary, the coefficients and standard errors are inconsistent, and the apparent significance would be spurious (V1 p.160).
^ex-01-05-18

### Example 19: Unit roots and predictability of stock market returns by price-to-earnings ratio (V1 p.160)

Setting: Johann de Vries regresses the monthly percentage change in the JSE All Share Index, $(P_t - P_{t-1})/P_{t-1}$, on the lagged P/E, $P_{t-1}/E_{t-2}$, January 1994 to December 2013, and finds a significant negative coefficient and a high $R^2$.
Step 1: before accepting this, test each series for a unit root (V1 p.160).
Step 2: the return series is likely stationary, but the P/E series is documented to be nonstationary; if one series has a unit root the regression is meaningless and cannot support the claim that P/E predicts returns (V1 p.160).
Lesson: a high $R^2$ with a nonstationary regressor is the textbook spurious regression (V1 p.160).
^ex-01-05-19

### Example 20: Testing for cointegration between Intel sales and nominal GDP (V1 p.162)

Setting: test whether $\ln$ Intel sales and $\ln$ GDP are cointegrated, quarterly 1Q 1995 to 4Q 2019.
Step 1: Dickey-Fuller test on each series; if neither rejects the unit root, both are nonstationary and cointegration must be tested (V1 p.162).
Step 2: estimate $\ln \text{Intel sales}_t = b_0 + b_1 \ln \text{GDP}_t + \varepsilon_t$ and run the Engle-Granger Dickey-Fuller test on the residuals (V1 p.162).
Step 3: rejecting the unit root in the residuals rejects "no cointegration", so the series are cointegrated and the regression estimates the long-run relation; failing to reject means the regression is spurious (V1 p.162).
^ex-01-05-20

### Example 21: Unit roots and returns to the Fidelity Select Technology Fund (V1 p.162)

Setting: monthly returns of the fund regressed on S&P 500 Growth and S&P 500 Value returns, October 2015 to August 2019, three time series.
Step 1: Dickey-Fuller test each of the three series (V1 p.162).
Step 2: if all three reject the unit root, multiple regression is valid (V1 p.162).
Step 3: if at least one has a unit root while at least one does not, the error cannot be stationary and the regression should not be used (V1 p.162).
Step 4: if all three have unit roots, test cointegration by a Dickey-Fuller test on the residuals of the multiple regression; even if cointegrated, modelling three cointegrated series is beyond the curriculum and best avoided (V1 p.163).
^ex-01-05-21

## Item-set patterns

> [!warning] Trap 1: the out-of-sample time index
> The vignette gives $\hat{b}_0$, $\hat{b}_1$, a sample of $T$ months ending in month $M$, and asks for the trend forecast two months after $M$.
> Correct: $t = T + 2$; WTI with $T = 181$ and October 2015 two months out gives $t = 183$ and $28.3278 + 0.4086(183) = 103.10$ (V1 p.188).
> Distractor $t = 2$ gives 29.15, tempting because "two months ahead"; distractor $t = T + 1$ or a mid-sample $t$ gives an answer near the current price, tempting because it "looks" plausible (V1 p.171).

> [!warning] Trap 2: forgetting to exponentiate the log-linear forecast
> The log-linear model returns $\ln \hat{y}$; the question asks for the price.
> Correct: $\hat{y} = e^{\hat{b}_0 + \hat{b}_1 t}$; $e^{3.3929 + 0.0075(182)} = e^{4.7579} = 116.50$ (V1 p.188).
> Distractors: 4.76 (the log itself), or a value computed with $t = 1$ or $t = 2$ such as 29.98, which is close to the current price and therefore feels right (V1 p.171).

> [!warning] Trap 3: Durbin-Watson on an AR model
> An exhibit for an AR(1) prints a Durbin-Watson statistic near 2, and an option says "the DW statistic shows the residuals are not serially correlated".
> Correct: DW is invalid when a lagged dependent variable is a regressor; use the residual autocorrelation t-statistics, $t_k = \hat{\rho}_k \sqrt{T}$ (V1 p.124, p.190).
> The DW option is tempting because it is the LM02 habit; the "t-statistic of the slope coefficient" option is tempting because it is significant, but significance of a coefficient says nothing about specification (V1 p.193).

> [!warning] Trap 4: which lag multiplies which coefficient
> An AR(2) or seasonal model with the two most recent observations listed, sometimes in reverse chronological order.
> Correct: $\hat{b}_1$ multiplies the most recent value $x_t$, $\hat{b}_2$ multiplies $x_{t-1}$ (AR(2)) or $x_{t-3}$ (quarterly seasonal forecast for $t + 1$) (V1 p.131, p.167).
> Distractor: swapping the values ($2.0017 + 1.3946(51.16) - 0.4249(42.86) = 55.14$ instead of 40.04); for the seasonal model, using $x_{t-4}$ instead of $x_{t-3}$ (V1 p.188).

> [!warning] Trap 5: mean reversion direction and sign of $b_1$
> "Based on the mean-reverting level, the next forecast is most likely greater than, equal to, or less than the current value."
> Correct: compute $b_0/(1 - b_1)$ and compare with the current value; WTI $1.5948/(1 - 0.9767) = 68.45 > 42.86$, so the forecast rises (V1 p.189).
> Distractors: "equal" (only true at the level itself), and with a negative $b_1$ the level $b_0/(1 + |b_1|)$; candidates who subtract a negative number incorrectly get $-0.0668/0.768 = -0.087$ instead of $-0.0542$ (V1 p.190).

> [!warning] Trap 6: random walk versus stationary, "consistent with both"
> The analyst lists conclusions: variance increases over time, mean-reverting level undefined, $b_0$ not different from zero.
> Correct: only $b_0 = 0$ is consistent with both a random walk and a covariance-stationary series; increasing variance and an undefined level are random-walk-only properties (V1 p.192).
> Each distractor is a true random-walk property, which is why it tempts; the question asks about the intersection, not the union.

> [!warning] Trap 7: reading the differenced regression
> After differencing, nothing is significant and $R^2$ is 0.0017; the option "the model is useless" tempts.
> Correct: insignificant $b_0$, $b_1$ and residual autocorrelations in the differenced regression are the evidence that the differenced series is stationary and the original series had a unit root (V1 p.192).
> Distractor "random walk with drift" is wrong because the intercept of the differenced series is insignificant; "the original series is stationary" is wrong because a stationary original would not need differencing (V1 p.192).

> [!warning] Trap 8: the Dickey-Fuller transformation
> "To perform the unit root test, the analyst should transform the AR(1) by ..."
> Correct: subtract $x_{t-1}$ from both sides, so the dependent variable is $\Delta x_t$ and the slope is $g_1 = b_1 - 1$; test $g_1 = 0$ with Dickey-Fuller critical values (V1 p.141, p.192).
> Distractors: "add a second lag" (that is the fix for residual autocorrelation) and "change the independent variable" (it stays $x_{t-1}$).

> [!warning] Trap 9: seasonal forecast in dollars from five quarters of sales
> Exhibit lists $\text{Sales}_{t-1}$ to $\text{Sales}_{t-5}$ and the seasonal log-differenced coefficients; ask for next quarter's sales.
> Correct: $\hat{y} = b_0 + b_1 \ln(S_{t-1}/S_{t-2}) + b_2 \ln(S_{t-4}/S_{t-5})$, then $S_{t-1} e^{\hat{y}}$; PoweredUP gives 4.231 (V1 p.193).
> Distractors: dropping the seasonal term (3.892), or using $S_{t-1}(1 + \hat{y})$ (4.215, rounds close and is tempting), or mispairing the quarters.

> [!warning] Trap 10: which company's regression on oil is valid
> A table of unit-root, trend, residual-correlation, ARCH and cointegration flags for several stocks and for oil.
> Correct: the regression is valid for the company whose price has a unit root and is cointegrated with oil (both unit roots plus cointegration), for the long-run relation only (V1 p.193).
> Distractors: the company with no unit root (oil has one, so exactly one series has a unit root and the regression is spurious) and the company with a unit root but no cointegration; the ARCH flag is a separate question about predictable error variance (V1 p.193).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM05-Time-Series-Analysis-Practice-Problems]]

## Cross-links

- [[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions]]: the assumption of uncorrelated errors that trend models must satisfy, and why its violation is more damaging when the regressor is a lagged dependent variable (V1 p.112).
- [[LM02-Evaluating-Regression-Model-Fit-and-Interpreting-Model-Results]]: t-tests on coefficients and the meaning of $R^2$ and the standard error of the estimate, which this module reuses for in-sample forecast comparison and warns cannot choose between level and differenced models (V1 p.132, p.140).
- [[LM03-Model-Misspecification]]: the Durbin-Watson test and the consequences of serial correlation and heteroskedasticity for standard errors; this module replaces DW with residual autocorrelation tests for AR models and adds ARCH as time-series heteroskedasticity (V1 p.122, p.124, p.156).
- [[LM04-Extensions-of-Multiple-Regression]]: dummy variables and logistic models are alternatives to seasonal lags for seasonality in cross-section-style specifications; the multiple-regressor unit-root discussion here extends the multiple regression setting (V1 p.162, p.163).
- [[LM06-Machine-Learning]]: out-of-sample validation and the in-sample versus out-of-sample distinction carry directly into training and test sets and the bias-variance trade-off (V1 p.132).
- [[LM06-Backtesting-and-Simulation]] (09-Portfolio-Management): rolling-window backtests and regime shifts are the portfolio version of coefficient instability and the sample-period decision (V1 p.134).
- [[LM02-Economic-Growth]] (02-Economics): log-linear trends and constant growth rates are the statistical form of the steady-state growth models, and the Fisher-effect regression of Example 18 is an economics application that needs unit-root checks (V1 p.117, p.159).

## Self-test

Vignette A (Q1 to Q4): Priya Raman models 60 quarters of a retailer's sales (\$ millions), 1Q 2010 to 4Q 2024.
A log-linear trend gives $\ln \hat{y}_t = 5.2100 + 0.0210 t$, $R^2 = 0.94$, DW = 0.35; the 5% lower critical value $d_l$ is 1.55.
She then fits an AR(1) to $\Delta \ln y_t$ and obtains $\Delta \ln \hat{y}_t = 0.0150 - 0.30 \Delta \ln y_{t-1}$ with no significant residual autocorrelation; the latest observed growth is $\Delta \ln y_{60} = 0.040$.

> [!question] Q1
> The log-linear trend forecast of sales for 2Q 2025 is closest to:
> A. \$6.51 million.
> B. \$659.2 million.
> C. \$673.2 million.

> [!question] Q2
> The quarterly growth rate implied by the log-linear trend is closest to:
> A. 2.10%.
> B. 2.12%.
> C. 2.31%.

> [!question] Q3
> Regarding the log-linear trend model, Raman should conclude that:
> A. the model is adequate because $R^2$ is 0.94.
> B. the residuals are positively serially correlated because DW is below $d_l$.
> C. the residuals are negatively serially correlated because DW is below 2.

> [!question] Q4
> Using the AR(1) on log differences, the two-quarter-ahead forecast of growth and the mean-reverting growth rate are, respectively, closest to:
> A. 0.0030 and 0.0115.
> B. 0.0141 and 0.0115.
> C. 0.0141 and 0.0214.

Vignette B (Q5 to Q7): Tomas Weil fits an AR(1) to 100 month-end levels of a commodity index: $\hat{x}_t = 1.20 + 0.985 x_{t-1}$, with a t-statistic of 150 on the slope and $R^2 = 0.99$.
A Dickey-Fuller regression of $\Delta x_t$ on $x_{t-1}$ gives $\hat{g}_1 = -0.015$ with a t-statistic of $-1.10$; the Dickey-Fuller 5% critical value is $-2.88$.
Residual autocorrelations from the level AR(1) at lags 1 to 4 are 0.05, 0.25, 0.08 and $-0.03$.

> [!question] Q5
> Weil computes a mean-reverting level of 80 for the index. The most appropriate criticism is that:
> A. the arithmetic is wrong; the level is $1.20/0.985 = 1.22$.
> B. the level is meaningless because the Dickey-Fuller test fails to reject a unit root.
> C. the level is valid because the slope is significantly different from zero.

> [!question] Q6
> The residual autocorrelation at lag 2 implies that the level AR(1):
> A. is correctly specified, because 0.25 is below the 1.98 critical value.
> B. is misspecified, because $0.25 \times \sqrt{100} = 2.5$ exceeds 1.98.
> C. cannot be assessed, because residual autocorrelations require the Durbin-Watson statistic.

> [!question] Q7
> The best next step for Weil is to:
> A. add a second lag of the index level and re-estimate.
> B. model $\Delta x_t$ with an AR model and test its residual autocorrelations.
> C. test $H_0: b_1 = 1$ with a conventional t-test, since $t = (0.985 - 1)/0.0066 = -2.3$.

Vignette C (Q8 to Q10): Lena Okafor models quarterly sales of a toy maker with $\Delta \ln S_t = 0.008 - 0.12 \Delta \ln S_{t-1} + 0.70 \Delta \ln S_{t-4} + \varepsilon_t$, all residual autocorrelations insignificant.
Sales (\$ millions): $S_t = 500$, $S_{t-1} = 480$, $S_{t-2} = 470$, $S_{t-3} = 460$, $S_{t-4} = 440$, $S_{t-5} = 400$.
An ARCH test on the residuals gives $\hat{\varepsilon}_t^2 = 0.0004 + 0.35 \hat{\varepsilon}_{t-1}^2$ with a t-statistic of 3.1 on the slope; the latest residual is 0.05.
Separately, she regresses the log of the company's sales on the log of toy-industry sales; both series fail to reject a unit root, and the Engle-Granger Dickey-Fuller test on the residuals rejects a unit root.

> [!question] Q8
> The forecast of next quarter's sales is closest to:
> A. \$517.4 million.
> B. \$519.9 million.
> C. \$536.2 million.

> [!question] Q9
> The forecast of next quarter's error variance and the implication of the ARCH test are, respectively:
> A. 0.001275; the standard errors of the sales model are invalid.
> B. 0.0179; the standard errors of the sales model are invalid.
> C. 0.001275; the sales model must be re-estimated with an additional lag.

> [!question] Q10
> The regression of log company sales on log industry sales:
> A. is spurious because both series have unit roots.
> B. gives consistent estimates of the long-run relation because the series are cointegrated.
> C. is valid only after both series are first-differenced.

> [!success]- Answer key
> Q1: C.
> 2Q 2025 is $t = 62$; $5.2100 + 0.0210(62) = 6.5120$; $e^{6.5120} = 673.2$.
> A is the log itself; B uses $t = 61$ (1Q 2025).
>
> Q2: B.
> $e^{0.0210} - 1 = 0.02122$, or 2.12%.
> A reads $b_1$ as the growth rate without exponentiating; C is $b_1 + b_1^2/2$ misapplied, a plausible-looking but wrong number.
>
> Q3: B.
> DW = 0.35 is below $d_l = 1.55$, so the null of no positive serial correlation is rejected; a small DW means positive correlation (V1 p.122).
> A ignores the assumption violation, the Starbucks lesson (V1 p.119).
> C has the direction backwards; negative serial correlation gives DW above 2.
>
> Q4: B.
> One ahead: $0.0150 - 0.30(0.040) = 0.0030$; two ahead: $0.0150 - 0.30(0.0030) = 0.0141$.
> Mean-reverting growth: $0.0150/(1 + 0.30) = 0.01154$.
> A reports the one-period forecast; C uses $1 - 0.30$ in the denominator, the sign error of Trap 5.
>
> Q5: B.
> $1.20/(1 - 0.985) = 80$ is arithmetically right, but the Dickey-Fuller t-statistic of $-1.10$ is not below $-2.88$, so the unit root is not rejected and the level series is nonstationary; the AR(1) and its level are meaningless (V1 p.137, p.141).
> A divides by $b_1$ instead of $1 - b_1$.
> C uses the significance of $b_1$, which is invalid for a nonstationary series (V1 p.138).
>
> Q6: B.
> Standard error $1/\sqrt{100} = 0.10$; $t = 0.25/0.10 = 2.5 > 1.98$, so the residuals are serially correlated (V1 p.125).
> A compares the autocorrelation itself with the critical value instead of its t-statistic.
> C inverts the rule: DW is the invalid tool for AR models (V1 p.124).
>
> Q7: B.
> The level series has a unit root, so first-difference it and model the stationary differences with an AR, testing residual autocorrelations (V1 p.142).
> A adds a lag to a nonstationary regression, which cannot fix nonstationarity.
> C is the invalid conventional t-test of $b_1 = 1$ (V1 p.141).
>
> Q8: A.
> $\Delta \ln S_t = \ln(500/480) = 0.04082$; the seasonal term for period $t+1$ is $\Delta \ln S_{t-3} = \ln(460/440) = 0.04445$.
> $\hat{y} = 0.008 - 0.12(0.04082) + 0.70(0.04445) = 0.008 - 0.00490 + 0.03112 = 0.03422$; $500 e^{0.03422} = 517.4$.
> B drops the lag-1 term ($0.008 + 0.03112 = 0.03912$, giving 519.9).
> C uses $\Delta \ln S_{t-4} = \ln(440/400) = 0.09531$ as the seasonal input, the wrong quarter (V1 p.167).
>
> Q9: A.
> $\hat{\sigma}_{t+1}^2 = 0.0004 + 0.35(0.05)^2 = 0.0004 + 0.35(0.0025) = 0.001275$.
> The slope t-statistic of 3.1 is significant, so the errors are ARCH(1) and the sales model's standard errors are not correct; the fix is generalized least squares, not another lag (V1 p.158).
> B forgets to square the residual; C prescribes the wrong remedy.
>
> Q10: B.
> Both series have unit roots and the Engle-Granger test rejects a unit root in the residuals, so the series are cointegrated and the coefficients are consistent for the long-run relation (V1 p.161).
> A would be true only if the residual test had failed to reject.
> C differences away the long-run relation; differencing is the remedy for a single unit-root series, not for a cointegrated pair.

## Flashcards

#flashcards/cfa-l2/01-Quantitative-Methods/lm05

Linear trend model::$y_t = b_0 + b_1 t + \varepsilon_t$; the series changes by the constant amount $b_1$ each period (V1 p.113)

Log-linear trend model and its level forecast::$\ln y_t = b_0 + b_1 t + \varepsilon_t$; $\hat{y}_t = e^{\hat{b}_0 + \hat{b}_1 t}$ (V1 p.117)

Growth rate implied by log-linear slope $b_1$::$e^{b_1} - 1$ per period, constant; $b_1 = 0.05$ gives 5.13% (V1 p.117)

When to choose a linear versus a log-linear trend::Constant amount of change, linear; constant rate of growth (exponential), log-linear (V1 p.166)

How trend models fail::Residuals persistently above or below the line, which is serial correlation; test with Durbin-Watson, reject if DW is below $d_l$ (V1 p.122)

Three conditions for covariance stationarity::Constant finite mean; constant finite variance; constant finite covariance with itself at each fixed lag (V1 p.123)

Consequence of running AR(1) on a nonstationary series::Spurious results; $\hat{b}_1$ biased and hypothesis tests invalid (V1 p.123)

AR(p) model::$x_t = b_0 + b_1 x_{t-1} + \dots + b_p x_{t-p} + \varepsilon_t$ (V1 p.123)

Why Durbin-Watson is invalid for AR models::A lagged dependent variable is among the regressors; test residual autocorrelations instead (V1 p.124)

Standard error of a residual autocorrelation::$1/\sqrt{T}$, the same at every lag; t-statistic is $\hat{\rho}_k \sqrt{T}$ (V1 p.125)

Three-step check that an AR model fits::Estimate the AR, compute residual autocorrelations, test each against zero; any significant lag means misspecification (V1 p.125)

Mean-reverting level of an AR(1)::$b_0/(1 - b_1)$; forecast rises below it and falls above it (V1 p.128)

Chain rule of forecasting::$\hat{x}_{t+2} = \hat{b}_0 + \hat{b}_1 \hat{x}_{t+1}$, substituting the one-period forecast (V1 p.128)

Why multi-period forecasts are less certain::Each forecast period adds its own uncertainty, so the forecast variance rises with the horizon (V1 p.128)

In-sample versus out-of-sample forecast errors::In-sample errors are the residuals of the fitted model; out-of-sample errors are actual minus forecast beyond the estimation period (V1 p.132)

RMSE definition and decision rule::Square root of the average squared forecast error; smaller out-of-sample RMSE means the more accurate model (V1 p.132)

Random walk equation and its AR(1) parameters::$x_t = x_{t-1} + \varepsilon_t$; $b_0 = 0$, $b_1 = 1$ (V1 p.137)

Best forecast from a random walk::The current value, at every horizon (V1 p.137)

Variance of a random walk after t periods::$(t - 1)\sigma^2$, unbounded, so not covariance stationary (V1 p.137)

Mean-reverting level of a random walk::$0/0$, undefined (V1 p.137)

First difference of a random walk::$y_t = \varepsilon_t$, an AR(1) with $b_0 = b_1 = 0$, level 0, variance $\sigma^2$, stationary (V1 p.137)

Random walk with drift::$x_t = b_0 + x_{t-1} + \varepsilon_t$, $b_1 = 1$, $b_0 \ne 0$; differenced, $\Delta x_t = b_0 + \varepsilon_t$ (V1 p.140)

Unit root, explosive root::$|b_1| = 1$ is a unit root (random walk); $|b_1| > 1$ is explosive (V1 p.141)

Why not t-test $b_1 = 1$ directly::Under the null the series is nonstationary and the t-statistic does not follow the t-distribution (V1 p.141)

Dickey-Fuller regression and hypotheses::$\Delta x_t = b_0 + g_1 x_{t-1} + \varepsilon_t$, $g_1 = b_1 - 1$; $H_0: g_1 = 0$ (unit root), $H_a: g_1 < 0$; DF critical values, larger in absolute value (V1 p.141)

Why R-squared cannot compare level and differenced models::A random walk's level regression has near-1 $R^2$ while the correct differenced model has near-0 $R^2$ (V1 p.140)

n-period moving average::$(x_t + x_{t-1} + \dots + x_{t-(n-1)})/n$; smooths but lags large moves (V1 p.145, p.147)

MA(1) model::$x_t = \varepsilon_t + \theta \varepsilon_{t-1}$; only the first autocorrelation is nonzero (V1 p.147, p.148)

Distinguishing AR from MA by autocorrelations::AR: start large and decay gradually; MA(q): first $q$ nonzero then cut to zero (V1 p.148)

Result for S&P BSE 100 monthly returns::No significant autocorrelations, so MA(0): $x_t = \mu + \varepsilon_t$, unpredictable (V1 p.149)

Seasonal lag for quarterly and monthly data::Lag 4 and lag 12; detected as a significant residual autocorrelation at that lag (V1 p.150, p.153)

Forecast from quarterly AR(1) with seasonal lag made at t for t+1::$\hat{b}_0 + \hat{b}_1 x_t + \hat{b}_2 x_{t-3}$ (V1 p.167)

Level forecast from a log-differenced model::$\widehat{\text{Sales}}_{t+1} = \text{Sales}_t \, e^{\hat{y}_{t+1}}$; $\hat{y}$ is a continuously compounded growth rate (V1 p.144)

ARMA limitations::Unstable parameters; choosing $p$ and $q$ is more art than science; may forecast poorly; not for fewer than 80 observations (V1 p.156)

ARCH(1) error process::$\varepsilon_t \sim N(0, a_0 + a_1 \varepsilon_{t-1}^2)$; $a_1 > 0$ means a large error raises next period's variance (V1 p.156, p.157)

ARCH(1) test regression::$\hat{\varepsilon}_t^2 = a_0 + a_1 \hat{\varepsilon}_{t-1}^2 + u_t$; significant $\hat{a}_1$ means ARCH (V1 p.157)

Consequences of ARCH errors::Standard errors of the model are wrong, so correct with generalized least squares; error variance becomes predictable (V1 p.158)

ARCH(1) variance forecast::$\hat{\sigma}_{t+1}^2 = \hat{a}_0 + \hat{a}_1 \hat{\varepsilon}_t^2$; square the error first (V1 p.157)

Two series, neither has a unit root::Linear regression is valid (V1 p.159)

Two series, exactly one has a unit root::Error nonstationary, coefficients inconsistent, regression spurious; do not use (V1 p.160)

Two series, both have unit roots::Usable only if cointegrated; test with Engle-Granger Dickey-Fuller on the residuals (V1 p.161)

Definition of cointegration::A long-term economic relationship keeps two unit-root series from diverging without bound, for example a shared trend (V1 p.161)

Engle-Granger steps::Regress $y_t$ on $x_t$; DF test on the residuals with Engle-Granger critical values; reject unit root means cointegrated, consistent long-run coefficients (V1 p.161)

Cointegrated regression caveat::Estimates the long-run relation but may be a poor model of the short run (V1 p.161)

Transformation for a linear trend, and for an exponential trend::Linear trend, first-difference; exponential trend, take logs then first-difference (V1 p.164)

Handling a regime shift in the sample::Estimate separate models before and after the shift (V1 p.164, p.134)

Which trap: analyst says forecast equals current value because the series is at its mean::Only true if the current value equals $b_0/(1 - b_1)$ exactly; otherwise compare and state the direction (V1 p.128)

Which trap: DW near 2 proves AR residuals are uncorrelated::DW is invalid for AR models; only residual autocorrelation t-statistics count (V1 p.190)

Which trap: "consistent with both random walk and stationarity"::Only $b_0 = 0$; increasing variance and undefined level are random-walk-only (V1 p.192)

Which trap: Dickey-Fuller transformation::Subtract $x_{t-1}$ from both sides; not "add a lag", not "change the regressor" (V1 p.192)

Micro-problem: $b_0 = 2$, $b_1 = 0.6$, $x_t = 10$; one- and two-period forecasts?::$2 + 0.6(10) = 8$; $2 + 0.6(8) = 6.8$; keystrokes `0.6 x 10 + 2 =` then `x 0.6 + 2 =` (V1 p.128)

Micro-problem: $b_0 = 2$, $b_1 = 0.6$; mean-reverting level?::$2/(1 - 0.6) = 5$; keystrokes `1 - 0.6 = 1/x x 2 =` (V1 p.128)

Micro-problem: $\ln \hat{y} = 3 + 0.02 t$, $t = 50$; level forecast?::$e^{4} = 54.60$; keystrokes `0.02 x 50 + 3 = 2nd LN` (V1 p.117)

Micro-problem: out-of-sample errors 1, $-2$, 2, $-1$; RMSE?::$\sqrt{(1 + 4 + 4 + 1)/4} = \sqrt{2.5} = 1.581$ (V1 p.132)

Micro-problem: $T = 64$; standard error of residual autocorrelations, and is 0.26 at lag 3 significant?::$1/8 = 0.125$; $t = 0.26/0.125 = 2.08 > 1.99$, significant, misspecified (V1 p.125)

Micro-problem: ARCH $a_0 = 2$, $a_1 = 0.3$, $\hat{\varepsilon}_t = 3$; next variance?::$2 + 0.3(9) = 4.7$ (V1 p.157)

Micro-problem: $\Delta \ln S_t = -0.0075$, $S_t = 8{,}872$; $S_{t+1}$?::$8{,}872 e^{-0.0075} = 8{,}805$; keystrokes `0.0075 +/- 2nd LN x 8872 =` (V1 p.144)

Nine suggested steps, compressed
?
Choose regression or time-series; plot for stationarity; try a trend and DW-test it; transform (difference, log-difference, split sample, seasonal lags); AR(1) and residual test; raise the order until clean; seasonal lag check; ARCH test; out-of-sample RMSE (V1 p.164, p.165)

{{Stationarity in the past}} does not guarantee {{stationarity in the future}}; a regime change can invalidate a correctly specified model (V1 p.124)

## Common mistakes

1. Using $t = k$ (periods ahead) instead of $t = T + k$ in a trend forecast, which turns \$103.10 into \$29.15 (V1 p.188).
2. Reporting $\ln \hat{y}$ instead of $e^{\ln \hat{y}}$ from a log-linear model, or reading $b_1$ as the growth rate instead of $e^{b_1} - 1$ (V1 p.117, p.188).
3. Trusting a high $R^2$ or a large coefficient t-statistic as evidence of a good model when the residuals are serially correlated; Starbucks' linear trend had $R^2 = 0.96$ and was rejected (V1 p.119).
4. Interpreting a Durbin-Watson statistic in an AR regression; DW is invalid once a lagged dependent variable is a regressor (V1 p.124, p.190).
5. Comparing a residual autocorrelation directly with the critical value instead of dividing by $1/\sqrt{T}$ first, or using the wrong $T$ (the regression's observation count, 180 not 181) (V1 p.188).
6. Mishandling a negative $b_1$ in $b_0/(1 - b_1)$, subtracting $|b_1|$ instead of adding it (V1 p.190).
7. Swapping which observation multiplies $b_1$ and which multiplies $b_2$ in an AR(2), or using $x_{t-4}$ instead of $x_{t-3}$ in the seasonal forecast for $t + 1$ (V1 p.188, p.167).
8. Treating the near-1 slope and t-statistic of 211 in a level regression as proof of anything; standard errors are invalid when the series is a random walk (V1 p.138).
9. Choosing between a level model and a differenced model by $R^2$ (0.9897 versus 0.0008), which favors the invalid model (V1 p.140).
10. Testing for a unit root with a conventional t-test of $b_1 = 1$, or describing the Dickey-Fuller transformation as "add a lag" (V1 p.141, p.192).
11. Listing "increasing variance" or "undefined mean-reverting level" as consistent with a stationary series; only $b_0 = 0$ is shared with the random walk (V1 p.192).
12. Forgetting that log-differenced coefficients are continuously compounded growth rates, so dollar forecasts need $S_t e^{\hat{y}}$ and percent inputs need $\ln(1 + g)$ (V1 p.144, p.194).
13. Not squaring the residual in the ARCH variance forecast, or claiming ARCH is fixed by adding another AR lag rather than by correcting the standard errors (V1 p.157, p.158).
14. Regressing one time series on another without unit-root tests, or concluding "both have unit roots, so the regression is spurious" without the cointegration test (V1 p.160, p.161).
15. Relying on residual autocorrelations to pick the sample period; they cannot detect a regime change, judgment about policy shifts must (V1 p.136).
16. Extrapolating a short-horizon AR model many periods ahead into economically impossible territory, such as negative unemployment (V1 p.192).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "01-05" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
