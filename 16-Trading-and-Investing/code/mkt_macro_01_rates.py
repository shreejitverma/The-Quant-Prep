"""Yield curves and rates trading: every number in 04-Macro-Rates-FX/01-Yield-Curve-Dynamics-and-Rates-Trading.md.

Independent routes used here:
- the semi-annual par bootstrap is checked by repricing every input par bond from the bootstrapped discount
  factors (each must price at exactly 100), and f(T) > y(T) on an upward curve by differencing ln P numerically;
- DV01 notionals and the 2s10s flattener P&L are computed leg by leg and compared with spread change times DV01;
- the butterfly weights are solved as a 2x2 linear system and then checked by repricing the three legs under a
  parallel shift and under a linear-in-maturity slope shift (both must give zero P&L);
- covered interest parity: the synthetic dollar borrowing rate implied by the basis-adjusted forward is computed
  from explicit cash flows (borrow EUR, sell spot, buy forward) and compared with r_d - basis.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_macro_01_rates.py
"""

from __future__ import annotations

import math

import numpy as np
from mkt_assets_lib import close, q


def bootstrap_check() -> None:
    print("Bootstrap: semi-annual par bonds reprice at 100 from the bootstrapped discount factors")
    par = {0.5: 0.040, 1.0: 0.041, 1.5: 0.042, 2.0: 0.043, 2.5: 0.0435, 3.0: 0.044}  # hypothetical annual par coupons
    dfs: list[float] = []
    for c in par.values():
        p = (1 - c / 2 * sum(dfs)) / (1 + c / 2)
        dfs.append(p)
    for i, c in enumerate(par.values()):
        price = 100 * (c / 2 * sum(dfs[: i + 1]) + dfs[i])
        close(f"par bond {i + 1} reprices at 100", price, 100.0, 1e-9)
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
    close("net P&L vs 15bp flattening x $50,000 DV01", pnl2 + pnl10, (25 - 10) * 50_000, 1e-6)


def butterfly() -> None:
    print("2s5s10s butterfly weights")
    t1, tb, t2 = 2.0, 5.0, 10.0
    # wing DV01s as fractions w1, w2 of the body DV01: parallel neutral w1 + w2 = 1; linear-slope neutral w1 (t1 - tb) + w2 (t2 - tb) = 0
    w1, w2 = np.linalg.solve(np.array([[1.0, 1.0], [t1 - tb, t2 - tb]]), np.array([1.0, 0.0]))
    q("short-wing share of body DV01", w1, "0.625")
    q("long-wing share of body DV01", w2, "0.375")
    for name, shock in (("parallel +1bp", lambda t: 1.0), ("linear slope 1bp per year", lambda t: t - 5.0)):
        pnl = -(w1 * shock(t1) + w2 * shock(t2)) + shock(tb)  # long wings, short body, in body-DV01 units
        close(f"butterfly P&L under {name}", pnl, 0.0, 1e-12)
    slope_pnl_5050 = -(0.5 * (t1 - tb) + 0.5 * (t2 - tb))
    q("50/50 butterfly P&L under the slope shock (body-DV01 bp)", slope_pnl_5050, "-1")


def cip() -> None:
    print("Covered interest parity and the basis (hypothetical rates)")
    S, rd, rf, basis, T = 1.10, 0.045, 0.025, -0.0030, 1.0  # USD per EUR; basis x < 0
    F = S * math.exp((rd - rf - basis) * T)
    # synthetic USD borrowing: borrow 1 EUR at rf, sell it spot for S USD, buy back e^{rf T} EUR forward at F
    usd_received, usd_repaid = S, math.exp(rf * T) * F
    synthetic = math.log(usd_repaid / usd_received) / T
    close("synthetic USD rate vs r_d - basis", synthetic, rd - basis, 1e-12)
    assert synthetic > rd, "a negative basis makes synthetic dollars dearer than direct dollars"


if __name__ == "__main__":
    bootstrap_check()
    dv01_trades()
    butterfly()
    cip()
    print("all rates numbers verified")
