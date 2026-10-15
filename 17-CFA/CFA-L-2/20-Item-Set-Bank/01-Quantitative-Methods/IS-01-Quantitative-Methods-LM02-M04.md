---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 2
title: "Tessaline Real Estate Partners warehouse cap-rate models"
los: [los-01-02-a, los-01-02-b, los-01-02-c]
difficulty: 4
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Tessaline Real Estate Partners warehouse cap-rate models

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Rafael Quintero, CFA, is an acquisitions analyst at Tessaline Real Estate Partners, a closed-end fund that buys logistics warehouses in northern Europe.
He is pricing the Brennholt Logistics Park warehouse, which the seller is marketing at an asking price of EUR 160 million.
Tessaline prices assets from a cross-sectional regression of transaction capitalization rates (CAP, in percent) estimated on n = 64 comparable warehouse sales.
The independent variables are distance to the nearest container port in kilometres (PORT), building age in years (AGE), clear height in metres (CLEAR), weighted average remaining lease term in years (WALT), and the percentage of rent paid by investment-grade tenants (CREDIT).

Model 1 uses PORT, AGE and WALT.
Model 2 adds CLEAR to Model 1.
Model 3 adds CREDIT to Model 2.
Model 2L uses the same four regressors as Model 2 but takes the natural logarithm of CAP as the dependent variable.
The sample standard deviation of the 64 cap rates is 0.58 percentage points, and their mean is 4.62%.

A software licence lapsed before Model 3's output was saved in full, so Quintero has only its overall F-statistic of 19.60, with 5 and 58 degrees of freedom and a p-value below 0.0001.

Exhibit 1. Fit statistics exported before the licence lapsed

| Statistic | Model 1 | Model 2 | Model 3 | Model 2L |
|---|---|---|---|---|
| Dependent variable | CAP | CAP | CAP | ln(CAP) |
| Independent variables | 3 | 4 | 5 | 4 |
| R-squared | 0.5790 | 0.6120 | not saved | 0.6290 |
| Adjusted R-squared | 0.5580 | 0.5857 | not saved | 0.6039 |
| AIC | -118.10 | -121.33 | not saved | -341.74 |
| BIC | -109.47 | -110.53 | not saved | -330.95 |

Exhibit 2. Estimated coefficients (standard errors were not saved)

| Variable | Model 2 | Model 3 |
|---|---|---|
| Intercept | 5.02 | 5.10 |
| PORT | 0.013 | 0.012 |
| AGE | 0.022 | 0.021 |
| CLEAR | -0.094 | -0.085 |
| WALT | -0.071 | -0.064 |
| CREDIT | | -0.0045 |

Exhibit 3. Brennholt Logistics Park

| Item | Value |
|---|---|
| Distance to port | 18 km |
| Year built | 2008 |
| Clear height | 12.2 m |
| Weighted average remaining lease term | 4.5 years |
| Rent from investment-grade tenants | 60% |
| Stabilised year-one net operating income | EUR 6.85 million |

The valuation date is in 2026.
For Brennholt's inputs the software had reported a standard error of the forecast of 0.31 percentage points for Model 3.

Selected values: $\ln(64) = 4.1589$; $F_{0.05}(2, 58) = 3.156$; $F_{0.01}(2, 58) = 4.991$; $F_{0.05}(5, 58) = 2.374$; $t_{0.025}(58) = 2.002$.

Tessaline's model policy requires the pricing model to be the specification best suited to prediction, and the investment committee memo to report the specification with the best goodness of fit.

On 11 May 2026, Head of Research Harriet Voss reviewed Quintero's draft.

Voss: "Model 2L has the highest adjusted R-squared in the table and by far the lowest AIC and BIC, so it wins on every count. Whatever model you use, the CREDIT slope is too small to matter, so leave that term out when you price Brennholt."

Quintero: "Before I accept either point, I will rebuild Model 3's fit statistics from its F-statistic and the dispersion of cap rates. I will also test whether CLEAR and CREDIT together belong in the model, with Model 1 as the restricted model."

## Questions

1. The adjusted R-squared of Model 3, and what it implies about the t-statistic of CREDIT in Model 3, are: (LOS: los-01-02-a)
   - A. 0.596; the absolute value of CREDIT's t-statistic is below 1.0
   - B. 0.628; the absolute value of CREDIT's t-statistic exceeds 1.0
   - C. 0.596; the absolute value of CREDIT's t-statistic exceeds 1.0
2. For Quintero's joint test at the 5% level, the F-statistic and the conclusion are: (LOS: los-01-02-b)
   - A. 2.74; fail to reject the null hypothesis, so Model 1 is supported
   - B. 3.84; reject the null hypothesis, so CLEAR and CREDIT should be retained
   - C. 4.24; reject the null hypothesis, so CLEAR and CREDIT should be retained
3. The AIC of Model 3, and the models that satisfy Tessaline's policy for pricing and for the goodness-of-fit report, respectively, are closest to: (LOS: los-01-02-a)
   - A. -122.06; Model 3 for pricing and Model 2 for goodness of fit
   - B. -122.06; Model 2L for pricing and Model 2L for goodness of fit
   - C. -115.76; Model 2 for pricing and Model 2 for goodness of fit
4. Using the model Tessaline's policy requires for pricing, the implied value of Brennholt Logistics Park is closest to: (LOS: los-01-02-c)
   - A. EUR 156.8 million
   - B. EUR 163.7 million
   - C. EUR 167.1 million

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The overall F-statistic is $F = \frac{R^2 / k}{(1 - R^2) / (n - k - 1)}$, so $R^2 = \frac{kF}{kF + (n - k - 1)} = \frac{5 \times 19.60}{98.00 + 58} = \frac{98.00}{156.00} = 0.62821$.
>    $\bar{R}^2 = 1 - \left(\frac{n-1}{n-k-1}\right)(1 - R^2) = 1 - (63 / 58)(0.37179) = 1 - 0.40385 = 0.59615$, equivalently $1 - 63 / 156 = 0.59615$.
>    Model 3 is Model 2 plus CREDIT, and adjusted R-squared rises from 0.5857 to 0.5962, which happens only if the added variable's $|t|$ exceeds 1.0.
>    Cross-check: the nested F for CREDIT alone is $\frac{0.62821 - 0.6120}{0.37179 / 58} = 2.5280 = t^2$, so $|t| = 1.5900$, above 1.0 but below $t_{0.025}(58) = 2.002$.
>    A is wrong because it compares Model 3's adjusted R-squared of 0.5962 with Model 2's unadjusted R-squared of 0.6120, sees a "fall", and infers $|t| < 1$; like must be compared with like.
>    B is wrong because 0.628 is Model 3's unadjusted R-squared.
> 2. **B.** $H_0: b_{CLEAR} = b_{CREDIT} = 0$ against $H_a$: at least one is not zero; restricted Model 1, unrestricted Model 3, $q = 2$, $n - k - 1 = 58$.
>    Because $SSE = SST(1 - R^2)$ and SST is common to both models, the nested F can be written in R-squared form: $F = \frac{(R^2_U - R^2_R) / q}{(1 - R^2_U) / (n - k - 1)} = \frac{(0.62821 - 0.5790) / 2}{0.37179 / 58} = \frac{0.024603}{0.0064103} = 3.8380$.
>    In sums of squares: $SST = 63 \times 0.58^2 = 21.1932$, $SSE_1 = 21.1932 \times 0.4210 = 8.9223$, $SSE_3 = 21.1932 \times 0.37179 = 7.8795$, and $\frac{(8.9223 - 7.8795) / 2}{7.8795 / 58} = 3.8380$.
>    3.84 exceeds $F_{0.05}(2, 58) = 3.156$, so reject (p-value 0.0272; the test would not reject at 1% against 4.991); CLEAR and CREDIT jointly explain cap rates.
>    A is wrong because it substitutes adjusted R-squareds into the R-squared form: $\frac{(0.59615 - 0.5580) / 2}{0.40385 / 58} = 2.7398$, which flips the decision; the identity $SSE = SST(1 - R^2)$ holds only for unadjusted R-squared.
>    C is wrong because it divides by $SSE / n$ instead of $SSE / (n - k - 1)$: $0.024603 / (0.37179 / 64) = 4.2350$; the conclusion happens to be right but the statistic is not.
> 3. **A.** $SST = (n - 1)s_Y^2 = 21.1932$ and $SSE_3 = 7.8795$ from Question 2, so $n \ln(SSE / n) = 64 \ln(7.8795 / 64) = 64 \ln(0.123118) = -134.0554$.
>    $AIC_3 = -134.0554 + 2(6) = -122.0554$ and $BIC_3 = -134.0554 + 4.1589(6) = -109.1021$.
>    Among the CAP models, AIC is lowest for Model 3 (-122.06 versus -121.33 and -118.10), so Model 3 is the prediction model used for pricing.
>    BIC is lowest for Model 2 (-110.53 versus -109.47 and -109.10), so Model 2 is reported as the best goodness of fit; BIC's penalty of 4.1589 per parameter outweighs CREDIT's fit gain of $64 \ln(7.8795 / 8.2230) = -2.7304$, while AIC's penalty of 2 does not.
>    B is wrong because AIC, BIC and R-squared are comparable only across models with the same dependent variable; Model 2L explains ln(CAP), whose much smaller residuals make its criteria look far lower without saying anything about fit to CAP.
>    C is wrong because it puts $SSE / (n - k - 1)$ inside the logarithm instead of $SSE / n$: $64 \ln(7.8795 / 58) + 12 = -127.7552 + 12 = -115.7552$, which is above Model 2's printed -121.33 and makes Model 2 look best on both criteria.
> 4. **C.** The pricing model is Model 3, the AIC choice from Question 3, and every term stays in the equation, including CREDIT; AGE $= 2026 - 2008 = 18$.
>    $\hat{Y} = 5.10 + 0.012(18) + 0.021(18) - 0.085(12.2) - 0.064(4.5) - 0.0045(60)$.
>    Terms: $5.10 + 0.2160 + 0.3780 - 1.0370 - 0.2880 - 0.2700 = 4.0990$%.
>    Value $= NOI / CAP = 6.85 / 0.040990 = 167.11$, about EUR 167.1 million.
>    A is wrong because it follows Voss and drops the CREDIT term from Model 3: $4.0990 + 0.2700 = 4.3690$%, and $6.85 / 0.043690 = 156.79$; the slopes were estimated jointly, and Question 2 shows CREDIT and CLEAR belong in the model.
>    B is wrong because it prices with Model 2, the goodness-of-fit (BIC) model rather than the prediction (AIC) model: $5.02 + 0.2340 + 0.3960 - 1.1468 - 0.3195 = 4.1837$%, and $6.85 / 0.041837 = 163.73$.
>    The asking price and the standard error of the forecast are not needed for the point value.

## Distractor design

1. A: Model 3's adjusted R-squared compared with Model 2's unadjusted R-squared; B: unadjusted R-squared reported.
2. A: adjusted R-squareds substituted into the R-squared form of the nested F; C: $SSE / n$ used in the denominator instead of $SSE / (n - k - 1)$.
3. B: information criteria compared across models with different dependent variables; C: $SSE / (n - k - 1)$ used inside the AIC logarithm instead of $SSE / n$.
4. A: an estimated term dropped from the forecast equation; B: forecast from the goodness-of-fit (BIC) model instead of the prediction (AIC) model.
