"""Markets Mastery OS: Track definitions, stage progression, and automated stage gates.

Standard-library only, integrates with qp Store and Vault to verify
learner progression across quantitative prop trading and trading tracks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GateRequirement:
    name: str
    target: str
    actual: str
    passed: bool


@dataclass
class StageGate:
    track_id: str
    stage: str
    title: str
    requirements: list[GateRequirement] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.requirements) if self.requirements else False

    def to_dict(self) -> dict[str, Any]:
        return {
            "track_id": self.track_id,
            "stage": self.stage,
            "title": self.title,
            "passed": self.passed,
            "requirements": [
                {
                    "name": r.name,
                    "target": r.target,
                    "actual": r.actual,
                    "passed": r.passed,
                }
                for r in self.requirements
            ],
        }


TRACK_METADATA = {
    "track_0_pqt": {
        "id": "track_0_pqt",
        "name": "Professional Quant Trading",
        "description": "Desk roles, fair value, order flow, adverse selection, and inventory control.",
        "card_prefix": "mkt-pqt-",
    },
    "track_6_trd": {
        "id": "track_6_trd",
        "name": "Trading (Discretionary & Systematic)",
        "description": "Base rates, transaction costs, sizing, stops, setup taxonomy, and execution.",
        "card_prefix": "mkt-trd-",
    },
    "track_fa": {
        "id": "track_fa",
        "name": "Fundamental Analysis & Forensics",
        "description": "Three statements, ROIC, Sloan accruals, Beneish M-Score, and 10-K forensic audit.",
        "card_prefix": "mkt-fa-",
    },
    "track_val": {
        "id": "track_val",
        "name": "Valuation & Financial Modeling",
        "description": "DCF first principles, WACC mechanics, reverse DCF, multiples, and net-net liquidation.",
        "card_prefix": "mkt-val-",
    },
    "track_vi": {
        "id": "track_vi",
        "name": "Value Investing & Security Analysis",
        "description": "Margin of safety, owner earnings, capital cycle theory, second-level thinking, and special situations.",
        "card_prefix": "mkt-vi-",
    },
    "track_pf": {
        "id": "track_pf",
        "name": "Portfolio Management & Risk Allocation",
        "description": "Asset allocation benchmark, factor replication, drawdown mathematics, Kelly sizing, and Risk Parity.",
        "card_prefix": "mkt-pf-",
    },
    "track_opt": {
        "id": "track_opt",
        "name": "Options & Volatility Trading",
        "description": "Greeks hedging, volatility surfaces, dealer positioning, GEX, and variance trading.",
        "card_prefix": "mkt-opt-",
    },
    "track_ta": {
        "id": "track_ta",
        "name": "Technical Analysis & Market Profile",
        "description": "Auction theory, Volume Profile, VWAP, market internals, and empirical rule validation.",
        "card_prefix": "mkt-ta-",
    },
    "track_sys": {
        "id": "track_sys",
        "name": "Systematic Trading Systems",
        "description": "Cross-sectional momentum, risk parity, deflated Sharpe, CPCV, and production decision ledgers.",
        "card_prefix": "mkt-sys-",
    },
    "track_ind": {
        "id": "track_ind",
        "name": "Indian Markets Microstructure & F&O",
        "description": "NSE/BSE co-location, NIFTY/BANKNIFTY weeklys, STT taxation, and SEBI regulatory architecture.",
        "card_prefix": "mkt-ind-",
    },
    "track_mac": {
        "id": "track_mac",
        "name": "Macro Rates & FX Dynamics",
        "description": "Yield curve regimes, duration/convexity, central bank plumbing, and rates curve trading.",
        "card_prefix": "mkt-mac-",
    },
    "track_cmd": {
        "id": "track_cmd",
        "name": "Commodity Term Structures & Storage",
        "description": "Contango, backwardation, roll yield, convenience yield, and physical storage arbitrage.",
        "card_prefix": "mkt-cmd-",
    },
    "track_cry": {
        "id": "track_cry",
        "name": "Crypto Perpetuals & Funding Arbitrage",
        "description": "Perpetual futures, hourly funding rate carry, cross-venue basis arbitrage, and liquidations.",
        "card_prefix": "mkt-cry-",
    },
    "track_his": {
        "id": "track_his",
        "name": "Market Crises & Historical Event Studies",
        "description": "1929 through 2022 crises, liquidity evaporation, abnormal returns, and strategy pre-mortems.",
        "card_prefix": "mkt-his-",
    },
    "track_psy": {
        "id": "track_psy",
        "name": "Trading Psychology & Peak Performance",
        "description": "Tilt mitigation, loss aversion, cognitive biases, autonomic regulation, and execution discipline.",
        "card_prefix": "mkt-psy-",
    },
    "track_dec": {
        "id": "track_dec",
        "name": "Probability & Decision Making Under Uncertainty",
        "description": "Bayesian inference, expected value betting, cognitive traps, and probabilistic reasoning.",
        "card_prefix": "mkt-dec-",
    },
    "track_exe": {
        "id": "track_exe",
        "name": "Order Types & Algorithmic Execution",
        "description": "VWAP, TWAP, Almgren-Chriss optimal trajectories, implementation shortfall, and market impact.",
        "card_prefix": "mkt-exe-",
    },
    "track_reg": {
        "id": "track_reg",
        "name": "Regulation, Tax & Trading Operations",
        "description": "Reg NMS, MiFID II, STT tax optimization, trade break reconciliation, and post-trade settlement.",
        "card_prefix": "mkt-reg-",
    },
    "track_car": {
        "id": "track_car",
        "name": "Quantitative & Prop Trading Careers",
        "description": "Firm models (prop vs pod), QT/QR/QD roles, formulaic PnL payouts, and interview rubrics.",
        "card_prefix": "mkt-car-",
    },
}

LAB_ENGINES = {
    "games": "Mental Math & Market Making Games",
    "lob_sim": "Limit Order Book & Execution (TCA) Simulator",
    "mm_quote": "Avellaneda-Stoikov Market Maker Quoting",
    "pos_sizing": "Position Sizing, Kelly & Ruin Simulator",
    "opt_desk": "Options Volatility & Greeks Hedging",
    "replay_chart": "Interactive Blind Chart Replay & Brier Calibration",
    "overfit_trap": "Backtest Overfitting Trap & Deflated Sharpe",
    "journal_stats": "Trade Journal Analytics & Expectancy",
    "fut_desk": "Futures Term Structure & Basis Arbitrage",
    "port_alloc": "Multi-Asset Portfolio Allocator & Risk Parity",
    "event_study": "Historical Crisis Event Study & CAR Analysis",
}

PERSONA_CONFIGS = {
    "holistic": {
        "name": "Holistic Market Master",
        "description": "Comprehensive multi-disciplinary mastery across all quant, discretionary, macro, and fundamental disciplines.",
        "track_weights": {k: 1.0 for k in TRACK_METADATA},
        "required_engines": list(LAB_ENGINES.keys()),
    },
    "quant_trader": {
        "name": "Quantitative Trader (QT / Market Maker)",
        "description": "High-frequency quoting, adverse selection, order book mechanics, options Greeks, and market making games.",
        "track_weights": {
            "track_0_pqt": 2.5,
            "track_opt": 2.0,
            "track_exe": 2.0,
            "track_car": 1.5,
            "track_dec": 1.5,
            "track_ind": 1.0,
            "track_cry": 1.0,
            "track_sys": 1.0,
        },
        "required_engines": ["lob_sim", "mm_quote", "games", "opt_desk"],
    },
    "quant_researcher": {
        "name": "Quantitative Researcher (QR / Alpha Modeler)",
        "description": "Statistical signal discovery, backtest deflated Sharpe ratio, portfolio construction, and factor modeling.",
        "track_weights": {
            "track_sys": 3.0,
            "track_pf": 2.0,
            "track_opt": 1.5,
            "track_his": 1.5,
            "track_mac": 1.0,
            "track_car": 1.0,
            "track_cmd": 0.5,
        },
        "required_engines": ["overfit_trap", "port_alloc", "opt_desk", "event_study"],
    },
    "macro_derivatives_trader": {
        "name": "Macro & Derivatives Trader",
        "description": "Yield curves, rates trading, commodities term structure, options skew, and risk parity.",
        "track_weights": {
            "track_mac": 2.5,
            "track_cmd": 2.0,
            "track_opt": 2.0,
            "track_pf": 1.5,
            "track_his": 1.5,
            "track_ind": 1.0,
            "track_cry": 1.0,
        },
        "required_engines": ["fut_desk", "opt_desk", "port_alloc", "event_study"],
    },
    "retail_algorithmic_trader": {
        "name": "Discretionary & Systematic Algorithmic Trader",
        "description": "Expectancy, trade journal adherence, position sizing, setup taxonomy, tape reading, and discipline.",
        "track_weights": {
            "track_6_trd": 2.5,
            "track_ta": 2.0,
            "track_psy": 1.5,
            "track_dec": 1.5,
            "track_reg": 1.0,
            "track_fa": 1.0,
            "track_val": 1.0,
        },
        "required_engines": ["pos_sizing", "replay_chart", "journal_stats", "lob_sim"],
    },
}

PERSONA_CHOICES: list[str] = list(PERSONA_CONFIGS)


def get_card_count_for_prefix(cards: dict[str, Any], prefix: str) -> int:
    """Count how many cards matching the prefix exist in the vault."""
    return sum(1 for cid in cards if cid.startswith(prefix))


def evaluate_gate(
    track_id: str,
    stage: str,
    vault_cards: dict[str, Any] | None = None,
    store_state: dict[str, Any] | None = None,
) -> StageGate:
    """Evaluate whether a learner meets the criteria for a specific track and stage."""
    vault_cards = vault_cards or {}
    store_state = store_state or {}

    # Extract learner state metrics
    reviewed_cards = store_state.get("cards", {})
    lab_history = store_state.get("lab_history", [])

    if track_id == "track_0_pqt":
        if stage == "foundations":
            prefix = "mkt-pqt-"
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 64)
            # Default target to 64 if vault cards aren't fully loaded
            target_count = max(64, total_cards) if total_cards > 0 else 64
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 64
                and reviewed_cards[cid].get("reps", 0) > 0
            )

            # Check lab games
            game_sessions = [s for s in lab_history if s.get("engine") == "games"]
            best_score = max((s.get("metrics", {}).get("performance_score", 0.0) for s in game_sessions), default=0.0)

            reqs = [
                GateRequirement(
                    name="Track 0 Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
                GateRequirement(
                    name="Interview Trading Games Practice",
                    target="Performance score >= 60.0",
                    actual=f"{best_score:.1f} score",
                    passed=best_score >= 60.0,
                ),
            ]
            return StageGate(track_id, stage, "Pro Quant Foundations Gate", reqs)

        if stage == "core":
            prefix = "mkt-pqt-"
            total_core_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and 64 < int(cid.split("-")[-1]) <= 128)
            target_core = max(64, total_core_cards) if total_core_cards > 0 else 64
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 64 < int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )

            # LOB and MM executions
            lob_runs = sum(1 for s in lab_history if s.get("engine") == "lob_sim")
            mm_runs = sum(1 for s in lab_history if s.get("engine") == "mm_quote")

            reqs = [
                GateRequirement(
                    name="Track 0 Core Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core_cards > 0 else False,
                ),
                GateRequirement(
                    name="Limit Order Book Matching Simulation",
                    target=">= 1 lob_sim sessions completed",
                    actual=f"{lob_runs} sessions",
                    passed=lob_runs >= 1,
                ),
                GateRequirement(
                    name="Avellaneda-Stoikov Market Maker Quoting",
                    target=">= 1 mm_quote sessions completed",
                    actual=f"{mm_runs} sessions",
                    passed=mm_runs >= 1,
                ),
            ]
            return StageGate(track_id, stage, "Pro Quant Core Gate", reqs)

    elif track_id == "track_6_trd":
        if stage == "foundations":
            prefix = "mkt-trd-"
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 64)
            target_count = max(64, total_cards) if total_cards > 0 else 64
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 64
                and reviewed_cards[cid].get("reps", 0) > 0
            )

            # Sizing sessions
            sizing_runs = sum(1 for s in lab_history if s.get("engine") == "pos_sizing")

            reqs = [
                GateRequirement(
                    name="Track 6 Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
                GateRequirement(
                    name="Position Sizing & Ruin Simulation",
                    target=">= 1 pos_sizing sessions completed",
                    actual=f"{sizing_runs} sessions",
                    passed=sizing_runs >= 1,
                ),
            ]
            return StageGate(track_id, stage, "Trading Foundations Gate", reqs)

        if stage == "core":
            prefix = "mkt-trd-"
            total_core_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and 64 < int(cid.split("-")[-1]) <= 128)
            target_core = max(64, total_core_cards) if total_core_cards > 0 else 64
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 64 < int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )

            journal_trades = store_state.get("journal_trades", [])
            logged_count = len(journal_trades)

            reqs = [
                GateRequirement(
                    name="Track 6 Core Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core_cards > 0 else False,
                ),
                GateRequirement(
                    name="Documented Trade Plan Execution",
                    target=">= 5 planned trades logged",
                    actual=f"{logged_count} trades logged",
                    passed=logged_count >= 5,
                ),
            ]
            return StageGate(track_id, stage, "Trading Core Gate", reqs)

        if stage in ("capital_gate", "capital"):
            journal_trades = store_state.get("journal_trades", [])
            logged_count = len(journal_trades)

            from tools.qp.lab.journal_stats import analyze_trade_journal

            analysis = analyze_trade_journal(journal_trades)

            pf = analysis["profit_factor"]
            max_dd_r = analysis["max_drawdown_r"]
            adherence = analysis["adherence_score_pct"]
            revenge = analysis["revenge_trade_count"]
            moved_stops = analysis["moved_stop_count"]
            mae_tight = analysis["mae_win_under_50_pct"]
            trades_evaluated = logged_count

            reqs = [
                GateRequirement(
                    name="100-Trade Verified Sample",
                    target=">= 100 trades",
                    actual=f"{trades_evaluated} trades",
                    passed=trades_evaluated >= 100,
                ),
                GateRequirement(
                    name="Profit Factor Verification",
                    target="Profit Factor >= 1.50",
                    actual=f"{pf:.2f} PF",
                    passed=logged_count > 0 and pf >= 1.50,
                ),
                GateRequirement(
                    name="Drawdown Constraint",
                    target="Max Drawdown <= 10.0R",
                    actual=f"{max_dd_r:.1f}R peak-to-trough",
                    passed=logged_count > 0 and max_dd_r <= 10.0,
                ),
                GateRequirement(
                    name="Rule Adherence & Zero Tilt",
                    target="Adherence >= 95.0% and 0 revenge trades",
                    actual=f"{adherence:.1f}% adherence ({revenge} revenge, {moved_stops} moved stops)",
                    passed=logged_count > 0 and adherence >= 95.0 and revenge == 0 and moved_stops == 0,
                ),
                GateRequirement(
                    name="MAE/MFE Calibration Audit",
                    target=">= 70.0% winners with MAE <= 0.5R",
                    actual=f"{mae_tight:.1f}% tight winners",
                    passed=logged_count > 0 and mae_tight >= 70.0,
                ),
            ]
            return StageGate(track_id, stage, "Trading Capital Gate (Live Capital Eligibility)", reqs)

    elif track_id == "track_fa":
        prefix = "mkt-fa-"
        if stage == "foundations":
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 128)
            target_count = max(128, total_cards) if total_cards > 0 else 128
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Track FA Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
                GateRequirement(
                    name="Three-Statement & ROIC Analysis Fluency",
                    target=">= 64 cards reviewed with reps > 0",
                    actual=f"{passed_cards} cards completed",
                    passed=passed_cards >= 64,
                ),
            ]
            return StageGate(track_id, stage, "Fundamental Analysis Foundations Gate", reqs)

        if stage == "core":
            total_core = sum(1 for cid in vault_cards if cid.startswith(prefix) and 128 < int(cid.split("-")[-1]) <= 256)
            target_core = max(128, total_core) if total_core > 0 else 128
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 128 < int(cid.split("-")[-1]) <= 256
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            total_fa_reviewed = sum(
                1 for cid in reviewed_cards if cid.startswith(prefix) and cid in vault_cards and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Track FA Core Forensics Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core > 0 else False,
                ),
                GateRequirement(
                    name="Sloan Accruals & Beneish M-Score Screening",
                    target=">= 120 total FA cards reviewed",
                    actual=f"{total_fa_reviewed} total FA cards reviewed",
                    passed=total_fa_reviewed >= 120,
                ),
            ]
            return StageGate(track_id, stage, "Fundamental Analysis Core Gate", reqs)

    elif track_id == "track_val":
        prefix = "mkt-val-"
        if stage == "foundations":
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 128)
            target_count = max(128, total_cards) if total_cards > 0 else 128
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Track Valuation Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
                GateRequirement(
                    name="DCF & WACC Hurdle Rate Rigor",
                    target=">= 64 cards reviewed with reps > 0",
                    actual=f"{passed_cards} cards completed",
                    passed=passed_cards >= 64,
                ),
            ]
            return StageGate(track_id, stage, "Valuation Foundations Gate", reqs)

        if stage == "core":
            total_core = sum(1 for cid in vault_cards if cid.startswith(prefix) and 128 < int(cid.split("-")[-1]) <= 256)
            target_core = max(128, total_core) if total_core > 0 else 128
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 128 < int(cid.split("-")[-1]) <= 256
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            total_val_reviewed = sum(
                1 for cid in reviewed_cards if cid.startswith(prefix) and cid in vault_cards and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Track Valuation Core Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core > 0 else False,
                ),
                GateRequirement(
                    name="Reverse DCF & SOTP Conglomerate Rebuild",
                    target=">= 120 total Valuation cards reviewed",
                    actual=f"{total_val_reviewed} total Valuation cards reviewed",
                    passed=total_val_reviewed >= 120,
                ),
            ]
            return StageGate(track_id, stage, "Valuation Core Gate", reqs)

    elif track_id == "track_vi":
        prefix = "mkt-vi-"
        if stage == "foundations":
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 128)
            target_count = max(128, total_cards) if total_cards > 0 else 128
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Track Value Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
                GateRequirement(
                    name="Graham-Buffett Margin of Safety Discipline",
                    target=">= 64 cards reviewed with reps > 0",
                    actual=f"{passed_cards} cards completed",
                    passed=passed_cards >= 64,
                ),
            ]
            return StageGate(track_id, stage, "Value Investing Foundations Gate", reqs)

        if stage == "core":
            total_core = sum(1 for cid in vault_cards if cid.startswith(prefix) and 128 < int(cid.split("-")[-1]) <= 256)
            target_core = max(128, total_core) if total_core > 0 else 128
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 128 < int(cid.split("-")[-1]) <= 256
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            total_vi_reviewed = sum(
                1 for cid in reviewed_cards if cid.startswith(prefix) and cid in vault_cards and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Track Value Core Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core > 0 else False,
                ),
                GateRequirement(
                    name="Special Situations & Capital Cycle Traps",
                    target=">= 120 total Value cards reviewed",
                    actual=f"{total_vi_reviewed} total Value cards reviewed",
                    passed=total_vi_reviewed >= 120,
                ),
            ]
            return StageGate(track_id, stage, "Value Investing Core Gate", reqs)

    elif track_id == "track_pf":
        prefix = "mkt-pf-"
        if stage == "foundations":
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 128)
            target_count = max(128, total_cards) if total_cards > 0 else 128
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Track Portfolio Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
                GateRequirement(
                    name="Drawdown Risk & Sequence of Returns Safety",
                    target=">= 64 cards reviewed with reps > 0",
                    actual=f"{passed_cards} cards completed",
                    passed=passed_cards >= 64,
                ),
            ]
            return StageGate(track_id, stage, "Portfolio Management Foundations Gate", reqs)

        if stage == "core":
            total_core = sum(1 for cid in vault_cards if cid.startswith(prefix) and 128 < int(cid.split("-")[-1]) <= 256)
            target_core = max(128, total_core) if total_core > 0 else 128
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 128 < int(cid.split("-")[-1]) <= 256
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            total_pf_reviewed = sum(
                1 for cid in reviewed_cards if cid.startswith(prefix) and cid in vault_cards and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Track Portfolio Core Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core > 0 else False,
                ),
                GateRequirement(
                    name="Kelly Sizing & All Weather Risk Parity",
                    target=">= 120 total Portfolio cards reviewed",
                    actual=f"{total_pf_reviewed} total Portfolio cards reviewed",
                    passed=total_pf_reviewed >= 120,
                ),
            ]
            return StageGate(track_id, stage, "Portfolio Management Core Gate", reqs)

    elif track_id == "track_opt":
        prefix = "mkt-opt-"
        if stage == "foundations":
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 64)
            target_count = max(64, total_cards) if total_cards > 0 else 64
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 64
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Options Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
            ]
            return StageGate(track_id, stage, "Options & Volatility Foundations Gate", reqs)

        if stage == "core":
            total_core = sum(1 for cid in vault_cards if cid.startswith(prefix) and 64 < int(cid.split("-")[-1]) <= 128)
            target_core = max(64, total_core) if total_core > 0 else 64
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 64 < int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            opt_runs = sum(1 for s in lab_history if s.get("engine") == "opt_desk")
            reqs = [
                GateRequirement(
                    name="Options Volatility Core Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core > 0 else False,
                ),
                GateRequirement(
                    name="Options Volatility Desk Simulation",
                    target=">= 1 opt_desk sessions completed",
                    actual=f"{opt_runs} sessions",
                    passed=opt_runs >= 1,
                ),
            ]
            return StageGate(track_id, stage, "Options & Volatility Core Gate", reqs)

    elif track_id == "track_ta":
        prefix = "mkt-ta-"
        if stage == "foundations":
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 128)
            target_count = max(128, total_cards) if total_cards > 0 else 128
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Technical Analysis Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
            ]
            return StageGate(track_id, stage, "Technical Analysis Foundations Gate", reqs)

        if stage == "core":
            total_core = sum(1 for cid in vault_cards if cid.startswith(prefix) and 128 < int(cid.split("-")[-1]) <= 256)
            target_core = max(128, total_core) if total_core > 0 else 128
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 128 < int(cid.split("-")[-1]) <= 256
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            chart_runs = sum(1 for s in lab_history if s.get("engine") == "replay_chart")
            reqs = [
                GateRequirement(
                    name="Market Profile & Rule Validation Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core > 0 else False,
                ),
                GateRequirement(
                    name="Blind Chart Replay Calibration",
                    target=">= 1 replay_chart sessions completed",
                    actual=f"{chart_runs} sessions",
                    passed=chart_runs >= 1,
                ),
            ]
            return StageGate(track_id, stage, "Technical Analysis Core Gate", reqs)

    elif track_id == "track_sys":
        prefix = "mkt-sys-"
        if stage == "foundations":
            total_cards = sum(1 for cid in vault_cards if cid.startswith(prefix) and int(cid.split("-")[-1]) <= 128)
            target_count = max(128, total_cards) if total_cards > 0 else 128
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= 128
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name="Systematic Strategy Foundations Cards Mastered",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_cards > 0 else False,
                ),
            ]
            return StageGate(track_id, stage, "Systematic Trading Foundations Gate", reqs)

        if stage == "core":
            total_core = sum(1 for cid in vault_cards if cid.startswith(prefix) and 128 < int(cid.split("-")[-1]) <= 256)
            target_core = max(128, total_core) if total_core > 0 else 128
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and 128 < int(cid.split("-")[-1]) <= 256
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            trap_runs = sum(1 for s in lab_history if s.get("engine") == "overfit_trap")
            reqs = [
                GateRequirement(
                    name="Overfitting & CPCV Systems Cards Mastered",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_core > 0 else False,
                ),
                GateRequirement(
                    name="Deflated Sharpe Overfitting Trap Audit",
                    target=">= 1 overfit_trap sessions completed",
                    actual=f"{trap_runs} sessions",
                    passed=trap_runs >= 1,
                ),
            ]
            return StageGate(track_id, stage, "Systematic Trading Core Gate", reqs)

    # Specialized modules: Indian Markets, Macro, Commodities, Crypto, History, Psychology, Decision, Execution, Reg, Careers
    elif track_id in TRACK_METADATA:
        prefix = TRACK_METADATA[track_id]["card_prefix"]
        t_name = TRACK_METADATA[track_id]["name"]
        total_in_vault = sum(1 for cid in vault_cards if cid.startswith(prefix))
        split_point = max(1, total_in_vault // 2) if total_in_vault > 0 else 16

        if stage == "foundations":
            target_count = split_point
            passed_cards = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) <= split_point
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name=f"{t_name} Foundations Cards",
                    target=f"{target_count} cards",
                    actual=f"{passed_cards} cards reviewed",
                    passed=passed_cards >= target_count if total_in_vault > 0 else False,
                ),
            ]
            return StageGate(track_id, stage, f"{t_name} Foundations Gate", reqs)

        if stage == "core":
            target_core = total_in_vault - split_point if total_in_vault > split_point else split_point
            passed_core = sum(
                1
                for cid in reviewed_cards
                if cid.startswith(prefix)
                and cid in vault_cards
                and int(cid.split("-")[-1]) > split_point
                and reviewed_cards[cid].get("reps", 0) > 0
            )
            reqs = [
                GateRequirement(
                    name=f"{t_name} Core Cards",
                    target=f"{target_core} cards",
                    actual=f"{passed_core} cards reviewed",
                    passed=passed_core >= target_core if total_in_vault > 0 else False,
                ),
            ]
            return StageGate(track_id, stage, f"{t_name} Core Gate", reqs)

    # Fallback generic stage gate
    reqs = [
        GateRequirement(
            name="Stage Definition Pending",
            target="Complete prerequisite curriculum",
            actual="In review",
            passed=False,
        )
    ]
    return StageGate(track_id, stage, f"{track_id} {stage.title()} Gate", reqs)


def evaluate_all_markets_gates(
    vault_cards: dict[str, Any] | None = None,
    store_state: dict[str, Any] | None = None,
) -> dict[str, dict[str, StageGate]]:
    """Evaluate all implemented stage gates across Tracks."""
    out: dict[str, dict[str, StageGate]] = {}
    for tid in TRACK_METADATA:
        gates = {
            "foundations": evaluate_gate(tid, "foundations", vault_cards, store_state),
            "core": evaluate_gate(tid, "core", vault_cards, store_state),
        }
        if tid == "track_6_trd":
            gates["capital_gate"] = evaluate_gate(tid, "capital_gate", vault_cards, store_state)
        out[tid] = gates
    return out


def calculate_markets_mastery(
    vault_cards: dict[str, Any] | None = None,
    store_state: dict[str, Any] | None = None,
    persona: str = "holistic",
) -> dict[str, Any]:
    """Calculate holistic mastery across all pillars, engines, and gates for a given persona."""
    vault_cards = vault_cards or {}
    store_state = store_state or {}
    reviewed_cards = store_state.get("cards", {})
    lab_history = store_state.get("lab_history", [])

    if persona not in PERSONA_CONFIGS:
        persona = "holistic"
    p_config = PERSONA_CONFIGS[persona]

    track_stats: dict[str, Any] = {}
    total_markets_cards = 0
    total_markets_reviewed = 0
    total_markets_mature = 0

    for tid, meta in TRACK_METADATA.items():
        prefix = meta["card_prefix"]
        t_total = sum(1 for cid in vault_cards if cid.startswith(prefix))
        if t_total == 0 and tid in ("track_fa", "track_val", "track_vi", "track_pf"):
            t_total = 256
        t_reviewed = sum(1 for cid in reviewed_cards if cid.startswith(prefix) and reviewed_cards[cid].get("reps", 0) > 0)
        t_mature = sum(1 for cid in reviewed_cards if cid.startswith(prefix) and reviewed_cards[cid].get("interval", 0) >= 21)

        total_markets_cards += t_total
        total_markets_reviewed += t_reviewed
        total_markets_mature += t_mature

        cov = (t_reviewed / t_total) if t_total > 0 else 0.0
        ret = (
            (
                sum(
                    min(reviewed_cards[cid].get("interval", 0) / 21.0, 1.0)
                    for cid in reviewed_cards
                    if cid.startswith(prefix) and cid in vault_cards
                )
                / t_reviewed
            )
            if t_reviewed > 0
            else 0.0
        )

        mastery_pct = round((0.60 * cov + 0.40 * ret) * 100.0, 1)

        track_stats[tid] = {
            "name": meta["name"],
            "prefix": prefix,
            "total_cards": t_total,
            "reviewed_cards": t_reviewed,
            "mature_cards": t_mature,
            "coverage_pct": round(cov * 100.0, 1),
            "mastery_pct": mastery_pct,
        }

    # Persona-weighted card score
    weights = p_config["track_weights"]
    weighted_mastery_sum = sum(
        track_stats[tid]["mastery_pct"] * weights.get(tid, 0.0) for tid in TRACK_METADATA if weights.get(tid, 0.0) > 0
    )
    total_weight = sum(weights.get(tid, 0.0) for tid in TRACK_METADATA if weights.get(tid, 0.0) > 0)
    card_score = round(weighted_mastery_sum / total_weight, 1) if total_weight > 0 else 0.0

    # Lab engines progress
    engine_sessions: dict[str, int] = {e: 0 for e in LAB_ENGINES}
    for s in lab_history:
        eng = s.get("engine")
        if eng in engine_sessions:
            engine_sessions[eng] += 1

    completed_engines = [e for e, count in engine_sessions.items() if count > 0]
    req_engines = p_config["required_engines"]
    req_completed = [e for e in req_engines if engine_sessions.get(e, 0) > 0]

    req_pct = (len(req_completed) / len(req_engines) * 100.0) if req_engines else 100.0
    all_pct = len(completed_engines) / len(LAB_ENGINES) * 100.0
    lab_score = round(0.70 * req_pct + 0.30 * all_pct, 1)

    # Gates evaluation
    all_gates = evaluate_all_markets_gates(vault_cards, store_state)
    relevant_tracks = [t for t in TRACK_METADATA if weights.get(t, 0.0) > 0]
    total_gates_count = 0
    passed_gates_count = 0

    for tid in relevant_tracks:
        tg = all_gates.get(tid, {})
        for g in tg.values():
            total_gates_count += 1
            if g.passed:
                passed_gates_count += 1

    gate_score = round((passed_gates_count / total_gates_count * 100.0), 1) if total_gates_count > 0 else 0.0

    # Capital Gate
    cap_gate = evaluate_gate("track_6_trd", "capital_gate", vault_cards, store_state)

    # Overall Mastery Composite
    overall_score = round(0.50 * card_score + 0.30 * lab_score + 0.20 * gate_score, 1)

    if overall_score >= 80.0 and cap_gate.passed:
        readiness_level = "Elite / Live Desk Ready"
    elif overall_score >= 60.0:
        readiness_level = "Advanced Market Practitioner"
    elif overall_score >= 35.0:
        readiness_level = "Practitioner / Intermediate"
    else:
        readiness_level = "Novice / Foundations"

    # Actionable next steps
    next_actions = []
    sorted_unmastered = sorted(
        [tid for tid in relevant_tracks if track_stats[tid]["mastery_pct"] < 80.0],
        key=lambda tid: (track_stats[tid]["mastery_pct"], -weights.get(tid, 0.0)),
    )
    for tid in sorted_unmastered[:3]:
        next_actions.append(f"Review cards for {track_stats[tid]['name']} (currently {track_stats[tid]['mastery_pct']}% mastered)")

    unrun_engines = [e for e in req_engines if engine_sessions.get(e, 0) == 0]
    for e in unrun_engines[:2]:
        next_actions.append(f"Execute Trading Lab simulation engine: ./qp lab run {e}")

    if not cap_gate.passed and persona in ("retail_algorithmic_trader", "holistic"):
        next_actions.append("Log closed trades with `qp journal log` until the 100-trade Capital Gate passes (`qp journal` shows it)")

    return {
        "persona": persona,
        "persona_name": p_config["name"],
        "persona_description": p_config["description"],
        "overall_score": overall_score,
        "readiness_level": readiness_level,
        "card_score": card_score,
        "lab_score": lab_score,
        "gate_score": gate_score,
        "total_markets_cards": total_markets_cards,
        "total_markets_reviewed": total_markets_reviewed,
        "total_markets_mature": total_markets_mature,
        "track_stats": track_stats,
        "lab_stats": {
            "total_engines": len(LAB_ENGINES),
            "completed_engines": len(completed_engines),
            "required_engines_count": len(req_engines),
            "required_completed_count": len(req_completed),
            "engine_sessions": engine_sessions,
        },
        "gates_stats": {
            "total_gates": total_gates_count,
            "passed_gates": passed_gates_count,
            "capital_gate_passed": cap_gate.passed,
        },
        "next_actions": next_actions,
    }
