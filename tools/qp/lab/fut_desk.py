"""Futures, Basis & Carry Desk Trading Lab Engine.

Models cost-of-carry term structures, calendar spreads, roll yields,
cash-and-carry arbitrage, and crypto perpetual funding rate convergence.
Pure Python standard library implementation.
"""

from __future__ import annotations

import math
import random

from .base import LabResult, Param, TradingLabEngine
from .registry import register


class FuturesDeskEngine(TradingLabEngine):
    """Engine for futures term structures, calendar spreads, and basis arbitrage."""

    @property
    def engine_id(self) -> str:
        return "fut_desk"

    @property
    def name(self) -> str:
        return "Futures, Basis & Carry Desk"

    @property
    def description(self) -> str:
        return "Cost-of-carry term structures, calendar spreads, roll yields, and basis arbitrage simulation."

    @property
    def asset_class(self) -> str:
        return "Futures & Derivatives"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "spot_price": Param(
                name="spot_price",
                param_type="float",
                default=100.0,
                description="Underlying spot asset price.",
                min_val=1.0,
                max_val=100000.0,
            ),
            "risk_free_rate": Param(
                name="risk_free_rate",
                param_type="float",
                default=0.045,
                description="Annualized risk-free financing rate (e.g. 0.045 for 4.5%).",
                min_val=-0.05,
                max_val=0.25,
            ),
            "dividend_yield": Param(
                name="dividend_yield",
                param_type="float",
                default=0.015,
                description="Annualized dividend or income yield on spot asset.",
                min_val=0.0,
                max_val=0.20,
            ),
            "storage_cost": Param(
                name="storage_cost",
                param_type="float",
                default=0.01,
                description="Annualized storage, insurance, and warehousing cost rate.",
                min_val=0.0,
                max_val=0.20,
            ),
            "convenience_yield": Param(
                name="convenience_yield",
                param_type="float",
                default=0.0,
                description="Annualized convenience yield for physical commodity ownership.",
                min_val=0.0,
                max_val=0.30,
            ),
            "maturities_days": Param(
                name="maturities_days",
                param_type="str",
                default="30,60,90,180,360",
                description="Comma-separated contract expirations in days.",
            ),
            "sim_regime": Param(
                name="sim_regime",
                param_type="str",
                default="contango",
                description="Market term structure regime.",
                choices=["contango", "backwardation", "equity_index", "crypto_funding"],
            ),
            "crypto_funding_rate_8h": Param(
                name="crypto_funding_rate_8h",
                param_type="float",
                default=0.0003,
                description="8-hour perpetual contract funding rate (e.g. 0.0003 for 3 bps).",
                min_val=-0.01,
                max_val=0.02,
            ),
            "arbitrage_capital": Param(
                name="arbitrage_capital",
                param_type="float",
                default=100000.0,
                description="Allocated capital for cash-and-carry basis arbitrage.",
                min_val=1000.0,
                max_val=10000000.0,
            ),
            "seed": Param(
                name="seed",
                param_type="int",
                default=42,
                description="Random number generator seed for convergence simulation.",
            ),
        }

    def run(self, **kwargs) -> LabResult:
        p = self.validate_params(kwargs)
        rng = random.Random(p["seed"])

        spot = float(p["spot_price"])
        r = float(p["risk_free_rate"])
        q = float(p["dividend_yield"])
        c = float(p["storage_cost"])
        y = float(p["convenience_yield"])
        regime = str(p["sim_regime"])
        funding_8h = float(p["crypto_funding_rate_8h"])
        capital = float(p["arbitrage_capital"])

        # Override carry parameters according to selected market regime
        if regime == "contango":
            # High storage cost, zero convenience yield -> upward sloping forward curve
            c = max(c, 0.04)
            y = 0.0
            q = 0.0
        elif regime == "backwardation":
            # Severe physical scarcity: convenience yield dominates financing and storage
            y = max(y, 0.12)
            c = 0.01
            q = 0.0
        elif regime == "equity_index":
            # Traditional financial index: r - q
            c = 0.0
            y = 0.0
        elif regime == "crypto_funding":
            # Perpetual funding rate drives effective annualized carry
            annual_funding = funding_8h * 3.0 * 365.0
            c = 0.0
            y = 0.0
            # Let the funding rate represent the forward premium / basis spread
            r = annual_funding

        # Parse maturities
        try:
            days_list = [int(d.strip()) for d in str(p["maturities_days"]).split(",") if d.strip()]
        except Exception:
            days_list = [30, 60, 90, 180, 360]

        if not days_list:
            days_list = [30, 60, 90, 180, 360]
        days_list.sort()

        # Net cost of carry rate
        net_carry_rate = (r - q + c) - y

        term_structure = []
        for days in days_list:
            t = days / 365.0
            # Continuous cost-of-carry model: F = S * exp(net_carry * T)
            f_theo = spot * math.exp(net_carry_rate * t)
            # Add small microstructure basis noise (+- 5 to 15 bps)
            noise_pct = rng.uniform(-0.0015, 0.0015)
            f_market = f_theo * (1.0 + noise_pct)

            basis_dollar = f_market - spot
            basis_pct = (basis_dollar / spot) * 100.0
            annualized_basis = (basis_pct / t) if t > 0 else 0.0

            term_structure.append(
                {
                    "days": days,
                    "years": round(t, 4),
                    "theoretical_future": round(f_theo, 4),
                    "market_future": round(f_market, 4),
                    "basis_dollar": round(basis_dollar, 4),
                    "basis_pct": round(basis_pct, 4),
                    "annualized_basis_pct": round(annualized_basis, 2),
                }
            )

        # Front month (T1) and next month (T2) calendar spread
        front_contract = term_structure[0]
        next_contract = term_structure[1] if len(term_structure) > 1 else term_structure[0]
        calendar_spread = next_contract["market_future"] - front_contract["market_future"]
        calendar_spread_pct = (calendar_spread / front_contract["market_future"]) * 100.0

        # Roll yield: - (F2 - F1) / F1 normalized
        roll_days_diff = next_contract["days"] - front_contract["days"]
        roll_yield_annual = (
            -(calendar_spread / front_contract["market_future"]) * (365.0 / roll_days_diff) * 100.0 if roll_days_diff > 0 else 0.0
        )

        # Cash-and-carry arbitrage simulation on front contract
        # Strategy: Buy Spot with borrowed capital at rate r, Short Future at F_market
        front_t = front_contract["years"]
        units = capital / spot
        borrowed_cost = capital * (math.exp(r * front_t) - 1.0)
        dividend_collected = capital * (math.exp(q * front_t) - 1.0)
        storage_paid = capital * (math.exp(c * front_t) - 1.0)

        # At expiration T: Spot converges to Future
        revenue_from_short = units * front_contract["market_future"]
        net_repayment = capital + borrowed_cost + storage_paid - dividend_collected
        arb_net_pnl = revenue_from_short - net_repayment
        arb_annualized_roi = (arb_net_pnl / capital) * (1.0 / front_t) * 100.0 if front_t > 0 else 0.0

        # Multi-day convergence path simulation for front contract
        convergence_path = []
        n_steps = front_contract["days"]
        cur_spot = spot

        # Daily drift and volatility for spot
        daily_vol = 0.012  # ~19% annual
        for day in range(n_steps + 1):
            remaining_t = (n_steps - day) / 365.0
            # As time reaches 0, future converges directly to spot
            theoretical_f_now = cur_spot * math.exp(net_carry_rate * remaining_t)
            basis_premium = (front_contract["market_future"] - front_contract["theoretical_future"]) * ((n_steps - day) / n_steps)
            sim_fut = theoretical_f_now + basis_premium

            convergence_path.append(
                {
                    "day": day,
                    "spot": round(cur_spot, 2),
                    "future": round(sim_fut, 2),
                    "basis": round(sim_fut - cur_spot, 4),
                }
            )

            # Advance spot price for next day
            shock = rng.gauss(0, daily_vol)
            cur_spot *= math.exp(shock)

        curve_shape = "Contango" if net_carry_rate > 0.005 else ("Backwardation" if net_carry_rate < -0.005 else "Flat")

        metrics: dict[str, float | int | str] = {
            "spot_price": round(spot, 2),
            "net_carry_rate_pct": round(net_carry_rate * 100.0, 3),
            "curve_structure": curve_shape,
            "front_contract_days": front_contract["days"],
            "front_future_price": front_contract["market_future"],
            "front_basis_pct": front_contract["basis_pct"],
            "front_annualized_basis_pct": front_contract["annualized_basis_pct"],
            "calendar_spread_dollar": round(calendar_spread, 4),
            "calendar_spread_pct": round(calendar_spread_pct, 4),
            "annualized_roll_yield_pct": round(roll_yield_annual, 2),
            "arb_net_pnl": round(arb_net_pnl, 2),
            "arb_annualized_roi_pct": round(arb_annualized_roi, 2),
            "regime": regime,
        }

        summary = (
            f"Term structure is in {curve_shape} (net carry: {net_carry_rate * 100:.2f}%). "
            f"Front {front_contract['days']}d contract trades at {front_contract['market_future']:.2f} "
            f"({front_contract['basis_pct']:+.2f}% basis). Calendar roll yield is {roll_yield_annual:+.2f}% annualized. "
            f"Cash-and-carry basis trade generates ${arb_net_pnl:,.2f} net profit ({arb_annualized_roi:.2f}% annualized ROI)."
        )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={
                "params": p,
                "term_structure": term_structure,
                "convergence_path": convergence_path[:60],  # sample 60 days for visualization
            },
            summary=summary,
        )


# Self-register upon import
register(FuturesDeskEngine())
