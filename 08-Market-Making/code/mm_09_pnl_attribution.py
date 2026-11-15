"""P&L attribution and markouts: every number in `08-Market-Making/09-Market-Making-PnL-Attribution-and-Markouts.md`.

Independent routes used here:
- the attribution buckets from an as-of lookup on the theo path (`numpy.searchsorted`, last value at or
  before the time) in exact cents, reconciled against the cash-flow P&L computed without any theo;
- clustered standard errors by a seeded simulation of bursts of fills that share one outcome, compared
  with the closed-form cluster count and with the naive per-fill formula;
- venue and options attribution arithmetic recomputed from the stated inputs.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 08-Market-Making/code/mm_09_pnl_attribution.py`.
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
    print(f"    {label} ~ {estimate:.4f} (expected {expected:.4f}, tolerance {tol:.4f})")


# theo path of Example 1, in dollars as exact fractions
THEO_T = np.array([0.0, 1.0, 5.0, 6.0, 10.0])
THEO = [F(10000, 100), F(9999, 100), F(9997, 100), F(99975, 1000), F(9996, 100)]


def theo_at(t: float) -> F:
    """Last theo at or before t, never after (the as-of join)."""
    i = int(np.searchsorted(THEO_T, t, side="right")) - 1
    assert i >= 0, t
    return THEO[i]


def example1() -> None:
    print("Example 1: attributing a short session (cards mm-pnl-attribution-identity, mm-pnl-numeric-session)")
    tau, close_t = 1.0, 60.0
    # time, side (+1 buy), size, price, passive?, fee per share (+ rebate)
    fills = [
        (0.0, +1, 100, F(9998, 100), True, F(2, 1000)),
        (5.0, -1, 50, F(9999, 100), True, F(2, 1000)),
        (10.0, -1, 50, F(9995, 100), False, F(-3, 1000)),
    ]
    rows = []
    for t, d, n, p, passive, fee in fills:
        edge = n * d * (theo_at(t) - p)
        adverse = n * d * (theo_at(t + tau) - theo_at(t))
        drift = n * d * (theo_at(close_t) - theo_at(t + tau))
        rows.append((edge, adverse, drift, n * fee, passive))
    quoted = [
        (F(2), F(-1), F(-3), F(20, 100)),
        (F(1), F(-25, 100), F(75, 100), F(10, 100)),
        (F(-50, 100), F(0), F(0), F(-15, 100)),
    ]
    for i, (row, lit) in enumerate(zip(rows, quoted, strict=True)):
        exact(f"trade {i + 1}: edge, adverse, drift, fee", row[:4], lit)
    passive_edge = sum(r[0] for r in rows if r[4])
    adverse = sum(r[1] for r in rows)
    drift = sum(r[2] for r in rows)
    hedge = sum(r[0] for r in rows if not r[4])
    fees = sum(r[3] for r in rows)
    exact("passive edge", passive_edge, F(3))
    exact("adverse selection", adverse, F(-125, 100))
    exact("inventory drift", drift, F(-225, 100))
    exact("hedge cost", hedge, F(-50, 100))
    exact("fees", fees, F(15, 100))
    total = passive_edge + adverse + drift + hedge + fees
    exact("sum of buckets", total, F(-85, 100))
    # independent route: cash flows only, no theo anywhere
    cash = sum(-d * n * p for _, d, n, p, _, _ in fills)
    exact("final position", sum(d * n for _, d, n, _, _, _ in fills), 0)
    exact("cash legs", [-d * n * p for _, d, n, p, _, _ in fills], [F(-9998), F(499950, 100), F(499750, 100)])
    exact("cash from trades", cash, F(-1))
    exact("cash plus fees", cash + fees, total)
    exact("quotes net of selection", passive_edge + adverse, F(175, 100))
    # card mm-pnl-numeric-session: the first fill alone, unhedged, marked at the close
    exact("first fill alone: edge + adverse + drift", sum(rows[0][:3]), F(-2))
    exact("first fill alone: 100 x (99.96 - 99.98)", 100 * (theo_at(close_t) - F(9998, 100)), F(-2))


def snippet() -> None:
    print("The note's float snippet (first two rows of Example 1)")
    theo_t = np.array([0.0, 1.0, 5.0, 6.0, 10.0])
    theo = np.array([100.00, 99.99, 99.97, 99.975, 99.96])

    def at(t: float) -> float:
        return float(theo[np.searchsorted(theo_t, t, side="right") - 1])

    out = [
        (round(n * d * (at(t) - p), 2), round(n * d * (at(t + 1.0) - at(t)), 2))
        for t, d, n, p in [(0.0, +1, 100, 99.98), (5.0, -1, 50, 99.99)]
    ]
    exact("printed pairs", out, [(2.0, -1.0), (1.0, -0.25)])


def example2() -> None:
    print("Example 2: venue curves net of fees (card mm-pnl-venue-net-of-fees)")
    a, b = F(-1, 10) + F(25, 100), F(-4, 10) - F(10, 100)
    exact("venue A net at 10 s", a, F(15, 100))
    exact("venue B net at 10 s", b, F(-50, 100))
    exact("venue A total (ticks)", 40_000 * a, 6000)
    exact("venue B total (ticks)", 10_000 * b, -5000)
    exact("difference per fill", a - b, F(65, 100))
    exact("fee gap (0.25 rebate against a 0.10 fee)", F(25, 100) + F(10, 100), F(35, 100))
    exact("pre-fee markout gap at 10 s", F(-1, 10) - F(-4, 10), F(3, 10))


def example3(rng: np.random.Generator) -> None:
    print("Example 3: is the venue difference real? (card mm-pnl-cluster-se)")
    sd = 4.0
    se_a, se_b = sd / math.sqrt(4000), sd / math.sqrt(1000)
    approx("SE venue A", se_a, 0.063, 3)
    approx("SE venue B", se_b, 0.126, 3)
    se_diff = math.hypot(se_a, se_b)
    approx("SE of the difference", se_diff, 0.141, 3)
    approx("net difference in SEs", 0.65 / se_diff, 4.6, 1)
    approx("pre-fee markout difference in SEs", 0.3 / se_diff, 2.1, 1)
    approx("naive SE treating 10,000 B fills as independent", sd / math.sqrt(10_000), 0.04, 2)
    approx("understatement factor", se_b / (sd / math.sqrt(10_000)), 3.16, 2)
    # simulation: 1,000 bursts of 10 fills, each burst sharing one N(0, 4^2) outcome
    reps, means, naive = 4000, [], []
    for _ in range(reps // 500):
        bursts = rng.normal(0.0, sd, size=(500, 1000))
        fills = np.repeat(bursts, 10, axis=1)
        means.append(fills.mean(axis=1))
        naive.append(fills.std(axis=1, ddof=1) / math.sqrt(fills.shape[1]))
    m = np.concatenate(means)
    true_se = float(m.std(ddof=1))
    simulated("true SE of B's mean markout", true_se, se_b, 4 * se_b / math.sqrt(2 * reps))
    simulated("average naive SE", float(np.concatenate(naive).mean()), 0.04, 0.001)


def example4() -> None:
    print("Example 4: an options day (card mm-pnl-options-edge-vega)")
    n, m, vega, gamma, theta = 100, 100, 0.19, 0.0302, 0.026
    edge = n * m * vega * 0.5
    vega_pnl = -n * m * vega * 0.8
    theta_pnl = n * m * theta
    pos_gamma = n * m * gamma
    gamma_pnl = -0.5 * pos_gamma * sum(0.60**2 for _ in range(4))
    approx("edge at fill", edge, 950, 0)
    approx("vega", vega_pnl, -1520, 0)
    approx("theta", theta_pnl, 260, 0)
    approx("position gamma", pos_gamma, 302, 0)
    approx("gamma", gamma_pnl, -217, 0)
    approx("total explained", edge + vega_pnl + theta_pnl + gamma_pnl, -527, 0)


def example5() -> None:
    print("Example 5: a stale-quote diagnosis (card mm-pnl-negative-horizon)")
    curve = {-1: F(5, 10), 0: F(1, 10), 1: F(-3, 10)}
    exact("theo move toward your price in the second before the fill", curve[-1] - curve[0], F(4, 10))


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    example1()
    snippet()
    example2()
    example3(rng)
    example4()
    example5()
    print("all P&L attribution checks passed")
