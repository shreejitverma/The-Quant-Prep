"""Curve construction numerics: forward shapes, Hagan-West monotone convex, locality, Jacobians, turns.

Backs every number in `06-Fixed-Income-and-Asset-Classes/14-Curve-Construction-Numerics.md`.
Independent checks: the analytic calibration Jacobian is compared with central finite differences of the
par-rate pricing functions; its inverse is compared with bump-and-rebootstrap sensitivities of zero
rates to par quotes; the par bond's par-quote risk is compared with a bump-and-rebootstrap revaluation;
the monotone convex interpolant is checked to reprice every pillar by numerical quadrature of its
forward curve; locality is measured by bumping one pillar and differencing the forward curves.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_curve_numerics.py`.
"""

from __future__ import annotations

import math
from collections.abc import Callable

QUOTED: list[str] = []
PAR = [0.030, 0.035, 0.040]
TIMES = [1.0, 2.0, 3.0]


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def bootstrap(par: list[float]) -> list[float]:
    """Annual par swaps with pillars at every coupon date: P_n = (1 - s_n sum_{i<n} P_i) / (1 + s_n)."""
    dfs: list[float] = []
    for s in par:
        dfs.append((1.0 - s * sum(dfs)) / (1.0 + s))
    return dfs


def par_rates_from_zeros(z: list[float]) -> list[float]:
    p = [math.exp(-t * zz) for t, zz in zip(TIMES, z, strict=True)]
    return [(1.0 - p[i]) / sum(p[: i + 1]) for i in range(len(p))]


def zeros_from_par(par: list[float]) -> list[float]:
    return [-math.log(p) / t for p, t in zip(bootstrap(par), TIMES, strict=True)]


def analytic_jacobian(par: list[float]) -> list[list[float]]:
    """J[i][j] = ds_i/dz_j for annual par swaps with continuous zero rates at the pillars."""
    p = bootstrap(par)
    n = len(p)
    jac = [[0.0] * n for _ in range(n)]
    for i in range(n):
        a_i = sum(p[: i + 1])
        for j in range(i + 1):
            ds_dp = -(1.0 + par[i]) / a_i if j == i else -par[i] / a_i
            jac[i][j] = ds_dp * (-TIMES[j] * p[j])
    return jac


def lower_triangular_inverse(m: list[list[float]]) -> list[list[float]]:
    n = len(m)
    inv = [[0.0] * n for _ in range(n)]
    for col in range(n):
        for row in range(n):
            rhs = 1.0 if row == col else 0.0
            acc = sum(m[row][k] * inv[k][col] for k in range(row))
            inv[row][col] = (rhs - acc) / m[row][row]
    return inv


# ---------------------------------------------------------------- Hagan-West monotone convex (no amelioration)


def monotone_convex(times: list[float], fd: list[float]) -> Callable[[float], float]:
    """Instantaneous forward f(t) from discrete forwards fd[i] on [times[i-1], times[i]], times[0] = 0.

    Hagan and West (2006): nodal values from equations (30) to (32), the quadratic of (34), and the
    four-sector monotonicity fix of equations (49) to (56).
    """
    n = len(fd)
    f = [0.0] * (n + 1)
    for i in range(1, n):
        lo, mid, hi = times[i - 1], times[i], times[i + 1]
        f[i] = (mid - lo) / (hi - lo) * fd[i] + (hi - mid) / (hi - lo) * fd[i - 1]
    f[0] = fd[0] - 0.5 * (f[1] - fd[0])
    f[n] = fd[n - 1] - 0.5 * (f[n - 1] - fd[n - 1])

    def g_of(g0: float, g1: float, x: float) -> float:
        if g0 == 0.0 and g1 == 0.0:
            return 0.0
        if (g0 > 0.0 and -0.5 * g0 >= g1 >= -2.0 * g0) or (g0 < 0.0 and -0.5 * g0 <= g1 <= -2.0 * g0):
            return g0 * (1.0 - 4.0 * x + 3.0 * x * x) + g1 * (-2.0 * x + 3.0 * x * x)
        if (g0 < 0.0 and g1 > -2.0 * g0) or (g0 > 0.0 and g1 < -2.0 * g0):
            eta = (g1 + 2.0 * g0) / (g1 - g0)
            return g0 if x <= eta else g0 + (g1 - g0) * ((x - eta) / (1.0 - eta)) ** 2
        if (g0 > 0.0 and 0.0 > g1 > -0.5 * g0) or (g0 < 0.0 and 0.0 < g1 < -0.5 * g0):
            eta = 3.0 * g1 / (g1 - g0)
            return g1 + (g0 - g1) * ((eta - x) / eta) ** 2 if x < eta else g1
        eta = g1 / (g1 + g0)
        a = -g0 * g1 / (g0 + g1)
        if x < eta:
            return a + (g0 - a) * ((eta - x) / eta) ** 2
        return a + (g1 - a) * ((x - eta) / (1.0 - eta)) ** 2

    def fwd(t: float) -> float:
        if t >= times[-1]:
            return f[n]
        i = 1
        while t > times[i]:
            i += 1
        x = (t - times[i - 1]) / (times[i] - times[i - 1])
        return fd[i - 1] + g_of(f[i - 1] - fd[i - 1], f[i] - fd[i - 1], x)

    return fwd


def simpson(fun: Callable[[float], float], a: float, b: float, n: int = 2000) -> float:
    h = (b - a) / n
    total = fun(a) + fun(b)
    for k in range(1, n):
        total += (4.0 if k % 2 else 2.0) * fun(a + k * h)
    return total * h / 3.0


def natural_cubic_spline(xs: list[float], ys: list[float]) -> tuple[Callable[[float], float], Callable[[float], float]]:
    """Natural cubic spline value and first derivative (tridiagonal solve for second derivatives)."""
    n = len(xs)
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    a = [0.0] * n
    b = [1.0] * n
    c = [0.0] * n
    d = [0.0] * n
    for i in range(1, n - 1):
        a[i], b[i], c[i] = h[i - 1], 2.0 * (h[i - 1] + h[i]), h[i]
        d[i] = 6.0 * ((ys[i + 1] - ys[i]) / h[i] - (ys[i] - ys[i - 1]) / h[i - 1])
    for i in range(1, n):
        w = a[i] / b[i - 1]
        b[i] -= w * c[i - 1]
        d[i] -= w * d[i - 1]
    m = [0.0] * n
    m[-1] = d[-1] / b[-1]
    for i in range(n - 2, -1, -1):
        m[i] = (d[i] - c[i] * m[i + 1]) / b[i]

    def seg(x: float) -> int:
        i = 0
        while i < n - 2 and x > xs[i + 1]:
            i += 1
        return i

    def value(x: float) -> float:
        i = seg(x)
        t0, t1 = xs[i + 1] - x, x - xs[i]
        return (
            m[i] * t0**3 / (6 * h[i])
            + m[i + 1] * t1**3 / (6 * h[i])
            + (ys[i] / h[i] - m[i] * h[i] / 6) * t0
            + (ys[i + 1] / h[i] - m[i + 1] * h[i] / 6) * t1
        )

    def deriv(x: float) -> float:
        i = seg(x)
        t0, t1 = xs[i + 1] - x, x - xs[i]
        return (
            -m[i] * t0**2 / (2 * h[i])
            + m[i + 1] * t1**2 / (2 * h[i])
            - (ys[i] / h[i] - m[i] * h[i] / 6)
            + (ys[i + 1] / h[i] - m[i + 1] * h[i] / 6)
        )

    return value, deriv


# ---------------------------------------------------------------- examples


def example_forward_shapes() -> None:
    print("  1. Log-linear discount factors: piecewise-constant forwards")
    p = bootstrap(PAR)
    for t, v, e in zip(TIMES, p, (0.970874, 0.933352, 0.888299), strict=True):
        quoted(f"P({t:.0f})", v, e, 6)
    fd = [-math.log(p[0]), -math.log(p[1] / p[0]), -math.log(p[2] / p[1])]
    quoted("forward on [0,1] (%)", fd[0] * 100, 2.9559, 4)
    quoted("forward on [1,2] (%)", fd[1] * 100, 3.9414, 4)
    quoted("forward on [2,3] (%)", fd[2] * 100, 4.9474, 4)
    quoted("jump at t=1 (bp)", (fd[1] - fd[0]) * 1e4, 98.55, 2)
    quoted("jump at t=2 (bp)", (fd[2] - fd[1]) * 1e4, 100.60, 2)
    z = [-math.log(pp) / t for pp, t in zip(p, TIMES, strict=True)]
    quoted("zero z(3) (%)", z[2] * 100, 3.9482, 4)
    # Linear interpolation on zero rates: f = z + t z' jumps by T_k times the slope change.
    slope_12, slope_23 = (z[1] - z[0]) / 1.0, (z[2] - z[1]) / 1.0
    quoted("linear-zero forward just before t=2 (%)", (z[1] + 2.0 * slope_12) * 100, 4.4342, 4)
    quoted("linear-zero forward just after t=2 (%)", (z[1] + 2.0 * slope_23) * 100, 4.4478, 4)
    quoted("linear-zero forward just after t=1 (%)", (z[0] + 1.0 * slope_12) * 100, 3.4486, 4)

    print("  2. Hagan-West monotone convex on the same curve")
    fwd = monotone_convex([0.0, *TIMES], fd)
    quoted("f(0) (%)", fwd(0.0) * 100, 2.7095, 4)
    quoted("f(1), continuous (%)", fwd(1.0) * 100, 3.4486, 4)
    quoted("f(2), continuous (%)", fwd(2.0) * 100, 4.4444, 4)
    quoted("f(3) (%)", fwd(3.0) * 100, 5.1989, 4)
    left, right = fwd(1.0 - 1e-9), fwd(1.0 + 1e-9)
    assert abs(left - right) < 1e-8
    for k, t in enumerate(TIMES):
        integral = simpson(fwd, 0.0, t)
        assert abs(math.exp(-integral) - p[k]) < 1e-12, (t, math.exp(-integral), p[k])
    minimum = min(fwd(k / 1000.0) for k in range(3001))
    quoted("minimum forward on [0,3] (%)", minimum * 100, 2.7095, 4)


def example_locality() -> None:
    print("  3. Locality: bump the 7y zero by 1 bp")
    ts = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    zs = [0.0300, 0.0340, 0.0370, 0.0400, 0.0415, 0.0430]

    def mc_forward(zz: list[float]) -> Callable[[float], float]:
        rt = [0.0] + [t * z for t, z in zip(ts, zz, strict=True)]
        grid = [0.0, *ts]
        fd = [(rt[i + 1] - rt[i]) / (grid[i + 1] - grid[i]) for i in range(len(ts))]
        return monotone_convex(grid, fd)

    def spline_forward(zz: list[float]) -> Callable[[float], float]:
        val, der = natural_cubic_spline(ts, zz)
        return lambda t: val(t) + t * der(t)

    bumped = list(zs)
    bumped[4] += 1e-4
    bumped_fwd = mc_forward(bumped)
    grid = [0.0, *ts]
    for k, z in enumerate(bumped):
        integral = sum(simpson(bumped_fwd, grid[i], grid[i + 1], 4000) for i in range(k + 1))
        assert abs(integral - ts[k] * z) < 1e-10, (ts[k], integral, ts[k] * z)

    for name, builder in (("monotone convex", mc_forward), ("cubic spline on zeros", spline_forward)):
        base, bump = builder(zs), builder(bumped)
        d15 = (bump(1.5) - base(1.5)) * 1e4
        d25 = (bump(2.5) - base(2.5)) * 1e4
        if name == "monotone convex":
            quoted("monotone convex: change in f(1.5) (bp)", d15, 0.0, 4)
            quoted("monotone convex: change in f(2.5) (bp)", d25, 0.0, 4)
            quoted("monotone convex: change in f(6) (bp)", (bump(6.0) - base(6.0)) * 1e4, 4.5217, 4)
        else:
            quoted("cubic spline: change in f(1.5) (bp)", d15, -0.0063, 4)
            quoted("cubic spline: change in f(2.5) (bp)", d25, 0.0357, 4)
            quoted("cubic spline: change in f(6) (bp)", (bump(6.0) - base(6.0)) * 1e4, 4.1067, 4)


def example_jacobian() -> None:
    print("  4. Calibration Jacobian ds/dz and its inverse")
    p = bootstrap(PAR)
    annuities = [sum(p[: i + 1]) for i in range(3)]
    for k, e in enumerate((0.970874, 1.904226, 2.792525)):
        quoted(f"A{k + 1}", annuities[k], e, 6)
    jac = analytic_jacobian(PAR)
    expected = {(0, 0): 1.030000, (1, 0): 0.017845, (1, 1): 1.014606, (2, 0): 0.013907, (2, 1): 0.026739, (2, 2): 0.992468}
    z0 = zeros_from_par(PAR)
    h = 1e-6
    for (i, j), e in expected.items():
        up, dn = list(z0), list(z0)
        up[j] += h
        dn[j] -= h
        fd = (par_rates_from_zeros(up)[i] - par_rates_from_zeros(dn)[i]) / (2 * h)
        assert abs(fd - jac[i][j]) < 1e-8, (i, j, fd, jac[i][j])
        quoted(f"J[{i + 1},{j + 1}]", jac[i][j], e, 6)
    assert all(abs(jac[i][j]) < 1e-15 for i in range(3) for j in range(i + 1, 3))
    quoted("ds1/dP1", -(1 + PAR[0]) / annuities[0], -1.060900, 6)
    quoted("ds2/dP1", -PAR[1] / annuities[1], -0.018380, 6)
    quoted("ds2/dP2", -(1 + PAR[1]) / annuities[1], -0.543528, 6)
    quoted("ds3/dP1", -PAR[2] / annuities[2], -0.014324, 6)
    quoted("ds3/dP3", -(1 + PAR[2]) / annuities[2], -0.372423, 6)

    inv = lower_triangular_inverse(jac)
    exp_inv = {(0, 0): 0.970874, (1, 0): -0.017076, (1, 1): 0.985604, (2, 0): -0.013144, (2, 1): -0.026554, (2, 2): 1.007589}
    for (i, j), e in exp_inv.items():
        up, dn = list(PAR), list(PAR)
        up[j] += h
        dn[j] -= h
        fd = (zeros_from_par(up)[i] - zeros_from_par(dn)[i]) / (2 * h)
        assert abs(fd - inv[i][j]) < 1e-8, (i, j, fd, inv[i][j])
        quoted(f"Jinv[{i + 1},{j + 1}]", inv[i][j], e, 6)

    print("  5. Mapping zero risk to par risk for a 3y 4% par bond")
    cf = [4.0, 4.0, 104.0]
    dpv_dz = [-t * c * pp for t, c, pp in zip(TIMES, cf, p, strict=True)]
    for k, e in enumerate((-3.8835, -7.4668, -277.1493)):
        quoted(f"dPV/dz{k + 1}", dpv_dz[k], e, 4)
    dpv_ds = [sum(dpv_dz[k] * inv[k][j] for k in range(3)) for j in range(3)]
    quoted("term (dPV/dz1)(Jinv11)", dpv_dz[0] * inv[0][0], -3.7704, 4)
    quoted("term (dPV/dz2)(Jinv21)", dpv_dz[1] * inv[1][0], 0.1275, 4)
    quoted("term (dPV/dz3)(Jinv31)", dpv_dz[2] * inv[2][0], 3.6429, 4)
    quoted("term (dPV/dz2)(Jinv22)", dpv_dz[1] * inv[1][1], -7.3593, 4)
    quoted("term (dPV/dz3)(Jinv32)", dpv_dz[2] * inv[2][1], 7.3593, 4)
    for k, e in enumerate((0.0, 0.0, -279.2525)):
        quoted(f"dPV/ds{k + 1}", dpv_ds[k], e, 4)

    def bond_pv(par: list[float]) -> float:
        return sum(c * d for c, d in zip(cf, bootstrap(par), strict=True))

    for j in range(3):
        up, dn = list(PAR), list(PAR)
        up[j] += h
        dn[j] -= h
        assert abs((bond_pv(up) - bond_pv(dn)) / (2 * h) - dpv_ds[j]) < 1e-5
    quoted("-100 x A3", -100.0 * annuities[2], -279.2525, 4)


def example_turn() -> None:
    print("  6. A year-end turn: jump versus smearing")
    turn_days, premium = 2.0, 0.0100
    jump = premium * turn_days / 365.0
    quoted("jump in -ln P across the turn", jump, 0.0000548, 7)
    quoted("1-week forward over year end, explicit jump (bp)", jump / (7.0 / 365.0) * 1e4, 28.57, 2)
    # Smeared evenly over the quarter, every week of the quarter (year-end week included) carries jump / 0.25.
    quoted("any week of the quarter if the turn is smeared over it (bp)", jump / 0.25 * 1e4, 2.19, 2)
    weeks_in_quarter = math.floor(0.25 * 365.0 / 7.0)
    quoted("whole weeks in the quarter", weeks_in_quarter, 13, 0)
    quoted("weeks overpriced by smearing (all but the year-end week)", weeks_in_quarter - 1, 12, 0)


def main() -> None:
    print("=== fi_curve_numerics: interpolation, locality, Jacobians, turns ===")
    example_forward_shapes()
    example_locality()
    example_jacobian()
    example_turn()
    print(f"\nVerified {len(QUOTED)} curve construction figures.")


if __name__ == "__main__":
    main()
