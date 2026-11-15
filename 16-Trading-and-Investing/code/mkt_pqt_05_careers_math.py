"""Careers note: every number in the worked examples and cards, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/05-Quant-and-Prop-Trading-Careers.md`.
Independent routes used here:
- Example 1 bonus pool from a signed line-item ledger summed in exact decimal arithmetic, against the
  note's step-by-step subtotals;
- Example 2 posterior P(loaded | 6) by Bayes in exact fractions, by enumerating the equally likely
  (die, face) outcomes with the loaded die's faces weighted in tenths, and by a seeded simulation with a
  five-standard-error band;
- card mkt-car-026: the gambler's-ruin probability k / A by solving the absorbing Markov chain's linear
  system with numpy and by a seeded simulation;
- Example 3 struct sizes and field offsets from ctypes layouts of the two C structs.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_pqt_05_careers_math.py`.
"""

from __future__ import annotations

import ctypes
from decimal import Decimal
from fractions import Fraction

import numpy as np

SEED = 53


def rounded(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(value):,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def example_1() -> None:
    print("Example 1: desk bonus pool")
    ledger = [
        ("gross trading profits", Decimal(18_500_000)),
        ("exchange fees, clearing, brokerage", Decimal(-3_200_000)),
        ("infrastructure overhead", Decimal(-1_100_000)),
        ("base salaries", Decimal(-600_000)),
        ("capital charge 6% on $40m", Decimal(-40_000_000) * Decimal("0.06")),
    ]
    net = sum(v for _, v in ledger)
    direct = -sum(v for k, v in ledger if k in ("exchange fees, clearing, brokerage", "infrastructure overhead", "base salaries"))
    rounded("direct expenses", direct, "4,900,000")
    rounded("capital charge", -ledger[-1][1], "2,400,000")
    rounded("net economic PnL", net, "11,200,000")
    pool = max(Decimal(0), Decimal("0.20") * net)
    rounded("bonus pool", pool, "2,240,000")
    rounded("total desk compensation", pool + 600_000, "2,840,000")


def example_2(rng: np.random.Generator) -> None:
    print("Example 2: loaded-die posterior")
    p_l, p_f = Fraction(1, 4), Fraction(3, 4)
    l6, f6 = Fraction(1, 2), Fraction(1, 6)
    p6 = l6 * p_l + f6 * p_f
    rounded("P(L)", p_l, "0.25")
    rounded("P(F)", p_f, "0.75")
    rounded("P(6 | L) P(L)", l6 * p_l, "0.125")
    rounded("P(6 | F) P(F)", f6 * p_f, "0.125")
    rounded("P(6)", p6, "0.25")
    rounded("P(L | 6), Bayes", l6 * p_l / p6, "0.50")
    # enumeration: 4 dice x 60 equally weighted face-slots (fair face = 10 slots, loaded 6 = 30 slots)
    slots = []
    for die in range(4):
        loaded = die == 3
        for face in range(1, 7):
            weight = (30 if face == 6 else 6) if loaded else 10
            slots += [(loaded, face)] * weight
    sixes = [loaded for loaded, face in slots if face == 6]
    rounded("P(L | 6), enumeration", Fraction(sum(sixes), len(sixes)), "0.50")
    n = 2_000_000
    loaded = rng.random(n) < 0.25
    six = np.where(loaded, rng.random(n) < 0.5, rng.integers(1, 7, n) == 6)
    est = loaded[six].mean()
    se = np.sqrt(est * (1 - est) / six.sum())
    print(f"    P(L | 6), simulation (seed {SEED}) = {est:.4f} +/- {se:.4f}")
    assert abs(est - 0.5) < 5 * se
    rounded("edge per contract bought at 0.47", Fraction(1, 2) - Fraction(47, 100), "0.03")


def gamblers_ruin(rng: np.random.Generator) -> None:
    print("Card mkt-car-026: gambler's ruin")
    a = 10
    m = np.zeros((a + 1, a + 1))
    b = np.zeros(a + 1)
    m[0, 0] = m[a, a] = 1.0
    b[a] = 1.0
    for k in range(1, a):
        m[k, k], m[k, k - 1], m[k, k + 1] = 1.0, -0.5, -0.5
    h = np.linalg.solve(m, b)
    assert np.allclose(h, np.arange(a + 1) / a, atol=1e-12)
    print(f"    linear system P(hit {a} before 0 | k) = {np.round(h, 6).tolist()}")
    k0, paths = 3, 100_000
    pos = np.full(paths, k0)
    alive = np.ones(paths, dtype=bool)
    while alive.any():
        pos[alive] += rng.choice([-1, 1], alive.sum())
        alive &= (pos > 0) & (pos < a)
    est = (pos == a).mean()
    se = np.sqrt(est * (1 - est) / paths)
    print(f"    simulated P(hit {a} before 0 | k = {k0}) = {est:.4f} +/- {se:.4f}, k / A = {k0 / a}")
    assert abs(est - k0 / a) < 5 * se


def example_3() -> None:
    print("Example 3: struct layouts")

    class BadDeskStats(ctypes.Structure):
        _fields_ = [(f"fills_core{i}", ctypes.c_uint64) for i in range(4)]

    class CoreStats(ctypes.Structure):
        _fields_ = [("fills", ctypes.c_uint64), ("padding", ctypes.c_char * 56)]

    class OptimizedDeskStats(ctypes.Structure):
        _fields_ = [("cores", CoreStats * 4)]

    offsets = [getattr(BadDeskStats, f"fills_core{i}").offset for i in range(4)]
    print(f"    BadDeskStats offsets = {offsets}")
    assert offsets == [0, 8, 16, 24]
    rounded("sizeof(BadDeskStats)", ctypes.sizeof(BadDeskStats), "32")
    rounded("padding bytes", 64 - ctypes.sizeof(ctypes.c_uint64), "56")
    rounded("sizeof(CoreStats)", ctypes.sizeof(CoreStats), "64")
    rounded("sizeof(OptimizedDeskStats)", ctypes.sizeof(OptimizedDeskStats), "256")
    # every core's counter sits in a distinct 64-byte line when the array starts on a line boundary
    lines = {(i * ctypes.sizeof(CoreStats)) // 64 for i in range(4)}
    assert len(lines) == 4
    assert len({o // 64 for o in offsets}) == 1


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    example_1()
    example_2(rng)
    gamblers_ruin(rng)
    example_3()
    print("all careers-note numbers check out")
