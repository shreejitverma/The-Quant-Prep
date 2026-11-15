"""DCF first principles and cash flow forecasting: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/Investing/Valuation Models/01-DCF-First-Principles-and-Cash-Flow-Forecasting.md`.
Independent routes used here:
- the five-year forecast is built line by line in exact rational arithmetic (fractions.Fraction), and the
  explicit present value is computed twice: as a forward sum of mid-year discounted cash flows, and by
  backward induction V_t = (V_{t+1} + CF_{t+1}) / (1 + WACC) on end-of-year flows rescaled by (1 + WACC)^0.5;
- the Gordon terminal value is checked against an explicit 3,000-year sum of the growing cash flows plus
  the closed-form tail beyond it;
- the growth rate implied by an exit multiple is found by bisection on TV(g) = multiple x EBITDA and
  compared with the closed form;
- the mid-year uplift is compared with a cash flow spread evenly over the year, integrated by the trapezoid rule.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_val_01_dcf.py`.
"""

from __future__ import annotations

from fractions import Fraction as F

import numpy as np


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


WACC = 0.085
G = 0.025


def forecast() -> dict[str, list]:
    """Exact five-year forecast for Horizon Software (all inputs hypothetical)."""
    growth = [F(15, 100), F(12, 100), F(10, 100), F(8, 100), F(6, 100)]
    margin = [F(20 + i, 100) for i in range(6)]
    rev = [F(1000)]
    for x in growth:
        rev.append(rev[-1] * (1 + x))
    ebit = [r * m for r, m in zip(rev, margin, strict=True)]
    tax = [e * F(25, 100) for e in ebit]
    nopat = [e - t for e, t in zip(ebit, tax, strict=True)]
    da = [r * F(5, 100) for r in rev]
    capex = [r * F(6, 100) for r in rev]
    dowc = [F(0)] + [F(4, 100) * (rev[i] - rev[i - 1]) for i in range(1, 6)]
    fcff = [nopat[i] + da[i] - capex[i] - dowc[i] for i in range(6)]
    return {"rev": rev, "ebit": ebit, "tax": tax, "nopat": nopat, "da": da, "capex": capex, "dowc": dowc, "fcff": fcff}


def worked_case() -> None:
    print("Worked case: Horizon Software five-year DCF (cards mkt-val-010, mkt-val-257, mkt-val-258)")
    fc = forecast()
    table = {
        "rev": [1000.0, 1150.0, 1288.0, 1416.8, 1530.1, 1622.0],
        "ebit": [200.0, 241.5, 283.4, 325.9, 367.2, 405.5],
        "tax": [50.0, 60.4, 70.8, 81.5, 91.8, 101.4],
        "nopat": [150.0, 181.1, 212.5, 244.4, 275.4, 304.1],
        "da": [50.0, 57.5, 64.4, 70.8, 76.5, 81.1],
        "capex": [60.0, 69.0, 77.3, 85.0, 91.8, 97.3],
    }
    for key, quoted in table.items():
        for year, q in enumerate(quoted):
            approx(f"{key} year {year}", fc[key][year], q, 1)
    for year, q in zip(range(1, 6), [6.0, 5.5, 5.2, 4.5, 3.7], strict=True):
        approx(f"delta OWC year {year}", fc["dowc"][year], q, 1)
    for year, q in zip(range(1, 6), [163.6, 194.1, 225.1, 255.6, 284.2], strict=True):
        approx(f"FCFF year {year}", fc["fcff"][year], q, 1)
    f = [float(x) for x in fc["fcff"]]
    dfs = [(1 + WACC) ** -(t - 0.5) for t in range(1, 6)]
    for t, q in zip(range(1, 6), [0.9600, 0.8848, 0.8155, 0.7516, 0.6927], strict=True):
        approx(f"mid-year discount factor year {t}", dfs[t - 1], q, 4)
    pvs = [f[t] * dfs[t - 1] for t in range(1, 6)]
    for t, q in zip(range(1, 6), [157.1, 171.8, 183.6, 192.1, 196.9], strict=True):
        approx(f"PV of FCFF year {t}", pvs[t - 1], q, 1)
    pv_explicit = sum(pvs)
    # Independent route: backward induction on end-of-year flows, then shift every flow half a year earlier.
    v = 0.0
    for t in range(5, 0, -1):
        v = (v + f[t]) / (1 + WACC)
    approx("PV explicit by backward induction x 1.085^0.5", v * (1 + WACC) ** 0.5, 901.4, 1)
    approx("PV explicit (forward sum)", pv_explicit, 901.4, 1)

    approx("FCFF year 5 (unrounded)", f[5], 284.224, 3)
    f6 = f[5] * (1 + G)
    approx("FCFF year 6", f6, 291.33, 2)
    tv = f6 / (WACC - G)
    # Independent route: explicit sum of the growing perpetuity for 3,000 years plus its closed-form tail.
    n = 3000
    ratio = (1 + G) / (1 + WACC)
    explicit = sum(f6 * ratio ** (k - 1) / (1 + WACC) for k in range(1, n + 1))
    tail = f6 * ratio**n / (WACC - G)
    approx("TV by explicit sum", explicit + tail, 4855.5, 1)
    approx("Terminal value at year 5", tv, 4855.5, 1)
    d5 = (1 + WACC) ** -5
    approx("end-of-year-5 discount factor", d5, 0.66505, 5)
    pv_tv = tv * d5
    approx("PV of terminal value", pv_tv, 3229.1, 1)
    ev = pv_explicit + pv_tv
    approx("Enterprise value", ev, 4130.5, 1)
    approx("TV share of EV (percent)", 100 * pv_tv / ev, 78.2, 1)
    equity = ev - 300 + 100
    approx("Equity value", equity, 3930.5, 1)
    approx("Value per share", equity / 100, 39.31, 2)

    # Mid-year consistency: Gordon flows also arrive mid-year, so the whole TV moves half a year earlier.
    pv_tv_mid = pv_tv * (1 + WACC) ** 0.5
    tv_mid_sum = sum(f6 * (1 + G) ** (k - 1) / (1 + WACC) ** (k - 0.5) for k in range(1, n + 1)) + tail * (1 + WACC) ** 0.5
    approx("TV with mid-year flows by explicit sum (value at year 5)", tv_mid_sum, 5057.6, 1)
    approx("PV of TV with mid-year flows", pv_tv_mid, 3363.6, 1)
    ev_mid = pv_explicit + pv_tv_mid
    approx("EV with mid-year TV", ev_mid, 4265.0, 1)
    approx("Value per share with mid-year TV", (ev_mid - 200) / 100, 40.65, 2)
    approx("per-share gap between the two conventions", (ev_mid - ev) / 100, 1.34, 2)

    # Exit multiple cross-check.
    ebitda5 = float(fc["ebit"][5] + fc["da"][5])
    approx("EBITDA year 5", ebitda5, 486.6, 1)
    approx("exit EV/EBITDA implied by the Gordon TV", tv / ebitda5, 9.98, 2)
    target = 15 * ebitda5
    lo, hi = -0.05, WACC - 1e-9
    for _ in range(200):
        mid = (lo + hi) / 2
        if f[5] * (1 + mid) / (WACC - mid) < target:
            lo = mid
        else:
            hi = mid
    closed = (target * WACC - f[5]) / (target + f[5])
    approx("g implied by 15x EBITDA (bisection, percent)", 100 * lo, 4.43, 2)
    approx("g implied by 15x EBITDA (closed form, percent)", 100 * closed, 4.43, 2)
    approx("FCFF5 / EBITDA5 conversion", f[5] / ebitda5, 0.584, 3)


def mid_year_uplift() -> None:
    print("Core concepts 4: mid-year uplift at an 8% WACC (card mkt-val-007)")
    approx("mid-year uplift 1.08^0.5 - 1 (percent)", 100 * (1.08**0.5 - 1), 3.92, 2)
    # Independent route: a cash flow spread evenly over the year, integrated numerically (trapezoid rule
    # on 100,001 points), against the same cash lumped at year end.
    s = np.linspace(0.0, 1.0, 100_001)
    y = 1.08**-s
    continuous = float(np.sum((y[1:] + y[:-1]) / 2) * (s[1] - s[0]))
    approx("continuous-flow discount factor over year 1", continuous, 0.9625, 4)
    approx("continuous-flow uplift over year-end (percent)", 100 * (continuous * 1.08 - 1), 3.95, 2)


if __name__ == "__main__":
    worked_case()
    mid_year_uplift()
    print("all DCF first-principles numbers check out")
