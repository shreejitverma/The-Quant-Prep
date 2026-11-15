"""Mean-variance portfolio construction: every weight, Sharpe, bias and no-trade-band number in the note.

Backs every number in `09-Alpha-Research-and-Portfolio/10-Mean-Variance-Portfolio-Construction.md`.
Independent routes used here:
- minimum-variance, tangency and utility-optimal weights by brute-force search over a fine weight grid,
  against the closed forms Sigma^-1 1 / A and Sigma^-1 mu / B;
- the frontier sigma^2(m) = (A m^2 - 2 B m + C) / D against a direct solve of the KKT linear system;
- the long-only tangency portfolio by grid search on [0, 1];
- the in-sample squared Sharpe bias (N/T, and the (T-1)/(T-N-2) factor for an estimated covariance)
  by seeded simulation, with a tolerance of four standard errors;
- the Jagannathan-Ma equivalence by checking that the long-only minimum-variance portfolio is the
  unconstrained one for a covariance matrix shrunk by the constraint multipliers;
- the no-trade band by maximising the cost-adjusted utility on a grid from each starting weight.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 09-Alpha-Research-and-Portfolio/code/alpha_10_mean_variance.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


GRID = np.linspace(-3.0, 3.0, 6_000_001)  # w1 on a 1e-6 grid, w2 = 1 - w1


def two_asset(s1: float, s2: float, rho: float) -> np.ndarray:
    return np.array([[s1 * s1, rho * s1 * s2], [rho * s1 * s2, s2 * s2]])


def grid_var(cov: np.ndarray, w1: np.ndarray) -> np.ndarray:
    w2 = 1 - w1
    return cov[0, 0] * w1 * w1 + 2 * cov[0, 1] * w1 * w2 + cov[1, 1] * w2 * w2


def gmv_two_asset() -> None:
    print("Two-asset minimum variance (worked example 1, card alpha-mv-two-asset-gmv)")
    cov = two_asset(0.2, 0.3, 0.2)
    approx("sigma_12", cov[0, 1], 0.012, 12)
    exact(
        "w1 numerator and denominator",
        (Fraction(9, 100) - Fraction(12, 1000), Fraction(4, 100) + Fraction(9, 100) - Fraction(24, 1000)),
        (Fraction(78, 1000), Fraction(106, 1000)),
    )
    var = grid_var(cov, GRID)
    w1 = float(GRID[np.argmin(var)])
    approx("w1 by grid search", w1, 0.736, 3)
    approx("w2 by grid search", 1 - w1, 0.264, 3)
    approx("minimum volatility by grid search (%)", math.sqrt(var.min()) * 100, 18.06, 2)
    approx("minimum volatility, card (%)", math.sqrt(var.min()) * 100, 18.1, 1)
    inv = np.linalg.inv(cov)
    a = float(np.ones(2) @ inv @ np.ones(2))
    approx("sqrt(1/A) (%)", math.sqrt(1 / a) * 100, 18.06, 2)


def tangency_two_asset() -> None:
    print("Two-asset tangency (worked example 2)")
    cov = two_asset(0.2, 0.3, 0.2)
    mu = np.array([0.05, 0.08])
    approx("Sharpe of asset 1", 0.05 / 0.2, 0.25, 2)
    approx("Sharpe of asset 2", 0.08 / 0.3, 0.267, 3)
    w1 = GRID
    ret = mu[0] * w1 + mu[1] * (1 - w1)
    sharpe = ret / np.sqrt(grid_var(cov, w1))
    i = int(np.argmax(sharpe))
    approx("tangency w1 by grid search", float(w1[i]), 0.577, 3)
    approx("tangency w2 by grid search", float(1 - w1[i]), 0.423, 3)
    approx("tangency return (%)", float(ret[i]) * 100, 6.27, 2)
    approx("tangency volatility (%)", math.sqrt(float(grid_var(cov, w1[i : i + 1])[0])) * 100, 18.79, 2)
    approx("tangency Sharpe by grid search", float(sharpe[i]), 0.334, 3)
    approx("sqrt(mu' Sigma^-1 mu)", math.sqrt(mu @ np.linalg.solve(cov, mu)), 0.334, 3)
    # utility max over a 2-D grid of holdings (cash takes the rest)
    g = np.linspace(0.0, 0.6, 1201)
    x, y = np.meshgrid(g, g, indexing="ij")
    util = mu[0] * x + mu[1] * y - 4 / 2 * (cov[0, 0] * x * x + 2 * cov[0, 1] * x * y + cov[1, 1] * y * y)
    j = np.unravel_index(np.argmax(util), util.shape)
    approx("utility-optimal holding in asset 1 (lambda = 4)", float(x[j]), 0.256, 3)
    approx("utility-optimal holding in asset 2 (lambda = 4)", float(y[j]), 0.188, 3)
    approx("fraction invested (%)", float(x[j] + y[j]) * 100, 44, 0)


def frontier_formula(rng: np.random.Generator) -> None:
    print("Frontier with a budget constraint (core concepts, card alpha-mv-frontier)")
    n = 5
    b = rng.standard_normal((n, n))
    cov = b @ b.T / n + 0.05 * np.eye(n)
    mu = rng.uniform(0.02, 0.10, n)
    inv = np.linalg.inv(cov)
    one = np.ones(n)
    a, bb, c = one @ inv @ one, one @ inv @ mu, mu @ inv @ mu
    d = a * c - bb * bb
    for m in (0.03, 0.06, 0.09):
        kkt = np.zeros((n + 2, n + 2))
        kkt[:n, :n] = cov
        kkt[:n, n] = -mu
        kkt[:n, n + 1] = -one
        kkt[n, :n] = mu
        kkt[n + 1, :n] = one
        rhs = np.concatenate([np.zeros(n), [m, 1.0]])
        sol = np.linalg.solve(kkt, rhs)
        w = sol[:n]
        assert abs(w @ cov @ w - (a * m * m - 2 * bb * m + c) / d) < 1e-12
        assert abs(sol[n] - (a * m - bb) / d) < 1e-12 and abs(sol[n + 1] - (c - bb * m) / d) < 1e-12
    budget = np.zeros((n + 1, n + 1))
    budget[:n, :n] = 2 * cov
    budget[:n, n] = one
    budget[n, :n] = one
    w_gmv = np.linalg.solve(budget, np.concatenate([np.zeros(n), [1.0]]))[:n]
    assert abs(w_gmv @ cov @ w_gmv - 1 / a) < 1e-12 and abs(w_gmv @ mu - bb / a) < 1e-12
    print("    sigma^2(m), l1 and l2 match a direct KKT solve at three targets; budget-only KKT gives GMV variance 1/A and mean B/A")


def instability() -> None:
    print("Instability with correlated assets (worked example 3, card alpha-mv-correlated-instability)")
    cov = two_asset(0.2, 0.2, 0.9)
    eig = np.linalg.eigvalsh(cov)
    approx("small eigenvalue", float(eig[0]), 0.004, 6)
    approx("large eigenvalue", float(eig[1]), 0.076, 6)
    approx("condition number", float(eig[1] / eig[0]), 19, 6)
    rows = {}
    for mu, wq, sq in (((0.05, 0.06), -0.36, 0.303), ((0.05, 0.07), -1.08, 0.380), ((0.06, 0.06), 0.50, 0.308)):
        ret = mu[0] * GRID + mu[1] * (1 - GRID)
        sharpe = ret / np.sqrt(grid_var(cov, GRID))
        i = int(np.argmax(sharpe))
        rows[mu] = float(GRID[i])
        approx(f"tangency w1 for mu = {mu}", float(GRID[i]), wq, 2)
        approx(f"tangency w2 for mu = {mu}", 1 - float(GRID[i]), 1 - wq, 2)
        approx(f"tangency Sharpe for mu = {mu}", float(sharpe[i]), sq, 3)
    approx("weight swing per asset (points)", (rows[(0.05, 0.06)] - rows[(0.05, 0.07)]) * 100, 72, 0)
    lo = GRID[(GRID >= 0) & (GRID <= 1)]
    ret = 0.05 * lo + 0.06 * (1 - lo)
    sharpe = ret / np.sqrt(grid_var(cov, lo))
    i = int(np.argmax(sharpe))
    approx("long-only w1", float(lo[i]), 0.0, 6)
    approx("long-only Sharpe", float(sharpe[i]), 0.300, 3)
    unc = math.sqrt(np.array([0.05, 0.06]) @ np.linalg.solve(cov, np.array([0.05, 0.06])))
    approx("Sharpe given up by the long-only constraint", unc - float(sharpe[i]), 0.0035, 4)


def sharpe_bias(rng: np.random.Generator) -> None:
    print("In-sample Sharpe inflation (worked example 4, card alpha-mv-insample-bias)")
    approx("E[theta_hat^2], N = 50, T = 60", 0.2**2 + 50 / 60, 0.873, 3)
    approx("in-sample Sharpe, monthly", math.sqrt(0.2**2 + 50 / 60), 0.93, 2)
    approx("in-sample Sharpe, annualised", math.sqrt(0.2**2 + 50 / 60) * math.sqrt(12), 3.2, 1)
    approx("true Sharpe, annualised", 0.2 * math.sqrt(12), 0.69, 2)
    exact("(T-1)/(T-N-2)", Fraction(59, 60 - 50 - 2), Fraction(59, 8))
    approx("with estimated covariance", 59 / 8 * (0.2**2 + 50 / 60), 6.4, 1)
    approx("known-Sigma formula, N = 10", 0.2**2 + 10 / 60, 0.207, 3)
    approx("estimated-Sigma formula, N = 10", 59 / 48 * (0.2**2 + 10 / 60), 0.254, 3)

    sims = 20_000
    for n, t in ((50, 60), (10, 60)):
        mu = np.full(n, 0.2 / math.sqrt(n))
        known, est, oos = [], [], []
        for _ in range(sims):
            x = rng.standard_normal((t, n)) + mu
            m = x.mean(0)
            known.append(m @ m)
            if n == 10:
                w = np.linalg.solve(np.cov(x, rowvar=False), m)
                est.append(m @ w)
                oos.append((w @ mu) / math.sqrt(w @ w))
        known = np.array(known)
        target = 0.2**2 + n / t
        simulated(f"known Sigma, N = {n}, simulated", float(known.mean()), round(target, 4), 4 * known.std() / math.sqrt(sims))
        if n == 10:
            est = np.array(est)
            simulated("estimated Sigma, N = 10, simulated", float(est.mean()), round(59 / 48 * target, 4), 4 * est.std() / math.sqrt(sims))
            oos = np.array(oos)
            simulated(
                "true Sharpe of the estimated tangency portfolio, N = 10", float(oos.mean()), 0.08, 4 * oos.std() / math.sqrt(sims) + 0.005
            )


def jagannathan_ma(rng: np.random.Generator) -> None:
    print("Long-only minimum variance as covariance shrinkage (core concepts, card alpha-mv-long-only-shrinkage)")
    n = 6
    b = rng.standard_normal((n, n))
    cov = b @ b.T / n + 0.02 * np.eye(n)
    # long-only minimum variance by active-set enumeration
    best = None
    for mask in range(1, 2**n):
        idx = [i for i in range(n) if mask >> i & 1]
        sub = cov[np.ix_(idx, idx)]
        w_sub = np.linalg.solve(sub, np.ones(len(idx)))
        w_sub /= w_sub.sum()
        if np.all(w_sub >= -1e-12):
            w = np.zeros(n)
            w[idx] = w_sub
            if best is None or w @ cov @ w < best @ cov @ best:
                best = w
    w = best
    lam_star = w @ cov @ w
    lam = np.maximum(cov @ w - lam_star, 0.0)  # KKT multipliers of w >= 0 (zero where the weight is positive)
    shrunk = cov - (np.outer(lam, np.ones(n)) + np.outer(np.ones(n), lam))
    w_unc = np.linalg.solve(shrunk, np.ones(n))
    w_unc /= w_unc.sum()
    assert np.allclose(w_unc, w, atol=1e-8)
    print(f"    {int((w <= 1e-9).sum())} of {n} weights bind at zero; the GMV of Sigma - (lam 1' + 1 lam') equals the long-only GMV")


def mean_precision() -> None:
    print("How hard means are to estimate (card alpha-mv-means-vs-cov)")
    approx("SE of a mean with 16% vol after 30 years (%)", 16 / math.sqrt(30), 2.9, 1)


def no_trade_band() -> None:
    print("No-trade band from linear costs (worked example 5, card alpha-mv-no-trade-band)")
    mu, sigma, lam, c = 0.05, 0.2, 5.0, 0.01
    approx("frictionless target", mu / (lam * sigma**2), 0.25, 2)
    w = np.linspace(0.0, 0.5, 500_001)

    def best_from(w0: float) -> float:
        util = mu * w - lam / 2 * sigma**2 * w * w - c * np.abs(w - w0)
        return float(w[np.argmax(util)])

    approx("optimal weight from w0 = 0.10", best_from(0.10), 0.20, 4)
    approx("optimal weight from w0 = 0.27", best_from(0.27), 0.27, 4)
    starts = np.linspace(0.0, 0.5, 501)
    stay = [w0 for w0 in starts if abs(best_from(w0) - w0) < 1e-6]
    approx("lower edge of the no-trade band", min(stay), 0.20, 3)
    approx("upper edge of the no-trade band", max(stay), 0.30, 3)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    gmv_two_asset()
    tangency_two_asset()
    frontier_formula(rng)
    instability()
    sharpe_bias(rng)
    jagannathan_ma(rng)
    mean_precision()
    no_trade_band()
    print("All mean-variance numbers check.")
