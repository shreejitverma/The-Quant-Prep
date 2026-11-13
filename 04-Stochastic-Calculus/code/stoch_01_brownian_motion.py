"""Brownian motion: every moment, barrier probability and hitting-time result in the note.

Backs every number in `04-Stochastic-Calculus/01-Brownian-Motion.md`.
Independent routes used here:
- covariances and the bridge variance by exact rational arithmetic on the covariance min(s, t);
- quadratic and first variation by seeded simulation against their exact finite-n moments;
- the reflection law of the running maximum by exact simulation of the continuous maximum
  (Brownian-bridge maxima between grid points), never by the reflection formula itself;
- the hitting-time density by quadrature (its CDF and Laplace transform) and its infinite mean by
  the growth of the truncated mean;
- the grid bias of the maximum by Spitzer's identity E[max_k S_k] = sum_k E[S_k^+]/k (exact) and the
  constant -zeta(1/2)/sqrt(2 pi) computed by Euler-Maclaurin, then cross-checked by simulation;
- two-sided and one-sided barrier probabilities and exit times by finite-difference solution of the
  ODEs (sigma^2/2) u'' + mu u' = 0 or -1, and by bridge-corrected simulation;
- P(W_1 > 0, W_2 > 0) by quadrature of phi(x) Phi(x) and by simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 04-Stochastic-Calculus/code/stoch_01_brownian_motion.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261112


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
    print(f"    {label} ~ {estimate:.4f} (se {se:.1e}, target {target:.4f}, tolerance {k:g} se)")


def ncdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def mean_se(x: np.ndarray) -> tuple[float, float]:
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(x.size))


def trapezoid(y: np.ndarray, x: np.ndarray) -> float:
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))


def thomas(lower: np.ndarray, diag: np.ndarray, upper: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """Solve a tridiagonal system (lower[0] and upper[-1] unused)."""
    n = diag.size
    c, d = np.empty(n), np.empty(n)
    c[0], d[0] = upper[0] / diag[0], rhs[0] / diag[0]
    for i in range(1, n):
        m = diag[i] - lower[i] * c[i - 1]
        c[i] = upper[i] / m if i < n - 1 else 0.0
        d[i] = (rhs[i] - lower[i] * d[i - 1]) / m
    x = np.empty(n)
    x[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def solve_bvp(mu: float, sigma: float, lo: float, hi: float, u_lo: float, u_hi: float, source: float, n: int, x0: float) -> float:
    """Central finite differences for (sigma^2/2) u'' + mu u' = -source on [lo, hi]; returns u(x0)."""
    x = np.linspace(lo, hi, n + 1)
    h = x[1] - x[0]
    a, b = 0.5 * sigma**2 / h**2, mu / (2 * h)
    m = n - 1
    lower, diag, upper = np.full(m, a - b), np.full(m, -2 * a), np.full(m, a + b)
    rhs = np.full(m, -source)
    rhs[0] -= (a - b) * u_lo
    rhs[-1] -= (a + b) * u_hi
    u = np.concatenate([[u_lo], thomas(lower, diag, upper, rhs), [u_hi]])
    return float(np.interp(x0, x, u))


def bridge_max(x: np.ndarray, y: np.ndarray, h: float, rng: np.random.Generator) -> np.ndarray:
    """Exact sample of the maximum of a Brownian bridge from x to y over time h (unit volatility)."""
    return 0.5 * (x + y + np.sqrt((y - x) ** 2 - 2.0 * h * np.log(rng.random(x.shape))))


# ------------------------------------------------------------------ sections


def covariances(rng: np.random.Generator) -> None:
    print("Covariance of levels and the bridge (cards sc-bm-covariance-levels, sc-bm-scaling, sc-bm-bridge-variance)")
    cov = [[Fraction(min(s, t)) for t in (1, 2)] for s in (1, 2)]
    var = cov[0][0] + cov[1][1] + 2 * cov[0][1]
    exact("Var(W_1 + W_2) = 1 + 2 + 2*1", var, 5)
    z = rng.standard_normal((1_000_000, 2))
    w1, w2 = z[:, 0], z[:, 0] + z[:, 1]
    s = w1 + w2
    m, se = mean_se((s - s.mean()) ** 2)
    simulated("Var(W_1 + W_2), simulated", m, se, 5.0)
    # time inversion: Cov(s W_{1/s}, t W_{1/t}) = s t min(1/s, 1/t) = min(s, t)
    for s_, t_ in ((1 / 3, 2.0), (2.5, 1.75)):
        lo, hi = sorted((1 / s_, 1 / t_))
        zz = rng.standard_normal((1_000_000, 2))
        w_lo = math.sqrt(lo) * zz[:, 0]
        w_hi = w_lo + math.sqrt(hi - lo) * zz[:, 1]
        m, se = mean_se(s_ * t_ * w_lo * w_hi)
        simulated(f"Cov(s W_(1/s), t W_(1/t)) at (s, t) = ({s_:.4g}, {t_:g}), simulated, vs min(s, t)", m, se, min(s_, t_))
    # bridge B_t = W_t - (t/T) W_T on a 400-step grid of [0, 1]: Var(B_t) = t(T - t)/T
    n = 400
    dw = rng.standard_normal((50_000, n)) * math.sqrt(1 / n)
    w = np.cumsum(dw, axis=1)
    for t in (0.25, 0.5, 0.6):
        b = w[:, round(t * n) - 1] - t * w[:, -1]
        m, se = mean_se(b**2)
        simulated(f"Var(B_{t:g}), simulated, vs t(T - t)/T (largest, 1/4, at t = 1/2)", m, se, t * (1 - t))
    m, se = mean_se(b * w[:, -1])
    simulated("Cov(B_0.6, W_1), simulated (exact 0: independent of W_T)", m, se, 0.0)


def variation(rng: np.random.Generator) -> None:
    print("Quadratic and first variation, n = 400 steps on [0, 1] (cards sc-bm-quadratic-variation, sc-bm-total-variation)")
    n, T, paths = 400, 1.0, 50_000
    dw = rng.standard_normal((paths, n)) * math.sqrt(T / n)
    q = (dw**2).sum(axis=1)
    m, se = mean_se(q)
    simulated("E[Q_n], simulated (exact n Delta = T = 1)", m, se, T)
    v = float(q.var(ddof=1))
    se_v = v * math.sqrt(2 / (paths - 1)) * math.sqrt(1 + 6 / n)  # excess kurtosis of Q_n is 12/n
    simulated("Var(Q_n), simulated (exact 2 T^2 / n = 0.005)", v, se_v, 2 * T**2 / n)
    tv = np.abs(dw).sum(axis=1)
    m, se = mean_se(tv)
    exact_tv = math.sqrt(2 * n * T / math.pi)
    simulated("E sum |dW|, simulated (exact sqrt(2 n T / pi))", m, se, exact_tv)
    approx("sqrt(2 n T / pi) at n = 400", exact_tv, 15.96, 2)
    approx("sqrt(2 n T / pi) at n = 40000 (grows like sqrt(n))", math.sqrt(2 * 40_000 * T / math.pi), 159.58, 2)


def running_maximum(rng: np.random.Generator) -> None:
    print("Running maximum by exact bridge-maximum simulation (cards sc-bm-reflection-max, sc-bm-expected-max)")
    n, paths = 16, 1_000_000
    h = 1.0 / n
    m_cont = np.zeros(paths)
    w = np.zeros(paths)
    for _ in range(n):
        w_new = w + math.sqrt(h) * rng.standard_normal(paths)
        m_cont = np.maximum(m_cont, bridge_max(w, w_new, h, rng))
        w = w_new
    p_closed = 2 * (1 - ncdf(1.0))
    approx("2(1 - Phi(1))", p_closed, 0.3173, 4)
    m, se = mean_se((m_cont >= 1.0).astype(float))
    simulated("P(M_1 >= 1), exact continuous-maximum simulation", m, se, p_closed)
    approx("sqrt(2/pi)", math.sqrt(2 / math.pi), 0.798, 3)
    m, se = mean_se(m_cont)
    simulated("E[M_1], exact continuous-maximum simulation", m, se, math.sqrt(2 / math.pi))
    m, se = mean_se(m_cont**2)
    simulated("E[M_1^2], simulated (exact t = 1)", m, se, 1.0)
    for a in (0.5, 1.0, 2.0):  # the whole law: P(M >= a) = P(|W| >= a)
        mm, ss = mean_se((m_cont >= a).astype(float))
        simulated(f"P(M_1 >= {a}) vs 2(1 - Phi({a}))", mm, ss, 2 * (1 - ncdf(a)))
    joint = ((m_cont >= 1.0) & (w <= 0.0)).astype(float)
    mm, ss = mean_se(joint)
    simulated("P(M_1 >= 1, W_1 <= 0) vs P(W_1 >= 2)", mm, ss, 1 - ncdf(2.0))
    mm, ss = mean_se(((m_cont >= 1.0) & (w <= 0.5)).astype(float))
    simulated("P(M_1 >= 1, W_1 <= 0.5) vs P(W_1 >= 1.5)", mm, ss, 1 - ncdf(1.5))


def log_quad(fun, lo: float, hi: float, n: int = 400_000) -> float:
    """int_lo^hi fun(s) ds on a grid uniform in log s (the substitution s = e^u)."""
    u = np.linspace(math.log(lo), math.log(hi), n + 1)
    s = np.exp(u)
    return trapezoid(fun(s) * s, u)


def hitting_time() -> None:
    print("Hitting-time density by quadrature (cards sc-bm-hitting-time-mean, sc-bm-reflection-max)")
    a = 1.0

    def f(s: np.ndarray) -> np.ndarray:
        return a / np.sqrt(2 * math.pi * s**3) * np.exp(-(a**2) / (2 * s))

    for t in (0.5, 1.0, 4.0):
        approx(f"int_0^{t} f_tau(s) ds vs 2(1 - Phi(a/sqrt(t)))", log_quad(f, 1e-6, t), 2 * (1 - ncdf(a / math.sqrt(t))), 8)
    approx("total mass int_0^(1e14) f_tau (tau finite a.s.)", log_quad(f, 1e-6, 1e14), 1.0, 6)
    for lam in (0.5, 1.0, 3.0):
        lt = log_quad(lambda s, lam=lam: np.exp(-lam * s) * f(s), 1e-6, 1e4)
        approx(f"E[exp(-{lam} tau)] by quadrature vs exp(-a sqrt(2 lambda))", lt, math.exp(-a * math.sqrt(2 * lam)), 8)
    for t in (1e8, 1e12):  # the truncated mean int_0^t s f(s) ds grows like a sqrt(2t/pi): no finite mean
        approx(f"int_0^{t:g} s f(s) ds / sqrt({t:g}) vs sqrt(2/pi)", log_quad(lambda s: s * f(s), 1e-6, t) / math.sqrt(t), 0.798, 3)


def grid_bias(rng: np.random.Generator) -> None:
    print("Grid bias of the maximum, n = 400 steps (card sc-bm-discrete-monitoring-bias)")
    big = 1_000_000
    k = np.arange(1, big + 1, dtype=float)
    zeta_half = float(np.sum(k**-0.5)) - 2 * math.sqrt(big) - 0.5 / math.sqrt(big) + big**-1.5 / 24
    approx("zeta(1/2) by Euler-Maclaurin (cited value -1.4603545088)", zeta_half, -1.4603545088, 9)
    beta = -zeta_half / math.sqrt(2 * math.pi)
    approx("beta = -zeta(1/2)/sqrt(2 pi)", beta, 0.5826, 4)
    n = 400
    shift = beta / math.sqrt(n)
    approx("beta sqrt(Delta t) at Delta t = 1/400", shift, 0.029, 3)
    spitzer = math.sqrt(1 / (2 * math.pi * n)) * float(np.sum(np.arange(1, n + 1, dtype=float) ** -0.5))
    approx("E[max of the 400-step grid] by Spitzer's identity (exact)", spitzer, 0.7693, 4)
    approx("continuous E[M_1] - beta sqrt(Delta t)", math.sqrt(2 / math.pi) - shift, 0.7688, 4)
    approx("BGK-shifted P(grid max >= 1) = 2(1 - Phi(1 + beta/20))", 2 * (1 - ncdf(1 + shift)), 0.3034, 4)
    paths, chunk = 100_000, 20_000
    maxima = []
    for _ in range(paths // chunk):
        w = np.cumsum(rng.standard_normal((chunk, n)) * math.sqrt(1 / n), axis=1)
        maxima.append(np.maximum(w.max(axis=1), 0.0))
    mg = np.concatenate(maxima)
    m, se = mean_se(mg)
    simulated("E[grid max], 100k simulated paths, vs Spitzer", m, se, spitzer)
    m, se = mean_se((mg >= 1.0).astype(float))
    simulated("P(grid max >= 1), simulated, vs the BGK-shifted value", m, se, 2 * (1 - ncdf(1 + shift)))


def worked_examples() -> None:
    print("Worked examples: running maximum in trader units, both positive (cards sc-bm-both-positive, sc-bm-expected-max)")
    approx("sqrt(2/pi) to two decimals", math.sqrt(2 / math.pi), 0.80, 2)
    approx("expected 20-day high, 1% daily vol, in percent: sqrt(2/pi) sqrt(20)", math.sqrt(2 / math.pi) * math.sqrt(20), 3.57, 2)
    approx("P(touch +2 sd of the horizon move) = 2(1 - Phi(2)), percent", 200 * (1 - ncdf(2.0)), 4.55, 2)
    approx("terminal probability 1 - Phi(2), percent", 100 * (1 - ncdf(2.0)), 2.28, 2)
    x = np.linspace(0.0, 12.0, 1_200_001)
    phi = np.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)
    big_phi = 0.5 * (1 + np.vectorize(math.erf)(x / math.sqrt(2)))
    p = trapezoid(phi * big_phi, x)  # P(W_1 > 0, Z > -W_1) = int_0^inf phi(x) Phi(x) dx
    approx("P(W_1 > 0, W_2 > 0) by quadrature of phi(x) Phi(x)", p, 0.375, 9)
    approx("1/4 + arcsin(1/sqrt 2)/(2 pi) (Sheppard)", 0.25 + math.asin(1 / math.sqrt(2)) / (2 * math.pi), 0.375, 12)
    approx("P(W_2 > 0 | W_1 > 0) = quadrature / P(W_1 > 0)", p / 0.5, 0.75, 9)


def barriers(rng: np.random.Generator) -> None:
    print("Barriers with drift (cards sc-bm-exit-time-interval, sc-bm-negative-drift-ever-hit, sc-bm-positive-drift-hit-time)")
    mu, sig = 0.5, 1.0
    p_fd = solve_bvp(mu, sig, -1.0, 1.0, 0.0, 1.0, 0.0, 4000, 0.0)
    approx("P(hit +1 before -1), X = 0.5 t + W, by finite differences", p_fd, 0.731, 3)
    approx("    and 1/(1 + e^-1)", 1 / (1 + math.exp(-1)), p_fd, 6)
    th, a, b = 2 * mu / sig**2, 1.0, 1.0
    approx(
        "    and (e^{theta b} - 1)/(e^{theta b} - e^{-theta a})", (math.exp(th * b) - 1) / (math.exp(th * b) - math.exp(-th * a)), p_fd, 6
    )
    t_fd = solve_bvp(mu, sig, -1.0, 1.0, 0.0, 0.0, 1.0, 4000, 0.0)
    approx("E[exit time] by finite differences", t_fd, 0.924, 3)
    approx("    and 2(2p - 1)", 2 * (2 * p_fd - 1), t_fd, 6)
    # bridge-corrected simulation of the exit side: exact up to a double crossing within one step
    paths, h, steps = 400_000, 0.01, 1200
    x = np.zeros(paths)
    side = np.zeros(paths)  # +1 upper, -1 lower, 0 still inside
    for _ in range(steps):
        live = side == 0
        if not live.any():
            break
        x0 = x[live]
        x1 = x0 + mu * h + sig * math.sqrt(h) * rng.standard_normal(x0.size)
        up = np.exp(-2 * np.maximum(1 - x0, 0) * np.maximum(1 - x1, 0) / (sig**2 * h))
        dn = np.exp(-2 * np.maximum(x0 + 1, 0) * np.maximum(x1 + 1, 0) / (sig**2 * h))
        u = rng.random(x0.size)
        hit_up = (x1 >= 1) | (u < up)
        hit_dn = ~hit_up & ((x1 <= -1) | (u < up + dn))
        s = np.zeros(x0.size)
        s[hit_up], s[hit_dn] = 1.0, -1.0
        side[live] = s
        x[live] = x1
    assert not (side == 0).any(), "every path exits within the simulated horizon"
    m, se = mean_se((side == 1).astype(float))
    simulated("P(hit +1 before -1), bridge-corrected simulation, step 0.01", m, se, p_fd)
    # driftless exit times: (1/2) u'' = -1 gives u(0) = ab
    for lo, hi, quoted in ((-1.0, 1.0, 1.0), (-2.0, 3.0, 6.0)):
        approx(f"E[exit time of ({lo:g}, {hi:g})] by finite differences", solve_bvp(0.0, 1.0, lo, hi, 0.0, 0.0, 1.0, 2000, 0.0), quoted, 6)
        p_hi = solve_bvp(0.0, 1.0, lo, hi, 0.0, 1.0, 0.0, 2000, 0.0)
        wald = hi**2 * p_hi + lo**2 * (1 - p_hi)
        approx("    and optional stopping E[W_tau^2] = b^2 P(hit b) + a^2 P(hit -a), P by finite differences", wald, quoted, 6)
    # negative drift, ever hit +1: X = -t + W, solve on (-L, 1) with L large
    p_ever = solve_bvp(-1.0, 1.0, -30.0, 1.0, 0.0, 1.0, 0.0, 62_000, 0.0)
    approx("P(X = -t + W ever hits +1) by finite differences on (-30, 1)", p_ever, 0.135, 3)
    approx("    and e^-2", math.exp(-2), p_ever, 5)
    # positive drift first-passage mean: a/mu by quadrature of the inverse-Gaussian density
    mu2, sig2, a2 = 0.7, 1.3, 2.0

    def ig(s: np.ndarray) -> np.ndarray:
        return a2 / (sig2 * np.sqrt(2 * math.pi * s**3)) * np.exp(-((a2 - mu2 * s) ** 2) / (2 * sig2**2 * s))

    approx("E[tau_a] by quadrature, mu = 0.7, sigma = 1.3, a = 2, vs a/mu", log_quad(lambda s: s * ig(s), 1e-6, 1e4), a2 / mu2, 6)


def doubling() -> None:
    print("Will a stock with negative log drift ever double? (worked example; card sc-ps-gbm-ever-double in note 09)")
    mu, sig = 0.02, 0.30
    nu = mu - 0.5 * sig**2
    approx("log drift nu = mu - sigma^2/2", nu, -0.025, 6)
    p_fd = solve_bvp(nu, sig, -60.0, math.log(2), 0.0, 1.0, 0.0, 120_000, 0.0)
    approx("P(ever double) by finite differences on (-60, log 2)", p_fd, 0.680, 3)
    approx("    and 2^(2 mu / sigma^2 - 1)", 2 ** (2 * mu / sig**2 - 1), p_fd, 5)
    p0 = solve_bvp(-0.5 * sig**2, sig, -60.0, math.log(2), 0.0, 1.0, 0.0, 120_000, 0.0)
    approx("mu = 0: P(ever double) by finite differences (Doob bound 1/2 attained)", p0, 0.5, 5)


def main() -> None:
    rng = np.random.default_rng(SEED)
    covariances(rng)
    variation(rng)
    running_maximum(rng)
    hitting_time()
    grid_bias(rng)
    worked_examples()
    barriers(rng)
    doubling()
    print("all Brownian motion checks passed")


if __name__ == "__main__":
    main()
