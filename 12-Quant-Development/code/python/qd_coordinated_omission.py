"""Coordinated omission, computed: the same server stall measured by a closed-loop and an open-loop load generator.

Used by 12-Quant-Development/03-Low-Latency-Engineering.md.
Deterministic (no randomness): a single FIFO server takes 50 us per request and freezes for 2 s
starting at t = 30 s; the load generator intends one request every 1 ms for 60 s.

- Closed loop (the naive benchmark): the generator waits for each response before sending the next,
  sending at the next scheduled slot after the response arrives; slots missed during the stall are
  silently skipped, and latency is measured from the actual send time.
- Open loop (the corrected benchmark): every request is issued at its intended time, and latency is
  measured from the intended time, so requests queued behind the stall are counted.

Run: python3 12-Quant-Development/code/python/qd_coordinated_omission.py
"""

from __future__ import annotations

import math

RUN_S = 60.0
INTERVAL_S = 0.001
SERVICE_S = 50e-6
STALL_START_S = 30.0
STALL_END_S = 32.0
N_SLOTS = round(RUN_S / INTERVAL_S)


def serve(arrival: float, server_free: float) -> float:
    """Completion time of a request arriving at `arrival` to a FIFO server free from `server_free`."""
    start = max(arrival, server_free)
    if STALL_START_S <= start < STALL_END_S:
        start = STALL_END_S
    return start + SERVICE_S


def closed_loop() -> list[float]:
    latencies = []
    server_free = 0.0
    slot = 0
    while slot < N_SLOTS:
        send = slot * INTERVAL_S
        done = serve(send, server_free)
        server_free = done
        latencies.append(done - send)
        slot = max(slot + 1, math.ceil(done / INTERVAL_S - 1e-9))  # next slot at or after the response
    return latencies


def open_loop() -> list[float]:
    latencies = []
    server_free = 0.0
    for slot in range(N_SLOTS):
        arrival = slot * INTERVAL_S
        done = serve(arrival, server_free)
        server_free = done
        latencies.append(done - arrival)
    return latencies


def pct(sample: list[float], q: float) -> float:
    """Nearest-rank percentile."""
    s = sorted(sample)
    rank = max(1, -(-round(q * 1000) * len(s) // 100_000))  # exact ceil(q% of n) for q with <= 3 decimals
    return s[rank - 1]


def describe(name: str, lat: list[float]) -> dict[str, float]:
    out = {
        "n": len(lat),
        "mean_ms": 1e3 * sum(lat) / len(lat),
        "p50_ms": 1e3 * pct(lat, 50),
        "p99_ms": 1e3 * pct(lat, 99),
        "p999_ms": 1e3 * pct(lat, 99.9),
        "max_ms": 1e3 * max(lat),
        "over_10ms": sum(1 for x in lat if x > 0.010),
    }
    print(
        f"{name:<11} samples {out['n']:6d}  mean {out['mean_ms']:8.4f} ms  p50 {out['p50_ms']:.4f}  "
        f"p99 {out['p99_ms']:.4f}  p99.9 {out['p999_ms']:9.4f}  max {out['max_ms']:9.4f} ms  >10ms {out['over_10ms']}"
    )
    return out


def main() -> None:
    naive = describe("closed loop", closed_loop())
    true = describe("open loop", open_loop())

    # Closed loop: one sample sees the stall, the 2 s of skipped slots vanish from the record.
    assert naive["n"] == 58_000, naive["n"]  # 30,000 before the stall, 1 during, 27,999 after
    assert naive["over_10ms"] == 1
    assert math.isclose(naive["max_ms"], 2000.05, abs_tol=1e-6)
    assert math.isclose(naive["p99_ms"], 0.05, abs_tol=1e-9)
    assert math.isclose(naive["p999_ms"], 0.05, abs_tol=1e-9)
    assert round(naive["mean_ms"], 4) == 0.0845, naive["mean_ms"]  # quoted mean, 4 decimals

    # Open loop: every request intended during the stall waits for it, then for the backlog to drain.
    assert true["n"] == 60_000
    assert math.isclose(true["max_ms"], 2000.05, abs_tol=1e-6)
    assert math.isclose(true["p50_ms"], 0.05, abs_tol=1e-9)
    assert math.isclose(true["p99_ms"], 1430.05, abs_tol=1e-6), true["p99_ms"]
    assert math.isclose(true["p999_ms"], 1943.05, abs_tol=1e-6), true["p999_ms"]
    assert round(true["mean_ms"], 4) == 35.1544, true["mean_ms"]  # quoted mean, 4 decimals
    assert true["over_10ms"] == 2_095, true["over_10ms"]

    ratio = true["p99_ms"] / naive["p99_ms"]
    print(f"p99 understated by a factor of {ratio:,.0f}")
    assert round(ratio) == 28_601
    print("all assertions passed")


if __name__ == "__main__":
    main()
