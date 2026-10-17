"""Study Board generator and mastery reporting engine for Markets Mastery OS.

Inspects learner state across all 19 market tracks, 11 simulation engines,
and 39 stage gates, generating an updated STUDY_BOARD.md dashboard.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from tools.qp.markets import (
    LAB_ENGINES,
    PERSONA_CONFIGS,
    calculate_markets_mastery,
    evaluate_all_markets_gates,
)
from tools.qp.state import Store
from tools.qp.vault import REPO_ROOT, load_vault


def build_study_board_markdown(
    holistic: dict,
    personas: dict[str, dict],
    all_gates: dict,
) -> str:
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    c_score = holistic["card_score"]
    c_status = "Satisfied" if c_score >= 80.0 else "In Progress"
    c_rev = holistic["total_markets_reviewed"]
    c_tot = holistic["total_markets_cards"]
    c_mat = holistic["total_markets_mature"]

    l_comp = holistic["lab_stats"]["completed_engines"]
    l_tot = holistic["lab_stats"]["total_engines"]
    l_status = "Satisfied" if l_comp == l_tot else "In Progress"

    g_pass = holistic["gates_stats"]["passed_gates"]
    g_tot = holistic["gates_stats"]["total_gates"]
    g_status = "Satisfied" if g_pass == g_tot else "In Progress"

    cap_passed = holistic["gates_stats"]["capital_gate_passed"]
    cap_actual = "Passed" if cap_passed else "Pending Paper Sample"
    cap_status = "PASSED" if cap_passed else "PENDING"

    lines = [
        "---",
        "type: moc",
        'title: "Markets Mastery OS - Live Study Board & Progression Dashboard"',
        "track: [quant-trader, quant-research, quant-risk]",
        "tier: core",
        "status: solid",
        "tags: [study-board, mastery-dashboard, capital-gate, progress, analytics]",
        "---",
        "",
        "# Markets Mastery OS - Live Study Board & Progression Dashboard",
        "",
        "Markets Mastery OS integrates quantitative finance, market microstructure, and systematic strategy research.",
        (
            f"This study board tracks real-time progress across 19 curriculum pillars, "
            f"{l_tot} simulation engines, and 39 automated stage gates (last updated: {now_utc})."
        ),
        "",
        "---",
        "",
        "## TL;DR",
        "",
        "The Markets Mastery OS study board quantifies learner readiness through transparent mathematical formulas.",
        "Mastery integrates spaced-repetition retention, interactive lab simulation sessions, and disciplined stage gate progression.",
        (
            f"Overall curriculum scope encompasses {c_tot} cards, "
            f"{l_tot} pure-Python simulation engines, and a verifiable 100-trade capital gate."
        ),
        "",
        "---",
        "",
        "## 1. Holistic Mastery Overview",
        "",
        "| Metric | Target | Actual State | Status |",
        "| :--- | :--- | :--- | :--- |",
        f"| **Overall Composite Score** | >= 80.0% | {holistic['overall_score']:.1f}% | {holistic['readiness_level']} |",
        f"| **Card Retention & Mastery** | >= 80.0% | {c_score:.1f}% ({c_rev}/{c_tot} cards, {c_mat} mature) | {c_status} |",
        f"| **Simulation Engine Execution** | {l_tot}/{l_tot} Engines | {l_comp}/{l_tot} engines executed | {l_status} |",
        f"| **Automated Stage Gates** | 39 Gates | {g_pass}/{g_tot} gates passed | {g_status} |",
        f"| **Capital Gate Eligibility** | 100 trades, PF >= 1.50, DD <= 10% | {cap_actual} | {cap_status} |",
        "",
        "---",
        "",
        "## 2. Persona-Specific Readiness Scores",
        "",
        "Learners can orient their progression toward one of four distinct market archetypes:",
        "",
        "| Persona Archetype | Focal Mandate | Overall Score | Readiness Level | Lab Coverage |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    for p_id, p_data in personas.items():
        if p_id == "holistic":
            continue
        req_c = p_data["lab_stats"]["required_completed_count"]
        req_t = p_data["lab_stats"]["required_engines_count"]
        lines.append(
            f"| **{p_data['persona_name']}** | {p_data['persona_description']} | "
            f"{p_data['overall_score']:.1f}% | {p_data['readiness_level']} | {req_c}/{req_t} Required |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 3. Curriculum Pillar Mastery Breakdown",
            "",
            "| Pillar ID | Pillar Name | Card Prefix | Cards Total | Reviewed | Mature | Mastery % | Stage Gate Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
    )

    for tid, tinfo in holistic["track_stats"].items():
        gates = all_gates.get(tid, {})
        f_gate = "Pass" if gates.get("foundations") and gates["foundations"].passed else "Pend"
        c_gate = "Pass" if gates.get("core") and gates["core"].passed else "Pend"
        gate_summary = f"F: {f_gate} / C: {c_gate}"
        if tid == "track_6_trd":
            cap_stat = "Pass" if gates.get("capital_gate") and gates["capital_gate"].passed else "Pend"
            gate_summary += f" / Cap: {cap_stat}"

        lines.append(
            f"| `{tid}` | {tinfo['name']} | `{tinfo['prefix']}` | {tinfo['total_cards']} | "
            f"{tinfo['reviewed_cards']} | {tinfo['mature_cards']} | {tinfo['mastery_pct']:.1f}% | {gate_summary} |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 4. Trading Lab Simulation Engines",
            "",
            f"The Trading Lab contains {l_tot} pure-Python standard-library simulation engines located in `tools/qp/lab/`.",
            "",
            "| Engine ID | Name | Sessions Run | Status | Quick CLI Command |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
    )

    for eng_id, eng_name in LAB_ENGINES.items():
        runs = holistic["lab_stats"]["engine_sessions"].get(eng_id, 0)
        status_str = f"Active ({runs} runs)" if runs > 0 else "Unrun"
        lines.append(f"| `{eng_id}` | {eng_name} | {runs} | {status_str} | `./qp lab run {eng_id}` |")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 5. Capital Gate and Trading Journal Audit",
            "",
            "> [!IMPORTANT]",
            (
                "> Transitioning from paper simulation to live capital requires "
                "completing the 100-trade journal sample gate with zero rule violations."
            ),
            "",
            "### Key Criteria for Live Deployment",
            "- **Sample Depth**: Minimum 100 documented trades executed according to pre-registered setup rules.",
            "- **Profit Factor**: Realized Gross Profit / Realized Gross Loss >= 1.50 across the sample.",
            "- **Maximum Drawdown**: Realized portfolio peak-to-trough equity decline <= 10.0%.",
            "- **Strict Rule Adherence**: >= 95.0% trade adherence score with 0 revenge trades and 0 moved stop losses.",
            "- **MAE/MFE Efficiency**: >= 70.0% of winning trades experiencing Maximum Adverse Excursion <= 0.5R.",
            "",
            "---",
            "",
            "## 6. Recommended Next Actions",
            "",
        ]
    )

    for action in holistic["next_actions"]:
        lines.append(f"- {action}")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 7. Navigation and Quick Links",
            "",
            "- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]",
            "- **Trading Styles**: [[16-Trading-and-Investing/07-Trading-Styles/_Index_Trading_Styles|Trading Styles Guide]]",
            "- **Execution Microstructure**: [[16-Trading-and-Investing/08-Execution-Microstructure/_Index_Execution|Execution]]",
            "- **Crisis Case Studies**: [[16-Trading-and-Investing/20-History-and-Events/_Index_History_Events|Historical Crises]]",
            "- **Interactive Web Lab**: Run `./qp serve` and open `tools/qp/lab/web/index.html`",
            "",
        ]
    )

    return "\n".join(lines)


def write_study_board(output_path: Path | None = None) -> Path:
    vault = load_vault(REPO_ROOT)
    store = Store()

    all_gates = evaluate_all_markets_gates(vault.cards, store.data)

    personas = {}
    for p_id in PERSONA_CONFIGS:
        personas[p_id] = calculate_markets_mastery(vault.cards, store.data, p_id)

    holistic = personas["holistic"]

    study_board_md = build_study_board_markdown(holistic, personas, all_gates)
    target = output_path or (REPO_ROOT / "16-Trading-and-Investing" / "STUDY_BOARD.md")
    target.write_text(study_board_md, encoding="utf-8")
    return target


def main() -> int:
    target = write_study_board()
    vault = load_vault(REPO_ROOT)
    store = Store()
    holistic = calculate_markets_mastery(vault.cards, store.data, "holistic")

    print(f"study_board: generated {target}")
    print(f"Overall Score: {holistic['overall_score']:.1f}% ({holistic['readiness_level']})")
    print(f"Cards: {holistic['total_markets_reviewed']}/{holistic['total_markets_cards']} reviewed")
    print(f"Engines: {holistic['lab_stats']['completed_engines']}/{holistic['lab_stats']['total_engines']} completed")
    print(f"Gates: {holistic['gates_stats']['passed_gates']}/{holistic['gates_stats']['total_gates']} passed")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
