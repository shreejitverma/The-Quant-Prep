"""Execution algorithm schedules (TWAP, VWAP, POV) and transaction cost analysis (Perold implementation shortfall).

Backs every number in 08-Execution-Algorithms-and-TCA.md.
Run ``python execution_algos.py``: each result is printed and asserted.
The intraday volume profile and prices are hypothetical illustrations.
"""

from __future__ import annotations

import math

import numpy as np

# Share of daily volume in each of the 13 half-hour buckets from 09:30 to 16:00 (sums to 100%): a U shape
PROFILE = np.array([12.0, 9.0, 7.0, 6.0, 6.0, 5.0, 5.0, 5.0, 6.0, 7.0, 8.0, 10.0, 14.0]) / 100.0


def check(label: str, value: float, expected: float, tol: float = 1e-9) -> float:
    """Print a labelled result and assert it is within tol of the expected value."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


def twap_schedule(quantity: float, buckets: int) -> np.ndarray:
    """Equal slices per time bucket."""
    return np.full(buckets, quantity / buckets)


def vwap_schedule(quantity: float, profile: np.ndarray) -> np.ndarray:
    """Slices proportional to the expected volume profile."""
    return quantity * profile / profile.sum()


def pov_fills(quantity: float, others_volume: np.ndarray, rate: float) -> np.ndarray:
    """Participation of `rate` in total volume (others plus us): child = rate / (1 - rate) * others, capped at what is left."""
    fills = np.zeros_like(others_volume)
    left = quantity
    for i, vol in enumerate(others_volume):
        take = min(left, rate / (1 - rate) * vol)
        fills[i] = take
        left -= take
    return fills


def schedules() -> None:
    print("== Schedules for 100,000 shares over 13 half-hour buckets ==")
    assert abs(PROFILE.sum() - 1.0) < 1e-12
    twap = twap_schedule(100_000, 13)
    vwap = vwap_schedule(100_000, PROFILE)
    check("TWAP slice", float(twap[0]), 7_692.3077, 5e-5)
    check("VWAP first bucket", float(vwap[0]), 12_000.0, 1e-6)
    check("VWAP lunchtime bucket", float(vwap[6]), 5_000.0, 1e-6)
    check("VWAP last bucket", float(vwap[-1]), 14_000.0, 1e-6)
    # Tracking: the share of the order done after the first hour
    check("TWAP done after 1 hour (%)", float(twap[:2].sum() / 1_000), 15.3846, 5e-5)
    check("VWAP done after 1 hour (%)", float(vwap[:2].sum() / 1_000), 21.0, 1e-9)

    print("== POV at 10% of a 2,000,000-share day, order 150,000 ==")
    others = 2_000_000 * PROFILE * 0.9  # everyone else's realised volume
    fills = pov_fills(150_000, others, 0.10)
    done = np.cumsum(fills)
    finish = int(np.argmax(done >= 150_000 - 1e-6))
    check("others' volume in first bucket", float(others[0]), 216_000.0, 1e-6)
    check("child in first bucket", float(fills[0]), 24_000.0, 1e-6)
    check("cumulative fills after ten buckets", float(done[9]), 136_000.0, 1e-6)
    check("POV 20% child against 400,000 shares of others", float(pov_fills(1e9, np.array([400_000.0]), 0.20)[0]), 100_000.0, 1e-6)
    check("participation in first bucket", float(fills[0] / (fills[0] + others[0])), 0.10, 1e-12)
    check("20% of total volume as a share of others' volume", 0.20 / 0.80, 0.25, 1e-12)
    check("bucket index where the order completes (0-based)", finish, 10, 0)
    check("shares filled in the completing bucket", float(fills[finish]), 14_000.0, 1e-6)
    # Completion time is driven by realised volume: a quiet day at 60% of normal volume
    fills_q = pov_fills(150_000, others * 0.6, 0.10)
    check("filled by the close on a 60% volume day", float(fills_q.sum()), 120_000.0, 1e-6)


def implementation_shortfall() -> None:
    print("== Perold implementation shortfall ==")
    q_target, p_decision, p_arrival = 100_000, 50.00, 50.10
    fills = [(20_000, 50.20), (30_000, 50.30), (30_000, 50.50)]
    q_exec = sum(q for q, _ in fills)
    avg = sum(q * p for q, p in fills) / q_exec
    p_close, fee = 50.60, 0.005
    check("executed shares", q_exec, 80_000, 0)
    check("average fill price", avg, 50.35, 1e-12)
    paper_notional = q_target * p_decision
    delay = q_exec * (p_arrival - p_decision)
    execution = sum(q * (p - p_arrival) for q, p in fills)
    opportunity = (q_target - q_exec) * (p_close - p_decision)
    fees = fee * q_exec
    total = delay + execution + opportunity + fees
    check("delay cost ($)", delay, 8_000.0, 1e-6)
    check("execution cost ($)", execution, 20_000.0, 1e-6)
    check("opportunity cost ($)", opportunity, 12_000.0, 1e-6)
    check("fees ($)", fees, 400.0, 1e-9)
    check("implementation shortfall ($)", total, 40_400.0, 1e-6)
    check("implementation shortfall (bp of paper notional)", total / paper_notional * 1e4, 80.8, 1e-9)
    for label, comp, bp in (
        ("delay", delay, 16.0),
        ("execution", execution, 40.0),
        ("opportunity", opportunity, 24.0),
        ("fees", fees, 0.8),
    ):
        check(f"{label} (bp of paper notional)", comp / paper_notional * 1e4, bp, 1e-9)
    paper_pnl = q_target * (p_close - p_decision)
    real_pnl = q_exec * (p_close - avg) - fees
    check("paper portfolio P&L ($)", paper_pnl, 60_000.0, 1e-6)
    check("real portfolio P&L ($)", real_pnl, 19_600.0, 1e-6)
    check("paper minus real equals shortfall", paper_pnl - real_pnl, total, 1e-6)
    check("arrival slippage of executed shares (bp)", (avg - p_arrival) / p_arrival * 1e4, 49.9002, 5e-5)

    print("== VWAP benchmark and participation ==")
    vwap_interval = 50.30
    check("slippage vs interval VWAP ($/share)", avg - vwap_interval, 0.05, 1e-12)
    check("slippage vs interval VWAP (bp)", (avg - vwap_interval) / vwap_interval * 1e4, 9.9404, 5e-5)
    w = 0.30  # our share of interval volume
    others_vwap = (vwap_interval - w * avg) / (1 - w)
    check("VWAP of everyone else", others_vwap, 50.278571, 5e-7)
    check("our price minus others' VWAP", avg - others_vwap, 0.071429, 5e-7)
    check("measured slippage = (1 - w) x true slippage", (1 - w) * (avg - others_vwap), avg - vwap_interval, 1e-12)

    print("== Post-trade reversion ==")
    p_end, p_later = 50.55, 50.40
    check("move from arrival to end of execution ($)", p_end - p_arrival, 0.45, 1e-12)
    check("reversion over the next 30 minutes ($)", p_end - p_later, 0.15, 1e-12)
    check("share of the move that reverted", (p_end - p_later) / (p_end - p_arrival), 1 / 3, 1e-12)


def tca_noise() -> None:
    print("== How noisy is measured slippage? ==")
    sigma_daily, horizon_days = 0.02, 0.5
    # Average of a Brownian path over a uniform schedule: sd = sigma sqrt(T/3)
    sd_bp = sigma_daily * math.sqrt(horizon_days / 3) * 1e4
    check("sd of arrival slippage, uniform half-day schedule (bp)", sd_bp, 81.65, 0.005)
    n = (1.96 * sd_bp / 5.0) ** 2
    check("orders to detect a 5 bp mean at 1.96 standard errors", n, 1_024.4, 0.05)
    # Comparing two algorithms (two-sample test, 5% two-sided, 80% power): n per arm = 2 ((z_a + z_b) sd / diff)^2
    z_alpha, z_power = 1.959964, 0.841621
    n_arm = 2 * ((z_alpha + z_power) * sd_bp / 5.0) ** 2
    check("orders per algorithm to compare two algorithms at 80% power", n_arm, 4_186.0, 0.5)
    rng = np.random.default_rng(8)
    steps, paths = 1_000, 20_000
    w = np.cumsum(rng.standard_normal((paths, steps)) * math.sqrt(horizon_days / steps), axis=1)
    check("simulated sd of the path average (bp)", float(w.mean(axis=1).std() * sigma_daily * 1e4), 81.85, 0.005)


if __name__ == "__main__":
    schedules()
    implementation_shortfall()
    tca_noise()
    print("all execution and TCA checks passed")
