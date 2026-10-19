"""Curve risk: zero versus par DV01, key-rate durations, curve trades, PCA and PCA-neutral butterflies.

Backs every number in `06-Fixed-Income-and-Asset-Classes/15-Curve-Risk-and-Hedging.md`.
Independent checks: par DV01s come from bumping each par quote and re-bootstrapping (not from the
Jacobian of note 14, which they confirm); key-rate durations are checked to sum to the parallel
duration computed by a separate parallel bump; the bond's yield DV01 is checked against a finite
difference of its price-yield function; PCA eigenpairs from numpy are checked against the roots of the
characteristic polynomial and against the definition C v = lambda v.
The covariance matrix in the PCA example is a labelled hypothetical input, not market data.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_curve_risk.py`.
"""

from __future__ import annotations

import math

import numpy as np

QUOTED: list[str] = []
CURVE_10Y = [0.030, 0.035, 0.0375, 0.039, 0.040, 0.041, 0.042, 0.043, 0.044, 0.045]


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def bootstrap(par: list[float]) -> list[float]:
    dfs: list[float] = []
    for s in par:
        dfs.append((1.0 - s * sum(dfs)) / (1.0 + s))
    return dfs


def pv_from_zeros(cfs: list[float], zeros: list[float]) -> float:
    return sum(cf * math.exp(-(k + 1) * z) for k, (cf, z) in enumerate(zip(cfs, zeros, strict=True)))


def example_zero_vs_par() -> None:
    print("  1. Zero DV01 versus par DV01, 3y 4% par bond")
    par = [0.030, 0.035, 0.040]
    p = bootstrap(par)
    z = [-math.log(pp) / (k + 1) for k, pp in enumerate(p)]
    for k, e in enumerate((2.9559, 3.4486, 3.9482)):
        quoted(f"z{k + 1} (%)", z[k] * 100, e, 4)
    cfs = [4.0, 4.0, 104.0]
    h = 1e-6
    zero_dv01 = []
    for k in range(3):
        up, dn = list(z), list(z)
        up[k] += h
        dn[k] -= h
        zero_dv01.append(-(pv_from_zeros(cfs, up) - pv_from_zeros(cfs, dn)) / (2 * h) * 1e-4)
    for k, e in enumerate((0.000388, 0.000747, 0.027715)):
        quoted(f"zero DV01 {k + 1}y per 100", zero_dv01[k], e, 6)
    quoted("sum of zero DV01s", sum(zero_dv01), 0.028850, 6)

    def bond_pv(pr: list[float]) -> float:
        return sum(cf * d for cf, d in zip(cfs, bootstrap(pr), strict=True))

    par_dv01 = []
    for k in range(3):
        up, dn = list(par), list(par)
        up[k] += h
        dn[k] -= h
        par_dv01.append(-(bond_pv(up) - bond_pv(dn)) / (2 * h) * 1e-4)
    for k, e in enumerate((0.0, 0.0, 0.027925)):
        quoted(f"par DV01 {k + 1}y per 100", par_dv01[k], e, 6)
    a3 = sum(p)
    quoted("100 x A3 x 1e-4", 100 * a3 * 1e-4, 0.027925, 6)

    def price_at_yield(y: float) -> float:
        return sum(cf / (1 + y) ** (k + 1) for k, cf in enumerate(cfs))

    yield_dv01 = -(price_at_yield(0.04 + h) - price_at_yield(0.04 - h)) / (2 * h) * 1e-4
    closed = 100 * (1 - 1.04**-3) / 0.04 * 1e-4
    assert abs(yield_dv01 - closed) < 1e-9  # a par bond's modified duration equals its annuity factor at y
    quoted("bond yield DV01 per 100", yield_dv01, 0.027751, 6)
    hedge = par_dv01[2] / (a3 * 1e-4)
    quoted("3y payer swap notional per 100 face to hedge", hedge, 100.0, 4)


def example_key_rates() -> None:
    print("  2. Key-rate durations on a 10y 4.5% annual bond (keys 2y, 5y, 10y)")
    p = bootstrap(CURVE_10Y)
    z = [-math.log(pp) / (k + 1) for k, pp in enumerate(p)]
    cfs = [4.5] * 9 + [104.5]
    price = pv_from_zeros(cfs, z)
    quoted("bond price", price, 100.0, 4)
    keys = [2.0, 5.0, 10.0]

    def shift(key_idx: int, t: float) -> float:
        k = keys[key_idx]
        left = keys[key_idx - 1] if key_idx > 0 else None
        right = keys[key_idx + 1] if key_idx < len(keys) - 1 else None
        if t <= k:
            if left is None:
                return 1.0
            return max(0.0, (t - left) / (k - left))
        if right is None:
            return 1.0
        return max(0.0, (right - t) / (right - k))

    h = 1e-6
    krd = []
    for i in range(len(keys)):
        up = [zz + h * shift(i, k + 1.0) for k, zz in enumerate(z)]
        dn = [zz - h * shift(i, k + 1.0) for k, zz in enumerate(z)]
        krd.append(-(pv_from_zeros(cfs, up) - pv_from_zeros(cfs, dn)) / (2 * h) / price)
    par_up = [zz + h for zz in z]
    par_dn = [zz - h for zz in z]
    parallel = -(pv_from_zeros(cfs, par_up) - pv_from_zeros(cfs, par_dn)) / (2 * h) / price
    for i, e in enumerate((0.2597, 0.7956, 7.1809)):
        quoted(f"KRD {keys[i]:.0f}y", krd[i], e, 4)
    quoted("sum of KRDs", sum(krd), 8.2362, 4)
    quoted("parallel (zero-rate) duration", parallel, 8.2362, 4)
    assert abs(sum(krd) - parallel) < 1e-8


def example_steepener_and_fly() -> None:
    print("  3. 2s10s steepener and 2s5s10s 50/50 butterfly")
    p = bootstrap(CURVE_10Y)
    a2, a5, a10 = sum(p[:2]), sum(p[:5]), sum(p)
    quoted("A2", a2, 1.9042, 4)
    quoted("A5", a5, 4.4775, 4)
    quoted("A10", a10, 8.0335, 4)
    dv01_2, dv01_10 = a2 * 100, a10 * 100  # USD per bp per 1mm
    quoted("DV01 per 1mm, 2y (USD)", dv01_2, 190.42, 2)
    quoted("DV01 per 1mm, 10y (USD)", dv01_10, 803.35, 2)
    n10, n2 = 10_000 / dv01_10, 10_000 / dv01_2
    quoted("10y payer notional (mm)", n10, 12.448, 3)
    quoted("2y receiver notional (mm)", n2, 52.515, 3)
    quoted("2y receiver notional, 4 decimals (mm)", n2, 52.5148, 4)
    quoted("10y payer notional, 4 decimals (mm)", n10, 12.4478, 4)
    # Full revaluation: 2y quote -5 bp, 10y quote +5 bp, curve rebuilt, both swaps repriced.
    shocked = list(CURVE_10Y)
    shocked[1] -= 0.0005
    shocked[9] += 0.0005
    q = bootstrap(shocked)
    s2_new, s10_new = (1 - q[1]) / sum(q[:2]), (1 - q[9]) / sum(q)
    pnl_2 = n2 * 1e6 * (0.035 - s2_new) * sum(q[:2])
    pnl_10 = n10 * 1e6 * (s10_new - 0.045) * sum(q)
    quoted("revalued P&L, 2y receiver (USD)", pnl_2, 50_024.0, 0)
    quoted("revalued P&L, 10y payer (USD)", pnl_10, 49_980.0, 0)
    quoted("revalued P&L of a 10 bp steepening (USD)", pnl_2 + pnl_10, 100_004.0, 0)

    carry_2 = n2 * 1e6 * (0.035 - 0.030)
    carry_10 = n10 * 1e6 * (0.045 - 0.030)
    quoted("first-year carry, 2y receiver (USD)", carry_2, 262_574.0, 0)
    quoted("first-year carry, 10y payer (USD)", -carry_10, -186_717.0, 0)
    quoted("first-year carry, floating legs at 3.00% (USD)", carry_2 - carry_10, 75_857.0, 0)
    quoted("receiver carry per unit DV01, 2y (%)", (0.035 - 0.030) / a2 * 100, 0.26, 2)
    quoted("receiver carry per unit DV01, 10y (%)", (0.045 - 0.030) / a10 * 100, 0.19, 2)
    belly = 100_000_000 * a5 * 1e-4
    quoted("belly DV01, 100mm 5y (USD)", belly, 44_775.43, 2)
    quoted("each wing's DV01, 50/50 (USD)", belly / 2, 22_387.71, 2)
    n2w, n10w = belly / 2 / (a2 * 1e-4) / 1e6, belly / 2 / (a10 * 1e-4) / 1e6

    quoted("2y wing notional (mm)", n2w, 117.569, 3)

    quoted("10y wing notional (mm)", n10w, 27.868, 3)


def example_pca() -> None:
    print("  4. PCA of 2y, 5y, 10y daily yield changes (hypothetical covariance, bp^2)")
    vol = np.array([6.0, 7.0, 6.5])
    corr = np.array([[1.0, 0.90, 0.75], [0.90, 1.0, 0.93], [0.75, 0.93, 1.0]])
    cov = corr * np.outer(vol, vol)
    eigval, eigvec = np.linalg.eigh(cov)
    order = np.argsort(eigval)[::-1]
    eigval, eigvec = eigval[order], eigvec[:, order]
    # Sign conventions: level all positive, slope 10y above 2y (steepening positive), curvature belly negative.
    if eigvec[:, 0].sum() < 0:
        eigvec[:, 0] *= -1.0
    if eigvec[2, 1] - eigvec[0, 1] < 0:
        eigvec[:, 1] *= -1.0
    if eigvec[1, 2] > 0:
        eigvec[:, 2] *= -1.0
    # Independent checks: characteristic polynomial roots and C v = lambda v.
    roots = np.sort(np.roots(np.poly(cov)).real)[::-1]
    assert np.allclose(roots, eigval, atol=1e-9)
    for k in range(3):
        assert np.allclose(cov @ eigvec[:, k], eigval[k] * eigvec[:, k], atol=1e-9)
    share = eigval / eigval.sum()
    for k, e in enumerate((91.43, 7.63, 0.94)):
        quoted(f"variance share PC{k + 1} (%)", share[k] * 100, e, 2)
    for name, k, exp in (
        ("PC1", 0, (0.5104, 0.6443, 0.5695)),
        ("PC2", 1, (-0.7509, 0.0113, 0.6603)),
        ("PC3", 2, (0.4190, -0.7647, 0.4896)),
    ):
        for j, tenor in enumerate(("2y", "5y", "10y")):
            quoted(f"{name} loading {tenor}", eigvec[j, k], exp[j], 4)
    # Position DV01 vector d (USD per bp, receiver positive); P&L = -d . dy, so exposure to PC k is d . e_k.
    fifty = np.array([0.5, -1.0, 0.5])
    exposures_5050 = eigvec.T @ fifty
    for k, e in enumerate((-0.1044, -0.0566, 1.2190)):
        quoted(f"50/50 fly exposure to PC{k + 1}", exposures_5050[k], e, 4)
    a = np.array([[eigvec[0, 0], eigvec[2, 0]], [eigvec[0, 1], eigvec[2, 1]]])
    b = np.array([eigvec[1, 0], eigvec[1, 1]])
    w2, w10 = np.linalg.solve(a, b)
    pca_fly = np.array([w2, -1.0, w10])
    exposures_pca = eigvec.T @ pca_fly
    quoted("PCA fly 2y DV01 per unit belly DV01", w2, 0.5479, 4)
    quoted("PCA fly 10y DV01 per unit belly DV01", w10, 0.6403, 4)
    quoted("PCA fly exposure to PC1", exposures_pca[0], 0.0, 4)
    quoted("PCA fly exposure to PC2", exposures_pca[1], 0.0, 4)
    quoted("PCA fly exposure to PC3", exposures_pca[2], 1.3077, 4)
    quoted("PCA fly net DV01 per unit belly DV01", float(pca_fly.sum()), 0.1882, 4)
    sd_5050 = math.sqrt(fifty @ cov @ fifty)
    sd_pca = math.sqrt(pca_fly @ cov @ pca_fly)
    quoted("daily P&L sd, 50/50 fly, per 1 USD of belly DV01 (USD)", sd_5050, 1.7529, 4)
    quoted("daily P&L sd, PCA fly, per 1 USD of belly DV01 (USD)", sd_pca, 1.4290, 4)
    quoted("PCA fly sd explained by PC3 alone (USD)", abs(exposures_pca[2]) * math.sqrt(eigval[2]), 1.4290, 4)


def main() -> None:
    print("=== fi_curve_risk: zero vs par risk, KRD, curve trades, PCA ===")
    example_zero_vs_par()
    example_key_rates()
    example_steepener_and_fly()
    example_pca()
    print(f"\nVerified {len(QUOTED)} curve risk figures.")


if __name__ == "__main__":
    main()
