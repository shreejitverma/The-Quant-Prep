"""Fixed Income Mortgages and Securitized Products Reference Engine.

Asserts every quantitative figure quoted in Note 22
(22-Mortgages-and-Securitized-Products.md) to within half a unit
in the last quoted decimal place using standard-library pure Python.
"""


def smm_to_cpr(smm: float) -> float:
    """Convert Single Monthly Mortality (SMM) to Constant Prepayment Rate (CPR)."""
    return 1.0 - (1.0 - smm) ** 12


def cpr_to_smm(cpr: float) -> float:
    """Convert Constant Prepayment Rate (CPR) to Single Monthly Mortality (SMM)."""
    return 1.0 - (1.0 - cpr) ** (1.0 / 12.0)


def psa_cpr(month: int, psa_multiple: float = 100.0) -> float:
    """Calculate projected CPR at loan age month for a given PSA benchmark speed."""
    if month <= 0:
        return 0.0
    base_cpr = 0.06 * (month / 30.0) if month <= 30 else 0.06
    return base_cpr * (psa_multiple / 100.0)


def dollar_roll_implied_rate(
    p_front: float,
    p_back: float,
    cash_flow_forgone: float,
    days: int = 30,
    day_count_basis: int = 360,
) -> tuple[float, float, float]:
    """Calculate dollar roll drop, net financing cost, and annualized implied rate.

    Returns:
        (drop, net_cost, implied_rate)
    """
    drop = p_front - p_back
    net_cost = cash_flow_forgone - drop
    implied_rate = (net_cost / p_front) * (day_count_basis / days)
    return drop, net_cost, implied_rate


def sequential_cmo_month_waterfall(
    balances: list[float],
    total_principal_cashflow: float,
) -> tuple[list[float], list[float]]:
    """Allocate total principal cash flow sequentially across tranches.

    Returns:
        (principal_received_by_tranche, ending_balances)
    """
    remaining_cf = total_principal_cashflow
    received = []
    ending = []
    for bal in balances:
        allocated = min(bal, remaining_cf)
        received.append(allocated)
        ending.append(bal - allocated)
        remaining_cf -= allocated
    return received, ending


def main() -> None:
    # 1. SMM to CPR conversion (Example 1)
    smm = 0.0050  # 0.50%
    cpr = smm_to_cpr(smm)
    assert round(cpr * 100, 4) == 5.8377, f"Expected 5.8377%, got {cpr * 100}"
    assert round(cpr * 100, 2) == 5.84, f"Expected 5.84%, got {cpr * 100}"

    # Invert back to SMM
    smm_back = cpr_to_smm(cpr)
    assert round(smm_back * 100, 4) == 0.5000, f"Expected 0.5000%, got {smm_back * 100}"

    # 2. PSA Benchmark Schedule (Example 2)
    # Month 10 at 100% PSA
    cpr_m10_100 = psa_cpr(10, 100.0)
    assert round(cpr_m10_100 * 100, 2) == 2.00, f"Expected 2.00%, got {cpr_m10_100 * 100}"

    # Month 20 at 100% PSA
    cpr_m20_100 = psa_cpr(20, 100.0)
    assert round(cpr_m20_100 * 100, 2) == 4.00, f"Expected 4.00%, got {cpr_m20_100 * 100}"

    # Month 30 at 150% PSA
    cpr_m30_150 = psa_cpr(30, 150.0)
    assert round(cpr_m30_150 * 100, 2) == 9.00, f"Expected 9.00%, got {cpr_m30_150 * 100}"

    # Month 60 at 150% PSA (flat post month 30)
    cpr_m60_150 = psa_cpr(60, 150.0)
    assert round(cpr_m60_150 * 100, 2) == 9.00, f"Expected 9.00%, got {cpr_m60_150 * 100}"

    # 3. Dollar Roll Implied Financing Rate (Example 3)
    p_front = 101.50
    p_back = 101.125
    cf_forgone = 0.480
    drop, net_cost, implied_rate = dollar_roll_implied_rate(p_front, p_back, cf_forgone, days=30)
    assert round(drop, 3) == 0.375, f"Expected drop 0.375, got {drop}"
    assert round(net_cost, 3) == 0.105, f"Expected net cost 0.105, got {net_cost}"
    assert round(implied_rate * 100, 4) == 1.2414, f"Expected 1.2414%, got {implied_rate * 100}"
    assert round(implied_rate * 100, 2) == 1.24, f"Expected 1.24%, got {implied_rate * 100}"

    gc_repo = 0.0450
    specialness_bps = (gc_repo - implied_rate) * 10000
    assert round(specialness_bps, 0) == 326.0, f"Expected 326 bps, got {specialness_bps}"

    # 4. Sequential CMO Waterfall (Example 4)
    # Tranche A ($60M), Tranche B ($40M)
    init_balances = [60_000_000.0, 40_000_000.0]
    total_principal_cf = 1_500_000.0
    rec, end_bal = sequential_cmo_month_waterfall(init_balances, total_principal_cf)
    assert rec[0] == 1_500_000.0, f"Tranche A should receive all $1.5M, got {rec[0]}"
    assert rec[1] == 0.0, f"Tranche B should receive $0, got {rec[1]}"
    assert end_bal[0] == 58_500_000.0, f"Tranche A balance should be $58.5M, got {end_bal[0]}"
    assert end_bal[1] == 40_000_000.0, f"Tranche B balance should be $40.0M, got {end_bal[1]}"

    print("All fi_mortgages assertions passed successfully.")


if __name__ == "__main__":
    main()
