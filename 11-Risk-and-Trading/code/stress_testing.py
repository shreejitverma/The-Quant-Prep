"""Stress testing: hypothetical and historical scenarios, conditional expansion, plausibility, reverse stress tests.

Backs every number in 11-Risk-and-Trading/04-Stress-Testing-and-Scenarios.md.

Every position, covariance and scenario below is a labelled teaching input, not market data.
Reverse stress testing is solved as an optimisation: find the most plausible factor move (smallest Mahalanobis
distance under a reference covariance) whose loss reaches a threshold, in closed form for a linear book and
numerically (with a brute-force check) for an option book revalued in full.

Run: python 11-Risk-and-Trading/code/stress_testing.py
"""

from __future__ import annotations

import math

import numpy as np

SQRT2 = math.sqrt(2.0)


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.6f}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def bs_price(kind: str, s: float, k: float, vol: float, tau: float, r: float = 0.0) -> float:
    if tau <= 0.0:
        return max(s - k, 0.0) if kind == "call" else max(k - s, 0.0)
    sq = vol * math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * tau) / sq
    d2 = d1 - sq
    if kind == "call":
        return s * ncdf(d1) - k * math.exp(-r * tau) * ncdf(d2)
    return k * math.exp(-r * tau) * ncdf(-d2) - s * ncdf(-d1)


def bs_delta(kind: str, s: float, k: float, vol: float, tau: float, r: float = 0.0) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * tau) / (vol * math.sqrt(tau))
    return ncdf(d1) if kind == "call" else ncdf(d1) - 1.0


def chi2_sf_even(q: float, df: int) -> float:
    """P(chi^2_df > q) for even df: exp(-q/2) sum_{j < df/2} (q/2)^j / j!."""
    assert df % 2 == 0
    half = q / 2.0
    return math.exp(-half) * sum(half**j / math.factorial(j) for j in range(df // 2))


# ---------------------------------------------------------------------------
# Example 1: a hypothetical multi-asset scenario, linear and with an option overlay
# ---------------------------------------------------------------------------

FACTORS = ("equity", "ust10y_bp", "oil", "hy_bp")
# One-month factor vols and correlations: labelled hypothetical inputs for the plausibility calculations.
VOLS = np.array([0.045, 25.0, 0.09, 40.0])
CORR = np.array(
    [
        [1.0, 0.3, 0.3, -0.7],
        [0.3, 1.0, 0.2, -0.3],
        [0.3, 0.2, 1.0, -0.3],
        [-0.7, -0.3, -0.3, 1.0],
    ]
)
COV = CORR * np.outer(VOLS, VOLS)
STAGFLATION = np.array([-0.18, 85.0, 0.35, 140.0])


def linear_pnl(x: np.ndarray) -> dict[str, float]:
    """$200m equities at beta 1.15, Treasuries with DV01 $110k, 500,000 bbl of crude at $80, CDX HY protection sold, CS01 $42k."""
    return {
        "equity": 200e6 * 1.15 * x[0],
        "rates": -110_000.0 * x[1],
        "oil": 500_000.0 * 80.0 * x[2],
        "credit": -42_000.0 * x[3],
    }


def put_overlay_pnl(eq_move: float, vol_move: float) -> float:
    """Long 3-month 90%-strike index puts on $200m notional: S = 100, vol 18%, revalued after one month."""
    qty = 200e6 / 100.0
    v0 = bs_price("put", 100.0, 90.0, 0.18, 0.25)
    v1 = bs_price("put", 100.0 * (1.0 + eq_move), 90.0, 0.18 + vol_move, 0.25 - 1.0 / 12.0)
    return qty * (v1 - v0)


def section_example_1() -> None:
    print("\n[Worked example 1: hypothetical stagflation scenario]")
    legs = linear_pnl(STAGFLATION)
    for name, v in legs.items():
        print(f"  {name:<7} {v / 1e6:+.2f}m")
    total = sum(legs.values())
    check("equity leg (m)", legs["equity"] / 1e6, -41.40, 1e-9)
    check("rates leg (m)", legs["rates"] / 1e6, -9.35, 1e-9)
    check("oil leg (m)", legs["oil"] / 1e6, 14.00, 1e-9)
    check("credit leg (m)", legs["credit"] / 1e6, -5.88, 1e-9)
    check("total (m)", total / 1e6, -42.63, 1e-9)
    z = STAGFLATION / VOLS
    for got, want in zip(z, (-4.0, 3.4, 3.89, 3.5), strict=True):
        assert abs(got - want) < 5e-3, f"z-score {got} vs {want}"
    d2 = float(STAGFLATION @ np.linalg.solve(COV, STAGFLATION))
    print(f"  z-scores {np.round(z, 2)}, Mahalanobis distance {math.sqrt(d2):.3f}")
    check("Mahalanobis distance of the scenario", math.sqrt(d2), 8.189, 5e-4)
    check("P(chi^2_4 > d^2) x 1e13: share of one-month moves at least this far out", chi2_sf_even(d2, 4) * 1e13, 0.947, 5e-4)
    expo = np.array([200e6 * 1.15, -110_000.0, 40e6, -42_000.0])
    sigma_p = math.sqrt(float(expo @ COV @ expo))
    check("one-month P&L standard deviation of the book (m)", sigma_p / 1e6, 12.529, 5e-4)
    check("scenario loss in book sigmas", total / sigma_p, -3.402, 5e-4)
    print("  put overlay revalued in full, scenario severity scaled (equity move, +vol points):")
    rows = []
    for scale in (0.5, 1.0, 2.0):
        lin = sum(linear_pnl(scale * STAGFLATION).values())
        put = put_overlay_pnl(scale * STAGFLATION[0], scale * 0.15)
        rows.append((scale, lin, put))
        print(f"  x{scale:<3} linear {lin / 1e6:+8.2f}m, puts {put / 1e6:+7.2f}m, total {(lin + put) / 1e6:+8.2f}m")
    check("put overlay at 0.5x severity (m)", rows[0][2] / 1e6, 5.54, 5e-3)
    check("put overlay at 1x (m)", rows[1][2] / 1e6, 18.34, 5e-3)
    check("put overlay at 2x (m)", rows[2][2] / 1e6, 51.48, 5e-3)
    check("total at 1x with puts (m)", (rows[1][1] + rows[1][2]) / 1e6, -24.29, 5e-3)
    check("total at 2x with puts (m)", (rows[2][1] + rows[2][2]) / 1e6, -33.78, 5e-3)
    check("total at 0.5x with puts (m)", (rows[0][1] + rows[0][2]) / 1e6, -15.78, 5e-3)
    check("2x / 1x hedged loss", (rows[2][1] + rows[2][2]) / (rows[1][1] + rows[1][2]), 1.39, 5e-3)


# ---------------------------------------------------------------------------
# Historical replay: absolute against relative shocks
# ---------------------------------------------------------------------------


def section_replay() -> None:
    print("\n[Core concepts: replaying a historical rate move at today's level]")
    then_level, then_move, today = 0.040, -0.015, 0.010
    absolute = today + then_move
    relative = today * (then_level + then_move) / then_level
    print(f"  yield fell {then_move * 1e4:.0f}bp from {then_level:.1%}; today {today:.1%}")
    check("absolute replay: today's yield after the shock", absolute, -0.005, 1e-12)
    check("relative replay: today's yield after the shock", relative, 0.00625, 1e-12)
    check("relative replay move (bp)", (relative - today) * 1e4, -37.5, 1e-9)


# ---------------------------------------------------------------------------
# Conditional scenario expansion
# ---------------------------------------------------------------------------


def section_conditional() -> None:
    print("\n[Core concepts: conditional expansion from equity and rates to oil and HY]")
    i1, i2 = [0, 1], [2, 3]
    s11 = COV[np.ix_(i1, i1)]
    s21 = COV[np.ix_(i2, i1)]
    s22 = COV[np.ix_(i2, i2)]
    shock = STAGFLATION[i1]
    cond_mean = s21 @ np.linalg.solve(s11, shock)
    cond_cov = s22 - s21 @ np.linalg.solve(s11, s21.T)
    cond_sd = np.sqrt(np.diag(cond_cov))
    print(f"  given equity -18% and 10y +85bp: E[oil] {cond_mean[0]:+.4f}, E[HY] {cond_mean[1]:+.2f}bp")
    print(f"  conditional sd: oil {cond_sd[0]:.4f}, HY {cond_sd[1]:.2f}bp")
    check("conditional mean oil move", cond_mean[0], -0.0580, 5e-5)
    check("conditional mean HY move (bp)", cond_mean[1], 93.80, 5e-3)
    check("conditional sd oil", cond_sd[0], 0.0852, 5e-5)
    check("conditional sd HY (bp)", cond_sd[1], 28.32, 5e-3)
    check("hypothetical oil +35% in conditional sds", (0.35 - cond_mean[0]) / cond_sd[0], 4.79, 5e-3)


# ---------------------------------------------------------------------------
# Reverse stress testing
# ---------------------------------------------------------------------------


def reverse_linear(delta: np.ndarray, cov: np.ndarray, loss: float) -> tuple[np.ndarray, float]:
    """argmin x' cov^-1 x subject to delta' x = -loss: x* = -loss cov delta / (delta' cov delta), distance loss / sigma_P."""
    sp2 = float(delta @ cov @ delta)
    return -loss * (cov @ delta) / sp2, loss / math.sqrt(sp2)


STRANGLE_S0, STRANGLE_VOL, STRANGLE_T, HORIZON = 100.0, 0.20, 1.0 / 12.0, 10.0 / 365.0
REV_VOLS = np.array([0.20 * math.sqrt(10.0 / 252.0), 0.03])  # 10-day equity log-return sd, implied vol change sd
REV_RHO = -0.7
REV_COV = np.array([[REV_VOLS[0] ** 2, REV_RHO * REV_VOLS[0] * REV_VOLS[1]], [REV_RHO * REV_VOLS[0] * REV_VOLS[1], REV_VOLS[1] ** 2]])


def strangle_pnl(x: np.ndarray) -> float:
    """Short 100,000 95-puts and 100,000 105-calls (1 month, vol 20%), stock-hedged at inception; 10-day full revaluation."""
    s0, v0, t = STRANGLE_S0, STRANGLE_VOL, STRANGLE_T
    hedge = 100_000.0 * (bs_delta("put", s0, 95.0, v0, t) + bs_delta("call", s0, 105.0, v0, t))
    s1 = s0 * math.exp(x[0])
    v1 = max(v0 + x[1], 0.01)
    opt = -100_000.0 * (bs_price("put", s1, 95.0, v1, t - HORIZON) - bs_price("put", s0, 95.0, v0, t))
    opt += -100_000.0 * (bs_price("call", s1, 105.0, v1, t - HORIZON) - bs_price("call", s0, 105.0, v0, t))
    return opt + hedge * (s1 - s0)


def _radius_on_ray(loss_fn, u: np.ndarray, chol: np.ndarray, loss: float, r_max: float = 12.0) -> float:
    """Smallest Mahalanobis radius r along whitened direction u at which the loss reaches `loss` (inf if never)."""
    grid = np.linspace(0.0, r_max, 241)
    vals = [-loss_fn(chol @ (r * u)) for r in grid]
    for i in range(1, len(grid)):
        if vals[i] >= loss:
            lo, hi = grid[i - 1], grid[i]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                lo, hi = (lo, mid) if -loss_fn(chol @ (mid * u)) >= loss else (mid, hi)
            return 0.5 * (lo + hi)
    return math.inf


def reverse_full_bruteforce(loss_fn, cov: np.ndarray, loss: float, n_angles: int = 1440) -> tuple[np.ndarray, float]:
    """2-factor reverse stress by brute force: minimise the ray radius over a dense grid of whitened directions."""
    chol = np.linalg.cholesky(cov)
    best_r, best_u = math.inf, None
    for th in np.linspace(0.0, 2.0 * math.pi, n_angles, endpoint=False):
        u = np.array([math.cos(th), math.sin(th)])
        r = _radius_on_ray(loss_fn, u, chol, loss)
        if r < best_r:
            best_r, best_u = r, u
    return chol @ (best_r * best_u), best_r


def reverse_full_iterative(loss_fn, cov: np.ndarray, loss: float, y0: np.ndarray, iters: int = 60) -> tuple[np.ndarray, float]:
    """Fixed-point solver: at the optimum the whitened scenario is parallel to the gradient of the loss.

    Iterate y <- r(u) u with u = grad(loss)(y) / |grad|, r(u) the radius on that ray where the loss hits the threshold.
    Gradients by central differences in the whitened coordinates.
    """
    chol = np.linalg.cholesky(cov)
    y = y0.copy()
    for _ in range(iters):
        g = np.zeros_like(y)
        for i in range(len(y)):
            e = np.zeros_like(y)
            e[i] = 1e-5
            g[i] = (-loss_fn(chol @ (y + e)) + loss_fn(chol @ (y - e))) / 2e-5
        u = g / np.linalg.norm(g)
        r = _radius_on_ray(loss_fn, u, chol, loss)
        y_new = r * u
        if np.linalg.norm(y_new - y) < 1e-10:
            y = y_new
            break
        y = y_new
    return chol @ y, float(np.linalg.norm(y))


def section_reverse() -> None:
    print("\n[Core concepts and worked example 2: reverse stress tests]")
    delta = np.array([200e6 * 1.15, -110_000.0, 40e6, -42_000.0])
    x_star, k_star = reverse_linear(delta, COV, 40e6)
    print(f"  linear book, 40m loss: x* = {np.round(x_star, 4)}, distance {k_star:.3f}")
    check("distance of the most plausible 40m-loss scenario (sigmas)", k_star, 3.192, 5e-4)
    check("its equity move", x_star[0], -0.1351, 5e-5)
    check("its 10y move (bp)", x_star[1], -10.06, 5e-3)
    check("its oil move", x_star[2], -0.1527, 5e-5)
    check("its HY move (bp)", x_star[3], 93.56, 5e-3)
    check("loss of x* (m), equals the threshold", -float(delta @ x_star) / 1e6, 40.0, 1e-9)
    check("1-d tail P(Z > k*)", 1.0 - ncdf(k_star), 7.05e-4, 5e-7)
    check("ellipsoid tail P(chi^2_4 > k*^2)", chi2_sf_even(k_star**2, 4), 0.0373, 5e-5)
    check("ratio of the two tails", chi2_sf_even(k_star**2, 4) / (1.0 - ncdf(k_star)), 52.9, 0.05)
    # Any other scenario on the loss boundary is further out: check against random boundary points.
    rng = np.random.default_rng(3)
    inv = np.linalg.inv(COV)
    for _ in range(2000):
        x = rng.standard_normal(4) * VOLS * 3
        x = x * (-40e6 / float(delta @ x)) if float(delta @ x) < 0 else -x * (40e6 / float(delta @ x))
        assert math.sqrt(float(x @ inv @ x)) >= k_star - 1e-9
    print("  2,000 random scenarios with the same loss are all further out than x*")

    print("  short strangle, 10-day horizon, loss threshold 1.0m, full revaluation:")
    base_loss = 1.0e6
    h = 1e-5
    g_lin = np.array(
        [
            (strangle_pnl(np.array([h, 0.0])) - strangle_pnl(np.array([-h, 0.0]))) / (2 * h),
            (strangle_pnl(np.array([0.0, h])) - strangle_pnl(np.array([0.0, -h]))) / (2 * h),
        ]
    )
    x_lin, k_lin = reverse_linear(g_lin, REV_COV, base_loss)
    x_bf, k_bf = reverse_full_bruteforce(strangle_pnl, REV_COV, base_loss)
    # Multi-start: the fixed-point iteration finds a local optimum, so start it from the linear answer and from
    # each whitened axis direction, then keep the closest.
    chol = np.linalg.cholesky(REV_COV)
    starts = [np.linalg.solve(chol, x_lin)] + [3.0 * v for v in (np.array([1.0, 0.0]), np.array([-1.0, 0.0]))]
    local = [reverse_full_iterative(strangle_pnl, REV_COV, base_loss, y0) for y0 in starts]
    for x_loc, k_loc in local:
        print(f"  local optimum from a start: x = ({x_loc[0]:+.4f}, {x_loc[1]:+.4f}), distance {k_loc:.4f}")
    x_it, k_it = min(local, key=lambda pair: pair[1])
    crash = min((pair for pair in local if pair[0][0] < 0.0), key=lambda pair: pair[1])
    check("crash-side local optimum distance", crash[1], 4.285, 5e-4)
    check("crash-side equity move", crash[0][0], -0.1707, 5e-4)
    check("crash-side vol move", crash[0][1], 0.0911, 5e-4)
    print(f"  linear (delta-vega) answer: x = ({x_lin[0]:+.4f}, {x_lin[1]:+.4f}), distance {k_lin:.3f}, "
          f"full-reval loss there {-strangle_pnl(x_lin) / 1e6:.3f}m")  # fmt: skip
    print(f"  brute force: x = ({x_bf[0]:+.4f}, {x_bf[1]:+.4f}), distance {k_bf:.4f}")
    print(f"  fixed-point solver: x = ({x_it[0]:+.4f}, {x_it[1]:+.4f}), distance {k_it:.4f}")
    check("10-day equity log-return sd", REV_VOLS[0], 0.0398, 5e-5)
    check("strangle equity sensitivity per unit log-return (m)", g_lin[0] / 1e6, 0.0485, 5e-5)
    check("strangle vega per unit vol (m)", g_lin[1] / 1e6, -1.078, 5e-4)
    check("linear reverse-stress distance", k_lin, 29.642, 5e-4)
    check("full-revaluation reverse-stress distance (brute force)", k_bf, 3.875, 2e-3)
    check("fixed-point solver distance", k_it, k_bf, 1e-3)
    check("most plausible equity move", x_it[0], 0.1544, 5e-4)
    check("most plausible vol move", x_it[1], -0.0814, 5e-4)
    check("loss at the fixed-point answer (m)", -strangle_pnl(x_it) / 1e6, 1.0, 1e-6)
    check("full-revaluation loss at the linear answer (m)", -strangle_pnl(x_lin) / 1e6, 5.31, 5e-3)
    # The equity factor is a log return: convert each answer to the price move a trader would quote.
    check("linear answer equity log return", x_lin[0], -0.8605, 5e-5)
    check("linear answer vol move", x_lin[1], 0.8885, 5e-5)
    check("linear answer price move exp(x) - 1", math.exp(x_lin[0]) - 1.0, -0.577, 5e-4)
    check("most plausible price move exp(x) - 1", math.exp(x_it[0]) - 1.0, 0.167, 5e-4)
    check("crash-side price move exp(x) - 1", math.exp(crash[0][0]) - 1.0, -0.157, 5e-4)


# ---------------------------------------------------------------------------
# Liquidity: economic P&L against cash
# ---------------------------------------------------------------------------


def section_liquidity() -> None:
    print("\n[Core concepts: margin cash against economic P&L]")
    s0, k, vol, t = 100.0, 100.0, 0.25, 0.25
    qty = 1_000_000.0  # long OTC calls on 1m shares, no collateral exchanged on the option
    delta0 = bs_delta("call", s0, k, vol, t)
    fut = -qty * delta0  # short futures hedge, daily variation margin
    s1 = 110.0
    opt_gain = qty * (bs_price("call", s1, k, vol, t - 1.0 / 365.0) - bs_price("call", s0, k, vol, t))
    vm = fut * (s1 - s0)
    print(f"  hedge {fut:,.0f} futures-equivalent shares; +10% day: option MTM {opt_gain / 1e6:+.3f}m, futures VM {vm / 1e6:+.3f}m")
    check("option delta at inception", delta0, 0.5249, 5e-5)
    check("option mark-to-market gain (m)", opt_gain / 1e6, 6.676, 5e-4)
    check("futures variation margin paid (m)", vm / 1e6, -5.249, 5e-4)
    check("economic P&L (m)", (opt_gain + vm) / 1e6, 1.427, 5e-4)


def section_correlation() -> None:
    print("\n[Core concepts: what correlation stress does to a diversified book]")
    n, w, vol = 10, 0.1, 0.20
    for rho in (0.3, 0.9):
        port_vol = vol * math.sqrt(n * w * w + n * (n - 1) * w * w * rho)
        print(f"  10 equal-weight assets at 20% vol, rho {rho}: portfolio vol {port_vol:.4f}")
    check("portfolio vol at rho 0.3", vol * math.sqrt(0.1 + 0.9 * 0.3), 0.1217, 5e-5)
    check("portfolio vol at rho 0.9", vol * math.sqrt(0.1 + 0.9 * 0.9), 0.1908, 5e-5)
    check("VaR multiplier from the correlation stress", math.sqrt(0.1 + 0.9 * 0.9) / math.sqrt(0.1 + 0.9 * 0.3), 1.568, 5e-4)


def main() -> None:
    section_example_1()
    section_replay()
    section_conditional()
    section_reverse()
    section_liquidity()
    section_correlation()
    print("\nAll stress testing checks passed.")


if __name__ == "__main__":
    main()
