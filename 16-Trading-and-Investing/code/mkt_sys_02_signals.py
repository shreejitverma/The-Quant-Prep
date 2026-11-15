"""Cross-sectional and time-series signals: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/60-Systems/02-Cross-Sectional-and-Time-Series-Signals.md`.
Independent routes used here:
- Pearson IC with numpy's correlation matrix and again from explicit sums;
- Spearman rank IC as the Pearson correlation of ranks and again from the 1 - 6 sum d^2 / (n(n^2-1)) formula;
- the MAD consistency constant by bisection for the normal quartile, then checked by seeded simulation;
- the fundamental law by seeded simulation of a signal with known IC across 500 assets and 12 periods a year;
- effective breadth from the variance of an equal-weighted basket built from the full correlation matrix.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_sys_02_signals.py`.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261114


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (expected {expected:.4f}, tolerance {tol:.3g})")


def ic_example() -> None:
    print("Example 1: IC, rank IC and ICIR (cards mkt-sys-036, mkt-sys-037, mkt-sys-038)")
    s = np.array([1.40, 0.90, 0.50, 0.10, -0.20, -0.60, -0.90, -1.20])
    r = np.array([2.1, 1.5, 0.4, 0.8, -0.3, -0.7, -1.8, -1.2]) / 100
    pearson = float(np.corrcoef(s, r)[0, 1])
    sc, rc = s - s.mean(), r - r.mean()
    manual = float((sc @ rc) / math.sqrt((sc @ sc) * (rc @ rc)))
    assert abs(pearson - manual) < 1e-12
    approx("Pearson IC", pearson, 0.957, 3)
    rank_s = np.argsort(np.argsort(s)) + 1
    rank_r = np.argsort(np.argsort(r)) + 1
    assert list(rank_s) == [8, 7, 6, 5, 4, 3, 2, 1] and list(rank_r) == [8, 7, 5, 6, 4, 3, 1, 2]
    d2 = int(np.sum((rank_s - rank_r) ** 2))
    assert d2 == 4
    spearman_formula = 1 - 6 * d2 / (8 * (64 - 1))
    approx("Spearman rank IC, 1 - 6 sum d^2 / (n(n^2-1))", spearman_formula, 0.952, 3)
    approx("Spearman rank IC, Pearson of ranks", float(np.corrcoef(rank_s, rank_r)[0, 1]), 0.952, 3)
    icir = 0.045 / 0.110
    approx("daily ICIR", icir, 0.409, 3)
    approx("annualized ICIR", icir * math.sqrt(252), 6.49, 2)


def mad_constant(rng: np.random.Generator) -> None:
    print("MAD consistency constant (Core concepts 2, card mkt-sys-040)")
    lo, hi = 0.0, 2.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if 0.5 * math.erfc(-mid / math.sqrt(2)) < 0.75:
            lo = mid
        else:
            hi = mid
    q75 = 0.5 * (lo + hi)
    approx("Phi^-1(0.75)", q75, 0.6745, 4)
    approx("1 / Phi^-1(0.75)", 1 / q75, 1.4826, 4)
    x = rng.standard_normal(1_000_001) * 2.0
    mad = float(np.median(np.abs(x - np.median(x))))
    simulated("1.4826 x MAD of N(0, 2^2) draws, divided by 2", 1.4826 * mad / 2.0, 1.0, 0.005)


def fundamental_law(rng: np.random.Generator) -> None:
    print("Example 2 and the fundamental law (cards mkt-sys-034, mkt-sys-035, mkt-sys-064)")
    approx("sqrt(6000)", math.sqrt(6000), 77.46, 2)
    ir = 0.03 * math.sqrt(6000)
    approx("unconstrained IR", ir, 2.32, 2)
    ir_c = 0.42 * ir
    approx("constrained IR", ir_c, 0.98, 2)
    approx("reduction (percent)", 100 * (1 - ir_c / ir), 58, 0)
    # Simulation: standardized residual returns r = IC s + sqrt(1 - IC^2) e, weights proportional to s.
    n_assets, ic, years = 500, 0.03, 2500
    periods = 12 * years
    pnl = np.empty(periods)
    for t in range(periods):
        sig = rng.standard_normal(n_assets)
        ret = ic * sig + math.sqrt(1 - ic * ic) * rng.standard_normal(n_assets)
        pnl[t] = sig @ ret
    ir_sim = pnl.mean() / pnl.std(ddof=1) * math.sqrt(12)
    exact_model = ic * math.sqrt(12 * n_assets) / math.sqrt(1 + ic * ic)
    approx("model IR, IC sqrt(BR) / sqrt(1 + IC^2)", exact_model, 2.32, 2)
    se = math.sqrt((1 + 0.5 * (ir_sim / math.sqrt(12)) ** 2) / periods) * math.sqrt(12)
    simulated(f"simulated IR, 500 assets x 12 periods x {years} years (seed {SEED})", float(ir_sim), exact_model, 4 * se)


def breadth() -> None:
    print("Effective breadth with correlated bets (card mkt-sys-050)")
    n, rho = 500, 0.5
    corr = np.full((n, n), rho)
    np.fill_diagonal(corr, 1.0)
    var_basket = float(np.ones(n) @ corr @ np.ones(n)) / n**2
    approx("effective N = 1 / Var(equal-weighted basket of unit-variance names)", 1 / var_basket, 2.0, 2)
    approx("N / (1 + (N - 1) rho)", n / (1 + (n - 1) * rho), 1.996, 3)


def half_life() -> None:
    print("Half-life (card mkt-sys-042)")
    lam = math.log(2) / 5
    approx("decay rate for a 5-day half-life", lam, 0.1386, 4)
    approx("autocorrelation after one half-life", math.exp(-lam * 5), 0.5, 12)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    ic_example()
    mad_constant(rng)
    fundamental_law(rng)
    breadth()
    half_life()
    print("all signal numbers check out")
