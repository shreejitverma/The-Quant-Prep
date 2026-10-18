"""Market and reference data platform: quote cleaning, golden copy, identifiers, RFET, snapshot clocks and tick sizing.

Backs every number in `18-Pricing-and-Risk-Systems/03-Market-and-Reference-Data-Platform.md`.

1. Robust outlier filtering with the modified z-score of Iglewicz and Hoaglin (1993), and why a standard-deviation
   z-score misses the same outlier (masking).
2. Field-level golden-copy survivorship for reference data.
3. Check digits of real identifiers: LEI (ISO 17442, ISO/IEC 7064 MOD 97-10), ISIN (ISO 6166, Luhn), CUSIP and FIGI.
4. The FRTB risk factor eligibility test of MAR31.13 on observation calendars.
5. End-of-day snapshot instants in UTC across daylight-saving regimes (US and EU rules implemented directly).
6. Tick ingestion sizing from labelled-hypothetical inputs, and Gorilla-style delta-of-delta and XOR bit costs measured
   on a seeded synthetic tick stream.

Quotes, spreads, volumes and record layouts are hypothetical teaching inputs unless a source is named.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_market_reference_data.py`.
"""

from __future__ import annotations

import datetime as dt
import random
import statistics
import struct

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:.{decimals}f}")
    return value


# ============================================================================
# 1. Robust quote filtering
# ============================================================================


def modified_z(xs: list[float]) -> tuple[float, float, list[float]]:
    """Median, MAD and modified z-scores M_i = 0.6745 (x_i - median) / MAD (Iglewicz and Hoaglin, 1993)."""
    med = statistics.median(xs)
    mad = statistics.median(abs(x - med) for x in xs)
    return med, mad, [0.6745 * (x - med) / mad for x in xs]


def classic_z(xs: list[float]) -> list[float]:
    mu, sd = statistics.mean(xs), statistics.stdev(xs)
    return [(x - mu) / sd for x in xs]


def validate_quote(bid: float, ask: float, age_s: float, prev_mid: float, max_age_s: float, max_jump: float) -> list[str]:
    """Return the failed checks for one quote (crossed or locked, stale, jump versus previous mid)."""
    fails = []
    if bid >= ask:
        fails.append("crossed" if bid > ask else "locked")
    if age_s > max_age_s:
        fails.append("stale")
    if abs(0.5 * (bid + ask) / prev_mid - 1.0) > max_jump:
        fails.append("jump")
    return fails


# ============================================================================
# 2. Field-level golden copy
# ============================================================================


def golden_record(candidates: dict[str, dict[str, object]], priority: dict[str, list[str]]) -> dict[str, tuple[object, str]]:
    """For each field take the value from the highest-priority source that supplies it; keep the winning source."""
    out = {}
    for field, order in priority.items():
        for src in order:
            v = candidates.get(src, {}).get(field)
            if v is not None:
                out[field] = (v, src)
                break
    return out


# ============================================================================
# 3. Identifier check digits
# ============================================================================


def _alnum_value(c: str) -> int:
    return int(c) if c.isdigit() else ord(c) - ord("A") + 10


def lei_check_digits(base18: str) -> str:
    """ISO/IEC 7064 MOD 97-10 check digits for the first 18 characters of an LEI."""
    n = int("".join(str(_alnum_value(c)) for c in base18) + "00")
    return f"{98 - n % 97:02d}"


def lei_valid(lei: str) -> bool:
    return len(lei) == 20 and int("".join(str(_alnum_value(c)) for c in lei)) % 97 == 1


def luhn_digit(digits: str) -> int:
    """Luhn check digit: double every second digit starting from the rightmost, sum the digits, complement mod 10."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
        total += d // 10 + d % 10
    return (10 - total % 10) % 10


def isin_check_digit(base11: str) -> int:
    return luhn_digit("".join(str(_alnum_value(c)) for c in base11))


def cusip_check_digit(base8: str) -> int:
    total = 0
    for i, c in enumerate(base8, start=1):
        v = _alnum_value(c) if c.isalnum() else {"*": 36, "@": 37, "#": 38}[c]
        if i % 2 == 0:
            v *= 2
        total += v // 10 + v % 10
    return (10 - total % 10) % 10


def figi_check_digit(base11: str) -> int:
    """'Modulus 10 Double Add Double' over the first 11 characters, doubling every second character from the left."""
    total = 0
    for i, c in enumerate(base11, start=1):
        v = _alnum_value(c)
        if i % 2 == 0:
            v *= 2
        total += sum(int(d) for d in str(v))
    return (10 - total % 10) % 10


# ============================================================================
# 4. FRTB risk factor eligibility test (MAR31.13)
# ============================================================================


def rfet(obs_days: list[dt.date], as_of: dt.date) -> dict[str, object]:
    """Both RFET criteria over the 12 months to `as_of`, counting at most one real price per day."""
    start = as_of - dt.timedelta(days=365)
    days = sorted({d for d in obs_days if start < d <= as_of})
    n = len(days)
    # Criterion (1): >= 24 per year and no 90-day window in the last 12 months with fewer than 4 observations.
    worst = min(
        sum(1 for d in days if w <= d < w + dt.timedelta(days=90)) for w in (start + dt.timedelta(days=k) for k in range(1, 365 - 89 + 1))
    )
    c1 = n >= 24 and worst >= 4
    c2 = n >= 100
    return {"count": n, "min_90d": worst, "criterion_1": c1, "criterion_2": c2, "passes": c1 or c2}


# ============================================================================
# 5. Snapshot instants in UTC across daylight saving
# ============================================================================


def _nth_sunday(year: int, month: int, n: int) -> dt.date:
    d = dt.date(year, month, 1)
    first = d + dt.timedelta(days=(6 - d.weekday()) % 7)
    return first + dt.timedelta(weeks=n - 1)


def _last_sunday(year: int, month: int) -> dt.date:
    d = dt.date(year + (month == 12), month % 12 + 1, 1) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def new_york_offset_h(d: dt.date) -> int:
    """US rule since 2007: daylight time from the second Sunday of March to the first Sunday of November."""
    return -4 if _nth_sunday(d.year, 3, 2) <= d < _nth_sunday(d.year, 11, 1) else -5


def london_offset_h(d: dt.date) -> int:
    """EU and UK rule: summer time from the last Sunday of March to the last Sunday of October."""
    return 1 if _last_sunday(d.year, 3) <= d < _last_sunday(d.year, 10) else 0


def snap_utc(d: dt.date, local_h: float, offset_h: int) -> float:
    return local_h - offset_h


# ============================================================================
# 6. Tick sizing and Gorilla-style compression costs
# ============================================================================


def tick_sizing(
    avg_rate: float, peak_rate: float, record_bytes: int, hours: float, ratio: float, hot_days: int, years: int, days_per_year: int
) -> dict[str, float]:
    daily_ticks = avg_rate * hours * 3600
    daily_raw = daily_ticks * record_bytes
    daily_comp = daily_raw / ratio
    return {
        "avg_MBps": avg_rate * record_bytes / 1e6,
        "avg_Mbps": avg_rate * record_bytes * 8 / 1e6,
        "peak_MBps": peak_rate * record_bytes / 1e6,
        "peak_Mbps": peak_rate * record_bytes * 8 / 1e6,
        "daily_ticks": daily_ticks,
        "daily_raw_GB": daily_raw / 1e9,
        "daily_comp_GB": daily_comp / 1e9,
        "hot_GB": daily_comp * hot_days / 1e9,
        "archive_TB": daily_comp * days_per_year * years / 1e12,
    }


def dod_bits(ts: list[int]) -> int:
    """Bits for timestamps 2..n with the Gorilla delta-of-delta buckets (Pelkonen et al., 2015, section 4.1.1)."""
    bits = 0
    for i in range(2, len(ts)):
        d = (ts[i] - ts[i - 1]) - (ts[i - 1] - ts[i - 2])
        if d == 0:
            bits += 1
        elif -63 <= d <= 64:
            bits += 2 + 7
        elif -255 <= d <= 256:
            bits += 3 + 9
        elif -2047 <= d <= 2048:
            bits += 4 + 12
        else:
            bits += 4 + 32
    return bits


def _f2u(x: float) -> int:
    return struct.unpack(">Q", struct.pack(">d", x))[0]


def xor_bits(vals: list[float]) -> int:
    """Bits for values 2..n with Gorilla XOR encoding (section 4.1.2), reusing the previous window when it fits."""
    bits = 0
    prev_lead, prev_trail = -1, -1
    for i in range(1, len(vals)):
        x = _f2u(vals[i]) ^ _f2u(vals[i - 1])
        if x == 0:
            bits += 1
            continue
        lead = 64 - x.bit_length()
        trail = (x & -x).bit_length() - 1
        lead = min(lead, 31)  # 5-bit field
        if prev_lead >= 0 and lead >= prev_lead and trail >= prev_trail:
            bits += 2 + (64 - prev_lead - prev_trail)
        else:
            bits += 2 + 5 + 6 + (64 - lead - trail)
            prev_lead, prev_trail = lead, trail
    return bits


def delta_bits(ints: list[int]) -> int:
    """Bits for integers 2..n coding the first difference with the same buckets as the timestamp scheme."""
    bits = 0
    for i in range(1, len(ints)):
        d = ints[i] - ints[i - 1]
        if d == 0:
            bits += 1
        elif -63 <= d <= 64:
            bits += 2 + 7
        elif -255 <= d <= 256:
            bits += 3 + 9
        elif -2047 <= d <= 2048:
            bits += 4 + 12
        else:
            bits += 4 + 32
    return bits


def luhn_digit_sum(digits: str) -> int:
    """Sum of digits after doubling every second digit starting with the rightmost (card sys-03-14 working)."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch) * (2 if i % 2 == 0 else 1)
        total += d // 10 + d % 10
    return total


def luhn_valid(number: str) -> bool:
    """Validate a complete number (check digit included): double every second digit from the right, excluding the last."""
    total = 0
    for i, ch in enumerate(reversed(number)):
        d = int(ch) * (2 if i % 2 == 1 else 1)
        total += d - 9 if d > 9 else d
    return total % 10 == 0


def synthetic_ticks(n: int, seed: int) -> tuple[list[int], list[float]]:
    """Millisecond timestamps with jittered gaps and a mid price on a 0.01 grid that changes on 30% of ticks."""
    rng = random.Random(seed)
    t, cents = 0, 10_000
    ts, px = [], []
    for _ in range(n):
        t += rng.choice((1, 2, 2, 3, 5, 8, 20, 50))
        if rng.random() < 0.3:
            cents += rng.choice((-2, -1, 1, 2))
        ts.append(t)
        px.append(cents / 100.0)
    return ts, px


def run_tests() -> None:
    print("Market and reference data platform checks")

    print("  Example 1: five broker quotes for one swaption normal vol (bp), hypothetical")
    quotes = [62.5, 63.0, 62.8, 89.5, 63.2]
    med, mad, mz = modified_z(quotes)
    quoted("median", med, 63.0, 1)
    quoted("MAD", mad, 0.2, 1)
    devs = [round(abs(q - med), 6) for q in quotes]
    assert devs == [0.5, 0.0, 0.2, 26.5, 0.2], devs
    quoted("75th percentile of the standard normal (the 0.6745 constant)", statistics.NormalDist().inv_cdf(0.75), 0.6745, 4)
    quoted("modified z of broker 4", mz[3], 89.37, 2)
    quoted("largest modified z among the other four", max(abs(z) for i, z in enumerate(mz) if i != 3), 1.69, 2)
    survivors = [q for q, z in zip(quotes, mz, strict=True) if abs(z) <= 3.5]
    quoted("survivors", len(survivors), 4, 0)
    quoted("mean of survivors", statistics.mean(survivors), 62.875, 3)
    quoted("median of survivors", statistics.median(survivors), 62.9, 1)
    cz = classic_z(quotes)
    quoted("mean with the outlier", statistics.mean(quotes), 68.2, 1)
    quoted("sample standard deviation with the outlier", statistics.stdev(quotes), 11.91, 2)
    quoted("classic z of broker 4", cz[3], 1.788, 3)
    assert abs(cz[3]) < 3.0  # masking: a 3-sigma rule misses the outlier it inflated
    quoted("largest possible classic z with n = 5, (n - 1)/sqrt(n)", 4 / 5**0.5, 1.789, 3)
    assert abs(cz[3]) <= 4 / 5**0.5  # Shiffler (1988): no sample z can exceed (n - 1)/sqrt(n)

    print("  Quote checks")
    assert validate_quote(100.02, 100.01, 1, 100.0, 5, 0.05) == ["crossed"]
    assert validate_quote(100.00, 100.02, 30, 100.0, 5, 0.05) == ["stale"]
    assert validate_quote(110.00, 110.02, 1, 100.0, 5, 0.05) == ["jump"]
    assert validate_quote(100.00, 100.02, 1, 100.0, 5, 0.05) == []

    print("  Example 2: proxy spread for an illiquid bond (hypothetical)")
    alpha, beta, index_spread = 20.0, 1.15, 145.0
    quoted("beta times index spread (bp)", beta * index_spread, 166.75, 2)
    quoted("proxy spread (bp)", alpha + beta * index_spread, 186.75, 2)
    quoted("proxy spread after a 10 bp index widening (bp)", alpha + beta * (index_spread + 10), 198.25, 2)

    print("  Example 3: field-level golden copy (hypothetical sources)")
    cands = {
        "issuer_feed": {"maturity": "2033-06-15", "coupon": 4.25, "seniority": None},
        "vendor_a": {"maturity": "2033-06-15", "coupon": 4.25, "seniority": "Senior Unsecured", "country": "US"},
        "vendor_b": {"maturity": "2033-06-14", "coupon": None, "seniority": "Senior", "country": "US"},
    }
    prio = {
        "maturity": ["issuer_feed", "vendor_a", "vendor_b"],
        "coupon": ["issuer_feed", "vendor_a", "vendor_b"],
        "seniority": ["vendor_a", "vendor_b"],
        "country": ["vendor_b", "vendor_a"],
    }
    g = golden_record(cands, prio)
    assert g["maturity"] == ("2033-06-15", "issuer_feed") and g["seniority"] == ("Senior Unsecured", "vendor_a")
    disagreements = sum(len({c[f] for c in cands.values() if c.get(f) is not None}) > 1 for f in prio)
    quoted("fields where sources disagree (sent to a data steward)", disagreements, 2, 0)

    print("  Identifiers: check digits of real codes")
    gleif = "506700GE1G29325QX363"  # LEI of the Global Legal Entity Identifier Foundation (api.gleif.org)
    assert lei_valid(gleif)
    quoted("LEI check digits recomputed for GLEIF", int(lei_check_digits(gleif[:18])), 63, 0)
    assert not lei_valid(gleif[:17] + "R" + gleif[18:])
    assert "".join(str(_alnum_value(c)) for c in "US037833100") == "3028037833100"  # card sys-03-14
    quoted("ISIN check digit for US037833100 (Apple Inc.)", isin_check_digit("US037833100"), 5, 0)
    quoted("Luhn digit sum of 3028037833100 (card sys-03-14)", luhn_digit_sum("3028037833100"), 45, 0)
    assert luhn_valid("30280378331005") and not luhn_valid("30280378331004")  # validation of the full ISIN
    quoted("CUSIP check digit for 03783310 (Apple Inc.)", cusip_check_digit("03783310"), 0, 0)
    quoted("FIGI check digit for BBG000B9XRY (Apple Inc.)", figi_check_digit("BBG000B9XRY"), 4, 0)
    # The ISIN embeds the CUSIP for US securities: country code + 9-character CUSIP + ISIN check digit.
    assert "US" + "03783310" + str(cusip_check_digit("03783310")) == "US037833100"
    # A single transposition is caught by Luhn unless it swaps 0 and 9.
    assert isin_check_digit("US037833010") != 5

    print("  Example 4: FRTB RFET (MAR31.13) on two observation calendars")
    as_of = dt.date(2026, 9, 30)
    start = as_of - dt.timedelta(days=365)
    # Factor A: 30 real prices, all in the first half of the window (a liquid spell, then nothing).
    a_days = [start + dt.timedelta(days=1 + 6 * k) for k in range(30)]
    ra = rfet(a_days, as_of)
    quoted("factor A observations", ra["count"], 30, 0)
    quoted("factor A fewest observations in any 90-day window", ra["min_90d"], 0, 0)
    assert ra["passes"] is False
    # Factor B: 26 real prices, one every 14 days.
    b_days = [start + dt.timedelta(days=1 + 14 * k) for k in range(26)]
    rb = rfet(b_days, as_of)
    quoted("factor B observations", rb["count"], 26, 0)
    quoted("factor B fewest observations in any 90-day window", rb["min_90d"], 6, 0)
    assert rb["passes"] is True and rb["criterion_2"] is False

    print("  Example 5: snapshot instants in UTC (hypothetical snap times 16:30 London, 16:00 New York)")
    for d, gap in ((dt.date(2026, 1, 15), 4.5), (dt.date(2026, 3, 16), 3.5), (dt.date(2026, 7, 15), 4.5), (dt.date(2026, 10, 28), 3.5)):
        lon = snap_utc(d, 16.5, london_offset_h(d))
        nyc = snap_utc(d, 16.0, new_york_offset_h(d))
        quoted(f"{d.isoformat()} New York snap minus London snap (hours)", nyc - lon, gap, 1)
    misaligned = sum(
        1
        for k in range(365)
        if (lambda d: snap_utc(d, 16.0, new_york_offset_h(d)) - snap_utc(d, 16.5, london_offset_h(d)))(
            dt.date(2026, 1, 1) + dt.timedelta(days=k)
        )
        != 4.5
    )
    quoted("calendar days in 2026 when the gap is not 4.5 hours", misaligned, 28, 0)
    try:
        from zoneinfo import ZoneInfo

        for k in range(365):
            d = dt.date(2026, 1, 1) + dt.timedelta(days=k)
            for tz, fn in (("America/New_York", new_york_offset_h), ("Europe/London", london_offset_h)):
                off = dt.datetime(d.year, d.month, d.day, 12, tzinfo=ZoneInfo(tz)).utcoffset()
                assert off is not None and off.total_seconds() / 3600 == fn(d), (tz, d)
        print("    hand-coded DST rules agree with the IANA tz database for every day of 2026")
    except Exception as exc:  # tz database absent on some minimal images; the rules above are then the only check
        if type(exc).__name__ not in ("ZoneInfoNotFoundError", "ModuleNotFoundError"):
            raise
        print("    IANA tz database not available; skipped cross-check")

    print("  Example 6: tick ingestion sizing (hypothetical inputs)")
    z = tick_sizing(80_000, 450_000, 32, 10, 4.5, 30, 7, 252)
    quoted("average bandwidth (MB/s)", z["avg_MBps"], 2.56, 2)
    quoted("average bandwidth (Mbit/s)", z["avg_Mbps"], 20.48, 2)
    quoted("peak bandwidth (MB/s)", z["peak_MBps"], 14.4, 1)
    quoted("peak bandwidth (Mbit/s)", z["peak_Mbps"], 115.2, 1)
    quoted("ticks per day (billions)", z["daily_ticks"] / 1e9, 2.88, 2)
    quoted("raw volume per day (GB)", z["daily_raw_GB"], 92.16, 2)
    quoted("compressed per day at 4.5:1 (GB)", z["daily_comp_GB"], 20.48, 2)
    quoted("30-day hot tier (GB)", z["hot_GB"], 614.4, 1)
    quoted("7-year archive (TB)", z["archive_TB"], 36.13, 2)

    print("  Gorilla-style bit costs on a synthetic tick stream (seed 5, 200,000 ticks)")
    ts, px = synthetic_ticks(200_000, seed=5)
    tbits = dod_bits(ts) / (len(ts) - 2)
    vbits = xor_bits(px) / (len(px) - 1)
    quoted("timestamp bits per tick, delta-of-delta", tbits, 7.8, 1)
    quoted("price bits per tick, XOR of binary doubles", vbits, 16.0, 1)
    quoted("bytes per (timestamp, price) pair with XOR prices", (tbits + vbits) / 8, 2.97, 2)
    quoted("compression versus 16 raw bytes with XOR prices", 16 / ((tbits + vbits) / 8), 5.4, 1)
    ibits = delta_bits([round(p * 100) for p in px]) / (len(px) - 1)
    quoted("price bits per tick, delta of integer ticks", ibits, 3.4, 1)
    quoted("bytes per pair with integer-tick prices", (tbits + ibits) / 8, 1.39, 2)
    quoted("compression versus 16 raw bytes with integer-tick prices", 16 / ((tbits + ibits) / 8), 11.5, 1)
    unchanged = sum(px[i] == px[i - 1] for i in range(1, len(px))) / (len(px) - 1)
    quoted("share of ticks with an unchanged price (%)", 100 * unchanged, 70.1, 1)

    print(f"  {len(QUOTED)} numbers quoted in note 03 computed, printed and asserted")
    print("All market and reference data checks passed.")


if __name__ == "__main__":
    run_tests()
