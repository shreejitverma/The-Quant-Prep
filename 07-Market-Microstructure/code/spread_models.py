"""Spread models: Roll estimator, Glosten-Milgrom quotes, and a two-component spread decomposition.

Backs every number in 03-Spread-Models-Roll-and-Glosten-Milgrom.md.
Run ``python spread_models.py``: each result is printed and asserted.
Simulations use fixed seeds; quoted simulation values are seed-stable.
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a labelled result and assert it is within tol of the expected value."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


def autocov1(x: np.ndarray) -> float:
    """First-order sample autocovariance."""
    d = x - x.mean()
    return float(np.mean(d[1:] * d[:-1]))


def roll_estimate(prices: np.ndarray) -> float:
    """Roll (1984) half-spread estimate c = sqrt(-Cov(dp_t, dp_{t-1})); NaN when the autocovariance is positive."""
    cov = autocov1(np.diff(prices))
    return math.sqrt(-cov) if cov < 0 else float("nan")


def roll_simulation() -> None:
    print("== Roll model ==")
    rng = np.random.default_rng(1)
    n, c, sigma = 200_000, 0.05, 0.10
    m = 100 + np.cumsum(sigma * rng.standard_normal(n))
    q = rng.choice([-1.0, 1.0], size=n)
    p = m + c * q
    dp = np.diff(p)
    check("theoretical Var(dp)", sigma**2 + 2 * c**2, 0.015, 1e-12)
    check("theoretical Cov(dp_t, dp_t-1)", -(c**2), -0.0025, 1e-12)
    check("sample Var(dp)", float(dp.var()), 0.01491, 1e-5)
    check("sample Cov(dp_t, dp_t-1)", autocov1(dp), -0.00247, 1e-5)
    c_hat = roll_estimate(p)
    check("Roll half-spread estimate", c_hat, 0.0497, 1e-4)
    check("Roll spread estimate (2c)", 2 * c_hat, 0.0994, 1e-4)

    # Persistent order flow: q follows a symmetric Markov chain with autocorrelation rho
    rho = 0.5
    stay = rng.random(n) < (1 + rho) / 2
    qp = np.empty(n)
    qp[0] = 1.0
    for t in range(1, n):
        qp[t] = qp[t - 1] if stay[t] else -qp[t - 1]
    pp = m + c * qp
    check("theoretical Roll estimate with rho=0.5: c(1-rho)", c * (1 - rho), 0.025, 1e-12)
    check("Roll estimate with persistent flow", roll_estimate(pp), 0.0249, 1e-4)

    # Short windows: how often is the autocovariance positive so the estimator is undefined?
    window, c_small = 50, 0.02
    trials = 20_000
    pos = 0
    for _ in range(trials):
        mm = np.cumsum(sigma * rng.standard_normal(window + 1))
        qq = rng.choice([-1.0, 1.0], size=window + 1)
        if autocov1(np.diff(mm + c_small * qq)) >= 0:
            pos += 1
    frac = pos / trials
    check("share of 50-trade windows with positive autocovariance (c=0.02, sigma=0.10)", frac, 0.345, 1e-3)


def gm_quotes(v_low: float, v_high: float, pi_high: float, mu: float) -> tuple[float, float]:
    """Glosten-Milgrom bid and ask: conditional expectations of value given a sell or a buy."""
    buy_h, buy_l = mu + (1 - mu) / 2, (1 - mu) / 2
    sell_h, sell_l = (1 - mu) / 2, mu + (1 - mu) / 2
    p_h_buy = pi_high * buy_h / (pi_high * buy_h + (1 - pi_high) * buy_l)
    p_h_sell = pi_high * sell_h / (pi_high * sell_h + (1 - pi_high) * sell_l)
    return v_low + (v_high - v_low) * p_h_sell, v_low + (v_high - v_low) * p_h_buy


def glosten_milgrom() -> None:
    print("== Glosten-Milgrom ==")
    v_low, v_high, pi_high, mu = 95.0, 105.0, 0.4, 0.25
    bid, ask = gm_quotes(v_low, v_high, pi_high, mu)
    mean = v_low + (v_high - v_low) * pi_high
    check("prior mean", mean, 99.0, 1e-12)
    check("P(H | buy)", (ask - v_low) / (v_high - v_low), 0.25 / 0.475, 1e-12)
    check("P(buy | H)", mu + (1 - mu) / 2, 0.625, 1e-12)
    check("P(buy | L)", (1 - mu) / 2, 0.375, 1e-12)
    check("P(H | sell)", (bid - v_low) / (v_high - v_low), 0.15 / 0.525, 1e-12)
    check("P(H | sell) value", (bid - v_low) / (v_high - v_low), 0.285714, 1e-6)
    check("ask", ask, 100.263158, 1e-6)
    check("bid", bid, 97.857143, 1e-6)
    check("spread", ask - bid, 2.406015, 1e-6)
    check("ask minus prior mean", ask - mean, 1.263158, 1e-6)
    check("prior mean minus bid", mean - bid, 1.142857, 1e-6)

    # Zero expected profit: gains from uninformed trades equal losses to informed trades
    buy_h, buy_l = mu + (1 - mu) / 2, (1 - mu) / 2
    sell_h, sell_l = (1 - mu) / 2, mu + (1 - mu) / 2
    profit = 0.0
    for v, pv, pb, ps in ((v_high, pi_high, buy_h, sell_h), (v_low, 1 - pi_high, buy_l, sell_l)):
        profit += pv * (pb * (ask - v) + ps * (v - bid))
    check("market maker expected profit per trade", profit, 0.0, 1e-12)
    uninformed_gain = (1 - mu) * 0.5 * ((ask - mean) + (mean - bid))
    check("expected gain from uninformed per trade", uninformed_gain, 0.902256, 1e-6)

    # Symmetric case pi = 1/2: half-spread = mu (V_H - V_L) / 2
    b2, a2 = gm_quotes(v_low, v_high, 0.5, mu)
    check("symmetric half-spread", (a2 - b2) / 2, mu * (v_high - v_low) / 2, 1e-12)
    check("symmetric half-spread value", (a2 - b2) / 2, 1.25, 1e-12)

    # Learning: true value is V_H; average spread after k trades across paths
    rng = np.random.default_rng(2)
    paths, horizon = 20_000, 50
    pis = np.full(paths, pi_high)
    spreads_at, p_high_at = {}, {}
    for k in range(1, horizon + 1):
        informed = rng.random(paths) < mu
        buy = np.where(informed, True, rng.random(paths) < 0.5)
        lik_h = np.where(buy, buy_h, sell_h)
        lik_l = np.where(buy, buy_l, sell_l)
        pis = pis * lik_h / (pis * lik_h + (1 - pis) * lik_l)
        if k in (10, 25, 50):
            b_k, a_k = gm_quotes(v_low, v_high, pis, mu)
            spreads_at[k] = float(np.mean(a_k - b_k))
            p_high_at[k] = float(pis.mean())
    for k, want_p, want_s in ((10, 0.6504, 1.5996), (25, 0.8225, 0.8565), (50, 0.9340, 0.3242)):
        check(f"mean P(H) after {k} trades", p_high_at[k], want_p, 1e-4)
        check(f"mean spread after {k} trades", spreads_at[k], want_s, 1e-4)


def decomposition() -> None:
    print("== Spread decomposition (MRR-style, iid trade signs) ==")
    rng = np.random.default_rng(3)
    n, theta, phi, su = 200_000, 0.02, 0.03, 0.03
    q = rng.choice([-1.0, 1.0], size=n)
    m = 50 + np.cumsum(theta * q + su * rng.standard_normal(n))
    p = m + phi * q
    dp = np.diff(p)
    x = np.column_stack([q[1:], q[:-1]])
    coef, *_ = np.linalg.lstsq(x, dp, rcond=None)
    theta_hat, phi_hat = coef[0] + coef[1], -coef[1]
    check("coefficient on q_t (theta + phi)", float(coef[0]), 0.0500, 1e-4)
    check("coefficient on q_t-1 (-phi)", float(coef[1]), -0.0300, 1e-4)
    check("adverse selection theta", float(theta_hat), 0.0199, 1e-4)
    check("transitory phi", float(phi_hat), 0.0300, 1e-4)
    check("adverse-selection share of the half-spread", float(theta_hat / (theta_hat + phi_hat)), 0.399, 1e-3)
    check("theoretical Roll estimate sqrt(phi(theta+phi))", math.sqrt(phi * (theta + phi)), 0.0387298, 1e-6)
    check("Roll estimate on the same data", roll_estimate(p), 0.0387, 1e-4)


def card_numbers() -> None:
    print("== Numbers used in the interview cards ==")
    c = math.sqrt(0.0004)
    check("Roll spread from autocovariance -0.0004", 2 * c, 0.04, 1e-12)
    b, a = gm_quotes(48.0, 52.0, 0.5, 0.4)
    check("GM bid, V in {48, 52}, mu = 0.4", b, 49.2, 1e-12)
    check("GM ask, V in {48, 52}, mu = 0.4", a, 50.8, 1e-12)
    coef_now, coef_lag = 0.06, -0.04
    check("transitory phi from lag coefficient", -coef_lag, 0.04, 1e-12)
    check("permanent theta from coefficient sum", coef_now + coef_lag, 0.02, 1e-12)
    check("adverse-selection share", (coef_now + coef_lag) / coef_now, 1 / 3, 1e-12)
    check("Roll with rho = 0.5 as a share of c", (1 - 0.5), 0.5, 1e-12)


if __name__ == "__main__":
    card_numbers()
    roll_simulation()
    glosten_milgrom()
    decomposition()
    print("all spread model checks passed")
