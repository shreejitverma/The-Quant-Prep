"""The Greeks: every number in 05-The-Greeks.md.

Closed-form Greeks are computed here and each one is confirmed by central finite differences of the
Black-Scholes price from pricing_core (an independent route: only prices are differentiated).
The Black-Scholes PDE is checked with the finite-difference Greeks, the P&L explain is compared with full revaluation,
and the peaks of gamma and vega in spot are located by a grid search.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_01_07_greeks.py
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price, norm_cdf, norm_pdf


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:64s} {value:14.8f}  quoted {quoted}")
    assert abs(value - float(quoted)) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:58s} |diff| = {abs(a - b):.2e} (tol {tol:.0e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def greeks(S: float, K: float, tau: float, r: float, sigma: float, q_: float = 0.0, call: bool = True) -> dict[str, float]:
    """Closed-form Black-Scholes Greeks (per unit of each input; theta per year in calendar time)."""
    sd = sigma * math.sqrt(tau)
    d1 = (math.log(S / K) + (r - q_ + 0.5 * sigma**2) * tau) / sd
    d2 = d1 - sd
    dq, dr, pdf = math.exp(-q_ * tau), math.exp(-r * tau), norm_pdf(d1)
    vega = S * dq * pdf * math.sqrt(tau)
    if call:
        delta = dq * norm_cdf(d1)
        theta = -S * dq * pdf * sigma / (2 * math.sqrt(tau)) - r * K * dr * norm_cdf(d2) + q_ * S * dq * norm_cdf(d1)
        rho = K * tau * dr * norm_cdf(d2)
    else:
        delta = -dq * norm_cdf(-d1)
        theta = -S * dq * pdf * sigma / (2 * math.sqrt(tau)) + r * K * dr * norm_cdf(-d2) - q_ * S * dq * norm_cdf(-d1)
        rho = -K * tau * dr * norm_cdf(-d2)
    return {
        "price": bs_price(S, K, tau, r, sigma, q_, call),
        "delta": delta,
        "gamma": dq * pdf / (S * sd),
        "vega": vega,
        "theta": theta,
        "rho": rho,
        "vanna": -dq * pdf * d2 / sigma,
        "volga": vega * d1 * d2 / sigma,
        "d1": d1,
        "d2": d2,
    }


def fd_greeks(S: float, K: float, tau: float, r: float, sigma: float, call: bool = True) -> dict[str, float]:
    """Central finite differences of the price only."""

    def v(s=S, t=tau, rr=r, sg=sigma):
        return bs_price(s, K, t, rr, sg, 0.0, call)

    hs, hv, ht, hr = 1e-2, 1e-4, 1e-5, 1e-5
    return {
        "delta": (v(s=S + hs) - v(s=S - hs)) / (2 * hs),
        "gamma": (v(s=S + hs) - 2 * v() + v(s=S - hs)) / hs**2,
        "vega": (v(sg=sigma + hv) - v(sg=sigma - hv)) / (2 * hv),
        "theta": -(v(t=tau + ht) - v(t=tau - ht)) / (2 * ht),
        "rho": (v(rr=r + hr) - v(rr=r - hr)) / (2 * hr),
        "vanna": (v(s=S + hs, sg=sigma + hv) - v(s=S + hs, sg=sigma - hv) - v(s=S - hs, sg=sigma + hv) + v(s=S - hs, sg=sigma - hv))
        / (4 * hs * hv),
        "volga": (v(sg=sigma + 1e-3) - 2 * v() + v(sg=sigma - 1e-3)) / 1e-6,
    }


def main() -> None:
    print("Example 1: S = K = 100, T = 1, r = 5%, 20% vol")
    gc = greeks(100, 100, 1.0, 0.05, 0.2)
    gp = greeks(100, 100, 1.0, 0.05, 0.2, call=False)
    q("phi(d1) = phi(0.35)", norm_pdf(gc["d1"]), "0.3752")
    rows = [
        ("price", "10.4506", "5.5735"),
        ("delta", "0.6368", "-0.3632"),
        ("gamma", "0.01876", "0.01876"),
        ("vega", "37.52", "37.52"),
        ("theta", "-6.414", "-1.658"),
        ("rho", "53.23", "-41.89"),
        ("vanna", "-0.281", "-0.281"),
        ("volga", "9.85", "9.85"),
    ]
    for name, qc, qp in rows:
        q(f"call {name}", gc[name], qc)
        q(f"put {name}", gp[name], qp)
    tol = {"delta": 1e-7, "gamma": 1e-5, "vega": 1e-5, "theta": 1e-5, "rho": 1e-5, "vanna": 1e-4, "volga": 1e-3}
    for call, g in ((True, gc), (False, gp)):
        fd = fd_greeks(100, 100, 1.0, 0.05, 0.2, call)
        for name, t in tol.items():
            close(f"{'call' if call else 'put'} {name}: closed form vs finite difference", g[name], fd[name], t)
    q("vega per vol point", gc["vega"] / 100, "0.375")
    q("call theta per calendar day", gc["theta"] / 365, "-0.0176")
    q("put theta per calendar day", gp["theta"] / 365, "-0.0045")
    q("call rho per 1%", gc["rho"] / 100, "0.532")
    q("put rho per 1%", gp["rho"] / 100, "-0.419")
    q("vanna per vol point", gc["vanna"] / 100, "-0.0028")
    fd = fd_greeks(100, 100, 1.0, 0.05, 0.2)
    pde = fd["theta"] + 0.5 * 0.04 * 100**2 * fd["gamma"] + 0.05 * 100 * fd["delta"] - 0.05 * gc["price"]
    close("Black-Scholes PDE with finite-difference Greeks", pde, 0.0, 1e-4)
    q("PDE term 0.5 sigma^2 S^2 Gamma", 0.5 * 0.04 * 100**2 * gc["gamma"], "3.752")
    q("PDE term r S Delta", 0.05 * 100 * gc["delta"], "3.184")
    q("PDE term r V", 0.05 * gc["price"], "0.523")
    g0 = greeks(100, 100, 1.0, 0.0, 0.2)
    q("zero-rate vega (rule of thumb 40)", g0["vega"], "39.70")
    q("zero-rate gamma (rule of thumb 0.020)", g0["gamma"], "0.0198")
    q("zero-rate gamma, five decimals", g0["gamma"], "0.01985")
    q("rule-of-thumb gamma 0.4 / (100 x 0.2)", 0.4 / (100 * 0.2), "0.020")
    q("sqrt(365)", math.sqrt(365), "19")
    q("sqrt(252)", math.sqrt(252), "16")
    close("vega = sigma S^2 tau Gamma", gc["vega"], 0.2 * 100**2 * 1.0 * gc["gamma"], 1e-10)

    print("\nShapes: peaks in spot (S = K = 100 strike, T = 1, r = 5%, 20% vol)")
    grid = np.linspace(50.0, 150.0, 1_000_001)
    sd = 0.2
    d1 = (np.log(grid / 100) + (0.05 + 0.02)) / sd
    gamma_grid = np.exp(-0.5 * d1**2) / (grid * sd)  # proportional to gamma
    vega_grid = grid * np.exp(-0.5 * d1**2)  # proportional to vega
    s_gamma = q("spot of maximum gamma, K e^{-(r - q + 3 sigma^2/2) tau}", 100 * math.exp(-(0.05 + 1.5 * 0.04)), "89.58")
    close("formula vs grid search", s_gamma, float(grid[np.argmax(gamma_grid)]), 1e-3)
    s_vega = q("spot of maximum vega, where d2 = 0", 100 * math.exp(-(0.05 - 0.5 * 0.04)), "97.04")
    close("formula vs grid search", s_vega, float(grid[np.argmax(vega_grid)]), 1e-3)
    # Charm with r = q = 0: dDelta/dt = phi(d1) d2 / (2 tau). Checked by a finite difference in calendar time.
    S, K, tau = 95.0, 100.0, 0.25
    g = greeks(S, K, tau, 0.0, 0.2)
    charm = norm_pdf(g["d1"]) * g["d2"] / (2 * tau)
    charm_fd = -(greeks(S, K, tau + 1e-6, 0.0, 0.2)["delta"] - greeks(S, K, tau - 1e-6, 0.0, 0.2)["delta"]) / 2e-6
    q("charm of a 3m 100 call at spot 95, per year (OTM delta decays)", charm, "-0.40")
    q("same charm per calendar day", charm / 365, "-0.0011")
    close("charm formula vs finite difference", charm, charm_fd, 1e-6)

    print("\nExample 2: zero rates, S = K = 100, 20% vol, three months")
    g3 = greeks(100, 100, 0.25, 0.0, 0.2)
    q("gamma", g3["gamma"], "0.03984")
    q("gamma, four decimals (card)", g3["gamma"], "0.0398")
    q("theta per year", g3["theta"], "-7.97")
    q("theta per day", g3["theta"] / 365, "-0.0218")
    close("theta vs -0.5 sigma^2 S^2 Gamma", g3["theta"], -0.5 * 0.04 * 100**2 * g3["gamma"], 1e-10)
    be = q("breakeven daily move from gamma and theta", math.sqrt(2 * (-g3["theta"] / 365) / g3["gamma"]), "1.047")
    close("breakeven vs S sigma / sqrt(365)", be, 100 * 0.2 / math.sqrt(365), 1e-10)
    q("gamma P&L on a 2-dollar day", 0.5 * g3["gamma"] * 4, "0.0797")
    q("rule of thumb gamma 0.4 / (S sigma sqrt T)", 0.4 / (100 * 0.2 * 0.5), "0.040")
    q("rule of thumb theta -0.2 S sigma / sqrt T", -0.2 * 100 * 0.2 / 0.5, "-8.0")
    q("card deriv-breakeven-move: S sigma / sqrt(252)", 100 * 0.2 / math.sqrt(252), "1.26")
    q("card deriv-breakeven-move: S sigma / sqrt(365)", 100 * 0.2 / math.sqrt(365), "1.05")
    q("r - q + 3 sigma^2 / 2", 0.05 + 1.5 * 0.04, "0.11")

    print("\nExample 3 and card deriv-gamma-hedge-book: short 50 one-year ATM calls, multiplier 100, zero rates")
    n = 50 * 100
    q("book delta (shares)", -n * g0["delta"], "-2699")
    q("book gamma (per dollar)", -n * g0["gamma"], "-99.2")
    q("book vega per vol point", -n * g0["vega"] / 100, "-1985")
    q("book theta per day", -n * g0["theta"] / 365, "54.4")
    ratio = q("three-month calls needed, 50 x 0.01985 / 0.03984", 50 * g0["gamma"] / g3["gamma"], "24.9")
    assert round(ratio) == 25
    m = 25 * 100
    q("new gamma", -n * g0["gamma"] + m * g3["gamma"], "0.37")
    q("three-month call delta", g3["delta"], "0.520")
    q("new delta (shares) before the stock hedge", -n * g0["delta"] + m * g3["delta"], "-1399")
    new_vega = q("vega left per vol point", -n * g0["vega"] / 100 + m * g3["vega"] / 100, "-1487")
    q("vega left as a fraction of the original", new_vega / (-n * g0["vega"] / 100), "0.75")
    q("theta per day after the hedge", -n * g0["theta"] / 365 + m * g3["theta"] / 365, "-0.20")

    print("\nExample 4: P&L explain for the long call of Example 1 (spot 102, vol 21%, one day)")
    terms = {
        "delta": gc["delta"] * 2,
        "gamma": 0.5 * gc["gamma"] * 4,
        "vega": gc["vega"] * 0.01,
        "theta": gc["theta"] / 365,
        "vanna": gc["vanna"] * 2 * 0.01,
        "volga": 0.5 * gc["volga"] * 0.0001,
    }
    quoted = {"delta": "1.2737", "gamma": "0.0375", "vega": "0.3752", "theta": "-0.0176", "vanna": "-0.0056", "volga": "0.0005"}
    for k, v in terms.items():
        q(f"{k} term", v, quoted[k])
    explained = q("total explained", sum(terms.values()), "1.6637")
    full = q("full revaluation", bs_price(102, 100, 1 - 1 / 365, 0.05, 0.21) - gc["price"], "1.6610")
    q("unexplained", full - explained, "-0.0027")

    print("\nExample 5: dollar gamma of 100 contracts (10,000 options)")
    dg = q("dollar gamma per 1% move", gc["gamma"] * 100**2 / 100 * 10_000, "18762")
    p1 = q("P&L of a 1% move", 0.5 * dg * 1.0 * 0.01, "93.8")
    p3 = q("P&L of a 3% move", 0.5 * dg * 3.0 * 0.03, "844")
    exact_gamma_pnl = 0.5 * gc["gamma"] * (100 * 0.03) ** 2 * 10_000
    close("3% P&L vs 0.5 Gamma dS^2 per option x 10,000", p3, exact_gamma_pnl, 1e-9)
    close("3% move earns 9 times the 1% move", p3, 9 * p1, 1e-9)
    q("card deriv-dollar-gamma: 2% move on 50,000 of dollar gamma", 0.5 * 50_000 * 2 * 0.02, "1000")
    print("\nAll Greeks checks passed.")


if __name__ == "__main__":
    main()
