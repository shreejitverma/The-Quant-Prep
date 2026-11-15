"""Reverse DCF and expectations investing: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/Investing/Valuation Models/03-Reverse-DCF-and-Expectations-Investing.md`.
Independent routes used here:
- explicit present values as a year-by-year sum, checked against the closed-form growing annuity;
- the implied growth rate by bisection, checked by Newton-Raphson with a numerical derivative started
  from the linear-interpolation guess, and by recomputing EV(g*) - EV_market = 0;
- the expectations grid by bisection for each margin, checked by Newton-Raphson;
- the downside case by recomputing equity value per share from the 15% path.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_val_03_reverse_dcf.py`.
"""

from __future__ import annotations

WACC, G_TERM, YEARS, R0 = 0.09, 0.025, 7, 800.0
TAX, REINVEST = 0.25, 0.15
EV_MARKET = 120.0 * 50.0 + 400.0 - 200.0


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


def conversion(margin: float) -> float:
    return margin * (1 - TAX) * (1 - REINVEST)


def pv_explicit(g: float, margin: float = 0.25) -> float:
    c = conversion(margin)
    return sum(c * R0 * (1 + g) ** t / (1 + WACC) ** t for t in range(1, YEARS + 1))


def pv_explicit_annuity(g: float, margin: float = 0.25) -> float:
    c1 = conversion(margin) * R0 * (1 + g)
    return c1 / (WACC - g) * (1 - ((1 + g) / (1 + WACC)) ** YEARS)


def pv_terminal(g: float, margin: float = 0.25) -> float:
    r7 = R0 * (1 + g) ** YEARS
    tv = r7 * (1 + G_TERM) * conversion(margin) / (WACC - G_TERM)
    return tv / (1 + WACC) ** YEARS


def ev(g: float, margin: float = 0.25) -> float:
    return pv_explicit(g, margin) + pv_terminal(g, margin)


def bisect(margin: float) -> float:
    lo, hi = -0.5, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ev(mid, margin) < EV_MARKET else (lo, mid)
    return (lo + hi) / 2


def newton(margin: float, g0: float) -> float:
    g = g0
    for _ in range(50):
        h = 1e-6
        f = ev(g, margin) - EV_MARKET
        d = (ev(g + h, margin) - ev(g - h, margin)) / (2 * h)
        g -= f / d
    return g


def worked_case() -> None:
    print("Worked case: CyberShield reverse DCF (cards mkt-val-068, mkt-val-071, mkt-val-261)")
    approx("market cap", 120.0 * 50.0, 6000.0, 1)
    approx("EV market", EV_MARKET, 6200.0, 1)
    approx("NOPAT per dollar of revenue", 0.25 * (1 - TAX), 0.1875, 4)
    approx("FCFF per dollar of revenue", conversion(0.25), 0.159375, 6)
    for g, r7, pve, tv, pvtv, total in [
        (0.10, 1559.0, 925.9, 3918.0, 2143.3, 3069.2),
        (0.25, 3814.7, 1602.2, 9587.2, 5244.5, 6846.7),
    ]:
        tag = f"g = {100 * g:.0f}%"
        approx(f"{tag}: year 7 revenue", R0 * (1 + g) ** 7, r7, 1)
        approx(f"{tag}: PV explicit (annuity closed form)", pv_explicit_annuity(g), pve, 1)
        approx(f"{tag}: PV explicit (sum)", pv_explicit(g), pve, 1)
        approx(f"{tag}: TV at year 7", pv_terminal(g) * (1 + WACC) ** 7, tv, 1)
        approx(f"{tag}: PV of TV", pv_terminal(g), pvtv, 1)
        approx(f"{tag}: EV", ev(g), total, 1)
    approx("FCFF in year 8 at g = 10%", R0 * 1.1**7 * 1.025 * conversion(0.25), 254.67, 2)
    approx("FCFF in year 8 at g = 25%", R0 * 1.25**7 * 1.025 * conversion(0.25), 623.17, 2)
    approx("discount factor 1 / 1.09^7", 1.09**-7, 0.54703, 5)
    e10, e25 = ev(0.10), ev(0.25)
    linear = 0.10 + (EV_MARKET - e10) / (e25 - e10) * 0.15
    approx("linear interpolation guess (percent)", 100 * linear, 22.43, 2)
    g_star = bisect(0.25)
    g_newton = newton(0.25, linear)
    approx("implied growth by bisection (percent)", 100 * g_star, 23.08, 2)
    approx("implied growth by Newton-Raphson (percent)", 100 * g_newton, 23.08, 2)
    assert abs(ev(g_star) - EV_MARKET) < 1e-6
    approx("year 7 revenue at g*", R0 * (1 + g_star) ** 7, 3422.9, 1)
    approx("growth multiple of a 12% industry", g_star / 0.12, 1.92, 2)
    approx("implied return on new capital g* / reinvestment rate (percent)", 100 * g_star / REINVEST, 153.9, 1)

    # One change at a time: explicit-period reinvestment becomes g / 30% of NOPAT; terminal assumptions unchanged.
    def ev_linked(g: float, ronic: float = 0.30) -> float:
        c = 0.25 * (1 - TAX) * (1 - g / ronic)
        return sum(c * R0 * (1 + g) ** t / (1 + WACC) ** t for t in range(1, YEARS + 1)) + pv_terminal(g)

    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ev_linked(mid) < EV_MARKET else (lo, mid)
    assert abs(ev_linked(lo) - EV_MARKET) < 1e-6
    g_lin = g_star
    for _ in range(50):  # Newton-Raphson started from the headline root g*, independent of the bisection
        h = 1e-6
        g_lin -= (ev_linked(g_lin) - EV_MARKET) / ((ev_linked(g_lin + h) - ev_linked(g_lin - h)) / (2 * h))
    approx("implied growth with reinvestment g / 30% (bisection, percent)", 100 * lo, 27.51, 2)
    approx("implied growth with reinvestment g / 30% (Newton, percent)", 100 * g_lin, 27.51, 2)
    pve, pvtv = pv_explicit(0.15), pv_terminal(0.15)
    approx("g = 15%: PV explicit", pve, 1112.2, 1)
    approx("g = 15%: PV of TV", pvtv, 2925.6, 1)
    approx("g = 15%: EV", pve + pvtv, 4037.8, 1)
    eq = pve + pvtv - 400 + 200
    approx("g = 15%: equity value", eq, 3837.8, 1)
    approx("g = 15%: value per share", eq / 50, 76.76, 2)
    approx("g = 15%: downside to $120 (percent)", 100 * (1 - eq / 50 / 120), 36.0, 1)


def grid() -> None:
    print("Core concepts 4: expectations grid at $120 and 9% WACC (card mkt-val-069)")
    for margin, quoted in [(0.15, 33.19), (0.18, 29.52), (0.20, 27.43), (0.22, 25.56), (0.25, 23.08)]:
        g_b = bisect(margin)
        g_n = newton(margin, 0.25)
        approx(f"margin {100 * margin:.0f}%: implied growth by Newton (percent)", 100 * g_n, quoted, 2)
        approx(f"margin {100 * margin:.0f}%: implied growth by bisection (percent)", 100 * g_b, quoted, 2)


if __name__ == "__main__":
    worked_case()
    grid()
    print("all reverse-DCF numbers check out")
