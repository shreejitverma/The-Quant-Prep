"""Timed drills and trading games. Pure logic with seeded randomness; no I/O.

- ``arith``: Zetamac-style arithmetic (defaults match the public Zetamac settings:
  a+b with a, b in [2, 100], the matching subtractions, a*b with a in [2, 12] and
  b in [2, 100], and the matching divisions).
- ``optiver``: mixed integer, decimal, percentage and fraction arithmetic in the style
  of numerical screening tests (80 questions, 8 minutes by default).
- ``MarketMakingGame``: make two-sided markets on the sum of hidden dice against a mix
  of informed and noise counterparties; it teaches fair-value updating, width against
  adverse selection, and inventory skew.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from fractions import Fraction

DRILL_MODES = {
    "arith": {"seconds": 120, "questions": None, "title": "Arithmetic sprint (Zetamac rules)"},
    "optiver": {"seconds": 480, "questions": 80, "title": "80 in 8: mixed numerical test"},
}


@dataclass(frozen=True)
class Problem:
    text: str
    answer: Fraction
    tolerance: Fraction = Fraction(0)  # absolute tolerance, used for non-terminating answers

    def check(self, raw: str) -> bool:
        value = parse_number(raw)
        if value is None:
            return False
        return abs(value - self.answer) <= self.tolerance

    @property
    def answer_text(self) -> str:
        return fmt(self.answer)


def parse_number(raw: str) -> Fraction | None:
    s = raw.strip().replace(",", "").replace(" ", "")
    if not s or s.count("/") > 1 or "e" in s.lower() or "_" in s:  # plain decimals and a/b only
        return None
    try:
        if "/" in s:
            num, den = s.split("/", 1)
            return Fraction(Fraction(num), Fraction(den))
        return Fraction(s)
    except (ValueError, ZeroDivisionError):
        return None


def terminates(x: Fraction) -> bool:
    d = x.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    if terminates(x):
        sign = "-" if x < 0 else ""
        x = abs(x)
        whole, rem = divmod(x.numerator, x.denominator)
        digits = []
        while rem:
            rem *= 10
            q, rem = divmod(rem, x.denominator)
            digits.append(str(q))
        return f"{sign}{whole}.{''.join(digits)}"
    return f"{x.numerator}/{x.denominator}"


# --- arithmetic sprint -----------------------------------------------------


def arith_problem(rng: random.Random) -> Problem:
    kind = rng.choice("+-*/")
    if kind in "+-":
        a, b = rng.randint(2, 100), rng.randint(2, 100)
        if kind == "+":
            return Problem(f"{a} + {b}", Fraction(a + b))
        return Problem(f"{a + b} - {a}", Fraction(b))
    a, b = rng.randint(2, 12), rng.randint(2, 100)
    if kind == "*":
        return Problem(f"{a} x {b}", Fraction(a * b))
    return Problem(f"{a * b} / {a}", Fraction(b))


# --- mixed numerical test --------------------------------------------------


def _dec(rng: random.Random, choices: list[str]) -> Fraction:
    return Fraction(rng.choice(choices))


def optiver_problem(rng: random.Random) -> Problem:
    kind = rng.randrange(7)
    if kind == 0:  # two-digit multiplication
        a, b = rng.randint(12, 99), rng.randint(12, 99)
        return Problem(f"{a} x {b}", Fraction(a * b))
    if kind == 1:  # decimal times integer
        a = _dec(rng, ["0.2", "0.25", "0.3", "0.4", "0.6", "0.75", "0.8", "1.5", "2.5", "0.125"])
        b = rng.randint(12, 96)
        return Problem(f"{fmt(a)} x {b}", a * b)
    if kind == 2:  # division with a terminating result
        q = Fraction(rng.randint(3, 60), rng.choice([1, 1, 2, 4]))
        d = _dec(rng, ["0.2", "0.25", "0.4", "0.5", "0.8", "4", "8", "12", "1.5"])
        return Problem(f"{fmt(q * d)} / {fmt(d)}", q)
    if kind == 3:  # percentage of
        p = _dec(rng, ["5", "10", "12.5", "15", "20", "25", "30", "40", "60", "75", "80", "120", "150"])
        n = rng.choice([40, 80, 120, 160, 200, 240, 320, 360, 400, 480, 640, 800])
        return Problem(f"{fmt(p)}% of {n}", p * n / 100)
    if kind == 4:  # fraction to decimal
        b = rng.choice([4, 5, 8, 16, 20, 25, 40])
        a = rng.randint(1, b - 1)
        return Problem(f"{a}/{b} as a decimal", Fraction(a, b))
    if kind == 5:  # decimal addition and subtraction
        a = Fraction(rng.randint(100, 9999), 100)
        b = Fraction(rng.randint(100, 9999), 100)
        if rng.random() < 0.5:
            return Problem(f"{fmt(a)} + {fmt(b)}", a + b)
        hi, lo = max(a, b), min(a, b)
        return Problem(f"{fmt(hi)} - {fmt(lo)}", hi - lo)
    # fraction arithmetic; non-terminating answers accept 3 decimal places
    x = Fraction(rng.randint(1, 5), rng.choice([2, 3, 4, 6, 8]))
    y = Fraction(rng.randint(1, 5), rng.choice([2, 3, 4, 6, 8]))
    op = rng.choice("+x")
    ans = x + y if op == "+" else x * y
    tol = Fraction(0) if terminates(ans) else Fraction(1, 2000)
    return Problem(f"{x} {op} {y}", ans, tol)


GENERATORS = {"arith": arith_problem, "optiver": optiver_problem}


def problems(mode: str, seed: int | None = None):
    """Infinite generator of problems for a drill mode."""
    if mode not in GENERATORS:
        raise ValueError(f"unknown drill mode {mode!r}; choose from {', '.join(GENERATORS)}")
    rng = random.Random(seed)
    while True:
        yield GENERATORS[mode](rng)


# --- market-making game ----------------------------------------------------


@dataclass
class Trade:
    round: int
    side: str  # "buy" or "sell" from the player's point of view
    price: int
    qty: int
    counterparty: str  # "informed" or "noise"


@dataclass
class MarketMakingGame:
    """Quote the final sum of ``n_dice`` hidden dice. One die is revealed after each round.

    Each round the player quotes ``bid``/``ask`` with ``ask - bid`` between 1 and
    ``max_width``. A counterparty then arrives: with probability ``p_informed`` it knows
    the true sum and lifts your ask if the sum is above it or hits your bid if below;
    otherwise it is a noise trader that buys, sells or passes with equal probability.
    Every trade is ``lot`` contracts. At the end the position settles at the true sum.
    """

    seed: int | None = None
    n_dice: int = 4
    sides: int = 6
    max_width: int = 4
    p_informed: float = 0.5
    lot: int = 10
    dice: list[int] = field(default_factory=list)
    revealed: int = 0
    position: int = 0
    cash: int = 0
    trades: list[Trade] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        if not self.dice:
            self.dice = [self._rng.randint(1, self.sides) for _ in range(self.n_dice)]

    @property
    def finished(self) -> bool:
        return self.revealed >= self.n_dice

    @property
    def known(self) -> list[int]:
        return self.dice[: self.revealed]

    @property
    def fair_value(self) -> Fraction:
        """Expected final sum given the revealed dice."""
        unknown = self.n_dice - self.revealed
        return Fraction(sum(self.known)) + unknown * Fraction(self.sides + 1, 2)

    @property
    def total(self) -> int:
        return sum(self.dice)

    def quote(self, bid: int, ask: int) -> dict:
        if self.finished:
            raise ValueError("game is over")
        if not isinstance(bid, int) or not isinstance(ask, int):
            raise ValueError("bid and ask must be integers")
        if not 1 <= ask - bid <= self.max_width:
            raise ValueError(f"width must be between 1 and {self.max_width}")
        fv = self.fair_value
        informed = self._rng.random() < self.p_informed
        if informed:
            side = "sell" if self.total > ask else "buy" if self.total < bid else None
        else:
            side = self._rng.choice(["sell", "buy", None])
        trade = None
        if side == "sell":  # counterparty lifts our ask: we sell
            self.position -= self.lot
            self.cash += ask * self.lot
            trade = Trade(self.revealed + 1, "sell", ask, self.lot, "informed" if informed else "noise")
        elif side == "buy":  # counterparty hits our bid: we buy
            self.position += self.lot
            self.cash -= bid * self.lot
            trade = Trade(self.revealed + 1, "buy", bid, self.lot, "informed" if informed else "noise")
        if trade:
            self.trades.append(trade)
        event = {
            "round": self.revealed + 1,
            "bid": bid,
            "ask": ask,
            "fair_value": float(fv),
            "mid_error": float(Fraction(bid + ask, 2) - fv),
            "trade": trade.__dict__ if trade else None,
            "position": self.position,
        }
        self.revealed += 1
        event["revealed_die"] = self.dice[self.revealed - 1]
        self.history.append(event)
        return event

    def pnl(self) -> int:
        """Mark-to-final P&L; only meaningful once the game is finished."""
        return self.cash + self.position * self.total

    def summary(self) -> dict:
        """Split P&L into edge at trade time (versus fair value then) and the rest."""
        edge = 0.0
        for h in self.history:
            t = h["trade"]
            if t:
                sign = 1 if t["side"] == "sell" else -1
                edge += sign * (t["price"] - h["fair_value"]) * t["qty"]
        pnl = self.pnl()
        informed = [t for t in self.trades if t.counterparty == "informed"]
        return {
            "total": self.total,
            "dice": self.dice,
            "pnl": pnl,
            "edge_at_fill": round(edge, 2),
            "adverse_and_inventory": round(pnl - edge, 2),
            "trades": len(self.trades),
            "informed_trades": len(informed),
            "final_position": self.position,
        }

    def state(self) -> dict:
        return {
            "n_dice": self.n_dice,
            "sides": self.sides,
            "max_width": self.max_width,
            "lot": self.lot,
            "revealed": self.known,
            "round": min(self.revealed + 1, self.n_dice),
            "finished": self.finished,
            "position": self.position,
            "cash": self.cash,
            "history": self.history,
            "summary": self.summary() if self.finished else None,
        }
