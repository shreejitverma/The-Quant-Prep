"""Microprice and order flow imbalance: every number in the fair-value note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/02-Fair-Value-and-Microprice.md`.
Independent routes used here:
- Example 1 mid, imbalance and volume-weighted microprice in exact rational arithmetic (fractions) from
  the weighted-average definition (Q_b * P_a + Q_a * P_b) / (Q_b + Q_a), checked against the literals;
- Example 2 OFI two ways: the Cont-Kukanov-Stoikov (2014) indicator formula applied to book snapshots, and
  a sum over the order book events (limit orders, cancels, market orders at the best quotes) that
  produced those snapshots; the event route never looks at the snapshot formula;
- the same snapshot-versus-event agreement on 5,000 random event sequences from a seeded simulated book,
  so a sign or case error in either route fails the check.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_pqt_02_microprice_ofi.py`.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

SEED = 23
TICK = 1  # prices in the random book are integer ticks


def rounded(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(value):,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def example_1() -> None:
    print("Example 1: volume-weighted microprice")
    pb, pa = Fraction("50.00"), Fraction("50.02")
    qb, qa = 8000, 2000
    print(f"    input: bid ${float(pb):.2f} x {qb:,}, ask ${float(pa):.2f} x {qa:,}")
    mid = (pa + pb) / 2
    imbalance = Fraction(qb - qa, qb + qa)
    micro = (qb * pa + qa * pb) / (qb + qa)
    rounded("quoted mid", mid, "50.0100")
    rounded("imbalance I", imbalance, "0.60")
    rounded("quoted spread", pa - pb, "0.02")
    rounded("I x half-spread", imbalance * (pa - pb) / 2, "0.0060")
    rounded("microprice", micro, "50.0160")
    rounded("microprice minus mid (cents)", (micro - mid) * 100, "0.6")
    assert micro == Fraction("50.016")
    rounded("skewed bid one tick above the bid", pb + Fraction(1, 100), "50.01")
    print("    cited: one tick = $0.01; Rule 612 increments $0.01 (>= $1.00), $0.0001 (< $1.00), 2024 amendment $0.005")
    print("    cited: $0.015 time-weighted average quoted spread threshold for the $0.005 increment")
    print("    cited: Cont, Kukanov and Stoikov (2014) OFI sample, TAQ data for 50 US stocks")
    print("    cited: Release 34-105656 (June 11, 2026) defers compliance to the first business day of November 2027")
    print("    cited: Release 34-105655 (June 11, 2026, File S7-2026-20) proposes rescinding Rules 611 and 610(e)")
    print("    cited: Andersen and Bondarenko (2014) dispute VPIN's power to predict toxicity events")


def snapshot_ofi(prev: tuple, cur: tuple) -> float:
    """Cont-Kukanov-Stoikov indicator form on (bid price, bid size, ask price, ask size) snapshots."""
    pb0, qb0, pa0, qa0 = prev
    pb1, qb1, pa1, qa1 = cur
    e = (pb1 >= pb0) * qb1 - (pb1 <= pb0) * qb0 - (pa1 <= pa0) * qa1 + (pa1 >= pa0) * qa0
    return float(e)


def example_2() -> None:
    print("Example 2: OFI across three book updates")
    snaps = [(100.00, 500, 100.05, 500), (100.00, 900, 100.05, 500), (100.05, 200, 100.10, 600)]
    for t, (pb_t, qb_t, pa_t, qa_t) in enumerate(snaps):
        print(f"    input: t={t} bid ${pb_t:.2f} x {qb_t}, ask ${pa_t:.2f} x {qa_t}")
    ofi = [snapshot_ofi(snaps[i - 1], snaps[i]) for i in (1, 2)]
    # event route: (side, kind, size) with signs fixed by the event type, not by the snapshot formula
    events = [
        [("bid", "limit", 400)],  # t=1: limit buys join the bid
        [("ask", "market_buy", 500), ("bid", "limit_improve", 200)],  # t=2: sweep the ask, new higher bid
    ]
    sign = {"limit": +1, "limit_improve": +1, "market_buy": +1}
    ofi_events = [sum(sign[k] * s for _, k, s in step) for step in events]
    (pb0, qb0, pa0, qa0), (pb1_, qb1_, pa1_, qa1_) = snaps[0], snaps[1]
    assert pb1_ == pb0 and pa1_ == pa0
    rounded("e_b,1 = Q_b,1 - Q_b,0 (bid unchanged)", qb1_ - qb0, "400")
    rounded("e_a,1 = Q_a,1 - Q_a,0 (ask unchanged)", qa1_ - qa0, "0")
    rounded("OFI_1, snapshot formula", ofi[0], "400")
    rounded("OFI_1, events", ofi_events[0], "400")
    rounded("OFI_2, snapshot formula", ofi[1], "700")
    rounded("OFI_2, events", ofi_events[1], "700")
    (pb1, qb1, pa1, qa1), (pb2, qb2, pa2, qa2) = snaps[1], snaps[2]
    e_b = (pb2 >= pb1) * qb2 - (pb2 <= pb1) * qb1
    e_a = (pa2 <= pa1) * qa2 - (pa2 >= pa1) * qa1
    rounded("e_b at t=2", e_b, "200")
    rounded("e_a at t=2 (minus the old ask size)", e_a, "-500")
    total = sum(ofi)
    rounded("cumulative OFI (shares)", total, "1,100")
    mid0 = (Fraction("100.00") + Fraction("100.05")) / 2
    mid2 = (Fraction("100.05") + Fraction("100.10")) / 2
    rounded("start mid", mid0, "100.025")
    rounded("end mid", mid2, "100.075")
    rounded("mid change", mid2 - mid0, "0.050")
    beta = (mid2 - mid0) / Fraction(int(total))
    rounded("price change per share of OFI", beta, "0.00004545")
    rounded("cents per 1,000 shares", beta * 1000 * 100, "4.55")


def random_book_check(rng: np.random.Generator, sequences: int = 5000, steps: int = 40) -> None:
    """Simulate events at the best quotes; compare per-event OFI by both routes."""
    print("Snapshot formula versus event sum on random books")
    mismatches = 0
    for _ in range(sequences):
        bids = {100 - k: int(rng.integers(1, 10)) * 100 for k in range(0, 6)}
        asks = {102 + k: int(rng.integers(1, 10)) * 100 for k in range(0, 6)}
        for _ in range(steps):
            bb, ba = max(bids), min(asks)
            prev = (bb, bids[bb], ba, asks[ba])
            kind = rng.integers(0, 8)
            size = int(rng.integers(1, 6)) * 100
            if kind == 0:  # limit buy at the best bid
                bids[bb] += size
                ev = +size
            elif kind == 1 and ba - bb > TICK:  # limit buy improving the bid
                bids[bb + TICK] = size
                ev = +size
            elif kind in (2, 3):  # cancel at, or market sell into, the best bid (possibly the whole queue)
                c = min(size, bids[bb])
                bids[bb] -= c
                ev = -c
            elif kind == 4:  # limit sell at the best ask
                asks[ba] += size
                ev = -size
            elif kind == 5 and ba - bb > TICK:  # limit sell improving the ask
                asks[ba - TICK] = size
                ev = -size
            elif kind == 6:  # cancel at the best ask
                c = min(size, asks[ba])
                asks[ba] -= c
                ev = +c
            else:  # market buy into the best ask
                c = min(size, asks[ba])
                asks[ba] -= c
                ev = +c
            bids = {p: q for p, q in bids.items() if q > 0}
            asks = {p: q for p, q in asks.items() if q > 0}
            if len(bids) < 2:
                bids[min(bids, default=max(bids, default=100)) - TICK] = 500
            if len(asks) < 2:
                asks[max(asks, default=min(asks, default=102)) + TICK] = 500
            bb, ba = max(bids), min(asks)
            cur = (bb, bids[bb], ba, asks[ba])
            if snapshot_ofi(prev, cur) != ev:
                mismatches += 1
    print(f"    sequences = {sequences}, events = {sequences * steps}, mismatches = {mismatches}")
    assert mismatches == 0


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    example_1()
    example_2()
    random_book_check(rng)
    print("all microprice and OFI numbers check out")
