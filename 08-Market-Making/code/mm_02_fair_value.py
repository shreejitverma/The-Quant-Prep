"""Fair value and theoretical pricing: every weighted mid, blend, carry, ETF and decay number in the note.

Backs every number in `08-Market-Making/02-Fair-Value-and-Theoretical-Pricing.md`.
Independent routes used here:
- weighted mids, the futures-implied move and the ETF basket in exact `fractions.Fraction` arithmetic;
- inverse-variance weights by golden-section minimisation of the blend variance over w, and the blended error
  standard deviation by a seeded simulation of the two estimates;
- the cost-of-carry futures price by an exact rational Taylor series of exp, checked against math.exp;
- the decayed signal by solving x^5 = 2^-2 with bisection, never by evaluating 2 ** -0.4.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 08-Market-Making/code/mm_02_fair_value.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction as F

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.5f} (quoted {expected}, tolerance {tol:.5f})")


def section_weighted_mid() -> None:
    print("Example 1: weighted mid (cards mm-fv-weighted-mid-formula, mm-fv-weighted-mid-example)")
    pb, pa, qb, qa = F("50.00"), F("50.01"), 800, 200
    imb = F(qb, qb + qa)
    exact("I", imb, F(4, 5))
    pw = pb * F(qa, qb + qa) + pa * F(qb, qb + qa)
    exact("weighted mid", pw, F("50.008"))
    exact("mid", (pa + pb) / 2, F("50.005"))
    exact("m + s (I - 1/2)", (pa + pb) / 2 + (pa - pb) * (imb - F(1, 2)), pw)
    exact("ask above theo, cents", (pa - pw) * 100, F(2, 10))
    exact("bid below theo, cents", (pw - pb) * 100, F(8, 10))


def section_futures_lead() -> None:
    print("Example 2: futures lead (card mm-fv-futures-implied-move)")
    ret = F(10, 5000)
    exact("futures return", ret, F(2, 1000))
    exact("implied stock move, dollars", 200 * F(12, 10) * ret, F("0.48"))


def golden_min(f, lo: float, hi: float) -> float:
    invphi = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = lo, hi
    c, d = b - invphi * (b - a), a + invphi * (b - a)
    for _ in range(200):
        if f(c) < f(d):
            b, d = d, c
            c = b - invphi * (b - a)
        else:
            a, c = c, d
            d = a + invphi * (b - a)
    return 0.5 * (a + b)


def section_blend(rng: np.random.Generator) -> None:
    print("Example 3: blending two estimates (cards mm-fv-inverse-variance-blend, mm-fv-stale-quote-edge)")
    sa, sb = 0.02, 0.01
    w_a = golden_min(lambda w: w * w * sa * sa + (1 - w) ** 2 * sb * sb, 0.0, 1.0)
    approx("w_A minimising blend variance", w_a, 0.2, 6)
    approx("w_B", 1 - w_a, 0.8, 6)
    exact("1/0.02^2 and 1/0.01^2", (1 / F("0.02") ** 2, 1 / F("0.01") ** 2), (2500, 10000))
    exact("their sum", 1 / F("0.02") ** 2 + 1 / F("0.01") ** 2, 12500)
    theo = F(1, 5) * F("100.004") + F(4, 5) * F("100.012")
    exact("theo", theo, F("100.0104"))
    sd = math.sqrt(w_a**2 * sa**2 + (1 - w_a) ** 2 * sb**2)
    approx("blend error sd", sd, 0.0089, 4)
    n = 1_000_000
    blend = w_a * rng.normal(0, sa, n) + (1 - w_a) * rng.normal(0, sb, n)
    simulated("blend error sd, simulated", float(blend.std(ddof=1)), 0.0089, 5 * 0.0089 / math.sqrt(2 * n) + 5e-5)
    exact("ask at 100.01 relative to theo", F("100.01") - theo, F("-0.0004"))
    exact("bid edge", theo - F("99.99"), F("0.0204"))


def exp_series(x: F, terms: int = 30) -> F:
    total, term = F(1), F(1)
    for j in range(1, terms):
        term = term * x / j
        total += term
    return total


def section_carry() -> None:
    print("Example 4: cost-of-carry theo (card mm-fv-carry-futures-price)")
    exponent = (F("0.05") - F("0.015")) * F("0.25")
    exact("(r - q) T", exponent, F("0.00875"))
    f = 5000 * exp_series(exponent)
    assert abs(float(f) - 5000 * math.exp(0.00875)) < 1e-9
    approx("F", float(f), 5043.94, 2)


def section_etf() -> None:
    print("Example 5: ETF indicative value (card mm-fv-etf-indicative-value)")
    weights, moves = [F(1, 2), F(3, 10), F(1, 5)], [F("0.003"), F("-0.002"), F("0.005")]
    parts = [w * m for w, m in zip(weights, moves, strict=True)]
    exact("contributions", parts, [F("0.0015"), F("-0.0006"), F("0.0010")])
    ret = sum(parts)
    exact("basket return", ret, F("0.0019"))
    exact("indicative value", 80 * (1 + ret), F("80.152"))


def section_decay() -> None:
    print("Example 6: decaying a signal (card mm-fv-signal-half-life)")
    lo, hi = 0.0, 1.0
    for _ in range(200):  # x = 2^(-2/5) solves x^5 = 1/4
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if mid**5 < 0.25 else (lo, mid)
    factor = 0.5 * (lo + hi)
    exact("age / half-life", F(200, 500), F(2, 5))
    approx("remaining contribution, ticks", 2 * factor, 1.52, 2)
    approx("remaining contribution, ticks (3 dp)", 2 * factor, 1.516, 3)


if __name__ == "__main__":
    generator = np.random.default_rng(SEED)
    section_weighted_mid()
    section_futures_lead()
    section_blend(generator)
    section_carry()
    section_etf()
    section_decay()
