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

import bisect
import math
from collections import deque
from collections.abc import Callable

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


def bootstrap(q: list[float]) -> list[float]:
    """q[0] = 1y continuously compounded zero rate; q[1], q[2] = 2y and 3y annual par swap rates. Returns D1, D2, D3."""
    d1 = math.exp(-q[0] * 1.0)
    d2 = (1.0 - q[1] * d1) / (1.0 + q[1])
    d3 = (1.0 - q[2] * (d1 + d2)) / (1.0 + q[2])
    return [d1, d2, d3]


def model_quotes(d: list[float]) -> list[float]:
    """F(D): the quotes implied by discount factors (the calibration targets)."""
    return [-math.log(d[0]) / 1.0, (1 - d[1]) / (d[0] + d[1]), (1 - d[2]) / (d[0] + d[1] + d[2])]


def jacobian(d: list[float]) -> list[list[float]]:
    """Analytic J_ij = dF_i/dD_j."""
    a2, a3 = d[0] + d[1], d[0] + d[1] + d[2]
    q2, q3 = (1 - d[1]) / a2, (1 - d[2]) / a3
    return [
        [-1.0 / d[0], 0.0, 0.0],
        [-q2 / a2, -(1 + q2) / a2, 0.0],
        [-q3 / a3, -q3 / a3, -(1 + q3) / a3],
    ]


def zero_coupon_pv(d: list[float], notional: float, t: float = 2.5) -> float:
    """PV of a zero-coupon payment at t between pillars 2 and 3, log-linear in discount factor."""
    w = (t - 2.0) / 1.0
    return notional * math.exp((1 - w) * math.log(d[1]) + w * math.log(d[2]))


def zero_coupon_grad(d: list[float], notional: float, t: float = 2.5) -> list[float]:
    w = (t - 2.0) / 1.0
    v = zero_coupon_pv(d, notional, t)
    return [0.0, v * (1 - w) / d[1], v * w / d[2]]


def receiver_swap_pv(d: list[float], notional: float, k: float) -> float:
    """3y annual receiver swap: receive fixed k, pay floating (floating leg = 1 - D3 per unit notional)."""
    return notional * (k * sum(d) - (1 - d[2]))


def receiver_swap_grad(notional: float, k: float) -> list[float]:
    return [notional * k, notional * k, notional * (k + 1.0)]


def quote_sensitivity(grad_d: list[float], j: list[list[float]]) -> list[float]:
    """dV/dq = (dD/dq)^T dV/dD with dD/dq = J^{-1}; solve J^T x = dV/dD (upper triangular back substitution)."""
    # [ j[0][0]  j[1][0]  j[2][0] ] [x0]   [g0]
    # [    0     j[1][1]  j[2][1] ] [x1] = [g1]
    # [    0        0     j[2][2] ] [x2]   [g2]
    x2 = grad_d[2] / j[2][2]
    x1 = (grad_d[1] - j[2][1] * x2) / j[1][1]
    x0 = (grad_d[0] - j[1][0] * x1 - j[2][0] * x2) / j[0][0]
    return [x0, x1, x2]


def bump_sensitivity(pv: Callable[[list[float]], float], q: list[float], h: float = 1e-6) -> list[float]:
    """Central differences of PV to each quote, re-bootstrapping the curve for every bump."""
    out = []
    for k in range(len(q)):
        up, dn = list(q), list(q)
        up[k] += h
        dn[k] -= h
        out.append((pv(bootstrap(up)) - pv(bootstrap(dn))) / (2 * h))
    return out


# ============================================================================
# 2. Interpolation: natural cubic spline on zero rates versus flat forwards
# ============================================================================


class NaturalSpline:
    def __init__(self, x: list[float], y: list[float]) -> None:
        n = len(x)
        h = [x[i + 1] - x[i] for i in range(n - 1)]
        m = n - 2
        diag = [2.0 * (h[i - 1] + h[i]) for i in range(1, n - 1)]
        sub = [h[i] for i in range(1, n - 2)]
        sup = [h[i] for i in range(1, n - 2)]
        rhs = [3.0 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]) for i in range(1, n - 1)]

        if m == 0:
            c_interior = []
        elif m == 1:
            c_interior = [rhs[0] / diag[0]]
        else:
            cp = [0.0] * (m - 1)
            dp = [0.0] * m
            cp[0] = sup[0] / diag[0]
            dp[0] = rhs[0] / diag[0]
            for i in range(1, m - 1):
                denom = diag[i] - sub[i - 1] * cp[i - 1]
                cp[i] = sup[i] / denom
                dp[i] = (rhs[i] - sub[i - 1] * dp[i - 1]) / denom
            denom = diag[m - 1] - sub[m - 2] * cp[m - 2]
            dp[m - 1] = (rhs[m - 1] - sub[m - 2] * dp[m - 2]) / denom

            c_interior = [0.0] * m
            c_interior[m - 1] = dp[m - 1]
            for i in range(m - 2, -1, -1):
                c_interior[i] = dp[i] - cp[i] * c_interior[i + 1]

        self.x = x
        self.y = y
        self.h = h
        self.c = [0.0] + c_interior + [0.0]

    def _seg(self, t: float) -> tuple[int, float, float, float]:
        idx = bisect.bisect_right(self.x, t) - 1
        i = int(min(max(idx, 0), len(self.x) - 2))
        h, c = self.h[i], self.c
        bb = (self.y[i + 1] - self.y[i]) / h - h * (2 * c[i] + c[i + 1]) / 3.0
        dd = (c[i + 1] - c[i]) / (3.0 * h)
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


def flat_forward_zero(x: list[float], y: list[float], t: float) -> float:
    """Zero rate under linear interpolation of log discount factors (piecewise flat forwards)."""
    lx = [-y_i * x_i for x_i, y_i in zip(x, y, strict=True)]
    if t <= x[0]:
        val = lx[0]
    elif t >= x[-1]:
        val = lx[-1]
    else:
        i = bisect.bisect_right(x, t) - 1
        w = (t - x[i]) / (x[i + 1] - x[i])
        val = lx[i] + w * (lx[i + 1] - lx[i])
    return -val / t


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
    q = [0.04, 0.045, 0.05]
    d = bootstrap(q)
    quoted("D1", d[0], 0.960789, 6)
    quoted("D2", d[1], 0.915564, 6)
    quoted("D3", d[2], 0.863031, 6)
    quoted("2y zero rate (%)", -math.log(d[1]) / 2 * 100, 4.4107, 4)
    quoted("3y zero rate (%)", -math.log(d[2]) / 3 * 100, 4.9102, 4)
    mq = model_quotes(d)
    for q_calc, q_exp in zip(mq, q, strict=True):
        assert abs(q_calc - q_exp) < 1e-14
    j = jacobian(d)
    quoted("J11 = -1/D1", j[0][0], -1.040811, 6)
    quoted("J21 = -q2/(D1 + D2)", j[1][0], -0.023983, 6)
    quoted("J22 = -(1 + q2)/(D1 + D2)", j[1][1], -0.556931, 6)
    quoted("J31 = J32 = -q3/(D1 + D2 + D3)", j[2][0], -0.018252, 6)
    quoted("J33 = -(1 + q3)/(D1 + D2 + D3)", j[2][2], -0.383298, 6)
    quoted("D1 + D2", d[0] + d[1], 1.876354, 6)
    quoted("D1 + D2 + D3", sum(d), 2.739384, 6)

    # The analytic Jacobian matches finite differences of F.
    for r in range(3):
        for c in range(3):
            d_up, d_dn = list(d), list(d)
            d_up[c] += 1e-7
            d_dn[c] -= 1e-7
            fd_val = (model_quotes(d_up)[r] - model_quotes(d_dn)[r]) / 2e-7
            assert abs(fd_val - j[r][c]) < 1e-6
    # Lower triangular with a non-zero diagonal, so the bootstrap is a forward substitution.
    assert all(j[r][c] == 0.0 for r in range(3) for c in range(r + 1, 3))
    assert all(j[k][k] != 0.0 for k in range(3))

    print("  Example 2: market-quote sensitivities through the Jacobian (per 1 bp, notional 100m)")
    n = 100e6
    zc = lambda dd: zero_coupon_pv(dd, n)  # noqa: E731
    g_q = [x * 1e-4 for x in quote_sensitivity(zero_coupon_grad(d, n), j)]
    g_fd = [x * 1e-4 for x in bump_sensitivity(zc, q)]
    for a, b in zip(g_q, g_fd, strict=True):
        assert abs(a - b) < 1e-3
    quoted("2.5y zero-coupon PV", zc(d), 88_890_944, 0)
    quoted("2.5y zero-coupon delta to the 1y quote (per bp)", g_q[0], 426, 0)
    quoted("2.5y zero-coupon delta to the 2y quote (per bp)", g_q[1], -8_276, 0)
    quoted("2.5y zero-coupon delta to the 3y quote (per bp)", g_q[2], -13_436, 0)
    quoted("sum of quote deltas (per bp)", sum(g_q), -21_286, 0)

    at_market = lambda dd: receiver_swap_pv(dd, n, 0.05)  # noqa: E731
    s_at = [x * 1e-4 for x in quote_sensitivity(receiver_swap_grad(n, 0.05), j)]
    for a, b in zip(s_at, [x * 1e-4 for x in bump_sensitivity(at_market, q)], strict=True):
        assert abs(a - b) < 1e-3  # Jacobian solve versus bump-and-rebootstrap
    quoted("at-market 3y receiver PV", at_market(d), 0.0, 6)
    quoted("at-market 3y receiver delta to the 1y quote (per bp)", s_at[0], 0.0, 6)
    quoted("at-market 3y receiver delta to the 2y quote (per bp)", s_at[1], 0.0, 6)
    quoted("at-market 3y receiver delta to the 3y quote (per bp)", s_at[2], -27_394, 0)
    quoted("minus annuity times notional per bp", -sum(d) * n * 1e-4, -27_394, 0)

    off = lambda dd: receiver_swap_pv(dd, n, 0.06)  # noqa: E731
    s_off = [x * 1e-4 for x in quote_sensitivity(receiver_swap_grad(n, 0.06), j)]
    for a, b in zip(s_off, [x * 1e-4 for x in bump_sensitivity(off, q)], strict=True):
        assert abs(a - b) < 1e-3  # Jacobian solve versus bump-and-rebootstrap
    quoted("6% receiver PV", off(d), 2_739_384, 0)
    quoted("6% receiver delta to the 1y quote (per bp)", s_off[0], -88, 0)
    quoted("6% receiver delta to the 2y quote (per bp)", s_off[1], -171, 0)
    quoted("6% receiver delta to the 3y quote (per bp)", s_off[2], -27_655, 0)

    print("  Example 3: natural cubic spline on zero rates versus flat forwards (hypothetical curve)")
    x = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 30.0]
    y = [0.050, 0.045, 0.027, 0.024, 0.028, 0.030, 0.032, 0.033]
    yx = [y_i * x_i for x_i, y_i in zip(x, y, strict=True)]
    disc = [(yx[i + 1] - yx[i]) / (x[i + 1] - x[i]) for i in range(len(x) - 1)]
    quoted("lowest discrete forward between pillars (%)", min(disc) * 100, 0.9, 1)
    assert min(disc) > 0

    s = NaturalSpline(x, y)
    n_grid = 59_001
    grid = [0.5 + i * (30.0 - 0.5) / (n_grid - 1) for i in range(n_grid)]
    fwd = [spline_forward(s, t) for t in grid]
    min_fwd = min(fwd)
    min_idx = fwd.index(min_fwd)
    quoted("lowest spline instantaneous forward (%)", min_fwd * 100, -0.12, 2)
    quoted("maturity of the lowest spline forward (years)", grid[min_idx], 1.8, 1)
    assert min_fwd < min(disc)  # below every discrete forward between pillars
    assert disc.index(min(disc)) == 1  # the lowest discrete forward is on the 1y to 2y interval
    # On each interval the instantaneous forward averages to the discrete forward: integrate f = d(t z)/dt numerically.
    a_, b_ = 1.0, 2.0
    m = 2_000
    avg = sum(spline_forward(s, a_ + (k + 0.5) * (b_ - a_) / m) for k in range(m)) / m
    assert abs(avg - disc[1]) < 1e-6

    # Locality: bump the 2y zero rate by 1 bp and look at the 9y zero rate.
    yb = list(y)
    yb[2] += 1e-4
    sb = NaturalSpline(x, yb)
    quoted("spline: change in 9y zero from a 1 bp 2y bump (bp)", (sb.value(9.0) - s.value(9.0)) * 1e4, -0.041, 3)
    quoted("spline: change in 1.5y zero (bp)", (sb.value(1.5) - s.value(1.5)) * 1e4, 0.56, 2)
    quoted("flat forwards: change in 9y zero (bp)", (flat_forward_zero(x, yb, 9.0) - flat_forward_zero(x, y, 9.0)) * 1e4, 0.0, 6)

    test_grid = [3.0 + i * (30.0 - 3.0) / 270 for i in range(271)]
    nonlocal_pillars = sum(abs(sb.value(t) - s.value(t)) > 1e-12 for t in test_grid)
    quoted("spline: grid points from 3y to 30y moved by the 2y bump (of 271)", nonlocal_pillars, 266, 0)
    quoted("grid points that are pillars (3, 5, 7, 10, 30) and cannot move", sum(t in x for t in test_grid), 5, 0)
    # Minimal 3-point spline verification (m=1 case)
    s3 = NaturalSpline([0.0, 1.0, 2.0], [0.0, 1.0, 0.0])
    assert len(s3.c) == 3 and abs(s3.c[1] - (-1.5)) < 1e-14

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
