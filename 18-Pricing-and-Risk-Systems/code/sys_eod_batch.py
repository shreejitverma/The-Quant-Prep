"""EOD risk batch: critical path method, SLA headroom, stochastic durations, late trades, failover and idempotency.

Backs every number in `18-Pricing-and-Risk-Systems/13-EOD-Risk-Batch.md`.

1. A generic critical path method (CPM) on a task DAG with optional release times: topological order, forward pass
   (early start and finish), backward pass (late start and finish) and total float.
   Checked against brute-force enumeration of every source-to-sink path.
2. Crashing the critical path: diminishing returns once a second path becomes critical.
3. Stochastic durations (PERT bias): with mean-preserving noise on every task, every path keeps its mean length but the
   expected makespan rises, because the makespan is a maximum over paths.
   A zero-noise control run isolates the noise as the cause.
4. A late trade: full rerun versus an incremental sub-DAG that prices one trade and merges additive vectors.
5. Lease-based scheduler failover: closed-form best and worst case, checked by simulating the crash phase.
6. Retry semantics: an append-only write double counts a retried task; a keyed upsert does not.

All durations, times, lease settings and positions are hypothetical teaching inputs.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_eod_batch.py`.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

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
# 1. Critical path method
# ============================================================================


@dataclass(frozen=True)
class Task:
    name: str
    duration: float
    preds: tuple[str, ...] = ()
    release: float = 0.0  # earliest allowed start (for example, when an input arrives)


@dataclass(frozen=True)
class Schedule:
    order: list[str]
    es: dict[str, float]
    ef: dict[str, float]
    ls: dict[str, float]
    lf: dict[str, float]
    slack: dict[str, float]
    makespan: float


def topological_order(tasks: dict[str, Task]) -> list[str]:
    """Kahn's algorithm with a sorted ready set, so the order is deterministic; raises on a cycle."""
    indeg = {n: len(t.preds) for n, t in tasks.items()}
    succs: dict[str, list[str]] = {n: [] for n in tasks}
    for n, t in tasks.items():
        for p in t.preds:
            if p not in tasks:
                raise KeyError(f"{n} depends on unknown task {p}")
            succs[p].append(n)
    ready = sorted(n for n, d in indeg.items() if d == 0)
    order: list[str] = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for s in succs[n]:
            indeg[s] -= 1
            if indeg[s] == 0:
                ready.append(s)
                ready.sort()
    if len(order) != len(tasks):
        raise ValueError("dependency cycle")
    return order


def cpm(tasks: dict[str, Task]) -> Schedule:
    """Forward and backward pass; float = LS - ES."""
    order = topological_order(tasks)
    es: dict[str, float] = {}
    ef: dict[str, float] = {}
    for n in order:
        t = tasks[n]
        es[n] = max([t.release] + [ef[p] for p in t.preds])
        ef[n] = es[n] + t.duration
    makespan = max(ef.values())
    succs: dict[str, list[str]] = {n: [] for n in tasks}
    for n, t in tasks.items():
        for p in t.preds:
            succs[p].append(n)
    lf: dict[str, float] = {}
    ls: dict[str, float] = {}
    for n in reversed(order):
        lf[n] = min([ls[s] for s in succs[n]], default=makespan)
        ls[n] = lf[n] - tasks[n].duration
    slack = {n: ls[n] - es[n] for n in tasks}
    return Schedule(order, es, ef, ls, lf, slack, makespan)


def all_paths(tasks: dict[str, Task]) -> list[list[str]]:
    """Every source-to-sink path, by depth-first enumeration (brute force, independent of the passes)."""
    succs: dict[str, list[str]] = {n: [] for n in tasks}
    for n, t in tasks.items():
        for p in t.preds:
            succs[p].append(n)
    sources = [n for n, t in tasks.items() if not t.preds]
    paths: list[list[str]] = []

    def walk(node: str, acc: list[str]) -> None:
        acc = acc + [node]
        if not succs[node]:
            paths.append(acc)
            return
        for s in succs[node]:
            walk(s, acc)

    for s in sources:
        walk(s, [])
    return paths


def brute_force_floats(tasks: dict[str, Task]) -> tuple[float, dict[str, float], list[list[str]]]:
    """Makespan = longest path; float of a task = makespan - longest full path through it (no release times)."""
    paths = all_paths(tasks)
    length = {tuple(p): sum(tasks[n].duration for n in p) for p in paths}
    makespan = max(length.values())
    through = {n: max(v for p, v in length.items() if n in p) for n in tasks}
    critical = [list(p) for p, v in length.items() if v == makespan]
    return makespan, {n: makespan - through[n] for n in tasks}, critical


def example_dag() -> dict[str, Task]:
    """The worked example: an Americas fixed income batch (durations in minutes)."""
    ts = [
        Task("A", 15.0),  # trade extract and normalisation
        Task("B", 25.0),  # market snapshot and curve calibration
        Task("C", 20.0, ("B",)),  # vol surface calibration
        Task("D", 45.0, ("A", "B", "C")),  # sensitivity grid
        Task("E", 60.0, ("A", "B")),  # full revaluation scenario grid
        Task("F", 15.0, ("E",)),  # VaR and ES aggregation
        Task("G", 20.0, ("D", "F")),  # P&L explain and sign-off
    ]
    return {t.name: t for t in ts}


def test_cpm() -> Schedule:
    print("  1. Critical path method on the worked-example DAG (minutes)")
    tasks = example_dag()
    s = cpm(tasks)
    expected = {
        # name: (ES, EF, LS, LF, float)
        "A": (0, 15, 10, 25, 10),
        "B": (0, 25, 0, 25, 0),
        "C": (25, 45, 35, 55, 10),
        "D": (45, 90, 55, 100, 10),
        "E": (25, 85, 25, 85, 0),
        "F": (85, 100, 85, 100, 0),
        "G": (100, 120, 100, 120, 0),
    }
    for n, (es, ef, ls, lf, fl) in expected.items():
        quoted(f"task {n} ES", s.es[n], es, 0)
        quoted(f"task {n} EF", s.ef[n], ef, 0)
        quoted(f"task {n} LS", s.ls[n], ls, 0)
        quoted(f"task {n} LF", s.lf[n], lf, 0)
        quoted(f"task {n} float", s.slack[n], fl, 0)
    quoted("makespan (minutes)", s.makespan, 120, 0)

    # Independent check: brute-force path enumeration.
    mk, floats, critical = brute_force_floats(tasks)
    assert mk == s.makespan
    assert all(abs(floats[n] - s.slack[n]) < 1e-12 for n in tasks)
    assert critical == [["B", "E", "F", "G"]], critical
    print(f"    critical path (brute force) = {' -> '.join(critical[0])}")
    quoted("number of source-to-sink paths", len(all_paths(tasks)), 5, 0)
    # The near-critical path that caps the benefit of crashing E.
    quoted("length of path B-C-D-G (minutes)", sum(tasks[n].duration for n in "BCDG"), 110, 0)
    return s


def test_crashing() -> None:
    print("  2. Crashing task E: diminishing returns")
    for new_e, expected_makespan in [(60.0, 120.0), (55.0, 115.0), (50.0, 110.0), (40.0, 110.0), (30.0, 110.0)]:
        tasks = example_dag()
        tasks["E"] = Task("E", new_e, ("A", "B"))
        quoted(f"makespan with E = {new_e:.0f} min", cpm(tasks).makespan, expected_makespan, 0)
    # Doubling the cores on D (halving D) changes nothing: D has 10 minutes of float.
    tasks = example_dag()
    tasks["D"] = Task("D", 22.5, ("A", "B", "C"))
    quoted("makespan with D halved", cpm(tasks).makespan, 120, 0)
    # After E is cut to 50, both paths are critical: shortening only E no longer helps.
    tasks = example_dag()
    tasks["E"] = Task("E", 50.0, ("A", "B"))
    s = cpm(tasks)
    crit = sorted(n for n in tasks if abs(s.slack[n]) < 1e-12)
    assert crit == ["B", "C", "D", "E", "F", "G"], crit
    print(f"    zero-float tasks with E = 50 min = {''.join(crit)}")


def test_sla_headroom(s: Schedule) -> None:
    print("  3. SLA headroom (batch starts 18:00, sign-off deadline 20:30, both hypothetical)")
    window = 150.0
    quoted("window (minutes)", window, 150, 0)
    quoted("deterministic headroom (minutes)", window - s.makespan, 30, 0)


# ============================================================================
# 3. Stochastic durations: PERT bias
# ============================================================================


def simulate_makespans(tasks: dict[str, Task], sigma: float, n_sims: int, seed: int) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Each duration is multiplied by an independent lognormal factor with mean 1 (so every path keeps its mean)."""
    rng = np.random.default_rng(seed)
    order = topological_order(tasks)
    dur = {n: tasks[n].duration * np.exp(sigma * rng.standard_normal(n_sims) - 0.5 * sigma * sigma) for n in order}
    ef: dict[str, np.ndarray] = {}
    for n in order:
        start = np.zeros(n_sims)
        for p in tasks[n].preds:
            start = np.maximum(start, ef[p])
        ef[n] = start + dur[n]
    makespan = np.max(np.vstack([ef[n] for n in order]), axis=0)
    return makespan, dur


def test_pert_bias() -> None:
    print("  4. Stochastic durations: expected makespan versus deterministic CPM (seed 2026, 200,000 runs)")
    tasks = example_dag()
    n_sims = 200_000
    control, _ = simulate_makespans(tasks, 0.0, n_sims, 2026)
    assert np.all(np.abs(control - 120.0) < 1e-9)  # zero-noise control reproduces CPM exactly
    mk, dur = simulate_makespans(tasks, 0.25, n_sims, 2026)
    crit_len = dur["B"] + dur["E"] + dur["F"] + dur["G"]
    se_crit = float(np.std(crit_len) / np.sqrt(n_sims))
    se_mk = float(np.std(mk) / np.sqrt(n_sims))
    # The critical path alone keeps its mean (within Monte Carlo error) ...
    assert abs(float(np.mean(crit_len)) - 120.0) < 4.0 * se_crit
    quoted("mean length of path B-E-F-G (minutes)", float(np.mean(crit_len)), 120.0, 1)
    # ... but the makespan, a maximum over paths, does not.
    mean_mk = float(np.mean(mk))
    assert mean_mk - 120.0 > 20.0 * se_mk
    quoted("mean makespan (minutes)", mean_mk, 124.0, 1)
    quoted("95th percentile makespan (minutes)", float(np.quantile(mk, 0.95)), 153.0, 1)
    quoted("probability makespan exceeds the 150-minute window (%)", 100.0 * float(np.mean(mk > 150.0)), 6.6, 1)


# ============================================================================
# 4. Late trade: full rerun versus incremental sub-DAG
# ============================================================================


def clock(minutes_after_start: float, start_minutes: int = 18 * 60) -> str:
    """Wall-clock time for a batch that starts at 18:00 (hypothetical)."""
    total = start_minutes + int(round(minutes_after_start))
    return f"{total // 60:02d}:{total % 60:02d}"


def test_late_trade() -> None:
    print("  5. Late trade arriving 95 minutes into the batch")
    arrival = 95.0
    base = example_dag()
    # Option 1: rerun everything from the arrival time.
    rerun = {n: Task(t.name, t.duration, t.preds, arrival) for n, t in base.items()}
    full = cpm(rerun).makespan
    quoted("full rerun completion (minutes after start)", full, 215, 0)
    assert clock(arrival) == "19:35" and clock(full) == "21:35" and clock(120.0) == "20:00"
    print(f"    arrival {clock(arrival)}, full rerun done {clock(full)}, original sign-off {clock(120.0)}")
    # Option 2: price the trade alone, then merge additive vectors into the aggregates already built.
    inc = dict(base)
    inc["L"] = Task("L", 0.75, ("B", "C"), arrival)  # sensitivities and scenario P&L vector for one trade (45 s)
    inc["F2"] = Task("F2", 1.0, ("F", "L"))  # add the trade's scenario vector, re-take the VaR and ES quantiles
    inc["G2"] = Task("G2", 1.5, ("G", "L"))  # merge Greeks into P&L explain, re-run sign-off checks
    s = cpm(inc)
    quoted("trade priced at (minutes after start)", s.ef["L"], 95.75, 2)
    quoted("incremental completion (minutes after start)", s.makespan, 121.5, 1)
    quoted("delay added by the late trade (minutes)", s.makespan - 120.0, 1.5, 1)
    quoted("headroom left in the 150-minute window (minutes)", 150.0 - s.makespan, 28.5, 1)
    # Additivity check that justifies the merge: scenario P&L adds across trades, VaR does not.
    rng = np.random.default_rng(7)
    book = rng.standard_normal(500) * 1e6
    trade = -0.6 * book + rng.standard_normal(500) * 2e5  # a partial hedge

    def var99(x: np.ndarray) -> float:
        return float(-np.quantile(x, 0.01))

    merged = var99(book + trade)
    assert merged < var99(book) + var99(trade)  # VaR of the sum is not the sum of VaRs
    assert merged < var99(book)  # the hedge reduces VaR, so a VaR increment cannot be added naively
    print(f"    VaR(book) = {var99(book):,.0f}, VaR(trade) = {var99(trade):,.0f}, VaR(book + trade) = {merged:,.0f}")


# ============================================================================
# 5. Lease-based failover
# ============================================================================


def test_failover() -> None:
    print("  6. Active-passive scheduler failover with a lease (TTL 15 s, renew every 5 s, poll every 2 s, recover 8 s)")
    ttl, renew, poll, recover = 15.0, 5.0, 2.0, 8.0
    best = (ttl - renew) + 0.0 + recover  # crash just before a renewal; standby polls at expiry
    worst = ttl + poll + recover  # crash just after a renewal; standby just missed a poll
    mean = (ttl - renew / 2.0) + poll / 2.0 + recover
    quoted("mean detection delay (s)", ttl - renew / 2.0, 12.5, 1)
    quoted("best-case failover (s)", best, 18, 0)
    quoted("worst-case failover (s)", worst, 25, 0)
    quoted("mean failover, uniform crash phase (s)", mean, 21.5, 1)
    # Independent check: simulate the renewal and polling clocks.
    rng = random.Random(11)
    samples = []
    for _ in range(100_000):
        crash = rng.uniform(0.0, 1000.0)
        last_renewal = renew * int(crash // renew)  # renewals at 0, 5, 10, ... (lease renewed at each)
        expiry = last_renewal + ttl
        phase = rng.uniform(0.0, poll)  # the standby's poll clock is independent of the leader's
        k = int(max(0.0, expiry - phase) // poll)
        first_poll = phase + k * poll
        if first_poll < expiry:
            first_poll += poll
        samples.append(first_poll + recover - crash)
    assert min(samples) >= best - 1e-9 and max(samples) <= worst + 1e-9
    sim_mean = sum(samples) / len(samples)
    assert abs(sim_mean - mean) < 0.05, sim_mean
    print(f"    simulated mean failover = {sim_mean:.2f} s (min {min(samples):.2f}, max {max(samples):.2f})")


# ============================================================================
# 6. Retry semantics
# ============================================================================


def test_idempotency() -> None:
    print("  7. A task that commits and then crashes before acknowledging is retried")
    rows = [("2026-01-15", "RATES-NY", "USD-SOFR-5Y", 1500.0), ("2026-01-15", "RATES-NY", "USD-SOFR-10Y", -700.0)]
    rows.append(("2026-01-15", "RATES-NY", "USD-SOFR-30Y", 2200.0))
    append_table: list[tuple[str, str, str, float]] = []
    upsert_table: dict[tuple[str, str, str], float] = {}
    for _attempt in range(2):  # original run plus one retry
        append_table.extend(rows)
        for d, book, rf, dv01 in rows:
            upsert_table[(d, book, rf)] = dv01
    quoted("true DV01 of the book ($ per bp)", sum(r[3] for r in rows), 3000, 0)
    quoted("DV01 after retry, append-only table", sum(r[3] for r in append_table), 6000, 0)
    quoted("DV01 after retry, keyed upsert", sum(upsert_table.values()), 3000, 0)


def main() -> None:
    print("EOD risk batch checks")
    s = test_cpm()
    test_crashing()
    test_sla_headroom(s)
    test_pert_bias()
    test_late_trade()
    test_failover()
    test_idempotency()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All EOD risk batch checks passed.")


if __name__ == "__main__":
    main()
