---
type: moc
title: "Systematic Trading Systems Index"
track: [quant-trader, quant-dev, quant-research]
tier: advanced
status: solid
tags: [systems, systematic-trading, decision-ledger, backtesting, risk-management, moc]
---

# Systematic Trading Systems Index

The Systematic Trading Systems pillar bridges quantitative strategy design, institutional risk control, backtest validation, and automated execution architecture.
It ensures every strategy is subjected to rigorous out-of-sample stress testing, combinatorial purged cross-validation, and production-grade execution constraints.

---

## Learning Objectives

- Formulate end-to-end systematic trading strategies across universe definition, alpha signals, portfolio weighting, and execution.
- Implement robust backtesting protocols that eliminate lookahead bias, survivorship bias, and multiple-testing data snooping.
- Build automated risk engines enforcing real-time Value-at-Risk (VaR), Expected Shortfall (ES), and maximum drawdown cutoffs.
- Maintain an auditable Decision Ledger recording trading rationale, parameter states, and execution telemetry.

---

## Systematic Trading Curriculum Map

The core curriculum comprises eight comprehensive concept notes with 256 verified interview questions and problem cards:

1. [[16-Trading-and-Investing/60-Systems/01-Strategy-Architecture-and-Universe-Selection|01. Strategy Architecture and Universe Selection]]
   - The four-layer pipeline (Universe, Signals, Portfolio, Execution).
   - Dynamic liquidity filters, rolling ADV thresholds, and minimum price bounds.
   - Eliminating survivorship and delisting biases with point-in-time constituent data.
   - Borrow availability, locate verification, and hard-to-borrow (HTB) cost economics.
   - Hysteresis buffer bands to eliminate universe constituent churn.
   - Cards: `mkt-sys-001` through `mkt-sys-032`.

2. [[16-Trading-and-Investing/60-Systems/02-Cross-Sectional-and-Time-Series-Signals|02. Cross-Sectional and Time-Series Signals]]
   - Cross-sectional relative ranking vs time-series absolute momentum (Moskowitz, Ooi, Pedersen 2012).
   - Feature normalization: MAD Winsorization, cross-sectional z-scoring, and uniform rank mapping.
   - Performance evaluation: Pearson IC, Spearman Rank IC, and IC Information Ratio (ICIR).
   - Signal half-life and autocorrelation decay modeling.
   - Grinold's Fundamental Law ($IR = IC \times \sqrt{BR}$) and the Transfer Coefficient (TC) constraint penalty.
   - Cards: `mkt-sys-033` through `mkt-sys-064`.

3. [[16-Trading-and-Investing/60-Systems/03-Portfolio-Construction-and-Risk-Parity|03. Portfolio Construction and Risk Parity]]
   - Markowitz mean-variance optimization and Michaud's "error maximization" curse.
   - Covariance ill-conditioning, condition numbers ($\lambda_{\max} / \lambda_{\min}$), and Ledoit-Wolf shrinkage.
   - Equal Risk Contribution (ERC) risk parity: marginal and total risk contribution derivations.
   - Hierarchical Risk Parity (HRP, Lopez de Prado 2016): tree clustering, quasi-diagonalization, and recursive bisection.
   - Real-world portfolio constraints: turnover penalties, leverage caps, and sector bounds.
   - Cards: `mkt-sys-065` through `mkt-sys-096`.

4. [[16-Trading-and-Investing/60-Systems/04-Backtest-Overfitting-and-Multiple-Testing|04. Backtest Overfitting and Multiple Testing]]
   - Statistical mechanism of selection bias under the null hypothesis (Extreme Value Theory).
   - Expected maximum Sharpe of $N$ null trials scaling with $\sqrt{2 \ln N}$.
   - Probabilistic Sharpe Ratio (PSR) adjusting for sample length, negative skewness, and fat-tailed kurtosis.
   - Deflated Sharpe Ratio (DSR, Bailey & Lopez de Prado 2014) setting benchmarks to null selection maxima.
   - Harvey, Liu, and Zhu (2016) multiple-testing haircuts (Bonferroni, Holm, BHY FDR) and the $t > 3.0$ factor threshold.
   - Minimum Backtest Length (MinBTL) in years.
   - Cards: `mkt-sys-097` through `mkt-sys-128`.

5. [[16-Trading-and-Investing/60-Systems/05-Combinatorial-Purged-Cross-Validation|05. Combinatorial Purged Cross-Validation]]
   - Failure of standard k-fold cross-validation on financial time series due to non-iid serial correlation.
   - Data purging: removing overlapping forward holding period labels to eliminate leakage.
   - Data embargoing: removing post-test buffers to eliminate autoregressive persistence.
   - Combinatorial Purged Cross-Validation (CPCV): generating $\binom{N-1}{k-1}$ out-of-sample backtest paths from $\binom{N}{k}$ splits.
   - Combinatorially Symmetric Cross-Validation (CSCV) and Probability of Backtest Overfitting (PBO).
   - Cards: `mkt-sys-129` through `mkt-sys-160`.

6. [[16-Trading-and-Investing/60-Systems/06-Execution-Slippage-and-Cost-Models|06. Execution Slippage and Cost Models]]
   - Complete transaction cost taxonomy: explicit fees, bid-ask spread, delay cost, and opportunity cost.
   - Implementation Shortfall (Perold 1988) formulation and component attribution.
   - Temporary vs permanent market impact dynamics.
   - The universal square-root law of market impact ($I = Y \cdot \sigma \sqrt{Q / V_{\text{ADV}}}$).
   - Strategy capacity estimation and the Sharpe ratio decay curve ($R_{\text{net}} = \alpha_0 - c \cdot \tau \sqrt{A}$).
   - Algorithmic execution benchmarks: TWAP, VWAP, POV, and Almgren-Chriss optimal execution.
   - Cards: `mkt-sys-161` through `mkt-sys-192`.

7. [[16-Trading-and-Investing/60-Systems/07-Volatility-Targeting-and-Dynamic-Leverage|07. Volatility Targeting and Dynamic Leverage]]
   - Dynamic gross exposure scaling inversely to rolling realized volatility ($k_t = \sigma_{\text{target}} / \hat{\sigma}_t$).
   - Statistical edge: exploiting volatility clustering (Engle 1982) and the risk-return disconnect (Moreira & Muir 2017).
   - Realized volatility estimators: Close-to-Close EWMA, Parkinson high-low, Garman-Klass, and Rogers-Satchell.
   - Leverage caps, unencumbered cash buffers, margin haircuts, and financing spread drag.
   - Multi-tiered systematic drawdown governors and circuit breakers (Tier 1 warning, Tier 2 throttle, Tier 3 nuclear flatten).
   - Cards: `mkt-sys-193` through `mkt-sys-224`.

8. [[16-Trading-and-Investing/60-Systems/08-Production-Architecture-and-Decision-Ledger|08. Production Architecture and Decision Ledger]]
   - Four-tier production architecture: Market data, strategy state, pre-trade risk, and OMS/EMS.
   - SEC Rule 15c3-5 (Market Access Rule) mandatory pre-trade price collar bands and capital throttles.
   - The Decision Ledger: immutable, append-only audit trail logging inputs, parameters, weights, and telemetry.
   - Hardware and daemon kill-switch architecture with heartbeat dead-man switches.
   - Post-trade Transaction Cost Analysis (TCA) and Brinson-Fachler performance attribution.
   - Cards: `mkt-sys-225` through `mkt-sys-256`.

---

## Cross-Vault Alpha Research References

This pillar directly operationalizes theoretical research across the Quant Prep vault:

- [[09-Alpha-Research-and-Portfolio/01-Research-Process-and-Hypothesis-Discipline|01. Research Process and Hypothesis Discipline]]
- [[09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay|03. Signals, Features, and Alpha Decay]]
- [[09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls|07. Backtesting Methodology and Pitfalls]]
- [[09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe|08. Overfitting and Deflated Sharpe]]
- [[09-Alpha-Research-and-Portfolio/09-Performance-Metrics-and-Fundamental-Law|09. Performance Metrics and Fundamental Law]]
- [[09-Alpha-Research-and-Portfolio/10-Mean-Variance-Portfolio-Construction|10. Mean-Variance Portfolio Construction]]

---

## Trading Lab Engines

- `overfit_trap`: Backtest Overfitting Trap, Deflated Sharpe Ratio (DSR), Harvey-Liu haircuts, and CSCV PBO simulator.
- `pos_sizing`: Dynamic position sizing engine evaluating ruin probabilities under Kelly and leverage constraints.
- `port_alloc`: Multi-asset portfolio allocator (Risk Parity, Black-Litterman, HRP).

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Trading Styles**: [[16-Trading-and-Investing/07-Trading-Styles/_Index_Trading_Styles|Trading Styles Index]]
- **Technical Analysis**: [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/_Index_Technical_Analysis|Technical Analysis Index]]
- **Pricing and Risk Systems**: [[18-Pricing-and-Risk-Systems/README|Pricing and Risk Systems Architecture]]
