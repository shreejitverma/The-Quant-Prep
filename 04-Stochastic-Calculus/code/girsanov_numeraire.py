"""Girsanov, Radon-Nikodym densities and numeraire changes, checked by Monte Carlo.

Backs every number in 04-Stochastic-Calculus/05-Change-of-Measure-and-Girsanov.md:

1. The Girsanov density Z_T = exp(-theta W_T - theta^2 T / 2): mean 1, variance exp(theta^2 T) - 1, and the drift shift.
2. Importance sampling of P(W_1 > 4) by a Girsanov drift shift.
3. Stock (share) measure: N(d1) as a probability, and the Margrabe exchange option priced with S2 as numeraire.
4. T-forward measure in the Vasicek model: E^T[r_T] = f(0, T), and a zero-coupon bond option priced three ways.
5. Annuity (swap) measure: the forward swap rate is an annuity-measure martingale; a payer swaption by Monte Carlo
   against the Jamshidian closed form, and its Black implied volatility.
6. Quanto forward: the drift adjustment -rho sigma_S sigma_X checked by simulating under the foreign measure.

Run from the repo root: uv run --no-project --with numpy python 04-Stochastic-Calculus/code/girsanov_numeraire.py
"""

from __future__ import annotations

import math

import numpy as np

SQRT2 = math.sqrt(2.0)


def ncdf(x: float) -> float:
    """Standard normal CDF via erfc (keeps relative accuracy in the left tail)."""
    return 0.5 * math.erfc(-x / SQRT2)


def bs_call(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
    sd = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / sd
    return S * math.exp(-q * T) * ncdf(d1) - K * math.exp(-r * T) * ncdf(d1 - sd)


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a quoted number and assert it against the value the note quotes."""
    print(f"{name:58s} {value:.6g}")
    assert abs(value - expected) <= tol, f"{name}: {value} vs {expected} (tol {tol})"
    return value


def mc_mean(x: np.ndarray) -> tuple[float, float]:
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(x.size))


# ----------------------------------------------------------------------------------------------
# 1. The Girsanov density
# ----------------------------------------------------------------------------------------------


def girsanov_density(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Girsanov density in a simulation'; cards sc-girsanov-gaussian-shift, sc-girsanov-density-variance."""
    print("\n1. Girsanov density, theta = 0.4, T = 1")
    theta, T, n = 0.4, 1.0, 2_000_000
    W = rng.standard_normal(n) * math.sqrt(T)
    Z = np.exp(-theta * W - 0.5 * theta**2 * T)
    check("E^P[Z_T] (exact 1)", float(Z.mean()), 0.9999, 5e-5)
    check("Var^P(Z_T) exact exp(theta^2 T) - 1", math.exp(theta**2 * T) - 1, 0.1735, 5e-5)
    check("Var^P(Z_T) Monte Carlo", float(Z.var()), 0.1735, 5e-5)
    # Under Q, W^Q_T = W_T + theta T is N(0, T): mean 0, second moment T, under the weights Z
    WQ = W + theta * T
    check("E^Q[W_T + theta T] = E^P[Z (W_T + theta T)]", float((Z * WQ).mean()), 0.0001, 5e-5)
    check("E^Q[(W_T + theta T)^2]", float((Z * WQ**2).mean()), 1.0001, 5e-5)
    check("E^Q[W_T] (drift -theta T)", float((Z * W).mean()), -0.3999, 5e-5)
    # The weights degenerate as theta grows: variance exp(theta^2 T) - 1
    check("Var^P(Z_T) for theta = 3", math.exp(9.0) - 1, 8102.08, 5e-3)
    check("  rounded to an integer (card)", math.exp(9.0) - 1, 8102, 0.5)


# ----------------------------------------------------------------------------------------------
# 2. Importance sampling
# ----------------------------------------------------------------------------------------------


def importance_sampling(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Importance sampling a three-in-a-hundred-thousand event'; card sc-girsanov-importance-sampling."""
    print("\n2. Importance sampling P(W_1 > 4)")
    exact = 0.5 * math.erfc(4.0 / SQRT2)
    check("exact P(Z > 4)", exact, 3.167e-5, 5e-9)
    n = 100_000
    z = rng.standard_normal(n)
    plain = (z > 4.0).astype(float)
    p_mean, p_se = mc_mean(plain)
    check("plain MC hits in 100,000 draws", float(plain.sum()), 1.0, 0.0)
    check("plain MC relative standard error (theory)", math.sqrt((1 - exact) / (n * exact)), 0.562, 5e-4)
    check("  as a percentage (card)", 100 * math.sqrt((1 - exact) / (n * exact)), 56, 0.5)
    # Sample X ~ N(4, 1) and weight by dP/dQ = exp(-4 X + 8)
    mu = 4.0
    x = rng.standard_normal(n) + mu
    w = np.where(x > 4.0, np.exp(-mu * x + 0.5 * mu * mu), 0.0)
    is_mean, is_se = mc_mean(w)
    check("IS estimate x 1e5", is_mean * 1e5, 3.157, 5e-4)
    assert abs(is_mean - exact) < 4 * is_se
    check("IS relative standard error", is_se / is_mean, 0.0067, 5e-5)
    check("  as a percentage (card)", 100 * is_se / is_mean, 0.67, 5e-3)
    var_ratio = exact * (1 - exact) / (is_se**2 * n)
    check("variance reduction factor", var_ratio, 7050, 5)
    _ = p_mean, p_se


# ----------------------------------------------------------------------------------------------
# 3. Stock measure: N(d1) and the Margrabe exchange option
# ----------------------------------------------------------------------------------------------


def stock_measure(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Exchange option with the second asset as numeraire';
    cards sc-numeraire-margrabe, sc-numeraire-drift-rule."""
    print("\n3. Stock measure")
    S0, K, T, r, sig = 100.0, 105.0, 0.5, 0.05, 0.25
    d1 = (math.log(S0 / K) + (r + 0.5 * sig**2) * T) / (sig * math.sqrt(T))
    check("N(d1)", ncdf(d1), 0.4816, 5e-5)
    n = 2_000_000
    z = rng.standard_normal(n)
    ST = S0 * np.exp((r - 0.5 * sig**2) * T + sig * math.sqrt(T) * z)
    # Q^S(S_T > K) = E^Q[(S_T / (S_0 e^{rT})) 1{S_T > K}]
    check("Q^S(S_T > K) by reweighting Q-paths", float((ST / (S0 * math.exp(r * T)) * (ST > K)).mean()), 0.4814, 5e-5)
    # Directly under Q^S: log-drift r + sigma^2 / 2
    STs = S0 * np.exp((r + 0.5 * sig**2) * T + sig * math.sqrt(T) * z)
    check("Q^S(S_T > K) simulating log-drift r + sigma^2/2", float((STs > K).mean()), 0.4812, 5e-5)

    print("   Margrabe exchange option (S1_T - S2_T)^+")
    S1, S2, s1, s2, rho, T, r = 100.0, 100.0, 0.30, 0.20, 0.5, 1.0, 0.05
    sig = math.sqrt(s1 * s1 + s2 * s2 - 2 * rho * s1 * s2)
    check("exchange-ratio vol sqrt(s1^2 + s2^2 - 2 rho s1 s2)", sig, 0.2646, 5e-5)
    d1 = (math.log(S1 / S2) + 0.5 * sig**2 * T) / (sig * math.sqrt(T))
    margrabe = S1 * ncdf(d1) - S2 * ncdf(d1 - sig * math.sqrt(T))
    check("Margrabe price", margrabe, 10.5243, 5e-5)
    check("  Margrabe price to two decimals (card)", margrabe, 10.52, 5e-3)
    n = 1_000_000
    z1 = rng.standard_normal(n)
    z2 = rho * z1 + math.sqrt(1 - rho * rho) * rng.standard_normal(n)
    prices = []
    for r_test in (0.05, 0.0):
        X1 = S1 * np.exp((r_test - 0.5 * s1 * s1) * T + s1 * math.sqrt(T) * z1)
        X2 = S2 * np.exp((r_test - 0.5 * s2 * s2) * T + s2 * math.sqrt(T) * z2)
        price, se = mc_mean(math.exp(-r_test * T) * np.maximum(X1 - X2, 0.0))
        check(f"MC under Q with r = {r_test}", price, 10.563, 5e-4)
        assert abs(price - margrabe) < 4 * se
        check(f"  standard error (r = {r_test})", se, 0.018, 5e-4)
        prices.append(price)
    # Both legs are assets: e^{rT} scales X1 and X2 and the discount removes it, path by path
    assert abs(prices[0] - prices[1]) < 1e-12 * prices[1], prices
    print("   MC prices for r = 5% and r = 0 agree to within 1e-12 relative")


# ----------------------------------------------------------------------------------------------
# 4 and 5. Vasicek: T-forward and annuity measures
# ----------------------------------------------------------------------------------------------

KAPPA, THETA, SIGMA, R0 = 0.3, 0.05, 0.01, 0.03


def vas_B(tau: float | np.ndarray) -> float | np.ndarray:
    return (1.0 - np.exp(-KAPPA * tau)) / KAPPA


def vas_bond(tau: float | np.ndarray, r: float | np.ndarray) -> float | np.ndarray:
    """Vasicek zero-coupon bond P(t, t + tau) given r_t = r."""
    B = vas_B(tau)
    lnA = (THETA - SIGMA**2 / (2 * KAPPA**2)) * (B - tau) - SIGMA**2 * B**2 / (4 * KAPPA)
    return np.exp(lnA - B * r)


def vas_joint(T: float) -> tuple[np.ndarray, np.ndarray]:
    """Mean and covariance of (r_T, I_T = int_0^T r ds) under Q, both Gaussian."""
    e1, e2 = math.exp(-KAPPA * T), math.exp(-2 * KAPPA * T)
    m_r = THETA + (R0 - THETA) * e1
    m_i = THETA * T + (R0 - THETA) * (1 - e1) / KAPPA
    v_r = SIGMA**2 / (2 * KAPPA) * (1 - e2)
    v_i = SIGMA**2 / KAPPA**2 * (T - 2 * (1 - e1) / KAPPA + (1 - e2) / (2 * KAPPA))
    c = SIGMA**2 / (2 * KAPPA**2) * (1 - e1) ** 2
    return np.array([m_r, m_i]), np.array([[v_r, c], [c, v_i]])


def zcb_option(T: float, S: float, K: float, call: bool) -> float:
    """Option at T on the bond maturing at S: Black formula under the T-forward measure."""
    sp = SIGMA / KAPPA * (1 - math.exp(-KAPPA * (S - T))) * math.sqrt((1 - math.exp(-2 * KAPPA * T)) / (2 * KAPPA))
    PT, PS = float(vas_bond(T, R0)), float(vas_bond(S, R0))
    h = math.log(PS / (K * PT)) / sp + 0.5 * sp
    if call:
        return PS * ncdf(h) - K * PT * ncdf(h - sp)
    return K * PT * ncdf(-h + sp) - PS * ncdf(-h)


def forward_measure(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Forward measure in Vasicek: bond option three ways';
    cards sc-numeraire-forward-rate-expectation, sc-numeraire-vasicek-bond-option."""
    print(f"\n4. T-forward measure, Vasicek kappa={KAPPA}, theta={THETA}, sigma={SIGMA}, r0={R0}")
    T, S = 1.0, 5.0
    PT, PS = float(vas_bond(T, R0)), float(vas_bond(S, R0))
    check("P(0,1)", PT, 0.967821, 5e-7)
    check("P(0,5)", PS, 0.820839, 5e-7)
    fwd = PS / PT
    check("forward bond price P(0,5)/P(0,1)", fwd, 0.848131, 5e-7)
    h = 1e-5
    f0T = -(math.log(float(vas_bond(T + h, R0))) - math.log(float(vas_bond(T - h, R0)))) / (2 * h)
    mean, cov = vas_joint(T)
    check("E^Q[r_1]", float(mean[0]), 0.035184, 5e-7)
    check("instantaneous forward f(0,1)", f0T, 0.035146, 5e-7)
    check("E^T[r_1] = E^Q[r_1] - Cov(r_1, I_1)", float(mean[0] - cov[0, 1]), f0T, 1e-9)
    check("Cov(r_1, I_1) in bp (E^Q[r_1] - f(0,1))", float(cov[0, 1]) * 1e4, 0.373, 5e-4)

    n = 2_000_000
    L = np.linalg.cholesky(cov)
    draws = mean + rng.standard_normal((n, 2)) @ L.T
    rT, IT = draws[:, 0], draws[:, 1]
    disc = np.exp(-IT)
    check("MC E^Q[exp(-I_1)] vs P(0,1)", float(disc.mean()), PT, 2e-5)
    PTS = vas_bond(S - T, rT)
    K = 0.85
    closed = zcb_option(T, S, K, call=True)
    check("ZCB call K=0.85 closed form (forward measure Black)", closed, 0.0057565, 5e-8)
    q_price, q_se = mc_mean(disc * np.maximum(PTS - K, 0.0))
    check("  MC under Q (stochastic discounting)", q_price, 0.0057584, 5e-8)
    # Under Q^T the short rate r_T is Gaussian with mean shifted by -Cov(r_T, I_T); no discounting inside
    rT_fwd = mean[0] - cov[0, 1] + math.sqrt(cov[0, 0]) * rng.standard_normal(n)
    PTS_f = vas_bond(S - T, rT_fwd)
    check("  E^T[P(1,5)] = forward bond price", float(PTS_f.mean()), 0.848149, 5e-7)
    assert abs(PTS_f.mean() - fwd) < 4 * PTS_f.std() / math.sqrt(n)
    t_price, t_se = mc_mean(PT * np.maximum(PTS_f - K, 0.0))
    check("  MC under Q^T: P(0,1) E^T[(P(1,5) - K)^+]", t_price, 0.0057683, 5e-8)
    check("  standard error under Q", q_se, 6.5e-6, 5e-8)
    assert abs(q_price - closed) < 4 * q_se
    check("  standard error under Q^T", t_se, 6.5e-6, 5e-8)
    assert abs(t_price - closed) < 4 * t_se


def annuity_measure(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Annuity measure: a 1y x 4y swaption';
    cards sc-numeraire-swaption-annuity, sc-numeraire-swap-rate-under-q."""
    print("\n5. Annuity measure: 1y x 4y annual payer swaption in Vasicek")
    T0, pay = 1.0, np.array([2.0, 3.0, 4.0, 5.0])
    P0 = np.array([float(vas_bond(t, R0)) for t in np.r_[T0, pay]])
    A0 = float(P0[1:].sum())
    S0 = (P0[0] - P0[-1]) / A0
    check("annuity A(0)", A0, 3.507230, 5e-7)
    check("forward swap rate S(0)", S0, 0.041908, 5e-7)
    K = S0
    # Jamshidian: find r* with sum c_i P(T0, T_i; r*) = 1, then a portfolio of zero-coupon puts
    c = np.full(pay.size, K)
    c[-1] += 1.0
    lo, hi = -1.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        val = float((c * vas_bond(pay - T0, mid)).sum())
        lo, hi = (mid, hi) if val > 1.0 else (lo, mid)
    rstar = 0.5 * (lo + hi)
    X = vas_bond(pay - T0, rstar)
    jam = float(sum(ci * zcb_option(T0, Ti, float(Xi), call=False) for ci, Ti, Xi in zip(c, pay, X, strict=True)))
    check("payer swaption (Jamshidian), per unit notional", jam, 0.0074500, 5e-8)

    n = 2_000_000
    mean, cov = vas_joint(T0)
    draws = mean + rng.standard_normal((n, 2)) @ np.linalg.cholesky(cov).T
    rT, IT = draws[:, 0], draws[:, 1]
    bonds = vas_bond((pay - T0)[None, :], rT[:, None])
    AT = bonds.sum(axis=1)
    ST = (1.0 - bonds[:, -1]) / AT
    disc = np.exp(-IT)
    mc, se = mc_mean(disc * AT * np.maximum(ST - K, 0.0))
    check("  MC under Q: E^Q[D A_T (S_T - K)^+]", mc, 0.0074434, 5e-8)
    check("  standard error", se, 7.6e-6, 5e-8)
    assert abs(mc - jam) < 4 * se
    # Annuity measure weights dQ^A/dQ = D(T0) A(T0) / A(0): swap rate is a martingale
    wA = disc * AT / A0
    check("  E^A[1] (weights integrate to 1)", float(wA.mean()), 1.0000, 5e-5)
    check("  E^A[S_T] = S(0)", float((wA * ST).mean()), 0.041906, 5e-7)
    check("  E^Q[S_T] without the annuity weights (biased)", float(ST.mean()), 0.042004, 5e-7)
    check("  E^Q[S_T] - S(0) in bp", (float(ST.mean()) - S0) * 1e4, 0.96, 5e-3)
    check("  swaption price in bp of notional", jam * 1e4, 74.50, 5e-3)
    # Black implied vol under the annuity measure: price = A0 * Black(S0, K, sigma, T0)
    lo, hi = 1e-4, 2.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        sd = mid * math.sqrt(T0)
        black = A0 * (S0 * ncdf(0.5 * sd) - K * ncdf(-0.5 * sd))
        lo, hi = (mid, hi) if black < jam else (lo, mid)
    check("  Black implied vol of the ATM swaption", 0.5 * (lo + hi), 0.1271, 5e-5)
    normal_vol = jam / A0 / math.sqrt(T0 / (2 * math.pi))
    check("  normal (Bachelier) vol in bp", normal_vol * 1e4, 53.25, 5e-3)


# ----------------------------------------------------------------------------------------------
# 6. Quanto forward
# ----------------------------------------------------------------------------------------------


def quanto(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Quanto forward'; card sc-numeraire-quanto-drift."""
    print("\n6. Quanto forward: foreign index paid in domestic currency at a fixed rate")
    S0, rf, rd, q, sS, sX, rho, T = 100.0, 0.005, 0.04, 0.02, 0.20, 0.10, 0.3, 1.0
    adj = -rho * sS * sX
    check("drift adjustment -rho sigma_S sigma_X", adj, -0.006, 1e-12)
    fq = S0 * math.exp((rf - q + adj) * T)
    check("quanto forward", fq, 97.9219, 5e-5)
    check("  quanto forward to two decimals (card)", fq, 97.92, 5e-3)
    check("ordinary (foreign-currency) forward", S0 * math.exp((rf - q) * T), 98.5112, 5e-5)
    check("  ordinary forward to two decimals (card)", S0 * math.exp((rf - q) * T), 98.51, 5e-3)
    # Simulate under the foreign measure Q^f: S has drift rf - q; X (domestic per foreign) has drift rd - rf + sX^2
    n = 2_000_000
    z1 = rng.standard_normal(n)
    z2 = rho * z1 + math.sqrt(1 - rho * rho) * rng.standard_normal(n)
    ST = S0 * np.exp((rf - q - 0.5 * sS * sS) * T + sS * math.sqrt(T) * z1)
    XT_over_X0 = np.exp((rd - rf + sX * sX - 0.5 * sX * sX) * T + sX * math.sqrt(T) * z2)
    dQd_dQf = math.exp((rd - rf) * T) / XT_over_X0
    check("  E^f[dQd/dQf] = 1", float(dQd_dQf.mean()), 1.0001, 5e-5)
    check("  E^d[S_T] = E^f[S_T dQd/dQf]", float((ST * dQd_dQf).mean()), 97.919, 5e-4)


def main() -> None:
    rng = np.random.default_rng(20261016)
    girsanov_density(rng)
    importance_sampling(rng)
    stock_measure(rng)
    forward_measure(rng)
    annuity_measure(rng)
    quanto(rng)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
