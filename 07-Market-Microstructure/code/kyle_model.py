"""Kyle (1985): single-auction equilibrium, Monte Carlo check, and the sequential-auction recursion.

Backs every number in 04-Kyle-Model-and-Informed-Trading.md.
Run ``python kyle_model.py``: each result is printed and asserted.
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a labelled result and assert it is within tol of the expected value."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


def single_auction() -> None:
    print("== One-period Kyle model ==")
    p0, sigma_v, sigma_u = 100.0, 2.0, 10_000.0
    sigma0 = sigma_v**2
    lam = sigma_v / (2 * sigma_u)
    beta = sigma_u / sigma_v
    check("lambda ($ per share)", lam, 1e-4, 1e-15)
    check("beta (shares per $ of mispricing)", beta, 5_000.0, 1e-9)
    check("depth 1/lambda (shares per $1 move)", 1 / lam, 10_000.0, 1e-6)
    check("insider expected profit", sigma_v * sigma_u / 2, 10_000.0, 1e-9)
    check("noise traders expected loss lambda*sigma_u^2", lam * sigma_u**2, 10_000.0, 1e-6)
    check("posterior variance Var(v | y)", sigma0 / 2, 2.0, 1e-12)
    check("Var(order flow) / sigma_u^2", (beta**2 * sigma0 + sigma_u**2) / sigma_u**2, 2.0, 1e-12)

    # One realisation
    v, u = 103.0, -4_000.0
    x = beta * (v - p0)
    y = x + u
    p = p0 + lam * y
    check("insider order x", x, 15_000.0, 1e-9)
    check("total order flow y", y, 11_000.0, 1e-9)
    check("clearing price", p, 101.10, 1e-9)
    check("price move vs 3.00 of mispricing", p - p0, 1.10, 1e-9)
    check("insider realised profit", (v - p) * x, 28_500.0, 1e-6)

    # Deviations from beta, holding lambda fixed: E[profit] = b*Sigma0 - lam*b^2*Sigma0
    def profit(b: float) -> float:
        return b * sigma0 - lam * b**2 * sigma0

    check("profit at 2*beta", profit(2 * beta), 0.0, 1e-6)
    check("profit at beta/2", profit(beta / 2), 7_500.0, 1e-6)

    # Monte Carlo
    rng = np.random.default_rng(4)
    n = 1_000_000
    vs = p0 + sigma_v * rng.standard_normal(n)
    us = sigma_u * rng.standard_normal(n)
    ys = beta * (vs - p0) + us
    ps = p0 + lam * ys
    slope = float(np.cov(vs, ys)[0, 1] / ys.var())
    check("MC regression slope of v on y", slope, 9.994e-5, 1e-8)
    check("MC insider mean profit", float(np.mean((vs - ps) * beta * (vs - p0))), 9_982.0, 1.0)
    check("MC Var(v - p)", float(np.var(vs - ps)), 1.998, 1e-3)
    check("MC corr(p, v)^2", float(np.corrcoef(ps, vs)[0, 1] ** 2), 0.4997, 1e-4)

    # Doubling noise trading
    check("lambda with 2*sigma_u", sigma_v / (2 * 2 * sigma_u), 5e-5, 1e-15)
    check("profit with 2*sigma_u", sigma_v * 2 * sigma_u / 2, 20_000.0, 1e-9)


def solve_lambda(alpha: float, k: float) -> float:
    """Root of 2 k lam^2 (1 - alpha lam) = 1 - 2 alpha lam on (0, 1/(2 alpha)), the Kyle (1985) Theorem 2 cubic."""
    if alpha == 0.0:
        return 1.0 / math.sqrt(2.0 * k)
    lo, hi = 0.0, 1.0 / (2.0 * alpha)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = 2.0 * k * mid**2 * (1.0 - alpha * mid) - (1.0 - 2.0 * alpha * mid)
        if f < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def sequential(n_auctions: int, sigma_v: float = 1.0, sigma_u: float = 1.0) -> dict:
    """Backward recursion for N equally spaced auctions on [0, 1] with total noise variance sigma_u^2.

    Normalise Sigma_N = 1, solve backward, then rescale (lambda ~ sqrt(Sigma), alpha ~ 1/sqrt(Sigma),
    delta ~ sqrt(Sigma)) so that Sigma_0 = sigma_v^2.  Returns per-auction lambda and beta (forward order),
    the posterior variances Sigma_0..Sigma_N and the insider's ex-ante expected profit.
    """
    dt = 1.0 / n_auctions
    alpha, delta, sig = 0.0, 0.0, 1.0
    lams, sigmas = [], [sig]
    for _ in range(n_auctions):
        k = sigma_u**2 * dt / sig
        lam = solve_lambda(alpha, k)
        assert lam * (1 - alpha * lam) > 0, "second-order condition"
        new_alpha = 1.0 / (4.0 * lam * (1.0 - alpha * lam))
        delta = delta + alpha * lam**2 * sigma_u**2 * dt
        sig = sig / (1.0 - k * lam**2)
        alpha = new_alpha
        lams.append(lam)
        sigmas.append(sig)
    scale = sigma_v**2 / sig
    root = math.sqrt(scale)
    lams = [lam * root for lam in reversed(lams)]
    sigmas = [s * scale for s in reversed(sigmas)]
    betas = [lam * sigma_u**2 / sigmas[i + 1] for i, lam in enumerate(lams)]  # Kyle: lambda_n = beta_n Sigma_n / sigma_u^2
    profit = (alpha / root) * sigma_v**2 + delta * root
    return {"lambdas": lams, "betas": betas, "sigmas": sigmas, "profit": profit, "dt": dt}


def forward_check(res: dict, sigma_u: float = 1.0) -> None:
    """Recompute each lambda_n and Sigma_n from the Bayesian update given beta_n: they must match."""
    dt, sig = res["dt"], res["sigmas"][0]
    for lam, beta, sig_next in zip(res["lambdas"], res["betas"], res["sigmas"][1:], strict=True):
        var_y = beta**2 * dt**2 * sig + sigma_u**2 * dt
        assert abs(beta * dt * sig / var_y - lam) < 1e-9
        sig = sig * sigma_u**2 * dt / var_y
        assert abs(sig - sig_next) < 1e-9


def monte_carlo_profit(res: dict, n_paths: int, seed: int, sigma_v: float = 1.0, sigma_u: float = 1.0) -> float:
    """Simulate the insider trading x_n = beta_n (v - p_{n-1}) dt against the equilibrium lambdas."""
    rng = np.random.default_rng(seed)
    dt = res["dt"]
    v = sigma_v * rng.standard_normal(n_paths)
    p = np.zeros(n_paths)
    profit = np.zeros(n_paths)
    for lam, beta in zip(res["lambdas"], res["betas"], strict=True):
        x = beta * (v - p) * dt
        p = p + lam * (x + sigma_u * math.sqrt(dt) * rng.standard_normal(n_paths))
        profit += (v - p) * x
    return float(profit.mean())


def multi_period() -> None:
    print("== Sequential auctions (sigma_v = sigma_u = 1) ==")
    expected = {
        1: (0.5, 0.5, 0.5),
        2: (0.6529, 0.3460, 0.6206),
        4: (0.7648, 0.2206, 0.7307),
        10: (0.8653, 0.1099, 0.8439),
        100: (0.9745, 0.0138, 0.9714),
        1000: (0.9962, 0.0014, 0.9959),
    }
    for n, (l1, se, pr) in expected.items():
        r = sequential(n)
        forward_check(r)
        check(f"N={n} lambda_1", r["lambdas"][0], l1, 1e-4)
        check(f"N={n} Sigma_N/Sigma_0", r["sigmas"][-1], se, 1e-4)
        check(f"N={n} profit", r["profit"], pr, 1e-4)
    mc = monte_carlo_profit(sequential(2), 2_000_000, seed=5)
    check("N=2 Monte Carlo insider profit", mc, 0.6205, 1e-4)
    mc10 = monte_carlo_profit(sequential(10), 1_000_000, seed=6)
    check("N=10 Monte Carlo insider profit", mc10, 0.8438, 1e-4)


if __name__ == "__main__":
    single_auction()
    multi_period()
    print("all Kyle model checks passed")
