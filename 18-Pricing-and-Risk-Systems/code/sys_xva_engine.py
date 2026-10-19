"""XVA engine: storage tiers, CVA quadrature, FVA, MVA, KVA and incremental CVA from stored netting-set paths.

Backs every number in `18-Pricing-and-Risk-Systems/11-XVA-Engine.md`.
Portfolio sizes, exposure, margin and capital profiles, spreads and hurdle rates are labelled-hypothetical inputs.
Sign conventions follow `11-Risk-and-Trading/15-XVA.md`: V = V_rf - CVA + DVA - FVA - MVA - KVA, FVA = FCA - FBA,
each adjustment a positive number when it is a cost.
Checks that are not arithmetic on literals: the bucketed CVA is compared with the exact integral of a piecewise-constant
exposure against the default density; the simulated exposure of a Brownian netting set is compared with its closed
form within three standard errors.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_xva_engine.py`.
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


def quoted_about(label: str, value: float, expected: float, step: float) -> float:
    """A seeded simulation result: assert it is within half a step of the quoted rounded value."""
    assert abs(value - expected) <= 0.5 * step + 1e-9, f"{label}: computed {value!r}, quoted about {expected}"
    QUOTED.append(label)
    print(f"    {label} = about {round(value / step) * step:,.0f}")
    return value


def n_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def n_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ============================================================================
# 1. Storage tiers (hypothetical dealer)
# ============================================================================


def check_storage() -> None:
    print("  1. Storage tiers for 120,000 trades, 4,500 netting sets, 10,000 paths, 80 dates")
    trades, sets, paths, dates = 120_000, 4_500, 10_000, 80
    points = paths * dates
    quoted("path-date points per trade", points, 800_000, 0)
    quoted("trade-level values, float64 (GB)", trades * points * 8 / 1e9, 768.0, 1)
    quoted("netting-set path cube, float64 (GB)", sets * points * 8 / 1e9, 28.8, 1)
    quoted("netting-set path cube, float32 (GB)", sets * points * 4 / 1e9, 14.4, 1)
    quoted("one netting set's paths in memory (MB)", points * 8 / 1e6, 6.4, 1)
    quoted("EE and ENE profiles for all netting sets (MB)", sets * dates * 2 * 8 / 1e6, 5.76, 2)
    quoted("average trades per netting set", trades / sets, 26.67, 2)


# ============================================================================
# 2. CVA, FVA, MVA, KVA on annual buckets
# ============================================================================

R = 0.04
YEARS = (1, 2, 3)
EE = (1_200_000.0, 1_800_000.0, 950_000.0)  # expected positive exposure at each year end, hypothetical
ENE = (400_000.0, 600_000.0, 300_000.0)  # expected negative exposure (as a positive amount), hypothetical


def df(t: float) -> float:
    return math.exp(-R * t)


def check_cva() -> None:
    print("  2. Unilateral CVA, uncollateralised 3-year swap (hypothetical)")
    lgd, spread = 0.60, 0.0150
    lam = spread / lgd  # credit triangle: an approximation for a flat curve
    quoted("hazard rate from the credit triangle (%)", lam * 100, 2.50, 2)
    bucket = []
    for t, ee in zip(YEARS, EE, strict=True):
        dpd = math.exp(-lam * (t - 1)) - math.exp(-lam * t)
        quoted(f"year {t} discount factor", df(t), {1: 0.9608, 2: 0.9231, 3: 0.8869}[t], 4)
        quoted(f"year {t} default probability in the year", dpd, {1: 0.02469, 2: 0.02408, 3: 0.02349}[t], 5)
        bucket.append(lgd * df(t) * ee * dpd)
    for t, q in zip(YEARS, (17_079.82, 24_007.42, 11_873.19), strict=True):
        quoted(f"year {t} CVA contribution ($)", bucket[t - 1], q, 2)
    cva = quoted("CVA, exposure and discount at year end ($)", sum(bucket), 52_960.43, 2)
    # exact integral of a piecewise-constant EE against D(t) * lambda * exp(-lambda t) on each year
    exact = 0.0
    for t, ee in zip(YEARS, EE, strict=True):
        a = R + lam
        exact += lgd * ee * lam / a * (math.exp(-a * (t - 1)) - math.exp(-a * t))
    numeric = 0.0
    n = 30_000
    for i in range(n):
        u = 3.0 * (i + 0.5) / n
        ee = EE[min(int(u), 2)]
        numeric += lgd * ee * df(u) * lam * math.exp(-lam * u) * 3.0 / n
    assert abs(exact - numeric) < 0.01
    quoted("CVA, exact integral with exposure constant within each year ($)", exact, 54_038.41, 2)
    quoted("bucketing effect, exact minus year-end convention ($)", exact - cva, 1_077.98, 2)
    quoted("bucketing effect relative to the year-end figure (%)", (exact / cva - 1) * 100, 2.0, 1)


def check_fva_mva_kva() -> None:
    print("  3. FVA, MVA and KVA on the same annual grid (hypothetical)")
    sb = sl = 0.0080
    fca = sum(sb * df(t) * ee for t, ee in zip(YEARS, EE, strict=True))
    fba = sum(sl * df(t) * ene for t, ene in zip(YEARS, ENE, strict=True))
    quoted("FCA at 80 bp ($)", fca, 29_257.05, 2)
    quoted("FBA at 80 bp ($)", fba, 9_634.09, 2)
    quoted("FVA, symmetric funding ($)", fca - fba, 19_622.96, 2)
    quoted("FVA when excess cash earns no spread ($)", fca, 29_257.05, 2)
    im = (5_000_000.0, 4_200_000.0, 3_100_000.0, 1_800_000.0, 600_000.0)
    s_im = 0.0075
    mva = sum(s_im * df(t) * x for t, x in zip(range(1, 6), im, strict=True))
    quoted("MVA, 75 bp on the expected IM profile ($)", mva, 100_916.90, 2)
    capital = (600_000.0, 450_000.0, 200_000.0)
    hurdle = 0.10
    kva = sum(hurdle * df(t) * k for t, k in zip(YEARS, capital, strict=True))
    quoted("KVA at a 10% hurdle ($)", kva, 116_926.01, 2)


# ============================================================================
# 3. Incremental CVA from stored netting-set paths
# ============================================================================


def ee_closed_form(mean: float, sd: float) -> float:
    if sd == 0.0:
        return max(mean, 0.0)
    z = mean / sd
    return mean * n_cdf(z) + sd * n_pdf(z)


def check_incremental() -> None:
    print("  4. Incremental CVA of a new trade against stored netting-set paths (20,000 paths, seed 2026)")
    rng = random.Random(2026)
    n_paths, steps = 20_000, (1.0, 2.0, 3.0)
    a, s1 = 500_000.0, 1_000_000.0  # existing netting set: value a + s1 W1(t)
    s2, rho = 800_000.0, -0.8  # new trade: value s2 (rho W1 + sqrt(1 - rho^2) W2)(t)
    lgd, lam = 0.60, 0.025
    ee_old = [0.0] * 3
    ee_new_alone = [0.0] * 3
    ee_combined = [0.0] * 3
    sq_old = [0.0] * 3
    for _ in range(n_paths):
        w1 = w2 = 0.0
        prev = 0.0
        for k, t in enumerate(steps):
            dt = t - prev
            prev = t
            w1 += math.sqrt(dt) * rng.gauss(0.0, 1.0)
            w2 += math.sqrt(dt) * rng.gauss(0.0, 1.0)
            old = a + s1 * w1
            new = s2 * (rho * w1 + math.sqrt(1 - rho * rho) * w2)
            ee_old[k] += max(old, 0.0)
            sq_old[k] += max(old, 0.0) ** 2
            ee_new_alone[k] += max(new, 0.0)
            ee_combined[k] += max(old + new, 0.0)
    ee_old = [x / n_paths for x in ee_old]
    ee_new_alone = [x / n_paths for x in ee_new_alone]
    ee_combined = [x / n_paths for x in ee_combined]
    for k, t in enumerate(steps):
        se = math.sqrt(sq_old[k] / n_paths - ee_old[k] ** 2) / math.sqrt(n_paths)
        exact = ee_closed_form(a, s1 * math.sqrt(t))
        assert abs(ee_old[k] - exact) < 3 * se, "simulated EE outside 3 standard errors of the closed form"

    def cva(profile: list[float]) -> float:
        return sum(lgd * df(t) * e * (math.exp(-lam * (t - 1)) - math.exp(-lam * t)) for t, e in zip((1, 2, 3), profile, strict=True))

    base, alone, combined = cva(ee_old), cva(ee_new_alone), cva(ee_combined)
    quoted_about("CVA of the existing netting set ($)", base, 33_140, 10)
    quoted_about("standalone CVA of the new trade ($)", alone, 17_440, 10)
    quoted_about("CVA of the netting set with the new trade ($)", combined, 25_700, 10)
    quoted_about("incremental CVA of the new trade ($)", combined - base, -7_440, 10)


def main() -> None:
    print("XVA engine checks")
    check_storage()
    check_cva()
    check_fva_mva_kva()
    check_incremental()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All XVA engine checks passed.")


if __name__ == "__main__":
    main()
