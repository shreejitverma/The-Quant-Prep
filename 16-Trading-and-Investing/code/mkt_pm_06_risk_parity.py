"""Risk parity and the All Weather framework: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Portfolio-Management/06-Risk-Parity-and-The-All-Weather-Framework.md`.
Independent routes used here:
- the 60/40 variance terms in exact fractions, against Euler risk contributions from a finite-difference gradient
  and a seeded simulation of portfolio returns;
- equal-risk-contribution weights by Newton's method on the Maillard-Roncalli-Teiletche log-barrier problem,
  against cyclical coordinate descent and against the inverse-volatility closed form when correlations are equal;
- the levered sleeve sizes in exact fractions, and the unlevered volatility against a seeded simulation.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_pm_06_risk_parity.py
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
    print(f"{label:64s} {float(value):16.6f}  quoted {quoted}")
    assert abs(float(value) - float(quoted)) <= tol, f"{label}: {float(value)} does not round to {quoted}"
    return float(value)


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:58s} |diff| = {abs(a - b):.2e} (tol {tol:.1e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def sixty_forty() -> None:
    print("60/40 with sigma_E = 16%, sigma_B = 5%, rho = 0 (hypothetical)")
    we, wb, se, sb = Fraction(60, 100), Fraction(40, 100), Fraction(16, 100), Fraction(5, 100)
    eq_term, bd_term = we**2 * se**2, wb**2 * sb**2
    var = eq_term + bd_term
    q("equity variance term", eq_term, "0.009216")
    q("bond variance term", bd_term, "0.000400")
    q("portfolio variance", var, "0.009616")
    q("portfolio volatility (%)", 100 * math.sqrt(var), "9.806")
    q("equity share of variance (%)", 100 * eq_term / var, "95.84")
    q("bond share of variance (%)", 100 * bd_term / var, "4.16")
    w = np.array([0.6, 0.4])
    cov = np.diag([0.16**2, 0.05**2])
    sig = math.sqrt(w @ cov @ w)
    h = 1e-6
    grad = np.array(
        [(math.sqrt((w + h * e) @ cov @ (w + h * e)) - math.sqrt((w - h * e) @ cov @ (w - h * e))) / (2 * h) for e in np.eye(2)]
    )
    trc = w * grad
    close("Euler: sum of TRC equals sigma_p", trc.sum(), sig, 1e-9)
    close("finite-difference equity TRC share vs exact", trc[0] / sig, float(eq_term / var), 1e-8)
    rng = np.random.default_rng(SEED)
    z = rng.standard_normal((2_000_000, 2)) * np.array([0.16, 0.05])
    p = z @ w
    sim = np.cov(0.6 * z[:, 0], p)[0, 1] / p.var(ddof=1)
    batches = [np.cov(0.6 * a, b)[0, 1] / b.var(ddof=1) for a, b in zip(np.split(z[:, 0], 40), np.split(p, 40), strict=True)]
    close("simulated equity share (5 standard errors)", sim, float(eq_term / var), 5 * np.std(batches, ddof=1) / math.sqrt(40))


def erc_newton(cov: np.ndarray) -> np.ndarray:
    """Minimise 0.5 x' S x - sum(ln x) by Newton's method; normalise to weights."""
    x = 1 / np.sqrt(np.diag(cov))
    for _ in range(100):
        g = cov @ x - 1 / x
        hess = cov + np.diag(1 / x**2)
        x = x - np.linalg.solve(hess, g)
    return x / x.sum()


def erc_ccd(cov: np.ndarray) -> np.ndarray:
    """Cyclical coordinate descent on x_i (S x)_i = 1 (Griveau-Billion, Richard and Roncalli 2013)."""
    n = len(cov)
    x = np.ones(n)
    for _ in range(2000):
        for i in range(n):
            b = cov[i] @ x - cov[i, i] * x[i]
            x[i] = (-b + math.sqrt(b * b + 4 * cov[i, i])) / (2 * cov[i, i])
    return x / x.sum()


def risk_parity() -> None:
    print("Equal risk contribution: equities 16%, Treasuries 5%, commodities 20% (hypothetical)")
    vol = np.array([0.16, 0.05, 0.20])
    for rho in (0.0, 0.3):
        cov = np.outer(vol, vol) * (rho + (1 - rho) * np.eye(3))
        newton, ccd = erc_newton(cov), erc_ccd(cov)
        inv = (1 / vol) / (1 / vol).sum()
        for i in range(3):
            close(f"Newton vs coordinate descent, rho = {rho}, asset {i}", newton[i], ccd[i], 1e-10)
            close(f"Newton vs inverse volatility, rho = {rho}, asset {i}", newton[i], inv[i], 1e-10)
        trc = newton * (cov @ newton)
        close(f"risk contributions equal at rho = {rho}", trc.max() - trc.min(), 0.0, 1e-14)
    corr = np.array([[1.0, -0.2, 0.3], [-0.2, 1.0, 0.1], [0.3, 0.1, 1.0]])
    cov = np.outer(vol, vol) * corr
    newton, ccd = erc_newton(cov), erc_ccd(cov)
    close("Newton vs coordinate descent, unequal correlations", float(np.abs(newton - ccd).max()), 0.0, 1e-10)
    q("inverse volatility of equities 1 / 0.16", 1 / 0.16, "6.25")
    q("inverse volatility of Treasuries 1 / 0.05", 1 / 0.05, "20")
    q("inverse volatility of commodities 1 / 0.20", 1 / 0.20, "5")
    total = Fraction(625, 100) + 20 + 5
    q("sum of inverse volatilities", total, "31.25")
    sleeves = [200 * Fraction(625, 100) / total, 200 * 20 / total, 200 * 5 / total]
    for name, val, lit in zip(("equities", "Treasuries", "commodities"), sleeves, ("40", "128", "32"), strict=True):
        q(f"levered sleeve, {name} ($)", val, lit)
    for name, val, v in zip(
        ("equities", "Treasuries", "commodities"), sleeves, (Fraction(16, 100), Fraction(5, 100), Fraction(20, 100)), strict=True
    ):
        q(f"standalone dollar volatility, {name} ($)", val * v, "6.40")
    q("Treasury capital weight (%)", 100 * sleeves[1] / 200, "64")
    unlev = math.sqrt(sum((float(s) / 200 * v) ** 2 for s, v in zip(sleeves, vol, strict=True)))
    rng = np.random.default_rng(SEED + 1)
    z = rng.standard_normal((2_000_000, 3)) * vol
    pr = z @ (np.array([float(s) for s in sleeves]) / 200)
    se = unlev / math.sqrt(2 * len(pr))
    close("simulated unlevered volatility (5 standard errors)", pr.std(ddof=1), unlev, 5 * se)
    q("unlevered volatility at zero correlation (%)", 100 * unlev, "5.54")
    q("leverage for a 10% volatility target", 0.10 / unlev, "1.80")


def main() -> None:
    sixty_forty()
    risk_parity()
    print("all risk-parity checks passed")


if __name__ == "__main__":
    main()
