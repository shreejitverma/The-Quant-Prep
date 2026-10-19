---
type: problem-set
track: [quant-risk]
tier: core
status: solid
prereqs: [capital-aware-trading-kva-and-rwa-limits]
est_hours: 4
sources: [Basel Framework RBC20 RBC30 RBC40 RBC90 CAP30 CRE20 CRE31 CRE32 CRE52 CRE54 MAR22 MAR31 MAR32 MAR33 MAR50 OPE25 LCR40 LEV20 LEV40 (versions published on bis.org - read 2026-10-16), Directive 2013/36/EU (CRD) Article 104a(4) and Article 141, 12 CFR 225.8(f)(2), Jon Gregory - The xVA Challenge 4th edition - Wiley (2020)]
---

# Regulatory Capital Problem Set

## TL;DR

- Capital adequacy is a stack: Pillar 1 minima of 4.5% CET1, 6% Tier 1 and 8% total (RBC20.1), Pillar 2 requirements, then buffers (conservation 2.5%, countercyclical, G-SIB) that trigger distribution limits rather than breaches.
- RWA is the higher of nominated-approach RWA and 72.5% of all-standardised RWA (RBC20.4), phased in from 50% in 2023 to 72.5% in 2028 (RBC90.1).
- The formulas interviewers ask you to run by hand: the IRB ASRF capital (CRE31.5), SA-CCR EAD (CRE52), BA-CVA (MAR50.14), the SMA BIC and ILM (OPE25), LCR run-offs (LCR40) and the SCB (12 CFR 225.8).
- Two worked problems (an output-floor capital stack and an SA-CCR margined versus unmargined netting set) and 27 cards; every number is computed by the section code.

## Learning objectives

- Calculate complete bank regulatory capital stacks including CET1, Tier 1, Total Capital, and all supervisory buffers.
- Apply the output floor to internal ratings-based (IRB) and internal models approach (IMA) institutions.
- Derive capital requirements for corporate credit exposures using the Vasicek asymptotic single risk factor model.
- Compute counterparty credit risk EAD for complex derivative netting sets under SA-CCR across margined and unmargined agreements.
- Aggregate multi-currency market risk capital under the FRTB Sensitivities-Based Method across low, medium, and high correlation regimes.
- Quantify operational risk capital under the Standardised Measurement Approach (SMA) and evaluate liquidity and IRRBB compliance.

## Core concepts

### Capital stack

| Layer | Requirement | Source |
| :--- | :--- | :--- |
| Pillar 1 | CET1 4.5%, Tier 1 6.0%, total 8.0% of RWA | RBC20.1 |
| Pillar 2 requirement (EU) | bank-specific; at least 56.25% in CET1 and 75% in Tier 1 | CRD Article 104a(4) |
| Conservation buffer | 2.5% CET1 | RBC30 |
| Countercyclical buffer | 0% to 2.5% CET1 for reciprocity purposes, higher at national discretion | RBC30 |
| G-SIB higher loss absorbency | 1.0% to 3.5% CET1 by bucket | RBC40 |
| Leverage | Tier 1 at least 3% of exposure, plus 50% of the G-SIB requirement for G-SIBs | LEV20.7, LEV40.2 |

Falling into the buffer zone limits distributions in four equal bands (RBC30.4); in the EU the combined buffer sits above P1 and P2R, and the MDA applies when it is not met (CRD Article 141).

### Output floor

$$
\text{RWA} = \max\left(\text{RWA}_{\text{nominated}},\; f \times \text{RWA}_{\text{SA}}\right),
\qquad f = 72.5\% \text{ from 1 January 2028},
$$

with $f$ stepping through 50%, 55%, 60%, 65% and 70% from 2023 (RBC90.1) and an optional 25% cap on the increase during the phase-in (RBC90.2).
The base uses the standardised approaches listed in RBC20.11, including the SA for market risk and SA-CCR for counterparty risk.

### IRB ASRF formula (CRE31.5)

$$
K = \left[LGD \cdot \Phi\left(\frac{\Phi^{-1}(PD) + \sqrt{R}\,\Phi^{-1}(0.999)}{\sqrt{1-R}}\right) - PD \cdot LGD\right] \cdot \frac{1 + (M - 2.5)\,b}{1 - 1.5\,b},
\qquad b = (0.11852 - 0.05478 \ln PD)^2,
$$

with corporate $R$ between 12% and 24% decreasing in PD, and $\text{RWA} = 12.5 \times K \times \text{EAD}$.

### SA-CCR (CRE52)

$$
\text{EAD} = 1.4\,(\text{RC} + \text{PFE}),
\qquad
\text{PFE} = \min\left(1,\; 0.05 + 0.95\, e^{(V - C)/(2 \times 0.95 \times \text{AddOn})}\right) \times \text{AddOn}.
$$

IR effective notional per currency: $\sqrt{D_1^2 + D_2^2 + D_3^2 + 1.4 D_1 D_2 + 1.4 D_2 D_3 + 0.6 D_1 D_3}$ over maturity buckets (under 1 year, 1 to 5 years, over 5 years), with $D_i = \delta_i \times N_i \times SD_i \times MF_i$ and supervisory factor 0.5%.

### FRTB SbM aggregation (MAR21.4 to MAR21.6)

$$
K_b = \sqrt{\sum_k WS_k^2 + \sum_{k \ne l} \rho_{kl} WS_k WS_l},
\qquad
\text{Delta} = \sqrt{\sum_b K_b^2 + \sum_{b \ne c} \gamma_{bc} S_b S_c},
$$

computed under medium, high ($\min(1.25\rho, 1)$) and low ($\max(2\rho - 1, 0.75\rho)$) correlations, with the largest result taken.

## Worked examples

### Problem 1: output floor and the capital stack

A bank (USD millions) reports nominated-approach RWA of credit 280,000 (A-IRB), market 35,000 (IMA), operational 45,000 (SMA) and CVA capital of 10,000, which is $12.5 \times 10{,}000 = 125{,}000$ of RWA, total 485,000.
All-standardised RWA: credit 420,000, market 55,000, operational 45,000, CVA $12.5 \times 16{,}000 = 200{,}000$, total 720,000.
Capital: CET1 44,000, AT1 6,000, Tier 2 8,000.
Requirements: Pillar 1 minima, P2R 1.5% (EU split: 56.25% CET1, 75% Tier 1), conservation 2.5%, G-SIB 1.5%, CCyB 0.5%, floor fully phased in.

1. Floor: $0.725 \times 720{,}000 = 522{,}000 > 485{,}000$, so binding RWA is 522,000, up 37,000 or 7.63%.
2. Targets: CET1 $4.5\% + 1.5\% \times 56.25\% + 2.5\% + 1.5\% + 0.5\% = 9.84375\%$ (the P2R CET1 piece is 0.84375%); Tier 1 $6\% + 1.125\% + 4.5\% = 11.625\%$; total $8\% + 1.5\% + 4.5\% = 14.0\%$.
3. Ratios at 522,000: CET1 8.43%, Tier 1 9.58%, total 11.11%.
4. Gaps: CET1 $-1.41\%$ or $-7{,}384.4$; Tier 1 $-10{,}682.5$; total $-15{,}080$.
5. Before the floor the ratios were 9.07%, 10.31% and 11.96%: the bank already missed its targets, and the floor deepens the gap; it needs 51,384.4 of CET1 to meet the CET1 target at the floor.

The answer an interviewer wants: name which constraint binds (here all three, total capital worst), and that raising AT1 or Tier 2 fixes the Tier 1 and total gaps but not the CET1 gap.

### Problem 2: SA-CCR, margined versus unmargined

A netting set with a hedge fund, all USD swaps starting today: trade 1 receive fixed 100m 5 years (MtM +2.5m), trade 2 pay fixed 50m 10 years (MtM -1.8m), trade 3 receive fixed 80m 2 years (MtM +0.3m).
Delta convention: +1 when long the primary risk factor (rates), so pay fixed is +1 and receive fixed is -1.

1. Supervisory durations: $SD(5) = 4.4240$, $SD(10) = 7.8694$, $SD(2) = 1.9033$.
2. Bucket 2 (1 to 5 years) holds trades 1 and 3: $D_2 = -100 \times 4.4240 - 80 \times 1.9033 = -594.66$m; bucket 3 holds trade 2: $D_3 = 50 \times 7.8694 = 393.47$m.
3. $EN = \sqrt{594.66^2 + 393.47^2 - 1.4 \times 594.66 \times 393.47} = 425.2823$m and $\text{AddOn} = 0.5\% \times EN = 2{,}126{,}412$ (2,126,411.6 unrounded).
4. Unmargined: $V = 1{,}000{,}000$, $\text{RC} = 1{,}000{,}000$; the multiplier exponent is $1{,}000{,}000 / (2 \times 0.95 \times 2{,}126{,}411.6) = 0.2475 > 0$, so the multiplier is 1; $\text{EAD} = 1.4 \times (1{,}000{,}000 + 2{,}126{,}411.6) = 4{,}376{,}976$.
5. Margined daily with collateral held 800,000, threshold 0, MTA 50,000, NICA 0 and a 10-day MPOR: $\text{RC} = \max(200{,}000, 50{,}000, 0) = 200{,}000$; $MF = 1.5\sqrt{10/250} = 0.30$, so the add-on is $0.30 \times 2{,}126{,}411.6 = 637{,}923.5$, the multiplier is still 1, and $\text{EAD} = 1.4 \times (200{,}000 + 637{,}923.5) = 1{,}173{,}093$.
6. Margining cuts EAD by 3,203,883, or 73.2%; most of it comes from the maturity factor (0.30 against 1), not from the collateral.

## Pitfalls

- Using the 72.5% floor in a year when the local phase-in factor is lower, or the Basel schedule in a jurisdiction that changed it.
- Reading the MDA trigger as a breach of minima: buffers sit above P1 and P2R, and using them limits distributions.
- Mixing currencies in the SMA: the BIC buckets are in EUR (OPE25.7).
- Netting across maturity buckets as if they were one: SA-CCR offsets across buckets only partially (correlations 1.4/2 and 0.6/2 in the formula).
- Forgetting the margined maturity factor $1.5\sqrt{MPOR/250}$, or using 10 days when the MPOR floor is 20 (more than 5,000 trades or illiquid collateral, CRE52.50).
- Calling the DRC equity LGD a floor: it is a prescribed 100% (MAR22.12).

## Interview questions

> [!question]- reg-21-01 | What is the mathematical formula and economic rationale for the Basel IV Output Floor?
> $\text{RWA} = \max(\text{RWA}_{\text{nominated}}, 72.5\% \times \text{RWA}_{\text{SA}})$ (RBC20.4), phased in from 50% in 2023 to 72.5% from 2028 (RBC90.1).
> RBC20.11 gives the rationale: reduce excessive variability of RWA and improve comparability of capital ratios across banks.

> [!question]- reg-21-02 | How does the maturity adjustment factor in the Vasicek formula behave as PD approaches zero?
> It grows: $b = (0.11852 - 0.05478 \ln PD)^2$ rises as PD falls, so $\frac{1 + (M - 2.5) b}{1 - 1.5 b}$ is steeper in $M$.
> High-grade credits have more room to be downgraded over a longer maturity, so maturity matters more for them in relative terms.

> [!question]- reg-21-03 | In SA-CCR, under what condition does the PFE multiplier drop below 1.0?
> When $V - C < 0$: the netting set is out of the money or over-collateralised.
> The multiplier $0.05 + 0.95 \exp((V - C) / (2 \times 0.95 \times \text{AddOn}))$ falls towards the 5% floor (CRE52.23); with $V - C = -1$m and an add-on of 2.126m it is 0.7917.

> [!question]- reg-21-04 | Why are three correlation scenarios (Medium, High, Low) required under the FRTB Sensitivities-Based Method?
> Because correlations break down in stress in either direction, so hedges and diversification may fail.
> The SbM computes capital with medium $\rho$, high $\min(1.25\rho, 1)$ and low $\max(2\rho - 1, 0.75\rho)$ and takes the largest (MAR21.6); curve and basis trades are typically punished by the low scenario.

> [!question]- reg-21-05 | What is the difference between the Business Indicator (BI) and the Business Indicator Component (BIC) in the Operational Risk SMA?
> The BI is the financial-statement proxy, $\text{ILDC} + \text{SC} + \text{FC}$, with components averaged over three years (OPE25.3 to OPE25.5).
> The BIC applies marginal coefficients to it: 12% up to EUR 1bn, 15% from 1bn to 30bn, 18% above 30bn (OPE25.7).

> [!question]- reg-21-06 | What is the Maximum Distributable Amount (MDA) and what triggers it?
> The cap on discretionary distributions (dividends, buybacks, AT1 coupons, variable pay) when a bank does not meet its combined buffer requirement.
> The combined buffer (conservation, countercyclical, G-SIB or O-SII, systemic risk) sits on top of P1 and P2R; P2R is not part of the buffer, and P2G is outside the MDA (CRD Article 141; ECB).
> Basel's version: retention of 100%, 80%, 60% or 40% of earnings by quartile of the buffer (RBC30.4).

> [!question]- reg-21-07 | How does the Liquidity Coverage Ratio (LCR) treat operational versus non-operational corporate deposits?
> Operational deposits run off at 25% (LCR40.26).
> Non-operational deposits of non-financial corporates run off at 40%, or 20% if fully insured (LCR40.40 to LCR40.41); unsecured wholesale funding from financial institutions runs off at 100% (LCR40.42).

> [!question]- reg-21-08 | What are the two tests required for a trading desk to maintain Internal Model Approach (IMA) eligibility under FRTB?
> Desk backtesting: no more than 12 exceptions at the 99th percentile and 30 at the 97.5th over 12 months, counting the larger of APL and HPL exceptions (MAR32.18 to MAR32.19).
> PLA: Spearman correlation and KS distance between HPL and RTPL; green needs Spearman above 0.80 and KS below 0.09, red is Spearman below 0.70 or KS above 0.12 (MAR32.42).
> The bank-wide traffic light (green up to 4 exceptions at 99%) is a separate test that sets the multiplier.

> [!question]- reg-21-09 | What is a Non-Modellable Risk Factor (NMRF) and how is its capital charge calculated?
> A risk factor that fails the RFET: at least 24 real price observations a year with no 90-day period under four, or at least 100 in 12 months (MAR31.13).
> Each NMRF gets a stress-scenario charge at a horizon of at least 20 days (MAR33.16); idiosyncratic credit and equity NMRFs aggregate in quadrature and the rest with $\rho = 0.6$ (MAR33.17), and SES is added to IMCC without diversification.

> [!question]- reg-21-10 | Why does an uncollateralized interest rate swap have a higher KVA than a centrally cleared swap?
> The bilateral swap carries SA-CCR counterparty RWA at the client's risk weight and CVA capital over its life.
> A QCCP-cleared swap has no CVA capital (MAR50.5) and a 2% risk weight on trade exposure (CRE54.7), plus default-fund capital and initial-margin funding, so capital is lower but not zero.

> [!question]- reg-21-11 | What is the supervisory floor on LGD for senior corporate exposures under the Advanced IRB approach?
> 25% for unsecured corporate exposures; for secured exposures 0% (financial collateral), 10% (receivables), 10% (commercial or residential real estate) and 15% (other physical) (CRE32.16).

> [!question]- reg-21-12 | How does the Leverage Ratio act as a backstop to the risk-weighted capital framework?
> Tier 1 must be at least 3% of total exposure regardless of risk weights (LEV20.7), with a G-SIB buffer of 50% of its higher-loss-absorbency requirement (LEV40.2).
> It limits balance sheets of low-risk-weight assets such as repo and sovereign bonds, where model or risk-weight error would otherwise go unchecked.

> [!question]- reg-21-13 | What is the economic difference between Economic Value of Equity (EVE) and Net Interest Income (NII) in IRRBB?
> EVE is the change in present value of banking-book assets minus liabilities under a rate shock, a run-off, long-horizon measure.
> NII is the change in earnings over a short horizon (typically one year) on a going-concern balance sheet; the two can move in opposite directions.

> [!question]- reg-21-14 | Under what condition is the Internal Loss Multiplier (ILM) equal to 1.0 in the Operational Risk SMA?
> When the Loss Component equals the BIC, since $\text{ILM} = \ln(e - 1 + (LC/BIC)^{0.8})$ and $LC = 15 \times$ average annual losses over ten years (OPE25.8).
> It is also 1 for bucket 1 banks and where a supervisor exercises the national discretion to set it to 1 for all banks (OPE25.9, OPE25.11).
> With $LC = 2 \times BIC$ it is 1.2411.

> [!question]- reg-21-15 | In the FRTB Default Risk Charge (DRC), why is the supervisory floor on LGD set to 100% for equity positions?
> It is a prescribed LGD, not a floor: equity and non-senior debt 100%, senior debt 75%, covered bonds 25% (MAR22.12).
> Equity is the most junior claim, so default is assumed to wipe it out.

> [!question]- reg-21-16 | What is the supervisory duration of a 10-year swap starting today?
> $7.8694$.
> $SD = (e^{-0.05 \times 0} - e^{-0.05 \times 10}) / 0.05 = (1 - 0.60653) / 0.05$ (CRE52.34).

> [!question]- reg-21-17 | In Problem 2, why is the multiplier 1 in both the margined and unmargined case?
> Because $V - C > 0$ in both: 1.0m unmargined and 0.2m margined, so the exponent is positive and the formula is capped at 1.

> [!question]- reg-21-18 | What is the IRB risk weight of a corporate with PD 1%, LGD 45%, M 2.5, no SME adjustment?
> About 92.32%.
> Correlation $R = 0.1928$, $K = 7.39\%$ of EAD, risk weight $12.5 K$ (CRE31.5).

> [!question]- reg-21-19 | What is the BIC for a Business Indicator of EUR 35bn?
> EUR 5,370m: $0.12 \times 1{,}000 + 0.15 \times 29{,}000 + 0.18 \times 5{,}000$ (OPE25.7).

> [!question]- reg-21-20 | A bank has 100 each of operational deposits, uninsured non-operational non-financial corporate deposits and unsecured funding from financial institutions. What are the LCR outflows?
> $165$: $25 + 40 + 100$ (LCR40.26, LCR40.40, LCR40.42).

> [!question]- reg-21-21 | A G-SIB with a 1.5% surcharge and no CCyB has a CET1 ratio of 6.8% for the buffer test. What share of earnings may it distribute under Basel?
> 40%.
> The buffer is $2.5\% + 1.5\% = 4\%$ above 4.5%, in four 1-point bands; 6.8% is in the third band (6.5% to 7.5%), which requires 60% retention (RBC30.4, RBC40.2).

> [!question]- reg-21-22 | Tier 1 is 50bn and leverage exposure 1,500bn for a G-SIB with a 1.5% surcharge. Does it meet the leverage requirement and buffer?
> No: 3.33% against $3\% + 0.5 \times 1.5\% = 3.75\%$; it meets the minimum but is inside the leverage buffer (LEV20.7, LEV40.2).

> [!question]- reg-21-23 | Start CET1 13.0%, minimum projected 10.5%, planned dividends for quarters 4 to 7 of 1bn, trough RWA 200bn. What is the Fed SCB?
> $3.0\%$: decline 2.5% plus $1/200 = 0.5\%$, above the 2.5% floor (12 CFR 225.8(f)(2)).

> [!question]- reg-21-24 | What output floor applies in 2027 under the Basel schedule?
> 70% (RBC90.1); 72.5% from 1 January 2028.
> Local schedules differ: the EU and Canada set their own (see [Implementation Status by Jurisdiction](19-Implementation-Status-by-Jurisdiction.md)).

> [!question]- reg-21-25 | Two approved desks have SA of 30 (amber) and 90 (green); jointly $SA_{G,A} = 120$ and $IMA_{G,A} = 80$. What is the amber surcharge?
> $5$: $k = 0.5 \times 30 / 120 = 0.125$ and the surcharge is $0.125 \times (120 - 80)$ (MAR33.45).

> [!question]- reg-21-26 | How are DTAs from net operating loss carry-forwards treated in CET1?
> Deducted in full, net of eligible DTLs; DTAs from temporary differences are deducted only above the 10% and 15% thresholds (CAP30.9, CAP30.32 to CAP30.34).

> [!question]- reg-21-27 | In Problem 2, what share of the EAD reduction from margining comes from the maturity factor rather than the lower RC?
> Most of it: the add-on falls from 2,126,411.6 to 637,923.5 (the 0.30 maturity factor), by 1,488,488, which removes $1.4 \times 1{,}488{,}488 = 2{,}083{,}883$ of EAD, while RC falls by 800,000, removing $1{,}120{,}000$.
> The maturity factor accounts for 65.0% of the 3,203,883 reduction.

## Further reading

- Basel Committee on Banking Supervision, *The Basel Framework* (bis.org/basel_framework): RBC, CAP, CRE, MAR, OPE, LCR and LEV standards.
- Directive 2013/36/EU (CRD), Articles 104a and 141.
- Jon Gregory, *The xVA Challenge: Counterparty Risk, Funding, Collateral, Capital and Initial Margin*, 4th edition, Wiley, 2020.
- Andrea Resti and Andrea Sironi, *Risk Management and Shareholders' Value in Banking*, Wiley, 2007.

## In this repo and SDE-Interview-Prep

- [Capital, RWA and the Basel Framework](01-Capital-RWA-and-the-Basel-Framework.md), [Credit Risk Capital](03-Credit-Risk-Capital-SA-and-IRB.md), [SA-CCR](04-Counterparty-Credit-Risk-SA-CCR.md), [CVA](05-CVA-Capital-Charge-SA-CVA-and-BA-CVA.md).
- [FRTB SbM Delta](07-FRTB-Sensitivities-Based-Method-Delta.md), [FRTB IMA](10-FRTB-Internal-Model-Approach-ES.md), [Backtesting and PLA](12-FRTB-Backtesting-and-PLA-Testing.md).
- [Operational Risk SMA](14-Operational-Risk-Standardised-Measurement-Approach.md), [Leverage and Liquidity](15-Leverage-Ratio-and-Liquidity-Ratios-LCR-and-NSFR.md), [IRRBB](16-Interest-Rate-Risk-in-the-Banking-Book-IRRBB.md), [KVA](20-Capital-Aware-Trading-KVA-and-RWA-Limits.md).
- [code/basel_stress_reg.py](code/basel_stress_reg.py) - asserts every number in this note (`check_note21`), using the SA-CCR, IRB, SMA, LCR, MDA and IMA engines in this folder.
