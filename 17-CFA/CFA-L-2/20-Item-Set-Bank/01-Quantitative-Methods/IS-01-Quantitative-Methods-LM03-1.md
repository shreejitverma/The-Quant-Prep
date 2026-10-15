---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 3
title: "Harrowgate Small-Cap Value Fund Attribution"
los: [los-01-03-a, los-01-03-b, los-01-03-c, los-01-03-d]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Harrowgate Small-Cap Value Fund Attribution

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Priya Raman, CFA, is a quantitative analyst at Harrowgate Asset Management, a London-based manager of equity funds.
She is preparing the annual performance attribution report for the Harrowgate Small-Cap Value Fund, which the investment committee will review in March 2026.
Raman regresses 84 monthly excess returns of the fund on four factors: the market excess return (MKTRF), size (SMB), value (HML), and momentum (MOM).
None of the regressors is a lagged value of the fund's return.
Exhibit 1 reports the OLS estimates together with White-corrected standard errors.

**Exhibit 1: Four-factor regression, 84 monthly observations**

| Variable | Coefficient | OLS standard error | White standard error |
|---|---|---|---|
| Intercept | 0.0011 | 0.0014 | 0.0013 |
| MKTRF | 1.0842 | 0.0512 | 0.0736 |
| SMB | 0.4127 | 0.1488 | 0.2231 |
| HML | 0.3065 | 0.1201 | 0.1392 |
| MOM | -0.1374 | 0.0598 | 0.0842 |

$R^2 = 0.8615$, adjusted $R^2 = 0.8545$, $F = 122.85$.

Raman's residual plots show the dispersion of the residuals widening in months when MKTRF is large in absolute value.
She squares the residuals, regresses them on the four factors, and summarizes that auxiliary regression in Exhibit 2.

**Exhibit 2: Regression of squared residuals on MKTRF, SMB, HML, and MOM**

| Statistic | Value |
|---|---|
| Multiple R | 0.3677 |
| $R^2$ | 0.1352 |
| Adjusted $R^2$ | 0.0914 |
| Observations | 84 |

**Exhibit 3: Selected critical values**

| Distribution | Value |
|---|---|
| Chi-square, 5%, 3 df | 7.815 |
| Chi-square, 5%, 4 df | 9.488 |
| Chi-square, 5%, 5 df | 11.070 |
| t, two-tailed 5%, 79 df | 1.990 |
| t, two-tailed 1%, 79 df | 2.640 |

To check for multicollinearity, Raman regresses each factor on the other three.
The resulting $R^2$ values are 0.312 for MKTRF, 0.588 for SMB, 0.645 for HML, and 0.402 for MOM.
The largest pairwise correlation among the factors is 0.61, between SMB and HML.

Raman's colleague Dmitri Volkov points out that the fund holds some of the least liquid stocks in its universe.
He plots the four-factor residuals against a traded liquidity factor (LIQ) that is not in the model.
The fitted line has a slope of 0.37 and an $R^2$ of 0.41, and LIQ has a correlation of 0.58 with SMB over the sample.

Volkov also runs a Breusch-Godfrey test with two lags on the four-factor residuals.
The F-statistic is 4.12 against a 5% critical value of 3.115 for $F(2, 77)$.

At a review meeting on 14 February 2026, the two analysts make the following statements.

- Raman: "Because the variance of the residuals rises with the magnitude of MKTRF, the OLS standard errors were understated, and our original t-tests were prone to Type I errors."
- Volkov: "Now that the White standard errors are in the report, the heteroskedasticity has been removed from the residuals, and the factor loadings in the report are new, more efficient estimates."

## Questions

1. The Breusch-Pagan test statistic and the conclusion at the 5% significance level are closest to: (LOS: los-01-03-b)
   - A. 7.68; there is no evidence of conditional heteroskedasticity.
   - B. 11.36; there is evidence of conditional heteroskedasticity.
   - C. 72.37; there is evidence of conditional heteroskedasticity.
2. Using the White-corrected standard errors, the slope coefficients that are significantly different from zero at the 5% level are: (LOS: los-01-03-b)
   - A. MKTRF and HML only.
   - B. MKTRF, SMB, HML, and MOM.
   - C. MKTRF only.
3. Based on Volkov's liquidity analysis, the four-factor model most likely: (LOS: los-01-03-a)
   - A. has a biased intercept, but its slope coefficients are estimated correctly.
   - B. has understated standard errors only, which the White correction already addresses.
   - C. has biased and inconsistent coefficients and standard errors, and LIQ should be added to the model.
4. Given Volkov's Breusch-Godfrey result, Raman's most appropriate response is to: (LOS: los-01-03-c)
   - A. keep the White standard errors, because they already correct for serial correlation.
   - B. treat all coefficient estimates as inconsistent and re-estimate the model.
   - C. replace the White standard errors with Newey-West standard errors, relying on the existing coefficient estimates.
5. The variance inflation factor for HML and the most appropriate conclusion are: (LOS: los-01-03-d)
   - A. 1.55; multicollinearity is not a concern.
   - B. 2.82; multicollinearity is not a concern.
   - C. 2.82; multicollinearity explains why SMB and MOM lose significance under the White correction.
6. Which of the statements made at the review meeting is correct? (LOS: los-01-03-b)
   - A. Raman's only.
   - B. Volkov's only.
   - C. Both statements.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The Breusch-Pagan statistic uses the unadjusted $R^2$ of the auxiliary regression: $\chi^2_{BP} = nR^2 = 84 \times 0.1352 = 11.3568$. The degrees of freedom equal the number of regressors, $k = 4$, so the 5% critical value is 9.488. Because $11.3568 > 9.488$ (p-value 0.0228), reject the null of no conditional heteroskedasticity. A is wrong because it uses the adjusted $R^2$: $84 \times 0.0914 = 7.6776$, which falls below 9.488 and reverses the conclusion. C is wrong because it uses the $R^2$ of the original factor regression: $84 \times 0.8615 = 72.366$.
> 2. **A.** Robust t-statistics are $\hat{b}_j / SE_{White}$: MKTRF $1.0842/0.0736 = 14.7310$, SMB $0.4127/0.2231 = 1.8498$, HML $0.3065/0.1392 = 2.2019$, MOM $-0.1374/0.0842 = -1.6318$. Against the two-tailed 5% critical value of 1.990 with $84 - 4 - 1 = 79$ df, only MKTRF and HML remain significant. B is wrong because it uses the OLS standard errors: $t$ = 21.1758, 2.7735, 2.5520 and $-2.2977$, all above 1.990 in absolute value, but these standard errors are understated under conditional heteroskedasticity. C is wrong because it applies the 1% critical value of 2.640, which HML (2.2019) fails, although the question asks for the 5% level.
> 3. **C.** The residuals are linearly related to a variable outside the model ($R^2 = 0.41$), which is the signature of an omitted variable. Because LIQ is correlated with an included regressor (0.58 with SMB), the error term is correlated with SMB, so the intercept, the slopes, and the standard errors are all biased and inconsistent. The correction is to add LIQ and re-estimate. A is wrong because it describes an omitted variable uncorrelated with the included regressors. B is wrong because it treats a coefficient problem as a variance problem; robust standard errors cannot remove bias from the coefficients.
> 4. **C.** $4.12 > 3.115$, so the test rejects the null of no serial correlation up to lag 2. No regressor is a lagged dependent variable, so the coefficients remain consistent and only the standard errors are invalid. Newey-West (HAC) standard errors correct for both serial correlation and heteroskedasticity, so they supersede the White standard errors. A is wrong because White standard errors correct only for heteroskedasticity. B is wrong because serial correlation makes coefficients inconsistent only when a lagged dependent variable is a regressor.
> 5. **B.** $VIF_{HML} = 1/(1 - R_{HML}^2) = 1/(1 - 0.645) = 2.8169$. The other VIFs are 1.4535 (MKTRF), 2.4272 (SMB), and 1.6722 (MOM), all below the investigation threshold of 5, so multicollinearity is not a concern. A is wrong because it computes $1/R_j^2 = 1/0.645 = 1.5504$ instead of $1/(1 - R_j^2)$. C is wrong because the VIFs rule out multicollinearity; SMB and MOM lose significance because the White correction raises their standard errors to account for conditional heteroskedasticity.
> 6. **A.** Raman is correct: conditional heteroskedasticity makes the OLS standard errors understated, which inflates t-statistics and leads to too many rejections of true nulls (Type I errors). Volkov is wrong on both counts: robust standard errors do not remove heteroskedasticity from the residuals, and the coefficients in Exhibit 1 are unchanged by the correction; only the standard errors, t-statistics, and p-values change. B is wrong because it accepts Volkov's claims. C is wrong because Volkov's statement is incorrect.

## Distractor design

1. A uses the adjusted $R^2$ in $nR^2$; C uses the $R^2$ of the original regression instead of the auxiliary regression.
2. B uses the OLS standard errors instead of the robust ones; C applies the 1% critical value instead of the 5% value.
3. A applies the uncorrelated-omitted-variable case; B treats omitted-variable bias as a standard error problem that robust standard errors fix.
4. A assumes White standard errors correct for serial correlation; B applies the lagged-dependent-variable consequence to a model without one.
5. A uses the wrong VIF formula ($1/R_j^2$); C blames multicollinearity for a standard error increase caused by the heteroskedasticity correction.
6. B and C accept that robust standard errors remove heteroskedasticity and re-estimate the coefficients.
