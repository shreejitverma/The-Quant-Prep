"""Sensitivities and revaluation: bump sizes, finite-difference error, AAD, Taylor proxies against full revaluation, grids.

Backs every number in 11-Risk-and-Trading/12-Sensitivities-and-Revaluation.md (and problems in 17-Risk-Problem-Set.md).

Conventions: Black-Scholes call with S = 100, K = 100, r = 5%, sigma = 20%, T = 1 (no dividends) unless stated.
Finite-difference errors in the truncation regime are asserted at the quoted rounding; errors in the round-off regime
depend on the last bits of the platform's libm, so they are asserted only as orders of magnitude.
AAD costs are counted in elementary operations recorded on the tape (deterministic), never in wall-clock time.
Simulations use fixed seeds; the note quotes them as "about".

Run: python 11-Risk-and-Trading/code/risk_sensitivities.py
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np

SQRT2 = math.sqrt(2.0)
EPS = 2.0**-52  # IEEE 754 double machine epsilon, 2.22e-16
Z99 = 2.3263478740408408

S0, K0, R0, VOL0, T0 = 100.0, 100.0, 0.05, 0.20, 1.0


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.10g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def check_range(label: str, value: float, lo: float, hi: float) -> float:
    """Print a value and assert it lies in [lo, hi] (used for round-off-dominated and order-of-magnitude claims)."""
    print(f"  {label}: {value:.3e}")
    assert lo <= value <= hi, f"{label}: {value} outside [{lo}, {hi}]"
    return value


def ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def npdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


_verf = np.vectorize(math.erf, otypes=[float])


def ncdf_v(x: np.ndarray) -> np.ndarray:
    return 0.5 * (1.0 + _verf(x / SQRT2))


def bs_call(s: float, k: float, r: float, vol: float, t: float) -> float:
    sq = vol * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / sq
    return s * ncdf(d1) - k * math.exp(-r * t) * ncdf(d1 - sq)


def bs_call_v(s: np.ndarray, k: float, r: np.ndarray, vol: np.ndarray, t: float) -> np.ndarray:
    sq = vol * math.sqrt(t)
    d1 = (np.log(s / k) + (r + 0.5 * vol * vol) * t) / sq
    return s * ncdf_v(d1) - k * np.exp(-r * t) * ncdf_v(d1 - sq)


def bs_greeks(s: float = S0, k: float = K0, r: float = R0, vol: float = VOL0, t: float = T0) -> dict[str, float]:
    """Analytic Black-Scholes call Greeks, including the third and fourth spot derivatives used for error analysis."""
    u = vol * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / u
    d2 = d1 - u
    gamma = npdf(d1) / (s * u)
    speed = -gamma / s * (1.0 + d1 / u)  # V'''(S)
    # V''''(S) = d(speed)/dS, differentiating speed = -(gamma / S)(1 + d1 / u) with d d1/dS = 1 / (S u)
    v4 = -speed / s * (1.0 + d1 / u) + gamma / s**2 * (1.0 + d1 / u) - gamma / (s * s * u * u)
    vega = s * npdf(d1) * math.sqrt(t)
    return {
        "price": s * ncdf(d1) - k * math.exp(-r * t) * ncdf(d2),
        "delta": ncdf(d1),
        "gamma": gamma,
        "speed": speed,
        "v4": v4,
        "vega": vega,
        "rho": k * t * math.exp(-r * t) * ncdf(d2),
        "dv_dk": -math.exp(-r * t) * ncdf(d2),
        "dv_dt": s * npdf(d1) * vol / (2.0 * math.sqrt(t)) + r * k * math.exp(-r * t) * ncdf(d2),
        "vanna": -npdf(d1) * d2 / vol,
        "volga": vega * d1 * d2 / vol,
        "d1": d1,
        "d2": d2,
    }


# ---------------------------------------------------------------------------
# Core concepts "Finite differences": truncation against round-off (cards risk-optimal-finite-difference-bump-size,
# risk-forward-vs-central-difference, risk-floating-point-cancellation-definition, risk-optimal-gamma-step-size-derivation)
# ---------------------------------------------------------------------------


def fd_delta_forward(h: float) -> float:
    return (bs_call(S0 + h, K0, R0, VOL0, T0) - bs_call(S0, K0, R0, VOL0, T0)) / h


def fd_delta_central(h: float) -> float:
    return (bs_call(S0 + h, K0, R0, VOL0, T0) - bs_call(S0 - h, K0, R0, VOL0, T0)) / (2.0 * h)


def fd_gamma_central(h: float) -> float:
    v0 = bs_call(S0, K0, R0, VOL0, T0)
    return (bs_call(S0 + h, K0, R0, VOL0, T0) - 2.0 * v0 + bs_call(S0 - h, K0, R0, VOL0, T0)) / (h * h)


def section_finite_differences() -> None:
    g = bs_greeks()
    print("\n[Black-Scholes reference values]")
    check("call value", g["price"], 10.4506, 5e-5)
    check("delta N(d1)", g["delta"], 0.636831, 5e-7)
    check("gamma", g["gamma"], 0.018762, 5e-7)
    check("vega", g["vega"], 37.5240, 5e-5)
    check("speed V'''", g["speed"], -0.000516, 5e-7)
    check("V''''", g["v4"], -0.0000276, 5e-8)

    print("\n[Finite-difference error table, absolute bump h in spot units]")
    rows = {}
    for h in (1.0, 0.1, 0.01, 1e-3, 1e-4, 1e-6, 1e-8):
        ef = abs(fd_delta_forward(h) - g["delta"])
        ec = abs(fd_delta_central(h) - g["delta"])
        eg = abs(fd_gamma_central(h) - g["gamma"])
        rows[h] = (ef, ec, eg)
        print(f"  h={h:>7g}: forward delta err {ef:.2e}, central delta err {ec:.2e}, central gamma err {eg:.2e}")
    # Truncation regime: errors follow the leading Taylor terms h*gamma/2, h^2*|speed|/6, h^2*|V''''|/12.
    check("forward delta error, h = 1", rows[1.0][0], 0.0093, 5e-5)
    check("leading term gamma/2 for h = 1", g["gamma"] / 2.0, 0.0094, 5e-5)
    check("forward delta error, h = 0.01", rows[0.01][0], 0.000094, 5e-7)
    check("central delta error, h = 1", rows[1.0][1], 0.000086, 5e-7)
    check("leading term |speed|/6 for h = 1", abs(g["speed"]) / 6.0, 0.000086, 5e-7)
    check("central delta error x 1e9, h = 0.01", rows[0.01][1] * 1e9, 8.6, 0.05)
    check("central gamma error x 1e7, h = 1", rows[1.0][2] * 1e7, 23.0, 0.05)
    check("leading term |V''''|/12 x 1e7", abs(g["v4"]) / 12.0 * 1e7, 23.0, 0.05)
    # Round-off regime: only orders of magnitude are platform independent.
    check("forward delta error x 1e7, h = 1e-4 (truncation still dominates)", rows[1e-4][0] * 1e7, 9.38, 0.01)
    # Mixed and round-off regimes: the table in the note quotes these ranges, not digits.
    check_range("central gamma error, h = 0.01 (mixed)", rows[0.01][2], 0.0, 1e-9)
    check_range("central delta error, h = 1e-4 (round-off)", rows[1e-4][1], 0.0, 1e-10)
    check_range("central gamma error, h = 1e-4 (round-off)", rows[1e-4][2], 1e-8, 1e-6)
    check_range("forward delta error, h = 1e-6 (mixed)", rows[1e-6][0], 1e-9, 1e-7)
    check_range("central delta error, h = 1e-6 (round-off)", rows[1e-6][1], 1e-10, 1e-7)
    check_range("forward delta error, h = 1e-8 (round-off)", rows[1e-8][0], 1e-8, 1e-5)
    check_range("central delta error, h = 1e-8 (round-off)", rows[1e-8][1], 1e-8, 1e-5)
    check_range("central gamma error, h = 1e-8 (round-off)", rows[1e-8][2], 1e-3, 1e3)
    check_range("central gamma error, h = 1e-6 (round-off, garbage)", rows[1e-6][2], 1e-4, 1e1)
    check("round-off scale eps |V| x 1e15", EPS * g["price"] * 1e15, 2.32, 0.005)
    check("round-off bound 4 eps |V| / h^2 at h = 1e-6", 4.0 * EPS * g["price"] / 1e-12, 0.0093, 5e-5)
    check_range("gamma error at h = 1e-6 relative to gamma", rows[1e-6][2] / g["gamma"], 0.01, 1.0)

    print("\n[Optimal bumps from minimising truncation + round-off, eps = 2.22e-16]")
    v = g["price"]
    h_fwd = 2.0 * math.sqrt(EPS * v / g["gamma"])
    h_cen = (3.0 * EPS * v / abs(g["speed"])) ** (1.0 / 3.0)
    h_gam = (48.0 * EPS * v / abs(g["v4"])) ** 0.25
    check("eps^(1/2)", math.sqrt(EPS), 1.49e-8, 5e-11)
    check("eps^(1/3)", EPS ** (1.0 / 3.0), 6.06e-6, 5e-9)
    check("eps^(1/4)", EPS**0.25, 1.22e-4, 5e-7)
    check("forward-difference optimal h", h_fwd, 7.0e-7, 5e-9)
    check("central-difference optimal h", h_cen, 0.00024, 5e-6)
    check("central gamma optimal h", h_gam, 0.0080, 5e-5)
    err_cen_opt = abs(fd_delta_central(h_cen) - g["delta"])
    err_gam_opt = abs(fd_gamma_central(h_gam) - g["gamma"])
    check_range("central delta error at its optimal h", err_cen_opt, 0.0, 5e-10)
    check_range("central gamma error at its optimal h", err_gam_opt, 0.0, 5e-8)

    print("\n[Regulatory sensitivity: FRTB equity delta is a one-sided 1% relative bump (MAR21.21)]")
    s_frtb = (bs_call(1.01 * S0, K0, R0, VOL0, T0) - bs_call(S0, K0, R0, VOL0, T0)) / 0.01
    check("MAR21.21 sensitivity (V(1.01 S) - V(S)) / 0.01", s_frtb, 64.6125, 5e-4)
    check("S x delta", S0 * g["delta"], 63.6831, 5e-4)
    check("difference, about S^2 gamma x 0.01 / 2", s_frtb - S0 * g["delta"], 0.9294, 5e-4)


# ---------------------------------------------------------------------------
# Core concepts "Bumping a Monte Carlo pricer" (cards risk-common-random-numbers-bumping, risk-pathwise-digital-failure)
# ---------------------------------------------------------------------------


def mc_terminal(s: float, z: np.ndarray) -> np.ndarray:
    return s * np.exp((R0 - 0.5 * VOL0**2) * T0 + VOL0 * math.sqrt(T0) * z)


def section_mc_bumping() -> None:
    print("\n[Monte Carlo deltas: independent seeds, common random numbers, pathwise (the AAD estimator)]")
    n_paths, n_reps = 20_000, 200
    disc = math.exp(-R0 * T0)
    rng = np.random.default_rng(20261018)
    est: dict[str, list[float]] = {"indep h=0.01": [], "crn h=0.01": [], "crn h=1": [], "pathwise": [], "dig crn h=1": []}
    est["dig crn h=0.01"] = []
    for _ in range(n_reps):
        z = rng.standard_normal(n_paths)
        z2 = rng.standard_normal(n_paths)
        z3 = rng.standard_normal(n_paths)
        h = 0.01
        up_indep = disc * np.maximum(mc_terminal(S0 + h, z2) - K0, 0.0).mean()
        dn_indep = disc * np.maximum(mc_terminal(S0 - h, z3) - K0, 0.0).mean()
        est["indep h=0.01"].append((up_indep - dn_indep) / (2 * h))
        for hh, key in ((0.01, "crn h=0.01"), (1.0, "crn h=1")):
            up = disc * np.maximum(mc_terminal(S0 + hh, z) - K0, 0.0).mean()
            dn = disc * np.maximum(mc_terminal(S0 - hh, z) - K0, 0.0).mean()
            est[key].append((up - dn) / (2 * hh))
        st = mc_terminal(S0, z)
        est["pathwise"].append(disc * np.mean((st > K0) * st / S0))
        for hh, key in ((1.0, "dig crn h=1"), (0.01, "dig crn h=0.01")):
            up = disc * (mc_terminal(S0 + hh, z) > K0).mean()
            dn = disc * (mc_terminal(S0 - hh, z) > K0).mean()
            est[key].append((up - dn) / (2 * hh))
    sd = {k: float(np.std(v, ddof=1)) for k, v in est.items()}
    mean = {k: float(np.mean(v)) for k, v in est.items()}
    g = bs_greeks()
    print(f"  {n_reps} replications of {n_paths} paths each")
    check("sd, independent seeds, h = 0.01", sd["indep h=0.01"], 7.07, 0.1)
    check("sd, common random numbers, h = 0.01", sd["crn h=0.01"], 0.0039, 1e-4)
    check("sd, common random numbers, h = 1", sd["crn h=1"], 0.0039, 1e-4)
    check("sd, pathwise", sd["pathwise"], 0.0039, 1e-4)
    check("mean pathwise delta", mean["pathwise"], g["delta"], 2e-3)
    true_dig_delta = math.exp(-R0 * T0) * npdf(g["d2"]) / (S0 * VOL0 * math.sqrt(T0))
    check("digital delta, exact e^(-rT) phi(d2) / (S sigma sqrt(T))", true_dig_delta, 0.018762, 5e-6)
    check("digital, CRN h = 1, sd", sd["dig crn h=1"], 0.00065, 3e-5)
    check("digital, CRN h = 0.01, sd", sd["dig crn h=0.01"], 0.0067, 2e-4)
    check("digital, CRN h = 1, mean", mean["dig crn h=1"], true_dig_delta, 5e-4)


# ---------------------------------------------------------------------------
# Core concepts "AAD" (cards risk-aad-adjoint-algorithmic-differentiation, risk-aad-cost-count, risk-aad-tape-checkpointing)
# ---------------------------------------------------------------------------


class Tape:
    """Minimal reverse-mode AD tape: each recorded node stores (parent index, local partial) pairs."""

    def __init__(self) -> None:
        self.nodes: list[tuple[tuple[int, float], ...]] = []
        self.n_inputs = 0

    def var(self, value: float) -> Var:
        self.nodes.append(())
        self.n_inputs += 1
        return Var(self, len(self.nodes) - 1, value)

    def record(self, value: float, parents: tuple[tuple[int, float], ...]) -> Var:
        self.nodes.append(parents)
        return Var(self, len(self.nodes) - 1, value)

    def ops(self) -> int:
        """Elementary operations recorded by the forward sweep (inputs excluded)."""
        return len(self.nodes) - self.n_inputs

    def edges(self) -> int:
        return sum(len(p) for p in self.nodes)

    def gradient(self, out: Var) -> list[float]:
        adj = [0.0] * len(self.nodes)
        adj[out.idx] = 1.0
        for i in range(len(self.nodes) - 1, -1, -1):
            a = adj[i]
            if a == 0.0:
                continue
            for p, d in self.nodes[i]:
                adj[p] += a * d
        return adj


class Var:
    __slots__ = ("tape", "idx", "val")

    def __init__(self, tape: Tape, idx: int, val: float) -> None:
        self.tape, self.idx, self.val = tape, idx, val

    def __add__(self, o: Var | float) -> Var:
        if isinstance(o, Var):
            return self.tape.record(self.val + o.val, ((self.idx, 1.0), (o.idx, 1.0)))
        return self.tape.record(self.val + o, ((self.idx, 1.0),))

    __radd__ = __add__

    def __sub__(self, o: Var | float) -> Var:
        if isinstance(o, Var):
            return self.tape.record(self.val - o.val, ((self.idx, 1.0), (o.idx, -1.0)))
        return self.tape.record(self.val - o, ((self.idx, 1.0),))

    def __rsub__(self, o: float) -> Var:
        return self.tape.record(o - self.val, ((self.idx, -1.0),))

    def __neg__(self) -> Var:
        return self.tape.record(-self.val, ((self.idx, -1.0),))

    def __mul__(self, o: Var | float) -> Var:
        if isinstance(o, Var):
            return self.tape.record(self.val * o.val, ((self.idx, o.val), (o.idx, self.val)))
        return self.tape.record(self.val * o, ((self.idx, o),))

    __rmul__ = __mul__

    def __truediv__(self, o: Var | float) -> Var:
        if isinstance(o, Var):
            return self.tape.record(self.val / o.val, ((self.idx, 1.0 / o.val), (o.idx, -self.val / (o.val * o.val))))
        return self.tape.record(self.val / o, ((self.idx, 1.0 / o),))

    def __rtruediv__(self, o: float) -> Var:
        return self.tape.record(o / self.val, ((self.idx, -o / (self.val * self.val)),))


def v_exp(x: Var) -> Var:
    e = math.exp(x.val)
    return x.tape.record(e, ((x.idx, e),))


def v_log(x: Var) -> Var:
    return x.tape.record(math.log(x.val), ((x.idx, 1.0 / x.val),))


def v_sqrt(x: Var) -> Var:
    s = math.sqrt(x.val)
    return x.tape.record(s, ((x.idx, 0.5 / s),))


def v_ncdf(x: Var) -> Var:
    return x.tape.record(ncdf(x.val), ((x.idx, npdf(x.val)),))


def bs_call_aad(s: Var, k: Var, r: Var, vol: Var, t: Var) -> Var:
    sq = vol * v_sqrt(t)
    d1 = (v_log(s / k) + (r + 0.5 * vol * vol) * t) / sq
    d2 = d1 - sq
    return s * v_ncdf(d1) - k * v_exp(-(r * t)) * v_ncdf(d2)


def section_aad_black_scholes() -> None:
    print("\n[AAD on Black-Scholes: all five first-order Greeks from one reverse sweep]")
    tape = Tape()
    xs = [tape.var(v) for v in (S0, K0, R0, VOL0, T0)]
    price = bs_call_aad(*xs)
    adj = tape.gradient(price)
    g = bs_greeks()
    names = ("delta", "dv_dk", "rho", "vega", "dv_dt")
    worst = max(abs(adj[x.idx] - g[n]) for x, n in zip(xs, names, strict=True))
    for x, n in zip(xs, names, strict=True):
        print(f"  {n}: AAD {adj[x.idx]:.12f}, analytic {g[n]:.12f}")
    check_range("max |AAD - analytic| over the five Greeks", worst, 0.0, 1e-12)
    check("dV/dK", g["dv_dk"], -0.532325, 5e-7)
    check("rho", g["rho"], 53.2325, 5e-4)
    check("dV/dT (theta with opposite sign)", g["dv_dt"], 6.4140, 5e-4)
    ops, edges = tape.ops(), tape.edges()
    print(f"  forward ops {ops}, reverse multiply-adds {edges}")
    check("forward elementary ops", ops, 20, 0)
    check("reverse multiply-adds", edges, 33, 0)
    check("AAD cost / pricing cost (ops + adds) / ops", (ops + edges) / ops, 2.65, 5e-3)
    check("central FD cost / pricing cost for 5 inputs", bump_counts(5)["cen_grad"], 10, 0)


def zero_rate_weights(t: float, pillars: Sequence[float]) -> list[tuple[int, float]]:
    """Linear interpolation weights on the pillar zero rates, flat outside the pillar range."""
    if t <= pillars[0]:
        return [(0, 1.0)]
    if t >= pillars[-1]:
        return [(len(pillars) - 1, 1.0)]
    j = int(np.searchsorted(pillars, t)) - 1
    w = (t - pillars[j]) / (pillars[j + 1] - pillars[j])
    return [(j, 1.0 - w), (j + 1, w)]


def book_cashflows() -> list[tuple[float, float]]:
    """A labelled toy book: long 4% 30-year, short 3% 10-year, long 5% 5-year semi-annual bonds (notionals 1m, 2m, 1.5m)."""
    flows: dict[float, float] = {}
    for coupon, maturity, notional in ((0.04, 30.0, 1e6), (0.03, 10.0, -2e6), (0.05, 5.0, 1.5e6)):
        n = int(round(maturity * 2))
        for i in range(1, n + 1):
            t = i * 0.5
            flows[t] = flows.get(t, 0.0) + notional * coupon / 2.0 + (notional if i == n else 0.0)
    return sorted(flows.items())


def book_pv(z: Sequence[float], pillars: Sequence[float], flows: list[tuple[float, float]]) -> float:
    pv = 0.0
    for t, cf in flows:
        zt = sum(w * z[j] for j, w in zero_rate_weights(t, pillars))
        pv += cf * math.exp(-zt * t)
    return pv


def book_pv_aad(z: list[Var], pillars: Sequence[float], flows: list[tuple[float, float]]) -> Var:
    pv: Var | float = 0.0
    for t, cf in flows:
        terms = [z[j] * w for j, w in zero_rate_weights(t, pillars)]
        zt = terms[0] if len(terms) == 1 else terms[0] + terms[1]
        pv = pv + v_exp(zt * (-t)) * cf
    assert isinstance(pv, Var)
    return pv


def section_aad_curve() -> None:
    print("\n[AAD against bumping on a 30-pillar curve (toy bond book)]")
    pillars = [float(y) for y in range(1, 31)]
    z0 = [0.03 + 0.0005 * (y - 1) for y in range(1, 31)]  # labelled upward-sloping zero curve, 3.0% to 4.45%
    flows = book_cashflows()
    tape = Tape()
    zv = [tape.var(v) for v in z0]
    pv = book_pv_aad(zv, pillars, flows)
    adj = tape.gradient(pv)
    grad_aad = [adj[v.idx] for v in zv]
    # Analytic gradient by the chain rule: dPV/dz_j = sum_k -t_k CF_k exp(-z(t_k) t_k) w_kj
    grad_exact = [0.0] * len(pillars)
    for t, cf in flows:
        ws = zero_rate_weights(t, pillars)
        zt = sum(w * z0[j] for j, w in ws)
        for j, w in ws:
            grad_exact[j] += -t * cf * math.exp(-zt * t) * w
    h = 1e-4

    def bumped(j: int, d: float) -> float:
        zz = list(z0)
        zz[j] += d
        return book_pv(zz, pillars, flows)

    base = book_pv(z0, pillars, flows)
    grad_cen = [(bumped(j, h) - bumped(j, -h)) / (2 * h) for j in range(len(pillars))]
    grad_fwd = [(bumped(j, h) - base) / h for j in range(len(pillars))]
    rel = [abs(grad_aad[j] - grad_exact[j]) / abs(grad_exact[j]) for j in range(len(pillars)) if grad_exact[j] != 0.0]
    check_range("max relative |AAD - chain rule|", max(rel), 0.0, 1e-12)
    j30 = 29
    check("PV of the book", base, 667555.34, 0.01)
    check("PV01 at the 30y pillar (per bp)", grad_exact[j30] * 1e-4, -813.26, 0.01)
    check("relative error, forward 1bp at 30y", abs(grad_fwd[j30] - grad_exact[j30]) / abs(grad_exact[j30]), 0.0015, 5e-5)
    check("relative error, central 1bp at 30y, x 1e6", abs(grad_cen[j30] - grad_exact[j30]) / abs(grad_exact[j30]) * 1e6, 1.5, 0.05)
    ops, edges = tape.ops(), tape.edges()
    ratio = (ops + edges) / ops
    print(f"  cash flows {len(flows)}, forward ops {ops}, reverse multiply-adds {edges}")
    check("AAD cost / one pricing", ratio, 2.28, 5e-3)
    check("central FD cost / one pricing (2N, N = 30)", bump_counts(len(pillars))["cen_grad"], 60, 0)
    check("forward FD cost / one pricing (N + 1)", bump_counts(len(pillars))["fwd_grad"], 31, 0)


def bump_counts(n: int) -> dict[str, int]:
    """Pricing calls: gradient by forward (N + 1) or central (2N) differences, full Hessian by central differences."""
    return {"fwd_grad": n + 1, "cen_grad": 2 * n, "hessian": 2 * n * n + 1}


def section_costs() -> None:
    print("\n[Bump counts and full-revaluation cost (labelled hypothetical inputs)]")
    for n, exp_h in ((10, 201), (100, 20_001), (1000, 2_000_001)):
        check(f"full central Hessian pricings, N = {n}", bump_counts(n)["hessian"], exp_h, 0)
    check("central gradient pricings, N = 2,000", bump_counts(2000)["cen_grad"], 4_000, 0)
    check("forward gradient pricings, N = 2,000", bump_counts(2000)["fwd_grad"], 2_001, 0)
    check("full central Hessian pricings, N = 5,000", bump_counts(5000)["hessian"], 50_000_001, 0)
    trades, scenarios, micros = 500_000, 10_000, 10.0  # hypothetical book, scenario count and cost per pricing call
    calls = trades * scenarios
    check("pricing calls for full revaluation", calls, 5e9, 0)
    check("CPU-hours at 10 microseconds a call", calls * micros * 1e-6 / 3600.0, 13.9, 0.05)


# ---------------------------------------------------------------------------
# Worked example 2: full revaluation against Taylor proxies (cards risk-full-revaluation-vs-taylor-tradeoff,
# risk-taylor-proxy-tail-underestimation, risk-diagonal-vs-cross-gamma, risk-proxy-stress-breakdown)
# ---------------------------------------------------------------------------


def aad_gradient_call(x: Sequence[float]) -> list[float]:
    tape = Tape()
    s, r, vol = (tape.var(v) for v in x)
    k, t = tape.var(K0), tape.var(T0)
    out = bs_call_aad(s, k, r, vol, t)
    adj = tape.gradient(out)
    return [adj[s.idx], adj[r.idx], adj[vol.idx]]


def hessian_from_aad(x: Sequence[float], h: Sequence[float]) -> np.ndarray:
    """Central differences of the AAD gradient: truncation O(h^2), round-off eps / h only (one division)."""
    n = len(x)
    hess = np.zeros((n, n))
    for j in range(n):
        up, dn = list(x), list(x)
        up[j] += h[j]
        dn[j] -= h[j]
        gu, gd = aad_gradient_call(up), aad_gradient_call(dn)
        for i in range(n):
            hess[i, j] = (gu[i] - gd[i]) / (2 * h[j])
    return 0.5 * (hess + hess.T)


def var_es(loss: np.ndarray, q: float = 0.99) -> tuple[float, float]:
    """Empirical VaR (the ceil(qN)-th smallest loss) and ES (mean of the losses at or beyond it)."""
    srt = np.sort(loss)
    k = int(math.ceil(q * len(srt))) - 1
    return float(srt[k]), float(srt[k:].mean())


def scenario_pnls(scale: float, seed: int, n: int = 100_000) -> dict[str, np.ndarray]:
    sd = np.array([5.0, 0.0025, 0.02]) * scale
    corr = np.array([[1.0, 0.2, -0.5], [0.2, 1.0, 0.0], [-0.5, 0.0, 1.0]])
    cov = np.outer(sd, sd) * corr
    rng = np.random.default_rng(seed)
    dx = rng.standard_normal((n, 3)) @ np.linalg.cholesky(cov).T
    x0 = np.array([S0, R0, VOL0])
    assert (x0[2] + dx[:, 2]).min() > 0.0, "a scenario produced a negative volatility"
    v0 = bs_call(S0, K0, R0, VOL0, T0)
    full = bs_call_v(x0[0] + dx[:, 0], K0, x0[1] + dx[:, 1], x0[2] + dx[:, 2], T0) - v0
    grad = np.array(aad_gradient_call(x0))
    hess = hessian_from_aad(x0, [1e-3, 1e-6, 1e-6])
    lin = dx @ grad
    diag = lin + 0.5 * (dx**2) @ np.diag(hess)
    full2 = lin + 0.5 * np.einsum("ni,ij,nj->n", dx, hess, dx)
    return {"full": full, "delta": lin, "diag": diag, "dg": full2, "dx": dx}


def section_proxies() -> None:
    print("\n[Hessian of the call in (S, r, sigma) by central differences of the AAD gradient]")
    x0 = [S0, R0, VOL0]
    hess = hessian_from_aad(x0, [1e-3, 1e-6, 1e-6])
    g = bs_greeks()
    check("gamma", hess[0, 0], g["gamma"], 1e-8)
    check("vanna d2V/dS dsigma", hess[0, 2], g["vanna"], 1e-7)
    check("volga d2V/dsigma^2", hess[2, 2], g["volga"], 1e-5)
    check("vanna", g["vanna"], -0.281430, 5e-7)
    check("volga", g["volga"], 9.8501, 5e-4)
    check("d2V/dS dr", hess[0, 1], 1.8762, 5e-4)

    print("\n[Worked example 2: 100,000 correlated scenarios on (S, r, sigma), 99% VaR and ES of the loss]")
    out = scenario_pnls(1.0, seed=7)
    full = out["full"]
    stats = {}
    for key in ("full", "delta", "diag", "dg"):
        var, es = var_es(-out[key])
        err = out[key] - full
        stats[key] = (var, es, float(np.abs(err).mean()), float(np.sqrt((err**2).mean())), float(np.abs(err).max()))
        print(f"  {key:>5}: VaR {var:.3f}, ES {es:.3f}, MAE {stats[key][2]:.4f}, RMSE {stats[key][3]:.4f}, max {stats[key][4]:.3f}")
    check("full revaluation VaR", stats["full"][0], 5.50, 0.01)
    check("full revaluation ES", stats["full"][1], 6.06, 0.01)
    check("delta-only VaR", stats["delta"][0], 6.78, 0.01)
    check("delta-only ES", stats["delta"][1], 7.71, 0.01)
    check("diagonal delta-gamma VaR", stats["diag"][0], 5.56, 0.01)
    check("full second-order (with cross terms) VaR", stats["dg"][0], 5.50, 0.01)
    check("full second-order ES", stats["dg"][1], 6.09, 0.01)
    check("full second-order MAE", stats["dg"][2], 0.019, 0.001)
    check("delta-only MAE", stats["delta"][2], 0.252, 0.002)
    check("diagonal MAE", stats["diag"][2], 0.030, 0.001)
    check("full second-order max abs error", stats["dg"][4], 0.76, 0.01)
    check("delta-only VaR / full VaR", stats["delta"][0] / stats["full"][0], 1.234, 5e-4)

    print("\n[Same book, shocks doubled (stress calibration)]")
    st = scenario_pnls(2.0, seed=7)
    sv_full = var_es(-st["full"])
    sv_dg = var_es(-st["dg"])
    print(f"  full VaR {sv_full[0]:.3f} ES {sv_full[1]:.3f}; second-order VaR {sv_dg[0]:.3f} ES {sv_dg[1]:.3f}")
    check("stressed full VaR", sv_full[0], 8.68, 0.01)
    check("stressed second-order VaR", sv_dg[0], 8.84, 0.01)
    check("stressed full ES", sv_full[1], 9.18, 0.01)
    check("stressed second-order ES", sv_dg[1], 9.62, 0.01)
    check("stressed second-order max abs error", float(np.abs(st["dg"] - st["full"]).max()), 6.72, 0.01)
    check("stressed second-order VaR minus full VaR", sv_dg[0] - sv_full[0], 0.155, 0.001)
    check(
        "max error ratio, doubled shocks to base (third-order error: about 2^3)",
        float(np.abs(st["dg"] - st["full"]).max()) / stats["dg"][4],
        8.84,
        0.01,
    )
    vertex = -g["delta"] / g["gamma"]
    check("spot-only parabola vertex -delta/gamma", vertex, -33.94, 0.01)
    # A long call cannot lose more than its premium; the quadratic has no such bound.
    v0 = g["price"]
    check("worst full-revaluation loss in the stressed run", float(-st["full"].min()), 10.29, 0.01)
    check("premium V0 (upper bound on any loss)", v0, 10.4506, 5e-5)
    check("worst second-order loss in the stressed run", float(-st["dg"].min()), 12.41, 0.01)


# ---------------------------------------------------------------------------
# Core concepts "Where Taylor fails": a down-and-out call (card risk-barrier-options-taylor-failure)
# ---------------------------------------------------------------------------


def down_and_out_call(s: float, k: float, h: float, r: float, vol: float, t: float) -> float:
    """Continuously monitored down-and-out call, barrier h <= strike k, no dividends (Hull, Options Futures and Other
    Derivatives, chapter on exotic options).  Zero once spot is at or below the barrier."""
    if s <= h:
        return 0.0
    u = vol * math.sqrt(t)
    lam = (r + 0.5 * vol * vol) / (vol * vol)
    y = math.log(h * h / (s * k)) / u + lam * u
    c_di = s * (h / s) ** (2 * lam) * ncdf(y) - k * math.exp(-r * t) * (h / s) ** (2 * lam - 2) * ncdf(y - u)
    return bs_call(s, k, r, vol, t) - c_di


def doc_mc_bridge(n_paths: int, n_steps: int, seed: int) -> tuple[float, float]:
    """Monte Carlo with the Brownian-bridge survival probability between steps: exact continuous monitoring."""
    rng = np.random.default_rng(seed)
    dt = T0 / n_steps
    x = np.full(n_paths, math.log(S0))
    b = math.log(90.0)
    surv = np.ones(n_paths)
    for _ in range(n_steps):
        x_new = x + (R0 - 0.5 * VOL0**2) * dt + VOL0 * math.sqrt(dt) * rng.standard_normal(n_paths)
        alive = (x > b) & (x_new > b)
        p_cross = np.exp(-2.0 * np.maximum(x - b, 0.0) * np.maximum(x_new - b, 0.0) / (VOL0**2 * dt))
        surv *= np.where(alive, 1.0 - p_cross, 0.0)
        x = x_new
    pay = math.exp(-R0 * T0) * np.maximum(np.exp(x) - K0, 0.0) * surv
    return float(pay.mean()), float(pay.std(ddof=1) / math.sqrt(n_paths))


def section_barrier() -> None:
    print("\n[Down-and-out call S = 100, K = 100, barrier 90: closed form, bridge Monte Carlo, Taylor proxy]")
    hb = 90.0

    def f(s: float) -> float:
        return down_and_out_call(s, K0, hb, R0, VOL0, T0)

    v0 = f(S0)
    mc, se = doc_mc_bridge(1_000_000, 20, seed=11)
    check("closed-form value", v0, 8.6655, 5e-5)
    check("bridge Monte Carlo value (about)", mc, 8.668, 0.001)
    assert abs(mc - v0) < 3 * se, f"Monte Carlo {mc} differs from closed form {v0} by more than 3 standard errors {se}"
    h = 0.01
    delta = (f(S0 + h) - f(S0 - h)) / (2 * h)
    gamma = (f(S0 + h) - 2 * v0 + f(S0 - h)) / (h * h)
    check("barrier delta", delta, 0.8302, 5e-4)
    check("barrier gamma (negative: long a call, short a down-and-in)", gamma, -0.00101, 5e-6)
    print("  spot move | full revaluation P&L | delta-gamma P&L")
    table = {}
    for ds in (-5.0, -9.0, -9.9, -10.1, -15.0):
        full = f(S0 + ds) - v0
        prox = delta * ds + 0.5 * gamma * ds * ds
        table[ds] = (full, prox)
        print(f"  {ds:>6.1f} | {full:>9.4f} | {prox:>9.4f}")
    check("full P&L, spot -9.9", table[-9.9][0], -8.5712, 5e-4)
    check("proxy P&L, spot -9.9", table[-9.9][1], -8.2680, 5e-4)
    check("full P&L, spot -10.1 (knocked out)", table[-10.1][0], -8.6655, 5e-4)
    check("proxy P&L, spot -10.1", table[-10.1][1], -8.4360, 5e-4)
    check("full P&L, spot -5", table[-5.0][0], -4.1966, 5e-4)
    check("proxy P&L, spot -5", table[-5.0][1], -4.1634, 5e-4)
    gamma_near = (f(90.51) - 2 * f(90.5) + f(90.49)) / 1e-4
    check("gamma just above the barrier, S = 90.5", gamma_near, -0.0243, 5e-5)
    check("gamma near the barrier / gamma at spot 100", gamma_near / gamma, 24.15, 0.01)


# ---------------------------------------------------------------------------
# Core concepts "Grids and Chebyshev" (cards risk-chebyshev-grid-revaluation, risk-spot-ladder-interpolation)
# ---------------------------------------------------------------------------


def section_chebyshev() -> None:
    print("\n[Chebyshev interpolation of the call value in spot on [50, 150]]")
    grid = np.linspace(50.0, 150.0, 2001)
    exact = np.array([bs_call(s, K0, R0, VOL0, T0) for s in grid])

    def f(s: np.ndarray) -> np.ndarray:
        return np.array([bs_call(float(x), K0, R0, VOL0, T0) for x in np.atleast_1d(s)])

    errs = {}
    for deg in (4, 8, 16, 32):
        p = np.polynomial.Chebyshev.interpolate(f, deg, domain=[50.0, 150.0])
        errs[deg] = float(np.abs(p(grid) - exact).max())
        print(f"  degree {deg:>2} ({deg + 1} pricings): max error {errs[deg]:.2e}")
    # numpy's Chebyshev.interpolate uses the deg + 1 Chebyshev points of the first kind (roots of T_{deg+1})
    check("max error, degree 4", errs[4], 0.325, 5e-4)
    check("max error, degree 8, x 1e3", errs[8] * 1e3, 9.38, 0.01)
    check("max error, degree 16, x 1e6", errs[16] * 1e6, 1.98, 0.01)
    check_range("max error, degree 32", errs[32], 0.0, 1e-9)
    # Linear interpolation on an equally spaced spot ladder of 21 points (5-unit steps)
    ladder = np.linspace(50.0, 150.0, 21)
    lin = np.interp(grid, ladder, np.array([bs_call(s, K0, R0, VOL0, T0) for s in ladder]))
    err_lin = float(np.abs(lin - exact).max())
    check("max error, linear interpolation on a 21-point ladder", err_lin, 0.0676, 5e-4)

    print("\n[Same for the down-and-out call on [80, 120]: kink at the barrier, then split at the barrier]")
    grid_b = np.linspace(80.0, 120.0, 4001)
    exact_b = np.array([down_and_out_call(s, K0, 90.0, R0, VOL0, T0) for s in grid_b])

    def fb(s: np.ndarray) -> np.ndarray:
        return np.array([down_and_out_call(float(x), K0, 90.0, R0, VOL0, T0) for x in np.atleast_1d(s)])

    errs_b = {}
    for deg in (16, 64):
        p = np.polynomial.Chebyshev.interpolate(fb, deg, domain=[80.0, 120.0])
        errs_b[deg] = float(np.abs(p(grid_b) - exact_b).max())
        print(f"  degree {deg:>2}: max error {errs_b[deg]:.2e}")
    check("barrier, max error degree 16", errs_b[16], 0.246, 0.001)
    check("barrier, max error degree 64", errs_b[64], 0.063, 0.001)
    above = grid_b >= 90.0
    p_split = np.polynomial.Chebyshev.interpolate(fb, 16, domain=[90.0, 120.0])
    err_split = float(np.abs(p_split(grid_b[above]) - exact_b[above]).max())
    check_range("barrier, degree 16 on [90, 120] only (zero below 90)", err_split, 0.0, 1e-9)


def main() -> None:
    section_finite_differences()
    section_mc_bumping()
    section_aad_black_scholes()
    section_aad_curve()
    section_costs()
    section_proxies()
    section_barrier()
    section_chebyshev()
    print("\nAll sensitivity and revaluation checks passed.")


if __name__ == "__main__":
    main()
