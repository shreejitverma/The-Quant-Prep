---
type: cfa-itemset
topic: "Economics"
topic_code: "02"
topic_slug: "02-Economics"
lm: 1
title: "Alpenwerk Medical Treasury Desk"
los: [los-02-01-a, los-02-01-b, los-02-01-c, los-02-01-d]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/economics]
---

# Alpenwerk Medical Treasury Desk

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Alpenwerk Medical AG is a Zug-based manufacturer of surgical imaging equipment whose functional and reporting currency is the Swiss franc (CHF).
Most of its revenue is invoiced in US dollars (USD) and euros (EUR), so the treasury team manages a steady stream of currency conversions and forward hedges.
Treasurer Marco Bianchi has asked treasury analyst Lena Vogt to prepare the desk's quarterly hedge report and to review the pricing the company receives from its house bank, Rheintal Bank.

On the morning of the review, Vogt downloads the interbank spot quotes in Exhibit 1 and the client quotes Rheintal Bank has streamed to Alpenwerk in Exhibit 2.

Exhibit 1: Interbank Spot Quotes (bid/offer)

| Currency pair | Bid | Offer |
|---|---|---|
| USD/EUR | 1.0852 | 1.0856 |
| USD/CHF | 1.1346 | 1.1351 |
| JPY/USD | 149.62 | 149.66 |

Exhibit 2: Rheintal Bank Quotes to Alpenwerk

| Quote | Bid | Offer |
|---|---|---|
| CHF/USD spot | 0.8805 | 0.8819 |
| CHF/USD 6-month forward points | -156.3 | -153.9 |
| CHF/EUR spot | 0.9559 | 0.9570 |
| CHF/EUR 3-month forward points | -59.4 | -57.0 |

Exhibit 3: Market Reference Rates (annualized, Actual/360)

| Currency | 90-day | 180-day |
|---|---|---|
| CHF | 1.15% | 1.20% |
| EUR | 3.60% | 3.75% |
| USD | 4.85% | 4.80% |

Vogt has three transactions to handle.
First, a US hospital group has just paid an invoice, and Alpenwerk must convert USD 12,000,000 into CHF at Rheintal's spot quote.
Second, a further USD 7,500,000 receivable is due in 180 days, and Bianchi wants to lock in the CHF value today with a forward contract from Rheintal.
Third, three months ago Alpenwerk sold EUR 8,000,000 six months forward against CHF at an all-in rate of CHF/EUR 0.9480 to hedge a German distributor's payment; the hedge report must show its current mark-to-market value.

While reviewing the quotes, Bianchi makes three comments about why Rheintal's spreads look the way they do.
He first says that Alpenwerk's AA credit rating is the main reason its CHF/USD spot spread is as narrow as 14 pips.
He then says that the spread on the 6-month CHF/USD forward is wider than the spot spread because longer-dated contracts are less liquid and carry more counterparty credit risk and interest rate risk.
Finally, he says that the desk should execute its CHF/USD trades at 07:30 Zurich time, before London opens, because spreads are tightest before the European session begins.

Vogt also receives an unsolicited quote from a second dealer, Dealer B, which offers to deal CHF/EUR at 0.9549/0.9555 for amounts up to EUR 5,000,000.
She notes that the interbank market quotes the franc against the dollar as USD/CHF, so any comparison of Dealer B's cross quote with the interbank market requires inverting that pair.
Bianchi asks her whether Alpenwerk could profit from Dealer B's quote without taking any currency exposure, and, if so, how much it would earn on the maximum EUR 5,000,000.

Finally, for the hedge report, Vogt must document the 180-day forward premium or discount on the CHF/USD rate implied by the midpoint of Rheintal's spot quote and the 180-day rates in Exhibit 3, so that the audit committee can see how the forward points relate to interest rate differentials.

## Questions

1. The CHF amount Alpenwerk will receive from converting the USD 12,000,000 at Rheintal's spot quote is closest to: (LOS: los-02-01-a)
   - A. CHF 10,566,000.
   - B. CHF 10,574,400.
   - C. CHF 10,582,800.
2. Which of Bianchi's comments about Rheintal's spreads is most likely correct? (LOS: los-02-01-a)
   - A. The comment about Alpenwerk's credit rating.
   - B. The comment about the forward contract's term.
   - C. The comment about trading at 07:30 Zurich time.
3. Using Exhibit 1 and Dealer B's quote, Alpenwerk's triangular arbitrage opportunity on EUR 5,000,000 is best described as: (LOS: los-02-01-b)
   - A. sell EUR to Dealer B at 0.9549 and buy EUR in the interbank market.
   - B. buy EUR from Dealer B and sell EUR in the interbank market, for a profit closest to CHF 6,565.
   - C. buy EUR from Dealer B and sell EUR in the interbank market, for a profit closest to CHF 2,696.
4. The 180-day forward premium (discount) on the CHF/USD rate that Vogt should document is closest to: (LOS: los-02-01-c)
   - A. -0.0303.
   - B. -0.0155.
   - C. +0.0155.
5. The CHF amount Alpenwerk can lock in today for the USD 7,500,000 receivable due in 180 days is closest to: (LOS: los-02-01-c)
   - A. CHF 6,486,525.
   - B. CHF 6,488,325.
   - C. CHF 6,498,825.
6. The mark-to-market value of Alpenwerk's EUR 8,000,000 forward position is closest to: (LOS: los-02-01-d)
   - A. -CHF 15,635.
   - B. -CHF 26,324.
   - C. -CHF 26,400.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Alpenwerk sells USD, the base currency of the CHF/USD quote, so it hits Rheintal's bid: $12{,}000{,}000 \times 0.8805 = \text{CHF }10{,}566{,}000$.
>    B is wrong because it uses the midpoint $0.8812$, giving $12{,}000{,}000 \times 0.8812 = 10{,}574{,}400$, a rate no dealer offers a client.
>    C is wrong because it uses the offer $0.8819$, the price at which a client buys USD, giving $10{,}582{,}800$.
> 2. **B.** Forward spreads widen with term because liquidity thins and counterparty credit and interest rate exposure grow; the all-in forward spread here is $(0.8819 - 0.01539) - (0.8805 - 0.01563) = 0.86651 - 0.86487 = 0.00164$, or 16.4 pips versus 14 pips spot.
>    A is wrong because spot trades settle T+2, so credit risk has little influence on spot spreads.
>    C is wrong because spreads are tightest during the London-New York overlap (roughly 14:00 to 17:00 Zurich time), not before London opens.
> 3. **C.** Invert USD/CHF and swap sides: CHF/USD bid $= 1/1.1351 = 0.880980$, offer $= 1/1.1346 = 0.881368$.
>    Implied CHF/EUR bid $= 1.0852/1.1351 = 0.956039$; implied offer $= 1.0856/1.1346 = 0.956813$.
>    Dealer B's offer (0.9555) is below the implied interbank bid (0.956039), so buy EUR from Dealer B at 0.9555 and sell EUR interbank at 0.956039.
>    Profit $= (0.956039 - 0.9555) \times 5{,}000{,}000 = 0.000539 \times 5{,}000{,}000 = \text{CHF }2{,}696$ (2,695.58 at full precision).
>    A is wrong because it reverses the trade direction: Dealer B's bid (0.9549) does not exceed the implied interbank offer (0.956813), so buying EUR interbank and selling it to Dealer B loses $(0.9549 - 0.956813) \times 5{,}000{,}000 = -\text{CHF }9{,}565$ (Python: $-9{,}564.87$).
>    B is wrong because it sells EUR interbank at the implied offer 0.956813, the price at which the market sells EUR, not buys it: $(0.956813 - 0.9555) \times 5{,}000{,}000 = 6{,}565$.
> 4. **B.** USD is the base currency, so $i_B = 4.80\%$ and $i_P = 1.20\%$; midpoint spot $= (0.8805 + 0.8819)/2 = 0.8812$.
>    $F - S = 0.8812 \times \dfrac{180/360}{1 + 0.0480(180/360)} \times (0.0120 - 0.0480) = 0.8812 \times \dfrac{0.5}{1.024} \times (-0.036) = -0.015490$.
>    The higher-yielding USD trades at a forward discount, consistent with the negative points in Exhibit 2 (the CIP value of $-154.9$ points sits between the quoted $-156.3$ and $-153.9$).
>    A is wrong because it applies the full-year rate differential without the 180/360 scaling: $0.8812/1.048 \times (-0.036) = -0.0303$.
>    C is wrong because it reverses the rate differential (base rate minus price rate), flipping the sign.
> 5. **A.** Alpenwerk will sell USD (the base) forward, so it uses the bid side of both spot and points: $0.8805 + (-156.3/10{,}000) = 0.8805 - 0.01563 = 0.86487$.
>    Proceeds $= 7{,}500{,}000 \times 0.86487 = \text{CHF }6{,}486{,}525$.
>    B is wrong because it adds the offer points to the bid spot: $0.8805 - 0.01539 = 0.86511$, giving $6{,}488{,}325$.
>    C is wrong because it uses the offer side of both, the rate for a client buying USD: $0.8819 - 0.01539 = 0.86651$, giving $6{,}498{,}825$.
> 6. **B.** Alpenwerk is short EUR (the base) forward, so it closes by buying EUR three months forward at the offer on spot and points: $0.9570 + (-57.0/10{,}000) = 0.9570 - 0.0057 = 0.9513$.
>    Settlement cash flow $= (0.9480 - 0.9513) \times 8{,}000{,}000 = -0.0033 \times 8{,}000{,}000 = -\text{CHF }26{,}400$, a loss because the EUR appreciated against the CHF.
>    Discount 90 days at the CHF rate, the currency of the cash flow: $-26{,}400/(1 + 0.0115 \times 90/360) = -26{,}400/1.002875 = -\text{CHF }26{,}324$ (Python: $-26{,}324.32$).
>    A is wrong because it offsets on the bid side: $0.9559 - 0.00594 = 0.94996$, giving $(0.9480 - 0.94996) \times 8{,}000{,}000 = -15{,}680$ and $-15{,}680/1.002875 = -15{,}635$.
>    C is wrong because it omits discounting the settlement cash flow to today.

## Distractor design

- Q1: B uses the midpoint rate; C uses the offer (wrong side of the quote for a seller of the base currency).
- Q2: A overstates credit risk for T+2 spot settlement; C misidentifies the most liquid trading window.
- Q3: A reverses the trade direction, selling EUR to the dealer whose quote is already the cheap side (direction error); B sells EUR at the implied interbank offer instead of the bid (wrong side).
- Q4: A omits the Actual/360 day-count scaling; C reverses the interest rate differential (sign error).
- Q5: B pairs offer points with bid spot (mixed sides); C uses the offer side for a sale of the base currency.
- Q6: A offsets the short position at the bid (wrong side); C omits discounting at the CHF rate.
