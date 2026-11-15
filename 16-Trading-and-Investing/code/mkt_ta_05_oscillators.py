"""Oscillators and the multiple-testing hazard: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/05-Oscillators-Mean-Reversion-and-Overfitting.md`.
Independent routes used here:
- the RSI worked example by a generic Wilder RSI implementation run on a constructed price series whose
  14-day averages are the stated 1.20 and 0.40, against the hand arithmetic in exact fractions;
- the long-run RSI level under a hypothetical drift from the closed-form normal partial moments, checked
  against a seeded simulation of the average up and down moves (five standard errors);
- false-positive counts and Harvey-Liu-Zhu p-values from the normal CDF by math.erf and by numerical
  quadrature of the density, and P(at least one false positive) by summing the exact binomial pmf;
- the Bailey-Lopez de Prado expected maximum Sharpe ratio against the exact expected maximum of N normals
  by quadrature and a seeded simulation, and the Sharpe-ratio standard error in the DSR denominator against
  the simulated spread of Sharpe estimates for normal returns;
- Lambert's CCI scaling from the normal mean absolute deviation, checked by simulation.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_05_oscillators.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261115
EULER_GAMMA = 0.5772156649015329


def check(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def phi_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def phi_cdf_quad(x: float, lo: float = -12.0, n: int = 200_001) -> float:
    grid = np.linspace(lo, x, n)
    dens = np.exp(-0.5 * grid**2) / math.sqrt(2 * math.pi)
    return float(np.trapezoid(dens, grid))


def phi_inv(p: float) -> float:
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if phi_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def wilder_rsi(prices: np.ndarray, n: int) -> np.ndarray:
    """Wilder RSI: seed with the simple mean of the first n changes, then smooth with alpha = 1/n."""
    change = np.diff(prices)
    up = np.maximum(change, 0.0)
    down = np.maximum(-change, 0.0)
    avg_u, avg_d = up[:n].mean(), down[:n].mean()
    out = [100.0 * avg_u / (avg_u + avg_d)]
    for u, d in zip(up[n:], down[n:], strict=True):
        avg_u = (avg_u * (n - 1) + u) / n
        avg_d = (avg_d * (n - 1) + d) / n
        out.append(100.0 * avg_u / (avg_u + avg_d))
    return np.array(out)


def rsi_examples() -> None:
    closes = np.array([100.0, 102.0, 101.0, 104.0, 106.0])
    change = np.diff(closes)
    assert list(np.maximum(change, 0)) == [2.0, 0.0, 3.0, 2.0]
    assert list(np.maximum(-change, 0)) == [0.0, 1.0, 0.0, 0.0]
    print("daily U = [2, 0, 3, 2], D = [0, 1, 0, 0]")
    # 14 changes: seven gains of 2.40 and seven losses of 0.80 give averages 1.20 and 0.40; then a +1.00 day.
    changes = np.array([2.40, -0.80] * 7 + [1.00])
    prices = 100.0 + np.concatenate([[0.0], np.cumsum(changes)])
    rsi = wilder_rsi(prices, 14)
    avg_u, avg_d = Fraction(120, 100), Fraction(40, 100)
    check("RS = 1.20 / 0.40", float(avg_u / avg_d), "3.00")
    check("100 / (1 + RS)", float(Fraction(100) / (1 + avg_u / avg_d)), "25.00")
    check("RSI from the hand formula 100 - 100 / (1 + RS)", float(100 - Fraction(100) / (1 + avg_u / avg_d)), "75.00")
    check("RSI from the generic Wilder implementation, day 14", rsi[0], "75.00")
    next_u = (13 * avg_u + 1) / 14
    next_d = (13 * avg_d + 0) / 14
    check("smoothed average gain after a +1.00 day", float(next_u), "1.1857")
    check("smoothed average loss after a +1.00 day", float(next_d), "0.3714")
    check("RSI after a +1.00 day, exact fractions", float(100 * next_u / (next_u + next_d)), "76.15")
    check("RSI after a +1.00 day, generic Wilder implementation", rsi[1], "76.15")


def drift_rsi_level(rng: np.random.Generator) -> None:
    """Long-run level of Wilder's averages for normal daily changes with mean/sd = 0.2 (hypothetical)."""
    z = 0.2
    pdf = math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    e_up = z * phi_cdf(z) + pdf  # E[max(X, 0)] / sigma
    e_down = -z * phi_cdf(-z) + pdf  # E[max(-X, 0)] / sigma
    level = 100 * e_up / (e_up + e_down)
    x = rng.normal(z, 1.0, size=2_000_000)
    up, down = np.maximum(x, 0), np.maximum(-x, 0)
    for name, sample, exact in (("up", up, e_up), ("down", down, e_down)):
        se = sample.std(ddof=1) / math.sqrt(sample.size)
        assert abs(sample.mean() - exact) < 5 * se, f"E[{name}] {sample.mean()} vs {exact}"
    check("E[up move] / sigma at drift 0.2 sigma", e_up, "0.5069")
    check("E[down move] / sigma at drift 0.2 sigma", e_down, "0.3069")
    check("long-run RSI level 100 E[U] / (E[U] + E[D])", level, "62.3")
    path = 100 + np.cumsum(rng.normal(z, 1.0, size=200_000))
    rsi = wilder_rsi(path, 14)
    print(f"simulated 14-day RSI on that drift (seed {SEED}, illustration only): median {np.median(rsi):.1f}")


def multiple_testing() -> None:
    alpha = 0.05
    check("expected false positives in 20 independent tests at 5%", 20 * alpha, "1")
    p_any = 1 - (1 - alpha) ** 20
    a = Fraction(1, 20)
    p_any_binom = sum(math.comb(20, k) * a**k * (1 - a) ** (20 - k) for k in range(1, 21))
    assert abs(float(p_any_binom) - p_any) < 1e-12
    check("P(at least one false positive in 20 tests), percent", 100 * float(p_any_binom), "64.2")
    check("expected false positives in 1,000 tests at 5%", 1000 * alpha, "50")
    check("two-sided 5% critical value", phi_inv(0.975), "1.96")
    p3 = 2 * (1 - phi_cdf(3.0))
    p3_quad = 2 * (1 - phi_cdf_quad(3.0))
    assert abs(p3 - p3_quad) < 1e-8
    check("two-sided p-value at t = 3.0", p3_quad, "0.0027")
    hlz = {"factors catalogued": 316, "t hurdle": 3.0}
    print(f"cited constants, Harvey, Liu and Zhu (2016): {hlz}")


def expected_max_normal(n: int) -> float:
    x = np.linspace(-10, 10, 400_001)
    cdf = 0.5 * (1 + np.vectorize(math.erf)(x / math.sqrt(2)))
    pdf = np.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)
    return float(np.trapezoid(x * n * cdf ** (n - 1) * pdf, x))


def deflated_sharpe(rng: np.random.Generator) -> None:
    n_trials, years, var_sr = 500, 5, 0.25
    t_obs = years * 252
    check("T = 5 years x 252 days", t_obs, "1,260")
    check("T - 1", t_obs - 1, "1,259")
    sigma_sr = math.sqrt(var_sr)
    check("sigma_SR = sqrt(0.25)", sigma_sr, "0.50")
    z1 = phi_inv(1 - 1 / n_trials)
    z2 = phi_inv(1 - 1 / (n_trials * math.e))
    check("Phi^-1(1 - 1/500)", z1, "2.8782")
    check("Phi^-1(1 - 1/(500 e))", z2, "3.1802")
    approx = (1 - EULER_GAMMA) * z1 + EULER_GAMMA * z2
    check("Bailey-Lopez de Prado E[max] approximation, standard deviations", approx, "3.0525")
    exact = expected_max_normal(n_trials)
    sims = rng.standard_normal((20_000, n_trials)).max(axis=1)
    se = sims.std(ddof=1) / math.sqrt(sims.size)
    assert abs(sims.mean() - exact) < 5 * se, f"simulated max {sims.mean()} vs quadrature {exact}"
    check("exact E[max of 500 standard normals] by quadrature", exact, "3.04")
    print(f"simulated E[max of 500] (seed {SEED}) = {sims.mean():.4f} +/- {se:.4f}")
    sr_star_ann = sigma_sr * approx
    check("SR* annualized = 0.50 x 3.0525", sr_star_ann, "1.526")
    check("SR* annualized, rounded", sr_star_ann, "1.53")
    sr_star = sr_star_ann / math.sqrt(252)
    sr_hat = 1.40 / math.sqrt(252)
    check("daily SR* = 1.526 / sqrt(252)", sr_star, "0.0961")
    check("daily SR-hat = 1.40 / sqrt(252)", sr_hat, "0.0882")
    g3, g4 = -0.60, 4.50 + 3.0
    check("raw kurtosis = 4.50 + 3", g4, "7.50")
    denom = math.sqrt(1 - g3 * sr_hat + (g4 - 1) / 4 * sr_hat**2)
    check("DSR denominator", denom, "1.0323")
    stat = (sr_hat - sr_star) * math.sqrt(t_obs - 1) / denom
    check("DSR test statistic", stat, "-0.27")
    dsr = phi_cdf_quad(stat)
    assert abs(dsr - phi_cdf(stat)) < 1e-8
    check("DSR = Phi(statistic)", dsr, "0.39")
    assert dsr < 0.95
    n_h = 1_000_000
    gamma_harmonic = float(np.sum(1.0 / np.arange(1, n_h + 1))) - math.log(n_h) - 1 / (2 * n_h)
    assert abs(gamma_harmonic - EULER_GAMMA) < 1e-9
    check("Euler-Mascheroni constant from H_n - ln n", gamma_harmonic, "0.5772")
    # The denominator is the standard error of a Sharpe estimate; for normal returns the (g4 - 1) / 4 term is 1/2.
    sr_true, t_sim = 0.0882, 1260
    rets = rng.normal(sr_true, 1.0, size=(20_000, t_sim))
    est = rets.mean(axis=1) / rets.std(axis=1, ddof=1)
    formula_sd = math.sqrt((1 + 0.5 * sr_true**2) / (t_sim - 1))
    sd = est.std(ddof=1)
    sd_se = sd / math.sqrt(2 * (est.size - 1))
    assert abs(sd - formula_sd) < 5 * sd_se, f"simulated SD of SR-hat {sd} vs formula {formula_sd}"
    print(f"SD of daily SR estimates for normal returns, simulated {sd:.5f} vs formula {formula_sd:.5f}")


def cited_conventions() -> None:
    check("hypothetical rally from 100 to 140, percent", 100 * (140 / 100 - 1), "40")
    conventions = {
        "RSI oversold / overbought lines": (30, 70),
        "practitioner bull-market RSI band": (40, 80),
        "MACD fast / slow EMA lengths (days)": (12, 26),
        "practitioner ADX filter threshold": 25,
        "fragile lookback change (illustrative)": (14, 15),
        "stable lookback plateau (illustrative)": (12, 18),
        "DSR confidence level (percent)": 95,
    }
    for key, value in conventions.items():
        print(f"cited: {key} = {value}")


def cci_scaling(rng: np.random.Generator) -> None:
    k = 1.5 * math.sqrt(2 / math.pi)  # 100 CCI units = 100 x 0.015 = 1.5 mean deviations = 1.5 x 0.7979 sigma
    inside = 2 * phi_cdf(k) - 1
    check("1.5 mean absolute deviations in sigma units", k, "1.197")
    check("share of normal deviations inside +/-100 CCI, percent", 100 * inside, "76.9")
    x = rng.standard_normal(1_000_000)
    cci = x / (0.015 * np.mean(np.abs(x)))
    share = np.mean(np.abs(cci) < 100)
    se = math.sqrt(inside * (1 - inside) / x.size)
    assert abs(share - inside) < 5 * se, f"simulated {share} vs {inside}"


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    rsi_examples()
    drift_rsi_level(rng)
    multiple_testing()
    deflated_sharpe(rng)
    cci_scaling(rng)
    cited_conventions()
    print("all oscillator and multiple-testing numbers check out")
