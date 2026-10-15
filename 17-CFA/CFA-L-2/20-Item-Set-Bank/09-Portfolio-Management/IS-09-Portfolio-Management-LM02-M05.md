---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 2
title: "Tidemark Reinsurance: Rebuilding the Active Equity Line-Up"
los: [los-09-02-c, los-09-02-d, los-09-02-e, los-09-02-f]
difficulty: 4
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Tidemark Reinsurance: Rebuilding the Active Equity Line-Up

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Oluwaseun Adeyemi, CFA, is a senior analyst in the investment office of Tidemark Reinsurance.
Tidemark's surplus portfolio holds a global developed-market equity allocation, currently a single index fund that replicates the benchmark.
Beatriz Montalvo, the chief investment officer, has asked Adeyemi to choose one external active manager for the allocation and to evaluate an in-house systematic sleeve.
Tidemark may hold the index fund long or short through futures.

The benchmark's expected return is 8.46%, its volatility is 15.5%, and the risk-free rate is 3.50%, giving a benchmark Sharpe ratio of 0.32.
Adeyemi assumes that every manager's active returns are uncorrelated with benchmark returns and that every portfolio has a benchmark beta of 1.

Exhibit 1: Candidate managers

| | Cobalt Ridge | Larchmont Sector | Pinecrest Quant |
|---|---|---|---|
| Strategy | Long-short country pairs | Industry rotation | Stock selection |
| Number of positions | 12 pairs | 20 industries | 500 stocks |
| Average pairwise correlation of active returns | -0.06 | 0.20 | 0.00 |
| Forecast and rebalancing cycle | Annual | Quarterly | Monthly |
| Information coefficient | 0.06 | 0.08 | 0.015 |
| Transfer coefficient | 0.85 | 0.75 | 0.65 |
| Delivered active risk | 5.0% | 6.5% | 3.5% |
| Realized 3-year information ratio | 0.21 | 0.38 | 0.12 |

Adeyemi's due diligence adds three facts.
Larchmont's quarterly forecasts come from a fresh industry survey each quarter, and successive quarterly forecasts are uncorrelated.
Pinecrest's pitch book reports breadth of $500 \times 12 = 6{,}000$, but its composite valuation score changes very little from month to month, and Adeyemi estimates that each stock's score has a month-to-month correlation above 0.95.
Cobalt Ridge's pairs are built so that the active returns of different pairs are mildly negatively correlated.

Montalvo notes on 2 June 2026 that, to keep the mandate simple, Tidemark may initially hold the chosen manager on its own, at its delivered active risk, with no position in the index fund.

Montalvo adds that Tidemark's board is considering new country position caps for any external mandate.
Cobalt Ridge estimates that, under those caps, its transfer coefficient would fall from 0.85 to 0.55, with no change to its information coefficient or breadth.

The in-house sleeve is an unconstrained long-short strategy, so Adeyemi treats its transfer coefficient as 1.00.
It selects among 225 stocks with uncorrelated active returns and annual independent forecasts.
Its expected information coefficient is 0.04, and the standard deviation of its realized annual information coefficient over the past 15 years is 0.10.
Tidemark's risk model predicts an active risk of 2.0% for the sleeve.
The sleeve's realized information coefficient last year was 0.07.

Adeyemi plans to report the sleeve using the strategy-risk refinement of Qian and Hua, because the naive fundamental law ignores uncertainty about the information coefficient.
Montalvo remarks that the committee has seen naive fundamental-law estimates overstate realized information ratios before, and she wants a figure that allows for that.

## Questions

1. Based on Exhibit 1 and the due diligence findings, the manager with the highest expected information ratio is: (LOS: los-09-02-e)
   - A. Cobalt Ridge.
   - B. Larchmont Sector.
   - C. Pinecrest Quant.
2. If Tidemark holds the manager selected in Question 1 on its own, at its delivered active risk, the expected Sharpe ratio of the equity allocation is closest to: (LOS: los-09-02-d)
   - A. 0.316.
   - B. 0.398.
   - C. 0.441.
3. If the board adopts the position caps, the maximum Sharpe ratio Tidemark can achieve by optimally combining Cobalt Ridge with the index fund is closest to: (LOS: los-09-02-c)
   - A. 0.361.
   - B. 0.375.
   - C. 0.415.
4. After allowing for strategy risk, the in-house sleeve's expected active risk and expected information ratio are closest to: (LOS: los-09-02-f)
   - A. 2.0% and 0.60.
   - B. 3.0% and 0.60.
   - C. 3.0% and 0.40.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Apply $IR = TC \times IC \times \sqrt{BR}$, with breadth adjusted for correlation, $BR = N/[1 + (N-1)\rho]$, and for truly independent decisions over time.
> Cobalt Ridge: $BR = 12/[1 + 11(-0.06)] = 12/0.34 = 35.2941$, so $IR = 0.85 \times 0.06 \times 5.9409 = 0.3030$.
> Larchmont: per quarter $BR = 20/[1 + 19(0.20)] = 20/4.80 = 4.1667$; four independent quarters give $BR = 16.6667$, so $IR = 0.75 \times 0.08 \times 4.0825 = 0.2449$.
> Pinecrest: the persistent score means monthly rebalancing does not add independent decisions, so $BR = 500$ and $IR = 0.65 \times 0.015 \times 22.3607 = 0.2180$.
> B is wrong because it ignores the correlation adjustments: Larchmont at $BR = 80$ gives $0.75 \times 0.08 \times 8.9443 = 0.5367$, while Cobalt at $BR = 12$ falls to $0.1767$.
> C is wrong because it accepts the pitch-book breadth of 6,000: $0.65 \times 0.015 \times 77.4597 = 0.7552$.
> The realized 3-year IRs are ex post and do not measure expected skill; ranking by them would also point to Larchmont.
> 2. **B.** Expected active return $= IR \times \sigma_A = 0.3030 \times 5.0 = 1.5149\%$, and expected benchmark excess return $= 0.32 \times 15.5 = 4.9600\%$.
> Expected excess return of the allocation $= 4.9600 + 1.5149 = 6.4749\%$.
> Total risk $= \sqrt{15.5^2 + 5.0^2} = 16.2865\%$, because benchmark and active returns are uncorrelated.
> Sharpe ratio $= 6.4749/16.2865 = 0.3976$.
> This is below the maximum because 5.0% is far below the optimal active risk of $(0.3030/0.32) \times 15.5 = 14.68\%$.
> A is wrong because it adds benchmark risk and active risk in levels: $6.4749/(15.5 + 5.0) = 0.3159$.
> C is wrong because it assumes the delivered active risk is optimal and reports $\sqrt{0.32^2 + 0.3030^2} = 0.4407$.
> 3. **B.** The unconstrained IR is $IR^{*} = IC\sqrt{BR} = 0.06 \times 5.9409 = 0.3565$.
> Under the caps, $IR = 0.55 \times 0.3565 = 0.1960$, and $SR_P = \sqrt{SR_B^2 + TC^2 (IR^{*})^2} = \sqrt{0.32^2 + 0.1960^2} = 0.3753$.
> A is wrong because it applies the new TC to the already constrained IR: $0.55 \times 0.3030 = 0.1666$, and $\sqrt{0.32^2 + 0.1666^2} = 0.3608$.
> C is wrong because it does not square TC: $\sqrt{0.32^2 + 0.55 \times 0.3565^2} = 0.4151$.
> 4. **C.** Strategy risk: $\sigma_A = \sigma_{IC}\sqrt{N}\,\sigma_{RM} = 0.10 \times \sqrt{225} \times 2.0 = 0.10 \times 15 \times 2.0 = 3.0\%$.
> Expected active return $= (IC/\sigma_{IC})\,\sigma_A = (0.04/0.10) \times 3.0 = 1.20\%$, so the IR is $1.20/3.0 = 0.40$.
> The naive law gives $IR = 0.04\sqrt{225} = 0.60$, so the adjusted IR is $0.40/0.60 = 66.67\%$ of the naive figure, inside the 45% to 91% range the curriculum cites.
> The expected active return is the same 1.20% as the naive law at 2.0%; strategy risk raises the risk, not the return.
> A is wrong because it ignores strategy risk and uses the risk-model active risk with the naive IR.
> B is wrong because it raises active risk to 3.0% but applies the naive law at that risk, $0.60 \times 3.0 = 1.80\%$, which scales the return up with the risk.
> Last year's realized IC of 0.07 is a single observation, not the expected IC.

## Distractor design

1. B: correlation adjustment to breadth ignored; C: naive time-series breadth accepted for a persistent signal.
2. A: benchmark and active risk added in levels instead of variances; C: delivered active risk assumed optimal, maximum Sharpe ratio reported.
3. A: new transfer coefficient applied to the already constrained IR (TC counted twice); C: transfer coefficient not squared in the constrained Sharpe relation.
4. A: strategy risk ignored (risk-model active risk and naive IR); B: naive IR applied at the strategy-risk active risk.
