---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 3
title: "Ridgeline Capital Rate-Risk Report"
los: [los-06-03-i, los-06-03-j, los-06-03-k, los-06-03-l, los-06-03-m]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Ridgeline Capital Rate-Risk Report

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Devika Rao, CFA, is the risk manager at Ridgeline Capital, a credit hedge fund.
Each month she prepares an interest rate risk report for the portfolio manager, Marcus Feld, and for the fund's prime broker.
This month the report focuses on three three-year annual-coupon bonds issued by Obrecht Logistics, all of which trade at an option-adjusted spread of 60 bps.

- Bond R1 pays 5.00% and is callable at par at the end of Year 1 and at the end of Year 2.
- Bond R2 pays 4.00% and is putable at par at the end of Year 1 and at the end of Year 2.
- Bond R3 pays 4.30% and is option-free.

Rao implies the OAS from each market price, shifts the benchmark par curve (3.000%, 3.400% and 3.750%) up and down by 25 bps in parallel, rebuilds the tree at 10% volatility each time, and revalues each bond at the same 60 bps OAS.

**Exhibit 1: Obrecht bond prices (per 100 of par)**

| Bond | $PV_0$ | $PV_-$ (curve down 25 bps) | $PV_+$ (curve up 25 bps) |
|---|---|---|---|
| R1 (callable) | 101.206 | 101.597 | 100.716 |
| R2 (putable) | 100.386 | 100.717 | 100.144 |
| R3 (option-free) | 99.869 | 100.564 | 99.181 |

The prime broker's system reports a modified duration of 2.736 for Bond R1, calculated from its yield to maturity of 4.561%.

Ridgeline also holds Bond R4, a 20-year 7.25% annual-coupon bond of a different issuer that is callable at par at any time from the end of Year 5.
The 20-year benchmark par rate is 4.10%, and the issuer's credit spread has been stable.

Finally, the fund holds a three-year floating-rate note issued by a AAA supranational that pays the one-year reference rate set in arrears, capped at 4.25%.
Rao values it with no credit spread on the unshifted benchmark tree in Exhibit 2.

**Exhibit 2: Benchmark one-year forward rates at 10% volatility**

| Node | Year 0 | Year 1 | Year 2 |
|---|---|---|---|
| Upper | 3.0000% | 4.1971% | 5.4428% |
| Middle | | | 4.4562% |
| Lower | | 3.4363% | 3.6484% |

Feld reviews the draft report on 5 September and makes two comments.

Comment 1: "The prime broker's 2.736 is the number I want in the report for R1. It comes straight from the bond's cash flows and does not depend on a volatility model."

Comment 2: "If rates rise 100 bps from here, R2's duration will lengthen toward R3's, because the put stops mattering, and R1's duration will barely move."

Rao responds on 6 September.
She notes that R1 trades only slightly above its call price and that she intends to report one-sided durations and effective convexity for it, because a single two-sided duration hides the asymmetry of its price response.
She also plans a key rate duration profile for Bond R4, which the prime broker currently maps to the 20-year point on the curve.

## Questions

1. The effective duration of Bond R1 is closest to: (LOS: los-06-03-i)
   - A. 0.87
   - B. 1.74
   - C. 3.48
2. Regarding Comment 2, if benchmark rates rise by 100 bps, the effective duration of which bond will most likely lengthen? (LOS: los-06-03-j)
   - A. Bond R1
   - B. Bond R2
   - C. Bond R3
3. Which statement about the one-sided durations of Bond R1 is most accurate? (LOS: los-06-03-k)
   - A. The one-sided up-duration, about 1.94, exceeds the one-sided down-duration, about 1.55, because the call price limits price gains when rates fall.
   - B. The one-sided down-duration, about 1.94, exceeds the one-sided up-duration, about 1.55, because the call protects the holder when rates fall.
   - C. Both one-sided durations equal about 1.74, because the two-sided effective duration applies to shifts in either direction.
4. In Rao's key rate duration profile for Bond R4, the largest key rate duration will most likely be at the: (LOS: los-06-03-k)
   - A. 20-year rate.
   - B. 5-year rate.
   - C. 1-year rate.
5. The effective convexity of Bond R1 is closest to: (LOS: los-06-03-l)
   - A. -156.5
   - B. -39.1
   - C. +156.5
6. The value of the capped supranational floating-rate note is closest to: (LOS: los-06-03-m)
   - A. 99.644
   - B. 99.737
   - C. 100.356

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** $\text{EffDur} = (PV_- - PV_+)/(2 \times \Delta\text{Curve} \times PV_0) = (101.597 - 100.716)/(2 \times 0.0025 \times 101.206) = 0.881/0.50603 = 1.7410$ (V6 p.150).
> Effective duration, not the prime broker's yield-based 2.736, is the valid measure because R1's cash flows change when rates change, so Comment 1 is wrong.
> A is wrong because it uses the 50 bps width of the two shifts as $\Delta\text{Curve}$ inside the factor 2: $0.881/(2 \times 0.005 \times 101.206) = 0.8705$.
> C is wrong because it drops the factor 2: $0.881/(0.0025 \times 101.206) = 3.4820$, which also exceeds the bond's three-year maturity.
> 2. **A.** Rising rates push R1's call out of the money, so the bond stops trading to the call date and its duration lengthens toward that of the straight bond (V6 p.152, p.153).
> B is wrong because rising rates push R2's put into the money, so its duration shortens toward the put date; Comment 2 reverses the putable effect.
> C is wrong because an option-free bond's effective duration falls slightly as rates rise.
> 3. **A.** $\text{EffDur}_{\text{up}} = (101.206 - 100.716)/(0.0025 \times 101.206) = 0.490/0.253015 = 1.9366$.
> $\text{EffDur}_{\text{down}} = (101.597 - 101.206)/(0.0025 \times 101.206) = 0.391/0.253015 = 1.5454$.
> A callable near the money gains little when rates fall because no investor pays much above a price at which the bond can be called away, so up-duration exceeds down-duration (V6 p.154, p.155).
> B is wrong because it swaps $PV_-$ and $PV_+$ and misassigns the protection, which belongs to the issuer.
> C is wrong because it reports the two-sided average, which is exactly the asymmetry the one-sided measures are designed to expose.
> 4. **B.** A 7.25% coupon against a 4.10% 20-year par rate puts the call deep in the money, so R4 is expected to be called at Year 5 and trades like a five-year bond (V6 p.157).
> Its sensitivity migrates from the maturity date to the exercise date, so the 5-year key rate duration dominates.
> A is wrong because it treats R4 as if the call were out of the money, which would leave the maturity-matched rate dominant.
> C is wrong because no exercise decision or dominant cash flow sits at Year 1.
> 5. **A.** $\text{EffCon} = (PV_- + PV_+ - 2 PV_0)/(\Delta\text{Curve}^2 \times PV_0) = (101.597 + 100.716 - 202.412)/(0.0025^2 \times 101.206) = -0.099/0.000632538 = -156.51$ (V6 p.158).
> Negative convexity is expected because the near-the-money call caps the upside; by contrast R2 is $+141.85$ and R3 is $+11.21$ on the same formula.
> B is wrong because it squares the 50 bps total width instead of the 25 bps shift: $-0.099/(0.005^2 \times 101.206) = -39.13$.
> C is wrong because it computes $2 PV_0 - PV_- - PV_+$, flipping the sign, which would describe a putable-like profile.
> 6. **A.** The coupon set at each node is $\min(r_{\text{node}}, 4.25\%)$, paid one year later; the cap binds only at the 5.4428% and 4.4562% nodes (4.1971% is below the cap).
> Year 2: $104.25/1.054428 = 98.8687$; $104.25/1.044562 = 99.8026$; lower node 100.
> Year 1 upper: $(4.1971 + 0.5 \times (98.8687 + 99.8026))/1.041971 = 99.3624$.
> Year 1 lower: $(3.4363 + 0.5 \times (99.8026 + 100))/1.034363 = 99.9046$.
> Year 0: $(3.0 + 0.5 \times (99.3624 + 99.9046))/1.03 = 99.6442$, about 99.644, so the cap is worth $0.356$ (V6 p.161, p.162).
> B is wrong because it caps only the highest node and leaves the 4.4562% node uncapped, giving 99.737.
> C is wrong because it adds the cap's value to par, $100 + 0.356 = 100.356$, as if the cap were an investor option.

## Distractor design

- Q1: A uses the total width of the two shifts as the shift (wrong shift size); C drops the factor 2 (wrong formula variant).
- Q2: B reverses which option moves into the money (sign); C applies option logic to an option-free bond.
- Q3: B swaps the up and down prices (misread exhibit); C reports the symmetric two-sided measure (wrong formula variant).
- Q4: A ignores the moneyness of the call (maturity-date anchoring); C picks the short end with no economic link.
- Q5: B squares the wrong shift size; C flips the numerator (sign).
- Q6: B applies the cap at only one node (partial exercise); C treats the cap as an investor option (sign).
