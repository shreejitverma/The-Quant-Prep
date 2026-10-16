---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: senior
status: draft
prereqs: [pnl-platform]
est_hours: 4
sources: [Basel Committee on Banking Supervision - Minimum capital requirements for market risk (BCBS d457 2019), International Swaps and Derivatives Association - FRTB Technology Infrastructure and Analytics Architecture (2021), European Banking Authority - Regulatory Technical Standards on the Standardised and Internal Model Approaches (2021)]
---

# FRTB Engine Architecture

## TL;DR

The Fundamental Review of the Trading Book (FRTB, BCBS 239/d457) represents the most computationally demanding regulatory framework ever imposed on capital markets technology.
An enterprise FRTB engine must support dual tracks: the Standardised Approach (SA) and the Internal Models Approach (IMA).
The SA engine automates the Sensitivities-Based Method (SbM), aggregating Delta, Vega, and Curvature across seven asset classes and three correlation scenarios (Medium, High, Low), compounded by Default Risk Charges (DRC) and Residual Risk Add-Ons (RRAO).
The IMA engine evaluates Expected Shortfall across a five-tier liquidity horizon cascade (10, 20, 40, 60, 120 days) scaled by reduced-set stress ratios.
Crucially, trading desks earn and maintain IMA eligibility only by continuously passing two automated middle-office pipelines: the Risk Factor Eligibility Test (RFET) for Non-Modellable Risk Factors (NMRF) and the daily P&L Attribution (PLA) / Backtesting framework.
A failure in PLA testing demotes the desk to the fallback Standardised Approach, triggering massive capital surcharges.

## Learning objectives

- Map the end-to-end computational pipeline of an enterprise FRTB engine spanning SA, IMA, NMRF, and PLA testing.
- Design the Sensitivities-Based Method (SbM) aggregation engine across all 7 asset classes and 3 correlation regimes.
- Formulate the IMA Expected Shortfall liquidity-horizon cascade and reduced-set calibration algorithms.
- Architect the automated Risk Factor Eligibility Test (RFET) pipeline to classify modellable versus non-modellable risk factors.
- Implement automated P&L Attribution (PLA) engines evaluating Kolmogorov-Smirnov and Spearman rank correlation metrics.
- Calculate the total compute budget ($\text{Positions} \times \text{Risk Factors} \times \text{Scenarios} \times \text{Horizons}$) and size distributed cluster resources.

## Core concepts

### 1. Dual-Track FRTB Engine Architecture

```mermaid
flowchart TB
    subgraph InputTier["Market & Trade Data Ingestion"]
        TradeRepository[(Front Office Trade Store)]
        MarketFeeds[(Market Quotes & Real Price Ingest)]
    end

    subgraph RFETPipeline["Risk Factor Eligibility Pipeline (RFET)"]
        RealPriceObs["Real Price Verifier: 24 obs/yr and 4 per 90d, or 100 obs"]
        ModellableSplit{Modellable?}
        MRF["Modellable Factors (IMCC)"]
        NMRF["Non-Modellable Factors (SES)"]
    end

    subgraph CoreEngines["FRTB Core Calculation Engines"]
        SAEngine["FRTB SA Engine (SbM + DRC + RRAO)"]
        IMAEngine["FRTB IMA Engine (Expected Shortfall Cascade)"]
        NMRFEngine["NMRF Stressed Capital Engine (SES)"]
    end

    subgraph DeskMonitoring["Desk Health & Governance"]
        Backtesting[Daily 99% VaR Backtesting]
        PLATest[P&L Attribution Test: KS & Spearman]
        TrafficLight{Desk Zone Status}
    end

    subgraph CapitalAggregation["Capital Aggregator"]
        FinalCapital[Enterprise Market Risk Capital]
    end

    TradeRepository --> SAEngine
    TradeRepository --> IMAEngine
    MarketFeeds --> RealPriceObs
    RealPriceObs --> ModellableSplit
    ModellableSplit -->|Yes| MRF
    ModellableSplit -->|No| NMRF

    MRF --> IMAEngine
    NMRF --> NMRFEngine

    IMAEngine --> Backtesting
    IMAEngine --> PLATest
    Backtesting --> TrafficLight
    PLATest --> TrafficLight

    TrafficLight -->|Green Zone: Approved| FinalCapital
    TrafficLight -->|Amber Zone: Surcharge| FinalCapital
    TrafficLight -->|Red Zone: Fallback to SA| SAEngine

    SAEngine --> FinalCapital
    NMRFEngine --> FinalCapital
```

### 2. Standardised Approach (SA) Engine: SbM, DRC, and RRAO

The SA engine computes three discrete capital components:

$$K_{\text{SA}} = K_{\text{SbM}} + K_{\text{DRC}} + K_{\text{RRAO}}$$

#### 1. Sensitivities-Based Method ($K_{\text{SbM}}$):
- Computed for Delta, Vega, and Curvature across 7 risk classes: GIRR, CSR non-sec, CSR sec-ctp, CSR sec non-ctp, Equity, Commodity, FX.
- Sensitivity weighting: $WS_k = RW_k \times s_k$.
- Bucket-level aggregation:

$$K_b = \sqrt{ \max\left(0, \sum_{k \in b} WS_k^2 + \sum_{k \in b} \sum_{l \neq k, l \in b} \rho_{kl} WS_k WS_l\right) }$$

- Across-bucket aggregation across all buckets $b$:

$$K_{\text{SbM}} = \sqrt{ \sum_b K_b^2 + \sum_b \sum_{c \neq b} \gamma_{bc} S_b S_c }$$

- If the across-bucket radicand is negative, $S_b$ is clamped to $[-K_b, K_b]$ (MAR21.4(5)(b)); the prescribed CSR and equity $\gamma$ matrices are not always PSD, so the engine must still guard the square root (see [SbM Delta](../17-Regulatory-Capital-Basel-and-FRTB/07-FRTB-Sensitivities-Based-Method-Delta.md)).
- Evaluated across three correlation scenarios (MAR21.6): medium ($\rho, \gamma$ as specified), high ($\min(1.25\rho, 1)$), low ($\max(2\rho - 1, 0.75\rho)$).
  Within each scenario, delta, vega and curvature are summed over all risk classes, and the SbM is the largest scenario total (MAR21.7):

$$K_{\text{SbM}} = \max_{s \in \{\text{medium}, \text{high}, \text{low}\}} \sum_{\text{risk classes}} \left(\Delta_s + \mathcal{V}_s + \mathcal{C}_s\right)$$

#### 2. Default Risk Charge ($K_{\text{DRC}}$):
- Evaluates Jump-to-Default (JTD) across debt and equity positions:

$$\text{JTD}_{\text{long}} = \max\left(LGD \times \text{Notional} + P\&L, 0\right), \qquad P\&L = \text{market value} - \text{notional}$$

- LGD is 100% for equity and non-senior debt, 75% for senior debt and 25% for covered bonds (MAR22.12); JTDs under one year are scaled by maturity with a three-month floor (MAR22.15, MAR22.18).

- Offsetting within the same obligor where the short is equally or more junior than the long (MAR22.19), then within each bucket net shorts are discounted by the hedge benefit ratio $HBR = \sum L / (\sum L + \sum |S|)$ and the bucket charge is floored at zero (MAR22.23, MAR22.25).

#### 3. Residual Risk Add-On ($K_{\text{RRAO}}$):
- Applied to instruments with an exotic underlying (longevity, weather, natural disasters, future realised volatility) and to instruments bearing other residual risks (barriers, digitals, Asians, baskets, best-of, Bermudans, multi-callable bonds) (MAR23.3 to MAR23.5).
- Add-on: $1.0\%$ of gross notional for exotic underlyings and $0.1\%$ for other residual risks, with only exact back-to-back trades excluded (MAR23.7, MAR23.8).

### 3. IMA Expected Shortfall with Liquidity Horizons

Under the Internal Models Approach, Expected Shortfall is evaluated across a 5-tier cascade of liquidity horizons ($LH$):

$$\text{ES} = \sqrt{ (\text{ES}_1)^2 + \sum_{j=2}^5 (\text{ES}_j)^2 \frac{LH_j - LH_{j-1}}{10} }$$

Where $\text{ES}_j$ is the 10-day ES shocking only risk factors whose MAR33.12 horizon is at least $LH_j$, with $LH = 10, 20, 40, 60, 120$ days (MAR33.4).
Examples of horizons: specified-currency rates, large-cap equity prices and specified FX pairs 10 days; IG sovereign spreads, small-cap equity prices and energy prices 20; IG corporate spreads and FX volatility 40; HY corporate spreads and rates volatility 60; credit spread volatility and other commodity volatility 120.
The full table and its derivation are in [Internal Model Approach: Expected Shortfall](../17-Regulatory-Capital-Basel-and-FRTB/10-FRTB-Internal-Model-Approach-ES.md).

To incorporate historical stress without running full portfolios across decades, the calibrated ES is scaled via a reduced set ($R$) of liquid risk factors:

$$\text{ES}_{\text{calibrated}} = \text{ES}_{R,S} \times \frac{\text{ES}_{F,C}}{\text{ES}_{R,C}}$$

Where $S$ denotes the 12-month historical stress period, $C$ denotes the current 12-month period, $F$ is the full risk factor set, and $R$ is the reduced set; the ratio $\text{ES}_{F,C}/\text{ES}_{R,C}$ is floored at 1 (MAR33.6).

### 4. Desk Eligibility Traffic Light Matrix (Backtesting & PLA)

| Test | Green | Amber | Red |
| :--- | :--- | :--- | :--- |
| Bank-wide 99% one-day VaR backtest, 250 days (MAR32.9) | 0 to 4 exceptions, $m_c = 1.50$ | 5 to 9, $m_c$ 1.70 to 1.92 | 10 or more, $m_c = 2.00$, model may be disallowed |
| PLA test per desk (MAR32.42) | $r_S > 0.80$ and $KS < 0.09$ | otherwise | $r_S < 0.70$ or $KS > 0.12$: desk to SA |

Desk-level backtesting is separate: a desk with more than 12 exceptions at 99% or more than 30 at 97.5% in 12 months moves to SA (MAR32.19).
Amber PLA desks stay on IMA and drive the bank-level surcharge $k\max\{0, SA_{G,A} - IMA_{G,A}\}$ with $k = 0.5\sum_{amber}SA_i/\sum_{green,amber}SA_i$ (MAR33.45); they do not change $m_c$.
Details are in [Backtesting and PLA Testing](../17-Regulatory-Capital-Basel-and-FRTB/12-FRTB-Backtesting-and-PLA-Testing.md).

## Worked examples

### Example 1: FRTB Compute Budget Sizing for a Tier-1 Trading Book

A global bank designs the hardware and grid capacity for its internal models FRTB engine:
- Portfolio Scope: $P = 250,000$ active trading book positions across 30 trading desks.
- Number of Modellable Risk Factors (MRFs): $N_{\text{MRF}} = 15,000$.
- Number of Non-Modellable Risk Factors (NMRFs): $N_{\text{NMRF}} = 3,500$.
- Historical Scenario Sample: $S = 250$ business days.
- Liquidity Horizon Sub-portfolios: 5 liquidity subsets ($LH_1 \dots LH_5$).
- Calibrations: 3 ($ES_{F,C}$, $ES_{R,C}$, $ES_{R,S}$), each needing its own shocked market states.

Compute Breakdown for Overnight IMA Run:
1. Expected Shortfall Simulation:
   - 250 scenario valuations $\times$ 5 liquidity horizon passes $\times$ 3 calibrations $= 3,750$ portfolio revaluation passes.
   - Total Position Valuations: $250,000\text{ positions} \times 3,750\text{ passes} = 937,500,000\text{ valuations}$.
   - This counts whole-book nested sets only; the risk-class terms of IMCC (MAR33.14) raise the count to up to 21 distinct nested sets per calibration, the "up to 63" ES calculations of the MAR33.15 FAQ, although each position only needs the sets of its own risk class.
2. NMRF Stressed Expected Shortfall ($SES$):
   - 3,500 NMRFs evaluated under extreme stress scenarios (250 days):
   - Total NMRF evaluations: $3,500 \times 250 = 875,000\text{ factor-scenario evaluations}$.
3. Standardised Approach Backup Run (Mandatory benchmark):
   - Delta, Vega, and Curvature across 15,000 risk factors:
   - Using AAD, Greek generation takes $4\times$ base evaluation: $250,000 \times 4 = 1,000,000\text{ valuations}$.
   - Curvature up/down shocks ($2 \times 15,000\text{ pillars}$): evaluated analytically or via grid proxies.

Total Daily Compute Budget:

$$\text{Total Daily Evaluations} \approx 937,500,000 + 875,000 + 1,000,000 = 939,375,000\text{ evaluations}$$

Grid Sizing:
- Average valuation latency across mixed portfolio (swaps, bonds, exotics): $0.5\text{ milliseconds}$ per position evaluation.
- Total Serial CPU Time: $939.375 \times 10^6 \times 0.0005\text{ s} = 469,687.5\text{ CPU seconds} \approx 130.5\text{ CPU hours}$.
- To finish within a $2\text{-hour}$ ($7,200\text{ seconds}$) batch window:

$$N_{\text{cores}} = \frac{469,687.5}{7,200} \approx 65.2 \implies \text{at least 66 cores, before headroom for reruns and skew}$$

### Example 2: PLA Test Automation: Spearman and Kolmogorov-Smirnov Calculation

Over a 250-day observation window, Product Control generates daily Hypothetical PnL ($\mathbf{HPL}$) and Risk-Theoretical PnL ($\mathbf{RTPL}$) for a FX Options Desk:
- Step 1: Kolmogorov-Smirnov Distance ($KS$):
  - Form the empirical cumulative distribution functions $F_{\text{HPL}}(x)$ and $F_{\text{RTPL}}(x)$.
  - Find the maximum vertical divergence:

$$KS = \max_x \left| F_{\text{HPL}}(x) - F_{\text{RTPL}}(x) \right|$$

  - If $KS = 0.065 \le 0.090 \implies$ **Green Zone**.
- Step 2: Spearman Rank Correlation ($r_s$):
  - Assign ranks $R(\text{HPL}_i)$ and $R(\text{RTPL}_i)$ from 1 to 250.
  - Compute rank differences $d_i = R(\text{HPL}_i) - R(\text{RTPL}_i)$.
  - Spearman formula:

$$r_s = 1 - \frac{6 \sum_{i=1}^{250} d_i^2}{250 \times (250^2 - 1)}$$

  - If $r_s = 0.885 \ge 0.800 \implies$ **Green Zone**.
- Outcome: The desk achieves Green Zone status on both metrics, maintaining full IMA eligibility with zero capital surcharge.

### Example 3: Capital Impact of Desk Demotion from IMA to Fallback SA

A desk trading exotic equity baskets manages $\$500,000,000$ of positions:
- While in Green Zone (IMA Model):
  - Calibrated Expected Shortfall ($\text{IMCC}$): $\$18,000,000$.
  - NMRF Stressed Capital ($\text{SES}$): $\$6,000,000$.
  - Total IMA Capital Charge with $m_c = 1.5$ and averages equal to the latest values: $1.5 \times \$18,000,000 + \$6,000,000 = \$33,000,000$ (MAR33.41; SES is not multiplied).
  - Associated RWA ($12.5 \times K$): $\$412,500,000$.
- The desk updates its pricing model without updating the middle-office risk factor engine. Over the next quarter, uncaptured model basis causes $r_s$ to fall to $0.62$ ($< 0.70$) and $KS$ to rise to $0.15$ ($> 0.12$).
- At the next quarterly classification the desk is in the PLA **Red Zone** (MAR32.43):
  - The desk loses IMA eligibility and must calculate capital under the Standardised Approach ($K_{\text{SA}}$).
  - Standalone SbM Delta, Vega, and Curvature: $\$35,000,000$.
  - Default Risk Charge (DRC): $\$8,000,000$.
  - Residual Risk Add-On (RRAO on exotic baskets): $\$15,000,000$.
  - Total SA Capital Charge: $\$35,000,000 + \$8,000,000 + \$15,000,000 = \$58,000,000$.
  - Associated RWA: $12.5 \times \$58,000,000 = \$725,000,000$.
- Capital Impact:
  $$\Delta K = \$58,000,000 - \$33,000,000 = +\$25,000,000\text{ (+75.8\% increase)}$$
  $$\Delta\text{RWA} = \$725,000,000 - \$300,000,000 = +\$425,000,000$$
The desk's return on equity collapses, forcing the bank to shut down the exotic basket trading strategy.

## Pitfalls

- **Neglecting the Low Correlation Scenario in SbM Aggregation:** Assuming the Medium correlation scenario is always binding causes massive capital shortfalls; curve-hedged portfolios often bind under the Low correlation regime ($2\rho - 1$) because offsetting hedges decouple.
- **Treating RFET Real Price Verification as a Point-in-Time Check:** The 24-observation criterion is monitored monthly and also requires that no 90-day period in the previous 12 months holds fewer than four real price observations (MAR31.13); a quiet quarter can turn a factor into an NMRF at the next quarterly test unless it has 100 observations, triggering SES capital.
- **Ignoring Model Differences in PLA Testing:** Using different yield curve interpolation methods (e.g., cubic spline in Front Office vs linear discount factors in Risk) introduces artificial basis that causes PLA test failure even when underlying economic pricing matches.
- **Underestimating Curvature Calculation Overhead:** Curvature requires two full revaluations (up-shock and down-shock) for every single risk factor. Without analytic shortcuts or parallel grids, curvature alone can consume 80% of total SbM runtime.
- **Failing to Track Desk-Level Carve-Outs:** When a desk fails PLA testing and reverts to SA, the bank cannot cherry-pick: the entire desk must be carved out of the IMA aggregation, and cross-desk diversification benefits between that desk and surviving IMA desks are lost.

## Interview questions

> [!question]- sys-10-01 | What are the three core capital components of the FRTB Standardised Approach?
> The three components are:
> 1. Sensitivities-Based Method (SbM): Capital for Delta, Vega, and Curvature across 7 risk classes.
> 2. Default Risk Charge (DRC): Capital for jump-to-default risk in credit and equity trading positions.
> 3. Residual Risk Add-On (RRAO): Capital surcharge for complex and path-dependent instruments with exotic risks.

> [!question]- sys-10-02 | Why must the SbM capital charge be evaluated across three correlation scenarios (Medium, High, Low)?
> Correlations between risk factors are unstable during market crises.
> Offsetting positions that hedge each other under normal correlations can diverge under stress.
> Evaluating across medium ($\rho$), high ($\min(1.25\rho, 1)$) and low ($\max(2\rho - 1, 0.75\rho)$) correlations, summing all risk classes within each scenario and taking the largest total (MAR21.6, MAR21.7), ensures capital covers both correlation spikes and breakdowns.

> [!question]- sys-10-03 | What is the Risk Factor Eligibility Test (RFET) for FRTB internal models?
> RFET is a data-driven test determining whether a risk factor is modellable (MRF) or non-modellable (NMRF).
> A risk factor is modellable if it has at least 24 verifiable real price observations (trades or committed quotes) over the past 12 months with no continuous period of 90 days having fewer than 4 observations.

> [!question]- sys-10-04 | How is capital calculated for Non-Modellable Risk Factors (NMRFs)?
> Each NMRF is capitalized using a stressed Expected Shortfall measure ($SES$) calibrated to an extreme historical stress period.
> Individual $SES$ charges are aggregated as $\sqrt{\sum ISES_i^2} + \sqrt{\sum ISES_j^2} + \sqrt{(0.6\sum SES_k)^2 + 0.64\sum SES_k^2}$: zero correlation only for idiosyncratic credit and equity NMRFs shown to be independent, and a one-factor model with loading 0.6 for all others (MAR33.17).

> [!question]- sys-10-05 | What is the difference between the Kolmogorov-Smirnov test and the Spearman correlation test in FRTB PLA testing?
> The Kolmogorov-Smirnov ($KS$) test evaluates whether the empirical probability distributions of HPL and RTPL match across their entire shape (mean, variance, skewness).
> The Spearman rank correlation test ($r_s$) evaluates whether the directional daily movements of HPL and RTPL are monotonic and correlated in rank order.

> [!question]- sys-10-06 | What happens when a trading desk falls into the Amber Zone in PLA testing?
> An Amber Zone desk remains eligible for the Internal Models Approach, but while any desk is amber the bank adds the surcharge $k\max\{0, SA_{G,A} - IMA_{G,A}\}$ with $k = 0.5\sum_{amber}SA_i/\sum_{green,amber}SA_i$ (MAR33.45).
> The desk returns to green only after a green PLA result with backtesting satisfied over the prior 12 months (MAR32.44).

> [!question]- sys-10-07 | What triggers immediate demotion of a trading desk to the Fallback Standardised Approach?
> A desk moves to the standardised approach if it enters the PLA Red Zone ($KS > 0.12$ or $r_S < 0.70$, MAR32.43) or has more than 12 exceptions of its 99% one-day VaR or more than 30 of its 97.5% one-day VaR in the most recent 12 months (MAR32.19).

> [!question]- sys-10-08 | How does the liquidity horizon cascade operate in FRTB Expected Shortfall?
> Risk factors are mapped to five liquidity horizons: 10, 20, 40, 60, and 120 days based on asset liquidity.
> Expected Shortfall is evaluated across incremental horizon buckets: $\sqrt{(\text{ES}_1)^2 + \sum_{j=2}^5 (\text{ES}_j)^2 \frac{LH_j - LH_{j-1}}{10}}$, ensuring less liquid positions are held against longer holding periods.

> [!question]- sys-10-09 | What is the purpose of the reduced set of risk factors in IMA Expected Shortfall calibration?
> Calculating full-portfolio Expected Shortfall across decades of historical market data is computationally impossible.
> Banks calibrate a reduced set of liquid risk factors ($R$) that explains at least 75% of portfolio variance over both the current window and the historical stress window, scaling the full-set current ES by the stress ratio: $\text{ES} = \text{ES}_{R,S} \times \frac{\text{ES}_{F,C}}{\text{ES}_{R,C}}$.

> [!question]- sys-10-10 | Why is Curvature risk in SbM non-linear, and how is it calculated?
> Curvature captures option Gamma and Vega non-linearities not captured by linear Delta.
> It is calculated by applying upward and downward supervisory shocks to the risk factor, subtracting the linear Delta move: $CVR_k^+ = -\left[ V(S_k + RW_k) - V(S_k) - RW_k \times s_k \right]$.
> Within each bucket the engine takes the larger of the aggregated up and down charges, $K_b = \max(K_b^+, K_b^-)$, using squared delta correlations and the $\psi$ indicator that drops cross terms between two negative CVRs (MAR21.5, MAR21.100).

## Further reading

- Basel Committee on Banking Supervision. *Minimum capital requirements for market risk*. BIS d457, 2019.
- European Banking Authority. *Regulatory Technical Standards on the P&L attribution test*. EBA/RTS/2021/04, 2021.
- International Swaps and Derivatives Association. *FRTB Implementation Guide: Practical Steps and Industry Best Practice*. ISDA, 2020.
- European Central Bank. *ECB Guide to internal models: Market risk chapter*. ECB Banking Supervision, 2019.
