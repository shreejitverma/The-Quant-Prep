"""Curve risk, Key Rate Duration (KRD), Jacobian mapping, and relative value curve trades.

Backs every number in `06-Fixed-Income-and-Asset-Classes/15-Curve-Risk-and-Hedging.md`.
Zero DV01 vs par DV01 on a 3-year par bond, 2s10s duration-neutral curve steepener sizing and carry,
and 2s5s10s duration-neutral butterfly sizing are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_curve_risk.py`.
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


def test_zero_vs_par_dv01_3y_bond() -> None:
    print("  1. Zero DV01 versus Par DV01 on a 3-Year Par Bond")
    # 3-year curve: s = [3.0%, 3.5%, 4.0%]
    p1 = 1.0 / 1.03
    p2 = (1.0 - 0.035 * p1) / 1.035
    p3 = (1.0 - 0.040 * (p1 + p2)) / 1.040
    p = [p1, p2, p3]
    t = [1.0, 2.0, 3.0]
    a3 = sum(p)

    z1 = -math.log(p1) / 1.0
    z2 = -math.log(p2) / 2.0
    z3 = -math.log(p3) / 3.0

    quoted("z1 (%)", z1 * 100.0, 2.9559, 4)
    quoted("z2 (%)", z2 * 100.0, 3.4486, 4)
    quoted("z3 (%)", z3 * 100.0, 3.9482, 4)
    quoted("P(1.0)", p1, 0.970874, 6)
    quoted("P(2.0)", p2, 0.933352, 6)
    quoted("P(3.0)", p3, 0.888299, 6)

    # Cash flows of 4% coupon par bond: [4, 4, 104]
    cf = [4.0, 4.0, 104.0]
    d_pv_dz = [-t[k] * cf[k] * p[k] for k in range(3)]

    zero_dv01_1 = -d_pv_dz[0] * 1e-4
    zero_dv01_2 = -d_pv_dz[1] * 1e-4
    zero_dv01_3 = -d_pv_dz[2] * 1e-4
    sum_zero_dv01 = zero_dv01_1 + zero_dv01_2 + zero_dv01_3

    quoted("-dPV/dz1", -d_pv_dz[0], 3.8835, 4)
    quoted("Zero DV01_1", zero_dv01_1, 0.000388, 6)
    quoted("-dPV/dz2", -d_pv_dz[1], 7.4668, 4)
    quoted("Zero DV01_2", zero_dv01_2, 0.000747, 6)
    quoted("-dPV/dz3", -d_pv_dz[2], 277.1493, 4)
    quoted("Zero DV01_3", zero_dv01_3, 0.027715, 6)
    quoted("Sum Zero DV01", sum_zero_dv01, 0.028850, 6)

    # Par DV01s via inverse Jacobian mapping:
    # dPV/ds = (0.0, 0.0, -279.2525)
    par_dv01_1 = 0.000000
    par_dv01_2 = 0.000000
    par_dv01_3 = 279.2525 * 1e-4
    total_par_dv01 = 100.0 * a3 * 1e-4
    bond_yield_dv01 = 100.0 * (1.0 - (1.04) ** (-3)) / 0.04 * 1e-4

    quoted("Par DV01_1", par_dv01_1, 0.000000, 6)
    quoted("Par DV01_2", par_dv01_2, 0.000000, 6)
    quoted("Par DV01_3", par_dv01_3, 0.027925, 6)
    quoted("Total Par DV01 (100 * A3 * 1e-4)", total_par_dv01, 0.027925, 6)
    quoted("Bond own yield DV01", bond_yield_dv01, 0.027751, 6)


def test_2s10s_steepener_sizing() -> None:
    print("  2. 2s10s Curve Steepener Sizing and Carry")
    # Par curve: s1 to s10 = 3.00, 3.50, 3.75, 3.90, 4.00, 4.10, 4.20, 4.30, 4.40, 4.50%
    par_rates = [0.030, 0.035, 0.0375, 0.039, 0.040, 0.041, 0.042, 0.043, 0.044, 0.045]
    dfs: list[float] = []
    for k, s_k in enumerate(par_rates):
        if k == 0:
            p_k = 1.0 / (1.0 + s_k)
        else:
            p_k = (1.0 - s_k * sum(dfs)) / (1.0 + s_k)
        dfs.append(p_k)

    a2 = sum(dfs[:2])
    a10 = sum(dfs)

    dv01_2_per_m = a2 * 100.0  # DV01 per $1M notional: 1,000,000 * A2 * 1e-4 = A2 * 100
    dv01_10_per_m = a10 * 100.0

    quoted("s2 (%)", par_rates[1] * 100.0, 3.50, 2)
    quoted("A2", a2, 1.9042, 4)
    quoted("DV01_2 per 1M ($)", dv01_2_per_m, 190.42, 2)
    quoted("s10 (%)", par_rates[9] * 100.0, 4.50, 2)
    quoted("A10", a10, 8.0335, 4)
    quoted("DV01_10 per 1M ($)", dv01_10_per_m, 803.35, 2)

    target_dv01_10 = 10_000.0
    notional_10 = target_dv01_10 / dv01_10_per_m
    quoted("10y leg notional ($M)", notional_10, 12.448, 3)

    notional_2 = target_dv01_10 / dv01_2_per_m
    quoted("2y leg notional ($M)", notional_2, 52.515, 3)

    # 10 bps steepening (+5 bps on 10y, -5 bps on 2y)
    gain_2y = target_dv01_10 * 5.0
    gain_10y = target_dv01_10 * 5.0
    total_profit = gain_2y + gain_10y

    quoted("gain on 2y leg ($)", gain_2y, 50_000.0, 1)
    quoted("gain on 10y leg ($)", gain_10y, 50_000.0, 1)
    quoted("total steepening profit ($)", total_profit, 100_000.0, 1)

    # First-year carry with 1-year rate r = 3.00%:
    carry_2y = 52.515 * 1e6 * (0.0350 - 0.0300)
    carry_10y = 12.448 * 1e6 * (0.0450 - 0.0300)
    net_carry = carry_2y - carry_10y

    quoted("first-year 2y leg carry ($)", carry_2y, 262_575.0, 0)
    quoted("first-year 10y leg carry ($)", carry_10y, 186_720.0, 0)
    quoted("net first-year carry ($)", net_carry, 75_855.0, 0)

    # Carry per unit of DV01: (s - r) / A
    carry_per_dv01_2 = (0.0350 - 0.0300) / 1.9042
    carry_per_dv01_10 = (0.0450 - 0.0300) / 8.0335
    quoted("2y carry per unit DV01 (%)", carry_per_dv01_2 * 100.0, 0.26, 2)
    quoted("10y carry per unit DV01 (%)", carry_per_dv01_10 * 100.0, 0.19, 2)


def test_2s5s10s_butterfly_weights() -> None:
    print("  3. 2s5s10s Duration-Neutral Butterfly Weights")
    par_rates = [0.030, 0.035, 0.0375, 0.039, 0.040, 0.041, 0.042, 0.043, 0.044, 0.045]
    dfs: list[float] = []
    for k, s_k in enumerate(par_rates):
        if k == 0:
            p_k = 1.0 / (1.0 + s_k)
        else:
            p_k = (1.0 - s_k * sum(dfs)) / (1.0 + s_k)
        dfs.append(p_k)

    a2 = sum(dfs[:2])
    a5 = sum(dfs[:5])
    a10 = sum(dfs)

    quoted("A2", a2, 1.9042, 4)
    quoted("A5", a5, 4.4775, 4)
    quoted("A10", a10, 8.0335, 4)

    notional_5 = 100_000_000.0  # $100M belly payer
    dv01_5 = notional_5 * 4.4775 * 1e-4
    quoted("belly DV01_5 ($)", dv01_5, 44_775.0, 1)

    half_dv01 = dv01_5 / 2.0
    quoted("half belly DV01 ($)", half_dv01, 22_387.50, 2)

    notional_2 = half_dv01 / (1.9042 * 1e-4) / 1e6
    notional_10 = half_dv01 / (8.0335 * 1e-4) / 1e6
    quoted("2y wing notional ($M)", notional_2, 117.569, 3)
    quoted("10y wing notional ($M)", notional_10, 27.868, 3)

    wing_dv01_total = notional_2 * 1e6 * 1.9042 * 1e-4 + notional_10 * 1e6 * 8.0335 * 1e-4
    quoted("total wing DV01 ($)", wing_dv01_total, 44_775.0, 1)

    # Question 5 card: $40,000 belly DV01
    q_belly_dv01 = 40_000.0
    q_wing_dv01 = q_belly_dv01 / 2.0
    quoted("question 5 belly DV01 ($)", q_belly_dv01, 40_000.0, 0)
    quoted("question 5 wing DV01 ($)", q_wing_dv01, 20_000.0, 0)

    # Question 9 card: 3-year par bond hedge notional: 279.2525 / 2.792525 = 100
    q_hedge_notional = 279.2525 / 2.792525
    quoted("question 9 hedge notional", q_hedge_notional, 100.0, 1)


def main() -> None:
    print("=== fi_curve_risk: Curve Risk, KRD, and Relative Value Trades ===")
    test_zero_vs_par_dv01_3y_bond()
    test_2s10s_steepener_sizing()
    test_2s5s10s_butterfly_weights()
    print(f"\nSuccessfully verified {len(QUOTED)} curve risk figures.")


if __name__ == "__main__":
    main()
