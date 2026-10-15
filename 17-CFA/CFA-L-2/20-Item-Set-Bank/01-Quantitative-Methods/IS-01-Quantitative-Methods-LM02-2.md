---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 2
title: "Northgate Bancorp credit spread model validation"
los: [los-01-02-a, los-01-02-b, los-01-02-c]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Northgate Bancorp credit spread model validation

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Northgate Bancorp prices loans to investment-grade corporate borrowers off a cross-sectional model of bond option-adjusted spreads (OAS, in basis points).
Under the bank's model risk policy, every pricing model must be independently validated before its annual reapproval.
Elena Varga, a validator in the Model Risk Management group, is reviewing the model submitted by Samuel Reid of the credit analytics desk.

Reid estimated the unrestricted model (Model U) on n = 120 issuers:

$$ OAS_i = b_0 + b_1 LEV_i + b_2 COV_i + b_3 VOL_i + b_4 SIZE_i + b_5 LIQ_i + \varepsilon_i $$

LEV is net debt to EBITDA (turns), COV is EBITDA to interest expense (times), VOL is 12-month equity volatility (percentage points), SIZE is the natural log of total assets in USD billions, and LIQ is the average bid-ask spread in price points.
Reid then dropped SIZE and LIQ, both individually insignificant at 5%, and submitted the restricted Model R with LEV, COV and VOL only.

Exhibit 1. Model U estimated coefficients

| Variable | Coefficient | Standard error | t-statistic |
|---|---|---|---|
| Intercept | 38.40 | 9.85 | 3.90 |
| LEV | 14.60 | 2.10 | 6.95 |
| COV | -3.20 | 0.95 | -3.37 |
| VOL | 2.52 | 0.28 | 9.00 |
| SIZE | -4.10 | 2.53 | -1.62 |
| LIQ | 6.80 | 4.82 | 1.41 |

Exhibit 2. Summary statistics

| Statistic | Model U | Model R |
|---|---|---|
| Independent variables | 5 | 3 |
| Residual sum of squares | 41,800 | 44,300 |
| R-squared | 0.6473 | 0.6262 |
| Standard error of estimate (bp) | 19.15 | 19.54 |
| Correlation of SIZE with LIQ | -0.71 | n/a |

The total sum of squares is 118,500 for both models.

Selected critical values:

| Distribution | 1% | 2.5% | 5% |
|---|---|---|---|
| $F(2, 114)$, right tail | 4.796 | 3.811 | 3.076 |
| $F(5, 114)$, right tail | 3.182 | 2.680 | 2.294 |
| $t(114)$, one tail | 2.360 | 1.981 | 1.658 |

A prudential guideline issued to the bank sets a benchmark sensitivity of 2.0 bp of spread per point of equity volatility and asks validators to test whether the fitted sensitivity is consistent with it.

For the reapproval file, Varga must price a new borrower, Castell Freight, with LEV 3.2, COV 6.5, VOL 28, SIZE 2.3 and LIQ 1.5, using Model U.
The estimation software reports a standard error of the forecast of 20.40 bp for Castell's inputs, which themselves are analyst projections for next year.

On 2 June 2026, the two staff members recorded the following statements in the validation log.

Reid: "Model U's F-statistic has a p-value below 0.0001, which confirms that the specification is correct and that each of the five variables is significant. Because SIZE and LIQ each fail the t-test, Model R is the right model to approve."

Varga: "Rejecting the overall null tells us only that at least one slope is nonzero. SIZE and LIQ are strongly correlated, so I will test them jointly before accepting the restriction, and I will compare the models on information criteria computed from the residual sums of squares."

## Questions

1. The hypotheses and decision rule for Varga's joint test of SIZE and LIQ at the 5% level are most accurately stated as: (LOS: los-01-02-b)
   - A. $H_0: b_4 = b_5 = 0$; $H_a$: at least one of $b_4$, $b_5$ is not zero; reject if $F > 3.076$
   - B. $H_0: b_4 = b_5 = 0$; $H_a$: at least one of $b_4$, $b_5$ is not zero; reject if $F > 3.811$
   - C. $H_0: b_4 = b_5 = 0$; $H_a$: $b_4 \neq 0$ and $b_5 \neq 0$; reject if $F > 3.076$
2. The joint F-statistic for SIZE and LIQ and the most appropriate validation conclusion are: (LOS: los-01-02-b)
   - A. 1.36; fail to reject, so the restriction in Model R is supported
   - B. 3.41; reject, so SIZE and LIQ should not be dropped
   - C. 3.41; fail to reject, because SIZE and LIQ are each insignificant by their t-tests
3. Computing AIC and BIC from the residual sums of squares, the model preferred for goodness of fit and the model preferred for prediction are, respectively: (LOS: los-01-02-a)
   - A. Model U and Model U
   - B. Model U and Model R
   - C. Model R and Model U
4. The F-statistic for the test that all slopes in Model U equal zero, and the analyst whose statement about it is correct, are: (LOS: los-01-02-a)
   - A. 34.86; Varga's statement is correct
   - B. 41.84; Varga's statement is correct
   - C. 41.84; Reid's statement is correct
5. The test the prudential guideline requires, at the 5% level against a two-sided alternative, leads to which conclusion? (LOS: los-01-02-b)
   - A. Reject $H_0: b_3 = 2.0$, because $t = 9.00$ exceeds 1.981
   - B. Reject $H_0: b_3 = 2.0$, because $t = 1.86$ exceeds 1.658
   - C. Fail to reject $H_0: b_3 = 2.0$, because $t = 1.86$ is below 1.981
6. The 95% prediction interval for Castell Freight's OAS from Model U is closest to: (LOS: los-01-02-c)
   - A. 95.2 bp to 176.1 bp
   - B. 97.7 bp to 173.6 bp
   - C. 115.3 bp to 156.1 bp

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The joint test drops $q = 2$ variables, so the null is that both slopes are zero and the alternative is that at least one is not.
>    The statistic has $q = 2$ and $n - k - 1 = 120 - 5 - 1 = 114$ degrees of freedom and the test is one-tailed to the right, so the 5% critical value is $F_{0.05}(2, 114) = 3.076$.
>    B is wrong because it splits alpha as if the F-test were two-tailed and uses the 2.5% value 3.811.
>    C is wrong because the alternative to "all restricted slopes are zero" is "at least one is not zero", not "both are nonzero".
> 2. **B.** $MSE_U = 41{,}800 / 114 = 366.6667$.
>    $F = \frac{(44{,}300 - 41{,}800) / 2}{366.6667} = \frac{1{,}250.0000}{366.6667} = 3.4091$.
>    3.41 exceeds 3.076, so reject $H_0$ (p-value 0.0365); SIZE and LIQ jointly explain OAS and Reid's restriction is not supported.
>    The correlation of -0.71 between SIZE and LIQ is why each t-test understates their shared explanatory power.
>    A is wrong because it sets $q$ equal to the five variables of Model U instead of the two dropped, $(2{,}500 / 5) / 366.6667 = 1.3636$.
>    C is wrong because it lets the individual t-tests overrule the joint test; the joint F is the correct tool when regressors are correlated.
> 3. **C.** $AIC = n \ln(SSE / n) + 2(k + 1)$ and $BIC = n \ln(SSE / n) + \ln(n)(k + 1)$, with $\ln(120) = 4.7875$.
>    Model U: $120 \ln(41{,}800 / 120) = 702.3792$, so $AIC_U = 702.3792 + 12 = 714.3792$ and $BIC_U = 702.3792 + 4.7875(6) = 731.1041$.
>    Model R: $120 \ln(44{,}300 / 120) = 709.3498$, so $AIC_R = 709.3498 + 8 = 717.3498$ and $BIC_R = 709.3498 + 4.7875(4) = 728.4998$.
>    BIC, the goodness-of-fit criterion, is lower for Model R; AIC, the prediction criterion, is lower for Model U.
>    A is wrong because it applies the AIC ranking to both purposes, ignoring BIC's heavier penalty of 4.79 per parameter.
>    B is wrong because it swaps the purposes of the two criteria.
> 4. **B.** $R^2_U = 1 - 41{,}800 / 118{,}500 = 0.64726$.
>    $F = \frac{R^2 / k}{(1 - R^2) / (n - k - 1)} = \frac{0.64726 / 5}{0.35274 / 114} = \frac{0.12945}{0.0030942} = 41.8364$, equivalently $(76{,}700 / 5) / 366.6667$.
>    41.84 exceeds $F_{0.05}(5, 114) = 2.294$, but rejecting shows only that at least one slope is nonzero, which is Varga's statement.
>    A is wrong because it counts the intercept in the numerator degrees of freedom, $(0.64726 / 6) / 0.0030942 = 34.8636$.
>    C is wrong because the overall F does not establish correct specification or the significance of each slope; SIZE and LIQ are individually insignificant.
> 5. **C.** $H_0: b_3 = 2.0$ against $H_a: b_3 \neq 2.0$, with 114 degrees of freedom.
>    $t = (2.52 - 2.0) / 0.28 = 1.8571$, which lies inside plus or minus 1.981, so fail to reject; the fitted sensitivity is consistent with the benchmark.
>    A is wrong because 9.00 is the software's t-statistic against zero, which tests the wrong hypothesis.
>    B is wrong because it uses the 5% one-tailed critical value, 1.658, for a two-sided alternative.
> 6. **A.** $\hat{Y} = 38.40 + 14.60(3.2) - 3.20(6.5) + 2.52(28) - 4.10(2.3) + 6.80(1.5)$.
>    Terms: $38.40 + 46.72 - 20.80 + 70.56 - 9.43 + 10.20 = 135.65$ bp.
>    Half-width $= t_{0.025}(114) \times s_f = 1.981 \times 20.40 = 40.4122$, so the interval is 95.24 bp to 176.06 bp.
>    B is wrong because it uses the standard error of estimate, 19.15, which omits the sampling error from projected inputs: $135.65 \pm 1.981 \times 19.1485$ gives 97.72 to 173.58.
>    C is wrong because $135.65 \pm 20.40$ is a one-standard-error band, not a 95% interval.

## Distractor design

1. B: F-test treated as two-tailed with alpha split; C: alternative hypothesis misstated as "both nonzero".
2. A: $q$ set to the number of variables in the unrestricted model; C: individual t-tests allowed to overrule the joint F with correlated regressors.
3. A: AIC ranking applied to the fit question; B: AIC and BIC purposes swapped.
4. A: intercept counted in numerator degrees of freedom; C: overall F read as proof of specification and of every slope's significance.
5. A: software t-statistic against zero used for a non-zero hypothesised value; B: one-tailed critical value used for a two-sided test.
6. B: standard error of estimate used instead of the standard error of the forecast; C: one-standard-error band instead of $t \times s_f$.
