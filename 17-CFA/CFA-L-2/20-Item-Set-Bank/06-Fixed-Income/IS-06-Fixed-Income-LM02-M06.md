---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 2
title: "Halvorsen Re: Rebuilding a Vendor Lattice"
los: [los-06-02-d, los-06-02-e, los-06-02-b, los-06-02-f]
difficulty: 4
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Halvorsen Re: Rebuilding a Vendor Lattice

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Halvorsen Re is a reinsurer that holds a large portfolio of government and quasi-government bonds to back its claims reserves.
Leila Haddad, CFA, is the senior investment risk analyst, and she reports to Stefan Brandt, the chief risk officer.
A pricing vendor has delivered a lognormal binomial interest rate tree that Halvorsen will later use for its callable holdings, but a data-transfer error corrupted part of the file.

The vendor confirms that the tree was built with the one-factor lognormal model and calibrated to the annual-pay benchmark par curve in Exhibit 1.
The volatility field in the file is blank.
Brandt notes that the one-year swaption market currently implies a volatility of 22%, and he suggests Haddad simply use that figure.

Exhibit 1: Benchmark par curve and market data

| Item | Value |
|---|---|
| 1-year par rate | 3.10% |
| 2-year par rate | 3.70% |
| 3-year par rate | 4.10% |
| 4-year par rate | 4.35% |
| 1-year swaption implied volatility | 22% |

Exhibit 2: Surviving entries of the vendor tree (one-year forward rates)

| Time 0 | Time 1 | Time 2 |
|---|---|---|
| 3.1000% | 5.0603% | 6.7944% |
| | (corrupted) | (corrupted) |
| | | (corrupted) |

Halvorsen's model policy requires that any tree used for valuation reprice the benchmark par bonds exactly and that its volatility assumption be documented in the model inventory.
The vendor has promised to resend the Time 3 rates next week, so the four-year par rate is not needed for the current rebuild.
Haddad's plan is to rebuild the tree from the surviving entries rather than rely on an outside volatility estimate.
She reasons that the two Time 1 rates must value the two-year benchmark par bond at exactly 100, which pins down the missing Time 1 rate.
Once both Time 1 rates are known, the volatility the vendor used follows from the lognormal spacing, and that volatility fills in the missing Time 2 rates.

Haddad will use the rebuilt tree to value a three-year, 5.50% annual-coupon, option-free bond issued by a government-guaranteed export agency whose debt trades on the benchmark curve.
A dealer is offering Halvorsen the agency bond at 103.6500 per 100 of par.
Brandt observes that the bond's yield to maturity at the dealer's price is close to the 4.10% three-year par rate and suggests that the bond is fairly priced.

Brandt also questions whether the rebuild matters for valuation.
He makes the following comment.

"Suppose we ignore the vendor's volatility and recalibrate the whole tree at the 22% swaption volatility.
The wider tree gives more weight to low-rate outcomes, where the agency bond is worth more, so its value on the lattice will come out above what the vendor's tree gives."

Haddad replies that she will show the committee the Time 0 value from the rebuilt tree alongside the value from a recalibrated 22% tree before the bond is approved.

## Questions

1. The lower one-year forward rate at Time 1 that is consistent with the vendor's calibration is closest to: (LOS: los-06-02-d)
   - A. 3.2590%.
   - B. 3.5917%.
   - C. 3.6018%.
2. Using the rebuilt tree, the value of the 5.50% agency bond at the lower node at Time 1 is closest to: (LOS: los-06-02-e)
   - A. 101.8841.
   - B. 103.0979.
   - C. 103.6108.
3. Relative to its arbitrage-free value, the dealer's offer for the agency bond is: (LOS: los-06-02-b)
   - A. below value by 0.2278.
   - B. below value by 0.2496.
   - C. below value by 0.3182.
4. The Time 0 value of the agency bond on the rebuilt tree, and its value on a tree recalibrated at 22% volatility, are closest to: (LOS: los-06-02-f)
   - A. 103.8996 on the rebuilt tree and 103.8996 at 22% volatility.
   - B. 103.8996 on the rebuilt tree and a higher value at 22% volatility.
   - C. 109.3996 on the rebuilt tree and 109.3996 at 22% volatility.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The two-year 3.70% par bond pays 103.70 at Time 2 and must be worth 100 at Time 0: $100 = [3.70 + 0.5(V_H + V_L)]/1.031$.
> Required sum of Time 1 values: $V_H + V_L = 2(100 \times 1.031 - 3.70) = 198.8000$.
> Upper node: $V_H = 103.70/1.050603 = 98.7052$, so $V_L = 198.8000 - 98.7052 = 100.0948$.
> Lower rate: $i_{1,L} = 103.70/100.0948 - 1 = 3.6018\%$.
> A is wrong because it adopts Brandt's 22% swaption volatility, $5.0603\% \times e^{-0.44} = 3.2590\%$, a rate that does not reprice the benchmark and ignores the vendor's actual calibration.
> B is wrong because it places the two rates symmetrically around the implied forward rate, $2 \times 4.3260\% - 5.0603\% = 3.5917\%$, where the forward is $1.037112^2/1.031 - 1 = 4.3260\%$ on spots of 3.1000% and 3.7112%; lognormal rates are spread multiplicatively, so their average sits slightly above the forward.
> 2. **B.** The volatility the vendor used follows from the two Time 1 rates recovered in Question 1: $\sigma = \ln(5.0603\%/3.6018\%)/2 = 0.3400/2 = 17.00\%$.
> Missing Time 2 rates: middle $6.7944\% \times e^{-0.34} = 4.8361\%$, lower $6.7944\% \times e^{-0.68} = 3.4422\%$.
> Time 2 values of the 105.50 final cash flow: $105.50/1.067944 = 98.7880$, $105.50/1.048361 = 100.6333$, $105.50/1.034422 = 101.9893$.
> Lower Time 1 node: $[5.50 + 0.5(100.6333 + 101.9893)]/1.036018 = 106.8113/1.036018 = 103.0979$.
> A is wrong because it discounts the node at the next period's middle rate of 4.8361% instead of the node's own rate: $106.8113/1.048361 = 101.8841$.
> C is wrong because it fills the Time 2 nodes with the 22% swaption volatility (4.3758% and 2.8182%), giving values of 101.0770 and 102.6083 and a node value of $[5.50 + 0.5(101.0770 + 102.6083)]/1.036018 = 103.6108$.
> 3. **B.** Bootstrap the spot rates from Exhibit 1: $z_1 = 3.1000\%$, $z_2 = 3.7112\%$, and $1 = 0.041/1.031 + 0.041/1.037112^2 + 1.041/(1+z_3)^3$ gives $z_3 = 4.1251\%$.
> Arbitrage-free value: $5.50/1.031 + 5.50/1.037112^2 + 105.50/1.041251^3 = 5.3346 + 5.1134 + 93.4516 = 103.8996$.
> The offer is below value by $103.8996 - 103.6500 = 0.2496$ per 100, so Brandt's YTM-based conclusion that the bond is fairly priced is wrong.
> A is wrong because it measures value by discounting every cash flow at the 4.10% three-year par yield (103.8778), the single-YTM error: $103.8778 - 103.6500 = 0.2278$.
> C is wrong because it discounts each cash flow at the par rate of its own maturity, $5.50/1.031 + 5.50/1.037^2 + 105.50/1.041^3 = 103.9682$, using par yields instead of spot rates: $103.9682 - 103.6500 = 0.3182$.
> 4. **A.** Upper Time 1 node: $[5.50 + 0.5(98.7880 + 100.6333)]/1.050603 = 100.1431$; Time 0: $[5.50 + 0.5(100.1431 + 103.0979)]/1.031 = 103.8996$, the spot-rate value from Question 3.
> A calibrated tree must return the spot-rate value for an option-free bond at any volatility, because both methods are arbitrage free.
> Recalibrating at 22% moves the Time 1 rates to 5.2729% and 3.3959% and the Time 2 rates to 7.3850%, 4.7562% and 3.0632%, and the bond still values at 103.8996.
> B is wrong because it accepts Brandt's argument: the wider spread is fully absorbed when the tree is recalibrated to the benchmark prices, and an option-free bond has no option value to gain.
> C is wrong because it adds a phantom 5.50 coupon at Time 0 ($103.8996 + 5.50 = 109.3996$); no coupon is received on the valuation date.

## Distractor design

1. A: outside swaption volatility (decoy) used instead of the par-bond calibration condition; B: rates placed arithmetically symmetric around the implied forward rate instead of solving the calibration equation.
2. A: node discounted at the next period's rate instead of its own; C: missing Time 2 rates filled with the decoy 22% volatility instead of the volatility implied by the rebuilt Time 1 rates.
3. A: single-YTM discounting at the three-year par yield; C: each cash flow discounted at its own maturity's par yield instead of its spot rate.
4. B: option value attributed to an option-free bond at higher volatility; C: phantom coupon added at Time 0.
