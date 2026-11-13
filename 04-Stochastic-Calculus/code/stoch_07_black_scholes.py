"""Black-Scholes derivation: prices, PDE checks, boundary conditions and the discrete-hedging table.

Backs every number in `04-Stochastic-Calculus/07-Black-Scholes-Derivation.md`.
Independent routes used here:
- the call and put by quadrature of the payoff against the risk-neutral lognormal density, by seeded
  simulation, and by a Crank-Nicolson solution of the PDE with the boundary conditions the note states
  (so the boundary conditions themselves are tested), all against the closed form;
- the PDE, the heat-equation substitution and the Greeks identity by central finite differences;
- the power solutions S^p by the roots of the quadratic and a finite-difference PDE residual;
- the at-the-money approximation against quadrature;
- the discrete-hedging error by simulating the self-financing hedge, against the rule of M. Kamal (Goldman Sachs research note, 1998)
  sqrt(pi/4) sigma vega / sqrt(N).
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 04-Stochastic-Calculus/code/stoch_07_black_scholes.py`.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261116
S0, K, T, R, SIG = 100.0, 105.0, 0.5, 0.05, 0.25


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, se: float, target: float, k: float = 4.0) -> None:
    """Assert a seeded Monte Carlo estimate is within k standard errors of an independently computed target."""
    assert abs(estimate - target) <= k * se, f"{label}: simulated {estimate!r} +/- {se:.2g}, target {target}"
    print(f"    {label} ~ {estimate:.4f} (se {se:.1e}, target {target:.4f}, tolerance {k:g} se)")


def ncdf(x):
    return 0.5 * (1.0 + np.vectorize(math.erf)(np.asarray(x) / math.sqrt(2.0))) if np.ndim(x) else 0.5 * math.erfc(-x / math.sqrt(2.0))


def npdf(x):
    return np.exp(-0.5 * np.asarray(x) ** 2) / math.sqrt(2 * math.pi)


def d12(s, k: float, tau: float, r: float, sig: float):
    d1 = (np.log(s / k) + (r + 0.5 * sig**2) * tau) / (sig * math.sqrt(tau))
    return d1, d1 - sig * math.sqrt(tau)


def call(s, k: float, tau: float, r: float, sig: float):
    d1, d2 = d12(s, k, tau, r, sig)
    return s * ncdf(d1) - k * math.exp(-r * tau) * ncdf(d2)


def put(s, k: float, tau: float, r: float, sig: float):
    d1, d2 = d12(s, k, tau, r, sig)
    return k * math.exp(-r * tau) * ncdf(-d2) - s * ncdf(-d1)


def mean_se(x: np.ndarray) -> tuple[float, float]:
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(x.size))


def thomas(lower: np.ndarray, diag: np.ndarray, upper: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    n = diag.size
    c, d = np.empty(n), np.empty(n)
    c[0], d[0] = upper[0] / diag[0], rhs[0] / diag[0]
    for i in range(1, n):
        m = diag[i] - lower[i] * c[i - 1]
        c[i] = upper[i] / m if i < n - 1 else 0.0
        d[i] = (rhs[i] - lower[i] * d[i - 1]) / m
    x = np.empty(n)
    x[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def crank_nicolson(payoff, bc_low, bc_high, n_x: int = 1200, n_t: int = 600) -> float:
    """Solve V_tau = (sigma^2/2) V_xx + (r - sigma^2/2) V_x - r V in x = ln S, with Dirichlet boundaries.

    bc_low(tau) and bc_high(tau, S_max) are the boundary values the note states; four fully implicit
    half-steps first (Rannacher) damp the payoff kink. Returns V(0, S0).
    """
    width = 8 * SIG * math.sqrt(T)
    x = np.linspace(math.log(S0) - width, math.log(S0) + width, n_x + 1)
    h, dt = x[1] - x[0], T / n_t
    a = 0.5 * SIG**2 / h**2 - (R - 0.5 * SIG**2) / (2 * h)
    c = 0.5 * SIG**2 / h**2 + (R - 0.5 * SIG**2) / (2 * h)
    b = -(SIG**2) / h**2 - R
    v = payoff(np.exp(x))
    tau = 0.0
    steps = [(0.5 * dt, 1.0)] * 4 + [(dt, 0.5)] * (n_t - 2)
    for step, theta in steps:
        tau += step
        m = n_x - 1
        lo_v, hi_v = bc_low(tau), bc_high(tau, math.exp(x[-1]))
        explicit = v[1:-1] + (1 - theta) * step * (a * v[:-2] + b * v[1:-1] + c * v[2:])
        rhs = explicit.copy()
        rhs[0] += theta * step * a * lo_v
        rhs[-1] += theta * step * c * hi_v
        lower = np.full(m, -theta * step * a)
        diag = np.full(m, 1 - theta * step * b)
        upper = np.full(m, -theta * step * c)
        v = np.concatenate([[lo_v], thomas(lower, diag, upper, rhs), [hi_v]])
    assert abs(tau - T) < 1e-12
    return float(np.interp(math.log(S0), x, v))


def prices(rng: np.random.Generator) -> None:
    print("Call and put, S0 = 100, K = 105, T = 0.5, r = 5%, sigma = 25% (worked example; cards sc-bs-call-formula, sc-bs-put-call-parity)")
    approx("sigma sqrt(T)", SIG * math.sqrt(T), 0.1768, 4)
    approx("ln(100/105)", math.log(S0 / K), -0.0488, 4)
    d1, d2 = d12(S0, K, T, R, SIG)
    approx("d1", d1, -0.0462, 4)
    approx("d2", d2, -0.2230, 4)
    approx("d1 from the rounded inputs (-0.0488 + 0.040625)/0.1768", (-0.0488 + (0.05 + 0.03125) * 0.5) / 0.1768, -0.0462, 4)
    approx("N(d1)", ncdf(d1), 0.4816, 4)
    approx("N(d2)", ncdf(d2), 0.4118, 4)
    c = call(S0, K, T, R, SIG)
    approx("call, closed form", c, 5.9885, 4)
    approx("call from the rounded working 48.16 - 105 e^{-0.025} 0.4118", 48.16 - 105 * math.exp(-0.025) * 0.4118, 5.99, 2)
    p = put(S0, K, T, R, SIG)
    approx("put, closed form", p, 8.40, 2)
    approx("put by parity from the rounded call 5.99 - 100 + 105 e^{-0.025}", 5.99 - 100 + 105 * math.exp(-0.025), 8.40, 2)
    z = np.linspace(-12, 12, 2_400_001)
    st = S0 * np.exp((R - 0.5 * SIG**2) * T + SIG * math.sqrt(T) * z)
    w = npdf(z) * np.gradient(z)
    approx("call by quadrature of e^{-rT} E^Q[(S_T - K)^+]", math.exp(-R * T) * float(np.sum(np.maximum(st - K, 0) * w)), c, 5)
    approx("put by quadrature", math.exp(-R * T) * float(np.sum(np.maximum(K - st, 0) * w)), p, 5)
    zz = rng.standard_normal(4_000_000)
    sq = S0 * np.exp((R - 0.5 * SIG**2) * T + SIG * math.sqrt(T) * zz)
    m, se = mean_se(math.exp(-R * T) * np.maximum(sq - K, 0.0))
    simulated("call by simulation, 4e6 paths", m, se, c)
    # PDE with the stated boundary conditions, solved numerically
    cn_call = crank_nicolson(lambda s: np.maximum(s - K, 0.0), lambda tau: 0.0, lambda tau, smax: smax - K * math.exp(-R * tau))
    approx("call by Crank-Nicolson with V(t,0) = 0 and V ~ S - K e^{-r(T-t)}", cn_call, c, 3)
    cn_put = crank_nicolson(lambda s: np.maximum(K - s, 0.0), lambda tau: K * math.exp(-R * tau), lambda tau, smax: 0.0)
    approx("put by Crank-Nicolson with V(t,0) = K e^{-r(T-t)} and V -> 0", cn_put, p, 3)


def boundary_conditions() -> None:
    print("Boundary behaviour of the closed form (card sc-bs-boundary-conditions)")
    tau = 0.5
    approx("call at S = 1e-6 (-> 0)", float(call(1e-6, K, tau, R, SIG)), 0.0, 12)
    approx("put at S = 1e-6 minus K e^{-r tau} (-> 0)", float(put(1e-6, K, tau, R, SIG)) - K * math.exp(-R * tau), 0.0, 5)
    for s in (300.0, 1000.0):
        approx(f"call at S = {s:g} minus (S - K e^(-r tau))", float(call(s, K, tau, R, SIG)) - (s - K * math.exp(-R * tau)), 0.0, 7)
        approx(f"put at S = {s:g} (-> 0)", float(put(s, K, tau, R, SIG)), 0.0, 7)
    # at S = 0 the PDE degenerates to V_t = r V, which is what fixes V(t, 0) = V(T, 0) e^{-r (T - t)}
    approx("PDE coefficients at S = 0: sigma^2 S^2 / 2 and r S", 0.5 * SIG**2 * 0.0**2 + R * 0.0, 0.0, 12)


def pde_checks() -> None:
    print("PDE residual, heat equation and Greeks identity by finite differences (cards sc-bs-pde, sc-bs-heat-equation)")
    t, s, ds, dt = 0.1, 100.0, 1e-2, 1e-5

    def v(t_: float, s_: float) -> float:
        return float(call(s_, K, T - t_, R, SIG))

    vt = (v(t + dt, s) - v(t - dt, s)) / (2 * dt)
    vs = (v(t, s + ds) - v(t, s - ds)) / (2 * ds)
    vss = (v(t, s + ds) - 2 * v(t, s) + v(t, s - ds)) / ds**2
    res = vt + 0.5 * SIG**2 * s**2 * vss + R * s * vs - R * v(t, s)
    assert abs(res) < 1e-6, res
    print(f"    PDE residual of the call at t = 0.1, S = 100: {res:.1e} (finite-difference noise; below 1e-6)")
    for f, name in ((lambda t_, s_: s_, "V = S"), (lambda t_, s_: K * math.exp(-R * (T - t_)), "V = K e^{-r(T-t)}")):
        ft = (f(t + dt, s) - f(t - dt, s)) / (2 * dt)
        fs = (f(t, s + ds) - f(t, s - ds)) / (2 * ds)
        fss = (f(t, s + ds) - 2 * f(t, s) + f(t, s - ds)) / ds**2
        r_ = ft + 0.5 * SIG**2 * s**2 * fss + R * s * fs - R * f(t, s)
        assert abs(r_) < 1e-4, (name, r_)
    print("    V = S and V = K e^{-r(T-t)} solve the PDE (residuals below 1e-4)")
    # heat equation: u(x, tau) = e^{r tau} V(T - tau, S) with x = ln S + (r - sigma^2/2) tau
    tau, x, hx, ht = 0.4, math.log(100.0) + (R - 0.5 * SIG**2) * 0.4, 1e-3, 1e-5

    def u(x_: float, tau_: float) -> float:
        s_ = math.exp(x_ - (R - 0.5 * SIG**2) * tau_)
        return math.exp(R * tau_) * float(call(s_, K, tau_, R, SIG))

    ut = (u(x, tau + ht) - u(x, tau - ht)) / (2 * ht)
    uxx = (u(x + hx, tau) - 2 * u(x, tau) + u(x - hx, tau)) / hx**2
    assert abs(ut - 0.5 * SIG**2 * uxx) < 1e-4, (ut, uxx)
    print(f"    u_tau - (sigma^2/2) u_xx = {ut - 0.5 * SIG**2 * uxx:.1e} after the substitution")
    # Greeks identity with closed-form Greeks
    tau = T - t
    d1, d2 = d12(s, K, tau, R, SIG)
    delta, gamma = float(ncdf(d1)), float(npdf(d1)) / (s * SIG * math.sqrt(tau))
    theta = -s * float(npdf(d1)) * SIG / (2 * math.sqrt(tau)) - R * K * math.exp(-R * tau) * float(ncdf(d2))
    approx(
        "Theta + sigma^2 S^2 Gamma / 2 + r S Delta - r V (closed-form Greeks)",
        theta + 0.5 * SIG**2 * s**2 * gamma + R * s * delta - R * v(t, s),
        0.0,
        10,
    )
    approx("finite-difference Delta vs N(d1)", vs, delta, 6)


def atm() -> None:
    print("At-the-money-forward approximation, S0 = K = 100, r = 0, sigma = 20%, T = 1 (card sc-bs-atm-approx)")
    exact_c = float(call(100.0, 100.0, 1.0, 0.0, 0.2))
    approx("exact", exact_c, 7.966, 3)
    approx("sigma S0 sqrt(T) / sqrt(2 pi)", 0.2 * 100 / math.sqrt(2 * math.pi), 7.979, 3)
    approx("0.4 sigma S0 sqrt(T)", 0.4 * 0.2 * 100, 8.0, 1)
    approx("1/sqrt(2 pi)", 1 / math.sqrt(2 * math.pi), 0.4, 1)
    z = np.linspace(-12, 12, 2_400_001)
    st = 100 * np.exp(-0.02 + 0.2 * z)
    approx("    exact by quadrature", float(np.sum(np.maximum(st - 100, 0) * npdf(z) * np.gradient(z))), exact_c, 6)
    approx("ATM vega per unit vol, S0 phi(d1) sqrt(T)", 100 * float(npdf(0.1)), 39.70, 2)


def power_solutions() -> None:
    print("Powers S^p solving the PDE, r = 5%, sigma = 25% (card sc-bs-power-solutions)")
    roots = sorted(float(z.real) for z in np.roots([0.5 * SIG**2, R - 0.5 * SIG**2, -R]))
    approx("root 1", roots[1], 1.0, 12)
    approx("root 2 = -2r/sigma^2", roots[0], -1.6, 12)
    p, s, ds = -1.6, 80.0, 1e-3

    def f(x: float) -> float:
        return x**p

    res = 0.5 * SIG**2 * s**2 * (f(s + ds) - 2 * f(s) + f(s - ds)) / ds**2 + R * s * (f(s + ds) - f(s - ds)) / (2 * ds) - R * f(s)
    assert abs(res) < 1e-9, res
    print(f"    finite-difference PDE residual of S^-1.6 at S = 80: {res:.1e}")
    approx("analytic residual 0.03125 (-1.6)(-2.6) + 0.05 (-1.6) - 0.05", 0.03125 * (-1.6) * (-2.6) + 0.05 * (-1.6) - 0.05, 0.0, 15)


def discrete_hedging(rng: np.random.Generator) -> None:
    print(
        "Discrete delta hedging of a sold one-year ATM call, sigma = 20%, r = 0, S0 = 100, 40,000 paths (card sc-bs-discrete-hedge-error)"
    )
    s0, k, sig, tm, paths = 100.0, 100.0, 0.2, 1.0, 40_000
    c0 = float(call(s0, k, tm, 0.0, sig))
    vega = s0 * float(npdf(d12(s0, k, tm, 0.0, sig)[0])) * math.sqrt(tm)
    approx("vega per unit of volatility", vega, 39.70, 2)
    quoted = {21: (1.48, 1.54), 84: (0.75, 0.77), 252: (0.44, 0.44)}
    sds: dict[int, float] = {}
    for n, (q_sim, q_rule) in quoted.items():
        h = tm / n
        s = np.full(paths, s0)
        pnl = np.full(paths, c0)
        for i in range(n):
            tau = tm - i * h
            delta = ncdf(d12(s, k, tau, 0.0, sig)[0])
            s_new = s * np.exp(-0.5 * sig**2 * h + sig * math.sqrt(h) * rng.standard_normal(paths))
            pnl += delta * (s_new - s)  # self-financing: gains only from the shares held over the step
            s = s_new
        pnl -= np.maximum(s - k, 0.0)
        sd = float(pnl.std(ddof=1))
        rule = math.sqrt(math.pi / 4) * sig * vega / math.sqrt(n)
        m, se = mean_se(pnl)
        simulated(f"mean P&L, N = {n} (zero within noise)", m, se, 0.0)
        approx(f"simulated sd, N = {n}", sd, q_sim, 2)
        approx(f"sqrt(pi/4) sigma vega / sqrt(N), N = {n}", rule, q_rule, 2)
        assert 0.90 < sd / rule < 1.02, (n, sd / rule)
        sds[n] = sd
    print("    simulated sd / rule lies in (0.90, 1.02) for every N, approaching 1 as N grows")
    approx("sd(N = 21) / sd(N = 84): quadrupling the frequency halves the error", sds[21] / sds[84], 2.0, 1)
    approx("sqrt(pi/4)", math.sqrt(math.pi / 4), 0.886, 3)


def main() -> None:
    rng = np.random.default_rng(SEED)
    prices(rng)
    boundary_conditions()
    pde_checks()
    atm()
    power_solutions()
    discrete_hedging(rng)
    print("all Black-Scholes checks passed")


if __name__ == "__main__":
    main()
