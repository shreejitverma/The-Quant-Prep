"""Cost of capital, WACC and terminal value traps: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/Investing/Valuation Models/02-Cost-of-Capital-WACC-and-Terminal-Value-Traps.md`.
Independent routes used here:
- the relevered beta, cost of equity and WACC in exact rational arithmetic (fractions.Fraction), with the
  relevered beta checked by unlevering it back to the peer asset beta;
- each value-driver terminal value against a year-by-year simulation of the steady state: invest
  g / RONIC of NOPAT, earn RONIC on it from the next year, discount 3,000 years of free cash flow and
  add the closed-form tail; RONIC = WACC must then equal the zero-growth perpetuity NOPAT / WACC;
- spread sensitivities as ratios of separately evaluated terminal values;
- the regression-beta standard error against a seeded Monte Carlo of 60-month regressions, with a
  tolerance of four Monte Carlo standard errors.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_val_02_wacc.py`.
"""

from __future__ import annotations

from fractions import Fraction as F

import numpy as np


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


def simulated_tv(nopat_next: float, g: float, ronic: float, wacc: float, years: int = 3000) -> float:
    """Value at year N of FCFF from year N+1 on, built year by year from the reinvestment rule."""
    rr = g / ronic
    nopat, value = nopat_next, 0.0
    for k in range(1, years + 1):
        invest = rr * nopat
        value += (nopat - invest) / (1 + wacc) ** k
        nopat += ronic * invest  # new capital earns RONIC from the following year
    # closed-form tail of the remaining growing perpetuity
    return value + (nopat * (1 - rr)) / (wacc - g) / (1 + wacc) ** years


def wacc_case() -> None:
    print("Worked case steps 1-4: Global Logistics cost of capital (cards mkt-val-035, mkt-val-259)")
    rf, erp, beta_u, t = F(4, 100), F(5, 100), F(8, 10), F(25, 100)
    d_v, e_v = F(30, 100), F(70, 100)
    de = d_v / e_v
    approx("D/E", de, 0.4286, 4)
    approx("(1 - t) x D/E", (1 - t) * de, 0.3214, 4)
    beta_l = beta_u * (1 + (1 - t) * de)
    exact("relevered beta (exact)", beta_l, F(37, 35))
    approx("relevered beta", beta_l, 1.057, 3)
    # Independent check: unlever the target beta back to the asset beta.
    exact("unlevered back to the peer beta", beta_l / (1 + (1 - t) * de), beta_u)
    ke = rf + beta_l * erp
    approx("beta x ERP (percent)", 100 * beta_l * erp, 5.2857, 4)
    approx("cost of equity (percent)", 100 * ke, 9.2857, 4)
    coverage = F(200, 25)
    exact("interest coverage", coverage, 8)
    kd = rf + F(120, 10000)
    approx("pre-tax cost of debt (percent)", 100 * kd, 5.20, 2)
    approx("after-tax cost of debt (percent)", 100 * kd * (1 - t), 3.90, 2)
    exact("equity term of WACC (percent)", 100 * e_v * ke, F(65, 10))
    approx("debt term of WACC (percent)", 100 * d_v * kd * (1 - t), 1.170, 3)
    wacc = e_v * ke + d_v * kd * (1 - t)
    exact("WACC (percent, exact)", 100 * wacc, F(767, 100))
    approx("relevered beta (five decimals)", beta_l, 1.05714, 5)
    # Damodaran ratings page, data as of January 2026: large non-financial firms, 6.5x-8.5x -> Aa2/AA, 0.55%.
    kd_dam = rf + F(55, 10000)
    approx("Kd with the January 2026 table (percent)", 100 * kd_dam, 4.55, 2)
    approx("after-tax Kd with the January 2026 table (percent)", 100 * kd_dam * (1 - t), 3.4125, 4)
    approx("WACC with the January 2026 table (percent)", 100 * (e_v * ke + d_v * kd_dam * (1 - t)), 7.52, 2)


def terminal_scenarios() -> None:
    print("Worked case step 5: terminal value under three RONIC scenarios (cards mkt-val-043, mkt-val-059)")
    wacc, g = 0.0767, 0.025
    nopat6 = 180.0 * (1 + g)
    approx("year 6 NOPAT", nopat6, 184.50, 2)
    approx("WACC - g", wacc - g, 0.0517, 4)
    # A: RONIC 20%
    rr_a = g / 0.20
    approx("reinvestment rate A (percent)", 100 * rr_a, 12.5, 1)
    approx("FCFF6 A", nopat6 * (1 - rr_a), 161.44, 2)
    tv_a = nopat6 * (1 - rr_a) / (wacc - g)
    approx("TV A (simulated)", simulated_tv(nopat6, g, 0.20, wacc), 3122.6, 1)
    approx("TV A (value driver)", tv_a, 3122.6, 1)
    # B: RONIC = WACC
    rr_b = g / wacc
    approx("reinvestment rate B (percent)", 100 * rr_b, 32.6, 1)
    approx("reinvestment rate B (percent, four decimals)", 100 * rr_b, 32.5945, 4)
    approx("FCFF6 B", nopat6 * (1 - rr_b), 124.363, 3)
    tv_b = nopat6 * (1 - rr_b) / (wacc - g)
    approx("TV B (simulated)", simulated_tv(nopat6, g, wacc, wacc), 2405.5, 1)
    approx("TV B (value driver)", tv_b, 2405.5, 1)
    approx("NOPAT6 / WACC (zero-growth perpetuity)", nopat6 / wacc, 2405.5, 1)
    # C: zero reinvestment
    tv_c = nopat6 / (wacc - g)
    approx("TV C (naive)", tv_c, 3568.7, 1)
    approx("naive overstatement vs B", tv_c - tv_b, 1163.2, 1)
    approx("naive overstatement vs B (percent)", 100 * (tv_c / tv_b - 1), 48.4, 1)
    # A naive model is RONIC = infinity: the simulation with a huge RONIC converges to it.
    approx("TV with RONIC = 1e9 (simulated)", simulated_tv(nopat6, g, 1e9, wacc), 3568.7, 1)
    print("Card mkt-val-059: exit multiple and implied growth")
    approx("scenario A TV / year-5 NOPAT (implied EV/NOPAT exit multiple)", tv_a / 180.0, 17.35, 2)

    def multiple(gg: float) -> float:
        return (1 + gg) * (1 - gg / 0.20) / (wacc - gg)

    lo, hi = 0.0, wacc - 1e-9
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if multiple(mid) < 20.0 else (lo, mid)
    # Closed form: (1 + g)(1 - 5 g) = 20 (WACC - g) rearranges to 5 g^2 - 16 g + (20 WACC - 1) = 0.
    a, b, c = 5.0, -(20.0 - 4.0), 20.0 * wacc - 1.0
    g_closed = (-b - np.sqrt(b * b - 4 * a * c)) / (2 * a)
    approx("g implied by a 20x EV/NOPAT exit, RONIC 20% (bisection, percent)", 100 * lo, 3.37, 2)
    approx("g implied by a 20x EV/NOPAT exit, RONIC 20% (quadratic, percent)", 100 * g_closed, 3.37, 2)


def spread_sensitivity() -> None:
    print("Core concepts 4 and card mkt-val-046: (WACC - g) sensitivity")
    base = 1 / (0.0767 - 0.025)
    approx("TV change if spread narrows 50 bp (percent)", 100 * ((1 / (0.0717 - 0.025)) / base - 1), 10.7, 1)
    approx("TV change if spread widens 50 bp (percent)", 100 * ((1 / (0.0817 - 0.025)) / base - 1), -8.8, 1)
    base7 = 1 / (0.07 - 0.025)
    approx("WACC 7%, g 2.5%: spread -100 bp (percent)", 100 * ((1 / (0.06 - 0.025)) / base7 - 1), 28.6, 1)
    approx("WACC 7%, g 2.5%: spread +100 bp (percent)", 100 * ((1 / (0.08 - 0.025)) / base7 - 1), -18.2, 1)


def regression_beta_noise() -> None:
    print("Core concepts 2: standard error of a 60-month regression beta (hypothetical inputs, card mkt-val-260)")
    n, beta = 60, 1.0
    sig_m, sig_e = 0.15 / np.sqrt(12), 0.30 / np.sqrt(12)
    # Var(beta_hat) = sig_e^2 E[1 / sum (x - xbar)^2] = (sig_e / sig_m)^2 / (n - 3) for normal market returns.
    se_closed = (sig_e / sig_m) / np.sqrt(n - 3)
    approx("sigma_e / sigma_m", sig_e / sig_m, 2.0, 6)
    approx("standard error, closed form", se_closed, 0.26, 2)
    rng = np.random.default_rng(20261114)
    reps = 40_000
    x = rng.normal(0.0, sig_m, size=(reps, n))
    y = beta * x + rng.normal(0.0, sig_e, size=(reps, n))
    xc = x - x.mean(axis=1, keepdims=True)
    b = (xc * (y - y.mean(axis=1, keepdims=True))).sum(axis=1) / (xc**2).sum(axis=1)
    sd = float(b.std(ddof=1))
    mc_se = sd / np.sqrt(2 * (reps - 1))
    print(f"    Monte Carlo sd of beta_hat = {sd:.4f} (MC standard error {mc_se:.4f}, seed 20261114)")
    assert abs(sd - se_closed) < 4 * mc_se, (sd, se_closed, mc_se)
    approx("Monte Carlo sd of beta_hat", sd, 0.26, 2)
    approx("95% interval half-width (1.96 x SE)", 1.96 * se_closed, 0.52, 2)


if __name__ == "__main__":
    wacc_case()
    terminal_scenarios()
    spread_sensitivity()
    regression_beta_noise()
    print("all cost-of-capital numbers check out")
