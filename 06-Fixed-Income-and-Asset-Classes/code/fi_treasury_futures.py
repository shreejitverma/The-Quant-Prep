"""Treasury futures, conversion factors, delivery basket, and cash-futures basis.

Backs every number in `06-Fixed-Income-and-Asset-Classes/16-Treasury-Futures-and-the-Basis.md`.
CME conversion factors, invoice prices, gross basis, net basis, implied repo rates (IRR),
CTD ranking, and hedge ratios are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_treasury_futures.py`.
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


def cme_conversion_factor(coupon: float, years: int) -> float:
    """CME conversion factor formula for integer years to maturity and coupon at delivery."""
    n_semi = 2 * years
    r_semi = 0.03
    return (coupon / 2.0 / r_semi) * (1.0 - (1.0 + r_semi) ** (-n_semi)) + (1.0 + r_semi) ** (-n_semi)


def solve_semiannual_yield(coupon: float, clean_price: float, years: int = 10) -> float:
    """Solve for semiannual yield y via Newton-Raphson."""
    n = 2 * years
    c_semi = coupon / 2.0 * 100.0

    def pv(y: float) -> float:
        r = y / 2.0
        return (c_semi / r) * (1.0 - (1.0 + r) ** (-n)) + 100.0 * (1.0 + r) ** (-n)

    y = coupon
    for _ in range(25):
        val = pv(y)
        dval = (pv(y + 1e-6) - pv(y - 1e-6)) / 2e-6
        y -= (val - clean_price) / dval
    return y


def test_conversion_factors() -> None:
    print("  1. CME Conversion Factor Calculation (Example 1)")
    # Bond B: 6.00% coupon, 10 years
    cf_b = cme_conversion_factor(0.06, 10)
    quoted("Bond B CF (6% coupon, 10y)", cf_b, 1.000000, 6)

    # Bond A: 4.00% coupon, 10 years
    denom = 1.03**20
    inv_denom = 1.0 / denom
    bracket = 1.0 - inv_denom
    cf_a_first = (0.02 / 0.03) * bracket
    cf_a = cf_a_first + inv_denom

    quoted("(1.03)^20", denom, 1.806111, 6)
    quoted("(1.03)^(-20)", inv_denom, 0.553676, 6)
    quoted("1 - (1.03)^(-20)", bracket, 0.446324, 6)
    quoted("2/3 * bracket", cf_a_first, 0.297549, 6)
    quoted("Bond A CF (4% coupon, 10y)", cf_a, 0.851225, 6)


def test_gross_basis_invoice_and_irr() -> None:
    print("  2. Gross Basis, Invoice Price, and Implied Repo Rate (Example 2)")
    f = 110.00
    cf_a = 0.851225
    clean_spot_a = 94.00
    ai_spot_a = 0.50
    dirty_spot_a = clean_spot_a + ai_spot_a
    ai_deliv_a = 1.50
    days = 90

    f_times_cf = round(f * cf_a + 1e-9, 4)
    gross_basis_a = clean_spot_a - f_times_cf
    invoice_price_a = f_times_cf + ai_deliv_a
    diff_a = invoice_price_a - dirty_spot_a
    irr_a = (diff_a / dirty_spot_a) * (360.0 / days)

    quoted("Futures price F", f, 110.00, 2)
    quoted("Clean spot price Bond A", clean_spot_a, 94.00, 2)
    quoted("Spot accrued interest Bond A", ai_spot_a, 0.50, 2)
    quoted("Dirty spot price Bond A", dirty_spot_a, 94.50, 2)
    quoted("Accrued interest at delivery Bond A", ai_deliv_a, 1.50, 2)
    quoted("Converted futures price F * CF_A", f_times_cf, 93.6348, 4)
    quoted("Gross basis Bond A", gross_basis_a, 0.3652, 4)
    quoted("Invoice price Bond A", invoice_price_a, 95.1348, 4)
    quoted("Invoice - Dirty spot", diff_a, 0.6348, 4)
    quoted("IRR Bond A (%)", irr_a * 100.0, 2.687, 3)

    # Actual repo rate 2.25%
    repo_rate = 0.0225
    spread_bps = (irr_a - repo_rate) * 10_000.0
    quoted("Actual repo rate (%)", repo_rate * 100.0, 2.250, 3)
    quoted("Arbitrage spread over repo (bps)", spread_bps, 43.7, 1)


def test_cheapest_to_deliver_comparison() -> None:
    print("  3. Cheapest-to-Deliver (CTD) Comparison (Example 3)")
    f = 110.00
    cf_c = 1.000000
    clean_spot_c = 111.00
    ai_spot_c = 0.75
    dirty_spot_c = clean_spot_c + ai_spot_c
    ai_deliv_c = 2.25
    days = 90

    invoice_price_c = f * cf_c + ai_deliv_c
    gross_basis_c = clean_spot_c - f * cf_c
    diff_c = invoice_price_c - dirty_spot_c
    irr_c = (diff_c / dirty_spot_c) * (360.0 / days)

    quoted("Clean spot price Bond C", clean_spot_c, 111.00, 2)
    quoted("Spot accrued interest Bond C", ai_spot_c, 0.75, 2)
    quoted("Dirty spot price Bond C", dirty_spot_c, 111.75, 2)
    quoted("Accrued interest at delivery Bond C", ai_deliv_c, 2.25, 2)
    quoted("Invoice price Bond C", invoice_price_c, 112.25, 2)
    quoted("Gross basis Bond C", gross_basis_c, 1.0000, 4)
    quoted("Invoice - Dirty spot Bond C", diff_c, 0.50, 2)
    quoted("IRR Bond C (%)", irr_c * 100.0, 1.790, 3)

    # Implied yields
    yield_a = solve_semiannual_yield(0.04, 94.00, 10)
    yield_c = solve_semiannual_yield(0.06, 111.00, 10)
    quoted("Implied semiannual yield Bond A (%)", yield_a * 100.0, 4.761, 3)
    quoted("Implied semiannual yield Bond C (%)", yield_c * 100.0, 4.614, 3)

    # Bond C priced at Bond A's yield
    r_a = yield_a / 2.0
    n = 20
    p_c_at_a = (3.0 / r_a) * (1.0 - (1.0 + r_a) ** (-n)) + 100.0 * (1.0 + r_a) ** (-n)
    dirty_c_at_a = p_c_at_a + 0.75
    irr_c_hypo = ((invoice_price_c - dirty_c_at_a) / dirty_c_at_a) * (360.0 / days)

    quoted("Bond C price at Bond A yield", p_c_at_a, 109.7665, 4)
    quoted("Bond C dirty price at Bond A yield", dirty_c_at_a, 110.5165, 4)
    quoted("Hypothetical IRR Bond C (%)", irr_c_hypo * 100.0, 6.274, 3)


def test_market_case_and_interview_questions() -> None:
    print("  4. Market Case and Interview Card Calculations")
    fed_purchases_billions = 500.0
    quoted("Fed purchases March 2020 ($B)", fed_purchases_billions, 500.0, 1)

    # Question 8 card: $10M cash bond with CF = 0.85
    cash_notional = 10_000_000.0
    cf_q = 0.85
    fut_notional = cash_notional * cf_q
    contract_size = 100_000.0
    num_contracts = fut_notional / contract_size

    quoted("Required futures notional ($)", fut_notional, 8_500_000.0, 1)
    quoted("Number of futures contracts", num_contracts, 85.0, 1)


def main() -> None:
    print("=== fi_treasury_futures: Treasury Futures and the Basis ===")
    test_conversion_factors()
    test_gross_basis_invoice_and_irr()
    test_cheapest_to_deliver_comparison()
    test_market_case_and_interview_questions()
    print(f"\nSuccessfully verified {len(QUOTED)} Treasury futures figures.")


if __name__ == "__main__":
    main()
