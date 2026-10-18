"""Counterparty Credit Risk Analytics and Exposure Profiling Engine.

Pure Python 3.10+ standard library implementation:
1. Bilateral netting sets: Gross Exposure, Net Exposure, Net-to-Gross Ratio (NGR), and Basel factor.
2. Monte Carlo exposure simulation for forward contracts (monotonic diffusion).
3. Monte Carlo exposure simulation for interest rate swaps (hump shape: diffusion vs annuity amortization).
4. Quantile metrics: Expected Exposure (EE), Potential Future Exposure (PFE 95%), and ENE.
5. Basel regulatory metrics: Effective Expected Exposure (EEE) envelope, Expected Positive Exposure (EPE),
   Effective EPE, and Regulatory Exposure at Default (EAD = alpha * Effective EPE).
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence


def compute_netting_set_metrics(trade_values: Sequence[float]) -> dict[str, float]:
    """Calculate Gross Exposure, Net Exposure, NGR, and Basel standardized netting factor."""
    gross = sum(max(v, 0.0) for v in trade_values)
    net = max(sum(trade_values), 0.0)
    ngr = (net / gross) if gross > 0.0 else 0.0
    basel_factor = 0.4 + 0.6 * ngr
    return {
        "gross_exposure": gross,
        "net_exposure": net,
        "ngr": ngr,
        "basel_netting_factor": basel_factor,
    }


def simulate_forward_contract(
    maturity: float = 5.0,
    annual_vol: float = 0.20,
    r: float = 0.03,
    notional: float = 1_000_000.0,
    num_steps: int = 50,
    num_paths: int = 1000,
    seed: int = 42,
) -> dict[str, list[float]]:
    """Simulate exposure profile for a forward contract."""
    rng = random.Random(seed)
    dt = maturity / num_steps
    grid = [i * dt for i in range(num_steps + 1)]
    s0 = 100.0

    values: list[list[float]] = [[0.0] * num_paths for _ in range(num_steps + 1)]

    for p in range(num_paths):
        s = s0
        for i in range(1, num_steps + 1):
            t = grid[i]
            z = rng.gauss(0.0, 1.0)
            s = s * math.exp((r - 0.5 * annual_vol**2) * dt + annual_vol * math.sqrt(dt) * z)
            v = notional * (s / s0 - math.exp(r * t))
            values[i][p] = v

    ee: list[float] = []
    pfe_95: list[float] = []

    for i in range(num_steps + 1):
        pos_v = [max(0.0, v) for v in values[i]]
        sorted_pos = sorted(pos_v)
        idx_95 = int(math.floor(0.95 * num_paths))
        ee.append(sum(pos_v) / num_paths)
        pfe_95.append(sorted_pos[min(idx_95, num_paths - 1)])

    return {
        "grid": grid,
        "ee": ee,
        "pfe_95": pfe_95,
    }


def simulate_interest_rate_swap(
    maturity: float = 5.0,
    rate_vol: float = 0.010,  # 100 bps annual normal volatility
    swap_rate: float = 0.040,  # 4.0% par swap
    notional: float = 10_000_000.0,
    num_steps: int = 50,
    num_paths: int = 1000,
    seed: int = 42,
) -> dict[str, list[float] | float]:
    """Simulate exposure profile for a payer interest rate swap."""
    rng = random.Random(seed)
    dt = maturity / num_steps
    grid = [i * dt for i in range(num_steps + 1)]

    values: list[list[float]] = [[0.0] * num_paths for _ in range(num_steps + 1)]

    for p in range(num_paths):
        s_t = swap_rate
        for i in range(1, num_steps + 1):
            t = grid[i]
            z = rng.gauss(0.0, 1.0)
            s_t = s_t + rate_vol * math.sqrt(dt) * z
            rem_time = max(0.0, maturity - t)
            annuity = (1.0 - math.exp(-swap_rate * rem_time)) / swap_rate if swap_rate > 0 else rem_time
            v = notional * (s_t - swap_rate) * annuity
            values[i][p] = v

    ee: list[float] = []
    ene: list[float] = []
    pfe_95: list[float] = []
    pfe_99: list[float] = []

    for i in range(num_steps + 1):
        pos_v = [max(0.0, v) for v in values[i]]
        neg_v = [max(0.0, -v) for v in values[i]]
        sorted_pos = sorted(pos_v)
        idx_95 = int(math.floor(0.95 * num_paths))
        idx_99 = int(math.floor(0.99 * num_paths))

        ee.append(sum(pos_v) / num_paths)
        ene.append(sum(neg_v) / num_paths)
        pfe_95.append(sorted_pos[min(idx_95, num_paths - 1)])
        pfe_99.append(sorted_pos[min(idx_99, num_paths - 1)])

    # Effective EE: EEE(t) = max_{s <= t} EE(s)
    effective_ee = [ee[0]]
    for i in range(1, num_steps + 1):
        effective_ee.append(max(effective_ee[-1], ee[i]))

    # EPE: average EE over full maturity T
    epe = sum(0.5 * (ee[i - 1] + ee[i]) * dt for i in range(1, num_steps + 1)) / maturity

    # Effective EPE: average EEE over 1 year (min(T, 1y))
    steps_1y = int(round(1.0 / dt))
    effective_epe = sum(0.5 * (effective_ee[i - 1] + effective_ee[i]) * dt for i in range(1, steps_1y + 1)) / 1.0

    regulatory_ead = 1.4 * effective_epe

    return {
        "grid": grid,
        "ee": ee,
        "ene": ene,
        "pfe_95": pfe_95,
        "pfe_99": pfe_99,
        "effective_ee": effective_ee,
        "epe": epe,
        "effective_epe": effective_epe,
        "regulatory_ead": regulatory_ead,
    }


def run_ccr_verification() -> None:
    """Assert all figures quoted in Note 14."""
    # Example 1: Netting Set and NGR
    trades = [12_000_000.0, -8_500_000.0, 1_500_000.0]
    metrics = compute_netting_set_metrics(trades)

    assert abs(metrics["gross_exposure"] - 13_500_000.0) < 1e-4, f"Gross exposure mismatch: {metrics['gross_exposure']}"
    assert abs(metrics["net_exposure"] - 5_000_000.0) < 1e-4, f"Net exposure mismatch: {metrics['net_exposure']}"
    assert abs(metrics["ngr"] - 0.37037037) < 1e-5, f"NGR mismatch: {metrics['ngr']}"
    assert abs(metrics["basel_netting_factor"] - 0.62222222) < 1e-5, f"Basel factor mismatch: {metrics['basel_netting_factor']}"

    # Example 2: Swap Exposure Profile Simulation (1000 paths, seed 42)
    swap_res = simulate_interest_rate_swap(
        maturity=5.0,
        rate_vol=0.010,
        swap_rate=0.040,
        notional=10_000_000.0,
        num_steps=50,
        num_paths=1000,
        seed=42,
    )

    ee = swap_res["ee"]
    pfe = swap_res["pfe_95"]
    time_grid = swap_res["grid"]

    assert isinstance(ee, list)
    assert isinstance(pfe, list)
    assert isinstance(time_grid, list)

    # Step at t = 0.0 (index 0)
    assert abs(ee[0] - 0.00) < 1e-4
    assert abs(pfe[0] - 0.00) < 1e-4

    # Step at t = 1.0 (index 10)
    assert abs(ee[10] - 144_101.27) < 0.50, f"EE(1.0) mismatch: {ee[10]}"
    assert abs(pfe[10] - 608_302.12) < 0.50, f"PFE(1.0) mismatch: {pfe[10]}"

    # Peak Hump: step at t = 2.3 (index 23)
    assert abs(ee[23] - 159_124.02) < 0.50, f"Peak EE(2.3) mismatch: {ee[23]}"
    assert abs(pfe[23] - 655_890.68) < 0.50, f"Peak PFE(2.3) mismatch: {pfe[23]}"

    # Step at t = 2.5 (index 25)
    assert abs(ee[25] - 153_456.89) < 0.50, f"EE(2.5) mismatch: {ee[25]}"
    assert abs(pfe[25] - 614_332.86) < 0.50, f"PFE(2.5) mismatch: {pfe[25]}"

    # Terminal at t = 5.0 (index 50)
    assert abs(ee[50] - 0.00) < 1e-4
    assert abs(pfe[50] - 0.00) < 1e-4

    # EPE and Effective EPE integration
    epe = float(swap_res["epe"])
    effective_epe = float(swap_res["effective_epe"])
    ead = float(swap_res["regulatory_ead"])

    assert abs(epe - 111_327.61) < 0.50, f"EPE mismatch: {epe}"
    assert abs(effective_epe - 102_386.87) < 0.50, f"Effective EPE mismatch: {effective_epe}"
    assert abs(ead - 143_341.62) < 0.50, f"Regulatory EAD mismatch: {ead}"

    # Forward exposure verification
    fwd_res = simulate_forward_contract(
        maturity=5.0,
        annual_vol=0.20,
        r=0.03,
        notional=1_000_000.0,
        num_steps=50,
        num_paths=1000,
        seed=42,
    )
    fwd_ee = fwd_res["ee"]
    fwd_pfe = fwd_res["pfe_95"]
    assert abs(fwd_ee[-1] - 199_571.89) < 0.50, f"5y Forward EE mismatch: {fwd_ee[-1]}"
    assert abs(fwd_pfe[-1] - 936_262.07) < 0.50, f"5y Forward PFE mismatch: {fwd_pfe[-1]}"

    print(f"Netting Set: Gross=${metrics['gross_exposure']:,.2f}, Net=${metrics['net_exposure']:,.2f}, NGR={metrics['ngr']:.2%}")
    print(f"Basel Netting Factor: {metrics['basel_netting_factor']:.4f}")
    print(f"5y Swap Peak EE (t=2.3): ${ee[23]:,.2f}, PFE95: ${pfe[23]:,.2f}")
    print(f"5y Swap EPE: ${epe:,.2f}, Effective EPE: ${effective_epe:,.2f}")
    print(f"Basel Regulatory EAD (alpha=1.4): ${ead:,.2f}")
    print(f"5y Forward Terminal EE: ${fwd_ee[-1]:,.2f}, PFE95: ${fwd_pfe[-1]:,.2f}")
    print("All counterparty credit risk analytics tests passed successfully!")


if __name__ == "__main__":
    run_ccr_verification()
