---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 3
title: "Meridian Mutual Life Office Property Valuation"
los: [los-01-03-a, los-01-03-b, los-01-03-d]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Meridian Mutual Life Office Property Valuation

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Meridian Mutual Life is an insurance company whose general account holds direct office property in the United States, the United Kingdom, and Germany.
Its chief investment officer, Ingrid Solberg, asks Kwame Asante, a real estate analyst, to build a hedonic regression model to support the year-end valuation of the office portfolio.

Asante collects 150 office transactions from 2019 to 2024 in the same three countries.
His first specification, Model 1, regresses the transaction price (PRICE, USD millions) on net rentable area (AREA, thousands of square feet), occupancy at sale (OCC, %), and building age (AGE, years).

**Exhibit 1: Model 1 estimates, 150 transactions**

| Variable | Coefficient | Standard error |
|---|---|---|
| Intercept | -8.420 | 4.105 |
| AREA | 0.482 | 0.041 |
| OCC | 0.124 | 0.043 |
| AGE | -0.215 | 0.088 |

$R^2 = 0.7340$, adjusted $R^2 = 0.7285$, $F = 134.29$.

A plot of the Model 1 residuals against AREA shows the spread of the residuals widening sharply as AREA increases, and a plot of PRICE against AREA curves upward.
Asante regresses the squared residuals of Model 1 on AREA, OCC, and AGE and reports the results in Exhibit 2.

**Exhibit 2: Breusch-Pagan auxiliary regression for Model 1**

| Statistic | Value |
|---|---|
| Multiple R | 0.2474 |
| $R^2$ | 0.0612 |
| Adjusted $R^2$ | 0.0419 |
| Observations | 150 |

**Exhibit 3: Chi-square critical values**

| Degrees of freedom | 5% | 1% |
|---|---|---|
| 1 | 3.841 | 6.635 |
| 3 | 7.815 | 11.345 |
| 4 | 9.488 | 13.277 |

In response, Asante re-specifies the model as Model 1L, which regresses the natural log of price per square foot on the log of AREA, OCC, and AGE.
The Breusch-Pagan auxiliary regression for Model 1L, again with 150 observations, has an $R^2$ of 0.0341.
Solberg observes that the Model 1L residuals are more dispersed in some sale years than in others, but that the dispersion is unrelated to the size, occupancy, or age of the buildings.

Asante then considers distance to the central business district (DIST), which is not in either model.
Its sample correlations with ln(AREA), OCC, and AGE are 0.03, -0.02, and 0.01.

Finally, Asante estimates Model 2, which adds the number of floors (FLOORS) and parking spaces (PARKING) to the Model 1L regressors.

**Exhibit 4: Model 2 variance inflation factors**

| Regressor | ln(AREA) | FLOORS | PARKING | OCC | AGE |
|---|---|---|---|---|---|
| VIF | 11.8 | 9.4 | 4.6 | 1.3 | 1.9 |

At the valuation committee on 20 November 2026, Asante and Solberg make the following statements about Model 1.

- Asante: "Because the residual variance depends on AREA, the F-test of Model 1 is also unreliable, not just the individual t-tests."
- Solberg: "The heteroskedasticity also means the AREA coefficient of 0.482 is a biased estimate of the value of an additional thousand square feet."

## Questions

1. The Breusch-Pagan test on Model 1 at the 5% significance level indicates a test statistic of: (LOS: los-01-03-b)
   - A. 6.29, so there is no evidence of conditional heteroskedasticity.
   - B. 9.18, so there is no evidence of conditional heteroskedasticity.
   - C. 9.18, so there is evidence of conditional heteroskedasticity.
2. The residual and price plots for Model 1 most likely indicate: (LOS: los-01-03-a)
   - A. inappropriate variable scaling and form, best addressed first by revising the model.
   - B. inappropriate data pooling, best addressed by keeping Model 1 and reporting White-corrected standard errors.
   - C. multicollinearity, best addressed by dropping AREA from the model.
3. For Model 1L, the most appropriate conclusion is: (LOS: los-01-03-b)
   - A. there is no evidence of conditional heteroskedasticity, and the year-to-year differences in dispersion create no major inference problem.
   - B. the Breusch-Pagan statistic of 5.12 exceeds its critical value, so Model 1L remains conditionally heteroskedastic.
   - C. the year-to-year differences in dispersion are conditional heteroskedasticity, so White-corrected standard errors are required.
4. Omitting DIST from Model 1L most likely: (LOS: los-01-03-a)
   - A. biases the intercept but leaves the slope coefficients correctly estimated.
   - B. makes every coefficient and standard error biased and inconsistent.
   - C. has no effect on the model because DIST is uncorrelated with the regressors.
5. Based on Exhibit 4, the $R^2$ from regressing FLOORS on the other Model 2 regressors and the most appropriate action are: (LOS: los-01-03-d)
   - A. 0.106; no action is needed for any regressor.
   - B. 0.894; FLOORS requires correction.
   - C. 0.894; FLOORS warrants investigation, and ln(AREA) requires correction.
6. Which of the statements made at the valuation committee is correct? (LOS: los-01-03-b)
   - A. Solberg's only.
   - B. Asante's only.
   - C. Both statements.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** $\chi^2_{BP} = nR^2 = 150 \times 0.0612 = 9.18$, using the unadjusted $R^2$ of the auxiliary regression. The degrees of freedom equal the $k = 3$ regressors of Model 1, so the 5% critical value is 7.815. Because $9.18 > 7.815$ (p-value 0.0270), reject the null of no conditional heteroskedasticity at 5% (but not at 1%, where the critical value is 11.345). A is wrong because it uses the adjusted $R^2$: $150 \times 0.0419 = 6.285$. B is wrong because it counts the intercept as a regressor and uses 4 degrees of freedom, whose 5% critical value 9.488 exceeds 9.18.
> 2. **A.** Raw prices of buildings of very different sizes are not comparable, and a curved relation forced into a straight line leaves residuals whose spread grows with AREA: this is inappropriate scaling combined with inappropriate functional form. The curriculum's first correction for every violation is to revise the model, here by scaling price by area and taking logs, and only then to rely on robust standard errors. B is wrong because pooling shows up as separated clusters, not a fan, and White standard errors do not fix the misspecification behind the fan. C is wrong because Model 1 shows no multicollinearity symptom and dropping the main value driver would create an omitted variable.
> 3. **A.** $nR^2 = 150 \times 0.0341 = 5.115$, below the 3-df 5% critical value of 7.815 (p-value 0.1636), so there is no evidence of conditional heteroskedasticity. Dispersion that changes across sale years but is unrelated to any regressor is unconditional heteroskedasticity, which creates no major problem for inference. B is wrong because it uses 1 degree of freedom (critical value 3.841) instead of 3. C is wrong because heteroskedasticity is conditional only if the variance is correlated with the regressors, and Solberg states it is not.
> 4. **A.** From $Y = b_0 + b_1 X_1 + b_2 X_2 + \varepsilon$ estimated without $X_2$, the residual becomes $b_2 X_2 + \varepsilon$. Because DIST is essentially uncorrelated with every included regressor (correlations 0.03, -0.02, 0.01), the residual no longer has zero mean, so the intercept is biased, but the slopes are still estimated correctly. B is wrong because it describes an omitted variable that is correlated with the included regressors. C is wrong because the omission still leaves a non-zero-mean residual and a biased intercept.
> 5. **C.** $R_{FLOORS}^2 = 1 - 1/VIF = 1 - 1/9.4 = 0.8936$. A VIF between 5 and 10 warrants investigation, while ln(AREA) at 11.8 exceeds 10 and requires correction ($R^2 = 1 - 1/11.8 = 0.9153$). A is wrong because it computes $1/VIF = 0.1064$ instead of $1 - 1/VIF$ and ignores the thresholds. B is wrong because it applies the correction threshold of 10 to a VIF of 9.4, collapsing the two thresholds into one.
> 6. **B.** Asante is correct: under conditional heteroskedasticity the MSE is a biased estimator of the population error variance, so the F-test is unreliable as well as the t-tests. Solberg is wrong because heteroskedasticity biases the standard errors, not the coefficient estimates; the AREA coefficient remains consistent. A is wrong because it accepts Solberg's claim about the coefficient. C is wrong because Solberg's statement is incorrect.

## Distractor design

1. A uses the adjusted $R^2$; B counts the intercept in the chi-square degrees of freedom.
2. B misreads a fan as pooling and substitutes robust standard errors for respecification; C misdiagnoses multicollinearity and would create an omitted variable.
3. B uses 1 degree of freedom instead of $k = 3$; C calls variance unrelated to the regressors conditional heteroskedasticity.
4. B applies the correlated-omitted-variable case; C ignores the intercept bias from a non-zero-mean residual.
5. A inverts the VIF incorrectly as $1/VIF$; B treats the investigation threshold of 5 and the correction threshold of 10 as one.
6. A and C say heteroskedasticity biases the coefficients.
