"""Valuation Rebuild Drills: every number in the four worked solutions.

Backs every number in `16-Trading-and-Investing/30-Drills/Valuation-Rebuild-Drills.md`.
Independent routes used here:
- Drill 1 FCFF: a year-by-year projection loop in exact `fractions.Fraction` arithmetic, checked against
  closed-form geometric-series present values of each FCFF component (NOPAT, D&A, capex, change in NWC);
  the Gordon terminal value is checked against a direct sum of 3,000 years of growing cash flows;
- Drill 2 WACC: exact rational un-levering and re-levering (D/E = 2/3 exactly), checked in floating point;
- Drill 3 reverse DCF: the implied growth rate by bisection on the explicit 10-year cash-flow sum,
  confirmed by a secant solve on the closed-form growing-annuity value from a different bracket;
- Drill 4 NCAV: exact sums of the balance-sheet lines, checked against the stated totals.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_drill_01_valuation_rebuild.py`.
"""

from __future__ import annotations

from fractions import Fraction as F


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


# ------------------------------------------------------------------ Drill 1: FCFF bridge


def drill1() -> None:
    print("Drill 1: FCFF valuation bridge")
    r0 = F(1000)
    growth, margin, tax, nwc_pct = F(12, 100), F(25, 100), F(21, 100), F(10, 100)
    wacc, g_term = F(85, 1000), F(25, 1000)
    cash, debt, shares = F(150), F(300), F(50)
    capex1, da1, cg = F(50), F(40), F(105, 100)

    # Route A: explicit loop.
    rev_prev, nwc_prev = r0, nwc_pct * r0
    rows = []
    for t in range(1, 6):
        rev = rev_prev * (1 + growth)
        ebit = rev * margin
        nopat = ebit * (1 - tax)
        da = da1 * cg ** (t - 1)
        capex = capex1 * cg ** (t - 1)
        nwc = rev * nwc_pct
        dnwc = nwc - nwc_prev
        fcff = nopat + da - capex - dnwc
        rows.append((rev, ebit, nopat, da, capex, dnwc, fcff))
        rev_prev, nwc_prev = rev, nwc

    quoted = {
        "revenue": [1120.0, 1254.4, 1404.9, 1573.5, 1762.3],
        "ebit": [280.0, 313.6, 351.2, 393.4, 440.6],
        "nopat": [221.2, 247.7, 277.5, 310.8, 348.1],
        "da": [40.0, 42.0, 44.1, 46.3, 48.6],
        "capex": [50.0, 52.5, 55.1, 57.9, 60.8],
        "dnwc": [12.0, 13.4, 15.1, 16.9, 18.9],
        "fcff": [199.2, 223.8, 251.4, 282.3, 317.0],
    }
    for i, name in enumerate(quoted):
        for t, q in enumerate(quoted[name], 1):
            approx(f"{name} year {t}", rows[t - 1][i], q, 1)

    fcff = [row[6] for row in rows]
    quoted_fcff2 = [199.20, 223.80, 251.40, 282.33, 317.03]
    for t, q in enumerate(quoted_fcff2, 1):
        approx(f"unrounded FCFF year {t}", fcff[t - 1], q, 2)

    pv = [fcff[t - 1] / (1 + wacc) ** t for t in range(1, 6)]
    for t, q in enumerate([183.59, 190.11, 196.82, 203.73, 210.84], 1):
        approx(f"PV FCFF year {t}", pv[t - 1], q, 2)
    pv_sum = sum(pv)

    # Route B: closed-form geometric series per component.
    def geo_pv(first: F, q: F, n: int = 5) -> F:
        x = q / (1 + wacc)
        return first / (1 + wacc) * (1 - x**n) / (1 - x)

    pv_nopat = geo_pv(r0 * (1 + growth) * margin * (1 - tax), 1 + growth)
    pv_da = geo_pv(da1, cg)
    pv_capex = geo_pv(capex1, cg)
    pv_dnwc = geo_pv(nwc_pct * r0 * growth, 1 + growth)
    pv_closed = pv_nopat + pv_da - pv_capex - pv_dnwc
    assert abs(float(pv_closed - pv_sum)) < 1e-9, (float(pv_closed), float(pv_sum))
    approx("PV of discrete FCFF", pv_closed, 985.09, 2)

    fcff6 = fcff[4] * (1 + g_term)
    approx("terminal FCFF year 6", fcff6, 324.95, 2)
    tv5 = fcff6 / (wacc - g_term)
    # Independent check of the Gordon value: sum 3,000 years of growing cash flows in float.
    direct = sum(float(fcff6) * float(1 + g_term) ** k / float(1 + wacc) ** (k + 1) for k in range(3000))
    assert abs(direct - float(tv5)) < 1e-6, (direct, float(tv5))
    approx("terminal value year 5", tv5, 5415.85, 2)
    approx("1.085^5", (1 + wacc) ** 5, 1.50366, 5)
    pv_tv = tv5 / (1 + wacc) ** 5
    approx("PV of terminal value", pv_tv, 3601.78, 2)
    ev = pv_closed + pv_tv
    approx("enterprise value", ev, 4586.87, 2)
    eq = ev + cash - debt
    approx("equity value", eq, 4436.87, 2)
    approx("value per share", eq / shares, 88.74, 2)


# ------------------------------------------------------------------ Drill 2: Hamada and WACC


def drill2() -> None:
    print("Drill 2: Hamada un-levering and WACC")
    t = F(25, 100)
    peers = {"A": (F(135, 100), F(50, 100)), "B": (F(110, 100), F(20, 100)), "C": (F(155, 100), F(80, 100))}
    quoted_u = {"A": 0.9818, "B": 0.9565, "C": 0.9688}
    bu = {}
    for name, (bl, de) in peers.items():
        bu[name] = bl / (1 + (1 - t) * de)
        # float route
        flt = float(bl) / (1 + 0.75 * float(de))
        assert abs(flt - float(bu[name])) < 1e-12
        approx(f"unlevered beta {name}", bu[name], quoted_u[name], 4)
    avg = sum(bu.values()) / 3
    approx("sum of unlevered betas", sum(bu.values()), 2.9071, 4)
    approx("average unlevered beta", avg, 0.9690, 4)
    de_target = F(40, 60)
    approx("target D/E", de_target, 0.667, 3)
    factor = 1 + (1 - t) * de_target
    exact("relevering factor", factor, F(3, 2))
    bl_target = avg * factor
    approx("relevered beta", bl_target, 1.4535, 4)
    rf, erp = F(4, 100), F(55, 1000)
    ke = rf + bl_target * erp
    approx("beta x ERP (percent)", 100 * bl_target * erp, 7.994, 3)
    approx("cost of equity (percent)", 100 * ke, 11.994, 3)
    approx("cost of equity rounded (percent)", 100 * ke, 11.99, 2)
    kd_after = F(65, 1000) * (1 - t)
    approx("after-tax cost of debt (percent)", 100 * kd_after, 4.875, 3)
    approx("equity term (percent)", 100 * F(6, 10) * ke, 7.197, 3)
    approx("debt term (percent)", 100 * F(4, 10) * kd_after, 1.950, 3)
    wacc = F(6, 10) * ke + F(4, 10) * kd_after
    approx("WACC (percent)", 100 * wacc, 9.147, 3)
    approx("WACC rounded (percent)", 100 * wacc, 9.15, 2)


# ------------------------------------------------------------------ Drill 3: reverse DCF


R, G_T, REV0, N = 0.09, 0.03, 2000.0, 10


def fcf_margin() -> float:
    return 0.20 * (1 - 0.21) - 0.04


def ev_loop(g: float) -> tuple[float, float, float]:
    m = fcf_margin()
    pv_cf = sum(REV0 * (1 + g) ** t * m / (1 + R) ** t for t in range(1, N + 1))
    fcf10 = REV0 * (1 + g) ** N * m
    tv = fcf10 * (1 + G_T) / (R - G_T)
    pv_tv = tv / (1 + R) ** N
    return pv_cf + pv_tv, pv_cf, pv_tv


def ev_closed(g: float) -> float:
    m = fcf_margin()
    fcf1 = REV0 * (1 + g) * m
    x = (1 + g) / (1 + R)
    pv_cf = fcf1 / (1 + R) * (1 - x**N) / (1 - x)
    pv_tv = REV0 * (1 + g) ** N * m * (1 + G_T) / (R - G_T) / (1 + R) ** N
    return pv_cf + pv_tv


def drill3() -> None:
    print("Drill 3: reverse DCF")
    target = 120.0 * 100 + 1500 - 500
    approx("market cap ($M)", 120.0 * 100, 12000.0, 1)
    approx("enterprise value ($M)", target, 13000.0, 1)
    approx("NOPAT margin (percent)", 100 * 0.20 * (1 - 0.21), 15.80, 2)
    approx("FCF margin (percent)", 100 * fcf_margin(), 11.80, 2)
    approx("TV multiple of FCF10", (1 + G_T) / (R - G_T), 17.167, 3)
    approx("1.09^10", (1 + R) ** N, 2.3674, 4)

    ev10, pv_cf10, pv_tv10 = ev_loop(0.10)
    assert abs(ev10 - ev_closed(0.10)) < 1e-6
    approx("g=10%: year 10 revenue", REV0 * 1.1**N, 5187.0, 0)
    approx("g=10%: year 10 FCF", REV0 * 1.1**N * fcf_margin(), 612.1, 1)
    approx("g=10%: TV10", REV0 * 1.1**N * fcf_margin() * 1.03 / 0.06, 10508.0, 0)
    approx("g=10%: PV of TV", pv_tv10, 4439.0, 0)
    approx("g=10%: PV of 10-year FCF", pv_cf10, 2482.0, 0)
    approx("g=10%: EV", ev10, 6921.0, 0)

    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if ev_loop(mid)[0] < target:
            lo = mid
        else:
            hi = mid
    g_bis = 0.5 * (lo + hi)
    # secant on the closed form from a different starting pair
    a, b = 0.05, 0.30
    for _ in range(100):
        fa, fb = ev_closed(a) - target, ev_closed(b) - target
        if fb == fa:
            break
        a, b = b, b - fb * (b - a) / (fb - fa)
    assert abs(a - g_bis) < 1e-9 or abs(b - g_bis) < 1e-9, (a, b, g_bis)
    approx("implied growth (percent)", 100 * g_bis, 18.31, 2)
    approx("implied growth factor", 1 + g_bis, 1.183074, 6)
    approx("implied growth unrounded (percent)", 100 * g_bis, 18.3074, 4)
    ev_g, pv_cf_g, pv_tv_g = ev_loop(g_bis)
    approx("implied: (1+g)^10", (1 + g_bis) ** N, 5.3718, 4)
    approx("implied: year 10 revenue", REV0 * (1 + g_bis) ** N, 10744.0, 0)
    approx("implied: year 10 FCF", REV0 * (1 + g_bis) ** N * fcf_margin(), 1267.7, 1)
    approx("implied: TV10", REV0 * (1 + g_bis) ** N * fcf_margin() * 1.03 / 0.06, 21763.0, 0)
    approx("implied: PV of TV", pv_tv_g, 9193.0, 0)
    approx("implied: PV of 10-year FCF", pv_cf_g, 3807.0, 0)
    approx("implied: EV", ev_g, 13000.0, 0)
    approx("revenue expansion multiple", (1 + g_bis) ** N, 5.4, 1)


# ------------------------------------------------------------------ Drill 4: NCAV


def drill4() -> None:
    print("Drill 4: net-net NCAV")
    assets = {"cash": F(25), "ar": F(30), "raw": F(20), "fg": F(20), "ppe": F(60), "intang": F(15)}
    recovery = {"cash": F(1), "ar": F(75, 100), "raw": F(40, 100), "fg": F(70, 100), "ppe": F(0), "intang": F(0)}
    liabs = [F(22), F(18), F(10), F(12)]
    exact("total assets", sum(assets.values()), F(170))
    exact("total liabilities and claims", sum(liabs), F(62))
    ca = assets["cash"] + assets["ar"] + assets["raw"] + assets["fg"]
    exact("current assets", ca, F(95))
    ncav = ca - sum(liabs)
    exact("NCAV", ncav, F(33))
    approx("NCAV per share", ncav / 10, 3.30, 2)
    liq = sum(assets[k] * recovery[k] for k in assets)
    exact("liquidated assets", liq, F(139, 2))
    approx("liquidated assets", liq, 69.5, 1)
    net_liq = liq - sum(liabs)
    approx("net liquidation value", net_liq, 7.5, 1)
    approx("net liquidation value per share", net_liq / 10, 0.75, 2)
    approx("premium to NCAV (percent)", 100 * (F(6) / (ncav / 10) - 1), 81.8, 1)
    approx("price / liquidation value", F(6) / (net_liq / 10), 8.0, 1)
    approx("two-thirds of NCAV per share", F(2, 3) * ncav / 10, 2.20, 2)


def main() -> None:
    drill1()
    drill2()
    drill3()
    drill4()
    print("all valuation drill numbers verified")


if __name__ == "__main__":
    main()
