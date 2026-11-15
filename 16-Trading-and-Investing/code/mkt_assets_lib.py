"""Shared helpers for the asset-class pillar scripts (opt, exec, india, macro, cmdty, crypto).

Not an example itself (no main guard): the `mkt_<pillar>_<NN>_*.py` scripts import it.
- `q` prints a value and asserts it rounds to the literal a note quotes, at that literal's precision.
- `close` asserts agreement between two independent routes within a stated tolerance.
- Black-Scholes-Merton prices come in two independent forms: the closed form and a direct quadrature of the
  discounted payoff against the lognormal density, so a check of one against the other is not circular.
Standard library and numpy only.
"""

from __future__ import annotations

import math

import numpy as np

SQRT_2PI = math.sqrt(2.0 * math.pi)


def decimals_of(quoted: str) -> int:
    return len(quoted.split(".")[1]) if "." in quoted else 0


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes (commas allowed in the literal)."""
    lit = quoted.replace(",", "")
    tol = 0.5 * 10.0 ** -decimals_of(lit) * (1 + 1e-9) + 1e-12
    print(f"{label:70s} {value:18.8f}  quoted {quoted}")
    assert abs(value - float(lit)) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:64s} |diff| = {abs(a - b):.2e} (tol {tol:.0e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / SQRT_2PI


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def d1_d2(S: float, K: float, T: float, r: float, q_: float, sigma: float) -> tuple[float, float]:
    sd = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q_ + 0.5 * sigma * sigma) * T) / sd
    return d1, d1 - sd


def bs_price(S: float, K: float, T: float, r: float, q_: float, sigma: float, call: bool = True) -> float:
    """Closed-form Black-Scholes-Merton price with continuous dividend yield q_."""
    d1, d2 = d1_d2(S, K, T, r, q_, sigma)
    if call:
        return S * math.exp(-q_ * T) * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S * math.exp(-q_ * T) * norm_cdf(-d1)


def bs_price_quad(S: float, K: float, T: float, r: float, q_: float, sigma: float, call: bool = True, n: int = 200_001) -> float:
    """Discounted risk-neutral expectation of the payoff by trapezoid quadrature over z ~ N(0, 1).

    S_T = S exp((r - q - sigma^2 / 2) T + sigma sqrt(T) z); the grid spans |z| <= 12, so the truncated mass is
    below 1e-30. No normal CDF is used, so this is independent of the closed form.
    """
    z = np.linspace(-12.0, 12.0, n)
    st = S * np.exp((r - q_ - 0.5 * sigma * sigma) * T + sigma * math.sqrt(T) * z)
    payoff = np.maximum(st - K, 0.0) if call else np.maximum(K - st, 0.0)
    dens = np.exp(-0.5 * z * z) / SQRT_2PI
    return math.exp(-r * T) * float(np.trapezoid(payoff * dens, z))


def bs_greeks(S: float, K: float, T: float, r: float, q_: float, sigma: float, call: bool = True) -> dict[str, float]:
    """Closed-form Greeks per unit of each input; theta per year of calendar time."""
    d1, d2 = d1_d2(S, K, T, r, q_, sigma)
    sq = math.sqrt(T)
    dq, dr, pdf = math.exp(-q_ * T), math.exp(-r * T), norm_pdf(d1)
    vega = S * dq * pdf * sq
    decay = -S * dq * pdf * sigma / (2 * sq)
    if call:
        delta = dq * norm_cdf(d1)
        theta = decay - r * K * dr * norm_cdf(d2) + q_ * S * dq * norm_cdf(d1)
        charm = q_ * dq * norm_cdf(d1) - dq * pdf * (2 * (r - q_) * T - d2 * sigma * sq) / (2 * T * sigma * sq)
    else:
        delta = -dq * norm_cdf(-d1)
        theta = decay + r * K * dr * norm_cdf(-d2) - q_ * S * dq * norm_cdf(-d1)
        charm = -q_ * dq * norm_cdf(-d1) - dq * pdf * (2 * (r - q_) * T - d2 * sigma * sq) / (2 * T * sigma * sq)
    return {
        "d1": d1,
        "d2": d2,
        "delta": delta,
        "gamma": dq * pdf / (S * sigma * sq),
        "vega": vega,
        "theta": theta,
        "vanna": -dq * pdf * d2 / sigma,
        "volga": vega * d1 * d2 / sigma,
        "charm": charm,
    }


def bisect(f, lo: float, hi: float, tol: float = 1e-12, max_iter: int = 500) -> float:
    """Root of a continuous f on [lo, hi] with a sign change, by bisection (no derivative used)."""
    flo = f(lo)
    assert flo * f(hi) <= 0, "bisect: no sign change on the bracket"
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)
