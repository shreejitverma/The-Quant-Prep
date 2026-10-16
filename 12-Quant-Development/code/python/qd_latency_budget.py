"""Latency arithmetic for 12-Quant-Development/03-Low-Latency-Engineering.md.

Every number printed here is quoted in the note and asserted below:
1. Ethernet serialization delay (frame plus 8 bytes preamble/SFD plus 12 bytes inter-frame gap).
2. Propagation delay in fibre (stated group index 1.468) versus free space.
3. Tail amplification: the chance that a path of k stages hits at least one stage's p99.
4. Queueing: M/M/1 time in system as utilization rises (why you keep headroom).
5. An illustrative tick-to-trade budget built from stated assumptions.

Run: python3 12-Quant-Development/code/python/qd_latency_budget.py
"""

from __future__ import annotations

import math

C_KM_PER_S = 299_792.458  # speed of light in vacuum, exact by definition of the metre
FIBRE_GROUP_INDEX = 1.468  # stated assumption: typical single-mode fibre near 1550 nm
ETH_OVERHEAD_BYTES = 8 + 12  # preamble + start-of-frame delimiter, inter-frame gap


def serialization_ns(frame_bytes: int, gbps: float) -> float:
    """Time to clock one Ethernet frame onto the wire, including preamble and inter-frame gap."""
    return (frame_bytes + ETH_OVERHEAD_BYTES) * 8 / gbps  # bits / (Gbit/s) = ns


def propagation_us_per_km(index: float) -> float:
    return index / C_KM_PER_S * 1e6


def p_any_stage_over_p99(k: int, q: float = 0.99) -> float:
    return 1.0 - q**k


def mm1_time_in_system_ns(service_ns: float, utilization: float) -> float:
    """Mean time in an M/M/1 system: W = 1 / (mu - lambda) = service / (1 - rho)."""
    return service_ns / (1.0 - utilization)


def main() -> None:
    print("1. serialization delay (ns)")
    ser = {}
    for frame in (64, 1500):
        for gbps in (1.0, 10.0, 25.0):
            ser[(frame, gbps)] = serialization_ns(frame, gbps)
            print(f"   {frame:5d}-byte frame at {gbps:4.0f} GbE: {ser[(frame, gbps)]:8.2f} ns")
    assert math.isclose(ser[(64, 10.0)], 67.2)
    assert math.isclose(ser[(64, 1.0)], 672.0)
    assert math.isclose(ser[(64, 25.0)], 26.88)
    assert math.isclose(ser[(1500, 10.0)], 1216.0)
    assert math.isclose(ser[(1500, 1.0)], 12160.0)
    assert math.isclose(ser[(1500, 25.0)], 486.4)

    print("2. propagation delay")
    fibre = propagation_us_per_km(FIBRE_GROUP_INDEX)
    vacuum = propagation_us_per_km(1.0)
    print(f"   fibre (n = {FIBRE_GROUP_INDEX}): {fibre:.3f} us/km; free space: {vacuum:.3f} us/km")
    one_way_1000 = (1000 * fibre, 1000 * vacuum)
    print(f"   1000 km one way: fibre {one_way_1000[0] / 1000:.3f} ms, free space {one_way_1000[1] / 1000:.3f} ms")
    saving = 1 - vacuum / fibre
    print(f"   free-space path saves {saving:.1%} of the fibre delay over the same distance")
    assert math.isclose(fibre, 4.897, abs_tol=5e-4)
    assert math.isclose(vacuum, 3.336, abs_tol=5e-4)
    assert math.isclose(one_way_1000[0] / 1000, 4.897, abs_tol=5e-4)
    assert math.isclose(one_way_1000[1] / 1000, 3.336, abs_tol=5e-4)
    assert math.isclose(saving, 0.319, abs_tol=5e-4)
    ratio = one_way_1000[0] * 1000 / ser[(64, 10.0)]
    print(f"   1000 km of fibre vs serializing 64 bytes at 10 GbE: {ratio:,.0f} times longer")
    assert round(ratio) == 72_868

    print("3. tail amplification: P(at least one of k independent stages exceeds its own p99)")
    tails = {k: p_any_stage_over_p99(k) for k in (1, 5, 10, 100)}
    for k, p in tails.items():
        print(f"   k = {k:3d}: {p:.2%}")
    assert math.isclose(tails[5], 0.0490, abs_tol=5e-5)
    assert math.isclose(tails[10], 0.0956, abs_tol=5e-5)
    assert math.isclose(tails[100], 0.6340, abs_tol=5e-5)

    print("4. M/M/1 mean time in system, service 300 ns")
    mm1 = {rho: mm1_time_in_system_ns(300.0, rho) for rho in (0.5, 0.6, 0.9, 0.99)}
    for rho, w in mm1.items():
        print(f"   utilization {rho:4.2f}: {w:8.0f} ns  (arrival rate {rho / 300e-9 / 1e6:.2f} M msg/s)")
    assert math.isclose(mm1[0.5], 600.0)
    assert math.isclose(mm1[0.6], 750.0)
    assert math.isclose(mm1[0.9], 3000.0)
    assert math.isclose(mm1[0.99], 30000.0)
    for rho, rate in ((0.5, 1.67), (0.6, 2.00), (0.9, 3.00), (0.99, 3.30)):
        assert math.isclose(rho / 300e-9 / 1e6, rate, abs_tol=5e-3)
    assert math.isclose(tails[1], 0.01)

    print("5. illustrative software tick-to-trade budget (assumptions, not measurements)")
    budget_ns = {
        "NIC to user space via kernel bypass": 800,
        "decode one market-data message": 100,
        "update order book": 150,
        "strategy decision": 500,
        "pre-trade risk checks": 200,
        "encode order and hand to NIC": 250,
    }
    total = sum(budget_ns.values())
    for stage, ns in budget_ns.items():
        print(f"   {stage:<38} {ns:5d} ns  {ns / total:6.1%}")
    print(f"   {'total':<38} {total:5d} ns")
    assert total == 2000
    shares = [0.40, 0.05, 0.075, 0.25, 0.10, 0.125]
    assert all(math.isclose(ns / total, s) for ns, s in zip(budget_ns.values(), shares, strict=True))

    print("6. TLB reach of a hypothetical 1536-entry TLB = entries x page size")
    entries = 1536
    reach = {name: entries * size for name, size in (("4 KiB", 4 << 10), ("16 KiB", 16 << 10), ("2 MiB", 2 << 20), ("1 GiB", 1 << 30))}
    for name, r in reach.items():
        print(f"   {name:>6} pages: {r / (1 << 20):10,.0f} MiB")
    assert reach["4 KiB"] == 6 << 20 and reach["16 KiB"] == 24 << 20
    assert reach["2 MiB"] == 3 << 30 and reach["1 GiB"] == 1536 << 30
    print(f"   2 MiB pages cover {reach['2 MiB'] // reach['4 KiB']} times more memory than 4 KiB pages")
    assert reach["2 MiB"] // reach["4 KiB"] == 512
    print("all assertions passed")


if __name__ == "__main__":
    main()
