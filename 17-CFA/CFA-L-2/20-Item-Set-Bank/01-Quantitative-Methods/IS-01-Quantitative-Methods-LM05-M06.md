---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 5
title: "Marisol Coastal Hotels RevPAR"
los: [los-01-05-l, los-01-05-e, los-01-05-g]
difficulty: 3
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Marisol Coastal Hotels RevPAR

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Keiko Andersen is a lodging analyst at Halvard Real Estate Securities, a fund that invests in listed hotel owners.
She covers Marisol Coastal Hotels, which owns resort properties whose revenue per available room (RevPAR) peaks every December and falls sharply in January.
Because Marisol's operating costs are largely fixed, its quarterly earnings are highly sensitive to RevPAR in the first months of each year.
Andersen's director of research has asked her to confirm that any model she relies on is correctly specified and to show how it performs on data it was not estimated on.
Andersen models the monthly log change in RevPAR, $y_t = \ln \text{RevPAR}_t - \ln \text{RevPAR}_{t-1}$, which is not seasonally adjusted.
A unit root test rejects nonstationarity for $y_t$.
Her first model is an AR(1) estimated on 143 monthly observations from February 2013 through December 2024.

Exhibit 1: AR(1) model of $y_t$ (143 observations)

| Item | Coefficient | t-statistic |
|---|---|---|
| Intercept | 0.0061 | 1.37 |
| $y_{t-1}$ | $-0.1840$ | $-2.23$ |
| $R^2$ | 0.0341 | |
| Durbin-Watson statistic | 1.97 | |

| Lag | Residual autocorrelation |
|---|---|
| 1 | 0.0412 |
| 2 | $-0.0935$ |
| 3 | 0.0588 |
| 6 | $-0.1120$ |
| 12 | 0.4580 |

The critical t-value at the 5% level is 1.98 for all regressions in this vignette.

Andersen then estimates a revised model with an added lagged regressor.
Because the sample start is fixed, the revised model uses 132 observations, from January 2014 through December 2024.

Exhibit 2: Revised model of $y_t$ (132 observations)

| Item | Coefficient | t-statistic |
|---|---|---|
| Intercept | 0.0024 | 0.81 |
| $y_{t-1}$ | $-0.0915$ | $-1.52$ |
| $y_{t-12}$ | 0.6870 | 11.64 |
| $R^2$ | 0.5124 | |

| Lag | Residual autocorrelation |
|---|---|
| 1 | 0.0381 |
| 2 | $-0.0724$ |
| 3 | 0.0490 |
| 6 | $-0.0655$ |
| 12 | 0.1690 |

An ARCH(1) test on the Exhibit 2 residuals is not significant.

Exhibit 3: Marisol RevPAR (\$)

| Month | RevPAR |
|---|---|
| November 2023 | 118.40 |
| December 2023 | 131.60 |
| January 2024 | 104.90 |
| February 2024 | 109.30 |
| November 2024 | 124.10 |
| December 2024 | 138.20 |

Andersen tests both models out of sample over January to June 2025.

Exhibit 4: Out-of-sample forecast errors for $y_t$, actual minus forecast (percentage points)

| Month (2025) | AR(1) error | Revised model error |
|---|---|---|
| January | $-13.2$ | 1.8 |
| February | 10.4 | $-1.4$ |
| March | $-4.1$ | 2.1 |
| April | 3.9 | $-0.6$ |
| May | $-7.2$ | 2.2 |
| June | 10.4 | 0.7 |

On 14 July 2025 her colleague, Tomasz Wieland, comments: "The revised model tends to under-forecast; its errors are mostly positive, while the AR(1) errors average almost exactly zero.
The jump in $R^2$ from 0.0341 to 0.5124 is in-sample fit, so the out-of-sample record should decide which model we use."

## Questions

1. Based on Exhibit 1, Andersen should conclude that the AR(1) model is: (LOS: los-01-05-l)
   - A. correctly specified, because no residual autocorrelation exceeds the critical value of 1.98.
   - B. misspecified; the lag-12 residual autocorrelation has a t-statistic of about 5.48, so $y_{t-12}$ should be added as a regressor.
   - C. misspecified; the lag-12 residual autocorrelation has a t-statistic of about 5.48, so $y_{t-4}$ should be added as a regressor.
2. Based on Exhibit 2, the t-statistic of the lag-12 residual autocorrelation of the revised model, and the correct conclusion, are closest to: (LOS: los-01-05-e)
   - A. 1.94; the revised model is correctly specified.
   - B. 2.02; the revised model is still misspecified by seasonality.
   - C. 1.94; the revised model is misspecified, because the coefficient on $y_{t-12}$ is significant.
3. Using Exhibits 2 and 3, the forecast of Marisol's RevPAR for January 2025 is closest to: (LOS: los-01-05-l)
   - A. \$115.64.
   - B. \$117.39.
   - C. \$147.51.
4. Based on Exhibit 4, the out-of-sample root mean squared error of the revised model, and the model that forecasts more accurately, are closest to: (LOS: los-01-05-g)
   - A. 1.60 percentage points; the revised model.
   - B. 2.55 percentage points; the revised model.
   - C. 1.60 percentage points; the AR(1) model, because its average error is closer to zero.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The standard error of each residual autocorrelation is $1/\sqrt{143} = 0.08362$.
> The lag-12 t-statistic is $0.4580 \times \sqrt{143} = 0.4580 \times 11.9583 = 5.48$, above 1.98; every other lag is insignificant (the largest is lag 6, $-0.1120 \times 11.9583 = -1.34$).
> For monthly data a significant twelfth residual autocorrelation is the signature of seasonality, and the correction is a seasonal lag one year back, $y_{t-12}$.
> A is wrong because it compares the raw autocorrelations with the critical value instead of their t-statistics; the Durbin-Watson statistic of 1.97, which also looks reassuring, is invalid for an AR model.
> C is wrong because lag 4 is the seasonal lag for quarterly data; with monthly data it does not address a twelfth-lag pattern.
>
> 2. **A.** The test uses the number of observations in the regression being tested, $T = 132$, so the standard error is $1/\sqrt{132} = 0.08704$.
> The lag-12 t-statistic is $0.1690 \times \sqrt{132} = 0.1690 \times 11.4891 = 1.94$, below 1.98, and all other lags are smaller in absolute value (lag 2: $-0.0724 \times 11.4891 = -0.83$), so no residual autocorrelation is significant and the revised model is correctly specified.
> B is wrong because it keeps the AR(1) sample size: $0.1690 \times \sqrt{143} = 0.1690 \times 11.9583 = 2.02$.
> C is wrong because specification is judged by the residual autocorrelations, not by the significance of a coefficient; a significant seasonal coefficient is what one expects once seasonality is modeled.
>
> 3. **B.** The forecast made at the end of December 2024 for January 2025 uses the latest log change and the log change for the same month one year earlier, $y_{t-11}$, because $(t + 1) - 12 = t - 11$.
> $y_t = \ln(138.20/124.10) = 0.10761$ (December 2024).
> $y_{t-11} = \ln(104.90/131.60) = -0.22676$ (January 2024).
> $\hat{y}_{t+1} = 0.0024 - 0.0915(0.10761) + 0.6870(-0.22676) = 0.0024 - 0.00985 - 0.15578 = -0.16323$.
> $\widehat{\text{RevPAR}} = 138.20 \times e^{-0.16323} = 138.20 \times 0.84940 = 117.39$.
> A is wrong because it treats the log change as a simple growth rate: $138.20 \times (1 - 0.16323) = 115.64$.
> C is wrong because it uses the December 2023 change, $y_{t-12} = \ln(131.60/118.40) = 0.10570$, as the seasonal input: $\hat{y} = 0.0024 - 0.00985 + 0.07261 = 0.06517$ and $138.20 \times e^{0.06517} = 147.51$.
>
> 4. **A.** Revised model squared errors: 3.24, 1.96, 4.41, 0.36, 4.84, 0.49; sum 15.30; mean $15.30/6 = 2.55$; RMSE $= \sqrt{2.55} = 1.5969$.
> AR(1) squared errors: 174.24, 108.16, 16.81, 15.21, 51.84, 108.16; sum 474.42; mean $474.42/6 = 79.07$; RMSE $= \sqrt{79.07} = 8.8921$.
> The model with the smaller out-of-sample RMSE is the more accurate, so the revised model wins out of sample, consistent with its better in-sample fit; Wieland is right that the out-of-sample record should decide.
> B is wrong because 2.55 is the mean squared error; the square root has not been taken.
> C is wrong because the mean error ($0.2/6 = 0.03$ for the AR(1) versus $4.8/6 = 0.80$ for the revised model) measures bias, and large positive and negative errors cancel in it; accuracy is judged by RMSE.

## Distractor design

1. A: compares raw autocorrelations with the critical value (and is tempted by the invalid Durbin-Watson statistic); C: quarterly seasonal lag applied to monthly data.
2. B: wrong $T$ (the AR(1) sample of 143 instead of the revised model's 132); C: judges specification by coefficient significance instead of residual autocorrelations.
3. A: log change applied as a simple growth rate; C: misread exhibit, seasonal input taken from $t - 12$ instead of $t - 11$.
4. B: omits the square root (MSE, not RMSE); C: mean error (bias) used instead of RMSE.
