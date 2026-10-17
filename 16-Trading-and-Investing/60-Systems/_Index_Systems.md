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

## Core Topics

### 1. Strategy Architecture and Pipeline
- **Universe Selection**: Dynamic liquidity filters, minimum average daily volume (ADV), market cap thresholds, and borrow availability.
- **Signal Generation**: Feature engineering, normalization (z-scores, cross-sectional ranking), and decay half-life analysis.
- **Portfolio Construction**: Mean-variance optimization with shrinkage, Hierarchical Risk Parity (HRP), and volatility-targeted risk parity.
- **Execution Interface**: Translating target portfolio weights into discrete child orders with minimum lot sizes and transaction cost models.

### 2. Backtesting Rigor and Overfitting Defense
- **Lookahead and Survivorship Bias**: Proper handling of point-in-time corporate fundamentals, split adjustments, and historical index delistings.
- **Combinatorial Purged Cross-Validation (CPCV)**: Preventing information leakage across overlapping holding periods by purging and embargoing train-test splits (Lopéz de Prado).
- **Deflated Sharpe Ratio (DSR)**: Adjusting the observed backtest Sharpe ratio for the number of tested trials, return skewness, and kurtosis.

### 3. Risk Management and Position Sizing Engines
- **Kelly Criterion**: Full Kelly versus Fractional Kelly (half-Kelly / quarter-Kelly) to balance capital growth against catastrophic drawdown risk.
- **Volatility Targeting**: Dynamically scaling total leverage so annualized portfolio volatility remains pegged to a constant target (e.g. 10% annualized).
- **Circuit Breakers and Throttles**: Automated drawdown governors cutting position sizes by 50% upon reaching a 5% peak-to-trough drawdown, and flattening all risk upon reaching 10%.

### 4. Decision Ledger and Audit Trail
- **Systematic Decision Logging**: Recording every strategy state, raw alpha signal, target weight, executed fill, and post-trade slippage.
- **Performance Attribution**: Decomposing gross strategy returns into asset allocation, stock selection, timing, and execution friction.

---

## Trading Lab Engines

- `overfit_trap`: Backtest overfitting detector and Deflated Sharpe Ratio analyzer.
- `pos_sizing`: Dynamic position sizing engine evaluating ruin probabilities under Kelly and leverage constraints.
- `port_alloc`: Multi-asset portfolio allocator (Risk Parity, Black-Litterman, HRP).

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Trading Styles**: [[16-Trading-and-Investing/07-Trading-Styles/_Index_Trading_Styles|Trading Styles Index]]
- **Pricing and Risk Systems**: [[18-Pricing-and-Risk-Systems/README|Pricing and Risk Systems Architecture]]
