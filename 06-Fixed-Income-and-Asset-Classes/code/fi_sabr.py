"""SABR model: Hagan smile, Obloj correction, normal vols, density checks and a Monte Carlo cross-check.

Backs every number in `06-Fixed-Income-and-Asset-Classes/18-Rates-Volatility-and-SABR.md`.
- Example 1 and card fi-rates-vol-sabr-atm-alpha-solve: Hagan et al. (2002) smile, Gamma terms, alpha from an ATM quote.
- Example 2: parameter sensitivities (nu, rho) of the Hagan smile.
- Example 3: shifted SABR for a negative forward and its equivalent normal (Bachelier) volatility.
- Example 4: Monte Carlo simulation of the SABR SDEs (an independent check of the asymptotic formula) and Obloj's (2008) correction.
- Example 5 and card fi-rates-vol-sabr-normal-vs-lognormal: exact Black-to-Bachelier conversion and the ATM approximation.
- Example 6 and card fi-rates-vol-sabr-wing-arbitrage: Breeden-Litzenberger density of the Hagan smile at 1y and 10y.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_sabr.py`.
"""

from __future__ import annotations

import math

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


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def sabr_gamma(f: float, k: float, alpha: float, beta: float, rho: float, nu: float) -> float:
    """The O(T) correction Gamma of Hagan et al. (2002), evaluated at the geometric mean of F and K."""
    fk = f * k
    return (
        ((1.0 - beta) ** 2 / 24.0) * alpha * alpha / fk ** (1.0 - beta)
        + 0.25 * rho * beta * nu * alpha / fk ** (0.5 * (1.0 - beta))
        + ((2.0 - 3.0 * rho * rho) / 24.0) * nu * nu
    )


def chi(z: float, rho: float) -> float:
    return math.log((math.sqrt(1.0 - 2.0 * rho * z + z * z) + z - rho) / (1.0 - rho))


def sabr_hagan_lognormal_vol(f: float, k: float, t_exp: float, alpha: float, beta: float, rho: float, nu: float) -> float:
    """Hagan et al. (2002) asymptotic implied Black volatility for SABR."""
    if f <= 0.0 or k <= 0.0:
        raise ValueError("Forward and strike must be positive; use the shifted model for negative rates.")
    if abs(f - k) < 1e-12:
        return alpha / f ** (1.0 - beta) * (1.0 + sabr_gamma(f, f, alpha, beta, rho, nu) * t_exp)
    log_fk = math.log(f / k)
    fk_pow = (f * k) ** (0.5 * (1.0 - beta))
    z = (nu / alpha) * fk_pow * log_fk
    z_over_chi = 1.0 if abs(z) < 1e-10 else z / chi(z, rho)
    denom = fk_pow * (1.0 + ((1.0 - beta) ** 2 / 24.0) * log_fk**2 + ((1.0 - beta) ** 4 / 1920.0) * log_fk**4)
    return alpha / denom * z_over_chi * (1.0 + sabr_gamma(f, k, alpha, beta, rho, nu) * t_exp)


def sabr_obloj_lognormal_vol(f: float, k: float, t_exp: float, alpha: float, beta: float, rho: float, nu: float) -> float:
    """Obloj (2008) leading term nu ln(F/K) / chi(z) with z = nu (F^(1-beta) - K^(1-beta)) / (alpha (1-beta)), times Hagan's 1 + Gamma T."""
    if abs(f - k) < 1e-12:
        return sabr_hagan_lognormal_vol(f, k, t_exp, alpha, beta, rho, nu)
    z = nu * (f ** (1.0 - beta) - k ** (1.0 - beta)) / (alpha * (1.0 - beta))
    return nu * math.log(f / k) / chi(z, rho) * (1.0 + sabr_gamma(f, k, alpha, beta, rho, nu) * t_exp)


def shifted_sabr_hagan_lognormal_vol(
    f: float, k: float, t_exp: float, alpha: float, beta: float, rho: float, nu: float, shift: float
) -> float:
    """Shifted SABR: Hagan's formula applied to F + s and K + s."""
    if f + shift <= 0.0 or k + shift <= 0.0:
        raise ValueError("Forward and strike + shift must be strictly positive.")
    return sabr_hagan_lognormal_vol(f + shift, k + shift, t_exp, alpha, beta, rho, nu)


def black_call(f: float, k: float, vol: float, t: float) -> float:
    """Undiscounted Black-76 call (per unit annuity)."""
    sd = vol * math.sqrt(t)
    d1 = (math.log(f / k) + 0.5 * sd * sd) / sd
    return f * norm_cdf(d1) - k * norm_cdf(d1 - sd)


def bachelier_call(f: float, k: float, vol_n: float, t: float) -> float:
    """Undiscounted Bachelier call (per unit annuity)."""
    sd = vol_n * math.sqrt(t)
    d = (f - k) / sd
    return (f - k) * norm_cdf(d) + sd * norm_pdf(d)


def implied_normal_vol(price: float, f: float, k: float, t: float) -> float:
    """Bachelier volatility matching an undiscounted call price; the price is increasing in vol, so bisect."""
    lo, hi = 1e-8, 0.10
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if bachelier_call(f, k, mid, t) < price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def implied_black_vol(price: float, f: float, k: float, t: float) -> float:
    lo, hi = 1e-6, 3.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if black_call(f, k, mid, t) < price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def hagan_density(f: float, k: float, t: float, alpha: float, beta: float, rho: float, nu: float, h: float = 1e-5) -> float:
    """Breeden-Litzenberger density d2C/dK2 of the Hagan smile, by central differences of Black prices."""
    prices = [black_call(f, kk, sabr_hagan_lognormal_vol(f, kk, t, alpha, beta, rho, nu), t) for kk in (k - h, k, k + h)]
    return (prices[0] - 2.0 * prices[1] + prices[2]) / (h * h)


def alpha_from_atm_vol(sigma_atm: float, f: float, t: float, beta: float, rho: float, nu: float) -> float:
    """Smallest positive root of the ATM cubic in alpha, found by bisection on [0, upper]."""

    def resid(alpha: float) -> float:
        return sabr_hagan_lognormal_vol(f, f, t, alpha, beta, rho, nu) - sigma_atm

    lo, hi = 1e-8, sigma_atm * f ** (1.0 - beta)
    while resid(hi) < 0.0:
        hi *= 1.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if resid(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


F0, T1, ALPHA, BETA, RHO, NU = 0.040, 1.0, 0.035, 0.5, -0.25, 0.40


def example1_hagan() -> None:
    print("  1. Hagan smile, Gamma terms and the ATM alpha solve (Example 1, card fi-rates-vol-sabr-atm-alpha-solve)")
    one_minus_beta = 1.0 - BETA
    f_pow = F0**one_minus_beta
    quoted("F^(1-beta)", f_pow, 0.20, 2)
    quoted("alpha / F^(1-beta)", ALPHA / f_pow, 0.1750, 4)
    term1 = (one_minus_beta**2 / 24.0) * ALPHA**2 / F0 ** (2.0 * one_minus_beta)
    term2 = 0.25 * RHO * BETA * NU * ALPHA / f_pow
    term3 = ((2.0 - 3.0 * RHO**2) / 24.0) * NU**2
    quoted("Gamma term 1", term1, 0.000319, 6)
    quoted("Gamma term 1 (7 dp)", term1, 0.0003190, 7)
    quoted("Gamma term 2", term2, -0.0021875, 7)
    quoted("Gamma term 3", term3, 0.012083, 6)
    quoted("Gamma term 3 (7 dp)", term3, 0.0120833, 7)
    quoted("Gamma", term1 + term2 + term3, 0.010215, 6)
    quoted("1 + Gamma T", 1.0 + (term1 + term2 + term3) * T1, 1.010215, 6)
    quoted("sigma_B ATM 4% (%)", sabr_hagan_lognormal_vol(F0, 0.04, T1, ALPHA, BETA, RHO, NU) * 100.0, 17.68, 2)
    quoted("sigma_B 2% (%)", sabr_hagan_lognormal_vol(F0, 0.02, T1, ALPHA, BETA, RHO, NU) * 100.0, 27.54, 2)
    quoted("sigma_B 6% (%)", sabr_hagan_lognormal_vol(F0, 0.06, T1, ALPHA, BETA, RHO, NU) * 100.0, 16.54, 2)
    # Calibration step 2: a market ATM quote of 18.00% with (beta, rho, nu) fixed pins alpha.
    alpha_18 = alpha_from_atm_vol(0.18, F0, T1, BETA, RHO, NU)
    quoted("alpha solving sigma_ATM = 18.00%", alpha_18, 0.03564, 5)
    # Round trip: the ATM quote 17.68% implied by alpha = 0.035 gives alpha back.
    sigma_atm = sabr_hagan_lognormal_vol(F0, F0, T1, ALPHA, BETA, RHO, NU)
    assert abs(alpha_from_atm_vol(sigma_atm, F0, T1, BETA, RHO, NU) - ALPHA) < 1e-12


def example2_sensitivities() -> None:
    print("  2. Parameter sensitivities (Example 2)")
    cases = [
        ("nu=0.80", -0.25, 0.80, (36.76, 18.27, 20.69)),
        ("rho=0", 0.0, 0.40, (25.47, 17.74, 18.25)),
        ("rho=+0.30", 0.30, 0.40, (22.44, 17.75, 19.97)),
    ]
    for name, rho, nu, expected in cases:
        for k, e in zip((0.02, 0.04, 0.06), expected, strict=True):
            quoted(f"{name} K={k:.2f} (%)", sabr_hagan_lognormal_vol(F0, k, T1, ALPHA, BETA, rho, nu) * 100.0, e, 2)
    quoted("rho=+0.50 K=0.02 (%)", sabr_hagan_lognormal_vol(F0, 0.02, T1, ALPHA, BETA, 0.50, 0.40) * 100.0, 19.94, 2)
    quoted("rho=+0.50 K=0.06 (%)", sabr_hagan_lognormal_vol(F0, 0.06, T1, ALPHA, BETA, 0.50, 0.40) * 100.0, 20.95, 2)


def example3_shifted() -> None:
    print("  3. Shifted SABR for a negative forward (Example 3)")
    f_neg, shift = -0.0050, 0.0300
    quoted("Shifted forward F + s (%)", (f_neg + shift) * 100.0, 2.50, 2)
    vol_1y = shifted_sabr_hagan_lognormal_vol(f_neg, f_neg, 1.0, ALPHA, BETA, RHO, NU, shift)
    vol_2y = shifted_sabr_hagan_lognormal_vol(f_neg, f_neg, 2.0, ALPHA, BETA, RHO, NU, shift)
    quoted("Shifted lognormal ATM vol, 1y (%)", vol_1y * 100.0, 22.35, 2)
    quoted("Shifted lognormal ATM vol, 2y (%)", vol_2y * 100.0, 22.57, 2)
    # The same option priced in shifted Black, then re-quoted in Bachelier: shifts cancel in F - K.
    price = black_call(f_neg + shift, f_neg + shift, vol_1y, 1.0)
    quoted("Equivalent normal ATM vol, 1y (bp)", implied_normal_vol(price, f_neg, f_neg, 1.0) * 1e4, 55.77, 2)


def example4_monte_carlo_and_obloj() -> None:
    print("  4. Monte Carlo SABR (independent check of the expansion) and Obloj's correction (Example 4)")
    rng = np.random.default_rng(20020701)
    n_paths, n_steps = 200_000, 200
    dt = T1 / n_steps
    fwd = np.full(n_paths, F0)
    vol = np.full(n_paths, ALPHA)
    sq = math.sqrt(1.0 - RHO * RHO)
    for _ in range(n_steps):
        z1 = rng.standard_normal(n_paths)
        z2 = RHO * z1 + sq * rng.standard_normal(n_paths)
        fwd = np.maximum(fwd + vol * fwd**BETA * math.sqrt(dt) * z1, 0.0)  # absorbing at zero
        vol = vol * np.exp(NU * math.sqrt(dt) * z2 - 0.5 * NU * NU * dt)  # exact lognormal step
    mc_mean = float(fwd.mean())
    assert abs(mc_mean - F0) < 5e-5, f"forward should stay a martingale, got {mc_mean}"
    targets = {0.02: 27.5, 0.04: 17.7, 0.06: 16.6}
    for k, about in targets.items():
        # Out-of-the-money option on each side, converted to a call by parity on the simulated forward.
        if k < F0:
            call = float(np.maximum(k - fwd, 0.0).mean()) + mc_mean - k
        else:
            call = float(np.maximum(fwd - k, 0.0).mean())
        iv_mc = implied_black_vol(call, mc_mean, k, T1)
        iv_hagan = sabr_hagan_lognormal_vol(F0, k, T1, ALPHA, BETA, RHO, NU)
        quoted(f"MC implied vol K={k:.2f} (%), seed-stable", iv_mc * 100.0, about, 1)
        # Independent check: the asymptotic formula and the simulated SDE agree to within 0.3 vol points here.
        assert abs(iv_mc - iv_hagan) < 0.003, f"Hagan {iv_hagan} vs MC {iv_mc} at K={k}"
    quoted("Obloj vol K=0.02 (%)", sabr_obloj_lognormal_vol(F0, 0.02, T1, ALPHA, BETA, RHO, NU) * 100.0, 27.58, 2)
    quoted("Obloj vol K=0.06 (%)", sabr_obloj_lognormal_vol(F0, 0.06, T1, ALPHA, BETA, RHO, NU) * 100.0, 16.55, 2)


def example5_normal_vols() -> None:
    print("  5. Lognormal to normal volatility (Example 5, card fi-rates-vol-sabr-normal-vs-lognormal)")
    expected = {0.02: 79.23, 0.04: 70.62, 0.06: 81.50}
    for k, e in expected.items():
        sigma_b = sabr_hagan_lognormal_vol(F0, k, T1, ALPHA, BETA, RHO, NU)
        sigma_n = implied_normal_vol(black_call(F0, k, sigma_b, T1), F0, k, T1)
        quoted(f"normal vol K={k:.2f} (bp)", sigma_n * 1e4, e, 2)
    sigma_b_atm = sabr_hagan_lognormal_vol(F0, F0, T1, ALPHA, BETA, RHO, NU)
    quoted("sigma_B * F (bp)", sigma_b_atm * F0 * 1e4, 70.715, 3)
    quoted("sigma_B ATM (5 dp)", sigma_b_atm, 0.17679, 5)
    approx = sigma_b_atm * F0 * (1.0 - sigma_b_atm**2 * T1 / 24.0)
    quoted("sigma_B^2 T / 24", sigma_b_atm**2 * T1 / 24.0, 0.0013, 4)
    quoted("ATM approximation sigma_B F (1 - sigma_B^2 T / 24) (bp)", approx * 1e4, 70.62, 2)


def example6_density() -> None:
    print("  6. Density of the Hagan smile (Example 6, card fi-rates-vol-sabr-wing-arbitrage)")
    strikes = [0.001 + i * 0.0005 for i in range(239)]  # 0.10% to 12.00%
    dens_1y = [hagan_density(F0, k, 1.0, ALPHA, BETA, RHO, NU) for k in strikes]
    assert min(dens_1y) > 0.0, "1y Hagan density should be positive on the grid"
    dens_10y = [hagan_density(F0, k, 10.0, ALPHA, BETA, RHO, NU) for k in strikes]
    assert dens_10y[0] < 0.0 < dens_10y[-1]
    # The density changes sign once on the grid; bisect for the crossing strike.
    lo, hi = 0.001, 0.03
    assert hagan_density(F0, lo, 10.0, ALPHA, BETA, RHO, NU) < 0.0 < hagan_density(F0, hi, 10.0, ALPHA, BETA, RHO, NU)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if hagan_density(F0, mid, 10.0, ALPHA, BETA, RHO, NU) < 0.0:
            lo = mid
        else:
            hi = mid
    quoted("10y density negative below strike (%)", 0.5 * (lo + hi) * 100.0, 0.90, 2)
    quoted("10y Hagan vol at K=0.50% (%)", sabr_hagan_lognormal_vol(F0, 0.005, 10.0, ALPHA, BETA, RHO, NU) * 100.0, 53.75, 2)


def main() -> None:
    print("=== fi_sabr: Rates Volatility and SABR ===")
    example1_hagan()
    example2_sensitivities()
    example3_shifted()
    example4_monte_carlo_and_obloj()
    example5_normal_vols()
    example6_density()
    print(f"\nSuccessfully verified {len(QUOTED)} SABR figures.")


if __name__ == "__main__":
    main()
