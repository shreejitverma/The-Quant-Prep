"""Repo mechanics, carry of repo-financed bonds, specials and fails, and compounded overnight rates.

Backs every number in `06-Fixed-Income-and-Asset-Classes/12-Money-Markets-Repo-and-Overnight-Rates.md`.
Cross-checks: repo carry is computed twice (coupon accrual minus financing, and the repo-implied forward
price minus spot), the fallback period's weights must sum to its calendar days, and the margin-ratio
cushion is checked as a share of cash rather than of collateral.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_money_markets.py`.
"""

from __future__ import annotations

import datetime as dt

QUOTED: list[str] = []
ONE_DAY = dt.timedelta(days=1)


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def compounded_rate(rates: list[float], weights: list[int], basis: float) -> float:
    """[prod(1 + r_i n_i / B) - 1] * B / sum(n_i)."""
    growth = 1.0
    for r, n in zip(rates, weights, strict=True):
        growth *= 1.0 + r * n / basis
    return (growth - 1.0) * basis / sum(weights)


def example_repo() -> None:
    print("  1. Repo: haircut, interest, repayment, margin ratio")
    collateral, haircut, rate, days = 100_000_000.0, 0.02, 0.0530, 7
    cash = collateral * (1.0 - haircut)
    interest = cash * rate * days / 360.0
    quoted("cash lent with 2% haircut (USD)", cash, 98_000_000.0, 0)
    quoted("repo interest 7 days ACT/360 (USD)", interest, 100_994.44, 2)
    quoted("repurchase price (USD)", cash + interest, 98_100_994.44, 2)
    quoted("collateral cushion (USD)", collateral - cash, 2_000_000.0, 0)
    # Initial margin quoted as a ratio: collateral = (1 + m) * cash.
    cash_m = collateral / 1.02
    quoted("cash lent with 102% initial margin (USD)", cash_m, 98_039_215.69, 2)
    quoted("cushion with 102% initial margin (USD)", collateral - cash_m, 1_960_784.31, 2)
    assert abs((collateral - cash_m) / cash_m - 0.02) < 1e-12  # the margin is 2% of cash, not of collateral
    quoted("maximum leverage at a 2% haircut (x)", 1.0 / haircut, 50.0, 0)


def example_compounding() -> None:
    print("  2. Compounded in arrears vs day-weighted average (one week)")
    rates = [0.050, 0.050, 0.050, 0.051, 0.051]
    weights = [1, 1, 1, 1, 3]
    simple = sum(r * n for r, n in zip(rates, weights, strict=True)) / sum(weights)
    comp = compounded_rate(rates, weights, 360.0)
    quoted("day-weighted average (%)", simple * 100.0, 5.0571, 4)
    quoted("growth factor", 1.0 + comp * 7.0 / 360.0, 1.000983688, 9)
    quoted("compounded rate (%)", comp * 100.0, 5.0590, 4)
    quoted("compounded minus average (bp)", (comp - simple) * 1e4, 0.18, 2)
    flat = compounded_rate([0.05] * 5, weights, 360.0)
    quoted("constant 5% week: compounded minus 5% (bp)", (flat - 0.05) * 1e4, 0.18, 2)
    # Second-order expansion of the product: r^2 [(sum n)^2 - sum n^2] / (2 B sum n).
    n_sum, n_sq = sum(weights), sum(n * n for n in weights)
    approx = 0.05**2 * (n_sum**2 - n_sq) / (2.0 * 360.0 * n_sum)
    quoted("second-order approximation of that gap (bp)", approx * 1e4, 0.18, 2)
    assert abs(approx - (flat - 0.05)) < 1e-8
    sonia_basis = compounded_rate(rates, weights, 365.0)
    quoted("same fixings on a 365 basis (SONIA style) (%)", sonia_basis * 100.0, 5.0589, 4)


def example_carry() -> None:
    print("  3. Carry on a repo-financed Treasury (ACT/ACT coupon, ACT/360 repo)")
    coupon, repo, clean = 0.04, 0.05, 100.0
    last_cpn, next_cpn = dt.date(2026, 2, 15), dt.date(2026, 8, 15)
    buy, sell = dt.date(2026, 3, 1), dt.date(2026, 3, 31)
    half = (next_cpn - last_cpn).days
    ai_buy = 100.0 * coupon / 2.0 * (buy - last_cpn).days / half
    ai_sell = 100.0 * coupon / 2.0 * (sell - last_cpn).days / half
    d = (sell - buy).days
    dirty = clean + ai_buy
    accrual = ai_sell - ai_buy
    financing = dirty * repo * d / 360.0
    carry = accrual - financing
    quoted("half-year days", float(half), 181.0, 0)
    quoted("accrued interest at purchase", ai_buy, 0.154696, 6)
    quoted("accrued interest at sale", ai_sell, 0.486188, 6)
    quoted("coupon accrual over 30 days", accrual, 0.331492, 6)
    quoted("repo financing on the dirty price", financing, 0.417311, 6)
    quoted("carry per 100", carry, -0.085820, 6)
    # Independent route: the repo-implied forward clean price.
    fwd_clean = dirty * (1.0 + repo * d / 360.0) - ai_sell
    quoted("forward clean price (break-even)", fwd_clean, 100.085820, 6)
    assert abs((fwd_clean - clean) + carry) < 1e-12
    quoted("carry on 100mm face (USD)", carry * 1e6, -85_820.0, 0)


def example_specials_and_fails() -> None:
    print("  4. Specialness and the fails charge")
    gc, special, notional = 0.0530, 0.0380, 100_000_000.0
    quoted("specialness (bp)", (gc - special) * 1e4, 150.0, 0)
    quoted("30-day financing saving (USD)", notional * (gc - special) * 30.0 / 360.0, 125_000.0, 0)

    def fails_charge(proceeds: float, ref_rate_pct: float, floor_pct: float) -> float:
        return proceeds * 0.01 * max(3.0 - ref_rate_pct, floor_pct) / 360.0

    quoted("one-day fail, reference rate 0%, floor 0 (USD)", fails_charge(notional, 0.0, 0.0), 8_333.33, 2)
    quoted("one-day fail, reference rate 4%, floor 0 (USD)", fails_charge(notional, 4.0, 0.0), 0.0, 2)
    quoted("one-day fail, reference rate 4%, floor 1 (USD)", fails_charge(notional, 4.0, 1.0), 2_777.78, 2)


def example_fallback() -> None:
    print("  5. A 3M USD LIBOR fallback: compounded SOFR plus the fixed spread")
    holidays = {dt.date(2026, 7, 3), dt.date(2026, 9, 7)}

    def is_bd(d: dt.date) -> bool:
        return d.weekday() < 5 and d not in holidays

    start, end = dt.date(2026, 7, 1), dt.date(2026, 10, 1)
    weights = []
    d = start
    while d < end:
        if is_bd(d):
            nxt = d + ONE_DAY
            while not is_bd(nxt):
                nxt += ONE_DAY
            weights.append((min(nxt, end) - d).days)
        d += ONE_DAY
    assert sum(weights) == (end - start).days
    quoted("calendar days", float(sum(weights)), 92.0, 0)
    quoted("business-day fixings", float(len(weights)), 64.0, 0)
    comp = compounded_rate([0.0430] * len(weights), weights, 360.0)
    quoted("compounded SOFR at a flat 4.30% (%)", comp * 100.0, 4.32320, 5)
    spread = 0.0026161
    quoted("fallback rate (%)", (comp + spread) * 100.0, 4.58481, 5)


def main() -> None:
    print("=== fi_money_markets: repo, carry, specials, compounded RFRs ===")
    example_repo()
    example_compounding()
    example_carry()
    example_specials_and_fails()
    example_fallback()
    print(f"\nVerified {len(QUOTED)} money market and repo figures.")


if __name__ == "__main__":
    main()
