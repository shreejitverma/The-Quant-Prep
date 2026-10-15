---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 1
title: "Quillon Capital Five-Factor Allocation"
los: [los-01-01-a, los-01-01-b, los-01-01-c]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Quillon Capital Five-Factor Allocation

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Tobias Lindqvist is a senior research analyst at Harbourline Family Office, which is considering a USD 40 million allocation to the Quillon Capital long-short equity fund.
To value the fund's expected return against its fee load, Lindqvist models Quillon's monthly excess return over the risk-free rate (RETRF) with a five-factor model.
The independent variables are the market excess return (MKTRF), the size factor (SMB), the value factor (HML), the profitability factor (RMW), and the investment factor (CMA).
All returns in the regression are measured in whole percentages, so a 1.5% return is entered as 1.5.
The sample contains 96 monthly observations.

**Exhibit 1: Regression of Quillon RETRF on five factors (96 months)**

| Variable | Coefficient | Standard error |
|---|---|---|
| Intercept | 0.42 | 0.25 |
| MKTRF | 0.78 | 0.09 |
| SMB | 0.35 | 0.21 |
| HML | -0.52 | 0.17 |
| RMW | 0.61 | 0.24 |
| CMA | -0.29 | 0.19 |
| R-squared | 0.6840 | |
| Mean RETRF over the sample | 0.97 | |

The two-tailed 5% critical t-value for the residual degrees of freedom is 1.99.

Harbourline's strategy team circulates a factor outlook for next month in decimal form, as it is used elsewhere in the firm's risk system.

**Exhibit 2: Factor outlook for next month (decimal form)**

| MKTRF | SMB | HML | RMW | CMA |
|---|---|---|---|---|
| 0.012 | -0.004 | 0.006 | 0.003 | -0.002 |

Lindqvist's associate, Aiko Brandt, reviews the model and reports three observations.

First, in the scatterplot matrix, the plot of RETRF against RMW shows almost no slope, and the fitted line is nearly flat inside a wide confidence band.

Second, she standardizes each residual by dividing it by the standard error of the estimate and prepares a normal Q-Q plot.
Eleven of the 96 standardized residuals lie below -1.65, and the lowest points bend well below the diagonal beyond -2.

Third, she proposes adding a quality factor, QUAL, which Harbourline's data vendor constructs each month as exactly RMW minus CMA, to capture quality exposure more directly.

In a separate note dated 12 May, Brandt suggests a second model for the investment committee.
The dependent variable would equal 1 if Quillon beats its 8% annual hurdle rate in a given year and 0 otherwise, with the five factor averages and a dummy variable for recession years as the independent variables.
Lindqvist replies on 13 May: "Dummy variables are allowed in multiple linear regression, so we can estimate your hurdle model with the same ordinary least squares routine."

## Questions

1. Using Exhibits 1 and 2, the predicted RETRF for Quillon next month is closest to: (LOS: los-01-01-b)
   - A. 0.43%
   - B. 1.03%
   - C. 1.15%
2. At the 5% significance level, which of the following slope coefficients in Exhibit 1 is not statistically different from zero? (LOS: los-01-01-b)
   - A. SMB
   - B. HML
   - C. RMW
3. Brandt's first observation, together with the regression output, is best explained by the fact that: (LOS: los-01-01-c)
   - A. the regression is misspecified, because a significant coefficient must appear as a sloped pairwise scatterplot.
   - B. the scatterplot shows the unconditional relation between RETRF and RMW, whereas the RMW coefficient is a partial effect after controlling for the other four factors.
   - C. heteroskedastic residuals have inflated the RMW t-statistic, so RMW should be removed.
4. Based on Brandt's second observation, the most appropriate conclusion is that: (LOS: los-01-01-c)
   - A. about 10 standardized residuals would be expected below -1.65 under normality, so the residuals are consistent with a normal distribution.
   - B. about 5 standardized residuals would be expected below -1.65 under normality, so the residuals appear fat-tailed and the normality assumption is in doubt.
   - C. about 5 standardized residuals would be expected below -1.65 under normality, so the residual variance is not constant across observations.
5. If QUAL is added to the model as proposed in Brandt's third observation, the most likely consequence is that: (LOS: los-01-01-c)
   - A. the model cannot be estimated, because there is an exact linear relation among the independent variables.
   - B. the model can be estimated, but the coefficients on RMW, CMA and QUAL will be difficult to interpret.
   - C. the errors will no longer be independent, because QUAL is built from factors already in the model.
6. Regarding the 12 May and 13 May notes, the most appropriate approach for the hurdle model is: (LOS: los-01-01-a)
   - A. multiple linear regression, because the recession dummy is a legitimate independent variable.
   - B. logistic regression, because the dependent variable is discrete.
   - C. simple linear regression on the recession dummy alone, because the hurdle outcome is driven by the business cycle.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The model is estimated in whole percentages, so the decimal outlook must be converted first: MKTRF 1.2, SMB $-0.4$, HML 0.6, RMW 0.3, CMA $-0.2$.
> $0.78 \times 1.2 = 0.9360$.
> $0.35 \times (-0.4) = -0.1400$.
> $-0.52 \times 0.6 = -0.3120$.
> $0.61 \times 0.3 = 0.1830$.
> $-0.29 \times (-0.2) = +0.0580$.
> $\widehat{RETRF} = 0.42 + 0.9360 - 0.1400 - 0.3120 + 0.1830 + 0.0580 = 1.1450$, or about 1.15% (V1 p.8).
> A (0.43%) is wrong because it plugs the decimal outlook into a whole-percent model: $0.42 + 0.00936 - 0.0014 - 0.00312 + 0.00183 + 0.00058 = 0.4272$.
> B (1.03%) is wrong because it treats the CMA term as negative, missing that a negative slope times a negative factor return adds to return: $1.1450 - 2(0.0580) = 1.0290$.
> 2. **A.** Each t-statistic is the coefficient divided by its standard error (V1 p.12).
> SMB: $0.35 / 0.21 = 1.6667$, below 1.99 in absolute value, so not significant.
> HML: $-0.52 / 0.17 = -3.0588$, with $|t| = 3.0588 > 1.99$, significant.
> RMW: $0.61 / 0.24 = 2.5417 > 1.99$, significant.
> CMA ($-0.29 / 0.19 = -1.5263$) is also not significant, but it is not among the choices.
> B is wrong because it compares the signed t-statistic of $-3.0588$ with $+1.99$ as if the test were one-sided in the positive direction; a two-tailed test uses the absolute value.
> C is wrong because it picks the slope with the largest standard error, 0.24, without dividing the coefficient by it.
> 3. **B.** A pairwise scatterplot is an unconditional picture of two variables, while a multiple regression slope is a partial coefficient measured with the other independent variables held constant; a factor can look flat in isolation and still be significant once the others are controlled for, as with SMB in the curriculum's ABC example (V1 p.12).
> A is wrong because there is no contradiction to resolve; the two facts are compatible.
> C is wrong because nothing in the vignette points to heteroskedasticity, and heteroskedasticity is diagnosed from residuals versus predicted values, not from a flat Y-versus-X scatter.
> 4. **B.** Under normality about 5% of standardized residuals fall below $-1.65$ (V1 p.16), so the expected count is $0.05 \times 96 = 4.8$, about 5.
> Eleven observations, more than twice the expected number, plus lower-tail points bending below the diagonal past $-2$, indicate a fat left tail, so the residuals are not normal (V1 p.19).
> A is wrong because it uses 10% ($0.10 \times 96 = 9.6$), the two-tailed probability beyond $\pm 1.65$, for a one-tail count.
> C is wrong because a Q-Q plot tests normality; departures in the tails indicate fat tails, not heteroskedasticity, which is read from the residuals-versus-predicted plot.
> 5. **A.** QUAL equals RMW minus CMA in every month, so $QUAL - RMW + CMA = 0$ for all observations; this is an exact linear relation among independent variables, a violation of assumption 5b, and the model cannot be estimated (V1 p.10).
> B is wrong because "estimable but hard to interpret" describes an approximate linear relation, such as highly correlated factors, not an exact one.
> C is wrong because independence of errors concerns correlation between residuals across observations, not how the regressors are constructed; the shared word "independence" is the trap.
> 6. **B.** The first fork of the regression process asks whether the dependent variable is continuous; a 0/1 hurdle outcome is discrete, so the model is a logistic regression (V1 pp.5-6).
> A is wrong because dummy variables are legitimate on the right-hand side, but the problem here is the dummy on the left-hand side.
> C is wrong because it leaves the dependent variable discrete and discards the five factors without any diagnostic reason.

## Distractor design

- Q1: A is a units error (decimal inputs into a whole-percent model); B is a sign error on the product of two negatives.
- Q2: B compares a signed t-statistic with a positive critical value (one-sided misreading of a two-tailed test); C picks the largest standard error instead of computing the t-statistic.
- Q3: A treats pairwise and partial relations as the same thing; C assigns the pattern to the wrong assumption and the wrong chart.
- Q4: A uses the two-tailed probability for a one-tail count; C reads a Q-Q tail departure as heteroskedasticity.
- Q5: B confuses exact with approximate collinearity; C is the "independence" word trap.
- Q6: A confuses a dummy independent variable with a dummy dependent variable; C drops to simple regression, a step the process does not provide.
