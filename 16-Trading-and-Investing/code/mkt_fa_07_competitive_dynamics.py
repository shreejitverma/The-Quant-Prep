"""Competitive dynamics case study: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Fundamental-Analysis/07-Industry-Competitive-Dynamics-and-Porter-Helmer.md`.
Independent routes used here:
- expected customer lifetime as the closed form 1 / churn, as an explicit sum of yearly survival
  probabilities (a customer who pays in year k survived k - 1 renewals), and by a seeded simulation of
  geometric customer lifetimes with a tolerance of five standard errors;
- lifetime value (undiscounted gross profit per account over the expected lifetime) as the closed form
  ARPA x gross margin / churn and as the truncated survival-weighted series;
- LTV / CAC from the unrounded lifetime value, which shows why rounding the lifetime first moves the
  quoted ratio.
The McGahan-Porter (1997) variance shares are cited constants from the paper's abstract.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_fa_07_competitive_dynamics.py`.
"""

from __future__ import annotations

import numpy as np

SEED = 7


def rounded(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def survival_series(churn: float, years: int = 5000) -> float:
    k = np.arange(1, years + 1)
    return float(np.sum((1 - churn) ** (k - 1)))


def simulated_lifetime(churn: float, rng: np.random.Generator, n: int = 400_000) -> tuple[float, float]:
    life = rng.geometric(churn, size=n)  # years paid, counting the first year
    return float(life.mean()), float(life.std(ddof=1) / np.sqrt(n))


def company(name: str, arpa: float, gm: float, churn: float, cac: float, quoted: dict[str, str], rng) -> None:
    print(f"{name}: ARPA ${arpa:,.0f}, gross margin {gm:.0%}, churn {churn:.1%}, CAC ${cac:,.0f}")
    closed = 1 / churn
    series = survival_series(churn)
    sim, se = simulated_lifetime(churn, rng)
    assert abs(series - closed) < 1e-9
    assert abs(sim - closed) < 5 * se, f"simulated lifetime {sim} vs {closed} (se {se})"
    rounded("expected lifetime, closed form (years)", closed, quoted["life"])
    rounded("expected lifetime, survival series (years)", series, quoted["life"])
    print(f"    simulated lifetime (seed {SEED}) = {sim:.3f} +/- {se:.3f}")
    margin = arpa * gm
    ltv_closed = margin / churn
    ltv_series = margin * series
    rounded("annual gross profit per account", margin, quoted["margin"])
    rounded("LTV, closed form", ltv_closed, quoted["ltv"])
    rounded("LTV, survival series", ltv_series, quoted["ltv"])
    rounded("LTV / CAC", ltv_closed / cac, quoted["ratio"])
    rounded("LTV / CAC with the lifetime rounded to one decimal first", margin * round(closed, 1) / cac, quoted["old"])


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    company(
        "Competitor A: CloudOS",
        40_000,
        0.82,
        0.035,
        12_000,
        {"life": "28.6", "margin": "32,800", "ltv": "937,143", "ratio": "78.1", "old": "78.2"},
        rng,
    )
    company(
        "Competitor B: ToolBox",
        15_000,
        0.68,
        0.18,
        10_000,
        {"life": "5.6", "margin": "10,200", "ltv": "56,667", "ratio": "5.7", "old": "5.7"},
        rng,
    )
    shares = {"year": 2, "industry": 19, "corporate parent": 4, "business-specific": 32}
    print(f"Cited constants, McGahan and Porter (1997), percent of profitability variance: {shares}")
    print("all competitive-dynamics numbers check out")
