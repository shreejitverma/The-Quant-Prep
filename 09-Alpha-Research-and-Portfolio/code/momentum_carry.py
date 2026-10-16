"""Momentum, short-term reversal and carry: construction details and crash risk on synthetic data.

Every number quoted in 05-Momentum-Mean-Reversion-and-Carry.md is printed and asserted here.

1. Cross-sectional momentum (Jegadeesh-Titman style): 12-1 versus 12-0 formation, one-month versus
   six-month overlapping holding, turnover, and the conditional beta of winners-minus-losers after
   bear markets (the momentum-crash mechanism).
2. Short-term reversal: gross return, turnover and break-even cost.
3. Time-series momentum (Moskowitz-Ooi-Pedersen style): sign of the 12-month return, positions
   scaled to 40% ex-ante volatility with an EWMA of center of mass 60 days, diversification across
   instruments.
4. Carry definitions (Koijen-Moskowitz-Pedersen-Vrugt): FX, equity index, commodity and bond
   carry plus roll-down, computed exactly.
5. Carry crash risk: skewness and Sharpe of a carry-like return stream with rare crashes.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/momentum_carry.py
"""

from __future__ import annotations

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> float:
    print(f"{label}: {value:{fmt}}")
    assert abs(value - expected) <= tol, f"{label}: {value} not within {tol} of {expected}"
    return value


def sharpe(x: np.ndarray, periods: int = 12) -> float:
    return float(x.mean() / x.std(ddof=1) * np.sqrt(periods))


# ---------------------------------------------------------------------------
# 1 and 2. Cross-sectional momentum and short-term reversal
# ---------------------------------------------------------------------------


def simulate_stocks(seed: int = 1, n: int = 500, months: int = 600) -> dict[str, np.ndarray]:
    """r = beta m + mu + liquidity shock - 0.3 * last month's shock + noise, with persistent mu."""
    rng = np.random.default_rng(seed)
    beta = np.clip(rng.normal(1.0, 0.5, n), 0.0, None)
    m = rng.normal(0.006, 0.045, months)
    mu = np.zeros((months, n))
    mu[0] = rng.normal(0.0, 0.006, n)
    for t in range(1, months):
        mu[t] = 0.95 * mu[t - 1] + np.sqrt(1 - 0.95**2) * rng.normal(0.0, 0.006, n)
    liq = rng.normal(0.0, 0.03, (months, n))
    liq_prev = np.vstack([np.zeros(n), liq[:-1]])
    r = beta * m[:, None] + mu + liq - 0.3 * liq_prev + rng.normal(0.0, 0.08, (months, n))
    return {"r": r, "m": m, "beta": beta}


def decile_weights(score: np.ndarray, long_high: bool = True) -> np.ndarray:
    """Equal-weight top decile long, bottom decile short; each leg has weight 1."""
    order = np.argsort(score)
    k = score.size // 10
    w = np.zeros(score.size)
    hi, lo = order[-k:], order[:k]
    if not long_high:
        hi, lo = lo, hi
    w[hi] = 1.0 / k
    w[lo] = -1.0 / k
    return w


def cumulative(r: np.ndarray, t: int, start: int, end: int) -> np.ndarray:
    """Compound return over months t-start .. t-end-1 (start > end >= 0)."""
    return np.prod(1.0 + r[t - start : t - end], axis=0) - 1.0


def section_cross_sectional(d: dict[str, np.ndarray]) -> None:
    print("== 1. Cross-sectional momentum ==")
    r, m, beta = d["r"], d["m"], d["beta"]
    months = r.shape[0]
    w121, w120, wrev = [], [], []
    for t in range(12, months):
        w121.append(decile_weights(cumulative(r, t, 12, 1)))
        w120.append(decile_weights(cumulative(r, t, 12, 0)))
        wrev.append(decile_weights(r[t - 1], long_high=False))
    w121, w120, wrev = np.array(w121), np.array(w120), np.array(wrev)
    fut = r[12:]
    ret121 = (w121 * fut).sum(1)
    ret120 = (w120 * fut).sum(1)
    retrev = (wrev * fut).sum(1)
    check("WML 12-1 mean return (% per month)", 100 * ret121.mean(), 0.38, 0.006, ".2f")
    check("WML 12-1 Sharpe (annualised)", sharpe(ret121), 0.51, 0.006, ".2f")
    check("WML 12-0 mean return (% per month)", 100 * ret120.mean(), 0.15, 0.006, ".2f")
    check("WML 12-0 Sharpe (annualised)", sharpe(ret120), 0.20, 0.006, ".2f")

    # Six overlapping cohorts (Jegadeesh-Titman K = 6): hold the average of the last six formations.
    k_hold = 6
    w_jt = np.array([w121[t - k_hold + 1 : t + 1].mean(0) for t in range(k_hold - 1, len(w121))])
    ret_jt = (w_jt * fut[k_hold - 1 :]).sum(1)
    check("WML 12-1 with K=6 overlapping cohorts, mean (% per month)", 100 * ret_jt.mean(), 0.38, 0.006, ".2f")
    check("WML 12-1 with K=6 overlapping cohorts, Sharpe", sharpe(ret_jt), 0.58, 0.006, ".2f")
    to_1 = np.abs(np.diff(w121, axis=0)).sum(1).mean()
    to_6 = np.abs(np.diff(w_jt, axis=0)).sum(1).mean()
    check("two-sided monthly turnover, K=1 (fraction of gross 2)", to_1 / 2, 0.604, 0.0006, ".3f")
    check("two-sided monthly turnover, K=6 (fraction of gross 2)", to_6 / np.abs(w_jt).sum(1).mean(), 0.231, 0.0006, ".3f")

    # Conditional beta: after a 12-month market decline, losers are the high-beta names.
    mkt = m[12:]
    past_mkt = np.array([np.prod(1 + m[t - 12 : t]) - 1 for t in range(12, months)])
    wml_beta = (w121 * beta).sum(1)
    bear = past_mkt < -0.10
    check("months after a 12-month market decline worse than -10%", int(bear.sum()), 124, 0, "d")
    check("WML ex-ante beta after bear markets", wml_beta[bear].mean(), -0.51, 0.006, ".2f")
    check("WML ex-ante beta otherwise", wml_beta[~bear].mean(), 0.15, 0.006, ".2f")
    rebound = bear & (mkt > 0.05)
    check("WML mean return in bear-state months with market up >5% (%)", 100 * ret121[rebound].mean(), -5.04, 0.006, ".2f")

    print("== 2. Short-term reversal ==")
    check("1-month reversal mean return (% per month)", 100 * retrev.mean(), 0.77, 0.006, ".2f")
    check("1-month reversal Sharpe", sharpe(retrev), 1.10, 0.006, ".2f")
    to_rev = np.abs(np.diff(wrev, axis=0)).sum(1).mean()
    check("1-month reversal two-sided turnover per month (traded / gross)", to_rev / 2, 1.815, 0.0006, ".3f")
    check("break-even one-way cost, reversal (bp)", 1e4 * retrev.mean() / to_rev, 21.3, 0.06, ".1f")
    check("break-even one-way cost, momentum K=1 (bp)", 1e4 * ret121.mean() / to_1, 31.4, 0.06, ".1f")
    check("break-even one-way cost, momentum K=6 (bp)", 1e4 * ret_jt.mean() / to_6, 83.2, 0.06, ".1f")
    check("drag from including month t-1 (% per month)", 100 * (ret121.mean() - ret120.mean()), 0.23, 0.006, ".2f")
    check("break-even cost ratio, K=6 over K=1", (ret_jt.mean() / to_6) / (ret121.mean() / to_1), 2.65, 0.006, ".2f")


def section_crash_arithmetic() -> None:
    print("== 1b. Crash arithmetic ==")
    beta_w, beta_l, rebound = 0.6, 1.6, 0.20
    check("WML beta when winners have 0.6 and losers 1.6", beta_w - beta_l, -1.0, 1e-12, ".1f")
    check("WML loss from beta alone in a +20% market rebound (%)", 100 * (beta_w - beta_l) * rebound, -20.0, 1e-9, ".1f")


# ---------------------------------------------------------------------------
# 3. Time-series momentum
# ---------------------------------------------------------------------------


def section_tsmom(seed: int = 2) -> None:
    print("== 3. Time-series momentum ==")
    rng = np.random.default_rng(seed)
    n_inst, years, dpm = 24, 30, 21
    months = 12 * years
    days = months * dpm
    ann_vol = np.repeat([0.15, 0.06, 0.10, 0.25], 6)  # equities, bonds, FX, commodities
    cls = np.repeat(np.arange(4), 6)
    # Persistent monthly drift (in units of per-day Sharpe), correlated within an asset class.
    drift = np.zeros((months, n_inst))
    for t in range(1, months):
        common = rng.standard_normal(4)[cls]
        drift[t] = 0.9 * drift[t - 1] + np.sqrt(1 - 0.9**2) * 0.05 * (0.6 * common + 0.8 * rng.standard_normal(n_inst))
    common_d = rng.standard_normal((days, 4))[:, cls]
    z = 0.4 * common_d + np.sqrt(1 - 0.16) * rng.standard_normal((days, n_inst))
    daily_vol = ann_vol / np.sqrt(252)
    r = daily_vol * (np.repeat(drift, dpm, axis=0) + z)

    com = 60.0
    delta = com / (1 + com)
    check("EWMA decay for center of mass 60 days", delta, 0.98361, 0.00001, ".5f")
    check("EWMA half-life for center of mass 60 days (days)", np.log(0.5) / np.log(delta), 41.9, 0.05, ".1f")
    var = np.zeros((days, n_inst))
    var[0] = daily_vol**2
    for t in range(1, days):
        var[t] = delta * var[t - 1] + (1 - delta) * r[t - 1] ** 2
    month_ret = r.reshape(months, dpm, n_inst).sum(1)
    pos, ret = [], []
    for mo in range(12, months):
        past = month_ret[mo - 12 : mo].sum(0)
        sig_ann = np.sqrt(var[mo * dpm] * 252)  # estimate available at the start of month mo
        p = np.sign(past) * 0.40 / sig_ann
        pos.append(p)
        ret.append(p * month_ret[mo])
    pos, ret = np.array(pos), np.array(ret)
    realised = ret.std(axis=0, ddof=1) * np.sqrt(12)
    check("mean realised vol per instrument after 40% scaling", realised.mean(), 0.413, 0.0006, ".3f")
    check("min realised vol per instrument", realised.min(), 0.359, 0.0006, ".3f")
    check("max realised vol per instrument", realised.max(), 0.440, 0.0006, ".3f")
    single = np.array([sharpe(ret[:, i]) for i in range(n_inst)])
    port = ret.mean(axis=1)
    check("average single-instrument TSMOM Sharpe", single.mean(), 0.24, 0.006, ".2f")
    check("diversified TSMOM portfolio Sharpe", sharpe(port), 1.18, 0.006, ".2f")
    check("diversified TSMOM portfolio vol (annual)", port.std(ddof=1) * np.sqrt(12), 0.084, 0.0006, ".3f")
    rho = np.corrcoef(ret, rowvar=False)[np.triu_indices(n_inst, 1)].mean()
    check("average pairwise correlation of instrument TSMOM returns", rho, -0.000, 0.0006, ".3f")
    check("diversification multiplier sqrt(N/(1+(N-1)rho))", np.sqrt(n_inst / (1 + (n_inst - 1) * rho)), 4.91, 0.006, ".2f")
    check("single-instrument Sharpe times multiplier", single.mean() * np.sqrt(n_inst / (1 + (n_inst - 1) * rho)), 1.18, 0.006, ".2f")


# ---------------------------------------------------------------------------
# 4. Carry definitions
# ---------------------------------------------------------------------------


def section_carry() -> None:
    print("== 4. Carry ==")
    # FX: long the investment currency, funded in the funding currency, one-year forward by CIP.
    r_inv, r_fund, spot = 0.05, 0.01, 1.0
    fwd = spot * (1 + r_fund) / (1 + r_inv)
    check("FX carry (S - F)/F (%)", 100 * (spot - fwd) / fwd, 3.96, 0.005, ".2f")
    # Equity index future, one year, simple compounding.
    s, r, d = 5000.0, 0.04, 0.015
    f = s * (1 + r - d)
    check("equity index one-year futures price", f, 5125.0, 1e-9, ".1f")
    check("equity index carry (S - F)/F (%)", 100 * (s - f) / f, -2.44, 0.005, ".2f")
    # Commodity curve in backwardation: nearby 80, contract one year later 76.
    near, far = 80.0, 76.0
    check("commodity carry of a long deferred future, curve unchanged (%)", 100 * (near - far) / far, 5.26, 0.005, ".2f")

    # Bond: buy a 10-year 4% annual-coupon bond at par; in one year it is a 9-year bond.
    def price(coupon: float, y: float, n: int) -> float:
        cf = np.full(n, coupon * 100.0)
        cf[-1] += 100.0
        return float((cf / (1 + y) ** np.arange(1, n + 1)).sum())

    p0 = price(0.04, 0.04, 10)
    p1_unchanged = price(0.04, 0.038, 9)  # curve unchanged: the 9-year point yields 3.8%
    p1_flat = price(0.04, 0.04, 9)
    repo = 0.03
    total = (p1_unchanged + 4.0 - p0) / p0 - repo
    check("10-year bond price at 4% yield", p0, 100.00, 1e-9, ".2f")
    check("price after one year if the curve is unchanged (9y at 3.8%)", p1_unchanged, 101.50, 0.005, ".2f")
    check("bond carry plus roll-down over repo (%)", 100 * total, 2.50, 0.005, ".2f")
    check("of which coupon minus repo (%)", 100 * (4.0 / p0 - repo), 1.00, 1e-9, ".2f")
    check("of which roll-down (%)", 100 * (p1_unchanged - p1_flat) / p0, 1.50, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 5. Carry crash risk
# ---------------------------------------------------------------------------


def section_carry_crash(seed: int = 4) -> None:
    print("== 5. Carry crash risk ==")
    rng = np.random.default_rng(seed)
    months = 600
    normal = rng.normal(0.007, 0.02, months)
    crash = rng.random(months) < 0.02
    x = np.where(crash, rng.normal(-0.10, 0.03, months), normal)
    z = (x - x.mean()) / x.std()
    skew = float((z**3).mean())
    kurt = float((z**4).mean())
    check("carry-like stream: crash months", int(crash.sum()), 15, 0, "d")
    check("carry-like stream: annualised Sharpe", sharpe(x), 0.57, 0.006, ".2f")
    check("carry-like stream: Sharpe excluding crash months", sharpe(x[~crash]), 1.22, 0.006, ".2f")
    check("carry-like stream: skewness", skew, -1.71, 0.006, ".2f")
    check("carry-like stream: kurtosis", kurt, 9.44, 0.006, ".2f")
    check("carry-like stream: worst month (%)", 100 * x.min(), -13.4, 0.06, ".1f")


def main() -> None:
    d = simulate_stocks()
    section_cross_sectional(d)
    section_crash_arithmetic()
    section_tsmom()
    section_carry()
    section_carry_crash()


if __name__ == "__main__":
    main()
