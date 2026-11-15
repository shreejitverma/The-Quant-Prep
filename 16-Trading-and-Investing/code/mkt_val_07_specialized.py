"""Specialized valuation (banks, cyclicals, loss-makers, biotech): every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Valuation Models/07-Specialized-Valuation-Financials-Cyclicals-and-Loss-Makers.md`.
Independent routes used here:
- justified P/TBV against a year-by-year clean-surplus simulation (earn ROTCE on tangible book, retain
  g of it, pay the rest, discount 3,000 years plus the tail);
- cumulative probabilities of approval from the BIO 2011-2020 phase transition rates by exact products
  and by a seeded simulation of 2,000,000 candidates, with a four-standard-error tolerance;
- the mid-cycle enterprise value against a year-by-year steady-state simulation in which reinvestment
  earns RONIC = g / RR from the following year, and the growth-destroys-value claim by changing g alone.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_val_07_specialized.py`.
"""

from __future__ import annotations

import numpy as np


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


def simulated_pb(roe: float, ke: float, g: float, years: int = 3000) -> float:
    book, value = 1.0, 0.0
    for k in range(1, years + 1):
        earnings = roe * book
        value += (earnings - g * book) / (1 + ke) ** k
        book *= 1 + g
    return value + (roe - g) * book / (ke - g) / (1 + ke) ** years


def simulated_ev(nopat1: float, rr: float, ronic: float, wacc: float, years: int = 3000) -> float:
    nopat, value = nopat1, 0.0
    for k in range(1, years + 1):
        invest = rr * nopat
        value += (nopat - invest) / (1 + wacc) ** k
        nopat += ronic * invest
    g = rr * ronic
    return value + nopat * (1 - rr) / (wacc - g) / (1 + wacc) ** years


def bank() -> None:
    print("Core concepts 2 and worked case part 1: P/TBV and First Metro Bank (card mkt-val-195)")
    for rotce, quoted in [(0.15, 1.71), (0.10, 1.00), (0.08, 0.71)]:
        approx(f"justified P/TBV at ROTCE {100 * rotce:.0f}%, Ke 10%, g 3% (simulated)", simulated_pb(rotce, 0.10, 0.03), quoted, 2)
        approx(f"justified P/TBV at ROTCE {100 * rotce:.0f}% (closed form)", (rotce - 0.03) / (0.10 - 0.03), quoted, 2)
    approx("TBV per share", 10_000 / 500, 20.00, 2)
    pb = (0.14 - 0.03) / (0.10 - 0.03)
    approx("First Metro justified P/TBV (simulated)", simulated_pb(0.14, 0.10, 0.03), 1.571, 3)
    approx("First Metro justified P/TBV (closed form)", pb, 1.571, 3)
    approx("First Metro justified P/TBV (four decimals)", pb, 1.5714, 4)
    approx("intrinsic value per share", 20 * pb, 31.43, 2)
    approx("market P/TBV at $22", 22 / 20, 1.10, 2)
    approx("discount of $22 to intrinsic (percent)", 100 * (1 - 22 / (20 * pb)), 30.0, 1)
    approx("Basel minimum CET1 plus conservation buffer (percent)", 4.5 + 2.5, 7.0, 1)


def rule_of_40() -> None:
    print("Core concepts 4: Rule of 40 examples")
    approx("60% growth, -15% FCF margin", 60 - 15, 45, 0)
    approx("15% growth, 10% FCF margin", 15 + 10, 25, 0)


def biotech() -> None:
    print("Core concepts 5: BIO 2011-2020 transition rates (cards mkt-val-211, mkt-val-212, mkt-val-264)")
    p = {"I->II": 0.520, "II->III": 0.289, "III->NDA": 0.578, "NDA->approval": 0.906}
    from_nda = p["NDA->approval"]
    from_iii = p["III->NDA"] * from_nda
    from_ii = p["II->III"] * from_iii
    from_i = p["I->II"] * from_ii
    approx("LOA from NDA/BLA filing (percent)", 100 * from_nda, 90.6, 1)
    approx("LOA from Phase III (percent)", 100 * from_iii, 52.4, 1)
    approx("LOA from Phase II (percent)", 100 * from_ii, 15.1, 1)
    approx("LOA from Phase I (percent)", 100 * from_i, 7.9, 1)
    approx("LOA from Phase II relative to Phase I", from_ii / from_i, 1.92, 2)
    approx("LOA from Phase II relative to Phase III", from_ii / from_iii, 0.289, 3)
    rng = np.random.default_rng(20261114)
    n = 2_000_000
    alive = np.ones(n, dtype=bool)
    for rate in p.values():
        alive &= rng.random(n) < rate
    sim = alive.mean()
    se = np.sqrt(from_i * (1 - from_i) / n)
    print(f"    simulated LOA from Phase I = {100 * sim:.3f}% (standard error {100 * se:.3f}%, seed 20261114)")
    assert abs(sim - from_i) < 4 * se
    approx("simulated LOA from Phase I (percent)", 100 * sim, 7.9, 1)


def vulcan() -> None:
    print("Worked case part 2: Vulcan Mining mid-cycle value (cards mkt-val-202, mkt-val-265)")
    mcap = 35.0 * 200
    approx("market cap", mcap, 7000, 0)
    approx("maximum net income at reported EBIT", 1200 * 0.75, 900, 0)
    approx("minimum reported P/E", mcap / 900, 7.8, 1)
    rev, cost, sga = 500 * 3.80, 500 * 2.20, 150.0
    approx("mid-cycle revenue", rev, 1900, 0)
    approx("site operating costs", cost, 1100, 0)
    ebit = rev - cost - sga
    approx("mid-cycle EBIT", ebit, 650, 0)
    nopat = ebit * 0.75
    approx("mid-cycle NOPAT", nopat, 487.5, 1)
    approx("reinvestment (capex in excess of D&A)", 0.25 * nopat, 121.9, 1)
    fcff = nopat * 0.75
    approx("mid-cycle FCFF", fcff, 365.625, 3)
    ev_closed = fcff / (0.09 - 0.02)
    # NOPAT here is the next-year figure the Gordon formula uses; RONIC = g / RR = 8%.
    ev_sim = simulated_ev(nopat, 0.25, 0.02 / 0.25, 0.09)
    approx("EV (simulated steady state)", ev_sim, 5223.2, 1)
    approx("EV (Gordon)", ev_closed, 5223.2, 1)
    approx("equity value", ev_closed - 500, 4723.2, 1)
    per_share = (ev_closed - 500) / 200
    approx("normalized value per share", per_share, 23.62, 2)
    approx("overvaluation at $35 (percent)", 100 * (35 / per_share - 1), 48.2, 1)
    approx("implied RONIC g / RR (percent)", 100 * 0.02 / 0.25, 8.0, 1)
    # Change one thing: growth to zero with RONIC held at 8% (so reinvestment is zero).
    ev_zero = simulated_ev(nopat, 0.0, 0.08, 0.09)
    approx("EV with zero growth (simulated)", ev_zero, 5416.7, 1)
    approx("EV with zero growth (NOPAT / WACC)", nopat / 0.09, 5416.7, 1)
    approx("value per share with zero growth", (nopat / 0.09 - 500) / 200, 24.58, 2)
    approx("per-share cost of the assumed growth", (nopat / 0.09 - ev_closed) / 200, 0.97, 2)


if __name__ == "__main__":
    bank()
    rule_of_40()
    biotech()
    vulcan()
    print("all specialized-valuation numbers check out")
