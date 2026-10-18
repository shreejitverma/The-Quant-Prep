"""Options Volatility Desk and Greeks Hedging Simulator.

Simulates Black-Scholes pricing, analytical Greeks, volatility surfaces,
dynamic delta hedging (gamma scalping), earnings vol crush, and PnL attribution.
Standard-library only, fully deterministic.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable

from .base import LabResult, Param, TradingLabEngine
from .registry import register

GREEK_DECIMALS = {
    "delta": 4,
    "gamma": 5,
    "vega": 4,
    "vega_unit": 4,
    "theta_daily": 4,
    "theta_annual": 2,
    "rho": 4,
    "vanna": 4,
    "volga": 4,
}
HEDGE_BAND_SHARES = 0.01
COMPONENT_TO_INDEX_VOL = 1.40


class OptionsDeskEngine(TradingLabEngine):
    @property
    def engine_id(self) -> str:
        return "opt_desk"

    @property
    def name(self) -> str:
        return "Options Volatility Desk and Greeks Hedging Engine"

    @property
    def description(self) -> str:
        return (
            "Simulates Black-Scholes pricing, analytical Greeks, dynamic delta-hedging, "
            "gamma scalping, earnings volatility crush, and exact PnL attribution."
        )

    @property
    def asset_class(self) -> str:
        return "Options & Volatility / Derivatives"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "scenario": Param(
                name="scenario",
                param_type="str",
                default="gamma_scalp",
                description="Simulation scenario: gamma_scalp, earnings_crush, skew_shift, dispersion",
                choices=["gamma_scalp", "earnings_crush", "skew_shift", "dispersion"],
            ),
            "spot": Param(
                name="spot",
                param_type="float",
                default=100.0,
                description="Current underlying asset spot price ($)",
                min_val=1.0,
                max_val=10000.0,
            ),
            "strike": Param(
                name="strike",
                param_type="float",
                default=100.0,
                description="Option strike price ($)",
                min_val=1.0,
                max_val=10000.0,
            ),
            "implied_vol": Param(
                name="implied_vol",
                param_type="float",
                default=0.25,
                description="Initial implied volatility sigma (e.g. 0.25 = 25%)",
                min_val=0.01,
                max_val=3.0,
            ),
            "realized_vol": Param(
                name="realized_vol",
                param_type="float",
                default=0.32,
                description="Actual realized asset volatility sigma during simulation",
                min_val=0.01,
                max_val=3.0,
            ),
            "days_to_expiry": Param(
                name="days_to_expiry",
                param_type="int",
                default=30,
                description="Option tenor in calendar days",
                min_val=1,
                max_val=365,
            ),
            "risk_free_rate": Param(
                name="risk_free_rate",
                param_type="float",
                default=0.04,
                description="Annualized risk-free interest rate (e.g. 0.04 = 4%)",
                min_val=0.0,
                max_val=0.25,
            ),
            "hedge_frequency_hours": Param(
                name="hedge_frequency_hours",
                param_type="int",
                default=4,
                description="Hours between dynamic delta hedge rebalances",
                min_val=1,
                max_val=24,
            ),
            "seed": Param(
                name="seed",
                param_type="int",
                default=42,
                description="Deterministic random number seed",
            ),
        }

    # --- Black-Scholes-Merton Core Mathematics ---

    @staticmethod
    def std_norm_cdf(x: float) -> float:
        """Cumulative distribution function of standard normal distribution."""
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    @staticmethod
    def std_norm_pdf(x: float) -> float:
        """Probability density function of standard normal distribution."""
        return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)

    @classmethod
    def calc_d1_d2(cls, s: float, k: float, t: float, r: float, sigma: float, q: float = 0.0) -> tuple[float, float]:
        if t <= 0.0 or sigma <= 0.0:
            return 0.0, 0.0
        d1 = (math.log(s / k) + (r - q + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
        d2 = d1 - sigma * math.sqrt(t)
        return d1, d2

    @classmethod
    def bsm_price(cls, s: float, k: float, t: float, r: float, sigma: float, option_type: str = "call", q: float = 0.0) -> float:
        """European Black-Scholes-Merton pricing."""
        if t <= 1e-6:
            return max(0.0, s - k) if option_type == "call" else max(0.0, k - s)
        d1, d2 = cls.calc_d1_d2(s, k, t, r, sigma, q)
        disc_r = math.exp(-r * t)
        disc_q = math.exp(-q * t)
        if option_type == "call":
            return s * disc_q * cls.std_norm_cdf(d1) - k * disc_r * cls.std_norm_cdf(d2)
        else:
            return k * disc_r * cls.std_norm_cdf(-d2) - s * disc_q * cls.std_norm_cdf(-d1)

    @classmethod
    def bsm_greeks(
        cls, s: float, k: float, t: float, r: float, sigma: float, option_type: str = "call", q: float = 0.0
    ) -> dict[str, float]:
        """Analytical first, second, and third order Greeks."""
        if t <= 1e-6:
            if option_type == "call":
                delta = 1.0 if s > k else 0.0
            else:
                delta = -1.0 if s < k else 0.0
            return {name: delta if name == "delta" else 0.0 for name in GREEK_DECIMALS}

        d1, d2 = cls.calc_d1_d2(s, k, t, r, sigma, q)
        sqrt_t = math.sqrt(t)
        pdf_d1 = cls.std_norm_pdf(d1)
        disc_q = math.exp(-q * t)
        disc_r = math.exp(-r * t)

        # Delta
        if option_type == "call":
            delta = disc_q * cls.std_norm_cdf(d1)
        else:
            delta = -disc_q * cls.std_norm_cdf(-d1)

        # Gamma (identical for Call and Put)
        gamma = (disc_q * pdf_d1) / (s * sigma * sqrt_t)

        # Vega (per 1.0 unit of sigma, and per 1% vol change)
        vega_unit = s * disc_q * pdf_d1 * sqrt_t
        vega_1pct = vega_unit / 100.0

        # Theta (annualized and per calendar day)
        term1 = -(s * disc_q * pdf_d1 * sigma) / (2.0 * sqrt_t)
        if option_type == "call":
            theta_ann = term1 - r * k * disc_r * cls.std_norm_cdf(d2) + q * s * disc_q * cls.std_norm_cdf(d1)
        else:
            theta_ann = term1 + r * k * disc_r * cls.std_norm_cdf(-d2) - q * s * disc_q * cls.std_norm_cdf(-d1)
        theta_daily = theta_ann / 365.0

        # Rho (per 1% interest rate change)
        if option_type == "call":
            rho = (k * t * disc_r * cls.std_norm_cdf(d2)) / 100.0
        else:
            rho = (-k * t * disc_r * cls.std_norm_cdf(-d2)) / 100.0

        # Higher-Order Greeks
        vanna = -disc_q * pdf_d1 * (d2 / sigma)
        volga = vega_unit * ((d1 * d2) / sigma)

        return {
            "delta": delta,
            "gamma": gamma,
            "vega": vega_1pct,
            "vega_unit": vega_unit,
            "theta_daily": theta_daily,
            "theta_annual": theta_ann,
            "rho": rho,
            "vanna": vanna,
            "volga": volga,
        }

    @staticmethod
    def round_greeks(greeks: dict[str, float]) -> dict[str, float]:
        return {name: round(value, GREEK_DECIMALS[name]) for name, value in greeks.items()}

    @classmethod
    def straddle_greeks(cls, s: float, k: float, t: float, r: float, sigma: float) -> dict[str, float]:
        call = cls.bsm_greeks(s, k, t, r, sigma, "call")
        put = cls.bsm_greeks(s, k, t, r, sigma, "put")
        return {name: call[name] + put[name] for name in call}

    @classmethod
    def put_delta_strike(cls, s: float, t: float, r: float, vol_at: Callable[[float], float], target_delta: float = -0.25) -> float:
        """Strike whose put delta, priced at that strike's own smile vol, equals target_delta."""

        def excess(log_m: float) -> float:
            stk = s * math.exp(log_m)
            return cls.bsm_greeks(s, stk, t, r, vol_at(stk), "put")["delta"] - target_delta

        grid = [-6.0 + 0.01 * i for i in range(801)]
        values = [excess(log_m) for log_m in grid]
        bracket = next((i for i in range(len(grid) - 1) if values[i] > 0.0 >= values[i + 1]), None)
        if bracket is None:
            raise ValueError(f"No strike has a put delta of {target_delta} on this smile; lower implied_vol or days_to_expiry")
        lo, hi = grid[bracket], grid[bracket + 1]
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if excess(mid) > 0.0:
                lo = mid
            else:
                hi = mid
        return s * math.exp(0.5 * (lo + hi))

    def run(self, **kwargs) -> LabResult:
        params = self.validate_params(kwargs)
        scenario = params["scenario"]
        s0 = params["spot"]
        k = params["strike"]
        iv = params["implied_vol"]
        rv = params["realized_vol"]
        days = params["days_to_expiry"]
        r = params["risk_free_rate"]
        hedge_hrs = params["hedge_frequency_hours"]
        seed = params["seed"]

        rng = random.Random(seed)
        t_years = days / 365.0
        hours_per_year = 24.0 * 365.0

        # Initial option pricing for the straddle
        call_init = self.bsm_price(s0, k, t_years, r, iv, "call")
        put_init = self.bsm_price(s0, k, t_years, r, iv, "put")
        straddle_cost = call_init + put_init

        call_greeks = self.bsm_greeks(s0, k, t_years, r, iv, "call")
        put_greeks = self.bsm_greeks(s0, k, t_years, r, iv, "put")
        net_greeks = {name: call_greeks[name] + put_greeks[name] for name in call_greeks}

        if scenario == "gamma_scalp":
            # Dynamic delta hedging of a long straddle, rebalanced every hedge_hrs hours
            total_hours = days * 24
            total_steps = math.ceil(total_hours / hedge_hrs)

            spot = s0
            held = net_greeks
            stock_shares = -held["delta"]
            cash = -straddle_cost - (stock_shares * spot)
            total_hedges = 0
            max_residual_delta = 0.0
            elapsed_hours = 0

            gamma_pnl_accum = 0.0
            theta_cost_accum = 0.0

            for step in range(1, total_steps + 1):
                step_hours = min(hedge_hrs, total_hours - elapsed_hours)
                elapsed_hours += step_hours
                dt = step_hours / hours_per_year
                time_left = (total_hours - elapsed_hours) / hours_per_year

                cash *= math.exp(r * dt)

                # Underlying path under realized volatility
                z = rng.gauss(0.0, 1.0)
                prev_spot = spot
                spot *= math.exp((r - 0.5 * rv * rv) * dt + rv * math.sqrt(dt) * z)
                delta_s = spot - prev_spot

                # Attribution uses the Greeks held over the interval: 1/2 * Gamma * (Delta S)^2 and Theta * dt
                gamma_pnl_accum += 0.5 * held["gamma"] * (delta_s**2)
                theta_cost_accum -= held["theta_annual"] * dt

                if step == total_steps:
                    break

                held = self.straddle_greeks(spot, k, time_left, r, iv)
                hedge_trade = -held["delta"] - stock_shares
                if abs(hedge_trade) >= HEDGE_BAND_SHARES:
                    stock_shares += hedge_trade
                    cash -= hedge_trade * spot
                    total_hedges += 1
                max_residual_delta = max(max_residual_delta, abs(held["delta"] + stock_shares))

            # Final settlement at expiration
            final_straddle_val = max(0.0, spot - k) + max(0.0, k - spot)
            total_pnl = cash + final_straddle_val + (stock_shares * spot)

            metrics = {
                "scenario": scenario,
                "initial_straddle_cost": round(straddle_cost, 2),
                "final_spot_price": round(spot, 2),
                "total_rebalances": total_hedges,
                "gross_gamma_pnl": round(gamma_pnl_accum, 2),
                "total_theta_decay_cost": round(theta_cost_accum, 2),
                "net_hedged_pnl": round(total_pnl, 2),
                "vol_differential_pct": round((rv - iv) * 100, 1),
                "max_residual_delta": round(max_residual_delta, 4),
            }

            summary = (
                f"Gamma scalping simulation complete ({days} days, {total_hedges} rebalances). "
                f"Realized Vol ({rv * 100:.1f}%) vs Implied Vol ({iv * 100:.1f}%). "
                f"Gamma Captured: ${gamma_pnl_accum:+,.2f}, Theta Decayed: ${theta_cost_accum:,.2f}, "
                f"Net Strategy PnL: ${total_pnl:+,.2f}."
            )

        elif scenario == "earnings_crush":
            # Short straddle ahead of earnings: implied vol is crushed by 55% (not below 12%, never upward)
            pre_iv = iv
            post_iv = min(iv, max(0.12, iv * 0.45))
            gap_sigma = rv / math.sqrt(252.0) * 2.0
            post_spot = s0 * math.exp(gap_sigma * rng.gauss(0.0, 1.0) - 0.5 * gap_sigma * gap_sigma)
            earnings_move_pct = post_spot / s0 - 1.0
            post_days = max(1, days - 1)
            post_t = post_days / 365.0

            pre_straddle = straddle_cost
            post_straddle = self.bsm_price(post_spot, k, post_t, r, post_iv, "call") + self.bsm_price(
                post_spot, k, post_t, r, post_iv, "put"
            )

            short_straddle_pnl = pre_straddle - post_straddle
            iv_drop_pts = (pre_iv - post_iv) * 100.0
            vega_pnl = net_greeks["vega"] * iv_drop_pts

            metrics = {
                "scenario": scenario,
                "pre_earnings_iv_pct": round(pre_iv * 100, 1),
                "post_earnings_iv_pct": round(post_iv * 100, 1),
                "underlying_jump_pct": round(earnings_move_pct * 100, 2),
                "pre_straddle_price": round(pre_straddle, 2),
                "post_straddle_price": round(post_straddle, 2),
                "short_straddle_pnl": round(short_straddle_pnl, 2),
                "vega_pnl_attribution": round(vega_pnl, 2),
            }

            summary = (
                f"Earnings volatility crush simulation: IV collapsed from {pre_iv * 100:.1f}% to {post_iv * 100:.1f}%. "
                f"Stock jumped {earnings_move_pct * 100:+.2f}%. Short Straddle PnL: ${short_straddle_pnl:+,.2f}."
            )

        elif scenario == "skew_shift":
            # SVI-style quadratic volatility smile in log-moneyness
            base_skew = -0.15  # negative equity index skew
            stress_skew = -0.35  # steepening put bid during panic

            def calm_vol(stk: float) -> float:
                log_m = math.log(stk / s0)
                return max(0.05, iv + base_skew * log_m + 0.20 * (log_m**2))

            def stressed_vol(stk: float) -> float:
                log_m = math.log(stk / s0)
                return max(0.05, iv + 0.08 + stress_skew * log_m + 0.40 * (log_m**2))

            put25_calm = self.put_delta_strike(s0, t_years, r, calm_vol)
            put25_stressed = self.put_delta_strike(s0, t_years, r, stressed_vol)

            metrics = {
                "scenario": scenario,
                "atm_vol": round(calm_vol(s0), 3),
                "base_skew_slope": base_skew,
                "stressed_skew_slope": stress_skew,
                "25d_put_strike_calm": round(put25_calm, 2),
                "25d_put_vol_calm": round(calm_vol(put25_calm), 4),
                "25d_put_strike_stressed": round(put25_stressed, 2),
                "25d_put_vol_stressed": round(stressed_vol(put25_stressed), 4),
            }

            summary = (
                f"Volatility skew steepening simulation: 25-delta put implied volatility shifted from "
                f"{calm_vol(put25_calm) * 100:.1f}% (strike {put25_calm:,.2f}) to "
                f"{stressed_vol(put25_stressed) * 100:.1f}% (strike {put25_stressed:,.2f})."
            )

        else:  # dispersion
            # Long single-stock variance vs short index variance. For a large equal-weight basket the index
            # variance is rho * component variance, so implied and realized correlation follow from the vols.
            # implied_vol is the index implied vol, realized_vol the realized index vol; components are priced
            # at COMPONENT_TO_INDEX_VOL times the index vol and realize at least their implied vol.
            index_vol = iv
            component_vol = iv * COMPONENT_TO_INDEX_VOL
            component_realized_vol = max(component_vol, rv)
            implied_corr = (index_vol / component_vol) ** 2
            realized_corr = (rv / component_realized_vol) ** 2

            dispersion_edge = (component_vol**2) - (index_vol**2)
            component_leg_pnl = component_realized_vol**2 - component_vol**2
            index_leg_pnl = index_vol**2 - rv**2
            dispersion_pnl = component_leg_pnl + index_leg_pnl
            if dispersion_pnl > 0.0:
                status = "PROFITABLE_LONG_DISPERSION"
            elif dispersion_pnl < 0.0:
                status = "LOSING_LONG_DISPERSION"
            else:
                status = "FLAT_LONG_DISPERSION"

            metrics = {
                "scenario": scenario,
                "index_implied_vol_pct": round(index_vol * 100, 1),
                "component_implied_vol_pct": round(component_vol * 100, 1),
                "index_realized_vol_pct": round(rv * 100, 1),
                "priced_implied_correlation": round(implied_corr, 4),
                "realized_correlation": round(realized_corr, 4),
                "variance_dispersion_spread": round(dispersion_edge, 4),
                "long_dispersion_variance_pnl": round(dispersion_pnl, 4),
                "strategy_edge_status": status,
            }

            summary = (
                f"Dispersion trading simulation: realized correlation {realized_corr:.3f} vs implied {implied_corr:.3f}. "
                f"Long component variance minus short index variance PnL: {dispersion_pnl:+.4f} ({status})."
            )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={
                "call_greeks": self.round_greeks(call_greeks),
                "put_greeks": self.round_greeks(put_greeks),
                "net_straddle_greeks": {
                    "delta": round(net_greeks["delta"], 4),
                    "gamma": round(net_greeks["gamma"], 5),
                    "vega_1pct": round(net_greeks["vega"], 4),
                    "theta_daily": round(net_greeks["theta_daily"], 4),
                },
            },
            summary=summary,
        )


# Self-register into the lab
register(OptionsDeskEngine())
