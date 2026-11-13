"""Black-Scholes formula and intuition: every number in 04-Black-Scholes-Formula-and-Intuition.md.

Prices come from pricing_core.bs_price and are confirmed independently by integrating the payoff against the
lognormal (or, for Black-76, the futures) density with the trapezoid rule, and by a 2000-step CRR tree for the base case.
The ATM shortcut errors are compared with the series term sigma^2 T / 24.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_01_07_black_scholes.py
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price, norm_cdf


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


def quad_call(F: float, K: float, T: float, r: float, sigma: float, n: int = 400_001) -> float:
    """e^{-rT} E[(S_T - K)^+] with ln S_T ~ N(ln F - sigma^2 T / 2, sigma^2 T), trapezoid from ln K upward (no N(d) used)."""
    m = math.log(F) - 0.5 * sigma**2 * T
    sd = sigma * math.sqrt(T)
    x = np.linspace(math.log(K), m + 12 * sd, n)
    g = (np.exp(x) - K) * np.exp(-0.5 * ((x - m) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
    return math.exp(-r * T) * float(np.sum(0.5 * (g[1:] + g[:-1]) * np.diff(x)))


def crr_call(S: float, K: float, T: float, r: float, sigma: float, n: int) -> float:
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    p = (math.exp(r * dt) - 1 / u) / (u - 1 / u)
    v = np.maximum(S * u ** (n - 2.0 * np.arange(n + 1)) - K, 0.0)
    for _ in range(n):
        v = math.exp(-r * dt) * (p * v[:-1] + (1 - p) * v[1:])
    return float(v[0])


def main() -> None:
    print("Example 1: S = K = 100, T = 1, r = 5%, 20% vol")
    d1 = (math.log(1.0) + (0.05 + 0.5 * 0.04) * 1.0) / 0.2
    q("d1", d1, "0.35")
    q("d2", d1 - 0.2, "0.15")
    q("N(d1)", norm_cdf(d1), "0.6368")
    q("N(d2)", norm_cdf(d1 - 0.2), "0.5596")
    q("K e^{-rT}", 100 * math.exp(-0.05), "95.123")
    q("S N(d1): stock received if exercised, in PV", 100 * norm_cdf(d1), "63.68")
    q("K e^{-rT} N(d2): strike paid if exercised, in PV", 100 * math.exp(-0.05) * norm_cdf(d1 - 0.2), "53.23")
    c = q("call", bs_price(100, 100, 1.0, 0.05, 0.2), "10.45")
    p = q("put", bs_price(100, 100, 1.0, 0.05, 0.2, call=False), "5.57")
    q("call, four decimals", c, "10.4506")
    q("delta read off the formula, N(d1)", norm_cdf(d1), "0.64")
    q("risk-neutral exercise probability, N(d2)", norm_cdf(d1 - 0.2), "0.56")
    q("S - K e^{-rT}", 100 - 100 * math.exp(-0.05), "4.88")
    q("K e^{-rT}, two decimals", 100 * math.exp(-0.05), "95.12")
    close("call vs lognormal quadrature", c, quad_call(100 * math.exp(0.05), 100, 1.0, 0.05, 0.2), 1e-8)
    close("call vs 2000-step CRR tree", c, crr_call(100, 100, 1.0, 0.05, 0.2, 2000), 5e-3)
    close("put from parity vs put formula", c - (100 - 100 * math.exp(-0.05)), p, 1e-12)

    print("\nExample 2: pricing in your head (zero rates)")
    q("0.4 x 100 x 0.30 x 0.5", 0.4 * 100 * 0.30 * 0.5, "6.00")
    q("exact three-month ATM call at 30%", bs_price(100, 100, 0.25, 0.0, 0.3), "5.98")
    q("exact, four decimals", bs_price(100, 100, 0.25, 0.0, 0.3), "5.9785")
    q("exact straddle", 2 * bs_price(100, 100, 0.25, 0.0, 0.3), "11.96")
    q("straddle shortcut 0.8 x 100 x 0.30 x 0.5", 0.8 * 100 * 0.30 * 0.5, "12.00")
    q("sqrt(1/3) (four months)", math.sqrt(1 / 3), "0.577")
    q("shortcut at 80% vol, 0.4 x 100 x 0.8", 0.4 * 100 * 0.8, "32.00")
    q("0.4 x 200 x 0.25 x sqrt(1/3)", 0.4 * 200 * 0.25 * math.sqrt(1 / 3), "11.55")
    q("exact four-month ATM call on 200 at 25%", bs_price(200, 200, 1 / 3, 0.0, 0.25), "11.51")
    exact80 = q("exact one-year ATM call at 80%", bs_price(100, 100, 1.0, 0.0, 0.8), "31.08")
    q("80 / sqrt(2 pi)", 80 / math.sqrt(2 * math.pi), "31.92")
    q("relative overestimate with 1/sqrt(2 pi) (%)", 100 * (80 / math.sqrt(2 * math.pi) / exact80 - 1), "2.7")
    q("series term sigma^2 T / 24 at sigma sqrt(T) = 0.8 (%)", 100 * 0.64 / 24, "2.7")
    q("series term at sigma sqrt(T) = 0.2 (%)", 100 * 0.04 / 24, "0.2")
    q("relative overestimate with the rounded 0.4 (%)", 100 * (32 / exact80 - 1), "2.9")
    q("extra from rounding 0.3989 up to 0.4 (%)", 100 * (32 / exact80 - 1) - 100 * (80 / math.sqrt(2 * math.pi) / exact80 - 1), "0.3")
    for x in (0.2, 0.8):  # the series term predicts the exact relative error to second order
        exact = bs_price(100, 100, 1.0, 0.0, x)
        close(f"(100 x {x} / sqrt(2 pi)) / exact - 1 vs {x}^2/24", 100 * x / math.sqrt(2 * math.pi) / exact - 1, x * x / 24, 3e-3 * x**4)

    print("\nExample 3: earnings straddle, stock 50, one-week straddle 4.00")
    q("expected absolute move (%)", 100 * 4 / 50, "8")
    q("one-standard-deviation move, 8% / 0.8 (%)", 8 / 0.8, "10")
    q("annualised vol on 7 calendar days (%)", 100 * 4 / (0.8 * 50 * math.sqrt(7 / 365)), "72")
    q("sqrt(1/52)", math.sqrt(1 / 52), "0.139")

    print("\nExample 4: ATM spot with rates")
    q("0.4 x 100 x 0.2 + (100 - 95.12) / 2", 0.4 * 100 * 0.2 + 0.5 * (100 - 100 * math.exp(-0.05)), "10.44")
    q("half the forward intrinsic", 0.5 * (100 - 100 * math.exp(-0.05)), "2.44")

    print("\nExample 5 and card deriv-strike-slide-estimate: sliding along the strike (r = 0, 20%, 1y)")
    atm = q("ATM call", bs_price(100, 100, 1.0, 0.0, 0.2), "7.97")
    nd2 = q("N(d2) = N(-0.1)", norm_cdf(-0.1), "0.460")
    q("N(-0.1), two decimals (card)", nd2, "0.46")
    q("linear estimate of the 102 call", atm - 2 * nd2, "7.05")
    q("exact 102 call", bs_price(100, 102, 1.0, 0.0, 0.2), "7.08")
    q("linear estimate of the 110 call", atm - 10 * nd2, "3.36")
    q("exact 110 call", bs_price(100, 110, 1.0, 0.0, 0.2), "4.29")
    h = 1e-3
    slope = (bs_price(100, 100 + h, 1.0, 0.0, 0.2) - bs_price(100, 100 - h, 1.0, 0.0, 0.2)) / (2 * h)
    close("dC/dK by finite difference vs -N(d2)", slope, -nd2, 1e-8)

    print("\nExample 6: Black-76, crude futures 80, strike 75, 6m, r = 4%, 35% vol")
    sd = 0.35 * math.sqrt(0.5)
    d1 = (math.log(80 / 75) + 0.5 * sd * sd) / sd
    q("d1", d1, "0.385")
    q("d2", d1 - sd, "0.137")
    q("N(d1)", norm_cdf(d1), "0.6497")
    q("N(d2)", norm_cdf(d1 - sd), "0.5545")
    # Black-76 is Black-Scholes with q = r on a spot equal to the futures price.
    c76 = q("Black-76 call", bs_price(80, 75, 0.5, 0.04, 0.35, q=0.04), "10.18")
    q("Black-76 call, four decimals", c76, "10.1832")
    close("Black-76 vs quadrature on the futures density", c76, quad_call(80, 75, 0.5, 0.04, 0.35), 1e-8)

    print("\nCards and mental-maths kit")
    q("deriv-atm-delta-above-half: N(0.4)", norm_cdf(0.4), "0.655")
    q("deriv-atm-delta-above-half: N(-0.4)", norm_cdf(-0.4), "0.345")
    q("deriv-rule-of-16: 32% / sqrt(252) (%)", 32 / math.sqrt(252), "2.0")
    q("sqrt(252)", math.sqrt(252), "15.87")
    q("1/sqrt(2 pi)", 1 / math.sqrt(2 * math.pi), "0.3989")
    q("1/sqrt(2 pi), three decimals (card)", 1 / math.sqrt(2 * math.pi), "0.399")
    q("sqrt(2/pi)", math.sqrt(2 / math.pi), "0.80")
    q("sqrt(1/12)", math.sqrt(1 / 12), "0.29")
    q("sqrt(52)", math.sqrt(52), "7.2")
    q("sqrt(12)", math.sqrt(12), "3.5")
    q("1/sqrt(252)", 1 / math.sqrt(252), "0.063")
    q("card deriv-atm-straddle-mental: 0.8 x 100 x 0.2 x 0.5", 0.8 * 100 * 0.2 * 0.5, "8.0")
    q("card deriv-atm-straddle-mental: exact 3m straddle at 20%", 2 * bs_price(100, 100, 0.25, 0.0, 0.2), "7.98")
    print("\nLimits")
    q(
        "call at sigma = 1e-6 equals discounted forward intrinsic",
        bs_price(100, 90, 1.0, 0.05, 1e-6) - (100 - 90 * math.exp(-0.05)),
        "0.0000",
    )
    q("call at sigma = 20 is close to S", bs_price(100, 100, 1.0, 0.05, 20.0), "100.0")
    q("homogeneity C(2S, 2K) - 2 C(S, K)", bs_price(200, 220, 0.5, 0.03, 0.3) - 2 * bs_price(100, 110, 0.5, 0.03, 0.3), "0.0000")
    print("\nAll Black-Scholes checks passed.")


if __name__ == "__main__":
    main()
