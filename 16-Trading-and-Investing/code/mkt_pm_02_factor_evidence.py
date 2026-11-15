"""Factor investing evidence: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Portfolio-Management/02-Factor-Investing-Evidence-Replication-and-Decay.md`.
Independent routes used here:
- normal tail probabilities from math.erfc, against composite Simpson integration of the normal density,
  and the expected count of false discoveries against a seeded simulation of 1,000 null t-statistics;
- the Bonferroni cutoff for 316 tests by bisection on the erfc tail, checked by integrating the density back;
- McLean and Pontiff (2016) percentage declines from their published coefficients and in-sample mean;
- the Student-t p-value for the hypothetical regression by Simpson integration of the t density
  (log-gamma normalisation), against a seeded simulation of Z / sqrt(chi2 / df);
- the value-momentum combination Sharpe ratio from the closed form, against a seeded simulation
  of correlated factor returns.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_pm_02_factor_evidence.py
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261114


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:64s} {float(value):16.6f}  quoted {quoted}")
    assert abs(float(value) - float(quoted)) <= tol, f"{label}: {float(value)} does not round to {quoted}"
    return float(value)


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:58s} |diff| = {abs(a - b):.2e} (tol {tol:.1e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def simpson(f, a: float, b: float, n: int = 20_000) -> float:
    if n % 2:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


def normal_two_sided(z: float) -> float:
    return math.erfc(z / math.sqrt(2))


def normal_two_sided_quad(z: float) -> float:
    return 1.0 - 2.0 * simpson(lambda x: np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi), 0.0, z)


def multiple_testing() -> None:
    print("Multiple testing thresholds (two-sided normal tails)")
    for z, quoted in ((1.96, "0.0500"), (2.0, "0.0455"), (3.0, "0.0027")):
        close(f"erfc vs Simpson at |t| = {z}", normal_two_sided(z), normal_two_sided_quad(z), 1e-10)
        q(f"two-sided p-value at |t| = {z}", normal_two_sided(z), quoted)
    q("expected false discoveries in 1,000 null tests at |t| > 1.96", 1000 * normal_two_sided(1.96), "50.0")
    q("expected false discoveries in 1,000 null tests at |t| > 2", 1000 * normal_two_sided(2.0), "45.5")
    rng = np.random.default_rng(SEED)
    reps = 4000
    counts = (np.abs(rng.standard_normal((reps, 1000))) > 2.0).sum(axis=1)
    se = counts.std(ddof=1) / math.sqrt(reps)
    close("simulated false discoveries at |t| > 2 (5 standard errors)", counts.mean(), 1000 * normal_two_sided(2.0), 5 * se)
    target = 0.05 / 316
    lo, hi = 2.0, 6.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if normal_two_sided(mid) > target:
            lo = mid
        else:
            hi = mid
    cut = 0.5 * (lo + hi)
    close("Bonferroni cutoff tail by Simpson", normal_two_sided_quad(cut), target, 1e-9)
    q("Bonferroni per-test level 0.05 / 316", target, "0.000158")
    q("Bonferroni |t| cutoff for 316 tests", cut, "3.78")


def mclean_pontiff() -> None:
    print("McLean and Pontiff (2016): in-sample mean 0.582% a month; coefficients -0.150 and -0.337")
    post_sample = q("post-sample decline 0.150 / 0.582 (%)", 100 * 0.150 / 0.582, "26")
    post_pub = q("post-publication decline 0.337 / 0.582 (%)", 100 * 0.337 / 0.582, "58")
    q("publication-informed trading, post-publication minus post-sample (pp)", post_pub - post_sample, "32")


def log_t_density(x: np.ndarray, df: int) -> np.ndarray:
    c = math.lgamma((df + 1) / 2) - math.lgamma(df / 2) - 0.5 * math.log(df * math.pi)
    return c - (df + 1) / 2 * np.log1p(x * x / df)


def regression_table() -> None:
    print("Hypothetical Fama-French three-factor regression, 60 months, 4 coefficients")
    for label, coef, se, quoted in (
        ("alpha t-stat 0.25 / 0.08", 0.25, 0.08, "3.125"),
        ("market t-stat 0.850 / 0.035", 0.850, 0.035, "24.29"),
        ("SMB t-stat 0.420 / 0.060", 0.420, 0.060, "7.00"),
        ("HML t-stat -0.310 / 0.055", -0.310, 0.055, "-5.64"),
    ):
        q(label, coef / se, quoted)
    df = 60 - 4
    t = 0.25 / 0.08
    p_quad = 1.0 - 2.0 * simpson(lambda x: np.exp(log_t_density(x, df)), 0.0, t)
    rng = np.random.default_rng(SEED + 1)
    n = 4_000_000
    draws = rng.standard_normal(n) / np.sqrt(rng.chisquare(df, n) / df)
    hits = np.abs(draws) > t
    p_sim = hits.mean()
    se = math.sqrt(p_sim * (1 - p_sim) / n)
    close("simulated t-tail (5 standard errors)", p_sim, p_quad, 5 * se)
    q("two-sided p-value of alpha, df = 56", p_quad, "0.0028")
    p_mkt = 1.0 - 2.0 * simpson(lambda x: np.exp(log_t_density(x, df)), 0.0, 5.64)
    assert p_mkt < 1e-4, p_mkt
    print(f"  smallest other |t| = 5.64 has p = {p_mkt:.2e} < 0.0001")
    q("annualized alpha, simple 0.25 x 12 (%)", 0.25 * 12, "3.00")
    q("annualized alpha, compounded (%)", 100 * (1.0025**12 - 1), "3.04")


def value_momentum_combo() -> None:
    print("50/50 value-momentum mix: equal volatility and equal Sharpe ratio S (hypothetical)")
    rng = np.random.default_rng(SEED + 2)
    n, sharpe = 2_000_000, 0.4
    for rho, quoted in ((-0.53, "2.063"), (-0.28, "1.667")):
        closed = math.sqrt(2 / (1 + rho))
        z = rng.standard_normal((n, 2))
        a = sharpe + z[:, 0]
        b = sharpe + rho * z[:, 0] + math.sqrt(1 - rho * rho) * z[:, 1]
        mix = 0.5 * (a + b)
        sr_mix = mix.mean() / mix.std(ddof=1)
        ratio = sr_mix / sharpe
        # the Sharpe estimate has standard error about sqrt((1 + SR^2 / 2) / n); scale by 1 / S for the ratio
        se = math.sqrt((1 + 0.5 * sr_mix**2) / n) / sharpe
        close(f"simulated Sharpe multiplier at rho = {rho} (5 standard errors)", ratio, closed, 5 * se)
        q(f"Sharpe multiplier sqrt(2 / (1 + rho)) at rho = {rho}", closed, quoted)


def main() -> None:
    multiple_testing()
    mclean_pontiff()
    regression_table()
    value_momentum_combo()
    print("all factor-evidence checks passed")


if __name__ == "__main__":
    main()
