"""Curriculum notes: the few computed numbers in Learning-Path and Masters-Codex.

Backs `16-Trading-and-Investing/00-Curriculum/Learning-Path.md` (the Rule of 16 and the daily rhythm total) and
`16-Trading-and-Investing/00-Curriculum/Masters-Codex.md` (the 5:1 reward-to-risk arithmetic).
Independent routes used here:
- sqrt(252) by integer bisection on squares, checked against a seeded simulation of 252 iid daily
  returns whose annual standard deviation must match sqrt(252) times the daily one;
- 5:1 breakeven win rate and expectancy in exact rational arithmetic (`fractions.Fraction`),
  checked against a seeded simulation of Bernoulli trades with a standard-error tolerance.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_hist_00_curriculum.py`.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

SEED = 20261114


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def sqrt_by_bisection(n: int, digits: int) -> float:
    """Square root of n to `digits` decimals by bisection on integer squares (no math.sqrt)."""
    scale = 10**digits
    target = n * scale * scale
    lo, hi = 0, n * scale + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid * mid <= target:
            lo = mid
        else:
            hi = mid
    return lo / scale


def rule_of_16(rng: np.random.Generator) -> None:
    print("Learning-Path: Rule of 16")
    root = sqrt_by_bisection(252, 6)
    approx("sqrt(252)", root, 15.87, 2)
    # Simulation route: annual sd of a sum of 252 iid daily returns is sqrt(252) times the daily sd.
    daily_sd = 0.01
    years = 200_000
    annual = rng.normal(0.0, daily_sd, size=(years, 252)).sum(axis=1)
    ratio = annual.std(ddof=1) / daily_sd
    # sd of a sample sd is about sd / sqrt(2 (n - 1)); scale by the ratio and allow 5 standard errors.
    se = ratio / np.sqrt(2 * (years - 1))
    simulated("annual sd / daily sd", float(ratio), 15.87, 5 * se + 0.005)
    # 16% annual vol is about 1% a day under the rule; the exact figure uses sqrt(252).
    approx("daily vol for 16% annual (exact)", 16.0 / root, 1.01, 2)


def daily_rhythm() -> None:
    print("Learning-Path: daily rhythm")
    # Blocks as listed in the note: (min, max) minutes; summed row by row, never taken from the header.
    blocks = {"cards": (10, 10), "drill": (10, 10), "lab or notes": (30, 60), "journal": (5, 5)}
    low = sum(lo for lo, _ in blocks.values())
    high = sum(hi for _, hi in blocks.values())
    assert (low, high) == (55, 85), (low, high)
    print(f"    daily rhythm minutes = {low} to {high}")


def five_to_one(rng: np.random.Generator) -> None:
    print("Masters-Codex: 5:1 reward-to-risk")
    reward, risk = Fraction(5), Fraction(1)
    breakeven = risk / (reward + risk)
    assert breakeven == Fraction(1, 6)
    approx("breakeven win rate (%)", float(100 * breakeven), 16.67, 2)
    p = Fraction(3, 10)
    expectancy = p * reward - (1 - p) * risk
    assert expectancy == Fraction(4, 5)
    approx("expectancy at 30% wins (R per trade)", float(expectancy), 0.80, 2)
    # Simulation route: Bernoulli(0.3) trades paying +5R or -1R.
    n = 2_000_000
    wins = rng.random(n) < 0.3
    pnl = np.where(wins, 5.0, -1.0)
    se = pnl.std(ddof=1) / np.sqrt(n)
    simulated("simulated expectancy (R per trade)", float(pnl.mean()), 0.80, 5 * se)


def main() -> None:
    rng = np.random.default_rng(SEED)
    rule_of_16(rng)
    daily_rhythm()
    five_to_one(rng)
    print("all curriculum numbers verified")


if __name__ == "__main__":
    main()
