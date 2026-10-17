"""Automated Two-Sided Market Maker Engine (`mm_quote`).

Implements the Avellaneda-Stoikov (2008) optimal quoting framework under inventory risk,
Glosten-Milgrom (1985) adverse selection, and exact PnL attribution:
Total PnL = Spread Capture + Inventory PnL + Adverse Selection (Markout) - Fees.
"""

from __future__ import annotations

import math
import random
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .registry import register


class MarketMakerEngine(TradingLabEngine):
    @property
    def engine_id(self) -> str:
        return "mm_quote"

    @property
    def name(self) -> str:
        return "Two-Sided Market Maker Quoting Engine"

    @property
    def description(self) -> str:
        return "Avellaneda-Stoikov inventory control, adverse selection, and exact PnL attribution."

    @property
    def asset_class(self) -> str:
        return "Market Making / Microstructure"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "initial_price": Param("initial_price", "float", 100.0, "Starting fair value mid-price", min_val=1.0),
            "gamma": Param("gamma", "float", 0.1, "Risk aversion parameter", min_val=0.001, max_val=10.0),
            "sigma": Param("sigma", "float", 0.20, "Annualized asset volatility", min_val=0.01, max_val=2.0),
            "kappa": Param("kappa", "float", 1.5, "Order arrival liquidity density", min_val=0.1, max_val=10.0),
            "informed_fraction": Param(
                "informed_fraction",
                "float",
                0.20,
                "Fraction of trades from informed counterparties",
                min_val=0.0,
                max_val=0.9,
            ),
            "n_steps": Param("n_steps", "int", 100, "Number of quoting steps", min_val=10, max_val=1000),
            "strategy": Param(
                "strategy",
                "str",
                "avellaneda_stoikov",
                "Quoting rule: 'avellaneda_stoikov' or 'naive_symmetric'",
                choices=["avellaneda_stoikov", "naive_symmetric"],
            ),
            "seed": Param("seed", "int", 42, "Random seed"),
        }

    @staticmethod
    def avellaneda_stoikov_quotes(
        mid: float,
        inventory: int,
        gamma: float,
        sigma: float,
        kappa: float,
        time_left: float,
    ) -> tuple[float, float, float]:
        """Compute reservation price and optimal bid/ask quotes.

        r(s, q, t) = s - q * gamma * sigma^2 * (T - t)
        delta_spread = gamma * sigma^2 * (T - t) + (2 / gamma) * ln(1 + gamma / kappa)
        """
        vol_term = gamma * (sigma**2) * max(1e-4, time_left)
        reservation_price = mid - (inventory * vol_term)
        optimal_half_spread = 0.5 * (vol_term + (2.0 / gamma) * math.log(1.0 + gamma / kappa))

        bid = reservation_price - optimal_half_spread
        ask = reservation_price + optimal_half_spread
        return round(reservation_price, 4), round(bid, 4), round(ask, 4)

    def run(self, **kwargs: Any) -> LabResult:
        p = self.validate_params(kwargs)
        mid = float(p["initial_price"])
        gamma = float(p["gamma"])
        sigma = float(p["sigma"])
        kappa = float(p["kappa"])
        alpha_informed = float(p["informed_fraction"])
        n_steps = int(p["n_steps"])
        strategy = str(p["strategy"])
        seed = int(p["seed"])

        rng = random.Random(seed)
        dt = 1.0 / 252.0
        time_left_total = 1.0

        inventory = 0
        cash = 0.0

        # Exact PnL attribution buckets
        spread_capture = 0.0
        adverse_selection = 0.0
        exchange_fees = 0.0
        fee_per_share = 0.001  # 10 bps maker rebate / taker fee structure

        trades_executed = 0
        starting_mid = mid

        price_history = [starting_mid]
        inventory_history = [0]

        for step in range(n_steps):
            time_left = max(1e-4, time_left_total * (n_steps - step) / n_steps)

            # Quoting decision
            if strategy == "avellaneda_stoikov":
                _res_p, bid, ask = self.avellaneda_stoikov_quotes(mid, inventory, gamma, sigma, kappa, time_left)
            else:  # naive symmetric
                half_spread = 0.05
                bid = round(mid - half_spread, 4)
                ask = round(mid + half_spread, 4)

            # Flow arrival (Poisson)
            # Distance from mid influences fill probability: lambda = A * exp(-kappa * delta)
            delta_bid = mid - bid
            delta_ask = ask - mid

            p_bid_fill = max(0.01, min(0.95, math.exp(-kappa * max(0.01, delta_bid))))
            p_ask_fill = max(0.01, min(0.95, math.exp(-kappa * max(0.01, delta_ask))))

            pre_trade_mid = mid

            # Mid price diffusion for step
            z = rng.gauss(0.0, 1.0)
            mid_drift = (sigma * math.sqrt(dt)) * z
            mid = round(mid * math.exp(mid_drift), 4)

            # Check for buys of our ask (market buy arriving)
            if rng.random() < p_ask_fill:
                is_informed = rng.random() < alpha_informed
                trade_size = 100
                inventory -= trade_size
                cash += ask * trade_size
                trades_executed += 1
                exchange_fees += trade_size * fee_per_share

                # Spread capture vs mid: (ask - pre_mid)
                spread_capture += (ask - pre_trade_mid) * trade_size

                # If informed, mid moves adversely post-trade
                if is_informed:
                    adverse_move = (sigma * math.sqrt(dt)) * 1.5
                    mid = round(mid * math.exp(adverse_move), 4)
                    adverse_selection -= abs(mid - pre_trade_mid) * trade_size

            # Check for sells to our bid (market sell arriving)
            if rng.random() < p_bid_fill:
                is_informed = rng.random() < alpha_informed
                trade_size = 100
                inventory += trade_size
                cash -= bid * trade_size
                trades_executed += 1
                exchange_fees += trade_size * fee_per_share

                # Spread capture vs mid: (pre_mid - bid)
                spread_capture += (pre_trade_mid - bid) * trade_size

                if is_informed:
                    adverse_move = -(sigma * math.sqrt(dt)) * 1.5
                    mid = round(mid * math.exp(adverse_move), 4)
                    adverse_selection -= abs(pre_trade_mid - mid) * trade_size

            price_history.append(mid)
            inventory_history.append(inventory)

        # Mark-to-market ending valuation
        ending_mid = mid
        ending_inventory_value = inventory * ending_mid
        total_pnl = cash + ending_inventory_value

        # Inventory PnL is total_pnl minus (spread_capture + adverse_selection - exchange_fees)
        # ensuring mathematical identity: Total = Spread + Inventory + Adverse - Fees
        inventory_pnl = total_pnl - (spread_capture + adverse_selection - exchange_fees)

        metrics = {
            "total_pnl": round(total_pnl, 2),
            "spread_capture": round(spread_capture, 2),
            "inventory_pnl": round(inventory_pnl, 2),
            "adverse_selection": round(adverse_selection, 2),
            "exchange_fees": round(exchange_fees, 2),
            "final_inventory": inventory,
            "ending_mid_price": round(ending_mid, 4),
            "trades_executed": trades_executed,
        }

        summary = (
            f"Strategy '{strategy}' generated Total PnL of ${total_pnl:+,.2f} across {trades_executed} fills. "
            f"Attribution: Spread capture: ${spread_capture:+,.2f}, Inventory: ${inventory_pnl:+,.2f}, "
            f"Adverse selection: ${adverse_selection:+,.2f}, Fees: ${exchange_fees:,.2f}."
        )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={
                "params": p,
                "price_history": price_history,
                "inventory_history": inventory_history,
            },
            summary=summary,
        )


# Self-register
register(MarketMakerEngine())
