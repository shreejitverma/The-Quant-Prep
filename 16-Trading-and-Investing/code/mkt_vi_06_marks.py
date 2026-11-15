"""Howard Marks and the credit cycle: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Value Investing/06-Marks-Second-Level-Thinking-and-Market-Cycles.md`.
Independent routes used here:
- spread, expected default loss and net spread in exact fractions;
- the expected loss checked against a seeded simulation of one-year defaults on a large bond portfolio,
  with the tolerance set at five computed standard errors;
- the break-even default rate by closed form spread / (1 - recovery), against bisection on net spread = 0.
All market inputs are hypothetical; every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_vi_06_marks.py
"""

from __future__ import annotations

import math
from fractions import Fraction as F

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


def bisect(f, lo: float, hi: float, iters: int = 200) -> float:
    """Root of an increasing function f on [lo, hi]."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def credit_case() -> None:
    print("High-yield case study (hypothetical inputs, %)")
    hy, tsy = F(65, 10), F(365, 100)
    spread = hy - tsy
    q("spread 6.5 - 3.65 (%)", spread, "2.85")
    q("spread (bps)", 100 * spread, "285")
    pd, recovery = F(35, 1000), F(40, 100)
    loss = pd * (1 - recovery)
    q("expected default loss 3.5% x (1 - 0.40) (%)", 100 * loss, "2.10")
    rng = np.random.default_rng(SEED)
    n_bonds, n_years = 2_000, 500
    defaults = rng.random((n_years, n_bonds)) < float(pd)
    yearly_loss = defaults.mean(axis=1) * (1 - float(recovery))
    se = yearly_loss.std(ddof=1) / math.sqrt(n_years)
    close("simulated loss vs closed form (5 SE)", 100 * yearly_loss.mean(), 100 * float(loss), 5 * 100 * se)
    net = spread - 100 * loss
    q("net expected spread (%)", net, "0.75")
    q("net expected spread (bps)", 100 * net, "75")
    closed = float(spread) / (1 - float(recovery))
    root = bisect(lambda d: d * (1 - float(recovery)) - float(spread), 0.0, 100.0)
    close("break-even default rate closed form vs bisection", closed, root, 1e-12)
    q("break-even default rate (%)", closed, "4.75")


def main() -> None:
    credit_case()
    print("all Marks checks passed")


if __name__ == "__main__":
    main()
