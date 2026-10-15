---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 1
title: "Aldermoor Mutual: Locking a Reinvestment Rate and Carrying a Bond Forward"
los: [los-07-01-c, los-07-01-d]
difficulty: 4
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Aldermoor Mutual: Locking a Reinvestment Rate and Carrying a Bond Forward

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Aldermoor Mutual is a property and casualty insurer that manages its euro liquidity in-house.
Jonas Verhoeven, CFA, a portfolio manager, reports to Clara Lindqvist, the chief investment officer.
All market reference rates (MRRs) are annualized add-on rates on an actual/360 basis, and Verhoeven assumes no transaction costs.

Aldermoor expects a reinsurance recovery of EUR 75,000,000 in 60 days and plans to place it in a 90-day MRR deposit.
To lock in its reinvestment rate, Aldermoor enters a 2 x 5 forward rate agreement (FRA) today as the receive-fixed party, at the no-arbitrage FRA rate, on a notional of EUR 75,000,000.

Exhibit 1: MRR term structure on the FRA trade date

| Days | 30 | 60 | 90 | 150 | 180 |
|---|---|---|---|---|---|
| MRR | 3.10% | 3.20% | 3.28% | 3.42% | 3.48% |

Forty days after the trade date, Lindqvist asks for a mark-to-market of the FRA.

Exhibit 2: MRR term structure 40 days after the trade date

| Days | 20 | 50 | 60 | 90 | 110 | 150 |
|---|---|---|---|---|---|---|
| MRR | 3.45% | 3.52% | 3.55% | 3.61% | 3.66% | 3.78% |

Verhoeven also prepares a settlement illustration for the board.
He assumes that at FRA expiration the 90-day MRR fixes at 3.71% and that the contract specifies a settlement discount rate of 3.95%.

Aldermoor's second position concerns a euro government bond that is the cheapest-to-deliver issue for a futures contract expiring in 120 days.
The bond pays a 4.20% annual coupon semiannually on 180-day coupon periods, and 150 days have passed since the last coupon.
Verhoeven's pricing screen shows the bond's full price, which already includes accrued interest.

Exhibit 3: Bond and futures inputs today (per 100 par)

| Item | Value |
|---|---|
| Full (dirty) price of the bond | 99.86 |
| Next coupon | 2.10, paid in 30 days |
| Futures expiration | 120 days |
| Conversion factor | 0.8620 |
| Risk-free rate, annual compounding | 3.40% |
| Yield to maturity of the bond | 4.46% |
| Quoted futures price at yesterday's close | 113.90 |

Two months ago Aldermoor entered long forward contracts to buy EUR 30,000,000 par of this bond for delivery on the futures expiration date.
The contracts settle on the quoted (clean) price at delivery, and the agreed forward price was 96.40 per 100 par.
Lindqvist asks for the equilibrium quoted futures price and for the current value of the bond forward position, using the Exhibit 3 inputs.

Lindqvist is concerned that Verhoeven's screen reports a full price while the futures settle on clean prices.
She reminds him that accrued interest must be counted exactly once when carrying the bond and must be removed at delivery.

## Questions

1. Based on Exhibits 1 and 2, the value of Aldermoor's FRA position 40 days after the trade date is closest to: (LOS: los-07-01-c)
   - A. -EUR 28,153.
   - B. EUR 28,153.
   - C. -EUR 66,906.
2. Under Verhoeven's settlement assumptions, the FRA settlement at expiration is closest to: (LOS: los-07-01-c)
   - A. EUR 30,125 paid by Aldermoor.
   - B. EUR 30,423 paid by Aldermoor.
   - C. EUR 30,125 received by Aldermoor.
3. Based on Exhibit 3, the equilibrium quoted futures price is closest to: (LOS: los-07-01-d)
   - A. 113.47.
   - B. 114.69.
   - C. 115.52.
4. The current value of Aldermoor's long bond forward position is closest to: (LOS: los-07-01-d)
   - A. EUR 418,766.
   - B. EUR 423,459.
   - C. EUR 730,275.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** First price the FRA at initiation from $L_{60}$ and $L_{150}$, annualized over the 90-day underlying.
> $FRA_0 = \{[1 + 0.0342(150/360)]/[1 + 0.0320(60/360)] - 1\}/(90/360) = (1.014250/1.005333 - 1) \times 4 = 3.5477\%$.
> Forty days later the contract is a 20 x 110 day FRA, so the offsetting rate uses $L_{20}$ and $L_{110}$: $FRA_g = \{[1 + 0.0366(110/360)]/[1 + 0.0345(20/360)] - 1\}/(90/360) = 3.6996\%$.
> Aldermoor receives fixed, so its value is $-V_g = 75{,}000{,}000 \times (0.035477 - 0.036996)(90/360)/[1 + 0.0366(110/360)] = -28{,}468.21/1.011183 = -28{,}153.36$.
> Rates rose, so the receive-fixed position lost value.
> B is wrong because it reports the value to the pay-fixed counterparty.
> C is wrong because it rebuilds $FRA_g$ from the original 60-day and 150-day tenors on the new curve (3.9102%), giving $-66{,}906$.
> 2. **A.** The FRA is advanced set and advanced settled, and the contract names a settlement discount rate of 3.95%, so the discount uses $D_m$, not $L_m$.
> Receive-fixed settlement $= 75{,}000{,}000 \times (0.035477 - 0.0371)(90/360)/[1 + 0.0395(90/360)] = -30{,}422.75/1.009875 = -30{,}125.26$.
> MRR fixed above the locked rate, so Aldermoor pays; its deposit will earn the higher 3.71%, which offsets the payment.
> B is wrong because it pays the in-arrears amount of 30,422.75 at expiration without discounting.
> C is wrong because it treats Aldermoor as the pay-fixed party, which gains when rates rise.
> Discounting at $L_m$ instead of $D_m$ would give 30,143.17, a smaller trap not offered here.
> 3. **A.** The screen shows the full price, so $B_0 + AI_0 = 99.86$ already; accrued interest is $AI_0 = (150/180)(2.10) = 1.75$ and the clean price is 98.11.
> $\text{FV}(B_0 + AI_0) = 99.86(1.034)^{120/360} = 100.9792$.
> The coupon of 2.10 in 30 days is a carry benefit: $FVCI = 2.10(1.034)^{90/360} = 2.1176$, and accrual restarts so $AI_T = (90/180)(2.10) = 1.05$.
> $Q_0 = (1/0.8620)(100.9792 - 1.05 - 2.1176) = 97.8115/0.8620 = 113.4705$.
> B is wrong because it omits $AI_T$, although the futures settles on the clean price: $(100.9792 - 2.1176)/0.8620 = 114.6886$.
> C is wrong because it adds accrued interest to a price that already includes it, carrying $99.86 + 1.75 = 101.61$ and giving 115.5234.
> The yield to maturity and yesterday's futures quote are decoys.
> 4. **A.** A forward on this specific bond settles on the clean price with no conversion factor, and today's no-arbitrage clean forward price for the same delivery date is $F_t = \text{FV}(B_0 + AI_0) - AI_T - FVCI = 97.8115$, which equals $Q_0 \times CF$ from Question 3.
> $V_t = (97.8115 - 96.40)/(1.034)^{120/360} = 1.4115/1.011207 = 1.3959$ per 100 par.
> Position value $= 0.0139589 \times 30{,}000{,}000 = \text{EUR }418{,}766$.
> B is wrong because it does not discount the locked-in difference from delivery to today: $0.014115 \times 30{,}000{,}000 = 423{,}459$.
> C is wrong because it uses the full forward price $F_t + AI_T = 98.8615$ against a clean contract price, giving 730,275.

## Distractor design

1. B: value reported for the wrong party (sign); C: $FRA_g$ built from the original tenors instead of the shortened ones.
2. B: advanced-settlement discounting omitted; C: receive-fixed and pay-fixed positions confused (sign).
3. B: $AI_T$ omitted (clean versus full price at expiration); C: accrued interest double counted on a price that is already full.
4. B: missing discounting of the forward price difference; C: full forward price compared with a clean contract price.
