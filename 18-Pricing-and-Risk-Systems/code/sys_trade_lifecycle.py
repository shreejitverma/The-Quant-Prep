"""Trade representation and lifecycle: bitemporal storage, event-sourced lifecycle primitives, compression and sizing.

Backs every number in `18-Pricing-and-Risk-Systems/02-Trade-Representation-and-Lifecycle.md`.

1. A bitemporal trade table in SQLite (standard library) that runs the note's SQL as-of queries verbatim.
2. Lifecycle events built from primitives modelled on the ISDA CDM event model (execution, quantity change,
   party change, split, terms change), with conservation invariants checked for allocation and novation.
3. Multilateral compression of a cycle of offsetting trades: gross notional falls, every participant's net is unchanged.
4. A rule-based schedule generator with the Modified Following convention on a weekends-only calendar.
5. Event-store storage sizing from labelled-hypothetical inputs.

Trade terms, volumes and sizes are hypothetical teaching inputs.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_trade_lifecycle.py`.
"""

from __future__ import annotations

import datetime as dt
import sqlite3
from dataclasses import dataclass, replace

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:.{decimals}f}")
    return value


# ============================================================================
# 1. Bitemporal table
# ============================================================================

END_OF_TIME = "9999-12-31 23:59:59"

SCHEMA = """
CREATE TABLE trades (
    trade_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    notional REAL NOT NULL,
    valid_from TEXT NOT NULL,
    valid_to TEXT NOT NULL,
    tx_from TEXT NOT NULL,
    tx_to TEXT NOT NULL,
    PRIMARY KEY (trade_id, version)
)
"""

# The two queries exactly as printed in the note.
QUERY_A = """
SELECT notional FROM trades
WHERE trade_id = 'SWAP-9901'
  AND valid_from <= '2026-09-30 23:59:59' AND valid_to > '2026-09-30 23:59:59'
  AND tx_from <= '2026-10-01 00:00:00' AND tx_to > '2026-10-01 00:00:00';
"""
QUERY_B = """
SELECT notional FROM trades
WHERE trade_id = 'SWAP-9901'
  AND valid_from <= '2026-09-30 23:59:59' AND valid_to > '2026-09-30 23:59:59'
  AND tx_to = '9999-12-31 23:59:59';
"""
AS_OF = """
SELECT notional FROM trades
WHERE trade_id = ? AND valid_from <= ? AND valid_to > ? AND tx_from <= ? AND tx_to > ?
"""


class BitemporalStore:
    """Append-only bitemporal table: a correction closes the transaction-time interval of the rows it supersedes."""

    def __init__(self) -> None:
        self.db = sqlite3.connect(":memory:")
        self.db.execute(SCHEMA)

    def _next_version(self, trade_id: str) -> int:
        (v,) = self.db.execute("SELECT COALESCE(MAX(version), 0) FROM trades WHERE trade_id = ?", (trade_id,)).fetchone()
        return v + 1

    def book(self, trade_id: str, notional: float, valid_from: str, valid_to: str, recorded: str) -> None:
        self.db.execute(
            "INSERT INTO trades VALUES (?, ?, ?, ?, ?, ?, ?)",
            (trade_id, self._next_version(trade_id), notional, valid_from, valid_to, recorded, END_OF_TIME),
        )

    def change(self, trade_id: str, notional: float, effective: str, recorded: str) -> None:
        """Set the notional from `effective` onwards, as known from `recorded`.

        Every current row whose valid interval reaches past `effective` is closed in transaction time; the part
        before `effective` (if any) is re-asserted unchanged and the part from `effective` gets the new notional.
        Nothing is ever deleted or updated except the tx_to of superseded rows.
        """
        rows = self.db.execute(
            "SELECT version, notional, valid_from, valid_to FROM trades WHERE trade_id = ? AND tx_to = ? AND valid_to > ?",
            (trade_id, END_OF_TIME, effective),
        ).fetchall()
        assert rows, "nothing to change"
        for version, old_notional, vf, vt in rows:
            self.db.execute("UPDATE trades SET tx_to = ? WHERE trade_id = ? AND version = ?", (recorded, trade_id, version))
            if vf < effective:
                self.book(trade_id, old_notional, vf, effective, recorded)
            self.book(trade_id, notional, max(vf, effective), vt, recorded)

    def as_of(self, trade_id: str, valid_t: str, tx_t: str) -> float | None:
        r = self.db.execute(AS_OF, (trade_id, valid_t, valid_t, tx_t, tx_t)).fetchall()
        assert len(r) <= 1, "overlapping bitemporal rows"
        return r[0][0] if r else None

    def count(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM trades").fetchone()[0]

    def overlaps(self) -> int:
        """Pairs of rows of one trade that overlap in both valid and transaction time (must be zero)."""
        q = """
        SELECT COUNT(*) FROM trades a JOIN trades b
          ON a.trade_id = b.trade_id AND a.version < b.version
         AND a.valid_from < b.valid_to AND b.valid_from < a.valid_to
         AND a.tx_from < b.tx_to AND b.tx_from < a.tx_to
        """
        return self.db.execute(q).fetchone()[0]


def bitemporal_examples() -> dict[str, float]:
    s = BitemporalStore()
    s.book("SWAP-9901", 100e6, "2026-09-30 00:00:00", "2031-09-30 00:00:00", "2026-09-28 14:00:00")
    s.change("SWAP-9901", 85e6, "2026-09-30 00:00:00", "2026-10-05 09:30:00")  # retroactive correction
    out = {
        "rows_after_correction": s.count(),
        "query_a": s.db.execute(QUERY_A).fetchone()[0],
        "query_b": s.db.execute(QUERY_B).fetchone()[0],
    }
    # A forward-effective partial termination: 85m to 60m from 2027-03-31, recorded on 2026-11-02.
    s.change("SWAP-9901", 60e6, "2027-03-31 00:00:00", "2026-11-02 10:00:00")
    out["rows_after_partial_termination"] = s.count()
    out["overlaps"] = s.overlaps()
    grid = {}
    for v in ("2026-12-31 00:00:00", "2027-06-30 00:00:00"):
        for t in ("2026-10-01 00:00:00", "2026-10-20 00:00:00", "2026-11-30 00:00:00"):
            grid[(v, t)] = s.as_of("SWAP-9901", v, t)
    out["grid"] = grid  # type: ignore[assignment]
    return out


# ============================================================================
# 2. Lifecycle primitives (modelled on the CDM event model)
# ============================================================================


@dataclass(frozen=True)
class TradeState:
    trade_id: str
    counterparty: str
    quantity: float  # notional
    fixed_rate: float
    status: str = "Live"


@dataclass(frozen=True)
class BusinessEvent:
    intent: str
    before: tuple[TradeState, ...]
    after: tuple[TradeState, ...]


def execution(trade_id: str, cpty: str, notional: float, rate: float) -> BusinessEvent:
    return BusinessEvent("Execution", (), (TradeState(trade_id, cpty, notional, rate),))


def split(t: TradeState, parts: list[tuple[str, float]]) -> tuple[TradeState, ...]:
    """Split one trade into several with new ids; quantities must be positive and sum to the original."""
    assert all(q > 0 for _, q in parts)
    assert abs(sum(q for _, q in parts) - t.quantity) < 1e-6
    return tuple(replace(t, trade_id=i, quantity=q) for i, q in parts)


def party_change(t: TradeState, new_cpty: str, new_id: str) -> TradeState:
    return replace(t, trade_id=new_id, counterparty=new_cpty)


def quantity_change(t: TradeState, new_quantity: float) -> TradeState:
    assert new_quantity >= 0
    return replace(t, quantity=new_quantity, status="Terminated" if new_quantity == 0 else t.status)


def allocation(block: TradeState, funds: list[tuple[str, float]]) -> BusinessEvent:
    """Block trade with an asset manager split into child trades facing each fund (split then party change)."""
    pieces = split(block, [(f"{block.trade_id}-{i + 1}", q) for i, (_, q) in enumerate(funds)])
    after = tuple(party_change(p, f, p.trade_id) for p, (f, _) in zip(pieces, funds, strict=True))
    closed = replace(block, status="Allocated")
    return BusinessEvent("Allocation", (block,), (closed, *after))


def partial_novation(t: TradeState, transferee: str, novated: float, new_id: str) -> BusinessEvent:
    """Transfer `novated` of the notional to a new counterparty; the remainder stays with the original."""
    remain, moved = split(t, [(t.trade_id, t.quantity - novated), (new_id, novated)])
    return BusinessEvent("Novation", (t,), (remain, party_change(moved, transferee, new_id)))


def gross_and_net(trades: tuple[TradeState, ...], me: str) -> tuple[float, float]:
    """Gross live notional and net receive-fixed notional; positive quantity here means I receive fixed."""
    live = [t for t in trades if t.status == "Live"]
    return sum(t.quantity for t in live), sum(t.quantity for t in live if t.counterparty != me)


# ============================================================================
# 3. Multilateral compression of a cycle
# ============================================================================


def compress_cycle(edges: dict[tuple[str, str], float]) -> dict[tuple[str, str], float]:
    """Remove the smallest edge along a directed cycle of fungible trades (payer -> receiver of fixed).

    Each participant's net (received minus paid notional) is unchanged; gross falls by cycle length times the minimum.
    """
    cut = min(edges.values())
    return {k: v - cut for k, v in edges.items() if v - cut > 1e-9}


def nets(edges: dict[tuple[str, str], float]) -> dict[str, float]:
    out: dict[str, float] = {}
    for (payer, receiver), n in edges.items():
        out[payer] = out.get(payer, 0.0) - n
        out[receiver] = out.get(receiver, 0.0) + n
    return out


# ============================================================================
# 4. Rule-based schedule generation (Modified Following, weekends-only calendar)
# ============================================================================


def is_business_day(d: dt.date) -> bool:
    return d.weekday() < 5  # hypothetical calendar: weekends only, no holidays


def modified_following(d: dt.date) -> dt.date:
    """Roll forward to a business day unless that crosses into the next month, in which case roll backward."""
    f = d
    while not is_business_day(f):
        f += dt.timedelta(days=1)
    if f.month == d.month:
        return f
    p = d
    while not is_business_day(p):
        p -= dt.timedelta(days=1)
    return p


def add_months(d: dt.date, months: int) -> dt.date:
    y, m = divmod(d.month - 1 + months, 12)
    year, month = d.year + y, m + 1
    last = (dt.date(year + (month == 12), month % 12 + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(year, month, min(d.day, last))


def schedule(effective: dt.date, termination: dt.date, months: int) -> list[tuple[dt.date, dt.date]]:
    """Unadjusted and adjusted dates, generated backward from termination (any stub is at the front)."""
    unadj = [termination]
    k = 1
    while True:
        d = add_months(termination, -months * k)
        if d <= effective:
            break
        unadj.append(d)
        k += 1
    unadj.append(effective)
    unadj.reverse()
    return [(d, modified_following(d)) for d in unadj]


# ============================================================================
# 5. Event-store sizing (hypothetical inputs)
# ============================================================================


@dataclass(frozen=True)
class StoreInputs:
    new_trades_per_day: float = 40_000
    business_days: int = 252
    booking_events_per_new_trade: float = 3  # execution, confirmation, clearing or allocation
    open_trades: float = 1_200_000
    fixings_per_open_trade_per_year: float = 4  # quarterly resets on the floating leg
    other_events_per_open_trade_per_year: float = 0.5  # amendments, partial terminations, novations
    document_bytes: float = 8_000  # compressed full trade state document per event
    column_bytes: float = 2_500  # normalised columns for querying
    index_bytes: float = 1_200  # interval and key indexes
    copies: int = 3  # replicas and backups
    years: int = 10


def store_sizing(s: StoreInputs) -> dict[str, float]:
    booking = s.new_trades_per_day * s.business_days * s.booking_events_per_new_trade
    lifecycle = s.open_trades * (s.fixings_per_open_trade_per_year + s.other_events_per_open_trade_per_year)
    per_year = booking + lifecycle
    total_events = per_year * s.years
    bytes_per_event = s.document_bytes + s.column_bytes + s.index_bytes
    raw = total_events * bytes_per_event
    return {
        "booking_events_per_year": booking,
        "lifecycle_events_per_year": lifecycle,
        "events_per_year": per_year,
        "events_10y": total_events,
        "bytes_per_event": bytes_per_event,
        "raw_TB": raw / 1e12,
        "raw_TiB": raw / 2**40,
        "provisioned_TB": raw * s.copies / 1e12,
    }


def uti_ok(uti: str) -> bool:
    """CPMI-IOSCO UTI shape: 20-character LEI of the generating entity, then a value, at most 52 characters in total,
    upper-case letters and digits only."""
    return 20 < len(uti) <= 52 and uti.isascii() and uti.isalnum() and uti == uti.upper()


def run_tests() -> None:
    print("Trade representation and lifecycle checks")

    print("  Example 1: bitemporal correction and the note's SQL")
    b = bitemporal_examples()
    quoted("rows after the retroactive correction", b["rows_after_correction"], 2, 0)
    quoted("Query A notional, as known on 1 October (USD m)", b["query_a"] / 1e6, 100, 0)
    quoted("Query B notional, current knowledge (USD m)", b["query_b"] / 1e6, 85, 0)
    quoted("rows after the forward-effective partial termination", b["rows_after_partial_termination"], 4, 0)
    quoted("bitemporal overlaps", b["overlaps"], 0, 0)
    g = b["grid"]
    expected = {
        ("2026-12-31 00:00:00", "2026-10-01 00:00:00"): 100,
        ("2026-12-31 00:00:00", "2026-10-20 00:00:00"): 85,
        ("2026-12-31 00:00:00", "2026-11-30 00:00:00"): 85,
        ("2027-06-30 00:00:00", "2026-10-01 00:00:00"): 100,
        ("2027-06-30 00:00:00", "2026-10-20 00:00:00"): 85,
        ("2027-06-30 00:00:00", "2026-11-30 00:00:00"): 60,
    }
    for (v, t), e in expected.items():
        quoted(f"notional valid {v[:10]} known {t[:10]} (USD m)", g[(v, t)] / 1e6, e, 0)

    print("  Example 2: allocation and partial novation (CDM-style primitives)")
    block = execution("BLK-1", "AssetMgr", 100e6, 0.0375).after[0]
    alloc = allocation(block, [("Fund A", 50e6), ("Fund B", 30e6), ("Fund C", 20e6)])
    children = [t for t in alloc.after if t.status == "Live"]
    quoted("child trades after allocation", len(children), 3, 0)
    quoted("allocated notional (USD m)", sum(t.quantity for t in children) / 1e6, 100, 0)
    assert all(t.fixed_rate == block.fixed_rate for t in children)
    t0 = TradeState("TR-001", "Bank B", 50e6, 0.04)
    nov = partial_novation(t0, "Bank C", 20e6, "TR-002")
    remain, moved = nov.after
    quoted("notional remaining with Bank B (USD m)", remain.quantity / 1e6, 30, 0)
    quoted("notional novated to Bank C (USD m)", moved.quantity / 1e6, 20, 0)
    assert remain.trade_id == "TR-001" and moved.counterparty == "Bank C"
    assert abs(remain.quantity + moved.quantity - t0.quantity) < 1e-6
    full = quantity_change(t0, 0.0)
    assert full.status == "Terminated"

    print("  Example 3: multilateral compression of a cycle (USD m, same maturity and rate)")
    edges = {("A", "B"): 100.0, ("B", "C"): 100.0, ("C", "A"): 80.0}
    after = compress_cycle(edges)
    quoted("gross notional before", sum(edges.values()), 280, 0)
    quoted("gross notional after", sum(after.values()), 40, 0)
    quoted("gross reduction (%)", 100 * (1 - sum(after.values()) / sum(edges.values())), 85.7, 1)
    quoted("trades after", len(after), 2, 0)
    nb, na = nets(edges), nets(after)
    for k in nb:
        assert abs(nb[k] - na.get(k, 0.0)) < 1e-9
    quoted("net of A before and after", na["A"], -20, 0)
    quoted("net of C before and after", na["C"], 20, 0)

    print("  Example 4: schedule generation, 5y semiannual from 2026-10-15, Modified Following, weekends only")
    sch = schedule(dt.date(2026, 10, 15), dt.date(2031, 10, 15), 6)
    quoted("schedule dates incl. effective and termination", len(sch), 11, 0)
    adjusted = [(u, a) for u, a in sch if u != a]
    for u, a in adjusted:
        print(f"    rolled {u.isoformat()} ({u.strftime('%a')}) -> {a.isoformat()}")
    quoted("dates that fall on a weekend and roll", len(adjusted), 3, 0)
    assert [u.isoformat() for u, _ in adjusted] == ["2028-04-15", "2028-10-15", "2029-04-15"]
    assert [a.isoformat() for _, a in adjusted] == ["2028-04-17", "2028-10-16", "2029-04-16"]
    # Month-end case: Saturday 31 May 2031 cannot roll forward into June, so it rolls back to Friday 30 May.
    quoted("Modified Following of Sat 2031-05-31 (day of month)", modified_following(dt.date(2031, 5, 31)).day, 30, 0)
    assert modified_following(dt.date(2031, 5, 31)) == dt.date(2031, 5, 30)
    stub = schedule(dt.date(2026, 10, 15), dt.date(2031, 12, 15), 6)
    quoted("front stub length in months for a 5y2m semiannual swap", (stub[1][0].month - stub[0][0].month) % 12, 2, 0)
    long_leg = schedule(dt.date(2026, 10, 15), dt.date(2056, 10, 15), 3)
    quoted("reset events on a 30y quarterly floating leg (event sourcing section)", len(long_leg) - 1, 120, 0)

    print("  Example 5: event-store sizing (hypothetical inputs)")
    z = store_sizing(StoreInputs())
    quoted("booking events per year (m)", z["booking_events_per_year"] / 1e6, 30.24, 2)
    quoted("lifecycle events on open trades per year (m)", z["lifecycle_events_per_year"] / 1e6, 5.4, 1)
    quoted("events per year (m)", z["events_per_year"] / 1e6, 35.64, 2)
    quoted("events over 10 years (m)", z["events_10y"] / 1e6, 356.4, 1)
    quoted("bytes per event", z["bytes_per_event"], 11_700, 0)
    quoted("raw storage over 10 years (TB, decimal)", z["raw_TB"], 4.17, 2)
    quoted("raw storage over 10 years (TiB)", z["raw_TiB"], 3.79, 2)
    quoted("provisioned with 3 copies (TB)", z["provisioned_TB"], 12.51, 2)
    quoted("TiB figure smaller than the TB figure (%)", (1 - z["raw_TiB"] / z["raw_TB"]) * 100, 9.05, 2)

    print("  UTI shape")
    lei = "506700GE1G29325QX363"  # LEI of the Global Legal Entity Identifier Foundation, used as the generating entity
    assert uti_ok(lei + "SWAP20261015000001")
    assert not uti_ok(lei + "X" * 33)  # 53 characters
    assert not uti_ok(lei + "swap-1")

    print(f"  {len(QUOTED)} numbers quoted in note 02 computed, printed and asserted")
    print("All trade representation and lifecycle checks passed.")


if __name__ == "__main__":
    run_tests()
