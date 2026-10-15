---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 3
title: "Corrib Bay Utility Callable Relative Value"
los: [los-06-03-c, los-06-03-g, los-06-03-h, los-06-03-i]
difficulty: 4
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Corrib Bay Utility Callable Relative Value

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tamsin Holloway, CFA, manages an investment-grade credit fund at Corrib Bay Asset Management.
The fund holds a three-year 5.50% annual-coupon bond issued by Galvani Power & Light, an A-rated regulated utility.
Galvani may redeem the bond at 100.75 at the end of Year 1 or at 100 at the end of Year 2, and on no other dates.
Corrib Bay's model prices the bond at an option-adjusted spread (OAS) of 100 bps, using the firm's standard interest rate volatility assumption of 15%.

**Exhibit 1: Benchmark government par curve (annual coupon)**

| Maturity | Par rate |
|---|---|
| 1 year | 3.400% |
| 2 years | 3.900% |
| 3 years | 4.300% |
| 5 years | 4.650% |

The pricing system calibrates a binomial tree to Exhibit 1 at 15% volatility, but the printout Holloway received was truncated and shows only one Year 2 node.
She knows that adjacent rates within a year are linked by $R_u = R_d e^{2\sigma\sqrt{t}}$ with annual time steps.

**Exhibit 2: Benchmark one-year forward rates at 15% volatility (truncated)**

| Node | Year 0 | Year 1 | Year 2 |
|---|---|---|---|
| Upper | 3.4000% | 5.0853% | not printed |
| Middle | | | not printed |
| Lower | | 3.7673% | 3.7496% |

To measure rate risk, the risk team shifts the par curve in Exhibit 1 up and down by 25 bps in parallel, recalibrates the tree at 15% volatility each time, and revalues the bond at the same 100 bps OAS.

**Exhibit 3: Galvani callable bond risk data (per 100 of par)**

| Item | Value |
|---|---|
| $PV_-$ (curve down 25 bps, OAS 100 bps) | 101.034 |
| $PV_+$ (curve up 25 bps, OAS 100 bps) | 99.757 |
| Modified duration from the prime broker (yield to maturity 5.354%) | 2.70 |

A dealer has sent Holloway the OAS levels in Exhibit 4 for three-year callable utility bonds with call schedules similar to Galvani's.
The dealer's footnote states that all OAS figures were computed at 10% interest rate volatility.

**Exhibit 4: Dealer comparables (OAS at 10% volatility)**

| Issuer | Rating | OAS (bps) |
|---|---|---|
| Aske Energy | A | 101 |
| Penhallow Gas | A | 103 |
| Duskmere Power | BBB | 148 |

Holloway's junior analyst, Farid Nasser, prepares the monthly relative value note on 9 September.
He writes: "Galvani's OAS of 100 bps is 2 bps tighter than the 102 bps average of the A-rated comparables, so Galvani is rich and should be sold. It is also far tighter than Duskmere."

Holloway asks Nasser to rebuild the tree, check the Galvani valuation node by node, and report an effective duration for the bond instead of the prime broker's figure.
She also tells him that the relative value note cannot go to the investment committee until the spread comparison is placed on a consistent basis.

## Questions

1. The benchmark one-year forward rate at the upper node in Year 2 is closest to: (LOS: los-06-03-c)
   - A. 5.0614%
   - B. 5.7311%
   - C. 6.8322%
2. Using an OAS of 100 bps, the value of the Galvani callable bond is closest to: (LOS: los-06-03-g)
   - A. 100.182
   - B. 100.396
   - C. 100.559
3. The effective duration of the Galvani callable bond is closest to: (LOS: los-06-03-i)
   - A. 2.54
   - B. 2.70
   - C. 5.09
4. The most appropriate response to Nasser's relative value conclusion is that: (LOS: los-06-03-h)
   - A. Galvani is rich, because its OAS is below the average OAS of the A-rated comparables.
   - B. the comparison is invalid as stated; at the dealer's 10% volatility Galvani's OAS would be higher than 100 bps and above the A-rated average, so Galvani is more likely cheap.
   - C. the comparison is invalid as stated; at the dealer's 10% volatility Galvani's OAS would be lower than 100 bps, so Galvani is even richer than Nasser concludes.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** With annual steps, each node is $e^{2\sigma} = e^{0.30} = 1.3499$ times the node below it (V6 p.137).
> Middle $= 3.7496\% \times e^{0.30} = 5.0614\%$; upper $= 3.7496\% \times e^{0.60} = 3.7496\% \times 1.8221 = 6.832\%$, which is option C (the unrounded lower node of 3.749561% gives 6.8322%).
> A is wrong because it applies the factor only once, which gives the middle node.
> B is wrong because it sets $t = 2$ (years from today) instead of the one-year time step and applies the factor once: $3.7496\% \times e^{0.30\sqrt{2}} = 3.7496\% \times 1.5285 = 5.731\%$.
> 2. **B.** Add 100 bps to every node: Year 0 4.4000%; Year 1 6.0853% and 4.7673%; Year 2 7.8322%, 6.0614% and 4.7496% (V6 p.145).
> Year 2: $105.50/1.078322 = 97.8372$; $105.50/1.060614 = 99.4707$; $105.50/1.047496 = 100.7164 \to$ called at 100.
> Year 1 upper: $(5.50 + 0.5 \times (97.8372 + 99.4707))/1.060853 = 98.1794$, not called.
> Year 1 lower: $(5.50 + 0.5 \times (99.4707 + 100))/1.047673 = 100.4467$, below the Year 1 call price of 100.75, so not called.
> Year 0: $(5.50 + 0.5 \times (98.1794 + 100.4467))/1.044 = 100.3957$.
> A is wrong because it applies a call price of 100 at Year 1, resetting the 100.4467 node: $(5.50 + 0.5 \times (98.1794 + 100))/1.044 = 100.1817$.
> C is wrong because it adds the OAS but never applies the call rule, which gives the option-free value at a 100 bps spread, 100.5594.
> Without the OAS the tree gives 102.2975, which would price Galvani as default-free.
> 3. **A.** $PV_0 = 100.396$ from Question 2, because the OAS is the spread that equates the model value to the price.
> $\text{EffDur} = (PV_- - PV_+)/(2 \times \Delta\text{Curve} \times PV_0) = (101.034 - 99.757)/(2 \times 0.0025 \times 100.396) = 1.277/0.50198 = 2.54$ (V6 p.150).
> B is wrong because modified duration assumes the cash flows do not change when rates change, which fails for a callable bond; the prime broker's 2.70 is a yield-based measure on the bond's full three-year cash flows.
> C is wrong because it drops the factor 2: $1.277/(0.0025 \times 100.396) = 5.09$, which exceeds the bond's three-year maturity.
> 4. **B.** OAS is a model output that depends on the volatility assumption, so Galvani's 100 bps at 15% cannot be compared with OAS figures computed at 10% (V6 p.146, p.147).
> At lower volatility the call is worth less, so the tree assigns a higher value to the bond at any given spread, and a larger OAS is needed to reprice the same 100.3957: solving the Galvani tree at 10% volatility gives about 103.9 bps, above the 102 bps A-rated average (at 20% volatility it would be about 96.4 bps).
> On a consistent basis Galvani offers more spread than its A-rated peers, so it is more likely underpriced (cheap), not rich.
> Duskmere is BBB rated, so its wider OAS compensates for credit risk and supports no relative value conclusion.
> A is wrong because it compares OAS figures computed under different volatility assumptions.
> C is wrong because it reverses the volatility-OAS relation; a lower volatility assumption raises a callable bond's OAS at a fixed price.

## Distractor design

- Q1: A stops one step short and returns the middle node (incomplete tree construction); B uses time from today instead of the time step in $\sqrt{t}$ (wrong formula variant).
- Q2: A misreads the step-down schedule and calls at 100 in Year 1 (misread exhibit); C adds the OAS but omits the exercise rule (straight value at the OAS).
- Q3: B uses the yield-based modified duration decoy (wrong measure for a bond with an option); C drops the factor 2 (wrong formula variant).
- Q4: A compares OAS across inconsistent volatility assumptions (misread exhibit footnote); C reverses the volatility-OAS direction (sign).
