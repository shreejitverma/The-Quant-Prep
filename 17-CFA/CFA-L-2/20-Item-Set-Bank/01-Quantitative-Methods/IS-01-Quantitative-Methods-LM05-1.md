---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 5
title: "Halden Brewing Quarterly Revenue"
los: [los-01-05-a, los-01-05-b, los-01-05-c, los-01-05-e, los-01-05-l, los-01-05-o]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Halden Brewing Quarterly Revenue

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Mira Castellanos, CFA, is an equity analyst at Ostrander Securities who covers Halden Brewing Company, a listed regional brewer whose revenue peaks every summer.
In January 2025 she begins rebuilding her revenue model ahead of an updated valuation.
She uses 56 quarters of reported revenue from 1Q 2011 through 4Q 2024, numbering 1Q 2011 as period 1.
Because revenue has more than doubled over the sample, she first estimates a linear trend and a log-linear trend.

Exhibit 1: Trend models of Halden quarterly revenue, 1Q 2011 to 4Q 2024 (56 observations)

| Statistic | Linear trend | Log-linear trend |
|---|---|---|
| Dependent variable | Revenue (\$ millions) | ln(Revenue) |
| Intercept | 98.40 | 4.8120 |
| Trend coefficient | 3.215 | 0.0165 |
| t-statistic of trend coefficient | 23.72 | 26.40 |
| $R^2$ | 0.9124 | 0.9281 |
| Durbin-Watson statistic | 0.31 | 0.42 |

The 5% lower Durbin-Watson critical value $d_l$ for 56 observations and one regressor is 1.53.

On 17 January 2025 Castellanos and her supervisor, Anders Vik, discuss the output.

Castellanos: "The log-linear model is the better description of Halden because revenue has grown at a roughly constant percentage rate, and its higher $R^2$ confirms it is ready for forecasting."

Vik: "Before we fit any autoregression to log revenue itself, remember that the series trends upward for fourteen years; I want a model estimated on a series whose mean and variance do not depend on time."

Castellanos then computes the quarterly log change in revenue, $\Delta \ln R_t = \ln R_t - \ln R_{t-1}$, and estimates an AR(1) model on it using 54 observations.

Exhibit 2: AR(1) model of $\Delta \ln R_t$ (54 observations)

| Item | Coefficient | t-statistic |
|---|---|---|
| Intercept | 0.0152 | 2.24 |
| $\Delta \ln R_{t-1}$ | $-0.1890$ | $-1.41$ |
| Durbin-Watson statistic | 1.96 | |

| Lag | Residual autocorrelation |
|---|---|
| 1 | 0.0842 |
| 2 | $-0.1105$ |
| 3 | 0.0317 |
| 4 | 0.4620 |

The critical t-value at the 5% level for the Exhibit 2 regression is 2.01.

After reviewing Exhibit 2, she re-estimates the model with an additional lagged regressor.
The larger lag structure reduces the sample to 51 observations.

Exhibit 3: Revised model of $\Delta \ln R_t$ (51 observations)

| Item | Coefficient | t-statistic |
|---|---|---|
| Intercept | 0.0068 | 1.62 |
| $\Delta \ln R_{t-1}$ | $-0.1420$ | $-2.05$ |
| $\Delta \ln R_{t-4}$ | 0.6810 | 7.93 |
| $R^2$ | 0.6415 | |

Residual autocorrelations at lags 1 to 4 are 0.0311, $-0.0724$, 0.1083 and $-0.0915$, each with a standard error of 0.1400, and the critical t-value is 2.01.

Exhibit 4: Halden reported revenue (\$ millions)

| Quarter | Revenue |
|---|---|
| 3Q 2023 | 318.4 |
| 4Q 2023 | 285.1 |
| 1Q 2024 | 262.7 |
| 2Q 2024 | 309.5 |
| 3Q 2024 | 336.2 |
| 4Q 2024 | 301.9 |

Castellanos intends to run an ARCH test on the Exhibit 3 residuals before finalizing the model; assume for this set that no ARCH effect is found.

## Questions

1. Using the log-linear trend model in Exhibit 1, Halden's forecasted revenue for 2Q 2025 is closest to: (LOS: los-01-05-a)
   - A. \$284.87 million.
   - B. \$314.98 million.
   - C. \$320.22 million.
2. Castellanos's statement on 17 January 2025 is best described as: (LOS: los-01-05-b)
   - A. correct.
   - B. incorrect, because Halden's revenue grows by a constant amount, so the linear trend is the appropriate form.
   - C. incorrect, because although the log-linear form suits constant-rate growth, its errors are positively serially correlated, so it is not reliable for forecasting.
3. Vik's concern on 17 January 2025 is best explained by the fact that: (LOS: los-01-05-c)
   - A. a series whose mean rises with time is not covariance stationary, so an autoregression on it produces a biased slope estimate and invalid hypothesis tests.
   - B. taking natural logarithms stabilizes the variance of revenue and therefore makes log revenue covariance stationary, so his concern is unfounded.
   - C. log revenue is covariance stationary provided the residuals of the log-linear trend model are homoskedastic.
4. Based on Exhibit 2, the t-statistic of the fourth-lag residual autocorrelation and the most appropriate response are: (LOS: los-01-05-e)
   - A. 0.46; the AR(1) model is correctly specified.
   - B. 3.39; add $\Delta \ln R_{t-4}$ as a regressor.
   - C. 3.39; add $\Delta \ln R_{t-2}$ as a regressor to form an AR(2) model.
5. Using Exhibits 3 and 4, Halden's forecasted revenue for 1Q 2025 is closest to: (LOS: los-01-05-l)
   - A. \$286.27 million.
   - B. \$291.91 million.
   - C. \$308.64 million.
6. Based on all the exhibits, the most appropriate model for forecasting Halden's quarterly revenue is: (LOS: los-01-05-o)
   - A. the log-linear trend model, because it has the highest $R^2$ among the trend models.
   - B. an AR(1) model of first-differenced log revenue that includes a seasonal lag of four quarters.
   - C. an AR(2) model of first-differenced revenue measured in dollars.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** 2Q 2025 is two quarters beyond period 56, so $t = 58$.
> $\ln \hat{R}_{58} = 4.8120 + 0.0165(58) = 4.8120 + 0.9570 = 5.7690$, and $\hat{R}_{58} = e^{5.7690} = 320.22$.
> A is wrong because it applies the linear trend instead of the log-linear trend: $98.40 + 3.215(58) = 98.40 + 186.47 = 284.87$.
> B is wrong because it uses $t = 57$, the next quarter (1Q 2025): $e^{4.8120 + 0.0165(57)} = e^{5.7525} = 314.98$.
>
> 2. **C.** A constant growth rate is the case for a log-linear trend, which implies quarterly growth of $e^{0.0165} - 1 = 1.66\%$.
> But the Durbin-Watson statistic of 0.42 is below $d_l = 1.53$, so the null of no positive serial correlation is rejected and the model violates the uncorrelated-errors assumption.
> A high $R^2$ does not rescue a trend model with serially correlated errors.
> A is wrong because it relies on $R^2$ and ignores the Durbin-Watson result.
> B is wrong because constant-amount growth describes the linear trend, and the linear trend also fails the test (DW 0.31 below 1.53).
>
> 3. **A.** Covariance stationarity requires a constant and finite mean, variance, and autocovariance at each lag.
> A series that trends upward has a mean that changes with $t$, and running an AR model on a nonstationary series gives a biased estimate of $b_1$ and invalid t-tests.
> B is wrong because a log transformation converts exponential growth into a linear trend but does not remove the trend; first-differencing is still required.
> C is wrong because homoskedastic trend residuals say nothing about whether the mean of the series is constant.
>
> 4. **B.** The standard error of each residual autocorrelation is $1/\sqrt{54} = 0.1361$.
> The fourth-lag t-statistic is $0.4620/0.1361 = 0.4620 \times 7.3485 = 3.39$, above 2.01, so the AR(1) is misspecified.
> For quarterly data a significant fourth-lag residual autocorrelation signals seasonality, and the correction is a seasonal lag, $\Delta \ln R_{t-4}$.
> A is wrong because it compares the raw autocorrelation (0.46) with the critical value instead of dividing by the standard error; the Durbin-Watson statistic of 1.96 is also irrelevant for an AR model.
> C is wrong because an AR(2) lag does not address a fourth-lag (seasonal) pattern.
>
> 5. **B.** The forecast made at the end of 4Q 2024 for 1Q 2025 uses the most recent log change and the log change of the same quarter one year earlier, which is period $t - 3$.
> $\Delta \ln R_t = \ln(301.9/336.2) = -0.10761$ and $\Delta \ln R_{t-3} = \ln(262.7/285.1) = -0.08183$.
> $\hat{y} = 0.0068 - 0.1420(-0.10761) + 0.6810(-0.08183) = 0.0068 + 0.01528 - 0.05572 = -0.03364$.
> $\hat{R} = 301.9 \times e^{-0.03364} = 301.9 \times 0.96692 = 291.91$.
> A is wrong because it uses the 4Q 2023 change, $\ln(285.1/318.4) = -0.11047$, as the seasonal input: $\hat{y} = -0.05315$ and $301.9 e^{-0.05315} = 286.27$.
> C is wrong because it omits the seasonal term: $\hat{y} = 0.0068 + 0.01528 = 0.02208$ and $301.9 e^{0.02208} = 308.64$.
>
> 6. **B.** Revenue grows at a roughly constant rate, so logs are taken; the log series trends, so it is first-differenced; the AR(1) residuals show a significant fourth-lag autocorrelation, so a seasonal lag is added.
> The Exhibit 3 residual t-statistics are all below 2.01 in absolute value (largest $0.1083/0.1400 = 0.77$), and no ARCH effect is assumed, so this specification is appropriate.
> A is wrong because the trend residuals are serially correlated and $R^2$ cannot validate the model.
> C is wrong because differencing dollar revenue is the transformation for a linear trend, and an extra nonseasonal lag does not capture the seasonal pattern.

## Distractor design

1. A: wrong model (linear trend instead of log-linear); B: wrong period index ($t = T + 1$ instead of $T + 2$).
2. A: accepts $R^2$ as validation and ignores Durbin-Watson; B: confuses constant-amount with constant-rate growth.
3. B: believes a log transformation alone removes a trend; C: confuses homoskedasticity with stationarity of the mean.
4. A: compares the raw autocorrelation with the critical value (and is tempted by the invalid DW of 1.96); C: right diagnosis, wrong remedy (nonseasonal lag).
5. A: misread exhibit, seasonal input taken from $t - 4$ instead of $t - 3$; C: omits the seasonal term.
6. A: in-sample $R^2$ criterion on a misspecified trend; C: wrong transformation (level differencing) and wrong lag structure.
