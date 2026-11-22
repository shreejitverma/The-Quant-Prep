"""Adverse selection models: every number in the order-flow note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/03-Order-Flow-and-Adverse-Selection.md`.
Independent routes used here:
- Glosten-Milgrom quotes by direct Bayes enumeration over (state, trader type, order side) in exact
  fractions, against the note's closed-form ask, bid and spread formulas on 200 random (p0, alpha) pairs,
  and against a seeded simulation of order arrivals (E[V | buy] estimated with a five-standard-error band);
- Kyle (1985) one-period lambda and depth: regress simulated values on simulated order flow and compare
  with sqrt(Sigma_0) / (2 sigma_u) within five standard errors;
- Kyle continuous time: simulate the insider's strategy beta(t) = sigma_u / (sqrt(Sigma_0) (1 - t)) with
  lambda = sqrt(Sigma_0) / sigma_u and check that the posterior variance at t = 1/2 is (1 - t) Sigma_0;
- Roll (1984): the estimate on the five quoted prices from the sample products, and the estimator's mean
  under independent trade signs (recovers s) and under alternating signs (2 s) by simulation.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_pqt_03_adverse_selection.py`.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

SEED = 31


def rounded(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(value):,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def gm_enumerate(vl: Fraction, vh: Fraction, p0: Fraction, alpha: Fraction) -> tuple[Fraction, Fraction]:
    """E[V | buy] and E[V | sell] by summing joint probabilities of (state, trader type, side)."""
    joint = {("buy", vh): Fraction(0), ("buy", vl): Fraction(0), ("sell", vh): Fraction(0), ("sell", vl): Fraction(0)}
    for v, pv in ((vh, p0), (vl, 1 - p0)):
        informed_side = "buy" if v == vh else "sell"
        joint[(informed_side, v)] += pv * alpha
        for side in ("buy", "sell"):
            joint[(side, v)] += pv * (1 - alpha) / 2
    out = []
    for side in ("buy", "sell"):
        mass = joint[(side, vh)] + joint[(side, vl)]
        out.append((joint[(side, vh)] * vh + joint[(side, vl)] * vl) / mass)
    return out[0], out[1]


def gm_closed_form(vl, vh, p0, alpha):
    s0 = p0 * vh + (1 - p0) * vl
    d = alpha * (2 * p0 - 1)
    ask = s0 + (vh - s0) * 2 * alpha * p0 / (1 + d)
    bid = s0 - (s0 - vl) * 2 * alpha * (1 - p0) / (1 - d)
    spread = (vh - vl) * 4 * alpha * p0 * (1 - p0) / (1 - d * d)
    return ask, bid, spread


def glosten_milgrom(rng: np.random.Generator) -> None:
    print("Glosten-Milgrom example")
    vl, vh, p0, alpha = Fraction(80), Fraction(120), Fraction(1, 2), Fraction(1, 4)
    print(f"    input: V_L = ${float(vl):.2f}, V_H = ${float(vh):.2f}, p0 = {float(p0):.2f}, alpha = {float(alpha):.2f}")
    ask, bid = gm_enumerate(vl, vh, p0, alpha)
    rounded("S0", p0 * vh + (1 - p0) * vl, "100.00")
    rounded("P(buy | V_H)", alpha + (1 - alpha) / 2, "0.625")
    rounded("P(buy | V_L)", (1 - alpha) / 2, "0.375")
    rounded("P(buy)", p0 * (alpha + (1 - alpha) / 2) + (1 - p0) * (1 - alpha) / 2, "0.50")
    rounded("informed share (%)", alpha * 100, "25")
    rounded("noise share (%)", (1 - alpha) * 100, "75")
    rounded("noise fraction 1 - alpha", 1 - alpha, "0.75")
    rounded("P(V_H | buy)", (ask - vl) / (vh - vl), "0.625")
    p_h_buy = p0 * (alpha + (1 - alpha) / 2) / (p0 * (alpha + (1 - alpha) / 2) + (1 - p0) * (1 - alpha) / 2)
    rounded("P(V_H | buy) x V_H", p_h_buy * vh, "75.00")
    rounded("P(V_L | buy) x V_L", (1 - p_h_buy) * vl, "30.00")
    p_sell = p0 * (1 - alpha) / 2 + (1 - p0) * (alpha + (1 - alpha) / 2)
    rounded("P(sell)", p_sell, "0.50")
    p_l_sell = (1 - p0) * (alpha + (1 - alpha) / 2) / p_sell
    rounded("P(V_L | sell), Bayes", p_l_sell, "0.625")
    rounded("P(V_H | sell) x V_H", (1 - p_l_sell) * vh, "45.00")
    rounded("P(V_L | sell) x V_L", p_l_sell * vl, "50.00")
    assert (1 - p_l_sell) * vh + p_l_sell * vl == bid
    rounded("V_H - V_L", vh - vl, "40.00")
    rounded("ask, Bayes enumeration", ask, "105.00")
    rounded("bid, Bayes enumeration", bid, "95.00")
    rounded("P(V_H | sell)", (bid - vl) / (vh - vl), "0.375")
    rounded("spread", ask - bid, "10.00")
    rounded("alpha * (V_H - V_L)", alpha * (vh - vl), "10.00")
    insider_take = vh - ask
    noise_pay = ask - (p0 * vh + (1 - p0) * vl)
    rounded("insider gain per order", insider_take, "15.00")
    rounded("noise trader loss per order", noise_pay, "5.00")
    rounded("expected loss to insiders per order", alpha * insider_take, "3.75")
    rounded("expected gain from noise per order", (1 - alpha) * noise_pay, "3.75")

    print("  closed forms against enumeration on random priors")
    for _ in range(200):
        p = Fraction(int(rng.integers(1, 99)), 100)
        a = Fraction(int(rng.integers(1, 99)), 100)
        e_ask, e_bid = gm_enumerate(vl, vh, p, a)
        c_ask, c_bid, c_spread = gm_closed_form(vl, vh, p, a)
        assert e_ask == c_ask and e_bid == c_bid and e_ask - e_bid == c_spread
        assert c_ask > p * vh + (1 - p) * vl > c_bid
    print("    200 random (p0, alpha) pairs: closed form equals enumeration exactly")

    n = 400_000
    high = rng.random(n) < 0.5
    informed = rng.random(n) < 0.25
    buy = np.where(informed, high, rng.random(n) < 0.5)
    v = np.where(high, 120.0, 80.0)
    est, se = v[buy].mean(), v[buy].std(ddof=1) / np.sqrt(buy.sum())
    print(f"    simulated E[V | buy] (seed {SEED}) = {est:.3f} +/- {se:.3f}")
    assert abs(est - 105.0) < 5 * se

    # spread shrinks as beliefs converge (card mkt-pqt-085): exact posterior path in the high state
    p = Fraction(1, 2)
    spreads = []
    for _ in range(60):
        spreads.append(gm_closed_form(vl, vh, p, alpha)[2])
        p = p * (1 + alpha) / (1 + alpha * (2 * p - 1))  # posterior after a buy
    print(f"    spread after 0, 20, 59 consecutive buys = {float(spreads[0]):.4f}, {float(spreads[20]):.4f}, {float(spreads[59]):.6f}")
    assert all(spreads[i + 1] < spreads[i] for i in range(59)) and spreads[59] < spreads[0] / 1000


def kyle(rng: np.random.Generator) -> None:
    print("Kyle one-period lambda")
    sigma0, su = 4.0, 3.0  # Sigma_0 = 16, sigma_u = 3 (hypothetical)
    lam = np.sqrt(sigma0**2) / (2 * su)
    beta = su / sigma0
    n = 400_000
    v = rng.normal(0, sigma0, n)
    y = beta * v + rng.normal(0, su, n)
    slope = np.cov(v, y)[0, 1] / np.var(y, ddof=1)
    resid = v - slope * y
    se = np.sqrt(np.var(resid, ddof=1) / (np.var(y, ddof=1) * n))
    print(f"    lambda closed form = {lam:.4f}, regression = {slope:.4f} +/- {se:.4f}")
    assert abs(slope - lam) < 5 * se
    print(f"    depth 1 / lambda = {1 / lam:.4f} (2 sigma_u / sqrt(Sigma_0) = {2 * su / sigma0:.4f})")

    print("Kyle continuous time: posterior variance (1 - t) Sigma_0")
    paths, steps, t_end = 40_000, 2000, 0.5
    dt = t_end / steps
    lam_c = sigma0 / su
    v = rng.normal(0, sigma0, paths)
    p = np.zeros(paths)
    for k in range(steps):
        t = k * dt
        b = su / (sigma0 * (1 - t))
        dy = b * (v - p) * dt + su * np.sqrt(dt) * rng.normal(size=paths)
        p += lam_c * dy
    var = np.var(v - p, ddof=1)
    se = var * np.sqrt(2 / (paths - 1))
    print(f"    Var(v - p) at t = 0.5: simulated {var:.4f} +/- {se:.4f}, theory {(1 - t_end) * sigma0**2:.4f}")
    assert abs(var - (1 - t_end) * sigma0**2) < 5 * se


def roll(rng: np.random.Generator) -> None:
    print("Roll estimator")
    prices = np.array([100.00, 100.05, 100.00, 100.05, 100.00])
    print(f"    input: trade prices {', '.join(f'${p:.2f}' for p in prices)}")
    dp = np.diff(prices)
    rounded("mean price change", dp.mean() + 0.0, "0.00")
    products = dp[1:] * dp[:-1]
    cov = products.sum() / len(products)
    rounded("sample serial covariance", cov, "-0.0025")
    s_roll = 2 * np.sqrt(-cov)
    rounded("Roll spread", s_roll, "0.10")
    quoted = prices.max() - prices.min()
    rounded("quoted spread in the sample (cents)", 100 * quoted, "5")
    rounded("Roll spread / quoted spread", s_roll / quoted, "2")
    rounded("expected covariance with s = 0.05", -(quoted**2) / 4, "-0.000625")
    rounded("ratio of sample to expected covariance", cov / (-(quoted**2) / 4), "4")

    s, sigma, n, reps = 0.05, 0.02, 2000, 400
    est_ind, est_alt = [], []
    for _ in range(reps):
        m = np.cumsum(rng.normal(0, sigma, n))
        q = rng.choice([-1, 1], n)
        d = np.diff(m + q * s / 2)
        est_ind.append(np.mean((d[1:] - d.mean()) * (d[:-1] - d.mean())))
        q_alt = np.where(np.arange(n) % 2 == 0, 1, -1)
        d = np.diff(m + q_alt * s / 2)
        est_alt.append(np.mean((d[1:] - d.mean()) * (d[:-1] - d.mean())))
    for name, est, target in (("independent signs", est_ind, -(s**2) / 4), ("alternating signs", est_alt, -(s**2))):
        mean, se = np.mean(est), np.std(est, ddof=1) / np.sqrt(reps)
        print(f"    mean serial covariance, {name} = {mean:.7f} +/- {se:.7f} (theory {target:.7f})")
        assert abs(mean - target) < 5 * se


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    glosten_milgrom(rng)
    print("Card mkt-pqt-091: internalizer price improvement")
    rounded("midpoint of $100.00 x $100.01", (Fraction("100.00") + Fraction("100.01")) / 2, "100.005")
    print("    cited: card mkt-pqt-084, Tick Size Pilot (2016) raised the increment from $0.01 to $0.05")
    print("    cited: Lee and Ready (1991) compare each trade with the quote in effect 5 seconds earlier")
    print("    cited: Release 34-105655 (June 11, 2026, File S7-2026-20) proposes rescinding Rules 611 and 610(e)")
    kyle(rng)
    roll(rng)
    print("all adverse-selection numbers check out")
