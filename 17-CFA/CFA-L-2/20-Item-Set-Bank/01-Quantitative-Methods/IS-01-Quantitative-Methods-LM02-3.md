---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 2
title: "Kalmar Specialty Chemicals IPO multiple regression"
los: [los-01-02-a, los-01-02-b, los-01-02-c]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Kalmar Specialty Chemicals IPO multiple regression

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tomasz Wierzbicki is an equity analyst at Vistula Securities, one of the banks advising on the planned initial public offering of Kalmar Specialty Chemicals.
Kalmar is owned by a private equity fund and has no traded share price, so Wierzbicki values it from a cross-sectional regression of listed peers' forward EV/EBITDA multiples.
His sample contains n = 38 listed European specialty chemicals companies.
The dependent variable is the forward EV/EBITDA multiple (times).
The independent variables are GROWTH, the consensus three-year EBITDA growth rate (percent per year); ROIC, return on invested capital (percent); LEV, net debt to EBITDA (turns); and BETA, the equity beta against a regional index.

Exhibit 1. Estimated peer regression

| Variable | Coefficient | t-statistic |
|---|---|---|
| Intercept | 4.10 | 5.62 |
| GROWTH | 0.42 | 5.10 |
| ROIC | 0.15 | 3.20 |
| LEV | -0.55 | -1.90 |
| BETA | -0.80 | -0.70 |

Exhibit 2. ANOVA and fit

| Item | Value |
|---|---|
| Regression sum of squares | 103.47 |
| Residual sum of squares | 27.93 |
| Total sum of squares | 131.40 |
| Standard error of estimate | 0.92 |
| Residual sum of squares, model with GROWTH and ROIC only | 32.40 |
| Median peer multiple | 7.4x |

Exhibit 3. Kalmar inputs (fiscal 2026 estimates)

| Item | Value |
|---|---|
| GROWTH | 7.5 |
| ROIC | 11.0 |
| LEV | 2.4 |
| BETA (estimated from peers) | 1.15 |
| EBITDA | EUR 185 million |
| Net debt | EUR 444 million |
| Dividend payout ratio | 35% |

For Kalmar's inputs, the software reports a standard error of the forecast of 1.05 turns.
The relevant critical values are $t_{0.025}(33) = 2.035$ and $F_{0.05}(2, 33) = 3.285$.

Wierzbicki's team leader, Anna Dudek, reviewed the draft on 9 September 2026.
"BETA is nowhere near significant, so take it out of the equation before you plug in Kalmar's numbers; the multiple will be cleaner."
"And since LEV is also insignificant at 5%, test whether LEV and BETA can be dropped together, then tell me the model's adjusted R-squared so the syndicate desk can judge how much weight to put on it."

Wierzbicki notes that the fund intends to price the offering below the lower end of the 95% prediction range if demand is weak, and that the syndicate desk wants that lower bound expressed as an equity value.

## Questions

1. Using the estimated regression, Kalmar's predicted EV/EBITDA multiple is closest to: (LOS: los-01-02-c)
   - A. 6.66x
   - B. 7.58x
   - C. 9.30x
2. The lower bound of the 95% prediction interval for Kalmar's equity value is closest to: (LOS: los-01-02-c)
   - A. EUR 393 million
   - B. EUR 442 million
   - C. EUR 837 million
3. The adjusted R-squared of the four-variable model, and the effect on adjusted R-squared of removing BETA, are most likely: (LOS: los-01-02-a)
   - A. 0.762; adjusted R-squared would fall if BETA were removed
   - B. 0.762; adjusted R-squared would rise if BETA were removed
   - C. 0.787; adjusted R-squared would rise if BETA were removed
4. For Dudek's joint test at the 5% level, the F-statistic and the conclusion are: (LOS: los-01-02-b)
   - A. 2.64; fail to reject, so the four-variable model is preferred
   - B. 2.64; fail to reject, so the model with GROWTH and ROIC only is preferred
   - C. 5.28; reject, so LEV and BETA should be retained

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** $\hat{Y} = 4.10 + 0.42(7.5) + 0.15(11.0) - 0.55(2.4) - 0.80(1.15)$.
>    Terms: $4.10 + 3.15 + 1.65 - 1.32 - 0.92 = 6.66$x.
>    Every variable in the estimated equation is used, including BETA, because the slopes were estimated jointly; Dudek's first instruction is wrong.
>    B is wrong because it drops the insignificant BETA term, $6.66 + 0.92 = 7.58$.
>    C is wrong because it adds the LEV term instead of subtracting it, $6.66 + 2(1.32) = 9.30$.
> 2. **A.** Half-width $= t_{0.025}(33) \times s_f = 2.035 \times 1.05 = 2.13675$, so the lower multiple is $6.66 - 2.13675 = 4.52325$x.
>    Lower enterprise value $= 4.52325 \times 185 = 836.80$; lower equity value $= 836.80 - 444 = 392.80$, about EUR 393 million.
>    B is wrong because it uses the standard error of estimate, $6.66 - 2.035 \times 0.92 = 4.7878$x, giving $4.7878 \times 185 - 444 = 441.74$; the forecast standard error of 1.05 is the right input because Kalmar's inputs are themselves estimates.
>    C is wrong because it stops at enterprise value, EUR 837 million, and does not deduct net debt.
> 3. **B.** $R^2 = 103.47 / 131.40 = 0.78744$.
>    $\bar{R}^2 = 1 - \frac{27.93 / 33}{131.40 / 37} = 1 - \frac{0.84636}{3.55135} = 0.76168$, equivalently $1 - (37 / 33)(0.21256) = 0.76168$.
>    BETA's $|t| = 0.70$ is below 1.0, so removing it would raise adjusted R-squared, because the variable does not earn the degree of freedom it uses.
>    A is wrong because it confuses adjusted R-squared with R-squared; R-squared would fall on removal, but adjusted R-squared rises whenever the removed variable has $|t| < 1$.
>    C is wrong because 0.787 is the unadjusted R-squared.
> 4. **B.** $H_0: b_{LEV} = b_{BETA} = 0$ against $H_a$: at least one is not zero; $q = 2$ and $n - k - 1 = 33$.
>    $F = \frac{(32.40 - 27.93) / 2}{27.93 / 33} = \frac{2.2350}{0.84636} = 2.6407$.
>    2.64 is below 3.285, so fail to reject; LEV and BETA jointly add nothing at 5%, and the more parsimonious restricted model is preferred.
>    A is wrong because failing to reject favours the restricted model, not the unrestricted one.
>    C is wrong because it does not divide the rise in SSE by $q$, $4.47 / 0.84636 = 5.2814$, which flips the decision.

## Distractor design

1. B: insignificant variable dropped from the forecast; C: sign error on a negative slope.
2. B: standard error of estimate used instead of the standard error of the forecast; C: enterprise value reported without deducting net debt.
3. A: R-squared behaviour attributed to adjusted R-squared; C: unadjusted R-squared reported.
4. A: correct statistic, but failing to reject is read as favouring the unrestricted model; C: rise in SSE not divided by $q$.
