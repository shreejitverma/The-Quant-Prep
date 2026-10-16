"""Point-in-time data: survivorship, index-membership, timing and restatement biases, quantified.

Every number quoted in 02-Point-in-Time-Data-and-Survivorship.md is printed and asserted here.

1. As-of join on publication time versus the naive "latest vintage by period end" join.
2. Time zones: the same UTC timestamp falls before or after the New York close depending on DST.
3. Survivorship: a simulated universe with performance delistings (-30%) and takeovers (+25%),
   backtested on (a) full point-in-time data with delisting returns, (b) point-in-time data
   that silently drops the delisting-month return, (c) today's survivors only.
4. Index membership: backtesting today's top-500 names over history versus point-in-time members.
5. Timing and restatements: IC of an earnings signal stamped at period end, at the filing date
   with the first release, and at the filing date with the restated value.
6. Corporate actions: split-adjusted returns and the back-adjusted price-filter trap.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/pit_survivorship.py
"""

from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> float:
    print(f"{label}: {value:{fmt}}")
    assert abs(value - expected) <= tol, f"{label}: {value} not within {tol} of {expected}"
    return value


# ---------------------------------------------------------------------------
# 1. As-of join
# ---------------------------------------------------------------------------

# (fiscal period end, publication date, EPS); the last Q4 row is an amendment (restatement).
RECORDS = [
    (dt.date(2024, 9, 30), dt.date(2024, 10, 30), 1.05),
    (dt.date(2024, 12, 31), dt.date(2025, 2, 20), 1.10),
    (dt.date(2024, 12, 31), dt.date(2025, 4, 15), 0.95),
    (dt.date(2025, 3, 31), dt.date(2025, 5, 1), 1.20),
]


def asof_value(query: dt.date) -> float | None:
    """Latest record whose publication date is on or before the query date (point-in-time)."""
    known = [r for r in RECORDS if r[1] <= query]
    if not known:
        return None
    return max(known, key=lambda r: (r[1], r[0]))[2]


def naive_value(query: dt.date) -> float | None:
    """Latest fiscal period ending on or before the query date, using the final vintage (look-ahead)."""
    final: dict[dt.date, float] = {}
    for period, _, eps in sorted(RECORDS, key=lambda r: r[1]):
        final[period] = eps
    periods = [p for p in final if p <= query]
    return final[max(periods)] if periods else None


def section_asof() -> None:
    print("== 1. As-of join ==")
    queries = [dt.date(2025, 1, 31), dt.date(2025, 3, 3), dt.date(2025, 4, 30), dt.date(2025, 5, 2)]
    expected_pit = [1.05, 1.10, 0.95, 1.20]
    expected_naive = [0.95, 0.95, 1.20, 1.20]
    for q, e_pit, e_naive in zip(queries, expected_pit, expected_naive, strict=True):
        pit, naive = asof_value(q), naive_value(q)
        assert pit is not None and naive is not None
        check(f"as-of {q} point-in-time EPS", pit, e_pit, 1e-12, ".2f")
        check(f"as-of {q} naive EPS", naive, e_naive, 1e-12, ".2f")


# ---------------------------------------------------------------------------
# 2. Time zones
# ---------------------------------------------------------------------------


def section_timezones() -> None:
    print("== 2. Time zones ==")
    ny = ZoneInfo("America/New_York")
    for day, expected_hour in [(dt.date(2025, 7, 15), 16), (dt.date(2025, 1, 15), 15)]:
        stamp = dt.datetime(day.year, day.month, day.day, 20, 30, tzinfo=dt.timezone.utc).astimezone(ny)
        check(f"20:30 UTC on {day} in New York (hour)", stamp.hour + stamp.minute / 60, expected_hour + 0.5, 1e-12, ".2f")
    # Filing deadlines (SEC Form 10-K General Instruction A(2), Form 10-Q General Instruction A.1, as of 2026-10).
    q_end = dt.date(2025, 3, 31)
    check("10-Q deadline for a large accelerated filer (days after 31 Mar)", (q_end + dt.timedelta(days=40) - q_end).days, 40, 0, "d")
    print(f"10-Q due date: {q_end + dt.timedelta(days=40)}")
    assert q_end + dt.timedelta(days=40) == dt.date(2025, 5, 10)
    fy_end = dt.date(2024, 12, 31)
    print(f"10-K due dates (60, 75, 90 days): {[str(fy_end + dt.timedelta(days=d)) for d in (60, 75, 90)]}")
    assert fy_end + dt.timedelta(days=60) == dt.date(2025, 3, 1)
    assert fy_end + dt.timedelta(days=90) == dt.date(2025, 3, 31)


# ---------------------------------------------------------------------------
# 3. Survivorship with delistings
# ---------------------------------------------------------------------------


def simulate_universe(seed: int = 7, n0: int = 1000, months: int = 240) -> dict[str, np.ndarray]:
    """Equal true expected returns; performance delistings at -30%, takeovers at +25%; replaced one for one."""
    rng = np.random.default_rng(seed)
    mu, sigma = 0.008, 0.10
    max_names = n0 * 3
    ret = np.full((months, max_names), np.nan)  # realised monthly simple return, NaN when not listed
    delist_month = np.full(max_names, -1)
    delist_kind = np.zeros(max_names, dtype=int)  # 0 alive, 1 performance, 2 takeover
    rel_price = np.ones(max_names)  # price relative to listing price
    alive = np.zeros(max_names, dtype=bool)
    alive[:n0] = True
    next_id = n0
    for t in range(months):
        ids = np.flatnonzero(alive)
        r = np.exp(rng.normal(mu - 0.5 * sigma**2, sigma, ids.size)) - 1.0
        distressed = rel_price[ids] < 0.4
        p_perf = np.where(distressed, 0.06, 0.001)
        u = rng.random(ids.size)
        perf = u < p_perf
        takeover = (~perf) & (u < p_perf + 0.0025)
        r = np.where(perf, -0.30, np.where(takeover, 0.25, r))
        ret[t, ids] = r
        rel_price[ids] *= 1.0 + r
        gone = ids[perf | takeover]
        delist_month[gone] = t
        delist_kind[gone] = np.where(perf[perf | takeover], 1, 2)
        alive[gone] = False
        new = np.arange(next_id, next_id + gone.size)
        alive[new] = True
        rel_price[new] = 1.0
        next_id += gone.size
    used = next_id
    return {
        "ret": ret[:, :used],
        "delist_month": delist_month[:used],
        "delist_kind": delist_kind[:used],
        "alive_end": alive[:used],
    }


def ew_series(ret: np.ndarray, mask: np.ndarray) -> np.ndarray:
    r = np.where(mask, ret, np.nan)
    return np.nanmean(r, axis=1)


def trailing_return(ret: np.ndarray, t: int, window: int) -> np.ndarray:
    block = ret[t - window : t]
    return np.prod(1.0 + block, axis=0) - 1.0  # NaN unless listed for the whole window


def loser_minus_winner(ret: np.ndarray, usable: np.ndarray, window: int = 12) -> np.ndarray:
    """Equal-weight bottom decile minus top decile of trailing 12-month return, held one month."""
    out = []
    for t in range(window, ret.shape[0]):
        past = trailing_return(ret, t, window)
        ok = np.isfinite(past) & usable[t] & np.isfinite(ret[t])
        idx = np.flatnonzero(ok)
        order = idx[np.argsort(past[idx])]
        k = order.size // 10
        out.append(ret[t, order[:k]].mean() - ret[t, order[-k:]].mean())
    return np.array(out)


def section_survivorship() -> None:
    print("== 3. Survivorship ==")
    u = simulate_universe()
    ret, dm, kind, alive_end = u["ret"], u["delist_month"], u["delist_kind"], u["alive_end"]
    months = ret.shape[0]
    listed = np.isfinite(ret)
    rows = np.arange(months)[:, None]
    is_delist_month = rows == dm[None, :]

    full = ew_series(ret, listed)
    no_delist_ret = ew_series(ret, listed & ~is_delist_month)
    no_perf_ret = ew_series(ret, listed & ~(is_delist_month & (kind == 1)[None, :]))
    survivors = ew_series(ret, listed & alive_end[None, :])

    n_perf = int((kind == 1).sum())
    n_take = int((kind == 2).sum())
    check("performance delistings over 20 years", n_perf, 575, 0, "d")
    check("takeovers over 20 years", n_take, 582, 0, "d")
    check("names alive at the end", int(alive_end.sum()), 1000, 0, "d")
    a_full = check("EW annual return, full PIT with delisting returns (%)", 1200 * full.mean(), 9.47, 0.01, ".2f")
    a_nodl = check("EW annual return, delisting returns dropped (%)", 1200 * no_delist_ret.mean(), 9.65, 0.01, ".2f")
    a_noperf = check("EW annual return, performance-delisting returns dropped (%)", 1200 * no_perf_ret.mean(), 10.36, 0.01, ".2f")
    check("bias from dropping performance-delisting returns (pp per year)", a_noperf - a_full, 0.89, 0.01, ".2f")
    a_surv = check("EW annual return, survivors only (%)", 1200 * survivors.mean(), 13.04, 0.01, ".2f")
    check("bias from dropping delisting returns (pp per year)", a_nodl - a_full, 0.18, 0.01, ".2f")
    check("survivorship bias (pp per year)", a_surv - a_full, 3.57, 0.01, ".2f")

    lmw_full = loser_minus_winner(ret, listed)
    lmw_surv = loser_minus_winner(ret, listed & alive_end[None, :])
    check("losers-minus-winners annual return, full PIT (%)", 1200 * lmw_full.mean(), -2.03, 0.01, ".2f")
    check("losers-minus-winners annual return, survivors only (%)", 1200 * lmw_surv.mean(), 7.22, 0.01, ".2f")
    sr_full = lmw_full.mean() / lmw_full.std(ddof=1) * np.sqrt(12)
    sr_surv = lmw_surv.mean() / lmw_surv.std(ddof=1) * np.sqrt(12)
    check("losers-minus-winners Sharpe, full PIT", sr_full, -0.37, 0.01, ".2f")
    check("losers-minus-winners Sharpe, survivors only", sr_surv, 1.06, 0.01, ".2f")


# ---------------------------------------------------------------------------
# 4. Index membership
# ---------------------------------------------------------------------------


def section_index_membership(seed: int = 11) -> None:
    print("== 4. Index membership ==")
    rng = np.random.default_rng(seed)
    n, years, top = 2000, 20, 500
    months = 12 * years
    log_cap0 = rng.normal(0.0, 1.5, n)
    r = np.exp(rng.normal(0.008 - 0.5 * 0.08**2, 0.08, (months, n))) - 1.0
    log_cap = log_cap0 + np.vstack([np.zeros(n), np.cumsum(np.log1p(r), axis=0)])  # cap at start of month t
    pit_member = np.zeros((months, n), dtype=bool)
    for y in range(years):
        caps = log_cap[12 * y]
        members = np.argsort(caps)[-top:]
        pit_member[12 * y : 12 * (y + 1), members] = True
    today = np.argsort(log_cap[-1])[-top:]
    today_mask = np.zeros(n, dtype=bool)
    today_mask[today] = True
    pit = np.array([r[t, pit_member[t]].mean() for t in range(months)])
    hindsight = r[:, today_mask].mean(axis=1)
    a_pit = check("EW return of point-in-time top-500 members (% per year)", 1200 * pit.mean(), 10.02, 0.01, ".2f")
    a_hind = check("EW return of today's top-500 backtested 20 years (% per year)", 1200 * hindsight.mean(), 15.24, 0.01, ".2f")
    check("index-membership look-ahead bias (pp per year)", a_hind - a_pit, 5.23, 0.01, ".2f")
    first_year_overlap = np.mean(today_mask[pit_member[0]])
    check("fraction of year-1 members still in today's top 500", first_year_overlap, 0.632, 0.001, ".3f")


# ---------------------------------------------------------------------------
# 5. Timing and restatements
# ---------------------------------------------------------------------------


def corr_cs(x: np.ndarray, y: np.ndarray) -> float:
    """Average cross-sectional correlation over rows."""
    xs = (x - x.mean(1, keepdims=True)) / x.std(1, keepdims=True)
    ys = (y - y.mean(1, keepdims=True)) / y.std(1, keepdims=True)
    return float((xs * ys).mean())


def section_timing(seed: int = 3) -> None:
    print("== 5. Timing and restatements ==")
    rng = np.random.default_rng(seed)
    n, quarters = 500, 80
    first_release = rng.standard_normal((quarters, n))
    # The restated (final) value adds information that only arrives later: e = f + 0.7 v.
    restated = first_release + 0.7 * rng.standard_normal((quarters, n))
    # Filing month: the market prices the first release.
    r_filing = 0.02 * first_release + 0.08 * rng.standard_normal((quarters, n))
    # Next month: a third of the later revision is learned, plus a small post-announcement drift.
    r_next = 0.02 * (restated - first_release) / 3 + 0.002 * first_release + 0.08 * rng.standard_normal((quarters, n))

    check("IC stamped at period end (look-ahead into filing month)", corr_cs(first_release, r_filing), 0.241, 0.002, ".3f")
    check("IC point-in-time, first release, next month", corr_cs(first_release, r_next), 0.026, 0.002, ".3f")
    check("IC with restated values at filing date, next month", corr_cs(restated, r_next), 0.058, 0.002, ".3f")
    # Analytic values for the same model.
    sd_next = np.sqrt((0.02 * 0.7 / 3) ** 2 + 0.002**2 + 0.08**2)
    sd_e = np.sqrt(1 + 0.7**2)
    check("sd of next-month return", sd_next, 0.0802, 0.0001)
    check("sd of restated value", sd_e, 1.2207, 0.0001)
    check("cov(restated, next-month return)", 0.02 * 0.7**2 / 3 + 0.002, 0.00527, 0.00001, ".5f")
    check("analytic IC at period end", 0.02 / np.sqrt(0.02**2 + 0.08**2), 0.243, 0.001, ".3f")
    check("analytic IC point-in-time", 0.002 / sd_next, 0.025, 0.001, ".3f")
    check("analytic IC restated", (0.02 * 0.7**2 / 3 + 0.002) / (sd_e * sd_next), 0.054, 0.001, ".3f")


# ---------------------------------------------------------------------------
# 6. Corporate actions and back-adjusted prices
# ---------------------------------------------------------------------------


def section_corporate_actions() -> None:
    print("== 6. Corporate actions ==")
    # A 2-for-1 split: close 100 before, 51 after.
    raw = 51 / 100 - 1
    adjusted = 51 * 2 / 100 - 1
    check("raw close-to-close return across a 2-for-1 split (%)", 100 * raw, -49.0, 1e-9, ".1f")
    check("split-adjusted return (%)", 100 * adjusted, 2.0, 1e-9, ".1f")
    # A distressed stock trading at 0.80 later does a 1-for-10 reverse split.
    back_adjusted = 0.80 * 10
    check("back-adjusted historical price after a 1-for-10 reverse split", back_adjusted, 8.0, 1e-9, ".2f")
    assert back_adjusted > 5.0 > 0.80  # a "price above 5" filter on adjusted prices admits a penny stock


def main() -> None:
    section_asof()
    section_timezones()
    section_survivorship()
    section_index_membership()
    section_timing()
    section_corporate_actions()


if __name__ == "__main__":
    main()
