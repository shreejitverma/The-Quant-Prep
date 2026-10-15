---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 1
title: "Kestrel Retirement System Credit Sleeve"
los: [los-01-01-a, los-01-01-b, los-01-01-c]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Kestrel Retirement System Credit Sleeve

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Marisol Achebe, CFA, is the fixed-income strategist at the Kestrel Municipal Employees' Retirement System, a public defined-benefit plan.
The plan holds an investment-grade corporate bond sleeve that is benchmarked to a broad corporate index.
Before the quarterly investment committee meeting, Achebe must decide whether to add a duration overlay to the sleeve.
To support the decision, she estimates a multiple linear regression of the sleeve's monthly excess return over Treasuries (RET) on three drivers.
The drivers are the monthly change in the 10-year government bond yield (BY), the monthly change in the index option-adjusted credit spread (CS), and the monthly excess return of a broad equity index (EQ).
All variables are measured in decimal form, so a yield rise of 25 basis points is entered as 0.0025.
The sample covers 72 months.

Exhibit 1 shows the estimation output.

**Exhibit 1: Regression of RET on BY, CS and EQ (72 monthly observations)**

| Variable | Coefficient | Standard error |
|---|---|---|
| Intercept | 0.0018 | 0.0009 |
| BY | -6.2140 | 0.4130 |
| CS | -3.4075 | 0.6210 |
| EQ | 0.0850 | 0.0310 |
| R-squared | 0.8120 | |
| Mean of BY over the sample | 0.0003 | |

Achebe's analyst, Jonah Pellerin, separately regresses RET on CS alone over the same 72 months and obtains a slope of -1.9500.
He also regresses RET on BY alone and obtains a slope of -4.8000.

For the committee, Achebe builds a forward-looking scenario for next month.
She assumes the 10-year yield rises by 40 basis points, the credit spread narrows by 15 basis points, and the equity index delivers an excess return of 2.00%.
Her desk's separate view is that credit spreads will widen by 10 basis points over the following month, but that view is not part of the committee scenario.

Pellerin makes three statements in a memo dated 3 March.

Statement 1: "The CS slope from my single-variable regression, -1.9500, is the better measure of the sleeve's spread sensitivity because it relies on fewer variables and is therefore less exposed to estimation error."

Statement 2: "The residuals from the three-variable model widen noticeably as the predicted return rises, but the R-squared of 0.8120 is high enough that we can use the model for the committee scenario as it stands."

Statement 3: "When I plot the residuals in time order, positive residuals tend to be followed by positive residuals and negative by negative, producing long runs of the same sign across 2021 and 2022."

Achebe replies on 4 March that she will only present the scenario to the committee once the model has passed every step of the regression process.
She also asks Pellerin to explain in plain language what the intercept and the BY coefficient mean, because several trustees have no quantitative background.

## Questions

1. Regarding Statement 1, the most appropriate response is that the CS coefficient to use for spread sensitivity is: (LOS: los-01-01-b)
   - A. -1.9500, because a single-variable slope captures the total effect of spreads on the sleeve.
   - B. -3.4075, because it measures the change in RET for a one-unit change in CS holding BY and EQ constant.
   - C. -3.4057, because the intercept must be added to the partial slope to obtain the sleeve's spread sensitivity.
2. Using Exhibit 1 and Achebe's committee scenario, the predicted excess return of the sleeve for next month is closest to: (LOS: los-01-01-b)
   - A. -0.0265
   - B. -0.0180
   - C. -0.0162
3. If the 10-year yield rises by 25 basis points and all other independent variables are unchanged, the predicted change in RET is closest to: (LOS: los-01-01-b)
   - A. -0.0120
   - B. -0.0155
   - C. -0.0189
4. The most appropriate plain-language explanation of the intercept for the trustees is that the sleeve is expected to earn approximately: (LOS: los-01-01-b)
   - A. 2.16% per year over Treasuries when the yield and the credit spread are unchanged and the equity index excess return is zero.
   - B. 0.18% per year over Treasuries when the yield and the credit spread are unchanged and the equity index excess return is zero.
   - C. 2.16% per year over Treasuries when the yield change, spread change and equity excess return are at their sample means.
5. Given the residual pattern described in Statement 2, the step Achebe should require under the regression process is to: (LOS: los-01-01-a)
   - A. adjust the model and re-estimate it before evaluating goodness of fit.
   - B. use the model for the committee scenario, because the overall fit is strong.
   - C. switch to logistic regression, because the residuals are not well behaved.
6. The pattern described in Statement 3 most likely indicates a violation of which regression assumption? (LOS: los-01-01-c)
   - A. Independence of the independent variables
   - B. Independence of errors
   - C. Normality of the residuals

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** A slope in a multiple regression is a partial regression coefficient: $-3.4075$ is the change in RET for a one-unit change in CS with BY and EQ held constant (V1 p.8).
> Because yields and spreads tend to move together, the single-variable slope of $-1.9500$ mixes the spread effect with whatever CS shares with the omitted BY and EQ, so it is not a cleaner measure.
> A is wrong because it treats the pairwise, unconditional slope as the sensitivity of interest and ignores that the omitted drivers are pushed into the error term.
> C is wrong because $-3.4075 + 0.0018 = -3.4057$ adds the intercept to the slope, which is not an interpretation of any coefficient.
> 2. **C.** Enter the scenario in decimals: $BY = 0.0040$, $CS = -0.0015$, $EQ = 0.0200$.
> $-6.2140 \times 0.0040 = -0.024856$.
> $-3.4075 \times (-0.0015) = +0.005111$.
> $0.0850 \times 0.0200 = +0.001700$.
> $\widehat{RET} = 0.0018 - 0.024856 + 0.005111 + 0.001700 = -0.016245$, or about $-0.0162$.
> A ($-0.0265$) is wrong because it treats the spread term as negative, ignoring that a narrowing spread times a negative slope adds to return: $0.0018 - 0.024856 - 0.005111 + 0.0017 = -0.026467$.
> B ($-0.0180$) is wrong because it omits the intercept: $-0.024856 + 0.005111 + 0.0017 = -0.018045$.
> 3. **B.** With CS and EQ held constant, only the BY term changes: $\Delta \widehat{RET} = -6.2140 \times 0.0025 = -0.015535$, about $-0.0155$ (V1 p.8).
> The slope of $-6.2140$ is the sleeve's empirical duration.
> A ($-0.0120$) is wrong because it uses the single-variable BY slope from Pellerin's separate regression: $-4.8000 \times 0.0025 = -0.0120$.
> C ($-0.0189$) is wrong because it also adds the desk's 10 basis point spread view, which violates "all other variables unchanged": $-0.015535 - 3.4075 \times 0.0010 = -0.018943$.
> 4. **A.** The intercept is the expected value of RET when every independent variable equals zero (V1 p.4).
> Here $0.0018$ per month, annualised by simple multiplication as in the curriculum's bond example, is $0.0018 \times 12 = 0.0216$, or 2.16% per year (V1 p.8).
> B is wrong because it reports the monthly figure, 0.18%, as an annual one.
> C is wrong because the intercept is conditional on all Xs being zero, not on the Xs being at their sample means; the sample mean of BY in Exhibit 1 is a decoy.
> 5. **A.** Residual variance that rises with the predicted value is heteroskedasticity, so the answer to "Are the assumptions satisfied?" is no, and every no in the process flowchart routes to "adjust the model and re-estimate" (V1 pp.6-7).
> Assumptions are checked before goodness of fit, because fit and test statistics rely on the assumptions.
> B is wrong because a high R-squared does not allow the analyst to skip the assumption gate.
> C is wrong because logistic regression is chosen at the first fork when the dependent variable is discrete, and RET is continuous.
> 6. **B.** Independence of errors requires residuals to be uncorrelated across observations; long runs of same-signed residuals in time order show that one month's residual predicts the next, the assumption most often broken with time-series data (V1 p.10).
> A is wrong because independence of the independent variables concerns linear relations among BY, CS and EQ, not the residuals; the shared word "independence" is the trap.
> C is wrong because normality is judged from a normal Q-Q plot of the residuals, not from their ordering in time.

## Distractor design

- Q1: A is the pairwise-versus-partial error (using a simple-regression slope); C is the intercept-plus-slope error.
- Q2: A is a sign error on the product of two negatives (CS narrowing); B omits the intercept.
- Q3: A uses the wrong model's slope (misread exhibit, single-variable regression); C breaks the ceteris paribus clause by adding the spread view.
- Q4: B is a period error (monthly stated as annual); C confuses "all Xs equal zero" with "all Xs at their means".
- Q5: B skips the assumption gate in favour of fit; C applies the discrete-dependent-variable fork to a continuous Y.
- Q6: A is the "independence" word trap; C assigns the pattern to the Q-Q plot's assumption.
