"""Kalman filter, RTS smoother and prediction-error likelihood: local level model and time-varying hedge ratio.

Backs every number in ``11-State-Space-Models-and-Kalman-Filter.md``.
Run ``uv run --no-project --with numpy python 02-Statistics-and-Econometrics/code/kalman_filter.py``;
each printed number is asserted, so drift in the note fails CI.
Simulations use fixed seeds; their results are quoted in the note as "about".

Model (time-invariant matrices):
    state        a_t = T a_{t-1} + eta_t,   eta_t ~ N(0, Q)
    observation  y_t = Z_t a_t + eps_t,     eps_t ~ N(0, H)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<64s} {value:12.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


@dataclass
class FilterOutput:
    a_pred: np.ndarray  # a_{t|t-1}, shape (n, m)
    p_pred: np.ndarray  # P_{t|t-1}, shape (n, m, m)
    a_filt: np.ndarray  # a_{t|t}
    p_filt: np.ndarray  # P_{t|t}
    v: np.ndarray  # innovations y_t - Z_t a_{t|t-1}
    f: np.ndarray  # innovation variances
    loglik: float


def kalman_filter(
    y: np.ndarray, Z: np.ndarray, H: float, T: np.ndarray, Q: np.ndarray, a0: np.ndarray, p0: np.ndarray, burn: int = 0
) -> FilterOutput:
    """Univariate-observation Kalman filter; Z has shape (n, m). Log-likelihood skips the first ``burn`` terms."""
    n, m = Z.shape
    a_pred, p_pred = np.empty((n, m)), np.empty((n, m, m))
    a_filt, p_filt = np.empty((n, m)), np.empty((n, m, m))
    v, f = np.empty(n), np.empty(n)
    a, p = a0.astype(float), p0.astype(float)
    for t in range(n):
        # predict
        a = T @ a
        p = T @ p @ T.T + Q
        a_pred[t], p_pred[t] = a, p
        # update
        z = Z[t]
        v[t] = y[t] - z @ a
        pz = p @ z
        f[t] = z @ pz + H
        k = pz / f[t]
        a = a + k * v[t]
        p = p - np.outer(k, pz)
        a_filt[t], p_filt[t] = a, p
    ll = -0.5 * float(np.sum(np.log(2 * math.pi * f[burn:]) + v[burn:] ** 2 / f[burn:]))
    return FilterOutput(a_pred, p_pred, a_filt, p_filt, v, f, ll)


def rts_smoother(out: FilterOutput, T: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Rauch-Tung-Striebel: a_{t|n} = a_{t|t} + C_t (a_{t+1|n} - a_{t+1|t}), C_t = P_{t|t} T' P_{t+1|t}^{-1}."""
    n = out.a_filt.shape[0]
    a_s, p_s = out.a_filt.copy(), out.p_filt.copy()
    for t in range(n - 2, -1, -1):
        c = out.p_filt[t] @ T.T @ np.linalg.inv(out.p_pred[t + 1])
        a_s[t] = out.a_filt[t] + c @ (a_s[t + 1] - out.a_pred[t + 1])
        p_s[t] = out.p_filt[t] + c @ (p_s[t + 1] - out.p_pred[t + 1]) @ c.T
    return a_s, p_s


def local_level_loglik_grid(y: np.ndarray, q_grid: np.ndarray, h_grid: np.ndarray) -> np.ndarray:
    """Exact local-level log-likelihood on a grid of (Q, H), vectorised over the grid; diffuse start on y_0."""
    qq, hh = np.meshgrid(q_grid, h_grid, indexing="ij")
    a = np.full(qq.shape, y[0])
    p = hh.copy()  # after a diffuse prior is updated with y_0, P_{0|0} = H
    ll = np.zeros(qq.shape)
    for t in range(1, y.size):
        p_pred = p + qq
        f = p_pred + hh
        v = y[t] - a
        ll -= 0.5 * (np.log(2 * math.pi * f) + v**2 / f)
        k = p_pred / f
        a = a + k * v
        p = (1 - k) * p_pred
    return ll


def steady_state_local_level(q: float, h: float) -> tuple[float, float]:
    """Predicted steady-state variance P solves P = P H/(P+H) + Q; returns (P, K)."""
    r = q / h
    p = h * (r + math.sqrt(r * r + 4 * r)) / 2.0
    return p, p / (p + h)


# ---------------------------------------------------------------- sections


def one_step() -> None:
    print("\n# 1. One predict-update step of a local level model")
    print("#    backs: Worked example 1; card stat-kf-one-step-numeric")
    m, p, q, h, y = 100.0, 4.0, 1.0, 4.0, 103.0
    m_pred, p_pred = m, p + q
    f = p_pred + h
    k = p_pred / f
    check("predicted variance P- = P + Q", p_pred, 5.0, 1e-12)
    check("innovation variance F = P- + H", f, 9.0, 1e-12)
    check("Kalman gain K = P-/F", k, 0.5556, 1e-4)
    check("updated mean m + K (y - m)", m_pred + k * (y - m_pred), 101.6667, 1e-4)
    check("updated variance (1 - K) P-", (1 - k) * p_pred, 2.2222, 1e-4)
    check("precision check 1/P = 1/P- + 1/H", 1 / (1 / p_pred + 1 / h), 2.2222, 1e-4)


def steady_state() -> None:
    print("\n# 2. Steady state of the local level model and the EWMA equivalence")
    print("#    backs: Core concepts (steady state), Worked example 2; cards stat-kf-steady-state-gain-q01, stat-kf-arima011")
    for q, p_exp, k_exp in [(0.1, 0.3702, 0.2702), (0.01, 0.1051, 0.0951)]:
        p, k = steady_state_local_level(q, 1.0)
        check(f"q={q}: steady-state predicted P (H=1)", p, p_exp, 1e-4)
        check(f"q={q}: steady-state gain K", k, k_exp, 1e-4)
        # iterate the Riccati recursion from a diffuse start
        pp = 1e6
        for _ in range(200):
            pp = pp * 1.0 / (pp + 1.0) + q
        assert abs(pp - p) < 1e-10
    p, k = steady_state_local_level(0.1, 1.0)
    check("q=0.1: P + H, the denominator of K", p + 1.0, 1.3702, 1e-4)
    check("q=0.1: EWMA weight on history 1 - K", 1 - k, 0.7298, 1e-4)
    check("q=0.1: EWMA half-life ln 0.5 / ln(1-K) in observations", math.log(0.5) / math.log(1 - k), 2.2010, 1e-4)
    check("q=0.1: lag-1 autocorr of dy, -1/(q+2)", -1 / 2.1, -0.4762, 1e-4)
    theta = -(1 - k)
    check("q=0.1: ARIMA(0,1,1) theta = -(1-K), theta/(1+theta^2)", theta / (1 + theta**2), -0.4762, 1e-4)
    # filtered level equals an EWMA once P has converged
    rng = np.random.default_rng(3)
    level = np.cumsum(math.sqrt(0.1) * rng.standard_normal(300))
    y = level + rng.standard_normal(300)
    p_filt_ss = p * (1 - k)  # filtered steady state; the filter predicts first, P- = P + Q = p
    out = kalman_filter(y, np.ones((300, 1)), 1.0, np.eye(1), np.array([[0.1]]), np.array([y[0]]), np.array([[p_filt_ss]]))
    ewma = np.empty(300)
    prev = y[0]
    for t in range(300):
        prev = prev + k * (y[t] - prev)
        ewma[t] = prev
    check("max |Kalman filtered level - EWMA| (P started at steady state)", float(np.max(np.abs(out.a_filt[:, 0] - ewma))), 0.0, 1e-9)


def local_level_mle() -> None:
    print("\n# 3. Local level: MLE by prediction error decomposition (true Q = 0.1, H = 1, T = 500)")
    print("#    backs: Worked example 3; card stat-kf-likelihood")
    rng = np.random.default_rng(500)
    n = 500
    level = np.cumsum(math.sqrt(0.1) * rng.standard_normal(n))
    y = level + rng.standard_normal(n)
    q_grid = np.exp(np.linspace(math.log(0.01), math.log(1.0), 161))
    h_grid = np.exp(np.linspace(math.log(0.3), math.log(3.0), 161))
    ll = local_level_loglik_grid(y, q_grid, h_grid)
    i, j = np.unravel_index(np.argmax(ll), ll.shape)
    q_hat, h_hat = q_grid[i], h_grid[j]
    ll_true = local_level_loglik_grid(y, np.array([0.1]), np.array([1.0]))[0, 0]
    check("MLE Q (grid)", q_hat, 0.126, 0.0005)
    check("MLE H (grid)", h_hat, 0.976, 0.0005)
    check("max log-likelihood", float(ll[i, j]), -792.15, 0.005)
    check("log-likelihood at the true (0.1, 1)", ll_true, -792.59, 0.005)
    check("LR statistic 2 (ll_max - ll_true), chi2_2 5% cv 5.991", 2 * (float(ll[i, j]) - ll_true), 0.89, 0.005)
    # cross-check one grid point with the generic filter (burn the diffuse first step)
    out = kalman_filter(y, np.ones((n, 1)), 1.0, np.eye(1), np.array([[0.1]]), np.array([0.0]), np.array([[1e8]]), burn=1)
    check("generic filter log-likelihood at the truth (same value)", out.loglik, ll_true, 1e-4)
    a_s, _ = rts_smoother(out, np.eye(1))
    rmse_f = math.sqrt(float(np.mean((out.a_filt[:, 0] - level) ** 2)))
    rmse_s = math.sqrt(float(np.mean((a_s[:, 0] - level) ** 2)))
    check("RMSE of filtered level", rmse_f, 0.549, 0.0005)
    check("RMSE of smoothed level", rmse_s, 0.402, 0.0005)
    p_ss, _ = steady_state_local_level(0.1, 1.0)
    check("theory: steady-state filtered sd sqrt((1-K) P-)", math.sqrt(p_ss / (p_ss + 1.0)), 0.5198, 1e-4)


def simulate_hedge(seed: int = 2013, n: int = 1000, q_beta: float = 1e-4, h: float = 1.0, alpha: float = 0.0):
    """x a geometric random walk from 50 with 1% daily vol, beta_t a random walk from 1, y = alpha + beta_t x_t + eps."""
    rng = np.random.default_rng(seed)
    x = 50.0 * np.exp(np.cumsum(0.01 * rng.standard_normal(n)))
    beta = 1.0 + np.cumsum(math.sqrt(q_beta) * rng.standard_normal(n))
    y = alpha + beta * x + math.sqrt(h) * rng.standard_normal(n)
    return x, beta, y


def hedge_ratio() -> None:
    print("\n# 4. Time-varying hedge ratio: y_t = beta_t x_t + eps_t, beta_t a random walk (q = 1e-4, H = 1)")
    print("#    backs: Worked example 4; cards stat-kf-vs-rolling-ols, stat-kf-innovations-check, stat-kf-rts-smoother,")
    print("#    stat-kf-rls, stat-kf-intercept-collinearity")
    n, q_beta, h = 1000, 1e-4, 1.0
    x, beta, y = simulate_hedge()
    Z = x[:, None]
    T, Q = np.eye(1), np.array([[q_beta]])
    out = kalman_filter(y, Z, h, T, Q, np.zeros(1), np.array([[1e4]]), burn=1)
    b_f = out.a_filt[:, 0]
    a_s, p_s = rts_smoother(out, T)
    b_s = a_s[:, 0]
    sl = slice(100, n)  # score after a 100-day warm-up so every method has data
    roll = np.full(n, np.nan)
    w = 60
    for t in range(w - 1, n):
        xs, ys = x[t - w + 1 : t + 1], y[t - w + 1 : t + 1]
        roll[t] = float(xs @ ys / (xs @ xs))
    full = float(x @ y / (x @ x))
    rm = {
        "filtered": math.sqrt(float(np.mean((b_f[sl] - beta[sl]) ** 2))),
        "smoothed": math.sqrt(float(np.mean((b_s[sl] - beta[sl]) ** 2))),
        "rolling OLS 60": math.sqrt(float(np.mean((roll[sl] - beta[sl]) ** 2))),
        "full-sample OLS": math.sqrt(float(np.mean((full - beta[sl]) ** 2))),
    }
    check("x range: min", float(x.min()), 42.0, 0.05)
    check("x range: max", float(x.max()), 78.7, 0.05)
    check("true beta range: min", float(beta.min()), 0.896, 0.0005)
    check("true beta range: max", float(beta.max()), 1.271, 0.0005)
    for name, exp in {"filtered": 0.0108, "smoothed": 0.0088, "rolling OLS 60": 0.0375, "full-sample OLS": 0.0879}.items():
        check(f"RMSE of beta, {name}", rm[name], exp, 0.00005)
    check("RMSE ratio rolling OLS 60 / Kalman filter", rm["rolling OLS 60"] / rm["filtered"], 3.5, 0.05)
    z = (b_f - beta) / np.sqrt(out.p_filt[:, 0, 0])
    check("coverage of +-1.96 sd filtered bands", float(np.mean(np.abs(z[sl]) < 1.96)), 0.970, 0.0005)
    zs = (b_s - beta) / np.sqrt(p_s[:, 0, 0])
    check("coverage of +-1.96 sd smoothed bands", float(np.mean(np.abs(zs[sl]) < 1.96)), 0.962, 0.0005)
    e = out.v[sl] / np.sqrt(out.f[sl])
    check("standardised innovations: mean", float(e.mean()), 0.01, 0.005)
    check("standardised innovations: variance", float(e.var()), 0.92, 0.005)
    check("standardised innovations: lag-1 autocorrelation", float(np.corrcoef(e[1:], e[:-1])[0, 1]), -0.01, 0.005)
    check("filtered sd of beta at the end, sqrt(P)", math.sqrt(float(out.p_filt[-1, 0, 0])), 0.0096, 0.00005)

    # MLE of (q_beta, H) on a grid, vectorised over the grid (scalar state)
    lq = np.linspace(math.log(1e-5), math.log(1e-3), 81)
    lh = np.linspace(math.log(0.5), math.log(2.0), 81)
    qq, hh = (np.exp(g) for g in np.meshgrid(lq, lh, indexing="ij"))
    a = np.zeros(qq.shape)
    p = np.full(qq.shape, 1e4)
    ll = np.zeros(qq.shape)
    for t in range(n):
        p = p + qq
        f = p * x[t] ** 2 + hh
        v = y[t] - a * x[t]
        if t >= 1:
            ll -= 0.5 * (np.log(2 * math.pi * f) + v**2 / f)
        k = p * x[t] / f
        a = a + k * v
        p = p - k * x[t] * p
    i, j = np.unravel_index(np.argmax(ll), ll.shape)
    check("MLE q_beta x 1e4 (true 1)", float(qq[i, j]) * 1e4, 0.79, 0.005)
    check("MLE H (true 1)", float(hh[i, j]), 0.97, 0.005)
    # the vectorised grid and the generic filter agree at the true parameters
    k_true = int(np.argmin(np.abs(lq - math.log(q_beta))))
    j_true = int(np.argmin(np.abs(lh - math.log(h))))
    assert abs(qq[k_true, j_true] - q_beta) < 1e-12 and abs(hh[k_true, j_true] - h) < 1e-12
    check("log-likelihood at the truth: grid vs generic filter", float(ll[k_true, j_true]), out.loglik, 1e-6)

    # adding an intercept state makes alpha and beta nearly collinear (x stays near 50)
    Z2 = np.column_stack([np.ones(n), x])
    T2, Q2 = np.eye(2), np.diag([0.0, q_beta])
    out2 = kalman_filter(y, Z2, h, T2, Q2, np.zeros(2), np.diag([1e4, 1e4]), burn=1)
    check("with an intercept state: RMSE of filtered beta", math.sqrt(float(np.mean((out2.a_filt[sl, 1] - beta[sl]) ** 2))), 0.133, 0.0005)
    p_end = out2.p_filt[-1]
    corr_end = p_end[0, 1] / math.sqrt(p_end[0, 0] * p_end[1, 1])
    check("with an intercept state: posterior corr(alpha, beta) at the end", corr_end, -0.98, 0.005)

    # Q = 0 turns the filter into recursive least squares: the last filtered state is the OLS fit
    ols_fit = np.linalg.lstsq(Z2, y, rcond=None)[0]
    rls = kalman_filter(y, Z2, h, T2, np.zeros((2, 2)), np.zeros(2), np.diag([1e10, 1e10]))
    check("Q = 0: max |final filtered state - full-sample OLS|", float(np.max(np.abs(rls.a_filt[-1] - ols_fit))), 0.0, 1e-4)


if __name__ == "__main__":
    one_step()
    steady_state()
    local_level_mle()
    hedge_ratio()
    print("\nall kalman_filter checks passed")
