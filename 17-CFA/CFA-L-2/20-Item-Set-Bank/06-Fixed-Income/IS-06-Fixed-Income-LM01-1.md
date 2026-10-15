---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 1
title: "Lakeshore Mutual Life: Rebuilding the Valuation Curve"
los: [los-06-01-a, los-06-01-b, los-06-01-c, los-06-01-h]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Lakeshore Mutual Life: Rebuilding the Valuation Curve

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ingrid Lund, CFA, is a fixed-income analyst at Lakeshore Mutual Life, a Canadian life insurer that funds long-dated annuity liabilities with default-free sovereign bonds.
Lakeshore's chief investment officer, Marit Olsen, has asked Lund to rebuild the insurer's valuation curve before the quarterly asset-liability committee meeting.
Lund starts from the annual-coupon par curve of on-the-run sovereign bonds shown in Exhibit 1.
She has already bootstrapped the one- to three-year spot rates and still needs the four-year spot rate.

Exhibit 1: Sovereign par and spot rates (annual compounding)

| Maturity (years) | Par rate | Spot rate |
|---|---|---|
| 1 | 2.00% | 2.00% |
| 2 | 3.00% | 3.02% |
| 3 | 3.90% | 3.95% |
| 4 | 4.60% | not yet computed |
| 5 | 5.10% | not yet computed |

The committee is considering Bond K as a match for a block of annuity payments.
Bond K is a default-free sovereign bond with exactly three years to maturity and a 6.00% annual coupon.
Lund prices Bond K off the spot rates in Exhibit 1 and then solves for its yield to maturity.
Exhibit 2 summarizes other data Lund collected for the meeting.

Exhibit 2: Supplementary data

| Item | Value |
|---|---|
| Three-month sovereign bill yield | 1.85% |
| Bond K coupon (annual) | 6.00% |
| Bond K remaining maturity | 3.00 years |
| Duration of the annuity block | 11.4 years |

Lund plans to show the committee what Bond K would earn over the coming year under two different assumptions about how the curve evolves.
Under the first assumption, spot rates evolve exactly as implied by today's forward curve.
Under the second assumption, the spot curve one year from now is identical to today's curve.
She also wants to quote the rate that Lakeshore could lock in today for a two-year loan beginning one year from now, because a large premium receipt is expected in twelve months.

Olsen and Lund then discuss the rate outlook.
Lund's economics team expects the central bank to pause its tightening cycle.
Lund accepts the market's implied one-year rates for the next two years.
However, she projects that the one-year spot rate two years from today will be 5.25%, and she asks whether that projection changes her view of a three-year sovereign zero-coupon bond.

Olsen responds with the following comment.

"Even if every investor expected the one-year rate to stay at 2.00% forever, our curve would still slope upward."
"Buyers of long bonds demand compensation for price risk, and that compensation grows with maturity."
"That is why I never read the forward curve as a clean forecast of future spot rates."

Lund notes that Lakeshore, like its peers, is required by its regulator to match long liabilities with long assets.
She wonders aloud whether that constraint also shapes the curve, and Olsen agrees to take the question up at a later meeting.

## Questions

1. Using Exhibit 1, the four-year spot rate is closest to: (LOS: los-06-01-b)
   - A. 4.60%.
   - B. 4.70%.
   - C. 6.96%.
2. The rate Lakeshore could lock in today for a two-year loan beginning one year from now is closest to: (LOS: los-06-01-a)
   - A. 4.05%.
   - B. 4.94%.
   - C. 5.84%.
3. The yield to maturity of Bond K is closest to: (LOS: los-06-01-a)
   - A. 2.99%.
   - B. 3.88%.
   - C. 3.95%.
4. Under Lund's first assumption, the one-year holding-period return on Bond K is closest to: (LOS: los-06-01-c)
   - A. 2.00%.
   - B. 3.88%.
   - C. 5.53%.
5. Based on Lund's projection for the one-year spot rate two years from today, the three-year sovereign zero-coupon bond is most likely: (LOS: los-06-01-c)
   - A. undervalued.
   - B. fairly valued.
   - C. overvalued.
6. Olsen's comment is most consistent with the: (LOS: los-06-01-h)
   - A. unbiased expectations theory.
   - B. liquidity preference theory.
   - C. segmented markets theory.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Bootstrap with the four-year par rate as the coupon and the spot rates already found: $1 = \frac{0.046}{1.02} + \frac{0.046}{(1.0302)^2} + \frac{0.046}{(1.0395)^3} + \frac{1.046}{(1+z_4)^4}$.
> The three coupon present values are $0.0451 + 0.0433 + 0.0410 = 0.1294$, so $(1+z_4)^4 = 1.046 / (1 - 0.1294) = 1.046 / 0.8706 = 1.2015$ and $z_4 = 1.2015^{1/4} - 1 = 4.6954\%$, about 4.70%.
> A is wrong because it takes the par rate as the spot rate; beyond one year on an upward-sloping curve the spot rate sits above the par rate because the par bond's coupons are discounted at lower early spot rates.
> C is wrong because it reports the marginal one-year forward rate from year 3 to year 4, $1.20146 / (1.0395)^3 - 1 = 1.20146 / 1.12324 - 1 = 6.96\%$, instead of the average (spot) rate.
> 2. **B.** The loan starts at $A = 1$ and has tenor $B - A = 2$, so it links $z_1$ and $z_3$: $f_{1,2} = \left[\frac{(1.0395)^3}{1.02}\right]^{1/2} - 1 = (1.1232 / 1.02)^{1/2} - 1 = (1.1012)^{1/2} - 1 = 4.94\%$.
> A is wrong because it is the one-year loan beginning in one year, $f_{1,1} = (1.0302)^2 / 1.02 - 1 = 4.05\%$ (tenor misread).
> C is wrong because it is the one-year loan beginning in two years, $f_{2,1} = (1.0395)^3 / (1.0302)^2 - 1 = 5.84\%$ (start date and tenor swapped).
> 3. **B.** Price off the spot curve: $P = \frac{6}{1.02} + \frac{6}{(1.0302)^2} + \frac{106}{(1.0395)^3} = 5.8824 + 5.6534 + 94.3697 = 105.9054$.
> Solving $105.9054 = \frac{6}{1+y} + \frac{6}{(1+y)^2} + \frac{106}{(1+y)^3}$ gives $y = 3.8770\%$, about 3.88%.
> The YTM is a cash-flow-weighted average of the spot rates, pulled toward $z_3$ because the year-3 flow is by far the largest, yet it stays below $z_3$ because the coupons are discounted at the lower early spots.
> A is wrong because it is the equally weighted average of the three spot rates, $(2.00 + 3.02 + 3.95)/3 = 2.99\%$, which ignores the dominant final cash flow.
> C is wrong because it sets the YTM equal to the final spot rate, ignoring the weight of the coupons.
> 4. **A.** If spot rates evolve as the forwards imply, the one-year rate in one year is $f_{1,1} = 4.0502\%$ and the two-year rate is $f_{1,2} = 4.9389\%$.
> Bond K's price in one year is $\frac{6}{1.040502} + \frac{106}{(1.049389)^2} = 5.7664 + 96.2571 = 102.0235$.
> Return $= (6 + 102.0235)/105.9054 - 1 = 2.00\%$, exactly the one-year spot rate, as every default-free bond must earn when the forward curve is realized.
> B is wrong because it assumes the one-year return equals the YTM.
> C is wrong because it is the return under the second (static curve) assumption: price $= \frac{6}{1.02} + \frac{106}{(1.0302)^2} = 5.8824 + 99.8764 = 105.7587$, return $(6 + 105.7587)/105.9054 - 1 = 5.53\%$, which is the rolldown gain, not the forward-consistent return.
> 5. **A.** The relevant market rate is the implied forward $f_{2,1} = (1.0395)^3/(1.0302)^2 - 1 = 5.84\%$.
> Lund's projected one-year spot rate for that period, 5.25%, is below the forward, so the market is discounting the year-3 cash flow at a higher rate than she believes is warranted.
> The market price is below her intrinsic value, so the zero is undervalued and she expects to earn more than the one-period rate by holding it.
> B is wrong because a bond is fairly valued only if the projected spot rates equal the forwards, and the market-consistent price off today's curve is not the same as fair value to an investor with a different view.
> C is wrong because it compares the 5.25% projection with today's three-year spot rate of 3.95% instead of with the 5.84% forward rate that the market has priced in.
> 6. **B.** Olsen argues that the curve would slope upward even with flat rate expectations because investors demand a premium for price risk that increases with maturity, which makes forwards upward-biased predictors of future spot rates: liquidity preference.
> A is wrong because unbiased expectations theory treats forwards as unbiased forecasts and assumes risk-neutral investors, the view Olsen explicitly rejects.
> C is wrong because the asset-liability matching constraint appears in Lund's aside, not in Olsen's comment, and segmented markets theory says nothing about a premium that rises with maturity.

## Distractor design

1. A: par rate read as spot rate (par vs spot); C: marginal forward $f_{3,1}$ reported instead of the spot rate (spot vs forward).
2. A: tenor misread as one year ($f_{1,1}$); C: start date and tenor swapped ($f_{2,1}$), the subscript trap.
3. A: equally weighted average of spot rates (wrong weighting); C: YTM set equal to the final spot rate (coupon effect ignored).
4. B: one-year return equated with YTM (restrictive YTM assumptions ignored); C: static-curve rolldown return used instead of the forward-consistent return (wrong scenario).
5. B: market-consistent price confused with investor fair value; C: projection compared with today's spot rate instead of the forward rate (spot vs forward).
6. A: theory Olsen explicitly rejects (risk neutrality); C: theory triggered by the regulatory aside rather than the comment (misread vignette).
