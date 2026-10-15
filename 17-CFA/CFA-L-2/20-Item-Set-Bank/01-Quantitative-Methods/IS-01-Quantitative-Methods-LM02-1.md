---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 2
title: "Harrowgate County Retirement System small-cap value review"
los: [los-01-02-a, los-01-02-b, los-01-02-c]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Harrowgate County Retirement System small-cap value review

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Priya Anand, CFA, is a consultant at Lindqvist Advisory, which prepares the quarterly manager review report for the Harrowgate County Employees' Retirement System.
The system has allocated USD 410 million to Brightwater Small Cap Value, an external manager.
Anand regresses Brightwater's monthly excess returns (in percent) on factor returns (in percent) over the last n = 72 months.
She estimates three nested specifications.
Model A uses the market (MKT), size (SMB) and value (HML) factors.
Model B adds the profitability factor (RMW).
Model C adds the investment factor (CMA) to Model B.
In Model B, the RMW coefficient has a t-statistic of 1.75.

Exhibit 1. ANOVA for Model C

| Source | df | Sum of squares |
|---|---|---|
| Regression | 5 | 352.35 |
| Residual | 66 | 168.05 |
| Total | 71 | 520.40 |

Exhibit 2. Goodness-of-fit statistics

| Statistic | Model A | Model B | Model C |
|---|---|---|---|
| Independent variables | 3 | 4 | 5 |
| R-squared | 0.6612 | 0.6760 | see Exhibit 1 |
| Adjusted R-squared | 0.6463 | 0.6567 | see Exhibit 1 |
| AIC | 72.48 | 71.26 | 73.03 |
| BIC | 81.58 | 82.65 | 86.69 |
| Durbin-Watson | 1.97 | 1.95 | 1.94 |

Exhibit 3. Model C estimated coefficients

| Variable | Coefficient | t-statistic |
|---|---|---|
| Intercept | 0.18 | 0.91 |
| MKT | 1.06 | 14.20 |
| SMB | 0.48 | 4.85 |
| HML | 0.31 | 2.62 |
| RMW | 0.22 | 1.70 |
| CMA | -0.09 | -0.46 |

The residual sum of squares of Model A is 176.30 and that of Model B is 168.60.

Anand's report includes a scenario for next month taken from Lindqvist's house view.

Exhibit 4. Assumed factor returns for next month (percent)

| MKT | SMB | HML | RMW | CMA | Momentum |
|---|---|---|---|---|---|
| 1.20 | -0.40 | 0.60 | 0.35 | -0.50 | 0.80 |

Critical values: $F_{0.05}(5, 66) = 2.354$; $F_{0.05}(2, 66) = 3.136$; two-tailed $t_{0.025}(66) = 1.997$.

At the 14 March 2026 investment committee meeting, Chief Investment Officer Daniel Okafor made two remarks.
"Model C explains the most variation in Brightwater's returns, so it should be the model we both report and use for scenario analysis."
"Adjusted R-squared fell when CMA was added, which I suppose happens whenever a factor fails a 5% significance test."

Anand replied that the report must separate the question of which specification fits best from the question of which specification should drive forward-looking scenarios.
She also proposed a formal test of whether RMW and CMA together belong in the model.

## Questions

1. The R-squared and adjusted R-squared of Model C are closest to: (LOS: los-01-02-a)
   - A. 0.323 and 0.272
   - B. 0.677 and 0.653
   - C. 0.677 and 0.658
2. The F-statistic for the test that all five slope coefficients of Model C equal zero, and the conclusion at the 5% level, are: (LOS: los-01-02-b)
   - A. 2.10; fail to reject the null hypothesis
   - B. 23.06; reject the null hypothesis
   - C. 27.68; reject the null hypothesis
3. Regarding Okafor's second remark, the change in adjusted R-squared from Model B to Model C is most accurately explained as follows: (LOS: los-01-02-a)
   - A. Adjusted R-squared fell because the absolute value of the CMA t-statistic is below 1.0.
   - B. Adjusted R-squared fell because R-squared fell when CMA was added.
   - C. Adjusted R-squared fell because any factor that is not significant at the 5% level lowers adjusted R-squared.
4. Using the information criteria, the model that provides the best goodness of fit and the model that should drive the scenario analysis are, respectively: (LOS: los-01-02-a)
   - A. Model A and Model B
   - B. Model C and Model C
   - C. Model B and Model A
5. Using Model C and the assumptions in Exhibit 4, Brightwater's predicted excess return for next month is closest to: (LOS: los-01-02-c)
   - A. 1.388%
   - B. 1.523%
   - C. 1.568%
6. For the test Anand proposed at the 5% level, the joint F-statistic and the conclusion are: (LOS: los-01-02-b)
   - A. 1.59; fail to reject that the RMW and CMA coefficients are both zero
   - B. 1.62; fail to reject that the RMW and CMA coefficients are both zero
   - C. 3.24; reject that the RMW and CMA coefficients are both zero

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** $R^2 = SSR / SST = 352.35 / 520.40 = 0.67708$.
>    $\bar{R}^2 = 1 - \left(\frac{n-1}{n-k-1}\right)(1 - R^2) = 1 - (71 / 66)(0.32292) = 1 - 0.34739 = 0.65261$.
>    A is wrong because it takes $SSE / SST = 0.32292$ as R-squared and then adjusts that figure, $1 - (71 / 66)(0.67708) = 0.27163$.
>    C is wrong because it uses $n - k = 67$ in the degrees-of-freedom factor, giving $1 - (71 / 67)(0.32292) = 0.65780$.
> 2. **C.** $H_0: b_{MKT} = b_{SMB} = b_{HML} = b_{RMW} = b_{CMA} = 0$ against $H_a$: at least one slope is not zero.
>    $MSR = 352.35 / 5 = 70.4700$ and $MSE = 168.05 / 66 = 2.5462$, so $F = 70.4700 / 2.5462 = 27.6764$.
>    27.68 exceeds $F_{0.05}(5, 66) = 2.354$, so reject; at least one slope differs from zero.
>    A is wrong because it divides the sums of squares without their degrees of freedom, $352.35 / 168.05 = 2.0967$, and then fails to reject.
>    B is wrong because it counts the intercept in the numerator degrees of freedom, $(352.35 / 6) / 2.5462 = 23.0637$; the conclusion is right but the statistic is not.
> 3. **A.** Adjusted R-squared falls from 0.6567 to 0.6526 even though R-squared rises from 0.6760 to 0.6771.
>    Adjusted R-squared rises when a variable is added only if the absolute value of its t-statistic exceeds 1.0, and CMA's t-statistic is -0.46.
>    Cross-check: the nested F for CMA alone is $(168.60 - 168.05) / (168.05 / 66) = 0.2160$, and $\sqrt{0.2160} = 0.4648$, matching the printed $|t|$ to rounding.
>    B is wrong because R-squared cannot fall when a variable is added; it rose from 0.6760 to 0.6771.
>    C is wrong because the threshold is $|t| > 1$, not 5% significance; RMW had $t = 1.75$, below the 5% critical value of 1.997, yet adjusted R-squared rose from 0.6463 to 0.6567 when it was added.
> 4. **A.** BIC is the criterion for best goodness of fit and AIC the criterion for prediction, and lower is better for both.
>    BIC is lowest for Model A (81.58 versus 82.65 and 86.69); AIC is lowest for Model B (71.26 versus 72.48 and 73.03).
>    Adjusted R-squared is highest for Model B, which is why the stem names the information criteria: BIC is the curriculum's criterion for the best fit and it carries the heavier parameter penalty of $\ln(72) = 4.277$ against AIC's 2.
>    B is wrong because it picks on R-squared, which is always highest for the largest model; Model C has the worst AIC and the worst BIC.
>    C is wrong because it swaps the criteria, using AIC for fit and BIC for prediction.
> 5. **C.** $\hat{Y} = 0.18 + 1.06(1.20) + 0.48(-0.40) + 0.31(0.60) + 0.22(0.35) - 0.09(-0.50)$.
>    Terms: $0.18 + 1.2720 - 0.1920 + 0.1860 + 0.0770 + 0.0450 = 1.5680$, a predicted excess return of 1.568%.
>    The Momentum assumption is ignored because Momentum is not in Model C.
>    A is wrong because it omits the intercept, $1.568 - 0.180 = 1.388$; the intercept is always included.
>    B is wrong because it drops the insignificant CMA term, $1.568 - 0.045 = 1.523$; every variable in the estimated model stays in the forecast.
> 6. **B.** $H_0: b_{RMW} = b_{CMA} = 0$ against $H_a$: at least one is not zero; the restricted model is Model A and the unrestricted model is Model C, with $q = 2$ and $n - k - 1 = 66$.
>    $F = \frac{(176.30 - 168.05) / 2}{168.05 / 66} = \frac{4.1250}{2.5462} = 1.6201$.
>    1.62 is below $F_{0.05}(2, 66) = 3.136$, so fail to reject; RMW and CMA do not jointly add explanatory power at 5%.
>    A is wrong because it divides by the restricted model's error variance, $176.30 / 68 = 2.5926$, giving $4.1250 / 2.5926 = 1.5910$.
>    C is wrong because it does not divide the rise in SSE by $q$, $8.25 / 2.5462 = 3.2401$, which also flips the decision.

## Distractor design

1. A: R-squared computed as $SSE / SST$ instead of $SSR / SST$; C: wrong degrees-of-freedom factor ($n - k$ instead of $n - k - 1$).
2. A: sums of squares divided without degrees of freedom; B: intercept counted in the numerator degrees of freedom ($k + 1$).
3. B: believes R-squared can fall when a variable is added; C: confuses the $|t| > 1$ threshold for adjusted R-squared with 5% significance.
4. B: selects on R-squared, which always favours the largest model; C: AIC and BIC purposes swapped.
5. A: intercept omitted; B: insignificant variable dropped from the forecast.
6. A: restricted model's MSE used in the denominator; C: rise in SSE not divided by $q$.
