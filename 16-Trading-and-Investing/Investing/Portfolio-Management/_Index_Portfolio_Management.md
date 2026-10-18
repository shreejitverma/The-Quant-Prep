---
type: moc
title: "Portfolio Management and Capital Allocation Index"
track: [quant-trader, quant-research]
tier: core
status: solid
tags: [portfolio-management, asset-allocation, factor-investing, rebalancing, drawdowns, risk-of-ruin, kelly-criterion, risk-parity, all-weather, macro-regimes, behavioral-finance, moc]
---

# Portfolio Management and Capital Allocation Index

The Portfolio Management and Capital Allocation curriculum provides the mathematical, structural, and behavioral principles required to construct and manage institutional multi-asset investment portfolios.
It bridges theoretical portfolio optimization with execution reality, covering strategic and tactical asset allocation, factor premium harvesting, rebalancing mechanics, drawdown risk management, capital growth theory, risk parity, debt cycles, and behavioral governance.

---

## Learning Objectives

- Quantify the primacy of Strategic Asset Allocation (SAA) and prove Sharpe's Arithmetic of Active Management.
- Audit the empirical persistence, replication robustness, and post-publication decay of Fama-French and AQR factor premiums.
- Design optimal portfolio rebalancing policies that balance tracking error against transaction friction and capital gains taxes.
- Model path-dependent drawdown dynamics, sequence of returns risk, and gambler's ruin probabilities.
- Derive the continuous and discrete Kelly Criterion to maximize long-term logarithmic wealth while mitigating estimation risk.
- Construct Equal Risk Contribution (ERC) and Bridgewater All Weather portfolios across distinct macroeconomic growth and inflation quadrants.
- Diagnose macro regimes and systemic debt super-cycles using Minsky's financial instability taxonomy and central bank policy evolution (MP1, MP2, MP3).
- Implement institutional debiasing architectures, including Gary Klein pre-mortems, red-team protocols, and automated execution rules.

---

## Portfolio Management Curriculum Map

The portfolio management track comprises eight comprehensive concept notes containing 256 verified practice questions and problem cards:

1. [[16-Trading-and-Investing/Investing/Portfolio-Management/01-Asset-Allocation-and-The-Benchmark-to-Beat|01. Asset Allocation and The Benchmark to Beat]]
   - The Brinson, Singer, and Beebower empirical findings on the determinants of return variability.
   - William Sharpe's mathematical proof of the Arithmetic of Active Management.
   - The low-cost market index as the foundational performance hurdle.
   - Strategic Asset Allocation (SAA) policy portfolios versus Tactical Asset Allocation (TAA) tilts.
   - Antti Ilmanen's expected return building-block framework.
   - Cards: `mkt-pf-001` through `mkt-pf-032`.

2. [[16-Trading-and-Investing/Investing/Portfolio-Management/02-Factor-Investing-Evidence-Replication-and-Decay|02. Factor Investing: Evidence, Replication, and Decay]]
   - The Capital Asset Pricing Model (CAPM) and the emergence of the Multi-Factor "Factor Zoo".
   - The canonical academic factor premiums: Value (HML), Size (SMB), Momentum (UMD), Profitability (RMW), Investment (CMA), and Low Volatility (BAB).
   - McLean and Pontiff's empirical findings on post-publication factor return decay and crowd arbitrage.
   - Methodological replication requirements: cross-sectional sorting, value weighting, and delisting bias correction.
   - Multi-factor portfolio integration: sequential screening versus unified cross-sectional composite scoring.
   - Cards: `mkt-pf-033` through `mkt-pf-064`.

3. [[16-Trading-and-Investing/Investing/Portfolio-Management/03-Portfolio-Rebalancing-Tax-Drag-and-Execution-Friction|03. Portfolio Rebalancing, Tax Drag, and Execution Friction]]
   - Calendar-based periodic rebalancing versus opportunistic tolerance band corridor rebalancing.
   - The mathematics of the "rebalancing bonus" in uncorrelated volatile assets.
   - Calculating optimal corridor widths using asset volatility, transaction costs, and tracking error budgets.
   - Tax-aware rebalancing: cash flow directing, Specific Lot Identification (SpecID), and tax-loss harvesting.
   - Asset location optimization across taxable, tax-deferred, and tax-exempt accounts.
   - Cards: `mkt-pf-065` through `mkt-pf-096`.

4. [[16-Trading-and-Investing/Investing/Portfolio-Management/04-Drawdown-Mathematics-and-Risk-of-Ruin|04. Drawdown Mathematics and Risk of Ruin]]
   - The non-linear asymmetry of losses: $R_{\text{rec}} = D / (1 - D)$.
   - Maximum Drawdown (MDD), Ulcer Index, Calmar ratio, Sterling ratio, and Burke ratio.
   - Continuous Brownian motion drawdown scaling with drift and volatility.
   - Classical Gambler's Ruin difference equations across finite and infinite boundaries.
   - Sequence of Returns Risk (SRR) under ongoing capital withdrawal schedules.
   - Constant Proportion Portfolio Insurance (CPPI) and volatility targeting.
   - Cards: `mkt-pf-097` through `mkt-pf-128`.

5. [[16-Trading-and-Investing/Investing/Portfolio-Management/05-Kelly-Criterion-and-Capital-Growth-Theory|05. Kelly Criterion and Capital Growth Theory]]
   - Information theoretic origins and Shannon channel capacity equivalence.
   - Mathematical derivation of single-period and continuous Gaussian Kelly leverage: $f^* = (\mu - r) / \sigma^2$.
   - The capital growth curve $g(f)$, Double Kelly parity, and variance decay ruin.
   - Full Kelly versus Fractional Kelly trade-offs between growth rate and drawdown risk.
   - Multi-asset matrix Kelly optimization: $\mathbf{f}^* = \mathbf{\Sigma}^{-1}(\boldsymbol{\mu} - r\mathbf{1})$.
   - Epistemic uncertainty, parameter estimation error, and Bayesian shrinkage.
   - Cards: `mkt-pf-129` through `mkt-pf-160`.

6. [[16-Trading-and-Investing/Investing/Portfolio-Management/06-Risk-Parity-and-The-All-Weather-Framework|06. Risk Parity and The All-Weather Framework]]
   - The risk concentration fallacy of the traditional 60/40 equity/bond portfolio.
   - Euler's homogeneous function decomposition of portfolio risk into Marginal and Total Risk Contributions.
   - Equal Risk Contribution (ERC) formulation and convex optimization.
   - Bridgewater's 4-quadrant All Weather macro framework matching asset classes to growth and inflation regimes.
   - Leverage implementation mechanics, repo financing drag, and simultaneous stock-bond crash vulnerabilities (such as 2022).
   - Cards: `mkt-pf-161` through `mkt-pf-192`.

7. [[16-Trading-and-Investing/Investing/Portfolio-Management/07-Macro-Regimes-and-Debt-Cycles|07. Macro Regimes and Debt Cycles]]
   - Ray Dalio's three-force economic machine: productivity drift, short-term debt cycles, and long-term debt super-cycles.
   - Hyman Minsky's Financial Instability Hypothesis: Hedge, Speculative, and Ponzi financing stages.
   - Debt sustainability dynamics: the $r - g$ differential and primary budget balances.
   - Deleveraging mechanics: the four levers (austerity, defaults, wealth transfers, and debt monetization) and "Beautiful Deleveraging".
   - Central bank monetary policy evolution: Interest Rate Policy (MP1), Quantitative Easing (MP2), and Fiscal-Monetary Coordination (MP3).
   - Yield curve regime taxonomy: bull/bear steepeners, flatteners, and inversion warning signals.
   - Cards: `mkt-pf-193` through `mkt-pf-224`.

8. [[16-Trading-and-Investing/Investing/Portfolio-Management/08-Behavioral-Portfolio-Management-and-Decision-Rules|08. Behavioral Portfolio Management and Decision Rules]]
   - Kahneman and Tversky's Prospect Theory: reference dependence, loss aversion ($\lambda \approx 2.25$), and the S-shaped value function.
   - Shefrin and Statman's Disposition Effect and Odean's empirical quantification (PGR vs PLR).
   - Institutional agency friction: career risk, Keynesian conventional failure, closet indexing, and window dressing.
   - Decision quality versus outcome quality: Annie Duke's "resulting" matrix.
   - Institutional debiasing architectures: Gary Klein pre-mortems, red teams, blinded research, and automated IPS execution rules.
   - Cards: `mkt-pf-225` through `mkt-pf-256`.

---

## Card Registry and Summary

Across the eight notes of the Portfolio Management track, 256 flashcards are registered:

| Note | Title | Card Range | Total Cards |
|---|---|---|---|
| 01 | Asset Allocation and The Benchmark to Beat | `mkt-pf-001` to `mkt-pf-032` | 32 |
| 02 | Factor Investing: Evidence, Replication, and Decay | `mkt-pf-033` to `mkt-pf-064` | 32 |
| 03 | Portfolio Rebalancing, Tax Drag, and Execution Friction | `mkt-pf-065` to `mkt-pf-096` | 32 |
| 04 | Drawdown Mathematics and Risk of Ruin | `mkt-pf-097` to `mkt-pf-128` | 32 |
| 05 | Kelly Criterion and Capital Growth Theory | `mkt-pf-129` to `mkt-pf-160` | 32 |
| 06 | Risk Parity and The All-Weather Framework | `mkt-pf-161` to `mkt-pf-192` | 32 |
| 07 | Macro Regimes and Debt Cycles | `mkt-pf-193` to `mkt-pf-224` | 32 |
| 08 | Behavioral Portfolio Management and Decision Rules | `mkt-pf-225` to `mkt-pf-256` | 32 |
| **Total** | **Portfolio Management Track** | **`mkt-pf-001` to `mkt-pf-256`** | **256** |
