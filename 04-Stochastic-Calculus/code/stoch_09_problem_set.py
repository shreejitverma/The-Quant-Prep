"""Stochastic calculus problem set: every answer in the worked examples and the 39 cards.

Backs every number in `04-Stochastic-Calculus/09-Stochastic-Calculus-Problem-Set.md`.
Independent routes used here:
- Brownian moments from the Ito recursion and from the MGF series, both in exact rationals, and
  Gaussian expectations (including two-time ones via the independent increment) by Gauss-Hermite
  quadrature, which is exact for polynomials;
- the variance of int W^2 dW by exact rational bookkeeping of the three terms and by simulation of the
  Ito sum, whose discrete variance 3 h^3 sum i^2 is exact;
- martingale claims by checking E[f(t, W_t) | W_s = x] = f(s, x) with Gauss-Hermite quadrature,
  and the Hermite generating function by exact polynomial expansion;
- barrier probabilities and exit times by finite-difference solution of the ODEs, the reflection
  joint law by a Brownian-bridge quadrature and by exact bridge-maximum simulation, first-passage
  moments by quadrature of the inverse-Gaussian density;
- OU and AR(1) facts by simulating the recursion; GBM facts by quadrature and simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 04-Stochastic-Calculus/code/stoch_09_problem_set.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261117


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


def var_se(x: np.ndarray) -> tuple[float, float]:
    c = x - x.mean()
    v = float((c**2).mean())
    return v, float(math.sqrt(max((c**4).mean() - v * v, 0.0) / x.size))


GH_X, GH_W = np.polynomial.hermite_e.hermegauss(100)
GH_W = GH_W / GH_W.sum()


def gauss(g, t: float) -> float:
    """E[g(W_t)] by Gauss-Hermite quadrature."""
    return float(np.sum(GH_W * g(math.sqrt(t) * GH_X)))


def gauss2(g, s: float, t: float) -> float:
    """E[g(W_s, W_t)] for s < t, writing W_t = W_s + sqrt(t - s) Z with Z independent."""
    a = math.sqrt(s) * GH_X[:, None]
    b = a + math.sqrt(t - s) * GH_X[None, :]
    return float(np.sum(GH_W[:, None] * GH_W[None, :] * g(a, b)))


def log_quad(fun, lo: float, hi: float, n: int = 400_000) -> float:
    u = np.linspace(math.log(lo), math.log(hi), n + 1)
    s = np.exp(u)
    y = fun(s) * s
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(u)))


def thomas(lower: np.ndarray, diag: np.ndarray, upper: np.ndarray, rhs: np.ndarray) -> np.ndarray:
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


def solve_bvp(mu: float, sigma: float, lo: float, hi: float, u_lo: float, u_hi: float, source: float, n: int) -> float:
    """Central finite differences for (sigma^2/2) u'' + mu u' = -source on [lo, hi]; returns u(0)."""
    x = np.linspace(lo, hi, n + 1)
    h = x[1] - x[0]
    a, b = 0.5 * sigma**2 / h**2, mu / (2 * h)
    m = n - 1
    rhs = np.full(m, -source)
    rhs[0] -= (a - b) * u_lo
    rhs[-1] -= (a + b) * u_hi
    u = np.concatenate([[u_lo], thomas(np.full(m, a - b), np.full(m, -2 * a), np.full(m, a + b), rhs), [u_hi]])
    return float(np.interp(0.0, x, u))


# ------------------------------------------------------------------ polynomials in (t, x) as dicts {(i, j): coeff}


def poly_check_martingale(poly: dict[tuple[int, int], Fraction]) -> dict[tuple[int, int], Fraction]:
    """Return f_t + (1/2) f_xx for f = sum c t^i x^j."""
    out: dict[tuple[int, int], Fraction] = {}
    for (i, j), c in poly.items():
        if i:
            out[(i - 1, j)] = out.get((i - 1, j), Fraction(0)) + c * i
        if j >= 2:
            out[(i, j - 2)] = out.get((i, j - 2), Fraction(0)) + c * j * (j - 1) / 2
    return {k: v for k, v in out.items() if v != 0}


def moments() -> None:
    print("All moments of W_t (worked example; card sc-ps-bm-moments-general)")
    c = {0: Fraction(1)}
    for n in range(2, 13, 2):
        c[n] = Fraction(math.comb(n, 2)) * c[n - 2] / Fraction(n, 2)
    exact("E[W_t^n]/t^(n/2) for n = 2, 4, 6 by the Ito recursion", [c[2], c[4], c[6]], [1, 3, 15])
    exact("6 * (1/2) and 15 * 3 * (1/3): the two integration steps", (Fraction(6, 2), Fraction(15 * 3, 3)), (Fraction(3), Fraction(15)))
    mgf = [Fraction(math.factorial(2 * k), 2**k * math.factorial(k)) for k in range(1, 7)]
    exact("MGF coefficients (2k)!/(2^k k!) for k = 1..6", mgf, [c[2 * k] for k in range(1, 7)])
    exact("(n - 1)!! for n = 2..12 even", [math.prod(range(1, n, 2)) for n in range(2, 13, 2)], [int(c[n]) for n in range(2, 13, 2)])
    for n in (3, 5):
        approx(f"E[W_1^{n}] by quadrature (odd: zero)", gauss(lambda x, n=n: x**n, 1.0), 0.0, 12)


def int_w2_dw(rng: np.random.Generator) -> None:
    print("int_0^T W^2 dW (worked example; cards sc-ps-ito-w-cubed, sc-ps-int-w-squared-dw, sc-ps-isometry-w-squared)")
    var_cube = Fraction(15, 9)
    var_a = Fraction(1, 3)
    cov = Fraction(3, 2)
    exact("Var(W_T^3 / 3) / T^3 = 15/9", var_cube, Fraction(5, 3))
    exact("total (5/3 + 1/3 - 2 (1/3)(3/2)) T^3", var_cube + var_a - 2 * Fraction(1, 3) * cov, Fraction(1))
    for t in (0.3, 0.7):  # E[W_T^3 W_t] = 3 t T at T = 1
        approx(f"E[W_1^3 W_{t}] by quadrature vs 3 t T", gauss2(lambda a, b: b**3 * a, t, 1.0), 3 * t, 12)
    approx("E[W_1^6] / 9 = 15/9", gauss(lambda x: x**6, 1.0) / 9, 15 / 9, 12)
    approx("isometry int_0^1 E[W_t^4] dt = int 3 t^2 dt", 3 * float(np.mean(np.linspace(0, 1, 1_000_001) ** 2)), 1.0, 5)
    n, paths, T = 500, 50_000, 1.0
    h = T / n
    dw = rng.standard_normal((paths, n)) * math.sqrt(h)
    w = np.concatenate([np.zeros((paths, 1)), np.cumsum(dw, axis=1)], axis=1)
    ito = (w[:, :-1] ** 2 * dw).sum(axis=1)
    disc_var = 3 * h**3 * (n - 1) * n * (2 * n - 1) / 6  # sum_i E[W_{t_i}^4] h = 3 h^3 sum i^2
    v, se = var_se(ito)
    simulated("Var of the 500-step Ito sum of W^2 dW vs 3 h^3 sum i^2", v, se, disc_var)
    approx("    which tends to T^3", disc_var, 1.0, 2)
    a = (0.5 * (w[:, 1:] + w[:, :-1]) * h).sum(axis=1)
    gap = np.abs(ito - (w[:, -1] ** 3 / 3 - a))
    assert float(gap.mean()) < 0.06
    print(f"    Ito sum vs W_T^3/3 - int W dt: mean absolute gap {float(gap.mean()):.4f} on 500 steps (-> 0 like n^-1/2)")


def max_end_below(rng: np.random.Generator) -> None:
    print("P(max W >= 1, W_1 <= 0) (worked example; card sc-ps-max-and-end-below)")
    target = 1 - ncdf(2.0)
    approx("1 - Phi(2)", target, 0.0228, 4)
    w = np.linspace(-12.0, 0.0, 1_200_001)
    y = np.exp(-2 * (1 - w)) * np.exp(-0.5 * w**2) / math.sqrt(2 * math.pi)
    approx("Brownian-bridge quadrature int_{w<0} e^{-2(1-w)} phi(w) dw", float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(w))), target, 9)
    n, paths = 100, 400_000
    h = 1.0 / n
    x = np.zeros(paths)
    mx_grid = np.zeros(paths)
    mx_exact = np.zeros(paths)
    for _ in range(n):
        x_new = x + math.sqrt(h) * rng.standard_normal(paths)
        bridge = 0.5 * (x + x_new + np.sqrt((x_new - x) ** 2 - 2 * h * np.log(rng.random(paths))))
        mx_exact = np.maximum(mx_exact, bridge)
        mx_grid = np.maximum(mx_grid, x_new)
        x = x_new
    m, se = mean_se(((mx_exact >= 1) & (x <= 0)).astype(float))
    simulated("exact bridge-maximum simulation, 100 steps", m, se, target)
    m, se = mean_se(((mx_grid >= 1) & (x <= 0)).astype(float))
    approx("grid-monitored simulation, 100 steps (biased low)", m, 0.017, 3)
    bgk = 1 - ncdf(2 * (1 + 0.5826 * math.sqrt(h)))  # barrier shifted up by beta sqrt(h), beta = -zeta(1/2)/sqrt(2 pi)
    approx("Broadie-Glasserman-Kou shifted value 1 - Phi(2 (1 + 0.5826/10))", bgk, 0.0172, 4)
    simulated("grid simulation vs the shifted value", m, se, bgk)
    assert m < target - 4 * se


def barriers() -> None:
    print("Barriers and first passage (worked example; cards sc-ps-hit-asymmetric, sc-ps-exit-time-asymmetric, sc-ps-drift-*)")
    p = solve_bvp(1.0, 1.0, -1.0, 1.0, 0.0, 1.0, 0.0, 4000)
    approx("P(X = t + W hits +1 before -1) by finite differences", p, 0.881, 3)
    approx("    and 1/(1 + e^-2)", 1 / (1 + math.exp(-2)), p, 6)
    approx("    and (e^2 - 1)/(e^2 - e^-2)", (math.exp(2) - 1) / (math.exp(2) - math.exp(-2)), p, 6)
    approx("P(W hits +1 before -2) by finite differences", solve_bvp(0.0, 1.0, -2.0, 1.0, 0.0, 1.0, 0.0, 3000), 2 / 3, 6)
    exact("p + (1 - p)(-2) = 0 at p = 2/3", Fraction(2, 3) - 2 * Fraction(1, 3), 0)
    approx("E[exit time of (-2, 3)] by finite differences", solve_bvp(0.0, 1.0, -2.0, 3.0, 0.0, 0.0, 1.0, 2000), 6.0, 6)
    p_ever = solve_bvp(-0.1, 0.2, -6.0, 0.1, 0.0, 1.0, 0.0, 61_000)
    approx("P(X = -0.1 t + 0.2 W ever hits 0.1) by finite differences on (-6, 0.1)", p_ever, 0.607, 3)
    approx("    and e^{-2 (0.1)(0.1)/0.04} = e^-0.5", math.exp(-2 * 0.1 * 0.1 / 0.04), p_ever, 5)

    def ig(a: float, mu: float, sig: float):
        def f(s: np.ndarray) -> np.ndarray:
            return a / (sig * np.sqrt(2 * math.pi * s**3)) * np.exp(-((a - mu * s) ** 2) / (2 * sig**2 * s))

        return f

    for a, mu, sig, m_q, v_q in ((1.0, 1.0, 1.0, 1.0, 1.0), (1.0, 0.5, 1.0, 2.0, 8.0), (2.0, 0.3, 0.7, 2 / 0.3, 2 * 0.49 / 0.027)):
        f = ig(a, mu, sig)
        mass = log_quad(f, 1e-7, 1e5)
        m1 = log_quad(lambda s, f=f: s * f(s), 1e-7, 1e5)
        m2 = log_quad(lambda s, f=f: s * s * f(s), 1e-7, 1e5)
        approx(f"IG mass, a = {a}, mu = {mu}, sigma = {sig}", mass, 1.0, 8)
        approx("    mean by quadrature vs a/mu", m1, m_q, 6)
        approx("    variance by quadrature vs a sigma^2/mu^3", m2 - m1 * m1, v_q, 5)


def ou_ar1(rng: np.random.Generator) -> None:
    print("Mean reversion in numbers: daily AR(1) coefficient 0.9, residual sd 0.5 (worked example; cards sc-ps-ou-*)")
    kappa = -math.log(0.9)
    approx("kappa = -ln 0.9 per day", kappa, 0.105, 3)
    approx("half-life ln 2 / kappa, days", math.log(2) / kappa, 6.6, 1)
    approx("stationary variance 0.25 / (1 - 0.81)", 0.25 / 0.19, 1.316, 3)
    approx("stationary sd", math.sqrt(0.25 / 0.19), 1.15, 2)
    sig2 = 0.25 * 2 * kappa / (1 - 0.81)  # OU sigma^2 implied by residual variance (sigma^2/2kappa)(1 - e^{-2 kappa})
    approx("OU stationary variance sigma^2/(2 kappa) from the exact discretisation", sig2 / (2 * kappa), 1.316, 3)
    chains, steps = 200_000, 200
    x = np.zeros(chains)
    for _ in range(steps):
        x = 0.9 * x + 0.5 * rng.standard_normal(chains)
    v, se = var_se(x)
    simulated("variance after 200 steps of the recursion (0.81^200 negligible)", v, se, 0.25 / 0.19)
    lag = 5
    y = x.copy()
    for _ in range(lag):
        y = 0.9 * y + 0.5 * rng.standard_normal(chains)
    m, se = mean_se(x * y / (0.25 / 0.19))
    simulated("stationary Corr(X_s, X_{s+5}) vs e^{-5 kappa} = 0.9^5", m, se, 0.9**lag)
    half = 0.9 ** (math.log(2) / kappa)
    approx("0.9^(half-life) = 1/2", half, 0.5, 12)


def martingales() -> None:
    print("Recognising martingales (worked example; cards sc-ps-mart-*)")
    cases = {
        "W^3": {(0, 3): Fraction(1)},
        "W^3 - 3tW": {(0, 3): Fraction(1), (1, 1): Fraction(-3)},
        "W^4 - 6tW^2 + 3t^2": {(0, 4): Fraction(1), (1, 2): Fraction(-6), (2, 0): Fraction(3)},
        "W^2 - t": {(0, 2): Fraction(1), (1, 0): Fraction(-1)},
    }
    exact("drift of W^3 (f_t + f_xx/2)", poly_check_martingale(cases["W^3"]), {(0, 1): Fraction(3)})
    for name in ("W^3 - 3tW", "W^4 - 6tW^2 + 3t^2", "W^2 - t"):
        exact(f"drift of {name}", poly_check_martingale(cases[name]), {})
    s, t = 0.4, 1.3
    for x0 in (-0.8, 0.5, 1.7):
        approx(
            f"E[W_t^3 - 3tW_t | W_s = {x0}] vs W_s^3 - 3sW_s",
            gauss(lambda z, x0=x0: (x0 + z) ** 3 - 3 * t * (x0 + z), t - s),
            x0**3 - 3 * s * x0,
            12,
        )
        approx(
            f"E[W_t^4 - 6tW_t^2 + 3t^2 | W_s = {x0}] vs the same at s",
            gauss(lambda z, x0=x0: (x0 + z) ** 4 - 6 * t * (x0 + z) ** 2 + 3 * t * t, t - s),
            x0**4 - 6 * s * x0**2 + 3 * s * s,
            11,
        )
        approx(
            f"E[e^(t/2) sin W_t | W_s = {x0}] vs e^(s/2) sin x",
            math.exp(t / 2) * gauss(lambda z, x0=x0: np.sin(x0 + z), t - s),
            math.exp(s / 2) * math.sin(x0),
            12,
        )
        approx(
            f"E[W_t^3 | W_s = {x0}] - x^3 = 3x(t - s) (not a martingale)",
            gauss(lambda z, x0=x0: (x0 + z) ** 3, t - s) - x0**3,
            3 * x0 * (t - s),
            12,
        )
    # Hermite generating function: e^{theta x - theta^2 t/2} = sum theta^n/n! H_n(t, x)
    he = {3: {(0, 3): Fraction(1), (1, 1): Fraction(-3)}, 4: cases["W^4 - 6tW^2 + 3t^2"]}
    for n, poly in he.items():
        coeff: dict[tuple[int, int], Fraction] = {}
        for k in range(n // 2 + 1):  # theta^n coefficient of sum_a (theta x)^a/a! * sum_b (-theta^2 t/2)^b/b! with a + 2b = n
            a = n - 2 * k
            coeff[(k, a)] = Fraction((-1) ** k, math.factorial(a) * math.factorial(k) * 2**k) * math.factorial(n)
        exact(f"n! [theta^{n}] e^(theta W - theta^2 t/2)", {k: v for k, v in coeff.items() if v}, poly)
    for b in (-0.5, -0.125):  # e^{aW + bt} is a martingale iff b = -a^2/2: E[e^{aW_t + bt}] = e^{(b + a^2/2) t}
        a = math.sqrt(-2 * b)
        approx(f"E[e^(aW_t + bt)] with a = {a:g}, b = {b} at t = 1.3", gauss(lambda x, a=a, b=b: np.exp(a * x + b * t), t), 1.0, 12)


def gaussian_cards(rng: np.random.Generator) -> None:
    print("Gaussian cards (sc-ps-exp-bm-mean-var, sc-ps-w-exp-w, sc-ps-sum-levels-tail, sc-ps-product-squares, ...)")
    t = 0.6
    approx("E[e^{W_0.6}] vs e^{t/2}", gauss(np.exp, t), math.exp(t / 2), 12)
    approx("Var(e^{W_0.6}) vs e^{2t} - e^t", gauss(lambda x: np.exp(2 * x), t) - gauss(np.exp, t) ** 2, math.exp(2 * t) - math.exp(t), 11)
    approx("E[W_0.6 e^{W_0.6}] vs t e^{t/2}", gauss(lambda x: x * np.exp(x), t), t * math.exp(t / 2), 12)
    p = 1 - ncdf(2 / math.sqrt(5))
    approx("P(W_1 + W_2 > 2) = 1 - Phi(2/sqrt 5)", p, 0.186, 3)
    approx("Var(W_1 + W_2) by quadrature", gauss2(lambda a, b: (a + b) ** 2, 1.0, 2.0), 5.0, 12)
    z = rng.standard_normal((2_000_000, 2))
    w1, w2 = z[:, 0], z[:, 0] + z[:, 1]
    m, se = mean_se((w1 + w2 > 2).astype(float))
    simulated("P(W_1 + W_2 > 2), simulated", m, se, p)
    s, tt = 0.5, 2.0
    approx(
        "E[W_s^2 W_t^2] at s = 0.5, t = 2 by quadrature vs 2 s^2 + s t", gauss2(lambda a, b: a * a * b * b, s, tt), 2 * s * s + s * tt, 12
    )
    exact("3 s^2 + s (t - s) = 2 s^2 + s t (s = 1/2, t = 2)", Fraction(3, 4) + Fraction(1, 2) * Fraction(3, 2), Fraction(3, 2))
    ws = z[:, 0] * math.sqrt(0.3)
    wt = ws + z[:, 1] * math.sqrt(0.9)
    slope = float(ws @ wt / (wt @ wt))
    simulated("regression slope of W_0.3 on W_1.2 vs s/t = 0.25", slope, 0.001, 0.25)
    T = 1.0
    g = np.linspace(0.0, T, 1501)
    ss, tt2 = np.meshgrid(g, g, indexing="ij")
    cov = np.minimum(ss, tt2)
    inner = np.sum(0.5 * (cov[:, 1:] + cov[:, :-1]) * np.diff(g), axis=1)
    v_a = float(np.sum(0.5 * (inner[1:] + inner[:-1]) * np.diff(g)))
    approx("Var(int_0^1 W dt) by 2-D quadrature of min(s,t)", v_a, 1 / 3, 6)
    approx("E[exp(int_0^1 W dt)] = e^{Var/2} vs e^{T^3/6}", math.exp(v_a / 2), math.exp(T**3 / 6), 6)
    approx("    e^{1/6}", math.exp(1 / 6), 1.1814, 4)
    n, paths = 400, 50_000
    dw = rng.standard_normal((paths, n)) * math.sqrt(T / n)
    wp = np.concatenate([np.zeros((paths, 1)), np.cumsum(dw, axis=1)], axis=1)
    a = (0.5 * (wp[:, 1:] + wp[:, :-1]) * (T / n)).sum(axis=1)
    m, se = mean_se(np.exp(a))
    simulated("E[exp(int_0^1 W dt)], simulated", m, se, math.exp(1 / 6))
    m, se = mean_se(a * wp[:, -1])
    simulated("Cov(W_1, int_0^1 W dt), simulated, vs T^2/2", m, se, 0.5)
    x = np.linspace(-40.0, 40.0, 4_000_001)
    for tq in (0.2, 0.45):
        y = np.exp(x * x * (1 - 1 / (2 * tq))) / math.sqrt(2 * math.pi * tq)  # e^{x^2} times the N(0, t) density
        approx(
            f"E[e^(W_t^2)] at t = {tq} by quadrature vs 1/sqrt(1 - 2t)",
            float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x))),
            1 / math.sqrt(1 - 2 * tq),
            6,
        )
    approx("    1/sqrt(0.6)", 1 / math.sqrt(0.6), 1.2910, 4)
    exact("exponent 1 - 1/(2t) at t = 1/2 (boundary: integrand no longer decays)", 1 - 1 / (2 * Fraction(1, 2)), 0)


def gbm_cards(rng: np.random.Generator) -> None:
    print("GBM cards (sc-ps-d-inverse-gbm, sc-ps-gbm-*)")
    s0, mu, sig, T = 50.0, 0.08, 0.35, 1.5
    lg = math.log(s0) + (mu - 0.5 * sig**2) * T + sig * math.sqrt(T) * GH_X
    st = np.exp(lg)
    approx("E[1/S_T] by quadrature vs (1/S0) e^{(sigma^2 - mu) T}", float(GH_W @ (1 / st)), math.exp((sig**2 - mu) * T) / s0, 12)
    for p in (-2.0, 0.5, 2.0):
        approx(
            f"E[S_T^{p}] by quadrature vs S0^p e^(p mu T + p(p-1) sigma^2 T/2)",
            float(GH_W @ st**p),
            s0**p * math.exp(p * mu * T + 0.5 * p * (p - 1) * sig**2 * T),
            8,
        )
    w = rng.standard_normal(2_000_000) * math.sqrt(T)
    s_t = s0 * np.exp((mu - 0.5 * sig**2) * T + sig * w)
    m, se = mean_se((s_t > s0).astype(float))
    simulated("P(S_T > S0), simulated, vs Phi((mu - sigma^2/2) sqrt(T)/sigma)", m, se, ncdf((mu - 0.5 * sig**2) * math.sqrt(T) / sig))
    mu_med = 0.5 * sig**2
    s_med = s0 * np.exp((mu_med - 0.5 * sig**2) * T + sig * w)
    approx("median of S_T with mu = sigma^2/2, simulated, relative to S0", float(np.median(s_med)) / s0, 1.0, 2)
    approx(
        "    and its mean e^{sigma^2 T/2} by quadrature", float(GH_W @ np.exp(sig * math.sqrt(T) * GH_X)), math.exp(0.5 * sig**2 * T), 12
    )
    g = np.linspace(0, T, 300_001)
    y = s0 * np.exp(mu * g)
    approx(
        "E[(1/T) int S dt] by quadrature vs S0 (e^{mu T} - 1)/(mu T)",
        float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(g))) / T,
        s0 * (math.exp(mu * T) - 1) / (mu * T),
        8,
    )
    approx("ever double with mu = 0: 2^(2 mu/sigma^2 - 1)", 2 ** (-1.0), 0.5, 12)


def main() -> None:
    rng = np.random.default_rng(SEED)
    moments()
    int_w2_dw(rng)
    max_end_below(rng)
    barriers()
    ou_ar1(rng)
    martingales()
    gaussian_cards(rng)
    gbm_cards(rng)
    print("all problem-set checks passed")


if __name__ == "__main__":
    main()
