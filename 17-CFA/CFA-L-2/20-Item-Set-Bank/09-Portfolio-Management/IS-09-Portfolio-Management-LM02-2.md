---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 2
title: "Norrland Industrial Pension Plan: Global Equity Manager Search"
los: [los-09-02-b, los-09-02-c, los-09-02-d]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Norrland Industrial Pension Plan: Global Equity Manager Search

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Lars Ekholm, CFA, is a consultant at Fjordgate Advisory.
He is advising the Norrland Industrial Pension Plan, a corporate defined benefit plan, on the selection of one active global equity manager.
The plan already holds a low-cost index fund that replicates its global equity benchmark, and it may hold the index fund long or short through a futures overlay.
All three candidates in the search are measured against the same benchmark.

Ekholm's forecasts for the next year are shown in Exhibit 1.
The risk-free rate is 3.0%.

Exhibit 1: Ex ante forecasts

| | Expected return | Total risk | Active risk | Sharpe ratio |
|---|---|---|---|---|
| Benchmark | 8.60% | 16.00% | 0.0% | 0.350 |
| Fund P | 11.60% | 20.62% | 13.0% | 0.417 |
| Fund Q | 10.84% | 17.89% | 8.0% | 0.438 |
| Fund R | 10.00% | 17.09% | 6.0% | 0.410 |

Fund Q's manager states in its questionnaire that its process is essentially unconstrained today, with a transfer coefficient close to 1.00.
The manager estimates an information coefficient of 0.07 and 16 independent decisions per year, and says these figures reconcile with Ekholm's forecast for the fund.
Fund P's ex post record over 2023-2025 shows an average active return of -0.6% with active risk of 7.4%.

Ekholm makes three remarks in his draft report of 3 March 2026.

Remark 1: "Fund R has the lowest active risk and the lowest total risk, so it is the natural complement to the plan's index fund."

Remark 2: "The plan should hold the chosen active fund in whatever proportion delivers the optimal level of active risk, with the balance, positive or negative, in the index fund."

Remark 3: "Because the maximum Sharpe ratio satisfies $SR_P^2 = SR_B^2 + IR^2$, even Fund P's realized information ratio would have improved the plan's Sharpe ratio over 2023-2025."

Karin Lund, the plan's chief investment officer, replies with two observations.

Lund: "The plan's board is about to adopt guidelines that ban short sales and cap every country overweight at 5%.
Our risk team estimates that, applied inside Fund Q's mandate, the guidelines would cut its transfer coefficient to 0.70, with no effect on the manager's information coefficient or breadth."

Lund: "If we end up choosing Fund R, a 60/40 blend of Fund R and the index fund would reduce Fund R's active return and active risk by 40% each and leave its information ratio unchanged."

Ekholm is asked to recommend a fund, compute the plan's best achievable Sharpe ratio, and size the position both before and after the new guidelines.
He assumes that active returns are uncorrelated with benchmark returns for every fund.

## Questions

1. Using Exhibit 1, the fund that Norrland should combine with its index fund to achieve the highest Sharpe ratio is: (LOS: los-09-02-d)
   - A. Fund P.
   - B. Fund Q.
   - C. Fund R.
2. The highest Sharpe ratio Norrland can achieve by combining the fund selected in Question 1 with the index fund is closest to: (LOS: los-09-02-d)
   - A. 0.448.
   - B. 0.561.
   - C. 0.630.
3. Before the new guidelines, the weights on the selected fund and the index fund that achieve the optimal active risk are closest to: (LOS: los-09-02-d)
   - A. 0.63 in the fund and 0.37 in the index fund.
   - B. 1.60 in the fund and -0.60 in the index fund.
   - C. 2.50 in the fund and -1.50 in the index fund.
4. If the guidelines reduce Fund Q's transfer coefficient to 0.70, the optimal active risk for the combined portfolio is closest to: (LOS: los-09-02-d)
   - A. 6.27%.
   - B. 8.96%.
   - C. 12.80%.
5. Under the new guidelines, the expected active return of the combined portfolio at its new optimal active risk is closest to: (LOS: los-09-02-c)
   - A. 1.23%.
   - B. 1.76%.
   - C. 2.51%.
6. Which of the following statements is most accurate? (LOS: los-09-02-b)
   - A. Ekholm's Remark 1.
   - B. Ekholm's Remark 3.
   - C. Lund's statement about the 60/40 blend of Fund R.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Rank by expected information ratio, because $SR_P^2 = SR_B^2 + IR^2$ makes the highest-IR fund produce the highest combined Sharpe ratio.
> Active returns: P $= 11.60 - 8.60 = 3.00\%$, Q $= 2.24\%$, R $= 1.40\%$.
> IRs: P $= 3.00/13.0 = 0.2308$, Q $= 2.24/8.0 = 0.2800$, R $= 1.40/6.0 = 0.2333$.
> Check against the questionnaire: $IC\sqrt{BR} = 0.07\sqrt{16} = 0.28$ with TC of 1.00.
> A is wrong because Fund P has the highest active return, but it buys that return with the most active risk.
> C is wrong because it follows Remark 1 and ranks by the lowest active risk and the lowest total risk, which is irrelevant to the combination decision; Fund R's IR of 0.2333 only ranks second of the three.
> 2. **A.** $SR_P = \sqrt{0.35^2 + 0.28^2} = \sqrt{0.1225 + 0.0784} = \sqrt{0.2009} = 0.4482$.
> Verification at the optimal active risk of 12.8% (Question 3): excess return $= 0.35(16.0) + 0.28(12.8) = 5.600 + 3.584 = 9.184\%$, total risk $= \sqrt{16.0^2 + 12.8^2} = 20.49\%$, and $9.184/20.49 = 0.4482$.
> B is wrong because it combines the benchmark's Sharpe ratio with Fund Q's own Sharpe ratio instead of its IR: $\sqrt{0.35^2 + 0.438^2} = 0.5607$.
> C is wrong because it adds the ratios in levels, $0.35 + 0.28 = 0.63$, instead of in squares.
> 3. **B.** $\sigma_A^{*} = (IR/SR_B)\sigma_B = (0.28/0.35)(16.0) = 12.80\%$.
> Fund Q delivers only 8.0% active risk, so the fund weight is $12.80/8.0 = 1.60$ and the index fund weight is $1 - 1.60 = -0.60$, a short position.
> A is wrong because it inverts the scaling, $8.0/12.80 = 0.625$, which would cut active risk to 5.0% instead of raising it to 12.8%.
> C is wrong because it inverts the ratio in the optimal active risk formula, using $SR_B/IR$: $(0.35/0.28)(16.0) = 20.00\%$, and $20.00/8.0 = 2.50$.
> 4. **B.** With constraints, $\sigma_A = TC(IR^{*}/SR_B)\sigma_B = 0.70(0.28/0.35)(16.0) = 0.70 \times 12.80 = 8.96\%$.
> A is wrong because it applies TC twice: $0.70^2 \times 12.80 = 6.272\%$.
> C is wrong because it ignores the transfer coefficient and keeps the unconstrained 12.80%.
> 5. **B.** $E(R_A) = TC \times IC \times \sqrt{BR} \times \sigma_A = 0.70 \times 0.07 \times \sqrt{16} \times 8.96 = 0.70 \times 0.28 \times 8.96 = 1.7562\%$.
> The constrained IR is $0.70 \times 0.28 = 0.196$, and the constrained maximum Sharpe ratio falls to $\sqrt{0.35^2 + 0.196^2} = 0.4011$.
> A is wrong because it applies TC twice: $0.49 \times 0.28 \times 8.96 = 1.2293\%$.
> C is wrong because it omits TC from the fundamental law: $0.28 \times 8.96 = 2.5088\%$.
> 6. **C.** Mixing a fund with the benchmark scales every active weight by the fund weight, so active return falls to $0.60(1.40) = 0.84\%$ and active risk to $0.60(6.0) = 3.60\%$, and the IR stays $0.84/3.60 = 0.2333$.
> A is wrong because the level of active risk and the level of total risk do not determine the best complement; the IR does, and Fund R's IR (0.2333) is below Fund Q's (0.2800).
> B is wrong because squaring destroys the sign: Fund P's realized IR is $-0.6/7.4 = -0.0811$, and a negative-IR fund reduces, not improves, the Sharpe ratio; the relation cannot be used to rank or credit negative-IR funds.

## Distractor design

1. A: ranking by raw active return; C: ranking by lowest active risk and lowest total risk.
2. B: fund Sharpe ratio used in place of the IR; C: Sharpe ratio and IR added in levels, not squares.
3. A: fund weight ratio inverted (current over optimal active risk); C: IR and benchmark Sharpe ratio inverted inside the optimal active risk formula.
4. A: transfer coefficient applied twice; C: transfer coefficient omitted.
5. A: transfer coefficient applied twice (once in sigma and again squared in the law); C: transfer coefficient omitted from the law.
6. A: lowest active risk and lowest total risk confused with the IR criterion; B: sign lost by squaring a negative IR.
