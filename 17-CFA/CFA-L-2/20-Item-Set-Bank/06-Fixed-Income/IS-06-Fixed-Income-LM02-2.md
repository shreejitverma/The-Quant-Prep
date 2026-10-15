---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 2
title: "Kestrel Life: Validating a Calibrated Rate Tree"
los: [los-06-02-c, los-06-02-d, los-06-02-e]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Kestrel Life: Validating a Calibrated Rate Tree

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Kestrel Life Assurance is a mid-sized life insurer that reports the fair value of its general-account bond portfolio to its regulator each quarter.
Priya Ramaswamy, CFA, heads the model validation team, and she is reviewing a binomial interest rate tree built by Oliver Grant, a junior quantitative analyst.
The tree will later be used to value callable bonds, but Ramaswamy first wants to confirm that it prices option-free bonds correctly.
Kestrel's regulator has criticized the insurer in the past for relying on vendor prices without independent checks, so the validation report must document every step of the calibration and show that the tree is consistent with the benchmark curve.
Ramaswamy plans to rebuild the missing parts of the tree herself, test Grant's calibration logic, and value one bond two different ways.

Grant used the annual-pay benchmark par curve in Exhibit 1 and the one-factor lognormal interest rate model.
He estimated volatility at 18% from ten years of historical one-year rate changes; implied volatility from recent swaption prices was 21%, but Kestrel's model policy requires the historical estimate.

Exhibit 1: Benchmark par curve (annual pay)

| Maturity | Par rate |
|---|---|
| 1 year | 3.00% |
| 2 years | 3.60% |
| 3 years | 4.00% |
| 4 years | 4.25% |

Grant calibrated the first three periods of the tree at 18% volatility, and the file he submitted has two cells whose values were accidentally deleted.

Exhibit 2: Calibrated one-year forward rates at 18% volatility

| Time 0 | Time 1 | Time 2 |
|---|---|---|
| 3.0000% | 4.9842% | 6.7692% |
| | Node 1-L | Node 2-M |
| | | 3.2949% |

In Exhibit 2, Node 1-L is the lower rate at Time 1, and Node 2-M is the middle rate at Time 2.
Grant's working notes show how he calibrated Time 1.
He first tried a lower Time 1 rate of 3.9000%, set the upper rate using the lognormal relation, valued the two-year 3.60% par bond on the resulting two-period tree, and then adjusted his trial until the model price equaled 100.0000.

Ramaswamy selects a test bond from the portfolio: a three-year, 5.00% annual-coupon, option-free bond issued by a government agency whose debt trades on the benchmark curve.
She asks Grant to value the bond by backward induction on the completed three-period tree, and separately by discounting each cash flow at the benchmark spot rates.

Ramaswamy also asks how the tree would change under alternative volatility assumptions.
Grant replies: "If the regulator forced us to use a volatility close to zero, say 0.01%, the tree would collapse, and after recalibration every rate at Time 2 would sit on a single value."
Ramaswamy asks him to state that single value before the validation report is signed.

## Questions

1. The rate at Node 1-L is closest to: (LOS: los-06-02-d)
   - A. 3.1899%.
   - B. 3.4774%.
   - C. 4.1632%.
2. The rate at Node 2-M that is consistent with the other Time 2 rates in Exhibit 2 is closest to: (LOS: los-06-02-c)
   - A. 4.7227%.
   - B. 4.8566%.
   - C. 5.6541%.
3. Using Grant's first trial rate for Time 1, the model value of the two-year par bond and the adjustment it calls for are: (LOS: los-06-02-d)
   - A. 99.5275; the trial rates are too high and must be lowered.
   - B. 99.5275; the trial rates are too low and must be raised.
   - C. 99.9465; the trial rates are too high and must be lowered.
4. The value of the 5.00% agency bond at the upper node at Time 1 is closest to: (LOS: los-06-02-e)
   - A. 97.6910.
   - B. 99.3520.
   - C. 102.3970.
5. The Time 0 value of the 5.00% agency bond from backward induction on the tree is closest to: (LOS: los-06-02-e)
   - A. 102.7751.
   - B. 102.7908.
   - C. 107.7908.
6. The single value that the Time 2 rates would approach under Grant's 0.01% volatility scenario is closest to: (LOS: los-06-02-d)
   - A. 4.0000%.
   - B. 4.0244%.
   - C. 4.8566%.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Adjacent rates at the same date differ by the multiplier $e^{2\sigma}$, so $i_{1,L} = i_{1,H} e^{-2\sigma} = 4.9842\% \times e^{-0.36} = 4.9842\% \times 0.697676 = 3.4774\%$.
> A is wrong because it applies a linear multiplier, $4.9842\% \times (1 - 0.36) = 3.1899\%$, instead of the lognormal relation.
> C is wrong because it uses $e^{-\sigma} = e^{-0.18}$, giving 4.1632%, which places the nodes one standard deviation apart instead of two.
> 2. **A.** Node 2-M is one step above the lowest Time 2 node, so $i_{2,M} = 3.2949\% \times e^{0.36} = 4.7227\%$; equivalently it is the geometric mean $\sqrt{6.7692\% \times 3.2949\%} = 4.7227\%$, and $4.7227\% \times e^{0.36} = 6.7692\%$ confirms the upper node.
> B is wrong because 4.8566% is the implied one-year forward rate two years from now ($1.040244^3 / 1.036109^2 - 1$); the middle node only approximates the forward and is not equal to it once volatility is positive.
> C is wrong because it applies $e^{-\sigma}$ to the upper node ($6.7692\% \times e^{-0.18} = 5.6541\%$), half the correct spacing.
> 3. **A.** Trial rates: $i_{1,L} = 3.9000\%$ and $i_{1,H} = 3.9000\% \times e^{0.36} = 5.5900\%$.
> Time 1 values of the two-year bond: $103.60/1.055900 = 98.1154$ and $103.60/1.039000 = 99.7113$.
> Time 0 value: $[3.60 + 0.5(98.1154 + 99.7113)]/1.03 = 99.5275$, below par, so the trial discounts too heavily and the rates must be lowered.
> The calibrated solution is $i_{1,L} = 3.4774\%$ and $i_{1,H} = 4.9842\%$, lower than the trial, consistent with this conclusion.
> B is wrong because a model price below par means the discount rates are too high, not too low.
> C is wrong because it sets the upper rate with $e^{\sigma}$ ($3.9000\% \times e^{0.18} = 4.6691\%$), which gives $103.60/1.046691 = 98.9785$ and a Time 0 value of 99.9465.
> 4. **B.** Time 2 values: $105/1.067692 = 98.3430$, $105/1.047227 = 100.2648$, $105/1.032949 = 101.6507$.
> Upper Time 1 node, discounted at its own rate of 4.9842%: $[5 + 0.5(98.3430 + 100.2648)]/1.049842 = 104.3039/1.049842 = 99.3520$.
> A is wrong because it discounts the node at the next period's upper rate of 6.7692% instead of the node's own rate: $104.3039/1.067692 = 97.6910$.
> C is wrong because 102.3970 is the value at the lower Time 1 node, $[5 + 0.5(100.2648 + 101.6507)]/1.034774$, an upper and lower node mix-up.
> 5. **B.** Time 0: $[5 + 0.5(99.3520 + 102.3970)]/1.03 = 102.7908$.
> The spot rates bootstrapped from Exhibit 1 are 3.0000%, 3.6109% and 4.0244%, and $5/1.03 + 5/1.036109^2 + 105/1.040244^3 = 102.7908$, the same value, which confirms the calibration.
> A is wrong because it skips the tree and discounts every cash flow at the 4.00% three-year par yield (102.7751), the single-YTM error.
> C is wrong because it adds a phantom 5.00 coupon at Time 0 ($102.7908 + 5$); no coupon is received on the valuation date.
> 6. **C.** As volatility approaches zero, the calibrated tree collapses onto the implied one-year forward rates, so every Time 2 node approaches the forward rate two years from now: $1.040244^3 / 1.036109^2 - 1 = 4.8566\%$.
> Recalibrating at 0.01% volatility gives Time 2 rates of 4.8575%, 4.8566% and 4.8556%, confirming the limit.
> A is wrong because 4.00% is the three-year par rate, a yield on a coupon bond, not a one-year rate two years forward.
> B is wrong because 4.0244% is the three-year spot rate, the average rate over three years rather than the one-year rate for year three.

## Distractor design

1. A: linear $1 - 2\sigma$ multiplier instead of $e^{-2\sigma}$; C: $e^{-\sigma}$ used, one standard deviation of spacing instead of two.
2. B: implied forward rate taken as the exact middle node rather than its approximation; C: $e^{-\sigma}$ spacing applied from the upper node.
3. B: direction of the calibration adjustment reversed; C: upper trial rate built with $e^{\sigma}$ instead of $e^{2\sigma}$.
4. A: node discounted at the next period's rate instead of its own rate; C: upper and lower Time 1 nodes swapped.
5. A: single YTM (three-year par yield) used instead of the tree; C: phantom coupon added at Time 0.
6. A: par rate substituted for the forward rate; B: spot rate substituted for the forward rate.
