"""FRTB engine: nightly compute sizing, PLA test statistics, and a bank-level capital walk through the ACR formula.

Backs every number in `18-Pricing-and-Risk-Systems/10-FRTB-Engine.md`.
Portfolio sizes, unit costs, desk P&L series and capital inputs are labelled-hypothetical; regulatory constants are
from the Basel Framework (MAR32.9, MAR32.19, MAR32.35 to MAR32.42, MAR33.4, MAR33.41 to MAR33.46).
PLA statistics are computed from simulated P&L series and checked by a second, independent method (Spearman by the
rank-difference formula against Pearson on ranks; KS by a merge against brute-force evaluation at every observation).
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_frtb_engine.py`.
"""

from __future__ import annotations

import math
import random

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Nightly sizing (hypothetical bank)
# ============================================================================


def check_sizing() -> None:
    print("  1. Nightly FRTB compute sizing (hypothetical bank)")
    positions, scenarios = 250_000, 250
    calibrations, lh_sets = 3, 5  # ES_F,C, ES_R,C, ES_R,S; liquidity-horizon subsets j = 1..5 (MAR33.4, MAR33.6)
    es_vectors = calibrations * lh_sets
    es_revals = positions * scenarios * es_vectors
    quoted("ES scenario vectors per position per day", es_vectors, 15, 0)
    quoted("daily ES revaluations", es_revals, 937_500_000, 0)
    var_revals = positions * scenarios  # one-day VaR on current data for backtesting (MAR32.18)
    rtpl_revals = positions  # T-1 positions on today's market in the risk engine
    quoted("daily one-day VaR revaluations for backtesting", var_revals, 62_500_000, 0)
    sa_sens = positions * 4  # adjoint sensitivities at a hypothetical cost of 4 valuations per position
    curvature = int(50_000 * 1.5 * 2)  # 50,000 options, 1.5 curvature factors each, up and down shocks
    nmrf = 3_500 * 40 * 2  # 3,500 NMRF stress scenarios, 40 exposed positions each, up and down
    quoted("SA sensitivity cost in valuations", sa_sens, 1_000_000, 0)
    quoted("SA curvature revaluations", curvature, 150_000, 0)
    quoted("NMRF stress scenario revaluations", nmrf, 280_000, 0)
    daily = es_revals + var_revals + rtpl_revals + sa_sens + curvature + nmrf
    quoted("daily valuations in total", daily, 1_001_680_000, 0)
    secs = daily * 0.0005  # 0.5 ms per valuation, hypothetical
    quoted("serial CPU time (hours)", secs / 3600, 139.1, 1)
    cores = secs / 7_200
    quoted("cores to finish in a 2-hour window", cores, 69.6, 1)
    quoted("cores with 50% headroom, rounded up", math.ceil(cores * 1.5), 105, 0)
    # weekly: risk-class partial ES for positions exposed to two risk classes (MAR33.14, MAR33.15 FAQ1)
    weekly = int(positions * 0.20) * 2 * es_vectors * scenarios
    quoted("weekly partial-ES revaluations, 20% of positions in two classes", weekly, 375_000_000, 0)


# ============================================================================
# 2. PLA test statistics
# ============================================================================


def ranks(x: list[float]) -> list[int]:
    order = sorted(range(len(x)), key=lambda i: x[i])
    r = [0] * len(x)
    for pos, i in enumerate(order, start=1):
        r[i] = pos
    return r


def spearman_rank_difference(a: list[float], b: list[float]) -> float:
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    return 1.0 - 6.0 * sum((x - y) ** 2 for x, y in zip(ra, rb, strict=True)) / (n * (n * n - 1))


def pearson(a: list[float], b: list[float]) -> float:
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b, strict=True))
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return cov / math.sqrt(va * vb)


def ks_merge(a: list[float], b: list[float]) -> float:
    """Two-sample KS by walking both sorted samples once."""
    sa, sb = sorted(a), sorted(b)
    i = j = 0
    best = 0.0
    while i < len(sa) and j < len(sb):
        x = min(sa[i], sb[j])
        while i < len(sa) and sa[i] <= x:
            i += 1
        while j < len(sb) and sb[j] <= x:
            j += 1
        best = max(best, abs(i / len(sa) - j / len(sb)))
    return best


def ks_brute(a: list[float], b: list[float]) -> float:
    """MAR32.39 to MAR32.41 literally: ECDF = 0.004 x count at or below, at every P&L value."""
    out = 0.0
    for x in a + b:
        fa = 0.004 * sum(1 for v in a if v <= x)
        fb = 0.004 * sum(1 for v in b if v <= x)
        out = max(out, abs(fa - fb))
    return out


def ks_pvalue(ks: float, n1: int, n2: int) -> float:
    lam = ks * math.sqrt(n1 * n2 / (n1 + n2))
    return 2.0 * sum((-1) ** (k - 1) * math.exp(-2.0 * k * k * lam * lam) for k in range(1, 101))


def zone(rs: float, ks: float) -> str:
    if rs > 0.80 and ks < 0.09:
        return "green"
    if rs < 0.70 or ks > 0.12:
        return "red"
    return "amber"


def desk_series(seed: int, basis_weight: float, scale_err: float) -> tuple[list[float], list[float]]:
    """250 days of HPL; RTPL misses a basis factor (weight basis_weight) and mis-scales vega P&L by scale_err."""
    rng = random.Random(seed)
    hpl, rtpl = [], []
    for _ in range(250):
        delta = rng.gauss(0.0, 1.0)
        vega = rng.gauss(0.0, 0.6)
        basis = rng.gauss(0.0, 1.0)
        hpl.append(delta + vega + basis_weight * basis)
        rtpl.append(delta + (1.0 + scale_err) * vega)
    return hpl, rtpl


def check_pla() -> None:
    print("  2. PLA test statistics on simulated desks (250 days, hypothetical)")
    quoted("ECDF step size, 1/250", 1 / 250, 0.004, 3)
    quoted("KS 0.12 in steps of 0.004", 0.12 / 0.004, 30.0, 6)
    quoted("KS 0.09 in steps of 0.004", 0.09 / 0.004, 22.5, 6)
    quoted("asymptotic p-value at KS 0.09 (MAR32.42 quotes 0.264)", ks_pvalue(0.09, 250, 250), 0.2634, 4)
    quoted("asymptotic p-value at KS 0.12 (MAR32.42 quotes 0.055)", ks_pvalue(0.12, 250, 250), 0.0546, 4)
    assert zone(0.80, 0.05) == "amber" and zone(0.85, 0.12) == "amber" and zone(0.85, 0.124) == "red"
    for name, seed, bw, se, rs_q, ks_q, z_q in (
        ("rates desk", 3, 0.20, 0.00, 0.981, 0.060, "green"),
        ("FX options desk", 5, 0.70, -0.50, 0.846, 0.116, "amber"),
        ("credit desk", 3, 1.10, -0.60, 0.707, 0.136, "red"),
    ):
        hpl, rtpl = desk_series(seed, bw, se)
        rs = spearman_rank_difference(hpl, rtpl)
        assert abs(rs - pearson([float(v) for v in ranks(hpl)], [float(v) for v in ranks(rtpl)])) < 1e-12
        ks = ks_merge(hpl, rtpl)
        assert abs(ks - ks_brute(hpl, rtpl)) < 1e-12
        steps = round(ks / 0.004)
        assert abs(ks - steps * 0.004) < 1e-12, "KS must be a whole number of 0.004 steps"
        quoted(f"{name}: Spearman correlation", rs, rs_q, 3)
        quoted(f"{name}: KS statistic", ks, ks_q, 3)
        quoted(f"{name}: KS in 0.004 steps", steps, round(ks_q / 0.004), 0)
        assert zone(rs, ks) == z_q, f"{name}: zone {zone(rs, ks)}"
        print(f"    {name}: zone = {z_q}")


# ============================================================================
# 3. Bank-level capital walk (MAR33.41 to MAR33.45)
# ============================================================================


def c_a(imcc_last: float, imcc_avg: float, ses_last: float, ses_avg: float, m_c: float) -> float:
    return max(imcc_last + ses_last, m_c * imcc_avg + ses_avg)


def acr(ima_ga: float, sa_ga: float, sa_all: float, c_u: float, sa_by_desk: dict[str, float], amber: set[str]) -> tuple:
    k = 0.5 * sum(sa_by_desk[d] for d in amber) / sum(sa_by_desk.values())
    surcharge = k * max(0.0, sa_ga - ima_ga)
    total = min(ima_ga + surcharge + c_u, sa_all) + max(0.0, ima_ga - sa_ga)
    return k, surcharge, total


def check_capital_walk() -> None:
    print("  3. Bank capital walk across three quarters (hypothetical, $m)")
    m_c = 1.5  # green bank-wide backtesting zone (MAR32.9)
    sa_desk = {"rates": 120.0, "fx": 45.0, "credit": 35.0}  # standalone SA of each IMA desk
    # quarter 1: all three desks green
    ca1 = c_a(40.0, 38.0, 8.0, 7.5, m_c)
    quoted("Q1 latest IMCC plus latest SES", 40.0 + 8.0, 48.0, 1)
    ima1 = ca1 + max(12.0, 11.0)  # DRC: max of latest and 12-week average (MAR33.22)
    quoted("Q1 C_A", ca1, 64.5, 1)
    quoted("Q1 IMA_G,A", ima1, 76.5, 1)
    k1, s1, acr1 = acr(ima1, 190.0, 235.0, 50.0, sa_desk, set())
    quoted("Q1 ACR_total", acr1, 126.5, 1)
    quoted("Q1 market risk RWA", 12.5 * acr1, 1_581.25, 2)
    # quarter 2: FX options desk moves to the PLA amber zone; models unchanged
    k2, s2, acr2 = acr(ima1, 190.0, 235.0, 50.0, sa_desk, {"fx"})
    quoted("Q2 surcharge factor k", k2, 0.1125, 4)
    quoted("Q2 capital surcharge", s2, 12.77, 2)
    quoted("Q2 ACR_total", acr2, 139.27, 2)
    # quarter 3: credit desk goes red and joins C_U; IMA and SA re-run on the remaining desks
    sa_desk3 = {"rates": 120.0, "fx": 45.0}
    ca3 = c_a(34.0, 33.0, 6.0, 5.5, m_c)
    quoted("Q3 latest IMCC plus latest SES", 34.0 + 6.0, 40.0, 1)
    ima3 = ca3 + max(6.0, 5.0)
    quoted("Q3 C_A", ca3, 55.0, 1)
    quoted("Q3 IMA_G,A", ima3, 61.0, 1)
    k3, s3, acr3 = acr(ima3, 160.0, 235.0, 82.0, sa_desk3, {"fx"})
    quoted("Q3 surcharge factor k", k3, 0.1364, 4)
    quoted("Q3 capital surcharge", s3, 13.50, 2)
    quoted("Q3 ACR_total", acr3, 156.50, 2)
    quoted("Q3 change against Q1", acr3 - acr1, 30.00, 2)
    # the SA cap: had IMA plus surcharge plus C_U exceeded SA for all desks, the first term would stop at 235
    _, s_cap, capped = acr(155.0, 160.0, 235.0, 82.0, sa_desk3, {"fx"})
    quoted("first term before the cap when IMA_G,A is 155", 155.0 + s_cap + 82.0, 237.68, 2)
    quoted("ACR when IMA_G,A is 155 (capped at SA_all)", capped, 235.0, 1)
    _, _, above = acr(170.0, 160.0, 235.0, 82.0, sa_desk3, {"fx"})
    quoted("ACR when IMA_G,A is 170, above SA_G,A", above, 245.0, 1)


def main() -> None:
    print("FRTB engine checks")
    check_sizing()
    check_pla()
    check_capital_walk()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All FRTB engine checks passed.")


if __name__ == "__main__":
    main()
