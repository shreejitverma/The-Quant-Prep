"""Random variables and distributions: the table, the normal quantiles and every worked number.

Backs every number in `01-Probability/03-Random-Variables-and-Distributions.md`.
Independent routes used here:
- the mean and variance column of the table is recomputed from each PMF by direct summation, or from
  each PDF by composite Simpson integration, and compared with the closed forms the table quotes;
- the normal CDF is obtained by Simpson integration of the density (not from `math.erf`), and the
  quantiles by bisection on that integral;
- the exponential race, memorylessness, lognormal and thinning numbers are reproduced by seeded simulation;
- the Beta-binomial result is checked by exact polynomial integration with `fractions.Fraction`.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 01-Probability/code/prob_03_distributions.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261019


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


def simpson(f, a: float, b: float, n: int = 20_000) -> float:
    """Composite Simpson rule with an even number of panels."""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


def phi(x):
    return np.exp(-0.5 * np.asarray(x) ** 2) / math.sqrt(2 * math.pi)


def normal_cdf(z: float) -> float:
    """Phi(z) as 1/2 plus the Simpson integral of the density from 0 to z."""
    return 0.5 + (simpson(phi, 0.0, z) if z >= 0 else -simpson(phi, z, 0.0))


def normal_quantile(p: float) -> float:
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if normal_cdf(mid) < p else (lo, mid)
    return 0.5 * (lo + hi)


# ------------------------------------------------------------------ the table


def table_moments() -> None:
    print("The table: mean and variance by direct summation or integration, against the closed forms")

    def discrete(name: str, support, pmf, mean: float, var: float) -> None:
        k = np.asarray(list(support), dtype=float)
        p = np.array([pmf(int(v)) for v in k])
        assert abs(p.sum() - 1) < 1e-12, name
        m = float((k * p).sum())
        v = float(((k - m) ** 2 * p).sum())
        assert abs(m - mean) < 1e-9 and abs(v - var) < 1e-9, (name, m, v, mean, var)
        print(f"    {name}: mean {m:.6f}, variance {v:.6f} (closed forms {mean:.6f}, {var:.6f})")

    def continuous(name: str, pdf, a: float, b: float, mean: float, var: float, tol: float = 1e-7) -> None:
        total = simpson(pdf, a, b, 200_000)
        m = simpson(lambda x: x * pdf(x), a, b, 200_000)
        v = simpson(lambda x: (x - m) ** 2 * pdf(x), a, b, 200_000)
        assert abs(total - 1) < tol and abs(m - mean) < tol and abs(v - var) < tol * 10, (name, total, m, v, mean, var)
        print(f"    {name}: mean {m:.6f}, variance {v:.6f} (closed forms {mean:.6f}, {var:.6f})")

    p, n, r, lam = 0.3, 12, 3, 2.5
    discrete("Bernoulli(0.3)", range(2), lambda x: p**x * (1 - p) ** (1 - x), p, p * (1 - p))
    discrete("Binomial(12,0.3)", range(n + 1), lambda k: math.comb(n, k) * p**k * (1 - p) ** (n - k), n * p, n * p * (1 - p))
    discrete("Geometric(0.3) on 1,2,...", range(1, 400), lambda k: (1 - p) ** (k - 1) * p, 1 / p, (1 - p) / p**2)
    discrete(
        "Negative binomial(3,0.3)",
        range(r, 600),
        lambda k: math.comb(k - 1, r - 1) * p**r * (1 - p) ** (k - r),
        r / p,
        r * (1 - p) / p**2,
    )
    discrete("Poisson(2.5)", range(120), lambda k: math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1)), lam, lam)
    continuous("Uniform(2,5)", lambda x: np.full_like(x, 1 / 3), 2.0, 5.0, 3.5, 9 / 12)
    continuous("Exponential(rate 2.5)", lambda x: lam * np.exp(-lam * x), 0.0, 40.0, 1 / lam, 1 / lam**2)
    k_shape = 3.0
    continuous(
        "Gamma(3, rate 2.5)",
        lambda x: lam**k_shape * x ** (k_shape - 1) * np.exp(-lam * x) / math.gamma(k_shape),
        0.0,
        60.0,
        k_shape / lam,
        k_shape / lam**2,
    )
    mu, sig = 0.4, 1.3
    continuous("Normal(0.4, 1.3^2)", lambda x: phi((x - mu) / sig) / sig, mu - 15 * sig, mu + 15 * sig, mu, sig**2)
    mu, sig = 0.1, 0.25
    continuous(
        "Lognormal(0.1, 0.25^2)",
        lambda x: phi((np.log(np.maximum(x, 1e-300)) - mu) / sig) / (sig * np.maximum(x, 1e-300)),
        1e-9,
        20.0,
        math.exp(mu + sig**2 / 2),
        (math.exp(sig**2) - 1) * math.exp(2 * mu + sig**2),
    )
    a, b = 2.0, 5.0
    beta_ab = math.gamma(a) * math.gamma(b) / math.gamma(a + b)
    continuous(
        "Beta(2,5)",
        lambda x: x ** (a - 1) * (1 - x) ** (b - 1) / beta_ab,
        0.0,
        1.0,
        a / (a + b),
        a * b / ((a + b) ** 2 * (a + b + 1)),
    )

    print("Uniform variance at the board (card prob-dist-uniform-variance), exact integration of polynomials")
    e_u = Fraction(1, 2)  # integral of x over [0,1]
    e_u2 = Fraction(1, 3)  # integral of x^2 over [0,1]
    exact("Var U(0,1) = 1/3 - 1/4", e_u2 - e_u**2, Fraction(1, 12))

    print("Geometric and negative binomial dice (cards prob-dist-geometric-rolls-to-six, prob-dist-negative-binomial-three-sixes)")
    k = np.arange(1, 2000, dtype=float)
    pk = (5 / 6) ** (k - 1) / 6
    mean_g = float((k * pk).sum())
    var_g = float((k**2 * pk).sum()) - mean_g**2
    approx("rolls to first 6: mean", mean_g, 6, 6)
    approx("rolls to first 6: variance", var_g, 30, 6)
    kk = np.arange(3, 3000)
    pmf_nb = np.array([math.comb(int(x) - 1, 2) for x in kk], dtype=float) * (1 / 6) ** 3 * (5 / 6) ** (kk - 3.0)
    m_nb = float((kk * pmf_nb).sum())
    approx("rolls to third 6: mean", m_nb, 18, 6)
    approx("rolls to third 6: variance", float((kk**2 * pmf_nb).sum()) - m_nb**2, 90, 6)

    print("Chi-square moments (card prob-dist-chi-square-moments), by integration")
    approx("E[Z^2]", simpson(lambda x: x**2 * phi(x), -40, 40), 1, 9)
    approx("E[Z^4]", simpson(lambda x: x**4 * phi(x), -40, 40), 3, 9)


# ------------------------------------------------------------------ normal quantiles and tails


def normal_numbers() -> None:
    print("Normal table, Phi by Simpson integration of the density (TL;DR, table, card prob-dist-normal-quantiles)")
    rows = [
        (1, 0.8413, 0.6827, 0.1587, 4),
        (1.645, 0.9500, 0.9000, 0.0500, 4),
        (1.96, 0.9750, 0.9500, 0.0250, 4),
        (2, 0.9772, 0.9545, 0.0228, 4),
        (2.326, 0.9900, 0.9800, 0.0100, 4),
        (2.576, 0.9950, 0.9900, 0.0050, 4),
    ]
    for z, cdf, central, upper, dp in rows:
        c = normal_cdf(z)
        approx(f"Phi({z})", c, cdf, dp)
        approx(f"P(|Z| <= {z})", 2 * c - 1, central, dp)
        approx(f"1 - Phi({z})", 1 - c, upper, dp)
    c3 = normal_cdf(3)
    approx("Phi(3)", c3, 0.99865, 5)
    approx("P(|Z| <= 3)", 2 * c3 - 1, 0.9973, 4)
    approx("1 - Phi(3)", 1 - c3, 0.00135, 5)
    approx("P(|Z| <= 1) in %", 100 * (2 * normal_cdf(1) - 1), 68.3, 1)
    approx("P(|Z| <= 2) in %", 100 * (2 * normal_cdf(2) - 1), 95.4, 1)
    approx("P(|Z| <= 3) in %", 100 * (2 * c3 - 1), 99.73, 2)
    for p, q, dp in ((0.95, 1.645, 3), (0.975, 1.960, 3), (0.99, 2.326, 3), (0.995, 2.576, 3), (0.999, 3.09, 2)):
        approx(f"quantile {p}", normal_quantile(p), q, dp)
    approx("quantile 0.99 (2 dp, learning objective)", normal_quantile(0.99), 2.33, 2)

    print("3-sigma down day (card prob-dist-three-sigma-down-day)")
    tail = normal_cdf(-3)
    approx("P(Z < -3) in %", 100 * tail, 0.135, 3)
    approx("days between 3-sigma losses", 1 / tail, 741, 0)
    approx("in years of 252 days", 1 / tail / 252, 2.9, 1)


# ------------------------------------------------------------------ worked examples


def poisson_example() -> None:
    print("Example 1 - Poisson approximation (card prob-dist-poisson-limit-errors)")
    n, p = 1000, 0.001
    exact_at_least_one = 1 - (1 - p) ** n
    approx("exact 1 - 0.999^1000", exact_at_least_one, 0.6323, 4)
    approx("Poisson 1 - e^-1", 1 - math.exp(-1), 0.632, 3)
    approx("exact, 3 dp", exact_at_least_one, 0.632, 3)
    approx("Poisson P(exactly 2) = e^-1/2", math.exp(-1) / 2, 0.184, 3)
    binom = np.array([math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)])
    pois = np.array([math.exp(-1 - math.lgamma(k + 1)) for k in range(n + 1)])
    tv = 0.5 * float(np.abs(binom - pois).sum()) + 0.5 * (1 - float(pois.sum()))
    approx("exact Binomial P(exactly 2)", float(binom[2]), 0.184, 3)
    assert tv <= n * p * p, tv
    print(f"    total variation distance Bin(1000,0.001) vs Poisson(1) = {tv:.2e} <= Le Cam bound np^2 = {n * p * p:.0e}")
    approx("np^2 (Le Cam bound)", n * p * p, 0.001, 6)
    approx("total variation distance in units of 1e-4", tv * 1e4, 2.8, 1)


def exponential_examples(rng: np.random.Generator) -> None:
    print("Example 2 - exponential race (cards prob-dist-exponential-race-winner, prob-dist-exponential-max-expected)")
    m = 2_000_000
    buy = rng.exponential(1 / 2, m)
    sell = rng.exponential(1 / 1, m)
    simulated("P(next order is a buy)", float((buy < sell).mean()), 2 / 3, 0.002)
    simulated("E[time to next order]", float(np.minimum(buy, sell).mean()), 1 / 3, 0.002)
    simulated("E[time to see both]", float(np.maximum(buy, sell).mean()), 7 / 6, 0.004)
    first = np.minimum(buy, sell)
    simulated("E[wait | next is a buy] (independent of side)", float(first[buy < sell].mean()), 1 / 3, 0.002)
    simulated("E[wait | next is a sell] (independent of side)", float(first[buy >= sell].mean()), 1 / 3, 0.002)
    e_max = simpson(lambda x: 1 - (1 - np.exp(-2 * x)) * (1 - np.exp(-x)), 0.0, 60.0, 200_000)
    approx("E[max] by integrating the survival function", e_max, 7 / 6, 9)
    exact("1/2 + 1 - 1/3", Fraction(1, 2) + 1 - Fraction(1, 3), Fraction(7, 6))
    exact("memoryless route 1/3 + (2/3)(1) + (1/3)(1/2)", Fraction(1, 3) + Fraction(2, 3) + Fraction(1, 6), Fraction(7, 6))

    print("Memoryless bus (card prob-dist-exponential-memoryless-bus)")
    gaps = rng.exponential(10.0, m)
    simulated("E[X - 10 | X > 10], mean-10 exponential", float((gaps[gaps > 10] - 10).mean()), 10.0, 0.06)

    print("Inverse transform (card prob-dist-probability-integral-transform)")
    u = rng.random(m)
    x = -np.log(u) / 2.5
    simulated("mean of -ln(U)/2.5", float(x.mean()), 0.4, 0.002)
    simulated("P(-ln(U)/2.5 > 1) vs e^-2.5", float((x > 1).mean()), math.exp(-2.5), 0.001)


def lognormal_examples(rng: np.random.Generator) -> None:
    print("Example 3 - lognormal mean versus median")
    sigma = 0.2
    approx("log-mean -sigma^2/2", -(sigma**2) / 2, -0.02, 2)
    approx("log-variance sigma^2", sigma**2, 0.04, 2)
    approx("P(S1 > S0) = Phi(-0.1)", normal_cdf(-0.1), 0.460, 3)
    approx("median / S0 = e^-0.02", math.exp(-0.02), 0.980, 3)
    z = rng.standard_normal(2_000_000)
    s1 = np.exp(-(sigma**2) / 2 + sigma * z)
    simulated("E[S1/S0], simulated", float(s1.mean()), 1.0, 0.002)
    simulated("P(S1 > S0), simulated", float((s1 > 1).mean()), 0.460, 0.002)
    simulated("median S1/S0, simulated", float(np.median(s1)), 0.980, 0.002)

    print("Lognormal with ln X ~ N(0,1) (card prob-dist-lognormal-mean-median)")
    approx("E[e^Z] by integration", simpson(lambda x: np.exp(x) * phi(x), -40, 40), 1.649, 3)
    approx("median of e^Z", math.exp(normal_quantile(0.5)), 1.0, 6)


def beta_binomial(rng: np.random.Generator) -> None:
    print("Example 4 - Beta-binomial with a uniform prior (card prob-dist-beta-binomial-uniform-count)")

    def integral_p_power(a: int, b: int) -> Fraction:
        return sum((Fraction((-1) ** j * math.comb(b, j), a + j + 1) for j in range(b + 1)), Fraction(0))

    for n in range(1, 11):
        for k in range(n + 1):
            assert math.comb(n, k) * integral_p_power(k, n - k) == Fraction(1, n + 1), (n, k)
    print("    C(n,k) * integral p^k (1-p)^(n-k) dp = 1/(n+1) for all k <= n <= 10 (exact)")
    n = 5
    pts = rng.random((400_000, n + 1))
    heads = (pts[:, 1:] < pts[:, :1]).sum(axis=1)
    freq = np.bincount(heads, minlength=n + 1) / len(heads)
    assert np.all(np.abs(freq - 1 / (n + 1)) < 0.003), freq
    print(f"    billiard-ball simulation, n=5: frequencies {np.round(freq, 4).tolist()} all within 0.003 of 1/6")


def poisson_relations(rng: np.random.Generator) -> None:
    print("Thinning (card prob-dist-poisson-thinning-buys)")
    approx("P(no buys) = e^-3", math.exp(-3), 0.050, 3)
    total = rng.poisson(10, 1_000_000)
    buys = rng.binomial(total, 0.3)
    sells = total - buys
    simulated("P(no buys), simulated by thinning", float((buys == 0).mean()), 0.050, 0.001)
    simulated("corr(buys, sells), simulated", float(np.corrcoef(buys, sells)[0, 1]), 0.0, 0.004)
    simulated("mean of buys", float(buys.mean()), 3.0, 0.01)
    simulated("variance of buys", float(buys.var()), 3.0, 0.02)

    print("Poisson split given the total (card prob-dist-poisson-given-total)")

    def pois(lam: float, k: int) -> float:
        return math.exp(-lam) * lam**k / math.factorial(k)

    ratio = pois(2, 3) * pois(1, 0) / pois(3, 3)
    approx("P(all 3 orders are buys | 3 orders)", ratio, 8 / 27, 12)
    exact("(2/3)^3", Fraction(2, 3) ** 3, Fraction(8, 27))
    approx("8/27", 8 / 27, 0.296, 3)
    b = rng.poisson(2, 2_000_000)
    s = rng.poisson(1, 2_000_000)
    three = (b + s) == 3
    simulated("P(all buys | 3 orders), simulated", float((b[three] == 3).mean()), 8 / 27, 0.003)


def main() -> None:
    rng = np.random.default_rng(SEED)
    table_moments()
    normal_numbers()
    poisson_example()
    exponential_examples(rng)
    lognormal_examples(rng)
    beta_binomial(rng)
    poisson_relations(rng)
    print("All distribution checks passed.")


if __name__ == "__main__":
    main()
