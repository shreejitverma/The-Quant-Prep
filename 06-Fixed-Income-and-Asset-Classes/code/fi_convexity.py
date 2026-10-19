"""Convexity adjustments: futures versus forwards, CMS, in-arrears and quanto.

Backs every number in `06-Fixed-Income-and-Asset-Classes/17-Convexity-Adjustments.md`.
Independent checks: the Hull-White futures-forward closed form is compared with a direct numerical
integration of the HJM no-arbitrage drift; the CMS adjustment from static swaption replication
(Carr-Madan with Black prices) is compared with direct integration of the payoff against the lognormal
density, and both with the linear approximation; the in-arrears adjustment is compared with a seeded
Monte Carlo under the payment-delay measure; the quanto adjustment is compared with a seeded Monte Carlo
that applies the measure change explicitly.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_convexity.py`.
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def simpson(fun: Callable[[float], float], a: float, b: float, n: int) -> float:
    h = (b - a) / n
    total = fun(a) + fun(b)
    for k in range(1, n):
        total += (4.0 if k % 2 else 2.0) * fun(a + k * h)
    return total * h / 3.0


def hull_white_futures_adjustment(sigma: float, a: float, t1: float, t2: float) -> float:
    """Hull's closed form for the futures minus forward rate (continuously compounded)."""
    b12 = (1.0 - math.exp(-a * (t2 - t1))) / a
    b01 = (1.0 - math.exp(-a * t1)) / a
    return b12 / (t2 - t1) * (b12 * (1.0 - math.exp(-2.0 * a * t1)) + 2.0 * a * b01 * b01) * sigma * sigma / (4.0 * a)


def hjm_futures_adjustment(sigma: float, a: float, t1: float, t2: float, n: int = 200) -> float:
    """Independent: (1/tau) int_{t1}^{t2} int_0^{t1} sf(u,s) int_u^s sf(u,v) dv du ds with sf = sigma e^{-a(s-u)}.

    The inner v-integral is done numerically too, so nothing here uses the Hull-White bond formula.
    """

    def sf(u: float, s: float) -> float:
        return sigma * math.exp(-a * (s - u))

    def drift(s: float) -> float:
        return simpson(lambda u: sf(u, s) * simpson(lambda v: sf(u, v), u, s, 20), 0.0, t1, n)

    return simpson(drift, t1, t2, 10) / (t2 - t1)


def example_futures() -> None:
    print("  1. Futures versus forward rates")
    sigma = 0.012
    quoted("Ho-Lee, T1 = 2, T2 = 2.25 (bp)", 0.5 * sigma**2 * 2.0 * 2.25 * 1e4, 3.24, 2)
    quoted("fair forward from a 4.5000% futures rate (%)", (0.045 - 0.5 * sigma**2 * 2.0 * 2.25) * 100, 4.4676, 4)
    quoted("Ho-Lee, T1 = 5, T2 = 5.25 (bp)", 0.5 * sigma**2 * 5.0 * 5.25 * 1e4, 18.9, 1)
    hw = hull_white_futures_adjustment(sigma, 0.03, 5.0, 5.25)
    hjm = hjm_futures_adjustment(sigma, 0.03, 5.0, 5.25)
    assert abs(hw - hjm) < 1e-9, (hw, hjm)
    quoted("Hull-White a = 0.03, T1 = 5, T2 = 5.25 (bp)", hw * 1e4, 16.2, 1)
    quoted("Hull-White closed form, 4 decimals (bp)", hw * 1e4, 16.2355, 4)
    quoted("HJM drift integral, 4 decimals (bp)", hjm * 1e4, 16.2355, 4)
    ho_lee_limit = hull_white_futures_adjustment(sigma, 1e-7, 5.0, 5.25)
    assert abs(ho_lee_limit - 0.5 * sigma**2 * 5.0 * 5.25) < 1e-9
    for t1, exp in ((1.0, 0.87), (10.0, 54.88)):
        quoted(f"Hull-White a = 0.03, T1 = {t1:.0f} (bp)", hull_white_futures_adjustment(sigma, 0.03, t1, t1 + 0.25) * 1e4, exp, 2)
    quoted("Ho-Lee, T1 = 10 (bp)", 0.5 * sigma**2 * 10.0 * 10.25 * 1e4, 73.80, 2)


def annuity(s: float, n: int = 10) -> float:
    return sum((1.0 + s) ** (-i) for i in range(1, n + 1))


def black_call(f: float, k: float, vol: float, t: float) -> float:
    sd = vol * math.sqrt(t)
    d1 = (math.log(f / k) + 0.5 * sd * sd) / sd
    return f * norm_cdf(d1) - k * norm_cdf(d1 - sd)


def black_put(f: float, k: float, vol: float, t: float) -> float:
    return black_call(f, k, vol, t) - (f - k)


def example_cms() -> None:
    print("  2. CMS: 10y swap rate fixing and paid in 5y")
    s0, vol, t = 0.04, 0.20, 5.0
    a0 = annuity(s0)
    a_prime = -sum(i * (1.0 + s0) ** (-(i + 1)) for i in range(1, 11))
    quoted("(1.04)^-10", 1.04**-10, 0.675564, 6)
    quoted("A(4%)", a0, 8.110896, 6)
    quoted("A'(4%)", a_prime, -40.37716, 5)
    quoted("-A'/A", -a_prime / a0, 4.97814, 5)
    quoted("S0^2 sigma^2 T", s0 * s0 * vol * vol * t, 0.000320, 6)
    linear = s0 * s0 * vol * vol * t * (-a_prime / a0)
    quoted("linear approximation (bp)", linear * 1e4, 15.93, 2)
    quoted("expected CMS fixing, linear (%)", (s0 + linear) * 100, 4.1593, 4)

    def h(k: float) -> float:
        return k / annuity(k)

    def h2(k: float) -> float:
        e = 1e-4
        return (h(k + e) - 2.0 * h(k) + h(k - e)) / (e * e)

    def g(k: float) -> float:
        return 1.0 / annuity(k)

    def g2(k: float) -> float:
        e = 1e-4
        return (g(k + e) - 2.0 * g(k) + g(k - e)) / (e * e)

    def replicate(fn: Callable[[float], float], fn2: Callable[[float], float]) -> float:
        """E^A[fn(S)] = fn(S0) + int_0^S0 fn'' Put dK + int_S0^inf fn'' Call dK (undiscounted Black)."""
        put_part = simpson(lambda k: fn2(k) * black_put(s0, k, vol, t), 1e-4, s0, 2000)
        call_part = simpson(lambda k: fn2(k) * black_call(s0, k, vol, t), s0, 0.60, 4000)
        return fn(s0) + put_part + call_part

    # E^{T1}[S] = E^A[S G(S)] / E^A[G(S)]: the ratio keeps the model consistent with the zero bond.
    replicated = replicate(h, h2) / replicate(g, g2) - s0
    z, w = np.polynomial.hermite_e.hermegauss(120)
    s_t = s0 * np.exp(vol * math.sqrt(t) * z - 0.5 * vol * vol * t)
    e_h = float(np.sum(w * np.array([h(float(x)) for x in s_t]))) / math.sqrt(2.0 * math.pi)
    e_g = float(np.sum(w * np.array([g(float(x)) for x in s_t]))) / math.sqrt(2.0 * math.pi)
    density = e_h / e_g - s0
    assert abs(replicated - density) < 2e-7, (replicated, density)
    quoted("replication with Black swaptions (bp)", replicated * 1e4, 18.18, 2)
    quoted("direct integration over the lognormal density (bp)", density * 1e4, 18.18, 2)
    quoted("model minus linear approximation (bp)", (density - linear) * 1e4, 2.25, 2)
    # One change at a time: keep the linear formula, replace sigma^2 T by the exact lognormal e^{sigma^2 T} - 1.
    linear_exact_var = s0 * s0 * (math.exp(vol * vol * t) - 1.0) * (-a_prime / a0)
    quoted("linear formula with the exact lognormal variance (bp)", linear_exact_var * 1e4, 17.63, 2)
    quoted("gap explained by the variance approximation (bp)", (linear_exact_var - linear) * 1e4, 1.70, 2)
    quoted("gap left to higher-order terms (bp)", (density - linear_exact_var) * 1e4, 0.54, 2)

    narrow = simpson(lambda k: h2(k) * black_put(s0, k, vol, t), s0 - 0.01, s0, 2000)
    narrow += simpson(lambda k: h2(k) * black_call(s0, k, vol, t), s0, s0 + 0.01, 2000)
    narrow_g = simpson(lambda k: g2(k) * black_put(s0, k, vol, t), s0 - 0.01, s0, 2000)
    narrow_g += simpson(lambda k: g2(k) * black_call(s0, k, vol, t), s0, s0 + 0.01, 2000)
    truncated = (h(s0) + narrow) / (g(s0) + narrow_g) - s0
    quoted("replication truncated to strikes within 100 bp of S0 (bp)", truncated * 1e4, 9.84, 2)
    quoted("adjustment lost by the truncation (bp)", (density - truncated) * 1e4, 8.34, 2)

    quoted("normal versus lognormal vol mistake: variance ratio", (0.20 / 0.0080) ** 2, 625.0, 0)


def example_in_arrears() -> None:
    print("  3. In-arrears: a 12M rate fixing in 5y and paid at fixing")
    l0, tau, vol, t1 = 0.04, 1.0, 0.20, 5.0
    exact = tau * l0 * l0 * (math.exp(vol * vol * t1) - 1.0) / (1.0 + tau * l0)
    first = tau * l0 * l0 * vol * vol * t1 / (1.0 + tau * l0)
    rng = np.random.default_rng(20261018)
    z = rng.standard_normal(2_000_000)
    lt = l0 * np.exp(vol * math.sqrt(t1) * z - 0.5 * vol * vol * t1)
    # E^{T1}[L] = E^{T2}[L (1 + tau L)] / (1 + tau L0); L0 = E^{T2}[L] is used as a control variate.
    mc = tau * (float(np.mean(lt * lt)) - l0 * l0) / (1.0 + tau * l0)
    assert abs(mc - exact) < 2e-6, (mc, exact)
    quoted("exact lognormal adjustment (bp)", exact * 1e4, 3.41, 2)
    quoted("first-order adjustment (bp)", first * 1e4, 3.08, 2)
    quoted("Monte Carlo under the payment-delay measure (bp, about)", mc * 1e4, 3.4, 1)


def example_quanto() -> None:
    print("  4. Quanto: a EUR 10y swap rate fixing in 3y, paid in USD")
    s0, vs, vx, rho, t = 0.03, 0.18, 0.12, 0.40, 3.0
    drift = -rho * vs * vx
    quoted("relative drift adjustment per year", drift, -0.00864, 5)
    quoted("absolute drift per year (bp)", drift * s0 * 1e4, -2.59, 2)
    quoted("exp(drift T) - 1", math.exp(drift * t) - 1.0, -0.025587, 6)
    adj = s0 * (math.exp(drift * t) - 1.0)
    quoted("quanto adjustment (bp)", adj * 1e4, -7.68, 2)
    quoted("linear approximation (bp)", drift * s0 * t * 1e4, -7.78, 2)
    quoted("expected rate under the USD payment measure (%)", (s0 + adj) * 100, 2.9232, 4)
    # Independent: simulate under the foreign T-forward measure, where S and Y = 1/X (EUR per USD) are
    # driftless lognormals with corr(S, Y) = -rho, and reweight by dQ^d/dQ^f = Y_T / Y_fwd(0).
    rng = np.random.default_rng(20261018)
    z1 = rng.standard_normal(2_000_000)
    z2 = -rho * z1 + math.sqrt(1.0 - rho * rho) * rng.standard_normal(2_000_000)
    s_t = s0 * np.exp(vs * math.sqrt(t) * z1 - 0.5 * vs * vs * t)
    y_ratio = np.exp(vx * math.sqrt(t) * z2 - 0.5 * vx * vx * t)
    # Control variates: S and Y are martingales under this measure, so their sample means should be s0 and 1.
    mc = float(np.mean(s_t * y_ratio)) - s0 - (float(np.mean(s_t)) - s0) - s0 * (float(np.mean(y_ratio)) - 1.0)
    assert abs(mc - adj) < 6e-6, (mc, adj)
    quoted("Monte Carlo with the explicit measure change (bp, about)", mc * 1e4, -7.7, 1)


def main() -> None:
    print("=== fi_convexity: convexity adjustments ===")
    example_futures()
    example_cms()
    example_in_arrears()
    example_quanto()
    print(f"\nVerified {len(QUOTED)} convexity adjustment figures.")


if __name__ == "__main__":
    main()
