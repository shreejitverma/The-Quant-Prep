"""Hazard rates, CDS legs with exact integrals, bootstrapping, the credit triangle, standard contract dates, Merton.

Backs every number in note 06 (Credit Basics: Hazard Rates and CDS).
- Legs are integrated exactly on each sub-interval where the hazard rate and the forward rate are constant,
  the assumption the ISDA CDS Standard Model makes (piecewise-constant hazards, piecewise-flat forwards);
  a mid-point discretisation is computed beside it to show its error.
- The standard-contract date and coupon arithmetic reproduces Table 1 and the worked examples of
  "Standard CDS Examples: Supporting Document for the Implementation of the ISDA CDS Standard Model" (cdsmodel.com).
Each `q(...)` asserts a computed value against the literal quoted in the note and prints it.
Run with `python 06-Fixed-Income-and-Asset-Classes/code/fi_cds.py`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, timedelta
from statistics import NormalDist

N01 = NormalDist()


def q(tag: str, label: str, value: float, text: str) -> None:
    """Assert that `value` rounds to the quoted `text` (half a unit of its last decimal) and print it."""
    decimals = len(text.split(".")[1]) if "." in text else 0
    literal = float(text.replace(",", ""))
    assert abs(value - literal) <= 0.5 * 10.0**-decimals + 1e-12, f"[{tag}] {label}: computed {value!r}, note quotes {text}"
    print(f"  [{tag}] {label} = {text}")


# ------------------------------------------------------------ curves


@dataclass(frozen=True)
class HazardCurve:
    """Piecewise-constant hazard rates: hazards[j] applies on (pillars[j-1], pillars[j]], the last one beyond."""

    pillars: tuple[float, ...]
    hazards: tuple[float, ...]

    def hazard(self, t: float) -> float:
        for p, h in zip(self.pillars, self.hazards, strict=False):
            if t < p:
                return h
        return self.hazards[-1]

    def survival(self, t: float) -> float:
        acc, prev = 0.0, 0.0
        for p, h in zip(self.pillars, self.hazards, strict=False):
            if t <= p:
                return math.exp(-(acc + h * (t - prev)))
            acc += h * (p - prev)
            prev = p
        return math.exp(-(acc + self.hazards[-1] * (t - prev)))


def flat_df(r: float):
    return lambda t: math.exp(-r * t)


# ------------------------------------------------------------ CDS legs


def legs_exact(
    curve: HazardCurve, rate: float, maturity: float, period: float = 0.25, accrual_on_default: bool = True
) -> tuple[float, float]:
    """(RPV01, protection PV per unit notional with LGD = 1) by exact integration on constant-(h, r) sub-intervals.

    Premium accrues with year fraction equal to elapsed model time (a stylised schedule); on default the buyer
    pays the accrued premium at the default time.
    """
    df = flat_df(rate)
    n = int(round(maturity / period))
    rpv01, prot = 0.0, 0.0
    for i in range(n):
        s, e = i * period, (i + 1) * period
        cuts = sorted({s, e, *[p for p in curve.pillars if s < p < e]})
        rpv01 += period * df(e) * curve.survival(e)
        for a, b in zip(cuts[:-1], cuts[1:], strict=True):
            h = curve.hazard(0.5 * (a + b))
            lam, dt = rate + h, b - a
            base = df(a) * curve.survival(a)
            prot += base * h / lam * (1 - math.exp(-lam * dt))
            if accrual_on_default:
                x0 = a - s
                ex = math.exp(-lam * dt)
                rpv01 += base * h * (x0 * (1 - ex) / lam + (1 - ex * (1 + lam * dt)) / lam**2)
    return rpv01, prot


def legs_midpoint(curve: HazardCurve, rate: float, maturity: float, period: float = 0.25) -> tuple[float, float]:
    """Common textbook discretisation: default at period mid-point, half a coupon accrued on default."""
    df = flat_df(rate)
    n = int(round(maturity / period))
    rpv01, prot = 0.0, 0.0
    for i in range(n):
        s, e = i * period, (i + 1) * period
        pd = curve.survival(s) - curve.survival(e)
        rpv01 += period * df(e) * (curve.survival(e) + 0.5 * pd)
        prot += df(0.5 * (s + e)) * pd
    return rpv01, prot


def bootstrap(spreads: list[tuple[float, float]], recovery: float, rate: float, engine=legs_exact) -> HazardCurve:
    """Sequentially solve each pillar's hazard so that the par spread is repriced; bisection on a checked bracket."""
    pillars: list[float] = []
    hazards: list[float] = []
    for tenor, spread in spreads:
        pillars.append(tenor)

        def gap(h: float, tenor: float = tenor, spread: float = spread) -> float:
            rpv, prot = engine(HazardCurve(tuple(pillars), (*hazards, h)), rate, tenor)
            return (1 - recovery) * prot - spread * rpv

        lo, hi = 0.0, 2.0
        assert gap(lo) < 0 < gap(hi), "spread curve needs a negative or huge forward hazard"
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if gap(mid) < 0:
                lo = mid
            else:
                hi = mid
        hazards.append(0.5 * (lo + hi))
    return HazardCurve(tuple(pillars), tuple(hazards))


def par_spread(curve: HazardCurve, recovery: float, rate: float, tenor: float, engine=legs_exact) -> float:
    rpv, prot = engine(curve, rate, tenor)
    return (1 - recovery) * prot / rpv


# ------------------------------------------------------------ standard contract dates


def following(d: date) -> date:
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def merton(v0: float, debt: float, sigma: float, r: float, t: float) -> tuple[float, float, float, float]:
    """(equity, debt value, risk-neutral default probability, credit spread) in Merton (1974)."""
    sd = sigma * math.sqrt(t)
    d1 = (math.log(v0 / debt) + (r + 0.5 * sigma**2) * t) / sd
    d2 = d1 - sd
    equity = v0 * N01.cdf(d1) - debt * math.exp(-r * t) * N01.cdf(d2)
    debt_value = v0 - equity
    spread = -math.log(debt_value / (debt * math.exp(-r * t))) / t
    return equity, debt_value, N01.cdf(-d2), spread


def main() -> None:
    print("Note 06: Credit Basics: Hazard Rates and CDS")
    r, rec = 0.04, 0.40

    # --- Survival basics (card fi-cds-survival-math)
    q("fi-cds-survival-math", "5y survival at a constant 2.5% hazard, %", 100 * math.exp(-0.125), "88.25")
    q("fi-cds-survival-math", "1y default probability at 2.5% hazard, %", 100 * (1 - math.exp(-0.025)), "2.47")
    q("fi-cds-survival-math", "expected default time 1/lambda, years", 1 / 0.025, "40")

    # --- Example 1: the credit triangle against exact par spreads (cards fi-credit-cds-triangle, fi-cds-triangle-exact)
    for h, tri, txt_aod, txt_no in ((0.025, "150", "150.75", "151.23"), (0.20, "1200", "1205.97", "1236.73")):
        flat = HazardCurve((5.0,), (h,))
        q("fi-cds-triangle-exact", f"triangle (1 - R) h at h = {h:.1%}, bp", 1e4 * (1 - rec) * h, tri)
        q(
            "fi-cds-triangle-exact",
            f"exact quarterly par spread with accrual on default, h = {h:.1%}, bp",
            1e4 * par_spread(flat, rec, r, 5.0),
            txt_aod,
        )
        rpv_no, prot_no = legs_exact(flat, r, 5.0, accrual_on_default=False)
        q("fi-cds-accrual-on-default", f"same without accrual on default, h = {h:.1%}, bp", 1e4 * (1 - rec) * prot_no / rpv_no, txt_no)
    # continuous premium limit: RPV01 and protection share the integral of P Q, so s = (1 - R) h exactly
    flat = HazardCurve((5.0,), (0.025,))
    # the gap to the triangle is premium timing and shrinks linearly with the period: 0.75 bp quarterly, 0.25 bp monthly
    monthly = legs_exact(flat, r, 5.0, period=1 / 12)
    q("fi-cds-triangle-exact", "monthly premium with accrual on default, bp", 1e4 * (1 - rec) * monthly[1] / monthly[0], "150.25")
    fine = legs_exact(flat, r, 5.0, period=1 / 3650)
    assert abs((1 - rec) * fine[1] / fine[0] - 0.015) < 1e-7  # O(period) error, about 8e-8 at a tenth of a day

    # --- Example 2: bootstrapping 1y, 3y, 5y par spreads (cards fi-cds-bootstrap-calc, fi-credit-cds-rpv01-definition)
    quotes = [(1.0, 0.0100), (3.0, 0.0120), (5.0, 0.0150)]
    curve = bootstrap(quotes, rec, r)
    for tenor, s in quotes:
        assert abs(par_spread(curve, rec, r, tenor) - s) < 1e-12
    for j, txt in enumerate(("1.6584", "2.1714", "3.3684")):
        q("fi-cds-bootstrap-calc", f"hazard on segment {j + 1}, %", 100 * curve.hazards[j], txt)
    q("fi-cds-bootstrap-calc", "Q(5), %", 100 * curve.survival(5.0), "88.04")
    rpv5, prot5 = legs_exact(curve, r, 5.0)
    q("fi-credit-cds-rpv01-definition", "5y RPV01", rpv5, "4.2820")
    q("ex2", "5y protection leg PV (LGD 60%)", (1 - rec) * prot5, "0.064230")
    upfront = (1 - rec) * prot5 - 0.0100 * rpv5
    q("fi-credit-cds-upfront-formula", "upfront on a 100bp coupon, % of notional", 100 * upfront, "2.1410")
    assert abs(upfront - (0.0150 - 0.0100) * rpv5) < 1e-15
    q("ex2", "upfront on 10mm, USD", 1e7 * upfront, "214,101")
    mid_curve = bootstrap(quotes, rec, r, engine=legs_midpoint)
    rpv_mid, prot_mid = legs_midpoint(mid_curve, r, 5.0)
    q("ex2", "mid-point engine: 5y hazard, %", 100 * mid_curve.hazards[2], "3.3684")
    q("ex2", "mid-point engine: upfront, % of notional", 100 * ((1 - rec) * prot_mid - 0.01 * rpv_mid), "2.1410")

    # --- Example 3: CS01 by bump-and-rebootstrap (card fi-credit-cds-cs01-vs-dv01)
    notional = 10_000_000.0

    def buyer_value(qs: list[tuple[float, float]]) -> float:
        c = bootstrap(qs, rec, r)
        rp, pr = legs_exact(c, r, 5.0)
        return notional * ((1 - rec) * pr - 0.0100 * rp)

    v0 = buyer_value(quotes)
    up = buyer_value([(t, s + 1e-4) for t, s in quotes])
    q("fi-credit-cds-cs01-vs-dv01", "CS01 (all par spreads +1bp, rebuild), USD", up - v0, "4,196")
    q("fi-credit-cds-cs01-vs-dv01", "RPV01 x 1bp x notional, USD", rpv5 * 1e-4 * notional, "4,282")
    rate_up = notional * ((1 - rec) * legs_exact(curve, r + 1e-4, 5.0)[1] - 0.01 * legs_exact(curve, r + 1e-4, 5.0)[0])
    q("fi-credit-cds-cs01-vs-dv01", "IR01 (rates +1bp, hazards held), USD", rate_up - v0, "-69")

    # --- Example 4: jump to default (card fi-credit-cds-jtd-formula)
    jtd = (1 - rec) * notional - v0
    q("fi-credit-cds-jtd-formula", "buyer's JTD on 10mm right after trading, USD", jtd, "5,785,899")
    # recovery assumption: rebuild the hazards at R = 30% from the same par spreads (card fi-cds-recovery-sensitivity)
    curve30 = bootstrap(quotes, 0.30, r)
    rp30, pr30 = legs_exact(curve30, r, 5.0)
    up30 = notional * (0.70 * pr30 - 0.0100 * rp30)
    q("fi-cds-recovery-sensitivity", "5y hazard at R = 30%, %", 100 * curve30.hazards[2], "2.8801")
    q("fi-cds-recovery-sensitivity", "upfront on 10mm at R = 30%, USD", up30, "215,677")
    q("fi-cds-recovery-sensitivity", "upfront change from R = 40% to 30%, USD", up30 - v0, "1,576")
    q("fi-cds-recovery-sensitivity", "JTD on 10mm at R = 30%, USD", 0.70 * notional - up30, "6,784,323")
    q("fi-cds-recovery-sensitivity", "JTD change from R = 40% to 30%, USD", (0.70 * notional - up30) - jtd, "998,424")

    # --- Example 5: standard contract dates and coupons, ISDA Standard CDS Examples Table 1
    roll = [date(2008, 12, 20), date(2009, 3, 20), date(2009, 6, 20), date(2009, 9, 20), date(2009, 12, 20), date(2010, 3, 20)]
    pay = [following(d) for d in roll]
    assert pay[1:] == [date(2009, 3, 20), date(2009, 6, 22), date(2009, 9, 21), date(2009, 12, 21), date(2010, 3, 22)]
    days = []
    for i in range(1, 6):
        start = pay[i - 1]
        end = roll[5] + timedelta(days=1) if i == 5 else pay[i]  # last period includes the unadjusted maturity date
        days.append((end - start).days)
    for i, txt in enumerate(("88", "94", "91", "91", "90")):
        q("fi-cds-std-coupon-dates", f"accrual days in period {i + 1}", days[i], txt)
    for i, txt in enumerate(("88,000", "94,000", "91,000", "91,000", "90,000")):
        q("fi-cds-std-coupon-dates", f"coupon {i + 1} on 36mm at 100bp, USD", 36e6 * 0.01 * days[i] / 360, txt)
    q("fi-cds-std-coupon-dates", "total coupon days", sum(days), "454")
    q("fi-cds-std-coupon-dates", "2Q09 coupon on 10mm at 100bp, USD", 10e6 * 0.01 * days[1] / 360, "26,111")
    q(
        "fi-cds-std-coupon-dates",
        "final coupon for a 20Jun09 maturity, USD",
        10e6 * 0.01 * ((date(2009, 6, 21) - date(2009, 3, 20)).days) / 360,
        "25,833",
    )
    riskless = (date(2009, 2, 20) - date(2008, 12, 22)).days + 1
    q("fi-cds-accrued-rebate", "riskless accrual days 22Dec08 to 20Feb09 inclusive", riskless, "61")
    q("fi-cds-accrued-rebate", "2 points upfront on 36mm, USD", 0.02 * 36e6, "720,000")
    q("fi-cds-accrued-rebate", "accrued paid by the seller, USD", 36e6 * 0.01 * riskless / 360, "61,000")
    q("fi-cds-accrued-rebate", "net paid by the buyer for 2 points upfront, USD", 0.02 * 36e6 - 36e6 * 0.01 * riskless / 360, "659,000")

    # --- Example 6: quoted (conventional) spread to upfront with a single flat hazard (card fi-cds-conventional-spread)
    def flat_from_spread(s: float) -> HazardCurve:
        return bootstrap([(5.0, s)], rec, r)

    for quoted, coupon, txt in ((0.0198, 0.0100, "4.0864"), (0.0800, 0.0500, "9.9968")):
        fc = flat_from_spread(quoted)
        rp, _ = legs_exact(fc, r, 5.0)
        q("fi-cds-conventional-spread", f"5y upfront at quoted {quoted:.2%} with coupon {coupon:.0%}, %", 100 * (quoted - coupon) * rp, txt)
    flat_150 = flat_from_spread(0.0150)
    q("fi-cds-conventional-spread", "flat-curve upfront at 150bp quoted, %", 100 * 0.005 * legs_exact(flat_150, r, 5.0)[0], "2.1244")

    # --- Example 7: hedging a distressed bond's jump to default (card fi-cds-jtd-bond-hedge)
    q("fi-cds-jtd-bond-hedge", "bond loss on default, USD mm", 50 * (0.70 - 0.40), "15")
    q("fi-cds-jtd-bond-hedge", "CDS notional to hedge, USD mm", 50 * (0.70 - 0.40) / 0.60, "25")

    # --- Example 8: CDS-bond basis carry (card fi-credit-cds-negative-basis)
    q("fi-credit-cds-negative-basis", "basis = CDS - bond spread, bp", 150 - 180, "-30")
    q("fi-credit-cds-negative-basis", "carry = bond spread - CDS - funding spread, bp", 180 - 150 - 20, "10")

    # --- Example 9: Merton (cards fi-credit-cds-merton-shortcoming, fi-cds-merton-numbers)
    e5, d5, pd5, s5 = merton(100.0, 60.0, 0.25, 0.04, 5.0)
    q("fi-cds-merton-numbers", "equity value", e5, "52.7205")
    q("fi-cds-merton-numbers", "debt value", d5, "47.2795")
    q("fi-cds-merton-numbers", "risk-neutral 5y default probability, %", 100 * pd5, "16.06")
    q("fi-cds-merton-numbers", "5y credit spread, bp", 1e4 * s5, "77")
    for t, txt in ((1.0, "15.9"), (0.25, "0.022")):
        q("fi-credit-cds-merton-shortcoming", f"credit spread at T = {t:g}y, bp", 1e4 * merton(100.0, 60.0, 0.25, 0.04, t)[3], txt)

    print("All note 06 checks passed.")


if __name__ == "__main__":
    main()
