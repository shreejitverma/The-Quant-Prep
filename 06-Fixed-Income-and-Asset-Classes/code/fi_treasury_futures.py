"""Treasury futures: CME conversion factors, invoice, basis, carry, implied repo, CTD and hedge ratios.

Backs every number in `06-Fixed-Income-and-Asset-Classes/16-Treasury-Futures-and-the-Basis.md`.
The conversion factor follows CME's published formula (CME Group, "Calculating U.S. Treasury Futures
Conversion Factors") and is checked two independent ways: against the five worked examples CME
publishes in that document, and against a cash-flow-by-cash-flow price at a 6% yield of a bond with the
rounded maturity. Bond prices use the street (SIA) price-yield formula with ACT/ACT accrual, checked
by re-solving each yield from its price. Net basis and implied repo rate are checked to agree on the
cheapest-to-deliver. The deliverable bonds, yields, futures price and repo rate are hypothetical inputs.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_treasury_futures.py`.
"""

from __future__ import annotations

import datetime as dt
import math

QUOTED: list[str] = []
QUARTER_ROUNDING = {"TY", "TN", "US", "UB", "TWE"}  # CME: 10y, Ultra 10y, Bond, Ultra Bond, 20y
MONTH_ROUNDING = {"TU", "3YR", "FV"}


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def months_between(start: dt.date, end: dt.date) -> int:
    """Whole months from start to end (the day of month counts: 1 Dec to 31 Oct is 10 months)."""
    m = (end.year - start.year) * 12 + (end.month - start.month)
    if end.day < start.day:
        m -= 1
    return m


def cme_cf_terms(coupon: float, maturity: dt.date, delivery_month_start: dt.date, contract: str) -> dict[str, float]:
    """CME conversion factor: factor = a [coupon/2 + c + d] - b, rounded to 4 decimals."""
    coupon = math.floor(coupon * 800.0 + 0.5) / 800.0  # nearest 1/8 of one percent, ties up
    total = months_between(delivery_month_start, maturity)
    n, z = divmod(total, 12)
    if contract in QUARTER_ROUNDING:
        z = 3 * (z // 3)
        v = z if z < 7 else 3
    elif contract in MONTH_ROUNDING:
        v = z if z < 7 else z - 6
    else:
        raise ValueError(contract)
    a = 1.03 ** (-v / 6.0)
    b = coupon / 2.0 * (6 - v) / 6.0
    c = 1.03 ** (-2 * n) if z < 7 else 1.03 ** (-(2 * n + 1))
    d = coupon / 0.06 * (1.0 - c)
    raw = a * (coupon / 2.0 + c + d) - b
    return {"n": n, "z": z, "v": v, "a": a, "b": b, "c": c, "d": d, "raw": raw, "factor": round(raw, 4)}


def cf_by_cash_flows(coupon: float, n: int, z: int, v: int) -> float:
    """Independent check: price per 1 of par at 3% per half-year, enumerating every cash flow."""
    m = 2 * n if z < 7 else 2 * n + 1  # half-years from the first coupon to maturity
    pv = sum((coupon / 2.0) / 1.03 ** (v / 6.0 + j) for j in range(m + 1))
    pv += 1.0 / 1.03 ** (v / 6.0 + m)
    return pv - coupon / 2.0 * (6 - v) / 6.0  # clean: subtract accrued since the previous coupon


def add_months(d: dt.date, months: int) -> dt.date:
    idx = d.year * 12 + d.month - 1 + months
    return dt.date(idx // 12, idx % 12 + 1, d.day)


def coupon_dates(maturity: dt.date, settle: dt.date) -> tuple[dt.date, dt.date]:
    """Previous and next semiannual coupon dates around settle (15th-of-month bonds)."""
    nxt = maturity
    while add_months(nxt, -6) > settle:
        nxt = add_months(nxt, -6)
    return add_months(nxt, -6), nxt


def accrued(coupon: float, maturity: dt.date, settle: dt.date) -> float:
    prev, nxt = coupon_dates(maturity, settle)
    return 100.0 * coupon / 2.0 * (settle - prev).days / (nxt - prev).days


def price_from_yield(coupon: float, maturity: dt.date, settle: dt.date, y: float) -> tuple[float, float]:
    """Street convention: semiannual compounding, fractional first period on ACT/ACT. Returns (clean, dirty)."""
    prev, nxt = coupon_dates(maturity, settle)
    w = (nxt - settle).days / (nxt - prev).days
    k = 0
    d = nxt
    dirty = 0.0
    while d <= maturity:
        cf = 100.0 * coupon / 2.0 + (100.0 if d == maturity else 0.0)
        dirty += cf / (1.0 + y / 2.0) ** (w + k)
        k += 1
        d = add_months(d, 6)
    return dirty - accrued(coupon, maturity, settle), dirty


def yield_from_price(coupon: float, maturity: dt.date, settle: dt.date, clean: float) -> float:
    lo, hi = -0.05, 0.30
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if price_from_yield(coupon, maturity, settle, mid)[0] > clean:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def example_cme_published() -> None:
    print("  1. CME conversion factor formula against CME's five published examples")
    cases = [
        ("TU", 0.015, dt.date(2010, 10, 31), dt.date(2008, 12, 1), 0.9229),
        ("3YR", 0.01125, dt.date(2012, 1, 15), dt.date(2009, 3, 1), 0.8747),
        ("FV", 0.0275, dt.date(2013, 10, 31), dt.date(2008, 12, 1), 0.8653),
        ("TY", 0.0375, dt.date(2018, 11, 15), dt.date(2008, 12, 1), 0.8357),
        ("US", 0.045, dt.date(2038, 5, 15), dt.date(2008, 12, 1), 0.7943),
    ]
    for contract, cpn, mat, start, published in cases:
        t = cme_cf_terms(cpn, mat, start, contract)
        enumerated = cf_by_cash_flows(cpn, int(t["n"]), int(t["z"]), int(t["v"]))
        assert abs(enumerated - t["raw"]) < 1e-12
        quoted(f"{contract} {cpn * 100:.3f}% {mat.isoformat()} factor (CME publishes {published})", t["factor"], published, 4)
    ty = cme_cf_terms(0.0375, dt.date(2018, 11, 15), dt.date(2008, 12, 1), "TY")
    quoted("TY example: n", ty["n"], 9.0, 0)
    quoted("TY example: z", ty["z"], 9.0, 0)
    quoted("TY example: v", ty["v"], 3.0, 0)
    quoted("TY example: unrounded factor", ty["raw"], 0.835651, 6)
    six = cme_cf_terms(0.06, dt.date(2033, 8, 15), dt.date(2026, 12, 1), "TY")
    quoted("6% coupon factor", six["factor"], 1.0, 4)


BASKET = {
    "A": (0.0400, dt.date(2033, 8, 15), 0.0405),
    "B": (0.0450, dt.date(2034, 2, 15), 0.0412),
    "C": (0.0375, dt.date(2034, 8, 15), 0.0415),
}
SETTLE, DELIVERY, DM_START = dt.date(2026, 10, 1), dt.date(2026, 12, 31), dt.date(2026, 12, 1)
REPO = 0.0400


def basket_analytics(shift: float, futures: float) -> dict[str, dict[str, float]]:
    out = {}
    days = (DELIVERY - SETTLE).days
    for name, (cpn, mat, y) in BASKET.items():
        cf = cme_cf_terms(cpn, mat, DM_START, "TY")["factor"]
        clean, dirty = price_from_yield(cpn, mat, SETTLE, y + shift)
        ai0, ai1 = accrued(cpn, mat, SETTLE), accrued(cpn, mat, DELIVERY)
        carry = (ai1 - ai0) - dirty * REPO * days / 360.0
        gross = clean - futures * cf
        net = gross - carry
        invoice = futures * cf + ai1
        irr = (invoice - dirty) / dirty * 360.0 / days
        fwd_clean = dirty * (1.0 + REPO * days / 360.0) - ai1
        out[name] = {
            "cf": cf,
            "clean": clean,
            "dirty": dirty,
            "ai0": ai0,
            "ai1": ai1,
            "carry": carry,
            "gross": gross,
            "net": net,
            "invoice": invoice,
            "irr": irr,
            "fair": fwd_clean / cf,
        }
    return out


def example_basket() -> None:
    print("  2. A hypothetical TY (ZN) December 2026 basket: basis, carry, net basis, IRR")
    days = (DELIVERY - SETTLE).days
    quoted("days from settlement to delivery", float(days), 91.0, 0)
    for _cpn, mat, _y in BASKET.values():
        total = months_between(DM_START, mat)
        assert 78 <= 3 * ((total % 12) // 3) + 12 * (total // 12) <= 93  # 6y6m to 7y9m after quarter rounding
    probe = basket_analytics(0.0, 100.0)
    fair_ctd = min(v["fair"] for v in probe.values())
    futures = math.floor((fair_ctd - 0.10) * 64.0) / 64.0  # 0.10 points of option value, then down to 1/64
    quoted("futures price used (points)", futures, 111.484375, 6)
    res = basket_analytics(0.0, futures)
    expected = {
        "A": dict(cf=0.8937, clean=99.6989, ai0=0.5109, ai1=1.5000, carry=-0.0241, gross=0.0653, net=0.0894, irr=3.6472),
        "B": dict(cf=0.9153, clean=102.3906, ai0=0.5747, ai1=1.6875, carry=0.0717, gross=0.3490, net=0.2773, irr=2.9347),
        "C": dict(cf=0.8657, clean=97.3334, ai0=0.4789, ai1=1.4062, carry=-0.0617, gross=0.8213, net=0.8830, irr=0.4286),
    }
    for name, e in expected.items():
        r = res[name]
        yld = yield_from_price(BASKET[name][0], BASKET[name][1], SETTLE, r["clean"])
        assert abs(yld - BASKET[name][2]) < 1e-10
        quoted(f"{name} conversion factor", r["cf"], e["cf"], 4)
        quoted(f"{name} clean price", r["clean"], e["clean"], 4)
        quoted(f"{name} accrued at settlement", r["ai0"], e["ai0"], 4)
        quoted(f"{name} accrued at delivery", r["ai1"], e["ai1"], 4)
        quoted(f"{name} carry to delivery", r["carry"], e["carry"], 4)
        quoted(f"{name} gross basis", r["gross"], e["gross"], 4)
        quoted(f"{name} net basis", r["net"], e["net"], 4)
        quoted(f"{name} implied repo (%)", r["irr"] * 100, e["irr"], 4)
    ctd_net = min(res, key=lambda k: res[k]["net"])
    ctd_irr = max(res, key=lambda k: res[k]["irr"])
    assert ctd_net == ctd_irr == "A"
    quoted("CTD net basis as futures points (net / CF)", res["A"]["net"] / res["A"]["cf"], 0.1000, 4)
    quoted("CTD invoice price per 100", res["A"]["invoice"], 101.1336, 4)
    invoice_amount = round(1000.0 * futures * res["A"]["cf"], 2) + 1000.0 * res["A"]["ai1"]
    quoted("CTD invoice amount per contract (USD)", invoice_amount, 101_133.59, 2)
    quoted("CTD implied repo minus repo (bp)", (res["A"]["irr"] - REPO) * 1e4, -35.28, 2)


def example_ctd_switch() -> None:
    print("  3. CTD and the 6% rule: shift all yields")
    for shift, expect in ((0.0, "A"), (-0.02, "A"), (0.03, "C")):
        r = basket_analytics(shift, 100.0)
        ctd = min(r, key=lambda k: r[k]["clean"] / r[k]["cf"])
        assert ctd == expect, (shift, ctd)
    low = basket_analytics(-0.02, 100.0)
    quoted("price/CF at yields -200 bp, A", low["A"]["clean"] / low["A"]["cf"], 125.8124, 4)
    quoted("price/CF at yields -200 bp, B", low["B"]["clean"] / low["B"]["cf"], 126.9118, 4)
    quoted("price/CF at yields -200 bp, C", low["C"]["clean"] / low["C"]["cf"], 128.8307, 4)
    high = basket_analytics(0.03, 100.0)
    quoted("price/CF at yields +300 bp, A", high["A"]["clean"] / high["A"]["cf"], 93.5485, 4)
    quoted("price/CF at yields +300 bp, B", high["B"]["clean"] / high["B"]["cf"], 93.0453, 4)
    quoted("price/CF at yields +300 bp, C", high["C"]["clean"] / high["C"]["cf"], 92.1721, 4)


def example_hedge() -> None:
    print("  4. Futures DV01 and the CF hedge ratio")
    cpn, mat, y = BASKET["A"]
    up = price_from_yield(cpn, mat, SETTLE, y + 1e-4)[1]
    dn = price_from_yield(cpn, mat, SETTLE, y - 1e-4)[1]
    dv01_ctd = (dn - up) / 2.0 * 1000.0  # USD per bp per 100,000 face
    cf = cme_cf_terms(cpn, mat, DM_START, "TY")["factor"]
    quoted("CTD DV01 per 100,000 face (USD)", dv01_ctd, 59.37, 2)
    quoted("futures DV01 per contract, DV01_CTD / CF (USD)", dv01_ctd / cf, 66.44, 2)
    quoted("contracts to hedge 10mm face of the CTD", 10_000_000 / 100_000 * cf, 89.37, 2)


def main() -> None:
    print("=== fi_treasury_futures: conversion factors, basis, IRR, CTD ===")
    example_cme_published()
    example_basket()
    example_ctd_switch()
    example_hedge()
    print(f"\nVerified {len(QUOTED)} Treasury futures figures.")


if __name__ == "__main__":
    main()
