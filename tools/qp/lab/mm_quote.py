"""Automated Two-Sided Market Maker Engine (`mm_quote`).

Implements the Avellaneda-Stoikov (2008) optimal quoting framework under inventory risk,
Glosten-Milgrom (1985) adverse selection, and exact PnL attribution:
Total PnL = Spread Capture + Inventory PnL + Adverse Selection (Markout) - Fees.

Units: one run is a single trading-day session (T = 1, 252 sessions a year) split into
`n_steps` quoting steps, inventory is counted in lots of `LOT_SIZE` shares, and the
user-facing `gamma` and `kappa` are per 1% of mid.
`dollar_units` converts them to the absolute units of the paper, so every quote scales
with price: the same seed at 10x the price gives 10x the quotes and 10x the PnL.
A configuration whose flat opening bid is non-positive is rejected; during the run the
bid is withdrawn (not posted) on any step where inventory skew pushes it to zero or below.
"""

from __future__ import annotations

import math
import random
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .registry import register

SESSIONS_PER_YEAR = 252.0
LOT_SIZE = 100
FEE_BPS = 0.1
INFORMED_MOVE_SIGMAS = 1.5
MAX_FILL_PROBABILITY = 0.95


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
            "gamma": Param("gamma", "float", 0.1, "Risk aversion per 1% of mid", min_val=0.001, max_val=10.0),
            "sigma": Param("sigma", "float", 0.20, "Annualized asset volatility", min_val=0.01, max_val=2.0),
            "kappa": Param("kappa", "float", 1.5, "Order arrival decay per 1% of mid from the quote", min_val=0.1, max_val=10.0),
            "informed_fraction": Param(
                "informed_fraction",
                "float",
                0.20,
                "Fraction of trades from informed counterparties",
                min_val=0.0,
                max_val=0.9,
            ),
            "n_steps": Param("n_steps", "int", 100, "Quoting steps in the one-day session", min_val=10, max_val=1000),
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
        inventory: float,
        gamma: float,
        sigma: float,
        kappa: float,
        time_left: float,
    ) -> tuple[float, float, float]:
        """Compute reservation price and optimal bid/ask quotes in the paper's absolute units.

        `sigma` is dollar volatility per square root of the time unit, `gamma` and `kappa`
        are per dollar, `inventory` is in lots and `time_left` is T - t in the same time unit.

        r(s, q, t) = s - q * gamma * sigma^2 * (T - t)
        delta_spread = gamma * sigma^2 * (T - t) + (2 / gamma) * ln(1 + gamma / kappa)
        """
        vol_term = gamma * (sigma**2) * time_left
        reservation_price = mid - (inventory * vol_term)
        optimal_half_spread = 0.5 * (vol_term + (2.0 / gamma) * math.log(1.0 + gamma / kappa))
        return reservation_price, reservation_price - optimal_half_spread, reservation_price + optimal_half_spread

    @staticmethod
    def dollar_units(mid: float, sigma: float, gamma: float, kappa: float) -> tuple[float, float, float]:
        """Convert annual fractional sigma and per-1%-of-mid gamma and kappa to per-dollar, per-session units."""
        one_pct = 0.01 * mid
        return sigma * mid / math.sqrt(SESSIONS_PER_YEAR), gamma / one_pct, kappa / one_pct

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

        sigma_d, gamma_d, kappa_d = self.dollar_units(mid, sigma, gamma, kappa)
        _r, opening_bid, opening_ask = self.avellaneda_stoikov_quotes(mid, 0, gamma_d, sigma_d, kappa_d, 1.0)
        if opening_bid <= 0.0:
            raise ValueError(
                f"gamma={gamma}, sigma={sigma}, kappa={kappa} give an opening half-spread of "
                f"{(opening_ask - mid) / mid:.1%} of mid, so the bid would be non-positive; "
                "lower gamma or sigma, or raise kappa"
            )
        naive_half_spread_frac = (opening_ask - mid) / mid

        rng = random.Random(seed)
        step_vol = sigma / math.sqrt(SESSIONS_PER_YEAR) * math.sqrt(1.0 / n_steps)

        inventory = 0
        cash = 0.0

        spread_capture = 0.0
        adverse_selection = 0.0
        inventory_pnl = 0.0
        exchange_fees = 0.0

        trades_executed = 0
        bid_withdrawn_steps = 0

        price_history = [round(mid, 6)]
        inventory_history = [0]
        quotes: list[dict[str, Any]] = []
        fills: list[dict[str, Any]] = []

        for step in range(n_steps):
            time_left = (n_steps - step) / n_steps
            pre_trade_mid = mid

            if strategy == "avellaneda_stoikov":
                sigma_d, gamma_d, kappa_d = self.dollar_units(mid, sigma, gamma, kappa)
                reservation, bid, ask = self.avellaneda_stoikov_quotes(mid, inventory / LOT_SIZE, gamma_d, sigma_d, kappa_d, time_left)
            else:
                kappa_d = kappa / (0.01 * mid)
                reservation = mid
                bid = mid * (1.0 - naive_half_spread_frac)
                ask = mid * (1.0 + naive_half_spread_frac)

            bid_live = bid > 0.0
            if not bid_live:
                bid_withdrawn_steps += 1
            quotes.append(
                {
                    "step": step,
                    "time_left": round(time_left, 6),
                    "mid": round(mid, 6),
                    "inventory_lots": inventory // LOT_SIZE,
                    "reservation": round(reservation, 6),
                    "bid": round(bid, 6) if bid_live else None,
                    "ask": round(ask, 6),
                }
            )

            # Fill intensity lambda = exp(-kappa * delta), with delta the quote's distance from mid
            p_ask_fill = min(MAX_FILL_PROBABILITY, math.exp(-kappa_d * max(0.0, ask - mid)))
            p_bid_fill = min(MAX_FILL_PROBABILITY, math.exp(-kappa_d * max(0.0, mid - bid))) if bid_live else 0.0

            z = rng.gauss(0.0, 1.0)
            mid *= math.exp(step_vol * z - 0.5 * step_vol**2)

            step_fills: list[tuple[int, float, bool]] = []
            if rng.random() < p_ask_fill:
                is_informed = rng.random() < alpha_informed
                step_fills.append((-1, ask, is_informed))
                if is_informed:
                    mid *= math.exp(INFORMED_MOVE_SIGMAS * step_vol)

            if bid_live and rng.random() < p_bid_fill:
                is_informed = rng.random() < alpha_informed
                step_fills.append((1, bid, is_informed))
                if is_informed:
                    mid *= math.exp(-INFORMED_MOVE_SIGMAS * step_vol)

            inventory_pnl += inventory * (mid - pre_trade_mid)
            for side, price, is_informed in step_fills:
                fee = FEE_BPS * 1e-4 * price * LOT_SIZE
                inventory += side * LOT_SIZE
                cash -= side * price * LOT_SIZE + fee
                exchange_fees += fee
                trades_executed += 1
                spread_capture += side * (pre_trade_mid - price) * LOT_SIZE
                markout = side * (mid - pre_trade_mid) * LOT_SIZE
                adverse_selection += markout
                fills.append(
                    {
                        "step": step,
                        "side": "buy" if side > 0 else "sell",
                        "price": round(price, 6),
                        "pre_mid": round(pre_trade_mid, 6),
                        "post_mid": round(mid, 6),
                        "informed": is_informed,
                        "markout": round(markout, 6),
                    }
                )

            price_history.append(round(mid, 6))
            inventory_history.append(inventory)

        ending_mid = mid
        total_pnl = cash + inventory * ending_mid

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
                "quotes": quotes,
                "fills": fills,
                "bid_withdrawn_steps": bid_withdrawn_steps,
            },
            summary=summary,
        )


# Self-register
register(MarketMakerEngine())
