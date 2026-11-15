"""Kelly criterion and position sizing: every number in the note.

Backs every number in `11-Risk-and-Trading/01-Kelly-Criterion-and-Position-Sizing.md`.
Independent routes used here:
- Kelly fractions by numerically maximising the growth function (golden-section search), never by the
  closed forms f* = p - q/b or mu/sigma^2 the note quotes;
- median wealth after 100 flips from the exact binomial distribution of the number of heads;
- fractional-Kelly growth by Gauss-Hermite quadrature of E[log(1 + f R)] for rebalanced wealth, without Ito's lemma,
  and volatility by seeded simulation of log-wealth changes;
- drawdown and double-before-halve probabilities by a finite-difference solve of the hitting-probability ODE
  and by seeded simulation (log wealth with a Brownian-bridge correction, and daily-rebalanced wealth with no Ito drift),
  not by the x^(2/c-1) formula;
- the shrinkage factor under estimation error by seeded simulation of daily-return histories and their drift estimates;
- the two-asset allocation by exact rational Cramer's rule, compared with a numerical gradient search.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 11-Risk-and-Trading/code/risk_01_kelly.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


def argmax(fn, lo: float, hi: float) -> float:
    """Golden-section search for the maximiser of a unimodal function on [lo, hi]."""
    inv_phi = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = lo, hi
    for _ in range(200):
        c = b - inv_phi * (b - a)
        d = a + inv_phi * (b - a)
        if fn(c) > fn(d):
            b = d
        else:
            a = c
    return (a + b) / 2.0


def bisect_root(fn, lo: float, hi: float) -> float:
    flo = fn(lo)
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if (fn(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def binary_growth(p: float, b: float):
    return lambda f: p * math.log(1.0 + b * f) + (1.0 - p) * math.log(1.0 - f)


# ------------------------------------------------------------------ hitting probabilities of drifted Brownian motion


def hit_lower_fd(drift: float, vol: float, a: float, upper: float, n: int = 4000) -> float:
    """P(X hits -a before +upper | X_0 = 0) for dX = drift dt + vol dB, by finite differences on (vol^2/2) u'' + drift u' = 0."""
    h = (a + upper) / n
    lo_c = vol**2 / (2 * h * h) - drift / (2 * h)
    di_c = -(vol**2) / (h * h)
    up_c = vol**2 / (2 * h * h) + drift / (2 * h)
    m = n - 1  # interior nodes 1..n-1; u(-a) = 1, u(upper) = 0
    sub = np.full(m, lo_c)
    dia = np.full(m, di_c)
    sup = np.full(m, up_c)
    rhs = np.zeros(m)
    rhs[0] = -lo_c * 1.0
    # Thomas algorithm
    for i in range(1, m):
        w = sub[i] / dia[i - 1]
        dia[i] -= w * sup[i - 1]
        rhs[i] -= w * rhs[i - 1]
    u = np.zeros(m)
    u[-1] = rhs[-1] / dia[-1]
    for i in range(m - 2, -1, -1):
        u[i] = (rhs[i] - sup[i] * u[i + 1]) / dia[i]
    x = -a + h * np.arange(1, n)
    return float(np.interp(0.0, x, u))


def hit_lower_sim(rng: np.random.Generator, drift: float, vol: float, a: float, horizon: float, n_paths: int, n_steps: int):
    """P(X ever hits -a) by simulation; a Brownian bridge gives the exact crossing probability between grid points."""
    dt = horizon / n_steps
    survive = np.ones(n_paths)
    x = np.zeros(n_paths)
    for _ in range(n_steps):
        x_new = x + drift * dt + vol * math.sqrt(dt) * rng.standard_normal(n_paths)
        d0, d1 = x + a, x_new + a
        p_cross = np.where((d0 > 0) & (d1 > 0), np.exp(-2.0 * d0 * d1 / (vol**2 * dt)), 1.0)
        survive *= 1.0 - p_cross
        x = x_new
    est = 1.0 - survive
    return float(est.mean()), float(est.std(ddof=1) / math.sqrt(n_paths))


# ------------------------------------------------------------------ sections


def binary_bets() -> None:
    print("Example 1: biased coin at even money (cards risk-kelly-binary-formula, risk-kelly-coin-60)")
    g = binary_growth(0.6, 1.0)
    f_star = argmax(g, 0.0, 0.99)
    approx("f* by numerical maximisation", f_star, 0.2, 6)
    approx("growth per flip at f*", g(f_star), 0.0201, 4)
    approx("small-bet approximation mean^2/(2 E[X^2])", 0.2**2 / (2 * 1.0), 0.02, 12)
    # median wealth after 100 flips from the exact Bin(100, 0.6) law of the number of heads
    pmf = [Fraction(math.comb(100, k)) * Fraction(3, 5) ** k * Fraction(2, 5) ** (100 - k) for k in range(101)]
    cum, median_heads = Fraction(0), None
    for k, pk in enumerate(pmf):
        cum += pk
        if cum >= Fraction(1, 2):
            median_heads = k
            break
    exact("median number of heads in 100 flips", median_heads, 60)
    for f, growth, wealth in [(0.1, 0.0150, 4.50), (0.2, 0.0201, 7.49), (0.3, 0.0147, 4.37), (0.4, -0.0024, 0.78)]:
        approx(f"growth per flip at f = {f}", g(f), growth, 4)
        median_wealth = (1 + f) ** median_heads * (1 - f) ** (100 - median_heads)
        approx(f"median wealth after 100 flips at f = {f}", median_wealth, wealth, 2)
    approx("median wealth at f* (body: about 7.5 times)", (1.2**60) * (0.8**40), 7.5, 1)
    exact("expected profit per flip at 40% / at 20%", Fraction(2, 5) * Fraction(1, 5) / (Fraction(1, 5) * Fraction(1, 5)), 2)
    approx("zero-growth fraction by bisection", bisect_root(g, 0.25, 0.6), 0.389, 3)
    assert bisect_root(g, 0.25, 0.6) < 2 * f_star
    print("    zero-growth fraction is below 2 f* = 0.4")

    print("Example 2: 2 to 1 on a 40% event (card risk-kelly-long-odds)")
    g2 = binary_growth(0.4, 2.0)
    approx("expected profit per unit", 0.4 * 2 - 0.6, 0.2, 12)
    approx("f* by numerical maximisation", argmax(g2, 0.0, 0.99), 0.1, 6)
    approx("growth per bet", g2(0.1), 0.0097, 4)


def quadrature_growth(mu: float, sigma: float, f: float, steps_per_year: int = 2520) -> float:
    """Annual log growth of wealth rebalanced to fraction f at every step: steps_per_year x E[log(1 + f R_step)].

    R_step is normal with mean mu dt and sd sigma sqrt(dt); the expectation is Gauss-Hermite quadrature, so no Ito
    correction is assumed.  Ten steps a day keeps the discretisation bias below 0.0002 a year.
    """
    dt = 1.0 / steps_per_year
    nodes, weights = np.polynomial.hermite_e.hermegauss(120)
    weights = weights / math.sqrt(2 * math.pi)
    return float(steps_per_year * np.sum(weights * np.log1p(f * (mu * dt + sigma * math.sqrt(dt) * nodes))))


def simulated_log_vol(rng: np.random.Generator, mu: float, sigma: float, f: float, steps_per_year: int = 252, n_draws: int = 2_000_000):
    """Annualised sd of the log wealth change log(1 + f R_step), from seeded draws, with its standard error."""
    dt = 1.0 / steps_per_year
    logs = np.log1p(f * (mu * dt + sigma * math.sqrt(dt) * rng.standard_normal(n_draws)))
    sd = float(logs.std(ddof=1))
    return sd * math.sqrt(steps_per_year), sd / math.sqrt(2 * n_draws) * math.sqrt(steps_per_year)


def continuous(rng: np.random.Generator) -> None:
    print("Example 3: index with excess return 8% and volatility 20% (cards risk-kelly-continuous, risk-kelly-index-leverage)")
    mu, sigma = 0.08, 0.20
    growth = lambda f: f * mu - 0.5 * f * f * sigma**2  # noqa: E731 - the log-wealth drift of the model
    f_star = argmax(growth, 0.0, 10.0)
    approx("Kelly leverage by numerical maximisation", f_star, 2.0, 6)
    approx(
        "Kelly leverage by maximising the quadrature growth (no Ito)", argmax(lambda f: quadrature_growth(mu, sigma, f), 0.0, 10.0), 2.0, 3
    )
    approx("excess growth at full Kelly", growth(2.0), 0.08, 12)
    approx("excess growth at full Kelly, quadrature", quadrature_growth(mu, sigma, 2.0), 0.08, 3)
    approx("excess growth at half Kelly (fully invested), quadrature", quadrature_growth(mu, sigma, 1.0), 0.06, 3)
    approx("excess growth at leverage 4, quadrature", quadrature_growth(mu, sigma, 4.0), 0.0, 3)
    approx("shortcut SR / sigma = 0.4 / 0.2 against the maximiser", 0.4 / 0.2, f_star, 6)
    vol, se = simulated_log_vol(rng, mu, sigma, 2.0)
    simulated("portfolio volatility at full Kelly, simulated", vol, 0.40, 5 * se + 0.005)

    print("Fractional Kelly table (card risk-kelly-half-kelly): growth share by quadrature, volatility share by simulation")
    g_max = quadrature_growth(mu, sigma, 2.0)
    for c, share in [(0.25, 0.44), (0.5, 0.75), (1.0, 1.00), (1.5, 0.75), (2.0, 0.0)]:
        approx(f"growth share at c = {c}, quadrature", quadrature_growth(mu, sigma, c * 2.0) / g_max, share, 2)
        vol, se = simulated_log_vol(rng, mu, sigma, c * 2.0)
        simulated(f"volatility share at c = {c}, simulated", vol / 0.40, c, (5 * se + 0.002) / 0.40 + 0.005)
    approx("c(2 - c) at c = 0.25 (quoted 44%)", 0.25 * 1.75, 0.44, 2)
    approx("1.5x Kelly volatility over 0.5x Kelly volatility", 1.5 / 0.5, 3.0, 12)


def halving_wealth_sim(rng: np.random.Generator, mu: float, sigma: float, f: float, years: int, n_paths: int):
    """P(wealth ever touches half its start) for daily rebalanced wealth W *= 1 + f R, R normal; no Ito drift assumed.

    Daily monitoring misses crossings between days; the Broadie-Glasserman-Kou correction moves the barrier
    0.5826 x (daily log-wealth sd) toward the start to approximate continuous monitoring.
    """
    dt = 1.0 / 252
    barrier = math.log(0.5) + 0.5826 * f * sigma * math.sqrt(dt)
    logw = np.zeros(n_paths)
    hit = np.zeros(n_paths, dtype=bool)
    for _ in range(years * 252):
        logw += np.log1p(f * (mu * dt + sigma * math.sqrt(dt) * rng.standard_normal(n_paths)))
        hit |= logw <= barrier
    est = float(hit.mean())
    return est, math.sqrt(est * (1 - est) / n_paths)


def drawdowns(rng: np.random.Generator) -> None:
    print("Drawdown and double-before-halve probabilities (cards risk-kelly-drawdown, risk-kelly-double-before-halve)")
    sr = 1.0  # any Sharpe ratio gives the same answer; the hitting laws depend on drift / vol^2 only
    for c, quoted, quoted_db in [(1.0, Fraction(1, 2), Fraction(2, 3)), (0.5, Fraction(1, 8), Fraction(8, 9))]:
        drift = sr**2 * (c - c * c / 2)  # log-wealth drift at fraction c of Kelly
        vol = c * sr
        a = math.log(2.0)
        fd = hit_lower_fd(drift, vol, a, upper=60.0)
        approx(f"P(ever halve) at c = {c}, finite differences", fd, float(quoted), 4)
        sim, se = hit_lower_sim(rng, drift, vol, a, horizon=40.0, n_paths=40_000, n_steps=400)
        simulated(f"P(ever halve) at c = {c}, simulated log wealth with bridge correction", sim, float(quoted), 5 * se + 0.003)
        sim_w, se_w = halving_wealth_sim(rng, 0.20, 0.20, c * 5.0, years=30, n_paths=20_000)
        simulated(f"P(ever halve) at c = {c}, simulated daily-rebalanced wealth", sim_w, float(quoted), 5 * se_w + 0.01)
        db = 1.0 - hit_lower_fd(drift, vol, a, upper=a)
        approx(f"P(double before halving) at c = {c}, finite differences", db, float(quoted_db), 4)
        theta = 2 / c - 1
        approx(f"card formula 1/(1 + 2^-theta) at c = {c} against the finite-difference value", 1 / (1 + 2**-theta), db, 4)
    exact("0.5^3", Fraction(1, 2) ** 3, Fraction(1, 8))


def drift_estimates(rng: np.random.Generator, mu: float, sigma: float, years: int, n_paths: int) -> np.ndarray:
    """Annual drift estimates mu_hat = 252 x mean of daily returns, one per simulated history of `years` years."""
    days = 252 * years
    out = np.empty(n_paths)
    chunk = max(1, 2_000_000 // days)
    for i in range(0, n_paths, chunk):
        m = min(chunk, n_paths - i)
        daily = mu / 252 + sigma / math.sqrt(252) * rng.standard_normal((m, days))
        out[i : i + m] = 252 * daily.mean(axis=1)
    return out


def estimation_error(rng: np.random.Generator) -> None:
    print("Example 4: shrinkage under estimation error (cards risk-kelly-param-uncertainty, risk-kelly-shrink-four-years)")
    mu = sigma = 0.20
    for years, n_paths, s_quoted, k_quoted in [(1, 200_000, 0.20, 0.5), (4, 50_000, 0.10, 0.8), (10, 20_000, None, 0.91)]:
        mu_hat = drift_estimates(rng, mu, sigma, years, n_paths)
        sd_hat = float(mu_hat.std(ddof=1))
        if s_quoted is not None:
            simulated(f"standard error of mu_hat with {years} year(s), simulated", sd_hat, s_quoted, 5 * sd_hat / math.sqrt(2 * n_paths))
        # E[g](k) = k mu E[mu_hat]/sigma^2 - k^2 E[mu_hat^2]/(2 sigma^2), so k* = mu E[mu_hat] / E[mu_hat^2]
        m1, m2 = float(mu_hat.mean()), float((mu_hat**2).mean())
        k_sim = mu * m1 / m2
        cov = np.cov(np.vstack([mu_hat, mu_hat**2])) / n_paths
        grad = np.array([mu / m2, -mu * m1 / m2**2])
        se_k = float(math.sqrt(grad @ cov @ grad))  # delta method
        simulated(f"k* with {years} year(s) of data, simulated", k_sim, k_quoted, 5 * se_k + 0.005)
        if years == 1:
            for k, quoted in [(1.0, 0.0), (0.5, 0.25)]:
                f = k * mu_hat / sigma**2
                g = f * mu - 0.5 * f * f * sigma**2
                simulated(f"expected excess growth at k = {k}, simulated", float(g.mean()), quoted, 5 * float(g.std()) / math.sqrt(n_paths))
            approx("true-parameter maximum mu^2/(2 sigma^2)", mu**2 / (2 * sigma**2), 0.5, 12)
    approx("ten-year k* from exact moments", mu**2 / (mu**2 + sigma**2 / 10), 0.91, 2)


def two_assets() -> None:
    print("Example 5: two correlated assets (cards risk-kelly-multi-asset, risk-kelly-standalone-overbet)")
    mu = [Fraction(5, 100), Fraction(3, 100)]
    vol = [Fraction(20, 100), Fraction(15, 100)]
    rho = Fraction(1, 2)
    s11, s22, s12 = vol[0] ** 2, vol[1] ** 2, rho * vol[0] * vol[1]
    exact("Sigma entries", (s11, s12, s22), (Fraction(4, 100), Fraction(15, 1000), Fraction(225, 10000)))
    det = s11 * s22 - s12 * s12
    f1 = (s22 * mu[0] - s12 * mu[1]) / det
    f2 = (s11 * mu[1] - s12 * mu[0]) / det
    exact("f* by Cramer's rule", (f1, f2), (Fraction(1), Fraction(2, 3)))
    # numerical gradient ascent on f.mu - f'Sigma f/2 as an independent check
    cov = np.array([[0.04, 0.015], [0.015, 0.0225]])
    m = np.array([0.05, 0.03])
    f = np.zeros(2)
    for _ in range(20000):
        f += 5.0 * (m - cov @ f)
    approx("f*_1 by gradient ascent", f[0], 1.00, 2)
    approx("f*_2 by gradient ascent", f[1], 0.67, 2)
    approx("standalone sizing of asset 1", float(mu[0] / s11), 1.25, 2)
    approx("standalone sizing of asset 2", float(mu[1] / s22), 1.33, 2)
    approx("standalone total leverage", float(mu[0] / s11 + mu[1] / s22), 2.58, 2)
    approx("joint total leverage", float(f1 + f2), 1.67, 2)
    quad = mu[0] * f1 + mu[1] * f2
    exact("mu' Sigma^-1 mu", quad, Fraction(7, 100))
    approx("portfolio Sharpe", math.sqrt(quad), 0.265, 3)
    approx("maximal excess growth", float(quad / 2), 0.035, 3)
    approx("maximal excess growth from the gradient solution", 0.5 * float(m @ f), 0.035, 6)


def scaling() -> None:
    print("Pitfall and card risk-kelly-sigma-scaling: doubling volatility")
    g_lo = argmax(lambda f: f * 0.05 - 0.5 * f * f * 0.1**2, 0.0, 100.0)
    g_hi = argmax(lambda f: f * 0.05 - 0.5 * f * f * 0.2**2, 0.0, 100.0)
    approx("Kelly position ratio after volatility doubles", g_hi / g_lo, 0.25, 6)


def main() -> None:
    rng = np.random.default_rng(SEED)
    binary_bets()
    continuous(rng)
    drawdowns(rng)
    estimation_error(rng)
    two_assets()
    scaling()
    print("All Kelly numbers check.")


if __name__ == "__main__":
    main()
