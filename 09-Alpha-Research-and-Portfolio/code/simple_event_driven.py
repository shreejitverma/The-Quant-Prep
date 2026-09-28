"""A minimal event-driven backtester that avoids the classic look-ahead trap.

Flow per bar: MARKET -> strategy -> SIGNAL -> portfolio -> ORDER -> execution.
Orders are filled at the *next* bar's price (never the bar that generated the signal),
with commission and slippage, and the portfolio updates positions and cash on FILL.
Equity is marked to market after every bar.

Run: python3 simple_event_driven.py
"""

from __future__ import annotations

import datetime as dt
from collections import deque
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MarketEvent:
    timestamp: dt.datetime
    symbol: str
    price: float


@dataclass(frozen=True)
class SignalEvent:
    timestamp: dt.datetime
    symbol: str
    target: int  # desired position in shares


@dataclass(frozen=True)
class OrderEvent:
    timestamp: dt.datetime
    symbol: str
    quantity: int  # signed: + buy, - sell


@dataclass(frozen=True)
class FillEvent:
    timestamp: dt.datetime
    symbol: str
    quantity: int
    price: float
    commission: float


class MeanReversionStrategy:
    """Target -size when price is above its moving average, +size when below, flat otherwise."""

    def __init__(self, window: int = 3, size: int = 100, band: float = 0.5):
        self.window, self.size, self.band = window, size, band
        self.prices: deque[float] = deque(maxlen=window)

    def on_market(self, e: MarketEvent) -> SignalEvent | None:
        self.prices.append(e.price)
        if len(self.prices) < self.window:
            return None
        mean = sum(self.prices) / len(self.prices)
        target = -self.size if e.price > mean + self.band else self.size if e.price < mean - self.band else 0
        return SignalEvent(e.timestamp, e.symbol, target)


@dataclass
class Portfolio:
    cash: float = 100_000.0
    positions: dict[str, int] = field(default_factory=dict)
    last_price: dict[str, float] = field(default_factory=dict)
    equity_curve: list[tuple[dt.datetime, float]] = field(default_factory=list)

    def on_signal(self, s: SignalEvent) -> OrderEvent | None:
        delta = s.target - self.positions.get(s.symbol, 0)
        return OrderEvent(s.timestamp, s.symbol, delta) if delta else None

    def on_fill(self, f: FillEvent) -> None:
        self.positions[f.symbol] = self.positions.get(f.symbol, 0) + f.quantity
        self.cash -= f.quantity * f.price + f.commission

    def mark(self, e: MarketEvent) -> None:
        self.last_price[e.symbol] = e.price
        value = sum(q * self.last_price[s] for s, q in self.positions.items())
        self.equity_curve.append((e.timestamp, self.cash + value))


@dataclass
class NextBarExecution:
    """Fills pending orders at the next bar's price plus slippage; no fills on the signal bar."""

    commission_per_share: float = 0.005
    slippage_bps: float = 1.0
    pending: list[OrderEvent] = field(default_factory=list)

    def submit(self, o: OrderEvent) -> None:
        self.pending.append(o)

    def on_market(self, e: MarketEvent) -> list[FillEvent]:
        fills, keep = [], []
        for o in self.pending:
            if o.symbol != e.symbol:
                keep.append(o)
                continue
            sign = 1 if o.quantity > 0 else -1
            price = e.price * (1 + sign * self.slippage_bps / 1e4)
            fills.append(FillEvent(e.timestamp, o.symbol, o.quantity, price, abs(o.quantity) * self.commission_per_share))
        self.pending = keep
        return fills


def run_backtest(bars: list[MarketEvent], strategy, portfolio: Portfolio, execution: NextBarExecution) -> Portfolio:
    for bar in bars:
        for fill in execution.on_market(bar):  # 1. orders from earlier bars fill at this bar
            portfolio.on_fill(fill)
        portfolio.mark(bar)  # 2. mark to market
        signal = strategy.on_market(bar)  # 3. then react to this bar; the order fills next bar
        order = portfolio.on_signal(signal) if signal else None
        if order:
            execution.submit(order)
    return portfolio


def sample_bars() -> list[MarketEvent]:
    start = dt.datetime(2023, 1, 3, 10, 0)
    prices = [150.0, 151.0, 149.0, 152.5, 150.0, 148.0, 149.5, 151.0]
    return [MarketEvent(start + dt.timedelta(minutes=i), "AAPL", p) for i, p in enumerate(prices)]


if __name__ == "__main__":
    pf = run_backtest(sample_bars(), MeanReversionStrategy(), Portfolio(), NextBarExecution())
    for ts, eq in pf.equity_curve:
        print(f"{ts:%H:%M}  equity {eq:,.2f}")
    print(f"final position {pf.positions}, cash {pf.cash:,.2f}")
