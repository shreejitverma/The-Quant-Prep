"""Event-driven backtester with latency, FIFO queue position and a book-walking fill model.

Backs the numbers in 12-Quant-Development/09-Backtester-and-Simulator-Design.md.

Design (one instrument, prices in integer ticks of $0.01, times in integer microseconds):

* A single event heap keyed by (timestamp, sequence). The sequence number is a global
  insertion counter, so events with equal timestamps are processed in the order they were
  scheduled and two runs are bit-for-bit identical.
* Market data events come from a historical tape (book snapshots and trades). The exchange
  sees them at their tape time; the strategy sees them `md_latency` later.
* Orders sent by the strategy reach the simulated exchange `order_latency` later.
  Fill reports reach the strategy `md_latency` after the fill.
* Passive limit orders join the back of the FIFO queue at their price: `ahead` starts at the
  displayed size of other orders at that level when the order arrives.
  - A tape trade at our price consumes `ahead` first, then fills us.
  - A decrease in the displayed size not explained by trades is a cancellation; cancellations
    reduce `ahead` pro rata: ahead -= cancelled * ahead / others_at_level.
  - An increase in displayed size joins behind us and does not change `ahead`.
  - A trade strictly through our price fills all of our remaining quantity at our limit.
* At most one of our orders rests per (side, price); a second one raises.
* Market orders walk the latest book on the opposite side, level by level.
* The tape does not contain our orders, so our fills do not remove liquidity from later tape
  events (the standard "no market impact on replay" assumption, stated explicitly).
* Fees: passive fills earn a rebate, aggressive fills pay a fee, per share.

Run: uv run --no-project --with numpy python 12-Quant-Development/code/python/event_backtester.py
"""

from __future__ import annotations

import hashlib
import heapq
import math
import os
import subprocess
import sys
from dataclasses import dataclass, field

import numpy as np
from pcg_stream import PcgStream

TICK = 0.01  # dollars per price tick


# --------------------------------------------------------------------------- events


@dataclass(frozen=True)
class Book:
    """Tape book snapshot: lists of (price_ticks, size), best level first."""

    bids: tuple[tuple[int, int], ...]
    asks: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class Trade:
    price: int
    size: int
    aggressor: str  # "B" buyer lifted the offer, "S" seller hit the bid


@dataclass(frozen=True)
class NewOrder:
    oid: int
    side: str  # "B" or "S"
    qty: int
    price: int | None  # None means market order


@dataclass(frozen=True)
class FillReport:
    oid: int
    qty: int
    price: int
    liquidity: str  # "M" maker (passive) or "T" taker (aggressive)
    exch_time: int


@dataclass
class RestingOrder:
    oid: int
    side: str
    price: int
    leaves: int
    ahead: float
    arrival: int


# --------------------------------------------------------------------------- exchange


class SimulatedExchange:
    """Replays tape events and matches the strategy's orders against them."""

    def __init__(self) -> None:
        self.book = Book((), ())
        self.resting: dict[int, RestingOrder] = {}
        # Displayed size of *other* orders at each price we rest on, as we track it.
        self.tracked: dict[tuple[str, int], int] = {}
        self.queue_log: list[tuple[int, int, float]] = []  # (time, oid, ahead)

    @staticmethod
    def _level_size(levels: tuple[tuple[int, int], ...], price: int) -> int:
        for px, sz in levels:
            if px == price:
                return sz
        return 0

    def _side_levels(self, side: str) -> tuple[tuple[int, int], ...]:
        return self.book.bids if side == "B" else self.book.asks

    def on_book(self, t: int, book: Book) -> list[FillReport]:
        self.book = book
        for o in self.resting.values():
            key = (o.side, o.price)
            new_size = self._level_size(self._side_levels(o.side), o.price)
            old_size = self.tracked[key]
            if new_size < old_size:
                cancelled = old_size - new_size
                o.ahead = max(0.0, o.ahead - cancelled * o.ahead / old_size)
                self.queue_log.append((t, o.oid, o.ahead))
            self.tracked[key] = new_size
        return []

    def on_trade(self, t: int, tr: Trade) -> list[FillReport]:
        fills: list[FillReport] = []
        for o in list(self.resting.values()):
            hits_us = (o.side == "B" and tr.aggressor == "S") or (o.side == "S" and tr.aggressor == "B")
            if not hits_us:
                continue
            through = (o.side == "B" and tr.price < o.price) or (o.side == "S" and tr.price > o.price)
            if through:
                fills.append(FillReport(o.oid, o.leaves, o.price, "M", t))
                o.leaves = 0
            elif tr.price == o.price:
                key = (o.side, o.price)
                consumed_ahead = min(o.ahead, tr.size)
                o.ahead -= consumed_ahead
                remaining = tr.size - consumed_ahead
                if remaining > 0:
                    q = int(min(remaining, o.leaves))
                    if q > 0:
                        fills.append(FillReport(o.oid, q, o.price, "M", t))
                        o.leaves -= q
                # The tape trade removed tr.size shares of other orders from the level.
                self.tracked[key] = max(0, self.tracked[key] - tr.size)
                self.queue_log.append((t, o.oid, o.ahead))
            if o.leaves == 0:
                del self.resting[o.oid]
        return fills

    def on_order(self, t: int, o: NewOrder) -> list[FillReport]:
        fills, left = self._take(t, o)
        if o.price is None:
            if left > 0:
                raise RuntimeError(f"market order {o.oid} exhausted the book with {left} unfilled")
            return fills
        if left > 0:  # the unfilled remainder of a limit order rests at the back of the queue
            if any(r.side == o.side and r.price == o.price for r in self.resting.values()):
                # The queue model tracks one of our orders per level (`tracked` is keyed by level).
                raise RuntimeError(f"order {o.oid}: already resting at {o.side} {o.price}")
            size = self._level_size(self._side_levels(o.side), o.price)
            self.resting[o.oid] = RestingOrder(o.oid, o.side, o.price, left, float(size), t)
            self.tracked[(o.side, o.price)] = size
            self.queue_log.append((t, o.oid, float(size)))
        return fills

    def _take(self, t: int, o: NewOrder) -> tuple[list[FillReport], int]:
        """Walk the opposite side up to the limit price (no limit for a market order)."""
        levels = self.book.asks if o.side == "B" else self.book.bids
        fills: list[FillReport] = []
        left = o.qty
        for px, sz in levels:
            if left == 0:
                break
            if o.price is not None and ((o.side == "B" and px > o.price) or (o.side == "S" and px < o.price)):
                break
            q = min(left, sz)
            fills.append(FillReport(o.oid, q, px, "T", t))
            left -= q
        return fills, left


# --------------------------------------------------------------------------- engine


@dataclass
class Config:
    md_latency: int = 5  # exchange event -> strategy, microseconds
    order_latency: int = 10  # strategy send -> exchange, microseconds
    maker_rebate: float = 0.0020  # dollars per share earned on passive fills
    taker_fee: float = 0.0030  # dollars per share paid on aggressive fills


@dataclass
class Portfolio:
    position: int = 0
    cash: float = 0.0
    fees: float = 0.0
    fills: list[FillReport] = field(default_factory=list)


class Engine:
    """The event loop. Strategies call `send` and receive `on_market` and `on_fill`."""

    def __init__(self, cfg: Config, tape: list[tuple[int, object]], strategy) -> None:
        self.cfg = cfg
        self.heap: list[tuple[int, int, str, object]] = []
        self.seq = 0
        self.exchange = SimulatedExchange()
        self.pf = Portfolio()
        self.strategy = strategy
        self.next_oid = 1
        self.now = 0
        self.side_of: dict[int, str] = {}
        for t, ev in tape:
            self.schedule(t, "tape", ev)

    def schedule(self, t: int, kind: str, payload: object) -> None:
        heapq.heappush(self.heap, (t, self.seq, kind, payload))
        self.seq += 1

    def send(self, side: str, qty: int, price: int | None) -> int:
        oid = self.next_oid
        self.next_oid += 1
        self.side_of[oid] = side
        self.schedule(self.now + self.cfg.order_latency, "order", NewOrder(oid, side, qty, price))
        return oid

    def _book_fills(self, fills: list[FillReport]) -> None:
        for f in fills:
            sign = 1 if self.side_of[f.oid] == "B" else -1
            self.pf.position += sign * f.qty
            self.pf.cash -= sign * f.qty * f.price * TICK
            fee = -self.cfg.maker_rebate * f.qty if f.liquidity == "M" else self.cfg.taker_fee * f.qty
            self.pf.fees += fee
            self.pf.fills.append(f)
            self.schedule(f.exch_time + self.cfg.md_latency, "fill", f)

    def run(self) -> Portfolio:
        while self.heap:
            t, _, kind, ev = heapq.heappop(self.heap)
            self.now = t
            if kind == "tape":
                if isinstance(ev, Book):
                    self._book_fills(self.exchange.on_book(t, ev))
                else:
                    assert isinstance(ev, Trade)
                    self._book_fills(self.exchange.on_trade(t, ev))
                self.schedule(t + self.cfg.md_latency, "md", ev)
            elif kind == "order":
                assert isinstance(ev, NewOrder)
                self._book_fills(self.exchange.on_order(t, ev))
            elif kind == "md":
                self.strategy.on_market(self, ev)
            elif kind == "fill":
                self.strategy.on_fill(self, ev)
        return self.pf

    def mark(self, mid_ticks: float) -> float:
        return self.pf.cash + self.pf.position * mid_ticks * TICK - self.pf.fees


# --------------------------------------------------------------------------- known-answer test


class JoinBidThenExit:
    """Join the best bid with 100 shares on the first book; when fully filled, sell 100 at market."""

    def __init__(self) -> None:
        self.joined = False
        self.filled = 0
        self.exited = False
        self.events: list[tuple[int, str]] = []

    def on_market(self, eng: Engine, ev: object) -> None:
        if not self.joined and isinstance(ev, Book):
            self.joined = True
            eng.send("B", 100, ev.bids[0][0])
            self.events.append((eng.now, "send buy limit"))

    def on_fill(self, eng: Engine, f: FillReport) -> None:
        if eng.side_of[f.oid] == "B":
            self.filled += f.qty
            if self.filled == 100 and not self.exited:
                self.exited = True
                eng.send("S", 100, None)
                self.events.append((eng.now, "send market sell"))


def known_answer_tape() -> list[tuple[int, object]]:
    """Hand-built tape; the note derives every fill and the PnL from it."""
    return [
        (0, Book(((10000, 500), (9999, 800)), ((10001, 300), (10002, 600)))),
        (20, Book(((10000, 700), (9999, 800)), ((10001, 300), (10002, 600)))),  # +200 join behind us
        (30, Book(((10000, 560), (9999, 800)), ((10001, 300), (10002, 600)))),  # -140 cancels
        (40, Trade(10000, 300, "S")),
        (41, Book(((10000, 260), (9999, 800)), ((10001, 300), (10002, 600)))),
        (50, Trade(10000, 150, "S")),
        (51, Book(((10000, 110), (9999, 800)), ((10001, 300), (10002, 600)))),
        # Bid level pulled. The asks stay above our 100.00 bid: an ask at or below a price where we rest
        # would have traded with us, and this simulator does not infer fills from book updates.
        (58, Book(((9999, 800), (9998, 500)), ((10001, 300), (10002, 600)))),
        (60, Trade(9999, 400, "S")),  # trades through our 100.00 bid
        (70, Book(((9999, 60), (9998, 500)), ((10001, 300), (10002, 600)))),
    ]


def run_known_answer() -> tuple[Engine, JoinBidThenExit]:
    strat = JoinBidThenExit()
    eng = Engine(Config(), known_answer_tape(), strat)
    eng.run()
    return eng, strat


def fill_log_digest(fills: list[FillReport]) -> str:
    text = "\n".join(f"{f.exch_time},{f.oid},{f.qty},{f.price},{f.liquidity}" for f in fills)
    return hashlib.sha256(text.encode()).hexdigest()


# --------------------------------------------------------------------------- random tape for determinism


class Quoter:
    """Keeps one bid and one offer at the touch; requotes a side only after its order is fully filled.

    It tracks its own leaves quantity from fill reports and never reads simulator state.
    """

    def __init__(self) -> None:
        self.live: dict[str, int | None] = {"B": None, "S": None}
        self.leaves: dict[int, int] = {}

    def on_market(self, eng: Engine, ev: object) -> None:
        if not isinstance(ev, Book) or not ev.bids or not ev.asks:
            return
        for side, level in (("B", ev.bids[0]), ("S", ev.asks[0])):
            if self.live[side] is None:
                oid = eng.send(side, 100, level[0])
                self.live[side] = oid
                self.leaves[oid] = 100

    def on_fill(self, eng: Engine, f: FillReport) -> None:
        self.leaves[f.oid] -= f.qty
        side = eng.side_of[f.oid]
        if self.leaves[f.oid] == 0 and self.live[side] == f.oid:
            self.live[side] = None


def random_tape(seed: int, n: int) -> list[tuple[int, object]]:
    rng = PcgStream(seed)
    mid = 10000
    t = 0
    tape: list[tuple[int, object]] = []
    for _ in range(n):
        t += int(rng.integers(1, 20))
        if rng.uniform() < 0.7:
            mid += int(rng.choice([-1, 0, 0, 1]))
            bsz, asz = (int(x) for x in rng.integers(100, 1000, size=2))
            tape.append((t, Book(((mid, bsz), (mid - 1, 1000)), ((mid + 1, asz), (mid + 2, 1000)))))
        else:
            side = "S" if rng.uniform() < 0.5 else "B"
            px = mid if side == "S" else mid + 1
            tape.append((t, Trade(px, int(rng.integers(50, 600)), side)))
    return tape


SEED7_DIGEST = "2d735870cb68f066a0b17cd5dc7c0fd975bdd3c04002eb5f40408fde3f4d10f2"


def run_random(seed: int) -> Engine:
    eng = Engine(Config(), random_tape(seed, 5000), Quoter())
    eng.run()
    return eng


# --------------------------------------------------------------------------- look-ahead demonstration


def bid_ask_bounce(seed: int, n: int, half_spread: float) -> tuple[float, float]:
    """Contrarian strategy on trade prints that bounce between bid and ask around a random-walk mid.

    Signal at print t: buy one unit after a down-tick, sell one unit after an up-tick.
    Same-print fill (look-ahead): execute at the very print that produced the signal.
    Realistic fill: execute on the next event, crossing the spread (buy at ask, sell at bid).
    Returns the mean PnL per trade, in the same units as the mid, for both assumptions,
    each holding its position for one print and marking out at the mid of the print after its entry.
    """
    rng = PcgStream(seed)
    mid = 100.0 + np.cumsum(rng.normal(0.0, 0.001, n))
    side = rng.choice([-1.0, 1.0], n)  # -1 print at bid, +1 print at ask
    prints = mid + side * half_spread
    sig = -np.sign(np.diff(prints))  # contrarian: +1 buy after a down-tick
    sig = sig[:-2]  # signal at print t uses prints[t-1] and prints[t]; the realistic leg needs two more prints
    t = np.arange(1, n - 2)
    # Look-ahead fill at the print that produced the signal, exit at the next mid.
    pnl_same = sig * (mid[t + 1] - prints[t])
    # Realistic fill at the next event crossing the spread, exit one print later at the following mid.
    entry = mid[t + 1] + sig * half_spread
    pnl_next = sig * (mid[t + 2] - entry)
    mask = sig != 0
    return float(pnl_same[mask].mean()), float(pnl_next[mask].mean())


# --------------------------------------------------------------------------- impact arithmetic


def sqrt_impact_bps(daily_vol: float, participation: float, y: float = 1.0) -> float:
    """Square-root impact rule of thumb: cost = Y * sigma_daily * sqrt(Q / V), in basis points."""
    return y * daily_vol * math.sqrt(participation) * 1e4


# --------------------------------------------------------------------------- main


def main() -> None:
    eng, strat = run_known_answer()
    pf = eng.pf
    cfg = Config()
    print("Known-answer test")
    print(f"  config: md latency {cfg.md_latency} us, order latency {cfg.order_latency} us,", end=" ")
    print(f"maker rebate {cfg.maker_rebate:.4f}, taker fee {cfg.taker_fee:.4f} dollars per share")
    for t, ev in known_answer_tape():
        if isinstance(ev, Book):
            bids = ", ".join(f"{px * TICK:.2f} x {sz}" for px, sz in ev.bids)
            asks = ", ".join(f"{px * TICK:.2f} x {sz}" for px, sz in ev.asks)
            print(f"  tape t={t}: book bids [{bids}] asks [{asks}]")
        else:
            assert isinstance(ev, Trade)
            print(f"  tape t={t}: trade {ev.size} at {ev.price * TICK:.2f} aggressor {ev.aggressor}")
    print("  strategy events:", strat.events)
    assert strat.events == [(5, "send buy limit"), (65, "send market sell")]
    print("  queue log (time, oid, shares ahead):", eng.exchange.queue_log)
    expected_queue = [(15, 1, 500.0), (30, 1, 400.0), (40, 1, 100.0), (50, 1, 0.0), (58, 1, 0.0)]
    assert eng.exchange.queue_log == expected_queue, eng.exchange.queue_log
    fills = [(f.exch_time, f.oid, f.qty, f.price, f.liquidity) for f in pf.fills]
    print("  fills (exch time, oid, qty, price ticks, liquidity):", fills)
    assert fills == [(50, 1, 50, 10000, "M"), (60, 1, 50, 10000, "M"), (75, 2, 60, 9999, "T"), (75, 2, 40, 9998, "T")]
    gross = pf.cash
    buy_cost = sum(f.qty * f.price * TICK for f in pf.fills if f.oid == 1)
    legs = [round(f.qty * f.price * TICK, 2) for f in pf.fills if f.oid == 2]
    rebate = sum(f.qty for f in pf.fills if f.liquidity == "M") * Config().maker_rebate
    fee = sum(f.qty for f in pf.fills if f.liquidity == "T") * Config().taker_fee
    print(f"  buy cost {buy_cost:.2f}, sell legs {legs}, sell proceeds {sum(legs):.2f}, rebate {rebate:.2f}, taker fee {fee:.2f}")
    assert abs(buy_cost - 10000.00) < 1e-9 and legs == [5999.40, 3999.20] and abs(sum(legs) - 9998.60) < 1e-9
    assert abs(rebate - 0.20) < 1e-12 and abs(fee - 0.30) < 1e-12
    print(f"  position {pf.position}, gross cash PnL {gross:.2f}, fees {pf.fees:.2f}, net {gross - pf.fees:.2f}")
    assert pf.position == 0
    assert abs(gross - (-1.40)) < 1e-9
    assert abs(pf.fees - 0.10) < 1e-12
    assert abs((gross - pf.fees) - (-1.50)) < 1e-9

    # Same scenario with zero latency: the strategy joins at t=0 and is in the same queue position
    # (the book did not change between 0 and 15), but exits at t=60 against the t=58 book.
    eng0 = Engine(Config(md_latency=0, order_latency=0), known_answer_tape(), JoinBidThenExit())
    eng0.run()
    fills0 = [(f.exch_time, f.qty, f.price, f.liquidity) for f in eng0.pf.fills]
    net0 = eng0.pf.cash - eng0.pf.fees
    print("  zero-latency fills:", fills0, f"gross {eng0.pf.cash:.2f} net {net0:.2f}")
    assert abs(eng0.pf.cash - (-1.00)) < 1e-9
    latency_cost = net0 - (gross - pf.fees)
    print(f"  latency cost on this tape {latency_cost:.2f}")
    assert abs(latency_cost - 0.40) < 1e-9
    assert fills0 == [(50, 50, 10000, "M"), (60, 50, 10000, "M"), (60, 100, 9999, "T")]
    assert abs(net0 - (-1.10)) < 1e-9

    print("Determinism")
    a = run_random(7)
    da = fill_log_digest(a.pf.fills)
    print(f"  seed 7: {len(a.pf.fills)} fills, position {a.pf.position}, digest {da[:16]}")
    # Replays in fresh interpreters with different string-hash seeds: iterating a set or a dict keyed by
    # strings would change order across these processes, and the digests would differ.
    for hash_seed in ("1", "2"):
        out = subprocess.run(
            [sys.executable, __file__, "--digest", "7"],
            env={**os.environ, "PYTHONHASHSEED": hash_seed},
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"  PYTHONHASHSEED={hash_seed} replay digest {out.stdout.strip()[:16]}")
        assert out.stdout.strip() == da
    # The regression artifact: the seed-7 fill log, pinned. A change to the fill model changes it.
    assert da == SEED7_DIGEST and len(a.pf.fills) > 50
    c = run_random(8)
    assert fill_log_digest(c.pf.fills) != da

    print("Look-ahead: bid-ask bounce")
    print("  inputs: seed 11, 200,000 prints, half-spread 0.005, mid step sd 0.001")
    same, nxt = bid_ask_bounce(seed=11, n=200_000, half_spread=0.005)
    print(f"  mean PnL per trade, same-print fill {same:+.5f}, next-event fill {nxt:+.5f}")
    # Theory: half the time consecutive prints sit on opposite sides; then the contrarian signal earns the
    # half-spread h. Otherwise the signal is noise with zero mean. So E[same] is about h / 2 = 0.0025.
    print(f"  theory: same-print about h/2 = {0.005 / 2:.4f}, next-event about -h = {-0.005:.4f}")
    # Note 09 example 3 quotes the seed-11 printed value +0.00249 and the theory value about +0.0025.
    assert f"{same:+.5f}" == "+0.00249"
    assert abs(same - 0.0025) < 0.0002
    # A realistic fill pays the half-spread h and then holds one mid step, which is independent of the
    # signal and has mean 0, so E[next] = -h; the standard error is 0.001 / sqrt(trades), about 2.2e-6.
    assert f"{nxt:+.4f}" == "-0.0050" and abs(nxt - (-0.005)) < 5 * 0.001 / np.sqrt(200_000)

    print("Square-root impact")
    for vol, part in ((0.02, 0.01), (0.02, 0.04), (0.015, 0.10)):
        bps = sqrt_impact_bps(vol, part)
        print(f"  sigma {vol:.3f}, Q/V {part:.2f}: {bps:.1f} bp")
    # Note 09 example 4 and card qd-bt-sqrt-impact quote 20.0, 40.0 and 47.4 bp.
    assert f"{sqrt_impact_bps(0.02, 0.01):.1f}" == "20.0"
    assert f"{sqrt_impact_bps(0.02, 0.04):.1f}" == "40.0"
    assert f"{sqrt_impact_bps(0.015, 0.10):.1f}" == "47.4"

    print("all assertions passed")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--digest":
        print(fill_log_digest(run_random(int(sys.argv[2])).pf.fills))
    else:
        main()
