"""Jump-diffusion and Levy models: Merton series, Kou and variance gamma by characteristic function, all checked by Monte Carlo.

Backs every number in 04-Stochastic-Calculus/08-Jump-Processes-and-Levy-Models.md:

1. Merton (1976): the Poisson-weighted Black-Scholes series, a Fourier (Lewis 2001) price from the characteristic
   function, and exact simulation, all agreeing; the implied-volatility smile and how fast it flattens with maturity;
   cumulants of the log return.
2. Kou (2002) double exponential jumps: Fourier price against simulation.
3. Variance gamma (Madan, Carr and Chang 1998): Fourier price against simulation of Brownian motion in gamma time,
   and the equivalence of the time-change and Levy-measure (CGMY with Y = 0) forms of its characteristic function.
4. Levy-Khintchine sanity checks: phi_T(-i) = exp((r - q) T) (martingale condition) and phi_{2T} = phi_T^2.
5. Gap risk: the loss of a delta-hedged short option on a jump.

Run from the repo root: uv run --no-project --with numpy python 04-Stochastic-Calculus/code/jump_levy_models.py
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np

SQRT2 = math.sqrt(2.0)
_ERFC = np.frompyfunc(math.erfc, 1, 1)
CharFn = Callable[[np.ndarray], np.ndarray]


def ncdf(x: float | np.ndarray) -> np.ndarray:
    return 0.5 * np.asarray(_ERFC(-np.asarray(x, dtype=float) / SQRT2), dtype=float)


def bs_call(S: float, K: np.ndarray | float, T: float, r: float, sigma: np.ndarray | float) -> np.ndarray:
    K, sigma = np.asarray(K, dtype=float), np.asarray(sigma, dtype=float)
    sd = sigma * math.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / sd
    return S * ncdf(d1) - K * np.exp(-r * T) * ncdf(d1 - sd)


def implied_vol(price: np.ndarray, S: float, K: np.ndarray, T: float, r: float) -> np.ndarray:
    """Vectorised bisection on [1e-4, 3]; the call price is increasing in sigma."""
    lo, hi = np.full(np.shape(K), 1e-4), np.full(np.shape(K), 3.0)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        above = bs_call(S, K, T, r, mid) > price
        hi, lo = np.where(above, mid, hi), np.where(above, lo, mid)
    return 0.5 * (lo + hi)


_NODES, _WEIGHTS = np.polynomial.legendre.leggauss(400)


def lewis_call(cf: CharFn, S: float, K: np.ndarray, T: float, r: float, u_max: float = 200.0) -> np.ndarray:
    """Call from phi(u) = E[exp(i u ln(S_T/S_0))] (Lewis 2001), 400-point Gauss-Legendre on [0, u_max]."""
    K = np.atleast_1d(np.asarray(K, dtype=float))
    u = 0.5 * u_max * (_NODES + 1.0)
    w = 0.5 * u_max * _WEIGHTS
    z = u - 0.5j
    phi_y = cf(z) * np.exp(-1j * z * r * T)
    F = S * math.exp(r * T)
    k = np.log(F / K)[:, None]
    integral = (np.real(np.exp(1j * u[None, :] * k) * phi_y[None, :]) / (u * u + 0.25)[None, :]) @ w
    return math.exp(-r * T) * (F - np.sqrt(F * K) / math.pi * integral)


def check(name: str, value: float, expected: float, tol: float) -> float:
    print(f"{name:64s} {value:.6g}")
    assert abs(value - expected) <= tol, f"{name}: {value} vs {expected} (tol {tol})"
    return value


def check_mc(name: str, value: float, se: float, quoted: float, truth: float, quoted_tol: float, se_quoted: float, se_tol: float) -> None:
    """Seed-stable simulation number: equals the quoted value, its standard error equals the quoted one,
    and it lies within 4 standard errors of the truth."""
    print(f"{name:64s} {value:.6g}  (se {se:.2g})")
    assert abs(value - quoted) <= quoted_tol, f"{name}: {value} vs quoted {quoted}"
    assert abs(se - se_quoted) <= se_tol, f"{name}: standard error {se} vs quoted {se_quoted}"
    assert abs(value - truth) <= 4 * se, f"{name}: {value} vs truth {truth}, se {se}"


S0, R = 100.0, 0.05
STRIKES = np.array([80.0, 90.0, 100.0, 110.0, 120.0])

# ----------------------------------------------------------------------------------------------
# 1. Merton jump-diffusion
# ----------------------------------------------------------------------------------------------

SIG_M, LAM_M, MJ, DJ = 0.20, 1.0, -0.10, 0.15  # diffusion vol, jumps per year, mean and sd of the log jump


def merton_kbar() -> float:
    return math.exp(MJ + 0.5 * DJ * DJ) - 1.0


def merton_cf(u: np.ndarray, T: float) -> np.ndarray:
    kbar = merton_kbar()
    drift = R - LAM_M * kbar - 0.5 * SIG_M**2
    return np.exp(T * (1j * u * drift - 0.5 * SIG_M**2 * u * u + LAM_M * (np.exp(1j * u * MJ - 0.5 * DJ * DJ * u * u) - 1.0)))


def merton_series(K: np.ndarray, T: float, tol: float = 1e-12) -> tuple[np.ndarray, int]:
    """Merton (1976): sum over n of Poisson(lam' T) weights times Black-Scholes with r_n and sigma_n."""
    kbar = merton_kbar()
    lam_p = LAM_M * (1 + kbar)
    total = np.zeros_like(K)
    n = 0
    while True:
        w = math.exp(-lam_p * T) * (lam_p * T) ** n / math.factorial(n)
        sig_n = math.sqrt(SIG_M**2 + n * DJ * DJ / T)
        r_n = R - LAM_M * kbar + n * math.log(1 + kbar) / T
        # Black-Scholes with rate r_n both in the drift and in the discounting: the lam' weights absorb the difference
        total = total + w * bs_call(S0, K, T, r_n, sig_n)
        n += 1
        if w < tol and n > lam_p * T:
            return total, n


def merton(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Merton: three prices that must agree' and 'Merton smile and its term structure';
    cards sc-jump-merton-series, sc-jump-merton-compensator, sc-jump-smile-decay, sc-jump-cumulants."""
    print(f"\n1. Merton: sigma={SIG_M}, lambda={LAM_M}, m={MJ}, delta={DJ}, S0=100, r=5%, T=1")
    T = 1.0
    kbar = merton_kbar()
    check("mean jump size kbar = exp(m + delta^2/2) - 1", kbar, -0.08493, 5e-6)
    check("compensated drift r - lambda kbar", R - LAM_M * kbar, 0.13493, 5e-6)
    series, nterms = merton_series(STRIKES, T)
    fourier = lewis_call(lambda u: merton_cf(u, T), S0, STRIKES, T, R)
    for K, s_, f_ in zip(STRIKES, series, fourier, strict=True):
        check(f"  K={K:.0f} series", float(s_), float(f_), 1e-8)
    check("  K=100 Merton call", float(series[2]), 12.7613, 5e-5)
    check("  terms in the series to reach weight 1e-12", float(nterms), 16.0, 0.0)
    # Exact simulation: N ~ Poisson(lambda T), sum of N normal log-jumps
    n = 2_000_000
    N = rng.poisson(LAM_M * T, n)
    X = (R - LAM_M * kbar - 0.5 * SIG_M**2) * T + SIG_M * math.sqrt(T) * rng.standard_normal(n)
    X += N * MJ + DJ * np.sqrt(N) * rng.standard_normal(n)
    ST = S0 * np.exp(X)
    check("  E[S_T] / (S0 e^{rT}) (martingale check)", float(ST.mean() / (S0 * math.exp(R * T))), 0.9997, 5e-5)
    assert abs(ST.mean() / (S0 * math.exp(R * T)) - 1) < 4 * ST.std() / math.sqrt(n) / (S0 * math.exp(R * T))
    pay = math.exp(-R * T) * np.maximum(ST - 100.0, 0.0)
    check_mc("  K=100 Monte Carlo", float(pay.mean()), float(pay.std() / math.sqrt(n)), 12.741, float(series[2]), 5e-4, 0.013, 5e-4)

    iv = implied_vol(series, S0, STRIKES, T, R)
    for K, v in zip(STRIKES, iv, strict=True):
        print(f"  implied vol K={K:.0f}: {100 * v:.2f}%")
    for K, v, q in zip(STRIKES, iv, (27.70, 26.82, 26.12, 25.58, 25.18), strict=True):
        check(f"  implied vol at K={K:.0f} (%)", 100 * float(v), q, 5e-3)
    check("  total vol sqrt(sigma^2 + lambda (m^2 + delta^2)) (%)", 100 * math.sqrt(SIG_M**2 + LAM_M * (MJ**2 + DJ**2)), 26.93, 5e-3)

    # Cumulants of X_1 = ln(S_1/S_0): c2 = sigma^2 + lambda (m^2 + delta^2), c3 = lambda (m^3 + 3 m delta^2), ...
    c2 = SIG_M**2 + LAM_M * (MJ**2 + DJ**2)
    c3 = LAM_M * (MJ**3 + 3 * MJ * DJ**2)
    c4 = LAM_M * (MJ**4 + 6 * MJ**2 * DJ**2 + 3 * DJ**4)
    skew, exkurt = c3 / c2**1.5, c4 / c2**2
    check("  skewness of the one-year log return", skew, -0.3970, 5e-5)
    check("  excess kurtosis of the one-year log return", exkurt, 0.5648, 5e-5)
    xc = X - X.mean()
    check("  skewness by simulation", float((xc**3).mean() / xc.var() ** 1.5), -0.396, 5e-4)
    check("  excess kurtosis by simulation", float((xc**4).mean() / xc.var() ** 2 - 3), 0.562, 5e-4)
    check("  excess kurtosis at T = 0.1 (scales like 1/T)", exkurt / 0.1, 5.648, 5e-4)

    # Skew term structure: 90%-110% forward-moneyness vol spread
    print("  skew (vol at 0.9F minus vol at 1.1F), vol points:")
    skews: dict[float, float] = {}
    for T_, q in ((0.1, 6.30), (0.5, 2.09), (1.0, 1.14), (3.0, 0.39)):
        F = S0 * math.exp(R * T_)
        K = np.array([0.9 * F, 1.1 * F])
        prices = lewis_call(lambda u, T_=T_: merton_cf(u, T_), S0, K, T_, R)
        v = implied_vol(prices, S0, K, T_, R)
        skews[T_] = check(f"    T={T_}", 100 * float(v[0] - v[1]), q, 5e-3)
    check("  skew decay factor from T = 0.1 to T = 1", skews[0.1] / skews[1.0], 5.5, 0.05)


# ----------------------------------------------------------------------------------------------
# 2. Kou double exponential
# ----------------------------------------------------------------------------------------------

SIG_K, LAM_K, P_UP, ETA1, ETA2 = 0.16, 1.0, 0.4, 10.0, 5.0


def kou_cf(u: np.ndarray, T: float) -> np.ndarray:
    zeta = P_UP * ETA1 / (ETA1 - 1) + (1 - P_UP) * ETA2 / (ETA2 + 1) - 1
    drift = R - 0.5 * SIG_K**2 - LAM_K * zeta
    jump = P_UP * ETA1 / (ETA1 - 1j * u) + (1 - P_UP) * ETA2 / (ETA2 + 1j * u) - 1
    return np.exp(T * (1j * u * drift - 0.5 * SIG_K**2 * u * u + LAM_K * jump))


def kou(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Kou and variance gamma by Fourier inversion'; card sc-levy-kou."""
    print(f"\n2. Kou: sigma={SIG_K}, lambda={LAM_K}, p={P_UP}, eta1={ETA1}, eta2={ETA2}, T=1")
    T = 1.0
    zeta = P_UP * ETA1 / (ETA1 - 1) + (1 - P_UP) * ETA2 / (ETA2 + 1) - 1
    check("E[e^J] - 1 (zeta)", zeta, -0.05556, 5e-6)
    price = lewis_call(lambda u: kou_cf(u, T), S0, STRIKES, T, R)
    check("K=100 Kou call by Fourier", float(price[2]), 12.4325, 5e-5)
    n = 2_000_000
    N = rng.poisson(LAM_K * T, n)
    X = (R - 0.5 * SIG_K**2 - LAM_K * zeta) * T + SIG_K * math.sqrt(T) * rng.standard_normal(n)
    jumps = np.zeros(n)
    counts = N
    for j in range(int(counts.max())):
        has = counts > j
        up = rng.random(n) < P_UP
        size = np.where(up, rng.exponential(1 / ETA1, n), -rng.exponential(1 / ETA2, n))
        jumps += np.where(has, size, 0.0)
    ST = S0 * np.exp(X + jumps)
    pay = math.exp(-R * T) * np.maximum(ST - 100.0, 0.0)
    check_mc("K=100 Kou Monte Carlo", float(pay.mean()), float(pay.std() / math.sqrt(n)), 12.431, float(price[2]), 5e-4, 0.012, 5e-4)
    iv = implied_vol(price, S0, STRIKES, T, R)
    check("Kou implied vol at K=80 (%)", 100 * float(iv[0]), 29.20, 5e-3)
    check("Kou implied vol at K=120 (%)", 100 * float(iv[4]), 23.61, 5e-3)


# ----------------------------------------------------------------------------------------------
# 3. Variance gamma
# ----------------------------------------------------------------------------------------------

SIG_V, NU_V, TH_V = 0.12, 0.2, -0.14


def vg_omega() -> float:
    return math.log(1 - TH_V * NU_V - 0.5 * SIG_V**2 * NU_V) / NU_V


def vg_cf(u: np.ndarray, T: float) -> np.ndarray:
    base = 1 - 1j * u * TH_V * NU_V + 0.5 * SIG_V**2 * NU_V * u * u
    return np.exp(1j * u * (R + vg_omega()) * T - T / NU_V * np.log(base))


def variance_gamma(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Kou and variance gamma by Fourier inversion'; cards sc-levy-vg-time-change, sc-levy-infinite-activity."""
    print(f"\n3. Variance gamma: sigma={SIG_V}, nu={NU_V}, theta={TH_V}, T=1")
    T = 1.0
    check("martingale correction omega", vg_omega(), 0.13107, 5e-6)
    price = lewis_call(lambda u: vg_cf(u, T), S0, STRIKES, T, R)
    check("K=100 VG call by Fourier", float(price[2]), 8.0441, 5e-5)
    n = 2_000_000
    G = rng.gamma(T / NU_V, NU_V, n)
    X = (R + vg_omega()) * T + TH_V * G + SIG_V * np.sqrt(G) * rng.standard_normal(n)
    pay = math.exp(-R * T) * np.maximum(S0 * np.exp(X) - 100.0, 0.0)
    check_mc(
        "K=100 VG Monte Carlo (Brownian motion in gamma time)",
        float(pay.mean()),
        float(pay.std() / math.sqrt(n)),
        8.045,
        float(price[2]),
        5e-4,
        0.0064,
        5e-5,
    )
    iv = implied_vol(price, S0, STRIKES, T, R)
    check("VG implied vol at K=80 (%)", 100 * float(iv[0]), 15.68, 5e-3)
    check("VG implied vol at K=100 (%)", 100 * float(iv[2]), 13.50, 5e-3)
    check("VG implied vol at K=120 (%)", 100 * float(iv[4]), 11.95, 5e-3)
    # Levy measure form: nu(dx) = C exp(G x)/|x| (x < 0), C exp(-M x)/x (x > 0), C = 1/nu
    a = math.sqrt(0.25 * TH_V**2 * NU_V**2 + 0.5 * SIG_V**2 * NU_V)
    Gp, Mp = 1 / (a - 0.5 * TH_V * NU_V), 1 / (a + 0.5 * TH_V * NU_V)
    check("CGMY G (decay rate of down jumps)", Gp, 18.37, 5e-3)
    check("CGMY M (decay rate of up jumps)", Mp, 37.81, 5e-3)
    check("G / M (left-tail decay relative to right)", Gp / Mp, 0.49, 5e-3)
    u = np.linspace(-30, 30, 61)
    cgmy = (Gp * Mp / ((Mp - 1j * u) * (Gp + 1j * u))) ** (T / NU_V)
    base = (1 - 1j * u * TH_V * NU_V + 0.5 * SIG_V**2 * NU_V * u * u) ** (-T / NU_V)
    check("max |CGMY(Y=0) cf - VG cf| on u in [-30, 30]", float(np.max(np.abs(cgmy - base))), 0.0, 1e-15)


# ----------------------------------------------------------------------------------------------
# 4. Levy-Khintchine sanity checks
# ----------------------------------------------------------------------------------------------


def levy_khintchine() -> None:
    """Backs 'Core concepts > Levy processes and the Levy-Khintchine formula'; card sc-levy-martingale-condition."""
    print("\n4. Levy-Khintchine: martingale condition and infinite divisibility")
    for name, cf in (("Merton", merton_cf), ("Kou", kou_cf), ("VG", vg_cf)):
        mart = complex(cf(np.array([-1j]), 1.0)[0])
        check(f"{name}: phi_1(-i) / e^r", abs(mart / math.exp(R)), 1.0, 1e-12)
        u = np.linspace(-20, 20, 41)
        check(f"{name}: max |phi_2(u) - phi_1(u)^2|", float(np.max(np.abs(cf(u, 2.0) - cf(u, 1.0) ** 2))), 0.0, 1e-12)


# ----------------------------------------------------------------------------------------------
# 5. Gap risk
# ----------------------------------------------------------------------------------------------


def gap_risk() -> None:
    """Backs 'Worked examples > The gap a delta hedge cannot cover'; card sc-jump-hedging-gap."""
    print("\n5. Gap risk: short 3m ATM call, sigma 20%, delta-hedged, spot jumps -20%")
    S, K, T, r, sig = 100.0, 100.0, 0.25, 0.05, 0.20
    sd = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sig**2) * T) / sd
    delta = float(ncdf(d1))
    V0 = float(bs_call(S, K, T, r, sig))
    V1 = float(bs_call(80.0, K, T, r, sig))
    loss = (V1 - V0) - delta * (80.0 - S)  # change in long option minus hedge: the short position loses this
    check("call price", V0, 4.6150, 5e-5)
    check("delta", delta, 0.5695, 5e-5)
    check("call after the jump to 80", V1, 0.0564, 5e-5)
    check("delta-hedged short call loss on the jump", loss, 6.83, 5e-3)
    check("loss as a multiple of the premium collected", loss / V0, 1.48, 5e-3)
    check("short call gain on the jump V0 - V1", V0 - V1, 4.56, 5e-3)
    check("hedge loss delta x 20", delta * 20.0, 11.39, 5e-3)
    check("same loss as days of theta at sigma = 20% (theta per day)", loss / (V0 - float(bs_call(S, K, T - 1 / 365, r, sig))), 237.5, 0.05)


def main() -> None:
    rng = np.random.default_rng(1976)
    merton(rng)
    kou(rng)
    variance_gamma(rng)
    levy_khintchine()
    gap_risk()
    print("\nall checks passed")


if __name__ == "__main__":
    main()
