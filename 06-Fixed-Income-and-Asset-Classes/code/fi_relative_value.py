"""Fixed income P&L attribution and relative value: carry, roll-down, full revaluation, butterflies, asset swaps.

Backs every number in `06-Fixed-Income-and-Asset-Classes/24-Fixed-Income-PnL-and-Relative-Value.md`.
- Example 1 and cards fi-rv-pnl-carry-vs-rolldown and fi-rv-attribution-residual: one-month P&L of a repo-financed 10-year note,
  decomposed into coupon, pull to par, financing, roll-down, delta and convexity, and checked against full revaluation.
- Example 2 and cards fi-rv-fifty-fifty-dv01-limitation and fi-rv-regression-beta-butterfly: 50-50 and regression-weighted
  2s5s10s butterflies and their exposure to a twist.
- Example 3 and cards fi-rv-asset-swap-spread-asw and fi-rv-par-par-vs-market-value-asw: par-par and market-value asset swap
  spreads from a bond and a swap curve.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_relative_value.py`.
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


def dirty_price(coupon: float, y: float, n_coupons: int, w: float) -> float:
    """Dirty price per 100 of a semi-annual bond with n_coupons left, the next one w periods away (street convention)."""
    v = 1.0 / (1.0 + y / 2.0)
    return sum(coupon * 50.0 * v ** (w + k) for k in range(n_coupons)) + 100.0 * v ** (w + n_coupons - 1)


def example1_attribution() -> None:
    print("  1. One-month P&L attribution with full revaluation (Example 1)")
    face, coupon, y0, repo = 100_000_000.0, 0.0425, 0.0420, 0.0400
    slope_per_year = 0.0004  # curve 4 bp higher per extra year of maturity around 10 years
    dt_years, repo_days = 1.0 / 12.0, 30
    w_end = 1.0 - dt_years / 0.5
    y_roll = y0 - slope_per_year * dt_years
    shift = 0.0005

    p0 = dirty_price(coupon, y0, 20, 1.0)  # on a coupon date: dirty = clean
    accrued_end = coupon * 50.0 * (1.0 - w_end)
    p_time = dirty_price(coupon, y0, 20, w_end)
    p_roll = dirty_price(coupon, y_roll, 20, w_end)
    p_end = dirty_price(coupon, y_roll + shift, 20, w_end)
    scale = face / 100.0

    quoted("start price", p0, 100.4049, 4)
    quoted("rolled-down yield (%)", y_roll * 100.0, 4.1967, 4)
    coupon_income = accrued_end * scale
    pull_to_par = (p_time - accrued_end - p0) * scale
    financing = -repo * p0 * scale * repo_days / 360.0
    roll_down = (p_roll - p_time) * scale
    rate_move = (p_end - p_roll) * scale
    total = (p_end - p0) * scale + financing
    quoted("coupon income ($)", coupon_income, 354_166.67, 2)
    quoted("pull to par at unchanged yield ($)", pull_to_par, -5_785.64, 2)
    quoted("financing ($)", financing, -334_682.89, 2)
    quoted("net carry ($)", coupon_income + pull_to_par + financing, 13_698.13, 2)
    quoted("roll-down ($)", roll_down, 26_880.09, 2)
    quoted("rate move, full revaluation ($)", rate_move, -402_306.10, 2)
    quoted("total P&L ($)", total, -361_727.88, 2)
    assert abs(total - (coupon_income + pull_to_par + financing + roll_down + rate_move)) < 1e-6

    # Taylor approximation of the rate move from DV01 and convexity at the rolled-down point.
    h = 1e-6
    p_up, p_dn = dirty_price(coupon, y_roll + h, 20, w_end), dirty_price(coupon, y_roll - h, 20, w_end)
    dv01 = (p_dn - p_up) / (2.0 * h) * 1e-4 * scale
    dollar_convexity = (p_up + p_dn - 2.0 * p_roll) / (h * h) * scale
    quoted("DV01 ($ per bp)", dv01, 80_653.08, 2)
    quoted("delta P&L -DV01 x 5 ($)", -dv01 * 5.0, -403_265.42, 2)
    quoted("convexity P&L 0.5 C (dy)^2 ($)", 0.5 * dollar_convexity * shift**2, 960.98, 2)
    quoted("carry plus roll-down ($)", coupon_income + pull_to_par + financing + roll_down, 40_578.22, 2)
    quoted("breakeven yield rise over the month (bp)", (coupon_income + pull_to_par + financing + roll_down) / dv01, 0.50, 2)
    quoted("unexplained residual ($)", rate_move - (-dv01 * 5.0 + 0.5 * dollar_convexity * shift**2), -1.66, 2)


def example2_butterfly() -> None:
    print("  2. 2s5s10s butterflies (Example 2)")
    dv01_2, dv01_5, dv01_10 = 19.50, 44.20, 81.50  # $ per bp per $100,000 notional
    body_notional = 100_000_000.0
    body_dv01 = body_notional / 100_000.0 * dv01_5
    quoted("body DV01 ($)", body_dv01, 44_200.0, 0)
    quoted("50-50: DV01 per wing ($)", 0.5 * body_dv01, 22_100.0, 0)
    n2 = 0.5 * body_dv01 / dv01_2 * 100_000.0
    n10 = 0.5 * body_dv01 / dv01_10 * 100_000.0
    quoted("50-50: 2y notional ($)", n2, 113_333_333.0, 0)
    quoted("50-50: 10y notional ($)", n10, 27_116_564.0, 0)
    # A 1 bp-per-year twist pivoting on the 5y: the 2y moves -3 bp, the 10y +5 bp, the 5y 0.
    twist = -(0.5 * body_dv01) * (-3.0) - (0.5 * body_dv01) * 5.0 + body_dv01 * 0.0
    quoted("50-50: 2y wing P&L in the twist ($)", -(0.5 * body_dv01) * (-3.0), 66_300.0, 0)
    quoted("50-50: 10y wing P&L in the twist ($)", -(0.5 * body_dv01) * 5.0, -110_500.0, 0)
    quoted("50-50 P&L for a 1 bp/yr steepening twist about the 5y ($)", twist, -44_200.0, 0)
    beta2, beta10 = 0.40, 0.65  # illustrative regression of 5y changes on 2y and 10y changes
    reg_dv01_2, reg_dv01_10 = beta2 * body_dv01, beta10 * body_dv01
    quoted("regression: 2y wing DV01 ($)", reg_dv01_2, 17_680.0, 0)
    quoted("regression: 10y wing DV01 ($)", reg_dv01_10, 28_730.0, 0)
    quoted("regression: 2y notional ($)", reg_dv01_2 / dv01_2 * 100_000.0, 90_666_667.0, 0)
    quoted("regression: 10y notional ($)", reg_dv01_10 / dv01_10 * 100_000.0, 35_251_534.0, 0)
    quoted("regression: net parallel DV01 ($)", reg_dv01_2 + reg_dv01_10 - body_dv01, 2_210.0, 0)


def example3_asset_swap() -> None:
    print("  3. Par-par and market-value asset swaps (Example 3)")
    swap_rate, years, coupon, bond_yield = 0.0410, 7, 4.00, 0.0445
    dfs = [(1.0 + swap_rate) ** -(i + 1) for i in range(years)]  # flat annual par curve: discount at the swap rate
    annuity = sum(dfs)
    assert abs((1.0 - dfs[-1]) / annuity - swap_rate) < 1e-12, "the curve must reprice the par swap"
    price = sum(coupon / (1.0 + bond_yield) ** (i + 1) for i in range(years)) + 100.0 / (1.0 + bond_yield) ** years
    price_swap_curve = sum(coupon * d for d in dfs) + 100.0 * dfs[-1]
    quoted("bond price at 4.45% (full price, on a coupon date)", price, 97.3434, 4)
    quoted("bond priced off the swap curve", price_swap_curve, 99.4020, 4)
    quoted("swap annuity", annuity, 5.9799, 4)
    quoted("swap annuity (5 dp)", annuity, 5.97994, 5)
    quoted("bond price (5 dp)", price, 97.34343, 5)
    quoted("bond on the swap curve (5 dp)", price_swap_curve, 99.40201, 5)
    par_par = (price_swap_curve - price) / (100.0 * annuity)
    quoted("par-par asset swap spread (bp)", par_par * 1e4, 34.42, 2)
    quoted("market-value asset swap spread (bp)", par_par * 100.0 / price * 1e4, 35.36, 2)
    quoted("yield spread to the swap rate (bp)", (bond_yield - swap_rate) * 1e4, 35.00, 2)
    # Check from the swap's legs: the investor pays 100 - price upfront, so at the par-par spread the swap (pay the bond's
    # coupons, receive projected forwards plus the spread on 100) must be worth exactly that upfront.
    fixed_leg = sum(coupon * d for d in dfs)
    forwards = [(1.0 if i == 0 else dfs[i - 1]) / dfs[i] - 1.0 for i in range(years)]
    float_leg = sum(100.0 * (f + par_par) * d for f, d in zip(forwards, dfs, strict=True))
    assert abs((float_leg - fixed_leg) - (100.0 - price)) < 1e-9, "par-par swap value must equal the upfront"


def main() -> None:
    print("=== fi_relative_value: P&L Attribution and Relative Value ===")
    example1_attribution()
    example2_butterfly()
    example3_asset_swap()
    print(f"\nSuccessfully verified {len(QUOTED)} relative value figures.")


if __name__ == "__main__":
    main()
