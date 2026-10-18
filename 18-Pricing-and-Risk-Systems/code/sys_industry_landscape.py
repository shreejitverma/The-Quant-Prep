"""Industry landscape: Total Cost of Ownership (TCO) buy-vs-build, NPV, and hybrid architectures.

Backs every number in `18-Pricing-and-Risk-Systems/17-Industry-Landscape.md`.
Nominal 5-year cash flows, discounted net present values, hybrid tier economics, and ORE grid sizing are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_industry_landscape.py`.
"""

from __future__ import annotations

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def test_nominal_tco() -> None:
    print("  1. 5-Year Nominal Total Cost of Ownership: Vendor vs In-House")
    # Option A: Commercial Vendor (Murex MX.3)
    v_upfront_lic = 12_000_000.0
    v_impl = 18_000_000.0
    v_ann_lic = 4_500_000.0
    v_dev_count = 15
    v_dev_comp = 300_000.0
    v_ann_dev = v_dev_count * v_dev_comp  # 4,500,000
    v_ann_infra = 1_500_000.0

    v_y1 = v_upfront_lic + v_impl + v_ann_lic + v_ann_dev + v_ann_infra  # 40,500,000
    v_ann_recurring = v_ann_lic + v_ann_dev + v_ann_infra  # 10,500,000
    v_y2_5 = 4.0 * v_ann_recurring  # 42,000,000
    v_total_tco = v_y1 + v_y2_5  # 82,500,000

    quoted("vendor year 1 cost ($)", v_y1, 40_500_000.0, 0)
    quoted("vendor annual recurring cost ($)", v_ann_recurring, 10_500_000.0, 0)
    quoted("vendor years 2 to 5 cost ($)", v_y2_5, 42_000_000.0, 0)
    quoted("vendor 5-year total TCO ($)", v_total_tco, 82_500_000.0, 0)

    # Option B: In-House Build (Athena / Quartz Style)
    b_impl = 14_000_000.0
    b_dev_count = 45
    b_dev_comp = 300_000.0
    b_ann_dev = b_dev_count * b_dev_comp  # 13,500,000
    b_ann_infra = 2_000_000.0

    b_y1 = b_impl + b_ann_dev + b_ann_infra  # 29,500,000
    b_ann_recurring = b_ann_dev + b_ann_infra  # 15,500,000
    b_y2_5 = 4.0 * b_ann_recurring  # 62,000,000
    b_total_tco = b_y1 + b_y2_5  # 91,500,000

    quoted("in-house year 1 cost ($)", b_y1, 29_500_000.0, 0)
    quoted("in-house annual recurring cost ($)", b_ann_recurring, 15_500_000.0, 0)
    quoted("in-house years 2 to 5 cost ($)", b_y2_5, 62_000_000.0, 0)
    quoted("in-house 5-year total TCO ($)", b_total_tco, 91_500_000.0, 0)

    # Cost differential
    nominal_delta = b_total_tco - v_total_tco  # 9,000,000
    nominal_pct = (nominal_delta / b_total_tco) * 100.0  # 9.836%

    quoted("nominal TCO delta ($)", nominal_delta, 9_000_000.0, 0)
    quoted("vendor savings relative to in-house (%)", nominal_pct, 9.8, 1)


def test_discounted_npv_tco() -> None:
    print("  2. Discounted Net Present Value (NPV) TCO at 8% Discount Rate")
    r = 0.08
    df = [1.0 / ((1.0 + r) ** t) for t in range(1, 6)]

    # Option A (Vendor) cash flows across Years 1 to 5:
    v_cfs = [40_500_000.0, 10_500_000.0, 10_500_000.0, 10_500_000.0, 10_500_000.0]
    v_npv = sum(cf * d for cf, d in zip(v_cfs, df, strict=True))

    # Option B (In-House) cash flows across Years 1 to 5:
    b_cfs = [29_500_000.0, 15_500_000.0, 15_500_000.0, 15_500_000.0, 15_500_000.0]
    b_npv = sum(cf * d for cf, d in zip(b_cfs, df, strict=True))

    npv_delta = b_npv - v_npv
    npv_pct = (npv_delta / b_npv) * 100.0

    quoted("vendor discounted TCO ($)", v_npv, 69_701_233.0, 0)
    quoted("in-house discounted TCO ($)", b_npv, 74_849_969.0, 0)
    quoted("discounted NPV delta ($)", npv_delta, 5_148_735.0, 0)
    quoted("discounted vendor savings relative to in-house (%)", npv_pct, 6.9, 1)


def test_hybrid_architecture_tco() -> None:
    print("  3. Modern Hybrid Architecture TCO: Vendor Back-Office + Open-Source In-House Front-Office")
    # Commodity Back-Office (Vendor Calypso for settlement/clearing):
    h_back_lic = 1_200_000.0
    h_back_dev = 4 * 300_000.0  # 1,200,000

    # Proprietary Front-Office / XVA (QuantLib / ORE core):
    h_front_impl_y1 = 5_000_000.0
    h_front_dev = 20 * 300_000.0  # 6,000,000
    h_front_infra = 1_200_000.0

    h_y1 = h_front_impl_y1 + (h_back_lic + h_back_dev) + (h_front_dev + h_front_infra)  # 14,600,000
    h_ann_recurring = (h_back_lic + h_back_dev) + (h_front_dev + h_front_infra)  # 9,600,000
    h_y2_5 = 4.0 * h_ann_recurring  # 38,400,000
    h_total_tco = h_y1 + h_y2_5  # 53,000,000

    r = 0.08
    df = [1.0 / ((1.0 + r) ** t) for t in range(1, 6)]
    h_cfs = [h_y1] + [h_ann_recurring] * 4
    h_npv = sum(cf * d for cf, d in zip(h_cfs, df, strict=True))

    savings_vs_vendor = 82_500_000.0 - h_total_tco  # 29,500,000
    savings_vs_inhouse = 91_500_000.0 - h_total_tco  # 38,500,000
    savings_pct_vendor = (savings_vs_vendor / 82_500_000.0) * 100.0  # 35.8%
    savings_pct_inhouse = (savings_vs_inhouse / 91_500_000.0) * 100.0  # 42.1%

    quoted("hybrid year 1 cost ($)", h_y1, 14_600_000.0, 0)
    quoted("hybrid annual recurring cost ($)", h_ann_recurring, 9_600_000.0, 0)
    quoted("hybrid 5-year total TCO ($)", h_total_tco, 53_000_000.0, 0)
    quoted("hybrid discounted TCO ($)", h_npv, 42_959_646.0, 0)
    quoted("hybrid savings vs pure vendor ($)", savings_vs_vendor, 29_500_000.0, 0)
    quoted("hybrid savings vs pure in-house ($)", savings_vs_inhouse, 38_500_000.0, 0)
    quoted("hybrid savings relative to vendor (%)", savings_pct_vendor, 35.8, 1)
    quoted("hybrid savings relative to in-house (%)", savings_pct_inhouse, 42.1, 1)


def test_ore_simulation_sizing() -> None:
    print("  4. Open Risk Engine (ORE) Enterprise Simulation Grid Sizing")
    trades = 5_000
    netting_sets = 12
    paths = 10_000
    timesteps = 80
    bytes_per_float = 8

    total_pricings = trades * paths * timesteps  # 4,000,000,000
    pricing_micros = 50.0
    total_cpu_seconds = (total_pricings * pricing_micros) / 1_000_000.0  # 200,000
    total_cpu_hours = total_cpu_seconds / 3600.0  # 55.56 hours

    cores = 128
    wall_clock_minutes = (total_cpu_seconds / cores) / 60.0  # 26.04 minutes

    # Exposure matrix storage: netting_sets x timesteps x paths x 8 bytes
    exposure_bytes = netting_sets * timesteps * paths * bytes_per_float
    exposure_mb = exposure_bytes / (1024.0 * 1024.0)  # 73.24 MB

    quoted("total trade evaluations (billions)", total_pricings / 1e9, 4.0, 1)
    quoted("total compute budget (core-seconds)", total_cpu_seconds, 200_000.0, 0)
    quoted("total compute budget (core-hours)", total_cpu_hours, 55.6, 1)
    quoted("parallel runtime on 128 cores (minutes)", wall_clock_minutes, 26.0, 1)
    quoted("exposure matrix resident RAM (MB)", exposure_mb, 73.2, 1)


def main() -> None:
    print("=== sys_industry_landscape: Total Cost of Ownership and Open Source Architecture ===")
    test_nominal_tco()
    test_discounted_npv_tco()
    test_hybrid_architecture_tco()
    test_ore_simulation_sizing()
    print(f"\nSuccessfully verified {len(QUOTED)} industry landscape figures.")


if __name__ == "__main__":
    main()
