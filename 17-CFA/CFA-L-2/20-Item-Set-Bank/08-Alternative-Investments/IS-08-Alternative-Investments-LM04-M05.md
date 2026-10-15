---
type: cfa-itemset
topic: "Alternative Investments"
topic_code: "08"
topic_slug: "08-Alternative-Investments"
lm: 4
title: "Quillfeather Multi-Strategy Fund Desk Review"
los: [los-08-04-b, los-08-04-c, los-08-04-d, los-08-04-f]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/alternative-investments]
---

# Quillfeather Multi-Strategy Fund Desk Review

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Mariko Tanabe, CFA, is an investment officer at Harrowgate Mutual Insurance, which is conducting annual due diligence on its USD 300 million allocation to the Quillfeather Multi-Strategy Fund.
Quillfeather runs four desks under one roof, and Tanabe reviews one current position from each desk with Quillfeather's chief risk officer, Declan Moyo.

The equity desk runs a stub trade in Brannock Industries, a listed holding company that owns 70% of Brannock Logistics and 45% of Selwyn Chemicals, both separately listed.
The desk regards Brannock Industries as overvalued relative to the market value of its two listed stakes.
It has shorted 120,000 Brannock Industries shares and weights the subsidiary legs by the parent's ownership percentages.
Exhibit 1 shows the desk's data.

**Exhibit 1: Brannock stub trade data**

| Company | Share price (USD) | Market beta | Parent's ownership |
|---|---|---|---|
| Brannock Industries (parent) | 58.20 | 1.05 | n/a |
| Brannock Logistics | 31.40 | 0.90 | 70% |
| Selwyn Chemicals | 24.75 | 1.20 | 45% |

The event desk runs a merger arbitrage book.
Its two largest positions are in stock-for-stock deals, in each of which the desk is long the target and short the acquirer in the offer ratio.
Exhibit 2 summarizes them.

**Exhibit 2: Largest merger arbitrage positions**

| Deal | Structure | Current spread |
|---|---|---|
| Veldhoven Pharma (acquirer, Netherlands) for Ashby Biologics (target, United States) | Cross-border, friendly; needs approval from both countries' regulators | 6.1% |
| Corrin Foods (acquirer) for Pell Bakeries (target), both United States | Domestic, friendly, horizontal | 2.4% |

Moyo makes two statements about the merger book.

Statement 1: "The Veldhoven-Ashby spread is wider mainly because a cross-border deal needs two governmental approvals, which raises the risk that it fails."

Statement 2: "To protect the Veldhoven-Ashby position if the deal fails, we buy out-of-the-money puts on Veldhoven and out-of-the-money calls on Ashby."

The rates desk put on a trade during a recent period of market stress, when hedged inflation-linked bonds traded far cheaper than their usual premium over nominal bonds.
The desk bought USD 40 million of 5-year inflation-linked government bonds at a real yield of 2.45% and shorted USD 40 million of 5-year nominal government bonds of the same government at a yield of 4.05%.
It also entered a zero-cost 5-year inflation swap on a notional of USD 40 million, receiving a fixed rate of 2.30% and paying realized inflation.
Trailing 12-month inflation is 3.10%.
Assume the inflation accrual on the inflation-linked bonds equals the inflation paid on the swap, and ignore financing and transaction costs.

The volatility desk hedges the fund's equity tail risk.
One year ago it bought a one-year volatility swap on a broad equity index with a vega notional of USD 150,000 per volatility point.
The strike was set at the swap's fair volatility of 16.0 at inception.
Over the year, the index's realized volatility was 21.4, and on the expiry date the index's one-month implied volatility was 19.0.

Tanabe tells Moyo that she will summarize each desk's position for Harrowgate's investment committee meeting on 18 March.

## Questions

1. To complete the Brannock stub trade, the equity desk's position in Selwyn Chemicals should be: (LOS: los-08-04-b)
   - A. long 54,000 shares.
   - B. long 66,000 shares.
   - C. short 54,000 shares.
2. Which of Moyo's statements about the merger arbitrage book is correct? (LOS: los-08-04-c)
   - A. Statement 1 only
   - B. Statement 2 only
   - C. Both Statement 1 and Statement 2
3. The rates desk's expected annual net cash flow from its combined position is closest to: (LOS: los-08-04-d)
   - A. negative USD 640,000
   - B. USD 280,000
   - C. USD 600,000
4. The payoff to the volatility desk on the volatility swap at expiry is closest to: (LOS: los-08-04-f)
   - A. USD 450,000
   - B. USD 810,000
   - C. negative USD 810,000

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** In a stub trade, the subsidiary legs are weighted by the parent's ownership percentages, so each parent share shorted is offset by buying subsidiary shares equal to the ownership percentage.
> Because the desk is short the overvalued parent, it must be long the subsidiaries: Selwyn Chemicals shares bought $= 120{,}000 \times 0.45 = 54{,}000$ (and Brannock Logistics shares bought $= 120{,}000 \times 0.70 = 84{,}000$).
> This replicates the parent's look-through exposure to its listed stakes, so only the relative mispricing of the parent against its holdings remains.
> The share prices and betas in Exhibit 1 are not needed for the ownership-weighted hedge.
> B is wrong because it uses the 55% of Selwyn held by outside shareholders: $120{,}000 \times (1 - 0.45) = 66{,}000$.
> C is wrong because it reverses the direction of the subsidiary leg; shorting both the parent and the subsidiary would double the exposure rather than hedge it.
> 2. **A.** Statement 1 is correct: cross-border deals need two governmental approvals and so carry a higher risk of failure, which the market prices as a wider spread than a domestic friendly deal.
> Statement 2 is incorrect because it reverses both legs of the hedge.
> The desk is long Ashby (the target) and short Veldhoven (the acquirer); if the deal fails, Ashby falls back and Veldhoven rebounds toward their pre-announcement prices.
> The protection is therefore out-of-the-money calls on Veldhoven, which cover the short as the acquirer rallies, and out-of-the-money puts on Ashby, which floor the long as the target falls.
> B is wrong because the puts on the acquirer and calls on the target pay off when the position is already winning, not when the deal fails.
> C is wrong because it accepts the reversed hedge in Statement 2.
> 3. **B.** The inflation accrual received on the inflation-linked bonds cancels the realized inflation paid on the swap, and the equal long and short positions require no net outlay.
> Net rate $= 2.45\% + 2.30\% - 4.05\% = 0.70\%$, or 70 bps, well above the usual premium, which is why the trade appears only in stressed markets.
> Annual net cash flow $= 0.0070 \times 40{,}000{,}000 = 280{,}000$.
> A is wrong because it ignores the inflation swap and compares the real yield directly with the nominal yield: $(2.45\% - 4.05\%) \times 40{,}000{,}000 = -640{,}000$.
> C is wrong because it adds the trailing inflation rate instead of the swap's fixed rate, counting the inflation accrual on the bonds while forgetting that the swap pays that inflation away: $(2.45\% + 3.10\% - 4.05\%) \times 40{,}000{,}000 = 1.50\% \times 40{,}000{,}000 = 600{,}000$.
> 4. **B.** A volatility swap is a forward contract on realized volatility; the buyer receives the vega notional times realized volatility minus the strike.
> Payoff $= 150{,}000 \times (21.4 - 16.0) = 150{,}000 \times 5.4 = 810{,}000$.
> The implied volatility on the expiry date is a decoy; the swap settles on realized volatility, which is why it gives pure volatility exposure without delta hedging.
> A is wrong because it uses the implied volatility at expiry instead of realized volatility: $150{,}000 \times (19.0 - 16.0) = 450{,}000$.
> C is wrong because it gives the seller's payoff; the desk bought the swap and receives realized volatility.

## Distractor design

- Q1: B uses the outside shareholders' percentage instead of the parent's ownership percentage; C reverses the direction of the subsidiary leg.
- Q2: B and C accept the reversed failure hedge (puts on the acquirer, calls on the target).
- Q3: A omits the inflation swap's fixed leg; C substitutes trailing inflation for the swap's fixed rate (misread exhibit).
- Q4: A uses implied volatility at expiry instead of realized volatility; C is a sign error (seller's payoff reported for the buyer).
