"""Backtesting methodology and pitfalls: every cost, look-ahead, survivorship and purging number in the note.

Backs every number in `09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md`.
Independent routes used here:
- cost drag and survivorship bias in exact `fractions.Fraction` arithmetic, and the cost drag again by
  simulating daily gross returns and charging the daily cost explicitly;
- the look-ahead Sharpe of a same-bar sign strategy by quadrature of E|r| and by a large seeded
  simulation, against the closed form sqrt(2/pi)/sqrt(1 - 2/pi) sqrt(252);
- the note's pandas snippet, run exactly as printed;
- purging and embargo by enumerating every sample's return days and testing overlap with the test fold,
  not by the hand count.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 09-Alpha-Research-and-Portfolio/code/alpha_07_backtesting.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import pandas as pd

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


def cost_drag(rng: np.random.Generator) -> None:
    print("Cost drag (worked example 1, TL;DR, card alpha-bt-cost-drag)")
    turnover, days = Fraction(30, 100), 252
    for bp, quoted in ((2, 1.35), (4, 1.20), (6, 1.05), (8, 0.90)):
        annual_cost = turnover * days * Fraction(bp, 10_000)
        net = (Fraction(15, 100) - annual_cost) / Fraction(10, 100)
        if bp == 4:
            approx("annual cost at 4 bp (%)", float(annual_cost) * 100, 3.02, 2)
        approx(f"net Sharpe at {bp} bp", float(net), quoted, 2)
        if bp == 8:
            approx("annual cost at 8 bp (%)", float(annual_cost) * 100, 6.05, 2)
    approx(
        "Sharpe moved by a 4 bp cost error (4 to 8 bp)", float(Fraction(30, 100) * days * Fraction(4, 10_000) / Fraction(10, 100)), 0.3, 1
    )
    approx("Sharpe lost per basis point of cost", float(turnover * days * Fraction(1, 10_000) / Fraction(10, 100)), 0.076, 3)
    # simulate gross daily returns and charge 30% x 4 bp each day
    n = 252 * 4000
    gross = rng.normal(0.15 / 252, 0.10 / math.sqrt(252), n)
    net = gross - 0.30 * 0.0004
    sr = net.mean() / net.std() * math.sqrt(252)
    simulated("net Sharpe from simulated daily returns", float(sr), 1.20, 4 * math.sqrt(1 / 4000))


def look_ahead(rng: np.random.Generator) -> None:
    print("The missing shift (worked example 2, TL;DR, cards alpha-bt-shift-rule and alpha-bt-noise-lookahead-sharpe)")
    ratio = math.sqrt(2 / math.pi) / math.sqrt(1 - 2 / math.pi)
    approx("E|r| / sd|r| for Gaussian r", ratio, 1.32, 2)
    approx("annualised look-ahead Sharpe", ratio * math.sqrt(252), 21.0, 1)
    x = np.linspace(-12.0, 12.0, 240001)
    phi = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    e_abs = float(np.trapezoid(np.abs(x) * phi, x))
    e_sq = float(np.trapezoid(x * x * phi, x))
    approx("E|r| / sd|r| by quadrature", e_abs / math.sqrt(e_sq - e_abs**2), 1.32, 2)
    r = rng.normal(0, 0.01, 10_000_000)
    pnl = np.sign(r) * r
    sr = pnl.mean() / pnl.std() * math.sqrt(252)
    simulated(
        "look-ahead Sharpe on 10 million noise days", float(sr), 21.0, 4 * math.sqrt((1 + 1.32**2 / 2) / r.size) * math.sqrt(252) + 0.05
    )

    # the note's snippet, exactly as printed
    snip = np.random.default_rng(2)
    ret = pd.Series(snip.normal(0, 0.01, 2520))
    pos = np.sign(ret)

    def sharpe(s: pd.Series) -> float:
        return s.mean() / s.std() * np.sqrt(252)

    approx("snippet: look-ahead Sharpe (seed 2)", float(sharpe(pos * ret)), 21, 0)
    approx("snippet: shifted Sharpe (seed 2)", float(sharpe(pos.shift(1) * ret)), 0.25, 2)


def survivorship() -> None:
    print("Survivorship bias (worked example 3, card alpha-bt-survivorship)")
    true_ret = Fraction(95, 100) * Fraction(10, 100) + Fraction(5, 100) * Fraction(-60, 100)
    exact("true equal-weight return", true_ret, Fraction(65, 1000))
    exact("bias of a survivors-only database", Fraction(10, 100) - true_ret, Fraction(35, 1000))
    exact("0.05 x (10% + 60%)", Fraction(5, 100) * (Fraction(10, 100) + Fraction(60, 100)), Fraction(35, 1000))


def purge_embargo() -> None:
    print("Purging and embargo (worked example 4, card alpha-bt-purge-embargo)")
    n, folds, horizon = 2500, 5, 10
    embargo = int(0.01 * n)
    exact("embargo samples", embargo, 25)
    fold_size = n // folds
    exact("test fold size", fold_size, 500)
    # sample t's label uses the returns of days t+1, ..., t+horizon
    days = [set(range(t + 1, t + horizon + 1)) for t in range(n)]
    sizes = []
    for f in range(folds):
        test = range(f * fold_size, (f + 1) * fold_size)
        test_days = set().union(*(days[t] for t in test))
        purged = [t for t in range(n) if t not in test and days[t] & test_days]
        after = [t for t in purged if t > test[-1]]
        start = (max(after) if after else test[-1]) + 1
        embargoed = [t for t in range(start, min(start + embargo, n)) if t not in test]
        train = [t for t in range(n) if t not in test and t not in purged and t not in embargoed]
        before = len(purged) - len(after)
        sizes.append((before, len(after), len(embargoed), len(train)))
        print(f"    fold {f}: purged before {before}, purged after {len(after)}, embargoed {len(embargoed)}, training {len(train)}")
    exact("interior fold: purged before the test fold", sizes[2][0], 9)
    exact("interior fold: purged after the test fold", sizes[2][1], 9)
    exact("interior fold: samples lost", sizes[2][0] + sizes[2][1] + sizes[2][2], 43)
    exact("interior fold: training samples", sizes[2][3], 1957)
    exact("first fold: training samples", sizes[0][3], 1966)
    exact("last fold: training samples", sizes[-1][3], 1991)
    exact("training samples with no purging or embargo", n - fold_size, 2000)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    cost_drag(rng)
    look_ahead(rng)
    survivorship()
    purge_embargo()
    print("All backtesting numbers check.")
