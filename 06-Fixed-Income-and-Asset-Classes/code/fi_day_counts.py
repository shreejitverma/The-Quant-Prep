"""Day count fractions, business-day rolls, schedules and RFR observation conventions.

Backs every number and date in `06-Fixed-Income-and-Asset-Classes/11-Day-Counts-Calendars-and-Schedules.md`.
Day counts follow the 2006 ISDA Definitions Section 4.16 (b) to (h), ICMA Rule 251 for ACT/ACT ICMA,
31 CFR Part 356 Appendix B for US Treasury accrued interest, and the SIA/SIFMA "30/360 US" rule set.
Each fraction that has an independent definition is cross-checked against it: ACT/ACT ISDA against a
day-by-day enumeration, ACT/360 and ACT/365F against counted days, and the Treasury half-year lengths
against Table 1 of 31 CFR Part 356 Appendix B.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_day_counts.py`.
"""

from __future__ import annotations

import calendar
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


def quoted_date(label: str, value: dt.date, expected: dt.date) -> dt.date:
    """Print a date the note quotes and assert it equals the quoted date."""
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value.isoformat()} ({value.strftime('%A')})")
    return value


# ---------------------------------------------------------------- day counts (ISDA 2006 Section 4.16)


def days_in_year(year: int) -> int:
    return 366 if calendar.isleap(year) else 365


def is_last_of_feb(d: dt.date) -> bool:
    return d.month == 2 and d.day == calendar.monthrange(d.year, 2)[1]


def act_360(d1: dt.date, d2: dt.date) -> float:
    """4.16(e): actual days / 360."""
    return (d2 - d1).days / 360.0


def act_365f(d1: dt.date, d2: dt.date) -> float:
    """4.16(d): actual days / 365."""
    return (d2 - d1).days / 365.0


def act_act_isda(d1: dt.date, d2: dt.date) -> float:
    """4.16(b): days in a leap year / 366 plus days in a non-leap year / 365 (split at 1 January)."""
    if d1.year == d2.year:
        return (d2 - d1).days / days_in_year(d1.year)
    frac = (dt.date(d1.year + 1, 1, 1) - d1).days / days_in_year(d1.year)
    frac += float(d2.year - d1.year - 1)
    frac += (d2 - dt.date(d2.year, 1, 1)).days / days_in_year(d2.year)
    return frac


def act_act_isda_enumerated(d1: dt.date, d2: dt.date) -> float:
    """Independent check: add 1/365 or 1/366 for every calendar day in [d1, d2)."""
    total = 0.0
    cur = d1
    while cur < d2:
        total += 1.0 / days_in_year(cur.year)
        cur += ONE_DAY
    return total


def act_act_icma(d1: dt.date, d2: dt.date, ref_start: dt.date, ref_end: dt.date, freq: int) -> float:
    """4.16(c) / ICMA Rule 251: days accrued / (frequency x days in the reference coupon period)."""
    return (d2 - d1).days / (freq * (ref_end - ref_start).days)


def _thirty(y1: int, m1: int, dd1: int, y2: int, m2: int, dd2: int) -> float:
    return (360 * (y2 - y1) + 30 * (m2 - m1) + (dd2 - dd1)) / 360.0


def thirty_360_bond_basis(d1: dt.date, d2: dt.date) -> float:
    """4.16(f) 30/360 (Bond Basis): D1 31 -> 30; D2 31 -> 30 only if D1 (after adjustment) is 30."""
    dd1 = 30 if d1.day == 31 else d1.day
    dd2 = 30 if (d2.day == 31 and dd1 == 30) else d2.day
    return _thirty(d1.year, d1.month, dd1, d2.year, d2.month, dd2)


def thirty_u_360(d1: dt.date, d2: dt.date, eom: bool = True) -> float:
    """SIA/SIFMA 30/360 US: the Bond Basis rules plus the February end-of-month rules."""
    dd1, dd2 = d1.day, d2.day
    if eom and is_last_of_feb(d1) and is_last_of_feb(d2):
        dd2 = 30
    if eom and is_last_of_feb(d1):
        dd1 = 30
    if dd2 == 31 and dd1 >= 30:
        dd2 = 30
    if dd1 == 31:
        dd1 = 30
    return _thirty(d1.year, d1.month, dd1, d2.year, d2.month, dd2)


def thirty_e_360(d1: dt.date, d2: dt.date) -> float:
    """4.16(g) 30E/360 (Eurobond Basis): any 31 -> 30."""
    return _thirty(d1.year, d1.month, min(d1.day, 30), d2.year, d2.month, min(d2.day, 30))


def thirty_e_360_isda(d1: dt.date, d2: dt.date, maturity: dt.date) -> float:
    """4.16(h) 30E/360 (ISDA): last day of month -> 30, except D2 = last day of February at maturity."""
    dd1 = 30 if d1.day == calendar.monthrange(d1.year, d1.month)[1] else d1.day
    last2 = d2.day == calendar.monthrange(d2.year, d2.month)[1]
    dd2 = 30 if (last2 and not (d2 == maturity and d2.month == 2)) else d2.day
    return _thirty(d1.year, d1.month, dd1, d2.year, d2.month, dd2)


# ---------------------------------------------------------------- calendars and business-day conventions


class Calendar:
    """Weekends plus an explicit, versioned holiday list."""

    def __init__(self, name: str, holidays: set[dt.date]) -> None:
        self.name = name
        self.holidays = holidays

    def is_business_day(self, d: dt.date) -> bool:
        return d.weekday() < 5 and d not in self.holidays

    def following(self, d: dt.date) -> dt.date:
        while not self.is_business_day(d):
            d += ONE_DAY
        return d

    def preceding(self, d: dt.date) -> dt.date:
        while not self.is_business_day(d):
            d -= ONE_DAY
        return d

    def modified_following(self, d: dt.date) -> dt.date:
        f = self.following(d)
        return f if f.month == d.month else self.preceding(d)

    def modified_preceding(self, d: dt.date) -> dt.date:
        p = self.preceding(d)
        return p if p.month == d.month else self.following(d)

    def add_business_days(self, d: dt.date, n: int) -> dt.date:
        step = ONE_DAY if n >= 0 else -ONE_DAY
        remaining = abs(n)
        while remaining:
            d += step
            if self.is_business_day(d):
                remaining -= 1
        return d


WEEKENDS_ONLY = Calendar("weekends only", set())
# A few US holidays used in the examples (Labor Day 2025, Veterans Day 2026, Thanksgiving 2026).
US_EXAMPLE = Calendar(
    "US example",
    {dt.date(2025, 9, 1), dt.date(2026, 11, 11), dt.date(2026, 11, 26)},
)


def add_months(d: dt.date, months: int, eom: bool) -> dt.date:
    """Unadjusted date `months` after d; with eom the result is pinned to the month end."""
    idx = d.year * 12 + d.month - 1 + months
    year, m0 = divmod(idx, 12)
    last = calendar.monthrange(year, m0 + 1)[1]
    return dt.date(year, m0 + 1, last if eom else min(d.day, last))


def backward_schedule(effective: dt.date, maturity: dt.date, months: int, cal: Calendar) -> list[tuple[dt.date, dt.date]]:
    """Unadjusted dates generated backward from maturity (short front stub), then modified following."""
    unadjusted = [maturity]
    k = 1
    while True:
        d = add_months(maturity, -months * k, eom=False)
        if d <= effective:
            break
        unadjusted.append(d)
        k += 1
    unadjusted.append(effective)
    unadjusted.reverse()
    adjusted = [unadjusted[0]] + [cal.modified_following(d) for d in unadjusted[1:]]
    return list(zip(adjusted[:-1], adjusted[1:], strict=True))


def nth_weekday(year: int, month: int, weekday: int, n: int) -> dt.date:
    d = dt.date(year, month, 1)
    while d.weekday() != weekday:
        d += ONE_DAY
    return d + dt.timedelta(days=7 * (n - 1))


# ---------------------------------------------------------------- examples


def example_four_conventions() -> None:
    print("  1. One coupon period, four conventions (15 Feb 2024 to 15 Aug 2024)")
    d1, d2 = dt.date(2024, 2, 15), dt.date(2024, 8, 15)
    notional, rate = 1_000_000.0, 0.05
    days = (d2 - d1).days
    enumerated_days = sum(1 for k in range(400) if d1 + dt.timedelta(days=k) < d2)
    assert days == enumerated_days
    quoted("actual days", float(days), 182.0, 0)
    fr = {
        "ACT/360": act_360(d1, d2),
        "ACT/365F": act_365f(d1, d2),
        "30/360 Bond Basis": thirty_360_bond_basis(d1, d2),
        "ACT/ACT ISDA": act_act_isda(d1, d2),
    }
    assert abs(fr["ACT/ACT ISDA"] - act_act_isda_enumerated(d1, d2)) < 1e-12
    expected = {
        "ACT/360": (0.505556, 25_277.78),
        "ACT/365F": (0.498630, 24_931.51),
        "30/360 Bond Basis": (0.500000, 25_000.00),
        "ACT/ACT ISDA": (0.497268, 24_863.39),
    }
    for name, (f_exp, i_exp) in expected.items():
        quoted(f"{name} fraction", fr[name], f_exp, 6)
        quoted(f"{name} interest (USD)", notional * rate * fr[name], i_exp, 2)
    # ACT/ACT ICMA on a semiannual schedule: a full regular period is exactly 0.5.
    icma = act_act_icma(d1, d2, d1, d2, 2)
    quoted("ACT/ACT ICMA fraction (full semiannual period)", icma, 0.500000, 6)
    spread = notional * rate * (fr["ACT/360"] - fr["ACT/ACT ISDA"])
    quoted("ACT/360 minus ACT/ACT ISDA per 1mm (USD)", spread, 414.3898, 4)
    quoted("same gap on 5bn notional (USD)", spread * 5_000.0, 2_071_949.0, 0)
    quoted("ACT/360 minus ACT/365F per 1mm (USD)", notional * rate * (fr["ACT/360"] - fr["ACT/365F"]), 346.27, 2)
    quoted("ACT/360 over ACT/365F ratio minus 1 (%)", (365.0 / 360.0 - 1.0) * 100.0, 1.39, 2)


def example_act_act_isda_split() -> None:
    print("  2. ACT/ACT ISDA across 1 January (1 Jul 2023 to 1 Jul 2024)")
    d1, d2 = dt.date(2023, 7, 1), dt.date(2024, 7, 1)
    quoted("actual days", float((d2 - d1).days), 366.0, 0)
    quoted("days in 2023", float((dt.date(2024, 1, 1) - d1).days), 184.0, 0)
    quoted("days in 2024", float((d2 - dt.date(2024, 1, 1)).days), 182.0, 0)
    isda = act_act_isda(d1, d2)
    assert abs(isda - act_act_isda_enumerated(d1, d2)) < 1e-12
    quoted("184/365", 184.0 / 365.0, 0.504110, 6)
    quoted("182/366", 182.0 / 366.0, 0.497268, 6)
    quoted("ACT/ACT ISDA fraction", isda, 1.001377, 6)
    quoted("ACT/365F fraction", act_365f(d1, d2), 1.002740, 6)
    quoted("ACT/365F minus ACT/ACT ISDA", act_365f(d1, d2) - isda, 0.001362, 6)
    quoted("same gap in days of a 365-day year", (act_365f(d1, d2) - isda) * 365.0, 0.50, 2)


def example_thirty_360_family() -> None:
    print("  3. The 30/360 family on month-end dates")
    # 31 Jan 2024 to 31 Mar 2024: all variants give 60/360.
    a, b = dt.date(2024, 1, 31), dt.date(2024, 3, 31)
    quoted("31 Jan to 31 Mar 2024, Bond Basis", thirty_360_bond_basis(a, b), 60.0 / 360.0, 6)
    # 28 Feb 2025 (last day of February) to 31 Aug 2025.
    d1, d2 = dt.date(2025, 2, 28), dt.date(2025, 8, 31)
    quoted("actual days 28 Feb to 31 Aug 2025", float((d2 - d1).days), 184.0, 0)
    quoted("30/360 Bond Basis (days)", thirty_360_bond_basis(d1, d2) * 360.0, 183.0, 0)
    quoted("30/360 US with Feb EOM rule (days)", thirty_u_360(d1, d2) * 360.0, 180.0, 0)
    quoted("30E/360 (days)", thirty_e_360(d1, d2) * 360.0, 182.0, 0)
    quoted("30E/360 ISDA (days)", thirty_e_360_isda(d1, d2, maturity=dt.date(2030, 8, 31)) * 360.0, 180.0, 0)
    quoted("ACT/ACT ICMA semiannual (days in 360 basis)", act_act_icma(d1, d2, d1, d2, 2) * 360.0, 180.0, 0)
    # 30E/360 ISDA at maturity on the last day of February keeps the actual day.
    m1, m2 = dt.date(2025, 8, 31), dt.date(2026, 2, 28)
    quoted("30E/360 ISDA to Feb maturity (days)", thirty_e_360_isda(m1, m2, maturity=m2) * 360.0, 178.0, 0)
    quoted("30E/360 ISDA to Feb non-maturity (days)", thirty_e_360_isda(m1, m2, maturity=dt.date(2030, 2, 28)) * 360.0, 180.0, 0)


def example_rolls_and_eom() -> None:
    print("  4. Business-day rolls and the end-of-month rule")
    cal = WEEKENDS_ONLY
    quoted_date("30 Nov 2024 following", cal.following(dt.date(2024, 11, 30)), dt.date(2024, 12, 2))
    quoted_date("30 Nov 2024 modified following", cal.modified_following(dt.date(2024, 11, 30)), dt.date(2024, 11, 29))
    quoted_date("31 May 2025 modified following", cal.modified_following(dt.date(2025, 5, 31)), dt.date(2025, 5, 30))
    quoted_date("1 Jun 2025 preceding", cal.preceding(dt.date(2025, 6, 1)), dt.date(2025, 5, 30))
    quoted_date("1 Jun 2025 modified preceding", cal.modified_preceding(dt.date(2025, 6, 1)), dt.date(2025, 6, 2))
    # Holiday interaction: Sunday 31 Aug 2025, Monday 1 Sep 2025 is Labor Day.
    us = US_EXAMPLE
    quoted_date("31 Aug 2025 following, US example calendar", us.following(dt.date(2025, 8, 31)), dt.date(2025, 9, 2))
    quoted_date("31 Aug 2025 modified following, US example calendar", us.modified_following(dt.date(2025, 8, 31)), dt.date(2025, 8, 29))
    # EOM rule: six months from Friday 28 Feb 2025.
    no_eom = add_months(dt.date(2025, 2, 28), 6, eom=False)
    with_eom = add_months(dt.date(2025, 2, 28), 6, eom=True)
    quoted_date("6m after 28 Feb 2025 without EOM (unadjusted)", no_eom, dt.date(2025, 8, 28))
    quoted_date("6m after 28 Feb 2025 with EOM (unadjusted)", with_eom, dt.date(2025, 8, 31))
    quoted_date("EOM date after modified following", cal.modified_following(with_eom), dt.date(2025, 8, 29))
    quoted_date("non-EOM date after modified following", cal.modified_following(no_eom), dt.date(2025, 8, 28))


def example_treasury_accrual() -> None:
    print("  5. US Treasury accrued interest (31 CFR Part 356 Appendix B)")
    last_cpn, next_cpn, settle = dt.date(2026, 2, 15), dt.date(2026, 8, 15), dt.date(2026, 4, 1)
    half_year = (next_cpn - last_cpn).days
    # Table 1 of Appendix B: February to August, 15th of the month, regular year = 181 days.
    assert half_year == 181
    quoted("days in half-year 15 Feb to 15 Aug 2026", float(half_year), 181.0, 0)
    accrued_days = (settle - last_cpn).days
    quoted("days accrued to 1 Apr 2026", float(accrued_days), 45.0, 0)
    ai = 100.0 * 0.04 / 2.0 * accrued_days / half_year
    quoted("accrued interest per 100 on a 4% note", ai, 0.497238, 6)
    wrong = 100.0 * 0.04 * accrued_days / 365.0
    quoted("same accrual if computed ACT/365F (wrong)", wrong, 0.493151, 6)
    quoted("error of the ACT/365F accrual (points)", ai - wrong, 0.0041, 4)


def example_backward_schedule() -> None:
    print("  6. Backward schedule with a short front stub")
    eff, mat = dt.date(2026, 1, 15), dt.date(2028, 11, 15)
    periods = backward_schedule(eff, mat, 6, WEEKENDS_ONLY)
    starts = [p[0] for p in periods]
    ends = [p[1] for p in periods]
    quoted("number of periods", float(len(periods)), 6.0, 0)
    quoted_date("stub end (first payment)", ends[0], dt.date(2026, 5, 15))
    quoted_date("15 Nov 2026 rolled (Sunday)", ends[1], dt.date(2026, 11, 16))
    quoted_date("15 May 2027 rolled (Saturday)", ends[2], dt.date(2027, 5, 17))
    quoted("stub accrual ACT/360", act_360(starts[0], ends[0]), 0.333333, 6)
    quoted("stub length in days", float((ends[0] - starts[0]).days), 120.0, 0)
    forward = []
    d = eff
    while d < mat:
        nxt = add_months(d, 6, eom=False)
        forward.append(min(nxt, mat))
        d = nxt
    quoted_date("forward generation: last regular date before maturity", forward[-2], dt.date(2028, 7, 15))
    quoted("forward generation: back stub days", float((mat - forward[-2]).days), 123.0, 0)


def example_rfr_lookback_vs_shift() -> None:
    print("  7. Compounded SOFR: lookback without shift vs observation shift (2 business days)")
    cal = US_EXAMPLE
    fix = {
        dt.date(2026, 10, 29): 0.0430,
        dt.date(2026, 10, 30): 0.0445,
        dt.date(2026, 11, 2): 0.0431,
        dt.date(2026, 11, 3): 0.0431,
        dt.date(2026, 11, 4): 0.0432,
        dt.date(2026, 11, 5): 0.0432,
        dt.date(2026, 11, 6): 0.0433,
    }
    start, end = dt.date(2026, 11, 2), dt.date(2026, 11, 9)

    def business_days(a: dt.date, b: dt.date) -> list[dt.date]:
        out, cur = [], a
        while cur < b:
            if cal.is_business_day(cur):
                out.append(cur)
            cur += ONE_DAY
        return out

    # Lookback without shift: weights from the accrual period, rate from 2 business days earlier.
    growth_lb = 1.0
    for d in business_days(start, end):
        n_i = (cal.add_business_days(d, 1) - d).days
        growth_lb *= 1.0 + fix[cal.add_business_days(d, -2)] * n_i / 360.0
    rate_lb = (growth_lb - 1.0) * 360.0 / (end - start).days
    # Observation shift: both rates and weights from the observation period shifted 2 business days.
    o_start, o_end = cal.add_business_days(start, -2), cal.add_business_days(end, -2)
    growth_os = 1.0
    for d in business_days(o_start, o_end):
        n_i = (cal.add_business_days(d, 1) - d).days
        growth_os *= 1.0 + fix[d] * n_i / 360.0
    rate_os = (growth_os - 1.0) * 360.0 / (o_end - o_start).days
    quoted_date("observation period start", o_start, dt.date(2026, 10, 29))
    quoted_date("observation period end", o_end, dt.date(2026, 11, 5))
    quoted("lookback without shift (%)", rate_lb * 100.0, 4.33420, 5)
    quoted("observation shift (%)", rate_os * 100.0, 4.37136, 5)
    quoted("difference (bp)", (rate_os - rate_lb) * 1e4, 3.72, 2)


def example_imm_and_cds_dates() -> None:
    print("  8. IMM futures dates and CDS roll dates for 2026")
    for month, day in ((3, 18), (6, 17), (9, 16), (12, 16)):
        quoted_date(f"third Wednesday {month}/2026", nth_weekday(2026, month, 2, 3), dt.date(2026, month, day))
    # CDS standard coupon dates: the 20th, adjusted following (weekends only here).
    quoted_date("CDS date 20 Jun 2026 (Saturday) following", WEEKENDS_ONLY.following(dt.date(2026, 6, 20)), dt.date(2026, 6, 22))
    quoted_date("CDS date 20 Dec 2026 (Sunday) following", WEEKENDS_ONLY.following(dt.date(2026, 12, 20)), dt.date(2026, 12, 21))


def main() -> None:
    print("=== fi_day_counts: day counts, calendars, schedules ===")
    example_four_conventions()
    example_act_act_isda_split()
    example_thirty_360_family()
    example_rolls_and_eom()
    example_treasury_accrual()
    example_backward_schedule()
    example_rfr_lookback_vs_shift()
    example_imm_and_cds_dates()
    print(f"\nVerified {len(QUOTED)} day count, date and schedule figures.")


if __name__ == "__main__":
    main()
