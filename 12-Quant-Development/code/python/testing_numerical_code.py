"""Testing trading and numerical code: every number quoted in note 14.

Sections (each prints its numbers and asserts them):
  1. Floating-point comparison: ulps, absolute vs relative tolerance, math.isclose vs numpy.isclose.
  2. Summation order: non-associativity, fsum, and why parallel reductions are not bit-reproducible.
  3. Seeds: Python random, NumPy bit generators, SeedSequence spawning.
  4. Monte Carlo tolerance from the standard error.
  5. Property-based testing with a hand-rolled generator and shrinker (hypothesis is not required).
  6. Metamorphic tests on a Black-Scholes pricer.
  7. Golden values and a golden hash of canonical output.
  8. Fuzzing a length-prefixed binary parser.
  9. Replay regression: locate the first divergent output event.

Run: uv run --no-project --with numpy python 12-Quant-Development/code/python/testing_numerical_code.py
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import struct
import sys

import numpy as np


class SplitMix64:
    """Tiny portable PRNG. Its stream is fixed by this code, not by a library version.

    Python guarantees only random.random() across versions for a given seed; NumPy (NEP 19)
    guarantees bit-generator streams but lets Generator distribution methods change in X.Y releases.
    Tests that pin exact counts therefore draw from this generator.
    """

    MASK = (1 << 64) - 1

    def __init__(self, seed: int) -> None:
        self.state = seed & self.MASK

    def next(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & self.MASK
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & self.MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & self.MASK
        return z ^ (z >> 31)

    def below(self, n: int) -> int:
        return self.next() % n

    def uniform(self, a: float, b: float) -> float:
        return a + (b - a) * ((self.next() >> 11) * 2.0**-53)

    def randint(self, a: int, b: int) -> int:
        return a + self.below(b - a + 1)

    def choice(self, seq):
        return seq[self.below(len(seq))]

    def randbytes(self, n: int) -> bytes:
        return bytes(self.below(256) for _ in range(n))


def naive_sum(xs) -> float:
    """Left-to-right recursive summation, what a plain loop (or C++ std::accumulate) does."""
    total = 0.0
    for v in xs:
        total += v
    return total


# ---------------------------------------------------------------------------
# 1. Floating-point comparison
# ---------------------------------------------------------------------------


def ordered_bits(x: float) -> int:
    """Map a double to an integer so adjacent doubles differ by 1 (sign-magnitude to two's-complement order)."""
    (i,) = struct.unpack("<q", struct.pack("<d", x))
    return i if i >= 0 else -(i & 0x7FFF_FFFF_FFFF_FFFF)


def ulp_distance(a: float, b: float) -> int:
    if math.isnan(a) or math.isnan(b):
        raise ValueError("ulp distance undefined for NaN")
    return abs(ordered_bits(a) - ordered_bits(b))


def section_float_comparison() -> dict:
    s = 0.1 + 0.2
    out = {
        "sum_repr": repr(s),
        "eq": s == 0.3,
        "ulps": ulp_distance(s, 0.3),
        "ulp1": math.ulp(1.0),
        "ulp100": math.ulp(100.0),
        "ulp1e6": math.ulp(1e6),
        "eps_half": math.ulp(1.0) / 2,  # unit roundoff u = 2^-53, derived from the measured ulp at 1.0
        "isclose_default": math.isclose(s, 0.3),
        "isclose_zero": math.isclose(1e-20, 0.0),
        "isclose_zero_abs": math.isclose(1e-20, 0.0, abs_tol=1e-12),
        "np_isclose_small": bool(np.isclose(1e-9, 2e-9)),
        "np_isclose_asym_ab": bool(np.isclose(1.0, 2.0, rtol=0.5, atol=0.0)),
        "np_isclose_asym_ba": bool(np.isclose(2.0, 1.0, rtol=0.5, atol=0.0)),
        "math_isclose_sym": math.isclose(1.0, 2.0, rel_tol=0.5) and math.isclose(2.0, 1.0, rel_tol=0.5),
        "ulps_zero": ulp_distance(0.0, -0.0),
        "ulps_tiny": ulp_distance(5e-324, -5e-324),
    }
    print("1. Floating-point comparison")
    print(f"   0.1 + 0.2 = {out['sum_repr']}, == 0.3 is {out['eq']}, ulp distance {out['ulps']}")
    print(f"   ulp(1.0) = {out['ulp1']!r}, ulp(100.0) = {out['ulp100']!r}, ulp(1e6) = {out['ulp1e6']!r}")
    print(f"   unit roundoff 2^-53 = {out['eps_half']!r}")
    print(f"   math.isclose(0.1+0.2, 0.3) = {out['isclose_default']}")
    print(f"   math.isclose(1e-20, 0.0) = {out['isclose_zero']}, with abs_tol=1e-12: {out['isclose_zero_abs']}")
    print(f"   np.isclose(1e-9, 2e-9) with default atol=1e-8: {out['np_isclose_small']}")
    print(f"   np.isclose(1, 2, rtol=0.5, atol=0) = {out['np_isclose_asym_ab']}, np.isclose(2, 1, ...) = {out['np_isclose_asym_ba']}")
    print(f"   math.isclose(1, 2, rel_tol=0.5) in both orders: {out['math_isclose_sym']}")
    print(f"   ulp distance(0.0, -0.0) = {out['ulps_zero']}, (5e-324, -5e-324) = {out['ulps_tiny']}")
    assert out["sum_repr"] == "0.30000000000000004" and not out["eq"] and out["ulps"] == 1
    assert out["ulp1"] == 2.220446049250313e-16 and out["ulp100"] == 1.4210854715202004e-14
    assert out["ulp1e6"] == 1.1641532182693481e-10
    assert out["eps_half"] == 1.1102230246251565e-16
    # Note 14 Core concepts and card qd-testing-ulp-size quote these at 3 significant figures.
    assert f"{out['ulp1']:.2e}" == "2.22e-16" and f"{out['eps_half']:.2e}" == "1.11e-16"
    assert f"{out['ulp1e6']:.2e}" == "1.16e-10"
    assert out["isclose_default"] and not out["isclose_zero"] and out["isclose_zero_abs"]
    assert out["np_isclose_small"]
    assert out["np_isclose_asym_ab"] is True and out["np_isclose_asym_ba"] is False and out["math_isclose_sym"]
    assert out["ulps_zero"] == 0 and out["ulps_tiny"] == 2
    return out


# ---------------------------------------------------------------------------
# 2. Summation order
# ---------------------------------------------------------------------------


def kahan_sum(xs) -> float:
    """Kahan compensated summation: carry the rounding error of each addition into the next."""
    total = 0.0
    comp = 0.0
    for v in xs:
        y = v - comp
        t = total + y
        comp = (t - total) - y  # what was lost when y was added to total
        total = t
    return total


def chunked_sum(x: list[float], chunks: int) -> float:
    """Sum the way a parallel reduction would: per-chunk partial sums, then combine."""
    n = len(x)
    bounds = [n * k // chunks for k in range(chunks + 1)]
    partials = [naive_sum(x[bounds[k] : bounds[k + 1]]) for k in range(chunks)]
    return naive_sum(partials)


def section_summation() -> dict:
    left = (0.1 + 0.2) + 0.3
    right = 0.1 + (0.2 + 0.3)
    rng = SplitMix64(14)
    x = [rng.uniform(-1000.0, 1000.0) for _ in range(100_000)]
    exact = math.fsum(x)
    fwd = naive_sum(x)
    rev = naive_sum(reversed(x))
    chunk_results = {c: chunked_sum(x, c) for c in (1, 2, 4, 8, 16)}
    distinct = len(set(chunk_results.values()))
    worst = max(ulp_distance(v, exact) for v in [fwd, rev, *chunk_results.values()])
    big = [1e16, 1.0, -1e16]
    out = {
        "left": left,
        "right": right,
        "fwd_ulps": ulp_distance(fwd, exact),
        "rev_ulps": ulp_distance(rev, exact),
        "distinct_chunk_sums": distinct,
        "worst_ulps": worst,
        "kahan_ulps": ulp_distance(kahan_sum(x), exact),
        "big_naive": naive_sum(big),
        "big_fsum": math.fsum(big),
        "big_builtin": sum(big),
    }
    print("2. Summation order")
    print(f"   (0.1+0.2)+0.3 = {left!r}, 0.1+(0.2+0.3) = {right!r}")
    print(f"   100000 uniforms on [-1000, 1000] (SplitMix64 seed 14): fsum = {exact!r}")
    print(f"   ulps from the correctly rounded sum: forward loop {out['fwd_ulps']}, reversed loop {out['rev_ulps']}")
    print(f"   chunked loops with 1, 2, 4, 8, 16 chunks give {distinct} distinct results; worst {worst} ulps")
    print(f"   Kahan compensated loop: {out['kahan_ulps']} ulps from fsum")
    print(f"   loop over [1e16, 1, -1e16] = {out['big_naive']!r}, fsum = {out['big_fsum']!r}, builtin sum = {out['big_builtin']!r}")
    assert left == 0.6000000000000001 and right == 0.6
    assert exact == -18009.51879856792  # fsum is correctly rounded, so this is platform-independent
    assert out["fwd_ulps"] == 179 and out["rev_ulps"] == 103
    assert distinct == 5 and worst == 533
    assert out["kahan_ulps"] == 0
    assert out["big_naive"] == 0.0 and out["big_fsum"] == 1.0
    if sys.version_info >= (3, 12):  # builtin sum() of floats is compensated (Neumaier) from Python 3.12
        assert out["big_builtin"] == 1.0
    out["exact"] = exact
    out["chunk_results"] = chunk_results
    return out


# ---------------------------------------------------------------------------
# 3. Seeds
# ---------------------------------------------------------------------------


def section_seeds() -> dict:
    py_first = random.Random(42).random()
    a = np.random.default_rng(42).standard_normal(5)
    b = np.random.default_rng(42).standard_normal(5)
    children = np.random.SeedSequence(42).spawn(4)
    streams = [np.random.default_rng(c).integers(0, 2**32, size=3).tolist() for c in children]
    distinct_streams = len({tuple(s) for s in streams})
    sm = SplitMix64(0)
    sm_first = sm.next()
    out = {"py_first": py_first, "same": bool(np.array_equal(a, b)), "distinct": distinct_streams, "sm_first": sm_first}
    print("3. Seeds")
    print(f"   random.Random(42).random() = {py_first!r}")
    print(f"   two default_rng(42) generators agree bit for bit: {out['same']}")
    print(f"   SeedSequence(42).spawn(4) -> {distinct_streams} distinct child streams")
    print(f"   SplitMix64(0) first output = {sm_first:#018x}")
    assert py_first == 0.6394267984578837
    assert out["same"] and distinct_streams == 4
    assert sm_first == 0xE220A8397B1DCDAF  # published SplitMix64 reference value for seed 0
    return out


# ---------------------------------------------------------------------------
# 4 and 6. Black-Scholes pricer, Monte Carlo tolerance, metamorphic tests
# ---------------------------------------------------------------------------


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def bs_call(s: float, k: float, r: float, sigma: float, t: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)


def bs_put(s: float, k: float, r: float, sigma: float, t: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return k * math.exp(-r * t) * norm_cdf(-d2) - s * norm_cdf(-d1)


def pinned_normals(seed: int, n: int) -> np.ndarray:
    """Standard normals from the raw PCG64 stream through Box-Muller.

    The raw 64-bit stream is fixed by the PCG64 algorithm and the seed; Generator.standard_normal
    is a distribution method that NEP 19 allows to change in feature releases, so a test that pins
    an exact Monte Carlo estimate builds its normals from the raw stream instead.
    """
    raw = np.random.PCG64(seed).random_raw(n + n % 2)
    u = (raw >> np.uint64(11)).astype(np.float64) * 2.0**-53  # uniforms on [0, 1)
    radius = np.sqrt(-2.0 * np.log(1.0 - u[0::2]))  # 1 - u is in (0, 1], so the log is finite
    angle = 2.0 * math.pi * u[1::2]
    return np.concatenate([radius * np.cos(angle), radius * np.sin(angle)])[:n]


def section_mc_tolerance() -> dict:
    s, k, r, sig, t = 100.0, 100.0, 0.05, 0.2, 1.0
    exact = bs_call(s, k, r, sig, t)
    n = 200_000
    z = pinned_normals(2024, n)
    st = s * np.exp((r - 0.5 * sig * sig) * t + sig * math.sqrt(t) * z)
    pay = math.exp(-r * t) * np.maximum(st - k, 0.0)
    est = float(pay.mean())
    se = float(pay.std(ddof=1) / math.sqrt(n))
    zscore = (est - exact) / se
    p_false_4 = math.erfc(4.0 / math.sqrt(2.0))
    p_false_3 = math.erfc(3.0 / math.sqrt(2.0))
    out = {"exact": exact, "est": est, "se": se, "z": zscore, "p4": p_false_4, "p3": p_false_3}
    print("4. Monte Carlo tolerance")
    print(f"   BS call S=K=100 r=5% vol=20% T=1: {exact:.4f}")
    print(f"   MC with 200000 paths (PCG64 raw stream, Box-Muller, seed 2024): {est:.4f}, standard error {se:.4f}, z = {zscore:.2f}")
    print(f"   false-failure probability of a 4-SE two-sided test {p_false_4:.2e}, of a 3-SE test {p_false_3:.2e}")
    print(f"   with 1000 such tests per CI run at 3 SE, expected false failures {1000 * p_false_3:.1f}")
    print(f"   with 1000 such tests per CI run at 4 SE, expected false failures {1000 * p_false_4:.2f}")
    # Note 14 example 3 and card qd-testing-mc-tolerance, at the quoted rounding.
    assert f"{exact:.4f}" == "10.4506"
    assert abs(zscore) < 4.0
    assert f"{est:.4f}" == "10.3970" and f"{se:.4f}" == "0.0328" and f"{zscore:.2f}" == "-1.63"
    assert f"{p_false_4:.2e}" == "6.33e-05" and f"{p_false_4:.1e}" == "6.3e-05" and f"{p_false_3:.2e}" == "2.70e-03"
    assert f"{1000 * p_false_3:.1f}" == "2.7" and f"{1000 * p_false_4:.2f}" == "0.06"
    return out


def section_metamorphic() -> dict:
    rng = SplitMix64(6)
    n = 10_000
    max_parity = 0.0
    mono_violations = 0  # strict: bumped price below base price at all
    mono_violations_tol = 0  # below base by more than 1e-12 * S
    bound_violations = 0
    max_homog = 0.0
    for _ in range(n):
        s = rng.uniform(50, 150)
        k = rng.uniform(50, 150)
        r = rng.uniform(0.0, 0.08)
        sig = rng.uniform(0.05, 0.8)
        t = rng.uniform(0.05, 3.0)
        c = bs_call(s, k, r, sig, t)
        p = bs_put(s, k, r, sig, t)
        max_parity = max(max_parity, abs((c - p) - (s - k * math.exp(-r * t))) / s)
        bumped = min(bs_call(s * 1.01, k, r, sig, t), bs_call(s, k, r, sig * 1.01, t))
        if bumped < c:
            mono_violations += 1
        if bumped < c - 1e-12 * s:
            mono_violations_tol += 1
        if not (max(s - k * math.exp(-r * t), 0.0) - 1e-12 * s <= c <= s * (1 + 1e-12)):
            bound_violations += 1
        max_homog = max(max_homog, abs(bs_call(3 * s, 3 * k, r, sig, t) - 3 * c) / (3 * s))
    out = {
        "n": n,
        "parity": max_parity,
        "mono": mono_violations,
        "mono_tol": mono_violations_tol,
        "bounds": bound_violations,
        "homog": max_homog,
    }
    print("6. Metamorphic tests on Black-Scholes, 10000 random parameter sets (SplitMix64 seed 6)")
    print(f"   max |C - P - (S - K e^-rT)| / S = {max_parity:.1e}")
    print(f"   monotonicity: {mono_violations} strict violations (rounding noise), {mono_violations_tol} beyond 1e-12 * S")
    print(f"   bound violations {bound_violations}")
    print(f"   max |C(3S,3K) - 3C(S,K)| / 3S = {max_homog:.1e}")
    assert max_parity < 1e-13 and max_homog < 1e-13
    assert mono_violations < 100, "libm-dependent count (6 on macOS, possibly 0 elsewhere): never assert it"
    assert mono_violations_tol == 0 and bound_violations == 0
    return out


# ---------------------------------------------------------------------------
# 5. Property-based test with shrinking
# ---------------------------------------------------------------------------


def split_order_buggy(qty: int, max_child: int) -> list[int]:
    """Split a parent order into child orders of at most max_child. Bug: emits a zero-size child."""
    return [max_child] * (qty // max_child) + [qty % max_child]


def split_order_fixed(qty: int, max_child: int) -> list[int]:
    full, rest = divmod(qty, max_child)
    return [max_child] * full + ([rest] if rest else [])


def split_property(fn, qty: int, max_child: int) -> bool:
    children = fn(qty, max_child)
    return sum(children) == qty and all(0 < c <= max_child for c in children)


def shrink(fn, qty: int, max_child: int) -> tuple[int, int, int]:
    """Greedy shrinking: try smaller candidates, keep any that still fails, stop at a fixed point."""
    steps = 0
    improved = True
    while improved:
        improved = False
        candidates = [
            (qty // 2, max_child // 2),
            (qty // 2, max_child),
            (qty - 1, max_child),
            (qty, max_child // 2),
            (qty, max_child - 1),
            (qty - max_child, max_child),
        ]
        for q, m in candidates:
            if q >= 1 and m >= 1 and (q, m) != (qty, max_child) and not split_property(fn, q, m):
                qty, max_child = q, m
                steps += 1
                improved = True
                break
    return qty, max_child, steps


def section_property() -> dict:
    rng = SplitMix64(5)
    first_fail = None
    tried = 0
    for _ in range(1000):
        qty = rng.randint(1, 10_000)
        max_child = rng.choice([100, 200, 500, 1000])
        tried += 1
        if not split_property(split_order_buggy, qty, max_child):
            first_fail = (qty, max_child)
            break
    assert first_fail is not None
    q, m, steps = shrink(split_order_buggy, *first_fail)
    fixed_ok = all(split_property(split_order_fixed, rng.randint(1, 10_000), rng.randint(1, 1000)) for _ in range(2000))
    out = {"tried": tried, "first_fail": first_fail, "shrunk": (q, m), "steps": steps, "fixed_ok": fixed_ok}
    print("5. Property-based test of an order splitter (SplitMix64 seed 5)")
    print(f"   first failing input after {tried} cases: qty={first_fail[0]}, max_child={first_fail[1]}")
    print(f"   -> {split_order_buggy(*first_fail)[-3:]} (last three children)")
    print(f"   shrunk in {steps} steps to qty={q}, max_child={m}: {split_order_buggy(q, m)}")
    print(f"   fixed splitter passes 2000 random cases: {fixed_ok}")
    assert (q, m) == (1, 1) and split_order_buggy(1, 1) == [1, 0]
    assert first_fail == (7400, 100) and tried == 10 and steps == 14
    assert fixed_ok
    return out


# ---------------------------------------------------------------------------
# 7. Golden values and golden hash
# ---------------------------------------------------------------------------

GOLDEN_CALLS = {  # (S, K) -> price with r=5%, vol=20%, T=1, stored once from a reviewed run
    (90.0, 100.0): 5.091222078817552,
    (100.0, 100.0): 10.450583572185565,
    (110.0, 100.0): 17.662953740590453,
}
GOLDEN_SHA256 = "8ead068d954fbbbb75b6da00a96d3604255bdef01348aae262ad722f90a0f2d6"


def canonical_bytes(prices: dict) -> bytes:
    """Canonical serialisation: sorted keys, fixed decimal rounding, no whitespace variance."""
    rows = [[s, k, round(v, 8)] for (s, k), v in sorted(prices.items())]
    return json.dumps(rows, separators=(",", ":")).encode()


def section_golden() -> dict:
    now = {key: bs_call(key[0], key[1], 0.05, 0.2, 1.0) for key in GOLDEN_CALLS}
    worst_rel = max(abs(now[k] - v) / v for k, v in GOLDEN_CALLS.items())
    digest = hashlib.sha256(canonical_bytes(now)).hexdigest()
    print("7. Golden tests")
    print(f"   worst relative deviation from golden prices {worst_rel:.1e} (tolerance 1e-12)")
    print(f"   sha256 of canonical output rounded to 8 dp: {digest}")
    assert worst_rel < 1e-12
    assert digest == GOLDEN_SHA256
    return {"worst_rel": worst_rel, "digest": digest}


# ---------------------------------------------------------------------------
# 8. Fuzzing a length-prefixed parser
# ---------------------------------------------------------------------------


def parse_blocks_trusting(buf: bytes, count: int) -> list[bytes]:
    """Bug: trusts the declared lengths. Python slicing never raises, so short data passes silently."""
    out, off = [], 0
    for _ in range(count):
        (n,) = struct.unpack_from(">H", buf, off)
        out.append(buf[off + 2 : off + 2 + n])
        off += 2 + n
    return out


def parse_blocks_checked(buf: bytes, count: int) -> list[bytes]:
    out, off = [], 0
    for _ in range(count):
        if len(buf) - off < 2:
            raise ValueError("truncated length field")
        (n,) = struct.unpack_from(">H", buf, off)
        if len(buf) - off - 2 < n:
            raise ValueError("block overruns buffer")
        out.append(buf[off + 2 : off + 2 + n])
        off += 2 + n
    if off != len(buf):
        raise ValueError("trailing bytes")
    return out


def section_fuzz() -> dict:
    rng = SplitMix64(8)
    valid = struct.pack(">H", 4) + b"ABCD" + struct.pack(">H", 3) + b"XYZ"
    silent_short = 0
    crashes_trusting = 0
    checked_rejects = 0
    checked_other_exc = 0
    n_cases = 20_000
    for _ in range(n_cases):
        buf = bytearray(valid)
        mode = rng.below(3)
        if mode == 0:
            buf[rng.below(len(buf))] = rng.below(256)
        elif mode == 1:
            del buf[rng.below(len(buf)) :]
        else:
            buf = bytearray(rng.randbytes(rng.below(16)))
        data = bytes(buf)
        try:
            blocks = parse_blocks_trusting(data, 2)
            off = 0
            for blk in blocks:
                (declared,) = struct.unpack_from(">H", data, off)
                if len(blk) != declared:
                    silent_short += 1
                    break
                off += 2 + declared
        except struct.error:
            crashes_trusting += 1
        try:
            parse_blocks_checked(data, 2)
        except ValueError:
            checked_rejects += 1
        except Exception:  # noqa: BLE001 - any other exception type is a parser bug the fuzzer must count
            checked_other_exc += 1
    out = {
        "cases": n_cases,
        "silent_short": silent_short,
        "crashes": crashes_trusting,
        "rejects": checked_rejects,
        "other": checked_other_exc,
    }
    print("8. Fuzzing a length-prefixed parser, 20000 mutated inputs (SplitMix64 seed 8)")
    print(f"   trusting parser: {silent_short} inputs silently returned a short block, {crashes_trusting} raised struct.error")
    print(f"   checked parser: {checked_rejects} clean ValueError rejections, {checked_other_exc} unexpected exceptions")
    assert silent_short > 0 and checked_other_exc == 0
    assert out == {"cases": 20000, "silent_short": 3089, "crashes": 12737, "rejects": 15835, "other": 0}
    return out


# ---------------------------------------------------------------------------
# 9. Replay regression
# ---------------------------------------------------------------------------


def make_event_log(seed: int, n: int) -> list[tuple[int, int, str, float]]:
    """(timestamp_us, arrival_seq, symbol, price); timestamps collide on purpose."""
    rng = SplitMix64(seed)
    log, ts = [], 0
    for seq in range(n):
        ts += rng.choice([0, 0, 1, 2])
        log.append((ts, seq, rng.choice(["AAA", "BBB"]), round(100 + rng.uniform(-1, 1), 2)))
    return log


def lead_lag(events) -> list[str]:
    """Buy BBB when it trades more than 0.80 below the last AAA price (cross-instrument state)."""
    last_aaa = None
    out = []
    for ts, seq, sym, px in events:
        if sym == "AAA":
            last_aaa = px
        elif last_aaa is not None and px < last_aaa - 0.80:
            out.append(f"{ts}:{seq}:BBB:BUY@{px:.2f}")
    return out


def strategy_v1(log: list[tuple[int, int, str, float]]) -> list[str]:
    """Process events in (timestamp, arrival sequence) order: the order the feed delivered them."""
    return lead_lag(sorted(log, key=lambda e: (e[0], e[1])))


def strategy_v2(log: list[tuple[int, int, str, float]]) -> list[str]:
    """'Harmless refactor' that breaks timestamp ties by symbol: same logic, different event order."""
    return lead_lag(sorted(log, key=lambda e: (e[0], e[2])))


def first_divergence(a: list[str], b: list[str]) -> int | None:
    for i, (x, y) in enumerate(zip(a, b, strict=False)):
        if x != y:
            return i
    return None if len(a) == len(b) else min(len(a), len(b))


def section_replay() -> dict:
    log = make_event_log(9, 500)
    base = strategy_v1(log)
    again = strategy_v1(log)
    changed = strategy_v2(log)
    h1 = hashlib.sha256("\n".join(base).encode()).hexdigest()[:16]
    h2 = hashlib.sha256("\n".join(changed).encode()).hexdigest()[:16]
    idx = first_divergence(base, changed)
    ties = sum(1 for i in range(1, len(log)) if log[i][0] == log[i - 1][0])
    out = {"events": len(log), "ties": ties, "orders": len(base), "same_twice": base == again, "diverge": idx}
    print("9. Replay regression, 500 events (SplitMix64 seed 9)")
    print(f"   {ties} events share a timestamp with their predecessor")
    print(f"   v1 emits {len(base)} orders, hash {h1}; rerun identical: {base == again}")
    print(f"   v2 hash {h2}; first divergent order index {idx}: {base[idx]} vs {changed[idx]}")
    assert base == again and h1 != h2 and idx is not None
    assert h1 == "c687cb7e4204b92f" and h2 == "8fe97de119af012c"
    assert base[idx] == "29:46:BBB:BUY@99.63" and changed[idx] == "29:44:BBB:BUY@99.36"
    assert ties == 241 and len(base) == 48 and idx == 2
    return out


def main() -> None:
    section_float_comparison()
    section_summation()
    section_seeds()
    section_mc_tolerance()
    section_property()
    section_metamorphic()
    section_golden()
    section_fuzz()
    section_replay()
    print("all assertions passed")


if __name__ == "__main__":
    main()
