"""Market impact: square-root law, the Almgren et al. (2005) cost model, and propagator (transient impact) simulations.

Backs every number in 06-Market-Impact-Models.md.
Run ``python market_impact.py``: each result is printed and asserted.
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


def sqrt_law_bp(sigma_daily: float, q_over_v: float, y: float = 1.0) -> float:
    """Square-root law peak impact in basis points: Y sigma sqrt(Q/V)."""
    return y * sigma_daily * math.sqrt(q_over_v) * 1e4


def square_root_law() -> None:
    print("== Square-root law, sigma = 2% daily, Y = 1 ==")
    for frac, bp in ((0.001, 6.32), (0.01, 20.0), (0.05, 44.72), (0.10, 63.25), (0.25, 100.0)):
        check(f"impact at Q/V = {frac:.1%} (bp)", sqrt_law_bp(0.02, frac), bp, 0.005)
    # Dollar cost of 100,000 shares of a $50 stock trading 2,000,000 a day
    notional = 100_000 * 50.0
    check("notional ($)", notional, 5_000_000.0, 1e-6)
    check("cost of 5% ADV at 44.72 bp ($)", notional * sqrt_law_bp(0.02, 0.05) / 1e4, 22_360.68, 0.005)
    check("per-share cost doubling ratio (2x size)", sqrt_law_bp(0.02, 0.10) / sqrt_law_bp(0.02, 0.05), math.sqrt(2), 1e-12)
    check("total cost ratio for 2x size", 2 * sqrt_law_bp(0.02, 0.10) / sqrt_law_bp(0.02, 0.05), 2.828427, 5e-7)
    # Fair-pricing argument: average price paid = mean of sqrt(q) over the order = 2/3 of peak impact
    q = np.linspace(0, 1, 1_000_001)
    avg = float(np.trapezoid(np.sqrt(q), q))
    check("average impact paid / peak impact (sqrt path)", avg, 2 / 3, 1e-6)
    check("fair-pricing permanent impact for a 30 bp peak (bp)", 30 * avg, 20.0, 1e-4)


def almgren_2005() -> None:
    print("== Almgren, Thum, Hauptmann and Li (2005) cost model ==")
    gamma, eta, alpha, beta, delta = 0.314, 0.142, 1.0, 0.6, 0.25
    # Inputs from their Table 3: V (shares/day), Theta (shares out), sigma (daily), X/V = 0.1
    stocks = {"IBM": (6.561e6, 1728e6, 0.0157), "DRI": (1.929e6, 168e6, 0.0226)}
    published = {
        "IBM": {"I_over_sigma": 0.126, "I": 20, "K": (22, 15, 8), "J": (32, 25, 18)},
        "DRI": {"I_over_sigma": 0.096, "I": 22, "K": (32, 21, 12), "J": (43, 32, 23)},
    }
    quoted = {
        "IBM": {"I": 19.9, "K": (22.3, 14.7, 8.5), "J": (32.2, 24.6, 18.4)},
        "DRI": {"I": 21.7, "K": (32.1, 21.2, 12.2), "J": (42.9, 32.0, 23.1)},
    }
    for name, (vol, shares_out, sigma) in stocks.items():
        x_over_v = 0.1
        i_over_sigma = gamma * x_over_v**alpha * (shares_out / vol) ** delta
        i_bp = i_over_sigma * sigma * 1e4
        check(f"{name} Theta/V", shares_out / vol, {"IBM": 263.37, "DRI": 87.09}[name], 0.005)
        check(f"{name} I/sigma", i_over_sigma, published[name]["I_over_sigma"], 5e-4)
        check(f"{name} permanent impact I (bp)", i_bp, published[name]["I"], 0.5)
        check(f"{name} permanent impact I (bp), as quoted", i_bp, quoted[name]["I"], 0.05)
        rows = zip((0.1, 0.2, 0.5), published[name]["K"], published[name]["J"], quoted[name]["K"], quoted[name]["J"], strict=True)
        for t_days, k_pub, j_pub, k_quoted, j_quoted in rows:
            k_over_sigma = eta * (x_over_v / t_days) ** beta
            k_bp = k_over_sigma * sigma * 1e4
            j_bp = i_bp / 2 + k_bp
            check(f"{name} T={t_days} K/sigma", k_over_sigma, {0.1: 0.142, 0.2: 0.094, 0.5: 0.054}[t_days], 5e-4)
            check(f"{name} T={t_days} temporary K (bp)", k_bp, k_pub, 0.5)
            check(f"{name} T={t_days} realised cost J (bp)", j_bp, j_pub, 0.5)
            check(f"{name} T={t_days} temporary K (bp), as quoted", k_bp, k_quoted, 0.05)
            check(f"{name} T={t_days} realised cost J (bp), as quoted", j_bp, j_quoted, 0.05)


def metaorder_path(kernel: np.ndarray, duration: int, horizon: int) -> np.ndarray:
    """Impact I(t) of buying one unit per step for `duration` steps; I(t) = sum_{s < min(t, T)} G(t - s)."""
    path = np.zeros(horizon + 1)
    for t in range(1, horizon + 1):
        lags = t - np.arange(min(t, duration))
        path[t] = kernel[lags].sum()
    return path


def propagator_decay() -> None:
    print("== Transient impact of a metaorder ==")
    horizon = 4_000
    lags = np.arange(horizon + 1, dtype=float)
    power = np.zeros(horizon + 1)
    power[1:] = lags[1:] ** -0.5
    for duration, peak in ((100, 18.5896), (400, 38.5646)):
        path = metaorder_path(power, duration, max(horizon, 10 * duration))
        check(f"peak impact, T = {duration}, beta = 1/2", path[duration], peak, 5e-5)
    p100 = metaorder_path(power, 100, horizon)
    p400 = metaorder_path(power, 400, horizon)
    check("peak ratio T=400 vs T=100", p400[400] / p100[100], 2.0745, 5e-5)
    for mult, frac in ((2, 0.4294), (5, 0.2448), (10, 0.1683)):
        check(f"I({mult}T)/I(T), power law beta = 1/2, T = 400", p400[mult * 400] / p400[400], frac, 5e-5)
    check("continuum value sqrt(2) - 1", math.sqrt(2) - 1, 0.414214, 5e-7)
    check("continuum value sqrt(5) - 2", math.sqrt(5) - 2, 0.236068, 5e-7)
    check("continuum value sqrt(10) - 3", math.sqrt(10) - 3, 0.162278, 5e-7)
    # Exponential kernel with the same peak timescale: decays geometrically
    rho = 1 / 100
    expo = np.exp(-rho * lags)
    pe = metaorder_path(expo, 400, horizon)
    check("I(2T)/I(T), exponential kernel, 1/rho = 100, T = 400", pe[800] / pe[400], math.exp(-4), 1e-12)
    check("I(2T)/I(T), exponential kernel, as quoted (%)", 100 * pe[800] / pe[400], 1.8, 0.05)


def fgn_davies_harte(n: int, hurst: float, rng: np.random.Generator) -> np.ndarray:
    """Exact fractional Gaussian noise of length n by circulant embedding."""
    k = np.arange(n + 1, dtype=float)
    acov = 0.5 * ((k + 1) ** (2 * hurst) - 2 * k ** (2 * hurst) + np.abs(k - 1) ** (2 * hurst))
    row = np.concatenate([acov, acov[-2:0:-1]])
    eig = np.fft.fft(row).real
    assert eig.min() > -1e-8, "circulant embedding must be non-negative definite"
    eig = np.clip(eig, 0, None)
    m = len(row)
    z = rng.standard_normal(m) + 1j * rng.standard_normal(m)
    w = np.fft.fft(np.sqrt(eig / m) * z)
    return w.real[:n]


def propagator_diffusion() -> None:
    print("== Propagator model: long-memory signs and price diffusion ==")
    rng = np.random.default_rng(7)
    n, hurst, paths = 2**16, 0.75, 16
    gamma = 2 - 2 * hurst
    beta_c = (1 - gamma) / 2
    check("sign autocorrelation exponent gamma", gamma, 0.5, 1e-12)
    check("critical propagator exponent beta_c", beta_c, 0.25, 1e-12)
    signs = [np.sign(fgn_davies_harte(n, hurst, rng)) for _ in range(paths)]
    s = np.array(signs)
    c10 = float(np.mean(s[:, 10:] * s[:, :-10]))
    c100 = float(np.mean(s[:, 100:] * s[:, :-100]))
    rho = lambda lag: 0.5 * ((lag + 1) ** 1.5 - 2 * lag**1.5 + (lag - 1) ** 1.5)  # noqa: E731
    check("theoretical sign autocorrelation at lag 10", 2 / math.pi * math.asin(rho(10)), 0.0757, 5e-5)
    check("sample sign autocorrelation at lag 10", c10, 0.0759, 5e-5)
    check("theoretical sign autocorrelation at lag 100", 2 / math.pi * math.asin(rho(100)), 0.0239, 5e-5)
    check("sample sign autocorrelation at lag 100", c100, 0.0241, 5e-5)
    lag_short, lag_long = 16, 2_048
    results = {}
    for beta in (0.10, 0.25, 0.40):
        kernel = np.zeros(n)
        kernel[1:] = np.arange(1, n, dtype=float) ** -beta
        ratios = []
        for eps in s:
            size = 2 * n
            price = np.fft.irfft(np.fft.rfft(eps, size) * np.fft.rfft(kernel, size), size)[:n]
            v_short = np.mean((price[lag_short:] - price[:-lag_short]) ** 2) / lag_short
            v_long = np.mean((price[lag_long:] - price[:-lag_long]) ** 2) / lag_long
            ratios.append(v_long / v_short)
        results[beta] = float(np.mean(ratios))
    check("diffusion ratio D(2048)/D(16), beta = 0.10 (superdiffusive)", results[0.10], 3.80, 0.005)
    check("diffusion ratio D(2048)/D(16), beta = 0.25 (critical)", results[0.25], 0.94, 0.005)
    check("diffusion ratio D(2048)/D(16), beta = 0.40 (subdiffusive)", results[0.40], 0.26, 0.005)


if __name__ == "__main__":
    square_root_law()
    almgren_2005()
    propagator_decay()
    propagator_diffusion()
    print("all market impact checks passed")
