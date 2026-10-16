"""Reg NMS mechanics for a router: NBBO, trade-through checks, intermarket sweeps, fee-aware venue choice, tick and SHO checks.

Backs every number in 09-Fragmentation-Reg-NMS-and-Routing.md.
Run ``python routing_reg_nms.py``: each result is printed and asserted.
Venue quotes and fee levels are hypothetical illustrations (fees chosen inside the Rule 610(c) caps).
"""

from __future__ import annotations

from dataclasses import dataclass


def check(label: str, value: float, expected: float, tol: float = 1e-9) -> float:
    """Print a labelled result and assert it is within tol of the expected value."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


@dataclass(frozen=True)
class Quote:
    venue: str
    bid: float
    bid_size: int
    ask: float
    ask_size: int
    taker_fee: float  # $ per share paid by a taker (negative = rebate)
    protected: bool = True  # automated quotation at an exchange best bid/offer


BOOK = [
    Quote("A", 20.00, 500, 20.03, 600, 0.0030),
    Quote("B", 20.01, 200, 20.02, 400, 0.0030),
    Quote("C", 19.99, 1_000, 20.02, 300, -0.0005),
    Quote("D", 20.01, 300, 20.04, 2_000, 0.0029),
]


def nbbo(book: list[Quote]) -> tuple[float, int, float, int]:
    """National best bid and offer from protected quotes, with aggregate size at each."""
    prot = [q for q in book if q.protected]
    nbb = max(q.bid for q in prot)
    nbo = min(q.ask for q in prot)
    return nbb, sum(q.bid_size for q in prot if q.bid == nbb), nbo, sum(q.ask_size for q in prot if q.ask == nbo)


def is_trade_through_buy(price: float, book: list[Quote]) -> bool:
    """A buy executed at `price` trades through if any protected offer is priced lower (Rule 600(b) definition)."""
    return any(q.protected and q.ask < price - 1e-12 for q in book)


def iso_sweep_buy(qty: int, limit: float, book: list[Quote]) -> list[tuple[str, int, float]]:
    """Route ISOs to the full displayed size of every protected offer priced better than `limit`, then take at `limit`."""
    fills = []
    left = qty
    for q in sorted(book, key=lambda q: (q.ask, q.taker_fee)):
        if q.ask > limit + 1e-12 or left == 0:
            continue
        take = q.ask_size if q.ask < limit - 1e-12 else min(left, q.ask_size)
        take = min(take, left)
        fills.append((q.venue, take, q.ask))
        left -= take
    return fills


def valid_increment(price: float, tick: float) -> bool:
    """True if `price` is an integer multiple of `tick` (Rule 612 minimum pricing increment)."""
    n = round(price / tick)
    return abs(n * tick - price) < 1e-9


def short_sale_permitted(price: float, nbb: float) -> bool:
    """Under an active Rule 201 restriction a short sale may not execute or display at or below the national best bid."""
    return price > nbb + 1e-12


def main() -> None:
    print("== NBBO ==")
    nbb, nbb_size, nbo, nbo_size = nbbo(BOOK)
    check("NBB", nbb, 20.01)
    check("size at NBB (B + D)", nbb_size, 500, 0)
    check("NBO", nbo, 20.02)
    check("size at NBO (B + C)", nbo_size, 700, 0)

    print("== Trade-through check ==")
    assert is_trade_through_buy(20.03, BOOK)
    assert not is_trade_through_buy(20.02, BOOK)
    print("buy at 20.03 on A while 20.02 offers are protected: trade-through = True")

    print("== ISO sweep: buy 2,000 limit 20.03 ==")
    fills = iso_sweep_buy(2_000, 20.03, BOOK)
    print("fills:", fills)
    assert fills == [("C", 300, 20.02), ("B", 400, 20.02), ("A", 600, 20.03)], fills
    filled = sum(f[1] for f in fills)
    avg = sum(f[1] * f[2] for f in fills) / filled
    fees = {q.venue: q.taker_fee for q in BOOK}
    fee_total = sum(f[1] * fees[f[0]] for f in fills)
    check("shares filled", filled, 1_300, 0)
    check("average price", avg, 20.024615, 1e-6)
    check("taker fees paid ($)", fee_total, 2.85, 1e-9)
    check("all-in average price", avg + fee_total / filled, 20.026808, 1e-6)
    check("residual shares left to rest at 20.03", 2_000 - filled, 700, 0)

    print("== Fee-aware choice at the same displayed price ==")
    check("all-in price at B (fee 30 mils)", 20.02 + 0.0030, 20.0230)
    check("all-in price at C (rebate 5 mils)", 20.02 - 0.0005, 20.0195)
    check("saving on 300 shares by taking C first ($)", 300 * (0.0030 + 0.0005), 1.05)
    check("saving per share ($)", 0.0030 + 0.0005, 0.0035)
    check("taker fee arithmetic: 400 x 0.003 + 600 x 0.003 - 300 x 0.0005", 400 * 0.003 + 600 * 0.003 - 300 * 0.0005, 2.85)

    print("== Dark midpoint ping before taking (hypothetical) ==")
    p_fill, saving_if_filled, adverse_if_not = 0.30, 0.005 + 0.0030, 0.002
    check("saving if the ping fills (half-spread + fee)", saving_if_filled, 0.008)
    check("expected saving per share", p_fill * saving_if_filled - (1 - p_fill) * adverse_if_not, 0.0010, 1e-12)

    print("== Rule 612 increments ==")
    assert not valid_increment(20.015, 0.01)
    assert valid_increment(20.015, 0.005)
    assert valid_increment(0.5012, 0.0001)
    print("20.015: invalid at $0.01, valid at $0.005; 0.5012 valid below $1.00")
    check("relative half-penny tick on a $20.00 stock (bp)", 0.005 / 20 * 1e4, 2.5)

    print("== Locked market avoidance ==")
    post_bid = 20.02
    locks = post_bid >= nbo - 1e-12
    assert locks
    check("post-only reprice of a 20.02 bid (one tick below the NBO)", round(nbo - 0.01, 2), 20.01)

    print("== Reg SHO Rule 201 ==")
    prior_close = 25.00
    trigger = prior_close * 0.90
    check("Rule 201 trigger price (10% below prior close)", trigger, 22.50)
    nbb_now = 22.40
    assert short_sale_permitted(22.41, nbb_now)
    assert not short_sale_permitted(22.40, nbb_now)
    print("short sale at 22.41 permitted (above NBB 22.40); at 22.40 not permitted")


if __name__ == "__main__":
    main()
    print("all routing checks passed")
