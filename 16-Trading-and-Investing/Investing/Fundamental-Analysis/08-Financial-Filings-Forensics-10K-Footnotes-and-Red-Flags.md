---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [O'Glove (1987) - Quality of Earnings: The Investor's Guide to How Much Money a Company Is Really Making, Penman (2013) - Financial Statement Analysis and Security Valuation, Schilit and Perler (2010) - Financial Shenanigans: How to Detect Accounting Gimmicks and Fraud in Financial Reports, SEC - Form 10-K Form 10-Q and Form 8-K General Instructions, SEC - Regulation S-K]
---

# Financial Filings Forensics, 10-K Footnotes, and Governance Red Flags

## TL;DR

- The face of the financial statements is only a summary; the obligations and accounting choices behind it are in the notes to the financial statements and the 10-K's disclosure schedules.
- Earnings calls and press releases are management's framing; MD&A is required disclosure (Regulation S-K Item 303) but is not audited, whereas the notes are part of the audited financial statements.
- Key footnote battlegrounds include Revenue Recognition (ASC 606 contract assets/liabilities), Income Tax rate reconciliations, Pension underfunding, Debt covenants, and Related-Party Transactions.
- The DEF 14A Proxy statement reveals corporate governance, executive compensation metrics (watch for bonuses tied to generous non-GAAP measures such as "Adjusted EBITDA") and insider ownership.
- An 8-K disclosing an auditor change (Item 4.01) or "non-reliance on previously issued financial statements" (Item 4.02) is among the most serious red flags a filing can carry.

## Learning objectives

- Navigate SEC filing structures across annual 10-K reports, quarterly 10-Q reports, 8-K material event notices, and DEF 14A proxy statements.
- Audit critical 10-K footnotes: Revenue Recognition (ASC 606), Debt Covenants, Income Taxes, Pension Obligations, and Contingent Liabilities.
- Detect executive compensation gaming and misaligned incentives inside proxy filings.
- Reconcile reported operating income to normalized economic income by stripping non-operating adjustments.
- Work through a 20-point forensic filings checklist to surface accounting and distress risk early.

## Core concepts

### 1. The Hierarchy of SEC Filings

Filings with the Securities and Exchange Commission (SEC) follow a fixed set of forms (deadlines as of November 2026, from each form's General Instructions):

```
+-----------------------------------------------------------------------+
|                    SEC REGULATORY FILINGS TAXONOMY                    |
+-----------------------------------------------------------------------+
| Filing  | Frequency | Audit Status | Primary Information Content      |
+---------+-----------+--------------+----------------------------------+
| Form    | Annual    | Audited by   | Complete annual business review, |
| 10-K    |           | Independent  | audited 3-statement financials,  |
|         |           | Public Acct  | comprehensive footnote schedules |
| Form    | Quarterly | Unaudited    | Interim performance, quarterly   |
| 10-Q    | (3x/year) | (Reviewed)   | balance sheet, working capital   |
| Form    | Ad-hoc    | Unaudited    | Material unscheduled events:     |
| 8-K     | (4 days)  |              | auditor changes, exec departures |
| DEF 14A | Annual    | Statutory    | Executive compensation metrics,  |
| (Proxy) |           | Disclosure   | board governance, insider stakes |
| Form 4  | Event     | Statutory    | Insider trades by officers,      |
|         | (2 days)  | Disclosure   | directors and >10% owners        |
+-----------------------------------------------------------------------+
```

### 2. Anatomy of the Form 10-K

The annual 10-K is divided into four parts (selected items shown):
- **Part I**:
  - **Item 1: Business**: Operating segments, major customer concentrations, seasonal patterns, regulatory constraints.
  - **Item 1A: Risk Factors**: Boilerplate risks versus newly added, specific operational threats (tracking year-over-year textual diffs is critical).
- **Part II**:
  - **Item 7: Management's Discussion and Analysis (MD&A)**: Management's narrative explanation of operating results, liquidity trends, and capital commitments.
  - **Item 8: Financial Statements and Supplementary Data**: The three core financial statements and the exhaustive footnote disclosures.
- **Part III**:
  - **Items 10-14**: Executive officers, corporate governance, executive compensation, and principal accounting fees (often incorporated by reference to DEF 14A).
- **Part IV**:
  - **Item 15: Exhibits and Financial Statement Schedules**: Material contracts, credit agreements, list of subsidiaries, and executive employment agreements.

### 3. Deep-Dive Footnote Forensics

```
+-----------------------------------------------------------------------+
|                    THE 8 ESSENTIAL FOOTNOTE AUDITS                    |
+-----------------------------------------------------------------------+
| 1. Revenue Recognition (ASC 606)     5. Pension & Post-Retirement     |
|    - Contract Assets & Liabilities      - Discount rate assumptions   |
|    - Remaining Perf Oblig (RPO)         - Plan asset returns vs actual|
| 2. Income Tax Reconciliation         6. Commitments & Contingencies   |
|    - Statutory vs effective rates       - Legal claims & indemnities  |
|    - Valuation allowance changes        - Off-balance-sheet guarantees|
| 3. Debt & Credit Facilities          7. Related-Party Transactions    |
|    - Maturity schedule                  - Executive aircraft leasing  |
|    - Financial maintenance covenants    - Nepotistic supplier deals   |
| 4. Inventory Valuation               8. Stock-Based Compensation      |
|    - LIFO/FIFO reserves                 - Black-Scholes volatility    |
|    - Raw materials vs WIP vs Finished   - Dilution overhang           |
+-----------------------------------------------------------------------+
```

#### Footnote 1: Revenue Recognition (ASC 606)
- **Contract Assets (Unbilled Receivables)**: Revenue recognized before unconditional right to invoice; rapid growth signals milestone gaming.
- **Contract Liabilities (Deferred Revenue)**: Upfront cash collected before delivery; a sequential deceleration in deferred revenue indicates organic sales contraction before headline revenue shows it.
- **Remaining Performance Obligations (RPO)**: Contractually committed future revenue (backlog); provides clean visibility into enterprise demand.

#### Footnote 2: Income Taxes
The tax footnote reconciles the statutory corporate tax rate (21% US federal for tax years beginning after 2017, Internal Revenue Code section 11(b)) to the effective tax rate reported:

$$\text{Effective Tax Rate} = \frac{\text{Reported Income Tax Expense}}{\text{Pre-Tax GAAP Income}}$$

- **Red Flag**: A persistent, poorly explained gap where the effective tax rate sits far below the statutory rate, driven by aggressive transfer pricing or one-time deferred tax adjustments.
- **Valuation Allowance**: If management releases a valuation allowance on Deferred Tax Assets (DTAs), it records a non-cash tax benefit that boosts Net Income without moving cash; the release can be legitimate under ASC 740, but it is a judgment that deserves scrutiny.

#### Footnote 3: Debt, Credit Agreements, and Covenants
- **Maturity Schedule**: A wall of debt maturing in the next one to two years without committed credit lines creates refinancing risk.
- **Financial Covenants**: Typical forms are a maximum leverage ratio (for example $\text{Total Net Debt} / \text{EBITDA}$ at or below a stated multiple) and a minimum fixed charge coverage ratio; the exact definitions, including which EBITDA add-backs count, are in the credit agreement filed as an exhibit.
- **Headroom Analysis**: Recompute each covenant under a stress case of your own choosing (a revenue decline, for example) to see how close the firm is to a breach.

#### Footnote 4: Related-Party Transactions
Material related-party transactions must be disclosed in the notes (ASC 850), and Regulation S-K Item 404 requires disclosure of transactions above $\$120,000$ in which a director, executive officer or other related person has a material interest:
- Examples: Leasing real estate from an entity owned by the CEO; paying consulting fees to relatives of board members; providing unsecured loans to founders.
- Significant related-party activity raises the risk of self-dealing and calls for scrutiny of how the board approved it.

### 4. Proxy Statement (DEF 14A) Forensics

The Proxy statement exposes executive compensation structure:
1. **The Adjusted EBITDA Trap**: Bonus targets tied to "Adjusted EBITDA" can let executives exclude stock compensation, restructuring costs and acquisition integration charges, so pay can rise while value per share falls.
2. **Alignment Metric**: Many investors prefer incentives built on Return on Invested Capital (ROIC) or relative Total Shareholder Return (TSR) measured over several years.
3. **Golden Parachutes**: Large change-of-control payments can bias management toward a sale; the proxy quantifies them.
4. **Insider Ownership & Pledging**: Regulation S-K Item 403(b) requires the proxy to footnote shares pledged as security by directors and officers; pledged shares can be sold by lenders after a price fall, adding selling pressure.

### 5. Form 8-K Critical Triggers

An 8-K filing is triggered by specified corporate events and, for most items, must be filed within four business days:

```
+-----------------------------------------------------------------------+
|                    THE 8-K EMERGENCY RED FLAG CODES                  |
+-----------------------------------------------------------------------+
| Item 4.01 : Change in Registrant's Certifying Accountant              |
|             (Sudden auditor resignation or dispute over accounting)   |
| Item 4.02 : Non-Reliance on Previously Issued Financial Statements    |
|             (Formal restatement admissions; catastrophic accounting)  |
| Item 5.02 : Departure of Directors or Certain Officers                |
|             (Sudden CFO, CEO, or Audit Committee Chair resignation)   |
| Item 2.04 : Triggering Events That Accelerate or Increase a Direct    |
|             Financial Obligation (for example, a covenant default)    |
| Item 1.03 : Bankruptcy or Receivership                                |
+-----------------------------------------------------------------------+
```

### 6. The 20-Point Forensic Red Flag Checklist

```
+-----------------------------------------------------------------------+
|                    THE 20-POINT FORENSIC AUDIT MATRIX                 |
+-----------------------------------------------------------------------+
| 01. Receivables growing much faster than revenue                      |
| 02. Unbilled receivables surge as a percentage of total AR            |
| 03. Inventory growing while sales decline or gross margins expand     |
| 04. Sudden shift from FIFO to LIFO (or LIFO liquidation gains)        |
| 05. Extending depreciable lives of plant or equipment                 |
| 06. Capitalizing normal operating costs into intangible assets        |
| 07. Cash Flow from Operations (CFO) collapsing while Net Income rises |
| 08. Sequential drop in Deferred Revenue while headline revenue grows  |
| 09. Negative Sloan Accrual score reversing into high positive decile  |
| 10. Beneish M-Score rising above -1.78 threshold                      |
| 11. Reversal of tax valuation allowances to manufacture net income    |
| 12. "Non-recurring" restructuring charges that recur year after year  |
| 13. Adjusted EBITDA excludes normal recurring cash expenses           |
| 14. Pension plan discount rate raised or expected return inflated     |
| 15. Debt maturities concentrated in the next 12 to 24 months          |
| 16. Thin covenant headroom under the base case                        |
| 17. Related-party transactions with executives or major shareholders  |
| 18. Executive compensation tied to non-GAAP metrics ex-SBC            |
| 19. Sudden resignation of CFO or Audit Committee Chair (Item 5.02)   |
| 20. Auditor resignation or non-reliance restatement (Item 4.01/4.02)  |
+-----------------------------------------------------------------------+
```

## Worked numerical case study

Analyze the footnotes of a hypothetical Matrix Cloud Corp:
- Reported Net Income: $120M
- Reported Revenue: $1,000M
- Reported GAAP Income Tax Expense: $12M (Effective tax rate: 12 / 132 = 9.1%)
- Statutory Tax Rate: 21.0%

### Footnote Examination:
1. **Tax Reconciliation Footnote**:
   - Pre-tax income: $132M
   - Expected tax at 21%: $27.72M
   - Less: Reversal of valuation allowance on historical DTAs: -$15.72M
   - Actual reported tax expense: $12.00M
   - Forensic finding: $15.72M of the $120M Net Income (13.1%) comes from releasing a tax valuation allowance, a judgment call that adds no cash and is unlikely to recur.

2. **Revenue Recognition Footnote (ASC 606)**:
   - Contract Assets (Unbilled AR): Increased from $20M to $65M (+$45M, +225%)
   - Billed Accounts Receivable: Increased from $100M to $120M (+$20M, +20%)
   - Deferred Revenue (Contract Liability): Decreased from $180M to $140M (-$40M, -22.2%)
   - Remaining Performance Obligations (RPO): Dropped from $400M to $310M (-$90M, -22.5%)

3. **Executive Compensation (DEF 14A)**:
   - GAAP operating profit: $140M, less $8M of net interest expense, ties to the $132M pre-tax income in the tax footnote.
   - CEO target bonus metric: "Adjusted EBITDA", which adds back $40M of depreciation and amortization plus $85M of Stock-Based Compensation and $25M of "Cloud Transformation Restructuring Charges".
   - Total adjustments: $150M ($40M + $85M + $25M) added to GAAP operating profit of $140M to claim "Adjusted EBITDA" of $290M.
   - Plain EBITDA is $140M + $40M = $180M (equivalently $120M net income + $12M tax + $8M interest + $40M D&A).
   - If the $110M of SBC and restructuring add-backs are recurring costs, as they are here, they inflate the bonus metric by 61.1% over plain EBITDA ($290M / $180M - 1).

### Forensic Synthesis:
The footnotes together show a pattern consistent with aggressive earnings management.
Headline revenue and net income appear solid, but the forward indicators have weakened:
- RPO (backlog) fell 22.5% and deferred revenue fell 22.2%, indicating that forward bookings are shrinking.
- Contract assets rose $45M (225%), so a growing share of revenue was recognized before the company had an unconditional right to bill.
- Net Income includes a $15.72M non-cash tax benefit from the allowance release.
- The bonus metric adds back $85M of SBC and $25M of restructuring costs.
- Conclusion: the filing warrants deeper review (revenue recognition policy, contract terms, auditor communications) before any position is taken.

## Practice questions

> [!question]- mkt-fa-225 | What is the statutory filing deadline for a Form 10-K for a Large Accelerated Filer?
> 60 days after the end of the fiscal year.

> [!question]- mkt-fa-226 | What is the difference between a Form 10-K and a Form 10-Q regarding audit verification?
> The financial statements in a Form 10-K are audited by an independent registered public accounting firm; the interim statements in a Form 10-Q are reviewed by that firm but not audited.

> [!question]- mkt-fa-227 | What is the deadline to file a Form 8-K following a triggering material corporate event?
> Four business days after the triggering event for most items (Form 8-K General Instruction B.1).

> [!question]- mkt-fa-228 | What does an 8-K Item 4.02 filing declare to the market?
> Non-Reliance on Previously Issued Financial Statements, indicating that prior published accounting figures were materially flawed and must be restated.

> [!question]- mkt-fa-229 | What does an 8-K Item 4.01 filing indicate?
> A change in the company's certifying public accountant (dismissal or resignation of the external independent auditor).

> [!question]- mkt-fa-230 | Which section of the 10-K contains Management's Discussion and Analysis?
> Item 7 of Part II.

> [!question]- mkt-fa-231 | Why is tracking year-over-year textual modifications in Item 1A (Risk Factors) valuable?
> Textual additions reveal emerging legal liabilities, customer loss risks, or operational threats that management is legally obliged to disclose.

> [!question]- mkt-fa-232 | What is a Contract Asset under ASC 606 revenue recognition?
> An entity's right to consideration for goods or services already transferred when that right is conditional on something other than the passage of time (ASC 606-10-45-3).
> An unbilled amount whose payment depends only on time passing is a receivable, not a contract asset.

> [!question]- mkt-fa-233 | How does a sudden surge in Contract Assets indicate revenue recognition risk?
> It shows revenue being recognized before the company has an unconditional right to payment, often on estimates of progress, so growth in it outrunning revenue deserves a look at the revenue recognition policy.

> [!question]- mkt-fa-234 | What does a sequential decline in Deferred Revenue signal for a subscription software company?
> It signals that customer renewals and new bookings are contracting, which will cause future reported revenue growth to stall.

> [!question]- mkt-fa-235 | What is Remaining Performance Obligations (RPO)?
> The aggregate dollar amount of contractually committed customer fees that have not yet been recognized as revenue (contract backlog).

> [!question]- mkt-fa-236 | How can a company use the tax valuation allowance to manipulate reported net income?
> By reversing a previously established allowance on Deferred Tax Assets, creating a non-cash negative tax expense that inflates Net Income.

> [!question]- mkt-fa-237 | What is the purpose of the Effective Tax Rate reconciliation schedule in the tax footnote?
> To explain the exact mathematical differences between the statutory corporate tax rate and the effective tax rate reported on the income statement.

> [!question]- mkt-fa-238 | What is a debt maintenance covenant?
> A contractual clause in a credit agreement requiring the borrower to maintain financial ratios (e.g. Debt/EBITDA, Interest Coverage) above defined minimum levels.

> [!question]- mkt-fa-239 | What happens when a company breaches a debt covenant?
> Once any cure or grace period lapses, the breach is an event of default: lenders can typically accelerate the debt, charge default interest, or enforce on collateral if the debt is secured, and they often extract fees and tighter terms in exchange for a waiver.

> [!question]- mkt-fa-240 | Why is the debt maturity schedule in the footnotes critical for solvency analysis?
> It highlights upcoming debt refinancing cliffs, exposing liquidity crunches if large tranches mature during tight credit market conditions.

> [!question]- mkt-fa-241 | How do companies game defined benefit pension footnotes?
> Raising the expected return on plan assets lowers reported pension expense (it does not change the obligation), and a higher discount rate lowers the projected benefit obligation; compare both assumptions with peers and with high-quality bond yields.

> [!question]- mkt-fa-242 | What does an underfunded pension plan represent economically?
> A debt-like liability requiring future corporate cash contributions to meet employee retirement obligations; analysts usually add the after-tax deficit to net debt.

> [!question]- mkt-fa-243 | Why are related-party transactions a major corporate governance red flag?
> They create the opportunity for self-dealing, transferring corporate resources to insiders, so they test whether the Board's oversight is effective.

> [!question]- mkt-fa-244 | What is the DEF 14A filing?
> The definitive proxy statement filed prior to the annual shareholder meeting, detailing executive compensation, board elections, and voting matters.

> [!question]- mkt-fa-245 | Why is executive compensation tied strictly to "Adjusted EBITDA" problematic?
> It incentivizes executives to execute dilutive acquisitions and ignore real cash costs (SBC, restructuring) excluded from Adjusted EBITDA definitions.

> [!question]- mkt-fa-246 | What is the golden parachute provision in executive contracts?
> Substantial guaranteed payouts, accelerated stock vesting, and bonuses awarded to top executives if the company is acquired.

> [!question]- mkt-fa-247 | What is the risk of an executive pledging common shares against personal margin loans?
> If the stock price declines, lenders issue margin calls, triggering forced open-market sales that precipitate cascading share price collapses.

> [!question]- mkt-fa-248 | What is a Form 4 SEC filing?
> A filing reporting changes in ownership by corporate insiders (directors, officers, and >10% beneficial owners) within two business days of a transaction.

> [!question]- mkt-fa-249 | What does a cluster of insider open-market sales by both the CEO and CFO typically signal?
> Possibly negative private information, but sales are a noisier signal than purchases because insiders sell for diversification, taxes and liquidity; check whether the sales were made under a pre-arranged Rule 10b5-1 plan before reading much into them.

> [!question]- mkt-fa-250 | How does a company disguise recurring operating expenses as restructuring charges?
> By continuously taking "one-time" restructuring charges year after year, encouraging Wall Street analysts to ignore real operating cash drains.

> [!question]- mkt-fa-251 | What is a LIFO liquidation gain?
> When a LIFO firm liquidates older, lower-cost inventory layers during inflation, artificially boosting gross margin with historical inventory costs.

> [!question]- mkt-fa-252 | Where in the 10-K can an analyst find details of ongoing litigation and potential fines?
> In the Commitments and Contingencies footnote in Item 8.

> [!question]- mkt-fa-253 | What is an Audit Committee Chair resignation red flag?
> A sudden resignation of the Audit Committee Chair, especially if followed by an auditor change, can signal disagreements over financial reporting; a director who resigns over a disagreement can require the letter to be filed with the 8-K (Item 5.02(a)).

> [!question]- mkt-fa-254 | What footnote reveals true dilution potential from executive stock options?
> The Stock-Based Compensation footnote, detailing outstanding options, strike prices, restricted stock units, and vesting timelines.

> [!question]- mkt-fa-255 | Why is an unexpected increase in "Principal Accounting Fees and Services" noteworthy?
> A jump in audit or non-audit fees can reflect added audit work on problem areas, complex transactions or regulatory inquiries; the proxy's fee table lets you track it year to year.

> [!question]- mkt-fa-256 | What is the ultimate objective of 10-K footnote forensics?
> To dismantle management's public narrative, quantify hidden liabilities, normalize true earnings power, and uncover risks before they manifest in market prices.

> [!question]- mkt-fa-263 | Which 8-K items should trigger an immediate forensic review, and what does each disclose?
> Item 4.01 (change in the certifying accountant, with any disagreements), Item 4.02 (non-reliance on previously issued financial statements), Item 5.02 (departure of directors or certain officers) and Item 2.04 (triggering events that accelerate a direct financial obligation).
> Most 8-K items are due within four business days of the event.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_fa_08_filings.py`](../../code/mkt_fa_08_filings.py) prints and asserts every number in the case study: the tax footnote rebuilt from pre-tax income down to net income, the effective rate two ways, each footnote balance change, and EBITDA from operating profit and from net income before the Adjusted EBITDA add-backs.
- Related notes: [Fraud Detection, Beneish M-Score, and Piotroski F-Score](06-Fraud-Detection-Beneish-M-Score-and-Piotroski-F-Score.md), [Forensic Accounting, Sloan Accruals, and Earnings Quality](05-Forensic-Accounting-Sloan-Accruals-and-Earnings-Quality.md).

## Further reading

- O'Glove, T. L. (1987). *Quality of Earnings: The Investor's Guide to How Much Money a Company Is Really Making*. Free Press.
- Penman, S. H. (2013). *Financial Statement Analysis and Security Valuation* (5th ed.). McGraw-Hill.
- Schilit, H. M., & Perler, J. (2010). *Financial Shenanigans: How to Detect Accounting Gimmicks and Fraud in Financial Reports* (3rd ed.). McGraw-Hill.
- U.S. Securities and Exchange Commission. *Form 10-K*, *Form 10-Q* and *Form 8-K*, General Instructions.
- U.S. Securities and Exchange Commission. Regulation S-K, Items 303, 403 and 404 (17 CFR 229).
- FASB Accounting Standards Codification: ASC 606 (revenue), ASC 740 (income taxes), ASC 850 (related parties).
