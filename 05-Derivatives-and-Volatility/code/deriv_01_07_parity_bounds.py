"""Option payoffs, put-call parity and model-free bounds: every number in 02-Option-Payoffs-and-Put-Call-Parity.md.

Parity, boxes, butterflies and conversions are checked by construction: each replicating portfolio is evaluated
on a grid of terminal prices and its payoff is compared with the claim it replicates.
Option prices come from Black-Scholes (pricing_core) and are confirmed by integrating the payoff against the
lognormal density; the American put uses a CRR tree.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_01_07_parity_bounds.py
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price

S_GRID = np.linspace(0.0, 400.0, 40_001)  # terminal prices for payoff-by-construction checks


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:66s} {value:14.8f}  quoted {quoted}")
    assert abs(value - float(quoted)) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:60s} |diff| = {abs(a - b):.2e} (tol {tol:.0e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def lognormal_price(payoff, S: float, T: float, r: float, sigma: float, q_: float = 0.0, n: int = 400_001) -> float:
    """Discounted risk-neutral expectation of payoff(S_T) by trapezoid quadrature over log price (independent of the BS formula)."""
    m = math.log(S) + (r - q_ - 0.5 * sigma**2) * T
    sd = sigma * math.sqrt(T)
    x = np.linspace(m - 12 * sd, m + 12 * sd, n)
    dens = np.exp(-0.5 * ((x - m) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
    g = payoff(np.exp(x)) * dens
    return math.exp(-r * T) * float(np.sum(0.5 * (g[1:] + g[:-1]) * np.diff(x)))


def crr_american_put(S: float, K: float, T: float, r: float, sigma: float, n: int) -> float:
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    v = np.maximum(K - S * u ** (n - 2.0 * np.arange(n + 1)), 0.0)
    for i in range(n - 1, -1, -1):
        v = disc * (p * v[:-1] + (1 - p) * v[1:])
        v = np.maximum(v, K - S * u ** (i - 2.0 * np.arange(i + 1)))
    return float(v[0])


def call(k: float) -> np.ndarray:
    return np.maximum(S_GRID - k, 0.0)


def put(k: float) -> np.ndarray:
    return np.maximum(k - S_GRID, 0.0)


def main() -> None:
    print("Parity by construction: call + bond paying K and put + one share both pay max(S_T, K)")
    for k in (50.0, 100.0, 150.0):
        assert np.array_equal(call(k) + k, put(k) + S_GRID) or np.allclose(call(k) + k, put(k) + S_GRID, atol=1e-12, rtol=0)
    print("  check payoffs equal on 40,001 terminal prices for K = 50, 100, 150")

    print("\nExample 1: conversion (S = K = 100, T = 1, r = 5%, call 10.45, put 4.50)")
    pv_k = 100 * math.exp(-0.05)
    q("parity value C - P = S - K e^{-rT}", 100 - pv_k, "4.877")
    q("market C - P", 10.45 - 4.50, "5.95")
    q("PV of the strike borrowed", pv_k, "95.12")
    cash_today = q("cash today from sell call, buy put, buy stock, borrow PV(K)", 10.45 - 4.50 - 100 + pv_k, "1.07")
    terminal = S_GRID + put(100) - call(100) - 100.0  # stock + put - call delivers exactly 100, which repays the loan
    assert float(np.max(np.abs(terminal))) < 1e-12, "conversion terminal cash flow must be zero in every state"
    print("  check conversion terminal cash flow is zero on every terminal price")
    c_bs, p_bs = bs_price(100, 100, 1.0, 0.05, 0.2), bs_price(100, 100, 1.0, 0.05, 0.2, call=False)
    q("Black-Scholes call at 20%", c_bs, "10.45")
    q("Black-Scholes put at 20%", p_bs, "5.57")
    close("BS call vs lognormal quadrature", c_bs, lognormal_price(lambda s: np.maximum(s - 100, 0), 100, 1.0, 0.05, 0.2), 1e-8)
    close("BS put vs lognormal quadrature", p_bs, lognormal_price(lambda s: np.maximum(100 - s, 0), 100, 1.0, 0.05, 0.2), 1e-8)
    close("cash today vs BS put minus market put", cash_today, p_bs - 4.50, 0.005)

    print("\nExample 2 and cards: boxes")
    box = call(95) - call(105) + put(105) - put(95)
    assert float(np.ptp(box)) < 1e-12 and abs(float(box[0]) - 10) < 1e-12
    print("  check the 95/105 box pays exactly 10 on every terminal price")
    q("fair 95/105 box, 6m, r = 4%", 10 * math.exp(-0.04 * 0.5), "9.802")
    q("implied rate of a box trading at 9.75 (%)", -100 * math.log(9.75 / 10) / 0.5, "5.06")
    q("same as a decimal (code comment)", -math.log(9.75 / 10) / 0.5, "0.0506")
    q("card deriv-box-spread-value: 90/110 box, 1y, r = 5%", 20 * math.exp(-0.05), "19.02")

    print("\nExample 3: butterfly arbitrage (calls 90 at 14.00, 100 at 8.00, 110 at 1.50)")
    q("butterfly cost", 14.00 - 2 * 8.00 + 1.50, "-0.50")
    fly = call(90) - 2 * call(100) + call(110)
    assert float(fly.min()) >= -1e-12 and abs(float(fly.max()) - 10) < 1e-9
    print("  check butterfly payoff is >= 0 everywhere with peak 10 at 100")
    q("90/100 call spread", 14.00 - 8.00, "6.00")
    q("100/110 call spread", 8.00 - 1.50, "6.50")

    print("\nExample 4: deep in-the-money American put (S = 10, K = 100, r = 5%, T = 1, 20% vol)")
    p_eu = q("European put", bs_price(10, 100, 1.0, 0.05, 0.2, call=False), "85.12")
    q("Ke^{-rT} - S", pv_k - 10, "85.12")
    p_am = q("American put on a 500-step CRR tree", crr_american_put(10, 100, 1.0, 0.05, 0.2, 500), "90.00")
    q("value given up by holding the European put", p_am - p_eu, "4.88")
    q("interest on the strike, 100 (1 - e^{-0.05})", 100 * (1 - math.exp(-0.05)), "4.88")

    print("\nExample 5: dividend and the American call (K = 100, r = 5%, dividend 2, 3 months to expiry after ex-date)")
    thr = q("K(1 - e^{-r tau})", 100 * (1 - math.exp(-0.05 * 0.25)), "1.24")
    q("exercise iff the ex-dividend European put is below", 2 - thr, "0.76")
    # Brute-force the decision at 20% vol: exercise (S - K) beats holding the ex-dividend European call exactly when P < 0.76.
    for s in np.linspace(80.0, 200.0, 241):
        hold = bs_price(s - 2, 100, 0.25, 0.05, 0.2)
        put_ex = bs_price(s - 2, 100, 0.25, 0.05, 0.2, call=False)
        assert (s - 100 > hold) == (put_ex < 2 - thr), s
    print("  check exercise decision equals the put-threshold rule on 241 spot levels")
    assert 1 - thr < 0
    print("  check a dividend of 1 gives a negative threshold, so never exercise")

    print("\nCalendar (card deriv-european-put-calendar): deep ITM European put, S = 50, K = 100, r = 5%")
    p1 = q("one-year European put", bs_price(50, 100, 1.0, 0.05, 0.2, call=False), "45.13")
    p2 = q("two-year European put", bs_price(50, 100, 2.0, 0.05, 0.2, call=False), "40.61")
    assert p2 < p1

    print("\nDigital and density from strikes (base case S = K = 100, T = 1, r = 5%, 20% vol)")
    h = 0.01
    digital_fd = (bs_price(100, 100 - h, 1.0, 0.05, 0.2) - bs_price(100, 100 + h, 1.0, 0.05, 0.2)) / (2 * h)
    q("digital call from a tight call spread", digital_fd, "0.5323")
    # Discounted Q(S_T > 100): trapezoid over log prices from ln 100 up, so the payoff jump sits on a grid edge.
    mu, sd = math.log(100) + (0.05 - 0.02) * 1.0, 0.2
    x = np.linspace(math.log(100), mu + 12 * sd, 400_001)
    dens = np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
    digital_quad = math.exp(-0.05) * float(np.sum(0.5 * (dens[1:] + dens[:-1]) * np.diff(x)))
    close("call spread vs quadrature of the digital payoff", digital_fd, digital_quad, 1e-6)
    fly_100 = bs_price(100, 99, 1.0, 0.05, 0.2) - 2 * bs_price(100, 100, 1.0, 0.05, 0.2) + bs_price(100, 101, 1.0, 0.05, 0.2)
    q("99/100/101 butterfly price", fly_100, "0.01876")
    f_q = math.exp(-0.5 * ((math.log(100) - mu) / sd) ** 2) / (100 * sd * math.sqrt(2 * math.pi))  # lognormal density at K = 100
    q("risk-neutral density at 100 from the butterfly, e^{rT} fly / h^2", math.exp(0.05) * fly_100, "0.01972")
    close("butterfly density vs lognormal density", math.exp(0.05) * fly_100, f_q, 1e-5)
    q("lognormal density at 100", f_q, "0.01972")
    q("e^{-rT}", math.exp(-0.05), "0.9512")
    q("N(d2) at the base case", (math.exp(0.05) * digital_quad), "0.5596")

    print("\nBounds hold for Black-Scholes prices at every vol (sanity)")
    for sig in (0.01, 0.2, 1.0, 5.0):
        for k in (50.0, 100.0, 200.0):
            c = bs_price(100, k, 1.0, 0.05, sig)
            p = bs_price(100, k, 1.0, 0.05, sig, call=False)
            lo_c, lo_p = max(100 - k * math.exp(-0.05), 0), max(k * math.exp(-0.05) - 100, 0)
            assert lo_c - 1e-9 <= c <= 100 + 1e-9 and lo_p - 1e-9 <= p <= k * math.exp(-0.05) + 1e-9
    print("  check call and put bounds on 12 vol and strike pairs")
    print("\nAll parity and bounds checks passed.")


if __name__ == "__main__":
    main()
