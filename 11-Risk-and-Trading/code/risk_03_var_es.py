"""Value at Risk and expected shortfall: every number in the note.

Backs every number in `11-Risk-and-Trading/03-VaR-and-Expected-Shortfall.md`.
Independent routes used here:
- normal quantiles by bisection on erfc, cross-checked by Simpson integration of the density; no quantile is recalled;
- normal and Student-t(4) ES by the closed forms against Simpson quadrature of the tail integral and seeded simulation;
- Student-t(4) quantiles by bisection on a Simpson-integrated CDF, cross-checked by seeded simulation;
- the two-position and component VaR by exact rational covariance algebra and by numerical differentiation (Euler);
- historical VaR and ES by applying the inf-quantile and integral-ES definitions to a 500-scenario loss vector;
- the two-bond subadditivity example by exact enumeration of the four default states with fractions;
- the Kupiec and traffic-light probabilities by exact binomial sums, with the chi-square tail by simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 11-Risk-and-Trading/code/risk_03_var_es.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np

SEED = 20261114


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


def simpson(fn, a: float, b: float, n: int = 20_000) -> float:
    n += n % 2
    x = np.linspace(a, b, n + 1)
    y = fn(x)
    h = (b - a) / n
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


def bisect(fn, target: float, lo: float, hi: float) -> float:
    for _ in range(200):
        mid = (lo + hi) / 2
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def norm_pdf(x):
    return np.exp(-0.5 * np.asarray(x) ** 2) / math.sqrt(2 * math.pi)


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2))


def norm_ppf(p: float) -> float:
    return bisect(norm_cdf, p, -12.0, 12.0)


def t4_pdf(t):
    return 0.375 * (1 + np.asarray(t) ** 2 / 4) ** -2.5  # Gamma(5/2) / (sqrt(4 pi) Gamma(2)) = 3/8


def t4_cdf_closed(t: float) -> float:
    """Closed-form CDF of Student-t with 4 degrees of freedom; its derivative is 12/(t^2+4)^(5/2), the density."""
    return 0.5 + t * (t * t + 6) / (2 * (t * t + 4) ** 1.5)


def t4_cdf_simpson(t: float) -> float:
    return 0.5 + simpson(t4_pdf, 0.0, t, 4000)


def t4_tail_mean_simpson(q: float) -> float:
    """int_q^inf x f(x) dx by the substitution x = q/u; the integrand is O(u^2) near 0, so (0, 1e-4) adds under 1e-12."""

    def integrand(u):
        x = q / u
        return x * t4_pdf(x) * q / u**2

    return simpson(integrand, 1e-4, 1.0)


# ------------------------------------------------------------------ sections


def normal_table(rng: np.random.Generator) -> dict[float, float]:
    print("Normal VaR and ES multiples (TL;DR, table, card risk-var-normal-multipliers)")
    z = {}
    sample = rng.standard_normal(4_000_000)
    for level, z_quoted, es_quoted in [(0.95, 1.645, 2.063), (0.975, 1.960, 2.338), (0.99, 2.326, 2.665)]:
        z[level] = norm_ppf(level)
        approx(f"z_{level} by bisection on erfc", z[level], z_quoted, 3)
        approx(f"Phi(z_{level}) by Simpson integration of the density", 0.5 + simpson(norm_pdf, 0.0, z[level]), level, 9)
        es_closed = float(norm_pdf(z[level])) / (1 - level)
        es_quad = simpson(lambda x: x * norm_pdf(x), z[level], z[level] + 40.0) / (1 - level)
        approx(f"ES multiple at {level}, closed form", es_closed, es_quoted, 3)
        approx(f"ES multiple at {level}, quadrature", es_quad, es_quoted, 3)
        tail = sample[sample >= z[level]]
        simulated(
            f"ES multiple at {level}, simulated", float(tail.mean()), es_quoted, 5 * float(tail.std()) / math.sqrt(len(tail)) + 0.0005
        )
    approx("z_0.99 to four decimals", z[0.99], 2.3263, 4)
    approx("phi(z_0.99)", float(norm_pdf(z[0.99])), 0.02665, 5)
    z999 = norm_ppf(0.999)
    approx("z_0.999", z999, 3.09, 2)
    approx("z_0.999 to three decimals", z999, 3.090, 3)
    return z


def t4_tails(rng: np.random.Generator, z: dict[float, float]) -> None:
    print("Student-t(4) rescaled to unit variance (fat tails section, Example 6, card risk-var-fat-tails)")
    scale = math.sqrt(2.0)  # Var of t_4 is 4/(4-2) = 2
    sample = rng.standard_t(4, size=4_000_000) / scale
    for t in (0.5, 1.0, 2.0, 5.0):
        assert abs(t4_cdf_closed(t) - t4_cdf_simpson(t)) < 1e-10, t
        assert abs(12 / (t * t + 4) ** 2.5 - float(t4_pdf(t))) < 1e-15, t
    out = {}
    for level, var_quoted, var_dec in [(0.99, 2.649, 3), (0.999, 5.07, 2)]:
        q_t = bisect(t4_cdf_simpson, level, 0.0, 50.0)
        q_closed_check = t4_cdf_simpson(q_t)
        assert abs(q_closed_check - level) < 1e-10
        q = q_t / scale
        approx(f"t4 unit-variance VaR at {level}, bisection on Simpson CDF", q, var_quoted, var_dec)
        approx(
            f"t4 unit-variance VaR at {level}, bisection on the closed-form CDF",
            bisect(t4_cdf_closed, level, 0.0, 50.0) / scale,
            var_quoted,
            var_dec,
        )
        q_sim = float(np.quantile(sample, level))
        se_q = math.sqrt(level * (1 - level) / len(sample)) / (float(t4_pdf(q_t)) * scale)
        simulated(f"t4 unit-variance VaR at {level}, simulated", q_sim, var_quoted, 5 * se_q + 0.5 * 10.0**-var_dec)
        out[level] = (q_t, q)
    q_t, q = out[0.99]
    es_closed = float(t4_pdf(q_t)) * (4 + q_t**2) / ((4 - 1) * 0.01) / scale
    es_quad = t4_tail_mean_simpson(q_t) / 0.01 / scale
    approx("t4 unit-variance ES at 0.99, closed form", es_closed, 3.692, 3)
    approx("t4 unit-variance ES at 0.99, quadrature", es_quad, 3.692, 3)
    tail = sample[sample >= q]
    simulated("t4 unit-variance ES at 0.99, simulated", float(tail.mean()), 3.692, 5 * float(tail.std()) / math.sqrt(len(tail)) + 0.005)
    q975_t = bisect(t4_cdf_simpson, 0.975, 0.0, 50.0)
    es975_closed = float(t4_pdf(q975_t)) * (4 + q975_t**2) / (3 * 0.025) / scale
    approx("t4 unit-variance ES at 0.975, closed form", es975_closed, 2.824, 3)
    approx("t4 unit-variance ES at 0.975, quadrature", t4_tail_mean_simpson(q975_t) / 0.025 / scale, 2.824, 3)
    tail975 = sample[sample >= q975_t / scale]
    se975 = 5 * float(tail975.std()) / math.sqrt(len(tail975)) + 0.0005
    simulated("t4 unit-variance ES at 0.975, simulated", float(tail975.mean()), 2.824, se975)
    es_norm = float(norm_pdf(z[0.99])) / 0.01
    print("  Example 6, book volatility 1m")
    approx("normal 99% VaR (m)", z[0.99], 2.33, 2)
    approx("normal 99% ES (m)", es_norm, 2.67, 2)
    approx("normal 99.9% VaR (m)", norm_ppf(0.999), 3.09, 2)
    approx("t4 99% VaR (m)", q, 2.65, 2)
    approx("t4 99% ES (m)", es_closed, 3.69, 2)
    approx("t4 99.9% VaR (m)", out[0.999][1], 5.07, 2)
    approx("VaR ratio minus 1 (percent)", 100 * (q / z[0.99] - 1), 14, 0)
    approx("ES ratio minus 1 (percent)", 100 * (es_closed / es_norm - 1), 39, 0)


def parametric(z: dict[float, float]) -> None:
    print("Example 1: parametric VaR and ES (card risk-var-parametric-calc)")
    sd = 10e6 * 0.015
    approx("sigma_P", sd, 150_000, 6)
    es_mult = float(norm_pdf(z[0.99])) / 0.01
    approx("99% one-day VaR, to the nearest 1,000", round(z[0.99] * sd, -3), 349_000, 0)
    approx("99% one-day ES, to the nearest 1,000", round(es_mult * sd, -3), 400_000, 0)
    approx("ten-day VaR by the square-root rule (m)", z[0.99] * sd * math.sqrt(10) / 1e6, 1.10, 2)

    print("Example 2: two positions and component VaR (card risk-var-component)")
    w = [Fraction(6_000_000), Fraction(4_000_000)]
    vol = [Fraction(2, 100), Fraction(1, 100)]
    rho = Fraction(3, 10)
    cov = [[vol[0] ** 2, rho * vol[0] * vol[1]], [rho * vol[0] * vol[1], vol[1] ** 2]]
    cw = [sum(cov[i][j] * w[j] for j in range(2)) for i in range(2)]
    var_p = sum(w[i] * cw[i] for i in range(2))
    exact("sigma_P^2 (exact)", var_p, Fraction(18_880_000_000))
    exact("dollar volatilities", (w[0] * vol[0], w[1] * vol[1]), (Fraction(120_000), Fraction(40_000)))
    sd_p = math.sqrt(var_p)
    approx("sigma_P to the nearest 100", round(sd_p, -2), 137_400, 0)
    approx("sigma_P unrounded", sd_p, 137_405, 0)
    approx("z_0.99 to five decimals", z[0.99], 2.32635, 5)
    approx("2.32635 x 137,405 to the nearest 100", round(2.32635 * 137_405, -2), 319_700, 0)
    approx("2.326 x 137,400 to the nearest 100", round(2.326 * 137_400, -2), 319_600, 0)
    total = z[0.99] * sd_p
    approx("99% VaR to the nearest 100", round(total, -2), 319_700, 0)
    stand = [z[0.99] * float(w[i] * vol[i]) for i in range(2)]
    approx("standalone VaR 1", round(stand[0], -2), 279_200, 0)
    approx("standalone VaR 2", round(stand[1], -2), 93_100, 0)
    approx("sum of standalone VaRs", round(sum(stand), -2), 372_200, 0)
    approx("diversification benefit", round(sum(stand) - total, -2), 52_600, 0)

    def port_var(w1: float, w2: float) -> float:
        return z[0.99] * math.sqrt(float(cov[0][0]) * w1 * w1 + 2 * float(cov[0][1]) * w1 * w2 + float(cov[1][1]) * w2 * w2)

    h = 1.0
    w1, w2 = float(w[0]), float(w[1])
    comp = [w1 * (port_var(w1 + h, w2) - port_var(w1 - h, w2)) / (2 * h), w2 * (port_var(w1, w2 + h) - port_var(w1, w2 - h)) / (2 * h)]
    approx("component VaR 1 by numerical differentiation", round(comp[0], -2), 268_200, 0)
    approx("component VaR 2 by numerical differentiation", round(comp[1], -2), 51_500, 0)
    approx("component VaR 1 by the Euler formula", z[0.99] * float(w[0] * cw[0]) / sd_p, 268_182, 0)
    approx("component VaR 2 by the Euler formula", z[0.99] * float(w[1] * cw[1]) / sd_p, 51_469, 0)
    approx("VaR, unrounded", total, 319_651, 0)
    approx("components sum to the total", round(sum(comp), -2), 319_700, 0)
    approx("share of position 1 (percent)", 100 * comp[0] / total, 84, 0)


def historical(rng: np.random.Generator) -> None:
    print("Example 3: historical VaR and ES (card risk-var-historical-es)")
    worst = [4.1, 3.6, 3.2, 2.9, 2.7, 2.5]
    others = rng.uniform(-3.0, 2.4, size=494)  # hypothetical rest of the window, all below the 6th worst
    losses = np.sort(np.concatenate([others, worst]))
    n = len(losses)
    exact("scenarios", n, 500)
    exact("tail scenarios at 1%", round(n * 0.01), 5)
    # VaR_alpha = inf{l : P(L <= l) >= alpha} on the empirical distribution
    var_inf = min(x for x in losses if np.count_nonzero(losses <= x) / n >= 0.99)
    approx("99% VaR by the inf definition (6th worst)", var_inf, 2.5, 12)
    approx("5th worst loss", losses[-5], 2.7, 12)
    # ES_alpha = (1/(1-alpha)) int_alpha^1 VaR_u du with the empirical quantile, exactly on a grid of u-intervals
    es = Fraction(0)
    for k in range(n):
        lo, hi = Fraction(k, n), Fraction(k + 1, n)  # VaR_u equals the (k+1)th smallest loss for u in (k/n, (k+1)/n]
        lo = max(lo, Fraction(99, 100))
        if hi > lo:
            es += (hi - lo) * Fraction(str(losses[k]))
    es /= Fraction(1, 100)
    approx("99% ES by the integral definition", float(es), 3.3, 12)
    approx("mean of the five worst", sum(worst[:5]) / 5, 3.3, 12)


def subadditivity() -> None:
    print("Example 4: VaR is not subadditive (card risk-var-not-subadditive)")
    pd = Fraction(4, 100)

    def var_es(dist: dict[int, Fraction], alpha: Fraction) -> tuple[int, Fraction]:
        support = sorted(dist)
        cum, var = Fraction(0), None
        for x in support:
            cum += dist[x]
            if cum >= alpha:
                var = x
                break
        # integral ES: average of the quantile function over (alpha, 1]
        es, upper = Fraction(0), Fraction(1)
        for x in reversed(support):
            lower = max(upper - dist[x], alpha)
            if upper > lower:
                es += (upper - lower) * x
            upper -= dist[x]
            if upper <= alpha:
                break
        return var, es / (1 - alpha)

    alpha = Fraction(95, 100)
    single = {0: 1 - pd, 100: pd}
    pair: dict[int, Fraction] = {}
    for d1, d2 in itertools.product((0, 1), repeat=2):
        p = (pd if d1 else 1 - pd) * (pd if d2 else 1 - pd)
        pair[100 * (d1 + d2)] = pair.get(100 * (d1 + d2), Fraction(0)) + p
    exact("pair loss distribution", pair, {0: Fraction(576, 625), 100: Fraction(48, 625), 200: Fraction(1, 625)})
    approx("P(L >= 100) for the pair (percent)", float(100 * (pair[100] + pair[200])), 7.84, 2)
    approx("P(L = 200) (percent)", float(100 * pair[200]), 0.16, 2)
    approx("P(L = 100) (percent)", float(100 * pair[100]), 7.68, 2)
    v1, e1 = var_es(single, alpha)
    v2, e2 = var_es(pair, alpha)
    exact("95% VaR of one bond", v1, 0)
    exact("95% VaR of the pair", v2, 100)
    exact("95% ES of one bond", e1, Fraction(80))
    exact("95% ES of the pair", e2, Fraction(516, 5))
    approx("95% ES of the pair", float(e2), 103.2, 1)
    exact(
        "(0.0016 x 200 + 0.0484 x 100)/0.05", (Fraction(16, 10000) * 200 + Fraction(484, 10000) * 100) / Fraction(5, 100), Fraction(516, 5)
    )
    assert e2 <= 2 * e1
    # the naive tail conditional expectation E[L | L >= VaR] is not subadditive on the same example
    tce1 = sum(x * p for x, p in single.items() if x >= v1) / sum(p for x, p in single.items() if x >= v1)
    tce2 = sum(x * p for x, p in pair.items() if x >= v2) / sum(p for x, p in pair.items() if x >= v2)
    exact("E[L | L >= VaR] for one bond", tce1, Fraction(4))
    approx("E[L | L >= VaR] for the pair", float(tce2), 102.0, 1)
    assert tce2 > 2 * tce1


def backtesting(rng: np.random.Generator, z: dict[float, float]) -> None:
    print("Example 5 and traffic light: backtesting (cards risk-var-kupiec, risk-var-traffic-light)")
    t_days, p = 250, Fraction(1, 100)
    pmf = [math.comb(t_days, k) * p**k * (1 - p) ** (t_days - k) for k in range(t_days + 1)]
    approx("expected exceptions", float(t_days * p), 2.5, 12)
    approx("P(X >= 8) (percent)", float(100 * sum(pmf[8:])), 0.40, 2)
    approx("P(X <= 4) (percent)", float(100 * sum(pmf[:5])), 89, 0)
    approx("P(X <= 4) (percent, Basel 1996 table)", float(100 * sum(pmf[:5])), 89.22, 2)
    approx("P(X <= 9) (percent)", float(100 * sum(pmf[:10])), 99.97, 2)
    x, pf = 8, 0.01
    ph = x / t_days
    approx("p_hat", ph, 0.032, 12)
    lr = -2 * ((t_days - x) * math.log(1 - pf) + x * math.log(pf) - (t_days - x) * math.log(1 - ph) - x * math.log(ph))
    approx("LR_POF", lr, 7.73, 2)
    approx("LR_POF (card)", lr, 7.7, 1)
    crit = norm_ppf(0.975) ** 2
    approx("5% critical value of chi-square(1) = z_0.975^2", crit, 3.84, 2)
    p_value = math.erfc(math.sqrt(lr / 2))
    approx("p-value", p_value, 0.005, 3)
    chi = rng.standard_normal(4_000_000) ** 2
    se = math.sqrt(p_value * (1 - p_value) / len(chi))
    simulated("p-value, simulated chi-square(1) tail", float((chi > lr).mean()), round(p_value, 4), 5 * se + 0.00005)
    chi_pdf = math.exp(-crit / 2) / math.sqrt(2 * math.pi * crit)
    se_q = math.sqrt(0.05 * 0.95 / len(chi)) / chi_pdf
    simulated("critical value, simulated chi-square(1) quantile", float(np.quantile(chi, 0.95)), 3.84, 5 * se_q + 0.005)
    assert 5 <= x <= 9
    print("    8 exceptions is in the yellow zone (5 to 9)")


def main() -> None:
    rng = np.random.default_rng(SEED)
    z = normal_table(rng)
    t4_tails(rng, z)
    parametric(z)
    historical(rng)
    subadditivity()
    backtesting(rng, z)
    approx("tail observations at 99% in 500 days", 500 * 0.01, 5, 12)
    print("All VaR and ES numbers check.")


if __name__ == "__main__":
    main()
