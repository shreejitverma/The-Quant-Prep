"""Counterparty Credit Risk Exposure Profiles and XVA Analytics.

Pure Python 3.10+ standard library implementation:
1. Monte Carlo simulation of derivative portfolio exposures (Swap and Forward).
2. Counterparty exposure profile analytics: Expected Exposure (EE),
   Potential Future Exposure (PFE 95% and 99%), and Effective EPE.
3. ISDA Master Agreement netting and Net-to-Gross Ratio (NGR).
4. Credit Support Annex (CSA) collateralization with Threshold and MTA
   (instantaneous collateral approximation without MPOR lag).
5. Bilateral Credit Valuation Adjustment (CVA) and Debit Valuation Adjustment (DVA).
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# ============================================================================
# 1. Exposure Simulation: Swaps and Forwards
# ============================================================================


@dataclass
class ExposureProfile:
    grid: list[float]  # time grid in years
    ee: list[float]  # Expected Exposure E[max(V, 0)]
    ene: list[float]  # Expected Negative Exposure E[max(-V, 0)]
    pfe_95: list[float]  # 95% quantile of max(V, 0)
    pfe_99: list[float]  # 99% quantile of max(V, 0)
    effective_ee: list[float]  # Non-decreasing envelope EEE(t)
    epe: float  # Expected Positive Exposure (average EE)
    effective_epe: float  # Effective EPE (average EEE over 1 year or tenor)


def simulate_forward_contract(
    maturity: float = 5.0,
    annual_vol: float = 0.20,
    r: float = 0.03,
    notional: float = 1_000_000.0,
    num_steps: int = 50,
    num_paths: int = 2000,
    seed: int = 42,
) -> ExposureProfile:
    """Simulate exposure of a par forward struck at K = S0 * exp(r * T).

    Mark-to-market is V(t) = N * (S(t) / S0 - exp(r * t)), so E[V(t)] = 0.
    Exposure grows with sqrt(t).
    """
    rng = random.Random(seed)
    dt = maturity / num_steps
    grid = [i * dt for i in range(num_steps + 1)]

    # Under the risk-neutral drift: dS = r S dt + sigma S dW, S(0) = 100.
    s0 = 100.0

    # Matrix of path values: [step][path]. V(0) = 0 for a par forward.
    values: list[list[float]] = [[0.0] * num_paths for _ in range(num_steps + 1)]

    for p in range(num_paths):
        s = s0
        for i in range(1, num_steps + 1):
            t = grid[i]
            z = rng.gauss(0.0, 1.0)
            s = s * math.exp((r - 0.5 * annual_vol**2) * dt + annual_vol * math.sqrt(dt) * z)
            # Par delivery price K = S0*exp(r*T): V(t) = N*(S(t)/S0 - exp(r*t))
            v = notional * (s / s0 - math.exp(r * t))
            values[i][p] = v

    return _calculate_exposure_metrics(grid, values)


def simulate_interest_rate_swap(
    maturity: float = 5.0,
    rate_vol: float = 0.010,  # 100 bps annual normal volatility
    swap_rate: float = 0.040,  # 4.0% par swap
    notional: float = 10_000_000.0,
    num_steps: int = 50,
    num_paths: int = 2000,
    seed: int = 42,
) -> ExposureProfile:
    """Simulate exposure profile for a payer interest rate swap.

    Exhibits classic hump shape: diffusion increases uncertainty early,
    while remaining annuity amortization pulls exposure to zero at maturity.
    """
    rng = random.Random(seed)
    dt = maturity / num_steps
    grid = [i * dt for i in range(num_steps + 1)]

    values: list[list[float]] = [[0.0] * num_paths for _ in range(num_steps + 1)]

    for p in range(num_paths):
        s_t = swap_rate
        for i in range(1, num_steps + 1):
            t = grid[i]
            z = rng.gauss(0.0, 1.0)
            # Arithmetic Brownian motion with zero drift under swap measure
            s_t = s_t + rate_vol * math.sqrt(dt) * z
            # Remaining annuity: A(t) = (1 - exp(-0.04 * (T - t))) / 0.04
            rem_time = max(0.0, maturity - t)
            annuity = (1.0 - math.exp(-swap_rate * rem_time)) / swap_rate if swap_rate > 0 else rem_time
            # Payer swap value: Notional * (S(t) - K) * A(t)
            v = notional * (s_t - swap_rate) * annuity
            values[i][p] = v

    return _calculate_exposure_metrics(grid, values)


def _calculate_exposure_metrics(grid: list[float], values: list[list[float]]) -> ExposureProfile:
    """Compute statistical exposure metrics from simulated path matrices."""
    num_steps = len(grid) - 1
    num_paths = len(values[0])

    ee: list[float] = [0.0] * (num_steps + 1)
    ene: list[float] = [0.0] * (num_steps + 1)
    pfe_95: list[float] = [0.0] * (num_steps + 1)
    pfe_99: list[float] = [0.0] * (num_steps + 1)
    effective_ee: list[float] = [0.0] * (num_steps + 1)

    idx_95 = int(math.floor(0.95 * num_paths))
    idx_99 = int(math.floor(0.99 * num_paths))

    for i in range(num_steps + 1):
        step_vals = values[i]
        pos_exposures = [max(0.0, v) for v in step_vals]
        neg_exposures = [max(0.0, -v) for v in step_vals]

        ee[i] = sum(pos_exposures) / num_paths
        ene[i] = sum(neg_exposures) / num_paths

        sorted_pos = sorted(pos_exposures)
        pfe_95[i] = sorted_pos[idx_95]
        pfe_99[i] = sorted_pos[idx_99]

        if i == 0:
            effective_ee[i] = ee[i]
        else:
            effective_ee[i] = max(effective_ee[i - 1], ee[i])

    def time_average(profile: list[float], horizon: float) -> float:
        if horizon <= 0.0:
            return 0.0

        area = 0.0
        left_time = grid[0]
        left_value = profile[0]
        for right_time, right_value in zip(grid[1:], profile[1:], strict=True):
            if left_time >= horizon:
                break
            end_time = min(right_time, horizon)
            fraction = (end_time - left_time) / (right_time - left_time)
            end_value = left_value + fraction * (right_value - left_value)
            area += (left_value + end_value) * 0.5 * (end_time - left_time)
            if end_time == horizon:
                break
            left_time = right_time
            left_value = right_value
        return area / horizon

    # Expected Positive Exposure (EPE): time-average EE over maturity
    epe = time_average(ee, grid[-1])

    # Effective EPE: time-average Effective EE over the first year or tenor
    effective_epe = time_average(effective_ee, min(1.0, grid[-1]))

    return ExposureProfile(
        grid=grid,
        ee=ee,
        ene=ene,
        pfe_95=pfe_95,
        pfe_99=pfe_99,
        effective_ee=effective_ee,
        epe=epe,
        effective_epe=effective_epe,
    )


# ============================================================================
# 2. Netting and Collateral Analytics
# ============================================================================


def evaluate_netting_set(
    trades_values: Sequence[Sequence[float]],
) -> tuple[float, float, float]:
    """Calculate Gross Exposure, Net Exposure, and Net-to-Gross Ratio (NGR).

    trades_values[trade_idx][path_idx] represents simulated values across trades.
    """
    num_trades = len(trades_values)
    num_paths = len(trades_values[0])

    gross_exposure = 0.0
    net_exposure = 0.0

    for p in range(num_paths):
        path_gross = sum(max(0.0, trades_values[t][p]) for t in range(num_trades))
        path_net = max(0.0, sum(trades_values[t][p] for t in range(num_trades)))

        gross_exposure += path_gross
        net_exposure += path_net

    avg_gross = gross_exposure / num_paths
    avg_net = net_exposure / num_paths
    ngr = (avg_net / avg_gross) if avg_gross > 0 else 0.0

    return avg_gross, avg_net, ngr


def apply_csa_collateral(
    uncollateralized_values: Sequence[float],
    threshold: float = 0.0,
    mta: float = 50_000.0,
) -> list[float]:
    """Apply Credit Support Annex (CSA) Variation Margin with Threshold and MTA."""
    collateralized: list[float] = []

    for v in uncollateralized_values:
        if v <= threshold:
            # Below threshold: zero collateral posted by counterparty
            collateral_held = 0.0
        else:
            unthresholded = v - threshold
            if unthresholded < mta:
                # Below Minimum Transfer Amount: no call made
                collateral_held = 0.0
            else:
                # Collateral held equals full excess above threshold
                collateral_held = unthresholded

        # Net unhedged exposure to the bank
        net_exp = max(0.0, v - collateral_held)
        collateralized.append(net_exp)

    return collateralized


# ============================================================================
# 3. Bilateral CVA and DVA Calculation
# ============================================================================


def calculate_cva_dva(
    exposure: ExposureProfile,
    discount_curve: Callable[[float], float],
    counterparty_hazard_rate: float = 0.020,  # 2.0% hazard rate (~120 bp CDS)
    counterparty_recovery: float = 0.40,  # 40% recovery (60% LGD)
    bank_hazard_rate: float = 0.010,  # 1.0% bank hazard rate (~60 bp CDS)
    bank_recovery: float = 0.40,
) -> tuple[float, float, float]:
    """Calculate Bilateral CVA, DVA, and Net Bilateral Adjustment using trapezoidal integration."""
    grid = exposure.grid
    ee = exposure.ee
    ene = exposure.ene
    num_steps = len(grid) - 1

    lgd_c = 1.0 - counterparty_recovery
    lgd_b = 1.0 - bank_recovery

    cva = 0.0
    dva = 0.0

    for i in range(num_steps):
        t1 = grid[i]
        t2 = grid[i + 1]
        t_mid = 0.5 * (t1 + t2)

        df = discount_curve(t_mid)

        # Counterparty default probability over [t1, t2]
        # P(tau_c in [t1, t2]) = exp(-lambda * t1) - exp(-lambda * t2)
        surv_c1 = math.exp(-counterparty_hazard_rate * t1)
        surv_c2 = math.exp(-counterparty_hazard_rate * t2)
        dpd_c = surv_c1 - surv_c2

        # Bank default probability over [t1, t2]
        surv_b1 = math.exp(-bank_hazard_rate * t1)
        surv_b2 = math.exp(-bank_hazard_rate * t2)
        dpd_b = surv_b1 - surv_b2

        # Midpoint exposures
        ee_mid = 0.5 * (ee[i] + ee[i + 1])
        ene_mid = 0.5 * (ene[i] + ene[i + 1])

        cva += lgd_c * df * ee_mid * dpd_c
        dva += lgd_b * df * ene_mid * dpd_b

    net_adj = dva - cva  # Bank benefit minus counterparty risk
    return cva, dva, net_adj


# ============================================================================
# 4. Verification Tests
# ============================================================================


def run_tests() -> None:
    print("Testing Counterparty Credit Risk, Exposure Profiles, and XVA...")

    def discount_curve(t: float) -> float:
        return math.exp(-0.035 * t)

    # 1. Forward Contract Exposure Simulation
    fwd_exp = simulate_forward_contract(
        maturity=5.0,
        annual_vol=0.20,
        r=0.03,
        notional=1_000_000.0,
        num_steps=50,
        num_paths=1000,
        seed=42,
    )
    # Forward exposure strictly increases with time: EE(5y) > EE(1y)
    assert fwd_exp.ee[-1] > fwd_exp.ee[10], "Forward EE must increase with time"
    # Par-forward closed form: E[max(N*(S(t)/S0 - exp(r*t)), 0)]
    # = N*exp(r*t)*(2*Phi(0.5*sigma*sqrt(t)) - 1)
    half_01 = 0.5 * 0.20 * math.sqrt(fwd_exp.grid[1])
    ee_01_closed = 1_000_000.0 * math.exp(0.03 * fwd_exp.grid[1]) * (2.0 * norm_cdf(half_01) - 1.0)
    assert math.isclose(fwd_exp.ee[1], ee_01_closed, rel_tol=0.10), (
        f"Simulated forward EE({fwd_exp.grid[1]:.1f}y) {fwd_exp.ee[1]} deviates from closed-form {ee_01_closed}"
    )
    half_1 = 0.5 * 0.20 * math.sqrt(fwd_exp.grid[10])
    ee_1_closed = 1_000_000.0 * math.exp(0.03 * fwd_exp.grid[10]) * (2.0 * norm_cdf(half_1) - 1.0)
    assert math.isclose(fwd_exp.ee[10], ee_1_closed, rel_tol=0.10), (
        f"Simulated forward EE(1y) {fwd_exp.ee[10]} deviates from closed-form {ee_1_closed}"
    )
    # PFE 99% must exceed PFE 95%
    assert fwd_exp.pfe_99[25] > fwd_exp.pfe_95[25], "PFE 99% must exceed PFE 95%"
    print(f"5y Forward EE at maturity: ${fwd_exp.ee[-1]:,.2f}, 95% PFE: ${fwd_exp.pfe_95[-1]:,.2f}")

    # 2. Interest Rate Swap Exposure Simulation (Hump Shape)
    swap_exp = simulate_interest_rate_swap(
        maturity=5.0,
        rate_vol=0.010,
        swap_rate=0.040,
        notional=10_000_000.0,
        num_steps=50,
        num_paths=1000,
        seed=42,
    )
    # Swap exposure peaks in middle and drops toward maturity: EE(mid) > EE(end)
    mid_idx = 25
    assert swap_exp.ee[mid_idx] > swap_exp.ee[-1], f"Swap EE must exhibit hump shape: {swap_exp.ee[mid_idx]} vs {swap_exp.ee[-1]}"
    # Verify swap EE at t=1.0 against analytical ABM closed form: N * A(t) * sigma * sqrt(t) * phi(0)
    # A(1.0) = (1 - exp(-0.04 * 4)) / 0.04 ~= 3.6964074; phi(0) = 1 / sqrt(2*pi) ~= 0.39894228
    ee_1y_closed_form = 10_000_000.0 * ((1.0 - math.exp(-0.04 * 4.0)) / 0.04) * 0.010 * 1.0 / math.sqrt(2.0 * math.pi)
    assert math.isclose(swap_exp.ee[10], ee_1y_closed_form, rel_tol=0.05), (
        f"Simulated EE(1y) {swap_exp.ee[10]} deviates from closed-form {ee_1y_closed_form}"
    )
    print(f"5y Swap Peak EE (Year 2.5): ${swap_exp.ee[mid_idx]:,.2f}, Terminal EE: ${swap_exp.ee[-1]:,.2f}")
    print(f"5y Swap EPE: ${swap_exp.epe:,.2f}, Effective EPE: ${swap_exp.effective_epe:,.2f}")

    # 3. Netting Set Analytics
    # Two offsetting trades: Trade 1 = +$100k, Trade 2 = -$60k
    t1_paths = [100_000.0, 50_000.0, -20_000.0, 80_000.0]
    t2_paths = [-60_000.0, -40_000.0, 30_000.0, -70_000.0]
    gross_exp, net_exp, ngr = evaluate_netting_set([t1_paths, t2_paths])
    # Exact hand-computed oracles:
    # Gross = (100k + 50k + 30k + 80k) / 4 = 260k / 4 = 65,000.0
    # Net = (max(0, 40k) + max(0, 10k) + max(0, 10k) + max(0, 10k)) / 4 = 70k / 4 = 17,500.0
    # NGR = 17,500 / 65,000 = 0.2692307...
    assert math.isclose(gross_exp, 65_000.0, rel_tol=1e-5), f"Expected gross 65k, got {gross_exp}"
    assert math.isclose(net_exp, 17_500.0, rel_tol=1e-5), f"Expected net 17.5k, got {net_exp}"
    assert math.isclose(ngr, 17_500.0 / 65_000.0, rel_tol=1e-5), f"Expected NGR 0.2692, got {ngr}"
    print(f"Netting Set: Gross=${gross_exp:,.2f}, Net=${net_exp:,.2f}, NGR={ngr:.2%}")

    # 4. CSA Collateralization
    uncol = [200_000.0, 40_000.0, 150_000.0]
    col = apply_csa_collateral(uncol, threshold=50_000.0, mta=20_000.0)
    # For 200k: excess 150k > MTA 20k -> collateral 150k -> net 50k
    assert col[0] == 50_000.0
    # For 40k: below threshold 50k -> zero collateral -> net 40k
    assert col[1] == 40_000.0
    # For 150k: excess 100k > MTA 20k -> collateral 100k -> net 50k
    assert col[2] == 50_000.0

    # 5. Bilateral CVA / DVA
    cva, dva, net_xva = calculate_cva_dva(
        swap_exp,
        discount_curve,
        counterparty_hazard_rate=0.025,
        counterparty_recovery=0.40,
        bank_hazard_rate=0.015,
        bank_recovery=0.40,
    )
    assert cva > 0.0, "CVA must be strictly positive"
    assert dva > 0.0, "DVA must be strictly positive"
    print(f"Bilateral XVA: CVA=${cva:,.2f}, DVA=${dva:,.2f}, Net Adjustment=${net_xva:,.2f}")

    # Analytic CVA check on flat constant exposure profile with zero interest rates:
    # LGD * EE_const * (1 - exp(-hazard * T))
    flat_ee = ExposureProfile(
        grid=[0.0, 1.0, 2.0],
        ee=[100_000.0, 100_000.0, 100_000.0],
        ene=[0.0, 0.0, 0.0],
        pfe_95=[100_000.0] * 3,
        pfe_99=[100_000.0] * 3,
        effective_ee=[100_000.0] * 3,
        epe=100_000.0,
        effective_epe=100_000.0,
    )
    cva_flat, _, _ = calculate_cva_dva(
        flat_ee,
        lambda t: 1.0,
        counterparty_hazard_rate=0.02,
        counterparty_recovery=0.40,
        bank_hazard_rate=0.01,
        bank_recovery=0.40,
    )
    expected_cva_flat = 0.60 * 100_000.0 * (1.0 - math.exp(-0.02 * 2.0))
    assert math.isclose(cva_flat, expected_cva_flat, rel_tol=1e-4), f"Analytic CVA mismatch: {cva_flat} vs {expected_cva_flat}"

    print("All counterparty risk, exposure profile, and XVA tests passed!")


if __name__ == "__main__":
    run_tests()
