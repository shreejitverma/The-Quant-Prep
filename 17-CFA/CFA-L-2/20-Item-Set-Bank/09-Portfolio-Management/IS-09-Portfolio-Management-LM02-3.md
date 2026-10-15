---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 2
title: "Tamarind Capital: Three Strategies Under the Fundamental Law"
los: [los-09-02-c, los-09-02-e, los-09-02-f]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Tamarind Capital: Three Strategies Under the Fundamental Law

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tamarind Capital is a Singapore-based asset manager that runs three active strategies against the same broad Asia-Pacific equity benchmark.
Its head of research, Wen Jie Tan, CFA, is preparing a strategy review for Tamarind's product committee, which will decide where to allocate the firm's research budget for 2027.
Tan evaluates every strategy with the fundamental law of active management.

Strategy 1 is a tactical market timer that switches between the benchmark and a cash-plus-futures position.
Each month it makes a binary call on whether equities will outperform cash, and Tan's backtest shows each monthly call is independent of the previous one.
Over the past ten years the calls have been correct 54% of the time.
The strategy has no implementation constraints.

Strategy 2 rotates among the 11 sectors of the benchmark once a year, with independent annual forecasts, an information coefficient of 0.12, and no constraints.
Tan's risk model shows that the sector active returns share a common pairwise correlation of 0.10.

Strategy 3 selects among 150 stocks whose active returns are uncorrelated in the risk model.
It forecasts annually from a valuation score, has an information coefficient of 0.04, and is run long-only, which Tan estimates gives a transfer coefficient of 0.55.
It targets 4.0% active risk.
The strategy's 36-month realized tracking error is 4.3%, and its average holding count is 118.

Exhibit 1: Summary inputs

| | Strategy 1 | Strategy 2 | Strategy 3 |
|---|---|---|---|
| Decision unit | Monthly market call | Annual sector call | Annual stock call |
| Forecast accuracy or IC | 54% correct | IC 0.12 | IC 0.04 |
| Securities or sectors | 1 | 11 | 150 |
| Correlation of active returns | n/a | 0.10 | 0.00 |
| Transfer coefficient | 1.00 | 1.00 | 0.55 |
| Target active risk | 4.0% | 4.0% | 4.0% |

The Strategy 3 team submits three proposals to raise its information ratio.

Proposal A: Rebalance quarterly instead of annually, using the same valuation score, which changes little from quarter to quarter.

Proposal B: Convert the strategy to a 130/30 structure, which permits short positions.

Proposal C: Raise the active risk target from 4.0% to 6.0% while remaining long-only.

The Strategy 3 team's marketing draft also claims: "Because we will rebalance monthly, our breadth is $150 \times 12 = 1{,}800$, giving an information ratio of $0.55 \times 0.04 \times \sqrt{1{,}800} = 0.93$."

Tan lists three possible critiques of the marketing claim for the committee.

Critique 1: "The valuation score is slow moving, so monthly decisions are not independent and 1,800 overstates breadth."

Critique 2: "The fundamental law ignores portfolio constraints such as long-only rules, so the claimed IR is unreliable."

Critique 3: "The 0.04 information coefficient is an uncertain ex ante estimate that varies over time, and that uncertainty adds risk and lowers the IR likely to be realized."

Finally, a committee member asks how accurate Strategy 1 would need to be if it were limited to quarterly calls, still independent, to match Strategy 2's information ratio.

## Questions

1. Strategy 1's information coefficient and expected information ratio are closest to: (LOS: los-09-02-e)
   - A. IC 0.08 and IR 0.28.
   - B. IC 0.08 and IR 0.96.
   - C. IC 0.54 and IR 1.87.
2. Strategy 2's expected information ratio is closest to: (LOS: los-09-02-e)
   - A. 0.17.
   - B. 0.28.
   - C. 0.40.
3. Strategy 3's expected active return at its 4.0% target active risk is closest to: (LOS: los-09-02-c)
   - A. 0.59%.
   - B. 1.08%.
   - C. 1.96%.
4. Which proposal would most likely increase Strategy 3's information ratio? (LOS: los-09-02-e)
   - A. Proposal A.
   - B. Proposal B.
   - C. Proposal C.
5. Which of Tan's critiques of the marketing claim is least valid? (LOS: los-09-02-f)
   - A. Critique 1.
   - B. Critique 2.
   - C. Critique 3.
6. The accuracy Strategy 1 would need with independent quarterly calls to match Strategy 2's information ratio is closest to: (LOS: los-09-02-e)
   - A. 54.1%.
   - B. 57.0%.
   - C. 64.1%.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** $IC = 2(0.54) - 1 = 0.08$.
> Twelve independent monthly calls give $BR = 12$, so $IR = 0.08\sqrt{12} = 0.08 \times 3.4641 = 0.2771$.
> B is wrong because it multiplies by breadth instead of its square root: $0.08 \times 12 = 0.96$.
> C is wrong because it uses the hit rate as the IC: $0.54\sqrt{12} = 1.8706$.
> 2. **B.** Correlated sector bets shrink breadth: $BR = N/[1 + (N-1)\rho] = 11/[1 + 10(0.10)] = 11/2.0 = 5.50$.
> $IR = 0.12\sqrt{5.50} = 0.12 \times 2.3452 = 0.2814$.
> A is wrong because it takes the denominator of the breadth formula as breadth: $0.12\sqrt{2.0} = 0.1697$.
> C is wrong because it ignores the correlation and uses $BR = 11$: $0.12\sqrt{11} = 0.3980$.
> 3. **B.** $IR = TC \times IC \times \sqrt{BR} = 0.55 \times 0.04 \times \sqrt{150} = 0.55 \times 0.04 \times 12.2474 = 0.2694$.
> $E(R_A) = 0.2694 \times 4.0 = 1.0778\%$.
> A is wrong because it squares the transfer coefficient: $0.55^2 \times 0.04 \times 12.2474 \times 4.0 = 0.5928\%$.
> C is wrong because it omits the transfer coefficient: $0.04 \times 12.2474 \times 4.0 = 1.9596\%$.
> The 4.3% realized tracking error and the 118 average holdings are not inputs; the law uses the target active risk and the independent decisions per year.
> 4. **B.** Permitting short positions relaxes the binding long-only constraint, moving actual active weights closer to optimal weights, which raises TC and therefore $IR = TC \times IC \times \sqrt{BR}$.
> A is wrong because rebalancing more often adds breadth only when successive forecasts are independent; a slow-moving score repeats the same decision, so breadth barely rises while turnover costs increase.
> C is wrong because an unconstrained IR is invariant to aggressiveness, but in a long-only portfolio the constraints bind harder as active risk rises, so TC and the IR fall.
> 5. **B.** The transfer coefficient is the standard refinement that brings constraints into the law, and the claim already includes TC of 0.55, so "the law ignores constraints" is the weakest critique.
> A is wrong because Critique 1 is valid: time-series dependence of a persistent signal means 12 monthly decisions are not 12 independent bets.
> C is wrong because Critique 3 is valid: the ex ante IC is uncertain and tends to be overestimated, and strategy risk from IC uncertainty lowers realized IRs relative to naive law estimates.
> 6. **B.** Target IR from Question 2 is 0.2814, and quarterly independent calls give $BR = 4$.
> Required $IC = 0.2814/\sqrt{4} = 0.1407$, so accuracy $= (1 + IC)/2 = 1.1407/2 = 57.04\%$.
> A is wrong because it keeps monthly breadth: $IC = 0.2814/\sqrt{12} = 0.0812$, accuracy $= 54.06\%$.
> C is wrong because it inverts $IC = 2p - 1$ as $p = IC + 0.5 = 0.1407 + 0.5 = 64.07\%$.

## Distractor design

1. B: breadth used without the square root; C: hit rate used as the information coefficient.
2. A: breadth-formula denominator mistaken for breadth; C: correlation adjustment ignored (BR = N).
3. A: transfer coefficient squared; C: transfer coefficient omitted.
4. A: rebalancing frequency assumed to add breadth despite a persistent signal; C: unconstrained aggressiveness invariance applied to a constrained portfolio.
5. A and C: valid limitations (time-series dependence, IC uncertainty) mistaken for the weak one.
6. A: breadth left at the monthly count; C: IC-to-accuracy formula inverted without halving.
