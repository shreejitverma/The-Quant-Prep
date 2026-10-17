---
type: guide
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Beneish (1999) - The Detection of Earnings Manipulation, Sloan (1996) - Do Stock Prices Fully Reflect Information in Accruals, Schilit (2010) - Financial Shenanigans: How to Detect Accounting Gimmicks]
---

# Statement Forensics Drills

## Overview

The Statement Forensics Drills bank trains financial analysts and quantitative researchers to detect aggressive accounting practices, earnings manipulation, and hidden balance sheet hazards.
Each drill presents a realistic financial data set from corporate filings.
Analyze the indicators, identify the forensic red flags, calculate the relevant accounting metrics, and formulate your audit conclusion before revealing the detailed solution.

---

## Drill 1: The Sloan Balance Sheet Accrual Divergence

### Scenario
Company Alpha reports the following trailing two-year balance sheet and income statement metrics (all figures in millions):

```
+-----------------------------------------------------------------------+
| Metric                                   | Year t-1      | Year t     |
|------------------------------------------+---------------+------------|
| Total Assets                             | $1,000        | $1,250     |
| Net Income                               | $80           | $140       |
| Cash and Cash Equivalents                | $100          | $90        |
| Total Current Assets                     | $350          | $520       |
| Total Current Liabilities                | $150          | $170       |
| Short-Term Debt (in Current Liab)        | $20           | $25        |
| Depreciation & Amortization              | $40           | $45        |
| Cash Flow from Operations (CFO)          | $75           | $60        |
+-----------------------------------------------------------------------+
```

### Questions to Solve
1. Calculate the Balance Sheet Accruals for Year t using the balance sheet decomposition formula.
2. Calculate the Cash Flow Accruals for Year t ($Net Income - CFO$).
3. Scale both accrual measures by Average Total Assets.
4. Interpret the forensic divergence between Net Income growth (+75%) and CFO contraction (-20%).

<details>
<summary>Reveal Forensic Audit & Solution</summary>

#### Step 1: Balance Sheet Accrual Calculation
$$\Delta \text{NOA} = \Delta \text{Current Assets} - \Delta \text{Cash} - (\Delta \text{Current Liabilities} - \Delta \text{Short-Term Debt}) - \text{Depreciation}$$

$$\Delta \text{Current Assets} = 520 - 350 = +170$$
$$\Delta \text{Cash} = 90 - 100 = -10$$
$$\Delta \text{Current Liabilities} = 170 - 150 = +20$$
$$\Delta \text{Short-Term Debt} = 25 - 20 = +5$$
$$\Delta \text{Operating Current Liabilities} = 20 - 5 = +15$$

$$\text{Accruals}_{BS} = (170 - (-10)) - 15 - 45 = 180 - 15 - 45 = \$120 \text{ million}$$

#### Step 2: Cash Flow Accrual Calculation
$$\text{Accruals}_{CF} = \text{Net Income} - \text{CFO} = 140 - 60 = \$80 \text{ million}$$

#### Step 3: Scaled Accrual Ratio
$$\text{Average Total Assets} = \frac{1,000 + 1,250}{2} = \$1,125 \text{ million}$$

$$\text{Scaled Accrual Ratio}_{BS} = \frac{120}{1,125} = +10.67\%$$
$$\text{Scaled Accrual Ratio}_{CF} = \frac{80}{1,125} = +7.11\%$$

#### Step 4: Forensic Audit Interpretation
Scaled accruals above +10% place Company Alpha in the highest accrual decile documented by Richard Sloan (1996).
Net Income surged by 75% while physical cash flow from operations fell by 20%.
The explosion in working capital ($\Delta \text{Non-Cash Current Assets} = +180$) indicates massive uncollected receivables or unsold inventory build-up.
Future earnings reversal and multiple compression are statistically imminent within 12 to 24 months.

</details>

---

## Drill 2: Days Sales Outstanding (DSO) Channel Stuffing Audit

### Scenario
Company Beta operates in the enterprise hardware sector.
Over four quarters, it reports the following revenue and Accounts Receivable balances (figures in millions):

```
+-----------------------------------------------------------------------+
| Metric                 | Q1          | Q2          | Q3          | Q4 |
|------------------------+-------------+-------------+-------------+----|
| Quarterly Revenue      | $200        | $210        | $220        | $280 |
| Accounts Receivable    | $130        | $150        | $185        | $270 |
| Trailing 12M Revenue   | $800        | $820        | $850        | $910 |
+-----------------------------------------------------------------------+
```

### Questions to Solve
1. Calculate the quarterly Days Sales Outstanding (DSO) for each quarter using the standard 90-day convention: $\text{DSO} = (\text{AR} / \text{Quarterly Revenue}) \times 90$.
2. Calculate the year-over-year percentage growth in Q4 Revenue versus Q4 Accounts Receivable.
3. Identify the primary forensic explanation for this decoupling.

<details>
<summary>Reveal Forensic Audit & Solution</summary>

#### Step 1: Quarterly DSO Calculation
$$\text{DSO}_{Q1} = \frac{130}{200} \times 90 = 58.5 \text{ days}$$
$$\text{DSO}_{Q2} = \frac{150}{210} \times 90 = 64.3 \text{ days}$$
$$\text{DSO}_{Q3} = \frac{185}{220} \times 90 = 75.7 \text{ days}$$
$$\text{DSO}_{Q4} = \frac{270}{280} \times 90 = 86.8 \text{ days}$$

#### Step 2: Year-over-Year Growth Comparison
Assuming Q4 of the prior year had revenue of $215 million and AR of $135 million:
Revenue grew at:
$$\frac{280 - 215}{215} = +30.2\%$$
Accounts Receivable grew at:
$$\frac{270 - 135}{135} = +100.0\%$$

#### Step 3: Forensic Conclusion
Receivables grew more than three times faster than revenue, driving DSO from 58.5 days to 86.8 days.
This pattern is a classic signature of end-of-year channel stuffing.
Management offered extended payment terms, deep off-book discounts, or right-of-return concessions to distributors to meet consensus sales targets.
Q1 of the following year will experience severe revenue collapse and cash collection deficits as channels digest excess inventory.

</details>

---

## Drill 3: Capitalized Operating Expenses Shenanigans

### Scenario
Company Gamma is an optical telecommunications provider expanding its fiber network.
Over three years, the company reports the following financial figures (figures in millions):

```
+-----------------------------------------------------------------------+
| Metric                                   | Year 1   | Year 2 | Year 3 |
|------------------------------------------+----------+--------+--------|
| Revenue                                  | $500     | $520   | $540   |
| Line Cost / Maintenance Expense (P&L)   | $220     | $180   | $120   |
| Reported Gross Margin                    | 56.0%    | 65.4%  | 77.8%  |
| Capital Expenditures (Cash Flow Stmt)   | $80      | $140   | $230   |
| Net Property, Plant & Equipment (PP&E)  | $400     | $500   | $680   |
| Operating Cash Flow (CFO)                | $110     | $170   | $240   |
+-----------------------------------------------------------------------+
```

### Questions to Solve
1. Analyze the relationship between the dramatic gross margin expansion and the surge in Capital Expenditures.
2. Explain how misclassifying routine maintenance costs as capitalized assets inflates both Net Income and Operating Cash Flow.
3. Calculate true adjusted Operating Cash Flow and true adjusted Free Cash Flow for Year 3 assuming baseline line costs remained constant at 44% of revenue.

<details>
<summary>Reveal Forensic Audit & Solution</summary>

#### Step 1: Anomaly Identification
Reported gross margin expanded from 56.0% to 77.8% while line costs on the income statement dropped from $220 million to $120 million.
Simultaneously, Capital Expenditures exploded from $80 million to $230 million, and PP&E grew by 70%.
This is the classic WorldCom playbook: shifting routine network maintenance operating expenses off the income statement and capitalizing them as long-term assets on the balance sheet.

#### Step 2: Cash Flow and Income Statement Mechanics
Capitalizing operating costs:
1. Removes the expense from the income statement, immediately inflating reported Operating Income and Net Income.
2. Removes the cash outflow from Operating Cash Flow (CFO) and moves it to Cash Flow from Investing (CFI) as capex.
3. Inflates reported CFO, creating a fraudulent appearance of high cash-generating ability.

#### Step 3: True Normalized Cash Flow Calculation
If true normalized line costs were 44% of revenue:
$$\text{True Line Cost Year 3} = 0.44 \times 540 = \$237.6 \text{ million}$$
$$\text{Reported Line Cost} = \$120.0 \text{ million}$$
$$\text{Improperly Capitalized Expense} = 237.6 - 120.0 = \$117.6 \text{ million}$$

Adjusted Operating Cash Flow:
$$\text{Adjusted CFO} = \text{Reported CFO} - \text{Improper Capitalization} = 240 - 117.6 = \$122.4 \text{ million}$$

Adjusted Free Cash Flow (FCF = CFO - Capex):
$$\text{Adjusted Capex} = 230 - 117.6 = \$112.4 \text{ million}$$
$$\text{Adjusted FCF} = 122.4 - 112.4 = \$10.0 \text{ million}$$
Reported FCF was $240 - 230 = \$10.0 \text{ million}$.
While total FCF remains identical, reported CFO was overstated by nearly 100%, and future periods will suffer massive non-cash asset impairment charges.

</details>

---

## Drill 4: Beneish M-Score Component Diagnostics

### Scenario
An automated quantitative forensic screen flags Company Delta with the following trailing metrics:

```
+-----------------------------------------------------------------------+
| Beneish Variable                           | Value   | Safe Threshold |
|--------------------------------------------+---------+----------------|
| Days Sales in Receivables Index (DSRI)    | 1.45    | <= 1.05        |
| Gross Margin Index (GMI)                   | 1.28    | <= 1.02        |
| Asset Quality Index (AQI)                  | 1.35    | <= 1.04        |
| Sales Growth Index (SGI)                   | 1.32    | <= 1.15        |
| Depreciation Index (DEPI)                  | 0.82    | >= 0.95        |
| Sales, General & Admin Index (SGAI)        | 1.18    | <= 1.03        |
| Leverage Index (LVGI)                      | 1.12    | <= 1.05        |
| Total Accruals to Total Assets (TATA)      | 0.08    | <= 0.02        |
+-----------------------------------------------------------------------+
```

### Questions to Solve
1. Using the 8-variable Beneish M-Score formula, compute the composite M-Score:
   $$\text{M-Score} = -4.84 + 0.920 \cdot \text{DSRI} + 0.528 \cdot \text{GMI} + 0.404 \cdot \text{AQI} + 0.892 \cdot \text{SGI} + 0.115 \cdot \text{DEPI} - 0.172 \cdot \text{SGAI} + 0.0327 \cdot \text{LVGI} + 4.379 \cdot \text{TATA}$$
2. Determine whether Company Delta is flagged as an earnings manipulator (threshold: $M > -1.78$).
3. Detail which three individual components contribute the most risk to the score.

<details>
<summary>Reveal Forensic Audit & Solution</summary>

#### Step 1: Linear Calculation
$$\text{Constant} = -4.84$$
$$0.920 \times 1.45 = +1.3340$$
$$0.528 \times 1.28 = +0.6758$$
$$0.404 \times 1.35 = +0.5454$$
$$0.892 \times 1.32 = +1.1774$$
$$0.115 \times 0.82 = +0.0943$$
$$-0.172 \times 1.18 = -0.2030$$
$$0.0327 \times 1.12 = +0.0366$$
$$4.379 \times 0.08 = +0.3503$$

$$\text{M-Score} = -4.84 + 1.3340 + 0.6758 + 0.5454 + 1.1774 + 0.0943 - 0.2030 + 0.0366 + 0.3503 = -0.8292$$

#### Step 2: Evaluation Against Critical Threshold
The critical cutoff is $-1.78$.
A score greater than $-1.78$ indicates a high probability of accounting manipulation.
Here, $-0.83 > -1.78$.
Company Delta is strongly flagged as a probable financial statement manipulator.

#### Step 3: Primary Risk Drivers
1. **DSRI (1.45)**: Receivables grew 45% faster than sales, signaling unearned revenue recognition or uncollected billings.
2. **SGI (1.32)**: Rapid sales growth (+32%) puts enormous pressure on management to continue hitting targets.
3. **GMI (1.28)**: Prior year gross margins were higher than current year margins, showing deteriorating underlying fundamentals that management is incentivized to mask.

</details>

---

## Drill 5: Inventory Valuation and Gross Margin Distortion

### Scenario
Company Epsilon manufactures specialty semiconductors.
Over two periods, the company faces declining consumer demand, but reports higher operating profits.
Filings reveal the following data:

```
+-----------------------------------------------------------------------+
| Metric                                   | Year 1        | Year 2     |
|------------------------------------------+---------------+------------|
| Units Produced                           | 1,000,000     | 1,500,000  |
| Units Sold                               | 1,000,000     | 900,000    |
| Selling Price per Unit                   | $100          | $100       |
| Total Fixed Manufacturing Overhead       | $30,000,000   | $30,000,000|
| Variable Cost per Unit                   | $40           | $40        |
| Ending Inventory (Units)                 | 0             | 600,000    |
+-----------------------------------------------------------------------+
```

### Questions to Solve
1. Under absorption costing, calculate the product cost per unit in Year 1 versus Year 2.
2. Compute reported Gross Profit in Year 1 versus Year 2.
3. Explain how management manufactured paper profits by deliberately overproducing into a demand slowdown.

<details>
<summary>Reveal Forensic Audit & Solution</summary>

#### Step 1: Unit Cost Calculation Under Absorption Costing
In Year 1:
$$\text{Fixed Overhead per Unit} = \frac{\$30,000,000}{1,000,000} = \$30.00$$
$$\text{Total Cost per Unit} = \$40 (\text{variable}) + \$30 (\text{fixed}) = \$70.00$$

In Year 2:
$$\text{Fixed Overhead per Unit} = \frac{\$30,000,000}{1,500,000} = \$20.00$$
$$\text{Total Cost per Unit} = \$40 (\text{variable}) + \$20 (\text{fixed}) = \$60.00$$

#### Step 2: Gross Profit Calculation
In Year 1:
$$\text{Revenue} = 1,000,000 \times \$100 = \$100,000,000$$
$$\text{COGS} = 1,000,000 \times \$70 = \$70,000,000$$
$$\text{Gross Profit} = 100,000,000 - 70,000,000 = \$30,000,000 \quad (30.0\% \text{ margin})$$

In Year 2:
$$\text{Revenue} = 900,000 \times \$100 = \$90,000,000$$
$$\text{COGS} = 900,000 \times \$60 = \$54,000,000$$
$$\text{Gross Profit} = 90,000,000 - 54,000,000 = \$36,000,000 \quad (40.0\% \text{ margin})$$

#### Step 3: Forensic Audit Takeaway
Even though unit sales fell by 10% (from 1,000,000 to 900,000) and selling prices remained flat, reported Gross Profit expanded by 20% (from $30M to $36M), and gross margin rose from 30% to 40%.
By overproducing 600,000 unsold units, management absorbed $12 million of fixed factory overhead ($600,000 \times \$20$) into balance sheet inventory rather than expensing it on the income statement.
When the company eventually slows production to liquidate inventory, unabsorbed fixed overhead will crush reported margins, accompanied by major inventory write-downs.

</details>

---

## Drill 6: The Deferred Tax Valuation Allowance Cushion

### Scenario
Company Zeta has generated cumulative pre-tax operating losses of $200 million over the past three years.
It has accumulated $50 million of Gross Deferred Tax Assets (DTAs) with a 25% statutory tax rate.
At Year t-1, the Valuation Allowance against DTAs was $50 million (carrying value of DTAs = $0).
In Year t, pre-tax operating income is $15 million.
However, management lowers the Valuation Allowance from $50 million to $20 million.

```
+-----------------------------------------------------------------------+
| Income Statement Component                | Year t Reported           |
|-------------------------------------------+---------------------------|
| Pre-Tax Income                            | $15,000,000               |
| Current Tax Expense                       | $0                        |
| Deferred Tax Benefit (Allowance Release)  | -$30,000,000              |
| Reported Net Income                       | $45,000,000               |
+-----------------------------------------------------------------------+
```

### Questions to Solve
1. Analyze the tax footnote entry to explain how Company Zeta generated a Net Income three times larger than its Pre-Tax Operating Income.
2. Compute the company's Effective Tax Rate for Year t.
3. Assess the sustainability of this earnings quality.

<details>
<summary>Reveal Forensic Audit & Solution</summary>

#### Step 1: Accounting Mechanism
Management released $30 million of its previously established Valuation Allowance against Deferred Tax Assets.
Under GAAP/IFRS, reversing a valuation allowance passes directly through the tax provision line on the income statement as a negative tax expense (tax benefit).
This non-cash, purely discretionary accounting estimate generated $30 million of reported Net Income without a single dollar of cash generation.

#### Step 2: Effective Tax Rate Calculation
$$\text{Effective Tax Rate} = \frac{\text{Reported Tax Provision}}{\text{Pre-Tax Income}} = \frac{-\$30,000,000}{\$15,000,000} = -200.0\%$$

#### Step 3: Earnings Quality Assessment
Earnings quality is near zero.
$30 million out of the $45 million in reported Net Income (66.7%) is a one-time non-cash paper gain that cannot recur.
Operating earnings power is only $15 million, yet algorithmic screeners will see a trailing P/E ratio based on $45 million of earnings.
Analysts must strip out the valuation allowance reversal to reflect true ongoing earning power.

</details>
