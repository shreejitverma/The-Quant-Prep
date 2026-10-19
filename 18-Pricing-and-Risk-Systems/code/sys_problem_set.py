"""Systems design problem set: every number in the six case studies, recomputed and cross-checked.

Backs every number in `18-Pricing-and-Risk-Systems/18-Systems-Design-Problem-Set.md`.

1. FRTB SbM sensitivity pipeline: record layout, payload and wire time, combiner savings, and the count of
   across-bucket aggregation terms using the bucket counts of MAR21 (Basel Framework) for the fixed-bucket risk classes.
2. Pre-deal exposure proxy: expected positive exposure of a normal netting-set value, a mean-shift Taylor proxy,
   and a variance-aware proxy for a trade that also changes the volatility, against the exact closed form, with the
   closed form itself checked by numerical integration.
3. EOD batch: critical path with the generic CPM of sys_eod_batch.py, floats checked by path enumeration, and a late
   amendment sub-DAG scheduled with release times (instead of adding its durations to the makespan).
4. Curve snapshot reads: utilisation and waiting time of one contended cache line (M/D/1) at different read rates.
5. Pre-trade gateway queue: M/M/1 mean, p99 and M/D/1 comparison, checked by Lindley-recursion simulation.
6. Grid scaling: Amdahl's law and the longest-task bound under longest-processing-time-first list scheduling.

All volumes, timings and prices are hypothetical teaching inputs; Basel bucket counts are cited in the note.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_problem_set.py`.
"""

from __future__ import annotations

import heapq
import math
import random
import struct
from statistics import NormalDist

from sys_eod_batch import Task, brute_force_floats, cpm

QUOTED: list[str] = []
N01 = NormalDist()


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. FRTB SbM sensitivity pipeline
# ============================================================================

# Fixed bucket counts from the Basel Framework: CSR non-securitisation 18 (MAR21.51), CSR securitisation CTP 16
# (MAR21.59), CSR securitisation non-CTP 25 (MAR21.62), equity 13 (MAR21.77), commodity 11 (MAR21.82).
# GIRR has one bucket per currency (MAR21.41) and FX one per currency pair against the reporting currency (MAR21.86):
# 10 of each here is a hypothetical portfolio.
BUCKETS = {"GIRR": 10, "CSR non-sec": 18, "CSR sec CTP": 16, "CSR sec non-CTP": 25, "Equity": 13, "Commodity": 11, "FX": 10}


def test_sbm_pipeline() -> None:
    print("  1. FRTB SbM sensitivity pipeline (hypothetical volumes)")
    positions, per_position = 500_000, 40
    records = positions * per_position
    quoted("sensitivity records (millions)", records / 1e6, 20.0, 1)
    # Natural alignment without packing: int64 trade id, float64 value, int32 risk factor, int16 bucket, uint16 flags.
    layout = "=qdihH"
    size = struct.calcsize(layout)
    quoted("record size (bytes)", size, 24, 0)
    assert struct.calcsize("@qdihH") == 24  # native alignment gives the same size: no padding needed in this order
    assert struct.calcsize("@qihdH") > 24  # the order of the original packed struct would need padding
    # Field offsets under natural alignment, computed from prefix sizes of the layout.
    offsets = [struct.calcsize("@" + "qdihH"[:k] + "0" + "qdihH"[k]) - struct.calcsize("@0" + "qdihH"[k]) for k in range(5)]
    assert offsets == [0, 8, 16, 20, 22], offsets
    print(f"    field offsets = {offsets}")
    payload_mb = records * size / 1e6
    quoted("payload (MB)", payload_mb, 480.0, 1)
    quoted("time at a 10 Gbit/s line rate (s)", payload_mb * 8 / 10_000.0, 0.384, 3)
    # Combiner: each of 500 workers nets its records by risk factor before sending (MAR21.4(2) netting).
    workers, factors_per_worker, net_record = 500, 20_000, 16  # hypothetical; 16 bytes = factor id + value
    quoted("combined payload (MB)", workers * factors_per_worker * net_record / 1e6, 160.0, 1)
    raw_grid = 500_000 * 1_000 * 8
    quoted("raw scenario grid, 500,000 positions x 1,000 scenarios (GB)", raw_grid / 1e9, 4.0, 1)
    squares = sum(b * b for b in BUCKETS.values())
    quoted("sum over risk classes of buckets squared", squares, 1695, 0)
    quoted("across-bucket terms: 3 scenarios x 3 measures", 3 * 3 * squares, 15_255, 0)
    total_b = sum(BUCKETS.values())
    quoted("total buckets", total_b, 103, 0)
    quoted("terms if all buckets were wrongly correlated across classes", 3 * 3 * total_b * total_b, 95_481, 0)


# ============================================================================
# 2. Pre-deal exposure proxy
# ============================================================================


def ee(mu: float, sigma: float) -> float:
    """E[max(V, 0)] for V ~ N(mu, sigma^2)."""
    z = mu / sigma
    return mu * N01.cdf(z) + sigma * N01.pdf(z)


def ee_numeric(mu: float, sigma: float, n: int = 20_000) -> float:
    """Composite Simpson integration of max(x, 0) times the normal density over mu +/- 12 sigma."""
    lo, hi = mu - 12 * sigma, mu + 12 * sigma
    h = (hi - lo) / n

    def f(x: float) -> float:
        return max(x, 0.0) * math.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))

    s = f(lo) + f(hi) + sum((4 if i % 2 else 2) * f(lo + i * h) for i in range(1, n))
    return s * h / 3


def test_pre_deal() -> None:
    print("  2. Pre-deal expected exposure proxy ($)")
    mu, sigma, v = 15e6, 8e6, 1.5e6
    z = mu / sigma
    quoted("z = mu / sigma", z, 1.875, 3)
    quoted("Phi(z)", N01.cdf(z), 0.969604, 6)
    quoted("phi(z)", N01.pdf(z), 0.068786, 6)
    base = ee(mu, sigma)
    assert abs(base - ee_numeric(mu, sigma)) < 1.0  # closed form agrees with numerical integration to a dollar
    quoted("baseline EE", base, 15_094_345, 0)
    first = N01.cdf(z) * v
    second = 0.5 * N01.pdf(z) / sigma * v * v
    quoted("Taylor first-order term", first, 1_454_405, 0)
    quoted("Taylor second-order term", second, 9_673, 0)
    quoted("Taylor increment", first + second, 1_464_079, 0)
    exact_new = ee(mu + v, sigma)
    quoted("exact new EE", exact_new, 16_557_360, 0)
    quoted("exact increment", exact_new - base, 1_463_015, 0)
    quoted("Taylor error", first + second - (exact_new - base), 1_063, 0)
    quoted("Taylor relative error (%)", 100 * (first + second - (exact_new - base)) / (exact_new - base), 0.07, 2)
    # Near the money, a hedging trade that also lowers the volatility: mu 2m, own sd 3m, correlation -0.6.
    mu2, s_t, rho = 2e6, 3e6, -0.6
    z2 = mu2 / sigma
    base2 = ee(mu2, sigma)
    quoted("near-the-money baseline EE", base2, 4_290_758, 0)
    sigma_new = math.sqrt(sigma**2 + 2 * rho * sigma * s_t + s_t**2)
    quoted("new netting-set sd", sigma_new, 6_648_308, 0)
    exact2 = ee(mu2 + v, sigma_new) - base2
    quoted("exact increment", exact2, 470_815, 0)
    shift = N01.cdf(z2) * v + 0.5 * N01.pdf(z2) / sigma * v * v
    quoted("mean-shift Taylor increment", shift, 952_435, 0)
    quoted("mean-shift Taylor error (%)", 100 * (shift - exact2) / exact2, 102.3, 1)
    dm, ds, p = v, sigma_new - sigma, N01.pdf(z2)
    first2 = N01.cdf(z2) * dm + p * ds  # dEE/dmu = Phi(z), dEE/dsigma = phi(z)
    quoted("first-order mean and vol proxy", first2, 375_403, 0)
    quoted("first-order mean and vol proxy error (%)", 100 * (first2 - exact2) / exact2, -20.3, 1)
    # Second order: d2/dmu2 = phi/sigma, d2/dmu dsigma = -z phi/sigma, d2/dsigma2 = z^2 phi/sigma.
    second2 = first2 + 0.5 * (p / sigma) * (dm * dm - 2 * z2 * dm * ds + z2 * z2 * ds * ds)
    quoted("second-order mean and vol proxy", second2, 457_038, 0)
    quoted("second-order proxy error (%)", 100 * (second2 - exact2) / exact2, -2.9, 1)
    # Finite-difference check of the analytic derivatives used above.
    h = 1e3
    assert abs((ee(mu2 + h, sigma) - ee(mu2 - h, sigma)) / (2 * h) - N01.cdf(z2)) < 1e-6
    assert abs((ee(mu2, sigma + h) - ee(mu2, sigma - h)) / (2 * h) - p) < 1e-6
    d2 = (ee(mu2 + h, sigma + h) - ee(mu2 + h, sigma - h) - ee(mu2 - h, sigma + h) + ee(mu2 - h, sigma - h)) / (4 * h * h)
    assert abs(d2 - (-z2 * p / sigma)) < 1e-9


# ============================================================================
# 3. EOD batch with a late amendment
# ============================================================================


def problem_dag() -> dict[str, Task]:
    ts = [
        Task("A", 15.0),  # market data snap
        Task("B", 20.0, ("A",)),  # curve calibration
        Task("C", 25.0),  # trade extraction
        Task("D", 50.0, ("B", "C")),  # pricing and Greeks
        Task("E", 35.0, ("D",)),  # Monte Carlo VaR and ES
        Task("F", 20.0, ("D",)),  # FRTB SbM aggregation
        Task("G", 25.0, ("D",)),  # P&L explain
        Task("H", 15.0, ("E", "F", "G")),  # ledger sign-off
    ]
    return {t.name: t for t in ts}


def test_batch() -> None:
    print("  3. EOD batch: critical path and a late amendment (minutes)")
    tasks = problem_dag()
    s = cpm(tasks)
    mk, floats, critical = brute_force_floats(tasks)
    assert mk == s.makespan and all(abs(floats[n] - s.slack[n]) < 1e-12 for n in tasks)
    assert critical == [["A", "B", "D", "E", "H"]], critical
    for name, ef in [("B", 35), ("C", 25), ("D", 85), ("E", 120), ("F", 105), ("G", 110)]:
        quoted(f"early finish of {name}", s.ef[name], ef, 0)
    quoted("start of H", s.es["H"], 120, 0)
    quoted("makespan", s.makespan, 135, 0)
    quoted("float of C (trade extraction)", s.slack["C"], 10, 0)
    quoted("float of F (FRTB aggregation)", s.slack["F"], 15, 0)
    quoted("float of G (P&L explain)", s.slack["G"], 10, 0)
    quoted("SLA headroom against 180 minutes", 180 - s.makespan, 45, 0)
    # 500 amendments arrive at t = 100 while E, F and G are running.
    late = dict(tasks)
    late["C2"] = Task("C2", 1.0, (), 100.0)  # extract the amendments
    late["D2"] = Task("D2", 3.5, ("B", "C2"))  # price them (burst queue)
    late["E2"] = Task("E2", 2.0, ("E", "D2"))  # merge scenario vectors, re-take VaR and ES
    late["F2"] = Task("F2", 1.0, ("F", "D2"))  # merge net sensitivities, recompute SbM
    late["G2"] = Task("G2", 1.0, ("G", "D2"))  # merge into P&L explain
    late["H"] = Task("H", 15.0, ("E2", "F2", "G2"))
    s2 = cpm(late)
    quoted("amendments priced by", s2.ef["D2"], 104.5, 1)
    quoted("makespan with amendments", s2.makespan, 137, 0)
    quoted("delay caused by the amendments", s2.makespan - s.makespan, 2, 0)
    quoted("naive serial estimate of the delay", 1.0 + 3.5 + 2.0 + 1.0, 7.5, 1)
    quoted("SLA headroom with amendments", 180 - s2.makespan, 43, 0)


# ============================================================================
# 4. Curve snapshot reads
# ============================================================================


def test_contention() -> None:
    print("  4. One contended cache line per read (hypothetical 100 ns per serialized update)")
    t_c = 100e-9
    for rate, rho_exp, wait_exp in [(1e4, 0.001, 0.05), (1e6, 0.1, 5.6), (5e6, 0.5, 50.0), (9e6, 0.9, 450.0)]:
        rho = rate * t_c
        wq_ns = rho * t_c / (2 * (1 - rho)) * 1e9  # M/D/1 mean wait
        quoted(f"utilisation at {rate:,.0f} reads/s", rho, rho_exp, 3)
        quoted(f"mean wait at {rate:,.0f} reads/s (ns)", wq_ns, wait_exp, 2 if wait_exp < 1 else 1)
    quoted("saturation read rate (millions per second)", 1 / t_c / 1e6, 10.0, 1)


# ============================================================================
# 5. Pre-trade gateway queue
# ============================================================================


def lindley(lam: float, mu: float, n: int, seed: int) -> tuple[float, float]:
    """FCFS single server with exponential arrivals and service; returns (mean sojourn, p99 sojourn) in seconds."""
    rng = random.Random(seed)
    w = 0.0
    soj = []
    for _ in range(n):
        s = rng.expovariate(mu)
        soj.append(w + s)
        a = rng.expovariate(lam)
        w = max(0.0, w + s - a)
    soj.sort()
    return sum(soj) / n, soj[int(0.99 * n)]


def test_queue() -> None:
    print("  5. Pre-trade gateway: M/M/1 and M/D/1 (service 10 microseconds)")
    service = 10e-6
    mu = 1 / service
    out = {}
    for rho, w_exp, wq_exp, p99_exp, md1_exp in [(0.70, 33.3, 23.3, 153.5, 11.7), (0.95, 200.0, 190.0, 921.0, 95.0)]:
        lam = rho * mu
        w = 1 / (mu - lam)
        quoted(f"rho {rho}: mean time in system (us)", w * 1e6, w_exp, 1)
        quoted(f"rho {rho}: mean wait (us)", (w - service) * 1e6, wq_exp, 1)
        p99 = math.log(100) / (mu - lam)
        quoted(f"rho {rho}: p99 time in system (us)", p99 * 1e6, p99_exp, 1)
        quoted(f"rho {rho}: M/D/1 mean wait (us)", rho * service / (2 * (1 - rho)) * 1e6, md1_exp, 1)
        n = 400_000 if rho < 0.9 else 2_000_000
        sim_w, sim_p99 = lindley(lam, mu, n, 7)
        assert abs(sim_w / w - 1) < 0.05 and abs(sim_p99 / p99 - 1) < 0.05, (rho, sim_w, sim_p99)
        print(f"    rho {rho}: simulated mean {sim_w * 1e6:.1f} us, p99 {sim_p99 * 1e6:.1f} us")
        out[rho] = w
    quoted("mean latency ratio 0.95 versus 0.70", out[0.95] / out[0.70], 6.0, 1)
    quoted("flow increase from 70k to 95k orders/s (%)", (95 / 70 - 1) * 100, 35.7, 1)


# ============================================================================
# 6. Grid scaling
# ============================================================================


def lpt_makespan(durations: list[float], workers: int) -> float:
    heap = [0.0] * workers
    for d in sorted(durations, reverse=True):
        t = heapq.heappop(heap)
        heapq.heappush(heap, t + d)
    return max(heap)


def test_scaling() -> None:
    print("  6. Grid scaling")
    f = 0.02
    for n, exp in [(128, 36.2), (1024, 47.7)]:
        quoted(f"Amdahl speedup with 2% serial work on {n} cores", 1 / (f + (1 - f) / n), exp, 1)
    quoted("Amdahl limit", 1 / f, 50.0, 1)
    tasks = [1.0] * 999 + [30.0]
    quoted("total work (minutes)", sum(tasks), 1029, 0)
    quoted("LPT makespan on 100 workers, one 30-minute task (minutes)", lpt_makespan(tasks, 100), 30, 0)
    split = [1.0] * 999 + [1.0] * 30
    quoted("LPT makespan after splitting it into 30 pieces (minutes)", lpt_makespan(split, 100), 11, 0)
    quoted("lower bound total / workers (minutes)", sum(split) / 100, 10.29, 2)


def main() -> None:
    print("Systems design problem set checks")
    test_sbm_pipeline()
    test_pre_deal()
    test_batch()
    test_contention()
    test_queue()
    test_scaling()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All problem set checks passed.")


if __name__ == "__main__":
    main()
