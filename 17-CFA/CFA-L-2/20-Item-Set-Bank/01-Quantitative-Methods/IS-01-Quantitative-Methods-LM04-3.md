---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 4
title: "Carrow Valley Bank: Small Business Default Logit"
los: [los-01-04-c]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Carrow Valley Bank: Small Business Default Logit

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Carrow Valley Bank is a regional lender with a large book of owner-occupied commercial real estate loans to small businesses.
Its credit risk policy requires every loan approval to include a model-based probability of default, and the bank's regulator has asked for documentation of how that probability is produced and interpreted.
Elena Marchetti, CFA, head of credit analytics, is preparing the documentation.

The model is a logistic regression estimated by maximum likelihood on 1,200 loans originated over a six-year period.
The dependent variable, DEFAULT, equals 1 if the borrower became 90 or more days past due within 12 months of origination and 0 otherwise.
The independent variables are:

- DSCR: the borrower's debt service coverage ratio at origination (times).
- LTV: the loan-to-value ratio at origination, in percent (for example, 70 means 70%).
- YEARS: the number of years the business has operated.

**Exhibit 1: Default logit, full model**

| | Coefficient | Standard error | z-statistic | p-value |
|---|---|---|---|---|
| Intercept | -1.850 | 0.410 | -4.51 | 0.000 |
| DSCR | -0.920 | 0.210 | -4.38 | 0.000 |
| LTV | 0.035 | 0.008 | 4.38 | 0.000 |
| YEARS | -0.060 | 0.033 | -1.82 | 0.069 |

Log-likelihood = -488.9; LL-Null = -520.4; pseudo-$R^2$ = 0.061.

**Exhibit 2: Restricted model estimated on the same 1,200 loans**

| Model | Independent variables | Log-likelihood |
|---|---|---|
| Restricted | DSCR, LTV | -490.6 |

**Exhibit 3: Chi-square critical values, 5% significance**

| Degrees of freedom | 1 | 2 | 3 |
|---|---|---|---|
| Critical value | 3.841 | 5.991 | 7.815 |

Marchetti's draft documentation contains three tasks.

First, the regulator's examiner has asked what the intercept means in probability terms.
Marchetti notes that no real borrower has all three independent variables equal to zero, but she agrees to report the implied value for completeness.

Second, the documentation includes a worked example for a pending application from Talbot Fabrication, a machine shop with a DSCR of 1.40, a requested LTV of 70%, and 8 years in operation.
Talbot's requested loan amount is $2.6 million, and the bank's policy limit for automatic approval is a 25% probability of default.

Third, the chief credit officer, David Okafor, wants to simplify the model.
In a memo dated 14 May, Okafor wrote: "YEARS is not significant at the 5% level in Exhibit 1.
Before we drop it, confirm with a likelihood ratio test whether the model without YEARS is adequate."
Marchetti also plans to explain to the loan officers how the LTV coefficient should be read, because several of them have been describing it as "the change in default probability per point of LTV."

## Questions

1. The probability of default implied by the intercept, for a loan on which all independent variables equal zero, is closest to: (LOS: los-01-04-c)
   - A. 13.6%.
   - B. 15.7%.
   - C. 86.4%.
2. The model's probability of default for Talbot Fabrication is closest to: (LOS: los-01-04-c)
   - A. 23.7%.
   - B. 31.1%.
   - C. 76.3%.
3. Holding DSCR and YEARS constant, a 10 percentage point increase in LTV is best described as: (LOS: los-01-04-c)
   - A. raising the probability of default by 35 percentage points.
   - B. raising the log odds of default by a factor of about 1.42.
   - C. multiplying the odds of default by about 1.42.
4. In response to Okafor's memo, the likelihood ratio statistic and the correct conclusion are: (LOS: los-01-04-c)
   - A. 1.70; fail to reject the restricted model, so YEARS can be dropped.
   - B. 3.40; fail to reject the restricted model, so YEARS can be dropped.
   - C. 63.00; reject the restricted model, so YEARS should be retained.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The intercept is the log odds of default when every independent variable is zero.
> Odds $= e^{-1.850} = 0.1572$; probability $= \frac{0.1572}{1 + 0.1572} = \frac{0.1572}{1.1572} = 0.1359$, or 13.6%.
> B is wrong because it reports the odds, 0.1572, as if it were the probability.
> C is wrong because it flips the sign in the exponent, $1/(1 + e^{-1.850}) = 0.8641$, which is the probability of no default.
> 2. **A.** $z = -1.850 - 0.920(1.40) + 0.035(70) - 0.060(8) = -1.850 - 1.2880 + 2.4500 - 0.4800 = -1.1680$.
> $P = \frac{1}{1 + e^{1.1680}} = \frac{1}{1 + 3.2156} = 0.2372$, or 23.7%, which is below the 25% policy limit.
> B is wrong because it reports the odds $e^{-1.1680} = 0.3110$ as the probability.
> C is wrong because of a sign error in the exponent, which returns $1 - P = 0.7628$.
> 3. **C.** A logit slope coefficient is the change in the log odds per unit change in the variable, holding the others constant.
> A 10-point increase raises the log odds by $0.035 \times 10 = 0.35$, so the odds are multiplied by $e^{0.35} = 1.4191$.
> A is wrong because it reads the log-odds change as a change in probability; the probability effect depends on where the borrower sits on the logistic curve.
> B is wrong because the log odds rise by 0.35 (additively), and 1.42 is the multiplier on the odds, not on the log odds.
> 4. **B.** The restricted model drops one variable, so $q = 1$.
> $LR = -2(LL_{restricted} - LL_{unrestricted}) = -2\left[-490.6 - (-488.9)\right] = -2(-1.7) = 3.40$.
> Since $3.40 < 3.841$, the bank fails to reject the null that the restricted model is adequate, and YEARS can be dropped at the 5% level (p-value 0.0652), consistent with its z-statistic of -1.82.
> A is wrong because it omits the factor of 2; the conclusion happens to match, but the statistic is wrong.
> C is wrong because it tests the full model against the intercept-only model, $-2[-520.4 - (-488.9)] = 63.00$, which answers a different question (joint significance of all three variables) and says nothing about YEARS alone.

## Distractor design

- Q1: B = odds reported as probability; C = sign error in the exponent (probability of the non-event).
- Q2: B = odds reported as probability; C = sign error in the exponent.
- Q3: A = log-odds coefficient read as a probability change; B = odds multiplier attached to the log odds.
- Q4: A = factor of 2 omitted from the LR statistic; C = wrong restricted model (intercept-only null instead of the model without YEARS).
