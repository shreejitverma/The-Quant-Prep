"""Non-functional architecture: Kahan summation, synchronous DR replication sizing, and Cloud FinOps.

Backs every number in `18-Pricing-and-Risk-Systems/16-Non-Functional-Design.md`.
Numerical truncation errors, DR replication bandwidths, and cloud unit economics are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_non_functional.py`.
"""

from __future__ import annotations

import math
import struct

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9 * max(1.0, abs(expected))
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def f32(x: float) -> float:
    """Convert a float to standard IEEE 754 32-bit single precision."""
    return struct.unpack("f", struct.pack("f", x))[0]


def test_kahan_summation() -> None:
    print("  1. Kahan compensated summation versus standard float32 addition")
    base = f32(100_000.0)
    addend = f32(0.0001)
    n = 1_000_000

    # Standard summation in float32
    naive_sum = base
    for _ in range(n):
        naive_sum = f32(naive_sum + addend)

    # Kahan summation in float32
    kahan_sum = base
    c = f32(0.0)
    for _ in range(n):
        y = f32(addend - c)
        t = f32(kahan_sum + y)
        c = f32(f32(t - kahan_sum) - y)
        kahan_sum = t

    quoted("naive float32 sum", naive_sum, 100_000.0, 1)
    quoted("Kahan float32 sum", kahan_sum, 100_100.0, 1)
    quoted("recovered precision ($)", kahan_sum - naive_sum, 100.0, 1)


def test_dr_replication_sizing() -> None:
    print("  2. Synchronous DR replication bandwidth (New York to Chicago)")
    rtt_ms = 7.8
    rtt_sec = rtt_ms / 1000.0
    tps = 4_500.0
    wal_kb = 1.8

    flow_kb_sec = tps * wal_kb
    flow_mb_sec = flow_kb_sec / 1000.0
    bandwidth_mbps = flow_mb_sec * 8.0
    burst_mult = 3.0
    required_mbps = bandwidth_mbps * burst_mult
    concurrent_streams = tps * rtt_sec

    quoted("round-trip latency RTT (ms)", rtt_ms, 7.8, 1)
    quoted("peak transactions per second", tps, 4_500.0, 0)
    quoted("transaction WAL payload (KB)", wal_kb, 1.8, 1)
    quoted("average data flow (MB/sec)", flow_mb_sec, 8.1, 1)
    quoted("average network bandwidth (Mbps)", bandwidth_mbps, 64.8, 1)
    quoted("required burst bandwidth (Mbps)", required_mbps, 194.4, 1)
    quoted("theoretical concurrent streams required", concurrent_streams, 35.1, 1)


def test_cloud_finops() -> None:
    print("  3. Cloud FinOps unit economics: On-Premises vs AWS Spot Bursting")
    vcpus_needed = 50_000
    vcpus_per_inst = 64
    instances = int(math.ceil(vcpus_needed / vcpus_per_inst))
    on_demand_rate = 3.57
    spot_rate = 1.14
    hourly_cost = instances * spot_rate
    annual_cost = hourly_cost * 250.0

    quoted("virtual cores required", vcpus_needed, 50_000.0, 0)
    quoted("instances required (c7i.16xlarge)", instances, 782.0, 0)
    quoted("on-demand hourly rate ($)", on_demand_rate, 3.57, 2)
    quoted("spot hourly rate ($)", spot_rate, 1.14, 2)
    quoted("hourly spot run cost ($)", hourly_cost, 891.48, 2)
    quoted("annual spot run cost ($)", annual_cost, 222_870.0, 0)

    # On-prem comparison
    capex = 3_500_000.0
    opex_annual = 450_000.0
    year1_onprem = capex + opex_annual
    savings_pct = ((year1_onprem - annual_cost) / year1_onprem) * 100.0

    quoted("year 1 on-premises capex + opex ($)", year1_onprem, 3_950_000.0, 0)
    quoted("cloud spot TCO savings (%)", savings_pct, 94.4, 1)


def main() -> None:
    print("Non-functional architecture checks")
    test_kahan_summation()
    test_dr_replication_sizing()
    test_cloud_finops()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All non-functional checks passed.")


if __name__ == "__main__":
    main()
