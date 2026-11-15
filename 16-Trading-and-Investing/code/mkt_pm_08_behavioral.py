"""Behavioral portfolio management: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Portfolio-Management/08-Behavioral-Portfolio-Management-and-Decision-Rules.md`.
Independent routes used here:
- the gain that offsets a $10,000 loss under the Tversky-Kahneman (1992) value function by bisection on
  v(G) = lambda v(10,000), against the closed form lambda^(1/alpha) x 10,000;
- the value of a 50/50 gamble relative to its certain equivalent by direct evaluation of v, against 0.5 x 2^alpha;
- the probability weight w(0.5) for gains from the Tversky-Kahneman weighting function, against its symmetric
  simplification at p = 0.5;
- Odean (1998) PGR and PLR recomputed from the published counts in exact fractions, with the two-proportion
  t-statistic recomputed from the same counts;
- Barber and Odean (2000) return gaps from the published annual returns.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_pm_08_behavioral.py
"""

from __future__ import annotations

import math
from fractions import Fraction

ALPHA = 0.88
LAMBDA = 2.25
GAMMA = 0.61


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


def value(x: float) -> float:
    return x**ALPHA if x >= 0 else -LAMBDA * (-x) ** ALPHA


def prospect_theory() -> None:
    print("Tversky and Kahneman (1992) median parameters: alpha = beta = 0.88, lambda = 2.25, gamma = 0.61")
    q("linear loss-aversion equivalent of a $10,000 loss ($)", LAMBDA * 10_000, "22500")
    target = -value(-10_000.0)
    lo, hi = 10_000.0, 100_000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if value(mid) < target:
            lo = mid
        else:
            hi = mid
    closed = LAMBDA ** (1 / ALPHA) * 10_000
    close("bisection vs lambda^(1/alpha) x 10,000", 0.5 * (lo + hi), closed, 1e-6)
    q("gain that offsets a $10,000 loss with curvature ($)", closed, "25131")
    ratio_gain = 0.5 * value(10_000.0) / value(5_000.0)
    close("direct evaluation vs 0.5 x 2^alpha", ratio_gain, 0.5 * 2**ALPHA, 1e-12)
    q("value of 50% chance at $10,000 relative to a sure $5,000", ratio_gain, "0.920")
    ratio_loss = 0.5 * value(-10_000.0) / value(-5_000.0)
    q("disvalue of 50% chance of -$10,000 relative to a sure -$5,000", ratio_loss, "0.920")
    p = 0.5
    w = p**GAMMA / (p**GAMMA + (1 - p) ** GAMMA) ** (1 / GAMMA)
    close("w(0.5) via the symmetric form 0.5^g / (2 x 0.5^g)^(1/g)", w, 0.5**GAMMA / (2 * 0.5**GAMMA) ** (1 / GAMMA), 1e-15)
    q("decision weight w(0.5) for gains", w, "0.421")
    p = 0.01
    q("decision weight w(0.01) for gains", p**GAMMA / (p**GAMMA + (1 - p) ** GAMMA) ** (1 / GAMMA), "0.055")


def odean() -> None:
    print("Odean (1998), Table I counts, 10,000 accounts, 1987-1993")
    counts = {
        "entire year": (13_883, 79_658, 11_930, 110_348),
        "December": (866, 7_131, 1_555, 10_604),
    }
    rg, pg, rl, pl = counts["entire year"]
    drg, dpg, drl, dpl = counts["December"]
    counts["January-November"] = (rg - drg, pg - dpg, rl - drl, pl - dpl)
    lits = {"entire year": ("0.148", "0.098"), "December": ("0.108", "0.128"), "January-November": ("0.152", "0.094")}
    for name, (a, b, c, d) in counts.items():
        pgr, plr = Fraction(a, a + b), Fraction(c, c + d)
        q(f"PGR, {name}", pgr, lits[name][0])
        q(f"PLR, {name}", plr, lits[name][1])
    pgr, plr = rg / (rg + pg), rl / (rl + pl)
    se = math.sqrt(pgr * (1 - pgr) / (rg + pg) + plr * (1 - plr) / (rl + pl))
    t = (pgr - plr) / se
    assert t > 35, t
    print(f"  two-proportion t-statistic for the entire year = {t:.1f} (paper: greater than 35)")
    q("winners sold minus paper losers, next 252 days (%)", 100 * (0.0235 - (-0.0106)), "3.41")


def barber_odean() -> None:
    print("Barber and Odean (2000): 66,465 households, 1991-1996")
    q("most active quintile vs market (pp a year)", 11.4 - 17.9, "-6.5")


def main() -> None:
    prospect_theory()
    odean()
    barber_odean()
    print("all behavioral checks passed")


if __name__ == "__main__":
    main()
