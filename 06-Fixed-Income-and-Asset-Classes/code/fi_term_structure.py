"""Term structure models: HJM drift condition, LGM separable kernel, and LMM terminal measure.

Backs every number in `06-Fixed-Income-and-Asset-Classes/19-Term-Structure-Models-HJM-LGM-LMM.md`.
Ho-Lee and Hull-White HJM no-arbitrage forward rate drifts, LGM bond pricing formula,
and Libor Market Model (LMM) terminal measure drift dynamics are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_term_structure.py`.
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


def test_hjm_drifts() -> None:
    print("  1. Heath-Jarrow-Morton (HJM) Drift Conditions (Examples 1 & 2)")
    # Example 1: Constant volatility Ho-Lee HJM drift
    sigma_hl = 0.0150
    t = 1.0
    t_mat = 3.0
    dt_hl = t_mat - t
    alpha_hl = (sigma_hl**2) * dt_hl
    quoted("Ho-Lee sigma^2 * (T - t)", alpha_hl, 0.000450, 6)

    # Example 2: Hull-White exponentially decaying volatility HJM drift
    sigma_hw = 0.0120
    a_hw = 0.03
    dt_hw = 2.0
    decay = math.exp(-a_hw * dt_hw)
    bracket_hw = 1.0 - decay
    alpha_hw = ((sigma_hw**2) / a_hw) * decay * bracket_hw
    quoted("Hull-White HJM drift alpha(t, T)", alpha_hw, 0.000263, 6)


def test_lgm_separable_bond_pricing() -> None:
    print("  2. Linear Gauss-Markov (LGM) Bond Pricing")
    # LGM bond formula: P(t, T) = (P(0, T) / P(0, t)) * exp(-(H(T) - H(t))*x - 0.5*(H(T)^2 - H(t)^2)*zeta)
    a = 0.03
    sigma_hw = 0.0120
    t = 1.0
    t_mat = 5.0

    def h_func(mat: float) -> float:
        return (1.0 - math.exp(-a * mat)) / a

    h_t = h_func(t)
    h_tmat = h_func(t_mat)
    delta_h = h_tmat - h_t
    quoted("H(1.0)", h_t, 0.985149, 6)
    quoted("H(5.0)", h_tmat, 4.643067, 6)
    quoted("H(5.0) - H(1.0)", delta_h, 3.657919, 6)

    zeta_t = (sigma_hw**2) * (math.exp(2.0 * a * t) - 1.0) / (2.0 * a)
    quoted("LGM variance zeta(t=1)", zeta_t, 0.000148, 6)

    # Baseline flat zero curve at 4%
    p_0_t = math.exp(-0.04 * t)
    p_0_tmat = math.exp(-0.04 * t_mat)
    fwd_df = p_0_tmat / p_0_t
    quoted("Baseline forward discount P(0, 5)/P(0, 1)", fwd_df, 0.852144, 6)

    # Bond price at state x = 0
    convexity_adj = math.exp(-0.5 * (h_tmat**2 - h_t**2) * zeta_t)
    p_t_tmat_x0 = fwd_df * convexity_adj
    quoted("LGM bond price P(1, 5) at x=0", p_t_tmat_x0, 0.850843, 6)


def test_lmm_terminal_drift_example3() -> None:
    print("  3. 2-Factor LMM Drift Dynamics (Example 3)")
    tau2 = 0.25
    l2 = 0.040
    l1 = 0.040
    sigma1 = 0.200
    sigma2 = 0.180
    rho12 = 0.85

    denom = 1.0 + tau2 * l2
    num = tau2 * l2
    cov = sigma1 * sigma2 * rho12
    ratio = num / denom
    mu1 = -ratio * cov
    abs_drift = l1 * mu1
    abs_drift_bps = abs_drift * 10_000.0

    quoted("1 + tau2 * L2", denom, 1.0100, 4)
    quoted("tau2 * L2", num, 0.0100, 4)
    quoted("sigma1 * sigma2 * rho12", cov, 0.0306, 4)
    quoted("tau2 * L2 / (1 + tau2 * L2)", ratio, 0.009901, 6)
    quoted("Relative drift mu1 per year", mu1, -0.000303, 6)
    quoted("Absolute drift dL1/dt", abs_drift, -0.0000121, 7)
    quoted("Absolute drift (bps per year)", abs_drift_bps, -0.12, 2)


def main() -> None:
    print("=== fi_term_structure: Term Structure Models (HJM, LGM, LMM) ===")
    test_hjm_drifts()
    test_lgm_separable_bond_pricing()
    test_lmm_terminal_drift_example3()
    print(f"\nSuccessfully verified {len(QUOTED)} term structure figures.")


if __name__ == "__main__":
    main()
