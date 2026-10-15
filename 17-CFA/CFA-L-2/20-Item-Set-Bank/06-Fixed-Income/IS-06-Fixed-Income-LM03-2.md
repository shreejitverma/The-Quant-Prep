---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 3
title: "Castellan Savings Bank Callable Corporate Screen"
los: [los-06-03-c, los-06-03-g, los-06-03-h]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Castellan Savings Bank Callable Corporate Screen

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Rafael Okonkwo is an analyst on the asset-liability management desk of Castellan Savings Bank.
The desk invests surplus deposits in short-dated investment-grade corporate bonds and must justify each purchase to the bank's treasurer, Helen Marsh, CFA.
Okonkwo is evaluating a three-year 5.40% annual-coupon bond issued by Trevian Industrial Corp., rated A.
The bond is callable at par at the end of Year 1 and at the end of Year 2, and it trades at 99.40 per 100 of par.

Okonkwo values Trevian's bond in the arbitrage-free framework.
He starts from the government par curve in Exhibit 1 and uses the desk's standard interest rate volatility assumption of 15%.

**Exhibit 1: Government par curve (annual coupon)**

| Maturity | Par rate |
|---|---|
| 1 year | 2.800% |
| 2 years | 3.300% |
| 3 years | 3.600% |

**Exhibit 2: Calibrated one-year forward rates at 15% volatility**

| Node | Year 0 | Year 1 | Year 2 |
|---|---|---|---|
| Upper | 2.8000% | 4.3913% | 5.6078% |
| Middle | | | 4.1544% |
| Lower | | 3.2531% | 3.0776% |

To judge relative value, Okonkwo compiles option-adjusted spreads for comparable three-year callable bonds, all computed by the same dealer model at 15% volatility.

**Exhibit 3: Comparable three-year callable bonds (OAS at 15% volatility)**

| Issuer | Rating | Call schedule | OAS (bps) |
|---|---|---|---|
| Arlo Chemicals | A | Par, Years 1 and 2 | 152 |
| Benning Paper | A | Par, Years 1 and 2 | 148 |
| Corvid Mining | BB | Par, Years 1 and 2 | 265 |

Okonkwo notes that Trevian's own five-year callable bonds trade at an OAS of 175 bps, but they are not part of the comparable set.
He takes the average OAS of the two A-rated comparables, 150 bps, as the spread that Trevian's three-year bond should carry.

Marsh sends Okonkwo the following instruction on 8 September: "Build the tree from the government curve and our volatility assumption, add the comparable spread, apply Trevian's call rule at every node, and work backward to today. Do not shortcut it by discounting the cash flows at spot rates."

Okonkwo reports back on 9 September.
He writes: "At an OAS of 150 bps the model value of the Trevian bond is above its 99.40 market price, so the bond looks expensive against its A-rated peers. It also looks expensive against Corvid, which pays 265 bps."

Marsh replies that she wants the relative value conclusion restated correctly before the purchase committee meets.
She adds that the bank's model risk team has proposed raising the desk's volatility assumption from 15% to 20% for all callable bonds, and she asks Okonkwo what that would do to the OAS he reports for Trevian at its current market price.

## Questions

1. Regarding Marsh's instruction, which statement about using the arbitrage-free framework to value the Trevian bond is most accurate? (LOS: los-06-03-c)
   - A. The tree should be calibrated to Trevian's own par curve so that the call decision reflects Trevian's credit, leaving no spread to add.
   - B. One-period forward rates on a tree are required because whether Trevian calls depends on the bond's value at each future call date, which spot rates alone cannot supply.
   - C. The call rule should be applied only at the Year 0 node, after discounting, because the call decision is made on the basis of today's price.
2. Using an OAS of 150 bps, the value of the Trevian bond is closest to: (LOS: los-06-03-g)
   - A. 100.417
   - B. 100.838
   - C. 102.529
3. The most appropriate restatement of Okonkwo's relative value conclusion is that the Trevian bond is: (LOS: los-06-03-g)
   - A. overpriced, because its model value at the comparable OAS exceeds its market price.
   - B. overpriced, because its OAS is below the 265 bps offered by the Corvid bond.
   - C. underpriced, because its OAS must exceed the 150 bps carried by comparable A-rated bonds.
4. If the model risk team's proposal is adopted and the Trevian price stays at 99.40, the OAS Okonkwo reports for Trevian will most likely: (LOS: los-06-03-h)
   - A. decrease.
   - B. remain unchanged.
   - C. increase.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The framework has three steps: generate the tree from the benchmark curve and the volatility assumption, apply the exercise decision at every node, and run backward induction (V6 p.136).
> Forward rates are needed because the value of the remaining cash flows at each future call date determines whether Trevian calls, and spot rates only give a single value today (V6 p.126).
> A is wrong because the tree is built from the default-free benchmark and credit and liquidity risk enter through the OAS added to every node (V6 p.144, p.145).
> C is wrong because the exercise test is applied at each call date before the value is passed one column left; testing only today reproduces the straight value.
> 2. **A.** Add 150 bps to every rate in Exhibit 2: Year 0 4.3000%; Year 1 5.8913% and 4.7531%; Year 2 7.1078%, 5.6544% and 4.5776%.
> Year 2: $105.40/1.071078 = 98.4055$; $105.40/1.056544 = 99.7592$; $105.40/1.045776 = 100.7864 \to$ called at 100.
> Year 1 upper: $(5.40 + 0.5 \times (98.4055 + 99.7592))/1.058913 = 98.6695$, not called.
> Year 1 lower: $(5.40 + 0.5 \times (99.7592 + 100))/1.047531 = 100.5026 \to$ called at 100.
> Year 0: $(5.40 + 0.5 \times (98.6695 + 100))/1.043 = 100.4168$, about 100.417.
> B is wrong because it adds the OAS but never applies the call rule, which gives the straight bond at a 150 bps spread, 100.838.
> C is wrong because it omits the OAS and values the callable on the government tree, 102.529, which prices Trevian as if it were default-free.
> 3. **C.** A higher spread lowers the model value, so a market price (99.40) below the model value at 150 bps (100.417) means the spread that reprices the bond is larger than 150 bps; solving at 15% volatility gives an OAS of about 200.6 bps (V6 p.145).
> A bond with a higher OAS than bonds of similar characteristics and credit quality is underpriced, or cheap (V6 p.146).
> A is wrong because it reverses the price-to-spread logic: a model value above the market price signals cheapness, not richness.
> B is wrong because Corvid is BB rated; its extra spread is compensation for credit risk, so no relative value conclusion can be drawn across ratings.
> 4. **A.** At a higher volatility assumption the call option is worth more, so the tree assigns a lower value to the callable at any given spread, and a smaller constant spread is needed to reprice the same 99.40 (V6 p.146, p.147).
> Solving the Trevian tree at 20% volatility gives an OAS of about 196.6 bps against about 200.6 bps at 15%.
> B is wrong because OAS is a model output that depends on the volatility assumption, even though the curve and the price are fixed.
> C is wrong because it reverses the direction, which would hold only if higher volatility made the call less valuable.

## Distractor design

- Q1: A moves credit from the spread into the tree (wrong framework variant); C applies the exercise test after discounting and only today (wrong node order).
- Q2: B adds the spread but omits the call rule (straight value at the OAS); C omits the spread (benchmark tree, default-free value).
- Q3: A reverses the price-spread relation (sign); B compares OAS across credit ratings (misread exhibit).
- Q4: B treats OAS as independent of the model's volatility input; C reverses the volatility-OAS direction (sign).
