"""Performance metrics and the fundamental law: every Sharpe, standard error, breadth and drawdown number in the note.

Backs every number in `09-Alpha-Research-and-Portfolio/09-Performance-Metrics-and-Fundamental-Law.md`.
Independent routes used here:
- the log growth rate by numerical integration of E[ln(1 + r)], against the sigma^2/2 drag approximation;
- Sharpe standard errors (Lo 2002 normal, Mertens 2002 non-normal) by seeded simulation of 756 daily
  returns, normal and from a two-normal mixture with skewness -1 and kurtosis 8;
- Lo's autocorrelation correction by simulating MA(1) monthly returns and measuring the Sharpe of annual sums;
- the fundamental law, transfer coefficient and effective breadth by simulating 500-name cross-sections;
- the binary-forecast IC by enumerating the joint distribution of forecast and outcome in exact fractions;
- the drawdown and Sortino demo in exact fractions and by calling `performance_metrics.py` itself.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 09-Alpha-Research-and-Portfolio/code/alpha_09_performance_metrics.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction
from statistics import NormalDist

import numpy as np
import pandas as pd
from alpha_08_deflated_sharpe import mixture_with, sample_mixture
from performance_metrics import PerformanceMetrics

SEED = 20261114
N01 = NormalDist()


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


def annualising() -> None:
    print("Annualising a daily track record (worked example 1)")
    approx("annualised Sharpe", 0.0005 / 0.01 * math.sqrt(252), 0.794, 3)
    approx("annualised arithmetic return (%)", 252 * 0.05, 12.6, 1)
    approx("annualised volatility (%)", 1 * math.sqrt(252), 15.9, 1)
    drag = 12.6 - 15.874507866387544**2 / 100 / 2
    approx("arithmetic return minus sigma^2/2 (%)", drag, 11.3, 1)
    approx("volatility drag sigma^2/2 (%)", 0.159**2 / 2 * 100, 1.26, 2)
    x = np.linspace(-12.0, 12.0, 240001)
    phi = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    e_log = float(np.trapezoid(np.log1p(0.0005 + 0.01 * x) * phi, x))
    approx("log growth rate by quadrature of E[ln(1 + r)] (%)", 252 * e_log * 100, 11.3, 1)


def sharpe_se(rng: np.random.Generator) -> None:
    print("Precision of a 3-year Sharpe of 1.5 (worked example 2, cards alpha-perf-sharpe-se-*)")
    sr = 1.5 / math.sqrt(252)
    approx("daily Sharpe", sr, 0.0945, 4)
    lo = math.sqrt((1 + sr * sr / 2) / 756) * math.sqrt(252)
    approx("Lo standard error, annualised", lo, 0.579, 3)
    mertens = math.sqrt((1 + sr + 7 / 4 * sr * sr) / 756) * math.sqrt(252)
    approx("Mertens standard error, annualised", mertens, 0.608, 3)
    approx("Mertens standard error, card", mertens, 0.61, 2)
    approx("95% interval, lower", 1.5 - 1.96 * mertens, 0.31, 2)
    approx("95% interval, upper", 1.5 + 1.96 * mertens, 2.69, 2)
    approx("t", 1.5 / mertens, 2.47, 2)
    approx("trap: annual Sharpe in the 3-observation formula", math.sqrt((1 + 1.5**2 / 2) / 3), 0.84, 2)
    srm = 1.5 / math.sqrt(12)
    approx("36 monthly returns, annualised SE", math.sqrt((1 + srm * srm / 2) / 36) * math.sqrt(12), 0.60, 2)
    approx("SE after 5 years of daily data (about 1/sqrt(5))", 1 / math.sqrt(5), 0.45, 2)

    sims, t = 20_000, 756
    normal = rng.standard_normal((sims, t)) + sr
    est = normal.mean(axis=1) / normal.std(axis=1, ddof=1) * math.sqrt(252)
    simulated("Lo SE by simulation of normal daily returns", float(est.std(ddof=1)), 0.579, 4 * 0.579 / math.sqrt(2 * sims))
    p, d, s = mixture_with(-1.0, 8.0)
    sims = 120_000
    est = []
    for _ in range(sims // 1000):
        xm = sr + sample_mixture(rng, (1000, t), p, d, s)
        est.append(xm.mean(axis=1) / xm.std(axis=1, ddof=1) * math.sqrt(252))
    est = np.concatenate(est)
    tol = 4 * 0.608 * math.sqrt(2 / sims) * 1.2
    simulated("Mertens SE by simulation, skewness -1 and kurtosis 8", float(est.std(ddof=1)), 0.608, tol)
    assert abs(float(est.std(ddof=1)) - 0.579) > tol, "the simulation must separate the non-normal SE from the normal one"
    monthly = rng.standard_normal((200_000, 36)) + srm
    est_m = monthly.mean(axis=1) / monthly.std(axis=1, ddof=1) * math.sqrt(12)
    simulated("36 monthly returns, SE by simulation (small-sample)", float(est_m.std(ddof=1)), 0.62, 0.006)


def lo_autocorrelation(rng: np.random.Generator) -> None:
    print("Autocorrelated monthly returns (worked example 3, card alpha-perf-lo-autocorr)")
    eta = 12 / math.sqrt(12 + 2 * 11 * 0.2)
    approx("12 + 2 x 11 x 0.2", 12 + 2 * 11 * 0.2, 16.4, 9)
    approx("eta(12)", eta, 2.963, 3)
    approx("sqrt(12)", math.sqrt(12), 3.464, 3)
    approx("Lo annualised Sharpe", 0.3 * eta, 0.89, 2)
    approx("naive annualised Sharpe", 0.3 * math.sqrt(12), 1.04, 2)
    approx("naive overstatement (%)", (math.sqrt(12) / eta - 1) * 100, 17, 0)
    # MA(1) with lag-1 autocorrelation 0.2: theta / (1 + theta^2) = 0.2
    theta = (1 - math.sqrt(1 - 4 * 0.2**2)) / (2 * 0.2)
    years = 400_000
    e = rng.standard_normal((years, 13))
    r = (e[:, 1:] + theta * e[:, :-1]) / math.sqrt(1 + theta * theta) + 0.3
    lag1 = np.corrcoef(r[:, 1:].ravel(), r[:, :-1].ravel())[0, 1]
    simulated("simulated lag-1 autocorrelation", float(lag1), 0.2, 0.003)
    annual = r.sum(axis=1)
    simulated("Sharpe of simulated annual sums", float(annual.mean() / annual.std(ddof=1)), 0.889, 4 * math.sqrt(1 / years) + 0.002)


def fundamental_law(rng: np.random.Generator) -> None:
    print("The fundamental law in numbers (worked example 4, cards alpha-perf-fl-numeric, -transfer-coefficient, -effective-breadth)")
    approx("IR, IC 0.02, breadth 6000", 0.02 * math.sqrt(6000), 1.55, 2)
    approx("IR with TC 0.5", 0.5 * 0.02 * math.sqrt(6000), 0.77, 2)
    n_eff = 500 / (1 + 499 * 0.05)
    approx("effective breadth per month", n_eff, 19.3, 1)
    approx("effective breadth, card 'about 19'", n_eff, 19, 0)
    approx("IR with correlated bets", 0.02 * math.sqrt(12 * n_eff), 0.30, 2)

    months, names, ic = 20_000, 500, 0.02
    sig = rng.uniform(0.04, 0.12, names)  # hypothetical monthly residual vols
    full, half, corr_bets, corr_resid = [], [], [], []
    for _ in range(months // 1000):
        z = rng.standard_normal((1000, names))
        e = rng.standard_normal((1000, names))
        r = sig * (ic * z + math.sqrt(1 - ic * ic) * e)
        h = ic * sig * z / sig**2  # h = alpha / sigma^2, the unconstrained mean-variance direction
        full.append((h * r).sum(axis=1))
        u = rng.standard_normal((1000, names))
        h_tc = (0.5 * z + math.sqrt(0.75) * u) / sig  # risk-adjusted weights correlated 0.5 with the forecasts
        half.append((h_tc * r).sum(axis=1))
        f = rng.standard_normal((1000, 1))
        payoff = ic + math.sqrt(0.05) * f + math.sqrt(0.95) * e  # unit-variance bets with pairwise correlation 0.05
        corr_bets.append(payoff.sum(axis=1))
        zc = z - z.mean(axis=1, keepdims=True)
        resid = math.sqrt(0.05) * f + math.sqrt(0.95) * e  # equicorrelated residuals, demeaned signal
        rc = ic * zc + math.sqrt(1 - ic * ic) * resid
        corr_resid.append((zc * rc).sum(axis=1))

    def ir(x: list[np.ndarray]) -> float:
        a = np.concatenate(x)
        return float(a.mean() / a.std(ddof=1) * math.sqrt(12))

    se = 4 * math.sqrt(12 / months)
    simulated("IR of the unconstrained book, simulated", ir(full), 1.55, se)
    simulated("IR with transfer coefficient 0.5, simulated", ir(half), 0.77, se)
    simulated("IR when bet payoffs have pairwise correlation 0.05, simulated", ir(corr_bets), 0.30, se)
    approx("IC sqrt(6000 / 0.95), common component cancelled", 0.02 * math.sqrt(6000 / 0.95), 1.59, 2)
    simulated("IR when only residuals are correlated and the signal is demeaned, simulated", ir(corr_resid), 1.59, se)

    print("Binary forecasts (card alpha-perf-hit-rate-ic)")
    p = Fraction(52, 100)
    joint = {(1, 1): p / 2, (-1, -1): p / 2, (1, -1): (1 - p) / 2, (-1, 1): (1 - p) / 2}
    cov = sum(prob * f * o for (f, o), prob in joint.items())
    exact("IC of a +/-1 forecast that is right 52% of the time", cov, Fraction(4, 100))
    approx("IR at 10 bets a day", 0.04 * math.sqrt(10 * 252), 2.0, 1)
    exact("breadth", 10 * 252, 2520)


def drawdown_sortino() -> None:
    print("Drawdown and Sortino (worked example 5, card alpha-perf-sortino-correct)")
    prices = [Fraction(v) for v in (100, 102, 104, 103, 105, 108, 101, 103)]
    rets = [b / a - 1 for a, b in zip(prices[:-1], prices[1:], strict=True)]
    for value, quoted in zip(rets, (2.00, 1.96, -0.96, 1.94, 2.86, -6.48, 1.98), strict=True):
        approx("return (%)", float(value) * 100, quoted, 2)
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
    approx("mean (%)", float(mean) * 100, 0.471, 3)
    approx("standard deviation (%)", math.sqrt(var) * 100, 3.29, 2)
    peak, mdd = prices[0], Fraction(0)
    for px in prices:
        peak = max(peak, px)
        mdd = min(mdd, px / peak - 1)
    exact("max drawdown", mdd, Fraction(101, 108) - 1)
    approx("max drawdown (%)", float(mdd) * 100, -6.48, 2)
    downside = math.sqrt(sum(min(r, 0) ** 2 for r in rets) / len(rets))
    approx("downside deviation (%)", downside * 100, 2.48, 2)
    approx("downside deviation from the 4 dp returns (%)", math.sqrt((0.0096**2 + 0.0648**2) / 7) * 100, 2.48, 2)
    approx("mean (%, 4 dp)", float(mean) * 100, 0.4710, 4)
    approx("downside deviation (%, 4 dp)", downside * 100, 2.4766, 4)
    approx("Sortino from the 4 dp inputs 0.004710 / 0.024766 x sqrt(252)", 0.004710 / 0.024766 * math.sqrt(252), 3.02, 2)
    sortino = float(mean) / downside * math.sqrt(252)
    approx("Sortino, unrounded", sortino, 3.02, 2)
    approx("Sortino from inputs rounded to 0.00471 and 0.0248", 0.00471 / 0.0248 * math.sqrt(252), 3.01, 2)
    demo = PerformanceMetrics.sortino_ratio(PerformanceMetrics.calculate_returns(pd.Series([float(p) for p in prices])))
    approx("performance_metrics.py sortino_ratio", demo, 3.0189, 4)
    losses = [r for r in rets if r < 0]
    lm = sum(losses) / len(losses)
    sd_losses = math.sqrt(sum((r - lm) ** 2 for r in losses) / (len(losses) - 1))
    approx("sd of the two losing returns (%)", sd_losses * 100, 3.90, 2)
    approx("buggy Sortino", float(mean) / sd_losses * math.sqrt(252), 1.92, 2)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    annualising()
    sharpe_se(rng)
    lo_autocorrelation(rng)
    fundamental_law(rng)
    drawdown_sortino()
    print("All performance-metric numbers check.")
