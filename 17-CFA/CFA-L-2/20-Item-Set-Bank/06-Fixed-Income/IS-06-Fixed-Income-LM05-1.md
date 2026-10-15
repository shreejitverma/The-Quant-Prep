---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 5
title: "Harrow Mutual Life: CDS Risk Report"
los: [los-06-05-a, los-06-05-b, los-06-05-c, los-06-05-d]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Harrow Mutual Life: CDS Risk Report

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Denise Okoro, CFA, is head of credit risk at Harrow Mutual Life, a US life insurer with a large corporate bond portfolio.
Harrow's investment policy permits credit default swaps for hedging and for tactical credit exposure, and each quarter Okoro reports every CDS position to the board risk committee.
All of Harrow's contracts are documented under the Standard North American Contract.

Harrow has sold $750 million of five-year protection on the on-the-run CDX North American Investment Grade index (CDX IG), which has 125 equally weighted constituents.
To reduce concentration, Okoro bought $4.5 million of five-year single-name protection on Kestrel Components, a CDX IG constituent whose five-year spread had widened from 95 bps to 240 bps after a product recall.
During the quarter, Kestrel filed for bankruptcy.

Harrow also holds $20 million face value of the two-year senior unsecured notes of Lorne Paper Company, and it bought $20 million of five-year protection on Lorne whose reference obligation is Lorne's seven-year senior unsecured bond.
Lorne missed a scheduled coupon on its ten-year subordinated note, and the grace period expired without payment.
Lorne has not filed for bankruptcy and is negotiating with creditors.
The regional ISDA Determinations Committee then voted 12 to 3 that a credit event had occurred.

Exhibit 1: Lorne Paper debt prices after the Determinations Committee vote

| Obligation | Seniority | Price (% of par) |
|---|---|---|
| Term loan due in three years | Senior secured | 61 |
| Notes due in two years | Senior unsecured | 38 |
| Bond due in seven years | Senior unsecured | 33 |
| Note due in ten years | Subordinated | 18 |

At the committee meeting, general counsel Martin Hale and Okoro discuss the Lorne contract.

Hale: "Lorne's missed payment cannot trigger our contract, because the payment was missed on a subordinated note while our reference obligation is senior."

Okoro: "Had Lorne instead negotiated a voluntary maturity extension with its bondholders, that would also have been a credit event under our contract."

The committee also reviews Mercer Health Systems, a hospital operator whose bonds Harrow holds.
Harrow's credit model produces the annual hazard rates in Exhibit 2.

Exhibit 2: Mercer Health Systems hazard rates

| Year | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Hazard rate | 1.2% | 1.8% | 2.5% | 3.1% | 3.6% |

Harrow's chief economist expects Mercer's liquidity to remain strong for the next two years, supported by a committed bank facility.
She is concerned, however, that reimbursement reforms taking effect in six years will raise Mercer's long-term credit risk substantially relative to its short-term credit risk.
Okoro wants a CDS position on Mercer that profits if the economist is right while keeping the net premium outlay low.
Mercer CDS trade at two-year and ten-year maturities, and the ten-year contract has an effective spread duration of 7.8.

## Questions

1. At the time of Kestrel's bankruptcy filing, and before any settlement takes place, Harrow's net notional credit exposure to Kestrel through its CDS positions is closest to: (LOS: los-06-05-a)
   - A. long $6.0 million.
   - B. long $1.5 million.
   - C. long $3.0 million.
2. Regarding the statements made by Hale and Okoro about credit events, which is most accurate? (LOS: los-06-05-b)
   - A. Only Hale is correct.
   - B. Only Okoro is correct.
   - C. Neither is correct.
3. Assuming the settlement auction values the cheapest-to-deliver obligation at its Exhibit 1 price, the cash settlement payout on Harrow's Lorne CDS is closest to: (LOS: los-06-05-b)
   - A. $13.4 million.
   - B. $12.4 million.
   - C. $16.4 million.
4. Given the Lorne notes it owns, Harrow should most likely: (LOS: los-06-05-b)
   - A. be indifferent between settlement methods, because either delivers $20.0 million.
   - B. prefer cash settlement, because it delivers $21.0 million in total.
   - C. prefer cash settlement, because it delivers $24.0 million in total.
5. Based on Exhibit 2, the probability that Mercer defaults at some point during the next three years is closest to: (LOS: los-06-05-c)
   - A. 5.40%.
   - B. 5.50%.
   - C. 12.20%.
6. The CDS position on Mercer that best expresses the chief economist's view is to: (LOS: los-06-05-d)
   - A. buy two-year protection and sell ten-year protection.
   - B. buy two-year protection and buy ten-year protection.
   - C. buy ten-year protection and sell two-year protection.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Index CDS are equally weighted, so selling $750 million of CDX IG protection is long credit exposure of $750 / 125 = $6.0$ million per constituent.
> The single-name purchase of $4.5 million of Kestrel protection is short credit exposure of $4.5 million.
> Net exposure $= 6.0 - 4.5 = 1.5$, long $1.5 million (75% of the index exposure is hedged).
> A is wrong because it reports the index exposure and ignores the single-name hedge.
> C is wrong because it divides by 100, the CDX HY constituent count: $750 / 100 - 4.5 = 3.0$.
> 2. **C.** Hale is wrong: failure to pay a scheduled coupon after the grace period is a credit event, no bankruptcy filing is needed, and the trigger applies to Lorne's outstanding obligations, not only to the reference obligation; seniority limits which bonds are deliverable, not whether the event occurred.
> Okoro is wrong twice: restructuring is not a credit event under the Standard North American Contract, and even where recognized it must be involuntary or coercive, not a voluntary negotiated extension.
> A is wrong because it accepts Hale's seniority argument, which confuses deliverability with the trigger.
> B is wrong because it imports the European treatment of restructuring into a US contract and ignores the voluntary nature of the extension.
> 3. **A.** The contract covers obligations ranked equal to or higher than the senior unsecured reference bond, so the subordinated note is excluded.
> Among the covered obligations (secured loan at 61, senior notes at 38, senior bond at 33), the cheapest to deliver is the seven-year bond at 33, so $\text{RR} = 0.33$.
> Payout $= (1 - 0.33) \times 20{,}000{,}000 = 13{,}400{,}000$.
> B is wrong because it uses the price of the bond Harrow owns (38): $(1 - 0.38) \times 20 = 12.4$ million; the payout is set by the cheapest deliverable, not the holder's own bond.
> C is wrong because it treats the subordinated note at 18 as deliverable: $(1 - 0.18) \times 20 = 16.4$ million.
> 4. **B.** Cash settlement: payout $13.4$ million plus sale of the two-year notes at 38, $0.38 \times 20 = 7.6$ million, total $21.0$ million.
> Physical settlement: deliver the notes and receive the $20.0$ million notional.
> Harrow owns a covered bond priced above the cheapest to deliver, so cash settlement is worth $1.0$ million more.
> A is wrong because indifference holds only for a holder of the cheapest-to-deliver obligation itself.
> C is wrong because it builds the cash total on the subordinated note as cheapest to deliver: $16.4 + 7.6 = 24.0$ million.
> 5. **A.** Survival through year 3 $= (1 - 0.012)(1 - 0.018)(1 - 0.025) = 0.988 \times 0.982 \times 0.975 = 0.9460$ (0.945961).
> POD $= 1 - 0.9460 = 0.0540$, or 5.40%.
> B is wrong because it adds the three hazard rates ($1.2 + 1.8 + 2.5 = 5.50\%$), ignoring that each is conditional on prior survival.
> C is wrong because it adds all five hazard rates ($12.20\%$), using the wrong horizon as well as the additive shortcut.
> 6. **C.** The view is that long-term credit risk rises relative to short-term credit risk, a steepening of Mercer's credit curve.
> Buy ten-year protection (short the long end, which gains if long-term spreads widen) and sell two-year protection (long the short end, whose premium income offsets the cost), a steepener that is bullish on Mercer in the short run.
> A is wrong because it is the flattener, which profits if near-term risk rises relative to long-term risk, the opposite of the view.
> B is wrong because buying protection at both maturities is a bet on a rise in the level of spreads, not on the curve's shape, and it maximizes rather than limits the premium outlay.

## Distractor design

1. A: single-name hedge ignored (index exposure only); C: wrong constituent count (CDX HY 100 instead of CDX IG 125).
2. A: deliverability by seniority confused with the failure-to-pay trigger; B: European restructuring rule applied to a US contract and the voluntary-versus-coercive test ignored.
3. B: holder's own bond price used instead of the cheapest to deliver; C: subordinated note treated as deliverable against a senior reference obligation.
4. A: indifference claimed for a holder whose bond trades above the cheapest to deliver; C: subordinated note used as the cheapest to deliver in the cash total.
5. B: hazard rates added instead of survival probabilities multiplied; C: additive shortcut over the full five-year table (wrong horizon).
6. A: steepener and flattener legs swapped; B: level trade substituted for a curve trade.
