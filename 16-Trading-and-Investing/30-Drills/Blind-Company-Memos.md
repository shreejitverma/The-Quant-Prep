---
type: guide
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Enron Corp Form 10-K for 2000 and Form 10-Q for Q1 2001, Amazon.com Form 10-K for 2001 and 2002, Valeant Pharmaceuticals Form 10-K for 2015 and Bausch Health Form 10-K for 2017, Costco Wholesale Form 10-K for fiscal 2010, Hertz Global Holdings Form 10-K for 2019 and 2020 and Form 10-Q for Q1 2020 and press release of June 10 2021, Apple Computer Form 10-K for fiscal 2003, Report of Investigation of the Special Investigative Committee of the Board of Enron Corp (Powers Report) February 1 2002]
---

# Blind Company Investment Memos

## Overview

The Blind Company Memos bank trains investors and quantitative analysts to evaluate business fundamentals and balance sheet realities free from brand bias, management halo effects, or popular media narratives.
Each case presents financial statements, operating facts and debt structures from a pivotal moment in a real company's history, with the company's name withheld.
Analyze the evidence, select an investment decision (BUY, SHORT, or PASS), and formulate your core thesis before revealing the identity and what happened next.

Every figure in the financial profiles is copied from the company's own SEC filing named in the reveal, in US dollars, with fiscal years as the company reports them.
Every ratio in the questions and solutions is recomputed and asserted by the backing script listed at the end.
Prices labelled "hypothetical entry price" are chosen inside the filed trading range only to illustrate a valuation; they are not quotes.

---

## Case 1: The Energy Trading Conglomerate (Year 2000)

### Financial Profile (Figures in Millions)
```
+-----------------------------------------------------------------------+
| Metric                                   | Year t-2  | Year t-1 | Year t  |
|------------------------------------------+-----------+----------+---------|
| Total Revenues                           | $31,260   | $40,112  | $100,789|
| Operating Income                         | $1,378    | $802     | $1,953  |
| Income Before Interest, Minority         |           |          |         |
|   Interests and Income Taxes             | $1,582    | $1,995   | $2,482  |
| Net Income                               | $703      | $893     | $979    |
| Cash Flow from Operations (CFO)          | $1,640    | $1,228   | $4,779  |
| Capital Expenditures                     | $1,905    | $2,363   | $2,381  |
| Short- and Long-Term Debt                | $7,357    | $8,152   | $10,229 |
| Total Assets                             | $29,350   | $33,381  | $65,503 |
+-----------------------------------------------------------------------+
| Interim: first quarter of Year t and Year t+1                         |
| Q1 Year t:   Net Income $338, CFO -$457                               |
| Q1 Year t+1: Net Income $425, CFO -$464                               |
+-----------------------------------------------------------------------+
```

### Business and Operational Context
- **Industry**: A natural gas pipeline company that has become a wholesale trader and market-maker in gas, electricity, metals and broadband capacity.
- **Revenue Growth**: Total revenues rose 151.3% in Year t, and total assets rose 96.2%.
- **Accounting Method**: Energy trading contracts are accounted for on a mark-to-market (fair value) basis, with gains and losses included in revenues, so the estimated value of long-dated contracts is recognised before the cash arrives.
- **Related Parties**: A related-party footnote discloses transactions with limited partnerships whose general partner's managing member is a senior officer of the company.
In Year t the company contributed assets valued at about $1.2 billion to newly formed entities, including its own notes and its own restricted common stock, and those entities were used to hedge the company's merchant investments.
- **Cash Flow Commentary**: Management attributes the Year t jump in operating cash flow to working capital changes, operating results "and a receipt of cash associated with the assumption of a contractual obligation".
- **Valuation**: At the Year t high of $90.75, the stock traded at 81.0x diluted EPS of $1.12 and 5.95x year-end book value per share of $15.25.

### Questions to Solve
1. Calculate the CFO-to-Net Income ratio for each year and for both first quarters.
2. Identify the contradiction between the full-year cash flow and the quarterly cash flow pattern.
3. Identify what the related-party footnote implies about the quality of the hedges protecting reported earnings.
4. Formulate your investment recommendation: BUY, SHORT, or PASS.

<details>
<summary>Reveal True Identity & Historical Outcome</summary>

#### Forensic Audit Analysis
1. CFO-to-Net Income was 2.33 (Year t-2), 1.38 (Year t-1) and 4.88 (Year t), which looks excellent at first glance.
2. The quarterly pattern contradicts it: CFO-to-Net Income was -1.35 in Q1 of Year t and -1.09 in Q1 of Year t+1.
Subtracting the first quarter from the full year, the last nine months of Year t produced $5,236 million of operating cash, so the full-year figure depended on cash arriving late in the year, partly from what management itself called the assumption of a contractual obligation.
Cash received for taking on an obligation behaves like borrowing, even when it is reported as operating cash flow.
3. Hedges written by entities capitalised with the company's own stock are only as good as that stock: if the share price falls, the hedge counterparty weakens at exactly the moment the hedged investments lose value.
4. Mark-to-market revenue on long-dated, illiquid contracts lets reported earnings run ahead of cash, so earnings quality cannot be judged from net income.

#### True Identity
**Enron Corp. (fiscal 2000)**.
- **Leadership in the 2000 10-K**: Kenneth Lay (Chairman, CEO until February 2001) and Jeffrey Skilling (President and COO, CEO from February 2001).
- **CFO**: Andrew Fastow, identified in the Powers Report as the senior officer running the LJM partnerships.

#### Historical Performance
- On October 16, 2001, Enron reported third-quarter charges and a reduction in shareholders' equity tied to the related-party entities.
- On November 8, 2001, Enron announced it would restate its financial statements for 1997 through 2000.
- Enron filed for Chapter 11 on December 2, 2001.
- The Powers Report (February 1, 2002) concluded that the related-party transactions were used to keep debt off the balance sheet and to offset losses on merchant investments.
- Arthur Andersen, Enron's auditor, was convicted of obstruction of justice in June 2002; the Supreme Court reversed the conviction in 2005 (Arthur Andersen LLP v. United States), but the firm had already ceased auditing public companies.

#### Optimal Decision
**SHORT or, at minimum, PASS**.
The disclosed facts were enough: fair-value revenue on illiquid contracts, operating cash that was negative in both first quarters shown and concentrated late in the year, and hedges backed by the company's own stock through partnerships run by its CFO.

</details>

---

## Case 2: The Cash-Burning E-Commerce Platform (Year 2001)

### Financial Profile (Figures in Millions)
```
+-----------------------------------------------------------------------+
| Metric                                   | Year t-2  | Year t-1 | Year t |
|------------------------------------------+-----------+----------+--------|
| Net Sales                                | $1,640    | $2,762   | $3,122 |
| Gross Margin                             | 17.7%     | 23.7%    | 25.6%  |
| Loss from Operations                     | -$606     | -$864    | -$412  |
| Net Loss                                 | -$720     | -$1,411  | -$567  |
| Cash Flow from Operations (CFO)          | -$91      | -$130    | -$120  |
| Purchases of Fixed Assets                | $287      | $135     | $50    |
| Cash and Marketable Securities           | $706      | $1,101   | $997   |
| Long-Term Debt (mostly convertible)      | $1,466    | $2,127   | $2,156 |
| Stockholders' Equity (Deficit)           | $266      | -$967    | -$1,440|
+-----------------------------------------------------------------------+
```

### Business and Operational Context
- **Macro Environment**: The dot-com bubble has burst and equity markets are largely closed to unprofitable internet companies.
- **Working Capital Dynamics**: On average Year t balances, inventory represented 25.0 days of cost of sales and accounts payable 73.0 days, so suppliers financed about 48 days of the cost of goods the company sold.
- **Cost Discipline**: Purchases of fixed assets fell from $287 million to $50 million as the fulfillment-center buildout ended.
- **Cash Reconciliation**: In Year t the net loss of $567 million was offset by $412 million of adjustments not affecting cash (mainly amortization of goodwill and intangibles, depreciation, restructuring charges and equity-method losses) and $36 million of working-capital inflows.
- **Valuation**: The stock traded between $5.97 and $21.88 during Year t, against a high of $91.50 in the first quarter of Year t-1, a 93.5% fall from that high to the Year t low.
At a hypothetical entry price of $8.00 and 373.3 million shares, market value is $2,986 million and enterprise value is $4,146 million, or 1.33x Year t sales.

### Questions to Solve
1. Explain how a company reporting a Net Loss of $567 million used only $120 million of operating cash.
2. Calculate Year t free cash flow (CFO less purchases of fixed assets) and the years of cash runway at that burn rate.
3. Explain what the negative working-capital cycle implies if sales keep growing.
4. Formulate your investment recommendation: BUY, SHORT, or PASS.

<details>
<summary>Reveal True Identity & Historical Outcome</summary>

#### Fundamental Analysis
1. Most of the accounting loss was non-cash: $412 million of the $567 million came from amortization, depreciation, restructuring and equity-method losses that consumed no cash in the year.
2. Free cash flow was $-120 - 50 = -\$170$ million, so $997 million of cash and marketable securities covers about 5.9 years of burn at the Year t rate.
3. With payables at 73.0 days against inventory at 25.0 days, each extra dollar of sales brings supplier cash in before the goods are paid for, so growth funds itself rather than draining cash.
4. The risks are real: stockholders' equity is a $1,440 million deficit and $2,156 million of long-term debt is outstanding, so the case rests on the cash runway and the working-capital float rather than on the balance sheet.

#### True Identity
**Amazon.com, Inc. (fiscal 2001)**.
- **Founder and CEO**: Jeff Bezos.

#### Historical Performance
- In fiscal 2002 net cash provided by operating activities turned positive at $174 million (Form 10-K for 2002), from a net loss of $149 million offset by $284 million of non-cash adjustments and $40 million of working-capital inflows.

#### Optimal Decision
**BUY, sized for the balance-sheet risk**.
The headline GAAP loss overstated the cash burn, the runway was several years long, and the negative working-capital cycle meant growth would generate rather than consume cash.

</details>

---

## Case 3: The Specialty Pharmaceutical Roll-Up (Year 2015)

### Financial Profile (Figures in Millions)
```
+-----------------------------------------------------------------------+
| Metric                                   | Year t-2  | Year t-1 | Year t  |
|------------------------------------------+-----------+----------+---------|
| Revenues                                 | $5,769.6  | $8,206.0 | $10,446.5|
| Operating Income (Loss)                  | -$409.5   | $2,000.7 | $1,527.4|
| Net Income (Loss) to Shareholders        | -$866.1   | $880.7   | -$291.7 |
| Research and Development Expense         | $156.8    | $246.0   | $334.4  |
| Long-Term Debt incl. Current Portion     | $17,329.8 | $15,228.9| $31,088.4|
| Goodwill plus Intangible Assets, Net     | n/a       | $20,639.3| $41,635.8|
| Total Assets                             | $27,932.9 | $26,304.7| $48,964.5|
| Shareholders' Equity                     | $5,118.7  | $5,279.4 | $5,911.0|
+-----------------------------------------------------------------------+
```
Year t-1 is shown as restated in the Year t filing.

### Business and Operational Context
- **Business Model**: Growth by debt-financed acquisition of pharmaceutical companies, with research spending of 2.72%, 3.00% and 3.20% of revenue over the three years, a small fraction of what research-based drug companies spend.
- **Pricing**: The company's pricing decisions on particular drugs are under investigation by the US Senate Special Committee on Aging and the House Committee on Oversight and Government Reform, and the North Carolina Department of Justice is investigating the pricing of Nitropress, Isuprel and Cuprimine.
- **Balance Sheet Risk**: Long-term debt more than doubled in Year t (+104.1%) to $31.1 billion, 5.26 times shareholders' equity.
Goodwill and intangibles are 85.0% of total assets, so tangible equity is -$35,724.8 million.
- **Distribution Channel**: On December 15, 2014 the company took an option to acquire a specialty pharmacy network and began consolidating it as a variable interest entity; sales to that network before the option were later found to have been recognised too early.
- **Valuation**: The stock reached $263.81 on the NYSE in the third quarter of Year t, roughly $90.5 billion of market value on 342.9 million shares.

### Questions to Solve
1. Assess the sustainability of a drug company spending about 3% of revenue on research.
2. Calculate tangible equity and evaluate the solvency risk of $31.1 billion of debt against it.
3. Assess what the specialty-pharmacy arrangement implies for the quality of reported revenue.
4. Formulate your investment recommendation: BUY, SHORT, or PASS.

<details>
<summary>Reveal True Identity & Historical Outcome</summary>

#### Forensic Audit Analysis
1. With little internal research, revenue growth depended on further acquisitions and on price increases, both of which need continued access to debt markets and tolerance from payers and regulators.
2. Tangible equity of -$35.7 billion means the debt is serviced entirely by the cash flows of acquired products; any impairment, price rollback or loss of reimbursement falls straight on lenders and shareholders.
3. A captive pharmacy channel can move revenue recognition from the point of sale to a related distributor, which is exactly what the restatement corrected.

#### True Identity
**Valeant Pharmaceuticals International, Inc. (fiscal 2015)**.
- **CEO**: J. Michael Pearson; the board named Joseph C. Papa as Chairman and CEO on April 25, 2016.
- **Specialty pharmacy**: Philidor Rx Services, LLC.

#### Historical Performance
- In October 2015, after public allegations about Philidor, the board formed an ad hoc committee of independent directors; the company severed ties with Philidor effective November 1, 2015.
- The Year t 10-K (filed April 29, 2016) restated 2014 because certain sales to Philidor in the second half of 2014 should have been recognised when Philidor dispensed the product rather than on delivery.
- The same filing lists investigations by two US Attorney's Offices, the SEC, Congress and state authorities.
- The stock fell from its Year t high of $263.81 to a low of $8.31 in the second quarter of 2017 (NYSE prices in the company's 10-K filings), a 96.9% decline.

#### Optimal Decision
**SHORT or PASS**.
Debt of five times book equity against negative tangible equity, revenue growth dependent on price increases under investigation, and a related distribution channel left no margin for error.

</details>

---

## Case 4: The Membership Warehouse Club (Year 2010)

### Financial Profile (Figures in Millions)
```
+-----------------------------------------------------------------------+
| Metric                                   | Year t-2  | Year t-1 | Year t |
|------------------------------------------+-----------+----------+--------|
| Net Sales                                | $70,977   | $69,889  | $76,255|
| Membership Fees                          | $1,506    | $1,533   | $1,691 |
| Merchandise Gross Margin                 | 10.53%    | 10.81%   | 10.83% |
| Operating Income                         | $1,969    | $1,777   | $2,077 |
| Net Income                               | $1,283    | $1,086   | $1,303 |
| Cash Flow from Operations (CFO)          | $2,206    | $2,092   | $2,780 |
| Member Renewal Rate (US and Canada)      | n/a       | 87%      | 88%    |
| Cash and Short-Term Investments          | n/a       | $3,727   | $4,749 |
| Total Debt                               | $2,346    | $2,226   | $2,167 |
+-----------------------------------------------------------------------+
```

### Business and Operational Context
- **Gross Margin Discipline**: Merchandise is sold at a gross margin of about 10.8% of sales.
- **Profit Engine**: Membership fees were $1,691 million against operating income of $2,077 million, so the merchandise business contributed only $386 million, or 0.51% of net sales.
Business and Gold Star memberships cost $50 a year, with an Executive tier at about $100.
- **Working Capital Float**: Inventory turned 12.3 times in Year t (29.6 days of merchandise costs on average balances), while accounts payable averaged 30.6 days; at year-end payables were 105.5% of inventory, so suppliers financed the entire inventory.
- **Balance Sheet**: Cash and short-term investments of $4,749 million exceeded total debt of $2,167 million.
- **Valuation**: The stock closed between $53.61 and $59.16 in the fourth quarter of Year t, 18.4x to 20.3x diluted EPS of $2.92.

### Questions to Solve
1. Analyze the relationship between membership fees ($1,691 million) and operating income ($2,077 million).
2. Explain why a thin merchandise margin can be a competitive strength rather than a weakness.
3. Formulate your investment recommendation: BUY, SHORT, or PASS.

<details>
<summary>Reveal True Identity & Historical Outcome</summary>

#### Fundamental Analysis
1. Membership fees were 81.4% of operating income ($1,691 million / $2,077 million).
The business is closer to a subscription club than a retailer: it passes its purchasing scale back to members as low prices and earns its profit from renewals.
2. Nick Sleep and Qais Zakaria's Nomad Investment Partnership letters called this model "scale economics shared": a competitor that tries to undercut prices that are already near cost loses money doing it.
3. An 88% renewal rate makes fee income predictable, and payables that exceed inventory mean suppliers fund the goods on the shelves.

#### True Identity
**Costco Wholesale Corporation (fiscal 2010)**.
- **Co-founders**: Jim Sinegal (President and CEO) and Jeffrey Brotman (Chairman); Charles Munger served on the board.

#### Historical Performance
- Check later Costco 10-K filings for renewal rates, fee changes and results rather than relying on remembered return figures; this drill does not quote them.

#### Optimal Decision
**LONG-TERM BUY**.
Recurring fee income, a self-funding working-capital cycle, a net cash balance sheet and a price position competitors cannot match made a P/E of 18.4x to 20.3x reasonable for the quality of the earnings.

</details>

---

## Case 5: The Rental Fleet in a Travel Freeze (May 2020)

### Financial Profile (Figures in Millions)
```
+-----------------------------------------------------------------------+
| Metric                                   | Year t-2  | Year t-1 | Q1 Year t |
|------------------------------------------+-----------+----------+-----------|
| Total Revenues                           | $9,504    | $9,779   | $1,923    |
| Net Income (Loss)                        | -$225     | -$58     | -$356     |
| Cash Flow from Operations (CFO)          | $2,556    | $2,900   | $449      |
| Total Debt                               | $16,324   | $17,089  | $18,754   |
| Total Assets                             | $21,382   | $24,627  | $25,842   |
| Cash and Cash Equivalents                | $1,127    | $865     | $1,017    |
+-----------------------------------------------------------------------+
```

### Business and Operational Context
- **Exogenous Shock**: In March 2020 travel collapses with the COVID-19 pandemic, and first-quarter revenue falls 8.7% year over year before the full effect of April lockdowns.
- **Fleet Financing**: At March 31 the company owes $18,754 million: $14,438 million of vehicle debt (77.0% of the total), mostly asset-backed notes issued by a bankruptcy-remote financing subsidiary, and $4,316 million of corporate debt.
Debt is 72.6% of total assets and 12.6 times total equity of $1,491 million.
The company's peak 2019 fleet was about 567,600 vehicles in the US and 204,000 internationally.
- **Collateral Mechanism**: The US fleet is leased from the financing subsidiary under an operating lease whose monthly payments rise when used-vehicle values fall, so a used-car price shock raises cash payments exactly when rental revenue disappears.
- **Liquidity Status**: On April 27, 2020 the company did not make certain payments due under the operating lease; noteholders and lenders agreed to forbear and waive defaults only until May 22, 2020.

### Questions to Solve
1. Analyze the mismatch between asset-backed fleet debt and corporate cash flow during a travel freeze.
2. Formulate your investment recommendation for the common stock: BUY, SHORT, or PASS.

<details>
<summary>Reveal True Identity & Historical Outcome</summary>

#### Fundamental Analysis
1. With $18.8 billion of debt against $1.5 billion of equity, small changes in fleet value swamp the equity.
2. The lease structure turns falling used-car prices into immediate cash demands, and the forbearance deadline put the decision in creditors' hands.

#### True Identity
**Hertz Global Holdings, Inc. (May 2020)**.

#### Historical Performance
- Hertz and its US and Canadian subsidiaries filed for Chapter 11 on May 22, 2020, the day the forbearance and waiver agreements expired.
- In June 2020, with Bankruptcy Court approval, Hertz started an at-the-market program to sell up to $500 million of common stock; it suspended the program on June 15 and terminated it on June 18, 2020, after issuing 13,912,368 shares for about $28 million of net proceeds (about $2.01 per share).
- The Bankruptcy Court confirmed Hertz's plan on June 10, 2021 and the company emerged on June 30, 2021; the plan paid creditors in full and, according to Hertz's June 10, 2021 press release, gave existing shareholders more than $1 billion of value.

#### Optimal Decision
**PASS or EXIT the common stock**.
Equity holders in a Chapter 11 case are last in line, and in May 2020 there was no way to underwrite the eventual shareholder recovery.

</details>

---

## Case 6: The Turnaround Consumer Technology Company (Year 2003)

### Financial Profile (Figures in Millions)
```
+-----------------------------------------------------------------------+
| Metric                                   | Year t-2  | Year t-1 | Year t |
|------------------------------------------+-----------+----------+--------|
| Net Sales                                | $5,363    | $5,742   | $6,207 |
| Gross Margin                             | 23.0%     | 27.9%    | 27.5%  |
| Operating Income (Loss)                  | -$344     | $17      | -$1    |
| Net Income (Loss)                        | -$25      | $65      | $69    |
| Cash Generated by Operating Activities  | $185      | $89      | $289   |
| Cash, Cash Equivalents and ST Investments| $4,336    | $4,337   | $4,566 |
| Long-Term Debt incl. Current Maturities  | $317      | $316     | $304   |
| Purchases of Property and Equipment      | $232      | $174     | $164   |
| Music Player Unit Sales (thousands)      | n/a       | 381      | 939    |
+-----------------------------------------------------------------------+
```

### Business and Operational Context
- **Core Market**: Personal computers, where the company is a small player in a market dominated by Windows machines.
- **Balance Sheet**: $4,566 million of cash and short-term investments against $304 million of debt ($300 million of 6.5% notes maturing in February 2004).
- **Hidden Growth Catalyst**: The company's portable music player sold 939,000 units in Year t, up 146.5%; in April of Year t it launched an online music store for its own computers, and in October, just after the fiscal year-end, it released its music software and store for Windows.
- **Valuation**: The stock closed between $19.06 and $23.10 in the last quarter of Year t, with 367.7 million shares outstanding.
At a hypothetical entry price of $20.00, market value is $7,355 million, cash is 62.1% of it (net cash 57.9%, or $11.59 per share), and enterprise value is $3,093 million, or 0.50x Year t sales.

### Questions to Solve
1. Calculate enterprise value at the hypothetical entry price and evaluate the downside protection from net cash.
2. Analyze the option value of the music player and store, now that they reach Windows users.
3. Formulate your investment recommendation: BUY, SHORT, or PASS.

<details>
<summary>Reveal True Identity & Historical Outcome</summary>

#### Fundamental Analysis
1. At $20.00, cash covers 62.1% of the market value and net cash 57.9%, so the market values the operating business at about half a year of sales.
2. The core business is at operating breakeven (an operating loss of $1 million) but generates operating cash ($289 million in Year t), so the cash pile is not being consumed.
3. Opening the music player and store to Windows users multiplies the addressable market, and the cash balance means the company can fund that growth without outside capital.

#### True Identity
**Apple Computer, Inc. (fiscal 2003)**.
- **CEO**: Steve Jobs.

#### Historical Performance
- The products in the catalyst were the iPod (939,000 units in fiscal 2003) and the iTunes Music Store (launched April 2003, Windows version October 2003).
- Apple introduced the iPhone on January 9, 2007 (Apple press release).

#### Optimal Decision
**BUY**.
A net cash balance covering most of the market value, a breakeven core business that still generated cash, and a fast-growing product line opening to the much larger Windows market gave strong downside protection with large upside.

</details>

---

## In this repo and The-Distinguished-Engineer

- Every ratio, margin, growth rate and valuation multiple in the six cases is printed and asserted by [`mkt_drill_03_blind_company_memos.py`](../code/mkt_drill_03_blind_company_memos.py).
  Independent routes: exact-fraction recomputation from the filed line items, with filed subtotals re-added from their components (Amazon's 2001 operating cash flow from its 17 reconciliation lines, Apple and Costco gross margin from sales less cost of sales, Hertz total debt from its two debt lines) and interim cash flow recovered by subtraction.
