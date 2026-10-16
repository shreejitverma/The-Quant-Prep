---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: advanced
status: draft
prereqs: [bcbs-239-risk-data-aggregation]
est_hours: 4
sources: [European Union - Capital Requirements Regulation III (CRR3 2024), Federal Reserve Board - Re-proposal on Basel III Endgame Rules (2024), UK Prudential Regulation Authority - Implementation of the Basel 3.1 standards (PS9/24 2024), Basel Committee on Banking Supervision - Basel III Monitoring Report (2024)]
---

# Implementation Status by Jurisdiction

## TL;DR

While the Basel Committee on Banking Supervision (BCBS) establishes international regulatory capital benchmarks, individual sovereign jurisdictions enact them through domestic legislation.
This creates divergence across timelines, technical rules, and capital floors.
The European Union enacted Capital Requirements Regulation III (CRR3) effective January 1, 2025, incorporating temporary relief for unrated corporates, residential real estate, and legacy CVA corporate exemptions.
The United States proposed the "Basel III Endgame" for banks with assets exceeding $100 billion, sparking industry pushback that resulted in a major 2024 re-proposal scaling back capital surcharges and adjusting the Operational Risk Internal Loss Multiplier.
The United Kingdom Prudential Regulation Authority (PRA) finalized its "Basel 3.1" rulebook effective January 1, 2026, alongside a simplified regime for smaller domestic institutions.
These geographic divergences introduce regulatory arbitrage opportunities and booking model fragmentation across multinational investment banks.

## Learning objectives

- Map the implementation timelines and legislative instruments across the European Union (CRR3), the United States (Basel III Endgame), and the United Kingdom (Basel 3.1).
- Identify key jurisdictional deviations from the BCBS baseline, including EU corporate CVA exemptions and transitional output floor arrangements.
- Analyze the US Basel III Endgame evolution from the initial July 2023 Notice of Proposed Rulemaking (NPR) to the September 2024 re-proposal.
- Quantify cross-border capital disparities for identical derivative and credit portfolios under divergent EU versus US regulatory treatments.
- Contrast the Collins Amendment dual-stack requirement in the United States with European and British single-stack capital frameworks.
- Evaluate the strategic implications of cross-border regulatory arbitrage on global bank booking models and legal entity structures.

## Core concepts

### 1. Jurisdictional Comparison Matrix

```
+---------------------------------------------------------------------------------------------------+
| Feature               | European Union (CRR3)       | United States (Endgame)   | United Kingdom (Basel 3.1)|
+---------------------------------------------------------------------------------------------------+
| Effective Date        | January 1, 2025             | Mid-2025 to 2026 (Phased) | January 1, 2026           |
| Primary Legislation   | CRR3 / CRD VI               | Dodd-Frank Joint Rule     | PRA Policy Statements     |
| Scope                 | All credit institutions     | Category I-IV (> $100B)   | All PRA-regulated banks   |
| Output Floor Path     | 50% (2025) -> 72.5% (2030)  | 72.5% (Phased transition) | 50% (2026) -> 72.5% (2030)|
| CVA Exemptions        | Preserved (Sovereigns, NFCs)| No exemptions (Full SA)   | Narrowed exemptions       |
| Credit Models         | Retains F-IRB and A-IRB     | Eliminates internal credit| Retains F-IRB and A-IRB   |
| Capital Framework     | Single stack + Output Floor | Dual stack (Standardized  | Single stack + Output     |
|                       |                             | vs Expanded ERBA)         | Floor                     |
+---------------------------------------------------------------------------------------------------+
```

### 2. European Union: CRR3 and CRD VI

The European Parliament and Council finalized CRR3 in May 2024, taking effect on January 1, 2025:
- **Unrated Corporate Transitional Treatment:** Because European corporate borrowers rely on bank loans rather than public debt ratings, an unrated corporate with an internal PD equivalent to investment grade receives a favorable transitional risk weight of $65\%$ (rather than $100\%$) through 2032.
- **Preservation of CVA Exemptions:** The EU retained historical exemptions from CVA capital charges for derivative transactions with non-financial corporates (NFCs), sovereigns, and pension funds to protect hedging costs for the real economy.
- **FRTB Implementation Postponement:** To maintain parity with US delays, the European Commission postponed the mandatory market risk own funds requirement (FRTB SA/IMA) from January 2025 to January 2026, while keeping FRTB reporting requirements active.

### 3. United States: Basel III Endgame

In July 2023, the Fed, FDIC, and OCC issued a joint NPR targeting large banks ($>\$100\text{B}$ in assets).
Key flashpoints and the September 2024 re-proposal:
- **Capital Impact Scaling:** The original NPR was projected to increase aggregate Tier 1 common capital requirements by approximately $16\%$ to $19\%$ for G-SIBs. The 2024 re-proposal narrowed this increase to approximately $9\%$.
- **Elimination of Internal Models for Credit Risk:** The US framework completely eliminates internal ratings-based (A-IRB) approaches for credit risk, forcing large banks to use the new Expanded Risk-Based Approach (ERBA), a standardized framework.
- **The Collins Amendment Dual-Stack:** Under Dodd-Frank Section 171, US banks must compute their capital requirements under two distinct stacks:
  1. Standardized Approach (Pillar 1 minimum).
  2. Expanded Risk-Based Approach (ERBA).
  The binding capital constraint is whichever stack produces the higher RWA.
- **Operational Risk Internal Loss Multiplier (ILM):** The re-proposal neutralized the ILM to $1.0$ (neutral historical loss scaling) or allowed banks to base it purely on business volume rather than punitive historical loss history.

### 4. United Kingdom: PRA Basel 3.1

The PRA finalized its Basel 3.1 policy via PS9/24 and PS17/24:
- **Implementation Date:** Set to January 1, 2026, aligning closely with international counterparts.
- **Transitional Floor:** 5-year phase-in: $50\%$ in 2026, $55\%$ in 2027, $60\%$ in 2028, $65\%$ in 2029, and reaching the terminal $72.5\%$ in 2030.
- **Strong and Simple Regime:** Established the Small Domestic Deposit Takers (SDDT) regime, exempting non-systemic, domestically focused UK banks from complex Basel 3.1 rules while maintaining prudential soundness.

### 5. Cross-Border Arbitrage and Booking Models

Disparities in local rules incentivize multinational financial institutions to optimize booking models:
- **CVA Carve-Outs:** Booking over-the-counter (OTC) derivative hedges with uncollateralized corporate clients in an EU legal entity rather than a US broker-dealer to avoid heavy CVA capital charges.
- **Trading Desk Relocations:** Aligning internal risk-booking models with jurisdictions offering delayed FRTB capital enforcement or more favorable market risk parameters.

## Worked examples

### Example 1: Cross-Border CVA Capital Disparity (EU vs. US Booking Entity)

A global investment bank negotiates an uncollateralized 5-year Interest Rate Swap (IRS) with a European airline (a non-financial corporate without an external credit rating):
- Netting Set Mark-to-Market Value: $\$10\text{ million}$
- Notional: $\$250\text{ million}$
- SA-CCR EAD: $\$18,500,000$
- Effective Maturity ($M$): $3.5\text{ years}$
- Supervisory Risk Weight ($RW$ for unrated airline / BBB- proxy): $1.4\%$
- Discount Factor ($\alpha$): $0.5$

#### Option A: Booked in Paris (EU Subsidiary under CRR3)
- Under CRR3 Article 382, transactions with Non-Financial Counterparties (NFCs) entering derivatives for hedging purposes are explicitly **exempt** from CVA capital requirements.
- CVA Capital Charge: $\$0.00$
- CVA RWA: $\$0.00$
- CVA Capital Cost (at 10% hurdle rate on CET1): $\$0.00$

#### Option B: Booked in New York (US Subsidiary under US Basel III Endgame)
- Under the US Basel III Endgame, there are **no exemptions** for commercial end-users, non-financial corporates, or sovereigns.
- The bank must compute CVA capital under the Basic Approach for CVA (BA-CVA) or Standardized CVA (SA-CVA).
- Applying Reduced BA-CVA:

$$K_{\text{CVA}} = \alpha \times RW \times M \times \text{EAD} = 0.5 \times 0.014 \times 3.5 \times \$18,500,000$$
$$K_{\text{CVA}} = 0.0245 \times \$18,500,000 = \$453,250$$

- CVA Risk-Weighted Assets:

$$\text{RWA}_{\text{CVA}} = 12.5 \times \$453,250 = \$5,665,625$$

- Required CET1 Capital (assuming 12.0% total CET1 target):

$$\text{Required Capital} = 12.0\% \times \$5,665,625 = \$679,875$$

- Annual Capital Drag (at 12% cost of capital):

$$\text{Annual Drag} = 12\% \times \$679,875 = \$81,585\text{ per year}$$

Conclusion:
Booking the trade in the US legal entity imposes an immediate $\$679,875$ capital commitment and $\$81,585$ annual drag that does not exist in the EU.
The bank's structuring desk will route the transaction through its European entity to preserve client pricing competitiveness.

### Example 2: US Collins Amendment Dual-Stack Evaluation

A US Category II bank evaluates its credit portfolio under the dual-stack regime:
- Total Standardized Approach RWA (Stack 1): $\$500,000\text{ million}$
- Total Expanded Risk-Based Approach (ERBA) RWA (Stack 2):
  - Credit Risk (Standardized ERBA): $\$410,000\text{ million}$
  - Market Risk (FRTB SA): $\$45,000\text{ million}$
  - Operational Risk (SMA): $\$60,000\text{ million}$
  - Total ERBA RWA: $\$410,000 + \$45,000 + \$60,000 = \$515,000\text{ million}$

The bank holds $\$60,000\text{ million}$ of Tier 1 Common Equity (CET1).

Capital Ratios:
- Standardized Approach Ratio: $\frac{\$60,000}{\$500,000} = 12.00\%$
- ERBA Ratio: $\frac{\$60,000}{\$515,000} = 11.65\%$

Binding Determination:
- Under Dodd-Frank Section 171, the bank's binding capital ratio is the lower ratio ($11.65\%$), which corresponds to the higher RWA stack ($\$515,000\text{ million}$).
- If market volatility temporarily drops market risk RWA to $\$25,000\text{ million}$, total ERBA RWA becomes $\$495,000\text{ million}$.
- In that scenario, Stack 1 becomes binding at $\$500,000\text{ million}$, preventing the bank from benefiting from the reduction in ERBA RWA.

## Pitfalls

- **Assuming Global Parity in CVA Exemptions:** Assuming that European exemptions for corporate hedging apply in the US or UK causes severe undercapitalization on US-booked derivatives.
- **Ignoring the US Collins Floor:** When modeling RWA optimization for US banks, analysts frequently optimize only ERBA without realizing that the Standardized Approach acts as a non-diversifiable hard floor.
- **Overlooking Transitional Phase-In Schedules:** Output floors do not jump to $72.5\%$ immediately on day one; they step up annually from $50\%$ to $72.5\%$ over a 5-year horizon, altering medium-term capital planning.
- **Neglecting Extraterritoriality in Risk Models:** Cross-border banks operating in London, New York, and Frankfurt must maintain dual-reporting engines running local variations of SA-CCR and FRTB simultaneously.
- **Assuming Internal Models Are Dead Globally:** While the US eliminated internal models for credit risk under ERBA, the EU and UK retained Advanced and Foundation IRB, maintaining substantial modeling advantages for European banks.

## Interview questions

> [!question]- reg-19-01 | What is the Collins Amendment, and how does it affect US capital adequacy?
> Enacted under Section 171 of the Dodd-Frank Act, the Collins Amendment mandates that capital requirements for large US banking organizations cannot be less than the generally applicable Standardized Approach.
> This forces US institutions to maintain a dual-stack calculation where the Standardized Approach forms an immovable regulatory capital floor.

> [!question]- reg-19-02 | How does the EU CRR3 treat unrated corporate exposures differently from the BCBS baseline?
> Under BCBS rules, unrated corporates receive a $100\%$ risk weight under the Standardized Approach.
> CRR3 introduces a transitional period through 2032 allowing banks to apply a favorable $65\%$ risk weight to unrated corporate borrowers if their internal credit assessment corresponds to an investment-grade PD.

> [!question]- reg-19-03 | Why did the European Union preserve CVA capital exemptions under CRR3?
> The EU preserved CVA exemptions for transactions with non-financial corporates, sovereigns, and pension funds to prevent derivative hedging costs from escalating for corporate borrowers and public entities, protecting real-economy commercial financing.

> [!question]- reg-19-04 | What is the Small Domestic Deposit Takers (SDDT) regime in the UK?
> The SDDT regime (part of the PRA's "Strong and Simple" framework) exempts smaller, domestic-focused UK banks from complex Basel 3.1 standards.
> It replaces them with a streamlined, conservative capital regime that reduces compliance costs while ensuring safety.

> [!question]- reg-19-05 | What major change did the US Federal Reserve introduce in its September 2024 Basel III Endgame re-proposal regarding operational risk?
> The Fed neutralized the Internal Loss Multiplier (ILM) to $1.0$ (or allowed banks to calculate operational risk without punitive historical loss multipliers), substantially reducing the operational risk capital surcharge that was heavily criticized in the initial 2023 NPR.

> [!question]- reg-19-06 | How does the implementation timeline for FRTB market risk differ between the EU and the US?
> Both jurisdictions delayed mandatory FRTB own funds requirements.
> The EU postponed capital compliance to January 2026 while maintaining FRTB reporting requirements, aligning with US delays to maintain a level playing field for global trading desks.

> [!question]- reg-19-07 | What is the primary difference in credit risk modeling permitted between the EU and US Basel III finalization?
> The EU and UK retained internal ratings-based approaches (A-IRB and F-IRB) with revised input floors.
> The US completely abolished internal models for credit risk in large banks, forcing institutions to rely exclusively on the standardized Expanded Risk-Based Approach (ERBA).

> [!question]- reg-19-08 | What is the phase-in schedule for the Basel III output floor?
> The output floor phases in over five years:
> Year 1: $50\%$
> Year 2: $55\%$
> Year 3: $60\%$
> Year 4: $65\%$
> Year 5: $72.5\%$ terminal floor.

> [!question]- reg-19-09 | How does regulatory fragmentation lead to booking model restructuring in multinational investment banks?
> Differences in capital rules (such as EU CVA exemptions or differential treatment of equity exposures) lead multinational banks to establish specialized booking hubs.
> Transactions are executed in jurisdictions with the lowest capital consumption and back-to-back hedged internally.

> [!question]- reg-19-10 | What is the threshold for a bank to be subject to the US Basel III Endgame rules?
> The rules apply to Category I through IV banking organizations with total consolidated assets of $\$100\text{ billion}$ or more, significantly expanding the scope beyond only the largest G-SIBs.

## Further reading

- European Banking Authority. *Opinion on the implementation of the Basel III framework in the EU*. EBA/Op/2023/12.
- Board of Governors of the Federal Reserve System. *Statement on Basel III Endgame Re-proposal*. Press Release, September 2024.
- Prudential Regulation Authority. *Implementation of the Basel 3.1 standards*. Bank of England Policy Statements PS9/24 and PS17/24.
- Institute of International Finance. *Global Harmonization and Basel III Implementation*. IIF Policy Brief, 2024.
