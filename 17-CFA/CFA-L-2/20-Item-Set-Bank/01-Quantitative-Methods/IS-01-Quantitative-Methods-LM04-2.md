---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 4
title: "Ridgeline Appraisal: Warehouse Price Model"
los: [los-01-04-b, los-01-04-a]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Ridgeline Appraisal: Warehouse Price Model

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Ridgeline Appraisal Partners values industrial property for lenders and real estate funds.
Senior appraiser Marcus Oyelaran, CFA, is building a model to value logistics warehouses in a regional distribution corridor.
He collects 85 arm's-length warehouse sales from the past three years.

Each warehouse lies in one of three location categories: inland, suburban, or port-adjacent.
Oyelaran expects port-adjacent warehouses to trade at a premium and also to lose value faster with age, because tenants at the port need modern loading equipment.
He specifies the following model:

$$
PRICE_i = b_0 + b_1 AGE_i + d_1 SUB_i + d_2 PORT_i + d_3 (PORT_i \times AGE_i) + \varepsilon_i
$$

PRICE is the sale price in dollars per square foot, AGE is the building age in years, SUB equals 1 for a suburban warehouse and 0 otherwise, and PORT equals 1 for a port-adjacent warehouse and 0 otherwise.
The results are shown in Exhibit 1.

**Exhibit 1: Warehouse price regression (n = 85)**

| | Coefficient | Standard error |
|---|---|---|
| Intercept | 142.00 | 6.20 |
| AGE | -2.40 | 0.31 |
| SUB | 11.50 | 4.10 |
| PORT | 36.00 | 5.30 |
| PORT_AGE | -1.10 | 0.40 |

Sum of squared errors = 15,120; $R^2$ = 0.620; mean AGE = 18.4 years; mean PRICE = $118.60 per square foot.
Two-tailed 5% critical t-value with 80 degrees of freedom = 1.990.

To test whether location matters at all, Oyelaran also estimates a restricted model with AGE as the only independent variable.
Its sum of squared errors is 21,450.
The 5% critical F-value with 3 and 80 degrees of freedom is 2.72, and with 4 and 80 degrees of freedom it is 2.49.

A junior analyst, Hannah Brandt, reviews the specification.
She suggests adding a third location dummy, INLAND, "so that every location has its own coefficient and none is left out."

Oyelaran has two client requests.
First, a lender wants the model value of a 12-year-old port-adjacent warehouse.
Second, a fund choosing between a port-adjacent site and a suburban site asks at what building age the model would assign the two locations the same price per square foot.

Before finalizing, Oyelaran reviews the influence diagnostics for three sales that stood out in a scatterplot (Exhibit 2).

**Exhibit 2: Influence diagnostics, selected sales**

| Sale | Location | AGE | Leverage $h_{ii}$ | Studentized deleted residual $t_i^*$ |
|---|---|---|---|---|
| W-17 | Port | 61 | 0.21 | 0.40 |
| W-52 | Suburban | 9 | 0.16 | -2.35 |
| W-66 | Inland | 22 | 0.09 | 3.40 |

The two-tailed 5% critical t-value with 79 degrees of freedom is 1.990.

## Questions

1. If Oyelaran adopts Brandt's suggestion and re-estimates the model with an intercept, the most likely result is that: (LOS: los-01-04-b)
   - A. the INLAND coefficient will equal the intercept in Exhibit 1, 142.00.
   - B. the model cannot be estimated because the three location dummies sum to the intercept column.
   - C. the model will fit better because each location is measured against its own base.
2. The model value per square foot of the 12-year-old port-adjacent warehouse is closest to: (LOS: los-01-04-b)
   - A. $136.00.
   - B. $149.20.
   - C. $164.80.
3. The building age at which the model assigns the same price per square foot to a port-adjacent and a suburban warehouse is closest to: (LOS: los-01-04-b)
   - A. 7.0 years.
   - B. 22.3 years.
   - C. 32.7 years.
4. Which statement about the effect of age on port-adjacent warehouses is most accurate? (LOS: los-01-04-b)
   - A. Port-adjacent warehouses lose $1.10 per square foot per year of age, and this slope differs significantly from the inland slope.
   - B. Port-adjacent warehouses lose $3.50 per square foot per year of age, and this slope differs significantly from the inland slope.
   - C. Port-adjacent warehouses lose $3.50 per square foot per year of age, but this slope does not differ significantly from the inland slope.
5. The F-statistic for the joint test that the three location variables (SUB, PORT, PORT_AGE) are all equal to zero is closest to: (LOS: los-01-04-b)
   - A. 7.87.
   - B. 11.16.
   - C. 33.49.
6. Based on Exhibit 2, which statement is most accurate? (LOS: los-01-04-a)
   - A. W-17 is the only high-leverage sale, while W-52 and W-66 are flagged by their studentized deleted residuals.
   - B. W-17 and W-52 are both high-leverage sales, and W-17 should be removed because its leverage exceeds the cutoff.
   - C. W-66 is the only flagged sale, because it is the only one with a studentized deleted residual above 3.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** With three categories only $3 - 1 = 2$ dummies may be used alongside an intercept.
> Adding INLAND makes $INLAND + SUB + PORT = 1$ for every sale, an exact linear relationship with the intercept column (the dummy variable trap), so the coefficients cannot be estimated.
> A is wrong because it treats the intercept as if it were a separate inland coefficient; the intercept already is the base group's level, which is why the inland dummy is omitted.
> C is wrong because dummy coefficients are always measured against one omitted base category; there is no "own base" for each location.
> 2. **A.** For PORT = 1, SUB = 0: $PRICE = (142.00 + 36.00) + (-2.40 - 1.10)(12) = 178.00 - 3.50 \times 12 = 178.00 - 42.00 = 136.00$.
> B is wrong because it ignores the slope dummy and uses the base slope: $178.00 - 2.40 \times 12 = 149.20$.
> C is wrong because it treats the interaction coefficient as the whole slope: $178.00 - 1.10 \times 12 = 164.80$.
> 3. **B.** Port minus suburban at age $A$: $\left[(142.00 + 36.00) - 3.50A\right] - \left[(142.00 + 11.50) - 2.40A\right] = 24.50 - 1.10A$.
> Setting this to zero gives $A = 24.50 / 1.10 = 22.2727$, about 22.3 years.
> Beyond that age the port-adjacent warehouse is valued below the suburban one, because the gap between groups depends on AGE when both intercept and slope dummies are present.
> A is wrong because it divides the intercept gap by the full port slope instead of the difference in slopes: $24.50 / 3.50 = 7.0$.
> C is wrong because it measures the gap against the inland base instead of the suburban group: $36.00 / 1.10 = 32.7273$.
> 4. **B.** The port slope on AGE is $b_1 + d_3 = -2.40 + (-1.10) = -3.50$ per year.
> The difference from the inland slope is $d_3$, tested with $t = -1.10 / 0.40 = -2.75$; $|{-2.75}| > 1.990$, so it is significant at 5%.
> A is wrong because $-1.10$ is the change in slope relative to inland, not the port slope itself.
> C is wrong because it compares the signed statistic, $-2.75 < 1.990$, instead of its absolute value.
> 5. **B.** $F = \frac{(SSE_R - SSE_U)/q}{SSE_U/(n - k - 1)} = \frac{(21{,}450 - 15{,}120)/3}{15{,}120/(85 - 4 - 1)} = \frac{2{,}110.0000}{189.0000} = 11.1640$.
> Since $11.16 > 2.72$, the location variables are jointly significant.
> A is wrong because it puts the restricted SSE in the denominator: $2{,}110.0 / (21{,}450/80) = 2{,}110.0 / 268.125 = 7.8695$.
> C is wrong because it does not divide the numerator by $q = 3$: $6{,}330 / 189.0 = 33.4921$.
> 6. **A.** Leverage cutoff $= 3(k+1)/n = 3 \times 5 / 85 = 0.1765$, so only W-17 (0.21) is high leverage; W-52 (0.16) is below it.
> With $n - k - 2 = 79$ degrees of freedom the critical value is 1.990, so W-52 ($|-2.35|$) and W-66 (3.40) are flagged; W-17's residual of 0.40 shows it sits close to the fitted line.
> B is wrong because it uses $3k/n = 12/85 = 0.1412$, which wrongly adds W-52, and because a flagged point should be investigated and refitted, not removed automatically.
> C is wrong because it applies the $|t^*| > 3$ outlier rule of thumb instead of the 5% critical value, missing W-52, and ignores the leverage measure entirely.

## Distractor design

- Q1: A = intercept misread as a category coefficient; C = belief that every category can have its own dummy (dummy variable trap).
- Q2: B = slope dummy ignored; C = interaction coefficient taken as the full slope.
- Q3: A = full slope used instead of slope difference; C = gap measured against the wrong base group (misread comparison).
- Q4: A = change in slope quoted as the slope; C = sign error in comparing a negative t-statistic.
- Q5: A = wrong SSE in the denominator; C = numerator not divided by the number of restrictions.
- Q6: B = cutoff $3k/n$ plus automatic deletion; C = outlier rule of thumb substituted for the significance test.
