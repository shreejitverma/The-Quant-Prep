"""Convex portfolio problems, KKT conditions and three small QP solvers: every number quoted in notes 08 and 09.

Run: uv run --no-project --with numpy python 03-Linear-Algebra-and-Optimization/code/portfolio_optimization.py

Solvers (dense, small n, for teaching; production code uses OSQP, Clarabel, MOSEK, Gurobi and the like):
- projected gradient onto {1'w = 1, lo <= w <= hi};
- primal active-set method for the same feasible set;
- primal-dual interior-point method for min 1/2 x'Qx + c'x s.t. Ax = b, Gx <= h.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def check(label: str, value: float, expected: float, tol: float = 5e-4) -> float:
    """Print a labelled number and assert it matches the value quoted in the notes."""
    v = float(value) + 0.0
    print(f"{label} = {int(v) if v.is_integer() and abs(v) < 1e15 else format(v, '.10g')}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


def cov_from(vols: np.ndarray, corr: np.ndarray) -> np.ndarray:
    return corr * np.outer(vols, vols)


# ---------------------------------------------------------------------------
# Note 08: closed forms from the Lagrangian
# ---------------------------------------------------------------------------

VOL3 = np.array([0.15, 0.20, 0.25])
CORR3 = np.array([[1.0, 0.3, 0.2], [0.3, 1.0, 0.5], [0.2, 0.5, 1.0]])
MU3 = np.array([0.05, 0.07, 0.09])
RF = 0.02


def closed_forms() -> None:
    print("\n[08] three-asset closed forms")
    sigma = cov_from(VOL3, CORR3)
    ones = np.ones(3)
    si1 = np.linalg.solve(sigma, ones)
    si_mu = np.linalg.solve(sigma, MU3)
    a, b, c = ones @ si1, ones @ si_mu, MU3 @ si_mu
    d = a * c - b * b
    check("A = 1'S^-1 1", a, 56.3137, 1e-4)
    check("B = 1'S^-1 mu", b, 3.32706, 1e-5)
    check("C = mu'S^-1 mu", c, 0.219592, 1e-6)
    check("D = AC - B^2", d, 1.29673, 1e-5)
    w_gmv = si1 / a
    for i, want in enumerate((0.6616, 0.2228, 0.1156)):
        check(f"GMV weight {i + 1}", w_gmv[i], want, 1e-4)
    check("GMV vol = 1/sqrt(A)", math.sqrt(w_gmv @ sigma @ w_gmv), 1 / math.sqrt(a), 1e-12)
    check("GMV vol", 1 / math.sqrt(a), 0.133258, 1e-6)
    check("GMV mean = B/A", w_gmv @ MU3, 0.059081, 1e-6)

    # target-return frontier via the full KKT system: [2S mu 1; mu' 0 0; 1' 0 0]
    m = 0.08
    kkt = np.zeros((5, 5))
    kkt[:3, :3] = 2 * sigma
    kkt[:3, 3] = -MU3
    kkt[:3, 4] = -ones
    kkt[3, :3] = MU3
    kkt[4, :3] = ones
    sol = np.linalg.solve(kkt, np.array([0, 0, 0, m, 1.0]))
    w, lam, nu = sol[:3], sol[3], sol[4]
    for i, want in enumerate((0.1048, 0.2903, 0.6048)):
        check(f"frontier weight {i + 1} at m = 8%", w[i], want, 1e-4)
    var_m = (a * m * m - 2 * b * m + c) / d
    check("frontier variance (A m^2 - 2 B m + C)/D", w @ sigma @ w, var_m, 1e-12)
    check("frontier vol at m = 8%", math.sqrt(var_m), 0.191734, 1e-6)
    check("multiplier lambda on the return constraint", lam, 2 * (a * m - b) / d, 1e-9)
    check("lambda value", lam, 1.81694, 1e-5)
    check("multiplier nu on the budget", nu, 2 * (c - b * m) / d, 1e-9)
    h = 1e-6
    fd = ((a * (m + h) ** 2 - 2 * b * (m + h) + c) - (a * (m - h) ** 2 - 2 * b * (m - h) + c)) / d / (2 * h)
    check("shadow price d(var)/dm by finite difference = lambda", fd, lam, 1e-6)
    check("variance cost of +10bp target, lambda x 0.001", lam * 0.001, 0.0018169, 1e-7)

    excess = MU3 - RF
    z = np.linalg.solve(sigma, excess)
    w_tan = z / z.sum()
    for i, want in enumerate((0.3831, 0.2566, 0.3603)):
        check(f"tangency weight {i + 1}", w_tan[i], want, 1e-4)
    sharpe = math.sqrt(excess @ z)
    check("max Sharpe sqrt((mu - r)'S^-1 (mu - r))", sharpe, 0.330205, 1e-6)
    check("tangency Sharpe from weights", (w_tan @ excess) / math.sqrt(w_tan @ sigma @ w_tan), sharpe, 1e-12)
    check("tangency expected return", w_tan @ MU3, 0.069544, 1e-6)
    check("tangency vol", math.sqrt(w_tan @ sigma @ w_tan), 0.150040, 1e-6)
    gamma = 4.0
    w_util = z / gamma
    check("mean-variance utility, gamma = 4: total risky weight", w_util.sum(), 0.550196, 1e-6)
    check("  ... portfolio vol", math.sqrt(w_util @ sigma @ w_util), 0.082551, 1e-6)


def long_only_two_asset() -> None:
    print("\n[08] two assets, vols 10% and 20%, rho = 0.8: KKT with w >= 0")
    s1, s2, rho = 0.10, 0.20, 0.8
    sigma = np.array([[s1 * s1, rho * s1 * s2], [rho * s1 * s2, s2 * s2]])
    w2 = (s1 * s1 - rho * s1 * s2) / (s1 * s1 + s2 * s2 - 2 * rho * s1 * s2)
    check("unconstrained GMV w2", w2, -1 / 3, 1e-12)
    w = np.array([1 - w2, w2])
    check("unconstrained GMV variance", w @ sigma @ w, 0.008, 1e-12)
    check("unconstrained GMV vol", math.sqrt(w @ sigma @ w), 0.089443, 1e-6)
    w_lo = np.array([1.0, 0.0])
    grad = 2 * sigma @ w_lo
    check("rho s1 s2", rho * s1 * s2, 0.016, 1e-15)
    check("gradient 2 Sigma w, asset 1", grad[0], 0.02, 1e-12)
    check("gradient 2 Sigma w, asset 2", grad[1], 0.032, 1e-12)
    check("denominator s1^2 + s2^2 - 2 rho s1 s2", s1 * s1 + s2 * s2 - 2 * rho * s1 * s2, 0.018, 1e-12)
    nu = grad[0]  # asset 1 is free: grad_1 = nu
    mult = grad[1] - nu  # asset 2 at its bound: grad_2 = nu + mult
    check("budget multiplier nu", nu, 0.02, 1e-12)
    check("bound multiplier on w2 >= 0", mult, 0.012, 1e-12)
    check("long-only variance", w_lo @ sigma @ w_lo, 0.01, 1e-12)
    eps = 1e-6
    w_relax = np.array([1 + eps, -eps])  # relax w2 >= 0 to w2 >= -eps
    check("shadow price: d(var)/d(relaxation)", -(w_relax @ sigma @ w_relax - 0.01) / eps, 0.012, 1e-5)


def duality_toy() -> None:
    print("\n[08] min x^2 s.t. x >= 1: dual function g(l) = l - l^2/4")
    lam = np.linspace(0, 4, 400_001)
    g = lam - lam**2 / 4
    check("dual optimum lambda*", lam[np.argmax(g)], 2.0, 1e-5)
    check("dual optimal value d*", g.max(), 1.0, 1e-12)
    x = np.linspace(1, 5, 400_001)
    check("primal optimum x* (grid over x >= 1)", x[np.argmin(x**2)], 1.0, 1e-12)
    check("primal optimal value p*", (x**2).min(), 1.0, 1e-12)


# ---------------------------------------------------------------------------
# Note 09: three QP solvers on a five-asset problem
# ---------------------------------------------------------------------------

VOL5 = np.array([0.12, 0.16, 0.20, 0.24, 0.30])
LOAD5 = np.array([0.5, 0.6, 0.7, 0.6, 0.9])
MU5 = np.array([0.04, 0.06, 0.07, 0.08, 0.10])


def sigma5() -> np.ndarray:
    corr = np.outer(LOAD5, LOAD5)
    np.fill_diagonal(corr, 1.0)
    return cov_from(VOL5, corr)


def project_budget_box(y: np.ndarray, lo: np.ndarray, hi: np.ndarray, budget: float = 1.0) -> np.ndarray:
    """Euclidean projection onto {sum w = budget, lo <= w <= hi}: w = clip(y - t), t found by bisection."""
    a, b = (y - hi).min() - 1.0, (y - lo).max() + 1.0  # sum(clip) is decreasing in t
    for _ in range(200):
        t = 0.5 * (a + b)
        if np.clip(y - t, lo, hi).sum() > budget:
            a = t
        else:
            b = t
    return np.clip(y - 0.5 * (a + b), lo, hi)


def project_simplex_sort(y: np.ndarray) -> np.ndarray:
    """Exact simplex projection by sorting (Held, Wolfe and Crowder 1974; Duchi et al. 2008)."""
    u = np.sort(y)[::-1]
    css = np.cumsum(u)
    k = np.arange(1, len(y) + 1)
    rho = int(np.nonzero(u - (css - 1) / k > 0)[0][-1])
    theta = (css[rho] - 1) / (rho + 1)
    return np.maximum(y - theta, 0.0)


def projected_gradient(q: np.ndarray, c: np.ndarray, lo: np.ndarray, hi: np.ndarray, tol: float = 1e-13) -> tuple[np.ndarray, int]:
    step = 1.0 / np.linalg.eigvalsh(q)[-1]
    w = project_budget_box(np.full(len(c), 1.0 / len(c)), lo, hi)
    for it in range(1, 200_000):
        w_new = project_budget_box(w - step * (q @ w + c), lo, hi)
        if np.abs(w_new - w).max() < tol:
            return w_new, it
        w = w_new
    raise RuntimeError("projected gradient did not converge")


def active_set(q: np.ndarray, c: np.ndarray, lo: np.ndarray, hi: np.ndarray, w0: np.ndarray) -> tuple[np.ndarray, int]:
    """Primal active-set method for min 1/2 w'Qw + c'w s.t. 1'w = 1, lo <= w <= hi, from a feasible w0.

    The working set fixes some variables at a bound. Each iteration solves the equality-constrained QP on the
    free variables; a blocked step adds a bound, and a wrong-signed multiplier releases one.
    """
    n = len(c)
    w = w0.astype(float).copy()
    at_lo = np.isclose(w, lo)
    at_hi = np.isclose(w, hi) & ~at_lo
    for it in range(1, 100):
        free = ~(at_lo | at_hi)
        f = np.nonzero(free)[0]
        fixed_sum = w[~free].sum()
        # KKT on free variables: Q_ff w_f + Q_f,fixed w_fixed + c_f = nu 1, 1'w_f = 1 - fixed_sum
        k = len(f)
        kkt = np.zeros((k + 1, k + 1))
        kkt[:k, :k] = q[np.ix_(f, f)]
        kkt[:k, k] = -1.0
        kkt[k, :k] = 1.0
        rhs = np.concatenate([-(c[f] + q[np.ix_(f, ~free)] @ w[~free]), [1.0 - fixed_sum]])
        sol = np.linalg.solve(kkt, rhs)
        target = w.copy()
        target[f] = sol[:k]
        nu = sol[k]
        p = target - w
        if np.abs(p).max() < 1e-14:
            g = q @ w + c
            mult_lo = np.where(at_lo, g - nu, np.inf)
            mult_hi = np.where(at_hi, nu - g, np.inf)
            worst = min(mult_lo.min(), mult_hi.min())
            if worst >= -1e-12:
                return w, it
            i = int(np.argmin(np.minimum(mult_lo, mult_hi)))
            at_lo[i] = at_hi[i] = False
            continue
        # longest feasible step along p, capped at 1
        alpha, block, to_hi = 1.0, -1, False
        for i in f:
            if p[i] < -1e-15 and (lo[i] - w[i]) / p[i] < alpha:
                alpha, block, to_hi = (lo[i] - w[i]) / p[i], i, False
            elif p[i] > 1e-15 and (hi[i] - w[i]) / p[i] < alpha:
                alpha, block, to_hi = (hi[i] - w[i]) / p[i], i, True
        w = w + alpha * p
        if block >= 0:
            w[block] = hi[block] if to_hi else lo[block]
            (at_hi if to_hi else at_lo)[block] = True
    raise RuntimeError(f"active set did not converge in {n} variables")


@dataclass
class IpmResult:
    x: np.ndarray
    y: np.ndarray  # equality multipliers
    z: np.ndarray  # inequality multipliers
    s: np.ndarray  # slacks h - Gx
    iterations: int


def interior_point(
    q: np.ndarray, c: np.ndarray, a: np.ndarray, b: np.ndarray, g: np.ndarray, h: np.ndarray, tol: float = 1e-10
) -> IpmResult:
    """Primal-dual path-following for min 1/2 x'Qx + c'x s.t. Ax = b, Gx <= h (no Mehrotra corrector)."""
    n, m_eq, m_in = len(c), len(b), len(h)
    x = np.zeros(n)
    y = np.zeros(m_eq)
    s = np.ones(m_in)
    z = np.ones(m_in)
    for it in range(1, 200):
        r_d = q @ x + c + a.T @ y + g.T @ z
        r_p = a @ x - b
        r_g = g @ x + s - h
        mu = s @ z / m_in
        if max(np.abs(r_d).max(), np.abs(r_p).max(), np.abs(r_g).max(), mu) < tol:
            return IpmResult(x, y, z, s, it)
        sigma_c = 0.1
        d = z / s
        lhs = np.zeros((n + m_eq, n + m_eq))
        lhs[:n, :n] = q + g.T @ (d[:, None] * g)
        lhs[:n, n:] = a.T
        lhs[n:, :n] = a
        rhs_x = -r_d - g.T @ (d * r_g - z + sigma_c * mu / s)
        sol = np.linalg.solve(lhs, np.concatenate([rhs_x, -r_p]))
        dx, dy = sol[:n], sol[n:]
        dz = d * (g @ dx + r_g) - z + sigma_c * mu / s
        ds = -r_g - g @ dx
        step = 1.0
        for v, dv in ((s, ds), (z, dz)):
            neg = dv < 0
            if neg.any():
                step = min(step, 0.99 * float((-v[neg] / dv[neg]).min()))
        x, y, z, s = x + step * dx, y + step * dy, z + step * dz, s + step * ds
    raise RuntimeError("interior point did not converge")


def kkt_budget_box(q: np.ndarray, c: np.ndarray, lo: np.ndarray, hi: np.ndarray, w: np.ndarray) -> dict[str, float]:
    """KKT residuals for min 1/2 w'Qw + c'w s.t. 1'w = 1, lo <= w <= hi."""
    grad = q @ w + c
    tol = 1e-9
    at_lo = w <= lo + tol
    at_hi = w >= hi - tol
    free = ~(at_lo | at_hi)
    nu = grad[free].mean()
    return {
        "stationarity": float(np.abs(grad[free] - nu).max()),
        "primal": float(max(abs(w.sum() - 1), (lo - w).max(), (w - hi).max(), 0.0)),
        "min bound multiplier": float(min(np.min(grad[at_lo] - nu, initial=np.inf), np.min(nu - grad[at_hi], initial=np.inf))),
        "nu": float(nu),
    }


def budget_box_ipm(q: np.ndarray, c: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> IpmResult:
    n = len(c)
    g = np.vstack([-np.eye(n), np.eye(n)])
    h = np.concatenate([-lo, hi])
    return interior_point(q, c, np.ones((1, n)), np.array([1.0]), g, h)


def solver_comparison() -> None:
    print("\n[09] five-asset problems: projected gradient vs active set vs interior point")
    sigma = sigma5()
    n = 5
    w_unc = np.linalg.solve(sigma, np.ones(n))
    w_unc /= w_unc.sum()
    for i, want in enumerate((0.6477, 0.3190, 0.1501, 0.0778, -0.1946)):
        check(f"unconstrained GMV weight {i + 1}", w_unc[i], want, 1e-4)
    check("five-asset unconstrained GMV vol", math.sqrt(w_unc @ sigma @ w_unc), 0.099725, 1e-6)

    # P1: long-only minimum variance
    q, c = 2 * sigma, np.zeros(n)
    lo, hi = np.zeros(n), np.ones(n)
    w_pg, it_pg = projected_gradient(q, c, lo, hi)
    w_as, it_as = active_set(q, c, lo, hi, np.full(n, 0.2))
    ipm = budget_box_ipm(q, c, lo, hi)
    for i, want in enumerate((0.6587, 0.2682, 0.0523, 0.0208, 0.0)):
        check(f"P1 long-only GMV weight {i + 1}", w_as[i], want, 1e-4)
    check("P1 long-only GMV vol", math.sqrt(w_as @ sigma @ w_as), 0.107933, 1e-6)
    clipped = np.maximum(w_unc, 0.0)
    clipped /= clipped.sum()
    for i, want in enumerate((0.5422, 0.2670, 0.1257, 0.0651, 0.0)):
        check(f"clip-and-renormalise weight {i + 1}", clipped[i], want, 1e-4)
    check("clip-and-renormalise vol", math.sqrt(clipped @ sigma @ clipped), 0.109862, 1e-6)
    check("P1 max |PG - active set|", np.abs(w_pg - w_as).max(), 0.0, 1e-9)
    check("P1 max |IPM - active set|", np.abs(ipm.x - w_as).max(), 0.0, 1e-8)
    check("P1 projected-gradient iterations", it_pg, 258, 0)
    check("P1 active-set iterations", it_as, 3, 0)
    check("P1 interior-point iterations", ipm.iterations, 14, 0)
    k = kkt_budget_box(q, c, lo, hi, w_as)
    check("P1 KKT stationarity residual", k["stationarity"], 0.0, 1e-12)
    check("P1 KKT primal residual", k["primal"], 0.0, 1e-12)
    check("P1 smallest bound multiplier (>= 0)", k["min bound multiplier"], 0.017517, 1e-6)
    check("P1 budget multiplier nu = 2 x variance", k["nu"], 2 * w_as @ sigma @ w_as, 1e-12)
    check("P1 IPM complementarity max s_i z_i", float((ipm.s * ipm.z).max()), 0.0, 1e-10)

    # P2: mean-variance with box 0 <= w <= 0.35, risk aversion 4
    gamma = 4.0
    q, c = gamma * sigma, -MU5
    hi = np.full(n, 0.35)
    w_pg, it_pg = projected_gradient(q, c, lo, hi)
    w_as, it_as = active_set(q, c, lo, hi, np.full(n, 0.2))
    ipm = budget_box_ipm(q, c, lo, hi)
    for i, want in enumerate((0.35, 0.3256, 0.1721, 0.1524, 0.0)):
        check(f"P2 box mean-variance weight {i + 1}", w_as[i], want, 1e-4)
    check("P2 expected return", w_as @ MU5, 0.057768, 1e-6)
    check("P2 vol", math.sqrt(w_as @ sigma @ w_as), 0.119076, 1e-6)
    check("P2 max |PG - active set|", np.abs(w_pg - w_as).max(), 0.0, 1e-9)
    check("P2 max |IPM - active set| (about 3e-7)", np.abs(ipm.x - w_as).max(), 3e-7, 5e-8)
    k = kkt_budget_box(q, c, lo, hi, w_as)
    check("P2 KKT stationarity residual", k["stationarity"], 0.0, 1e-12)
    check("P2 smallest bound multiplier (>= 0)", k["min bound multiplier"], 0.000370, 1e-6)
    print(f"P2 iterations: PG {it_pg}, active set {it_as}, IPM {ipm.iterations}")
    check("P2 projected-gradient iterations", it_pg, 178, 0)
    check("P2 active-set iterations", it_as, 4, 0)


def simplex_projection_examples() -> None:
    print("\n[09] Euclidean projection onto the simplex")
    y = np.array([0.5, 0.4, -0.2, 0.6])
    p = project_simplex_sort(y)
    check("simplex threshold theta = y_i - p_i on the support", y[0] - p[0], 1 / 6, 1e-12)
    for i, want in enumerate((0.3333, 0.2333, 0.0, 0.4333)):
        check(f"projection component {i + 1}", p[i], want, 1e-4)
    check("bisection projection agrees", np.abs(project_budget_box(y, np.zeros(4), np.ones(4)) - p).max(), 0.0, 1e-12)


def rebalance_with_costs() -> None:
    print("\n[09] rebalance from equal weights with linear costs and a turnover cap")
    sigma = sigma5()
    n = 5
    gamma, cost, tau = 4.0, 0.002, 0.20
    w0 = np.full(n, 0.2)
    # variables x = (w, buy, sell): w = w0 + buy - sell
    q = np.zeros((3 * n, 3 * n))
    q[:n, :n] = gamma * sigma
    c = np.concatenate([-MU5, np.full(n, cost), np.full(n, cost)])
    a = np.zeros((n + 1, 3 * n))
    a[:n, :n] = np.eye(n)
    a[:n, n : 2 * n] = -np.eye(n)
    a[:n, 2 * n :] = np.eye(n)
    a[n, :n] = 1.0
    b = np.concatenate([w0, [1.0]])
    g = np.vstack([-np.eye(3 * n), np.concatenate([np.zeros(n), np.ones(2 * n)])[None, :]])
    h = np.concatenate([np.zeros(3 * n), [tau]])
    check("rebalance QP: variables", q.shape[0], 15, 0)
    check("rebalance QP: equalities", a.shape[0], 6, 0)
    check("rebalance QP: inequalities", g.shape[0], 16, 0)
    res = interior_point(q, c, a, b, g, h)
    w = res.x[:n]
    turnover = np.abs(w - w0).sum()
    for i, want in enumerate((0.2787, 0.2213, 0.2, 0.2, 0.1)):
        check(f"rebalanced weight {i + 1}", w[i], want, 1e-4)
    check("turnover |w - w0|_1", turnover, 0.2, 1e-6)
    check("turnover cap multiplier (shadow price per unit turnover)", res.z[-1], 0.016543, 1e-6)
    check("interior-point iterations", res.iterations, 13, 0)
    r_d = q @ res.x + c + a.T @ res.y + g.T @ res.z
    check("KKT stationarity residual", np.abs(r_d).max(), 0.0, 1e-9)
    check("KKT complementarity max s_i z_i", float((res.s * res.z).max()), 0.0, 1e-9)
    check("buy and sell never both positive", float(np.minimum(res.x[n : 2 * n], res.x[2 * n :]).max()), 0.0, 1e-8)
    # The same problem without the turnover cap: the optimiser sells asset 5 all the way to zero.
    free = interior_point(q, c, a, b, g[:-1], h[:-1])
    check("no cap: weight of asset 5", free.x[n - 1], 0.0, 1e-6)
    check("no cap: turnover |w - w0|_1", np.abs(free.x[:n] - w0).sum(), 0.4717, 1e-4)


def main() -> None:
    closed_forms()
    long_only_two_asset()
    duality_toy()
    solver_comparison()
    simplex_projection_examples()
    rebalance_with_costs()
    print("\nall portfolio_optimization checks passed")


if __name__ == "__main__":
    main()
