---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 4
title: "Kestrel Event Partners: Takeover Target Screen"
los: [los-01-04-c, los-01-04-b]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Kestrel Event Partners: Takeover Target Screen

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Kestrel Event Partners is a hedge fund that takes long positions in listed mid-cap companies it believes are likely to receive a takeover bid within 12 months.
Portfolio manager Aiko Tanabe, CFA, asks quantitative analyst Rafael Duarte to build a screen that ranks candidates by their probability of becoming a target.

Duarte estimates a logistic regression by maximum likelihood on 640 US company-years.
The dependent variable, TARGET, equals 1 if the company received a formal bid within the next 12 months and 0 otherwise.
The independent variables are:

- PB: price-to-book ratio.
- CASH: cash and equivalents divided by total assets (a decimal, so 0.15 means 15%).
- SIZE: the natural log of market capitalization in USD millions.
- TECH: equal to 1 for a technology company and 0 otherwise.
- HLTH: equal to 1 for a healthcare company and 0 otherwise.

Every company in the sample is in one of three sectors: technology, healthcare, or industrials.

**Exhibit 1: Takeover logit (n = 640)**

| | Coefficient | Standard error | z-statistic | p-value |
|---|---|---|---|---|
| Intercept | 0.350 | 0.170 | 2.06 | 0.040 |
| PB | -0.420 | 0.110 | -3.82 | 0.000 |
| CASH | 2.600 | 0.950 | 2.74 | 0.006 |
| SIZE | -0.180 | 0.140 | -1.29 | 0.199 |
| TECH | 0.620 | 0.270 | 2.30 | 0.022 |
| HLTH | 0.180 | 0.260 | 0.69 | 0.489 |

Log-likelihood = -297.6; LL-Null = -338.2; pseudo-$R^2$ = 0.120.

**Exhibit 2: Sample means of the continuous variables**

| PB | CASH | SIZE |
|---|---|---|
| 2.20 | 0.15 | 6.40 |

To test whether sector matters, Duarte re-estimates the model on the same 640 observations without TECH and HLTH.
The restricted model has a log-likelihood of -301.9.

**Exhibit 3: Chi-square critical values, 5% significance**

| Degrees of freedom | 2 | 5 | 6 |
|---|---|---|---|
| Critical value | 5.991 | 11.070 | 12.592 |

Tanabe raises four points in a meeting on 9 June.

First, she wants the model's baseline: the probability of a bid for an industrial company with sample-average PB, CASH, and SIZE.

Second, she asks how much that probability changes if the average industrial company's cash-to-assets ratio rises by 10 percentage points, all else equal.

Third, she asks how the odds of a bid for a technology company compare with those for an otherwise identical industrial company.

Fourth, she wants the screen applied to Corvane Systems, a technology company with PB of 1.40, CASH of 0.32, and SIZE of 5.10.
Kestrel's investment committee has ruled that the screen must use only the coefficients (including the intercept) that are statistically significant at the 5% level, and that a company is classified as a likely target if its probability exceeds 60%.

After the meeting, three colleagues comment on the model.

Tanabe: "A European version of this model, estimated by our London office on 410 European company-years, has a pseudo-$R^2$ of only 0.09, so our US model fits better."

Duarte: "Relative to the intercept-only model, the five independent variables are jointly significant, because the likelihood ratio statistic of 81.2 exceeds the critical value of 11.070."

A third colleague proposes replacing the logit with a linear probability model, arguing that its coefficients can be read directly as probability changes that are the same for every company.

## Questions

1. The probability of a bid for an industrial company with sample-average PB, CASH, and SIZE is closest to: (LOS: los-01-04-c)
   - A. 20.8%.
   - B. 26.3%.
   - C. 79.2%.
2. For the average industrial company, the change in the probability of a bid when CASH rises from 0.15 to 0.25 is closest to: (LOS: los-01-04-c)
   - A. +4.6 percentage points.
   - B. +26.0 percentage points.
   - C. +57.2 percentage points.
3. Holding the other variables constant, the odds of a bid for a technology company relative to those for an industrial company are closest to: (LOS: los-01-04-b)
   - A. 0.62 higher.
   - B. 1.55 times as large.
   - C. 1.86 times as large.
4. Applying the investment committee's rules, Corvane's probability of a bid and its classification are closest to: (LOS: los-01-04-c)
   - A. 22.9%; not a likely target.
   - B. 57.3%; not a likely target.
   - C. 77.1%; a likely target.
5. For the test of whether the two sector dummies jointly improve the model, the likelihood ratio statistic and conclusion are: (LOS: los-01-04-c)
   - A. 4.30; fail to reject that sector is irrelevant.
   - B. 8.60; reject that sector is irrelevant.
   - C. 8.60; fail to reject that sector is irrelevant.
6. Which of the comments made after the meeting is most accurate? (LOS: los-01-04-c)
   - A. Tanabe's comment.
   - B. Duarte's comment.
   - C. The third colleague's comment.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** An industrial company is the base group, so TECH = HLTH = 0.
> $z_0 = 0.350 - 0.420(2.20) + 2.600(0.15) - 0.180(6.40) = 0.350 - 0.9240 + 0.3900 - 1.1520 = -1.3360$.
> $P_0 = \frac{1}{1 + e^{1.3360}} = \frac{1}{1 + 3.8038} = 0.2082$, or 20.8%.
> B is wrong because it reports the odds $e^{-1.3360} = 0.2629$ as the probability.
> C is wrong because of a sign error in the exponent, which gives $1 - P_0 = 0.7918$.
> 2. **A.** Raising CASH by 0.10 adds $2.600 \times 0.10 = 0.2600$ to the log odds: $z_1 = -1.3360 + 0.2600 = -1.0760$.
> $P_1 = \frac{1}{1 + e^{1.0760}} = 0.2543$, so $\Delta P = 0.2543 - 0.2082 = 0.0461$, about +4.6 percentage points.
> (Check: $P_0(1 - P_0) \times 2.600 \times 0.10 = 0.0429$, close to the exact change.)
> B is wrong because it treats the log-odds change of 0.26 as a probability change of 26 percentage points.
> C is wrong because it raises CASH by one whole unit (from 0.15 to 1.15) instead of by the stated 0.10: $P = 0.7797$, change $= 0.5715$.
> 3. **C.** TECH is measured against the omitted base category, industrials.
> Being a technology company adds 0.620 to the log odds, so the odds are multiplied by $e^{0.620} = 1.8589$.
> A is wrong because 0.620 is the change in the log odds, not in the odds.
> B is wrong because it measures technology against healthcare rather than the base group: $e^{0.620 - 0.180} = e^{0.440} = 1.5527$.
> 4. **C.** At 5%, the intercept (p = 0.040), PB, CASH, and TECH are significant; SIZE (p = 0.199) and HLTH (p = 0.489) are not.
> $z = 0.350 - 0.420(1.40) + 2.600(0.32) + 0.620(1) = 0.350 - 0.5880 + 0.8320 + 0.6200 = 1.2140$.
> $P = \frac{1}{1 + e^{-1.2140}} = \frac{1}{1 + 0.2970} = 0.7710$, or 77.1%, which exceeds 60%, so Corvane is classified as a likely target.
> A is wrong because of a sign error in the exponent: $1/(1 + e^{1.2140}) = 0.2290$.
> B is wrong because it uses every coefficient, including SIZE: $z = 1.2140 - 0.180(5.10) = 0.2960$ and $P = 0.5735$, which ignores the committee's rule.
> 5. **B.** The restricted model removes TECH and HLTH, so $q = 2$.
> $LR = -2\left[-301.9 - (-297.6)\right] = -2(-4.3) = 8.60$, and $8.60 > 5.991$, so the null that the restricted model is adequate is rejected (p-value 0.0136).
> The sector dummies are jointly significant even though HLTH alone is not.
> A is wrong because it omits the factor of 2 and then fails to reject.
> C is wrong because it uses 6 degrees of freedom (the number of estimated coefficients) and the critical value 12.592 instead of the 2 restrictions.
> 6. **B.** $LR = -2\left[-338.2 - (-297.6)\right] = -2(-40.6) = 81.20$ with $q = 5$ restrictions, and $81.20 > 11.070$, so the five variables are jointly significant.
> A is wrong because pseudo-$R^2$ is valid only for comparing specifications of the same model on the same dataset; the European model uses a different sample.
> C is wrong because a linear probability model can produce fitted probabilities below 0 or above 1 and forces the effect of each variable on the probability to be constant, which is precisely the defect the logit corrects.

## Distractor design

- Q1: B = odds reported as probability; C = sign error in the exponent.
- Q2: B = log-odds change read as a probability change; C = wrong increment (one whole unit instead of the stated 0.10).
- Q3: A = log odds read as odds; B = wrong base category (healthcare instead of industrials).
- Q4: A = sign error in the exponent; B = all coefficients used despite the significance rule.
- Q5: A = factor of 2 omitted; C = wrong degrees of freedom (coefficients counted instead of restrictions).
- Q6: A = pseudo-$R^2$ compared across different datasets; C = linear probability model defects ignored.
