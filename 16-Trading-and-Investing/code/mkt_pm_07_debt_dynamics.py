"""Macro regimes and debt cycles: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Portfolio-Management/07-Macro-Regimes-and-Debt-Cycles.md`.
Independent routes used here:
- the one-year change in the debt ratio from the exact law of motion d' = d (1 + i) / (1 + g) - pb in exact fractions,
  against the linear approximation (i - g) d - pb;
- the debt-stabilising primary balance from its closed form, checked by iterating the law of motion;
- the steady-state debt ratio when g > i from its closed form, against iterating the law of motion for 3,000 years.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_pm_07_debt_dynamics.py
"""

from __future__ import annotations

from fractions import Fraction


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


def step(d: Fraction, i: Fraction, g: Fraction, pb: Fraction) -> Fraction:
    """Exact law of motion for debt / GDP with primary surplus pb as a share of this year's GDP."""
    return d * (1 + i) / (1 + g) - pb


def debt_dynamics() -> None:
    print("Debt ratio d = 100% of GDP, i = 5%, g = 3%, primary balance 0 (hypothetical)")
    d, i, g = Fraction(1), Fraction(5, 100), Fraction(3, 100)
    exact = step(d, i, g, Fraction(0)) - d
    approx = (i - g) * d
    q("exact one-year change in debt ratio (pp of GDP)", 100 * exact, "1.94")
    q("linear approximation (i - g) d (pp of GDP)", 100 * approx, "2.00")
    stabilising = d * (i - g) / (1 + g)
    close("stabilising surplus keeps d fixed", float(step(d, i, g, stabilising)), 1.0, 1e-15)
    q("debt-stabilising primary surplus (% of GDP)", 100 * stabilising, "1.94")

    print("Debt ratio 60% of GDP, i = 3%, g = 5%, primary deficit 2% of GDP (hypothetical)")
    i, g, pb = Fraction(3, 100), Fraction(5, 100), Fraction(-2, 100)
    steady = -pb * (1 + g) / (g - i)
    path = 0.60
    for _ in range(3000):
        path = path * 1.03 / 1.05 + 0.02
    close("iterated path vs closed-form steady state", path, float(steady), 1e-9)
    q("steady-state debt ratio when g > i (% of GDP)", 100 * steady, "105")
    first = step(Fraction(60, 100), i, g, pb) - Fraction(60, 100)
    q("first-year change from 60% (pp of GDP)", 100 * first, "0.86")


def main() -> None:
    debt_dynamics()
    print("all debt-dynamics checks passed")


if __name__ == "__main__":
    main()
