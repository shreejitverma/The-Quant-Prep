"""Track-record statistics, return attribution, capacity, and forecast calibration.

Backs 13-Interview-Playbook/12-Senior-Level-Expectations.md (sections 1 to 4) and
13-Interview-Playbook/09-Behavioral-and-Fit.md (section 5, calibrated confidence).

1. How long a track record must be before its Sharpe ratio is statistically meaningful.
2. Luck among many managers: how many zero-skill records look excellent.
3. Attribution of a seeded synthetic monthly track record into market beta, a style factor and alpha.
4. Capacity: the AUM that maximises dollar P&L when impact grows with the square root of size.
5. Calibration: a binomial test of stated confidence and Brier scores.

Run: uv run --no-project --with numpy python 13-Interview-Playbook/code/track_record.py
"""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

ND = NormalDist()


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".2f") -> None:
    """Print `label = value` and assert it matches the literal the note quotes, to tolerance and to the printed digits."""
    printed, quoted = (s.removeprefix("-") if float(s) == 0 else s for s in (f"{value:{fmt}}", f"{expected:{fmt}}"))
    print(f"{label} = {printed}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    assert printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"


def section_significance() -> None:
    print("\n== 1. Track-record length ==")
    # Backs int-senior-sharpe-tstat and the Core concepts table: t = SR * sqrt(years), years = (t / SR)^2.
    for sr, years, t in ((0.5, 3.0, 0.87), (1.0, 3.0, 1.73), (1.5, 3.0, 2.60), (2.0, 3.0, 3.46)):
        check(f"t-stat of Sharpe {sr} over {years:g} years", sr * math.sqrt(years), t, 0.005)
    for sr, need in ((0.5, 16.0), (0.75, 7.1), (1.0, 4.0), (1.5, 1.8)):
        check(f"years for Sharpe {sr} to reach t = 2", (2 / sr) ** 2, need, 0.05, ".1f")


def section_luck() -> None:
    print("\n== 2. Luck among many managers ==")
    # Backs int-senior-lucky-managers: 1000 zero-skill managers, 3-year records, annualised Sharpe SE ~ 1/sqrt(3).
    se = 1 / math.sqrt(3)
    check("Sharpe standard error over 3 years", se, 0.58, 0.005)
    p = 1 - ND.cdf(1.5 / se)
    check("P(zero-skill 3-year Sharpe above 1.5)", p, 0.0047, 5e-5, ".4f")
    check("expected count above 1.5 out of 1000", 1000 * p, 4.7, 0.05, ".1f")
    rng = np.random.default_rng(5)
    daily = rng.standard_normal((1000, 756)) * 0.01  # 1000 managers, 3 years of daily zero-mean returns
    sr = daily.mean(axis=1) / daily.std(axis=1, ddof=1) * math.sqrt(252)
    check("simulated count above 1.5 out of 1000 (seed 5)", float((sr > 1.5).sum()), 4.0, 0.0, ".0f")


def section_attribution() -> None:
    print("\n== 3. Attribution of a monthly track record ==")
    # Backs Worked example 2 and int-senior-attribution-alpha. True model: r = 0.25% + 0.5 m + 0.4 f + e, monthly.
    rng = np.random.default_rng(12)
    n = 60
    m = 0.007 + 0.045 * rng.standard_normal(n)  # market excess return
    f = 0.003 + 0.030 * rng.standard_normal(n)  # a style factor (for example momentum)
    e = 0.015 * rng.standard_normal(n)
    r = 0.0025 + 0.5 * m + 0.4 * f + e
    x = np.column_stack([np.ones(n), m, f])
    coef, *_ = np.linalg.lstsq(x, r, rcond=None)
    resid = r - x @ coef
    s2 = resid @ resid / (n - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(x.T @ x)))
    total = 12 * r.mean()
    parts = 12 * np.array([coef[0], coef[1] * m.mean(), coef[2] * f.mean()])
    # OLS with an intercept reproduces the sample mean exactly: alpha + beta mean(m) + gamma mean(f) = mean(r).
    assert abs(parts.sum() - total) < 1e-12
    sharpe = r.mean() / r.std(ddof=1) * math.sqrt(12)
    check("headline annualised return (%)", 100 * total, 10.09, 0.005)
    check("headline annualised Sharpe", sharpe, 1.08, 0.005)
    check("estimated market beta", float(coef[1]), 0.47, 0.005)
    check("estimated factor loading", float(coef[2]), 0.42, 0.005)
    check("return from market beta (%/yr)", 100 * float(parts[1]), 7.68, 0.005)
    check("return from the style factor (%/yr)", 100 * float(parts[2]), 0.55, 0.005)
    check("alpha (%/yr)", 100 * float(parts[0]), 1.85, 0.005)
    check("alpha t-stat", float(coef[0] / se[0]), 0.75, 0.005)
    check("R-squared", float(1 - resid @ resid / ((r - r.mean()) @ (r - r.mean()))), 0.70, 0.005)
    check("annualised information ratio of the residual", float((coef[0]) / math.sqrt(s2) * math.sqrt(12)), 0.35, 0.005)


def section_capacity() -> None:
    print("\n== 4. Capacity ==")
    # Backs int-senior-capacity-one-third: net alpha a(A) = a0 - c sqrt(A); dollar P&L A a(A) peaks at sqrt(A*) = 2 a0 / (3c).
    a0, gone_at = 0.06, 1000.0  # gross alpha 6%/yr at tiny size; impact eats all of it at 1000 (illustrative units of AUM)
    c = a0 / math.sqrt(gone_at)
    grid = np.linspace(0.0, gone_at, 1_000_001)
    pnl = grid * (a0 - c * np.sqrt(grid))
    a_star = float(grid[pnl.argmax()])
    check("P&L-maximising AUM (grid)", a_star, 444.4, 0.05, ".1f")
    check("P&L-maximising AUM (closed form, (2/3)^2 x 1000)", (2 * a0 / (3 * c)) ** 2, 444.4, 0.05, ".1f")
    check("net alpha at that AUM (%)", 100 * (a0 - c * math.sqrt(a_star)), 2.00, 0.005)
    check("max dollar P&L (units of AUM x return)", float(pnl.max()), 8.89, 0.005)
    check("net alpha at half the break-even size, 500 (%)", 100 * (a0 - c * math.sqrt(500.0)), 1.76, 0.005)


def section_calibration() -> None:
    print("\n== 5. Calibration (note 09) ==")
    # Backs int-beh-calibration-binomial: 10 answers at stated 90% confidence, only 6 right.
    p_le_6 = sum(math.comb(10, k) * 0.9**k * 0.1 ** (10 - k) for k in range(7))
    check("P(6 or fewer right out of 10 | truly 90%)", p_le_6, 0.0128, 5e-5, ".4f")
    # Backs int-beh-brier-score.
    probs = np.array([0.9, 0.9, 0.8, 0.7, 0.6, 0.3, 0.2, 0.1])
    outcome = np.array([1, 1, 1, 0, 1, 0, 0, 0])
    check("Brier score of the stated probabilities", float(np.mean((probs - outcome) ** 2)), 0.1062, 5e-5, ".4f")
    check("Brier score of always saying 50%", float(np.mean((0.5 - outcome) ** 2)), 0.2500, 1e-12, ".4f")
    sure = np.where(probs > 0.5, 0.99, 0.01)  # the same calls, each stated as near-certain
    check("Brier score of the same calls stated at 99% or 1%", float(np.mean((sure - outcome) ** 2)), 0.1226, 5e-5, ".4f")
    miss = int(np.flatnonzero((sure > 0.5) != (outcome == 1))[0])
    check("Brier cost of the single confident miss", float((sure[miss] - outcome[miss]) ** 2), 0.9801, 5e-5, ".4f")


if __name__ == "__main__":
    section_significance()
    section_luck()
    section_attribution()
    section_capacity()
    section_calibration()
    print("\nAll checks passed.")
