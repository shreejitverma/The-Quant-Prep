"""Non-functional design: reproducible sums, counter-based random numbers, tail latency, availability, DR and cost.

Backs every number in `18-Pricing-and-Risk-Systems/16-Non-Functional-Design.md`.

1. Floating-point order dependence: a sum of 1,000,000 values of mixed magnitude in different orders versus the
   correctly rounded sum (math.fsum); a fixed reduction tree gives one answer for any worker count, while combining
   partial sums in completion order does not.
2. Kahan compensated summation in float32 (emulated with struct round-trips) against naive float32 and the exact sum
   of the float32 addends (fractions.Fraction).
3. Counter-based random numbers (NumPy Philox keyed per path): identical results for any partition of paths over
   workers, against a shared sequential stream whose draws depend on scheduling.
4. Percentiles do not add: an exact two-stage example where each stage's p99 is 1 ms and the p99 of the sum is 101 ms;
   fan-out amplification 1 - 0.99^n.
5. Availability arithmetic for serial chains and redundant pairs, and downtime per year.
6. Disaster recovery physics: great-circle distance New York to Chicago, round-trip lower bounds in vacuum and fibre,
   commits in flight by Little's law, replication bandwidth.
7. Recovery point and recovery time arithmetic from labelled-hypothetical settings.
8. Cloud versus owned capacity: break-even utilisation from labelled-hypothetical prices.

All prices, rates, sizes and settings are hypothetical teaching inputs unless a source is named in the note.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_non_functional.py`.
"""

from __future__ import annotations

import math
import random
import struct
from fractions import Fraction

import numpy as np

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Order dependence of floating-point sums
# ============================================================================


def position_pnls(n: int, seed: int) -> list[float]:
    """Mixed magnitudes from 1 cent to 10 million dollars, both signs (random.random only, no libm)."""
    rng = random.Random(seed)
    scales = (0.01, 0.1, 1.0, 10.0, 100.0, 1e3, 1e4, 1e5, 1e6, 1e7)  # literals, so no libm pow is involved
    return [(rng.random() - 0.5) * scales[rng.randrange(10)] for _ in range(n)]


def naive_sum(xs: list[float]) -> float:
    s = 0.0
    for x in xs:
        s += x
    return s


def fixed_tree_sum(xs: list[float], block: int, workers: int = 1) -> float:
    """Blocks are fixed by position; workers take blocks round-robin and file each partial under its block index;
    the partials are then combined in a fixed pairwise tree, so the worker count cannot change the result."""
    n_blocks = (len(xs) + block - 1) // block
    level = [0.0] * n_blocks
    for w in range(workers):
        for b in reversed(range(w, n_blocks, workers)):  # each worker runs its blocks in its own order
            level[b] = naive_sum(xs[b * block : (b + 1) * block])
    while len(level) > 1:
        nxt = [level[i] + level[i + 1] for i in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0]


def test_order_dependence() -> None:
    print("  1. One million position P&Ls (seed 2026): order dependence of the float64 sum")
    xs = position_pnls(1_000_000, 2026)
    exact = math.fsum(xs)
    forward = naive_sum(xs)
    backward = naive_sum(xs[::-1])
    ascending = naive_sum(sorted(xs, key=abs))
    rng = random.Random(1)
    shuffled = xs[:]
    rng.shuffle(shuffled)
    shuffled_sum = naive_sum(shuffled)
    results = {"forward": forward, "backward": backward, "ascending |x|": ascending, "shuffled": shuffled_sum}
    spread = max(results.values()) - min(results.values())
    assert len(set(results.values())) > 1  # the order changes the answer
    for name, v in results.items():
        print(f"    {name:14s} sum - exact = {v - exact:+.3e}")
    quoted("portfolio total ($ million)", exact / 1e6, -1012.773, 3)
    quoted("spread across the four orders (millionths of a dollar)", spread * 1e6, 23, 0)
    quoted("spread across the four orders (units in the last place of the total)", spread / math.ulp(exact), 190, 0)
    kahan = 0.0
    c = 0.0
    for x in xs:
        y = x - c
        t = kahan + y
        c = (t - kahan) - y
        kahan = t
    quoted("Kahan sum minus exact (units in the last place)", (kahan - exact) / math.ulp(exact), 0, 0)
    # Fixed tree versus completion-order combination of partial sums.
    block = 4096
    trees = {fixed_tree_sum(xs, block, workers) for workers in (1, 4, 16, 64)}
    tree = trees.pop()
    assert not trees  # one total for every worker count
    partials = [naive_sum(xs[i : i + block]) for i in range(0, len(xs), block)]
    dynamic = set()
    for run in range(20):
        order = partials[:]
        random.Random(100 + run).shuffle(order)  # workers finish in a different order each run
        dynamic.add(naive_sum(order))
    quoted("distinct totals in 20 runs, completion-order combine", len(dynamic), 10, 0)
    quoted("distinct totals for 1, 4, 16 and 64 workers, fixed tree", 1 + len(trees), 1, 0)
    print(f"    fixed-tree total - exact = {tree - exact:+.3e}")


# ============================================================================
# 2. Kahan summation in float32
# ============================================================================


def f32(x: float) -> float:
    return struct.unpack("<f", struct.pack("<f", x))[0]


def test_kahan_float32() -> None:
    print("  2. float32: 100,000 plus one million additions of 0.0001")
    base, add, n = f32(100_000.0), f32(0.0001), 1_000_000
    naive = base
    for _ in range(n):
        naive = f32(naive + add)
    s, c = base, 0.0
    for _ in range(n):
        y = f32(add - c)
        t = f32(s + y)
        c = f32(f32(t - s) - y)
        s = t
    exact = Fraction(base) + n * Fraction(add)
    spacing = f32(struct.unpack("<f", struct.pack("<I", struct.unpack("<I", struct.pack("<f", base))[0] + 1))[0]) - base
    quoted("float32 spacing at 100,000", spacing, 0.0078125, 7)
    quoted("naive float32 sum", naive, 100_000.0, 2)
    quoted("Kahan float32 sum", s, 100_100.0, 2)
    quoted("exact sum of the float32 addends", float(exact), 100_099.999997, 6)
    quoted("float32 nearest to the exact sum", f32(float(exact)), 100_100.0, 2)
    assert s == f32(float(exact))  # Kahan returns the correctly rounded result here


# ============================================================================
# 3. Counter-based random numbers
# ============================================================================


def path_payoff(path: int, steps: int, key: int) -> float:
    """Each path owns a Philox stream keyed by (key, path): its draws do not depend on who runs it."""
    gen = np.random.Generator(np.random.Philox(key=[key, path]))
    u = gen.random(steps)
    return float(np.max(np.cumsum(u - 0.5)))


def test_counter_rng() -> None:
    print("  3. Counter-based streams: same answer for any partition of 2,000 paths")
    n_paths, steps, key = 2_000, 64, 20_261_018
    payoffs_one = [path_payoff(p, steps, key) for p in range(n_paths)]
    # Four workers, interleaved assignment, processing their paths in reverse order.
    payoffs_four = [0.0] * n_paths
    for w in range(4):
        for p in reversed(range(w, n_paths, 4)):
            payoffs_four[p] = path_payoff(p, steps, key)
    assert payoffs_one == payoffs_four  # bit for bit, path by path
    assert path_payoff(1234, steps, key) == payoffs_one[1234]  # one path can be replayed alone for debugging

    # A shared sequential stream: which numbers a path gets depends on the order paths are served.
    def shared_stream(order: list[int]) -> list[float]:
        gen = np.random.Generator(np.random.Philox(key=[key, 0]))
        out = [0.0] * n_paths
        for p in order:
            out[p] = float(np.max(np.cumsum(gen.random(steps) - 0.5)))
        return out

    in_order = shared_stream(list(range(n_paths)))
    interleaved = shared_stream([p for w in range(4) for p in range(w, n_paths, 4)])
    changed = sum(a != b for a, b in zip(in_order, interleaved, strict=True))
    changed_counter = sum(a != b for a, b in zip(payoffs_one, payoffs_four, strict=True))
    quoted("per-path results changed by the schedule, counter-based (%)", 100.0 * changed_counter / n_paths, 0.0, 1)
    quoted("per-path results changed by the schedule, shared stream (%)", 100.0 * changed / n_paths, 99.9, 1)


# ============================================================================
# 4. Percentiles do not add
# ============================================================================


def quantile_discrete(dist: dict[float, float], q: float) -> float:
    """Smallest x with P(X <= x) >= q."""
    acc = 0.0
    for x in sorted(dist):
        acc += dist[x]
        if acc >= q - 1e-15:
            return x
    raise ValueError("bad distribution")


def test_tail_latency() -> None:
    print("  4. Tail latency: percentiles neither add nor bound")
    stage = {1.0: 0.992, 100.0: 0.008}  # ms: usually 1 ms, 0.8% of the time 100 ms
    total: dict[float, float] = {}
    for a, pa in stage.items():
        for b, pb in stage.items():
            total[a + b] = total.get(a + b, 0.0) + pa * pb
    p99_stage = quantile_discrete(stage, 0.99)
    p99_total = quantile_discrete(total, 0.99)
    quoted("p99 of each stage (ms)", p99_stage, 1, 0)
    quoted("sum of the stage p99s (ms)", 2 * p99_stage, 2, 0)
    quoted("probability the request is slow (%)", 100.0 * (1.0 - total[2.0]), 1.59, 2)
    quoted("p99 of the two-stage request (ms)", p99_total, 101, 0)
    # Monte Carlo check of the same distribution.
    rng = np.random.default_rng(5)
    a = np.where(rng.random(1_000_000) < 0.008, 100.0, 1.0)
    b = np.where(rng.random(1_000_000) < 0.008, 100.0, 1.0)
    assert float(np.quantile(a + b, 0.99)) == 101.0
    # Fan-out: a request waits for the slowest of n leaves.
    for n, exp in [(1, 1.0), (10, 9.56), (100, 63.40)]:
        quoted(f"fan-out {n}: share of requests hitting a leaf's 1% tail (%)", 100.0 * (1.0 - 0.99**n), exp, 2)
    quoted("per-leaf percentile needed for a fan-out-100 p99 (%)", 100.0 * 0.99 ** (1.0 / 100.0), 99.990, 3)


# ============================================================================
# 5. Availability
# ============================================================================

MINUTES_PER_YEAR = 365.25 * 24 * 60


def test_availability() -> None:
    print("  5. Availability arithmetic (independent failures assumed)")
    for a, exp in [(0.999, 525.96), (0.9999, 52.60), (0.99999, 5.26)]:
        quoted(f"downtime at {100 * a:g}% (minutes per year)", (1 - a) * MINUTES_PER_YEAR, exp, 2)
    serial = 0.999**3
    quoted("three 99.9% components in series (%)", 100.0 * serial, 99.7003, 4)
    quoted("series downtime (hours per year)", (1 - serial) * MINUTES_PER_YEAR / 60.0, 26.27, 2)
    pair = 1 - (1 - 0.999) ** 2
    quoted("two 99.9% replicas in parallel (%)", 100.0 * pair, 99.9999, 4)
    quoted("parallel-pair downtime (minutes per year)", (1 - pair) * MINUTES_PER_YEAR, 0.53, 2)
    # Redundant pair behind a 99.99% load balancer: the single point of failure dominates.
    chain = 0.9999 * pair
    quoted("pair behind a 99.99% load balancer (%)", 100.0 * chain, 99.9899, 4)


# ============================================================================
# 6. Disaster recovery physics
# ============================================================================


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088  # mean Earth radius (km)
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def test_dr_physics() -> None:
    print("  6. New York to Chicago synchronous replication")
    c_km_s = 299_792.458
    d = haversine_km(40.7128, -74.0060, 41.8781, -87.6298)
    quoted("great-circle distance (km)", d, 1144, 0)
    quoted("round trip at the speed of light in vacuum (ms)", 2 * d / c_km_s * 1e3, 7.63, 2)
    n_fibre = 1.47  # assumed group index of single-mode fibre
    rtt_gc_fibre = 2 * d * n_fibre / c_km_s * 1e3
    quoted("round trip in fibre along the great circle (ms)", rtt_gc_fibre, 11.22, 2)
    route_km = 1_300.0  # hypothetical fibre route length
    rtt = 2 * route_km * n_fibre / c_km_s * 1e3
    quoted("round trip on a 1,300 km fibre route (ms)", rtt, 12.75, 2)
    tps, wal_kb = 4_500.0, 1.8
    quoted("commits in flight (Little's law, 4,500 per second)", tps * rtt / 1e3, 57.4, 1)
    mb_s = tps * wal_kb / 1e3
    quoted("replication stream (MB/s)", mb_s, 8.1, 1)
    quoted("replication stream (Mbit/s)", mb_s * 8, 64.8, 1)
    quoted("with a 3x burst allowance (Mbit/s)", mb_s * 8 * 3, 194.4, 1)
    metro_km = 50.0  # hypothetical metro distance for the synchronous pair
    quoted("round trip over 50 km of fibre (ms)", 2 * metro_km * n_fibre / c_km_s * 1e3, 0.49, 2)


# ============================================================================
# 7. RPO and RTO
# ============================================================================


def test_rpo_rto() -> None:
    print("  7. Recovery point and recovery time (hypothetical settings)")
    snapshot_interval_min, log_ship_interval_min = 60.0, 5.0
    quoted("worst-case RPO, hourly snapshots only (minutes)", snapshot_interval_min, 60, 0)
    quoted("worst-case RPO, plus log shipping every 5 minutes (minutes)", min(snapshot_interval_min, log_ship_interval_min), 5, 0)
    lag_s, async_tps = 2.0, 4_500.0
    quoted("transactions at risk with 2 s async lag", lag_s * async_tps, 9_000, 0)
    detect, decide, promote, reconnect = 60.0, 300.0, 120.0, 180.0  # seconds
    quoted("RTO with a human failover decision (minutes)", (detect + decide + promote + reconnect) / 60.0, 11.0, 1)
    quoted("RTO with automated failover (minutes)", (detect + promote + reconnect) / 60.0, 6.0, 1)


# ============================================================================
# 8. Owned versus rented capacity
# ============================================================================


def test_break_even() -> None:
    print("  8. Owned versus cloud capacity (hypothetical prices)")
    server_cost, server_vcpu, life_years, opex_share = 30_000.0, 128, 4, 0.40  # opex per year as a share of price
    hours = 365.25 * 24
    owned_per_vcpu_hour = (server_cost / life_years + opex_share * server_cost) / server_vcpu / hours
    quoted("owned cost per vCPU-hour at full utilisation ($)", owned_per_vcpu_hour, 0.0174, 4)
    on_demand, spot = 0.045, 0.015  # $ per vCPU-hour
    quoted("break-even utilisation versus on-demand (%)", 100.0 * owned_per_vcpu_hour / on_demand, 38.6, 1)
    quoted("break-even utilisation versus spot (%)", 100.0 * owned_per_vcpu_hour / spot, 115.9, 1)
    burst_util = 1.0 / 24.0 * 252.0 / 365.25  # one hour per business day
    quoted("utilisation of a one-hour daily burst (%)", 100.0 * burst_util, 2.87, 2)
    vcpus = 50_000
    owned_year = owned_per_vcpu_hour * vcpus * hours
    rented_year = on_demand * vcpus * 252.0
    quoted("owned fleet for the burst, per year ($ million)", owned_year / 1e6, 7.62, 2)
    quoted("on-demand burst, per year ($ million)", rented_year / 1e6, 0.57, 2)


def main() -> None:
    print("Non-functional design checks")
    test_order_dependence()
    test_kahan_float32()
    test_counter_rng()
    test_tail_latency()
    test_availability()
    test_dr_physics()
    test_rpo_rto()
    test_break_even()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All non-functional checks passed.")


if __name__ == "__main__":
    main()
