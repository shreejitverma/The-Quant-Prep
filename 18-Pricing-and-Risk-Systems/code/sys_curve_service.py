"""Curve and surface service: bootstrap, calibration Jacobians, quote sensitivities, interpolation and the curve DAG.

Backs every number in `18-Pricing-and-Risk-Systems/04-Curve-and-Surface-Service.md`.

1. A three-pillar bootstrap (one zero-rate quote, two annual par swap quotes), its calibration Jacobian
   J = dF/dD, and market-quote sensitivities by solving J^T g_q = g_D, checked against bump-and-rebootstrap.
2. Natural cubic spline on zero rates versus flat forwards (linear in log discount factor): instantaneous forwards and
   locality of a pillar bump, on a hypothetical curve with an inverted short end.
3. A dirty-flag dependency DAG for a hypothetical multi-currency curve set: how many nodes a single quote invalidates,
   how many a lazy request recomputes, and cycle detection.
4. Calibration cost and memory for dense versus triangular Jacobians, from labelled-hypothetical pillar counts.

All quotes and curve sets are hypothetical teaching inputs.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_curve_service.py`.
"""

from __future__ import annotations

import math
from collections import deque

import numpy as np

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:.{decimals}f}")
    return value


# ============================================================================
# 1. Bootstrap, Jacobian and quote sensitivities
# ============================================================================


def bootstrap(q: np.ndarray) -> np.ndarray:
    """q[0] = 1y continuously compounded zero rate; q[1], q[2] = 2y and 3y annual par swap rates. Returns D1, D2, D3."""
    d1 = math.exp(-q[0] * 1.0)
    d2 = (1.0 - q[1] * d1) / (1.0 + q[1])
    d3 = (1.0 - q[2] * (d1 + d2)) / (1.0 + q[2])
    return np.array([d1, d2, d3])


def model_quotes(d: np.ndarray) -> np.ndarray:
    """F(D): the quotes implied by discount factors (the calibration targets)."""
    return np.array([-math.log(d[0]) / 1.0, (1 - d[1]) / (d[0] + d[1]), (1 - d[2]) / (d[0] + d[1] + d[2])])


def jacobian(d: np.ndarray) -> np.ndarray:
    """Analytic J_ij = dF_i/dD_j."""
    a2, a3 = d[0] + d[1], d[0] + d[1] + d[2]
    q2, q3 = (1 - d[1]) / a2, (1 - d[2]) / a3
    return np.array(
        [
            [-1.0 / d[0], 0.0, 0.0],
            [-q2 / a2, -(1 + q2) / a2, 0.0],
            [-q3 / a3, -q3 / a3, -(1 + q3) / a3],
        ]
    )


def zero_coupon_pv(d: np.ndarray, notional: float, t: float = 2.5) -> float:
    """PV of a zero-coupon payment at t between pillars 2 and 3, log-linear in discount factor."""
    w = (t - 2.0) / 1.0
    return notional * math.exp((1 - w) * math.log(d[1]) + w * math.log(d[2]))


def zero_coupon_grad(d: np.ndarray, notional: float, t: float = 2.5) -> np.ndarray:
    w = (t - 2.0) / 1.0
    v = zero_coupon_pv(d, notional, t)
    return np.array([0.0, v * (1 - w) / d[1], v * w / d[2]])


def receiver_swap_pv(d: np.ndarray, notional: float, k: float) -> float:
    """3y annual receiver swap: receive fixed k, pay floating (floating leg = 1 - D3 per unit notional)."""
    return notional * (k * d.sum() - (1 - d[2]))


def receiver_swap_grad(notional: float, k: float) -> np.ndarray:
    return notional * np.array([k, k, k + 1.0])


def quote_sensitivity(grad_d: np.ndarray, j: np.ndarray) -> np.ndarray:
    """dV/dq = (dD/dq)^T dV/dD with dD/dq = J^{-1}; solve J^T x = dV/dD (triangular, so forward/back substitution)."""
    return np.linalg.solve(j.T, grad_d)


def bump_sensitivity(pv, q: np.ndarray, h: float = 1e-6) -> np.ndarray:
    """Central differences of PV to each quote, re-bootstrapping the curve for every bump."""
    out = np.zeros(len(q))
    for k in range(len(q)):
        up, dn = q.copy(), q.copy()
        up[k] += h
        dn[k] -= h
        out[k] = (pv(bootstrap(up)) - pv(bootstrap(dn))) / (2 * h)
    return out


# ============================================================================
# 2. Interpolation: natural cubic spline on zero rates versus flat forwards
# ============================================================================


class NaturalSpline:
    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        n = len(x)
        h = np.diff(x)
        a = np.zeros((n, n))
        b = np.zeros(n)
        a[0, 0] = a[-1, -1] = 1.0
        for i in range(1, n - 1):
            a[i, i - 1], a[i, i], a[i, i + 1] = h[i - 1], 2 * (h[i - 1] + h[i]), h[i]
            b[i] = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])
        self.x, self.y, self.h = x, y, h
        self.c = np.linalg.solve(a, b)

    def _seg(self, t: float) -> tuple[int, float, float, float]:
        i = int(min(max(np.searchsorted(self.x, t) - 1, 0), len(self.x) - 2))
        h, c = self.h[i], self.c
        bb = (self.y[i + 1] - self.y[i]) / h - h * (2 * c[i] + c[i + 1]) / 3
        dd = (c[i + 1] - c[i]) / (3 * h)
        return i, bb, dd, t - self.x[i]

    def value(self, t: float) -> float:
        i, bb, dd, dx = self._seg(t)
        return self.y[i] + bb * dx + self.c[i] * dx**2 + dd * dx**3

    def deriv(self, t: float) -> float:
        i, bb, dd, dx = self._seg(t)
        return bb + 2 * self.c[i] * dx + 3 * dd * dx**2


def spline_forward(s: NaturalSpline, t: float) -> float:
    """Instantaneous forward f(t) = d(t z(t))/dt = z(t) + t z'(t)."""
    return s.value(t) + t * s.deriv(t)


def flat_forward_zero(x: np.ndarray, y: np.ndarray, t: float) -> float:
    """Zero rate under linear interpolation of log discount factors (piecewise flat forwards)."""
    lx = -y * x
    return -float(np.interp(t, x, lx)) / t


# ============================================================================
# 3. Dirty-flag curve DAG
# ============================================================================


class CurveGraph:
    """Nodes with parents; a quote update marks all descendants dirty; a request recomputes only dirty ancestors."""

    def __init__(self) -> None:
        self.parents: dict[str, list[str]] = {}
        self.children: dict[str, list[str]] = {}
        self.dirty: set[str] = set()
        self.recomputed: list[str] = []

    def add(self, node: str, parents: list[str]) -> None:
        self.parents[node] = list(parents)
        self.children.setdefault(node, [])
        for p in parents:
            self.children.setdefault(p, []).append(node)

    def invalidate(self, node: str) -> int:
        """Mark descendants of an updated input dirty; return how many nodes were newly marked (O(V + E))."""
        marked = 0
        stack = list(self.children[node])
        while stack:
            n = stack.pop()
            if n in self.dirty:
                continue
            self.dirty.add(n)
            marked += 1
            stack.extend(self.children[n])
        return marked

    def get(self, node: str) -> None:
        """Lazily recompute a node: first its dirty parents, then itself."""
        for p in self.parents[node]:
            if p in self.dirty:
                self.get(p)
        if node in self.dirty:
            self.dirty.discard(node)
            self.recomputed.append(node)

    def topological_order(self) -> list[str]:
        """Kahn's algorithm; raises if the graph has a cycle (for example circular proxy curves)."""
        indeg = {n: len(p) for n, p in self.parents.items()}
        for n in self.children:
            indeg.setdefault(n, 0)
        queue = deque(sorted(n for n, k in indeg.items() if k == 0))
        order = []
        while queue:
            n = queue.popleft()
            order.append(n)
            for c in self.children.get(n, []):
                indeg[c] -= 1
                if indeg[c] == 0:
                    queue.append(c)
        if len(order) != len(indeg):
            raise ValueError("dependency cycle")
        return order


def build_curve_set(ccys: list[str], tenors_per_ccy: int, ois_quotes: int, fwd_quotes: int, basis_quotes: int) -> CurveGraph:
    """Hypothetical USD-centred curve set.

    Per currency: an OIS curve on its own quotes; `tenors_per_ccy` forward curves on their quotes and the OIS curve;
    for non-USD currencies a cross-currency discount curve (domestic cashflows collateralised in USD) on basis quotes,
    the USD OIS curve and the domestic OIS curve; and one swaption surface per currency on its first forward curve
    and its OIS curve.
    """
    g = CurveGraph()
    for c in ccys:
        for k in range(ois_quotes):
            g.add(f"{c}.q.ois.{k}", [])
        g.add(f"{c}.OIS", [f"{c}.q.ois.{k}" for k in range(ois_quotes)])
        for t in range(tenors_per_ccy):
            qs = [f"{c}.q.fwd{t}.{k}" for k in range(fwd_quotes)]
            for qn in qs:
                g.add(qn, [])
            g.add(f"{c}.FWD{t}", [*qs, f"{c}.OIS"])
        g.add(f"{c}.VOL", [f"{c}.FWD0", f"{c}.OIS"])
    for c in ccys:
        if c == "USD":
            continue
        qs = [f"{c}.q.xccy.{k}" for k in range(basis_quotes)]
        for qn in qs:
            g.add(qn, [])
        g.add(f"{c}.XCCY", [*qs, "USD.OIS", f"{c}.OIS"])
    return g


def run_tests() -> None:
    print("Curve and surface service checks")

    print("  Example 1: three-pillar bootstrap")
    q = np.array([0.04, 0.045, 0.05])
    d = bootstrap(q)
    quoted("D1", d[0], 0.960789, 6)
    quoted("D2", d[1], 0.915564, 6)
    quoted("D3", d[2], 0.863031, 6)
    quoted("2y zero rate (%)", -math.log(d[1]) / 2 * 100, 4.4107, 4)
    quoted("3y zero rate (%)", -math.log(d[2]) / 3 * 100, 4.9102, 4)
    assert np.allclose(model_quotes(d), q, atol=1e-15)
    j = jacobian(d)
    quoted("J11 = -1/D1", j[0, 0], -1.040811, 6)
    quoted("J21 = -q2/(D1 + D2)", j[1, 0], -0.023983, 6)
    quoted("J22 = -(1 + q2)/(D1 + D2)", j[1, 1], -0.556931, 6)
    quoted("J31 = J32 = -q3/(D1 + D2 + D3)", j[2, 0], -0.018252, 6)
    quoted("J33 = -(1 + q3)/(D1 + D2 + D3)", j[2, 2], -0.383298, 6)
    quoted("D1 + D2", d[0] + d[1], 1.876354, 6)
    quoted("D1 + D2 + D3", d.sum(), 2.739384, 6)
    # The analytic Jacobian matches finite differences of F.
    fd = np.zeros((3, 3))
    for k in range(3):
        e = np.zeros(3)
        e[k] = 1e-7
        fd[:, k] = (model_quotes(d + e) - model_quotes(d - e)) / 2e-7
    assert np.allclose(fd, j, atol=1e-7)
    assert np.allclose(np.triu(j, 1), 0.0) and np.all(np.diag(j) != 0)  # lower triangular, non-zero diagonal

    print("  Example 2: market-quote sensitivities through the Jacobian (per 1 bp, notional 100m)")
    n = 100e6
    zc = lambda dd: zero_coupon_pv(dd, n)  # noqa: E731
    g_q = quote_sensitivity(zero_coupon_grad(d, n), j) * 1e-4
    g_fd = bump_sensitivity(zc, q) * 1e-4
    assert np.allclose(g_q, g_fd, rtol=1e-6, atol=1e-3)
    quoted("2.5y zero-coupon PV", zc(d), 88_890_944, 0)
    quoted("2.5y zero-coupon delta to the 1y quote (per bp)", g_q[0], 426, 0)
    quoted("2.5y zero-coupon delta to the 2y quote (per bp)", g_q[1], -8_276, 0)
    quoted("2.5y zero-coupon delta to the 3y quote (per bp)", g_q[2], -13_436, 0)
    quoted("sum of quote deltas (per bp)", g_q.sum(), -21_286, 0)
    at_market = lambda dd: receiver_swap_pv(dd, n, 0.05)  # noqa: E731
    s_at = quote_sensitivity(receiver_swap_grad(n, 0.05), j) * 1e-4
    assert np.allclose(s_at, bump_sensitivity(at_market, q) * 1e-4, rtol=1e-6, atol=1e-3)
    quoted("at-market 3y receiver PV", at_market(d), 0.0, 6)
    quoted("at-market 3y receiver delta to the 1y quote (per bp)", s_at[0], 0.0, 6)
    quoted("at-market 3y receiver delta to the 2y quote (per bp)", s_at[1], 0.0, 6)
    quoted("at-market 3y receiver delta to the 3y quote (per bp)", s_at[2], -27_394, 0)
    quoted("minus annuity times notional per bp", -d.sum() * n * 1e-4, -27_394, 0)
    off = lambda dd: receiver_swap_pv(dd, n, 0.06)  # noqa: E731
    s_off = quote_sensitivity(receiver_swap_grad(n, 0.06), j) * 1e-4
    assert np.allclose(s_off, bump_sensitivity(off, q) * 1e-4, rtol=1e-6, atol=1e-3)
    quoted("6% receiver PV", off(d), 2_739_384, 0)
    quoted("6% receiver delta to the 1y quote (per bp)", s_off[0], -88, 0)
    quoted("6% receiver delta to the 2y quote (per bp)", s_off[1], -171, 0)
    quoted("6% receiver delta to the 3y quote (per bp)", s_off[2], -27_655, 0)

    print("  Example 3: natural cubic spline on zero rates versus flat forwards (hypothetical curve)")
    x = np.array([0.5, 1, 2, 3, 5, 7, 10, 30.0])
    y = np.array([0.050, 0.045, 0.027, 0.024, 0.028, 0.030, 0.032, 0.033])
    disc = np.diff(y * x) / np.diff(x)
    quoted("lowest discrete forward between pillars (%)", disc.min() * 100, 0.9, 1)
    assert disc.min() > 0
    s = NaturalSpline(x, y)
    grid = np.linspace(0.5, 30.0, 59_001)
    fwd = np.array([spline_forward(s, t) for t in grid])
    quoted("lowest spline instantaneous forward (%)", fwd.min() * 100, -0.12, 2)
    quoted("maturity of the lowest spline forward (years)", grid[fwd.argmin()], 1.8, 1)
    quoted("highest spline instantaneous forward (%)", fwd.max() * 100, 4.61, 2)
    quoted("highest discrete forward (%)", disc.max() * 100, 4.0, 1)
    # Locality: bump the 2y zero rate by 1 bp and look at the 9y zero rate.
    yb = y.copy()
    yb[2] += 1e-4
    sb = NaturalSpline(x, yb)
    quoted("spline: change in 9y zero from a 1 bp 2y bump (bp)", (sb.value(9.0) - s.value(9.0)) * 1e4, -0.041, 3)
    quoted("spline: change in 1.5y zero (bp)", (sb.value(1.5) - s.value(1.5)) * 1e4, 0.6, 1)
    quoted("flat forwards: change in 9y zero (bp)", (flat_forward_zero(x, yb, 9.0) - flat_forward_zero(x, y, 9.0)) * 1e4, 0.0, 6)
    nonlocal_pillars = sum(abs(sb.value(t) - s.value(t)) > 1e-12 for t in np.linspace(3.0, 30.0, 271))
    quoted("spline: grid points from 3y to 30y moved by the 2y bump (of 271)", nonlocal_pillars, 266, 0)
    quoted("grid points that are pillars (3, 5, 7, 10, 30) and cannot move", sum(t in x for t in np.linspace(3.0, 30.0, 271)), 5, 0)

    print("  Example 4: dirty-flag DAG on a hypothetical 15-currency curve set")
    ccys = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "SEK", "NOK", "DKK", "HKD", "SGD", "CNH", "MXN"]
    g = build_curve_set(ccys, tenors_per_ccy=2, ois_quotes=20, fwd_quotes=20, basis_quotes=15)
    order = g.topological_order()
    derived = [k for k in g.parents if g.parents[k]]
    quoted("nodes in the graph", len(order), 1_184, 0)
    quoted("derived curves and surfaces", len(derived), 74, 0)
    marked = g.invalidate("USD.q.ois.12")
    quoted("nodes invalidated by one USD OIS quote", marked, 18, 0)
    g.get("EUR.XCCY")
    quoted("nodes recomputed to price a EUR trade collateralised in USD", len(g.recomputed), 2, 0)
    quoted("nodes still dirty after that request", len(g.dirty), 16, 0)
    g2 = build_curve_set(ccys, 2, 20, 20, 15)
    g2.invalidate("EUR.q.fwd1.3")
    quoted("nodes invalidated by one EUR forward-curve quote", len(g2.dirty), 1, 0)
    g3 = build_curve_set(["USD", "EUR"], 1, 2, 2, 2)
    g3.add("EUR.PROXY", ["EUR.FWD0"])
    g3.parents["EUR.FWD0"].append("EUR.PROXY")
    g3.children["EUR.PROXY"].append("EUR.FWD0")
    try:
        g3.topological_order()
        raise AssertionError("cycle not detected")
    except ValueError:
        pass

    print("  Example 5: calibration cost and memory (hypothetical pillar counts)")
    for pillars, flops, mb in ((60, 1.44e5, 0.0288), (600, 1.44e8, 2.88)):
        quoted(f"dense LU flops for {pillars} pillars (2N^3/3)", 2 * pillars**3 / 3, flops, 0)
        quoted(f"dense Jacobian memory for {pillars} pillars (MB, float64)", pillars**2 * 8 / 1e6, mb, 4 if pillars == 60 else 2)
    quoted("triangular solve flops for 600 pillars (N^2)", 600**2, 360_000, 0)
    quoted("dense over triangular cost at 600 pillars", (2 * 600**3 / 3) / 600**2, 400, 0)

    print(f"  {len(QUOTED)} numbers quoted in note 04 computed, printed and asserted")
    print("All curve and surface service checks passed.")


if __name__ == "__main__":
    run_tests()
