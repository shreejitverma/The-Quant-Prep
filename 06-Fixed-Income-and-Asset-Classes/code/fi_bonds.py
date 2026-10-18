"""Bond prices from yields, accrued interest, Treasury pricing formulas, duration, convexity and hedging.

Backs every number in note 02 (Bonds, Duration and Convexity).
Part 1 reproduces the U.S. Treasury's own worked examples in 31 CFR Part 356 Appendix B, section II
(eCFR, retrieved 2026-10-17), counting the day numbers r and s from the calendar rather than copying them.
Every analytic duration and convexity is checked against bump-and-reprice.
Each `q(...)` asserts a computed value against the literal quoted in the note at the note's rounding and prints it.
Run with `python 06-Fixed-Income-and-Asset-Classes/code/fi_bonds.py`.
"""

from __future__ import annotations

import math
from datetime import date


def q(tag: str, label: str, value: float, text: str) -> None:
    """Assert that `value` rounds to the quoted `text` (half a unit of its last decimal) and print it."""
    decimals = len(text.split(".")[1]) if "." in text else 0
    literal = float(text.replace(",", ""))
    assert abs(value - literal) <= 0.5 * 10.0**-decimals + 1e-12, f"[{tag}] {label}: computed {value!r}, note quotes {text}"
    print(f"  [{tag}] {label} = {text}")


def days(a: date, b: date) -> int:
    return (b - a).days


# ------------------------------------------------------------ 31 CFR 356 Appendix B, section II


def annuity(i: float, n: int) -> float:
    """a_n = v + v^2 + ... + v^n with v = 1/(1 + i/2); summed directly so i = 0 is handled (Appendix B special case)."""
    v = 1.0 / (1.0 + i / 2.0)
    return sum(v**k for k in range(1, n + 1))


def treasury_price_regular(c: float, i: float, n: int, r: int, s: int) -> float:
    """Section II.A/B: P [1 + (r/s)(i/2)] = (C/2)(r/s) + (C/2) a_n + 100 v^n."""
    v_n = (1.0 + i / 2.0) ** -n
    return ((c / 2) * (r / s) + (c / 2) * annuity(i, n) + 100 * v_n) / (1 + (r / s) * (i / 2))


def treasury_price_long_first(c: float, i: float, n: int, r: int, s: int) -> float:
    """Section II.C: P [1 + (r/s)(i/2)] = [(C/2)(r/s)] v + (C/2) a_n + 100 v^n."""
    v = 1.0 / (1.0 + i / 2.0)
    return ((c / 2) * (r / s) * v + (c / 2) * annuity(i, n) + 100 * v**n) / (1 + (r / s) * (i / 2))


def treasury_price_with_accrued(c: float, i: float, n: int, r: int, s: int) -> tuple[float, float]:
    """Section II.D: (P + A)[1 + (r/s)(i/2)] = C/2 + (C/2) a_n + 100 v^n with A = ((s - r)/s)(C/2); returns (P, A)."""
    accrued = (s - r) / s * (c / 2)
    dirty = (c / 2 + (c / 2) * annuity(i, n) + 100 * (1 + i / 2) ** -n) / (1 + (r / s) * (i / 2))
    return dirty - accrued, accrued


def dirty_compound_fraction(c: float, i: float, n: int, r: int, s: int) -> float:
    """Alternative convention: discount the fractional period with (1 + i/2)^(r/s) instead of simple interest."""
    return (c / 2 + (c / 2) * annuity(i, n) + 100 * (1 + i / 2) ** -n) * (1 + i / 2) ** -(r / s)


# ------------------------------------------------------------ yield-based risk on a regular schedule


def cashflows(coupon: float, years: int, freq: int = 1, face: float = 100.0) -> list[tuple[float, float]]:
    n = years * freq
    return [((k + 1) / freq, face * coupon / freq + (face if k == n - 1 else 0.0)) for k in range(n)]


def price(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    return sum(cf * (1 + y / freq) ** (-freq * t) for t, cf in cfs)


def macaulay(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    return sum(t * cf * (1 + y / freq) ** (-freq * t) for t, cf in cfs) / price(cfs, y, freq)


def modified(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    return macaulay(cfs, y, freq) / (1 + y / freq)


def convexity(cfs: list[tuple[float, float]], y: float, freq: int = 1) -> float:
    """(1/P) d2P/dy2 = (1/P) sum cf t (t + 1/f) (1 + y/f)^(-f t - 2)."""
    s = sum(cf * t * (t + 1 / freq) * (1 + y / freq) ** (-freq * t - 2) for t, cf in cfs)
    return s / price(cfs, y, freq)


def bump_duration_convexity(cfs: list[tuple[float, float]], y: float, dy: float, freq: int = 1) -> tuple[float, float]:
    """Effective duration and convexity by central bump-and-reprice."""
    p0, pu, pd = price(cfs, y, freq), price(cfs, y + dy, freq), price(cfs, y - dy, freq)
    return (pd - pu) / (2 * p0 * dy), (pu + pd - 2 * p0) / (p0 * dy * dy)


def ytm(cfs: list[tuple[float, float]], target: float, freq: int = 1) -> float:
    lo, hi = -0.5, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if price(cfs, mid, freq) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> None:
    print("Note 02: Bonds, Duration and Convexity")

    # --- 1. Treasury Appendix B examples, day numbers counted from the calendar (Core concepts, card fi-bd-treasury-formula)
    r_a = days(date(1990, 5, 15), date(1990, 11, 15))
    assert r_a == 184
    q("treasury-II.A", "8 3/4% bond at 8.84%, P", treasury_price_regular(8.75, 0.0884, 59, r_a, r_a), "99.057893")
    r_b, s_b = days(date(1990, 4, 2), date(1990, 9, 30)), days(date(1990, 3, 31), date(1990, 9, 30))
    assert (r_b, s_b) == (181, 183)
    q("treasury-II.B", "8 1/2% note short first period at 8.59%, P", treasury_price_regular(8.50, 0.0859, 3, r_b, s_b), "99.838183")
    r_c, s_c = days(date(1990, 3, 1), date(1990, 5, 15)), days(date(1989, 11, 15), date(1990, 5, 15))
    assert (r_c, s_c) == (75, 181)
    q("treasury-II.C", "8 1/2% note long first period at 8.53%, P", treasury_price_long_first(8.50, 0.0853, 10, r_c, s_c), "99.805118")
    r_d, s_d = days(date(1985, 11, 29), date(1986, 5, 15)), days(date(1985, 11, 15), date(1986, 5, 15))
    assert (r_d, s_d) == (167, 181)
    p_d, a_d = treasury_price_with_accrued(9.50, 0.0954, 19, r_d, s_d)
    q("treasury-II.D", "9 1/2% note accrued A per 100", a_d, "0.367403")
    q("treasury-II.D", "9 1/2% note clean P", p_d, "99.730918")
    # Appendix B section I.D example: 6 3/4% note, 92 days accrued in a 184-day half-year, per $1,000 rounded to 5 places
    daily = 1000 * 0.0675 / 2 / 184
    q("treasury-I.D", "daily interest decimal per $1,000", daily, "0.183423913")
    q("treasury-I.D", "accrued per $1,000 for 92 days", round(daily * 92, 5), "16.87500")

    # --- 2. A hypothetical 4.25% note maturing 15 Nov 2034, settling Mon 19 Oct 2026 at 4.10% (Example 1, cards fi-clean-dirty, fi-bd-*)
    last, nxt, settle = date(2026, 5, 15), date(2026, 11, 15), date(2026, 10, 19)
    s = days(last, nxt)
    r = days(settle, nxt)
    elapsed = days(last, settle)
    q("ex1", "days in the coupon period s", s, "184")
    q("ex1", "days accrued", elapsed, "157")
    q("ex1", "days to next coupon r", r, "27")
    n_after = 16  # coupons 15 May 2027 ... 15 Nov 2034 after the next one
    assert sum(1 for y in range(2027, 2035) for _ in (5, 11)) == n_after
    clean, accrued = treasury_price_with_accrued(4.25, 0.041, n_after, r, s)
    q("fi-bd-treasury-accrued", "accrued per 100", accrued, "1.813179")
    q("ex1", "clean price (Appendix B simple-interest fraction)", clean, "101.016799")
    q("ex1", "dirty price", clean + accrued, "102.829978")
    dirty_cf = dirty_compound_fraction(4.25, 0.041, n_after, r, s)
    q("ex1", "dirty price, compounded fraction convention", dirty_cf, "102.832642")
    q("fi-bd-fraction-convention", "convention difference per 100, cents", 100 * (dirty_cf - (clean + accrued)), "0.27")
    q("fi-bd-fraction-convention", "convention difference on 100mm, USD", 1e6 * (dirty_cf - (clean + accrued)), "2,664")
    # clean is smooth, dirty jumps through the coupon date at constant yield (card fi-bd-dirty-jump-coupon)
    fri, mon = date(2026, 11, 13), date(2026, 11, 16)
    c_fri, a_fri = treasury_price_with_accrued(4.25, 0.041, n_after, days(fri, nxt), s)
    s2 = days(nxt, date(2027, 5, 15))
    c_mon, a_mon = treasury_price_with_accrued(4.25, 0.041, n_after - 1, days(mon, date(2027, 5, 15)), s2)
    q("fi-bd-dirty-jump-coupon", "Fri 13 Nov dirty", c_fri + a_fri, "103.116329")
    q("fi-bd-dirty-jump-coupon", "Mon 16 Nov dirty", c_mon + a_mon, "101.025519")
    q("fi-bd-dirty-jump-coupon", "Fri 13 Nov clean", c_fri, "101.014427")
    q("fi-bd-dirty-jump-coupon", "Mon 16 Nov clean", c_mon, "101.013778")
    q("fi-bd-dirty-jump-coupon", "dirty change over the coupon, per 100", (c_mon + a_mon) - (c_fri + a_fri), "-2.090811")
    q("fi-bd-dirty-jump-coupon", "clean change over the coupon, per 100", c_mon - c_fri, "-0.000649")
    # A coupon-equals-yield bond halfway through a period is not at par (card fi-par-bond-price)
    c_half, a_half = treasury_price_with_accrued(4.0, 0.04, 10, 91, 182)
    q("fi-par-bond-price", "4% at 4% halfway, Appendix B clean", c_half, "99.990099")
    dirty_half_cf = dirty_compound_fraction(4.0, 0.04, 10, 91, 182)
    q("fi-par-bond-price", "4% at 4% halfway, compounded-fraction clean", dirty_half_cf - a_half, "99.995049")

    # --- 3. Duration and convexity, analytic versus bump-and-reprice (Examples 2 to 4)
    b2 = cashflows(0.05, 2)
    p2 = price(b2, 0.04)
    assert abs(p2 - (5 / 1.04 + 105 / 1.04**2)) < 1e-12
    q("ex2", "2y 5% at 4%: price", p2, "101.886095")
    q("ex2", "Macaulay duration", macaulay(b2, 0.04), "1.952813")
    q("ex2", "modified duration", modified(b2, 0.04), "1.877705")
    q("ex2", "convexity", convexity(b2, 0.04), "5.372829")
    dv01_2 = (price(b2, 0.0399) - price(b2, 0.0401)) / 2
    q("fi-dv01-formula", "DV01 per 100 by bump", dv01_2, "0.019131")
    q("fi-dv01-formula", "P x Dmod x 1e-4", p2 * modified(b2, 0.04) * 1e-4, "0.019131")
    full = price(b2, 0.05) - p2
    approx = p2 * (-modified(b2, 0.04) * 0.01 + 0.5 * convexity(b2, 0.04) * 0.01**2)
    q("ex2", "+100bp full reprice", full, "-1.886095")
    q("ex2", "+100bp duration-convexity estimate", approx, "-1.885749")
    q("ex2", "error of the estimate", full - approx, "-0.000345")
    # third-order term explains the residual: -(1/6) P * (1/P d3P/dy3) dy^3
    d3 = sum(cf * t * (t + 1) * (t + 2) * 1.04 ** (-t - 3) for t, cf in b2)
    q("ex2", "third-order Taylor term", -d3 * 0.01**3 / 6, "-0.000349")

    par10 = cashflows(0.04, 10)
    assert abs(price(par10, 0.04) - 100) < 1e-10
    dmod10, c10 = modified(par10, 0.04), convexity(par10, 0.04)
    q("ex3", "10y par: modified duration", dmod10, "8.1109")
    q("ex3", "10y par: Macaulay duration", macaulay(par10, 0.04), "8.4353")
    q("ex3", "10y par: convexity", c10, "80.754")
    q("ex3", "10y par: DV01 per 100", 100 * dmod10 * 1e-4, "0.081109")
    q("ex3", "price at 5%", price(par10, 0.05), "92.2783")
    q("ex3", "price at 3%", price(par10, 0.03), "108.5302")
    q("fi-duration-convexity-approx", "exact change at 5%, per 100", price(par10, 0.05) - 100, "-7.7217")
    q("ex3", "exact change at 3%, per 100", price(par10, 0.03) - 100, "8.5302")
    q("ex3", "duration-convexity estimate +100bp", 100 * (-dmod10 * 0.01 + 0.5 * c10 * 1e-4), "-7.707")
    q("ex3", "duration-convexity estimate -100bp", 100 * (dmod10 * 0.01 + 0.5 * c10 * 1e-4), "8.515")
    q("fi-duration-convexity-approx", "duration term", -dmod10 * 0.01, "-0.081109")
    q("fi-duration-convexity-approx", "convexity term", 0.5 * c10 * 1e-4, "0.004038")
    # bump-and-reprice reproduces the analytics; large bumps pick up higher-order terms
    ed1, ec1 = bump_duration_convexity(par10, 0.04, 1e-4)
    ed100, ec100 = bump_duration_convexity(par10, 0.04, 0.01)
    # central differences have O(dy^2) truncation error: about 1e-6 relative at 1bp
    assert abs(ed1 - dmod10) < 1e-5 and abs(ec1 - c10) < 1e-2, (ed1, dmod10, ec1, c10)
    q("fi-bd-effective-duration-bump", "effective duration, 1bp bump", ed1, "8.1109")
    q("fi-bd-effective-duration-bump", "effective duration, 100bp bump", ed100, "8.1260")
    q("fi-bd-effective-duration-bump", "effective convexity, 1bp bump", ec1, "80.754")
    q("fi-bd-effective-duration-bump", "effective convexity, 100bp bump", ec100, "80.847")

    zero10 = [(10.0, 100.0)]
    q("ex4", "10y zero price at 4%", price(zero10, 0.04), "67.5564")
    q("fi-zero-duration", "10y zero Macaulay duration", macaulay(zero10, 0.04), "10.0000")
    q("fi-bd-zero-convexity-formula", "10y zero convexity T(T+1)/(1+y)^2", convexity(zero10, 0.04), "101.70")
    assert abs(convexity(zero10, 0.04) - 110 / 1.04**2) < 1e-12
    # coupon effect: higher coupon, lower duration (card fi-coupon-duration-effect)
    q("fi-coupon-duration-effect", "10y 8% bond modified duration at 4%", modified(cashflows(0.08, 10), 0.04), "7.3435")

    # --- 4. Curve-based (Fisher-Weil) duration versus yield duration (card fi-bd-fisher-weil)
    zc = [math.log(1.03), 2 * math.log(1.035) / 2, 3 * math.log(1.04) / 3]  # continuous zeros of note 01 Example 1
    flows = [(1.0, 4.0), (2.0, 4.0), (3.0, 104.0)]
    pv = sum(cf * math.exp(-z * t) for (t, cf), z in zip(flows, zc, strict=True))
    q("ex5", "3y 4% bond on the note 01 curve", pv, "100.0732")
    fisher_weil = sum(t * cf * math.exp(-z * t) for (t, cf), z in zip(flows, zc, strict=True)) / pv
    h = 1e-5
    pv_up = sum(cf * math.exp(-(z + h) * t) for (t, cf), z in zip(flows, zc, strict=True))
    pv_dn = sum(cf * math.exp(-(z - h) * t) for (t, cf), z in zip(flows, zc, strict=True))
    assert abs((pv_dn - pv_up) / (2 * h * pv) - fisher_weil) < 1e-8
    q("fi-bd-fisher-weil", "Fisher-Weil duration (parallel continuous zero shift)", fisher_weil, "2.8851")
    y3 = ytm(flows, pv)
    q("fi-bd-fisher-weil", "yield to maturity, %", 100 * y3, "3.9737")
    q("fi-bd-fisher-weil", "Macaulay duration at the yield", macaulay(flows, y3), "2.8861")
    q("fi-bd-fisher-weil", "modified duration at the yield", modified(flows, y3), "2.7758")
    q("ex5", "Macaulay minus Fisher-Weil", macaulay(flows, y3) - fisher_weil, "0.0011")

    # --- 5. DV01 hedge and what it leaves (cards fi-duration-hedge, fi-bd-steepener-hedge-pnl)
    dv01_10 = (price(par10, 0.0399) - price(par10, 0.0401)) / 2
    ratio = dv01_10 / dv01_2
    q("fi-duration-hedge", "face of 2y 5% bond to short per 100 of 10y par", ratio, "4.2396")
    # parallel +10bp: hedged P&L is the convexity mismatch only
    pnl_par = (price(par10, 0.041) - 100) - ratio * (price(b2, 0.041) - p2)
    q("fi-bd-steepener-hedge-pnl", "hedged P&L per 100, parallel +10bp", pnl_par, "0.0029")
    pnl_steep = price(par10, 0.041) - 100
    q("fi-bd-steepener-hedge-pnl", "hedged P&L per 100, 10y +10bp and 2y unchanged", pnl_steep, "-0.8071")

    # --- 6. Barbell versus bullet with zeros at a flat 4% annual (card fi-barbell-bullet)
    w2 = (10 - 5) / (10 - 2)
    q("fi-barbell-bullet", "PV weight on the 2y zero", w2, "0.625")
    conv_bullet = 5 * 6 / 1.04**2
    conv_barbell = w2 * 2 * 3 / 1.04**2 + (1 - w2) * 10 * 11 / 1.04**2
    q("fi-barbell-bullet", "bullet 5y zero convexity", conv_bullet, "27.737")
    q("fi-barbell-bullet", "barbell convexity", conv_barbell, "41.605")

    def barbell_minus_bullet(dy: float) -> float:
        """P&L per 100 of PV of long barbell, short bullet after a parallel yield move dy."""
        g = (1.04 / (1.04 + dy)) ** 1
        return 100 * (w2 * g**2 + (1 - w2) * g**10 - g**5)

    q("fi-barbell-bullet", "barbell minus bullet, +100bp", barbell_minus_bullet(0.01), "0.0651")
    q("fi-barbell-bullet", "barbell minus bullet, -100bp", barbell_minus_bullet(-0.01), "0.0740")
    q("fi-barbell-bullet", "barbell minus bullet, +1bp, USD per 100mm of PV", 1e6 * barbell_minus_bullet(0.0001), "6.9")

    # --- 7. Corporate 30/360 accrued (card fi-clean-dirty)
    acc = 2.5 * 60 / 180
    q("fi-clean-dirty", "30/360 accrued per 100", acc, "0.8333")
    q("fi-clean-dirty", "dirty price from clean 99.50", 99.50 + acc, "100.3333")

    # --- 8. Yield solve: bracket with negative yields (card fi-ytm-solve)
    y_neg = ytm(cashflows(0.0, 5), 102.0)
    q("fi-ytm-solve", "5y zero priced at 102: yield, %", 100 * y_neg, "-0.3953")

    print("All note 02 checks passed.")


if __name__ == "__main__":
    main()
