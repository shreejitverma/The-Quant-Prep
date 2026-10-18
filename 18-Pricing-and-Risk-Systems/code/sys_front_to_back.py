"""Front-to-back architecture: sizing, queueing, latency budgets, reconciliation and event-handling checks.

Backs every number in `18-Pricing-and-Risk-Systems/01-Front-to-Back-Architecture.md`.
All bank volumes, payload sizes, service times and thresholds below are labelled-hypothetical inputs chosen
for teaching; none is a measurement of any real firm or product.
Every quoted number is computed from those inputs, printed as ``label = value`` and asserted to within half a unit
of its last quoted decimal.

Run it with `python 18-Pricing-and-Risk-Systems/code/sys_front_to_back.py`.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from statistics import NormalDist

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:.{decimals}f}")
    return value


# ============================================================================
# 1. Trade event bus sizing (Example 1)
# ============================================================================


@dataclass(frozen=True)
class BusInputs:
    """Hypothetical inputs for a trade lifecycle event bus."""

    events_per_day: float = 2_500_000  # new, amend, cancel, exercise, fixing events
    window_seconds: float = 10 * 3600  # events assumed spread over a 10-hour day
    burst_multiplier: float = 40.0  # peak-to-average ratio at opens, closes and data releases
    payload_bytes: float = 12_000  # serialised event incl. legs, parties and audit headers
    replication: int = 3  # copies kept by the log
    hot_retention_days: int = 14
    service_ms: float = 5.0  # mean per-event processing time of one risk consumer
    headroom: float = 1.5  # capacity margin over the peak


def bus_sizing(b: BusInputs) -> dict[str, float]:
    lam_avg = b.events_per_day / b.window_seconds
    lam_peak = lam_avg * b.burst_multiplier
    mu = 1000.0 / b.service_ms
    consumers_exact = lam_peak / mu
    return {
        "lam_avg": lam_avg,
        "lam_peak": lam_peak,
        "avg_MBps": lam_avg * b.payload_bytes / 1e6,
        "avg_Mbps": lam_avg * b.payload_bytes * 8 / 1e6,
        "peak_MBps": lam_peak * b.payload_bytes / 1e6,
        "peak_Mbps": lam_peak * b.payload_bytes * 8 / 1e6,
        "raw_GB_day": b.events_per_day * b.payload_bytes / 1e9,
        "replicated_GB_day": b.events_per_day * b.payload_bytes * b.replication / 1e9,
        "hot_TB": b.events_per_day * b.payload_bytes * b.replication * b.hot_retention_days / 1e12,
        "mu": mu,
        "consumers_exact": consumers_exact,
        "consumers_min": math.ceil(consumers_exact),
        "partitions": math.ceil(consumers_exact * b.headroom),
    }


def mm1_partition_sojourn_ms(lam_total: float, partitions: int, mu: float) -> float:
    """Mean time in system (queue plus service) of one partition modelled as M/M/1 with lam_total/partitions arrivals."""
    lam_p = lam_total / partitions
    assert lam_p < mu, "partition is unstable"
    return 1000.0 / (mu - lam_p)


def simulate_partition_sojourn_ms(lam_total: float, partitions: int, mu: float, n: int, seed: int) -> float:
    """Discrete-event check of the M/M/1 formula for one partition (Lindley recursion)."""
    rng = random.Random(seed)
    lam_p = lam_total / partitions
    wait = 0.0
    total = 0.0
    prev_service = 0.0
    for i in range(n):
        inter = rng.expovariate(lam_p)
        if i:
            wait = max(0.0, wait + prev_service - inter)
        prev_service = rng.expovariate(mu)
        total += wait + prev_service
    return 1000.0 * total / n


# ============================================================================
# 2. Latency budget: the p99 of a sum is not the sum of p99s
# ============================================================================

# Hypothetical RFQ path stages: (name, median ms, lognormal sigma).
RFQ_STAGES = (
    ("gateway and normalisation", 0.4, 0.5),
    ("curve and surface snapshot read", 0.6, 0.6),
    ("pricing", 3.0, 0.4),
    ("pre-trade credit and limit check", 0.8, 0.7),
    ("quote publication", 0.3, 0.5),
)


def lognormal_quantile(median: float, sigma: float, p: float) -> float:
    return median * math.exp(sigma * NormalDist().inv_cdf(p))


def latency_budget(n: int, seed: int) -> dict[str, float]:
    rng = random.Random(seed)
    sum_p99 = sum(lognormal_quantile(m, s, 0.99) for _, m, s in RFQ_STAGES)
    totals = sorted(sum(m * math.exp(s * rng.gauss(0.0, 1.0)) for _, m, s in RFQ_STAGES) for _ in range(n))
    p99_total = totals[int(0.99 * n) - 1]
    return {"sum_median": sum(m for _, m, _ in RFQ_STAGES), "sum_p99": sum_p99, "p99_total": p99_total}


# ============================================================================
# 3. Front-office versus back-office valuation break (Example 2)
# ============================================================================


def receiver_swap_pv(notionals: list[float], fixed: float, zero: float) -> float:
    """PV of receiving `fixed` annually on notional N_i for year i, paying the annual forward, on a flat continuous zero curve."""
    pv = 0.0
    for i, n in enumerate(notionals, start=1):
        df_prev, df = math.exp(-zero * (i - 1)), math.exp(-zero * i)
        fwd = df_prev / df - 1.0  # simple annual forward with accrual 1
        pv += n * (fixed - fwd) * df
    return pv


# ============================================================================
# 4. At-least-once delivery, ordering and idempotent consumers (Example 3)
# ============================================================================


@dataclass(frozen=True)
class Event:
    trade_id: int
    version: int
    notional: float


def make_events(n_trades: int, rng: random.Random) -> list[list[Event]]:
    out = []
    for t in range(n_trades):
        versions = 1 + (rng.random() < 0.3) + (rng.random() < 0.1)  # some trades are amended once or twice
        out.append([Event(t, v, float(rng.randint(1, 100)) * 1e6) for v in range(1, versions + 1)])
    return out


def deliver(per_trade: list[list[Event]], partitions: int, by_trade_key: bool, dup_prob: float, rng: random.Random) -> list[Event]:
    """Produce events to partitions, then interleave partitions at random as a multi-threaded consumer group would.

    Keyed by trade id, all versions of a trade share a partition, so their order is preserved.
    Unkeyed (round robin), versions of one trade can land on different partitions and be consumed out of order.
    Each delivery is repeated with probability `dup_prob` (a retry after a lost acknowledgement).
    """
    queues: list[list[Event]] = [[] for _ in range(partitions)]
    rr = 0
    for evs in per_trade:
        for e in evs:
            if by_trade_key:
                p = e.trade_id % partitions
            else:
                p = rr % partitions
                rr += 1
            queues[p].append(e)
            if rng.random() < dup_prob:
                queues[p].append(e)
    heads = [0] * partitions
    out = []
    live = [p for p in range(partitions) if queues[p]]
    while live:
        p = rng.choice(live)
        # Unequal consumer speed: a partition drains a random small batch at a time.
        for _ in range(rng.randint(1, 50)):
            if heads[p] >= len(queues[p]):
                break
            out.append(queues[p][heads[p]])
            heads[p] += 1
        live = [q for q in range(partitions) if heads[q] < len(queues[q])]
    return out


def consume(stream: list[Event], dedupe: bool, version_guard: bool) -> tuple[dict[int, float], float]:
    """Return final notional per trade and the summed notional of every applied 'new trade' event."""
    state: dict[int, tuple[int, float]] = {}
    seen: set[tuple[int, int]] = set()
    booked_total = 0.0
    for e in stream:
        key = (e.trade_id, e.version)
        if dedupe:
            if key in seen:
                continue
            seen.add(key)
        if e.version == 1:
            booked_total += e.notional
        if version_guard and e.trade_id in state and state[e.trade_id][0] >= e.version:
            continue
        state[e.trade_id] = (e.version, e.notional)
    return {t: v[1] for t, v in state.items()}, booked_total


def ordering_experiment(seed: int = 7, n_trades: int = 10_000, partitions: int = 12, dup_prob: float = 0.02) -> dict[str, float]:
    rng = random.Random(seed)
    per_trade = make_events(n_trades, rng)
    truth = {evs[-1].trade_id: evs[-1].notional for evs in per_trade}
    true_booked = sum(evs[0].notional for evs in per_trade)
    res: dict[str, float] = {"events": sum(len(e) for e in per_trade), "amended": sum(len(e) > 1 for e in per_trade)}
    for keyed in (True, False):
        stream = deliver(per_trade, partitions, keyed, dup_prob, random.Random(seed + (0 if keyed else 1)))
        tag = "keyed" if keyed else "unkeyed"
        res[f"{tag}_deliveries"] = len(stream)
        for dedupe, guard, name in ((False, False, "naive"), (True, False, "dedupe"), (True, True, "dedupe_guard")):
            final, booked = consume(stream, dedupe, guard)
            res[f"{tag}_{name}_wrong_final"] = sum(final[t] != truth[t] for t in truth)
            res[f"{tag}_{name}_overbooked_pct"] = 100.0 * (booked / true_booked - 1.0)
    return res


# ============================================================================
# 5. Trade lifecycle state machine
# ============================================================================

LIFECYCLE = {
    "Pending": {"Live", "Rejected"},
    "Live": {"Live", "Novated", "PartiallyTerminated", "Terminated", "Exercised", "Matured", "Cancelled"},
    "PartiallyTerminated": {"Live", "PartiallyTerminated", "Terminated", "Novated", "Matured"},
    "Rejected": set(),
    "Novated": set(),
    "Terminated": set(),
    "Exercised": set(),
    "Matured": set(),
    "Cancelled": set(),
}
CONFIRMATION = {
    "Unconfirmed": {"Affirmed", "Disputed"},
    "Affirmed": {"Confirmed", "Disputed"},
    "Disputed": {"Affirmed", "Unconfirmed"},
    "Confirmed": {"Unconfirmed"},  # an economic amendment reopens confirmation
}


def valid_path(machine: dict[str, set[str]], path: list[str]) -> bool:
    return all(b in machine[a] for a, b in zip(path, path[1:], strict=False))


def run_tests() -> None:
    print("Front-to-back architecture checks")

    print("  Example 1: event bus sizing (hypothetical inputs)")
    b = BusInputs()
    s = bus_sizing(b)
    quoted("average arrival rate (events/s)", s["lam_avg"], 69.44, 2)
    quoted("peak arrival rate (events/s)", s["lam_peak"], 2777.78, 2)
    quoted("average throughput (MB/s)", s["avg_MBps"], 0.833, 3)
    quoted("average throughput (Mbit/s)", s["avg_Mbps"], 6.67, 2)
    quoted("peak throughput (MB/s)", s["peak_MBps"], 33.33, 2)
    quoted("peak throughput (Mbit/s)", s["peak_Mbps"], 266.67, 2)
    quoted("raw log volume (GB/day)", s["raw_GB_day"], 30, 0)
    quoted("replicated log volume (GB/day)", s["replicated_GB_day"], 90, 0)
    quoted("14-day hot tier (TB)", s["hot_TB"], 1.26, 2)
    quoted("one consumer capacity (events/s)", s["mu"], 200, 0)
    quoted("consumers needed at peak, exact", s["consumers_exact"], 13.89, 2)
    quoted("consumers needed at peak, rounded up", s["consumers_min"], 14, 0)
    quoted("partitions with 1.5x headroom", s["partitions"], 21, 0)
    for c, expected in ((14, 630.0), (21, 14.77)):
        w = mm1_partition_sojourn_ms(s["lam_peak"], c, s["mu"])
        quoted(f"M/M/1 mean time in partition at peak with {c} partitions (ms)", w, expected, 0 if c == 14 else 2)
        quoted(f"utilisation with {c} partitions", s["lam_peak"] / (c * s["mu"]), 0.992 if c == 14 else 0.661, 3)
        quoted(f"arrivals per partition with {c} partitions (events/s)", s["lam_peak"] / c, 198.41 if c == 14 else 132.28, 2)
    sim21 = simulate_partition_sojourn_ms(s["lam_peak"], 21, s["mu"], 400_000, seed=11)
    quoted("simulated mean time in partition with 21 partitions (ms, seed 11)", sim21, 14.9, 1)
    littles_l = s["lam_peak"] * mm1_partition_sojourn_ms(s["lam_peak"], 21, s["mu"]) / 1000.0
    quoted("Little's law: events in flight at peak with 21 partitions", littles_l, 41.0, 1)

    print("  Latency budget (hypothetical stage medians and spreads, seed 3)")
    lb = latency_budget(200_000, seed=3)
    quoted("sum of stage medians (ms)", lb["sum_median"], 5.1, 1)
    quoted("sum of stage p99s (ms)", lb["sum_p99"], 16.3, 1)
    quoted("simulated p99 of end-to-end latency (ms)", lb["p99_total"], 10.9, 1)
    assert lb["p99_total"] < lb["sum_p99"]

    print("  Example 2: amortising swap dropped to bullet by a downstream feed (hypothetical terms)")
    amort = [50e6, 40e6, 30e6, 20e6, 10e6]
    bullet = [50e6] * 5
    fixed, zero = 0.045, 0.035
    pv_a = receiver_swap_pv(amort, fixed, zero)
    pv_b = receiver_swap_pv(bullet, fixed, zero)
    quoted("annual forward on the flat 3.5% continuous curve (%)", (math.exp(zero) - 1) * 100, 3.5620, 4)
    quoted("front-office PV, amortising (USD)", pv_a, 1_297_927, 0)
    quoted("downstream PV, bullet (USD)", pv_b, 2_113_914, 0)
    quoted("valuation break (USD)", pv_b - pv_a, 815_986, 0)
    quoted("break as a multiple of a 50,000 tolerance", (pv_b - pv_a) / 50_000, 16.3, 1)
    # Signature of a dropped schedule on a FLAT curve: every period has the same forward, so the PV ratio equals the
    # ratio of DF-weighted notionals (computed here without the pricer).
    w = [math.exp(-zero * i) for i in range(1, 6)]
    ratio = sum(n * d for n, d in zip(amort, w, strict=True)) / sum(n * d for n, d in zip(bullet, w, strict=True))
    assert abs(pv_a / pv_b - ratio) < 1e-12
    quoted("bullet PV over amortising PV (card sys-01-16)", pv_b / pv_a, 1.63, 2)
    # On a sloped curve the forwards differ by period and the signature fails (the note says it is a hint, not a proof).
    sloped = [0.02 + 0.006 * i for i in range(6)]  # hypothetical zero rates at 0..5 years

    def pv_sloped(notionals: list[float]) -> float:
        out = 0.0
        for i, n in enumerate(notionals, start=1):
            df_prev, df = math.exp(-sloped[i - 1] * (i - 1)), math.exp(-sloped[i] * i)
            out += n * (fixed - (df_prev / df - 1.0)) * df
        return out

    ws = [math.exp(-sloped[i] * i) for i in range(1, 6)]
    ratio_s = sum(n * d for n, d in zip(amort, ws, strict=True)) / sum(n * d for n, d in zip(bullet, ws, strict=True))
    assert abs(pv_sloped(amort) / pv_sloped(bullet) - ratio_s) > 0.1

    print("  Example 3: at-least-once delivery and ordering (seed 7, 10,000 trades, 12 partitions, 2% redelivery)")
    r = ordering_experiment()
    quoted("lifecycle events produced", r["events"], 14_033, 0)
    quoted("trades with at least one amendment", r["amended"], 3_732, 0)
    quoted("keyed, naive consumer: overbooked notional (%)", r["keyed_naive_overbooked_pct"], 2.1, 1)
    quoted("keyed, naive consumer: trades with wrong final notional", r["keyed_naive_wrong_final"], 0, 0)
    quoted("keyed, dedupe: overbooked notional (%)", r["keyed_dedupe_overbooked_pct"], 0.0, 1)
    quoted("unkeyed, dedupe without version guard: wrong final notional", r["unkeyed_dedupe_wrong_final"], 1_834, 0)
    quoted("unkeyed, dedupe with version guard: wrong final notional", r["unkeyed_dedupe_guard_wrong_final"], 0, 0)
    assert r["keyed_dedupe_guard_wrong_final"] == 0 and r["keyed_dedupe_wrong_final"] == 0

    print("  Lifecycle state machines")
    assert valid_path(LIFECYCLE, ["Pending", "Live", "Live", "PartiallyTerminated", "Novated"])
    assert not valid_path(LIFECYCLE, ["Pending", "Live", "Matured", "Live"])  # terminal states are final
    assert not valid_path(LIFECYCLE, ["Live", "Pending"])
    assert valid_path(CONFIRMATION, ["Unconfirmed", "Affirmed", "Confirmed", "Unconfirmed", "Affirmed", "Confirmed"])
    terminal = sorted(k for k, v in LIFECYCLE.items() if not v)
    assert terminal == ["Cancelled", "Exercised", "Matured", "Novated", "Rejected", "Terminated"]
    quoted("terminal lifecycle states", len(terminal), 6, 0)

    print(f"  {len(QUOTED)} numbers quoted in note 01 computed, printed and asserted")
    print("All front-to-back checks passed.")


if __name__ == "__main__":
    run_tests()
