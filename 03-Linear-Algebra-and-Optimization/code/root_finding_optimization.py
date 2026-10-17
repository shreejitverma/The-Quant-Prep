"""Root finding, implied volatility, descent methods and Levenberg-Marquardt: every number quoted in note 10.

Run: uv run --no-project --with numpy python 03-Linear-Algebra-and-Optimization/code/root_finding_optimization.py
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np


def check(label: str, value: float, expected: float, tol: float = 5e-4) -> float:
    """Print a labelled number and assert it matches the value quoted in the notes."""
    v = float(value) + 0.0
    print(f"{label} = {int(v) if v.is_integer() and abs(v) < 1e15 else format(v, '.10g')}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


Fn = Callable[[float], float]


# ---------------------------------------------------------------------------
# Scalar root finders
# ---------------------------------------------------------------------------


def bisection(f: Fn, a: float, b: float, tol: float) -> tuple[float, int]:
    fa = f(a)
    assert fa * f(b) < 0, "bisection needs a sign change"
    it = 0
    while b - a > tol:
        it += 1
        m = 0.5 * (a + b)
        fm = f(m)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return 0.5 * (a + b), it


def newton(f: Fn, df: Fn, x: float, tol: float, max_iter: int = 100) -> tuple[float, int, list[float]]:
    path = [x]
    for it in range(1, max_iter + 1):
        step = f(x) / df(x)
        x -= step
        path.append(x)
        if abs(step) < tol:
            return x, it, path
    raise RuntimeError("Newton did not converge")


def secant(f: Fn, x0: float, x1: float, tol: float, max_iter: int = 100) -> tuple[float, int]:
    f0, f1 = f(x0), f(x1)
    for it in range(1, max_iter + 1):
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(x2 - x1) < tol:
            return x2, it
        x0, f0, x1, f1 = x1, f1, x2, f(x2)
    raise RuntimeError("secant did not converge")


def brent(f: Fn, a: float, b: float, tol: float, max_iter: int = 200) -> tuple[float, int]:
    """Brent (1973) zero finder: inverse quadratic interpolation or secant, falling back to bisection."""
    fa, fb = f(a), f(b)
    assert fa * fb < 0, "Brent needs a sign change"
    if abs(fa) < abs(fb):
        a, b, fa, fb = b, a, fb, fa
    c, fc = a, fa
    d = e = b - a
    for it in range(1, max_iter + 1):
        if fb == 0:
            return b, it
        if fa * fb > 0:  # keep the root bracketed between a and b
            a, fa = c, fc
            d = e = b - c
        if abs(fa) < abs(fb):
            c, fc = b, fb
            b, fb = a, fa
            a, fa = c, fc
        tol1 = 2 * np.finfo(float).eps * abs(b) + 0.5 * tol
        xm = 0.5 * (a - b)
        if abs(xm) <= tol1:
            return b, it
        if abs(e) >= tol1 and abs(fc) > abs(fb):
            s = fb / fc
            if a == c:  # secant
                p, q = 2 * xm * s, 1 - s
            else:  # inverse quadratic interpolation
                q, r = fc / fa, fb / fa
                p = s * (2 * xm * q * (q - r) - (b - c) * (r - 1))
                q = (q - 1) * (r - 1) * (s - 1)
            if p > 0:
                q = -q
            p = abs(p)
            if 2 * p < min(3 * xm * q - abs(tol1 * q), abs(e * q)):
                e, d = d, p / q
            else:
                d = e = xm
        else:
            d = e = xm
        c, fc = b, fb
        b += d if abs(d) > tol1 else math.copysign(tol1, xm)
        fb = f(b)
    raise RuntimeError("Brent did not converge")


ROOT = 2.0945514815423265  # real root of x^3 - 2x - 5 (Wallis's example)


def scalar_roots() -> None:
    print("\n[10] x^3 - 2x - 5 = 0 on [2, 3]")

    def f(x: float) -> float:
        return x**3 - 2 * x - 5

    def df(x: float) -> float:
        return 3 * x**2 - 2

    x_b, it_b = bisection(f, 2.0, 3.0, 1e-12)
    check("bisection root", x_b, ROOT, 1e-12)
    check("bisection iterations to width 1e-12", it_b, 40, 0)
    check("ceil(log2(width / tol)) for [2, 3] to 1e-12", math.ceil(math.log2((3.0 - 2.0) / 1e-12)), 40, 0)
    x_n, it_n, path = newton(f, df, 2.0, 1e-14)
    check("Newton root", x_n, ROOT, 1e-15)
    check("Newton iterations from x0 = 2", it_n, 5, 0)
    errs = [abs(x - ROOT) for x in path[:4]]
    for k, (e, want) in enumerate(zip(errs, (9.455e-2, 5.449e-3, 1.664e-5, 1.559e-10), strict=True)):
        check(f"Newton error after {k} steps", e, want, want * 1e-3)
    check("e_2 / e_1^2 (tends to f''(r)/(2f'(r)))", errs[2] / errs[1] ** 2, 0.5605, 1e-4)
    check("f''(r) / (2 f'(r))", 6 * ROOT / (2 * (3 * ROOT**2 - 2)), 0.5630, 1e-4)
    x_s, it_s = secant(f, 2.0, 3.0, 1e-14)
    check("secant root", x_s, ROOT, 1e-14)
    check("secant iterations", it_s, 7, 0)
    x_br, it_br = brent(f, 2.0, 3.0, 1e-14)
    check("Brent root", x_br, ROOT, 1e-13)
    check("Brent iterations", it_br, 7, 0)
    check("golden ratio (secant order)", (1 + math.sqrt(5)) / 2, 1.618034, 1e-6)

    def g(x: float) -> float:
        return (x - 1.0) ** 2

    def dg(x: float) -> float:
        return 2 * (x - 1.0)

    x = 0.0
    cycle = []
    for _ in range(4):
        x -= (x**3 - 2 * x + 2) / (3 * x**2 - 2)
        cycle.append(x)
    check("x^3 - 2x + 2 from 0: iterate 1", cycle[0], 1.0, 1e-15)
    check("x^3 - 2x + 2 from 0: iterate 2", cycle[1], 0.0, 1e-15)
    check("x^3 - 2x + 2 from 0: iterate 4", cycle[3], 0.0, 1e-15)

    _, it_double, path = newton(g, dg, 2.0, 1e-10)
    check("Newton on a double root: error ratio", (path[3] - 1) / (path[2] - 1), 0.5, 1e-12)
    check("Newton on a double root: iterations to 1e-10 step", it_double, 34, 0)


# ---------------------------------------------------------------------------
# Implied volatility
# ---------------------------------------------------------------------------


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call(s: float, k: float, t: float, r: float, vol: float) -> float:
    sq = vol * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / sq
    return s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d1 - sq)


def bs_vega(s: float, k: float, t: float, r: float, vol: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
    return s * math.sqrt(t) * math.exp(-0.5 * d1 * d1) / math.sqrt(2 * math.pi)


def implied_vol_newton(
    price: float, s: float, k: float, t: float, r: float, vol0: float, tol: float = 1e-12, max_iter: int = 50
) -> tuple[float, int, list[float]]:
    """Plain Newton on C(vol) - price; returns early (unconverged) when vega underflows or vol leaves (0, inf)."""
    vol, path = vol0, [vol0]
    for it in range(1, max_iter + 1):
        vega = bs_vega(s, k, t, r, vol)
        if vega == 0.0:
            return vol, it, path  # vega underflowed: Newton cannot continue
        step = (bs_call(s, k, t, r, vol) - price) / vega
        vol -= step
        path.append(vol)
        if not math.isfinite(vol) or vol <= 0:
            return vol, it, path  # the failure mode a safeguard must catch
        if abs(step) < tol:
            return vol, it, path
    return vol, max_iter, path


def implied_vol_safeguarded(
    price: float,
    s: float,
    k: float,
    t: float,
    r: float,
    tol: float = 1e-12,
    ftol: float = 1e-13,
    pricer: Callable[[float, float, float, float, float], float] | None = None,
) -> tuple[float, int]:
    """Newton inside a shrinking bracket [lo, hi]; any step that leaves the bracket becomes a bisection step.

    The starting bracket [1e-6, 5] is widened until C(lo) < price < C(hi), so it always contains the root.
    """
    call = pricer or bs_call
    intrinsic = max(s - k * math.exp(-r * t), 0.0)
    if not intrinsic < price < s:
        raise ValueError("price outside no-arbitrage bounds: no implied volatility exists")
    lo, hi = 1e-6, 5.0
    while call(s, k, t, r, hi) <= price:
        hi *= 2.0
    while call(s, k, t, r, lo) >= price:
        lo *= 0.5
    vol = math.sqrt(2 * abs(math.log(s / k) + r * t) / t)  # Manaster-Koehler seed
    vol = min(max(vol, lo), hi)
    for it in range(1, 200):
        diff = call(s, k, t, r, vol) - price
        # Stop on the price residual first: at the root, diff is pure rounding noise whose sign and size
        # differ across libm builds, and acting on it would trigger spurious bisection steps.
        if abs(diff) <= ftol:
            return vol, it
        if diff > 0:
            hi = vol
        else:
            lo = vol
        vega = bs_vega(s, k, t, r, vol)
        cand = vol - diff / vega if vega > 0 else math.nan
        new = cand if lo < cand < hi else 0.5 * (lo + hi)
        if abs(new - vol) < tol:
            return new, it
        vol = new
    raise RuntimeError("safeguarded Newton did not converge")


def implied_vol_examples() -> None:
    print("\n[10] implied volatility: S = 100, K = 110, T = 0.5, r = 3%, true vol 25%")
    s, k, t, r, true_vol = 100.0, 110.0, 0.5, 0.03, 0.25
    price = bs_call(s, k, t, r, true_vol)
    check("call price", price, 3.8986, 1e-4)
    seed = math.sqrt(2 * abs(math.log(s / k) + r * t) / t)
    check("Manaster-Koehler seed sqrt(2|ln(S/K) + rT|/T)", seed, 0.5668, 1e-4)
    d1 = (math.log(s / k) + (r + 0.5 * seed**2) * t) / (seed * math.sqrt(t))
    d2 = d1 - seed * math.sqrt(t)
    check("d1 d2 at the seed (volga = vega d1 d2 / vol = 0: vega is maximal)", d1 * d2, 0.0, 1e-12)
    h = 1e-5
    check(
        "vega slope at the seed by finite difference",
        (bs_vega(s, k, t, r, seed + h) - bs_vega(s, k, t, r, seed - h)) / (2 * h),
        0.0,
        1e-6,
    )
    vol, it, path = implied_vol_newton(price, s, k, t, r, seed)
    check("Newton implied vol", vol, true_vol, 1e-12)
    check("Newton iterations from the seed", it, 5, 0)
    for j, want in enumerate((0.3168, 0.0051, 0.0000098)):
        check(f"Newton vol error after {j} steps", path[j] - true_vol, want, 5e-5 if j < 2 else 1e-7)
    for j, want in enumerate((0.5668, 0.2551, 0.2500, 0.2500)):
        check(f"Newton path step {j}", path[j], want, 1e-4)
    vol_b, it_b = bisection(lambda v: bs_call(s, k, t, r, v) - price, 0.01, 3.0, 1e-10)
    check("bisection implied vol", vol_b, true_vol, 1e-10)
    check("bisection iterations on [0.01, 3] to 1e-10", it_b, 35, 0)
    vol_s, it_s = implied_vol_safeguarded(price, s, k, t, r)
    check("safeguarded implied vol", vol_s, true_vol, 1e-12)
    check("safeguarded iterations", it_s, 5, 0)
    # Different libm builds round erf and exp differently in the last bits. Perturb every price by up to
    # 4 ulps (seeded) and require the same iteration count: the residual stop makes the count reproducible.
    counts = set()
    for seed_ in range(200):
        rng = np.random.default_rng(seed_)

        def noisy(s_: float, k_: float, t_: float, r_: float, v_: float, _rng=rng) -> float:
            p_ = bs_call(s_, k_, t_, r_, v_)
            return p_ + float(_rng.integers(-4, 5)) * math.ulp(p_)

        counts.add(implied_vol_safeguarded(price, s, k, t, r, pricer=noisy)[1])
    check("distinct safeguarded iteration counts under 4-ulp price noise (200 seeds)", len(counts), 1, 0)
    check("that iteration count", counts.pop(), 5, 0)
    big_price = bs_call(100.0, 100.0, 1.0, 0.0, 6.0)
    check("S = K = 100, T = 1, r = 0, vol 600%: call price", big_price, 99.73, 5e-3)
    vol_big, _ = implied_vol_safeguarded(big_price, 100.0, 100.0, 1.0, 0.0)
    check("safeguarded implied vol above the initial cap of 5 (bracket widened)", vol_big, 6.0, 1e-9)

    print("\n[10] Newton failure: S = 100, K = 150, T = 0.25, r = 0, true vol 30%, start at 10%")
    s, k, t, r, true_vol = 100.0, 150.0, 0.25, 0.0, 0.30
    price = bs_call(s, k, t, r, true_vol)
    check("deep OTM call price", price, 0.019233, 1e-6)
    check("vega at 10%", bs_vega(s, k, t, r, 0.10), 1.282e-13, 1e-16)
    vol_bad, _, path = implied_vol_newton(price, s, k, t, r, 0.10)
    check("first Newton step lands at", path[1], 1.4998e11, 1e7)
    vol_s, it_s = implied_vol_safeguarded(price, s, k, t, r)
    check("deep OTM: safeguarded implied vol", vol_s, true_vol, 1e-11)
    check("deep OTM: safeguarded iterations", it_s, 10, 0)
    vega_true = bs_vega(s, k, t, r, true_vol)
    check("vega at the solution", vega_true, 0.63105, 1e-5)
    check("vol error from a 1e-8 price error = 1e-8 / vega", 1e-8 / vega_true, 1.585e-8, 1e-11)

    print("\n[10] Brenner-Subrahmanyam ATM approximation: S = K = 100, T = 0.5, r = 0, vol 20%")
    c = bs_call(100.0, 100.0, 0.5, 0.0, 0.20)
    check("ATM call price", c, 5.6372, 1e-4)
    check("sqrt(2 pi / T) C / S", math.sqrt(2 * math.pi / 0.5) * c / 100, 0.19983, 1e-5)
    check("card: sqrt(4 pi) x C/S rounded to 0.0564", math.sqrt(4 * math.pi) * round(c / 100, 4), 0.19993, 1e-5)
    check("1 / sqrt(2 pi)", 1 / math.sqrt(2 * math.pi), 0.3989, 1e-4)


# ---------------------------------------------------------------------------
# Descent methods
# ---------------------------------------------------------------------------


def quadratic_rates() -> None:
    print("\n[10] f(x) = 1/2 x'Ax with A = diag(1, 100): iterations to |x| < 1e-8 from (1, 1)")
    a = np.diag([1.0, 100.0])
    mu_, big_l = 1.0, 100.0
    kappa = big_l / mu_
    check("gradient descent contraction (k - 1)/(k + 1)", (kappa - 1) / (kappa + 1), 0.980198, 1e-6)
    check("heavy-ball contraction (sqrt k - 1)/(sqrt k + 1)", (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1), 0.818182, 1e-6)
    x = np.ones(2)
    step = 2 / (big_l + mu_)
    it_gd = 0
    while np.linalg.norm(x) >= 1e-8:
        x = x - step * (a @ x)
        it_gd += 1
    check("gradient descent iterations", it_gd, 939, 0)
    alpha = 4 / (math.sqrt(big_l) + math.sqrt(mu_)) ** 2
    beta = ((math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)) ** 2
    x_prev, x, it_hb = np.ones(2), np.ones(2), 0
    while np.linalg.norm(x) >= 1e-8:
        x, x_prev = x - alpha * (a @ x) + beta * (x - x_prev), x
        it_hb += 1
    check("heavy-ball (Polyak) iterations", it_hb, 119, 0)
    rate = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
    check("contraction-only estimate log(sqrt(2)/1e-8)/log(1/rate)", math.log(math.sqrt(2) / 1e-8) / math.log(1 / rate), 93.5, 0.1)
    x = np.ones(2) - np.linalg.solve(a, a @ np.ones(2))
    check("Newton: |x| after one step", np.linalg.norm(x), 0.0, 1e-15)


def rosenbrock(x: np.ndarray) -> float:
    return float(100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2)


def rosenbrock_grad(x: np.ndarray) -> np.ndarray:
    return np.array([-400 * x[0] * (x[1] - x[0] ** 2) - 2 * (1 - x[0]), 200 * (x[1] - x[0] ** 2)])


def rosenbrock_hess(x: np.ndarray) -> np.ndarray:
    return np.array([[1200 * x[0] ** 2 - 400 * x[1] + 2, -400 * x[0]], [-400 * x[0], 200.0]])


def backtrack(x: np.ndarray, p: np.ndarray, g: np.ndarray) -> float:
    t, fx = 1.0, rosenbrock(x)
    slope = float(g[0] * p[0] + g[1] * p[1])
    while rosenbrock(x + t * p) > fx + 1e-4 * t * slope:
        t *= 0.5
    return t


def descent(method: str, x0: np.ndarray, gtol: float = 1e-8, max_iter: int = 100_000) -> tuple[np.ndarray, int]:
    x = x0.copy()
    h_inv = np.eye(2)
    g = rosenbrock_grad(x)
    for it in range(1, max_iter + 1):
        if method == "gd":
            p = -g
        elif method == "newton":
            hess = rosenbrock_hess(x)
            p = -np.linalg.solve(hess, g)
            if g @ p >= 0:  # not a descent direction: fall back to steepest descent
                p = -g
        else:
            p = -h_inv @ g
        t = backtrack(x, p, g)
        x_new = x + t * p
        g_new = rosenbrock_grad(x_new)
        if method == "bfgs":
            s_vec, y_vec = x_new - x, g_new - g
            sy = s_vec @ y_vec
            if sy > 1e-12:  # curvature condition; skip the update otherwise
                rho = 1.0 / sy
                eye = np.eye(2)
                h_inv = (eye - rho * np.outer(s_vec, y_vec)) @ h_inv @ (eye - rho * np.outer(y_vec, s_vec)) + rho * np.outer(s_vec, s_vec)
        x, g = x_new, g_new
        if np.linalg.norm(g) < gtol:
            return x, it
    return x, max_iter


def rosenbrock_comparison() -> None:
    print("\n[10] Rosenbrock from (-1.2, 1), Armijo backtracking, stop at |grad| < 1e-8")
    x0 = np.array([-1.2, 1.0])
    for method, want in (("gd", 19_435), ("newton", 21), ("bfgs", 35)):
        x, it = descent(method, x0)
        print(f"{method}: iterations {it}, x = ({x[0]:.10f}, {x[1]:.10f})")
        check(f"{method} iterations", it, want, 0)
        check(f"{method} distance to (1, 1)", np.linalg.norm(x - 1.0), 0.0, 1e-6)


# ---------------------------------------------------------------------------
# Levenberg-Marquardt: Nelson-Siegel calibration
# ---------------------------------------------------------------------------

NS_TENORS = np.array([0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30], dtype=float)


def nelson_siegel(p: np.ndarray, t: np.ndarray = NS_TENORS) -> np.ndarray:
    b0, b1, b2, tau = p
    x = t / tau
    f1 = (1 - np.exp(-x)) / x
    return b0 + b1 * f1 + b2 * (f1 - np.exp(-x))


def ns_jacobian(p: np.ndarray, h: float = 1e-7) -> np.ndarray:
    base = nelson_siegel(p)
    jac = np.zeros((len(NS_TENORS), 4))
    for j in range(4):
        dp = np.zeros(4)
        dp[j] = h * max(1.0, abs(p[j]))
        jac[:, j] = (nelson_siegel(p + dp) - base) / dp[j]
    return jac


def levenberg_marquardt(y: np.ndarray, p0: np.ndarray, lam: float = 1e-3, tol: float = 1e-8) -> tuple[np.ndarray, int, bool]:
    """Marquardt-scaled LM: (J'J + lam diag(J'J)) step = -J'r. Returns (params, iterations, converged)."""
    p = p0.copy()
    r = nelson_siegel(p) - y
    for it in range(1, 1000):
        jac = ns_jacobian(p)
        jtj = jac.T @ jac
        step = np.linalg.solve(jtj + lam * np.diag(np.diag(jtj)), -jac.T @ r)
        p_try = p + step
        r_try = nelson_siegel(p_try) - y
        if r_try @ r_try < r @ r:
            p, r = p_try, r_try
            lam = max(lam / 10, 1e-12)
            if np.abs(step).max() < tol * (1 + np.abs(p).max()):
                return p, it, True
        else:
            lam *= 10
            if lam > 1e12:  # no downhill step at any damping: a (local) minimum to machine precision
                return p, it, True
    return p, 1000, False


def ns_profile_tau(y: np.ndarray, taus: np.ndarray) -> tuple[float, np.ndarray]:
    """For each tau the model is linear in the betas: solve OLS and keep the tau with the smallest residual."""
    best = (math.inf, 0.0, np.zeros(3))
    for tau in taus:
        x = NS_TENORS / tau
        f1 = (1 - np.exp(-x)) / x
        design = np.column_stack([np.ones_like(x), f1, f1 - np.exp(-x)])
        beta, *_ = np.linalg.lstsq(design, y, rcond=None)
        sse = float(np.sum((design @ beta - y) ** 2))
        if sse < best[0]:
            best = (sse, float(tau), beta)
    return best[1], best[2]


def nelson_siegel_fit() -> None:
    print("\n[10] Levenberg-Marquardt fit of Nelson-Siegel (beta0 4%, beta1 -2%, beta2 1%, tau 2)")
    true = np.array([0.04, -0.02, 0.01, 2.0])
    y = nelson_siegel(true)
    check("model 3m yield", y[0], 0.021775, 1e-6)
    check("model 30y yield", y[-1], 0.039333, 1e-6)
    p, it, ok = levenberg_marquardt(y, np.array([0.035, -0.015, 0.005, 1.5]))
    assert ok
    for name, v, want in zip(("beta0", "beta1", "beta2", "tau"), p, true, strict=True):
        check(f"good start: fitted {name}", v, want, 1e-8)
    check("good start: LM iterations", it, 5, 0)
    p, it, ok = levenberg_marquardt(y, np.array([0.03, -0.01, 0.0, 1.0]))
    rmse_bp = math.sqrt(np.mean((nelson_siegel(p) - y) ** 2)) * 1e4
    check("poor start: stalls at tau", p[3], 0.8113, 1e-4)
    check("poor start: beta2", p[2], -0.009600, 1e-6)
    check("poor start: RMSE (bp) at the local minimum", rmse_bp, 0.746, 1e-3)
    grad = ns_jacobian(p).T @ (nelson_siegel(p) - y)
    check("poor start: |J'r| at the stall (stationary)", np.abs(grad).max(), 0.0, 1e-13)
    tau0, beta0 = ns_profile_tau(y, np.arange(0.25, 10.0001, 0.05))
    check("profile over tau: best grid tau", tau0, 2.0, 1e-9)
    p, it, ok = levenberg_marquardt(y, np.concatenate([beta0, [tau0]]))
    check("profile then LM: fitted tau", p[3], 2.0, 1e-8)
    rng = np.random.default_rng(8)
    y_noisy = y + rng.normal(0, 0.0001, len(y))  # 1bp noise
    p, _, _ = levenberg_marquardt(y_noisy, np.array([0.035, -0.015, 0.005, 1.5]))
    rmse_bp = math.sqrt(np.mean((nelson_siegel(p) - y_noisy) ** 2)) * 1e4
    check("1bp noise: fitted tau (seed 8)", p[3], 1.955, 1e-3)
    check("1bp noise: fitted beta2 (seed 8)", p[2], 0.00906, 1e-5)
    check("1bp noise: RMSE (bp)", rmse_bp, 0.596, 1e-3)


def main() -> None:
    scalar_roots()
    implied_vol_examples()
    quadratic_rates()
    rosenbrock_comparison()
    nelson_siegel_fit()
    print("\nall root_finding_optimization checks passed")


if __name__ == "__main__":
    main()
