---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 5
title: "Skyline Air Fuel Hedge Diagnostics"
los: [los-01-05-n, los-01-05-c, los-01-05-d, los-01-05-m, los-01-05-o]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Skyline Air Fuel Hedge Diagnostics

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Priyanka Nair is a treasury analyst at Skyline Air, a listed mid-sized airline that is redesigning its fuel hedging program.
Because jet fuel swaps are illiquid beyond six months, Skyline hedges longer exposures with Brent crude oil futures and needs a regression of jet fuel prices on Brent prices to set the hedge ratio.
Nair assembles 180 month-end observations from January 2010 through December 2024 and tests each series for a unit root.

Exhibit 1: Dickey-Fuller unit root tests (5% critical value $-2.88$)

| Series | Dickey-Fuller t-statistic |
|---|---|
| ln(jet fuel price) | $-1.62$ |
| ln(Brent price) | $-1.48$ |
| ln(Skyline share price) | $-1.95$ |
| Jet crack spread (jet fuel minus Brent, \$ per barrel) | $-4.11$ |
| Monthly change in ln(Brent price) | $-12.30$ |

She then estimates three regressions and, where appropriate, tests their residuals.

Exhibit 2: Regressions on ln(Brent price)

| Regression | Dependent variable | $R^2$ | Engle-Granger residual test statistic |
|---|---|---|---|
| A | ln(jet fuel price) | 0.9612 | $-4.36$ |
| B | ln(Skyline share price) | 0.5820 | $-2.21$ |
| C | Jet crack spread | 0.4105 | not computed |

The 5% Engle-Granger critical value for two variables is $-3.34$.

To budget for the refining margin embedded in unhedged jet fuel, Nair models the crack spread directly.

Exhibit 3: AR(1) model of the jet crack spread (179 observations)

| Item | Coefficient | t-statistic |
|---|---|---|
| Intercept | 4.12 | 4.95 |
| Crack spread$_{t-1}$ | 0.7640 | 15.87 |

No residual autocorrelation at lags 1 to 12 has a t-statistic above 1.10 in absolute value.
The sample mean of the crack spread is \$17.52 per barrel, and the December 2024 value is \$21.40 per barrel.
An ARCH(1) regression of the squared AR(1) residuals gives $\hat{\varepsilon}_t^2 = 1.85 + 0.38\,\hat{\varepsilon}_{t-1}^2$, with t-statistics of 4.10 and 5.60, and the December 2024 residual is $-2.60$.

On 20 January 2025 Nair and her colleague Marcus Leung discuss the hedge regression.

Leung: "Because ln(jet fuel) and ln(Brent) each have a unit root, Regression A is spurious; we should first-difference both series before we estimate any hedge ratio."

Nair: "The Engle-Granger residual test settles the question, and we can evaluate it with the standard Dickey-Fuller critical value from Exhibit 1."

Leung is also building a model to time Skyline's share buybacks.
He proposes to fit an AR(1) model directly to ln(Skyline share price).
Nair instead fits an AR(1) model to the monthly first difference of ln(Skyline share price) and finds significant residual autocorrelations at lag 1 (t-statistic 2.84) and lag 2 ($-2.31$), with no significant autocorrelation at lag 12.
An AR(2) model of the same first-differenced series leaves no significant residual autocorrelation at any lag, and an ARCH test on its residuals is insignificant.

## Questions

1. Based on Exhibits 1 and 2, which regression is most likely to yield valid coefficients for estimating the long-run relationship between the two variables? (LOS: los-01-05-n)
   - A. Regression A
   - B. Regression B
   - C. Regression C
2. Regarding the statements made on 20 January 2025: (LOS: los-01-05-n)
   - A. Leung is correct and Nair is incorrect.
   - B. both Leung and Nair are incorrect.
   - C. Nair is correct, because $-4.36$ is below the Dickey-Fuller critical value of $-2.88$.
3. If Leung fits his proposed AR(1) model to ln(Skyline share price), the most likely consequence is that: (LOS: los-01-05-c)
   - A. the model is valid provided its residual autocorrelations are insignificant.
   - B. the coefficient estimates are unbiased, but the $R^2$ understates the explanatory power of the model.
   - C. the slope estimate is biased and the hypothesis tests are invalid, because the series is not covariance stationary.
4. Using Exhibit 3, the forecasted crack spread for February 2025 is closest to: (LOS: los-01-05-d)
   - A. \$16.61 per barrel.
   - B. \$17.49 per barrel.
   - C. \$19.76 per barrel.
5. Using the ARCH(1) results, the forecasted standard deviation of the January 2025 crack-spread error is closest to: (LOS: los-01-05-m)
   - A. \$1.68 per barrel.
   - B. \$2.10 per barrel.
   - C. \$4.42 per barrel.
6. The most appropriate model for Leung's buyback timing analysis of Skyline's share price is: (LOS: los-01-05-o)
   - A. an AR(2) model of ln(Skyline share price).
   - B. an AR(1) model of the first difference of ln(Skyline share price) with a lag-12 seasonal term.
   - C. an AR(2) model of the first difference of ln(Skyline share price).

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** ln(jet fuel) and ln(Brent) both fail to reject a unit root ($-1.62$ and $-1.48$ are not below $-2.88$), so the regression is usable only if they are cointegrated.
> The Engle-Granger statistic of $-4.36$ is below $-3.34$, so the unit root in the residuals is rejected, the error is stationary, and the series are cointegrated.
> B is wrong because ln(Skyline share price) and ln(Brent) both have unit roots but $-2.21$ is not below $-3.34$, so they are not cointegrated and the regression is spurious despite an $R^2$ of 0.58.
> C is wrong because the crack spread is stationary ($-4.11 < -2.88$) while ln(Brent) has a unit root; when exactly one series has a unit root the error cannot be stationary and the coefficients are inconsistent.
>
> 2. **B.** Leung is wrong because two unit-root series can be regressed on each other when they are cointegrated, and Regression A passes that test; the coefficients are then consistent for the long-run relationship, although the regression may be a poor model of short-run dynamics.
> First-differencing both series would discard exactly the long-run relationship the hedge ratio is meant to capture.
> Nair is wrong because the residuals depend on estimated coefficients, so the test must use Engle-Granger critical values ($-3.34$), not standard Dickey-Fuller values ($-2.88$).
> A is wrong because Leung's rule ignores cointegration.
> C is wrong because it reaches the right conclusion about cointegration with the wrong critical value; with a statistic between $-2.88$ and $-3.34$ the two approaches would disagree.
>
> 3. **C.** ln(Skyline share price) has a unit root ($-1.95$ is not below $-2.88$), so it does not have a constant, finite mean and variance.
> An AR model estimated on a nonstationary series has a biased slope estimate and invalid hypothesis tests; the series should be first-differenced before an AR model is fitted.
> A is wrong because clean residual autocorrelations do not cure nonstationarity; the specification test assumes the series is stationary.
> B is wrong because the problem is biased estimates and invalid inference, not an understated $R^2$ (a nonstationary level regression typically shows a very high $R^2$).
>
> 4. **C.** The crack spread is stationary, so the AR(1) is valid and the chain rule applies.
> January: $4.12 + 0.7640(21.40) = 4.12 + 16.3496 = 20.4696$.
> February: $4.12 + 0.7640(20.4696) = 4.12 + 15.6388 = 19.7588$, or about \$19.76.
> Both forecasts fall toward the mean-reverting level $4.12/(1 - 0.7640) = 17.4576$, because December's 21.40 is above it.
> A is wrong because it chains the slope but not the intercept: $4.12 + 0.7640^2(21.40) = 4.12 + 0.583696(21.40) = 16.6111$.
> B is wrong because it starts the chain from the sample mean of 17.52 rather than from the last observation, 21.40: $4.12 + 0.7640(17.52) = 17.5053$, then $4.12 + 0.7640(17.5053) = 17.4940$, or about \$17.49.
>
> 5. **B.** The slope t-statistic of 5.60 is significant, so the errors are ARCH(1) and the variance is predictable.
> $\hat{\sigma}^2_{t+1} = 1.85 + 0.38(-2.60)^2 = 1.85 + 0.38(6.7600) = 1.85 + 2.5688 = 4.4188$, and the standard deviation is $\sqrt{4.4188} = 2.1021$.
> Because of the ARCH effect, the AR(1) standard errors in Exhibit 3 are also unreliable and should be corrected, for example with generalized least squares.
> A is wrong because it uses the absolute residual instead of its square: $\sqrt{1.85 + 0.38(2.60)} = \sqrt{2.8380} = 1.68$.
> C is wrong because it reports the variance, 4.42, as if it were the standard deviation.
>
> 6. **C.** The log share price has a unit root, so it is first-differenced; the AR(1) on the differences leaves significant residual autocorrelation at lags 1 and 2, so the order is raised to AR(2), which leaves clean residuals and no ARCH.
> A is wrong because an AR model of the undifferenced log price is invalid when the series has a unit root, whatever its lag order.
> B is wrong because there is no evidence of seasonality (lag 12 is insignificant), and a seasonal term does not address the lag-2 autocorrelation.

## Distractor design

1. B: both unit roots treated as sufficient without cointegration; C: exactly one series with a unit root, spurious regression.
2. A: differencing discards a cointegrated long-run relation; C: standard Dickey-Fuller critical value instead of Engle-Granger.
3. A: residual tests assumed to cure nonstationarity; B: misstates the consequence of nonstationarity.
4. A: intercept dropped from the chained forecast; B: chain started from the sample mean instead of the last observation.
5. A: residual not squared; C: variance reported instead of standard deviation.
6. A: ignores the unit root; B: wrong remedy (seasonal lag) for nonseasonal residual autocorrelation.
