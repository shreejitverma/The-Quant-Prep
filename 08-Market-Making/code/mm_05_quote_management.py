"""Quote management: every number in `08-Market-Making/05-Quote-Management-Skew-Width-and-Size.md`.

Independent routes used here:
- the square-root-of-time volatility scaling by a seeded simulation of per-second Gaussian steps
  (tolerance three standard errors of the sample standard deviation);
- quote expected values in exact rational arithmetic with `fractions.Fraction`, and the
  break-even adverse move by bisection rather than by rearranging the formula;
- quote sizes by brute force over every integer size against the loss-budget and position-limit rules;
- the toxicity table by counting fills per hour, and the width that maximises edge by enumeration.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 08-Market-Making/code/mm_05_quote_management.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction as F

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
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.5f} (expected {expected:.5f}, tolerance {tol:.5f})")


def example1(rng: np.random.Generator) -> None:
    print("Example 1: is a one-tick market worth quoting? (cards mm-quote-one-tick-breakeven, mm-quote-holding-risk-charge)")
    sigma_s = 40 * 0.015 / math.sqrt(6.5 * 3600)
    approx("per-second volatility (dollars)", sigma_s, 0.00392, 5)
    hold = sigma_s * math.sqrt(30)
    approx("sigma sqrt(30)", hold, 0.0215, 4)
    # simulation: 30 one-second steps summed, sample standard deviation vs sigma sqrt(30)
    paths = 200_000
    sums = rng.normal(0.0, sigma_s, size=(paths, 30)).sum(axis=1)
    simulated("sd of 30 summed one-second steps", float(sums.std(ddof=1)), hold, 3 * hold / math.sqrt(2 * paths))
    charge = 0.25 * hold
    approx("risk charge kappa x sigma sqrt(tau)", charge, 0.0054, 4)
    h_min = 0.0003 - 0.0020 + 0.0040 + charge
    approx("h_min", h_min, 0.0077, 4)
    approx("shown working: h_min from the rounded charge", 0.0003 - 0.002 + 0.004 + 0.0054, 0.0077, 4)
    assert h_min > 0.005
    print("    half-spread 0.005 < h_min: quoting both sides at the touch loses on average")


def example2() -> None:
    print("Example 2: damped skew (cards mm-quote-damped-skew, mm-quote-damped-skew-value)")
    s_max, beta, q_max = 2.0, 1.5, 10_000
    for q, tanh_lit, lin_lit in ((3000, 0.84, 0.60), (6000, 1.43, 1.20), (9000, 1.75, 1.80), (10000, 1.81, 2.00)):
        x = beta * q / q_max
        damped = s_max * (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)  # tanh from exponentials
        approx(f"tanh skew at {q}", damped, tanh_lit, 2)
        approx(f"linear skew at {q}", s_max * q / q_max, lin_lit, 2)
    eps = 1e-6
    slope_ratio = (s_max * math.tanh(beta * eps / q_max) / eps) / (s_max / q_max)
    approx("slope at zero, damped over linear (= beta)", slope_ratio, 1.5, 6)
    assert s_max * math.tanh(beta * 1e9 / q_max) <= s_max
    lo, hi = 1000.0, 10_000.0  # damped minus linear changes sign once on this interval
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if s_max * math.tanh(beta * mid / q_max) > s_max * mid / q_max else (lo, mid)
    approx("position where damped and linear skew cross (hundreds of shares)", lo / 100, 86, 0)
    print("    the damped rule saturates at S_max")


def example3() -> None:
    print("Example 3: join or improve (cards mm-quote-join-vs-improve, mm-quote-improve-breakeven)")
    join = F(3, 10) * (2 - F(12, 10))
    improve = F(8, 10) * (1 - F(9, 10))
    exact("EV join (ticks)", join, F(24, 100))
    exact("EV improve (ticks)", improve, F(8, 100))
    exact("EV improve with 0.5-tick adverse move", F(8, 10) * (1 - F(5, 10)), F(40, 100))
    lo, hi = 0.0, 1.0  # adverse move on improved fills at which improving ties with joining
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if 0.8 * (1 - mid) > float(join) else (lo, mid)
    approx("break-even adverse move for improving", lo, 0.7, 6)


def example4() -> None:
    print("Example 4: sizing from a loss budget (cards mm-quote-size-rule, mm-quote-ask-cap)")
    budget, jump, pos, limit = 5000, 0.25, 3000, 10_000
    sizes = range(0, 50_001)
    bid = max(n for n in sizes if n * jump <= budget and pos + n <= limit)
    ask = max(n for n in sizes if n * jump <= budget and pos - n >= -limit)
    exact("loss-budget size", max(n for n in sizes if n * jump <= budget), 20_000)
    exact("bid size", bid, 7000)
    exact("ask size", ask, 13_000)


def example5() -> None:
    print("Example 5: width against toxicity (cards mm-quote-width-vs-toxicity, mm-quote-toxicity-table)")
    jump = 3
    uninformed = {1: 100, 2: 30, 3: 10}
    for informed, row in ((20, {1: 60, 2: 40, 3: 30}), (60, {1: -20, 2: 0, 3: 30})):
        edge = {h: uninformed[h] * h + informed * (h - jump) for h in uninformed}
        exact(f"edge per hour with {informed} informed fills", edge, row)
        best = max(edge, key=edge.get)
        print(f"    best half-spread with {informed} informed fills = {best}")
        assert best == (1 if informed == 20 else 3)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    example1(rng)
    example2()
    example3()
    example4()
    example5()
    print("all quote management checks passed")
