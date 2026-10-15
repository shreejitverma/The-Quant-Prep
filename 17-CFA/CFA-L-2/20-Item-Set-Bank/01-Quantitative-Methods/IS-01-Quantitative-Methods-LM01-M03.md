---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 1
title: "Pellham Savings Bank Valuation Screen"
los: [los-01-01-a, los-01-01-b, los-01-01-c]
difficulty: 4
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Pellham Savings Bank Valuation Screen

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Selin Marchetti, CFA, is a financials analyst at Wexcombe Partners, an event-driven fund that looks for mispriced regional banks.
To screen for relative value, she estimates a cross-sectional multiple linear regression of the price-to-book ratio (P/B, in times) of 64 listed regional banks at the end of the latest fiscal year.
The independent variables are return on equity (ROE), the common equity tier 1 ratio (CET1), the nonperforming loan ratio (NPL), and a dummy variable (WEALTH) equal to 1 if the bank owns a wealth management unit and 0 otherwise.
ROE is net income divided by average common equity, CET1 is CET1 capital divided by risk-weighted assets, and NPL is nonperforming loans divided by gross loans.
All three ratios are entered in whole percentages, so 9.5% is entered as 9.5.

**Exhibit 1: Regression of P/B on ROE, CET1, NPL and WEALTH (64 banks)**

| Variable | Coefficient |
|---|---|
| Intercept | 0.200 |
| ROE | 0.085 |
| CET1 | 0.040 |
| NPL | -0.120 |
| WEALTH | 0.150 |
| R-squared | 0.74 |
| Mean P/B of the 64 banks | 1.16 |

Marchetti's first target is Pellham Savings Bank, which has no wealth management unit and whose shares trade at 1.18 times book value.
Pellham issued new common equity during the year.

**Exhibit 2: Pellham Savings Bank, selected data for the latest fiscal year (millions)**

| Item | Amount |
|---|---|
| Net income | 84 |
| Common equity, beginning of year | 640 |
| Common equity, end of year | 760 |
| CET1 capital | 690 |
| Risk-weighted assets | 5,750 |
| Total assets | 9,200 |
| Gross loans | 6,000 |
| Nonperforming loans | 138 |
| Loan loss reserves | 96 |

Pellham's management has announced a share buyback that it expects to reduce the CET1 ratio by 1.5 percentage points.
Marchetti wants to know how much ROE would have to improve for the model's predicted P/B to be unaffected by the buyback.

Her associate, Ansel Okafor, sorts the 64 banks into quintiles by fitted P/B and summarizes the residuals in each group.

**Exhibit 3: Residuals by quintile of fitted P/B**

| Quintile | Fitted P/B range | Banks | Mean residual | Standard deviation of residuals |
|---|---|---|---|---|
| 1 (lowest) | 0.55 to 0.85 | 13 | 0.004 | 0.060 |
| 2 | 0.85 to 1.05 | 13 | -0.006 | 0.085 |
| 3 | 1.05 to 1.25 | 13 | 0.002 | 0.130 |
| 4 | 1.25 to 1.50 | 13 | 0.005 | 0.190 |
| 5 (highest) | 1.50 to 2.10 | 12 | -0.005 | 0.270 |

On 14 April, Okafor writes: "The overall F-test is significant at the 1% level, the R-squared is 0.74, and this specification beat the two alternatives we tried, so the screen is ready to rank banks."
On 15 April, Wexcombe's risk manager, Dora Lindgren, replies: "P/B can never be negative, so the model should be re-estimated as a logistic regression before we rely on it."
Marchetti decides to settle the question by following the regression process strictly.

## Questions

1. Using Exhibits 1 and 2, the predicted P/B for Pellham Savings Bank is closest to: (LOS: los-01-01-b)
   - A. 1.24
   - B. 1.34
   - C. 1.42
2. Holding NPL and WEALTH constant, the increase in Pellham's ROE needed to leave its predicted P/B unchanged after the buyback is closest to: (LOS: los-01-01-b)
   - A. 0.47 percentage points.
   - B. 0.71 percentage points.
   - C. 3.19 percentage points.
3. Based on Exhibit 3, the most accurate statement is that the residual variance in the highest quintile is about: (LOS: los-01-01-c)
   - A. 4.5 times that in the lowest quintile, indicating heteroskedasticity.
   - B. 20.3 times that in the lowest quintile, indicating heteroskedasticity.
   - C. 20.3 times that in the lowest quintile, indicating that the relationship between P/B and the independent variables is not linear.
4. Regarding the 14 April and 15 April statements, the most appropriate next step under the regression process is to: (LOS: los-01-01-a)
   - A. use the model to rank banks, because the overall fit is significant and the specification is the best of the candidates.
   - B. re-estimate the model as a logistic regression, because P/B is bounded below by zero.
   - C. adjust the model and re-estimate it, because the residual analysis shows that a regression assumption is not satisfied.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Build each ratio to the model's definitions, in whole percentages, before applying the estimated equation (V1 p.8).
> Average equity: $(640 + 760) / 2 = 700$, so $ROE = 84 / 700 = 12.0000\%$.
> $CET1 = 690 / 5{,}750 = 12.0000\%$.
> $NPL = 138 / 6{,}000 = 2.3000\%$, and $WEALTH = 0$.
> $0.085 \times 12.0 = 1.0200$; $0.040 \times 12.0 = 0.4800$; $-0.120 \times 2.3 = -0.2760$.
> $\widehat{P/B} = 0.200 + 1.0200 + 0.4800 - 0.2760 + 0 = 1.4240$, about 1.42.
> A (1.24) is wrong because it divides CET1 capital by total assets instead of risk-weighted assets: $690 / 9{,}200 = 7.5000\%$, and $0.200 + 1.0200 + 0.040 \times 7.5 - 0.2760 = 1.2440$.
> B (1.34) is wrong because it computes ROE on ending equity, $84 / 760 = 11.0526\%$, even though the model defines ROE on average equity and Pellham issued equity during the year: $0.200 + 0.085 \times 11.0526 + 0.4800 - 0.2760 = 1.3435$.
> The market P/B of 1.18, the mean P/B of 1.16, and the loan loss reserves are not inputs to the prediction.
> 2. **B.** Each slope is a partial effect with the other independent variables held constant (V1 p.8).
> The buyback changes predicted P/B by $0.040 \times (-1.5) = -0.0600$.
> An ROE increase of $\Delta ROE$ adds $0.085 \times \Delta ROE$, so setting the sum to zero gives $\Delta ROE = 0.0600 / 0.085 = 0.7059$ percentage points, about 0.71.
> A (0.47) is wrong because it computes the offset for a one-point change in CET1 rather than the announced 1.5 points: $0.040 / 0.085 = 0.4706$.
> C (3.19) is wrong because it inverts the slope ratio, $0.085 \times 1.5 / 0.040 = 3.1875$, which is the CET1 change that would offset a 1.5-point ROE change.
> 3. **B.** Variance is the square of the standard deviation, so the ratio is $0.270^2 / 0.060^2 = 0.0729 / 0.0036 = 20.25$, about 20.3.
> The residual spread rises steadily from 0.060 to 0.270 as the fitted P/B rises, the fanning pattern in a residuals-versus-predicted analysis that indicates a violation of homoskedasticity, the assumption that the residual variance is the same for all observations (V1 p.10, p.18).
> The mean residual stays close to zero in every quintile, with no systematic sign pattern, so nothing in Exhibit 3 points to a curved relationship.
> A is wrong because it compares standard deviations, $0.270 / 0.060 = 4.5$, and reports the result as a variance ratio.
> C is wrong because it pairs the correct ratio with the wrong assumption; a linearity problem would show as mean residuals that change sign systematically across the fitted range, not as widening dispersion around a zero mean.
> 4. **C.** After estimation, the first gate of the regression process is whether the assumptions are satisfied, and a no at that gate routes to adjusting the model and re-estimating it (V1 pp.6-7).
> Question 3 shows that the homoskedasticity assumption fails, so the fit, significance, and best-model results that Okafor cites cannot yet be relied on, because those statistics depend on the assumptions (V1 p.10).
> A is wrong because it skips the assumption gate; a significant F-test and a high R-squared come later in the process and do not override a failed assumption check.
> B is wrong because the choice of logistic regression is made at the first fork, when the dependent variable is discrete, such as a 0/1 flag (V1 p.5); P/B is continuous, and a lower bound at zero does not make it discrete.

## Distractor design

- Q1: A divides CET1 capital by total assets instead of risk-weighted assets (misread exhibit); B computes ROE on ending instead of average equity (wrong formula variant).
- Q2: A drops the 1.5-point size of the CET1 change (per-unit error); C inverts the ratio of the two partial slopes (swapped roles of the variables).
- Q3: A reports a standard deviation ratio as a variance ratio; C attaches the correct ratio to the linearity assumption instead of homoskedasticity (wrong assumption).
- Q4: A skips the assumption gate in favour of fit and model comparison; B applies the discrete-dependent-variable fork to a bounded but continuous variable.
