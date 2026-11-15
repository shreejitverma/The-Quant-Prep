"""Rule validation, calibration and overfitting controls: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/08-Quantitative-Rule-Validation-and-Calibration.md`.
Independent routes used here:
- the Brier score of the ten-trade log computed directly as a mean squared error, against Murphy's (1973)
  reliability - resolution + uncertainty partition of the same forecasts;
- the expected calibration error rebuilt from 1,000 synthetic forecast records that match the three
  buckets, binned from the raw records, against the bucket summary;
- the CSCV combination count by math.comb and by explicit enumeration, and the probability of backtest
  overfitting for pure-noise strategies against its exact value of 1/2 by seeded simulation (five standard
  errors across independent replications);
- the minimum track record length of Bailey and Lopez de Prado (2012) against a seeded simulation of
  Sharpe estimates at that length, which must exceed zero 95% of the time (five standard errors);
- the correlation of 14-day and 15-day Wilder RSI on seeded random walks.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_08_validation.py`.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

SEED = 8


def check(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def phi_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def phi_inv(p: float) -> float:
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if phi_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def brier_score(f: np.ndarray, o: np.ndarray) -> float:
    return float(np.mean((f - o) ** 2))


def brier_two_class(f: np.ndarray, o: np.ndarray) -> float:
    return float(np.mean((f - o) ** 2 + ((1 - f) - (1 - o)) ** 2))


def brier() -> None:
    f = np.array([0.8] * 5 + [0.3] * 5)
    o = np.array([1, 1, 1, 0, 1, 0, 0, 1, 0, 0])
    direct = brier_score(f, o)
    base = o.mean()
    rel = res = 0.0
    for value in np.unique(f):
        mask = f == value
        w = mask.mean()
        rel += w * (value - o[mask].mean()) ** 2
        res += w * (o[mask].mean() - base) ** 2
    unc = base * (1 - base)
    check("uncertainty", unc, "0.2500")
    check("reliability", rel, "0.0050")
    check("resolution", res, "0.0900")
    check("Brier score, Murphy partition", rel - res + unc, "0.1650")
    check("Brier score, direct mean squared error", direct, "0.1650")
    check("Brier skill score against always 0.5", 1 - direct / 0.25, "0.34")
    f_half, f_perfect, f_inverse = np.full(o.size, 0.5), o.astype(float), 1.0 - o
    check("Brier score of always forecasting 0.5", brier_score(f_half, o), "0.25")
    check("Brier score of perfect foresight", brier_score(f_perfect, o), "0.0")
    check("Brier score of complete inversion", brier_score(f_inverse, o), "1.0")
    check("Brier's original two-class score of the same forecasts", brier_two_class(f, o), "0.3300")
    check("two-class score of complete inversion (the upper bound)", brier_two_class(f_inverse, o), "2.0")
    check("log loss of f = 0.99 on an event that fails", -math.log(0.01), "4.605")


def ece() -> None:
    buckets = [(0.25, 400, 0.20), (0.55, 400, 0.45), (0.85, 200, 0.65)]
    forecasts, outcomes = [], []
    for fbar, n, obar in buckets:
        forecasts += [fbar] * n
        wins = round(n * obar)
        outcomes += [1] * wins + [0] * (n - wins)
    f, o = np.array(forecasts), np.array(outcomes)
    edges = [0.0, 0.4, 0.7, 1.0]
    parts = []
    for lo, hi in itertools.pairwise(edges):
        mask = (f >= lo) & (f < hi) if hi < 1.0 else (f >= lo)
        parts.append(mask.mean() * abs(f[mask].mean() - o[mask].mean()))
    check("bucket 1 weighted gap", parts[0], "0.020")
    check("bucket 2 weighted gap", parts[1], "0.040")
    check("bucket 3 weighted gap", parts[2], "0.040")
    check("ECE from raw records", sum(parts), "0.100")
    summary = sum(n / 1000 * abs(fb - ob) for fb, n, ob in buckets)
    assert abs(summary - sum(parts)) < 1e-12
    check("mean forecast", f.mean(), "0.49")
    check("observed frequency", o.mean(), "0.39")


def pbo_noise(rng: np.random.Generator) -> None:
    check("CSCV combinations for S = 16 blocks, C(16, 8)", math.comb(16, 8), "12,870")
    assert sum(1 for _ in itertools.combinations(range(16), 8)) == math.comb(16, 8)
    s_blocks, n_strat, t_obs, reps = 8, 50, 800, 200
    combos = list(itertools.combinations(range(s_blocks), s_blocks // 2))
    check("CSCV combinations for S = 8 blocks", len(combos), "70")
    pbos = []
    for _ in range(reps):
        m = rng.standard_normal((t_obs, n_strat))
        blocks = np.array_split(m, s_blocks)
        below = 0
        for c in combos:
            is_ = np.vstack([blocks[i] for i in c])
            oos = np.vstack([blocks[i] for i in range(s_blocks) if i not in c])
            sr_is = is_.mean(0) / is_.std(0, ddof=1)
            sr_oos = oos.mean(0) / oos.std(0, ddof=1)
            best = int(np.argmax(sr_is))
            rank = int(np.sum(sr_oos <= sr_oos[best]))  # 1 = worst out of sample
            omega = rank / (n_strat + 1)
            below += math.log(omega / (1 - omega)) <= 0
        pbos.append(below / len(combos))
    pbos = np.array(pbos)
    se = pbos.std(ddof=1) / math.sqrt(reps)
    assert abs(pbos.mean() - 0.5) < 5 * se, f"PBO under noise {pbos.mean()} vs 0.5 (se {se})"
    print(f"PBO of pure-noise strategies (seed {SEED}, {reps} replications) = {pbos.mean():.3f} +/- {se:.3f}; exact 0.5")


def min_trl(sr: float, g3: float, g4: float, p: float = 0.95) -> float:
    return 1 + (1 - g3 * sr + (g4 - 1) / 4 * sr**2) * (phi_inv(p) / sr) ** 2


def track_record(rng: np.random.Generator) -> None:
    sr_d = 1 / math.sqrt(252)
    n_norm = min_trl(sr_d, 0.0, 3.0)
    check("MinTRL for annual SR 1.0, daily normal returns, 95% one-sided, years", n_norm / 252, "2.71")
    years_t2 = (4 * (1 + 0.5 * sr_d**2) / sr_d**2 + 1) / 252
    check("years of daily data for t = 2.0 at annual SR 1.0", years_t2, "4.0")
    n_obs = math.ceil(n_norm)
    sims = rng.normal(sr_d, 1.0, size=(20_000, n_obs))
    est = sims.mean(axis=1) / sims.std(axis=1, ddof=1)
    share = float(np.mean(est > 0))
    se = math.sqrt(0.95 * 0.05 / est.size)
    assert abs(share - 0.95) < 5 * se, f"share of positive SR estimates {share} vs 0.95"
    print(f"simulated share of positive Sharpe estimates at MinTRL (seed {SEED}) = {share:.4f} +/- {se:.4f}")
    n_skew = min_trl(sr_d, -1.0, 6.0)
    check("MinTRL with skew -1 and kurtosis 6, daily, years", n_skew / 252, "2.89")
    check("increase from non-normality on daily data, percent", 100 * (n_skew / n_norm - 1), "6.6")
    sr_m = 1 / math.sqrt(12)
    m_norm, m_skew = min_trl(sr_m, 0.0, 3.0), min_trl(sr_m, -1.0, 6.0)
    check("MinTRL monthly, normal, years", m_norm / 12, "2.90")
    check("MinTRL monthly, skew -1 and kurtosis 6, years", m_skew / 12, "3.85")
    check("increase from non-normality on monthly data, percent", 100 * (m_skew / m_norm - 1), "32.7")


def wilder_rsi(prices: np.ndarray, n: int) -> np.ndarray:
    change = np.diff(prices)
    up, down = np.maximum(change, 0.0), np.maximum(-change, 0.0)
    au, ad = up[:n].mean(), down[:n].mean()
    out = np.empty(len(change) - n + 1)
    out[0] = 100 * au / (au + ad)
    for k, (u, d) in enumerate(zip(up[n:], down[n:], strict=True), 1):
        au = (au * (n - 1) + u) / n
        ad = (ad * (n - 1) + d) / n
        out[k] = 100 * au / (au + ad)
    return out


def rsi_correlation(rng: np.random.Generator) -> None:
    cors = []
    for _ in range(20):
        p = 100 + np.cumsum(rng.standard_normal(20_000))
        r14, r15 = wilder_rsi(p, 14)[1:], wilder_rsi(p, 15)
        cors.append(np.corrcoef(r14, r15)[0, 1])
    print(f"correlation of 14-day and 15-day RSI on 20 random walks (seed {SEED}): min {min(cors):.4f}")
    assert min(cors) > 0.99


def expectancy() -> None:
    check("expectancy at 85% wins of 1R and losses of 10R, R", 0.85 * 1 - 0.15 * 10, "-0.65")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    brier()
    ece()
    pbo_noise(rng)
    track_record(rng)
    rsi_correlation(rng)
    expectancy()
    print("cited: Aronson (2006) tested 6,402 rules on the S&P 500, 1980 to 2005")
    print("cited: rule-spec inputs, 5-bar swing low, retest within 0.5%, volume above 1.25 x SMA_50(volume)")
    print("cited: illustrative forecasts, 70% over 5 days, a 99% coin-toss call, an 80% forecast true 60% of the time")
    print("all rule-validation numbers check out")
