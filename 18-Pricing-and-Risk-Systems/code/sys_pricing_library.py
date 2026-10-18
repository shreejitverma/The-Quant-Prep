"""Pricing library architecture: instrument/engine/observer pattern, reverse-mode AD on a tape, and determinism.

Backs every number in `18-Pricing-and-Risk-Systems/05-Pricing-Library-Architecture.md`.

1. Observable quotes and curves, lazy instruments and pluggable engines (the QuantLib design reduced to its core),
   with the "forward the first notification only" rule of QuantLib's LazyObject, and counts of calculations and
   notifications.
2. A tape-based reverse-mode automatic differentiation (AAD) engine: the elementary-node example, a swap gradient with
   respect to 40 zero rates checked against the analytic gradient, operation counts versus finite differences and
   forward mode, and a Monte Carlo pathwise delta and vega checked against Black-Scholes.
3. Floating-point non-associativity and a reduction whose result does not depend on how work is split.
4. Finite differences versus AAD cost and tape memory, from labelled-hypothetical inputs.

Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_pricing_library.py`.
"""

from __future__ import annotations

import math
import random
import statistics
from abc import ABC, abstractmethod
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
# 1. Observer, lazy object, instrument and engine
# ============================================================================


class Observable:
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self.notifications_sent = 0

    def register_observer(self, obs: Observer) -> None:
        if obs not in self._observers:
            self._observers.append(obs)

    def notify_observers(self) -> None:
        for obs in list(self._observers):
            self.notifications_sent += 1
            obs.update()


class Observer(ABC):
    @abstractmethod
    def update(self) -> None: ...


class SimpleQuote(Observable):
    def __init__(self, value: float) -> None:
        super().__init__()
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    def set_value(self, v: float) -> None:
        if v != self._value:
            self._value = v
            self.notify_observers()


class LazyObject(Observable, Observer):
    """Cache results; on update, forward a notification only if the cache was valid (QuantLib's default rule)."""

    def __init__(self) -> None:
        Observable.__init__(self)
        self._calculated = False
        self._updating = False
        self.calculations = 0

    def update(self) -> None:
        if self._updating:  # recursion guard against observer cycles
            return
        self._updating = True
        try:
            if self._calculated:
                self._calculated = False
                self.notify_observers()
        finally:
            self._updating = False

    def calculate(self) -> None:
        if not self._calculated:
            self._calculated = True
            try:
                self.calculations += 1
                self.perform_calculations()
            except Exception:
                self._calculated = False
                raise

    @abstractmethod
    def perform_calculations(self) -> None: ...


class FlatCurve(LazyObject):
    """A 'curve' built from one quote; stands in for a bootstrapped term structure."""

    def __init__(self, quote: SimpleQuote) -> None:
        super().__init__()
        self.quote = quote
        quote.register_observer(self)
        self._rate = 0.0

    def perform_calculations(self) -> None:
        self._rate = self.quote.value

    def discount(self, t: float) -> float:
        self.calculate()
        return math.exp(-self._rate * t)


class PricingEngine(ABC):
    @abstractmethod
    def calculate(self, args: dict[str, float]) -> dict[str, float]: ...


class DiscountingBondEngine(PricingEngine):
    def __init__(self, curve: FlatCurve) -> None:
        self.curve = curve

    def calculate(self, args: dict[str, float]) -> dict[str, float]:
        c, n, mat = args["coupon"], args["notional"], int(args["maturity"])
        pv = sum(c * n * self.curve.discount(t) for t in range(1, mat + 1)) + n * self.curve.discount(mat)
        return {"npv": pv}


class FixedRateBond(LazyObject):
    """Holds terms only; packages them as arguments for whichever engine is attached."""

    def __init__(self, notional: float, coupon: float, maturity: int) -> None:
        super().__init__()
        self.args = {"notional": notional, "coupon": coupon, "maturity": float(maturity)}
        self.engine: PricingEngine | None = None
        self._npv = 0.0

    def set_engine(self, engine: DiscountingBondEngine) -> None:
        self.engine = engine
        engine.curve.register_observer(self)
        self._calculated = False

    def perform_calculations(self) -> None:
        if self.engine is None:
            raise ValueError("no pricing engine set")
        self._npv = self.engine.calculate(dict(self.args))["npv"]

    def npv(self) -> float:
        self.calculate()
        return self._npv


def observer_demo() -> dict[str, float]:
    q = SimpleQuote(0.04)
    curve = FlatCurve(q)
    bonds = [FixedRateBond(1e6, 0.05, m) for m in range(1, 11)]
    eng = DiscountingBondEngine(curve)
    for b in bonds:
        b.set_engine(eng)
    first = sum(b.npv() for b in bonds)
    for _ in range(1000):  # repeated requests with no market change hit the cache
        sum(b.npv() for b in bonds)
    after_cache = sum(b.calculations for b in bonds)
    q.set_value(0.041)  # first update: curve was calculated, so it notifies the 10 bonds
    q.set_value(0.042)  # second update before anyone recalculated: the curve is already dirty, nothing forwarded
    q.set_value(0.043)
    sent_curve = curve.notifications_sent
    final = sum(b.npv() for b in bonds)
    return {
        "npv_4pct": first,
        "npv_4_3pct": final,
        "calcs_after_1001_requests": after_cache,
        "curve_calcs": curve.calculations,
        "curve_notifications": sent_curve,
        "bond_calcs_total": sum(b.calculations for b in bonds),
    }


# ============================================================================
# 2. Reverse-mode AD on a tape
# ============================================================================


class Tape:
    def __init__(self) -> None:
        self.nodes: list[tuple[tuple[int, ...], tuple[float, ...]]] = []  # (parents, local partials)

    def push(self, parents: tuple[int, ...], partials: tuple[float, ...]) -> int:
        self.nodes.append((parents, partials))
        return len(self.nodes) - 1

    def gradient(self, out: int, seed: float = 1.0) -> tuple[list[float], int]:
        """Reverse sweep: adjoint_j += adjoint_k * dv_k/dv_j; returns adjoints and the number of multiply-adds."""
        adj = [0.0] * len(self.nodes)
        adj[out] = seed
        ops = 0
        for k in range(out, -1, -1):
            a = adj[k]
            if a == 0.0:
                continue
            parents, partials = self.nodes[k]
            for p, d in zip(parents, partials, strict=True):
                adj[p] += a * d
                ops += 1
        return adj, ops


class Var:
    __slots__ = ("idx", "tape", "val")

    def __init__(self, tape: Tape, val: float, parents: tuple[int, ...] = (), partials: tuple[float, ...] = ()) -> None:
        self.tape, self.val = tape, val
        self.idx = tape.push(parents, partials)

    # Constants (floats) are not recorded: an operation with a constant has one parent on the tape.
    def __add__(self, o: Var | float) -> Var:
        if isinstance(o, Var):
            return Var(self.tape, self.val + o.val, (self.idx, o.idx), (1.0, 1.0))
        return Var(self.tape, self.val + o, (self.idx,), (1.0,))

    __radd__ = __add__

    def __sub__(self, o: Var | float) -> Var:
        if isinstance(o, Var):
            return Var(self.tape, self.val - o.val, (self.idx, o.idx), (1.0, -1.0))
        return Var(self.tape, self.val - o, (self.idx,), (1.0,))

    def __rsub__(self, o: float) -> Var:
        return Var(self.tape, o - self.val, (self.idx,), (-1.0,))

    def __mul__(self, o: Var | float) -> Var:
        if isinstance(o, Var):
            return Var(self.tape, self.val * o.val, (self.idx, o.idx), (o.val, self.val))
        return Var(self.tape, self.val * o, (self.idx,), (o,))

    __rmul__ = __mul__


def vexp(x: Var) -> Var:
    e = math.exp(x.val)
    return Var(x.tape, e, (x.idx,), (e,))


def vmax0(x: Var) -> Var:
    return Var(x.tape, max(x.val, 0.0), (x.idx,), (1.0 if x.val > 0 else 0.0,))


def swap_pv(z: list, times: list[float], fixed: float, notional: float, exp=math.exp):
    """Receiver swap on a zero curve: receive fixed quarterly, pay floating (= 1 - D(T) per unit notional).

    The same code prices with floats (exp=math.exp) or records a tape (Var inputs, exp=vexp).
    """
    dfs = [exp(zi * (-t)) for zi, t in zip(z, times, strict=True)]
    pv = 0.0
    for df in dfs:
        pv = pv + df * (fixed * 0.25 * notional)
    return pv - (1.0 - dfs[-1]) * notional


def aad_swap(n_pillars: int = 40) -> dict[str, float]:
    times = [0.25 * (i + 1) for i in range(n_pillars)]
    zeros = [0.03 + 0.0005 * i for i in range(n_pillars)]
    fixed, notional = 0.045, 100e6
    tape = Tape()
    zv = [Var(tape, zi) for zi in zeros]
    start = len(tape.nodes)
    pv = swap_pv(zv, times, fixed, notional, exp=vexp)
    fwd_nodes = len(tape.nodes) - start
    adj, rev_ops = tape.gradient(pv.idx)
    grad = [adj[v.idx] for v in zv]
    analytic = [-t * fixed * 0.25 * notional * math.exp(-z * t) for z, t in zip(zeros, times, strict=True)]
    analytic[-1] -= times[-1] * notional * math.exp(-zeros[-1] * times[-1])
    err = max(abs(a - b) for a, b in zip(grad, analytic, strict=True))
    # Finite differences: one bumped revaluation per pillar plus the base.
    h = 1e-7
    base = swap_pv(zeros, times, fixed, notional)
    fd = []
    for i in range(n_pillars):
        zb = list(zeros)
        zb[i] += h
        fd.append((swap_pv(zb, times, fixed, notional) - base) / h)
    fd_err = max(abs(a - b) / max(abs(b), 1.0) for a, b in zip(fd, analytic, strict=True))
    return {
        "pv": pv.val,
        "pv01_total": sum(grad) * 1e-4,
        "grad_err": err,
        "fd_rel_err": fd_err,
        "forward_nodes": fwd_nodes,
        "reverse_ops": rev_ops,
        "fd_evals": n_pillars + 1,
        "fwd_mode_passes": n_pillars,
        "last_bucket": grad[-1] * 1e-4,
    }


def bs_call(s: float, k: float, r: float, sig: float, t: float) -> tuple[float, float, float]:
    nd = NormalDist()
    d1 = (math.log(s / k) + (r + 0.5 * sig * sig) * t) / (sig * math.sqrt(t))
    d2 = d1 - sig * math.sqrt(t)
    price = s * nd.cdf(d1) - k * math.exp(-r * t) * nd.cdf(d2)
    return price, nd.cdf(d1), s * nd.pdf(d1) * math.sqrt(t)


def aad_monte_carlo(n_paths: int, seed: int) -> dict[str, float]:
    """European call by Monte Carlo on one tape; delta and vega from one reverse sweep (pathwise derivatives)."""
    rng = random.Random(seed)
    tape = Tape()
    s0, vol = Var(tape, 100.0), Var(tape, 0.2)
    k, r, t = 100.0, 0.03, 1.0
    half_var = vol * vol * (0.5 * t)  # recorded once, shared by every path
    sq = math.sqrt(t)
    total = 0.0
    payoffs = []
    for _ in range(n_paths):
        zz = rng.gauss(0.0, 1.0)
        st = s0 * vexp((r * t) - half_var + vol * (sq * zz))
        pay = vmax0(st - k)
        payoffs.append(pay.val)
        total = total + pay
    price = total * (math.exp(-r * t) / n_paths)
    adj, _ = tape.gradient(price.idx)
    bs, bs_delta, bs_vega = bs_call(100.0, k, r, 0.2, t)
    se = math.exp(-r * t) * statistics.stdev(payoffs) / math.sqrt(n_paths)
    return {
        "price": price.val,
        "se": se,
        "delta": adj[s0.idx],
        "vega": adj[vol.idx],
        "bs_price": bs,
        "bs_delta": bs_delta,
        "bs_vega": bs_vega,
        "nodes": len(tape.nodes),
    }


def elementary_node() -> tuple[float, float, float]:
    tape = Tape()
    v1, v2 = Var(tape, 3.0), Var(tape, 4.0)
    v3 = v1 * v2
    adj, _ = tape.gradient(v3.idx, seed=2.5)
    return v3.val, adj[v1.idx], adj[v2.idx]


# ============================================================================
# 3. Determinism
# ============================================================================


def chunked_sum(xs: list[float], chunks: int) -> float:
    """What a parallel reduction does: sum each chunk, then sum the partial sums."""
    n = len(xs)
    parts = [sum(xs[i * n // chunks : (i + 1) * n // chunks]) for i in range(chunks)]
    return sum(parts)


def fixed_tree_sum(xs: list[float], block: int = 1024) -> float:
    """Sum fixed-size blocks in index order, then combine block sums pairwise in a fixed tree.

    Any worker count can compute the blocks; the result depends only on the data and `block`.
    """
    level = [sum(xs[i : i + block]) for i in range(0, len(xs), block)]
    while len(level) > 1:
        level = [level[i] + level[i + 1] if i + 1 < len(level) else level[i] for i in range(0, len(level), 2)]
    return level[0]


def determinism_demo(seed: int = 42, n: int = 1_000_000) -> dict[str, float]:
    rng = random.Random(seed)
    xs = [rng.uniform(-1.0, 1.0) * 10.0 ** rng.randint(-6, 12) for _ in range(n)]
    exact = math.fsum(xs)
    by_chunks = {c: chunked_sum(xs, c) for c in (1, 8, 16, 64)}
    distinct = len(set(by_chunks.values()))
    worst = max(abs(v - exact) for v in by_chunks.values())
    tree = fixed_tree_sum(xs)
    # The fixed tree gives the same bits whichever way the blocks are farmed out.
    blocks = [sum(xs[i : i + 1024]) for i in range(0, n, 1024)]
    shuffled_order = list(range(len(blocks)))
    random.Random(7).shuffle(shuffled_order)
    recomputed = [0.0] * len(blocks)
    for i in shuffled_order:
        recomputed[i] = blocks[i]
    level = recomputed
    while len(level) > 1:
        level = [level[i] + level[i + 1] if i + 1 < len(level) else level[i] for i in range(0, len(level), 2)]
    assert level[0] == tree
    return {"distinct_chunk_results": distinct, "worst_abs_err": worst, "tree_abs_err": abs(tree - exact), "exact": exact}


def run_tests() -> None:
    print("Pricing library architecture checks")

    print("  Example 1: observer pattern and lazy evaluation")
    o = observer_demo()
    quoted("10 bonds NPV at 4% (sum, USD)", o["npv_4pct"], 10_432_712, 0)
    quoted("bond calculations after 1,001 portfolio requests", o["calcs_after_1001_requests"], 10, 0)
    quoted("curve notifications for three quote updates", o["curve_notifications"], 10, 0)
    quoted("curve calculations in total", o["curve_calcs"], 2, 0)
    quoted("bond calculations in total", o["bond_calcs_total"], 20, 0)
    quoted("10 bonds NPV at 4.3% (sum, USD)", o["npv_4_3pct"], 10_282_258, 0)

    print("  Example 2: the elementary reverse-sweep node")
    v3, a1, a2 = elementary_node()
    quoted("v3 = v1 * v2", v3, 12.0, 1)
    quoted("adjoint of v1 with output adjoint 2.5", a1, 10.0, 1)
    quoted("adjoint of v2 with output adjoint 2.5", a2, 7.5, 1)

    print("  Example 3: AAD gradient of a 10y quarterly receiver swap to 40 zero rates")
    s = aad_swap(40)
    quoted("swap PV (USD)", s["pv"], -2_567_094, 0)
    quoted("sum of bucketed PV01s (USD per bp)", s["pv01_total"], -78_158, 0)
    quoted("10y bucket PV01 (USD per bp)", s["last_bucket"], -61_643, 0)
    assert s["grad_err"] < 1e-6
    assert s["fd_rel_err"] < 1e-4
    quoted("forward tape nodes", s["forward_nodes"], 163, 0)
    quoted("reverse-sweep multiply-adds", s["reverse_ops"], 203, 0)
    quoted("reverse work over forward nodes", s["reverse_ops"] / s["forward_nodes"], 1.25, 2)
    quoted("pricings needed by one-sided finite differences", s["fd_evals"], 41, 0)
    quoted("passes needed by forward-mode AD", s["fwd_mode_passes"], 40, 0)
    quoted("FD node work over AAD forward+reverse work", 41 * s["forward_nodes"] / (s["forward_nodes"] + s["reverse_ops"]), 18.3, 1)

    print("  Example 4: Monte Carlo call, delta and vega from one reverse sweep (seed 2024, 20,000 paths)")
    m = aad_monte_carlo(20_000, seed=2024)
    quoted("Black-Scholes price", m["bs_price"], 9.4134, 4)
    quoted("Black-Scholes delta", m["bs_delta"], 0.5987, 4)
    quoted("Black-Scholes vega", m["bs_vega"], 38.67, 2)
    quoted("Monte Carlo price", m["price"], 9.57, 2)
    quoted("Monte Carlo standard error", m["se"], 0.10, 2)
    assert abs(m["price"] - m["bs_price"]) < 3 * m["se"]
    quoted("AAD pathwise delta", m["delta"], 0.600, 3)
    quoted("AAD pathwise vega", m["vega"], 39.6, 1)
    assert abs(m["delta"] - m["bs_delta"]) < 0.01 and abs(m["vega"] / m["bs_vega"] - 1) < 0.05
    quoted("tape nodes for 20,000 paths", m["nodes"], 160_005, 0)
    quoted("tape nodes per path", (m["nodes"] - 5) / 20_000, 8, 0)

    print("  Example 5: floating-point determinism")
    left, right = (0.1 + 0.2) + 0.3, 0.1 + (0.2 + 0.3)
    assert left != right
    quoted("(0.1 + 0.2) + 0.3 minus 0.1 + (0.2 + 0.3)", (left - right) * 1e16, 1.11, 2)
    d = determinism_demo()
    quoted("distinct sums from 1, 8, 16 and 64 chunks", d["distinct_chunk_results"], 3, 0)
    quoted("worst chunked-sum error versus the exact sum", d["worst_abs_err"], 0.0078, 4)
    quoted("fixed-tree sum error versus the exact sum", d["tree_abs_err"], 0.031, 3)

    print("  Example 6: FD versus AAD cost and tape memory (hypothetical inputs)")
    t_price, n_factors, aad_multiple = 12.5, 2_000, 4.0
    fd_s = (n_factors + 1) * t_price
    quoted("one-sided FD runs", fd_s / t_price, 2_001, 0)
    quoted("central FD runs", (2 * n_factors + 1), 4_001, 0)
    quoted("one-sided FD time (s)", fd_s, 25_012.5, 1)
    quoted("one-sided FD time (hours)", fd_s / 3600, 6.95, 2)
    quoted("central FD time (hours)", (2 * n_factors + 1) * t_price / 3600, 13.89, 2)
    quoted("AAD time at a hypothetical 4x multiple (s)", aad_multiple * t_price, 50.0, 1)
    quoted("speed-up", fd_s / (aad_multiple * t_price), 500.25, 2)
    quoted("break-even factor count for a 4x AAD multiple", aad_multiple - 1, 3, 0)
    nodes = 100_000 * 100 * 10
    quoted("tape nodes: 100,000 paths x 100 steps x 10 ops (billions)", nodes / 1e9, 0.1, 1)
    quoted("tape memory at 24 bytes per node (GB)", nodes * 24 / 1e9, 2.4, 1)
    quoted("tape memory per path with path-wise checkpointing (KB)", 100 * 10 * 24 / 1e3, 24.0, 1)

    print(f"  {len(QUOTED)} numbers quoted in note 05 computed, printed and asserted")
    print("All pricing library checks passed.")


if __name__ == "__main__":
    run_tests()
