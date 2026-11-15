"""Market making fundamentals: every P&L decomposition, fee and break-even number in the note.

Backs every number in `08-Market-Making/01-Market-Making-Fundamentals.md`.
Independent routes used here:
- the three-fill tape decomposed fill by fill in exact `fractions.Fraction` arithmetic and checked against the
  cash-plus-marked-position P&L computed directly from the trades;
- the telescoping identity checked on a seeded random tape of 10,000 fills;
- break-even half-spreads by enumerating the informed and uninformed outcomes and solving for zero expected P&L by
  bisection, never by rearranging h + r = pi J;
- the break-even condition checked by a seeded simulation of informed fills.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 08-Market-Making/code/mm_01_market_making_fundamentals.py`.
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
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def section_tape(rng: np.random.Generator) -> None:
    print("Example 1: decomposing a three-fill tape (cards mm-fund-pnl-four-components, mm-fund-telescoping-identity)")
    size = 100
    m_close = F("99.99")
    # side (+1 buy), price, mid at fill, mid 1 s later
    tape = [
        (+1, F("99.99"), F("100.00"), F("99.995")),
        (+1, F("99.98"), F("99.99"), F("99.985")),
        (-1, F("100.00"), F("99.99"), F("99.995")),
    ]
    spread = sum(size * d * (m - p) for d, p, m, _ in tape)
    adverse = sum(size * d * (m1 - m) for d, _, m, m1 in tape)
    inventory = sum(size * d * (m_close - m1) for d, _, _, m1 in tape)
    exact("spread capture, dollars", spread, 3)
    exact("adverse selection per fill", [d * (m1 - m) for d, _, m, m1 in tape], [F("-0.005")] * 3)
    exact("adverse selection, dollars", adverse, F("-1.5"))
    exact("inventory P&L per fill", [d * (m_close - m1) for d, _, _, m1 in tape], [F("-0.005"), F("0.005"), F("0.005")])
    exact("inventory P&L, dollars", inventory, F("0.5"))
    exact("sum of components, dollars", spread + adverse + inventory, 2)
    cash = sum(-d * size * p for d, p, _, _ in tape)
    position = sum(d * size for d, _, _, _ in tape)
    exact("cash, dollars", cash, -9997)
    exact("final position, shares", position, 100)
    exact("position marked at the close, dollars", position * m_close, 9999)
    exact("direct P&L, dollars", cash + position * m_close, 2)
    exact("share of spread capture given back within 1 s", -adverse / spread, F(1, 2))

    n = 10_000
    side = rng.choice([-1, 1], n)
    mid = 100 + np.cumsum(rng.normal(0, 0.01, n + 1))
    price = mid[:-1] - side * 0.01
    later = mid[np.minimum(np.arange(n) + 5, n)]
    close = mid[-1]
    lhs = float(np.sum(side * (close - price)))
    parts = float(np.sum(side * (mid[:-1] - price)) + np.sum(side * (later - mid[:-1])) + np.sum(side * (close - later)))
    cash_route = float(-np.sum(side * price) + np.sum(side) * close)
    assert abs(lhs - parts) < 1e-8 and abs(lhs - cash_route) < 1e-8, (lhs, parts, cash_route)
    print("    telescoping identity and cash route agree on a seeded 10,000-fill tape")


def section_day() -> None:
    print("Example 2: a day of P&L with fees")
    shares = 1000 * 100
    exact("shares filled", shares, 100_000)
    spread = shares * F("0.01")
    adverse = -shares * F("0.006")
    rebate = shares * F("0.0020")
    costs = -shares * F("0.0005")
    inventory = F(-150)
    exact("spread capture", spread, 1000)
    exact("adverse selection", adverse, -600)
    exact("rebates", rebate, 200)
    exact("costs", costs, -50)
    net = spread + adverse + rebate + costs + inventory
    exact("net P&L, dollars", net, 400)
    exact("net per share, cents", net / shares * 100, F(4, 10))
    exact("rebate as a share of net P&L", rebate / net, F(1, 2))


def section_fill_rate() -> None:
    print("Example 3: fill rate versus edge (card mm-fund-fill-rate-misleading)")
    a = 1000 * (1 - F(8, 10))
    b = 300 * (1 - F(2, 10))
    exact("strategy A, ticks", a, 200)
    exact("strategy B, ticks", b, 240)
    exact("B's fills relative to A's, percent fewer", (1 - F(300, 1000)) * 100, 70)


def expected_pnl(h: F, r: F, pi: F, jump: F) -> F:
    """Enumerate the two kinds of fill: uninformed (keep h + r) and informed (keep h + r - J)."""
    outcomes = [((1 - pi), h + r), (pi, h + r - jump)]
    return sum(p * x for p, x in outcomes)


def break_even(r: F, pi: F, jump: F) -> F:
    lo, hi = F(-10), F(10)
    for _ in range(80):
        mid = (lo + hi) / 2
        if expected_pnl(mid, r, pi, jump) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def section_break_even(rng: np.random.Generator) -> None:
    print("Example 4: break-even half-spread (cards mm-fund-break-even-half-spread, mm-fund-rebate-share-of-pnl)")
    for label, r, pi, jump, quoted in (
        ("no rebate", F(0), F(2, 10), F(5), F(1)),
        ("rebate 0.3 ticks", F(3, 10), F(2, 10), F(5), F(7, 10)),
        ("news: 30% informed, 4-tick jump", F(0), F(3, 10), F(4), F(12, 10)),
    ):
        approx(f"break-even half-spread, {label}", float(break_even(r, pi, jump)), float(quoted), 9)
    exact("a 2-tick market (h = 1) after the news, ticks per fill", expected_pnl(F(1), F(0), F(3, 10), F(4)), F(-2, 10))
    n = 1_000_000
    informed = rng.random(n) < 0.2
    pnl = 1.0 - 5.0 * informed
    se = float(pnl.std(ddof=1)) / math.sqrt(n)
    simulated("simulated P&L per fill at h = 1, pi = 0.2, J = 5", float(pnl.mean()), 0.0, 5 * se)
    exact("card: 0.5 + 0.2 - 0.6 cents", F(5, 10) + F(2, 10) - F(6, 10), F(1, 10))
    exact("card: without the rebate", F(5, 10) - F(6, 10), F(-1, 10))


if __name__ == "__main__":
    generator = np.random.default_rng(SEED)
    section_tape(generator)
    section_day()
    section_fill_rate()
    section_break_even(generator)
