---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 2
title: "Crestline Retirement System: Paths and Simulations"
los: [los-06-02-c, los-06-02-g, los-06-02-h]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Crestline Retirement System: Paths and Simulations

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

The Crestline Municipal Employees' Retirement System is a public pension plan with a large fixed-income allocation that includes government bonds and agency mortgage-backed securities (MBS).
Daniel Hollis, CFA, a senior analyst in the plan's fixed-income group, is training Mei Tanaka, a new analyst, on the plan's valuation models before the annual review by the plan's investment consultant.

Hollis first shows Tanaka a lognormal binomial interest rate tree that the group calibrated to the current annual-pay benchmark par curve of 1.50% (1 year), 2.00% (2 years) and 2.40% (3 years), using a volatility assumption of 12%.

Exhibit 1: Calibrated one-year forward rates at 12% volatility

| Time 0 | Time 1 | Time 2 |
|---|---|---|
| 1.5000% | 2.8136% | 4.0605% |
| | 2.2133% | 3.1941% |
| | | 2.5126% |

Hollis asks Tanaka to value a three-year, 3.50% annual-coupon, option-free government bond by pathwise valuation rather than backward induction.
He explains that a path is identified by the sequence of up (H) and down (L) moves after Time 0, so that path HL takes the higher rate at Time 1 and then moves down to the middle rate at Time 2.
Part of Tanaka's spreadsheet is shown in Exhibit 2.

Exhibit 2: Present value of the 3.50% bond's cash flows by path

| Path | Time 0 rate | Time 1 rate | Time 2 rate | Present value |
|---|---|---|---|---|
| HH | 1.5000% | 2.8136% | 4.0605% | 102.1120 |
| HL | 1.5000% | 2.8136% | 3.1941% | (to be computed) |
| LH | 1.5000% | 2.2133% | 3.1941% | 103.4964 |
| LL | 1.5000% | 2.2133% | 2.5126% | (to be computed) |

Hollis notes that the plan also holds a five-year option-free agency bond that the group values on a five-period version of the same tree.
He tells Tanaka that the consultant will check whether the pathwise value agrees with the value from backward induction, because a mismatch would signal a spreadsheet error.

The conversation turns to the MBS portfolio.
Crestline values its MBS with a Monte Carlo forward-rate simulation that generates 500 monthly short-rate paths.
Tanaka makes two statements.

Statement 1: "If we increase the simulation from 500 to 5,000 paths, the model value of each MBS will move closer to its fundamental value."

Statement 2: "We need simulation rather than a tree for MBS because prepayments depend on the path that rates have taken to reach their current level, not just on the current level itself."

Hollis then describes a problem discovered in a recent model run.
Before any adjustment, the simulated paths produced average present values for the benchmark government bonds that were above their observed market prices.

Finally, the investment consultant asks about the volatility input.
Hollis explains that the 12% volatility is a proportional volatility of the one-year rate, and the consultant asks what it would imply for the standard deviation of the one-year rate if the one-year rate were 3.00% instead of today's 1.50%.

## Questions

1. The number of interest rate paths Crestline must evaluate to value the five-year agency bond pathwise is: (LOS: los-06-02-g)
   - A. 5.
   - B. 16.
   - C. 32.
2. The present value of the 3.50% bond's cash flows along path HL is closest to: (LOS: los-06-02-g)
   - A. 100.9430.
   - B. 102.9123.
   - C. 106.4123.
3. The value of the 3.50% bond from pathwise valuation is closest to: (LOS: los-06-02-g)
   - A. 102.8402.
   - B. 103.0545.
   - C. 103.1650.
4. Which of Tanaka's statements about Monte Carlo simulation is correct? (LOS: los-06-02-h)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.
5. The most appropriate way to correct the benchmark problem Hollis describes is to: (LOS: los-06-02-h)
   - A. subtract a constant from all rates on all paths until the benchmarks reprice to market.
   - B. add a constant to all rates on all paths until the benchmarks reprice to market.
   - C. increase the number of paths until the benchmarks reprice to market.
6. The standard deviation of the one-year rate asked about by the consultant is closest to: (LOS: los-06-02-c)
   - A. 18 bps.
   - B. 36 bps.
   - C. 72 bps.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** A binomial tree for an n-period bond has $2^{n-1}$ paths because the Time 0 rate is common to all of them; for five periods, $2^{4} = 16$.
> A is wrong because 5 is the number of distinct rates at Time 4, not the number of paths; the middle nodes are reached by many paths (Pascal's Triangle gives 1, 4, 6, 4, 1).
> C is wrong because $2^{5} = 32$ counts a branching at Time 0, which does not exist.
> 2. **B.** Discount each cash flow by the cumulative product of the rates along the path.
> Discount factors: $1/1.015 = 0.985222$; $1/(1.015 \times 1.028136) = 0.958260$; $1/(1.015 \times 1.028136 \times 1.031941) = 0.928600$.
> Present value: $3.50 \times 0.985222 + 3.50 \times 0.958260 + 103.50 \times 0.928600 = 3.4483 + 3.3539 + 96.1101 = 102.9123$.
> A is wrong because it discounts each cash flow at the single rate for its period raised to its time, $3.50/1.015 + 3.50/1.028136^2 + 103.50/1.031941^3 = 100.9430$, instead of compounding across the path.
> C is wrong because it adds a phantom 3.50 coupon at Time 0 ($102.9123 + 3.50 = 106.4123$).
> 3. **C.** Path LL: $3.50/1.015 + 3.50/(1.015 \times 1.022133) + 103.50/(1.015 \times 1.022133 \times 1.025126) = 104.1391$.
> Average of all four paths: $(102.1120 + 102.9123 + 103.4964 + 104.1391)/4 = 103.1650$.
> This equals the backward induction value and the spot-rate value ($z_1 = 1.5000\%$, $z_2 = 2.0050\%$, $z_3 = 2.4138\%$ give 103.1650), which confirms the calibration.
> A is wrong because it averages only the three paths in the spreadsheet with values (HH, HL, LH), omitting path LL: $(102.1120 + 102.9123 + 103.4964)/3 = 102.8402$.
> B is wrong because it treats the three terminal rates as three paths, counting the middle node once: $(102.1120 + 102.9123 + 104.1391)/3 = 103.0545$; paths HL and LH are distinct and each carries weight one quarter.
> 4. **B.** Statement 2 is correct: prepayment cash flows are path dependent, and a recombining tree collapses different rate histories into the same node, so Monte Carlo is required.
> Statement 1 is incorrect because more paths improve only the statistical accuracy of the estimate; closeness to fundamental value depends on the quality of the model and its inputs.
> A and C are wrong because they accept Statement 1, confusing precision with truth.
> 5. **B.** The simulated benchmark values are too high, which means the simulated rates are too low on average.
> A constant drift adjustment added to all rates on all paths raises the discount rates until the average present value of each benchmark equals its market price, which makes the simulation arbitrage free.
> A is wrong because subtracting a constant lowers rates and pushes the benchmark values even further above market.
> C is wrong because more paths reduce sampling error but do not remove a systematic level bias in the simulated rates.
> 6. **B.** Under the lognormal model the standard deviation of the one-year rate is $i_0 \sigma$, proportional to the level of rates: $3.00\% \times 0.12 = 0.36\%$, or 36 bps.
> A is wrong because $1.50\% \times 0.12 = 18$ bps uses today's rate and ignores the question's premise that volatility scales with the rate level.
> C is wrong because it applies $2\sigma$, the node-spacing exponent, as if it were the standard deviation: $3.00\% \times 0.24 = 72$ bps.

## Distractor design

1. A: number of terminal nodes counted instead of paths; C: $2^{n}$ instead of $2^{n-1}$ (branching at Time 0 assumed).
2. A: per-period rates applied independently instead of cumulative path discounting; C: phantom coupon at Time 0.
3. A: missing path omitted from the average; B: recombining middle node counted as one path (Pascal's Triangle weights ignored).
4. A: statistical accuracy confused with closeness to fundamental value; C: accepts the false statement along with the true one.
5. A: drift adjustment applied in the wrong direction; C: path count used to fix a calibration bias.
6. A: level dependence of lognormal volatility ignored; C: node-spacing $2\sigma$ used as the standard deviation.
