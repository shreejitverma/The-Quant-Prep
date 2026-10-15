---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 5
title: "Solent Credit Opportunities: Pricing and Relative Value"
los: [los-06-05-c, los-06-05-d, los-06-05-e]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Solent Credit Opportunities: Pricing and Relative Value

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Callum Adeyemi, CFA, manages Solent Credit Opportunities, a London hedge fund that trades single-name CDS, corporate bonds, and listed equities.
Ines Moreau, a quantitative analyst, supports him with pricing work.
All contracts use the standardized coupons of 1% for investment-grade and 5% for high-yield reference entities, and all quotes are for $100 of notional.

Nine months ago, Solent sold $25 million of five-year protection on Varga Chemicals, a high-yield issuer.
At that time the Varga contract was quoted at a price of 96.40 per 100 par, and its effective spread duration was 4.5.
Today Varga's five-year credit spread is 640 bps, and the effective spread duration of Solent's contract has declined to 3.9.
Varga's one-year CDS currently trades at 710 bps.
The widening followed a guidance cut, and Adeyemi is considering whether to close the Varga position with an offsetting contract rather than hold it to maturity.
Solent's contracts are centrally cleared, so an offsetting trade with any dealer would terminate the exposure.

Adeyemi now wants to buy five-year protection on Oakhurst Utilities, an investment-grade issuer, as a hedge against the fund's utility bond holdings.
Oakhurst's five-year credit spread is 65 bps and the effective spread duration is 4.6.

Moreau is also analyzing Pell Shipping, an investment-grade issuer whose one-year CDS trades at 180 bps.
She makes the following statement to Adeyemi.

Moreau: "Treating the one-year contract as a single-period CDS with no time value and a 40% expected recovery rate, I can back out Pell's one-year probability of default.
If I then assume the hazard rate stays constant, I can extend it to a cumulative two-year default probability."

Exhibit 1: Thornbury Homes, five-year instruments

| Instrument | Quote |
|---|---|
| Senior unsecured bond, trading close to par | Yield 7.15% |
| Five-year CDS spread | 4.35% |
| Market reference rate (MRR) | 3.20% |
| Thornbury equity, dividend yield | 2.40% |

Adeyemi notes that the bond has no embedded options and asks Moreau which relative-value trade, if any, the Thornbury quotes support if the credit spreads in the two markets converge.

Finally, a contact tells Adeyemi that a private equity sponsor is preparing to take Halvorsen Leisure private.
The sponsor would offer a premium to the current share price for all of Halvorsen's public equity and would fund the purchase mostly with new senior debt issued by Halvorsen itself.
Halvorsen currently has modest leverage and an investment-grade rating, and its shares trade at 14.2 times earnings.
Adeyemi wants a trade in which both legs benefit if the buyout is completed.

## Questions

1. The Varga credit spread implied by the price quoted when Solent entered the contract is closest to: (LOS: los-06-05-c)
   - A. 420 bps.
   - B. 580 bps.
   - C. 860 bps.
2. At initiation of the Oakhurst contract, Solent will most likely: (LOS: los-06-05-c)
   - A. pay an upfront premium of 1.61% of notional, at a price of 98.39.
   - B. receive an upfront premium of 2.99% of notional, at a price of 102.99.
   - C. receive an upfront premium of 1.61% of notional, at a price of 101.61.
3. If Solent closes its Varga position today with an offsetting contract, the result is closest to: (LOS: los-06-05-d)
   - A. a gain of $585,000.
   - B. a loss of $675,000.
   - C. a loss of $585,000.
4. Following the method Moreau describes, Pell's cumulative probability of default over two years is closest to: (LOS: los-06-05-c)
   - A. 5.91%.
   - B. 6.00%.
   - C. 8.80%.
5. The Thornbury quotes in Exhibit 1 are best described as a: (LOS: los-06-05-e)
   - A. negative basis; buy the bond and buy protection to capture about 40 bps.
   - B. positive basis; sell protection and short the bond to capture about 115 bps.
   - C. positive basis; sell protection and short the bond to capture about 40 bps.
6. The trade that best meets Adeyemi's objective for Halvorsen is to: (LOS: los-06-05-e)
   - A. buy Halvorsen shares and sell protection on Halvorsen.
   - B. buy Halvorsen shares and buy protection on Halvorsen.
   - C. short Halvorsen shares and buy protection on Halvorsen.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Upfront premium % $= 100 - \text{price} = 100 - 96.40 = 3.60\%$, positive, so the protection buyer paid it (the spread exceeds the 5% high-yield coupon).
> Credit spread $= \text{coupon} + \dfrac{\text{upfront}}{\text{duration}} = 5.00\% + \dfrac{3.60\%}{4.5} = 5.00\% + 0.80\% = 5.80\%$, or 580 bps.
> A is wrong because it treats a price below 100 as a seller-paid upfront and subtracts: $5.00\% - 0.80\% = 4.20\%$.
> C is wrong because it adds the upfront to the coupon without amortizing it over the duration: $5.00\% + 3.60\% = 8.60\%$.
> 2. **C.** Oakhurst is investment grade, so the coupon is 1%.
> Upfront premium $= (0.0065 - 0.0100) \times 4.6 = -0.0161$, or $-1.61\%$; negative means the protection seller pays the buyer, so Solent, the buyer, receives 1.61%.
> Price $= 100 - (-1.61) = 101.61$.
> A is wrong because it keeps the buyer as payer regardless of sign and subtracts the absolute premium ($100 - 1.61 = 98.39$).
> B is wrong because it multiplies the full spread by duration ($0.0065 \times 4.6 = 2.99\%$), ignoring the standardized coupon.
> 3. **C.** Solent sold protection at a 580 bps spread, so it is long Varga credit and loses when the spread widens.
> Spread change $= 640 - 580 = 60$ bps; loss $= 0.0060 \times 3.9 \times 25{,}000{,}000 = 585{,}000$.
> Solent closes by buying protection at the now higher upfront premium, locking in the loss.
> A is wrong on sign: widening benefits the protection buyer, not the seller.
> B is wrong because it uses the initiation duration of 4.5 instead of the current 3.9: $0.0060 \times 4.5 \times 25{,}000{,}000 = 675{,}000$.
> 4. **A.** One-period spread $\approx (1 - \text{RR}) \times \text{POD}$, so $\text{POD} = 0.0180 / (1 - 0.40) = 0.0300$.
> With a constant 3% hazard, two-year survival $= 0.97^2 = 0.9409$ and cumulative POD $= 1 - 0.9409 = 0.0591$, or 5.91%.
> B is wrong because it adds the two annual hazard rates ($3\% + 3\% = 6.00\%$), ignoring conditional survival.
> C is wrong because it divides the spread by the recovery rate instead of the loss rate ($0.018 / 0.40 = 4.5\%$), then compounds correctly: $1 - 0.955^2 = 0.0880$.
> 5. **C.** Bond credit spread $= 7.15\% - 3.20\% = 3.95\%$.
> Basis $= \text{CDS spread} - \text{bond credit spread} = 4.35\% - 3.95\% = +0.40\%$, positive, because credit risk is priced higher in the CDS market.
> Sell protection (collect the rich CDS spread) and short the bond (pay away the cheaper bond credit spread), hedging interest rate risk; convergence captures about 40 bps.
> A is wrong because it labels the basis negative and applies the negative-basis trade, which would lose the 40 bps if the spreads converge.
> B is wrong because it computes $4.35\% - 3.20\% = 1.15\%$, subtracting MRR from the CDS spread instead of comparing the two credit spreads.
> 6. **B.** The buyout premium raises Halvorsen's share price, so buy the shares.
> Funding the purchase with new debt issued by Halvorsen raises its leverage and default probability, widening its CDS spread, so buy protection on Halvorsen; both legs gain if the deal completes.
> A is wrong because selling protection is long Halvorsen credit, which loses when the added debt widens the spread.
> C is wrong because shorting the shares loses as the premium bid lifts the price.

## Distractor design

1. A: upfront sign reversed (price below 100 read as seller-paid); C: upfront not amortized over duration.
2. A: payer fixed as the buyer and absolute premium subtracted; B: whole spread times duration, coupon ignored.
3. A: protection seller treated as gaining on widening (sign); B: initiation duration used instead of the current, shorter duration.
4. B: hazard rates added instead of survival compounded; C: spread divided by recovery rate instead of loss given default.
5. A: basis sign reversed and the wrong leg directions applied; B: MRR subtracted from the CDS spread (mismatched quantities).
6. A: bond intuition that a premium bid helps credit, so seller of protection; C: leverage read as bad for the target's equity, ignoring the buyout premium.
