---
type: concept
track: [quant-risk]
tier: advanced
status: solid
prereqs: [interest-rate-risk-in-the-banking-book-irrbb]
est_hours: 4
sources: [Board of Governors of the Federal Reserve System - Comprehensive Capital Analysis and Review: Assessment Framework and Results (2023), European Banking Authority - EU-Wide Stress Test Methodology (2023), Bank of England - The Financial Policy Committee approach to the bank capital framework (2022)]
---

# Stress Testing: CCAR, DFAST, and EBA

## TL;DR

Regulatory stress testing subjects bank portfolios to hypothetical macroeconomic and financial shocks to ensure capital adequacy during severe crises.
In the United States, the Federal Reserve enforces the Comprehensive Capital Analysis and Review (CCAR) and Dodd-Frank Act Stress Testing (DFAST) across Baseline and Severely Adverse scenarios.
In Europe, the European Banking Authority (EBA) and European Central Bank (ECB) conduct biennial EU-wide stress tests under static balance sheet assumptions and IFRS 9 staging rules.
Under modern US rules, CCAR quantitative stress projections directly dictate the Stress Capital Buffer (SCB), bridging point-in-time stress losses with ongoing Pillar 1 minimums.
In Europe, stress test outcomes directly inform Pillar 2 Guidance (P2G) and Pillar 2 Requirements (P2R).
Accurate modeling requires projecting Pre-Provision Net Revenue (PPNR), credit loss migrations, trading book mark-to-market losses, and counterparty defaults across 9-quarter forecast horizons.

## Learning objectives

- Distinguish the supervisory frameworks, objectives, and balance sheet assumptions of US CCAR/DFAST versus European EBA/ECB stress testing.
- Explain the nine-quarter macroeconomic trajectory design, including GDP contraction, unemployment surges, equity drawdowns, and yield curve shifts.
- Formulate the Pre-Provision Net Revenue (PPNR) projection components across net interest income (NII) and non-interest income/expense.
- Quantify stress credit loss estimation under expected loss models, including loan loss provision spikes, charge-offs, and IFRS 9 staging migrations.
- Calculate the US Stress Capital Buffer (SCB) from peak-to-trough CET1 capital drawdowns and planned dividend distributions.
- Contrast static versus dynamic balance sheet assumptions and their direct implications for deleveraging defenses during crises.

## Core concepts

### 1. Regulatory Frameworks: CCAR, DFAST, and EBA

Regulatory stress testing tests whether large banks can survive severe economic distress while continuing to lend to creditworthy households and businesses.

| Dimension | US CCAR / DFAST | European EBA / ECB |
| :--- | :--- | :--- |
| **Primary Regulator** | Federal Reserve Board (FRB) | EBA and ECB Single Supervisory Mechanism (SSM) |
| **Horizon** | 9 quarters forward | 3 years forward (annual steps) |
| **Balance Sheet Assumption** | Dynamic balance sheet (constrained management actions) | Strict static balance sheet (constant volume, maturity, mix) |
| **Capital Linkage** | Directly sets Stress Capital Buffer (SCB) added to Pillar 1 | Informs Pillar 2 Guidance (P2G, non-binding) and P2R (binding) |
| **Accounting Standard** | US GAAP (CECL - Current Expected Credit Losses) | IFRS 9 (Stage 1, 2, and 3 credit migration) |
| **Capital Distribution** | Planned capital actions evaluated; SCB sets payout limits | Hurdle rate assessment; dividend distribution restrictions |

### 2. Supervisory Macroeconomic Scenarios

The Federal Reserve and EBA publish detailed macroeconomic scenarios annually or biennially:
- **Baseline Scenario:** Tracks consensus economic forecasts (moderate growth, stable inflation and unemployment).
- **Severely Adverse Scenario:** Severe global recession characterized by sharp contractions in real GDP (often 5% to 8% peak-to-trough), unemployment surges (spikes to 10% or higher), asset price deflation (commercial real estate down 35% to 40%, equities down 50%), and significant financial market volatility.
- **Global Market Shock (GMS):** An instantaneous, comprehensive repricing shock applied to trading book positions and private equity holdings for institutions with substantial trading operations.
- **Largest Counterparty Default (LCPD):** An instantaneous default of the single largest counterparty across derivatives and securities financing transactions, net of collateral recovery.

### 3. Balance Sheet Dynamics: Static vs. Dynamic Assumptions

The choice of balance sheet assumption alters bank survivability:
- **Static Balance Sheet (EBA approach):**
  Assets and liabilities that mature during the stress horizon are replaced with assets and liabilities having identical remaining maturity, credit quality, sector, and currency.
  The bank cannot organically shrink its loan book, alter its business mix, or cut unprofitable lines to conserve capital.
  This assumption ensures comparability across European institutions but ignores natural deleveraging.
- **Dynamic Balance Sheet (US CCAR approach):**
  Banks model loan demand contractions, drawdowns on committed lines of credit, deposit outflows, and changes in asset composition under economic stress.
  However, regulators restrict speculative management interventions (such as massive fire sales of illiquid assets or unapproved cost cuts).

### 4. PPNR Modeling (Pre-Provision Net Revenue)

PPNR is operating revenue before credit loss provisions and taxes:

$$\text{PPNR} = \text{Net Interest Income (NII)} + \text{Non-Interest Income} - \text{Non-Interest Expense}$$

- **Net Interest Income (NII):**
  Product of stressed asset yields minus stressed funding costs across earning assets.
  During severe recessions, central banks cut policy rates to zero (or hike aggressively in stagflation shocks), causing asset repricing mismatches, margin compression, and deposit beta distortions.
- **Non-Interest Income:**
  Investment banking fees, asset management fees, and trading commissions collapse due to depressed deal activity, market valuation declines, and reduced client trading flows.
- **Non-Interest Expense:**
  Operational costs, regulatory litigation reserves, and IT overhead remain sticky or increase due to workout and collections expenses on defaulted loans.

### 5. Credit Loss Modeling and Staging Under Stress

Credit stress modeling estimates credit impairments over the 9-quarter horizon:
- **US CECL Framework:**
  Requires reserving for lifetime expected credit losses at every stress quarter.
  As macroeconomic forecasts deteriorate in Quarter 1 and Quarter 2, banks must book massive front-loaded provisions before actual defaults peak.
- **European IFRS 9 Framework:**
  Models migration of exposures across three stages:
  - Stage 1: 12-month expected credit loss ($ECL_{12m}$) for performing assets without significant increase in credit risk (SICR).
  - Stage 2: Lifetime expected credit loss ($ECL_{lifetime}$) upon SICR trigger (e.g., ratings downgrade, 30+ days past due, macroeconomic deterioration).
  - Stage 3: Credit-impaired assets (defaulted, 90+ days past due).
  Under the EBA scenario, large swathes of corporate and retail exposures migrate from Stage 1 to Stage 2, resulting in non-linear provision surges.

### 6. Capital Determination: The US Stress Capital Buffer (SCB)

Introduced in 2020, the SCB integrates CCAR stress projections into ongoing capital requirements:

$$\text{SCB} = \max\left(2.5\%, \left(\text{Starting CET1 Ratio} - \text{Minimum Stressed CET1 Ratio}\right) + \frac{4 \times \text{Planned Common Dividends}}{\text{Stressed RWA}}\right)$$

Where:
- Starting CET1 Ratio is the actual capital ratio at the projection base date (typically Q4).
- Minimum Stressed CET1 Ratio is the lowest projected CET1 ratio reached across any of the 9 quarters under the Severely Adverse scenario.
- $4 \times \text{Planned Common Dividends}$ represents the next four quarters of planned dividend payments.
- The standard floor is $2.5\%$.
- The total CET1 requirement for a Category I bank becomes:

$$\text{Total CET1 Minimum} = 4.5\% \text{ (Pillar 1)} + \text{SCB} + \text{G-SIB Surcharge} + \text{CCyB}$$

## Worked examples

### Example 1: Full 9-Quarter CET1 Trajectory and SCB Calculation

A US Category I bank reports the following starting balance sheet and capital position at Q0:
- Tier 1 Common Equity (CET1): $\$50,000\text{ million}$
- Risk-Weighted Assets (RWA): $\$400,000\text{ million}$
- Starting CET1 Ratio: $\frac{\$50,000}{\$400,000} = 12.50\%$
- Planned Quarterly Common Stock Dividends: $\$500\text{ million}$ (total $\$2,000\text{ million}$ over 4 quarters)
- Effective Corporate Tax Rate: $21\%$ (assuming immediate tax benefit offset against deferred tax liabilities)

Under the Federal Reserve Severely Adverse scenario, the 9-quarter stress model generates cumulative financial results:
- Cumulative 9-Quarter PPNR: $+\$14,000\text{ million}$
- Cumulative 9-Quarter Provisions for Loan Losses: $-\$22,000\text{ million}$
- Instantaneous Global Market Shock (GMS) Pre-Tax Loss: $-\$6,000\text{ million}$
- Largest Counterparty Default (LCPD) Pre-Tax Loss: $-\$2,000\text{ million}$
- Cumulative Pre-Tax Net Income:

$$\text{Pre-Tax Net Income} = 14,000 - 22,000 - 6,000 - 2,000 = -\$16,000\text{ million}$$

- Cumulative After-Tax Loss (at 21%):

$$\text{Net Loss} = -16,000 \times (1 - 0.21) = -\$12,640\text{ million}$$

Quarterly distribution of stress impacts:
- In Quarter 3, cumulative after-tax losses reach $-\$9,500\text{ million}$.
- Credit line drawdowns and market volatility expand RWA in Quarter 3 from $\$400,000\text{ million}$ to $\$425,000\text{ million}$.
- Stressed CET1 Capital at Quarter 3:

$$\text{Stressed CET1}_{\text{Q3}} = \$50,000 - \$9,500 = \$40,500\text{ million}$$

- Minimum Stressed CET1 Ratio (reached at Q3 trough):

$$\text{CET1 Ratio}_{\text{Q3}} = \frac{\$40,500}{\$425,000} = 9.5294\% \approx 9.53\%$$

- Peak-to-Trough Capital Depletion:

$$\text{Depletion} = \text{Starting CET1 Ratio} - \text{Minimum Stressed CET1 Ratio} = 12.50\% - 9.53\% = 2.97\%$$

- Dividend Add-On Component (using Q3 RWA of $\$425,000\text{ million}$, the quarter with the lowest projected CET1 ratio, as required by 12 CFR 225.8):

$$\text{Dividend Add-on} = \frac{4 \times \$500}{\$425,000} = \frac{\$2,000}{\$425,000} = 0.4706\% \approx 0.47\%$$

- Calculated SCB:

$$\text{SCB} = \max\left(2.5\%, 2.97\% + 0.47\%\right) = \max(2.5\%, 3.44\%) = 3.44\%$$

The bank's new binding CET1 capital requirement (assuming a $2.0\%$ G-SIB surcharge and $0.0\%$ CCyB) is:

$$\text{Required CET1} = 4.5\% + 3.44\% + 2.0\% + 0.0\% = 9.94\%$$

With a starting capital ratio of $12.50\%$, the bank maintains a capital cushion of $12.50\% - 9.94\% = 2.56\%$ above its regulatory restriction threshold.

### Example 2: EBA IFRS 9 Staging Transition Under Macroeconomic Stress

A European commercial bank holds a $€10,000\text{ million}$ portfolio of corporate loans at Year 0.
Under normal economic conditions:
- $90\%$ of loans are in Stage 1 ($€9,000\text{ million}$), with 12-month $PD = 0.8\%$ and $LGD = 40\%$.
- $10\%$ of loans are in Stage 2 ($€1,000\text{ million}$), with lifetime $PD = 6.0\%$ and $LGD = 45\%$.
- Stage 1 Provisions: $9,000 \times 0.008 \times 0.40 = €28.8\text{ million}$.
- Stage 2 Provisions: $1,000 \times 0.060 \times 0.45 = €27.0\text{ million}$.
- Baseline Provisions: $28.8 + 27.0 = €55.8\text{ million}$.

Under the EBA Severely Adverse 3-year scenario:
- $25\%$ of Stage 1 loans experience a Significant Increase in Credit Risk (SICR) and migrate to Stage 2 ($€2,250\text{ million}$).
- Remaining Stage 1 loans ($€6,750\text{ million}$) see 12-month $PD$ double to $1.6\%$.
- Stressed Stage 2 loans ($€1,000 + €2,250 = €3,250\text{ million}$) see lifetime $PD$ rise to $14.0\%$ and stressed $LGD$ rise to $50\%$.
- Stressed Stage 1 Provisions: $6,750 \times 0.016 \times 0.40 = €43.2\text{ million}$.
- Stressed Stage 2 Provisions: $3,250 \times 0.140 \times 0.50 = €227.5\text{ million}$.
- Total Stressed Provisions: $43.2 + 227.5 = €270.7\text{ million}$.
- Net Provision Spike: $€270.7 - €55.8 = €214.9\text{ million}$ (a $385\%$ increase).
Under the static balance sheet rule, the bank cannot resolve this capital drain by shrinking the corporate lending book.

## Pitfalls

- **Ignoring CECL Reserve Front-Loading:** Under US CECL, banks cannot recognize loan losses gradually as defaults occur.
  Lifetime expected credit losses must be recognized when economic forecasts worsen in Q1, creating an early CET1 trough.
- **Assuming Constant RWA Under Stress:** RWAs do not remain static during economic crises.
  Corporate credit downgrades trigger higher regulatory risk weights, derivative netting sets suffer higher replacement costs, and drawn commitments increase total balance sheet assets.
- **Double Counting GMS and Credit Losses:** If corporate bond trading positions suffer mark-to-market declines under the Global Market Shock, analysts must verify that the same corporate issuers are not double-counted in the banking book credit default module.
- **Confusing DFAST with CCAR:** DFAST is purely a supervisory and company-run stress testing exercise using standardized capital distributions.
  CCAR incorporates bank-proposed capital actions (dividends, share buybacks) and directly sets binding capital constraints via the SCB.
- **Neglecting Tax Valuation Allowances:** In a severe stress scenario, accumulating pre-tax operating losses can create substantial Deferred Tax Assets (DTAs).
  If the bank cannot demonstrate future profitability to realize these DTAs, supervisory rules require deducting them from CET1 capital, compounding capital depletion.

## Interview questions

> [!question]- reg-17-01 | What is the primary difference between US CCAR and European EBA stress testing methodologies regarding balance sheet assumptions?
> EBA enforces a strict static balance sheet assumption where maturing assets and liabilities are replaced with identical instruments, preventing banks from organically deleveraging or altering their business mix.
> In contrast, US CCAR uses dynamic balance sheet modeling where banks project realistic loan contractions, commitment drawdowns, and deposit shifts, subject to supervisory validation.

> [!question]- reg-17-02 | How is the Stress Capital Buffer (SCB) under the Federal Reserve framework calculated?
> The SCB is calculated as $\max(2.5\%, \text{Peak-to-Trough CET1 Ratio Depletion} + \text{Four Quarters of Planned Dividends as \% of Stressed RWA})$.
> It replaces the previous static $2.5\%$ capital conservation buffer for large US banks, tailoring ongoing capital requirements to specific stress losses.

> [!question]- reg-17-03 | What constitutes the Pre-Provision Net Revenue (PPNR) in stress testing?
> PPNR equals Net Interest Income plus Non-Interest Income minus Non-Interest Expense before deducting provisions for loan and lease losses and income taxes.
> It measures the core operating earnings available to absorb credit and market losses during an economic crisis.

> [!question]- reg-17-04 | How does the CECL accounting standard affect the quarterly timing of credit loss recognition in CCAR?
> CECL requires recognizing lifetime expected credit losses based on reasonable and supportable macroeconomic forecasts.
> When the severe stress scenario is initiated, forward-looking macroeconomic deterioration causes a massive spike in loan loss allowances in Quarters 1 and 2, shifting the capital trough earlier compared to incurred loss models.

> [!question]- reg-17-05 | What is the Global Market Shock (GMS) component in supervisory stress tests?
> The GMS is an instantaneous, comprehensive asset price and volatility repricing shock applied to the trading book and private equity portfolios of banks with significant trading operations.
> Mark-to-market gains and losses are recognized in the first quarter of the projection horizon without any portfolio rebalancing.

> [!question]- reg-17-06 | What is the Largest Counterparty Default (LCPD) scenario?
> The LCPD assumes the instantaneous and unexpected default of the bank's single largest counterparty across derivatives and securities financing transactions.
> The net stressed exposure is calculated after applying stressed collateral haircuts, and the resulting uncollateralized loss is deducted in Quarter 1.

> [!question]- reg-17-07 | How does RWA migration exacerbate capital depletion during stress periods?
> During economic downturns, credit quality degrades, triggering borrower downgrades that elevate IRB risk weights.
> Furthermore, off-balance sheet credit lines are drawn by liquidity-strained corporates, expanding total assets.
> The expansion in the denominator (RWA) occurs simultaneously with the erosion of the numerator (CET1), driving a sharp drop in the capital ratio.

> [!question]- reg-17-08 | What is the difference between binding Pillar 2 Requirements (P2R) and non-binding Pillar 2 Guidance (P2G) in the ECB framework?
> P2R is a legally binding capital requirement addressing risks underestimated or not covered by Pillar 1; breaching P2R restricts dividend distributions through the Maximum Distributable Amount (MDA).
> P2G is supervisory capital guidance derived from stress test outcomes; breaching P2G does not trigger automatic legal restrictions on distributions but triggers intense supervisory intervention.

> [!question]- reg-17-09 | Why do banks face DTA (Deferred Tax Asset) deduction hurdles during severe stress tests?
> Accumulating net operating losses generate DTAs that depend on future profitability to be realized.
> Under Basel III and US capital rules, DTAs that rely on future profitability and exceed statutory thresholds must be deducted 100% from CET1 capital, accelerating capital erosion right at the stress trough.

> [!question]- reg-17-10 | How do deposit betas and non-maturity deposit behavior impact PPNR under rapid rate shock stress scenarios?
> Rapid rate hikes or cuts alter the spread between earning assets and funding liabilities.
> In a stagflation shock, deposit betas rise as depositors shift non-interest bearing balances into higher-yielding instruments, compressing net interest margins and sharply reducing PPNR.

## Further reading

- Federal Reserve Board. *Dodd-Frank Act Stress Testing (DFAST) and CCAR Supervisory Scenarios*. Published annually in February.
- European Banking Authority (EBA). *Methodological Note: EU-wide Stress Test*. EBA guidelines.
- Basel Committee on Banking Supervision. *Stress testing principles*. BCBS guidelines, October 2018. https://www.bis.org/bcbs/publ/d450.htm
- Schuermann, Til. *Stress Testing Banks*. International Journal of Forecasting, 2014.
- Federal Reserve Board. *Comprehensive Capital Analysis and Review: Summary Instructions and Results*. FRB Publications.

## In this repo and SDE-Interview-Prep

- 01-Capital-RWA-and-the-Basel-Framework.md - Basel capital definitions and minimums.
- 03-Credit-Risk-Capital-SA-and-IRB.md - Standardised and IRB credit risk models.
- 16-Interest-Rate-Risk-in-the-Banking-Book-IRRBB.md - IRRBB principles and shocks.
- `code/basel_stress_reg.py` - Reference implementation verifying SCB calculations and IFRS 9 stress staging.
