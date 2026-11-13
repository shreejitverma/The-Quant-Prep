"""Stochastic differential equations: GBM, OU and CIR moments, the Feller example and scheme orders.

Backs every number in `04-Stochastic-Calculus/03-Stochastic-Differential-Equations.md`.
Independent routes used here:
- GBM mean, median and P(S_t > S_0) by a 1,000-step Euler simulation of the SDE itself (never the
  closed-form solution), the mode by maximising the density on a grid, and the moments by quadrature;
- OU and CIR first and second moments by RK4 integration of the moment ODEs
  m' = kappa (theta - m), q' = 2 kappa theta m - 2 kappa q + (diffusion term), not the closed forms;
- CIR by exact non-central chi-squared sampling of the transition and of the long-run law;
- the OU AR(1) coefficient by least squares on a simulated path;
- Euler and Milstein strong errors for GBM against the exact solution on shared increments (the table's
  seed), with the convergence orders from a log-log fit;
- the squared-Bessel SDE of W^2 by its simulated quadratic variation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 04-Stochastic-Calculus/code/stoch_03_sde.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, se: float, target: float, k: float = 4.0) -> None:
    """Assert a seeded Monte Carlo estimate is within k standard errors of an independently computed target."""
    assert abs(estimate - target) <= k * se, f"{label}: simulated {estimate!r} +/- {se:.2g}, target {target}"
    print(f"    {label} ~ {estimate:.6g} (se {se:.1e}, target {target:.6g}, tolerance {k:g} se)")


def ncdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def mean_se(x: np.ndarray) -> tuple[float, float]:
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(x.size))


def var_se(x: np.ndarray) -> tuple[float, float]:
    c = x - x.mean()
    v = float((c**2).mean())
    return v, float(math.sqrt(max((c**4).mean() - v * v, 0.0) / x.size))


def rk4(f, y0: np.ndarray, t: float, n: int) -> np.ndarray:
    y, h = np.array(y0, dtype=float), t / n
    for _ in range(n):
        k1 = f(y)
        k2 = f(y + 0.5 * h * k1)
        k3 = f(y + 0.5 * h * k2)
        k4 = f(y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y


GH_X, GH_W = np.polynomial.hermite_e.hermegauss(80)
GH_W = GH_W / GH_W.sum()


def gbm(rng: np.random.Generator) -> None:
    print(
        "GBM, mu = 10%, sigma = 30%, t = 2, S0 = 100 (worked example; cards sc-sde-gbm-mean-median, sc-sde-gbm-variance, sc-sde-gbm-mode)"
    )
    mu, sig, t, s0 = 0.10, 0.30, 2.0, 100.0
    approx("mean S0 e^{mu t}", s0 * math.exp(mu * t), 122.14, 2)
    approx("median S0 e^{(mu - sigma^2/2) t}", s0 * math.exp((mu - 0.5 * sig**2) * t), 111.63, 2)
    approx("mode S0 e^{(mu - 3 sigma^2/2) t}", s0 * math.exp((mu - 1.5 * sig**2) * t), 93.24, 2)
    z = (mu - 0.5 * sig**2) * math.sqrt(t) / sig
    approx("(mu - sigma^2/2) sqrt(t) / sigma = 0.055 sqrt 2 / 0.3", z, 0.055 * math.sqrt(2) / 0.3, 12)
    approx("P(S_2 > 100) = Phi(0.2593)", ncdf(z), 0.602, 3)
    # mode by maximising the lognormal density on a fine grid
    m_log, s_log = math.log(s0) + (mu - 0.5 * sig**2) * t, sig * math.sqrt(t)
    x = np.linspace(50.0, 150.0, 1_000_001)
    dens = np.exp(-((np.log(x) - m_log) ** 2) / (2 * s_log**2)) / (x * s_log * math.sqrt(2 * math.pi))
    approx("mode by grid argmax of the density", float(x[np.argmax(dens)]), 93.24, 2)
    # moments by Gauss-Hermite on log S_t
    st = np.exp(m_log + s_log * GH_X)
    approx(
        "Var(S_t) by quadrature vs S0^2 e^{2 mu t}(e^{sigma^2 t} - 1)",
        float(GH_W @ st**2 - (GH_W @ st) ** 2),
        s0**2 * math.exp(2 * mu * t) * (math.exp(sig**2 * t) - 1),
        8,
    )
    for p in (-1.0, 0.5, 3.0):
        approx(
            f"E[S_t^{p}] by quadrature vs closed form",
            float(GH_W @ st**p),
            s0**p * math.exp(p * mu * t + 0.5 * p * (p - 1) * sig**2 * t),
            6,
        )
    g = np.linspace(0.0, t, 200_001)
    approx(
        "E int_0^T S dt by quadrature of S0 e^{mu t} vs S0 (e^{mu T} - 1)/mu",
        float(np.sum(0.5 * np.diff(g) * (s0 * np.exp(mu * g[1:]) + s0 * np.exp(mu * g[:-1])))),
        s0 * (math.exp(mu * t) - 1) / mu,
        6,
    )
    # the SDE itself by Euler, 1000 steps: no use of the closed-form solution
    paths, steps = 200_000, 1000
    h = t / steps
    s = np.full(paths, s0)
    for _ in range(steps):
        s = s * (1 + mu * h + sig * math.sqrt(h) * rng.standard_normal(paths))
    m, se = mean_se(s)
    simulated("E[S_2], Euler simulation of the SDE", m, se, s0 * math.exp(mu * t))
    med = float(np.median(s))
    f_med = math.exp(-0.0) / (s0 * math.exp((mu - 0.5 * sig**2) * t) * s_log * math.sqrt(2 * math.pi))
    simulated("median of S_2, Euler simulation", med, math.sqrt(0.25 / paths) / f_med, s0 * math.exp((mu - 0.5 * sig**2) * t))
    m, se = mean_se((s > s0).astype(float))
    simulated("P(S_2 > 100), Euler simulation", m, se, ncdf(z))
    # mu = 0: mean stays S0 while the median e^{-sigma^2 t/2} S0 -> 0
    approx("median with mu = 0, sigma = 30%, t = 100 (per unit of S0)", math.exp(-0.5 * sig**2 * 100), 0.011, 3)


def ou(rng: np.random.Generator) -> None:
    print("OU, kappa = 2, theta = 1, sigma = 0.5, X0 = 3, t = 0.7 (worked example; cards sc-sde-ou-variance, sc-sde-ou-half-life)")
    k, th, sig, x0, t = 2.0, 1.0, 0.5, 3.0, 0.7
    # moment ODEs: m' = k (th - m), v' = -2 k v + sigma^2
    m, v = rk4(lambda y: np.array([k * (th - y[0]), -2 * k * y[1] + sig**2]), np.array([x0, 0.0]), t, 2000)
    approx("E[X_0.7] by RK4 of the moment ODE", m, 1.493, 3)
    approx("    and 1 + 2 e^{-1.4}", 1 + 2 * math.exp(-1.4), m, 9)
    approx("Var(X_0.7) by RK4", v, 0.0587, 4)
    approx("    and (0.25/4)(1 - e^{-2.8})", 0.25 / 4 * (1 - math.exp(-2.8)), v, 9)
    approx("stationary variance sigma^2/(2 kappa)", sig**2 / (2 * k), 0.0625, 4)
    approx("half-life ln 2 / kappa", math.log(2) / k, 0.35, 2)
    approx("half-life to three decimals", math.log(2) / k, 0.347, 3)
    approx("t / half-life (about two half-lives)", t / (math.log(2) / k), 2.02, 2)
    approx("remaining deviation 2 e^{-1.4}", 2 * math.exp(-1.4), 0.493, 3)
    paths, steps = 200_000, 700
    h = t / steps
    x = np.full(paths, x0)
    for _ in range(steps):
        x = x + k * (th - x) * h + sig * math.sqrt(h) * rng.standard_normal(paths)
    mm, se = mean_se(x)
    simulated("E[X_0.7], Euler simulation (bias O(h) = O(1e-3) relative)", mm, se + 2e-3, m)
    vv, se = var_se(x)
    simulated("Var(X_0.7), Euler simulation", vv, se + 1e-4, v)
    # AR(1): sample the exact transition and regress
    dt, n = 0.01, 400_000
    phi = math.exp(-k * dt)
    sd = math.sqrt(sig**2 / (2 * k) * (1 - phi * phi))
    eps = rng.standard_normal(n) * sd
    path = np.empty(n)
    path[0] = th
    for i in range(1, n):
        path[i] = th + phi * (path[i - 1] - th) + eps[i]
    xc, yc = path[:-1] - path[:-1].mean(), path[1:] - path[1:].mean()
    slope = float(xc @ yc / (xc @ xc))
    simulated("AR(1) slope by least squares vs e^{-kappa dt}", slope, math.sqrt((1 - phi * phi) / n), phi)
    simulated("kappa = -ln(slope)/dt", -math.log(slope) / dt, math.sqrt((1 - phi * phi) / n) / (phi * dt), k)


def cir(rng: np.random.Generator) -> None:
    print("CIR, kappa = 1.5, theta = 4%, sigma = 0.2, r0 = 2% (cards sc-sde-cir-feller, sc-sde-cir-stationary, sc-sde-cir-variance)")
    k, th, sig, r0, t = 1.5, 0.04, 0.2, 0.02, 1.0
    exact("2 kappa theta (in hundredths)", Fraction(2) * Fraction(15, 10) * Fraction(4), Fraction(12))
    approx("2 kappa theta", 2 * k * th, 0.12, 12)
    approx("sigma^2", sig**2, 0.04, 12)
    assert 2 * k * th >= sig**2
    approx("shape 2 kappa theta / sigma^2", 2 * k * th / sig**2, 3.0, 12)
    approx("scale sigma^2/(2 kappa)", sig**2 / (2 * k), 0.0133, 4)
    approx("stationary sd sqrt(theta sigma^2 / (2 kappa)), percent", 100 * math.sqrt(th * sig**2 / (2 * k)), 2.3, 1)
    approx("    and sqrt(0.04 * 0.04 / 3), percent", 100 * math.sqrt(0.04 * 0.04 / 3), 2.3, 1)
    # moment ODEs: m' = k (th - m); q = E[r^2]: q' = 2 k th m - 2 k q + sigma^2 m
    m, q = rk4(lambda y: np.array([k * (th - y[0]), 2 * k * th * y[0] - 2 * k * y[1] + sig**2 * y[0]]), np.array([r0, r0 * r0]), t, 2000)
    var = q - m * m
    approx("E[r_1] by RK4, percent", 100 * m, 3.55, 2)
    approx("    and 4% - 2% e^{-1.5}, percent", 100 * (th - (th - r0) * math.exp(-k)), 100 * m, 9)
    approx("Var(r_1) by RK4, in units of 1e-4", 1e4 * var, 4.14, 2)
    closed = r0 * sig**2 / k * (math.exp(-k * t) - math.exp(-2 * k * t)) + th * sig**2 / (2 * k) * (1 - math.exp(-k * t)) ** 2
    approx("    and the closed form", closed, var, 12)
    # exact transition: r_t = c chi'^2(d, lambda)
    c = sig**2 * (1 - math.exp(-k * t)) / (4 * k)
    d = 4 * k * th / sig**2
    lam = r0 * math.exp(-k * t) / c
    approx("degrees of freedom 4 kappa theta / sigma^2 (Feller holds iff >= 2)", d, 6.0, 12)
    r1 = c * rng.noncentral_chisquare(d, lam, 2_000_000)
    mm, se = mean_se(r1)
    simulated("E[r_1], exact non-central chi-squared sampling", mm, se, m)
    vv, se = var_se(r1)
    simulated("Var(r_1), exact sampling", vv, se, var)
    c_inf = sig**2 * (1 - math.exp(-k * 20)) / (4 * k)
    r_inf = c_inf * rng.noncentral_chisquare(d, r0 * math.exp(-k * 20) / c_inf, 2_000_000)
    mm, se = mean_se(r_inf)
    simulated("long-run mean (t = 20), exact sampling, vs theta", mm, se, th)
    vv, se = var_se(r_inf)
    simulated("long-run variance (t = 20), exact sampling, vs theta sigma^2/(2 kappa)", vv, se, th * sig**2 / (2 * k))
    sk = float(((r_inf - r_inf.mean()) ** 3).mean() / r_inf.var() ** 1.5)
    simulated("long-run skewness vs Gamma(shape 3): 2/sqrt(3)", sk, 0.01, 2 / math.sqrt(3))


def milstein_table() -> None:
    print("Euler and Milstein strong errors for GBM, mu = 0.05, sigma = 0.5, T = 1, 20,000 paths, seed 3 (worked example)")
    rng = np.random.default_rng(3)
    mu, sig, T, N, nf = 0.05, 0.5, 1.0, 20_000, 2**10
    dwf = rng.standard_normal((N, nf)) * math.sqrt(T / nf)
    exact_s = np.exp((mu - sig**2 / 2) * T + sig * dwf.sum(axis=1))
    quoted = {8: (0.0521, 0.00462), 16: (0.0377, 0.00255), 32: (0.0263, 0.00136), 64: (0.0186, 0.00071), 128: (0.0133, 0.00036)}
    em_err, mil_err = [], []
    for m, (q_em, q_mil) in quoted.items():
        dw, h = dwf.reshape(N, m, nf // m).sum(axis=2), T / m
        em, mil = np.ones(N), np.ones(N)
        for i in range(m):
            em *= 1 + mu * h + sig * dw[:, i]
            mil *= 1 + mu * h + sig * dw[:, i] + 0.5 * sig**2 * (dw[:, i] ** 2 - h)
        e1, e2 = float(np.abs(em - exact_s).mean()), float(np.abs(mil - exact_s).mean())
        approx(f"EM strong error, {m} steps", e1, q_em, 4)
        approx(f"Milstein strong error, {m} steps", e2, q_mil, 5)
        em_err.append(e1)
        mil_err.append(e2)
    lh = np.log(1.0 / np.array(list(quoted)))
    slope_em = float(np.polyfit(lh, np.log(em_err), 1)[0])
    slope_mil = float(np.polyfit(lh, np.log(mil_err), 1)[0])
    slope_mil_fine = float(np.polyfit(lh[2:], np.log(mil_err[2:]), 1)[0])
    approx("fitted strong order, Euler, 8 to 128 steps", slope_em, 0.50, 2)
    approx("fitted strong order, Milstein, 8 to 128 steps", slope_mil, 0.92, 2)
    approx("fitted strong order, Milstein, 32 to 128 steps", slope_mil_fine, 0.96, 2)
    ratios_em = np.array(em_err[:-1]) / np.array(em_err[1:])
    ratios_mil = np.array(mil_err[:-1]) / np.array(mil_err[1:])
    exact("Euler error ratio per halving, rounded", [round(float(r), 2) for r in ratios_em], [1.38, 1.43, 1.41, 1.41])
    exact("Milstein error ratio per halving, rounded", [round(float(r), 2) for r in ratios_mil], [1.81, 1.87, 1.93, 1.96])


def squared_bessel(rng: np.random.Generator) -> None:
    print("W^2 as a squared Bessel process (card sc-sde-w-squared-sde)")
    n, paths, T = 2000, 20_000, 1.0
    h = T / n
    w = np.cumsum(rng.standard_normal((paths, n)) * math.sqrt(h), axis=1)
    x = np.concatenate([np.zeros((paths, 1)), w**2], axis=1)
    qv = (np.diff(x, axis=1) ** 2).sum(axis=1)
    target = (4 * x[:, :-1] * h).sum(axis=1)  # [X]_T = int 4 X dt for dX = dt + 2 sqrt(X) dB
    rel = float(np.mean(np.abs(qv - target)) / np.mean(target))
    assert rel < 0.05, rel
    print(f"    sum (dX)^2 vs int 4 X dt: mean relative gap {rel:.3f} (-> 0 as the grid refines)")
    exact("Feller-type check 2a >= sigma^2 with a = 1, sigma = 2: 2 >= 4", 2 * 1 >= 2**2, False)


def main() -> None:
    rng = np.random.default_rng(SEED)
    gbm(rng)
    ou(rng)
    cir(rng)
    milstein_table()
    squared_bessel(rng)
    print("all SDE checks passed")


if __name__ == "__main__":
    main()
