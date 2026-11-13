"""Poisson processes: every number in the note, recomputed by an independent route.

Backs `01-Probability/13-Poisson-Processes.md`.
Closed forms are evaluated and asserted to the quoted decimals; each is then checked against a seeded simulation
built from exponential inter-arrival times (never from the Poisson pmf the closed form uses), against numerical
integration, or against a cumulant computation.
Simulation tolerances are five standard errors; the seed is fixed.
Run it with `python 01-Probability/code/prob_13_poisson_processes.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261019
RNG = np.random.default_rng(SEED)
N_SIM = 400_000


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")
    return value


def exact(label: str, value: Fraction, expected: Fraction) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def sim_mean(label: str, samples: np.ndarray, target: float) -> None:
    est = float(samples.mean())
    se = float(samples.std(ddof=1)) / math.sqrt(samples.size)
    assert abs(est - target) <= 5.0 * se + 1e-12, f"{label}: simulated {est} (se {se}), target {target}"
    print(f"    {label}: simulated {est:.6g} (se {se:.2g}) vs {target:.6g}")


def simpson(f, a: float, b: float, n: int = 4000) -> float:
    h = (b - a) / n
    s = f(a) + f(b)
    s += 4.0 * sum(f(a + (2 * k - 1) * h) for k in range(1, n // 2 + 1))
    s += 2.0 * sum(f(a + 2 * k * h) for k in range(1, n // 2))
    return s * h / 3.0


def arrival_times(rate: float, horizon: float, n_paths: int, max_events: int) -> np.ndarray:
    """Event times from cumulated Exp(rate) gaps; columns beyond the horizon are set to inf."""
    t = np.cumsum(RNG.exponential(1 / rate, size=(n_paths, max_events)), axis=1)
    assert np.all(t[:, -1] > horizon), "max_events too small"
    return np.where(t <= horizon, t, np.inf)


def first_arrivals(rate: float, n_paths: int, k: int) -> np.ndarray:
    """The first k event times of each path, from cumulated Exp(rate) gaps."""
    return np.cumsum(RNG.exponential(1 / rate, size=(n_paths, k)), axis=1)


def counts(rate: float, horizon: float, n_paths: int = N_SIM) -> np.ndarray:
    max_events = int(rate * horizon + 12 * math.sqrt(rate * horizon) + 20)
    return np.isfinite(arrival_times(rate, horizon, n_paths, max_events)).sum(axis=1)


def basic_counts() -> None:
    print("Cards and worked examples: counts from exponential gaps")
    n2 = counts(2.0, 1.0)
    quoted("e^-2 (card prob-pp-no-event-probability)", math.exp(-2), 0.135, 3)
    sim_mean("P(N(1) = 0), rate 2", (n2 == 0).astype(float), math.exp(-2))
    p3 = math.exp(-2) * 2**3 / math.factorial(3)
    quoted("P(N = 3), rate 2 (card prob-ps-poisson-three-events)", p3, 0.180, 3)
    sim_mean("P(N(1) = 3), rate 2", (n2 == 3).astype(float), p3)
    sim_mean("E[N(1)] = 2", n2.astype(float), 2.0)
    disp = n2.var(ddof=1) / n2.mean()
    assert abs(disp - 1) < 0.02, disp
    print(f"    index of dispersion Var(N)/E[N] = {disp:.4f}")
    mu = 1.3
    even = (counts(mu, 1.0) % 2 == 0).astype(float)
    sim_mean("P(N even), mu = 1.3, versus (1 + e^-2mu)/2 (card prob-pp-even-count)", even, (1 + math.exp(-2 * mu)) / 2)
    exact_even = sum(math.exp(-mu) * mu**k / math.factorial(k) for k in range(0, 60, 2))
    quoted("P(N even) by summing the pmf", exact_even, (1 + math.exp(-2 * mu)) / 2, 14)
    quoted("e^-1 (card prob-pp-binomial-limit)", math.exp(-1), 0.368, 3)
    quoted("0.999^1000", 0.999**1000, 0.3677, 4)
    trades = RNG.random((20_000, 1000)) < 0.001
    sim_mean("simulated P(no failures in 1000 trades)", (~trades.any(axis=1)).astype(float), 0.999**1000)
    quoted("e^-5 (card prob-ps-poisson-quiet-period)", math.exp(-5), 0.0067, 4)
    gaps = RNG.exponential(1 / 10, N_SIM)
    sim_mean("P(Exp(10) gap > 0.5)", (gaps > 0.5).astype(float), math.exp(-5))


def gamma_and_covariance() -> None:
    print("Cards: n-th arrival, covariance and sum of arrival times")
    lam, n = 3.0, 4
    t = first_arrivals(lam, N_SIM, n)
    s_n = t[:, n - 1]
    sim_mean("E[S_4] = n/lambda (card prob-pp-nth-arrival-gamma)", s_n, n / lam)
    sim_mean("Var proxy: E[(S_4 - 4/3)^2] = n/lambda^2", (s_n - n / lam) ** 2, n / lam**2)
    tail = 1 - sum(math.exp(-lam) * lam**k / math.factorial(k) for k in range(n))
    sim_mean("P(S_4 <= 1) = P(N(1) >= 4) from the Poisson pmf", (s_n <= 1.0).astype(float), tail)
    times = arrival_times(2.0, 2.0, N_SIM, 30)
    n1 = (times <= 1.0).sum(axis=1)
    n2 = np.isfinite(times).sum(axis=1)
    cov = np.mean((n1 - n1.mean()) * (n2 - n2.mean()))
    se = np.std((n1 - n1.mean()) * (n2 - n2.mean()), ddof=1) / math.sqrt(N_SIM)
    assert abs(cov - 2.0) <= 5 * se, cov
    print(f"    Cov(N(1), N(2)), rate 2: simulated {cov:.4f} (se {se:.4f}) vs lambda * min = 2 (card prob-pp-count-covariance)")
    total = np.where(np.isfinite(times), times, 0.0).sum(axis=1)
    sim_mean("E[sum of arrival times in [0, 2]], rate 2: lambda t^2 / 2", total, 2.0 * 2.0**2 / 2)


def superposition_and_racing() -> None:
    print("Worked example: racing two processes (rates 2 and 3 are inputs)")
    exact("P(two A before one B)", Fraction(2, 5) ** 2, Fraction(4, 25))
    a = first_arrivals(2.0, N_SIM, 2)
    b = first_arrivals(3.0, N_SIM, 1)
    sim_mean("simulated P(A_2 < B_1) (card prob-pp-k-before-one)", (a[:, 1] < b[:, 0]).astype(float), 4 / 25)
    sim_mean("first event from A: lambda/(lambda+mu) (card prob-pp-superposition-rate)", (a[:, 0] < b[:, 0]).astype(float), 2 / 5)
    merged_rate = 1 / np.minimum(a[:, 0], b[:, 0]).mean()
    assert abs(merged_rate - 5) < 0.05, merged_rate
    print(f"    merged first-event rate: simulated {merged_rate:.3f} vs 5")
    exact("E[max(T_A, T_B)] = 1/2 + 1/3 - 1/5", Fraction(1, 2) + Fraction(1, 3) - Fraction(1, 5), Fraction(19, 30))
    integral = simpson(lambda t: 1 - (1 - math.exp(-2 * t)) * (1 - math.exp(-3 * t)), 0.0, 40.0)
    quoted("E[max] by integrating P(max > t)", integral, 19 / 30, 7)
    sim_mean("simulated E[max(T_A, T_B)]", np.maximum(a[:, 0], b[:, 0]), 19 / 30)
    exact("card prob-pp-max-of-two-exponential-waits: 1 + 1/2 - 1/3", Fraction(1) + Fraction(1, 2) - Fraction(1, 3), Fraction(7, 6))
    integral = simpson(lambda t: 1 - (1 - math.exp(-t)) * (1 - math.exp(-2 * t)), 0.0, 60.0)
    quoted("rates 1 and 2: E[max] by integration", integral, 7 / 6, 7)


def thinning() -> None:
    print("Worked example: thinning order flow (10 per second, buy probability 0.3)")
    quoted("e^-3", math.exp(-3), 0.050, 3)
    n = counts(10.0, 1.0)
    buys = RNG.binomial(n, 0.3)
    sells = n - buys
    sim_mean("P(no buys in a second)", (buys == 0).astype(float), math.exp(-3))
    sim_mean("E[buys] = 3 (card prob-pp-thinning-independence)", buys.astype(float), 3.0)
    sim_mean("E[sells] = 7", sells.astype(float), 7.0)
    corr = np.corrcoef(buys, sells)[0, 1]
    assert abs(corr) < 5 / math.sqrt(n.size), corr
    print(f"    corr(buys, sells) = {corr:.4f} (independent streams)")
    sel = n == 5
    sim_mean("given 5 orders, E[buys] = 5 * 0.3", buys[sel].astype(float), 1.5)


def covering_gap(gaps: np.ndarray, probe: float) -> tuple[np.ndarray, np.ndarray]:
    """One independent bus process per row; return (wait, covering gap) at the fixed probe time."""
    times = np.cumsum(gaps, axis=1)
    assert np.all(times[:, -1] > probe), "too few gaps simulated"
    k = (times <= probe).sum(axis=1)
    rows = np.arange(times.shape[0])
    after = times[rows, k]
    before = np.where(k > 0, times[rows, np.maximum(k - 1, 0)], 0.0)
    return after - probe, after - before


def inspection() -> None:
    print("Worked example and cards: buses and the inspection paradox")
    probe = 300.0  # minutes after the first bus process starts; 30 mean gaps, far from 0
    wait, gap = covering_gap(RNG.exponential(10.0, size=(N_SIM // 2, 80)), probe)
    sim_mean("Poisson buses, mean gap 10: mean wait (card prob-pp-inspection-paradox)", wait, 10.0)
    sim_mean("Poisson buses: mean covering gap", gap, 20.0)
    sim_mean("Poisson buses: time since last bus", gap - wait, 10.0)
    phase = RNG.random(N_SIM) * 10.0
    sim_mean("buses every 10 minutes exactly: mean wait", 10.0 - phase, 5.0)
    exact("E[L^2]/(2E[L]) for L = 10", Fraction(10**2, 2 * 10), Fraction(5))
    exact("E[L^2]/(2E[L]) for Exp mean 10: 200/20", Fraction(2 * 10**2, 2 * 10), Fraction(10))
    # Gaps uniform on [0, 20]: E[L^2] / (2 E[L]) = (400/3) / 20 = 20/3.
    exact("uniform gaps on [0, 20]: E[L^2]/(2E[L])", Fraction(400, 3) / 20, Fraction(20, 3))
    quoted("20/3 (card prob-pp-uniform-gap-wait)", 20 / 3, 6.67, 2)
    gaps_u = RNG.random(N_SIM) * 20.0
    sim_mean("simulated E[L^2] for U(0, 20) gaps", gaps_u**2, 400 / 3)
    exact("Var(L) = E[L^2] - E[L]^2 for U(0, 20)", Fraction(400, 3) - 10**2, Fraction(100, 3))
    wait, gap = covering_gap(RNG.random((N_SIM // 2, 80)) * 20.0, probe)
    sim_mean("simulated wait with U(0, 20) gaps", wait, 20 / 3)
    sim_mean("simulated covering gap with U(0, 20) gaps: E[L^2]/E[L]", gap, 40 / 3)


def compound() -> None:
    print("Worked example and cards: compound Poisson (2 jumps a day, N(0, 1%^2) sizes)")
    lam, sig = 2.0, 0.01
    var = lam * sig**2
    quoted("daily variance lambda E[Y^2]", var, 0.0002, 10)
    quoted("daily jump sd (%)", math.sqrt(var) * 100, 1.41, 2)
    # Cumulants of compound Poisson: kappa_m = lambda t E[Y^m]; excess kurtosis = kappa_4 / kappa_2^2.
    for t, want, dec in ((1.0, 1.5, 1), (20.0, 0.075, 3)):
        k2, k4 = lam * t * sig**2, lam * t * 3 * sig**4
        quoted(f"excess kurtosis at t = {t:g} days (card prob-pp-compound-kurtosis)", k4 / k2**2, want, dec)
    n = counts(lam, 1.0, 1_000_000)
    x = RNG.standard_normal(n.size) * sig * np.sqrt(n)
    sim_mean("simulated Var(X(1)) (card prob-pp-compound-variance)", x**2, var)
    m2, m4 = np.mean(x**2), np.mean(x**4)
    kurt = m4 / m2**2 - 3
    assert abs(kurt - 1.5) < 0.1, kurt
    print(f"    simulated excess kurtosis at one day = {kurt:.3f}")
    # Variance uses E[Y^2], not Var(Y): jumps with mean 0.5% and sd 1%.
    y_mean = 0.005
    n = counts(lam, 1.0)
    xs = RNG.standard_normal(n.size) * sig * np.sqrt(n) + y_mean * n
    target = lam * (sig**2 + y_mean**2)
    sim_mean("non-zero-mean jumps: Var = lambda E[Y^2]", (xs - lam * y_mean) ** 2, target)


def conditional_uniformity() -> None:
    print("Worked example and card: arrival times given the count")
    t = arrival_times(2.0, 1.0, 1_000_000, 25)
    two = np.isfinite(t).sum(axis=1) == 2
    first, second = t[two, 0], t[two, 1]
    sim_mean("given N(1) = 2: P(both before 1/2) (card prob-ps-poisson-both-in-first-half)", (second < 0.5).astype(float), 0.25)
    sim_mean("given N(1) = 2: E[first time] = 1/3", first, 1 / 3)
    exact("(1/2)^2", Fraction(1, 2) ** 2, Fraction(1, 4))


if __name__ == "__main__":
    basic_counts()
    gamma_and_covariance()
    superposition_and_racing()
    thinning()
    inspection()
    compound()
    conditional_uniformity()
    print("All Poisson process checks passed.")
