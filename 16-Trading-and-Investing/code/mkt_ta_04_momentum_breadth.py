"""Cross-sectional momentum, relative strength and breadth: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/04-Momentum-Relative-Strength-and-Breadth.md`.
Independent routes used here:
- the 12-1 formation window by enumerating month offsets, and the product formula against a cumulative-sum of
  log returns on a seeded return series (two different computations of the same compounded return);
- the long-short example by marking an explicit share position to market on each leg (shares bought or sold
  short at the start, valued at the end) against the percentage arithmetic in exact rational numbers;
- the breadth example (index change, A/D change, net figures) in exact rational arithmetic;
- the McClellan smoothing constants 0.10 and 0.05 by checking that alpha = 2 / (N + 1) is the EMA whose mean
  lag, summed from its explicit geometric weights, equals the (N - 1) / 2 lag of an N-day SMA, and by running
  the recursive EMA on a ramp and measuring its delay;
- the equal-weight share 1/500 in exact arithmetic.
Zweig's breadth-thrust thresholds are cited constants (Zweig 1986) printed for reference.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_04_momentum_breadth.py`.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

SEED = 4


def check(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def formation_window() -> None:
    offsets = [k for k in range(1, 13) if k != 1]  # months t-12 .. t-2, skipping t-1
    check("months in the 12-1 formation window", len(offsets), "11")
    assert min(offsets) == 2 and max(offsets) == 12
    rng = np.random.default_rng(SEED)
    r = rng.normal(0.01, 0.08, 24)  # monthly returns; index -k is month t-k
    product = np.prod([1 + r[-k] for k in offsets]) - 1
    via_logs = np.expm1(np.sum(np.log1p(r[-12:-1])))
    assert abs(product - via_logs) < 1e-12, "the window t-12..t-2 is r[-12:-1]"
    print(f"12-1 return on the seeded series (seed {SEED}) = {product:.6f}")


def long_short() -> None:
    notional = Fraction(1_000_000)
    pa0, pc0 = Fraction(50), Fraction(20)  # any start prices; the result must not depend on them
    shares_a = notional / pa0
    shares_c = notional / pc0
    pa1 = pa0 * Fraction(118, 100)
    pc1 = pc0 * Fraction(92, 100)
    pnl_long = shares_a * (pa1 - pa0)
    pnl_short = -shares_c * (pc1 - pc0)
    check("long leg P&L ($)", float(pnl_long), "180,000")
    check("short leg P&L ($)", float(pnl_short), "80,000")
    check("long-short P&L ($)", float(pnl_long + pnl_short), "260,000")
    spread = Fraction(18, 100) - Fraction(-8, 100)
    assert (pnl_long + pnl_short) / notional == spread
    check("spread return per dollar long and short (%)", float(100 * spread), "26.0")


def ranking() -> None:
    formation = {"A": Fraction(45, 100), "B": Fraction(12, 100), "C": Fraction(-28, 100)}
    print("cited: Example 1 inputs, 12-1 returns A +45.0%, B +12.0%, C -28.0%, benchmark +10.0%")
    order = sorted(formation, key=formation.get, reverse=True)
    assert order == ["A", "B", "C"], order
    print(f"winner, middle, loser = {order}")
    top = sum(1 for rank in range(1, 100) if rank >= 80)
    check("share of the 1 to 99 ranks rated 80 or higher (%)", 100 * top / 99, "20")


def breadth() -> None:
    print("cited: Example 2 inputs, stocks above the 200-day SMA 72.0% in month 1 and 38.0% in month 3")
    check("S&P 500 change month 1 to month 3 (%)", float(100 * (Fraction(5100, 4800) - 1)), "6.25")
    check("month 1 net advances", 2_200 - 800, "1,400")
    check("A/D line change over the quarter", 96_500 - 100_000, "-3,500")
    check("month 1 net new highs", 250 - 20, "230")
    check("month 3 net new highs", 65 - 140, "-75")
    check("equal weight in a 500-stock index (%)", float(100 * Fraction(1, 500)), "0.2")


def ema_lag_alpha(n: int) -> float:
    alpha = 2 / (n + 1)
    k = np.arange(5_000)
    w = alpha * (1 - alpha) ** k
    mean_lag = float(np.sum(k * w) / np.sum(w))
    assert abs(mean_lag - (n - 1) / 2) < 1e-6
    # Recursive EMA on a ramp P_t = t: its steady-state delay is the mean lag.
    ema = 0.0
    for t in range(2_000):
        ema = alpha * t + (1 - alpha) * ema
    assert abs((1_999 - ema) - (n - 1) / 2) < 1e-6
    return alpha


def mcclellan() -> None:
    check("McClellan fast EMA alpha (19 days)", ema_lag_alpha(19), "0.10")
    check("McClellan slow EMA alpha (39 days)", ema_lag_alpha(39), "0.05")


if __name__ == "__main__":
    formation_window()
    ranking()
    long_short()
    breadth()
    mcclellan()
    print("cited: Asness, Moskowitz and Pedersen (2013) value and momentum premia in 8 markets and asset classes")
    print("cited: De Bondt and Thaler (1985) 36-month formation and 36-month holding periods")
    print("cited: Bernard and Thomas (1989) drift over the 60 trading days after the announcement")
    print("cited: Moskowitz, Ooi and Pedersen (2012) 58 instruments; O'Neil RS rating 80 or higher on a 1 to 99 scale")
    print("cited: conventions, 52-week highs and lows, 200-day SMA, 52-week Mansfield lookback")
    print("cited: IBD RS rating, the 40% / 20% / 20% / 20% quarterly weighting quoted online is a third-party approximation")
    print("cited: Jegadeesh and Titman (1993) 3- to 12-month formation and holding periods; long top 10%, short bottom 10%")
    print("input: high-beta pitfall, a 2.0 beta stock against a 1.0 beta index")
    print("cited: Zweig breadth thrust = 10-day average of advances / (advances + declines) from below 40% to above 61.5%")
    print("all momentum and breadth numbers check out")
