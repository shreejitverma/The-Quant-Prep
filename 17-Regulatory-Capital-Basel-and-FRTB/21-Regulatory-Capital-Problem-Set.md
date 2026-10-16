---
type: problem-set
track: [quant-trader, quant-research, quant-dev]
tier: core
status: draft
prereqs: [capital-aware-trading-kva-and-rwa-limits]
est_hours: 4
sources: [Basel Committee on Banking Supervision - The Basel Framework (Consolidated 2024), Jon Gregory - Counterparty Credit Risk and Credit Value Adjustment (2015), Darrell Duffie - How Big Banks Fail and What to Do About It (2011)]
---

# Regulatory Capital Problem Set

## TL;DR

This comprehensive problem set synthesizes the core quantitative methods, regulatory formulas, and analytical trade-offs across the entire Basel capital framework.
Problems span the full spectrum of capital adequacy: the Pillar 1/Pillar 2 capital stack, the Basel IV output floor, Vasicek credit risk modeling, SA-CCR exposure calculations, CVA capital charges under BA-CVA, FRTB Sensitivities-Based Method (SbM) market risk aggregations, Default Risk Charge (DRC), IMA Expected Shortfall with liquidity horizons, Operational Risk SMA, LCR and NSFR liquidity ratios, IRRBB economic value sensitivity shocks, and Capital Valuation Adjustment (KVA).
Each problem presents clear input parameters, complete step-by-step arithmetic derivations, and rigorous risk management takeaways.

## Learning objectives

- Calculate complete bank regulatory capital stacks including CET1, Tier 1, Total Capital, and all supervisory buffers.
- Apply the Basel IV output floor to internal ratings-based (IRB) and internal models approach (IMA) institutions.
- Derive capital requirements for corporate credit exposures using the Vasicek asymptotic single risk factor model.
- Compute counterparty credit risk EAD for complex derivative netting sets under SA-CCR across margined and unmargined agreements.
- Aggregate multi-currency market risk capital under the FRTB Sensitivities-Based Method across low, medium, and high correlation regimes.
- Quantify operational risk capital under the Standardised Measurement Approach (SMA) and evaluate liquidity and IRRBB compliance.

## Core concepts

### 1. Capital Stack Structure and Hierarchy

The Basel III/IV regulatory capital stack establishes minimum solvency constraints:
- **Pillar 1 Minimums:** Common Equity Tier 1 ($4.5\%$), Tier 1 ($6.0\%$), and Total Capital ($8.0\%$).
- **Capital Conservation Buffer (CCB):** $2.5\%$ CET1, or replaced by the Stress Capital Buffer (SCB) in the United States.
- **Countercyclical Capital Buffer (CCyB):** $0.0\%$ to $2.5\%$ CET1 depending on national credit-to-GDP expansion.
- **G-SIB Surcharge:** $1.0\%$ to $3.5\%+$ CET1 based on global systemic importance score.
- **Pillar 2 Requirements (P2R):** Bank-specific supervisory add-ons addressing uncaptured risks.

### 2. Basel IV Output Floor

$$\text{RWA}_{\text{Binding}} = \max\left(\text{RWA}_{\text{Internal Models}}, 72.5\% \times \text{RWA}_{\text{Standardized}}\right)$$

Where:
- $\text{RWA}_{\text{Standardized}} = \text{Credit SA} + \text{FRTB SA} + \text{Operational Risk SMA} + 12.5 \times \text{CVA capital charge}$.
- Phased in from $50\%$ to $72.5\%$ over five years.

### 3. Vasicek ASRF Credit Risk Formula

$$K = \left[ LGD \times \Phi\left( \frac{\Phi^{-1}(PD) + \sqrt{\rho} \Phi^{-1}(0.999)}{\sqrt{1 - \rho}} \right) - (PD \times LGD) \right] \times \frac{1 + (M - 2.5)b}{1 - 1.5b}$$

Where asset correlation $\rho$ and maturity adjustment $b$ are prescribed supervisory functions of PD and firm size.

### 4. SA-CCR Counterparty Credit Risk EAD

$$\text{EAD} = 1.4 \times (\text{RC} + \text{PFE})$$
$$\text{PFE} = \text{Multiplier} \times \sum_{a} \text{AddOn}^{(a)}$$

### 5. FRTB Sensitivities-Based Method (SbM)

$$K_{\text{SbM}} = \sqrt{ \sum_k K_k^2 + \sum_k \sum_{l \neq k} \gamma_{kl} S_k S_l }$$

Aggregated across three correlation scenarios: Medium ($\rho_{kl}$), High ($1.25 \rho_{kl}$ capped at 1.0), and Low ($2 \rho_{kl} - 1.0$ or $0.75 \rho_{kl}$).

## Worked examples

### Problem 1: Enterprise Capital Adequacy and Output Floor Binding Check

A globally active investment bank operates with an internal models framework across credit and market risk.
The bank's risk department compiles the following risk-weighted asset projections:
- Internal Models Stack ($\text{RWA}_{\text{Internal}}$):
  - Credit Risk (A-IRB): $\$280,000\text{ million}$
  - Market Risk (FRTB IMA): $\$35,000\text{ million}$
  - Operational Risk (SMA): $\$45,000\text{ million}$
  - CVA Capital Charge: $\$10,000\text{ million}$ (equivalent to $\$125,000\text{ million}$ RWA at the 8% minimum capital ratio)
  - Total Internal RWA: $\$280,000 + \$35,000 + \$45,000 + \$125,000 = \$485,000\text{ million}$

- Standardized Stack ($\text{RWA}_{\text{Standardized}}$):
  - Credit Risk (SA): $\$420,000\text{ million}$
  - Market Risk (FRTB SA): $\$55,000\text{ million}$
  - Operational Risk (SMA): $\$45,000\text{ million}$
  - CVA Capital (SA-CVA): $\$16,000\text{ million}$ (equivalent to $\$200,000\text{ million}$ RWA at the 8% minimum capital ratio)
  - Total Standardized RWA: $\$420,000 + \$55,000 + \$45,000 + \$200,000 = \$720,000\text{ million}$

The bank's capital components are:
- Common Equity Tier 1 (CET1): $\$44,000\text{ million}$
- Additional Tier 1 (AT1): $\$6,000\text{ million}$
- Tier 2 Capital: $\$8,000\text{ million}$

Supervisory requirements applicable to the bank:
- Pillar 1 Minimums: CET1 $4.5\%$, Tier 1 $6.0\%$, Total Capital $8.0\%$
- Capital Conservation Buffer (CCB): $2.5\%$
- G-SIB Surcharge (Bucket 2): $1.5\%$
- Countercyclical Capital Buffer (CCyB): $0.5\%$
- Pillar 2 Requirement (P2R): $1.5\%$ (must be held $56.25\%$ in CET1)
- Basel IV Output Floor: Fully phased-in at $72.5\%$

#### Step 1: Output Floor Evaluation

Compute the standardized floor threshold:

$$\text{Floor Threshold} = 72.5\% \times \text{RWA}_{\text{Standardized}} = 0.725 \times \$720,000\text{ million} = \$522,000\text{ million}$$

Compare with Internal Models RWA:

$$\text{RWA}_{\text{Internal}} = \$485,000\text{ million} < \$522,000\text{ million}$$

The output floor binds!
The bank must report and capitalize against the higher floor RWA:

$$\text{Binding RWA} = \$522,000\text{ million}$$

RWA Increase from floor:

$$\Delta\text{RWA} = \$522,000 - \$485,000 = \$37,000\text{ million (+7.63\%)}$$

#### Step 2: Total Required Capital Target Calculation

Break down the CET1 requirement:
- Pillar 1 CET1 Minimum: $4.5\%$
- P2R CET1 component: $1.5\% \times 56.25\% = 0.84375\%$
- CCB: $2.5\%$
- G-SIB: $1.5\%$
- CCyB: $0.5\%$
- Total CET1 Target Ratio:

$$\text{Target CET1 Ratio} = 4.5\% + 0.84375\% + 2.5\% + 1.5\% + 0.5\% = 9.84375\% \approx 9.84\%$$

Total Capital Target Ratio:
- Pillar 1: $8.0\%$
- P2R: $1.5\%$
- CCB: $2.5\%$
- G-SIB: $1.5\%$
- CCyB: $0.5\%$
- Total Capital Target: $8.0\% + 1.5\% + 2.5\% + 1.5\% + 0.5\% = 14.0\%$

#### Step 3: Capital Adequacy and Buffer Surplus/Deficit

Actual capital ratios based on binding RWA of $\$522,000\text{ million}$:
- Actual CET1 Ratio:

$$\text{CET1 Ratio} = \frac{\$44,000}{\$522,000} = 8.4291\% \approx 8.43\%$$

- CET1 Cushion above Target:

$$\text{CET1 Surplus} = 8.4291\% - 9.84375\% = -1.41465\% \approx -1.41\%$$
$$\text{Surplus in Dollars} = -0.0141465 \times \$522,000\text{ million} \approx -\$7,384.4\text{ million}$$

- Actual Total Capital Ratio:

$$\text{Total Capital} = \$44,000 + \$6,000 + \$8,000 = \$58,000\text{ million}$$
$$\text{Total Capital Ratio} = \frac{\$58,000}{\$522,000} = 11.1111\% \approx 11.11\%$$

- Total Capital Surplus above $14.0\%$ Target:

$$\text{Total Surplus} = 11.1111\% - 14.0\% = -2.8889\% \approx -\$15,080\text{ million}$$

Conclusion:
The bank breaches the CET1 and total capital targets after the output floor binds.
Even before the floor, its $\$485,000\text{ million}$ internal RWA implies CET1 of 9.07% and total capital of 11.96%, both below the stated targets.
The floor raises RWA to $\$522,000\text{ million}$, reducing CET1 to 8.43% and total capital to 11.11%.

### Problem 2: SA-CCR Margined vs. Unmargined Netting Set Comparison

A fixed income desk maintains a bilateral derivative netting set with a hedge fund consisting of three interest rate swaps:
- Trade 1: 5-year swap, Notional $\$100\text{ million}$, MtM $= +\$2,500,000$ (Bank receives fixed)
- Trade 2: 10-year swap, Notional $\$50\text{ million}$, MtM $= -\$1,800,000$ (Bank pays fixed)
- Trade 3: 2-year swap, Notional $\$80\text{ million}$, MtM $= +\$300,000$ (Bank receives fixed)
- All trades are USD interest rate products in the same supervisory currency bucket.

Supervisory parameters:
- Supervisory Factor for Interest Rates: $SF = 0.5\%$
- Supervisory Duration:
  - Trade 1 (5y): $SD_1 = \frac{e^{-0.05 \times 0} - e^{-0.05 \times 5}}{0.05} = \frac{1 - 0.778801}{0.05} = 4.4240$
  - Trade 2 (10y): $SD_2 = \frac{1 - e^{-0.05 \times 10}}{0.05} = \frac{1 - 0.606531}{0.05} = 7.8694$
  - Trade 3 (2y): $SD_3 = \frac{1 - e^{-0.05 \times 2}}{0.05} = \frac{1 - 0.904837}{0.05} = 1.9033$

Maturity Buckets and Supervisory Delta:
- Trade 1 (Time-to-maturity 5y, Time-to-start 0): Bucket 3 ($> 5$ years? 5y is Bucket 2: 1 to 5 years).
  - Let's classify: Bucket 1 is $\le 1$ year, Bucket 2 is $> 1$ and $\le 5$ years, Bucket 3 is $> 5$ years.
  - Trade 1: 5y $\to$ Bucket 2. Receive-fixed value falls when rates rise ($\delta_1 = -1$).
  - Trade 2: 10y $\to$ Bucket 3. Pay-fixed value rises when rates rise ($\delta_2 = +1$).
  - Trade 3: 2y $\to$ Bucket 2. Receive-fixed value falls when rates rise ($\delta_3 = -1$).

Effective Notional within Buckets:
- Bucket 2:
  $$D_{2,1} = \delta_1 \times N_1 \times SD_1 = -1 \times \$100\text{M} \times 4.4240 = -\$442.40\text{M}$$
  $$D_{2,3} = \delta_3 \times N_3 \times SD_3 = -1 \times \$80\text{M} \times 1.9033 = -\$152.26\text{M}$$
  $$D_{\text{Bucket 2}} = -442.40 - 152.26 = -\$594.66\text{M}$$
- Bucket 3:
  $$D_{\text{Bucket 3}} = \delta_2 \times N_2 \times SD_2 = +1 \times \$50\text{M} \times 7.8694 = +\$393.47\text{M}$$

Aggregated Effective Notional for Currency (USD):

$$D_{\text{USD}} = \sqrt{ D_{\text{Bucket 2}}^2 + D_{\text{Bucket 3}}^2 + 1.4 \times D_{\text{Bucket 2}} \times D_{\text{Bucket 3}} }$$
$$D_{\text{USD}} = \sqrt{ (-594.66)^2 + (393.47)^2 + 1.4 \times (-594.66) \times (393.47) }$$
$$D_{\text{USD}} = \sqrt{ 353,620.5 + 154,818.6 - 327,575.5 } = \sqrt{ 180,863.6 } = \$425.28\text{ million}$$

Add-On for IR Asset Class:

$$\text{AddOn}_{\text{IR}} = SF \times D_{\text{USD}} = 0.005 \times \$425.28\text{ million} = \$2,126,400$$

Net Portfolio Value:

$$V = +\$2,500,000 - \$1,800,000 + \$300,000 = +\$1,000,000$$

#### Case A: Unmargined Agreement (No Collateral, $C = 0$)
- Replacement Cost: $\text{RC} = \max(V - C, 0) = \max(\$1,000,000, 0) = \$1,000,000$
- Multiplier:

$$\text{Multiplier} = \min\left(1.0, 0.05 + 0.95 \times \exp\left( \frac{1,000,000}{2 \times 0.95 \times 2,126,400} \right)\right)$$
$$\text{Multiplier} = \min\left(1.0, 0.05 + 0.95 \times \exp(0.2475)\right) = \min(1.0, 0.05 + 0.95 \times 1.2808) = 1.0$$

- Potential Future Exposure:

$$\text{PFE} = 1.0 \times \$2,126,400 = \$2,126,400$$

- Total EAD:

$$\text{EAD}_{\text{Unmargined}} = 1.4 \times (\text{RC} + \text{PFE}) = 1.4 \times (\$1,000,000 + \$2,126,400) = 1.4 \times \$3,126,400 = \$4,376,960$$

#### Case B: Margined Agreement
- Collateral Held ($C$): $\$800,000$ cash
- Threshold ($\text{TH}$): $\$0$
- Minimum Transfer Amount ($\text{MTA}$): $\$50,000$
- Net Independent Collateral Amount ($\text{NICA}$): $\$0$
- Replacement Cost:

$$\text{RC} = \max(V - C, \text{TH} + \text{MTA} - \text{NICA}, 0) = \max(1,000,000 - 800,000, 0 + 50,000, 0) = \max(\$200,000, \$50,000, 0) = \$200,000$$

- Multiplier:
  $$V - C = \$200,000$$
  $$\text{Multiplier} = \min\left(1.0, 0.05 + 0.95 \times \exp\left( \frac{200,000}{2 \times 0.95 \times 2,126,400} \right)\right)$$
  $$\text{Multiplier} = 0.05 + 0.95 \times \exp(0.0495) = 0.05 + 0.95 \times 1.0507 = 0.05 + 0.9982 = 1.0$$
- Margin Period of Risk (MPOR) factor:
  For centrally cleared or daily margined bilateral portfolios with hedge funds, $\text{MPOR} = 10\text{ business days}$.
  Supervisory unmargined maturity scaling assumes $1\text{ year} = 250\text{ days}$.
  Margined maturity factor:

$$MF = \frac{3}{2} \sqrt{\frac{\text{MPOR}}{250}} = 1.5 \times \sqrt{\frac{10}{250}} = 1.5 \times \sqrt{0.04} = 1.5 \times 0.20 = 0.30$$

- Stressed Margined Add-On:

$$\text{AddOn}_{\text{Margined}} = 0.30 \times \$2,126,400 = \$637,920$$

- Margined PFE:

$$\text{PFE}_{\text{Margined}} = 1.0 \times \$637,920 = \$637,920$$

- Margined EAD:

$$\text{EAD}_{\text{Margined}} = 1.4 \times (\text{RC} + \text{PFE}) = 1.4 \times (\$200,000 + \$637,920) = 1.4 \times \$837,920 = \$1,173,088$$

EAD Reduction:

$$\Delta\text{EAD} = \$4,376,960 - \$1,173,088 = \$3,203,872\text{ (a 73.2\% reduction)}$$

Posting daily margin with an $\$800,000$ cash cushion eliminates over $73\%$ of counterparty credit risk exposure and regulatory capital.

## Pitfalls

- **Ignoring the Output Floor in Internal Model Optimization:** Optimizing A-IRB risk weights or FRTB internal models without checking the standardized floor creates illusionary capital savings that get wiped out by the $72.5\%$ floor.
- **Applying Standalone Formulae to Netting Sets:** Computing SA-CCR EAD or KVA on a trade-by-trade basis violates regulatory rules and grossly overstates capital by ignoring netting benefits and directional offsets.
- **Misinterpreting Supervisory MPOR:** Underestimating the Margin Period of Risk (e.g., using 10 days instead of 20 days for illiquid collateral or non-standard master agreements) leads to severe supervisory audit sanctions.
- **Overlooking FRTB Multi-Currency Correlation Penalties:** Calculating multi-currency GIRR capital by simply summing currency capitals ignores the mandatory cross-currency correlation ($\gamma = 0.50$) and high/low scenario stress multipliers.
- **Confusing Accounting Reserves with Regulatory Capital:** Deducting accounting CVA from capital reserves without accounting for the regulatory CVA capital charge (BA-CVA or SA-CVA) results in unexpected Pillar 1 capital deficits.

## Interview questions

> [!question]- reg-21-01 | What is the mathematical formula and economic rationale for the Basel IV Output Floor?
> The formula is $\text{RWA}_{\text{Binding}} = \max(\text{RWA}_{\text{Internal}}, 72.5\% \times \text{RWA}_{\text{Standardized}})$.
> The rationale is to restore market confidence by limiting excessive model variability and curbing aggressive internal model parameter choices across global banks.

> [!question]- reg-21-02 | How does the maturity adjustment factor in the Vasicek formula behave as PD approaches zero?
> The maturity adjustment factor is $\frac{1 + (M - 2.5)b}{1 - 1.5b}$, where $b = [0.11852 - 0.05478 \times \ln(PD)]^2$.
> As $PD$ decreases (higher credit quality), $b$ increases, making capital significantly more sensitive to longer maturities $M$ because unexpected downgrade risk over time is highest for high-grade credits.

> [!question]- reg-21-03 | In SA-CCR, under what condition does the PFE multiplier drop below 1.0?
> The multiplier drops below $1.0$ when the netting set holds excess collateral ($C > V$) such that $V - C < 0$.
> The formula $0.05 + 0.95 \times \exp\left(\frac{V-C}{2 \times 0.95 \times \text{AddOn}}\right)$ decays exponentially toward the $5\%$ floor as the collateral surplus increases.

> [!question]- reg-21-04 | Why are three correlation scenarios (Medium, High, Low) required under the FRTB Sensitivities-Based Method?
> Historical correlations break down during market crises: correlated assets can decouple (low correlation stress) or uncorrelated assets can collapse together (high correlation stress).
> Computing capital across $1.0 \times \rho$, $1.25 \times \rho$, and $0.75 \times \rho$ (or $2\rho - 1$) ensures desks holding basis trades or curve hedges hold robust capital against correlation breakdown.

> [!question]- reg-21-05 | What is the difference between the Business Indicator (BI) and the Business Indicator Component (BIC) in the Operational Risk SMA?
> The BI is the raw financial accounting proxy summing the Interest, Leases, and Dividend Component (ILDC), the Services Component (SC), and the Financial Component (FC).
> The BIC is the tiered marginal capital requirement obtained by applying progressive marginal weights ($12\%$ for $\le \$1\text{B}$, $15\%$ for $\$1\text{B}-\$30\text{B}$, $18\%$ for $> \$30\text{B}$) to the BI.

> [!question]- reg-21-06 | What is the Maximum Distributable Amount (MDA) and what triggers it?
> The MDA is the statutory cap on discretionary capital distributions (common dividends, share buybacks, and AT1 coupon payments).
> It is triggered when a bank's CET1 ratio breaches its Combined Buffer Requirement (CCB + CCyB + G-SIB + P2R) even if it remains above its Pillar 1 minimums.

> [!question]- reg-21-07 | How does the Liquidity Coverage Ratio (LCR) treat operational versus non-operational corporate deposits?
> Operational deposits (arising from clearing, custody, and cash management services necessary for client operations) are assigned a low outflow rate ($25\%$ under Basel III).
> Non-operational corporate deposits (excess treasury liquidity placed for yield) are deemed flighty and assigned a high outflow rate ($100\%$ if uncollateralized).

> [!question]- reg-21-08 | What are the two tests required for a trading desk to maintain Internal Model Approach (IMA) eligibility under FRTB?
> The two tests are:
> 1. Backtesting: Counting 1-day 99% VaR exceptions against Actual PnL and Hypothetical PnL over a 250-day window (must remain in the Green Zone with $\le 4$ exceptions).
> 2. P&L Attribution (PLA) Testing: Measuring the Spearman correlation ($r_s \ge 0.80$) and Kolmogorov-Smirnov test metric ($KS \le 0.09$) between Hypothetical PnL and Risk-Theoretical PnL.

> [!question]- reg-21-09 | What is a Non-Modellable Risk Factor (NMRF) and how is its capital charge calculated?
> An NMRF is a risk factor that fails the Risk Factor Eligibility Test (RFET), which requires at least 24 verifiable real price observations per year with no 90-day gap.
> NMRF capital is calculated using an extreme stressed Expected Shortfall measure ($SES$) aggregated across risk factors assuming conservative correlation structures.

> [!question]- reg-21-10 | Why does an uncollateralized interest rate swap have a higher KVA than a centrally cleared swap?
> An uncollateralized swap incurs bilateral SA-CCR counterparty risk exposure and BA-CVA or SA-CVA capital charges over its entire 5-to-30 year lifetime.
> A cleared swap faces a qualifying CCP with a $2\%$ risk weight and zero CVA capital charge, lowering required lifetime capital $K(t)$ to near-zero.

> [!question]- reg-21-11 | What is the supervisory floor on LGD for senior corporate exposures under the Advanced IRB approach?
> Under Basel III finalisation, supervisory input floors establish an LGD floor of $25\%$ for unsecured senior corporate exposures and $0\%$, $10\%$, $10\%$ and $15\%$ for exposures secured by financial collateral, receivables, real estate and other physical collateral (CRE32.16).

> [!question]- reg-21-12 | How does the Leverage Ratio act as a backstop to the risk-weighted capital framework?
> The Leverage Ratio is non-risk-weighted: $\text{Leverage Ratio} = \frac{\text{Tier 1 Capital}}{\text{Total Leverage Exposure}} \ge 3.0\%$.
> It prevents banks from accumulating massive balance sheets loaded with low-risk-weighted assets (e.g., sovereign bonds or repo books) that could trigger insolvency during unexpected systemic liquidity shocks.

> [!question]- reg-21-13 | What is the economic difference between Economic Value of Equity (EVE) and Net Interest Income (NII) in IRRBB?
> EVE is a long-term, economic valuation metric measuring the change in the net present value of all banking book assets, liabilities, and off-balance sheet items under interest rate shocks.
> NII is a short-term, accounting earnings metric measuring the projected change in net interest income over a 1-to-2 year horizon.

> [!question]- reg-21-14 | Under what condition is the Internal Loss Multiplier (ILM) equal to 1.0 in the Operational Risk SMA?
> The ILM equals $1.0$ when the Loss Component ($15 \times \text{Average 10-Year Annual Operational Losses}$) exactly equals the Business Indicator Component (BIC), or when the national supervisor exercises national discretion to set $\text{ILM} = 1.0$ (as proposed in the US and UK).

> [!question]- reg-21-15 | In the FRTB Default Risk Charge (DRC), why is the supervisory floor on LGD set to 100% for equity positions?
> Equities represent the most junior claim in a corporate capital structure; in the event of default or bankruptcy, equity holders suffer complete loss of principal before any debt recovery.
> Hence, the DRC supervisory formula prescribes an LGD of $100\%$ for all equity exposures.

## Further reading

- Basel Committee on Banking Supervision. *The Basel Framework: Consolidated Rules*. BIS Online Portal.
- Gregory, Jon. *The xVA Challenge: Counterparty Risk, Funding, Collateral, Capital and Initial Margin*. 4th Edition, Wiley, 2020.
- Resti, Andrea and Sironi, Andrea. *Risk Management and Shareholders' Value in Banking*. Wiley Finance, 2007.
- Federal Reserve Board. *Supervisory Assessment of Capital Planning and Adequacy*. SR Letter 15-18.
