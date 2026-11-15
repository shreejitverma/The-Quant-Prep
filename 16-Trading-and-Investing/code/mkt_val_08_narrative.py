"""Narrative and numbers: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/Investing/Valuation Models/08-Narrative-and-Numbers-Valuation-Synthesis.md`.
Independent routes used here:
- each ten-year CAGR in closed form and by bisection on 200 (1 + g)^10 = target revenue;
- the explicit ten-year free cash flows summed forward and, separately, valued by backward induction;
- the terminal value against a 3,000-year explicit sum of the growing perpetuity plus its tail;
- operating margins from the filing figures (Apple FY2024 and Lockheed Martin 2024 Form 10-K), computed
  in exact fractions.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_val_08_narrative.py`.
"""

from __future__ import annotations

from fractions import Fraction as F


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


R0, WACC, G, TAX = 200.0, 0.105, 0.025, 0.25


def cagr_bisect(target: float) -> float:
    lo, hi = 0.0, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if R0 * (1 + mid) ** 10 < target else (lo, mid)
    return lo


def drivers() -> None:
    print("Worked case steps 1-3: AeroVolt narratives (cards mkt-val-229, mkt-val-231)")
    approx("market cap", 45.0 * 100, 4500, 0)
    approx("operating loss at -20%", R0 * -0.20, -40, 0)
    approx("30% of a $50B market ($B)", 0.30 * 50, 15, 0)
    approx("10% of a $50B market ($B)", 0.10 * 50, 5, 0)
    for target, quoted in [(15_000.0, 54.0), (5_000.0, 38.0)]:
        approx(f"CAGR to {target:,.0f} (closed form, percent)", 100 * ((target / R0) ** 0.1 - 1), quoted, 1)
        approx(f"CAGR to {target:,.0f} (bisection, percent)", 100 * cagr_bisect(target), quoted, 1)
    approx("disciplined CAGR (two decimals, percent)", 100 * ((5000 / R0) ** 0.1 - 1), 37.97, 2)
    approx("year 10 EBIT, story", 15_000 * 0.35, 5250, 0)
    approx("year 10 EBIT, disciplined", 5_000 * 0.18, 900, 0)
    approx("reinvestment, story (sales-to-capital 3.0)", (15_000 - R0) / 3.0, 4933, 0)
    approx("reinvestment, disciplined (sales-to-capital 1.5)", (5_000 - R0) / 1.5, 3200, 0)


def explicit_flows() -> list[float]:
    g = (5000 / R0) ** 0.1 - 1
    rev = [R0 * (1 + g) ** t for t in range(11)]
    flows = []
    for t in range(1, 11):
        ebit = rev[t] * (-0.20 + 0.038 * t)
        tax = TAX * max(ebit, 0.0)
        reinvest = (rev[t] - rev[t - 1]) / 1.5
        flows.append(ebit - tax - reinvest)
    return flows


def valuation() -> None:
    print("Worked case step 4: disciplined valuation (card mkt-val-266)")
    nopat10 = 900 * (1 - TAX)
    approx("year 10 NOPAT", nopat10, 675.0, 1)
    rr = G / 0.15
    approx("terminal reinvestment rate (percent)", 100 * rr, 16.67, 2)
    f11 = nopat10 * (1 + G) * (1 - rr)
    approx("year 11 FCFF", f11, 576.6, 1)
    tv = f11 / (WACC - G)
    n = 3000
    explicit = sum(f11 * (1 + G) ** (k - 1) / (1 + WACC) ** k for k in range(1, n + 1))
    tail = f11 * (1 + G) ** n / (WACC - G) / (1 + WACC) ** n
    approx("TV by explicit sum", explicit + tail, 7207.0, 1)
    approx("TV at year 10", tv, 7207.0, 1)
    df10 = (1 + WACC) ** -10
    approx("discount factor 1 / 1.105^10", df10, 0.36845, 5)
    pv_tv = tv * df10
    approx("PV of TV", pv_tv, 2655.4, 1)
    approx("margin step per year (points)", 100 * (0.18 - -0.20) / 10, 3.8, 1)
    flows = explicit_flows()
    approx("year 1 FCFF", flows[0], -95.3, 1)
    approx("year 10 FCFF", flows[-1], -242.4, 1)
    approx("first year with positive EBIT", next(t for t in range(1, 11) if -0.20 + 0.038 * t > 0), 6, 0)
    pv_fwd = sum(f / (1 + WACC) ** t for t, f in enumerate(flows, start=1))
    v = 0.0
    for f in reversed(flows):
        v = (v + f) / (1 + WACC)
    approx("PV of explicit FCFF (backward induction)", v, -1094.5, 1)
    approx("PV of explicit FCFF (forward sum)", pv_fwd, -1094.5, 1)
    ev = pv_tv + pv_fwd
    approx("enterprise value", ev, 1560.9, 1)
    approx("equity value", ev + 300, 1860.9, 1)
    approx("value per share", (ev + 300) / 100, 18.61, 2)
    approx("downside from $45 (percent)", 100 * (1 - (ev + 300) / 100 / 45), 58.6, 1)


def filings() -> None:
    print("Step 2: operating margins from Form 10-K filings")
    approx("Apple FY2024 operating margin (percent)", 100 * F(123_216, 391_035), 31.5, 1)
    approx("Lockheed Martin 2024 operating margin (percent)", 100 * F(7_013, 71_043), 9.9, 1)


if __name__ == "__main__":
    drivers()
    valuation()
    filings()
    print("all narrative-and-numbers figures check out")
