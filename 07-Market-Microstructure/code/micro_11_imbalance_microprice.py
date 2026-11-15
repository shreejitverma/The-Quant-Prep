"""Order book imbalance and the microprice: every weighted mid, microprice, OFI and markout number in the note.

Backs every number in `07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md`.
Independent routes used here:
- weighted mids in exact `fractions.Fraction` arithmetic;
- the toy microprice three ways: the linear solve g1 = (1 - Q)^-1 R1, the Neumann series sum_n Q^n R1, and a
  seeded simulation of the imbalance chain run through several mid changes (which also checks that the later
  terms g2, g3, ... vanish when imbalance restarts symmetrically);
- order flow imbalance from the Cont-Kukanov-Stoikov indicator formula and from an explicit list of book events;
- the markout standard errors by simulating 2,000 fills.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 07-Market-Microstructure/code/micro_11_imbalance_microprice.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction as F

import numpy as np

SEED = 20261114
U = np.array([0.02, 0.05, 0.10, 0.18, 0.30])
D = U[::-1].copy()
BUCKETS = [0.1, 0.3, 0.5, 0.7, 0.9]


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


def section_weighted_mid() -> None:
    print("Example 1: imbalance and weighted mid (card ms-obi-weighted-mid-numeric)")
    pb, pa, qb, qa = F("100.00"), F("100.01"), 800, 200
    imb = F(qb, qb + qa)
    exact("I", imb, F(4, 5))
    pw = imb * pa + (1 - imb) * pb
    exact("weighted mid", pw, F("100.008"))
    mid = (pa + pb) / 2
    exact("mid", mid, F("100.005"))
    exact("weighted mid minus mid, ticks", (pw - mid) / F("0.01"), F(3, 10))
    exact("M + (I - 1/2) S agrees", mid + (imb - F(1, 2)) * (pa - pb), pw)
    imb2 = F(qb - 600, qb - 600 + qa)
    exact("I after a 600-lot bid cancels", imb2, F(1, 2))
    exact("weighted mid after the cancel", imb2 * pa + (1 - imb2) * pb, mid)


def transient_matrix(stay_only: bool = False) -> np.ndarray:
    """Imbalance moves while the mid stays: half the no-change mass stays, a quarter to each neighbour (reflecting)."""
    q = np.zeros((5, 5))
    for i in range(5):
        rest = 1 - U[i] - D[i]
        if stay_only:
            q[i, i] = rest
            continue
        q[i, i] += 0.5 * rest
        for j in (i - 1, i + 1):
            q[i, j if 0 <= j < 5 else i] += 0.25 * rest
    return q


def section_toy_microprice(rng: np.random.Generator) -> None:
    print("Example 2: a toy microprice (cards ms-obi-microprice-g1, ms-obi-toy-microprice)")
    q = transient_matrix()
    r1 = 0.5 * (U - D)
    g1 = np.linalg.solve(np.eye(5) - q, r1)
    series = np.zeros(5)
    term = r1.copy()
    for _ in range(2000):
        series += term
        term = q @ term
    assert np.max(np.abs(series - g1)) < 1e-12
    quoted = [-0.362, -0.219, 0.0, 0.219, 0.362]
    for i, b in enumerate(BUCKETS):
        approx(f"microprice minus mid at I = {b} (ticks)", g1[i], quoted[i], 3)
        approx(f"weighted mid minus mid at I = {b} (ticks)", b - 0.5, [-0.4, -0.2, 0.0, 0.2, 0.4][i], 1)
    print("    Neumann series sum_n Q^n R1 equals the linear solve to 1e-12")
    gaps = np.abs(np.array(BUCKETS) - 0.5 - g1)
    approx("largest gap between weighted mid and microprice (ticks)", float(gaps.max()), 0.038, 3)
    assert np.all(np.abs(g1) < 0.5)
    exact("steeper than the weighted mid at I = 0.7", bool(g1[3] > 0.2), True)
    exact("flatter than the weighted mid at I = 0.9", bool(g1[4] < 0.4), True)
    g_stay = np.linalg.solve(np.eye(5) - transient_matrix(stay_only=True), r1)
    approx("I = 0.9 if imbalance never moved before the mid (ticks)", g_stay[4], 0.4375, 4)
    approx("0.5 x 0.28 / 0.32", 0.5 * 0.28 / 0.32, 0.4375, 4)
    print("    letting imbalance mean-revert first pulls the I = 0.9 value from 0.4375 to 0.362 ticks")
    # T g1 = 0 when imbalance restarts from a distribution symmetric around 0.5
    restart = np.array([0.1, 0.2, 0.4, 0.2, 0.1])
    t_mat = np.outer(U + D, restart)
    exact("T g1 = 0 (max abs, below 1e-15)", bool(np.max(np.abs(t_mat @ g1)) < 1e-15), True)

    # simulation: start in each bucket, run through 4 mid changes, average the total mid change
    paths = 400_000
    cum_q = np.cumsum(q / q.sum(axis=1, keepdims=True), axis=1)
    for start in range(5):
        state = np.full(paths, start)
        total = np.zeros(paths)
        changes = np.zeros(paths, dtype=int)
        while np.any(changes < 4):
            live = changes < 4
            u = rng.random(paths)
            up = live & (u < U[state])
            down = live & ~up & (u < U[state] + D[state])
            moved = up | down
            total += 0.5 * up - 0.5 * down
            changes += moved
            restart_state = np.minimum(np.searchsorted(np.cumsum(restart), rng.random(paths)), 4)
            stay = live & ~moved
            nxt = np.minimum((rng.random(paths)[:, None] > cum_q[state]).sum(axis=1), 4)  # inverse-CDF draw per row
            state = np.where(moved, restart_state, state)
            state[stay] = nxt[stay]
        se = float(total.std(ddof=1)) / math.sqrt(paths)
        simulated(f"E[mid after 4 changes] - mid from I = {BUCKETS[start]}", float(total.mean()), quoted[start], 5 * se)


def cks_ofi(prev: tuple[F, int, F, int], cur: tuple[F, int, F, int]) -> int:
    """Cont, Kukanov and Stoikov (2014) e_n from consecutive (bid price, bid size, ask price, ask size)."""
    pb0, qb0, pa0, qa0 = prev
    pb1, qb1, pa1, qa1 = cur
    return (pb1 >= pb0) * qb1 - (pb1 <= pb0) * qb0 - (pa1 <= pa0) * qa1 + (pa1 >= pa0) * qa0


def section_ofi() -> None:
    print("Example 3: computing OFI (cards ms-obi-ofi-definition, ms-obi-ofi-numeric)")
    snaps = [
        (F("100.00"), 500, F("100.01"), 400),
        (F("100.00"), 700, F("100.01"), 400),
        (F("100.00"), 700, F("100.01"), 100),
        (F("100.00"), 700, F("100.02"), 600),
        (F("100.01"), 200, F("100.02"), 600),
    ]
    e = [cks_ofi(a, b) for a, b in zip(snaps[:-1], snaps[1:], strict=True)]
    exact("e_n for n = 1..4", e, [200, 300, 100, 200])
    # event route: bid adds +, ask removals +, with level changes counting the whole old ask or new bid queue
    events = [("bid add", 200), ("ask removed", 300), ("ask level cleared", 100), ("new better bid", 200)]
    exact("sum of signed book events", sum(size for _, size in events), 800)
    exact("OFI", sum(e), 800)
    depth = 1000
    exact("stylised Delta P = OFI / (2 D) in ticks", F(sum(e), 2 * depth), F(2, 5))
    mid0 = (snaps[0][0] + snaps[0][2]) / 2
    mid4 = (snaps[-1][0] + snaps[-1][2]) / 2
    exact("mid at n = 0", mid0, F("100.005"))
    exact("mid at n = 4", mid4, F("100.015"))
    exact("actual mid change, ticks", (mid4 - mid0) / F("0.01"), 1)


def section_markout_rule(rng: np.random.Generator) -> None:
    print("Example 4: judging an imbalance rule by markouts (card ms-obi-pull-rule-gain)")
    rows = [(2000, F(-6, 10)), (5000, F(1, 10)), (3000, F(4, 10))]
    exact("bid fills bucketed", sum(n for n, _ in rows), 10_000)
    totals = [n * m for n, m in rows]
    exact("bucket totals", totals, [-1200, 500, 1200])
    exact("total edge", sum(totals), 500)
    exact("total after pulling I < 0.3", sum(totals[1:]), 1700)
    exact("gain from pulling", sum(totals[1:]) - sum(totals), 1200)
    for sd, quoted in ((2.0, 0.045), (4.0, 0.089)):
        approx(f"standard error with per-fill sd {sd:.0f} over 2,000 fills", sd / math.sqrt(2000), quoted, 3)
        means = rng.normal(-0.6, sd, (5000, 2000)).mean(axis=1)
        simulated(
            f"simulated sd of the bucket mean, sd {sd:.0f}", float(means.std(ddof=1)), quoted, 5 * quoted / math.sqrt(2 * 5000) + 5e-4
        )
    approx("-0.6 in standard errors at sd 4", 0.6 / (4 / math.sqrt(2000)), 6.7, 1)


if __name__ == "__main__":
    generator = np.random.default_rng(SEED)
    section_weighted_mid()
    section_toy_microprice(generator)
    section_ofi()
    section_markout_rule(generator)
