"""Joint distributions and transformations: every probability and moment in the note.

Backs every number in `01-Probability/05-Joint-Distributions-and-Transformations.md`.
Independent routes used here:
- region probabilities and moments over the unit square and the triangle are integrated exactly as
  polynomials with `fractions.Fraction`, or numerically on a fine grid;
- the bivariate-normal forecast, hedge ratio, orthant probability, radius tail, portfolio volatility and
  the normal-marginals counterexample are reproduced by seeded simulation with stated tolerances;
- derived densities (chi-square with one degree of freedom, lognormal) are integrated and compared with
  simulated frequencies.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 01-Probability/code/prob_05_joint.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261019
N = 2_000_000


def exact(label: str, value: Fraction | int, expected: Fraction | int) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


def normal_cdf(z: float) -> float:
    return 0.5 * math.erfc(-z / math.sqrt(2))


def poly_integral_triangle(p: int, q: int) -> Fraction:
    """Exact integral of x^p y^q over {0 < x < y < 1}: inner over x in (0, y), outer over y."""
    return Fraction(1, p + 1) * Fraction(1, p + q + 2)


def uniforms(rng: np.random.Generator) -> None:
    print("Example 1 - sum of two uniforms (card prob-joint-sum-two-uniforms)")
    # exact: the corner {u+v >= 1.5} is the triangle with legs 1/2
    exact("corner area 0.5^2/2", Fraction(1, 2) ** 2 / 2, Fraction(1, 8))
    s = np.linspace(0, 1.5, 300_001)
    tri = np.minimum(s, 2 - s)
    integral = float(((tri[1:] + tri[:-1]) / 2 * np.diff(s)).sum())
    approx("integral of the triangle density up to 1.5", integral, 7 / 8, 9)
    exact("P(U+V < 1.5)", 1 - Fraction(1, 8), Fraction(7, 8))
    u, v = rng.random(N), rng.random(N)
    simulated("P(U+V < 1.5), simulated", float((u + v < 1.5).mean()), 7 / 8, 0.001)

    print("Example 2 - product of two uniforms (card prob-joint-product-two-uniforms)")
    simulated("P(UV <= 1/2), simulated", float((u * v <= 0.5).mean()), 0.5 + 0.5 * math.log(2), 0.001)
    approx("1/2 + (1/2) ln 2", 0.5 + 0.5 * math.log(2), 0.847, 3)
    simulated("P(-ln(UV) <= 2) against Gamma(2,1) CDF 1 - 3e^-2", float((-np.log(u * v) <= 2).mean()), 1 - 3 * math.exp(-2), 0.002)

    print("Example 5 - triangle support, min and max of two uniforms (cards prob-joint-triangle-support-dependence, ...)")
    # density 2 on {0<x<y<1}: moments by exact polynomial integration
    ex, ey = 2 * poly_integral_triangle(1, 0), 2 * poly_integral_triangle(0, 1)
    ex2, ey2, exy = 2 * poly_integral_triangle(2, 0), 2 * poly_integral_triangle(0, 2), 2 * poly_integral_triangle(1, 1)
    exact("total mass", 2 * poly_integral_triangle(0, 0), 1)
    exact("E[min]", ex, Fraction(1, 3))
    exact("E[max]", ey, Fraction(2, 3))
    exact("E[min * max] = E[UV]", exy, Fraction(1, 4))
    exact("Var[min]", ex2 - ex**2, Fraction(1, 18))
    exact("Var[max]", ey2 - ey**2, Fraction(1, 18))
    exact("Cov(min, max)", exy - ex * ey, Fraction(1, 36))
    exact("Corr(min, max)", (exy - ex * ey) / (ex2 - ex**2), Fraction(1, 2))
    lo, hi = np.minimum(u, v), np.maximum(u, v)
    simulated("Corr(min, max), simulated", float(np.corrcoef(lo, hi)[0, 1]), 0.5, 0.002)
    band = np.abs(hi - 0.6) < 0.005
    simulated("E[min | max = 0.6], simulated (Y/2 = 0.3)", float(lo[band].mean()), 0.3, 0.003)
    simulated("min < 0.1 whenever max = 0.1 (fraction of violations)", float((lo[np.abs(hi - 0.1) < 0.005] > 0.105).mean()), 0.0, 0.0)


def bivariate_normal(rng: np.random.Generator) -> None:
    print("Example 3 - conditional forecast and hedge ratio (cards prob-joint-conditional-forecast-returns, ...)")
    sx, sy, rho = 0.02, 0.03, 0.6
    x = sx * rng.standard_normal(N)
    y = sy * (rho * x / sx + math.sqrt(1 - rho**2) * rng.standard_normal(N))
    beta = float(np.cov(x, y)[0, 1] / x.var())
    resid = y - beta * x
    simulated("OLS slope of Y on X (hedge ratio)", beta, 0.9, 0.003)
    simulated("residual sd after hedging, in %", 100 * float(resid.std()), 2.4, 0.01)
    simulated("fraction of Y variance removed", 1 - float(resid.var() / y.var()), 0.36, 0.002)
    band = np.abs(x - 0.04) < 0.0005
    simulated("E[Y | X = 4%] in %, simulated", 100 * float(y[band].mean()), 3.6, 0.1)
    simulated("sd[Y | X = 4%] in %, simulated", 100 * float(y[band].std()), 2.4, 0.1)
    simulated("P(Y > 0 | X = 4%), simulated", float((y[band] > 0).mean()), 0.933, 0.02)
    approx("conditional mean 0.6 * 2 * 3%", 100 * rho * (0.04 / sx) * sy, 3.6, 1)
    approx("conditional sd 3% sqrt(1 - 0.36)", 100 * sy * math.sqrt(1 - rho**2), 2.4, 1)
    approx("Phi(1.5)", normal_cdf(1.5), 0.933, 3)

    print("Example 4 - both positive (card prob-joint-bivariate-normal-orthant)")
    for r, quoted in ((0.5, 1 / 3), (0.0, 0.25), (-0.5, 1 / 6)):
        z1 = rng.standard_normal(N)
        z2 = r * z1 + math.sqrt(1 - r * r) * rng.standard_normal(N)
        simulated(f"P(X>0, Y>0) at rho={r}, simulated", float(((z1 > 0) & (z2 > 0)).mean()), quoted, 0.001)
    approx("1/4 + arcsin(0.5)/(2 pi)", 0.25 + math.asin(0.5) / (2 * math.pi), 1 / 3, 12)
    approx("rho = 1 limit", 0.25 + math.asin(1) / (2 * math.pi), 0.5, 12)
    approx("rho = -1 limit", 0.25 + math.asin(-1) / (2 * math.pi), 0.0, 12)

    print("Radius of two normals (card prob-joint-radius-two-normals)")
    z1, z2 = rng.standard_normal(N), rng.standard_normal(N)
    r2 = z1**2 + z2**2
    simulated("P(X^2 + Y^2 > 4), simulated", float((r2 > 4).mean()), math.exp(-2), 0.001)
    approx("e^-2", math.exp(-2), 0.135, 3)
    simulated("E[R^2] (Exp with mean 2)", float(r2.mean()), 2.0, 0.005)
    theta = np.arctan2(z2, z1)
    simulated("corr(R^2, Theta) (independent)", float(np.corrcoef(r2, theta)[0, 1]), 0.0, 0.003)
    u1, u2 = rng.random(N), rng.random(N)
    bm = np.sqrt(-2 * np.log(u1)) * np.cos(2 * math.pi * u2)
    simulated("Box-Muller sample sd", float(bm.std()), 1.0, 0.002)
    simulated("Box-Muller P(Z <= 1)", float((bm <= 1).mean()), normal_cdf(1), 0.001)

    print("Portfolio volatility (card prob-joint-two-asset-portfolio-vol)")
    approx("4 + 9 + 2*0.6*2*3", 4 + 9 + 2 * 0.6 * 2 * 3, 20.2, 9)
    approx("sqrt(4 + 9 + 2*0.6*2*3) in %", math.sqrt(4 + 9 + 2 * 0.6 * 2 * 3), 4.49, 2)
    cov = np.array([[0.02**2, 0.6 * 0.02 * 0.03], [0.6 * 0.02 * 0.03, 0.03**2]])
    w = np.ones(2)
    approx("sqrt(w' Sigma w) in % (matrix route)", 100 * math.sqrt(float(w @ cov @ w)), 4.49, 2)
    simulated("sd of x + y, simulated, in %", 100 * float((x + y).std()), 4.49, 0.01)

    print("Normal marginals that are not jointly normal (card prob-joint-normal-marginals-not-jointly-normal)")
    xx = rng.standard_normal(N)
    w2 = rng.choice([-1.0, 1.0], N) * xx
    simulated("Cov(X, SX)", float(np.mean(xx * w2)), 0.0, 0.003)
    simulated("P(X + SX = 0)", float((xx + w2 == 0).mean()), 0.5, 0.002)
    simulated("P(SX <= 1) (standard normal marginal)", float((w2 <= 1).mean()), normal_cdf(1), 0.001)

    print("Uncorrelated but dependent (card prob-joint-uncorrelated-not-independent)")
    uu = rng.uniform(-1, 1, N)
    simulated("Cov(X, X^2) for X ~ U(-1,1)", float(np.mean(uu * uu**2) - uu.mean() * np.mean(uu**2)), 0.0, 0.001)


def transformations(rng: np.random.Generator) -> None:
    print("Transformations (cards prob-joint-chi-square-one-density, prob-joint-lognormal-density, prob-joint-normal-ratio-cauchy)")
    # integrate with the substitution y = t^2 to remove the 1/sqrt(y) singularity
    t = np.linspace(0, 1, 200_001)
    integrand = 2 * t * np.exp(-(t**2) / 2) / np.sqrt(2 * math.pi * t**2 + 1e-300)
    integrand[0] = 2 / math.sqrt(2 * math.pi)
    p_le_1 = float(((integrand[1:] + integrand[:-1]) / 2 * np.diff(t)).sum())
    z = rng.standard_normal(N)
    simulated("P(Z^2 <= 1) from the derived density vs simulation", p_le_1, float((z**2 <= 1).mean()), 0.001)
    mu, sig = 0.1, 0.3
    ys = np.linspace(1e-9, 20, 2_000_001)
    f = np.exp(-((np.log(ys) - mu) ** 2) / (2 * sig**2)) / (ys * sig * math.sqrt(2 * math.pi))
    mass = float(((f[1:] + f[:-1]) / 2 * np.diff(ys)).sum())
    mean = float(((ys[1:] * f[1:] + ys[:-1] * f[:-1]) / 2 * np.diff(ys)).sum())
    approx("lognormal density integrates to 1", mass, 1.0, 6)
    simulated("lognormal density mean vs simulated e^X", mean, float(np.exp(mu + sig * z).mean()), 0.002)
    ratio = rng.standard_normal(N) / rng.standard_normal(N)
    simulated("P(|Z1/Z2| <= 1) (standard Cauchy gives 1/2)", float((np.abs(ratio) <= 1).mean()), 0.5, 0.001)
    simulated("P(Z1/Z2 <= 2) against Cauchy CDF 1/2 + arctan(2)/pi", float((ratio <= 2).mean()), 0.5 + math.atan(2) / math.pi, 0.001)


def main() -> None:
    rng = np.random.default_rng(SEED)
    uniforms(rng)
    bivariate_normal(rng)
    transformations(rng)
    print("All joint-distribution checks passed.")


if __name__ == "__main__":
    main()
