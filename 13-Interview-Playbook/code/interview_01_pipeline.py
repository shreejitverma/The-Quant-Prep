"""How quant interviews work: the few numbers in the worked examples and cards.

Backs every number in `13-Interview-Playbook/01-How-Quant-Interviews-Work.md`.
Independent routes used here:
- waiting times for one 6 and for two 6s in a row by solving the absorbing Markov chain exactly
  (Gaussian elimination over `fractions.Fraction`), not by the 1/p or first-step formulas, plus seeded simulation;
- the coin-flip market by enumerating all 2^10 sequences;
- the pacing budget from the drill's own configuration in `tools/qp/drills.py`.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 13-Interview-Playbook/code/interview_01_pipeline.py`.
"""

from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.qp.drills import DRILL_MODES  # noqa: E402

SEED = 20261112


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


def expected_steps(transient: list[list[Fraction]]) -> list[Fraction]:
    """Solve (I - Q) t = 1 for the expected steps to absorption from each transient state."""
    n = len(transient)
    a = [[(Fraction(1) if i == j else Fraction(0)) - transient[i][j] for j in range(n)] + [Fraction(1)] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if a[r][col] != 0)
        a[col], a[piv] = a[piv], a[col]
        a[col] = [x / a[col][col] for x in a[col]]
        for r in range(n):
            if r != col and a[r][col] != 0:
                f = a[r][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[col], strict=True)]
    return [a[i][n] for i in range(n)]


def main() -> None:
    rng = np.random.default_rng(SEED)

    print("Example 1 (cards int-pipeline-geometric-first-six, int-pipeline-two-sixes-in-a-row)")
    p = Fraction(1, 6)
    exact("E[rolls to first 6], Markov chain", expected_steps([[1 - p]])[0], 6)
    # states: 0 = no current 6, 1 = last roll was a 6; absorbing after a second consecutive 6
    exact("E[rolls to two 6s in a row], Markov chain", expected_steps([[1 - p, p], [1 - p, Fraction(0)]])[0], 42)
    exact("1/p + 1/p^2", 1 / p + 1 / p**2, 42)
    n = 50_000
    rolls = rng.integers(1, 7, size=(n, 1000), dtype=np.int8)
    six = rolls == 6
    first = np.argmax(six, axis=1) + 1
    simulated("E[first 6], simulated", float(first.mean()), 6.0, 4 * float(first.std()) / math.sqrt(n))
    pair = six[:, 1:] & six[:, :-1]
    assert pair.any(axis=1).all()  # P(no two 6s in a row within 1000 rolls) is below 1e-10
    waits = np.argmax(pair, axis=1) + 2
    simulated("E[two 6s in a row], simulated", float(waits.mean()), 42.0, 4 * float(waits.std()) / math.sqrt(n))

    print("Example 2 (card int-pipeline-test-pacing)")
    exact("drill optiver: questions and seconds", (DRILL_MODES["optiver"]["questions"], DRILL_MODES["optiver"]["seconds"]), (80, 480))
    exact("seconds per question", Fraction(480, 80), 6)
    exact("second-pass limit, twice the budget", 2 * 6, 12)

    print("Example 3 (card int-pipeline-ten-flips-market)")
    heads = [sum(o) for o in itertools.product((0, 1), repeat=10)]
    mean = Fraction(sum(heads), 1024)
    var = sum((h - mean) ** 2 for h in heads) / 1024
    exact("mean heads", mean, 5)
    exact("variance", var, Fraction(5, 2))
    approx("sd", math.sqrt(var), 1.58, 2)
    print("All pipeline checks passed.")


if __name__ == "__main__":
    main()
