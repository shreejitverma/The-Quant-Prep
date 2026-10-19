"""Storage and compute: Gorilla compression (encoder and decoder), columnar I/O, entropy of float columns, cube sizing.

Backs every number in `18-Pricing-and-Risk-Systems/14-Storage-and-Compute.md`.

1. Gorilla XOR value compression and delta-of-delta timestamp compression, implemented as in Pelkonen et al. (PVLDB 8(12)
   2015, section 4.1), with a decoder; every encoded series is decoded and compared bit for bit with the input.
2. The single-value walkthrough (100.0 then 100.125) and bits per value for synthetic price series on a binary grid
   (1/256), on a decimal grid (0.01) and on a decimal grid with mostly unchanged prices, against delta-encoded integer
   ticks with zigzag varints.
3. Bytes scanned by a row store versus a column store for an aggregation over a labelled-hypothetical schema.
4. Order-0 Shannon entropy of the eight byte streams of float64 scenario P&L (what BYTE_STREAM_SPLIT exposes to an
   entropy coder), raw versus rounded to whole dollars.
5. Ten-year sizing of a sensitivity cube and a scenario P&L archive from labelled-hypothetical inputs.

Synthetic series use fixed seeds; every input is a hypothetical teaching value.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_storage_compute.py`.
"""

from __future__ import annotations

import math
import random
import struct
from collections import Counter

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
# 1. Gorilla
# ============================================================================


def f2u(x: float) -> int:
    return struct.unpack(">Q", struct.pack(">d", x))[0]


def u2f(u: int) -> float:
    return struct.unpack(">d", struct.pack(">Q", u))[0]


def clz64(x: int) -> int:
    return 64 - x.bit_length()


def ctz64(x: int) -> int:
    return (x & -x).bit_length() - 1


class BitWriter:
    def __init__(self) -> None:
        self.bits: list[int] = []

    def write(self, value: int, width: int) -> None:
        for i in range(width - 1, -1, -1):
            self.bits.append((value >> i) & 1)


class BitReader:
    def __init__(self, bits: list[int]) -> None:
        self.bits = bits
        self.pos = 0

    def read(self, width: int) -> int:
        v = 0
        for _ in range(width):
            v = (v << 1) | self.bits[self.pos]
            self.pos += 1
        return v


def gorilla_encode_values(values: list[float]) -> list[int]:
    """Pelkonen et al. section 4.1.2: first value raw; then '0' if unchanged, else '1' plus case (a) or (b)."""
    w = BitWriter()
    prev = f2u(values[0])
    w.write(prev, 64)
    prev_lead, prev_trail = -1, -1  # no window yet
    for x in values[1:]:
        cur = f2u(x)
        xor = cur ^ prev
        if xor == 0:
            w.write(0, 1)
        else:
            w.write(1, 1)
            lead = min(clz64(xor), 31)  # 5-bit field
            trail = ctz64(xor)
            if prev_lead >= 0 and lead >= prev_lead and trail >= prev_trail:
                # (a) control '0': the meaningful bits fit in the previous window; reuse it
                w.write(0, 1)
                width = 64 - prev_lead - prev_trail
                w.write(xor >> prev_trail, width)
            else:
                # (b) control '1': 5 bits leading-zero count, 6 bits length (64 stored as 0), then the bits
                w.write(1, 1)
                width = 64 - lead - trail
                w.write(lead, 5)
                w.write(width % 64, 6)
                w.write(xor >> trail, width)
                prev_lead, prev_trail = lead, trail
        prev = cur
    return w.bits


def gorilla_decode_values(bits: list[int], n: int) -> list[float]:
    r = BitReader(bits)
    prev = r.read(64)
    out = [u2f(prev)]
    lead, trail = -1, -1
    for _ in range(n - 1):
        if r.read(1) == 0:
            out.append(u2f(prev))
            continue
        if r.read(1) == 0:
            width = 64 - lead - trail
            xor = r.read(width) << trail
        else:
            lead = r.read(5)
            width = r.read(6) or 64
            trail = 64 - lead - width
            xor = r.read(width) << trail
        prev ^= xor
        out.append(u2f(prev))
    assert r.pos == len(bits)
    return out


def gorilla_timestamp_bits(ts: list[int]) -> int:
    """Delta-of-delta encoding (section 4.1.1): 64-bit header, 14-bit first delta, then variable-length D."""
    bits = 64 + 14
    prev_delta = ts[1] - ts[0]
    for i in range(2, len(ts)):
        delta = ts[i] - ts[i - 1]
        d = delta - prev_delta
        if d == 0:
            bits += 1
        elif -63 <= d <= 64:
            bits += 2 + 7
        elif -255 <= d <= 256:
            bits += 3 + 9
        elif -2047 <= d <= 2048:
            bits += 4 + 12
        else:
            bits += 4 + 32
        prev_delta = delta
    return bits


def varint_zigzag_bytes(deltas: list[int]) -> int:
    total = 0
    for d in deltas:
        z = (d << 1) ^ (d >> 63)  # zigzag
        z &= (1 << 64) - 1
        total += max(1, math.ceil(z.bit_length() / 7))
    return total


def test_gorilla_walkthrough() -> None:
    print("  1. Gorilla single-value walkthrough: 100.0 then 100.125")
    v0, v1 = 100.0, 100.125
    xor = f2u(v0) ^ f2u(v1)
    assert f2u(v0) == 0x4059000000000000 and f2u(v1) == 0x4059080000000000
    quoted("leading zeros", clz64(xor), 20, 0)
    quoted("trailing zeros", ctz64(xor), 43, 0)
    quoted("meaningful bits", 64 - clz64(xor) - ctz64(xor), 1, 0)
    bits = gorilla_encode_values([v0, v1])
    quoted("bits for the second value", len(bits) - 64, 14, 0)
    quoted("saving on that value versus 64 bits (%)", 100.0 * (64 - (len(bits) - 64)) / 64.0, 78.1, 1)
    assert gorilla_decode_values(bits, 2) == [v0, v1]
    # A third value with the same window is cheaper: case (a) reuses the window.
    bits3 = gorilla_encode_values([100.0, 100.125, 100.0])
    quoted("bits for a third value 100.0 (window reused)", len(bits3) - len(bits), 3, 0)
    assert gorilla_decode_values(bits3, 3) == [100.0, 100.125, 100.0]


def walk(n: int, p_unchanged: float, seed: int) -> list[int]:
    rng = random.Random(seed)
    k = [0]
    for _ in range(n - 1):
        if rng.random() < p_unchanged:
            k.append(k[-1])
        else:
            k.append(k[-1] + rng.choice([-2, -1, 1, 2]))
    return k


def test_gorilla_series() -> None:
    print("  2. Bits per value on 10,000-tick synthetic series (seed 42)")
    n = 10_000
    ticks = walk(n, 0.0, 42)
    ticks_sticky = walk(n, 0.7, 42)
    series = {
        "binary grid 1/256": [100.0 + k / 256.0 for k in ticks],
        "decimal grid 0.01": [(10_000 + k) / 100.0 for k in ticks],
        "decimal grid 0.01, 70% unchanged": [(10_000 + k) / 100.0 for k in ticks_sticky],
    }
    expected = {"binary grid 1/256": 12.8, "decimal grid 0.01": 51.0, "decimal grid 0.01, 70% unchanged": 16.1}
    for name, xs in series.items():
        bits = gorilla_encode_values(xs)
        assert gorilla_decode_values(bits, n) == xs  # lossless, bit for bit
        quoted(f"Gorilla bits per value, {name}", (len(bits) - 64) / (n - 1), expected[name], 1)
    deltas = [ticks[i] - ticks[i - 1] for i in range(1, n)]
    quoted("integer ticks, zigzag varint bits per value", 8.0 * varint_zigzag_bytes(deltas) / (n - 1), 8.0, 1)
    # Timestamps: regular 1-second sampling versus irregular nanosecond tick times.
    regular = [1_768_500_000 + i for i in range(n)]
    quoted("timestamp bits per point, regular 1 s interval", (gorilla_timestamp_bits(regular) - 78) / (n - 2), 1.0, 1)
    rng = random.Random(7)
    t, irregular = 0, []
    for _ in range(n):
        t += int(rng.expovariate(1.0 / 2_000_000.0)) + 1  # mean gap 2 ms in nanoseconds
        irregular.append(t)
    quoted("timestamp bits per point, irregular ns ticks", (gorilla_timestamp_bits(irregular) - 78) / (n - 2), 36.0, 1)


# ============================================================================
# 3. Row versus column scans
# ============================================================================


def test_columnar_io() -> None:
    print("  3. Bytes scanned per row: row store versus column store (hypothetical schema)")
    cat_cols, cat_bytes, num_cols, num_bytes = 10, 4, 45, 8
    row_width = cat_cols * cat_bytes + num_cols * num_bytes
    quoted("row width (bytes)", row_width, 400, 0)
    quoted("scan reduction for SUM(dv01)", row_width / num_bytes, 50, 0)
    quoted("scan reduction for SUM(dv01) GROUP BY desk, currency", row_width / (num_bytes + 2 * cat_bytes), 25, 0)


# ============================================================================
# 4. Entropy of float64 byte streams
# ============================================================================


def stream_entropy_bits(x: np.ndarray) -> float:
    """Sum over the 8 byte positions of the order-0 Shannon entropy of that byte stream (bits per value)."""
    raw = np.ascontiguousarray(x, dtype="<f8").view(np.uint8).reshape(-1, 8)
    total = 0.0
    for j in range(8):
        counts = Counter(raw[:, j].tolist())
        n = raw.shape[0]
        total += -sum(c / n * math.log2(c / n) for c in counts.values())
    return total


def test_entropy() -> float:
    print("  4. Order-0 entropy of byte-split float64 scenario P&L (seed 2026, 100,000 values, sd 100,000 dollars)")
    rng = np.random.default_rng(2026)
    pnl = rng.normal(0.0, 1e5, 100_000)
    raw_bits = stream_entropy_bits(pnl)
    rounded_bits = stream_entropy_bits(np.round(pnl))
    quoted("raw float64: bits per value", raw_bits, 56, 0)
    quoted("raw float64: order-0 ratio", 64.0 / raw_bits, 1.14, 2)
    quoted("rounded to whole dollars: bits per value", rounded_bits, 20.3, 1)
    quoted("rounded to whole dollars: order-0 ratio", 64.0 / rounded_bits, 3.15, 2)
    return 64.0 / raw_bits


# ============================================================================
# 5. Archive sizing
# ============================================================================


def test_sizing(raw_ratio: float) -> None:
    print("  5. Ten-year archive sizing (hypothetical inputs, decimal units)")
    positions, row_width, days, years = 200_000, 400, 252, 10
    daily = positions * row_width / 1e6
    quoted("sensitivity cube per day, uncompressed (MB)", daily, 80.0, 1)
    quoted("sensitivity cube per day at 5:1 (MB)", daily / 5.0, 16.0, 1)
    quoted("sensitivity cube per year at 5:1 (GB)", daily / 5.0 * days / 1e3, 4.03, 2)
    quoted("sensitivity cube, ten years at 5:1 (GB)", daily / 5.0 * days * years / 1e3, 40.3, 1)
    scenarios = 1_000
    grid_day = positions * scenarios * 8 / 1e9
    quoted("scenario P&L per day, uncompressed (GB)", grid_day, 1.6, 1)
    quoted("scenario P&L, ten years uncompressed (TB)", grid_day * days * years / 1e3, 4.03, 2)
    quoted("scenario P&L, ten years at 3:1 (TB)", grid_day * days * years / 1e3 / 3.0, 1.34, 2)
    quoted("scenario P&L, ten years at the raw-float order-0 ratio (TB)", grid_day * days * years / 1e3 / raw_ratio, 3.54, 2)


def main() -> None:
    print("Storage and compute checks")
    test_gorilla_walkthrough()
    test_gorilla_series()
    test_columnar_io()
    raw_ratio = test_entropy()
    test_sizing(raw_ratio)
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All storage and compute checks passed.")


if __name__ == "__main__":
    main()
