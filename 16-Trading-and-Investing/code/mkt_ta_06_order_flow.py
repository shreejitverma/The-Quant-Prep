"""Order flow, footprint and tape-reading arithmetic: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/06-Order-Flow-Tape-Reading-and-Footprint.md`.
Independent routes used here:
- the order-book sweep by a price-time matching routine run on the displayed ask ladder, against the
  stated fills, new best ask, last price and average fill price;
- the footprint totals in exact integer arithmetic from the bid x ask table: row deltas, bid and ask
  column totals, bar volume and delta are each checked against the figure the note quotes, so the quoted
  row and column numbers must agree with one another, and the delta percent, point of control and
  diagonal imbalance ratios follow from the same table;
- the Lee-Ready (1991) classification by the quote rule with a tick-rule fallback that looks back to the
  last different trade price (not to the previous classification), applied to the four-trade example;
- the risk-reward ratio of the absorption example as an exact fraction, and its break-even hit rate by
  bisection on the expectancy against the closed form risk / (risk + reward).
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_06_order_flow.py`.
"""

from __future__ import annotations

from fractions import Fraction


def check(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def sweep(asks: list[tuple[float, int]], qty: int) -> tuple[list[tuple[float, int]], list[tuple[float, int]]]:
    """Fill a market buy against an ask ladder sorted by price; return fills and the remaining ladder."""
    fills, book = [], [list(level) for level in asks]
    while qty > 0:
        price, size = book[0]
        take = min(size, qty)
        fills.append((price, take))
        qty -= take
        book[0][1] -= take
        if book[0][1] == 0:
            book.pop(0)
    return fills, [tuple(level) for level in book]


def order_book() -> None:
    asks = [(100.01, 90), (100.02, 180), (100.03, 250)]
    bids = [(99.99, 120), (99.98, 210), (99.97, 340)]
    check("quoted spread", asks[0][0] - bids[0][0], "0.02")
    fills, book = sweep(asks, 150)
    assert fills == [(100.01, 90), (100.02, 60)], fills
    print("fills = 90 @ 100.01 + 60 @ 100.02")
    check("new best ask", book[0][0], "100.02")
    check("contracts left at the new best ask", book[0][1], "120")
    check("last traded price", fills[-1][0], "100.02")
    vwap = sum(p * q for p, q in fills) / sum(q for _, q in fills)
    check("average fill price", vwap, "100.014")


FOOTPRINT = {  # price: (volume sold at the bid, volume bought at the ask)
    100.05: (12, 140),
    100.04: (45, 520),
    100.03: (110, 680),
    100.02: (250, 310),
    100.01: (480, 95),
    100.00: (650, 20),
}


def footprint() -> None:
    print("input: footprint bar, (sold at the bid, bought at the ask) by price, 100.05 down to 100.00")
    print(f"input: {list(FOOTPRINT.items())}")
    bid_vol = {p: at_bid for p, (at_bid, _) in FOOTPRINT.items()}
    ask_vol = {p: at_ask for p, (_, at_ask) in FOOTPRINT.items()}
    row_delta = {p: ask_vol[p] - bid_vol[p] for p in FOOTPRINT}
    assert [row_delta[p] for p in FOOTPRINT] == [128, 475, 570, 60, -385, -630]
    print("row deltas, 100.05 down to 100.00 = +128, +475, +570, +60, -385, -630")
    total = sum(at_bid + at_ask for at_bid, at_ask in FOOTPRINT.values())
    delta = sum(row_delta.values())
    check("total bar volume", total, "3,312")
    check("volume sold at the bid", sum(bid_vol.values()), "1,547")
    check("volume bought at the ask", sum(ask_vol.values()), "1,765")
    check("bar delta", delta, "218")
    check("delta percent of volume", 100 * delta / total, "6.58")
    level_total = {p: bid_vol[p] + ask_vol[p] for p in FOOTPRINT}
    poc = max(level_total, key=level_total.get)
    check("bar point of control", poc, "100.03")
    check("volume at the point of control", level_total[poc], "790")
    # Diagonal ratios: ask volume at P against bid volume one tick lower, and the mirror for selling.
    buy_ratio = {p: ask_vol[p] / bid_vol[round(p - 0.01, 2)] for p in FOOTPRINT if round(p - 0.01, 2) in bid_vol}
    sell_ratio = {p: bid_vol[p] / ask_vol[round(p + 0.01, 2)] for p in FOOTPRINT if round(p + 0.01, 2) in ask_vol}
    check("buy ratio at 100.05 (140 / 45)", buy_ratio[100.05], "3.11")
    check("buy ratio at 100.04 (520 / 110)", buy_ratio[100.04], "4.73")
    check("buy ratio at 100.03 (680 / 250)", buy_ratio[100.03], "2.72")
    check("sell ratio at 100.00 (650 / 95)", sell_ratio[100.00], "6.84")
    buy_3to1 = sorted(p for p, r in buy_ratio.items() if r >= 3)
    sell_3to1 = sorted(p for p, r in sell_ratio.items() if r >= 3)
    assert buy_3to1 == [100.04, 100.05] and sell_3to1 == [100.00], (buy_3to1, sell_3to1)
    print("3:1 buying imbalances at 100.04 and 100.05 (two levels, not a stack of three); 3:1 selling at 100.00")


def lee_ready(trades: list[float], bid: float, ask: float) -> list[int]:
    mid = (bid + ask) / 2
    signs = []
    for i, price in enumerate(trades):
        if price > mid:
            signs.append(1)
        elif price < mid:
            signs.append(-1)
        else:  # tick rule: compare with the most recent different trade price
            j = i - 1
            while j >= 0 and trades[j] == price:
                j -= 1
            if j < 0:
                raise ValueError("no earlier different price for the tick rule")
            signs.append(1 if price > trades[j] else -1)
    return signs


def classification() -> None:
    prices = [50.04, 50.00, 50.02, 50.02]
    sizes = [500, 1200, 300, 400]
    signs = lee_ready(prices, 50.00, 50.04)
    assert signs == [1, -1, 1, 1], signs
    check("midpoint", (50.00 + 50.04) / 2, "50.02")
    print("Lee-Ready signs = +1 (quote), -1 (quote), +1 (uptick), +1 (zero-uptick)")
    check("net delta of the four trades", sum(s * q for s, q in zip(signs, sizes, strict=True)), "0")


def cited_constants() -> None:
    print("cited: Lee and Ready (1991) compare each trade with the quote at least 5 seconds earlier")
    print("cited: Odders-White (2000) Lee-Ready classified about 85% of NYSE (TORQ) trades correctly")
    print("cited: CME Rule 526 (block trades) and CME Rule 538 (EFRPs); Dodd-Frank (2010) section 747")
    print("cited: Regulation NMS Rule 600(b) and Rule 611 for intermarket sweep orders")
    print("cited: footprint imbalance ratio is user-chosen; charting packages often default to 3 or 4 times")
    print("cited: hypothetical scenario sizes, 500,000 shares bought at $150.00 and a drop to $149.20")
    print("cited: hypothetical iceberg sizes, 100,000 shares showing 500 and 50,000 shares showing 100")


def absorption_trade() -> None:
    entry, stop, target = Fraction(449700, 100), Fraction(450400, 100), Fraction(447500, 100)
    risk, reward = stop - entry, entry - target
    check("risk, points", float(risk), "7.00")
    check("reward, points", float(reward), "22.00")
    check("reward / risk", float(reward / risk), "3.14")
    lo, hi = Fraction(0), Fraction(1)
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if mid * reward - (1 - mid) * risk < 0 else (lo, mid)
    check("risk + reward, points", float(risk + reward), "29")
    check("break-even hit rate by bisection on the expectancy, percent", 100 * float(lo), "24.1")
    check("break-even hit rate from risk / (risk + reward), percent", 100 * float(risk / (risk + reward)), "24.1")
    check("wave 2 close below the 4,500.00 breakout level, points", 4498 - 4500, "-2")
    print("cited: Example 2 inputs, prior high 4,500.00, wave 1 pullback to 4,492.00, wave 2 close 4,498.00")
    print("cited: Example 2 trade plan, entry 4,497.00, stop 4,504.00, target 4,475.00")
    check("wave 2 delta added (17,000 - 5,000)", 17_000 - 5_000, "12,000")
    check("wave 2 new high above the prior high, points", 4503 - 4500, "3")


if __name__ == "__main__":
    order_book()
    footprint()
    classification()
    absorption_trade()
    cited_constants()
    print("all order-flow numbers check out")
