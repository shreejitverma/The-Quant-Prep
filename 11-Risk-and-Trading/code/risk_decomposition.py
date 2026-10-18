"""Risk decomposition: Euler allocation of VaR and ES (marginal, component, incremental), risk parity, factor risk.

Backs every number in 11-Risk-and-Trading/13-Risk-Decomposition-and-Attribution.md (and problems in
17-Risk-Problem-Set.md).  Every Euler contribution is checked against a brute-force recomputation: finite differences of
the risk measure in the position sizes, or a full recomputation of the portfolio risk with and without the trade.
Portfolios, volatilities and correlations are labelled illustrative inputs, not market data.  Simulations use fixed
seeds and are quoted in the note as "about".

Run: python 11-Risk-and-Trading/code/risk_decomposition.py
"""

from __future__ import annotations

import math

import numpy as np

Z95 = 1.6448536269514722
Z99 = 2.3263478740408408


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.10g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def cov_matrix(vols: np.ndarray, corr: np.ndarray) -> np.ndarray:
    return np.outer(vols, vols) * corr


def normal_var(x: np.ndarray, cov: np.ndarray, z: float) -> float:
    """Delta-normal VaR of dollar positions x: z sqrt(x' Sigma x)."""
    return z * math.sqrt(float(x @ cov @ x))


def euler_normal(x: np.ndarray, cov: np.ndarray, z: float) -> tuple[float, np.ndarray, np.ndarray]:
    """VaR, marginal VaR per dollar (dVaR/dx_i = z (Sigma x)_i / sigma_p) and component VaR x_i dVaR/dx_i."""
    sig = math.sqrt(float(x @ cov @ x))
    marginal = z * (cov @ x) / sig
    return z * sig, marginal, x * marginal


# ---------------------------------------------------------------------------
# Worked example 1 (cards risk-marginal-vs-component-var, risk-beta-relationship-marginal-var, risk-60-40-equity-risk-concentration)
# ---------------------------------------------------------------------------


def two_asset_portfolio() -> tuple[np.ndarray, np.ndarray]:
    vols = np.array([0.20, 0.06])
    corr = np.array([[1.0, -0.15], [-0.15, 1.0]])
    x = np.array([60e6, 40e6])
    return x, cov_matrix(vols, corr)


def section_example_1() -> None:
    print("\n[Worked example 1: 60m equities (20% vol) and 40m bonds (6% vol), correlation -0.15, 95% one-year VaR]")
    x, cov = two_asset_portfolio()
    var, marg, comp = euler_normal(x, cov, Z95)
    w = x / x.sum()
    sig_w = math.sqrt(float(w @ cov @ w))
    beta = (cov @ w) / (w @ cov @ w)
    check("portfolio volatility", sig_w, 0.118794, 5e-7)
    check("portfolio variance", sig_w**2, 0.014112, 5e-7)
    check("VaR", var, 19_539_864, 1.0)
    check("z_0.95 (Phi(z) = 0.95)", Z95, 1.644854, 5e-7)
    check("Phi(z_0.95)", 0.5 * (1.0 + math.erf(Z95 / math.sqrt(2.0))), 0.95, 1e-15)
    check("VaR with z rounded to 1.6449", 1.6449 * sig_w * x.sum(), 19_540_415, 1.0)
    check("Cov(r_equity, r_p)", float((cov @ w)[0]), 0.02328, 1e-12)
    check("Cov(r_bond, r_p)", float((cov @ w)[1]), 0.00036, 1e-12)
    check("beta equities", beta[0], 1.649660, 5e-7)
    check("beta bonds", beta[1], 0.025510, 5e-7)
    check("marginal VaR equities, per dollar", marg[0], 0.322341, 5e-7)
    check("marginal VaR bonds, per dollar", marg[1], 0.004985, 5e-7)
    check("component VaR equities", comp[0], 19_340_478, 1.0)
    check("component VaR bonds", comp[1], 199_386, 1.0)
    check("equity share of VaR", comp[0] / var, 0.98980, 5e-6)
    check("bond share of VaR", comp[1] / var, 0.01020, 5e-6)
    check("sum of components minus VaR", comp.sum() - var, 0.0, 1e-6)
    # Brute force: central differences of VaR in each dollar position
    h = 1_000.0
    for i, name in enumerate(("equities", "bonds")):
        up, dn = x.copy(), x.copy()
        up[i] += h
        dn[i] -= h
        fd = (normal_var(up, cov, Z95) - normal_var(dn, cov, Z95)) / (2 * h)
        check(f"brute-force marginal VaR {name} minus Euler", fd - marg[i], 0.0, 1e-9)
    standalone = np.array([Z95 * math.sqrt(cov[i, i]) * x[i] for i in range(2)])
    check("standalone VaR equities", standalone[0], 19_738_244, 1.0)
    check("standalone VaR bonds", standalone[1], 3_947_649, 1.0)
    check("diversification benefit", standalone.sum() - var, 4_146_028, 1.0)
    check("sum of standalone VaRs", standalone.sum(), 23_685_892, 1.0)
    # Incremental VaR of removing each position (full recomputation): these do not add up to the total.
    inc = np.array([var - normal_var(np.where(np.arange(2) == i, 0.0, x), cov, Z95) for i in range(2)])
    check("incremental VaR of the equity position", inc[0], 15_592_215, 1.0)
    check("incremental VaR of the bond position", inc[1], -198_379, 1.0)
    check("sum of incremental VaRs", inc.sum(), 15_393_836, 1.0)

    print("\n[A conventional 60/40 with 18% and 5% vols]")
    for rho, exp_share in ((0.0, 0.966844), (0.2, 0.935644)):
        cov6040 = cov_matrix(np.array([0.18, 0.05]), np.array([[1.0, rho], [rho, 1.0]]))
        _, _, c = euler_normal(np.array([0.6, 0.4]), cov6040, 1.0)
        check(f"equity share of risk at correlation {rho}", c[0] / c.sum(), exp_share, 5e-6)


# ---------------------------------------------------------------------------
# Worked example 2: incremental VaR of a trade, marginal estimate against recomputation, best hedge
# (cards risk-incremental-var-formula, risk-best-hedge-position)
# ---------------------------------------------------------------------------


def section_example_2() -> None:
    print("\n[Worked example 2: adding gold (15% vol, correlation 0.10 with equities, 0.30 with bonds)]")
    vols = np.array([0.20, 0.06, 0.15])
    corr = np.array([[1.0, -0.15, 0.10], [-0.15, 1.0, 0.30], [0.10, 0.30, 1.0]])
    cov = cov_matrix(vols, corr)
    x = np.array([60e6, 40e6, 0.0])
    var0, marg, _ = euler_normal(x, cov, Z95)
    cov_gold_port = float((cov @ x)[2])
    check("Cov(gold return, portfolio dollar P&L) / 1e6", cov_gold_port / 1e6, 0.288, 5e-7)
    check("marginal VaR of gold, per dollar", marg[2], 0.039877, 5e-7)
    results = {}
    for add in (5e6, 50e6):
        approx = add * marg[2]
        y = x.copy()
        y[2] += add
        exact = normal_var(y, cov, Z95) - var0
        results[add] = (approx, exact)
        print(f"  add {add / 1e6:.0f}m gold: marginal estimate {approx:,.0f}, recomputed {exact:,.0f}")
    check("5m: marginal estimate", results[5e6][0], 199_386, 1.0)
    check("5m: recomputed incremental VaR", results[5e6][1], 236_893, 1.0)
    check("50m: marginal estimate", results[50e6][0], 1_993_864, 1.0)
    check("50m: recomputed incremental VaR", results[50e6][1], 5_197_006, 1.0)
    # Best hedge in gold: the holding that minimises portfolio variance (Litterman 1996)
    best = -cov_gold_port / cov[2, 2]
    y = x.copy()
    y[2] = best
    check("variance-minimising gold position", best, -12_800_000, 1.0)
    check("VaR after the best hedge", normal_var(y, cov, Z95), 19_282_961, 1.0)
    grid = np.linspace(best - 1e6, best + 1e6, 2001)
    brute = grid[np.argmin([normal_var(np.array([60e6, 40e6, g]), cov, Z95) for g in grid])]
    check("brute-force grid minimiser minus closed form", brute - best, 0.0, 1_000.0)


# ---------------------------------------------------------------------------
# Core concepts "Euler beyond the normal": simulated ES and VaR contributions with an option position
# (cards risk-expected-shortfall-euler-decomposition, risk-component-var-simulation-noise)
# ---------------------------------------------------------------------------


def bs_put(s: np.ndarray, k: float, r: float, vol: float, t: float) -> np.ndarray:
    from math import erf

    verf = np.vectorize(erf, otypes=[float])
    sq = vol * math.sqrt(t)
    d1 = (np.log(s / k) + (r + 0.5 * vol * vol) * t) / sq
    d2 = d1 - sq

    def ncdf(v: np.ndarray) -> np.ndarray:
        return 0.5 * (1.0 + verf(v / math.sqrt(2.0)))

    return k * math.exp(-r * t) * ncdf(-d2) - s * ncdf(-d1)


def simulate_factors(n: int, seed: int, nu: float = 4.0) -> np.ndarray:
    """Daily returns of equity, bonds and gold: multivariate Student t (nu = 4) scaled to unit-variance marginals."""
    vols = np.array([0.0125, 0.004, 0.009])
    corr = np.array([[1.0, -0.15, 0.10], [-0.15, 1.0, 0.30], [0.10, 0.30, 1.0]])
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n, 3)) @ np.linalg.cholesky(corr).T
    w = rng.chisquare(nu, n)
    t = z / np.sqrt(w / nu)[:, None] * math.sqrt((nu - 2.0) / nu)
    return t * vols


def tail_stats(loss: np.ndarray, q: float) -> tuple[float, float, np.ndarray]:
    k = int(math.ceil(q * len(loss))) - 1
    order = np.argsort(loss)
    var = float(loss[order[k]])
    tail = order[k:]
    return var, float(loss[tail].mean()), tail


def section_simulated_euler() -> None:
    print("\n[Euler by simulation: 1,000,000 Student t (nu = 4) days, 97.5% ES and 99% VaR]")
    r = simulate_factors(1_000_000, seed=2026)
    x = np.array([60e6, 40e6, 10e6])
    pnl_lin = r * x  # dollar P&L of each linear position
    loss = -pnl_lin.sum(axis=1)
    q = 0.975
    _, es, tail = tail_stats(loss, q)
    ces = -pnl_lin[tail].mean(axis=0)
    cov = np.cov(r.T)
    share_cov = x * (cov @ x) / float(x @ cov @ x)
    check("ES 97.5%, linear book", es, 2_161_000, 1_000)
    check("sum of ES contributions minus ES", ces.sum() - es, 0.0, 1e-6)
    for i, name in enumerate(("equities", "bonds", "gold")):
        print(f"  {name}: ES contribution share {ces[i] / es:.4f}, covariance share {share_cov[i]:.4f}")
    check("equity ES share (elliptical: equals covariance share)", ces[0] / es, share_cov[0], 0.01)
    check("gold ES share", ces[2] / es, share_cov[2], 0.01)
    check("equity ES share, quoted", ces[0] / es, 0.946, 5e-4)
    check("equity covariance share, quoted", share_cov[0], 0.946, 5e-4)

    print("\n[Add a short put: 4,000 one-month at-the-money puts on an index at 100, 20% implied vol]")
    idx0, n_puts = 100.0, 4_000.0 * 100.0  # contracts x multiplier 100
    put0 = float(bs_put(np.array([idx0]), 100.0, 0.0, 0.20, 1.0 / 12.0)[0])
    put1 = bs_put(idx0 * np.exp(r[:, 0]), 100.0, 0.0, 0.20, 1.0 / 12.0 - 1.0 / 252.0)
    pnl_put = -n_puts * (put1 - put0)
    pnl = np.column_stack([pnl_lin, pnl_put])
    scale = np.ones(4)

    def es_of(sc: np.ndarray) -> tuple[float, float, np.ndarray]:
        return tail_stats(-(pnl * sc).sum(axis=1), q)

    var99, _, _ = tail_stats(-(pnl * scale).sum(axis=1), 0.99)
    _, es_full, tail = es_of(scale)
    ces = -pnl[tail].mean(axis=0)
    h = 0.01
    brute = np.zeros(4)
    for i in range(4):
        up, dn = scale.copy(), scale.copy()
        up[i] += h
        dn[i] -= h
        brute[i] = (es_of(up)[1] - es_of(dn)[1]) / (2 * h)
    names = ("equities", "bonds", "gold", "short put")
    for i in range(4):
        print(f"  {names[i]}: Euler E[L_i | L >= VaR] {ces[i]:,.0f}, brute-force dES/dscale {brute[i]:,.0f}")
    check("ES 97.5% with the short put", es_full, 2_978_000, 1_000)
    check("short put ES contribution", ces[3], 824_000, 1_000)
    check("equity ES contribution, with the put", ces[0], 2_082_000, 1_000)
    check("gold ES contribution, with the put", ces[2], 57_200, 300)
    check("bond ES contribution, with the put", ces[1], 14_500, 300)
    check("short put contribution share", ces[3] / es_full, 0.277, 0.001)
    check("max relative gap Euler vs brute force", float(np.max(np.abs(ces - brute) / np.abs(ces))), 0.006, 5e-4)
    check("put premium per index point", put0, 2.3030, 5e-5)
    # VaR contributions: E[L_i | L = VaR], estimated from the 2m + 1 scenarios nearest to the VaR order statistic
    loss_all = -pnl.sum(axis=1)
    order = np.argsort(loss_all)
    k = int(math.ceil(0.99 * len(loss_all))) - 1
    contrib = {}
    for m in (50, 500):
        near = order[k - m : k + m + 1]
        contrib[m] = -pnl[near].mean(axis=0)
        print(f"  window +-{m}: VaR contributions {np.round(contrib[m] / 1e3, 1)} (thousands), sum {contrib[m].sum():,.0f}")
    check("99% VaR with the short put", var99, 2_765_000, 1_000)
    check("short put VaR contribution, window +-500", contrib[500][3], 746_000, 1_000)
    check("short put VaR contribution, window +-50", contrib[50][3], 755_000, 1_000)
    check("bond VaR contribution, window +-500", contrib[500][1], 17_400, 300)
    check("bond VaR contribution, window +-50", contrib[50][1], -3_000, 300)


# ---------------------------------------------------------------------------
# Core concepts "Risk parity" (cards risk-parity-definition, risk-erc-two-asset-inverse-vol)
# ---------------------------------------------------------------------------


def erc_newton(cov: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """Equal risk contribution weights: solve (Sigma y)_i = 1 / y_i with Newton, the stationarity condition of the
    strictly convex f(y) = y' Sigma y / 2 - sum log y_i, then normalise y to sum to one."""
    n = cov.shape[0]
    y = 1.0 / np.sqrt(np.diag(cov))
    for _ in range(100):
        g = cov @ y - 1.0 / y
        if np.max(np.abs(g * y)) < tol:
            break
        hess = cov + np.diag(1.0 / y**2)
        step = np.linalg.solve(hess, g)
        while np.any(y - step <= 0.0):
            step *= 0.5
        y = y - step
    else:
        raise RuntimeError("ERC Newton did not converge")
    assert n == len(y)
    return y / y.sum()


def erc_ccd(cov: np.ndarray, sweeps: int = 2000) -> np.ndarray:
    """Cyclical coordinate descent on the same convex function: Sigma_ii y_i^2 + c_i y_i - 1 = 0 per coordinate."""
    y = np.ones(cov.shape[0])
    for _ in range(sweeps):
        for i in range(len(y)):
            c = float(cov[i] @ y - cov[i, i] * y[i])
            y[i] = (-c + math.sqrt(c * c + 4.0 * cov[i, i])) / (2.0 * cov[i, i])
    return y / y.sum()


def risk_shares(w: np.ndarray, cov: np.ndarray) -> np.ndarray:
    rc = w * (cov @ w)
    return rc / rc.sum()


def section_risk_parity() -> None:
    print("\n[Risk parity: two assets give inverse-volatility weights for any correlation]")
    vols = np.array([0.18, 0.05])
    for rho in (-0.3, 0.5):
        w = erc_newton(cov_matrix(vols, np.array([[1.0, rho], [rho, 1.0]])))
        check(f"equity ERC weight at correlation {rho}", w[0], 0.217391, 5e-7)
    check("inverse-vol equity weight 0.05 / 0.23", 0.05 / 0.23, 0.217391, 5e-7)

    print("\n[Three assets: equities 18%, bonds 5%, commodities 20%; correlations -0.2, 0.3, 0.0]")
    v3 = np.array([0.18, 0.05, 0.20])
    c3 = np.array([[1.0, -0.2, 0.3], [-0.2, 1.0, 0.0], [0.3, 0.0, 1.0]])
    cov = cov_matrix(v3, c3)
    w_n = erc_newton(cov)
    w_c = erc_ccd(cov)
    w_iv = (1.0 / v3) / (1.0 / v3).sum()
    check("ERC weight equities", w_n[0], 0.1712, 5e-5)
    check("ERC weight bonds", w_n[1], 0.6931, 5e-5)
    check("ERC weight commodities", w_n[2], 0.1357, 5e-5)
    check("Newton minus coordinate descent, max abs", float(np.max(np.abs(w_n - w_c))), 0.0, 1e-10)
    check("ERC max deviation of risk share from 1/3", float(np.max(np.abs(risk_shares(w_n, cov) - 1.0 / 3.0))), 0.0, 1e-12)
    rs_iv = risk_shares(w_iv, cov)
    check("inverse-vol weight bonds", w_iv[1], 0.6545, 5e-4)
    check("inverse-vol risk share equities", rs_iv[0], 0.34375, 5e-5)
    check("inverse-vol risk share bonds", rs_iv[1], 0.2500, 5e-5)
    check("inverse-vol risk share commodities", rs_iv[2], 0.40625, 5e-6)
    check("ERC portfolio volatility", math.sqrt(float(w_n @ cov @ w_n)), 0.0544, 5e-5)


# ---------------------------------------------------------------------------
# Core concepts "Factor risk attribution" (cards risk-factor-risk-decomposition-advantage, risk-factor-euler-contributions)
# ---------------------------------------------------------------------------


def section_factor() -> None:
    print("\n[Factor decomposition: 4 stocks, market and value factors, specific risk]")
    b = np.array([[1.1, 0.3], [0.9, -0.2], [1.2, 0.5], [0.7, -0.4]])
    f_vols = np.array([0.16, 0.06])
    f_corr = np.array([[1.0, -0.2], [-0.2, 1.0]])
    cov_f = cov_matrix(f_vols, f_corr)
    spec = np.array([0.25, 0.20, 0.30, 0.15])
    w = np.array([0.4, 0.3, -0.2, 0.5])  # fractions of NAV, long-short
    xf = b.T @ w
    sys_var = float(xf @ cov_f @ xf)
    spec_var = float(np.sum((w * spec) ** 2))
    sig = math.sqrt(sys_var + spec_var)
    rc_f = xf * (cov_f @ xf) / sig
    rc_spec = spec_var / sig
    check("market exposure", xf[0], 0.82, 1e-12)
    check("value exposure", xf[1], -0.24, 1e-12)
    check("factor portfolio volatility", sig, 0.2025, 5e-5)
    check("market contribution share", rc_f[0] / sig, 0.4290, 5e-5)
    check("value contribution share", rc_f[1] / sig, 0.0143, 5e-5)
    check("specific contribution share", rc_spec / sig, 0.5567, 5e-5)
    check("sum of factor and specific contributions minus sigma", rc_f.sum() + rc_spec - sig, 0.0, 1e-15)
    cov_assets = b @ cov_f @ b.T + np.diag(spec**2)
    rc_assets = w * (cov_assets @ w) / sig
    check("sum of asset contributions minus sigma (same total, other axis)", rc_assets.sum() - sig, 0.0, 1e-15)
    # Euler on variance gives twice the variance: variance is homogeneous of degree 2
    check("sum w_i d(var)/dw_i divided by var", float(w @ (2.0 * cov_assets @ w)) / float(w @ cov_assets @ w), 2.0, 1e-12)


def main() -> None:
    section_example_1()
    section_example_2()
    section_simulated_euler()
    section_risk_parity()
    section_factor()
    print("\nAll risk decomposition checks passed.")


if __name__ == "__main__":
    main()
