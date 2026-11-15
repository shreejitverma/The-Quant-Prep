"""Greenblatt special situations and the Magic Formula: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Value Investing/07-Greenblatt-Special-Situations-and-Magic-Formula.md`.
Independent routes used here:
- the merger-arbitrage spread and simple annualization in exact fractions;
- the compounded annual rate by closed form, against compounding the daily-equivalent rate day by day;
- the break-even closing probability by closed form, against bisection on the expected value of the trade;
- Apex's enterprise value and Magic Formula ratios in exact fractions;
- the capital-structure example: P/E from net income after interest and tax, earnings yield from EBIT and EV;
- growth of $1 at the cited rates (50% for 10 years; 30.8% and 12.4% for 17 years) by closed form
  against a year-by-year product.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_vi_07_greenblatt.py
"""

from __future__ import annotations

import math
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


def growth(rate: float, years: int) -> tuple[float, float]:
    product = 1.0
    for _ in range(years):
        product *= 1 + rate
    return (1 + rate) ** years, product


def merger_arb() -> None:
    print("BioCore merger arbitrage (hypothetical inputs)")
    offer, price, broken = F(50), F(475, 10), F(35)
    upside = offer - price
    q("upside per share ($)", upside, "2.50")
    spread = upside / price
    q("gross spread (%)", 100 * spread, "5.263")
    q("365 / 90", F(365, 90), "4.0556")
    simple = spread * F(365, 90)
    q("simple annualized return (%)", 100 * simple, "21.35")
    compounded = (1 + float(spread)) ** (365 / 90) - 1
    daily = (1 + float(spread)) ** (1 / 90)
    day_by_day = math.prod(daily for _ in range(365)) - 1
    close("compounded closed form vs day-by-day product", compounded, day_by_day, 1e-12)
    q("compounded annualized return (%)", 100 * compounded, "23.12")
    downside = price - broken
    q("downside if the deal breaks ($)", downside, "12.50")
    q("downside / upside (x)", downside / upside, "5.0")
    p_closed = downside / (upside + downside)
    p_root = bisect(lambda p: p * 2.5 - (1 - p) * 12.5, 0.0, 1.0)
    close("break-even probability closed form vs bisection", float(p_closed), p_root, 1e-12)
    q("2.50 + 12.50", upside + downside, "15.0")
    q("break-even closing probability (%)", 100 * p_closed, "83.3")
    ev = F(96, 100) * upside - F(4, 100) * downside
    q("expected gain at a 96% closing probability ($)", ev, "1.90")
    q("expected gain over 90 days (%)", 100 * ev / price, "4.00")


def magic_formula() -> None:
    print("Apex Corp (hypothetical inputs, $M)")
    mcap = F(40) * F(25)
    q("market cap 40 x 25", mcap, "1000")
    cash, debt = F(100), F(300)
    q("net debt", debt - cash, "200")
    ev = mcap + debt - cash
    q("enterprise value", ev, "1200")
    ebit = F(180)
    q("non-cash current assets 250 - 100", F(250) - cash, "150")
    nwc = F(250) - cash - F(70)
    q("net working capital", nwc, "80")
    tce = nwc + F(220)
    q("tangible capital employed", tce, "300")
    q("earnings yield EBIT / EV (%)", 100 * ebit / ev, "15.00")
    q("return on capital EBIT / TCE (%)", 100 * ebit / tce, "60.00")


def capital_structure() -> None:
    print("Same EBIT, same EV, different debt (hypothetical)")
    ebit, ev, tax = F(100), F(1000), F(25, 100)
    for debt, pe_quoted in ((F(0), "13.3"), (F(500), "9.5")):
        net_income = (ebit - debt * F(6, 100)) * (1 - tax)
        equity = ev - debt
        q(f"earnings yield with debt {float(debt):.0f} (%)", 100 * ebit / ev, "10.0")
        q(f"P/E with debt {float(debt):.0f} (x)", equity / net_income, pe_quoted)


def compounding() -> None:
    print("Growth of $1 at cited rates")
    for rate, years, quoted in ((0.50, 10, "57.67"), (0.308, 17, "96.01"), (0.124, 17, "7.30")):
        closed, product = growth(rate, years)
        close(f"closed form vs product at {rate:.1%} for {years} years", closed, product, 1e-9)
        q(f"$1 at {rate:.1%} for {years} years ($)", closed, quoted)
    q("years 1988 to 2004 inclusive", 2004 - 1988 + 1, "17")


def main() -> None:
    merger_arb()
    magic_formula()
    capital_structure()
    compounding()
    print("all Greenblatt checks passed")


if __name__ == "__main__":
    main()
