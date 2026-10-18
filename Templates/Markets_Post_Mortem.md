---
type: post-mortem
date: 2026-10-18
event_id: "PM-2026-001"
ticker: "TICKER"
event_category: "execution-loss"
pnl_impact: 0.00
r_impact: 0.00
rule_violation: false
tags: [post-mortem, risk-audit, continuous-improvement]
---

# Post-Mortem Incident Report: {{event_id}} ({{date}})

## 1. Executive Summary and Chronological Timeline
- **Event Description**: Concise factual narrative of the trade, outage, or risk anomaly being analyzed.
- **Instrument**: {{ticker}}
- **Total Realized PnL**: {{pnl_impact}}
- **Impact in R-Multiples**: {{r_impact}} R
- **Rule Adherence**: {{rule_violation}}
- **Chronological Sequence of Events**:
  - `HH:MM:SS` - Order entry initiated via execution algorithm or discretionary ticket.
  - `HH:MM:SS` - First fills received; initial spread slippage observed.
  - `HH:MM:SS` - Adverse price shock or volatility expansion occurred.
  - `HH:MM:SS` - Position closed or stop loss triggered.

---

## 2. Quantitative Execution and Slippage Attribution
- **Expected Entry vs Actual Fill**: Slip in cents and basis points relative to arrival price.
- **Market Impact Component**: Did the order consume more than 5% of available order book depth?
- **Fee and Financing Costs**: Exchange fees, clearing costs, borrow fees, and overnight financing drag.
- **Net Execution Efficiency**: Implementation Shortfall versus VWAP benchmark.

---

## 3. Root Cause Investigation (The 5 Whys Method)
1. **First Order Effect**: Why did the trade experience an unexpected loss or execution deviation?
2. **Second Order Effect**: Why was the risk parameter or stop loss insufficient to contain the excursion?
3. **Third Order Effect**: Why did the pre-trade screening model fail to anticipate the adverse liquidity condition?
4. **Fourth Order Effect**: Why did the risk monitoring system fail to alert the trader prior to breach?
5. **Root Systemic Cause**: What structural assumption or software limitation allowed this event to occur?

---

## 4. Excursion Forensics (MAE and MFE)
- **Maximum Adverse Excursion (MAE)**: Maximum unrealized loss experienced during the life of the trade.
- **Maximum Favorable Excursion (MFE)**: Maximum unrealized gain reached prior to exit.
- **Efficiency Metric**: Was capital left on the table due to premature profit taking, or was the stop loss too loose?

---

## 5. Psychological and Behavioral State Audit
- **Stress and Cognitive Load**: Was the trader fatigued, overextended, or trading outside core market hours?
- **Cognitive Biases Manifested**: Sunk cost fallacy, loss aversion, anchoring, or revenge trading.
- **Intervention Discipline**: Was the exit executed strictly in accordance with plan, or delayed due to emotional hope?

---

## 6. Classification: Stochastic Variance versus Process Breakdown
- **Pure Variance**: Trade followed all playbook criteria with high discipline, but resulted in a normal probabilistic loss.
- **Execution Drift**: Minor timing or sizing errors that did not violate explicit risk rules.
- **Process Breakdown**: Severe rule violation, oversized position, bypassed stop, or unvetted strategy execution.

---

## 7. Actionable Systemic Safeguards and Remediation
- **Immediate Corrective Action**: Immediate code patch, hard risk limit adjustment, or playbook refinement.
- **Regression Test Added**: Automated test case added to `tools/tests/` or validation scripts to prevent recurrence.
- **Audit Verification Date**: Planned follow-up review date to verify safeguard effectiveness in live trading.
