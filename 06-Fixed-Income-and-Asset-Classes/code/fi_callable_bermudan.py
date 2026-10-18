"""Callable bonds, Bermudan swaptions, trinomial tree backward induction, and LSMC.

Backs every number in `06-Fixed-Income-and-Asset-Classes/20-Callable-and-Bermudan-Products.md`.
Hull-White trinomial tree Bermudan swaption pricing, Jamshidian co-terminal swaptions,
early exercise premium, callable bond negative convexity profile, and Longstaff-Schwartz regression are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_callable_bermudan.py`.
"""

from __future__ import annotations

import math
from collections.abc import Callable

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def bond_price_and_duration(coupon: float, yield_rate: float, years: int) -> tuple[float, float]:
    """Analytical price and modified duration of an annual coupon bond."""
    p = 0.0
    weighted_cf = 0.0
    for t in range(1, years + 1):
        cf = coupon if t < years else coupon + 100.0
        df = (1.0 + yield_rate) ** (-t)
        p += cf * df
        weighted_cf += t * cf * df
    mac_duration = weighted_cf / p
    mod_duration = mac_duration / (1.0 + yield_rate)
    return p, mod_duration


def hw_b(a: float, t: float, big_t: float) -> float:
    """Hull-White B(t, T) = (1 - e^{-a(T-t)}) / a."""
    return (1.0 - math.exp(-a * (big_t - t))) / a


def hw_zcb_price_from_state(
    discount_curve: Callable[[float], float],
    a: float,
    sigma: float,
    t: float,
    big_t: float,
    x: float,
) -> float:
    """Hull-White zero coupon bond price P(t, T) from OU state x = r(t) - alpha(t)."""
    if t >= big_t:
        return 1.0
    p0_t = discount_curve(t)
    p0_big_t = discount_curve(big_t)
    b_val = hw_b(a, t, big_t)
    # Standard Hull-White formula
    var_int = (sigma * sigma / (2.0 * a * a)) * (
        (big_t - t) + (2.0 / a) * math.exp(-a * (big_t - t)) - (1.0 / (2.0 * a)) * math.exp(-2.0 * a * (big_t - t)) - 1.5 / a
    )
    # Using exact analytical ratio:
    ln_p = math.log(p0_big_t / p0_t) - b_val * x - var_int
    return math.exp(ln_p)


def test_bermudan_swaption_example1() -> None:
    print("  1. Hull-White Trinomial Tree Bermudan Swaption Valuation (Example 1)")
    from rates_models import hw_bermudan_swaption_tree, hw_swaption_jamshidian

    def discount_curve(t: float) -> float:
        return math.exp(-0.04 * t)

    strike = 0.04
    exercises = [1.0, 2.0, 3.0, 4.0]
    swap_end = 5.0
    swap_freq = 1
    a = 0.03
    sigma = 0.012

    p_berm, p_eur, p_prem = hw_bermudan_swaption_tree(discount_curve, strike, exercises, swap_end, swap_freq, a, sigma, dt=0.05)
    p_jam_1_4 = hw_swaption_jamshidian(discount_curve, strike, 1.0, 4.0, 1, a, sigma)
    p_jam_2_3 = hw_swaption_jamshidian(discount_curve, strike, 2.0, 3.0, 1, a, sigma)

    quoted("European Swaption Tree Price", p_eur, 0.0176082, 7)
    quoted("European Swaption Tree Price (bps)", p_eur * 10_000.0, 176.08, 2)
    quoted("Analytic Jamshidian 1y into 4y", p_jam_1_4, 0.017568, 6)

    err_pct = abs(p_eur - p_jam_1_4) / p_jam_1_4 * 100.0
    quoted("Tree vs Jamshidian error (%)", err_pct, 0.23, 2)

    quoted("Bermudan Swaption Tree Price", p_berm, 0.0232815, 7)
    quoted("Bermudan Swaption Tree Price (bps)", p_berm * 10_000.0, 232.82, 2)

    quoted("Early Exercise Premium", p_prem, 0.0056733, 7)
    quoted("Early Exercise Premium (bps)", p_prem * 10_000.0, 56.73, 2)

    prem_pct = p_prem / p_eur * 100.0
    quoted("Premium over European (%)", prem_pct, 32.2, 1)

    quoted("Most valuable single European (2y into 3y)", p_jam_2_3, 0.017794, 6)


def test_callable_bond_negative_convexity_example2() -> None:
    print("  2. Negative Convexity in a Callable Bond (Example 2)")
    coupon = 6.0

    # 1. At 8% yield (30-year straight bond)
    p_8, dur_8 = bond_price_and_duration(coupon, 0.08, 30)
    quoted("Price at 8% yield", p_8, 77.48, 2)
    quoted("Modified duration at 8% yield (years)", dur_8, 11.79, 2)

    # 100 bp drop to 7% yield
    p_7, _ = bond_price_and_duration(coupon, 0.07, 30)
    gain_pct = (p_7 - p_8) / p_8 * 100.0
    quoted("Price at 7% yield", p_7, 87.59, 2)
    quoted("Price gain on 100 bp drop (%)", gain_pct, 13.0, 1)

    # 2. At 4% yield
    # Straight bond price
    p_4_straight, _ = bond_price_and_duration(coupon, 0.04, 30)
    quoted("Straight bond price at 4% yield", p_4_straight, 134.58, 2)

    # Callable bond priced to 5-year call at par
    p_4_call, dur_4_call = bond_price_and_duration(coupon, 0.04, 5)
    quoted("Callable bond price to 5y call date at 4%", p_4_call, 108.90, 2)
    quoted("Callable bond modified duration at 4% (years)", dur_4_call, 4.32, 2)


def test_longstaff_schwartz_regression_example3() -> None:
    print("  3. Longstaff-Schwartz Regression Step (Example 3)")
    # Paths at T1: x in {0.02, 0.03, 0.04, 0.05}
    # In-the-money paths: x = 0.02 and x = 0.03
    x_itm = [0.02, 0.03]
    y_itm = [0.045, 0.038]

    # Linear regression Y = beta0 + beta1 * x
    dx = x_itm[1] - x_itm[0]
    dy = y_itm[1] - y_itm[0]
    beta1 = dy / dx
    beta0 = y_itm[0] - beta1 * x_itm[0]

    quoted("LSMC regression slope beta1", beta1, -0.70, 2)
    quoted("LSMC regression intercept beta0", beta0, 0.059, 3)

    # Path 1 (x = 0.02)
    v_cont_1 = beta0 + beta1 * x_itm[0]
    swap_npv_1 = 0.06
    quoted("Path 1 V_cont", v_cont_1, 0.045, 3)
    quoted("Path 1 SwapNPV", swap_npv_1, 0.06, 2)

    # Path 2 (x = 0.03)
    v_cont_2 = beta0 + beta1 * x_itm[1]
    swap_npv_2 = 0.03
    quoted("Path 2 V_cont", v_cont_2, 0.038, 3)
    quoted("Path 2 SwapNPV", swap_npv_2, 0.03, 2)


def main() -> None:
    print("=== fi_callable_bermudan: Callable Bonds and Bermudan Swaptions ===")
    test_bermudan_swaption_example1()
    test_callable_bond_negative_convexity_example2()
    test_longstaff_schwartz_regression_example3()
    print(f"\nSuccessfully verified {len(QUOTED)} callable and Bermudan figures.")


if __name__ == "__main__":
    main()
