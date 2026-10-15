---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 5
title: "Marlowe Street Capital: Canadian Credit Book"
los: [los-06-05-b, los-06-05-c, los-06-05-d, los-06-05-e]
difficulty: 3
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Marlowe Street Capital: Canadian Credit Book

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Helena Voss is the portfolio manager of Marlowe Street Capital, a Toronto hedge fund that trades single-name credit default swaps against corporate bonds and listed equities.
Dev Raman, a junior analyst, prepares the fund's weekly credit review.
All of Marlowe's CDS are US dollar contracts documented under the Standard North American Contract, with standardized coupons of 1% for investment-grade and 5% for high-yield reference entities, and all CDS quotes are per 100 of notional.

Marlowe holds $22 million of protection on Portage Mills, a pulp producer whose five-year senior unsecured notes are the reference obligation.
Portage missed a scheduled interest payment on those notes, and the grace period expired last week without payment.
Portage has not filed for bankruptcy and says it is negotiating with a group of its lenders.
The regional Determinations Committee met, and its members voted 11 to 4 that a failure to pay had occurred.
Raman writes in his review: "Because the committee has voted that a failure to pay occurred, a credit event has been declared, and settlement of our Portage protection should follow in about 30 days."

Voss is also reviewing Cormac Energy, a high-yield oil and gas producer whose credit quality has improved after two years of debt reduction.
Believing the improvement is largely complete and will hold, Voss sells $15 million of five-year protection on Cormac at the quotes in Exhibit 1.

Exhibit 1: Cormac Energy CDS quotes on the trade date

| Maturity | Credit spread (bps) | Effective spread duration |
|---|---|---|
| 3 years | 360 | 2.8 |
| 5 years | 430 | 4.6 |
| 7 years | 475 | 6.1 |

Two weeks after the trade, Cormac announces a large acquisition financed with new debt, and its five-year credit spread jumps to 580 bps.
Raman assumes that the effective spread duration of Marlowe's contract is still 4.6.

Finally, Voss asks Raman to study Keswick Rail, a Canadian freight railway rated BB whose shares trade at CAD 42.50.
Keswick has announced a deeply discounted rights offering that will raise CAD 1.2 billion, all of which will be used to repay bank loans and redeem bonds.

Exhibit 2: Keswick Rail selected data

| Item | Before rights offering | After rights offering (pro forma) |
|---|---|---|
| Total debt (CAD billions) | 3.8 | 2.6 |
| Shares outstanding (millions) | 120 | 165 |
| Debt to EBITDA | 4.5x | 3.1x |
| Annual dividend per share (CAD) | 1.10 | 1.10 |

Raman expects Keswick's share price to fall as the new shares dilute existing shareholders.
He also expects Keswick's CDS spread to narrow materially as its leverage declines.
Voss wants a trade in which both the equity leg and the credit leg profit if Raman's expectations prove correct.

## Questions

1. Raman's statement about Portage Mills is most likely: (LOS: los-06-05-b)
   - A. correct.
   - B. incorrect, because a failure to pay is not a credit event unless Portage files for bankruptcy.
   - C. incorrect, because declaring a credit event requires a supermajority of at least 12 of the committee's 15 members.
2. At initiation of the Cormac contract, Marlowe most likely: (LOS: los-06-05-c)
   - A. received an upfront payment of 3.22% of notional, at a price of 96.78.
   - B. paid an upfront payment of 0.70% of notional, at a price of 100.70.
   - C. paid an upfront payment of 3.22% of notional, at a price of 103.22.
3. After Cormac's five-year spread moves to 580 bps, the price of the Cormac CDS and the change in value of Marlowe's position are closest to: (LOS: los-06-05-d)
   - A. 96.32 and a gain of $1,035,000.
   - B. 99.20 and a loss of $225,000.
   - C. 96.32 and a loss of $1,035,000.
4. The trade that best meets Voss's objective for Keswick is to: (LOS: los-06-05-e)
   - A. short Keswick shares and buy protection on Keswick.
   - B. short Keswick shares and sell protection on Keswick.
   - C. buy Keswick shares and sell protection on Keswick.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Each regional Determinations Committee has 15 members (10 sell-side and 5 buy-side), and declaring a credit event requires a supermajority of 12 votes.
> An 11 to 4 vote falls one vote short, so no credit event has been declared, and the 30-day settlement clock has not started.
> The underlying facts would qualify: a missed scheduled payment after the grace period is a failure to pay, whether or not the company files for bankruptcy.
> A is wrong because it treats a simple majority of the committee as sufficient.
> B is wrong because bankruptcy is only one of the three common credit events; failure to pay is a credit event in its own right.
> 2. **C.** Cormac is high yield, so the standardized coupon is 5%.
> Upfront premium $\approx (\text{spread} - \text{coupon}) \times \text{duration} = (0.0430 - 0.0500) \times 4.6 = -0.0322$, or $-3.22\%$ of notional.
> A negative upfront means the protection seller pays the buyer, so Marlowe, the seller, paid 3.22% (about 483,000 dollars on 15 million of notional), because it will collect a 5% running coupon on a credit whose spread is only 4.30%.
> Price per 100 $= 100 - (-3.22) = 103.22$.
> A is wrong because it keeps the buyer as the payer regardless of sign and subtracts the absolute premium: $100 - 3.22 = 96.78$.
> B is wrong because it omits the duration, using only the one-year spread shortfall: $0.0430 - 0.0500 = -0.70\%$, price $100.70$.
> The three-year and seven-year quotes in Exhibit 1 are decoys; the contract is five years.
> 3. **C.** New upfront premium $= (0.0580 - 0.0500) \times 4.6 = 0.0368$, or $3.68\%$, now positive (the buyer pays), so the price is $100 - 3.68 = 96.32$.
> The price has fallen by $103.22 - 96.32 = 6.90$ points, which equals the spread change times duration: $0.0150 \times 4.6 = 0.0690$.
> Marlowe sold protection, so it is long Cormac credit and loses when the spread widens: $0.0150 \times 4.6 \times 15{,}000{,}000 = 1{,}035{,}000$.
> Closing the position would require buying protection at the new, higher upfront, locking in the loss.
> A is wrong because it treats the CDS price like a bond sold short, reading the fall from 103.22 to 96.32 as a gain for the seller; a lower CDS price means protection has become more expensive, which hurts the protection seller.
> B is wrong because it omits the duration: price $= 100 - (0.0580 - 0.0500) \times 100 = 99.20$ and loss $= 0.0150 \times 15{,}000{,}000 = 225{,}000$.
> 4. **B.** Raman expects the equity to fall, so the equity leg is a short position in Keswick shares.
> He expects the CDS spread to narrow as debt falls from CAD 3.8 billion to CAD 2.6 billion and debt to EBITDA from 4.5x to 3.1x, so the credit leg is long Keswick credit, which in single-name CDS means selling protection.
> Both legs gain if the dilution depresses the share price and the deleveraging lowers the probability of default.
> This is the mirror image of the curriculum's leveraged-buyout trade (buy the stock, buy protection), in which a change in capital structure moves equity and credit in opposite directions.
> A is wrong because buying protection is short credit and loses as the spread narrows; it assumes that bad news for shareholders must also be bad news for creditors.
> C is wrong because buying the shares loses from the dilution Raman expects; it reads the deleveraging as good for both classes of investor.
> The unchanged dividend per share is a decoy; it does not change either expected move.

## Distractor design

1. A: simple majority of the Determinations Committee treated as sufficient; B: bankruptcy treated as the only credit event.
2. A: payer fixed as the buyer and the absolute premium subtracted (sign); B: duration omitted from the upfront premium.
3. A: CDS price read like a short bond position, so the protection seller is credited with a gain on widening; B: duration omitted from both the price and the profit.
4. A: equity and credit assumed to move in the same direction, so protection is bought; C: dilution ignored, so the equity leg is long.
