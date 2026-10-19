"""Order statistics and extremes: every expectation, law and constant in the note.

Backs every number in `01-Probability/08-Order-Statistics-and-Extremes.md`.
Independent routes used here:
- dice maxima and minima by enumerating every outcome with `fractions.Fraction`;
- uniform order-statistic moments by exact polynomial integration of the binomial-tail CDF
  P(U_(k) > x) = P(Bin(n, x) < k), never via the Beta mean formula;
- exponential maxima by exact inclusion-exclusion integrals and by simulation, not the Renyi sum;
- records by enumerating permutations; the German tank estimator by enumerating every sample;
- Gaussian maxima by numerical integration of n x Phi^(n-1) phi, cross-checked by simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 01-Probability/code/prob_08_order_statistics.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np

SEED = 20261019


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


# ------------------------------------------------------------------ polynomials in x with Fraction coefficients


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_pow(a: list[Fraction], k: int) -> list[Fraction]:
    out = [Fraction(1)]
    for _ in range(k):
        out = poly_mul(out, a)
    return out


def integrate01(p: list[Fraction]) -> Fraction:
    return sum((c / (i + 1) for i, c in enumerate(p)), Fraction(0))


def survival_kth(n: int, k: int) -> list[Fraction]:
    """P(U_(k) > x) = P(fewer than k of n uniforms are <= x), as a polynomial in x."""
    out = [Fraction(0)]
    for j in range(k):
        term = [
            c * math.comb(n, j) for c in poly_mul(poly_pow([Fraction(0), Fraction(1)], j), poly_pow([Fraction(1), Fraction(-1)], n - j))
        ]
        out = [a + b for a, b in itertools.zip_longest(out, term, fillvalue=Fraction(0))]
    return out


def uniform_moments(n: int, k: int) -> tuple[Fraction, Fraction]:
    """E[U_(k)] and E[U_(k)^2] from the tail formulas E[X] = int S(x) dx and E[X^2] = int 2x S(x) dx."""
    s = survival_kth(n, k)
    return integrate01(s), integrate01(poly_mul([Fraction(0), Fraction(2)], s))


# ------------------------------------------------------------------ sections


def dice() -> None:
    print("Dice maxima and minima (cards prob-os-expected-max-two-dice, prob-os-expected-min-two-dice, prob-os-expected-max-three-dice)")
    two = list(itertools.product(range(1, 7), repeat=2))
    three = list(itertools.product(range(1, 7), repeat=3))
    pmf = [Fraction(sum(1 for r in two if max(r) == k), 36) for k in range(1, 7)]
    exact("P(max of two = k), k = 1..6", pmf, [Fraction(2 * k - 1, 36) for k in range(1, 7)])
    exact("k(2k-1) for k = 1..6", [k * (2 * k - 1) for k in range(1, 7)], [1, 6, 15, 28, 45, 66])
    e_max2 = Fraction(sum(max(r) for r in two), 36)
    exact("E[max of two dice]", e_max2, Fraction(161, 36))
    approx("E[max of two dice]", float(e_max2), 4.47, 2)
    e_min2 = Fraction(sum(min(r) for r in two), 36)
    exact("E[min of two dice]", e_min2, Fraction(91, 36))
    approx("E[min of two dice]", float(e_min2), 2.53, 2)
    exact("sum of ((7-k)/6)^2", sum((Fraction(7 - k, 6) ** 2 for k in range(1, 7)), Fraction(0)), Fraction(91, 36))
    e_max3 = Fraction(sum(max(r) for r in three), 216)
    exact("E[max of three dice]", e_max3, Fraction(119, 24))
    approx("E[max of three dice]", float(e_max3), 4.96, 2)
    exact("1+8+27+64+125", sum(k**3 for k in range(1, 6)), 225)
    for n in range(1, 6):
        outcomes = list(itertools.product(range(1, 7), repeat=n))
        brute = Fraction(sum(max(r) for r in outcomes), len(outcomes))
        assert brute == 6 - sum(Fraction(k, 6) ** n for k in range(1, 6)), n
    print("    E[max of n dice] = 6 - sum_{k=1}^{5} (k/6)^n by enumeration for n = 1..5")


def uniforms(rng: np.random.Generator) -> None:
    print("Uniform order statistics, exact integration of the binomial-tail CDF (cards prob-os-kth-uniform-order-stat, ...)")
    for n in range(1, 9):
        for k in range(1, n + 1):
            m1, m2 = uniform_moments(n, k)
            assert m1 == Fraction(k, n + 1), (n, k, m1)
            assert m2 - m1 * m1 == Fraction(k * (n - k + 1), (n + 1) ** 2 * (n + 2)), (n, k)
        e_max, e_max2 = uniform_moments(n, n)
        e_min, _ = uniform_moments(n, 1)
        assert e_max - e_min == Fraction(n - 1, n + 1)
        assert e_max2 - e_max**2 == Fraction(n, (n + 1) ** 2 * (n + 2))
        assert e_max2 == Fraction(n, n + 2)
    print("    E[U_(k)] = k/(n+1), Var = k(n-k+1)/((n+1)^2(n+2)), E[range] = (n-1)/(n+1) and Var[max] = n/((n+1)^2(n+2)), n = 1..8")
    u = np.sort(rng.random((500_000, 5)), axis=1)
    gaps = np.diff(np.concatenate([np.zeros((len(u), 1)), u, np.ones((len(u), 1))], axis=1), axis=1)
    assert np.all(np.abs(gaps.mean(axis=0) - 1 / 6) < 0.001), gaps.mean(axis=0)
    print("    n=5: all six simulated spacings have mean 1/6 within 0.001")

    print("Correlation of the min and max of two uniforms (card prob-os-min-max-two-uniforms-correlation)")
    e_min, e_min2 = uniform_moments(2, 1)
    e_max, e_max2 = uniform_moments(2, 2)
    exact("E[min], E[max]", (e_min, e_max), (Fraction(1, 3), Fraction(2, 3)))
    exact("Var[min], Var[max]", (e_min2 - e_min**2, e_max2 - e_max**2), (Fraction(1, 18), Fraction(1, 18)))
    exact("1*2/(9*4)", Fraction(1 * 2, 9 * 4), Fraction(1, 18))
    e_prod = Fraction(1, 2) * Fraction(1, 2)  # min * max = U V and U, V are independent
    exact("Cov = 1/4 - 2/9", e_prod - e_min * e_max, Fraction(1, 36))
    exact("Corr", (e_prod - e_min * e_max) / (e_min2 - e_min**2), Fraction(1, 2))
    v = rng.random((1_000_000, 2))
    simulated("Corr(min, max), simulated", float(np.corrcoef(v.min(axis=1), v.max(axis=1))[0, 1]), 0.5, 0.003)
    for n in (3, 6):
        w = np.sort(rng.random((500_000, n)), axis=1)
        simulated(f"Corr(U_(1), U_({n})) for n={n} (positive; equals 1/n)", float(np.corrcoef(w[:, 0], w[:, -1])[0, 1]), 1 / n, 0.004)

    print("Median of three uniforms (card prob-os-median-three-uniforms)")
    s = survival_kth(3, 2)
    cdf = [Fraction(1) - s[0]] + [-c for c in s[1:]]
    exact("CDF coefficients of U_(2), n=3 (const, x, x^2, x^3)", cdf, [0, 0, 3, -2])
    approx("P(median <= 0.3)", float(sum(c * Fraction(3, 10) ** i for i, c in enumerate(cdf))), 0.216, 3)
    approx("3(0.09) - 2(0.027)", 0.27 - 0.054, 0.216, 12)
    m1, m2 = uniform_moments(3, 2)
    exact("mean of the median", m1, Fraction(1, 2))
    exact("variance of the median", m2 - m1 * m1, Fraction(1, 20))
    med = np.median(rng.random((1_000_000, 3)), axis=1)
    simulated("P(median <= 0.3), simulated", float((med <= 0.3).mean()), 0.216, 0.002)

    print("Second-price auction, 4 bidders (card prob-os-second-price-auction-revenue)")
    second, _ = uniform_moments(4, 3)
    top, _ = uniform_moments(4, 4)
    exact("E[second highest of 4]", second, Fraction(3, 5))
    exact("E[winner's surplus] = E[U_(4) - U_(3)]", top - second, Fraction(1, 5))
    exact("best of 4 offers E[max]", top, Fraction(4, 5))

    print("All of three uniforms within 1/2 (card prob-os-uniform-range-within-half)")
    # P(range <= r) by exact integration: the min sits at x and the other n-1 points lie in [x, min(x+r, 1)]
    n, r = 3, Fraction(1, 2)
    # for x in [0, 1-r]: n r^(n-1) dx; for x in [1-r, 1]: n (1-x)^(n-1) dx
    part1 = n * r ** (n - 1) * (1 - r)
    part2 = n * Fraction(1, n) * r**n
    exact("P(range of 3 uniforms <= 1/2), by integrating over the min", part1 + part2, Fraction(1, 2))
    exact("n r^(n-1) - (n-1) r^n at n=3, r=1/2", n * r ** (n - 1) - (n - 1) * r**n, Fraction(1, 2))
    w = rng.random((1_000_000, 3))
    simulated("P(range <= 1/2), simulated", float((w.max(axis=1) - w.min(axis=1) <= 0.5).mean()), 0.5, 0.002)


def exponentials(rng: np.random.Generator) -> None:
    print("Exponentials (cards prob-os-min-of-exponentials, prob-os-max-of-exponentials)")

    def e_max_exp(n: int) -> Fraction:
        """int_0^inf 1 - (1 - e^-x)^n dx = sum_{j=1}^{n} (-1)^(j+1) C(n,j)/j by inclusion-exclusion."""
        return sum((Fraction((-1) ** (j + 1) * math.comb(n, j), j) for j in range(1, n + 1)), Fraction(0))

    for n in range(1, 15):
        assert e_max_exp(n) == sum(Fraction(1, k) for k in range(1, n + 1)), n
    print("    inclusion-exclusion integral of 1 - (1 - e^-x)^n equals H_n for n = 1..14")
    exact("three bulbs: E[last failure]", e_max_exp(3), Fraction(11, 6))
    exact("1/3 + 1/2 + 1", Fraction(1, 3) + Fraction(1, 2) + 1, Fraction(11, 6))
    life = rng.exponential(1.0, (1_000_000, 3))
    srt = np.sort(life, axis=1)
    simulated("E[last of three bulbs], simulated", float(srt[:, 2].mean()), 11 / 6, 0.005)
    simulated("E[first failure] = 1/3", float(srt[:, 0].mean()), 1 / 3, 0.002)
    simulated("E[second gap] = 1/2", float((srt[:, 1] - srt[:, 0]).mean()), 0.5, 0.003)
    simulated("E[third gap] = 1", float((srt[:, 2] - srt[:, 1]).mean()), 1.0, 0.004)
    simulated("corr(first gap, second gap) (independent)", float(np.corrcoef(srt[:, 0], srt[:, 1] - srt[:, 0])[0, 1]), 0.0, 0.003)
    x = rng.exponential(1 / 2.0, 1_000_000)
    y = rng.exponential(1 / 3.0, 1_000_000)
    mn = np.minimum(x, y)
    simulated("min(Exp(2), Exp(3)) mean = 1/5", float(mn.mean()), 0.2, 0.001)
    simulated("P(X < Y) = 2/5", float((x < y).mean()), 0.4, 0.002)
    simulated("E[min | X wins] = E[min | Y wins] (independence of argmin)", float(mn[x < y].mean() - mn[x >= y].mean()), 0.0, 0.002)


def records() -> None:
    print("Records (card prob-os-expected-records)")
    for n in range(1, 9):
        perms = list(itertools.permutations(range(n)))
        total = sum(sum(1 for j in range(n) if p[j] == max(p[: j + 1])) for p in perms)
        assert Fraction(total, len(perms)) == sum(Fraction(1, j) for j in range(1, n + 1)), n
    print("    E[records] = H_n by enumerating all permutations, n = 1..8")
    n = 10**6
    h = sum(1 / j for j in range(1, n + 1))
    approx("H_n - ln n at n = 10^6 (Euler-Mascheroni constant)", h - math.log(n), 0.577, 3)


def german_tank() -> None:
    print("German tank (card prob-os-german-tank-serials)")
    for big_n, k in ((20, 4), (15, 3), (12, 5)):
        samples = list(itertools.combinations(range(1, big_n + 1), k))
        e_m = Fraction(sum(max(s) for s in samples), len(samples))
        assert e_m == Fraction(k * (big_n + 1), k + 1), (big_n, k)
        est = Fraction(sum(max(s) * Fraction(k + 1, k) - 1 for s in samples), len(samples))
        assert est == big_n, (big_n, k, est)
    print("    E[max] = k(N+1)/(k+1) and E[m(1+1/k) - 1] = N exactly, by enumerating every sample (N, k) in (20,4), (15,3), (12,5)")
    exact("estimate from k=4 serials with max 60", 60 * Fraction(5, 4) - 1, 74)


def gaussian_maxima(rng: np.random.Generator) -> None:
    print("Gaussian maxima (card prob-os-max-of-normals-growth)")
    x = np.linspace(-12, 12, 480_001)
    phi = np.exp(-x * x / 2) / math.sqrt(2 * math.pi)
    big_phi = np.cumsum(phi) * (x[1] - x[0])
    big_phi = np.clip(big_phi - big_phi[0] + phi[0] * (x[1] - x[0]) / 2, 0, 1)

    def e_max(n: int) -> float:
        dens = n * big_phi ** (n - 1) * phi
        return float((x * dens).sum() * (x[1] - x[0]))

    m10, m100 = e_max(10), e_max(100)
    approx("E[max of 10 normals] (integration)", m10, 1.54, 2)
    approx("E[max of 100 normals] (integration)", m100, 2.51, 2)
    sims10 = rng.standard_normal((200_000, 10)).max(axis=1).mean()
    sims100 = rng.standard_normal((40_000, 100)).max(axis=1).mean()
    simulated("E[max of 10 normals], simulated", float(sims10), m10, 0.005)
    simulated("E[max of 100 normals], simulated", float(sims100), m100, 0.008)
    approx("sqrt(2 ln 10)", math.sqrt(2 * math.log(10)), 2.15, 2)
    approx("sqrt(2 ln 100)", math.sqrt(2 * math.log(100)), 3.03, 2)
    approx("overstatement at n = 100", math.sqrt(2 * math.log(100)) - m100, 0.5, 1)


def main() -> None:
    rng = np.random.default_rng(SEED)
    dice()
    uniforms(rng)
    exponentials(rng)
    records()
    german_tank()
    gaussian_maxima(rng)
    print("All order-statistic checks passed.")


if __name__ == "__main__":
    main()
