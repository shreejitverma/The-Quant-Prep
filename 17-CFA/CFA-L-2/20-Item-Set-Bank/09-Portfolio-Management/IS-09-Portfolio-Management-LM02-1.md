---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 2
title: "Harwell University Endowment: Annual Attribution Report"
los: [los-09-02-a, los-09-02-b]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Harwell University Endowment: Annual Attribution Report

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Priya Anand, CFA, is the senior investment analyst at the Harwell University Endowment, a USD 3.2 billion perpetual fund.
She is preparing the annual performance report for the endowment's investment committee for calendar year 2025.
The endowment's policy portfolio sets long-term weights for four asset classes, and the chief investment officer tilts the actual weights away from policy each year.
Each asset class is run by an external active manager and is measured against its own asset-class benchmark.

Exhibit 1: Harwell Endowment, 2025 weights and returns

| Asset class | Policy weight | Actual weight | Sub-portfolio return | Benchmark return |
|---|---|---|---|---|
| Domestic equity | 45% | 50% | 14.2% | 12.8% |
| International equity | 20% | 15% | 6.1% | 7.4% |
| Fixed income | 25% | 22% | 3.9% | 3.2% |
| Real assets | 10% | 13% | -1.5% | -2.8% |

The endowment's total return for 2025 was 8.678%, and the policy portfolio returned 7.760%.
The risk-free rate averaged 4.0% during the year.
Anand estimates the annualized volatility of the endowment's total return at 10.4%.

The domestic equity manager, Crestline Partners, reports its 2025 return against the benchmark as "alpha of 1.40%."
Anand's risk system estimates the beta of the Crestline portfolio relative to its benchmark at 1.15.
The domestic equity manager has held an average of 212 stocks, and the benchmark contains 1,008.

For the whole endowment, Anand also computes ex post statistics from 60 monthly observations of the difference between the endowment's return and the policy portfolio's return.
The mean monthly active return is 0.085%, and the standard deviation of the monthly active returns is 0.49%.

Two committee members comment on the draft report at the 14 January 2026 meeting.

Martin Ogilvie, the committee chair, says: "Our Sharpe ratio is 0.45.
If we move 25% of the endowment into Treasury bills to reduce volatility ahead of the capital campaign, the Sharpe ratio of the total fund will be unaffected."

Helen Tsai, a committee member, responds with two statements.

Statement 1: "Moving 25% into Treasury bills would also leave the endowment's information ratio against the policy portfolio unchanged, because Treasury bills carry no risk."

Statement 2: "If instead we asked each external manager to double every active weight, with no position limits binding, each manager's information ratio would be unchanged, although active risk would double."

Anand asks her junior analyst to prepare the attribution split, the beta-adjusted return for Crestline, and an annualized information ratio before the report is finalized.
She reminds him that the attribution convention assigns any interaction effect to security selection, and that monthly statistics are annualized by multiplying the mean by 12 and the standard deviation by the square root of 12.

## Questions

1. The value added by Harwell's asset allocation decisions in 2025 is closest to: (LOS: los-09-02-a)
   - A. 0.09%.
   - B. 0.24%.
   - C. 0.92%.
2. The value added by security selection within the asset classes in 2025 is closest to: (LOS: los-09-02-a)
   - A. 0.68%.
   - B. 0.83%.
   - C. 0.92%.
3. The beta-adjusted alpha of the Crestline domestic equity portfolio in 2025 is closest to: (LOS: los-09-02-a)
   - A. -0.52%.
   - B. 1.40%.
   - C. 3.07%.
4. The annualized ex post information ratio of the endowment against its policy portfolio is closest to: (LOS: los-09-02-b)
   - A. 0.17.
   - B. 0.60.
   - C. 2.08.
5. If 25% of the endowment is moved into Treasury bills, as Ogilvie describes, the Sharpe ratio of the combined fund is closest to: (LOS: los-09-02-b)
   - A. 0.34.
   - B. 0.45.
   - C. 0.60.
6. Which of Tsai's statements is correct? (LOS: los-09-02-b)
   - A. Only Statement 1.
   - B. Only Statement 2.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Active class weights against policy are +5%, -5%, -3%, +3%.
> Allocation value added $= \sum \Delta w_j R_{B,j} = 0.05(12.8) - 0.05(7.4) - 0.03(3.2) + 0.03(-2.8) = 0.640 - 0.370 - 0.096 - 0.084 = 0.0900\%$.
> B is wrong because it multiplies the active weights by the sub-portfolio returns instead of the benchmark returns: $0.05(14.2) - 0.05(6.1) - 0.03(3.9) + 0.03(-1.5) = 0.2430\%$.
> C is wrong because it is the total value added, $8.678 - 7.760 = 0.9180\%$, not the allocation component.
> 2. **B.** Within-class value added: $14.2 - 12.8 = 1.4$, $6.1 - 7.4 = -1.3$, $3.9 - 3.2 = 0.7$, $-1.5 - (-2.8) = 1.3$.
> Selection value added $= \sum w_{P,j} R_{A,j} = 0.50(1.4) + 0.15(-1.3) + 0.22(0.7) + 0.13(1.3) = 0.700 - 0.195 + 0.154 + 0.169 = 0.8280\%$.
> Check: $0.0900 + 0.8280 = 0.9180\%$, equal to $8.678 - 7.760$.
> A is wrong because it weights the within-class value added by policy weights, $0.45(1.4) + 0.20(-1.3) + 0.25(0.7) + 0.10(1.3) = 0.6750\%$, which drops the interaction effect that the convention assigns to selection.
> C is wrong because it is the total value added rather than the selection component.
> 3. **A.** $\alpha_P = R_P - \beta_P R_B = 14.2 - 1.15(12.8) = 14.2 - 14.72 = -0.5200\%$.
> Crestline's 1.40% is active return, which equals alpha only when beta is 1; with beta 1.15 the higher return is more than explained by the extra benchmark exposure.
> B is wrong because it accepts the manager's label and treats active return $R_P - R_B$ as alpha.
> C is wrong because it divides the benchmark return by beta instead of multiplying: $14.2 - 12.8/1.15 = 14.2 - 11.1304 = 3.0696\%$.
> 4. **B.** Annualized active return $= 0.085 \times 12 = 1.0200\%$; annualized active risk $= 0.49 \times \sqrt{12} = 1.6974\%$.
> $IR = 1.0200 / 1.6974 = 0.6009$.
> A is wrong because it leaves the ratio monthly, $0.085/0.49 = 0.1735$ (equivalently, it annualizes the standard deviation by 12 instead of $\sqrt{12}$).
> C is wrong because it annualizes the mean but not the standard deviation: $1.0200/0.49 = 2.0816$.
> 5. **B.** Current Sharpe ratio $= (8.678 - 4.0)/10.4 = 4.678/10.4 = 0.4498$.
> With 75% in the fund and 25% in T-bills: return $= 0.75(8.678) + 0.25(4.0) = 7.5085\%$, volatility $= 0.75(10.4) = 7.80\%$, so $SR = (7.5085 - 4.0)/7.80 = 3.5085/7.80 = 0.4498$, unchanged.
> A is wrong because it scales the excess return by 0.75 but keeps the full 10.4% volatility: $3.5085/10.4 = 0.3374$.
> C is wrong because it scales the volatility but not the excess return: $4.678/7.80 = 0.5997$.
> 6. **B.** Statement 2 is correct: multiplying every active weight by a constant scales active return and active risk by the same constant, so an unconstrained portfolio's IR is unchanged while active risk doubles.
> Statement 1 is wrong: against a risky policy benchmark, a T-bill position is itself a large active bet (an underweight of every risky class), so active return and active risk do not scale together and the IR generally shrinks.
> A is wrong because it transfers the Sharpe ratio's cash invariance to the IR.
> C is wrong because only the aggressiveness property holds for the IR.

## Distractor design

1. B: active weights multiplied by portfolio (sub-portfolio) returns instead of benchmark returns; C: total value added reported as the allocation component.
2. A: selection weighted by policy weights, dropping the interaction term; C: total value added reported as the selection component.
3. B: active return mislabelled as alpha (beta assumed to be 1); C: beta adjustment inverted (benchmark return divided by beta).
4. A: monthly ratio not annualized (or volatility annualized by 12); C: mean annualized but volatility left monthly.
5. A: only the numerator scaled for cash; C: only the denominator scaled for cash.
6. A: Sharpe ratio cash invariance wrongly assigned to the IR; C: both invariance properties assigned to the IR.
