"""Fisher scuttlebutt and qualitative growth: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Value Investing/02-Fisher-Scuttlebutt-and-Qualitative-Growth-Investing.md`.
Independent routes used here:
- MedTech ratios (hypothetical inputs) in exact fractions, against numpy float arithmetic;
- the revenue base five years ago by discounting 500 / 1.22^5, against compounding a candidate base forward
  year by year and bisecting for the one that reaches 500;
- the annual dilution rate by the closed form (50 / 49.5)^(1/5) - 1, against bisection on (1 + g)^5 = 50 / 49.5;
- the See's purchase multiple from the figures in the 2007 and 2014 Berkshire letters.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_vi_02_fisher.py
"""

from __future__ import annotations

from fractions import Fraction as F

import numpy as np


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


def compound_forward(base: float, rate: float, years: int) -> float:
    value = base
    for _ in range(years):
        value *= 1 + rate
    return value


def scuttlebutt() -> None:
    print("Scuttlebutt illustration (hypothetical)")
    q("four of five competitors agree (%)", 100 * F(4, 5), "80")
    q("supplier paid 45 - 28 days early", 45 - 28, "17")


def medtech() -> None:
    print("MedTech Diagnostics (hypothetical inputs, $M)")
    price, shares, revenue = F(65), F(50), F(500)
    mcap = price * shares
    q("market capitalization", mcap, "3250")
    op_income = F(24, 100) * revenue
    close("operating income fraction vs numpy", float(op_income), float(np.multiply(0.24, 500.0)), 1e-9)
    q("operating income", op_income, "120.0")
    q("market cap / operating income (x)", mcap / op_income, "27.1")
    q("R&D / revenue (%)", 100 * F(60) / revenue, "12.0")
    q("P/B on $500M book equity (x)", mcap / F(500), "6.5")
    discounted = 500 / 1.22**5
    forward = bisect(lambda b: compound_forward(b, 0.22, 5) - 500.0, 1.0, 500.0)
    close("discounted base vs forward-compounding bisection", discounted, forward, 1e-9)
    q("revenue five years ago at a 22% CAGR", discounted, "185.0")
    total_dilution = F(50) / F(495, 10) - 1
    q("share count growth over five years (%)", 100 * total_dilution, "1.0")
    closed = (50 / 49.5) ** (1 / 5) - 1
    root = bisect(lambda g: (1 + g) ** 5 - 50 / 49.5, 0.0, 0.1)
    close("annual dilution closed form vs bisection", closed, root, 1e-12)
    q("annual dilution (%)", 100 * closed, "0.20")


def sees() -> None:
    print("See's Candies, Berkshire letters 2007 and 2014")
    q("purchase price / net tangible assets, 25 / 8 (x)", F(25) / F(8), "3.1")


def main() -> None:
    scuttlebutt()
    medtech()
    sees()
    print("all Fisher checks passed")


if __name__ == "__main__":
    main()
