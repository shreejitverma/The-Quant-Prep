"""SABR stochastic volatility model, Hagan asymptotic smile formula, and shifted SABR.

Backs every number in `06-Fixed-Income-and-Asset-Classes/18-Rates-Volatility-and-SABR.md`.
Hagan asymptotic lognormal volatility formula, parameter sensitivities (vol-of-vol, skew, backbone),
and shifted SABR for negative rates are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_sabr.py`.
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


def sabr_hagan_lognormal_vol(
    f: float,
    k: float,
    t_exp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. (2002) asymptotic implied Black volatility for SABR."""
    if f <= 0.0 or k <= 0.0:
        raise ValueError("Forward and strike must be positive.")
    if t_exp <= 0.0:
        return alpha / (f ** (1.0 - beta))

    one_minus_beta = 1.0 - beta

    # ATM special case
    if abs(f - k) < 1e-8:
        fk_mid = f**one_minus_beta
        term1 = alpha / fk_mid
        factor2 = (
            (one_minus_beta**2 / 24.0) * (alpha * alpha) / (f ** (2.0 * one_minus_beta))
            + 0.25 * rho * beta * nu * alpha / (f**one_minus_beta)
            + ((2.0 - 3.0 * rho * rho) / 24.0) * (nu * nu)
        )
        return term1 * (1.0 + factor2 * t_exp)

    log_fk = math.log(f / k)
    fk = f * k
    fk_pow = fk ** (one_minus_beta * 0.5)

    z = (nu / alpha) * fk_pow * log_fk

    if abs(z) < 1e-6:
        z_over_x = 1.0
    else:
        disc = 1.0 - 2.0 * rho * z + z * z
        sqrt_disc = math.sqrt(max(0.0, disc))
        arg = (sqrt_disc + z - rho) / (1.0 - rho)
        if arg <= 0.0:
            return alpha / fk_pow
        chi_z = math.log(arg)
        z_over_x = z / chi_z

    denom_bracket = 1.0 + (one_minus_beta**2 / 24.0) * (log_fk**2) + (one_minus_beta**4 / 1920.0) * (log_fk**4)
    prefactor = (alpha / (fk_pow * denom_bracket)) * z_over_x

    gamma = (
        (one_minus_beta**2 / 24.0) * (alpha * alpha) / (fk**one_minus_beta)
        + 0.25 * rho * beta * nu * alpha / fk_pow
        + ((2.0 - 3.0 * rho * rho) / 24.0) * (nu * nu)
    )

    return prefactor * (1.0 + gamma * t_exp)


def shifted_sabr_hagan_lognormal_vol(
    f: float,
    k: float,
    t_exp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
    shift: float,
) -> float:
    """Shifted SABR implied lognormal volatility for negative forward rates."""
    shifted_f = f + shift
    shifted_k = k + shift
    if shifted_f <= 0.0 or shifted_k <= 0.0:
        raise ValueError("Forward and strike + shift must be strictly positive.")
    return sabr_hagan_lognormal_vol(shifted_f, shifted_k, t_exp, alpha, beta, rho, nu)


def test_hagan_sabr_vol_example1() -> None:
    print("  1. Hagan SABR Implied Volatility Calculation (Example 1)")
    f = 0.040
    t = 1.0
    alpha = 0.035
    beta = 0.5
    rho = -0.25
    nu = 0.40

    # Intermediate terms for ATM
    one_minus_beta = 1.0 - beta
    f_pow = f**one_minus_beta
    prefactor_atm = alpha / f_pow
    quoted("1 - beta", one_minus_beta, 0.5, 1)
    quoted("F^(1-beta)", f_pow, 0.20, 2)
    quoted("alpha / F^(1-beta)", prefactor_atm, 0.1750, 4)

    # Gamma components
    term1 = ((one_minus_beta**2) / 24.0) * (alpha**2) / (f ** (2.0 * one_minus_beta))
    term2 = 0.25 * (rho * beta * nu * alpha) / f_pow
    term3 = ((2.0 - 3.0 * (rho**2)) / 24.0) * (nu**2)
    gamma = term1 + term2 + term3

    quoted("Gamma term 1", term1, 0.000319, 6)
    quoted("Gamma term 2", term2, -0.002187, 6)
    quoted("Gamma term 3", term3, 0.012083, 6)
    quoted("Total Gamma", gamma, 0.010215, 6)

    # Implied vols across strikes
    vol_atm = sabr_hagan_lognormal_vol(f, 0.04, t, alpha, beta, rho, nu)
    vol_low = sabr_hagan_lognormal_vol(f, 0.02, t, alpha, beta, rho, nu)
    vol_high = sabr_hagan_lognormal_vol(f, 0.06, t, alpha, beta, rho, nu)

    quoted("sigma_B ATM (4%)", vol_atm * 100.0, 17.68, 2)
    quoted("sigma_B Low strike (2%)", vol_low * 100.0, 27.54, 2)
    quoted("sigma_B High strike (6%)", vol_high * 100.0, 16.54, 2)


def test_parameter_sensitivities_example2() -> None:
    print("  2. Parameter Sensitivity of the SABR Smile (Example 2)")
    f = 0.040
    t = 1.0
    alpha = 0.035
    beta = 0.5

    # 1. Higher vol-of-vol nu = 0.80 (with rho = -0.25)
    nu_high = 0.80
    vol_2_nu = sabr_hagan_lognormal_vol(f, 0.02, t, alpha, beta, -0.25, nu_high)
    vol_atm_nu = sabr_hagan_lognormal_vol(f, 0.04, t, alpha, beta, -0.25, nu_high)
    vol_6_nu = sabr_hagan_lognormal_vol(f, 0.06, t, alpha, beta, -0.25, nu_high)
    quoted("nu=0.80 Low strike (2%)", vol_2_nu * 100.0, 36.76, 2)
    quoted("nu=0.80 ATM (4%)", vol_atm_nu * 100.0, 18.27, 2)
    quoted("nu=0.80 High strike (6%)", vol_6_nu * 100.0, 20.69, 2)

    # 2. Zero correlation rho = 0.0 (nu = 0.40)
    vol_2_rho0 = sabr_hagan_lognormal_vol(f, 0.02, t, alpha, beta, 0.0, 0.40)
    vol_atm_rho0 = sabr_hagan_lognormal_vol(f, 0.04, t, alpha, beta, 0.0, 0.40)
    vol_6_rho0 = sabr_hagan_lognormal_vol(f, 0.06, t, alpha, beta, 0.0, 0.40)
    quoted("rho=0.0 Low strike (2%)", vol_2_rho0 * 100.0, 25.47, 2)
    quoted("rho=0.0 ATM (4%)", vol_atm_rho0 * 100.0, 17.74, 2)
    quoted("rho=0.0 High strike (6%)", vol_6_rho0 * 100.0, 18.25, 2)

    # 3. Positive correlation rho = +0.30
    vol_2_rho30 = sabr_hagan_lognormal_vol(f, 0.02, t, alpha, beta, 0.30, 0.40)
    vol_atm_rho30 = sabr_hagan_lognormal_vol(f, 0.04, t, alpha, beta, 0.30, 0.40)
    vol_6_rho30 = sabr_hagan_lognormal_vol(f, 0.06, t, alpha, beta, 0.30, 0.40)
    quoted("rho=0.30 Low strike (2%)", vol_2_rho30 * 100.0, 22.44, 2)
    quoted("rho=0.30 ATM (4%)", vol_atm_rho30 * 100.0, 17.75, 2)
    quoted("rho=0.30 High strike (6%)", vol_6_rho30 * 100.0, 19.97, 2)

    # 4. Inverted skew rho = +0.50
    vol_2_rho50 = sabr_hagan_lognormal_vol(f, 0.02, t, alpha, beta, 0.50, 0.40)
    vol_6_rho50 = sabr_hagan_lognormal_vol(f, 0.06, t, alpha, beta, 0.50, 0.40)
    quoted("rho=0.50 Low strike (2%)", vol_2_rho50 * 100.0, 19.94, 2)
    quoted("rho=0.50 High strike (6%)", vol_6_rho50 * 100.0, 20.95, 2)


def test_shifted_sabr_example3() -> None:
    print("  3. Shifted SABR for Negative Rates (Example 3)")
    f_neg = -0.0050  # -0.50%
    shift = 0.0300  # 3.00%
    shifted_f = f_neg + shift
    quoted("Shifted forward F' (%)", shifted_f * 100.0, 2.50, 2)

    alpha = 0.035
    beta = 0.5
    rho = -0.25
    nu = 0.40

    vol_shift_1y = shifted_sabr_hagan_lognormal_vol(f_neg, f_neg, 1.0, alpha, beta, rho, nu, shift)
    vol_shift_2y = shifted_sabr_hagan_lognormal_vol(f_neg, f_neg, 2.0, alpha, beta, rho, nu, shift)

    quoted("Shifted SABR ATM 1y (%)", vol_shift_1y * 100.0, 22.35, 2)
    quoted("Shifted SABR ATM 2y (%)", vol_shift_2y * 100.0, 22.57, 2)


def main() -> None:
    print("=== fi_sabr: Rates Volatility and SABR ===")
    test_hagan_sabr_vol_example1()
    test_parameter_sensitivities_example2()
    test_shifted_sabr_example3()
    print(f"\nSuccessfully verified {len(QUOTED)} SABR volatility figures.")


if __name__ == "__main__":
    main()
