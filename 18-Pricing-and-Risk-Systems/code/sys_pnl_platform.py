"""P&L platform: Greek explain against full revaluation, a bond desk P&L walk, and a day-one reserve.

Backs every number in `18-Pricing-and-Risk-Systems/09-PnL-Platform.md`.
Books, market moves, trades, fees and reserve policies are labelled-hypothetical teaching inputs.
Nothing is a plug: the option book is repriced with Black-Scholes, its Greeks are analytic and checked against
finite differences, and the residual is whatever full revaluation leaves; the bond is priced from its yield, and the
walk's total is checked against the day rebuilt from position quantities times unit marks and a cash ledger with one
event per flow, which must catch any flow booked twice in the ledger or the coupon added again in the walk.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_pnl_platform.py`.
"""

from __future__ import annotations

import math

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Black-Scholes book and its Greeks
# ============================================================================


def n_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def n_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def call(s: float, k: float, t: float, r: float, vol: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
    return s * n_cdf(d1) - k * math.exp(-r * t) * n_cdf(d1 - vol * math.sqrt(t))


def greeks(s: float, k: float, t: float, r: float, vol: float) -> dict[str, float]:
    """Analytic Black-Scholes call Greeks; theta is dV/dt in calendar time (per year), vol in decimals."""
    sq = math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * sq)
    d2 = d1 - vol * sq
    vega = s * n_pdf(d1) * sq
    return {
        "delta": n_cdf(d1),
        "gamma": n_pdf(d1) / (s * vol * sq),
        "vega": vega,
        "theta": -s * n_pdf(d1) * vol / (2 * sq) - r * k * math.exp(-r * t) * n_cdf(d2),
        "vanna": -n_pdf(d1) * d2 / vol,
        "volga": vega * d1 * d2 / vol,
    }


def check_greeks_by_differences(s: float, k: float, t: float, r: float, vol: float) -> None:
    g = greeks(s, k, t, r, vol)
    hs, hv, ht = 0.01, 1e-4, 1e-6

    def v(ss: float = s, vv: float = vol, tt: float = t) -> float:
        return call(ss, k, tt, r, vv)

    fd = {
        "delta": (v(ss=s + hs) - v(ss=s - hs)) / (2 * hs),
        "gamma": (v(ss=s + hs) - 2 * v() + v(ss=s - hs)) / hs**2,
        "vega": (v(vv=vol + hv) - v(vv=vol - hv)) / (2 * hv),
        "theta": -(v(tt=t + ht) - v(tt=t - ht)) / (2 * ht),
        "vanna": (v(ss=s + hs, vv=vol + hv) - v(ss=s + hs, vv=vol - hv) - v(ss=s - hs, vv=vol + hv) + v(ss=s - hs, vv=vol - hv))
        / (4 * hs * hv),
        "volga": (v(vv=vol + hv) - 2 * v() + v(vv=vol - hv)) / hv**2,
    }
    for name, value in fd.items():
        assert abs(value - g[name]) <= 1e-4 * max(1.0, abs(g[name])), f"{name}: {value} vs {g[name]}"


def check_greek_explain() -> None:
    print("  Example 1: Greek explain of a long index call book against full revaluation")
    units = 10_000  # calls on 10,000 units of the index, hypothetical
    s0, k, t0, r, vol0 = 5_000.0, 5_000.0, 1.0, 0.04, 0.18
    s1, vol1, dt = 5_040.0, 0.175, 1.0 / 365.0
    check_greeks_by_differences(s0, k, t0, r, vol0)
    v0 = units * call(s0, k, t0, r, vol0)
    v1 = units * call(s1, k, t0 - dt, r, vol1)
    g = {name: units * x for name, x in greeks(s0, k, t0, r, vol0).items()}
    ds, dvol = s1 - s0, vol1 - vol0
    quoted("book value at T-1 ($)", v0, 4_581_801, 0)
    quoted("book value at T ($)", v1, 4_732_380, 0)
    full = quoted("full revaluation P&L ($)", v1 - v0, 150_579, 0)
    quoted("book delta ($ per index point)", g["delta"], 6_226, 0)
    quoted("book gamma ($ per point squared)", g["gamma"], 4.22, 2)
    quoted("book vega ($ per vol point)", g["vega"] / 100, 189_982, 0)
    quoted("book theta ($ per calendar day)", g["theta"] / 365, -7_594, 0)
    quoted("book vanna ($ per point per vol point)", g["vanna"] / 100, -27.91, 2)
    quoted("book volga ($ per vol point squared)", g["volga"] / 1e4, 435.72, 2)
    terms = {
        "theta": g["theta"] * dt,
        "delta": g["delta"] * ds,
        "gamma": 0.5 * g["gamma"] * ds * ds,
        "vega": g["vega"] * dvol,
        "vanna": g["vanna"] * ds * dvol,
        "volga": 0.5 * g["volga"] * dvol * dvol,
    }
    # theta is dV/dt in calendar time (negative for a long call), so one day of decay is theta * dt
    for name, q in (
        ("theta", -7_594),
        ("delta", 249_026),
        ("gamma", 3_377),
        ("vega", -94_991),
        ("vanna", 558),
        ("volga", 54.47),
    ):
        quoted(f"{name} P&L ($)", terms[name], q, 0 if name != "volga" else 2)
    first = terms["theta"] + terms["delta"] + terms["vega"]
    second = first + terms["gamma"]
    full_explain = second + terms["vanna"] + terms["volga"]
    quoted("explained by theta, delta, vega ($)", first, 146_441, 0)
    quoted("unexplained after first order ($)", full - first, 4_138, 0)
    quoted("unexplained after adding gamma ($)", full - second, 760, 0)
    quoted("unexplained after adding vanna and volga ($)", full - full_explain, 148, 0)
    quoted("unexplained as % of full P&L", (full - full_explain) / full * 100, 0.10, 2)
    # one-step explain in the order that matches a risk system: move time first, then market at the new time
    v_time = units * call(s0, k, t0 - dt, r, vol0)
    quoted("P&L from time alone, full revaluation ($)", v_time - v0, -7_597, 0)
    quoted("P&L from market moves at the new time ($)", v1 - v_time, 158_176, 0)


# ============================================================================
# 2. Bond desk P&L walk
# ============================================================================


def bond_dirty(face: float, coupon: float, y: float, years_to_next: float, n_coupons: int) -> float:
    """Dirty value of an annual-coupon bond with n_coupons left, the next in years_to_next, yield y (annual comp)."""
    pv = 0.0
    for i in range(n_coupons):
        tau = years_to_next + i
        cf = face * coupon + (face if i == n_coupons - 1 else 0.0)
        pv += cf / (1.0 + y) ** tau
    return pv


def book_value(book: dict[str, tuple[float, float]]) -> float:
    return sum(qty * mark for qty, mark in book.values())


def account_pnl(start: dict[str, tuple[float, float]], end: dict[str, tuple[float, float]], cash: list[tuple[str, float]]) -> float:
    """Day's P&L from the books: (quantity, unit mark) positions at both closes plus every cash event of the day."""
    return book_value(end) - book_value(start) + sum(amount for _, amount in cash)


def check_pnl_walk() -> None:
    print("  Example 2: bond desk P&L walk (hypothetical)")
    face, cpn = 10_000_000.0, 0.05
    # T-1: coupon due tomorrow (1/365 years), 5 coupons left; T: coupon paid, 4 left, next in 1 year
    v_prev = bond_dirty(face, cpn, 0.0450, 1.0 / 365.0, 5)
    v_now = bond_dirty(face, cpn, 0.0447, 1.0, 4)
    coupon_cash = face * cpn
    hpl = v_now + coupon_cash - v_prev
    quoted("dirty value at T-1, coupon due tomorrow ($)", v_prev, 10_678_088, 0)
    quoted("dirty value at T, ex-coupon ($)", v_now, 10_190_272, 0)
    quoted("coupon received ($)", coupon_cash, 500_000, 0)
    quoted("hypothetical P&L of the static position ($)", hpl, 12_184, 0)
    carry = bond_dirty(face, cpn, 0.0450, 1.0, 4) + coupon_cash - v_prev
    quoted("of which time at unchanged yield ($)", carry, 1_288, 0)
    quoted("of which the 3 bp yield fall ($)", hpl - carry, 10_896, 0)
    wrong = (v_now - v_prev) + coupon_cash + coupon_cash
    quoted("P&L if the coupon is added again on top ($)", wrong, 512_184, 0)
    new_trade = 5_000_000.0 * (0.9980 - 0.9950)
    funding, commissions, clearing = -12_500.0, -8_000.0, -4_500.0
    apl = hpl + new_trade + funding
    reported = apl + commissions + clearing
    quoted("new trade P&L, bought at 99.50, closed at 99.80 ($)", new_trade, 15_000, 0)
    quoted("actual P&L, Basel definition, excluding fees and commissions ($)", apl, 14_684, 0)
    quoted("reported daily P&L including fees and commissions ($)", reported, 2_184, 0)
    # second route: the day rebuilt from quantities times unit marks at both closes and a cash ledger of every flow
    start_book = {"5% bond": (face, bond_dirty(1.0, cpn, 0.0450, 1.0 / 365.0, 5))}
    end_book = {"5% bond": (face, bond_dirty(1.0, cpn, 0.0447, 1.0, 4)), "new bond": (5_000_000.0, 0.9980)}
    ledger = [
        ("coupon received", face * cpn),
        ("new bond purchase at 99.50", -5_000_000.0 * 0.9950),
        ("funding", -12_500.0),
        ("commissions", -8_000.0),
        ("clearing fees", -4_500.0),
    ]
    tol = 0.01
    assert abs(account_pnl(start_book, end_book, ledger) - reported) < tol, "walk and account disagree"
    for event in ledger:
        doubled = account_pnl(start_book, end_book, [*ledger, event])
        assert abs(doubled - reported) > tol, f"{event[0]} booked twice was not caught"
    wrong_reported = wrong + new_trade + funding + commissions + clearing
    assert abs(account_pnl(start_book, end_book, ledger) - wrong_reported) > tol, "coupon added twice was not caught"


def check_day_one() -> None:
    print("  Example 3: day-one gain on a Level 3 trade (hypothetical policy)")
    gain, years = 1_200_000.0, 4.0
    per_year = gain / years
    quoted("deferred day-one gain released per year, straight line ($)", per_year, 300_000, 0)
    quoted("remaining deferral recognised when inputs become observable after one year ($)", gain - per_year, 900_000, 0)


def main() -> None:
    print("P&L platform checks")
    check_greek_explain()
    check_pnl_walk()
    check_day_one()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All P&L platform checks passed.")


if __name__ == "__main__":
    main()
