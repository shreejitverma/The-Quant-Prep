---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 4
title: "Pell River Retirement System: Enhanced Index Risk Budget"
los: [los-09-04-d, los-09-04-e, los-09-04-g]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Pell River Retirement System: Enhanced Index Risk Budget

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

The Pell River Municipal Employees' Retirement System allocates part of its US large-cap equity portfolio to an enhanced index mandate managed by Corvina Asset Management.
The mandate's guidelines require Corvina to keep annual tracking risk at or below 2.00% and to deliver an information ratio of at least 0.35, both measured over the trailing three years.
Nadia Ferreira, CFA, a senior investment officer at the system, is preparing Corvina's mandate review.
Oliver Stroud, a consultant retained by the board, assists her.

Ferreira uses the system's fundamental factor model, which has four standardized style factors and industry factors.
Corvina's industry weights match the benchmark's, so its industry exposures are omitted.
The model vendor states that covariances among the style factor returns are negligible, and it reports Corvina's active specific risk as 1.17 (% squared).
Sensitivities are measured at the start of the review period.

**Exhibit 1: Style factor sensitivities and factor return volatility**

| Factor | Corvina sensitivity | Benchmark sensitivity | Annual standard deviation of factor return |
|---|---|---|---|
| Value (book-to-price) | 0.30 | 0.10 | 3.0% |
| Size (log market capitalization) | 0.45 | 0.60 | 4.0% |
| Momentum (12-month price change) | 0.12 | 0.00 | 5.0% |
| Quality (return on equity) | 0.20 | 0.20 | 2.5% |

**Exhibit 2: Trailing three-year performance, annualized**

| Statistic | Corvina | Benchmark |
|---|---|---|
| Mean return | 11.40% | 10.80% |
| Standard deviation of return | 15.8% | 15.2% |

Ferreira computes Corvina's active factor risk directly from the active exposures and the factor variances, adds the vendor's active specific risk to obtain active risk squared, and then evaluates the manager against both guideline limits.

Stroud reviews Ferreira's draft and makes two comments.

Stroud (2 June): "Corvina's quality sensitivity of 0.20 is its second-largest exposure in Exhibit 1, so the quality factor must be one of the more important sources of its active risk. By contrast, its momentum sensitivity is the smallest of its tilts, so momentum can contribute very little."

Stroud (2 June, continued): "I ran a five-factor macroeconomic model and our fundamental model, which includes about 60 industry dummy variables, on the same large-cap universe last year. The fundamental model explained 41% of the variance of monthly stock returns against 13% for the macroeconomic model. The fundamental model is therefore superior in every respect, and the system has no use for a macroeconomic model."

Ferreira intends to present a breakdown of Corvina's active risk that shows how much comes from security selection and how much comes from each style tilt, because the board has asked whether an enhanced index manager should be taking style bets at all.
She also plans to respond to Stroud's model comparison before the board meets, because the system's liability-driven overlay program already uses a macroeconomic model to measure its exposure to inflation and interest rate surprises.

## Questions

1. Corvina's active factor risk is closest to: (LOS: los-09-04-g)
   - A. 0.28 (% squared).
   - B. 1.08 (% squared).
   - C. 4.66 (% squared).
2. Corvina's tracking risk and information ratio, and its compliance with the mandate guidelines, are best described as: (LOS: los-09-04-g)
   - A. 1.50% and 0.40; both guidelines are met.
   - B. 2.25% and 0.27; neither guideline is met.
   - C. 0.60% and 1.00; both guidelines are met.
3. Based on Ferreira's decomposition, which statement about the sources of Corvina's active risk is most accurate? (LOS: los-09-04-e)
   - A. Momentum contributes the least active factor risk, because Corvina's momentum active exposure is the smallest of its three style tilts.
   - B. The quality factor contributes to active risk, because Corvina's quality sensitivity of 0.20 is not zero.
   - C. Active specific risk is 52% of active risk squared, and the value, size, and momentum tilts each account for 16%.
4. The most appropriate response to Stroud's model comparison is that: (LOS: los-09-04-d)
   - A. part of the fundamental model's explanatory advantage is built into the comparison, because its industry factors together replicate the market, while the macroeconomic model is more parsimonious and maps directly to economic views such as inflation surprises.
   - B. Stroud is correct, because the proportion of return variance explained is the single criterion for choosing a factor model.
   - C. Stroud's figures are probably reversed, because macroeconomic models, whose factors are zero-mean surprises, typically explain more return variance than fundamental models.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Active exposures are Corvina's sensitivities minus the benchmark's: value $0.30 - 0.10 = 0.20$, size $0.45 - 0.60 = -0.15$, momentum $0.12 - 0.00 = 0.12$, quality $0.20 - 0.20 = 0.00$.
> With negligible factor covariances, active factor risk $= \sum (b_k^a)^2 \sigma^2(F_k)$.
> Value $0.20^2 \times 3.0^2 = 0.3600$; size $(-0.15)^2 \times 4.0^2 = 0.3600$; momentum $0.12^2 \times 5.0^2 = 0.3600$; quality $0.00^2 \times 2.5^2 = 0.0000$.
> Active factor risk $= 1.0800$ (% squared).
> A is wrong because it multiplies squared active exposures by factor standard deviations instead of variances: $0.04 \times 3.0 + 0.0225 \times 4.0 + 0.0144 \times 5.0 = 0.2820$.
> C is wrong because it uses Corvina's own sensitivities instead of active exposures: $0.09 \times 9 + 0.2025 \times 16 + 0.0144 \times 25 + 0.04 \times 6.25 = 4.6600$.
> 2. **A.** Active risk squared $= 1.0800 + 1.1700 = 2.2500$, so tracking risk $= \sqrt{2.2500} = 1.5000\%$.
> Mean active return $= 11.40 - 10.80 = 0.6000\%$, so $IR = 0.60/1.50 = 0.4000$.
> Tracking risk of 1.50% is within the 2.00% limit and the IR of 0.40 exceeds the 0.35 floor, so both guidelines are met.
> B is wrong because it reports active risk squared as tracking risk and divides by it: $0.60/2.25 = 0.2667$.
> C is wrong because it takes the difference in total return volatilities, $15.8 - 15.2 = 0.60\%$, as tracking risk; tracking risk is the standard deviation of the active return series, not the difference in standard deviations, which gives the spurious $IR = 0.60/0.60 = 1.0000$.
> 3. **C.** Active specific risk is $1.17/2.25 = 52.00\%$ of active risk squared, and active factor risk is $1.08/2.25 = 48.00\%$.
> Each of the three style tilts contributes $0.36/2.25 = 16.00\%$, so the manager's active risk is split about evenly between security selection and style bets, with no single tilt dominating.
> A is wrong because contribution depends on the squared active exposure times the factor variance; momentum's small exposure is offset by the highest factor volatility, so it contributes the same 0.36 as value and size.
> B is wrong because active risk comes from active exposures; Corvina's quality sensitivity equals the benchmark's, so its active quality exposure and contribution are zero.
> 4. **A.** Fundamental models, with many industry and style variables, often explain more return variance than macroeconomic models, but the gap overstates their superiority.
> The industry dummy variables together sum to the market, while the macroeconomic model contains no market factor, so part of the advantage is built into the comparison.
> Macroeconomic models are parsimonious and let the user express and measure exposures to economic views directly, which is what the system's overlay program needs, while fundamental models give a detailed, security-characteristic picture of risk; the model types serve different uses.
> B is wrong because variance explained ignores parsimony, interpretability, and the purpose of the analysis.
> C is wrong because it reverses the typical empirical finding; zero-mean surprise factors say nothing about how much variance a model explains.

## Distractor design

1. A: factor standard deviations used instead of factor variances; C: portfolio sensitivities used instead of active (portfolio minus benchmark) exposures.
2. B: active risk squared reported as tracking risk (square root omitted); C: difference in total volatilities used as tracking risk (misread exhibit decoy).
3. A: small active exposure assumed to mean small risk contribution, ignoring factor variance; B: zero portfolio-minus-benchmark exposure confused with a non-zero portfolio sensitivity.
4. B: variance explained treated as the only model criterion; C: empirical ranking reversed and zero-mean surprise property misapplied.
