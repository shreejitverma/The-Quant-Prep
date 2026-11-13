"""Time series, stationarity and ARMA: every number in the note, by an independent route.

Backs every number in `02-Statistics-and-Econometrics/08-Time-Series-Stationarity-and-ARMA.md`.
Independent routes used here:
- AR(1) forecasts and forecast errors by seeded simulation of many paths from the stated state;
- MA(1) roots with `numpy.roots`, and its autocorrelation, the Roll spread and over-differencing by simulation;
- AR(2) stationarity from the characteristic roots, its ACF from the Yule-Walker linear system and from a long
  simulated path, and its PACF by Durbin-Levinson;
- Dickey-Fuller critical values by simulating random walks, compared with MacKinnon (2010); ADF power by simulation;
- the Ljung-Box chi-square tail by the closed form for 3 degrees of freedom and by quadrature, and the m - p degrees
  of freedom on fitted AR residuals by simulation;
- the half-life snippet re-run with its own seed, and the Kendall small-sample bias by simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_08_arma.py`.
"""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

SEED = 20261112
N01 = NormalDist()
LN_HALF = math.log(0.5)

# MacKinnon (2010), "Critical Values for Cointegration Tests", Queen's Economics Department Working Paper 1227,
# response-surface coefficients for N = 1 (the Dickey-Fuller tau statistics): (b_inf, b1, b2, b3) by level.
MACKINNON = {
    "nc": {0.01: (-2.56574, -2.2358, -3.627, 0.0), 0.05: (-1.94100, -0.2686, -3.365, 31.223)},
    "c": {0.01: (-3.43035, -6.5393, -16.786, -79.433), 0.05: (-2.86154, -2.8903, -4.234, -40.040)},
    "ct": {0.01: (-3.95877, -9.0531, -28.428, -134.155), 0.05: (-3.41049, -4.3904, -9.036, -45.374)},
}


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def mackinnon_cv(case: str, level: float, t: int) -> float:
    b0, b1, b2, b3 = MACKINNON[case][level]
    return b0 + b1 / t + b2 / t**2 + b3 / t**3


def df_tstats(x: np.ndarray, case: str) -> np.ndarray:
    """Dickey-Fuller t-statistics (no lags) for each row of x: regress dx_t on [deterministics, x_{t-1}]."""
    dx, lag = np.diff(x, axis=1), x[:, :-1]
    t = dx.shape[1]
    if case == "nc":
        z = np.empty((t, 0))
    elif case == "c":
        z = np.ones((t, 1))
    else:
        z = np.c_[np.ones(t), np.arange(1, t + 1)]
    if z.shape[1]:
        proj = np.linalg.solve(z.T @ z, z.T)  # k x t
        dx = dx - (dx @ proj.T) @ z.T
        lag = lag - (lag @ proj.T) @ z.T
    sxx = np.sum(lag * lag, axis=1)
    g = np.sum(lag * dx, axis=1) / sxx
    e = dx - g[:, None] * lag
    s2 = np.sum(e * e, axis=1) / (t - z.shape[1] - 1)
    return g / np.sqrt(s2 / sxx)


def ar1_paths(rng: np.random.Generator, phi: float, n: int, paths: int) -> np.ndarray:
    """AR(1) with unit innovations started from its stationary law (a random walk from 0 when phi = 1)."""
    x = np.empty((paths, n))
    x[:, 0] = rng.standard_normal(paths) / math.sqrt(1 - phi * phi) if phi < 1 else 0.0
    eps = rng.standard_normal((paths, n))
    for t in range(1, n):
        x[:, t] = phi * x[:, t - 1] + eps[:, t]
    return x


def chi2_3_sf(q: float) -> float:
    """Closed-form upper tail of chi-square with 3 degrees of freedom."""
    r = math.sqrt(q)
    return 2 * (1 - N01.cdf(r)) + math.sqrt(2 * q / math.pi) * math.exp(-q / 2)


def ar1_example(rng: np.random.Generator) -> None:
    print("Example 1 and cards stat-arma-half-life, stat-arma-ar1-forecast, stat-arma-ou-mapping")
    phi, sig, dev = 0.95, 0.10, 0.8
    hl = LN_HALF / math.log(phi)
    approx("half-life ln 0.5/ln 0.95", hl, 13.5, 1)
    sd_stat = sig / math.sqrt(1 - phi**2)
    approx("stationary sd", sd_stat, 0.320, 3)
    approx("phi^2", phi**2, 0.9025, 4)
    approx("standard deviations rich", dev / sd_stat, 2.5, 1)
    paths = 400000
    x = np.full(paths, dev)
    for _ in range(5):
        x = phi * x + sig * rng.standard_normal(paths)
    sd5 = sig * math.sqrt((1 - phi**10) / (1 - phi**2))
    simulated("mean five-step deviation from 0.8 (simulated)", float(x.mean()), 0.619, 4 * sd5 / math.sqrt(paths) + 0.0005)
    approx("0.8 x 0.95^5", dev * phi**5, 0.619, 3)
    approx("0.8 x 0.95^5 (card)", dev * phi**5, 0.62, 2)
    simulated("sd of the five-step value (simulated)", float(x.std()), 0.203, 4 * sd5 / math.sqrt(2 * paths) + 0.0005)
    approx("forecast error sd", sd5, 0.203, 3)
    approx("expected five-day move", dev * phi**5 - dev, -0.181, 3)
    kappa = -math.log(phi) * 252
    approx("OU speed kappa per year", kappa, 12.9, 1)
    approx("half-life ln 2/kappa in trading days", math.log(2) / kappa * 252, 13.5, 1)
    approx("half-life at phi = 0.98", LN_HALF / math.log(0.98), 34, 0)


def ma1_and_roll(rng: np.random.Generator) -> None:
    print("Example 2 and cards stat-arma-ma1-max-rho, stat-arma-roll-spread, stat-arma-overdifferencing")
    roots = sorted(np.roots([0.4, 1.0, 0.4]).real)
    approx("root theta = -2", roots[0], -2.0, 10)
    approx("root theta = -0.5", roots[1], -0.5, 10)
    e = rng.standard_normal(2_000_001)
    x = e[1:] - 0.5 * e[:-1]
    r1 = float(np.corrcoef(x[1:], x[:-1])[0, 1])
    simulated("lag-1 autocorrelation of a simulated MA(1), theta = -0.5", r1, -0.4, 4 / math.sqrt(len(x)))
    grid = np.linspace(-5, 5, 100001)
    rho = grid / (1 + grid**2)
    approx("max |theta/(1+theta^2)| over a grid", float(np.max(np.abs(rho))), 0.5, 6)
    approx("argmax theta", float(abs(grid[np.argmax(rho)])), 1.0, 4)
    approx("Roll spread 2 sqrt(0.0004)", 2 * math.sqrt(0.0004), 0.04, 10)
    # Roll model: efficient price random walk plus +/- s/2 bounce with independent signs
    s, n = 0.04, 2_000_000
    mid = np.cumsum(0.01 * rng.standard_normal(n))
    p = mid + 0.5 * s * rng.choice([-1.0, 1.0], n)
    dp = np.diff(p)
    cov1 = float(np.mean((dp[1:] - dp.mean()) * (dp[:-1] - dp.mean())))
    simulated("lag-1 autocovariance of simulated Roll price changes", cov1, -0.0004, 0.00001)
    approx("spread recovered from it", 2 * math.sqrt(-cov1), 0.04, 3)
    d = np.diff(rng.standard_normal(2_000_000))
    simulated("lag-1 autocorrelation of differenced white noise", float(np.corrcoef(d[1:], d[:-1])[0, 1]), -0.5, 0.003)


def ar2_example(rng: np.random.Generator) -> None:
    print("Example 3: AR(2) x_t = 0.5 x_{t-1} + 0.3 x_{t-2} + e_t")
    phi1, phi2 = 0.5, 0.3
    mods = sorted(abs(r) for r in np.roots([-phi2, -phi1, 1.0]))  # roots of 1 - 0.5 z - 0.3 z^2
    approx("root modulus 1", mods[0], 1.17, 2)
    approx("root modulus 2", mods[1], 2.84, 2)
    approx("phi1 + phi2", phi1 + phi2, 0.8, 10)
    approx("phi2 - phi1", phi2 - phi1, -0.2, 10)
    # Yule-Walker for rho_1, rho_2 as a linear system: rho1 = phi1 + phi2 rho1, rho2 = phi1 rho1 + phi2
    a = np.array([[1 - phi2, 0.0], [-phi1, 1.0]])
    rho1, rho2 = np.linalg.solve(a, np.array([phi1, phi2]))
    rho3 = phi1 * rho2 + phi2 * rho1
    approx("rho_1", rho1, 0.714, 3)
    approx("rho_2", rho2, 0.657, 3)
    approx("rho_3", rho3, 0.543, 3)
    n = 1_000_000
    x = np.zeros(n)
    e = rng.standard_normal(n)
    for t in range(2, n):
        x[t] = phi1 * x[t - 1] + phi2 * x[t - 2] + e[t]
    x = x[1000:]
    for k, q in ((1, rho1), (2, rho2), (3, rho3)):
        simulated(f"sample ACF lag {k} of a 1,000,000-step path", float(np.corrcoef(x[k:], x[:-k])[0, 1]), q, 0.01)
    # Durbin-Levinson PACF from the theoretical ACF
    acf = [1.0, rho1, rho2, rho3]
    pacf2 = (rho2 - rho1**2) / (1 - rho1**2)
    approx("PACF lag 2", pacf2, 0.3, 10)
    r = np.array([[acf[abs(i - j)] for j in range(3)] for i in range(3)])
    coef = np.linalg.solve(r, np.array(acf[1:4]))
    approx("PACF lag 3 (last coefficient of the order-3 Yule-Walker fit)", float(coef[2]), 0.0, 10)


def dickey_fuller(rng: np.random.Generator) -> None:
    print("Unit-root tests: critical values (Core concepts), Example 4 and cards stat-arma-df-critical-value, stat-arma-df-power")
    quoted = {("nc", 0.05): -1.94, ("c", 0.05): -2.86, ("ct", 0.05): -3.41, ("nc", 0.01): -2.57, ("c", 0.01): -3.43, ("ct", 0.01): -3.96}
    for (case, level), q in quoted.items():
        approx(f"MacKinnon asymptotic {case} {level:.0%}", MACKINNON[case][level][0], q, 2)
    t_len, paths = 500, 40000
    stats = {c: [] for c in ("nc", "c", "ct")}
    for _ in range(4):
        rw = np.cumsum(rng.standard_normal((paths // 4, t_len + 1)), axis=1)
        for c in stats:
            stats[c].append(df_tstats(rw, c))
    for case, level in quoted:
        draws = np.concatenate(stats[case])
        sim = float(np.quantile(draws, level))
        h = 0.05
        dens = float(np.mean(np.abs(draws - sim) < h)) / (2 * h)  # density at the quantile, for its standard error
        se = math.sqrt(level * (1 - level) / len(draws)) / dens
        target = mackinnon_cv(case, level, t_len)
        simulated(f"simulated {case} {level:.0%} quantile, T = 500 (MacKinnon finite-T {target:.3f})", sim, target, 4 * se)
    approx("Student-t (normal) one-sided 5% value", N01.inv_cdf(0.05), -1.645, 3)
    approx("MacKinnon finite-sample 5% value with a constant at T = 500", mackinnon_cv("c", 0.05, t_len), -2.87, 2)
    approx("MacKinnon finite-sample 5% value with a constant at T = 250", mackinnon_cv("c", 0.05, 250), -2.87, 2)
    approx("Example 4: t = -0.02/0.009", -0.02 / 0.009, -2.22, 2)
    approx("Example 4: implied half-life at phi = 0.98", LN_HALF / math.log(0.98), 34, 0)
    cv = -2.86
    reps = 20000
    for phi, n, q in ((0.98, 250, 0.13), (0.98, 1000, 0.87), (0.95, 250, 0.48), (1.0, 250, 0.053)):
        x = ar1_paths(rng, phi, n, reps)
        rate = float(np.mean(df_tstats(x, "c") < cv))
        simulated(f"ADF rejection rate at 5%, phi = {phi}, T = {n}", rate, q, 4 * math.sqrt(q * (1 - q) / reps) + 0.005)


def ljung_box(rng: np.random.Generator) -> None:
    print("Example 5 and card stat-arma-ljung-box")
    t = 500
    rho = (0.08, -0.05, 0.06)
    q = t * (t + 2) * sum(r * r / (t - k) for k, r in enumerate(rho, start=1))
    approx("Q(3)", q, 6.30, 2)
    grid = np.linspace(0, 60, 600001)
    dens = np.sqrt(grid) * np.exp(-grid / 2) / math.sqrt(2 * math.pi)  # chi-square 3 density
    cdf = np.concatenate([[0.0], np.cumsum((dens[1:] + dens[:-1]) / 2 * (grid[1] - grid[0]))])
    approx("chi2_{3, 0.95} by quadrature", float(np.interp(0.95, cdf, grid)), 7.81, 2)
    approx("p-value, closed form", chi2_3_sf(q), 0.098, 3)
    approx("p-value, quadrature", 1 - float(np.interp(q, grid, cdf)), 0.098, 3)
    approx("Bartlett band 1.96/sqrt(500)", N01.inv_cdf(0.975) / math.sqrt(t), 0.088, 3)
    # degrees of freedom on fitted residuals: Q(10) on AR(1) residuals has mean m - p = 9, not 10
    reps, n, m = 4000, 1000, 10
    x = ar1_paths(rng, 0.5, n, reps)
    qs = np.empty(reps)
    for i in range(reps):
        y, lag = x[i, 1:], x[i, :-1]
        b = np.linalg.lstsq(np.c_[np.ones(n - 1), lag], y, rcond=None)[0]
        e = y - b[0] - b[1] * lag
        e = e - e.mean()
        g0 = e @ e
        r = np.array([e[k:] @ e[:-k] / g0 for k in range(1, m + 1)])
        qs[i] = (n - 1) * (n + 1) * np.sum(r * r / (n - 1 - np.arange(1, m + 1)))
    simulated(
        "mean Ljung-Box Q(10) on fitted AR(1) residuals (chi2_9 mean 9)",
        float(qs.mean()),
        9.1,
        4 * float(qs.std()) / math.sqrt(reps) + 0.05,
    )
    assert abs(float(qs.mean()) - 10.0) > 8 * float(qs.std()) / math.sqrt(reps), "residual Q should not look like chi2_10"


def snippet_and_bias(rng: np.random.Generator) -> None:
    print("Example 6: the half-life snippet with its own seed, and the interval for phi")

    def fit_ar1(x):
        X = np.column_stack([np.ones(len(x) - 1), x[:-1]])
        (c, phi), *_ = np.linalg.lstsq(X, x[1:], rcond=None)
        return phi, LN_HALF / math.log(phi)

    snip_rng = np.random.default_rng(7)
    x = np.full(1000, 1.0)
    for t in range(1, 1000):
        x[t] = 0.05 + 0.95 * x[t - 1] + 0.1 * snip_rng.standard_normal()
    phi_hat, hl_hat = fit_ar1(x)
    approx("snippet phi_hat", phi_hat, 0.963, 3)
    approx("snippet half-life", hl_hat, 18.2, 1)
    approx("snippet DF t-stat", float(df_tstats(x[None, :], "c")[0]), -4.34, 2)
    se = math.sqrt((1 - 0.95**2) / 1000)
    approx("se of phi_hat at T = 1000", se, 0.0099, 4)
    approx("phi - 2 se", 0.95 - 2 * se, 0.9303, 4)
    approx("phi + 2 se", 0.95 + 2 * se, 0.96975, 5)
    approx("half-life at phi - 2 se", LN_HALF / math.log(0.95 - 2 * se), 9.6, 1)
    approx("half-life at phi + 2 se", LN_HALF / math.log(0.95 + 2 * se), 22.6, 1)
    approx("half-life at the quoted lower bound 0.9303", LN_HALF / math.log(0.9303), 9.6, 1)
    approx("half-life at the quoted upper bound 0.96975", LN_HALF / math.log(0.96975), 22.6, 1)
    print("Kendall bias of phi_hat with an estimated mean: -(1 + 3 phi)/T")
    reps, n, phi = 20000, 250, 0.95
    paths = ar1_paths(rng, phi, n, reps)
    lag, y = paths[:, :-1], paths[:, 1:]
    lag_c = lag - lag.mean(axis=1, keepdims=True)
    y_c = y - y.mean(axis=1, keepdims=True)
    est = np.sum(lag_c * y_c, axis=1) / np.sum(lag_c * lag_c, axis=1)
    approx("Kendall approximation at phi = 0.95, T = 250", -(1 + 3 * phi) / n, -0.0154, 4)
    simulated("simulated mean bias of phi_hat", float(est.mean() - phi), -0.017, 4 * float(est.std()) / math.sqrt(reps) + 0.0005)
    print("Spurious regression of two independent random walks (card stat-arma-spurious-regression)")
    a = np.cumsum(rng.standard_normal((2000, 250)), axis=1)
    b = np.cumsum(rng.standard_normal((2000, 250)), axis=1)
    a_c, b_c = a - a.mean(axis=1, keepdims=True), b - b.mean(axis=1, keepdims=True)
    slope = np.sum(a_c * b_c, axis=1) / np.sum(b_c * b_c, axis=1)
    resid = a_c - slope[:, None] * b_c
    tstat = slope / np.sqrt(np.sum(resid * resid, axis=1) / 248 / np.sum(b_c * b_c, axis=1))
    frac = float(np.mean(np.abs(tstat) > 1.96))
    print(f"    share of |t| > 1.96 with no relationship ~ {frac:.3f}")
    assert frac > 0.5


def main() -> None:
    rng = np.random.default_rng(SEED)
    ar1_example(rng)
    ma1_and_roll(rng)
    ar2_example(rng)
    dickey_fuller(rng)
    ljung_box(rng)
    snippet_and_bias(rng)
    print("all ARMA checks passed")


if __name__ == "__main__":
    main()
