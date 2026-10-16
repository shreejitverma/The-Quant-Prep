"""Transaction costs, turnover and dynamic trading toward an aim portfolio, on numbers.

Backs 09-Alpha-Research-and-Portfolio/13-Transaction-Costs-and-Turnover.md.

1. Per-trade cost: half-spread + fees + square-root impact, and how splitting an order
   changes linear, 3/2-power and quadratic cost.
2. Alpha decay versus impact: the best number of days to work an order.
3. One asset, one period: the optimal trade under linear, quadratic and 3/2-power costs,
   each confirmed by brute-force maximisation.
4. Several assets with quadratic costs: w = (lambda Sigma + C)^-1 (alpha + C w0),
   a matrix-weighted average of the frictionless target and the current book.
5. Garleanu-Pedersen (2013): closed-form trading rate a / lambda and aim portfolio, confirmed
   by value iteration on the linear-quadratic Bellman equation, by the weighted-average-of-
   future-Markowitz identity, and by a direct search over linear trading rules.
6. Simulation with a mean-reverting signal: no trading, full rebalancing to Markowitz,
   partial adjustment toward Markowitz, and the Garleanu-Pedersen rule.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/costs_turnover.py
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> None:
    print(f"{label}: {value:{fmt}}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    if expected != 0:  # the printed value must equal the literal the note quotes, at the printed rounding
        assert f"{value:{fmt}}" == f"{expected:{fmt}}", f"{label}: prints {value:{fmt}}, note quotes {expected:{fmt}}"


# ---------------------------------------------------------------------------
# 1. Per-trade cost model
# ---------------------------------------------------------------------------


def trade_cost_bp(participation: float, half_spread_bp: float, fee_bp: float, daily_vol: float, y_coef: float) -> float:
    """One-way cost in bp of traded value: half-spread + fees + Y * sigma * sqrt(Q / V)."""
    return half_spread_bp + fee_bp + 1e4 * y_coef * daily_vol * math.sqrt(participation)


def section_cost_model() -> None:
    print("\n== 1. Per-trade cost model ==")
    sigma, y_coef, hs, fee = 0.015, 1.0, 2.0, 0.5
    c1 = trade_cost_bp(0.01, hs, fee, sigma, y_coef)
    c10 = trade_cost_bp(0.10, hs, fee, sigma, y_coef)
    check("impact at 1% of ADV (bp)", 1e4 * y_coef * sigma * math.sqrt(0.01), 15.0, 1e-9, ".2f")
    check("impact at 10% of ADV (bp)", 1e4 * y_coef * sigma * math.sqrt(0.10), 47.43, 0.01, ".2f")
    check("cost at 1% of ADV (bp)", c1, 17.5, 1e-9, ".2f")
    check("cost at 10% of ADV (bp)", c10, 49.93, 0.01, ".2f")
    check("dollar cost of $5m at 1% of ADV", 5e6 * c1 / 1e4, 8750.0, 1e-6, ".0f")
    # Splitting an order of 8% of ADV into n equal daily pieces (impact resets each day).
    q = 0.08
    one_day = y_coef * sigma * math.sqrt(q) * 1e4
    four_day = y_coef * sigma * math.sqrt(q / 4) * 1e4
    check("sqrt impact, 8% ADV in one day (bp)", one_day, 42.43, 0.01, ".2f")
    check("sqrt impact, 2% ADV on each of 4 days (bp)", four_day, 21.21, 0.01, ".2f")
    # Total cost relative to trading in one day: linear n*(Q/n) = Q, 3/2 power n*(Q/n)^1.5, quadratic n*(Q/n)^2.
    per_unit = {
        "linear": lambda x: (hs + fee) / 1e4,  # spread and fees: cost per unit does not depend on size
        "3/2-power": lambda x: y_coef * sigma * math.sqrt(x),  # square-root impact
        "quadratic": lambda x: 0.5 * x,  # linear (Almgren-Chriss temporary) impact, any slope
    }

    def total_cost(shape: str, pieces: int) -> float:
        return sum(per_unit[shape](q / pieces) * (q / pieces) for _ in range(pieces))

    for shape, exp in [("linear", 1.0), ("3/2-power", 0.5), ("quadratic", 0.25)]:
        check(f"{shape} cost ratio, 4 days vs 1", total_cost(shape, 4) / total_cost(shape, 1), exp, 1e-12, ".2f")
    # Amortisation: 4% annual alpha, 40 bp round trip.
    check("weekly alpha of a 4%/yr signal (%)", 4.0 / 52, 0.077, 5e-4, ".3f")
    check("round-trip cost as a fraction of alpha, 1-year hold", 0.40 / 4.0, 0.10, 1e-12, ".2f")
    check("round-trip cost as a multiple of alpha, 1-week hold", 0.40 / (4.0 / 52), 5.2, 1e-9, ".2f")


# ---------------------------------------------------------------------------
# 2. Alpha decay versus impact: how many days to work an order
# ---------------------------------------------------------------------------


def section_alpha_decay() -> None:
    print("\n== 2. Alpha decay versus impact ==")
    alpha_bp, half_life, q, y_sigma = 60.0, 5.0, 0.10, 0.015
    delta = 0.5 ** (1 / half_life)
    check("daily alpha retention delta", delta, 0.8706, 1e-4)
    check("alpha lost per day of delay (%)", 100 * (1 - delta), 12.94, 0.01, ".2f")

    def net_bp(n: int) -> tuple[float, float, float]:
        captured = alpha_bp * (1 - delta**n) / (n * (1 - delta))  # piece k earns alpha * delta^k
        impact = 1e4 * y_sigma * math.sqrt(q / n)  # each daily piece is q/n of ADV
        return captured, impact, captured - impact

    for n, (cap, imp, net) in [(1, (60.0, 47.43, 12.57)), (4, (49.32, 23.72, 25.61)), (10, (34.76, 15.0, 19.76))]:
        got = net_bp(n)
        check(f"n={n:2d} days: alpha captured (bp)", got[0], cap, 0.01, ".2f")
        check(f"n={n:2d} days: impact (bp)", got[1], imp, 0.01, ".2f")
        check(f"n={n:2d} days: net (bp)", got[2], net, 0.01, ".2f")
    best = max(range(1, 31), key=lambda k: net_bp(k)[2])
    check("best number of days", best, 4, 0)


# ---------------------------------------------------------------------------
# 3. One asset, one period, three cost shapes
# ---------------------------------------------------------------------------


def brute_force_argmax(f, lo: float, hi: float) -> float:
    grid = np.linspace(lo, hi, 200_001)
    return float(grid[np.argmax(f(grid))])


def section_cost_shapes() -> None:
    print("\n== 3. One asset, one period: linear vs quadratic vs 3/2-power cost ==")
    mu, sigma, lam = 0.05, 0.20, 5.0
    lv = lam * sigma**2  # 0.2
    check("frictionless target mu/(lambda sigma^2)", mu / lv, 0.25, 1e-12)
    c_lin, kappa, k32 = 0.01, 0.2, 0.05
    # kappa and k32 are calibrated so the 0.25 trade costs the same: kappa/2*0.25^2 = k32*0.25^1.5
    check("quadratic cost of a 0.25 trade", kappa / 2 * 0.25**2, 0.00625, 1e-12, ".5f")
    check("3/2-power cost of a 0.25 trade", k32 * 0.25**1.5, 0.00625, 1e-12, ".5f")

    check("no-trade band lower edge (mu - c)/(lambda sigma^2)", (mu - c_lin) / lv, 0.20, 1e-12)
    check("no-trade band upper edge (mu + c)/(lambda sigma^2)", (mu + c_lin) / lv, 0.30, 1e-12)

    def util(w, w0, cost):
        return mu * w - 0.5 * lv * w**2 - cost(np.abs(w - w0))

    for w0, lin_exp, quad_exp, p32_exp in [(0.0, 0.20, 0.125, 0.1201), (0.27, 0.27, 0.26, 0.2678)]:
        # Linear: no-trade band [(mu - c)/lv, (mu + c)/lv]; trade to the nearest edge.
        w_lin = min(max(w0, (mu - c_lin) / lv), (mu + c_lin) / lv)
        # Quadratic: w = (mu + kappa w0) / (lv + kappa).
        w_quad = (mu + kappa * w0) / (lv + kappa)
        # 3/2 power: FOC mu - lv w - 1.5 k32 sqrt(|w - w0|) sign(w - w0) = 0, solved by bisection on d = w - w0.
        target = mu / lv
        sgn = 1.0 if target > w0 else -1.0
        lo, hi = 0.0, abs(target - w0)
        for _ in range(200):
            d = 0.5 * (lo + hi)
            g = sgn * (mu - lv * (w0 + sgn * d)) - 1.5 * k32 * math.sqrt(d)
            lo, hi = (d, hi) if g > 0 else (lo, d)
        w_32 = w0 + sgn * 0.5 * (lo + hi)
        check(f"w0={w0}: linear-cost optimum", w_lin, lin_exp, 1e-9)
        check(f"w0={w0}: quadratic-cost optimum", w_quad, quad_exp, 1e-9)
        check(f"w0={w0}: 3/2-power-cost optimum", w_32, p32_exp, 1e-4)
        if w0 == 0.27:
            check("w0=0.27: size of the 3/2-power-cost trade", abs(w_32 - w0), 0.0022, 1e-4)
        # Brute-force confirmation of all three.
        bf_lin = brute_force_argmax(lambda w, w0=w0: util(w, w0, lambda t: c_lin * t), -0.5, 1.0)
        bf_quad = brute_force_argmax(lambda w, w0=w0: util(w, w0, lambda t: 0.5 * kappa * t**2), -0.5, 1.0)
        bf_32 = brute_force_argmax(lambda w, w0=w0: util(w, w0, lambda t: k32 * t**1.5), -0.5, 1.0)
        assert abs(bf_lin - w_lin) < 1e-4 and abs(bf_quad - w_quad) < 1e-4 and abs(bf_32 - w_32) < 1e-4


# ---------------------------------------------------------------------------
# 4. Several assets, quadratic costs: closed form
# ---------------------------------------------------------------------------


def section_multi_asset() -> None:
    print("\n== 4. Turnover-penalised optimisation with quadratic costs ==")
    vols = np.array([0.20, 0.25, 0.30])
    corr = np.full((3, 3), 0.3)
    np.fill_diagonal(corr, 1.0)
    sigma = np.outer(vols, vols) * corr
    alpha = np.array([0.03, 0.01, -0.02])
    lam = 5.0
    cmat = np.diag([0.1, 0.2, 0.4])
    w0 = np.array([0.1, 0.1, 0.0])
    w_star = np.linalg.solve(lam * sigma, alpha)
    w_tc = np.linalg.solve(lam * sigma + cmat, alpha + cmat @ w0)
    # Matrix-weighted average: (lam Sigma + C)^-1 (lam Sigma w* + C w0).
    w_avg = np.linalg.solve(lam * sigma + cmat, lam * sigma @ w_star + cmat @ w0)
    assert np.allclose(w_avg, w_tc)
    # First-order condition alpha - lam Sigma w - C (w - w0) = 0.
    assert np.allclose(alpha - lam * sigma @ w_tc - cmat @ (w_tc - w0), 0.0)

    def net_util(w: np.ndarray) -> float:
        d = w - w0
        return float(alpha @ w - 0.5 * lam * w @ sigma @ w - 0.5 * d @ cmat @ d)

    for i, (ws, wt) in enumerate(zip([0.1812, 0.0193, -0.0855], [0.1345, 0.0486, -0.0442], strict=True)):
        check(f"frictionless w*[{i}]", w_star[i], ws, 1e-4)
        check(f"cost-aware w[{i}]", w_tc[i], wt, 1e-4)
    check("turnover to w* (sum |dw|)", float(np.abs(w_star - w0).sum()), 0.2475, 1e-4)
    check("turnover to cost-aware w", float(np.abs(w_tc - w0).sum()), 0.1301, 1e-4)
    check("net utility, stay at w0 (bp)", 1e4 * net_util(w0), 6.87, 0.01, ".2f")
    check("net utility, jump to w* (bp)", 1e4 * net_util(w_star), 12.26, 0.01, ".2f")
    check("net utility, cost-aware w (bp)", 1e4 * net_util(w_tc), 23.59, 0.01, ".2f")


# ---------------------------------------------------------------------------
# 5. Garleanu-Pedersen
# ---------------------------------------------------------------------------


def gp_a(gamma: float, lam: float, rho: float) -> float:
    """Garleanu-Pedersen (2013) a; the trading rate is a / lambda."""
    s = gamma * (1 - rho) + lam * rho
    return (-s + math.sqrt(s * s + 4 * gamma * lam * (1 - rho) ** 2)) / (2 * (1 - rho))


def value_iteration_policy(gamma: float, lam: float, rho: float, sig2: float, b: float, phi: float) -> tuple[float, float]:
    """Solve V(y, f) = max_x (1-rho)(b x f - gamma sig2 x^2 / 2) - lam sig2 (x - y)^2 / 2 + (1-rho) E V(x, f')
    with f' = (1 - phi) f + eps, by iterating on the quadratic form V = -1/2 [y f] P [y f]^T + const.
    Returns the policy x = c_y y + c_f f."""
    beta = 1 - rho
    p = np.zeros((2, 2))
    s_map = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1 - phi]])  # (x, y, f) -> (x, f')
    c_y = c_f = 0.0
    for _ in range(100_000):
        m = np.zeros((3, 3))  # objective = -1/2 z^T M z, z = (x, y, f)
        m[0, 0] += beta * gamma * sig2 + lam * sig2
        m[1, 1] += lam * sig2
        m[0, 1] = m[1, 0] = -lam * sig2
        m[0, 2] = m[2, 0] = -beta * b
        m += beta * s_map.T @ p @ s_map
        c_y, c_f = -m[0, 1] / m[0, 0], -m[0, 2] / m[0, 0]
        p_new = m[1:, 1:] - np.outer(m[1:, 0], m[0, 1:]) / m[0, 0]
        if np.max(np.abs(p_new - p)) < 1e-13:
            p = p_new
            break
        p = p_new
    return c_y, c_f


def linear_rule_utility(c: float, k: float, b: float, gamma: float, lam: float, sig2: float, psi: float) -> float:
    """Exact stationary expected utility per period of x_t = (1 - c) x_{t-1} + c k f_t,
    f AR(1) with coefficient psi and unit variance: b E[xf] - gamma sig2/2 E[x^2] - lam sig2/2 E[dx^2]."""
    u = 1 - c
    exf = c * k / (1 - u * psi)
    ex2 = c * c * k * k * (1 + u * psi) / ((1 - u * u) * (1 - u * psi))
    efx_lag = psi * exf  # E[f_t x_{t-1}]
    edx2 = c * c * (k * k - 2 * k * efx_lag + ex2)
    return b * exf - 0.5 * gamma * sig2 * ex2 - 0.5 * lam * sig2 * edx2


def best_linear_rule(b: float, gamma: float, lam: float, sig2: float, psi: float) -> tuple[float, float, float]:
    """Maximise over (c, k): utility is quadratic in k for fixed c, so k*(c) is closed form; golden-section on c."""

    def best_k(c: float) -> tuple[float, float]:
        u1 = linear_rule_utility(c, 1.0, b, gamma, lam, sig2, psi)
        u2 = linear_rule_utility(c, 2.0, b, gamma, lam, sig2, psi)
        # U(k) = A k - B k^2: U(1) = A - B, U(2) = 2A - 4B.
        bb = (2 * u1 - u2) / 2
        aa = u1 + bb
        k = aa / (2 * bb)
        return k, linear_rule_utility(c, k, b, gamma, lam, sig2, psi)

    lo, hi = 1e-6, 1 - 1e-6
    g = (math.sqrt(5) - 1) / 2
    for _ in range(200):
        x1, x2 = hi - g * (hi - lo), lo + g * (hi - lo)
        if best_k(x1)[1] > best_k(x2)[1]:
            hi = x2
        else:
            lo = x1
    c = 0.5 * (lo + hi)
    k, util = best_k(c)
    return c, k, util


def section_gp() -> None:
    print("\n== 5. Garleanu-Pedersen trading rate and aim portfolio ==")
    gamma, lam, sig2, b = 1.0, 50.0, 1.0, 0.1
    phi = 1 - 0.5 ** (1 / 20)  # signal half-life 20 periods
    check("signal mean-reversion phi (half-life 20)", phi, 0.0341, 1e-4)

    # Closed form against value iteration, for two discount rates.
    for rho in (0.0, 0.01):
        a = gp_a(gamma, lam, rho)
        rate = a / lam
        aim_coef = b / (gamma * sig2 * (1 + a * phi / gamma))
        c_y, c_f = value_iteration_policy(gamma, lam, rho, sig2, b, phi)
        check(f"rho={rho}: closed-form trading rate a/lambda", rate, {0.0: 0.1318, 0.01: 0.1272}[rho], 1e-4)
        check(f"rho={rho}: value-iteration trading rate 1 - c_y", 1 - c_y, rate, 1e-8)
        check(f"rho={rho}: value-iteration signal loading c_f vs (a/lambda) aim", c_f, rate * aim_coef, 1e-8, ".6f")

    a = gp_a(gamma, lam, 0.0)
    check("a at rho=0", a, 6.5887, 1e-4)
    markowitz_coef = b / (gamma * sig2)
    aim_coef = markowitz_coef / (1 + a * phi / gamma)
    check("Markowitz loading b/(gamma sigma^2)", markowitz_coef, 0.1, 1e-12)
    check("aim loading b/(gamma sigma^2 (1 + a phi / gamma))", aim_coef, 0.0817, 1e-4)
    # Aim = sum_tau z (1-z)^tau E_t[Markowitz_{t+tau}], z = gamma / (gamma + a), E_t f_{t+tau} = (1-phi)^tau f_t.
    z = gamma / (gamma + a)
    taus = np.arange(20_000)
    weighted = float(np.sum(z * (1 - z) ** taus * markowitz_coef * (1 - phi) ** taus))
    check("z = gamma/(gamma + a)", z, 0.1318, 1e-4)
    check("weighted average of future Markowitz loadings", weighted, aim_coef, 1e-10)

    # Comparative statics.
    for lam_i, exp in [(10.0, 0.2702), (50.0, 0.1318), (200.0, 0.0683)]:
        check(f"trading rate a/lambda at lambda={lam_i:.0f}", gp_a(gamma, lam_i, 0.0) / lam_i, exp, 1e-4)
    for hl, exp in [(5.0, 0.5397), (100.0, 0.9565)]:
        ph = 1 - 0.5 ** (1 / hl)
        check(f"aim/Markowitz loading, signal half-life {hl:.0f}", 1 / (1 + a * ph / gamma), exp, 1e-4)

    # The closed form is the best linear rule for long-run average utility (rho = 0).
    psi = 1 - phi
    c_best, k_best, u_best = best_linear_rule(b, gamma, lam, sig2, psi)
    check("best linear rule: trading rate", c_best, a / lam, 1e-5)
    check("best linear rule: target loading", k_best, aim_coef, 1e-5)
    frictionless = b * b / (2 * gamma * sig2)
    check("full rebalance: cost over gross utility 2 lambda phi / gamma", 2 * lam * phi / gamma, 3.4064, 1e-4)
    check("frictionless Markowitz utility per period", frictionless, 0.005, 1e-12, ".5f")
    rows = {
        "full rebalance to Markowitz": (1.0, markowitz_coef, -2.4064),
        "partial (a/lambda) toward Markowitz": (a / lam, markowitz_coef, 0.6334),
        "Garleanu-Pedersen": (a / lam, aim_coef, 0.6670),
    }
    for name, (c, k, exp) in rows.items():
        check(f"exact utility / frictionless: {name}", linear_rule_utility(c, k, b, gamma, lam, sig2, psi) / frictionless, exp, 1e-4)
    # Best rate if you insist on trading toward Markowitz (k fixed at the Markowitz loading).
    grid = np.linspace(0.001, 1.0, 100_000)
    utils = np.array([linear_rule_utility(c, markowitz_coef, b, gamma, lam, sig2, psi) for c in grid])
    check("best rate toward Markowitz", float(grid[np.argmax(utils)]), 0.1069, 1e-3)
    check("its utility / frictionless", float(utils.max()) / frictionless, 0.6412, 1e-4)

    # Simulation of the same model.
    print("\n== 6. Simulation with a mean-reverting signal ==")
    rng = np.random.default_rng(13)
    n = 400_000
    eps = rng.standard_normal(n) * math.sqrt(1 - psi * psi)
    f = np.empty(n)
    f[0] = rng.standard_normal()
    for t in range(1, n):
        f[t] = psi * f[t - 1] + eps[t]
    r_next = b * f + math.sqrt(sig2) * rng.standard_normal(n)  # r_{t+1} = b f_t + u_{t+1}

    def run(c: float, k: float) -> tuple[float, float, float, float]:
        x = np.empty(n)
        prev = 0.0
        for t in range(n):
            prev = (1 - c) * prev + c * k * f[t]
            x[t] = prev
        dx = np.diff(np.concatenate([[0.0], x]))
        pnl = x * r_next - 0.5 * lam * sig2 * dx * dx
        util = pnl.mean() - 0.5 * gamma * sig2 * np.mean(x * x)
        sharpe = pnl.mean() / pnl.std() * math.sqrt(252)
        gross = x * r_next
        gross_sharpe = gross.mean() / gross.std() * math.sqrt(252)
        return float(util / frictionless), float(sharpe), float(np.mean(np.abs(dx))), float(gross_sharpe)

    sims = {
        "no trading": (0.0, 0.0, (0.0, 0.0, 0.0, 0.0)),
        "full rebalance to Markowitz": (1.0, markowitz_coef, (-2.37, -1.06, 0.0209, 1.61)),
        "partial (a/lambda) toward Markowitz": (a / lam, markowitz_coef, (0.67, 1.29, 0.0050, 1.46)),
        "Garleanu-Pedersen": (a / lam, aim_coef, (0.70, 1.32, 0.0040, 1.46)),
    }
    for name, (c, k, (u_exp, s_exp, t_exp, g_exp)) in sims.items():
        if c == 0.0:
            print(f"{name}: utility 0, Sharpe undefined, turnover 0")
            continue
        u, s, turn, gs = run(c, k)
        check(f"sim utility / frictionless: {name}", u, u_exp, 0.006, ".2f")
        check(f"sim net annualised Sharpe: {name}", s, s_exp, 0.006, ".2f")
        check(f"sim gross annualised Sharpe: {name}", gs, g_exp, 0.006, ".2f")
        check(f"sim mean |dx| per period: {name}", turn, t_exp, 5e-4)


if __name__ == "__main__":
    section_cost_model()
    section_alpha_decay()
    section_cost_shapes()
    section_multi_asset()
    section_gp()
    print("\nAll checks passed.")
