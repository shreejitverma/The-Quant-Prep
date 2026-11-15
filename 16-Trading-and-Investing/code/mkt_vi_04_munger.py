"""Munger's latticework: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Value Investing/04-Munger-Latticework-Mental-Models-and-Inversion.md`.
Independent routes used here:
- annual interest, coverage and the 150 bp rate shock in exact fractions;
- the projected revenue growth rate by closed form 3^(1/4) - 1, against bisection on compounding $100M forward;
- Berkshire's four major declines (2017 letter) recomputed from the published highs and lows, against the
  percentages printed in the letter.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_vi_04_munger.py
"""

from __future__ import annotations

from fractions import Fraction as F


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


def acquisition() -> None:
    print("Apex Corp acquisition of DataTrack (hypothetical inputs, $M)")
    debt, price, cash_flow = F(800), F(1200), F(70)
    q("debt share of the price (%)", 100 * debt / price, "66.7")
    interest = debt * F(8, 100)
    q("interest at 8%", interest, "64")
    q("interest coverage 70 / 64 (x)", cash_flow / interest, "1.09")
    shock = debt * F(150, 10_000)
    q("extra interest from +150 bp", shock, "12")
    shocked = interest + shock
    q("interest after the shock", shocked, "76")
    q("coverage after the shock 70 / 76 (x)", cash_flow / shocked, "0.92")
    assert cash_flow - shocked < 0, "cash flow after interest should be negative"
    closed = 3 ** (1 / 4) - 1
    root = bisect(lambda g: 100 * (1 + g) ** 4 - 300, 0.0, 1.0)
    close("growth closed form vs bisection", closed, root, 1e-12)
    q("revenue growth 100 -> 300 over 4 years (% a year)", 100 * closed, "31.6")


def berkshire_declines() -> None:
    print("Berkshire's four major declines (2017 letter: high, low, printed percentage)")
    table = (
        ("March 1973-January 1975", 93, 38, "-59.1"),
        ("10/2/87-10/27/87", 4_250, 2_675, "-37.1"),
        ("6/19/98-3/10/2000", 80_900, 41_300, "-48.9"),
        ("9/19/08-3/5/09", 147_000, 72_400, "-50.7"),
    )
    for period, high, low, quoted in table:
        q(f"decline {period} (%)", 100 * (F(low, high) - 1), quoted)


def main() -> None:
    acquisition()
    berkshire_declines()
    print("all Munger checks passed")


if __name__ == "__main__":
    main()
