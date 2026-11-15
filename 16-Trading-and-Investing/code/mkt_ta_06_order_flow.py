"""Order flow, footprint and tape-reading arithmetic: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/06-Order-Flow-Tape-Reading-and-Footprint.md`.
Independent routes used here:
- the order-book sweep by a price-time matching routine run on the displayed ask ladder, against the
  stated fills, new best ask, last price and average fill price;
- the footprint bar rebuilt from a shuffled tape of one-lot prints, each classified by comparing its
  aggressor price with the bid and ask, then re-aggregated into the bid x ask matrix, totals, delta,
  delta percent, point of control and diagonal imbalance ratios;
- the Lee-Ready (1991) classification by the quote rule with a tick-rule fallback that looks back to the
  last different trade price (not to the previous classification), applied to the four-trade example;
- the risk-reward ratio of the absorption example as an exact fraction.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_06_order_flow.py`.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

SEED = 6


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


def footprint(rng: np.random.Generator) -> None:
    # Rebuild the bar from a tape: one print per lot with the bid and ask that stood when it traded.
    tape = []
    for price, (at_bid, at_ask) in FOOTPRINT.items():
        tape += [(price, round(price, 2), round(price + 0.01, 2))] * at_bid  # sell hits a bid at this price
        tape += [(price, round(price - 0.01, 2), round(price, 2))] * at_ask  # buy lifts an ask at this price
    order = rng.permutation(len(tape))
    bid_vol: dict[float, int] = {}
    ask_vol: dict[float, int] = {}
    for i in order:
        price, bid, ask = tape[i]
        if price >= ask:
            ask_vol[price] = ask_vol.get(price, 0) + 1
        elif price <= bid:
            bid_vol[price] = bid_vol.get(price, 0) + 1
    for price, (at_bid, at_ask) in FOOTPRINT.items():
        assert bid_vol.get(price, 0) == at_bid and ask_vol.get(price, 0) == at_ask
    row_delta = {p: ask_vol.get(p, 0) - bid_vol.get(p, 0) for p in FOOTPRINT}
    assert [row_delta[p] for p in FOOTPRINT] == [128, 475, 570, 60, -385, -630]
    print("row deltas, 100.05 down to 100.00 = +128, +475, +570, +60, -385, -630")
    total = len(tape)
    delta = sum(1 if tape[i][0] >= tape[i][2] else -1 for i in order)
    check("total bar volume", total, "3,312")
    check("volume sold at the bid", sum(bid_vol.values()), "1,547")
    check("volume bought at the ask", sum(ask_vol.values()), "1,765")
    check("bar delta", delta, "218")
    check("delta percent of volume", 100 * delta / total, "6.58")
    level_total = {p: bid_vol.get(p, 0) + ask_vol.get(p, 0) for p in FOOTPRINT}
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


def absorption_trade() -> None:
    entry, stop, target = Fraction(449700, 100), Fraction(450400, 100), Fraction(447500, 100)
    risk, reward = stop - entry, entry - target
    check("risk, points", float(risk), "7.00")
    check("reward, points", float(reward), "22.00")
    check("reward / risk", float(reward / risk), "3.14")
    breakeven = risk / (risk + reward)
    # Break-even hit rate p solves p x reward = (1 - p) x risk; check by expectancy, not by the same ratio.
    assert breakeven * reward - (1 - breakeven) * risk == 0
    check("break-even hit rate before costs, percent", 100 * float(breakeven), "24.1")
    check("wave 2 delta added (17,000 - 5,000)", 17_000 - 5_000, "12,000")
    check("wave 2 new high above the prior high, points", 4503 - 4500, "3")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    order_book()
    footprint(rng)
    classification()
    absorption_trade()
    print("all order-flow numbers check out")
