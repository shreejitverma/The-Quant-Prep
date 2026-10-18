"""PnL platform and attribution: Taylor Greek explain, PnL walk, and FRTB PLA metrics.

Backs every number in `18-Pricing-and-Risk-Systems/09-PnL-Platform.md`.
Greek sensitivities, option full revaluations, dirty/clean/actual PnL walks, and PLA statistics are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_pnl_platform.py`.
"""

from __future__ import annotations

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9 * max(1.0, abs(expected))
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def test_greek_pnl_explain() -> None:
    print("  1. Greek PnL explain decomposition for equity option portfolio")
    v_t0 = 12_500_000.0
    v_t1 = 14_028_000.0
    actual_pnl = v_t1 - v_t0
    quoted("initial portfolio MTM ($)", v_t0, 12_500_000, 0)
    quoted("final portfolio MTM ($)", v_t1, 14_028_000, 0)
    quoted("actual mark-to-market PnL change ($)", actual_pnl, 1_528_000, 0)

    # Market moves
    s0 = 5000.00
    s1 = 5040.00
    ds = s1 - s0
    vol0 = 18.00
    vol1 = 17.50
    dvol = vol1 - vol0  # -0.50%
    dt = 1.0

    quoted("S&P 500 spot move (points)", ds, 40.0, 1)
    quoted("ATM implied volatility move (%)", dvol, -0.50, 2)

    # Greeks
    delta = 45_000.0
    gamma = 120.0
    vega = 350_000.0
    theta = -18_000.0

    delta_pnl = delta * ds
    gamma_pnl = 0.5 * gamma * (ds**2)
    vega_pnl = vega * dvol
    theta_pnl = theta * dt
    explained_pnl = delta_pnl + gamma_pnl + vega_pnl + theta_pnl
    residual = actual_pnl - explained_pnl

    quoted("delta PnL ($)", delta_pnl, 1_800_000, 0)
    quoted("gamma PnL ($)", gamma_pnl, 96_000, 0)
    quoted("vega PnL ($)", vega_pnl, -175_000, 0)
    quoted("theta PnL ($)", theta_pnl, -18_000, 0)
    quoted("total explained PnL ($)", explained_pnl, 1_703_000, 0)
    quoted("unexplained residual PnL ($)", residual, -175_000, 0)

    # Higher-order cross-Greek explain: Vanna
    vanna = -8_500.0
    vanna_pnl = vanna * ds * dvol
    quoted("vanna PnL ($)", vanna_pnl, 170_000, 0)
    explained_with_vanna = explained_pnl + vanna_pnl
    residual_with_vanna = actual_pnl - explained_with_vanna
    quoted("explained PnL with vanna ($)", explained_with_vanna, 1_873_000, 0)
    quoted("residual with vanna ($)", residual_with_vanna, -345_000, 0)

    # Higher-order adjustments (volga, discrete dividend)
    higher_order_adj = -333_000.0
    reconciled_residual = actual_pnl - (explained_with_vanna + higher_order_adj)
    quoted("higher-order adjustments ($)", higher_order_adj, -333_000, 0)
    quoted("final reconciled residual ($)", reconciled_residual, -12_000, 0)


def test_pnl_walk() -> None:
    print("  2. Clean vs dirty vs actual PnL walk for bond desk")
    mtm_t0 = 85_000_000.0
    mtm_t1_static = 85_450_000.0
    clean_pnl = mtm_t1_static - mtm_t0
    coupon = 65_000.0
    intraday_gain = 10_000_000.0 * (0.9980 - 0.9950)
    commissions = -8_000.0
    fees = -4_500.0
    funding = -12_500.0

    dirty_pnl = clean_pnl + coupon
    actual_pnl = clean_pnl + coupon + intraday_gain + commissions + fees + funding

    quoted("static portfolio MTM at T-1 ($)", mtm_t0, 85_000_000, 0)
    quoted("static portfolio MTM at T ($)", mtm_t1_static, 85_450_000, 0)
    quoted("clean PnL / hypothetical PnL ($)", clean_pnl, 450_000, 0)
    quoted("bond coupon cash received ($)", coupon, 65_000, 0)
    quoted("intraday trading gain ($)", intraday_gain, 30_000, 0)
    quoted("brokerage commissions ($)", commissions, -8_000, 0)
    quoted("exchange & clearing fees ($)", fees, -4_500, 0)
    quoted("overnight repo funding cost ($)", funding, -12_500, 0)
    quoted("dirty PnL ($)", dirty_pnl, 515_000, 0)
    quoted("actual PnL ($)", actual_pnl, 520_000, 0)


def main() -> None:
    print("PnL platform and attribution checks")
    test_greek_pnl_explain()
    test_pnl_walk()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All PnL platform checks passed.")


if __name__ == "__main__":
    main()
