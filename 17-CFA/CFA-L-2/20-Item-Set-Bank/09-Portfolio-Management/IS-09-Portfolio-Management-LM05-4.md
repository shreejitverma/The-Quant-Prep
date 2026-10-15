---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 5
title: "Aldermoor Municipal Pension Plan: Surplus at Risk and Sleeve Budgets"
los: [los-09-05-e, los-09-05-f, los-09-05-j, los-09-05-l]
difficulty: 4
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Aldermoor Municipal Pension Plan: Surplus at Risk and Sleeve Budgets

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Helena Marsh, CFA, is chief investment officer of the Aldermoor Municipal Pension Plan, a defined benefit plan in the United Kingdom.
The plan's assets are GBP 4,800 million, and the present value of its liabilities, discounted on the curve its regulator prescribes, is GBP 5,200 million.
Last year the plan reported a funding ratio of 95.1%.
The trustees want a single number describing how badly the plan's financial position could deteriorate over the coming year.

Marsh models the liabilities as a short position in long-dated fixed income and prepares the one-year estimates in Exhibit 1, assuming normal distributions.

Exhibit 1: One-year assumptions

| Input | Assets | Liabilities |
|---|---|---|
| Expected growth | 6.0% | 4.0% |
| Standard deviation of growth | 9.0% | 7.5% |
| Correlation of asset returns with liability value changes | 0.55 | 0.55 |

The trustees have set a 95% confidence level for all plan-level measures.

The plan's return-seeking assets are split into three sleeves, and the trustees' risk appetite for these sleeves is a combined 95% one-year VaR of GBP 260 million.
Marsh's risk system produces the figures in Exhibit 2, where each sleeve's contribution is its position-weighted marginal VaR.

Exhibit 2: Return-seeking sleeves, 95% one-year VaR (GBP millions)

| Sleeve | Standalone VaR | Contribution to total VaR |
|---|---|---|
| Global equity | 210 | 180 |
| Private credit | 95 | 55 |
| Real assets | 70 | 25 |
| Total | 375 | 260 |

Trustee Owen Pryce proposes setting each sleeve's limit on a standalone basis, scaling the standalone VaRs down pro rata so that the sleeve limits sum to the GBP 260 million appetite.

Last month the plan replaced its global equity manager with one running a concentrated, high-conviction strategy against the same index benchmark.
The plan also holds an absolute-return sleeve benchmarked to cash.
Marsh and Pryce discuss the risk reports for these mandates.

Marsh: "The ex post tracking error of the global equity sleeve will take many months to reflect the new manager's strategy, whereas its ex ante tracking error reflects the new holdings immediately."

Pryce: "For the absolute-return sleeve, relative VaR and absolute VaR are effectively the same number, because the benchmark is cash."

Finally, the plan's consultant, Imogen Dhar, reviews the plan's full toolkit: a historical-simulation surplus at risk with a ten-year lookback, a replay of the 2022 gilt market crisis applied to current holdings, the liabilities' duration, and a hypothetical "stagflation" scenario.
She asks the trustees to identify which of these measures depend on market returns from a particular historical period.

## Questions

1. Based on Exhibit 1, the plan's 95% one-year surplus at risk is closest to: (LOS: los-09-05-l)
   - A. GBP 425 million.
   - B. GBP 566 million.
   - C. GBP 1,114 million.
2. Under Pryce's proposal, the global equity sleeve's limit and its consequence are closest to: (LOS: los-09-05-j)
   - A. GBP 145.6 million, and the plan would leave part of its GBP 260 million appetite unused.
   - B. GBP 145.6 million, and the plan would use exactly its GBP 260 million appetite.
   - C. GBP 180.0 million, and the plan would leave part of its GBP 260 million appetite unused.
3. Regarding the tracking error and relative VaR statements, which is correct? (LOS: los-09-05-e)
   - A. Marsh's statement only.
   - B. Pryce's statement only.
   - C. Both statements.
4. Of the measures in Dhar's review, those based on market returns from a particular historical period are: (LOS: los-09-05-f)
   - A. the historical-simulation surplus at risk and the 2022 gilt crisis replay.
   - B. the liabilities' duration and the hypothetical stagflation scenario.
   - C. the 2022 gilt crisis replay and the liabilities' duration.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Surplus at risk is VaR on assets long and liabilities short, so the change in surplus is $A r_A - L r_L$.
> Expected change: $4{,}800(0.060) - 5{,}200(0.040) = 288 - 208 = \text{GBP } 80$ million.
> Variance: $(4{,}800 \times 0.09)^2 + (5{,}200 \times 0.075)^2 - 2(0.55)(4{,}800)(5{,}200)(0.09)(0.075) = 186{,}624 + 152{,}100 - 185{,}328 = 153{,}396$, so $\sigma_S = \text{GBP } 391.6580$ million.
> SaR $= 1.65 \times 391.6580 - 80 = 646.2357 - 80 = \text{GBP } 566.2357$ million, about GBP 566 million.
> A is wrong because it ignores the liabilities and computes asset-only VaR: $1.65 \times 432 - 288 = \text{GBP } 424.8$ million, which misses the hedge and the drift of the liabilities.
> C is wrong because it treats the liabilities as a long position and adds the covariance term: $\sigma = 723.9144$, SaR $= 1.65 \times 723.9144 - 80 = \text{GBP } 1{,}114.5$ million.
> The 95.1% prior funding ratio is a decoy; the current ratio is $4{,}800/5{,}200 = 92.31\%$ and surplus is $-\text{GBP } 400$ million, neither of which enters SaR.
> 2. **A.** Pro rata scaling gives the global equity sleeve $260 \times 210/375 = \text{GBP } 145.6$ million (private credit 65.9, real assets 48.5).
> Standalone VaRs ignore diversification between sleeves, so if every sleeve fills its standalone limit, total VaR is only about $260 \times 260/375 = \text{GBP } 180.3$ million, leaving roughly GBP 80 million of appetite unused.
> B is wrong because it assumes standalone VaRs add up to total VaR, which holds only if the sleeves are perfectly correlated.
> C is wrong because GBP 180.0 million is the sleeve's marginal VaR contribution, which is the limit under marginal VaR budgeting, and marginal VaR budgets sum exactly to the GBP 260 million total, so that approach uses the full appetite.
> 3. **C.** Marsh is correct: ex post tracking error is measured from realized returns, so it lags until returns under the new strategy dominate the history, while ex ante tracking error pushes the current holdings through past market variability and responds immediately.
> Pryce is correct: relative VaR (ex ante tracking error) is VaR on portfolio minus benchmark, and a cash benchmark has essentially zero volatility, so relative and absolute VaR coincide.
> A and B are wrong because each rejects a correct statement.
> 4. **A.** Historical-simulation VaR (here, surplus at risk) and historical scenario analysis are both built from market returns in a specific past period.
> B is wrong because duration is a sensitivity to a small change in current rates, and a hypothetical scenario is by construction free of any historical period.
> C is wrong because it pairs a history-based measure with a sensitivity measure that is not history-based.

## Distractor design

1. A: liabilities omitted (asset-only VaR in place of surplus at risk); C: sign error on the covariance term (liabilities treated as long).
2. B: standalone VaRs assumed additive (diversification benefit ignored); C: marginal VaR contribution substituted for the pro rata standalone limit, with the wrong utilization consequence.
3. A: relative VaR against a cash benchmark mistakenly treated as different from VaR; B: ex post and ex ante tracking error responsiveness reversed.
4. B: sensitivity and hypothetical scenario misclassified as history-based; C: only one of the two history-based measures identified.
