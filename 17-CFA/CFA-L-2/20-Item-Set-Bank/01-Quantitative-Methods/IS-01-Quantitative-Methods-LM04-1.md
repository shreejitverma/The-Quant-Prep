---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 4
title: "Halvorsen Mutual: Spread Model Validation"
los: [los-01-04-a, los-01-04-b]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Halvorsen Mutual: Spread Model Validation

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Halvorsen Mutual Insurance runs a relative-value model for the industrial bonds in its general account.
Before the model can be used in the quarterly investment report, the model risk team must validate it.
Priya Nandakumar, CFA, a validation analyst, is assigned the review.

The model regresses the option-adjusted spread (OAS, in basis points) of 24 industrial bonds on three independent variables.
LEV is the issuer's debt-to-EBITDA ratio, COV is the issuer's EBITDA-to-interest coverage ratio, and SEC is a dummy variable equal to 1 if the bond is secured and 0 if it is unsecured.
Exhibit 1 presents the full-sample results.

**Exhibit 1: OAS regression, full sample (n = 24)**

| | Coefficient | Standard error | t-statistic | p-value |
|---|---|---|---|---|
| Intercept | 120.0 | 28.0 | 4.29 | 0.000 |
| LEV | 38.5 | 6.2 | 6.21 | 0.000 |
| COV | -12.4 | 4.1 | -3.02 | 0.007 |
| SEC | -42.6 | 15.0 | -2.84 | 0.010 |

$R^2$ = 0.781; mean OAS = 212.4 bps.

Nandakumar extracts the influence diagnostics for the seven bonds with the most unusual values (Exhibit 2).
The software did not return a studentized deleted residual for Bond 14 because its record was flagged for manual review.
For Bond 14, she recovers the full-sample residual of 31.0 bps, the mean squared error of the regression estimated without Bond 14, $MSE_{(14)}$ = 400.0, and its leverage.

**Exhibit 2: Influence diagnostics, selected bonds**

| Bond | Leverage $h_{ii}$ | Studentized deleted residual $t_i^*$ |
|---|---|---|
| 3 | 0.58 | 0.35 |
| 6 | 0.09 | 2.61 |
| 9 | 0.41 | -1.20 |
| 11 | 0.15 | -2.23 |
| 14 | 0.52 | not reported |
| 19 | 0.07 | -3.24 |
| 22 | 0.06 | 2.09 |

**Exhibit 3: Two-tailed critical t-values, 5% significance**

| Degrees of freedom | 19 | 20 | 21 |
|---|---|---|---|
| Critical value | 2.093 | 2.086 | 2.080 |

To judge whether any flagged bond changes the estimated relationship, Nandakumar re-estimates the model twice, once without Bond 3 and once without Bond 14.

**Exhibit 4: Re-estimated coefficients (p-values in parentheses)**

| | Without Bond 3 | Without Bond 14 |
|---|---|---|
| Intercept | 118.2 (0.001) | 131.5 (0.000) |
| LEV | 37.9 (0.000) | 27.1 (0.000) |
| COV | -12.1 (0.011) | -12.9 (0.004) |
| SEC | -41.8 (0.015) | -24.3 (0.148) |

Bond 19 is a secured bond whose issuer announced a covenant breach two weeks before the spread observation date.
The model's developer, Tomas Lindqvist, and Nandakumar exchange views on this bond.

Lindqvist (3 March): "Bond 19 has a studentized residual beyond 3 in absolute value, so it is a bad data point.
The cleanest fix is to delete it and re-estimate."

Nandakumar (4 March): "The spread for Bond 19 matches the dealer quotes, so it is not an entry error.
A valid outlier of this kind suggests the model may be missing a variable, such as a credit event indicator, and deleting it without that analysis would hide the problem."

The final section of the validation report requires Nandakumar to illustrate the model with a fitted spread.
She uses a secured bond whose issuer has LEV of 4.0 and COV of 3.5.

## Questions

1. Using the leverage measure, the bonds in Exhibit 2 that are potentially influential are: (LOS: los-01-04-a)
   - A. Bond 3 only.
   - B. Bonds 3 and 14.
   - C. Bonds 3, 9, and 14.
2. Considering only the bonds with a reported studentized deleted residual, the bonds flagged as potentially influential at the 5% significance level are: (LOS: los-01-04-a)
   - A. Bond 19 only.
   - B. Bonds 6, 11, and 19.
   - C. Bonds 6, 11, 19, and 22.
3. The studentized deleted residual for Bond 14 and the correct conclusion at the 5% significance level are closest to: (LOS: los-01-04-a)
   - A. 1.55; Bond 14 is not flagged.
   - B. 2.15; Bond 14 is flagged as potentially influential.
   - C. 2.24; Bond 14 is flagged as potentially influential.
4. Based on Exhibit 4, which statement about Bonds 3 and 14 is most accurate? (LOS: los-01-04-a)
   - A. Bond 3 is the more influential observation because it has the highest leverage in the sample.
   - B. Neither bond is influential because neither has a studentized deleted residual above 3 in absolute value.
   - C. Bond 14 is influential because excluding it lowers the LEV coefficient materially and removes the significance of SEC.
5. Regarding the statements on Bond 19, which is most likely correct? (LOS: los-01-04-a)
   - A. Only Lindqvist's statement.
   - B. Only Nandakumar's statement.
   - C. Both statements.
6. Using Exhibit 1, the fitted OAS for the bond Nandakumar uses as an illustration is closest to: (LOS: los-01-04-b)
   - A. 188.0 bps.
   - B. 230.6 bps.
   - C. 273.2 bps.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The leverage cutoff is $3\left(\frac{k+1}{n}\right) = 3 \times \frac{3+1}{24} = 0.5000$.
> Bond 3 (0.58) and Bond 14 (0.52) exceed 0.5000; Bond 9 (0.41) does not.
> A is wrong because it flags only the single largest leverage, which is not the rule.
> C is wrong because it uses $3k/n = 9/24 = 0.3750$, forgetting that the intercept is one of the $k+1$ estimated coefficients, which wrongly adds Bond 9.
> 2. **B.** Degrees of freedom are $n - k - 2 = 24 - 3 - 2 = 19$, so the critical value is 2.093.
> Absolute studentized residuals above 2.093: Bond 6 (2.61), Bond 11 (2.23), Bond 19 (3.24).
> Bond 22 at 2.09 falls just short of 2.093.
> A is wrong because it applies the $|t_i^*| > 3$ outlier rule of thumb instead of the stated 5% significance test.
> C is wrong because it uses $n - k - 1 = 20$ degrees of freedom and the critical value 2.086, which wrongly flags Bond 22.
> 3. **C.** $t_{14}^* = \frac{e_{14}}{\sqrt{MSE_{(14)}(1 - h_{14})}} = \frac{31.0}{\sqrt{400.0 \times (1 - 0.52)}} = \frac{31.0}{\sqrt{192.0}} = \frac{31.0}{13.8564} = 2.2372$.
> Because $2.2372 > 2.093$ (19 df), Bond 14 is flagged; it is also a high-leverage point, so it deserves the closest review.
> A is wrong because it divides by $\sqrt{MSE_{(14)}} = 20.0$ and omits the $(1 - h_{ii})$ adjustment: $31.0/20.0 = 1.55$.
> B is wrong because it puts the leverage itself under the square root instead of $1 - h_{ii}$: $31.0/\sqrt{400.0 \times 0.52} = 31.0/14.4222 = 2.1495$.
> 4. **C.** An observation is influential only if its exclusion substantially changes the estimated regression.
> Without Bond 14, the LEV coefficient falls from 38.5 to 27.1 and the SEC coefficient shrinks from -42.6 to -24.3 with its p-value rising from 0.010 to 0.148, so SEC is no longer significant at 5%.
> Without Bond 3, every coefficient changes by less than 2 units and every conclusion holds.
> A is wrong because high leverage identifies an unusual X value, not influence; Bond 3 barely moves the fit.
> B is wrong because the $|t_i^*| > 3$ rule flags outliers, while influence is judged by refitting and comparing; Bond 14's residual (2.24) is significant at 5% in any case.
> 5. **B.** Bond 19 is an outlier ($|-3.24| > 3$ and $> 2.093$), but the curriculum warns against automatic deletion.
> The recommended sequence is to check for a data error first; if the observation is valid, it may signal an omitted variable or a violated assumption.
> The covenant breach is exactly such a candidate variable, so Nandakumar's statement is correct.
> A and C are wrong because Lindqvist equates an outlier with bad data and deletes it without investigation.
> 6. **A.** $\widehat{OAS} = 120.0 + 38.5(4.0) - 12.4(3.5) - 42.6(1) = 120.0 + 154.0 - 43.4 - 42.6 = 188.0$ bps.
> The SEC coefficient is an intercept shift relative to the base group (unsecured bonds), so a secured bond's spread is 42.6 bps lower, other variables held constant.
> B is wrong because it sets SEC = 0, which is the fitted spread for an unsecured bond: 230.6 bps.
> C is wrong because it adds 42.6 instead of subtracting it: $230.6 + 42.6 = 273.2$ bps.

## Distractor design

- Q1: A = highest leverage only; C = cutoff $3k/n$ omits the intercept.
- Q2: A = outlier rule of thumb $|t^*| > 3$ used for an influence test at 5%; C = wrong degrees of freedom $n-k-1$.
- Q3: A = $(1-h_{ii})$ omitted; B = $h_{ii}$ used under the square root in place of $1-h_{ii}$.
- Q4: A = leverage confused with influence; B = outlier rule confused with the refit comparison.
- Q5: A and C = outlier treated as a data error and deleted automatically.
- Q6: B = dummy set to the base group (misread exhibit); C = sign error on the dummy coefficient.
