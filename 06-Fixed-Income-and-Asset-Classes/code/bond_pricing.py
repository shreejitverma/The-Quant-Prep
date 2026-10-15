"""Day counts, bond pricing and risk, and overnight-rate compounding.

Small reference implementation for the fixed income notes.
Run ``python bond_pricing.py``: the ``__main__`` block checks every result
against a value derived by hand in the notes (closed forms or visible arithmetic).
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta

# ---------------------------------------------------------------- day counts


def _is_leap(year: int) -> bool:
    return calendar.isleap(year)


def yearfrac(start: date, end: date, convention: str) -> float:
    """Year fraction between two dates under a named convention.

    ``30/360`` is the US bond basis (30/360 with end-of-February ignored), ``ACT/ACT``
    is the ISDA variant that splits the period by calendar year.
    """
    if end < start:
        raise ValueError("end before start")
    if convention == "ACT/360":
        return (end - start).days / 360.0
    if convention == "ACT/365F":
        return (end - start).days / 365.0
    if convention == "30/360":
        d1, d2 = min(start.day, 30), end.day
        if d2 == 31 and d1 == 30:
            d2 = 30
        days = 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)
        return days / 360.0
    if convention == "ACT/ACT":
        if start.year == end.year:
            return (end - start).days / (366.0 if _is_leap(start.year) else 365.0)
        first = (date(start.year + 1, 1, 1) - start).days / (366.0 if _is_leap(start.year) else 365.0)
        last = (end - date(end.year, 1, 1)).days / (366.0 if _is_leap(end.year) else 365.0)
        return first + (end.year - start.year - 1) + last
    raise ValueError(f"unknown convention {convention}")


def add_months(d: date, months: int) -> date:
    """Add calendar months, clamping the day to the end of the target month."""
    total = d.year * 12 + (d.month - 1) + months
    year, month = divmod(total, 12)
    return date(year, month + 1, min(d.day, calendar.monthrange(year, month + 1)[1]))


def modified_following(d: date, holidays: frozenset[date] = frozenset()) -> date:
    """Roll to the next business day, back to the previous one if that crosses a month end."""

    def is_bd(x: date) -> bool:
        return x.weekday() < 5 and x not in holidays

    out = d
    while not is_bd(out):
        out += timedelta(days=1)
    if out.month != d.month:
        out = d
        while not is_bd(out):
            out -= timedelta(days=1)
    return out


# ------------------------------------------------------------------ bonds


def cashflows(coupon: float, years: int, freq: int = 1, face: float = 100.0) -> list[tuple[float, float]]:
    """(time in years, amount) for a fixed-rate bullet paying on exact period ends."""
    n = years * freq
    return [((i + 1) / freq, face * coupon / freq + (face if i == n - 1 else 0.0)) for i in range(n)]


def price(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    """Price from a periodically compounded yield: sum CF / (1 + y/f)^(f t)."""
    return sum(cf / (1 + y / freq) ** (freq * t) for t, cf in cfs)


def yield_from_price(cfs: list[tuple[float, float]], p: float, freq: int = 1) -> float:
    """Solve price(y) = p by bisection; price is strictly decreasing in y."""
    lo, hi = -0.5, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if price(cfs, mid, freq) > p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def macaulay_duration(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    p = price(cfs, y, freq)
    return sum(t * cf / (1 + y / freq) ** (freq * t) for t, cf in cfs) / p


def modified_duration(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    return macaulay_duration(cfs, y, freq) / (1 + y / freq)


def convexity(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    """(1/P) d2P/dy2 for a periodically compounded yield."""
    p = price(cfs, y, freq)
    s = sum(cf * t * (t + 1 / freq) / (1 + y / freq) ** (freq * t + 2) for t, cf in cfs)
    return s / p


def dv01(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    """Price change for a one basis point fall in yield, by central difference."""
    h = 1e-4
    return (price(cfs, y - h, freq) - price(cfs, y + h, freq)) / 2


# ------------------------------------------------- overnight rate compounding


def compound_in_arrears(rates: list[float], days: list[int], basis: float = 360.0) -> float:
    """Compounded overnight rate over a period: (prod (1 + r_i d_i / B) - 1) * B / sum(d_i)."""
    growth = 1.0
    for r, d in zip(rates, days, strict=True):
        growth *= 1 + r * d / basis
    return (growth - 1) * basis / sum(days)


def main() -> None:
    # Day counts: 2024-02-15 to 2024-08-15 (leap year, 182 actual days).
    s, e = date(2024, 2, 15), date(2024, 8, 15)
    assert (e - s).days == 182
    assert abs(yearfrac(s, e, "ACT/360") - 182 / 360) < 1e-12
    assert abs(yearfrac(s, e, "ACT/365F") - 182 / 365) < 1e-12
    assert abs(yearfrac(s, e, "30/360") - 0.5) < 1e-12
    assert abs(yearfrac(s, e, "ACT/ACT") - 182 / 366) < 1e-12
    # Month-end roll: 31 Jan plus one month clamps to 29 Feb in a leap year.
    assert add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)
    # Without an end-of-month flag, anchor stepping leaves month-end starts off month end.
    assert add_months(date(2025, 2, 28), 6) == date(2025, 8, 28)
    assert add_months(date(2025, 4, 30), 6) == date(2025, 10, 30)
    assert modified_following(date(2025, 8, 31)) == date(2025, 8, 29)
    # ACT/ACT across a year boundary: 184 days of 2023 plus 182 days of leap 2024.
    assert abs(yearfrac(date(2023, 7, 1), date(2024, 7, 1), "ACT/ACT") - (184 / 365 + 182 / 366)) < 1e-12
    assert abs(yearfrac(date(2023, 7, 1), date(2024, 7, 1), "ACT/365F") - 366 / 365) < 1e-12
    # US 30/360 from 31 Jan to 31 Mar: both day-31s become 30, so 60 days.
    assert abs(yearfrac(date(2024, 1, 31), date(2024, 3, 31), "30/360") - 60 / 360) < 1e-12
    # Saturdays 30 Nov 2024 and 31 May 2025 roll back to the Friday under modified following.
    assert modified_following(date(2024, 11, 30)) == date(2024, 11, 29)
    assert modified_following(date(2025, 5, 31)) == date(2025, 5, 30)
    # 2026 IMM dates are Wednesdays on days 15 to 21 of the quarterly months.
    for m, d in ((3, 18), (6, 17), (9, 16), (12, 16)):
        assert date(2026, m, d).weekday() == 2 and 15 <= d <= 21

    # 2-year 5% annual bullet at 4%: P = 5/1.04 + 105/1.04^2 by hand.
    cfs = cashflows(0.05, 2)
    p = price(cfs, 0.04)
    hand = 5 / 1.04 + 105 / 1.04**2
    assert abs(p - hand) < 1e-12
    # Macaulay duration: (1*5/1.04 + 2*105/1.04^2) / P.
    mac = (5 / 1.04 + 2 * 105 / 1.04**2) / hand
    assert abs(macaulay_duration(cfs, 0.04) - mac) < 1e-12
    assert abs(modified_duration(cfs, 0.04) - mac / 1.04) < 1e-12
    # Convexity: (1/P) * (2*1*5/1.04^3 + 3*2*105/1.04^4)... = sum CF t (t+1) / (1+y)^(t+2).
    conv = (5 * 1 * 2 / 1.04**3 + 105 * 2 * 3 / 1.04**4) / hand
    assert abs(convexity(cfs, 0.04) - conv) < 1e-12
    # DV01 close to -dP/dy * 1bp = P * D_mod * 1e-4 (convexity correction is second order).
    assert abs(dv01(cfs, 0.04) - hand * modified_duration(cfs, 0.04) * 1e-4) < 1e-6
    # Price-yield round trip.
    assert abs(yield_from_price(cfs, p) - 0.04) < 1e-10
    # Duration-convexity approximation for a +100bp shock vs full reprice.
    approx = hand * (-modified_duration(cfs, 0.04) * 0.01 + 0.5 * conv * 0.01**2)
    assert abs((price(cfs, 0.05) - hand) - approx) < 1e-3
    # Par bond: price 100 and modified duration equal to the annuity factor (1 - (1+y)^-n) / y.
    par3 = cashflows(0.03, 3)
    assert abs(price(par3, 0.03) - 100.0) < 1e-10
    assert abs(modified_duration(par3, 0.03) - (1 - 1.03**-3) / 0.03) < 1e-12
    par10 = cashflows(0.04, 10)
    d10 = (1 - 1.04**-10) / 0.04
    assert abs(price(par10, 0.04) - 100.0) < 1e-10
    assert abs(modified_duration(par10, 0.04) - d10) < 1e-12
    assert abs(macaulay_duration(par10, 0.04) - 1.04 * d10) < 1e-12
    assert abs(convexity(par10, 0.04) - 80.754) < 1e-3
    assert abs(dv01(par10, 0.04) - 0.081109) < 1e-6
    assert abs(price(par10, 0.05) - 92.2783) < 1e-4
    assert abs(price(par10, 0.03) - 108.5302) < 1e-4
    c10 = convexity(par10, 0.04)
    assert abs(100 * (-d10 * 0.01 + 0.5 * c10 * 0.01**2) - (-7.707)) < 1e-3
    assert abs(100 * (d10 * 0.01 + 0.5 * c10 * 0.01**2) - 8.515) < 1e-3
    # 10-year zero: price 100/1.04^10, Macaulay duration 10, convexity T(T+1)/(1+y)^2.
    zero = [(10.0, 100.0)]
    assert abs(price(zero, 0.04) - 100 / 1.04**10) < 1e-12
    assert abs(price(zero, 0.04) - 67.5564) < 1e-4
    assert abs(macaulay_duration(zero, 0.04) - 10.0) < 1e-12
    assert abs(convexity(zero, 0.04) - 110 / 1.04**2) < 1e-12

    # Compounding in arrears: 5 business days (Mon to Fri, 3 days over weekend) at 5.00% then 5.10%.
    r = compound_in_arrears([0.05, 0.05, 0.05, 0.051, 0.051], [1, 1, 1, 1, 3])
    growth = (1 + 0.05 / 360) ** 3 * (1 + 0.051 / 360) * (1 + 0.051 * 3 / 360)
    assert abs(r - (growth - 1) * 360 / 7) < 1e-12

    print("price", round(p, 6), "macD", round(mac, 6), "modD", round(mac / 1.04, 6))
    print("convexity", round(conv, 6), "DV01", round(dv01(cfs, 0.04), 6))
    print("shock +100bp: full", round(price(cfs, 0.05) - p, 6), "approx", round(approx, 6))
    print("compounded SOFR-style rate", round(r * 100, 6), "%")
    print("ok")


if __name__ == "__main__":
    main()
