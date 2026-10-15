---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 3
title: "Sablewood Partners: Overlaying a Cash Buffer with ETFs"
los: [los-09-03-a, los-09-03-f, los-09-03-g, los-09-03-h]
difficulty: 4
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Sablewood Partners: Overlaying a Cash Buffer with ETFs

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Nadia Feldmann, CFA, is a portfolio strategist at Sablewood Partners, an outsourced chief investment office for nonprofit institutions.
One client, the Harrowgate Arts Foundation, has a USD 360 million global ex-US equity sleeve run by two external managers.
To meet grant payments and capital calls, the sleeve keeps an average cash balance equal to 5% of its value in a money market account.
Last year the sleeve's benchmark returned 12.4%, the money market account yielded 4.6%, and the two managers together returned 11.9% before fees.

Feldmann proposes that the foundation buy an ETF tracking the sleeve's benchmark with the full cash balance at the start of next year, hold it for 12 months, and sell it at year-end.
The ETF's exchange liquidity would still let the foundation raise cash for grants at short notice.
For her base case she assumes that next year's benchmark return and cash yield will equal last year's, that cash drag equals the cash weight multiplied by the difference between the benchmark return and the cash yield, and that the ETF earns the benchmark return before its own costs.

Tobias Reyes, Sablewood's head trader, gathers data on two ETFs that track the benchmark.

Exhibit 1: Candidate ETFs

| | ETF G | ETF H |
|---|---|---|
| Sponsor | Talbrook Funds | Castlemont Investments |
| Share price | USD 32.00 | USD 64.00 |
| Commission per share, each way | USD 0.0080 | USD 0.0064 |
| Quoted bid-ask spread | 0.12% | 0.03% |
| Annual management fee | 0.08% | 0.22% |
| Annualized 12-month tracking error | 0.09% | 0.06% |
| Median daily volume | USD 38 million | USD 1.6 billion |
| Assets under management | USD 410 million | USD 22.5 billion |
| Creation unit | 50,000 shares | 50,000 shares |
| Creation or redemption fee per unit | USD 4,000 | USD 500 |
| AP cost to buy the creation basket | 0.10% of basket value | 0.03% of basket value |
| AP cost to sell the redemption basket | 0.07% of basket value | 0.02% of basket value |

Reyes explains his method: "I compare the two funds on total holding-period cost, excluding compounding.
I charge commissions on the purchase and on the sale, one full quoted bid-ask spread for the round trip, and the management fee prorated for the months held.
Because ETF G has the lower fee but the higher trading cost, there is a holding period beyond which it becomes the cheaper fund."

Reyes will buy the whole position in one order on the first trading day of the year.
On-screen depth in either fund will not absorb an order of that size, so he will ask an authorized participant to fill it at a single price with newly created shares.
He assumes that the iNAV at the time of the trade equals the share price in Exhibit 1, that the AP can trade the creation basket at the cost shown, and that the AP requires no compensation beyond covering its costs.

Reyes adds that Talbrook Funds, a subsidiary of a regional bank whose one-year credit default swap spread is 1.1%, is reported to be in merger talks with Castlemont Investments.
Industry analysts expect a combined firm to close the smaller of any two overlapping funds.
Feldmann asks Reyes for a stress case in which the foundation holds ETF G for six months, sells it on the exchange before its closing date, and buys ETF H for the remaining six months.

## Questions

1. Using Reyes's method, the holding period beyond which ETF G has the lower total holding-period cost is closest to: (LOS: los-09-03-f)
   - A. 9.0 months.
   - B. 10.3 months.
   - C. 18.0 months.
2. In the base case, the expected net annual benefit to the foundation of Feldmann's proposal, implemented with the ETF that has the lower 12-month holding-period cost, is closest to: (LOS: los-09-03-h)
   - A. USD 0.50 million.
   - B. USD 1.36 million.
   - C. USD 2.19 million.
3. For the ETF used in Question 2, the lowest price per share at which an AP could fill Reyes's order with newly created shares without a loss, and the party that bears the creation costs, are: (LOS: los-09-03-a)
   - A. USD 32.03, borne by the foundation through the price it pays.
   - B. USD 32.11, borne by the foundation through the price it pays.
   - C. USD 32.11, borne by all ETF G shareholders in proportion to their holdings.
4. In Feldmann's stress case, the total 12-month cost of the overlay as a percentage of the amount invested, and the risk that the stress case illustrates, are closest to: (LOS: los-09-03-g)
   - A. 0.37%, and fund-closure risk.
   - B. 0.52%, and fund-closure risk.
   - C. 0.37%, and counterparty risk.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Convert commissions to percentages: ETF G $0.0080/32.00 = 0.0250\%$ each way; ETF H $0.0064/64.00 = 0.0100\%$ each way.
>    Round-trip trading cost: ETF G $2 \times 0.0250\% + 0.12\% = 0.1700\%$; ETF H $2 \times 0.0100\% + 0.03\% = 0.0500\%$.
>    Set the holding-period costs equal: $0.17 + \frac{m}{12}(0.08) = 0.05 + \frac{m}{12}(0.22)$, so $m = \frac{12 \times (0.17 - 0.05)}{0.22 - 0.08} = \frac{1.44}{0.14} = 10.2857$ months.
>    A is wrong because it charges the commission only once: round trips of $0.025 + 0.12 = 0.145\%$ and $0.010 + 0.03 = 0.040\%$ give $12 \times 0.105/0.14 = 9.0$ months.
>    C is wrong because it charges the full spread on the purchase and again on the sale: round trips of $0.05 + 0.24 = 0.29\%$ and $0.02 + 0.06 = 0.08\%$ give $12 \times 0.21/0.14 = 18.0$ months.
> 2. **B.** The 12-month holding is beyond the 10.2857-month break-even, so ETF G is cheaper: $0.17 + 0.08 = 0.25\%$ against $0.05 + 0.22 = 0.27\%$ for ETF H.
>    Cash equitized $= 0.05 \times 360 = 18.0$ million.
>    Cash drag avoided $= 18.0 \times (12.4\% - 4.6\%) = \text{USD } 1{,}404{,}000$.
>    ETF cost $= 18.0 \text{ million} \times 0.25\% = \text{USD } 45{,}000$.
>    Net benefit $= 1{,}404{,}000 - 45{,}000 = \text{USD } 1{,}359{,}000$, about USD 1.36 million.
>    Investing the cash buffer in a liquid benchmark ETF to stay fully invested is cash equitization, and the benefit dwarfs the ETF's costs.
>    A is wrong because it applies the ETF's cost to the whole USD 360 million sleeve rather than to the USD 18 million invested: $1{,}404{,}000 - 900{,}000 = \text{USD } 504{,}000$.
>    C is wrong because it ignores the yield the cash already earns: $18.0 \times 12.4\% - 0.045 = \text{USD } 2.187$ million.
>    Using ETF H instead gives $1{,}404{,}000 - 48{,}600 = \text{USD } 1{,}355{,}400$, which also rounds to USD 1.36 million, so the fund choice matters little here; it matters in Questions 3 and 4.
>    The managers' 11.9% return is a decoy; the drag is measured against the benchmark the ETF tracks.
> 3. **B.** To create, the AP buys the creation basket and pays the creation fee, so its break-even selling price is iNAV plus both costs per share.
>    Basket cost per share $= 32.00 \times 0.0010 = 0.0320$; creation fee per share $= 4{,}000/50{,}000 = 0.0800$.
>    Break-even price $= 32.00 + 0.0320 + 0.0800 = \text{USD } 32.1120$, a premium of $0.1120/32.00 = 0.3500\%$ to iNAV, which is the upper edge of the arbitrage band.
>    The AP passes its basket trading costs and creation fee to the transacting investor through the price, so the foundation bears them and existing ETF G shareholders are shielded.
>    A is wrong because it omits the creation fee: $32.00 \times 1.0010 = \text{USD } 32.032$.
>    C is wrong because spreading transaction costs across all holders is the mutual fund outcome; in an ETF the costs of entry fall on the investor who enters.
>    The redemption-side costs (0.07% and the redemption fee) are decoys; they bound the discount side of the band, not a creation.
> 4. **A.** Stress-case cost $= \text{RT}_G + \frac{6}{12} \times 0.08\% + \text{RT}_H + \frac{6}{12} \times 0.22\% = 0.17 + 0.04 + 0.05 + 0.11 = 0.37\%$, or USD 66,600 on USD 18 million.
>    That is above the 0.27% cost of holding ETF H all year, so if closure became likely, the higher-fee fund would be the cheaper choice.
>    A fund shut down because of a corporate action such as a merger of ETF sponsors illustrates fund-closure risk, whose drivers are regulation, competition, and corporate actions.
>    B is wrong because it charges each fund a full year's fee instead of six months each: $0.17 + 0.08 + 0.05 + 0.22 = 0.52\%$.
>    C is wrong because counterparty risk is the default exposure of an ETN holder to its issuer or of a fund to a swap or lending counterparty; the stress case is a business decision to close the fund, and the 1.1% CDS spread on Talbrook's parent is a decoy, well below the 5% level that signals significant default risk.

## Distractor design

1. A: commission charged once instead of on purchase and sale; C: full spread charged on purchase and again on sale.
2. A: fund cost applied to the whole sleeve instead of the cash equitized; C: cash yield ignored in the cash drag.
3. A: creation fee omitted from the AP's break-even price; C: mutual fund cost sharing attributed to an ETF.
4. B: annual fees not prorated for two six-month holdings; C: sponsor business risk mislabeled as counterparty risk.
