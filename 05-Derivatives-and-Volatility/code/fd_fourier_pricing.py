"""Finite-difference and Fourier pricing, checked against closed forms.

Backs the note 05-Derivatives-and-Volatility/11-Finite-Differences-and-Fourier-Pricing.md.
Every number the note quotes is printed here and asserted, so drift fails CI.

Sections
1. Theta-scheme (explicit, implicit, Crank-Nicolson) for Black-Scholes in log-spot, Thomas solver.
2. Explicit-scheme stability limit and blow-up.
3. Convergence of implicit and Crank-Nicolson against Black-Scholes.
4. Crank-Nicolson gamma oscillations on a digital and Rannacher smoothing.
5. American put by PSOR and by the penalty method, against a CRR binomial tree; exercise boundary.
6. Carr-Madan FFT (Simpson weights) against Black-Scholes and Heston; sensitivity to alpha and eta.
7. COS method (Fang-Oosterlee 2008) against Black-Scholes and Heston; convergence in N.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/fd_fourier_pricing.py
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np
from pricing_core import bs_price, heston_call, heston_cf, norm_cdf, norm_pdf

CharFn = Callable[[np.ndarray], np.ndarray]

# Base case used throughout the note.
S0, K, T, R, Q, SIG = 100.0, 100.0, 1.0, 0.05, 0.0, 0.20
# Heston parameters used for the Fourier checks.
HESTON = {"kappa": 2.0, "theta": 0.04, "xi": 0.5, "rho": -0.7, "v0": 0.04}


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a labelled value and assert it is within tol of the quoted number."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    return value


# ---------------------------------------------------------------------------
# 1. Theta-scheme in log-spot
# ---------------------------------------------------------------------------


def thomas(lower: np.ndarray, diag: np.ndarray, upper: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """Solve a tridiagonal system; lower[0] and upper[-1] are ignored. O(n), no pivoting (diagonally dominant here)."""
    n = len(diag)
    c = np.empty(n)
    d = np.empty(n)
    c[0] = upper[0] / diag[0]
    d[0] = rhs[0] / diag[0]
    for i in range(1, n):
        m = diag[i] - lower[i] * c[i - 1]
        c[i] = upper[i] / m if i < n - 1 else 0.0
        d[i] = (rhs[i] - lower[i] * d[i - 1]) / m
    x = np.empty(n)
    x[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def log_grid(n_space: int, half_width: float = 5.0 * SIG * math.sqrt(T)) -> tuple[np.ndarray, float]:
    """Uniform grid in x = ln S, centred on ln S0 so that S0 (and K = S0) is a node."""
    x = math.log(S0) + np.linspace(-half_width, half_width, n_space + 1)
    return x, x[1] - x[0]


def operator_coeffs(dx: float, sigma: float = SIG, r: float = R, q: float = Q) -> tuple[float, float, float]:
    """Coefficients (a, b, c) of L V_i = a V_{i-1} + b V_i + c V_{i+1} for
    L = 0.5 sigma^2 d2/dx2 + (r - q - 0.5 sigma^2) d/dx - r, central differences."""
    nu = r - q - 0.5 * sigma**2
    a = 0.5 * sigma**2 / dx**2 - 0.5 * nu / dx
    c = 0.5 * sigma**2 / dx**2 + 0.5 * nu / dx
    b = -(sigma**2) / dx**2 - r
    return a, b, c


def theta_scheme(
    payoff: np.ndarray,
    x: np.ndarray,
    n_time: int,
    theta: float,
    lower_bc: Callable[[float], float],
    upper_bc: Callable[[float], float],
    rannacher_steps: int = 0,
    exercise: np.ndarray | None = None,
    american: str = "",
    horizon: float = T,
) -> np.ndarray:
    """March V_tau = L V from tau = 0 (payoff) to tau = T.

    theta = 0 explicit, 1 implicit, 0.5 Crank-Nicolson. ``rannacher_steps`` replaces that many initial
    CN steps by two implicit half-steps each. ``american`` = "psor" or "penalty" enforces V >= exercise.
    Dirichlet boundaries come from lower_bc(tau) and upper_bc(tau).
    """
    dx = x[1] - x[0]
    a, b, c = operator_coeffs(dx)
    v = payoff.copy()
    m = len(x) - 2  # interior nodes
    dt_full = horizon / n_time
    schedule: list[tuple[float, float]] = []
    for step in range(n_time):
        if step < rannacher_steps:
            schedule += [(1.0, 0.5 * dt_full)] * 2
        else:
            schedule.append((theta, dt_full))
    tau = 0.0
    for th, dt in schedule:
        tau_new = tau + dt
        lv = np.zeros(m)
        lv[:] = a * v[:-2] + b * v[1:-1] + c * v[2:]
        rhs = v[1:-1] + (1.0 - th) * dt * lv
        lo_new, hi_new = lower_bc(tau_new), upper_bc(tau_new)
        rhs[0] += th * dt * a * lo_new
        rhs[-1] += th * dt * c * hi_new
        sub = np.full(m, -th * dt * a)
        dia = np.full(m, 1.0 - th * dt * b)
        sup = np.full(m, -th * dt * c)
        if th == 0.0:
            interior = rhs
        elif american == "psor":
            interior = psor(sub, dia, sup, rhs, exercise[1:-1], v[1:-1])
        elif american == "penalty":
            interior = penalty_solve(sub, dia, sup, rhs, exercise[1:-1])
        else:
            interior = thomas(sub, dia, sup, rhs)
        if american and th == 0.0:
            interior = np.maximum(interior, exercise[1:-1])
        v = np.concatenate(([lo_new], interior, [hi_new]))
        tau = tau_new
    return v


def psor(sub: np.ndarray, dia: np.ndarray, sup: np.ndarray, rhs: np.ndarray, g: np.ndarray, start: np.ndarray) -> np.ndarray:
    """Projected SOR for the linear complementarity problem A v >= rhs, v >= g, (A v - rhs)(v - g) = 0."""
    v = np.maximum(start.copy(), g)
    omega, n = 1.5, len(dia)
    for _ in range(10_000):
        err = 0.0
        for i in range(n):
            left = sub[i] * v[i - 1] if i > 0 else 0.0
            right = sup[i] * v[i + 1] if i < n - 1 else 0.0
            gs = (rhs[i] - left - right) / dia[i]
            new = max(g[i], v[i] + omega * (gs - v[i]))
            err += (new - v[i]) ** 2
            v[i] = new
        if err < 1e-16:
            return v
    raise RuntimeError("PSOR did not converge")


def penalty_solve(sub: np.ndarray, dia: np.ndarray, sup: np.ndarray, rhs: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Penalty method (Forsyth-Vetzal 2002): solve (A + P) v = rhs + P g with P = rho on nodes where v < g, iterate."""
    rho = 1e8
    active = np.zeros(len(dia), dtype=bool)
    v_prev = np.full(len(dia), np.inf)
    for _ in range(100):
        p = np.where(active, rho, 0.0)
        v = thomas(sub, dia + p, sup, rhs + p * g)
        new_active = v < g
        if (
            np.array_equal(new_active, active) or np.max(np.abs(v - v_prev)) < 1e-7
        ):  # Forsyth-Vetzal stopping rule; a node at v = g can flip forever
            return v
        active, v_prev = new_active, v
    raise RuntimeError("penalty iteration did not converge")


def fd_call(
    n_space: int, n_time: int, theta: float, rannacher: int = 0, half_width: float = 5.0 * SIG * math.sqrt(T), upper: str = "dirichlet"
) -> tuple[float, np.ndarray, np.ndarray]:
    """European call on the log grid; returns (price at S0, grid, values).

    upper = "dirichlet" uses V = S e^{-q tau} - K e^{-r tau} at the top node; "zero" uses the wrong V = 0
    to show how a bad boundary contaminates the price at S0.
    """
    x, _ = log_grid(n_space, half_width)
    s = np.exp(x)
    s_hi = s[-1]
    v = theta_scheme(
        np.maximum(s - K, 0.0),
        x,
        n_time,
        theta,
        lambda tau: 0.0,
        (lambda tau: s_hi * math.exp(-Q * tau) - K * math.exp(-R * tau)) if upper == "dirichlet" else (lambda tau: 0.0),
        rannacher,
    )
    return float(v[n_space // 2]), s, v


def fd_digital(n_space: int, n_time: int, theta: float, rannacher: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Cash-or-nothing call paying 1 if S_T > K; payoff 1/2 at the strike node."""
    x, _ = log_grid(n_space)
    s = np.exp(x)
    payoff = np.where(s > K, 1.0, 0.0)
    payoff[np.isclose(s, K)] = 0.5
    v = theta_scheme(payoff, x, n_time, theta, lambda tau: 0.0, lambda tau: math.exp(-R * tau), rannacher)
    return s, v


def grid_gamma(s: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Gamma on a non-uniform spot grid (log grid mapped to spot), three-point formula at interior nodes."""
    h1 = s[1:-1] - s[:-2]
    h2 = s[2:] - s[1:-1]
    return 2.0 * (v[2:] * h1 - v[1:-1] * (h1 + h2) + v[:-2] * h2) / (h1 * h2 * (h1 + h2))


def digital_gamma_exact(s: np.ndarray) -> np.ndarray:
    sd = SIG * math.sqrt(T)
    d2 = (np.log(s / K) + (R - Q - 0.5 * SIG**2) * T) / sd
    d1 = d2 + sd
    return -math.exp(-R * T) * norm_pdf(d2) * d1 / (s**2 * SIG**2 * T)


def american_put_fd(n_space: int, n_time: int, method: str) -> tuple[float, np.ndarray, np.ndarray]:
    x, _ = log_grid(n_space)
    s = np.exp(x)
    g = np.maximum(K - s, 0.0)
    v = theta_scheme(g, x, n_time, 1.0, lambda tau: K - s[0], lambda tau: 0.0, rannacher_steps=0, exercise=g, american=method)
    return float(v[n_space // 2]), s, v


def crr_american_put(n_steps: int, s0: float = S0) -> float:
    """Cox-Ross-Rubinstein tree, vectorised backward induction with early exercise."""
    dt = T / n_steps
    u = math.exp(SIG * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp((R - Q) * dt) - d) / (u - d)
    disc = math.exp(-R * dt)
    j = np.arange(n_steps + 1)
    v = np.maximum(K - s0 * u ** (n_steps - 2 * j), 0.0)
    for n in range(n_steps - 1, -1, -1):
        j = np.arange(n + 1)
        v = np.maximum(disc * (p * v[:-1] + (1 - p) * v[1:]), K - s0 * u ** (n - 2 * j))
    return float(v[0])


def american_put_cn(n_space: int, n_time: int, horizon: float = T, method: str = "penalty") -> tuple[float, np.ndarray, np.ndarray]:
    """American put by Crank-Nicolson with two Rannacher start-up steps and the early-exercise constraint."""
    x, _ = log_grid(n_space)
    s = np.exp(x)
    g = np.maximum(K - s, 0.0)
    v = theta_scheme(g, x, n_time, 0.5, lambda tau: K - s[0], lambda tau: 0.0, 2, g, method, horizon)
    return float(v[n_space // 2]), s, v


def exercise_boundary(n_space: int, steps_per_year: int, taus: tuple[float, ...]) -> dict[float, float]:
    """Critical spot S*(tau): the largest grid node below K where the American put equals intrinsic."""
    out = {}
    for tau in taus:
        _, s, v = american_put_cn(n_space, max(2, round(steps_per_year * tau)), horizon=tau)
        g = np.maximum(K - s, 0.0)
        exercised = np.flatnonzero((np.abs(v - g) < 1e-6) & (s < K))
        out[tau] = float(s[exercised.max()])
    return out


# ---------------------------------------------------------------------------
# 6. Carr-Madan FFT
# ---------------------------------------------------------------------------


def carr_madan(
    cf_logret: CharFn, s0: float, strikes: np.ndarray, r: float, t: float, alpha: float = 1.5, n: int = 4096, eta: float = 0.25
) -> np.ndarray:
    """Carr-Madan (1999) FFT with Simpson weights.

    Works in units of S0: cf_logret is the characteristic function of ln(S_T / S0), k = ln(K / S0).
    The damped call exp(alpha k) C(k) has transform
    psi(v) = exp(-r t) phi(v - (alpha + 1) i) / (alpha^2 + alpha - v^2 + i (2 alpha + 1) v).
    Log-strike spacing lambda = 2 pi / (n eta); the grid is centred on k = 0 (so K = S0 is a node) and
    prices off the grid are linearly interpolated in log strike.
    """
    j = np.arange(n)
    v = eta * j
    lam = 2.0 * math.pi / (n * eta)
    b = 0.5 * n * lam
    k_grid = -b + lam * j
    psi = math.exp(-r * t) * cf_logret(v - (alpha + 1.0) * 1j) / (alpha**2 + alpha - v**2 + 1j * (2.0 * alpha + 1.0) * v)
    simpson = (3.0 + (-1.0) ** (j + 1)) / 3.0
    simpson[0] = 1.0 / 3.0
    x = np.exp(1j * b * v) * psi * eta * simpson
    calls = np.exp(-alpha * k_grid) / math.pi * np.real(np.fft.fft(x))
    return s0 * np.interp(np.log(strikes / s0), k_grid, calls)


def bs_cf_logret(r: float, q: float, sigma: float, t: float) -> CharFn:
    """Characteristic function of ln(S_T / S0) under Black-Scholes."""
    return lambda u: np.exp(1j * u * (r - q - 0.5 * sigma**2) * t - 0.5 * sigma**2 * t * u * u)


def heston_cf_logret(r: float, q: float, t: float) -> CharFn:
    return lambda u: heston_cf(u, t, r, q, **HESTON)


# ---------------------------------------------------------------------------
# 7. COS method
# ---------------------------------------------------------------------------


def cos_call(
    cf_logret: CharFn, s0: float, strikes: np.ndarray, r: float, t: float, c1: float, c2: float, n: int = 128, L: float = 10.0
) -> np.ndarray:
    """Fang-Oosterlee (2008) COS price of European calls.

    cf_logret is the characteristic function of X = ln(S_T / S_0); c1, c2 its first two cumulants.
    For each strike, y = ln(S_T / K) = ln(S0 / K) + X is expanded in cosines on [A, B] = ln(S0/K) + c1 -/+ L sqrt(c2).
    """
    out = []
    kk = np.arange(n)
    for strike in np.atleast_1d(strikes):
        x0 = math.log(s0 / strike)
        A = x0 + c1 - L * math.sqrt(c2)
        B = x0 + c1 + L * math.sqrt(c2)
        u = kk * math.pi / (B - A)
        # payoff coefficients of K (e^y - 1)^+ on [0, B]
        chi = (
            np.cos(u * (B - A)) * math.exp(B) - np.cos(u * (0.0 - A)) + u * np.sin(u * (B - A)) * math.exp(B) - u * np.sin(u * (0.0 - A))
        ) / (1.0 + u * u)
        psi = np.empty(n)
        psi[0] = B
        psi[1:] = (np.sin(u[1:] * (B - A)) - np.sin(u[1:] * (0.0 - A))) / u[1:]
        coef = 2.0 / (B - A) * strike * (chi - psi)
        phi_y = cf_logret(u) * np.exp(1j * u * x0)
        terms = np.real(phi_y * np.exp(-1j * u * A)) * coef
        terms[0] *= 0.5
        out.append(math.exp(-r * t) * terms.sum())
    return np.array(out)


def check_sci(label: str, value: float, expected: float) -> float:
    """Check a value the note quotes to two significant figures; tiny round-off values only need to stay tiny."""
    print(f"{label}: {value:.2e}")
    if abs(expected) < 1e-12:
        assert abs(value) < 1e-12, f"{label}: got {value}, expected below 1e-12"
    else:
        assert abs(value - expected) <= 0.051 * abs(expected), f"{label}: got {value}, expected {expected:.2e}"
    return value


def main() -> None:
    bs = bs_price(S0, K, T, R, SIG, Q)
    check("Black-Scholes call", bs, 10.4506, 5e-5)
    print()

    # 2. Explicit stability. Backs "Stability: von Neumann analysis", Example 1 and cards deriv-fd-explicit-stability,
    #    deriv-fd-explicit-numbers.
    n_space = 200
    _, dx = log_grid(n_space)
    dt_max = dx**2 / (SIG**2 + R * dx**2)  # all explicit weights non-negative: 1 - dt (sigma^2 / dx^2 + r) >= 0
    check("dx (200 cells over +/- 5 sd)", dx, 0.01, 1e-12)
    check("explicit dt limit dx^2 / (sigma^2 + r dx^2)", dt_max, 0.0025, 1e-6)
    check("explicit 500 steps price", fd_call(n_space, 500, 0.0)[0], 10.4504, 5e-5)
    p_bad, _, v_bad = fd_call(n_space, 380, 0.0)
    check("380 steps: percent by which dt exceeds the limit", 100 * ((T / 380) / dt_max - 1), 5.3, 0.05)
    check("explicit 380 steps (dt 5% over the limit): log10 max |V|", math.log10(np.max(np.abs(v_bad))), 14.26, 0.01)
    check_sci("explicit 380 steps price at S0", p_bad, -1.79e14)
    print()

    # 3. Convergence and boundaries. Backs "Boundary conditions and the domain", Example 2 and cards
    #    deriv-fd-theta-scheme, deriv-fd-orders, deriv-fd-boundaries.
    expected = {
        50: (-5.76e-02, -3.63e-02),
        100: (-1.96e-02, -9.01e-03),
        200: (-7.50e-03, -2.25e-03),
        400: (-3.19e-03, -5.62e-04),
        800: (-1.45e-03, -1.40e-04),
    }
    got = {n: (fd_call(n, n, 1.0)[0] - bs, fd_call(n, n, 0.5)[0] - bs) for n in expected}
    for n, (e_imp, e_cn) in expected.items():
        check_sci(f"n={n} implicit error", got[n][0], e_imp)
        check_sci(f"n={n} CN error", got[n][1], e_cn)
    check("implicit error ratio n 400 -> 800", got[400][0] / got[800][0], 2.2, 0.05)
    check("CN error ratio n 400 -> 800", got[400][1] / got[800][1], 4.0, 0.05)
    check("implicit / CN error at n = 800 (equal cost)", got[800][0] / got[800][1], 10.3, 0.05)
    expected_bc = {3.0: (-2.01e-04, -3.32e-01), 5.0: (-5.62e-04, -7.60e-04), 8.0: (-1.44e-03, -1.44e-03)}
    for hw_sd, (e_d, e_z) in expected_bc.items():
        check_sci(f"+/- {hw_sd:.0f} sd, Dirichlet top", fd_call(400, 400, 0.5, half_width=hw_sd * SIG)[0] - bs, e_d)
        check_sci(f"+/- {hw_sd:.0f} sd, V=0 top", fd_call(400, 400, 0.5, half_width=hw_sd * SIG, upper="zero")[0] - bs, e_z)
    print()

    # 4. CN oscillations on a digital, Rannacher fix. Backs "Non-smooth payoffs and Rannacher smoothing", Example 3
    #    and cards deriv-fd-cn-oscillation, deriv-fd-rannacher, deriv-fd-greeks-from-grid.
    n_space, n_time = 400, 25
    _, dx = log_grid(n_space)
    check("digital grid: sigma^2 dt / dx^2", SIG**2 * (T / n_time) / dx**2, 64.0, 1e-9)
    mu = SIG**2 * (T / n_time) / dx**2
    # amplification of the highest-frequency (sawtooth) mode for the diffusion part, xi dx = pi
    check("CN amplification (1 - mu) / (1 + mu)", (1 - mu) / (1 + mu), -0.9692, 5e-5)
    check("CN sawtooth surviving after 25 steps", abs((1 - mu) / (1 + mu)) ** n_time, 0.458, 5e-4)
    check("implicit amplification 1 / (1 + 2 mu)", 1 / (1 + 2 * mu), 0.00775, 5e-6)
    check("Rannacher: four implicit half-steps 1 / (1 + mu)^4", (1 / (1 + mu)) ** 4, 5.6e-8, 5e-10)
    s, v_cn = fd_digital(n_space, n_time, 0.5)
    _, v_ran = fd_digital(n_space, n_time, 0.5, rannacher=2)
    _, v_imp = fd_digital(n_space, n_time, 1.0)
    d2 = (math.log(S0 / K) + (R - Q - 0.5 * SIG**2) * T) / (SIG * math.sqrt(T))
    check("digital exact e^{-rT} N(d2)", math.exp(-R * T) * norm_cdf(d2), 0.5323, 5e-5)
    check("digital CN at S0", v_cn[n_space // 2], 0.5326, 5e-5)
    check("digital Rannacher at S0", v_ran[n_space // 2], 0.5323, 5e-5)
    check("digital implicit at S0", v_imp[n_space // 2], 0.5320, 5e-5)
    win = (s[1:-1] > 90) & (s[1:-1] < 110)
    g_exact = digital_gamma_exact(s[1:-1][win])
    check_sci("digital max |gamma| exact on 90-110", np.max(np.abs(g_exact)), 5.32e-4)
    err_cn = check_sci("digital max gamma error CN", np.max(np.abs(grid_gamma(s, v_cn)[win] - g_exact)), 0.414)
    err_ran = check_sci("digital max gamma error Rannacher", np.max(np.abs(grid_gamma(s, v_ran)[win] - g_exact)), 6.9e-7)
    err_imp = check_sci("digital max gamma error implicit", np.max(np.abs(grid_gamma(s, v_imp)[win] - g_exact)), 3.6e-5)
    check("CN gamma error / true max gamma", err_cn / np.max(np.abs(g_exact)), 778, 2)
    check("implicit / Rannacher gamma error", err_imp / err_ran, 52, 1)
    print()

    # 5. American put. Backs "American options as a complementarity problem", Example 4 and cards
    #    deriv-fd-american-lcp, deriv-fd-penalty-vs-psor, deriv-fd-exercise-boundary.
    euro_put = bs_price(S0, K, T, R, SIG, Q, call=False)
    check("European put", euro_put, 5.5735, 5e-5)
    tree = crr_american_put(10_000)
    check("CRR American put 10000 steps", tree, 6.0903, 5e-5)
    check("early-exercise premium", tree - euro_put, 0.5168, 5e-5)
    p_psor = american_put_cn(200, 200, method="psor")[0]
    check("PSOR CN-Rannacher 200x200", p_psor, 6.0874, 5e-5)
    check("|PSOR - penalty| 200x200 (below 1e-9)", abs(p_psor - american_put_cn(200, 200)[0]), 0.0, 1e-9)
    check("penalty CN-Rannacher 400x400", american_put_cn(400, 400)[0], 6.0895, 5e-5)
    check("penalty CN-Rannacher 800x800", american_put_cn(800, 800)[0], 6.0901, 5e-5)
    check("penalty implicit 800x800", american_put_fd(800, 800, "penalty")[0], 6.0884, 5e-5)
    bnd = exercise_boundary(800, 800, (0.1, 0.25, 0.5, 1.0))
    for tau, s_star in zip((0.1, 0.25, 0.5, 1.0), (90.26, 86.72, 83.95, 80.86), strict=True):
        check(f"exercise boundary S*(tau={tau})", bnd[tau], s_star, 5e-3)
    check("perpetual boundary 2rK / (2r + sigma^2)", 2 * R * K / (2 * R + SIG**2), 71.43, 5e-3)
    print()

    # 6. Carr-Madan. Backs "Fourier pricing", Example 5 and cards deriv-fourier-carr-madan-damping,
    #    deriv-fourier-grid-tradeoff, deriv-fourier-aliasing.
    strikes = np.array([80.0, 90.0, 100.0, 110.0, 120.0])
    bs_k = np.asarray(bs_price(S0, strikes, T, R, SIG, Q))
    check("FFT strike spacing 2 pi / (N eta), N 4096 eta 0.25", 2 * math.pi / (4096 * 0.25), 0.006136, 1e-6)
    for alpha, (e_max, e_atm) in {0.1: (1.5, 1.5), 0.5: (6.2e-2, 6.2e-2), 1.5: (7.4e-4, 2.2e-7), 5.0: (7.4e-4, 0.0)}.items():
        c = carr_madan(bs_cf_logret(R, Q, SIG, T), S0, strikes, R, T, alpha=alpha)
        check_sci(f"FFT alpha {alpha}: max error 80-120", np.max(np.abs(c - bs_k)), e_max)
        check_sci(f"FFT alpha {alpha}: error at K=100 (grid node)", abs(c[2] - bs_k[2]), e_atm)
    for eta, (e_max, e_atm) in {0.05: (8.2e-3, 0.0), 0.25: (7.4e-4, 2.2e-7), 1.0: (2.8e-1, 2.8e-1)}.items():
        c = carr_madan(bs_cf_logret(R, Q, SIG, T), S0, strikes, R, T, eta=eta)
        lam_expected = {0.05: 0.0307, 0.25: 0.0061, 1.0: 0.0015}[eta]
        check(f"FFT eta {eta}: log-strike spacing 2 pi / (N eta)", 2 * math.pi / (4096 * eta), lam_expected, 5e-5)
        check_sci(f"FFT eta {eta}: max error 80-120", np.max(np.abs(c - bs_k)), e_max)
        check_sci(f"FFT eta {eta}: error at K=100", abs(c[2] - bs_k[2]), e_atm)
    # The discrete Fourier sum is periodic in log strike; Simpson's alternating weights make the period pi / eta,
    # and the deep in-the-money image (call value close to S0) leaks back as about S0 exp(-alpha pi / eta) / 3.
    for alpha, eta in ((1.0, 0.25), (1.5, 0.25), (2.0, 0.25), (1.0, 0.125)):
        node_err = carr_madan(bs_cf_logret(R, Q, SIG, T), S0, strikes[2:3], R, T, alpha=alpha, eta=eta)[0] - bs_k[2]
        alias = -S0 * math.exp(-alpha * math.pi / eta) / 3.0
        check_sci(f"FFT ATM error alpha {alpha} eta {eta}", node_err, alias)
        print(f"  alias estimate -S0 exp(-alpha pi / eta) / 3 = {alias:.2e}")
    hes = np.asarray(heston_call(S0, strikes, T, R, Q, **HESTON))
    for k_, p_, ex in zip(strikes, hes, (25.2368, 17.1401, 10.1546, 4.8662, 1.7382), strict=True):
        check(f"Heston call K={k_:.0f} (Lewis)", p_, ex, 5e-5)
    cm_h = carr_madan(heston_cf_logret(R, Q, T), S0, strikes, R, T)
    check_sci("FFT vs Lewis Heston, max error 80-120", np.max(np.abs(cm_h - hes)), 1.0e-3)
    check_sci("FFT vs Lewis Heston, error at K=100", abs(cm_h[2] - hes[2]), 2.2e-7)
    print()

    # 7. COS. Backs "Fourier pricing", Example 6 and cards deriv-fourier-cos, deriv-fourier-validate-cf.
    c1, c2 = (R - Q - 0.5 * SIG**2) * T, SIG**2 * T
    for n, e in {8: 2.9, 16: 8.6e-2, 32: 1.8e-6, 64: 0.0}.items():
        check_sci(
            f"COS N={n} vs BS max error", np.max(np.abs(cos_call(bs_cf_logret(R, Q, SIG, T), S0, strikes, R, T, c1, c2, n=n) - bs_k)), e
        )
    for L, e in {4.0: 6.25e-4, 3.0: 2.74e-2, 2.0: 0.498}.items():
        err = np.max(np.abs(cos_call(bs_cf_logret(R, Q, SIG, T), S0, strikes, R, T, c1, c2, n=128, L=L) - bs_k))
        check_sci(f"COS L={L} N=128 vs BS max error (truncation)", err, e)
    hc1, hc2 = (R - Q - 0.5 * HESTON["theta"]) * T, HESTON["theta"] * T
    for n, e in {32: 3.5e-2, 64: 4.3e-4, 128: 9.2e-8, 256: 2.8e-10}.items():
        c = cos_call(heston_cf_logret(R, Q, T), S0, strikes, R, T, hc1, hc2, n=n, L=12.0)
        check_sci(f"COS N={n} vs Lewis Heston max error", np.max(np.abs(c - hes)), e)


if __name__ == "__main__":
    main()
