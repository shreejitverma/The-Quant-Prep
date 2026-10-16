"""End-to-end alpha research case studies on synthetic data, with every number asserted.

Backs the note 15-Alpha-Research-Case-Studies.md.

Case A: cross-sectional short-term residual reversal in a 500-stock universe.
    Neutralise against sectors and beta, measure rank IC and its decay, backtest with the
    position shift, charge costs on turnover, run a delay test, search the lookback and
    deflate the winner's Sharpe (Bailey and Lopez de Prado 2014).
Case B: time-series momentum on 24 synthetic futures, volatility-scaled as in
    Moskowitz, Ooi and Pedersen (2012); lookback search, train/test split and deflated Sharpe.
Case C: critique of a flawed backtest. Each flaw is switched on alone against a clean
    baseline so its Sharpe inflation is measured: survivorship, missing position shift,
    full-sample normalisation and a parameter search over pure noise.

Conventions: Sharpe ratios are annualised with sqrt(periods per year) unless labelled
per period; the deflated Sharpe ratio uses per-period Sharpes throughout, as in note 08.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/research_case_studies.py
"""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

ND = NormalDist()
A_NEUTRAL_TABLE = np.array([-1.62, 0.13, 0.71, 1.12, 1.19, 1.41, 1.53, 1.64, 1.59, 1.38])
A_RAW_TABLE = np.array([-1.54, 0.08, 0.63, 1.07, 1.26, 1.49, 1.60, 1.63, 1.54, 1.30])
B_TABLE = np.array(
    [
        0.45,
        0.74,
        0.73,
        0.83,
        0.64,
        0.62,
        0.71,
        0.85,
        0.79,
        0.91,
        0.76,
        0.80,
        0.77,
        0.80,
        0.95,
        0.90,
        0.98,
        0.96,
        0.99,
        0.92,
        0.91,
        0.85,
        0.84,
        0.88,
    ]
)
EULER_GAMMA = 0.5772156649015329


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> float:
    """Print a computed value and assert it is within tol of the expected value."""
    print(f"{label}: {value:{fmt}}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +- {tol}"
    if expected != 0:  # the printed value must equal the literal the note quotes, at the printed rounding
        assert f"{value:{fmt}}" == f"{expected:{fmt}}", f"{label}: prints {value:{fmt}}, note quotes {expected:{fmt}}"
    return value


# ---------------------------------------------------------------------------
# Statistics shared by all cases
# ---------------------------------------------------------------------------


def sharpe(x: np.ndarray, periods: int = 1) -> float:
    """Mean over standard deviation (ddof 1), scaled by sqrt(periods)."""
    return float(x.mean() / x.std(ddof=1) * math.sqrt(periods))


def skew_kurt(x: np.ndarray) -> tuple[float, float]:
    """Sample skewness and (non-excess) kurtosis from population moments."""
    d = x - x.mean()
    m2 = float((d**2).mean())
    return float((d**3).mean() / m2**1.5), float((d**4).mean() / m2**2)


def expected_max(n: int) -> float:
    """Approximate E[max of n iid standard normals] (Bailey and Lopez de Prado 2014)."""
    return (1 - EULER_GAMMA) * ND.inv_cdf(1 - 1 / n) + EULER_GAMMA * ND.inv_cdf(1 - 1 / (n * math.e))


def psr(sr: float, sr_star: float, t: int, skew: float, kurt: float) -> float:
    """Probabilistic Sharpe ratio; sr and sr_star per period, kurt non-excess (normal = 3)."""
    denom = math.sqrt(1 - skew * sr + (kurt - 1) / 4 * sr**2)
    return ND.cdf((sr - sr_star) * math.sqrt(t - 1) / denom)


def deflated_sharpe(selected: np.ndarray, trial_sharpes: np.ndarray) -> tuple[float, float]:
    """Return (SR0 per period, DSR) for the selected return series given all trials' per-period Sharpes."""
    sr0 = float(np.sqrt(trial_sharpes.var(ddof=1))) * expected_max(len(trial_sharpes))
    s, k = skew_kurt(selected)
    return sr0, psr(sharpe(selected), sr0, len(selected), s, k)


def row_ranks(x: np.ndarray) -> np.ndarray:
    """Cross-sectional ranks 0..N-1 of each row (continuous data, so no ties)."""
    return np.argsort(np.argsort(x, axis=1), axis=1).astype(float)


def row_corr(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Pearson correlation of each row of a with the same row of b."""
    a = a - a.mean(1, keepdims=True)
    b = b - b.mean(1, keepdims=True)
    return (a * b).sum(1) / np.sqrt((a**2).sum(1) * (b**2).sum(1))


def verify_dsr_against_note_08() -> None:
    """Note 08 worked example: best of 100 trials, annualised Sharpe 2, sd 0.5, 5y daily, skew -1, kurt 6."""
    print("== DSR implementation check against note 08 ==")
    sr = 2 / math.sqrt(252)
    sr0 = math.sqrt(0.25 / 252) * expected_max(100)
    check("expected max bracket N=10", expected_max(10), 1.5746, 1e-3)
    check("expected max bracket N=100", expected_max(100), 2.5306, 1e-3)
    check("note 08 SR0 annualised", sr0 * math.sqrt(252), 1.265, 1e-3, ".3f")
    check("note 08 DSR", psr(sr, sr0, 1260, -1, 6), 0.9375, 1e-3)


# ---------------------------------------------------------------------------
# Case A: cross-sectional residual reversal
# ---------------------------------------------------------------------------


def simulate_equity_panel(rng: np.random.Generator, n: int, t: int) -> dict[str, np.ndarray]:
    """Daily returns: market * beta + sector + hidden styles + idiosyncratic with a decaying reversal.

    The idiosyncratic part is e_t = u_t - c * m_t with m_t = u_{t-1} + delta * m_{t-1}, so a
    shock is partly reversed over the following days with geometric decay delta (half-life 3.1 days).
    """
    n_sectors, n_hidden = 10, 5
    sector = np.repeat(np.arange(n_sectors), n // n_sectors)
    beta = rng.uniform(0.5, 1.5, n)
    idio_vol = rng.uniform(0.01, 0.03, n)
    hidden_load = rng.standard_normal((n, n_hidden))
    f_mkt = rng.normal(0.0003, 0.01, t)
    f_sec = rng.normal(0.0, 0.01, (t, n_sectors))
    f_hid = rng.normal(0.0, 0.005, (t, n_hidden))
    u = rng.standard_normal((t, n)) * idio_vol
    delta = 0.8
    c = 0.02 + 0.08 * rng.standard_normal(t)  # reversal strength varies day to day
    m = np.zeros(n)
    e = np.empty((t, n))
    for i in range(t):
        e[i] = u[i] - c[i] * m
        m = u[i] + delta * m
    r = f_mkt[:, None] * beta + f_sec[:, sector] + f_hid @ hidden_load.T + e
    x = np.column_stack([(sector[:, None] == np.arange(n_sectors)).astype(float), beta])
    return {"r": r, "x": x, "beta": beta, "styles": hidden_load}


def residual_projector(x: np.ndarray) -> np.ndarray:
    """M = I - X (X'X)^-1 X': removes sector and beta exposure from any cross-section."""
    return np.eye(x.shape[0]) - x @ np.linalg.solve(x.T @ x, x.T)


def trailing_sum(a: np.ndarray, k: int) -> np.ndarray:
    """Sum of the last k rows ending at each row (NaN before k rows exist)."""
    c = np.cumsum(a, axis=0)
    out = np.full_like(a, np.nan)
    out[k - 1] = c[k - 1]
    out[k:] = c[k:] - c[:-k]
    return out


def book(signal: np.ndarray, proj: np.ndarray | None) -> np.ndarray:
    """z-score, winsorise at +-3, neutralise (or demean), scale to unit gross."""
    z = (signal - signal.mean(1, keepdims=True)) / signal.std(1, keepdims=True)
    z = np.clip(z, -3, 3)
    z = z @ proj if proj is not None else z - z.mean(1, keepdims=True)
    return z / np.abs(z).sum(1, keepdims=True)


def run_book(w: np.ndarray, r: np.ndarray, cost: float, lag: int = 1) -> tuple[np.ndarray, np.ndarray]:
    """Weights w[j] set at the close of day j earn r[j + lag]; trading into w[j] costs |w[j] - w[j-1]| * cost.

    Returns (net daily pnl, two-sided turnover); both start at j = 1 so every day pays for its trade.
    """
    j_end = w.shape[0] - lag
    gross = (w[1:j_end] * r[1 + lag : j_end + lag]).sum(1)
    turnover = np.abs(w[1:j_end] - w[: j_end - 1]).sum(1)
    return gross - cost * turnover, turnover


def case_a() -> None:
    print("\n== Case A: cross-sectional residual reversal ==")
    rng = np.random.default_rng(20261015)
    n, burn, t_eval = 500, 30, 1260
    panel = simulate_equity_panel(rng, n, burn + t_eval)
    r, x = panel["r"], panel["x"]
    proj = residual_projector(x)
    resid = r @ proj  # cross-sectional residual returns (M is symmetric)
    sl = slice(burn, None)

    # Signal: minus the 5-day residual return, the pre-registered hypothesis
    k0 = 5
    sig = -trailing_sum(resid, k0)[sl]
    fwd_resid = resid[sl]
    r_ev = r[sl]
    w = book(sig, proj)
    check("A max |net beta exposure| of book", float(np.abs(w @ panel["beta"]).max()), 0.0, 1e-12, ".2e")

    ic = row_corr(row_ranks(sig[:-1]), row_ranks(fwd_resid[1:]))
    ic_mean, ic_sd = float(ic.mean()), float(ic.std(ddof=1))
    check("A mean daily rank IC (k=5)", ic_mean, 0.0191, 2e-4)
    check("A sd of daily rank IC", ic_sd, 0.1341, 2e-4)
    check("A annualised IC information ratio", ic_mean / ic_sd * math.sqrt(252), 2.26, 0.006, ".2f")
    check("A IC t-stat", ic_mean / ic_sd * math.sqrt(len(ic)), 5.1, 0.06, ".1f")
    check("A fraction of days with positive IC", float((ic > 0).mean()), 0.55, 0.006, ".2f")

    decay = [float(row_corr(row_ranks(sig[:-h]), row_ranks(fwd_resid[h:])).mean()) for h in range(1, 6)]
    for h, (v, e) in enumerate(zip(decay, [0.0191, 0.0176, 0.0142, 0.0122, 0.0097], strict=True), start=1):
        check(f"A rank IC at lag {h}", v, e, 6e-5)

    gross, to = run_book(w, r_ev, 0.0)
    check("A gross annualised Sharpe", sharpe(gross, 252), 2.43, 0.006, ".2f")
    check("A gross annual return on unit gross (%)", float(gross.mean() * 252 * 100), 16.0, 0.06, ".1f")
    check("A gross daily return on unit gross (bp)", float(gross.mean() * 1e4), 6.37, 0.006, ".2f")
    check("A daily two-sided turnover (fraction of gross)", float(to.mean()), 0.647, 2e-3, ".3f")
    rho = float(row_corr(sig[1:], sig[:-1]).mean())
    check("A day-to-day cross-sectional signal autocorrelation", rho, 0.787, 2e-3, ".3f")
    check("A turnover implied by sqrt(2(1 - rho))", math.sqrt(2 * (1 - rho)), 0.653, 2e-3, ".3f")
    net5, _ = run_book(w, r_ev, 5e-4)
    check("A net Sharpe at 5 bp per unit traded", sharpe(net5, 252), 1.19, 0.006, ".2f")
    check("A break-even cost (bp per unit traded)", float(gross.mean() / to.mean() * 1e4), 9.8, 0.06, ".1f")

    s5, k5 = skew_kurt(net5)
    check("A pre-registered k=5 net PSR(0)", psr(sharpe(net5), 0.0, len(net5), s5, k5), 0.9960, 2e-4)

    delayed, _ = run_book(w, r_ev, 0.0, lag=2)
    check("A delay test: gross Sharpe with one extra day", sharpe(delayed, 252), 2.36, 0.006, ".2f")

    # Fuller risk model: also neutralise against the five style exposures
    proj_full = residual_projector(np.column_stack([x, panel["styles"]]))
    resid_full = r @ proj_full
    sig_full = -trailing_sum(resid_full, k0)[sl]
    w_full = book(sig_full, proj_full)
    ic_full = row_corr(row_ranks(sig_full[:-1]), row_ranks(resid_full[sl][1:]))
    check("A style-neutral mean rank IC", float(ic_full.mean()), 0.0220, 2e-4)
    check("A style-neutral sd of rank IC", float(ic_full.std(ddof=1)), 0.1158, 2e-4)
    gross_full, to_full = run_book(w_full, r_ev, 0.0)
    check("A style-neutral gross Sharpe", sharpe(gross_full, 252), 3.11, 0.006, ".2f")
    net_full, _ = run_book(w_full, r_ev, 5e-4)
    check("A style-neutral net Sharpe at 5 bp", sharpe(net_full, 252), 1.57, 0.006, ".2f")

    # Without neutralisation: same signal on raw returns, demeaned only
    sig_raw = -trailing_sum(r, k0)[sl]
    w_raw = book(sig_raw, None)
    gross_raw, _ = run_book(w_raw, r_ev, 0.0)
    check("A raw (un-neutralised) gross Sharpe", sharpe(gross_raw, 252), 2.46, 0.006, ".2f")
    check("A raw book annualised vol (%)", float(gross_raw.std(ddof=1) * math.sqrt(252) * 100), 6.8, 0.06, ".1f")
    check("A neutral book annualised vol (%)", float(gross.std(ddof=1) * math.sqrt(252) * 100), 6.6, 0.06, ".1f")

    # Lookback search, net of 5 bp: 10 lookbacks x neutral/raw = 20 trials
    trial_sr, trial_net = [], {}
    for k in range(1, 11):
        for neutral in (True, False):
            base = resid if neutral else r
            wk = book(-trailing_sum(base, k)[sl], proj if neutral else None)
            netk, _ = run_book(wk, r_ev, 5e-4)
            trial_sr.append(sharpe(netk))
            trial_net[(k, neutral)] = netk
    trial_sr_arr = np.array(trial_sr)
    table = np.round(trial_sr_arr.reshape(10, 2) * math.sqrt(252), 2)
    print("A net Sharpe by lookback 1..10 (neutral):", " ".join(f"{v:.2f}" for v in table[:, 0]))
    print("A net Sharpe by lookback 1..10 (raw):    ", " ".join(f"{v:.2f}" for v in table[:, 1]))
    assert np.allclose(table[:, 0], A_NEUTRAL_TABLE, rtol=0.0, atol=1e-9), table[:, 0]
    assert np.allclose(table[:, 1], A_RAW_TABLE, rtol=0.0, atol=1e-9), table[:, 1]
    # Why the short lookbacks differ by design: they trade far more, so costs eat their gross alpha.
    for k, exp_to, exp_share in [(1, 1.418, 2.09), (2, 1.008, 0.94), (5, 0.647, 0.51)]:
        gk, tok = run_book(book(-trailing_sum(resid, k)[sl], proj), r_ev, 0.0)
        check(f"A lookback {k} neutral: daily two-sided turnover", float(tok.mean()), exp_to, 2e-3, ".3f")
        check(f"A lookback {k} neutral: 5 bp cost as a share of gross alpha", float(5e-4 * tok.mean() / gk.mean()), exp_share, 0.006, ".2f")
    best_idx = int(np.argmax(trial_sr_arr))
    best_key = list(trial_net)[best_idx]
    best = trial_net[best_key]
    print(f"A best trial: lookback {best_key[0]} neutral {best_key[1]}")
    assert best_key == (8, True)
    check("A best trial net Sharpe", sharpe(best, 252), 1.64, 0.006, ".2f")
    sr0, dsr = deflated_sharpe(best, trial_sr_arr)
    check("A SR0 annualised (20 trials)", sr0 * math.sqrt(252), 1.84, 0.006, ".2f")
    check("A deflated Sharpe ratio", dsr, 0.33, 0.006, ".2f")

    # Train on first 3 years, test on last 2
    split = 756
    is_sr = np.array([sharpe(v[:split]) for v in trial_net.values()])
    pick = list(trial_net)[int(np.argmax(is_sr))]
    print(f"A in-sample pick: lookback {pick[0]} neutral {pick[1]}")
    assert pick == (8, False)
    check("A pick in-sample net Sharpe", sharpe(trial_net[pick][:split], 252), 1.83, 0.006, ".2f")
    check("A pick out-of-sample net Sharpe", sharpe(trial_net[pick][split:], 252), 1.32, 0.006, ".2f")


# ---------------------------------------------------------------------------
# Case B: time-series momentum on futures
# ---------------------------------------------------------------------------


def case_b() -> None:
    print("\n== Case B: volatility-scaled time-series momentum ==")
    rng = np.random.default_rng(2012)
    n_assets, warm, t_eval = 24, 48, 360
    t = warm + t_eval
    vol = np.linspace(0.05, 0.40, n_assets) / math.sqrt(12)  # monthly
    phi, kappa = 0.95, 0.2  # drift persistence; sd(drift)/sd(noise)
    mu = np.zeros((t, n_assets))
    eta = rng.standard_normal((t, n_assets)) * math.sqrt(1 - phi**2)
    for i in range(1, t):
        mu[i] = phi * mu[i - 1] + eta[i]
    common = rng.standard_normal((t, 1))
    eps = math.sqrt(0.2) * common + math.sqrt(0.8) * rng.standard_normal((t, n_assets))
    r = vol * (kappa * mu + eps)

    def tsmom(lookback: int, scaled: bool) -> tuple[np.ndarray, np.ndarray]:
        """Position at month end j: sign of trailing return times 40% / ex-ante vol; earns r[j+1]."""
        trail = trailing_sum(r, lookback)
        ex_ante = np.full_like(r, np.nan)
        for j in range(23, t):
            ex_ante[j] = r[j - 23 : j + 1].std(axis=0, ddof=1) * math.sqrt(12)
        size = 0.40 / ex_ante if scaled else np.ones_like(r)
        pos = np.sign(trail) * size
        pnl_i = pos[warm - 1 : -1] * r[warm:]
        return pnl_i.mean(1), pnl_i

    port, pnl_i = tsmom(12, True)
    check("B TSMOM(12) scaled annualised Sharpe", sharpe(port, 12), 0.80, 0.006, ".2f")
    check("B TSMOM(12) scaled annualised vol (%)", float(port.std(ddof=1) * math.sqrt(12) * 100), 10.2, 0.06, ".1f")
    port_u, pnl_u = tsmom(12, False)
    check("B TSMOM(12) unscaled annualised Sharpe", sharpe(port_u, 12), 0.74, 0.006, ".2f")

    def top4_share(p: np.ndarray) -> float:
        tot = p.mean(1)
        contrib = np.array([np.cov(p[:, i] / p.shape[1], tot)[0, 1] for i in range(p.shape[1])])
        return float(contrib[-4:].sum() / tot.var(ddof=1))

    check("B risk share of 4 highest-vol assets, unscaled", top4_share(pnl_u), 0.39, 0.006, ".2f")
    check("B risk share of 4 highest-vol assets, scaled", top4_share(pnl_i), 0.19, 0.006, ".2f")

    sr_by_l = {lb: tsmom(lb, True)[0] for lb in range(1, 25)}
    trial = np.array([sharpe(v) for v in sr_by_l.values()])
    table = np.round(trial * math.sqrt(12), 2)
    print("B Sharpe by lookback 1..24:", " ".join(f"{v:.2f}" for v in table))
    assert np.allclose(table, B_TABLE, rtol=0.0, atol=1e-9), table
    best_l = int(np.argmax(trial)) + 1
    print(f"B best lookback over 24 trials: {best_l}")
    assert best_l == 19
    check("B best lookback annualised Sharpe", sharpe(sr_by_l[best_l], 12), 0.99, 0.006, ".2f")
    sr0, dsr = deflated_sharpe(sr_by_l[best_l], trial)
    check("B SR0 annualised (24 trials)", sr0 * math.sqrt(12), 0.25, 0.006, ".2f")
    check("B deflated Sharpe ratio", dsr, 0.9999, 2e-4)
    half = t_eval // 2
    is_sr = np.array([sharpe(v[:half]) for v in sr_by_l.values()])
    pick = int(np.argmax(is_sr)) + 1
    print(f"B in-sample pick (first 15 years): {pick}")
    assert pick == 24
    check("B pick out-of-sample Sharpe (last 15 years)", sharpe(sr_by_l[pick][half:], 12), 0.70, 0.006, ".2f")


# ---------------------------------------------------------------------------
# Case C: critique of a flawed backtest
# ---------------------------------------------------------------------------


def decile_ls(signal: np.ndarray, fwd: np.ndarray, valid: np.ndarray | None = None) -> np.ndarray:
    """Long top decile, short bottom decile of signal (equal weight), earning fwd (same row index)."""
    out = np.empty(signal.shape[0])
    for j in range(signal.shape[0]):
        ok = np.ones(signal.shape[1], bool) if valid is None else valid[j]
        s, f = signal[j, ok], fwd[j, ok]
        q = max(1, len(s) // 10)
        order = np.argsort(s)
        out[j] = f[order[-q:]].mean() - f[order[:q]].mean()
    return out


def case_c_survivorship() -> None:
    print("\n== Case C1: survivorship in a buy-the-losers backtest ==")
    rng = np.random.default_rng(1993)
    n, warm, t_eval = 1000, 12, 240
    t = warm + t_eval
    ret = np.empty((t, n))
    ids = np.empty((t, n), dtype=np.int64)
    age = np.zeros(n, dtype=np.int64)  # months of returns observed for the current stock in each slot
    cur = np.arange(n)
    next_id = n
    replace = np.zeros(n, bool)
    for j in range(t):
        if replace.any():
            k = int(replace.sum())
            cur[replace] = np.arange(next_id, next_id + k)
            next_id += k
            age[replace] = 0
        ids[j] = cur
        trail = np.zeros(n)
        has12 = age >= 12
        if j >= 12:
            trail = np.log1p(ret[j - 12 : j]).sum(0)
        distressed = has12 & (trail < -0.5)
        hazard = 0.001 + 0.01 * distressed
        delist = rng.random(n) < hazard
        rj = rng.normal(0.006, 0.045) + rng.normal(0.0, 0.10, n)
        rj = np.maximum(rj, -0.9)
        rj[delist] = -0.3  # delisting return
        ret[j] = rj
        age += 1
        replace = delist
    final_ids = ids[-1]
    print(f"C1 stocks ever listed: {next_id}, survivors at the end: {n}")
    assert next_id == 1519
    # Decision at month end j uses 12 trailing returns of the same stock; it earns ret[j+1].
    trail12 = trailing_sum(np.log1p(ret), 12)
    same_stock = np.zeros((t, n), bool)
    for j in range(11, t):
        same_stock[j] = (ids[j - 11 : j + 1] == ids[j]).all(0)
    alive_next = ids[1:] == ids[:-1]  # stock at j still trades in j+1 (its delisting month included)
    elig = same_stock[warm - 1 : -1] & alive_next[warm - 1 :]
    surv = np.isin(ids[warm - 1 : -1], final_ids)
    sig = -trail12[warm - 1 : -1]
    fwd = ret[warm:]
    true_ls = decile_ls(sig, fwd, elig)
    surv_ls = decile_ls(sig, fwd, elig & surv)
    check("C1 losers-minus-winners Sharpe, point-in-time universe", sharpe(true_ls, 12), -0.74, 0.006, ".2f")
    check("C1 losers-minus-winners Sharpe, survivors only", sharpe(surv_ls, 12), 0.05, 0.006, ".2f")
    check("C1 annual return bias from survivorship (%)", float((surv_ls.mean() - true_ls.mean()) * 12 * 100), 4.4, 0.06, ".1f")
    ew_true = np.array([fwd[j, elig[j]].mean() for j in range(t_eval)])
    ew_surv = np.array([fwd[j, elig[j] & surv[j]].mean() for j in range(t_eval)])
    check("C1 equal-weight universe return bias (% per year)", float((ew_surv.mean() - ew_true.mean()) * 12 * 100), 1.5, 0.06, ".1f")


def case_c_noise_panel() -> None:
    print("\n== Case C2: look-ahead, full-sample normalisation and search over noise ==")
    rng = np.random.default_rng(7)
    n, warm, t_eval = 1000, 48, 120
    t = warm + t_eval
    r = rng.normal(0.006, 0.045, (t, 1)) + rng.normal(0.0, 0.08, (t, n))  # no cross-sectional alpha

    # Clean momentum 12-1 style without skip, and the same without the position shift
    trail12 = trailing_sum(r, 12)
    clean = decile_ls(trail12[warm - 1 : -1], r[warm:])
    no_shift = decile_ls(trail12[warm:], r[warm:])
    check("C2 clean 12m momentum Sharpe (zero alpha)", sharpe(clean, 12), 0.34, 0.006, ".2f")
    check("C2 same signal without the position shift", sharpe(no_shift, 12), 26.2, 0.06, ".1f")

    # Time-series normalisation of the trailing return: full-sample versus expanding statistics
    full_mean = r[warm:].mean(0)
    sig_full = -(trail12 - 12 * full_mean)
    exp_mean = np.cumsum(r, axis=0) / np.arange(1, t + 1)[:, None]
    sig_exp = -(trail12 - 12 * exp_mean)
    leak = decile_ls(sig_full[warm - 1 : -1], r[warm:])
    causal = decile_ls(sig_exp[warm - 1 : -1], r[warm:])
    check("C2 contrarian with full-sample mean, Sharpe", sharpe(leak, 12), 2.13, 0.006, ".2f")
    leak_ic = row_corr(row_ranks(sig_full[warm - 1 : -1]), row_ranks(r[warm:])).mean()
    check("C2 leaked rank IC from full-sample mean", float(leak_ic), 0.0274, 2e-4)
    check("C2 leaked IC predicted sqrt(12) / T", math.sqrt(12) / t_eval, 0.0289, 1e-4)
    check("C2 contrarian with expanding mean, Sharpe", sharpe(causal, 12), -0.21, 0.006, ".2f")

    # Parameter search: lookback 1..24, with and without a 1-month skip, momentum or contrarian: 96 trials
    trials = {}
    for lb in range(1, 25):
        for skip in (0, 1):
            s = trailing_sum(r, lb)
            if skip:
                s = np.vstack([np.full((1, n), np.nan), s[:-1]])
            for sign in (1, -1):
                trials[(lb, skip, sign)] = decile_ls(sign * s[warm - 1 : -1], r[warm:])
    tsr = np.array([sharpe(v) for v in trials.values()])
    best_key = list(trials)[int(np.argmax(tsr))]
    best = trials[best_key]
    print(f"C2 best of 96 noise trials: lookback {best_key[0]} skip {best_key[1]} sign {best_key[2]}")
    assert best_key == (8, 1, 1)
    check("C2 best noise trial annualised Sharpe", sharpe(best, 12), 0.69, 0.006, ".2f")
    check("C2 expected max bracket for N=96", expected_max(96), 2.52, 0.006, ".2f")
    sr0, dsr = deflated_sharpe(best, tsr)
    check("C2 SR0 annualised", sr0 * math.sqrt(12), 0.89, 0.006, ".2f")
    check("C2 deflated Sharpe ratio of the best noise trial", dsr, 0.27, 0.006, ".2f")
    s, k = skew_kurt(best)
    check("C2 naive PSR(0) of the best noise trial", psr(sharpe(best), 0.0, len(best), s, k), 0.98, 0.006, ".2f")


if __name__ == "__main__":
    verify_dsr_against_note_08()
    case_a()
    case_b()
    case_c_survivorship()
    case_c_noise_panel()
    print("\nall checks passed")
