---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 5
title: "Tern Harbor Container Volumes"
los: [los-01-05-a, los-01-05-b, los-01-05-d, los-01-05-f]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Tern Harbor Container Volumes

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ingrid Solberg is a credit analyst at Coastline Infrastructure Debt Partners, a fund that invests in revenue bonds of transport assets.
The fund holds bonds of the Tern Harbor Port Authority, whose wharfage revenue is set per container handled.
Solberg is preparing volume projections for the bonds' debt service coverage test.
The indenture requires coverage of at least 1.25 times, tested each year on projected wharfage revenue for the following twelve months.
The fund's investment committee will review her projections before the annual surveillance report on the bonds is issued.
Her portfolio manager has asked her to document every model she considers and to explain why the model she adopts is preferred.
She uses 96 months of seasonally adjusted container throughput, in thousands of twenty-foot equivalent units (TEU), from July 2016 through June 2024.
She numbers July 2016 as period 1.
Over the sample, volumes have more than doubled, and the port's own planning documents describe traffic as compounding with regional trade.

Exhibit 1: Trend models of monthly volume, July 2016 to June 2024 (96 observations)

| Statistic | Linear trend | Log-linear trend |
|---|---|---|
| Dependent variable | Volume (thousand TEU) | ln(Volume) |
| Intercept | 137.60 | 5.0010 |
| Trend coefficient | 1.818 | 0.00812 |
| t-statistic of trend coefficient | 38.62 | 44.18 |
| $R^2$ | 0.9408 | 0.9541 |
| Standard error of regression | 12.78 | 0.0499 |
| Durbin-Watson statistic | 0.44 | 0.58 |

The 5% lower Durbin-Watson critical value $d_l$ for 96 observations and one regressor is 1.65.

On 15 July 2024 Solberg and her portfolio manager, Dario Menn, review Exhibit 1.

Solberg: "The log-linear form matches the way this port grows, a roughly constant percentage each month rather than a constant number of containers."

Menn: "Agreed, and with a trend t-statistic of 44.18 and an $R^2$ of 0.9541, the log-linear model is reliable enough to use directly in the coverage projections."

Solberg is not persuaded and also models the monthly log change in volume, $g_t = \ln V_t - \ln V_{t-1}$.
A unit root test rejects nonstationarity for $g_t$.
She estimates an AR(1) model of $g_t$ on 94 observations.

Exhibit 2: AR(1) model of $g_t$ (94 observations)

| Item | Coefficient | t-statistic |
|---|---|---|
| Intercept | 0.0118 | 4.21 |
| $g_{t-1}$ | $-0.4150$ | $-4.39$ |
| Durbin-Watson statistic | 2.06 | |

None of the residual autocorrelations at lags 1 to 12 is significant at the 5% level.
The sample mean of $g_t$ over the estimation period is 0.0081.

Exhibit 3: Recent monthly volumes (thousand TEU)

| Month | Volume |
|---|---|
| April 2024 | 322.4 |
| May 2024 | 318.6 |
| June 2024 | 331.9 |

Solberg notes that June 2024 volume was lifted by cargo diverted from a competing port during a two-week labor dispute.

## Questions

1. Using the log-linear trend model in Exhibit 1, the forecasted volume for December 2024 is closest to: (LOS: los-01-05-a)
   - A. 156.0 thousand TEU.
   - B. 323.0 thousand TEU.
   - C. 340.1 thousand TEU.
2. The annual growth rate implied by the log-linear trend model, and the most appropriate evaluation of Menn's statement, are: (LOS: los-01-05-b)
   - A. 9.74%; Menn is incorrect, because the Durbin-Watson statistic shows positive serial correlation in the errors.
   - B. 10.23%; Menn is incorrect, because the Durbin-Watson statistic shows positive serial correlation in the errors.
   - C. 10.23%; Menn is correct, because the trend coefficient is highly significant and the model explains over 95% of the variation in log volume.
3. Using Exhibits 2 and 3, the forecasted volume for August 2024 is closest to: (LOS: los-01-05-d)
   - A. 328.5 thousand TEU.
   - B. 330.2 thousand TEU.
   - C. 334.8 thousand TEU.
4. Based on Exhibits 2 and 3, the mean-reverting level of $g_t$ and the forecast of July 2024 growth relative to June 2024 growth are: (LOS: los-01-05-f)
   - A. 0.0083; July growth is forecast to be lower than June growth.
   - B. 0.0202; July growth is forecast to be lower than June growth.
   - C. 0.0083; July growth is forecast to be higher than June growth.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** July 2016 is period 1, so June 2024 is period 96 and December 2024, six months later, is $t = 96 + 6 = 102$.
> $\ln \hat{V}_{102} = 5.0010 + 0.00812(102) = 5.0010 + 0.82824 = 5.82924$.
> $\hat{V}_{102} = e^{5.82924} = 340.10$ thousand TEU.
> A is wrong because it uses $t = 6$, the number of months ahead, as the time index: $e^{5.0010 + 0.00812(6)} = e^{5.04972} = 155.98$.
> B is wrong because it applies the linear trend instead of the log-linear trend: $137.60 + 1.818(102) = 137.60 + 185.436 = 323.04$.
>
> 2. **B.** In a log-linear trend the ratio of consecutive values is $e^{b_1}$, so twelve months compound to $e^{12 b_1}$.
> Annual growth $= e^{12(0.00812)} - 1 = e^{0.09744} - 1 = 1.10235 - 1 = 10.23\%$ (monthly, $e^{0.00812} - 1 = 0.8153\%$).
> Solberg is right that constant-rate growth calls for the log-linear form, but the Durbin-Watson statistic of 0.58 is below $d_l = 1.65$, so the null of no positive serial correlation is rejected.
> Serially correlated errors violate the regression assumptions, so the trend model's standard errors and forecasts are unreliable however high the $R^2$ and t-statistic.
> A is wrong because it reads $12 b_1 = 0.09744$ as the growth rate without exponentiating.
> C is wrong because it relies on $R^2$ and coefficient significance, which cannot validate a trend model with serially correlated errors.
>
> 3. **C.** The latest observed growth is $g_{\text{Jun}} = \ln(331.9/318.6) = 0.04090$.
> July, one step ahead: $\hat{g}_{\text{Jul}} = 0.0118 - 0.4150(0.04090) = 0.0118 - 0.01697 = -0.00517$.
> August, by the chain rule: $\hat{g}_{\text{Aug}} = 0.0118 - 0.4150(-0.00517) = 0.0118 + 0.00215 = 0.01395$.
> The two log changes add: $-0.00517 + 0.01395 = 0.00877$, so $\hat{V}_{\text{Aug}} = 331.9 \times e^{0.00877} = 331.9 \times 1.00881 = 334.82$.
> A is wrong because it applies the July growth forecast to both months instead of chaining: $331.9 \times e^{2(-0.00517)} = 328.48$.
> B is wrong because it stops at the one-month-ahead forecast for July: $331.9 \times e^{-0.00517} = 330.19$.
>
> 4. **A.** The mean-reverting level is $\hat{b}_0/(1 - \hat{b}_1) = 0.0118/(1 - (-0.4150)) = 0.0118/1.4150 = 0.00834$.
> June growth of 0.0409 is above the level, so the model forecasts lower growth for July, and the July forecast of $-0.0052$ confirms it; the negative slope makes the forecast overshoot below the level before moving back toward it, which is why August growth (0.0139) is above the level.
> The level is close to the log-linear trend coefficient (0.00812) and the sample mean (0.0081), as expected for a stationary growth series, but the sample mean is not the model's level.
> B is wrong because it subtracts the absolute value of the negative slope: $0.0118/(1 - 0.4150) = 0.0118/0.5850 = 0.0202$.
> C is wrong because it reverses the direction: a series above its mean-reverting level is forecast to fall toward it.

## Distractor design

1. A: wrong period index ($t = k$ instead of $t = T + k$); B: wrong model (linear trend read from the misread exhibit column).
2. A: reads $12 b_1$ as the growth rate without exponentiating; C: accepts $R^2$ and coefficient significance and ignores Durbin-Watson.
3. A: repeats the one-period growth forecast instead of chaining; B: stops at the one-period forecast.
4. B: sign error on a negative $b_1$ in $b_0/(1 - b_1)$; C: reverses the mean-reversion direction.
