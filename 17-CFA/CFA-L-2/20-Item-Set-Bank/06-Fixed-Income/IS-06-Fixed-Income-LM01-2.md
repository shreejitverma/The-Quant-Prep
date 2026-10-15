---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 1
title: "Corvina Bank Treasury: Swap Curves and Funding Stress"
los: [los-06-01-d, los-06-01-e, los-06-01-f, los-06-01-g]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Corvina Bank Treasury: Swap Curves and Funding Stress

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Rafael Quintero is head of treasury investments at Corvina Bank, a wholesale bank headquartered in Country M.
Country M's private sector borrows heavily in local currency, but its government issues few bonds and secondary trading in them is thin.
Most of Corvina's assets and liabilities reset off the market reference rate (MRR), and the bank hedges its balance sheet with interest rate swaps.
Quintero's deputy, Elena Brandt, is preparing a review of benchmark curves and trade ideas for the asset-liability committee.

Exhibit 1: Country M swap curve discount factors (annual)

| Maturity (years) | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Discount factor | 0.9690 | 0.9299 | 0.8852 | 0.8386 |

Exhibit 2: Country M par swap rates (annual fixed leg)

| Maturity (years) | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Swap rate | 3.20% | 3.69% | not shown | 4.46% |

Brandt asks an assistant to compute the missing three-year swap rate from Exhibit 1.
The committee has also asked her to justify why the bank values its Country M positions off the swap curve rather than the government curve.

Corvina's investment horizon for its surplus liquidity is two years.
Brandt proposes buying a four-year bond priced at par off the swap curve, with a 4.46% annual coupon, instead of a two-year par bond with a 3.69% annual coupon, and selling the four-year bond after two years.
She assumes the swap curve will be unchanged over the next two years and that the first coupon on either bond can be reinvested for one year at the one-year swap rate.

Corvina also holds bonds issued in Country L, a neighboring country with deep government and swap markets.

Exhibit 3: Country L government yields and swap rates

| Date | Maturity | Government yield | Swap rate |
|---|---|---|---|
| 12 months ago | 5 years | -0.35% | 0.05% |
| Today | 4 years | 0.31% | 0.55% |
| Today | 5 years | 0.40% | 0.62% |

Brandt is evaluating a senior bond issued by Talvera Bank, a Country L commercial bank, that matures in exactly 4.5 years.
Dealers quote the bond at an I-spread of 48 bps, and its Z-spread to the Country L government spot curve is 66 bps.
Brandt interpolates linearly wherever she needs a rate at the bond's maturity.

Finally, Quintero asks how Country L's money markets have behaved over the past six months.
He is concerned that rising stress among Country L banks could raise Corvina's own short-term funding costs.

Exhibit 4: Country L three-month money market rates

| Date | MRR | Treasury bill | Overnight indexed swap (OIS) |
|---|---|---|---|
| March | 0.42% | 0.10% | 0.30% |
| September | 0.78% | -0.05% | 0.28% |

Brandt's draft commentary states that the MRR-OIS spread is the measure the committee should track for money market risk and liquidity, and that the Z-spread belongs in the bond-pricing section of the report.

## Questions

1. The three-year swap rate the assistant should compute from Exhibit 1 is closest to: (LOS: los-06-01-e)
   - A. 4.12%.
   - B. 4.15%.
   - C. 6.05%.
2. The most appropriate justification for valuing Corvina's Country M positions off the swap curve is that: (LOS: los-06-01-e)
   - A. swap rates carry no bank credit risk, so they measure the time value of money more purely than government yields.
   - B. Country M's government bond market is thin relative to its private sector, and the liquid swap market supplies more maturities from which to build a benchmark curve.
   - C. the swap curve is a spot curve, so Corvina can discount cash flows without first bootstrapping it.
3. Based on Exhibit 3, the change in Country L's five-year swap spread over the past 12 months is best described as having: (LOS: los-06-01-f)
   - A. narrowed by 18 bps, indicating lower perceived credit and liquidity risk.
   - B. widened by 52 bps, indicating higher perceived credit and liquidity risk.
   - C. widened by 57 bps, indicating higher perceived credit and liquidity risk.
4. The yield to maturity of the Talvera Bank bond is closest to: (LOS: los-06-01-f)
   - A. 0.84%.
   - B. 1.07%.
   - C. 1.10%.
5. Based on Exhibit 4, the change in the MRR-OIS spread from March to September and its most likely interpretation is: (LOS: los-06-01-g)
   - A. a widening of 38 bps, signaling greater bank credit and liquidity risk.
   - B. a widening of 51 bps, signaling greater bank credit and liquidity risk.
   - C. a narrowing of 2 bps, signaling slightly lower bank credit and liquidity risk.
6. Under Brandt's assumptions, the annualized two-year horizon return on her proposed four-year bond is closest to: (LOS: los-06-01-d)
   - A. 3.68%.
   - B. 4.43%.
   - C. 5.13%.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The par swap equation gives $s_T = (1 - DF_T) / \sum_{t=1}^{T} DF_t$.
> $s_3 = (1 - 0.8852) / (0.9690 + 0.9299 + 0.8852) = 0.1148 / 2.7841 = 4.1234\%$, about 4.12%.
> B is wrong because it is the three-year spot rate implied by the discount factor, $(1/0.8852)^{1/3} - 1 = 4.15\%$; the swap rate is a par rate, not a spot rate.
> C is wrong because it omits the final discount factor from the fixed-leg annuity, $0.1148 / (0.9690 + 0.9299) = 6.05\%$.
> 2. **B.** Where the government market is illiquid or small relative to the private sector, the swap curve is the more relevant benchmark for the time value of money; swap markets are deep, need no underlying bond supply, and offer more maturity points, and banks that hedge with swaps value their balance sheets off that curve.
> A is wrong because swap rates are built off MRR, an unsecured bank lending rate, so they embed bank credit and liquidity risk; that premium is exactly what the swap spread measures.
> C is wrong because the swap curve is a par curve; its spot rates and discount factors must be derived from it, as in Question 1.
> 3. **A.** Swap spread $=$ swap rate minus same-maturity government yield.
> 12 months ago: $0.05\% - (-0.35\%) = 0.40\%$; today: $0.62\% - 0.40\% = 0.22\%$.
> Change $= 0.22\% - 0.40\% = -0.18\%$, a narrowing of 18 bps, which signals lower perceived credit and liquidity risk of bank counterparties relative to the sovereign.
> B is wrong because it drops the negative sign on the old government yield: $0.05\% - 0.35\% = -0.30\%$, so the change appears to be $0.22\% - (-0.30\%) = +0.52\%$.
> C is wrong because it tracks the swap rate alone ($0.62\% - 0.05\% = 0.57\%$), which moved with the general level of rates, not the spread.
> 4. **B.** Interpolate the swap curve to 4.5 years: $0.55\% + 0.5 \times (0.62\% - 0.55\%) = 0.585\%$.
> The I-spread is the bond yield minus the interpolated swap rate, so $y = 0.585\% + 0.48\% = 1.065\%$, about 1.07%.
> Equivalently, the interpolated government yield is $0.31\% + 0.5 \times 0.09\% = 0.355\%$, the interpolated swap spread is $0.23\%$, and $0.355\% + 0.23\% + 0.48\% = 1.065\%$.
> A is wrong because it adds the I-spread to the government yield ($0.355\% + 0.48\% = 0.835\%$), omitting the swap spread; the I-spread is quoted over the swap curve, not the government curve.
> C is wrong because it uses the unadjusted five-year swap rate ($0.62\% + 0.48\% = 1.10\%$) instead of interpolating to the bond's 4.5-year maturity.
> The 66 bp Z-spread is a decoy; it is measured against the government spot curve and is not used to rebuild the yield from swap quotes.
> 5. **A.** MRR-OIS in March: $0.42\% - 0.30\% = 0.12\%$; in September: $0.78\% - 0.28\% = 0.50\%$; change $= +0.38\%$, a 38 bp widening.
> A wider MRR-OIS spread means unsecured bank lending demands a larger premium over the expected overnight rate, signaling greater bank credit and liquidity risk.
> B is wrong because it is the change in the TED spread: $0.42\% - 0.10\% = 0.32\%$ to $0.78\% - (-0.05\%) = 0.83\%$, a 51 bp widening; the TED spread also mixes in the flight into bills that pushed the bill yield negative.
> C is wrong because it reads the change in the OIS rate ($0.28\% - 0.30\% = -0.02\%$) as the change in the spread.
> 6. **C.** The four-year par bond pays 4.46; the first coupon is reinvested at 3.20%: $4.46 \times 1.032 = 4.6027$.
> At the horizon it is a two-year bond, sold at the unchanged two-year rate of 3.69%: $\frac{4.46}{1.0369} + \frac{104.46}{(1.0369)^2} = 4.3013 + 97.1575 = 101.4588$.
> Proceeds $= 4.6027 + 4.46 + 101.4588 = 110.5215$; annualized return $= (110.5215/100)^{1/2} - 1 = 5.13\%$.
> The static upward-sloping curve lets the bond roll down to a lower yield, adding a capital gain to the higher coupon.
> A is wrong because it is the maturity-matched two-year bond: $3.69 \times 1.032 + 3.69 + 100 = 107.4981$, return $(1.074981)^{1/2} - 1 = 3.68\%$.
> B is wrong because it sells the bond at its original 4.46% yield (price 100), ignoring the rolldown: $(4.6027 + 4.46 + 100)/100 = 1.090627$, return $4.43\%$.

## Distractor design

1. B: spot rate from the discount factor reported as the swap rate (spot vs par); C: final discount factor omitted from the annuity (wrong formula variant).
2. A: swap rates wrongly treated as credit-risk-free (misstated content of MRR); C: swap curve mislabeled as a spot curve (par vs spot).
3. B: negative government yield treated as positive (sign); C: change in swap rate read as change in spread (misread exhibit).
4. A: I-spread added to the government curve (wrong benchmark); C: no interpolation to 4.5 years (period).
5. B: TED spread computed instead of MRR-OIS (wrong spread); C: change in OIS rate read as change in spread (misread exhibit).
6. A: maturity-matched bond's return (wrong strategy); B: sale at the original yield, rolldown gain ignored (static curve misapplied).
