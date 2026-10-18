---
type: concept
track: [quant-risk]
tier: advanced
status: solid
prereqs: [bcbs-239-risk-data-aggregation]
est_hours: 4
sources: [European Union - Capital Requirements Regulation III and Delegated Regulation (EU) 2025/1496, Federal Reserve Board - March 19 2026 capital proposals, UK Prudential Regulation Authority - PS1/26 Implementation of Basel 3.1 final rules, Basel Committee on Banking Supervision - Basel III Monitoring Report (2024)]
---

# Implementation Status by Jurisdiction

## TL;DR

While the Basel Committee on Banking Supervision (BCBS) establishes international regulatory capital benchmarks, individual sovereign jurisdictions enact them through domestic legislation.
This creates divergence across timelines, technical rules, and capital floors.
The European Union’s CRR3 has applied since January 1, 2025, with transitional treatments and a separate delay for FRTB market-risk own-funds requirements.
In the United States, the agencies issued new capital proposals on March 19, 2026; the proposal for the largest and most internationally active banks uses one calculation instead of the dual calculation in the 2024 re-proposal.
Those US proposals remain proposals, and the cited agency release gives no first-application date.
The UK PRA finalized Basel 3.1 in PS1/26, with most rules taking effect January 1, 2027 and the market-risk internal model approach taking effect January 1, 2028.
Differences in enacted rules, proposals, and implementation dates affect cross-border capital planning, but do not by themselves establish an arbitrage opportunity.

## Learning objectives

- Map the implementation timelines and legislative instruments across the European Union (CRR3), the United States (Basel III Endgame), and the United Kingdom (Basel 3.1).
- Identify key jurisdictional deviations from the BCBS baseline, including EU corporate CVA exemptions and transitional output floor arrangements.
- Distinguish the March 2026 US proposals from the earlier 2023 NPR and 2024 re-proposal, including the proposed single-calculation framework and the absence of a stated first-application date.
- Quantify cross-border capital disparities for identical derivative and credit portfolios under divergent EU versus US regulatory treatments.
- Compare the US agencies’ proposed single-calculation framework for the largest banks with the enacted EU and UK frameworks, while distinguishing proposals from effective rules.
- Evaluate the strategic implications of cross-border regulatory arbitrage on global bank booking models and legal entity structures.

## Core concepts

### 1. Jurisdictional Comparison Matrix

```
+---------------------------------------------------------------------------------------------------+
| Feature               | European Union (CRR3)       | United States (March 2026 proposal) | United Kingdom (Basel 3.1)|
+---------------------------------------------------------------------------------------------------+
| Status / date         | CRR3 applies from Jan 1, 2025 | March 19, 2026 proposals; no first-application date stated | Most rules Jan 1, 2027; market-risk IMA Jan 1, 2028 |
| Legal basis / status | CRR3 / CRD VI                | Existing rules; March 2026 agency proposal | PRA Rulebook / PS1/26 |
| Scope                 | CRR3 institutions            | Largest internationally active banks; others may opt in | PRA-regulated firms in scope |
| Output Floor Path     | Transitional CRR3 schedule   | Proposal; see draft rules for transition | Transitional schedule begins 2027; 72.5% terminal floor |
| CVA Exemptions        | CRR3 treatment applies       | Proposal details govern; not final | Basel 3.1 treatment applies |
| Credit Models         | Retains F-IRB and A-IRB     | Proposed standardized credit-risk approaches | Retains F-IRB and A-IRB   |
| Capital Framework     | CRR3 rules + output floor    | March 2026 proposal: one calculation for largest banks | Basel 3.1 rules + output floor |
+---------------------------------------------------------------------------------------------------+
```

### 2. European Union: CRR3 and CRD VI

CRR3 has applied since January 1, 2025.
Relevant market-risk timing was subsequently changed by Commission Delegated Regulation (EU) 2025/1496:
- **Unrated Corporate Transitional Treatment:** Because European corporate borrowers rely on bank loans rather than public debt ratings, an unrated corporate with an internal PD equivalent to investment grade receives a favorable transitional risk weight of $65\%$ (rather than $100\%$) through 2032.
- **Preservation of CVA Exemptions:** The EU retained historical exemptions from CVA capital charges for derivative transactions with non-financial corporates (NFCs), sovereigns, and pension funds to protect hedging costs for the real economy.
- **FRTB Own-Funds Application:** Delegated Regulation (EU) 2025/1496 defers the application of FRTB market-risk own-funds requirements to January 1, 2027.
  Until then, the prior CRR market-risk framework continues to apply.

### 3. United States: Basel III Endgame

On March 19, 2026, the Fed, FDIC, and OCC requested comment on new capital proposals.
The proposal primarily for the largest, most internationally active banks would use one rather than two sets of calculations for risk-based capital requirements; other banks could elect to adopt it, and the market-risk component would apply only to banks with significant trading activity.
- **Proposal status:** These remain proposed rules, not effective requirements.
  The comment period closed June 18, 2026; the agencies’ announcement does not state a first-application date.
- **Earlier proposals:** The July 2023 NPR and September 2024 re-proposal are historical stages, not the current proposal.
  Do not present the 2024 dual-calculation design, impact estimates, or operational-risk calibration as the current proposed framework.
- **Credit risk models:** The March 2026 proposal continues to eliminate internal models for credit risk, as described in the agency statements; the details remain subject to the proposed rule and any final action.

### 4. United Kingdom: PRA Basel 3.1

The PRA published final Basel 3.1 rules in PS1/26.
- **Implementation dates:** Most rules take effect January 1, 2027; the market-risk internal model approach (IMA) takes effect January 1, 2028.
- **Transitional floor:** The output floor transition is aligned to the delayed implementation, reaching the terminal $72.5\%$ in 2032.
- **Strong and Simple Regime:** The PRA has finalized a simplified capital regime for Small Domestic Deposit Takers (SDDTs), with its own scope and requirements.

### 5. Cross-Border Arbitrage and Booking Models

Disparities in local rules incentivize multinational financial institutions to optimize booking models:
- **CVA Differences:** Jurisdiction-specific CVA scope and exemptions can affect the capital treatment of OTC derivatives; determine the applicable enacted rule for each entity and counterparty before drawing a booking conclusion.
- **Trading Desk Relocations:** Implementation timing and market-risk approaches differ, including the EU 2027 own-funds date and UK 2028 IMA date; verify applicable local rules rather than assuming a general capital advantage.

## Worked examples

### Example 1: Illustrative CVA Calculation Under Assumed Rules

This calculation is an illustrative comparison of assumed treatments, not a statement of the current US proposal or a recommendation to book a trade in a particular entity.
A global bank models an uncollateralized 5-year Interest Rate Swap (IRS) with a European airline (a non-financial corporate without an external credit rating):
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

#### Option B: Assumed treatment for a separate entity
- For this arithmetic illustration only, assume the applicable rules require a CVA capital calculation and that the entity uses the reduced BA-CVA formula below.
- This assumed calculation does not establish the treatment under the March 2026 US proposal, which is not yet final.
- Applying Reduced BA-CVA:

$$K_{\text{CVA}} = \alpha \times RW \times M \times \text{EAD} = 0.5 \times 0.014 \times 3.5 \times \$18,500,000$$
$$K_{\text{CVA}} = 0.0245 \times \$18,500,000 = \$453,250$$

- CVA Risk-Weighted Assets:

$$\text{RWA}_{\text{CVA}} = 12.5 \times \$453,250 = \$5,665,625$$

- Required CET1 Capital (assuming 12.0% total CET1 target):

$$\text{Required Capital} = 12.0\% \times \$5,665,625 = \$679,875$$

- Annual Capital Drag (at 12% cost of capital):

$$\text{Annual Drag} = 12\% \times \$679,875 = \$81,585\text{ per year}$$

Under these assumptions, the calculated capital requirement is $\$679,875$ and annual drag is $\$81,585$.
Actual entity-level treatment depends on the rules in force and the transaction facts; this example alone does not support a booking recommendation.

### Example 2: Effect of the March 2026 US Single-Calculation Proposal

The March 2026 proposal for the largest, most internationally active banks would replace the 2024 proposal’s two-calculation design with one calculation for risk-based capital compliance.
The following arithmetic is only a contrast with a hypothetical two-calculation design, not a description of a current or proposed binding US requirement:
- Total Standardized Approach RWA (Stack 1): $\$500,000\text{ million}$
- Total Expanded Risk-Based Approach (ERBA) RWA (Stack 2):
  - Credit Risk (Standardized ERBA): $\$410,000\text{ million}$
  - Market Risk (FRTB SA): $\$45,000\text{ million}$
  - Operational Risk (SMA): $\$60,000\text{ million}$
  - Total ERBA RWA: $\$410,000 + \$45,000 + \$60,000 = \$515,000\text{ million}$

Assume solely for this illustration that the bank holds $\$60,000\text{ million}$ of CET1.

Capital Ratios:
- Standardized Approach Ratio: $\frac{\$60,000}{\$500,000} = 12.00\%$
- ERBA Ratio: $\frac{\$60,000}{\$515,000} = 11.65\%$

Under a hypothetical rule requiring both calculations, the higher RWA would be $\$515,000\text{ million}$.
The March 2026 proposal instead describes one calculation for the covered banks, so the maximum-of-two-stacks determination above is not a description of that proposal.
The agencies’ release does not specify a first-application date.

## Pitfalls

- **Assuming Global Parity in CVA Exemptions:** Assuming that an exemption in one jurisdiction applies in another can understate capital; check the current rule and counterparty facts for each entity.
- **Confusing US proposal stages:** The 2024 re-proposal described two calculations; the March 2026 proposal for the largest banks describes one.
  Keep proposal history separate from current binding requirements.
- **Overlooking Transitional Phase-In Schedules:** Output floors do not jump to $72.5\%$ immediately on day one; check the local transition dates and percentages when modeling medium-term capital requirements.
- **Neglecting Extraterritoriality in Risk Models:** Cross-border banks operating in London, New York, and Frankfurt must maintain dual-reporting engines running local variations of SA-CCR and FRTB simultaneously.
- **Confusing Proposed and Effective Credit Rules:** The March 2026 US proposal uses standardized credit-risk approaches for covered banks, while the EU and UK Basel 3.1 rules retain IRB approaches subject to restrictions.
  Keep the US proposal distinct from effective requirements.

## Interview questions

> [!question]- reg-19-01 | How does the March 2026 US proposal change the calculation design?
> Section 171 of the Dodd-Frank Act establishes a statutory capital floor.
> Separately, the March 2026 proposal for the largest, most internationally active banks would use one rather than two sets of calculations for risk-based capital compliance.
> It is a proposal, and the agency announcement does not state a first-application date.

> [!question]- reg-19-02 | How does the EU CRR3 treat unrated corporate exposures differently from the BCBS baseline?
> Under BCBS rules, unrated corporates receive a $100\%$ risk weight under the Standardized Approach.
> CRR3 introduces a transitional period through 2032 allowing banks to apply a favorable $65\%$ risk weight to unrated corporate borrowers if their internal credit assessment corresponds to an investment-grade PD.

> [!question]- reg-19-03 | Why did the European Union preserve CVA capital exemptions under CRR3?
> The EU preserved CVA exemptions for transactions with non-financial corporates, sovereigns, and pension funds to prevent derivative hedging costs from escalating for corporate borrowers and public entities, protecting real-economy commercial financing.

> [!question]- reg-19-04 | What is the Small Domestic Deposit Takers (SDDT) regime in the UK?
> The SDDT regime (part of the PRA's "Strong and Simple" framework) exempts smaller, domestic-focused UK banks from complex Basel 3.1 standards.
> It replaces them with a streamlined, conservative capital regime that reduces compliance costs while ensuring safety.

> [!question]- reg-19-05 | What is the status of the US capital proposals issued in March 2026?
> The agencies issued proposals on March 19, 2026, and the comment period closed June 18, 2026.
> The proposal for the largest, most internationally active banks uses one rather than two sets of risk-based capital calculations.
> The announcement does not state a first-application date.

> [!question]- reg-19-06 | How does the implementation timeline for FRTB market risk differ between the EU and the US?
> The EU deferred FRTB market-risk own-funds application to January 1, 2027 under Delegated Regulation (EU) 2025/1496.
> The US March 2026 proposal includes market-risk requirements for banks with significant trading activity, but the agencies’ release does not state an application date.

> [!question]- reg-19-07 | How do credit risk approaches differ across the EU, UK, and March 2026 US proposal?
> The EU and UK Basel 3.1 frameworks retain foundation and advanced IRB approaches subject to revised requirements.
> The March 2026 US proposal uses standardized credit-risk approaches for the covered banks; it remains a proposal and has no first-application date in the agencies’ announcement.

> [!question]- reg-19-08 | What is the phase-in schedule for the Basel III output floor?
> The output floor phases in over five years:
> Year 1: $50\%$
> Year 2: $55\%$
> Year 3: $60\%$
> Year 4: $65\%$
> Year 5: $72.5\%$ terminal floor.

> [!question]- reg-19-09 | How does regulatory fragmentation lead to booking model restructuring in multinational investment banks?
> Differences in capital rules can affect booking and legal-entity decisions, but a capital difference alone does not determine the appropriate booking location.
> Banks must assess applicable rules, transaction facts, and supervisory requirements for each entity.

> [!question]- reg-19-10 | What is the application date for the US proposals issued in March 2026?
> The agencies’ March 19, 2026 announcement does not state a first-application date.
> Any application date depends on subsequent final rules.

## Further reading

- European Banking Authority. *Opinion on the implementation of the Basel III framework in the EU*. EBA/Op/2023/12.
- Federal Reserve Board, FDIC, and OCC. *Agencies request comment on proposals to modernize the regulatory capital framework*. March 19, 2026.
- Prudential Regulation Authority. *Implementation of Basel 3.1: Final rules*. Policy Statement PS1/26, January 2026.
- Institute of International Finance. *Global Harmonization and Basel III Implementation*. IIF Policy Brief, 2024.

## In this repo and SDE-Interview-Prep

- 01-Capital-RWA-and-the-Basel-Framework.md - Basel framework structure and output floor.
- 05-CVA-Capital-Charge-SA-CVA-and-BA-CVA.md - CVA capital charge methodologies.
- 06-FRTB-Trading-and-Banking-Book-Boundary.md - Trading and banking book boundary rules.
- `code/basel_stress_reg.py` - Reference implementation verifying cross-border CVA and US single-calculation proposals.

