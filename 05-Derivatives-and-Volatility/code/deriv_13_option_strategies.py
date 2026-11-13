"""Option strategies and volatility trading: every number in 13-Option-Strategies-and-Volatility-Trading.md.

Independent routes used here:
- Black-Scholes prices from ``pricing_core`` are re-derived by Gauss-Legendre quadrature of the payoff against
  the lognormal density, so the closed form is never checked against itself;
- every Greek is computed from its closed form and checked against central finite differences of the price
  (delta, gamma, vega, theta, vanna and volga), and every scenario P&L is a full revaluation;
- strikes from deltas are solved by bisection on the delta, not by inverting the closed form;
- the event-volatility split solves the two total-variance equations as a 2 x 2 linear system, and the
  straddle break-even moves are found by bisection on full revaluation.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_13_option_strategies.py
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price, norm_cdf, norm_pdf

_X, _W = np.polynomial.legendre.leggauss(200)


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"    {label} = {value:.8f}  (quoted {quoted})")
    assert abs(value - float(quoted)) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"      check {label}: |{a:.8g} - {b:.8g}| = {abs(a - b):.1e} <= {tol:.0e}")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def quad_price(S: float, K: float, T: float, sig: float, call: bool) -> float:
    """r = 0 European price by quadrature over the normal driver, split at the strike."""
    zk = (math.log(K / S) + 0.5 * sig * sig * T) / (sig * math.sqrt(T))
    total = 0.0
    for lo, hi in ((-12.0, zk), (zk, 12.0)):
        z = 0.5 * (hi - lo) * _X + 0.5 * (hi + lo)
        st = S * np.exp(-0.5 * sig * sig * T + sig * math.sqrt(T) * z)
        pay = np.maximum(st - K, 0.0) if call else np.maximum(K - st, 0.0)
        total += 0.5 * (hi - lo) * float(np.sum(_W * pay * np.exp(-0.5 * z * z))) / math.sqrt(2 * math.pi)
    return total


def price(S: float, K: float, T: float, sig: float, cp: int) -> float:
    return float(bs_price(S, K, T, 0.0, sig, call=cp > 0))


def greeks(S: float, K: float, T: float, sig: float, cp: int) -> dict[str, float]:
    """Closed-form r = 0 Greeks: vega, vanna and volga per vol point (volga per point squared), theta per calendar day."""
    sd = sig * math.sqrt(T)
    d1 = math.log(S / K) / sd + 0.5 * sd
    d2 = d1 - sd
    vega = S * norm_pdf(d1) * math.sqrt(T)
    return {
        "price": price(S, K, T, sig, cp),
        "delta": norm_cdf(d1) if cp > 0 else norm_cdf(d1) - 1,
        "gamma": norm_pdf(d1) / (S * sd),
        "vega": vega / 100,
        "theta": -S * norm_pdf(d1) * sig / (2 * math.sqrt(T)) / 365,
        "vanna": -norm_pdf(d1) * d2 / sig / 100,
        "volga": vega * d1 * d2 / sig / 1e4,
    }


def book(S: float, legs: list[tuple[float, float, float, float, int]]) -> dict[str, float]:
    out: dict[str, float] = {}
    for qty, K, T, sig, cp in legs:
        for k, v in greeks(S, K, T, sig, cp).items():
            out[k] = out.get(k, 0.0) + qty * v
    return out


def book_value(S: float, legs, dvol: float = 0.0, dt: float = 0.0) -> float:
    return sum(qty * price(S, K, T - dt, sig + dvol, cp) for qty, K, T, sig, cp in legs)


def fd_check(name: str, legs) -> None:
    """Finite-difference every closed-form Greek of a book, a route independent of the formulas above."""
    g = book(100.0, legs)
    h, dv = 0.01, 1e-4
    close(f"{name} price by quadrature", sum(q_ * quad_price(100.0, K, T, s, cp > 0) for q_, K, T, s, cp in legs), g["price"], 1e-9)
    close(f"{name} delta", (book_value(100 + h, legs) - book_value(100 - h, legs)) / (2 * h), g["delta"], 1e-6)
    gam = (book_value(100 + h, legs) - 2 * book_value(100, legs) + book_value(100 - h, legs)) / h**2
    close(f"{name} gamma", gam, g["gamma"], 1e-4)
    close(f"{name} vega", (book_value(100, legs, dv) - book_value(100, legs, -dv)) / (2 * dv) / 100, g["vega"], 1e-7)
    close(f"{name} theta", (book_value(100, legs, dt=0.5 / 365) - book_value(100, legs, dt=-0.5 / 365)), g["theta"], 1e-5)
    dd = lambda d: (book_value(100 + h, legs, d) - book_value(100 - h, legs, d)) / (2 * h)  # noqa: E731
    close(f"{name} vanna", (dd(dv) - dd(-dv)) / (2 * dv) / 100, g["vanna"], 1e-6)
    volga = (book_value(100, legs, dv) - 2 * book_value(100, legs) + book_value(100, legs, -dv)) / dv**2 / 1e4
    close(f"{name} volga", volga, g["volga"], 1e-6)


def strike_for_delta(target: float, T: float, sig: float, cp: int) -> float:
    """Spot-delta strike by bisection on the delta itself (r = 0, S = 100)."""
    lo, hi = 20.0, 400.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        d = greeks(100.0, mid, T, sig, cp)["delta"]
        if d > target:  # delta falls as the strike rises, for calls and puts alike
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def solve(f, lo: float, hi: float) -> float:
    flo = f(lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> None:
    print("Straddle arithmetic (TL;DR and core concepts)")
    q("phi(0) = 1 / sqrt(2 pi)", 1 / math.sqrt(2 * math.pi), "0.3989")
    q("2 phi(0) = sqrt(2 / pi)", 2 / math.sqrt(2 * math.pi), "0.8")
    q("E|X| / sigma for a normal, sqrt(2 / pi), three decimals", math.sqrt(2 / math.pi), "0.798")
    rng = np.random.default_rng(13)
    close("E|Z| by simulation, 10^6 draws", float(np.abs(rng.standard_normal(1_000_000)).mean()), math.sqrt(2 / math.pi), 0.003)

    print("Example 1: 30-day ATM straddle, 25% vol, r = 0")
    T1 = 30 / 365
    strad = [(1, 100, T1, 0.25, 1), (1, 100, T1, 0.25, -1)]
    fd_check("straddle", strad)
    g = book(100.0, strad)
    q("straddle price", g["price"], "5.717")
    q("straddle price, card", g["price"], "5.72")
    q("straddle price, code", g["price"], "5.7174")
    q("0.8 sigma S sqrt T", 0.8 * 0.25 * 100 * math.sqrt(T1), "5.734")
    q("lower break-even", 100 - g["price"], "94.28")
    q("upper break-even", 100 + g["price"], "105.72")
    q("delta", g["delta"], "0.029")
    q("delta, code", g["delta"], "0.0286")
    q("gamma", g["gamma"], "0.111")
    q("gamma, code", g["gamma"], "0.1113")
    q("vega per point", g["vega"], "0.229")
    q("vega, code", g["vega"], "0.2286")
    q("theta per calendar day", g["theta"], "-0.095")
    q("theta, code", g["theta"], "-0.0952")
    q("break-even move sqrt(2 x 0.095 / 0.111)", math.sqrt(2 * 0.095 / 0.111), "1.31")
    q("break-even move from unrounded Greeks", math.sqrt(-2 * g["theta"] / g["gamma"]), "1.31")
    q("25% / sqrt(365) (%)", 25 / math.sqrt(365), "1.31")
    q("25% / sqrt(252) (%)", 25 / math.sqrt(252), "1.57")
    q("25 / 16 (%) (card)", 25 / 16, "1.56")

    print("Example 5 code: one-month / three-month ATM calendar at 20%")
    cal = [(-1, 100, 1 / 12, 0.20, 1), (1, 100, 0.25, 0.20, 1)]
    fd_check("calendar", cal)
    gc = book(100.0, cal)
    q("one-month call", price(100, 100, 1 / 12, 0.2, 1), "2.303")
    q("three-month call", price(100, 100, 0.25, 0.2, 1), "3.988")
    q("calendar cost", gc["price"], "1.685")
    q("calendar cost, code", gc["price"], "1.6848")
    q("calendar delta, code", gc["delta"], "0.0084")
    q("calendar gamma", gc["gamma"], "-0.029")
    q("calendar gamma, code", gc["gamma"], "-0.0292")
    q("calendar vega", gc["vega"], "0.084")
    q("calendar vega, code", gc["vega"], "0.0841")
    q("calendar theta per day", gc["theta"], "0.016")
    q("parallel 1-point rise, full revaluation", book_value(100, cal, 0.01) - book_value(100, cal), "0.084")
    weighted = (price(100, 100, 0.25, 0.21, 1) - price(100, 100, 0.25, 0.20, 1)) - (
        price(100, 100, 1 / 12, 0.20 + math.sqrt(3) / 100, 1) - price(100, 100, 1 / 12, 0.20, 1)
    )
    q("sqrt(3)", math.sqrt(3), "1.73")
    q("P&L with one-month up sqrt(3) points, three-month up 1", weighted, "-0.0002")
    v1, v3 = greeks(100, 100, 1 / 12, 0.2, 1)["vega"], greeks(100, 100, 0.25, 0.2, 1)["vega"]
    q("ATM vega ratio, three-month / one-month", v3 / v1, "1.731")
    q("sqrt(3) to three decimals", math.sqrt(3), "1.732")

    print("Example 2: realized 30% against implied 25%")
    v30 = 2 * price(100, 100, T1, 0.30, 1)  # ATM-spot straddle with r = 0: C + P = 2C
    q("straddle at 30%", price(100, 100, T1, 0.30, 1) + price(100, 100, T1, 0.30, -1), "6.860")
    close("C + P = 2C at the money with r = 0", v30, price(100, 100, T1, 0.30, 1) + price(100, 100, T1, 0.30, -1), 1e-12)
    q("value difference 6.860 - 5.717", v30 - g["price"], "1.143")
    q("vega x 5 points", g["vega"] * 5, "1.14")

    print("Example 3: event volatility from two expiries")
    w1, w2 = 0.60**2 * 10 / 252, 0.40**2 * 30 / 252
    q("front total variance", w1, "0.014286")
    q("back total variance", w2, "0.019048")
    A = np.array([[9 / 252, 1.0], [29 / 252, 1.0]])  # sigma_b^2 (T_i - 1 day) + m^2 = w_i
    sb2, m2 = np.linalg.solve(A, np.array([w1, w2]))
    q("ex-event variance sigma_b^2", float(sb2), "0.06")
    q("ex-event vol (%)", 100 * math.sqrt(sb2), "24.5")
    q("event variance m^2", float(m2), "0.012143")
    q("event variance m^2, card", float(m2), "0.0121")
    q("event-day standard deviation m (%)", 100 * math.sqrt(m2), "11.0")
    q("expected absolute move m sqrt(2/pi) (%)", 100 * math.sqrt(m2) * math.sqrt(2 / math.pi), "8.8")
    p0 = q("front ATM straddle, 10 trading days at 60%", 2 * price(100, 100, 10 / 252, 0.6, 1), "9.53")
    sb = math.sqrt(sb2)
    p1 = q("next day, no move, 9 days at 24.5%", 2 * price(100, 100, 9 / 252, sb, 1), "3.69")
    q("vol crush", p0 - p1, "5.84")
    strad_next = lambda s: price(s, 100, 9 / 252, sb, 1) + price(s, 100, 9 / 252, sb, -1) - p0  # noqa: E731
    q("break-even up move", solve(strad_next, 100, 130) - 100, "9.4")
    q("break-even down move", 100 - solve(strad_next, 70, 100), "9.5")

    print("Example 4: 25-delta risk reversal, three months, put 24%, call 18%")
    Tq = 0.25
    kp = q("25-delta put strike", strike_for_delta(-0.25, Tq, 0.24, -1), "92.89")
    kc = q("25-delta call strike", strike_for_delta(0.25, Tq, 0.18, 1), "106.69")
    rr = [(1, kc, Tq, 0.18, 1), (-1, kp, Tq, 0.24, -1)]
    fd_check("risk reversal", rr)
    grr = book(100.0, rr)
    q("call premium", price(100, kc, Tq, 0.18, 1), "1.284")
    q("put premium", price(100, kp, Tq, 0.24, -1), "1.903")
    q("credit", -grr["price"], "0.619")
    q("delta", grr["delta"], "0.50")
    q("net vega", grr["vega"], "0.000")
    q("vega of each leg", greeks(100, kc, Tq, 0.18, 1)["vega"], "0.159")
    close("the two legs have equal vega", greeks(100, kc, Tq, 0.18, 1)["vega"], greeks(100, kp, Tq, 0.24, -1)["vega"], 1e-9)
    q("vanna per vol point", grr["vanna"], "0.021")
    steepen = book_value(100, [(1, kc, Tq, 0.17, 1), (-1, kp, Tq, 0.25, -1)]) - book_value(100, rr)
    q("loss when put vol +1 and call vol -1", -steepen, "0.317")
    q("loss, two decimals (card)", -steepen, "0.32")
    q("loss on a 5-point drop, sticky strike", -(book_value(95, rr) - book_value(100, rr)), "2.48")

    print("Example 6: vega-neutral strangle against straddle, three months, flat 20%")
    kp6 = q("25-delta put strike", strike_for_delta(-0.25, Tq, 0.2, -1), "93.95")
    kc6 = q("25-delta call strike", strike_for_delta(0.25, Tq, 0.2, 1), "107.51")
    stg = [(1, kp6, Tq, 0.2, -1), (1, kc6, Tq, 0.2, 1)]
    std = [(1, 100, Tq, 0.2, 1), (1, 100, Tq, 0.2, -1)]
    fd_check("strangle", stg)
    fd_check("straddle", std)
    gs, gd = book(100.0, stg), book(100.0, std)
    q("strangle vega", gs["vega"], "0.318")
    q("strangle volga per point squared", gs["volga"], "0.0072")
    q("straddle vega", gd["vega"], "0.398")
    print(f"    straddle volga per point squared = {gd['volga']:.6f} (essentially zero)")
    assert abs(gd["volga"]) < 0.01 * gs["volga"]
    n = q("strangles per straddle for vega neutrality", gd["vega"] / gs["vega"], "1.254")
    q("strangles per straddle, card", n, "1.25")
    for dv, quoted in ((-0.05, "0.144"), (0.05, "0.094")):
        pnl = n * (book_value(100, stg, dv) - book_value(100, stg)) - (book_value(100, std, dv) - book_value(100, std))
        q(f"P&L for a parallel {100 * dv:+.0f}-point move", pnl, quoted)
    print("All option strategy checks passed.")


if __name__ == "__main__":
    main()
