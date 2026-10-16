"""Feynman-Kac: pricing PDEs, their boundary conditions, and Monte Carlo checks of the expectation side.

Backs every number in 04-Stochastic-Calculus/06-Feynman-Kac-and-Pricing-PDEs.md:

1. Black-Scholes call: PDE residual and the boundary behaviour at S -> 0 and S -> infinity.
2. Affine bond prices: Vasicek and CIR Riccati ODEs (RK4) against closed forms and Monte Carlo of E[exp(-int r)].
3. Down-and-out call by the method of images: zero on the barrier, solves the PDE, matches a bridge-corrected simulation.
4. Perpetual American put: the time-independent ODE, smooth pasting, and a long-dated binomial check.
5. Perpetual one-touch: (S/H)^p from the ODE, checked by simulating the discounted hitting time.
6. Range accrual: Feynman-Kac with a running payoff, quadrature against simulation.

Run from the repo root: uv run --no-project --with numpy python 04-Stochastic-Calculus/code/feynman_kac_pdes.py
"""

from __future__ import annotations

import math

import numpy as np

SQRT2 = math.sqrt(2.0)
_ERFC = np.frompyfunc(math.erfc, 1, 1)


def ncdf(x: float | np.ndarray) -> float | np.ndarray:
    """Standard normal CDF via erfc; works on floats and arrays."""
    out = 0.5 * np.asarray(_ERFC(-np.asarray(x, dtype=float) / SQRT2), dtype=float)
    return float(out) if out.ndim == 0 else out


def bs_call(S: float | np.ndarray, K: float, tau: float, r: float, sigma: float, q: float = 0.0) -> float | np.ndarray:
    S = np.asarray(S, dtype=float)
    sd = sigma * math.sqrt(tau)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma * sigma) * tau) / sd
    out = S * math.exp(-q * tau) * ncdf(d1) - K * math.exp(-r * tau) * ncdf(d1 - sd)
    return float(out) if np.ndim(out) == 0 else out


def check(name: str, value: float, expected: float, tol: float) -> float:
    print(f"{name:62s} {value:.6g}")
    assert abs(value - expected) <= tol, f"{name}: {value} vs {expected} (tol {tol})"
    return value


def check_mc(name: str, value: float, se: float, quoted: float, truth: float, digits_tol: float) -> None:
    """Seed-stable simulation number: equal to the quoted value and within 4 standard errors of the truth."""
    print(f"{name:62s} {value:.6g}  (se {se:.2g})")
    assert abs(value - quoted) <= digits_tol, f"{name}: {value} vs quoted {quoted}"
    assert abs(value - truth) <= 4 * se, f"{name}: {value} vs truth {truth}, se {se}"


# ----------------------------------------------------------------------------------------------
# 1. Black-Scholes PDE and boundary behaviour
# ----------------------------------------------------------------------------------------------


def black_scholes_pde() -> None:
    """Backs 'Worked examples > The call satisfies the PDE and its boundaries'; card sc-fk-call-put-boundaries."""
    print("\n1. Black-Scholes call: S0=100, K=105, T=0.5, r=5%, sigma=25%")
    K, T, r, sig = 105.0, 0.5, 0.05, 0.25
    check("call price at t=0", bs_call(100.0, K, T, r, sig), 5.9885, 5e-5)
    # Residual V_t + 0.5 sig^2 S^2 V_SS + r S V_S - r V at (t, S) = (0.1, 100) by central differences
    t, S, h, dt = 0.1, 100.0, 1e-2, 1e-5

    def v(t_: float, s_: float) -> float:
        return bs_call(s_, K, T - t_, r, sig)

    Vt = (v(t + dt, S) - v(t - dt, S)) / (2 * dt)
    VS = (v(t, S + h) - v(t, S - h)) / (2 * h)
    VSS = (v(t, S + h) - 2 * v(t, S) + v(t, S - h)) / h**2
    res = Vt + 0.5 * sig**2 * S**2 * VSS + r * S * VS - r * v(t, S)
    check("PDE residual (finite differences, should be ~0)", res, 0.0, 1e-5)
    # Boundary behaviour: V(t, 0) = 0, V ~ S - K e^{-r tau} for large S
    check("V(0, S=1) (S -> 0 boundary)", bs_call(1.0, K, T, r, sig), 0.0, 1e-12)
    check("V(0, 250) - (250 - K e^{-rT})", bs_call(250.0, K, T, r, sig) - (250.0 - K * math.exp(-r * T)), 1.2e-6, 5e-8)


# ----------------------------------------------------------------------------------------------
# 2. Affine bond prices
# ----------------------------------------------------------------------------------------------


def rk4(f, y0: np.ndarray, tau: float, n: int) -> np.ndarray:
    y, h = np.array(y0, dtype=float), tau / n
    for _ in range(n):
        k1 = f(y)
        k2 = f(y + 0.5 * h * k1)
        k3 = f(y + 0.5 * h * k2)
        k4 = f(y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y


def affine_bonds(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Bond prices: PDE, ODE and expectation agree'; cards sc-fk-vasicek-riccati, sc-fk-cir-riccati."""
    print("\n2. Affine bond prices P(0, 5) = exp(A - B r0)")
    tau = 5.0
    # Vasicek: dr = kappa (theta - r) dt + sigma dW
    k, th, s, r0 = 0.3, 0.05, 0.01, 0.03
    B = (1 - math.exp(-k * tau)) / k
    lnA = (th - s * s / (2 * k * k)) * (B - tau) - s * s * B * B / (4 * k)
    closed = math.exp(lnA - B * r0)
    check("Vasicek B(5)", B, 2.589566, 5e-7)
    check("Vasicek P(0,5) closed form", closed, 0.820839, 5e-7)
    # Riccati system in tau: B' = 1 - kappa B, (ln A)' = -kappa theta B + sigma^2 B^2 / 2
    y = rk4(lambda y: np.array([1 - k * y[0], -k * th * y[0] + 0.5 * s * s * y[0] ** 2]), np.zeros(2), tau, 500)
    check("Vasicek P(0,5) from RK4 Riccati", math.exp(y[1] - y[0] * r0), closed, 1e-10)
    # Monte Carlo of E[exp(-int r)] with the exact Gaussian integral of the short rate
    e1, e2 = math.exp(-k * tau), math.exp(-2 * k * tau)
    m_i = th * tau + (r0 - th) * (1 - e1) / k
    v_i = s * s / (k * k) * (tau - 2 * (1 - e1) / k + (1 - e2) / (2 * k))
    disc = np.exp(-(m_i + math.sqrt(v_i) * rng.standard_normal(1_000_000)))
    check_mc("Vasicek P(0,5) Monte Carlo", float(disc.mean()), float(disc.std() / 1e3), 0.82082, closed, 5e-6)

    # CIR: dr = kappa (theta - r) dt + sigma sqrt(r) dW
    k, th, s, r0 = 1.5, 0.04, 0.2, 0.02
    g = math.sqrt(k * k + 2 * s * s)
    den = (g + k) * (math.exp(g * tau) - 1) + 2 * g
    B = 2 * (math.exp(g * tau) - 1) / den
    A = (2 * g * math.exp((k + g) * tau / 2) / den) ** (2 * k * th / (s * s))
    closed = A * math.exp(-B * r0)
    check("CIR gamma = sqrt(kappa^2 + 2 sigma^2)", g, 1.526434, 5e-7)
    check("CIR B(5)", B, 0.660521, 5e-7)
    check("CIR P(0,5) closed form", closed, 0.830783, 5e-7)
    # Riccati: B' = 1 - kappa B - sigma^2 B^2 / 2, (ln A)' = -kappa theta B
    y = rk4(lambda y: np.array([1 - k * y[0] - 0.5 * s * s * y[0] ** 2, -k * th * y[0]]), np.zeros(2), tau, 500)
    check("CIR P(0,5) from RK4 Riccati", math.exp(y[1] - y[0] * r0), closed, 1e-10)
    # Monte Carlo: full-truncation Euler, 1000 steps, trapezoid integral of r
    n, steps = 200_000, 1000
    dt = tau / steps
    r = np.full(n, r0)
    integral = np.zeros(n)
    for _ in range(steps):
        rp = np.maximum(r, 0.0)
        r_new = r + k * (th - rp) * dt + s * np.sqrt(rp * dt) * rng.standard_normal(n)
        integral += 0.5 * (rp + np.maximum(r_new, 0.0)) * dt
        r = r_new
    disc = np.exp(-integral)
    check_mc("CIR P(0,5) Monte Carlo (Euler, 1000 steps)", float(disc.mean()), float(disc.std() / math.sqrt(n)), 0.83072, closed, 5e-6)


# ----------------------------------------------------------------------------------------------
# 3. Down-and-out call by the method of images
# ----------------------------------------------------------------------------------------------


def down_and_out(S: float | np.ndarray, K: float, H: float, tau: float, r: float, sig: float) -> float | np.ndarray:
    """Down-and-out call, H <= K, no dividends, continuous monitoring: C(S) - (S/H)^(1 - 2r/sig^2) C(H^2/S)."""
    S = np.asarray(S, dtype=float)
    a = 1 - 2 * r / sig**2
    out = np.asarray(bs_call(S, K, tau, r, sig)) - (S / H) ** a * np.asarray(bs_call(H * H / S, K, tau, r, sig))
    return float(out) if out.ndim == 0 else out


def barrier_boundary(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > A knock-out boundary by images'; card sc-fk-barrier-image."""
    print("\n3. Down-and-out call: S0=100, K=100, H=90, T=1, r=5%, sigma=25%")
    K, H, T, r, sig = 100.0, 90.0, 1.0, 0.05, 0.25
    vanilla = bs_call(100.0, K, T, r, sig)
    dao = down_and_out(100.0, K, H, T, r, sig)
    check("vanilla call", vanilla, 12.3360, 5e-5)
    check("down-and-out call (images)", dao, 9.1112, 5e-5)
    check("image exponent 1 - 2r/sigma^2", 1 - 2 * r / sig**2, -0.6, 1e-12)
    check("fraction of the vanilla removed by the knock-out", 1 - dao / vanilla, 0.26, 5e-3)
    check("value on the barrier S = H", down_and_out(H, K, H, T, r, sig), 0.0, 1e-12)
    # The image term solves the PDE too: residual at (tau, S) = (0.6, 100)
    tau, S, h, dt = 0.6, 100.0, 1e-2, 1e-5

    def v(t_: float, s_: float) -> float:
        return down_and_out(s_, K, H, tau - t_, r, sig)

    Vt = (v(dt, S) - v(-dt, S)) / (2 * dt)
    VS = (v(0, S + h) - v(0, S - h)) / (2 * h)
    VSS = (v(0, S + h) - 2 * v(0, S) + v(0, S - h)) / h**2
    res = Vt + 0.5 * sig**2 * S**2 * VSS + r * S * VS - r * v(0, S)
    check("PDE residual of the down-and-out price", res, 0.0, 1e-5)
    # Monte Carlo with continuous monitoring through the Brownian-bridge crossing probability
    n, steps = 200_000, 250
    dt = T / steps
    x = np.full(n, math.log(100.0))
    alive = np.ones(n, dtype=bool)
    lh = math.log(H)
    for _ in range(steps):
        x_new = x + (r - 0.5 * sig**2) * dt + sig * math.sqrt(dt) * rng.standard_normal(n)
        p_cross = np.exp(-2 * np.maximum(x - lh, 0) * np.maximum(x_new - lh, 0) / (sig**2 * dt))
        alive &= (x_new > lh) & (rng.random(n) > p_cross)
        x = x_new
    pay = math.exp(-r * T) * np.where(alive, np.maximum(np.exp(x) - K, 0.0), 0.0)
    check_mc("down-and-out Monte Carlo (bridge-corrected)", float(pay.mean()), float(pay.std() / math.sqrt(n)), 9.112, dao, 5e-4)


# ----------------------------------------------------------------------------------------------
# 4. Perpetual American put
# ----------------------------------------------------------------------------------------------


def perpetual_put() -> None:
    """Backs 'Worked examples > Perpetual American put'; cards sc-fk-perpetual-put, sc-fk-american-free-boundary."""
    print("\n4. Perpetual American put: K=100, r=5%, sigma=25%")
    K, r, sig = 100.0, 0.05, 0.25
    p = -2 * r / sig**2
    s_star = p * K / (p - 1)
    check("negative root p = -2r/sigma^2", p, -1.6, 1e-12)
    check("exercise boundary S* = K p/(p - 1)", s_star, 61.538, 5e-4)
    check("intrinsic value at the boundary K - S*", K - s_star, 38.46, 5e-3)

    def value(spot: float) -> float:
        if spot <= s_star:
            return K - spot
        return (K - s_star) * (spot / s_star) ** p

    check("perpetual put at S=100", value(100.0), 17.687, 5e-4)
    h = 1e-4
    slope = (value(s_star + h) - value(s_star)) / h
    check("smooth pasting: V'(S*+) = -1", slope, -1.0, 1e-4)
    S, h = 100.0, 1e-3
    gamma = (value(S + h) - 2 * value(S) + value(S - h)) / h**2
    delta = (value(S + h) - value(S - h)) / (2 * h)
    res = 0.5 * sig**2 * S**2 * gamma + r * S * delta - r * value(S)
    check("ODE residual in the continuation region", res, 0.0, 1e-5)
    # Long-dated CRR American put approaches the perpetual value from below
    T, n = 100.0, 20_000
    dt = T / n
    u = math.exp(sig * math.sqrt(dt))
    d = 1 / u
    qp = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    j = np.arange(n + 1)
    Sx = 100.0 * u ** (n - 2 * j)
    V = np.maximum(K - Sx, 0.0)
    for i in range(n - 1, -1, -1):
        Sx = 100.0 * u ** (i - 2 * np.arange(i + 1))
        V = np.maximum(K - Sx, disc * (qp * V[:-1] + (1 - qp) * V[1:]))
    check("100-year American put, 20,000-step CRR tree", float(V[0]), 17.682, 5e-4)


# ----------------------------------------------------------------------------------------------
# 5. Perpetual one-touch
# ----------------------------------------------------------------------------------------------


def one_touch(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > Perpetual one-touch'; card sc-fk-perpetual-one-touch."""
    print("\n5. Perpetual one-touch paying 1 when S first hits H = 120 from S0 = 100")
    S0, H, r, q, sig = 100.0, 120.0, 0.05, 0.02, 0.25
    # Roots of 0.5 sig^2 p (p - 1) + (r - q) p - r = 0
    a, b, c = 0.5 * sig**2, r - q - 0.5 * sig**2, -r
    p_plus = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    check("positive root p+ (q = 2%)", p_plus, 1.2851, 5e-5)
    closed = (S0 / H) ** p_plus
    check("one-touch value (S0/H)^p+", closed, 0.7911, 5e-5)
    check("one-touch value with q = 0: S0/H", S0 / H, 0.8333, 5e-5)
    # Simulate the discounted hitting time with a bridge crossing check; horizon 40y (e^{-2} tail bounded below)
    n, dt, horizon = 100_000, 1 / 100, 40.0
    steps = int(horizon / dt)
    x = np.zeros(n)
    lh = math.log(H / S0)
    hit_time = np.full(n, np.inf)
    alive = np.ones(n, dtype=bool)
    mu = r - q - 0.5 * sig**2
    for i in range(steps):
        idx = np.flatnonzero(alive)
        if idx.size == 0:
            break
        xn = x[idx] + mu * dt + sig * math.sqrt(dt) * rng.standard_normal(idx.size)
        p_cross = np.exp(-2 * np.maximum(lh - x[idx], 0) * np.maximum(lh - xn, 0) / (sig**2 * dt))
        crossed = (xn >= lh) | (rng.random(idx.size) < p_cross)
        hit_time[idx[crossed]] = (i + 0.5) * dt
        alive[idx[crossed]] = False
        x[idx] = xn
    pay = np.exp(-r * hit_time)
    tail_bound = math.exp(-r * horizon)
    check("bound on the truncated tail e^{-r 40}", tail_bound, 0.1353, 5e-5)
    # Paths not hit by 40y contribute at most e^{-2} each; add the exact conditional value at the horizon
    left = ~np.isfinite(hit_time)
    pay[left] = math.exp(-r * horizon) * (np.exp(x[left]) / (H / S0)) ** p_plus
    check_mc("one-touch Monte Carlo E[exp(-r tau)]", float(pay.mean()), float(pay.std() / math.sqrt(n)), 0.7907, closed, 5e-4)


# ----------------------------------------------------------------------------------------------
# 6. Range accrual: running payoff
# ----------------------------------------------------------------------------------------------


def range_accrual(rng: np.random.Generator) -> None:
    """Backs 'Worked examples > A running payoff: range accrual'; card sc-fk-running-payoff."""
    print("\n6. Range accrual: pays 1/252 per day with 90 < S < 110, S0=100, T=1, r=5%, sigma=20%")
    S0, L, U, r, sig, days = 100.0, 90.0, 110.0, 0.05, 0.20, 252
    t = np.arange(1, days + 1) / days
    sd = sig * np.sqrt(t)
    m = math.log(S0) + (r - 0.5 * sig**2) * t
    prob = np.asarray(ncdf((math.log(U) - m) / sd)) - np.asarray(ncdf((math.log(L) - m) / sd))
    value = float(np.sum(np.exp(-r * t) * prob) / days)
    check("value by quadrature of e^{-rt} Q(L < S_t < U)", value, 0.5648, 5e-5)
    check("expected fraction of days in range (undiscounted)", float(prob.mean()), 0.5767, 5e-5)
    n = 100_000
    z = rng.standard_normal((n, days))
    logS = math.log(S0) + np.cumsum((r - 0.5 * sig**2) / days + sig / math.sqrt(days) * z, axis=1)
    inside = (logS > math.log(L)) & (logS < math.log(U))
    pay = (inside * np.exp(-r * t)).sum(axis=1) / days
    check_mc("Monte Carlo with daily fixings", float(pay.mean()), float(pay.std() / math.sqrt(n)), 0.5637, value, 5e-4)


def main() -> None:
    rng = np.random.default_rng(6)
    black_scholes_pde()
    affine_bonds(rng)
    barrier_boundary(rng)
    perpetual_put()
    one_touch(rng)
    range_accrual(rng)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
