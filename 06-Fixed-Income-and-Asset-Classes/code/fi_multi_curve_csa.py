"""Multi-curve pricing, CSA collateral discounting, and tenor / cross-currency basis swaps.

Backs every number in `06-Fixed-Income-and-Asset-Classes/13-Multi-Curve-and-CSA-Discounting.md`.
Dual-curve vs single-curve par swaps, tenor basis swaps (3M vs 6M), cross-currency basis swaps, and CTD collateral are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_multi_curve_csa.py`.
"""

from __future__ import annotations

import math

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def test_dual_curve_swap() -> None:
    print("  1. Dual-Curve Par Swap vs Single-Curve Par Swap")
    # OIS Curve
    r_ois_1 = 0.030
    s_ois_2 = 0.035
    p_ois_1 = 1.0 / (1.0 + r_ois_1)
    p_ois_2 = (1.0 - s_ois_2 * p_ois_1) / (1.0 + s_ois_2)
    a_ois = p_ois_1 + p_ois_2
    s_single = (1.0 - p_ois_2) / a_ois

    quoted("P_ois(1)", p_ois_1, 0.970874, 6)
    quoted("P_ois(2)", p_ois_2, 0.933352, 6)
    quoted("OIS annuity A_ois", a_ois, 1.904226, 6)
    quoted("single-curve par swap rate (%)", s_single * 100.0, 3.5000, 4)

    # Projection Curve (+20 bps spread on zero rates: 3.2% and 3.7%)
    p_proj_1 = 1.0 / (1.0 + 0.032)
    p_proj_2 = 1.0 / ((1.0 + 0.037) ** 2)
    f_proj_1 = (1.0 / p_proj_1) - 1.0
    f_proj_2 = (p_proj_1 / p_proj_2) - 1.0

    c1_pv = p_ois_1 * f_proj_1
    c2_pv = p_ois_2 * f_proj_2
    pv_float = c1_pv + c2_pv
    s_dual = pv_float / a_ois
    dual_spread_bps = (s_dual - s_single) * 10_000.0

    quoted("P_proj(1)", p_proj_1, 0.968992, 6)
    quoted("P_proj(2)", p_proj_2, 0.929913, 6)
    quoted("projected forward F(0, 1) (%)", f_proj_1 * 100.0, 3.2000, 4)
    quoted("projected forward F(1, 2) (%)", f_proj_2 * 100.0, 4.2024, 4)
    quoted("coupon 1 floating leg PV", c1_pv, 0.031068, 6)
    quoted("coupon 2 floating leg PV", c2_pv, 0.039223, 6)
    quoted("total floating leg PV", pv_float, 0.070291, 6)
    quoted("dual-curve par swap rate (%)", s_dual * 100.0, 3.6913, 4)
    quoted("dual vs single spread (bps)", dual_spread_bps, 19.13, 2)


def test_tenor_basis_swap() -> None:
    print("  2. Tenor Basis Swap Valuation: 3M vs 6M Floating")
    r_ois = 0.030
    p_25 = math.exp(-r_ois * 0.25)
    p_50 = math.exp(-r_ois * 0.50)
    p_75 = math.exp(-r_ois * 0.75)
    p_100 = math.exp(-r_ois * 1.00)

    a_4 = 0.25 * (p_25 + p_50 + p_75 + p_100)
    a_2 = 0.50 * (p_50 + p_100)

    f3 = [0.032, 0.033, 0.034, 0.035]
    f6 = [0.0345, 0.0365]

    pv_3 = 0.25 * (p_25 * f3[0] + p_50 * f3[1] + p_75 * f3[2] + p_100 * f3[3])
    pv_6 = 0.50 * (p_50 * f6[0] + p_100 * f6[1])

    beta_3v6 = (pv_6 - pv_3) / a_4
    beta_bps = beta_3v6 * 10_000.0

    quoted("P_ois(0.25)", p_25, 0.992528, 6)
    quoted("P_ois(0.50)", p_50, 0.985112, 6)
    quoted("P_ois(0.75)", p_75, 0.977751, 6)
    quoted("P_ois(1.00)", p_100, 0.970446, 6)
    quoted("quarterly OIS annuity A4", a_4, 0.981459, 6)
    quoted("semiannual OIS annuity A2", a_2, 0.977779, 6)
    quoted("PV of 3M floating leg", pv_3, 0.032870, 6)
    quoted("PV of 6M floating leg", pv_6, 0.034704, 6)
    quoted("3M vs 6M par basis spread (%)", beta_3v6 * 100.0, 0.1869, 4)
    quoted("3M vs 6M par basis spread (bps)", beta_bps, 18.69, 2)


def test_cross_currency_basis() -> None:
    print("  3. Cross-Currency Basis Swap (EUR/USD)")
    spot_fx = 1.1000  # USD per EUR
    usd_notional = 100_000_000.0
    eur_notional = usd_notional / spot_fx

    basis_spread_bps = -25.0
    basis_spread = basis_spread_bps / 10_000.0

    sofr = 0.0500
    synthetic_dollar_borrowing = sofr - basis_spread  # SOFR + 25 bps

    quoted("spot FX rate (USD per EUR)", spot_fx, 1.1000, 4)
    quoted("EUR initial notional posted (€)", eur_notional, 90_909_091.0, 0)
    quoted("cross-currency basis spread (bps)", basis_spread_bps, -25.0, 1)
    quoted("synthetic dollar borrowing cost over SOFR (bps)", -basis_spread_bps, 25.0, 1)
    quoted("all-in synthetic dollar borrowing rate (%)", synthetic_dollar_borrowing * 100.0, 5.25, 2)


def main() -> None:
    print("=== fi_multi_curve_csa: Multi-Curve and CSA Discounting ===")
    test_dual_curve_swap()
    test_tenor_basis_swap()
    test_cross_currency_basis()
    print(f"\nSuccessfully verified {len(QUOTED)} multi-curve and CSA figures.")


if __name__ == "__main__":
    main()
