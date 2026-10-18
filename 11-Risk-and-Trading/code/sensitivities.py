"""Sensitivities and revaluation: bump sizes, finite-difference error, Taylor proxies, Chebyshev grids, AAD against bumping.

Backs every number in 11-Risk-and-Trading/12-Sensitivities-and-Revaluation.md.

Numbers in the round-off regime of finite differences depend on the last bits of libm and are only asserted as
orders of magnitude; everything else is asserted at the quoted rounding.  The AAD section uses a minimal tape-based
reverse-mode implementation and compares operation counts, which are deterministic, not wall-clock times.

Run: python 11-Risk-and-Trading/code/sensitivities.py
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np

SQRT2 = math.sqrt(2.0)
EPS = 2.0**-52


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.6f}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def npdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs_call(s: float, k: float, r: float, vol: float, t: float) -> float:
    sq = vol * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / sq
    return s * ncdf(d1) - k * math.exp(-r * t) * ncdf(d1 - sq)


def bs_call_greeks(s: float, k: float, r: float, vol: float, t: float) -> dict[str, float]:
    sq = vol * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / sq
    gamma = npdf(d1) / (s * sq)
    return {
        "price": bs_call(s, k, r, vol, t),
        "delta": ncdf(d1),
        "gamma": gamma,
        "speed": -gamma / s * (1.0 + d1 / sq),  # d gamma / dS = V'''
        "vega": s * npdf(d1) * math.sqrt(t),
        "rho": k * t * math.exp(-r * t) * ncdf(d1 - sq),
    }


# ---------------------------------------------------------------------------
# Finite-difference error against bump size
# ---------------------------------------------------------------------------


def section_bump_error() -> None:
    print("\n[Worked example 1: finite-difference error against bump size, 1y ATM call, S = 100, r = 5%, vol = 20%]")
    s, k, r, vol, t = 100.0, 100.0, 0.05, 0.20, 1.0
    g = bs_call_greeks(s, k, r, vol, t)

    def v(x: float) -> float:
        return bs_call(x, k, r, vol, t)

    # V'''' from central differences of the analytic speed (smooth, so a moderate step is accurate).
    v4 = (bs_call_greeks(s + 1e-3, k, r, vol, t)["speed"] - bs_call_greeks(s - 1e-3, k, r, vol, t)["speed"]) / 2e-3
    check("V = call price", g["price"], 10.4506, 5e-5)
    check("delta", g["delta"], 0.636831, 5e-7)
    check("gamma", g["gamma"], 0.018762, 5e-7)
    check("V''' (speed)", g["speed"], -0.000516, 5e-7)
    check("V'''' (x 1e5)", v4 * 1e5, -2.76, 5e-3)
    h_fwd = math.sqrt(2.0 * EPS * g["price"] / g["gamma"])
    h_ctr = (3.0 * EPS * g["price"] / abs(g["speed"])) ** (1.0 / 3.0)
    h_gam = (48.0 * EPS * g["price"] / abs(v4)) ** 0.25
    check("optimal forward-difference bump sqrt(2 eps V / |V''|) (x 1e7)", h_fwd * 1e7, 4.97, 5e-3)
    check("optimal central-difference bump (3 eps V / |V'''|)^(1/3) (x 1e4)", h_ctr * 1e4, 2.38, 5e-3)
    check("optimal second-difference bump (48 eps V / |V''''|)^(1/4) (x 1e3)", h_gam * 1e3, 7.97, 5e-3)
    check("eps^(1/3) x S, the rule of thumb", EPS ** (1 / 3) * s, 0.000606, 5e-7)
    check("eps^(1/4) x S", EPS**0.25 * s, 0.0122, 5e-5)
    print("  h          fwd delta err   ctr delta err   gamma err")
    errs = {}
    for e in range(-10, 1):
        h = 10.0**e
        fwd = (v(s + h) - v(s)) / h - g["delta"]
        ctr = (v(s + h) - v(s - h)) / (2 * h) - g["delta"]
        gam = (v(s + h) - 2 * v(s) + v(s - h)) / h**2 - g["gamma"]
        errs[e] = (abs(fwd), abs(ctr), abs(gam))
        print(f"  1e{e:<3}     {abs(fwd):.2e}        {abs(ctr):.2e}        {abs(gam):.2e}")
    # Truncation regime: platform independent, asserted at the quoted rounding.
    check("forward error at h = 1 (x 1e3)", errs[0][0] * 1e3, 9.29, 5e-3)
    check("central error at h = 1 (x 1e5)", errs[0][1] * 1e5, 8.60, 5e-3)
    check("central error at h = 0.1 (x 1e7)", errs[-1][1] * 1e7, 8.60, 5e-3)
    check("gamma error at h = 1 (x 1e6)", errs[0][2] * 1e6, 2.30, 5e-3)
    check("theory h^2 |V'''| / 6 at h = 1 (x 1e5)", abs(g["speed"]) / 6.0 * 1e5, 8.60, 5e-3)
    # Round-off regime: orders of magnitude only (these digits depend on libm).
    assert 1e-8 < errs[-10][1] < 1e-4, "central delta at h = 1e-10 should be wrecked by round-off"
    assert errs[-10][2] > 1.0, "gamma with h = 1e-10 must be destroyed by round-off (eps V / h^2 ~ 1e5)"
    best_ctr = min(range(-10, 1), key=lambda e: errs[e][1])
    best_gam = min(range(-10, 1), key=lambda e: errs[e][2])
    print(f"  best decade: central delta 1e{best_ctr}, gamma 1e{best_gam}")
    assert best_ctr in (-5, -4, -3) and best_gam in (-3, -2)


# ---------------------------------------------------------------------------
# Full revaluation against Taylor proxies
# ---------------------------------------------------------------------------


def section_proxy() -> None:
    print("\n[Worked example 2: full revaluation against delta-gamma (with cross-gamma) on 2,000 scenarios, seed 123]")
    k, t = 100.0, 1.0
    base = np.array([100.0, 0.05, 0.20])

    def price(x: np.ndarray) -> float:
        return bs_call(x[0], k, x[1], x[2], t)

    hs = np.array([0.01, 1e-4, 1e-4])
    grad = np.zeros(3)
    hess = np.zeros((3, 3))
    v0 = price(base)
    for i in range(3):
        e = np.zeros(3)
        e[i] = hs[i]
        grad[i] = (price(base + e) - price(base - e)) / (2 * hs[i])
        hess[i, i] = (price(base + e) - 2 * v0 + price(base - e)) / hs[i] ** 2
        for j in range(i + 1, 3):
            f = np.zeros(3)
            f[j] = hs[j]
            hess[i, j] = hess[j, i] = (price(base + e + f) - price(base + e - f) - price(base - e + f) + price(base - e - f)) / (
                4 * hs[i] * hs[j]
            )
    sd = np.array([5.0, 0.0025, 0.02])
    corr = np.array([[1.0, 0.2, -0.5], [0.2, 1.0, 0.0], [-0.5, 0.0, 1.0]])
    cov = corr * np.outer(sd, sd)
    dx = np.random.default_rng(123).standard_normal((2000, 3)) @ np.linalg.cholesky(cov).T
    full = np.array([price(base + d) - v0 for d in dx])
    proxy = dx @ grad + 0.5 * np.einsum("ni,ij,nj->n", dx, hess, dx)
    delta_only = dx @ grad
    err = np.abs(full - proxy)

    def var_es(pnl: np.ndarray) -> tuple[float, float]:
        losses = np.sort(-pnl)[::-1]
        k_tail = math.ceil(0.01 * len(pnl))
        return float(losses[k_tail - 1]), float(losses[:k_tail].mean())

    fv, fe = var_es(full)
    pv, pe = var_es(proxy)
    dv, de = var_es(delta_only)
    print(f"  V0 {v0:.4f}; delta {grad[0]:.4f}, gamma {hess[0, 0]:.5f}, vega {grad[2]:.3f}, rho {grad[1]:.3f}")
    print(f"  MAE {err.mean():.4f}, RMSE {math.sqrt(float(np.mean(err**2))):.4f}, max {err.max():.4f}")
    print(f"  99% VaR / ES: full {fv:.3f} / {fe:.3f}, delta-gamma {pv:.3f} / {pe:.3f}, delta only {dv:.3f} / {de:.3f}")
    check("V0", v0, 10.4506, 5e-5)
    check("bumped delta", grad[0], 0.6368, 5e-5)
    check("bumped gamma", hess[0, 0], 0.01876, 5e-6)
    check("bumped vega", grad[2], 37.524, 5e-4)
    check("bumped vanna (cross-gamma S, vol)", hess[0, 2], -0.2814, 5e-4)
    check("MAE", float(err.mean()), 0.0186, 5e-5)
    check("RMSE", math.sqrt(float(np.mean(err**2))), 0.0412, 5e-5)
    check("max abs error", float(err.max()), 0.4582, 5e-5)
    check("99% VaR, full", fv, 5.484, 5e-4)
    check("99% VaR, delta-gamma", pv, 5.510, 5e-4)
    check("99% VaR, delta only", dv, 6.834, 5e-4)
    check("99% ES, full", fe, 6.313, 5e-4)
    check("99% ES, delta-gamma", pe, 6.369, 5e-4)
    check("99% ES, delta only", de, 8.108, 5e-4)
    check("vertex of the spot parabola, -delta / gamma", -grad[0] / hess[0, 0], -33.94, 5e-3)
    print("  crash grid: spot moves with vol +10 points, full against delta-gamma:")
    rows = {}
    for move in (-10.0, -30.0, -50.0, -70.0):
        d = np.array([move, 0.0, 0.10])
        f = price(base + d) - v0
        p = float(d @ grad + 0.5 * d @ hess @ d)
        rows[move] = (f, p)
        print(f"  dS = {move:+.0f}: full {f:+.3f}, proxy {p:+.3f}")
    check("full, dS = -50", rows[-50.0][0], -10.333, 5e-4)
    check("proxy, dS = -50", rows[-50.0][1], -3.180, 5e-4)
    check("full, dS = -70", rows[-70.0][0], -10.450, 5e-4)
    check("proxy, dS = -70", rows[-70.0][1], 7.160, 5e-4)


# ---------------------------------------------------------------------------
# Barrier: where a Taylor proxy cannot work
# ---------------------------------------------------------------------------


def down_and_out_call(s: float, k: float, h: float, r: float, vol: float, t: float) -> float:
    """Continuously monitored down-and-out call, barrier h <= strike k, no rebate (Reiner-Rubinstein form)."""
    if s <= h:
        return 0.0
    lam = (r + 0.5 * vol * vol) / (vol * vol)
    sq = vol * math.sqrt(t)
    y = math.log(h * h / (s * k)) / sq + lam * sq
    down_in = s * (h / s) ** (2 * lam) * ncdf(y) - k * math.exp(-r * t) * (h / s) ** (2 * lam - 2) * ncdf(y - sq)
    return bs_call(s, k, r, vol, t) - down_in


def section_barrier() -> None:
    print("\n[Core concepts: Taylor proxy across a barrier, down-and-out call K = 100, H = 95, r = 5%, vol 20%, T = 1]")
    k, h, r, vol, t = 100.0, 95.0, 0.05, 0.20, 1.0
    assert abs(down_and_out_call(95.0 + 1e-9, k, h, r, vol, t)) < 1e-6, "value must vanish at the barrier"
    assert abs(down_and_out_call(100.0, k, 1e-6, r, vol, t) - bs_call(100.0, k, r, vol, t)) < 1e-9
    s0 = 98.0
    v0 = down_and_out_call(s0, k, h, r, vol, t)
    d = (down_and_out_call(s0 + 0.01, k, h, r, vol, t) - down_and_out_call(s0 - 0.01, k, h, r, vol, t)) / 0.02
    gm = (down_and_out_call(s0 + 0.01, k, h, r, vol, t) - 2 * v0 + down_and_out_call(s0 - 0.01, k, h, r, vol, t)) / 1e-4
    print(f"  S0 = 98: value {v0:.4f}, delta {d:.4f}, gamma {gm:.5f}")
    check("value at S0 = 98", v0, 3.4522, 5e-5)
    check("delta", d, 1.1128, 5e-4)
    check("gamma", gm, -0.0225, 5e-4)
    for move in (-2.0, -4.0):
        full = down_and_out_call(s0 + move, k, h, r, vol, t) - v0
        prox = d * move + 0.5 * gm * move * move
        print(f"  dS = {move:+.0f}: full {full:+.4f}, delta-gamma {prox:+.4f}")
    check("full P&L through the barrier (dS = -4)", down_and_out_call(94.0, k, h, r, vol, t) - v0, -3.4522, 5e-5)
    check("delta-gamma P&L, dS = -4", d * -4.0 + 0.5 * gm * 16.0, -4.6312, 5e-4)
    check("full P&L, dS = -2", down_and_out_call(96.0, k, h, r, vol, t) - v0, -2.2743, 5e-5)
    check("delta-gamma P&L, dS = -2", d * -2.0 + 0.5 * gm * 4.0, -2.2706, 5e-4)


# ---------------------------------------------------------------------------
# Chebyshev interpolation of the pricer
# ---------------------------------------------------------------------------


def chebyshev_fit(f: Callable[[float], float], a: float, b: float, n: int) -> np.ndarray:
    """Coefficients of the degree n-1 interpolant at the n Chebyshev points of the first kind."""
    j = np.arange(n)
    x = np.cos(math.pi * (j + 0.5) / n)
    fx = np.array([f(0.5 * (b - a) * xi + 0.5 * (b + a)) for xi in x])
    c = np.array([2.0 / n * np.sum(fx * np.cos(math.pi * m * (j + 0.5) / n)) for m in range(n)])
    c[0] /= 2.0
    return c


def chebyshev_eval(c: np.ndarray, a: float, b: float, s: np.ndarray) -> np.ndarray:
    return np.polynomial.chebyshev.chebval((2.0 * s - a - b) / (b - a), c)


def section_chebyshev() -> None:
    print("\n[Core concepts: Chebyshev proxy of the 1y ATM call on spot in [50, 150]]")
    k, r, vol, t = 100.0, 0.05, 0.20, 1.0
    grid = np.linspace(50.0, 150.0, 2001)
    exact = np.array([bs_call(x, k, r, vol, t) for x in grid])
    out = {}
    for n in (8, 12, 16, 24, 32):
        c = chebyshev_fit(lambda x: bs_call(x, k, r, vol, t), 50.0, 150.0, n)
        out[n] = float(np.max(np.abs(chebyshev_eval(c, 50.0, 150.0, grid) - exact)))
        print(f"  {n} nodes: max error {out[n]:.2e}")
    g = bs_call_greeks(100.0, k, r, vol, t)
    taylor = g["price"] + g["delta"] * (grid - 100.0) + 0.5 * g["gamma"] * (grid - 100.0) ** 2
    tay_err = float(np.max(np.abs(taylor - exact)))
    print(f"  delta-gamma Taylor around 100: max error {tay_err:.3f}")
    check("max error, 8 nodes (x 1e2)", out[8] * 1e2, 1.30, 5e-3)
    check("max error, 16 nodes (x 1e6)", out[16] * 1e6, 3.34, 5e-3)
    check("max error, 12 nodes (x 1e4)", out[12] * 1e4, 4.54, 5e-3)
    check("max error, 24 nodes (x 1e10)", out[24] * 1e10, 6.73, 0.02)
    assert out[32] < 1e-12, "32 nodes should reach the round-off floor"
    check("max error, delta-gamma Taylor", tay_err, 10.774, 5e-4)


# ---------------------------------------------------------------------------
# AAD against bumping
# ---------------------------------------------------------------------------


class Tape:
    """Minimal reverse-mode AD: each node stores (parent indices, local partial derivatives)."""

    def __init__(self) -> None:
        self.parents: list[tuple[int, ...]] = []
        self.partials: list[tuple[float, ...]] = []
        self.values: list[float] = []

    def var(self, value: float) -> Node:
        return self._push(value, (), ())

    def _push(self, value: float, parents: tuple[int, ...], partials: tuple[float, ...]) -> Node:
        self.values.append(value)
        self.parents.append(parents)
        self.partials.append(partials)
        return Node(self, len(self.values) - 1)

    def gradient(self, out: Node, wrt: list[Node]) -> tuple[list[float], int]:
        """Backward sweep; returns d out / d wrt and the number of adjoint updates performed."""
        adj = [0.0] * len(self.values)
        adj[out.i] = 1.0
        updates = 0
        for i in range(out.i, -1, -1):
            if adj[i] == 0.0:
                continue
            for p, d in zip(self.parents[i], self.partials[i], strict=True):
                adj[p] += adj[i] * d
                updates += 1
        return [adj[w.i] for w in wrt], updates


class Node:
    def __init__(self, tape: Tape, i: int) -> None:
        self.tape, self.i = tape, i

    @property
    def v(self) -> float:
        return self.tape.values[self.i]

    def __add__(self, o: Node | float) -> Node:
        if isinstance(o, Node):
            return self.tape._push(self.v + o.v, (self.i, o.i), (1.0, 1.0))
        return self.tape._push(self.v + o, (self.i,), (1.0,))

    __radd__ = __add__

    def __mul__(self, o: Node | float) -> Node:
        if isinstance(o, Node):
            return self.tape._push(self.v * o.v, (self.i, o.i), (o.v, self.v))
        return self.tape._push(self.v * o, (self.i,), (o,))

    __rmul__ = __mul__

    def exp(self) -> Node:
        e = math.exp(self.v)
        return self.tape._push(e, (self.i,), (e,))


def bond_book_value(rates: list, tenors: np.ndarray, n_bonds: int, exp_fn: Callable) -> object:
    """Value of n_bonds annual-coupon bonds (maturities 1..30y cycling, coupon 4%) on a zero curve with linear interpolation.

    `rates` holds plain floats (for bumping) or tape Nodes (for AAD); `exp_fn` is the matching exponential.
    """
    total = 0.0
    for b in range(n_bonds):
        maturity = 1 + b % 30
        for year in range(1, maturity + 1):
            j = int(np.searchsorted(tenors, year))
            if j == 0:
                z = rates[0]
            elif j >= len(tenors):
                z = rates[-1]
            else:
                w = (year - tenors[j - 1]) / (tenors[j] - tenors[j - 1])
                z = rates[j - 1] * (1.0 - w) + rates[j] * w
            cf = 4.0 + (100.0 if year == maturity else 0.0)
            total = total + cf * exp_fn(z * (-float(year)))
    return total


def section_aad() -> None:
    print("\n[Core concepts: AAD against bumping on a bond book priced off an N-node zero curve]")
    rows = {}
    for n_nodes in (10, 30):
        tenors = np.linspace(1.0, 30.0, n_nodes)
        base = [0.03 + 0.0005 * i for i in range(n_nodes)]
        tape = Tape()
        xs = [tape.var(r) for r in base]
        value = bond_book_value(xs, tenors, 60, lambda z: z.exp())
        forward_nodes = len(tape.values)
        grad, updates = tape.gradient(value, xs)
        bumps = []
        for i in range(n_nodes):
            up = base.copy()
            dn = base.copy()
            up[i] += 1e-6
            dn[i] -= 1e-6
            bumps.append((bond_book_value(up, tenors, 60, math.exp) - bond_book_value(dn, tenors, 60, math.exp)) / 2e-6)
        max_diff = max(abs(a - b) for a, b in zip(grad, bumps, strict=True))
        rows[n_nodes] = (forward_nodes, updates, max_diff, value.v)
        print(f"  N = {n_nodes}: tape {forward_nodes} nodes, backward sweep {updates} adjoint updates, "
              f"bumping needs {2 * n_nodes} extra pricings; max |AAD - bump| {max_diff:.2e}")  # fmt: skip
    check("book value", rows[10][3], 6_471.88, 0.01)
    assert rows[10][2] < 1e-3 and rows[30][2] < 1e-3, "AAD and central bumps must agree"
    check("tape nodes, N = 10", rows[10][0], 6_340, 0)
    check("tape nodes, N = 30", rows[30][0], 6_360, 0)
    check("backward adjoint updates, N = 10", rows[10][1], 8_129, 0)
    check("backward adjoint updates, N = 30", rows[30][1], 8_129, 0)
    check("AAD work / one pricing, (tape + updates) / tape, N = 30", (rows[30][0] + rows[30][1]) / rows[30][0], 2.28, 5e-3)
    check("bumping work / one pricing, 2N, N = 30", 2 * 30, 60, 0)
    print("\n[Core concepts: bump counts]")
    n = 200
    check("central-difference gradient, 2N pricings, N = 200", 2 * n, 400, 0)
    check("full Hessian, 2N + 4 N(N-1)/2 = 2N^2 pricings", 2 * n + 4 * n * (n - 1) // 2, 80_000, 0)


def main() -> None:
    section_bump_error()
    section_proxy()
    section_barrier()
    section_chebyshev()
    section_aad()
    print("\nAll sensitivity checks passed.")


if __name__ == "__main__":
    main()
