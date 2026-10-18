"""Drawdowns of a drifted Brownian motion: exact distribution, Magdon-Ismail asymptotics, Monte Carlo, limits.

Backs every number in 11-Risk-and-Trading/05-Drawdowns-and-Risk-Limits.md.

Model: log equity X_t = mu t + sigma W_t (arithmetic Brownian motion, X_0 = 0), running maximum M_t,
drawdown D_t = M_t - X_t (in log units), maximum drawdown MDD_T = max_{t <= T} D_t.

Exact method (independent of the published asymptotics): D is a Brownian motion with drift -mu reflected at 0.
P(MDD_T < h) is the probability that D, started at 0, has not reached h by T.  It solves the backward equation
    u_t = (sigma^2 / 2) u_xx - mu u_x  on (0, h),  u_x(0) = 0 (reflection),  u(h) = 0 (absorption),  u(0, x) = 1,
whose Sturm-Liouville eigenfunctions are phi(x) = exp(c x) psi(x), c = mu / sigma^2, with
    psi = cos(k x) - (c / k) sin(k x),  k h cos(k h) = c h sin(k h),  lambda = -(sigma^2 / 2) k^2 - mu^2 / (2 sigma^2),
plus, when c h > 1, one hyperbolic mode psi = cosh(kappa x) - (c / kappa) sinh(kappa x) with
    kappa h = c h tanh(kappa h),  lambda = (sigma^2 / 2) kappa^2 - mu^2 / (2 sigma^2).
The weight is exp(-2 c x), so the expansion coefficient of the constant 1 is int exp(-c x) psi / int psi^2.
E[MDD_T] = int_0^inf P(MDD_T >= h) dh is then a one-dimensional Gauss-Legendre integral.

This reproduces the closed form sqrt(pi/2) sigma sqrt(T) at mu = 0 and the large-T asymptotics of
Magdon-Ismail, Atiya, Pratap and Abu-Mostafa (2004), J. Appl. Prob. 41(1), 147-161, which this script checks.

Run: python 11-Risk-and-Trading/code/drawdowns.py
"""

from __future__ import annotations

import math

import numpy as np

EULER_GAMMA = 0.5772156649015329
MAGDON_QP_CONST = 0.49088  # large-x constant of Q_p quoted by Magdon-Ismail et al. (2004)
TRADING_DAYS = 252


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.6f}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


# ---------------------------------------------------------------------------
# Exact distribution of the maximum drawdown
# ---------------------------------------------------------------------------


def _bisect(f, lo: np.ndarray, hi: np.ndarray, iters: int = 64) -> np.ndarray:
    """Vectorised bisection; caller guarantees a sign change on each [lo, hi]."""
    flo = f(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        left = np.sign(fm) == np.sign(flo)
        lo = np.where(left, mid, lo)
        flo = np.where(left, fm, flo)
        hi = np.where(left, hi, mid)
    return 0.5 * (lo + hi)


def _hyperbolic_eps(a: float) -> float:
    """eps in (0, 1) with eps = 1 - tanh(a (1 - eps)), for a > 1 (the root u = a (1 - eps) of a tanh(u) = u)."""
    if a > 3.0:
        # Contraction with slope about 4 a exp(-2a) < 0.03: fixed-point iteration converges to full precision.
        eps = 0.0
        for _ in range(60):
            eps_new = 2.0 / (math.exp(2.0 * a * (1.0 - eps)) + 1.0)
            if eps_new == eps:
                break
            eps = eps_new
        return eps
    # Here eps >= 0.004, so solving for u by bisection and setting eps = 1 - u / a loses no precision.
    lo, hi = 1e-12, a
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if a * math.tanh(mid) - mid > 0.0 else (lo, mid)
    return 1.0 - 0.5 * (lo + hi) / a


def survival_mdd(h: float, t: float, mu: float, sigma: float) -> float:
    """P(MDD_T < h) for X_t = mu t + sigma W_t, by the eigenfunction expansion above."""
    if h <= 0.0:
        return 0.0
    c = mu / sigma**2
    a = c * h
    if abs(a - 1.0) < 1e-6:
        # c h = 1 is a removable degeneracy (the lowest mode is linear); S is smooth in h, so average its neighbours.
        return 0.5 * (survival_mdd(h * (1.0 - 3e-6), t, mu, sigma) + survival_mdd(h * (1.0 + 3e-6), t, mu, sigma))
    # Enough trig modes that exp(lambda_n T) < 1e-19 for the last one.
    n_modes = int(h / math.pi * math.sqrt(90.0 / (sigma**2 * t))) + 8
    lo = np.arange(n_modes, dtype=float) * math.pi
    hi = lo + math.pi
    lo[0] = 1e-9

    def g(th: np.ndarray) -> np.ndarray:
        return a * np.sin(th) - th * np.cos(th)

    valid = np.sign(g(lo)) != np.sign(g(hi))
    theta = _bisect(g, lo[valid], hi[valid])
    k = theta / h
    lam = -0.5 * sigma**2 * k**2 - mu**2 / (2.0 * sigma**2)
    # Coefficient of mode n, using k cos(kh) = c sin(kh) to simplify the closed-form integrals:
    #   int_0^h exp(-c x) psi dx = exp(-c h) sin(kh) / k
    #   int_0^h psi^2 dx = (1 + c^2/k^2) (h - c sin^2(kh) / k^2) / 2
    # The exponentials are combined in log space so that strongly negative drift cannot overflow.
    sin_t = np.sin(theta)
    den = (1.0 + c**2 / k**2) * (h - c * sin_t**2 / k**2) / 2.0
    total = float(np.sum(sin_t / (k * den) * np.exp(-c * h + lam * t)))
    if a > 1.0:
        # Hyperbolic mode: kappa = c (1 - eps), where eps in (0, 1) solves 1 - tanh(a (1 - eps)) = eps.
        # Working with eps keeps 1 - c^2/kappa^2 and lambda accurate when a is large and eps ~ 2 exp(-2a).
        eps = _hyperbolic_eps(a)
        u = a * (1.0 - eps)
        kap = c * (1.0 - eps)
        lam_h = -(mu**2 / (2.0 * sigma**2)) * eps * (2.0 - eps)
        # Same integrals with k -> i kappa, divided through by sinh^2(u) to stay finite for large u.
        q = math.exp(-2.0 * u)
        num_s = 2.0 * math.exp(-c * h - u) / (1.0 - q)  # exp(-c h) / sinh(u)
        one_minus = -eps * (2.0 - eps) / (1.0 - eps) ** 2  # 1 - c^2 / kappa^2
        den_s = one_minus * (4.0 * h * q / (1.0 - q) ** 2 - 1.0 / (c * (1.0 - eps) ** 2)) / 2.0
        total += num_s / (kap * den_s) * math.exp(lam_h * t)
    return min(max(total, 0.0), 1.0)


def _survival_by_quadrature(h: float, t: float, mu: float, sigma: float, n_modes: int = 60) -> float:
    """Slow reference for survival_mdd: the same eigenfunctions, coefficients by Gauss-Legendre (moderate inputs)."""
    c = mu / sigma**2
    a = c * h
    lo = np.arange(n_modes, dtype=float) * math.pi
    lo[0] = 1e-9
    hi = lo + math.pi

    def g(th: np.ndarray) -> np.ndarray:
        return a * np.sin(th) - th * np.cos(th)

    valid = np.sign(g(lo)) != np.sign(g(hi))
    ks = list(_bisect(g, lo[valid], hi[valid]) / h)
    nodes, weights = np.polynomial.legendre.leggauss(3000)
    x = 0.5 * h * (nodes + 1.0)
    w = 0.5 * h * weights
    total = 0.0
    for k in ks:
        psi = np.cos(k * x) - (c / k) * np.sin(k * x)
        lam = -0.5 * sigma**2 * k**2 - mu**2 / (2.0 * sigma**2)
        total += float(np.sum(w * np.exp(-c * x) * psi) / np.sum(w * psi**2)) * math.exp(lam * t)
    if a > 1.0:
        kap = _bisect(lambda z: a * np.tanh(z) - z, np.array([1e-9]), np.array([a]))[0] / h
        psi = np.cosh(kap * x) - (c / kap) * np.sinh(kap * x)
        lam = 0.5 * sigma**2 * kap**2 - mu**2 / (2.0 * sigma**2)
        total += float(np.sum(w * np.exp(-c * x) * psi) / np.sum(w * psi**2)) * math.exp(lam * t)
    return total


def _h_max(t: float, mu: float, sigma: float) -> float:
    """Upper integration limit beyond which P(MDD_T >= h) is negligible (below about 1e-20)."""
    h = max(-mu * t, 0.0) + 12.0 * sigma * math.sqrt(t)
    if mu > 0.0:
        x = mu**2 * t / (2.0 * sigma**2)
        h = min(h, sigma**2 / (2.0 * mu) * (math.log(max(x, 1.0)) + 50.0))
    return h


def _h_grid(t: float, mu: float, sigma: float, n: int = 120) -> tuple[np.ndarray, np.ndarray]:
    h_max = _h_max(t, mu, sigma)
    nodes, weights = np.polynomial.legendre.leggauss(n)
    return 0.5 * h_max * (nodes + 1.0), 0.5 * h_max * weights


def expected_mdd(t: float, mu: float, sigma: float) -> float:
    """E[MDD_T] in log units, exact (series plus quadrature)."""
    hs, ws = _h_grid(t, mu, sigma)
    return float(sum(w * (1.0 - survival_mdd(h, t, mu, sigma)) for h, w in zip(hs, ws, strict=True)))


def expected_pct_mdd(t: float, mu: float, sigma: float) -> float:
    """E[1 - exp(-MDD_T)]: the expected maximum percentage drawdown of equity exp(X_t)."""
    hs, ws = _h_grid(t, mu, sigma)
    return float(sum(w * math.exp(-h) * (1.0 - survival_mdd(h, t, mu, sigma)) for h, w in zip(hs, ws, strict=True)))


def prob_mdd_at_least(h: float, t: float, mu: float, sigma: float) -> float:
    return 1.0 - survival_mdd(h, t, mu, sigma)


def mdd_quantile(q: float, t: float, mu: float, sigma: float) -> float:
    """h such that P(MDD_T <= h) = q, by bisection on the exact distribution."""
    lo, hi = 1e-9, _h_max(t, mu, sigma)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if survival_mdd(mid, t, mu, sigma) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def magdon_q(x: float, positive: bool) -> float:
    """Q_p(x) (positive drift) or Q_n(x) (negative drift) of Magdon-Ismail et al., computed from the exact E[MDD].

    With sigma = 1 and |mu| = 1, x = mu^2 T / (2 sigma^2) = T / 2 and E[MDD] = 2 Q(x).
    """
    mu = 1.0 if positive else -1.0
    return expected_mdd(2.0 * x, mu, 1.0) / 2.0


def asymptotic_mdd(t: float, mu: float, sigma: float) -> float:
    """Large-T positive-drift asymptotic (2 sigma^2 / mu) (ln(x) / 4 + 0.49088), x = mu^2 T / (2 sigma^2)."""
    x = mu**2 * t / (2.0 * sigma**2)
    return 2.0 * sigma**2 / mu * (0.25 * math.log(x) + MAGDON_QP_CONST)


# ---------------------------------------------------------------------------
# Monte Carlo
# ---------------------------------------------------------------------------


def mc_mdd(t: float, mu: float, sigma: float, steps_per_year: int, n_paths: int, seed: int) -> np.ndarray:
    """Discretely monitored maximum drawdown (log units) of n_paths simulated paths."""
    rng = np.random.default_rng(seed)
    n = int(round(t * steps_per_year))
    dt = t / n
    out = np.empty(n_paths)
    batch = 2000
    for start in range(0, n_paths, batch):
        m = min(batch, n_paths - start)
        incr = mu * dt + sigma * math.sqrt(dt) * rng.standard_normal((m, n))
        x = np.concatenate([np.zeros((m, 1)), np.cumsum(incr, axis=1)], axis=1)
        out[start : start + m] = np.max(np.maximum.accumulate(x, axis=1) - x, axis=1)
    return out


def mc_terminal_drawdown(mu: float, sigma: float, years: float, steps_per_year: int, n_paths: int, seed: int) -> np.ndarray:
    """Drawdown D_T = M_T - X_T at the horizon, for n_paths paths (close to stationary once T >> sigma^2 / mu^2)."""
    rng = np.random.default_rng(seed)
    n = int(years * steps_per_year)
    dt = 1.0 / steps_per_year
    out = np.empty(n_paths)
    batch = 500
    for start in range(0, n_paths, batch):
        m = min(batch, n_paths - start)
        x = np.cumsum(mu * dt + sigma * math.sqrt(dt) * rng.standard_normal((m, n)), axis=1)
        out[start : start + m] = np.maximum(np.max(x, axis=1), 0.0) - x[:, -1]
    return out


def mc_ever_lose(h: float, mu: float, sigma: float, years: float, steps_per_year: int, n_paths: int, seed: int) -> float:
    """P(min_t X_t <= -h) within `years`, with an exact Brownian-bridge crossing correction between steps."""
    rng = np.random.default_rng(seed)
    n = int(years * steps_per_year)
    dt = 1.0 / steps_per_year
    surv = np.ones(n_paths)
    x = np.zeros(n_paths)
    for _ in range(n):
        x_new = x + mu * dt + sigma * math.sqrt(dt) * rng.standard_normal(n_paths)
        above = (x > -h) & (x_new > -h)
        p_cross = np.where(above, np.exp(-2.0 * (x + h) * (x_new + h) / (sigma**2 * dt)), 1.0)
        surv *= 1.0 - p_cross
        x = x_new
    return float(1.0 - surv.mean())


# ---------------------------------------------------------------------------
# Limit ladders and drawdown-control policies
# ---------------------------------------------------------------------------

LADDER = ((0.05, 1.0), (0.10, 0.7), (0.15, 0.4))  # (drawdown below which, risk multiplier); at or beyond 15%: stop


def ladder_multiplier(dd: float) -> float:
    """Risk multiplier of the note's ladder: < 5% full, 5-10% 70%, 10-15% 40%, >= 15% liquidate."""
    for bound, mult in LADDER:
        if dd < bound:
            return mult
    return 0.0


def simulate_ladder(mu: float, sigma: float, years: float, n_paths: int, seed: int, use_ladder: bool) -> dict[str, float]:
    """Daily simple returns r = mu dt + sigma sqrt(dt) z; exposure set from the previous close's drawdown."""
    rng = np.random.default_rng(seed)
    n = int(years * TRADING_DAYS)
    dt = 1.0 / TRADING_DAYS
    eq = np.ones(n_paths)
    hwm = np.ones(n_paths)
    mdd = np.zeros(n_paths)
    stopped = np.zeros(n_paths, dtype=bool)
    for _ in range(n):
        r = mu * dt + sigma * math.sqrt(dt) * rng.standard_normal(n_paths)
        if use_ladder:
            dd = 1.0 - eq / hwm
            mult = np.select([dd < 0.05, dd < 0.10, dd < 0.15], [1.0, 0.7, 0.4], 0.0)
            stopped |= mult == 0.0
            mult = np.where(stopped, 0.0, mult)
        else:
            mult = 1.0
        eq = eq * (1.0 + mult * r)
        hwm = np.maximum(hwm, eq)
        mdd = np.maximum(mdd, 1.0 - eq / hwm)
    return {
        "mean_return": float(eq.mean() - 1.0),
        "p_mdd_20": float(np.mean(mdd >= 0.20)),
        "mean_mdd": float(mdd.mean()),
        "p_stopped": float(stopped.mean()),
    }


def simulate_drawdown_floor(
    m: float, alpha: float, mu: float, sigma: float, years: float, steps: int, n_paths: int, seed: int, crash: float | None
) -> dict[str, float]:
    """Grossman-Zhou style policy: risky exposure = m (W - alpha M); M = running max of W.

    The risky asset has simple per-step returns mu dt + sigma sqrt(dt) z; `crash` adds a one-step return at mid-horizon.
    Returns the worst ratio W / M seen (the floor is alpha) and the share of paths that breached it.
    """
    rng = np.random.default_rng(seed)
    n = int(years * steps)
    dt = 1.0 / steps
    w = np.ones(n_paths)
    mx = np.ones(n_paths)
    worst = np.ones(n_paths)
    for i in range(n):
        r = mu * dt + sigma * math.sqrt(dt) * rng.standard_normal(n_paths)
        if crash is not None and i == n // 2:
            r = np.full(n_paths, crash)
        exposure = m * np.maximum(w - alpha * mx, 0.0)
        w = w + exposure * r
        mx = np.maximum(mx, w)
        worst = np.minimum(worst, w / mx)
    return {"worst_ratio": float(worst.min()), "p_breach": float(np.mean(worst < alpha - 1e-12))}


# ---------------------------------------------------------------------------
# The note's numbers
# ---------------------------------------------------------------------------


def section_closed_forms() -> None:
    print("\n[Core concepts: closed forms and the exact series]")
    for h, t, mu, sigma in ((0.05, 1.0, 0.15, 0.10), (0.30, 3.0, 0.15, 0.10), (0.40, 2.0, -0.10, 0.20), (0.20, 1.0, 0.0, 0.20)):
        fast, slow = survival_mdd(h, t, mu, sigma), _survival_by_quadrature(h, t, mu, sigma)
        assert abs(fast - slow) < 1e-10, f"closed-form coefficients disagree with quadrature: {fast} vs {slow}"
    print("  closed-form series coefficients agree with Gauss-Legendre quadrature to 1e-10")
    e0 = expected_mdd(1.0, 0.0, 1.0)
    check("E[MDD], mu = 0, sigma = 1, T = 1 (series)", e0, math.sqrt(math.pi / 2.0), 1e-9)
    check("sqrt(pi/2) (zero-drift closed form)", math.sqrt(math.pi / 2.0), 1.2533, 5e-5)
    check("sqrt(2/pi): E[max of W on [0,1]], for contrast", math.sqrt(2.0 / math.pi), 0.7979, 5e-5)
    qp = {x: magdon_q(x, positive=True) for x in (1.0, 10.0, 100.0, 1000.0)}
    for x, v in qp.items():
        print(f"  Q_p({x:g}) = {v:.5f}; 0.25 ln x + 0.49088 = {0.25 * math.log(x) + MAGDON_QP_CONST:.5f}")
    want = {1.0: (0.5877, 0.4909), 10.0: (1.0875, 1.0665), 100.0: (1.6457, 1.6422), 1000.0: (2.2183, 2.2178)}
    for x, (q_exact, q_asym) in want.items():
        check(f"Q_p({x:g}) exact", qp[x], q_exact, 5e-5)
        check(f"Q_p({x:g}) asymptote", 0.25 * math.log(x) + MAGDON_QP_CONST, q_asym, 5e-5)
    gaps = [qp[x] - (0.25 * math.log(x) + MAGDON_QP_CONST) for x in (10.0, 100.0, 1000.0)]
    assert gaps[0] > gaps[1] > gaps[2] > 0.0, "the asymptote must undershoot and tighten as x grows"
    check("gap exact - asymptote at x = 10", gaps[0], 0.021, 5e-4)
    check("gap at x = 100", gaps[1], 0.0035, 5e-5)
    check("gap at x = 1000", gaps[2], 0.0005, 5e-5)
    small = magdon_q(1e-4, positive=True)
    check("Q_p(1e-4) / (sqrt(pi/8) sqrt(2e-4)), small-x limit", small / (math.sqrt(math.pi / 8.0) * math.sqrt(2e-4)), 0.995, 1e-3)
    check("(ln 4 + Euler gamma) / 4, against the quoted 0.49088", (math.log(4.0) + EULER_GAMMA) / 4.0, 0.49088, 5e-6)


def section_example_1() -> dict[str, float]:
    print("\n[Worked example 1: Sharpe 1.5, sigma 10%, T = 3 and 10 years]")
    mu, sigma = 0.15, 0.10
    out = {}
    for t in (3.0, 10.0):
        x = mu**2 * t / (2.0 * sigma**2)
        asym = asymptotic_mdd(t, mu, sigma)
        gamma_form = sigma**2 / (2.0 * mu) * (math.log(2.0 * (mu / sigma) ** 2 * t) + EULER_GAMMA)
        exact = expected_mdd(t, mu, sigma)
        pct = expected_pct_mdd(t, mu, sigma)
        q95 = mdd_quantile(0.95, t, mu, sigma)
        print(f"  T = {t:g}: x = {x:.4f}, asymptote {asym:.5f}, gamma form {gamma_form:.5f}, exact {exact:.5f}, "
              f"E[% MDD] {pct:.5f}, 95% quantile {q95:.5f}")  # fmt: skip
        out[f"asym{t:g}"], out[f"exact{t:g}"], out[f"pct{t:g}"], out[f"q95_{t:g}"] = asym, exact, pct, q95
        assert abs(gamma_form - asym) < 1e-5, "the gamma form and the 0.49088 form must agree"
    check("x = mu^2 T / (2 sigma^2), T = 3", mu**2 * 3.0 / (2.0 * sigma**2), 3.375, 1e-12)
    check("x, T = 10", mu**2 * 10.0 / (2.0 * sigma**2), 11.25, 1e-12)
    check("asymptote, T = 3", out["asym3"], 0.1060, 5e-5)
    check("asymptote, T = 10", out["asym10"], 0.1461, 5e-5)
    check("exact E[MDD], T = 3", out["exact3"], 0.1120, 5e-5)
    check("exact E[MDD], T = 10", out["exact10"], 0.1487, 5e-5)
    check("exact E[% MDD] = E[1 - exp(-MDD)], T = 3", out["pct3"], 0.1054, 5e-5)
    check("exact E[% MDD], T = 10", out["pct10"], 0.1375, 5e-5)
    check("95% quantile of MDD, T = 3", out["q95_3"], 0.1799, 5e-5)
    check("95% quantile of MDD, T = 10", out["q95_10"], 0.2234, 5e-5)
    p15 = prob_mdd_at_least(0.15, 3.0, mu, sigma)
    check("exact P(MDD_3y >= 0.15)", p15, 0.1311, 5e-5)
    check("asymptote shortfall, T = 3 (percentage points)", (out["exact3"] - out["asym3"]) * 100, 0.60, 5e-3)
    check("asymptote / exact, T = 3", out["asym3"] / out["exact3"], 0.947, 5e-4)
    check("percentage fall for a 0.10 log drawdown", 1.0 - math.exp(-0.10), 0.0952, 5e-5)
    # Monte Carlo at daily and at 10x finer monitoring, then extrapolation in sqrt(dt).
    daily = mc_mdd(3.0, mu, sigma, TRADING_DAYS, 20_000, seed=5)
    fine = mc_mdd(3.0, mu, sigma, 10 * TRADING_DAYS, 8_000, seed=6)
    r = math.sqrt(10.0)
    extrap = (fine.mean() * r - daily.mean()) / (r - 1.0)
    print(f"  MC daily {daily.mean():.5f} (s.e. {daily.std() / math.sqrt(daily.size):.5f}), "
          f"10x finer {fine.mean():.5f} (s.e. {fine.std() / math.sqrt(fine.size):.5f}), sqrt(dt) extrapolation {extrap:.5f}")  # fmt: skip
    check("MC daily mean MDD, T = 3 (seed 5)", float(daily.mean()), 0.1049, 1e-3)
    check("MC 10x finer mean MDD, T = 3 (seed 6)", float(fine.mean()), 0.1094, 1.5e-3)
    check("sqrt(dt)-extrapolated MC, against the exact series", float(extrap), out["exact3"], 2.5e-3)
    check("MC daily P(MDD_3y >= 15%)", float(np.mean(daily >= 0.15)), 0.105, 5e-3)
    assert daily.mean() < fine.mean() < out["exact3"], "discrete monitoring can only miss drawdown"
    return out


def section_sharpe_table() -> None:
    print("\n[Core concepts: E[MDD] / sigma by Sharpe and horizon (sigma = 1, mu = S)]")
    expected = {
        0.0: (1.253, 2.171, 3.963),
        0.5: (1.069, 1.663, 2.525),
        1.0: (0.925, 1.336, 1.855),
        2.0: (0.727, 0.969, 1.252),
    }
    for s, vals in expected.items():
        got = [expected_mdd(t, s, 1.0) for t in (1.0, 3.0, 10.0)]
        print(f"  S = {s:.1f}: T=1 {got[0]:.3f}  T=3 {got[1]:.3f}  T=10 {got[2]:.3f}")
        for g, w in zip(got, vals, strict=True):
            assert abs(g - w) < 5e-4, f"E[MDD]/sigma table, S={s}: {g} vs {w}"
    print("  E[MDD]/sigma table matches the note")
    print("\n[Core concepts: P(MDD_T >= h), sigma = 10%]")
    want = {0.0: (0.629, 0.495), 0.5: (0.476, 0.242), 1.0: (0.331, 0.089), 2.0: (0.126, 0.006)}
    for s, vals in want.items():
        got = (prob_mdd_at_least(0.10, 1.0, 0.1 * s, 0.1), prob_mdd_at_least(0.20, 3.0, 0.1 * s, 0.1))
        print(f"  S = {s:.1f}: P(MDD_1y >= 10%) {got[0]:.3f}  P(MDD_3y >= 20%) {got[1]:.3f}")
        for g, w in zip(got, vals, strict=True):
            assert abs(g - w) < 5e-4, f"probability table, S={s}: {g} vs {w}"
    print("  probability table matches the note")


def section_stationary_and_ruin() -> None:
    print("\n[Core concepts: long-run drawdown and probability of ever losing h, S = 1, sigma = 10%]")
    mu, sigma = 0.10, 0.10
    check("stationary mean drawdown sigma^2 / (2 mu)", sigma**2 / (2.0 * mu), 0.05, 1e-12)
    check("stationary P(D > 10%) = exp(-2 mu h / sigma^2)", math.exp(-2.0 * mu * 0.10 / sigma**2), 0.1353, 5e-5)
    daily = mc_terminal_drawdown(mu, sigma, 20.0, TRADING_DAYS, 20_000, seed=11)
    fine = mc_terminal_drawdown(mu, sigma, 10.0, 10 * TRADING_DAYS, 4_000, seed=12)
    print(f"  MC D_T: daily T=20 mean {daily.mean():.5f}, P(D>10%) {np.mean(daily > 0.1):.4f}; "
          f"10x finer T=10 mean {fine.mean():.5f}")  # fmt: skip
    check("MC mean D_20y, daily (seed 11)", float(daily.mean()), 0.0465, 1e-3)
    check("MC mean D_10y, 10x finer (seed 12)", float(fine.mean()), 0.0489, 1e-3)
    check("MC P(D_20y > 10%), daily", float(np.mean(daily > 0.10)), 0.126, 1e-3)
    p_formula = math.exp(-2.0 * mu * 0.20 / sigma**2)
    p_mc = mc_ever_lose(0.20, mu, sigma, 100.0, 12, 50_000, seed=13)
    print(f"  P(ever lose 20% log): formula {p_formula:.5f}, bridge-corrected MC {p_mc:.5f}")
    check("exp(-2 mu h / sigma^2) = exp(-4), card risk-probability-ever-losing-h", p_formula, 0.0183, 5e-5)
    check("bridge-corrected MC over 100 years (seed 13)", p_mc, p_formula, 1.2e-3)


def section_recovery_and_ladder() -> None:
    print("\n[Core concepts: recovery asymmetry]")
    want = {0.10: 0.111, 0.20: 0.250, 0.30: 0.429, 0.50: 1.000, 0.75: 3.000, 0.90: 9.000}
    for d, w in want.items():
        check(f"gain to recover from {d:.0%}", 1.0 / (1.0 - d) - 1.0, w, 5e-4)
    print("\n[Worked example 2: the drawdown ladder]")
    eq0, hwm = 88_000_000.0, 100_000_000.0
    mult = ladder_multiplier(1.0 - eq0 / hwm)
    check("multiplier at a 12% drawdown", mult, 0.40, 1e-12)
    throttled = eq0 * (1.0 + mult * 0.15)
    full = eq0 * 1.15
    check("throttled equity after a +15% rebound (m)", throttled / 1e6, 93.28, 1e-9)
    check("remaining drawdown", 1.0 - throttled / hwm, 0.0672, 1e-9)
    check("unthrottled equity (m)", full / 1e6, 101.2, 1e-9)
    check("gain still needed after throttling", hwm / throttled - 1.0, 0.0720, 5e-5)
    check("50% cut after a 20% loss, +25% rebound: equity", 0.8 * (1.0 + 0.5 * 0.25), 0.90, 1e-12)
    print("\n[Core concepts: what the ladder costs and buys, 1 year, sigma 20%, 20,000 paths, seed 21]")
    res = {}
    for s in (1.0, 0.0):
        for use in (False, True):
            res[(s, use)] = simulate_ladder(0.20 * s, 0.20, 1.0, 20_000, seed=21, use_ladder=use)
            r = res[(s, use)]
            print(f"  S = {s:.0f}, ladder {use!s:<5}: mean return {r['mean_return']:+.4f}, mean MDD {r['mean_mdd']:.4f}, "
                  f"P(MDD >= 20%) {r['p_mdd_20']:.4f}, P(stopped) {r['p_stopped']:.4f}")  # fmt: skip
    check("S=1 no ladder: mean return", res[(1.0, False)]["mean_return"], 0.222, 5e-4)
    check("S=1 ladder: mean return", res[(1.0, True)]["mean_return"], 0.167, 5e-4)
    check("S=1 no ladder: mean MDD", res[(1.0, False)]["mean_mdd"], 0.159, 5e-4)
    check("S=1 ladder: mean MDD", res[(1.0, True)]["mean_mdd"], 0.122, 5e-4)
    check("S=1 no ladder: P(MDD >= 20%)", res[(1.0, False)]["p_mdd_20"], 0.217, 5e-4)
    check("S=1 ladder: P(stopped)", res[(1.0, True)]["p_stopped"], 0.180, 5e-4)
    check("S=0 no ladder: P(MDD >= 20%)", res[(0.0, False)]["p_mdd_20"], 0.499, 5e-4)
    check("S=0 ladder: P(stopped)", res[(0.0, True)]["p_stopped"], 0.454, 5e-4)
    check("S=0 ladder: mean MDD", res[(0.0, True)]["mean_mdd"], 0.138, 5e-4)
    check("S=0 no ladder: mean MDD", res[(0.0, False)]["mean_mdd"], 0.213, 5e-4)
    assert res[(1.0, True)]["p_mdd_20"] == 0.0 and res[(0.0, True)]["p_mdd_20"] == 0.0, "the hard stop caps MDD below 20%"
    cost = res[(1.0, False)]["mean_return"] - res[(1.0, True)]["mean_return"]
    check("expected-return cost of the ladder, Sharpe 1 (points)", cost * 100, 5.6, 0.05)
    assert abs(res[(0.0, True)]["mean_return"]) < 0.002 and abs(res[(0.0, False)]["mean_return"]) < 0.002


def section_limits() -> None:
    print("\n[Core concepts: VaR limit implied vol and drawdown consistency]")
    z99 = 2.3263478740408408  # standard normal 99% quantile
    sig_d = 0.01 / z99
    sig_a = sig_d * math.sqrt(TRADING_DAYS)
    check("daily sigma allowed by a 1% 99% VaR limit", sig_d, 0.0043, 5e-5)
    check("annualised", sig_a, 0.0682, 5e-5)
    check("P(MDD_1y >= 10%) at that vol, Sharpe 1", prob_mdd_at_least(0.10, 1.0, sig_a, sig_a), 0.0804, 5e-5)
    check("P(MDD_1y >= 10%) at that vol, Sharpe 0", prob_mdd_at_least(0.10, 1.0, 0.0, sig_a), 0.2856, 5e-5)
    print("\n[Core concepts: drawdown-control policy, m = 4, alpha = 0.8, sigma 20%, 5 years daily]")
    calm = simulate_drawdown_floor(4.0, 0.8, 0.08, 0.20, 5.0, TRADING_DAYS, 4000, seed=31, crash=None)
    gap = simulate_drawdown_floor(4.0, 0.8, 0.08, 0.20, 5.0, TRADING_DAYS, 4000, seed=31, crash=-0.30)
    print(f"  no gap: worst W/M {calm['worst_ratio']:.4f}, breached {calm['p_breach']:.4f}")
    print(f"  one -30% gap day: worst W/M {gap['worst_ratio']:.4f}, breached {gap['p_breach']:.4f}")
    check("gap that wipes the cushion, 1/m", 1.0 / 4.0, 0.25, 1e-12)
    check("no-gap worst W/M (seed 31)", calm["worst_ratio"], 0.800, 5e-4)
    check("worst W/M with a -30% gap: 0.8 - 0.2 x 0.2 at most", gap["worst_ratio"], 0.76, 1e-9)
    assert calm["p_breach"] == 0.0 and gap["p_breach"] == 1.0


def main() -> None:
    section_closed_forms()
    section_example_1()
    section_sharpe_table()
    section_stationary_and_ruin()
    section_recovery_and_ladder()
    section_limits()
    print("\nAll drawdown checks passed.")


if __name__ == "__main__":
    main()
