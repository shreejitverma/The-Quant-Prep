---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 2
title: "Castellane Endowment: Strip Prices and an Amortizing Note"
los: [los-06-02-b, los-06-02-a, los-06-02-e, los-06-02-i]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Castellane Endowment: Strip Prices and an Amortizing Note

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Elodie Marchand, CFA, manages the liquidity sleeve of the Castellane University Endowment, which holds sovereign bonds and sovereign-guaranteed agency paper.
Her colleague Rafael Duarte, a quantitative analyst, supports her with pricing models.
Marchand is reviewing a three-year, 4.60% annual-coupon, option-free sovereign bond that trades on three electronic venues.
Sovereign dealers strip coupon bonds into zero-coupon securities and reconstitute them freely, and Marchand ignores transaction costs throughout.
The endowment's investment policy permits the sleeve to execute riskless arbitrage trades across venues and against the strip market when they arise.

Exhibit 1: Sovereign zero-coupon strip prices and a par yield (per 100 of face value)

| Maturity | Strip price |
|---|---|
| 1 year | 97.0874 |
| 2 years | 93.5317 |
| 3 years | 89.5424 |
| 3-year sovereign par yield | 3.7327% |

Exhibit 2: Quoted prices of the 4.60% three-year sovereign bond (per 100 of par)

| Venue | Price |
|---|---|
| Venue A | 102.3685 |
| Venue B | 102.4298 |
| Venue C | 102.5300 |

Duarte tells Marchand that the three venues appear to price the bond off different curves, and that one of them uses a single discount rate for every cash flow.
Marchand wants to know the bond's arbitrage-free value and the trade that would earn the largest riskless profit if the quotes stay firm.

The endowment is also offered a three-year amortizing note issued by a sovereign-guaranteed agency whose debt trades on the sovereign curve.
The note has a face value of 100 and pays 5.00% annual interest on the principal outstanding at the start of each year.
Principal is repaid at the end of each year in scheduled installments of 30 (Year 1), 30 (Year 2), and 40 (Year 3), so the scheduled cash flows are 35.00, 33.50, and 42.00.
The note has no embedded options.

Duarte has calibrated a lognormal binomial interest rate tree to the strip curve in Exhibit 1 using a 15% volatility assumption.

Exhibit 3: Calibrated one-year forward rates at 15% volatility

| Time 0 | Time 1 | Time 2 |
|---|---|---|
| 3.0000% | 4.3712% | 5.8966% |
| | 3.2382% | 4.3683% |
| | | 3.2361% |

Duarte explains that he values the note by backward induction, and that each node value excludes the cash flow paid on that node's date.
Marchand asks for the value of the note at the upper node at Time 1 so she can see how much of the note's value depends on a rise in rates next year.

Finally, Duarte mentions that the endowment's risk system is being upgraded from a one-factor model to the Gauss+ model.
He describes the Gauss+ model to Marchand as follows: "It uses three factors: short, medium, and long rates.
The short rate is the rate the central bank controls, the long rate is mean reverting, and the model generates a hump-shaped volatility curve that peaks at medium maturities."
Marchand asks him to confirm which description of the model is accurate before the risk committee meets.

## Questions

1. Based on Exhibit 1, the arbitrage-free value of the 4.60% sovereign bond is closest to: (LOS: los-06-02-b)
   - A. 102.3685.
   - B. 102.4191.
   - C. 102.4298.
2. Based on Exhibits 1 and 2, the strategy that earns the largest riskless profit per 100 of par is to: (LOS: los-06-02-a)
   - A. buy the bond on Venue A, strip it, and sell the zero-coupon securities, earning 0.0613.
   - B. buy the bond on Venue A and sell it on Venue C, earning 0.1615.
   - C. buy zero-coupon securities, reconstitute the bond, and sell it on Venue C, earning 0.1002.
3. Based on Exhibit 3, the value of the amortizing note at the upper node at Time 1 is closest to: (LOS: los-06-02-e)
   - A. 69.3617.
   - B. 70.3755.
   - C. 74.5468.
4. Which statement about the Gauss+ model is most accurate? (LOS: los-06-02-i)
   - A. The long-rate factor is mean reverting, and the volatility curve is hump shaped with its peak at medium maturities.
   - B. The short-rate factor is a random, mean-reverting process, and the long rate is held constant.
   - C. It is a one-factor model like Vasicek, extended with a time-dependent drift so that it fits today's curve exactly.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** A coupon bond is a package of zero-coupon bonds, so each cash flow is valued at the strip price for its date.
> $4.60 \times 0.970874 + 4.60 \times 0.935317 + 104.60 \times 0.895424 = 4.46602 + 4.30246 + 93.66135 = 102.4298$.
> Equivalently, the strips imply spot rates of $3.0000\%$, $3.4000\%$ and $3.7506\%$, and discounting at those spot rates gives the same 102.4298.
> A is wrong because it discounts every cash flow at the three-year spot rate of 3.7506%: $4.4337 + 4.2734 + 93.6614 = 102.3685$, which over-discounts the two early coupons on an upward-sloping curve.
> B is wrong because it discounts every cash flow at the 3.7327% three-year par yield (the decoy in Exhibit 1): $4.4345 + 4.2749 + 93.7097 = 102.4191$, the single-YTM error.
> 2. **B.** The same bond trades at three prices, so the widest gap is between the cheapest venue (A, 102.3685) and the dearest venue (C, 102.5300).
> Buying on Venue A and selling on Venue C earns $102.5300 - 102.3685 = 0.1615$ per 100 of par with no net position.
> A is wrong because it is a genuine value-additivity arbitrage but smaller: the strips are worth 102.4298, so buying on Venue A and selling the strips earns only $102.4298 - 102.3685 = 0.0613$.
> C is wrong because it is also genuine but smaller: reconstituting at a strip cost of 102.4298 and selling on Venue C earns $102.5300 - 102.4298 = 0.1002$.
> Venue B is the arbitrage-free venue because its price equals the strip value.
> 3. **B.** Time 2 values, discounting the final cash flow of 42.00 at each Time 2 rate: $42/1.058966 = 39.6613$, $42/1.043683 = 40.2421$, $42/1.032361 = 40.6834$.
> Upper Time 1 node, with the Year 2 cash flow of 33.50 in the numerator and the node's own rate of 4.3712%: $[33.50 + 0.5(39.6613 + 40.2421)]/1.043712 = 73.4517/1.043712 = 70.3755$.
> The lower Time 1 node is 71.6428, and the Time 0 value is $[35.00 + 0.5(70.3755 + 71.6428)]/1.03 = 102.9215$, which equals the strip value $35 \times 0.970874 + 33.5 \times 0.935317 + 42 \times 0.895424 = 102.9215$, confirming the calibration.
> A is wrong because it discounts the node at the next period's upper rate of 5.8966% instead of the node's own rate: $73.4517/1.058966 = 69.3617$.
> C is wrong because it computes interest on the original 100 of face value every year (cash flows 35.00, 35.00 and 45.00), which gives Time 2 values of 42.4943 and 43.1165 and an upper-node value of $[35 + 0.5(42.4943 + 43.1165)]/1.043712 = 74.5468$.
> 4. **A.** Gauss+ is a multi-factor model with short, medium and long factors; the long-term factor is mean reverting, the short rate is not random because it is set by the central bank, and the model produces a hump-shaped volatility curve peaking at medium tenors.
> Duarte's description is therefore accurate, and statement A restates its key features.
> B is wrong because it reverses the roles: the short rate is the non-random, central-bank-controlled factor, and the long rate is the mean-reverting factor.
> C is wrong because Gauss+ is multi-factor, and a time-dependent drift that fits today's curve describes the one-factor Ho-Lee model, not Vasicek or Gauss+.

## Distractor design

1. A: every cash flow discounted at the longest spot rate; B: every cash flow discounted at the single three-year par yield (decoy).
2. A: a real but smaller value-additivity trade against the strips; C: a real but smaller reconstitution trade; the best trade uses the widest cross-venue gap.
3. A: node discounted at the next period's rate instead of its own; C: interest computed on original face value instead of the outstanding balance.
4. B: short-rate and long-rate factor roles reversed; C: Gauss+ confused with a one-factor arbitrage-free model (Ho-Lee drift attached to Vasicek).
