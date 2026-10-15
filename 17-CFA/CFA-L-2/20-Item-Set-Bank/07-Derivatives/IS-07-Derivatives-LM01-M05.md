---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 1
title: "Valtoria AG: Franc-Euro Swap Funding for a Eurozone Acquisition"
los: [los-07-01-f, los-07-01-e]
difficulty: 4
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Valtoria AG: Franc-Euro Swap Funding for a Eurozone Acquisition

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Valtoria AG is a Swiss specialty pharmaceutical company that reports in Swiss francs (CHF).
To fund the purchase of a German contract manufacturer, Valtoria's treasury enters a two-year fixed-for-fixed currency swap with a dealer.
Marc Keller, CFA, the group treasurer, and his analyst, Ines Baumann, manage the hedge program.

At initiation Valtoria delivers CHF 150,000,000 to the dealer and receives the equivalent euro (EUR) notional at the spot rate of CHF 0.9380 per EUR 1.
Every 180 days Valtoria pays a fixed euro rate on the euro notional and receives a fixed franc rate on the franc notional, and the notionals are re-exchanged at maturity.
Both fixed rates are set at their no-arbitrage levels, and all rates are add-on rates on an actual/360 basis.

Exhibit 1: Spot rates at swap initiation

| Days | 180 | 360 | 540 | 720 |
|---|---|---|---|---|
| EUR | 2.60% | 2.70% | 2.78% | 2.85% |
| CHF | 0.85% | 0.92% | 0.98% | 1.04% |

Valtoria also has an existing CHF 80,000,000 interest rate swap, entered one year ago, in which it pays a fixed rate of 1.60% and receives MRR, with semiannual resets on the same 180-day schedule.
The swap had three years to run at inception, so four semiannual settlements remain, and today is a reset date that coincides with the currency swap's initiation.

One hundred twenty days after the currency swap's initiation, Baumann prepares a quarter-end valuation.
The first semiannual exchange of fixed payments will occur 60 days later.

Exhibit 2: Spot rates 120 days after initiation

| Days | 60 | 240 | 420 | 600 |
|---|---|---|---|---|
| EUR | 2.88% | 2.96% | 3.03% | 3.09% |
| CHF | 0.70% | 0.76% | 0.81% | 0.86% |

On the valuation date the spot exchange rate is CHF 0.9610 per EUR 1, and the one-year forward rate is CHF 0.9400 per EUR 1.

Baumann drafts two statements for the audit committee.

Statement 1: "Had the exchange rate been quoted in euros per franc, the euro would become currency a, and the value of the currency swap to Valtoria would then be the negative of the value we report."

Statement 2: "Of the three market moves since initiation (higher euro rates, lower franc rates, and a stronger euro), only the stronger euro has reduced the value of the currency swap to Valtoria."

Keller asks Baumann to confirm the payment schedule and both valuations before the committee meets.

## Questions

1. Based on Exhibit 1, Valtoria's semiannual fixed euro payment is closest to: (LOS: los-07-01-f)
   - A. EUR 1,962,135.
   - B. EUR 2,230,094.
   - C. EUR 4,460,188.
2. Based on Exhibit 2, the value of the currency swap to Valtoria 120 days after initiation is closest to: (LOS: los-07-01-f)
   - A. -CHF 3,542,756.
   - B. CHF 154,808.
   - C. CHF 3,542,756.
3. Based on Exhibit 1, the value today of Valtoria's existing CHF interest rate swap is closest to: (LOS: los-07-01-e)
   - A. -CHF 1,798,101.
   - B. -CHF 899,051.
   - C. CHF 899,051.
4. Which of Baumann's statements is correct? (LOS: los-07-01-f)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The quote is CHF per EUR, so $NA_{EUR} = 150{,}000{,}000/0.9380 = \text{EUR }159{,}914{,}712$.
> EUR PV factors: $1/[1 + 0.0260(0.5)] = 0.987167$, $1/[1 + 0.0270(1.0)] = 0.973710$, $1/[1 + 0.0278(1.5)] = 0.959969$, $1/[1 + 0.0285(2.0)] = 0.946074$, sum 3.866920.
> $r_{EUR} = (1 - 0.946074)/3.866920 \times (360/180) = 1.3946\% \times 2 = 2.7891\%$.
> Payment $= 159{,}914{,}712 \times (180/360) \times 0.027891 = \text{EUR }2{,}230{,}094$.
> A is wrong because it multiplies by the spot rate to get the euro notional, $150{,}000{,}000 \times 0.9380 = 140{,}700{,}000$, giving 1,962,135.
> C is wrong because it applies the annual rate to a half-year period, doubling the payment.
> 2. **A.** The quote is CHF per EUR, so currency a is the franc, and Valtoria, which receives francs, is the party whose value is $V_{CS}$.
> CHF PV factors at initiation are 0.995768, 0.990884, 0.985513, 0.979624 (sum 3.951789), so $r_{CHF} = (1 - 0.979624)/3.951789 \times 2 = 1.0312\%$, a periodic coupon of 0.5156%.
> Exhibit 2 CHF factors are 0.998835, 0.994959, 0.990638, 0.985869 (sum 3.970301), so the CHF bond is worth $0.005156 \times 3.970301 + 0.985869 = 1.006341$ per 1, or CHF 150,951,126.
> Exhibit 2 EUR factors are 0.995223, 0.980649, 0.965857, 0.951022 (sum 3.892751), so the EUR bond is worth $0.013946 \times 3.892751 + 0.951022 = 1.005309$ per 1, or EUR 160,763,665.
> $V_{CS} = 150{,}951{,}126 - 0.9610 \times 160{,}763{,}665 = 150{,}951{,}126 - 154{,}493{,}882 = -\text{CHF }3{,}542{,}756$.
> B is wrong because it translates the euro bond at the initial spot rate of 0.9380, giving $+154{,}808$.
> C is wrong because it negates the value on the belief that Valtoria pays currency a; that figure is the dealer's value.
> The one-year forward rate is a decoy; the formula uses the current spot rate.
> 3. **B.** Today is a reset date, so the floating leg is worth par and the swap is valued from the new fixed rate on a swap with the same four remaining dates.
> That rate comes from the Exhibit 1 CHF curve and equals the currency swap's CHF rate: $FS_t = 0.5 \times 1.0312\% = 0.5156\%$ against $FS_0 = 0.5 \times 1.60\% = 0.80\%$.
> Receive-fixed value $= 80{,}000{,}000 \times (0.0080 - 0.005156) \times 3.951789 = 899{,}051$.
> Valtoria pays fixed and rates have fallen, so its value is $-899{,}051$.
> A is wrong because it uses the annual rate difference instead of the periodic difference, doubling the loss to $-1{,}798{,}101$.
> C is wrong because it reports the receive-fixed counterparty's value.
> 4. **B.** Statement 1 is incorrect: relabeling currency a changes only which party the formula values directly; Valtoria's economic value is unchanged and would be obtained by negating the new $V_{CS}$ and converting it at the current spot rate.
> Statement 2 is correct: higher euro rates lower the value of the euro bond Valtoria is short, lower franc rates raise the value of the franc bond it is long, and only the rise in the euro from CHF 0.9380 to CHF 0.9610 hurts a party that owes euros.
> Translating at the initial spot rate gives $+154{,}808$, so the currency move alone swings the value by about CHF 3.7 million.
> A and C accept Statement 1, which confuses the formula's reference party with the economics of the position.

## Distractor design

1. A: notional solved in the wrong direction ($NA_b = S_0 NA_a$ instead of $NA_a/S_0$); C: annual rate not scaled by the accrual period.
2. B: translation at $S_0$ instead of $S_t$; C: currency a misidentified, value reported for the wrong party (sign).
3. A: annual instead of periodic rate difference; C: value reported for the wrong party (sign).
4. A and C: currency a labeling mistaken for a change in the position's economics.
