"""A miniature research take-home on synthetic data with a known answer, plus the problem-set arithmetic.

Backs 13-Interview-Playbook/08-Research-Case-Studies-and-Take-Homes.md.

Part A, the mini take-home: a 200-stock, 750-day panel where a signal has a true daily information
coefficient of 0.03. Raw data carries injected defects (missing returns, bad prints). The pipeline
runs data checks, a baseline, a time split, daily rank IC with t-stats, a dollar-neutral backtest
with turnover and costs, the Sharpe standard error, and a leakage demonstration.

Part B, closed-form problems quoted in the cards: Sharpe t-stats, years to significance, Lo (2002)
standard errors, multiple testing, the fundamental law, cost drag and break-even cost.

Run: uv run --no-project --with numpy python 13-Interview-Playbook/code/take_home_mini.py
"""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

ND = NormalDist()
EULER_GAMMA = 0.5772156649015329


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> None:
    """Print `label = value` and assert it matches the literal the note quotes, to tolerance and to the printed digits."""
    printed, quoted = (s.removeprefix("-") if float(s) == 0 else s for s in (f"{value:{fmt}}", f"{expected:{fmt}}"))
    print(f"{label} = {printed}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    assert printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"


# ---------------------------------------------------------------------------
# Part A: the mini take-home
# ---------------------------------------------------------------------------

N_STOCKS, N_DAYS, TRUE_IC, IDIO_VOL, MKT_VOL = 200, 750, 0.03, 0.02, 0.01
N_MISSING, N_BAD_PRINTS, OUTLIER_CUT = 1500, 5, 0.5
TRAIN_DAYS, COST_BP = 450, 5.0


def rank_rows(x: np.ndarray) -> np.ndarray:
    """Cross-sectional ranks per row (0..n-1); rows must be NaN-free."""
    return x.argsort(axis=1).argsort(axis=1).astype(float)


def row_corr(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a - a.mean(axis=1, keepdims=True)
    b = b - b.mean(axis=1, keepdims=True)
    return (a * b).sum(axis=1) / np.sqrt((a * a).sum(axis=1) * (b * b).sum(axis=1))


def daily_rank_ic(signal: np.ndarray, fwd: np.ndarray) -> np.ndarray:
    """Spearman IC per day over stocks with both values present."""
    out = np.empty(signal.shape[0])
    for t in range(signal.shape[0]):
        ok = ~(np.isnan(signal[t]) | np.isnan(fwd[t]))
        out[t] = row_corr(rank_rows(signal[t, ok][None]), rank_rows(fwd[t, ok][None]))[0]
    return out


def t_stat(x: np.ndarray) -> float:
    return float(x.mean() / x.std(ddof=1) * math.sqrt(len(x)))


def make_panel(seed: int = 2026) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """signal[t] predicts fwd[t] (the return from t to t+1); also returns clean fwd returns for the leakage demo."""
    rng = np.random.default_rng(seed)
    sig = rng.standard_normal((N_DAYS, N_STOCKS))
    eps = rng.standard_normal((N_DAYS, N_STOCKS))
    mkt = MKT_VOL * rng.standard_normal((N_DAYS, 1))
    fwd = mkt + IDIO_VOL * (TRUE_IC * sig + math.sqrt(1 - TRUE_IC**2) * eps)
    raw = fwd.copy()
    flat = rng.choice(N_DAYS * N_STOCKS, size=N_MISSING, replace=False)
    raw.flat[flat] = np.nan
    # A bad print: one day's price is recorded 10x too high, so the return into it is +900% and out of it -90%.
    placed = 0
    while placed < N_BAD_PRINTS:
        t, i = int(rng.integers(1, N_DAYS - 1)), int(rng.integers(0, N_STOCKS))
        if np.isnan(raw[t - 1 : t + 1, i]).any() or (np.abs(raw[t - 1 : t + 1, i]) > OUTLIER_CUT).any():
            continue
        raw[t - 1, i] = (1 + raw[t - 1, i]) * 10 - 1
        raw[t, i] = (1 + raw[t, i]) / 10 - 1
        placed += 1
    return sig, raw, fwd


def section_take_home() -> None:
    print("\n== A. Mini take-home ==")
    sig, raw, clean = make_panel()

    # Data checks (note: Worked example step 1; card int-takehome-bad-print-two-returns).
    n_missing = int(np.isnan(raw).sum())
    n_outliers = int((np.abs(raw) > OUTLIER_CUT).sum())
    check("missing returns found", n_missing, 1500, 0, ".0f")
    check("returns beyond +/-50% found", n_outliers, 10, 0, ".0f")
    fwd = np.where(np.abs(raw) > OUTLIER_CUT, np.nan, raw)
    check("share of cells usable after cleaning (%)", 100 * float(np.mean(~np.isnan(fwd))), 98.99, 0.005, ".2f")

    # Baseline and signal IC (Worked example steps 2 and 3).
    ic = daily_rank_ic(sig, fwd)
    prev = np.vstack([np.full((1, N_STOCKS), np.nan), fwd[:-1]])  # return from t-1 to t, known at t
    ic_rev = daily_rank_ic(-prev[1:], fwd[1:])
    check("baseline (1-day reversal) mean rank IC", float(ic_rev.mean()), 0.0019, 5e-5)
    check("baseline t-stat", t_stat(ic_rev), 0.73, 0.005, ".2f")
    tr, te = ic[:TRAIN_DAYS], ic[TRAIN_DAYS:]
    check("signal mean rank IC, train (450 days)", float(tr.mean()), 0.0295, 5e-5)
    check("signal IC t-stat, train", t_stat(tr), 8.25, 0.005, ".2f")
    check("signal mean rank IC, test (300 days)", float(te.mean()), 0.0263, 5e-5)
    check("signal IC t-stat, test", t_stat(te), 5.96, 0.005, ".2f")
    check("IC information ratio (mean / sd), test", float(te.mean() / te.std(ddof=1)), 0.34, 0.005, ".2f")

    # Backtest on the test period (step 4): dollar-neutral rank weights, gross exposure 1.
    s_te, r_te = sig[TRAIN_DAYS:], fwd[TRAIN_DAYS:]
    rk = rank_rows(s_te)
    w = rk - rk.mean(axis=1, keepdims=True)
    w /= np.abs(w).sum(axis=1, keepdims=True)
    pnl = np.nansum(w * r_te, axis=1)
    turnover = np.abs(np.diff(w, axis=0)).sum(axis=1)
    sr_d = pnl.mean() / pnl.std(ddof=1)
    sr_ann = sr_d * math.sqrt(252)
    se_ann = math.sqrt((1 + 0.5 * sr_d**2) / len(pnl)) * math.sqrt(252)
    net = pnl[1:] - turnover * COST_BP / 1e4
    # Card int-takehome-fundamental-law-check: IR ~ IC sqrt(breadth) with breadth = 200 stocks x 252 days.
    check("fundamental-law IR from the test IC", float(te.mean()) * math.sqrt(N_STOCKS * 252), 5.90, 0.005, ".2f")
    check("test gross annualised Sharpe", sr_ann, 5.50, 0.005, ".2f")
    check("Lo standard error of that Sharpe (annualised)", se_ann, 0.94, 0.005, ".2f")
    check("mean daily turnover (sum |dw|, gross = 1)", float(turnover.mean()), 1.34, 0.005, ".2f")
    check("mean daily gross return (bp)", float(pnl.mean() * 1e4), 6.08, 0.005, ".2f")
    check("break-even cost per unit traded (bp)", float(pnl[1:].mean() / turnover.mean() * 1e4), 4.53, 0.005, ".2f")
    check("test net annualised Sharpe at 5 bp", float(net.mean() / net.std(ddof=1) * math.sqrt(252)), -0.56, 0.005, ".2f")

    # Leakage demo (step 5; card int-takehome-leak-five-day): a 5-day momentum feature whose window
    # wrongly ends at t+1 contains the target return itself.
    win = np.cumsum(np.nan_to_num(clean), axis=0)
    good = np.full_like(clean, np.nan)
    leak = np.full_like(clean, np.nan)
    good[5:] = win[4:-1] - np.vstack([np.zeros((1, N_STOCKS)), win[:-5]])[: N_DAYS - 5]  # returns t-5..t-1
    leak[4:] = win[4:] - np.vstack([np.zeros((1, N_STOCKS)), win[:-5]])  # returns t-4..t, includes fwd[t]
    ic_good = daily_rank_ic(good[5:], clean[5:])
    ic_leak = daily_rank_ic(leak[5:], clean[5:])
    check("5-day momentum rank IC, correct window", float(ic_good.mean()), 0.0011, 5e-5)
    check("5-day momentum rank IC, window includes the target", float(ic_leak.mean()), 0.4290, 5e-5)
    check("Pearson IC implied by the leak, 1/sqrt(5)", 1 / math.sqrt(5), 0.4472, 5e-5)


# ---------------------------------------------------------------------------
# Part B: problem-set arithmetic
# ---------------------------------------------------------------------------


def expected_max_std_normal(n: int) -> float:
    """Bailey and Lopez de Prado (2014) approximation to E[max of n iid N(0,1)]."""
    return (1 - EULER_GAMMA) * ND.inv_cdf(1 - 1 / n) + EULER_GAMMA * ND.inv_cdf(1 - 1 / (n * math.e))


def section_problems() -> None:
    print("\n== B. Problem-set arithmetic ==")
    # int-takehome-sharpe-tstat
    check("t-stat of Sharpe 1.0 over 4 years", 1.0 * math.sqrt(4), 2.00, 1e-12, ".2f")
    # int-takehome-years-to-significance
    for sr, yrs in ((0.5, 16.0), (1.0, 4.0), (2.0, 1.0)):
        check(f"years for Sharpe {sr} to reach t = 2", (2 / sr) ** 2, yrs, 1e-12, ".1f")
    # int-takehome-six-month-holdout
    check("t-stat of Sharpe 2 over 6 months", 2 * math.sqrt(0.5), 1.41, 0.005, ".2f")
    # int-takehome-lo-se-annual
    check("Lo SE, Sharpe 1 from 10 annual returns", math.sqrt((1 + 0.5) / 10), 0.3873, 5e-5)
    # int-takehome-lo-se-daily
    sr_d = 1.0 / math.sqrt(252)
    check("Lo SE (annualised), Sharpe 1 from 5 years daily", math.sqrt((1 + 0.5 * sr_d**2) / 1260) * math.sqrt(252), 0.4477, 5e-5)
    # int-takehome-family-wise-error
    check("P(at least one false positive), 20 tests at 5%", 1 - 0.95**20, 0.6415, 5e-5)
    check("Bonferroni per-test level for 20 tests", 0.05 / 20, 0.0025, 1e-12)
    check("two-sided z hurdle at 0.0025", ND.inv_cdf(1 - 0.0025 / 2), 3.02, 0.005, ".2f")
    # int-takehome-fundamental-law
    check("breadth, 500 stocks x 12 rebalances", 500 * 12, 6000, 0, ".0f")
    check("IR from IC 0.02, 500 stocks rebalanced monthly", 0.02 * math.sqrt(500 * 12), 1.55, 0.005, ".2f")
    check("variance inflation 1 + 499 x 0.1", 1 + 499 * 0.1, 50.9, 1e-9, ".1f")
    check("effective bets, 500 stocks with pairwise correlation 0.1", 500 / (1 + 499 * 0.1), 9.82, 0.005, ".2f")
    # int-takehome-ic-tstat
    check("t-stat of mean IC 0.02 with sd 0.10 over 250 days", 0.02 / 0.10 * math.sqrt(250), 3.16, 0.005, ".2f")
    # int-takehome-cost-drag
    drag = 0.5 * 5e-4 * 252
    check("annual cost of 0.5 daily turnover at 5 bp (%)", 100 * drag, 6.30, 1e-9, ".2f")
    check("Sharpe lost at 10% annual vol", drag / 0.10, 0.63, 1e-9, ".2f")
    # int-takehome-break-even
    check("break-even cost, 8% gross alpha and 100x annual turnover (bp)", 0.08 / 100 * 1e4, 8.0, 1e-9, ".1f")
    # int-takehome-expected-max-noise
    bracket = expected_max_std_normal(100)
    check("E[max of 100 standard normals] (Bailey-Lopez de Prado)", bracket, 2.5306, 5e-5)
    check("expected best Sharpe of 100 noise strategies, 5 years daily", bracket * math.sqrt(1 / 5), 1.13, 0.005, ".2f")
    # Simulation cross-check of the expected maximum (seeded).
    rng = np.random.default_rng(11)
    sim = rng.standard_normal((20_000, 100)).max(axis=1).mean()
    check("simulated E[max of 100 standard normals] (seed 11)", float(sim), 2.51, 0.005, ".2f")


if __name__ == "__main__":
    section_take_home()
    section_problems()
    print("\nAll checks passed.")
