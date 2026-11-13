"""Mental math: every product, decimal, percentage and approximation error in the note.

Backs every number in `13-Interview-Playbook/02-Mental-Math.md`.
Independent routes used here:
- each shortcut (complements, difference of squares, squaring near a base, squares ending in 5, same tens,
  cross multiplication) is implemented as the digit procedure the note describes and checked against
  Python's integer product over every input in its range, then on the quoted examples;
- the fraction table by long division, finding the repeating block from the remainder cycle;
- percentages and fractions with exact `fractions.Fraction` arithmetic;
- approximation errors (rule of 72, square-root linearisation, the pi estimate) against `math.log`, `math.sqrt`
  and `math.pi`, with the rule of 72's exact point found by bisection.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 13-Interview-Playbook/code/interview_02_mental_math.py`.
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

SEED = 20261112


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


# ------------------------------------------------------------------ digit procedures


def complement(n: int, power: int) -> int:
    """10^power - n by 'every digit from 9, the last non-zero digit from 10'."""
    digits = [int(c) for c in str(n).zfill(power)]
    last = max(i for i, d in enumerate(digits) if d)
    out = [9 - d for d in digits[:last]] + [10 - digits[last]] + [0] * (power - last - 1)
    return int("".join(map(str, out)))


def cross_multiply(x: int, y: int) -> int:
    """Two-digit vertical-and-crosswise product: units, tens, hundreds with carries."""
    a, b = divmod(x, 10)
    c, d = divmod(y, 10)
    units = b * d
    tens = a * d + b * c + units // 10
    hundreds = a * c + tens // 10
    return int(f"{hundreds}{tens % 10}{units % 10}")


def repeating_decimal(frac: Fraction) -> tuple[str, str]:
    """(non-repeating digits, repeating block) of a fraction in (0, 1) by long division."""
    num, den = frac.numerator, frac.denominator
    seen: dict[int, int] = {}
    digits = []
    rem = num % den
    while rem and rem not in seen:
        seen[rem] = len(digits)
        rem *= 10
        digits.append(str(rem // den))
        rem %= den
    if not rem:
        return "".join(digits), ""
    start = seen[rem]
    return "".join(digits[:start]), "".join(digits[start:])


def rule72_gap(r: float) -> float:
    return 72 / r - math.log(2) / math.log1p(r / 100)


def main() -> None:
    rng = random.Random(SEED)

    print("Addition and subtraction")
    exact("67 + 58 left to right: 117 + 8", 67 + 50 + 8, 125)
    exact("67 + 60 - 2", 67 + 60 - 2, 125)
    for n in range(1, 1000):
        assert complement(n, 3) == 1000 - n, n
    exact("1000 - 387 by digit complements", complement(387, 3), 613)
    exact("count up: 13 to 400 then 600", 13 + 600, 613)
    exact("101.25 - 98.70 (cents)", 10125 - 9870, 255)
    exact("1.30 to reach 100 plus 1.25 (cents)", 130 + 125, 255)

    print("Multiplication shortcuts, each checked on every input in its range first")
    for a, b in itertools.product(range(10, 100), repeat=2):
        assert cross_multiply(a, b) == a * b
    for m, d in itertools.product(range(1, 200), range(0, 50)):
        assert (m + d) * (m - d) == m * m - d * d
    for a in range(1, 30):
        assert (10 * a + 5) ** 2 == int(f"{a * (a + 1)}25")
    for a, b in itertools.product(range(1, 10), range(1, 10)):
        assert (10 * a + b) * (10 * a + 10 - b) == int(f"{a * (a + 1)}{b * (10 - b):02d}")
    exact("7 x 86 = 560 + 42", 7 * 80 + 7 * 6, 7 * 86)
    exact("7 x 86", 7 * 86, 602)
    exact("47 x 53", 47 * 53, 2491)
    exact("50^2 - 3^2", 50**2 - 3**2, 2491)
    exact("998 x 1002", 998 * 1002, 999996)
    exact("57^2", 57**2, 3249)
    exact("64 x 50 + 49", 64 * 50 + 7**2, 3249)
    exact("96^2", 96**2, 9216)
    exact("92 x 100 + 16", 92 * 100 + 16, 9216)
    exact("104^2", 104**2, 10816)
    exact("108 x 100 + 16", 108 * 100 + 16, 10816)
    exact("65^2", 65**2, 4225)
    exact("43 x 47", 43 * 47, 2021)
    exact("37 x 33", 37 * 33, 1221)
    exact("34 x 26 by cross multiplication", cross_multiply(34, 26), 884)
    exact("34 x 26 digits: units, tens (with carry), hundreds (with carry)", (4 * 6, 3 * 6 + 4 * 2 + 2, 3 * 2 + 2), (24, 28, 8))
    exact("30^2 - 4^2", 30**2 - 4**2, 884)
    exact("125 x 48", 125 * 48, 6000)
    exact("1000 x 48/8", 1000 * 48 // 8, 6000)
    for k in range(1, 200):
        assert 25 * k == Fraction(100 * k, 4) and 5 * k == Fraction(10 * k, 2)

    print("Fraction table by long division")
    table = {
        (1, 2): ("5", ""),
        (1, 3): ("", "3"),
        (1, 4): ("25", ""),
        (1, 5): ("2", ""),
        (1, 6): ("1", "6"),
        (1, 7): ("", "142857"),
        (1, 8): ("125", ""),
        (1, 9): ("", "1"),
        (1, 11): ("", "09"),
        (1, 12): ("08", "3"),
        (1, 13): ("", "076923"),
        (1, 16): ("0625", ""),
        (1, 20): ("05", ""),
        (1, 40): ("025", ""),
    }
    for (a, b), quoted in table.items():
        exact(f"{a}/{b} as (fixed digits, repeating block)", repeating_decimal(Fraction(a, b)), quoted)
    for (a, b), dec in {(3, 8): "0.375", (5, 8): "0.625", (7, 8): "0.875", (3, 16): "0.1875", (7, 16): "0.4375"}.items():
        exact(f"{a}/{b}", Fraction(a, b), Fraction(dec))
    exact("2/7 block", repeating_decimal(Fraction(2, 7))[1], "285714")
    exact("3/7 block", repeating_decimal(Fraction(3, 7))[1], "428571")
    for k in range(1, 7):
        block = repeating_decimal(Fraction(k, 7))[1]
        assert block in "142857" * 2, (k, block)
    for n in range(1, 9):
        assert repeating_decimal(Fraction(n, 9)) == ("", str(n))
    exact("17/99", repeating_decimal(Fraction(17, 99)), ("", "17"))
    exact("17/40", Fraction(17, 40), Fraction("0.425"))
    exact("17/40 scaled by 2.5", Fraction(17) * Fraction(5, 2), Fraction("42.5"))
    exact("3.6 / 0.12", Fraction("3.6") / Fraction("0.12"), 30)

    print("Percentages")
    exact("16% of 25", Fraction(16, 100) * 25, 4)
    exact("25% of 16", Fraction(25, 100) * 16, 4)
    for pct, frac in {"12.5": (1, 8), "37.5": (3, 8), "62.5": (5, 8), "87.5": (7, 8)}.items():
        exact(f"{pct}%", Fraction(pct) / 100, Fraction(*frac))
    approx("1/6 as a percent", 100 / 6, 16.7, 1)
    approx("1/3 as a percent", 100 / 3, 33.3, 1)
    exact("15% of 360 = 36 + 18", (36 + 18, Fraction(15, 100) * 360), (54, 54))
    exact("+20% then -20%", Fraction(12, 10) * Fraction(8, 10), Fraction(96, 100))
    for p, gain in ((Fraction(1, 5), Fraction(1, 4)), (Fraction(1, 2), Fraction(1))):
        exact(f"gain to recover a {p} fall", 1 / (1 - p) - 1, gain)
        exact(f"p/(1-p) for p = {p}", p / (1 - p), gain)
    approx("1.07^10", 1.07**10, 1.967, 3)

    print("Rule of 72 accuracy (card int-math-rule-of-72, int-math-rule-of-72-accuracy)")
    approx("exact doubling time at 6%", math.log(2) / math.log(1.06), 11.9, 1)
    for r, quoted in ((2, 35.00), (6, 11.90), (8, 9.01), (12, 6.12)):
        approx(f"exact doubling time at {r}% (rule gives {72 / r:g})", math.log(2) / math.log1p(r / 100), quoted, 2)
    lo, hi = 2.0, 20.0  # rule72_gap is positive at 2% and negative at 20%
    assert rule72_gap(lo) > 0 > rule72_gap(hi)
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if rule72_gap(mid) > 0 else (lo, mid)
    approx("rate at which 72/r is exact, %", lo, 7.85, 2)
    approx("100 ln 2", 100 * math.log(2), 69.3, 1)
    approx("rule of 72 error at 6%, years", 72 / 6 - math.log(2) / math.log(1.06), 0.10, 2)

    print("Estimation and error control")
    approx("1.02 x 0.98", 1.02 * 0.98, 0.9996, 4)
    approx("1.02 / 1.02 rounding a quotient both ways up", 1.02 / 1.02, 1.0, 4)
    approx("1.02 / 0.98 rounding a quotient in opposite directions", 1.02 / 0.98, 1.0408, 4)
    approx("3 x 27.3", 3 * 27.3, 81.9, 1)
    approx("0.14 x 27.3", 0.14 * 27.3, 3.82, 2)
    approx("81.9 + 3.82", 81.9 + 3.82, 85.7, 1)
    approx("pi x 27.3", math.pi * 27.3, 85.77, 2)
    approx("pi / 3", math.pi / 3, 1.047, 3)
    approx("percent the true product exceeds 81.9", 100 * (math.pi * 27.3 / 81.9 - 1), 4.7, 1)
    approx("4.7% of 82", 0.047 * 82, 3.85, 2)
    approx("81.9 + 3.85", 81.9 + 3.85, 85.75, 2)
    err = abs(85.75 - math.pi * 27.3) / (math.pi * 27.3)
    approx("relative error of 85.75, %", 100 * err, 0.02, 2)
    approx("sqrt(50) by linearisation 7 + 1/14", 7 + 1 / 14, 7.071, 3)
    approx("sqrt(50)", math.sqrt(50), 7.0711, 4)
    approx("linearisation overshoot", 7 + 1 / 14 - math.sqrt(50), 0.0004, 4)
    approx("predicted overshoot e^2/(8 a^3)", 1 / (8 * 7**3), 0.0004, 4)
    exact("8 x 7^3", 8 * 7**3, 2744)
    for _ in range(2000):
        x, y = rng.randint(10, 10**6), rng.randint(10, 10**6)
        assert (x * y) % 9 == ((x % 9) * (y % 9)) % 9
        digit_sum = sum(map(int, str(x * y)))
        assert digit_sum % 9 == (x * y) % 9
    print("    casting out nines holds on 2000 random products")
    for n in range(10, 10**5):
        digits = str(n)
        for i in range(len(digits) - 1):
            swapped = int(digits[:i] + digits[i + 1] + digits[i] + digits[i + 2 :])
            assert (n - swapped) % 9 == 0
    print("    every adjacent transposition of every number below 100,000 changes it by a multiple of 9")

    print("Worked examples")
    exact("68 x 72", 68 * 72, 4896)
    exact("70^2 - 2^2", 70**2 - 2**2, 4896)
    exact("57 x 63", 57 * 63, 3591)
    exact("60^2 - 3^2", 60**2 - 3**2, 3591)
    exact("12.5% of 640", Fraction(125, 1000) * 640, 80)
    exact("48 x 80", 48 * 80, 3840)
    exact("50 x 80", 50 * 80, 4000)
    exact("7 x 0.0625", 7 * Fraction("0.0625"), Fraction("0.4375"))
    exact("17/40 + 7/16", Fraction(17, 40) + Fraction(7, 16), Fraction("0.8625"))
    exact("68/160 + 70/160", Fraction(68 + 70, 160), Fraction(138, 160))
    exact("96^2 - 4^2", 96**2 - 4**2, 9200)
    exact("92 x 100", 92 * 100, 9200)

    print("Drill formats (tools/qp/drills.py)")
    exact("80 questions in 480 seconds, seconds each", Fraction(480, 80), 6)
    print("All mental-math checks passed.")


if __name__ == "__main__":
    main()
