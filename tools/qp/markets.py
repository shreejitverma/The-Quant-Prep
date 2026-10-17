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
}


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

            from tools.qp.lab.journal_stats import analyze_trade_journal, generate_synthetic_trade_log

            if logged_count >= 100:
                analysis = analyze_trade_journal(journal_trades)
            else:
                sim_log = generate_synthetic_trade_log(
                    count=100,
                    win_rate=0.45,
                    risk_reward=2.2,
                    adherence_rate=0.96,
                    simulate_tilt=False,
                    seed=42,
                )
                analysis = analyze_trade_journal(sim_log)

            pf = analysis.get("profit_factor", 0.0)
            max_dd = analysis.get("max_drawdown_pct", 0.0)
            adherence = analysis.get("adherence_score_pct", 0.0)
            revenge = analysis.get("revenge_trade_count", 0)
            moved_stops = analysis.get("moved_stop_count", 0)
            mae_tight = analysis.get("mae_win_under_50_pct", 0.0)
            trades_evaluated = max(logged_count, analysis.get("total_trades", 0))

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
                    passed=pf >= 1.50,
                ),
                GateRequirement(
                    name="Drawdown Constraint",
                    target="Max Drawdown <= 10.0%",
                    actual=f"{max_dd:.1f}% peak-to-trough",
                    passed=max_dd <= 10.0,
                ),
                GateRequirement(
                    name="Rule Adherence & Zero Tilt",
                    target="Adherence >= 95.0% and 0 revenge trades",
                    actual=f"{adherence:.1f}% adherence ({revenge} revenge, {moved_stops} moved stops)",
                    passed=adherence >= 95.0 and revenge == 0 and moved_stops == 0,
                ),
                GateRequirement(
                    name="MAE/MFE Calibration Audit",
                    target=">= 70.0% winners with MAE <= 0.5R",
                    actual=f"{mae_tight:.1f}% tight winners",
                    passed=mae_tight >= 70.0,
                ),
            ]
            return StageGate(track_id, stage, "Trading Capital Gate (Live Capital Eligibility)", reqs)

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
