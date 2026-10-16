"""Calculus and Taylor expansions for quants: every number quoted in note 07.

Run: uv run --no-project --with numpy python 03-Linear-Algebra-and-Optimization/code/calculus_taylor.py
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float = 5e-4) -> float:
    """Print a labelled number and assert it matches the value quoted in the notes."""
    v = float(value) + 0.0
    print(f"{label} = {int(v) if v.is_integer() and abs(v) < 1e15 else format(v, '.10g')}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs_call(s: float, k: float, t: float, r: float, vol: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
    d2 = d1 - vol * math.sqrt(t)
    return s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)


def bs_greeks(s: float, k: float, t: float, r: float, vol: float) -> dict[str, float]:
    sq = math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * sq)
    d2 = d1 - vol * sq
    gamma = norm_pdf(d1) / (s * vol * sq)
    return {
        "d1": d1,
        "d2": d2,
        "delta": norm_cdf(d1),
        "gamma": gamma,
        "speed": -gamma / s * (1.0 + d1 / (vol * sq)),
        "vega": s * norm_pdf(d1) * sq,
        "theta": -s * norm_pdf(d1) * vol / (2 * sq) - r * k * math.exp(-r * t) * norm_cdf(d2),
    }


# ---------------------------------------------------------------------------
# Delta-gamma as a second-order Taylor expansion
# ---------------------------------------------------------------------------


def delta_gamma_table() -> None:
    print("\n[07] delta-gamma versus full revaluation: S = K = 100, T = 0.5, r = 3%, vol = 20%")
    s, k, t, r, vol = 100.0, 100.0, 0.5, 0.03, 0.20
    g = bs_greeks(s, k, t, r, vol)
    c0 = bs_call(s, k, t, r, vol)
    check("call price", c0, 6.3710, 1e-4)
    check("delta", g["delta"], 0.5702, 1e-4)
    check("gamma", g["gamma"], 0.027772, 1e-6)
    check("speed (dGamma/dS)", g["speed"], -0.000625, 1e-6)
    check("vega (per 1.00 of vol)", g["vega"], 27.772, 1e-3)
    check("theta (per year)", g["theta"], -7.0738, 1e-4)
    check("vega per vol point", g["vega"] / 100, 0.2777, 1e-4)
    pde = g["theta"] + 0.5 * vol**2 * s**2 * g["gamma"] + r * s * g["delta"] - r * c0
    check("Black-Scholes PDE residual Theta + 1/2 s^2 S^2 Gamma + r S Delta - r C", pde, 0.0, 1e-10)
    check("1/2 s^2 S^2 Gamma (gamma rent per year)", 0.5 * vol**2 * s**2 * g["gamma"], 5.5544, 1e-4)
    rows = {-10.0: (-4.2667, -5.7016, -4.3130), -5.0: (-2.4940, -2.8508, -2.5036), -1.0: (-0.5562, -0.5702, -0.5563)}
    rows |= {1.0: (0.5839, 0.5702, 0.5840), 5.0: (3.1822, 2.8508, 3.1979), 10.0: (6.9479, 5.7016, 7.0902)}
    for ds, (full_want, d_want, dg_want) in rows.items():
        full = bs_call(s + ds, k, t, r, vol) - c0
        delta_only = g["delta"] * ds
        dg = delta_only + 0.5 * g["gamma"] * ds * ds
        check(f"dS = {ds:+.0f}: full revaluation", full, full_want, 1e-4)
        check(f"dS = {ds:+.0f}: delta only", delta_only, d_want, 1e-4)
        check(f"dS = {ds:+.0f}: delta-gamma", dg, dg_want, 1e-4)
    full = bs_call(s + 10, k, t, r, vol) - c0
    dgs = g["delta"] * 10 + 0.5 * g["gamma"] * 100 + g["speed"] * 1000 / 6
    check("dS = +10: adding speed dS^3/6", dgs, 6.9860, 1e-4)
    dg10 = g["delta"] * 10 + 0.5 * g["gamma"] * 100
    check("dS = +10: delta-gamma error vs full", dg10 - full, 0.1423, 1e-4)
    check("dS = +10: error left after adding speed", dgs - full, 0.038, 5e-4)
    check("dS = +10: share of the delta-gamma error removed by speed", (dg10 - dgs) / (dg10 - full), 0.73, 5e-3)
    for ds in (1.0, -1.0):
        dg1 = g["delta"] * ds + 0.5 * g["gamma"] * ds * ds
        check(f"dS = {ds:+.0f}: |delta-gamma - full| (about 1e-4)", abs(dg1 - (bs_call(s + ds, k, t, r, vol) - c0)), 1e-4, 1.5e-5)
    check("card: delta term for +5 (delta rounded to 0.5702)", round(g["delta"], 4) * 5, 2.851, 1e-12)
    check("card: gamma term for +5", 0.5 * g["gamma"] * 25, 0.3472, 1e-4)
    assert abs(full - dgs) < abs(full - (g["delta"] * 10 + 0.5 * g["gamma"] * 100))
    one_day = bs_call(s, k, t - 1 / 365, r, vol) - c0
    check("one-day theta P&L, full", one_day, -0.0194, 1e-4)
    check("one-day theta P&L, theta/365", g["theta"] / 365, -0.0194, 1e-4)
    # breakeven move: 1/2 Gamma dS^2 + Theta dt = 0
    check("one-day breakeven move |dS|", math.sqrt(-2 * g["theta"] / 365 / g["gamma"]), 1.1814, 1e-4)
    check("vol x S / sqrt(365)", vol * s / math.sqrt(365), 1.0468, 1e-4)


def quanto_cross_gamma() -> None:
    print("\n[07] cross-gamma: 1000 shares of a EUR stock held in USD, V = N S X")
    n_sh, s0, x0 = 1000.0, 50.0, 1.10
    s1, x1 = 55.0, 1.045
    ds, dx = s1 - s0, x1 - x0
    check("initial value USD", n_sh * s0 * x0, 55000.0, 1e-9)
    check("dS", ds, 5.0, 1e-12)
    check("dX", dx, -0.055, 1e-12)
    check("equity delta term N X dS", n_sh * x0 * ds, 5500.0, 1e-9)
    check("FX delta term N S dX", n_sh * s0 * dx, -2750.0, 1e-9)
    check("cross term N dS dX", n_sh * ds * dx, -275.0, 1e-9)
    check("exact P&L", n_sh * s1 * x1 - n_sh * s0 * x0, 2475.0, 1e-9)


# ---------------------------------------------------------------------------
# Duration and convexity as a Taylor expansion in yield
# ---------------------------------------------------------------------------


def bond_price(coupon: float, y: float, n: int, face: float = 100.0) -> float:
    return sum(coupon * face / (1 + y) ** t for t in range(1, n + 1)) + face / (1 + y) ** n


def duration_convexity() -> None:
    print("\n[07] 10y 5% annual bond at 5% yield")
    c, y, n = 0.05, 0.05, 10
    p0 = bond_price(c, y, n)
    cfs = [(t, c * 100 + (100 if t == n else 0)) for t in range(1, n + 1)]
    mac = sum(t * cf / (1 + y) ** t for t, cf in cfs) / p0
    mod = mac / (1 + y)
    conv = sum(t * (t + 1) * cf / (1 + y) ** (t + 2) for t, cf in cfs) / p0
    check("price", p0, 100.0, 1e-9)
    check("Macaulay duration", mac, 8.1078, 1e-4)
    check("modified duration", mod, 7.7217, 1e-4)
    check("convexity", conv, 74.9977, 1e-4)
    for dy, exact_want, dur_want, dc_want in (
        (0.01, 92.6399, 92.2783, 92.6533),
        (-0.01, 108.1109, 107.7217, 108.0967),
        (0.02, 85.9528, 84.5565, 86.0565),
    ):
        exact = bond_price(c, y + dy, n)
        dur_only = p0 * (1 - mod * dy)
        dur_conv = p0 * (1 - mod * dy + 0.5 * conv * dy * dy)
        check(f"dy = {dy * 1e4:+.0f}bp: exact", exact, exact_want, 1e-4)
        check(f"dy = {dy * 1e4:+.0f}bp: duration only", dur_only, dur_want, 1e-4)
        check(f"dy = {dy * 1e4:+.0f}bp: duration + convexity", dur_conv, dc_want, 1e-4)
    check("DV01 per 100 face", mod * p0 / 1e4, 0.077217, 1e-6)


# ---------------------------------------------------------------------------
# Limits, series and approximations
# ---------------------------------------------------------------------------


def limits_and_series() -> None:
    print("\n[07] limits, series and approximations")
    check("(1 - 1/100)^100", 0.99**100, 0.366032, 1e-6)
    check("1/e", math.exp(-1), 0.367879, 1e-6)
    check("(1 + 1/365)^365", (1 + 1 / 365) ** 365, 2.714567, 1e-6)
    check("e", math.e, 2.718282, 1e-6)
    stirling = math.sqrt(2 * math.pi * 10) * (10 / math.e) ** 10
    check("10!", math.factorial(10), 3628800, 0)
    check("Stirling sqrt(2 pi n)(n/e)^n at n = 10", stirling, 3598695.6, 0.1)
    check("Stirling ratio", stirling / math.factorial(10), 0.99170, 1e-5)
    check("Stirling shortfall", 1 - stirling / math.factorial(10), 0.0083, 1e-4)
    check("corrected Stirling overshoot", stirling * math.exp(1 / 120) - math.factorial(10), 10.05, 0.01)
    check("Stirling with 1/(12n) correction", stirling * math.exp(1 / 120), 3628810.1, 0.1)
    for x in (1e-3,):
        check("(1 - cos x)/x^2 at x = 1e-3", (1 - math.cos(x)) / x**2, 0.5, 1e-6)
        check("(e^x - 1 - x)/x^2 at x = 1e-3", (math.expm1(x) - x) / x**2, 0.500167, 1e-6)
    check("x^x at x = 1e-6", 1e-6**1e-6, 0.999986, 1e-6)
    check("100^(1/100)", 100 ** (1 / 100), 1.047129, 1e-6)
    k = np.arange(1, 200)
    check("sum k/2^k", float((k / 2.0**k).sum()), 2.0, 1e-12)
    check("sum k^2/2^k", float((k**2 / 2.0**k).sum()), 6.0, 1e-12)
    check("pi^2/6", math.pi**2 / 6, 1.644934, 1e-6)
    check("ln 2 (alternating harmonic)", math.log(2), 0.693147, 1e-6)
    h100 = sum(1 / i for i in range(1, 101))
    check("H_100", h100, 5.187378, 1e-6)
    gamma_em = 0.5772156649015329
    check("ln 100 + gamma", math.log(100) + gamma_em, 5.182386, 1e-6)
    check("ln 100 + gamma + 1/200", math.log(100) + gamma_em + 1 / 200, 5.187386, 1e-6)
    x = 0.1
    sqrt_quadratic = 1 + x / 2 - x**2 / 8
    log_two, log_three = x - x**2 / 2, x - x**2 / 2 + x**3 / 3
    check("sqrt(1.1)", math.sqrt(1 + x), 1.048809, 1e-6)
    check("1 + x/2 - x^2/8 at x = 0.1", sqrt_quadratic, 1.04875, 1e-9)
    check("x^2/8 at x = 0.1", x**2 / 8, 0.00125, 1e-15)
    check("sqrt(1.1) - quadratic, close to the next term x^3/16", math.sqrt(1 + x) - sqrt_quadratic, x**3 / 16, 5e-6)
    check("ln(1.1)", math.log1p(x), 0.0953102, 1e-7)
    check("r - r^2/2 at r = 0.1", log_two, 0.095, 1e-12)
    check("r - r^2/2 + r^3/3 at r = 0.1", log_three, 0.0953333, 1e-7)
    check("r^3/3 at r = 0.1", x**3 / 3, 0.000333, 1e-6)
    check("ln(1.1) - two terms, close to the next term r^3/3", math.log1p(x) - log_two, x**3 / 3, 3e-5)
    check("ln(1.1) - three terms, close to the next term -r^4/4", math.log1p(x) - log_three, -(x**4) / 4, 5e-6)
    prices = np.array([100.0, 50.0, 100.0])
    check("log returns of -50% then +100% add to", float(np.diff(np.log(prices)).sum()), 0.0, 1e-12)
    check("simple returns of -50% then +100% add to", float((prices[1:] / prices[:-1] - 1).sum()), 0.5, 1e-12)
    mu, sig, dt = 0.08, 0.2, 1e-6
    up, down = mu * dt + sig * math.sqrt(dt), mu * dt - sig * math.sqrt(dt)
    growth = 0.5 * (math.log1p(up) + math.log1p(down)) / dt
    check("median growth E[ln(1 + R)]/dt for +-sigma sqrt(dt) steps (8%, 20%)", growth, 0.06, 1e-6)


def lagrange_remainder() -> None:
    print("\n[07] Lagrange remainder for e^0.1 with the quadratic Taylor polynomial")
    approx = 1 + 0.1 + 0.1**2 / 2
    check("quadratic approximation", approx, 1.105, 1e-12)
    check("e^0.1", math.exp(0.1), 1.1051709, 1e-7)
    check("actual error", math.exp(0.1) - approx, 0.00017092, 1e-8)
    check("bound e^0.1 * 0.1^3 / 6 (using e^0.1 < 1.106)", 1.106 * 0.1**3 / 6, 0.00018433, 1e-8)
    check("lower bound 0.1^3 / 6", 0.1**3 / 6, 0.00016667, 1e-8)


# ---------------------------------------------------------------------------
# Leibniz rule, Breeden-Litzenberger, Gaussian integrals
# ---------------------------------------------------------------------------


def trapezoid(y: np.ndarray, x: np.ndarray) -> float:
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)


def leibniz_and_breeden_litzenberger() -> None:
    print("\n[07] differentiating a call price in strike (S = 100, T = 0.5, r = 3%, vol = 20%)")
    s, t, r, vol = 100.0, 0.5, 0.03, 0.20
    k, h = 100.0, 1e-3
    dc_dk = (bs_call(s, k + h, t, r, vol) - bs_call(s, k - h, t, r, vol)) / (2 * h)
    d2 = bs_greeks(s, k, t, r, vol)["d2"]
    check("dC/dK by finite difference", dc_dk, -math.exp(-r * t) * norm_cdf(d2), 1e-6)
    check("dC/dK = -e^{-rT} N(d2)", dc_dk, -0.5064, 1e-4)
    strikes = np.linspace(1.0, 400.0, 40_001)
    hk = strikes[1] - strikes[0]
    calls = np.array([bs_call(s, kk, t, r, vol) for kk in strikes])
    density = math.exp(r * t) * (calls[2:] - 2 * calls[1:-1] + calls[:-2]) / hk**2
    mid = strikes[1:-1]
    check("integral of e^{rT} C_KK dK", trapezoid(density, mid), 1.0, 1e-4)
    check("implied E[S_T] = S e^{rT}", trapezoid(density * mid, mid), s * math.exp(r * t), 1e-2)
    check("S e^{rT}", s * math.exp(r * t), 101.5113, 1e-4)


def feynman_trick() -> None:
    print("\n[07] Feynman's trick: I(a) = int_0^1 (x^a - 1)/ln x dx = ln(1 + a)")
    x = np.linspace(1e-9, 1 - 1e-9, 2_000_001)
    integrand = (x**2 - 1) / np.log(x)
    check("I(2) by quadrature", trapezoid(integrand, x), math.log(3), 1e-6)
    check("ln 3", math.log(3), 1.098612, 1e-6)


def gaussian_integrals() -> None:
    print("\n[07] Gaussian integrals")
    z = np.linspace(-12, 12, 480_001)
    phi = np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    check("int phi", trapezoid(phi, z), 1.0, 1e-10)
    check("E[Z^4]", trapezoid(z**4 * phi, z), 3.0, 1e-8)
    check("E[e^Z] = e^{1/2}", trapezoid(np.exp(z) * phi, z), math.exp(0.5), 1e-8)
    check("E[Z^2 e^Z] = 2 e^{1/2}", trapezoid(z**2 * np.exp(z) * phi, z), 2 * math.exp(0.5), 1e-7)
    check("2 e^{1/2}", 2 * math.exp(0.5), 3.297443, 1e-6)
    check("E[max(Z, 0)] = 1/sqrt(2 pi)", trapezoid(np.maximum(z, 0) * phi, z), 0.398942, 1e-6)
    check("E|Z| = sqrt(2/pi)", trapezoid(np.abs(z) * phi, z), 0.797885, 1e-6)
    check("Stein: E[Z sin Z] = E[cos Z] = e^{-1/2}", trapezoid(z * np.sin(z) * phi, z), math.exp(-0.5), 1e-8)
    check("e^{-1/2}", math.exp(-0.5), 0.606531, 1e-6)
    check("Gamma(1/2) = sqrt(pi)", math.gamma(0.5), math.sqrt(math.pi), 1e-12)
    check("int_0^inf x^3 e^{-x} dx = 3!", math.gamma(4), 6.0, 1e-12)


def main() -> None:
    delta_gamma_table()
    quanto_cross_gamma()
    duration_convexity()
    limits_and_series()
    lagrange_remainder()
    leibniz_and_breeden_litzenberger()
    feynman_trick()
    gaussian_integrals()
    print("\nall calculus_taylor checks passed")


if __name__ == "__main__":
    main()
