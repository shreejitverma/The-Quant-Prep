---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 1
title: "Harrow College Endowment: Reviewing a Consultant's Rate Memo"
los: [los-06-01-a, los-06-01-c, los-06-01-d, los-06-01-h, los-06-01-k]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Harrow College Endowment: Reviewing a Consultant's Rate Memo

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Naomi Achebe, CFA, is the compliance and risk officer of the Harrow College Endowment.
Before each investment committee meeting she checks every recommendation from the endowment's fixed-income consultant, Pelham Advisors, against the investment policy statement (IPS).
The IPS limits the fixed-income portfolio's duration to within 0.50 years of its benchmark, permits forward contracts only on default-free government zero-coupon bonds, and prohibits leverage.

Exhibit 1: Government zero-coupon (spot) rates, annual compounding

| Maturity (years) | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Spot rate | 2.50% | 2.85% | 3.10% | 3.30% | 3.45% |

The seven-year government par rate is 3.70%, and the portfolio's current duration is 6.10 years against a benchmark of 6.00 years.

Pelham's memo contains the following items.

Item 1: A donor has pledged USD 20 million to be paid to the endowment two years from today.
Pelham recommends entering a forward contract today to buy, at the pledge date, a government zero-coupon bond that matures five years from today.

Item 2: Committee member Daniel Cho projects that the three-year spot rate two years from today will be 3.40%.
He asks whether, under his projection, the zero-coupon bond underlying the Item 1 forward contract is attractively priced.

Item 3: Pelham expects the spot curve in Exhibit 1 to remain unchanged for the next year.
It recommends that the endowment buy the five-year government zero-coupon bond today and sell it after one year, rather than buy the one-year zero-coupon bond.

Item 4: Pelham describes a recent episode.
When the central bank began large purchases of long-dated government bonds, long government yields fell sharply.
Several pension funds that normally hold long government bonds then moved into long-dated corporate bonds and mortgage-backed securities to earn higher yields.
They moved back into government bonds after the yield advantage narrowed.

Item 5: Pelham writes: "The government has announced larger budget deficits, to be financed mainly with longer-maturity bonds."
"We expect this to reduce the bond risk premium and lower long-term government yields."

Item 6: Pelham's economists expect a sharp equity market decline over the next quarter that will trigger a flight to quality.
Pelham asks Achebe which portfolio change would best position the endowment for that view while remaining within the IPS.

Achebe also notes for the file that Pelham's fee is 0.12% of assets per year, which is unchanged from the prior contract.
She plans to record her conclusions item by item in the compliance log before the meeting.

## Questions

1. For Item 1, the no-arbitrage forward price per USD 1 of face value is closest to: (LOS: los-06-01-a)
   - A. 0.8928.
   - B. 0.9125.
   - C. 0.9250.
2. For Item 2, under Cho's projection the zero-coupon bond underlying the forward contract is most likely: (LOS: los-06-01-c)
   - A. undervalued.
   - B. fairly valued.
   - C. overvalued.
3. For Item 3, if Pelham's expectation is realized, the one-year holding-period return on the five-year zero-coupon bond is closest to: (LOS: los-06-01-d)
   - A. 2.50%.
   - B. 3.45%.
   - C. 4.05%.
4. The behavior of the pension funds described in Item 4 is most consistent with the: (LOS: los-06-01-h)
   - A. segmented markets theory.
   - B. preferred habitat theory.
   - C. local expectations theory.
5. Pelham's statement in Item 5 is: (LOS: los-06-01-k)
   - A. correct.
   - B. incorrect, because larger deficits and a longer maturity structure of government debt tend to raise the bond risk premium.
   - C. incorrect, because the supply of long-maturity bonds affects only short-term yields.
6. Given the view in Item 6, the portfolio change Achebe should approve is to: (LOS: los-06-01-k)
   - A. shift from a bullet to a barbell structure with the same duration.
   - B. shift from a barbell to a bullet structure with the same duration.
   - C. reduce portfolio duration by 1.00 year.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The contract is paid at $A = 2$ for a zero maturing at $B = 5$, so $F_{2,3} = DF_5 / DF_2$.
> $DF_2 = 1/(1.0285)^2 = 0.945347$ and $DF_5 = 1/(1.0345)^5 = 0.844010$, so $F_{2,3} = 0.844010 / 0.945347 = 0.8928$.
> On the USD 20 million pledge this price buys a face value of about USD 22.40 million.
> B is wrong because it is today's price of a three-year zero, $DF_3 = 1/(1.0310)^3 = 0.9125$, which ignores the two-year deferral.
> C is wrong because it misreads the subscripts as a two-year zero starting in three years, $DF_5 / DF_3 = 0.844010 / 0.912481 = 0.9250$.
> 2. **A.** The market's implied forward rate is $f_{2,3} = \left[(1.0345)^5 / (1.0285)^2\right]^{1/3} - 1 = 0.8928^{-1/3} - 1 = 3.85\%$.
> Cho projects a three-year spot rate of 3.40% two years from today, below the 3.85% forward, so the market is discounting the bond more heavily than he believes is warranted.
> Under his projection the bond will be worth $1/(1.034)^3 = 0.9046$ at delivery against a forward price of 0.8928, a gain of about 0.0118 per unit, so the bond is undervalued.
> B is wrong because a fair valuation requires the projected spot rate to equal the implied forward rate.
> C is wrong because it compares the 3.40% projection with today's three-year spot rate of 3.10% rather than with the 3.85% forward rate relevant to a bond delivered in two years.
> 3. **C.** Buy at $100/(1.0345)^5 = 84.4010$; with an unchanged curve the bond is a four-year zero in one year, priced at $100/(1.0330)^4 = 87.8211$.
> Return $= 87.8211/84.4010 - 1 = 4.05\%$, which equals the forward rate $f_{4,1} = (1.0345)^5/(1.0330)^4 - 1 = 4.05\%$ that rolls out of the pricing.
> The return exceeds the 2.50% one-year rate because a static upward-sloping curve lets the bond roll down to a lower yield.
> A is wrong because it is the return if spot rates evolve as the forward curve implies, not if the curve stays static.
> B is wrong because it assumes the one-year return equals the bond's five-year yield, ignoring the capital gain from rolling down the curve.
> 4. **B.** Preferred habitat theory holds that investors have preferred maturity segments but will leave them when the expected additional return is sufficient, which is what the pension funds did when central bank purchases compressed long government yields.
> A is wrong because segmented markets theory assumes investors do not leave their segment whatever the yield differential; the funds visibly did.
> C is wrong because local expectations theory concerns short-horizon returns being equal across maturities and says nothing about migration between segments.
> 5. **B.** Larger deficits increase the supply of government bonds, and a longer debt maturity structure adds duration supply, so both tend to raise the bond risk premium and long-term yields, the opposite of Pelham's conclusion.
> A is wrong because Pelham has the direction of the supply effect reversed.
> C is wrong because a greater supply of long-maturity bonds acts mainly on long-term yields and the term premium, not only on short-term yields.
> 6. **A.** A flight to quality produces bullish flattening: long-term government yields fall more than short-term yields.
> At the same duration, a barbell places more exposure at the long end, which rallies most, so the shift captures the flattening and keeps duration inside the IPS band.
> B is wrong because a bullet concentrates exposure at the intermediate maturities and underperforms a same-duration barbell in a bullish flattening.
> C is wrong because it positions for rising yields, the opposite of the view, and a 1.00-year cut takes duration from 6.10 to 5.10 years, outside the 0.50-year band around the 6.00-year benchmark.

## Distractor design

1. B: spot price of the three-year zero used (deferral ignored); C: subscripts misread, $DF_5/DF_3$ instead of $DF_5/DF_2$ (spot vs forward notation).
2. B: fair value assumed without comparing projection to forward; C: projection compared with today's spot rate instead of the forward rate (spot vs forward).
3. A: forward-realized return used instead of the static-curve return (wrong scenario); B: holding-period return equated with YTM (rolldown gain ignored).
4. A: theory that forbids the migration observed (misread vignette); C: theory about short-horizon returns, not segment choice (wrong theory).
5. A: supply effect direction reversed (sign); C: supply effect attached to the wrong end of the curve.
6. B: bullet vs barbell reversed; C: rate-direction view reversed and IPS duration band breached (constraint).
