---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Graham and Dodd (1934) - Security Analysis, Graham (1973) - The Intelligent Investor (4th revised edition), Graham (1976) - A Conversation with Benjamin Graham, Greenwald Kahn Sonkin and van Biema (2001) - Value Investing: From Graham to Buffett and Beyond, Oppenheimer (1986) - Ben Graham's Net Current Asset Values: A Performance Update]
---

# Asset-Based, Liquidation, and Net-Net Valuation

## TL;DR

- Asset-based valuation values an enterprise based on the tangible liquidation value or replacement cost of its balance sheet assets rather than future speculative earning power.
- Benjamin Graham's Net Current Asset Value (NCAV) "Net-Net" framework values a firm strictly by taking Current Assets minus Total Liabilities, assigning zero value to all fixed and intangible assets.
- The buying rule usually attributed to Graham, and tested by Oppenheimer (1986), is a price at or below two-thirds of NCAV per share, a one-third margin of safety.
- Bruce Greenwald's Earnings Power Value (EPV) framework compares current sustainable earning power against the Asset Reproduction Cost to quantify whether a company possesses an economic moat.
- A net-net trading at a deep discount is only an attractive investment if its operating cash burn rate does not exhaust the cash reserve before an activist catalyst or liquidation event occurs (the "Melting Ice Cube" trap).

## Learning objectives

- Formulate and calculate Benjamin Graham's Net Current Asset Value (NCAV) and Net-Net Working Capital (NNWC).
- Apply orderly and forced liquidation haircut schedules across cash, accounts receivable, inventory, and equipment.
- Account for off-balance-sheet liquidation liabilities: severance obligations, lease cancellation penalties, and environmental remediation.
- Execute Bruce Greenwald's Asset Reproduction Cost analysis and compare it to Earnings Power Value (EPV) to detect economic moats.
- Calculate the Graham Number and evaluate its modern applicability across equity markets.
- Identify the structural failure modes of modern net-net investing, including cash burn rate and controlling shareholder entrenchment.

## Core concepts

### 1. Benjamin Graham's Net-Net Framework

In *Security Analysis* (1934), Benjamin Graham and David Dodd sought a margin of safety that did not rely on predicting future earnings or trusting managerial forecasts.
He developed the **Net Current Asset Value (NCAV)** metric:

$$\text{NCAV} = \text{Total Current Assets} - \text{Total Liabilities} - \text{Preferred Stock}$$

$$\text{NCAV Per Share} = \frac{\text{Total Current Assets} - \text{Total Liabilities} - \text{Preferred Stock}}{\text{Diluted Common Shares Outstanding}}$$

```
+-----------------------------------------------------------------------+
|                    THE GRAHAM NET-NET BALANCE SHEET                   |
+-----------------------------------------------------------------------+
| CURRENT ASSETS:                                                       |
| Cash + Short-Term Securities + Accounts Receivable + Inventory        |
|                                                                       |
| LESS: ALL LIABILITIES                                                 |
| - Accounts Payable & Accrued Expenses                                 |
| - Short-Term & Long-Term Debt                                         |
| - Lease Liabilities & Pension Deficits                                |
| - Preferred Stock Claims                                              |
|                                                                       |
| EQUALS: NET CURRENT ASSET VALUE (NCAV)                                |
|                                                                       |
| ZERO VALUE ASSIGNED TO:                                               |
| - Net Property, Plant & Equipment (Land, Buildings, Machinery: $0)    |
| - All Intangibles, Patents, and Goodwill: $0                          |
+-----------------------------------------------------------------------+
```

The two-thirds rule (as tested by Oppenheimer 1986):
Buy when Market Price $\le \frac{2}{3} \times \text{NCAV Per Share}$.
At this price, the investor buys net current assets at a one-third discount and pays nothing for property, plant and future earning power.
Graham (1976) said of buying below net current asset value that "over a 30-odd year period we must have earned an average of some 20 per cent per year from this source."

### 2. Conservative Net-Net Working Capital (NNWC)

To protect against distressed inventory and uncollectible receivables, a common modern convention takes the low end of Graham and Dodd's ranges for receivables and inventory:

$$\text{NNWC} = (\text{Cash} \times 1.0) + (\text{Receivables} \times 0.75) + (\text{Inventory} \times 0.50) - \text{Total Liabilities} - \text{Off-Balance-Sheet Claims}$$

```
+-----------------------------------------------------------------------+
|     GRAHAM AND DODD: APPROXIMATE LIQUIDATING VALUE (% OF BOOK)        |
+--------------------------------------+---------------+----------------+
| Asset class                          | Normal range  | Rough average  |
+--------------------------------------+---------------+----------------+
| Cash assets (securities at market)   | 100%          | 100%           |
| Receivables (less usual reserves)    | 75% - 90%     | 80%            |
| Inventories (lower of cost/market)   | 50% - 75%     | 66 2/3%        |
| Fixed and miscellaneous assets       | 1% - 50%      | about 15%      |
+--------------------------------------+---------------+----------------+
```

### 3. Orderly Liquidation Value (OLV) vs Forced Liquidation Value (FLV)

Asset-based valuation splits into two distinct operational wind-down regimes:

1. **Orderly Liquidation Value (OLV)**:
   - Assumes a managed wind-down over months, long enough to find buyers.
   - Allows management to conduct orderly inventory clearance sales and market real estate to strategic buyers.
2. **Forced Liquidation Value (FLV)**:
   - Assumes a rapid sale, typically at auction, with little time to market the assets.
   - High auctioneer discounts, fire-sale asset dispositions, and massive friction.

#### Off-Balance-Sheet Liquidation Liabilities
A naive liquidation model checks only balance sheet liabilities.
In a real corporate wind-down, massive liabilities crystallize that never appear on a going-concern balance sheet:
- **Employee Severance and WARN Act Liability**: the WARN Act requires 60 days' written notice of a covered plant closing (29 U.S.C. 2102), and an employer that fails to give it owes back pay for each day of violation up to 60 days (29 U.S.C. 2104).
- **Lease Rejection Claims**: Landlords can claim damages when a lease is rejected, but US Bankruptcy Code Section 502(b)(6) caps the claim at the rent for the greater of one year or 15% of the remaining term (not to exceed three years), plus unpaid rent.
- **Contract Cancellation Fees**: Penalties for terminating multi-year IT and supplier purchase agreements early.
- **Environmental Clean-Up Obligations**: Superfund or industrial site remediation costs that senior lenders cannot escape.

### 4. Bruce Greenwald's Asset Reproduction Cost and EPV

Greenwald, Kahn, Sonkin and van Biema (2001) compare **Asset Reproduction Cost** with **Earnings Power Value (EPV)**:

```
+-----------------------------------------------------------------------+
|                    THE GREENWALD MOAT SPECTRUM                        |
+-----------------------------------------------------------------------+
| CASE 1: EPV < Asset Reproduction Cost                                 |
| - The business earns less than its cost of capital.                   |
| - Industry has excess capacity; reproducing the assets is foolish.   |
| - Value is anchored by liquidation value.                             |
+-----------------------------------------------------------------------+
| CASE 2: EPV = Asset Reproduction Cost                                 |
| - The business earns exactly its cost of capital.                     |
| - No economic moat exists; entrants can duplicate assets and returns.|
| - Competitive equilibrium.                                            |
+-----------------------------------------------------------------------+
| CASE 3: EPV > Asset Reproduction Cost                                 |
| - The business earns substantial excess economic returns (ROIC > WACC)|
| - The spread (EPV - Reproduction Cost) MEASURES THE VALUE OF THE MOAT.|
| - Competitors cannot duplicate earnings power by buying the assets.   |
+-----------------------------------------------------------------------+
```

#### How to Calculate Reproduction Cost:
1. Estimate current replacement cost of physical plant, property, and equipment (adjusting for inflation and technology).
2. Calculate the capital required to recreate the customer base (historical Customer Acquisition Cost $\times$ active customers).
3. Capitalize the cost of training the workforce and building the organizational software architecture.

### 5. The Graham Number

In Chapter 14 of *The Intelligent Investor* (4th revised edition, 1973), Graham suggests for the defensive investor that "the product of the multiplier times the ratio of price to book value should not exceed 22.5"; the Graham Number is the price at which that product equals 22.5:

$$\text{Maximum Price} = \sqrt{22.5 \times \text{EPS} \times \text{BVPS}}$$

Where:
- 22.5 represents the product of a maximum allowable P/E of $15.0\times$ and a maximum allowable P/B of $1.5\times$ ($15.0 \times 1.5 = 22.5$).
- A price below the Graham Number means P/E times P/B is below 22.5; it does not mean both limits hold separately.
- With EPS 2 and BVPS 20 the Graham Number is $\sqrt{900} = 30$ (P/E 15, P/B 1.5); with EPS 1 and BVPS 40 it is also 30, but at that price P/E is 30 and P/B is 0.75.

### 6. The Melting Ice Cube Trap: Modern Failure Modes of Net-Nets

Graham's recollection of about 20% a year (quoted in section 1) describes his own record over three decades; it does not explain the result, and it does not carry over automatically to today's net-nets.
In modern markets, buying a net-net without analyzing the **burn rate** is catastrophic:

$$\text{Months of Runway} = \frac{\text{Net Cash \& Liquid Assets}}{\text{Monthly Negative Operating Cash Flow (Burn Rate)}}$$

If a company has $50M in NCAV and trades at a $30M market cap (hypothetical figures), but burns $20M in operating cash each year, NCAV is gone in 2.5 years.
Unless an activist intervenes or management stops the burn, the asset cushion that justified the purchase disappears.

## Worked numerical case study

Analyze MicroTech Hardware Corp (a hypothetical company; every figure below is hypothetical):
- Shares Outstanding: 10.0M
- Current Market Share Price: $3.50 (Market Cap = $35.0M)
- Cash and Cash Equivalents: $20.0M
- Short-Term Treasury Bills: $10.0M
- Accounts Receivable: $15.0M
- Finished Goods Inventory: $20.0M
- Work-in-Process (WIP) Inventory: $10.0M
- Net PP&E (Factory and Equipment): $30.0M
- Goodwill & Patents: $15.0M
- Total Assets: $120.0M
- Accounts Payable: $12.0M
- Accrued Liabilities: $8.0M
- Total Debt (Bank Line): $10.0M
- Total Balance Sheet Liabilities: $30.0M
- Monthly Operating Cash Burn: $1.2M / month ($14.4M / year)

### Off-Balance-Sheet Wind-Down Estimates:
- Plant lease termination penalty: $4.0M
- Employee severance (150 factory workers): $3.0M
- Professional legal & liquidation fees: $2.0M
- Total Contingent Wind-Down Liabilities: $9.0M

### Step 1: Compute Standard Benjamin Graham NCAV
Current Assets = $\text{Cash } (20) + \text{T-Bills } (10) + \text{AR } (15) + \text{Inv } (30) = \$75.0\text{M}$
Total Balance Sheet Liabilities = $30.0M

$$\text{NCAV} = \$75.0\text{M} - \$30.0\text{M} = \$45.0\text{M}$$
$$\text{NCAV Per Share} = \frac{\$45.0\text{M}}{10.0\text{M}} = \$4.50$$
Graham 2/3 Buy Threshold = $\frac{2}{3} \times \$4.50 = \$3.00$.
(At $3.50, the stock trades at $0.78\times$ NCAV, appearing cheap to a novice).

### Step 2: Compute Conservative Net-Net Working Capital (NNWC)
- Cash & Treasuries (100%): $30.0M
- Accounts Receivable (75%): $\$15.0\text{M} \times 0.75 = \$11.25\text{M}$
- Finished Goods Inventory (50%): $\$20.0\text{M} \times 0.50 = \$10.0M$
- WIP Inventory (10%, below Graham and Dodd's inventory range because unfinished goods are hard to sell): $\$10.0\text{M} \times 0.10 = \$1.0M$
- Total Haircutted Liquid Assets: $\$30.0 + \$11.25 + \$10.0 + \$1.0 = \$52.25\text{M}$
- Less Balance Sheet Liabilities: -$30.0M

$$\text{NNWC} = \$52.25\text{M} - \$30.0\text{M} = \$22.25\text{M}$$
$$\text{NNWC Per Share} = \frac{\$22.25\text{M}}{10.0\text{M}} = \$2.225$$

### Step 3: Compute Forced Liquidation Value (FLV)
- Haircutted Assets: $52.25M
- Net PP&E (Auction scrap at 20%): $\$30.0\text{M} \times 0.20 = \$6.0M$
- Gross Liquidated Cash: $\$52.25\text{M} + \$6.0\text{M} = \$58.25\text{M}$
- Less Balance Sheet Liabilities: -$30.0M
- Less Off-Balance-Sheet Wind-Down Claims: -$9.0M

$$\text{Net Forced Liquidation Value} = \$58.25\text{M} - \$30.0\text{M} - \$9.0\text{M} = \$19.25\text{M}$$
$$\text{FLV Per Share} = \frac{\$19.25\text{M}}{10.0\text{M}} = \$1.925$$

For comparison, Graham and Dodd's rough-average percentages (cash 100%, receivables 80%, inventories 66 2/3%, fixed assets 15%, goodwill zero) give liquidating assets of $66.5M and $3.65 per share after balance-sheet liabilities, or $2.75 after the $9.0M wind-down claims; their low and high ends give $2.655 and $5.10 per share before those claims.

### Step 4: The Burn Rate Sanity Check
- Net Cash Available ($30M cash - $10M debt): $20.0M
- Annual Burn Rate: $14.4M per year ($1.2M / month)
- Operational Runway:
  $$\text{Runway} = \frac{\$20.0\text{M}}{\$14.4\text{M / year}} = 1.39 \text{ years (16.7 months)}$$

Forensic Verdict:
MicroTech is a classic Melting Ice Cube.
While Graham NCAV is $4.50 (above the $3.50 share price), forced liquidation value is only $1.925.
Furthermore, with 16.7 months of cash runway at the current burn, the net cash is gone within a year and a half unless the burn stops or an activist forces a liquidation.
At $3.50, the stock is an avoid or short candidate.

## Practice questions

> [!question]- mkt-val-161 | What is Benjamin Graham's Net Current Asset Value (NCAV)?
> NCAV = Total Current Assets - Total Liabilities - Preferred Stock, assigning zero value to all fixed and intangible assets.

> [!question]- mkt-val-162 | What was Benjamin Graham's operational threshold for purchasing net-net stocks?
> The rule usually attributed to him, and tested by Oppenheimer (1986), is to buy at or below two-thirds of NCAV per share, a one-third margin of safety.

> [!question]- mkt-val-163 | How does Net-Net Working Capital (NNWC) differ from NCAV?
> NNWC applies liquidation haircuts to working capital line items (commonly 75% on receivables and 50% on inventory, the low ends of Graham and Dodd's ranges) rather than full face value.

> [!question]- mkt-val-164 | What weight does Graham assign to Property, Plant, and Equipment (PP&E) in a net-net calculation?
> Zero weight (0%), treating all physical plant, machinery, and land as a free call option.

> [!question]- mkt-val-165 | What is the 'Melting Ice Cube' trap in net-net investing?
> When a company trading below liquidation value burns operational cash so rapidly that the asset buffer is exhausted before value can be realized.

> [!question]- mkt-val-166 | What is the formula for calculating operational cash runway for a loss-making net-net?
> Runway in Months = Net Liquid Cash / Monthly Operating Cash Burn Rate.

> [!question]- mkt-val-167 | What is the difference between Orderly Liquidation Value (OLV) and Forced Liquidation Value (FLV)?
> OLV assumes a managed disposition with time to find buyers; FLV assumes a rapid sale, typically at auction, so recoveries are lower.

> [!question]- mkt-val-168 | What typical haircut is applied to Work-in-Process (WIP) inventory in forced liquidation?
> There is no standard figure; appraisers estimate it case by case, and it is usually well below finished goods because unfinished goods must be completed or sold as scrap.
> The worked case here assumes a hypothetical 10% recovery.

> [!question]- mkt-val-169 | What off-balance-sheet liabilities must be incorporated into a liquidation valuation?
> Employee severance liabilities, lease cancellation penalties, pension deficits, and contract termination fees.

> [!question]- mkt-val-170 | What is the statutory limitation on landlord lease rejection claims under US Bankruptcy Code Section 502(b)(6)?
> The rent reserved by the lease for the greater of one year or 15% (not to exceed three years) of the remaining lease term.

> [!question]- mkt-val-171 | What is Bruce Greenwald's Asset Reproduction Cost?
> The estimated capital outlay required today to duplicate all operating assets, customer relationships, and organizational systems of a firm from scratch.

> [!question]- mkt-val-172 | What is Greenwald's Earnings Power Value (EPV)?
> The present value of current normalized operating earnings assuming zero future growth, capitalized at the cost of capital: EPV = Normalized NOPAT / WACC.

> [!question]- mkt-val-173 | How does comparing EPV to Reproduction Cost detect an economic moat?
> If EPV substantially exceeds Asset Reproduction Cost, the company possesses a sustainable competitive advantage that competitors cannot duplicate by buying assets.

> [!question]- mkt-val-174 | What does it signify if a company's EPV is significantly less than its Asset Reproduction Cost?
> The industry suffers from overcapacity and destructive competition, earning returns below the cost of capital and destroying shareholder wealth.

> [!question]- mkt-val-175 | What is the Graham Number formula?
> Square Root of (22.5 * EPS * Book Value Per Share); 22.5 is Graham's cap on P/E times P/B in The Intelligent Investor (1973, Ch. 14), corresponding to 15 times earnings and 1.5 times book.

> [!question]- mkt-val-176 | How would you find out which market currently has the most classic net-net stocks?
> Run a dated screen of price below NCAV per share across markets, count the hits per market and check them by hand for stale data, cross-shareholdings and minority-hostile controllers.
> Do not rely on a remembered answer; the count changes with market levels and accounting rules.

> [!question]- mkt-val-177 | What role do activist investors play in net-net investing?
> Activists act as catalysts by acquiring stakes and forcing management to liquidate unprofitable operations, sell real estate, or return excess cash to shareholders.

> [!question]- mkt-val-178 | What is the risk of an entrenched founder or controlling family in a net-net company?
> Insiders may pay themselves excessive salaries, perpetually consuming cash and refusing to liquidate, trapping minority shareholders in an illiquid discount.

> [!question]- mkt-val-179 | Why did Graham advocate holding a diversified basket of net-nets rather than concentrating in 2 or 3?
> Because individual net-nets carry large idiosyncratic risk of failure; a diversified basket lets the group's average re-rating show through.

> [!question]- mkt-val-180 | What is tangible book value per share (TBVPS)?
> (Total Shareholders' Equity - Goodwill - Identifiable Intangible Assets) / Diluted Shares Outstanding.

> [!question]- mkt-val-181 | Why is tangible book value more reliable than standard book value for distressed asset analysis?
> Because goodwill and capitalized intangibles have zero liquidation value in bankruptcy and are completely written off.

> [!question]- mkt-val-182 | How should marketable securities be valued in a liquidation schedule?
> Mark to market at current exchange prices (Graham and Dodd count securities at market value with cash), less estimated selling costs and any discount needed to sell a large block quickly.

> [!question]- mkt-val-183 | What is a 'cigar butt' stock according to Warren Buffett?
> Buffett's 1989 letter: "A cigar butt found on the street that has only one puff left in it may not offer much of a smoke, but the 'bargain purchase' will make that puff all profit."

> [!question]- mkt-val-184 | Why did Warren Buffett abandon pure net-net investing in favor of quality businesses?
> In the 1989 letter he gives two reasons: the bargain price rarely proves a steal because "never is there just one cockroach in the kitchen", and "any initial advantage you secure will be quickly eroded by the low return that the business earns".
> He summarizes: "Time is the friend of the wonderful business, the enemy of the mediocre."

> [!question]- mkt-val-185 | How does inflation impact the gap between historical book value and Asset Reproduction Cost?
> Inflation causes replacement cost of plant and real estate to substantially exceed historical depreciated book value.

> [!question]- mkt-val-186 | What is the 'clean surplus' relation in accounting-based valuation?
> Ending Book Value = Beginning Book Value + Net Income - Net Dividends, linking income statement earnings directly to balance sheet asset evolution.

> [!question]- mkt-val-187 | Why are customer acquisition costs (CAC) included in Asset Reproduction Cost?
> An entrant attempting to duplicate the incumbent's revenue must spend capital on marketing and sales to acquire an equivalent customer base.

> [!question]- mkt-val-188 | What is the liquidation haircut for finished goods inventory in a fashion retail bankruptcy?
> Usually severe, because seasonal apparel loses value quickly; there is no standard figure, so use a liquidator's appraisal or recoveries from comparable liquidations.

> [!question]- mkt-val-189 | What is debtor-in-possession (DIP) financing in corporate bankruptcy?
> New financing for a Chapter 11 debtor approved by the court under Bankruptcy Code section 364, which can grant it administrative or superpriority status and, with adequate protection for existing lienholders, a priming lien ahead of them.

> [!question]- mkt-val-190 | Why do equity holders frequently receive zero in a Chapter 7 liquidation?
> Because in Chapter 7 secured creditors are paid from their collateral and the rest of the estate goes in order to administrative and other priority claims, then general unsecured creditors, and only any surplus to equity (Bankruptcy Code sections 507 and 726).

> [!question]- mkt-val-191 | What is a rights offering and how is it used by distressed asset-rich companies?
> Offering existing shareholders the right to buy new shares at a discount to raise emergency equity cash and avoid formal bankruptcy.

> [!question]- mkt-val-192 | What is the ultimate lesson of asset-based valuation?
> Assets protect the downside only if they can be liquidated or monetized before operating losses consume them.

> [!question]- mkt-val-263 | Apply Graham and Dodd's rough-average liquidating percentages (cash 100%, receivables 80%, inventories 66 2/3%, fixed assets 15%, goodwill zero) to MicroTech. What is the value per share?
> Assets: 30 + 0.8 x 15 + (2/3) x 30 + 0.15 x 30 = 66.5, less 30 of liabilities = 36.5, or $3.65 per share.
> After the $9.0M of wind-down claims it is $2.75, below the $3.50 price.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_val_06_net_net.py`](../../code/mkt_val_06_net_net.py) prints and asserts every number on this page: NCAV, NNWC and forced liquidation value in exact fractions (NCAV also from total assets), the runway by a month-by-month burn simulation, the Graham and Dodd liquidating values at their low, average and high percentages, and the Graham Number examples.
- Related notes: [Specialized Valuation](07-Specialized-Valuation-Financials-Cyclicals-and-Loss-Makers.md).

## Further reading

- Berkshire Hathaway. Chairman's letter to shareholders, 1989. berkshirehathaway.com/letters/1989.html.
- Graham, B. (1973). *The Intelligent Investor* (4th rev. ed.). Harper & Row. Ch. 14 (stock selection for the defensive investor).
- Graham, B. (1976). A conversation with Benjamin Graham. *Financial Analysts Journal*, 32(5), 20-23.
- Graham, B., & Dodd, D. L. (1934). *Security Analysis*. McGraw-Hill (2nd ed. 1940).
- Greenwald, B. C., Kahn, J., Sonkin, P. D., & van Biema, M. (2001). *Value Investing: From Graham to Buffett and Beyond*. John Wiley & Sons.
- Oppenheimer, H. R. (1986). Ben Graham's net current asset values: A performance update. *Financial Analysts Journal*, 42(6), 40-47.
- Whitman, M. J., & Diz, F. (2009). *Distress Investing: Principles and Technique*. John Wiley & Sons.
