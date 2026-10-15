---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 2
title: "Kaimana Sovereign Fund: Compliance Review of an Equity Mandate"
los: [los-09-02-c, los-09-02-f]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Kaimana Sovereign Fund: Compliance Review of an Equity Mandate

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

The Kaimana Sovereign Fund outsources part of its developed-market equity allocation to Halvorsen Asset Management under a long-only mandate with sector and position limits.
After a disappointing 2025, Kaimana's head of manager oversight, Leilani Akana, CFA, asks her compliance analyst, Daniel Reyes, to review the mandate and Halvorsen's new marketing materials.

Reyes first checks how faithfully Halvorsen converts forecasts into positions.
He takes a five-stock sample from the portfolio at the start of 2025, together with Halvorsen's forecasts of annual active return, the forecast active risk of each stock, the active weights actually held, and the realized active returns for the year.
He assumes the stocks' active returns are uncorrelated.

Exhibit 1: Five-stock sample, start of 2025

| Stock | Forecast active return $\mu_i$ | Active risk $\sigma_i$ | Actual active weight $\Delta w_i$ | Realized active return |
|---|---|---|---|---|
| 1 | 2.0% | 20% | +4% | 3.1% |
| 2 | 3.0% | 30% | +3% | -0.8% |
| 3 | -1.5% | 25% | -2% | -2.2% |
| 4 | -4.0% | 40% | -1% | 1.5% |
| 5 | 1.0% | 35% | -4% | 0.4% |

Halvorsen's risk report gives the parameters for the whole portfolio in Exhibit 2.

Exhibit 2: Halvorsen portfolio statistics, 2025

| Parameter | Value |
|---|---|
| Transfer coefficient (whole portfolio) | 0.55 |
| Ex ante information coefficient | 0.06 |
| Breadth (independent annual decisions) | 81 |
| Active risk | 4.5% |
| Realized information coefficient, 2025 | 0.02 |
| Realized active return, 2025 (gross of fees) | -1.10% |
| Management fee | 0.45% |

In its 2025 letter to clients, Halvorsen wrote: "Our forecasts were right more often than wrong in 2025; the shortfall reflects bad luck from the mandate's constraints, not a failure of skill."

Halvorsen's new marketing deck, dated 20 February 2026, proposes moving the mandate to monthly rebalancing.
It states: "With 81 decisions a month, breadth rises to $81 \times 12 = 972$, and our expected information ratio becomes $0.55 \times 0.06 \times \sqrt{972} = 1.03$."
The deck notes that Halvorsen's forecasts come from a quality and valuation score that is updated monthly but changes slowly.

Reyes drafts two statements for Akana.

Statement 1: "The deck overstates breadth: because the score changes slowly, successive monthly decisions are not independent, so multiplying 81 by 12 overstates the number of independent decisions."

Statement 2: "The main weakness of the fundamental law as applied in the deck is that it ignores the mandate's long-only and sector constraints."

Akana asks Reyes to quantify three items before the review meeting: the transfer coefficient implied by the five-stock sample, the part of 2025 active return not explained by the realized information coefficient, and the share of Halvorsen's period-to-period performance variance that should be expected to come from constraint-induced noise.
She reminds him that both the information coefficient and the transfer coefficient are risk-weighted correlations, and that the 2025 shortfall should be judged against the value added implied by the realized information coefficient rather than against the ex ante forecast.

## Questions

1. The transfer coefficient implied by the five-stock sample in Exhibit 1 is closest to: (LOS: los-09-02-c)
   - A. 0.52.
   - B. 0.59.
   - C. 0.69.
2. The constraint-induced noise component of Halvorsen's 2025 active return is closest to: (LOS: los-09-02-c)
   - A. -2.44%.
   - B. -1.91%.
   - C. -1.55%.
3. The proportion of the variance of Halvorsen's realized active return that is attributable to constraint-induced noise is closest to: (LOS: los-09-02-c)
   - A. 30%.
   - B. 45%.
   - C. 70%.
4. Which of Reyes's statements is correct? (LOS: los-09-02-f)
   - A. Only Statement 1.
   - B. Only Statement 2.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** TC is the correlation between risk-weighted forecasts $\mu_i/\sigma_i$ and risk-weighted active weights $\Delta w_i \sigma_i$.
> Risk-weighted forecasts: $2.0/20 = 0.1000$, $3.0/30 = 0.1000$, $-1.5/25 = -0.0600$, $-4.0/40 = -0.1000$, $1.0/35 = 0.0286$.
> Risk-weighted weights: $4 \times 20 = 80$, $3 \times 30 = 90$, $-2 \times 25 = -50$, $-1 \times 40 = -40$, $-4 \times 35 = -140$.
> Correlation of the two series $= 0.5879$.
> A is wrong because it correlates the raw forecasts with the raw active weights, ignoring the risk adjustment: $0.5197$.
> C is wrong because it divides the weights by $\sigma_i$ as well, applying the risk adjustment in the same direction to both series: $0.6862$.
> The realized active return column is not used; correlating it with forecasts would estimate the IC, not the TC.
> 2. **C.** Value added conditional on the realized IC: $E(R_A \mid IC_R) = TC \times IC_R \times \sqrt{BR} \times \sigma_A = 0.55 \times 0.02 \times 9 \times 4.5 = 0.4455\%$.
> Noise $= R_A - E(R_A \mid IC_R) = -1.10 - 0.4455 = -1.5455\%$.
> The positive realized IC means forecasts were modestly right, so constraint-induced noise explains most of the shortfall, consistent with Halvorsen's letter.
> A is wrong because it subtracts the ex ante expectation, $0.55 \times 0.06 \times 9 \times 4.5 = 1.3365\%$, giving $-1.10 - 1.3365 = -2.4365\%$.
> B is wrong because it omits TC from the conditional expectation, $0.02 \times 9 \times 4.5 = 0.81\%$, giving $-1.10 - 0.81 = -1.91\%$.
> 3. **C.** Only $TC^2 = 0.55^2 = 0.3025$ of performance variance comes from variation in the realized IC, so the noise share is $1 - 0.3025 = 0.6975$, about 70%.
> A is wrong because it reports the forecasting-skill share $TC^2$ instead of the noise share.
> B is wrong because it uses $1 - TC = 0.45$ instead of $1 - TC^2$.
> 4. **A.** Statement 1 is correct: breadth counts independent decisions, and a slowly changing score produces time-series dependence, so the naive product 972 (and the 1.03 IR) overstates breadth and the achievable IR.
> Statement 2 is incorrect: the deck's calculation already includes the transfer coefficient of 0.55, which is how the fundamental law incorporates constraints; "ignoring constraints" is the weakest criticism of the law.
> B is wrong because it accepts the constraint critique, which TC already addresses.
> C is wrong because only the breadth critique is valid.

## Distractor design

1. A: risk adjustment omitted (raw forecasts against raw weights); C: risk adjustment applied in the same direction to forecasts and weights.
2. A: ex ante IC used in place of the realized IC; B: transfer coefficient omitted from the conditional expectation.
3. A: skill share $TC^2$ reported as the noise share; B: $1 - TC$ used instead of $1 - TC^2$.
4. B and C: constraints named as an ignored limitation even though the transfer coefficient already models them.
