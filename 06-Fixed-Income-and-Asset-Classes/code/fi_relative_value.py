"""Fixed Income P&L Attribution and Relative Value Reference Engine.

Asserts every quantitative figure quoted in Note 24
(24-Fixed-Income-PnL-and-Relative-Value.md) to within half a unit
in the last quoted decimal place using standard-library pure Python.
"""


def pnl_attribution_1d(
    notional: float,
    dirty_price: float,
    mod_duration: float,
    annual_convexity: float,
    coupon_rate: float,
    repo_rate: float,
    parallel_shift: float,
    rolldown_shift: float,
    day_count_basis: int = 360,
) -> tuple[float, float, float, float, float, float, float]:
    """Calculate 1-day P&L attribution components.

    Returns:
        (portfolio_val, dv01, dollar_convexity, carry, rolldown, delta_pnl, convexity_pnl, total_pnl)
    """
    p_val = notional * (dirty_price / 100.0)
    dv01 = p_val * mod_duration * 0.0001
    dollar_convexity = p_val * annual_convexity

    dt = 1.0 / day_count_basis
    carry = (coupon_rate * notional - repo_rate * p_val) * dt
    rolldown = -p_val * mod_duration * rolldown_shift
    delta_pnl = -p_val * mod_duration * parallel_shift
    convexity_pnl = 0.5 * dollar_convexity * (parallel_shift**2)

    total_pnl = carry + rolldown + delta_pnl + convexity_pnl
    return p_val, dv01, dollar_convexity, carry, rolldown, delta_pnl, convexity_pnl, total_pnl


def butterfly_50_50_weighting(
    body_notional: float,
    dv01_per_100k_wing1: float,
    dv01_per_100k_body: float,
    dv01_per_100k_wing2: float,
) -> tuple[float, float, float, float, float, float]:
    """Calculate 50-50 DV01 weighting for a butterfly trade.

    Returns:
        (body_dv01, target_dv01_w1, target_dv01_w2, notional_w1, notional_w2, net_dv01)
    """
    body_dv01 = (body_notional / 100_000.0) * dv01_per_100k_body
    target_dv01_w1 = 0.50 * body_dv01
    target_dv01_w2 = 0.50 * body_dv01

    notional_w1 = (target_dv01_w1 / dv01_per_100k_wing1) * 100_000.0
    notional_w2 = (target_dv01_w2 / dv01_per_100k_wing2) * 100_000.0
    net_dv01 = (target_dv01_w1 + target_dv01_w2) - body_dv01

    return body_dv01, target_dv01_w1, target_dv01_w2, notional_w1, notional_w2, net_dv01


def par_par_asw_spread(
    bond_yield: float,
    swap_rate: float,
    clean_price: float,
    pv01_swap: float,
) -> float:
    """Calculate approximate par-par asset swap spread."""
    upfront_adjustment = (100.0 - clean_price) / (100.0 * pv01_swap)
    return (bond_yield - swap_rate) / (1.0 + upfront_adjustment)


def main() -> None:
    # 1. P&L Attribution (Example 1)
    notional = 100_000_000.0
    dirty_p = 99.20
    d_mod = 8.20
    c_ann = 78.0
    c_rate = 0.0410  # 4.10%
    repo_r = 0.0400  # 4.00%
    dy_par = 0.0005  # +5 bps
    dy_roll = -0.00003  # -0.3 bps roll-down

    p_val, dv01, c_dollar, carry, rdown, delta_pnl, conv_pnl, tot_pnl = pnl_attribution_1d(
        notional, dirty_p, d_mod, c_ann, c_rate, repo_r, dy_par, dy_roll
    )

    assert round(p_val, 2) == 99_200_000.00, f"Expected $99.2M, got {p_val}"
    assert round(dv01, 2) == 81_344.00, f"Expected $81,344, got {dv01}"
    assert round(c_dollar, 2) == 7_737_600_000.00, f"Expected $7,737,600,000, got {c_dollar}"
    assert round(carry, 2) == 366.67, f"Expected carry $366.67, got {carry}"
    assert round(rdown, 2) == 24_403.20, f"Expected roll-down $24,403.20, got {rdown}"

    static_return = carry + rdown
    assert round(static_return, 2) == 24_769.87, f"Expected static horizon return $24,769.87, got {static_return}"

    assert round(delta_pnl, 2) == -406_720.00, f"Expected delta PnL -$406,720.00, got {delta_pnl}"
    assert round(conv_pnl, 2) == 967.20, f"Expected convexity PnL $967.20, got {conv_pnl}"
    assert round(tot_pnl, 2) == -380_982.93, f"Expected total PnL -$380,982.93, got {tot_pnl}"

    # 2. 2s-5s-10s Butterfly Trade (Example 2)
    body_notional = 100_000_000.0
    dv01_2y = 19.50
    dv01_5y = 44.20
    dv01_10y = 81.50

    b_dv01, t_w1, t_w2, n_w1, n_w2, net_dv01 = butterfly_50_50_weighting(body_notional, dv01_2y, dv01_5y, dv01_10y)

    assert round(b_dv01, 2) == 44_200.00, f"Expected body DV01 $44,200, got {b_dv01}"
    assert round(t_w1, 2) == 22_100.00, f"Expected wing 1 DV01 $22,100, got {t_w1}"
    assert round(t_w2, 2) == 22_100.00, f"Expected wing 2 DV01 $22,100, got {t_w2}"
    assert round(n_w1, 0) == 113_333_333.0, f"Expected 2y notional $113,333,333, got {n_w1}"
    assert round(n_w2, 0) == 27_116_564.0, f"Expected 10y notional $27,116,564, got {n_w2}"
    assert round(net_dv01, 6) == 0.0, f"Expected net DV01 $0, got {net_dv01}"

    # 3. Par-Par Asset Swap Spread
    y_b = 0.0445  # 4.45%
    y_sw = 0.0410  # 4.10%
    p_clean = 98.00  # discount
    pv01_sw = 7.50

    asw = par_par_asw_spread(y_b, y_sw, p_clean, pv01_sw)
    assert round(asw * 10000, 2) == 34.91, f"Expected ASW 34.91 bps, got {asw * 10000}"

    print("All fi_relative_value assertions passed successfully.")


if __name__ == "__main__":
    main()
