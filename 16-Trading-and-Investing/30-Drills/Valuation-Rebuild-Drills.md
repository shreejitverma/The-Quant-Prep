---
type: guide
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Damodaran (2012) - Investment Valuation, Koller Goedhart and Wessels (2020) - Valuation: Measuring and Managing the Value of Companies, Mauboussin and Rappaport (2016) - Expectations Investing]
---

# Valuation Rebuild Drills

## Overview

The Valuation Rebuild Drills bank provides rigorous mathematical exercises designed to build proficiency in corporate valuation modeling.
Each drill presents financial inputs from real-world corporate situations.
Calculate the intermediate metrics, build the valuation bridge, and derive the intrinsic value or implied market expectation before checking the hidden solution.

---

## Drill 1: The Complete FCFF Valuation Bridge

### Scenario
Company Alpha is an enterprise software provider generating recurring software revenue.
The company's trailing twelve months (TTM) financials and five-year projection assumptions are as follows (all currency in millions):

```
+-----------------------------------------------------------------------+
| Input Variable                                           | Value      |
|----------------------------------------------------------+------------|
| TTM Revenue                                              | $1,000.0   |
| Projected Annual Revenue Growth (Years 1 to 5)          | 12.0%      |
| Target Operating Margin (EBIT / Revenue)                | 25.0%      |
| Effective Corporate Tax Rate                             | 21.0%      |
| Net Working Capital (% of Revenue)                       | 10.0%      |
| Annual Capital Expenditures                              | $50.0      |
| Annual Depreciation & Amortization                       | $40.0      |
| Weighted Average Cost of Capital (WACC)                  | 8.5%       |
| Terminal Value Perpetuity Growth Rate (g)                | 2.5%       |
| Total Cash and Marketable Securities                     | $150.0     |
| Total Debt (Book and Fair Value)                         | $300.0     |
| Diluted Shares Outstanding                               | 50.0M      |
+-----------------------------------------------------------------------+
```

Assume Net Working Capital begins at $100.0 million in Year 0 (10% of $1,000.0M) and scales with projected revenue.
Capex and Depreciation grow at 5% annually from their Year 1 base of $50M and $40M respectively.

### Questions to Solve
1. Project Year 1 through Year 5 Revenue, EBIT, NOPAT, and Change in Working Capital.
2. Calculate Unlevered Free Cash Flow to Firm (FCFF) for Years 1 through 5.
3. Compute the Present Value of discrete FCFF discounted at WACC = 8.5% (use end-of-year discounting).
4. Calculate the Terminal Value at Year 5 using the Gordon Growth Model and discount it to Year 0.
5. Reconcile Enterprise Value to Equity Value and calculate the intrinsic value per share.

<details>
<summary>Reveal Valuation Solution & Bridge</summary>

#### Step 1: Projection Schedule (Years 1 to 5)

$$\text{Revenue}_t = \text{Revenue}_{t-1} \times 1.12$$
$$\text{EBIT}_t = \text{Revenue}_t \times 0.25$$
$$\text{NOPAT}_t = \text{EBIT}_t \times (1 - 0.21) = \text{EBIT}_t \times 0.79$$
$$\text{NWC}_t = \text{Revenue}_t \times 0.10 \implies \Delta \text{NWC}_t = \text{NWC}_t - \text{NWC}_{t-1}$$

```
+-----------------------------------------------------------------------+
| Line Item ($M)    | Year 1   | Year 2   | Year 3   | Year 4   | Year 5|
|-------------------+----------+----------+----------+----------+-------|
| Revenue           | $1,120.0 | $1,254.4 | $1,404.9 | $1,573.5 | $1,762.3
| EBIT (25.0%)      | $280.0   | $313.6   | $351.2   | $393.4   | $440.6|
| NOPAT (79.0%)     | $221.2   | $247.7   | $277.5   | $310.8   | $348.1|
| + Depreciation    | $40.0    | $42.0    | $44.1    | $46.3    | $48.6 |
| - Capex           | $50.0    | $52.5    | $55.1    | $57.9    | $60.8 |
| - Change in NWC   | $12.0    | $13.4    | $15.1    | $16.9    | $18.9 |
| FCFF              | $199.2   | $223.8   | $251.4   | $282.3   | $317.0|
+-----------------------------------------------------------------------+
```

#### Step 2: Discounting Discrete Cash Flows (WACC = 8.5%)
$$\text{Discount Factor}_t = \frac{1}{(1.085)^t}$$

- Year 1: $199.2 / 1.085^1 = \$183.60 \text{ million}$
- Year 2: $223.8 / 1.085^2 = \$189.98 \text{ million}$
- Year 3: $251.4 / 1.085^3 = \$196.87 \text{ million}$
- Year 4: $282.3 / 1.085^4 = \$203.71 \text{ million}$
- Year 5: $317.0 / 1.085^5 = \$210.82 \text{ million}$

$$\text{PV of Discrete FCFF} = 183.60 + 189.98 + 196.87 + 203.71 + 210.82 = \$984.98 \text{ million}$$

#### Step 3: Terminal Value Calculation
$$\text{Terminal FCFF}_{\text{Year 6}} = \text{FCFF}_5 \times (1 + g) = 317.0 \times 1.025 = \$324.93 \text{ million}$$

$$\text{Terminal Value}_5 = \frac{\text{Terminal FCFF}_6}{\text{WACC} - g} = \frac{324.93}{0.085 - 0.025} = \frac{324.93}{0.060} = \$5,415.50 \text{ million}$$

$$\text{PV of Terminal Value} = \frac{5,415.50}{(1.085)^5} = \frac{5,415.50}{1.50366} = \$3,601.55 \text{ million}$$

#### Step 4: Enterprise Value to Equity Value Bridge
$$\text{Enterprise Value (EV)} = \text{PV of Discrete Cash Flows} + \text{PV of Terminal Value}$$
$$\text{EV} = 984.98 + 3,601.55 = \$4,586.53 \text{ million}$$

$$\text{Equity Value} = \text{EV} + \text{Cash} - \text{Debt}$$
$$\text{Equity Value} = 4,586.53 + 150.0 - 300.0 = \$4,436.53 \text{ million}$$

$$\text{Intrinsic Value per Share} = \frac{\$4,436.53 \text{ million}}{50.0 \text{ million shares}} = \$88.73 \text{ per share}$$

</details>

---

## Drill 2: Hamada Equation and WACC Parameter Rebuild

### Scenario
An analyst is calculating the Weighted Average Cost of Capital (WACC) for a private medical device company (Company Beta).
Company Beta has a capital structure with $40% debt and 60% equity ($D/E = 0.667$).
Its corporate marginal tax rate is 25%.
The yield on 10-year US Treasuries (risk-free rate $R_f$) is 4.0%, and the market risk premium (ERP) is 5.5%.
Company Beta can borrow long-term debt at an interest rate of 6.5%.
Three publicly traded peer companies exhibit the following parameters:

```
+-----------------------------------------------------------------------+
| Peer Company      | Equity Beta (Beta_L) | Debt-to-Equity (D/E) | Tax Rate |
|-------------------+----------------------+----------------------+----------|
| MedTech A         | 1.35                 | 0.50                 | 25.0%    |
| MedTech B         | 1.10                 | 0.20                 | 25.0%    |
| MedTech C         | 1.55                 | 0.80                 | 25.0%    |
+-----------------------------------------------------------------------+
```

### Questions to Solve
1. Un-lever the equity betas of all three peers using the Hamada equation:
   $$\beta_U = \frac{\beta_L}{1 + (1 - T)(D/E)}$$
2. Compute the industry average unlevered asset beta ($\beta_U$).
3. Re-lever the industry asset beta to Company Beta's target capital structure ($D/E = 0.667$).
4. Compute Company Beta's Cost of Equity ($K_e$) using the CAPM.
5. Calculate Company Beta's Cost of Debt after tax ($K_d(1-T)$) and final WACC.

<details>
<summary>Reveal WACC Rebuild & Solution</summary>

#### Step 1: Un-levering Peer Betas
$$\text{MedTech A}: \beta_U = \frac{1.35}{1 + (1 - 0.25)(0.50)} = \frac{1.35}{1 + 0.375} = \frac{1.35}{1.375} = 0.9818$$

$$\text{MedTech B}: \beta_U = \frac{1.10}{1 + (1 - 0.25)(0.20)} = \frac{1.10}{1 + 0.150} = \frac{1.10}{1.150} = 0.9565$$

$$\text{MedTech C}: \beta_U = \frac{1.55}{1 + (1 - 0.25)(0.80)} = \frac{1.55}{1 + 0.600} = \frac{1.55}{1.600} = 0.9688$$

#### Step 2: Average Unlevered Beta
$$\bar{\beta}_U = \frac{0.9818 + 0.9565 + 0.9688}{3} = \frac{2.9071}{3} = 0.9690$$

#### Step 3: Re-levering to Target Capital Structure
Company Beta has $D/E = 0.667$ and tax rate $T = 25\%$:
$$\beta_{L, \text{target}} = \bar{\beta}_U \times [1 + (1 - T)(D/E)]$$
$$\beta_{L, \text{target}} = 0.9690 \times [1 + (1 - 0.25)(0.667)] = 0.9690 \times [1 + 0.500] = 0.9690 \times 1.50 = 1.4535$$

#### Step 4: Cost of Equity Calculation (CAPM)
$$K_e = R_f + \beta_L \times \text{ERP}$$
$$K_e = 4.0\% + 1.4535 \times 5.5\% = 4.0\% + 7.994\% = 11.994\% \approx 12.00\%$$

#### Step 5: After-Tax Cost of Debt and WACC
$$\text{After-Tax Cost of Debt} = K_d \times (1 - T) = 6.5\% \times (1 - 0.25) = 4.875\%$$

With Capital Weights: Equity = 60%, Debt = 40%:
$$\text{WACC} = \left(\frac{E}{V}\right) K_e + \left(\frac{D}{V}\right) K_d (1 - T)$$
$$\text{WACC} = (0.60 \times 11.994\%) + (0.40 \times 4.875\%)$$
$$\text{WACC} = 7.196\% + 1.950\% = 9.146\% \approx 9.15\%$$

</details>

---

## Drill 3: Reverse DCF Expectations Inversion

### Scenario
Company Gamma trades at a stock price of $120.00 with 100 million shares outstanding (Market Cap = $12.0 billion).
The balance sheet holds $500 million in cash and $1.5 billion in debt (Enterprise Value = $13.0 billion).
Base year trailing revenue is $2.0 billion.
An analyst assumes:
- Target steady-state operating margin: 20.0%
- Effective tax rate: 21.0%
- Net investment rate (Capex + $\Delta$NWC - D&A) as a fraction of revenue: 4.0%
- WACC: 9.0%
- Terminal value growth rate post Year 10: 3.0%

### Questions to Solve
1. Derive the Free Cash Flow margin as a percentage of revenue:
   $$\text{FCF Margin} = \text{Operating Margin} \times (1 - T) - \text{Net Investment Rate}$$
2. Formulate the relationship between Enterprise Value and revenue growth rate.
3. Solve for the 10-year compound annual revenue growth rate ($g_{\text{rev}}$) implied by the current market enterprise value of $13.0 billion.

<details>
<summary>Reveal Reverse DCF Solution</summary>

#### Step 1: Free Cash Flow Margin
$$\text{NOPAT Margin} = 20.0\% \times (1 - 0.21) = 15.80\%$$
$$\text{FCF Margin} = 15.80\% - 4.0\% = 11.80\% \text{ of Revenue}$$

#### Step 2: Expectations Inversion Framework
Let $g$ be the constant annual revenue growth rate for the next 10 years.
Annual Free Cash Flow is:
$$\text{FCF}_t = \text{Revenue}_0 \times (1 + g)^t \times 0.1180$$

At Year 10, Terminal Value is:
$$\text{TV}_{10} = \frac{\text{FCF}_{10} \times (1 + 0.03)}{0.09 - 0.03} = \frac{\text{FCF}_{10} \times 1.03}{0.06} \approx 17.167 \times \text{FCF}_{10}$$

Enterprise Value equals the sum of discounted cash flows over Years 1-10 plus discounted Terminal Value:
$$\text{EV} = \sum_{t=1}^{10} \frac{\text{FCF}_t}{(1.09)^t} + \frac{\text{TV}_{10}}{(1.09)^{10}} = \$13,000 \text{ million}$$

#### Step 3: Numerical Solution for Implied Growth Rate
- At $g = 10.0\%$:
  - Year 10 Revenue: $2,000 \times (1.10)^{10} = \$5,187 \text{M}$
  - Year 10 FCF: $5,187 \times 0.1180 = \$612.1 \text{M}$
  - $\text{TV}_{10} = 612.1 \times 17.167 = \$10,508 \text{M}$
  - PV of TV: $10,508 / (1.09)^{10} = 10,508 / 2.3674 = \$4,439 \text{M}$
  - PV of 10-yr cash flows: $\approx \$1,870 \text{M}$
  - Total EV $\approx \$6,309 \text{M}$ (Much too low; market is pricing significantly higher growth).

- At $g = 18.25\%$:
  - Year 10 Revenue: $2,000 \times (1.1825)^{10} = 2,000 \times 5.346 = \$10,692 \text{M}$
  - Year 10 FCF: $10,692 \times 0.1180 = \$1,261.7 \text{M}$
  - $\text{TV}_{10} = 1,261.7 \times 17.167 = \$21,659 \text{M}$
  - PV of TV: $21,659 / 2.3674 = \$9,149 \text{M}$
  - PV of 10-yr cash flows: $\approx \$3,851 \text{M}$
  - Total EV = $9,149 + 3,851 = \$13,000 \text{M}$

#### Conclusion:
The current market price of $120.00 implies that Company Gamma must grow revenues at an aggressive 18.25% CAGR for an entire decade while sustaining high 20% operating margins.
If the underlying addressable market cannot support a 5.3x expansion in company revenue, the stock is overvalued.

</details>

---

## Drill 4: Net-Net Liquidation (NCAV) Asset Haircut Audit

### Scenario
Company Delta is a micro-cap industrial manufacturer undergoing operational distress.
Its common shares trade at $6.00 with 10.0 million shares outstanding (Market Cap = $60.0 million).
The most recent balance sheet reports the following book values (figures in millions):

```
+-----------------------------------------------------------------------+
| Balance Sheet Item                       | Book Value | Graham Haircut|
|------------------------------------------+------------+---------------|
| Cash and Short-Term Investments          | $25.0      | 0% (100% val) |
| Accounts Receivable                      | $30.0      | 25% (75% val) |
| Raw Materials and Work-in-Process Inv    | $20.0      | 60% (40% val) |
| Finished Goods Inventory                 | $20.0      | 30% (70% val) |
| Property, Plant & Equipment (PP&E)       | $60.0      | 100% (0% val) |
| Goodwill and Intangibles                 | $15.0      | 100% (0% val) |
| Total Assets                             | $170.0     | -             |
| Accounts Payable & Accrued Liabilities   | $22.0      | 0% (100% liab)|
| Short-Term and Long-Term Bank Debt       | $18.0      | 0% (100% liab)|
| Underfunded Pension Obligations          | $10.0      | 0% (100% liab)|
| Off-Balance Sheet Operating Leases PV    | $12.0      | 0% (100% liab)|
| Total Liabilities & Obligations          | $62.0      | -             |
+-----------------------------------------------------------------------+
```

### Questions to Solve
1. Calculate Benjamin Graham's Net Current Asset Value (NCAV):
   $$\text{NCAV} = \text{Current Assets} - \text{Total Liabilities and Off-Balance Sheet Claims}$$
2. Calculate the Liquidation Value using the conservative asset haircut percentages.
3. Compare the current market price ($6.00) against NCAV per share and Liquidation Value per share.
4. Assess whether Company Delta provides an adequate margin of safety.

<details>
<summary>Reveal Net-Net Liquidation Solution</summary>

#### Step 1: Standard Graham NCAV Calculation
$$\text{Total Current Assets} = 25.0 (\text{cash}) + 30.0 (\text{AR}) + 40.0 (\text{inventory}) = \$95.0 \text{ million}$$
$$\text{Total Liabilities & Off-Balance Claims} = 22.0 + 18.0 + 10.0 + 12.0 = \$62.0 \text{ million}$$

$$\text{NCAV} = 95.0 - 62.0 = \$33.0 \text{ million}$$
$$\text{NCAV per Share} = \frac{\$33.0 \text{ million}}{10.0 \text{ million shares}} = \$3.30 \text{ per share}$$

#### Step 2: Conservative Liquidation Value
Applying conservative realization haircuts:
- Cash: $25.0 \times 1.00 = \$25.0 \text{ million}$
- Accounts Receivable: $30.0 \times 0.75 = \$22.5 \text{ million}$
- Raw Materials/WIP: $20.0 \times 0.40 = \$8.0 \text{ million}$
- Finished Goods: $20.0 \times 0.70 = \$14.0 \text{ million}$
- PP&E: $60.0 \times 0.00 = \$0.0 \text{ million}$
- Intangibles: $15.0 \times 0.00 = \$0.0 \text{ million}$

$$\text{Total Liquidated Assets} = 25.0 + 22.5 + 8.0 + 14.0 = \$69.5 \text{ million}$$
$$\text{Less Total Liabilities} = \$62.0 \text{ million}$$

$$\text{Net Liquidation Value} = 69.5 - 62.0 = \$7.5 \text{ million}$$
$$\text{Net Liquidation Value per Share} = \frac{\$7.5 \text{ million}}{10.0 \text{ million shares}} = \$0.75 \text{ per share}$$

#### Step 3: Margin of Safety Evaluation
- Current Stock Price: $6.00
- NCAV per share: $3.30 (Stock trades at a 81.8% premium to NCAV)
- Conservative Liquidation Value per share: $0.75 (Stock trades at an 8x premium to liquidation value)

#### Conclusion:
Company Delta fails Benjamin Graham's Net-Net rule completely.
Graham required buying at less than two-thirds of NCAV ($P \le \frac{2}{3} \text{NCAV} = \$2.20$).
At $6.00, investors are relying on an ongoing business turnaround.
If the company burns cash while attempting to liquidate, equity will be wiped out by debt and pension claims.

</details>
