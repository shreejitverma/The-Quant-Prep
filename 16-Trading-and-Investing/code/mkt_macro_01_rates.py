"""Yield curves and rates trading: every number in 04-Macro-Rates-FX/01-Yield-Curve-Dynamics-and-Rates-Trading.md.

Independent routes used here:
- the semi-annual par bootstrap is checked by solving each discount factor again by bisection on its par bond's
  price (each must price at 100 given the earlier discount factors), and f(T) > y(T) on an upward curve by
  differencing ln P numerically;
- DV01 notionals and the 2s10s flattener P&L are computed leg by leg;
- the butterfly weights are solved as a 2x2 linear system in maturity and then checked by pricing 2-, 5- and 10-year
  semi-annual par bonds, sizing the legs from analytic DV01s, and repricing the whole fly (central differences) under
  a parallel yield shift and a linear-in-maturity slope shift (both must give zero first-order P&L, and the 50/50 fly
  must lose one body-DV01 basis point per basis point per year of slope).
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_macro_01_rates.py
"""

from __future__ import annotations

import numpy as np
from mkt_assets_lib import bisect, close, q


def bootstrap_check() -> None:
    print("Bootstrap: semi-annual par discount factors in closed form vs bisection on each par bond's price")
    par = {0.5: 0.040, 1.0: 0.041, 1.5: 0.042, 2.0: 0.043, 2.5: 0.0435, 3.0: 0.044}  # hypothetical annual par coupons
    dfs: list[float] = []
    for c in par.values():
        p = (1 - c / 2 * sum(dfs)) / (1 + c / 2)
        dfs.append(p)
    solved: list[float] = []
    for i, c in enumerate(par.values()):

        def price_gap(p: float, c: float = c) -> float:
            return 100 * (c / 2 * (sum(solved) + p) + p) - 100.0

        solved.append(bisect(price_gap, 0.5, 1.0, tol=1e-14))
        close(f"discount factor {i + 1}: closed-form bootstrap vs bisection", dfs[i], solved[i], 1e-12)
    ts = np.array(list(par))
    y = -np.log(dfs) / ts
    f = -np.diff(np.log(dfs)) / np.diff(ts)
    assert np.all(np.diff(y) > 0) and np.all(f > y[1:] - 1e-12), "forwards sit above spot on an upward curve"


def dv01_trades() -> None:
    print("2s10s DV01 sizing and the flattener example")
    dv2, dv10 = 0.000190, 0.000820  # DV01 as a fraction of notional
    q("DV01 per $10,000 notional, 2-year", dv2 * 10_000, "1.90")
    q("DV01 per $10,000 notional, 10-year", dv10 * 10_000, "8.20")
    q("notional ratio 2Y / 10Y = 8.2 / 1.9", dv10 / dv2, "4.32")
    q("2-year notional against $10m of 10-year ($m)", 10 * dv10 / dv2, "43.2")
    n2, n10 = 50_000 / dv2, 50_000 / dv10
    q("2-year notional for $50,000 DV01", n2, "263,157,895")
    q("10-year notional for $50,000 DV01", n10, "60,975,610")
    q("2-year notional ($m)", n2 / 1e6, "263.16")
    q("10-year notional ($m)", n10 / 1e6, "60.98")
    pnl2 = n2 * dv2 * 25  # short 2y, yields up 25bp
    pnl10 = -n10 * dv10 * 10  # long 10y, yields up 10bp
    q("2-year leg P&L", pnl2, "1,250,000")
    q("10-year leg P&L", pnl10, "-500,000")
    q("net P&L", pnl2 + pnl10, "750,000")


def butterfly() -> None:
    print("2s5s10s butterfly weights")
    t1, tb, t2 = 2.0, 5.0, 10.0
    # wing DV01s as fractions w1, w2 of the body DV01: parallel neutral w1 + w2 = 1; linear-slope neutral w1 (t1 - tb) + w2 (t2 - tb) = 0
    w1, w2 = np.linalg.solve(np.array([[1.0, 1.0], [t1 - tb, t2 - tb]]), np.array([1.0, 0.0]))
    q("short-wing share of body DV01", w1, "0.625")
    q("long-wing share of body DV01", w2, "0.375")
    par_yield = {t1: 0.040, tb: 0.041, t2: 0.043}  # hypothetical par yields; each bond's coupon equals its yield
    bp, h = 1e-4, 1e-6  # DV01 per 1bp; the fly is repriced by central differences with a 0.01bp step

    def price(t: float, dy: float) -> float:
        c, y = par_yield[t], par_yield[t] + dy
        n = round(2 * t)
        return sum(100 * c / 2 / (1 + y / 2) ** k for k in range(1, n + 1)) + 100 / (1 + y / 2) ** n

    for t in (t1, tb, t2):
        close(f"{t:.0f}-year par bond prices at 100", price(t, 0.0), 100.0, 1e-9)

    def dv01_analytic(t: float) -> float:
        c, y, n = par_yield[t], par_yield[t], round(2 * t)
        dp_dy = -sum((k / 2) * 100 * c / 2 / (1 + y / 2) ** (k + 1) for k in range(1, n + 1)) - (n / 2) * 100 / (1 + y / 2) ** (n + 1)
        return -dp_dy * bp

    dv01 = {t: dv01_analytic(t) for t in (t1, tb, t2)}  # per 100 face, from the closed-form yield derivative

    def fly_pnl(wing1: float, wing2: float, shock) -> float:
        # long wings sized to wing1 and wing2 of the body DV01, short one unit of body; central difference in the shock size
        face = {t1: wing1 * dv01[tb] / dv01[t1], tb: -1.0, t2: wing2 * dv01[tb] / dv01[t2]}

        def book(eps: float) -> float:
            return sum(f * (price(t, eps * shock(t)) - 100.0) for t, f in face.items())

        return (book(h) - book(-h)) / 2 * bp / h / dv01[tb]  # in body-DV01 basis points per basis point of shock

    shocks = (("parallel +1bp", lambda t: 1.0), ("linear slope 1bp per year", lambda t: t - tb))
    for name, shock in shocks:
        close(f"repriced {w1:.3f}/{w2:.3f} butterfly P&L under {name}", fly_pnl(w1, w2, shock), 0.0, 1e-6)
    close("repriced 50/50 butterfly P&L under the parallel shift", fly_pnl(0.5, 0.5, shocks[0][1]), 0.0, 1e-6)
    slope_pnl_5050 = fly_pnl(0.5, 0.5, shocks[1][1])
    q("repriced 50/50 butterfly P&L under the slope shock (body-DV01 bp)", slope_pnl_5050, "-1")
    close("repriced 50/50 butterfly slope P&L vs -1 body-DV01 bp", slope_pnl_5050, -1.0, 1e-6)


if __name__ == "__main__":
    bootstrap_check()
    dv01_trades()
    butterfly()
    print("all rates numbers verified")
