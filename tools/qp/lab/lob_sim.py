"""Limit Order Book Simulation and Execution Engine (`lob_sim`).

Implements a continuous price-time-priority limit order book matching engine,
zero-intelligence Poisson background flow (Cont-Stoikov-Talreja 2010), order types
(Limit, Market, Cancel, IOC, Post-Only), and execution benchmarks (TWAP, VWAP, Almgren-Chriss).
"""

from __future__ import annotations

import math
import random
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .registry import register

AC_KAPPA = 0.03


def almgren_chriss_schedule(total_qty: int, n_steps: int, kappa: float = AC_KAPPA) -> list[int]:
    """Child order sizes per step for the Almgren-Chriss (2000) optimal liquidation trajectory.

    Holdings x_k = X sinh(kappa (N - k)) / sinh(kappa N) are rounded to whole shares with
    x_0 = X and x_N = 0 exactly, so the children x_k - x_{k+1} are non-negative and sum to X.
    """
    holdings = [round(total_qty * math.sinh(kappa * (n_steps - k)) / math.sinh(kappa * n_steps)) for k in range(n_steps + 1)]
    return [holdings[k] - holdings[k + 1] for k in range(n_steps)]


@dataclass
class Order:
    order_id: int
    side: str  # "buy" or "sell"
    price: float
    size: int
    timestamp: int
    order_type: str = "limit"  # "limit", "market", "ioc", "post_only"
    is_agent: bool = False


class LimitOrderBook:
    def __init__(self, tick_size: float = 0.01):
        self.tick_size = tick_size
        self.bids: dict[float, deque[Order]] = {}
        self.asks: dict[float, deque[Order]] = {}
        self.orders: dict[int, Order] = {}
        self.last_bid: float | None = None
        self.last_ask: float | None = None

    def round_tick(self, price: float) -> float:
        return round(round(price / self.tick_size) * self.tick_size, 4)

    def best_bid(self) -> float | None:
        return max(self.bids.keys()) if self.bids else None

    def best_ask(self) -> float | None:
        return min(self.asks.keys()) if self.asks else None

    def mid_price(self) -> float | None:
        """Mid of the best quotes; an emptied side is quoted at its last price level.

        After a sweep removes a whole side, its reference is the deepest level that was
        consumed (never the opposite side's best), so the mid keeps the impact instead of
        snapping back.
        """
        bb = self.best_bid()
        ba = self.best_ask()
        if ba is None and self.last_ask is not None:
            ba = self.last_ask if bb is None else max(self.last_ask, bb)
        if bb is None and self.last_bid is not None:
            bb = self.last_bid if ba is None else min(self.last_bid, ba)
        if bb is not None and ba is not None:
            return round(0.5 * (bb + ba), 4)
        return bb if bb is not None else ba

    def _remove_level(self, side: str, price: float) -> None:
        if side == "buy":
            del self.bids[price]
            self.last_bid = price
        else:
            del self.asks[price]
            self.last_ask = price

    def spread(self) -> float | None:
        bb = self.best_bid()
        ba = self.best_ask()
        if bb is not None and ba is not None:
            return round(ba - bb, 4)
        return None

    def cancel(self, order_id: int) -> bool:
        order = self.orders.get(order_id)
        if not order:
            return False
        book = self.bids if order.side == "buy" else self.asks
        queue = book.get(order.price)
        if queue:
            try:
                queue.remove(order)
                if not queue:
                    self._remove_level(order.side, order.price)
            except ValueError:
                pass
        del self.orders[order_id]
        return True

    def insert_order(self, order: Order) -> list[tuple[Order, Order, float, int]]:
        """Process order against book using price-time priority. Returns list of (maker, taker, price, size) fills."""
        fills: list[tuple[Order, Order, float, int]] = []
        order.price = self.round_tick(order.price)

        if order.side == "buy":
            # Match against asks
            while order.size > 0 and self.asks:
                best_ask = self.best_ask()
                if best_ask is None or (order.order_type != "market" and order.price < best_ask):
                    break
                queue = self.asks[best_ask]
                while queue and order.size > 0:
                    maker = queue[0]
                    trade_size = min(order.size, maker.size)
                    fills.append((maker, order, best_ask, trade_size))
                    order.size -= trade_size
                    maker.size -= trade_size
                    if maker.size == 0:
                        queue.popleft()
                        del self.orders[maker.order_id]
                if not queue:
                    self._remove_level("sell", best_ask)

            # Unfilled remainder
            if order.size > 0 and order.order_type not in ("market", "ioc"):
                if order.order_type == "post_only" and fills:
                    # Post-only crossed; cancel remainder
                    return fills
                queue = self.bids.setdefault(order.price, deque())
                queue.append(order)
                self.orders[order.order_id] = order

        else:  # sell
            while order.size > 0 and self.bids:
                best_bid = self.best_bid()
                if best_bid is None or (order.order_type != "market" and order.price > best_bid):
                    break
                queue = self.bids[best_bid]
                while queue and order.size > 0:
                    maker = queue[0]
                    trade_size = min(order.size, maker.size)
                    fills.append((maker, order, best_bid, trade_size))
                    order.size -= trade_size
                    maker.size -= trade_size
                    if maker.size == 0:
                        queue.popleft()
                        del self.orders[maker.order_id]
                if not queue:
                    self._remove_level("buy", best_bid)

            if order.size > 0 and order.order_type not in ("market", "ioc"):
                if order.order_type == "post_only" and fills:
                    return fills
                queue = self.asks.setdefault(order.price, deque())
                queue.append(order)
                self.orders[order.order_id] = order

        return fills


class LimitOrderBookEngine(TradingLabEngine):
    @property
    def engine_id(self) -> str:
        return "lob_sim"

    @property
    def name(self) -> str:
        return "Limit Order Book and Execution Engine"

    @property
    def description(self) -> str:
        return "Continuous price-time priority LOB with Poisson flow and Almgren-Chriss benchmarks."

    @property
    def asset_class(self) -> str:
        return "Microstructure / Execution"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "initial_price": Param("initial_price", "float", 100.0, "Starting mid-price", min_val=1.0),
            "parent_size": Param("parent_size", "int", 5000, "Parent order size in shares", min_val=100),
            "parent_side": Param("parent_side", "str", "buy", "Order direction: 'buy' or 'sell'", choices=["buy", "sell"]),
            "n_steps": Param("n_steps", "int", 100, "Execution horizon in discrete steps", min_val=10, max_val=1000),
            "strategy": Param(
                "strategy",
                "str",
                "twap",
                "Execution schedule: 'twap', 'aggressive' (sweep the whole remainder every step), 'almgren_chriss'",
                choices=["twap", "aggressive", "almgren_chriss"],
            ),
            "seed": Param("seed", "int", 42, "Random seed"),
        }

    def run(self, **kwargs: Any) -> LabResult:
        p = self.validate_params(kwargs)
        s0 = float(p["initial_price"])
        q_parent = int(p["parent_size"])
        side = str(p["parent_side"])
        n_steps = int(p["n_steps"])
        strategy = str(p["strategy"])
        seed = int(p["seed"])

        rng = random.Random(seed)
        lob = LimitOrderBook(tick_size=0.01)

        # Seed initial book around s0
        order_seq = 1
        for dist in range(1, 11):
            bid_p = lob.round_tick(s0 - dist * 0.01)
            ask_p = lob.round_tick(s0 + dist * 0.01)
            lob.insert_order(Order(order_seq, "buy", bid_p, 500, 0))
            order_seq += 1
            lob.insert_order(Order(order_seq, "sell", ask_p, 500, 0))
            order_seq += 1

        arrival_price = lob.mid_price() or s0
        remaining_q = q_parent
        executed_shares = 0
        total_spent = 0.0

        # Market-wide volume tracking for VWAP benchmark
        total_market_shares = 0
        total_market_dollars = 0.0
        recent_trades: list[dict[str, Any]] = []

        def record_trade(step: int, price: float, size: int, trade_side: str, aggressor: str) -> None:
            elapsed_ms = step * 1000 + len(recent_trades)
            timestamp = datetime(2000, 1, 1, 9, 30) + timedelta(milliseconds=elapsed_ms)
            recent_trades.append(
                {
                    "step": step,
                    "time": timestamp.strftime("%H:%M:%S.%f")[:-3],
                    "price": round(price, 4),
                    "size": size,
                    "side": trade_side,
                    "aggressor": aggressor,
                }
            )

        ac_schedule = almgren_chriss_schedule(q_parent, n_steps) if strategy == "almgren_chriss" else []
        ac_scheduled = 0

        mid = arrival_price
        for step in range(n_steps):
            book_mid = lob.mid_price()
            if book_mid is not None:
                mid = book_mid

            # 1. Background flow (Poisson arrivals for bids, asks, and random market orders)
            for _ in range(5):
                # Limit orders around current mid
                offset = rng.randint(1, 8) * 0.01
                bg_size = rng.randint(50, 300)
                if rng.random() < 0.5:
                    lob.insert_order(Order(order_seq, "buy", mid - offset, bg_size, step))
                else:
                    lob.insert_order(Order(order_seq, "sell", mid + offset, bg_size, step))
                order_seq += 1

            # Occasional random market orders creating realistic background trade volume
            if rng.random() < 0.60:
                bg_mkt_side = "buy" if rng.random() < 0.5 else "sell"
                bg_mkt_size = rng.randint(100, 400)
                fills = lob.insert_order(Order(order_seq, bg_mkt_side, 0.0, bg_mkt_size, step, order_type="market"))
                order_seq += 1
                for _, _, f_p, f_s in fills:
                    total_market_shares += f_s
                    total_market_dollars += f_p * f_s
                    record_trade(step, f_p, f_s, bg_mkt_side, "market")

            # 2. Agent order placement based on strategy
            child_size = 0
            if strategy == "aggressive":
                child_size = remaining_q
            elif strategy == "twap":
                child_size = math.ceil(remaining_q / (n_steps - step))
            elif strategy == "almgren_chriss":
                ac_scheduled += ac_schedule[step]
                child_size = max(0, remaining_q - (q_parent - ac_scheduled))

            if child_size > 0 and remaining_q > 0:
                alloc_size = min(child_size, remaining_q)
                agent_order = Order(order_seq, side, 0.0, alloc_size, step, order_type="market", is_agent=True)
                order_seq += 1
                agent_fills = lob.insert_order(agent_order)

                for _, _, fill_price, fill_size in agent_fills:
                    executed_shares += fill_size
                    total_spent += fill_price * fill_size
                    remaining_q -= fill_size
                    total_market_shares += fill_size
                    total_market_dollars += fill_price * fill_size
                    record_trade(step, fill_price, fill_size, side, "agent")

        avg_exec_price = total_spent / executed_shares if executed_shares > 0 else arrival_price
        vwap_bench = total_market_dollars / total_market_shares if total_market_shares > 0 else arrival_price

        # Implementation Shortfall in basis points
        # For buy: (avg_exec - arrival) / arrival * 10000
        # For sell: (arrival - avg_exec) / arrival * 10000
        if side == "buy":
            is_bps = ((avg_exec_price - arrival_price) / arrival_price) * 10000.0
            vwap_slip_bps = ((avg_exec_price - vwap_bench) / vwap_bench) * 10000.0
        else:
            is_bps = ((arrival_price - avg_exec_price) / arrival_price) * 10000.0
            vwap_slip_bps = ((vwap_bench - avg_exec_price) / vwap_bench) * 10000.0

        fill_rate = executed_shares / q_parent if q_parent > 0 else 1.0

        metrics = {
            "arrival_price": round(arrival_price, 4),
            "average_execution_price": round(avg_exec_price, 4),
            "vwap_benchmark": round(vwap_bench, 4),
            "implementation_shortfall_bps": round(is_bps, 2),
            "vwap_slippage_bps": round(vwap_slip_bps, 2),
            "fill_rate": round(fill_rate, 4),
            "executed_shares": executed_shares,
            "total_market_volume": total_market_shares,
        }

        summary = (
            f"Executed {executed_shares:,} of {q_parent:,} shares ({fill_rate * 100:.1f}%) "
            f"under '{strategy}' schedule. Avg execution: {avg_exec_price:.4f} vs arrival {arrival_price:.4f} "
            f"(IS: {is_bps:+.1f} bps, VWAP slippage: {vwap_slip_bps:+.1f} bps)."
        )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={"params": p, "trades": recent_trades[-50:]},
            summary=summary,
        )


# Self-register
register(LimitOrderBookEngine())
