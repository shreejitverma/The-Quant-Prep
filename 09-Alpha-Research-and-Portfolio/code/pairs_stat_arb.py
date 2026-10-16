"""Pairs trading and residual statistical arbitrage on synthetic data.

Every number quoted in 06-Statistical-Arbitrage-and-Pairs-Trading.md is printed and asserted here.

1. Spurious regression: two independent random walks look "related" under naive OLS t-stats.
2. Engle-Granger: the 5% critical value of the residual ADF t-stat, by simulation.
3. A cointegrated pair: hedge ratio (and its asymmetry), ADF on the spread, OU fit by AR(1):
   mean-reversion speed, half-life, equilibrium standard deviation.
4. Entry and exit bands: out-of-sample trading of the OU spread for several entry thresholds,
   gross and net of costs.
5. Distance method (Gatev-Goetzmann-Rouwenhorst): pair selection by sum of squared deviations of
   normalised prices among 40 stocks with 5 planted cointegrated pairs.
6. Avellaneda-Lee residual stat arb: PCA factors, 60-day residual regressions, AR(1) s-scores,
   open at |s| > 1.25, close short at s < 0.75, close long at s > -0.50, kappa filter.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/pairs_stat_arb.py
"""

from __future__ import annotations

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> float:
    printed, quoted = (s.removeprefix("-") if float(s) == 0 else s for s in (f"{value:{fmt}}", f"{expected:{fmt}}"))
    print(f"{label}: {printed}")
    assert abs(value - expected) <= tol, f"{label}: {value} not within {tol} of {expected}"
    if expected != 0 or not fmt.endswith("e"):  # zero in scientific format is a bound (tol); all else prints the quoted literal
        assert printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"
    return value


def ols(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """OLS of y on [1, x]; returns coefficients, standard errors and residuals."""
    A = np.column_stack([np.ones_like(x), x])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    s2 = resid @ resid / (len(y) - 2)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
    return coef, se, resid


def adf_t(e: np.ndarray) -> float:
    """Dickey-Fuller t-stat of gamma in de_t = gamma e_{t-1} + u_t (no constant: residuals have mean 0)."""
    de, lag = np.diff(e), e[:-1]
    g = (lag @ de) / (lag @ lag)
    u = de - g * lag
    s2 = u @ u / (len(de) - 1)
    return float(g / np.sqrt(s2 / (lag @ lag)))


def ar1(x: np.ndarray) -> tuple[float, float, float]:
    """Fit x_{t+1} = a + b x_t + e; return a, b, residual variance."""
    (a, b), _, e = ols(x[1:], x[:-1])
    return float(a), float(b), float(e.var(ddof=2))


# ---------------------------------------------------------------------------
# 1 and 2. Spurious regression and the Engle-Granger critical value
# ---------------------------------------------------------------------------


def section_spurious_and_eg(seed: int = 0, reps: int = 4000, T: int = 500) -> None:
    print("== 1. Spurious regression; 2. Engle-Granger null distribution ==")
    rng = np.random.default_rng(seed)
    big_t, r2, eg = 0, [], []
    for _ in range(reps):
        x = np.cumsum(rng.standard_normal(T))
        y = np.cumsum(rng.standard_normal(T))
        coef, se, e = ols(y, x)
        big_t += abs(coef[1] / se[1]) > 1.96
        r2.append(1 - e.var() / y.var())
        eg.append(adf_t(e))
    check("independent random walks: fraction with |t| > 1.96 on the slope", big_t / reps, 0.895, 0.0006, ".3f")
    check("independent random walks: mean R^2", float(np.mean(r2)), 0.241, 0.0006, ".3f")
    check("Engle-Granger residual DF t-stat, simulated 5% critical value (T=500)", float(np.quantile(eg, 0.05)), -3.36, 0.006, ".2f")
    check("Engle-Granger residual DF t-stat, simulated 1% critical value (T=500)", float(np.quantile(eg, 0.01)), -3.93, 0.006, ".2f")
    # Single known series (plain Dickey-Fuller, demeaned) for comparison.
    df = []
    for _ in range(reps):
        w = np.cumsum(rng.standard_normal(T))
        df.append(adf_t(w - w.mean()))
    check("plain Dickey-Fuller (demeaned) simulated 5% critical value", float(np.quantile(df, 0.05)), -2.87, 0.006, ".2f")


# ---------------------------------------------------------------------------
# 3 and 4. A cointegrated pair, OU fit, trading bands
# ---------------------------------------------------------------------------

B_TRUE, BETA_TRUE, SIG_S = 0.95, 1.3, 0.005


def simulate_pair(rng: np.random.Generator, T: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    log_b = np.log(50.0) + np.cumsum(rng.normal(0.0, 0.015, T))
    s = np.zeros(T)
    for t in range(1, T):
        s[t] = B_TRUE * s[t - 1] + SIG_S * rng.standard_normal()
    log_a = 0.2 + BETA_TRUE * log_b + s
    return log_a, log_b, s


def backtest_bands(z: np.ndarray, spread: np.ndarray, entry: float, exit_: float, cost: float) -> dict[str, float]:
    """Long spread when z < -entry, short when z > entry, flat when z crosses back through +-exit."""
    pos = 0
    positions = np.zeros(len(z))
    trades = 0
    for t in range(len(z)):
        if pos == 0:
            if z[t] > entry:
                pos, trades = -1, trades + 1
            elif z[t] < -entry:
                pos, trades = 1, trades + 1
        elif (pos == 1 and z[t] >= -exit_) or (pos == -1 and z[t] <= exit_):
            pos = 0
        positions[t] = pos
    pnl = positions[:-1] * np.diff(spread)
    gross = float(pnl.sum())
    traded = float(np.abs(np.diff(np.concatenate([[0.0], positions]))).sum())
    return {
        "trades": trades,
        "gross": gross,
        "net": gross - cost * traded,
        "days_in": float((positions != 0).mean()),
        "per_trade": gross / max(trades, 1),
    }


def section_pair(seed: int = 1) -> None:
    print("== 3. A cointegrated pair ==")
    rng = np.random.default_rng(seed)
    T_fit, T_trade = 1000, 25_000
    log_a, log_b, _ = simulate_pair(rng, T_fit + T_trade)
    fa, fb = log_a[:T_fit], log_b[:T_fit]
    coef_ab, _, e = ols(fa, fb)
    coef_ba, _, _ = ols(fb, fa)
    check("hedge ratio, A on B", coef_ab[1], 1.305, 0.0006, ".3f")
    check("1 / hedge ratio, B on A", 1 / coef_ba[1], 1.308, 0.0006, ".3f")
    r2 = float(np.corrcoef(fa, fb)[0, 1] ** 2)
    check("R^2 of the levels regression", r2, 0.998, 0.0006, ".3f")
    check("product of the two slopes equals R^2", coef_ab[1] * coef_ba[1] - r2, 0.0e00, 1e-12, ".1e")
    check("Avellaneda-Lee kappa threshold 252/30 (per year)", 252 / 30, 8.4, 1e-12, ".1f")
    check("ADF t-stat of the fitted spread", adf_t(e), -4.78, 0.006, ".2f")
    a, b, v = ar1(e)
    kappa = -np.log(b)
    check("AR(1) coefficient b", b, 0.9545, 0.00006, ".4f")
    check("-ln(0.95)", -np.log(B_TRUE), 0.0513, 0.00005, ".4f")
    check("sqrt(1 - 0.95^2)", np.sqrt(1 - B_TRUE**2), 0.312, 0.0006, ".3f")
    check("estimated / true half-life", (np.log(2) / kappa) / (np.log(2) / -np.log(B_TRUE)), 1.102, 0.0006, ".3f")
    check("candidate pairs among 500 stocks", 500 * 499 // 2, 124750, 0, "d")
    check("true half-life (days)", np.log(2) / -np.log(B_TRUE), 13.51, 0.005, ".2f")
    check("estimated half-life (days)", np.log(2) / kappa, 14.89, 0.006, ".2f")
    sig_eq = np.sqrt(v / (1 - b**2))
    check("true equilibrium sd of the spread", SIG_S / np.sqrt(1 - B_TRUE**2), 0.0160, 0.00005, ".4f")
    check("estimated equilibrium sd of the spread", sig_eq, 0.0167, 0.00006, ".4f")
    check("estimated kappa (per year, 252 days)", 252 * kappa, 11.7, 0.06, ".1f")

    print("== 4. Entry and exit bands (out of sample, 25,000 days) ==")
    ta, tb = log_a[T_fit:], log_b[T_fit:]
    spread = ta - coef_ab[1] * tb
    mu = a / (1 - b) + coef_ab[0]
    z = (spread - mu) / sig_eq
    cost = 0.001  # 10 bp per unit of spread traded (both legs, one way)
    expected = {
        1.0: (5.0, 1.36, 0.113, 0.103, 0.668),
        1.5: (2.8, 1.85, 0.087, 0.081, 0.483),
        2.0: (1.5, 2.33, 0.057, 0.054, 0.309),
        2.5: (0.7, 2.82, 0.034, 0.032, 0.165),
    }
    yrs = T_trade / 252
    for entry, (e_rt, e_pt, e_g, e_n, e_in) in expected.items():
        res = backtest_bands(z, spread, entry, 0.0, cost)
        check(f"entry {entry}: round trips per year", res["trades"] / yrs, e_rt, 0.06, ".1f")
        check(f"entry {entry}: gross PnL per round trip (in sigma_eq)", res["per_trade"] / sig_eq, e_pt, 0.006, ".2f")
        check(f"entry {entry}: gross PnL per year (log units)", res["gross"] / yrs, e_g, 0.0006, ".3f")
        check(f"entry {entry}: net PnL per year (log units)", res["net"] / yrs, e_n, 0.0006, ".3f")
        check(f"entry {entry}: fraction of days in a position", res["days_in"], e_in, 0.0006, ".3f")


# ---------------------------------------------------------------------------
# 5. Distance method
# ---------------------------------------------------------------------------


def section_distance(seed: int = 3) -> None:
    print("== 5. Distance method ==")
    rng = np.random.default_rng(seed)
    n, n_pairs, T = 40, 5, 252 + 126
    common_mkt = np.cumsum(rng.normal(0.0003, 0.01, T))
    logp = np.zeros((T, n))
    for i in range(n):
        logp[:, i] = 0.8 * common_mkt + np.cumsum(rng.normal(0.0, 0.012, T))
    planted = []
    for k in range(n_pairs):
        i, j = 2 * k, 2 * k + 1
        s = np.zeros(T)
        for t in range(1, T):
            s[t] = 0.9 * s[t - 1] + 0.006 * rng.standard_normal()
        logp[:, j] = logp[:, i] + s  # stock j tracks stock i with a mean-reverting gap
        planted.append((i, j))
    form = np.exp(logp[:252] - logp[0])  # normalised prices start at 1
    ssd = {(i, j): float(((form[:, i] - form[:, j]) ** 2).sum()) for i in range(n) for j in range(i + 1, n)}
    top = sorted(ssd, key=ssd.get)[:n_pairs]
    check("candidate pairs", len(ssd), 780, 0, "d")
    check("planted pairs among the 5 smallest SSD", sum(p in planted for p in top), 5, 0, "d")
    # Trade each selected pair for 126 days: open at 2 formation sd, close when the gap crosses zero.
    pnl = []
    for i, j in top:
        gap_f = form[:, i] - form[:, j]
        sd = gap_f.std()
        px = np.exp(logp[252:] - logp[0])
        gap = px[:, i] - px[:, j]
        res = backtest_bands(gap / sd, gap, 2.0, 0.0, 0.0)
        pnl.append(res["gross"])
    check("total gap PnL over the trading period (normalised price units)", float(np.sum(pnl)), 0.446, 0.0006, ".3f")


# ---------------------------------------------------------------------------
# 6. Avellaneda-Lee residual statistical arbitrage
# ---------------------------------------------------------------------------


def section_avellaneda_lee(seed: int = 5) -> None:
    print("== 6. Avellaneda-Lee residual stat arb ==")
    rng = np.random.default_rng(seed)
    n, T, k, w_pca, w_reg = 100, 1500, 3, 252, 60
    loadings = rng.normal(0.0, 1.0, (n, k)) * np.array([0.6, 0.3, 0.3]) + np.array([1.0, 0.0, 0.0])
    f = rng.normal(0.0, 0.01, (T, k))
    b_true = np.exp(-rng.uniform(1 / 40, 1 / 5, n))  # residual mean-reversion times 5 to 40 days
    x = np.zeros((T, n))
    for t in range(1, T):
        x[t] = b_true * x[t - 1] + 0.008 * rng.standard_normal(n)
    noise = rng.normal(0.0, 0.012, (T, n))  # non-reverting idiosyncratic noise
    r = f @ loadings.T + np.diff(np.vstack([np.zeros(n), x]), axis=0) + noise

    pos = np.zeros(n)
    daily, n_open, n_trades, passed = [], [], 0, []
    cost = 0.001  # 10 bp per position change, covering stock and hedge legs
    for t in range(w_pca, T - 1):
        hist = r[t - w_pca : t]
        sd = hist.std(0)
        corr = np.corrcoef(hist, rowvar=False)
        evals, evecs = np.linalg.eigh(corr)
        v = evecs[:, -k:] / sd[:, None]  # eigenportfolio weights
        fac = r[: t + 1] @ v  # eigenportfolio returns up to today
        X = np.column_stack([np.ones(w_reg), fac[t - w_reg + 1 : t + 1]])
        Y = r[t - w_reg + 1 : t + 1]
        coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
        resid = Y - X @ coef
        cum = np.cumsum(resid, axis=0)
        x0, x1 = cum[:-1], cum[1:]
        x0m, x1m = x0.mean(0), x1.mean(0)
        bb = ((x0 - x0m) * (x1 - x1m)).sum(0) / ((x0 - x0m) ** 2).sum(0)
        aa = x1m - bb * x0m
        zeta = x1 - (aa + bb * x0)
        ok = (bb > 0) & (bb < 1)
        bb_safe = np.where(ok, bb, 0.5)
        kappa = -np.log(bb_safe) * 252
        m = aa / (1 - bb_safe)
        sig_eq = np.sqrt(zeta.var(0) / (1 - bb_safe**2))
        s = (cum[-1] - m) / sig_eq
        eligible = ok & (kappa > 252 / 30)
        passed.append(eligible.mean())
        new = pos.copy()
        new[(pos == 0) & eligible & (s < -1.25)] = 1
        new[(pos == 0) & eligible & (s > 1.25)] = -1
        new[(pos == 1) & (s > -0.50)] = 0
        new[(pos == -1) & (s < 0.75)] = 0
        n_trades += int(((pos == 0) & (new != 0)).sum())
        changes = np.abs(new - pos).sum()
        pos = new
        # Next-day residual return of each stock against its hedge.
        beta = coef[1:]  # k x n
        res_next = r[t + 1] - (r[t + 1] @ v) @ beta
        gross = pos @ res_next
        daily.append(((gross - cost * changes) / n, gross / n))
        n_open.append(np.abs(pos).sum())
    daily = np.array(daily)
    net, gross = daily[:, 0], daily[:, 1]
    sh = lambda z: float(z.mean() / z.std(ddof=1) * np.sqrt(252))  # noqa: E731
    check("fraction of stocks passing the kappa > 252/30 filter", float(np.mean(passed)), 0.994, 0.0006, ".3f")
    check("average open positions", float(np.mean(n_open)), 35.2, 0.06, ".1f")
    check("positions opened per day", n_trades / len(daily), 3.56, 0.006, ".2f")
    check("gross Sharpe", sh(gross), 3.12, 0.006, ".2f")
    check("net Sharpe at 10 bp per position change", sh(net), 1.81, 0.006, ".2f")


def section_pinned_residual(seed: int = 6, reps: int = 4000, w: int = 60) -> None:
    print("== 6b. Kappa filter on pure noise ==")
    rng = np.random.default_rng(seed)
    passed = 0
    for _ in range(reps):
        e = rng.standard_normal(w)
        cum = np.cumsum(e - e.mean())  # residuals of a regression with intercept sum to zero
        _, b, _ = ar1(cum)
        passed += 0 < b < 1 and -np.log(b) * 252 > 252 / 30
    check("pure-noise residuals passing the kappa > 252/30 filter", passed / reps, 0.990, 0.0006, ".3f")


def main() -> None:
    section_spurious_and_eg()
    section_pair()
    section_distance()
    section_avellaneda_lee()
    section_pinned_residual()


if __name__ == "__main__":
    main()
