"""Mortgages and securitized products: SMM/CPR/PSA, pool cash flows, WAL, IO/PO, dollar roll, CMO waterfall, and OAS.

Backs every number in `06-Fixed-Income-and-Asset-Classes/22-Mortgages-and-Securitized-Products.md`.
- Examples 1 and 2 and cards fi-mbs-securitized-smm-to-cpr and fi-mbs-securitized-psa-benchmark: SMM, CPR and PSA.
- Example 3 and card fi-mbs-securitized-wal-psa: month-1 cash flow and weighted average life at 50, 100 and 300 PSA.
- Example 4 and card fi-mbs-securitized-io-duration: IO and PO values at two speeds.
- Example 5 and card fi-mbs-securitized-dollar-roll: dollar roll implied financing rate.
- Example 6: sequential CMO waterfall.
- Example 7 and cards fi-mbs-securitized-oas-mechanics and fi-mbs-securitized-negative-convexity: Monte Carlo OAS,
  zero-volatility spread, option cost, effective duration and convexity, under a labelled toy prepayment model.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_mortgages.py`.
"""

from __future__ import annotations

import math

import numpy as np

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def smm_to_cpr(smm: float) -> float:
    return 1.0 - (1.0 - smm) ** 12


def cpr_to_smm(cpr: float) -> float:
    return 1.0 - (1.0 - cpr) ** (1.0 / 12.0)


def psa_cpr(age_month: int, psa: float) -> float:
    """PSA benchmark: 0.2% CPR in month 1 rising 0.2% a month to 6% at month 30, flat after; scaled by psa / 100."""
    return min(age_month, 30) * 0.002 * psa / 100.0


def project_pool(balance: float, wac: float, coupon: float, term: int, psa: float) -> list[tuple[float, float, float, float]]:
    """Monthly (interest to investor, scheduled principal, prepayment, beginning balance) for a level-pay pool."""
    rows = []
    rate = wac / 12.0
    for month in range(1, term + 1):
        if balance <= 1e-12:
            break
        remaining = term - month + 1
        payment = balance * rate / (1.0 - (1.0 + rate) ** -remaining)
        sched = payment - balance * rate
        prepay = cpr_to_smm(psa_cpr(month, psa)) * (balance - sched)
        rows.append((balance * coupon / 12.0, sched, prepay, balance))
        balance -= sched + prepay
    return rows


def wal(rows: list[tuple[float, float, float, float]]) -> float:
    principal = [s + p for _, s, p, _ in rows]
    return sum((m + 1) / 12.0 * x for m, x in enumerate(principal)) / sum(principal)


def pv(cash: list[float], annual_yield: float) -> float:
    """Present value of monthly cash flows at a monthly-compounded yield."""
    return sum(c / (1.0 + annual_yield / 12.0) ** (m + 1) for m, c in enumerate(cash))


def example1_2_speeds() -> None:
    print("  1. SMM, CPR and PSA (Examples 1 and 2)")
    cpr = smm_to_cpr(0.005)
    quoted("0.995^12", 0.995**12, 0.941623, 6)
    quoted("CPR from SMM 0.50% (%)", cpr * 100.0, 5.8377, 4)
    quoted("SMM back from that CPR (%)", cpr_to_smm(cpr) * 100.0, 0.5000, 4)
    quoted("CPR at month 10, 100 PSA (%)", psa_cpr(10, 100.0) * 100.0, 2.00, 2)
    quoted("CPR at month 30, 150 PSA (%)", psa_cpr(30, 150.0) * 100.0, 9.00, 2)
    quoted("SMM at 6% CPR (%)", cpr_to_smm(0.06) * 100.0, 0.5143, 4)


def example3_cash_flows() -> None:
    print("  2. Pool cash flows and WAL (Example 3, card fi-mbs-securitized-wal-psa)")
    rows = project_pool(100.0, 0.060, 0.055, 360, 100.0)
    interest, sched, prepay, _ = rows[0]
    quoted("month-1 scheduled payment at 6.0% WAC", 100.0 * 0.005 / (1.0 - 1.005**-360), 0.599551, 6)
    quoted("month-1 interest to investors at 5.5%", interest, 0.458333, 6)
    quoted("month-1 servicing and guarantee fee", 100.0 * (0.060 - 0.055) / 12.0, 0.041667, 6)
    quoted("month-1 scheduled principal", sched, 0.099551, 6)
    quoted("month-1 prepayment at 100 PSA", prepay, 0.016665, 6)
    for psa, e in ((0.0, 19.31), (50.0, 14.53), (100.0, 11.36), (300.0, 5.74)):
        quoted(f"WAL at {psa:.0f} PSA (years)", wal(project_pool(100.0, 0.060, 0.055, 360, psa)), e, 2)


def example4_io_po() -> None:
    print("  3. IO and PO strips (Example 4, card fi-mbs-securitized-io-duration)")
    values = {}
    for psa in (100.0, 300.0):
        rows = project_pool(100.0, 0.060, 0.055, 360, psa)
        values[psa] = (pv([i for i, _, _, _ in rows], 0.055), pv([s + p for _, s, p, _ in rows], 0.055))
    quoted("IO value at 100 PSA", values[100.0][0], 41.80, 2)
    quoted("PO value at 100 PSA", values[100.0][1], 58.20, 2)
    quoted("IO value at 300 PSA", values[300.0][0], 25.08, 2)
    quoted("PO value at 300 PSA", values[300.0][1], 74.92, 2)
    quoted("value moved from IO to PO by 100 to 300 PSA", values[100.0][0] - values[300.0][0], 16.72, 2)
    for psa in (100.0, 300.0):
        assert abs(sum(values[psa]) - 100.0) < 1e-9, "IO + PO at the pass-through rate must equal par"


def example5_dollar_roll() -> None:
    print("  4. Dollar roll (Example 5, card fi-mbs-securitized-dollar-roll)")
    p_front, p_back, carry_given_up, days = 101.50, 101.125, 0.480, 30
    drop = p_front - p_back
    quoted("drop", drop, 0.375, 3)
    quoted("drop in 32nds", drop * 32.0, 12.0, 1)
    implied = (p_back + carry_given_up - p_front) / p_front * 360.0 / days
    quoted("implied financing rate (%)", implied * 100.0, 1.2414, 4)
    quoted("advantage versus 4.50% repo (bp)", (0.045 - implied) * 1e4, 326.0, 0)


def example6_cmo() -> None:
    print("  5. Sequential CMO, month 1 (Example 6)")
    balances, cash = [60_000_000.0, 40_000_000.0], 1_500_000.0
    paid = []
    for b in balances:
        x = min(b, cash)
        paid.append(x)
        cash -= x
    quoted("tranche A principal received ($)", paid[0], 1_500_000.0, 0)
    quoted("tranche B principal received ($)", paid[1], 0.0, 0)
    quoted("tranche A ending balance ($)", balances[0] - paid[0], 58_500_000.0, 0)


# Example 7 inputs: a labelled toy model, not a vendor prepayment model.
F0, SIGMA, MTG_SPREAD = 0.04, 0.008, 0.015
WAC, COUPON, TERM = 0.060, 0.055, 360
TURNOVER, REFI_MAX, REFI_MID, REFI_WIDTH = 0.06, 0.40, 0.010, 0.0025


def toy_cpr(incentive: np.ndarray, age: int) -> np.ndarray:
    ramp = min(age, 30) / 30.0
    return ramp * (TURNOVER + REFI_MAX / (1.0 + np.exp(-(incentive - REFI_MID) / REFI_WIDTH)))


def simulate_pool(f0: float, sigma: float, n_pairs: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cash flows and path discount factors under Ho-Lee fitted to a flat curve f0 (monthly steps, antithetic)."""
    dt = 1.0 / 12.0
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_pairs, TERM))
    z = np.vstack([z, -z])
    n = z.shape[0]
    w = np.zeros(n)
    balance = np.full(n, 100.0)
    log_df = np.zeros(n)
    cash = np.zeros((n, TERM))
    disc = np.zeros((n, TERM))
    rate = WAC / 12.0
    for k in range(TERM):
        t = k * dt
        short = f0 + 0.5 * sigma**2 * t * t + sigma * w
        ten_year = f0 + sigma * w + sigma**2 * (0.5 * t * t + 5.0 * t)  # Ho-Lee 10y zero yield
        incentive = WAC - (ten_year + MTG_SPREAD)
        remaining = TERM - k
        payment = balance * rate / (1.0 - (1.0 + rate) ** -remaining)
        sched = payment - balance * rate
        smm = 1.0 - (1.0 - toy_cpr(incentive, k + 1)) ** (1.0 / 12.0)
        prepay = smm * (balance - sched)
        log_df -= short * dt
        cash[:, k] = balance * COUPON / 12.0 + sched + prepay
        disc[:, k] = np.exp(log_df)
        balance = balance - sched - prepay
        w = w + math.sqrt(dt) * z[:, k]
    times = (np.arange(TERM) + 1.0) / 12.0
    return cash, disc, times


def price_with_spread(cash: np.ndarray, disc: np.ndarray, times: np.ndarray, spread: float) -> float:
    return float((cash * disc * np.exp(-spread * times)).sum(axis=1).mean())


def solve_spread(cash: np.ndarray, disc: np.ndarray, times: np.ndarray, target: float) -> float:
    lo, hi = -0.05, 0.05
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if price_with_spread(cash, disc, times, mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def example7_oas() -> None:
    print("  6. Monte Carlo OAS under a toy prepayment model (Example 7)")
    market_price = 101.00
    cash, disc, times = simulate_pool(F0, SIGMA, 2_000, 2026)
    # The simulated discount factors must reprice the flat curve (Ho-Lee is fitted to it).
    mean_df_10y = float(disc[:, 119].mean())
    quoted("mean path discount factor to 10y", mean_df_10y, 0.670, 3)
    quoted("curve discount factor exp(-0.4)", math.exp(-F0 * 10.0), 0.670, 3)
    oas = solve_spread(cash, disc, times, market_price)
    cash0, disc0, _ = simulate_pool(F0, 0.0, 1, 2026)
    z_spread = solve_spread(cash0[:1], disc0[:1], times, market_price)
    quoted("zero-volatility spread (bp)", z_spread * 1e4, 132.0, 0)
    quoted("OAS (bp), seed-stable", oas * 1e4, 64.0, 0)
    quoted("option cost (bp)", (z_spread - oas) * 1e4, 68.0, 0)
    bump = 0.0025
    p_up = price_with_spread(*simulate_pool(F0 + bump, SIGMA, 2_000, 2026), oas)
    p_dn = price_with_spread(*simulate_pool(F0 - bump, SIGMA, 2_000, 2026), oas)
    eff_dur = (p_dn - p_up) / (2.0 * market_price * bump)
    eff_conv = (p_up + p_dn - 2.0 * market_price) / (market_price * bump * bump)
    quoted("effective duration, seed-stable", eff_dur, 4.2, 1)
    quoted("effective convexity, seed-stable", eff_conv, -122.0, 0)
    assert eff_conv < 0.0, "a premium pass-through should be negatively convex in this model"


def main() -> None:
    print("=== fi_mortgages: Mortgages and Securitized Products ===")
    example1_2_speeds()
    example3_cash_flows()
    example4_io_po()
    example5_dollar_roll()
    example6_cmo()
    example7_oas()
    print(f"\nSuccessfully verified {len(QUOTED)} mortgage figures.")


if __name__ == "__main__":
    main()
