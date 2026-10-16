"""Dispersion and correlation trading: implied correlation, weighting schemes and an exact P&L decomposition.

Backs every number quoted in ``15-Dispersion-and-Correlation-Trading.md``: each value is printed and asserted.

1. Index variance as a weighted sum of covariances; exact implied correlation and the sigma_I^2 / (sum w sigma)^2 proxy.
2. Variance-swap strikes from the 1/K^2 strip for a flatter single-stock smile and a steeper index smile;
   implied correlation read at different strikes (correlation skew) and from variance strikes.
3. Straddle dispersion hedge ratios: vega-, theta- and gamma-neutral.
4. Variance-swap dispersion: correlation-weighted notionals, one simulated year with the P&L split exactly
   into a volatility term and a correlation term, a Monte Carlo of the P&L distribution, and a crash scenario.
5. The sign of a worst-of option's correlation sensitivity, by Monte Carlo.

Run from the repo root: ``uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/dispersion_correlation.py``.
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price, norm_pdf

# The five-stock basket used throughout: index weights and three-month ATM implied vols; index ATM vol 20%.
W = np.array([0.30, 0.25, 0.20, 0.15, 0.10])
SIG = np.array([0.25, 0.30, 0.35, 0.28, 0.40])
SIG_I = 0.20
DAYS = 252


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a quoted number and assert it to a tolerance, so drift in the note fails CI."""
    print(f"{name:58s} {value:14.6f}")
    assert abs(value - expected) <= tol, f"{name}: {value} vs expected {expected}"
    return value


def variance_parts(w: np.ndarray, sig: np.ndarray) -> tuple[float, float]:
    """A = sum w_i^2 sig_i^2 (own-variance part), B = sum_{i != j} w_i w_j sig_i sig_j (cross part)."""
    ws = w * sig
    a = float(ws @ ws)
    return a, float(ws.sum() ** 2 - a)


def implied_corr(w: np.ndarray, sig: np.ndarray, sig_i: float) -> float:
    """Exact equicorrelation that reproduces the index variance: (sig_I^2 - A) / B."""
    a, b = variance_parts(w, sig)
    return (sig_i**2 - a) / b


def proxy_corr(w: np.ndarray, sig: np.ndarray, sig_i: float) -> float:
    """Common proxy sig_I^2 / (sum w_i sig_i)^2, which drops the own-variance terms."""
    return sig_i**2 / float(w @ sig) ** 2


def svi_like(atm_vol: float, b: float, rho: float, s: float, T: float = 1.0):
    """Total implied variance w(k) = atm^2 T + b (rho k + sqrt(k^2 + s^2) - s); exact ATM vol at k = 0."""

    def w(k: np.ndarray) -> np.ndarray:
        return atm_vol**2 * T + b * (rho * k + np.sqrt(k * k + s * s) - s)

    return w


def var_strike(total_var, T: float = 1.0, F: float = 100.0) -> float:
    """Fair variance strike (r = 0) from the 1/K^2 strip of OTM options, integrated in log-strike."""
    k = np.linspace(-4.0, 4.0, 16001)
    K = F * np.exp(k)
    vol = np.sqrt(total_var(k) / T)
    otm = np.where(k < 0, bs_price(F, K, T, 0.0, vol, call=False), bs_price(F, K, T, 0.0, vol, call=True))
    integrand = otm / K  # P(K)/K^2 dK = P(K)/K dk
    return float(2.0 / T * np.sum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(k)))


def straddle_greeks(sig: float, T: float, S: float = 100.0) -> tuple[float, float, float]:
    """ATM straddle at r = 0: vega per vol point, theta per calendar day, gamma P&L of a 1% move."""
    sd = sig * math.sqrt(T)
    phi = float(norm_pdf(0.5 * sd))
    vega = 2 * S * phi * math.sqrt(T) * 0.01
    theta = 2 * (-S * phi * sig / (2 * math.sqrt(T))) / 365
    gamma = 2 * phi / (S * sd)
    return vega, theta, 0.5 * gamma * S * S * 0.01**2


def corr_weighted_notionals(n_index: float, w: np.ndarray, sig: np.ndarray, rho: float) -> np.ndarray:
    """Stock variance notionals that cancel the first-order vol exposure of a short index variance swap.

    At fixed correlation rho, d(sig_I^2)/d(sig_i^2) = w_i^2 + rho w_i sum_{j != i} w_j sig_j / sig_i.
    """
    ws = w * sig
    others = ws.sum() - ws
    return n_index * (w * w + rho * w * others / sig)


def dispersion_pnl(n_index: float, n_stock: np.ndarray, w: np.ndarray, k_vol: np.ndarray, k_ivol: float, r_vol: np.ndarray, r_ivar: float):
    """P&L of long stock variance / short index variance, in currency, with variances in vol points squared.

    Identity: index variance = A + rho B. With rho_K implied and rho_R := (sig_IR^2 - A_R) / B_R realised,
      total = vol term + corr term,
      vol term = sum N_i (sig_iR^2 - K_i) - N_I [(A_R - A_K) + rho_K (B_R - B_K)],
      corr term = -N_I (rho_R - rho_K) B_R.
    """
    a_k, b_k = variance_parts(w, k_vol)
    a_r, b_r = variance_parts(w, r_vol)
    rho_k = (k_ivol**2 - a_k) / b_k
    rho_r = (r_ivar - a_r) / b_r
    total = float(n_stock @ (r_vol**2 - k_vol**2)) - n_index * (r_ivar - k_ivol**2)
    vol_term = float(n_stock @ (r_vol**2 - k_vol**2)) - n_index * ((a_r - a_k) + rho_k * (b_r - b_k))
    corr_term = -n_index * (rho_r - rho_k) * b_r
    return total, vol_term, corr_term, rho_r


def simulate_year(rng: np.random.Generator, vols: np.ndarray, rho: float, paths: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Daily lognormal returns with equicorrelation rho; index return = sum w_i r_i (constant-weight index).

    Returns realised vols per stock and realised index variance, contract convention (252/n sum ln^2, no mean),
    in vol points and vol points squared, plus the daily log returns (paths, days, stocks).
    """
    n = len(vols)
    corr = np.full((n, n), rho) + (1 - rho) * np.eye(n)
    chol = np.linalg.cholesky(corr)
    dt = 1.0 / DAYS
    z = rng.standard_normal((paths, DAYS, n)) @ chol.T
    log_r = vols * math.sqrt(dt) * z - 0.5 * vols**2 * dt
    simple = np.expm1(log_r)
    log_index = np.log1p(simple @ W)
    r_vol = 100 * np.sqrt(DAYS / DAYS * np.sum(log_r**2, axis=1))  # 252/n with n = 252
    r_ivar = 1e4 * np.sum(log_index**2, axis=1)
    return r_vol, r_ivar, log_r


def main() -> None:
    # Backs: Core concepts "Index variance and implied correlation", Worked example 1;
    # cards deriv-disp-index-variance, deriv-disp-implied-corr-formula, deriv-disp-basket-number, deriv-disp-index-vol-bounds.
    print("1. Implied correlation of the five-stock basket")
    a, b = variance_parts(W, SIG)
    check("weighted average vol sum w_i sig_i", float(W @ SIG), 0.302, 1e-12)
    check("own-variance part A = sum w^2 sig^2", a, 0.019514, 1e-9)
    check("cross part B at rho = 1", b, 0.07169, 1e-9)
    rho_k = check("exact implied correlation", implied_corr(W, SIG, SIG_I), 0.285758, 1e-6)
    check("proxy sig_I^2 / (sum w sig)^2", proxy_corr(W, SIG, SIG_I), 0.438577, 1e-6)
    check("proxy minus exact", proxy_corr(W, SIG, SIG_I) - implied_corr(W, SIG, SIG_I), 0.152819, 1e-6)
    check("index vol if rho = 1, sqrt(A + B)", math.sqrt(a + b), 0.302, 1e-12)
    check("index vol if rho = 0, sqrt(A + 0 B)", math.sqrt(a + 0.0 * b), 0.139693, 1e-6)
    w50 = np.full(50, 1 / 50)
    check("50 names at 30%, index 18%: exact", implied_corr(w50, np.full(50, 0.30), 0.18), 0.346939, 1e-6)
    check("50 names at 30%, index 18%: proxy", proxy_corr(w50, np.full(50, 0.30), 0.18), 0.36, 1e-12)
    check("index vol per +0.10 correlation (sig_I at rho_K + 0.1)", math.sqrt(a + (rho_k + 0.1) * b), 0.217184, 1e-6)

    # Backs: Core concepts (correlation skew paragraph), Worked example 2;
    # cards deriv-corr-skew, deriv-corr-variance-strike-correlation.
    print("\n2. Strip variance strikes, correlation skew (one year, r = 0, F = 100)")
    flat = var_strike(lambda k: np.full_like(k, 0.04))
    check("flat 20% smile strip strike (vol)", 100 * math.sqrt(flat), 20.0, 1e-3)
    stock_smiles = [svi_like(s, 0.04, -0.3, 0.1) for s in SIG]
    index_smile = svi_like(SIG_I, 0.10, -0.7, 0.1)
    k_stock = np.array([var_strike(f) for f in stock_smiles])
    k_index = var_strike(index_smile)
    check("stock 1 (ATM 25) variance strike (vol)", 100 * math.sqrt(k_stock[0]), 26.306, 1e-3)
    check("stock 1 strike minus ATM (vol points)", 100 * math.sqrt(k_stock[0]) - 25.0, 1.306, 1e-3)
    check("index (ATM 20) variance strike (vol)", 100 * math.sqrt(k_index), 25.046, 1e-3)
    check("index strike minus ATM (vol points)", 100 * math.sqrt(k_index) - 20.0, 5.046, 1e-3)
    rho_var = implied_corr(W, np.sqrt(k_stock), math.sqrt(k_index))
    check("implied correlation from variance strikes", rho_var, 0.52827, 1e-5)
    check("variance-strike minus ATM implied correlation", rho_var - rho_k, 0.24251, 1e-5)
    for label, m, expected in (("90%", 0.9, 0.42749), ("100%", 1.0, 0.285758), ("110%", 1.1, 0.24367)):
        k = np.array([math.log(m)])
        s_i = np.array([math.sqrt(f(k)[0]) for f in stock_smiles])
        check(f"implied correlation at {label} strike", implied_corr(W, s_i, math.sqrt(index_smile(k)[0])), expected, 1e-5)

    # Backs: Core concepts "Weighting schemes" table, Worked example 3;
    # cards deriv-disp-weighting-schemes, deriv-disp-gamma-neutral-meaning.
    print("\n3. Straddle dispersion hedge ratios (3-month ATM, all spots 100, r = 0)")
    T = 0.25
    g_i = straddle_greeks(SIG_I, T)
    g_s = np.array([straddle_greeks(s, T) for s in SIG])
    check("index straddle price", 2 * bs_price(100.0, 100.0, T, 0.0, SIG_I), 7.97552, 1e-5)
    check("index straddle vega per vol point", g_i[0], 0.398444, 1e-6)
    check("index straddle theta per day", g_i[1], -0.043665, 1e-6)
    check("index straddle gamma P&L per 1% move", g_i[2], 0.039844, 1e-6)
    h_vega = check("vega-neutral h (index vega / sum w vega_i)", g_i[0] / float(W @ g_s[:, 0]), 1.00167, 1e-5)
    h_theta = check("theta-neutral h", g_i[1] / float(W @ g_s[:, 1]), 0.66346, 1e-5)
    h_gamma = check("gamma-neutral h", g_i[2] / float(W @ g_s[:, 2]), 1.47698, 1e-5)
    check("vega-neutral book: net theta per day", h_vega * float(W @ g_s[:, 1]) - g_i[1], -0.022259, 1e-6)
    check("theta-neutral book: net vega per vol point", h_theta * float(W @ g_s[:, 0]) - g_i[0], -0.13453, 1e-5)
    check("gamma-neutral book: net vega per vol point", h_gamma * float(W @ g_s[:, 0]) - g_i[0], 0.18907, 1e-5)

    # Backs: Core concepts "Weighting schemes" (correlation-weighted notionals), Worked example 4;
    # card deriv-disp-corr-weighted-notional.
    print("\n4. Variance-swap dispersion, correlation-weighted (index vega notional 100,000)")
    n_index = 100_000 / (2 * 100 * SIG_I)
    check("index variance notional per variance point", n_index, 2500.0, 1e-9)
    kv = 100 * SIG
    kiv = 100 * SIG_I
    n_cw = corr_weighted_notionals(n_index, W, kv, rho_k)
    for i, (n, e) in enumerate(zip(n_cw, (419.60, 291.39, 194.71, 155.76, 71.79), strict=True)):
        check(f"stock {i + 1} variance notional", n, e, 5e-3)
    vega_cw = 2 * kv * n_cw
    check("sum of stock vega notionals (correlation-weighted)", float(vega_cw.sum()), 66_559, 1)
    n_vn = W * 100_000 / (2 * kv)
    check("vega-neutral stock 1 variance notional", n_vn[0], 600.0, 1e-9)

    # Backs: Core concepts "The exact P&L decomposition", Worked example 4 table;
    # cards deriv-disp-pnl-decomposition, deriv-corr-realised-noise, deriv-corr-swap-vs-dispersion.
    rng = np.random.default_rng(11)
    r_vol_true = np.array([0.20, 0.24, 0.40, 0.30, 0.45])
    rv, riv, log_r = simulate_year(rng, r_vol_true, 0.15, 1)
    total, vol_t, corr_t, rho_r = dispersion_pnl(n_index, n_cw, W, kv, kiv, rv[0], riv[0])
    for i, (v, e) in enumerate(zip(rv[0], (20.243, 24.832, 40.762, 30.547, 45.527), strict=True)):
        check(f"one path: realised vol stock {i + 1}", v, e, 5e-3)
    check("one path: realised index vol", math.sqrt(riv[0]), 17.987, 5e-3)
    check("one path: realised implied-style correlation rho_R", rho_r, 0.20263, 5e-5)
    check("one path: total P&L", total, 160_406, 5)
    check("one path: vol term", vol_t, 16_865, 5)
    check("one path: correlation term", corr_t, 143_541, 5)
    assert abs(total - vol_t - corr_t) < 1e-6, "decomposition must be exact"
    print("decomposition total - vol - corr                           0 (asserted to 1e-6)")
    c = np.corrcoef(log_r[0].T)
    iu = np.triu_indices(5, 1)
    pair_w = np.outer(W, W)[iu]
    check("one path: correlation-swap estimator, weighted pairs", float(pair_w @ c[iu] / pair_w.sum()), 0.20716, 1e-5)
    check("one path: correlation-swap estimator, equal-weighted pairs", float(c[iu].mean()), 0.21810, 1e-5)

    # Backs: Worked example 5 table (fair world and realised correlation 0.15); card deriv-disp-long-is-short-corr.
    rng = np.random.default_rng(12)
    paths = 4000
    rv, riv, _ = simulate_year(rng, SIG, rho_k, paths)
    res = np.array([dispersion_pnl(n_index, n_cw, W, kv, kiv, rv[p], riv[p]) for p in range(paths)])
    check("fair world: mean P&L", res[:, 0].mean(), -767, 300)
    check("fair world: s.d. P&L", res[:, 0].std(), 55_740, 500)
    check("fair world: standard error of the mean", res[:, 0].std() / math.sqrt(paths), 881, 10)
    check("fair world: s.d. vol term", res[:, 1].std(), 668, 20)
    check("fair world: s.d. correlation term", res[:, 2].std(), 55_750, 500)
    rv, riv, _ = simulate_year(rng, SIG, 0.15, paths)
    res = np.array([dispersion_pnl(n_index, n_cw, W, kv, kiv, rv[p], riv[p]) for p in range(paths)])
    check("realised corr 0.15: mean P&L", res[:, 0].mean(), 243_290, 500)
    check("realised corr 0.15: s.d. P&L", res[:, 0].std(), 48_260, 500)
    check("realised corr 0.15: mean correlation term", res[:, 2].mean(), 242_290, 500)
    a_k, b_k = variance_parts(W, kv)
    check("first-order estimate N_I (rho_K - 0.15) B_K", n_index * (rho_k - 0.15) * b_k, 243_312.5, 1)

    # Vol shocks at the implied correlation: correlation-weighted vs vega-neutral notionals.
    # Backs: Worked example 5 (last paragraph); cards deriv-disp-corr-weighted-notional, deriv-disp-weighting-schemes.
    rng = np.random.default_rng(13)
    m = np.exp(0.3 * rng.standard_normal((paths, 1)) + 0.15 * rng.standard_normal((paths, 5)))
    r_vol = kv * m
    index_var = np.array([variance_parts(W, v)[0] + rho_k * variance_parts(W, v)[1] for v in r_vol])
    cw = np.array([dispersion_pnl(n_index, n_cw, W, kv, kiv, r_vol[p], index_var[p])[0] for p in range(paths)])
    vn = np.array([dispersion_pnl(n_index, n_vn, W, kv, kiv, r_vol[p], index_var[p])[0] for p in range(paths)])
    check("vol shocks at rho_K: s.d. P&L correlation-weighted", cw.std(), 16_180, 200)
    check("vol shocks at rho_K: s.d. P&L vega-neutral", vn.std(), 446_310, 2000)
    check("vol shocks at rho_K: mean P&L vega-neutral", vn.mean(), 150_820, 2000)

    # Backs: TL;DR (four times), Worked example 6; cards deriv-disp-crash, deriv-corr-swap-vs-dispersion.
    print("\n5. Crash scenario: realised vols double, realised correlation 0.9")
    crash_vol = 2 * kv
    a_c, b_c = variance_parts(W, crash_vol)
    total, vol_t, corr_t, rho_c = dispersion_pnl(n_index, n_cw, W, kv, kiv, crash_vol, a_c + 0.9 * b_c)
    check("crash: realised index vol", math.sqrt(a_c + 0.9 * b_c), 57.978, 5e-3)
    check("crash: total P&L", total, -4_403_500, 1)
    check("crash: vol term", vol_t, 0.0, 1e-6)
    check("crash: correlation term", corr_t, -4_403_500, 1)
    a_k, b_k = variance_parts(W, kv)
    n_rho = n_index * b_k
    check("correlation swap notional with the same initial rho exposure", n_rho, 1_792_250, 1e-6)
    check("that correlation swap in the crash", -n_rho * (0.9 - rho_k), -1_100_875, 1)
    check("ratio B_R / B_K", b_c / b_k, 4.0, 1e-12)

    # Backs: Core concepts "Who trades it" (worst-of sign), Worked example 7; card deriv-corr-worst-of-sign.
    print("\n6. Worst-of options on two stocks (S = K = 100, sigma 25%, T = 1, r = 0)")
    rng = np.random.default_rng(5)
    z1 = rng.standard_normal(400_000)
    z2 = rng.standard_normal(400_000)
    for rho, put_e, call_e in ((0.2, 15.73, 3.19), (0.5, 14.48, 4.55), (0.8, 12.79, 6.50)):
        x2 = rho * z1 + math.sqrt(1 - rho * rho) * z2
        s1 = 100 * np.exp(-0.5 * 0.0625 + 0.25 * z1)
        s2 = 100 * np.exp(-0.5 * 0.0625 + 0.25 * x2)
        lo = np.minimum(s1, s2)
        check(f"worst-of put, rho = {rho}", float(np.maximum(100 - lo, 0).mean()), put_e, 0.01)
        check(f"worst-of call, rho = {rho}", float(np.maximum(lo - 100, 0).mean()), call_e, 0.01)
    check("rho = 1 limit: Black-Scholes call", bs_price(100.0, 100.0, 1.0, 0.0, 0.25), 9.94764, 1e-5)
    check("rho = 1 limit: Black-Scholes put", bs_price(100.0, 100.0, 1.0, 0.0, 0.25, call=False), 9.94764, 1e-5)
    s1 = 100 * np.exp(-0.5 * 0.0625 + 0.25 * z1)
    check("rho = 1 limit: worst-of put by Monte Carlo", float(np.maximum(100 - s1, 0).mean()), 9.95, 0.05)


if __name__ == "__main__":
    main()
