---
type: moc
title: "Technical Analysis Track Index"
track: [quant-trader, quant-research]
tier: core
status: solid
tags: [technical-analysis, price-action, momentum, evidence-based, volume-profile, vwap, moc]
---

# Technical Analysis Track Index

The Technical Analysis track provides an evidence-based, quantitative evaluation of price action, chart geometry, market microstructure, and momentum phenomena.
Rather than treating technical indicators as mystical rituals or self-fulfilling prophecies, Markets Mastery OS subjects every pattern, oscillator, and trend-following rule to academic empirical rigor.
Each module pairs classical chartist observations with peer-reviewed literature, establishing where genuine structural edge exists and where data-snooping bias creates illusory patterns.

---

## Learning Objectives

- Distinguish statistically validated technical phenomena (e.g., time-series momentum, post-earnings announcement drift, institutional volume absorption) from refuted chartist folklore.
- Quantify the statistical significance of support, resistance, and geometric chart patterns using kernel regression and objective boundary algorithms.
- Interpret Auction Market Theory, Volume Profile, and Anchored VWAP to identify institutional accumulation and distribution zones.
- Evaluate momentum, relative strength, and market breadth divergences to detect underlying regime transitions.
- Apply proper scoring rules (Brier scores, log loss, Murphy decomposition) and blind chart replays to calibrate subjective probability forecasting.

---

## Evidence Ledger Hierarchy

Every technical pattern in this track carries an explicit empirical evidence grade:

- **STRONG**: Validated across multiple independent asset classes and decadal timeframes in peer-reviewed academic literature with controls for transaction costs and multiple testing.
- **MIXED**: Statistically significant in specific historical sub-periods or asset classes (e.g. commodities, small caps), but decayed post-publication or heavily sensitive to transaction friction.
- **WEAK**: Inconsistent statistical significance across broad samples; edge vanishes once data-snooping adjustments (White's Reality Check, Harvey-Liu-Zhu hurdle) are applied.
- **REFUTED**: Rigorously demonstrated to perform no better than random price diffusion once survivorship, bid-ask bounce, and look-ahead biases are eliminated.
- **UNTESTED**: Subjective chartist rules lacking verifiable algorithmic definitions or empirical backtest literature.

---

## Concept Notes in This Track

1. [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/01-Dow-Theory-and-Trend-Evidence|01 - Dow Theory, Trend Definition, and Empirical Evidence]]
2. [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/02-Chart-Patterns-and-Statistical-Edge|02 - Classical Chart Patterns, Geometric Formations, and Statistical Reality]]
3. [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/03-Auction-Theory-Volume-Profile-and-VWAP|03 - Auction Market Theory, Volume Profile, and Anchored VWAP]]
4. [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/04-Momentum-Relative-Strength-and-Breadth|04 - Cross-Sectional Momentum, Relative Strength, and Market Breadth]]
5. [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/05-Oscillators-Mean-Reversion-and-Overfitting|05 - Oscillators, Mean Reversion Regimes, and the Multiple Testing Hazard]]
6. [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/06-Order-Flow-Tape-Reading-and-Footprint|06 - Order Flow Microstructure, Footprint Charts, and Tape Reading]]
7. [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/07-Time-Series-Momentum-and-Trend-Following|07 - Time-Series Momentum, Trend Following, and Crisis Alpha]]
8. [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/08-Quantitative-Rule-Validation-and-Calibration|08 - Quantitative Rule Validation, Brier Calibration, and Overfitting Control]]

---

## Trading Lab Integration

- `replay_chart`: Blind chart replay engine evaluating user probability forecasts against an analytical oracle across market regimes.
- `overfit_trap`: Backtest variant explorer calculating Deflated Sharpe Ratios and Probability of Backtest Overfitting (PBO).

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Trading Styles Index**: [[16-Trading-and-Investing/07-Trading-Styles/_Index_Trading_Styles|Trading Styles and Personas Index]]
- **Discretionary Trading**: [[16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/01-Retail-Base-Rates-and-Costs|Discretionary Trading Foundations]]
