"""Research process and hypothesis discipline: every base rate, power and selection-bias number in the note.

Backs every number in `09-Alpha-Research-and-Portfolio/01-Research-Process-and-Hypothesis-Discipline.md`.
Independent routes used here:
- positive predictive values by counting ideas in a population of 10,000 with `fractions.Fraction`,
  and power at t > 3 by seeded simulation of non-central test statistics, against the closed form;
- years to significance and power by seeded simulation of daily iid return paths, against (c/S)^2;
- the expected maximum of N standard normals by quadrature of N x Phi^(N-1) phi and by simulation,
  against the Euler-Mascheroni approximation of Bailey and Lopez de Prado (2014);
- the six-month kill test by seeded simulation of realised Sharpe ratios of daily returns.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 09-Alpha-Research-and-Portfolio/code/alpha_01_research_process.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction
from statistics import NormalDist

import numpy as np

SEED = 20261114
N01 = NormalDist()
EULER_GAMMA = 0.5772156649015329


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def bracket(n: int) -> float:
    """Bailey-Lopez de Prado approximation to E[max of n iid N(0,1)]."""
    return (1 - EULER_GAMMA) * N01.inv_cdf(1 - 1 / n) + EULER_GAMMA * N01.inv_cdf(1 - 1 / (n * math.e))


def expected_max_quadrature(n: int) -> float:
    """E[max of n iid N(0,1)] = int x n Phi(x)^(n-1) phi(x) dx by Simpson's rule on [-12, 12]."""
    x = np.linspace(-12.0, 12.0, 24001)
    phi = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    cdf = np.array([N01.cdf(v) for v in x])
    y = x * n * cdf ** (n - 1) * phi
    h = x[1] - x[0]
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


def base_rates(rng: np.random.Generator) -> None:
    print("Base rates (worked example 1, TL;DR, card alpha-research-ppv)")
    ideas = 10_000
    real = ideas // 10
    true_pos = Fraction(real) * Fraction(8, 10)
    false_pos = Fraction(ideas - real) * Fraction(5, 100)
    ppv = true_pos / (true_pos + false_pos)
    exact("true positives per idea", true_pos / ideas, Fraction(8, 100))
    exact("false positives per idea", false_pos / ideas, Fraction(45, 1000))
    exact("all positives per idea", (true_pos + false_pos) / ideas, Fraction(125, 1000))
    exact("PPV at t > 1.96", ppv, Fraction(64, 100))
    approx("false discovery share at t > 1.96 (%)", float(1 - ppv) * 100, 36, 0)

    alpha3 = 2 * (1 - N01.cdf(3.0))
    approx("two-sided alpha at t > 3", alpha3, 0.0027, 4)
    z_power = N01.inv_cdf(0.8)
    approx("z for 80% power", z_power, 0.8416, 4)
    delta = 1.96 + z_power
    approx("non-centrality", delta, 2.80, 2)
    power3 = N01.cdf(delta - 3) + N01.cdf(-delta - 3)
    approx("power at t > 3", power3, 0.421, 3)
    t = rng.standard_normal(2_000_000) + delta
    sim_power = float(np.mean(np.abs(t) > 3))
    se = math.sqrt(power3 * (1 - power3) / t.size)
    simulated("power at t > 3, simulated", sim_power, 0.421, 4 * se + 0.0005)
    approx("true positives per idea at t > 3 (card)", 0.1 * power3, 0.0421, 4)
    ppv3 = 0.1 * power3 / (0.1 * power3 + 0.9 * alpha3)
    approx("PPV at t > 3", ppv3, 0.945, 3)
    approx("false discovery share at t > 3 (%)", (1 - ppv3) * 100, 5.5, 1)
    approx("false discovery share at t > 3, TL;DR 'about 5%' (%)", (1 - ppv3) * 100, 5, 0)
    # the population count route for t > 3 must agree with the formula
    pop = (real * power3) / (real * power3 + (ideas - real) * alpha3)
    assert abs(pop - ppv3) < 1e-12


def years_needed(rng: np.random.Generator) -> None:
    print("Years to significance (worked example 2, TL;DR, card alpha-research-years-to-significance)")
    approx("years to t = 2 at S = 0.8", (2 / 0.8) ** 2, 6.25, 2)
    approx("years to t = 2 at S = 0.8, TL;DR 'about 6'", (2 / 0.8) ** 2, 6, 0)
    z95, z975, z80 = N01.inv_cdf(0.95), N01.inv_cdf(0.975), N01.inv_cdf(0.8)
    approx("z_0.95", z95, 1.645, 3)
    approx("z_0.80", z80, 0.842, 3)
    y_one = ((z95 + z80) / 0.8) ** 2
    y_two = ((z975 + z80) / 0.8) ** 2
    approx("years for 80% power, one-sided 5%", y_one, 9.7, 1)
    approx("years for 80% power, two-sided 5%", y_two, 12.3, 1)
    approx("years for 80% power, two-sided 5%, TL;DR 'about 12'", y_two, 12, 0)
    approx("S = 2, one-sided 80% power (years)", ((z95 + z80) / 2) ** 2, 1.5, 1)
    approx("S = 2, two-sided 80% power (years)", ((z975 + z80) / 2) ** 2, 2.0, 1)
    approx("years to t = 2 at S = 0.5", (2 / 0.5) ** 2, 16, 0)

    # simulate daily iid returns with annual Sharpe 0.8 and check the t-stat of the mean
    paths, days_per_year = 20_000, 252
    sd = 0.01
    mu = 0.8 / math.sqrt(days_per_year) * sd
    for years, target, kind in ((6.25, 2.0, "mean t"), (y_two, 0.8, "power")):
        n = int(round(years * days_per_year))
        s1 = np.zeros(paths)
        s2 = np.zeros(paths)
        for start in range(0, n, 252):
            chunk = rng.normal(mu, sd, (paths, min(252, n - start)))
            s1 += chunk.sum(axis=1)
            s2 += (chunk * chunk).sum(axis=1)
        mean = s1 / n
        var = (s2 - n * mean * mean) / (n - 1)
        tstat = mean / np.sqrt(var / n)
        if kind == "mean t":
            simulated(f"mean t-stat after {years} years at S = 0.8", float(tstat.mean()), target, 4 / math.sqrt(paths) + 0.01)
        else:
            p = float(np.mean(tstat > z975))
            simulated(f"power after {years:.2f} years, two-sided 5%", p, target, 4 * math.sqrt(0.16 / paths) + 0.005)


def selection(rng: np.random.Generator) -> None:
    print("Best of N zero-skill strategies (core concepts, worked example 3, card alpha-research-expected-max-sharpe)")
    approx("Euler-Mascheroni gamma", EULER_GAMMA, 0.5772, 4)
    for n, quoted in ((10, 1.57), (50, 2.28), (100, 2.53)):
        approx(f"bracket for N = {n}", bracket(n), quoted, 2)
    approx("bracket for N = 50 (3 dp)", bracket(50), 2.276, 3)
    approx("E[max of 50 N(0,1)] by quadrature", expected_max_quadrature(50), 2.25, 2)
    draws = rng.standard_normal((200_000, 50)).max(axis=1)
    simulated("E[max of 50 N(0,1)] by simulation", float(draws.mean()), 2.25, 4 * draws.std() / math.sqrt(draws.size) + 0.005)
    approx("bracket overstatement of the exact E[max of 50] (%)", (bracket(50) / expected_max_quadrature(50) - 1) * 100, 1, 0)
    approx("SE of annualised Sharpe over 5 years", math.sqrt(1 / 5), 0.447, 3)
    approx("expected best Sharpe (bracket route)", bracket(50) * math.sqrt(1 / 5), 1.02, 2)
    approx("card: 2.28 x 0.447", 2.28 * 0.447, 1.02, 2)
    approx("expected best Sharpe, card 'about 1.0'", expected_max_quadrature(50) / math.sqrt(5), 1.0, 1)

    # the note's snippet, run exactly as printed
    snip = np.random.default_rng(0)
    years, n_trials, n_sims = 5, 50, 20_000
    sr_hat = snip.standard_normal((n_sims, n_trials)) / np.sqrt(years)
    approx("note snippet output (seed 0)", float(sr_hat.max(axis=1).mean()), 1.01, 2)


def kill_test(rng: np.random.Generator) -> None:
    print("Six bad months (worked example 4, card alpha-research-kill-six-months)")
    se6 = math.sqrt(1 / 0.5)
    approx("SE of 6-month annualised Sharpe", se6, 1.41, 2)
    z = (-0.5 - 1.0) / se6
    approx("z", z, -1.06, 2)
    approx("one-sided p", N01.cdf(z), 0.144, 3)
    approx("one-sided p, card", N01.cdf(z), 0.14, 2)
    approx("P(negative 6-month Sharpe | true Sharpe 1)", N01.cdf(-1.0 / se6), 0.24, 2)
    z2 = -1.5 / math.sqrt(1 / 2)
    approx("SE of 2-year Sharpe", math.sqrt(1 / 2), 0.707, 3)
    approx("z after 2 years", z2, -2.12, 2)
    approx("p after 2 years", N01.cdf(z2), 0.017, 3)

    # simulate 126 daily returns with annual Sharpe 1 and look at the realised annualised Sharpe
    paths, n = 400_000, 126
    sd = 0.01
    r = rng.normal(1.0 / math.sqrt(252) * sd, sd, (paths, n))
    sr = r.mean(axis=1) / r.std(axis=1, ddof=1) * math.sqrt(252)
    p_neg = float(np.mean(sr < 0))
    simulated("P(realised 6-month Sharpe < 0), simulated", p_neg, 0.24, 4 * math.sqrt(0.24 * 0.76 / paths) + 0.005)
    p_low = float(np.mean(sr <= -0.5))
    simulated("P(realised 6-month Sharpe <= -0.5), simulated", p_low, 0.144, 4 * math.sqrt(0.144 * 0.856 / paths) + 0.005)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    base_rates(rng)
    years_needed(rng)
    selection(rng)
    kill_test(rng)
    print("All research-process numbers check.")
