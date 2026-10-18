"""Inflation-linked debt, TIPS index ratio, deflation floor, and breakeven inflation.

Backs every number in `06-Fixed-Income-and-Asset-Classes/21-Inflation-Linked-Products.md`.
TIPS semi-annual coupon calculation, inflation-adjusted principal, terminal deflation floor redemption,
and exact vs approximate Fisher breakeven inflation rates are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_inflation.py`.
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


def tips_index_ratio(cpi_ref: float, cpi_base: float) -> float:
    """TIPS index ratio = Ref CPI / Base CPI."""
    if cpi_base <= 0.0:
        raise ValueError("Base CPI must be positive.")
    return cpi_ref / cpi_base


def tips_cash_flow(
    coupon_rate: float,
    base_principal: float,
    index_ratio: float,
    is_maturity: bool = False,
) -> float:
    """TIPS semi-annual cash flow with deflation floor on terminal principal."""
    semi_coupon = (coupon_rate / 2.0) * base_principal * index_ratio
    if not is_maturity:
        return semi_coupon
    principal_redemption = base_principal * max(1.0, index_ratio)
    return semi_coupon + principal_redemption


def breakeven_inflation_rate(y_nom: float, y_real: float) -> tuple[float, float, float]:
    """Exact Fisher BEIR, approximate BEIR, and spread difference in bps."""
    exact_beir = (1.0 + y_nom) / (1.0 + y_real) - 1.0
    approx_beir = y_nom - y_real
    spread_bps = (approx_beir - exact_beir) * 10_000.0
    return exact_beir, approx_beir, spread_bps


def test_tips_inflation_accrual_example1() -> None:
    print("  1. TIPS Cash Flow with Inflation Accrual (Example 1)")
    base_par = 1000.0
    real_coupon = 0.020  # 2.0% semi-annual
    base_cpi = 300.0
    ref_cpi = 315.0

    idx_ratio = tips_index_ratio(ref_cpi, base_cpi)
    quoted("Index Ratio", idx_ratio, 1.0500, 4)
    quoted("Index Ratio (%)", idx_ratio * 100.0, 105.0, 1)

    adj_principal = base_par * idx_ratio
    quoted("Adjusted Principal ($)", adj_principal, 1050.00, 2)

    coupon_payment = (real_coupon / 2.0) * adj_principal
    quoted("Semi-Annual Coupon ($)", coupon_payment, 10.50, 2)

    terminal_cf = coupon_payment + adj_principal
    quoted("Terminal Cash Flow ($)", terminal_cf, 1060.50, 2)


def test_tips_deflation_floor_example2() -> None:
    print("  2. TIPS Deflation Floor Protection (Example 2)")
    base_par = 1000.0
    real_coupon = 0.020
    base_cpi = 300.0
    deflation_cpi = 285.0

    idx_ratio_defl = tips_index_ratio(deflation_cpi, base_cpi)
    quoted("Deflation Index Ratio", idx_ratio_defl, 0.9500, 4)
    quoted("Deflation Index Ratio (%)", idx_ratio_defl * 100.0, 95.0, 1)

    coupon_defl = (real_coupon / 2.0) * base_par * idx_ratio_defl
    quoted("Deflated Coupon ($)", coupon_defl, 9.50, 2)

    principal_redeemed = base_par * max(1.0, idx_ratio_defl)
    quoted("Principal Redemption under Floor ($)", principal_redeemed, 1000.00, 2)

    total_terminal_defl = coupon_defl + principal_redeemed
    quoted("Total Terminal Cash Flow ($)", total_terminal_defl, 1009.50, 2)


def test_breakeven_inflation_example3() -> None:
    print("  3. Breakeven Inflation Rate Calculation (Example 3)")
    y_nom = 0.0425  # 4.25% nominal 10y Treasury yield
    y_real = 0.0185  # 1.85% real 10y TIPS yield

    exact_beir, approx_beir, spread_bps = breakeven_inflation_rate(y_nom, y_real)

    quoted("Exact Fisher BEIR (%)", exact_beir * 100.0, 2.3564, 4)
    quoted("Exact Fisher BEIR (bps)", exact_beir * 10_000.0, 235.64, 2)
    quoted("Approximate BEIR (%)", approx_beir * 100.0, 2.4000, 4)
    quoted("Approximate BEIR (bps)", approx_beir * 10_000.0, 240.00, 2)
    quoted("Approximation Overstatement (bps)", spread_bps, 4.36, 2)


def main() -> None:
    print("=== fi_inflation: Inflation-Linked Products and TIPS ===")
    test_tips_inflation_accrual_example1()
    test_tips_deflation_floor_example2()
    test_breakeven_inflation_example3()
    print(f"\nSuccessfully verified {len(QUOTED)} inflation and TIPS figures.")


if __name__ == "__main__":
    main()
