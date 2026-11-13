"""Geometric probability: every number in the note, recomputed by an independent route.

Backs `01-Probability/09-Geometric-Probability.md`.
Each closed form the note quotes is evaluated and asserted to the quoted decimals, then checked against a seeded
Monte Carlo of the actual geometric experiment (cut the stick, drop the points, draw the chord, drop the needle),
never against the same formula twice.
Simulation tolerances are five standard errors of the estimate, so a correct closed form fails with probability
below one in a million per check; the seed is fixed, so the run is reproducible.
Run it with `python 01-Probability/code/prob_09_geometric_probability.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261019
RNG = np.random.default_rng(SEED)
N_SIM = 1_000_000


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")
    return value


def exact(label: str, value: Fraction, expected: Fraction) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def sim_mean(label: str, samples: np.ndarray, target: float) -> float:
    """Assert a Monte Carlo mean is within five standard errors of the target."""
    est = float(samples.mean())
    se = float(samples.std(ddof=1)) / math.sqrt(samples.size)
    assert abs(est - target) <= 5.0 * se + 1e-12, f"{label}: simulated {est} (se {se}), target {target}"
    print(f"    {label}: simulated {est:.5f} (se {se:.5f}) vs {target:.5f}")
    return est


def simpson(f, a: float, b: float, n: int = 2000) -> float:
    """Composite Simpson rule on n (even) panels."""
    h = (b - a) / n
    s = f(a) + f(b)
    s += 4.0 * sum(f(a + (2 * k - 1) * h) for k in range(1, n // 2 + 1))
    s += 2.0 * sum(f(a + 2 * k * h) for k in range(1, n // 2))
    return s * h / 3.0


def unit_vectors(n: int, dim: int) -> np.ndarray:
    """Uniform points on the unit sphere in R^dim (normalised Gaussians, no angles needed)."""
    z = RNG.standard_normal((n, dim))
    return z / np.linalg.norm(z, axis=1, keepdims=True)


def area_ratios() -> None:
    print("Core concepts: area ratios in the unit square")
    x, y = RNG.random(N_SIM), RNG.random(N_SIM)
    t = 0.25
    sim_mean("P(|X-Y| < 1/4) = 1 - (3/4)^2", (np.abs(x - y) < t).astype(float), 1 - (1 - t) ** 2)
    for s in (0.5, 1.5):
        target = s * s / 2 if s <= 1 else 1 - (2 - s) ** 2 / 2
        sim_mean(f"P(X+Y < {s})", (x + y < s).astype(float), target)
    t = 0.5
    p_prod = t - t * math.log(t)
    sim_mean("P(XY < 1/2) = t - t ln t", (x * y < t).astype(float), p_prod)
    quoted("P(XY < 1/2) (card prob-geo-product-of-uniforms)", p_prod, 0.847, 3)
    assert abs(p_prod - (0.5 + math.log(2) / 2)) < 1e-15
    sim_mean("P(X^2+Y^2 < 1) = pi/4", (x * x + y * y < 1).astype(float), math.pi / 4)
    sim_mean("E|X - Y| = 1/3 (card prob-geo-expected-distance-unit-interval)", np.abs(x - y), 1 / 3)
    # The middle gap of two uniforms is |X - Y|; its density is 2(1-t): integrate t * 2(1-t).
    quoted("E|X-Y| from density 2(1-t)", simpson(lambda u: u * 2 * (1 - u), 0.0, 1.0), 1 / 3, 9)
    for n in (2, 3, 4, 5):
        u = RNG.random((N_SIM, n))
        sim_mean(f"P(U_1+...+U_{n} < 1) = 1/{n}!", (u.sum(axis=1) < 1).astype(float), 1 / math.factorial(n))
    print("    card prob-geo-sum-of-uniforms-simplex: three uniforms give 1/6, checked above")
    # Distance from a uniform point in the unit disc to the centre: rejection sample from the square.
    p = RNG.random((2 * N_SIM, 2)) * 2 - 1
    r = np.hypot(p[:, 0], p[:, 1])
    r = r[r < 1]
    sim_mean("E[R] for a uniform point in the unit disc (card prob-geo-disc-distance-to-center)", r, 2 / 3)
    sim_mean("P(R <= 1/2) = (1/2)^2, so the density is 2r", (r <= 0.5).astype(float), 0.25)


def circle_gaps() -> None:
    print("Core concepts: gaps on a circle and the semicircle result")
    n = 5
    raw = RNG.random((N_SIM // 2, n))
    # Gaps labelled by the point they follow: rotate so point 0 sits at 0, then cut [0, 1] at the others.
    rel = np.sort((raw[:, 1:] - raw[:, :1]) % 1.0, axis=1)
    m = rel.shape[0]
    gaps = np.diff(np.concatenate([np.zeros((m, 1)), rel, np.ones((m, 1))], axis=1), axis=1)
    for j in (0, 2, n - 1):
        sim_mean(f"mean of gap {j} of n = 5, labelled by the point it follows: 1/n", gaps[:, j], 1 / n)
    sim_mean("P(gap > 0.3) = P(min of n-1 uniforms > 0.3) = 0.7^4", (gaps[:, 0] > 0.3).astype(float), 0.7**4)
    # Labelled instead by position from a fixed origin, the gap covering the origin is length-biased.
    srt = np.sort(raw, axis=1)
    sim_mean("gap covering a fixed point on the circle: mean 2/(n+1), not 1/n", srt[:, 0] + 1 - srt[:, -1], 2 / (n + 1))
    for n, q in ((3, Fraction(3, 4)), (4, Fraction(1, 2)), (5, Fraction(5, 16))):
        exact(f"n/2^(n-1) for n = {n}", Fraction(n, 2 ** (n - 1)), q)
        pts = np.sort(RNG.random((N_SIM, n)), axis=1)
        gaps = np.diff(np.concatenate([pts, pts[:, :1] + 1.0], axis=1), axis=1)
        # All points lie in a semicircle iff some gap is at least half the circle.
        sim_mean(f"P(all {n} points in a semicircle)", (gaps.max(axis=1) > 0.5).astype(float), float(q))
    # Acute inscribed triangle, tested directly by the sign of the dot product at each vertex.
    ang = RNG.random((N_SIM, 3)) * 2 * math.pi
    v = np.stack([np.cos(ang), np.sin(ang)], axis=2)
    acute = np.ones(N_SIM, dtype=bool)
    for i in range(3):
        a, b, c = v[:, i], v[:, (i + 1) % 3], v[:, (i + 2) % 3]
        acute &= np.einsum("ij,ij->i", b - a, c - a) > 0
    sim_mean("P(inscribed triangle is acute) (card prob-geo-triangle-contains-center)", acute.astype(float), 0.25)
    # Contains the centre, tested by barycentric signs (independent of the acute test above).
    p0, p1, p2 = v[:, 0], v[:, 1], v[:, 2]

    def cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]

    s0, s1, s2 = cross(p1 - p0, -p0), cross(p2 - p1, -p1), cross(p0 - p2, -p2)
    inside = ((s0 > 0) & (s1 > 0) & (s2 > 0)) | ((s0 < 0) & (s1 < 0) & (s2 < 0))
    assert np.array_equal(inside, acute), "acute iff contains the centre"
    print("    acute iff the triangle contains the centre: identical on every sample")


def wendel_and_tetrahedron() -> None:
    print("Core concepts and worked example: Wendel's theorem and the tetrahedron")

    def wendel(n: int, d: int) -> Fraction:
        return Fraction(sum(math.comb(n - 1, k) for k in range(d)), 2 ** (n - 1))

    exact("Wendel d = 3, n = 4 (common hemisphere)", wendel(4, 3), Fraction(7, 8))
    for n in range(2, 9):
        assert wendel(n, 2) == Fraction(n, 2 ** (n - 1))
    print("    Wendel with d = 2 equals n/2^(n-1) for n = 2..8")
    n = 400_000
    pts = unit_vectors(4 * n, 3).reshape(n, 4, 3)
    a = np.concatenate([np.transpose(pts, (0, 2, 1)), np.ones((n, 1, 4))], axis=1)
    rhs = np.zeros((n, 4, 1))
    rhs[:, 3, 0] = 1.0
    lam = np.linalg.solve(a, rhs)[:, :, 0]
    contains = np.all(lam > 0, axis=1).astype(float)
    sim_mean("P(tetrahedron contains centre) (card prob-geo-sphere-tetrahedron-center)", contains, 1 / 8)


def broken_sticks() -> None:
    print("Core concepts and worked example: broken sticks")
    cuts = np.sort(RNG.random((N_SIM, 2)), axis=1)
    pieces = np.stack([cuts[:, 0], cuts[:, 1] - cuts[:, 0], 1 - cuts[:, 1]], axis=1)
    tri = (pieces.max(axis=1) < 0.5).astype(float)
    sim_mean("version 1: P(triangle) (card prob-geo-broken-stick-triangle)", tri, 0.25)
    sim_mean("P(left piece > 1/2)", (pieces[:, 0] > 0.5).astype(float), 0.25)
    srt = np.sort(pieces, axis=1)
    sim_mean("E[shortest of 3] = 1/9", srt[:, 0], 1 / 9)
    sim_mean("E[middle of 3] = 5/18", srt[:, 1], 5 / 18)
    sim_mean("E[longest of 3] = 11/18", srt[:, 2], 11 / 18)
    for n in (3, 4, 5):
        h_n = sum(Fraction(1, k) for k in range(1, n + 1))
        if n == 3:
            exact("1/n^2 for n = 3", Fraction(1, n * n), Fraction(1, 9))
            exact("H_n/n for n = 3", h_n / n, Fraction(11, 18))
            exact("middle = 1 - 1/9 - 11/18", 1 - Fraction(1, 9) - h_n / n, Fraction(5, 18))
        c = np.sort(RNG.random((N_SIM // 2, n - 1)), axis=1)
        pc = np.diff(np.concatenate([np.zeros((c.shape[0], 1)), c, np.ones((c.shape[0], 1))], axis=1), axis=1)
        sim_mean(f"E[shortest of {n}] = 1/n^2", pc.min(axis=1), 1 / n**2)
        sim_mean(f"E[longest of {n}] = H_n/n", pc.max(axis=1), float(h_n) / n)
    # Version 2: break once, then break the longer piece uniformly.
    x = RNG.random(N_SIM)
    long_start = np.where(x < 0.5, x, 0.0)
    long_len = np.maximum(x, 1 - x)
    y = long_start + RNG.random(N_SIM) * long_len
    lo, hi = np.minimum(x, y), np.maximum(x, y)
    tri2 = (np.maximum.reduce([lo, hi - lo, 1 - hi]) < 0.5).astype(float)
    v2 = 2 * math.log(2) - 1
    quoted("version 2: 2 ln 2 - 1 (card prob-geo-break-longer-piece-triangle)", v2, 0.386, 3)
    quoted("version 2 by Simpson on 2 * int_0^1/2 x/(1-x)", 2 * simpson(lambda t: t / (1 - t), 0.0, 0.5), v2, 10)
    sim_mean("version 2 simulated", tri2, v2)
    # Version 3: break once, then break a randomly chosen piece.
    pick_left = RNG.random(N_SIM) < 0.5
    start = np.where(pick_left, 0.0, x)
    length = np.where(pick_left, x, 1 - x)
    y3 = start + RNG.random(N_SIM) * length
    lo, hi = np.minimum(x, y3), np.maximum(x, y3)
    tri3 = (np.maximum.reduce([lo, hi - lo, 1 - hi]) < 0.5).astype(float)
    v3 = math.log(2) - 0.5
    quoted("version 3: ln 2 - 1/2", v3, 0.193, 3)
    sim_mean("version 3 simulated", tri3, v3)


def bertrand_and_buffon() -> None:
    print("Core concepts: Bertrand's paradox and Buffon's needle")
    root3 = math.sqrt(3)
    t1, t2 = RNG.random(N_SIM) * 2 * math.pi, RNG.random(N_SIM) * 2 * math.pi
    chord = 2 * np.abs(np.sin((t1 - t2) / 2))
    sim_mean("rule 1, uniform endpoints: P(chord > sqrt 3)", (chord > root3).astype(float), 1 / 3)
    sim_mean("expected chord length, uniform endpoints (card prob-geo-expected-chord-length)", chord, 4 / math.pi)
    quoted("4/pi", 4 / math.pi, 1.27, 2)
    d = RNG.random(N_SIM)
    sim_mean("rule 2, uniform distance on a radius", (2 * np.sqrt(1 - d * d) > root3).astype(float), 1 / 2)
    p = RNG.random((2 * N_SIM, 2)) * 2 - 1
    r = np.hypot(p[:, 0], p[:, 1])
    r = r[r < 1]
    sim_mean("rule 3, uniform midpoint in the disc", (2 * np.sqrt(1 - r * r) > root3).astype(float), 1 / 4)
    # Buffon: needle length 0.7 (input), lines spaced 1 apart; direction from a normalised Gaussian.
    ell, gap = 0.7, 1.0
    centre = RNG.random(N_SIM) * gap
    u = unit_vectors(N_SIM, 2)
    y1, y2 = centre - 0.5 * ell * u[:, 1], centre + 0.5 * ell * u[:, 1]
    crosses = (np.floor(y1 / gap) != np.floor(y2 / gap)).astype(float)
    sim_mean("Buffon, l = 0.7, d = 1: P(cross) = 2l/(pi d) (card prob-geo-buffon-needle)", crosses, 2 * ell / (math.pi * gap))


def meeting_and_centre() -> None:
    print("Worked examples: meeting problem and closer to the centre than to the edge")
    exact("meeting: 1 - (3/4)^2", 1 - Fraction(3, 4) ** 2, Fraction(7, 16))
    quoted("7/16", 7 / 16, 0.44, 2)
    x, y = RNG.random(N_SIM), RNG.random(N_SIM)
    sim_mean("meeting simulated (card prob-geo-meeting-problem)", (np.abs(x - y) <= 0.25).astype(float), 7 / 16)
    # Closer to the centre than to the nearest side, simulated on the full square.
    p = RNG.random((N_SIM, 2)) - 0.5
    closer = (np.hypot(p[:, 0], p[:, 1]) < 0.5 - np.abs(p).max(axis=1)).astype(float)
    target = (4 * math.sqrt(2) - 5) / 3
    quoted("(4 sqrt 2 - 5)/3 (card prob-geo-closer-to-center-than-edge)", target, 0.219, 3)
    sim_mean("closer to centre simulated", closer, target)
    # Parabola x = 1/4 - y^2 meets y = x: bisection, against (sqrt 2 - 1)/2.
    lo, hi = 0.0, 0.5
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if 0.25 - mid * mid - mid > 0:
            lo = mid
        else:
            hi = mid
    quoted("parabola meets y = x at", lo, (math.sqrt(2) - 1) / 2, 12)
    eighth = simpson(lambda yy: 0.25 - yy * yy - yy, 0.0, lo)
    quoted("8 * area of the one-eighth region (Simpson)", 8 * eighth, target, 10)
    quoted("inner disc pi/16", math.pi / 16, 0.196, 3)
    assert math.pi / 16 < target < math.pi / 4


if __name__ == "__main__":
    area_ratios()
    circle_gaps()
    wendel_and_tetrahedron()
    broken_sticks()
    bertrand_and_buffon()
    meeting_and_centre()
    print("All geometric probability checks passed.")
