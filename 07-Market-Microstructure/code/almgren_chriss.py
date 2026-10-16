"""Almgren-Chriss (2000) optimal liquidation: sinh trajectory, efficient frontier, TWAP and VWAP as special cases.

Backs every number in 07-Optimal-Execution-Almgren-Chriss.md.
Run ``python almgren_chriss.py``: each result is printed and asserted.
Units: shares, dollars, days.  Parameters are illustrative, not calibrated to any stock.
"""

from __future__ import annotations

import math

import numpy as np

X = 1_000_000.0  # shares to sell
T = 5.0  # days
N = 10  # trading intervals
TAU = T / N  # interval length (days)
SIGMA = 0.95  # $ per share per sqrt(day): about 30% annual on a $50 stock
EPS = 0.0625  # fixed temporary cost, $ per share (half-spread plus fees)
ETA = 2.5e-6  # linear temporary impact, $ per share per (share/day)
GAMMA = 2.5e-7  # linear permanent impact, $ per share per share
ETA_TILDE = ETA - 0.5 * GAMMA * TAU


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a labelled result and assert it is within tol of the expected value."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


def kappa(lam: float) -> float:
    """Discrete-time urgency: (2/tau^2)(cosh(kappa tau) - 1) = lam sigma^2 / eta_tilde."""
    k2 = lam * SIGMA**2 / ETA_TILDE
    return math.acosh(1 + 0.5 * k2 * TAU**2) / TAU


def trajectory(lam: float) -> np.ndarray:
    """Holdings x_0..x_N on the grid t_k = k tau: X sinh(kappa (T - t_k)) / sinh(kappa T), linear when lam = 0."""
    t = np.arange(N + 1) * TAU
    if lam == 0.0:
        return X * (1 - t / T)
    k = kappa(lam)
    return X * np.sinh(k * (T - t)) / math.sinh(k * T)


def cost_moments(x: np.ndarray) -> tuple[float, float]:
    """Expected implementation shortfall and its variance for holdings x_0 = X, ..., x_N = 0."""
    n = -np.diff(x)  # shares sold in each interval
    expected = 0.5 * GAMMA * X**2 + EPS * np.abs(n).sum() + ETA_TILDE / TAU * float(np.sum(n**2))
    variance = SIGMA**2 * TAU * float(np.sum(x[1:] ** 2))
    return float(expected), variance


def brute_force(lam: float) -> np.ndarray:
    """Minimise E + lam V directly: the first-order conditions are a tridiagonal linear system."""
    m = N - 1
    a = np.zeros((m, m))
    b = np.zeros(m)
    c = ETA_TILDE / TAU
    for i in range(m):
        a[i, i] = 2 * c + lam * SIGMA**2 * TAU
        if i > 0:
            a[i, i - 1] = -c
        if i < m - 1:
            a[i, i + 1] = -c
    b[0] = c * X
    inner = np.linalg.solve(a, b)
    return np.concatenate([[X], inner, [0.0]])


def main() -> None:
    check("eta tilde", ETA_TILDE, 2.4375e-6, 1e-15)
    check("annualised vol on $50 (sigma*sqrt(250)/50)", SIGMA * math.sqrt(250) / 50, 0.3004, 5e-5)

    print("== Trajectories (holdings in thousands of shares) ==")
    lams = (0.0, 1e-7, 1e-6, 1e-5)
    expected_holdings = {
        0.0: (1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 0),
        1e-7: (1000, 875, 759, 649, 546, 447, 353, 262, 173, 86, 0),
        1e-6: (1000, 737, 542, 398, 290, 210, 148, 101, 62, 30, 0),
        1e-5: (1000, 395, 156, 62, 24, 10, 4, 1, 1, 0, 0),
    }
    summary = {}
    for lam in lams:
        x = trajectory(lam)
        if lam > 0:
            assert np.allclose(x, brute_force(lam), rtol=0, atol=1e-3), "sinh solution must solve the FOC system"
        rounded = tuple(int(round(v / 1000)) for v in x)
        print(f"lambda = {lam:g}: {rounded}")
        assert rounded == expected_holdings[lam], rounded
        e, v = cost_moments(x)
        summary[lam] = (e, math.sqrt(v))
    expected_summary = {
        0.0: (675_000.0, 1_134_047.0),
        1e-7: (682_733.0, 1_060_448.0),
        1e-6: (945_216.0, 723_822.0),
        1e-5: (2_300_817.0, 288_990.0),
    }
    for lam in lams:
        e, sd = summary[lam]
        kap = 0.0 if lam == 0 else kappa(lam)
        check(f"lambda={lam:g} kappa (1/day)", kap, {0.0: 0.0, 1e-7: 0.1923, 1e-6: 0.6062, 1e-5: 1.8568}[lam], 5e-5)
        check(f"lambda={lam:g} expected cost ($)", e, expected_summary[lam][0], 0.5)
        check(f"lambda={lam:g} std of cost ($)", sd, expected_summary[lam][1], 0.5)

    check("cost increase TWAP -> lambda=1e-7 ($)", summary[1e-7][0] - summary[0.0][0], 7_733.0, 0.5)
    check("std decrease TWAP -> lambda=1e-7 ($)", summary[0.0][1] - summary[1e-7][1], 73_599.0, 0.5)
    # Closed-form trade list n_k = 2 sinh(kappa tau / 2) / sinh(kappa T) * cosh(kappa (T - t_{k-1/2})) X
    k6 = kappa(1e-6)
    mid_times = (np.arange(1, N + 1) - 0.5) * TAU
    n_formula = 2 * math.sinh(k6 * TAU / 2) / math.sinh(k6 * T) * np.cosh(k6 * (T - mid_times)) * X
    assert np.allclose(n_formula, -np.diff(trajectory(1e-6)), rtol=0, atol=1e-6), "closed-form trade list"
    print("closed-form trade list matches the trajectory differences")
    print("== Limits ==")
    e_twap, sd_twap = summary[0.0]
    check("TWAP expected cost = gamma X^2/2 + eps X + eta_tilde X^2 / T", 0.5 * GAMMA * X**2 + EPS * X + ETA_TILDE * X**2 / T, e_twap, 1e-6)
    check("permanent impact term gamma X^2/2", 0.5 * GAMMA * X**2, 125_000.0, 1e-6)
    check("fixed cost term eps X", EPS * X, 62_500.0, 1e-6)
    check("TWAP temporary term eta_tilde X^2 / T", ETA_TILDE * X**2 / T, 487_500.0, 1e-6)
    x_now = np.concatenate([[X], np.zeros(N)])
    e_now, v_now = cost_moments(x_now)
    check("sell everything in the first interval: expected cost", e_now, 5_062_500.0, 1e-6)
    check("sell everything in the first interval: variance", v_now, 0.0, 1e-9)
    check("continuous kappa for lambda=1e-6: sqrt(lam sigma^2/eta)", math.sqrt(1e-6 * SIGMA**2 / ETA), 0.6008, 5e-5)
    check("characteristic time 1/kappa (days) for lambda=1e-6", 1 / kappa(1e-6), 1.6497, 5e-5)

    print("== Efficient frontier and a VaR-style choice ==")
    grid = np.logspace(-9, -4, 501)
    best = min(grid, key=lambda lam: cost_moments(trajectory(lam))[0] + 1.645 * math.sqrt(cost_moments(trajectory(lam))[1]))
    e_b, v_b = cost_moments(trajectory(best))
    check("lambda minimising E + 1.645 sd", float(best), 1.2023e-6, 5e-11)
    check("its expected cost ($)", e_b, 1_005_856.0, 0.5)
    check("its std ($)", math.sqrt(v_b), 684_581.0, 0.5)
    check("its E + 1.645 sd ($)", e_b + 1.645 * math.sqrt(v_b), 2_131_992.0, 0.5)
    check("TWAP E + 1.645 sd ($)", e_twap + 1.645 * sd_twap, 2_540_507.0, 0.5)
    check("extra expected cost vs TWAP ($)", e_b - e_twap, 330_856.0, 0.5)
    check("reduction in E + 1.645 sd vs TWAP ($)", e_twap + 1.645 * sd_twap - (e_b + 1.645 * math.sqrt(v_b)), 408_515.0, 0.5)
    # Frontier slope: near TWAP, dE/dsd is zero (first-order risk reduction is free)
    e1, v1 = cost_moments(trajectory(1e-9))
    check("cost increase from TWAP at lambda=1e-9 ($)", e1 - e_twap, 0.915, 0.0005)
    check("std decrease from TWAP at lambda=1e-9 ($)", sd_twap - math.sqrt(v1), 807.5, 0.05)

    print("== VWAP as the risk-neutral optimum with volume-scaled impact ==")
    volume = np.array([16.0, 11.0, 8.0, 7.0, 6.0, 6.0, 7.0, 9.0, 12.0, 18.0])  # % of day per bucket
    weights = volume / volume.sum()
    # Minimise sum c n_k^2 / v_k subject to sum n_k = X: Lagrange gives n_k proportional to v_k
    a = np.diag(2.0 / volume)
    kkt = np.block([[a, np.ones((10, 1))], [np.ones((1, 10)), np.zeros((1, 1))]])
    rhs = np.concatenate([np.zeros(10), [X]])
    n_opt = np.linalg.solve(kkt, rhs)[:10]
    assert np.allclose(n_opt, X * weights), "optimal child sizes must be proportional to volume"
    check("first-bucket child order (shares)", float(n_opt[0]), 160_000.0, 1e-3)
    check("midday bucket child order (shares)", float(n_opt[4]), 60_000.0, 1e-3)
    check(
        "cost ratio TWAP vs VWAP schedule under volume-scaled impact",
        float(np.sum((X / 10) ** 2 / volume) / np.sum(n_opt**2 / volume)),
        1.1475,
        5e-5,
    )


if __name__ == "__main__":
    main()
    print("all Almgren-Chriss checks passed")
