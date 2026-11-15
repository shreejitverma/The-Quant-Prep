"""Options market making: every number in `08-Market-Making/07-Options-Market-Making.md`.

Independent routes used here:
- prices by numerical quadrature of the discounted payoff against the lognormal density
  (composite Simpson over the standard normal variable, no normal CDF), checked against the
  Black-Scholes closed form;
- Greeks by central finite differences of the quadrature price, checked against closed-form Greeks;
  theta is per calendar day (divided by 365);
- American exercise by a Cox-Ross-Rubinstein binomial tree, never by the parity inequality it is
  compared with;
- the sticky-moneyness vol from the linear skew evaluated at the moneyness-equivalent strike K S0 / S1.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 08-Market-Making/code/mm_07_options_market_making.py`.
"""

from __future__ import annotations

import math

import numpy as np


def simpson(a: float, b: float, n: int = 20_000) -> tuple[np.ndarray, np.ndarray]:
    """Nodes and composite-Simpson weights times the standard normal density on [a, b]."""
    z = np.linspace(a, b, n + 1)
    w = np.ones_like(z)
    w[1:-1:2], w[2:-1:2] = 4.0, 2.0
    w *= (z[1] - z[0]) / 3.0
    return z, w * np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


Z, W = simpson(-12.0, 12.0)


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def close(label: str, a: float, b: float, tol: float) -> None:
    assert abs(a - b) <= tol, f"{label}: {a!r} vs {b!r}"
    print(f"    check {label}: |diff| = {abs(a - b):.1e} <= {tol:.0e}")


def quad_price(S: float, K: float, T: float, vol: float, r: float = 0.0, call: bool = True) -> float:
    """Discounted expected payoff by Simpson quadrature over the normal variable, split at the kink."""
    sd = vol * math.sqrt(T)
    kink = (math.log(K / S) - (r - 0.5 * vol * vol) * T) / sd
    z, w = simpson(kink, 12.0) if call else simpson(-12.0, kink)
    ST = S * np.exp((r - 0.5 * vol * vol) * T + sd * z)
    payoff = ST - K if call else K - ST
    return math.exp(-r * T) * float(np.sum(w * payoff))


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_closed(S: float, K: float, T: float, vol: float, r: float = 0.0, call: bool = True) -> dict[str, float]:
    sd = vol * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * vol * vol) * T) / sd
    d2 = d1 - sd
    pdf = math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)
    c = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    price = c if call else c - S + K * math.exp(-r * T)
    carry = -r * K * math.exp(-r * T) * (norm_cdf(d2) if call else -norm_cdf(-d2))
    return {
        "price": price,
        "delta": norm_cdf(d1) if call else norm_cdf(d1) - 1.0,
        "gamma": pdf / (S * sd),
        "vega": S * pdf * math.sqrt(T) / 100.0,
        "theta": (-S * pdf * vol / (2.0 * math.sqrt(T)) + carry) / 365.0,
    }


def fd_greeks(S: float, K: float, T: float, vol: float, r: float = 0.0, call: bool = True) -> dict[str, float]:
    """Greeks from central differences of the quadrature price only."""

    def p(s: float = S, t: float = T, v: float = vol) -> float:
        return quad_price(s, K, t, v, r, call)

    hs, hv, ht = 0.01, 1e-4, 1e-5
    return {
        "price": p(),
        "delta": (p(s=S + hs) - p(s=S - hs)) / (2 * hs),
        "gamma": (p(s=S + hs) - 2 * p() + p(s=S - hs)) / hs**2,
        "vega": (p(v=vol + hv) - p(v=vol - hv)) / (2 * hv) / 100.0,
        "theta": -(p(t=T + ht) - p(t=T - ht)) / (2 * ht) / 365.0,
    }


def greeks(S: float, K: float, T: float, vol: float, r: float = 0.0, call: bool = True) -> dict[str, float]:
    fd, cf = fd_greeks(S, K, T, vol, r, call), bs_closed(S, K, T, vol, r, call)
    for key, tol in (("price", 1e-9), ("delta", 1e-6), ("gamma", 1e-5), ("vega", 1e-6), ("theta", 1e-6)):
        assert abs(fd[key] - cf[key]) <= tol, (key, fd[key], cf[key])
    return fd


def crr(S: float, K: float, T: float, r: float, vol: float, steps: int, call: bool, american: bool) -> float:
    dt = T / steps
    u = math.exp(vol * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    j = np.arange(steps + 1)
    s = S * u ** (steps - j) * d**j
    val = np.maximum(s - K, 0.0) if call else np.maximum(K - s, 0.0)
    for i in range(steps, 0, -1):
        k = np.arange(i)
        s = S * u ** (i - 1 - k) * d**k
        val = disc * (p * val[:-1] + (1.0 - p) * val[1:])
        if american:
            val = np.maximum(val, (s - K) if call else (K - s))
    return float(val[0])


def example1() -> dict[str, float]:
    print("Example 1: quoting one option (cards mm-options-vol-width-to-price, mm-options-hedge-cost-floor)")
    g = greeks(100, 105, 0.25, 0.25)
    close("quadrature price vs closed form", g["price"], bs_closed(100, 105, 0.25, 0.25)["price"], 1e-9)
    approx("call theo", g["price"], 2.99, 2)
    approx("delta", g["delta"], 0.372, 3)
    approx("gamma", g["gamma"], 0.0302, 4)
    approx("vega per vol point", g["vega"], 0.189, 3)
    approx("theta per calendar day", g["theta"], -0.026, 3)
    bid, ask = quad_price(100, 105, 0.25, 0.245), quad_price(100, 105, 0.25, 0.255)
    approx("bid at 24.5 vol", bid, 2.897, 3)
    approx("ask at 25.5 vol", ask, 3.086, 3)
    approx("price width", ask - bid, 0.19, 2)
    close("price width vs vega x 1 point", ask - bid, g["vega"], 0.001)
    tick = 0.05
    bid_q, ask_q = math.floor(bid / tick) * tick, math.ceil(ask / tick) * tick
    approx("bid rounded down to 0.05", bid_q, 2.85, 2)
    approx("ask rounded up to 0.05", ask_q, 3.10, 2)
    approx("half-width of the rounded market", (ask_q - bid_q) / 2, 0.125, 3)
    approx("hedge cost |delta| x 0.005", g["delta"] * 0.005, 0.002, 3)
    return g


def example2(g: dict[str, float]) -> None:
    print("Example 2: the underlying ticks up (card mm-options-sticky-strike-moneyness, mm-options-sticky-moneyness-theo)")
    base = quad_price(100, 105, 0.25, 0.25)
    up = quad_price(100.5, 105, 0.25, 0.25)
    approx("full reprice at 100.50", up, 3.181, 3)
    approx("change", up - base, 0.190, 3)
    approx("Taylor delta x 0.5 + gamma x 0.25 / 2", g["delta"] * 0.5 + 0.5 * g["gamma"] * 0.25, 0.190, 3)
    k_equiv = 105 * 100 / 100.5
    approx("moneyness-equivalent strike K S0 / S1", k_equiv, 104.5, 1)
    approx("moneyness-equivalent strike, two decimals", k_equiv, 104.48, 2)
    vol_sm = 25.0 + 0.2 * (105 - k_equiv)  # skew -0.2 vol points per dollar of strike
    approx("sticky-moneyness vol (points)", vol_sm, 25.1, 1)
    approx("vol change (points)", vol_sm - 25.0, 0.1, 1)
    sm = quad_price(100.5, 105, 0.25, 0.251)
    approx("theo at 25.1%", sm, 3.201, 3)
    approx("extra change from the smile", sm - up, 0.019, 3)
    approx("vega x 0.1", g["vega"] * 0.1, 0.019, 3)
    approx("smile term as a share of the move", (sm - up) / (up - base), 0.10, 2)


def example3() -> None:
    print("Example 3: portfolio Greeks and a lean (cards mm-options-gamma-theta, mm-options-lean-on-vega, mm-options-book-delta)")
    rows = [
        (200, greeks(100, 100, 0.25, 0.26), (0.526, 0.0306, 0.199, -0.028)),
        (-300, greeks(100, 105, 0.25, 0.25), (0.372, 0.0302, 0.189, -0.026)),
        (-100, greeks(100, 95, 0.5, 0.28, call=False), (-0.360, 0.0189, 0.265, -0.020)),
    ]
    for qty, g, quoted in rows:
        for key, lit, dec in zip(("delta", "gamma", "vega", "theta"), quoted, (3, 4, 3, 3), strict=True):
            approx(f"row {qty:+d}: {key}", g[key], lit, dec)

    def total(key: str, sel: slice = slice(None)) -> float:
        return sum(q * g[key] * 100 for q, g, _ in rows[sel])

    approx("book delta (shares)", total("delta"), 2974, 0)
    approx("shown working: book delta from the rounded table deltas", 100 * (200 * 0.526 - 300 * 0.372 + 100 * 0.360), 2960, 0)
    approx("book gamma (shares per dollar)", total("gamma"), -484, 0)
    approx("book vega (dollars per point)", total("vega"), -4336, 0)
    approx("book vega, hundreds of dollars (card: short about 4,300)", total("vega") / 100, -43, 0)
    approx("3-month vega", total("vega", slice(0, 2)), -1690, 0)
    approx("6-month vega", total("vega", slice(2, 3)), -2646, 0)
    assert abs(total("vega", slice(2, 3))) > abs(total("vega", slice(0, 2))), "card: mostly in 6 months"
    approx("book theta (dollars per day)", total("theta"), 413, 0)
    approx("shown working: one-dollar move cost 0.5 x 484", 0.5 * 484 * 1.0**2, 242, 0)
    approx("shown working: break-even daily move sqrt(2 x 413 / 484)", math.sqrt(2 * 413 / 484), 1.31, 2)
    # gamma-theta identity at r = 0: theta = -0.5 gamma S^2 sigma^2 (per year), from finite differences only
    g = rows[1][1]
    close("theta x 365 vs -0.5 gamma S^2 sigma^2", g["theta"] * 365, -0.5 * g["gamma"] * 100**2 * 0.25**2, 1e-4)


def example4() -> None:
    print("Example 4: implied event move and vol crush (cards mm-options-event-variance, mm-options-vol-crush)")
    T = 30 / 365
    ev = (0.45**2 - 0.25**2) * T
    approx("event variance", ev, 0.0115, 4)
    approx("event sd", math.sqrt(ev), 0.107, 3)
    approx("mean absolute move sd x sqrt(2/pi)", math.sqrt(ev) * math.sqrt(2 / math.pi), 0.086, 3)
    # mean absolute move of a normal by quadrature, not the sqrt(2/pi) formula
    approx("mean absolute move by quadrature", math.sqrt(ev) * float(np.sum(W * np.abs(Z))), 0.086, 3)
    before = quad_price(100, 100, T, 0.45) + quad_price(100, 100, T, 0.45, call=False)
    approx("ATM straddle at 45%", before, 10.29, 2)
    approx("0.8 sigma sqrt(T) S", 0.8 * 0.45 * math.sqrt(T) * 100, 10.32, 2)
    after = quad_price(100, 100, 29 / 365, 0.25) + quad_price(100, 100, 29 / 365, 0.25, call=False)
    approx("straddle next day at 25%, 29 days", after, 5.62, 2)
    approx("vol crush", before - after, 4.67, 2)


def example5() -> None:
    print("Example 5: pin risk (card mm-options-pin-risk)")
    shares = 1000 * 100
    approx("2% of 50.02", 0.02 * 50.02, 1.0, 2)
    approx("shown working: P&L swing at 1 dollar a share", shares * 1.0, 100_000, 0)


def example6() -> None:
    print("Example 6: exercise before the dividend (cards mm-options-early-exercise-call, mm-options-dividend-give-up)")
    K, S, D, r, vol, tau = 40.0, 50.0, 0.50, 0.05, 0.30, 30 / 365
    interest = K * (1 - math.exp(-r * tau))
    approx("interest on the strike", interest, 0.164, 3)
    put = quad_price(S - D, K, tau, vol, r, call=False)
    approx("put on the ex-dividend stock", put, 0.007, 3)
    approx("threshold", interest + put, 0.171, 3)
    # hold value: American call on 49.50 with no further dividends, by binomial tree
    hold = [crr(S - D, K, tau, r, vol, n, call=True, american=True) for n in (2000, 4000)]
    close("tree at 2000 vs 4000 steps", hold[0], hold[1], 2e-4)
    approx("call held through the ex-date (tree)", hold[1], 9.67, 2)
    approx("exercise value", S - K, 10.00, 2)
    approx("gain from exercising", (S - K) - hold[1], 0.33, 2)
    close("gain vs D - threshold", (S - K) - hold[1], D - (interest + put), 2e-4)
    approx("shown working: 0.50 - (0.164 + 0.007)", 0.50 - (0.164 + 0.007), 0.33, 2)

    print("Early exercise of a put: the parity condition is necessary, not sufficient (card mm-options-early-exercise-put)")
    for spot, decision in ((35.0, "hold"), (34.0, "exercise")):
        call = quad_price(spot, K, tau, vol, r)
        am = [crr(spot, K, tau, r, vol, n, call=False, american=True) for n in (2000, 4000)]
        print(f"    S = {spot}: K(1 - e^(-r tau)) = {interest:.3f}, call = {call:.3f}, American put = {am[1]:.4f}")
        assert interest > call
        if decision == "hold":
            assert min(am) > K - spot + 0.01, am
        else:
            assert max(am) <= K - spot + 1e-9, am
    approx("call at S = 35", quad_price(35.0, K, tau, vol, r), 0.093, 3)
    approx("American put at S = 35 (tree)", crr(35.0, K, tau, r, vol, 4000, call=False, american=True), 5.018, 3)


if __name__ == "__main__":
    g1 = example1()
    example2(g1)
    example3()
    example4()
    example5()
    example6()
    print("all options market making checks passed")
