"""Vasicek, CIR and Hull-White: closed forms checked against Monte Carlo and a PDE solver.

Backs every number in note 04 (Short-Rate Models).
- Vasicek bond prices against Monte Carlo of the exact OU transition with trapezoid integration.
- CIR bond prices against a Crank-Nicolson solution of the bond-pricing PDE, and the Feller condition in simulation.
- Hull-White: the theta(t) that fits a given curve is checked by simulating the SDE with that theta and recovering
  the market discount factors; zero-bond options and the Jamshidian swaption are checked against Monte Carlo.
Simulation results are quoted in the note as "about" the seed-stable printed value; asserts use multiples of the
Monte Carlo standard error, never a loosened tolerance.
Each `q(...)` asserts a computed value against the literal quoted in the note and prints it.
Run with `python 06-Fixed-Income-and-Asset-Classes/code/fi_short_rate.py`.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from statistics import NormalDist

import numpy as np

N01 = NormalDist()


def q(tag: str, label: str, value: float, text: str) -> None:
    """Assert that `value` rounds to the quoted `text` (half a unit of its last decimal) and print it."""
    decimals = len(text.split(".")[1]) if "." in text else 0
    literal = float(text.replace(",", ""))
    assert abs(value - literal) <= 0.5 * 10.0**-decimals + 1e-12, f"[{tag}] {label}: computed {value!r}, note quotes {text}"
    print(f"  [{tag}] {label} = {text}")


# ------------------------------------------------------------ Vasicek


def vasicek_b(k: float, tau: float) -> float:
    return (1 - math.exp(-k * tau)) / k


def vasicek_price(r: float, tau: float, k: float, theta: float, sigma: float) -> float:
    """P = A exp(-B r), ln A = (theta - sigma^2/(2k^2))(B - tau) - sigma^2 B^2/(4k)."""
    b = vasicek_b(k, tau)
    ln_a = (theta - sigma**2 / (2 * k**2)) * (b - tau) - sigma**2 * b**2 / (4 * k)
    return math.exp(ln_a - b * r)


def vasicek_mc(
    r0: float, tau: float, k: float, theta: float, sigma: float, n_paths: int, n_steps: int, seed: int
) -> tuple[float, float, float]:
    """(price, standard error, fraction of paths with r_T < 0) using the exact OU transition on a grid and trapezoid integration."""
    rng = np.random.default_rng(seed)
    dt = tau / n_steps
    decay = math.exp(-k * dt)
    sd = sigma * math.sqrt((1 - decay**2) / (2 * k))
    half = n_paths // 2
    r = np.full(n_paths, r0)
    integral = np.zeros(n_paths)
    for _ in range(n_steps):
        z = rng.standard_normal(half)
        z = np.concatenate([z, -z])  # antithetic pairs
        r_new = theta + (r - theta) * decay + sd * z
        integral += 0.5 * (r + r_new) * dt
        r = r_new
    disc = np.exp(-integral)
    pair_means = 0.5 * (disc[:half] + disc[half:])
    return float(disc.mean()), float(pair_means.std(ddof=1) / math.sqrt(half)), float((r < 0).mean())


# ------------------------------------------------------------ CIR


def cir_price(r: float, tau: float, k: float, theta: float, sigma: float) -> float:
    """Cox-Ingersoll-Ross (1985) zero-coupon bond price."""
    g = math.sqrt(k * k + 2 * sigma * sigma)
    e = math.exp(g * tau) - 1
    den = (g + k) * e + 2 * g
    b = 2 * e / den
    a = (2 * g * math.exp((k + g) * tau / 2) / den) ** (2 * k * theta / sigma**2)
    return a * math.exp(-b * r)


def cir_pde_price(
    r0: float, tau: float, k: float, theta: float, sigma: float, r_max: float = 0.6, n_r: int = 600, n_t: int = 4096
) -> float:
    """Crank-Nicolson for P_tau = k(theta - r)P_r + 0.5 sigma^2 r P_rr - r P, P(r, 0) = 1.

    At r = 0 the diffusion vanishes and the drift k theta > 0 points into the domain, so a one-sided
    (upwind) difference is used; at r_max the solution is taken as linear (P_rr = 0).
    The time-stepping matrix is constant, so it is raised to the n_t-th power by repeated squaring.
    """
    dr = r_max / n_r
    r = np.linspace(0.0, r_max, n_r + 1)
    lap = np.zeros((n_r + 1, n_r + 1))
    for i in range(1, n_r):
        drift, diff = k * (theta - r[i]), 0.5 * sigma**2 * r[i]
        lap[i, i - 1] = diff / dr**2 - drift / (2 * dr)
        lap[i, i] = -2 * diff / dr**2 - r[i]
        lap[i, i + 1] = diff / dr**2 + drift / (2 * dr)
    lap[0, 0], lap[0, 1] = -k * theta / dr, k * theta / dr  # P_tau = k theta P_r at r = 0 (r P term is zero)
    drift_n = k * (theta - r[-1])
    lap[-1, -2], lap[-1, -1] = -drift_n / dr, drift_n / dr - r[-1]  # P_rr = 0, backward difference for P_r
    dt = tau / n_t
    eye = np.eye(n_r + 1)
    step = np.linalg.solve(eye - 0.5 * dt * lap, eye + 0.5 * dt * lap)
    power, mat, n = eye, step, n_t
    while n:
        if n & 1:
            power = power @ mat
        mat = mat @ mat
        n >>= 1
    values = power @ np.ones(n_r + 1)
    return float(np.interp(r0, r, values))


def cir_euler_stats(
    r0: float, tau: float, k: float, theta: float, sigma: float, n_paths: int, n_steps: int, seed: int
) -> tuple[float, float, float]:
    """Full-truncation Euler (Lord, Koekkoek and van Dijk 2010): returns (price, standard error, share of steps that went negative)."""
    rng = np.random.default_rng(seed)
    dt = tau / n_steps
    r = np.full(n_paths, r0)
    integral = np.zeros(n_paths)
    negative = 0
    for _ in range(n_steps):
        rp = np.maximum(r, 0.0)
        r_new = r + k * (theta - rp) * dt + sigma * np.sqrt(rp * dt) * rng.standard_normal(n_paths)
        negative += int((r_new < 0).sum())
        integral += 0.5 * (rp + np.maximum(r_new, 0.0)) * dt
        r = r_new
    disc = np.exp(-integral)
    return float(disc.mean()), float(disc.std(ddof=1) / math.sqrt(n_paths)), negative / (n_paths * n_steps)


# ------------------------------------------------------------ Hull-White one factor


def ns_zero(t: float, b0: float = 0.045, b1: float = -0.01, b2: float = 0.01, lam: float = 2.0) -> float:
    """Hypothetical Nelson-Siegel continuous zero curve used as the 'market' curve."""
    x = t / lam
    g = (1 - math.exp(-x)) / x
    return b0 + b1 * g + b2 * (g - math.exp(-x))


def ns_df(t: float) -> float:
    return 1.0 if t == 0 else math.exp(-ns_zero(t) * t)


def ns_forward_and_slope(t: float, b0: float = 0.045, b1: float = -0.01, b2: float = 0.01, lam: float = 2.0) -> tuple[float, float]:
    """Analytic Nelson-Siegel instantaneous forward f(0,t) = b0 + b1 e^{-x} + b2 x e^{-x}, x = t/lam, and its t-derivative."""
    x = t / lam
    e = math.exp(-x)
    return b0 + b1 * e + b2 * x * e, (-b1 * e + b2 * (1 - x) * e) / lam


def inst_forward(df: Callable[[float], float], t: float, h: float = 1e-5) -> float:
    return -(math.log(df(t + h)) - math.log(df(max(t - h, 0.0)))) / (t + h - max(t - h, 0.0))


def hw_theta(df: Callable[[float], float], t: float, a: float, sigma: float, h: float = 1e-4, convexity: bool = True) -> float:
    """theta(t) = df(0,t)/dt + a f(0,t) + sigma^2/(2a) (1 - e^{-2at}) (Hull and White 1990)."""
    f = inst_forward(df, t)
    f_t = (inst_forward(df, t + h) - inst_forward(df, max(t - h, 1e-6))) / (t + h - max(t - h, 1e-6))
    return f_t + a * f + (sigma**2 / (2 * a) * (1 - math.exp(-2 * a * t)) if convexity else 0.0)


def hw_b(a: float, t: float, big_t: float) -> float:
    return (1 - math.exp(-a * (big_t - t))) / a


def hw_bond(df: Callable[[float], float], t: float, big_t: float, r_t: float, a: float, sigma: float) -> float:
    """P(t,T) = P(0,T)/P(0,t) exp(B f(0,t) - sigma^2/(4a)(1 - e^{-2at}) B^2 - B r(t)) (Brigo and Mercurio eq. 3.39)."""
    b = hw_b(a, t, big_t)
    ln_a = math.log(df(big_t) / df(t)) + b * inst_forward(df, t) - sigma**2 / (4 * a) * (1 - math.exp(-2 * a * t)) * b**2
    return math.exp(ln_a - b * r_t)


def hw_zcb_option(df: Callable[[float], float], t_exp: float, s_mat: float, strike: float, a: float, sigma: float, call: bool) -> float:
    sigma_p = sigma * math.sqrt((1 - math.exp(-2 * a * t_exp)) / (2 * a)) * hw_b(a, t_exp, s_mat)
    d1 = math.log(df(s_mat) / (strike * df(t_exp))) / sigma_p + 0.5 * sigma_p
    d2 = d1 - sigma_p
    if call:
        return df(s_mat) * N01.cdf(d1) - strike * df(t_exp) * N01.cdf(d2)
    return strike * df(t_exp) * N01.cdf(-d2) - df(s_mat) * N01.cdf(-d1)


def jamshidian_payer(df: Callable[[float], float], t_exp: float, n_years: int, strike: float, a: float, sigma: float) -> float:
    """Payer swaption, annual fixed leg, as a sum of zero-bond puts struck at P(T, T_i; r*)."""
    times = [t_exp + i for i in range(1, n_years + 1)]
    coupons = [strike] * n_years
    coupons[-1] += 1.0

    def value(r: float) -> float:
        return sum(c * hw_bond(df, t_exp, ti, r, a, sigma) for c, ti in zip(coupons, times, strict=True)) - 1.0

    lo, hi = -1.0, 1.0
    assert value(lo) > 0 > value(hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if value(mid) > 0:
            lo = mid
        else:
            hi = mid
    r_star = 0.5 * (lo + hi)
    return sum(
        c * hw_zcb_option(df, t_exp, ti, hw_bond(df, t_exp, ti, r_star, a, sigma), a, sigma, call=False)
        for c, ti in zip(coupons, times, strict=True)
    )


def hw_simulate(
    df: Callable[[float], float],
    a: float,
    sigma: float,
    horizon: float,
    n_paths: int,
    n_steps: int,
    seed: int,
    convexity: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Euler on dr = (theta(t) - a r) dt + sigma dW with antithetic normals; returns (r at horizon, integral of r)."""
    rng = np.random.default_rng(seed)
    dt = horizon / n_steps
    half = n_paths // 2
    r = np.full(n_paths, inst_forward(df, 0.0))
    integral = np.zeros(n_paths)
    for i in range(n_steps):
        t = i * dt
        z = rng.standard_normal(half)
        z = np.concatenate([z, -z])
        theta_mid = hw_theta(df, t + 0.5 * dt, a, sigma, convexity=convexity)
        r_new = r + (theta_mid - a * r) * dt + sigma * math.sqrt(dt) * z
        integral += 0.5 * (r + r_new) * dt
        r = r_new
    return r, integral


def antithetic_se(x: np.ndarray) -> float:
    half = x.size // 2
    return float((0.5 * (x[:half] + x[half:])).std(ddof=1) / math.sqrt(half))


def main() -> None:
    print("Note 04: Short-Rate Models")

    # --- Vasicek (Example 1, cards fi-short-rate-vasicek-neg-prob, fi-sr-vasicek-long-yield)
    k, theta, sigma, r0 = 0.30, 0.04, 0.01, 0.03
    p5 = vasicek_price(r0, 5.0, k, theta, sigma)
    q("ex1", "Vasicek P(0,5)", p5, "0.840865")
    q("ex1", "Vasicek 5y yield, %", 100 * -math.log(p5) / 5, "3.4665")
    q("fi-sr-vasicek-long-yield", "long yield theta - sigma^2/(2k^2), %", 100 * (theta - sigma**2 / (2 * k**2)), "3.9444")
    q("fi-sr-vasicek-long-yield", "Vasicek 100y yield, %", 100 * -math.log(vasicek_price(r0, 100.0, k, theta, sigma)) / 100, "3.9139")
    # closed form = exp(-E[I] + Var[I]/2) with the integrated OU moments (independent derivation)
    b5 = vasicek_b(k, 5.0)
    mean_i = theta * 5 + (r0 - theta) * b5
    var_i = sigma**2 / k**2 * (5 - b5 - k * b5**2 / 2)
    assert abs(math.exp(-mean_i + 0.5 * var_i) - p5) < 1e-14
    mc, se, neg_share = vasicek_mc(r0, 5.0, k, theta, sigma, 100_000, 500, seed=7)
    q("ex1", "Monte Carlo P(0,5), seed 7", mc, "0.84086")
    q("ex1", "Monte Carlo standard error (x1e6)", 1e6 * se, "4.1")
    assert abs(mc - p5) < 4 * se + 2e-6  # trapezoid bias O(dt^2) is below 1e-6 here
    m5 = theta + (r0 - theta) * math.exp(-k * 5)
    s5 = sigma * math.sqrt((1 - math.exp(-2 * k * 5)) / (2 * k))
    p_neg = N01.cdf(-m5 / s5)
    q("fi-short-rate-vasicek-neg-prob", "E[r_5], %", 100 * m5, "3.7769")
    q("fi-short-rate-vasicek-neg-prob", "sd[r_5], %", 100 * s5, "1.2584")
    q("fi-short-rate-vasicek-neg-prob", "P(r_5 < 0), %", 100 * p_neg, "0.1345")
    assert abs(neg_share - p_neg) < 4 * math.sqrt(p_neg * (1 - p_neg) / 100_000)
    q("ex1", "Monte Carlo share of negative r_5, %", 100 * neg_share, "0.127")

    # --- CIR closed form against the PDE (Example 2), Feller condition in simulation (Example 3)
    kc, thc, sc, rc = 0.50, 0.04, 0.10, 0.03
    q("ex2", "Feller ratio 2 k theta / sigma^2", 2 * kc * thc / sc**2, "4.00")
    pc = cir_price(rc, 5.0, kc, thc, sc)
    q("ex2", "CIR P(0,5) closed form", pc, "0.835234")
    pde = cir_pde_price(rc, 5.0, kc, thc, sc)
    q("ex2", "CIR P(0,5) Crank-Nicolson", pde, "0.835234")
    q("ex2", "PDE minus closed form (x1e9)", 1e9 * (pde - pc), "-5")
    # non-central chi-square parameters reproduce the conditional mean (card fi-sr-cir-distribution)
    c_par = 2 * kc / (sc**2 * (1 - math.exp(-kc * 5)))
    dof, nonc = 4 * kc * thc / sc**2, 2 * c_par * rc * math.exp(-kc * 5)
    q("fi-sr-cir-distribution", "degrees of freedom 4 k theta / sigma^2", dof, "8")
    assert abs((dof + nonc) / (2 * c_par) - (thc + (rc - thc) * math.exp(-kc * 5))) < 1e-15
    rng = np.random.default_rng(11)
    draws = rng.noncentral_chisquare(dof, nonc, 400_000) / (2 * c_par)
    q("fi-sr-cir-distribution", "sampled mean of r_5, % (seed 11)", 100 * float(draws.mean()), "3.92")
    q("fi-sr-cir-distribution", "exact mean of r_5, %", 100 * (thc + (rc - thc) * math.exp(-kc * 5)), "3.92")

    kf, thf, sf = 0.20, 0.05, 0.15
    q("fi-short-rate-cir-feller", "2 k theta", 2 * kf * thf, "0.020")
    q("fi-short-rate-cir-feller", "sigma^2", sf**2, "0.0225")
    pf = cir_price(rc, 5.0, kf, thf, sf)
    q("ex3", "Feller-violating CIR P(0,5) closed form", pf, "0.836017")
    pf_pde = cir_pde_price(rc, 5.0, kf, thf, sf)
    q("ex3", "same by Crank-Nicolson", pf_pde, "0.836017")
    q("ex3", "PDE minus closed form (x1e7)", 1e7 * (pf_pde - pf), "8")
    mc_f, se_f, neg_f = cir_euler_stats(rc, 5.0, kf, thf, sf, 100_000, 250, seed=3)
    q("ex3", "full-truncation Euler P(0,5), seed 3", mc_f, "0.8360")
    q("ex3", "its standard error (x1e4)", 1e4 * se_f, "3.1")
    q("ex3", "share of Euler steps that went negative, %", 100 * neg_f, "0.34")
    assert abs(mc_f - pf) < 4 * se_f + 5e-4  # Euler discretisation bias at 50 steps a year is below 5e-4 here

    # --- Hull-White: theta(t) refits the curve (Example 4); options (Examples 5 and 6)
    a, sig = 0.03, 0.012
    q("ex4", "market 5y zero (Nelson-Siegel), %", 100 * ns_zero(5.0), "4.4179")
    q("ex4", "market P(0,5)", ns_df(5.0), "0.801800")
    # theta(0) = f'(0) + a f(0) from the analytic Nelson-Siegel forward (the convexity term vanishes at t = 0)
    f0, f0_slope = ns_forward_and_slope(0.0)
    q("ex4", "f(0,0)", f0, "0.035")
    q("ex4", "df(0,t)/dt at t = 0", f0_slope, "0.01")
    q("ex4", "theta(0)", f0_slope + a * f0, "0.01105")
    # the finite-difference theta(t) used by the simulation (first midpoint t = 0.005) matches the analytic one
    for t_chk in (0.005, 0.5, 2.0, 4.995):
        f_c, fs_c = ns_forward_and_slope(t_chk)
        exact = fs_c + a * f_c + sig**2 / (2 * a) * (1 - math.exp(-2 * a * t_chk))
        assert abs(hw_theta(ns_df, t_chk, a, sig) - exact) < 1e-7, (t_chk, hw_theta(ns_df, t_chk, a, sig), exact)
    r5, int5 = hw_simulate(ns_df, a, sig, 5.0, 200_000, 500, seed=21)
    disc5 = np.exp(-int5)
    q("ex4", "Monte Carlo E[exp(-int r)] to 5y with fitted theta, seed 21", float(disc5.mean()), "0.80180")
    se5 = antithetic_se(disc5)
    # control: the same simulation and seed without the sigma^2/(2a)(1 - e^{-2at}) term in theta misses the curve
    _, int5_wrong = hw_simulate(ns_df, a, sig, 5.0, 200_000, 500, seed=21, convexity=False)
    q("fi-sr-hw-fit-check", "same paths, theta without the convexity term", float(np.exp(-int5_wrong).mean()), "0.80395")
    q("ex4", "effect of the convexity term, bp of price", 1e4 * float(np.exp(-int5_wrong).mean() - disc5.mean()), "22")
    assert abs(float(disc5.mean()) - ns_df(5.0)) < 4 * se5 + 2e-5
    # zero-bond option volatility (card fi-short-rate-hw-bond-option-vol)
    b15 = hw_b(a, 1.0, 5.0)
    v1 = (1 - math.exp(-2 * a)) / (2 * a)
    q("fi-short-rate-hw-bond-option-vol", "B(1,5)", b15, "3.769319")
    q("ex5", "variance factor (1 - e^{-2a})/(2a)", v1, "0.970591")
    q("ex5", "its square root", math.sqrt(v1), "0.985186")
    q("fi-short-rate-hw-bond-option-vol", "sigma_P", sig * math.sqrt(v1) * b15, "0.044562")
    fwd_price = ns_df(5.0) / ns_df(1.0)
    call = hw_zcb_option(ns_df, 1.0, 5.0, fwd_price, a, sig, call=True)
    q("ex5", "ATM-forward call on the 5y zero, expiry 1y", call, "0.014253")
    r1, int1 = hw_simulate(ns_df, a, sig, 1.0, 200_000, 250, seed=5)
    p15 = np.array([hw_bond(ns_df, 1.0, 5.0, float(x), a, sig) for x in r1[:2000]])  # spot check of the vectorised formula below
    b = hw_b(a, 1.0, 5.0)
    ln_a = math.log(ns_df(5.0) / ns_df(1.0)) + b * inst_forward(ns_df, 1.0) - sig**2 / (4 * a) * (1 - math.exp(-2 * a)) * b**2
    p15_all = np.exp(ln_a - b * r1)
    assert np.allclose(p15, p15_all[:2000], rtol=0, atol=1e-14)
    payoff = np.exp(-int1) * np.maximum(p15_all - fwd_price, 0.0)
    q("ex5", "Monte Carlo call, seed 5", float(payoff.mean()), "0.01426")
    assert abs(float(payoff.mean()) - call) < 4 * antithetic_se(payoff) + 2e-5

    def flat(t: float) -> float:
        return math.exp(-0.04 * t)

    swpt = jamshidian_payer(flat, 1.0, 5, 0.04, a, sig)
    q("fi-short-rate-jamshidian-trick", "1y into 5y payer at 4%, flat 4% curve (Jamshidian)", swpt, "0.021268")
    r1f, int1f = hw_simulate(flat, a, sig, 1.0, 200_000, 250, seed=9)
    bonds = []
    for ti in range(2, 7):
        bb = hw_b(a, 1.0, float(ti))
        la = math.log(flat(ti) / flat(1.0)) + bb * 0.04 - sig**2 / (4 * a) * (1 - math.exp(-2 * a)) * bb**2
        bonds.append(np.exp(la - bb * r1f))
    coupon_bond = 0.04 * sum(bonds) + bonds[-1]
    pay = np.exp(-int1f) * np.maximum(1.0 - coupon_bond, 0.0)
    q("ex6", "Monte Carlo payer swaption, seed 9", float(pay.mean()), "0.02127")
    assert abs(float(pay.mean()) - swpt) < 4 * antithetic_se(pay) + 2e-5
    annuity = sum(flat(1.0 + i) for i in range(1, 6))
    q("ex6", "price in bp of notional", 1e4 * swpt, "212.68")
    q("ex6", "annuity A(0) of the underlying swap", annuity, "4.267539")
    fwd_swap = (flat(1.0) - flat(6.0)) / annuity
    q("ex6", "forward swap rate, %", 100 * fwd_swap, "4.0811")

    # one-factor correlation: instantaneous vols of 2y and 10y zero-bond returns (card fi-short-rate-one-factor-correlation)
    q("fi-short-rate-one-factor-correlation", "instantaneous vol of a 2y zero, %", 100 * sig * hw_b(a, 0, 2), "2.3294")
    q("fi-short-rate-one-factor-correlation", "instantaneous vol of a 10y zero, %", 100 * sig * hw_b(a, 0, 10), "10.3673")

    print("All note 04 checks passed.")


if __name__ == "__main__":
    main()
