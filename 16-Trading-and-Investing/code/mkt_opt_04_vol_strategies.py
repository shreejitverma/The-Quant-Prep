"""Volatility trading strategies: every number in 03-Options-and-Volatility/04-Volatility-Trading-Strategies.md.

Independent routes used here:
- straddle gamma and theta come from the closed-form Greeks and are checked against central finite differences of the
  straddle price in spot and in time to expiry;
- the scalping hedge P&L is computed from the explicit trade blotter (cash flows of each whole-unit hedge) and compared
  with the leg-by-leg gamma sum 0.5 Gamma sum(dS^2);
- implied correlation is solved from the index-variance identity and checked by a seeded simulation of two correlated
  stocks whose equal-weight index volatility must come out at the quoted 24% within four standard errors;
- the variance-swap strike replication is checked by quadrature over an option strip;
- normal-approximation probabilities for the straddle implied move use the error function.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_opt_04_vol_strategies.py
"""

from __future__ import annotations

import math

import numpy as np
from mkt_assets_lib import bs_greeks, bs_price, close, norm_cdf, norm_pdf, q

SEED = 20261114


def example_1() -> None:
    print("Example 1: long 1,000 units of a 30-day ATM straddle at 16% implied, scalped over one day")
    S = K = 5000.0
    T, s, n = 30 / 365, 0.16, 1000
    c = bs_greeks(S, K, T, 0.0, 0.0, s)
    p = bs_greeks(S, K, T, 0.0, 0.0, s, call=False)
    q("d1 = 0.5 sigma sqrt(T)", c["d1"], "0.02294")
    q("phi(d1)", norm_pdf(c["d1"]), "0.39884")
    q("2 phi(d1)", 2 * norm_pdf(c["d1"]), "0.79767")
    q("S sigma sqrt(T)", S * s * math.sqrt(T), "229.35")
    g_unit = c["gamma"] + p["gamma"]
    q("straddle gamma per unit", g_unit, "0.0034779")
    g = n * g_unit
    q("position gamma", g, "3.4779")
    h = 0.5
    fd_gamma = (
        bs_price(S + h, K, T, 0, 0, s)
        + bs_price(S + h, K, T, 0, 0, s, False)
        - 2 * (bs_price(S, K, T, 0, 0, s) + bs_price(S, K, T, 0, 0, s, False))
    ) / h**2
    fd_gamma += (bs_price(S - h, K, T, 0, 0, s) + bs_price(S - h, K, T, 0, 0, s, False)) / h**2
    close("straddle gamma vs finite difference", g_unit, fd_gamma, 1e-8)
    theta_day = n * (c["theta"] + p["theta"]) / 365
    q("position theta per day (closed form)", theta_day, "-3,049.15")
    ht = 1e-6

    def straddle(T_: float) -> float:
        return bs_price(S, K, T_, 0, 0, s) + bs_price(S, K, T_, 0, 0, s, False)

    fd_theta_day = -n * (straddle(T + ht) - straddle(T - ht)) / (2 * ht) / 365
    close("position theta per day vs finite difference of the straddle price in T", theta_day, fd_theta_day, 1e-4)
    q("theta with gamma rounded to 3.478 first", -0.5 * 3.478 * S * S * s * s / 365, "-3,049.21")
    q("entry delta 1000 x (2N(d1) - 1)", n * (2 * norm_cdf(c["d1"]) - 1), "18.3")

    path = [5050.0, 4960.0, 5060.0]
    prev_hedge, cash, trades = 0, 0.0, []
    for spot in path:
        option_delta = g * (spot - S)
        target = -round(option_delta)
        trade = target - prev_hedge  # positive = buy
        cash -= trade * spot
        trades.append(trade)
        prev_hedge = target
    q("delta at 5050", g * 50, "173.9")
    q("delta at 4960", g * -40, "-139.1")
    q("delta at 5060", g * 60, "208.7")
    assert trades == [-174, 313, -348], trades
    assert prev_hedge == -209
    q("sell 174 at 5050", 174 * 5050, "878,700")
    q("buy 313 at 4960", 313 * 4960, "1,552,480")
    q("sell 348 at 5060", 348 * 5060, "1,760,880")
    q("short 209 marked at 5060", 209 * 5060, "1,057,540")
    q("hedge cash", cash, "1,087,100")
    hedge_pnl = cash + prev_hedge * path[-1]
    q("hedge P&L after marking the short 209 at 5060", hedge_pnl, "29,560")
    convexity = 0.5 * g * 60**2
    q("option convexity on the net move", convexity, "6,260.29")
    gross = hedge_pnl + convexity
    q("gross gamma gains", gross, "35,820.29")
    moves = np.diff([S, *path])
    leg = 0.5 * g * float(np.sum(moves**2))
    q("sum of squared moves", float(np.sum(moves**2)), "20,600")
    q("leg-by-leg gamma sum", leg, "35,822.75")
    q("rounding gap leg sum minus blotter", leg - gross, "2.46")
    net = gross - 120.0 + theta_day
    q("net session P&L", net, "32,651.14")
    q("realized vol of the hedged path (%)", 100 * math.sqrt(20_600 * 365) / 5000, "54.8")
    q("breakeven daily move at 16% implied", S * s * math.sqrt(1 / 365), "41.87")
    q("gross gamma gains / theta paid", gross / -theta_day, "11.7")


def example_2() -> None:
    print("Example 2: implied correlation of a two-stock equal-weight index")
    w, s1, s2, si = 0.5, 0.30, 0.30, 0.24
    q("index variance", si * si, "0.0576")
    q("w^2 sigma^2 per stock", w * w * s1 * s1, "0.0225")
    q("2 w1 w2 sigma1 sigma2", 2 * w * w * s1 * s2, "0.0450")
    rho = (si * si - w * w * (s1 * s1 + s2 * s2)) / (2 * w * w * s1 * s2)
    q("implied correlation", rho, "0.28")
    q("0.0576 - 0.0450", si * si - 0.0450, "0.0126")
    rng = np.random.default_rng(SEED)
    m = 400_000
    z1 = rng.standard_normal(m)
    z2 = rho * z1 + math.sqrt(1 - rho * rho) * rng.standard_normal(m)
    index = w * s1 * z1 + w * s2 * z2
    est = float(index.std())
    se = si / math.sqrt(2 * m)  # standard error of a sample standard deviation
    print(f"  simulated index vol = {est:.5f}, standard error = {se:.5f}")
    assert abs(est - si) <= 4 * se, est


def implied_move_and_vrp() -> None:
    print("Straddle implied move and normal-approximation probabilities")
    k = math.sqrt(2 / math.pi)
    q("straddle / one-sd move = sqrt(2/pi)", k, "0.80")
    q("one-sd move / straddle", 1 / k, "1.25")
    q("P(|move| < straddle) under a normal model (%)", 100 * (2 * norm_cdf(k) - 1), "57.5")
    q("P(|move| < one sd) under a normal model (%)", 100 * (2 * norm_cdf(1.0) - 1), "68.3")


def variance_swap_strip() -> None:
    print("Variance-swap strike from a strip of OTM options (zero rates, flat 25% vol, 90 days)")
    F, T, s = 100.0, 0.25, 0.25
    kp = np.linspace(0.1, F, 4001)
    kc = np.linspace(F, 2000.0, 8001)
    puts = np.array([bs_price(F, k, T, 0.0, 0.0, s, call=False) for k in kp])
    calls = np.array([bs_price(F, k, T, 0.0, 0.0, s) for k in kc])
    kvar = 2.0 / T * float(np.trapezoid(puts / kp**2, kp) + np.trapezoid(calls / kc**2, kc))
    close("strip-replicated K_var vs sigma^2", kvar, s * s, 1e-4)


if __name__ == "__main__":
    example_1()
    example_2()
    implied_move_and_vrp()
    variance_swap_strip()
    print("all volatility-strategy numbers verified")
