---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 1
title: "Corvale Industrial: Quarter-End Rate Hedge Reporting"
los: [los-07-01-c, los-07-01-e]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Corvale Industrial: Quarter-End Rate Hedge Reporting

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Hannah Brooks, CFA, is a treasury analyst at Corvale Industrial, a manufacturer of packaging machinery that funds itself with floating-rate bank debt priced off the market reference rate (MRR).
Mateus Oliveira, the treasurer, asks Brooks to price two new hedges and to prepare fair values of the company's derivatives for the quarter-end financial statements.
All MRRs are annualized add-on rates quoted on an actual/360 basis.

Corvale expects to draw a 40,000,000 bank loan in 90 days, with interest reset at the 180-day MRR for a single 180-day period.
To lock in its borrowing cost, Corvale enters a 3 x 9 forward rate agreement (FRA) today with a notional of 40,000,000, paying fixed at the no-arbitrage FRA rate.

Exhibit 1: MRR term structure today

| Days | 30 | 60 | 90 | 120 | 180 | 240 | 270 | 360 |
|---|---|---|---|---|---|---|---|---|
| MRR | 3.85% | 3.92% | 4.00% | 4.06% | 4.18% | 4.29% | 4.34% | 4.46% |

The quarter ends 30 days after the FRA is initiated.
On that date Brooks observes the following rates.

Exhibit 2: MRR term structure 30 days later (quarter-end)

| Days | 30 | 60 | 90 | 120 | 180 | 210 | 240 | 270 |
|---|---|---|---|---|---|---|---|---|
| MRR | 4.12% | 4.21% | 4.28% | 4.34% | 4.46% | 4.52% | 4.57% | 4.61% |

Brooks also wants to show Oliveira how the hedge would settle.
She assumes that when the FRA expires, the 90-day MRR will be 4.50% and the 180-day MRR will be 4.62%, and that the settlement discount rate will equal the 180-day MRR.

Corvale is also negotiating a new one-year, 60,000,000 floating-rate loan with quarterly interest resets.
Oliveira wants to swap it to fixed with a one-year, quarterly-reset, pay-fixed interest rate swap priced off the Exhibit 1 term structure, using 90, 180, 270, and 360 days as the settlement dates.

Finally, Corvale has an existing five-year, annual-reset interest rate swap entered two years ago, in which it pays a fixed rate of 3.10% and receives MRR on a notional of 25,000,000.
Three annual settlements remain, and the next settlement is exactly one year away.

Exhibit 3: Current present value factors for the existing swap

| Years to settlement | 1 | 2 | 3 |
|---|---|---|---|
| PV factor | 0.961538 | 0.922086 | 0.883278 |

Brooks drafts two statements for the audit committee memo.

Statement 1: "Our pay-fixed swap is equivalent to issuing a fixed-rate bond and holding a floating-rate bond of the same par, and on each reset date the floating-rate bond is worth par because its coupon resets to its own discount rate."

Statement 2: "The existing swap has gained value because the fixed rate on a new three-year swap is now below the 3.10% we pay."

Oliveira asks Brooks to confirm her numbers and her memo before the audit committee meets.

## Questions

1. Based on Exhibit 1, the fixed rate on the 3 x 9 FRA is closest to: (LOS: los-07-01-c)
   - A. 2.98%.
   - B. 4.32%.
   - C. 4.47%.
2. For the quarter-end financial statements, the value of Corvale's FRA position based on Exhibit 2 is closest to: (LOS: los-07-01-c)
   - A. 37,260.
   - B. 37,557.
   - C. 50,288.
3. Under Brooks's settlement assumptions, the FRA settlement at expiration is closest to: (LOS: los-07-01-c)
   - A. 15,289 received by Corvale.
   - B. 30,232 received by Corvale.
   - C. 30,931 received by Corvale.
4. Based on Exhibit 1, the annualized fixed rate on the one-year quarterly-reset swap is closest to: (LOS: los-07-01-e)
   - A. 1.10%.
   - B. 4.38%.
   - C. 5.81%.
5. Based on Exhibit 3, the value of the existing swap to Corvale is closest to: (LOS: los-07-01-e)
   - A. -773,701.
   - B. 279,627.
   - C. 773,701.
6. Which of Brooks's statements is correct? (LOS: los-07-01-e)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** A 3 x 9 FRA expires in 90 days on a 180-day underlying rate that matures at day 270, so use $L_{90}$ and $L_{270}$ and annualize over $t_m = 180/360$.
> $FRA_0 = \{[1 + 0.0434(270/360)]/[1 + 0.0400(90/360)] - 1\}/(180/360) = (1.032550/1.010000 - 1) \times 2 = 4.4653\%$.
> A is wrong because it annualizes the forward ratio over the full 270 days instead of the 180-day underlying: $0.022327/0.75 = 2.9769\%$.
> B is wrong because it uses $L_{180}$ instead of $L_{270}$, which prices a 3 x 6 FRA: $\{[1 + 0.0418(0.5)]/1.01 - 1\}/0.25 = 4.3168\%$.
> 2. **A.** Thirty days later the 3 x 9 FRA has become a 2 x 8, so the offsetting FRA is priced from the 60-day and 240-day rates.
> $FRA_g = \{[1 + 0.0457(240/360)]/[1 + 0.0421(60/360)] - 1\}/(180/360) = 4.6573\%$.
> Corvale pays fixed (long), so $V_g = 40{,}000{,}000 \times (0.04657321 - 0.04465347)(180/360)/[1 + 0.0457(240/360)] = 38{,}394.92/1.030467 = 37{,}259.74$.
> Rates rose, so the long FRA has a positive value; the discount runs over the 240 days to the end of the underlying period.
> B is wrong because it discounts over only the 180-day underlying at the 180-day rate, $38{,}394.92/[1 + 0.0446(0.5)] = 37{,}557.39$.
> C is wrong because it rebuilds $FRA_g$ from the original 90-day and 270-day tenors on the new curve (4.7245%), giving 50,288.26.
> 3. **B.** The FRA is advanced set and advanced settled, so the rate difference on the 180-day underlying is discounted back from day 270 to day 90.
> Long settlement $= 40{,}000{,}000 \times (0.0462 - 0.04465347)(180/360)/[1 + 0.0462(180/360)] = 30{,}930.69/1.023100 = 30{,}232.33$, received by Corvale because MRR rose above the fixed rate.
> A is wrong because it uses the 90-day MRR tenor for $t_m$ and the discount, $40{,}000{,}000 \times (0.0462 - 0.044653)(0.25)/1.01155 = 15{,}288.76$; the underlying is a 180-day rate.
> C is wrong because it omits the discount factor and pays the in-arrears amount of 30,930.69 at expiration.
> The 4.50% 90-day MRR is a decoy.
> 4. **B.** PV factors from Exhibit 1: $1/[1 + 0.0400(90/360)] = 0.990099$, $1/[1 + 0.0418(180/360)] = 0.979528$, $1/[1 + 0.0434(270/360)] = 0.968476$, $1/[1 + 0.0446(360/360)] = 0.957304$, summing to 3.895407.
> Periodic rate $= (1 - 0.957304)/3.895407 = 1.0961\%$; annualized $\times 360/90 = 4.3842\%$.
> A is wrong because it reports the quarterly periodic rate without annualizing by $1/AP$.
> C is wrong because it drops the final PV factor from the annuity sum, $(1 - 0.957304)/2.938103 \times 4 = 5.8127\%$.
> 5. **C.** Current three-year swap rate: $\sum PV_i = 0.961538 + 0.922086 + 0.883278 = 2.766902$ and $r_{FIX,t} = (1 - 0.883278)/2.766902 = 4.218509\%$.
> Receive-fixed value $= 25{,}000{,}000 \times (0.0310 - 0.04218509) \times 2.766902 = -773{,}700.95$.
> Corvale pays fixed, so its value is $+773{,}701$; rates have risen above its locked rate.
> A is wrong because it reports the receive-fixed counterparty's value.
> B is wrong because it omits the annuity of PV factors and values a single period's rate difference, $25{,}000{,}000 \times 0.01118509 = 279{,}627$.
> 6. **A.** Statement 1 is correct: pay-fixed, receive-floating replicates a short fixed-rate bond and a long floating-rate bond, and the floater prices at par at each reset.
> Statement 2 is incorrect: the swap gained value, but because the new three-year rate (4.2185%) is above, not below, the 3.10% Corvale pays.
> B and C accept Statement 2, which reverses the direction of the rate move that benefits a fixed payer.

## Distractor design

1. A: forward ratio annualized over $t_T$ instead of $t_m$; B: wrong spot-rate pair (3 x 6 instead of 3 x 9).
2. B: seasoned FRA discounted over m days at the m-day rate instead of T - g days; C: $FRA_g$ built from the original tenors instead of the shortened ones.
3. A: wrong underlying tenor (90-day instead of 180-day) in $t_m$ and the discount; C: advanced-settlement discounting omitted.
4. A: periodic rate not annualized by $1/AP$; C: final PV factor dropped from the annuity sum.
5. A: value reported for the wrong party (sign); B: rate difference not multiplied by $\sum PV_i$.
6. B and C: direction of the rate move that benefits the pay-fixed party reversed.
