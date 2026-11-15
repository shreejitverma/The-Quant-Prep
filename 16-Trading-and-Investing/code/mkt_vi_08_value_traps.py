"""Modern value masters, capital cycles and value traps: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Value Investing/08-Modern-Value-Masters-Capital-Cycles-and-Value-Traps.md`.
Independent routes used here:
- PackCorp multiples, yields and payout (hypothetical inputs) in exact fractions, against numpy floats;
- the capex growth rate by closed form, against bisection on (1 + g)^4 = 290 / 100;
- the leverage-trap condition by exact arithmetic on a stated EBIT and interest bill;
- Nomad's 921.1% (2013 annual letter) recomputed by compounding the letter's own calendar-year returns,
  and its 20.8% annual rate recomputed from the $10.21 value of a dollar over the exact inception-to-date span;
- the Superinvestors (1984) S&P 500 figures: 887.2% overall against 8.4% a year over 28.25 years.
Every quoted number is printed and asserted at the precision the note quotes; cited constants are labelled.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_vi_08_value_traps.py
"""

from __future__ import annotations

import datetime as dt
import math
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


def packcorp() -> None:
    print("PackCorp (hypothetical inputs)")
    price, mcap = F(18), F(1800)
    shares = mcap / price
    q("shares (M)", shares, "100")
    q("trailing P/E 18 / 2.50 (x)", price / F(25, 10), "7.2")
    pb = price / F(2118, 100)
    close("P/B fraction vs numpy", float(pb), float(np.divide(18.0, 21.18)), 1e-12)
    q("P/B 18 / 21.18 (x)", pb, "0.85")
    q("dividend yield 1.00 / 18 (%)", 100 * F(1) / price, "5.6")
    q("FCF yield 220 / 1,800 (%)", 100 * F(220) / mcap, "12.2")
    closed = (290 / 100) ** (1 / 4) - 1
    root = bisect(lambda g: 100 * (1 + g) ** 4 - 290, 0.0, 1.0)
    close("capex growth closed form vs bisection", closed, root, 1e-12)
    q("capex growth Year 1 to Year 5 (% a year)", 100 * closed, "30.5")
    q("normalized P/E 18 / 0.80 (x)", price / F(8, 10), "22.5")
    q("payout at normalized EPS 1.00 / 0.80 (%)", 100 * F(1) / F(8, 10), "125")
    q("payout after a 50% cut 0.50 / 0.80 (%)", 100 * F(1, 2) / F(8, 10), "62.5")


def leverage_trap() -> None:
    print("Leverage trap (hypothetical)")
    ebit, interest = F(100), F(85)
    q("interest share of EBIT (%)", 100 * interest / ebit, "85")
    q("pre-tax income before the drop", ebit - interest, "15")
    q("pre-tax income after a 15% EBIT drop", ebit * F(85, 100) - interest, "0")


def nomad() -> None:
    print("Nomad Investment Partnership, 2013 annual letter (cited, before fees)")
    calendar = {
        2001: 10.1, 2002: 1.3, 2003: 79.6, 2004: 22.1, 2005: 9.2, 2006: 13.6, 2007: 21.2,
        2008: -45.3, 2009: 71.5, 2010: 43.9, 2011: -9.9, 2012: 39.8, 2013: 62.2,
    }  # fmt: skip
    msci = {
        2001: 3.6, 2002: -19.9, 2003: 33.1, 2004: 14.7, 2005: 9.5, 2006: 20.1, 2007: 9.0,
        2008: -40.7, 2009: 30.0, 2010: 11.8, 2011: -5.5, 2012: 15.8, 2013: 26.7,
    }  # fmt: skip
    nomad_growth = math.prod(1 + r / 100 for r in calendar.values())
    msci_growth = math.prod(1 + r / 100 for r in msci.values())
    # The letter's calendar-year table and its cumulative table are separately rounded and not exactly
    # consistent (compounding the years gives 10.14 against 10.21); require agreement within 1%, which
    # still catches a transposed or mistyped cumulative figure.
    close("compounded calendar years vs 921.1% cumulative", nomad_growth, 1 + 921.1 / 100, 0.01 * 10.211)
    close("compounded MSCI years vs 116.9% cumulative", msci_growth, 1 + 116.9 / 100, 0.01 * 2.169)
    years = (dt.date(2013, 12, 31) - dt.date(2001, 9, 10)).days / 365.25
    q("annual rate before fees (%)", 100 * ((1 + 921.1 / 100) ** (1 / years) - 1), "20.8")
    q("MSCI World annual rate (%)", 100 * ((1 + 116.9 / 100) ** (1 / years) - 1), "6.5")


def superinvestors() -> None:
    print("Superinvestors of Graham-and-Doddsville (1984): S&P 500 over Schloss's 28.25 years (cited)")
    implied = (1 + 887.2 / 100) ** (1 / 28.25) - 1
    q("S&P 500 annual rate implied by 887.2% (%)", 100 * implied, "8.4")


def main() -> None:
    packcorp()
    leverage_trap()
    nomad()
    superinvestors()
    print("all value-trap checks passed")


if __name__ == "__main__":
    main()
