"""Volatility models, EWMA and GARCH: every number in the note, by an independent route.

Backs every number in `02-Statistics-and-Econometrics/09-Volatility-Models-GARCH.md`.
Independent routes used here:
- GARCH variance forecasts by iterating the one-step expectation recursion and by seeded Monte Carlo of
  return paths, never by re-evaluating the closed-form term structure;
- unconditional kurtosis by solving the second- and fourth-moment recursions as a linear system, not from
  Bollerslev's closed form;
- EWMA weights, half-life and centre of mass by summing the weight sequence;
- range-estimator efficiency: Parkinson exactly from the range moments E[R^2] = 4 ln 2 and E[R^4] = 9 zeta(3),
  zeta(3) summed as a series, and Garman-Klass by simulating finely discretised Brownian paths;
- the microstructure-noise bias by simulating a noisy price path sampled at three frequencies;
- Patton's loss-function result by minimising expected losses against a noisy proxy;
- the GARCH maximum-likelihood fit by a from-scratch Nelder-Mead and a local check that no single-axis
  step or step along the alpha + beta ridge raises the likelihood.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_09_garch.py`.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261112
LN_HALF = math.log(0.5)
OMEGA, ALPHA, BETA = 2e-6, 0.08, 0.90


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def sci(label: str, value: float, expected: float, sig: int) -> None:
    """Assert to ``sig`` significant figures, for literals quoted like 2.765e-4."""
    scale = 10.0 ** (math.floor(math.log10(abs(expected))) - sig + 1)
    assert abs(value - expected) <= 0.5 * scale + 1e-18, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{sig - 1}e}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.5g} (quoted {expected}, tolerance {tol:.3g})")


def ewma() -> None:
    print("EWMA: TL;DR, Example 2 and cards stat-garch-ewma-half-life, stat-garch-ewma-update")
    lam = 0.94
    w = (1 - lam) * lam ** np.arange(0, 2000)  # weight on r_{t-k}, k = 1, 2, ...
    approx("weights sum to one", float(w.sum()), 1.0, 10)
    k_half = next(k for k in range(1, 100) if w[k] <= w[0] / 2)
    assert w[0] * lam**11 > w[0] / 2 > w[0] * lam**12 and k_half == 12
    approx("weight half-life ln 0.5/ln 0.94 (between lags 11 and 12)", LN_HALF / math.log(lam), 11.2, 1)
    approx("centre of mass sum k w_k", float(np.sum(np.arange(1, 2001) * w)), 16.7, 1)
    approx("weight on the return five days ago", float(w[4]), 0.047, 3)
    s2 = lam * 1e-4 + (1 - lam) * 16e-4
    sci("updated variance", s2, 1.90e-4, 3)
    approx("updated vol (%)", 100 * math.sqrt(s2), 1.38, 2)
    approx("vol rise (%)", 100 * (math.sqrt(s2) / 0.01 - 1), 38, 0)


def garch_basics() -> None:
    print("Example 1 and cards stat-garch-long-run-variance, stat-garch-persistence-half-life, stat-garch-update")
    pers = ALPHA + BETA
    approx("persistence", pers, 0.98, 10)
    # long-run variance as the fixed point of v = omega + (alpha + beta) v, by iteration
    v = 0.0
    for _ in range(5000):
        v = OMEGA + pers * v
    sci("long-run variance (fixed point)", v, 1e-4, 6)
    approx("long-run daily vol (%)", 100 * math.sqrt(v), 1.00, 2)
    approx("long-run annual vol (%)", 100 * math.sqrt(252 * v), 15.9, 1)
    approx("shock half-life (days)", LN_HALF / math.log(pers), 34.3, 1)
    approx("shock half-life, card (days)", LN_HALF / math.log(pers), 34, 0)
    s2 = OMEGA + ALPHA * 0.03**2 + BETA * 0.015**2
    sci("tomorrow's variance", s2, 2.765e-4, 4)
    approx("tomorrow's vol (%)", 100 * math.sqrt(s2), 1.66, 2)
    approx("tomorrow's vol annualised (%)", 100 * math.sqrt(252 * s2), 26.4, 1)


def term_structure(rng: np.random.Generator) -> None:
    print("Example 3 and card stat-garch-term-structure: forecasts by recursion and by simulation")
    s1 = OMEGA + ALPHA * 0.03**2 + BETA * 0.015**2
    path = [s1]
    for _ in range(251):
        path.append(OMEGA + (ALPHA + BETA) * path[-1])  # E_t[sigma^2_{t+h+1}] = omega + (alpha+beta) E_t[sigma^2_{t+h}]
    path = np.array(path)
    approx("daily vol forecast h = 10 (%)", 100 * math.sqrt(path[9]), 1.57, 2)
    approx("daily vol forecast h = 21 (%)", 100 * math.sqrt(path[20]), 1.48, 2)
    approx("daily vol forecast h = 63 (%)", 100 * math.sqrt(path[62]), 1.23, 2)
    m21 = float(path[:21].mean())
    approx("one-month average daily vol (%)", 100 * math.sqrt(m21), 1.57, 2)
    approx("one-month vol annualised (%)", 100 * math.sqrt(252 * m21), 24.9, 1)
    approx("one-year vol annualised (%)", 100 * math.sqrt(252 * float(path.mean())), 18.4, 1)
    approx("EWMA at every horizon (%)", 100 * math.sqrt(252 * s1), 26.4, 1)
    approx("1.765e-4 = spot minus long-run variance", (s1 - 1e-4) * 1e4, 1.765, 3)
    paths = 200000
    s2 = np.full(paths, s1)
    total = np.zeros(paths)
    for _ in range(21):
        r = np.sqrt(s2) * rng.standard_normal(paths)
        total += r * r
        s2 = OMEGA + ALPHA * r * r + BETA * s2
    mean_var = float(total.mean()) / 21
    se = float(total.std()) / 21 / math.sqrt(paths)
    simulated(
        "simulated one-month vol annualised (%)",
        100 * math.sqrt(252 * mean_var),
        24.9,
        100 * math.sqrt(252) * 4 * se / (2 * math.sqrt(mean_var)) + 0.05,
    )


def gjr_persistence() -> None:
    print("GJR-GARCH persistence alpha + gamma/2 + beta: E[1{z<0} z^2] = 1/2 for N(0,1), by quadrature")
    z = np.linspace(-12, 0, 120001)
    y = z * z * np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    approx("E[1{z<0} z^2]", float(np.sum((y[1:] + y[:-1]) / 2) * (z[1] - z[0])), 0.5, 8)


def kurtosis() -> None:
    print("Example 6 and card stat-garch-kurtosis: kurtosis from the moment recursions")

    def kurt(alpha: float, beta: float, omega: float = 1.0) -> float:
        # unknowns m2 = E[sigma^2], m4 = E[sigma^4]; E[r^4] = 3 m4 for Gaussian z
        a = np.array(
            [
                [1 - alpha - beta, 0.0],
                [-2 * omega * (alpha + beta), 1 - (3 * alpha**2 + 2 * alpha * beta + beta**2)],
            ]
        )
        m2, m4 = np.linalg.solve(a, np.array([omega, omega**2]))
        return 3 * m4 / m2**2

    approx("GARCH(1,1) 0.08, 0.90 kurtosis", kurt(0.08, 0.90), 4.43, 2)
    approx("GARCH(1,1) kurtosis (one decimal)", kurt(0.08, 0.90), 4.4, 1)
    approx("3(1 - 0.9604)", 3 * (1 - 0.98**2), 0.1188, 4)
    approx("1 - 0.9604 - 2 x 0.0064", 1 - 0.98**2 - 2 * 0.08**2, 0.0268, 4)
    approx("ARCH(1) 0.3 kurtosis", kurt(0.3, 0.0), 3.74, 2)
    approx("alpha^2 for ARCH(1) 0.3", 0.3**2, 0.09, 10)
    approx("3 alpha^2", 3 * 0.3**2, 0.27, 10)
    approx("2 alpha^2 for GARCH alpha = 0.08", 2 * 0.08**2, 0.0128, 10)


def range_estimators(rng: np.random.Generator) -> None:
    print("Example 4, Core concepts table and card stat-garch-parkinson: range estimators")
    o, h, lo, c = 100.0, 103.0, 98.0, 101.0
    hl, co = math.log(h / lo), math.log(c / o)
    approx("ln(H/L)", hl, 0.04976, 5)
    approx("ln(C/O)", co, 0.00995, 5)
    park = hl**2 / (4 * math.log(2))
    sci("Parkinson variance", park, 8.93e-4, 3)
    approx("Parkinson vol (%)", 100 * math.sqrt(park), 2.99, 2)
    approx("Parkinson vol annualised (%)", 100 * math.sqrt(252 * park), 47.4, 1)
    gk = 0.5 * hl**2 - (2 * math.log(2) - 1) * co**2
    approx("2 ln 2 - 1", 2 * math.log(2) - 1, 0.3863, 4)
    sci("Garman-Klass variance", gk, 1.20e-3, 3)
    approx("Garman-Klass vol (%)", 100 * math.sqrt(gk), 3.46, 2)
    approx("Garman-Klass vol annualised (%)", 100 * math.sqrt(252 * gk), 55.0, 1)
    sci("close-to-close squared return", co**2, 9.9e-5, 2)
    approx("close-to-close vol (%)", 100 * abs(co), 0.995, 3)
    approx("close-to-close vol annualised (%)", 100 * math.sqrt(252) * abs(co), 15.8, 1)
    approx("range as a share of the open (%)", 100 * (h - lo) / o, 5, 6)
    zeta3 = sum(1.0 / k**3 for k in range(1, 200000)) + 1 / (2 * 200000**2)
    var_park = (9 * zeta3 - (4 * math.log(2)) ** 2) / (4 * math.log(2)) ** 2
    eff_park = 2.0 / var_park  # Var of a squared N(0,1) close-to-close return is 2
    approx("Parkinson efficiency, exact", eff_park, 4.91, 2)
    approx("Parkinson efficiency (one decimal)", eff_park, 4.9, 1)
    approx("Var of the Parkinson estimator / sigma^4", var_park, 0.4073, 4)
    # Exact range simulation: Brownian increments on a grid, then the maximum and minimum inside each step drawn
    # from the Brownian-bridge law, max = (a + b + sqrt((b - a)^2 - 2 dt ln U)) / 2, so no discretisation bias.
    steps, paths, chunk = 100, 200000, 5000
    dt = 1.0 / steps
    p_est, g_est = [], []
    for _ in range(paths // chunk):
        w = np.c_[np.zeros(chunk), np.cumsum(math.sqrt(dt) * rng.standard_normal((chunk, steps)), axis=1)]
        a, b = w[:, :-1], w[:, 1:]
        d2 = (b - a) ** 2
        hi = (0.5 * (a + b + np.sqrt(d2 - 2 * dt * np.log(rng.random(a.shape))))).max(axis=1)
        lw = (0.5 * (a + b - np.sqrt(d2 - 2 * dt * np.log(rng.random(a.shape))))).min(axis=1)
        cl = w[:, -1]
        p_est.append((hi - lw) ** 2 / (4 * math.log(2)))
        g_est.append(0.5 * (hi - lw) ** 2 - (2 * math.log(2) - 1) * cl**2)
    for name, est, quoted in (("Parkinson", np.concatenate(p_est), eff_park), ("Garman-Klass", np.concatenate(g_est), 7.4)):
        var = float(est.var())
        m4 = float(np.mean((est - est.mean()) ** 4))
        rel_se = math.sqrt((m4 / var**2 - 1) / paths)  # relative standard error of the sample variance
        simulated(f"{name} mean, unbiased for sigma^2 = 1", float(est.mean()), 1.0, 4 * math.sqrt(var / paths))
        eff = 2.0 / var
        simulated(f"{name} efficiency, 200,000 exact-range Brownian days", eff, quoted, 4 * eff * rel_se + 0.05)


def noise_bias(rng: np.random.Generator) -> None:
    print("Example 5 and card stat-garch-rv-noise: realized variance with iid noise")
    iv, noise_var = 1e-4, 1e-8
    for n, quoted, sig in ((78, 1.56e-6, 3), (390, 7.8e-6, 2), (23400, 4.68e-4, 3)):
        sci(f"bias 2 n omega^2, n = {n}", 2 * n * noise_var, quoted, sig)
    approx("5-minute bias share of IV (%)", 100 * 2 * 78 * noise_var / iv, 1.6, 1)
    approx("1-minute bias share of IV (%)", 100 * 2 * 390 * noise_var / iv, 7.8, 1)
    approx("1-second bias as a multiple of IV", 2 * 23400 * noise_var / iv, 4.7, 1)
    days = 400
    rv = {78: [], 390: [], 23400: []}
    for _ in range(days):
        eff = np.cumsum(math.sqrt(iv / 23400) * rng.standard_normal(23401))
        obs = eff + math.sqrt(noise_var) * rng.standard_normal(23401)
        for n in rv:
            step = 23400 // n
            rv[n].append(float(np.sum(np.diff(obs[::step]) ** 2)))
    for n in rv:
        arr = np.array(rv[n])
        simulated(
            f"mean RV at n = {n} over {days} simulated days",
            float(arr.mean()),
            iv + 2 * n * noise_var,
            4 * float(arr.std()) / math.sqrt(days),
        )


def patton_losses() -> None:
    print("Patton (2011), Evaluating forecasts: minimise E[L(proxy, h)] with proxy r^2 = sigma^2 z^2, sigma^2 = 1")
    z = np.linspace(-12, 12, 240001)
    phi = np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    dz = z[1] - z[0]
    proxy = z * z
    h = np.linspace(0.2, 2.0, 1801)
    mse = [float(np.sum(phi * (proxy - x) ** 2) * dz) for x in h]
    qlike = [float(np.sum(phi * (proxy / x - np.log(np.maximum(proxy, 1e-300) / x) - 1)) * dz) for x in h]
    mae_vol = [float(np.sum(phi * np.abs(np.abs(z) - math.sqrt(x))) * dz) for x in h]
    approx("argmin of MSE on variance", float(h[int(np.argmin(mse))]), 1.0, 3)
    approx("argmin of QLIKE", float(h[int(np.argmin(qlike))]), 1.0, 3)
    approx("argmin of MAE on volatility (median of z^2, not 1)", float(h[int(np.argmin(mae_vol))]), 0.455, 3)


def engle_patton() -> None:
    print("Engle and Patton (2001): Dow Jones daily GARCH(1,1), cited inputs alpha 0.0399, beta 0.9505, omega 0.0082")
    a, b, w = 0.0399, 0.9505, 0.0082
    approx("persistence", a + b, 0.9904, 4)
    approx("half-life counted from t+1, ln 0.5/ln 0.9904", LN_HALF / math.log(a + b), 71.9, 1)
    approx("half-life rounded to whole days", LN_HALF / math.log(a + b), 72, 0)
    approx("half-life counted from t, one step more (they report about 73)", 1 + LN_HALF / math.log(a + b), 72.9, 1)
    approx("long-run variance (% squared, daily)", w / (1 - a - b), 0.854, 3)
    approx("long-run annual vol (%)", math.sqrt(252 * w / (1 - a - b)), 14.67, 2)


def nelder_mead(f, x0: np.ndarray, scale: np.ndarray, iters: int = 4000) -> np.ndarray:
    """Plain Nelder-Mead (reflection 1, expansion 2, contraction 0.5, shrink 0.5)."""
    pts = [x0] + [x0 + np.eye(len(x0))[i] * scale[i] for i in range(len(x0))]
    vals = [f(p) for p in pts]
    for _ in range(iters):
        order = np.argsort(vals)
        pts, vals = [pts[i] for i in order], [vals[i] for i in order]
        centroid = np.mean(pts[:-1], axis=0)
        xr = centroid + (centroid - pts[-1])
        fr = f(xr)
        if fr < vals[0]:
            xe = centroid + 2 * (centroid - pts[-1])
            fe = f(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        else:
            xc = centroid + 0.5 * (pts[-1] - centroid)
            fc = f(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                pts = [pts[0] + 0.5 * (p - pts[0]) for p in pts]
                vals = [f(p) for p in pts]
        if max(vals) - min(vals) < 1e-12 and np.max(np.abs(np.array(pts) - pts[0])) < 1e-12:
            break
    return pts[int(np.argmin(vals))]


def garch_mle() -> None:
    print("Example 7: fit GARCH(1,1) by maximum likelihood to the snippet's simulated series (seed 1)")
    rng = np.random.default_rng(1)
    t_len = 5000
    r, s2 = np.empty(t_len), OMEGA / (1 - ALPHA - BETA)
    for t in range(t_len):
        r[t] = np.sqrt(s2) * rng.standard_normal()
        s2 = OMEGA + ALPHA * r[t] ** 2 + BETA * s2

    def neg_loglik(theta: np.ndarray) -> float:
        w, a, b = theta
        if w <= 0 or a < 0 or b < 0 or a + b >= 1:
            return math.inf
        v = np.empty(t_len)
        v[0] = r.var()
        for t in range(1, t_len):
            v[t] = w + a * r[t - 1] ** 2 + b * v[t - 1]
        return 0.5 * float(np.sum(np.log(v) + r**2 / v))

    # optimise in scaled units (omega in 1e-6) so the simplex is well conditioned
    def scaled(x: np.ndarray) -> float:
        return neg_loglik(np.array([x[0] * 1e-6, x[1], x[2]]))

    x = nelder_mead(scaled, np.array([r.var() * 0.05 * 1e6, 0.05, 0.90]), np.array([0.5, 0.02, 0.02]))
    best = scaled(x)
    directions = [np.eye(3)[i] * step for i, step in enumerate((0.01, 1e-4, 1e-4))]
    directions.append(np.array([0.0, 1e-4, -1e-4]))
    for d in directions:
        for sgn in (-1, 1):
            assert scaled(x + sgn * d) >= best - 1e-9, "Nelder-Mead did not reach a local maximum"
    w, a, b = x[0] * 1e-6, x[1], x[2]
    print("    local check passed: no step along any single axis or along the alpha + beta ridge raises the likelihood")
    sci("omega_hat", w, 2.13e-6, 3)
    approx("alpha_hat", a, 0.084, 3)
    approx("beta_hat", b, 0.895, 3)
    approx("persistence", a + b, 0.979, 3)
    approx("long-run annual vol", math.sqrt(252 * w / (1 - a - b)), 0.160, 3)
    approx("true long-run annual vol", math.sqrt(252 * OMEGA / (1 - ALPHA - BETA)), 0.159, 3)
    approx("years of daily data, 5000/252", t_len / 252, 20, 0)


def main() -> None:
    rng = np.random.default_rng(SEED)
    ewma()
    garch_basics()
    term_structure(rng)
    gjr_persistence()
    kurtosis()
    range_estimators(rng)
    noise_bias(rng)
    patton_losses()
    engle_patton()
    garch_mle()
    print("all GARCH checks passed")


if __name__ == "__main__":
    main()
