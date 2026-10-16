---
type: concept
track: [quant-research, quant-dev]
tier: advanced
status: draft
prereqs: [swaps-and-curve-building, money-markets-repo-and-overnight-rates]
est_hours: 5
sources: [Piterbarg - Funding beyond discounting collateral agreements and derivatives pricing Risk 2010, Ametrano and Bianchetti - Everything you always wanted to know about multiple interest rate curve bootstrapping, Bianchetti - Two curves one price Risk 2010, BIS - Covered interest parity lost understanding the cross-currency basis BIS Quarterly Review 2016]
---

# Multi-Curve and CSA Discounting

> [!info] Draft
> Written in this session with computed examples matching `code/curve_bootstrap.py`.
> Missing for `solid`: formal independent reviewer check of all equations and parameter citations.

## TL;DR

- Collateralized transactions posted under a Credit Support Annex (CSA) must be discounted at the interest rate paid on posted cash collateral, known as the collateral rate.
- For standard collateralized derivatives, the discount curve is the overnight index swap (OIS) curve, while floating reference rates require distinct forwarding curves for each tenor.
- The dual-curve par swap rate is $S = \frac{\sum_{i=1}^n \tau_i P_{\text{disc}}(0, T_i) F_{\text{proj}}(0; T_{i-1}, T_i)}{\sum_{j=1}^m \tau_j P_{\text{disc}}(0, T_j)}$.
- Tenor basis swaps exchange one floating tenor for another in the same currency plus a spread, reflecting credit risk, liquidity premium, and roll risk across tenors.
- Cross-currency basis swaps exchange floating interest across currencies; deviations from Covered Interest Parity manifest as a non-zero basis spread driven by imbalances in US dollar funding demand and regulatory balance-sheet constraints.

## Learning objectives

- Explain the theoretical rationale for OIS/collateral discounting following Piterbarg (2010).
- Price an interest rate swap in a dual-curve framework where discounting and forwarding curves diverge.
- Value tenor basis swaps and explain why 3-month versus 6-month basis spreads widened historically.
- Derive the mark-to-market mechanics of cross-currency basis swaps and identify the structural causes of Covered Interest Parity violations.
- Price collateral currency choice as an embedded cheapest-to-deliver option in multi-currency CSAs.

## Core concepts

### Why collateral determines the discount curve

Prior to 2008, quantitative finance assumed a single yield curve served simultaneously as the discount curve for present values and the projection curve for future reference rates.
Vladimir Piterbarg (2010) formalized the modern pricing framework: a derivative contract whose replacement value is continuously collateralized in cash must be discounted at the rate paid on that collateral.
Consider a derivative with market value $V_t$.
Under a zero-threshold daily variation margin CSA, the out-of-the-money party posts cash collateral equal to $V_t$.
The in-the-money party holds this cash and pays interest on it at the contractually agreed collateral rate $c_t$.
By self-financing replication, the holding of collateral offsets funding costs: the hedging portfolio requires only an investment of $V_t - C_t = 0$.
The growth rate of the risk-neutral numeraire is therefore dictated by $c_t$, forcing the discount factor to maturity $T$ to be
$$P_{\text{disc}}(t, T) = \mathbb{E}_t^{\mathbb{Q}^c}\left[ \exp\left( -\int_t^T c_u \, du \right) \right].$$
Because standard CSAs remunerate cash collateral at the central bank overnight rate (SOFR for USD, €STR for EUR, SONIA for GBP), the OIS curve is the unique risk-neutral discount curve for collateralized cash flows.

### Dual-curve swap valuation

When the floating reference rate $L$ has a distinct tenor (such as 3-month or 6-month term rates), future fixings cannot be assumed to earn the overnight collateral rate.
The market separates the discount curve $P_{\text{disc}}(0, t)$ from the index-specific projection curve $P_{\text{proj}}(0, t)$.
The projected forward rate over $[T_{i-1}, T_i]$ with accrual fraction $\tau_i$ is
$$F_{\text{proj}}(0; T_{i-1}, T_i) = \frac{1}{\tau_i} \left( \frac{P_{\text{proj}}(0, T_{i-1})}{P_{\text{proj}}(0, T_i)} - 1 \right).$$
The present value of the floating leg discounted at the collateral rate is
$$PV_{\text{float}} = N \sum_{i=1}^n \tau_i P_{\text{disc}}(0, T_i) F_{\text{proj}}(0; T_{i-1}, T_i).$$
Because $P_{\text{proj}} \neq P_{\text{disc}}$, the product $P_{\text{disc}}(0, T_i) F_{\text{proj}}(0; T_{i-1}, T_i)$ no longer simplifies to $P_{\text{disc}}(0, T_{i-1}) - P_{\text{disc}}(0, T_i)$.
The floating leg fails to telescope, and the dual-curve par swap rate becomes
$$S_{\text{dual}} = \frac{\sum_{i=1}^n \tau_i P_{\text{disc}}(0, T_i) F_{\text{proj}}(0; T_{i-1}, T_i)}{\sum_{j=1}^m \tau_j P_{\text{disc}}(0, T_j)} = \frac{\sum_{i=1}^n \tau_i P_{\text{disc}}(0, T_i) F_{\text{proj}}(0; T_{i-1}, T_i)}{A_{\text{disc}}(0, T_m)}.$$

### Tenor basis swaps

A tenor basis swap exchanges one floating tenor for another in the same currency, such as 3-month floating versus 6-month floating.
One leg pays the reference rate flat, while the other leg pays the reference rate plus a quoted basis spread $\beta_{3v6}$:
$$\sum_{i=1}^{n_3} \tau_i^{(3)} P_{\text{disc}}(0, T_i^{(3)}) \left( F_3(T_{i-1}^{(3)}, T_i^{(3)}) + \beta_{3v6} \right) = \sum_{j=1}^{n_6} \tau_j^{(6)} P_{\text{disc}}(0, T_j^{(6)}) F_6(T_{j-1}^{(6)}, T_j^{(6)}).$$
Tenor basis spreads exist because lending for 6 months unsecured entails greater credit risk, term liquidity risk, and rollover uncertainty than lending for two consecutive 3-month periods.

### Cross-currency swaps and covered interest parity failure

A standard cross-currency basis swap (XCCY) exchanges floating interest payments in two different currencies on agreed principal amounts.
Principal is exchanged at the prevailing spot foreign exchange rate $S_0$ at inception and returned at the same spot rate at maturity.
In standard market convention, the USD leg pays SOFR flat, while the non-USD leg pays its floating rate (e.g., 3-month Euribor or €STR) plus a cross-currency basis spread $\beta_{\text{XCCY}}$.
Under classical Covered Interest Parity (CIP), no-arbitrage between spot and forward foreign exchange dictates that $\beta_{\text{XCCY}} = 0$.
Post-2008, CIP failed systematically, with $\beta_{\text{XCCY}}$ trading persistently negative for major currencies versus the US dollar (e.g., EUR, JPY).
A negative spread means the party that swaps EUR into USD receives the EUR rate minus $|\beta_{\text{XCCY}}|$ on its EUR while paying SOFR flat, so non-US borrowers pay a premium to borrow US dollars synthetically.
The persistent basis is driven by heavy global demand for US dollar assets, coupled with bank balance sheet constraints under Basel III (the leverage ratio and liquidity coverage ratio) that penalize arbitrageurs for intermediating currency flows.

### Collateral currency choice and cheapest-to-deliver optionality

Many legacy and multi-currency CSAs permit the collateral posting party to choose among several eligible currencies (e.g., USD, EUR, GBP, JPY).
If cash collateral is posted in currency $k$, it earns the overnight rate $c_t^{(k)}$.
The posting party naturally selects the currency that minimizes its economic cost, creating an embedded cheapest-to-deliver (CTD) collateral option:
$$c_t^{\text{eff}} = \max_k \left( c_t^{(k)} - \text{cost of funding currency } k \right).$$
Valuing derivatives under a multi-currency CSA requires pricing this collateral switching option, which raises the effective discount rate, lowers effective discount factors, and lowers derivative asset values.

### How it is implemented

- Inputs: OIS discount curves per currency, tenor projection curves, tenor basis spreads, cross-currency basis curves, CSA agreements.
- Outputs: collateral-adjusted discount curves, projected forwards, net present values, currency-specific sensitivities.
- Algorithm: construct OIS curves from overnight instruments; bootstrap tenor curves from vanilla and basis swaps; calibrate cross-currency discount curves to match XCCY quotes.
- Complexity: $O(K \cdot N)$ where $K$ is the number of curves and $N$ is the number of instruments in the global bootstrap.
- Reference implementation: [`code/curve_bootstrap.py`](code/curve_bootstrap.py) provides `par_swap_rate_dual_curve`.
- System context: [the curve and surface service](../18-Pricing-and-Risk-Systems/04-Curve-and-Surface-Service.md).

## Worked examples

All calculations below match the verified assertions in `code/curve_bootstrap.py`.

### Example 1: dual-curve par swap rate vs single-curve rate

Consider a 2-year annual swap where:
OIS discount factors: $P_{\text{ois}}(1) = \frac{1}{1 + 0.030} = 0.970874$ and $P_{\text{ois}}(2) = \frac{1 - 0.035 \times 0.970874}{1.035} = 0.933352$.
OIS annuity: $A_{\text{ois}} = 0.970874 + 0.933352 = 1.904226$.
The single-curve OIS par swap rate is:
$$S_{\text{single}} = \frac{1 - P_{\text{ois}}(2)}{A_{\text{ois}}} = \frac{1 - 0.933352}{1.904226} = \frac{0.066648}{1.904226} = 3.5000\%.$$
Now suppose the floating leg references a term index whose annual forwarding zero rates sit 20 bp above the OIS par rates ($3.0\%$ and $3.5\%$) as a credit and liquidity spread:
$P_{\text{proj}}(1) = \frac{1}{1 + 0.032} = 0.968992 \implies F(0, 1) = \frac{1}{0.968992} - 1 = 3.2000\%$.
$P_{\text{proj}}(2) = \frac{1}{(1 + 0.037)^2} = 0.929913 \implies F(1, 2) = \frac{0.968992}{0.929913} - 1 = 4.2024\%$.

Calculate floating leg present value discounted at OIS:
$$\text{Coupon 1 PV} = \tau_1 \cdot P_{\text{ois}}(1) \cdot F(0, 1) = 1.0 \times 0.970874 \times 0.032000 = 0.031068.$$
$$\text{Coupon 2 PV} = \tau_2 \cdot P_{\text{ois}}(2) \cdot F(1, 2) = 1.0 \times 0.933352 \times 0.042024 = 0.039223.$$
$$PV_{\text{float}} = 0.031068 + 0.039223 = 0.070291.$$

The dual-curve par swap rate is:
$$S_{\text{dual}} = \frac{PV_{\text{float}}}{A_{\text{ois}}} = \frac{0.070291}{1.904226} = 3.6913\%.$$
Dual-curve pricing adds $3.6913\% - 3.5000\% = 19.13\text{ bps}$ to the fixed swap rate relative to the pure OIS rate.

### Example 2: valuing a tenor basis swap

Consider a 1-year tenor basis swap exchanging 3-month floating for 6-month floating.
Assume flat OIS discounting at $3.00\%$ continuous: $P(0, t) = e^{-0.03 t}$.
$P(0.25) = 0.992528$, $P(0.50) = 0.985112$, $P(0.75) = 0.977751$, $P(1.00) = 0.970446$.
Quarterly OIS annuity: $A_4 = 0.25 \times (0.992528 + 0.985112 + 0.977751 + 0.970446) = 0.981459$.
Semiannual OIS annuity: $A_2 = 0.50 \times (0.985112 + 0.970446) = 0.977779$.
Suppose the forward rates projected from respective curves are:
Quarterly 3M forwards: $F_3 = [3.20\%, 3.30\%, 3.40\%, 3.50\%]$.
Semiannual 6M forwards: $F_6 = [3.45\%, 3.65\%]$.
Present value of 3-month leg without spread:
$$PV_3 = 0.25 \times [0.992528(0.032) + 0.985112(0.033) + 0.977751(0.034) + 0.970446(0.035)] = 0.032870.$$
Present value of 6-month leg:
$$PV_6 = 0.50 \times [0.985112(0.0345) + 0.970446(0.0365)] = 0.034704.$$
The 3-month versus 6-month par basis spread $\beta_{3v6}$ added to the 3-month leg is:
$$\beta_{3v6} = \frac{PV_6 - PV_3}{A_4} = \frac{0.034704 - 0.032870}{0.981459} = \frac{0.001834}{0.981459} = 0.1869\% = 18.69\text{ bps}.$$

### Example 3: cross-currency swap pricing and synthetic dollar borrowing

A European bank borrows $100{,}000{,}000$ USD for 1 year via a mark-to-market cross-currency swap against EUR.
Current spot FX rate is $S_0 = 1.1000$ USD per EUR, so the bank posts $100{,}000{,}000 / 1.1000 = 90{,}909{,}091$ EUR.
The EUR/USD cross-currency basis spread is $\beta_{\text{XCCY}} = -25\text{ bps}$, quoted on the EUR leg.
The bank pays USD SOFR flat on the borrowed dollars and receives €STR plus the basis on its EUR: $3.50\% + (-0.25\%) = 3.25\%$.
If the bank funds its EUR at €STR ($3.50\%$), it loses $25\text{ bps}$ on the EUR leg, so its all-in cost of the synthetic dollars is SOFR $+ 25\text{ bps}$.
That $25\text{ bps}$ is the premium the USD-hungry European bank pays for dollar funding.
Conversely, a USD holder that swaps dollars into EUR pays only €STR $- 25\text{ bps}$ on the EUR it receives, so investing that EUR at €STR earns SOFR $+ 25\text{ bps}$ hedged back into dollars.

### Example 4: real-world case, covered interest parity failure during the 2020 dash for cash

In March 2020, as the COVID-19 pandemic triggered global financial turmoil, foreign corporations and financial institutions faced acute US dollar cash shortages, and the EUR/USD and JPY/USD cross-currency bases moved sharply negative.
Dealers could not fully arbitrage the gap because leverage-based capital rules, such as the Supplementary Leverage Ratio (SLR), made it costly to expand balance sheets for cross-currency and FX forward trades.
The Federal Reserve cut the price of its standing dollar swap lines with five central banks on 15 March 2020 and opened temporary swap lines with nine more on 19 March 2020, supplying dollars through foreign central banks, after which the basis narrowed (source: Federal Reserve press releases of 15 and 19 March 2020).

## Pitfalls

- Discounting uncollateralized or corporate cash flows at the OIS rate without an explicit Credit Valuation Adjustment (CVA).
- Ignoring collateral currency: discounting a EUR swap at the USD SOFR rate when collateral is posted exclusively in EUR.
- Assuming cross-currency basis is zero in cross-border valuation, causing errors of tens of basis points in foreign exchange forwards.
- Rebuilding all curves simultaneously with iterative solvers instead of respecting the hierarchy: OIS first, then tenor basis, then cross-currency.
- Neglecting the mark-to-market reset mechanism in modern cross-currency swaps, which rebalances principal periodically and removes currency-induced counterparty exposure.

## Interview questions

> [!question]- fi-piterbarg-collateral-discount | Explain Piterbarg's (2010) core argument for why derivative cash flows must be discounted at the collateral rate.
> A daily cash-collateralized position requires zero unsecured financing because the collateral received or posted exactly matches the contract value.
> The replication portfolio grows at the contractual interest rate paid on that collateral, forcing that rate to be the risk-neutral discounting rate.

> [!question]- fi-dual-curve-par-swap-formula | Write the formula for the dual-curve par swap rate and identify why the floating leg fails to telescope.
> $S = \frac{\sum \tau_i P_{\text{disc}}(0, T_i) F_{\text{proj}}(0; T_{i-1}, T_i)}{\sum \tau_j P_{\text{disc}}(0, T_j)}$.
> Telescoping fails because $F_{\text{proj}}(0; T_{i-1}, T_i) = \frac{1}{\tau_i}\left(\frac{P_{\text{proj}}(0, T_{i-1})}{P_{\text{proj}}(0, T_i)} - 1\right)$ involves projection discount factors that do not cancel out with collateral discount factors $P_{\text{disc}}$.

> [!question]- fi-tenor-basis-spread-causes | Why is the 6-month reference rate higher than compounded consecutive 3-month reference rates over the same half-year?
> 6-month lending exposes the lender to greater borrower default risk over the longer uninterrupted period.
> It also incorporates term liquidity premia and the inability to call back or roll cash at the intermediate 3-month mark.

> [!question]- fi-cip-failure-drivers | What economic factors explain the persistent breakdown of Covered Interest Parity since 2008?
> Imbalance between massive global structural demand for US dollars and foreign currency supplies.
> Post-crisis bank regulation (e.g., Basel III leverage ratio) limits dealers from expanding balance sheets to arbitrate the gap.

> [!question]- fi-cross-currency-basis-sign | If the 5-year EUR/USD cross-currency basis spread is $-25$ bps, what interest rate does a party borrowing USD against EUR collateral pay?
> By convention the basis sits on the EUR leg: the party pays SOFR flat on the USD and receives the EUR rate minus 25 bps on its EUR.
> Relative to funding the EUR at the EUR rate, its all-in USD cost is SOFR plus 25 bps, the premium for synthetic dollar borrowing.

> [!question]- fi-cheapest-to-deliver-csa | How does an embedded collateral currency choice option affect the present value of a swap?
> The party posting collateral has the option to deliver whichever currency has the cheapest effective financing rate.
> This option has positive value to the poster and negative value to the receiver, lowering the net valuation of the derivative asset.

> [!question]- fi-mtm-xccy-mechanism | What is a mark-to-market (MTM) cross-currency swap and why was it adopted?
> In an MTM cross-currency swap, the non-base currency notional is periodically adjusted to match spot FX fluctuations, with a cash balancing settlement.
> This removes large accumulated foreign exchange exposure, reducing counterparty credit risk and capital requirements.

> [!question]- fi-dual-curve-spread-effect | If the forwarding zero rates sit 20 bps above the OIS par rates, how does the dual-curve par swap rate compare to the single-curve OIS swap rate?
> The dual-curve par swap rate is higher than the single-curve OIS rate by approximately the 20 bp spread.
> Higher projected floating cash flows require a higher fixed coupon to balance the swap at inception.

> [!question]- fi-ois-discounting-numeraire | What is the change of numeraire associated with moving from unsecured Libor discounting to OIS discounting?
> The numeraire shifts from an unsecured money market bank account to a secured money market account growing at the overnight collateral rate $c_t$.
> Forward rates remain martingales under their specific forward measures, but present values discount under the collateral measure $\mathbb{Q}^c$.

> [!question]- fi-curve-bootstrap-hierarchy | In what order must curves be bootstrapped in a modern multi-curve interest rate trading desk?
> 1. OIS discount curves per currency from overnight swaps.
> 2. Floating tenor projection curves from single-currency basis swaps.
> 3. Cross-currency discount curves from cross-currency basis swaps.

## Further reading

- Piterbarg, "Funding Beyond Discounting: Collateral Agreements and Derivatives Pricing", *Risk*, 2010.
- Ametrano and Bianchetti, *Everything You Always Wanted to Know About Multiple Interest Rate Curve Bootstrapping but Were Afraid to Ask*.
- Bianchetti, "Two Curves, One Price", *Risk*, 2010.
- Borio, McCauley, McGuire, and Sushko, "Covered Interest Parity Lost: Understanding the Cross-Currency Basis", *BIS Quarterly Review*, 2016.

## In this repo and SDE-Interview-Prep

- Code: [`code/curve_bootstrap.py`](code/curve_bootstrap.py) (`par_swap_rate_dual_curve`).
- Related notes: [Swaps and Curve Building](03-Swaps-and-Curve-Building.md), [Curve Construction Numerics](14-Curve-Construction-Numerics.md), [Money Markets, Repo and Overnight Rates](12-Money-Markets-Repo-and-Overnight-Rates.md).
