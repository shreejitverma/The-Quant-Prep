---
type: cfa-itemset
topic: "Alternative Investments"
topic_code: "08"
topic_slug: "08-Alternative-Investments"
lm: 1
title: "Verhoeven Family Office Commodity Sleeve Review"
los: [los-08-01-e, los-08-01-g, los-08-01-i, los-08-01-j]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/alternative-investments]
---

# Verhoeven Family Office Commodity Sleeve Review

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

The Verhoeven Family Office manages the proceeds from the family's sale of an oilfield services company.
Its remaining private holdings are still concentrated in energy businesses.
Chiara Bellandi, CFA, oversees the office's commodity sleeve, and Pieter Verhoeven, a family trustee, chairs the investment committee.
Bellandi is preparing her quarterly review as of 30 September.

The sleeve holds only fully collateralized long futures positions.
Collateral equal to the full notional value of each position is invested in Treasury bills, which have yielded 4.5% annualized during the quarter.
Bellandi first reviews the market data in Exhibit 1.

Exhibit 1: Spot and futures prices, 30 September

| Commodity | Unit | Spot | Near futures | Far futures |
|---|---|---|---|---|
| Copper | USD per pound | 4.462 | 4.415 | 4.478 |
| WTI crude oil | USD per barrel | 78.90 | 78.25 | 76.80 |
| Natural gas | USD per MMBtu | 2.840 | 3.460 | 3.120 |

On 31 July, the sleeve bought copper futures in the December contract, which is the near contract in Exhibit 1.
The sleeve has held the position since then without adding to it.
On 30 September, Bellandi rolls the entire copper position from the December contract into the March contract, the far contract in Exhibit 1.
Exhibit 2 shows copper prices on the date the position was established.

Exhibit 2: Copper prices, 31 July (USD per pound)

| Item | Price |
|---|---|
| Spot price | 4.265 |
| December futures price | 4.180 |

Six months ago, the office's external overlay manager, Dmitri Rasko, sold a variance swap on WTI crude oil futures prices.
Rasko expected realized volatility to remain below the level fixed in the swap.
The swap matured on 30 September, and its terms and outcome are summarized in Exhibit 3.

Exhibit 3: WTI variance swap summary

| Item | Value |
|---|---|
| Family office position | Seller of variance |
| Variance notional | USD 5,000 per variance point |
| Fixed (strike) volatility | 24.0% |
| Realized volatility over the life of the swap | 36.0% |
| Implied volatility on 30 September | 27.0% |
| Cap on the variance difference | 400 variance points |

Variance points are calculated from annualized volatilities expressed in percent, so a volatility of 20% corresponds to 400 variance points.

Finally, the committee must adopt a benchmark for the sleeve.
Verhoeven wants a benchmark that will not add to the family's concentration in energy, even if energy prices rise sharply relative to other commodities.
Bellandi shortlists two broad indexes.
Index K holds 24 commodities weighted by the value of world production, rolls monthly into the nearby contract, and rebalances annually.
Index L holds 23 commodities weighted by a combination of production and futures market liquidity, with a 33% cap on any sector and a 2% floor on any commodity, rolls into the front-month contract, and rebalances annually.

Verhoeven comments: "I have read that the major commodity indexes are more than 70% correlated with one another, so I doubt the choice between them matters for our energy concentration."

## Questions

1. Based on Exhibit 1, which commodity has a negative basis and a positive calendar spread? (LOS: los-08-01-e)
   - A. Copper
   - B. WTI crude oil
   - C. Natural gas
2. The two-month total return on the copper position, measured through the 30 September roll, is closest to: (LOS: los-08-01-g)
   - A. 3.94%.
   - B. 4.95%.
   - C. 7.80%.
3. Based on Exhibit 3, at maturity of the variance swap the family office will: (LOS: los-08-01-i)
   - A. pay USD 2,000,000.
   - B. receive USD 2,000,000.
   - C. pay USD 3,600,000.
4. The most appropriate response to Verhoeven's comment is that: (LOS: los-08-01-j)
   - A. Index K is the better benchmark, because weighting by the value of world production gives the largest weights to the commodities with the deepest markets and therefore the best diversification.
   - B. the choice does not matter, because the high correlation among major indexes means that their construction has little effect on energy exposure.
   - C. Index L is the better benchmark, because its sector cap limits the energy weight, whereas production-value weights allow energy to dominate and to grow as energy prices rise.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Basis $=$ spot $-$ near futures and calendar spread $=$ near futures $-$ far futures.
> Natural gas: basis $= 2.840 - 3.460 = -0.6200$ and calendar spread $= 3.460 - 3.120 = +0.3400$, so the front of the curve (spot to near) is in contango while the near-to-far segment is in backwardation, a humped curve typical of a winter contract.
> Copper: basis $= 4.462 - 4.415 = +0.0470$ and calendar spread $= 4.415 - 4.478 = -0.0630$.
> WTI: basis $= 78.90 - 78.25 = +0.6500$ and calendar spread $= 78.25 - 76.80 = +1.4500$, a curve in backwardation throughout.
> A is wrong because it swaps the two definitions, treating near minus far ($-0.0630$) as the basis and spot minus near ($+0.0470$) as the calendar spread.
> B is wrong because it computes the basis as futures minus spot ($78.25 - 78.90 = -0.6500$), reversing the sign of a positive basis.
> 2. **B.** Price return uses the futures contract held, not the physical spot price: $(4.415 - 4.180)/4.180 = 5.6220\%$.
> Roll return with the whole position rolled: $(4.415 - 4.478)/4.415 \times 100\% = -1.4270\%$, negative because the December-to-March segment is in contango.
> Collateral return: $4.5\% \times 2/12 = 0.7500\%$.
> Total return $= 5.6220\% - 1.4270\% + 0.7500\% = 4.9451\% \approx 4.95\%$.
> A is wrong because it measures price return with the spot prices, $(4.462 - 4.265)/4.265 = 4.6190\%$, giving $4.6190\% - 1.4270\% + 0.7500\% = 3.9420\%$; physical spot prices are not the prices of the position, and the index convention is front-month futures prices.
> C is wrong because it treats the roll return as positive, $5.6220\% + 1.4270\% + 0.7500\% = 7.7990\%$; rolling into a dearer far contract produces a negative roll return.
> 3. **A.** Fixed variance $= 24.0^2 = 576$ points and realized variance $= 36.0^2 = 1{,}296$ points, so the variance difference is $1{,}296 - 576 = 720$ points.
> The difference exceeds the 400-point cap, so settlement uses 400 points: $5{,}000 \times 400 = \text{USD }2{,}000{,}000$.
> Realized variance exceeded fixed variance, so the buyer is paid and the family office, as seller, pays.
> The 27.0% implied volatility on the maturity date is a decoy; a variance swap settles on realized variance over its life.
> B is wrong because it reverses the payment direction: a positive realized-minus-fixed difference pays the buyer, not the seller.
> C is wrong because it ignores the cap and settles on the full 720 points: $5{,}000 \times 720 = \text{USD }3{,}600{,}000$.
> 4. **C.** Production-value weighting gives energy a dominant weight (historically up to 80% in the S&P GSCI), and because the weights drift with prices, a sharp relative rise in energy prices raises energy's weight further.
> A 33% sector cap, as in the BCOM-style construction of Index L, limits energy's weight regardless of its production value, which meets Verhoeven's objective.
> A is wrong because production-value weighting concentrates, rather than diversifies, the index in energy, which would add to the family's existing energy concentration.
> B is wrong because the high correlation among major indexes does not make construction irrelevant: weighting methodology determines sector exposure, and it is one of the main construction choices that drives index returns.

## Distractor design

1. A: basis and calendar spread definitions swapped; B: basis sign reversed (futures minus spot).
2. A: misread exhibit (physical spot prices used for price return instead of the futures contract held); C: roll return sign reversed in a contango roll.
3. B: payment direction reversed for the seller of variance; C: variance cap ignored (the implied volatility is a misread-exhibit decoy).
4. A: production-value weighting read as diversifying rather than concentrating in energy; B: true fact (high index correlation) used to dismiss the effect of construction on sector exposure.
