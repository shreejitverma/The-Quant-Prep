"""Drawdown mathematics and risk of ruin: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Portfolio-Management/04-Drawdown-Mathematics-and-Risk-of-Ruin.md`.
Independent routes used here:
- recovery returns D / (1 - D) in exact fractions, against bisection on (1 - D)(1 + R) = 1;
- the recovery time by bisection on 1.1^t = 2, against ln 2 / ln 1.1;
- gambler's-ruin probabilities from the closed form, against an exact rational solve with a far upper barrier,
  a numerical solve of the difference equation as a linear system, and a seeded simulation;
- expected maximum drawdown of Brownian motion from Magdon-Ismail et al. (2004), against a seeded simulation
  with Richardson extrapolation in the step size;
- the sequence-of-returns table by stepping the wealth recursion, against the closed-form sum of
  compounded withdrawals; the geometric mean by the product root and by the mean log return;
- the CPPI floor test by applying a gap to the cushion rule.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_pm_04_drawdown_ruin.py
"""

from __future__ import annotations

import math
from fractions import Fraction

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


def bisect(f, lo: float, hi: float) -> float:
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def recovery_table() -> None:
    print("Recovery return after a drawdown D")
    rows = (
        (10, "11.11", "1.11"),
        (20, "25.00", "1.25"),
        (30, "42.86", "1.43"),
        (40, "66.67", "1.67"),
        (50, "100.00", "2.00"),
        (60, "150.00", "2.50"),
        (75, "300.00", "4.00"),
        (90, "900.00", "10.00"),
        (95, "1900.00", "20.00"),
        (99, "9900.00", "100.00"),
    )
    for d_pct, r_q, m_q in rows:
        d = Fraction(d_pct, 100)
        exact = d / (1 - d)
        root = bisect(lambda r, d=float(d): (1 - d) * (1 + r) - 1, 0.0, 200.0)
        close(f"bisection vs D/(1-D) at D = {d_pct}%", root, float(exact), 1e-9)
        q(f"required gain after a {d_pct}% drawdown (%)", 100 * exact, r_q)
        q(f"multiple of remaining capital 1/(1-D) at D = {d_pct}%", 1 / (1 - d), m_q)
    h = 1e-4
    f = lambda d: d / (1 - d)  # noqa: E731
    for d, quoted in ((0.3, "5.83"), (0.5, "16")):
        fd = (f(d + h) - 2 * f(d) + f(d - h)) / (h * h)
        close(f"second derivative 2/(1-D)^3 vs finite difference at D = {d}", 2 / (1 - d) ** 3, fd, 1e-4)
        q(f"curvature of the recovery curve at D = {d}", fd, quoted)
    t = bisect(lambda x: 1.1**x - 2, 0.0, 50.0)
    close("bisection vs ln 2 / ln 1.1", t, math.log(2) / math.log(1.1), 1e-9)
    q("years to double at 10% a year", t, "7.27")
    two = 1 - Fraction(3, 4) ** 2
    q("two 25% drawdowns compound to (%)", 100 * two, "43.75")
    q("recovery needed after 43.75% (%)", 100 * two / (1 - two), "77.8")


def ruin_closed(p: float, c: int) -> float:
    return 1.0 if p <= 0.5 else ((1 - p) / p) ** c


def ruin_finite_exact(p: Fraction, c: int, b: int) -> Fraction:
    r = (1 - p) / p
    if r == 1:
        return 1 - Fraction(c, b)
    return (r**b - r**c) / (r**b - 1)


def ruin_linear_system(p: float, c: int, b: int) -> float:
    """Solve P(k) = p P(k+1) + q P(k-1), P(0) = 1, P(b) = 0, for k = 1..b-1."""
    n = b - 1
    a = np.zeros((n, n))
    rhs = np.zeros(n)
    for i in range(n):
        a[i, i] = 1.0
        if i + 1 < n:
            a[i, i + 1] = -p
        if i - 1 >= 0:
            a[i, i - 1] = -(1 - p)
        else:
            rhs[i] = 1 - p
    return float(np.linalg.solve(a, rhs)[c - 1])


def gamblers_ruin() -> None:
    print("Gambler's ruin with unit bets and no upper target")
    table = {
        0.48: ("1.0833", ("100.00", "100.00", "100.00")),
        0.50: ("1.0000", ("100.00", "100.00", "100.00")),
        0.52: ("0.9231", ("44.91", "13.52", "1.83")),
        0.55: ("0.8182", ("13.44", "0.66", "0.0044")),
        0.60: ("0.6667", ("1.73", "0.0040", "0.00")),
    }
    for p, (ratio_q, quoted) in table.items():
        q(f"q / p at p = {p}", (1 - p) / p, ratio_q)
        pf = Fraction(p).limit_denominator(1000)
        for c, lit in zip((10, 25, 50), quoted, strict=True):
            closed = ruin_closed(p, c)
            far = ruin_finite_exact(pf, c, 400 if p != 0.5 else 10**9)
            close(f"closed form vs exact far barrier, p = {p}, C = {c}", closed, float(far), 1e-6)
            if p > 0.5:
                lin = ruin_linear_system(p, c, 1500)
                close(f"closed form vs linear system, p = {p}, C = {c}", closed, lin, 1e-9)
            q(f"P(ruin) at p = {p}, C = {c} (%)", 100 * closed, lit)
    rng = np.random.default_rng(SEED)
    walks, cap = 40_000, 250
    wealth = np.full(walks, 10)
    alive = np.ones(walks, dtype=bool)
    ruined = np.zeros(walks, dtype=bool)
    while alive.any():
        steps = np.where(rng.random(alive.sum()) < 0.55, 1, -1)
        wealth[alive] += steps
        ruined |= wealth <= 0
        alive &= (wealth > 0) & (wealth < cap)
    p_sim = ruined.mean()
    se = math.sqrt(p_sim * (1 - p_sim) / walks)
    close("simulated ruin at p = 0.55, C = 10 (5 standard errors)", p_sim, ruin_closed(0.55, 10), 5 * se)


def max_drawdown(x: np.ndarray) -> np.ndarray:
    return (np.maximum.accumulate(x, axis=1) - x).max(axis=1)


def simulated_mdd(rng: np.random.Generator, mu: float, sig: float, horizon: float, n: int, paths: int) -> tuple[float, float]:
    """Mean max drawdown of Brownian motion; fine and 4x-coarse grids extrapolated to dt -> 0 (bias ~ sqrt(dt))."""
    dt = horizon / n
    out = []
    for _ in range(paths // 2000):
        inc = mu * dt + sig * math.sqrt(dt) * rng.standard_normal((2000, n))
        x = np.concatenate([np.zeros((2000, 1)), np.cumsum(inc, axis=1)], axis=1)
        out.append(2 * max_drawdown(x) - max_drawdown(x[:, ::4]))
    ext = np.concatenate(out)
    return float(ext.mean()), float(ext.std(ddof=1) / math.sqrt(len(ext)))


def brownian_drawdown() -> None:
    print("Expected maximum drawdown of Brownian motion (Magdon-Ismail et al. 2004)")
    q("sqrt(pi / 2)", math.sqrt(math.pi / 2), "1.2533")
    n_h = 100_000
    euler_gamma = math.fsum(1.0 / k for k in range(1, n_h + 1)) - math.log(n_h) - 1 / (2 * n_h) + 1 / (12 * n_h**2)
    q("Euler-Mascheroni constant, H_n - ln n - 1/(2n) + 1/(12n^2)", euler_gamma, "0.5772")
    rng = np.random.default_rng(SEED + 1)
    sim, se = simulated_mdd(rng, 0.0, 1.0, 1.0, 4000, 20_000)
    close("simulated E[MDD], zero drift, sigma = 1, T = 1 (5 standard errors)", sim, math.sqrt(math.pi / 2), 5 * se)
    asym = 0.5 * (math.log(2 * 1.0 * 50.0) + euler_gamma)
    sim, se = simulated_mdd(rng, 1.0, 1.0, 50.0, 20_000, 4_000)
    close("simulated E[MDD], alpha = 1, sigma = 1, T = 50 (5 standard errors)", sim, asym, 5 * se)
    q("asymptotic E[MDD] at alpha = 1, sigma = 1, T = 50", asym, "2.591")
    print("  diffusion barrier: P(ever fall by D) = exp(-2 alpha D / sigma^2) for alpha > 0")


def sequence_risk() -> None:
    print("Sequence of returns: $1,000,000, $60,000 withdrawn at year end, growing 2% a year (hypothetical)")
    bear = [-0.25, -0.15, -0.05, 0.05, 0.15, 0.25]
    bull = bear[::-1]
    lits = {
        "A": ("690000", "525300", "436611", "394769", "389039", "420053"),
        "B": ("1190000", "1307300", "1310241", "1181056", "938952", "637969"),
    }
    for name, seq in (("A", bear), ("B", bull)):
        w = Fraction(1_000_000)
        path = []
        for k, r in enumerate(seq):
            w = w * (1 + Fraction(r).limit_denominator(100)) - Fraction(60_000) * Fraction(102, 100) ** k
            path.append(w)
        for n in range(1, 7):
            growth = math.prod(1 + r for r in seq[:n])
            withdrawals = sum(60_000 * 1.02**k * math.prod(1 + r for r in seq[k + 1 : n]) for k in range(n))
            close(f"recursion vs closed-form sum, sequence {name}, year {n}", float(path[n - 1]), 1e6 * growth - withdrawals, 1e-6)
            q(f"sequence {name} capital after year {n} ($)", path[n - 1], lits[name][n - 1])
    prod = math.prod(1 + r for r in bear)
    gm = prod ** (1 / 6) - 1
    close("geometric mean via mean log return", gm, math.exp(sum(math.log1p(r) for r in bear) / 6) - 1, 1e-14)
    q("geometric mean return of either sequence (%)", 100 * gm, "-1.49")


def cppi() -> None:
    print("CPPI with W = 100, floor F = 80, multiplier m = 4 (hypothetical)")
    w, floor, m = 100.0, 80.0, 4
    cushion = w - floor
    equity = m * cushion
    q("equity exposure m x cushion", equity, "80")
    q("largest gap that keeps W >= F, 1 / m (%)", 100 / m, "25")
    for gap, quoted in ((-0.25, "80"), (-0.30, "76")):
        q(f"wealth after a {100 * gap:.0f}% gap", w + equity * gap, quoted)


def main() -> None:
    recovery_table()
    gamblers_ruin()
    brownian_drawdown()
    sequence_risk()
    cppi()
    print("all drawdown and ruin checks passed")


if __name__ == "__main__":
    main()
