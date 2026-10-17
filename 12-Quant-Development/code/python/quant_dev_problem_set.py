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
import zlib
from dataclasses import dataclass

import numpy as np


def show(label: str, value: object) -> None:
    print(f"{label}: {value}")


def check(label: str, value: object, quoted: str, fmt: str = "") -> None:
    """Print a computed value at the note's rounding and assert it equals the literal the note quotes."""
    shown = format(value, fmt)
    print(f"{label}: {shown}")
    assert shown == quoted, f"{label}: computed {shown}, the note quotes {quoted}"


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


def ab_double_loss(packets_per_day: float, p_loss: float) -> tuple[float, float, float, float]:
    per_line = packets_per_day * p_loss
    hidden = packets_per_day * 2 * p_loss * (1 - p_loss)  # lost on exactly one line: the other line fills it
    both = packets_per_day * p_loss * p_loss
    days_between = 1.0 / both
    return per_line, hidden, both, days_between


def itch_field_ranges() -> dict[str, float]:
    max_price_raw = round(200_000.0000 * 10**4)  # Price(4): 4 implied decimal places
    ns_per_day = 86_400 * 10**9
    max_ts = 2**48 - 1
    return {
        "max_price_raw": max_price_raw,
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


def queue_fill(ahead: int, my_qty: int, events: list[tuple[str, int]], cancels_from_ahead: bool) -> tuple[int, int | None, list[int]]:
    """FIFO queue: trades eat from the front; cancels shrink 'ahead' only if assumed ahead of us.

    Returns (filled quantity, index of the event that completed the fill or None, shares ahead
    initially and after each event).
    """
    filled = 0
    done_at = None
    trace = [ahead]
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
        trace.append(ahead)
    return filled, done_at, trace


def sqrt_impact(sigma_daily: float, q: float, v: float, y: float = 1.0) -> float:
    return y * sigma_daily * math.sqrt(q / v)


def order_arrival_us(feed_us: float, strategy_us: float, entry_us: float) -> float:
    """Time after the print at which the order reaches the matching engine."""
    return feed_us + strategy_us + entry_us


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
    # S +- 1e-12 is not representable: the step actually taken differs from the nominal 2h.
    step_ratio = ((s + tiny) - (s - tiny)) / (2 * tiny)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
    gamma = npdf(d1) / (s * vol * math.sqrt(t))
    speed = -gamma / s * (d1 / (vol * math.sqrt(t)) + 1.0)  # third derivative of the call in S
    return {
        "exact": exact,
        "h_fwd": h_fwd,
        "h_ctr": h_ctr,
        "err_fwd_opt": abs(fwd_opt - exact),
        "err_ctr_opt": abs(ctr_opt - exact),
        "err_fwd_h1": abs(fwd_big - exact),
        "err_ctr_h1": abs(ctr_big - exact),
        "err_ctr_tiny": abs(ctr_tiny - exact),
        "trunc_fwd_opt": h_fwd / 2 * gamma,
        "trunc_ctr_opt": h_ctr**2 / 6 * abs(speed),
        "step_ratio": step_ratio,
        "step_error_tiny": exact * (1.0 - step_ratio),
    }


def bump_pricings(n_inputs: int, central: bool) -> int:
    """Count pricer calls for bump-and-reprice sensitivities to every input.

    One-sided differences need the base price plus one bump per input (n + 1); central differences
    need an up and a down bump per input and never use the base price (2n), as in note 10.
    """
    calls = 0

    def price(bump: tuple[int, int] | None) -> None:
        nonlocal calls
        calls += 1

    if not central:
        price(None)  # base price
    for i in range(n_inputs):
        price((i, +1))
        if central:
            price((i, -1))
    return calls


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


def naive_vs_welford() -> tuple[float, float, float, float, float]:
    x = 1e9 + np.array([4.0, 7.0, 13.0, 16.0])
    n = len(x)
    s1 = s2 = 0.0
    for v in x.tolist():  # plain left-to-right sums: deterministic IEEE arithmetic on every platform
        s1 += v
        s2 += v * v
    numerator = s2 - s1 * s1 / n
    naive = numerator / (n - 1)
    # Exactly rounded sums do not rescue the formula: the squares are already rounded.
    naive_exact_sums = (math.fsum(v * v for v in x.tolist()) - math.fsum(x.tolist()) ** 2 / n) / (n - 1)
    mean = 0.0
    m2 = 0.0
    for i, v in enumerate(x, 1):
        d = v - mean
        mean += d / i
        m2 += d * (v - mean)
    welford = m2 / (n - 1)
    two_pass = float(np.var(x, ddof=1))
    return numerator, naive, naive_exact_sums, welford, two_pass


def column_cache_lines(a: np.ndarray, col: int, line: int = 64) -> int:
    """Distinct cache lines touched when reading one column of a 2-D array."""
    base = a.__array_interface__["data"][0]
    addrs = base + np.arange(a.shape[0], dtype=np.int64) * a.strides[0] + col * a.strides[1]
    return len(set((addrs // line).tolist()))


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


def partitions_read(days: int, buckets: int, symbol: str) -> tuple[int, int]:
    """Date x hash-bucket partitions in total, and those a one-symbol query over all days must open."""
    bucket = zlib.crc32(symbol.encode()) % buckets
    parts = [(d, b) for d in range(days) for b in range(buckets)]
    return len(parts), sum(1 for _, b in parts if b == bucket)


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


def buy_collar(reference: float, pct: float, price: float) -> tuple[bool, float]:
    upper = reference * (1.0 + pct)
    return price <= upper, upper


def leaves_after_replace(new_order_qty: int, cum_qty: int) -> int:
    """FIX: OrderQty on a cancel/replace includes what has already executed."""
    return max(new_order_qty - cum_qty, 0)


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
    print("== constants ==")
    check("float64 machine epsilon", float(np.finfo(float).eps), "2.22e-16", ".2e")
    check("float32 integers exact up to 2^24", float(np.float32(2**24)), "16,777,216", ",.0f")

    print("== 08 feed handlers ==")
    bw = feed_bandwidth(2_000_000)
    check("UDP payload max", bw["udp_payload_max"], "1472")
    check("room for blocks after the MoldUDP64 header", bw["blocks_room"], "1452")
    check("message block bytes", bw["block"], "38")
    check("messages per 1500-byte MTU packet", bw["per_packet"], "38")
    check("IP packet bytes", bw["ip_bytes"], "1492")
    check("wire bytes per frame", bw["wire_bytes"], "1530")
    check("packets per second", bw["pps"], "52,631.6", ",.1f")
    check("Gbit/s batched", bw["gbps_batched"], "0.644", ".3f")
    check("wire bytes single-message frame", bw["single_wire"], "124")
    check("Gbit/s one message per packet", bw["gbps_single"], "1.984", ".3f")
    check("unbatched / batched bandwidth", bw["gbps_single"] / bw["gbps_batched"], "3", ".0f")

    g = gap_example()
    show("gap requests (seq, count)", g.requests)
    show("applied", f"{g.applied[0]}..{g.applied[-1]} ({len(g.applied)} messages)")
    show("next expected", g.expected)
    show("duplicates dropped", g.duplicates)
    assert g.requests == [(1004, 3)]
    assert g.applied == list(range(1001, 1009)) and g.expected == 1009 and g.duplicates == 2

    per_line, hidden, both, days = ab_double_loss(20e6, 1e-5)
    check("expected losses per line per day", per_line, "200", ".0f")
    check("expected single-line losses per day across both lines, hidden by arbitration", hidden, "400", ".0f")
    check("expected double losses per day", both, "0.002", ".3f")
    check("days between double losses", days, "500", ".0f")

    fr = itch_field_ranges()
    check("max Price(4) raw", fr["max_price_raw"], "2,000,000,000", ",")
    check("max Price(4) raw in hex", hex(fr["max_price_raw"]), "0x77359400")
    check("int32 max", fr["int32_max"], "2,147,483,647", ",")
    assert fr["max_price_raw"] < fr["int32_max"] < fr["uint32_max"]
    check("ns per day", float(fr["ns_per_day"]), "8.64e+13", ".2e")
    assert fr["ns_per_day"] < fr["ts48_max"]
    check("48-bit timestamp max hours", fr["ts48_hours"], "78.2", ".1f")
    check("32-bit ns counter wraps after seconds", fr["ts32_seconds"], "4.295", ".3f")

    bids, asks = build_book()
    show("bids (px*1e4: qty)", dict(sorted(bids.items(), reverse=True)))
    show("asks (px*1e4: qty)", dict(sorted(asks.items())))
    bid_levels = [f"{px / 1e4:.4f} x {q}" for px, q in sorted(bids.items(), reverse=True)]
    ask_levels = [f"{px / 1e4:.4f} x {q}" for px, q in sorted(asks.items())]
    check("bid levels", bid_levels, "['10.0150 x 120', '10.0100 x 150']")
    check("ask levels", ask_levels, "['10.0300 x 200']")
    best_bid, best_ask = max(bids), min(asks)
    check("spread", (best_ask - best_bid) / 1e4, "0.0150", ".4f")
    check("mid", (best_ask + best_bid) / 2e4, "10.0225", ".4f")

    discard, apply = snapshot_merge(5_000_100, 5_000_200, 5_000_123)
    check("snapshot merge: discard", discard, "24")
    check("snapshot merge: apply", apply, "77")

    years64, minutes32 = seq_wrap(1e7)
    check("64-bit sequence wrap at 10M msg/s (years)", years64, "58,454", ",.0f")
    check("32-bit sequence wrap at 1M msg/s (minutes)", minutes32, "71.6", ".1f")

    print("== 09 backtester ==")
    events = [("trade", 1_500), ("cancel_ahead", 1_000), ("trade", 1_200), ("trade", 600)]
    opt = queue_fill(4_000, 300, events, cancels_from_ahead=True)
    pes = queue_fill(4_000, 300, events, cancels_from_ahead=False)
    check("shares ahead before the 600 trade (order-level)", opt[2][:4], "[4000, 2500, 1500, 300]")
    check("shares ahead after the 600 trade (pessimistic)", pes[2][-1], "700")
    check("queue fill, cancels ahead of us (filled, event)", opt[:2], "(300, 3)")
    check("queue fill, cancels behind us (filled, event)", pes[:2], "(0, None)")
    pes_more = queue_fill(4_000, 300, [*events, ("trade", 1_000)], cancels_from_ahead=False)
    check("pessimistic after one more 1000 trade", pes_more[:2], "(300, 4)")

    imp = sqrt_impact(0.02, 500_000, 10_000_000)
    check("square-root impact (fraction)", imp, "0.00447", ".5f")
    check("impact bp", imp * 1e4, "44.7", ".1f")
    check("impact cost on 500k shares at $40", imp * 500_000 * 40, "89,443", ",.0f")

    check("earliest order arrival us", order_arrival_us(15, 5, 30), "50", ".0f")

    print("== 10 pricing library ==")
    p = bs(100, 100, 0.05, 0.2, 1.0)
    check("call", p["call"], "10.4506", ".4f")
    check("put", p["put"], "5.5735", ".4f")
    check("parity C - P", p["call"] - p["put"], "4.8771", ".4f")
    check("K(1 - e^-rT)", 100 * (1 - math.exp(-0.05)), "4.8771", ".4f")
    check("delta", p["delta"], "0.6368", ".4f")
    check("gamma", p["gamma"], "0.018762", ".6f")
    check("vega", p["vega"], "37.524", ".3f")

    fd = fd_delta_errors()
    check("forward optimal h", fd["h_fwd"], "1.49e-06", ".2e")
    check("central optimal h", fd["h_ctr"], "6.06e-04", ".2e")
    check("truncation forward h*: h/2 gamma", fd["trunc_fwd_opt"], "1.40e-08", ".2e")
    check("truncation central h*: h^2/6 |speed|", fd["trunc_ctr_opt"], "3.15e-11", ".2e")
    # The note quotes these three "on the reference machine" (1.7e-08, 3.0e-11, 8.0e-03): round-off
    # moves them with the platform's libm, so assert bands around the quoted values, not digits.
    show("err forward h* (libm-dependent)", f"{fd['err_fwd_opt']:.1e}")
    show("err central h* (libm-dependent)", f"{fd['err_ctr_opt']:.1e}")
    show("err central h=1e-12 (libm-dependent)", f"{fd['err_ctr_tiny']:.1e}")
    assert 1.0e-8 < fd["err_fwd_opt"] < 2.5e-8 and 1.0e-11 < fd["err_ctr_opt"] < 6.0e-11
    assert 1e-3 < fd["err_ctr_tiny"] < 5e-2
    assert fd["err_ctr_opt"] < fd["err_fwd_opt"]
    check("err forward h=1", fd["err_fwd_h1"], "9.29e-03", ".2e")
    check("err central h=1", fd["err_ctr_h1"], "8.60e-05", ".2e")
    check("gamma / 2", p["gamma"] / 2, "0.0094", ".4f")
    check("ulp at 100", float(np.spacing(100.0)), "1.42e-14", ".2e")
    check("actual step / nominal step at h=1e-12", fd["step_ratio"], "0.9948", ".4f")
    check("delta error from the step alone", fd["step_error_tiny"], "3.3e-03", ".1e")

    check("bump pricings one-sided", bump_pricings(50 + 200, central=False), "251")
    check("bump pricings central", bump_pricings(50 + 200, central=True), "500")

    print("== 11 numerical python ==")
    nf = numpy_facts()
    check("array bytes", nf["bytes"], "400,000,000", ",")
    check("array MiB", nf["mib"], "381.47", ".2f")
    check("strides", nf["strides"], "(40000, 8)")
    check("strides of the transpose", nf["strides_T"], "(8, 40000)")
    assert nf["col_is_view"] and nf["col_stride"] == (40_000,)
    check("broadcast (3, 1, 5) with (4, 1)", nf["broadcast"], "(3, 4, 5)")
    check("broadcast (3, 2) with (3,)", nf["broadcast_32_3"], "error")
    check("float32 2^24 + 1", nf["float32_2_24_plus_1"], "16,777,216", ",.0f")
    check("float32 ulp at 2^24", nf["ulp_f32_2_24"], "2", ".0f")
    check("0.1 + 0.2 - 0.3", nf["sum_01_02_minus_03"], "5.55e-17", ".2e")
    a = np.zeros((10_000, 5_000))
    lines = column_cache_lines(a, 0)
    check("column stride bytes", a[:, 0].strides[0], "40,000", ",")
    assert a[:, 0].strides[0] > 16 * 1024  # larger than a 4 KiB or 16 KiB page
    check("bytes moved for a column sum", lines * 64, "640,000", ",")
    check("useful bytes", a.shape[0] * a.itemsize, "80,000", ",")
    check("amplification", lines * 64 / (a.shape[0] * a.itemsize), "8", ".0f")
    lines_128 = column_cache_lines(a, 0, line=128)  # Apple silicon reports 128-byte lines (note 03)
    check("bytes moved for a column sum, 128-byte lines", lines_128 * 128, "1,280,000", ",")
    check("amplification, 128-byte lines", lines_128 * 128 / (a.shape[0] * a.itemsize), "16", ".0f")

    numerator, naive, naive_exact_sums, welford, two_pass = naive_vs_welford()
    check("naive one-pass variance, left-to-right sums", naive, "-170.67", ".2f")
    check("naive numerator sum(x^2) - sum(x)^2 / n", numerator, "-512", ".0f")
    # Oracle: the same left-to-right float64 evaluation redone in exact integers, rounding to the nearest
    # double (int -> float is correctly rounded) after every operation; the true numerator is 90.

    def rnd(i: int) -> int:
        return int(float(i))

    xs = [10**9 + d for d in (4, 7, 13, 16)]
    s1_i = s2_i = 0
    for v in xs:
        s1_i = rnd(s1_i + v)
        s2_i = rnd(s2_i + rnd(v * v))
    check("numerator redone in integers with explicit rounding", rnd(s2_i - rnd(s1_i * s1_i) // 4), "-512")
    check("exact numerator", sum(v * v for v in xs) - sum(xs) ** 2 // 4, "90")
    # The DSA note's -128.0 is the same numerator divided by n = 4 instead of n - 1 = 3.
    check("naive one-pass population variance", numerator / 4, "-128.0", ".1f")
    check("naive one-pass variance, exactly rounded sums", naive_exact_sums, "0.0", ".1f")
    sq_devs = [(v - 10.0) ** 2 for v in (4.0, 7.0, 13.0, 16.0)]
    check("squared deviations", [int(d) for d in sq_devs], "[36, 9, 9, 36]")
    check("sum of squared deviations", sum(sq_devs), "90", ".0f")
    check("ulp at 4e18", float(np.spacing(4e18)), "512", ".0f")
    assert welford == 30.0 and two_pass == 30.0  # exactly 30
    check("welford variance", welford, "30", ".0f")

    wrapped, exact = int32_notional()
    check("int32 price*qty wrapped", wrapped, "705,032,704", ",")
    check("exact", exact, "5,000,000,000", ",")
    assert wrapped == exact - 2**32

    print("== 12 tick storage ==")
    cap = capacity(400e6, 40, 252, 4.0, 10, 3)
    check("raw GB per day", cap["raw_day_gb"], "16", ".0f")
    check("raw TB per year", cap["raw_year_tb"], "4.032", ".3f")
    check("compressed TB per year", cap["comp_year_tb"], "1.008", ".3f")
    check("total TB", cap["total_tb"], "30.24", ".2f")

    parts_total, parts_read = partitions_read(252, 64, "AAPL")
    check("partitions total", parts_total, "16,128", ",")
    check("partitions read", parts_read, "252")
    check("fraction of partitions read", f"1/{parts_total // parts_read}", "1/64")
    widths = [8] * 20  # equal-width columns
    check("column fraction read (3 of 20)", sum(widths[:3]) / sum(widths), "15%", ".0%")

    trades = [10, 25, 40, 55]
    quotes = [5, 20, 30, 50]
    back = asof_join(trades, quotes, None)
    tol = asof_join(trades, quotes, 8)
    fwd = asof_join(trades, quotes, None, forward=True)
    show("as-of backward quote index", back)
    check("as-of with tolerance 8: quote times", [None if j is None else quotes[j] for j in tol], "[5, 20, None, 50]")
    check("forward (look-ahead): quote times", [None if j is None else quotes[j] for j in fwd], "[20, 30, 50, None]")
    check("staleness of the trade at 40", 40 - quotes[back[2]], "10")

    print("== 13 risk and OMS ==")
    wc = worst_case_long(3_000, 4_000, 4_000)
    check("worst-case long", wc, "11,000", ",")
    assert wc > 10_000  # rejected
    check("netting open sells would give", wc - 2_500, "8,500", ",")
    ok, upper = buy_collar(50.00, 0.05, 53.00)
    check("buy collar upper bound", upper, "52.50", ".2f")
    assert not ok  # the buy at 53.00 is rejected
    notional = 10_000 * 250.00
    check("notional 10,000 x 250 (millions)", notional / 1e6, "2.5", ".1f")
    assert notional > 1_000_000  # rejected
    acc = token_bucket(20, 100, [(0.0, 50), (0.1, 15)])
    check("token bucket accepted", acc, "[20, 10]")
    check("token bucket rejected", 65 - sum(acc), "35")
    fills = [(300, 10.00), (200, 10.02), (500, 10.05)]
    check("fill notionals", [f"{q * px:.0f}" for q, px in fills], "['3000', '2004', '5025']")
    rows = exec_reports(1_000, fills)
    check("CumQty, LeavesQty", [(c, lv) for c, lv, _ in rows], "[(300, 700), (500, 500), (1000, 0)]")
    check("AvgPx after fill 1", rows[0][2], "10.0000", ".4f")
    check("AvgPx after fill 2", rows[1][2], "10.008", ".3f")
    check("AvgPx after fill 3", rows[2][2], "10.029", ".3f")
    check("leaves after replace to 600 with 500 filled", leaves_after_replace(600, 500), "100")

    print("== 14 testing ==")
    check("ulp distance 0.1+0.2 vs 0.3", ulp_distance(0.1 + 0.2, 0.3), "1")
    check("ulp at 0.3", float(np.spacing(0.3)), "5.55e-17", ".2e")
    check("(1e16 + 1) - 1e16", (1e16 + 1.0) - 1e16, "0", ".0f")
    check("(1e16 - 1e16) + 1", (1e16 - 1e16) + 1.0, "1", ".0f")
    check("ulp at 1e16", float(np.spacing(1e16)), "2", ".0f")
    se = 15.0 / math.sqrt(100_000)
    check("MC standard error", se, "0.0474", ".4f")
    check("4 SE tolerance", 4 * se, "0.190", ".3f")
    p4 = two_sided_tail(4.0)
    p3 = two_sided_tail(3.0)
    check("two-sided P(|Z|>4)", p4, "6.33e-05", ".2e")
    check("two-sided P(|Z|>3)", p3, "0.00270", ".5f")
    check("1 - P(|Z|>3)", 1 - p3, "0.9973", ".4f")
    check("P(any of 200 3-SE tests fails)", 1 - (1 - p3) ** 200, "0.418", ".3f")
    check("P(any of 200 4-SE tests fails)", 1 - (1 - p4) ** 200, "0.0126", ".4f")
    check("P(hit 2-byte value in 100k random inputs)", 1 - (1 - 1 / 65_536) ** 100_000, "0.783", ".3f")
    eps = float(np.finfo(float).eps)
    assert eps == 2.0**-52
    check("unit roundoff u = eps/2", eps / 2, "1.11e-16", ".2e")
    check("naive summation relative bound n*u for n=1e6", 1_000_000 * eps / 2, "1.11e-10", ".2e")

    print("all problem-set numbers asserted")


if __name__ == "__main__":
    main()
