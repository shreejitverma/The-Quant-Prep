"""Greeks, hedging and P&L attribution: every number in 03-Options-and-Volatility/01-Greeks-Hedging-and-Pnl-Attribution.md.

Independent routes used here:
- the closed-form call price is checked against direct quadrature of the discounted payoff (no normal CDF);
- every closed-form Greek (delta, gamma, vega, theta, vanna, volga, charm) is checked against central finite
  differences of the price alone;
- the Taylor P&L attribution of Example 2 is compared with full Black-Scholes revaluation, and the third-order
  zomma term is computed by finite differences;
- the discrete-hedging claim (hedging-error standard deviation scales with the square root of the rebalancing
  interval) is checked by a seeded simulation that changes only the number of rebalances;
- the strike that maximises vega is located by grid search and compared with the d1 = 0 strike.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_opt_01_greeks_pnl.py
"""

from __future__ import annotations

import math

import numpy as np
from mkt_assets_lib import bs_greeks, bs_price, bs_price_quad, close, norm_cdf, norm_pdf, q

SEED = 20261114


def fd_greeks(S: float, K: float, T: float, r: float, q_: float, s: float) -> dict[str, float]:
    """Central finite differences of the closed-form call price only."""

    def v(S_=S, T_=T, s_=s):
        return bs_price(S_, K, T_, r, q_, s_)

    hs, hv, ht = 0.5, 1e-4, 1e-6
    return {
        "delta": (v(S_=S + hs) - v(S_=S - hs)) / (2 * hs),
        "gamma": (v(S_=S + hs) - 2 * v() + v(S_=S - hs)) / hs**2,
        "vega": (v(s_=s + hv) - v(s_=s - hv)) / (2 * hv),
        "theta": -(v(T_=T + ht) - v(T_=T - ht)) / (2 * ht),
        "vanna": (v(S + hs, T, s + hv) - v(S + hs, T, s - hv) - v(S - hs, T, s + hv) + v(S - hs, T, s - hv)) / (4 * hs * hv),
        "volga": (v(s_=s + 1e-3) - 2 * v() + v(s_=s - 1e-3)) / 1e-6,
        "charm": -((v(S + hs, T + ht, s) - v(S - hs, T + ht, s)) - (v(S + hs, T - ht, s) - v(S - hs, T - ht, s))) / (4 * hs * ht),
    }


def example_1() -> dict[str, float]:
    print("Example 1: 30-day ATM index call, S = K = 5000, sigma 20%, r 4%, q 1.5%")
    S = K = 5000.0
    T, s, r, q_ = 30 / 365, 0.20, 0.04, 0.015
    sq = math.sqrt(T)
    q("T = 30 / 365", T, "0.08219")
    q("sqrt(T)", sq, "0.28669")
    q("r - q + sigma^2 / 2", r - q_ + 0.5 * s * s, "0.045")
    q("(r - q + sigma^2 / 2) T", (r - q_ + 0.5 * s * s) * T, "0.0036986")
    q("sigma sqrt(T)", s * sq, "0.057338")
    g = bs_greeks(S, K, T, r, q_, s)
    q("d1", g["d1"], "0.0645")
    q("d1, six decimals", g["d1"], "0.064505")
    q("d2", g["d2"], "0.007167")
    q("d2 from d1 rounded to 0.0645 first", 0.0645 - 0.057338, "0.00716")
    q("N(d1)", norm_cdf(g["d1"]), "0.5257")
    q("phi(d1)", norm_pdf(g["d1"]), "0.39811")
    q("1 / sqrt(2 pi)", 1 / math.sqrt(2 * math.pi), "0.39894")
    q("move as a share of spot (%)", 100 * 50 / 5000, "1")
    q("exp(-d1^2 / 2)", math.exp(-0.5 * g["d1"] ** 2), "0.99792")
    q("q T", q_ * T, "0.001233")
    q("exp(-q T)", math.exp(-q_ * T), "0.99877")
    q("delta", g["delta"], "0.5251")
    q("exp(-qT) phi(d1)", math.exp(-q_ * T) * norm_pdf(g["d1"]), "0.39762")
    q("S sigma sqrt(T)", S * s * sq, "286.69")
    q("gamma", g["gamma"], "0.001387")
    q("vega per unit vol", g["vega"], "569.97")
    q("vega per vol point", g["vega"] / 100, "5.70")
    q("N(d2)", norm_cdf(g["d2"]), "0.50286")
    q("exp(-r T)", math.exp(-r * T), "0.99672")
    num = S * math.exp(-q_ * T) * norm_pdf(g["d1"]) * s
    q("decay numerator S e^{-qT} phi(d1) sigma", num, "397.62")
    q("2 sqrt(T)", 2 * sq, "0.57338")
    decay = -num / (2 * sq)
    rate = -r * K * math.exp(-r * T) * norm_cdf(g["d2"])
    div = q_ * S * math.exp(-q_ * T) * norm_cdf(g["d1"])
    q("theta decay term", decay, "-693.47")
    q("theta rate term", rate, "-100.24")
    q("theta dividend term", div, "39.38")
    q("theta per year", g["theta"], "-754.33")
    q("theta per calendar day", g["theta"] / 365, "-2.07")
    q("decay term alone per day", decay / 365, "-1.90")
    close("closed-form theta = sum of the three terms", g["theta"], decay + rate + div, 1e-9)
    close("closed-form price vs payoff quadrature", bs_price(S, K, T, r, q_, s), bs_price_quad(S, K, T, r, q_, s), 1e-6)
    fd = fd_greeks(S, K, T, r, q_, s)
    tol = {"delta": 1e-7, "gamma": 1e-7, "vega": 1e-5, "theta": 1e-3, "vanna": 1e-5, "volga": 1e-2, "charm": 1e-2}
    for name, t in tol.items():
        close(f"{name}: closed form vs finite difference of the price", g[name], fd[name], t)
    return g


def example_2(g: dict[str, float]) -> None:
    print("Example 2: short 10,000 index units of the call, delta-hedged; S +50, vol -1 point, one day")
    S = K = 5000.0
    T, s, r, q_ = 30 / 365, 0.20, 0.04, 0.015
    n, dS, dv, dt = 10_000, 50.0, -0.01, 1 / 365
    q("per-unit delta, five decimals", g["delta"], "0.52507")
    q("per-unit gamma, five significant figures", g["gamma"], "0.0013869")
    q("per-unit theta per day, five decimals", g["theta"] / 365, "-2.06666")
    q("per-unit vega per vol point, five decimals", g["vega"] / 100, "5.69974")
    q("hedge units, two decimals", n * g["delta"], "5,250.68")
    q("position delta before the hedge", -n * g["delta"], "-5,251")
    q("position gamma, three decimals", -n * g["gamma"], "-13.869")
    q("position gamma", -n * g["gamma"], "-13.87")
    gamma_pnl = -n * 0.5 * g["gamma"] * dS**2
    theta_pnl = -n * g["theta"] * dt
    vega_pnl = -n * g["vega"] * dv
    vanna_pnl = -n * g["vanna"] * dS * dv
    volga_pnl = -n * 0.5 * g["volga"] * dv**2
    q("gamma P&L", gamma_pnl, "-17,337")
    q("position theta per day", -n * g["theta"] / 365, "20,667")
    q("theta P&L", theta_pnl, "20,667")
    q("position vega per vol point", -n * g["vega"] / 100, "-56,997")
    q("vega P&L", vega_pnl, "56,997")
    q("vanna P&L", vanna_pnl, "-71")
    q("volga P&L", volga_pnl, "-0.66")
    q("gamma + theta + vega", gamma_pnl + theta_pnl + vega_pnl, "60,327")
    q("six-term expansion", gamma_pnl + theta_pnl + vega_pnl + vanna_pnl + volga_pnl, "60,255")
    full = -n * (bs_price(S + dS, K, T - dt, r, q_, s + dv) - bs_price(S, K, T, r, q_, s)) + n * g["delta"] * dS
    q("full revaluation P&L (hedge financing and dividends ignored)", full, "58,615")
    q("gap: six-term expansion minus full revaluation", gamma_pnl + theta_pnl + vega_pnl + vanna_pnl + volga_pnl - full, "1,640")

    def c(S_: float, s_: float) -> float:
        return bs_price(S_, K, T, r, q_, s_)

    h, hv = 1.0, 1e-3
    zomma = (c(S + h, s + hv) - 2 * c(S, s + hv) + c(S - h, s + hv) - c(S + h, s - hv) + 2 * c(S, s - hv) - c(S - h, s - hv)) / (
        2 * h * h * hv
    )
    q("zomma term -n x 0.5 x zomma x dS^2 x dvol", -n * 0.5 * zomma * dS**2 * dv, "-866")


def discrete_hedging() -> None:
    print("Discrete hedging: error std scales with sqrt(rebalancing interval)")
    S0 = K = 100.0
    T, s = 30 / 365, 0.20
    rng = np.random.default_rng(SEED)
    paths = 20_000

    def hedge_error_std(steps: int, z: np.ndarray) -> float:
        dt = T / steps
        S = np.full(paths, S0)
        cash = np.full(paths, bs_price(S0, K, T, 0.0, 0.0, s))  # short call premium received, zero rates
        shares = np.zeros(paths)
        for k in range(steps):
            tau = T - k * dt
            d1 = (np.log(S / K) + 0.5 * s * s * tau) / (s * math.sqrt(tau))
            target = 0.5 * (1.0 + np.vectorize(math.erf)(d1 / math.sqrt(2.0)))
            cash -= (target - shares) * S
            shares = target
            S = S * np.exp(-0.5 * s * s * dt + s * math.sqrt(dt) * z[:, k])
        value = cash + shares * S - np.maximum(S - K, 0.0)
        return float(value.std())

    z_fine = rng.standard_normal((paths, 200))
    # the coarse path uses the same Brownian path, aggregated four steps at a time
    z_coarse = z_fine.reshape(paths, 50, 4).sum(axis=2) / 2.0
    s50 = hedge_error_std(50, z_coarse)
    s200 = hedge_error_std(200, z_fine)
    ratio = s50 / s200
    print(f"  std with 50 rebalances = {s50:.4f}, with 200 = {s200:.4f}, ratio = {ratio:.3f} (theory 2)")
    assert 1.85 <= ratio <= 2.15, ratio


def sign_claims() -> None:
    print("Sign and location claims")
    S, T, r, q_, s = 100.0, 0.25, 0.0, 0.0, 0.25
    otm_put = bs_greeks(S, 85.0, T, r, q_, s, call=False)
    otm_call = bs_greeks(S, 115.0, T, r, q_, s)
    assert otm_put["vanna"] < 0 < otm_call["vanna"], "vanna sign: negative for OTM put, positive for OTM call"
    assert otm_put["volga"] > 0 and otm_call["volga"] > 0, "volga positive away from the money"
    atm = bs_greeks(S, 100.0, T, r, q_, s)
    assert abs(atm["volga"]) < 0.05 * otm_put["volga"], "volga near zero at the money"
    deep_put = bs_greeks(50.0, 100.0, 1.0, 0.05, 0.0, 0.20, call=False)
    assert deep_put["theta"] > 0, "deep ITM European put with r > 0 has positive theta"
    Sx, Tx, rx, qx, sx = 100.0, 1.0, 0.05, 0.0, 0.30
    grid = np.linspace(80.0, 140.0, 600_001)
    vegas = [bs_greeks(Sx, k, Tx, rx, qx, sx)["vega"] for k in grid[::1000]]
    k_coarse = grid[::1000][int(np.argmax(vegas))]
    fine = np.linspace(k_coarse - 0.2, k_coarse + 0.2, 40_001)
    k_star = fine[int(np.argmax([bs_greeks(Sx, k, Tx, rx, qx, sx)["vega"] for k in fine]))]
    close("vega-maximising strike vs S exp((r - q + sigma^2/2) T)", k_star, Sx * math.exp((rx - qx + 0.5 * sx * sx) * Tx), 2e-4)


if __name__ == "__main__":
    greeks = example_1()
    example_2(greeks)
    discrete_hedging()
    sign_claims()
    print("all Greeks, hedging and attribution numbers verified")
