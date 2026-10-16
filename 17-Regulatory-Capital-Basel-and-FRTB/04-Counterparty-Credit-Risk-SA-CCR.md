---
type: concept
track: [quant-risk]
tier: core
status: draft
prereqs: [credit-risk-capital-sa-and-irb]
est_hours: 4
sources: [Basel Committee on Banking Supervision - The Standardised Approach for Measuring Counterparty Credit Risk Exposures (BCBS 279 2014), Basel Committee on Banking Supervision - Basel III: Finalising post-crisis reforms (2017), Jon Gregory - Counterparty Credit Risk and Credit Value Adjustment (2015), Michael Pykhtin and Steven Zhu - A Guide to Modeling Counterparty Credit Risk (2007)]
---

# Counterparty Credit Risk: SA-CCR

## TL;DR

The Standardised Approach for Counterparty Credit Risk (SA-CCR, Basel CRE52) replaced the obsolete Current Exposure Method (CEM) and Standardised Method (SM) for measuring bilateral OTC derivative exposures.
SA-CCR resolves the fundamental shortcomings of CEM by differentiating between margined and unmargined netting sets, recognizing economic netting and directional hedging within asset classes, and incorporating collateral thresholds and margin periods of risk.
Exposure at Default (EAD) is determined by scaling the sum of Replacement Cost (RC) and Potential Future Exposure (PFE) by a supervisory scalar $\alpha = 1.4$:
$$\text{EAD} = 1.4 \cdot (\text{RC} + \text{PFE})$$
Replacement Cost reflects instantaneous mark-to-market loss if the counterparty defaults today, accounting for collateral held, margin thresholds, and minimum transfer amounts.
Potential Future Exposure measures potential exposure expansion over a 1-year unmargined horizon or the Margin Period of Risk (MPOR) under collateralized CSAs.
PFE is calculated as the product of a non-linear collateral multiplier and an aggregate add-on across five derivative asset classes: Interest Rate (IR), Foreign Exchange (FX), Credit, Equity, and Commodity.

## Learning objectives

- Understand the historical drivers and systemic failure modes that led the Basel Committee to replace the Current Exposure Method (CEM) with SA-CCR.
- Formulate the Replacement Cost (RC) equations for unmargined and margined netting sets under bilateral Credit Support Annexes (CSAs).
- Derive the non-linear PFE collateral multiplier and evaluate its asymptotic behavior under deep in-the-money and out-of-the-money collateralization.
- Calculate supervisory duration, adjusted notional, and maturity factors ($MF$) across margined and unmargined trades.
- Construct supervisory hedging sets and evaluate intra-bucket and inter-bucket correlation aggregation across interest rate maturity buckets.
- Trace the role of the supervisory multiplier $\alpha = 1.4$ and its historical calibration to the Internal Model Method (IMM).
- Contrast SA-CCR with the Internal Model Method (IMM) for calculating Effective Expected Positive Exposure (EEPE).

## Core concepts

### The transition from CEM to SA-CCR

Under the 1988 Basel I accord, banks computed counterparty credit exposure using the Current Exposure Method (CEM):
$$\text{EAD}_{\text{CEM}} = \max(V, 0) + \text{AddOn}_{\text{gross}} \cdot \left(0.4 + 0.6 \cdot \text{NGR}\right)$$
CEM suffered from critical structural flaws:
1. It failed to differentiate between margined and unmargined counterparties, treating daily cash-collateralized hedge funds identically to uncollateralized sovereigns.
2. It measured directional risk poorly; opposite payer and receiver swap positions within the same currency could not offset gross notionals, creating absurdly punitive capital charges for balanced market-making books.
3. The supervisory add-on factors were fixed percentage scalars calibrated in the 1980s that ignored the duration of long-dated interest rate swaps.
4. CEM gave zero mathematical recognition to collateral thresholds, independent amounts, or Minimum Transfer Amounts (MTA).
In 2014, the Basel Committee finalized SA-CCR (BCBS 279), effective globally as part of the post-crisis Basel III and Basel IV reforms (CRE52).

### The master EAD equation

Under SA-CCR, Exposure at Default for a given netting set is defined as:
$$\text{EAD} = \alpha \cdot (\text{RC} + \text{PFE})$$
where $\alpha = 1.4$.
The scalar $\alpha = 1.4$ carries over from the Basel II Internal Model Method (IMM).
It was calibrated by Picoult, Canabarro, and Duffie to capture model risk, systemic correlation across counterparty exposures, extreme wrong-way risk, and the gap between unhedged portfolio variance and single-factor portfolio assumptions.

### Replacement Cost (RC)

Replacement Cost represents the current loss exposure if the counterparty defaulted immediately.

#### Unmargined netting sets
For netting sets without a bilateral margin agreement:
$$\text{RC} = \max(V - C, 0)$$
where $V$ is the current mark-to-market portfolio value (positive from the bank's perspective), and $C$ is the net collateral currently held by the bank (cash and securities, adjusted for supervisory haircuts).

#### Margined netting sets
For netting sets governed by a bilateral Credit Support Annex (CSA) with daily or periodic variation margin:
$$\text{RC} = \max(V - C, \text{TH} + \text{MTA} - \text{NICA}, 0)$$
where:
- $\text{TH}$ is the bilateral threshold above which the counterparty must post variation margin.
- $\text{MTA}$ is the Minimum Transfer Amount below which collateral calls are not executed.
- $\text{NICA}$ is the Net Independent Collateral Amount (initial margin or independent amount posted by the counterparty minus independent amount posted by the bank).
The term $\text{TH} + \text{MTA} - \text{NICA}$ captures the largest uncollateralized exposure the bank can legally face before a margin call is triggered under the contract.

### Potential Future Exposure (PFE) and the multiplier

Potential Future Exposure captures the risk of adverse market price movements over the exposure horizon:
$$\text{PFE} = \text{Multiplier} \cdot \text{AddOn}^{\text{aggregate}}$$
The aggregate add-on $\text{AddOn}^{\text{aggregate}}$ is the sum of the asset class add-ons:
$$\text{AddOn}^{\text{aggregate}} = \sum_{a \in \{\text{IR}, \text{FX}, \text{Credit}, \text{Equity}, \text{Commodity}\}} \text{AddOn}^{(a)}$$

The non-linear PFE multiplier recognizes excess collateral (over-collateralization) held by the bank:
$$\text{Multiplier} = \min\left(1.0, 0.05 + 0.95 \cdot \exp\left(\frac{V - C}{2 \cdot 0.95 \cdot \text{AddOn}^{\text{aggregate}}}\right)\right)$$
Key properties of the multiplier:
1. If $V \ge C$ (uncollateralized or under-collateralized), the exponential term is $\ge 1.0$, and the multiplier hits its cap of $1.0$.
2. If $C > V$ (over-collateralized), $V - C < 0$, causing the exponential term to decay towards zero.
3. The multiplier is bounded below by a hard supervisory floor of $0.05$ (5%).
Even if a counterparty posts billions of dollars in excess initial margin, the bank cannot reduce its PFE add-on below 5%, ensuring minimum capital coverage against extreme tail gap risk and market illiquidity during close-out.

### Trade-level adjusted notional and supervisory delta

Each derivative transaction $i$ is converted into an effective supervisory exposure:
$$D_i = d_i \cdot \delta_i \cdot MF_i$$
where:
- $d_i$ is the supervisory adjusted notional.
- $\delta_i$ is the supervisory delta.
- $MF_i$ is the maturity factor.

#### Adjusted notional for interest rate derivatives
Because long-dated interest rate swaps have greater duration and price sensitivity than short-dated swaps, the adjusted notional scales nominal notional $N_i$ by supervisory duration:
$$d_i = N_i \cdot \frac{e^{-0.05 \cdot S_i} - e^{-0.05 \cdot E_i}}{0.05}$$
where $S_i$ is the start time in years ($S_i = 0$ for spot-starting swaps), and $E_i$ is the end time in years.
For all other asset classes (FX, Equity, Credit), $d_i = N_i$ (converted to domestic base currency).

#### Supervisory delta ($\delta_i$)
- Plain vanilla linear derivatives (swaps, forwards, futures):
  - Long instrument / receive floating / pay fixed: $\delta_i = +1.0$.
  - Short instrument / pay floating / receive fixed: $\delta_i = -1.0$.
- Non-linear derivatives (options):
  - Computed using the standard Black-Scholes formula with prescribed supervisory volatilities $\sigma_j$ (e.g., $\sigma_{\text{IR}} = 50\%$, $\sigma_{\text{FX}} = 15\%$, $\sigma_{\text{Equity}} = 120\%$).
  - Long call / short put: $\delta_i > 0$.
  - Long put / short call: $\delta_i < 0$.

#### Maturity factor ($MF_i$)
- Unmargined transactions:
  $$MF_i^{\text{unmargined}} = \sqrt{\frac{\min(M_i, 1.0)}{1.0}}$$
  where $M_i$ is the residual maturity in years, floored at 10 business days ($10/250 = 0.04$).
  For any trade with residual maturity $M_i \ge 1.0$ year, $MF = 1.0$.
- Margined transactions:
  $$MF_i^{\text{margined}} = 1.5 \cdot \sqrt{\frac{\text{MPOR}}{250}}$$
  where $\text{MPOR}$ is the Margin Period of Risk in business days.
  For centrally cleared netting sets, the regulatory minimum MPOR is 10 days ($MF = 1.5 \times \sqrt{10/250} = 1.5 \times 0.2 = 0.30$).
  For non-centrally cleared netting sets with more than 5,000 trades, the supervisory MPOR floor is 20 days ($MF = 1.5 \times \sqrt{20/250} \approx 0.424$).

### Asset class hedging sets and correlation aggregation

#### Interest rate derivatives
Interest rate derivatives in the same currency belong to a single hedging set.
Trades are divided into three maturity buckets based on end time $E_i$:
- Bucket 1: $E_i \le 1\text{ year}$
- Bucket 2: $1\text{ year} < E_i \le 5\text{ years}$
- Bucket 3: $E_i > 5\text{ years}$
Within each bucket $b$, the effective notional is the algebraic sum of adjusted positions:
$$D_{j, b} = \sum_{i \in \text{Bucket } b} d_i \cdot \delta_i \cdot MF_i$$
The bucket add-on is $A_{j, b} = SF_{\text{IR}} \cdot |D_{j, b}|$, where $SF_{\text{IR}} = 0.50\%$.
The aggregate interest rate add-on combines buckets using prescribed supervisory correlations:
$$\rho_{12} = 0.70, \quad \rho_{23} = 0.70, \quad \rho_{13} = 0.30$$
$$\text{AddOn}_{\text{IR}} = \sqrt{A_1^2 + A_2^2 + A_3^2 + 1.4 A_1 A_2 + 1.4 A_2 A_3 + 0.6 A_1 A_3}$$
Because opposite positions within the same bucket offset fully ($\pm 1$), while positions across buckets offset partially via the correlation matrix, SA-CCR accurately captures curve slope and basis risk.

#### Foreign exchange derivatives
Each currency pair forms a distinct hedging set.
The supervisory factor is $SF_{\text{FX}} = 4.0\%$.
Within each currency pair, all trades offset directionally:
$$\text{AddOn}_{\text{FX}, k} = SF_{\text{FX}} \cdot \left| \sum_{i \in \text{Pair } k} d_i \cdot \delta_i \cdot MF_i \right|$$
The total FX add-on is the simple sum across all currency pairs:
$$\text{AddOn}_{\text{FX}} = \sum_k \text{AddOn}_{\text{FX}, k}$$

### Supervisory factors summary table

| Asset Class | Sub-class / Rating | Supervisory Factor ($SF$) | Supervisory Volatility ($\sigma$) |
| :--- | :--- | :--- | :--- |
| **Interest Rate** | All currencies | 0.50% | 50% |
| **Foreign Exchange** | All currency pairs | 4.00% | 15% |
| **Credit Single Name** | AAA / AA | 0.38% | 100% |
| **Credit Single Name** | A | 0.42% | 100% |
| **Credit Single Name** | BBB | 0.54% | 100% |
| **Credit Single Name** | BB | 1.06% | 100% |
| **Credit Single Name** | B / CCC | 1.60% / 6.00% | 100% |
| **Credit Index** | Investment Grade / High Yield | 0.38% / 1.06% | 80% |
| **Equity Single Name** | Large Cap / Small Cap | 20.0% / 32.0% | 120% |
| **Equity Index** | Developed / Emerging | 16.0% / 24.0% | 75% |
| **Commodity** | Energy / Metals / Agriculture | 18.0% - 40.0% | 70% - 150% |

### Regulatory text map

- **CRE50**: Counterparty credit risk - Overview and scope of application.
- **CRE51**: Counterparty credit risk - Definitions and qualifying criteria for netting agreements.
- **CRE52**: Standardised approach for counterparty credit risk (SA-CCR) - Detailed methodology, replacement cost formulas, hedging sets, and supervisory factors.
- **CRE53**: Internal Model Method (IMM) for counterparty credit risk - EPE/EEPE simulation, 1-year stressed effective EPE, backtesting, and validation.

### How it is implemented

The reference function `calculate_saccr` accepts a netting set with trades, margin status, MTM, collateral, and CSA parameters.
Its trade model supports interest-rate and FX asset classes, with notional, supervisory delta, start/end times, residual maturity, and an optional currency pair.
It calculates RC, IR and FX add-ons, PFE, and EAD; it does not parse trade schemas or calculate credit, equity, or commodity add-ons.
The implementation pools IR trades into three maturity buckets and aggregates FX trades by currency pair; FX notionals are used as supplied, with no currency conversion.
These implementation limits do not change the broader regulatory methodology described in this topic.

## Worked examples

### Example 1: Unmargined interest rate swap netting set

Consider an uncollateralized netting set with a commercial counterparty containing two USD interest rate swaps (verified in `code/basel_credit_saccr.py`):
- Current portfolio mark-to-market: $V = \$200,000$
- Current collateral: $C = \$0$
- Contract type: Unmargined bilateral agreement

**Trade 1: 5-Year Payer Swap**
- Notional $N_1 = \$10,000,000$
- Direction: Payer (pay fixed, receive floating) $\to \delta_1 = +1.0$
- Start time $S_1 = 0.0\text{ years}$, End time $E_1 = 5.0\text{ years}$, Maturity $M_1 = 5.0\text{ years}$

**Trade 2: 2-Year Receiver Swap**
- Notional $N_2 = \$10,000,000$
- Direction: Receiver (receive fixed, pay floating) $\to \delta_2 = -1.0$
- Start time $S_2 = 0.0\text{ years}$, End time $E_2 = 2.0\text{ years}$, Maturity $M_2 = 2.0\text{ years}$

**Step 1: Replacement Cost**
$$\text{RC} = \max(V - C, 0) = \max(\$200,000 - \$0, 0) = \$200,000.00$$

**Step 2: Adjusted notional and maturity factors**
Supervisory duration factors:
$$\text{Factor}_1 = \frac{e^{-0.05 \cdot 0} - e^{-0.05 \cdot 5.0}}{0.05} = \frac{1 - e^{-0.25}}{0.05} = \frac{1 - 0.778801}{0.05} = \frac{0.221199}{0.05} = 4.423984$$
$$\text{Factor}_2 = \frac{e^{-0.05 \cdot 0} - e^{-0.05 \cdot 2.0}}{0.05} = \frac{1 - e^{-0.10}}{0.05} = \frac{1 - 0.904837}{0.05} = \frac{0.095163}{0.05} = 1.903252$$
Adjusted notionals:
$$d_1 = \$10,000,000 \cdot 4.423984 = \$44,239,843.40$$
$$d_2 = \$10,000,000 \cdot 1.903252 = \$19,032,516.40$$
Because the contract is unmargined and $M \ge 1.0$:
$$MF_1 = \sqrt{\frac{\min(5.0, 1.0)}{1.0}} = 1.0, \quad MF_2 = \sqrt{\frac{\min(2.0, 1.0)}{1.0}} = 1.0$$

**Step 3: Bucket assignment and effective notionals**
- Trade 1 has $E_1 = 5.0\text{ years} \to \text{Bucket 2}$ ($1 < E \le 5$):
  $$D_2 = d_1 \cdot \delta_1 \cdot MF_1 = +\$44,239,843.40$$
- Trade 2 has $E_2 = 2.0\text{ years} \to \text{Bucket 2}$ ($1 < E \le 5$):
  $$D_2 \text{ addition} = d_2 \cdot \delta_2 \cdot MF_2 = -\$19,032,516.40$$
Net effective notional in Bucket 2:
$$D_{\text{Bucket 2}} = \$44,239,843.40 - \$19,032,516.40 = \$25,207,327.00$$
Buckets 1 and 3 are empty ($D_1 = 0, D_3 = 0$).

**Step 4: AddOn calculation**
The supervisory factor for interest rate derivatives is $SF_{\text{IR}} = 0.50\% = 0.0050$:
$$A_1 = 0, \quad A_2 = 0.0050 \cdot \$25,207,327.00 = \$126,036.635, \quad A_3 = 0$$
Evaluating inter-bucket aggregation:
$$\text{AddOn}_{\text{IR}} = \sqrt{A_2^2} = A_2 = \$126,036.635 \approx \$126,036.64$$

**Step 5: Multiplier and PFE**
Here $V - C = \$200,000 > 0$:
$$\text{Exponent} = \frac{\$200,000}{2 \cdot 0.95 \cdot \$126,036.635} = \frac{200,000}{239,469.61} = 0.835179$$
$$\exp(0.835179) = 2.305228$$
$$\text{Multiplier} = \min(1.0, 0.05 + 0.95 \cdot 2.305228) = \min(1.0, 2.239967) = 1.000000$$
The multiplier is capped at 1.0:
$$\text{PFE} = 1.000000 \cdot \$126,036.635 = \$126,036.64$$

**Step 6: Exposure at Default**
$$\text{EAD} = 1.4 \cdot (\text{RC} + \text{PFE}) = 1.4 \cdot (\$200,000.00 + \$126,036.64) = 1.4 \cdot \$326,036.64 = \$456,451.29$$

### Example 2: Margined interest rate swap netting set

Consider the identical swap portfolio from Example 1, but governed by a bilateral variation margin agreement (CSA):
- Mark-to-market: $V = \$200,000$
- Posted collateral: $C = \$180,000$
- Collateral threshold: $\text{TH} = \$50,000$
- Minimum Transfer Amount: $\text{MTA} = \$10,000$
- Independent collateral: $\text{NICA} = \$0$
- Margin Period of Risk: $\text{MPOR} = 10\text{ business days}$

**Step 1: Margined Replacement Cost**
$$\text{RC} = \max(V - C, \text{TH} + \text{MTA} - \text{NICA}, 0)$$
$$V - C = \$200,000 - \$180,000 = \$20,000$$
$$\text{TH} + \text{MTA} - \text{NICA} = \$50,000 + \$10,000 - \$0 = \$60,000$$
$$\text{RC} = \max(\$20,000, \$60,000, 0) = \$60,000.00$$
The threshold plus MTA term dominates because the bank is contractually exposed to uncollateralized swings up to $\$60,000$ before calling margin.

**Step 2: Margined maturity factor**
For daily margined netting sets with $\text{MPOR} = 10\text{ days}$:
$$MF^{\text{margined}} = 1.5 \cdot \sqrt{\frac{10}{250}} = 1.5 \cdot \sqrt{0.04} = 1.5 \cdot 0.20 = 0.300000$$

**Step 3: Margined AddOn calculation**
Effective notional in Bucket 2:
$$D_{\text{Bucket 2}} = (\$44,239,843.40 - \$19,032,516.40) \cdot 0.30 = \$25,207,327.00 \cdot 0.30 = \$7,562,198.10$$
$$\text{AddOn}_{\text{IR}} = 0.0050 \cdot \$7,562,198.10 = \$37,810.99$$

**Step 4: Margined multiplier and PFE**
$$V - C = \$20,000$$
$$\text{Exponent} = \frac{\$20,000}{2 \cdot 0.95 \cdot \$37,810.99} = \frac{20,000}{71,840.88} = 0.278393$$
$$\exp(0.278393) = 1.321027$$
$$\text{Multiplier} = \min(1.0, 0.05 + 0.95 \cdot 1.321027) = 1.000000$$
$$\text{PFE} = 1.000000 \cdot \$37,810.99 = \$37,810.99$$

**Step 5: Margined EAD**
$$\text{EAD} = 1.4 \cdot (\$60,000.00 + \$37,810.99) = 1.4 \cdot \$97,810.99 = \$136,935.39$$
Collateralizing the portfolio reduces total EAD from $\$456,451.29$ to $\$136,935.39$, achieving a 70.0% capital reduction.

### Example 3: The Archegos collapse and non-linear counterparty exposures

In March 2021, family office Archegos Capital Management defaulted on total return swaps (TRS) linked to highly concentrated equity positions (ViacomCBS, Discovery, Baidu), imposing $\$10\text{ billion}$ in losses across global prime brokers (Credit Suisse, Nomura, Morgan Stanley).
Several prime brokers utilized legacy counterparty credit metrics or granted zero-threshold, low-initial-margin CSAs based on competitive pressure.
Under standard SA-CCR rules:
- Single-stock equities carry a punitive supervisory factor of $SF = 32\%$ for small-cap / volatile names and supervisory volatility $\sigma = 120\%$.
- Directional equity swaps do not offset unless they reference the identical legal entity.
- If prime brokers had rigorously enforced SA-CCR capital charges into trade pricing (via KVA), the capital required to hold $\$50\text{ billion}$ of gross synthetic equity exposures without liquid collateral would have forced margin requirements exceeding 25-35%.
Instead, prime brokers held static collateral of only 10-15%, failed to model liquidation horizon expansion beyond standard 10-day MPORs for concentrated positions, and suffered catastrophic losses when multi-billion dollar liquidations crashed equity market prices.

## Pitfalls

- **Neglecting the CSA threshold in margined RC**: Calculating margined Replacement Cost simply as $\max(V - C, 0)$ and forgetting $\text{TH} + \text{MTA} - \text{NICA}$ understates exposure when positive thresholds exist.
- **Assuming full offset between cross-currency swaps**: Cross-currency basis swaps involve exchange of principal at maturity; in SA-CCR, the FX legs must be separated from the IR legs and allocated to the FX hedging set, creating substantial FX add-on charges.
- **MPOR floor violations under disputed margin calls**: If a counterparty has a history of disputing margin calls or settlement delays, supervisory rules mandate doubling the Margin Period of Risk from 10 days to 20 days, which scales margined $MF$ by $\sqrt{2} \approx 1.414$.
- **Ignoring non-linear option delta sensitivity**: Using simple nominal notional for deep out-of-the-money options overstates capital; using unhedged linear approximations for near-the-money options understates gamma and tail jump risk.
- **Applying unmargined maturity factors to margined netting sets**: Unmargined trades scale with $\sqrt{\min(M, 1.0)}$, whereas margined trades scale with $1.5 \sqrt{\text{MPOR}/250}$; confusing the two formulas produces massive errors in regulatory capital reporting.

## Interview questions

> [!question]- reg-saccr-alpha-rationale | Why is Exposure at Default (EAD) in SA-CCR multiplied by the regulatory scalar $\alpha = 1.4$?
> The scalar $\alpha = 1.4$ was originally calibrated by David Canabarro, Darrell Duffie, and Joe Picoult during the design of the Basel II Internal Model Method (IMM).
> It reflects the ratio between a comprehensive credit portfolio economic capital measure and an unadjusted single-factor Expected Positive Exposure (EPE).
> Specifically, $\alpha$ compensates for:
> 1. Systemic correlation between exposure and counterparty creditworthiness (general wrong-way risk).
> 2. The non-Gaussian nature and severe fat-tailed skewness of multi-asset derivative exposure distributions.
> 3. Market volatility clustering and model risk inherent in standardized netting and add-on formulas.
> 4. The diversification benefit shortfall when aggregating across uncorrelated trading books in a stressed bank.

> [!question]- reg-saccr-pfe-multiplier-asymptotics | What are the asymptotic limits of the SA-CCR PFE multiplier, and what economic reality does each limit represent?
> The PFE multiplier is given by:
> $$\text{Multiplier} = \min\left(1.0, 0.05 + 0.95 \cdot \exp\left(\frac{V - C}{2 \cdot 0.95 \cdot \text{AddOn}^{\text{aggregate}}}\right)\right)$$
> - Upper limit ($1.0$): When $V \ge C$, the exponential argument is non-negative, the exponential term is $\ge 1.0$, and the multiplier is capped at $1.0$. This represents an uncollateralized or under-collateralized netting set where current exposure is fully unhedged.
> - Lower limit ($0.05$): When the counterparty posts vast amounts of excess collateral ($C \gg V$), $V - C \to -\infty$, and the exponential term approaches zero, driving the multiplier to its supervisory floor of $0.05$ (5%).
> This 5% floor reflects residual tail risk: no matter how much collateral is posted, there is always non-zero gap risk, margin dispute risk, settlement failure, and market illiquidity during the liquidation period.

> [!question]- reg-saccr-supervisory-duration-derivation | Why does SA-CCR define the adjusted notional for interest rate swaps using an exponential discount formula rather than simple contractual maturity?
> The adjusted notional is defined as:
> $$d_i = N_i \cdot \frac{e^{-0.05 \cdot S_i} - e^{-0.05 \cdot E_i}}{0.05}$$
> This formula represents the standard continuous bond price sensitivity (duration) under an assumed flat continuous yield of 5%.
> Because an interest rate swap's DV01 (dollar value of an 01) is proportional to its modified duration rather than its nominal principal, a 30-year swap has much greater market risk than a 2-year swap with the same notional.
> The term $\frac{1 - e^{-0.05 T}}{0.05}$ caps the effective duration as $T \to \infty$ at $1 / 0.05 = 20\text{ years}$, preventing perpetual or ultra-long swaps from generating unbounded regulatory capital requirements while accurately reflecting duration roll-down.

> [!question]- reg-saccr-ir-correlation-matrix | How does SA-CCR prevent basis and curve slope risk from being netted away in interest rate portfolios?
> SA-CCR divides interest rate trades in the same currency into three maturity buckets ($<1\text{ year}$, $1\text{ to } 5\text{ years}$, $>5\text{ years}$).
> Full algebraic netting ($\delta = \pm 1$) is permitted only within the same maturity bucket.
> Across buckets, effective notionals are aggregated using a supervisory correlation matrix:
> $$\rho_{12} = 0.70, \quad \rho_{23} = 0.70, \quad \rho_{13} = 0.30$$
> Because the correlations are strictly less than 1.0 (particularly $\rho_{13} = 0.30$ between short-term and long-term rates), opposite positions across different tenors (such as a 1-year receiver vs a 10-year payer) receive only partial offset.
> This ensures capital is held against curve steepening, flattening, and butterfly twists.

> [!question]- reg-margined-rc-th-mta-role | Explain why margined Replacement Cost includes the term $\text{TH} + \text{MTA} - \text{NICA}$.
> Under a collateralized CSA, variation margin is only transferred when the uncollateralized exposure exceeds the threshold $\text{TH}$ plus the Minimum Transfer Amount $\text{MTA}$.
> If a counterparty's mark-to-market rises from zero to $\text{TH} + \text{MTA} - \$1$, the bank cannot legally issue a margin call.
> If the counterparty defaults at that exact instant, the bank suffers an uncollateralized loss equal to that gap.
> Subtracting Net Independent Collateral Amount ($\text{NICA}$) reflects that any initial margin held permanently cushions this threshold gap.
> Therefore, the bank's operational replacement cost can never be lower than $\text{TH} + \text{MTA} - \text{NICA}$.

> [!question]- reg-saccr-vs-imm-methodology | What are the core technical differences between SA-CCR and the Internal Model Method (IMM) for counterparty credit risk?
> SA-CCR is an analytical, rules-based framework using supervisory duration, fixed volatility add-ons, and parametric correlation formulas evaluated on a single snapshot of portfolio data.
> IMM is an internal Monte Carlo simulation framework that:
> 1. Simulates thousands of joint multi-asset market risk paths over horizons up to 30 years using calibrated term-structure and volatility models.
> 2. Fully revalues every derivative contract across all paths and future time grids.
> 3. Generates the full profile of Expected Exposure ($EE(t)$) accounting for path-dependent collateralization and margin call dynamics.
> 4. Computes Effective Expected Positive Exposure (EEPE) by taking the non-decreasing envelope of $EE(t)$ and averaging over the first year.
> EAD under IMM is $1.4 \times \text{EEPE}$, which captures complex non-linear path-dependent payoffs that SA-CCR's static add-ons cannot.

> [!question]- reg-mpor-floors-basel-iv | What are the mandatory supervisory floors for the Margin Period of Risk (MPOR) under Basel guidelines?
> Under Basel CRE52:
> - Centrally cleared transactions with daily variation margin: minimum MPOR is 10 business days.
> - Bilateral (non-cleared) netting sets: standard minimum MPOR is 10 business days.
> - Bilateral netting sets with more than 5,000 transactions: minimum MPOR is 20 business days.
> - Netting sets containing illiquid collateral or exotic derivatives that cannot be easily re-hedged: minimum MPOR is 20 business days.
> - Netting sets with two or more margin call disputes in the preceding two quarters that lasted longer than the current MPOR: minimum MPOR is doubled (typically to 20 or 40 business days).

> [!question]- reg-saccr-fx-hedging-set-structure | How are cross-currency swaps treated across hedging sets in SA-CCR?
> A cross-currency swap involves both interest rate risk in two distinct currencies and foreign exchange risk.
> In SA-CCR, the contract must be mathematically bifurcated:
> 1. The interest rate legs are split into two separate single-currency interest rate transactions, each allocated to its respective currency's IR hedging set.
> 2. The exchange of principal (or synthetic FX forward exposure) is allocated to the FX hedging set corresponding to that specific currency pair.
> This prevents banks from hiding foreign exchange market risk within interest rate hedging sets.

> [!question]- reg-negative-mtm-impact-on-ead | Can a deeply out-of-the-money derivative portfolio have a zero EAD under SA-CCR?
> No.
> Even if a bank has a massively negative mark-to-market ($V \ll 0$) or holds massive collateral ($C \gg V$), Replacement Cost is floored at zero ($\text{RC} \ge 0$).
> Furthermore, while the negative mark-to-market reduces the PFE multiplier, the multiplier is bounded below by the supervisory floor of $0.05$ (5%).
> As long as the netting set contains open derivative positions, $\text{AddOn}^{\text{aggregate}} > 0$, guaranteeing:
> $$\text{EAD} \ge 1.4 \cdot (0 + 0.05 \cdot \text{AddOn}^{\text{aggregate}}) = 0.07 \cdot \text{AddOn}^{\text{aggregate}} > 0$$
> EAD can never be zero for open derivative contracts.

> [!question]- reg-credit-derivatives-in-saccr | How does SA-CCR handle single-name Credit Default Swaps (CDS) compared to index CDS?
> Single-name CDS and index CDS belong to the Credit asset class but are separated into distinct hedging sets:
> - Each single-name entity constitutes its own independent hedging set; long and short protection on the same reference entity offset, but positions across different reference entities do not offset.
> - Credit indices (e.g., CDX IG, iTraxx Europe) form separate hedging sets; an index position cannot be netted directly against single-name constituent CDS positions unless a strict supervisory decomposition is applied.
> Supervisory factors range from 0.38% (AAA/AA single name, IG index) to 6.00% (CCC single name), reflecting credit spread volatility.

## Further reading

- Basel Committee on Banking Supervision. *The standardised approach for measuring counterparty credit risk exposures*. BCBS 279, March 2014.
- Basel Committee on Banking Supervision. *Basel III: Finalising post-crisis reforms*. Bank for International Settlements, December 2017.
- Gregory, Jon. *Counterparty Credit Risk and Credit Value Adjustment: A Continuing Challenge for Global Financial Markets*. Wiley, 2nd edition, 2012.
- Canabarro, Eduardo, and Darrell Duffie. "Measuring and Marking Counterparty Risk." *Asset/Liability Management of Financial Institutions*, Institutional Investor Books, 2003.
- Pykhtin, Michael, and Steven Zhu. "A Guide to Modeling Counterparty Credit Risk." *GARP Risk Review*, July/August 2007.

## In this repo and SDE-Interview-Prep

- [03-Credit-Risk-Capital-SA-and-IRB.md](03-Credit-Risk-Capital-SA-and-IRB.md) - Standardised and IRB credit capital, Vasicek model, and output floors.
- [05-CVA-Capital-Charge-SA-CVA-and-BA-CVA.md](05-CVA-Capital-Charge-SA-CVA-and-BA-CVA.md) - Regulatory CVA capital framework and eligible CVA hedges.
- `code/basel_credit_saccr.py` - Reference implementation of selected SA-CCR calculations for margined and unmargined netting sets.
