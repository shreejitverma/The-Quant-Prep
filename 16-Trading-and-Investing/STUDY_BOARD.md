---
type: moc
title: "Markets Mastery OS - Live Study Board & Progression Dashboard"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [study-board, mastery-dashboard, capital-gate, progress, analytics]
---

# Markets Mastery OS - Live Study Board & Progression Dashboard

Markets Mastery OS integrates quantitative finance, market microstructure, and systematic strategy research.
This study board tracks real-time progress across 19 curriculum pillars, 12 simulation engines, and 39 automated stage gates (last updated: 2026-10-17 02:44 UTC).

---

## TL;DR

The Markets Mastery OS study board quantifies learner readiness through transparent mathematical formulas.
Mastery integrates spaced-repetition retention, interactive lab simulation sessions, and disciplined stage gate progression.
Overall curriculum scope encompasses 2248 cards, 12 pure-Python simulation engines, and a verifiable 100-trade capital gate.

---

## 1. Holistic Mastery Overview

| Metric | Target | Actual State | Status |
| :--- | :--- | :--- | :--- |
| **Overall Composite Score** | >= 80.0% | 0.0% | Novice / Foundations |
| **Card Retention & Mastery** | >= 80.0% | 0.0% (0/2248 cards, 0 mature) | In Progress |
| **Simulation Engine Execution** | 12/12 Engines | 0/12 engines executed | In Progress |
| **Automated Stage Gates** | 39 Gates | 0/39 gates passed | In Progress |
| **Capital Gate Eligibility** | 100 trades, PF >= 1.50, DD <= 10% | Pending Paper Sample | PENDING |

---

## 2. Persona-Specific Readiness Scores

Learners can orient their progression toward one of four distinct market archetypes:

| Persona Archetype | Focal Mandate | Overall Score | Readiness Level | Lab Coverage |
| :--- | :--- | :--- | :--- | :--- |
| **Quantitative Trader (QT / Market Maker)** | High-frequency quoting, adverse selection, order book mechanics, options Greeks, and market making games. | 0.0% | Novice / Foundations | 0/5 Required |
| **Quantitative Researcher (QR / Alpha Modeler)** | Statistical signal discovery, backtest deflated Sharpe ratio, portfolio construction, and factor modeling. | 0.0% | Novice / Foundations | 0/4 Required |
| **Macro & Derivatives Trader** | Yield curves, rates trading, commodities term structure, options skew, and risk parity. | 0.0% | Novice / Foundations | 0/4 Required |
| **Discretionary & Systematic Algorithmic Trader** | Expectancy, trade journal adherence, position sizing, setup taxonomy, tape reading, and discipline. | 0.0% | Novice / Foundations | 0/4 Required |

---

## 3. Curriculum Pillar Mastery Breakdown

| Pillar ID | Pillar Name | Card Prefix | Cards Total | Reviewed | Mature | Mastery % | Stage Gate Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `track_0_pqt` | Professional Quant Trading | `mkt-pqt-` | 128 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_6_trd` | Trading (Discretionary & Systematic) | `mkt-trd-` | 128 | 0 | 0 | 0.0% | F: Pend / C: Pend / Cap: Pend |
| `track_fa` | Fundamental Analysis & Forensics | `mkt-fa-` | 256 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_val` | Valuation & Financial Modeling | `mkt-val-` | 256 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_vi` | Value Investing & Security Analysis | `mkt-vi-` | 256 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_pf` | Portfolio Management & Risk Allocation | `mkt-pf-` | 256 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_opt` | Options & Volatility Trading | `mkt-opt-` | 128 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_ta` | Technical Analysis & Market Profile | `mkt-ta-` | 256 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_sys` | Systematic Trading Systems | `mkt-sys-` | 256 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_ind` | Indian Markets Microstructure & F&O | `mkt-ind-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_mac` | Macro Rates & FX Dynamics | `mkt-mac-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_cmd` | Commodity Term Structures & Storage | `mkt-cmd-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_cry` | Crypto Perpetuals & Funding Arbitrage | `mkt-cry-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_his` | Market Crises & Historical Event Studies | `mkt-his-` | 40 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_psy` | Trading Psychology & Peak Performance | `mkt-psy-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_dec` | Probability & Decision Making Under Uncertainty | `mkt-dec-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_exe` | Order Types & Algorithmic Execution | `mkt-exe-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_reg` | Regulation, Tax & Trading Operations | `mkt-reg-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |
| `track_car` | Quantitative & Prop Trading Careers | `mkt-car-` | 32 | 0 | 0 | 0.0% | F: Pend / C: Pend |

---

## 4. Trading Lab Simulation Engines

The Trading Lab contains 12 pure-Python standard-library simulation engines located in `tools/qp/lab/`.

| Engine ID | Name | Sessions Run | Status | Quick CLI Command |
| :--- | :--- | :--- | :--- | :--- |
| `games` | Mental Math & Market Making Games | 0 | Unrun | `./qp lab run games` |
| `lob_sim` | Limit Order Book Matching Simulator | 0 | Unrun | `./qp lab run lob_sim` |
| `mm_quote` | Avellaneda-Stoikov Market Maker Quoting | 0 | Unrun | `./qp lab run mm_quote` |
| `pos_sizing` | Position Sizing, Kelly & Ruin Simulator | 0 | Unrun | `./qp lab run pos_sizing` |
| `options_lab` | Options Volatility & Greeks Hedging | 0 | Unrun | `./qp lab run options_lab` |
| `tca_engine` | Transaction Cost Analysis & Optimal Execution | 0 | Unrun | `./qp lab run tca_engine` |
| `replay_chart` | Interactive Blind Chart Replay & Brier Calibration | 0 | Unrun | `./qp lab run replay_chart` |
| `overfit_trap` | Backtest Overfitting Trap & Deflated Sharpe | 0 | Unrun | `./qp lab run overfit_trap` |
| `journal_stats` | Trade Journal Analytics & Expectancy | 0 | Unrun | `./qp lab run journal_stats` |
| `fut_desk` | Futures Term Structure & Basis Arbitrage | 0 | Unrun | `./qp lab run fut_desk` |
| `port_alloc` | Multi-Asset Portfolio Allocator & Risk Parity | 0 | Unrun | `./qp lab run port_alloc` |
| `event_study` | Historical Crisis Event Study & CAR Analysis | 0 | Unrun | `./qp lab run event_study` |

---

## 5. Capital Gate and Trading Journal Audit

> [!IMPORTANT]
> Transitioning from paper simulation to live capital requires completing the 100-trade journal sample gate with zero rule violations.

### Key Criteria for Live Deployment
- **Sample Depth**: Minimum 100 documented trades executed according to pre-registered setup rules.
- **Profit Factor**: Realized Gross Profit / Realized Gross Loss >= 1.50 across the sample.
- **Maximum Drawdown**: Realized portfolio peak-to-trough equity decline <= 10.0%.
- **Strict Rule Adherence**: >= 95.0% trade adherence score with 0 revenge trades and 0 moved stop losses.
- **MAE/MFE Efficiency**: >= 70.0% of winning trades experiencing Maximum Adverse Excursion <= 0.5R.

---

## 6. Recommended Next Actions

- Review cards for Professional Quant Trading (currently 0.0% mastered)
- Review cards for Trading (Discretionary & Systematic) (currently 0.0% mastered)
- Review cards for Fundamental Analysis & Forensics (currently 0.0% mastered)
- Execute Trading Lab simulation engine: ./qp lab run games
- Execute Trading Lab simulation engine: ./qp lab run lob_sim
- Complete 100-trade journal logging and pass Capital Gate rule adherence

---

## 7. Navigation and Quick Links

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Trading Styles**: [[16-Trading-and-Investing/07-Trading-Styles/_Index_Trading_Styles|Trading Styles Guide]]
- **Execution Microstructure**: [[16-Trading-and-Investing/08-Execution-Microstructure/_Index_Execution|Execution]]
- **Crisis Case Studies**: [[16-Trading-and-Investing/20-History-and-Events/_Index_History_Events|Historical Crises]]
- **Interactive Web Lab**: Run `./qp serve` and open `tools/qp/lab/web/index.html`
