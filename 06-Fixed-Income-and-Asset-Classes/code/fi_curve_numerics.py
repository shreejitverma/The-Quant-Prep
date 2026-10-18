"""Yield curve construction numerics, forward rate jumps, and analytical Jacobian.

Backs every number in `06-Fixed-Income-and-Asset-Classes/14-Curve-Construction-Numerics.md`.
Log-linear discount factor forward jumps, analytical calibration Jacobian elements,
inverse Jacobian via forward substitution, and par bond sensitivity transformations are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_curve_numerics.py`.
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


def test_loglinear_forward_jumps() -> None:
    print("  1. Log-Linear Discount Factor Interpolation and Forward Jumps")
    s1 = 0.030
    s2 = 0.035
    s3 = 0.040

    p1 = 1.0 / (1.0 + s1)
    p2 = (1.0 - s2 * p1) / (1.0 + s2)
    p3 = (1.0 - s3 * (p1 + p2)) / (1.0 + s3)

    quoted("P(1.0)", p1, 0.970874, 6)
    quoted("P(2.0)", p2, 0.933352, 6)
    quoted("P(3.0)", p3, 0.888299, 6)

    f1 = -math.log(p1) / 1.0
    ratio_12 = 0.933352 / 0.970874
    f2 = -math.log(p2 / p1) / (2.0 - 1.0)
    ratio_23 = 0.888299 / 0.933352
    f3 = -math.log(p3 / p2) / (3.0 - 2.0)

    quoted("f_1 (%)", f1 * 100.0, 2.9559, 4)
    quoted("ratio P2/P1", ratio_12, 0.961352, 6)
    quoted("f_2 (%)", f2 * 100.0, 3.9414, 4)
    quoted("ratio P3/P2", ratio_23, 0.951730, 6)
    quoted("f_3 (%)", f3 * 100.0, 4.9474, 4)

    jump_1 = (f2 - f1) * 10_000.0
    jump_2 = (f3 - f2) * 10_000.0
    quoted("forward jump at t=1.0 (bps)", jump_1, 98.55, 2)
    quoted("forward jump at t=2.0 (bps)", jump_2, 100.60, 2)

    # Flat zero extrapolation beyond T3
    z3 = -math.log(p3) / 3.0
    quoted("flat zero rate z3 (%)", z3 * 100.0, 3.9482, 4)


def test_analytical_jacobian() -> None:
    print("  2. Analytical Calibration Jacobian Matrix Construction")
    s = [0.030, 0.035, 0.040]
    p1 = 1.0 / 1.03
    p2 = (1.0 - 0.035 * p1) / 1.035
    p3 = (1.0 - 0.040 * (p1 + p2)) / 1.040
    p = [p1, p2, p3]
    t = [1.0, 2.0, 3.0]

    a1 = p[0]
    a2 = p[0] + p[1]
    a3 = p[0] + p[1] + p[2]
    a = [a1, a2, a3]

    quoted("annuity A1", a1, 0.970874, 6)
    quoted("annuity A2", a2, 1.904226, 6)
    quoted("annuity A3", a3, 2.792525, 6)

    # Row 1 (1-year swap)
    ds1_dp1 = -(1.0 + s[0]) / a[0]
    dp1_dz1 = -t[0] * p[0]
    j11 = ds1_dp1 * dp1_dz1
    quoted("ds1/dP1", ds1_dp1, -1.060900, 6)
    quoted("dP1/dz1", dp1_dz1, -0.970874, 6)
    quoted("J_1,1", j11, 1.030000, 6)

    # Row 2 (2-year swap)
    ds2_dp1 = -s[1] / a[1]
    j21 = ds2_dp1 * (-t[0] * p[0])
    ds2_dp2 = -(1.0 + s[1]) / a[1]
    dp2_dz2 = -t[1] * p[1]
    j22 = ds2_dp2 * dp2_dz2
    quoted("ds2/dP1", ds2_dp1, -0.018380, 6)
    quoted("J_2,1", j21, 0.017845, 6)
    quoted("ds2/dP2", ds2_dp2, -0.543528, 6)
    quoted("J_2,2", j22, 1.014606, 6)

    # Row 3 (3-year swap)
    ds3_dp1 = -s[2] / a[2]
    j31 = ds3_dp1 * (-t[0] * p[0])
    ds3_dp2 = -s[2] / a[2]
    j32 = ds3_dp2 * (-t[1] * p[1])
    ds3_dp3 = -(1.0 + s[2]) / a[2]
    dp3_dz3 = -t[2] * p[2]
    j33 = ds3_dp3 * dp3_dz3
    quoted("ds3/dP1", ds3_dp1, -0.014324, 6)
    quoted("J_3,1", j31, 0.013907, 6)
    quoted("ds3/dP2", ds3_dp2, -0.014324, 6)
    quoted("J_3,2", j32, 0.026739, 6)
    quoted("ds3/dP3", ds3_dp3, -0.372423, 6)
    quoted("J_3,3", j33, 0.992468, 6)


def test_inverse_jacobian_and_risk_mapping() -> None:
    print("  3. Inverse Jacobian and Par Market Risk Mapping")
    # Analytical inversion of lower triangular 3x3 matrix J
    # J = [[j11, 0, 0], [j21, j22, 0], [j31, j32, j33]]
    # Computed from exact values:
    s = [0.030, 0.035, 0.040]
    p1 = 1.0 / 1.03
    p2 = (1.0 - 0.035 * p1) / 1.035
    p3 = (1.0 - 0.040 * (p1 + p2)) / 1.040
    p = [p1, p2, p3]
    t = [1.0, 2.0, 3.0]
    a = [p[0], p[0] + p[1], p[0] + p[1] + p[2]]

    j11 = (-(1.0 + s[0]) / a[0]) * (-t[0] * p[0])
    j21 = (-s[1] / a[1]) * (-t[0] * p[0])
    j22 = (-(1.0 + s[1]) / a[1]) * (-t[1] * p[1])
    j31 = (-s[2] / a[2]) * (-t[0] * p[0])
    j32 = (-s[2] / a[2]) * (-t[1] * p[1])
    j33 = (-(1.0 + s[2]) / a[2]) * (-t[2] * p[2])

    inv11 = 1.0 / j11
    inv21 = -j21 / (j11 * j22)
    inv22 = 1.0 / j22
    inv31 = (j21 * j32 - j31 * j22) / (j11 * j22 * j33)
    inv32 = -j32 / (j22 * j33)
    inv33 = 1.0 / j33

    quoted("J_inv_1,1", inv11, 0.970874, 6)
    quoted("J_inv_2,1", inv21, -0.017076, 6)
    quoted("J_inv_2,2", inv22, 0.985604, 6)
    quoted("J_inv_3,1", inv31, -0.013144, 6)
    quoted("J_inv_3,2", inv32, -0.026554, 6)
    quoted("J_inv_3,3", inv33, 1.007589, 6)

    # 3-year par bond cash flows [4, 4, 104]
    cf = [4.0, 4.0, 104.0]
    d_pv_dz1 = -t[0] * cf[0] * p[0]
    d_pv_dz2 = -t[1] * cf[1] * p[1]
    d_pv_dz3 = -t[2] * cf[2] * p[2]

    quoted("dPV/dz1", d_pv_dz1, -3.8835, 4)
    quoted("dPV/dz2", d_pv_dz2, -7.4668, 4)
    quoted("dPV/dz3", d_pv_dz3, -277.1493, 4)

    # Market par quote sensitivities: dPV/ds_j = sum_k dPV/dz_k * J_inv_k,j
    # dPV/ds_1 components:
    term1_1 = d_pv_dz1 * inv11
    term1_2 = d_pv_dz2 * inv21
    term1_3 = d_pv_dz3 * inv31
    d_pv_ds1 = term1_1 + term1_2 + term1_3

    quoted("term1_1", term1_1, -3.7704, 4)
    quoted("term1_2", term1_2, 0.1275, 4)
    quoted("term1_3", term1_3, 3.6429, 4)
    quoted("dPV/ds1", d_pv_ds1, 0.0000, 4)

    # dPV/ds_2 components:
    term2_2 = d_pv_dz2 * inv22
    term2_3 = d_pv_dz3 * inv32
    d_pv_ds2 = term2_2 + term2_3

    quoted("term2_2", term2_2, -7.3593, 4)
    quoted("term2_3", term2_3, 7.3593, 4)
    quoted("dPV/ds2", d_pv_ds2, 0.0000, 4)

    # dPV/ds_3 component:
    d_pv_ds3 = d_pv_dz3 * inv33
    quoted("dPV/ds3", d_pv_ds3, -279.2525, 4)
    quoted("expected -100 * A3", -100.0 * a[2], -279.2525, 4)


def main() -> None:
    print("=== fi_curve_numerics: Curve Construction Numerics and Jacobian ===")
    test_loglinear_forward_jumps()
    test_analytical_jacobian()
    test_inverse_jacobian_and_risk_mapping()
    print(f"\nSuccessfully verified {len(QUOTED)} curve construction figures.")


if __name__ == "__main__":
    main()
