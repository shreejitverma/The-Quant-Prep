"""Numbers behind 12-Quant-Development/15-Quant-Dev-Problem-Set.md.

Every value the problem set quotes is computed here, printed with a label and asserted,
so a change in an assumption or a formula fails loudly instead of drifting silently.

Run: uv run --no-project --with numpy python 12-Quant-Development/code/python/quant_dev_problem_set.py
(standard library plus numpy; Python 3.10+).
"""

from __future__ import annotations

import bisect
import math
import struct
from dataclasses import dataclass

import numpy as np


def close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def show(label: str, value: object) -> None:
    print(f"{label}: {value}")


# ---------------------------------------------------------------------------
# 08 Feed handlers
# ---------------------------------------------------------------------------

ITCH_ADD_ORDER_BYTES = 36  # 'A' message length in TotalView-ITCH 5.0
MOLD_HEADER_BYTES = 20  # session 10 + sequence 8 + count 2
MOLD_LENGTH_PREFIX = 2
IPV4_HEADER = 20
UDP_HEADER = 8
ETH_HEADER = 14
ETH_FCS = 4
ETH_PREAMBLE_SFD = 8
ETH_IFG = 12
MTU = 1500


def feed_bandwidth(msgs_per_sec: float) -> dict[str, float]:
    block = ITCH_ADD_ORDER_BYTES + MOLD_LENGTH_PREFIX
    udp_payload_max = MTU - IPV4_HEADER - UDP_HEADER
    per_packet = (udp_payload_max - MOLD_HEADER_BYTES) // block
    ip_bytes = IPV4_HEADER + UDP_HEADER + MOLD_HEADER_BYTES + per_packet * block
    wire_extra = ETH_HEADER + ETH_FCS + ETH_PREAMBLE_SFD + ETH_IFG
    wire_bytes = ip_bytes + wire_extra
    pps = msgs_per_sec / per_packet
    gbps_batched = pps * wire_bytes * 8 / 1e9
    single_ip = IPV4_HEADER + UDP_HEADER + MOLD_HEADER_BYTES + block
    single_wire = single_ip + wire_extra
    gbps_single = msgs_per_sec * single_wire * 8 / 1e9
    return {
        "udp_payload_max": udp_payload_max,
        "blocks_room": udp_payload_max - MOLD_HEADER_BYTES,
        "block": block,
        "per_packet": per_packet,
        "ip_bytes": ip_bytes,
        "wire_bytes": wire_bytes,
        "pps": pps,
        "gbps_batched": gbps_batched,
        "single_wire": single_wire,
        "gbps_single": gbps_single,
    }


@dataclass
class GapTracker:
    """MoldUDP64-style sequencing: apply in order, buffer ahead, drop duplicates."""

    expected: int
    pending: dict[int, str]
    applied: list[int]
    requests: list[tuple[int, int]]
    duplicates: int = 0

    def on_packet(self, seq: int, count: int) -> None:
        for s in range(seq, seq + count):
            if s < self.expected or s in self.pending:
                self.duplicates += 1
            else:
                self.pending[s] = "msg"
        if self.pending and min(self.pending) > self.expected:
            gap_end = min(self.pending)
            self.requests.append((self.expected, gap_end - self.expected))
        while self.expected in self.pending:
            del self.pending[self.expected]
            self.applied.append(self.expected)
            self.expected += 1


def gap_example() -> GapTracker:
    t = GapTracker(expected=1001, pending={}, applied=[], requests=[])
    t.on_packet(1001, 3)
    t.on_packet(1007, 2)
    t.on_packet(1004, 3)  # retransmission
    t.on_packet(1005, 2)  # late duplicate from the other line
    return t


def ab_double_loss(packets_per_day: float, p_loss: float) -> tuple[float, float, float]:
    single = packets_per_day * p_loss
    both = packets_per_day * p_loss * p_loss
    days_between = 1.0 / both
    return single, both, days_between


def itch_field_ranges() -> dict[str, float]:
    max_price_raw = 2_000_000_000  # 200,000.0000 with 4 implied decimals
    ns_per_day = 86_400 * 10**9
    max_ts = 2**48 - 1
    return {
        "max_price_raw": max_price_raw,
        "max_price_hex": int("77359400", 16),
        "uint32_max": 2**32 - 1,
        "int32_max": 2**31 - 1,
        "ns_per_day": ns_per_day,
        "ts48_max": max_ts,
        "ts48_hours": max_ts / 1e9 / 3600,
        "ts32_seconds": (2**32 - 1) / 1e9,
    }


def build_book() -> tuple[dict[int, int], dict[int, int]]:
    """Replay an ITCH-style message list into price levels (price in 1e-4 units)."""
    orders: dict[int, tuple[str, int, int]] = {}
    msgs = [
        ("A", 1, "B", 100, 100_000),
        ("A", 2, "B", 200, 100_100),
        ("A", 3, "S", 300, 100_300),
        ("A", 4, "S", 150, 100_200),
        ("E", 2, 50),
        ("X", 3, 100),
        ("U", 1, 5, 120, 100_150),
        ("D", 4),
    ]
    for m in msgs:
        kind = m[0]
        if kind == "A":
            _, ref, side, qty, px = m
            orders[ref] = (side, qty, px)
        elif kind in ("E", "X"):
            _, ref, q = m
            side, qty, px = orders[ref]
            left = qty - q
            assert left >= 0
            if left == 0:
                del orders[ref]
            else:
                orders[ref] = (side, left, px)
        elif kind == "U":
            _, old, new, qty, px = m
            side, _, _ = orders.pop(old)
            orders[new] = (side, qty, px)
        elif kind == "D":
            del orders[m[1]]
    bids: dict[int, int] = {}
    asks: dict[int, int] = {}
    for side, qty, px in orders.values():
        book = bids if side == "B" else asks
        book[px] = book.get(px, 0) + qty
    return bids, asks


def snapshot_merge(buffer_first: int, buffer_last: int, snapshot_seq: int) -> tuple[int, int]:
    discard = snapshot_seq - buffer_first + 1
    apply = buffer_last - snapshot_seq
    return discard, apply


def seq_wrap(rate: float) -> tuple[float, float]:
    years64 = 2**64 / rate / (365.25 * 86_400)
    minutes32 = 2**32 / 1e6 / 60
    return years64, minutes32


# ---------------------------------------------------------------------------
# 09 Backtester and simulator
# ---------------------------------------------------------------------------


def queue_fill(ahead: int, my_qty: int, events: list[tuple[str, int]], cancels_from_ahead: bool) -> tuple[int, int | None]:
    """FIFO queue: trades eat from the front; cancels shrink 'ahead' only if assumed ahead of us.

    Returns (filled quantity, index of the event that completed the fill or None).
    """
    filled = 0
    done_at = None
    for i, (kind, q) in enumerate(events):
        if kind == "trade":
            eat_ahead = min(ahead, q)
            ahead -= eat_ahead
            rest = q - eat_ahead
            take = min(rest, my_qty - filled)
            filled += take
            if filled == my_qty and done_at is None:
                done_at = i
        elif kind == "cancel_ahead" and cancels_from_ahead:
            ahead = max(0, ahead - q)
    return filled, done_at


def sqrt_impact(sigma_daily: float, q: float, v: float, y: float = 1.0) -> float:
    return y * sigma_daily * math.sqrt(q / v)


# ---------------------------------------------------------------------------
# 10 Pricing library
# ---------------------------------------------------------------------------


def ncdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def npdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs(s: float, k: float, r: float, vol: float, t: float) -> dict[str, float]:
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
    d2 = d1 - vol * math.sqrt(t)
    df = math.exp(-r * t)
    call = s * ncdf(d1) - k * df * ncdf(d2)
    put = k * df * ncdf(-d2) - s * ncdf(-d1)
    return {
        "call": call,
        "put": put,
        "delta": ncdf(d1),
        "gamma": npdf(d1) / (s * vol * math.sqrt(t)),
        "vega": s * npdf(d1) * math.sqrt(t),
    }


def fd_delta_errors() -> dict[str, float]:
    s, k, r, vol, t = 100.0, 100.0, 0.05, 0.2, 1.0
    exact = bs(s, k, r, vol, t)["delta"]
    eps = np.finfo(float).eps

    def c(x: float) -> float:
        return bs(x, k, r, vol, t)["call"]

    h_fwd = math.sqrt(eps) * s
    h_ctr = eps ** (1.0 / 3.0) * s
    fwd_opt = (c(s + h_fwd) - c(s)) / h_fwd
    ctr_opt = (c(s + h_ctr) - c(s - h_ctr)) / (2 * h_ctr)
    fwd_big = (c(s + 1.0) - c(s)) / 1.0
    ctr_big = (c(s + 1.0) - c(s - 1.0)) / 2.0
    tiny = 1e-12
    ctr_tiny = (c(s + tiny) - c(s - tiny)) / (2 * tiny)
    return {
        "exact": exact,
        "h_fwd": h_fwd,
        "h_ctr": h_ctr,
        "err_fwd_opt": abs(fwd_opt - exact),
        "err_ctr_opt": abs(ctr_opt - exact),
        "err_fwd_h1": abs(fwd_big - exact),
        "err_ctr_h1": abs(ctr_big - exact),
        "err_ctr_tiny": abs(ctr_tiny - exact),
    }


# ---------------------------------------------------------------------------
# 11 Numerical Python
# ---------------------------------------------------------------------------


def numpy_facts() -> dict[str, object]:
    a = np.zeros((10_000, 5_000))
    col = a[:, 0]
    out = {
        "bytes": a.nbytes,
        "mib": a.nbytes / 2**20,
        "strides": a.strides,
        "strides_T": a.T.strides,
        "col_is_view": np.shares_memory(a, col),
        "col_stride": col.strides,
        "broadcast": np.broadcast_shapes((3, 1, 5), (4, 1)),
        "float32_2_24_plus_1": float(np.float32(2**24) + np.float32(1)),
        "ulp_f32_2_24": float(np.spacing(np.float32(2**24))),
        "ulp_f64_100": float(np.spacing(100.0)),
        "sum_01_02_minus_03": 0.1 + 0.2 - 0.3,
    }
    try:
        np.broadcast_shapes((3, 2), (3,))
        out["broadcast_32_3"] = "ok"
    except ValueError:
        out["broadcast_32_3"] = "error"
    return out


def naive_vs_welford() -> tuple[float, float, float]:
    x = 1e9 + np.array([4.0, 7.0, 13.0, 16.0])
    n = len(x)
    naive = (np.sum(x * x) - np.sum(x) ** 2 / n) / (n - 1)
    mean = 0.0
    m2 = 0.0
    for i, v in enumerate(x, 1):
        d = v - mean
        mean += d / i
        m2 += d * (v - mean)
    welford = m2 / (n - 1)
    two_pass = float(np.var(x, ddof=1))
    return float(naive), welford, two_pass


def int32_notional() -> tuple[int, int]:
    px = np.array([1_000_000], dtype=np.int32)  # 100.0000 in ITCH Price(4) units
    qty = np.array([5_000], dtype=np.int32)
    wrapped = int((px * qty)[0])
    exact = 1_000_000 * 5_000
    return wrapped, exact


# ---------------------------------------------------------------------------
# 12 Tick storage
# ---------------------------------------------------------------------------


def capacity(msgs_per_day: float, bytes_per_msg: float, days: int, ratio: float, years: int, replicas: int) -> dict[str, float]:
    raw_day = msgs_per_day * bytes_per_msg
    raw_year = raw_day * days
    comp_year = raw_year / ratio
    total = comp_year * years * replicas
    return {"raw_day_gb": raw_day / 1e9, "raw_year_tb": raw_year / 1e12, "comp_year_tb": comp_year / 1e12, "total_tb": total / 1e12}


def asof_join(trade_t: list[int], quote_t: list[int], tolerance: int | None, forward: bool = False) -> list[int | None]:
    out: list[int | None] = []
    for t in trade_t:
        if forward:
            j = bisect.bisect_left(quote_t, t)
            out.append(j if j < len(quote_t) else None)
            continue
        j = bisect.bisect_right(quote_t, t) - 1
        if j < 0 or (tolerance is not None and t - quote_t[j] > tolerance):
            out.append(None)
        else:
            out.append(j)
    return out


# ---------------------------------------------------------------------------
# 13 Risk checks and OMS
# ---------------------------------------------------------------------------


def worst_case_long(position: int, open_buys: int, new_buy: int) -> int:
    return position + open_buys + new_buy


def token_bucket(capacity_tokens: float, rate: float, arrivals: list[tuple[float, int]]) -> list[int]:
    tokens = capacity_tokens
    last = 0.0
    accepted = []
    for t, n in arrivals:
        tokens = min(capacity_tokens, tokens + (t - last) * rate)
        last = t
        ok = 0
        for _ in range(n):
            if tokens >= 1.0:
                tokens -= 1.0
                ok += 1
        accepted.append(ok)
    return accepted


def exec_reports(order_qty: int, fills: list[tuple[int, float]]) -> list[tuple[int, int, float]]:
    cum = 0
    notional = 0.0
    rows = []
    for q, px in fills:
        cum += q
        notional += q * px
        rows.append((cum, order_qty - cum, notional / cum))
    return rows


# ---------------------------------------------------------------------------
# 14 Testing
# ---------------------------------------------------------------------------


def ulp_distance(a: float, b: float) -> int:
    ia = struct.unpack("<q", struct.pack("<d", a))[0]
    ib = struct.unpack("<q", struct.pack("<d", b))[0]
    return abs(ia - ib)


def two_sided_tail(z: float) -> float:
    return math.erfc(z / math.sqrt(2.0))


def main() -> None:
    print("== 08 feed handlers ==")
    bw = feed_bandwidth(2_000_000)
    show("UDP payload max, room for blocks", (bw["udp_payload_max"], bw["blocks_room"]))
    assert (bw["udp_payload_max"], bw["blocks_room"]) == (1472, 1452)
    show("message block bytes", bw["block"])
    show("messages per 1500-byte MTU packet", bw["per_packet"])
    show("IP packet bytes", bw["ip_bytes"])
    show("wire bytes per frame", bw["wire_bytes"])
    show("packets per second", f"{bw['pps']:.1f}")
    show("Gbit/s batched", f"{bw['gbps_batched']:.3f}")
    show("wire bytes single-message frame", bw["single_wire"])
    show("Gbit/s one message per packet", f"{bw['gbps_single']:.3f}")
    assert bw["block"] == 38 and bw["per_packet"] == 38 and bw["ip_bytes"] == 1492 and bw["wire_bytes"] == 1530
    assert close(bw["pps"], 52_631.6, 0.1)
    assert close(bw["gbps_batched"], 0.644, 0.001)
    assert bw["single_wire"] == 124 and close(bw["gbps_single"], 1.984, 1e-9)

    g = gap_example()
    show("gap requests (seq, count)", g.requests)
    show("applied", f"{g.applied[0]}..{g.applied[-1]} ({len(g.applied)} messages)")
    show("next expected", g.expected)
    show("duplicates dropped", g.duplicates)
    assert g.requests == [(1004, 3)]
    assert g.applied == list(range(1001, 1009)) and g.expected == 1009 and g.duplicates == 2

    single, both, days = ab_double_loss(20e6, 1e-5)
    show("expected single-line losses per day", f"{single:.0f}")
    show("expected double losses per day", f"{both:.4f}")
    show("days between double losses", f"{days:.0f}")
    assert close(single, 200, 1e-9) and close(both, 0.002, 1e-12) and close(days, 500, 1e-6)

    fr = itch_field_ranges()
    show("max Price(4) raw", fr["max_price_raw"])
    show("int32 max", f"{fr['int32_max']:,}")
    show("ns per day", fr["ns_per_day"])
    show("48-bit timestamp max hours", f"{fr['ts48_hours']:.1f}")
    show("32-bit ns counter wraps after seconds", f"{fr['ts32_seconds']:.3f}")
    assert fr["max_price_raw"] == fr["max_price_hex"] < fr["int32_max"] < fr["uint32_max"]
    assert fr["ns_per_day"] == 8.64e13 < fr["ts48_max"] and close(fr["ts48_hours"], 78.2, 0.05)
    assert close(fr["ts32_seconds"], 4.295, 0.001)

    bids, asks = build_book()
    show("bids (px*1e4: qty)", dict(sorted(bids.items(), reverse=True)))
    show("asks (px*1e4: qty)", dict(sorted(asks.items())))
    best_bid, best_ask = max(bids), min(asks)
    show("best bid", best_bid / 1e4)
    show("best ask", best_ask / 1e4)
    show("spread", f"{(best_ask - best_bid) / 1e4:.4f}")
    show("mid", f"{(best_ask + best_bid) / 2e4:.4f}")
    assert bids == {100_150: 120, 100_100: 150} and asks == {100_300: 200}
    assert best_ask - best_bid == 150 and (best_ask + best_bid) == 200_450

    discard, apply = snapshot_merge(5_000_100, 5_000_200, 5_000_123)
    show("snapshot merge: discard, apply", (discard, apply))
    assert (discard, apply) == (24, 77)

    years64, minutes32 = seq_wrap(1e7)
    show("64-bit sequence wrap at 10M msg/s (years)", f"{years64:,.0f}")
    show("32-bit sequence wrap at 1M msg/s (minutes)", f"{minutes32:.1f}")
    assert close(years64, 58_454, 1) and close(minutes32, 71.6, 0.05)

    print("== 09 backtester ==")
    events = [("trade", 1_500), ("cancel_ahead", 1_000), ("trade", 1_200), ("trade", 600)]
    ahead_path = [4_000, 4_000 - 1_500, 4_000 - 1_500 - 1_000, 4_000 - 1_500 - 1_000 - 1_200]
    show("shares ahead after each event (order-level)", ahead_path)
    assert ahead_path == [4_000, 2_500, 1_500, 300]
    pes_ahead = 4_000 - 1_500 - 1_200 - 600
    show("shares ahead after 600 trade (pessimistic)", pes_ahead)
    assert pes_ahead == 700
    opt = queue_fill(4_000, 300, events, cancels_from_ahead=True)
    pes = queue_fill(4_000, 300, events, cancels_from_ahead=False)
    show("queue fill, cancels ahead of us (filled, event)", opt)
    show("queue fill, cancels behind us (filled, event)", pes)
    assert opt == (300, 3) and pes == (0, None)
    pes_more = queue_fill(4_000, 300, [*events, ("trade", 1_000)], cancels_from_ahead=False)
    show("pessimistic after one more 1000 trade", pes_more)
    assert pes_more == (300, 4)

    imp = sqrt_impact(0.02, 500_000, 10_000_000)
    show("square-root impact (fraction)", f"{imp:.5f}")
    show("impact bp", f"{imp * 1e4:.1f}")
    show("impact cost on 500k shares at $40", f"{imp * 500_000 * 40:,.0f}")
    assert close(imp * 1e4, 44.7, 0.05) and close(imp * 500_000 * 40, 89_443, 1)

    arrival = 15 + 5 + 30
    show("earliest order arrival us", arrival)
    assert arrival == 50

    print("== 10 pricing library ==")
    p = bs(100, 100, 0.05, 0.2, 1.0)
    show("call", f"{p['call']:.4f}")
    show("put", f"{p['put']:.4f}")
    show("parity C - P", f"{p['call'] - p['put']:.4f}")
    show("K(1 - e^-rT)", f"{100 * (1 - math.exp(-0.05)):.4f}")
    show("delta", f"{p['delta']:.4f}")
    show("gamma", f"{p['gamma']:.6f}")
    show("vega", f"{p['vega']:.3f}")
    assert close(p["call"], 10.4506, 5e-5) and close(p["put"], 5.5735, 5e-5)
    assert close(p["call"] - p["put"], 100 * (1 - math.exp(-0.05)), 1e-12)
    assert close(p["delta"], 0.6368, 5e-5) and close(p["gamma"], 0.018762, 5e-7) and close(p["vega"], 37.524, 5e-4)

    fd = fd_delta_errors()
    show("forward optimal h", f"{fd['h_fwd']:.2e}")
    show("central optimal h", f"{fd['h_ctr']:.2e}")
    show("err forward h*", f"{fd['err_fwd_opt']:.1e}")
    show("err central h*", f"{fd['err_ctr_opt']:.1e}")
    show("err forward h=1", f"{fd['err_fwd_h1']:.2e}")
    show("err central h=1", f"{fd['err_ctr_h1']:.2e}")
    show("gamma / 2", f"{p['gamma'] / 2:.4f}")
    assert close(p["gamma"] / 2, 0.0094, 5e-5)
    show("err central h=1e-12", f"{fd['err_ctr_tiny']:.1e}")
    assert close(fd["h_fwd"], 1.49e-6, 0.01e-6) and close(fd["h_ctr"], 6.06e-4, 0.01e-4)
    assert fd["err_ctr_opt"] < 1e-9 and fd["err_fwd_opt"] < 1e-6
    assert fd["err_ctr_opt"] < fd["err_fwd_opt"]
    assert close(fd["err_fwd_h1"], 9.29e-3, 0.01e-3) and close(fd["err_ctr_h1"], 8.60e-5, 0.01e-5)
    assert fd["err_ctr_tiny"] > 1e-6

    n_inputs = 50 + 200
    show("bump pricings one-sided, central", (n_inputs + 1, 2 * n_inputs + 1))
    assert (n_inputs + 1, 2 * n_inputs + 1) == (251, 501)

    print("== 11 numerical python ==")
    nf = numpy_facts()
    for key, val in nf.items():
        show(key, val)
    assert nf["bytes"] == 400_000_000 and close(float(nf["mib"]), 381.47, 0.005)
    assert nf["strides"] == (40_000, 8) and nf["strides_T"] == (8, 40_000)
    assert nf["col_is_view"] and nf["col_stride"] == (40_000,)
    assert nf["broadcast"] == (3, 4, 5) and nf["broadcast_32_3"] == "error"
    assert nf["float32_2_24_plus_1"] == 2**24 and nf["ulp_f32_2_24"] == 2.0
    assert close(float(nf["ulp_f64_100"]), 1.42e-14, 0.01e-14)
    assert close(float(nf["sum_01_02_minus_03"]), 5.55e-17, 0.01e-17)
    lines_touched = 10_000
    show("cache lines touched for a column sum", lines_touched)
    show("bytes moved vs useful", (lines_touched * 64, 10_000 * 8))
    assert lines_touched * 64 // (10_000 * 8) == 8

    naive, welford, two_pass = naive_vs_welford()
    show("naive one-pass variance", naive)
    sq_dev = sum((v - 10.0) ** 2 for v in (4.0, 7.0, 13.0, 16.0))
    show("sum of squared deviations", sq_dev)
    assert sq_dev == 90.0
    show("ulp at 4e18", float(np.spacing(4e18)))
    assert np.spacing(4e18) == 512.0
    show("welford variance", welford)
    show("numpy two-pass variance", two_pass)
    assert welford == 30.0 and two_pass == 30.0 and close(naive, -170.67, 0.01)

    wrapped, exact = int32_notional()
    show("int32 price*qty wrapped", wrapped)
    show("exact", exact)
    assert exact == 5_000_000_000 and wrapped == exact - 2**32

    print("== 12 tick storage ==")
    cap = capacity(400e6, 40, 252, 4.0, 10, 3)
    for key, val in cap.items():
        show(key, f"{val:.3f}")
    assert close(cap["raw_day_gb"], 16.0, 1e-9) and close(cap["raw_year_tb"], 4.032, 1e-9)
    assert close(cap["comp_year_tb"], 1.008, 1e-9) and close(cap["total_tb"], 30.24, 1e-9)

    parts_total, parts_read = 252 * 64, 252
    show("partitions total, read", (parts_total, parts_read))
    assert parts_total == 16_128 and parts_total // parts_read == 64
    show("column fraction read (3 of 20)", 3 / 20)
    assert close(3 / 20, 0.15, 1e-12)

    trades = [10, 25, 40, 55]
    quotes = [5, 20, 30, 50]
    back = asof_join(trades, quotes, None)
    tol = asof_join(trades, quotes, 8)
    fwd = asof_join(trades, quotes, None, forward=True)
    show("as-of backward quote index", back)
    show("as-of with tolerance 8", tol)
    show("forward (look-ahead) index", fwd)
    assert back == [0, 1, 2, 3] and tol == [0, 1, None, 3] and fwd == [1, 2, 3, None]

    print("== 13 risk and OMS ==")
    wc = worst_case_long(3_000, 4_000, 4_000)
    show("worst-case long", wc)
    assert wc == 11_000 > 10_000
    netted = wc - 2_500
    show("netting open sells would give", netted)
    assert netted == 8_500
    collar_hi = 50.00 * 1.05
    show("buy collar upper bound", f"{collar_hi:.2f}")
    assert close(collar_hi, 52.50, 1e-12)
    assert collar_hi < 53.00
    show("notional 10,000 x 250 (millions)", 10_000 * 250 / 1e6)
    assert 10_000 * 250 == 2_500_000 > 1_000_000
    acc = token_bucket(20, 100, [(0.0, 50), (0.1, 15)])
    show("token bucket accepted", acc)
    assert acc == [20, 10]
    show("token bucket rejected", 65 - sum(acc))
    assert 65 - sum(acc) == 35
    legs = [round(q * px, 2) for q, px in [(300, 10.00), (200, 10.02), (500, 10.05)]]
    show("fill notionals", legs)
    assert legs == [3000.0, 2004.0, 5025.0]
    rows = exec_reports(1_000, [(300, 10.00), (200, 10.02), (500, 10.05)])
    for cum, leaves, avg in rows:
        show("CumQty, LeavesQty, AvgPx", (cum, leaves, round(avg, 4)))
    assert [(c, lv) for c, lv, _ in rows] == [(300, 700), (500, 500), (1000, 0)]
    assert close(rows[1][2], 10.008, 1e-9) and close(rows[2][2], 10.029, 1e-9)
    replace_leaves = 600 - 500
    show("leaves after replace to 600 with 500 filled", replace_leaves)
    assert replace_leaves == 100

    print("== 14 testing ==")
    d = ulp_distance(0.1 + 0.2, 0.3)
    show("ulp distance 0.1+0.2 vs 0.3", d)
    assert d == 1
    show("ulp at 0.3", float(np.spacing(0.3)))
    assert close(float(np.spacing(0.3)), 5.55e-17, 0.01e-17)
    show("(1e16 + 1) - 1e16", (1e16 + 1.0) - 1e16)
    show("(1e16 - 1e16) + 1", (1e16 - 1e16) + 1.0)
    assert (1e16 + 1.0) - 1e16 == 0.0 and (1e16 - 1e16) + 1.0 == 1.0
    se = 15.0 / math.sqrt(100_000)
    show("MC standard error", f"{se:.4f}")
    show("4 SE tolerance", f"{4 * se:.3f}")
    assert close(4 * se, 0.190, 5e-4)
    p4 = two_sided_tail(4.0)
    p3 = two_sided_tail(3.0)
    show("two-sided P(|Z|>4)", f"{p4:.2e}")
    show("two-sided P(|Z|>3)", f"{p3:.5f}")
    show("1 - P(|Z|>3)", f"{1 - p3:.4f}")
    assert close(1 - p3, 0.9973, 5e-5)
    flaky = 1 - (1 - p3) ** 200
    show("P(any of 200 3-SE tests fails)", f"{flaky:.3f}")
    flaky4 = 1 - (1 - p4) ** 200
    show("P(any of 200 4-SE tests fails)", f"{flaky4:.4f}")
    assert close(se, 0.0474, 5e-5) and close(p4, 6.33e-5, 0.01e-5) and close(p3, 0.0027, 5e-5)
    assert close(flaky, 0.418, 5e-4) and close(flaky4, 0.0126, 5e-5)
    fuzz = 1 - (1 - 1 / 65_536) ** 100_000
    show("P(hit 2-byte value in 100k random inputs)", f"{fuzz:.3f}")
    assert close(fuzz, 0.783, 5e-4)
    eps = float(np.finfo(float).eps)
    show("float64 eps, unit roundoff", (f"{eps:.2e}", f"{eps / 2:.2e}"))
    assert eps == 2.0**-52
    naive_bound = 1_000_000 * np.finfo(float).eps / 2
    show("naive summation relative bound n*u for n=1e6", f"{naive_bound:.2e}")
    assert close(naive_bound, 1.11e-10, 0.01e-10)

    print("all problem-set numbers asserted")


if __name__ == "__main__":
    main()
