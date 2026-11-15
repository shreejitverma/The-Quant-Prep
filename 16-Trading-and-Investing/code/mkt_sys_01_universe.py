"""Strategy architecture and universe selection: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/60-Systems/01-Strategy-Architecture-and-Universe-Selection.md`.
Independent routes used here:
- the delisting drag as weight times delisting return in exact fractions, and again by marking a
  $1,000,000 book's two positions to their recovery values;
- the hysteresis band by running the inclusion rule on every rank from 1 to 1000 for both prior states;
- tick friction as one cent over the share price, in exact fractions.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_sys_01_universe.py`.
"""

from __future__ import annotations

from fractions import Fraction


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def delisting() -> None:
    print("Example 1: delisting-return drag (cards mkt-sys-003, mkt-sys-026)")
    weight = Fraction(2, 100)
    r_a = Fraction(1, 20) - 1  # $20.00 -> $1.00
    exact("delisting return A", r_a, Fraction(-95, 100))
    r_b = Fraction(-1)
    exact("loss A (percent of capital)", 100 * weight * r_a, Fraction(-190, 100))
    exact("loss B (percent of capital)", 100 * weight * r_b, Fraction(-2))
    drag = 100 * weight * (r_a + r_b)
    exact("total drag (percent)", drag, Fraction(-390, 100))
    exact("total drag (bps)", 100 * drag, Fraction(-390))
    # Independent route: mark the positions of a $1,000,000 book.
    book = 1_000_000
    pos = book * weight
    shares_a, shares_b = pos / 20, pos / 15
    value_after = shares_a * 1 + shares_b * 0
    exact("shares of A", shares_a, 1000)
    exact("book loss in dollars", 2 * pos - value_after, 39_000)
    exact("book loss (percent)", Fraction(2 * pos - value_after, book) * 100, Fraction(39, 10))
    exact("long book: 50 names at 2%", 50 * weight, 1)


def in_universe(prior: bool, rank: int, enter: int = 450, exit_above: int = 550) -> bool:
    if rank <= enter:
        return True
    if rank > exit_above:
        return False
    return prior


def hysteresis() -> None:
    print("Example 2: hysteresis band (cards mkt-sys-008, mkt-sys-016)")
    exact("Stock X (excluded, rank 475)", in_universe(False, 475), False)
    exact("Stock Y (included, rank 520)", in_universe(True, 520), True)
    exact("Stock Z (included, rank 565)", in_universe(True, 565), False)
    keep = [r for r in range(1, 1001) if in_universe(True, r) and not in_universe(False, r)]
    exact("ranks where the state is sticky", (keep[0], keep[-1], len(keep)), (451, 550, 100))


def ticks() -> None:
    print("Pitfalls: tick friction (card mkt-sys-006)")
    exact("one cent on a $1.00 stock (bps)", Fraction(1, 100) / 1 * 10_000, 100)
    exact("one cent on a $5.00 stock (bps)", Fraction(1, 100) / 5 * 10_000, 20)
    exact("one cent on a $50.00 stock (bps)", Fraction(1, 100) / 50 * 10_000, 2)


if __name__ == "__main__":
    delisting()
    hysteresis()
    ticks()
    print("all universe-selection numbers check out")
