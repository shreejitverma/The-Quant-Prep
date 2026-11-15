---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Dechow Sloan and Sweeney (1995) - Detecting Earnings Management, Jones (1991) - Earnings Management During Import Relief Investigations, Schilit and Perler (2010) - Financial Shenanigans: How to Detect Accounting Gimmicks and Fraud in Financial Reports, Sloan (1996) - Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?]
---

# Forensic Accounting, Sloan Accruals, and Earnings Quality

## TL;DR

- Accounting earnings consist of two distinct components: physical cash flows and non-cash accounting accruals.
- Sloan (1996) documented the "Accrual Anomaly": the cash flow component of earnings is more persistent than the accrual component, so high-accrual earnings revert faster.
- Stock prices behaved as if investors fixated on total earnings, so high-accrual firms earned lower and low-accrual firms higher subsequent abnormal returns in Sloan's 1962-1991 sample.
- Forensic accounting isolates abnormal discretionary accruals using the Modified Jones Model, separating normal business expansion from aggressive managerial manipulation.
- Key earnings quality red flags include DSO expanding faster than sales, unbilled receivables surges, capitalizing normal operating costs, and sudden depletion of reserve accounts.

## Learning objectives

- Calculate Balance Sheet Accruals and Cash Flow Statement Accruals scaled by average total assets.
- Explain the behavioral and structural drivers of Richard Sloan's Accrual Anomaly.
- Formulate and estimate the Modified Jones Model to isolate discretionary from non-discretionary accruals.
- Audit working capital line items for classic financial shenanigans: channel stuffing, premature revenue recognition, and cookie-jar reserves.
- Evaluate the earnings quality of a target enterprise through systematic accrual forensics.

## Core concepts

### 1. The Anatomy of Earnings: Cash Flow vs Accruals

Under accrual accounting principles, revenue is recognized when earned and expenses when incurred, regardless of when physical cash changes hands.
Total accounting earnings can be cleanly partitioned:

$$\text{Net Income} = \text{Cash Flow Component} + \text{Accrual Component}$$

```
+-----------------------------------------------------------------------+
|                    EARNINGS QUALITY SPECTRUM                          |
+-----------------------------------------------------------------------+
|  HIGH QUALITY EARNINGS                LOW QUALITY EARNINGS            |
|  - High Operating Cash Flow (CFO)     - High Accruals, Low Cash Flow  |
|  - Negative or Low Accruals           - Large positive working capital|
|  - Cash collections lead revenue      - Receivables & inventory surge |
|  - Highly persistent over time        - Fast mean reversion to losses |
+-----------------------------------------------------------------------+
```

Richard Sloan's 1996 paper showed that the accrual component of earnings is less persistent than the cash flow component.
With earnings measured as income from continuing operations over average total assets, he estimated:

$$\text{Earnings}_{t+1} = \gamma_0 + \gamma_1 \text{Accruals}_t + \gamma_2 \text{Cash Flows}_t + \upsilon_{t+1}$$

The pooled estimates in Sloan's Table 3 (40,679 firm-years, 1962-1991) are $\gamma_1 = 0.765$ on accruals and $\gamma_2 = 0.855$ on cash flows, and the F-test rejects equality.
Earnings driven by cash flow persist more; earnings driven by accruals revert faster because accruals must eventually reverse or be written off.

Sloan then sorted firms into accrual deciles: a hedge portfolio long the lowest-accrual decile and short the highest earned size-adjusted returns of $10.4\%$, $4.8\%$ and $2.9\%$ in the first, second and third years after portfolio formation (Table 6; the third-year figure is not statistically significant).

### 2. Measuring Accruals: Two Methodologies

#### Method 1: The Balance Sheet Approach (Sloan 1996)

Balance Sheet Accruals measure the net change in operating working capital accounts minus depreciation:

$$\text{Accruals}_{BS} = (\Delta \text{Current Assets} - \Delta \text{Cash}) - (\Delta \text{Current Liabilities} - \Delta \text{Short-Term Debt} - \Delta \text{Taxes Payable}) - \text{Depreciation}$$

Scaled Accrual Ratio:

$$\text{Accrual Ratio}_{BS} = \frac{\text{Accruals}_{BS}}{\text{Average Total Assets}} = \frac{\text{Accruals}_{BS}}{(\text{Assets}_t + \text{Assets}_{t-1}) / 2}$$

#### Method 2: The Cash Flow Statement Approach

Mergers, acquisitions, divestitures, and foreign currency translations change balance sheet accounts without passing through operating accruals.
Collins and Hribar (2002) showed that these non-articulation events contaminate balance sheet accrual estimates, and recommended measuring accruals from the cash flow statement:

$$\text{Accruals}_{CF} = \text{Net Income} - \text{Operating Cash Flow (CFO)}$$

$$\text{Accrual Ratio}_{CF} = \frac{\text{Net Income} - \text{CFO}}{\text{Average Total Assets}}$$

A large positive accrual ratio indicates weaker earnings quality (earnings far exceed cash generated).
A negative accrual ratio indicates cash generation above reported net income.
There is no universal cut-off: Sloan ranked firms into deciles each year, so judge a ratio against the same year's cross-section and the company's own history rather than a fixed threshold.

### 3. Discretionary vs Non-Discretionary Accruals: The Modified Jones Model

Total accruals naturally rise as a business grows.
To detect accounting manipulation, forensic analysts isolate **discretionary accruals** (managerial choice) from **non-discretionary accruals** (driven by economic growth and capital intensity).

The **Jones (1991) model** explains a firm's normal accruals with revenue growth and gross property, plant and equipment, estimated over a period with no presumed manipulation.
The **Modified Jones Model** (Dechow, Sloan, and Sweeney 1995) keeps the parameters estimated from the original Jones model in the estimation period, then computes event-period non-discretionary accruals with revenue growth reduced by the growth in receivables:

$$\frac{\text{Total Accruals}_t}{\text{Assets}_{t-1}} = \alpha_1 \left( \frac{1}{\text{Assets}_{t-1}} \right) + \alpha_2 \left( \frac{\Delta \text{Revenue}_t - \Delta \text{Receivables}_t}{\text{Assets}_{t-1}} \right) + \alpha_3 \left( \frac{\text{Gross PP&E}_t}{\text{Assets}_{t-1}} \right) + \epsilon_t$$

Where:
- $\Delta \text{Revenue}_t - \Delta \text{Receivables}_t$ assumes that any revenue increase tied up in uncollected receivables at year-end represents managerial discretion.
- $\text{Gross PP&E}_t$ controls for natural depreciation expenses.
- Event-period discretionary accruals are total accruals minus the fitted non-discretionary accruals (the residual $\epsilon_t$ in the equation).
- A statistically significant positive $\epsilon_t$ indicates aggressive earnings inflation.

### 4. Anatomy of Classical Financial Shenanigans

The grouping below is this note's own summary of techniques that Schilit and Perler (2010) catalogue in far more detail:

```
+-----------------------------------------------------------------------+
|           FIVE GROUPS OF SHENANIGANS (THIS NOTE'S SUMMARY)            |
+-----------------------------------------------------------------------+
| 1. Premature / Fabricated Revenue:                                    |
|    - Channel stuffing (shipping goods before purchase order)          |
|    - Bill-and-hold transactions (booking revenue without delivery)    |
|    - Recognizing revenue on transactions with contingent refund rights|
| 2. Pushing Current Expenses into Future Periods:                      |
|    - Capitalizing routine operating costs (software, customer acq)    |
|    - Extending asset depreciation lives (depreciation holiday)        |
|    - Failing to write down impaired inventory or goodwill             |
| 3. Concealing Liabilities and Expenses:                               |
|    - Off-balance-sheet special purpose vehicles (SPVs)                |
|    - Structuring leases to stay off balance sheet (pre-ASC 842)       |
| 4. Boosting Current Income with One-Off Gains:                        |
|    - Selling appreciated assets and burying gain inside revenue       |
|    - Releasing cookie-jar restructuring reserves                      |
| 5. Shifting Future Expenses into Current Period:                      |
|    - "Big Bath" restructuring write-offs under new management         |
+-----------------------------------------------------------------------+
```

### 5. Line-by-Line Forensic Red Flags

| Balance Sheet Item | Manipulation Technique | Forensic Diagnostic Test |
|---|---|---|
| **Accounts Receivable** | Channel stuffing; fictitious billing. | Days Sales Outstanding (DSO) jumps against the company's history while peers stay flat. |
| **Unbilled Receivables** | Recognizing revenue on milestone estimates before invoicing. | Unbilled AR rises as a share of total AR without a matching change in contract mix. |
| **Inventory** | Capitalizing production variances; overstating inventory value to lower COGS. | Days Inventory Outstanding (DIO) increases while Gross Margin unexpectedly expands. |
| **Prepaid Assets / Other** | Parking deferred operating expenses to avoid income statement recognition. | Other Current Assets growing significantly faster than total revenues. |
| **Capitalized Software** | Capitalizing maintenance software engineers as balance sheet intangibles. | Capitalized Software Additions / R&D Expense ratio rises above historical baseline. |
| **Warranty Reserves** | Reducing accrued warranty liability to manufacture paper earnings. | Warranty Provision / Revenue declines despite stable product defect rates. |

## Worked numerical example

Consider a hypothetical Titan Technologies over two consecutive years (taxes payable are included in accrued expenses and assumed unchanged):

| Metric ($ Millions) | Year 1 ($t-1$) | Year 2 ($t$) |
|---|---|---|
| Revenue | 500.0 | 650.0 (+30.0%) |
| Cost of Goods Sold (COGS) | 275.0 | 338.0 |
| Gross Profit | 225.0 | 312.0 (Margin: 45.0% -> 48.0%) |
| Operating Expenses (SG&A) | 125.0 | 152.0 |
| Operating Income (EBIT) | 100.0 | 160.0 (+60.0%) |
| Net Income | 75.0 | 120.0 (+60.0%) |
| Cash Flow from Operations (CFO) | 80.0 | 45.0 (-43.8%) |
| Cash and Cash Equivalents | 40.0 | 35.0 |
| Accounts Receivable | 60.0 | 135.0 (+125.0%) |
| Inventory | 70.0 | 110.0 (+57.1%) |
| Other Current Assets | 20.0 | 30.0 |
| Total Current Assets | 190.0 | 310.0 |
| Net PP&E | 250.0 | 280.0 |
| Total Assets | 440.0 | 590.0 |
| Accounts Payable | 45.0 | 50.0 |
| Accrued Expenses | 25.0 | 28.0 |
| Short-Term Debt | 10.0 | 15.0 |
| Total Current Liabilities | 80.0 | 93.0 |
| Depreciation Expense | 25.0 | 28.0 |

### Step 1: Diagnose Net Income vs CFO Divergence
In Year 2, Net Income surged from $75M to $120M (+60%), yet Operating Cash Flow collapsed from $80M to $45M (-43.8%).
This divergence is the classic first sign of low earnings quality.

### Step 2: Compute Sloan Accruals (Cash Flow Method)
Average Total Assets = $\frac{440.0 + 590.0}{2} = \$515.0\text{M}$

Year 1 Accruals:
$$\text{Accruals}_{CF, 1} = \text{Net Income}_1 - \text{CFO}_1 = 75.0 - 80.0 = -\$5.0\text{M}$$
$$\text{Accrual Ratio}_{CF, 1} = \frac{-5.0}{440.0} = -1.14\% \quad (\text{Year 0 assets unknown, so Year 1 ending assets})$$

Year 2 Accruals:
$$\text{Accruals}_{CF, 2} = \text{Net Income}_2 - \text{CFO}_2 = 120.0 - 45.0 = +\$75.0\text{M}$$
$$\text{Accrual Ratio}_{CF, 2} = \frac{+75.0}{515.0} = +14.56\%$$

### Step 3: Compute Sloan Accruals (Balance Sheet Method)
$$\Delta \text{Current Assets (ex cash)} = (310 - 35) - (190 - 40) = 275 - 150 = +\$125.0\text{M}$$
$$\Delta \text{Current Liabilities (ex short debt)} = (93 - 15) - (80 - 10) = 78 - 70 = +\$8.0\text{M}$$
$$\text{Depreciation} = \$28.0\text{M}$$

$$\text{Accruals}_{BS} = 125.0 - 8.0 - 28.0 = +\$89.0\text{M}$$
$$\text{Accrual Ratio}_{BS} = \frac{+89.0}{515.0} = +17.28\%$$

The two methods differ by $89.0 - 75.0 = \$14.0\text{M}$.
The reported CFO of $\$45.0\text{M}$ is $\$14.0\text{M}$ above the $120.0 + 28.0 - (125.0 - 8.0) = \$31.0\text{M}$ that net income, depreciation and working capital alone would give, so the company must have $\$14.0\text{M}$ of other non-cash charges (stock-based compensation, for example), which the cash flow method nets out and Sloan's balance sheet method does not.

### Step 4: Investigate Specific Forensic Drivers (year-end balances)
- Days Sales Outstanding (DSO):
  - Year 1: $\frac{60}{500} \times 365 = 43.8\text{ days}$
  - Year 2: $\frac{135}{650} \times 365 = 75.8\text{ days} \quad (+32.0\text{ days, } +73\%)$
- Days Inventory Outstanding (DIO):
  - Year 1: $\frac{70}{275} \times 365 = 92.9\text{ days}$
  - Year 2: $\frac{110}{338} \times 365 = 118.8\text{ days} \quad (+25.9\text{ days, } +28\%)$

Forensic verdict:
The pattern is consistent with channel stuffing, though the numbers alone cannot prove it.
Revenue expanded 30%, but Accounts Receivable grew 125%, driving DSO from 43.8 to 75.8 days.
Gross margin rose from 45% to 48% while inventory piled up (DIO up 26 days), which is consistent with fixed overhead being absorbed into inventory.
An accrual ratio of 14.56%, up from -1.14%, means most of the profit growth has not yet turned into cash; the next step is the receivables aging, revenue recognition and inventory footnotes.

## Practice questions

> [!question]- mkt-fa-129 | What is the fundamental insight of Richard Sloan's 1996 Accrual Anomaly?
> The cash flow component of earnings is more persistent than the accrual component (pooled coefficients 0.855 against 0.765), yet stock prices behaved as if investors fixated on total earnings, so high-accrual firms subsequently earned negative abnormal returns.

> [!question]- mkt-fa-130 | How is the Cash Flow Statement Accrual calculated?
> Accruals = Net Income - Operating Cash Flow (CFO), scaled by average total assets.

> [!question]- mkt-fa-131 | What does a high positive accrual ratio indicate about corporate earnings?
> It indicates weaker earnings quality: reported profits are driven by non-cash working capital expansion rather than cash collections, so earnings are less persistent.
> Judge "high" against the same year's cross-section (Sloan used deciles), not a fixed cut-off.

> [!question]- mkt-fa-132 | What does a negative accrual ratio indicate about corporate earnings?
> It indicates superior earnings quality, where actual operating cash collections exceed reported accounting net income.

> [!question]- mkt-fa-133 | Why is the Cash Flow Statement method of measuring accruals preferred over the Balance Sheet method?
> Collins and Hribar (2002) showed that acquisitions, divestitures and foreign currency translation move balance sheet accounts without passing through operating accruals, contaminating the balance sheet estimate; the cash flow statement method avoids those errors.

> [!question]- mkt-fa-134 | What is the core objective of the Modified Jones Model?
> To decompose total accruals into normal non-discretionary accruals driven by business scale and abnormal discretionary accruals driven by managerial manipulation.

> [!question]- mkt-fa-135 | Why does the Modified Jones Model subtract the change in Accounts Receivable from the change in Revenue?
> It assumes that credit sales growth that remains uncollected at fiscal year-end represents managerial discretion and potential revenue manipulation.

> [!question]- mkt-fa-136 | What is channel stuffing?
> The practice of shipping excessive, unneeded product inventory to distributors at quarter-end under aggressive terms to prematurely recognize revenue.

> [!question]- mkt-fa-137 | What is the primary diagnostic metric used to detect channel stuffing?
> A rapid expansion in Days Sales Outstanding (DSO) that significantly outpaces historical trends and competitor benchmarks.

> [!question]- mkt-fa-138 | What is bill-and-hold accounting?
> Recognizing revenue on merchandise that has been billed to a customer but remains physically stored in the seller's warehouse prior to shipment.

> [!question]- mkt-fa-139 | When is bill-and-hold revenue recognition permitted under GAAP?
> Under ASC 606-10-55-83 (and IFRS 15 paragraph B81) all four criteria must hold: the reason for the arrangement is substantive (for example, the customer requested it), the product is identified separately as the customer's, it is ready for physical transfer, and the seller cannot use it or direct it to another customer.

> [!question]- mkt-fa-140 | How can a company use inventory valuation to artificially inflate current gross margins?
> By allocating excessive fixed manufacturing overhead into ending inventory on the balance sheet, reducing the Cost of Goods Sold expensed on the income statement.

> [!question]- mkt-fa-141 | What red flag indicates that inventory is being used to manipulate gross margins?
> Gross margins unexpectedly expand while Days Inventory Outstanding (DIO) surges and finished goods inventory piles up.

> [!question]- mkt-fa-142 | What is cookie-jar reserve accounting?
> Overstating expense reserves in highly profitable years and later releasing them into income in weak years to smooth earnings.

> [!question]- mkt-fa-143 | How does reducing the warranty provision percentage boost operating earnings?
> Reducing the percentage of sales accrued for future warranty repairs lowers operating expenses, increasing operating income without generating cash.

> [!question]- mkt-fa-144 | What is the forensic signal of unbilled receivables manipulation?
> A rising ratio of unbilled receivables to total accounts receivable, indicating revenue recognition based on internal milestone estimates rather than client billing.

> [!question]- mkt-fa-145 | How does capitalizing operating software costs inflate Operating Cash Flow?
> It shifts cash outflows from operating expenses (which reduce CFO) into capital expenditures under Cash Flow from Investing (CFI).

> [!question]- mkt-fa-146 | What is a "big bath" accounting restructuring?
> Taking massive discretionary write-offs and restructuring charges in a single period (often following a CEO change) to clear the balance sheet and artificially boost future return metrics.

> [!question]- mkt-fa-147 | Why do companies capitalize customer acquisition costs (CAC) instead of expensing them?
> Capitalizing CAC defers marketing expenses to future balance sheet amortization, temporarily boosting current-period operating margins and EBITDA.

> [!question]- mkt-fa-148 | How does extending the depreciable useful life of plant assets inflate earnings?
> Extending useful lives reduces annual depreciation expense on the income statement, directly inflating reported operating income and pre-tax profit.

> [!question]- mkt-fa-149 | What is round-tripping or barter transaction revenue?
> Selling an asset to a counterparty while simultaneously buying back an equivalent asset from the same counterparty at an inflated price to book synthetic revenue.

> [!question]- mkt-fa-150 | What forensic ratio compares revenue growth to cash collections growth?
> Compare revenue growth with cash collected from customers (revenue minus the change in receivables plus the change in deferred revenue); revenue that persistently grows faster than collections signals deteriorating earnings quality.

> [!question]- mkt-fa-151 | What is the impact of an asset impairment write-down on subsequent year ROE and ROA?
> An impairment reduces equity and total assets immediately; in subsequent years, lower asset values and reduced depreciation inflate calculated ROE and ROA.

> [!question]- mkt-fa-152 | How does factoring receivables without recourse distort Operating Cash Flow?
> It sells uncollected receivables to a bank before quarter-end, accelerating cash into current CFO while hiding underlying customer payment delays.

> [!question]- mkt-fa-153 | What footnote disclosure reveals whether receivables have been factored to boost cash flow?
> The off-balance-sheet financing, transfer of financial assets, and credit facility footnote disclosures in the annual 10-K report.

> [!question]- mkt-fa-154 | What is consignment selling and how is it abused in revenue recognition?
> Shipping goods to dealers who only pay once sold to end users; abusing it involves booking revenue upon initial shipment rather than final retail sale.

> [!question]- mkt-fa-155 | What happens to working capital when a company delays payments to suppliers at quarter-end?
> Accounts payable temporarily surges, artificially inflating Operating Cash Flow for that quarter, which sharply reverses as bills are settled early next period.

> [!question]- mkt-fa-156 | How does a sudden change in revenue recognition accounting policies signal risk?
> It often indicates that organic business growth is slowing and management requires accounting changes to meet consensus market revenue estimates.

> [!question]- mkt-fa-157 | Why is an unexpected increase in Other Current Assets a forensic red flag?
> Companies often hide uncollectible operating costs, disputed payments, or deferred charges in miscellaneous asset buckets to avoid income statement expensing.

> [!question]- mkt-fa-158 | What is the role of auditor tenure in earnings quality?
> Very long tenure raises independence concerns, while an abrupt auditor resignation or dismissal is a serious red flag that a US registrant must disclose on Form 8-K Item 4.01, together with any disagreements with the auditor.

> [!question]- mkt-fa-159 | How does stock-based compensation (SBC) interact with the Sloan accrual calculation?
> SBC is added back to CFO under GAAP; failing to adjust for SBC makes CFO appear artificially robust, understating the true economic accrual burden.

> [!question]- mkt-fa-260 | What did Sloan's (1996) accrual hedge portfolio earn?
> Long the lowest and short the highest accrual decile, it earned size-adjusted returns of $10.4\%$, $4.8\%$ and $2.9\%$ in the first three years after formation (Table 6), with the third year not statistically significant.

> [!question]- mkt-fa-160 | What is the ultimate market outcome for companies in the highest decile of accruals?
> In Sloan (1996) the highest-accrual decile earned size-adjusted returns of $-5.5\%$, $-3.2\%$ and $-2.2\%$ in the three years after formation, significant in the first two years only (Table 6).

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_fa_05_accruals.py`](../../code/mkt_fa_05_accruals.py) prints and asserts every number on this page: the Titan table re-summed line by line, accruals by the cash flow and balance sheet methods with the $\$14.0\text{M}$ gap reconciled to other non-cash charges, and DSO and DIO with their changes from unrounded values; Sloan's coefficients and hedge returns are cited constants from the paper.
- Related notes: [Three-Statement Linkages and Cash Flow Dynamics](01-Three-Statement-Linkages-and-Cash-Flow-Dynamics.md), [Fraud Detection, Beneish M-Score, and Piotroski F-Score](06-Fraud-Detection-Beneish-M-Score-and-Piotroski-F-Score.md).

## Further reading

- Collins, D. W., & Hribar, P. (2002). *Errors in Estimating Accruals: Implications for Empirical Research*. Journal of Accounting Research, 40(1), 105-134.
- Dechow, P. M., Sloan, R. G., & Sweeney, A. P. (1995). *Detecting Earnings Management*. The Accounting Review, 70(2), 193-225.
- Jones, J. J. (1991). *Earnings Management During Import Relief Investigations*. Journal of Accounting Research, 29(2), 193-228.
- Schilit, H. M., & Perler, J. (2010). *Financial Shenanigans: How to Detect Accounting Gimmicks and Fraud in Financial Reports* (3rd ed.). McGraw-Hill.
- Sloan, R. G. (1996). *Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?* The Accounting Review, 71(3), 289-315.
