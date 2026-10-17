"""Volatility surface construction: SVI fit, Durrleman and calendar checks, SSVI, Dupire local vol.

Backs every number in ``05-Derivatives-and-Volatility/08-Volatility-Surface-Construction.md``.
Run from the repo root:

    uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/vol_surface_svi_dupire.py

Sections:
1. Raw SVI slice, its Lee wing slopes and Durrleman's butterfly function g(k).
2. Quasi-explicit SVI fit (linear in (a, d, c) for fixed (m, sigma), Nelder-Mead on (m, sigma)) to noisy synthetic quotes.
3. An arbitrageable slice (Vogt's example in Gatheral and Jacquier 2014) and a calendar-arbitrage pair.
4. SSVI surface with a power-law phi, its sufficient no-arbitrage conditions, checked on a grid.
5. Dupire local vol from prices (finite differences) and from total implied variance (analytic), cross-checked.
6. Local-vol Monte Carlo repricing of the surface, the short-maturity skew ratio, and the forward-smile flattening.
Every printed number is asserted against the value quoted in the note.
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price, implied_vol

# ---------------------------------------------------------------------------
# Raw SVI
# ---------------------------------------------------------------------------


def svi_w(k: np.ndarray, a: float, b: float, rho: float, m: float, sig: float) -> np.ndarray:
    """Raw SVI total implied variance w(k) = a + b (rho (k - m) + sqrt((k - m)^2 + sig^2))."""
    x = k - m
    return a + b * (rho * x + np.sqrt(x * x + sig * sig))


def svi_derivs(k: np.ndarray, a: float, b: float, rho: float, m: float, sig: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """w, w' and w'' of a raw SVI slice."""
    x = k - m
    s = np.sqrt(x * x + sig * sig)
    return a + b * (rho * x + s), b * (rho + x / s), b * sig * sig / s**3


def durrleman_g(w: np.ndarray, w1: np.ndarray, w2: np.ndarray, k: np.ndarray) -> np.ndarray:
    """Durrleman's g(k); the slice is free of butterfly arbitrage iff g >= 0 (and d_+ -> -inf on the right)."""
    return (1.0 - k * w1 / (2.0 * w)) ** 2 - 0.25 * w1 * w1 * (1.0 / w + 0.25) + 0.5 * w2


def nelder_mead(f, x0: np.ndarray, step: np.ndarray, iters: int = 400, tol: float = 1e-14) -> tuple[np.ndarray, float]:
    """Plain Nelder-Mead (reflection 1, expansion 2, contraction 1/2, shrink 1/2)."""
    n = len(x0)
    simplex = [np.asarray(x0, dtype=float)] + [np.asarray(x0, dtype=float) + np.eye(n)[i] * step[i] for i in range(n)]
    vals = [f(x) for x in simplex]
    for _ in range(iters):
        order = np.argsort(vals)
        simplex = [simplex[i] for i in order]
        vals = [vals[i] for i in order]
        if abs(vals[-1] - vals[0]) < tol:
            break
        centroid = np.mean(simplex[:-1], axis=0)
        xr = centroid + (centroid - simplex[-1])
        fr = f(xr)
        if fr < vals[0]:
            xe = centroid + 2.0 * (centroid - simplex[-1])
            fe = f(xe)
            simplex[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            simplex[-1], vals[-1] = xr, fr
        else:
            xc = centroid + 0.5 * (simplex[-1] - centroid)
            fc = f(xc)
            if fc < vals[-1]:
                simplex[-1], vals[-1] = xc, fc
            else:
                simplex = [simplex[0] + 0.5 * (x - simplex[0]) for x in simplex]
                vals = [f(x) for x in simplex]
    i = int(np.argmin(vals))
    return simplex[i], vals[i]


def svi_inner(k: np.ndarray, w: np.ndarray, wt: np.ndarray, m: float, sig: float) -> tuple[np.ndarray, float]:
    """For fixed (m, sig), w = a + d y + c sqrt(y^2 + 1) with y = (k - m)/sig is linear in (a, d, c): weighted least squares."""
    y = (k - m) / sig
    X = np.column_stack([np.ones_like(y), y, np.sqrt(y * y + 1.0)])
    sw = np.sqrt(wt)
    coef, *_ = np.linalg.lstsq(X * sw[:, None], w * sw, rcond=None)
    resid = X @ coef - w
    return coef, float(np.sum(wt * resid * resid))


def fit_svi(k: np.ndarray, w: np.ndarray, wt: np.ndarray) -> tuple[float, float, float, float, float]:
    """Quasi-explicit SVI calibration (Zeliade 2009): grid start, Nelder-Mead on (m, sig), linear inner solve."""

    def outer(p: np.ndarray) -> float:
        m, sig = p
        if sig < 1e-4:
            return 1e10
        return svi_inner(k, w, wt, m, sig)[1]

    grid = [(m, s) for m in np.linspace(-0.3, 0.3, 13) for s in (0.02, 0.05, 0.1, 0.2, 0.4)]
    start = min(grid, key=lambda p: outer(np.array(p)))
    best, _ = nelder_mead(outer, np.array(start), np.array([0.05, 0.03]))
    m, sig = best
    (a, d, c), _ = svi_inner(k, w, wt, m, sig)
    b = c / sig
    rho = d / c
    return a, b, rho, m, sig


# ---------------------------------------------------------------------------
# SSVI (Gatheral and Jacquier 2014) with a power-law phi
# ---------------------------------------------------------------------------

SSVI_RHO, SSVI_ETA, SSVI_GAMMA = -0.7, 1.0, 0.4
V0, VBAR, LAM = 0.03, 0.05, 1.0  # ATM total variance theta_t = vbar t + (v0 - vbar)(1 - e^{-lam t})/lam


def theta_t(t: np.ndarray) -> np.ndarray:
    return VBAR * t + (V0 - VBAR) * (1.0 - np.exp(-LAM * t)) / LAM


def dtheta_dt(t: np.ndarray) -> np.ndarray:
    return VBAR + (V0 - VBAR) * np.exp(-LAM * t)


def phi_of(th: np.ndarray, gamma: float = SSVI_GAMMA) -> np.ndarray:
    return SSVI_ETA / (th**gamma * (1.0 + th) ** (1.0 - gamma))


def dphi_dtheta(th: np.ndarray, gamma: float = SSVI_GAMMA) -> np.ndarray:
    return -phi_of(th, gamma) * (gamma / th + (1.0 - gamma) / (1.0 + th))


def ssvi_w(k: np.ndarray, t: np.ndarray, gamma: float = SSVI_GAMMA) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """SSVI w(k, t) and its derivatives w_k, w_kk, w_t (analytic)."""
    rho = SSVI_RHO
    th = theta_t(t)
    ph = phi_of(th, gamma)
    z = ph * k + rho
    s = np.sqrt(z * z + 1.0 - rho * rho)
    w = 0.5 * th * (1.0 + rho * ph * k + s)
    wk = 0.5 * th * ph * (rho + z / s)
    wkk = 0.5 * th * ph * ph * (1.0 - rho * rho) / s**3
    # d w / d theta at fixed k, through theta and phi(theta)
    dph = dphi_dtheta(th, gamma)
    dw_dth = 0.5 * (1.0 + rho * ph * k + s) + 0.5 * th * (rho * k + z * k / s) * dph
    return w, wk, wkk, dw_dth * dtheta_dt(t)


def local_var_from_w(k: np.ndarray, t: np.ndarray, gamma: float = SSVI_GAMMA) -> np.ndarray:
    """Dupire in total-implied-variance form (Gatheral 2006 eq. 1.10); the denominator is Durrleman's g."""
    w, wk, wkk, wt = ssvi_w(k, t, gamma)
    return wt / durrleman_g(w, wk, wkk, k)


S0, R, Q = 100.0, 0.03, 0.01


def fwd(t: np.ndarray) -> np.ndarray:
    return S0 * np.exp((R - Q) * t)


def ssvi_call(K: np.ndarray, t: np.ndarray) -> np.ndarray:
    k = np.log(K / fwd(t))
    w = ssvi_w(k, t)[0]
    return np.asarray(bs_price(S0, K, t, R, np.sqrt(w / t), Q))


def local_var_from_prices(K: float, t: float, hK: float = 0.05, ht: float = 1e-4) -> float:
    """Dupire in price form: sigma^2 = (C_T + (r - q) K C_K + q C) / (K^2 C_KK / 2), central differences."""
    c0 = float(ssvi_call(np.array(K), np.array(t)))
    cKp, cKm = (float(ssvi_call(np.array(K + s * hK), np.array(t))) for s in (1, -1))
    cTp, cTm = (float(ssvi_call(np.array(K), np.array(t + s * ht))) for s in (1, -1))
    cT = (cTp - cTm) / (2 * ht)
    cK = (cKp - cKm) / (2 * hK)
    cKK = (cKp - 2 * c0 + cKm) / hK**2
    return (cT + (R - Q) * K * cK + Q * c0) / (0.5 * K * K * cKK)


def local_vol_mc(n_paths: int, n_steps: int, T: float, seed: int) -> dict[float, np.ndarray]:
    """Log-Euler simulation of dS/S = (r - q) dt + sigma_loc(t, S) dW with antithetic pairs."""
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    x = np.zeros(2 * n_paths)  # log(S_t / F_t), so the drift is only the Ito term
    snaps = {}
    for i in range(n_steps):
        t = max(i * dt, 1e-4)  # sigma_loc(0, .) is the t -> 0 limit; 1e-4 years is close enough
        lv = np.sqrt(local_var_from_w(x, np.array(t)))
        z = rng.standard_normal(n_paths)
        z = np.concatenate([z, -z])
        x += -0.5 * lv * lv * dt + lv * math.sqrt(dt) * z
        t_next = (i + 1) * dt
        for snap_t in (0.5, 1.0):
            if abs(t_next - snap_t) < 1e-12:
                snaps[snap_t] = fwd(np.array(snap_t)) * np.exp(x)
    return snaps


def show(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> None:
    print(f"{label:<58s} {value:{fmt}}")
    assert abs(value - expected) <= tol, f"{label}: {value} vs {expected}"


def main() -> None:
    # 1. Raw SVI slice used to generate the synthetic quotes: note 08 Example 1, cards deriv-svi-raw-params, deriv-svi-wing-slopes
    T = 0.5
    true = (0.012, 0.06, -0.7, 0.02, 0.12)
    a, b, rho, m, sig = true
    print("1. Raw SVI slice, T = 0.5, (a, b, rho, m, sigma) =", true)
    show("ATM-forward vol of the true slice (%)", 100 * math.sqrt(float(svi_w(np.array(0.0), *true)) / T), 20.07, 0.005, ".2f")
    show("minimum total variance a + b sigma sqrt(1 - rho^2)", a + b * sig * math.sqrt(1 - rho * rho), 0.017142, 1e-6, ".6f")
    show("right wing slope b(1 + rho)", b * (1 + rho), 0.018, 1e-12)
    show("left wing slope b(1 - rho)", b * (1 - rho), 0.102, 1e-12)
    kk = np.linspace(-1.5, 1.5, 3001)
    g_true = durrleman_g(*svi_derivs(kk, *true), kk)
    show("min g(k) on [-1.5, 1.5] for the true slice", float(g_true.min()), 0.2795, 5e-4)

    # 2. Fit to noisy synthetic quotes: Example 2, card deriv-svi-quasi-explicit
    rng = np.random.default_rng(2024)
    k = np.linspace(-0.4, 0.25, 27)
    vol_true = np.sqrt(svi_w(k, *true) / T)
    vol_mkt = vol_true + rng.normal(0.0, 0.002, k.size)  # 0.2 vol point quote noise
    w_mkt = vol_mkt**2 * T
    wt = np.exp(-0.5 * (k / 0.2) ** 2)  # vega-like weight: trust the wings less
    fit = fit_svi(k, w_mkt, wt)
    print("2. Quasi-explicit SVI fit to 27 noisy quotes")
    for name, v, e in zip(("a", "b", "rho", "m", "sigma"), fit, (0.0125, 0.0590, -0.7100, 0.0238, 0.1065), strict=True):
        show(f"fitted {name}", v, e, 5e-5)
    vol_fit = np.sqrt(svi_w(k, *fit) / T)
    rmse_mkt = 100 * math.sqrt(np.mean((vol_fit - vol_mkt) ** 2))
    kd = np.linspace(-0.4, 0.25, 651)
    err_true = 100 * np.max(np.abs(np.sqrt(svi_w(kd, *fit) / T) - np.sqrt(svi_w(kd, *true) / T)))
    show("RMSE fit vs noisy quotes (vol points)", rmse_mkt, 0.18, 0.005, ".2f")
    show("max |fit - true| on the quoted range (vol points)", float(err_true), 0.13, 0.005, ".2f")
    g_fit = durrleman_g(*svi_derivs(kk, *fit), kk)
    show("min g(k) of the fitted slice", float(g_fit.min()), 0.2825, 5e-4)
    show("fitted b(1 + |rho|) (Lee: <= 2)", fit[1] * (1 + abs(fit[2])), 0.1009, 5e-4)

    # 3. Vogt's arbitrageable slice (Gatheral and Jacquier 2014), T = 1, F = 1: Example 3, cards deriv-svi-vogt, deriv-svi-durrleman
    vogt = (-0.0410, 0.1331, 0.3060, 0.3586, 0.4153)
    kv = np.linspace(-1.5, 1.5, 30001)
    gv = durrleman_g(*svi_derivs(kv, *vogt), kv)
    i = int(np.argmin(gv))
    print("3. Vogt slice (a, b, rho, m, sigma) =", vogt)
    show("min g(k) of the Vogt slice", float(gv[i]), -0.0329, 5e-4)
    show("  at k", float(kv[i]), 0.88, 0.005, ".2f")
    neg = kv[gv < 0]
    show("  g < 0 from k", float(neg.min()), 0.64, 0.005, ".2f")
    show("  g < 0 to k", float(neg.max()), 1.26, 0.005, ".2f")
    Kg = np.linspace(1.5, 3.0, 1501)  # uniform strike grid, h = 0.001
    hK = Kg[1] - Kg[0]
    cg = np.asarray(bs_price(1.0, Kg, 1.0, 0.0, np.sqrt(svi_w(np.log(Kg), *vogt))))
    dens = (cg[2:] - 2 * cg[1:-1] + cg[:-2]) / hK**2
    j = int(np.argmin(dens))
    show("min density C_KK on K in [1.5, 3] (x 1e5)", 1e5 * float(dens[j]), -5.77, 0.005, ".2f")
    show("  at K", float(Kg[1:-1][j]), 2.20, 0.005, ".2f")
    fly = [float(bs_price(1.0, K, 1.0, 0.0, math.sqrt(float(svi_w(np.array(math.log(K)), *vogt))))) for K in (2.19, 2.20, 2.21)]
    show("butterfly 2.19 / 2.20 / 2.21 price (x 1e9)", 1e9 * (fly[0] - 2 * fly[1] + fly[2]), -5.77, 0.005, ".2f")

    # Calendar arbitrage: two SVI slices whose total variances cross: Example 4, card deriv-surface-calendar-check
    s1 = (0.010, 0.08, -0.6, 0.0, 0.10)  # T = 0.25
    s2 = (0.022, 0.05, -0.2, 0.0, 0.10)  # T = 0.5
    kc = np.linspace(-0.6, 0.6, 1201)
    diff = svi_w(kc, *s2) - svi_w(kc, *s1)
    print("Calendar check, slices", s1, "and", s2)
    show("w2 - w1 at k = 0", float(svi_w(np.array(0.0), *s2) - svi_w(np.array(0.0), *s1)), 0.009, 1e-9)
    show("min (w2 - w1) on [-0.6, 0.6]", float(diff.min()), -0.0290, 5e-5)
    show("calendar arbitrage for k below", float(kc[diff < 0].max()), -0.16, 0.005, ".2f")

    # 4. SSVI surface and its sufficient conditions: Example 5, card deriv-surface-ssvi
    print("4. SSVI: rho, eta, gamma =", (SSVI_RHO, SSVI_ETA, SSVI_GAMMA), "theta_t with v0, vbar, lambda =", (V0, VBAR, LAM))
    ts = np.linspace(0.02, 3.0, 150)
    th = theta_t(ts)
    show("max theta phi (1 + |rho|) on t in [0.02, 3] (< 4)", float(np.max(th * phi_of(th) * (1 + abs(SSVI_RHO)))), 0.47, 0.005, ".2f")
    show("max theta phi^2 (1 + |rho|) (<= 4)", float(np.max(th * phi_of(th) ** 2 * (1 + abs(SSVI_RHO)))), 0.98, 0.005, ".2f")
    th_small = np.array(1e-4)
    show(
        "gamma = 0.7 (above 1/2): theta phi^2 (1 + |rho|) at theta = 1e-4",
        float(th_small * phi_of(th_small, 0.7) ** 2 * (1 + abs(SSVI_RHO))),
        67.7,
        0.05,
        ".1f",
    )
    kg = np.linspace(-1.5, 1.0, 501)
    K2, T2 = np.meshgrid(kg, ts)
    w2, wk2, wkk2, wt2 = ssvi_w(K2, T2)
    show("min Durrleman g over the grid", float(durrleman_g(w2, wk2, wkk2, K2).min()), 0.2655, 5e-4)
    show("min dw/dt over the grid", float(wt2.min()), 0.0143, 5e-5)
    for t, e in ((0.25, 17.97), (0.5, 18.51), (1.0, 19.33), (2.0, 20.34)):
        show(f"SSVI ATM-forward vol at T = {t} (%)", 100 * math.sqrt(float(theta_t(np.array(t))) / t), e, 0.005, ".2f")

    # 5. Dupire: price form vs total-variance form: Example 5 table, cards deriv-dupire-formula, deriv-dupire-w-form
    print("5. Dupire local vol (S0 = 100, r = 3%, q = 1%)")
    expected = {  # (T, K): (implied, local) in vol points
        (0.25, 80.0): (26.85, 35.01),
        (0.25, 90.0): (22.55, 27.03),
        (0.25, 100.0): (18.19, 18.92),
        (0.25, 110.0): (14.42, 12.93),
        (0.25, 120.0): (12.90, 12.43),
        (1.0, 80.0): (25.05, 31.74),
        (1.0, 90.0): (22.37, 26.52),
        (1.0, 100.0): (19.82, 21.57),
        (1.0, 110.0): (17.50, 17.30),
        (1.0, 120.0): (15.63, 14.44),
    }
    max_gap = 0.0
    for (t, K), (e_iv, e_lv) in expected.items():
        k_ = math.log(K / float(fwd(np.array(t))))
        lv_w = 100 * math.sqrt(float(local_var_from_w(np.array(k_), np.array(t))))
        lv_p = 100 * math.sqrt(local_var_from_prices(K, t))
        iv = 100 * math.sqrt(float(ssvi_w(np.array(k_), np.array(t))[0]) / t)
        max_gap = max(max_gap, abs(lv_w - lv_p))
        print(f"  T = {t:4.2f} K = {K:5.1f}: implied {iv:6.2f}  local (w-form) {lv_w:6.2f}  local (price form) {lv_p:6.2f}")
        assert abs(iv - e_iv) < 0.005 and abs(lv_w - e_lv) < 0.005, (t, K, iv, lv_w)
    show("max |w-form - price-form| local vol (vol points)", max_gap, 0.0, 0.001, ".4f")

    # Short-maturity skew ratio d sigma_loc / dk over d sigma_imp / dk at k = 0: Example 7, cards deriv-dupire-skew-ratio,
    # deriv-dupire-smile-dynamics
    print("Local-vol skew / implied skew at the money (gamma = 0: flat skew term structure; 0.4: skew ~ T^-0.4)")
    h = 1e-5
    for gam, t, e_ratio, e_skew in (
        (0.0, 0.001, 2.00, -0.0606),
        (0.0, 1.0, 2.11, -0.0652),
        (0.4, 0.0001, 1.63, -9.8125),
        (0.4, 0.01, 1.68, -1.5554),
        (0.4, 0.25, 1.79, -0.4303),
        (0.4, 1.0, 1.89, -0.2465),
    ):
        tt = np.array(t)
        imp = [math.sqrt(float(ssvi_w(np.array(x), tt, gam)[0]) / t) for x in (-h, h)]
        loc = [math.sqrt(float(local_var_from_w(np.array(x), tt, gam))) for x in (-h, h)]
        skew = (imp[1] - imp[0]) / (2 * h)
        show(f"  gamma = {gam}, T = {t}: implied ATM skew d sigma / dk", skew, e_skew, 5e-4)
        show(f"  gamma = {gam}, T = {t}: ratio", (loc[1] - loc[0]) / (imp[1] - imp[0]), e_ratio, 0.005, ".2f")

    # Skew stickiness ratio of local vol from the same averaging heuristic: the ATM vol moves by (1/T) int_0^T L(t) dt
    # per unit of log spot, L(t) the ATM local skew at time t; divided by the implied skew psi(T). Flat skew -> 2,
    # skew ~ T^-gamma -> (2 - gamma) / (1 - gamma). Integrated with t = T u^5 to absorb the t^-gamma singularity.
    # Backs Core concepts "Skew, smile dynamics and the forward smile" and card deriv-dupire-smile-dynamics.
    nodes, weights = np.polynomial.legendre.leggauss(200)
    u = 0.5 * (nodes + 1.0)
    for gam, t, e_ssr in ((0.0, 0.001, 2.00), (0.4, 1e-6, 2.68)):
        ts_ = t * u**5
        loc_skew = (
            np.sqrt(local_var_from_w(np.full_like(ts_, h), ts_, gam)) - np.sqrt(local_var_from_w(np.full_like(ts_, -h), ts_, gam))
        ) / (2 * h)
        avg_loc = float(np.sum(0.5 * weights * loc_skew * 5 * u**4))
        tt = np.array(t)
        imp = [math.sqrt(float(ssvi_w(np.array(x), tt, gam)[0]) / t) for x in (-h, h)]
        show(
            f"  gamma = {gam}, T = {t}: local-vol skew stickiness ratio (heuristic)",
            avg_loc / ((imp[1] - imp[0]) / (2 * h)),
            e_ssr,
            0.005,
            ".2f",
        )
    show("  power-law limit (2 - gamma) / (1 - gamma) at gamma = 0.4", (2 - 0.4) / (1 - 0.4), 2.67, 0.005, ".2f")
    show("  power-law limit (2 - gamma) / (1 - gamma) at gamma = 0.5", (2 - 0.5) / (1 - 0.5), 3.00, 0.005, ".2f")

    # 6. Local-vol Monte Carlo reprices the surface: Example 6, card deriv-dupire-validation
    print("6. Local-vol Monte Carlo, 2 x 100,000 antithetic paths, 250 steps per year")
    snaps = local_vol_mc(100_000, 250, 1.0, seed=7)
    strikes = np.array([80.0, 90.0, 100.0, 110.0, 120.0])
    exp_mc = {0.5: [25.55, 22.20, 18.87, 15.89, 13.95], 1.0: [24.96, 22.34, 19.81, 17.49, 15.61]}
    exp_in = {0.5: [25.61, 22.19, 18.84, 15.83, 13.89], 1.0: [25.05, 22.37, 19.82, 17.50, 15.63]}
    worst = 0.0
    for t in (0.5, 1.0):
        ST = snaps[t]
        payoff = np.maximum(ST[:, None] - strikes[None, :], 0.0) * math.exp(-R * t)
        pair = 0.5 * (payoff[: len(ST) // 2] + payoff[len(ST) // 2 :])
        price = pair.mean(0)
        se = pair.std(0, ddof=1) / math.sqrt(pair.shape[0])
        iv_mc = 100 * np.asarray(implied_vol(price, S0, strikes, t, R, Q))
        iv_in = 100 * np.sqrt(ssvi_w(np.log(strikes / fwd(np.array(t))), np.array(t))[0] / t)
        worst = max(worst, float(np.max(np.abs(iv_mc - iv_in))))
        print(f"  T = {t}: MC implied {np.round(iv_mc, 2)}  input {np.round(iv_in, 2)}  price s.e. {np.round(se, 3)}")
        assert np.allclose(iv_mc, exp_mc[t], atol=0.005) and np.allclose(iv_in, exp_in[t], atol=0.005)
    show("max |MC - input| implied vol (vol points)", worst, 0.0847, 0.0005, ".2f")

    # Forward smile, forward-start call on S_1 / S_0.5 versus today's 6-month smile: Example 7, card deriv-dupire-forward-smile
    ratio = snaps[1.0] / snaps[0.5]
    kappas = np.array([0.9, 1.0, 1.1])
    fwd_g = math.exp((R - Q) * 0.5)
    pay = np.maximum(ratio[:, None] - kappas[None, :] * fwd_g, 0.0) * math.exp(-R * 1.0)
    pair = 0.5 * (pay[: len(ratio) // 2] + pay[len(ratio) // 2 :])
    price = pair.mean(0) / math.exp(-R * 0.5)  # value at 0.5 of the forward-start option, per unit of S_0.5
    fwd_iv = 100 * np.asarray(implied_vol(price, 1.0, kappas * fwd_g, 0.5, R, Q))
    spot_iv = 100 * np.sqrt(ssvi_w(np.log(kappas), np.array(0.5))[0] / 0.5)
    print(f"  forward 6m smile in 6m (0.9, 1.0, 1.1 of forward): {np.round(fwd_iv, 2)}")
    print(f"  today's 6m smile (0.9, 1.0, 1.1 of forward): {np.round(spot_iv, 2)}")
    assert np.allclose(fwd_iv, [23.46, 20.93, 19.52], atol=0.005) and np.allclose(spot_iv, [21.88, 18.51, 15.55], atol=0.005)
    show("today's 6m skew, vol(90%) - vol(110%) (vol points)", float(spot_iv[0] - spot_iv[2]), 6.33, 0.005, ".2f")
    show("local-vol forward 6m skew in 6m, same moneyness", float(fwd_iv[0] - fwd_iv[2]), 3.94, 0.005, ".2f")
    show(
        "flattening, 1 - forward skew / today's skew (%)",
        100 * float(1 - (fwd_iv[0] - fwd_iv[2]) / (spot_iv[0] - spot_iv[2])),
        38.0,
        0.5,
        ".0f",
    )


if __name__ == "__main__":
    main()
