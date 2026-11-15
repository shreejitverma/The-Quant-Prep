"""Portfolio construction and risk parity: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/60-Systems/03-Portfolio-Construction-and-Risk-Parity.md`.
Independent routes used here:
- portfolio variance by the scalar expansion and by the matrix product, and marginal risk by central finite
  differences of sigma_p rather than the analytic gradient;
- equal-risk-contribution weights by a cyclical Newton solver on the risk-budget equations, compared with
  inverse-volatility weights;
- the minimum-variance and tangency formulas against a seeded random search over the budget hyperplane;
- the correlation distance's triangle inequality on random correlation matrices;
- sample-covariance rank by numpy's matrix rank on simulated data.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_sys_03_portfolio.py`.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261114


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def cov2(s1: float, s2: float, rho: float) -> np.ndarray:
    return np.array([[s1 * s1, rho * s1 * s2], [rho * s1 * s2, s2 * s2]])


def vol(w: np.ndarray, cov: np.ndarray) -> float:
    return math.sqrt(float(w @ cov @ w))


def risk_shares(w: np.ndarray, cov: np.ndarray) -> np.ndarray:
    """Risk contributions w_i dsigma/dw_i by central finite differences, as shares of sigma_p."""
    h = 1e-7
    grad = np.array([(vol(w + h * e, cov) - vol(w - h * e, cov)) / (2 * h) for e in np.eye(len(w))])
    trc = w * grad
    assert abs(trc.sum() - vol(w, cov)) < 1e-8  # Euler decomposition
    return trc / trc.sum()


def example1() -> None:
    print("Example 1: risk contributions of a 60/40 portfolio (cards mkt-sys-068, mkt-sys-069)")
    w = np.array([0.60, 0.40])
    cov = cov2(0.20, 0.05, 0.10)
    approx("sigma_E^2", cov[0, 0], 0.0400, 4)
    approx("sigma_B^2", cov[1, 1], 0.0025, 4)
    approx("sigma_EB", cov[0, 1], 0.0010, 4)
    approx("w_E^2 sigma_E^2", 0.36 * 0.04, 0.01440, 5)
    approx("w_B^2 sigma_B^2", 0.16 * 0.0025, 0.00040, 5)
    approx("2 w_E w_B sigma_EB", 2 * 0.6 * 0.4 * 0.001, 0.00048, 5)
    var = float(w @ cov @ w)
    approx("portfolio variance", var, 0.01528, 5)
    sp = math.sqrt(var)
    approx("portfolio vol (percent)", 100 * sp, 12.36, 2)
    approx("portfolio vol", sp, 0.1236, 4)
    sw = cov @ w
    approx("(Sigma w)_E", sw[0], 0.0244, 4)
    approx("(Sigma w)_B", sw[1], 0.0016, 4)
    approx("w_E (Sigma w)_E", 0.6 * sw[0], 0.01464, 5)
    approx("w_B (Sigma w)_B", 0.4 * sw[1], 0.00064, 5)
    shares = risk_shares(w, cov)
    approx("TRC_E (percent)", 100 * shares[0] * sp, 11.84, 2)
    approx("TRC_B (percent)", 100 * shares[1] * sp, 0.52, 2)
    approx("equity risk share (percent)", 100 * shares[0], 95.8, 1)
    approx("bond risk share (percent)", 100 * shares[1], 4.2, 1)


def sixty_forty() -> None:
    print("Core concepts 3: 60/40 with 16% and 5% volatility (card mkt-sys-071)")
    w = np.array([0.60, 0.40])
    for rho, q in ((-0.2, 99.8), (0.0, 95.8), (0.3, 90.9)):
        approx(f"equity risk share at rho = {rho} (percent)", 100 * risk_shares(w, cov2(0.16, 0.05, rho))[0], q, 1)
    approx("volatility ratio 16/5", 16 / 5, 3.2, 1)


def erc_solve(cov: np.ndarray) -> np.ndarray:
    """Equal risk contributions by cyclical Newton steps on w_i (Sigma w)_i = 1, then normalized."""
    n = len(cov)
    w = np.ones(n)
    for _ in range(200):
        for i in range(n):
            # Solve sigma_ii w_i^2 + b w_i - 1 = 0 for w_i > 0, with b = sum_{j != i} sigma_ij w_j.
            b = float(cov[i] @ w - cov[i, i] * w[i])
            w[i] = (-b + math.sqrt(b * b + 4 * cov[i, i])) / (2 * cov[i, i])
    return w / w.sum()


def example2() -> None:
    print("Example 2: equal risk contribution (cards mkt-sys-070, mkt-sys-077, mkt-sys-258)")
    for rho in (0.0, 0.10, 0.5, -0.3):
        w = erc_solve(cov2(0.20, 0.05, rho))
        approx(f"ERC equity weight at rho = {rho} (percent)", 100 * w[0], 20.0, 6)
        approx(f"ERC equity risk share at rho = {rho} (percent)", 100 * risk_shares(w, cov2(0.20, 0.05, rho))[0], 50.0, 5)
    sig = np.array([0.10, 0.20, 0.30])
    inv = (1 / sig) / (1 / sig).sum()
    equal = np.outer(sig, sig) * 0.3
    np.fill_diagonal(equal, sig**2)
    assert np.allclose(erc_solve(equal), inv, atol=1e-9)
    unequal = equal.copy()
    unequal[0, 1] = unequal[1, 0] = 0.8 * sig[0] * sig[1]
    assert np.max(np.abs(erc_solve(unequal) - inv)) > 0.01
    print("    inverse volatility equals ERC with equal correlations, not with unequal ones (3 assets)")


def frontier_formulas(rng: np.random.Generator) -> None:
    print("Minimum-variance and tangency formulas (cards mkt-sys-085, mkt-sys-091, mkt-sys-094)")
    sig = np.array([0.15, 0.20, 0.10])
    corr = np.array([[1.0, 0.4, 0.2], [0.4, 1.0, 0.3], [0.2, 0.3, 1.0]])
    cov = np.outer(sig, sig) * corr
    mu, rf = np.array([0.08, 0.10, 0.05]), 0.02
    one = np.ones(3)
    inv = np.linalg.inv(cov)
    w_mvp = inv @ one / (one @ inv @ one)
    w_tan = inv @ (mu - rf) / (one @ inv @ (mu - rf))
    draws = rng.normal(0, 1.5, size=(200_000, 3))
    draws = draws / draws.sum(axis=1, keepdims=True)
    draws = draws[np.abs(draws).max(axis=1) < 5]
    var_draws = np.einsum("ij,jk,ik->i", draws, cov, draws)
    sharpe = (draws @ mu - rf) / np.sqrt(var_draws)
    assert var_draws.min() >= float(w_mvp @ cov @ w_mvp) - 1e-12
    assert sharpe.max() <= float((w_tan @ mu - rf) / math.sqrt(w_tan @ cov @ w_tan)) + 1e-12
    print("    no random fully invested portfolio beats the closed-form MVP variance or tangency Sharpe")
    w = np.array([0.5, 0.3, 0.2])
    approx("rho = 1: sigma_p minus sum w_i sigma_i", vol(w, np.outer(sig, sig)) - float(w @ sig), 0.0, 12)


def distances_and_rank(rng: np.random.Generator) -> None:
    print("Correlation distance and sample-covariance rank (cards mkt-sys-076, mkt-sys-078)")
    for _ in range(200):
        x = rng.standard_normal((40, 6)) @ rng.standard_normal((6, 6))
        c = np.corrcoef(x, rowvar=False)
        d = np.sqrt(np.clip(0.5 * (1 - c), 0, None))
        for i in range(6):
            for j in range(6):
                assert np.all(d[i, j] <= d[i] + d[:, j] + 1e-12)
    print("    sqrt((1 - rho)/2) satisfies the triangle inequality on 200 random correlation matrices")
    n_assets, t_obs = 60, 50
    x = rng.standard_normal((t_obs, n_assets))
    s = np.cov(x, rowvar=False)
    rank = int(np.linalg.matrix_rank(s))
    assert rank == t_obs - 1, rank
    print(f"    sample covariance of {n_assets} assets over {t_obs} days has rank {rank} = T - 1")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    example1()
    sixty_forty()
    example2()
    frontier_formulas(rng)
    distances_and_rank(rng)
    print("all portfolio-construction numbers check out")
