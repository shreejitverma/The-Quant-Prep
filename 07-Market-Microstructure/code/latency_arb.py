"""Latency arbitrage: the Budish-Cramton-Shim zero-profit spread, stale-quote races, batching and speed bumps.

Backs every number in 10-Latency-Arbitrage-and-Speed.md.
Run ``python latency_arb.py``: each result is printed and asserted.
All market parameters are hypothetical illustrations, not estimates for any instrument.
"""

from __future__ import annotations

import math


def check(label: str, value: float, expected: float, tol: float = 1e-9) -> float:
    """Print a labelled result and assert it is within tol of the expected value."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


def sniping_cost_rate(half_spread: float, lam_jump: float, mean_jump: float) -> float:
    """lam_jump * P(J > h) * E[J - h | J > h] for exponential jumps with mean mean_jump: lam_jump * mean_jump * exp(-h / mean_jump)."""
    return lam_jump * mean_jump * math.exp(-half_spread / mean_jump)


def bcs_half_spread(lam_fund: float, lam_jump: float, mean_jump: float, exposure: float = 1.0) -> float:
    """Solve lam_fund * h = exposure * sniping_cost_rate(h) by bisection (unique root: LHS rises, RHS falls)."""
    lo, hi = 0.0, 50 * mean_jump
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if lam_fund * mid < exposure * sniping_cost_rate(mid, lam_jump, mean_jump):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def bcs_equilibrium() -> None:
    print("== Budish-Cramton-Shim zero-profit spread, exponential jumps ==")
    lam_fund, lam_jump, mean_jump, c_speed = 1.0, 0.5, 0.01, 0.0005
    h = bcs_half_spread(lam_fund, lam_jump, mean_jump)
    check("half-spread h ($)", h, 0.0035173, 5e-8)
    check("spread s = 2h ($)", 2 * h, 0.0070347, 5e-8)
    check("h / mean jump (Lambert W(0.5))", h / mean_jump, 0.351734, 5e-7)
    check("revenue from fundamental traders per second", lam_fund * h, sniping_cost_rate(h, lam_jump, mean_jump), 1e-12)
    n_firms = lam_fund * h / c_speed
    check("entry N = lam_fund h / c_speed", n_firms, 7.0347, 5e-5)
    check("total speed spend N c_speed per second", n_firms * c_speed, lam_fund * h, 1e-12)
    h2 = bcs_half_spread(lam_fund, 1.0, mean_jump)
    check("spread with twice as many jumps", 2 * h2, 0.0113429, 5e-8)
    h3 = bcs_half_spread(2.0, lam_jump, mean_jump)
    check("spread with twice as many fundamental traders", 2 * h3, 0.0040778, 5e-8)
    # Stylised batching: only jumps in the last delta of a batch interval tau can be sniped
    for ratio, spread, tol in ((0.1, 0.00095345, 5e-9), (0.001, 0.000009995, 5e-10)):
        h_b = bcs_half_spread(lam_fund, lam_jump, mean_jump, exposure=ratio)
        check(f"spread when sniping exposure is scaled by delta/tau = {ratio}", 2 * h_b, spread, tol)


def stale_quote_race() -> None:
    print("== One stale-quote race ==")
    ask, size, new_fair = 450.01, 1_000, 450.035
    profit = (new_fair - ask) * size
    check("sniper profit if it wins ($)", profit, 25.0, 1e-6)
    n = 5  # the maker plus four snipers react to the same signal
    check("maker's probability of losing the race", (n - 1) / n, 0.8)
    check("maker's expected loss per event ($)", profit * (n - 1) / n, 20.0, 1e-6)
    check("expected daily loss at 1,000 such events ($)", 1_000 * profit * (n - 1) / n, 20_000.0, 1e-3)
    check("each sniper's expected gain per event ($)", profit / n, 5.0, 1e-6)

    print("== Speed bump on takers only (asymmetric) ==")
    maker_cancel_us, sniper_take_us, bump_us = 50.0, 10.0, 350.0
    assert sniper_take_us < maker_cancel_us  # without the bump the sniper arrives first
    assert maker_cancel_us < sniper_take_us + bump_us  # with the bump the cancel arrives first
    check("maker's margin with the bump (microseconds)", sniper_take_us + bump_us - maker_cancel_us, 310.0)
    check("sniper arrival with the bump (microseconds)", sniper_take_us + bump_us, 360.0)

    print("== Propagation delay ==")
    c_km_per_ms = 299.792458
    check("vacuum one-way time for 1,000 km (ms)", 1_000 / c_km_per_ms, 3.33564, 5e-6)
    check("fibre one-way time for 1,000 km, index 1.47 (ms)", 1.47 * 1_000 / c_km_per_ms, 4.90339, 5e-6)
    check("round-trip saving reported for Spread Networks: 16 ms to 13 ms", 16 - 13, 3.0)


if __name__ == "__main__":
    bcs_equilibrium()
    stale_quote_race()
    print("all latency checks passed")
