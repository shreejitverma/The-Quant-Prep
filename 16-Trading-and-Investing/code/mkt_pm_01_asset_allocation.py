"""Asset allocation and the benchmark to beat: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Portfolio-Management/01-Asset-Allocation-and-The-Benchmark-to-Beat.md`.
Independent routes used here:
- Brinson, Singer and Beebower (1991) increments from the published R-squared values (Figure G) in exact decimals;
- fee drag by compounding both wealth paths year by year in exact rational arithmetic, against the closed form;
- building-block returns and portfolio sums in exact fractions, against floating-point dot products;
- the CAPE repricing drag by bisection on (1 + x)^10 = ratio, against the closed-form root;
- the 60/40 equity share of variance from Euler risk contributions, against a finite-difference gradient
  of portfolio volatility and against a seeded simulation of correlated returns.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_pm_01_asset_allocation.py
"""

from __future__ import annotations

import math
from decimal import Decimal
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


def bsb_increments() -> None:
    print("Brinson, Singer and Beebower (1991), Figure G: average R-squared of actual on constructed returns")
    policy, policy_timing, policy_selection = Decimal("91.5"), Decimal("93.3"), Decimal("96.1")
    q("timing increment 93.3 - 91.5 (pp)", policy_timing - policy, "1.8")
    q("selection increment 96.1 - 91.5 (pp)", policy_selection - policy, "4.6")
    q("residual 100 - 91.5 - 1.8 - 4.6 (pp)", Decimal(100) - policy - (policy_timing - policy) - (policy_selection - policy), "2.1")
    # Table III: policy 13.49% a year, actual portfolio 13.41% a year
    q("BSB actual minus policy return (pp a year)", Decimal("13.41") - Decimal("13.49"), "-0.08")


def fee_drag() -> None:
    print("Fee drag over 30 years")
    years, fee = 30, Fraction(15, 1000)
    for gross_pct, quoted in ((0, "36.5"), (7, "34.5")):
        r = Fraction(gross_pct, 100)
        gross, net = Fraction(1), Fraction(1)
        for _ in range(years):
            gross *= 1 + r
            net *= 1 + r - fee
        loop = 1 - net / gross
        closed = 1 - ((1 + gross_pct / 100 - 0.015) / (1 + gross_pct / 100)) ** years
        close(f"loop vs closed form at R = {gross_pct}%", float(loop), closed, 1e-12)
        q(f"share of terminal wealth lost at R = {gross_pct}% (%)", 100 * float(loop), quoted)


def benchmark_hurdle() -> None:
    print("Hypothetical strategy vs index fund")
    q("strategy net return 9.5 - 2.0 (%)", Decimal("9.5") - Decimal("2.0"), "7.5")
    q("index net return 9.0 - 0.03 (%)", Decimal("9.0") - Decimal("0.03"), "8.97")


def building_blocks() -> None:
    print("Endowment case study (hypothetical inputs)")
    f = Fraction
    q("additive required return 4.5 + 2.5 (%)", f(45, 10) + f(25, 10), "7.0")
    q("exact required return (1.045)(1.025) - 1 (%)", 100 * ((1 + f(45, 1000)) * (1 + f(25, 1000)) - 1), "7.1125")
    equity = f(22, 10) + f(20, 10) + f(25, 10) - f(7, 10)
    tips = f(20, 10) + f(25, 10)
    reit = f(50, 10) + f(10, 10) + f(25, 10)
    tsy = f(42, 10)
    q("global equities building blocks (%)", equity, "6.0")
    q("TIPS building blocks (%)", tips, "4.5")
    q("global REITs building blocks (%)", reit, "8.5")
    w6040 = [f(60, 100), f(40, 100)]
    r6040 = w6040[0] * equity + w6040[1] * tsy
    close("60/40 fraction vs float dot product", float(r6040), float(np.dot([0.6, 0.4], [6.0, 4.2])), 1e-12)
    q("60/40 equity term (%)", w6040[0] * equity, "3.60")
    q("60/40 Treasury term (%)", w6040[1] * tsy, "1.68")
    q("60/40 expected return (%)", r6040, "5.28")
    q("60/40 shortfall vs 7.0% (pp)", f(7) - r6040, "1.72")
    weights = [f(50, 100), f(20, 100), f(15, 100), f(15, 100)]
    rets = [equity, reit, tips, tsy]
    terms = [w * r for w, r in zip(weights, rets, strict=True)]
    for (label, quoted), t in zip(
        (("equity term", "3.00"), ("real estate term", "1.70"), ("TIPS term", "0.675"), ("Treasury term", "0.63")), terms, strict=True
    ):
        q(f"diversified {label} (%)", t, quoted)
    div = sum(terms)
    close("diversified fraction vs float dot product", float(div), float(np.dot([0.5, 0.2, 0.15, 0.15], [6.0, 8.5, 4.5, 4.2])), 1e-12)
    q("diversified expected return (%)", div, "6.005")
    q("diversified shortfall vs 7.0% (pp)", f(7) - div, "0.995")
    q("required return at 3.5% spending, additive (%)", f(35, 10) + f(25, 10), "6.0")


def cape_drag() -> None:
    print("CAPE repricing drag over 10 years (hypothetical CAPE path)")
    for end, quoted in ((18.0, "-6.70"), (30.0, "-1.81")):
        ratio = end / 36.0
        closed = ratio**0.1 - 1
        lo, hi = -0.5, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if (1 + mid) ** 10 > ratio:
                hi = mid
            else:
                lo = mid
        close(f"bisection vs closed form, CAPE 36 -> {end:.0f}", 0.5 * (lo + hi), closed, 1e-12)
        q(f"annual repricing return, CAPE 36 -> {end:.0f} (%)", 100 * closed, quoted)


def equity_risk_share(rho: float) -> tuple[float, float]:
    w = np.array([0.6, 0.4])
    vol = np.array([0.16, 0.05])
    cov = np.outer(vol, vol) * np.array([[1.0, rho], [rho, 1.0]])
    sig = math.sqrt(w @ cov @ w)
    euler = w[0] * (cov @ w)[0] / sig / sig
    h = 1e-6
    bumped = w.copy()
    bumped[0] += h
    down = w.copy()
    down[0] -= h
    grad = (math.sqrt(bumped @ cov @ bumped) - math.sqrt(down @ cov @ down)) / (2 * h)
    return euler, w[0] * grad / sig


def sixty_forty_risk() -> None:
    print("60/40 equity share of variance, sigma_E 16%, sigma_B 5% (hypothetical)")
    q("equity / bond volatility ratio", 0.16 / 0.05, "3.2")
    rng = np.random.default_rng(SEED)
    n = 2_000_000
    for rho, quoted in ((0.0, "95.8"), (0.5, "88.2"), (-0.2, "99.8")):
        euler, fd = equity_risk_share(rho)
        close(f"Euler vs finite difference at rho = {rho}", euler, fd, 1e-8)
        z = rng.standard_normal((n, 2))
        e = 0.16 * z[:, 0]
        b = 0.05 * (rho * z[:, 0] + math.sqrt(1 - rho * rho) * z[:, 1])
        p = 0.6 * e + 0.4 * b
        sim = np.cov(0.6 * e, p)[0, 1] / p.var(ddof=1)
        # standard error from 40 independent batches of the same draws
        batches = [np.cov(0.6 * eb, pb)[0, 1] / pb.var(ddof=1) for eb, pb in zip(np.split(e, 40), np.split(p, 40), strict=True)]
        se = float(np.std(batches, ddof=1) / math.sqrt(40))
        close(f"simulated share at rho = {rho} (5 standard errors)", sim, euler, 5 * se)
        q(f"equity share of variance at rho = {rho} (%)", 100 * euler, quoted)


def main() -> None:
    bsb_increments()
    fee_drag()
    benchmark_hurdle()
    building_blocks()
    cape_drag()
    sixty_forty_risk()
    print("all asset-allocation checks passed")


if __name__ == "__main__":
    main()
