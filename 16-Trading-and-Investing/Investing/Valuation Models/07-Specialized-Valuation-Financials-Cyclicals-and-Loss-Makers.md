---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [BIO Informa and QLS (2021) - Clinical Development Success Rates 2011-2020, Damodaran (2009) - Valuing Financial Service Firms, Damodaran (2012) - Investment Valuation: Tools and Techniques for Determining the Value of Any Asset, Koller Goedhart and Wessels (2020) - Valuation: Measuring and Managing the Value of Companies (McKinsey)]
---

# Specialized Valuation: Financials, Cyclicals, and High-Growth Loss-Makers

## TL;DR

- Standard enterprise DCF and EV/EBITDA valuation models collapse when applied to specialized sectors such as commercial banking, insurance, cyclical commodities, and unprofitable high-growth technology firms.
- Commercial banks cannot be valued with Enterprise Value because debt represents operating raw material (customer deposits) rather than capital structure; banks are valued using Price-to-Tangible Book Value (P/TBV) governed by Return on Tangible Common Equity (ROTCE) and the Dividend Discount Model (DDM) constrained by regulatory capital ratios (CET1).
- Cyclical and commodity producers display an inverse multiple trap: P/E is often high at cyclical troughs, when earnings are depressed, and low at peaks, when earnings are inflated, so trailing P/E can point the wrong way.
- Valuing high-growth, unprofitable software enterprises requires unit economics decomposition: Customer Lifetime Value (LTV), Customer Acquisition Cost (CAC), Payback Period, and the Rule of 40.
- Early-stage biotechnology companies are often valued through risk-adjusted Net Present Value (rNPV) models, discounting cash flows weighted by clinical phase transition probabilities.

## Learning objectives

- Explain why traditional FCFF, operating working capital, and EV/EBITDA fail when applied to financial institutions.
- Formulate and calibrate a regulatory-capital-constrained Dividend Discount Model (DDM) for commercial banks.
- Model the relationship between Return on Tangible Common Equity (ROTCE) and justified Price-to-Tangible Book Value (P/TBV).
- Execute mid-cycle earnings normalization for commodity and cyclical companies to eliminate the inverse multiple trap.
- Deconstruct early-stage software and consumer internet platforms using unit economics (LTV/CAC, cohort retention, Rule of 40).
- Construct risk-adjusted Net Present Value (rNPV) models for clinical-stage biotechnology pipelines.

## Core concepts

### 1. Financial Institutions: Why Traditional Models Fail

Commercial banks and insurance companies possess balance sheets and income statements that invert conventional corporate finance assumptions:

```
+-----------------------------------------------------------------------+
|                    THE BANK VALUATION CONUNDRUM                       |
+-----------------------------------------------------------------------+
| CONVENTIONAL ENTERPRISE                COMMERCIAL BANK                |
| - Debt is a financing choice.          - Debt (Deposits) is OPERATING |
|                                          RAW MATERIAL.                |
| - Interest is a financing cost.        - Interest is CORE COST OF     |
|                                          GOODS SOLD.                  |
| - PP&E generates revenue.              - Regulatory Capital (Equity)  |
|                                          enables balance sheet scale. |
| - EV/EBITDA works well.                - EV and EBITDA are MEANINGLESS|
+-----------------------------------------------------------------------+
```

Because interest expense cannot be separated from operating income, and debt cannot be separated from operating liabilities, **Enterprise Value cannot be defined for a bank**.
Valuation must proceed strictly at the equity level.

### 2. The P/TBV - ROTCE Framework for Banks

A bank's intrinsic equity value is governed by its Return on Tangible Common Equity (ROTCE) relative to its Cost of Equity ($K_e$):

$$\frac{P}{\text{TBV}} = \frac{\text{ROTCE} - g}{K_e - g}$$

Where:
- $\text{Tangible Book Value (TBV)} = \text{Common Equity} - \text{Goodwill} - \text{Intangibles}$.
- $\text{ROTCE} = \frac{\text{Net Income} - \text{Preferred Dividends}}{\text{Average Tangible Common Equity}}$.

```
+-----------------------------------------------------------------------+
|                   THE BANK VALUATION MATRIX (ROTCE VS P/TBV)          |
+---------------------+-------------------+-----------------------------+
| ROTCE Performance   | Spread (ROTCE-Ke) | Justified Price / TBV       |
+---------------------+-------------------+-----------------------------+
| ROTCE = 15%         | +5 points         | 1.71x TBV                   |
| ROTCE = 10% (Ke)    | Zero (Fair Return)| Exactly 1.00x TBV           |
| ROTCE = 8%          | -2 points         | 0.71x TBV                   |
| (Ke 10% and g 3% throughout; hypothetical inputs)                     |
+---------------------+-------------------+-----------------------------+
```

#### Regulatory Capital Constraints and the DDM
Banks cannot freely distribute all earnings as dividends.
The Basel Framework sets a minimum **Common Equity Tier 1 (CET1)** ratio of 4.5% of risk-weighted assets (RBC20.1) plus a 2.5% capital conservation buffer of CET1 (RBC30.2), 7.0% in total before any countercyclical buffer, systemic surcharge or national add-on.
Banks typically manage to a target above their own requirement, and that target is what binds dividends.
The cash flow available to equity in any year is strictly:

$$\text{Allowable Dividend} = \text{Net Income} - (\Delta \text{Risk-Weighted Assets} \times \text{Target CET1 Ratio})$$

If Risk-Weighted Assets (loans) grow rapidly, a bank may generate high net income yet have zero distributable cash flow because all profits are retained to satisfy regulatory capital requirements.

### 3. Cyclical and Commodity Companies: The Inverse Multiple Trap

For commodity producers (mining, energy, chemicals, steel) and cyclical industrials (semiconductors, heavy machinery), earnings fluctuate wildly with global macro cycles.
Valuing these firms on trailing multiples produces disastrous results:

```
+-----------------------------------------------------------------------+
|                    THE INVERSE CYCLICAL MULTIPLE TRAP                 |
+-----------------------------------------------------------------------+
| AT THE CYCLICAL PEAK:                  AT THE CYCLICAL TROUGH:        |
| - Commodity prices are at records.     - Commodity prices collapse.   |
| - Plants run at 100% capacity.         - Capacity is idled; losses.   |
| - Reported EPS is at all-time high.    - Reported EPS collapses to $0.|
| - Stock trades at a "cheap" P/E       - Stock trades at a very high  |
|   (say 5x, hypothetical).                or undefined P/E (say 40x).  |
| - Risk: peak margins will mean-revert. - Possible opportunity if      |
|                                          earnings recover.            |
+-----------------------------------------------------------------------+
```

#### Normalizing Mid-Cycle Earnings
Normalize earnings over a full economic cycle rather than a single year:
1. Estimate a mid-cycle commodity price from a full cycle of dated price history (the worked case below uses a hypothetical $3.80/lb copper).
2. Apply mid-cycle operating margins to normalized unit production capacity.
3. Compute Mid-Cycle NOPAT and value the enterprise using mid-cycle cash flows:
   $$\text{Normalized Value} = \frac{\text{Normalized EBIT} \times (1 - t)}{\text{WACC}} + \text{Growth PV}$$

### 4. High-Growth Loss-Makers: Unit Economics and the Rule of 40

Early-stage software-as-a-service (SaaS) and digital platform businesses can report large GAAP losses because customer acquisition spending is expensed upfront, while the revenue from a retained customer recurs for years.

```
+-----------------------------------------------------------------------+
|                    SAAS UNIT ECONOMICS ARCHITECTURE                   |
+-----------------------------------------------------------------------+
| 1. Customer Acquisition Cost (CAC):                                   |
|    Total Sales & Marketing Expense / New Customers Acquired           |
|                                                                       |
| 2. Customer Lifetime Value (LTV):                                     |
|    (Average Revenue Per User x Gross Margin %) / Annual Churn Rate    |
|                                                                       |
| 3. The LTV / CAC Health Metric (practitioner rule of thumb):          |
|    - Skok (SaaS Metrics 2.0): the best SaaS businesses have LTV/CAC   |
|      above 3, sometimes as high as 7 or 8.                            |
|                                                                       |
| 4. CAC Payback Period:                                                |
|    CAC / (Annualized ARPU x Gross Margin)                             |
|    (Skok: profitability is anemic if payback exceeds 12 months).      |
+-----------------------------------------------------------------------+
```

#### The Rule of 40
A practitioner benchmark balancing growth against profitability, stated by Brad Feld (2015) as growth rate plus profit (he prefers EBITDA margin) adding up to 40% for SaaS companies at scale; many analysts use the free cash flow margin instead:

$$\text{Rule of 40 Metric} = \text{Year-over-Year Revenue Growth Rate (\%)} + \text{Free Cash Flow Margin (\%)} \ge 40\%$$

A company growing revenue at 60% with a -15% FCF margin scores $60 - 15 = 45\%$ (exceeds the Rule of 40, healthy investment).
A company growing at 15% with a 10% FCF margin scores $15 + 10 = 25\%$ (below the benchmark).

### 5. Clinical-Stage Biotechnology: Risk-Adjusted NPV (rNPV)

Pre-revenue biotechnology companies cannot be valued with standard multiples.
Analysts use **risk-adjusted Net Present Value (rNPV)** by mapping peak sales and probability of clinical success:

$$\text{rNPV} = \sum_{\text{Phase}} \text{Cumulative Probability of Approval} \times \text{PV}(\text{Commercial Cash Flows}) - \text{PV}(\text{Clinical Trial Costs})$$

```
+-----------------------------------------------------------------------+
|   CLINICAL TRANSITION RATES, ALL INDICATIONS, 2011-2020 (BIO 2021)    |
+------------------------+-------------------+--------------------------+
| Starting Phase         | Phase Success Rate| Cumulative Approval Prob |
+------------------------+-------------------+--------------------------+
| Phase I                | 52.0%             | 7.9%                     |
| Phase II               | 28.9%             | 15.1%                    |
| Phase III              | 57.8%             | 52.4%                    |
| NDA / BLA Filing (FDA) | 90.6%             | 90.6%                    |
+------------------------+-------------------+--------------------------+
```

## Worked numerical case study

### Part 1: Valuing First Metro Bank (hypothetical bank and inputs)
- Tangible Common Equity (TBV): $10,000M
- Diluted Shares: 500M ($TBV per share = $20.00)
- Sustainable ROTCE: 14.0%
- Cost of Equity ($K_e$): 10.0%
- Long-term organic growth rate ($g$): 3.0%

Compute Justified P/TBV:
$$\frac{P}{\text{TBV}} = \frac{\text{ROTCE} - g}{K_e - g} = \frac{0.14 - 0.03}{0.10 - 0.03} = \frac{0.11}{0.07} = 1.571\times$$

$$\text{Intrinsic Value Per Share} = \$20.00 \times 1.5714 = \$31.43$$

If First Metro Bank trades at $22.00 (1.10x TBV), it sits 30.0% below this justified value, which is worth investigating only if the 14% ROTCE is sustainable.

### Part 2: Normalizing Cyclical Earnings for Vulcan Mining (hypothetical miner and inputs)
- Current Spot Copper Price: $5.20 / lb (a hypothetical cycle peak)
- Current Reported EBIT: $1,200M; even with zero interest, 25% tax leaves net income of at most $900M, so the reported P/E is at least $\$7,000\text{M} / \$900\text{M} = 7.8\times$ on the $35 stock price
- Annual Copper Production Capacity: 500M lbs
- Site cash operating cost: $2.20 / lb (not AISC: World Gold Council AISC already includes sustaining capital, corporate G&A and sustaining exploration, which this case deducts separately)
- Mid-Cycle Copper Price: $3.80 / lb (hypothetical)
- Tax Rate: 25.0%; Diluted Shares: 200M; Net Debt: $500M; WACC: 9.0%

#### Step 1: Normalize Mid-Cycle Earnings
$$\text{Mid-Cycle Revenue} = 500\text{M lbs} \times \$3.80 = \$1,900\text{M}$$
$$\text{Operating Production Costs} = 500\text{M lbs} \times \$2.20 = \$1,100\text{M}$$
$$\text{Corporate SG\&A \& Exploration} = \$150\text{M}$$
$$\text{Normalized Mid-Cycle EBIT} = 1,900 - 1,100 - 150 = \$650\text{M}$$
$$\text{Normalized NOPAT} = \$650\text{M} \times (1 - 0.25) = \$487.5\text{M}$$

#### Step 2: Value Mid-Cycle Enterprise Value
Assuming a mid-cycle reinvestment rate of 25% (capex exceeds D&A by $121.9M):
$$\text{Normalized Mid-Cycle FCFF} = 487.5 \times (1 - 0.25) = \$365.625\text{M}$$
$$\text{Enterprise Value (assuming 2\% terminal growth)} = \frac{365.625}{0.09 - 0.02} = \frac{365.625}{0.07} = \$5,223.2\text{M}$$
$$\text{Equity Value} = \text{EV} - \text{Net Debt} = 5,223.2 - 500.0 = \$4,723.2\text{M}$$
$$\text{Normalized Fair Value Per Share} = \frac{\$4,723.2\text{M}}{200\text{M shares}} = \$23.62$$

Forensic Cyclical Takeaway:
At $35.00, Vulcan Mining looks superficially "cheap" on peak earnings at a low P/E (at least 7.8x, and slightly higher once interest on the $500M net debt is deducted).
However, on normalized mid-cycle copper economics ($3.80/lb), its true intrinsic value is only **$23.62**.
At $35 the stock is priced 48.2% above this normalized value.
The inputs also imply a return on new capital of $g / \text{RR} = 2\% / 25\% = 8.0\%$, below the 9.0% WACC, so the assumed growth destroys value: with zero growth and no net reinvestment, EV would be $487.5 / 0.09 = \$5,416.7\text{M}$, or \$24.58 per share.

## Practice questions

> [!question]- mkt-val-193 | Why does the Enterprise Value concept fail when applied to commercial banks?
> Because bank debt (customer deposits) is an operational raw material rather than a financing choice, and interest expense is a core operating cost.

> [!question]- mkt-val-194 | What is the primary valuation multiple used to value commercial banks?
> Price-to-Tangible Book Value (P/TBV), benchmarked directly against Return on Tangible Common Equity (ROTCE).

> [!question]- mkt-val-195 | What is the mathematical relationship between a bank's P/TBV and ROTCE?
> P/TBV = (ROTCE - g) / (Ke - g); a bank justifies trading above tangible book value if and only if ROTCE exceeds its cost of equity.

> [!question]- mkt-val-196 | How do regulatory capital ratios (such as CET1) constrain bank dividend payments in a DDM?
> Allowable dividends equal Net Income minus the capital required to fund Risk-Weighted Asset growth at the target CET1 ratio.

> [!question]- mkt-val-197 | What is Net Interest Margin (NIM) for a commercial bank?
> NIM = (Interest Income - Interest Expense) / Total Average Earning Assets.

> [!question]- mkt-val-198 | What is an insurance company's combined ratio?
> Combined Ratio = (Incurred Losses + Operating Expenses) / Earned Premiums; a ratio below 100% indicates an underwriting profit.

> [!question]- mkt-val-199 | What is insurance float according to Warren Buffett?
> Premiums collected upfront that have not yet been paid out in claims, which the insurer invests until claims are paid.
> Its cost is the underwriting result; Berkshire's 2012 letter: "When such a profit is earned, we enjoy the use of free money - and, better yet, get paid for holding it."

> [!question]- mkt-val-200 | Why do cyclical companies trade at deceptively low P/E multiples at the top of an economic cycle?
> Peak earnings are unsustainably elevated; the market anticipates earnings collapse and prices the stock downward before reported profits drop.

> [!question]- mkt-val-201 | What is the golden rule for investing in commodity and cyclical producers based on P/E multiples?
> A heuristic, not a rule: trailing P/E tends to be high or undefined at the trough and low at the peak, so value cyclicals on normalized mid-cycle earnings rather than on the trailing multiple.

> [!question]- mkt-val-202 | What is mid-cycle earnings normalization?
> Replacing peak or trough financial metrics with full-cycle average commodity prices and operating margins to derive sustainable earning power.

> [!question]- mkt-val-203 | What is SEC PV-10 in the oil and gas sector?
> PV-10 is a non-GAAP measure: the present value of estimated future net cash flows from proved reserves before income taxes, discounted at 10% a year.
> SEC rules (Release 33-8995, effective 1 January 2010) price reserves at the unweighted average first-day-of-the-month price of the prior 12 months; the GAAP standardized measure (ASC 932) is the after-tax version.

> [!question]- mkt-val-204 | What is Customer Lifetime Value (LTV) in software unit economics?
> LTV = (Average Revenue Per User * Gross Margin %) / Annual Churn Rate.

> [!question]- mkt-val-205 | What is Customer Acquisition Cost (CAC)?
> Total sales and marketing expenditures divided by the number of new customers acquired during the period.

> [!question]- mkt-val-206 | What is the target LTV/CAC ratio for a healthy software enterprise?
> There is no law; a widely quoted practitioner benchmark is Skok's (SaaS Metrics 2.0): the best SaaS businesses have LTV/CAC above 3, sometimes as high as 7 or 8.

> [!question]- mkt-val-207 | What is the CAC Payback Period?
> The number of months required for a customer's gross profit contribution to equal the cost incurred to acquire that customer.

> [!question]- mkt-val-208 | What is Net Revenue Retention (NRR) and why is it critical for SaaS valuation?
> The percentage of recurring revenue retained from existing customers over one year, including expansions and subtracting churn; NRR > 100% indicates compounding organic cohorts.

> [!question]- mkt-val-209 | What is the Rule of 40 in high-growth software valuation?
> A practitioner benchmark (Feld 2015): revenue growth rate (%) plus profit margin (%) should add up to at least 40% for a SaaS company at scale; Feld uses EBITDA margin, many analysts use free cash flow margin.

> [!question]- mkt-val-210 | What is risk-adjusted Net Present Value (rNPV) in biotechnology valuation?
> Discounted cash flow valuation where future commercial revenues are weighted by the cumulative statistical probability of passing clinical trial phases.

> [!question]- mkt-val-211 | What is the historical average probability of a drug candidate passing from Phase I trials to FDA approval?
> 7.9% across all indications for 2011-2020 (BIO, Informa and QLS 2021), the product of the 52.0%, 28.9%, 57.8% and 90.6% phase transition rates.

> [!question]- mkt-val-212 | What is the historical probability of a drug candidate passing from Phase III to FDA approval?
> 52.4% for 2011-2020 (BIO, Informa and QLS 2021): 57.8% from Phase III to NDA/BLA times 90.6% from filing to approval.

> [!question]- mkt-val-213 | How does a binary Phase III trial outcome affect a single-drug biotech firm's valuation?
> Success raises the probability of approval from the Phase III level (52.4% on the BIO 2011-2020 average) to the filing level (90.6%), so the value of the asset jumps; failure removes most of the asset's value, and for a single-asset company most of the equity value, leaving mainly cash.

> [!question]- mkt-val-214 | What is the difference between proved reserves (1P) and proved plus probable reserves (2P) in oil and gas reporting?
> Under SPE-PRMS (2018), when probabilistic methods are used there should be at least a 90% probability (P90) that recovered quantities equal or exceed the proved estimate, and at least 50% that they equal or exceed the 2P estimate.
> Mining codes such as JORC classify reserves by confidence category rather than these probabilities.

> [!question]- mkt-val-215 | Why does the EV/Sales multiple fail to capture unit economics efficiency in tech?
> Two companies trading at 10x sales can have drastically different margins, churn rates, and capital requirements, obscuring true cash generation.

> [!question]- mkt-val-216 | What is the efficiency ratio in banking?
> Non-Interest Operating Expenses divided by Total Net Revenue; a lower ratio means less cost per dollar of revenue.

> [!question]- mkt-val-217 | How does an inverted yield curve affect commercial bank profitability?
> It tends to compress Net Interest Margin for banks that fund at short-term rates and lend at long-term rates, though the effect depends on deposit pricing, hedging and asset repricing.

> [!question]- mkt-val-218 | What is embedded value (EV) in life insurance valuation?
> The present value of future profits from existing in-force policies plus adjusted net asset value, omitting speculative future new business.

> [!question]- mkt-val-219 | What is all-in sustaining cost (AISC) in precious metals mining?
> A non-GAAP metric defined by World Gold Council guidance (2013, updated 2018) that adds to on-site costs (net of by-product credits) corporate G&A, reclamation accretion, sustaining exploration and sustaining capital expenditure.

> [!question]- mkt-val-220 | How should pre-revenue clinical trial costs be treated in a biotech valuation?
> Discounted as negative cash outflows in the explicit forecast period, unweighted by clinical risk since costs are incurred with certainty.

> [!question]- mkt-val-221 | Why is tangible common equity more relevant than total book value for banks?
> The Basel Framework requires goodwill and all other intangibles (except mortgage servicing rights) to be deducted from CET1 (CAP30.7), so tangible common equity is closer to the capital that constrains the balance sheet.

> [!question]- mkt-val-222 | What is magic formula earnings yield as defined by Joel Greenblatt?
> EBIT divided by Enterprise Value (EBIT / EV), used in The Little Book That Beats the Market (2005) alongside return on capital, EBIT / (net working capital + net fixed assets), so firms with different leverage can be compared.

> [!question]- mkt-val-223 | How does operating leverage amplify earnings volatility in cyclical companies?
> High fixed manufacturing costs mean small percentage changes in sales volume produce massive percentage swings in operating income.

> [!question]- mkt-val-224 | What is the ultimate principle for selecting a valuation methodology?
> Match the valuation tool to the economic reality of the business model: asset-based for distress, multiples for relative pricing, and DCF/rNPV for cash flow generation.

> [!question]- mkt-val-264 | Using the BIO 2011-2020 averages, what is the probability that a drug entering Phase II is eventually approved?
> 28.9% x 57.8% x 90.6% = 15.1%, about twice the 7.9% from Phase I and well under a third of the 52.4% from Phase III.

> [!question]- mkt-val-265 | Vulcan Mining's mid-cycle case assumes 2% growth with a 25% reinvestment rate and a 9% WACC. Does that growth add value?
> No: RONIC = g / RR = 2% / 25% = 8%, below the 9% WACC.
> With zero growth and no net reinvestment EV is 487.5 / 0.09 = 5,416.7 against 5,223.2 with growth, so growth costs $0.97 per share.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_val_07_specialized.py`](../../code/mkt_val_07_specialized.py) prints and asserts every number on this page: justified P/TBV against a clean-surplus simulation, the BIO cumulative approval probabilities by exact products and a seeded simulation of 2,000,000 candidates, and the Vulcan mid-cycle value against a steady-state reinvestment simulation, with the growth effect isolated by changing g alone.
- Related notes: [Relative Valuation and Multiples Done Right](04-Relative-Valuation-Multiples-Done-Right.md), [Basel capital ratios in the regulatory capital section](../../../17-Regulatory-Capital-Basel-and-FRTB/README.md).

## Further reading

- Basel Committee on Banking Supervision. *The Basel Framework*: RBC20.1 (minimum CET1 of 4.5%), RBC30.2 (capital conservation buffer of 2.5%), CAP30.7 (deduction of goodwill and other intangibles). bis.org/basel_framework.
- BIO, Informa Pharma Intelligence, & QLS Advisors (2021). *Clinical Development Success Rates 2011-2020*.
- Berkshire Hathaway. Chairman's letter to shareholders, 2012. berkshirehathaway.com/letters.
- Damodaran, A. (2009). *Valuing Financial Service Firms*. NYU Stern School of Business Working Paper.
- Damodaran, A. (2012). *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset* (3rd ed.). John Wiley & Sons. Ch. 21 (financial service firms), Ch. 22 (negative or abnormal earnings), Ch. 23 (young and start-up firms).
- Feld, B. (2015, February 3). The Rule of 40% for a healthy SaaS company. *Feld Thoughts*.
- Greenblatt, J. (2005). *The Little Book That Beats the Market*. John Wiley & Sons.
- Koller, T., Goedhart, M., & Wessels, D. (2020). *Valuation: Measuring and Managing the Value of Companies* (7th ed.). John Wiley & Sons. Ch. 37 (cyclical companies), Ch. 38 (banks).
- Skok, D. SaaS Metrics 2.0: A guide to measuring and improving what matters. *For Entrepreneurs* (forentrepreneurs.com).
- Society of Petroleum Engineers (2018). *Petroleum Resources Management System* (PRMS).
- US Securities and Exchange Commission (2008). *Modernization of Oil and Gas Reporting*, Release No. 33-8995.
- World Gold Council (2013, updated 2018). Guidance note on non-GAAP metrics: all-in sustaining costs and all-in costs.
