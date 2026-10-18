"""Money markets, repurchase agreements (repo), and overnight reference rates (SOFR/SONIA).

Backs every number in `06-Fixed-Income-and-Asset-Classes/12-Money-Markets-Repo-and-Overnight-Rates.md`.
Repo interest, haircut cash, compounding in arrears, carry of repo-financed bonds, specialness, and ISDA fallbacks are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_money_markets.py`.
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


def test_repo_interest_and_haircut() -> None:
    print("  1. Repurchase Agreement: Haircut Cash and Interest")
    collateral_value = 100_000_000.0
    haircut = 0.02
    repo_rate = 0.0530
    term_days = 7

    cash_lent = collateral_value * (1.0 - haircut)
    repo_interest = cash_lent * repo_rate * (term_days / 360.0)
    repayment_amount = cash_lent + repo_interest

    quoted("collateral market value ($)", collateral_value, 100_000_000.0, 0)
    quoted("haircut percentage (%)", haircut * 100.0, 2.0, 1)
    quoted("cash lent ($)", cash_lent, 98_000_000.0, 0)
    quoted("repo interest rate (%)", repo_rate * 100.0, 5.30, 2)
    quoted("repo interest ($)", repo_interest, 100_994.44, 2)
    quoted("total repayment amount ($)", repayment_amount, 98_100_994.44, 2)


def test_compounding_in_arrears() -> None:
    print("  2. Overnight Rate Compounding vs Simple Average (7-Day Period)")
    # Mon, Tue, Wed = 5.00% (1 day each)
    # Thu = 5.10% (1 day)
    # Fri = 5.10% (3 days over weekend)
    rates = [0.050, 0.050, 0.050, 0.051, 0.051]
    days = [1, 1, 1, 1, 3]
    total_days = sum(days)

    # Simple day-weighted average
    simple_avg = sum(r * d for r, d in zip(rates, days, strict=True)) / total_days

    # Compounded in arrears (ACT/360)
    growth = 1.0
    for r, d in zip(rates, days, strict=True):
        growth *= 1.0 + (r * d / 360.0)
    compounded_rate = (growth - 1.0) * (360.0 / total_days)

    compounding_spread_bps = (compounded_rate - simple_avg) * 10_000.0

    quoted("simple day-weighted average (%)", simple_avg * 100.0, 5.0571, 4)
    quoted("compounded overnight rate (%)", compounded_rate * 100.0, 5.0590, 4)
    quoted("compounding spread (bps)", compounding_spread_bps, 0.18, 2)


def test_repo_carry() -> None:
    print("  3. Carry and Roll-Down of a Repo-Financed Bond")
    notional = 100.0
    coupon_rate = 0.040  # 4% annual ACT/365F
    repo_rate = 0.050  # 5% ACT/360
    holding_days = 30

    coupon_accrual = notional * coupon_rate * (holding_days / 365.0)
    repo_cost = notional * repo_rate * (holding_days / 360.0)
    net_carry = coupon_accrual - repo_cost

    position_100m = 100_000_000.0
    monthly_carry_dollars = (position_100m / notional) * net_carry

    quoted("coupon accrual per 100 par", coupon_accrual, 0.3288, 4)
    quoted("repo financing cost per 100 par", repo_cost, 0.4167, 4)
    quoted("net monthly carry per 100 par", net_carry, -0.0879, 4)
    quoted("net monthly dollar carry on 100M ($)", monthly_carry_dollars, -87_900.0, 0)


def test_specialness_and_fallbacks() -> None:
    print("  4. Special Repo Rates and ISDA IBOR Fallbacks")
    gc_rate = 0.0530
    special_rate = 0.0380
    specialness_bps = (gc_rate - special_rate) * 10_000.0

    position = 100_000_000.0
    monthly_special_savings = position * (gc_rate - special_rate) * (30.0 / 360.0)

    quoted("general collateral GC rate (%)", gc_rate * 100.0, 5.30, 2)
    quoted("special repo rate (%)", special_rate * 100.0, 3.80, 2)
    quoted("specialness spread (bps)", specialness_bps, 150.0, 0)
    quoted("monthly funding savings from special bond ($)", monthly_special_savings, 125_000.0, 0)

    # ISDA 3M USD LIBOR fallback spread
    fallback_spread = 0.0026161  # 26.161 bps
    compounded_sofr = 0.051245
    synthetic_libor = compounded_sofr + fallback_spread

    quoted("3M USD LIBOR fallback spread (%)", fallback_spread * 100.0, 0.26161, 5)
    quoted("compounded SOFR fixing (%)", compounded_sofr * 100.0, 5.12450, 5)
    quoted("synthetic fallback rate (%)", synthetic_libor * 100.0, 5.38611, 5)


def main() -> None:
    print("=== fi_money_markets: Money Markets, Repo, and Overnight Rates ===")
    test_repo_interest_and_haircut()
    test_compounding_in_arrears()
    test_repo_carry()
    test_specialness_and_fallbacks()
    print(f"\nSuccessfully verified {len(QUOTED)} money market and repo figures.")


if __name__ == "__main__":
    main()
