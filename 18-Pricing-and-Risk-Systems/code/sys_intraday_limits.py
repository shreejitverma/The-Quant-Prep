"""Intraday risk and pre-trade limits: latency budget, credit reservation ledger, collars, ring buffer and OTR.

Backs every number in `18-Pricing-and-Risk-Systems/08-Intraday-Risk-and-Pre-Trade-Limits.md`.
Latency budgets, limits, orders and buffer sizes are labelled-hypothetical design inputs, not measurements of any
product; Knight Capital figures are quoted from SEC Release No. 34-70694 (October 16, 2013); the order-to-trade
ratio formula is Article 3 of Commission Delegated Regulation (EU) 2017/566.
The credit example is not arithmetic on literals: a small reservation ledger processes the order and execution
events and the asserted balances are whatever it ends in; a seeded random replay of reserve, fill, cancel and release
events then checks its available balance after every event against a naive model that recomputes it from the order
history, including the rejection of every reservation that would exceed the limit.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_intraday_limits.py`.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Latency budget and per-core capacity (hypothetical design budget)
# ============================================================================

# stage: (microseconds, runs on the gateway core)
BUDGET_US = {
    "NIC to user space (kernel bypass)": (3.5, False),
    "decode order message": (1.2, True),
    "price collar and size checks": (0.4, True),
    "credit reservation": (1.8, True),
    "position and short-sale checks": (1.1, True),
    "audit record to ring buffer": (0.8, True),
    "encode and send to venue": (4.2, False),
}


def check_latency_budget() -> None:
    print("  1. Hypothetical latency budget of an in-line gateway (microseconds)")
    total = sum(us for us, _ in BUDGET_US.values())
    on_core = sum(us for us, core in BUDGET_US.values() if core)
    quoted("total wire-to-wire budget (us)", total, 13.0, 1)
    quoted("gateway-core service time per order (us)", on_core, 5.3, 1)
    rate = 100_000  # orders per second arriving at one gateway, hypothetical
    quoted("utilisation of one core at 100,000 orders/s", rate * on_core * 1e-6, 0.53, 2)
    quoted("orders/s one core can serve at 100% utilisation", 1e6 / on_core, 188_679, 0)
    # a queue that is 53% busy still makes some orders wait: M/D/1 mean wait = rho * s / (2 (1 - rho))
    rho = rate * on_core * 1e-6
    quoted("M/D/1 mean queueing delay at that load (us)", rho * on_core / (2 * (1 - rho)), 2.99, 2)


# ============================================================================
# 2. Credit reservation ledger
# ============================================================================


@dataclass
class CreditLedger:
    """Running balances: available is the limit less committed and reserved; amounts in dollars."""

    limit: float
    committed: float
    reserved: dict[str, float] = field(default_factory=dict)

    @property
    def available(self) -> float:
        return self.limit - self.committed - sum(self.reserved.values())

    def check(self) -> None:
        """Internal sanity check: conservation holds by construction, so only a negative available can trip it."""
        total = self.available + sum(self.reserved.values()) + self.committed
        assert abs(total - self.limit) < 1e-6 and self.available >= -1e-6

    def new_order(self, order_id: str, qty: int, limit_px: float) -> bool:
        need = qty * limit_px  # reserve at the worst price the order can trade at
        if need > self.available:
            return False
        self.reserved[order_id] = need
        self.check()
        return True

    def fill(self, order_id: str, qty: int, px: float, limit_px: float) -> None:
        """A fill commits qty * px and releases qty * limit_px of the reservation."""
        self.reserved[order_id] -= qty * limit_px
        self.committed += qty * px
        assert self.reserved[order_id] >= -1e-6
        self.check()

    def terminal(self, order_id: str) -> None:
        """Canceled, Rejected or Expired: release whatever is still reserved."""
        self.reserved.pop(order_id)
        self.check()


def check_credit_reservation() -> None:
    print("  2. Credit reservation ledger (hypothetical prime-broker limit)")
    book = CreditLedger(limit=50_000_000.0, committed=44_000_000.0)
    quoted("available at the start ($)", book.available, 6_000_000, 0)
    ok1 = book.new_order("O1", 100_000, 200.0)
    assert not ok1
    quoted("order 1 notional at its limit price ($)", 100_000 * 200.0, 20_000_000, 0)
    ok2 = book.new_order("O2", 20_000, 200.0)
    assert ok2
    quoted("available after reserving order 2 ($)", book.available, 2_000_000, 0)
    ok3 = book.new_order("O3", 15_000, 200.0)
    assert not ok3, "order 3 must be rejected while order 2's reservation is held"
    quoted("order 3 notional ($)", 15_000 * 200.0, 3_000_000, 0)
    # outcome A: 15,000 shares fill at the limit, the venue cancels the rest
    book.fill("O2", 15_000, 200.0, 200.0)
    quoted("still reserved for order 2 after the fill ($)", book.reserved["O2"], 1_000_000, 0)
    book.terminal("O2")
    quoted("committed after fill and cancel ($)", book.committed, 47_000_000, 0)
    quoted("available after fill and cancel ($)", book.available, 3_000_000, 0)
    # outcome B (fresh ledger): the order is filled at a better price than its limit
    alt = CreditLedger(limit=50_000_000.0, committed=44_000_000.0)
    alt.new_order("O2", 20_000, 200.0)
    alt.fill("O2", 20_000, 199.50, 200.0)
    alt.terminal("O2")
    quoted("committed when all 20,000 fill at 199.50 ($)", alt.committed, 47_990_000, 0)
    quoted("price improvement returned to available ($)", alt.available - 2_000_000.0, 10_000, 0)
    # outcome C (fresh ledger): status unknown after a disconnect, nothing is released
    unk = CreditLedger(limit=50_000_000.0, committed=44_000_000.0)
    unk.new_order("O2", 20_000, 200.0)
    quoted("available while order 2's status is unknown ($)", unk.available, 2_000_000, 0)
    check_ledger_replay()


@dataclass
class NaiveCreditModel:
    """Keeps only the event history and recomputes available from scratch on every query."""

    limit: float
    committed_at_open: float
    orders: dict[str, tuple[int, float]] = field(default_factory=dict)  # accepted order id -> (qty, limit price)
    fills: list[tuple[str, int, float]] = field(default_factory=list)  # (order id, qty, price)
    closed: set[str] = field(default_factory=set)

    def filled_qty(self, order_id: str) -> int:
        return sum(q for oid, q, _ in self.fills if oid == order_id)

    def working(self) -> list[str]:
        return [oid for oid in self.orders if oid not in self.closed]

    def available(self) -> float:
        committed = self.committed_at_open + sum(q * px for _, q, px in self.fills)
        held = sum((self.orders[oid][0] - self.filled_qty(oid)) * self.orders[oid][1] for oid in self.working())
        return self.limit - committed - held


def check_ledger_replay(steps: int = 600, seed: int = 15) -> None:
    """Replay random reserve, fill, cancel and release events through the ledger and the naive model."""
    rng = random.Random(seed)
    book = CreditLedger(limit=50_000_000.0, committed=44_000_000.0)
    model = NaiveCreditModel(limit=50_000_000.0, committed_at_open=44_000_000.0)
    counts = dict.fromkeys(("accepted", "rejected", "fill", "release", "cancel"), 0)
    for step in range(steps):
        working = model.working()
        action = rng.choice(("new", "new", "fill", "fill", "cancel")) if working else "new"
        if action == "new":
            oid, qty, limit_px = f"N{step}", rng.randrange(100, 10_100, 100), rng.choice((25.0, 80.0, 200.0))
            accepted = book.new_order(oid, qty, limit_px)
            assert accepted == (qty * limit_px <= model.available()), f"{oid}: ledger and model disagree on acceptance"
            if accepted:
                model.orders[oid] = (qty, limit_px)
            counts["accepted" if accepted else "rejected"] += 1
        elif action == "fill":
            oid = rng.choice(working)
            qty, limit_px = model.orders[oid]
            fill_qty = rng.randint(1, qty - model.filled_qty(oid))
            px = limit_px - rng.choice((0.0, 0.01, 0.05, 0.25))
            book.fill(oid, fill_qty, px, limit_px)
            model.fills.append((oid, fill_qty, px))
            counts["fill"] += 1
            if model.filled_qty(oid) == qty:
                book.terminal(oid)
                model.closed.add(oid)
                counts["release"] += 1
        else:
            oid = rng.choice(working)
            book.terminal(oid)
            model.closed.add(oid)
            counts["cancel"] += 1
        assert abs(book.available - model.available()) < 1e-4, f"step {step}: available drifted from the model"
        assert set(book.reserved) == set(model.working()), f"step {step}: working orders differ"
    assert all(counts.values()), f"replay must exercise every event type: {counts}"
    print(f"    ledger replay: {steps} events matched the naive model ({counts['rejected']} rejections)")


# ============================================================================
# 3. Price collar, Knight Capital, ring buffer, order-to-trade ratio
# ============================================================================


def collar_ok(side: str, px: float, bid: float, ask: float, band: float) -> bool:
    return px <= ask * (1 + band) if side == "buy" else px >= bid * (1 - band)


def check_collar() -> None:
    print("  3. Price collar around the NBBO (hypothetical 3% band)")
    bid, ask, band = 100.00, 100.05, 0.03
    upper, lower = ask * (1 + band), bid * (1 - band)
    quoted("highest buy price accepted ($)", upper, 103.0515, 4)
    quoted("lowest sell price accepted ($)", lower, 97.00, 2)
    assert collar_ok("buy", 103.05, bid, ask, band) and not collar_ok("buy", 103.06, bid, ask, band)
    assert collar_ok("sell", 97.00, bid, ask, band) and not collar_ok("sell", 96.99, bid, ask, band)


def check_knight() -> None:
    print("  4. Knight Capital, August 1, 2012 (figures from SEC Release No. 34-70694)")
    executions, minutes = 4_000_000, 45  # "4 million executions ... in approximately 45 minutes"
    quoted("average executions per second over 45 minutes", executions / (minutes * 60), 1_481.5, 1)
    long_bn, short_bn = 3.5, 3.15
    quoted("gross unintended position ($bn)", long_bn + short_bn, 6.65, 2)


def check_ring_and_otr() -> None:
    print("  5. Ring buffer sizing and order-to-trade ratio")
    slots, slot_bytes = 2**20, 64
    quoted("ring buffer slots", slots, 1_048_576, 0)
    quoted("ring buffer size (MiB)", slots * slot_bytes / 2**20, 64.0, 1)
    mask = slots - 1
    assert all((seq & mask) == (seq % slots) for seq in (0, 1, slots - 1, slots, 3 * slots + 17))
    # RTS 9 Article 3: (total number of orders / total number of transactions) - 1, orders include
    # every submission, modification and cancellation; a transaction is a totally or partially executed order
    new, modify, cancel, trades = 10_000, 9_000, 6_000, 500
    orders = new + modify + cancel
    quoted("order messages counted", orders, 25_000, 0)
    quoted("OTR by number", orders / trades - 1, 49.0, 1)
    vol_orders, vol_trades = 4_000_000, 250_000
    quoted("OTR by volume", vol_orders / vol_trades - 1, 15.0, 1)


def main() -> None:
    print("Intraday risk and pre-trade limits checks")
    check_latency_budget()
    check_credit_reservation()
    check_collar()
    check_knight()
    check_ring_and_otr()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All intraday limits checks passed.")


if __name__ == "__main__":
    main()
