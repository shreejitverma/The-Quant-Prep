---
type: monthly-review
date: 2026-10-18
month: "2026-10"
portfolio_return_pct: 0.00
benchmark_return_pct: 0.00
sharpe_ratio: 0.00
sortino_ratio: 0.00
max_drawdown_pct: 0.00
capital_gate_status: "compliant"
tags: [monthly-review, portfolio-audit, risk-governance]
---

# Monthly Portfolio and Risk Review: {{month}} ({{date}})

## 1. Executive Performance Summary
- **Portfolio Return**: {{portfolio_return_pct}}%
- **Benchmark Return (S&P 500 / NIFTY 50)**: {{benchmark_return_pct}}%
- **Active Alpha Return**: Calculated difference versus the passive benchmark.
- **Sharpe Ratio (Annualized)**: {{sharpe_ratio}}
- **Sortino Ratio (Downside Semi-Variance)**: {{sortino_ratio}}
- **Maximum Realized Drawdown**: {{max_drawdown_pct}}%
- **Capital Gate Status**: {{capital_gate_status}}

---

## 2. Asset Allocation and Return Attribution
| Asset Class / Sector | Beginning Weight (%) | Ending Weight (%) | Return Contribution (%) | Realized Volatility (%) |
|---|---|---|---|---|
| Equities (Discretionary & Factors) | 0.0% | 0.0% | 0.00% | 0.0% |
| Options & Volatility Overlay | 0.0% | 0.0% | 0.00% | 0.0% |
| Fixed Income & Sovereign Debt | 0.0% | 0.0% | 0.00% | 0.0% |
| Commodities & Futures Basis | 0.0% | 0.0% | 0.00% | 0.0% |
| Cash & Treasury Bills | 0.0% | 0.0% | 0.00% | 0.0% |

---

## 3. Factor Exposure and Risk Analysis
- **Value (HML)**: Net beta exposure to cheap versus expensive equities.
- **Momentum (WML)**: Net exposure to cross-sectional trend continuation.
- **Quality / Profitability (RMW)**: Net exposure to high ROIC, low-accrual businesses.
- **Size (SMB)**: Small-cap versus large-cap factor tilt.
- **Value at Risk (Historical 99% 1-Day VaR)**: Maximum estimated daily loss at the 99% confidence tier.

---

## 4. Capital Gate and Sample Size Compliance
- **Total Logged Sample Size**: Cumulative count of verified paper/live trades in trade journal.
- **Cumulative Profit Factor**: All-time profit factor across the trade sample.
- **Peak Drawdown Limit Check**: Verification that realized drawdown has not breached the 10.0% hard capital gate.
- **Rule Adherence Threshold**: All-time rule adherence rate (must remain >= 95.0% for live capital allocation).

---

## 5. Strategy and Playbook Contribution Matrix
- **Top Alpha Generating Strategy**: Strategy name, Sharpe contribution, and primary edge source.
- **Underperforming Strategy**: Strategy name, drag on portfolio return, and regime cause.
- **Retirement / Re-Calibration Candidates**: Any model or playbook whose empirical returns fail deflated Sharpe thresholds.

---

## 6. Infrastructure, Algorithmic Execution, and System Health
- **Uptime and Reliability**: Feed handler and order routing system uptime percentage.
- **Latency and Slippage Performance**: Average fill latency in milliseconds and slippage vs arrival benchmarks.
- **Data Quality Audits**: Point-in-time database integrity checks, corporate action adjustments, and missing tick logs.

---

## 7. Strategic Outlook and Parameter Calibration
- **Macro Regime Assessment**: Current phase of the business cycle, debt cycle, and interest rate trajectory.
- **Volatility Outlook**: Forward volatility expectations and implied versus realized volatility spreads.
- **Parameter Adjustments**: Approved updates to risk fractions, position limits, or stop thresholds for the subsequent month.
