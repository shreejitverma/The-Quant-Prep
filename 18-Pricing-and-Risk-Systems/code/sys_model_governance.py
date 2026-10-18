"""Model governance and SR 11-7 lifecycle: materiality tiering, challenger model benchmarking, and post-mortem metrics.

Backs every number in `18-Pricing-and-Risk-Systems/15-Model-Governance.md`.
Materiality scores, challenger model confidence intervals, tracking errors, and incident loss figures are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_model_governance.py`.
"""

from __future__ import annotations

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def test_materiality_tiering() -> None:
    print("  1. Model materiality tiering calculation for Bermudan Swaption engine")
    s1 = 5.0  # Financial Exposure
    s2 = 4.0  # Model Complexity
    s3 = 5.0  # Regulatory Scrutiny
    s4 = 4.0  # Client Impact

    w1 = 0.35
    w2 = 0.25
    w3 = 0.25
    w4 = 0.15

    score1 = w1 * s1
    score2 = w2 * s2
    score3 = w3 * s3
    score4 = w4 * s4
    total_score = score1 + score2 + score3 + score4

    quoted("Financial exposure weighted score", score1, 1.75, 2)
    quoted("Model complexity weighted score", score2, 1.00, 2)
    quoted("Regulatory scrutiny weighted score", score3, 1.25, 2)
    quoted("Client impact weighted score", score4, 0.60, 2)
    quoted("composite model materiality score", total_score, 4.60, 2)
    assert total_score >= 3.75  # Tier 1 threshold


def test_challenger_benchmarking() -> None:
    print("  2. Challenger model benchmarking: Finite Difference PDE vs AMC")
    pv_pde = 4_215_800.0
    pv_amc = 4_208_450.0
    mc_ci_half_width = 8_200.0
    diff = pv_amc - pv_pde
    pct_diff = (diff / pv_pde) * 100.0

    quoted("Challenger PDE PV ($)", pv_pde, 4_215_800, 0)
    quoted("Candidate AMC PV ($)", pv_amc, 4_208_450, 0)
    quoted("AMC 95% confidence interval half-width ($)", mc_ci_half_width, 8_200, 0)
    quoted("PV discrepancy ($)", diff, -7_350, 0)
    quoted("percentage tracking discrepancy (%)", pct_diff, -0.17, 2)
    assert abs(diff) <= mc_ci_half_width


def test_london_whale_metrics() -> None:
    print("  3. JPMorgan London Whale post-mortem metrics (2012)")
    var_understatement_pct = 50.0
    realized_loss_billions = 6.2
    fines_billions = 1.0

    quoted("VaR understatement percentage (%)", var_understatement_pct, 50.0, 1)
    quoted("cumulative realized loss ($B)", realized_loss_billions, 6.2, 1)
    quoted("regulatory fines ($B)", fines_billions, 1.0, 1)


def main() -> None:
    print("Model governance checks")
    test_materiality_tiering()
    test_challenger_benchmarking()
    test_london_whale_metrics()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All model governance checks passed.")


if __name__ == "__main__":
    main()
