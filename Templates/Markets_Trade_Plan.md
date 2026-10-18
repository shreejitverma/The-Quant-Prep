---
type: trade-plan
date: 2026-10-18
ticker: "TICKER"
direction: long
playbook: "Setup Name"
timeframe: "15m"
target_entry: 0.00
invalidation_stop: 0.00
profit_target_1: 0.00
profit_target_2: 0.00
max_risk_dollars: 0.00
shares: 0
tags: [trade-plan, execution]
---

# Pre-Trade Plan: {{direction}} {{ticker}} ({{date}})

## 1. Setup Identification and Core Thesis
- **Instrument**: {{ticker}}
- **Direction**: {{direction}}
- **Playbook Setup**: {{playbook}}
- **Time Horizon**: {{timeframe}}
- **Core Edge Hypothesis**: Precise explanation of the structural market inefficiency or order flow imbalance being exploited.

---

## 2. Higher Timeframe Context and Market Internals
- **Market Regime**: Broad index trend (S&P 500 / NIFTY 50), volatility regime (VIX / India VIX), and advance-decline breadth.
- **Sector Relative Strength**: Sector ETF relative strength ranking versus the broader market.
- **Key Structural Levels**: Prior Day High/Low, Weekly Value Area (VAH/VAL/POC), and Anchored VWAP anchors.

---

## 3. Order Execution Architecture
- **Planned Entry Price**: {{target_entry}}
- **Entry Mechanism**: Limit order resting at key liquidity pool, or aggressive market order upon order book confirmation.
- **Queue and Slippage Allowance**: Maximum acceptable slippage tolerance in cents/ticks.
- **Execution Benchmark**: Implementation Shortfall versus arrival price.

---

## 4. Position Sizing and Capital Risk
- **Total Portfolio Equity**: Reference base equity at time of plan inception.
- **Risk Fraction**: Maximum percentage of portfolio risked on this setup (typically 0.5% to 1.0%).
- **Maximum Risk Amount**: {{max_risk_dollars}}
- **Position Size**: {{shares}} shares / contracts calculated via hard mathematical formula:
  $$\text{Shares} = \frac{\text{Maximum Risk Dollars}}{|\text{Target Entry} - \text{Invalidation Stop}|}$$

---

## 5. Invalidation Criteria and Hard Stop Placement
- **Structural Invalidation Level**: {{invalidation_stop}}
- **Invalidation Rationale**: Structural auction pivot where the premise is objectively refuted by market participants.
- **Stop Execution Rule**: Hard stop resting in the exchange order book; no manual mental stops.

---

## 6. Multi-Stage Profit Taking and Runner Management
- **Profit Target 1 (De-Risk)**: {{profit_target_1}} (take 50% off to cover risk and lock in baseline R-multiple).
- **Profit Target 2 (Terminal Target)**: {{profit_target_2}} (opposing major liquidity pool or daily average true range extension).
- **Trailing Stop Rule**: Trailing stop mechanism for runner portion (e.g., prior 15-minute swing pivot or 2-period ATR trail).
- **Time-Based Exit**: Maximum holding duration in bars or minutes if volatility fails to expand.

---

## 7. Contingency Scenario Matrix
- **Scenario A (Clean Expansion)**: Price hits entry and expands immediately toward Target 1; move stop to breakeven after Target 1 fill.
- **Scenario B (Early Chop / Indecision)**: Price fills entry but oscillates near entry for N bars without progress; reduce position by 50% at market.
- **Scenario C (Adverse Gap / Slippage)**: Price gaps past invalidation level on binary headline; execute immediate market liquidation with zero hesitation.
