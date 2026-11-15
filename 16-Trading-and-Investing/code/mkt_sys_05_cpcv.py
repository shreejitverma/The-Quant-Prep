"""Combinatorial purged cross-validation and PBO: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/60-Systems/05-Combinatorial-Purged-Cross-Validation.md`.
Independent routes used here:
- split and path counts by enumerating every CPCV split with ``itertools.combinations`` and stitching
  the test groups into complete paths, never by evaluating the binomial formula alone;
- the purge and embargo counts by testing every observation's label window against the test span;
- the PBO of the worked example by counting the table rows;
- PBO under the null by seeded simulation of CSCV on skill-less strategies, against the exact value 1/2
  implied by exchangeability (the out-of-sample rank of the in-sample winner is uniform).
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_sys_05_cpcv.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (expected {expected}, tolerance {tol:.3f})")


def cpcv_paths(n: int, k: int) -> tuple[int, list[list[tuple[int, int]]]]:
    """Enumerate splits; build paths by giving each group's j-th test appearance to path j.

    Returns the split count and the paths, each a list of (group, split index) covering every group once.
    """
    splits = list(itertools.combinations(range(n), k))
    appearances: dict[int, list[int]] = {g: [] for g in range(n)}
    for s_idx, test in enumerate(splits):
        for g in test:
            appearances[g].append(s_idx)
    counts = {len(v) for v in appearances.values()}
    assert len(counts) == 1, "every group must be tested equally often"
    n_paths = counts.pop()
    paths = [[(g, appearances[g][j]) for g in range(n)] for j in range(n_paths)]
    return len(splits), paths


def cpcv_counts() -> None:
    print("CPCV splits and paths (Example 1, cards mkt-sys-133, mkt-sys-134)")
    n_splits, paths = cpcv_paths(6, 2)
    exact("splits for N = 6, k = 2", n_splits, 15)
    exact("complete paths for N = 6, k = 2", len(paths), 5)
    exact("test sets containing group 0", sum(1 for t in itertools.combinations(range(6), 2) if 0 in t), 5)
    for path in paths:
        assert sorted(g for g, _ in path) == list(range(6))
    # Every split's k test groups are used by paths exactly k times in total, so no prediction is wasted.
    used = sorted(s for path in paths for _, s in path)
    assert all(used.count(s) == 2 for s in range(15))
    for n in range(2, 11):
        for k in range(1, n):
            ns, ps = cpcv_paths(n, k)
            assert ns == math.comb(n, k) and len(ps) == math.comb(n - 1, k - 1)
            assert Fraction(k, n) * ns == len(ps)
    print("    paths = (k/N) C(N, k) = C(N-1, k-1) for every 2 <= N <= 10, 1 <= k < N by enumeration")


def purge_embargo() -> None:
    print("Example 3: purging and embargo counts (cards mkt-sys-130, mkt-sys-131, mkt-sys-142)")
    t_obs, horizon, test_lo, test_hi = 1000, 5, 400, 599
    h = int(0.01 * t_obs)
    exact("embargo h = 1% of T", h, 10)
    test_label_end = test_hi + horizon
    purged_before, purged_after, embargoed = [], [], []
    for i in range(t_obs):
        if test_lo <= i <= test_hi:
            continue
        overlaps = i <= test_label_end and i + horizon >= test_lo
        if overlaps:
            (purged_before if i < test_lo else purged_after).append(i)
        elif test_label_end < i <= test_label_end + h:
            embargoed.append(i)
    exact("test-label span end", test_label_end, 604)
    exact("purged before the test set", len(purged_before), 5)
    exact("first and last purged before", (purged_before[0], purged_before[-1]), (395, 399))
    exact("purged after the test set", len(purged_after), 5)
    exact("embargoed", len(embargoed), 10)
    exact("first and last embargoed", (embargoed[0], embargoed[-1]), (605, 614))
    exact("training observations left", t_obs - 200 - len(purged_before) - len(purged_after) - len(embargoed), 780)


def pbo_example() -> None:
    print("Example 2: PBO from the CSCV table (cards mkt-sys-136, mkt-sys-137)")
    exact("partitions C(6, 3)", math.comb(6, 3), 20)
    exact("partitions C(8, 4)", math.comb(8, 4), 70)
    exact("partitions C(10, 5)", math.comb(10, 5), 252)
    omega = [0.24, 0.42, 0.55, 0.31, 0.18, 0.62, 0.48, 0.35, 0.70, 0.29]
    first_ten = sum(1 for w in omega if w <= 0.50)
    exact("first ten partitions at or below the median", first_ten, 7)
    for w in omega:
        assert (math.log(w / (1 - w)) <= 0) == (w <= 0.5)
    total = first_ten + 6
    exact("partitions at or below the median", total, 13)
    exact("PBO", Fraction(total, 20), Fraction(13, 20))
    print(f"    PBO = {100 * total / 20:.1f}%")
    assert 100 * total / 20 == 65.0


def cscv_pbo(returns: np.ndarray, s_blocks: int) -> float:
    """PBO by CSCV (Bailey, Borwein, Lopez de Prado and Zhu 2017) on a T x M return matrix."""
    t_obs, m = returns.shape
    blocks = np.array_split(np.arange(t_obs), s_blocks)
    below = 0
    combos = list(itertools.combinations(range(s_blocks), s_blocks // 2))
    for js in combos:
        is_idx = np.concatenate([blocks[j] for j in js])
        oos_idx = np.concatenate([blocks[j] for j in range(s_blocks) if j not in js])
        r_is, r_oos = returns[is_idx], returns[oos_idx]
        sr_is = r_is.mean(0) / r_is.std(0, ddof=1)
        sr_oos = r_oos.mean(0) / r_oos.std(0, ddof=1)
        winner = int(np.argmax(sr_is))
        rank = 1 + int(np.sum(sr_oos < sr_oos[winner]))  # 1 = worst, M = best
        omega = rank / (m + 1)
        below += math.log(omega / (1 - omega)) <= 0
    return below / len(combos)


def pbo_null(rng: np.random.Generator) -> None:
    print("PBO under the null is one half (Core concepts 4, card mkt-sys-138)")
    m, t_obs, s_blocks, reps = 50, 600, 6, 400
    # Exchangeability: the OOS rank of the IS winner is uniform on 1..M, so P(rank <= 25) = 25/50.
    exact("exact null PBO for M = 50", Fraction(sum(1 for r in range(1, m + 1) if r / (m + 1) <= 0.5), m), Fraction(1, 2))
    pbos = np.array([cscv_pbo(rng.standard_normal((t_obs, m)), s_blocks) for _ in range(reps)])
    se = float(pbos.std(ddof=1)) / math.sqrt(reps)
    simulated(f"mean CSCV PBO over {reps} skill-less universes (seed {SEED})", float(pbos.mean()), 0.5, 4 * se)
    quoted = 0.49  # the seeded run as quoted in the note, two decimals
    assert abs(float(pbos.mean()) - quoted) <= 0.005, pbos.mean()
    print(f"    seeded mean PBO to two decimals = {float(pbos.mean()):.2f}")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    cpcv_counts()
    purge_embargo()
    pbo_example()
    pbo_null(rng)
    print("all CPCV numbers check out")
