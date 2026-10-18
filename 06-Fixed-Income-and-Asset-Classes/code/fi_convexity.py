"""Convexity adjustments: futures vs forwards, CMS replication, and quanto drift.

Backs every number in `06-Fixed-Income-and-Asset-Classes/17-Convexity-Adjustments.md`.
Ho-Lee and Hull-White futures convexity bias, CMS linear duration approximation,
CMS static swaption replication, in-arrears adjustments, and quanto drift are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_convexity.py`.
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


def test_futures_convexity_adjustments() -> None:
    print("  1. Futures vs Forward Rate Convexity Adjustments")
    sigma = 0.0120  # 120 bps short rate volatility
    sigma_sq = sigma**2
    quoted("sigma^2", sigma_sq, 0.000144, 6)

    # 5-year expiry on 3-month rate (T1 = 5.0, T2 = 5.25)
    t1_5 = 5.0
    t2_5 = 5.25
    adj_ho_lee_5 = 0.5 * sigma_sq * t1_5 * t2_5
    quoted("Ho-Lee 5y futures adjustment (bps)", adj_ho_lee_5 * 10_000.0, 18.9, 1)

    # Hull-White with mean reversion a = 0.03
    a = 0.03
    b12 = (1.0 - math.exp(-a * (t2_5 - t1_5))) / a
    b01 = (1.0 - math.exp(-a * t1_5)) / a
    bracket = b12 * (1.0 - math.exp(-2.0 * a * t1_5)) + 2.0 * a * (b01**2)
    adj_hw_5 = (b12 / (t2_5 - t1_5)) * bracket * (sigma_sq / (4.0 * a))
    quoted("Hull-White 5y futures adjustment (bps)", adj_hw_5 * 10_000.0, 16.2, 1)

    # Example 1: 2-year futures contract on 3-month rate (T1 = 2.0, T2 = 2.25)
    t1_2 = 2.0
    t2_2 = 2.25
    adj_ho_lee_2 = 0.5 * sigma_sq * t1_2 * t2_2
    quoted("Ho-Lee 2y futures adjustment", adj_ho_lee_2, 0.000324, 6)
    quoted("Ho-Lee 2y futures adjustment (bps)", adj_ho_lee_2 * 10_000.0, 3.24, 2)

    quoted_fut_rate = 0.045000
    fair_fwd_rate = quoted_fut_rate - adj_ho_lee_2
    quoted("Quoted futures rate (%)", quoted_fut_rate * 100.0, 4.5000, 4)
    quoted("Fair forward rate (%)", fair_fwd_rate * 100.0, 4.4676, 4)


def test_cms_convexity_adjustment() -> None:
    print("  2. CMS Convexity Adjustment (Example 2)")
    s0 = 0.040  # 4% forward swap rate
    sigma_s = 0.200  # 20% lognormal swap rate vol
    t1 = 5.0
    tenor = 10

    # 1. Annuity factor A(S(0))
    df_10 = (1.0 + s0) ** (-tenor)
    quoted("(1.04)^(-10)", df_10, 0.675564, 6)

    annuity = sum((1.0 + s0) ** (-i) for i in range(1, tenor + 1))
    quoted("Annuity A(0.04)", annuity, 8.110896, 6)

    # 2. Annuity derivative A'(S(0))
    annuity_prime = -sum(i * ((1.0 + s0) ** (-(i + 1))) for i in range(1, tenor + 1))
    quoted("A'(0.04)", annuity_prime, -40.37716, 5)

    # 3. Relative duration
    dur_rel = -annuity_prime / annuity
    quoted("Relative duration Dur_rel", dur_rel, 4.97814, 5)

    # 4. Variance scaling term: S(0)^2 * sigma_S^2 * T1
    var_term = (s0**2) * (sigma_s**2) * t1
    quoted("S0^2 * sigma^2 * T1", var_term, 0.000320, 6)

    # 5. CMS convexity adjustment
    adj_cms = var_term * dur_rel
    quoted("Adj_CMS", adj_cms, 0.001593, 6)
    quoted("Adj_CMS (bps)", adj_cms * 10_000.0, 15.93, 2)

    expected_cms_fixing = s0 + adj_cms
    quoted("Expected 10y CMS fixing (%)", expected_cms_fixing * 100.0, 4.1593, 4)


def test_quanto_convexity_adjustment() -> None:
    print("  3. Quanto Interest Rate Adjustment (Example 3)")
    t = 3.0
    s_f0 = 0.030  # 3.0% forward EUR rate
    sigma_s = 0.180  # 18% foreign rate vol
    sigma_fx = 0.120  # 12% EUR/USD FX vol
    rho = 0.40  # correlation

    drift_rate = -rho * sigma_s * sigma_fx
    quoted("Relative drift adjustment per year", drift_rate, -0.00864, 5)

    rate_drift = drift_rate * s_f0
    quoted("Rate unit drift per year", rate_drift, -0.0002592, 7)
    quoted("Rate unit drift per year (bps)", rate_drift * 10_000.0, -2.59, 2)

    exp_term_minus_1 = math.exp(drift_rate * t) - 1.0
    quoted("exp(drift * T) - 1", exp_term_minus_1, -0.025587, 6)

    adj_quanto = s_f0 * exp_term_minus_1
    quoted("Adj_quanto", adj_quanto, -0.0007676, 7)
    quoted("Adj_quanto (bps)", adj_quanto * 10_000.0, -7.68, 2)

    linear_approx = drift_rate * s_f0 * t
    quoted("Linear approx Adj_quanto (bps)", linear_approx * 10_000.0, -7.78, 2)

    expected_bund_rate = s_f0 + adj_quanto
    quoted("Expected Bund rate under USD measure (%)", expected_bund_rate * 100.0, 2.9232, 4)

    # Pitfall scale factor: (0.20 / 0.0080)^2 = 625
    pitfall_scale = (0.20 / 0.0080) ** 2
    quoted("Normal vs lognormal variance distortion factor", pitfall_scale, 625.0, 1)


def main() -> None:
    print("=== fi_convexity: Convexity Adjustments ===")
    test_futures_convexity_adjustments()
    test_cms_convexity_adjustment()
    test_quanto_convexity_adjustment()
    print(f"\nSuccessfully verified {len(QUOTED)} convexity adjustment figures.")


if __name__ == "__main__":
    main()
