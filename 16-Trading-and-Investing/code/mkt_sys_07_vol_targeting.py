"""Volatility targeting and dynamic leverage: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/60-Systems/07-Volatility-Targeting-and-Dynamic-Leverage.md`.
Independent routes used here:
- exposure multipliers in exact rational arithmetic;
- the Garman-Klass example with ``math.log`` and again from log prices via ``math.log1p``;
- range-estimator efficiency: Parkinson exactly from the Brownian range moments E[R^2] = 4 ln 2 and
  E[R^4] = 9 zeta(3) (zeta(3) summed as a series), Garman-Klass and Rogers-Satchell by seeded simulation of
  Brownian days whose per-step high and low each follow the exact Brownian-bridge law (drawn separately, which
  departs from their joint law only when one step spans most of the day's range), the simulator validated
  against the exact Parkinson efficiency, every tolerance 4 computed standard errors;
- the two-regime volatility-management example: Sharpe ratios and kurtosis exactly from Gaussian moments
  per regime, checked by seeded simulation, and the effect isolated by changing only the risk-return link.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_sys_07_vol_targeting.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

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
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (expected {expected}, tolerance {tol:.3g})")


def multipliers() -> None:
    print("Example 1 and the regime diagram: exposure multipliers (cards mkt-sys-193, mkt-sys-196)")

    def k(target: Fraction, vol: Fraction, cap: Fraction) -> Fraction:
        return min(cap, target / vol)

    big = Fraction(10**6)
    exact("diagram calm, 10% / 8%", Fraction(10, 8), Fraction(5, 4))
    exact("diagram crisis, 10% / 40%", Fraction(10, 40), Fraction(1, 4))
    cap = Fraction(5, 2)
    for vol, mult, exposure in ((6, Fraction(2), 20), (16, Fraction(3, 4), Fraction(15, 2)), (48, Fraction(1, 4), Fraction(5, 2))):
        m = k(Fraction(12), Fraction(vol), cap)
        exact(f"k at {vol}% realized vol", m, mult)
        exact(f"gross exposure at {vol}% ($M)", m * 10 * big / big, exposure)
    exact("uncapped k at 4% vol for a 12% target", Fraction(12, 4), Fraction(3))


def garman_klass_example() -> None:
    print("Example 2: Garman-Klass on one day (card mkt-sys-198)")
    o, h, lo, c = 100.0, 104.0, 98.0, 102.0
    hl = math.log(h / lo)
    co = math.log(c / o)
    assert abs(hl - (math.log1p(4 / 100) - math.log1p(-2 / 100))) < 1e-15
    assert abs(co - math.log1p(2 / 100)) < 1e-15
    approx("H/L", h / lo, 1.06122, 5)
    approx("H/L (three decimals)", h / lo, 1.061, 3)
    approx("ln(H/L)", hl, 0.05942, 5)
    approx("ln(C/O)", co, 0.01980, 5)
    approx("ln(H/L)^2", hl * hl, 0.003531, 6)
    approx("ln(C/O)^2", co * co, 0.0003921, 7)
    approx("2 ln 2 - 1", 2 * math.log(2) - 1, 0.38629, 5)
    approx("0.5 ln(H/L)^2", 0.5 * hl * hl, 0.0017656, 7)
    approx("(2 ln 2 - 1) ln(C/O)^2", (2 * math.log(2) - 1) * co * co, 0.0001515, 7)
    gk = 0.5 * hl * hl - (2 * math.log(2) - 1) * co * co
    approx("GK variance", gk, 0.0016141, 7)
    approx("GK daily vol", math.sqrt(gk), 0.04018, 5)
    approx("GK daily vol (percent)", 100 * math.sqrt(gk), 4.02, 2)
    approx("sqrt(252)", math.sqrt(252), 15.8745, 4)
    approx("GK annualized vol (percent)", 100 * math.sqrt(gk * 252), 63.8, 1)
    approx("close-to-close move (percent)", 100 * (c / o - 1), 2.0, 1)


def range_efficiency(rng: np.random.Generator) -> None:
    print("Range-estimator efficiency for driftless Brownian motion (estimator table, cards mkt-sys-197, mkt-sys-198, mkt-sys-206)")
    zeta3 = sum(1.0 / n**3 for n in range(1, 200_000)) + 1 / (2 * 200_000**2)
    approx("zeta(3)", zeta3, 1.2020569, 7)
    var_park = 9 * zeta3 / (4 * math.log(2)) ** 2 - 1
    approx("Var of Parkinson (sigma^4 units)", var_park, 0.4073, 4)
    eff_park = 2 / var_park
    approx("Parkinson efficiency, exact", eff_park, 4.91, 2)

    days, steps = 200_000, 64
    dt = 1.0 / steps
    park, gk, rs, cc = [], [], [], []
    for _ in range(10):
        n = days // 10
        inc = rng.standard_normal((n, steps)) * math.sqrt(dt)
        path = np.concatenate([np.zeros((n, 1)), np.cumsum(inc, axis=1)], axis=1)
        a, b = path[:, :-1], path[:, 1:]
        d2 = (b - a) ** 2
        mx = 0.5 * (a + b + np.sqrt(d2 - 2 * dt * np.log(rng.random((n, steps)))))
        mn = 0.5 * (a + b - np.sqrt(d2 - 2 * dt * np.log(rng.random((n, steps)))))
        hi, low, close = mx.max(axis=1), mn.min(axis=1), path[:, -1]
        park.append((hi - low) ** 2 / (4 * math.log(2)))
        gk.append(0.5 * (hi - low) ** 2 - (2 * math.log(2) - 1) * close**2)
        rs.append(hi * (hi - close) + low * (low - close))
        cc.append(close**2)
    est = {name: np.concatenate(v) for name, v in (("park", park), ("gk", gk), ("rs", rs), ("cc", cc))}
    for name in est:
        x = est[name]
        assert abs(x.mean() - 1.0) <= 4 * x.std(ddof=1) / math.sqrt(len(x)), (name, x.mean())
    effs = {}
    for name in ("park", "gk", "rs"):
        x = est[name]
        v = float(x.var(ddof=1))
        # Standard error of a sample variance: sqrt((m4 - v^2)/n); propagate to 2/v.
        m4 = float(np.mean((x - x.mean()) ** 4))
        se_v = math.sqrt((m4 - v * v) / len(x))
        effs[name] = (2 / v, 2 / v * se_v / v)
    e, se = effs["park"]
    simulated("Parkinson efficiency, simulated (validates the simulator)", e, eff_park, 4 * se)
    e, se = effs["gk"]
    simulated("Garman-Klass efficiency, simulated", e, 7.4, 4 * se)
    e, se = effs["rs"]
    simulated("Rogers-Satchell efficiency, simulated", e, 6.0, 4 * se)
    print(f"    (seed {SEED}, {days} days of {steps} bridge steps; tolerance 4 standard errors)")


def gaussian_moments(a: float, b: float) -> tuple[float, float, float, float]:
    return a, a * a + b * b, a**3 + 3 * a * b * b, a**4 + 6 * a * a * b * b + 3 * b**4


def mixture_stats(regimes: list[tuple[float, float, float]]) -> tuple[float, float]:
    """Exact Sharpe (per period) and kurtosis of an equal-probability mixture of N(mean, sd) regimes."""
    m = [0.0, 0.0, 0.0, 0.0]
    for p, mean, sd in regimes:
        for i, v in enumerate(gaussian_moments(mean, sd)):
            m[i] += p * v
    mu, m2, m3, m4 = m
    var = m2 - mu * mu
    c4 = m4 - 4 * mu * m3 + 6 * mu * mu * m2 - 3 * mu**4
    return mu / math.sqrt(var), c4 / var**2


def vol_management(rng: np.random.Generator) -> None:
    print("Example 3: two-regime volatility management (cards mkt-sys-195, mkt-sys-205, mkt-sys-265)")
    mu = 0.005
    vols = (0.02, 0.06)

    def run(mean_of, weight_of) -> tuple[float, float]:
        regimes = [(0.5, weight_of(s) * mean_of(s), weight_of(s) * s) for s in vols]
        return mixture_stats(regimes)

    flat = lambda s: mu  # noqa: E731
    sr_u, k_u = run(flat, lambda s: 1.0)
    sr_v, k_v = run(flat, lambda s: 1 / s)
    sr_m, k_m = run(flat, lambda s: 1 / s**2)
    approx("unmanaged annualized Sharpe", sr_u * math.sqrt(12), 0.39, 2)
    approx("vol-targeted (1/sigma) annualized Sharpe", sr_v * math.sqrt(12), 0.58, 2)
    approx("variance-managed (1/sigma^2) annualized Sharpe", sr_m * math.sqrt(12), 0.64, 2)
    approx("unmanaged kurtosis", k_u, 4.92, 2)
    approx("vol-targeted kurtosis", k_v, 3.00, 2)
    # Simulation check of the unmanaged and variance-managed Sharpe ratios.
    n = 2_000_000
    sig = np.where(rng.random(n) < 0.5, vols[0], vols[1])
    r = mu + sig * rng.standard_normal(n)
    for w, sr_exact, name in ((np.ones(n), sr_u, "unmanaged"), (1 / sig**2, sr_m, "variance-managed")):
        x = w * r
        sd = x.std(ddof=1)
        sr_sim = x.mean() / sd
        z = (x - x.mean()) / sd
        skew, kurt = float(np.mean(z**3)), float(np.mean(z**4))
        se = math.sqrt((1 - skew * sr_sim + (kurt - 1) / 4 * sr_sim**2) / n)
        simulated(f"{name} monthly Sharpe, simulated", float(sr_sim), sr_exact, 4 * se)
    # Change one thing: make the expected return proportional to variance (a risk-return trade-off).
    a = mu / (0.5 * (vols[0] ** 2 + vols[1] ** 2))
    prop = lambda s: a * s * s  # noqa: E731
    sr_u2, _ = run(prop, lambda s: 1.0)
    sr_m2, _ = run(prop, lambda s: 1 / s**2)
    approx("with mean proportional to variance: unmanaged annualized Sharpe", sr_u2 * math.sqrt(12), 0.39, 2)
    approx("with mean proportional to variance: variance-managed annualized Sharpe", sr_m2 * math.sqrt(12), 0.23, 2)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    multipliers()
    garman_klass_example()
    range_efficiency(rng)
    vol_management(rng)
    print("all volatility-targeting numbers check out")
