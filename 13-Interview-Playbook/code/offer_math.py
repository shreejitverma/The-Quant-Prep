"""Offer arithmetic in neutral illustrative units: deferral, clawbacks, buyouts and decision rules.

Backs 13-Interview-Playbook/11-Offers-Compensation-and-Negotiation.md.

Every amount here is in abstract units (U) chosen to make the arithmetic visible.
None of them is market data or a claim about what any firm pays; only the mechanics carry over.

Run: uv run --no-project --with numpy python 13-Interview-Playbook/code/offer_math.py
"""

from __future__ import annotations

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".2f") -> None:
    """Print `label = value` and assert it matches the literal the note quotes, to tolerance and to the printed digits."""
    printed, quoted = (s.removeprefix("-") if float(s) == 0 else s for s in (f"{value:{fmt}}", f"{expected:{fmt}}"))
    print(f"{label} = {printed}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    assert printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"


def pv(amounts: list[float], times: list[float], rate: float, stay: float = 1.0) -> float:
    """Present value of vesting tranches; `stay` is the annual probability of still being employed (unvested is forfeited)."""
    return sum(a * stay**t / (1 + rate) ** t for a, t in zip(amounts, times, strict=True))


def section_deferral() -> None:
    print("\n== Deferred award ==")
    # Backs int-offer-deferred-pv and Worked example 1: 90 U vesting in thirds at 1, 2, 3 years, 6% discount.
    tranches, times = [30.0, 30.0, 30.0], [1.0, 2.0, 3.0]
    check("PV of 90 U deferred in thirds over 3 years at 6%", pv(tranches, times, 0.06), 80.19, 0.005)
    check("expected PV if 10% a year leave and forfeit", pv(tranches, times, 0.06, stay=0.9), 65.46, 0.005)
    # Monte Carlo cross-check of the forfeiture-adjusted value (seeded).
    rng = np.random.default_rng(3)
    leave_year = rng.geometric(0.10, size=2_000_000)  # first year in which the holder leaves (1, 2, ...)
    vested = sum(30.0 / 1.06**t * (leave_year > t) for t in (1, 2, 3))
    check("simulated expected PV (seed 3)", float(vested.mean()), 65.5, 0.1, ".1f")


def section_sign_on() -> None:
    print("\n== Sign-on clawback ==")
    # Backs int-offer-sign-on-clawback and Worked example 2.
    sign_on, months, left = 30.0, 24, 9
    check("months left on the clawback", months - left, 15, 0, ".0f")
    check("pro-rata repayment after 9 of 24 months", sign_on * (months - left) / months, 18.75, 1e-12)
    check("cliff repayment (all if before 12 months)", sign_on if left < 12 else 0.0, 30.00, 0.0)


def section_buyout() -> None:
    print("\n== Buyout of forfeited deferred pay ==")
    # Backs int-offer-buyout-pv and Worked example 3: old award 40 U at 0.5y and 40 U at 1.5y.
    old = pv([40.0, 40.0], [0.5, 1.5], 0.06)
    check("PV of forfeited tranches at 6%", old, 75.50, 0.005)
    check("time-value discount of the forfeited tranches vs face", 80.0 - old, 4.50, 0.005)
    replacement = pv([40.0, 40.0], [1.0, 2.0], 0.06)
    check("PV of a replacement award that vests a year later per tranche", replacement, 73.34, 0.005)
    check("shortfall of the delayed replacement vs forfeited award", old - replacement, 2.17, 0.005)


def section_bonus_choice() -> None:
    print("\n== Guaranteed vs discretionary ==")
    # Backs int-offer-guarantee-vs-discretionary and Worked example 4.
    outcomes, probs = np.array([0.0, 60.0, 100.0]), np.array([0.2, 0.5, 0.3])
    mean = float(outcomes @ probs)
    sd = float(np.sqrt(((outcomes - mean) ** 2) @ probs))
    check("expected discretionary bonus (U)", mean, 60.00, 1e-12)
    check("its standard deviation (U)", sd, 34.64, 0.005)
    check("probability it pays less than a 50 U guarantee", float(probs[outcomes < 50].sum()), 0.20, 1e-12)


def section_exploding_offer() -> None:
    print("\n== Exploding offer ==")
    # Backs int-offer-exploding-deadline and Worked example 5.
    accept_now, p_b, fallback = 100.0, 0.5, 70.0
    b_low, b_high = 80.0, 140.0  # if offer B arrives its value is uniform on [80, 140]
    wait = p_b * (b_low + b_high) / 2 + (1 - p_b) * fallback
    check("mean value of offer B if it arrives", (b_low + b_high) / 2, 110.00, 1e-12)
    check("expected value of letting offer A lapse to wait for B", wait, 90.00, 1e-12)
    # With an extension, you keep A while B resolves: take max(A, B) if B comes, else A.
    grid = np.linspace(b_low, b_high, 600_001)
    with_ext = p_b * float(np.maximum(grid, accept_now).mean()) + (1 - p_b) * accept_now
    closed = p_b * ((b_high**2 - accept_now**2) / 2 + accept_now * (accept_now - b_low)) / (b_high - b_low) + (1 - p_b) * accept_now
    check("expected value with an extension (grid)", with_ext, 106.67, 0.005)
    check("expected value with an extension (closed form)", closed, 106.67, 0.005)
    check("value of the extension over accepting immediately", closed - accept_now, 6.67, 0.005)


if __name__ == "__main__":
    section_deferral()
    section_sign_on()
    section_buyout()
    section_bonus_choice()
    section_exploding_offer()
    print("\nAll checks passed.")
