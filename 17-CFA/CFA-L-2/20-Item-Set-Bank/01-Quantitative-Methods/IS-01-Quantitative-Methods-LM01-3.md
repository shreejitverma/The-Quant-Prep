---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 1
title: "Northgate Mutual Model Validation"
los: [los-01-01-a, los-01-01-c]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Northgate Mutual Model Validation

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Chiara Okonkwo is a model validator in the model risk management group at Northgate Mutual Assurance, a life insurer with a large commercial real estate (CRE) mortgage book.
Under the insurer's model governance policy, no quantitative model may be used for capital or pricing decisions until the validation group confirms that it was built according to the firm's regression process standard.
The standard mirrors the usual sequence: choose the model type, estimate it, check the assumptions with residual analysis, assess goodness of fit and overall significance, and confirm that the model is the best of the candidate specifications.

The credit analytics desk submits three models for validation.

**Exhibit 1: Models submitted for validation**

| Model | Dependent variable | Independent variables | Estimation method |
|---|---|---|---|
| A | 1 if a CRE loan defaults within 12 months, 0 otherwise | Loan-to-value (LTV), debt service coverage ratio (DSCR), occupancy rate | Multiple linear regression |
| B | Monthly change in a CMBS spread index, in basis points | Four macroeconomic variables | Multiple linear regression |
| C | Recovery rate on defaulted loans, in decimal form | LTV, DSCR, property-type dummy | Multiple linear regression |

For Model B, the desk reports that the residual plots show no pattern, no fanning and no outliers, so the assumptions appear to hold.
However, none of the four macroeconomic variables is individually significant, and the test of overall significance fails at the 5% level.

Desk head Graham Tulloch writes on 9 June: "Because Model B satisfies every regression assumption, it is fit for pricing, and we will use it for spread forecasts starting next quarter."
Okonkwo notes in her file on 10 June: "Satisfying the assumptions is necessary but not sufficient under the standard."

Model C is estimated on 138 defaulted loans.
The output reports a standard error of the estimate of 0.0412 and a mean squared error of 0.0017.
The desk also lists the eight residuals with the largest absolute values.

**Exhibit 2: Model C, eight largest residuals by absolute value**

| Loan | Residual |
|---|---|
| L-017 | -0.0960 |
| L-044 | 0.0850 |
| L-061 | -0.0790 |
| L-083 | 0.0710 |
| L-092 | -0.0640 |
| L-105 | 0.0600 |
| L-121 | -0.0520 |
| L-130 | 0.0450 |

The mean recovery rate in the sample is 0.6120.
The validation policy defines a potential outlier as any observation whose standardized residual, the residual divided by the standard error of the estimate, exceeds 2 in absolute value.
Potential outliers must be investigated for events not captured by the model, such as litigation or environmental remediation, before sign-off.

Okonkwo must also document which diagnostic charts she will examine for Model C.
Her checklist has two open items: whether the recovery-rate residuals are normally distributed, and whether the residual variance is constant across loans.
The desk has supplied four charts: a scatterplot matrix of recovery rate, LTV and DSCR; a plot of LTV against DSCR; a plot of residuals against predicted recovery rates; and a normal Q-Q plot of the standardized residuals.

## Questions

1. Which submitted model is most clearly estimated with an inappropriate method? (LOS: los-01-01-a)
   - A. Model B, because a spread change in basis points is not a return.
   - B. Model C, because its property-type dummy requires logistic regression.
   - C. Model A, because its dependent variable is discrete and requires logistic regression.
2. Regarding the 9 June and 10 June statements about Model B, under the regression process the model should be: (LOS: los-01-01-a)
   - A. used for spread forecasts, as Tulloch proposes, because the assumption checks are the binding gate.
   - B. adjusted and re-estimated, because the overall fit is not significant.
   - C. re-estimated as a logistic regression, because none of the independent variables is significant.
3. Applying the validation policy to Exhibit 2, the number of Model C observations Okonkwo should flag as potential outliers is: (LOS: los-01-01-c)
   - A. 2
   - B. 4
   - C. 8
4. For her two open checklist items on Model C, Okonkwo should examine, respectively: (LOS: los-01-01-c)
   - A. the normal Q-Q plot for normality, and the scatterplot matrix for constant variance.
   - B. the residuals-versus-predicted plot for normality, and the plot of LTV against DSCR for constant variance.
   - C. the normal Q-Q plot for normality, and the residuals-versus-predicted plot for constant variance.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The first fork of the regression process asks whether the dependent variable is continuous; a 1/0 default flag is discrete, so Model A should be a logistic regression (V1 pp.5-6).
> A is wrong because a spread change in basis points is continuous, and multiple linear regression does not require the dependent variable to be a return.
> B is wrong because dummy independent variables, such as property type, are explicitly allowed in multiple linear regression; only a discrete dependent variable routes to logistic regression (V1 p.5).
> 2. **B.** After the assumption check, the process asks whether the overall fit is significant; a no at that gate routes back to "adjust the model and re-estimate" (V1 pp.6-7).
> Okonkwo is correct that passing the assumptions is necessary but not sufficient.
> A is wrong because it skips the overall-significance and best-model gates.
> C is wrong because the choice between linear and logistic regression depends on whether the dependent variable is continuous, not on whether the independent variables are significant.
> 3. **A.** Standardize each residual as $z_i = e_i / s_e$ with $s_e = 0.0412$.
> L-017: $-0.0960 / 0.0412 = -2.3301$.
> L-044: $0.0850 / 0.0412 = 2.0631$.
> L-061: $-0.0790 / 0.0412 = -1.9175$.
> L-083: $0.0710 / 0.0412 = 1.7233$.
> The remaining four are $-1.5534$, $1.4563$, $-1.2621$ and $1.0922$.
> Only L-017 and L-044 exceed 2 in absolute value, so two loans are flagged.
> B (4) is wrong because it applies the 1.65 cutoff from the Q-Q discussion instead of the policy threshold of 2, which also captures L-061 and L-083.
> C (8) is wrong because it divides by the mean squared error, 0.0017, instead of the standard error; for example $-0.0960 / 0.0017 \approx -56.5$, so every residual appears extreme.
> 4. **C.** The normal Q-Q plot compares standardized residuals with standard normal quantiles, and normal residuals lie on the diagonal (V1 p.16).
> The residuals-versus-predicted plot shows whether the residual spread is constant or fans out, which is the homoskedasticity check (V1 p.18, p.23).
> A is wrong because the scatterplot matrix shows the dependent and independent variables themselves; the spread of Y is not the spread of the residuals.
> B is wrong on both counts: the residuals-versus-predicted plot does not test normality, and a plot of one independent variable against another assesses independence of the independent variables, not constant variance.

## Distractor design

- Q1: A invents a "returns only" restriction on the dependent variable; B confuses a dummy independent variable with a dummy dependent variable.
- Q2: A stops the process at the assumption gate; C applies the discrete-Y fork to a significance problem.
- Q3: B uses the wrong threshold (1.65 instead of the policy's 2); C divides by the variance (mean squared error) instead of the standard deviation (misread exhibit).
- Q4: A uses a Y-versus-X chart for a residual property; B swaps the charts' purposes and uses the X-versus-X plot for a residual property.
