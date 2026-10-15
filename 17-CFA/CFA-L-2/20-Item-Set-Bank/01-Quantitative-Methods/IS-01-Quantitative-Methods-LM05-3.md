---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 5
title: "Arbor Currency Partners Pitch Book Review"
los: [los-01-05-g, los-01-05-i, los-01-05-j, los-01-05-k]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Arbor Currency Partners Pitch Book Review

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Hannah Okoye, CFA, is chief compliance officer at Arbor Currency Partners, an asset manager that runs currency overlay mandates for institutional clients.
She is reviewing a draft pitch book prepared by portfolio manager Diego Ferreira for a pension fund prospect.
The pitch book presents a time-series analysis of the month-end AUD/NZD exchange rate, quoted in New Zealand dollars per Australian dollar.
The sample contains 240 month-end observations from January 2005 through December 2024.

Exhibit 1: Regressions on the level of AUD/NZD, $x_t$

| Regression | Item | Coefficient | Standard error | t-statistic |
|---|---|---|---|---|
| 1: $x_t = b_0 + b_1 x_{t-1} + \varepsilon_t$ | Intercept | 0.0152 | 0.0126 | 1.21 |
| | $x_{t-1}$ | 0.9864 | 0.0066 | 149.45 |
| 2: $x_t - x_{t-1} = b_0 + g_1 x_{t-1} + \varepsilon_t$ | Intercept | 0.0152 | 0.0126 | 1.21 |
| | $x_{t-1}$ | $-0.0136$ | 0.0066 | |

Regression 1 uses 239 observations, has an $R^2$ of 0.9894, and has a Durbin-Watson statistic of 1.91.
The 5% Dickey-Fuller critical value for Regression 2 is $-2.87$, and the conventional 5% critical t-value is 1.97.

Exhibit 2: Regression 3, AR(1) on the first difference $y_t = x_t - x_{t-1}$ (238 observations)

| Item | Coefficient | t-statistic |
|---|---|---|
| Intercept | 0.0003 | 0.41 |
| $y_{t-1}$ | 0.0521 | 0.80 |
| $R^2$ | 0.0027 | |

Residual autocorrelations at lags 1 to 4 are 0.0412, $-0.0655$, 0.0303 and 0.0874, each with a standard error of 0.0648.

The pitch book also compares Arbor's proprietary Signal model, which forecasts the monthly percentage change in AUD/NZD, with a naive forecast of no change.

Exhibit 3: Out-of-sample forecast errors for the monthly percentage change, January to June 2025

| Month (2025) | Signal model error | No-change forecast error |
|---|---|---|
| January | 1.10 | 0.85 |
| February | $-1.45$ | $-1.02$ |
| March | 0.62 | 0.47 |
| April | $-0.88$ | $-1.20$ |
| May | 1.31 | 0.66 |
| June | $-0.54$ | $-0.39$ |

The draft, dated 10 July 2025, contains three claims.

Claim 1: "With an $R^2$ of 98.9%, our model explains virtually all of the movement in AUD/NZD."

Claim 2: "The model identifies a long-run equilibrium of 1.1176 NZD per AUD to which the rate reliably reverts, creating systematic trading opportunities."

Claim 3: "Out of sample, the Signal model outperformed the naive no-change forecast, with an average forecast error closer to zero."

On 12 July 2025 Okoye writes to Ferreira: "Before I approve the pitch book, I need to know whether this exchange rate behaves like a random walk.
If it does, I am concerned that Claims 2 and 3 misrepresent what the strategy can deliver."

Ferreira replies the same day: "The slope in Regression 1 has a t-statistic of almost 150, which proves the series is well behaved, and a model that fits this well in sample must forecast well out of sample."

## Questions

1. Based on Exhibit 1, the Dickey-Fuller test statistic and the correct conclusion are: (LOS: los-01-05-k)
   - A. $-2.06$; reject the null hypothesis of a unit root, because the statistic exceeds 1.97 in absolute value.
   - B. $-2.06$; fail to reject the null hypothesis of a unit root, because the statistic is not below $-2.87$.
   - C. 149.45; reject the null hypothesis of a unit root, because $b_1$ is significantly different from zero.
2. Regarding Claim 2, Okoye should conclude that it is: (LOS: los-01-05-i)
   - A. supported, because $0.0152/(1 - 0.9864) = 1.1176$ and a slope below 1 implies mean reversion.
   - B. not supported, because the correct equilibrium is $0.0152/0.9864 = 0.0154$.
   - C. not supported, because the rate cannot be distinguished from a random walk, whose mean-reverting level is undefined and whose best forecast is the current value.
3. Regression 3 in Exhibit 2 is most consistent with the conclusion that: (LOS: los-01-05-j)
   - A. AUD/NZD follows a random walk with drift, because the intercept of 0.0003 implies a steady monthly rise.
   - B. Regression 1 should be retained for forecasting, because the $R^2$ of Regression 3 is only 0.0027.
   - C. the first-differenced series is covariance stationary and AUD/NZD follows a random walk without drift, so monthly changes are unpredictable.
4. Regarding Claim 3, Okoye should conclude that it is: (LOS: los-01-05-g)
   - A. supported, because the Signal model's mean error of 0.027 is closer to zero than the no-change forecast's mean error of $-0.105$.
   - B. not supported, because the Signal model's out-of-sample RMSE of 1.04 exceeds the no-change forecast's RMSE of 0.82.
   - C. supported, because the in-sample $R^2$ of 0.9894 shows the modelling approach has superior forecasting accuracy.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Subtracting $x_{t-1}$ from both sides of Regression 1 gives Regression 2 with $g_1 = b_1 - 1 = 0.9864 - 1 = -0.0136$ and the same standard error, 0.0066.
> The Dickey-Fuller statistic is $-0.0136/0.0066 = -2.06$, and $H_0: g_1 = 0$ (unit root) is tested against $H_a: g_1 < 0$ using Dickey-Fuller critical values.
> Because $-2.06$ is not below $-2.87$, the unit root cannot be rejected and the series is not shown to be covariance stationary.
> A is wrong because it uses the conventional t critical value; under the null the statistic does not follow a t-distribution, which is why a conventional test of $b_1 = 1$ is invalid.
> C is wrong because 149.45 tests $b_1 = 0$, not $b_1 = 1$, and that t-statistic is itself unreliable if the series has a unit root.
>
> 2. **C.** A series with a unit root behaves as a random walk ($b_0 = 0$, $b_1 = 1$, and the Regression 1 intercept is insignificant with $t = 1.21$).
> A random walk has no finite mean-reverting level ($0/0$), its variance grows with time, and its best forecast at every horizon is the current value, so a "reliable" equilibrium is a misrepresentation.
> A is wrong because the arithmetic, $0.0152/0.0136 = 1.1176$, is correct but the formula is valid only for a covariance-stationary series.
> B is wrong because it divides by $b_1$ instead of $1 - b_1$.
>
> 3. **C.** The largest residual t-statistic is $0.0874/0.0648 = 1.35$, below 1.97, and neither coefficient is significant, so Regression 3 reduces to $y_t = \varepsilon_t$.
> That is the first difference of a random walk: mean-reverting level $0/(1 - 0) = 0$ and constant variance, so the differenced series is covariance stationary and the original series has a unit root.
> A is wrong because drift would require a significant intercept in the differenced regression, and $t = 0.41$ is not significant.
> B is wrong because $R^2$ cannot be used to choose between a level model and a differenced model; the high $R^2$ of Regression 1 reflects the random walk's current value predicting next month's level, not predictable changes.
>
> 4. **B.** Signal model squared errors: 1.2100, 2.1025, 0.3844, 0.7744, 1.7161, 0.2916; sum 6.4790; RMSE $= \sqrt{6.4790/6} = \sqrt{1.0798} = 1.0392$.
> No-change squared errors: 0.7225, 1.0404, 0.2209, 1.4400, 0.4356, 0.1521; sum 4.0115; RMSE $= \sqrt{4.0115/6} = \sqrt{0.6686} = 0.8177$.
> The model with the smaller out-of-sample RMSE is the more accurate, so the naive forecast outperformed the Signal model and Claim 3 is misleading.
> A is wrong because mean error lets positive and negative errors cancel ($0.16/6 = 0.0267$ versus $-0.63/6 = -0.1050$); it measures bias, not accuracy.
> C is wrong because in-sample fit is not a measure of out-of-sample forecasting accuracy, which is also the flaw in Ferreira's reply.

## Distractor design

1. A: conventional t critical value instead of Dickey-Fuller; C: tests $b_1 = 0$ instead of $b_1 = 1$.
2. A: applies the mean-reverting formula to a nonstationary series; B: wrong formula variant (divides by $b_1$).
3. A: reads an insignificant intercept as drift; B: chooses between level and differenced models by $R^2$.
4. A: mean error instead of RMSE; C: in-sample criterion used for an out-of-sample claim.
