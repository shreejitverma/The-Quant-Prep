---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 3
title: "Cascade Valley Bancorp Charge-Off Model Validation"
los: [los-01-03-a, los-01-03-b, los-01-03-c]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Cascade Valley Bancorp Charge-Off Model Validation

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Helena Ortiz is a model validator in the model risk management group of Cascade Valley Bancorp, a regional US bank.
Before the bank files its annual stress-test submission with its regulator, Ortiz must document whether the consumer loan charge-off model complies with the bank's model risk policy.
The regulator's guidance requires the bank to record each identified violation of the regression assumptions, its effect on the estimates, and the remedy applied.
The model developer, Marcus Lindqvist, has submitted two candidate specifications, each estimated on the same 64 usable quarterly observations from 2010Q1 to 2025Q4, the 2009Q4 charge-off rate being available to supply the first lag.

- Model A: $NCO_t = b_0 + b_1 \Delta UNEMP_t + b_2 HPI_t + b_3 NCO_{t-1} + \varepsilon_t$
- Model B: $NCO_t = b_0 + b_1 \Delta UNEMP_t + b_2 HPI_t + \varepsilon_t$

$NCO_t$ is the annualized net charge-off rate (%), $\Delta UNEMP_t$ is the quarterly change in the unemployment rate (percentage points), and $HPI_t$ is year-over-year house price growth (%).

**Exhibit 1: Model B estimates**

| Variable | Coefficient | OLS standard error | Newey-West standard error |
|---|---|---|---|
| Intercept | 0.2140 | 0.0610 | 0.0835 |
| $\Delta UNEMP$ | 0.3180 | 0.1150 | 0.1712 |
| $HPI$ | -0.0415 | 0.0122 | 0.0167 |

$R^2 = 0.4630$, adjusted $R^2 = 0.4454$, $F = 26.30$.

**Exhibit 2: Residual diagnostics**

| Model | Test | Statistic | Lagged dependent variable as regressor |
|---|---|---|---|
| A | Breusch-Godfrey, 4 lags | F = 2.65 | Yes |
| B | Durbin-Watson | 1.12 | No |

**Exhibit 3: Selected critical values**

| Distribution | Value |
|---|---|
| F(3, 56), upper 5% | 2.769 |
| F(4, 56), upper 5% | 2.537 |
| F(4, 56), upper 2.5% | 3.024 |
| F(4, 59), upper 5% | 2.528 |
| t, 61 df, two-tailed 5% | 2.000 |
| t, 61 df, one-tailed 5% | 1.670 |

Ortiz makes three further observations in her draft report.
First, the Model B residuals are much larger in quarters when $\Delta UNEMP$ was large, most notably 2020Q2 and 2020Q3.
Second, in 2016Q1 the bank shortened the point at which consumer loans are charged off from 180 days past due to 120 days past due.
A scatterplot of $NCO_t$ against $\Delta UNEMP_t$ shows two widely separated clusters, one before and one after 2016Q1, with little correlation within either cluster.
Third, the bank's stress scenarios will be run under the 120-day policy.

Lindqvist replies to the draft on 3 March 2026.
He argues that the large 2020 residuals are clustered in time and are therefore unconditional heteroskedasticity that needs no treatment.
He also argues that the Newey-West standard errors he supplied for Model A resolve every serial correlation concern for that model.

Ortiz's policy requires every regressor retained in a stress-test model to be significant at the 5% level using a two-tailed test and standard errors that are robust to the diagnosed violations.

## Questions

1. For the Breusch-Godfrey test on Model A, the appropriate 5% critical value and conclusion are: (LOS: los-01-03-c)
   - A. 2.537; there is evidence of serial correlation up to lag 4.
   - B. 2.769; there is insufficient evidence of serial correlation up to lag 4.
   - C. 3.024; there is insufficient evidence of serial correlation up to lag 4.
2. Ortiz's most appropriate conclusion about Model A is that: (LOS: los-01-03-c)
   - A. its coefficients are consistent, and Lindqvist's Newey-West standard errors make its t-tests reliable.
   - B. its coefficients are consistent, but White standard errors are needed in place of Newey-West standard errors.
   - C. its coefficients are inconsistent, so robust standard errors alone cannot make the model compliant and it must be respecified.
3. The first-order autocorrelation of the Model B residuals implied by Exhibit 2 is closest to: (LOS: los-01-03-c)
   - A. -0.44.
   - B. 0.56.
   - C. 0.44.
4. Under Ortiz's policy, the $\Delta UNEMP$ variable in Model B: (LOS: los-01-03-c)
   - A. fails, because its t-statistic is 1.86.
   - B. passes, because its t-statistic is 2.77.
   - C. passes, because its t-statistic of 1.86 exceeds 1.670.
5. Regarding the pattern in the Model B residual variance, the most accurate statement is that it is: (LOS: los-01-03-b)
   - A. unconditional heteroskedasticity, because the large residuals are clustered in time, so no correction is needed.
   - B. conditional heteroskedasticity, so the Model B coefficients are biased and must be re-estimated.
   - C. conditional heteroskedasticity, and the Newey-West standard errors in Exhibit 1 already account for it.
6. Ortiz's second and third observations most likely identify: (LOS: los-01-03-a)
   - A. inappropriate variable scaling, corrected by expressing charge-offs as a share of total loans.
   - B. inappropriate data pooling, corrected by estimating the model on the post-2016Q1 subsample.
   - C. an omitted variable, corrected by adding a lagged residual as a regressor.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The Breusch-Godfrey statistic is distributed $F(p, n - p - k - 1)$ with $p = 4$ lags, $n = 64$ and $k = 3$ regressors, so $F(4, 64 - 4 - 3 - 1) = F(4, 56)$. The test is one-tailed to the right, so the 5% critical value is the upper 5% point, 2.537. Because $2.65 > 2.537$ (p-value 0.0425), reject the null of no serial correlation up to lag 4. B is wrong because it uses $k = 3$ as the numerator degrees of freedom, the Breusch-Pagan convention, giving $F(3, 56) = 2.769$. C is wrong because it splits 5% into two tails and uses the upper 2.5% point, 3.024.
> 2. **C.** Model A includes $NCO_{t-1}$, a lagged value of the dependent variable, and question 1 established serial correlation. A lagged dependent variable contains last quarter's error, which is correlated with this quarter's error, so the regressor is correlated with the error term and every coefficient is inconsistent. Robust standard errors change only the standard errors, not the coefficients, so Lindqvist's claim fails and Model A must be respecified. A is wrong because coefficients stay consistent under serial correlation only when no lagged dependent variable is a regressor. B is wrong on the same point and also because White standard errors do not correct for serial correlation at all.
> 3. **C.** $DW \approx 2(1 - r)$, so $r \approx 1 - DW/2 = 1 - 1.12/2 = 0.4400$, positive first-order serial correlation. A is wrong on the sign; a Durbin-Watson statistic below 2 indicates positive, not negative, serial correlation. B is wrong because it reports $DW/2 = 0.56$ instead of $1 - DW/2$.
> 4. **A.** Model B shows positive serial correlation (question 3) and conditional heteroskedasticity (question 5), so the policy requires Newey-West standard errors, which are robust to both. $t = 0.3180/0.1712 = 1.8575$, which is below the two-tailed 5% critical value of 2.000 with $64 - 2 - 1 = 61$ df, so $\Delta UNEMP$ fails. B is wrong because it uses the OLS standard error: $0.3180/0.1150 = 2.7652$, which is inflated because serial correlation understates OLS standard errors. C is wrong because it compares the robust t-statistic with the one-tailed critical value of 1.670, although the policy requires a two-tailed test.
> 5. **C.** The residual variance is largest when $\Delta UNEMP$, a regressor, is largest, so the variance is correlated with the regressors, which is conditional heteroskedasticity. Newey-West (HAC) standard errors are consistent under both heteroskedasticity and autocorrelation, so the Exhibit 1 robust standard errors already account for it. A is wrong because what defines conditional heteroskedasticity is whether the variance is related to the regressors, not whether large residuals bunch in time. B is wrong because heteroskedasticity biases the standard errors, not the coefficients; the coefficients remain consistent.
> 6. **B.** A regime change in 2016Q1 splits the sample into two separated clusters with little correlation within each, which is the scatterplot signature of inappropriate data pooling. The remedy is to estimate the model on the subsample most representative of the forecast period, here the post-2016Q1 data, because the stress scenarios will run under the 120-day policy. A is wrong because scaling addresses comparisons across entities of different sizes, not a structural break. C is wrong because a separated-cluster pattern does not indicate an omitted variable, and adding a lagged residual is part of the Breusch-Godfrey auxiliary regression, not a specification remedy.

## Distractor design

1. B uses $k$ instead of $p$ as the numerator degrees of freedom; C treats the one-tailed F-test as two-tailed.
2. A ignores the lagged dependent variable; B also swaps Newey-West for White standard errors, which do not correct serial correlation.
3. A reverses the sign of the Durbin-Watson mapping; C uses $DW/2$ instead of $1 - DW/2$.
4. B uses the OLS standard error instead of the robust one; C uses a one-tailed instead of a two-tailed critical value.
5. A classifies heteroskedasticity by time clustering instead of by its relation to the regressors; B says heteroskedasticity biases coefficients.
6. A misnames a structural break as a scaling problem; C confuses the diagnostic regression with a model correction.
