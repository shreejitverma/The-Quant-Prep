---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 2
title: "Okonkwo Family Office: Step-Up Note Paths"
los: [los-06-02-c, los-06-02-g, los-06-02-d, los-06-02-h]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Okonkwo Family Office: Step-Up Note Paths

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Hana Sato, CFA, is an investment analyst at the Okonkwo Family Office, which manages the fixed-income wealth of a multigenerational family.
The office is considering a three-year, option-free step-up note issued by a supranational development bank whose debt trades on the government benchmark curve.
The note pays annual coupons of 2.00% in Year 1, 3.00% in Year 2, and 4.50% in Year 3, and repays 100 of par at maturity.

Sato receives a lognormal binomial interest rate tree from a pricing vendor.
The vendor states that the tree is calibrated to the annual-pay benchmark par curve of 1.80% (1 year), 2.30% (2 years), and 2.65% (3 years), but the file omits the volatility assumption.

Exhibit 1: Vendor tree of one-year forward rates

| Time 0 | Time 1 | Time 2 |
|---|---|---|
| 1.8000% | 3.2072% | 4.3986% |
| | 2.4239% | 3.3244% |
| | | 2.5125% |

Sato labels each path by the sequence of up (H) and down (L) moves after Time 0.
For example, path HL takes the higher rate at Time 1 and then moves down to the middle rate at Time 2, while path LH takes the lower rate at Time 1 and then moves up to the middle rate at Time 2.

Exhibit 2: Rates along each path

| Path | Time 0 | Time 1 | Time 2 |
|---|---|---|---|
| HH | 1.8000% | 3.2072% | 4.3986% |
| HL | 1.8000% | 3.2072% | 3.3244% |
| LH | 1.8000% | 2.4239% | 3.3244% |
| LL | 1.8000% | 2.4239% | 2.5125% |

Sato's first task is to recover the volatility assumption embedded in the vendor tree, because the family office's policy requires it to be documented.
Her second task is to value the step-up note pathwise and to confirm the result against backward induction.

Pieter de Wit, the family office's external fixed-income adviser, reviews the vendor's calibration method with Sato and makes two statements.

Statement 1: "To calibrate Time 2, the vendor holds the Time 1 rates fixed at their calibrated values, sets the other Time 2 rates as multiples of the lowest rate using the lognormal spacing, and adjusts the lowest rate until the three-year benchmark par bond is valued at exactly 100."

Statement 2: "If the vendor recalibrated the tree with a higher volatility assumption, the lower rate at Time 1 would rise, because both Time 1 rates must move up to offset the wider spread."

The family office also holds a small position in agency collateralized mortgage obligations.
For those securities the vendor uses a Monte Carlo forward-rate simulation, and de Wit makes two further statements.

Statement 3: "Modelers often impose mean reversion on simulated rates by setting upper and lower bounds on the rate process."

Statement 4: "To make the simulation arbitrage free, the vendor adjusts the rates on each path separately so that every individual path prices the benchmark bonds at their market values."

Sato records her conclusions in the family office's investment committee memo.

## Questions

1. The volatility assumption embedded in the vendor tree is closest to: (LOS: los-06-02-c)
   - A. 28.0%.
   - B. 16.2%.
   - C. 14.0%.
2. The present value of the step-up note's cash flows along path HL is closest to: (LOS: los-06-02-g)
   - A. 99.5155.
   - B. 101.0822.
   - C. 101.8402.
3. Which of de Wit's statements about calibration is correct? (LOS: los-06-02-d)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.
4. Which of de Wit's statements about Monte Carlo simulation is correct? (LOS: los-06-02-h)
   - A. Statement 4 only.
   - B. Statement 3 only.
   - C. Both Statement 3 and Statement 4.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Adjacent rates at the same date satisfy $i_H = i_L e^{2\sigma}$, so $\sigma = \ln(i_H / i_L)/2$.
> $i_H / i_L = 3.2072\% / 2.4239\% = 1.3232$, $\ln(1.3232) = 0.2800$, and $\sigma = 0.2800 / 2 = 0.1400$, or 14.0%.
> The Time 2 rates confirm it: $3.3244\% / 2.5125\% = 4.3986\% / 3.3244\% = 1.3231 = e^{0.28}$.
> A is wrong because it forgets to halve the log ratio, treating adjacent nodes as one standard deviation apart ($\ln 1.3232 = 28.0\%$).
> B is wrong because it uses a linear spacing, $(1.3232 - 1)/2 = 16.2\%$, instead of the lognormal relation.
> 2. **B.** Discount each cash flow by the cumulative product of the rates along path HL.
> Discount factors: $1/1.018 = 0.982318$; $1/(1.018 \times 1.032072) = 0.951792$; $1/(1.018 \times 1.032072 \times 1.033244) = 0.921169$.
> Present value: $2.00 \times 0.982318 + 3.00 \times 0.951792 + 104.50 \times 0.921169 = 1.9646 + 2.8554 + 96.2622 = 101.0822$.
> The four path values are 100.0917 (HH), 101.0822 (HL), 101.8402 (LH), and 102.6084 (LL); their average, 101.4056, equals the backward induction value and the spot-rate value on spots of 1.8000%, 2.3058% and 2.6639%.
> A is wrong because it discounts each cash flow at the single rate for its period raised to its time, $2/1.018 + 3/1.032072^2 + 104.50/1.033244^3 = 99.5155$, instead of compounding across the path.
> C is wrong because it misreads the path convention and values path LH (lower rate at Time 1, then the middle rate), which gives 101.8402.
> 3. **A.** Statement 1 describes calibration correctly: each date is solved after the earlier dates are fixed, the Time 2 rates are tied together by $e^{2\sigma}$ spacing, and the lowest rate is iterated until the benchmark par bond for that maturity prices at 100.
> Statement 2 is incorrect because a higher volatility spreads the calibrated rates farther apart around the implied forward rate: the upper rate rises and the lower rate falls.
> Recalibrating Exhibit 1 at 20% volatility moves the Time 1 rates to 3.3731% and 2.2611%, so the lower rate falls from 2.4239%.
> B and C are wrong because they accept Statement 2, which reverses the effect of volatility on the lower node.
> 4. **B.** Statement 3 is correct: modelers commonly impose mean reversion on the simulated rates through upper and lower bounds on the rate process.
> Statement 4 is incorrect because the drift adjustment is one constant added to all rates on all paths until the average present value across paths of each benchmark equals its market price; individual paths are not forced to reprice the benchmarks.
> A and C are wrong because they accept Statement 4, which replaces the single drift adjustment with path-by-path fitting.

## Distractor design

1. A: log ratio not halved (nodes treated as one standard deviation apart); B: linear rather than lognormal spacing.
2. A: per-period rates applied independently instead of cumulative path discounting; C: path convention misread (LH valued instead of HL).
3. B and C: effect of higher volatility on the lower node reversed.
4. A and C: drift adjustment misdescribed as path-by-path fitting rather than one constant on all paths that reprices benchmarks on average.
