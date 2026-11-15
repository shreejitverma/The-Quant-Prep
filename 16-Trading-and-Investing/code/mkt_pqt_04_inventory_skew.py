"""Inventory risk and skew: every number in the Avellaneda-Stoikov note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/04-Inventory-Risk-and-Skew.md`.
Independent routes used here:
- reservation bid and ask solved by bisection on the market maker's expected CARA utility, with the
  expectation over the normal terminal price taken by numerical quadrature (not the closed form); their
  average must equal s - q gamma sigma^2 (T - t);
- the spread's liquidity term (2 / gamma) ln(1 + gamma / kappa) as twice the maximizer of
  exp(-kappa d) (1 - exp(-gamma d)), found by golden-section search;
- the inventory drift A e^{-kappa s*/2} (e^{-kappa c q} - e^{kappa c q}) against a seeded simulation of
  Poisson bid and ask fills (five standard errors), and its small-q slope by finite differences;
- residual-variance fractions and the Example 2 hedge in exact fractions and by a seeded bivariate-normal
  simulation with batch-means standard errors (five standard errors).
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_pqt_04_inventory_skew.py`.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

SEED = 41


def rounded(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(value):,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def expected_utility(x: float, q: int, s: float, gamma: float, sigma: float, tau: float) -> float:
    """E[-exp(-gamma (x + q S_T))] with S_T ~ N(s, sigma^2 tau), by quadrature on a fine grid."""
    sd = sigma * np.sqrt(tau)
    z = np.linspace(-12, 12, 200_001)
    dens = np.exp(-0.5 * z**2) / np.sqrt(2 * np.pi)
    vals = -np.exp(-gamma * (x + q * (s + sd * z)))
    return float(np.sum(vals * dens) * (z[1] - z[0]))


def bisect(f, lo: float, hi: float, tol: float = 1e-12) -> float:
    flo = f(lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def reservation_prices(q: int, s: float, gamma: float, sigma: float, tau: float) -> tuple[float, float]:
    base = expected_utility(0.0, q, s, gamma, sigma, tau)
    r_bid = bisect(lambda p: expected_utility(-p, q + 1, s, gamma, sigma, tau) - base, s - 50, s + 50)
    r_ask = bisect(lambda p: expected_utility(p, q - 1, s, gamma, sigma, tau) - base, s - 50, s + 50)
    return r_bid, r_ask


def golden_max(f, lo: float, hi: float) -> float:
    g = (np.sqrt(5) - 1) / 2
    a, b = lo, hi
    for _ in range(200):
        c, d = b - g * (b - a), a + g * (b - a)
        if f(c) > f(d):
            b = d
        else:
            a = c
    return 0.5 * (a + b)


def example_1() -> None:
    print("Example 1: Avellaneda-Stoikov quotes")
    s, gamma, sigma, tau, kappa = 100.0, 0.1, 0.5, 1.0, 1.5
    print(f"    input: S = {s}, gamma = {gamma}, sigma = {sigma}, T - t = {tau}, kappa = {kappa}")
    rounded("sigma^2", sigma**2, "0.25")
    rounded("2 / gamma", 2 / gamma, "20")
    rounded("1 + gamma / kappa", 1 + gamma / kappa, "1.0667")
    rounded("ln(1 + gamma / kappa)", np.log1p(gamma / kappa), "0.06454")
    d_star = golden_max(lambda d: np.exp(-kappa * d) * (1 - np.exp(-gamma * d)), 0.0, 20.0)
    liquidity = 2 * d_star
    rounded("liquidity term, golden-section maximizer x 2", liquidity, "1.2908")
    rounded("liquidity term, closed form", 2 / gamma * np.log1p(gamma / kappa), "1.2908")
    risk = gamma * sigma**2 * tau
    rounded("risk term gamma sigma^2 (T - t)", risk, "0.0250")
    spread = risk + liquidity
    rounded("optimal total spread", spread, "1.3158")
    rounded("half-spread", spread / 2, "0.6579")
    print("  card mkt-pqt-100: total spread across gamma at Example 1's sigma, T - t and kappa")
    grid = {0.05: "1.3241", 0.1: "1.3158", 0.2: "1.3016", 0.5: "1.2757", 1.0: "1.2717"}
    spreads = []
    for g, lit in grid.items():
        d_g = golden_max(lambda d, g=g: np.exp(-kappa * d) * (1 - np.exp(-g * d)), 0.0, 40.0)
        s_g = g * sigma**2 * tau + 2 * d_g
        assert abs(s_g - (g * sigma**2 * tau + 2 / g * np.log1p(g / kappa))) < 1e-6
        rounded(f"spread at gamma = {g}", s_g, lit)
        spreads.append(s_g)
    assert all(a > b for a, b in zip(spreads, spreads[1:], strict=False))
    quoted = {
        0: ("100.00", "99.3421", "100.6579"),
        10: ("99.7500", "99.0921", "100.4079"),
        -10: ("100.2500", "99.5921", "100.9079"),
    }
    for q, (r_lit, b_lit, a_lit) in quoted.items():
        r_bid, r_ask = reservation_prices(q, s, gamma, sigma, tau)
        r = 0.5 * (r_bid + r_ask)
        assert abs(r - (s - q * gamma * sigma**2 * tau)) < 1e-6
        assert abs(r_ask - (s + (1 - 2 * q) * gamma * sigma**2 * tau / 2)) < 1e-6
        assert abs(r_bid - (s - (1 + 2 * q) * gamma * sigma**2 * tau / 2)) < 1e-6
        print(f"  q = {q:+d}: reservation bid {r_bid:.6f}, reservation ask {r_ask:.6f} (utility bisection)")
        rounded("reservation price", r, r_lit)
        rounded("optimal bid", r - spread / 2, b_lit)
        rounded("optimal ask", r + spread / 2, a_lit)
    rounded("inventory penalty for |q| = 10", 10 * gamma * sigma**2 * tau, "0.2500")
    shift_long = 100 * (float(quoted[0][1]) - float(quoted[10][1]))
    shift_short = 100 * (float(quoted[-10][2]) - float(quoted[0][2]))
    rounded("quote drop at q = +10 (cents)", shift_long, "25")
    rounded("quote rise at q = -10 (cents)", shift_short, "25")


def inventory_drift(rng: np.random.Generator) -> None:
    print("Inventory drift under AS quotes")
    A, kappa, gamma, sigma, tau = 140.0, 1.5, 0.1, 0.5, 1.0
    c = gamma * sigma**2 * tau
    s_star = c + 2 / gamma * np.log1p(gamma / kappa)
    for q in (2, 10):
        da, db = s_star / 2 - c * q, s_star / 2 + c * q
        lam_a, lam_b = A * np.exp(-kappa * da), A * np.exp(-kappa * db)
        exact = A * np.exp(-kappa * s_star / 2) * (np.exp(-kappa * c * q) - np.exp(kappa * c * q))
        dt, n = 0.001, 2_000_000
        dq = rng.poisson(lam_b * dt, n) - rng.poisson(lam_a * dt, n)
        est, se = dq.mean() / dt, dq.std(ddof=1) / np.sqrt(n) / dt
        print(f"    q = {q}: drift formula {exact:.4f}, simulated {est:.4f} +/- {se:.4f}")
        assert abs(est - exact) < 5 * se
    h = 1e-6
    slope = (A * np.exp(-kappa * s_star / 2) * (np.exp(-kappa * c * h) - np.exp(kappa * c * h))) / h
    lin = -2 * A * kappa * np.exp(-kappa * s_star / 2) * c
    print(f"    small-q slope: finite difference {slope:.6f}, 2 A kappa e^(-kappa s*/2) gamma sigma^2 (T-t) = {-lin:.6f}")
    assert abs(slope - lin) < 1e-4 * abs(lin)


def hedging(rng: np.random.Generator) -> None:
    print("Residual variance after a minimum-variance hedge")
    rho = Fraction(95, 100)
    rounded("residual variance fraction (%)", (1 - rho**2) * 100, "9.75")
    rounded("variance removed (%)", rho**2 * 100, "90.25")
    fracs = []
    for _ in range(50):
        zh = rng.normal(size=100_000)
        zs = 0.95 * zh + np.sqrt(1 - 0.95**2) * rng.normal(size=100_000)
        b = np.cov(zs, zh)[0, 1] / np.var(zh, ddof=1)
        fracs.append(np.var(zs - b * zh, ddof=1) / np.var(zs, ddof=1))
    frac, se = np.mean(fracs), np.std(fracs, ddof=1) / np.sqrt(len(fracs))
    print(f"    simulated residual fraction (seed {SEED}, batch means) = {frac:.5f} +/- {se:.5f}")
    assert abs(frac - 0.0975) < 5 * se

    print("Example 2: proxy hedge with NQ")
    gmv, limit, beta, corr = 10_000_000, 2_000_000, Fraction(135, 100), Fraction(90, 100)
    print(f"    input: beta = {float(beta)}, rho = {float(corr)}, NQ multiplier $20 (cited: CME contract spec), index 18,000")
    rounded("GMV of 50,000 shares at $200.00", 50_000 * 200, "10,000,000")
    contract = 18_000 * 20
    excess = gmv - limit
    rounded("excess value", excess, "8,000,000")
    rounded("NQ contract value", contract, "360,000")
    rounded("beta x excess value", beta * excess, "10,800,000")
    n_fut = -beta * excess / contract
    rounded("contracts", n_fut, "-30.0")
    rounded("NQ contracts sold short", -n_fut, "30")
    rounded("variance removed on the hedged slice (%)", corr**2 * 100, "81")
    vol_ratio = beta / corr
    rounded("stock vol / index vol", vol_ratio, "1.5")
    pos, hedge = Fraction(10), beta * 8  # $ millions
    rounded("hedge notional ($m)", hedge, "10.8")
    unhedged = pos**2 * vol_ratio**2
    hedged = unhedged - 2 * pos * hedge * beta + hedge**2
    rounded("unhedged variance (index-variance units)", unhedged, "225")
    rounded("hedged variance (index-variance units)", hedged, "50.04")
    rounded("variance removed, whole position (%)", (1 - hedged / unhedged) * 100, "77.76")

    batches, per = 50, 200_000
    ratios = []
    for _ in range(batches):
        rh = rng.normal(0, 0.01, per)
        rs = 0.9 * 1.5 * rh + np.sqrt(1 - 0.81) * 0.015 * rng.normal(size=per)
        ratios.append(np.var(10 * rs - 10.8 * rh) / np.var(10 * rs))
    mean, se = np.mean(ratios), np.std(ratios, ddof=1) / np.sqrt(batches)
    print(f"    simulated hedged / unhedged variance = {mean:.5f} +/- {se:.5f} (closed form {float(hedged / unhedged):.5f})")
    assert abs(mean - float(hedged / unhedged)) < 5 * se


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    example_1()
    inventory_drift(rng)
    hedging(rng)
    print("all inventory-skew numbers check out")
