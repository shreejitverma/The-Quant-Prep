"""XVA Pricing, Bilateral CVA/DVA, FVA, MVA, and KVA Engine.

Pure Python 3.10+ standard library implementation:
1. Bilateral CVA and DVA numerical quadrature integration over Monte Carlo exposure profiles.
2. Netting set bilateral adjustment (Net XVA = DVA - CVA).
3. Pre-trade funding valuation adjustment (FVA / FCA).
4. Uncleared Margin Rules (UMR) Margin Valuation Adjustment (MVA).
5. Capital Valuation Adjustment (KVA) as the lifetime hurdle cost of regulatory capital.
6. Running fixed-rate spread conversion for XVA charges.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from risk_ccr_analytics import simulate_interest_rate_swap


def integrate_cva_dva(
    grid: Sequence[float],
    ee_profile: Sequence[float],
    ene_profile: Sequence[float],
    discount_rate: float = 0.035,
    cpty_hazard: float = 0.025,
    cpty_recovery: float = 0.40,
    bank_hazard: float = 0.015,
    bank_recovery: float = 0.40,
) -> tuple[float, float, float]:
    """Integrate Bilateral CVA and DVA using trapezoidal quadrature."""
    n_steps = len(grid) - 1
    lgd_c = 1.0 - cpty_recovery
    lgd_b = 1.0 - bank_recovery

    cva = 0.0
    dva = 0.0

    for i in range(1, n_steps + 1):
        t_prev = grid[i - 1]
        t_curr = grid[i]
        t_mid = 0.5 * (t_prev + t_curr)
        df_mid = math.exp(-discount_rate * t_mid)

        # Marginal default probabilities over [t_{i-1}, t_i]
        dpd_c = math.exp(-cpty_hazard * t_prev) - math.exp(-cpty_hazard * t_curr)
        dpd_b = math.exp(-bank_hazard * t_prev) - math.exp(-bank_hazard * t_curr)

        ee_mid = 0.5 * (ee_profile[i - 1] + ee_profile[i])
        ene_mid = 0.5 * (ene_profile[i - 1] + ene_profile[i])

        cva += lgd_c * df_mid * ee_mid * dpd_c
        dva += lgd_b * df_mid * ene_mid * dpd_b

    net_adj = dva - cva
    return cva, dva, net_adj


def compute_pretrade_funding_charges(
    notional: float,
    epe: float,
    funding_spread: float,
    expected_im: float,
    margin_spread: float,
    tenor: float,
    midpoint_df: float,
) -> dict[str, float]:
    """Compute pre-trade FVA/FCA, MVA, total funding charge, and fixed rate running spread."""
    annuity_proxy = tenor * midpoint_df
    fca = funding_spread * epe * annuity_proxy
    mva = margin_spread * expected_im * annuity_proxy
    total_funding = fca + mva
    running_spread_bps = (total_funding / (notional * annuity_proxy)) * 10_000.0

    return {
        "fca": fca,
        "mva": mva,
        "total_funding": total_funding,
        "annuity_proxy": annuity_proxy,
        "running_spread_bps": running_spread_bps,
    }


def compute_kva(
    cost_of_capital: float,
    expected_capital: float,
    tenor: float,
    midpoint_df: float,
) -> float:
    """Compute Capital Valuation Adjustment (KVA)."""
    return cost_of_capital * expected_capital * midpoint_df * tenor


def run_xva_verification() -> None:
    """Assert all figures quoted in Note 15."""
    # Example 1: Bilateral CVA and DVA on 5y Interest Rate Swap
    swap_sim = simulate_interest_rate_swap(
        maturity=5.0,
        rate_vol=0.010,
        swap_rate=0.040,
        notional=10_000_000.0,
        num_steps=50,
        num_paths=1000,
        seed=42,
    )

    grid = swap_sim["grid"]
    ee = swap_sim["ee"]
    ene = swap_sim["ene"]

    assert isinstance(grid, list)
    assert isinstance(ee, list)
    assert isinstance(ene, list)

    # 5-year cumulative default probabilities:
    # Counterparty: 1 - exp(-0.025 * 5) = 1 - exp(-0.125) = 11.7503%
    # Bank:         1 - exp(-0.015 * 5) = 1 - exp(-0.075) = 7.2257%
    cum_pd_c = 1.0 - math.exp(-0.025 * 5.0)
    cum_pd_b = 1.0 - math.exp(-0.015 * 5.0)
    assert abs(cum_pd_c - 0.117503) < 1e-5
    assert abs(cum_pd_b - 0.072257) < 1e-5

    cva, dva, net_adj = integrate_cva_dva(
        grid=grid,
        ee_profile=ee,
        ene_profile=ene,
        discount_rate=0.035,
        cpty_hazard=0.025,
        cpty_recovery=0.40,
        bank_hazard=0.015,
        bank_recovery=0.40,
    )

    # Assert Note 15 Example 1 figures
    assert abs(cva - 7_336.14) < 1.00, f"CVA mismatch: {cva}"
    assert abs(dva - 4_457.21) < 1.00, f"DVA mismatch: {dva}"
    assert abs(net_adj - (-2_878.93)) < 1.00, f"Net bilateral adjustment mismatch: {net_adj}"

    # Example 2: Pre-Trade Incremental MVA and FVA Pricing
    notional = 10_000_000.0
    epe = 200_000.0
    funding_spread = 0.0080  # 80 bps
    expected_im = 150_000.0
    margin_spread = 0.0100  # 100 bps
    tenor = 5.0
    midpoint_df = 0.916

    funding_res = compute_pretrade_funding_charges(
        notional=notional,
        epe=epe,
        funding_spread=funding_spread,
        expected_im=expected_im,
        margin_spread=margin_spread,
        tenor=tenor,
        midpoint_df=midpoint_df,
    )

    assert abs(funding_res["fca"] - 7_328.00) < 1e-2, f"FCA mismatch: {funding_res['fca']}"
    assert abs(funding_res["mva"] - 6_870.00) < 1e-2, f"MVA mismatch: {funding_res['mva']}"
    assert abs(funding_res["total_funding"] - 14_198.00) < 1e-2, f"Total funding mismatch: {funding_res['total_funding']}"
    assert abs(funding_res["annuity_proxy"] - 4.580) < 1e-4, f"Annuity mismatch: {funding_res['annuity_proxy']}"
    assert abs(funding_res["running_spread_bps"] - 3.10) < 1e-2, f"Running spread mismatch: {funding_res['running_spread_bps']}"

    # KVA verification
    coc = 0.100  # 10%
    expected_capital = 500_000.0
    df_kva = 0.910
    kva = compute_kva(coc, expected_capital, tenor, df_kva)
    assert abs(kva - 227_500.00) < 1e-2, f"KVA mismatch: {kva}"

    print(f"5y Swap Bilateral XVA: CVA=${cva:,.2f}, DVA=${dva:,.2f}, Net Adjustment=${net_adj:,.2f}")
    print(f"Pre-Trade Funding Charges: FCA=${funding_res['fca']:,.2f}, MVA=${funding_res['mva']:,.2f}")
    print(f"Total Funding Cost: ${funding_res['total_funding']:,.2f} -> {funding_res['running_spread_bps']:.2f} bps running")
    print(f"Regulatory KVA: ${kva:,.2f}")
    print("All XVA pricing and valuation adjustment tests passed successfully!")


if __name__ == "__main__":
    run_xva_verification()
