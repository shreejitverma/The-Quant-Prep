"""ETF and index-futures market making: basket fair value, arbitrage bands, carry and hedge ratios.

Backs every number in ``08-ETF-and-Futures-Market-Making.md``.
Run ``uv run --no-project --with numpy python 08-Market-Making/code/etf_futures_mm.py``;
each printed number is asserted, so drift in the note fails CI.

All prices, fees, rates and volatilities are hypothetical inputs chosen for the examples.
The only market constant is the E-mini S&P 500 multiplier of 50 dollars per index point (CME contract specification).
"""

from __future__ import annotations

import math

import numpy as np

ES_MULTIPLIER = 50.0  # dollars per index point, CME E-mini S&P 500
CU_SHARES = 50_000  # hypothetical creation unit

# hypothetical basket per creation unit: (shares, bid, ask)
BASKET = {
    "AAA": (10_000, 149.99, 150.01),
    "BBB": (25_000, 79.99, 80.01),
    "CCC": (40_000, 44.99, 45.01),
    "DDD": (5_000, 409.95, 410.05),
}
CASH_COMPONENT = 12_500.0


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<64s} {value:16.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


def basket_value(side: str) -> float:
    """Dollar value of one creation unit's basket at bid, mid or ask, including the cash component."""
    total = CASH_COMPONENT
    for n, bid, ask in BASKET.values():
        price = {"bid": bid, "ask": ask, "mid": (bid + ask) / 2}[side]
        total += n * price
    return total


# ---------------------------------------------------------------- 1. NAV and the arbitrage band


def section_nav_and_band() -> None:
    """Backs Example 1 and cards mm-etf-nav-formula, mm-etf-band-numeric."""
    print("\n1. basket fair value and the creation / redemption band")
    mid = check("basket mid value per creation unit", basket_value("mid"), 7_362_500.0, 1e-6)
    nav = check("NAV per ETF share (mid)", mid / CU_SHARES, 147.25, 1e-9)
    bid_v = basket_value("bid") / CU_SHARES
    ask_v = basket_value("ask") / CU_SHARES
    check("basket bid value per ETF share", bid_v, 147.2300, 5e-5)
    check("basket ask value per ETF share", ask_v, 147.2700, 5e-5)
    check("basket half-spread in bp of NAV", (ask_v - nav) / nav * 1e4, 1.3582, 5e-5)
    # AP costs: fixed fee per creation or redemption order plus 2 bp impact on the basket trade
    fee, impact_bp = 500.0, 2.0
    upper = ask_v * (1 + impact_bp / 1e4) + fee / CU_SHARES
    lower = bid_v * (1 - impact_bp / 1e4) - fee / CU_SHARES
    check("creation bound: ETF bid above this -> create", upper, 147.3095, 5e-5)
    check("redemption bound: ETF ask below this -> redeem", lower, 147.1906, 5e-5)
    check("creation bound premium in bp over NAV", (upper - nav) / nav * 1e4, 4.0376, 5e-5)
    check("redemption bound discount in bp under NAV", (nav - lower) / nav * 1e4, 4.0371, 5e-5)
    # an ETF bid of 147.35 is above the band: profit per creation unit from creating and selling
    etf_bid = 147.35
    profit = etf_bid * CU_SHARES - (basket_value("ask") * (1 + impact_bp / 1e4) + fee)
    check("AP profit per CU at ETF bid 147.35", profit, 2027.30, 0.005)
    # independent check: same profit from the per-share band
    assert abs(profit - (etf_bid - upper) * CU_SHARES) < 1e-6


def section_stale_nav() -> None:
    """Backs Example 2 and cards mm-etf-closed-market-fv, mm-etf-premium-not-arb."""
    print("\n2. fair value of a Japan ETF in US hours (underlying market closed)")
    nav_close_usd, fut_ret, beta, usdjpy_close, usdjpy_now = 40.00, 0.012, 1.0, 150.00, 151.50
    fv_calc = nav_close_usd * (1 + beta * fut_ret) * usdjpy_close / usdjpy_now
    fv = check("fair value = NAV x (1 + beta r_fut) x FX_close / FX_now", fv_calc, 40.0792, 5e-5)
    check("move vs stale NAV in percent", (fv / nav_close_usd - 1) * 100, 0.1980, 5e-5)
    check("FX effect alone in percent", (usdjpy_close / usdjpy_now - 1) * 100, -0.9901, 5e-5)
    etf_px = 40.30
    check("apparent premium to stale NAV in bp", (etf_px / nav_close_usd - 1) * 1e4, 75.0, 1e-9)
    check("premium to fair value in bp", (etf_px / fv - 1) * 1e4, 55.0889, 5e-4)


# ---------------------------------------------------------------- 3. futures fair value and carry


def section_futures_fair_value() -> None:
    """Backs Example 3 and cards mm-futures-fv-discrete-div, mm-futures-rate-sensitivity, mm-futures-implied-repo."""
    print("\n3. index futures fair value with discrete dividends")
    s, r, t = 6000.0, 0.04, 0.25
    divs = [(0.10, 18.0), (0.20, 12.0)]
    pv_div = sum(d * math.exp(-r * ti) for ti, d in divs)
    check("PV of dividends (index points)", pv_div, 29.8325, 5e-5)
    f = check("fair futures F = (S - PV(D)) e^{rT}", (s - pv_div) * math.exp(r * t), 6030.1687, 5e-5)
    check("fair basis F - S", f - s, 30.1687, 5e-5)
    # cross-check: carry identity F = S e^{rT} - FV(D)
    fv_div = sum(d * math.exp(r * (t - ti)) for ti, d in divs)
    assert abs((s * math.exp(r * t) - fv_div) - f) < 1e-9
    check("rate sensitivity dF/dr per 1 bp = (S - PV(D)) T e^{rT} 1e-4 (pts)", f * t * 1e-4, 0.1508, 5e-5)
    # numeric derivative of F in r with the dividend PV held at the new rate too
    h = 1e-6
    f_up = (s - sum(d * math.exp(-(r + h) * ti) for ti, d in divs)) * math.exp((r + h) * t)
    check("full dF/dr per 1 bp including dividend discounting (pts)", (f_up - f) / h * 1e-4, 0.1512, 5e-5)
    # implied financing rate from a market futures price, dividends fixed
    f_mkt = 6034.00
    # solve (s - PV_r(D)) e^{r t} = f_mkt for r by bisection
    lo, hi = 0.0, 0.2
    for _ in range(200):
        mid = (lo + hi) / 2
        val = (s - sum(d * math.exp(-mid * ti) for ti, d in divs)) * math.exp(mid * t) - f_mkt
        lo, hi = (mid, hi) if val < 0 else (lo, mid)
    check("implied financing rate from F = 6034 (percent)", lo * 100, 4.2534, 5e-5)
    check("richness F_mkt - F (index points)", f_mkt - f, 3.8313, 5e-5)
    check("richness F_mkt - F in dollars per ES contract", (f_mkt - f) * ES_MULTIPLIER, 191.5673, 5e-4)
    # no-arbitrage band with different borrow and lend rates and 3 bp each-way cash trading cost
    r_lend, r_borrow, cost = 0.038, 0.044, 3e-4
    hi_bound = (s * (1 + cost) - pv_div) * math.exp(r_borrow * t)
    lo_bound = (s * (1 - cost) - pv_div) * math.exp(r_lend * t)
    check("upper no-arb bound (borrow at 4.4%, buy basket at +3 bp)", hi_bound, 6038.0217, 5e-4)
    check("lower no-arb bound (lend at 3.8%, sell basket at -3 bp)", lo_bound, 6025.3371, 5e-4)
    check("width of the no-arbitrage band (pts)", hi_bound - lo_bound, 12.6846, 5e-4)
    # calendar spread fair value with a continuous dividend yield
    q = 0.014
    t1, t2 = 0.25, 0.50
    spread = s * (math.exp((r - q) * t2) - math.exp((r - q) * t1))
    check("calendar spread F(0.5) - F(0.25) with q = 1.4%", spread, 39.3822, 5e-4)


# ---------------------------------------------------------------- 4. hedge ratios


def section_hedge() -> None:
    """Backs Example 4 and cards mm-futures-beta-one-hedge, mm-futures-sector-hedge."""
    print("\n4. hedging ETF inventory with futures")
    shares, etf_px, fut = 40_000, 585.00, 5_900.0
    v = check("ETF inventory value", shares * etf_px, 23_400_000.0, 1e-6)
    per = check("ES contract notional at F = 5900", fut * ES_MULTIPLIER, 295_000.0, 1e-9)
    n = check("beta-one hedge V / (multiplier F) contracts", v / per, 79.3220, 5e-5)
    resid = check("residual dollar delta after selling 79 contracts", v - 79 * per, 95_000.0, 1e-6)
    check("residual as percent of inventory", resid / v * 100, 0.4060, 5e-5)
    assert round(n) == 79

    # minimum-variance hedge of a sector ETF with index futures
    sig_e, sig_f, rho = 0.015, 0.011, 0.85
    h_star = rho * sig_e / sig_f
    check("min-variance hedge ratio rho sigma_E / sigma_F", h_star, 1.1591, 5e-5)
    grid = np.linspace(0.0, 2.0, 200_001)
    var = sig_e**2 - 2 * grid * rho * sig_e * sig_f + grid**2 * sig_f**2
    check("hedge ratio from a grid minimisation of variance", float(grid[np.argmin(var)]), 1.1591, 5e-5)
    resid_vol = math.sqrt(sig_e**2 * (1 - rho**2))
    check("residual daily vol sigma_E sqrt(1 - rho^2) (percent)", resid_vol * 100, 0.7902, 5e-5)
    check("variance removed rho^2 (percent)", rho**2 * 100, 72.25, 1e-9)
    check("vol removed 1 - sqrt(1 - rho^2) (percent)", (1 - math.sqrt(1 - rho**2)) * 100, 47.3217, 5e-5)
    sector_v = 10_000_000.0
    check("contracts for 10m of sector ETF", h_star * sector_v / per, 39.2912, 5e-5)
    # Monte Carlo confirmation of the residual vol (seed 5)
    rng = np.random.default_rng(5)
    z = rng.standard_normal((2, 400_000))
    re = sig_e * z[0]
    rf = sig_f * (rho * z[0] + math.sqrt(1 - rho**2) * z[1])
    beta_hat = float(np.cov(re, rf)[0, 1] / np.var(rf, ddof=1))
    check("OLS beta of ETF on futures returns (simulated, seed 5)", beta_hat, 1.1577, 5e-5)
    check("simulated residual vol (percent, seed 5)", float(np.std(re - beta_hat * rf)) * 100, 0.7904, 5e-5)


def section_create_vs_carry() -> None:
    """Backs Example 5 and card mm-etf-create-vs-carry."""
    print("\n5. short ETF inventory: carry the futures hedge or create units?")
    shares, nav = 100_000, 147.25
    borrow_fee = 0.0030  # annual stock-borrow fee on the ETF short
    value = check("short ETF value 100,000 x 147.25", shares * nav, 14_725_000.0, 1e-6)
    check("ES contracts hedging the short (value / 295,000)", value / (5_900.0 * ES_MULTIPLIER), 49.9153, 5e-5)
    daily = check("daily borrow cost of the short (act/360)", value * borrow_fee / 360, 122.7083, 5e-5)
    # create 2 CUs: fee 500 each, buy the basket at the ask plus 2 bp, unwind the futures hedge (half a tick of 0.25 on 50 contracts)
    n_cu = shares // CU_SHARES
    basket_cost = n_cu * (basket_value("ask") * 1.0002 - basket_value("mid"))
    check("basket cost over mid for 2 CUs (half-spread + 2 bp)", basket_cost, 4945.4000, 5e-4)
    fut_unwind = 50 * 0.125 * ES_MULTIPLIER
    check("futures unwind cost (50 contracts x half tick x 50)", fut_unwind, 312.5, 1e-9)
    total = check("total cost of creating", basket_cost + n_cu * 500 + fut_unwind, 6257.9000, 5e-4)
    check("break-even days of carrying instead", total / daily, 50.9982, 5e-4)


if __name__ == "__main__":
    section_nav_and_band()
    section_stale_nav()
    section_futures_fair_value()
    section_hedge()
    section_create_vs_carry()
    print("\nall checks passed")
