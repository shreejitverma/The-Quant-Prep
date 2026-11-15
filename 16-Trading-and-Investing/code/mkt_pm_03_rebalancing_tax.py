"""Rebalancing, tax drag and execution friction: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Portfolio-Management/03-Portfolio-Rebalancing-Tax-Drag-and-Execution-Friction.md`.
Independent routes used here:
- the drift example by compounding each sleeve year by year in exact fractions, against closed-form powers;
- portfolio volatility from the 2x2 covariance quadratic form, against a seeded simulation;
- the diversification (rebalancing) return by simulating daily-rebalanced geometric Brownian motion and averaging
  the per-step excess of portfolio log growth over the weighted asset log growth, against 0.5 w1 w2 (s1^2 + s2^2 - 2 s12);
- corridor bands, weights and trades in exact fractions;
- the tax example by compounding year by year in exact fractions, against floating-point powers.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_pm_03_rebalancing_tax.py
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261114


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:64s} {float(value):18.6f}  quoted {quoted}")
    assert abs(float(value) - float(quoted)) <= tol, f"{label}: {float(value)} does not round to {quoted}"
    return float(value)


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:58s} |diff| = {abs(a - b):.2e} (tol {tol:.1e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def drift() -> None:
    print("Unrebalanced 60/40 drift, equities +10% a year, bonds +2% a year, 10 years (hypothetical)")
    eq, bd = Fraction(60), Fraction(40)
    for _ in range(10):
        eq *= Fraction(110, 100)
        bd *= Fraction(102, 100)
    w = eq / (eq + bd)
    close("loop vs closed form equity weight", float(w), 0.6 * 1.1**10 / (0.6 * 1.1**10 + 0.4 * 1.02**10), 1e-12)
    q("equity weight after 10 years (%)", 100 * float(w), "76.1")
    q("bond weight after 10 years (%)", 100 * float(bd / (eq + bd)), "23.9")
    rng = np.random.default_rng(SEED)
    z = rng.standard_normal((2_000_000, 2))
    for weight, quoted in ((0.6, "9.81"), (float(w), "12.24")):
        closed = math.sqrt((weight * 0.16) ** 2 + ((1 - weight) * 0.05) ** 2)
        sim = (weight * 0.16 * z[:, 0] + (1 - weight) * 0.05 * z[:, 1]).std(ddof=1)
        se = closed / math.sqrt(2 * len(z))
        close(f"simulated volatility at equity weight {weight:.4f} (5 standard errors)", sim, closed, 5 * se)
        q(f"volatility at equity weight {weight:.4f} (%)", 100 * closed, quoted)
    vol = [math.sqrt((x * 0.16) ** 2 + ((1 - x) * 0.05) ** 2) for x in (0.6, float(w))]
    q("relative increase in volatility (%)", 100 * (vol[1] / vol[0] - 1), "25")


def diversification_return() -> None:
    print("Diversification return of a daily-rebalanced 50/50 mix, sigma 20% each (hypothetical)")
    for rho, quoted in ((0.0, "1.00"), (0.5, "0.50")):
        w1 = w2 = 0.5
        s1 = s2 = 0.20
        closed = 0.5 * w1 * w2 * (s1 * s1 + s2 * s2 - 2 * rho * s1 * s2)
        rng = np.random.default_rng(SEED + int(10 * rho))
        dt, steps = 1 / 252, 252 * 400
        z1 = rng.standard_normal(steps)
        z2 = rho * z1 + math.sqrt(1 - rho * rho) * rng.standard_normal(steps)
        mu = 0.08
        r1 = (mu - 0.5 * s1 * s1) * dt + s1 * math.sqrt(dt) * z1
        r2 = (mu - 0.5 * s2 * s2) * dt + s2 * math.sqrt(dt) * z2
        excess = np.log(w1 * np.exp(r1) + w2 * np.exp(r2)) - (w1 * r1 + w2 * r2)
        annual = excess.mean() / dt
        se = excess.std(ddof=1) / math.sqrt(steps) / dt
        close(f"simulated diversification return at rho = {rho} (5 standard errors)", annual, closed, 5 * se)
        q(f"diversification return at rho = {rho} (% a year)", 100 * closed, quoted)


def corridors() -> None:
    print("Relative +/-20% corridors and the year-1 shock (hypothetical)")
    for target, lo_q, hi_q in ((60, "48.0", "72.0"), (30, "24.0", "36.0"), (10, "8.0", "12.0"), (5, "4.0", "6.0")):
        q(f"lower band for {target}% target (%)", Fraction(target) * Fraction(8, 10), lo_q)
        q(f"upper band for {target}% target (%)", Fraction(target) * Fraction(12, 10), hi_q)
    eq, fi, au = Fraction(1_550_000), Fraction(520_000), Fraction(230_000)
    total = eq + fi + au
    q("total portfolio value ($)", total, "2300000")
    q("equity weight (%)", 100 * eq / total, "67.39")
    q("fixed income weight (%)", 100 * fi / total, "22.61")
    q("gold weight (%)", 100 * au / total, "10.00")
    q("fixed income target ($)", total * Fraction(30, 100), "690000")
    q("fixed income purchase ($)", total * Fraction(30, 100) - fi, "170000")
    q("equity target ($)", total * Fraction(60, 100), "1380000")
    q("equity trim ($)", eq - total * Fraction(60, 100), "170000")
    q("wash-sale window 30 + 1 + 30 (days)", 30 + 1 + 30, "61")


def tax_drag() -> None:
    print("Tax drag: $1,000,000, 10% gross, 30 years, 25% blended tax (hypothetical)")
    taxed, deferred = Fraction(1_000_000), Fraction(1_000_000)
    for _ in range(30):
        taxed *= 1 + Fraction(10, 100) * Fraction(75, 100)
        deferred *= Fraction(110, 100)
    close("taxed loop vs float power", float(taxed), 1e6 * 1.075**30, 1e-6)
    close("deferred loop vs float power", float(deferred), 1e6 * 1.1**30, 1e-6)
    after_tax = deferred - Fraction(25, 100) * (deferred - 1_000_000)
    q("annual net return 10% x (1 - 0.25) (%)", 10 * Fraction(75, 100), "7.50")
    q("terminal wealth with annual tax ($)", taxed, "8754955")
    q("pre-tax deferred terminal wealth ($)", deferred, "17449402")
    q("after-tax deferred terminal wealth ($)", after_tax, "13337052")
    q("difference ($)", after_tax - taxed, "4582097")
    q("difference as share of deferred after-tax wealth (%)", 100 * (after_tax - taxed) / after_tax, "34.4")
    cagr = float(after_tax / 1_000_000) ** (1 / 30) - 1
    lo, hi = 0.0, 0.2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (1 + mid) ** 30 < float(after_tax / 1_000_000):
            lo = mid
        else:
            hi = mid
    close("after-tax CAGR bisection vs closed form", 0.5 * (lo + hi), cagr, 1e-12)
    q("after-tax CAGR of the deferred account (%)", 100 * cagr, "9.02")
    q("annual tax drag 9.02 - 7.50 (pp)", 100 * cagr - 7.5, "1.52")
    q("tax-equivalent yield of a 3.5% muni at a 37% rate (%)", 3.5 / (1 - 0.37), "5.56")


def main() -> None:
    drift()
    diversification_return()
    corridors()
    tax_drag()
    print("all rebalancing and tax checks passed")


if __name__ == "__main__":
    main()
