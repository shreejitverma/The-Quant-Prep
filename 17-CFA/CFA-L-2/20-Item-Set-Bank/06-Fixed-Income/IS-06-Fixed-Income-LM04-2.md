---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 4
title: "Corvane Industrial: Tree-Based Credit Valuation for an Insurer"
los: [los-06-04-a, los-06-04-e, los-06-04-f]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Corvane Industrial: Tree-Based Credit Valuation for an Insurer

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Mateo Duarte, CFA, manages the corporate bond sleeve of Halvorsen Life Assurance, an insurer that matches annuity liabilities with high-grade debt.
He is valuing two senior unsecured bonds issued by Corvane Industrial Holdings, a maker of factory automation equipment.
Both bonds mature in three years and pay annually.

Bond F pays a fixed coupon of 3.75% and trades at 100.85 per 100 of par.
Bond N is a floating-rate note that pays the one-year benchmark rate plus a quoted margin of 0.40%.
The rate is set at the start of each year and paid at the end of that year (in arrears).

Duarte uses the benchmark par curve in Exhibit 1 and a binomial interest rate tree calibrated to it at 10% volatility, shown in Exhibit 2.
Each node is reached with the usual binomial probabilities, and each up and down move has probability 0.5.

Exhibit 1: Benchmark par curve and discount factors

| Maturity (years) | Par yield | Discount factor |
|---|---|---|
| 1 | 1.20% | 0.988142 |
| 2 | 1.90% | 0.962930 |
| 3 | 2.50% | 0.928023 |

Exhibit 2: One-year benchmark rates, 10% volatility (top node listed first)

| Date 0 | Date 1 | Date 2 |
|---|---|---|
| 1.2000% | 2.8800% | 4.5530% |
| | 2.3580% | 3.7277% |
| | | 3.0520% |

For both bonds, Halvorsen's credit team assumes a risk-neutral annual (hazard) probability of default of 1.60% and a recovery rate of 30% of the exposure.
Default can occur only on payment dates.
The team's historical default study for Corvane's rating category shows an average annual default rate of 0.40%.

Exhibit 3: Partially completed CVA table for Bond F (per 100 of par)

| Date | Expected exposure | LGD | POD | DF | PV of expected loss |
|---|---|---|---|---|---|
| 1 | 104.8421 | 73.3894 | 1.6000% | 0.988142 | 1.1603 |
| 2 | | | 1.5744% | 0.962930 | |
| 3 | 103.7500 | 72.6250 | 1.5492% | 0.928023 | 1.0441 |

Duarte's supervisor, Ingrid Solheim, reviews his work and makes two comments.

Comment 1: "For Bond F, report the credit spread the way our annuity pricing team uses it: over a theoretical government bond with exactly the same cash flows, not over the three-year par yield."

Comment 2: "The risk team wants to rerun everything on a 20% volatility tree calibrated to the same par curve.
Higher volatility spreads the node rates out, so it must change Bond F's value assuming no default, and it will widen Bond F's credit spread."

Duarte then turns to Bond N.
He notes that at a quoted margin of zero the floater's node values would all equal par, so any credit adjustment must come through the CVA table.
He begins by computing the Date 2 expected exposure for Bond N, the date that most clearly shows how in-arrears coupons enter the calculation.

## Questions

1. The value of Bond F assuming no default is closest to: (LOS: los-06-04-e)
   - A. 100.2935.
   - B. 103.5989.
   - C. 104.8421.
2. The Date 2 expected exposure for Bond F is closest to: (LOS: los-06-04-a)
   - A. 72.6166.
   - B. 99.9881.
   - C. 103.7381.
3. The fair value of Bond F is closest to: (LOS: los-06-04-e)
   - A. 100.2935.
   - B. 100.3333.
   - C. 106.9042.
4. Following Comment 1, the credit spread on Bond F is closest to: (LOS: los-06-04-e)
   - A. 115 bps.
   - B. 249 bps.
   - C. 364 bps.
5. Regarding Comment 2, the most accurate response is that a move to a 20% volatility tree will: (LOS: los-06-04-f)
   - A. lower Bond F's value assuming no default and widen its credit spread.
   - B. leave Bond F's value assuming no default unchanged and slightly lower its CVA, so the spread narrows marginally.
   - C. leave Bond F's value assuming no default unchanged and raise its CVA, because wider rate dispersion increases expected exposure.
6. The Date 2 expected exposure for Bond N is closest to: (LOS: los-06-04-e)
   - A. 100.3855.
   - B. 103.4045.
   - C. 104.5506.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Backward induction through Exhibit 2.
> Date 2 node values: $103.75/1.045530 = 99.2320$, $103.75/1.037277 = 100.0215$, $103.75/1.030520 = 100.6773$.
> Date 1 node values: $[0.5(99.2320) + 0.5(100.0215) + 3.75]/1.028800 = 100.4828$ and $[0.5(100.0215) + 0.5(100.6773) + 3.75]/1.023580 = 101.7013$.
> Date 0: $[0.5(100.4828) + 0.5(101.7013) + 3.75]/1.012000 = 103.5989$.
> Check with discount factors: $3.75 \times (0.988142 + 0.962930) + 103.75 \times 0.928023 = 103.5989$, confirming the tree is arbitrage free.
> A is wrong because it is the fair value after the CVA is deducted (Question 3).
> C is wrong because it is the Date 1 expected exposure from Exhibit 3, the probability-weighted Date 1 value plus the coupon, not the Date 0 value.
> 2. **C.** Expected exposure is the probability-weighted node value plus the coupon due on the date, with binomial weights 0.25, 0.50, 0.25 at Date 2.
> $EE_2 = 0.25(99.2320) + 0.50(100.0215) + 0.25(100.6773) + 3.75 = 99.9881 + 3.75 = 103.7381$.
> A is wrong because it is the Date 2 loss given default, $103.7381 \times 0.70 = 72.6166$, which nets the recovery out of the exposure.
> B is wrong because it omits the 3.75 coupon due on Date 2.
> 3. **A.** Complete Date 2: LGD $= 103.7381 \times 0.70 = 72.6166$; expected loss $= 72.6166 \times 0.015744 = 1.1433$; PV $= 1.1433 \times 0.962930 = 1.1009$.
> $CVA = 1.1603 + 1.1009 + 1.0441 = 3.3053$, and fair value $= 103.5989 - 3.3053 = 100.2935$.
> The bond trades at 100.85, above its fair value, but the question asks only for fair value.
> B is wrong because it uses the Date 2 exposure without the coupon (99.9881): Date 2 PV becomes 1.0611, CVA 3.2655, fair value 100.3333.
> C is wrong because it adds the CVA to VND ($103.5989 + 3.3053 = 106.9042$), a sign error.
> 4. **A.** Corporate YTM at fair value solves $100.2935 = \dfrac{3.75}{1+y} + \dfrac{3.75}{(1+y)^2} + \dfrac{103.75}{(1+y)^3}$: $y = 3.6449\%$.
> The theoretical government bond with the same cash flows is priced at VND, 103.5989, so its YTM solves the same equation at 103.5989: $2.4901\%$.
> Spread $= 3.6449\% - 2.4901\% = 1.1548\%$, about 115 bps.
> B is wrong because it reports the government bond's YTM (2.49%) as the spread.
> C is wrong because it reports Bond F's own YTM (3.64%) as the spread.
> 5. **B.** On a tree calibrated to the same par curve, an option-free bond's VND is independent of volatility: rerunning at 20% returns 103.5989 again.
> The lognormal tree spreads rates asymmetrically around the forwards, so the Date 2 expected exposure dips from 103.7381 to 103.7354, the CVA falls from 3.30533 to 3.30530, and fair value rises by about 0.00003.
> The effect is tiny, but its sign is a slightly lower CVA and a marginally narrower spread, and it exists only because the bond carries credit risk.
> A is wrong because volatility cannot change the default-free value of an option-free bond on a calibrated tree, which is Solheim's error.
> C is wrong because higher volatility lowers, not raises, the expected exposure of this bond; the high-rate nodes move further and their lower bond values dominate.
> 6. **B.** In arrears, the coupon paid on Date 2 was set by the Date 1 rate, so it takes Date 1 probabilities, while the bond value takes Date 2 probabilities.
> Date 2 node values: $(100 + 4.9530)/1.045530 = 100.3826$, $(100 + 4.1277)/1.037277 = 100.3856$, $(100 + 3.4520)/1.030520 = 100.3882$; weighted $0.25(100.3826) + 0.50(100.3856) + 0.25(100.3882) = 100.3855$.
> Date 2 coupons set at Date 1: $(2.8800\% + 0.40\%) \times 100 = 3.2800$ and $(2.3580\% + 0.40\%) \times 100 = 2.7580$; weighted $0.5(3.2800) + 0.5(2.7580) = 3.0190$.
> $EE_2 = 100.3855 + 3.0190 = 103.4045$.
> A is wrong because it omits the coupon due on Date 2.
> C is wrong because it sets the Date 2 coupon from the Date 2 rates with Date 2 probabilities ($0.25(4.9530) + 0.50(4.1277) + 0.25(3.4520) = 4.1651$, total 104.5506), ignoring the in-arrears reset.

## Distractor design

1. A: fair value (after CVA) confused with VND; C: Date 1 expected exposure read from Exhibit 3 as the Date 0 value.
2. A: recovery netted out (LGD reported as exposure); B: coupon omitted from the tree-based exposure.
3. B: coupon omitted from the Date 2 exposure; C: CVA added to VND instead of subtracted (sign).
4. B: benchmark YTM reported as the spread; C: corporate YTM reported as the spread.
5. A: volatility assumed to change VND of an option-free bond; C: direction of the exposure effect reversed.
6. A: in-arrears coupon omitted; C: coupon set from date-t rates and probabilities instead of date t-1 (period mismatch).
