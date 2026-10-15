---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 5
title: "Northgate Mutual Credit Spread Models"
los: [los-01-05-d, los-01-05-e, los-01-05-f, los-01-05-g, los-01-05-h, los-01-05-m]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Northgate Mutual Credit Spread Models

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tobias Brandt is a quantitative analyst in the asset-liability management group of Northgate Mutual Insurance.
The group sets reinvestment assumptions for the insurer's general account using a forecast of the monthly average option-adjusted spread of its BBB corporate bond benchmark, measured in percentage points.
The forecast feeds the reinvestment yield assumed in the insurer's cash-flow testing, so an error of even ten basis points in the projected spread changes the reserve margin reported to the board.
Brandt has 156 monthly observations from January 2012 through December 2024, and a unit root test rejects nonstationarity for the spread over this sample.
He must recommend a single model to the investment committee and document why it is preferred, including how its forecast uncertainty will be measured.
He estimates two autoregressive models.

Exhibit 1: Autoregressive models of the BBB spread, January 2012 to December 2024

| Statistic | AR(1) | AR(2) |
|---|---|---|
| Observations | 155 | 154 |
| Intercept (t-statistic) | 0.1860 (3.12) | 0.2105 (3.48) |
| Spread$_{t-1}$ (t-statistic) | 0.8710 (22.46) | 1.0620 (13.27) |
| Spread$_{t-2}$ (t-statistic) | | $-0.2080$ ($-2.61$) |
| $R^2$ | 0.7671 | 0.7768 |
| Standard error of regression | 0.0912 | 0.0889 |
| Durbin-Watson statistic | 1.94 | 1.99 |
| Residual autocorrelation, lag 1 | 0.0410 | 0.0120 |
| Residual autocorrelation, lag 2 | $-0.1920$ | $-0.0310$ |
| Residual autocorrelation, lag 3 | 0.0650 | 0.0540 |
| Residual autocorrelation, lag 4 | $-0.0380$ | $-0.0290$ |

The critical t-value at the 5% level is 1.98 for both regressions.

Exhibit 2: Recent month-end spreads (percentage points)

| Month | Spread |
|---|---|
| October 2024 | 1.31 |
| November 2024 | 1.26 |
| December 2024 | 1.18 |

After the data become available, Brandt compares the two models out of sample over the first half of 2025.

Exhibit 3: Out-of-sample forecast errors, actual minus forecast (percentage points)

| Month (2025) | AR(1) error | AR(2) error |
|---|---|---|
| January | 0.06 | 0.07 |
| February | $-0.09$ | $-0.05$ |
| March | 0.11 | 0.09 |
| April | $-0.04$ | $-0.06$ |
| May | 0.08 | 0.04 |
| June | $-0.05$ | $-0.03$ |

Finally, he regresses the squared residuals of the AR(2) model on their first lag.

Exhibit 4: ARCH(1) test on AR(2) residuals

| Item | Coefficient | t-statistic |
|---|---|---|
| Intercept, $\hat{a}_0$ | 0.0041 | 3.37 |
| Lagged squared residual, $\hat{a}_1$ | 0.4150 | 5.02 |

The AR(2) residual for December 2024 is $-0.12$.

Brandt circulates a memo on 3 February 2025: "The AR(2) is my preferred model because its residual autocorrelations are insignificant and its in-sample standard error is lower.
Out-of-sample testing will simply confirm what the in-sample evidence already shows."

Lucia Ferrante, head of the group, replies on 4 February 2025: "We should extend the sample back to January 2005, which adds 84 observations and includes the 2008 to 2009 crisis.
More data always produces more reliable coefficients, and if the residual autocorrelations of the longer-sample model are insignificant, pooling the two periods is justified."

Brandt notes that the standard deviation of the monthly spread was 1.02 percentage points over 2005 to 2011 and 0.29 percentage points over 2012 to 2024.

## Questions

1. Based on Exhibit 1, Brandt should conclude that the AR(1) model is: (LOS: los-01-05-e)
   - A. correctly specified, because its Durbin-Watson statistic of 1.94 is close to 2.
   - B. correctly specified, because every residual autocorrelation is smaller in absolute value than 1.98.
   - C. misspecified, because the t-statistic of the second-lag residual autocorrelation is about $-2.39$.
2. Using the AR(2) model, the forecasted spread for February 2025 is closest to: (LOS: los-01-05-d)
   - A. 1.2016.
   - B. 1.2411.
   - C. 1.3324.
3. The mean-reverting level implied by the AR(2) model, and the direction of the one-month-ahead forecast relative to December 2024, are closest to: (LOS: los-01-05-f)
   - A. 1.44; the spread is forecast to widen.
   - B. 1.44; the spread is forecast to narrow.
   - C. 0.21; the spread is forecast to narrow.
4. Based on Exhibit 3, the out-of-sample root mean squared error of the AR(2) model is closest to: (LOS: los-01-05-g)
   - A. 0.0036.
   - B. 0.0600.
   - C. 0.0657.
5. Ferrante's reply of 4 February 2025 is best described as: (LOS: los-01-05-h)
   - A. correct.
   - B. incorrect, because the estimation sample should be covariance stationary, the change in spread volatility suggests two regimes, and residual autocorrelations cannot reveal a regime change.
   - C. incorrect, because a longer sample always requires a higher-order autoregression, which reduces forecast accuracy.
6. Based on Exhibit 4, the forecasted variance of the January 2025 AR(2) error and the most appropriate response are: (LOS: los-01-05-m)
   - A. 0.0101; the AR(2) standard errors are unreliable and should be corrected, for example with generalized least squares.
   - B. 0.0539; the AR(2) standard errors are unreliable and should be corrected, for example with generalized least squares.
   - C. 0.0101; a third lag of the spread should be added to remove the ARCH effect.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The standard error of each residual autocorrelation is $1/\sqrt{155} = 0.0803$.
> The second-lag t-statistic is $-0.1920/0.0803 = -0.1920 \times \sqrt{155} = -2.39$, which exceeds 1.98 in absolute value, so the AR(1) residuals are serially correlated and the model is misspecified.
> A is wrong because the Durbin-Watson statistic is invalid when a lagged dependent variable is a regressor.
> B is wrong because it compares the raw autocorrelations, not their t-statistics, with the critical value.
>
> 2. **B.** The most recent value (December, 1.18) multiplies $\hat{b}_1$ and the one before it (November, 1.26) multiplies $\hat{b}_2$.
> January: $0.2105 + 1.0620(1.18) - 0.2080(1.26) = 0.2105 + 1.2532 - 0.2621 = 1.2016$.
> February by the chain rule, with the January forecast now the most recent value and December the lagged value: $0.2105 + 1.0620(1.2016) - 0.2080(1.18) = 0.2105 + 1.2761 - 0.2454 = 1.2411$.
> A is wrong because it is the one-month-ahead forecast for January.
> C is wrong because it swaps the lags: $0.2105 + 1.0620(1.26) - 0.2080(1.18) = 1.3032$, then $0.2105 + 1.0620(1.3032) - 0.2080(1.26) = 1.3324$.
>
> 3. **A.** At the mean-reverting level all lagged values equal $x^*$, so $x^* = \hat{b}_0/(1 - \hat{b}_1 - \hat{b}_2) = 0.2105/(1 - 1.0620 + 0.2080) = 0.2105/0.1460 = 1.4418$.
> The December spread of 1.18 is below 1.44, so the model forecasts a widening, consistent with the 1.2016 forecast for January.
> The misspecified AR(1) gives a nearly identical level, $0.1860/(1 - 0.8710) = 1.4419$, which is a useful check.
> B is wrong because it reverses the direction: a series below its mean-reverting level is forecast to rise.
> C is wrong because it treats the intercept as the long-run level.
>
> 4. **B.** Squared AR(2) errors: 0.0049, 0.0025, 0.0081, 0.0036, 0.0016, 0.0009; sum 0.0216; mean $0.0216/6 = 0.0036$; RMSE $= \sqrt{0.0036} = 0.0600$.
> For comparison the AR(1) RMSE is $\sqrt{0.0343/6} = 0.0756$, so the AR(2) is more accurate out of sample as well as in sample.
> Brandt's memo still overstates the case: in-sample fit does not guarantee out-of-sample accuracy, which is why the out-of-sample test is needed rather than a formality.
> A is wrong because it is the mean squared error without the square root.
> C is wrong because it divides by $n - 1 = 5$: $\sqrt{0.0216/5} = 0.0657$.
>
> 5. **B.** Coefficients of time-series models are often unstable across sample periods, and a model is only valid on a sample that is covariance stationary.
> The spread's standard deviation was $1.02/0.29 = 3.52$ times higher in 2005 to 2011, evidence of a different regime, so pooling the periods is likely to produce a misspecified model.
> Residual autocorrelations from the pooled model cannot detect the regime change; that requires judgment about the economic environment.
> A is wrong because more data helps only when the added data come from the same stationary process.
> C is wrong because there is no rule that a longer sample requires a higher order; the concern is stationarity, not lag length.
>
> 6. **A.** The t-statistic of 5.02 on $\hat{a}_1$ is significant, so the AR(2) errors exhibit ARCH(1).
> $\hat{\sigma}^2_{t+1} = 0.0041 + 0.4150(-0.12)^2 = 0.0041 + 0.4150(0.0144) = 0.0041 + 0.0060 = 0.0101$.
> ARCH means the AR(2) coefficient standard errors and t-tests are not reliable, so they should be corrected, for example with generalized least squares, while the ARCH equation can be used to forecast the error variance.
> B is wrong because it uses the absolute residual instead of its square: $0.0041 + 0.4150(0.12) = 0.0539$.
> C is wrong because ARCH is conditional heteroskedasticity, not residual autocorrelation in levels, so adding a lag does not correct it.

## Distractor design

1. A: applies the Durbin-Watson test to an AR model; B: compares raw autocorrelations with the critical value.
2. A: stops at the one-period forecast; C: swaps which observation multiplies $\hat{b}_1$ and $\hat{b}_2$.
3. B: reverses the mean-reversion direction; C: reads the intercept as the mean-reverting level.
4. A: omits the square root (MSE, not RMSE); C: wrong divisor ($n - 1$ instead of $n$).
5. A: assumes more data is always better; C: invents a link between sample length and model order.
6. B: residual not squared in the variance forecast; C: right number, wrong remedy for ARCH.
