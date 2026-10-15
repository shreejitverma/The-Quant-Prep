---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 5
title: "Lindqvist Kapital: A European Credit Overlay"
los: [los-06-05-a, los-06-05-b, los-06-05-c, los-06-05-d, los-06-05-e]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Lindqvist Kapital: A European Credit Overlay

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Astrid Lindqvist is chief investment officer of Lindqvist Kapital, a Stockholm asset manager that runs a credit overlay on its multi-asset funds using index and single-name CDS.
All contracts are documented under the Standard Europe Contract unless otherwise noted.
Lindqvist is preparing the quarterly report to the investment committee with her deputy, Jonas Ekberg.

The overlay has sold EUR 150 million of protection on the current series of the iTraxx Crossover index, which has 75 equally weighted high-yield constituents.
This quarter, one constituent, Baltic Ferrous, defaulted, and the settlement auction set its recovery rate at 30%.
Baltic Ferrous had also been a constituent of an earlier Crossover series, whose notional had been EUR 100 million with 50 constituents.

Two other developments affect the portfolio.
Tagus Energia, a Portuguese utility, used collective action clauses to impose a 25% reduction in principal on all bondholders, including those who voted against it.
Pioneer Freight, a US trucking company whose CDS are documented under the Standard North American Contract, reached an agreement with a group of its bondholders, who volunteered to extend the maturity of their bonds by two years in exchange for a higher coupon.
Neither company has filed for bankruptcy.

Ekberg tracks the credit curve of Nordhavn Shipping, a Danish shipowner facing a large vessel-financing maturity next year.

Exhibit 1: Nordhavn Shipping CDS spreads (bps)

| Maturity | 1 year | 3 years | 5 years | 10 years |
|---|---|---|---|---|
| Last quarter | 150 | 190 | 230 | 290 |
| Today | 520 | 470 | 390 | 330 |

For Fjell Telecom, Lindqvist expects spreads to widen by about 40 bps at every maturity over the next quarter as the company bids for new spectrum licenses.
She intends to trade EUR 20 million of notional.

Exhibit 2: Fjell Telecom CDS

| Maturity | Spread (bps) | Effective spread duration |
|---|---|---|
| 5 years | 180 | 4.5 |
| 10 years | 245 | 8.2 |

Ekberg then comments on index pricing.

Ekberg: "Suppose two CDS indexes have identical constituent single-name spreads.
The one whose constituents' defaults are more highly correlated will be more expensive to buy protection on."

Finally, Ekberg observes that the on-the-run iTraxx Main index trades at 95 bps, while the equally weighted average of the 125 constituents' single-name five-year spreads is 102 bps.
He estimates that the transaction costs of trading the index against all 125 single-name contracts would total about 6 bps.

## Questions

1. As a result of Baltic Ferrous's default, the payment Lindqvist Kapital makes on the current Crossover position and the position's remaining notional are closest to: (LOS: los-06-05-a)
   - A. EUR 1.40 million and EUR 148.0 million.
   - B. EUR 2.00 million and EUR 148.0 million.
   - C. EUR 1.05 million and EUR 148.5 million.
2. Which of the two developments is most likely a credit event under the relevant standard contract? (LOS: los-06-05-b)
   - A. Neither, because neither company filed for bankruptcy.
   - B. Only the Tagus Energia principal reduction.
   - C. Both, because each changes the terms of outstanding bonds.
3. The change in Nordhavn's credit curve in Exhibit 1 most likely indicates that: (LOS: los-06-05-c)
   - A. default has become more likely in later years than in earlier years.
   - B. the market now assumes a roughly constant hazard rate for Nordhavn.
   - C. near-term default risk has risen sharply, and if Nordhavn survives the near term, its conditional probability of default is lower.
4. The position that best expresses Lindqvist's view on Fjell, and its approximate gain if the view is correct, is to: (LOS: los-06-05-d)
   - A. buy five-year protection; gain of EUR 360,000.
   - B. sell ten-year protection; gain of EUR 656,000.
   - C. buy ten-year protection; gain of EUR 656,000.
5. Ekberg's statement about index pricing is most likely: (LOS: los-06-05-a)
   - A. correct.
   - B. incorrect, because less correlated defaults make index protection more expensive.
   - C. incorrect, because equal weighting makes default correlation irrelevant to index pricing.
6. The index trade Ekberg's observation supports, and its approximate profit on convergence after transaction costs, is to: (LOS: los-06-05-e)
   - A. sell protection on the index and buy protection on the constituents; about 1 bp.
   - B. buy protection on the index and sell protection on the constituents; about 1 bp.
   - C. buy protection on the index and sell protection on the constituents; about 7 bps.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Index CDS are equally weighted, so the defaulted constituent settles as a single-name CDS on $150 / 75 = 2.0$ million.
> As protection seller, Lindqvist pays $(1 - 0.30) \times 2{,}000{,}000 = 1{,}400{,}000$, and the index continues with $150 - 2 = 148.0$ million of notional.
> B is wrong because it pays the full per-entity notional, ignoring the 30% recovery rate (physical-settlement notional read as the net loss).
> C is wrong because it divides by 100, the CDX HY count: $150 / 100 = 1.5$, $0.70 \times 1.5 = 1.05$, remaining $148.5$ million.
> The earlier series' EUR 100 million and 50 constituents are irrelevant to the current position.
> 2. **B.** Restructuring is a credit event where recognized, including under the Standard Europe Contract, when it is involuntary or coercive; imposing a principal reduction on dissenting holders through collective action clauses is coercive.
> Pioneer's extension is voluntary, and in any case restructuring is not a credit event in the United States, where restructurings occur through bankruptcy.
> A is wrong because bankruptcy is only one of the three common credit events.
> C is wrong because a voluntary exchange agreed by bondholders is not a credit event, and US contracts do not recognize restructuring.
> 3. **C.** The curve has moved from upward sloping ($150 \to 290$ bps) to downward sloping ($520 \to 330$ bps), with the short end widening by $520 - 150 = 370$ bps and the long end by only $330 - 290 = 40$ bps.
> An inverted curve signals a greater probability of default in the near term, typical of severe near-term stress such as Nordhavn's refinancing need; survival through that period implies a lower conditional default probability afterward.
> A is wrong because it describes an upward-sloping curve, which was last quarter's shape.
> B is wrong because a roughly constant hazard rate produces a roughly flat curve, not a steeply inverted one.
> 4. **C.** The view is a parallel widening, a level trade, so buy protection; for the same spread change, longer-maturity CDS move more because of their higher duration.
> Gain on ten-year protection $= 0.0040 \times 8.2 \times 20{,}000{,}000 = 656{,}000$, versus $0.0040 \times 4.5 \times 20{,}000{,}000 = 360{,}000$ on five-year protection.
> A is wrong because the five-year contract captures less of the same parallel move (lower duration).
> B is wrong on sign: the protection seller is long credit and would lose EUR 656,000 if spreads widen.
> 5. **A.** Credit correlation is a key determinant of index CDS value; the more correlated the constituents' defaults, the more costly it is to buy protection on the combination.
> B is wrong because it reverses the relationship; a diverse group with low default correlation is cheaper to protect.
> C is wrong because equal weighting fixes each name's share of notional, not the joint behavior of defaults, so correlation still matters.
> 6. **B.** The index spread (95 bps) is below the average constituent spread (102 bps), so protection is cheap on the index and rich on the components.
> Buy protection on the index (pay 95 bps) and sell protection on the constituents (receive 102 bps), capturing $102 - 95 = 7$ bps on convergence, or about $7 - 6 = 1$ bp after costs.
> This is why index arbitrage opportunities are small: transaction costs absorb most of the profit.
> A is wrong because it reverses the legs, paying the rich spread and receiving the cheap one.
> C is wrong because it ignores the 6 bps of transaction costs.

## Distractor design

1. B: recovery rate ignored (full per-entity notional paid); C: wrong constituent count (CDX HY 100 instead of 75).
2. A: bankruptcy treated as the only credit event; C: voluntary US exchange counted, ignoring both the coercion test and the US exclusion of restructuring.
3. A: last quarter's upward-sloping shape read as today's; B: constant hazard rate (flat curve) confused with an inverted curve.
4. A: shorter maturity chosen despite lower duration for a parallel move; B: protection seller treated as gaining on widening (sign).
5. B: direction of the correlation effect reversed; C: equal weighting confused with independence of defaults.
6. A: index and constituent legs reversed; C: transaction costs omitted.
