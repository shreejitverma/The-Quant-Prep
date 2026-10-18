"""Systems design problem set: queueing latency, grid memory, pre-deal XVA proxy, and batch critical path.

Backs every number in `18-Pricing-and-Risk-Systems/18-Systems-Design-Problem-Set.md`.
Queueing latencies, FRTB SbM memory sizing, Taylor series XVA approximations, CPM batch schedules, and lock contention are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_problem_set.py`.
"""

from __future__ import annotations

import math

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def normal_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)


def normal_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def test_queueing_latency() -> None:
    print("  1. Pre-Trade Gateway M/M/1 Queueing Model and Congestion Sizing")
    service_time_micros = 10.0
    mu = 1_000_000.0 / service_time_micros  # 100,000 orders/sec

    # Case A: 70% utilization
    rho_a = 0.70
    lambda_a = rho_a * mu  # 70,000 orders/sec
    w_a_sec = 1.0 / (mu - lambda_a)
    w_a_micros = w_a_sec * 1_000_000.0
    wq_a_micros = w_a_micros - service_time_micros
    p99_a_micros = (math.log(100.0) / (mu - lambda_a)) * 1_000_000.0

    quoted("service time (microseconds)", service_time_micros, 10.0, 1)
    quoted("service rate mu (orders/sec)", mu, 100_000.0, 0)
    quoted("utilization rho (case A)", rho_a, 0.70, 2)
    quoted("average system latency W (case A, micros)", w_a_micros, 33.3, 1)
    quoted("average queue wait time Wq (case A, micros)", wq_a_micros, 23.3, 1)
    quoted("p99 latency (case A, micros)", p99_a_micros, 153.5, 1)

    # Case B: 95% utilization
    rho_b = 0.95
    lambda_b = rho_b * mu  # 95,000 orders/sec
    w_b_sec = 1.0 / (mu - lambda_b)
    w_b_micros = w_b_sec * 1_000_000.0
    wq_b_micros = w_b_micros - service_time_micros
    p99_b_micros = (math.log(100.0) / (mu - lambda_b)) * 1_000_000.0
    latency_expansion = w_b_micros / w_a_micros

    quoted("utilization rho (case B)", rho_b, 0.95, 2)
    quoted("average system latency W (case B, micros)", w_b_micros, 200.0, 1)
    quoted("average queue wait time Wq (case B, micros)", wq_b_micros, 190.0, 1)
    quoted("p99 latency (case B, micros)", p99_b_micros, 921.0, 1)
    quoted("queue congestion expansion factor", latency_expansion, 6.0, 1)


def test_frtb_grid_sizing() -> None:
    print("  2. FRTB SbM Grid Compute and Network Bandwidth Sizing")
    positions = 500_000
    avg_greeks_per_pos = 40
    total_sensitivities = positions * avg_greeks_per_pos  # 20,000,000

    struct_bytes = 24  # 8 (trade_id) + 4 (risk_factor_id) + 2 (bucket_id) + 8 (value) + 2 pad
    total_bytes = total_sensitivities * struct_bytes
    total_mb = total_bytes / 1_000_000.0

    wire_speed_gbps = 10.0
    wire_speed_mb_sec = (wire_speed_gbps * 1_000.0) / 8.0  # 1,250 MB/sec
    transfer_seconds = total_mb / wire_speed_mb_sec  # 0.384 seconds

    # SbM correlation matrix multiplications
    risk_classes = 7
    buckets_per_class = 15
    total_buckets = risk_classes * buckets_per_class  # 105
    scenarios = 3
    multiplications = scenarios * (total_buckets**2)  # 3 * 11025 = 33075

    quoted("total sensitivities generated (millions)", total_sensitivities / 1e6, 20.0, 1)
    quoted("packed struct size (bytes)", struct_bytes, 24.0, 0)
    quoted("total sensitivity payload (MB)", total_mb, 480.0, 1)
    quoted("wire speed (MB/sec)", wire_speed_mb_sec, 1_250.0, 1)
    quoted("network transfer time (seconds)", transfer_seconds, 0.384, 3)
    quoted("total buckets firm-wide", total_buckets, 105.0, 0)
    quoted("across-bucket matrix operations", multiplications, 33_075.0, 0)


def test_pre_deal_xva_proxy() -> None:
    print("  3. Pre-Deal Incremental XVA Analytical Taylor Proxy vs Full Expectation")
    e_v_base = 15_000_000.0
    sigma_base = 8_000_000.0
    v_trade = 1_500_000.0

    z_base = e_v_base / sigma_base  # 1.875
    phi_base = normal_pdf(z_base)  # 0.068786
    phi_cdf_base = normal_cdf(z_base)  # 0.969604

    # Baseline expected positive exposure E[V+] = sigma * [z * Phi(z) + phi(z)]
    epe_base = sigma_base * (z_base * phi_cdf_base + phi_base)

    # Taylor expansion: Delta EPE approx Phi(z) * v + 0.5 * (phi(z) / sigma) * v^2
    first_order = phi_cdf_base * v_trade
    second_order = 0.5 * (phi_base / sigma_base) * (v_trade**2)
    delta_epe_taylor = first_order + second_order

    # Exact new expected positive exposure
    e_v_new = e_v_base + v_trade  # 16,500,000
    z_new = e_v_new / sigma_base  # 2.0625
    phi_new = normal_pdf(z_new)
    phi_cdf_new = normal_cdf(z_new)
    epe_new = sigma_base * (z_new * phi_cdf_new + phi_new)
    delta_epe_exact = epe_new - epe_base

    abs_error = abs(delta_epe_taylor - delta_epe_exact)
    pct_error = (abs_error / delta_epe_exact) * 100.0

    quoted("standardized z-score base", z_base, 1.875, 3)
    quoted("baseline expected positive exposure ($)", epe_base, 15_094_345.0, 0)
    quoted("Taylor first-order increment ($)", first_order, 1_454_405.0, 0)
    quoted("Taylor second-order increment ($)", second_order, 9_673.0, 0)
    quoted("Taylor total incremental EPE ($)", delta_epe_taylor, 1_464_079.0, 0)
    quoted("exact new expected positive exposure ($)", epe_new, 16_557_360.0, 0)
    quoted("exact incremental EPE ($)", delta_epe_exact, 1_463_015.0, 0)
    quoted("Taylor approximation absolute error ($)", abs_error, 1_063.0, 0)
    quoted("Taylor approximation relative error (%)", pct_error, 0.07, 2)


def test_eod_batch_critical_path() -> None:
    print("  4. EOD Batch Critical Path and Sub-DAG Invalidation Sizing")
    # Task durations in minutes:
    dur_a = 15.0  # Market Data Snap
    dur_b = 20.0  # Multi-Curve Calibration (depends on A)
    dur_c = 25.0  # Trade Extraction & Normalization
    dur_d = 50.0  # Pricing & Greek Grid (depends on B, C)
    dur_e = 35.0  # Monte Carlo VaR/ES (depends on D)
    dur_f = 20.0  # FRTB SbM Aggregation (depends on D)
    dur_g = 25.0  # PnL Explain (depends on D)
    dur_h = 15.0  # General Ledger Sign-off (depends on E, F, G)

    path1_cpm = dur_a + dur_b + dur_d + dur_e + dur_h  # 15 + 20 + 50 + 35 + 15 = 135 min
    path2 = dur_c + dur_d + dur_e + dur_h  # 25 + 50 + 35 + 15 = 125 min

    float_c = path1_cpm - path2  # 10 min
    float_f = dur_e - dur_f  # 35 - 20 = 15 min
    float_g = dur_e - dur_g  # 35 - 25 = 10 min

    # Late trade sub-DAG re-run
    sub_c = 1.0
    sub_d = 3.5
    sub_e = 2.0
    sub_h = 1.0
    sub_rerun_delay = sub_c + sub_d + sub_e + sub_h  # 7.5 min
    total_batch_time = path1_cpm + sub_rerun_delay  # 142.5 min
    batch_sla = 180.0  # 3 hours
    sla_slack = batch_sla - total_batch_time  # 37.5 min

    quoted("critical path runtime (minutes)", path1_cpm, 135.0, 1)
    quoted("trade extraction float (minutes)", float_c, 10.0, 1)
    quoted("FRTB SbM float (minutes)", float_f, 15.0, 1)
    quoted("PnL explain float (minutes)", float_g, 10.0, 1)
    quoted("sub-DAG late trade rerun runtime (minutes)", sub_rerun_delay, 7.5, 1)
    quoted("total batch runtime with recovery (minutes)", total_batch_time, 142.5, 1)
    quoted("remaining batch SLA slack (minutes)", sla_slack, 37.5, 1)


def test_reactive_curve_cache_contention() -> None:
    print("  5. Reactive Curve Service: Shared Mutex vs Lock-Free Atomic shared_ptr")
    queries_per_sec = 10_000.0
    threads = 64

    # Mutex contention overhead
    mutex_contention_micros = 4.8
    mutex_total_overhead_sec = (queries_per_sec * mutex_contention_micros) / 1_000_000.0  # 0.048 s
    mutex_overhead_ms = mutex_total_overhead_sec * 1000.0  # 48.0 ms

    # Atomic shared_ptr overhead
    atomic_read_micros = 0.025  # 25 nanoseconds
    atomic_total_overhead_sec = (queries_per_sec * atomic_read_micros) / 1_000_000.0  # 0.00025 s
    atomic_overhead_ms = atomic_total_overhead_sec * 1000.0  # 0.25 ms

    speedup_factor = mutex_contention_micros / atomic_read_micros  # 192.0

    quoted("queries per second", queries_per_sec, 10_000.0, 0)
    quoted("concurrent reader threads", threads, 64.0, 0)
    quoted("mutex acquisition latency under contention (micros)", mutex_contention_micros, 4.8, 1)
    quoted("mutex total contention overhead (ms/sec)", mutex_overhead_ms, 48.0, 1)
    quoted("atomic shared_ptr latency (micros)", atomic_read_micros, 0.025, 3)
    quoted("atomic total read overhead (ms/sec)", atomic_overhead_ms, 0.25, 2)
    quoted("lock-free contention reduction factor", speedup_factor, 192.0, 1)


def main() -> None:
    print("=== sys_problem_set: Quantitative Financial Systems Design ===")
    test_queueing_latency()
    test_frtb_grid_sizing()
    test_pre_deal_xva_proxy()
    test_eod_batch_critical_path()
    test_reactive_curve_cache_contention()
    print(f"\nSuccessfully verified {len(QUOTED)} systems design problem figures.")


if __name__ == "__main__":
    main()
