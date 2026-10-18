---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Buffett (1986) - Berkshire Hathaway Shareholder Letter (Owner Earnings), Damodaran (2012) - Investment Valuation, Koller Goedhart and Wessels (2020) - Valuation (McKinsey), Penman (2013) - Financial Statement Analysis and Security Valuation]
---

# Capex: Maintenance vs Growth and Owner Earnings

## TL;DR

- Total capital expenditures (Capex) reported on the Cash Flow Statement split fundamentally into Maintenance Capex and Growth Capex.
- Maintenance Capex represents the capital required to replace aging assets, repair facilities, and preserve current competitive positioning and unit output.
- Growth Capex is discretionary capital deployed to open new facilities, enter new geographic markets, or acquire revenue-producing capacity.
- Warren Buffett (1986) formulated Owner Earnings as reported earnings plus non-cash charges minus the average annual maintenance capex required to maintain long-term competitive position.
- In inflationary environments, historical cost depreciation severely underestimates the cash required to replace physical assets, creating phantom accounting profits.
- Under IFRS 16 and ASC 842, operating leases longer than 12 months must be recognized on the balance sheet as Right-of-Use (ROU) assets and lease liabilities.
- Only IFRS 16 transforms rent expense into depreciation and interest (raising EBITDA); ASC 842 keeps a single straight-line operating-lease cost inside operating expenses, so EBITDA is essentially unchanged.

## Learning objectives

- Deconstruct total capital expenditures into maintenance and growth components using analytical and disclosure-based methods.
- Calculate Warren Buffett's Owner Earnings and compare it to GAAP Net Income and Free Cash Flow.
- Analyze the distortion of historical depreciation accounting during sustained inflationary regimes.
- Evaluate capital intensity metrics across industries (Capex/Revenue, Capex/D&A, Reinvestment Rate).
- Reconcile lease accounting under ASC 842 / IFRS 16 and adjust EBITDA, enterprise value, and return on invested capital.

## Core concepts

### 1. Growth Capex vs Maintenance Capex

Total capital expenditures on the Cash Flow Statement (Cash Flow from Investing) aggregate two economically distinct activities:

$$\text{Total Capex} = \text{Maintenance Capex} + \text{Growth Capex}$$

```
+-----------------------------------------------------------------------+
|                    CAPEX DECOMPOSITION FRAMEWORK                      |
+-----------------------------------------------------------------------+
| FEATURE                 | MAINTENANCE CAPEX      | GROWTH CAPEX       |
+-------------------------+------------------------+--------------------+
| Economic Purpose        | Replace worn equipment,| Expand capacity,   |
|                         | maintain current output| enter new markets  |
| Discretionary Status    | Non-discretionary      | Fully discretionary|
| Consequence of cutting  | Lost market share,     | Deferred expansion,|
|                         | asset degradation      | preserved cash flow|
| Relationship to D&A     | Often approximates D&A | Exceeds D&A during |
|                         | in zero-inflation      | expansion phase    |
| Impact on Earning Power | Preserves baseline     | Compounds future   |
|                         | earning power          | earning power      |
+-----------------------------------------------------------------------+
```

Because companies rarely disclose exact maintenance capex figures in SEC filings, fundamental analysts employ three estimation methods:
1. **Depreciation Benchmark**: In low-inflation environments, maintenance capex is often approximated by tangible asset depreciation ($\text{Maintenance Capex} \approx \text{Depreciation}$).
2. **Unit / Capacity Scaling**: Estimating capex per unit of production (e.g. per retail store or per barrel of oil) and multiplying by existing baseline units.
3. **Greenwald Growth Ratio Method**: Bruce Greenwald (2001) estimates growth capex by tracking changes in revenue relative to gross plant assets:
   $$\text{Capital-to-Sales Ratio} = \frac{\text{Gross PP&E}}{\text{Revenue}}$$
   $$\text{Growth Capex}_t = \Delta \text{Revenue}_t \times \left(\frac{\text{Gross PP&E}}{\text{Revenue}}\right)$$
   $$\text{Maintenance Capex}_t = \text{Total Capex}_t - \text{Growth Capex}_t$$

### 2. Warren Buffett's Owner Earnings Formulation

In his 1986 Berkshire Hathaway shareholder letter, Warren Buffett critiqued standard accounting metrics like Net Income and cash flow metrics like EBITDA, introducing **Owner Earnings**:

$$\text{Owner Earnings} = \text{Reported Net Income} + \text{D&A} + \text{Other Non-Cash Charges} - \text{Average Maintenance Capex} \pm \Delta \text{Working Capital}$$

Buffett's argument, paraphrased rather than quoted:
- If a company must spend $\$100\text{M}$ annually simply to replace trucks, machines, and software to maintain unit volume, that $\$100\text{M}$ can never be distributed to owners.
- It is a mandatory cost of staying in business, so it must be deducted before any earnings are called distributable.

EBITDA completely ignores capex, treating cash spent on replacement machinery as if it were distributable profit.
For capital-intensive companies (railroads, utilities, airlines), Owner Earnings is often less than half of reported EBITDA.

### 3. Depreciation Inadequacy in Inflationary Regimes

Standard GAAP accounting computes depreciation on the **historical acquisition cost** of an asset:

$$\text{Depreciation}_t = \frac{\text{Historical Purchase Price}}{\text{Useful Life}}$$

During sustained inflation:
- A factory asset purchased 10 years ago for $\$10,000,000$ depreciates at $\$1,000,000$ per year on financial statements.
- When the machine reaches the end of its useful life, replacing it today costs $\$25,000,000$ due to cumulative inflation.
- The $\$1,000,000$ annual depreciation tax shield and cash reserve falls disastrously short of funding the $\$25,000,000$ replacement cost.

Historical cost accounting creates **phantom profits**: reported Net Income appears high because depreciation expense is artificially depressed by outdated historical prices.
When the asset must finally be replaced, the company is forced to borrow debt or issue shares simply to maintain existing output.

### 4. Capital Intensity Metrics and the Reinvestment Rate

To evaluate a company's capital allocation efficiency:
- **Capex-to-Revenue Ratio**:
  $$\text{Capital Intensity} = \frac{\text{Capex}}{\text{Revenue}}$$
  Software and asset-light platforms operate at $2\% - 5\%$; semiconductor fabrication plants, telecommunication networks, and pipelines operate at $15\% - 30\%$.
- **Capex-to-D&A Ratio**:
  $$\frac{\text{Capex}}{\text{D&A}}$$
  A ratio $> 1.0$ indicates aggressive balance sheet expansion (Growth Capex); a ratio $< 1.0$ indicates capital underinvestment, where assets are wearing out faster than they are being replaced.
- **Fundamental Reinvestment Rate**:
  $$\text{Reinvestment Rate} = \frac{\text{Net Capex} + \Delta \text{Working Capital}}{\text{NOPAT}}$$
  Determines the proportion of after-tax operating profit plowed back into operations to drive organic earnings growth.

### 5. Lease Accounting: IFRS 16 and ASC 842

Prior to 2019, companies categorized leases as either capital leases (on balance sheet) or operating leases (off balance sheet in footnotes).
Retailers and airlines hid tens of billions in lease debt off their balance sheets, recognizing rent as a simple operating expense.

Under ASC 842 and IFRS 16:
- All leases longer than 12 months are capitalized on the balance sheet (IFRS 16 also exempts low-value assets):
  - **Asset Side**: Right-of-Use (ROU) Asset, reflecting the present value of future lease payments.
  - **Liability Side**: Lease Liability, reflecting the debt obligation to make lease payments.
- **Income Statement Shift under IFRS 16** (single lessee model): Rent expense is eliminated.
  It is replaced by **Depreciation of the ROU Asset** (operating expense below EBITDA) and **Interest Expense** on the lease liability (financing expense).
- **Income Statement under ASC 842** (dual model): Finance leases get the same depreciation-plus-interest split, but operating leases keep a single straight-line lease cost inside operating expenses, so EBITDA and EBIT are essentially unchanged.
- **Valuation Impact under IFRS 16**: EBITDA increases because rent is removed from operating costs, so Enterprise Value must include lease liabilities as debt to avoid valuation distortions.
- **Valuation Impact under ASC 842**: EBITDA still deducts operating-lease rent, so either leave operating-lease liabilities out of EV/EBITDA or add them to EV and divide by EBITDAR (EBITDA plus rent).

---

## Worked examples

### Example 1: Calculating Warren Buffett's Owner Earnings

A regional freight rail operator reports the following financials for the fiscal year:
- Reported Net Income: $\$450,000,000$
- Depreciation & Amortization: $\$320,000,000$
- Other Non-Cash Charges (SBC and impairments): $\$30,000,000$
- Total Capital Expenditures: $\$480,000,000$
- Increase in Non-Cash Operating Working Capital: $\$40,000,000$

Engineering and regulatory disclosures reveal that the company spends $\$300,000,000$ annually replacing worn rails, ties, locomotives, and maintaining signal systems to sustain existing track miles and freight capacity (Maintenance Capex).
The remaining $\$180,000,000$ was spent laying new double-track routes to expand capacity into a new industrial corridor (Growth Capex).

1. **Calculate Free Cash Flow (Standard Definition)**:
   $$\text{CFO} = \text{Net Income} + \text{D&A} + \text{Non-Cash} - \Delta \text{NWC}$$
   $$\text{CFO} = \$450\text{M} + \$320\text{M} + \$30\text{M} - \$40\text{M} = \$760,000,000$$
   $$\text{Standard FCF} = \text{CFO} - \text{Total Capex} = \$760\text{M} - \$480\text{M} = \$280,000,000$$
2. **Calculate Warren Buffett's Owner Earnings**:
   $$\text{Owner Earnings} = \text{Net Income} + \text{D&A} + \text{Non-Cash} - \text{Maintenance Capex} - \Delta \text{NWC}$$
   $$\text{Owner Earnings} = \$450\text{M} + \$320\text{M} + \$30\text{M} - \$300\text{M} - \$40\text{M} = \$460,000,000$$

Standard FCF ($\$280\text{M}$) penalizes the business for $\$180\text{M}$ of growth investments that expand future earning power.
Owner Earnings ($\$460\text{M}$) reflects the true annual cash generated that could be distributed to owners without impairing operations.

### Example 2: Lease Capitalization Impact (IFRS 16 versus ASC 842)

A national retail chain enters into a 5-year operating lease for store locations:
- Annual lease payment: $\$10,000,000$ due at year-end.
- Incremental borrowing rate: $6.0\%$.

1. **Calculate Present Value of Lease Payments (ROU Asset & Liability)**:
   $$\text{PV} = \$10\text{M} \times \left[ \frac{1 - (1 + 0.06)^{-5}}{0.06} \right] = \$10\text{M} \times 4.212364 = \$42,123,638$$
2. **Balance Sheet Recognition**:
   - ROU Asset: $+\$42,123,638$
   - Lease Liability: $+\$42,123,638$
3. **Year 1 Income Statement & Cash Flow Shift**:
   - Prior Accounting: Operating Rent Expense of $\$10,000,000$ reduced EBITDA by $\$10\text{M}$.
   - Under IFRS 16:
     - Straight-line ROU Depreciation: $\frac{\$42,123,638}{5} = \$8,424,728$ (Operating D&A).
     - Year 1 Interest Expense: $\$42,123,638 \times 6.0\% = \$2,527,418$ (Financing Expense).
     - **EBITDA Impact**: EBITDA increases by the full $+\$10,000,000$ because rent is eliminated from operating costs.
     - **CFO Impact**: The Year 1 principal repayment of $\$10,000,000 - \$2,527,418 = \$7,472,582$ is classified in CFF, inflating CFO by that amount.
   - Under ASC 842 (operating lease):
     - Single straight-line lease cost: $\frac{5 \times \$10,000,000}{5} = \$10,000,000$ in operating expenses.
     - **EBITDA Impact**: None; EBITDA still deducts the $\$10,000,000$, and only the balance sheet gains the ROU asset and lease liability.
     - **CFO Impact**: None; the whole $\$10,000,000$ payment stays in CFO.

---

## Pitfalls

- **Confusing Total Capex with Maintenance Capex**: Assuming that all capex is mandatory; high-growth compounders reinvesting $100\%$ of cash flow into high-ROIC expansion appear to have zero free cash flow, masking underlying earning power.
- **Ignoring Software Capitalization**: Software companies capitalizing internal developer salaries into balance sheet intangible assets, hiding operating expenses from the Income Statement and bloating perceived margins.
- **Relying on Depreciation in Asset-Heavy Mature Companies**: Assuming maintenance capex equals D&A during periods of severe inflation; replacing 20-year-old infrastructure requires far more cash than historical depreciation allowances.
- **Double-Counting Lease Debt in Valuation Multiples**: Adding capitalized lease debt to Enterprise Value while failing to use lease-adjusted EBITDA in the denominator (EBITDAR for ASC 842 operating leases).
- **Underestimating Maintenance Capex in Cyclical Troughs**: Slashing capex during recessions to preserve reported cash flow; deferred maintenance accumulates as an invisible liability, leading to future catastrophic equipment failures.

---

## Interview questions

> [!question]- mkt-fa-065 | What is the fundamental difference between Maintenance Capex and Growth Capex?
> Maintenance capex is non-discretionary capital required to replace aging assets and maintain existing output; growth capex is discretionary capital invested to expand capacity and revenue.

> [!question]- mkt-fa-066 | Define Warren Buffett's Owner Earnings (1986).
> Owner Earnings = Reported Net Income + D&A + Non-Cash Charges - Average Maintenance Capex +/- Delta Working Capital; representing true distributable cash flow.

> [!question]- mkt-fa-067 | Why did Warren Buffett criticize EBITDA as an investment metric?
> Because EBITDA ignores capital expenditures; treating cash required to replace worn assets as if it were free cash available for distribution to owners is a dangerous delusion.

> [!question]- mkt-fa-068 | How does inflation create phantom profits under historical cost depreciation accounting?
> Historical depreciation is based on outdated original purchase prices; when replacing assets costs significantly more due to inflation, real economic capital is consumed despite positive accounting profits.

> [!question]- mkt-fa-069 | What does a Capex-to-D&A ratio significantly greater than 1.0 indicate?
> It indicates aggressive balance sheet expansion and capacity investment (growth capex), common in fast-growing capital-intensive companies.

> [!question]- mkt-fa-070 | What does a Capex-to-D&A ratio significantly less than 1.0 indicate?
> It indicates capital underinvestment, where a company is deferring maintenance and allowing its physical asset base to depreciate without adequate replacement.

> [!question]- mkt-fa-071 | How does Bruce Greenwald's method estimate growth capex?
> By multiplying incremental revenue growth by the historical capital-to-sales ratio (Gross PP&E / Revenue), then subtracting that growth capex from total capex to yield maintenance capex.

> [!question]- mkt-fa-072 | How are operating leases accounted for on the balance sheet under ASC 842 / IFRS 16?
> Leases are recognized on the balance sheet as Right-of-Use (ROU) assets offset by matching lease liabilities equal to the present value of future lease payments.

> [!question]- mkt-fa-073 | What is the impact of IFRS 16 lease capitalization on reported EBITDA?
> EBITDA increases significantly because operating rent expense is eliminated from operating costs, replaced by depreciation of the ROU asset and financing interest expense.

> [!question]- mkt-fa-074 | When evaluating EV/EBITDA under IFRS 16 versus ASC 842, when must lease liabilities be included in Enterprise Value?
> Under IFRS 16, EBITDA no longer deducts rent, so lease liabilities must be treated as debt in EV for consistency; under ASC 842, operating-lease cost still sits inside EBITDA, so lease liabilities belong in EV only if rent is added back (EV/EBITDAR).

> [!question]- mkt-fa-075 | What is the Reinvestment Rate formula in corporate finance?
> Reinvestment Rate = (Net Capex + Delta Non-Cash Working Capital) / NOPAT; measuring the fraction of after-tax operating profits reinvested into the business.

> [!question]- mkt-fa-076 | What is the relationship between Reinvestment Rate, ROIC, and fundamental earnings growth?
> Fundamental Growth Rate = ROIC * Reinvestment Rate; long-term sustainable growth equals the return on invested capital multiplied by the percentage of profits reinvested.

> [!question]- mkt-fa-077 | What is software capitalization and how does it distort operating cash flow?
> Capitalizing internal software developer payroll as an intangible asset shifts operating cash outflows into CFI capex, artificially inflating reported Operating Cash Flow (CFO).

> [!question]- mkt-fa-078 | What is the difference between tangible asset depreciation and intangible asset amortization?
> Depreciation applies to physical assets (buildings, machinery, servers); amortization applies to acquired intangible assets (patents, customer lists, software licenses).

> [!question]- mkt-fa-079 | Why is goodwill not amortized under US GAAP and IFRS?
> Goodwill has an indefinite useful life and is not systematically amortized; instead, it is tested annually for impairment and written down only if fair value falls below book value.

> [!question]- mkt-fa-080 | What is capital intensity and which sectors have the highest capital intensity?
> Capital intensity is the ratio of capital investment to revenue (Capex / Sales); utilities, telecommunications, energy pipelines, and semiconductor fabrication have the highest.

> [!question]- mkt-fa-081 | Why do asset-light businesses often command higher valuation multiples than asset-heavy businesses?
> Asset-light businesses require minimal maintenance capex to grow, allowing a larger percentage of operating income to convert directly into distributable free cash flow.

> [!question]- mkt-fa-082 | What is dry capex vs maintenance capex in shipping and drilling?
> Dry capex represents periodic dry-docking and mandatory regulatory inspection costs required to keep maritime vessels legally certified to operate in global waters.

> [!question]- mkt-fa-083 | How does deferred maintenance manifest as an invisible corporate liability?
> Cutting maintenance capex temporarily boosts reported cash flow, but assets deteriorate, eventually causing operational bottlenecks, safety failures, and massive emergency capex outlays.

> [!question]- mkt-fa-084 | What is the salvage value of an asset?
> The estimated residual resale value of a tangible asset at the end of its useful economic life, used to determine total depreciable base (Cost - Salvage Value).

> [!question]- mkt-fa-085 | What is accelerated tax depreciation (e.g. MACRS / Section 179)?
> Tax rules allowing companies to deduct a larger portion of asset cost in the early years of asset life, deferring cash tax payments and creating Deferred Tax Liabilities.

> [!question]- mkt-fa-086 | How does capitalized interest affect financial statements during construction?
> Interest incurred to finance construction of major PP&E is added to asset cost on the balance sheet rather than expensed, temporarily boosting Net Income during construction.

> [!question]- mkt-fa-087 | What is the difference between straight-line depreciation and units-of-production depreciation?
> Straight-line deducts equal expense per time period; units-of-production deducts expense proportional to actual asset utilization (e.g. flight hours or tons extracted).

> [!question]- mkt-fa-088 | Why does standard Free Cash Flow (CFO - Capex) penalize compounders?
> Because it treats voluntary, high-ROIC growth capex that expands future earnings identically to defensive maintenance capex that merely preserves current operations.

> [!question]- mkt-fa-089 | What is asset impairment and under what condition is it triggered?
> An impairment charge is recognized when an asset's carrying book value exceeds its undiscounted expected future cash flows (GAAP) or recoverable amount (IFRS).

> [!question]- mkt-fa-090 | How does asset aging affect the maintenance capex required to preserve operations?
> As physical assets exceed their median design life, maintenance repair expenses and maintenance capex escalate non-linearly to prevent operational downtime.

> [!question]- mkt-fa-091 | What is the replacement cost approach to business valuation?
> Valuing a company based on the total capital expenditure required today to replicate its physical asset footprint, distribution network, and productive capacity from scratch.

> [!question]- mkt-fa-092 | What is sale-and-leaseback transaction?
> A company sells a physical asset (e.g. corporate real estate) to an investor for immediate cash and simultaneously leases it back, monetizing balance sheet equity.

> [!question]- mkt-fa-093 | Why does a negative Net Capex (Capex < D&A) raise red flags for cyclical manufacturing firms?
> It indicates the firm is liquidating its productive physical asset base through underinvestment, signaling deteriorating competitive positioning.

> [!question]- mkt-fa-094 | How does capital expenditure forecasting integrate into DCF modeling?
> Future capex is modeled as a percentage of revenue or driven by capacity expansion targets, balancing asset turnover and return on invested capital assumptions.

> [!question]- mkt-fa-095 | What is capital allocation in the context of growth capex?
> The management discipline of deploying retained corporate earnings across competing uses (growth capex, R&D, M&A, share repurchases, debt retirement, dividends) to maximize per-share value.

> [!question]- mkt-fa-096 | What is the ultimate test of whether growth capex was well-spent?
> Whether the incremental capital deployed generated a Return on Incremental Invested Capital (ROIIC) comfortably exceeding the company's Weighted Average Cost of Capital (WACC).

---

## Further reading

- Buffett, W. E. (1986). *Berkshire Hathaway Shareholder Letter: Appendix on Owner Earnings*. Berkshire Hathaway Inc.
- Damodaran, A. (2012). *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset*. John Wiley & Sons.
- Greenwald, B. C., Kahn, J., Sonkin, P. D., & van Biema, M. (2001). *Value Investing: From Graham to Buffett and Beyond*. John Wiley & Sons.
- Koller, T., Goedhart, M., & Wessels, D. (2020). *Valuation: Measuring and Managing the Value of Companies* (7th ed.). John Wiley & Sons.
