"""Evaluating an alternative-data signal: leakage, point-in-time traps and the fundamental law.

Backs 09-Alpha-Research-and-Portfolio/14-Alternative-Data-and-Feature-Engineering.md.

1. Fundamental law: simulated IR of alpha-weighted bets against IC * sqrt(N) (exact form
   IC sqrt(N) / sqrt(1 + IC^2)), the collapse of breadth when scores and residuals share a common
   component, and the recovery from cross-sectionally demeaning the scores.
2. Full-sample versus expanding normalisation of a feature that co-moves with the price level:
   the full-sample z-score manufactures a Sharpe out of nothing.
3. Publication lag: the same feature joined on its event date versus its knowledge date.
4. Vendor backfill: history reconstructed only for names covered at launch.
5. Panel evaluation of a noisy alt-data feature: IC, rank IC, IC IR, decay, half-life,
   autocorrelation and turnover, the effect of smoothing, and the effect of coverage.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/alt_data_signal_eval.py
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> None:
    printed, quoted = (s.removeprefix("-") if float(s) == 0 else s for s in (f"{value:{fmt}}", f"{expected:{fmt}}"))
    print(f"{label}: {printed}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    if expected != 0 or not fmt.endswith("e"):  # zero in scientific format is a bound (tol); all else prints the quoted literal
        assert printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"


def row_corr(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Pearson correlation of each row of a with the same row of b."""
    a = a - a.mean(axis=1, keepdims=True)
    b = b - b.mean(axis=1, keepdims=True)
    return (a * b).sum(axis=1) / np.sqrt((a * a).sum(axis=1) * (b * b).sum(axis=1))


def row_ranks(a: np.ndarray) -> np.ndarray:
    return np.argsort(np.argsort(a, axis=1), axis=1).astype(float)


# ---------------------------------------------------------------------------
# 1. Fundamental law
# ---------------------------------------------------------------------------


def simulate_ir(n: int, ic: float, rho_z: float, rho_e: float, demean: bool, periods: int, seed: int) -> float:
    """Per-period IR of R_t = sum_i z_i r_i / sigma_i with r_i / sigma_i = IC z_i + sqrt(1 - IC^2) e_i.
    Scores share a common component with weight rho_z, residuals one with weight rho_e."""
    rng = np.random.default_rng(seed)
    out = []
    chunk = 2000
    for _ in range(periods // chunk):
        h = rng.standard_normal((chunk, 1))
        g = rng.standard_normal((chunk, 1))
        z = math.sqrt(rho_z) * h + math.sqrt(1 - rho_z) * rng.standard_normal((chunk, n))
        e = math.sqrt(rho_e) * g + math.sqrt(1 - rho_e) * rng.standard_normal((chunk, n))
        r = ic * z + math.sqrt(1 - ic * ic) * e
        w = z - z.mean(axis=1, keepdims=True) if demean else z
        out.append((w * r).sum(axis=1))
    pnl = np.concatenate(out)
    return float(pnl.mean() / pnl.std())


def section_fundamental_law() -> None:
    print("\n== 1. Fundamental law of active management ==")
    n, ic, periods = 500, 0.02, 20_000
    naive = ic * math.sqrt(n)
    exact = ic * math.sqrt(n) / math.sqrt(1 + ic * ic)
    check("IC sqrt(N), N=500, IC=0.02 (per period)", naive, 0.4472, 1e-4)
    check("exact IC sqrt(N)/sqrt(1+IC^2)", exact, 0.4471, 1e-4)
    check("annualised with 12 rebalances: IC sqrt(12 N)", ic * math.sqrt(12 * n), 1.5492, 1e-4)
    # History needed for a target t-stat: t = IR_annual * sqrt(years).
    check("years of history for t = 2 at annual IR 0.5", (2 / 0.5) ** 2, 16.00, 1e-12, ".2f")
    check("years of history for t = 3 at annual IR 1.55", (3 / (ic * math.sqrt(12 * n))) ** 2, 3.75, 0.005, ".2f")
    sim = simulate_ir(n, ic, 0.0, 0.0, False, periods, 1)
    check("simulated IR, independent bets (per period)", sim, 0.4534, 0.02)

    rho_z, rho_e = 0.25, 0.20
    rho_bet = rho_z * rho_e
    n_eff = n / (1 + (n - 1) * rho_bet)
    check("bet correlation rho_z * rho_e", rho_bet, 0.0500, 1e-12)
    check("effective breadth N / (1 + (N-1) rho)", n_eff, 19.27, 0.01, ".2f")
    heuristic = ic * math.sqrt(n_eff)
    var_r = ic * ic * 2 * n * (1 + (n - 1) * rho_z**2) + (1 - ic * ic) * n * (1 + (n - 1) * rho_bet)
    exact_corr = ic * n / math.sqrt(var_r)
    check("heuristic IC sqrt(N_eff)", heuristic, 0.0878, 1e-4)
    check("exact IR with correlated bets", exact_corr, 0.0878, 1e-4)
    sim_corr = simulate_ir(n, ic, rho_z, rho_e, False, periods, 2)
    check("simulated IR with correlated bets", sim_corr, 0.0841, 0.02)

    exact_dm = ic * math.sqrt((n - 1) * (1 - rho_z) / (2 * ic * ic * (1 - rho_z) + (1 - ic * ic) * (1 - rho_e)))
    check("exact IR after demeaning scores", exact_dm, 0.4325, 1e-4)
    check("IR gain from demeaning (exact)", exact_dm / exact_corr, 4.93, 0.005, ".2f")
    sim_dm = simulate_ir(n, ic, rho_z, rho_e, True, periods, 3)
    check("simulated IR after demeaning scores", sim_dm, 0.4147, 0.02)


# ---------------------------------------------------------------------------
# 2. Full-sample versus expanding normalisation
# ---------------------------------------------------------------------------


def section_normalisation_leak() -> None:
    print("\n== 2. Full-sample versus expanding z-score ==")
    rng = np.random.default_rng(7)
    paths, t_len, burn = 200, 2520, 252
    full, expanding = [], []
    idx = np.arange(1, t_len + 1)
    for _ in range(paths):
        r = 0.01 * rng.standard_normal(t_len)
        logp = np.cumsum(r)
        x = logp + 0.05 * rng.standard_normal(t_len)  # feature tracks the price level, predicts nothing
        z_full = (x - x.mean()) / x.std()
        mean_exp = np.cumsum(x) / idx
        var_exp = np.cumsum(x * x) / idx - mean_exp**2
        z_exp = (x - mean_exp) / np.sqrt(np.maximum(var_exp, 1e-12))
        nxt = r[1:]  # position at t earns r_{t+1}
        for z, store in ((z_full, full), (z_exp, expanding)):
            pnl = -np.sign(z[burn:-1]) * nxt[burn:]
            store.append(pnl.mean() / pnl.std() * math.sqrt(252))
    full_m, exp_m = float(np.mean(full)), float(np.mean(expanding))
    check("mean Sharpe, full-sample z-score (200 noise paths)", full_m, 0.31, 0.006, ".2f")
    check("mean Sharpe, expanding z-score", exp_m, 0.01, 0.006, ".2f")
    check("fraction of paths with positive Sharpe, full-sample", float(np.mean(np.array(full) > 0)), 0.88, 0.006, ".2f")


# ---------------------------------------------------------------------------
# 3. Publication lag
# ---------------------------------------------------------------------------


def section_publication_lag() -> None:
    print("\n== 3. Event date versus knowledge date ==")
    w = np.array([0.40, 0.25, 0.15, 0.12, 0.08])  # price absorbs news y_t over 5 days through other channels
    s_e, lag = 2.0, 3
    sd_r = math.sqrt(float(w @ w) + s_e**2)
    check("sd of daily return", sd_r, 2.065, 5e-4, ".3f")
    ic_event = w[1] / (math.sqrt(2) * sd_r)  # x_t used at t to predict r_{t+1}
    ic_known = w[lag + 1] / (math.sqrt(2) * sd_r)  # x_{t-3}, the latest value actually known at t
    check("correlation with r_{t+1}, joined on event date (wrong)", ic_event, 0.0856, 1e-4)
    check("correlation with r_{t+1}, joined on knowledge date (right)", ic_known, 0.0274, 1e-4)
    check("fraction of apparent signal that is real", ic_known / ic_event, 0.32, 1e-12, ".2f")
    rng = np.random.default_rng(11)
    t_len = 400_000
    y = rng.standard_normal(t_len)
    x = y + rng.standard_normal(t_len)
    r = np.convolve(y, w)[:t_len] + s_e * rng.standard_normal(t_len)
    sim_event = float(np.corrcoef(x[10:-1], r[11:])[0, 1])
    sim_known = float(np.corrcoef(x[10 - lag : -1 - lag], r[11:])[0, 1])
    check("simulated, event date", sim_event, 0.0835, 0.005)
    check("simulated, knowledge date", sim_known, 0.0239, 0.005)


# ---------------------------------------------------------------------------
# 4. Vendor backfill
# ---------------------------------------------------------------------------


def section_backfill() -> None:
    print("\n== 4. Vendor backfill bias ==")
    rng = np.random.default_rng(5)
    n, pre, post, vol = 2000, 120, 60, 0.10
    ret = 0.008 + vol * rng.standard_normal((pre + post, n))
    cum_pre = ret[:pre].sum(axis=0)
    covered = cum_pre > np.median(cum_pre)  # vendor covers today's winners and reconstructs their history
    excess_pre = float((ret[:pre, covered].mean() - ret[:pre].mean()) * 12)
    excess_post = float((ret[pre:, covered].mean() - ret[pre:].mean()) * 12)
    analytic = vol * math.sqrt(2 / math.pi) / math.sqrt(pre) * 12
    check("analytic backfill excess, top half on 10y cumulative return (per year)", analytic, 0.0874, 1e-4)
    check("simulated covered-minus-universe, backfilled years (per year)", excess_pre, 0.0877, 0.004)
    check("simulated covered-minus-universe, live years (per year)", excess_post, 0.0022, 0.006)


# ---------------------------------------------------------------------------
# 5. Panel evaluation of a noisy alt-data feature
# ---------------------------------------------------------------------------


def section_panel() -> None:
    print("\n== 5. Panel evaluation: IC, decay, turnover, smoothing, coverage ==")
    rng = np.random.default_rng(21)
    n, t_len, rho, beta, s_x, theta = 1000, 1500, 0.95, 0.05, 1.0, 0.2
    f = np.empty((t_len, n))
    f[0] = rng.standard_normal(n)
    for t in range(1, t_len):
        f[t] = rho * f[t - 1] + math.sqrt(1 - rho * rho) * rng.standard_normal(n)
    x = f + s_x * rng.standard_normal((t_len, n))
    r_next = beta * f + rng.standard_normal((t_len, n))  # r_next[t] is the return from t to t+1
    xs = np.empty_like(x)
    xs[0] = x[0]
    for t in range(1, t_len):
        xs[t] = (1 - theta) * xs[t - 1] + theta * x[t]

    sd_r = math.sqrt(beta**2 + 1)
    ic1 = beta / (math.sqrt(1 + s_x**2) * sd_r)
    check("analytic IC(1)", ic1, 0.0353, 1e-4)
    burn = 50
    ics = row_corr(x[burn:], r_next[burn:])
    rics = row_corr(row_ranks(x[burn:]), row_ranks(r_next[burn:]))
    check("mean daily IC", float(ics.mean()), 0.0360, 0.003)
    check("1/sqrt(N)", 1 / math.sqrt(n), 0.0316, 1e-4)
    check("sd of daily IC", float(ics.std()), 0.0314, 0.002)
    check("IC IR (daily)", float(ics.mean() / ics.std()), 1.15, 0.006, ".2f")
    check("IC t-stat", float(ics.mean() / ics.std() * math.sqrt(len(ics))), 43.7, 4.0, ".1f")
    check("mean daily rank IC", float(rics.mean()), 0.0342, 0.003)
    check("fraction of days with positive IC", float(np.mean(ics > 0)), 0.87, 0.006, ".2f")

    for k, exp, sim_exp in [(1, 0.0353, 0.036), (5, 0.0288, 0.029), (10, 0.0223, 0.023), (20, 0.0133, 0.014)]:
        analytic = ic1 * rho ** (k - 1)
        check(f"analytic IC at lag {k}", analytic, exp, 1e-4)
        sim = float(row_corr(x[burn : t_len - k + 1], r_next[burn + k - 1 :]).mean())
        check(f"simulated IC at lag {k}", sim, sim_exp, 5e-4, ".3f")
    check("IC half-life ln2/ln(1/rho)", math.log(2) / math.log(1 / rho), 13.51, 0.01, ".2f")

    ac_raw = rho / (1 + s_x**2)
    check("analytic feature autocorrelation", ac_raw, 0.475, 1e-12, ".3f")
    check("simulated feature autocorrelation", float(row_corr(x[burn:-1], x[burn + 1 :]).mean()), 0.475, 0.005, ".3f")
    check("turnover of a signal-proportional book sqrt(2(1-ac))", math.sqrt(2 * (1 - ac_raw)), 1.0247, 1e-4)

    u = 1 - theta
    cov_sf = theta / (1 - u * rho)
    var_s = theta**2 * ((1 + u * rho) / ((1 - u * u) * (1 - u * rho)) + s_x**2 / (1 - u * u))
    ic_smooth = cov_sf / math.sqrt(var_s) * beta / sd_r
    check("analytic IC(1) of EMA-smoothed feature", ic_smooth, 0.0432, 1e-4)
    ic_s = row_corr(xs[burn:], r_next[burn:])
    check("simulated IC(1) of smoothed feature", float(ic_s.mean()), 0.0439, 0.003)
    ac_s_analytic = u + theta**2 * rho / ((1 - u * rho) * var_s)
    check("analytic smoothed feature autocorrelation", ac_s_analytic, 0.971, 5e-4, ".3f")
    ac_s = float(row_corr(xs[burn:-1], xs[burn + 1 :]).mean())
    check("simulated smoothed feature autocorrelation", ac_s, 0.971, 0.005, ".3f")
    check("smoothed turnover sqrt(2(1-ac))", math.sqrt(2 * (1 - ac_s_analytic)), 0.241, 5e-4, ".3f")

    cover = rng.random(n) < 0.4
    ics_c = row_corr(x[burn:, cover], r_next[burn:, cover])
    ratio = float((ics_c.mean() / ics_c.std()) / (ics.mean() / ics.std()))
    check("sqrt(coverage) for 40% coverage", math.sqrt(0.4), 0.632, 5e-4, ".3f")
    check("IC IR ratio, 40% coverage vs full", ratio, 0.64, 0.006, ".2f")


if __name__ == "__main__":
    section_fundamental_law()
    section_normalisation_leak()
    section_publication_lag()
    section_backfill()
    section_panel()
    print("\nAll checks passed.")
