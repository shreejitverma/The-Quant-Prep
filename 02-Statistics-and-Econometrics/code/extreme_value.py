"""Heavy tails and extreme value theory on Student-t data with a known tail index.

Backs every number in ``13-Heavy-Tails-and-Extreme-Value-Theory.md``.
Run ``uv run --no-project --with numpy python 02-Statistics-and-Econometrics/code/extreme_value.py``;
each printed number is asserted, so drift in the note fails CI.
Simulations use fixed seeds; prose quotes their results as "about" and their tables carry a caption naming the seed.

Student-t with nu = 4 has tail index alpha = 4, so its GPD/GEV shape is xi = 1/4.
Its CDF has the closed form F(t) = 1/2 + (3/4) s (1 - s^2/3) with s = t / sqrt(4 + t^2).
"""

from __future__ import annotations

import math
from collections.abc import Callable
from statistics import NormalDist

import numpy as np

PHI = NormalDist()
NU = 4


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<66s} {value:12.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


# ---------------------------------------------------------------- Student-t(4) exact results


def t4_cdf(t: float) -> float:
    s = t / math.sqrt(4.0 + t * t)
    return 0.5 + 0.75 * s * (1.0 - s * s / 3.0)


def t4_pdf(t: float) -> float:
    return 0.375 * (1.0 + t * t / 4.0) ** -2.5


def t4_quantile(q: float) -> float:
    lo, hi = -1e6, 1e6
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t4_cdf(mid) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def t_es_closed_form(q: float, nu: int = NU) -> float:
    """ES of the loss -X at level q for Student-t: f(t_q)/(1-q) * (nu + t_q^2)/(nu - 1)."""
    tq = t4_quantile(q)
    return t4_pdf(tq) / (1 - q) * (nu + tq * tq) / (nu - 1)


def t4_es_numeric(q: float) -> float:
    """Independent check: (1/(1-q)) int_q^1 F^{-1}(u) du via the substitution u = F(t)."""
    tq = t4_quantile(q)
    # integral of t f(t) dt from tq to infinity, with t = tq / w, w in (0, 1]
    w = np.linspace(1e-7, 1.0, 2_000_001)
    t = tq / w
    integrand = t * 0.375 * (1.0 + t * t / 4.0) ** -2.5 * tq / w**2
    return float(np.trapezoid(integrand, w)) / (1 - q)


def student_t_draws(rng: np.random.Generator, size: int, nu: int = NU) -> np.ndarray:
    """Z / sqrt(chi2_nu / nu), the chi-square built from nu squared normals (integer nu)."""
    z = rng.standard_normal(size)
    chi2 = np.zeros(size)
    for _ in range(nu):
        chi2 += rng.standard_normal(size) ** 2
    return z / np.sqrt(chi2 / nu)


# ---------------------------------------------------------------- estimators


def hill(losses: np.ndarray, k: int) -> float:
    """Hill estimator of the tail index alpha from the k largest losses (threshold X_(k+1))."""
    s = np.sort(losses)[::-1]
    return 1.0 / float(np.mean(np.log(s[:k]) - math.log(s[k])))


def gpd_fit(excess: np.ndarray) -> tuple[float, float, float]:
    """GPD MLE by Grimshaw's profile likelihood in theta = xi/sigma; returns (xi, sigma, loglik)."""
    k = excess.size
    ymax = float(excess.max())

    def profile(theta: float) -> float:
        xi = float(np.mean(np.log1p(theta * excess)))
        return -k * math.log(xi / theta) - k * (1.0 + xi)

    lo_neg = -1.0 / ymax * (1 - 1e-9)
    grid = np.concatenate([np.linspace(lo_neg, -1e-8, 400), np.exp(np.linspace(math.log(1e-6 / ymax), math.log(1e3 / ymax), 4000))])
    vals = np.array([profile(th) for th in grid])
    i = int(np.argmax(vals))
    a, b = grid[max(i - 1, 0)], grid[min(i + 1, grid.size - 1)]
    g = (math.sqrt(5) - 1) / 2
    for _ in range(200):
        c, d = b - g * (b - a), a + g * (b - a)
        if profile(c) > profile(d):
            b = d
        else:
            a = c
    theta = 0.5 * (a + b)
    xi = float(np.mean(np.log1p(theta * excess)))
    return xi, xi / theta, profile(theta)


def gpd_loglik(xi: float, sigma: float, excess: np.ndarray) -> float:
    z = 1.0 + xi * excess / sigma
    if sigma <= 0 or np.any(z <= 0):
        return -math.inf
    return -excess.size * math.log(sigma) - (1.0 + 1.0 / xi) * float(np.sum(np.log(z)))


def pot_var_es(u: float, xi: float, sigma: float, n: int, n_u: int, q: float) -> tuple[float, float]:
    """McNeil and Frey (2000): tail estimator VaR and ES from a GPD fitted above u (requires xi < 1)."""
    var = u + sigma / xi * (((n / n_u) * (1 - q)) ** (-xi) - 1.0)
    es = var / (1 - xi) + (sigma - xi * u) / (1 - xi)
    return var, es


def nelder_mead(f: Callable[[np.ndarray], float], x0: np.ndarray, step: np.ndarray, iters: int = 4000) -> np.ndarray:
    """Minimise f with the standard Nelder-Mead simplex (reflection 1, expansion 2, contraction 0.5, shrink 0.5)."""
    pts = [x0] + [x0 + np.eye(x0.size)[i] * step[i] for i in range(x0.size)]
    vals = [f(p) for p in pts]
    for _ in range(iters):
        order = np.argsort(vals)
        pts, vals = [pts[i] for i in order], [vals[i] for i in order]
        if abs(vals[-1] - vals[0]) < 1e-12:
            break
        centroid = np.mean(pts[:-1], axis=0)
        xr = centroid + (centroid - pts[-1])
        fr = f(xr)
        if fr < vals[0]:
            xe = centroid + 2.0 * (centroid - pts[-1])
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
                pts = [pts[0]] + [pts[0] + 0.5 * (p - pts[0]) for p in pts[1:]]
                vals = [vals[0]] + [f(p) for p in pts[1:]]
    return pts[int(np.argmin(vals))]


def gev_negloglik(params: np.ndarray, x: np.ndarray) -> float:
    mu, log_sigma, xi = params
    sigma = math.exp(log_sigma)
    z = (x - mu) / sigma
    if abs(xi) < 1e-8:
        return float(x.size * log_sigma + np.sum(z) + np.sum(np.exp(-z)))
    w = 1.0 + xi * z
    if np.any(w <= 0):
        return math.inf
    return float(x.size * log_sigma + (1.0 + 1.0 / xi) * np.sum(np.log(w)) + np.sum(w ** (-1.0 / xi)))


def gev_fit(x: np.ndarray) -> np.ndarray:
    s0 = math.sqrt(6.0) * float(x.std()) / math.pi
    x0 = np.array([float(x.mean()) - 0.5772 * s0, math.log(s0), 0.1])
    return nelder_mead(lambda p: gev_negloglik(p, x), x0, np.array([0.1 * s0, 0.1, 0.05]))


def gev_return_level(mu: float, sigma: float, xi: float, p: float) -> float:
    """Level exceeded by a block maximum with probability p."""
    return mu + sigma / xi * ((-math.log(1.0 - p)) ** (-xi) - 1.0)


# ---------------------------------------------------------------- sections


def t4_reference() -> None:
    print("\n# 1. Student-t(4) and normal reference values (exact)")
    print("#    backs: Worked example 1; cards stat-evt-normal-vs-t-var, stat-evt-five-sigma")
    check("t4 density at 0, Gamma(5/2)/(sqrt(4 pi) Gamma(2))", math.gamma(2.5) / (math.sqrt(4 * math.pi) * math.gamma(2)), 0.375, 1e-12)
    rows = {0.99: (3.7469, 5.2206), 0.999: (7.1732, 9.6862), 0.9999: (13.0337, 17.4461)}
    for q, (v, e) in rows.items():
        check(f"t4 VaR {q}", t4_quantile(q), v, 1e-4)
        check(f"t4 ES {q} (closed form)", t_es_closed_form(q), e, 1e-4)
        check(f"t4 ES {q} (numerical integral)", t4_es_numeric(q), e, 1e-3)
    sd = math.sqrt(NU / (NU - 2))
    check("t4 standard deviation sqrt(nu/(nu-2))", sd, 1.4142, 1e-4)
    check("unit-variance t4 99% VaR", t4_quantile(0.99) / sd, 2.6495, 1e-4)
    check("unit-variance t4 99% ES", t_es_closed_form(0.99) / sd, 3.6915, 1e-4)
    check("normal 99% VaR", PHI.inv_cdf(0.99), 2.3263, 1e-4)
    check("normal 99% ES phi(z)/(1-q)", PHI.pdf(PHI.inv_cdf(0.99)) / 0.01, 2.6652, 1e-4)
    check("unit-variance t4 99.9% VaR", t4_quantile(0.999) / sd, 5.0722, 1e-4)
    check("normal 99.9% VaR", PHI.inv_cdf(0.999), 3.0902, 1e-4)
    check("unit-variance t4 97.5% VaR (crosses the normal)", t4_quantile(0.975) / sd, 1.9632, 1e-4)
    check("normal 97.5% VaR", PHI.inv_cdf(0.975), 1.9600, 1e-4)
    check("unit-variance t4 95% VaR (below the normal)", t4_quantile(0.95) / sd, 1.5074, 1e-4)
    check("normal 95% VaR", PHI.inv_cdf(0.95), 1.6449, 1e-4)
    # exceedance probability of a 5-sd move under each model
    p_t = check("P(unit-variance t4 < -5) x 1e3", t4_cdf(-5 * sd) * 1e3, 1.0553, 1e-4) / 1e3
    p_n = check("P(N(0,1) < -5) x 1e7", PHI.cdf(-5) * 1e7, 2.8665, 1e-4) / 1e7
    check("one in how many days, t4", 1 / p_t, 948.0, 0.5)
    check("one in how many days, normal, in millions", 1 / p_n / 1e6, 3.4885, 1e-4)


def hill_and_kurtosis() -> None:
    print("\n# 2. Hill estimator and the instability of sample kurtosis (t4, n = 100,000, seed 13)")
    print("#    backs: Worked example 2; cards stat-evt-t4-kurtosis, stat-evt-hill-formula, stat-evt-hill-k-tradeoff")
    rng = np.random.default_rng(13)
    x = student_t_draws(rng, 100_000)
    losses = -x
    pos = losses[losses > 0]
    expected = {200: 3.58, 500: 3.41, 1000: 3.38, 2000: 3.24, 5000: 2.83}
    for k, a in expected.items():
        check(f"Hill alpha, k = {k} (true 4; se ~ alpha/sqrt(k))", hill(pos, k), a, 0.005)
    check("Hill standard error at k = 200, 4/sqrt(200)", 4 / math.sqrt(200), 0.2828, 1e-4)
    kurt = []
    for block in x.reshape(10, 10_000):
        c = block - block.mean()
        kurt.append(float(np.mean(c**4) / np.mean(c**2) ** 2))
    check("sample kurtosis over 10 blocks of 10,000: min", min(kurt), 7.4, 0.05)
    check("sample kurtosis over 10 blocks of 10,000: max", max(kurt), 216.3, 0.05)


def pot_section() -> None:
    print("\n# 3. Peaks over threshold: GPD by MLE, McNeil-Frey VaR and ES (t4, n = 100,000, seed 13)")
    print("#    backs: Worked example 3; cards stat-evt-gpd-xi-student-t, stat-evt-empirical-quantile-limits, stat-evt-normal-vs-sample-sd")
    rng = np.random.default_rng(13)
    x = student_t_draws(rng, 100_000)
    losses = -x
    n = losses.size
    u = float(np.quantile(losses, 0.98))
    excess = losses[losses > u] - u
    n_u = excess.size
    xi, sigma, ll = gpd_fit(excess)
    check("threshold u = empirical 98% quantile", u, 3.019, 0.0005)
    check("true t4 98% quantile", t4_quantile(0.98), 2.9985, 1e-4)
    check("exceedances N_u", n_u, 2000, 0)
    check("observations beyond the 99.99% quantile, n (1 - q)", float(np.sum(losses > np.quantile(losses, 0.9999))), 10, 0)
    check("GPD xi (true 0.25)", xi, 0.244, 0.0005)
    check("GPD sigma", sigma, 0.991, 0.0005)
    check("sigma / u", sigma / u, 0.328, 0.0005)
    check("asymptotic se of xi, (1 + xi)/sqrt(N_u)", (1 + xi) / math.sqrt(n_u), 0.028, 0.0005)
    # independent check that the profile maximum is the joint MLE: perturbations lower the likelihood
    assert abs(gpd_loglik(xi, sigma, excess) - ll) < 1e-6
    for dx, ds in ((1e-3, 0), (-1e-3, 0), (0, 1e-3), (0, -1e-3)):
        assert gpd_loglik(xi + dx, sigma + ds, excess) < ll
    me_emp = float(excess.mean())
    check("mean excess above u: empirical", me_emp, 1.321, 0.0005)
    check("mean excess above u: GPD sigma/(1-xi)", sigma / (1 - xi), 1.312, 0.0005)
    expected = {0.999: (7.40, 10.12, 7.46), 0.9999: (13.77, 18.56, 12.87)}
    for q, (v, e, emp) in expected.items():
        var, es = pot_var_es(u, xi, sigma, n, n_u, q)
        check(f"POT VaR {q} (true {t4_quantile(q):.4f})", var, v, 0.005)
        check(f"POT ES {q} (true {t_es_closed_form(q):.4f})", es, e, 0.005)
        check(f"empirical quantile {q}", float(np.quantile(losses, q)), emp, 0.005)
    s = float(losses.std())
    check("sample sd of the losses", s, 1.446, 0.0005)
    check("normal VaR 0.9999 with the sample sd", s * PHI.inv_cdf(0.9999), 5.38, 0.005)


def block_maxima() -> None:
    print("\n# 4. Block maxima: GEV by MLE on 2000 blocks of 250 (t4 and normal, seed 21)")
    print("#    backs: Worked example 4; cards stat-evt-return-level, stat-evt-normal-maxima-slow")
    rng = np.random.default_rng(21)
    m, nb = 250, 2000
    x = student_t_draws(rng, m * nb).reshape(nb, m)
    maxima = (-x).max(axis=1)
    mu, log_s, xi = gev_fit(maxima)
    sigma = math.exp(log_s)
    check("GEV xi, t4 maxima (true 0.25)", xi, 0.244, 0.0005)
    check("GEV mu", mu, 4.876, 0.0005)
    check("GEV sigma", sigma, 1.378, 0.0005)
    rl = gev_return_level(mu, sigma, xi, 0.1)
    true_rl = t4_quantile(0.9 ** (1.0 / m))
    check("1-in-10-block return level, GEV", rl, 9.006, 0.0005)
    check("1-in-10-block return level, exact F^{-1}(0.9^(1/250))", true_rl, 9.003, 0.0005)
    xn = rng.standard_normal((nb, m))
    _, _, xi_n = gev_fit(xn.max(axis=1))
    check("GEV xi, normal maxima (Gumbel limit 0; slow convergence)", xi_n, -0.10, 0.005)


def sharpe_section() -> None:
    print("\n# 5. Sharpe ratio standard error under fat tails (Mertens 2002)")
    print("#    backs: Core concepts (consequences), Worked example 5; card stat-evt-sharpe-fat-tails")

    # kurtosis of t5 by numerical integration of t^4 f(t) (closed form 3 (nu-2)/(nu-4) = 9)
    t = np.linspace(-4000.0, 4000.0, 8_000_001)
    f5 = math.gamma(3.0) / (math.sqrt(5 * math.pi) * math.gamma(2.5)) * (1 + t * t / 5) ** -3
    m2, m4 = float(np.trapezoid(t**2 * f5, t)), float(np.trapezoid(t**4 * f5, t))
    check("kurtosis of Student-t5", m4 / m2**2, 9.0, 0.01)

    def se_factor(sr: float, skew: float, kurt: float) -> float:
        return math.sqrt(1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr * sr)

    check("daily SR 0.1, normal (kurt 3)", se_factor(0.1, 0.0, 3.0), 1.0025, 1e-4)
    check("daily SR 0.1, t5 (kurt 9)", se_factor(0.1, 0.0, 9.0), 1.0100, 1e-4)
    check("monthly SR 0.3, normal", se_factor(0.3, 0.0, 3.0), 1.0223, 1e-4)
    check("monthly SR 0.3, kurt 9", se_factor(0.3, 0.0, 9.0), 1.0863, 1e-4)
    check("monthly SR 0.3, skew -1, kurt 9", se_factor(0.3, -1.0, 9.0), 1.2166, 1e-4)
    # simulation check: t5 monthly returns scaled to unit variance, true SR 0.3, T = 120, 20,000 paths
    rng = np.random.default_rng(5)
    reps, t = 20_000, 120
    r = 0.3 + student_t_draws(rng, reps * t, nu=5).reshape(reps, t) / math.sqrt(5.0 / 3.0)
    sr_hat = r.mean(1) / r.std(1, ddof=1)
    check("MC sd of SR_hat x sqrt(T), t5 (formula 1.0863)", float(sr_hat.std() * math.sqrt(t)), 1.07, 0.005)


if __name__ == "__main__":
    t4_reference()
    hill_and_kurtosis()
    pot_section()
    block_maxima()
    sharpe_section()
    print("\nall extreme_value checks passed")
