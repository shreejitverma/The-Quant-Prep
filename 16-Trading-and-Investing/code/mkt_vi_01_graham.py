"""Graham foundations: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Value Investing/01-Graham-Foundations-Margin-of-Safety-and-Mr-Market.md`.
Independent routes used here:
- margin-of-safety outcomes in exact fractions, against a log-return route (exp(ln V - ln P) - 1);
- the Graham Number by closed form sqrt(22.5 x EPS x BVPS), against a bisection for the highest price
  whose P/E x P/B product still passes the 22.5 rule;
- balance sheet totals and ratios in exact fractions, against numpy float sums and divisions;
- net-net exit returns by closed form 1.5^(1/n) - 1, against bisection on (1 + r)^n = 1.5.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_vi_01_graham.py
"""

from __future__ import annotations

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


def margin_of_safety() -> None:
    print("Margin of safety: buy at $60 against a $100 appraisal (hypothetical)")
    price = F(60)
    q("discount to appraisal (%)", 100 * (1 - price / 100), "40")
    for value, quoted in ((100, "67"), (80, "33"), (60, "0")):
        exact = 100 * (F(value) / price - 1)
        logroute = 100 * (math.exp(math.log(value) - math.log(60)) - 1)
        close(f"fraction vs log route at value {value}", float(exact), logroute, 1e-9)
        q(f"gain if true value is ${value} (%)", exact, quoted)
    q("appraisal optimism 100 -> 80 (%)", 100 * (1 - F(80, 100)), "20")
    q("Graham ch. 20 annual margin 9% - 4% (pp)", F(9) - F(4), "5")


def graham_number() -> None:
    print("Defensive criterion 7 and the Graham Number")
    q("15 x 1.5", F(15) * F(3, 2), "22.5")
    eps, bvps = 1.10, 13.00
    closed = math.sqrt(22.5 * eps * bvps)
    passes = bisect(lambda p: (p / eps) * (p / bvps) - 22.5, 0.0, 100.0)
    close("sqrt closed form vs bisection on the product rule", closed, passes, 1e-9)
    q("22.5 x 1.10 x 13.00", F(225, 10) * F(11, 10) * F(13), "321.75")
    q("Graham Number ($)", closed, "17.94")
    mos = (closed - 12.0) / closed
    mos_rounded_inputs = (17.94 - 12.00) / 17.94
    close("margin of safety, exact vs rounded Graham Number", mos, mos_rounded_inputs, 5e-4)
    q("margin of safety to Graham Number (%)", 100 * mos, "33.1")


def pioneer() -> None:
    print("Pioneer Manufacturing (hypothetical inputs, $M)")
    cash, ar, inv, ppe = F(45), F(35), F(40), F(50)
    cl, ltd, shares = F(25), F(15), F(10)
    ca = cash + ar + inv
    close("current assets fraction vs numpy", float(ca), float(np.sum([45.0, 35.0, 40.0])), 1e-12)
    q("total current assets", ca, "120.0")
    q("total assets", ca + ppe, "170.0")
    tl = cl + ltd
    q("total liabilities", tl, "40.0")
    equity = ca + ppe - tl
    q("shareholders' equity", equity, "130.0")
    q("BVPS ($)", equity / shares, "13.00")
    q("market capitalization", F(12) * shares, "120.0")
    q("current ratio (x)", ca / cl, "4.8")
    close("current ratio fraction vs float", float(ca / cl), np.float64(120.0) / np.float64(25.0), 1e-12)
    q("net working capital", ca - cl, "95.0")
    assert ltd <= ca - cl, "debt test fails"
    pe = F(12) / F(11, 10)
    pb = F(12) / F(13)
    q("P/E on 3-year average EPS (x)", pe, "10.91")
    q("P/B (x)", pb, "0.923")
    q("P/E x P/B, unrounded", pe * pb, "10.07")
    q("P/E x P/B from the rounded factors 10.91 x 0.923", 10.91 * 0.923, "10.07")
    ncav = ca - tl
    q("NCAV", ncav, "80.0")
    q("NCAV per share ($)", ncav / shares, "8.00")
    q("two-thirds of NCAV per share ($)", F(2, 3) * ncav / shares, "5.33")
    q("dividend yield 0.48 / 12 (%)", 100 * F(48, 100) / 12, "4.0")
    q("net cash 45 - 15", cash - ltd, "30.0")


def net_net_exit() -> None:
    print("Net-net exit arithmetic")
    gain = 1 / F(2, 3) - 1
    q("gain from 2/3 of NCAV to full NCAV (%)", 100 * gain, "50")
    for years, quoted in ((2, "22.47"), (3, "14.47")):
        closed = 1.5 ** (1 / years) - 1
        root = bisect(lambda r, n=years: (1 + r) ** n - 1.5, 0.0, 1.0)
        close(f"closed form vs bisection over {years} years", closed, root, 1e-12)
        q(f"annual return if NCAV is reached in {years} years (%)", 100 * closed, quoted)


def main() -> None:
    margin_of_safety()
    graham_number()
    pioneer()
    net_net_exit()
    print("all Graham checks passed")


if __name__ == "__main__":
    main()
