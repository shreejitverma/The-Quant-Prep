---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Damodaran (2012) - Investment Valuation: Tools and Techniques for Determining the Value of Any Asset, Fernandez (2015) - CAPM: An Absurd Model, Hamada (1972) - The Effect of the Firm's Capital Structure on the Systematic Risk of Common Stocks, Koller Goedhart and Wessels (2020) - Valuation: Measuring and Managing the Value of Companies (McKinsey), Pratt and Grabowski (2014) - Cost of Capital: Applications and Examples]
---

# Cost of Capital, WACC, and Terminal Value Traps

## TL;DR

- The Weighted Average Cost of Capital (WACC) represents the blended opportunity cost of capital demanded by all providers of corporate funding, weighted by their market values.
- Cost of Equity ($K_e$) derived from the Capital Asset Pricing Model (CAPM) depends critically on bottom-up unlevered betas rather than noisy single-stock regression betas.
- Terminal value is often the largest part of DCF enterprise value (78.2% in the DCF note's worked case), and the Zero-Reinvestment Fallacy inflates it: assuming perpetual growth without modeling the required reinvestment rate ($g / \text{RONIC}$).
- Perpetual terminal growth ($g$) cannot exceed the long-term nominal growth rate of the economy whose currency the cash flows are in, or the firm eventually outgrows that economy.
- Over-optimistic assumptions regarding terminal ROIC persistence ignore competitive mean reversion, leading to severe intrinsic overvaluation.

## Learning objectives

- Formulate, compute, and interpret the Weighted Average Cost of Capital (WACC) using market value weights.
- Calculate bottom-up asset betas and apply Hamada's equation to re-lever beta for target capital structures.
- Estimate implied forward-looking Equity Risk Premiums (ERP) and assess Country Risk Premiums (CRP).
- Quantify synthetic cost of debt based on credit ratings and interest coverage ratios.
- Avoid the five classic Terminal Value Traps: the GDP growth ceiling, zero-reinvestment fallacy, infinite ROIC assumption, WACC spread sensitivity, and negative terminal cash flow.
- Formulate the Value Driver formula linking terminal value directly to Return on New Invested Capital (RONIC).

## Core concepts

### 1. The Weighted Average Cost of Capital (WACC)

WACC is the minimum return an enterprise must earn on its existing asset base to satisfy debt holders, preferred stockholders, and common equity investors:

$$\text{WACC} = \left( \frac{E}{V} \right) K_e + \left( \frac{D}{V} \right) K_d (1 - t) + \left( \frac{P}{V} \right) K_p$$

Where:
- $E, D, P$: Market values of Equity, Debt, and Preferred Stock.
- $V = E + D + P$: Total Enterprise Market Value.
- $K_e$: Cost of Equity.
- $K_d$: Pre-tax Cost of Debt.
- $t$: Marginal corporate tax rate (creating the interest tax shield).
- $K_p$: Cost of Preferred Stock.

```
+-----------------------------------------------------------------------+
|                       WACC CAPITAL PROPORTIONS                        |
+-----------------------------------------------------------------------+
| MARKET VALUE OF EQUITY (E)           MARKET VALUE OF DEBT (D)         |
| Current Share Price x Diluted Shares  Traded Bond Value or PV of debt  |
| (Never use Book Value of Equity)      (Adjust for below-market coupon) |
+--------------------------------------+--------------------------------+
                                       |
                   Tax Shield: Interest is Tax Deductible
                   After-Tax Cost of Debt = Kd x (1 - t)
```

### 2. The Cost of Equity ($K_e$) and CAPM Anatomy

Under the standard Capital Asset Pricing Model (CAPM):

$$K_e = R_f + \beta_L \times \text{ERP} + \text{CRP}$$

Where:
- $R_f$: Risk-Free Rate, proxied by the 10-year or 30-year government sovereign bond yield in the currency of valuation.
- $\beta_L$: Levered Equity Beta, measuring the systematic non-diversifiable risk of the company relative to the market.
- $\text{ERP}$: Equity Risk Premium ($E[R_m] - R_f$), the incremental return demanded by investors for holding broad equities.
- $\text{CRP}$: Country Risk Premium, incorporated when operating cash flows originate in emerging or politically volatile jurisdictions.

#### Bottom-Up Beta vs Regression Beta
Single-stock regression betas (plotting stock returns against an index over 36 or 60 months) carry large standard errors.
For a hypothetical stock with true beta 1.0, 30% annual idiosyncratic volatility and a market with 15% annual volatility, the standard error of a 60-month beta is $(\sigma_e / \sigma_m) / \sqrt{n - 3} = 2 / \sqrt{57} = 0.26$, so the 95% interval is about $\pm 0.52$.
Damodaran (2012, Ch. 8) therefore prefers **bottom-up unlevered betas**:

1. Identify a peer group of publicly traded comparable companies in the same business sector.
2. Unlever each peer's regression beta using Hamada's (1972) equation, which assumes debt carries no market risk:
   $$\beta_U = \frac{\beta_L}{1 + (1 - t) \times (D/E)}$$
3. Take the median unlevered beta across the peer group to isolate pure business operational risk.
4. Re-lever the median beta using the target company's specific capital structure and marginal tax rate:
   $$\beta_{L, \text{target}} = \beta_{U, \text{peer}} \times \left[ 1 + (1 - t) \times \left( \frac{D}{E} \right)_{\text{target}} \right]$$

### 3. Estimating the Cost of Debt ($K_d$)

Cost of debt is not historical interest expense divided by total book debt.
It must reflect the marginal borrowing cost the company would incur if it issued new debt today:

1. **Option A: Traded Yield to Maturity (YTM)**:
   For companies with liquidly traded corporate bonds, $K_d$ is the market YTM on the company's long-term bonds.
2. **Option B: Synthetic Credit Rating Approach (Damodaran)**:
   For unrated firms or companies with complex private debt, compute the Interest Coverage Ratio:
   $$\text{Interest Coverage Ratio} = \frac{\text{Operating Income (EBIT)}}{\text{Interest Expense}}$$
   Map the coverage ratio to an estimated credit rating (e.g. AAA, BBB, B-) and add the corresponding default spread to the risk-free rate.
   Damodaran publishes the mapping on his ratings page and updates it each January; the table dated January 2026 for large non-financial firms maps coverage of 6.5x to 8.5x to Aa2/AA with a 0.55% default spread:
   $$K_d = R_f + \text{Default Spread}_{\text{Rating}}$$

### 4. The Five Fatal Terminal Value Traps

Terminal value was 78.2% of enterprise value in the DCF note's worked case.
Small errors in terminal assumptions therefore move the whole valuation:

```
+-----------------------------------------------------------------------+
|                    THE 5 TERMINAL VALUE DISASTERS                     |
+-----------------------------------------------------------------------+
| 1. The GDP Growth Ceiling Trap:                                       |
|    - Setting perpetual growth g > nominal GDP growth.                 |
|    - Mathematically implies the company swallows the entire economy.  |
| 2. The Zero-Reinvestment Fallacy:                                     |
|    - Assuming g > 0% while setting Capex = D&A and Delta OWC = 0.     |
|    - Violates physics: growth requires capital investment!            |
| 3. The Infinite ROIC Trap:                                            |
|    - Assuming perpetual ROIC of 30%+ in perpetuity.                  |
|    - Ignores competitive entry, margin decay, and asset obsolescence. |
| 4. The Spread Sensitivity Trap:                                       |
|    - A fragile (WACC - g) denominator: in the case below, a 50 bp     |
|      error in the spread moves TV by +10.7% or -8.8%.                 |
| 5. Negative Terminal Cash Flow Trap:                                  |
|    - Applying Gordon Growth to high-growth firms still burning cash   |
|      in Year 5, producing meaningless negative terminal values.       |
+-----------------------------------------------------------------------+
```

### 5. The Key Value Driver Formula: Linking Reinvestment to ROIC

The Gordon Growth Model assumes cash flow grows at $g$ forever.
Koller, Goedhart, and Wessels (2020, chapter 14) derive the value driver formula from the steady-state identity $g = \text{RONIC} \times \text{RR}$, so the reinvestment needed for growth is set by the return on new capital:

$$\text{Reinvestment Rate (RR)} = \frac{g}{\text{RONIC}}$$

Where:
- $\text{RONIC}$ is the Return on New Invested Capital earned on incremental investments.

Substituting into the perpetuity formula yields the **Key Value Driver Formula**:

$$\text{Terminal Value}_N = \frac{\text{NOPAT}_{N+1} \times \left( 1 - \frac{g}{\text{RONIC}} \right)}{\text{WACC} - g}$$

This equation reveals the three structural economic regimes of terminal value:

| Regime | Condition | Economic Consequence |
|---|---|---|
| **Value Accretive** | $\text{RONIC} > \text{WACC}$ | Higher growth ($g$) increases terminal value; reinvestment creates wealth. |
| **Value Neutral** | $\text{RONIC} = \text{WACC}$ | Growth ($g$) has zero impact on value; the formula simplifies to $\frac{\text{NOPAT}_{N+1}}{\text{WACC}}$, exactly equal to a zero-growth perpetuity. |
| **Value Destructive** | $\text{RONIC} < \text{WACC}$ | Higher growth ($g$) decreases terminal value; expanding the capital base destroys shareholder value. |

## Worked numerical case study

Analyze Global Logistics Corp (a hypothetical company; every input below is hypothetical, including the 5.0% ERP and the rating table in Step 3):
- 10-Year Treasury Yield ($R_f$): 4.0%
- Mature Market Equity Risk Premium ($\text{ERP}$): 5.0% (hypothetical; Damodaran's implied ERP for the S&P 500 was 4.33% at the start of January 2025 and 4.23% at the start of January 2026, per his histimpl dataset dated January 2026)
- Peer Group Unlevered Beta ($\beta_U$): 0.80
- Target Capital Structure: 30% Debt, 70% Equity ($D/E = 0.30 / 0.70 = 0.4286$)
- Marginal Tax Rate ($t$): 25.0%
- Operating Income (EBIT): $200M
- Annual Interest Expense: $25M
- Forecast Year 5 NOPAT: $180.0M
- Terminal Growth Rate ($g$): 2.5%

### Step 1: Re-Lever Beta for Target Capital Structure
$$\beta_L = \beta_U \times [1 + (1 - t) \times (D/E)] = 0.80 \times [1 + (1 - 0.25) \times 0.4286]$$
$$\beta_L = 0.80 \times [1 + 0.75 \times 0.4286] = 0.80 \times [1 + 0.3214] = 0.80 \times 1.3214 = 1.057$$
The exact value is $37/35 = 1.05714$; unlevering it with the same formula returns the peer beta of 0.80.

### Step 2: Compute Cost of Equity ($K_e$)
$$K_e = R_f + \beta_L \times \text{ERP} = 4.0\% + 1.05714 \times 5.0\% = 4.0\% + 5.2857\% = 9.2857\%$$

### Step 3: Compute Cost of Debt ($K_d$) via Synthetic Rating
$$\text{Interest Coverage Ratio} = \frac{\text{EBIT}}{\text{Interest}} = \frac{200}{25} = 8.0\times$$
Hypothetical rating table: coverage of $8.0\times$ maps to Rating = **A**, Default spread = **1.20%**.
$$K_d = R_f + \text{Default Spread} = 4.0\% + 1.20\% = 5.20\%$$
$$\text{After-Tax } K_d = 5.20\% \times (1 - 0.25) = 3.90\%$$

### Step 4: Compute Blended WACC
$$\text{WACC} = (0.70 \times 9.2857\%) + (0.30 \times 3.90\%) = 6.500\% + 1.170\% = 7.67\%$$
With Damodaran's January 2026 mapping instead (Aa2/AA, 0.55% spread), $K_d = 4.55\%$, the after-tax cost is 3.4125% and WACC falls to 7.52%.

### Step 5: Compare Terminal Value under Three Economic RONIC Scenarios
Year 6 NOPAT = $\$180\text{M} \times (1 + 0.025) = \$184.50\text{M}$
Denominator ($\text{WACC} - g$) = $0.0767 - 0.025 = 0.0517$

#### Scenario A: High Competitive Advantage ($\text{RONIC} = 20.0\%$)
$$\text{Reinvestment Rate} = \frac{g}{\text{RONIC}} = \frac{2.5\%}{20.0\%} = 12.5\%$$
$$\text{FCFF}_6 = 184.50 \times (1 - 0.125) = \$161.44\text{M}$$
$$\text{Terminal Value} = \frac{161.44}{0.0517} = \$3,122.6\text{M}$$

#### Scenario B: Competitive Convergence to Cost of Capital ($\text{RONIC} = \text{WACC} = 7.67\%$)
$$\text{Reinvestment Rate} = \frac{2.5\%}{7.67\%} = 32.5945\%$$
$$\text{FCFF}_6 = 184.50 \times (1 - 0.325945) = \$124.363\text{M}$$
$$\text{Terminal Value} = \frac{124.363}{0.0517} = \$2,405.5\text{M}$$
Notice: $\frac{\text{NOPAT}_6}{\text{WACC}} = \frac{184.50}{0.0767} = \$2,405.5\text{M}$ (identical).

#### Scenario C: The Zero-Reinvestment Fallacy (Naive Model assuming 100% conversion)
$$\text{FCFF}_6 = \text{NOPAT}_6 = \$184.50\text{M} \quad (\text{Assumes zero reinvestment required to grow 2.5\%!})$$
$$\text{Terminal Value} = \frac{184.50}{0.0517} = \$3,568.7\text{M}$$

Forensic takeaway:
The naive model overstates terminal value by $\$3,568.7\text{M} - \$2,405.5\text{M} = \$1,163.2\text{M}$ (+48.4%) because it assumes growth appears out of thin air without capital reinvestment.
Zero reinvestment is the limit of an infinite RONIC, which is why the naive value sits above even the 20% RONIC case.

## Practice questions

> [!question]- mkt-val-033 | What is the mathematical definition of Weighted Average Cost of Capital (WACC)?
> WACC = (E/V) * Ke + (D/V) * Kd * (1 - t) + (P/V) * Kp, using market value weights.

> [!question]- mkt-val-034 | Why must market values be used instead of book values when calculating capital structure weights in WACC?
> Because the cost of capital represents the current market rate demanded by investors to buy corporate claims at prevailing market prices.

> [!question]- mkt-val-035 | What is Hamada's equation?
> Beta_L = Beta_U * [1 + (1 - t) * (D/E)], quantifying how financial leverage increases equity beta above operating asset beta.

> [!question]- mkt-val-036 | Why are bottom-up industry betas superior to single-stock regression betas?
> Averaging the betas of many comparable firms reduces estimation error: if the peer errors were independent, the standard error of the average would fall with the square root of the number of peers.
> The method also lets you relever to the target's own capital structure rather than inheriting its historical one (Damodaran 2012, Ch. 8).

> [!question]- mkt-val-037 | What is the Equity Risk Premium (ERP)?
> The incremental expected return demanded by investors above the risk-free rate for holding a diversified portfolio of equities.
> It is an estimate, not a constant: Damodaran's implied ERP for the S&P 500 was 4.23% at the start of January 2026 (histimpl dataset, January 2026).

> [!question]- mkt-val-038 | What is the difference between historical ERP and implied forward-looking ERP?
> Historical ERP calculates realized equity returns over bonds over past decades; implied ERP solves for the internal rate of return equating market prices to future expected cash flows.

> [!question]- mkt-val-039 | What is the synthetic credit rating approach for estimating cost of debt?
> Calculating the interest coverage ratio (EBIT / Interest) to estimate an equivalent credit rating, and adding that rating's default spread to the risk-free rate.

> [!question]- mkt-val-040 | Why is historical interest expense divided by total debt an incorrect measure of Kd?
> It reflects legacy coupon rates on historical debt rather than the marginal market borrowing rate required to issue debt today.

> [!question]- mkt-val-041 | What is the Zero-Reinvestment Fallacy in terminal value modeling?
> Assuming a positive perpetual growth rate while projecting zero working capital investment and setting capex equal to depreciation.

> [!question]- mkt-val-042 | What is the formula for the required reinvestment rate to sustain growth (g) in terminal value?
> Reinvestment Rate = g / RONIC, where RONIC is the Return on New Invested Capital.

> [!question]- mkt-val-043 | What happens to terminal value if a company's terminal RONIC exactly equals its WACC?
> Terminal value becomes completely independent of growth, simplifying exactly to NOPAT / WACC.

> [!question]- mkt-val-044 | What happens to terminal value if terminal RONIC is less than WACC and growth increases?
> Terminal value decreases; each incremental dollar invested destroys economic wealth because it earns less than the cost of funding.

> [!question]- mkt-val-045 | What is the economic ceiling for the perpetual growth rate (g) in a DCF model?
> The long-run nominal growth rate of the economy whose currency the cash flows are in; Damodaran (2012, Ch. 12) uses the risk-free rate as a practical cap.

> [!question]- mkt-val-046 | Why does a small change in (WACC - g) cause violent swings in terminal valuation?
> Because terminal value is inversely proportional to the spread; when WACC is 7% and g is 2.5%, narrowing the 4.5% spread by 100 bp raises value by 28.6% and widening it by 100 bp lowers value by 18.2%.

> [!question]- mkt-val-047 | What is the Country Risk Premium (CRP) and when should it be added to the Cost of Equity?
> An additional risk premium added to Ke when operating assets or revenues reside in emerging or sovereign-risk jurisdictions.

> [!question]- mkt-val-048 | How does Roll's critique challenge the Capital Asset Pricing Model (CAPM)?
> Roll (1977) argued that CAPM's testable content is that the true market portfolio is mean-variance efficient; because that portfolio includes all assets (real estate, human capital and more), it is unobservable, so tests using a stock index proxy cannot confirm or reject CAPM.

> [!question]- mkt-val-049 | What is the Fama-French 3-factor model extension of CAPM?
> Fama and French (1993) add Size (SMB - Small Minus Big) and Value (HML - High Minus Low book-to-market) factors to explain returns beyond market beta alone.

> [!question]- mkt-val-050 | Why should the discount rate reflect the risk of the cash flow rather than the company's historical financing?
> Because an all-equity-funded company acquiring a speculative biotech asset must discount that asset at the biotech hurdle rate, not its corporate WACC.

> [!question]- mkt-val-051 | How should debt covenants impact WACC modeling?
> Tight debt covenants limit borrowing capacity, preventing the firm from achieving an optimal low-cost debt-to-equity weighting.

> [!question]- mkt-val-052 | What is the danger of applying Gordon Growth to high-growth unprofitable companies at Year 5?
> If the firm has not yet reached positive normalized operating cash flow, Gordon Growth yields an absurd negative or mathematically impossible terminal value.

> [!question]- mkt-val-053 | What is the solution when a company is still burning cash in Year 5 of an explicit forecast?
> Extend the explicit forecast period until cash flows stabilize into sustainable positive normalized earnings, and only then apply a terminal value.

> [!question]- mkt-val-054 | How does the interest tax shield affect WACC as leverage increases?
> The tax shield lowers WACC initially, but excessive debt escalates expected financial distress costs, eventually driving WACC upward.

> [!question]- mkt-val-055 | What is the Modigliani-Miller Theorem with corporate taxes?
> Modigliani and Miller (1963): with corporate taxes and no distress costs, the value of a levered firm is the unlevered value plus the present value of the tax shield, which for permanent debt is t x D, so value rises linearly with debt.

> [!question]- mkt-val-056 | What is the Trade-Off Theory of capital structure?
> Optimal capital structure is achieved where the marginal tax benefit of additional debt equals the marginal present value of financial distress costs.

> [!question]- mkt-val-057 | Why does an analyst using a 10-year Treasury rate for Rf need to ensure cash flows are projected in nominal terms?
> Because the 10-year Treasury yield includes embedded inflation expectations; matching nominal rates requires nominal cash flows to prevent mismatch.

> [!question]- mkt-val-058 | If an analyst projects real (inflation-adjusted) cash flows, what risk-free rate must be used?
> The real risk-free rate, derived from Treasury Inflation-Protected Securities (TIPS) yields.

> [!question]- mkt-val-059 | What is the relationship between the terminal exit multiple and the terminal perpetuity growth rate?
> Gordon value divided by final-year NOPAT is (1 + g)(1 - g / RONIC) / (WACC - g), so every exit multiple implies a perpetual growth rate.
> In this note's scenario A the terminal value is 17.35x year-5 NOPAT; a 20x exit at RONIC 20% and WACC 7.67% would imply g = 3.37%.

> [!question]- mkt-val-060 | What is the risk of assuming terminal ROIC exceeds WACC into infinite perpetuity?
> It assumes the company maintains permanent, impenetrable competitive moats that completely resist capitalist economic arbitrage across centuries.

> [!question]- mkt-val-061 | How should short-term debt be treated in the WACC calculation?
> If short-term debt is rolled over continuously to fund ongoing operations, it must be included in Total Debt at market value.

> [!question]- mkt-val-062 | How do convertible bonds impact the WACC capital structure weights?
> Split each convertible into a straight-debt component (its coupons and principal valued at the firm's straight-debt rate) and an equity component (the remainder of its market value), and weight each with the matching cost (Damodaran 2012, Ch. 8).

> [!question]- mkt-val-063 | What is a hurdle rate and how does it relate to WACC?
> A hurdle rate is a managerial cutoff rate for capital allocation, often set conservatively higher than WACC to build in a margin of safety.

> [!question]- mkt-val-064 | What is the ultimate test of terminal value sanity in a discounted cash flow model?
> Ensuring perpetual growth is below nominal GDP, required reinvestment is deducted, and implied terminal ROIC reflects realistic competitive convergence.

> [!question]- mkt-val-259 | In the Global Logistics case, what happens to WACC if you replace the hypothetical A / 1.20% rating with Damodaran's January 2026 mapping for 8.0x coverage?
> That table maps 6.5x to 8.5x to Aa2/AA with a 0.55% spread, so Kd = 4.55% and the after-tax cost is 3.4125%.
> WACC = 0.70 x 9.2857% + 0.30 x 3.4125% = 7.52%, down from 7.67%.

> [!question]- mkt-val-260 | Roughly how precise is a 60-month regression beta for a stock with 30% idiosyncratic and 15% market volatility (annual)?
> The standard error is (0.30 / 0.15) / sqrt(60 - 3) = 0.26, so the 95% interval is about plus or minus 0.52 around the estimate.
> A seeded Monte Carlo of 40,000 regressions gives the same 0.26.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_val_02_wacc.py`](../../code/mkt_val_02_wacc.py) prints and asserts every number on this page: the relevered beta, cost of equity and WACC in exact fractions, each value-driver terminal value against a year-by-year simulation of the reinvestment rule over 3,000 years, the exit-multiple growth rate by bisection against a quadratic, and the beta standard error against a seeded Monte Carlo.
- Related notes: [DCF First Principles and Cash Flow Forecasting](01-DCF-First-Principles-and-Cash-Flow-Forecasting.md), [Relative Valuation and Multiples Done Right](04-Relative-Valuation-Multiples-Done-Right.md).

## Further reading

- Damodaran, A. (2012). *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset* (3rd ed.). John Wiley & Sons. Ch. 7 (riskless rates and risk premiums), Ch. 8 (risk parameters and costs of financing), Ch. 12 (terminal value).
- Damodaran, A. Implied equity risk premiums for the S&P 500 (histimpl dataset, updated January 2026) and ratings, interest coverage ratios and default spreads (ratings page, data as of January 2026). NYU Stern, pages.stern.nyu.edu/~adamodar.
- Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33(1), 3-56.
- Fernandez, P. (2015). CAPM: An absurd model. *Business Valuation Review*, 34(1), 4-23.
- Hamada, R. S. (1972). The effect of the firm's capital structure on the systematic risk of common stocks. *Journal of Finance*, 27(2), 435-452.
- Koller, T., Goedhart, M., & Wessels, D. (2020). *Valuation: Measuring and Managing the Value of Companies* (7th ed.). John Wiley & Sons. Ch. 14 (continuing value), Ch. 15 (cost of capital).
- Modigliani, F., & Miller, M. H. (1963). Corporate income taxes and the cost of capital: A correction. *American Economic Review*, 53(3), 433-443.
- Pratt, S. P., & Grabowski, R. J. (2014). *Cost of Capital: Applications and Examples* (5th ed.). John Wiley & Sons.
- Roll, R. (1977). A critique of the asset pricing theory's tests Part I: On past and potential testability of the theory. *Journal of Financial Economics*, 4(2), 129-176.
