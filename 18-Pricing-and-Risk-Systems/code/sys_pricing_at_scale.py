"""Pricing at scale: grid sizing, Amdahl limits, stragglers, task granularity, tree reduction, transfers and caching.

Backs every number in `18-Pricing-and-Risk-Systems/06-Pricing-at-Scale.md`.
Portfolio sizes, per-valuation times, prices, overheads and failure rates are labelled-hypothetical teaching inputs;
the only external constants are the PCI Express 5.0 signalling rate (32 GT/s per lane) and 128b/130b encoding.
Simulations use fixed seeds and are quoted in the note as "about" their printed values.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_pricing_at_scale.py`.
"""

from __future__ import annotations

import heapq
import math
import random

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:.{decimals}f}")
    return value


# ============================================================================
# 1. Fan-out sizing
# ============================================================================


def fan_out(positions: int, scenarios: int, seconds_per_eval: float, window_s: float, overhead: float) -> dict[str, float]:
    evals = positions * scenarios
    core_s = evals * seconds_per_eval
    return {
        "evals": evals,
        "core_s": core_s,
        "core_h": core_s / 3600,
        "cores": core_s / window_s,
        "cores_with_overhead": core_s / window_s * overhead,
    }


def amdahl(serial_fraction: float, n: float) -> float:
    return 1.0 / (serial_fraction + (1.0 - serial_fraction) / n)


# ============================================================================
# 2. Stragglers and scheduling
# ============================================================================


def harmonic(n: int) -> float:
    return sum(1.0 / k for k in range(1, n + 1))


def expected_max_exponential_sim(n: int, trials: int, seed: int) -> float:
    rng = random.Random(seed)
    return sum(max(rng.expovariate(1.0) for _ in range(n)) for _ in range(trials)) / trials


def makespan(task_sizes: list[float], speeds: list[float], dynamic: bool, backup: bool = False) -> float:
    """Completion time of all tasks on workers of given speeds.

    Static: task i is pre-assigned to worker i mod W. Dynamic: an idle worker takes the next task from a queue.
    Backup: once the queue is empty, an idle worker re-runs the running task with the latest expected finish,
    and the task completes when either copy finishes (MapReduce backup tasks).
    """
    w = len(speeds)
    if not dynamic:
        load = [0.0] * w
        for i, s in enumerate(task_sizes):
            load[i % w] += s / speeds[i % w]
        return max(load)
    free = [(0.0, k) for k in range(w)]
    heapq.heapify(free)
    running: dict[int, tuple[float, float]] = {}  # task -> (start, finish) of its best copy
    finish_time = 0.0
    queue = list(range(len(task_sizes)))
    queue.reverse()
    while queue:
        t, k = heapq.heappop(free)
        task = queue.pop()
        end = t + task_sizes[task] / speeds[k]
        running[task] = (t, end)
        heapq.heappush(free, (end, k))
        finish_time = max(finish_time, end)
    if not backup:
        return max(e for _, e in running.values())
    # Speculative copies: each idle worker duplicates the running task with the latest finish.
    done = dict(running)
    while free:
        t, k = heapq.heappop(free)
        pending = [(e, task) for task, (_, e) in done.items() if e > t]
        if not pending:
            break
        e, task = max(pending)
        copy_end = t + task_sizes[task] / speeds[k]
        if copy_end < e:
            done[task] = (t, copy_end)
            heapq.heappush(free, (copy_end, k))
    return max(e for _, e in done.values())


def straggler_experiment(seed: int = 1, workers: int = 250, total_work: float = 250_000.0) -> dict[str, float]:
    rng = random.Random(seed)
    speeds = [0.2 if rng.random() < 0.02 else 1.0 for _ in range(workers)]  # 2% degraded nodes at a fifth of the speed
    ideal = total_work / sum(speeds)
    out = {"slow_nodes": sum(s < 1 for s in speeds), "ideal": ideal}
    for per_worker in (1, 20):
        n = workers * per_worker
        raw = [rng.lognormvariate(0.0, 1.0) for _ in range(n)]  # heavy-tailed task sizes
        scale = total_work / sum(raw)
        sizes = [x * scale for x in raw]
        out[f"static_{per_worker}"] = makespan(sizes, speeds, dynamic=False) / ideal
        out[f"dynamic_{per_worker}"] = makespan(sizes, speeds, dynamic=True) / ideal
        out[f"backup_{per_worker}"] = makespan(sizes, speeds, dynamic=True, backup=True) / ideal
    return out


# ============================================================================
# 3. Granularity, reduction, transfers and caches
# ============================================================================


def efficiency(trades_per_task: int, scenarios: int, seconds_per_eval: float, overhead_s: float) -> float:
    work = trades_per_task * scenarios * seconds_per_eval
    return work / (work + overhead_s)


def tree_reduce(vectors: list[list[float]]) -> tuple[list[float], int, int, int]:
    """Binary-tree sum; worker i keeps its index, so worker 0 ends as root. Returns sum, depth, messages, root fan-in."""
    level = list(enumerate(vectors))
    depth = messages = root_in = 0
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                (ka, va), (_, vb) = level[i], level[i + 1]
                messages += 1
                root_in += ka == 0
                nxt.append((ka, [a + b for a, b in zip(va, vb, strict=True)]))
            else:
                nxt.append(level[i])
        level = nxt
        depth += 1
    return level[0][1], depth, messages, root_in


def calibrations_on_cold_key(requests: int, arrival_window_ms: float, calibration_ms: float, coalesce: bool) -> int:
    """Requests for one uncached curve arrive uniformly in a window shorter than one calibration.

    Without coalescing every request that misses the cache starts its own calibration; with an in-flight map the
    first miss starts one and later requests wait on it.
    """
    cached_at = math.inf
    in_flight_until = -math.inf
    started = 0
    for r in range(requests):
        t = arrival_window_ms * r / requests
        if t >= cached_at:
            continue
        if coalesce and t < in_flight_until:
            continue
        started += 1
        in_flight_until = t + calibration_ms
        cached_at = min(cached_at, t + calibration_ms)
    return started


def historical_var(pnl: list[float], confidence: float) -> float:
    """Loss at the (1 - confidence) empirical quantile, taking the k-th worst with k = ceil(n (1 - confidence))."""
    k = math.ceil(len(pnl) * (1.0 - confidence) - 1e-12)
    return -sorted(pnl)[k - 1]


def pcie_gb_per_s(gt_per_s: float = 32.0, lanes: int = 16) -> float:
    """Per-direction payload bandwidth before protocol overheads: GT/s x lanes x 128/130 / 8 bits."""
    return gt_per_s * lanes * 128 / 130 / 8


def run_tests() -> None:
    print("Pricing at scale checks")

    print("  Fan-out sizing (hypothetical book)")
    f = fan_out(150_000, 1_200, 0.002, 1_800, 1.25)
    quoted("valuations", f["evals"] / 1e6, 180, 0)
    quoted("core-seconds", f["core_s"], 360_000, 0)
    quoted("core-hours", f["core_h"], 100, 0)
    quoted("cores for a 30-minute window", f["cores"], 200, 0)
    quoted("cores with 1.25x overhead", f["cores_with_overhead"], 250, 0)

    print("  Example 1: cloud burst sizing (hypothetical book and price)")
    c = fan_out(120_000, 300, 0.008, 1_200, 1.0)
    quoted("valuations (m)", c["evals"] / 1e6, 36, 0)
    quoted("core-seconds", c["core_s"], 288_000, 0)
    quoted("core-hours", c["core_h"], 80, 0)
    quoted("vCPUs for a 20-minute window", c["cores"], 240, 0)
    nodes = c["cores"] / 16
    quoted("16-vCPU nodes", nodes, 15, 0)
    buffered = math.ceil(nodes * 1.25)
    quoted("nodes with a 25% buffer", buffered, 19, 0)
    quoted("vCPUs provisioned", buffered * 16, 304, 0)
    price = 0.05  # hypothetical USD per vCPU-hour
    per_run = buffered * 16 * price * 20 / 60
    quoted("cost per run at a hypothetical 0.05 per vCPU-hour (USD)", per_run, 5.07, 2)
    quoted("cost per year over 252 runs (USD)", per_run * 252, 1_276.80, 2)
    quoted("utilisation of the provisioned vCPUs", c["core_s"] / (buffered * 16 * 1_200), 0.789, 3)

    print("  Amdahl's law (hypothetical 5% serial fraction)")
    quoted("speed-up on 250 cores", amdahl(0.05, 250), 18.6, 1)
    quoted("speed-up on 1,000 cores", amdahl(0.05, 1_000), 19.6, 1)
    quoted("limit", 1 / 0.05, 20, 0)
    quoted("speed-up on 250 cores with a 0.5% serial fraction", amdahl(0.005, 250), 111.4, 1)

    print("  Stragglers")
    quoted("H_250: expected max of 250 unit exponentials", harmonic(250), 6.10, 2)
    quoted("simulated, 2,000 trials, seed 3", expected_max_exponential_sim(250, 2_000, 3), 6.1, 1)
    s = straggler_experiment()
    quoted("degraded nodes among 250 (seed 1)", s["slow_nodes"], 7, 0)
    quoted("static, 1 task per worker: makespan over ideal", s["static_1"], 19.6, 1)
    quoted("dynamic, 1 task per worker", s["dynamic_1"], 19.6, 1)
    quoted("static, 20 tasks per worker", s["static_20"], 6.6, 1)
    quoted("dynamic, 20 tasks per worker", s["dynamic_20"], 1.9, 1)
    quoted("dynamic with backup copies, 20 tasks per worker", s["backup_20"], 1.7, 1)

    print("  Task granularity (hypothetical 1,200 scenarios at 2 ms, 2 s overhead per task)")
    quoted("work per trade per task (s, card sys-06-12)", 1_200 * 0.002, 2.4, 1)
    for b, e in ((1, 0.545), (10, 0.923), (100, 0.992), (1_000, 0.999)):
        quoted(f"efficiency with {b} trades per task", efficiency(b, 1_200, 0.002, 2.0), e, 3)

    print("  Example 2: tree reduction and VaR (seed 9)")
    rng = random.Random(9)
    vectors = [[rng.gauss(0.0, 1_000.0) for _ in range(1_000)] for _ in range(100)]
    tree, depth, messages, root_in = tree_reduce(vectors)
    central = [sum(v[s] for v in vectors) for s in range(1_000)]
    assert max(abs(a - b) for a, b in zip(tree, central, strict=True)) < 1e-6
    quoted("tree depth for 100 workers", depth, 7, 0)
    quoted("messages in the tree reduction", messages, 99, 0)
    quoted("vectors received by the root in the tree", root_in, 7, 0)
    quoted("bytes per 1,000-scenario vector (float64, KB)", 1_000 * 8 / 1e3, 8, 0)
    var99 = historical_var(tree, 0.99)
    assert var99 == historical_var(central, 0.99) or abs(var99 - historical_var(central, 0.99)) < 1e-6
    quoted("99% VaR as the 10th worst of 1,000", var99, 24_562, 0)
    quoted("99% VaR as the 11th worst", -sorted(tree)[10], 23_773, 0)

    print("  Host to device transfers (PCIe 5.0 x16)")
    bw = pcie_gb_per_s()
    quoted("PCIe 5.0 x16 per direction before protocol overhead (GB/s)", bw, 63.0, 1)
    trades_mb = 150_000 * 2_000 / 1e6
    quoted("trade data at 2 KB per trade (MB)", trades_mb, 300, 0)
    quoted("one transfer of the trades (ms)", trades_mb / 1e3 / bw * 1e3, 4.76, 2)
    scen_mb = 1_200 * 5_000 * 8 / 1e6
    quoted("scenario set, 1,200 x 5,000 factors (MB)", scen_mb, 48, 0)
    quoted("one transfer of the scenarios (ms)", scen_mb / 1e3 / bw * 1e3, 0.76, 2)
    quoted("resending the trades for every scenario (s)", 1_200 * trades_mb / 1e3 / bw, 5.71, 2)

    print("  Caching (hypothetical latencies)")
    for h, lat in ((0.90, 5.08), (0.99, 0.59), (0.999, 0.14)):
        quoted(f"mean curve fetch at {h:.1%} hit rate (ms)", h * 0.09 + (1 - h) * 50.0, lat, 2)
    quoted(
        "calibrations for 2,000 requests in 10 ms, 50 ms calibration, no coalescing",
        calibrations_on_cold_key(2_000, 10, 50, False),
        2_000,
        0,
    )
    quoted("same with request coalescing", calibrations_on_cold_key(2_000, 10, 50, True), 1, 0)

    print(f"  {len(QUOTED)} numbers quoted in note 06 computed, printed and asserted")
    print("All pricing at scale checks passed.")


if __name__ == "__main__":
    run_tests()
