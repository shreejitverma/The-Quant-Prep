---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 4
title: "Kestrel Shipping: A Pension Plan Credit Review"
los: [los-06-04-a, los-06-04-e, los-06-04-f]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Kestrel Shipping: A Pension Plan Credit Review

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Priya Raman, CFA, is a credit analyst at Northgate Teachers' Pension Plan, a defined benefit plan with a large allocation to investment-grade corporate debt.
The plan's portfolio manager, Tomasz Lind, asks her to decide whether to add a senior unsecured bond issued by Kestrel Shipping ASA, a dry bulk carrier, at its current market price.

The Kestrel bond has four years to maturity, pays a 4.25% coupon annually, and trades at 99.50 per 100 of par.
Raman values it with a credit valuation adjustment (CVA) model.
She assumes that the government bond yield curve is flat at 3.00% and that there is no interest rate volatility.
The plan's credit research group supplies a risk-neutral annual (hazard) probability of default of 2.00% and a recovery rate of 35% of the exposure.
Default can occur only on coupon dates.
Raman also notes that the historical one-year default rate for shipping issuers with Kestrel's rating is 0.85%, and that the bond's modified duration is 3.60.

Exhibit 1: Partially completed CVA table for the Kestrel bond (per 100 of par)

| Date | Exposure | LGD | POD | POS | Expected loss | DF | PV of expected loss |
|---|---|---|---|---|---|---|---|
| 1 | 107.7858 | 70.0607 | 2.0000% | 98.0000% | 1.4012 | 0.970874 | 1.3604 |
| 2 | | | | | | 0.942596 | |
| 3 | | | | | | 0.915142 | |
| 4 | 104.2500 | 67.7625 | 1.8824% | 92.2368% | 1.2756 | 0.888487 | 1.1333 |

Raman computes the value of the bond assuming no default (VND) as 104.6464 by discounting the promised cash flows at 3.00%.

After reviewing her draft, Lind asks her to stress the credit assumptions.
He proposes two alternative scenarios, each changing one parameter and holding everything else constant.

Scenario 1: The annual probability of default doubles to 4.00%, and the recovery rate stays at 35%.

Scenario 2: The recovery rate halves to 17.5%, and the annual probability of default stays at 2.00%.

Lind comments: "Kestrel's bonds are secured on nothing, so the recovery assumption is the one I lose sleep over.
I expect Scenario 2 to hurt the bond's spread much more than Scenario 1."

Raman replies that she will recompute the CVA, fair value and credit spread under each scenario before the investment committee meets.
She also reminds Lind that the plan's policy permits a purchase only when the model fair value is at or above the market price.

## Questions

1. The expected exposure to default loss for the Kestrel bond on Date 2 is closest to: (LOS: los-06-04-a)
   - A. 69.3172.
   - B. 102.3918.
   - C. 106.6418.
2. The probability of default for Date 3 in Raman's CVA table is closest to: (LOS: los-06-04-a)
   - A. 1.9208%.
   - B. 2.0000%.
   - C. 5.8808%.
3. The credit valuation adjustment for the Kestrel bond is closest to: (LOS: los-06-04-e)
   - A. 4.9793.
   - B. 5.1260.
   - C. 5.3521.
4. Based on Raman's assumptions, at its market price the Kestrel bond is: (LOS: los-06-04-e)
   - A. undervalued by about 0.17, so the purchase is permitted.
   - B. overvalued by about 0.21, so the purchase is not permitted.
   - C. undervalued by about 5.15, so the purchase is permitted.
5. The credit spread on the Kestrel bond implied by Raman's fair value is closest to: (LOS: los-06-04-e)
   - A. 0.70%.
   - B. 1.34%.
   - C. 4.34%.
6. Regarding Lind's stress scenarios, which statement is most likely correct? (LOS: los-06-04-f)
   - A. Scenario 1 widens the spread to about 269 bps, more than Scenario 2 does.
   - B. Scenario 2 widens the spread to about 269 bps, more than Scenario 1 does.
   - C. Neither scenario changes the spread, because the value assuming no default is unchanged.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Expected exposure is the value of the position on the default date before any recovery, including the coupon then due.
> With a flat 3.00% curve and no volatility: $EE_2 = 4.25 + \dfrac{4.25}{1.03} + \dfrac{104.25}{1.03^2} = 4.25 + 4.1262 + 98.2656 = 106.6418$.
> A is wrong because it is the loss given default, $106.6418 \times (1 - 0.35) = 69.3172$, which nets the recovery out of the exposure.
> B is wrong because it omits the Date 2 coupon ($106.6418 - 4.25 = 102.3918$); the coupon is at risk on the default date.
> 2. **A.** POD on Date 3 is the hazard rate applied to the probability of survival through Date 2: $POS_2 = 0.98^2 = 96.0400\%$, so $POD_3 = 2.00\% \times 96.0400\% = 1.9208\%$.
> B is wrong because it uses the unconditional hazard rate for every date and ignores that only survivors can default.
> C is wrong because it is the cumulative probability of default through Date 3, $1 - 0.98^3 = 5.8808\%$.
> 3. **A.** Complete Dates 2 and 3.
> Date 2: LGD $= 106.6418 \times 0.65 = 69.3172$; POD $= 1.9600\%$; expected loss $= 1.3586$; PV $= 1.3586 \times 0.942596 = 1.2806$.
> Date 3: exposure $= 4.25 + 104.25/1.03 = 105.4636$; LGD $= 68.5513$; POD $= 1.9208\%$; expected loss $= 1.3167$; PV $= 1.3167 \times 0.915142 = 1.2050$.
> $CVA = 1.3604 + 1.2806 + 1.2050 + 1.1333 = 4.9793$.
> B is wrong because it applies the 2.00% hazard as the POD on every date (unconditional PODs), giving 5.1260.
> C is wrong because it sums the undiscounted expected losses, $1.4012 + 1.3586 + 1.3167 + 1.2756 = 5.3521$.
> 4. **A.** Fair value $= VND - CVA = 104.6464 - 4.9793 = 99.6670$, which exceeds the 99.50 market price by 0.1670.
> The bond is undervalued under Raman's assumptions, and the policy permits the purchase.
> B is wrong because it deducts the undiscounted expected losses: $104.6464 - 5.3521 = 99.2943$, which is 0.2057 below the price.
> C is wrong because it compares the market price with the VND ($104.6464 - 99.50 = 5.1464$) and ignores the CVA.
> 5. **B.** Solve $99.6670 = \sum_{t=1}^{4} \dfrac{4.25}{(1+y)^t} + \dfrac{100}{(1+y)^4}$ for $y = 4.3425\%$.
> Spread $= 4.3425\% - 3.00\% = 1.3425\%$, about 1.34%, close to the approximation $h(1 - RR) = 2.00\% \times 0.65 = 1.30\%$.
> A is wrong because it multiplies the hazard by the recovery rate instead of the loss severity ($2.00\% \times 0.35 = 0.70\%$).
> C is wrong because it reports the bond's yield to maturity, 4.34%, as the spread without subtracting the 3.00% benchmark.
> 6. **A.** VND stays at 104.6464 in both scenarios; only the CVA changes.
> Scenario 1 (4.00%, 35%): CVA $= 9.6731$, fair value $= 94.9733$, YTM $= 5.6904\%$, spread $= 2.6904\%$, about 269 bps.
> Scenario 2 (2.00%, 17.5%): CVA $= 6.3199$, fair value $= 98.3264$, YTM $= 4.7189\%$, spread $= 1.7189\%$, about 172 bps.
> Doubling the POD scales the whole expected loss, while halving the recovery raises the loss severity only from 0.65 to 0.825, so Lind's expectation is backwards; the approximations $4.00\% \times 0.65 = 2.60\%$ and $2.00\% \times 0.825 = 1.65\%$ tell the same story.
> B is wrong because it swaps the two scenarios, which is Lind's intuition that recovery dominates.
> C is wrong because it confuses the invariance of VND to credit parameters with invariance of fair value; the CVA rises in both scenarios, so the spread widens in both.

## Distractor design

1. A: recovery netted out of the exposure (LGD reported as exposure); B: coupon due on the default date omitted.
2. B: hazard rate used as an unconditional POD; C: cumulative POD reported instead of the date's conditional POD.
3. B: unconditional PODs on every date; C: undiscounted expected losses summed (discounting step skipped).
4. B: undiscounted CVA deducted, flipping the decision; C: market price compared with VND, CVA ignored.
5. A: recovery rate used in place of loss severity in the spread approximation; C: YTM reported as spread (benchmark not subtracted).
6. B: POD and recovery sensitivities reversed; C: VND invariance mistaken for fair value invariance.
