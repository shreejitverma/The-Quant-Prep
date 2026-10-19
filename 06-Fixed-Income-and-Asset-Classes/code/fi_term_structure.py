"""Term structure models: HJM drift condition, LGM bond pricing, and LMM terminal- and spot-measure drifts.

Backs every number in `06-Fixed-Income-and-Asset-Classes/19-Term-Structure-Models-HJM-LGM-LMM.md`.
- Examples 1 and 2 and card fi-tsm-hjm-drift-condition: Ho-Lee and Hull-White HJM drifts, and a quadrature check that the
  closed-form drift makes discounted bonds martingales (drift integral equals half the variance) while a zero drift does not.
- Example 3 and card fi-tsm-lgm-vs-hw: LGM H(T), zeta(t), the bond price at x = 0, and a Gauss-Hermite check of the martingale
  property E[P(t, T; x) / N(t, x)] = P(0, T).
- Example 4 and cards fi-tsm-lmm-terminal-drift and fi-tsm-spot-vs-terminal-measure: two-rate LMM drift, and a Monte Carlo
  check that with the drift the ratio P(t, T0) / P(t, T2) is a martingale under the terminal measure while without it the
  simulation is biased, and the same check under the spot measure, P(t, T1) / P(t, T0), showing that even the front rate
  L1 drifts there.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_term_structure.py`.
"""

from __future__ import annotations

import math

import numpy as np

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def simpson(fn, lo: float, hi: float, n: int = 400) -> float:
    """Composite Simpson rule with an even number of intervals."""
    h = (hi - lo) / n
    total = fn(lo) + fn(hi)
    for i in range(1, n):
        total += (4.0 if i % 2 else 2.0) * fn(lo + i * h)
    return total * h / 3.0


def hw_vol(s: float, u: float, sigma: float, a: float) -> float:
    return sigma * math.exp(-a * (u - s))


def hw_drift_closed_form(s: float, u: float, sigma: float, a: float) -> float:
    """HJM drift for sigma(s, u) = sigma exp(-a (u - s)): sigma^2 / a * e^{-a(u-s)} (1 - e^{-a(u-s)})."""
    decay = math.exp(-a * (u - s))
    return sigma * sigma / a * decay * (1.0 - decay)


def example_hjm() -> None:
    print("  1. HJM drifts (Examples 1 and 2, card fi-tsm-hjm-drift-condition)")
    quoted("pairwise correlations among 40 forwards", 40 * 39 / 2, 780.0, 0)
    quoted("Ho-Lee drift sigma^2 (T - t), sigma = 1.5%, T - t = 2", 0.015**2 * 2.0, 0.000450, 6)
    sigma, a = 0.012, 0.03
    quoted("Hull-White drift, sigma = 1.2%, a = 0.03, T - t = 2", hw_drift_closed_form(0.0, 2.0, sigma, a), 0.000263, 6)
    quoted("Hull-White forward vol 10y ahead / short-end vol, a = 0.03", hw_vol(0.0, 10.0, 1.0, a), 0.7408, 4)
    # Independent check: log(P(t, T) / B(t)) is Gaussian with mean log P(0, T) - A and variance V, where
    # A = int_0^t int_s^T alpha(s, u) du ds and V = int_0^t (int_s^T sigma(s, u) du)^2 ds.
    # The discounted bond is a martingale iff A = V / 2.
    t, big_t = 1.0, 5.0
    drift_integral = simpson(lambda s: simpson(lambda u: hw_drift_closed_form(s, u, sigma, a), s, big_t), 0.0, t)
    half_var = 0.5 * simpson(lambda s: simpson(lambda u: hw_vol(s, u, sigma, a), s, big_t) ** 2, 0.0, t)
    quoted("drift integral A (t = 1, T = 5) x 1e4", drift_integral * 1e4, 12.7973, 4)
    quoted("half variance V / 2 x 1e4", half_var * 1e4, 12.7973, 4)
    assert abs(drift_integral - half_var) < 1e-12, "HJM drift must make the discounted bond a martingale"
    # With the Ho-Lee drift wrongly paired with the Hull-White volatility, the martingale test fails.
    wrong = simpson(lambda s: simpson(lambda u: sigma * sigma * (u - s), s, big_t), 0.0, t)
    assert abs(wrong - half_var) > 0.1 * half_var


def example_lgm() -> None:
    print("  2. LGM bond pricing (Example 3, card fi-tsm-lgm-vs-hw)")
    a, sigma_hw = 0.03, 0.012
    t, big_t = 1.0, 5.0

    def h_func(mat: float) -> float:
        return (1.0 - math.exp(-a * mat)) / a

    def zeta(time: float) -> float:
        return sigma_hw**2 * (math.exp(2.0 * a * time) - 1.0) / (2.0 * a)

    def disc(time: float) -> float:
        return math.exp(-0.04 * time)

    quoted("H(1)", h_func(t), 0.985149, 6)
    quoted("H(5)", h_func(big_t), 4.643067, 6)
    quoted("zeta(1) x 1e4", zeta(t) * 1e4, 1.4841, 4)
    quoted("P(0, 5) / P(0, 1)", disc(big_t) / disc(t), 0.852144, 6)

    def bond(x: float) -> float:
        return disc(big_t) / disc(t) * math.exp(-(h_func(big_t) - h_func(t)) * x - 0.5 * (h_func(big_t) ** 2 - h_func(t) ** 2) * zeta(t))

    def numeraire(x: float) -> float:
        return math.exp(h_func(t) * x + 0.5 * h_func(t) ** 2 * zeta(t)) / disc(t)

    quoted("LGM P(1, 5) at x = 0", bond(0.0), 0.850843, 6)
    # x(1) ~ N(0, zeta(1)) under the LGM measure; integrate P / N with 40-point Gauss-Hermite.
    nodes, weights = np.polynomial.hermite_e.hermegauss(40)
    sd = math.sqrt(zeta(t))
    expectation = sum(w * bond(sd * z) / numeraire(sd * z) for z, w in zip(nodes, weights, strict=True)) / math.sqrt(2.0 * math.pi)
    quoted("E[P(1, 5; x) / N(1, x)]", expectation, 0.818731, 6)
    quoted("P(0, 5)", disc(big_t), 0.818731, 6)
    assert abs(expectation - disc(big_t)) < 1e-12


def example_lmm() -> None:
    print("  3. LMM terminal- and spot-measure drift (Example 4, cards fi-tsm-lmm-terminal-drift, fi-tsm-spot-vs-terminal-measure)")
    tau2, l1, l2 = 0.25, 0.040, 0.040
    sigma1, sigma2, rho12 = 0.200, 0.180, 0.85
    ratio = tau2 * l2 / (1.0 + tau2 * l2)
    mu1 = -ratio * sigma1 * sigma2 * rho12
    quoted("1 + tau2 L2", 1.0 + tau2 * l2, 1.01, 2)
    quoted("tau2 L2 / (1 + tau2 L2)", ratio, 0.009901, 6)
    quoted("sigma1 sigma2 rho12", sigma1 * sigma2 * rho12, 0.0306, 4)
    quoted("relative drift mu1 per year", mu1, -0.000303, 6)
    quoted("absolute drift L1 mu1 (bp per year)", l1 * mu1 * 1e4, -0.12, 2)

    # Monte Carlo check with large parameters so the drift is visible above the noise.
    # Under Q^{T2}, P(t, T0) / P(t, T2) = (1 + tau L1)(1 + tau L2) must keep its initial expectation.
    tau, f1, f2, s1, s2, rho, t_fix = 1.0, 0.10, 0.10, 0.50, 0.50, 0.90, 2.0
    n_paths, n_steps = 200_000, 50
    dt = t_fix / n_steps
    target = (1.0 + tau * f1) * (1.0 + tau * f2)
    results = {}
    for use_drift in (True, False):
        rng = np.random.default_rng(1997)
        x1 = np.full(n_paths, f1)
        x2 = np.full(n_paths, f2)
        for _ in range(n_steps):
            z1 = rng.standard_normal(n_paths)
            z2 = rho * z1 + math.sqrt(1.0 - rho * rho) * rng.standard_normal(n_paths)
            drift = -tau * x2 / (1.0 + tau * x2) * s1 * s2 * rho if use_drift else 0.0
            x1 = x1 * np.exp((drift - 0.5 * s1 * s1) * dt + s1 * math.sqrt(dt) * z1)
            x2 = x2 * np.exp(-0.5 * s2 * s2 * dt + s2 * math.sqrt(dt) * z2)
        ratio_paths = (1.0 + tau * x1) * (1.0 + tau * x2)
        mean = float(ratio_paths.mean())
        stderr = float(ratio_paths.std()) / math.sqrt(n_paths)
        results[use_drift] = (mean - target) / stderr
    quoted("martingale target (1 + L1)(1 + L2)", target, 1.21, 2)
    quoted("with drift: error in standard errors, seed-stable", results[True], -0.4, 1)
    quoted("without drift: error in standard errors, seed-stable", results[False], 13.0, 1)
    assert abs(results[True]) < 3.0 < results[False]

    # Under the spot measure before the first reset the numeraire is P(t, T0), so
    # P(t, T1) / P(t, T0) = 1 / (1 + tau L1) must keep its initial expectation: the front rate needs a positive drift.
    spot_target = 1.0 / (1.0 + tau * f1)
    spot_results = {}
    for use_drift in (True, False):
        rng = np.random.default_rng(1997)
        x1 = np.full(n_paths, f1)
        for _ in range(n_steps):
            z1 = rng.standard_normal(n_paths)
            drift = tau * x1 / (1.0 + tau * x1) * s1 * s1 if use_drift else 0.0
            x1 = x1 * np.exp((drift - 0.5 * s1 * s1) * dt + s1 * math.sqrt(dt) * z1)
        ratio_paths = 1.0 / (1.0 + tau * x1)
        mean = float(ratio_paths.mean())
        stderr = float(ratio_paths.std()) / math.sqrt(n_paths)
        spot_results[use_drift] = (mean - spot_target) / stderr
    quoted("spot-measure martingale target 1 / (1 + L1)", spot_target, 0.9091, 4)
    quoted("spot measure, front-rate drift: error in standard errors", spot_results[True], 0.9, 1)
    quoted("spot measure, driftless front rate: error in standard errors", spot_results[False], 33.1, 1)
    assert abs(spot_results[True]) < 3.0 < spot_results[False], "the front rate must drift under the spot measure"


def main() -> None:
    print("=== fi_term_structure: Term Structure Models (HJM, LGM, LMM) ===")
    example_hjm()
    example_lgm()
    example_lmm()
    print(f"\nSuccessfully verified {len(QUOTED)} term structure figures.")


if __name__ == "__main__":
    main()
