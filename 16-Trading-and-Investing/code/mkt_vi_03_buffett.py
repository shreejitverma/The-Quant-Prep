"""Buffett's evolution: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Value Investing/03-Buffett-Evolution-From-Cigar-Butts-to-Quality-Compounders.md`.
Independent routes used here:
- owner earnings and naive free cash flow in exact fractions, against a line-item cash-flow build
  (operating cash flow from net income, D&A and the full working-capital change, then each capex slice);
- the float growth rate 1970-2024 by closed form, against bisection on (1 + g)^54 = 171,000 / 39;
- the cost of float from underwriting profit over average float, checked against a direct cash ledger;
- the 1990 look-through earnings sum from the letter's own components;
- the 2024 letter's 19.9% compounded gain, checked for consistency against its 5,502,284% overall gain.
Every quoted number is printed and asserted at the precision the note quotes; cited constants are labelled.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_vi_03_buffett.py
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


def berkshire_record() -> None:
    print("2024 letter: compounded annual gain 1965-2024 (cited) vs overall gain 1964-2024 (cited)")
    implied = (1 + 5_502_284 / 100) ** (1 / 60) - 1
    # The letter's 19.9% is computed from the annual returns; the overall-gain route must agree to 0.1 pp.
    close("19.9% vs rate implied by 5,502,284% over 60 years", 100 * implied, 19.9, 0.1)
    implied_spx = (1 + 39_054 / 100) ** (1 / 60) - 1
    close("10.4% vs rate implied by the S&P 500's 39,054%", 100 * implied_spx, 10.4, 0.1)


def sees() -> None:
    print("See's Candies, 2007 and 2014 letters")
    q("price / net tangible assets, 25 / 8 (x)", F(25, 8), "3.1")


def float_growth() -> None:
    print("Float: $39M in 1970 (2014 letter), $171B in 2024 (2024 letter)")
    ratio = 171_000 / 39
    closed = ratio ** (1 / 54) - 1
    root = bisect(lambda g: (1 + g) ** 54 - ratio, 0.0, 1.0)
    close("closed form vs bisection", closed, root, 1e-12)
    q("float growth rate 1970-2024 (% a year)", 100 * closed, "16.8")
    q("years 1970 to 2024", 2024 - 1970, "54")


def cost_of_float() -> None:
    print("Cost of float (hypothetical book)")
    premiums, combined, avg_float = F(100), F(96, 100), F(250)
    uw_profit = premiums * (1 - combined)
    q("underwriting profit at a 96% combined ratio ($)", uw_profit, "4")
    cost = -uw_profit / avg_float
    # ledger route: premiums in, losses and expenses out, the gap is what the insurer kept for free
    losses_and_expenses = 96
    ledger = -(100 - losses_and_expenses) / 250
    close("cost of float vs cash ledger", float(cost), ledger, 1e-12)
    q("cost of float (%)", 100 * cost, "-1.6")
    q("cost of float at a 100% combined ratio (%)", 100 * (-premiums * (1 - F(1)) / avg_float), "0.0")


def look_through_1990() -> None:
    print("1990 letter look-through earnings ($M, cited components)")
    retained, tax, reported = 250, 30, 371
    q("retained share less incremental tax", retained - tax, "220")
    total = retained - tax + reported
    q("look-through earnings", total, "591")
    close("letter's 'about $590 million'", total, 590, 5)


def owner_earnings() -> None:
    print("Consolidated Brands (hypothetical inputs, $M)")
    ni, da, capex, d_nwc = F(500), F(120), F(180), F(30)
    maint_capex, maint_nwc = F(90), F(10)
    oe = ni + da - maint_capex - maint_nwc
    q("growth capex 180 - 90", capex - maint_capex, "90")
    q("growth working capital 30 - 10", d_nwc - maint_nwc, "20")
    # line-item route: operating cash flow, then add back the growth slices the owner chose to spend
    cfo = 500.0 + 120.0 - 30.0
    q("operating cash flow NI + D&A - change in NWC", cfo, "590")
    naive_fcf = cfo - 180.0
    q("naive free cash flow CFO - total capex", naive_fcf, "410.0")
    oe_lines = naive_fcf + 90.0 + 20.0
    close("owner earnings formula vs FCF plus growth slices", float(oe), oe_lines, 1e-9)
    q("owner earnings", oe, "520.0")
    q("owner earnings above naive FCF (%)", 100 * (oe / F(410) - 1), "26.8")
    print("One-dollar test")
    q("market cap change 7,200 - 4,000", F(7200) - F(4000), "3200")
    q("market value per dollar retained 3,200 / 1,800 ($)", F(3200, 1800), "1.78")
    q("value destroyed when $100M retained adds $50M", 100 - 50, "50")
    q("market value per dollar retained, 50 / 100 ($)", F(50, 100), "0.50")
    q("market value per dollar retained, 300 / 100 ($)", F(300, 100), "3.00")


def main() -> None:
    berkshire_record()
    sees()
    float_growth()
    cost_of_float()
    look_through_1990()
    owner_earnings()
    print("all Buffett checks passed")


if __name__ == "__main__":
    main()
