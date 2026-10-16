"""Shared pricing primitives for the 05-Derivatives-and-Volatility examples.

Standard library plus numpy only:

- ``norm_cdf`` and ``norm_pdf`` (array-friendly, erfc-based so the left tail keeps relative accuracy),
- Black-Scholes prices and vega with a continuous dividend yield,
- a vectorised implied-volatility solver (bisection, so it cannot diverge),
- the Heston characteristic function in the Albrecher et al. (2007) "little trap" form,
- a Fourier pricer (Lewis 2001) that prices a European call for any model given the characteristic function of its log return.

The example scripts in this folder import it; it has no ``__main__`` guard, so ``tools/run_examples.py`` does not run it directly.
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np

SQRT2 = math.sqrt(2.0)
_ERFC = np.frompyfunc(math.erfc, 1, 1)

ArrayLike = float | np.ndarray
CharFn = Callable[[np.ndarray], np.ndarray]


def _out(x: np.ndarray) -> ArrayLike:
    """Return a Python float for 0-d results and the array otherwise."""
    return float(x) if np.ndim(x) == 0 else x


def norm_cdf(x: ArrayLike) -> ArrayLike:
    """Standard normal CDF, N(x) = erfc(-x / sqrt 2) / 2."""
    x = np.asarray(x, dtype=float)
    return _out(0.5 * np.asarray(_ERFC(-x / SQRT2), dtype=float))


def norm_pdf(x: ArrayLike) -> ArrayLike:
    """Standard normal density."""
    x = np.asarray(x, dtype=float)
    return _out(np.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi))


def bs_price(S: ArrayLike, K: ArrayLike, T: ArrayLike, r: float, sigma: ArrayLike, q: float = 0.0, call: bool = True) -> ArrayLike:
    """Black-Scholes-Merton price of a European call or put (continuous dividend yield q)."""
    S, K, T, sigma = (np.asarray(a, dtype=float) for a in (S, K, T, sigma))
    sd = sigma * np.sqrt(T)
    F = S * np.exp((r - q) * T)
    d1 = np.log(F / K) / sd + 0.5 * sd
    d2 = d1 - sd
    df = np.exp(-r * T)
    if call:
        return _out(df * (F * norm_cdf(d1) - K * norm_cdf(d2)))
    return _out(df * (K * norm_cdf(-d2) - F * norm_cdf(-d1)))


def bs_vega(S: ArrayLike, K: ArrayLike, T: ArrayLike, r: float, sigma: ArrayLike, q: float = 0.0) -> ArrayLike:
    """Black-Scholes vega per unit of volatility (multiply by 0.01 for one vol point)."""
    S, K, T, sigma = (np.asarray(a, dtype=float) for a in (S, K, T, sigma))
    sd = sigma * np.sqrt(T)
    F = S * np.exp((r - q) * T)
    d1 = np.log(F / K) / sd + 0.5 * sd
    return _out(np.exp(-r * T) * F * norm_pdf(d1) * np.sqrt(T))


def implied_vol(
    price: ArrayLike, S: ArrayLike, K: ArrayLike, T: ArrayLike, r: float, q: float = 0.0, call: bool = True, iters: int = 80
) -> ArrayLike:
    """Black-Scholes implied volatility by vectorised bisection on [1e-6, 5].

    Bisection is slower than safeguarded Newton but cannot diverge, which is what a test harness wants.
    Prices outside the no-arbitrage bounds return nan.
    """
    price, S, K, T = np.broadcast_arrays(*(np.asarray(a, dtype=float) for a in (price, S, K, T)))
    lo = np.full(price.shape, 1e-6)
    hi = np.full(price.shape, 5.0)
    p_lo = np.asarray(bs_price(S, K, T, r, lo, q, call))
    p_hi = np.asarray(bs_price(S, K, T, r, hi, q, call))
    bad = (price <= p_lo) | (price >= p_hi)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        above = np.asarray(bs_price(S, K, T, r, mid, q, call)) > price
        hi = np.where(above, mid, hi)
        lo = np.where(above, lo, mid)
    vol = 0.5 * (lo + hi)
    return _out(np.where(bad, np.nan, vol))


def heston_cf(u: np.ndarray, T: float, r: float, q: float, kappa: float, theta: float, xi: float, rho: float, v0: float) -> np.ndarray:
    """Characteristic function E[exp(i u ln(S_T / S_0))] under Heston, little-trap form.

    dS/S = (r - q) dt + sqrt(v) dW1, dv = kappa (theta - v) dt + xi sqrt(v) dW2, d<W1, W2> = rho dt.
    The form with g = (b - d) / (b + d) and exp(-d T) keeps the complex log on its principal branch
    (Albrecher, Mayer, Schoutens and Tistaert 2007).
    """
    u = np.asarray(u, dtype=complex)
    iu = 1j * u
    b = kappa - rho * xi * iu
    d = np.sqrt(b * b + xi * xi * (iu + u * u))
    g = (b - d) / (b + d)
    e = np.exp(-d * T)
    C = kappa * theta / xi**2 * ((b - d) * T - 2.0 * np.log((1.0 - g * e) / (1.0 - g)))
    D = (b - d) / xi**2 * (1.0 - e) / (1.0 - g * e)
    return np.exp(iu * (r - q) * T + C + D * v0)


_GL_NODES, _GL_WEIGHTS = np.polynomial.legendre.leggauss(400)


def lewis_call(cf_logret: CharFn, S: float, K: ArrayLike, T: float, r: float, q: float = 0.0, u_max: float = 200.0) -> ArrayLike:
    """European call from the characteristic function of X = ln(S_T / S_0) (Lewis 2001).

    With F = S exp((r - q) T), Y = X - (r - q) T has E[exp(Y)] = 1 and
    C = exp(-r T) [F - sqrt(F K) / pi * int_0^inf Re(exp(i u ln(F / K)) phi_Y(u - i/2)) / (u^2 + 1/4) du].
    The integral is truncated at u_max and done by 400-point Gauss-Legendre; callers check it against Black-Scholes.
    """
    K = np.atleast_1d(np.asarray(K, dtype=float))
    u = 0.5 * u_max * (_GL_NODES + 1.0)
    w = 0.5 * u_max * _GL_WEIGHTS
    z = u - 0.5j
    phi_y = cf_logret(z) * np.exp(-1j * z * (r - q) * T)
    F = S * np.exp((r - q) * T)
    k = np.log(F / K)[:, None]
    integrand = np.real(np.exp(1j * u[None, :] * k) * phi_y[None, :]) / (u * u + 0.25)[None, :]
    integral = integrand @ w
    price = np.exp(-r * T) * (F - np.sqrt(F * K) / math.pi * integral)
    return _out(price if price.size > 1 else price[0])


def heston_call(
    S: float, K: ArrayLike, T: float, r: float, q: float, kappa: float, theta: float, xi: float, rho: float, v0: float
) -> ArrayLike:
    """Heston European call by Fourier inversion of the little-trap characteristic function."""
    return lewis_call(lambda u: heston_cf(u, T, r, q, kappa, theta, xi, rho, v0), S, K, T, r, q)


def _self_test() -> None:
    """Fourier pricer reproduces Black-Scholes when fed the lognormal characteristic function."""
    S, r, q, sig = 100.0, 0.03, 0.01, 0.25
    for T in (0.1, 1.0, 5.0):
        K = np.array([60.0, 90.0, 100.0, 110.0, 150.0])

        def cf(u: np.ndarray, T: float = T) -> np.ndarray:
            return np.exp(1j * u * (r - q - 0.5 * sig**2) * T - 0.5 * sig**2 * T * u * u)

        err = np.max(np.abs(lewis_call(cf, S, K, T, r, q) - bs_price(S, K, T, r, sig, q)))
        assert err < 1e-8, (T, err)
    iv = implied_vol(bs_price(100.0, 120.0, 0.5, r, 0.3, q), 100.0, 120.0, 0.5, r, q)
    assert abs(iv - 0.3) < 1e-10, iv
