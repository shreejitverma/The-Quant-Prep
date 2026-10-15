---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 1
title: "Aldercrest Sovereign Fund Country-Risk Report"
los: [los-01-01-a, los-01-01-b, los-01-01-c]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Aldercrest Sovereign Fund Country-Risk Report

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Rafael Ibarra-Kwan is an analyst on the emerging-market equity team of the Aldercrest Sovereign Fund.
Each year the team publishes an appendix to the fund's annual report explaining how country-risk dimensions relate to the equity returns of the markets in which it invests.
This year, Ibarra-Kwan estimates a cross-country multiple linear regression on 42 markets.

The dependent variable is each market's annual equity excess return over US Treasury bills (ER), in whole percentages.
The independent variables are the change in the market's political-risk rating over the year (POL, in rating points, where a positive value means lower risk), the real GDP growth surprise relative to the consensus forecast at the start of the year (GROWTH, in percentage points), and the change in the market's five-year sovereign CDS spread (CDS, in percentage points).

**Exhibit 1: Regression of ER on POL, GROWTH and CDS (42 markets)**

| Variable | Coefficient |
|---|---|
| Intercept | 1.80 |
| POL | 0.65 |
| GROWTH | 1.20 |
| CDS | -4.50 |
| Mean ER across the 42 markets | 2.40 |

For the appendix, the fund's reporting office asks for a worked illustration using six pilot markets whose names are anonymised.

**Exhibit 2: Pilot markets**

| Market | POL | GROWTH | CDS | Actual ER | Fitted ER |
|---|---|---|---|---|---|
| Arvenia | 2 | 1.5 | -0.40 | 6.9 | 6.70 |
| Belmora | -1 | -0.5 | 0.60 | -5.8 | -2.15 |
| Castellan | 0 | 0.8 | 0.10 | 1.6 | 2.31 |
| Dravia | 3 | 2.0 | -0.80 | 13.1 | 9.75 |
| Estoria | -2 | -1.2 | 1.10 | -9.4 | -5.89 |
| Fennick | 1 | 0.4 | 0.20 | 4.8 | 2.03 |

The reporting office wants the appendix to state the variation of ER in the pilot sample, defined as in the regression literature, and to show the residual for Dravia.

Ibarra-Kwan's draft of the diagnostics section contains two findings.
First, a plot of the residuals against GROWTH for all 42 markets shows an inverted U-shape: residuals are mostly negative for large negative and large positive growth surprises and mostly positive for surprises near zero.
Second, the sample correlation between GROWTH and CDS is -0.91 and is statistically significant, whereas the correlations of POL with the other two variables are close to zero.

His supervisor, Helena Voss, reviews the draft on 18 February.
She notes that Ibarra-Kwan also estimated an alternative specification without POL.
Both specifications have a significant overall fit, and the alternative explains the variation in ER at least as well with fewer variables.
Voss writes: "We have run through the process, but we have not yet shown that the published specification is the best of our candidates."
Ibarra-Kwan responds on 19 February: "The three-variable model passed the assumption and significance gates, so it is ready for the appendix."

## Questions

1. The variation of ER in the six-market pilot sample is closest to: (LOS: los-01-01-b)
   - A. 45.08
   - B. 69.18
   - C. 345.91
2. The residual for Dravia is closest to: (LOS: los-01-01-c)
   - A. -3.35
   - B. 3.35
   - C. 11.23
3. The most accurate interpretation of the intercept for the appendix is that: (LOS: los-01-01-b)
   - A. a market with no change in political-risk rating, no growth surprise and no change in its CDS spread is expected to earn an excess return of 1.80%.
   - B. the average market in the 42-market sample is expected to earn an excess return of 1.80%.
   - C. each one-point improvement in the political-risk rating adds 1.80 percentage points to excess return, holding GROWTH and CDS constant.
4. The first diagnostic finding most likely indicates that: (LOS: los-01-01-c)
   - A. the residuals are fat-tailed and the normality assumption is violated.
   - B. the residual variance changes with GROWTH, violating homoskedasticity.
   - C. the relationship between ER and GROWTH is not linear, so the model is misspecified.
5. Regarding the 18 February and 19 February statements, under the regression process the most appropriate next step is to: (LOS: los-01-01-a)
   - A. publish the three-variable model, because it passed the assumption and overall-significance gates.
   - B. adjust the model and re-estimate, because the three-variable model has not cleared every gate of the regression process.
   - C. re-check the regression assumptions before considering goodness of fit, because the alternative drops POL.
6. The second diagnostic finding is best described as: (LOS: los-01-01-c)
   - A. an exact linear relation between GROWTH and CDS, so the model cannot be estimated.
   - B. an approximate linear relation between GROWTH and CDS, so the model can be estimated but their coefficients are difficult to interpret.
   - C. a violation of independence of errors, because the residuals for GROWTH and CDS are correlated.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The variation of Y is the sum of squared deviations from the mean, $\sum (Y_i - \bar{Y})^2$, also called the sum of squares total (V1 p.8).
> Mean: $\bar{Y} = (6.9 - 5.8 + 1.6 + 13.1 - 9.4 + 4.8) / 6 = 11.2 / 6 = 1.8667$.
> Squared deviations: Arvenia $(6.9 - 1.8667)^2 = 25.3344$; Belmora $(-5.8 - 1.8667)^2 = 58.7778$; Castellan $(1.6 - 1.8667)^2 = 0.0711$; Dravia $(13.1 - 1.8667)^2 = 126.1878$; Estoria $(-9.4 - 1.8667)^2 = 126.9378$; Fennick $(4.8 - 1.8667)^2 = 8.6044$.
> Sum: $345.9133$, about 345.91.
> A (45.08) is wrong because it sums squared residuals, $\sum (Y_i - \hat{Y}_i)^2$: $0.20^2 + (-3.65)^2 + (-0.71)^2 + 3.35^2 + (-3.51)^2 + 2.77^2 = 45.0821$, which is the unexplained part, not the total variation.
> B (69.18) is wrong because it divides the sum of squares by $n - 1 = 5$, giving the sample variance, $345.9133 / 5 = 69.1827$.
> 2. **B.** The residual is $e_i = Y_i - \hat{Y}_i$ (V1 p.13).
> For Dravia the fitted value from Exhibit 1 is $1.80 + 0.65(3) + 1.20(2.0) - 4.50(-0.80) = 1.80 + 1.95 + 2.40 + 3.60 = 9.75$, matching Exhibit 2.
> $e = 13.1 - 9.75 = 3.35$.
> A is wrong because it reverses the definition, $\hat{Y} - Y = -3.35$.
> C is wrong because it measures the deviation from the pilot mean, $13.1 - 1.8667 = 11.2333$, instead of from the fitted value.
> 3. **A.** The intercept is the expected value of the dependent variable when every independent variable equals zero (V1 p.4).
> With POL, GROWTH and CDS all zero, the expected excess return is 1.80%.
> B is wrong because the intercept is not the average return; the sample mean of ER in Exhibit 1 is 2.40, and the two coincide only if every X averages zero.
> C is wrong because it interprets the intercept as if it were the partial slope on POL, which is 0.65.
> 4. **C.** A plot of residuals against one independent variable is used to detect any remaining relation between the residuals and that variable; a systematic inverted U-shape means the straight-line term in GROWTH misses a curved relationship, so the model is misspecified and the linearity assumption is in doubt (V1 p.14, p.18).
> A is wrong because fat tails are diagnosed from the normal Q-Q plot, not from a residuals-versus-X pattern.
> B is wrong because the finding describes the sign of the residuals shifting with GROWTH, not the spread of the residuals widening or narrowing.
> 5. **B.** Every no in the regression process routes back to "adjust the model and re-estimate" (V1 pp.6-7).
> The first diagnostic finding, the inverted U in the residuals against GROWTH, means the assumption gate has not actually been passed, contrary to Ibarra-Kwan's claim.
> The final gate asks whether the model is the best of the candidate models, and an alternative that fits at least as well with fewer variables means that gate has not been passed either, so Voss is correct (V1 p.6).
> A is wrong because it relies on an assumption gate the misspecified model fails and skips the best-model gate.
> C is wrong because the assumptions have already been checked and a failed check calls for adjusting the model, not re-checking it; dropping POL, which is nearly uncorrelated with the other variables, does not address the curvature in GROWTH.
> 6. **B.** A significant pairwise correlation between independent variables signals an approximate linear relation, which threatens assumption 5b, independence of the independent variables; the model can still be estimated, but separating the effects of GROWTH and CDS is problematic (V1 p.10, p.17).
> A is wrong because a correlation of $-0.91$ is strong but not exact; only a perfect linear relation makes estimation impossible.
> C is wrong because independence of errors concerns correlation of residuals across observations; GROWTH and CDS are independent variables, not residuals.

## Distractor design

- Q1: A uses the residual sum of squares instead of the total (wrong formula variant); B divides by $n - 1$ and reports a variance.
- Q2: A is a sign error ($\hat{Y} - Y$ instead of $Y - \hat{Y}$); C measures from the mean instead of the fitted value.
- Q3: B confuses the intercept with the mean of Y (misread exhibit); C reads the intercept as a slope.
- Q4: A assigns the pattern to the Q-Q plot's assumption; B reads a shift in level as a change in spread.
- Q5: A trusts a failed assumption gate and skips the best-model gate; C re-checks the assumptions instead of adjusting the model.
- Q6: A confuses approximate with exact collinearity; C is the "independence" word trap.
