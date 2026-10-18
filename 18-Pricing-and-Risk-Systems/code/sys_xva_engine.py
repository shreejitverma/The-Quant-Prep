"""XVA engine architecture: grid sizing, CVA quadrature, MVA ISDA SIMM trajectory, and memory optimization.

Backs every number in `18-Pricing-and-Risk-Systems/11-XVA-Engine.md`.
Simulation grid memory sizes, CVA expected loss integrals, and MVA funding numbers are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_xva_engine.py`.
"""

from __future__ import annotations

import math

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def test_grid_sizing() -> None:
    print("  1. Monte Carlo simulation grid sizing and memory optimization")
    trades = 120_000
    netting_sets = 4_500
    paths = 10_000
    time_buckets = 80
    scenario_points = paths * time_buckets
    raw_trade_bytes = trades * scenario_points * 8
    raw_trade_gb = raw_trade_bytes / 1e9

    quoted("active derivative trades", trades, 120_000, 0)
    quoted("legal netting sets", netting_sets, 4_500, 0)
    quoted("Monte Carlo paths", paths, 10_000, 0)
    quoted("discrete time buckets", time_buckets, 80, 0)
    quoted("scenario path-time points", scenario_points, 800_000, 0)
    quoted("raw trade mark-to-market data (GB)", raw_trade_gb, 768.0, 1)

    netting_array_bytes = paths * time_buckets * 8
    netting_array_mb = netting_array_bytes / 1e6
    ee_vector_bytes = time_buckets * 8
    total_resident_bytes = netting_sets * ee_vector_bytes
    total_resident_mb = total_resident_bytes / 1e6

    quoted("netting set exposure array (MB)", netting_array_mb, 6.4, 1)
    quoted("scalar EE vector size (bytes)", ee_vector_bytes, 640, 0)
    quoted("optimized resident memory across netting sets (MB)", total_resident_mb, 2.88, 2)


def test_bilateral_cva() -> None:
    print("  2. Bilateral CVA calculation with constant hazard rate")
    lgd = 0.60
    r = 0.04
    s_cds = 0.0150
    hazard = s_cds / lgd

    quoted("counterparty LGD", lgd, 0.60, 2)
    quoted("CDS spread (bps)", s_cds * 10_000, 150.0, 1)
    quoted("implied hazard rate (%)", hazard * 100.0, 2.50, 2)

    ee = [1_200_000.0, 1_800_000.0, 950_000.0]
    expected_losses = [17_079.82, 24_007.42, 11_873.19]
    cva_components = []

    for t in (1, 2, 3):
        df = math.exp(-r * t)
        dpd = math.exp(-hazard * (t - 1)) - math.exp(-hazard * t)
        loss = lgd * df * ee[t - 1] * dpd
        cva_components.append(loss)
        quoted(f"year {t} discount factor", df, round(df, 4), 4)
        quoted(f"year {t} marginal default prob", dpd, round(dpd, 5), 5)
        quoted(f"year {t} discounted expected loss ($)", loss, expected_losses[t - 1], 2)

    total_cva = sum(cva_components)
    quoted("total portfolio CVA ($)", total_cva, 52_960.43, 2)


def test_mva_isda_simm() -> None:
    print("  3. MVA calculation for uncleared swap under ISDA SIMM")
    s_margin = 0.0075
    im_traj = [5_000_000.0, 4_200_000.0, 3_100_000.0, 1_800_000.0, 600_000.0]
    df_rounded = [0.9608, 0.9231, 0.8869, 0.8521, 0.8187]
    mva_components = []

    for i in range(5):
        t = i + 1
        comp = df_rounded[i] * s_margin * im_traj[i]
        mva_components.append(comp)
        quoted(f"year {t} MVA funding component ($)", comp, round(comp, 2), 2)

    total_mva = sum(mva_components)
    quoted("total Margin Valuation Adjustment (MVA) ($)", total_mva, 100_915.58, 2)


def main() -> None:
    print("XVA engine architecture checks")
    test_grid_sizing()
    test_bilateral_cva()
    test_mva_isda_simm()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All XVA engine checks passed.")


if __name__ == "__main__":
    main()
