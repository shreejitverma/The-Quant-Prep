"""SOFR compounding, OIS swap pricing, curve bootstrapping on real dates, and swap risk.

Backs every number in note 03 (Swaps and Curve Building).
Conventions used, with sources quoted in the note:
- SOFR accrues ACT/360 and compounds on business days, with simple interest at the prior business day's rate over
  non-business days (Federal Reserve Bank of New York, SOFR Averages and Index methodology, retrieved 2026-10-17).
- USD SOFR OIS: annual payments on both legs, ACT/360, spot start T+2, 2-day payment lag
  (CFTC press release 8745-23, 7 July 2023).
All rates and quotes below are hypothetical inputs, labelled as such in the note.
Each `q(...)` asserts a computed value against the literal quoted in the note and prints it.
Run with `python 06-Fixed-Income-and-Asset-Classes/code/fi_swaps_ois.py`.
"""

from __future__ import annotations

import calendar
import math
from datetime import date, timedelta


def q(tag: str, label: str, value: float, text: str) -> None:
    """Assert that `value` rounds to the quoted `text` (half a unit of its last decimal) and print it."""
    decimals = len(text.split(".")[1]) if "." in text else 0
    literal = float(text.replace(",", ""))
    assert abs(value - literal) <= 0.5 * 10.0**-decimals + 1e-12, f"[{tag}] {label}: computed {value!r}, note quotes {text}"
    print(f"  [{tag}] {label} = {text}")


# ------------------------------------------------------------ calendar helpers (weekends only; no holiday falls on these dates)


def is_business_day(d: date) -> bool:
    return d.weekday() < 5


def add_business_days(d: date, n: int) -> date:
    out = d
    while n > 0:
        out += timedelta(days=1)
        if is_business_day(out):
            n -= 1
    return out


def modified_following(d: date) -> date:
    out = d
    while not is_business_day(out):
        out += timedelta(days=1)
    if out.month != d.month:
        out = d
        while not is_business_day(out):
            out -= timedelta(days=1)
    return out


def add_years(d: date, years: int) -> date:
    y = d.year + years
    return date(y, d.month, min(d.day, calendar.monthrange(y, d.month)[1]))


# ------------------------------------------------------------ SOFR compounding


def compounded_rate(fixings: list[tuple[date, float]], end: date) -> float:
    """NY Fed style compounded average: prod(1 + r_i n_i / 360) - 1, times 360 / calendar days.

    `fixings` lists (business day, SOFR) in order; n_i counts calendar days until the next business day (or `end`).
    """
    growth = 1.0
    for k, (d, r) in enumerate(fixings):
        nxt = fixings[k + 1][0] if k + 1 < len(fixings) else end
        growth *= 1.0 + r * (nxt - d).days / 360.0
    total_days = (end - fixings[0][0]).days
    return (growth - 1.0) * 360.0 / total_days


# ------------------------------------------------------------ OIS curve on real dates


def ois_schedule(spot: date, years: int) -> list[date]:
    """Annual unadjusted anniversaries of spot, adjusted modified following."""
    return [modified_following(add_years(spot, k)) for k in range(1, years + 1)]


def bootstrap_ois(spot: date, quotes: list[float]) -> tuple[list[date], list[float], list[float]]:
    """Discount factors P(spot, T_n) from annual ACT/360 par OIS quotes (no payment lag in the bootstrap).

    Par condition per unit notional: S_n sum_i tau_i P_i = 1 - P_n (floating leg telescopes on one curve),
    so P_n = (1 - S_n sum_{i<n} tau_i P_i) / (1 + S_n tau_n).
    Returns (dates, accruals, discount factors).
    """
    dates = ois_schedule(spot, len(quotes))
    starts = [spot, *dates[:-1]]
    taus = [(e - s).days / 360.0 for s, e in zip(starts, dates, strict=True)]
    dfs: list[float] = []
    for n, s_n in enumerate(quotes):
        annuity_prev = sum(t * p for t, p in zip(taus[:n], dfs, strict=True))
        dfs.append((1.0 - s_n * annuity_prev) / (1.0 + s_n * taus[n]))
    return dates, taus, dfs


def annuity(taus: list[float], dfs: list[float], n: int) -> float:
    return sum(t * p for t, p in zip(taus[:n], dfs[:n], strict=True))


def par_rate(taus: list[float], dfs: list[float], n: int) -> float:
    return (1.0 - dfs[n - 1]) / annuity(taus, dfs, n)


def receiver_pv(quotes: list[float], spot: date, fixed: float, n: int, notional: float) -> float:
    """PV at spot of a receive-fixed OIS swap of n years on the curve bootstrapped from `quotes`."""
    _, taus, dfs = bootstrap_ois(spot, quotes)
    return notional * (fixed - par_rate(taus, dfs, n)) * annuity(taus, dfs, n)


# ------------------------------------------------------------ annual single-curve bootstrap (whole years)


def bootstrap_annual(par: list[float]) -> list[float]:
    dfs: list[float] = []
    for c in par:
        dfs.append((1.0 - c * sum(dfs)) / (1.0 + c))
    return dfs


def main() -> None:
    print("Note 03: Swaps and Curve Building")

    # --- 1. SOFR compounding over one week with a weekend (Example 1, card fi-sw-sofr-compounding)
    mon = date(2026, 10, 19)
    week = [(mon + timedelta(days=k), r) for k, r in enumerate([0.0430, 0.0431, 0.0429, 0.0432, 0.0433])]
    end = date(2026, 10, 26)
    comp = compounded_rate(week, end)
    q("ex1", "compounded SOFR, Mon 19 to Mon 26 Oct, %", 100 * comp, "4.31704")
    weights = [1, 1, 1, 1, 3]
    simple_avg = sum(r * w for (_, r), w in zip(week, weights, strict=True)) / 7
    q("ex1", "day-weighted simple average, %", 100 * simple_avg, "4.31571")
    q("fi-sw-sofr-compounding", "compounding minus simple average, bp", 1e4 * (comp - simple_avg), "0.13")
    naive = (math.prod(1 + r / 360 for _, r in week) - 1) * 360 / 5
    q("fi-sw-sofr-compounding", "error from ignoring the weekend weight (5 one-day accruals), bp", 1e4 * (naive - comp), "-0.60")
    q("ex1", "interest on 100mm for the week, USD", 1e8 * comp * 7 / 360, "83,942.51")
    # SOFR Index route: chain an index, round to 8 decimals as published, and recover the average
    index = [1.0]
    for k, (d, r) in enumerate(week):
        nxt = week[k + 1][0] if k + 1 < len(week) else end
        index.append(index[-1] * (1 + r * (nxt - d).days / 360))
    from_index = (index[-1] / index[0] - 1) * 360 / 7
    assert abs(from_index - comp) < 1e-15
    start_idx = 1.12345678  # a hypothetical published index level
    rounded = (round(start_idx * index[-1], 8) / start_idx - 1) * 360 / 7
    q("fi-sw-sofr-index", "average from 8-decimal index values, %", 100 * rounded, "4.31705")
    assert abs(rounded - comp) < 5e-9 * 360 / 7 / start_idx + 1e-15

    # --- 2. Real-date OIS bootstrap (Example 2, cards fi-sw-ois-conventions, fi-bootstrap-triangular)
    trade = date(2026, 10, 19)
    spot = add_business_days(trade, 2)
    assert spot == date(2026, 10, 21)
    quotes = [0.0360, 0.0345, 0.0340, 0.0342, 0.0348]
    dates, taus, dfs = bootstrap_ois(spot, quotes)
    assert dates == [date(2027, 10, 21), date(2028, 10, 23), date(2029, 10, 22), date(2030, 10, 21), date(2031, 10, 21)]
    q("ex2", "accrual 2027-10-21 to 2028-10-23 (ACT/360)", taus[1], "1.022222")
    q("ex2", "accrual 2028-10-23 to 2029-10-22 (ACT/360)", taus[2], "1.011111")
    q("ex2", "accrual 2029-10-22 to 2030-10-21 (ACT/360)", taus[3], "1.011111")
    q("ex2", "accrual 2030-10-21 to 2031-10-21 (ACT/360)", taus[4], "1.013889")
    q("ex2", "accrual first year 2026-10-21 to 2027-10-21", taus[0], "1.013889")
    expected_dfs = ["0.964785", "0.933337", "0.903251", "0.872511", "0.840614"]
    for k, (p, txt) in enumerate(zip(dfs, expected_dfs, strict=True)):
        q("ex2", f"P(spot, {dates[k]})", p, txt)
    for n in range(1, 6):
        assert abs(par_rate(taus, dfs, n) - quotes[n - 1]) < 1e-14  # every quote reprices exactly
    t_365 = [(d - spot).days / 365.0 for d in dates]
    zeros = [-math.log(p) / t for p, t in zip(dfs, t_365, strict=True)]
    for k, txt in enumerate(["3.5850", "3.4353", "3.3856", "3.4072", "3.4705"]):
        q("ex2", f"continuous zero ACT/365F to {dates[k]}, %", 100 * zeros[k], txt)
    fwds = [(dfs[k - 1] / dfs[k] - 1) / taus[k] for k in range(1, 5)]
    for k, txt in enumerate(["3.2962", "3.2942", "3.4845", "3.7424"], start=1):
        q("ex2", f"1y forward ACT/360 starting {dates[k - 1]}, %", 100 * fwds[k - 1], txt)
    # spot-date discount factors to trade date: two days at an overnight rate near the 1y level
    p_on = 1 / (1 + 0.0430 * 2 / 360)
    q("ex2", "P(trade, spot) at 4.30% overnight", p_on, "0.999761")

    # --- 3. Payment lag: the floating leg no longer telescopes exactly (card fi-sw-payment-lag)
    def df_at(d: date) -> float:
        """Log-linear in time between bootstrapped pillars (flat forward), spot = 1."""
        pts = [(spot, 1.0), *zip(dates, dfs, strict=True)]
        segments = list(zip(pts[:-1], pts[1:], strict=True))
        for k, ((d1, p1), (d2, p2)) in enumerate(segments):
            if d1 <= d <= d2 or (k == len(segments) - 1 and d > d2):  # flat-forward extrapolation of the last segment
                w = (d - d1).days / (d2 - d1).days
                return math.exp((1 - w) * math.log(p1) + w * math.log(p2))
        raise ValueError(d)

    for d, p_k in zip(dates, dfs, strict=True):
        assert abs(df_at(d) - p_k) < 1e-15

    pay = [add_business_days(d, 2) for d in dates]
    starts = [spot, *dates[:-1]]
    float_lag = sum(df_at(pd) * (df_at(s) / df_at(e) - 1) for s, e, pd in zip(starts, dates, pay, strict=True))
    ann_lag = sum(t * df_at(pd) for t, pd in zip(taus, pay, strict=True))
    s_lag = float_lag / ann_lag
    q("fi-sw-payment-lag", "5y par rate with 2-day payment lag on both legs, %", 100 * s_lag, "3.4800")
    q("fi-sw-payment-lag", "difference from the no-lag par rate, bp", 1e4 * (s_lag - quotes[4]), "-0.0005")

    # --- 4. Off-market swap: value, annuity DV01, bump-and-rebootstrap DV01, bucket deltas (Example 3)
    notional, fixed = 100_000_000.0, 0.0375
    a5 = annuity(taus, dfs, 5)
    q("ex3", "5y annuity per unit notional", a5, "4.580045")
    pv = receiver_pv(quotes, spot, fixed, 5, notional)
    q("ex3", "PV of 5y receiver at 3.75% on 100mm, USD", pv, "1,236,612")
    q("ex3", "annuity DV01, USD per bp", notional * a5 * 1e-4, "45,800")
    up = receiver_pv([s + 1e-4 for s in quotes], spot, fixed, 5, notional)
    dn = receiver_pv([s - 1e-4 for s in quotes], spot, fixed, 5, notional)
    q("fi-sw-dv01-definitions", "parallel par-bump DV01 (central), USD per bp", (dn - up) / 2, "46,156")
    buckets = []
    for k in range(5):
        bu = [s + (1e-4 if j == k else 0.0) for j, s in enumerate(quotes)]
        bd = [s - (1e-4 if j == k else 0.0) for j, s in enumerate(quotes)]
        buckets.append((receiver_pv(bd, spot, fixed, 5, notional) - receiver_pv(bu, spot, fixed, 5, notional)) / 2)
    for k, txt in enumerate(["23", "46", "70", "95", "45,922"]):
        q("fi-sw-bucket-deltas", f"{k + 1}y par-point delta, USD per bp", buckets[k], txt)
    q("fi-sw-bucket-deltas", "sum of bucket deltas, USD per bp", sum(buckets), "46,156")
    # control: the same swap struck at par has no 1y-4y delta, so the short buckets come from the off-market coupon
    for k in range(4):
        bu = [s + (1e-4 if j == k else 0.0) for j, s in enumerate(quotes)]
        assert abs(receiver_pv(bu, spot, quotes[4], 5, notional)) < 1e-6
    q(
        "fi-sw-dv01-definitions",
        "par 5y receiver: rebuild DV01 equals annuity DV01, USD per bp",
        (
            receiver_pv([s - 1e-4 for s in quotes], spot, quotes[4], 5, notional)
            - receiver_pv([s + 1e-4 for s in quotes], spot, quotes[4], 5, notional)
        )
        / 2,
        "45,800",
    )

    # --- 5. The annual whole-year example (Examples 4 to 6, existing cards)
    par = [0.03, 0.035, 0.04]
    p = bootstrap_annual(par)
    q("fi-bootstrap-p3-calc", "P(0,3)", p[2], "0.888299")
    q("ex4", "sum P(0,1) + P(0,2)", p[0] + p[1], "1.904226")
    q("ex4", "continuous zero 1y, %", 100 * -math.log(p[0]), "2.9559")
    q("ex4", "continuous zero 2y, %", 100 * -math.log(p[1]) / 2, "3.4486")
    q("ex4", "annual zero 2y, %", 100 * (p[1] ** -0.5 - 1), "3.5088")
    q("ex4", "continuous zero 3y, %", 100 * -math.log(p[2]) / 3, "3.9482")
    a3 = sum(p)
    q("ex4", "annuity A(0,3)", a3, "2.792525")
    q("ex4", "3y par rate rebuilt, %", 100 * (1 - p[2]) / a3, "4.0000")
    mtm = 100e6 * (0.04 - 0.035) * a3
    q("ex5", "payer MTM at K=3.5% with S=4%, USD", mtm, "1,396,262.44")
    q("fi-swap-mtm-formula", "with A rounded to 2.7925, USD", 100e6 * 0.005 * 2.7925, "1,396,250")
    q("ex5", "annuity DV01, USD per bp", 100e6 * a3 * 1e-4, "27,925.25")
    p_b = bootstrap_annual([0.03, 0.035, 0.0401])
    mtm_b = 100e6 * (0.0401 - 0.035) * sum(p_b)
    q("fi-sw-annuity-moves", "MTM after re-bootstrapping with s3 = 4.01%, USD", mtm_b, "1,424,050.76")
    q("fi-sw-annuity-moves", "change, USD", mtm_b - mtm, "27,788.32")
    q("fi-sw-annuity-moves", "new annuity", sum(p_b), "2.792256")
    q("ex6", "1y annuity", p[0], "0.970874")
    q("ex6", "1y DV01 per 100mm, USD", 100e6 * p[0] * 1e-4, "9,708.74")
    q("ex6", "1y hedge notional, USD", 100e6 * a3 / p[0], "287,630,063")
    q("ex6", "1y hedge notional, USD mm", 100 * a3 / p[0], "287.63")
    q("fi-swap-dv01-hedge-ratio", "85,000 / 19,000", 85_000 / 19_000, "4.474")
    q("fi-swap-daycount-friction", "ACT/360 year fraction of 365 days", 365 / 360, "1.0139")
    q("fi-swap-daycount-friction", "accrual misstatement, %", 100 * (365 / 360 - 1), "1.39")
    q("fi-swap-daycount-friction", "on a 4% coupon, bp of notional per year", 1e4 * 0.04 * 5 / 360, "5.56")

    print("All note 03 checks passed.")


if __name__ == "__main__":
    main()
