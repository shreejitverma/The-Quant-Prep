"""Volatility surfaces and skew: every number in 03-Options-and-Volatility/02-Volatility-Surfaces-and-Skew.md.

Independent routes used here:
- forward volatility is computed twice: from total implied variances, and from variance-swap strikes obtained by
  quadrature over a strip of out-of-the-money option prices (the log-contract replication), never from the formula alone;
- the sticky-moneyness delta is computed in closed form (BSM delta plus vega times d sigma / dS) and by a central
  finite difference that reprices the put with the smile moving with spot;
- Breeden-Litzenberger is checked by differencing call prices twice in strike and comparing with the lognormal density;
- Dupire's formula is checked by recovering a known constant volatility from finite differences of call prices;
- the straddle implied-move constant is computed by quadrature of |S_T - K| against the lognormal density;
- SVI wing slopes are checked against w(k) / |k| at large |k|.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_opt_02_vol_surface.py
"""

from __future__ import annotations

import math

import numpy as np
from mkt_assets_lib import bs_greeks, bs_price, close, norm_cdf, norm_pdf, q


def var_swap_strike_by_strip(sigma: float, T: float, F: float = 100.0) -> float:
    """K_var = (2 / T) * [int_0^F P(K) / K^2 dK + int_F^inf C(K) / K^2 dK] at zero rates, by quadrature."""
    ks_put = np.linspace(F * 1e-3, F, 200_001)
    ks_call = np.linspace(F, F * 20.0, 400_001)
    puts = np.array([bs_price(F, k, T, 0.0, 0.0, sigma, call=False) for k in ks_put[::50]])
    calls = np.array([bs_price(F, k, T, 0.0, 0.0, sigma) for k in ks_call[::50]])
    integral = np.trapezoid(puts / ks_put[::50] ** 2, ks_put[::50]) + np.trapezoid(calls / ks_call[::50] ** 2, ks_call[::50])
    return 2.0 / T * float(integral)


def example_1() -> None:
    print("Example 1: forward volatility between day 30 and day 90")
    T1, T2, s1, s2 = 30 / 365, 90 / 365, 0.18, 0.22
    q("T1", T1, "0.08219")
    q("T2", T2, "0.24658")
    w1, w2 = s1 * s1 * T1, s2 * s2 * T2
    q("w1", w1, "0.002663")
    q("w2", w2, "0.011934")
    q("w2 - w1", w2 - w1, "0.009271")
    q("T2 - T1", T2 - T1, "0.16438")
    fwd_var = (w2 - w1) / (T2 - T1)
    q("forward variance", fwd_var, "0.05640")
    q("forward volatility (%)", 100 * math.sqrt(fwd_var), "23.75")
    k1, k2 = var_swap_strike_by_strip(s1, T1), var_swap_strike_by_strip(s2, T2)
    close("variance-swap strike by option strip vs sigma^2 (30 day)", k1, s1 * s1, 2e-5)
    close("variance-swap strike by option strip vs sigma^2 (90 day)", k2, s2 * s2, 2e-5)
    close("forward vol from strip-replicated variance swaps", math.sqrt((k2 * T2 - k1 * T1) / (T2 - T1)), math.sqrt(fwd_var), 2e-4)


def example_2() -> None:
    print("Example 2: skew-adjusted delta of a 4750 put under sticky moneyness")
    S, K, T, s0, slope = 5000.0, 4750.0, 0.10, 0.25, -1.2

    def smile(m: float) -> float:
        return s0 + slope * (m - K / S)

    q("sqrt(T)", math.sqrt(T), "0.31623")
    q("dsigma/dK per dollar", -0.012 / 50.0, "-0.00024")
    q("g' = dsigma/dK x S", -0.012 / 50.0 * S, "-1.2")
    q("ln(S/K)", math.log(S / K), "0.051293")
    q("0.5 sigma^2 T", 0.5 * s0 * s0 * T, "0.003125")
    q("sigma sqrt(T)", s0 * math.sqrt(T), "0.079057")
    g = bs_greeks(S, K, T, 0.0, 0.0, s0, call=False)
    q("d1", g["d1"], "0.6883")
    q("N(d1)", norm_cdf(g["d1"]), "0.7544")
    q("BSM put delta", g["delta"], "-0.2456")
    q("phi(d1)", norm_pdf(g["d1"]), "0.31479")
    q("vega per unit vol", g["vega"], "497.73")
    q("vega per vol point", g["vega"] / 100, "4.98")
    dsig_dS = -K / S**2 * slope
    q("dsigma/dS at fixed strike", dsig_dS, "0.000228")
    q("skew adjustment vega x dsigma/dS", g["vega"] * dsig_dS, "0.1135")
    eff = g["delta"] + g["vega"] * dsig_dS
    q("sticky-moneyness delta", eff, "-0.1321")
    h = 0.01
    fd = (
        bs_price(S + h, K, T, 0.0, 0.0, smile(K / (S + h)), call=False) - bs_price(S - h, K, T, 0.0, 0.0, smile(K / (S - h)), call=False)
    ) / (2 * h)
    q("finite-difference delta with the smile moving with spot", fd, "-0.1321")
    q("hedge per option under sticky moneyness", -eff, "0.132")
    q("hedge per option under BSM", -g["delta"], "0.246")


def density_and_local_vol() -> None:
    print("Breeden-Litzenberger and Dupire with a flat 20% surface")
    S, T, r, s = 100.0, 0.5, 0.03, 0.20
    for K in (80.0, 100.0, 120.0):
        h = 0.01
        d2c = (bs_price(S, K + h, T, r, 0.0, s) - 2 * bs_price(S, K, T, r, 0.0, s) + bs_price(S, K - h, T, r, 0.0, s)) / h**2
        mu = math.log(S) + (r - 0.5 * s * s) * T
        lognormal = math.exp(-((math.log(K) - mu) ** 2) / (2 * s * s * T)) / (K * s * math.sqrt(2 * math.pi * T))
        close(f"exp(rT) d2C/dK2 vs lognormal density at K = {K:.0f}", math.exp(r * T) * d2c, lognormal, 1e-6)
        ht = 1e-5
        dCdT = (bs_price(S, K, T + ht, r, 0.0, s) - bs_price(S, K, T - ht, r, 0.0, s)) / (2 * ht)
        dCdK = (bs_price(S, K + h, T, r, 0.0, s) - bs_price(S, K - h, T, r, 0.0, s)) / (2 * h)
        local_var = (dCdT + r * K * dCdK) / (0.5 * K * K * d2c)
        close(f"Dupire local vol recovers 20% at K = {K:.0f}", math.sqrt(local_var), s, 1e-4)


def implied_move() -> None:
    print("Straddle implied move: straddle = sqrt(2/pi) x S sigma sqrt(T) for a short-dated ATM-forward straddle")
    S, sd = 100.0, 0.05
    z = np.linspace(-12, 12, 400_001)
    st = S * np.exp(-0.5 * sd * sd + sd * z)
    straddle = float(np.trapezoid(np.abs(st - S) * np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi), z))
    ratio = straddle / (S * sd)
    q("straddle / (S sigma sqrt(T)) by quadrature", ratio, "0.80")
    q("sqrt(2 / pi)", math.sqrt(2 / math.pi), "0.7979")
    q("one-sd move / straddle = 1 / 0.7979", 1 / math.sqrt(2 / math.pi), "1.253")
    close("quadrature ratio vs sqrt(2/pi) at sigma sqrt(T) = 5%", ratio, math.sqrt(2 / math.pi), 2e-3)


def svi_wings() -> None:
    print("SVI wings are asymptotically linear with slopes b(1 + rho) and b(1 - rho)")
    a, b, rho, m, sig = 0.02, 0.4, -0.6, 0.0, 0.1

    def w(k: float) -> float:
        return a + b * (rho * (k - m) + math.sqrt((k - m) ** 2 + sig * sig))

    close("w(k) / k at k = 1e6 vs b(1 + rho)", w(1e6) / 1e6, b * (1 + rho), 1e-6)
    close("w(k) / |k| at k = -1e6 vs b(1 - rho)", w(-1e6) / 1e6, b * (1 - rho), 1e-6)
    assert b * (1 + abs(rho)) <= 2, "this parameter set respects Lee's bound"


if __name__ == "__main__":
    example_1()
    example_2()
    density_and_local_vol()
    implied_move()
    svi_wings()
    print("all volatility-surface numbers verified")
