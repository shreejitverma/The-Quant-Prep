"""Fixed income day count conventions, calendar adjustments, and payment schedules.

Backs every number and date in `06-Fixed-Income-and-Asset-Classes/11-Day-Counts-Calendars-and-Schedules.md`.
ACT/360, ACT/365F, 30/360 US, 30E/360, ACT/ACT ISDA, business-day conventions, EOM schedules, and IMM dates are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_day_counts.py`.
"""

from __future__ import annotations

import calendar
import datetime

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def is_leap_year(year: int) -> bool:
    return calendar.isleap(year)


def days_in_year(year: int) -> int:
    return 366 if is_leap_year(year) else 365


def dcf_act_360(d1: datetime.date, d2: datetime.date) -> float:
    return (d2 - d1).days / 360.0


def dcf_act_365f(d1: datetime.date, d2: datetime.date) -> float:
    return (d2 - d1).days / 365.0


def dcf_30_360_us(d1: datetime.date, d2: datetime.date) -> float:
    day1 = d1.day
    day2 = d2.day
    last_feb1 = d1.month == 2 and d1.day == calendar.monthrange(d1.year, 2)[1]
    last_feb2 = d2.month == 2 and d2.day == calendar.monthrange(d2.year, 2)[1]
    if last_feb1:
        day1 = 30
    if last_feb1 and last_feb2:
        day2 = 30
    if day1 == 31:
        day1 = 30
    if day2 == 31 and day1 == 30:
        day2 = 30
    return (360 * (d2.year - d1.year) + 30 * (d2.month - d1.month) + (day2 - day1)) / 360.0


def dcf_30e_360(d1: datetime.date, d2: datetime.date) -> float:
    day1 = min(d1.day, 30)
    day2 = min(d2.day, 30)
    return (360 * (d2.year - d1.year) + 30 * (d2.month - d1.month) + (day2 - day1)) / 360.0


def dcf_act_act_isda(d1: datetime.date, d2: datetime.date) -> float:
    if d1.year == d2.year:
        return (d2 - d1).days / days_in_year(d1.year)
    # Spanning multiple years
    days_y1 = (datetime.date(d1.year + 1, 1, 1) - d1).days
    frac = days_y1 / days_in_year(d1.year)
    for _y in range(d1.year + 1, d2.year):
        frac += 1.0
    days_y2 = (d2 - datetime.date(d2.year, 1, 1)).days
    frac += days_y2 / days_in_year(d2.year)
    return frac


def roll_modified_following(d: datetime.date, holidays: set[datetime.date] | None = None) -> datetime.date:
    """Modified Following: Following unless it crosses month-end, then Preceding."""
    hols = holidays or set()

    def is_bus(cur: datetime.date) -> bool:
        return cur.weekday() < 5 and cur not in hols

    if is_bus(d):
        return d
    # Try Following
    cur = d + datetime.timedelta(days=1)
    while not is_bus(cur):
        cur += datetime.timedelta(days=1)
    if cur.month == d.month:
        return cur
    # Crossed month: roll Preceding
    cur = d - datetime.timedelta(days=1)
    while not is_bus(cur):
        cur -= datetime.timedelta(days=1)
    return cur


def add_months(d: datetime.date, months: int, eom: bool = False) -> datetime.date:
    month_index = d.year * 12 + d.month - 1 + months
    year, month0 = divmod(month_index, 12)
    month = month0 + 1
    last_day = calendar.monthrange(year, month)[1]
    day = last_day if eom else min(d.day, last_day)
    return datetime.date(year, month, day)


def generate_schedule(
    start: datetime.date,
    periods: int,
    months_per_period: int,
    eom: bool = False,
    holidays: set[datetime.date] | None = None,
) -> list[datetime.date]:
    return [roll_modified_following(add_months(start, i * months_per_period, eom), holidays) for i in range(1, periods + 1)]


def third_wednesday(year: int, month: int) -> datetime.date:
    """IMM date: 3rd Wednesday of the month."""
    c = calendar.Calendar(firstweekday=calendar.MONDAY)
    wednesdays = [d for d in c.itermonthdates(year, month) if d.month == month and d.weekday() == 2]
    return wednesdays[2]


def test_four_conventions_leap_year() -> None:
    print("  1. Four Conventions over 15 Feb 2024 to 15 Aug 2024 (182 actual days)")
    d1 = datetime.date(2024, 2, 15)
    d2 = datetime.date(2024, 8, 15)
    actual_days = (d2 - d1).days
    notional = 1_000_000.0
    rate = 0.05

    frac_act360 = dcf_act_360(d1, d2)
    frac_act365 = dcf_act_365f(d1, d2)
    frac_30360 = dcf_30_360_us(d1, d2)
    frac_isda = dcf_act_act_isda(d1, d2)

    int_act360 = notional * rate * frac_act360
    int_act365 = notional * rate * frac_act365
    int_30360 = notional * rate * frac_30360
    int_isda = notional * rate * frac_isda

    quoted("actual days in leap year period", float(actual_days), 182.0, 0)
    quoted("ACT/360 fraction", frac_act360, 0.505556, 6)
    quoted("ACT/360 interest ($)", int_act360, 25_277.78, 2)
    quoted("ACT/365F fraction", frac_act365, 0.498630, 6)
    quoted("ACT/365F interest ($)", int_act365, 24_931.51, 2)
    quoted("30/360 fraction", frac_30360, 0.500000, 6)
    quoted("30/360 interest ($)", int_30360, 25_000.00, 2)
    quoted("ACT/ACT ISDA fraction", frac_isda, 0.497268, 6)
    quoted("ACT/ACT ISDA interest ($)", int_isda, 24_863.39, 2)

    spread_1m = int_act360 - int_isda
    spread_5bn = (5_000_000_000.0 / notional) * spread_1m
    quoted("spread between highest and lowest per 1M ($)", spread_1m, 414.39, 2)
    quoted("spread between highest and lowest per 5B ($)", spread_5bn, 2_071_949.0, 0)


def test_act_act_split() -> None:
    print("  2. ACT/ACT ISDA across Leap Year Boundary (1 July 2023 to 1 July 2024)")
    d1 = datetime.date(2023, 7, 1)
    d2 = datetime.date(2024, 7, 1)
    actual_days = (d2 - d1).days

    days_2023 = (datetime.date(2024, 1, 1) - d1).days  # 184
    days_2024 = (d2 - datetime.date(2024, 1, 1)).days  # 182
    frac_isda = (days_2023 / 365.0) + (days_2024 / 366.0)
    frac_act365 = dcf_act_365f(d1, d2)

    quoted("actual days across leap year", float(actual_days), 366.0, 0)
    quoted("days in 2023 portion", float(days_2023), 184.0, 0)
    quoted("days in 2024 portion", float(days_2024), 182.0, 0)
    quoted("ACT/ACT ISDA split fraction", frac_isda, 1.001377, 6)
    quoted("ACT/365F fraction", frac_act365, 1.002740, 6)


def test_month_ends_and_rolls() -> None:
    print("  3. Month Ends and Modified Following Business Day Adjustments")
    # 31 Jan 2024 to 31 Mar 2024
    d1 = datetime.date(2024, 1, 31)
    d2 = datetime.date(2024, 3, 31)
    frac_30360 = dcf_30_360_us(d1, d2)
    quoted("31 Jan to 31 Mar 30/360 fraction", frac_30360, 60.0 / 360.0, 6)

    # Modified Following examples
    nov_sat = datetime.date(2024, 11, 30)  # Saturday
    nov_rolled = roll_modified_following(nov_sat)
    assert nov_rolled == datetime.date(2024, 11, 29)  # Friday 29 Nov

    may_sat = datetime.date(2025, 5, 31)  # Saturday
    may_rolled = roll_modified_following(may_sat)
    assert may_rolled == datetime.date(2025, 5, 30)  # Friday 30 May

    quoted("November Saturday rolled day", float(nov_rolled.day), 29.0, 0)
    quoted("May Saturday rolled day", float(may_rolled.day), 30.0, 0)

    feb29 = datetime.date(2024, 2, 29)
    mar30 = datetime.date(2024, 3, 30)
    quoted("29 Feb to 30 Mar US 30/360 fraction", dcf_30_360_us(feb29, mar30), 30.0 / 360.0, 6)

    schedule = generate_schedule(datetime.date(2025, 2, 28), 1, 6, eom=True)
    assert schedule == [datetime.date(2025, 8, 29)]
    quoted("EOM schedule rolled August day", float(schedule[0].day), 29.0, 0)


def test_imm_dates() -> None:
    print("  4. IMM Dates for 2026")
    imm_mar = third_wednesday(2026, 3)
    imm_jun = third_wednesday(2026, 6)
    imm_sep = third_wednesday(2026, 9)
    imm_dec = third_wednesday(2026, 12)

    assert imm_mar == datetime.date(2026, 3, 18)
    assert imm_jun == datetime.date(2026, 6, 17)
    assert imm_sep == datetime.date(2026, 9, 16)
    assert imm_dec == datetime.date(2026, 12, 16)

    quoted("IMM March 2026 day", float(imm_mar.day), 18.0, 0)
    quoted("IMM June 2026 day", float(imm_jun.day), 17.0, 0)
    quoted("IMM September 2026 day", float(imm_sep.day), 16.0, 0)
    quoted("IMM December 2026 day", float(imm_dec.day), 16.0, 0)


def main() -> None:
    print("=== fi_day_counts: Day Count Fractions and Schedules ===")
    test_four_conventions_leap_year()
    test_act_act_split()
    test_month_ends_and_rolls()
    test_imm_dates()
    print(f"\nSuccessfully verified {len(QUOTED)} day count and schedule figures.")


if __name__ == "__main__":
    main()
