"""Stochastic volatility: Heston by Fourier inversion and Monte Carlo, Heston calibration, SABR (Hagan 2002).

Backs every number in ``05-Derivatives-and-Volatility/09-Stochastic-Volatility-Heston-and-SABR.md``.
Run from the repo root:

    uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/heston_sabr.py

Sections:
1. Heston semi-closed form two ways (Lewis single integral, Heston's P1 / P2 by Gil-Pelaez) and the xi -> 0 Black-Scholes limit.
2. Heston Monte Carlo (full-truncation Euler, antithetic) against the Fourier price.
3. Parameter effects on the one-year smile, and the ATM skew term structure against the rho xi / (4 sqrt v0) limit.
4. Calibration to a synthetic surface by Levenberg-Marquardt on implied vols.
5. SABR: Hagan's lognormal formula, ATM limit, backbone, beta and rho effects, Hagan versus Monte Carlo,
   negative density at low strikes for a long expiry, shifted SABR for a negative forward.
Every printed number is asserted against the value quoted in the note.
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price, heston_call, heston_cf, implied_vol, lewis_call, self_test


def show(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> None:
    print(f"{label:<62s} {value:{fmt}}")
    assert abs(value - expected) <= tol, f"{label}: {value} vs {expected}"


def show_row(label: str, values: np.ndarray, expected: list[float], tol: float, fmt: str = "7.2f") -> None:
    print(f"{label:<34s}" + "".join(f"{v:{fmt}}" for v in values))
    assert np.allclose(values, expected, atol=tol), f"{label}: {values} vs {expected}"


# ---------------------------------------------------------------------------
# Heston
# ---------------------------------------------------------------------------

S0, R, Q = 100.0, 0.02, 0.0
BASE = {"kappa": 1.5, "theta": 0.04, "xi": 0.6, "rho": -0.7, "v0": 0.04}
STRIKES = np.array([80.0, 90.0, 100.0, 110.0, 120.0])


def h_call(K: np.ndarray, T: float, p: dict[str, float], u_max: float = 200.0) -> np.ndarray:
    if u_max == 200.0:
        return np.atleast_1d(heston_call(S0, K, T, R, Q, p["kappa"], p["theta"], p["xi"], p["rho"], p["v0"]))
    return np.atleast_1d(lewis_call(lambda u: heston_cf(u, T, R, Q, **p), S0, K, T, R, Q, u_max=u_max))


def h_vols(K: np.ndarray, T: float, p: dict[str, float], u_max: float = 200.0) -> np.ndarray:
    return np.atleast_1d(implied_vol(h_call(K, T, p, u_max), S0, K, T, R, Q))


def heston_p1p2(K: float, T: float, p: dict[str, float]) -> tuple[float, float, float]:
    """Heston's original form C = S e^{-qT} P1 - K e^{-rT} P2 with Gil-Pelaez inversion.

    P2 = Q(S_T > K); P1 = Q^S(S_T > K), the exercise probability under the share measure.
    """
    nodes, weights = np.polynomial.legendre.leggauss(400)
    u = 100.0 * (nodes + 1.0) + 1e-10
    w = 100.0 * weights

    def phi(z: np.ndarray) -> np.ndarray:  # characteristic function of ln S_T
        return np.exp(1j * z * math.log(S0)) * heston_cf(z, T, R, Q, **p)

    lnk = math.log(K)
    f2 = phi(u)
    f1 = phi(u - 1j) / (S0 * math.exp((R - Q) * T))
    P2 = 0.5 + np.sum(w * np.real(np.exp(-1j * u * lnk) * f2 / (1j * u))) / math.pi
    P1 = 0.5 + np.sum(w * np.real(np.exp(-1j * u * lnk) * f1 / (1j * u))) / math.pi
    price = S0 * math.exp(-Q * T) * P1 - K * math.exp(-R * T) * P2
    return float(P1), float(P2), float(price)


def heston_mc(K: np.ndarray, T: float, p: dict[str, float], n_steps: int, n_pairs: int, seed: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Full-truncation Euler (Lord, Koekkoek and van Dijk 2010) in log price, antithetic pairs."""
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    n = 2 * n_pairs
    x = np.zeros(n)
    v = np.full(n, p["v0"])
    rho, xi, kappa, theta = p["rho"], p["xi"], p["kappa"], p["theta"]
    sq = math.sqrt(1 - rho * rho)
    negatives = 0
    for _ in range(n_steps):
        z1 = rng.standard_normal(n_pairs)
        z2 = rng.standard_normal(n_pairs)
        z1 = np.concatenate([z1, -z1])
        z2 = np.concatenate([z2, -z2])
        zv = rho * z1 + sq * z2
        vp = np.maximum(v, 0.0)
        negatives += int(np.count_nonzero(v < 0))
        x += (R - Q - 0.5 * vp) * dt + np.sqrt(vp * dt) * z1
        v = v + kappa * (theta - vp) * dt + xi * np.sqrt(vp * dt) * zv
    ST = S0 * np.exp(x)
    pay = np.maximum(ST[:, None] - K[None, :], 0.0) * math.exp(-R * T)
    pair = 0.5 * (pay[:n_pairs] + pay[n_pairs:])
    return pair.mean(0), pair.std(0, ddof=1) / math.sqrt(n_pairs), negatives / (n * n_steps)


def to_params(z: np.ndarray) -> dict[str, float]:
    """Unconstrained z -> Heston parameters: logs for positive ones, tanh for rho."""
    return {"kappa": math.exp(z[0]), "theta": math.exp(z[1]), "xi": math.exp(z[2]), "rho": math.tanh(z[3]), "v0": math.exp(z[4])}


def from_params(p: dict[str, float]) -> np.ndarray:
    return np.array([math.log(p["kappa"]), math.log(p["theta"]), math.log(p["xi"]), math.atanh(p["rho"]), math.log(p["v0"])])


def calibrate(quotes: dict[float, np.ndarray], start: dict[str, float], iters: int = 50) -> tuple[dict[str, float], float, int, np.ndarray]:
    """Levenberg-Marquardt on implied-vol residuals with a forward-difference Jacobian."""

    def resid(z: np.ndarray) -> np.ndarray:
        p = to_params(z)
        return np.concatenate([h_vols(STRIKES, T, p) - q for T, q in quotes.items()])

    z = from_params(start)
    r = resid(z)
    lam = 1e-2
    it = 0
    for _it in range(1, iters + 1):
        it = _it
        J = np.empty((r.size, z.size))
        for j in range(z.size):
            dz = np.zeros_like(z)
            dz[j] = 1e-6
            J[:, j] = (resid(z + dz) - r) / 1e-6
        A = J.T @ J
        g = J.T @ r
        while True:
            step = np.linalg.solve(A + lam * np.diag(np.diag(A)), -g)
            r_new = resid(z + step)
            if r_new @ r_new < r @ r:
                z, r = z + step, r_new
                lam = max(lam / 3.0, 1e-9)
                break
            lam *= 4.0
            if lam > 1e8:
                break
        if math.sqrt(np.mean(r * r)) < 1e-9 or lam > 1e8:
            break
    sv = np.linalg.svd(J, compute_uv=False)
    return to_params(z), math.sqrt(np.mean(r * r)), it, sv


# ---------------------------------------------------------------------------
# SABR
# ---------------------------------------------------------------------------


def hagan_vol(F: float, K: np.ndarray, T: float, alpha: float, beta: float, rho: float, nu: float) -> np.ndarray:
    """Hagan, Kumar, Lesniewski and Woodward (2002) lognormal (Black) implied vol, eq. (2.17a)."""
    K = np.atleast_1d(np.asarray(K, dtype=float))
    lfk = np.log(F / K)
    fk = (F * K) ** ((1.0 - beta) / 2.0)
    omb = 1.0 - beta
    denom = fk * (1.0 + omb**2 / 24.0 * lfk**2 + omb**4 / 1920.0 * lfk**4)
    z = nu / alpha * fk * lfk
    with np.errstate(divide="ignore", invalid="ignore"):
        xz = np.log((np.sqrt(1.0 - 2.0 * rho * z + z * z) + z - rho) / (1.0 - rho))
        zx = np.where(np.abs(z) < 1e-12, 1.0, z / xz)
    corr = 1.0 + (omb**2 / 24.0 * alpha**2 / fk**2 + 0.25 * rho * beta * nu * alpha / fk + (2.0 - 3.0 * rho * rho) / 24.0 * nu * nu) * T
    return alpha / denom * zx * corr


def hagan_atm(F: float, T: float, alpha: float, beta: float, rho: float, nu: float) -> float:
    omb = 1.0 - beta
    fb = F**omb
    return (
        alpha
        / fb
        * (1.0 + (omb**2 / 24.0 * alpha**2 / fb**2 + 0.25 * rho * beta * nu * alpha / fb + (2.0 - 3.0 * rho**2) / 24.0 * nu**2) * T)
    )


def alpha_for_atm(target: float, F: float, T: float, beta: float, rho: float, nu: float) -> float:
    lo, hi = 1e-8, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if hagan_atm(F, T, mid, beta, rho, nu) < target else (lo, mid)
    return 0.5 * (lo + hi)


def black_call(F: float, K: np.ndarray, T: float, vol: np.ndarray) -> np.ndarray:
    """Undiscounted Black-76 call (per unit annuity)."""
    return np.atleast_1d(np.asarray(bs_price(F, K, T, 0.0, vol)))


def sabr_mc(F: float, K: np.ndarray, T: float, alpha: float, beta: float, rho: float, nu: float, n_steps: int, n_pairs: int, seed: int):
    """Euler in F with absorption at zero, exact lognormal alpha; antithetic pairs."""
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    n = 2 * n_pairs
    f = np.full(n, F)
    a = np.full(n, alpha)
    sq = math.sqrt(1 - rho * rho)
    for _ in range(n_steps):
        z1 = rng.standard_normal(n_pairs)
        z2 = rng.standard_normal(n_pairs)
        z1 = np.concatenate([z1, -z1])
        z2 = np.concatenate([z2, -z2])
        zf = rho * z2 + sq * z1
        f = np.maximum(f + a * f**beta * math.sqrt(dt) * zf, 0.0)
        a = a * np.exp(nu * math.sqrt(dt) * z2 - 0.5 * nu * nu * dt)
    pay = np.maximum(f[:, None] - K[None, :], 0.0)
    pair = 0.5 * (pay[:n_pairs] + pay[n_pairs:])
    return pair.mean(0), pair.std(0, ddof=1) / math.sqrt(n_pairs), float(np.mean(f == 0.0))


def main() -> None:
    self_test()  # the shared Lewis pricer must reproduce Black-Scholes before any Heston number is trusted
    # Note 09 Example 1 and cards deriv-heston-feller, deriv-heston-sde
    p = BASE
    print("Heston base: S0 = 100, r = 2%, q = 0,", p)
    show("Feller 2 kappa theta", 2 * p["kappa"] * p["theta"], 0.12, 1e-12, ".2f")
    show("xi^2", p["xi"] ** 2, 0.36, 1e-12, ".2f")

    # 1. Semi-closed form two ways: Example 1, card deriv-heston-p1-p2 (P1 / P2 cross-checked against the Lewis integral)
    T = 1.0
    c_lewis = h_call(STRIKES, T, p)
    show_row("1. Heston one-year calls (Lewis)", c_lewis, [23.2796, 15.0161, 7.9561, 3.0102, 0.8044], 5e-5, "9.4f")
    for K, c in zip(STRIKES, c_lewis, strict=True):
        P1, P2, c_hp = heston_p1p2(float(K), T, p)
        print(f"   K = {K:5.1f}: P1 {P1:.4f}  P2 {P2:.4f}  P1/P2 price {c_hp:.4f}  |diff| {abs(c_hp - c):.1e}")
        assert abs(c_hp - c) < 1e-8
    P1, P2, _ = heston_p1p2(100.0, T, p)
    show("P1 (share-measure exercise probability), K = 100", P1, 0.6982, 5e-5)
    show("P2 (risk-neutral exercise probability), K = 100", P2, 0.6311, 5e-5)
    show_row("   implied vols (%)", 100 * h_vols(STRIKES, T, p), [23.89, 20.68, 17.54, 14.85, 13.44], 0.005)

    # Variance swap strike from the 1/K^2 strip of Heston OTM prices against the closed form (1/T) int E[v_t] dt;
    # backs card deriv-heston-atm-below-varswap
    F1 = S0 * math.exp((R - Q) * T)
    Kgrid = np.exp(np.linspace(math.log(2.0), math.log(5000.0), 6000))
    calls = h_call(Kgrid, T, p)
    otm = np.where(Kgrid < F1, calls - math.exp(-R * T) * (F1 - Kgrid), calls) / Kgrid**2
    k_var = 2 * math.exp(R * T) / T * float(np.sum(0.5 * (otm[1:] + otm[:-1]) * np.diff(Kgrid)))
    closed = p["theta"] + (p["v0"] - p["theta"]) * (1 - math.exp(-p["kappa"] * T)) / (p["kappa"] * T)
    show("variance swap strike from the 1/K^2 strip of Heston prices", k_var, closed, 1e-6, ".5f")
    show("  as a vol (%)", 100 * math.sqrt(k_var), 20.00, 0.005, ".2f")
    show("ATM-forward implied vol (%)", 100 * float(h_vols(np.array([F1]), T, p)[0]), 16.94, 0.005, ".2f")

    # xi -> 0: Black-Scholes with the average expected variance; Example 1, card deriv-heston-xi-zero-limit
    p0 = dict(p, xi=0.001, rho=0.0, v0=0.09)
    avg_var = p0["theta"] + (p0["v0"] - p0["theta"]) * (1 - math.exp(-p0["kappa"] * T)) / (p0["kappa"] * T)
    bs = np.asarray(bs_price(S0, STRIKES, T, R, math.sqrt(avg_var), Q))
    show("xi = 0.001, rho = 0, v0 = 0.09: BS vol sqrt(average variance) (%)", 100 * math.sqrt(avg_var), 25.67, 0.005, ".2f")
    show("  max |Heston - BS| price", float(np.max(np.abs(h_call(STRIKES, T, p0) - bs))), 2.7e-6, 5e-7, ".1e")

    # 2. Monte Carlo against the Fourier price: Example 2, card deriv-heston-mc-scheme
    print("2. Full-truncation Euler, 2 x 100,000 antithetic paths, seed 11")
    expected_mc = {
        25: ([23.2961, 15.0613, 8.0231, 3.0849, 0.8498], [0.0236, 0.0202, 0.0166, 0.0123, 0.0076], 18.5, [0.7, 2.2, 4.0, 6.0, 6.0]),
        200: ([23.2944, 15.0264, 7.9594, 3.0087, 0.7987], [0.0231, 0.0196, 0.0160, 0.0119, 0.0073], 8.8, [0.6, 0.5, 0.2, -0.1, -0.8]),
    }
    for steps, (e_mc, e_se, e_neg, e_z) in expected_mc.items():
        mc, se, neg = heston_mc(STRIKES, T, p, steps, 100_000, seed=11)
        show_row(f"   {steps} steps: MC price", mc, e_mc, 5e-5, "9.4f")
        show_row(f"   {steps} steps: s.e.", se, e_se, 5e-5, "9.4f")
        show_row(f"   {steps} steps: (MC - Fourier) / s.e.", (mc - c_lewis) / se, e_z, 0.05, "9.1f")
        show(f"   share of variance steps truncated ({steps} steps, %)", 100 * neg, e_neg, 0.05, ".1f")
        if steps == 200:
            assert np.all(np.abs(mc - c_lewis) < 2 * se), "200-step MC must agree with Fourier within 2 s.e."
        else:
            assert np.max((mc - c_lewis) / se) > 5.5, "25-step bias must be visible"

    # 3. Parameter effects on the smile: Example 3, cards deriv-heston-rho-xi-effects, deriv-heston-kappa-effect
    print("3. One-year implied vols (%) at strikes", STRIKES)
    rows = {
        "base": ({}, [23.89, 20.68, 17.54, 14.85, 13.44]),
        "rho = 0": ({"rho": 0.0}, [20.73, 18.87, 17.94, 18.29, 19.40]),
        "rho = +0.5": ({"rho": 0.5}, [16.84, 16.41, 17.67, 19.86, 22.05]),
        "xi = 0.3": ({"xi": 0.3}, [22.81, 20.99, 19.26, 17.68, 16.34]),
        "xi = 0.9": ({"xi": 0.9}, [23.94, 19.84, 15.79, 12.63, 12.17]),
        "kappa = 0.5": ({"kappa": 0.5}, [24.28, 20.22, 16.03, 12.77, 12.55]),
        "kappa = 5": ({"kappa": 5.0}, [22.70, 20.90, 19.25, 17.77, 16.50]),
        "v0 = 0.02": ({"v0": 0.02}, [21.55, 18.26, 14.99, 12.26, 11.36]),
        "v0 = 0.08": ({"v0": 0.08}, [27.82, 24.84, 21.98, 19.44, 17.60]),
        "theta = 0.08": ({"theta": 0.08}, [27.37, 24.68, 22.15, 19.90, 18.18]),
    }
    for name, (chg, e) in rows.items():
        show_row(f"   {name}", 100 * h_vols(STRIKES, T, dict(p, **chg)), e, 0.005)

    # ATM skew term structure: Example 4, card deriv-heston-short-skew
    print("ATM-forward skew d sigma / dk (k = ln K / F) versus the T -> 0 limit rho xi / (4 sqrt v0)")
    show("   limit rho xi / (4 sqrt v0)", p["rho"] * p["xi"] / (4 * math.sqrt(p["v0"])), -0.525, 1e-12, ".3f")
    for t, e in ((0.01, -0.526), (0.1, -0.530), (0.25, -0.499), (1.0, -0.300), (3.0, -0.148)):
        F = S0 * math.exp((R - Q) * t)
        Ks = F * np.exp(np.array([-0.01, 0.01]))
        v = h_vols(Ks, t, p, u_max=2000.0)
        show(f"   T = {t}", float((v[1] - v[0]) / 0.02), e, 5e-4, ".3f")

    # 4. Calibration (recovered parameters compared with the generating ones): Example 5, card deriv-heston-identifiability
    print("4. Calibration to a synthetic surface (T = 0.25, 0.5, 1, 2; strikes 80-120)")
    quotes = {t: h_vols(STRIKES, t, p) for t in (0.25, 0.5, 1.0, 2.0)}
    start = {"kappa": 3.0, "theta": 0.06, "xi": 0.3, "rho": -0.3, "v0": 0.06}
    fit, rmse, it, sv = calibrate(quotes, start)
    print("   start", start)
    for kname in ("kappa", "theta", "xi", "rho", "v0"):
        show(f"   recovered {kname}", fit[kname], p[kname], 5e-5)
    show("   RMSE (vol points, below 1e-8)", 100 * rmse, 0.0, 1e-8, ".1e")
    show("   iterations", it, 11, 0, "d")
    show("   Jacobian condition number (largest / smallest singular value)", float(sv[0] / sv[-1]), 16.0, 0.5, ".0f")
    fit1, rmse1, _, sv1 = calibrate({1.0: quotes[1.0]}, start)
    for kname, e in (("kappa", 1.5937), ("theta", 0.0318), ("xi", 0.5916), ("rho", -0.6967), ("v0", 0.0480)):
        show(f"   one maturity only: {kname}", fit1[kname], e, 5e-5)
    show("   one-maturity RMSE (vol points)", 100 * rmse1, 6.3e-4, 5e-6, ".1e")
    show("   one-maturity condition number", float(sv1[0] / sv1[-1]), 3749.0, 0.5, ".0f")

    # 5. SABR alpha, beta / rho table and backbone: Example 6, cards deriv-sabr-atm-alpha, deriv-sabr-backbone, deriv-sabr-beta-rho
    F, Ts, beta, rho, nu = 0.03, 1.0, 0.5, -0.3, 0.4
    alpha = alpha_for_atm(0.20, F, Ts, beta, rho, nu)
    print("5. SABR F = 3%, T = 1, beta = 0.5, rho = -0.3, nu = 0.4, ATM 20%")
    show("   alpha", alpha, 0.03433, 5e-6, ".5f")
    show("   leading-order alpha / F^(1 - beta) (%)", 100 * alpha / F ** (1 - beta), 19.82, 0.005, ".2f")
    show(
        "   |general formula at K = F - ATM formula| (below 1e-15)",
        float(abs(hagan_vol(F, np.array([F]), Ts, alpha, beta, rho, nu)[0] - hagan_atm(F, Ts, alpha, beta, rho, nu))),
        0.0,
        1e-15,
        ".1e",
    )
    Ksabr = np.array([0.02, 0.025, 0.03, 0.035, 0.04])
    print("   strikes (%)", 100 * Ksabr)
    for name, b_, r_, n_, e in (
        ("beta 0, rho 0", 0.0, 0.0, 0.4, [25.99, 22.29, 20.00, 18.84, 18.42]),
        ("beta 0.5, rho 0", 0.5, 0.0, 0.4, [23.88, 21.35, 20.00, 19.57, 19.70]),
        ("beta 1, rho 0", 1.0, 0.0, 0.4, [21.93, 20.44, 20.00, 20.32, 21.04]),
        ("beta 0.5, rho -0.3", 0.5, -0.3, 0.4, [25.77, 22.35, 20.00, 18.63, 18.05]),
        ("beta 0.5, rho -0.6", 0.5, -0.6, 0.4, [27.42, 23.25, 20.00, 17.59, 16.06]),
        ("beta 0.5, rho +0.3", 0.5, 0.3, 0.4, [21.65, 20.24, 20.00, 20.43, 21.13]),
        ("beta 0.5, rho -0.3, nu 0.8", 0.5, -0.3, 0.8, [30.77, 24.33, 20.00, 18.73, 19.70]),
    ):
        a_ = alpha_for_atm(0.20, F, Ts, b_, r_, n_)
        show_row(f"   {name}", 100 * hagan_vol(F, Ksabr, Ts, a_, b_, r_, n_), e, 0.005)

    print("   backbone: ATM vol (%) as F moves with alpha fixed (rho = 0, nu = 0.4)")
    for b_, e in ((0.0, [30.06, 20.00, 14.99]), (0.5, [24.50, 20.00, 17.32]), (1.0, [20.00, 20.00, 20.00])):
        a_ = alpha_for_atm(0.20, F, Ts, b_, 0.0, 0.4)
        atm = np.array([100 * hagan_atm(f_, Ts, a_, b_, 0.0, 0.4) for f_ in (0.02, 0.03, 0.04)])
        show_row(f"   beta {b_}, F = 2%, 3%, 4%", atm, e, 0.005)

    # Hagan versus Monte Carlo: Example 7, card deriv-sabr-accuracy
    Kmc = np.array([0.02, 0.025, 0.03, 0.035, 0.04, 0.05])
    expected_sabr = {
        1.0: (
            [25.77, 22.35, 20.00, 18.63, 18.05, 18.23],
            [25.80, 22.38, 20.06, 18.71, 18.09, 18.30],
            [0.16, 0.06, 0.05, 0.05, 0.05, 0.14],
            0.0,
            [-0.03, -0.03, -0.06, -0.08, -0.04, -0.07],
            [-0.2, -0.5, -1.1, -1.8, -0.7, -0.5],
        ),
        10.0: (
            [26.09, 22.47, 20.00, 18.62, 18.13, 18.57],
            [23.09, 20.34, 18.46, 17.35, 16.88, 16.97],
            [0.15, 0.12, 0.10, 0.09, 0.09, 0.10],
            8.46,
            [3.00, 2.13, 1.54, 1.27, 1.26, 1.60],
            [19.7, 18.2, 15.5, 13.7, 13.5, 15.4],
        ),
    }
    for (T_, steps), (e_h, e_mc, e_se, e_abs, e_diff, e_z) in zip(((1.0, 250), (10.0, 500)), expected_sabr.values(), strict=True):
        a_ = alpha_for_atm(0.20, F, T_, beta, rho, nu)
        mc, se, absorbed = sabr_mc(F, Kmc, T_, a_, beta, rho, nu, steps, 100_000, seed=5)
        iv_mc = 100 * np.atleast_1d(implied_vol(mc, F, Kmc, T_, 0.0))
        iv_h = 100 * hagan_vol(F, Kmc, T_, a_, beta, rho, nu)
        vega = np.asarray(bs_price(F, Kmc, T_, 0.0, iv_mc / 100 + 1e-4)) - np.asarray(bs_price(F, Kmc, T_, 0.0, iv_mc / 100 - 1e-4))
        print(f"   T = {T_} ({steps} steps, 2 x 100,000 paths, seed 5): strikes {100 * Kmc}")
        show_row("     Hagan", iv_h, e_h, 0.005)
        show_row("     Monte Carlo", iv_mc, e_mc, 0.005)
        show_row("     Monte Carlo s.e. (vol points)", 2e-2 * se / vega, e_se, 0.005)
        show_row("     Hagan - Monte Carlo (vol points)", iv_h - iv_mc, e_diff, 0.005)
        show_row("     (Hagan - Monte Carlo) / s.e.", (iv_h - iv_mc) / (2e-2 * se / vega), e_z, 0.05, "7.1f")
        show(f"     share of paths absorbed at zero (T = {T_}, %)", 100 * absorbed, e_abs, 0.005, ".2f")

    # Density from Hagan prices: Example 7, card deriv-sabr-negative-density
    Kd = np.linspace(0.0005, 0.03, 600)
    h = 1e-5
    print(f"5c. Density d2C/dK2 from Hagan vols, beta {beta}, rho {rho}, nu {nu}, ATM 20%, K in [0.05%, 3%]")
    for T_, e_min, e_below, e_mass in ((1.0, 5.26e-3, 0.0, 0.0), (10.0, -111.9, 0.70, -0.113)):
        a_ = alpha_for_atm(0.20, F, T_, beta, rho, nu)
        c = [black_call(F, Kd + s_ * h, T_, hagan_vol(F, Kd + s_ * h, T_, a_, beta, rho, nu)) for s_ in (-1, 0, 1)]
        dens = (c[0] - 2 * c[1] + c[2]) / h**2
        show(f"   T = {T_}: min density", float(dens.min()), e_min, max(5e-5, 0.05 * abs(e_min)), ".2e")
        neg = Kd[dens < 0]
        show(f"   T = {T_}: density < 0 for K below (%)", 100 * float(neg.max()) if neg.size else 0.0, e_below, 0.005, ".2f")
        mass = float(np.sum(np.minimum(dens, 0.0)) * (Kd[1] - Kd[0]))
        show(f"   T = {T_}: negative probability mass", mass, e_mass, 5e-4, ".3f")

    # Shifted SABR for a negative forward: Example 8, card deriv-sabr-shifted
    Fn, s = -0.002, 0.02
    print("5d. Shifted SABR: F = -0.2%, shift 2%, alpha 0.03, beta 0.5, rho -0.2, nu 0.4, T = 1")
    with np.errstate(invalid="ignore"):
        plain = hagan_vol(Fn, np.array([0.001]), 1.0, 0.03, 0.5, -0.2, 0.4)
    print("   unshifted formula at F < 0:", plain)
    assert np.isnan(plain).all()
    Kn = np.array([-0.005, -0.002, 0.0, 0.005, 0.01])
    vols = hagan_vol(Fn + s, Kn + s, 1.0, 0.03, 0.5, -0.2, 0.4)
    show_row("   strikes -0.5%, -0.2%, 0, 0.5%, 1%: vols (%)", 100 * vols, [24.71, 22.60, 21.72, 20.86, 21.06], 0.005)
    show_row("   shifted Black prices (bp)", 1e4 * black_call(Fn + s, Kn + s, 1.0, vols), [35.41, 16.20, 8.32, 1.09, 0.12], 0.005, "8.2f")


if __name__ == "__main__":
    main()
