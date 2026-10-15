---
type: cfa-lm
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
volume: 1
lm: 2
title: "Evaluating Regression Model Fit and Interpreting Model Results"
pages: "25-48"
weight_band: "5-10%"
difficulty: 3
los_count: 3
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/quantitative-methods]
---

# LM2: Evaluating Regression Model Fit and Interpreting Model Results

Difficulty 3: the arithmetic is light, but the exam punishes anyone who confuses the three F-tests, the two information criteria, or the two R-squareds, and every one of those confusions is a ready-made distractor.

## LOS map

- **evaluate** how well a multiple regression model explains the dependent variable by analyzing ANOVA table results and measures of goodness of fit (V1 p.25) ^los-01-02-a
  - Examiner asks: given an ANOVA table and a fit table for two or three nested models, recompute R-squared and adjusted R-squared from the sums of squares, explain why adjusted R-squared fell when a variable was added, and pick the "best fit" model by BIC and the "best prediction" model by AIC.
- **formulate** hypotheses on the significance of two or more coefficients in a multiple regression model and interpret the results of the joint hypothesis tests (V1 p.25) ^los-01-02-b
  - Examiner asks: identify the restricted and unrestricted models, write H0 as "both slopes equal zero", compute the joint F-statistic from the two residual sums of squares with q and n - k - 1 degrees of freedom, and compare with a critical value the vignette supplies.
- **calculate** and interpret a predicted value for the dependent variable, given the estimated regression model and assumed values for the independent variable (V1 p.25) ^los-01-02-c
  - Examiner asks: plug assumed factor values into the full estimated equation, including the intercept and every insignificant slope, and recognise that the forecast interval is wider than the regression's own standard error when the X values are themselves forecasts.

## Core intuition

Every idea in this module comes from a single accounting identity: the total variation in the dependent variable splits into the part the regression explains and the part it does not (V1 p.26).
Write it as SST = SSR + SSE.
Once that split exists, every question about "fit" is a question about how big SSE is, how many parameters were spent to make it that small, and whether the reduction in SSE bought by an extra variable is large relative to what you would expect from pure noise.

> [!abstract] Idea 1: R-squared can only go up, so it cannot judge parsimony
> Adding an independent variable gives ordinary least squares one more degree of freedom to shrink SSE.
> OLS never uses that freedom to make SSE larger, so R-squared = SSR / SST rises or stays flat with every added variable (V1 p.26).
> A statistic that never falls cannot tell you when to stop adding variables.

The curriculum lists three failures of R-squared in multiple regression (V1 p.26-27).
It says nothing about whether coefficients are statistically significant.
It says nothing about whether the coefficients or predictions are biased.
It does not by itself say the fit is "good": asset-pricing models routinely have low R-squared and are still correct, while an overfitted model can have a high R-squared and be useless out of sample.
Overfitting is the curriculum's word for a model with too many independent variables relative to the number of observations, so that the estimated slopes stop representing true relationships (V1 p.27).

Adjusted R-squared repairs the first problem by comparing variances rather than sums of squares.
SSE / (n - k - 1) is the unbiased estimate of the error variance, and SST / (n - 1) is the unbiased estimate of the variance of Y.
One minus their ratio is adjusted R-squared (V1 p.27).
Because the denominator n - k - 1 shrinks with every added variable, a new variable must reduce SSE by more than one "share" of the remaining error variance to raise adjusted R-squared.
That is exactly the origin of the rule the exam loves: adding a variable raises adjusted R-squared if and only if the absolute value of its t-statistic exceeds 1.0 (V1 p.27).
The bar is deliberately low.
A t-statistic of 1.0 is nowhere near significance at 5% or 1%, so adjusted R-squared rising is weak evidence, and adjusted R-squared falling is strong evidence that the variable adds nothing (V1 p.27).
Three more cautions follow from the same construction (V1 p.30).
Adjusted R-squared has no clean "percentage of variation explained" interpretation, it can be negative, and it says nothing about coefficient significance or bias.

> [!abstract] Idea 2: AIC and BIC are penalised likelihoods, and BIC's penalty is always heavier
> Both criteria start from n times the log of the average squared residual, which is minus twice the Gaussian log-likelihood up to a constant, and add a penalty per estimated parameter (V1 p.32).
> AIC charges 2 per parameter; BIC charges ln(n) per parameter.
> ln(n) exceeds 2 as soon as n exceeds 7, so BIC always prefers the smaller model when the two disagree (V1 p.32).

The practical rule is short and heavily tested (V1 p.32).
Lower is better for both.
AIC when the model's job is prediction.
BIC when the goal is the best goodness of fit, which in practice means the most parsimonious model that still fits.
The absolute level of either number is meaningless; only differences across models that share the same dependent variable carry information (V1 p.32).
The five-factor illustration makes the disagreement concrete: AIC is minimised by the four-factor model, BIC by the one-factor model, and the analyst chooses according to purpose (V1 p.32).
When all 31 possible subsets of the five factors are ranked, the model with Factors 1 and 4 has the lowest AIC, the lowest BIC, and the highest adjusted R-squared, while the model with the highest R-squared, all five factors, ranks poorly on every other criterion (V1 p.38).
That single exhibit is the whole argument against picking models by R-squared.

The second half of the module is about tests rather than scores.
A single coefficient in a multiple regression is tested exactly as in simple regression: a t-statistic with n - k - 1 degrees of freedom against a hypothesised value that is usually, but not always, zero (V1 p.34).
Software reports the test against zero; to test against any other value you recompute the statistic with the new hypothesised value or check whether that value lies inside the reported confidence interval (V1 p.34).

> [!abstract] Idea 3: a joint test asks whether a group of variables earned its degrees of freedom
> Drop q variables from the full (unrestricted) model to get the restricted model.
> SSE must rise.
> The joint F-statistic is the rise in SSE per dropped variable divided by the unrestricted error variance (V1 p.35).
> If dropping the variables barely raised SSE relative to the noise, the group did not earn its place, and the restricted model wins.

The reason for a joint test instead of q separate t-tests is correlation among financial regressors (V1 p.35).
Two correlated variables can share explanatory power so that neither looks significant on its own while together they matter, or each looks marginal while jointly they add nothing.
The joint F-test handles the shared part correctly because it compares whole models rather than single slopes.
The hypotheses are H0: all q restricted slopes equal zero against Ha: at least one of them is not zero (V1 p.35).
The test is one-tailed to the right with q numerator and n - k - 1 denominator degrees of freedom, where k counts the independent variables in the unrestricted model (V1 p.35).
In the five-factor example, dropping Factors 4 and 5 raised SSE by only 7.8994, the F-statistic was 3.0694 against a 1% critical value of 5.120, and the restricted three-factor model was judged the better fit (V1 p.36).

The general linear F-test that appears in every ANOVA table is the same test with the restricted model reduced to an intercept only (V1 p.36-37).
Then SSE of the restricted model is SST, the rise in SSE is SSR, q equals k, and the statistic collapses to MSR / MSE with k and n - k - 1 degrees of freedom (V1 p.37).
Rejecting it says only that at least one slope is nonzero; it is a floor for usefulness, not a certificate of quality (V1 p.37).
The curriculum's Exhibit 7 gives the scoreboard (V1 p.38): adjusted R-squared higher is better, AIC and BIC lower is better, a t-statistic must be outside the critical bounds, and a joint F must exceed its critical value.
Model building is iterative, not a single pass through that table (V1 p.37).

Prediction closes the module.
A forecast is the intercept plus the sum of each estimated slope times its assumed value (V1 p.43).
Two rules are tested constantly (V1 p.44).
Every variable that was in the estimated model goes into the forecast, including the ones that were not significant, because the slopes were estimated jointly and reflect the correlations among all the regressors.
The intercept is always included.
The forecast carries two sources of error (V1 p.44).
Model error is the residual, the stochastic part of the regression.
Sampling error arises when the independent variables are themselves forecasts, so their errors feed into the forecast of Y.
Together they give a standard error of the forecast that is larger than the standard error of the regression, and a prediction interval wider than the in-sample residual spread (V1 p.44).
The curriculum does not derive the multiple-regression forecast variance and expects software to supply it; for the five-factor model the software reports a standard error of forecast of 1.1466 around a point estimate of -2.0971, with 95% bounds of -4.4098 and 0.2119 (V1 p.44).

## Formulas and derivations

**ANOVA decomposition and mean squares** (V1 p.27)
$$ SST = SSR + SSE, \qquad MSR = \frac{SSR}{k}, \qquad MSE = \frac{SSE}{n-k-1}, \qquad SEE = \sqrt{MSE} $$
^f-01-02-1

- SST is total sum of squares, sum of squared deviations of Y from its mean; SSR is the regression sum of squares; SSE is the residual sum of squares; all in squared units of Y.
- Degrees of freedom: k for regression, n - k - 1 for residual, n - 1 total, where k is the number of independent variables and n the number of observations.
- The identity holds because OLS residuals are orthogonal to the fitted values, so the cross term in the expansion of the total deviation vanishes.
- Check on Exhibit 1: 90.6234 + 56.6182 = 147.2416, 90.6234 / 5 = 18.1247, 56.6182 / 44 = 1.2868 (V1 p.27).

**Coefficient of determination** (V1 p.26)
$$ R^2 = \frac{\text{Sum of squares regression}}{\text{Sum of squares total}} = \frac{\sum_{i=1}^{n}(\hat{Y}_i - \bar{Y})^2}{\sum_{i=1}^{n}(Y_i - \bar{Y})^2} = 1 - \frac{SSE}{SST} $$
^f-01-02-2

- Unitless, between 0 and 1; the fraction of the variation in Y explained by the regression.
- Because SSR + SSE = SST, the two forms are identical; use whichever sum of squares the vignette prints.
- Non-decreasing in k: a new regressor can only lower SSE, so R-squared never falls when a variable is added (V1 p.26).

**Adjusted R-squared, sum of squares form** (V1 p.27)
$$ \bar{R}^2 = 1 - \frac{SSE / (n-k-1)}{SST / (n-1)} $$
^f-01-02-3

- Numerator is the unbiased estimate of error variance; denominator is the sample variance of Y.
- Can be negative when the model explains less than the degrees of freedom it consumes; R-squared cannot go below zero (V1 p.27).
- Derivation: replace each sum of squares in 1 - SSE / SST with its variance estimate, so that the penalty for parameters enters through n - k - 1.

**Adjusted R-squared, R-squared form** (V1 p.27)
$$ \bar{R}^2 = 1 - \left[\left(\frac{n-1}{n-k-1}\right)(1 - R^2)\right] $$
^f-01-02-4

- Since (n - 1) / (n - k - 1) > 1 whenever k is at least 1, adjusted R-squared is strictly below R-squared (V1 p.27).
- Derivation: divide numerator and denominator of the ratio in the previous formula by SST, note SSE / SST = 1 - R-squared, and collect the degrees-of-freedom factor.

> [!tip] Calculator
> Exhibit 1 values: `1 - 0.6155 = x 49 / 44 = +/- + 1 =` gives 0.5718 (V1 p.29).
> Keep the unrounded R-squared in memory if the vignette gives sums of squares: `90.6234 / 147.2416 = STO 1`, then `1 - RCL 1 = x 49 / 44 = +/- + 1 =`.

**Adjusted R-squared change rule** (V1 p.27)
$$ \bar{R}^2 \text{ rises when a variable is added} \iff |t_{\text{new}}| > 1.0 $$
^f-01-02-5

- t is the t-statistic of the added coefficient in the enlarged model.
- Reason it holds: adding one variable is a nested comparison with q = 1, and the joint F for one restriction equals the square of that variable's t-statistic.
- Adjusted R-squared rises exactly when the new SSE divided by its new degrees of freedom is smaller than the old error variance, which after rearranging is F > 1, that is, t-squared > 1.
- |t| = 1 is far below the 5% or 1% critical values, so a rise in adjusted R-squared is not evidence of significance (V1 p.27).

**Akaike's information criterion** (V1 p.32)
$$ AIC = n \ln\left(\frac{\text{Sum of squares error}}{n}\right) + 2(k+1) $$
^f-01-02-6

- n observations, k independent variables, so k + 1 estimated coefficients including the intercept; the level of AIC has no units or meaning, only differences across models with the same Y matter (V1 p.32).
- Lower is better; the term 2(k + 1) is the penalty for adding variables (V1 p.32).
- Derivation: for normal errors the maximised log-likelihood is -(n/2)[ln(2 pi) + ln(SSE/n) + 1], so -2 times the log-likelihood equals n ln(SSE/n) plus a constant that is identical across models with the same n and is dropped.
- Check: for the five-factor model, -25 [ln(2 pi) + ln(56.6182/50) + 1] = -74.05, matching the printed log-likelihood of -74.054 (V1 p.27).

**Schwarz's Bayesian information criterion** (V1 p.32)
$$ BIC = n \ln\left(\frac{\text{Sum of squares error}}{n}\right) + \ln(n)\,(k+1) $$
^f-01-02-7

- Same first term as AIC; the penalty per parameter is ln(n) instead of 2.
- Since ln(n) > 2 for every n above 7, BIC penalises complexity more heavily and prefers more parsimonious models (V1 p.32).
- BIC - AIC = (ln n - 2)(k + 1), which grows with k, so the two criteria disagree only when the extra variables buy a small SSE reduction.
- Use AIC for prediction, BIC for goodness of fit; lower is better in both (V1 p.32).

> [!tip] Calculator
> Five-factor model: `56.6182 / 50 = LN x 50 = + 12 =` gives 18.215 for AIC (V1 p.32).
> For BIC replace the last step with `+ ( 50 LN x 6 ) =`, or compute `50 LN = x 6 =` first and add it to the stored first term, giving 29.687.

**t-test for a single coefficient** (V1 p.34, p.41)
$$ t = \frac{\hat{b}_j - B_j}{s_{\hat{b}_j}}, \qquad df = n - k - 1 $$
^f-01-02-8

- b-hat is the estimated slope, B_j the hypothesised value (0 unless stated), s the coefficient's standard error; t is unitless.
- Two-sided H0: b_j = B_j; one-sided left H0: b_j >= B_j; one-sided right H0: b_j <= B_j (V1 p.34).
- Software tests against zero; against a non-zero B_j either recompute t or check whether B_j lies inside the reported confidence interval (V1 p.34).
- Identical to simple regression except for the degrees of freedom.

**Joint F-test for nested models** (V1 p.35)
$$ F = \frac{(SSE_{\text{restricted}} - SSE_{\text{unrestricted}}) / q}{SSE_{\text{unrestricted}} / (n-k-1)} $$
^f-01-02-9

- q is the number of restrictions, the count of variables omitted from the restricted model; k is the number of independent variables in the unrestricted model; the statistic follows F with q and n - k - 1 degrees of freedom (V1 p.35).
- H0: b_m = b_{m+1} = ... = b_{m+q-1} = 0; Ha: at least one of the q slopes is not zero; one-tailed, right side (V1 p.35).
- Derivation: the numerator is the extra SSE incurred per restriction and the denominator is the unrestricted MSE, so under H0 both estimate the same error variance and the ratio is F-distributed.
- Reject when the calculated F exceeds the critical value; failing to reject favours the restricted, more parsimonious model (V1 p.36).

> [!tip] Calculator
> Exhibit 5: `64.5176 - 56.6182 = / 2 = STO 1`, `56.6182 / 44 = STO 2`, `RCL 1 / RCL 2 =` gives 3.0694 (V1 p.36).
> When the vignette prints MSE for the unrestricted model, skip the second step and divide by the printed MSE.

**General linear F-test for the whole regression** (V1 p.37)
$$ F = \frac{MSR}{MSE} = \frac{SSR / k}{SSE / (n-k-1)}, \qquad df = (k,\ n-k-1) $$
^f-01-02-10

- H0: b_1 = b_2 = ... = b_k = 0; Ha: at least one slope differs from zero; one-tailed, right side (V1 p.36-37).
- Derivation: apply the nested F with the restricted model containing only an intercept, so SSE_restricted = SST, the numerator becomes SSR / k, and q = k.
- This is the F printed in every ANOVA table; five-factor model: 18.1247 / 1.2868 = 14.0853 (V1 p.37).

**Predicted value of the dependent variable** (V1 p.43)
$$ \hat{Y}_f = \hat{b}_0 + \hat{b}_1 X_{1f} + \hat{b}_2 X_{2f} + \dots + \hat{b}_k X_{kf} = \hat{b}_0 + \sum_{j=1}^{k} \hat{b}_j X_{jf} $$
^f-01-02-11

- X_jf are the assumed values of the independent variables; the intercept multiplies an assumed value of 1 (V1 p.43).
- All k variables that were in the estimated model must be included, significant or not, because their slopes were estimated jointly (V1 p.44).
- Units of Y-hat are the units of Y, so a percentage-return regression gives a percentage return.

**Prediction interval and standard error of the forecast** (V1 p.44)
$$ \hat{Y}_f \pm t_{\alpha/2,\ n-k-1}\, s_f, \qquad s_f > SEE \text{ when the } X_{jf} \text{ are forecasts} $$
^f-01-02-12

- s_f is the standard error of the forecast, which combines model error (the residual variance) with sampling error from forecasting the independent variables (V1 p.44).
- The curriculum states the full multiple-regression formula for s_f is beyond scope and takes s_f from software (V1 p.44).
- Check: for the five-factor model, t(0.025, 44) = 2.0154 and 2.0154 x 1.1466 = 2.3108, which equals half the printed interval width (0.2119 + 4.4098) / 2 = 2.3109 (V1 p.44).
- Larger sampling error in the X forecasts means larger s_f and a wider interval (V1 p.26).

## Worked examples

**Example 1: R-squared and adjusted R-squared from the five-factor ANOVA table** (V1 p.27-29)

Given: SSR = 90.6234, SSE = 56.6182, SST = 147.2416, n = 50, k = 5.
Step 1: R-squared = 90.6234 / 147.2416 = 0.61547, printed as 0.6155.
Step 2: Degrees-of-freedom factor = (n - 1) / (n - k - 1) = 49 / 44 = 1.11364.
Step 3: Adjusted R-squared = 1 - 1.11364 x (1 - 0.61547) = 1 - 1.11364 x 0.38453 = 1 - 0.42822 = 0.57178, printed as 0.5718.
Step 4: Cross-check with the sum of squares form: 1 - (56.6182 / 44) / (147.2416 / 49) = 1 - 1.28678 / 3.00493 = 0.5718.
Step 5: SEE = sqrt(1.2868) = 1.1344; the exhibit's "Standard Error" line prints 0.0113, which does not reconcile with the ANOVA figures, so treat the ANOVA table as authoritative.
Interpretation: the five factors explain 61.55% of the variation in portfolio excess returns, but adjusted R-squared is 4.4 points lower because two of the five factors (Factor 2 and Factor 5) carry t-statistics below 1 in absolute value (V1 p.28).
Python confirms 0.61547 and 0.57178. ^ex-01-02-1

**Example 2: AIC and BIC for the nested five-factor models** (V1 p.32)

Given: n = 50; the five-factor model has SSE = 56.6182 with k = 5; the three-factor model (Factors 1, 2, 3) has SSE = 64.5176 with k = 3 (V1 p.35).
Step 1: Five factors: ln(56.6182 / 50) = ln(1.13236) = 0.12431; n x that = 6.2154; AIC = 6.2154 + 2 x 6 = 18.215; BIC = 6.2154 + 3.91202 x 6 = 6.2154 + 23.472 = 29.687.
Step 2: Three factors: ln(64.5176 / 50) = ln(1.29035) = 0.25492; n x that = 12.746; AIC = 12.746 + 2 x 4 = 20.746; BIC = 12.746 + 3.91202 x 4 = 12.746 + 15.648 = 28.394.
Step 3: Compare with Exhibit 4: five factors 18.215 and 29.687 match exactly; three factors 20.743 and 28.393 match to rounding of the printed SSE.
Step 4: Across the five printed models, AIC is lowest (16.331) for Factors 1 to 4 and BIC is lowest (22.903) for Factor 1 only.
Interpretation: a prediction model would use four factors, a parsimonious best-fit model would use Factor 1 alone (V1 p.32).
Adjusted R-squared for the three-factor model from its SSE is 1 - (64.5176 / 46) / (147.2416 / 49) = 1 - 1.40256 / 3.00493 = 0.5332, matching the printed 0.533. ^ex-01-02-2

**Example 3: Knowledge check, Model 1 versus Model 2 for ROA** (V1 p.30-31)

Given: n = 26 diversified manufacturers; Model 1 regresses ROA on CAPEX (k = 1, R-squared 0.8799, adjusted 0.8749); Model 2 adds ADV (k = 2, R-squared 0.8805, adjusted 0.8701, ADV t-statistic -0.3320, p-value 0.7429).
Step 1: Verify Model 1 adjusted R-squared: 1 - (25 / 24)(1 - 0.8799) = 1 - 1.04167 x 0.1201 = 1 - 0.12510 = 0.8749.
Step 2: Verify Model 2 adjusted R-squared: 1 - (25 / 23)(1 - 0.8805) = 1 - 1.08696 x 0.1195 = 1 - 0.12989 = 0.8701.
Step 3: R-squared rose by 0.0006 while adjusted R-squared fell by 0.0048.
Step 4: The fall is consistent with |t| for ADV = 0.3320 < 1.0 and with the 74% p-value.
Interpretation: CAPEX alone explains 87.99% of the variation in ROA; adding ADV raises R-squared trivially, lowers adjusted R-squared, and does not improve the statistical performance of the model (V1 p.31).
Python confirms 0.87490 and 0.87011. ^ex-01-02-3

**Example 4: Knowledge check, goodness-of-fit statistics for the ROA models** (V1 p.33)

Given: Model 1 (CAPEX) R-squared 0.880, adjusted 0.875, AIC 23.899, BIC 26.523; Model 2 (CAPEX, ADV) R-squared 0.881, adjusted 0.870, AIC 25.804, BIC 28.792.
Step 1: R-squared comparison: 88.0% versus 88.1% of ROA variation explained.
Step 2: Adjusted R-squared falls from 0.875 to 0.870, so ADV's coefficient has |t| < 1 (the t-statistic is -0.3320).
Step 3: AIC 23.899 < 25.804 and BIC 26.523 < 28.792, so both criteria rank Model 1 first.
Conclusion: Model 1 is the better model on every criterion; adding ADV improves neither explanatory nor predictive power (V1 p.33).
Recomputation note: using the ANOVA residual sums of squares on pages 39-40 (Model 1 SSE 55.9934, Model 2 SSE 55.7263, n = 26) in Equations 3 and 4 gives AIC 23.946 and 25.821 and BIC 26.462 and 29.596.
The AIC values are within 0.05 of the printed figures but the printed BIC values do not reproduce, and the p.42 table even shows BIC below AIC for the R&D-only model, which Equations 3 and 4 cannot produce when ln(26) = 3.258 > 2.
The printed ROA criteria therefore come from a software convention that differs from the curriculum's formulas; the rankings, which are all the exam can test, are unchanged under either convention.
By contrast, the five-factor values in Exhibit 4 and the practice-problem values in Exhibit 4 on page 47 reproduce exactly from Equations 3 and 4. ^ex-01-02-4

**Example 5: Joint F-test for Factors 4 and 5 at the 1% level** (V1 p.35-36)

Given: restricted model (Factors 1, 2, 3) SSE = 64.5176 with 46 df; unrestricted model (Factors 1 to 5) SSE = 56.6182 with 44 df, MSE = 1.2868; n = 50, k = 5, q = 2.
Step 1: H0: b_Factor4 = b_Factor5 = 0; Ha: at least one is not zero.
Step 2: Test statistic is the nested F with 2 and 44 degrees of freedom.
Step 3: alpha = 1%, one-tailed right.
Step 4: Critical F = 5.120 per the curriculum's table (scipy gives 5.123); reject if the calculated F exceeds it.
Step 5: Numerator = (64.5176 - 56.6182) / 2 = 7.8994 / 2 = 3.9497; denominator = 56.6182 / 44 = 1.2868; F = 3.9497 / 1.2868 = 3.0694.
Step 6: 3.0694 < 5.120, so fail to reject H0.
Interpretation: adding Factors 4 and 5 lowered SSE by only 7.8994, not enough to justify two lost degrees of freedom; the restricted three-factor model fits better (V1 p.36).
Note that the p-value is about 0.057, so the same test would reject at 10% but not at 5%; the exam will state the level.
Python confirms 3.06945. ^ex-01-02-5

**Example 6: General linear F-test for the five-factor model at the 5% level** (V1 p.37)

Given: MSR = 18.1247 with 5 df; MSE = 1.2868 with 44 df.
Step 1: H0: b_1 = b_2 = b_3 = b_4 = b_5 = 0; Ha: at least one slope is nonzero.
Step 2: F = MSR / MSE with 5 and 44 degrees of freedom.
Step 3: alpha = 5%, one-tailed right.
Step 4: Critical F = 2.427; reject if the calculated F is larger.
Step 5: F = 18.1247 / 1.2868 = 14.0853.
Step 6: 14.0853 > 2.427, reject H0; at least one slope differs from zero (the p-value is on the order of 10 to the power -8).
Interpretation: the model as a whole has explanatory power, which is a necessary but not sufficient condition for it being the best model; Example 5 already showed two of its five variables are jointly unnecessary (V1 p.37).
Python confirms 14.0851 from the printed mean squares. ^ex-01-02-6

**Example 7: Knowledge check part 1, R-squared and adjusted R-squared for Model 3 (ROA on CAPEX, ADV, R&D)** (V1 p.40)

Given: SSR = 410.9591, SSE = 55.3949, SST = 466.3540, n = 26, k = 3.
Step 1: R-squared = 410.9591 / 466.3540 = 0.88122, printed 0.8812.
Step 2: Factor = 25 / 22 = 1.13636.
Step 3: Adjusted R-squared = 1 - 1.13636 x (1 - 0.8812) = 1 - 1.13636 x 0.1188 = 1 - 0.13500 = 0.8650.
Interpretation: three variables explain 88.12% of ROA variation, but adjusted R-squared of 0.8650 is below Model 1's 0.8749, so the two additions cost more degrees of freedom than they repaid (V1 p.40).
Python confirms 0.88122 and 0.86502. ^ex-01-02-7

**Example 8: Knowledge check part 2, does Model 3 explain ROA at the 1% level** (V1 p.40-41)

Given: MSR = 136.9864 (3 df), MSE = 2.5180 (22 df), printed F = 54.4039.
Step 1: H0: b_CAPEX = b_ADV = b_R&D = 0; Ha: at least one is nonzero.
Step 2: F = MSR / MSE with 3 and 22 df.
Step 3: alpha = 1%, one-tailed right.
Step 4: Critical F = 4.8166.
Step 5: F = 136.9864 / 2.5180 = 54.403 (the printed 54.4039 uses unrounded mean squares; 410.9591 / 3 divided by 55.3949 / 22 gives 54.4039).
Step 6: 54.40 > 4.8166, reject H0; the model has explanatory power.
Python confirms 54.4029 from rounded and 54.4039 from unrounded inputs. ^ex-01-02-8

**Example 9: Knowledge check part 3, individual slope tests in Model 3 at the 1% level** (V1 p.41)

Given: CAPEX 1.2302 (se 0.1056), ADV -0.0371 (se 0.1062), R&D 0.1029 (se 0.2837); df = 26 - 3 - 1 = 22.
Step 1: H0: b_j = 0; Ha: b_j is not 0, two-tailed.
Step 2: Critical t at 1% with 22 df = 2.8188 (scipy gives 2.8188).
Step 3: CAPEX t = 1.2302 / 0.1056 = 11.649; ADV t = -0.0371 / 0.1062 = -0.3493; R&D t = 0.1029 / 0.2837 = 0.3627.
Step 4: Reject for CAPEX because 11.649 > 2.8188; fail to reject for ADV and R&D because both lie inside plus or minus 2.8188.
Interpretation: only CAPEX is individually significant; the printed t-statistics (11.6490, -0.3490, 0.3628) differ from the recomputed ones only by rounding (V1 p.41).
Python confirms 11.6496, -0.34934, 0.36271. ^ex-01-02-9

**Example 10: Knowledge check part 4, joint F-test of ADV and R&D at the 1% level** (V1 p.41-42)

Given: restricted Model 1 SSE = 55.9934 (24 df); unrestricted Model 3 SSE = 55.3949 (22 df); q = 2; n - k - 1 = 22.
Step 1: H0: b_ADV = b_R&D = 0; Ha: at least one is nonzero.
Step 2: Nested F with 2 and 22 df.
Step 3: alpha = 1%, one-tailed right.
Step 4: Critical F = 5.7190.
Step 5: Numerator = (55.9934 - 55.3949) / 2 = 0.5985 / 2 = 0.29925; denominator = 55.3949 / 22 = 2.51795; F = 0.29925 / 2.51795 = 0.1188.
Step 6: 0.1188 < 5.7190, fail to reject H0.
Interpretation: adding ADV and R&D removed only 0.5985 of SSE from a base of 55.99; Model 1 with CAPEX alone is the better model (V1 p.42).
Python confirms 0.118847. ^ex-01-02-10

**Example 11: Knowledge check part 5, stating the conclusion** (V1 p.42)

Combine the evidence.
Adjusted R-squared is higher for Model 1 (0.8749) than for Model 3 (0.8650).
ADV and R&D are each insignificant by t-test in Model 3 (Example 9).
ADV and R&D are jointly insignificant by the nested F-test of Model 1 against Model 3 (Example 10).
Conclusion: variation in ROA across this sample is explained by CAPEX; ADV and R&D add nothing individually or together (V1 p.42).
Note that all three lines of evidence point the same way here; when they disagree, the item-set patterns below show how the exam expects you to prioritise. ^ex-01-02-11

**Example 12: Knowledge check part 6, choosing among all seven ROA models** (V1 p.42)

Given the table of all subsets: CAPEX alone has R-squared 0.8803, adjusted 0.8753, AIC 23.8988, BIC 26.5226; the three-variable model has R-squared 0.8814, adjusted 0.8653, AIC 27.6481, BIC 31.0365; the models without CAPEX have R-squared below 0.15.
Step 1: Highest R-squared is the three-variable model, as it must be.
Step 2: Highest adjusted R-squared is CAPEX alone (0.8753).
Step 3: Lowest AIC is CAPEX alone (23.8988).
Step 4: Lowest BIC is CAPEX alone (26.5226).
Conclusion: CAPEX alone is the best model on adjusted R-squared, AIC and BIC simultaneously, and it is also the most parsimonious (V1 p.42).
See Example 4 for why the printed AIC and BIC levels do not reproduce from Equations 3 and 4; the ordering is unaffected. ^ex-01-02-12

**Example 13: Predicting the portfolio return with the five-factor model, with its interval** (V1 p.43-44)

Given: Y-hat = -2.1876 + 1.5992 F1 + 0.1923 F2 - 0.7126 F3 + 3.3376 F4 - 2.6832 F5; assumed values F1 = 0.110, F2 = 0.040, F3 = 0.080, F4 = -0.010, F5 = 0.001.
Step 1: Intercept term = 1 x (-2.1876) = -2.1876.
Step 2: 0.110 x 1.5992 = 0.1759.
Step 3: 0.040 x 0.1923 = 0.0077.
Step 4: 0.080 x (-0.7126) = -0.0570.
Step 5: -0.010 x 3.3376 = -0.0334.
Step 6: 0.001 x (-2.6832) = -0.0027.
Step 7: Sum = -2.1876 + 0.1759 + 0.0077 - 0.0570 - 0.0334 - 0.0027 = -2.0971, a predicted excess return of -2.0971% (V1 p.43).
Step 8: Software reports s_f = 1.1466 and 95% bounds of -4.4098 and 0.2119 (V1 p.44); t(0.025, 44) = 2.0154 and 2.0154 x 1.1466 = 2.3108 reproduces the half-width.
Note the interval is wider than one built from SEE = 1.1344 because s_f includes sampling error from the forecasted factors.
Both Factor 2 and Factor 5 are insignificant yet both stay in the forecast (V1 p.44).
Python confirms -2.09706. ^ex-01-02-13

**Example 14: Knowledge check, predicted ROA** (V1 p.44)

Given: ROA = 4.7022 + 1.2302 CAPEX - 0.0371 ADV + 0.1029 R&D with CAPEX = 5, ADV = 4, R&D = 3 (all in percent).
Step 1: 1.2302 x 5 = 6.1510.
Step 2: -0.0371 x 4 = -0.1484.
Step 3: 0.1029 x 3 = 0.3087.
Step 4: ROA-hat = 4.7022 + 6.1510 - 0.1484 + 0.3087 = 11.0135%.
Interpretation: the insignificant ADV and R&D slopes are still applied because the equation was estimated with them; dropping them would give 10.8532, a wrong answer the exam will offer (V1 p.44).
Python confirms 11.0135. ^ex-01-02-14

## Item-set patterns

> [!warning] Trap 1: "Which model provides the best fit" versus "which model is best for prediction"
> The vignette prints AIC and BIC side by side and asks two separate questions.
> Correct approach: BIC for fit, AIC for prediction, lowest value wins in both (V1 p.32).
> Distractors: the model with the highest R-squared (always the largest model, tempting because "fit" sounds like R-squared); the model with the lowest AIC when the question asked about fit; the model with the highest AIC or BIC, tempting for anyone who remembers "higher is better" from adjusted R-squared.

> [!warning] Trap 2: adjusted R-squared fell, so why
> A vignette shows R-squared rising from 0.852 to 0.852 and adjusted R-squared falling from 0.846 to 0.844 after adding a variable with t = -0.276.
> Correct approach: adjusted R-squared falls exactly when the added variable's |t| < 1, which signals the variable does not add explanatory power (V1 p.27).
> Distractors: "adjusted R-squared decreases because the new variable improves explanatory power" (internally contradictory but sounds technical); a statement about the previous variable added (SMB improved Model 2), which is true but answers a different question.

> [!warning] Trap 3: which sums of squares go into the joint F
> The vignette prints full ANOVA tables for three nested models and asks for the joint F for two variables.
> Correct approach: restricted SSE is from the model without the two variables, unrestricted SSE from the model with them, q = number of variables dropped, denominator df = n - k - 1 of the unrestricted model (V1 p.35).
> Distractors: dividing by the restricted model's MSE; dividing by SSE / n instead of SSE / (n - k - 1) (gives 9.454 instead of 8.863 in practice problem 5); using SSR differences with the wrong sign; using the intermediate model as the restricted model when the question named the smallest one.

> [!warning] Trap 4: individually insignificant but jointly significant, or the reverse
> Two variables each have |t| below the critical value, and the vignette asks whether they should be dropped.
> Correct approach: run the joint F-test; correlated regressors share explanatory power, so t-tests on each alone can understate their joint contribution (V1 p.35).
> Distractors: "both t-statistics are insignificant, therefore drop both" (ignores shared power); "the overall F is significant, therefore keep both" (the overall F tests all slopes, not these two).

> [!warning] Trap 5: forecast that omits the insignificant variable or the intercept
> The vignette gives assumed values for every variable and the estimated equation, then offers three numbers.
> Correct approach: include the intercept and every estimated slope, significant or not (V1 p.44).
> Distractors: the sum without the intercept (practice problem 4 option C, 4.555); the sum with an insignificant slope dropped; a sign slip on a negative assumed value (practice problem 4 option B, 3.992, from adding rather than subtracting the VIX term).

> [!warning] Trap 6: the general F-test proves the model is good
> The ANOVA F is 103.8 with a p-value of 0.000, and the question asks which statement about model quality is most accurate.
> Correct approach: rejecting H0: all slopes = 0 only shows at least one slope is nonzero; parsimony and fit require adjusted R-squared, AIC, BIC and the nested F (V1 p.37).
> Distractors: "the model is correctly specified"; "all slopes are significant"; "the model has the best fit among the candidates".

> [!warning] Trap 7: degrees of freedom and tails for the F-tests
> The question supplies a table or asks you to state the decision rule.
> Correct approach: nested F has q and n - k - 1 df, overall F has k and n - k - 1 df, and both are one-tailed to the right; the t-test for a slope is two-tailed with n - k - 1 df unless the alternative is directional (V1 p.35-37).
> Distractors: using n - k df; splitting alpha for the F-test as if two-tailed; using k + 1 in the numerator because the intercept was counted.

> [!warning] Trap 8: prediction interval built from the standard error of the regression
> The vignette gives SEE and, separately, a standard error of the forecast, then asks for the 95% interval.
> Correct approach: use s_f, which exceeds SEE because the forecasted independent variables add sampling error to model error (V1 p.44).
> Distractors: an interval using SEE (too narrow); using 1.96 instead of the t-value with n - k - 1 df; describing the interval as "the same as the within-sample error".

> [!warning] Trap 9: testing a slope against a non-zero value
> The vignette says "the analyst believes the market beta is 1" and prints t = 14.68 against zero.
> Correct approach: recompute t = (b-hat - 1) / s, or check whether 1 falls inside the reported confidence interval (V1 p.34).
> Distractors: rejecting because the printed t is huge; using the printed p-value; using a one-tailed critical value for a two-sided question.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM02-Evaluating-Regression-Model-Fit-and-Interpreting-Model-Results-Practice-Problems]]

## Cross-links

- [[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions]]: supplies the ANOVA table, the meaning of SSE, SSR, SST, the standard error of estimate, and the assumptions under which the t and F distributions used here are valid.
- [[LM03-Model-Misspecification]]: explains why a high R-squared can hide omitted-variable bias, heteroskedasticity or multicollinearity; multicollinearity is the reason this module insists on joint F-tests instead of separate t-tests.
- [[LM04-Extensions-of-Multiple-Regression]]: extends the same F-test and prediction logic to dummy variables, interaction terms and logistic regression, where the likelihood ratio test replaces the nested F and pseudo R-squared replaces R-squared.
- [[LM05-Time-Series-Analysis]]: reuses adjusted R-squared, AIC and BIC to choose autoregressive lag length, and reuses out-of-sample forecast error to compare models.
- [[LM06-Machine-Learning]]: the overfitting and parsimony ideas here become bias-variance trade-off, penalised regression and cross-validation.
- [[LM07-Big-Data-Projects]]: model selection by information criteria and holdout performance is the template for the model-training step in a data project.
- [[LM04-Using-Multifactor-Models]]: the five-factor and Fama-French comparisons in this module are the statistical side of the multifactor return models in Portfolio Management.

## Self-test

Vignette for Q1 to Q10.
Kestrel Capital regresses a fund's monthly excess return (in percent) on four factors, MKT, SMB, HML and MOM, using n = 60 months.
The four-factor (unrestricted) model has SST = 2,400.0 and SSE = 1,080.0.
A two-factor (restricted) model with MKT and SMB only has SSE = 1,200.0.
Estimated four-factor equation: Y-hat = 0.42 + 1.08 MKT + 0.35 SMB - 0.21 HML + 0.12 MOM; the HML and MOM t-statistics are -1.4 and 0.6.
The MKT coefficient has a standard error of 0.05.
Assumed factor values for next month: MKT = 2.5, SMB = -1.2, HML = 0.8, MOM = -3.0.
Software reports a standard error of the forecast of 4.90 for these assumed values.
Critical values: F(4, 55) at 5% = 2.54; F(2, 55) at 5% = 3.16 and at 1% = 5.01; t(55) two-tailed at 5% = 2.004; ln(60) = 4.094.

> [!question] Q1
> The adjusted R-squared of the four-factor model is closest to:
> A. 0.517
> B. 0.550
> C. 0.483

> [!question] Q2
> The F-statistic for the test that all four slopes are zero, and the decision at 5%, are:
> A. 16.81, reject H0
> B. 16.81, fail to reject H0
> C. 3.06, reject H0

> [!question] Q3
> The joint F-statistic for H0: b_HML = b_MOM = 0 and the decision at 5% are:
> A. 3.06, fail to reject H0
> B. 3.06, reject H0
> C. 6.11, reject H0

> [!question] Q4
> Using AIC and BIC, the model Kestrel should use for prediction and the model with the best fit are, respectively:
> A. the four-factor model and the two-factor model
> B. the four-factor model for both
> C. the two-factor model for both

> [!question] Q5
> A fifth factor with a t-statistic of 0.9 is added to the two-factor model. The most likely effect is that:
> A. both R-squared and adjusted R-squared rise
> B. R-squared rises and adjusted R-squared falls
> C. R-squared is unchanged and adjusted R-squared falls

> [!question] Q6
> The predicted excess return for next month from the four-factor model is closest to:
> A. 1.75
> B. 2.17
> C. 2.53

> [!question] Q7
> Kestrel believes the true MKT coefficient is 1.0. Testing H0: b_MKT = 1 against a two-sided alternative at 5%, the analyst should:
> A. reject H0 because t = 21.6 exceeds 2.004
> B. fail to reject H0 because t = 1.6 is below 2.004
> C. reject H0 because the coefficient's p-value against zero is below 0.05

> [!question] Q8
> Which comparison is a valid nested-model joint F-test?
> A. A model with MKT and SMB against a model with MKT, HML and MOM
> B. A model with MKT, SMB, HML and MOM against a model with MKT and SMB
> C. The four-factor model of excess return against a four-factor model of total return

> [!question] Q9
> The 95% prediction interval for next month's excess return is closest to:
> A. -7.65 to 11.99
> B. -6.71 to 11.05
> C. -2.73 to 7.07

> [!question] Q10
> Suppose instead that HML and MOM each had |t| below 2.004 but the joint F for the pair was 6.2. The best explanation is:
> A. the two factors are correlated and share explanatory power, so the joint test detects what the individual tests miss
> B. the joint test is invalid because it is inconsistent with the t-tests
> C. the overall F-test must be insignificant

> [!success]- Answer key
> Q1: A. R-squared = 1 - 1080 / 2400 = 0.55; adjusted = 1 - (59 / 55)(0.45) = 1 - 0.48273 = 0.5173. B is the unadjusted R-squared. C is the adjusted R-squared of the two-factor model, 1 - (59 / 57)(0.50) = 0.4825.
> Q2: A. SSR = 2400 - 1080 = 1320; MSR = 1320 / 4 = 330; MSE = 1080 / 55 = 19.636; F = 16.81 > 2.54, reject. B misapplies the decision rule. C is the nested F for two variables, not the overall F.
> Q3: A. F = [(1200 - 1080) / 2] / (1080 / 55) = 60 / 19.636 = 3.056 < 3.16, fail to reject at 5% (and at 1%). B reverses the decision. C forgets to divide the numerator by q = 2 (120 / 19.636 = 6.11).
> Q4: A. Four-factor: AIC = 60 ln(18) + 10 = 173.42 + 10 = 183.42; BIC = 173.42 + 4.094 x 5 = 193.89. Two-factor: AIC = 60 ln(20) + 6 = 179.74 + 6 = 185.74; BIC = 179.74 + 4.094 x 3 = 192.03. AIC prefers four factors (prediction); BIC prefers two factors (fit). B and C each apply one criterion to both purposes.
> Q5: B. R-squared never falls when a variable is added, so C is wrong; adjusted R-squared rises only if |t| > 1, and 0.9 < 1, so it falls, which rules out A. Numerically, SSE would drop to about 1182.9, R-squared 0.5071, adjusted 0.4807 versus 0.4825 before.
> Q6: B. 0.42 + 1.08(2.5) + 0.35(-1.2) - 0.21(0.8) + 0.12(-3.0) = 0.42 + 2.70 - 0.42 - 0.168 - 0.36 = 2.172. A omits the intercept (1.752). C drops the insignificant MOM term (2.532); insignificant variables stay in the forecast.
> Q7: B. t = (1.08 - 1.00) / 0.05 = 1.6, below 2.004, so fail to reject; the data cannot distinguish the fund's market beta from 1. A tests against zero (1.08 / 0.05 = 21.6), which is the wrong hypothesis. C uses the p-value against zero, the same error in a different form.
> Q8: B. A nested test requires the restricted model to be a subset of the unrestricted one with the same dependent variable; B drops HML and MOM (q = 2). A has models that are not nested (each contains variables the other lacks). C changes the dependent variable, so SSE values are not comparable.
> Q9: A. 2.172 plus or minus 2.004 x 4.90 = 2.172 plus or minus 9.82, giving -7.65 to 11.99. B uses SEE = sqrt(19.636) = 4.43 instead of s_f, which ignores the sampling error in forecasted factors. C is 2.172 plus or minus 4.90, a one-standard-error band, which is not a 95% interval.
> Q10: A. Correlated regressors share explanatory power that individual t-tests cannot attribute to either variable, which is exactly why the curriculum prescribes the joint F (V1 p.35). B is wrong because the tests answer different questions and can legitimately disagree. C is wrong because the overall F tests all four slopes and is 16.81 here.

## Flashcards

#flashcards/cfa-l2/01-Quantitative-Methods/lm02

R-squared in multiple regression is defined as::SSR / SST, the share of the variation in Y explained by the regression, equal to 1 - SSE / SST (V1 p.26).

Why is R-squared a poor model-selection tool in multiple regression?::It never decreases when a variable is added, says nothing about coefficient significance or bias, and a high value can reflect overfitting (V1 p.26-27).

Adjusted R-squared in sum-of-squares form::1 - [SSE / (n - k - 1)] / [SST / (n - 1)] (V1 p.27).

Adjusted R-squared in terms of R-squared::1 - [(n - 1) / (n - k - 1)](1 - R-squared) (V1 p.27).

Adding a variable raises adjusted R-squared if and only if::the absolute value of its t-statistic exceeds 1.0 (V1 p.27).

Does a rise in adjusted R-squared show the new variable is significant?::No; |t| > 1 is far below the 5% and 1% critical values, so the bar is low (V1 p.27).

Can adjusted R-squared be negative?::Yes, while R-squared has a minimum of zero (V1 p.27).

Relationship between R-squared and adjusted R-squared when k is at least 1::R-squared is strictly greater than adjusted R-squared (V1 p.27).

Overfitting is::a model with too many independent variables relative to the number of observations, so slopes stop reflecting true relationships (V1 p.27).

AIC formula::n ln(SSE / n) + 2(k + 1) (V1 p.32).

BIC formula::n ln(SSE / n) + ln(n)(k + 1) (V1 p.32).

Which criterion for prediction, which for goodness of fit?::AIC for prediction, BIC for best goodness of fit; lower is better for both (V1 p.32).

Why does BIC prefer smaller models than AIC?::Its penalty per parameter is ln(n), which exceeds 2 for any n above 7 (V1 p.32).

Is the absolute level of AIC or BIC meaningful?::No; only relative values among models with the same dependent variable matter (V1 p.32).

Which of the 31 five-factor models was best on AIC, BIC and adjusted R-squared?::The model with Factors 1 and 4; the all-five model had the highest R-squared but ranked poorly elsewhere (V1 p.38).

Interpretation of the intercept in multiple regression::The expected value of Y when all independent variables are zero (V1 p.33).

Interpretation of a slope in multiple regression::Expected change in Y for a one-unit change in that X holding all other independent variables constant (V1 p.33).

t-statistic for a single coefficient::(b-hat_j - B_j) / s_b-hat_j with n - k - 1 degrees of freedom (V1 p.34, p.41).

Two ways to test a slope against a non-zero hypothesised value::Recompute t with B_j in the numerator, or check whether B_j lies inside the reported confidence interval (V1 p.34).

Restricted versus unrestricted model::The unrestricted model has the full set of variables; the restricted model sets q of the slopes to zero by omitting those variables and is nested within it (V1 p.34).

Joint F-statistic for nested models::[(SSE_restricted - SSE_unrestricted) / q] / [SSE_unrestricted / (n - k - 1)] (V1 p.35).

Degrees of freedom of the nested F-test::q in the numerator and n - k - 1 in the denominator, with k from the unrestricted model (V1 p.35).

Null and alternative of the joint test on q slopes::H0 is that all q restricted slopes equal zero; Ha is that at least one of them is not zero (V1 p.35).

Why use a joint F-test rather than separate t-tests?::Correlated regressors share explanatory power that individual t-tests do not capture (V1 p.35).

Is the joint F-test one- or two-tailed?::One-tailed, right side; reject when the calculated F exceeds the critical value (V1 p.36).

General linear F-test statistic::F = MSR / MSE with k and n - k - 1 degrees of freedom; H0 is all k slopes equal zero (V1 p.37).

How is the overall F a special case of the nested F?::The restricted model is intercept only, so SSE_restricted = SST, the numerator is SSR / k and q = k (V1 p.36-37).

Exhibit 7 criteria: adjusted R-squared, AIC, BIC, t-statistic, joint F::Higher, lower, lower, outside the critical t bounds, above the critical F (V1 p.38).

Predicted value formula::Y-hat_f = b-hat_0 + sum over j of b-hat_j times X_jf (V1 p.43).

Two rules when forecasting with a multiple regression::Include every variable that was in the estimated model, even insignificant ones, and always include the intercept (V1 p.44).

Two sources of forecast error::Model error (the residual) and sampling error from forecasting the independent variables (V1 p.44).

Standard error of the forecast versus standard error of the regression::s_f is larger, so the prediction interval is wider than the within-sample error (V1 p.44).

Five-factor forecast reported by the curriculum::Point estimate -2.0971, s_f 1.1466, 95% bounds -4.4098 and 0.2119 (V1 p.43-44).

Micro-problem: R-squared 0.6155, n 50, k 5, adjusted R-squared?
?
1 - (49 / 44)(0.3845) = 0.5718; keystrokes 1 - 0.6155 = x 49 / 44 = +/- + 1 = (V1 p.29).

Micro-problem: SSE 56.6182, n 50, k 5, AIC?
?
50 ln(1.13236) + 12 = 6.215 + 12 = 18.215; keystrokes 56.6182 / 50 = LN x 50 = + 12 = (V1 p.32).

Micro-problem: SSE 56.6182, n 50, k 5, BIC?
?
6.215 + 3.912 x 6 = 29.687; compute 50 LN x 6 = 23.472 and add the stored 6.215 (V1 p.32).

Micro-problem: SSE_r 64.5176, SSE_u 56.6182, q 2, n - k - 1 44, joint F?
?
(7.8994 / 2) / (56.6182 / 44) = 3.9497 / 1.2868 = 3.0694; fail to reject at 1% against 5.120 (V1 p.36).

Micro-problem: SSE_r 1087.618, SSE_u 908.647, q 2, df 90, joint F?
?
89.4855 / 10.096 = 8.863; reject at 1% against 4.849 (V1 p.48).

Micro-problem: ROA = 4.7022 + 1.2302(5) - 0.0371(4) + 0.1029(3)?
?
4.7022 + 6.1510 - 0.1484 + 0.3087 = 11.0135 (V1 p.44).

Micro-problem: MSR 18.1247, MSE 1.2868, overall F and decision at 5% with critical 2.427?
?
14.0853, reject H0 that all five slopes are zero (V1 p.37).

Trap: a question asks for the best-fit model and one option has the highest R-squared. Why is it the trap?::R-squared always favours the largest model; fit is judged by BIC (lowest) or adjusted R-squared (highest) (V1 p.32, p.38).

Trap: forecast option that is exactly the intercept lower than the correct one. What went wrong?::The intercept was omitted; it must always be included (V1 p.44).

Trap: joint F computed with SSE_u / n in the denominator. What is wrong?::The denominator must be SSE_u / (n - k - 1), the unrestricted MSE; using n understates the denominator and inflates F (V1 p.35).

Trap: two variables each insignificant by t-test, so drop both. Why is that premature?::They may be correlated and jointly significant; the joint F-test is the right tool (V1 p.35).

{{Adjusted R-squared}} adjusts for degrees of freedom; {{AIC}} is preferred for prediction; {{BIC}} is preferred for goodness of fit (V1 p.25).

The joint F-test's null is that the slope coefficients of all independent variables {{outside the restricted model}} are zero (V1 p.26).

The general linear F-test's null is that the slopes on {{all independent variables in the unrestricted model}} are zero (V1 p.26).

In the five-factor example the joint test on Factors 4 and 5 gave F = {{3.0694}} against a 1% critical value of {{5.120}}, so the {{restricted}} model was preferred (V1 p.36).

The nested F for a single added variable equals the {{square of that variable's t-statistic}}, which is why adjusted R-squared rises only when |t| > 1 (V1 p.27).

## Common mistakes

1. Choosing the model with the highest R-squared; R-squared never falls when a variable is added, so it always picks the largest model (V1 p.26).
2. Reading a rise in adjusted R-squared as evidence of significance; the threshold is only |t| > 1 (V1 p.27).
3. Applying AIC to a "best fit" question or BIC to a "best prediction" question; AIC is for prediction, BIC for fit, both lower is better (V1 p.32).
4. Comparing AIC or BIC across models with different dependent variables, or reading meaning into the level of a single AIC (V1 p.32).
5. Using the restricted model's MSE, or SSE / n, in the denominator of the joint F; it must be SSE_unrestricted / (n - k - 1) with k from the unrestricted model (V1 p.35).
6. Forgetting to divide the SSE difference by q, or setting q to the number of variables in the unrestricted model instead of the number dropped (V1 p.35).
7. Treating the F-tests as two-tailed or the coefficient t-test as one-tailed when the alternative is "not equal" (V1 p.34-37).
8. Concluding a model is well specified or "best" because the overall F-test rejects; it only shows at least one slope is nonzero (V1 p.37).
9. Dropping insignificant variables from the forecast equation or omitting the intercept (V1 p.44).
10. Building the prediction interval from the standard error of the regression rather than the larger standard error of the forecast when the X values are forecasts (V1 p.44).
11. Testing a coefficient against a non-zero hypothesised value with the software's t-statistic against zero (V1 p.34).
12. Drawing conclusions about a group of variables from separate t-tests when the variables are correlated; use the joint F (V1 p.35).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "01-02" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
