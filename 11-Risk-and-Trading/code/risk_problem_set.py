"""Risk problem set: every number in 11-Risk-and-Trading/17-Risk-Problem-Set.md.

Each problem recomputes its answer from the stated inputs and checks it against an independent route (a closed form
against a simulation, a short-cut against the full formula, an Euler sum against brute-force differences).
Functions are reused from the section's other scripts: risk_sensitivities.py, risk_decomposition.py,
risk_ccr_analytics.py and risk_liquidity_model.py.  Simulations use fixed seeds and are quoted as "about".

Run: python 11-Risk-and-Trading/code/risk_problem_set.py
"""

from __future__ import annotations

import math

import numpy as np
from drawdowns import asymptotic_mdd, expected_mdd
from risk_ccr_analytics import collateralised_ee_closed, effective_ee, effective_epe, ncdf, ninv
from risk_decomposition import Z95, cov_matrix, erc_newton, euler_normal, normal_var
from risk_liquidity_model import Z99, bachelier_put, black_put, horizon_variance_factor
from risk_sensitivities import bs_call, bs_greeks


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.10g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def npdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# Problem 1 (card risk-full-vs-half-kelly-drawdown)
def problem_kelly() -> None:
    print("\n[Problem: Kelly sizing, excess return 12%, vol 16%]")
    mu, sig = 0.12, 0.16
    f_star = mu / sig**2
    check("full Kelly leverage", f_star, 4.6875, 1e-12)
    check("Sharpe ratio", mu / sig, 0.75, 1e-12)

    def growth(f: float) -> float:
        return f * mu - 0.5 * f * f * sig * sig

    check("growth at full Kelly", growth(f_star), 0.28125, 1e-12)
    check("growth at half Kelly", growth(0.5 * f_star), 0.2109375, 1e-12)
    check("half-Kelly leverage", 0.5 * f_star, 2.34375, 1e-12)
    check("half-Kelly volatility", 0.5 * f_star * sig, 0.375, 1e-12)
    check("growth at twice Kelly", growth(2.0 * f_star), 0.0, 1e-12)
    for c, p_half, p_hd in ((1.0, 0.5, 1.0 / 3.0), (0.5, 0.125, 1.0 / 9.0)):
        f = c * f_star
        m, v = growth(f), (f * sig) ** 2  # log-wealth drift and variance
        theta = 2.0 * m / v
        u = math.log(2.0)
        # Brownian motion with drift: P(hit -u before +u) = (1 - e^{-theta u}) / (e^{theta u} - e^{-theta u})
        p_first = (1.0 - math.exp(-theta * u)) / (math.exp(theta * u) - math.exp(-theta * u))
        check(f"exponent 2/c - 1 at c = {c}", theta, 2.0 / c - 1.0, 1e-12)
        check(f"P(ever fall to half the starting capital), c = {c}", math.exp(-theta * u), p_half, 1e-12)
        check(f"P(halve before doubling), c = {c}", p_first, p_hd, 1e-12)
    # Simulation check for full Kelly: log wealth is Brownian with drift S^2/2 and variance S^2 per year
    rng = np.random.default_rng(3)
    n, dt = 20_000, 1.0 / 2520.0
    m, s = 0.5 * 0.75**2, 0.75
    x = np.zeros(n)
    done = np.zeros(n, dtype=bool)
    down = np.zeros(n, dtype=bool)
    for _ in range(200_000):
        idx = ~done
        if not idx.any():
            break
        x[idx] += m * dt + s * math.sqrt(dt) * rng.standard_normal(int(idx.sum()))
        hit_dn = idx & (x <= -math.log(2.0))
        hit_up = idx & (x >= math.log(2.0))
        down |= hit_dn
        done |= hit_dn | hit_up
    check("simulated P(halve before doubling), full Kelly (about)", float(down.mean()), 1.0 / 3.0, 0.012)


# Problem 2 (card risk-var-vs-es-coherence)
def problem_var_es() -> None:
    print("\n[Problem: 50m book, 1.2% daily vol, normal]")
    sd = 50e6 * 0.012
    z = ninv(0.99)
    check("z_0.99", z, 2.326348, 5e-7)
    check("99% VaR", z * sd, 1_395_809, 1.0)
    check("ES multiplier phi(z) / 0.01", npdf(z) / 0.01, 2.665214, 5e-7)
    check("99% ES", npdf(z) / 0.01 * sd, 1_599_128, 1.0)
    check("97.5% ES multiplier", npdf(ninv(0.975)) / 0.025, 2.337803, 5e-7)
    # Brute-force ES by quadrature of the tail quantile function: ES = (1 / 0.01) integral_{0.99}^{1} VaR_u du
    us = np.linspace(0.99, 1.0, 200_001)[1:-1]
    qs = np.array([ninv(float(u)) for u in us[::100]])
    es_quad = float(np.mean(qs))
    check("ES multiplier by averaging tail quantiles (about)", es_quad, 2.665, 0.002)


# Problem 3 (card risk-fhs-volatility-updating)
def problem_fhs() -> None:
    print("\n[Problem: filtered historical simulation, today's vol 2.2%]")
    now = 0.022
    for r, vol, exp_r in ((-0.03, 0.01, -0.066), (-0.045, 0.03, -0.033)):
        check(f"filtered return for {r} at vol {vol}", r * now / vol, exp_r, 1e-12)


# Problem 4 (card risk-reverse-stress-testing-mahalanobis)
def problem_reverse_stress() -> None:
    print("\n[Problem: most plausible scenario losing 2.5m; P&L = 20m x1 - 50k x2, sd 1% and 8bp, correlation 0.2]")
    delta = np.array([20e6, -50e3])
    sd = np.array([0.01, 8.0])
    cov = np.outer(sd, sd) * np.array([[1.0, 0.2], [0.2, 1.0]])
    loss = 2.5e6
    s2 = float(delta @ cov @ delta)
    x_star = -loss * (cov @ delta) / s2
    dist = loss / math.sqrt(s2)
    check("equity move", x_star[0], -0.017857, 5e-7)
    check("yield move (bp)", x_star[1], 42.857, 5e-4)
    check("P&L at the scenario", float(delta @ x_star), -2.5e6, 1e-6)
    check("Mahalanobis distance", dist, 6.0994, 5e-4)
    check("equity move in sds", x_star[0] / sd[0], -1.8, 0.05)
    check("yield move in sds", x_star[1] / sd[1], 5.4, 0.05)
    # Brute force: smallest Mahalanobis radius along 3,600 directions that reaches the loss
    chol = np.linalg.cholesky(cov)
    best = math.inf
    for a in np.linspace(0.0, 2.0 * math.pi, 3600, endpoint=False):
        u = np.array([math.cos(a), math.sin(a)])
        slope = float(delta @ (chol @ u))
        if slope < 0.0:
            best = min(best, loss / -slope)
    check("brute-force minimum distance over directions minus closed form", best - dist, 0.0, 1e-5)
    check("one-dimensional tail probability 1 - Phi(d) x 1e10", (1.0 - ncdf(dist)) * 1e10, 5.32, 0.01)


# Problem 5 (card risk-expected-maximum-drawdown-analytics)
def problem_mdd() -> None:
    print("\n[Problem: expected maximum drawdown, Sharpe 1.2, vol 12% (log units)]")
    sig, sharpe = 0.12, 1.2
    mu = sharpe * sig
    for t, exp_exact, exp_asym in ((2.0, 0.1319, 0.1164), (10.0, 0.2022, 0.1969)):
        exact = expected_mdd(t, mu, sig)
        asym = asymptotic_mdd(t, mu, sig)
        check(f"exact E[MDD], T = {t}", exact, exp_exact, 5e-5)
        check(f"Magdon-Ismail asymptote, T = {t}", asym, exp_asym, 5e-5)
        check(
            f"same asymptote in the form (sigma / 2S)(ln(S^2 T / 2) + 1.9635), T = {t}",
            sig / (2 * sharpe) * (math.log(sharpe**2 * t / 2) + 4 * 0.49088),
            asym,
            1e-12,
        )
    check("asymptote / exact at T = 2", asymptotic_mdd(2.0, mu, sig) / expected_mdd(2.0, mu, sig), 0.8825, 5e-4)
    check("zero drift, sqrt(pi / 2) sigma sqrt(T), T = 2", math.sqrt(math.pi / 2) * sig * math.sqrt(2.0), 0.2127, 5e-5)
    check("zero drift by the exact series, T = 2", expected_mdd(2.0, 0.0, sig), 0.2127, 5e-4)


# Problem 6 (card risk-vanna-volga-pnl-attribution)
def problem_greek_attribution() -> None:
    print("\n[Problem: 1,000 reference calls, spot +2, vol -2.5 points, one day: Taylor attribution against full revaluation]")
    q, ds, dv, dt = 1000.0, 2.0, -0.025, 1.0 / 252.0
    g = bs_greeks()
    t1 = 1.0 - dt
    full = q * (bs_call(100.0 + ds, 100.0, 0.05, 0.2 + dv, t1) - bs_call(100.0, 100.0, 0.05, 0.2, 1.0))
    theta = -(bs_call(100.0, 100.0, 0.05, 0.2, 1.0) - bs_call(100.0, 100.0, 0.05, 0.2, t1))
    terms = {
        "delta": q * g["delta"] * ds,
        "gamma": q * 0.5 * g["gamma"] * ds * ds,
        "vega": q * g["vega"] * dv,
        "vanna": q * g["vanna"] * ds * dv,
        "volga": q * 0.5 * g["volga"] * dv * dv,
        "theta": q * theta,
    }
    for k, v in terms.items():
        print(f"  {k}: {v:,.2f}")
    explained = sum(terms.values())
    check("delta P&L", terms["delta"], 1_273.66, 0.01)
    check("gamma P&L", terms["gamma"], 37.52, 0.01)
    check("vega P&L", terms["vega"], -938.10, 0.01)
    check("vanna P&L", terms["vanna"], 14.07, 0.01)
    check("volga P&L", terms["volga"], 3.08, 0.01)
    check("theta P&L (one day, full revaluation in time)", terms["theta"], -25.47, 0.01)
    check("full revaluation P&L", full, 373.83, 0.01)
    check("unexplained with vanna and volga", full - explained, 9.06, 0.01)
    check("unexplained without vanna and volga", full - (explained - terms["vanna"] - terms["volga"]), 26.21, 0.01)


# Problem 7 (card risk-black-scholes-daily-breakeven-rule-of-16)
def problem_breakeven() -> None:
    print("\n[Problem: delta-hedged long gamma, S = 500, gamma 800, implied vol 18%]")
    s0, gam, vol = 500.0, 800.0, 0.18
    theta_day = 0.5 * vol * vol * s0 * s0 * gam / 252.0
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 0.5 * gam * mid * mid < theta_day:
            lo = mid
        else:
            hi = mid
    check("daily theta from the PDE, 1/2 sigma^2 S^2 gamma / 252", theta_day, 12_857.14, 0.01)
    check("break-even move solved numerically", 0.5 * (lo + hi), 5.6695, 5e-5)
    check("closed form sigma S / sqrt(252)", vol * s0 / math.sqrt(252.0), 5.6695, 5e-5)
    check("rule of 16, sigma S / 16", vol * s0 / 16.0, 5.625, 1e-12)
    check("sqrt(252)", math.sqrt(252.0), 15.875, 5e-4)


# Problem 8 (card risk-pca-yield-curve-factor-shocks)
def problem_pca() -> None:
    print("\n[Problem: PCA eigenvalues 0.000180, 0.000018, 0.000002; +1.5 sd level shock]")
    lam = np.array([0.000180, 0.000018, 0.000002])
    shares = lam / lam.sum()
    check("PC1 share", shares[0], 0.90, 1e-12)
    check("PC2 share", shares[1], 0.09, 1e-12)
    v1 = np.ones(3) / math.sqrt(3.0)
    shock = 1.5 * math.sqrt(lam[0]) * v1
    check("level loading 1 / sqrt(3)", v1[0], 0.57735, 5e-6)
    check("level sd sqrt(lambda_1)", math.sqrt(lam[0]), 0.013416, 5e-7)
    check("shock per tenor (bp)", shock[0] * 1e4, 116.19, 0.01)
    # The factor scenario has Mahalanobis distance 1.5 under the covariance it came from
    q, _ = np.linalg.qr(np.column_stack([v1, [1.0, 0.0, -1.0], [1.0, -2.0, 1.0]]))
    cov = q @ np.diag(lam) @ q.T
    check("Mahalanobis distance of the level shock", math.sqrt(float(shock @ np.linalg.solve(cov, shock))), 1.5, 1e-9)


# Problem 9 (cards risk-forward-vs-central-difference, risk-fd-regulatory-forward-bump)
def problem_bumps() -> None:
    print("\n[Problem: delta of the reference call by forward and central 1% bumps]")
    g = bs_greeks()
    h = 1.0
    fwd = (bs_call(101.0, 100.0, 0.05, 0.2, 1.0) - bs_call(100.0, 100.0, 0.05, 0.2, 1.0)) / h
    cen = (bs_call(101.0, 100.0, 0.05, 0.2, 1.0) - bs_call(99.0, 100.0, 0.05, 0.2, 1.0)) / (2 * h)
    check("forward-bump delta", fwd, 0.646125, 5e-7)
    check("central-bump delta", cen, 0.636745, 5e-7)
    check("forward error / (gamma h / 2)", (fwd - g["delta"]) / (0.5 * g["gamma"] * h), 0.9907, 5e-4)
    check("forward error / central error", (fwd - g["delta"]) / abs(cen - g["delta"]), 108.1, 0.1)
    check("central error / (speed h^2 / 6)", (cen - g["delta"]) / (g["speed"] * h * h / 6.0), 0.9996, 5e-4)


# Problem 10 (cards risk-diagonal-vs-cross-gamma, risk-aad-cost-count)
def problem_bump_counts() -> None:
    print("\n[Problem: pricing calls for a 50-factor book, counted by running central differences on a counting pricer]")
    n = 50
    calls = {"n": 0}

    def pricer(x: list[float]) -> float:
        calls["n"] += 1
        return float(sum(xi * xi for xi in x))

    x0, h = [1.0] * n, 1e-3
    calls["n"] = 0
    for i in range(n):
        up, dn = list(x0), list(x0)
        up[i] += h
        dn[i] -= h
        pricer(up)
        pricer(dn)
    grad_calls = calls["n"]
    calls["n"] = 0
    pricer(x0)  # base value, shared by every diagonal term
    for i in range(n):
        for d in (h, -h):
            y = list(x0)
            y[i] += d
            pricer(y)
        for j in range(i + 1, n):
            for di, dj in ((h, h), (h, -h), (-h, h), (-h, -h)):
                y = list(x0)
                y[i] += di
                y[j] += dj
                pricer(y)
    hess_calls = calls["n"]
    check("central gradient calls", grad_calls, 100, 0)
    check("full central Hessian calls, 2N^2 + 1", hess_calls, 5_001, 0)
    check("formula 2N^2 + 1 minus the count", 2 * n * n + 1 - hess_calls, 0, 0)


# Problem 11 (card risk-taylor-proxy-tail-underestimation, risk-short-gamma-proxy-crash)
def problem_short_put_crash() -> None:
    print("\n[Problem: short 1-year ATM put (S = K = 100, r = 5%, vol 20%), spot falls 25 with vol unchanged]")

    def put(s: float) -> float:
        return bs_call(s, 100.0, 0.05, 0.2, 1.0) - s + 100.0 * math.exp(-0.05)

    g = bs_greeks()
    p_delta, p_gamma = g["delta"] - 1.0, g["gamma"]
    ds = -25.0
    full = -(put(100.0 + ds) - put(100.0))
    prox = -(p_delta * ds + 0.5 * p_gamma * ds * ds)
    check("put value", put(100.0), 5.5735, 5e-4)
    check("short put full-revaluation P&L", full, -15.5166, 5e-4)
    check("short put delta-gamma P&L", prox, -14.9424, 5e-5)
    check("proxy understates the loss by", prox - full, 0.5743, 5e-4)
    check("speed (third derivative) of the put, equal to the call's", g["speed"], -0.000516, 5e-7)


# Problem 12 (cards risk-euler-allocation-homogeneity, risk-marginal-vs-component-var)
def problem_euler() -> None:
    print("\n[Problem: 80m at 15% vol and 20m at 25% vol, correlation 0.4, 95% VaR]")
    x = np.array([80e6, 20e6])
    cov = cov_matrix(np.array([0.15, 0.25]), np.array([[1.0, 0.4], [0.4, 1.0]]))
    var, marg, comp = euler_normal(x, cov, Z95)
    check("portfolio volatility", math.sqrt(float(x @ cov @ x)) / 1e8, 0.147309, 5e-7)
    check("VaR", var, 24_230_207, 1.0)
    check("marginal VaR asset 1 per dollar", marg[0], 0.234486, 5e-7)
    check("marginal VaR asset 2 per dollar", marg[1], 0.273567, 5e-7)
    check("component VaR asset 1", comp[0], 18_758_870, 1.0)
    check("component VaR asset 2", comp[1], 5_471_337, 1.0)
    h = 1_000.0
    up, dn = x.copy(), x.copy()
    up[1] += h
    dn[1] -= h
    check(
        "brute-force marginal VaR asset 2 minus Euler", (normal_var(up, cov, Z95) - normal_var(dn, cov, Z95)) / (2 * h) - marg[1], 0.0, 1e-9
    )


# Problem 13 (cards risk-erc-two-asset-any-correlation, risk-erc-two-asset-inverse-vol)
def problem_erc_two() -> None:
    print("\n[Problem: equal risk contribution with two assets, vols 15% and 25%]")
    for rho in (-0.5, 0.0, 0.8):
        w = erc_newton(cov_matrix(np.array([0.15, 0.25]), np.array([[1.0, rho], [rho, 1.0]])))
        check(f"weight of the 15% asset at correlation {rho}", w[0], 0.625, 1e-10)


# Problem 14 (cards risk-forward-pfe-closed-form, risk-forward-ee-closed-form)
def problem_forward_exposure() -> None:
    print("\n[Problem: par forward, N = 10m, vol 30%, r = 0, one year]")
    n, vol = 10e6, 0.30
    ee = n * (2.0 * ncdf(0.5 * vol) - 1.0)
    pfe = n * (math.exp(-0.5 * vol * vol + vol * ninv(0.95)) - 1.0)
    check("EE(1) = N (2 Phi(sigma / 2) - 1)", ee, 1_192_354, 1.0)
    check("PFE95(1)", pfe, 5_658_927, 1.0)
    check("rule of thumb EE ~ 0.4 N sigma sqrt(t)", 0.4 * n * vol, 1_200_000, 1e-6)
    rng = np.random.default_rng(8)
    st = np.exp(-0.5 * vol * vol + vol * rng.standard_normal(1_000_000))
    pos = n * np.maximum(st - 1.0, 0.0)
    check("simulated EE (about)", float(pos.mean()), ee, 6_000)
    check("simulated PFE95 (about)", float(np.quantile(pos, 0.95)), pfe, 15_000)


# Problem 15 (cards risk-effective-epe-definition, risk-eepe-discrete-weights)
def problem_eepe() -> None:
    print("\n[Problem: Effective EPE from a coarse EE profile, CRE53.12 to CRE53.13]")
    grid = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0])
    ee = np.array([0.0, 80e3, 120e3, 160e3, 130e3, 80e3, 0.0])
    eee = effective_ee(ee, 0.0)
    check("Effective EE at 3y", eee[4], 160e3, 0.0)
    check("Effective EE at 5y", eee[6], 160e3, 0.0)
    eepe = effective_epe(grid, eee, 5.0)
    check("Effective EPE (right-endpoint weights)", eepe, 100_000, 1e-6)
    trap = float(np.sum(0.5 * (eee[1:3] + eee[:2]) * np.diff(grid[:3])))
    check("trapezoid instead (not the CRE53.13 sum)", trap, 70_000, 1e-6)
    check("EAD = 1.4 x Effective EPE", 1.4 * eepe, 140_000, 1e-6)
    epe = float(np.sum(0.5 * (ee[1:] + ee[:-1]) * np.diff(grid)) / 5.0)
    check("EPE over the life (trapezoid)", epe, 100_000, 1e-6)


# Problem 16 (cards risk-margin-period-of-risk-mpor, risk-collateralised-ee-sqrt-mpor)
def problem_mpor() -> None:
    print("\n[Problem: daily VM, MPOR 10 and 20 days, forward N = 10m, vol 30%, r = 0]")
    n, vol = 10e6, 0.30
    c10 = collateralised_ee_closed(n, vol, 10 / 250)
    c20 = collateralised_ee_closed(n, vol, 20 / 250)
    unc = collateralised_ee_closed(n, vol, 1.0)
    check("collateralised EE, MPOR 10", c10, 239_329, 1.0)
    check("collateralised EE, MPOR 20", c20, 338_412, 1.0)
    check("ratio", c20 / c10, 1.4140, 5e-5)
    check("uncollateralised EE at 1 year", unc, 1_192_354, 1.0)
    check("collateral cuts EE by", 1.0 - c10 / unc, 0.7993, 5e-4)


# Problem 17 (cards risk-ngr-four-trades, risk-net-to-gross-ratio-ngr)
def problem_ngr() -> None:
    print("\n[Problem: four trades +20, -15, +5, -2 (millions)]")
    v = np.array([20.0, -15.0, 5.0, -2.0])
    gross, net = float(np.maximum(v, 0).sum()), max(float(v.sum()), 0.0)
    check("gross", gross, 25.0, 0.0)
    check("net", net, 8.0, 0.0)
    check("NGR", net / gross, 0.32, 1e-12)
    check("MGN20.17 factor 0.4 + 0.6 NGR", 0.4 + 0.6 * net / gross, 0.592, 1e-12)


# Problem 18 (cards risk-cva-flat-exposure, risk-credit-triangle-cva)
def problem_cva_flat() -> None:
    print("\n[Problem: 1-year trade, average EE 500k, ENE 300k, hazards 3% and 1.5%, LGD 60%, r = 4%]")
    df = math.exp(-0.04 * 0.5)
    pd_c, pd_b = 1.0 - math.exp(-0.03), 1.0 - math.exp(-0.015)
    cva = 0.6 * df * 500e3 * pd_c
    dva = 0.6 * df * 300e3 * pd_b
    check("counterparty 1y PD", pd_c, 0.029554, 5e-7)
    check("bank 1y PD", pd_b, 0.014888, 5e-7)
    check("CVA", cva, 8_691, 1.0)
    check("DVA", dva, 2_627, 1.0)
    check("net adjustment DVA - CVA", dva - cva, -6_064, 1.0)
    # Same with a continuous integral: exposure flat at 500k, hazard density 0.03 e^{-0.03 t}, discount e^{-0.04 t}
    integral = 0.6 * 500e3 * 0.03 * (1.0 - math.exp(-0.07)) / 0.07
    check("CVA by the exact integral", integral, 8_692, 1.0)
    check("credit-triangle approximation spread x EE x annuity", 0.018 * 500e3 * (1.0 - math.exp(-0.04)) / 0.04, 8_822, 1.0)


# Problem 19 (cards risk-xva-midpoint-shortcut, risk-mva-regulatory-driver, risk-kva-capital-valuation-adjustment)
def problem_fva_mva_kva() -> None:
    print("\n[Problem: midpoint short-cuts against the integrals with a flat discount curve]")
    fca = 0.0075 * 400e3 * 0.945 * 3.0
    mva = 0.0120 * 2e6 * 0.910 * 5.0
    kva = 0.100 * 500e3 * 0.910 * 5.0
    check("FCA short-cut", fca, 8_505, 1e-6)
    check("MVA short-cut", mva, 109_200, 1e-6)
    check("KVA short-cut", kva, 227_500, 1e-6)
    r = -math.log(0.910) / 2.5
    ann = (1.0 - math.exp(-5.0 * r)) / r
    check("flat rate implied by P(0, 2.5) = 0.910", r, 0.037724, 5e-7)
    check("integral of e^{-rt} over 5 years", ann, 4.5567, 5e-4)
    check("MVA with the integral", 0.0120 * 2e6 * ann, 109_362, 1.0)
    check("short-cut error, relative", mva / (0.0120 * 2e6 * ann) - 1.0, -0.0015, 5e-5)


# Problem 20 (card risk-wrong-way-risk-classification, risk-wwr-two-state)
def problem_wwr_two_state() -> None:
    print("\n[Problem: two-state wrong-way risk]")
    p_stress, e_stress, e_normal, pd, lgd = 0.10, 10e6, 1e6, 0.01, 0.6
    ee = p_stress * e_stress + (1 - p_stress) * e_normal
    cva_ind = lgd * pd * ee
    cva_wwr = lgd * (pd / p_stress) * p_stress * e_stress  # every default happens in the stress state
    check("expected exposure", ee, 1_900_000, 1e-6)
    check("CVA, independent", cva_ind, 11_400, 1e-6)
    check("CVA, all defaults in the stress state", cva_wwr, 60_000, 1e-6)
    check("ratio", cva_wwr / cva_ind, 5.263, 5e-4)
    rng = np.random.default_rng(14)
    n = 2_000_000
    stress = rng.random(n) < p_stress
    default = stress & (rng.random(n) < pd / p_stress)
    loss = lgd * np.where(stress, e_stress, e_normal) * default
    check("simulated wrong-way CVA (about)", float(loss.mean()), 60_000, 1_500)


# Problem 21 (cards risk-almgren-chriss-urgency-parameter, risk-ac-discrete-kappa)
def problem_almgren_chriss() -> None:
    print("\n[Problem: sell 500,000 shares over 3 days, sigma 2, eta 2e-6, lambda 2e-6, no permanent impact]")
    x0, t_days, sig, eta, lam = 5e5, 3, 2.0, 2e-6, 2e-6
    kt2 = lam * sig * sig / eta
    kappa = math.acosh(1.0 + 0.5 * kt2)
    check("kappa_tilde^2", kt2, 4.0, 1e-12)
    check("discrete kappa = acosh(3)", kappa, 1.762747, 5e-7)
    hold = [x0 * math.sinh(kappa * (t_days - k)) / math.sinh(kappa * t_days) for k in range(t_days + 1)]
    sells = [hold[k] - hold[k + 1] for k in range(t_days)]
    check("day 1 sale", sells[0], 414_286, 1.0)
    check("day 2 sale", sells[1], 71_429, 1.0)
    check("day 3 sale", sells[2], 14_286, 1.0)
    # Brute force: minimise E + lam Var over (x1, x2) on the first-order conditions
    a = np.array([[2 * eta + lam * sig * sig, -eta], [-eta, 2 * eta + lam * sig * sig]])
    sol = np.linalg.solve(a, np.array([eta * x0, 0.0]))
    check("x1 from the linear system minus sinh formula", sol[0] - hold[1], 0.0, 1e-6)
    cont = [x0 * math.sinh(2.0 * (t_days - k)) / math.sinh(2.0 * t_days) for k in range(t_days + 1)]
    check("day 1 sale with the continuous kappa = 2 (wrong for daily trading)", cont[0] - cont[1], 432_355, 1.0)


# Problem 22 (cards risk-lvar-spread-cost-and-scaling, risk-liquidation-horizon-variance-factor)
def problem_lvar() -> None:
    print("\n[Problem: 30m EM sovereign bond, VaR 1.5m, spread 1.2% (sd 0.6%), 3 days to liquidate]")
    col = 0.5 * 30e6 * (0.012 + Z99 * 0.006)
    m = math.sqrt(horizon_variance_factor(3))
    check("cost of liquidation", col, 389_371, 1.0)
    check("horizon sd multiplier, L = 3", m, 1.2472, 5e-5)
    check("L-VaR", 1.5e6 * m + col, 2_260_200, 1.0)


# Problem 23 (cards risk-negative-oil-options-failure, risk-model-reserve-black-bachelier)
def problem_black_bachelier() -> None:
    print("\n[Problem: futures at 5, Bachelier vol 15.96, one month: probability of a negative settlement]")
    nvol, t = 15.96, 1.0 / 12.0
    check("P(F_T < 0) from F = 5", ncdf(-5.0 / (nvol * math.sqrt(t))), 0.1389, 5e-5)
    check("Bachelier put struck at 0", bachelier_put(5.0, 0.0, nvol, t), 0.3255, 5e-5)
    check("Black put struck at 0 (a lognormal forward cannot go below 0)", black_put(5.0, 0.0, 3.2, t), 0.0, 0.0)


# Problem 24 (cards risk-bgk-barrier-shift, risk-barrier-monitoring-validation)
def problem_bgk() -> None:
    print("\n[Problem: daily-monitored barrier at 90, vol 20%]")
    beta = 0.5826
    shifted = 90.0 * math.exp(-beta * 0.2 * math.sqrt(1.0 / 252.0))
    check("shifted continuous barrier", shifted, 89.3418, 5e-4)
    check("shift in vol units, beta sigma sqrt(dt)", beta * 0.2 * math.sqrt(1.0 / 252.0), 0.007340, 5e-7)


def main() -> None:
    problem_kelly()
    problem_var_es()
    problem_fhs()
    problem_reverse_stress()
    problem_mdd()
    problem_greek_attribution()
    problem_breakeven()
    problem_pca()
    problem_bumps()
    problem_bump_counts()
    problem_short_put_crash()
    problem_euler()
    problem_erc_two()
    problem_forward_exposure()
    problem_eepe()
    problem_mpor()
    problem_ngr()
    problem_cva_flat()
    problem_fva_mva_kva()
    problem_wwr_two_state()
    problem_almgren_chriss()
    problem_lvar()
    problem_black_bachelier()
    problem_bgk()
    print("\nAll problem set checks passed.")


if __name__ == "__main__":
    main()
