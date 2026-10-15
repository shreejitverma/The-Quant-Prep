---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 4
title: "Thornbury Family Office: Macro and Fundamental Model Review"
los: [los-09-04-c, los-09-04-d, los-09-04-e]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Thornbury Family Office: Macro and Fundamental Model Review

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

The Thornbury Family Office manages the liquid assets of three generations of the Thornbury family.
Leena Vasquez, CFA, is preparing the annual performance report for a $6.0 million equity sleeve that holds two stocks: $3.6 million in Harlow Industrial and $2.4 million in Pemberton Utilities.
The office subscribes to a three-factor macroeconomic model whose factors are surprises in real GDP growth, inflation, and the change in the investment-grade credit spread.
Exhibit 1 shows the model parameters and the asset-specific returns for the year.

**Exhibit 1: Macroeconomic factor model parameters**

| Stock | Intercept | GDP | Inflation | Credit spread | Asset-specific return | CAPM beta |
|---|---|---|---|---|---|---|
| Harlow Industrial | 8.40% | 1.60 | -0.50 | -1.20 | +1.00% | 1.25 |
| Pemberton Utilities | 6.00% | 0.40 | 0.80 | -0.30 | -0.50% | 0.55 |
| Coniston Retail | not shown | 2.00 | -1.00 | -0.80 | -1.50% | 1.40 |

**Exhibit 2: Macroeconomic data for the year**

| Variable | Consensus forecast at start of year | Actual |
|---|---|---|
| Real GDP growth | 2.40% | 1.60% |
| Inflation | 2.10% | 2.90% |
| Change in credit spread | 0.10% | 0.35% |

Coniston Retail is a stock the family is considering.
The vendor's report omits Coniston's intercept, but Vasquez knows that Coniston returned 4.20% over the year and that its asset-specific return is shown in Exhibit 1.

The vendor also offers a fundamental factor model.
For its financial leverage factor, the vendor standardizes each company's debt-to-equity ratio across a 1,200-stock universe.
Harlow's debt-to-equity ratio is 1.45.
The universe has a mean debt-to-equity ratio of 0.85, a median of 0.78, and a standard deviation of 0.40.

During a call, the vendor's representative, Duncan Pryce, makes two statements.

Statement 1: "In the macroeconomic model, we build the surprise series first and then estimate each stock's sensitivities by time-series regression. In the fundamental model, we specify the sensitivities first as standardized attributes and then estimate the factor returns by cross-sectional regression."

Statement 2: "Because both models are linear, the intercept in the fundamental model can be read as the stock's expected return, exactly as in the macroeconomic model."

Pryce also describes the vendor's third product, a statistical factor model, and Vasquez records several possible descriptions of it in her notes.

The family's patriarch, Edmund Thornbury, has recently hired an outside manager who describes herself as a growth-at-a-reasonable-price stock picker.
Vasquez must recommend which of the vendor's three model types would give the most direct evidence of that manager's style orientation, for example value versus growth and small versus large capitalization.

Vasquez treats portfolio parameters as market-value-weighted averages of the stocks' parameters and assumes that the consensus forecasts were fully reflected in prices at the start of the year.

## Questions

1. The realized return on the two-stock equity sleeve for the year is closest to: (LOS: los-09-04-c)
   - A. 6.35%.
   - B. 6.75%.
   - C. 9.40%.
2. The expected return on Coniston Retail implied by the macroeconomic model is closest to: (LOS: los-09-04-c)
   - A. 5.30%.
   - B. 6.80%.
   - C. 8.30%.
3. Harlow Industrial's sensitivity to the financial leverage factor in the fundamental model is closest to: (LOS: los-09-04-d)
   - A. 0.60.
   - B. 1.50.
   - C. 3.75.
4. Regarding Pryce's statements, which is correct? (LOS: los-09-04-d)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both statements.
5. Which description of the vendor's statistical factor model is most accurate? (LOS: los-09-04-d)
   - A. Its factors are portfolios of the securities studied; it makes minimal assumptions, but its factors are often hard to interpret economically.
   - B. In its principal components version the factors best explain historical return covariances, and in its factor analysis version they best explain historical return variances.
   - C. Its minimal assumptions make its factors easier to interpret than the factors of a macroeconomic model.
6. The model type Vasquez should recommend to assess the new manager's style orientation is: (LOS: los-09-04-e)
   - A. the macroeconomic model, because its factors capture the economy-wide surprises that drive growth stocks.
   - B. the fundamental model, because its factors are attributes such as book-to-price, earnings growth, and market capitalization that define style.
   - C. the statistical model, because its extracted factors replicate the manager's historical return variance most closely.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Surprises are actual minus forecast: GDP $1.60 - 2.40 = -0.80\%$, inflation $2.90 - 2.10 = +0.80\%$, credit spread $0.35 - 0.10 = +0.25\%$.
> Weights are $3.6/6.0 = 0.60$ and $2.4/6.0 = 0.40$.
> Portfolio intercept $= 0.6(8.40) + 0.4(6.00) = 7.4400\%$; GDP sensitivity $= 0.6(1.60) + 0.4(0.40) = 1.1200$; inflation sensitivity $= 0.6(-0.50) + 0.4(0.80) = 0.0200$; credit spread sensitivity $= 0.6(-1.20) + 0.4(-0.30) = -0.8400$; asset-specific return $= 0.6(1.00) + 0.4(-0.50) = 0.4000\%$.
> $R_P = 7.4400 + 1.1200(-0.80) + 0.0200(0.80) - 0.8400(0.25) + 0.4000 = 7.4400 - 0.8960 + 0.0160 - 0.2100 + 0.4000 = 6.7500\%$.
> A is wrong because it omits the asset-specific returns: $7.4400 - 1.0900 = 6.3500\%$.
> C is wrong because it uses the actual values instead of the surprises: $7.4400 + 1.1200(1.60) + 0.0200(2.90) - 0.8400(0.35) + 0.4000 = 9.3960\%$.
> 2. **C.** In a macroeconomic model the intercept is the expected return, so solve $4.20 = E(R) + \sum b_k F_k + \varepsilon$.
> Factor effect $= 2.00(-0.80) - 1.00(0.80) - 0.80(0.25) = -1.60 - 0.80 - 0.20 = -2.60\%$.
> $E(R) = 4.20 - (-2.60) - (-1.50) = 8.30\%$.
> A is wrong because it adds the asset-specific return with the wrong sign: $4.20 + 2.60 - 1.50 = 5.30\%$.
> B is wrong because it ignores the asset-specific return: $4.20 + 2.60 = 6.80\%$.
> 3. **B.** Standardized beta $= (1.45 - 0.85)/0.40 = 0.60/0.40 = 1.50$, so Harlow's leverage is 1.5 standard deviations above the universe mean.
> A is wrong because it stops at the raw difference from the mean and never scales by the standard deviation.
> C is wrong because it divides by the variance, $0.40^2 = 0.16$, instead of the standard deviation: $0.60/0.16 = 3.75$.
> The median of 0.78 is a decoy; the formula uses the mean.
> 4. **A.** Statement 1 correctly describes the order of estimation: macroeconomic models estimate sensitivities last, after building surprise series, while fundamental models specify standardized sensitivities first and estimate factor returns last.
> Statement 2 is wrong because with standardized sensitivities the fundamental model's intercept has no economic interpretation; only in the macroeconomic model, where factors are zero-mean surprises, is the intercept the expected return.
> B is wrong because it accepts the false intercept claim and rejects the correct estimation order.
> C is wrong because it accepts Statement 2.
> 5. **A.** Statistical factor models extract factors from historical returns, the factors are portfolios defined by weights on the securities studied, and the models make minimal assumptions at the cost of hard economic interpretation.
> B is wrong because it swaps the two versions: factor analysis factors best reproduce historical covariances and principal components factors best reproduce historical variances.
> C is wrong because it is the half-true claim: minimal assumptions are the advantage, but interpretation is the weakness.
> 6. **B.** Style orientation is defined by company and share attributes such as valuation multiples, earnings growth, and size, which are exactly the factors of a fundamental model, so the manager's standardized exposures read directly as a style profile.
> A is wrong because a macroeconomic model can shed only indirect light on style; its factors are economy-wide surprises, not security characteristics.
> C is wrong because statistical factors usually lack economic labels, so fitting return variance says little about value versus growth.

## Distractor design

- Q1: A = asset-specific returns omitted; C = actual factor values used instead of surprises.
- Q2: A = sign error on the asset-specific return; B = asset-specific return ignored.
- Q3: A = not scaled by the standard deviation; C = divided by the variance (and the median is a misread-exhibit decoy).
- Q4: B and C = macroeconomic intercept interpretation carried into the fundamental model.
- Q5: B = factor analysis and principal components swapped; C = half-true statement that fails on interpretation.
- Q6: A = macro factors mistaken for style factors; C = statistical fit mistaken for economic interpretation.
