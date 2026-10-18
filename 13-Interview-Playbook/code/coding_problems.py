"""Quant-flavoured coding interview problems, each solved and tested against a brute force.

Backs 13-Interview-Playbook/07-Coding-Interviews-for-Quants.md.

1. Streaming mean and variance (Welford) and the cancellation failure of the naive formula.
2. Sliding-window maximum with a monotonic deque.
3. Streaming median with two heaps.
4. Time-window VWAP with a deque and exact integer running sums.
5. One-pass maximum drawdown.
6. A price-time-priority limit order book (add, cancel, match), the fully solved problem.
7. A FIX tag=value parser with BodyLength and CheckSum validation.
8. A seeded Monte Carlo check of a puzzle answer (expected rolls to two sixes in a row).

Every fast solution is compared with an obvious O(n^2) or sort-based reference on seeded random
inputs, which is how you test under interview time pressure.

Run: uv run --no-project --with numpy python 13-Interview-Playbook/code/coding_problems.py
"""

from __future__ import annotations

import heapq
import math
import random
from collections import deque
from dataclasses import dataclass

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> None:
    """Print `label = value` and assert it matches the literal the note quotes, to tolerance and to the printed digits."""
    printed, quoted = (s.removeprefix("-") if float(s) == 0 else s for s in (f"{value:{fmt}}", f"{expected:{fmt}}"))
    print(f"{label} = {printed}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    assert printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"


# ---------------------------------------------------------------------------
# 1. Streaming mean and variance
# ---------------------------------------------------------------------------


class Welford:
    """Numerically stable running mean and sample variance in O(1) memory."""

    def __init__(self) -> None:
        self.n, self.mean, self.m2 = 0, 0.0, 0.0

    def push(self, x: float) -> None:
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        self.m2 += delta * (x - self.mean)

    def variance(self) -> float:
        return self.m2 / (self.n - 1) if self.n > 1 else math.nan


def naive_variance(xs: list[float]) -> float:
    n, s, s2 = len(xs), sum(xs), sum(x * x for x in xs)
    return (s2 - s * s / n) / (n - 1)


def section_welford() -> None:
    print("\n== 1. Welford ==")
    # Backs int-code-welford-cancellation and the Core concepts table.
    xs = [1e9 + d for d in (4.0, 7.0, 13.0, 16.0)]
    w = Welford()
    for x in xs:
        w.push(x)
    exact = sum((d - 10.0) ** 2 for d in (4.0, 7.0, 13.0, 16.0)) / 3  # offsets have mean 10
    check("Welford variance of 1e9 + [4, 7, 13, 16]", w.variance(), 30.0, 1e-9, ".1f")
    assert exact == 30.0
    check("naive sum-of-squares variance, offset 1e9", naive_variance(xs), 0.0, 0.0, ".1f")
    sum_sq = sum(x * x for x in xs)
    check("sum of squares, offset 1e9", sum_sq / 1e18, 4.0, 0.01, ".1f")
    check("spacing of doubles at that magnitude (ulp)", math.ulp(sum_sq), 512.0, 0.0, ".0f")
    xs10 = [1e10 + d for d in (4.0, 7.0, 13.0, 16.0)]
    w10 = Welford()
    for x in xs10:
        w10.push(x)
    check("Welford variance, offset 1e10", w10.variance(), 30.0, 1e-9, ".1f")
    check("naive sum-of-squares variance, offset 1e10", naive_variance(xs10), 21845.33, 0.005, ".2f")
    rng = random.Random(1)
    for _ in range(200):
        data = [rng.gauss(0, 1) for _ in range(rng.randint(2, 50))]
        w = Welford()
        for x in data:
            w.push(x)
        m = sum(data) / len(data)
        two_pass = sum((x - m) ** 2 for x in data) / (len(data) - 1)
        assert abs(w.variance() - two_pass) < 1e-12 * max(1.0, two_pass)
    print("Welford matches two-pass on 200 random streams")


# ---------------------------------------------------------------------------
# 2. Sliding-window maximum
# ---------------------------------------------------------------------------


def window_max(xs: list[int], k: int) -> list[int]:
    """Max of each length-k window in O(n): the deque holds indices of a decreasing run."""
    dq: deque[int] = deque()
    out = []
    for i, x in enumerate(xs):
        while dq and xs[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(xs[dq[0]])
    return out


def section_window_max() -> None:
    print("\n== 2. Sliding-window maximum ==")
    # Backs int-code-window-max.
    assert window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    rng = random.Random(2)
    for _ in range(300):
        n, k = rng.randint(1, 60), rng.randint(1, 10)
        xs = [rng.randint(-20, 20) for _ in range(n)]
        if k > n:
            continue
        assert window_max(xs, k) == [max(xs[i : i + k]) for i in range(n - k + 1)]
    print("window_max matches brute force on 300 random cases")


# ---------------------------------------------------------------------------
# 3. Streaming median
# ---------------------------------------------------------------------------


class StreamingMedian:
    """Lower half in a max-heap (negated), upper half in a min-heap; sizes differ by at most one."""

    def __init__(self) -> None:
        self.lo: list[float] = []
        self.hi: list[float] = []

    def push(self, x: float) -> None:
        if self.lo and x > -self.lo[0]:
            heapq.heappush(self.hi, x)
        else:
            heapq.heappush(self.lo, -x)
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        elif len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def median(self) -> float:
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2


def section_streaming_median() -> None:
    print("\n== 3. Streaming median ==")
    # Backs int-code-streaming-median.
    rng = random.Random(3)
    for _ in range(100):
        sm, seen = StreamingMedian(), []
        for _ in range(rng.randint(1, 80)):
            x = rng.randint(-50, 50)
            sm.push(x)
            seen.append(x)
            s, n = sorted(seen), len(seen)
            ref = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
            assert sm.median() == ref
    print("StreamingMedian matches sort-based median on 100 random streams")


# ---------------------------------------------------------------------------
# 4. Time-window VWAP
# ---------------------------------------------------------------------------


def window_vwap(trades: list[tuple[int, int, int]], window: int) -> list[float]:
    """VWAP of trades with time in (t - window, t] after each trade; prices in integer ticks keep sums exact."""
    dq: deque[tuple[int, int, int]] = deque()
    pq_sum = q_sum = 0
    out = []
    for t, p, q in trades:
        dq.append((t, p, q))
        pq_sum += p * q
        q_sum += q
        while dq[0][0] <= t - window:
            _, p0, q0 = dq.popleft()
            pq_sum -= p0 * q0
            q_sum -= q0
        out.append(pq_sum / q_sum)
    return out


def section_vwap() -> None:
    print("\n== 4. Time-window VWAP ==")
    # Backs the Worked examples VWAP trace and int-code-vwap-exact-sums.
    trades = [(0, 10000, 100), (2, 10010, 300), (5, 10020, 200), (6, 9990, 100)]
    v = window_vwap(trades, 5)
    check("VWAP at t=5 with a 5-second window (ticks)", v[2], 10014.0, 1e-9, ".1f")
    check("VWAP at t=6 with a 5-second window (ticks)", v[3], 10010.0, 1e-9, ".1f")
    # The trace's products at t=6: price x size for each trade in the window.
    for (_, p, q), prod in zip(trades[1:], (3003000, 2004000, 999000), strict=True):
        check(f"{p} x {q}", p * q, prod, 0, ".0f")
    rng = random.Random(4)
    for _ in range(200):
        t, trades = 0, []
        for _ in range(rng.randint(1, 40)):
            t += rng.randint(0, 3)
            trades.append((t, rng.randint(9900, 10100), rng.randint(1, 500)))
        w = rng.randint(1, 10)
        fast = window_vwap(trades, w)
        for i, (ti, _, _) in enumerate(trades):
            sub = [(p, q) for tj, p, q in trades[: i + 1] if tj > ti - w]
            assert fast[i] == sum(p * q for p, q in sub) / sum(q for _, q in sub)
    print("window_vwap matches brute force exactly on 200 random tapes")


# ---------------------------------------------------------------------------
# 5. Maximum drawdown
# ---------------------------------------------------------------------------


def max_drawdown(prices: list[float]) -> tuple[float, int, int]:
    """Most negative peak-to-trough return, with peak and trough indices, in one pass."""
    peak_i, best = 0, (0.0, 0, 0)
    for i, p in enumerate(prices):
        if p > prices[peak_i]:
            peak_i = i
        dd = p / prices[peak_i] - 1
        if dd < best[0]:
            best = (dd, peak_i, i)
    return best


def section_drawdown() -> None:
    print("\n== 5. Maximum drawdown ==")
    # Backs the Worked examples drawdown trace and int-code-max-drawdown.
    prices = [100.0, 120.0, 90.0, 130.0, 80.0, 110.0]
    dd, i, j = max_drawdown(prices)
    check("max drawdown of [100, 120, 90, 130, 80, 110] (%)", 100 * dd, -38.46, 0.005, ".2f")
    assert (i, j) == (3, 4)
    check("drawdown from 120 to 90 (%)", 100 * (90 / 120 - 1), -25.00, 1e-9, ".2f")
    rng = random.Random(5)
    for _ in range(300):
        ps = [rng.uniform(50, 150) for _ in range(rng.randint(1, 40))]
        ref = min((ps[j] / ps[i] - 1 for i in range(len(ps)) for j in range(i, len(ps))), default=0.0)
        assert abs(max_drawdown(ps)[0] - min(ref, 0.0)) < 1e-12
    print("max_drawdown matches O(n^2) brute force on 300 random paths")


# ---------------------------------------------------------------------------
# 6. Price-time-priority limit order book
# ---------------------------------------------------------------------------


@dataclass
class Order:
    oid: int
    side: str  # "B" or "S"
    price: int  # integer ticks
    qty: int


class OrderBook:
    """Limit order book with price-time priority.

    levels[side][price] is a FIFO of order ids; heaps[side] holds each price once (bids negated).
    Cancel removes the id from `orders` only; dead ids are skipped lazily when they reach a queue front,
    so cancel is O(1) and every id is popped at most once.
    """

    def __init__(self) -> None:
        self.levels: dict[str, dict[int, deque[int]]] = {"B": {}, "S": {}}
        self.heaps: dict[str, list[int]] = {"B": [], "S": []}
        self.orders: dict[int, Order] = {}

    def best(self, side: str) -> int | None:
        heap, levels = self.heaps[side], self.levels[side]
        while heap:
            price = -heap[0] if side == "B" else heap[0]
            queue = levels[price]
            while queue and queue[0] not in self.orders:
                queue.popleft()
            if queue:
                return price
            heapq.heappop(heap)
            del levels[price]
        return None

    def add(self, oid: int, side: str, price: int, qty: int) -> list[tuple[int, int, int, int]]:
        """Match against the opposite side, rest any remainder; return fills (aggressor, resting, price, qty)."""
        opp, fills = ("S" if side == "B" else "B"), []
        while qty > 0:
            best = self.best(opp)
            if best is None or (best > price if side == "B" else best < price):
                break
            resting = self.orders[self.levels[opp][best][0]]
            traded = min(qty, resting.qty)
            fills.append((oid, resting.oid, best, traded))
            qty -= traded
            resting.qty -= traded
            if resting.qty == 0:
                del self.orders[resting.oid]
                self.levels[opp][best].popleft()
        if qty > 0:
            if price not in self.levels[side]:
                self.levels[side][price] = deque()
                heapq.heappush(self.heaps[side], -price if side == "B" else price)
            self.levels[side][price].append(oid)
            self.orders[oid] = Order(oid, side, price, qty)
        return fills

    def cancel(self, oid: int) -> bool:
        return self.orders.pop(oid, None) is not None


class NaiveBook:
    """Reference: scan every resting order for the best (price, arrival) on each fill."""

    def __init__(self) -> None:
        self.resting: list[list[int | str]] = []  # [seq, oid, side, price, qty]
        self.seq = 0

    def add(self, oid: int, side: str, price: int, qty: int) -> list[tuple[int, int, int, int]]:
        fills = []
        while qty > 0:
            cands = [r for r in self.resting if r[2] != side and (r[3] <= price if side == "B" else r[3] >= price)]
            if not cands:
                break
            r = min(cands, key=lambda r: ((r[3] if side == "B" else -r[3]), r[0]))
            traded = min(qty, r[4])
            fills.append((oid, r[1], r[3], traded))
            qty -= traded
            r[4] -= traded
            if r[4] == 0:
                self.resting.remove(r)
        if qty > 0:
            self.seq += 1
            self.resting.append([self.seq, oid, side, price, qty])
        return fills

    def cancel(self, oid: int) -> bool:
        for r in self.resting:
            if r[1] == oid:
                self.resting.remove(r)
                return True
        return False


def section_order_book() -> None:
    print("\n== 6. Limit order book ==")
    # Backs the fully solved problem in Worked examples and int-code-lob-*.
    book = OrderBook()
    assert book.add(1, "S", 101, 10) == []
    assert book.add(2, "S", 101, 5) == []
    assert book.add(3, "S", 102, 7) == []
    assert book.add(4, "B", 99, 3) == []
    assert book.cancel(2)
    fills = book.add(5, "B", 102, 15)
    assert fills == [(5, 1, 101, 10), (5, 3, 102, 5)], fills
    vwap = sum(p * q for _, _, p, q in fills) / sum(q for *_, q in fills)
    check("order 5 fill VWAP (ticks)", vwap, 101.3333, 1e-3)
    assert (book.best("B"), book.best("S"), book.orders[3].qty) == (99, 102, 2)
    print("hand scenario: fills (5,1,101,10), (5,3,102,5); best bid 99, best ask 102, order 3 has 2 left")

    rng = random.Random(6)
    n_ops = 0
    for _ in range(300):
        fast, slow, live = OrderBook(), NaiveBook(), []
        for oid in range(1, rng.randint(2, 60)):
            if live and rng.random() < 0.25:
                victim = rng.choice(live)
                live.remove(victim)
                assert fast.cancel(victim) == slow.cancel(victim)
            side = rng.choice("BS")
            price, qty = rng.randint(95, 105), rng.randint(1, 10)
            f1, f2 = fast.add(oid, side, price, qty), slow.add(oid, side, price, qty)
            assert f1 == f2, (f1, f2)
            live.append(oid)
            n_ops += 1
            for s in "BS":
                ref = [r[3] for r in slow.resting if r[2] == s]
                assert fast.best(s) == ((max(ref) if s == "B" else min(ref)) if ref else None)
    check("random adds (with interleaved cancels) matched against the naive book", n_ops, 8499, 0, ".0f")


# ---------------------------------------------------------------------------
# 7. FIX tag=value parsing
# ---------------------------------------------------------------------------

SOH = "\x01"


def fix_checksum(text: str) -> int:
    return sum(text.encode("ascii")) % 256


def build_fix(body_fields: list[tuple[int, str]], begin: str = "FIX.4.2") -> str:
    body = "".join(f"{t}={v}{SOH}" for t, v in body_fields)
    head = f"8={begin}{SOH}9={len(body.encode('ascii'))}{SOH}"
    return f"{head}{body}10={fix_checksum(head + body):03d}{SOH}"


def parse_fix(msg: str) -> dict[int, str]:
    """Split on SOH, check BodyLength (9) and CheckSum (10), return tag -> value (last wins; no repeating groups)."""
    if not msg.endswith(SOH):
        raise ValueError("message must end with SOH")
    fields = [f.split("=", 1) for f in msg[:-1].split(SOH)]
    if [f[0] for f in fields[:2]] != ["8", "9"] or fields[-1][0] != "10":
        raise ValueError("bad header or trailer order")
    start = msg.index(SOH, msg.index(SOH) + 1) + 1  # first byte after 9=...SOH
    end = msg.rindex("10=")
    if int(fields[1][1]) != len(msg[start:end].encode("ascii")):
        raise ValueError("BodyLength mismatch")
    if int(fields[-1][1]) != fix_checksum(msg[:end]):
        raise ValueError("CheckSum mismatch")
    return {int(t): v for t, v in fields}


def section_fix() -> None:
    print("\n== 7. FIX parser ==")
    # Backs the FIX worked example and int-code-fix-checksum.
    body = [
        (35, "D"),
        (49, "CLIENT"),
        (56, "EXCH"),
        (34, "12"),
        (52, "20261017-14:30:00.000"),
        (11, "ORD1"),
        (55, "XYZ"),
        (54, "1"),
        (38, "100"),
        (40, "2"),
        (44, "101.25"),
    ]
    msg = build_fix(body)
    parsed = parse_fix(msg)
    print("message:", msg.replace(SOH, "|"))
    check("BodyLength (tag 9)", float(parsed[9]), 96.0, 0, ".0f")
    check("CheckSum (tag 10)", float(parsed[10]), 13.0, 0, ".0f")
    # Independent count of the body: sum of len("tag=value") + 1 for each body field.
    assert int(parsed[9]) == sum(len(f"{t}={v}") + 1 for t, v in body)
    # Independent checksum: numpy byte sum of everything before "10=", mod 256.
    raw = np.frombuffer(msg[: msg.rindex("10=")].encode("ascii"), dtype=np.uint8)
    assert int(parsed[10]) == int(raw.astype(np.int64).sum()) % 256
    assert msg.endswith(f"10=013{SOH}")
    corrupted = msg.replace("44=101.25", "44=101.26")
    try:
        parse_fix(corrupted)
        raise AssertionError("corruption not detected")
    except ValueError as e:
        assert "CheckSum" in str(e)
    print("a one-character price change is rejected by the checksum")


# ---------------------------------------------------------------------------
# 8. Monte Carlo check of a puzzle
# ---------------------------------------------------------------------------


def section_monte_carlo() -> None:
    print("\n== 8. Monte Carlo check: rolls until two sixes in a row ==")
    # Backs int-code-mc-check-two-sixes: exact answer by first-step equations, then a seeded simulation.
    # States: 0 = no trailing six, 1 = one trailing six. E0 = 1 + (5/6)E0 + (1/6)E1, E1 = 1 + (5/6)E0.
    a = np.array([[1 - 5 / 6, -1 / 6], [-5 / 6, 1.0]])
    e0 = float(np.linalg.solve(a, np.ones(2))[0])
    check("exact expected rolls (first-step equations)", e0, 42.0, 1e-9, ".1f")
    rng = np.random.default_rng(7)
    samples = []
    for _ in range(5):
        rolls = rng.integers(1, 7, size=(20_000, 1200))
        both = (rolls[:, 1:] == 6) & (rolls[:, :-1] == 6)
        assert both.any(axis=1).all(), "path length too short"
        samples.append(both.argmax(axis=1) + 2)
    x = np.concatenate(samples)
    mean, se = float(x.mean()), float(x.std(ddof=1) / math.sqrt(len(x)))
    check("simulated mean over 100,000 paths (seed 7)", mean, 41.99, 0.005, ".2f")
    check("standard error of the simulated mean", se, 0.13, 0.005, ".2f")
    check("z-score of simulation vs exact", (mean - e0) / se, -0.04, 0.005, ".2f")


if __name__ == "__main__":
    section_welford()
    section_window_max()
    section_streaming_median()
    section_vwap()
    section_drawdown()
    section_order_book()
    section_fix()
    section_monte_carlo()
    print("\nAll checks passed.")
