---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 2
title: "Nordhaven Savings Bank: Treasury Desk Arbitrage Review"
los: [los-06-02-a, los-06-02-b, los-06-02-f]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Nordhaven Savings Bank: Treasury Desk Arbitrage Review

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ingrid Solberg, CFA, is a fixed-income analyst on the treasury desk of Nordhaven Savings Bank, a regional lender that holds a liquidity portfolio of government securities.
Her supervisor, Marcus Lindqvist, asks her to review the desk's pricing of several government instruments before the monthly asset-liability committee meeting.
All instruments in this review are option-free, pay annual coupons, and carry the same credit risk as the benchmark government curve unless stated otherwise.

Solberg begins with the benchmark par curve published by the government debt office.

Exhibit 1: Benchmark government par curve (annual pay)

| Maturity | Par rate |
|---|---|
| 1 year | 2.40% |
| 2 years | 2.90% |
| 3 years | 3.30% |
| 4 years | 3.55% |

Government securities dealers in the market actively strip coupon bonds into zero-coupon securities and reconstitute zero-coupon securities into coupon bonds.
Solberg confirms that the dealers' bid and offer prices for zero-coupon strips are consistent with the spot rates implied by Exhibit 1, and she ignores transaction costs throughout.

The desk is considering a three-year government bond with a 5.25% annual coupon.
One dealer, Aurora Securities, is offering the bond at 105.2000 per 100 of par.
Lindqvist notes that the bond's quoted yield to maturity at that price, about 3.40%, is above the 3.30% three-year par rate, and he asks Solberg whether the offer represents value.

Solberg also reviews two one-year risk-free instruments held in the liquidity portfolio.

Exhibit 2: One-year risk-free instruments

| Instrument | Price today | Single payment in one year |
|---|---|---|
| Government bill | 97.6562 | 100.00 |
| Government-guaranteed agency note | 195.0000 | 200.00 |

Both instruments are backed by the full faith and credit of the government, so their payments are equally certain.
Lindqvist comments that the note's price is roughly twice the bill's price, and asks Solberg to confirm whether anything is wrong.

Finally, the desk is preparing to value a callable covered bond issued by another bank.
The desk's quantitative team has built a lognormal binomial interest rate tree calibrated to Exhibit 1 using a 15% volatility assumption, and it is debating whether to raise the volatility assumption to 20%.
Lindqvist makes the following two statements at the meeting.

Statement 1: "If we recalibrate the tree at 20% volatility and use it to value the 5.25% government bond, we will get a higher value than we get from the spot curve, because a wider tree gives more weight to low-rate outcomes."

Statement 2: "Calibrating a tree to the benchmark curve is mostly a validation exercise; its practical payoff is that it lets us value the callable covered bond, which the spot curve alone cannot do."

Solberg drafts her responses for the committee pack, showing each calculation so that the committee can audit it.

## Questions

1. Based on Exhibit 1, the three-year spot rate is closest to: (LOS: los-06-02-b)
   - A. 3.3000%.
   - B. 3.3190%.
   - C. 4.1474%.
2. The arbitrage-free value of the 5.25% three-year government bond is closest to: (LOS: los-06-02-b)
   - A. 105.4841.
   - B. 105.5137.
   - C. 105.5671.
3. Given the Aurora Securities offer, the arbitrage trade and its riskless profit per 100 of par are best described as: (LOS: los-06-02-a)
   - A. buy the bond from Aurora and sell its stripped cash flows, earning 0.3137.
   - B. buy zero-coupon strips, reconstitute the bond, and sell it to Aurora, earning 0.3137.
   - C. buy the bond from Aurora and sell its stripped cash flows, earning 0.2841.
4. Based on Exhibit 2, Solberg's most appropriate conclusion is that an arbitrage opportunity: (LOS: los-06-02-a)
   - A. exists under the value additivity principle; buy the bills and sell the note.
   - B. exists under the dominance principle; buy the note and sell the bills.
   - C. exists under the dominance principle; buy the bills and sell the note.
5. Regarding Statement 1, the value of the 5.25% bond on the tree recalibrated at 20% volatility will most likely be: (LOS: los-06-02-f)
   - A. equal to its value from the spot curve.
   - B. higher than its value from the spot curve.
   - C. lower than its value from the spot curve.
6. Is Lindqvist's Statement 2 correct? (LOS: los-06-02-f)
   - A. Yes.
   - B. No, because calibration is mainly used to identify benchmark bonds that the market has mispriced.
   - C. No, because a calibrated tree values option-free bonds more accurately than the spot curve does.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Bootstrap from the par curve, one maturity at a time.
> $z_1 = 2.4000\%$ because the one-year par bond has a single cash flow.
> $1 = 0.029/1.024 + 1.029/(1+z_2)^2$ gives $(1+z_2)^2 = 1.029 / 0.971680 = 1.058991$ and $z_2 = 2.9073\%$.
> $1 = 0.033/1.024 + 0.033/1.029073^2 + 1.033/(1+z_3)^3$ gives $z_3 = 3.3190\%$.
> A is wrong because it treats the three-year par rate as the three-year spot rate, which holds only for a flat curve.
> C is wrong because 4.1474% is the implied one-year forward rate two years from now, $1.033190^3 / 1.029073^2 - 1$, the spot-versus-forward switch.
> 2. **B.** Discount each cash flow at its own spot rate: $5.25/1.024 + 5.25/1.029073^2 + 105.25/1.033190^3 = 5.1270 + 4.9575 + 95.4292 = 105.5137$.
> A is wrong because it discounts every cash flow at the 3.30% three-year par yield (105.4841), over-discounting the early coupons on an upward-sloping curve.
> C is wrong because it discounts each cash flow at the par rate of its own maturity, $5.25/1.024 + 5.25/1.029^2 + 105.25/1.033^3 = 105.5671$, using par yields instead of spot rates.
> 3. **A.** The bond is worth 105.5137 as a package of zeros but Aurora offers it at 105.2000, so value additivity fails and the bond is cheap.
> Buy the bond, strip it, and sell the three zeros at spot-consistent prices of $5.25 \times 0.976563 = 5.1270$, $5.25 \times 0.944295 = 4.9575$ and $105.25 \times 0.906691 = 95.4292$, for proceeds of 105.5137 and a riskless profit of $105.5137 - 105.2000 = 0.3137$ today.
> B is wrong because reconstitution is the trade when the coupon bond is rich relative to its strips; here selling the bond at 105.2000 after paying 105.5137 for the strips loses 0.3137.
> C is wrong because it measures the gap against the price at the 3.30% par yield ($105.4841 - 105.2000 = 0.2841$), not against the spot-rate value the strip market actually pays.
> 4. **B.** The bill implies a one-year risk-free return of $100/97.6562 - 1 = 2.4000\%$ and the note implies $200/195.0000 - 1 = 2.5641\%$.
> Two equally certain claims must be discounted at the same rate, so the note, which offers the higher return, is cheap: this is a dominance violation.
> Buy one note for 195.0000 and short two bills for $2 \times 97.6562 = 195.3124$, collecting $0.3124$ today with offsetting payments of 200 in one year.
> A is wrong because nothing here is a package priced away from the sum of its parts, so value additivity is the wrong label, and the trade direction is reversed.
> C names the right principle but reverses the trade, buying the expensive bill and selling the cheap note, which locks in a loss.
> Lindqvist's price-ratio comparison misses the issue: $2 \times 97.6562 = 195.3124 \neq 195.0000$.
> 5. **A.** An option-free bond valued on a tree calibrated to the benchmark curve returns exactly its spot-rate value, 105.5137, at any volatility, because both methods are arbitrage free.
> Raising volatility spreads the node rates, but recalibration forces the tree to reprice the benchmarks, so the option-free value cannot move.
> B is wrong because it attributes option value to a bond with no option; convexity from wider rates is exactly offset by recalibration.
> C is wrong for the same reason in the other direction; the lognormal spread is absorbed in calibration.
> 6. **A.** Calibration does not improve option-free pricing, which the spot curve already handles exactly; its payoff is that the verified tree can generate the rate-dependent cash flows of a bond with an embedded option, such as the callable covered bond.
> B is wrong because calibration assumes the benchmark bonds are correctly priced; they are the standard, not the suspects.
> C is wrong because for option-free bonds the tree and the spot curve give identical values, so neither is more accurate.

## Distractor design

1. A: par rate used as spot rate (flat-curve assumption); C: implied forward rate substituted for the spot rate.
2. A: single-YTM discounting at the three-year par yield; C: each cash flow discounted at its own maturity's par yield instead of its spot rate.
3. B: stripping versus reconstitution direction reversed; C: mispricing measured against the YTM price instead of the spot-rate value.
4. A: value additivity mislabeled and trade reversed; C: correct principle, cheap and rich instruments swapped.
5. B: option value attributed to an option-free bond at higher volatility; C: lognormal averaging misread as a downward bias.
6. B: benchmarks treated as mispriced rather than as the calibration standard; C: tree assumed more accurate than spot rates for option-free bonds.
