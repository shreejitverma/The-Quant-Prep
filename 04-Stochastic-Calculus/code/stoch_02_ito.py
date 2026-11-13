"""Ito integral and Ito's lemma: every moment, variance and correction in the note.

Backs every number in `04-Stochastic-Calculus/02-Ito-Integral-and-Ito-Lemma.md`.
Independent routes used here:
- int W dW: seeded simulation of left-endpoint (Ito) and midpoint (Stratonovich) sums against
  (W_T^2 - T)/2 and W_T^2/2, the discrete Ito-sum variance T^2 (n-1)/(2n) in exact rationals, and the
  mean gap E|I_n - (W^2 - T)/2| from the exact chi-squared mean absolute deviation;
- moments of W_t from the Ito recursion E[W^n] = C(n,2) int E[W^(n-2)] in exact rationals, against
  Gauss-Hermite quadrature (exact for polynomials) and simulation;
- int_0^T W dt by 2-D quadrature of the covariance min(s, t) and by simulation, not by the isometry;
- E[cos W_t], E[e^{W_t}] and the martingale property of e^{t/2} cos W_t by Gauss-Hermite quadrature;
- the covariation d[W, B] = rho dt and the product rule by simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 04-Stochastic-Calculus/code/stoch_02_ito.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261113


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


def mean_se(x: np.ndarray) -> tuple[float, float]:
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(x.size))


def var_se(x: np.ndarray) -> tuple[float, float]:
    """Sample variance and its standard error from the fourth central moment."""
    c = x - x.mean()
    v = float((c**2).mean())
    return v, float(math.sqrt(max((c**4).mean() - v * v, 0.0) / x.size))


GH_X, GH_W = np.polynomial.hermite_e.hermegauss(80)
GH_W = GH_W / GH_W.sum()  # E[g(Z)] ~ sum w_i g(x_i) for Z ~ N(0, 1)


def gauss(g, t: float) -> float:
    """E[g(W_t)] by 80-point Gauss-Hermite quadrature (exact for polynomials of degree < 160)."""
    return float(np.sum(GH_W * g(math.sqrt(t) * GH_X)))


def ito_w_dw(rng: np.random.Generator) -> None:
    print("int_0^T W dW, n = 400 steps, T = 1 (cards sc-ito-w-dw, sc-ito-w-dw-variance, sc-ito-left-endpoint, sc-ito-stratonovich)")
    n, T, paths = 400, 1.0, 30_000
    h = T / n
    # half-steps so the true midpoint W_{(t_i + t_{i+1})/2} is available for the Stratonovich sum
    dz = rng.standard_normal((paths, 2 * n)) * math.sqrt(h / 2)
    wf = np.concatenate([np.zeros((paths, 1)), np.cumsum(dz, axis=1)], axis=1)
    w = wf[:, ::2]  # grid values W_0, ..., W_T
    mid = wf[:, 1::2]  # midpoints
    dw = np.diff(w, axis=1)
    wl, wr, wt = w[:, :-1], w[:, 1:], w[:, -1]
    ito = (wl * dw).sum(axis=1)
    right = (wr * dw).sum(axis=1)
    strat_mid = (mid * dw).sum(axis=1)
    strat_avg = (0.5 * (wl + wr) * dw).sum(axis=1)
    qv = (dw**2).sum(axis=1)
    assert np.max(np.abs(ito - 0.5 * (wt**2 - qv))) < 1e-12  # the telescoping identity, path by path
    assert np.max(np.abs(strat_avg - 0.5 * wt**2)) < 1e-12
    print("    sum W_i dW_i = (W_T^2 - sum dW_i^2)/2 and sum (W_i + W_i+1)/2 dW_i = W_T^2/2 hold path by path")
    m, se = mean_se(right - ito)
    simulated("E[right sum - left sum] (= E sum dW^2 = T)", m, se, T)
    m, se = mean_se(ito)
    simulated("E[Ito sum] (exact 0)", m, se, 0.0)
    v, se = var_se(ito)
    v_discrete = Fraction(1) ** 2 * Fraction(n - 1, 2 * n)  # sum_i E[W_{t_i}^2] h = h^2 (0 + 1 + ... + n-1)
    exact("exact Var of the 400-step Ito sum, T^2 (n-1)/(2n)", v_discrete, Fraction(399, 800))
    approx("    as a decimal", float(v_discrete), 0.49875, 5)
    simulated("Var(Ito sum), simulated, vs T^2 (n-1)/(2n)", v, se, float(v_discrete))
    # E|I_n - (W^2 - T)/2| = E|Q_n - T|/2 with n Q_n / T ~ chi^2_n; MAD of Gamma(k, 2) is 4 k^k e^-k / Gamma(k)
    k = n / 2
    mad = 4 * math.exp(k * math.log(k) - k - math.lgamma(k)) / n * T / 2
    approx("E|Ito sum - (W_T^2 - T)/2| exact, n = 400", mad, 0.028, 3)
    m, se = mean_se(np.abs(ito - 0.5 * (wt**2 - T)))
    simulated("    simulated", m, se, mad)
    k4 = 4 * n / 2
    approx(
        "    the same gap at n = 1600 (halves when n quadruples)",
        4 * math.exp(k4 * math.log(k4) - k4 - math.lgamma(k4)) / (4 * n) / 2,
        0.014,
        3,
    )
    m, se = mean_se(strat_mid - ito)
    simulated("E[midpoint (Stratonovich) sum - Ito sum] (= T/2)", m, se, T / 2)
    approx("    the simulated mean quoted in the note (seed above)", m, 0.4999, 4)
    m, se = mean_se(np.abs(strat_mid - 0.5 * wt**2))
    print(f"    E|midpoint sum - W_T^2/2| = {m:.4f} (shrinks like n^-1/2; Stratonovich limit is W_T^2/2)")
    assert m < 0.03


def moments(rng: np.random.Generator) -> None:
    print("Moments of W_t from the Ito recursion (cards sc-ito-fourth-moment, sc-ps-bm-moments-general)")

    # E[W_t^n] = c_n t^(n/2): the recursion gives c_n = C(n, 2) c_{n-2} / (n/2) since int_0^t s^(n/2 - 1) ds = t^(n/2)/(n/2)
    c = {0: Fraction(1)}
    for m in range(2, 9, 2):
        c[m] = Fraction(math.comb(m, 2)) * c[m - 2] / Fraction(m, 2)
    exact("E[W_t^{2k}] / t^k for 2k = 2, 4, 6, 8", [c[m] for m in (2, 4, 6, 8)], [1, 3, 15, 105])
    exact("(2k - 1)!! for k = 1..4", [math.prod(range(1, 2 * kk, 2)) for kk in range(1, 5)], [1, 3, 15, 105])
    t = 0.7
    for m in (2, 4, 6, 8):
        approx(f"E[W_0.7^{m}] by Gauss-Hermite vs recursion", gauss(lambda x, m=m: x**m, t), float(c[m]) * t ** (m // 2), 10)
    exact("int_0^t 6 s ds = 3 t^2: coefficient", Fraction(6) * Fraction(1, 2), Fraction(3))
    w = rng.standard_normal(2_000_000) * math.sqrt(t)
    mm, se = mean_se(w**4)
    simulated("E[W_0.7^4], simulated, vs 3 t^2", mm, se, 3 * t * t)


def time_integral(rng: np.random.Generator) -> None:
    print("int_0^T W dt and int_0^T t dW (cards sc-ito-time-integral-distribution, sc-ito-deterministic-integrand)")
    T = 2.0
    g = np.linspace(0.0, T, 2001)
    s_, t_ = np.meshgrid(g, g, indexing="ij")
    cov = np.minimum(s_, t_)
    inner = np.sum(0.5 * (cov[:, 1:] + cov[:, :-1]) * np.diff(g), axis=1)
    var_a = float(np.sum(0.5 * (inner[1:] + inner[:-1]) * np.diff(g)))
    approx("Var(int_0^2 W dt) = int int min(s,t) by 2-D quadrature vs T^3/3", var_a, T**3 / 3, 6)
    cov_wa = float(np.sum(0.5 * (g[1:] + g[:-1]) * np.diff(g)))
    approx("Cov(W_T, int_0^T W dt) = int_0^T min(t, T) dt vs T^2/2", cov_wa, T**2 / 2, 9)
    n, paths = 500, 100_000
    h = T / n
    dw = rng.standard_normal((paths, n)) * math.sqrt(h)
    w = np.concatenate([np.zeros((paths, 1)), np.cumsum(dw, axis=1)], axis=1)
    a = (0.5 * (w[:, 1:] + w[:, :-1]) * h).sum(axis=1)
    v, se = var_se(a)
    simulated("Var(int_0^2 W dt), simulated, vs T^3/3 = 8/3", v, se, T**3 / 3)
    mm, se = mean_se(a * w[:, -1])
    simulated("Cov(W_2, int_0^2 W dt), simulated, vs T^2/2 = 2", mm, se, T**2 / 2)
    tl = np.arange(n) * h
    b = (tl * dw).sum(axis=1)
    v, se = var_se(b)
    simulated("Var(int_0^2 t dW), simulated, vs T^3/3", v, se, T**3 / 3, k=5.0)
    # integration by parts T W_T = int W dt + int t dW, path by path up to the O(h) quadrature difference
    gap = np.abs(T * w[:, -1] - a - b)
    assert float(gap.mean()) < 0.02
    print(f"    T W_T - int W dt - int t dW: mean absolute gap {float(gap.mean()):.4f} on the 500-step grid (-> 0)")


def martingales() -> None:
    print("Exponential and cosine martingales by Gauss-Hermite quadrature (cards sc-ito-cos-martingale, sc-ito-exp-martingale)")
    t = 0.9
    approx("E[cos W_0.9] vs e^{-t/2}", gauss(np.cos, t), math.exp(-t / 2), 12)
    approx("E[e^{W_0.9}] vs e^{t/2}", gauss(np.exp, t), math.exp(t / 2), 12)
    approx("E[e^{W_t - t/2}] = 1", gauss(lambda x: np.exp(x - t / 2), t), 1.0, 12)
    s = 0.3
    for x in (-1.2, 0.4, 2.0):  # E[e^{t/2} cos W_t | W_s = x] = e^{s/2} cos x
        val = math.exp(t / 2) * gauss(lambda z, x=x: np.cos(x + z), t - s)
        approx(f"E[e^(t/2) cos W_t | W_s = {x}] vs e^(s/2) cos x", val, math.exp(s / 2) * math.cos(x), 12)
    for a in (0.0, 0.25, 1.0):  # drift of e^{at} cos W_t is (a - 1/2) e^{at} cos W_t
        val = math.exp(a * t) * gauss(np.cos, t)
        approx(f"E[e^({a} t) cos W_t] vs e^((a - 1/2) t)", val, math.exp((a - 0.5) * t), 12)


def covariation(rng: np.random.Generator) -> None:
    print("Correlated drivers: d[W, B] = rho dt and the product rule (cards sc-ito-quadratic-covariation, sc-ito-product-rule)")
    rho, T, n, paths = 0.6, 1.0, 400, 50_000
    h = T / n
    z1 = rng.standard_normal((paths, n))
    z2 = rho * z1 + math.sqrt(1 - rho * rho) * rng.standard_normal((paths, n))
    dw, db = z1 * math.sqrt(h), z2 * math.sqrt(h)
    cv = (dw * db).sum(axis=1)
    mm, se = mean_se(cv)
    simulated("sum dW dB, simulated, vs rho T = 0.6", mm, se, rho * T)
    sd = float(cv.std(ddof=1))
    approx("    its standard deviation sqrt((1 + rho^2) h T) -> 0", math.sqrt((1 + rho * rho) * h * T), 0.058, 3)
    assert abs(sd - math.sqrt((1 + rho * rho) * h * T)) < 0.002
    sx, sy = 0.3, 0.5
    xt, yt = sx * dw.sum(axis=1), sy * db.sum(axis=1)
    mm, se = mean_se(xt * yt)
    simulated("E[X_T Y_T] for dX = 0.3 dW, dY = 0.5 dB: int d[X, Y] = rho sx sy T = 0.09", mm, se, rho * sx * sy * T)


def main() -> None:
    rng = np.random.default_rng(SEED)
    ito_w_dw(rng)
    moments(rng)
    time_integral(rng)
    martingales()
    covariation(rng)
    print("all Ito checks passed")


if __name__ == "__main__":
    main()
