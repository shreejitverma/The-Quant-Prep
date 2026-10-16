"""Trading system design arithmetic and a sequenced, replayable state machine.

Used by 12-Quant-Development/06-System-Design-for-Trading.md.

Part 1 derives capacity and latency numbers from explicit, stated assumptions (they are inputs,
not market facts); every derived number is printed and asserted.
Part 2 demonstrates why exchanges and trading systems put a sequencer in front of a deterministic
state machine: replicas fed the same sequenced log agree bit for bit, replay from a snapshot
reproduces the live state, a gap in the sequence is detected and repaired from the journal, and
replicas that each apply events in their own arrival order diverge.

Run: python3 12-Quant-Development/code/python/qd_system_design.py
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import deque
from dataclasses import dataclass, field

# ----------------------------------------------------------------------------- part 1: capacity

ETH_WIRE_OVERHEAD = 8 + 12 + 14 + 4  # preamble/SFD, inter-frame gap, Ethernet header, FCS
IP_UDP = 20 + 8
MOLDUDP64_HEADER = 10 + 8 + 2  # session, sequence number, message count
MSG_BLOCK_LEN = 2  # each message is preceded by a 2-byte length


def capacity() -> None:
    # Assumptions (stated, illustrative).
    peak_msgs_per_s = 5_000_000
    avg_msg_bytes = 36  # an ITCH 5.0 Add Order is 36 bytes
    msgs_per_packet = 20
    session_s = 6.5 * 3600  # 09:30 to 16:00
    avg_msgs_per_s = 1_000_000
    compression = 4.0
    utilization_target = 0.7

    print("1a. market data bandwidth at peak")
    packet_payload = MOLDUDP64_HEADER + msgs_per_packet * (MSG_BLOCK_LEN + avg_msg_bytes)
    wire_bytes_per_packet = packet_payload + IP_UDP + ETH_WIRE_OVERHEAD
    packets_per_s = peak_msgs_per_s / msgs_per_packet
    gbps = packets_per_s * wire_bytes_per_packet * 8 / 1e9
    print(f"   packet: {packet_payload} B payload, {wire_bytes_per_packet} B on the wire")
    print(f"   {packets_per_s:,.0f} packets/s -> {gbps:.3f} Gbit/s")
    assert packet_payload == 780 and wire_bytes_per_packet == 846
    assert packets_per_s == 250_000
    assert f"{gbps:.3f}" == "1.692"

    print("1b. per-message processing budget for one thread at peak")
    budget_ns = 1e9 / peak_msgs_per_s
    budget_at_target = budget_ns * utilization_target
    print(f"   {budget_ns:.0f} ns per message to keep up; {budget_at_target:.0f} ns at {utilization_target:.0%} utilization")
    assert budget_ns == 200 and f"{budget_at_target:.0f}" == "140"

    print("1c. daily capture storage")
    msgs_per_day = avg_msgs_per_s * session_s
    raw_gb = msgs_per_day * (avg_msg_bytes + MSG_BLOCK_LEN) / 1e9
    print(f"   {msgs_per_day:,.0f} messages/day, {raw_gb:,.1f} GB raw, {raw_gb / compression:,.1f} GB at {compression:.0f}x compression")
    print(f"   one year of 252 sessions compressed: {252 * raw_gb / compression / 1000:,.1f} TB")
    assert msgs_per_day == 23_400_000_000
    assert f"{raw_gb:.1f}" == "889.2"
    assert f"{raw_gb / compression:.1f}" == "222.3"
    assert f"{252 * raw_gb / compression / 1000:.1f}" == "56.0"

    print("1d. sequence number width")
    wrap_32_s = 2**32 / peak_msgs_per_s
    years_64 = 2**64 / 1e9 / (365.25 * 24 * 3600)
    print(f"   a 32-bit sequence number wraps after {wrap_32_s:,.0f} s ({wrap_32_s / 60:.1f} min) at peak")
    print(f"   a 64-bit counter at 1e9 per second lasts {years_64:,.0f} years")
    assert f"{wrap_32_s:.0f}" == "859" and f"{wrap_32_s / 60:.1f}" == "14.3"
    assert f"{years_64:.0f}" == "585"

    print("1e. recovery: replay from the last snapshot")
    snapshot_interval_s = 300
    events_since_snapshot = peak_msgs_per_s * snapshot_interval_s
    replay_rate = 20_000_000  # events/s a single-threaded replay can apply (assumption)
    print(f"   worst case {events_since_snapshot:,} events to replay, {events_since_snapshot / replay_rate:.0f} s at {replay_rate:,}/s")
    full_day_s = msgs_per_day / replay_rate
    print(f"   replaying a whole day instead: {full_day_s:,.0f} s ({full_day_s / 60:.1f} min)")
    assert events_since_snapshot == 1_500_000_000 and events_since_snapshot / replay_rate == 75
    assert full_day_s == 1170 and full_day_s / 60 == 19.5

    print("1f. failure detection by heartbeats")
    hb_ms, missed = 100, 3
    detect_ms = hb_ms * missed
    lost = peak_msgs_per_s * detect_ms / 1000
    print(f"   {missed} missed {hb_ms} ms heartbeats -> {detect_ms} ms to declare failure, {lost:,.0f} peak messages to recover")
    assert detect_ms == 300 and lost == 1_500_000


# ----------------------------------------------------------------------------- part 2: sequencing


@dataclass(frozen=True)
class Event:
    kind: str  # "new" or "cancel"
    order_id: int
    side: str = ""
    price: int = 0
    qty: int = 0
    trader: str = ""


@dataclass
class Book:
    """Deterministic price-time matcher: same inputs in the same order -> same state, always."""

    bids: dict[int, deque] = field(default_factory=dict)
    asks: dict[int, deque] = field(default_factory=dict)
    fills: list[tuple[int, int, int, int]] = field(default_factory=list)
    applied_seq: int = 0

    def apply(self, seq: int, e: Event) -> None:
        if seq != self.applied_seq + 1:
            raise ValueError(f"out-of-order apply: expected {self.applied_seq + 1}, got {seq}")
        self.applied_seq = seq
        if e.kind == "cancel":
            for side in (self.bids, self.asks):
                for px, q in list(side.items()):
                    side[px] = deque(o for o in q if o[0] != e.order_id)
                    if not side[px]:
                        del side[px]
            return
        qty = e.qty
        opp, own = (self.asks, self.bids) if e.side == "B" else (self.bids, self.asks)
        while qty > 0 and opp:
            best = min(opp) if e.side == "B" else max(opp)
            if (e.side == "B" and best > e.price) or (e.side == "S" and best < e.price):
                break
            maker_id, maker_qty = opp[best][0]
            q = min(qty, maker_qty)
            self.fills.append((e.order_id, maker_id, best, q))
            qty -= q
            if q == maker_qty:
                opp[best].popleft()
                if not opp[best]:
                    del opp[best]
            else:
                opp[best][0] = (maker_id, maker_qty - q)
        if qty > 0:
            own.setdefault(e.price, deque()).append((e.order_id, qty))

    def digest(self) -> str:
        canon = {
            "bids": sorted((p, list(q)) for p, q in self.bids.items()),
            "asks": sorted((p, list(q)) for p, q in self.asks.items()),
            "fills": self.fills,
            "seq": self.applied_seq,
        }
        return hashlib.sha256(json.dumps(canon, separators=(",", ":")).encode()).hexdigest()[:16]

    def snapshot(self) -> str:
        return json.dumps(
            {
                "bids": {p: list(q) for p, q in self.bids.items()},
                "asks": {p: list(q) for p, q in self.asks.items()},
                "fills": self.fills,
                "seq": self.applied_seq,
            }
        )

    @staticmethod
    def restore(blob: str) -> Book:
        d = json.loads(blob)
        b = Book()
        b.bids = {int(p): deque(tuple(o) for o in q) for p, q in d["bids"].items()}
        b.asks = {int(p): deque(tuple(o) for o in q) for p, q in d["asks"].items()}
        b.fills = [tuple(f) for f in d["fills"]]
        b.applied_seq = d["seq"]
        return b


def gateway_flow(rng: random.Random, n: int, trader: str, id_base: int) -> list[tuple[float, Event]]:
    """One gateway's inbound orders with arrival timestamps (microseconds)."""
    out, t, live = [], 0.0, []
    for i in range(n):
        t += rng.expovariate(1.0)
        if live and rng.random() < 0.3:
            out.append((t, Event("cancel", live.pop(rng.randrange(len(live))))))
        else:
            oid = id_base + i
            side = rng.choice("BS")
            px = 100 + rng.randint(-3, 3)
            out.append((t, Event("new", oid, side, px, rng.randint(1, 10), trader)))
            live.append(oid)
    return out


def sequencing() -> None:
    rng = random.Random(11)
    flows = [gateway_flow(rng, 4000, "A", 1_000_000), gateway_flow(rng, 4000, "B", 2_000_000)]

    # The sequencer merges gateways by arrival time and stamps a gap-free sequence number.
    journal = [(seq, e) for seq, (_, e) in enumerate(sorted(flows[0] + flows[1], key=lambda x: x[0]), start=1)]
    print(f"2a. sequencer journal: {len(journal)} events")

    primary, replica = Book(), Book()
    for seq, e in journal:
        primary.apply(seq, e)
    for seq, e in journal:
        replica.apply(seq, e)
    print(f"   primary digest {primary.digest()}, replica digest {replica.digest()}, fills {len(primary.fills)}")
    assert primary.digest() == replica.digest()
    assert len(journal) == 8000 and len(primary.fills) == 4182

    print("2b. recovery from a snapshot plus the journal tail")
    cut = 5000
    partial = Book()
    for seq, e in journal[:cut]:
        partial.apply(seq, e)
    blob = partial.snapshot()
    recovered = Book.restore(blob)
    for seq, e in journal[cut:]:
        recovered.apply(seq, e)
    print(f"   snapshot at seq {cut} ({len(blob):,} bytes), replay {len(journal) - cut} events -> digest {recovered.digest()}")
    assert recovered.digest() == primary.digest() and len(blob) == 76_988

    print("2c. gap detection and retransmission")
    received = [m for m in journal if m[0] not in (1234, 1235, 6000)]  # three packets lost on the wire
    consumer, expected, gaps, retransmitted = Book(), 1, [], 0
    for seq, e in received:
        if seq > expected:
            gaps.append((expected, seq - 1))
            for rseq, re_ in journal[expected - 1 : seq - 1]:  # request the range from the journal
                consumer.apply(rseq, re_)
                retransmitted += 1
        consumer.apply(seq, e)
        expected = seq + 1
    print(f"   gaps {gaps}, retransmitted {retransmitted}, digest {consumer.digest()}")
    assert gaps == [(1234, 1235), (6000, 6000)] and retransmitted == 3
    assert consumer.digest() == primary.digest()

    print("2d. no sequencer: each replica applies events in its own arrival order")
    # The last 100 shares on offer; two buyers' orders reach two replicas in opposite orders.
    offer = Event("new", 1, "S", 100, 100, "MM")
    buy_a = Event("new", 2, "B", 100, 100, "A")
    buy_b = Event("new", 3, "B", 100, 100, "B")
    r1, r2 = Book(), Book()
    for i, e in enumerate([offer, buy_a, buy_b], start=1):
        r1.apply(i, e)
    for i, e in enumerate([offer, buy_b, buy_a], start=1):
        r2.apply(i, e)
    print(f"   replica 1 filled order {r1.fills[0][0]}, replica 2 filled order {r2.fills[0][0]}")
    print(f"   digests differ: {r1.digest() != r2.digest()}")
    assert r1.fills[0][0] == 2 and r2.fills[0][0] == 3 and r1.digest() != r2.digest()

    try:
        Book().apply(2, offer)
    except ValueError as exc:
        print(f"   applying out of order is refused: {exc}")
    else:
        raise AssertionError("out-of-order apply must fail")


def main() -> None:
    capacity()
    sequencing()
    print("all assertions passed")


if __name__ == "__main__":
    main()
