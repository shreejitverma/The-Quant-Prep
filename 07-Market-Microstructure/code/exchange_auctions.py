"""Exchange mechanics: call-auction uncross, maker-taker and inverted fee economics, ticks and halts.

Backs every number in 02-Exchange-Mechanics-Auctions-and-Fees.md.
Run ``python exchange_auctions.py``: each result is printed and asserted.
Fee levels below are hypothetical illustrations chosen inside the Rule 610(c) caps, not any venue's schedule.
"""

from __future__ import annotations

from dataclasses import dataclass

MKT = None  # limit price of a market (at-the-open or at-the-close) order


def check(label: str, value: float, expected: float, tol: float = 1e-9) -> float:
    """Print a labelled result and assert it matches the expected value."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


@dataclass(frozen=True)
class Order:
    oid: str
    side: str  # "B" or "S"
    qty: int
    limit: float | None  # None means market order
    seq: int  # arrival sequence number, lower is earlier


def demand(orders: list[Order], p: float) -> int:
    """Shares willing to buy at price p: market buys plus buy limits at or above p."""
    return sum(o.qty for o in orders if o.side == "B" and (o.limit is MKT or o.limit >= p - 1e-12))


def supply(orders: list[Order], p: float) -> int:
    """Shares willing to sell at price p: market sells plus sell limits at or below p."""
    return sum(o.qty for o in orders if o.side == "S" and (o.limit is MKT or o.limit <= p + 1e-12))


def uncross(orders: list[Order], reference: float) -> tuple[float, int, int, list[tuple[float, int, int, int, int]]]:
    """Single-price call auction.

    Candidate prices are the distinct limit prices.  The clearing price maximises executable volume,
    then minimises the absolute imbalance, then is closest to the reference price, then is the lower price.
    Returns (price, executed shares, signed imbalance at that price, full table).
    """
    prices = sorted({o.limit for o in orders if o.limit is not MKT})
    table = []
    for p in prices:
        d, s = demand(orders, p), supply(orders, p)
        table.append((p, d, s, min(d, s), d - s))
    best = min(table, key=lambda r: (-r[3], abs(r[4]), abs(r[0] - reference), r[0]))
    return best[0], best[3], best[4], table


def allocate(orders: list[Order], price: float, executed: int) -> dict[str, int]:
    """Fill each side up to `executed` shares by price priority (market first), then time priority."""
    fills: dict[str, int] = {}
    for side in ("B", "S"):
        if side == "B":
            eligible = [o for o in orders if o.side == "B" and (o.limit is MKT or o.limit >= price - 1e-12)]
        else:
            eligible = [o for o in orders if o.side == "S" and (o.limit is MKT or o.limit <= price + 1e-12)]
        if side == "B":
            eligible.sort(key=lambda o: (0 if o.limit is MKT else 1, -(o.limit or 0.0), o.seq))
        else:
            eligible.sort(key=lambda o: (0 if o.limit is MKT else 1, o.limit or 0.0, o.seq))
        left = executed
        for o in eligible:
            take = min(left, o.qty)
            fills[o.oid] = take
            left -= take
        assert left == 0, "allocation must exhaust the executed quantity on each side"
    return fills


def auction_example() -> None:
    print("== Opening auction uncross ==")
    orders = [
        Order("B-mkt", "B", 1_000, MKT, 1),
        Order("B1", "B", 800, 20.05, 2),
        Order("B2", "B", 1_200, 20.03, 3),
        Order("B3", "B", 1_500, 20.02, 4),
        Order("B4", "B", 2_000, 20.00, 5),
        Order("S-mkt", "S", 800, MKT, 6),
        Order("S1", "S", 700, 19.98, 7),
        Order("S2", "S", 1_000, 20.00, 8),
        Order("S3", "S", 1_200, 20.02, 9),
        Order("S4", "S", 1_500, 20.04, 10),
        Order("S5", "S", 2_000, 20.06, 11),
        Order("B5", "B", 500, 20.02, 12),
    ]
    price, executed, imbalance, table = uncross(orders, reference=20.01)
    print(" price  demand  supply  executable  imbalance")
    for p, d, s, e, imb in table:
        print(f"{p:6.2f} {d:7d} {s:7d} {e:11d} {imb:10d}")
    expected_table = [
        (19.98, 7_000, 1_500, 1_500, 5_500),
        (20.00, 7_000, 2_500, 2_500, 4_500),
        (20.02, 5_000, 3_700, 3_700, 1_300),
        (20.03, 3_000, 3_700, 3_000, -700),
        (20.04, 1_800, 5_200, 1_800, -3_400),
        (20.05, 1_800, 5_200, 1_800, -3_400),
        (20.06, 1_000, 7_200, 1_000, -6_200),
    ]
    for got, want in zip(table, expected_table, strict=True):
        assert abs(got[0] - want[0]) < 1e-9 and got[1:] == want[1:], (got, want)
    check("clearing price", price, 20.02)
    check("executed shares", executed, 3_700)
    check("buy imbalance at clearing price", imbalance, 1_300)
    fills = allocate(orders, price, executed)
    print("fills:", fills)
    want_fills = {"B-mkt": 1_000, "B1": 800, "B2": 1_200, "B3": 700, "B5": 0, "S-mkt": 800, "S1": 700, "S2": 1_000, "S3": 1_200}
    assert fills == want_fills, fills
    check("B3 fill (first at the clearing price)", fills["B3"], 700)
    check("B5 fill (later at the clearing price)", fills["B5"], 0)
    check("S3 fill", fills["S3"], 1_200)
    # Volume table rows used in the note
    rows = {round(p, 2): (d, s, e, imb) for p, d, s, e, imb in table}
    check("executable at 20.00", rows[20.00][2], 2_500)
    check("executable at 20.03", rows[20.03][2], 3_000)
    # A late 1,300-share sell limit at 20.02 absorbs the imbalance; volume rises, price unchanged
    late = [*orders, Order("S6", "S", 1_300, 20.02, 13)]
    p2, e2, i2, _ = uncross(late, reference=20.01)
    check("price after imbalance-offsetting sell", p2, 20.02)
    check("executed after imbalance-offsetting sell", e2, 5_000)
    check("imbalance after imbalance-offsetting sell", i2, 0)
    # A 3,000-share market sell instead moves the price down
    late2 = [*orders, Order("S-mkt2", "S", 3_000, MKT, 13)]
    p3, e3, i3, _ = uncross(late2, reference=20.01)
    check("price after 3,000 market sell", p3, 20.00)
    check("executed after 3,000 market sell", e3, 5_500)
    check("imbalance after 3,000 market sell", i3, 1_500)


def fee_example() -> None:
    print("== Fee models (hypothetical schedules, $ per share) ==")
    # Maker-taker venue MT and inverted venue INV; positive = paid to the participant
    mt_maker, mt_taker = +0.0020, -0.0030
    inv_maker, inv_taker = -0.0010, +0.0005
    bid, ask = 10.00, 10.01
    half = (ask - bid) / 2
    check("mid", (bid + ask) / 2, 10.005)
    check("taker all-in cost vs mid, MT", half - mt_taker, 0.0080)
    check("taker all-in cost vs mid, INV", half - inv_taker, 0.0045)
    check("net price of the 10.00 bid to a seller, MT", bid + mt_taker, 9.9970)
    check("net price of the 10.00 bid to a seller, INV", bid + inv_taker, 10.0005)
    check("maker round trip capturing the spread, MT", (ask - bid) + 2 * mt_maker, 0.0140)
    check("maker round trip capturing the spread, INV", (ask - bid) + 2 * inv_maker, 0.0080)
    # Expected value per share of a resting bid: P(fill) * (half-spread + maker fee - adverse move)
    adverse = 0.0045
    p_mt, p_inv = 0.25, 0.45
    v_mt = p_mt * (half + mt_maker - adverse)
    v_inv = p_inv * (half + inv_maker - adverse)
    check("EV per share of resting bid, MT", v_mt, 0.000625)
    check("EV per share of resting bid, INV", v_inv, -0.000225)
    # Inverted venue wins if its fills are less toxic: adverse 0.0030 at INV
    v_inv2 = p_inv * (half + inv_maker - 0.0030)
    check("EV per share of resting bid, INV with adverse 0.0030", v_inv2, 0.00045)
    # Access fee caps in basis points of price
    for px, old_bp, new_bp in ((5.0, 6.0, 2.0), (20.0, 1.5, 0.5), (100.0, 0.3, 0.1)):
        check(f"30-mil cap on a ${px:.0f} stock (bp)", 0.003 / px * 1e4, old_bp)
        check(f"10-mil cap on a ${px:.0f} stock (bp)", 0.001 / px * 1e4, new_bp)
    check("0.3% cap per share on a $0.50 quote", 0.003 * 0.50, 0.0015)
    check("0.1% cap per share on a $0.50 quote", 0.001 * 0.50, 0.0005)
    check("30-mil rebate as a share of a one-cent tick", 0.003 / 0.01, 0.30)


def tick_example() -> None:
    print("== Tick size ==")
    for px, bp in ((5.0, 20.0), (20.0, 5.0), (100.0, 1.0), (500.0, 0.2)):
        check(f"one-cent tick on ${px:.0f} (bp)", 0.01 / px * 1e4, bp)
    # Time-weighted average quoted spread over an evaluation period
    spreads = [(0.01, 0.70), (0.02, 0.25), (0.03, 0.05)]
    twaqs = sum(s * w for s, w in spreads)
    check("TWAQS", twaqs, 0.0135)
    assert twaqs <= 0.015  # qualifies for the $0.005 increment under amended Rule 612
    twaqs2 = sum(s * w for s, w in [(0.01, 0.50), (0.02, 0.40), (0.03, 0.10)])
    check("TWAQS, wider name", twaqs2, 0.016)
    assert twaqs2 > 0.015


def halt_example() -> None:
    print("== Price bands and circuit breakers ==")
    ref = 40.00
    check("LULD 5% lower band", ref * 0.95, 38.00)
    check("LULD 5% upper band", ref * 1.05, 42.00)
    check("LULD doubled lower band", ref * 0.90, 36.00)
    check("LULD doubled upper band", ref * 1.10, 44.00)
    spx = 5_800.0
    check("MWCB level 1 (7%)", spx * 0.93, 5_394.0)
    check("MWCB level 2 (13%)", spx * 0.87, 5_046.0)
    check("MWCB level 3 (20%)", spx * 0.80, 4_640.0)


if __name__ == "__main__":
    auction_example()
    fee_example()
    tick_example()
    halt_example()
    print("all exchange mechanics checks passed")
