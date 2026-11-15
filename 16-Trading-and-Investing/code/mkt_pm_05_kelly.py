"""Kelly criterion and capital growth: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Portfolio-Management/05-Kelly-Criterion-and-Capital-Growth-Theory.md`.
Independent routes used here:
- the Bernoulli Kelly fraction by golden-section maximisation of p ln(1 + b f) + q ln(1 - f), against (b p - q) / b,
  and the zero of the discrete growth curve by bisection;
- the share of maximum growth at c f* from a seeded simulation of a daily-rebalanced levered GBM position,
  against 2c - c^2;
- the probabilities of ever halving and of halving before doubling by solving the boundary-value problem
  0.5 s^2 P'' + m P' = 0 with finite differences, against the closed forms 0.5^a and (1 - 2^-a) / (2^a - 2^-a);
- the multi-asset Kelly vector by gradient ascent on the growth rate, against Sigma^-1 (mu - r 1).
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_pm_05_kelly.py
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261114


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:64s} {float(value):16.6f}  quoted {quoted}")
    assert abs(float(value) - float(quoted)) <= tol, f"{label}: {float(value)} does not round to {quoted}"
    return float(value)


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:58s} |diff| = {abs(a - b):.2e} (tol {tol:.1e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def golden_max(f, lo: float, hi: float) -> float:
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    for _ in range(200):
        c, d = b - g * (b - a), a + g * (b - a)
        if f(c) > f(d):
            b = d
        else:
            a = c
    return 0.5 * (a + b)


def bernoulli() -> None:
    print("Bernoulli Kelly, even money (b = 1), p = 0.55")
    p, b = 0.55, 1.0

    def g(f: float) -> float:
        return p * math.log1p(b * f) + (1 - p) * math.log1p(-f)

    fstar = golden_max(g, 0.0, 0.99)
    close("golden section vs (b p - q) / b", fstar, (b * p - (1 - p)) / b, 1e-9)
    q("Kelly fraction f*", fstar, "0.10")
    q("growth per bet at f* (x 10^4)", 1e4 * g(0.10), "50.08")
    q("growth per bet at 2 f* (x 10^4)", 1e4 * g(0.20), "-1.38")
    lo, hi = 0.15, 0.20
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(mid) > 0:
            lo = mid
        else:
            hi = mid
    q("fraction where discrete growth turns negative", 0.5 * (lo + hi), "0.1987")


def growth_share() -> None:
    print("Continuous Kelly: share of maximum excess growth at c f*, mu - r = 10%, sigma = 20% (hypothetical)")
    m, s = 0.10, 0.20
    fstar = m / s**2
    q("f* = (mu - r) / sigma^2", fstar, "2.5")
    q("maximum excess growth SR^2 / 2 (% a year)", 100 * 0.5 * (m / s) ** 2, "12.5")
    gmax = 0.5 * (m / s) ** 2
    # route 1: Gauss-Hermite quadrature of E[log(1 + f R)] for a daily-rebalanced position, R the daily lognormal return
    nodes, weights = np.polynomial.hermite_e.hermegauss(80)
    weights = weights / weights.sum()

    def quad_growth(c: float, dt: float) -> float:
        asset = np.exp((m - 0.5 * s * s) * dt + s * math.sqrt(dt) * nodes) - 1
        return float(weights @ np.log1p(c * fstar * asset)) / dt

    # route 2: a seeded simulation of a daily-rebalanced position, compared with the daily quadrature
    rng = np.random.default_rng(SEED)
    daily, steps = 1 / 252, 252 * 4000
    asset_s = np.exp((m - 0.5 * s * s) * daily + s * math.sqrt(daily) * rng.standard_normal(steps)) - 1
    for c, quoted in ((0.25, "43.75"), (0.5, "75.00"), (0.75, "93.75"), (1.0, "100.00"), (1.5, "75.00"), (2.0, "0.00")):
        # rebalancing 100 times a day makes the O(dt) discretisation term about 1e-5 a year
        close(f"quadrature excess growth at c = {c}, near-continuous rebalancing", quad_growth(c, 1 / 25_200), gmax * (2 * c - c * c), 1e-4)
        logret = np.log1p(c * fstar * asset_s)
        se = logret.std(ddof=1) / math.sqrt(steps) / daily
        close(f"simulated daily growth at c = {c} (5 standard errors)", logret.mean() / daily, quad_growth(c, daily), 5 * se)
        q(f"share of maximum growth at c = {c} (%)", 100 * (2 * c - c * c), quoted)


def bvp_hit_lower(drift: float, var: float, lower: float, upper: float, n: int = 20_000) -> float:
    """P(Brownian motion from 0 hits `lower` before `upper`), by finite differences on 0.5 var P'' + drift P' = 0."""
    x = np.linspace(lower, upper, n + 1)
    h = x[1] - x[0]
    a = 0.5 * var / h**2 - 0.5 * drift / h
    c = 0.5 * var / h**2 + 0.5 * drift / h
    bdiag = -var / h**2
    # Thomas algorithm for the tridiagonal system with P(lower) = 1, P(upper) = 0
    k = n - 1
    cp = np.zeros(k)
    dp = np.zeros(k)
    rhs = np.zeros(k)
    rhs[0] = -a * 1.0
    cp[0] = c / bdiag
    dp[0] = rhs[0] / bdiag
    for i in range(1, k):
        den = bdiag - a * cp[i - 1]
        cp[i] = c / den
        dp[i] = (rhs[i] - a * dp[i - 1]) / den
    sol = np.zeros(k)
    sol[-1] = dp[-1]
    for i in range(k - 2, -1, -1):
        sol[i] = dp[i] - cp[i] * sol[i + 1]
    full = np.concatenate([[1.0], sol, [0.0]])
    return float(np.interp(0.0, x, full))


def drawdown_odds() -> None:
    print("Fractional Kelly c = f / f*: log wealth over the riskless path has 2 drift / variance = a = 2/c - 1")
    rows = (
        (0.25, "0.78", "0.78"),
        (0.5, "12.50", "11.11"),
        (0.75, "31.50", "23.95"),
        (1.0, "50.00", "33.33"),
        (1.5, "79.37", "44.25"),
    )
    ln2 = math.log(2)
    for c, ever_q, before_q in rows:
        a = 2 / c - 1
        # take drift a/2 and variance 1 so that 2 drift / variance = a
        ever_closed = 0.5**a
        before_closed = (1 - 2**-a) / (2**a - 2**-a)
        far = 40.0 / a
        ever_fd = bvp_hit_lower(a / 2, 1.0, -ln2, far)
        before_fd = bvp_hit_lower(a / 2, 1.0, -ln2, ln2)
        close(f"finite-difference P(ever halve) at c = {c}", ever_fd, ever_closed, 1e-5)
        close(f"finite-difference P(halve before double) at c = {c}", before_fd, before_closed, 1e-5)
        q(f"P(ever halve) at c = {c} (%)", 100 * ever_closed, ever_q)
        q(f"P(halve before double) at c = {c} (%)", 100 * before_closed, before_q)
    q("P(ever halve) at c = 2, where a = 0 (%)", 100 * 0.5 ** (2 / 2.0 - 1), "100.00")
    q("P(double before halve) at half Kelly", 1 - (1 - 2**-3) / (2**3 - 2**-3), "0.8889")
    q("limit of P(halve before double) as c -> 2 (%)", 100 * bvp_hit_lower(1e-9, 1.0, -ln2, ln2), "50.00")
    q("ratio of P(ever halve), 1.5 f* vs 0.5 f*", 0.5 ** (2 / 1.5 - 1) / 0.5**3, "6.35")
    q("excess growth share at 2.5 f* (estimated SR 1.0, true 0.4)", 2 * 2.5 - 2.5**2, "-1.25")
    q("Kelly fraction ratio when volatility doubles", (1 / 0.2**2) / (1 / 0.4**2), "4")


def matrix_kelly() -> None:
    print("Multi-asset Kelly by gradient ascent (hypothetical two-asset inputs)")
    mu_ex = np.array([0.06, 0.03])
    vol = np.array([0.20, 0.10])
    cov = np.outer(vol, vol) * np.array([[1.0, 0.3], [0.3, 1.0]])
    closed = np.linalg.solve(cov, mu_ex)
    f = np.zeros(2)
    for _ in range(200_000):
        f += 0.5 * (mu_ex - cov @ f)
    close("gradient ascent vs Sigma^-1 (mu - r), asset 1", f[0], closed[0], 1e-9)
    close("gradient ascent vs Sigma^-1 (mu - r), asset 2", f[1], closed[1], 1e-9)


def main() -> None:
    bernoulli()
    growth_share()
    drawdown_odds()
    matrix_kelly()
    print("all Kelly checks passed")


if __name__ == "__main__":
    main()
