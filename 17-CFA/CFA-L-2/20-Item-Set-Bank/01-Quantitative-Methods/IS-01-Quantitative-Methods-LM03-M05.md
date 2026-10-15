---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 3
title: "Halvorsen Bulk Carriers Freight Exposure Model"
los: [los-01-03-a, los-01-03-b, los-01-03-c, los-01-03-d]
difficulty: 4
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Halvorsen Bulk Carriers Freight Exposure Model

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Skerry Point Capital is a hedge fund that trades listed shipping equities.
On 2 February 2026, portfolio manager Anders Viklund asks analyst Mei-Lin Castellanos, CFA, to estimate the sensitivity of Halvorsen Bulk Carriers (HBC), an Oslo-listed dry-bulk shipowner, to dry-bulk freight rates.
Viklund plans to hedge the fund's HBC position with freight futures in proportion to that sensitivity, so he wants an estimate whose significance he can trust.
The fund's risk committee approves a hedge ratio only if it rests on a coefficient that is significant at the 5% level in a two-tailed test.
The committee also requires standard errors that are robust to every violation diagnosed in the model, and it prefers the simplest specification consistent with economic reasoning.

Castellanos uses monthly data from January 2017 through December 2025.
Model 1 regresses HBC's monthly excess return (%) on the market excess return (MKT, %), the monthly percentage change in the Baltic Dry Index (BDI), and the monthly percentage change in the bunker fuel price (FUEL).
No lagged value of HBC's return is used as a regressor.

**Exhibit 1: Model 1 estimates**

| Variable | Coefficient | OLS standard error | White standard error | Newey-West standard error |
|---|---|---|---|---|
| Intercept | 0.2100 | 0.7310 | 0.7420 | 0.7960 |
| MKT | 1.1800 | 0.1420 | 0.1760 | 0.2010 |
| BDI | 0.2150 | 0.0420 | 0.0512 | 0.0588 |
| FUEL | -0.1640 | 0.0710 | 0.0830 | 0.0940 |

| ANOVA | df | Sum of squares |
|---|---|---|
| Regression | 3 | 5,168.9 |
| Residual | 104 | 5,832.4 |
| Total | 107 | 11,001.3 |

A plot of the Model 1 residuals against BDI shows the spread of the residuals widening in months with large freight rate moves.
Castellanos squares the Model 1 residuals and regresses them on MKT, BDI, and FUEL.

**Exhibit 2: ANOVA of the regression of squared Model 1 residuals on MKT, BDI, and FUEL**

| Source | df | Sum of squares |
|---|---|---|
| Regression | 3 | 9,406.0 |
| Residual | 104 | 106,437.0 |
| Total | 107 | 115,843.0 |

She also computes the sum of squared differences between successive Model 1 residuals, $\sum_{t=2}^{n}(\hat{u}_t - \hat{u}_{t-1})^2 = 11{,}256.5$.
Because dry-bulk freight follows seasonal patterns tied to the Chinese New Year and the South American grain harvest, she also runs a Breusch-Godfrey test with 12 lags on the Model 1 residuals, which gives an F-statistic of 2.31.

Viklund suggests adding the monthly percentage change in the Baltic Capesize Index (CAPE), noting that Capesize vessels make up most of HBC's fleet.
Castellanos points out that the Capesize rate is one of the components from which the BDI is calculated.
She nevertheless estimates Model 2, which adds CAPE to the three Model 1 regressors, and summarizes both models in Exhibit 3.
The pairwise correlation between BDI and CAPE over the sample is 0.95.

**Exhibit 3: Model comparison**

| Statistic | Model 1 | Model 2 |
|---|---|---|
| $R^2$ | 0.4698 | 0.4712 |
| Adjusted $R^2$ | 0.4546 | 0.4507 |
| BDI coefficient | 0.2150 | 0.1320 |
| BDI OLS standard error | 0.0420 | 0.1383 |
| BDI Newey-West standard error | 0.0588 | 0.1936 |
| $R^2$ of BDI regressed on the other regressors | 0.300 | 0.935 |

**Exhibit 4: Selected critical values**

| Distribution | Value |
|---|---|
| Chi-square, 3 df, upper 5% | 7.815 |
| Chi-square, 4 df, upper 5% | 9.488 |
| Chi-square, 3 df, upper 1% | 11.345 |
| F(12, 92), upper 5% | 1.859 |
| F(3, 92), upper 5% | 2.704 |
| t, 103 or 104 df, two-tailed 5% | 1.983 |

At a meeting on 9 February 2026, Viklund states: "Model 2 is the one to hedge with. Capesize exposure drives HBC's earnings, and once CAPE is in the model the BDI coefficient is no longer significant, so the broad index is not the exposure we should hedge."

## Questions

1. The Breusch-Pagan test statistic for Model 1 and the conclusion at the 5% significance level are closest to: (LOS: los-01-03-b)
   - A. 3.06; there is no evidence of conditional heteroskedasticity.
   - B. 8.77; there is no evidence of conditional heteroskedasticity.
   - C. 8.77; there is evidence of conditional heteroskedasticity.
2. The Durbin-Watson statistic for Model 1 and the most appropriate conclusion about serial correlation are: (LOS: los-01-03-c)
   - A. 1.93; the residuals show no serial correlation, so the OLS standard errors of Model 1 are reliable.
   - B. 1.93; serial correlation up to lag 12 is present even though first-order autocorrelation is negligible, so Newey-West standard errors should be used and the coefficient estimates remain consistent.
   - C. 1.02; strong positive first-order serial correlation makes the Model 1 coefficient estimates inconsistent.
3. The variance inflation factor of BDI in Model 2 and, holding the MSE and the sample variance of BDI constant, the factor by which the OLS standard error of the BDI coefficient rises from Model 1 to Model 2 are closest to: (LOS: los-01-03-d)
   - A. 10.26 and 2.68.
   - B. 15.38 and 3.28.
   - C. 15.38 and 10.77.
4. To decide whether HBC has a significant BDI exposure to hedge, the specification, standard errors, and conclusion most consistent with avoiding model misspecification are: (LOS: los-01-03-a)
   - A. Model 2 with Newey-West standard errors; $t = 0.68$, so HBC has no significant BDI exposure.
   - B. Model 1 with White standard errors; $t = 4.20$, so the BDI exposure is significant.
   - C. Model 1 with Newey-West standard errors; $t = 3.66$, so the BDI exposure is significant.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The total degrees of freedom in Exhibit 2 are 107, so $n = 107 + 1 = 108$. The unadjusted $R^2$ of the auxiliary regression is $9{,}406.0 / 115{,}843.0 = 0.081196$, or 0.0812 rounded. $\chi^2_{BP} = nR^2 = 108 \times 0.081196 = 8.7692$. The degrees of freedom equal the $k = 3$ regressors, so the 5% critical value is 7.815, and $8.7692 > 7.815$ (p-value 0.0325) rejects the null of no conditional heteroskedasticity at 5%, though not at 1% (11.345). A is wrong because it reports the F-statistic of the auxiliary regression, $(9{,}406.0/3)/(106{,}437.0/104) = 3{,}135.3333/1{,}023.4327 = 3.0635$, instead of $nR^2$, and compares it with the chi-square critical value. B is wrong because it counts the intercept as a regressor and uses 4 degrees of freedom, whose 5% critical value 9.488 exceeds 8.7692.
> 2. **B.** $DW = 11{,}256.5 / 5{,}832.4 = 1.9300$, where the denominator is the residual sum of squares of Model 1, so $r \approx 1 - 1.9300/2 = 0.0350$ and first-order serial correlation is negligible. The Breusch-Godfrey statistic is distributed $F(p, n - p - k - 1) = F(12, 108 - 12 - 3 - 1) = F(12, 92)$, and $2.31 > 1.859$ (p-value 0.0126), so serial correlation up to lag 12 is present; the Durbin-Watson test misses it because it detects only first-order serial correlation. Because no regressor is a lagged dependent variable, the coefficients remain consistent and only the standard errors are understated, so Newey-West (HAC) standard errors are required, and they also handle the conditional heteroskedasticity found in question 1. A is wrong because it relies on the Durbin-Watson statistic alone and ignores the Breusch-Godfrey rejection. C is wrong because it divides by the total sum of squares, $11{,}256.5 / 11{,}001.3 = 1.0232$ (implied $r \approx 0.4884$), and because serial correlation makes coefficients inconsistent only when a lagged dependent variable is a regressor.
> 3. **B.** $VIF_{BDI} = 1/(1 - 0.935) = 15.3846$ in Model 2, against $1/(1 - 0.300) = 1.4286$ in Model 1. The sampling variance of a coefficient is proportional to its VIF, so with the MSE and the variance of BDI unchanged the standard error rises by $\sqrt{15.3846 / 1.4286} = \sqrt{10.7692} = 3.2817$. The Exhibit 3 ratio $0.1383 / 0.0420 = 3.2929$ is slightly larger because the MSE rises from $5{,}832.4/104 = 56.0808$ to about 56.4805 when a degree of freedom is lost. A is wrong because it uses the squared pairwise correlation as $R_j^2$: $1/(1 - 0.95^2) = 10.2564$ and $\sqrt{10.2564/1.4286} = 2.6795$; with more than two regressors the auxiliary $R^2$, not the pairwise correlation, determines the VIF. C is wrong because it reports the variance ratio, 10.7692, as the standard error ratio instead of taking its square root.
> 4. **C.** The CAPE series is a component of the BDI, so adding it violates parsimony and economic reasoning: it raises $R^2$ only from 0.4698 to 0.4712, lowers adjusted $R^2$ from 0.4546 to 0.4507, and creates serious multicollinearity (VIF 15.38 > 10). The correct specification is Model 1, whose BDI VIF of 1.43 raises no concern, with Newey-West standard errors because questions 1 and 2 found conditional heteroskedasticity and serial correlation: $t = 0.2150 / 0.0588 = 3.6565 > 1.983$, so the BDI exposure is significant at 5%. A is wrong because $t = 0.1320 / 0.1936 = 0.6818$ is small only because multicollinearity inflates the standard error; concluding there is no exposure is a Type II error, and the correction is to drop the redundant regressor, not to reinterpret the model. B is wrong because White standard errors correct only for heteroskedasticity; $t = 0.2150 / 0.0512 = 4.1992$ still overstates significance because it ignores the serial correlation found in question 2.

## Distractor design

1. A uses the auxiliary regression's F-statistic in place of $nR^2$; B counts the intercept in the chi-square degrees of freedom.
2. A trusts the first-order Durbin-Watson test over the Breusch-Godfrey test; C divides by the total instead of the residual sum of squares and applies the lagged-dependent-variable consequence to a model without one.
3. A uses the squared pairwise correlation instead of the auxiliary $R^2$; C reports the variance inflation ratio as the standard error ratio.
4. A reads a multicollinearity-inflated standard error as absence of exposure; B uses heteroskedasticity-only standard errors when serial correlation is also present.
