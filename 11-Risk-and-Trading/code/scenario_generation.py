"""Scenario generation: historical, filtered historical and Monte Carlo scenarios, copulas, variance reduction, horizons.

Backs every number in 11-Risk-and-Trading/11-Scenario-Generation.md.

Data are simulated with fixed seeds from labelled models (GARCH(1,1) with Student t innovations); nothing here is
market data.  The backtest compares 99% one-day VaR from plain historical simulation, filtered historical simulation
(EWMA-filtered residuals rescaled by today's EWMA vol) and a normal model with the same EWMA vol, on the same path,
so the only change between HS and FHS is the filtering.

Run: python 11-Risk-and-Trading/code/scenario_generation.py
"""

from __future__ import annotations

import math

import numpy as np

SQRT2 = math.sqrt(2.0)
Z99 = 2.3263478740408408


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.6f}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def npdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ---------------------------------------------------------------------------
# Worked examples 1 and 2: FHS scaling and a Cholesky draw
# ---------------------------------------------------------------------------


def section_examples() -> None:
    print("\n[Worked example 1: filtered historical scenario]")
    r_hist, vol_then, vol_now = -0.022, 0.011, 0.024
    check("scale ratio", vol_now / vol_then, 2.1818, 5e-5)
    check("filtered return", r_hist * vol_now / vol_then, -0.048, 1e-12)
    check("standardised residual", r_hist / vol_then, -2.0, 1e-12)
    print("\n[Worked example 2: one correlated draw]")
    s_d, y_d, rho = 0.20 / math.sqrt(252.0), 0.0100 / math.sqrt(252.0), -0.35
    cov = np.array([[s_d**2, rho * s_d * y_d], [rho * s_d * y_d, y_d**2]])
    chol = np.linalg.cholesky(cov)
    dx = chol @ np.array([1.2, -0.8])
    check("daily equity sd", s_d, 0.012599, 5e-7)
    check("daily 10y sd", y_d, 0.00062994, 5e-9)
    check("L21 = rho sd_y", chol[1, 0], -0.00022048, 5e-9)
    check("L22 = sd_y sqrt(1 - rho^2)", chol[1, 1], 0.00059010, 5e-9)
    check("equity shock", dx[0], 0.015119, 5e-7)
    check("10y shock (bp)", dx[1] * 1e4, -7.3665, 5e-5)


# ---------------------------------------------------------------------------
# Backtest: HS against FHS against normal-EWMA on a GARCH path
# ---------------------------------------------------------------------------


def simulate_garch_t(
    n: int, seed: int, omega: float = 2e-6, alpha: float = 0.08, beta: float = 0.90, nu: float = 5.0
) -> tuple[np.ndarray, np.ndarray]:
    """GARCH(1,1) returns with unit-variance Student t innovations; unconditional daily vol sqrt(omega / (1 - a - b)) = 1%.

    Returns (returns, true conditional vols).
    """
    rng = np.random.default_rng(seed)
    z = rng.standard_t(nu, n) * math.sqrt((nu - 2.0) / nu)
    r = np.empty(n)
    sig = np.empty(n)
    var = omega / (1.0 - alpha - beta)
    for t in range(n):
        sig[t] = math.sqrt(var)
        r[t] = sig[t] * z[t]
        var = omega + alpha * r[t] ** 2 + beta * var
    return r, sig


def ewma_vols(r: np.ndarray, lam: float = 0.94, seed_var: float | None = None) -> np.ndarray:
    """vol[t] is the forecast for day t made with returns up to t - 1."""
    v = np.empty(len(r))
    var = float(np.var(r[:50])) if seed_var is None else seed_var
    for t in range(len(r)):
        v[t] = math.sqrt(var)
        var = lam * var + (1.0 - lam) * r[t] ** 2
    return v


def kupiec_pvalue(x: int, n: int, p: float) -> float:
    """Unconditional coverage LR test (Kupiec 1995), chi-square with 1 degree of freedom."""
    phat = x / n
    ll0 = (n - x) * math.log(1.0 - p) + x * math.log(p)
    ll1 = (n - x) * math.log(1.0 - phat) + (x * math.log(phat) if x > 0 else 0.0)
    lr = -2.0 * (ll0 - ll1)
    return math.erfc(math.sqrt(lr / 2.0))


def hs_quantile_loss(window: np.ndarray, q: float = 0.99) -> float:
    """99% VaR as a positive loss: the 3rd largest loss of 250 (no interpolation), i.e. sorted losses at rank ceil(0.01 n)."""
    losses = np.sort(-window)[::-1]
    k = math.ceil((1.0 - q) * len(window))
    return float(losses[k - 1])


def section_backtest() -> None:
    print("\n[Core concepts: backtesting HS, FHS and normal-EWMA 99% VaR on a simulated GARCH-t path]")
    r, true_sig = simulate_garch_t(5250, seed=2024)
    vols = ewma_vols(r)
    window, start = 250, 250
    names = ("HS", "FHS", "normal-EWMA")
    hits = {name: [] for name in names}
    for t in range(start, len(r)):
        hist = r[t - window : t]
        var_hs = hs_quantile_loss(hist)
        var_fhs = hs_quantile_loss(hist / vols[t - window : t]) * vols[t]
        var_n = Z99 * vols[t]
        for name, v in zip(names, (var_hs, var_fhs, var_n), strict=True):
            hits[name].append(-r[t] > v)
    n = len(hits["HS"])
    counts = {name: int(np.sum(hits[name])) for name in names}
    for name in names:
        x = counts[name]
        print(f"  {name:<12}: {x} exceptions in {n} days ({x / n:.2%}), Kupiec p-value {kupiec_pvalue(x, n, 0.01):.4f}")
    check("days tested", n, 5000, 0)
    check("HS exceptions", counts["HS"], 62, 0)
    check("FHS exceptions", counts["FHS"], 62, 0)
    check("normal-EWMA exceptions", counts["normal-EWMA"], 97, 0)
    check("Kupiec p-value at 62 of 5,000", kupiec_pvalue(62, n, 0.01), 0.1002, 5e-5)
    assert kupiec_pvalue(97, n, 0.01) < 1e-8
    assert abs(float(np.corrcoef(true_sig[start:], vols[start:])[0, 1])) > 0.5


def section_regime_switch() -> None:
    print("\n[Core concepts: HS against FHS after a volatility regime change, 2,000 paths, seed 77]")
    rng = np.random.default_rng(77)
    paths, pre, post, nu = 2000, 250, 60, 5.0
    z = rng.standard_t(nu, (paths, pre + post)) * math.sqrt((nu - 2.0) / nu)
    out = {}
    for label, (v_pre, v_post) in (("calm to stressed", (0.01, 0.02)), ("stressed to calm", (0.02, 0.01))):
        sig = np.concatenate([np.full(pre, v_pre), np.full(post, v_post)])
        r = z * sig
        lam, var = 0.94, np.full(paths, v_pre**2)
        ewma = np.empty_like(r)
        for t in range(pre + post):
            ewma[:, t] = np.sqrt(var)
            var = lam * var + (1.0 - lam) * r[:, t] ** 2
        hs_hits, fhs_hits = np.zeros((paths, post)), np.zeros((paths, post))
        for j, t in enumerate(range(pre, pre + post)):
            window = r[:, t - 250 : t]
            k = math.ceil(0.01 * 250)
            hs_var = np.sort(-window, axis=1)[:, -k]
            fhs_var = np.sort(-window / ewma[:, t - 250 : t], axis=1)[:, -k] * ewma[:, t]
            hs_hits[:, j] = -r[:, t] > hs_var
            fhs_hits[:, j] = -r[:, t] > fhs_var
        out[label] = (hs_hits[:, :20].mean(), hs_hits[:, 20:].mean(), fhs_hits[:, :20].mean(), fhs_hits[:, 20:].mean())
        print(f"  {label}: HS days 1-20 {out[label][0]:.2%}, days 21-60 {out[label][1]:.2%}; "
              f"FHS days 1-20 {out[label][2]:.2%}, days 21-60 {out[label][3]:.2%}")  # fmt: skip
    check("calm to stressed, HS exception rate days 1-20", out["calm to stressed"][0], 0.0717, 5e-5)
    check("calm to stressed, HS days 21-60", out["calm to stressed"][1], 0.0472, 5e-5)
    check("calm to stressed, FHS days 1-20", out["calm to stressed"][2], 0.0348, 1e-4)
    check("calm to stressed, FHS days 21-60", out["calm to stressed"][3], 0.0117, 5e-5)
    check("stressed to calm, HS days 1-20", out["stressed to calm"][0], 0.0009, 5e-5)
    check("stressed to calm, FHS days 21-60", out["stressed to calm"][3], 0.0078, 5e-5)
    check("stressed to calm, HS days 21-60", out["stressed to calm"][1], 0.0009, 5e-5)
    check("stressed to calm, FHS days 1-20", out["stressed to calm"][2], 0.0020, 5e-5)


# ---------------------------------------------------------------------------
# Copula tail dependence
# ---------------------------------------------------------------------------


def t_cdf(x: float, nu: float) -> float:
    c = math.gamma((nu + 1) / 2) / (math.sqrt(nu * math.pi) * math.gamma(nu / 2))
    nodes, weights = np.polynomial.legendre.leggauss(400)
    z = 0.5 * x * (nodes + 1.0)
    return 0.5 + float(np.sum(0.5 * x * weights * c * (1.0 + z * z / nu) ** (-(nu + 1) / 2)))


def t_copula_lambda(rho: float, nu: float) -> float:
    """Upper and lower tail dependence of the t copula: 2 t_{nu+1}(-sqrt((nu + 1)(1 - rho)/(1 + rho)))."""
    return 2.0 * t_cdf(-math.sqrt((nu + 1.0) * (1.0 - rho) / (1.0 + rho)), nu + 1.0)


def joint_tail_ratio(y: np.ndarray, q: float) -> float:
    """Empirical P(Y2 below its q-quantile | Y1 below its q-quantile)."""
    a = y[:, 0] <= np.quantile(y[:, 0], q)
    b = y[:, 1] <= np.quantile(y[:, 1], q)
    return float(np.mean(a & b) / q)


def section_copula() -> None:
    print("\n[Core concepts: tail dependence, Gaussian against t copula, rho = 0.5]")
    rho, nu = 0.5, 4.0
    lam = t_copula_lambda(rho, nu)
    check("t copula tail dependence, nu = 4, rho = 0.5", lam, 0.2532, 5e-5)
    check("argument sqrt(5 x 0.5 / 1.5)", math.sqrt(5.0 * 0.5 / 1.5), 1.291, 5e-4)
    check("t copula tail dependence, nu = 10, rho = 0.5", t_copula_lambda(rho, 10.0), 0.0819, 5e-5)
    rng = np.random.default_rng(99)
    n = 2_000_000
    chol = np.linalg.cholesky(np.array([[1.0, rho], [rho, 1.0]]))
    z = rng.standard_normal((n, 2)) @ chol.T
    w = rng.chisquare(nu, n)
    t = z / np.sqrt(w / nu)[:, None]
    for q in (0.01, 0.001):
        g, tt = joint_tail_ratio(z, q), joint_tail_ratio(t, q)
        print(f"  q = {q}: Gaussian P(joint | one) {g:.4f}, t(4) {tt:.4f}")
    check("Gaussian, q = 0.01", joint_tail_ratio(z, 0.01), 0.1316, 5e-4)
    check("Gaussian, q = 0.001", joint_tail_ratio(z, 0.001), 0.0515, 5e-4)
    check("t(4), q = 0.01", joint_tail_ratio(t, 0.01), 0.2933, 5e-4)
    check("t(4), q = 0.001", joint_tail_ratio(t, 0.001), 0.2660, 5e-4)


# ---------------------------------------------------------------------------
# Variance reduction: antithetics and quasi-Monte Carlo
# ---------------------------------------------------------------------------


def section_variance_reduction() -> None:
    print("\n[Core concepts: antithetic variates, efficiency against two independent draws]")
    rng = np.random.default_rng(5)
    z = rng.standard_normal(1_000_000)
    s = 100.0 * np.exp(-0.5 * 0.04 + 0.2 * z)
    s_anti = 100.0 * np.exp(-0.5 * 0.04 - 0.2 * z)
    payoffs = {
        "forward S - 100": (s - 100.0, s_anti - 100.0),
        "call max(S - 100, 0)": (np.maximum(s - 100.0, 0.0), np.maximum(s_anti - 100.0, 0.0)),
        "straddle |S - 100|": (np.abs(s - 100.0), np.abs(s_anti - 100.0)),
    }
    ratios, corrs = {}, {}
    for name, (a, b) in payoffs.items():
        ratio = float(np.var((a + b) / 2.0) / (np.var(a) / 2.0))
        corr = float(np.corrcoef(a, b)[0, 1])
        ratios[name] = ratio
        corrs[name] = corr
        print(f"  {name:<22}: corr(f(z), f(-z)) {corr:+.4f}, variance ratio {ratio:.4f}")
    check("variance ratio, forward", ratios["forward S - 100"], 0.0391, 5e-4)
    check("antithetic correlation, forward", corrs["forward S - 100"], -0.961, 5e-4)
    check("antithetic correlation, call", corrs["call max(S - 100, 0)"], -0.367, 5e-4)
    check("antithetic correlation, straddle", corrs["straddle |S - 100|"], 0.899, 5e-4)
    check("variance ratio, call", ratios["call max(S - 100, 0)"], 0.6321, 5e-4)
    check("variance ratio, straddle", ratios["straddle |S - 100|"], 1.8985, 5e-4)
    print("\n[Core concepts: Halton points against pseudo-random, E[exp(0.2 Z1 + 0.3 Z2)] = exp(0.065)]")
    exact = math.exp(0.065)
    check("exact value", exact, 1.0672, 5e-5)
    for n in (1024, 16384):
        u1, u2 = halton(n, 2), halton(n, 3)
        z1, z2 = box_muller(u1, u2)
        qmc_err = abs(float(np.mean(np.exp(0.2 * z1 + 0.3 * z2))) - exact)
        mc = []
        for rep in range(200):
            g = np.random.default_rng(1000 + rep).standard_normal((n, 2))
            mc.append(float(np.mean(np.exp(0.2 * g[:, 0] + 0.3 * g[:, 1]))) - exact)
        rmse = math.sqrt(float(np.mean(np.square(mc))))
        print(f"  N = {n:>5}: Halton error {qmc_err:.2e}, pseudo-random RMSE {rmse:.2e}")
        if n == 1024:
            check("Halton error x 1e5, N = 1024", qmc_err * 1e5, 99.6, 0.05)
            check("pseudo-random RMSE x 1e5, N = 1024", rmse * 1e5, 1285, 1.0)
            check("RMSE / Halton error, N = 1024", rmse / qmc_err, 12.9, 0.05)
        else:
            check("Halton error x 1e5, N = 16384", qmc_err * 1e5, 7.66, 0.05)
            check("pseudo-random RMSE x 1e5, N = 16384", rmse * 1e5, 298, 1.0)
            check("RMSE / Halton error, N = 16384", rmse / qmc_err, 38.9, 0.05)


def halton(n: int, base: int) -> np.ndarray:
    """First n points (starting at index 1) of the van der Corput sequence in `base`."""
    out = np.zeros(n)
    idx = np.arange(1, n + 1)
    f = 1.0
    while np.any(idx > 0):
        f /= base
        out += f * (idx % base)
        idx //= base
    return out


def box_muller(u1: np.ndarray, u2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    r = np.sqrt(-2.0 * np.log(u1))
    return r * np.cos(2.0 * math.pi * u2), r * np.sin(2.0 * math.pi * u2)


# ---------------------------------------------------------------------------
# Horizons: square root of time under GARCH and mean reversion; overlapping windows; scenario counts
# ---------------------------------------------------------------------------


def section_horizons() -> None:
    print("\n[Core concepts: 10-day scaling]")
    persistence, sig_bar, sig_next = 0.98, 0.01, 0.02
    var10 = sum(sig_bar**2 + persistence ** (k - 1) * (sig_next**2 - sig_bar**2) for k in range(1, 11))
    check("GARCH 10-day vol from a 2% day-ahead vol, persistence 0.98", math.sqrt(var10), 0.06119, 5e-5)
    check("sqrt(10) x 2%", math.sqrt(10.0) * sig_next, 0.06325, 5e-5)
    check("ratio", math.sqrt(var10) / (math.sqrt(10.0) * sig_next), 0.9675, 5e-5)
    check("sqrt(10) overstatement", math.sqrt(10.0) * sig_next / math.sqrt(var10) - 1.0, 0.0336, 5e-5)
    a, h = 0.5, 1.0
    check("OU variance over 1 year / random-walk variance, a = 0.5", (1.0 - math.exp(-2 * a * h)) / (2 * a * h), 0.6321, 5e-5)
    check("same over 10 days", (1.0 - math.exp(-2 * a * 10 / 252)) / (2 * a * 10 / 252), 0.9804, 5e-5)
    print("\n[Core concepts: overlapping 10-day windows (MAR33.4(7)), 97.5% ES of a normal, 2,000 trials of 259 days]")
    rng = np.random.default_rng(31)
    es_true = math.sqrt(10.0) * npdf(1.959963984540054) / 0.025
    over, nonover = [], []
    for _ in range(2000):
        r = rng.standard_normal(259)
        csum = np.concatenate([[0.0], np.cumsum(r)])
        ten_over = csum[10:] - csum[:-10]  # 250 overlapping sums
        ten_non = ten_over[::10]  # 25 non-overlapping
        for arr, out in ((ten_over, over), (ten_non, nonover)):
            losses = np.sort(-arr)[::-1]
            k = max(1, int(round(0.025 * len(arr))))
            out.append(float(losses[:k].mean()))
    check("true 10-day 97.5% ES of iid N(0,1) days, sqrt(10) phi(z) / 0.025", es_true, 7.3928, 5e-5)
    print(f"  overlapping: mean {np.mean(over):.3f}, sd {np.std(over):.3f}")
    print(f"  non-overlapping: mean {np.mean(nonover):.3f}, sd {np.std(nonover):.3f}")
    check("mean ES estimate, overlapping", float(np.mean(over)), 6.916, 5e-4)
    check("mean ES estimate, non-overlapping (the largest of 25)", float(np.mean(nonover)), 6.228, 5e-4)
    check("sd of ES estimate, overlapping", float(np.std(over)), 1.307, 5e-4)
    check("sd of ES estimate, non-overlapping", float(np.std(nonover)), 1.611, 5e-4)
    print("\n[Core concepts: Monte Carlo error of a 99% VaR estimate]")
    f_q = npdf(Z99)
    for n in (1000, 10000):
        se = math.sqrt(0.99 * 0.01 / n) / f_q
        print(f"  N = {n}: s.e. {se:.4f} sigma, {se / Z99:.2%} of VaR")
    check("density at the 99% quantile", f_q, 0.02665, 5e-6)
    check("s.e. of the 99% quantile, N = 1,000 (sigma units)", math.sqrt(0.0099 / 1000) / f_q, 0.1181, 5e-5)
    check("as a share of VaR", math.sqrt(0.0099 / 1000) / f_q / Z99, 0.0507, 5e-5)
    check("share of VaR, N = 10,000", math.sqrt(0.0099 / 10000) / f_q / Z99, 0.0160, 5e-5)
    check("s.e., N = 10,000 (sigma units)", math.sqrt(0.0099 / 10000) / f_q, 0.0373, 5e-5)
    sims = [float(np.quantile(-np.random.default_rng(500 + i).standard_normal(1000), 0.99)) for i in range(2000)]
    check("simulated sd of the 99% quantile, N = 1,000 (2,000 trials)", float(np.std(sims)), 0.1155, 5e-4)


def main() -> None:
    section_examples()
    section_backtest()
    section_regime_switch()
    section_copula()
    section_variance_reduction()
    section_horizons()
    print("\nAll scenario generation checks passed.")


if __name__ == "__main__":
    main()
