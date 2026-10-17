"""Market-making system design numbers: latency budgets, queueing, bursts, latency races and a pre-trade risk gate.

Backs every number in ``11-Market-Making-Systems-Architecture.md``.
Run ``uv run --no-project --with numpy python 08-Market-Making/code/mm_system_design.py``;
each printed number is asserted, so drift in the note fails CI.

Every latency, rate and limit below is a hypothetical input chosen for the examples, not a measurement of any firm or venue.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from statistics import NormalDist

import numpy as np

PHI = NormalDist()


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<66s} {value:14.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


# hypothetical software tick-to-trade budget, microseconds: (stage, p50, p99)
BUDGET = [
    ("NIC receive and kernel-bypass poll", 0.8, 1.5),
    ("feed decode and sequence check", 0.4, 0.9),
    ("book update", 0.3, 0.8),
    ("fair value update", 0.6, 1.6),
    ("quote decision", 0.4, 1.0),
    ("pre-trade risk checks", 0.3, 0.6),
    ("order encode and session layer", 0.5, 1.1),
    ("NIC transmit", 0.8, 1.5),
]


def section_budget() -> None:
    """Backs Example 1 and card mm-sys-p99-sum."""
    print("\n1. hypothetical tick-to-trade budget")
    p50 = check("sum of stage medians (us)", sum(b[1] for b in BUDGET), 4.1, 1e-9)
    p99 = check("sum of stage p99s (us)", sum(b[2] for b in BUDGET), 9.0, 1e-9)
    check("share of median spent outside strategy logic (percent)", (p50 - 0.6 - 0.4) / p50 * 100, 75.6098, 5e-5)
    # lognormal stages matched to each (p50, p99): mu = ln p50, s = ln(p99/p50) / z_0.99
    z99 = PHI.inv_cdf(0.99)
    mus = np.log([b[1] for b in BUDGET])
    sds = np.log([b[2] / b[1] for b in BUDGET]) / z99
    rng = np.random.default_rng(17)
    n = 1_000_000
    z = rng.standard_normal((n, len(BUDGET)))
    indep = np.exp(mus + sds * z).sum(axis=1)
    comon = np.exp(mus + sds * z[:, :1]).sum(axis=1)  # one shock drives every stage
    check("end-to-end p99, independent stages (us, seed 17)", float(np.quantile(indep, 0.99)), 5.8177, 5e-4)
    check("end-to-end p99, perfectly correlated stages (us, seed 17)", float(np.quantile(comon, 0.99)), 9.0006, 5e-4)
    check("end-to-end median, independent stages (us, seed 17)", float(np.median(indep)), 4.3041, 5e-4)
    # exact comonotone p99: every stage at its own p99 simultaneously
    assert abs(sum(math.exp(m + s * z99) for m, s in zip(mus, sds, strict=True)) - p99) < 1e-9


def md1_wait(lam: float, service: float) -> float:
    """Pollaczek-Khinchine mean queueing delay for M/D/1: rho / (2 mu (1 - rho))."""
    rho = lam * service
    return rho * service / (2 * (1 - rho))


def simulate_md1(lam: float, service: float, n: int, seed: int) -> float:
    """Lindley recursion W_{n+1} = max(0, W_n + S - A_{n+1}) with Poisson arrivals and fixed service."""
    rng = np.random.default_rng(seed)
    gaps = rng.exponential(1 / lam, n)
    w, total = 0.0, 0.0
    for a in gaps:
        total += w
        w = max(0.0, w + service - a)
    return total / n


def section_queueing() -> None:
    """Backs Examples 2 and 3 and cards mm-sys-md1, mm-sys-microburst, mm-sys-utilisation."""
    print("\n2. queueing in a feed handler: Poisson arrivals, fixed 400 ns per message")
    service = 400e-9
    check("capacity 1 / service (million msgs/s)", 1 / service / 1e6, 2.5, 1e-9)
    for rate, util, expected in ((2.0e6, 0.80, 800.0), (2.375e6, 0.95, 3800.0)):
        rho = check(f"utilisation at {rate / 1e6:.3f}m msgs/s", rate * service, util, 1e-12)
        check(f"M/D/1 mean wait at rho = {rho:.2f} (ns)", md1_wait(rate, service) * 1e9, expected, 1e-6)
    check("load increase from 2.0m to 2.375m msgs/s (percent)", (2.375 / 2.0 - 1) * 100, 18.75, 1e-9)
    check("ratio of mean waits rho 0.95 vs 0.80", md1_wait(2.375e6, service) / md1_wait(2.0e6, service), 4.75, 1e-9)
    sim = simulate_md1(2.0e6, service, 400_000, seed=3) * 1e9
    check("simulated mean wait at rho = 0.80 (ns, seed 3)", sim, 800.0, 25.0)
    check("simulated mean wait at rho = 0.80 (ns, seed 3), printed", sim, 793.6318, 5e-4)
    # microburst: 10,000 messages in 1 ms against 2,500 served per ms
    burst, window = 10_000, 1e-3
    served = window / service
    backlog = check("backlog at the end of a 10,000-message 1 ms burst", burst - served, 7500.0, 1e-6)
    check("time to drain the backlog (ms)", backlog * service * 1e3, 3.0, 1e-9)
    check("ring buffer slots: next power of two", 2 ** math.ceil(math.log2(backlog)), 8192, 0)


def section_race() -> None:
    """Backs Example 4 and card mm-sys-race-probability."""
    print("\n3. latency races: cancel before you are picked off")
    # your cancel latency ~ N(6, 1) us, the fastest taker's ~ N(5, 1) us, independent
    p_lose = check("P(taker beats your cancel) = Phi((6 - 5) / sqrt 2)", PHI.cdf(1 / math.sqrt(2)), 0.7602, 5e-5)
    rng = np.random.default_rng(23)
    mc = float(np.mean(rng.normal(6, 1, 1_000_000) > rng.normal(5, 1, 1_000_000)))
    check("simulated P(lose race) (seed 23)", mc, 0.7598, 5e-5)
    check("P(lose) after cutting 1 us (equal means)", PHI.cdf(0.0), 0.5, 1e-12)
    check("P(lose) after cutting 2 us", PHI.cdf(-1 / math.sqrt(2)), 0.2398, 5e-5)
    events, lots, tick_value = 500, 2, 12.50
    check("daily pick-off cost: 500 events x P x 2 lots x 12.50", events * p_lose * lots * tick_value, 9503.1242, 5e-3)
    check("daily saving from cutting 1 us", events * (p_lose - 0.5) * lots * tick_value, 3253.1242, 5e-3)


@dataclass
class Order:
    side: int  # +1 buy, -1 sell
    qty: int
    price: float
    t: float  # seconds


@dataclass
class RiskGate:
    """Pre-trade checks in the order an exchange-facing gate would run them; returns a reason or 'ok'."""

    max_qty: int = 500
    collar: float = 0.02  # reject prices more than 2% from the reference
    max_long: int = 1_000
    max_short: int = 1_000
    max_notional: float = 2_000_000.0
    rate: float = 100.0  # token refill per second
    burst: float = 20.0  # bucket size
    position: int = 0
    open_buy: int = 0
    open_sell: int = 0
    tokens: float = 20.0
    last_t: float = 0.0
    killed: bool = False

    def submit(self, o: Order, ref: float) -> str:
        if self.killed:
            return "killed"
        self.tokens = min(self.burst, self.tokens + (o.t - self.last_t) * self.rate)
        self.last_t = o.t
        if self.tokens < 1.0:
            return "throttle"
        self.tokens -= 1.0
        if o.qty <= 0 or o.qty > self.max_qty:
            return "max_qty"
        if abs(o.price / ref - 1) > self.collar:
            return "collar"
        if o.qty * o.price > self.max_notional:
            return "notional"
        if o.side > 0 and self.position + self.open_buy + o.qty > self.max_long:
            return "worst_case_long"
        if o.side < 0 and -(self.position - self.open_sell - o.qty) > self.max_short:
            return "worst_case_short"
        if o.side > 0:
            self.open_buy += o.qty
        else:
            self.open_sell += o.qty
        return "ok"


def run_gate(orders: list[Order]) -> list[str]:
    gate = RiskGate(position=800, open_buy=150)
    return [gate.submit(o, ref=100.0) for o in orders]


def section_risk_gate() -> None:
    """Backs Example 5 and cards mm-sys-worst-case-position, mm-sys-determinism."""
    print("\n4. pre-trade risk gate")
    scripted = [
        Order(+1, 100, 100.00, 0.000),  # worst case 800 + 150 + 100 = 1050 > 1000
        Order(+1, 50, 100.00, 0.001),  # worst case exactly 1000: allowed
        Order(-1, 600, 100.00, 0.002),  # above max_qty
        Order(-1, 100, 103.00, 0.003),  # 3% away from the reference
        Order(-1, 400, 99.50, 0.004),  # fine
    ]
    out = run_gate(scripted)
    print("   ", out)
    assert out == ["worst_case_long", "ok", "max_qty", "collar", "ok"], out
    # token bucket: 50 small orders in 10 ms (one every 0.2 ms) against bucket 20, refill 100/s
    burst = [Order(-1 if i % 2 else 1, 1, 100.0, 0.0002 * i) for i in range(50)]
    gate2 = RiskGate()
    res = [gate2.submit(o, 100.0) for o in burst]
    check("orders accepted out of a 50-order burst in 10 ms", res.count("ok"), 20, 0)
    # determinism: replaying the same event log gives a byte-identical decision log
    h1 = hashlib.sha256(repr(run_gate(scripted)).encode()).hexdigest()
    h2 = hashlib.sha256(repr(run_gate(scripted)).encode()).hexdigest()
    assert h1 == h2


def detect_gaps(seqs: list[int]) -> tuple[list[int], int]:
    """Return missing sequence numbers and the count of duplicates dropped, for a feed starting at seqs[0]."""
    expected, missing, dups, seen = seqs[0], [], 0, set()
    for s in seqs:
        if s in seen or s < expected:
            dups += 1
            continue
        if s > expected:
            missing.extend(range(expected, s))
        seen.add(s)
        expected = s + 1
    return missing, dups


def section_gaps() -> None:
    """Backs Example 6 and card mm-sys-gap-handling."""
    print("\n5. feed sequence gaps")
    seqs = [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 15, 16, 17, 18, 19, 20]
    missing, dups = detect_gaps(seqs)
    print("    missing", missing, "duplicates", dups)
    assert missing == [7, 8] and dups == 1
    check("messages to request from the retransmission service", len(missing), 2, 0)


if __name__ == "__main__":
    section_budget()
    section_queueing()
    section_race()
    section_risk_gate()
    section_gaps()
    print("\nall checks passed")
