"""Limit order books and order types: every fill, allocation, queue value and fill time in the note.

Backs every number in `07-Market-Microstructure/01-Limit-Order-Books-and-Order-Types.md`.
Independent routes used here:
- market, IOC, FOK and post-only orders run through a small price-time matching engine that works in integer
  cents and walks resting orders one at a time, never via the weighted-average formula;
- pro-rata allocations by exact `fractions.Fraction` shares with floor rounding, checked against a lot-by-lot
  allocation that hands each lot to the order furthest below its fair share;
- iceberg priority by replaying the queue event by event, with a refresh that re-enters at the back;
- queue values by exact rational arithmetic and by a seeded simulation of fills and markouts;
- the time-to-fill rule of thumb by exact expectation and by simulating independent cancellations.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 07-Market-Microstructure/code/micro_01_limit_order_books.py`.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from fractions import Fraction

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


# ------------------------------------------------------------------ a tiny price-time book (prices in integer cents)


@dataclass
class Resting:
    owner: str
    size: int


class AskBook:
    def __init__(self, levels: list[tuple[int, int]]):
        self.levels = {price: deque([Resting(f"L{price}", size)]) for price, size in levels}

    def best(self) -> int:
        return min(p for p, q in self.levels.items() if sum(o.size for o in q) > 0)

    def available(self, limit: int) -> int:
        return sum(o.size for p, q in self.levels.items() if p <= limit for o in q)

    def buy(self, qty: int, limit: int | None, tif: str) -> list[tuple[int, int]]:
        """Execute a buy; tif is 'IOC' (partial allowed, rest cancelled) or 'FOK' (all or nothing)."""
        cap = limit if limit is not None else max(self.levels)
        if tif == "FOK" and self.available(cap) < qty:
            return []
        fills, left = [], qty
        for price in sorted(self.levels):
            if price > cap or left == 0:
                break
            for order in self.levels[price]:
                while order.size and left:  # one share at a time, so no averaging formula is used
                    order.size -= 1
                    left -= 1
                    if fills and fills[-1][0] == price:
                        fills[-1] = (price, fills[-1][1] + 1)
                    else:
                        fills.append((price, 1))
        return fills


def section_walk_the_book() -> None:
    print("Example 1: walking the book, IOC, FOK and post-only (cards ms-lob-walk-the-book-vwap, ms-lob-ioc-vs-fok)")
    levels = [(5001, 300), (5002, 500), (5003, 400), (5005, 1000)]
    fills = AskBook(levels).buy(1000, None, "IOC")
    exact("market buy 1,000 fills (cents, shares)", fills, [(5001, 300), (5002, 500), (5003, 200)])
    cost_cents = sum(p * n for p, n in fills)
    avg = Fraction(cost_cents, 100 * 1000)
    exact("average price", avg, Fraction(50019, 1000))
    approx("average price", float(avg), 50.019, 3)
    mid = Fraction(5000, 100)
    exact("cost versus the mid, dollars", (avg - mid) * 1000, 19)
    exact("cost per share versus the mid", avg - mid, Fraction(19, 1000))
    exact("of which beyond the best ask, dollars", (avg - Fraction(5001, 100)) * 1000, 9)
    ioc = AskBook(levels).buy(1000, 5002, "IOC")
    exact("IOC 1,000 at 50.02: filled", sum(n for _, n in ioc), 800)
    exact("IOC 1,000 at 50.02: cancelled", 1000 - sum(n for _, n in ioc), 200)
    fok = AskBook(levels).buy(1000, 5002, "FOK")
    exact("FOK 1,000 at 50.02: filled", sum(n for _, n in fok), 0)
    book = AskBook(levels)
    post_only_price = 5001
    crosses = post_only_price >= book.best()
    repriced = book.best() - 1 if crosses else post_only_price
    exact("post-only buy at 50.01 would cross", crosses, True)
    exact("post-only repriced one tick below the ask (cents)", repriced, 5000)


def pro_rata(sizes: list[int], incoming: int) -> tuple[list[Fraction], list[int]]:
    total = sum(sizes)
    shares = [Fraction(incoming * n, total) for n in sizes]
    return shares, [math.floor(x) for x in shares]


def lot_by_lot(sizes: list[int], incoming: int) -> list[int]:
    """Hand out lots one at a time to the order furthest below its exact share (largest remaining deficit)."""
    total = sum(sizes)
    got = [0] * len(sizes)
    for _ in range(incoming):
        deficits = [Fraction(incoming * n, total) - g for n, g in zip(sizes, got, strict=True)]
        got[max(range(len(sizes)), key=lambda i: deficits[i])] += 1
    return got


def section_pro_rata() -> None:
    print("Example 2: pro-rata allocation and over-quoting (card ms-lob-pro-rata-numeric)")
    shares, alloc = pro_rata([500, 300, 200], 400)
    exact("400 against A 500, B 300, C 200", alloc, [200, 120, 80])
    exact("lot-by-lot allocation agrees", lot_by_lot([500, 300, 200], 400), [200, 120, 80])
    _, alloc = pro_rata([500, 300, 200, 1000], 400)
    exact("400 after you add 1,000 (A, B, C, you)", alloc, [100, 60, 40, 200])
    _, alloc = pro_rata([500, 300, 200, 1000], 2000)
    exact("2,000 sweep: your fill", alloc[3], 1000)
    shares, alloc = pro_rata([500, 300, 200], 333)
    exact("333 exact shares", shares, [Fraction(333, 2), Fraction(999, 10), Fraction(333, 5)])
    approx("333 exact shares (A)", float(shares[0]), 166.5, 1)
    approx("333 exact shares (B)", float(shares[1]), 99.9, 1)
    approx("333 exact shares (C)", float(shares[2]), 66.6, 1)
    exact("333 floored", alloc, [166, 99, 66])
    exact("333 floored total", sum(alloc), 331)
    exact("lots left to the residual rule", 333 - sum(alloc), 2)


def section_iceberg() -> None:
    print("Example 3: iceberg priority (card ms-lob-iceberg-refresh-priority)")
    queue = deque([["I", 100], ["B", 300], ["C", 200]])
    hidden = {"I": 900}
    fills: dict[str, int] = {}
    left = 700
    while left:
        head = queue[0]
        take = min(head[1], left)
        head[1] -= take
        left -= take
        fills[head[0]] = fills.get(head[0], 0) + take
        if head[1] == 0:
            queue.popleft()
            if hidden.get(head[0], 0):
                tip = min(100, hidden[head[0]])
                hidden[head[0]] -= tip
                queue.append([head[0], tip])  # the refreshed tip joins the back of the queue
    exact("fills by order", fills, {"I": 200, "B": 300, "C": 200})
    exact("iceberg total", fills["I"], 200)
    exact("fully displayed 1,000-lot at the front would get", min(1000, 700), 700)


def section_queue_value(rng: np.random.Generator) -> None:
    print("Example 4: the same price, opposite signs (cards ms-lob-queue-value-sign, ms-lob-queue-value-numeric)")
    h, r = Fraction(1, 2), Fraction(1, 5)
    front = Fraction(55, 100) * (h + r - Fraction(1, 4))
    back = Fraction(20, 100) * (h + r - Fraction(85, 100))
    exact("V front, ticks", front, Fraction(2475, 10000))
    exact("V back, ticks", back, Fraction(-3, 100))
    exact("difference, ticks", front - back, Fraction(2775, 10000))
    approx("difference, ticks (2 dp)", float(front - back), 0.28, 2)
    n = 400_000
    for label, p_fill, adverse, quoted in (("front", 0.55, 0.25, 0.2475), ("back", 0.20, 0.85, -0.03)):
        filled = rng.random(n) < p_fill
        move = rng.normal(adverse, 1.0, n)  # conditional adverse move with unit noise around its mean
        pnl = np.where(filled, 0.5 + 0.2 - move, 0.0)
        se = float(pnl.std(ddof=1)) / math.sqrt(n)
        simulated(f"V {label}, simulated", float(pnl.mean()), quoted, 5 * se)


def section_time_to_fill(rng: np.random.Generator) -> None:
    print("Example 5: rough time to fill (card ms-lob-time-to-fill)")
    exact("E[T] = 3000 x 0.6 / 600 seconds", Fraction(3000) * Fraction(6, 10) / 600, 3)
    paths = 200_000
    survivors = rng.binomial(3000, 0.6, paths)  # each order ahead cancels independently with probability 0.4
    times = survivors / 600.0
    se = float(times.std(ddof=1)) / math.sqrt(paths)
    simulated("E[T], independent cancellations", float(times.mean()), 3.0, 5 * se)


if __name__ == "__main__":
    generator = np.random.default_rng(SEED)
    section_walk_the_book()
    section_pro_rata()
    section_iceberg()
    section_queue_value(generator)
    section_time_to_fill(generator)
