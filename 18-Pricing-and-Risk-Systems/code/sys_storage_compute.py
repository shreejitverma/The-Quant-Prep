"""Storage and compute: Gorilla XOR compression, columnar risk cube sizing, and Arrow IPC.

Backs every number in `18-Pricing-and-Risk-Systems/14-Storage-and-Compute.md`.
Gorilla bit encodings, IEEE 754 XOR masks, columnar compression ratios, and 10-year storage volumes are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_storage_compute.py`.
"""

from __future__ import annotations

import struct

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9 * max(1.0, abs(expected))
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def test_gorilla_compression() -> None:
    print("  1. Gorilla floating-point XOR compression walkthrough")
    v0 = 100.00
    v1 = 100.125
    b0 = struct.unpack(">Q", struct.pack(">d", v0))[0]
    b1 = struct.unpack(">Q", struct.pack(">d", v1))[0]
    xor_val = b0 ^ b1

    # Count leading and trailing zeros
    xor_bits = f"{xor_val:064b}"
    leading_zeros = len(xor_bits) - len(xor_bits.lstrip("0"))
    trailing_zeros = len(xor_bits) - len(xor_bits.rstrip("0"))
    meaningful_length = 64 - leading_zeros - trailing_zeros

    total_bits = 1 + 1 + 5 + 6 + meaningful_length  # 1 (nonzero) + 1 (new window) + 5 + 6 + payload
    savings_pct = ((64 - total_bits) / 64.0) * 100.0

    quoted("Price 1 value", v0, 100.00, 2)
    quoted("Price 2 value", v1, 100.125, 3)
    quoted("Gorilla XOR leading zeros", leading_zeros, 20.0, 0)
    quoted("Gorilla XOR trailing zeros", trailing_zeros, 43.0, 0)
    quoted("Gorilla meaningful payload length", meaningful_length, 1.0, 0)
    quoted("Gorilla total encoded bits", total_bits, 14.0, 0)
    quoted("Gorilla bit savings (%)", savings_pct, 78.1, 1)


def test_storage_sizing() -> None:
    print("  2. Enterprise columnar risk cube storage sizing")
    positions = 200_000
    cat_cols = 10
    cat_bytes_each = 4
    num_cols = 45
    num_bytes_each = 8
    row_width = (cat_cols * cat_bytes_each) + (num_cols * num_bytes_each)
    daily_uncompressed_bytes = positions * row_width
    daily_uncompressed_mb = daily_uncompressed_bytes / 1e6

    quoted("daily positions", positions, 200_000, 0)
    quoted("categorical attributes row bytes", cat_cols * cat_bytes_each, 40.0, 0)
    quoted("numerical metrics row bytes", num_cols * num_bytes_each, 360.0, 0)
    quoted("total uncompressed row width (bytes)", row_width, 400.0, 0)
    quoted("daily uncompressed sensitivity volume (MB)", daily_uncompressed_mb, 80.0, 0)

    # Columnar compression (5:1)
    comp_ratio = 5.0
    daily_comp_mb = daily_uncompressed_mb / comp_ratio
    bus_days = 252
    annual_comp_mb = daily_comp_mb * bus_days
    annual_comp_gb = annual_comp_mb / 1000.0  # decimal GB standard or 1024
    ten_year_gb = annual_comp_gb * 10.0

    quoted("daily compressed sensitivity volume (MB)", daily_comp_mb, 16.0, 0)
    quoted("annual compressed volume (MB)", annual_comp_mb, 4_032.0, 0)
    quoted("annual compressed volume (GB)", annual_comp_gb, 4.03, 2)
    quoted("10-year historical sensitivity archive (GB)", ten_year_gb, 40.3, 1)

    # Scenario Grid Storage (1,000 scenarios per trade)
    scenarios = 1_000
    daily_grid_uncomp_bytes = positions * scenarios * 8
    daily_grid_uncomp_gb = daily_grid_uncomp_bytes / 1e9
    grid_comp_ratio = 3.0
    daily_grid_comp_mb = (daily_grid_uncomp_bytes / grid_comp_ratio) / 1e6
    annual_grid_comp_gb = (daily_grid_comp_mb * bus_days) / 1000.0
    ten_year_grid_tb = (annual_grid_comp_gb * 10.0) / 1000.0

    quoted("daily uncompressed scenario grid (GB)", daily_grid_uncomp_gb, 1.6, 1)
    quoted("daily compressed scenario grid (MB)", daily_grid_comp_mb, 533.3, 1)
    quoted("annual compressed scenario grid (GB)", annual_grid_comp_gb, 134.4, 1)
    quoted("10-year historical scenario archive (TB)", ten_year_grid_tb, 1.34, 2)


def main() -> None:
    print("Storage and compute checks")
    test_gorilla_compression()
    test_storage_sizing()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All storage and compute checks passed.")


if __name__ == "__main__":
    main()
