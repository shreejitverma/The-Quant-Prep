---
type: trade-log
date: 2026-10-16
ticker: "TICKER"
direction: long
playbook: "Setup Name"
entry_price: 0.00
exit_price: 0.00
stop_price: 0.00
shares: 0
pnl_net: 0.00
r_multiple: 0.00
mae_r: 0.00
mfe_r: 0.00
rule_adherence: true
tags: [trade-journal, private]
---

# Trade Log: {{direction}} {{ticker}} ({{date}})

## 1. Trade Overview
- **Instrument**: {{ticker}}
- **Direction**: {{direction}}
- **Playbook Setup**: {{playbook}}
- **Entry Price**: {{entry_price}}
- **Stop Loss**: {{stop_price}}
- **Exit Price**: {{exit_price}}
- **Position Size**: {{shares}}
- **Net PnL**: {{pnl_net}}
- **Realized R-Multiple**: {{r_multiple}} R

---

## 2. Pre-Trade Rationale & Context
- **Market Context**: S&P 500 / NIFTY market breadth, sector relative strength, and volatility regime.
- **Setup Trigger**: Why was this trade initiated at this exact bar and level?
- **Invalidation Rationale**: What structural level invalidated the long/short hypothesis?

---

## 3. Trade Execution & Management
- **Entry Execution**: Limit order filled at bid, or crossed spread with market order?
- **Management During Trade**: Were partial profits taken? Was stop moved according to plan?
- **Exit Rationale**: Hit pre-planned target, hit hard stop, or exited on time-based stop?

---

## 4. Psychological & Behavioral State
- **Pre-Entry**: Confident, impatient, revenge trading, or relaxed?
- **During Trade**: Urge to exit prematurely, fear of giving back gains, or calm detachment?
- **Post-Exit**: Satisfied with process adherence, or regretful of outcome?

---

## 5. Metrics and Calibration
- **Maximum Adverse Excursion (MAE)**: Lowest price reached before target was hit (measured in R).
- **Maximum Favorable Excursion (MFE)**: Highest price reached while holding the position (measured in R).
- **Takeaway Lesson**: One single sentence describing what this trade taught for future refinement.
