"""Tick storage: as-of joins, point-in-time joins, capacity estimates and columnar compression.

Backs the numbers in 12-Quant-Development/12-Tick-Data-Storage-and-Time-Series-Databases.md.

* `asof_join` is a per-symbol np.searchsorted as-of join (the semantics of kdb+ `aj` and
  pandas `merge_asof(direction="backward")`), checked against a brute-force reference.
* The forward join is the classic look-ahead bug; it is shown biasing an effective-spread study.
* A point-in-time join on knowledge timestamps versus a naive join on the period a value describes.
* Capacity arithmetic from stated assumptions, and row-group pruning with min/max statistics.
* zlib compression of row versus columnar versus delta-encoded layouts of seeded synthetic ticks.
  Compressed sizes depend on the zlib version: the quoted ratios are asserted exactly under the zlib
  version they were produced with (1.2.12) and only against ordering bounds otherwise.

Run: uv run --no-project --with numpy python 12-Quant-Development/code/python/tick_storage_asof.py
"""

from __future__ import annotations

import zlib

import numpy as np
from pcg_stream import PcgStream

NO_MATCH = -1


def asof_join(
    q_sym: np.ndarray,
    q_time: np.ndarray,
    t_sym: np.ndarray,
    t_time: np.ndarray,
    direction: str = "backward",
    tolerance: int | None = None,
) -> np.ndarray:
    """For each trade, the index of the matching quote of the same symbol, or NO_MATCH.

    backward: last quote with time <= trade time (prevailing quote; no look-ahead).
    forward:  first quote with time >= trade time (uses the future; a bug in most studies).
    tolerance: if set, a match older (or newer) than this many time units is rejected as stale.
    Quotes must be sorted by (symbol, time); trades may be in any order.
    """
    if direction not in ("backward", "forward"):
        raise ValueError(direction)
    order = np.lexsort((q_time, q_sym))
    if not np.array_equal(order, np.arange(len(q_sym))):
        raise ValueError("quotes must be sorted by (symbol, time)")
    out = np.full(len(t_sym), NO_MATCH, dtype=np.int64)
    for s in np.unique(t_sym):
        lo, hi = np.searchsorted(q_sym, s, "left"), np.searchsorted(q_sym, s, "right")
        qt = q_time[lo:hi]
        ti = np.flatnonzero(t_sym == s)
        if direction == "backward":
            k = np.searchsorted(qt, t_time[ti], side="right") - 1
            ok = k >= 0
        else:
            k = np.searchsorted(qt, t_time[ti], side="left")
            ok = k < len(qt)
        kk = np.where(ok, k, 0)
        if tolerance is not None and len(qt):
            ok &= np.abs(t_time[ti] - qt[kk]) <= tolerance
        out[ti] = np.where(ok, lo + kk, NO_MATCH)
    return out


def asof_brute(q_sym, q_time, t_sym, t_time, direction="backward") -> np.ndarray:
    out = np.full(len(t_sym), NO_MATCH, dtype=np.int64)
    for i in range(len(t_sym)):
        best = NO_MATCH
        for j in range(len(q_sym)):
            if q_sym[j] != t_sym[i]:
                continue
            if direction == "backward" and q_time[j] <= t_time[i] and (best == NO_MATCH or q_time[j] >= q_time[best]):
                best = j
            if direction == "forward" and q_time[j] >= t_time[i] and (best == NO_MATCH or q_time[j] < q_time[best]):
                best = j
        out[i] = best
    return out


def hand_example() -> None:
    print("== Hand example")
    q_sym = np.array([0, 0, 0, 1, 1])  # 0 = AAA, 1 = BBB
    q_time = np.array([100, 200, 300, 150, 250])
    t_sym = np.array([0, 0, 0, 0, 1])
    t_time = np.array([50, 200, 250, 400, 260])
    print("quotes AAA at", q_time[:3].tolist(), "BBB at", q_time[3:].tolist(), "; trades AAA at", t_time[:4].tolist(), "BBB at", [260])
    back = asof_join(q_sym, q_time, t_sym, t_time)
    fwd = asof_join(q_sym, q_time, t_sym, t_time, "forward")
    tol = asof_join(q_sym, q_time, t_sym, t_time, tolerance=60)
    print("backward quote times:", [int(q_time[k]) if k >= 0 else None for k in back])
    print("forward quote times: ", [int(q_time[k]) if k >= 0 else None for k in fwd])
    print("backward, tolerance 60:", [int(q_time[k]) if k >= 0 else None for k in tol])
    assert back.tolist() == [-1, 1, 1, 2, 4]
    assert fwd.tolist() == [0, 1, 2, -1, -1]
    assert tol.tolist() == [-1, 1, 1, -1, 4]
    # The quote times in note 12 example 1's table.
    assert [int(q_time[k]) if k >= 0 else None for k in back] == [None, 200, 200, 300, 250]
    assert [int(q_time[k]) if k >= 0 else None for k in fwd] == [100, 200, 300, None, None]
    assert [int(q_time[k]) if k >= 0 else None for k in tol] == [None, 200, 200, None, 250]


def random_check() -> None:
    print("== Random check against brute force")
    rng = PcgStream(5)
    nq, nt = 3000, 600
    q_sym = rng.integers(0, 4, nq)
    q_time = rng.integers(0, 100_000, nq)
    o = np.lexsort((q_time, q_sym))
    q_sym, q_time = q_sym[o], q_time[o]
    t_sym = rng.integers(0, 5, nt)  # symbol 4 has no quotes at all
    t_time = rng.integers(0, 100_000, nt)
    tie_next = (np.diff(q_sym) == 0) & (np.diff(q_time) == 0)
    tied = int(tie_next.sum())
    print(f"quotes sharing a symbol and time with the previous quote: {tied}")
    assert tied == 13  # note 12 example 1
    # One extra trade stamped at each tied quote time, so both joins must resolve real ties.
    t_sym = np.concatenate([t_sym, q_sym[1:][tie_next]])
    t_time = np.concatenate([t_time, q_time[1:][tie_next]])
    nt = len(t_sym)
    in_tie = np.zeros(nq, dtype=bool)
    in_tie[1:] |= tie_next
    in_tie[:-1] |= tie_next
    for d in ("backward", "forward"):
        fast = asof_join(q_sym, q_time, t_sym, t_time, d)
        slow = asof_brute(q_sym, q_time, t_sym, t_time, d)
        same = fast == slow  # indices, so a join that picks the wrong one of two tied quotes fails
        hits = int(in_tie[fast[fast >= 0]].sum())
        unmatched = int((fast < 0).sum())
        print(f"{d}: {nq:,} quotes, {nt} trades: {int(same.sum())}/{nt} agree, unmatched {unmatched}, matched to a tied quote {hits}")
        assert same.all()
        assert hits >= tied  # every added trade lands on a tie, so the tie rule is exercised in both directions
        assert hits == {"backward": 13, "forward": 14}[d]  # note 12 example 1


def tied_quotes() -> None:
    print("== Tied quote times")
    # Two AAA quotes stamped 200 arrive in feed order: index 1, then index 2.
    q_sym = np.array([0, 0, 0, 0])
    q_time = np.array([100, 200, 200, 300])
    t_sym = np.array([0, 0, 0])
    t_time = np.array([150, 200, 250])
    back = asof_join(q_sym, q_time, t_sym, t_time)
    fwd = asof_join(q_sym, q_time, t_sym, t_time, "forward")
    print("quotes at", q_time.tolist(), "; trades at", t_time.tolist())
    print("backward indices:", back.tolist(), " forward indices:", fwd.tolist())
    # Note 12 card qd-tick-asof-exact-time: a backward join uses a quote stamped at the trade's own time, and
    # among tied quotes the last one in feed order (kdb+ aj, pandas merge_asof); a forward join takes the first.
    assert back.tolist() == [0, 2, 2] and fwd.tolist() == [1, 1, 3]
    assert asof_brute(q_sym, q_time, t_sym, t_time).tolist() == [0, 2, 2]
    assert asof_brute(q_sym, q_time, t_sym, t_time, "forward").tolist() == [1, 1, 3]


def effective_spread_bias(seed: int = 6) -> tuple[float, float]:
    """Trades hit the prevailing quote; the next quote reflects impact. Measure the effective half-spread."""
    rng = PcgStream(seed)
    n = 50_000
    half, impact = 0.05, 0.02
    t = np.cumsum(rng.integers(1, 1000, n)) * 2  # even times for quotes
    mid = np.empty(n)
    sign = rng.choice([-1.0, 1.0], n)
    m = 100.0
    for i in range(n):
        mid[i] = m
        m += impact * sign[i] + rng.normal(0.0, 0.01)  # post-trade quote moves toward the trade
    q_sym = np.zeros(n, dtype=np.int64)
    q_time = t
    trade_time = t + 1  # each trade lands 1 unit after a quote, before the next quote
    price = mid + sign * half  # buys lift the ask, sells hit the bid
    t_sym = np.zeros(n, dtype=np.int64)
    back = asof_join(q_sym, q_time, t_sym, trade_time)
    fwd = asof_join(q_sym, q_time, t_sym, trade_time, "forward")
    ok = (back >= 0) & (fwd >= 0)
    eff_back = float(np.mean(sign[ok] * (price[ok] - mid[back[ok]])))
    eff_fwd = float(np.mean(sign[ok] * (price[ok] - mid[fwd[ok]])))
    return eff_back, eff_fwd


def point_in_time() -> None:
    print("== Point-in-time join of a restated field")
    print("quarter ends day 90; published day 120 as 1.00; restated day 200 as 0.80")
    # One symbol; fiscal quarter ending day 90, first published day 120 (EPS 1.00), restated day 200 (EPS 0.80).
    know = np.array([120, 200])
    eps = np.array([1.00, 0.80])
    asof_days = np.array([100, 150, 250])
    k = np.searchsorted(know, asof_days, side="right") - 1
    pit = [float(eps[i]) if i >= 0 else None for i in k]
    naive = [float(eps[-1])] * len(asof_days)  # latest version keyed on the period, ignoring knowledge time
    print("as of days", asof_days.tolist(), "PIT EPS", pit, "naive EPS", naive)
    assert pit == [None, 1.0, 0.8] and naive == [0.8, 0.8, 0.8]


SCHEMA = {
    "ts_ns int64": 8,
    "symbol_id int32": 4,
    "order_id int64": 8,
    "price int64": 8,
    "size int32": 4,
    "side int8": 1,
    "msg_type int8": 1,
    "venue int16": 2,
}


def capacity(ratio: float = 5.0) -> None:
    print("== Capacity estimate (assumptions, not facts)")
    events_per_day = 500e6  # assumption: normalized depth-of-book events per day for a broad equity universe
    row = sum(SCHEMA.values())
    days, years = 252, 10
    session_s = 6.5 * 3600
    peak_mult = 20  # assumption: busiest second is 20 times the session average
    print(f"inputs: {events_per_day:,.0f} events/day, {days} days/year, {years} years,", end=" ")
    print(f"session {session_s / 3600} h = {session_s:,.0f} s, peak multiple {peak_mult}")
    raw_day = events_per_day * row
    raw_year = raw_day * days
    raw_total = raw_year * years
    avg_rate = events_per_day / session_s
    peak_rate = avg_rate * peak_mult
    print(f"row {row} B; raw/day {raw_day / 1e9:.1f} GB; raw/year {raw_year / 1e12:.2f} TB; raw 10y {raw_total / 1e12:.1f} TB")
    print(f"compressed 10y at an assumed ratio {ratio:.1f}: {raw_total / ratio / 1e12:.2f} TB")
    print(f"average {avg_rate:,.0f} events/s; peak {peak_rate:,.0f} events/s = {peak_rate * row / 1e6:.1f} MB/s")
    # Note 12 example 6 table and card qd-tick-capacity-estimate, at the quoted rounding.
    assert row == 36 and ratio == 5.0
    assert f"{raw_day / 1e9:.1f}" == "18.0" and f"{raw_year / 1e12:.2f}" == "4.54" and f"{raw_total / 1e12:.1f}" == "45.4"
    assert f"{raw_total / ratio / 1e12:.2f}" == "9.07"
    assert f"{avg_rate:,.0f}" == "21,368" and f"{peak_rate:,.0f}" == "427,350"
    assert f"{peak_rate * row / 1e6:.1f}" == "15.4"


def pruning() -> None:
    print("== Row-group pruning with min/max statistics")
    rng = PcgStream(8)
    n, nsym, group = 2_000_000, 500, 100_000
    sym = rng.integers(0, nsym, n)
    target = 123
    n_groups = n // group
    unsorted = sym.reshape(n_groups, group)
    hit_unsorted = int(np.sum((unsorted.min(1) <= target) & (unsorted.max(1) >= target)))
    srt = np.sort(sym).reshape(n_groups, group)
    hit_sorted = int(np.sum((srt.min(1) <= target) & (srt.max(1) >= target)))
    rows = int(np.sum(sym == target))
    print(f"{n:,} rows, {nsym} symbols, row groups of {group:,}: {n_groups} row groups; symbol {target} has {rows:,} rows")
    print(f"groups read: unsorted {hit_unsorted}, sorted by symbol {hit_sorted}")
    assert hit_unsorted == n_groups == 20 and hit_sorted == 1 and rows == 3924


def synthetic_ticks(seed: int, n: int) -> dict[str, np.ndarray]:
    rng = PcgStream(seed)
    gaps = np.maximum(1, rng.exponential(5e6, n)).astype(np.int64)  # mean 5 ms in nanoseconds
    ts = 34_200_000_000_000 + np.cumsum(gaps)  # from 09:30:00 in nanoseconds since midnight
    steps = rng.choice([-1, 0, 0, 0, 1], n)
    price = 1_500_000 + 100 * np.cumsum(steps)  # Price(4) units: $150.0000 moving in one-cent (100-unit) steps
    size = rng.choice([100, 100, 100, 200, 300, 500, 1000, 37], n).astype(np.int32)
    side = rng.choice(np.array([ord("B"), ord("S")], dtype=np.uint8), n)
    return {"ts": ts, "price": price.astype(np.int64), "size": size, "side": side}


def compression(seed: int = 9, n: int = 200_000) -> float:
    print("== Compression: row vs columnar vs delta (zlib level 6; zlib-version dependent)")
    c = synthetic_ticks(seed, n)
    rec = np.empty(n, dtype=[("ts", "<i8"), ("price", "<i8"), ("size", "<i4"), ("side", "u1")])
    for k in rec.dtype.names:
        rec[k] = c[k]
    raw = rec.tobytes()
    row_z = len(zlib.compress(raw, 6))
    col_z = sum(len(zlib.compress(c[k].tobytes(), 6)) for k in ("ts", "price", "size", "side"))
    dts = np.diff(c["ts"], prepend=c["ts"][0])
    assert dts.max() < 2**31
    dpx = np.diff(c["price"], prepend=c["price"][0]) // 100  # deltas in cents fit in int8
    assert np.abs(dpx[1:]).max() <= 1
    delta_cols = {
        "ts": dts.astype(np.int32).tobytes(),
        "price": dpx[1:].astype(np.int8).tobytes(),
        "size": c["size"].tobytes(),
        "side": c["side"].tobytes(),
    }
    del_z = sum(len(zlib.compress(b, 6)) for b in delta_cols.values()) + 16  # + base values
    r_row, r_col, r_del = len(raw) / row_z, len(raw) / col_z, len(raw) / del_z
    print(f"raw {len(raw):,} B ({rec.itemsize} B/row); row {row_z:,} B ({r_row:.2f}x)")
    print(f"columnar {col_z:,} B ({r_col:.2f}x); delta {del_z:,} B ({r_del:.2f}x)")
    print(f"zlib version {zlib.ZLIB_RUNTIME_VERSION}")
    assert rec.itemsize == 21 and len(raw) == 21 * n
    assert 1.2 < r_row < r_col < r_del
    assert r_del > 3.0
    if zlib.ZLIB_RUNTIME_VERSION == "1.2.12":  # the version the note's quoted ratios were produced with
        assert (round(r_row, 2), round(r_col, 2), round(r_del, 2)) == (3.27, 4.02, 4.88)
    return r_del


def main() -> None:
    hand_example()
    tied_quotes()
    random_check()
    eb, ef = effective_spread_bias()
    print(f"== Effective half-spread: backward join {eb:.4f}, forward join {ef:.4f} (true 0.05, impact 0.02)")
    # Note 12 example 2 and card qd-tick-forward-join-bias quote about 0.050, about 0.030 and 40%.
    assert f"{eb:.3f}" == "0.050" and f"{ef:.3f}" == "0.030"
    print(f"   inputs 50,000 trades, seed 6; understatement {100 * (eb - ef) / eb:.0f}%")
    assert f"{100 * (eb - ef) / eb:.0f}" == "40"
    point_in_time()
    pruning()
    r = compression()
    assert 4.0 < r < 6.0  # so the 5x planning assumption below is in line with the measurement
    capacity()
    print("all assertions passed")


if __name__ == "__main__":
    main()
