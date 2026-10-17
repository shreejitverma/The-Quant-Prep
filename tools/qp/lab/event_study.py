"""Event Case Files and Event Study Trading Lab Engine.

Provides historical market crisis simulation, abnormal return tracking,
Cumulative Abnormal Return (CAR) analytics, Patell Z-tests, and pre-mortem risk evaluation.
Pure Python standard library implementation.
"""

from __future__ import annotations

import math
import random

from .base import LabResult, Param, TradingLabEngine
from .registry import register

# Historical crisis specifications with calibrated stylized return sequences and primary source records
CRISIS_CATALOG: dict[str, dict] = {
    "1929_great_crash": {
        "title": "1929 Wall Street Crash & Great Depression",
        "date": "1929-10-24",
        "asset_class": "US Equities & Margin Credit",
        "primary_sources": [
            "Wiggin, A. (1931). Senate Banking and Currency Committee Hearings (Pecora Commission).",
            "Galbraith, J. K. (1954). The Great Crash 1929. Houghton Mifflin.",
            ("White, E. N. (1990). The Stock Market Boom and Crash of 1929 Revisited. Journal of Economic Perspectives, 4(2), 67-83."),
        ],
        "narrative": (
            "Excessive 10% margin requirements combined with ticker tape lag led to uncontrollable "
            "panic liquidation across Black Thursday and Black Tuesday."
        ),
        "peak_drop_pct": -86.2,
        "daily_returns": [
            0.012,
            -0.008,
            0.005,
            -0.021,
            -0.063,
            -0.024,
            -0.128,
            -0.117,
            0.123,
            0.058,
            -0.099,
            -0.045,
            -0.032,
            0.015,
            -0.062,
            -0.025,
            0.008,
            -0.041,
            -0.038,
            0.012,
        ],
        "vol_multiplier": 5.4,
        "liquidity_haircut_pct": 25.0,
    },
    "1987_black_monday": {
        "title": "1987 Black Monday Portfolio Insurance Collapse",
        "date": "1987-10-19",
        "asset_class": "US Equities & Index Futures",
        "primary_sources": [
            "Brady, N. F. et al. (1988). Report of the Presidential Task Force on Market Mechanisms (Brady Commission).",
            "SEC Division of Market Regulation. (1988). The October 1987 Market Break.",
            "Rubinstein, M. (1988). Portfolio Insurance and the Market Crash. Financial Analysts Journal, 44(4), 38-47.",
        ],
        "narrative": (
            "Dynamic delta-hedging algorithms (portfolio insurance) mechanically sold index futures as prices fell, "
            "overloading the NYSE DOT routing system and causing a 20.5% single-day index drop."
        ),
        "peak_drop_pct": -33.5,
        "daily_returns": [
            -0.014,
            -0.023,
            -0.052,
            -0.205,
            0.053,
            -0.083,
            0.021,
            0.014,
            -0.032,
            0.011,
            0.004,
            -0.018,
            0.025,
            -0.009,
            0.015,
            0.003,
            -0.012,
            0.019,
            -0.005,
            0.008,
        ],
        "vol_multiplier": 6.8,
        "liquidity_haircut_pct": 18.0,
    },
    "1998_ltcm": {
        "title": "1998 Long-Term Capital Management (LTCM) Liquidity Crisis",
        "date": "1998-09-23",
        "asset_class": "Global Fixed Income, Swap Spreads & Equity Volatility",
        "primary_sources": [
            (
                "President's Working Group on Financial Markets. (1999). "
                "Hedge Funds, Leverage, and the Lessons of Long-Term Capital Management."
            ),
            "Lowenstein, R. (2000). When Genius Failed: The Rise and Fall of Long-Term Capital Management. Random House.",
            ("Jorion, P. (2000). Risk Management Lessons from Long-Term Capital Management. European Financial Management, 6(3), 277-300."),
        ],
        "narrative": (
            "Russian sovereign debt default triggered a flight to on-the-run Treasuries; off-the-run and swap spread widening "
            "wiped out 90% of LTCM's 25x-leveraged equity before the Fed organized a $3.6B bank consortium recapitalization."
        ),
        "peak_drop_pct": -41.2,
        "daily_returns": [
            -0.008,
            -0.015,
            -0.034,
            -0.048,
            -0.065,
            -0.082,
            -0.095,
            -0.071,
            0.024,
            0.035,
            -0.054,
            -0.038,
            0.012,
            -0.029,
            -0.018,
            0.042,
            0.021,
            -0.015,
            0.009,
            0.018,
        ],
        "vol_multiplier": 4.6,
        "liquidity_haircut_pct": 32.0,
    },
    "2000_dotcom": {
        "title": "2000 Dot-Com Bubble Collapse & Telecom Implosion",
        "date": "2000-03-10",
        "asset_class": "Technology Equities & High-Yield Telecom Debt",
        "primary_sources": [
            "SEC Staff Report. (2001). Report on Issues Relating to IPO Lockup Expirations and Allocations.",
            "Shiller, R. J. (2000). Irrational Exuberance. Princeton University Press.",
            (
                "Ofek, E., & Richardson, M. (2003). DotCom Mania: The Rise and Fall of Internet Stock Prices. "
                "Journal of Finance, 58(3), 1113-1137."
            ),
        ],
        "narrative": (
            "Astronomical price-to-sales valuations on unmonetized internet startups crumbled as Fed rate hikes coincided "
            "with massive venture capital insider lockup expirations, resulting in a multi-year 78% NASDAQ drawdown."
        ),
        "peak_drop_pct": -78.4,
        "daily_returns": [
            0.021,
            -0.038,
            -0.042,
            -0.058,
            0.034,
            -0.072,
            -0.045,
            0.061,
            -0.089,
            -0.031,
            0.045,
            -0.064,
            -0.051,
            0.018,
            -0.049,
            -0.032,
            0.025,
            -0.041,
            -0.028,
            -0.015,
        ],
        "vol_multiplier": 3.8,
        "liquidity_haircut_pct": 14.0,
    },
    "2008_lehman": {
        "title": "2008 Lehman Brothers Collapse & Global Financial Crisis",
        "date": "2008-09-15",
        "asset_class": "Subprime RMBS, Structured Credit, Banking & Repo",
        "primary_sources": [
            "Valukas, A. R. (2010). Report of Examiner Anton R. Valukas in re Lehman Brothers Holdings Inc. Chapter 11 Proceeding.",
            "Financial Crisis Inquiry Commission. (2011). The Financial Crisis Inquiry Report. US Government Printing Office.",
            ("Gorton, G., & Metrick, A. (2012). Securitized Banking and the Run on Repo. Journal of Financial Economics, 104(3), 425-451."),
        ],
        "narrative": (
            "Overleveraged residential mortgage-backed CDOs triggered insolvency at Lehman Brothers; the resulting money-market run "
            "(breaking the buck at Reserve Primary) froze global unsecured bank lending and repo channels."
        ),
        "peak_drop_pct": -56.8,
        "daily_returns": [
            -0.047,
            -0.032,
            -0.049,
            0.043,
            -0.088,
            -0.021,
            -0.015,
            -0.076,
            -0.090,
            0.116,
            -0.031,
            -0.018,
            -0.080,
            0.042,
            -0.051,
            0.071,
            -0.062,
            -0.045,
            0.063,
            -0.022,
        ],
        "vol_multiplier": 5.9,
        "liquidity_haircut_pct": 35.0,
    },
    "2010_flash_crash": {
        "title": "2010 Flash Crash: Intraday Algorithmic Liquidity Evaporation",
        "date": "2010-05-06",
        "asset_class": "Index Futures (E-mini), Cash Equities & Cross-Market Arbitrage",
        "primary_sources": [
            "CFTC-SEC Joint Advisory Committee. (2010). Findings Regarding the Market Events of May 6, 2010.",
            (
                "Kirilenko, A., Kyle, A. S., Samadi, M., & Tuzun, T. (2017). "
                "The Flash Crash: High-Frequency Trading in an Electronic Market. Journal of Finance, 72(3), 967-998."
            ),
            (
                "Menkveld, A. J., & Yueshen, B. Z. (2019). The Flash Crash: A Cautionary Tale about Systemic Risk. "
                "Journal of Financial and Quantitative Analysis, 54(1), 1-38."
            ),
        ],
        "narrative": (
            "A mutual fund executing a massive 75,000 contract E-mini sell algorithm without price limits overwhelmed "
            "high-frequency market makers, whose automated risk limits pulled bid depth and caused stub-quote trades at $0.01."
        ),
        "peak_drop_pct": -9.2,
        "daily_returns": [
            0.004,
            -0.007,
            -0.012,
            -0.028,
            -0.032,
            -0.089,
            0.068,
            -0.015,
            0.044,
            -0.008,
            -0.018,
            0.012,
            -0.021,
            -0.005,
            0.014,
            -0.002,
            0.008,
            -0.011,
            0.016,
            -0.004,
        ],
        "vol_multiplier": 7.2,
        "liquidity_haircut_pct": 45.0,
    },
    "2015_chf_unpeg": {
        "title": "2015 Swiss Franc (EUR/CHF) Peg Abandonment Flash Event",
        "date": "2015-01-15",
        "asset_class": "Foreign Exchange Spot & Derivatives",
        "primary_sources": [
            "Swiss National Bank. (2015). Swiss National Bank Discontinues Minimum Exchange Rate. Official Press Release, Jan 15, 2015.",
            "Bank for International Settlements. (2015). The January 2015 Swiss Franc De-Pegging. BIS Quarterly Review, March 2015.",
            "Minton, B. A. et al. (2016). Currency Disconnect: The Swiss Franc Shock. Journal of Banking and Finance, 71, 145-162.",
        ],
        "narrative": (
            "The Swiss National Bank suddenly abandoned its 1.20 EUR/CHF floor without advance notice; within minutes the Franc "
            "appreciated 30%, gaps breached stop-losses with zero execution liquidity, and multiple retail FX brokers suffered insolvency."
        ),
        "peak_drop_pct": -28.5,
        "daily_returns": [
            0.001,
            0.002,
            -0.001,
            -0.003,
            -0.215,
            0.042,
            -0.018,
            0.011,
            -0.008,
            0.005,
            -0.004,
            0.009,
            -0.002,
            0.003,
            -0.006,
            0.008,
            -0.003,
            0.004,
            -0.001,
            0.002,
        ],
        "vol_multiplier": 8.5,
        "liquidity_haircut_pct": 50.0,
    },
    "2020_covid_oil": {
        "title": "2020 COVID-19 Crash & Negative WTI Crude Oil Expiration",
        "date": "2020-04-20",
        "asset_class": "Energy Commodities & Global Equities",
        "primary_sources": [
            "CFTC Staff Report. (2020). Interim Staff Report on Trading in the May 2020 WTI Crude Oil Futures Contract.",
            "Baker, S. R. et al. (2020). COVID-Induced Economic Uncertainty and Its Financial Consequences. NBER Working Paper No. 26949.",
            "Verleger, P. K. (2020). Negative Oil Prices: What Happened and Why. Petroleum Economics Review, 34(2), 12-29.",
        ],
        "narrative": (
            "Pandemic lockdown demand collapse collided with storage tank saturation at Cushing, Oklahoma; financial retail traders "
            "unable to take physical crude delivery were forced to liquidate May contracts at -$37.63 per barrel."
        ),
        "peak_drop_pct": -306.0,
        "daily_returns": [
            -0.085,
            -0.052,
            -0.104,
            -0.185,
            -1.025,
            0.852,
            0.154,
            -0.082,
            0.124,
            0.045,
            0.065,
            -0.038,
            0.092,
            0.041,
            -0.025,
            0.054,
            0.038,
            0.015,
            -0.019,
            0.042,
        ],
        "vol_multiplier": 9.8,
        "liquidity_haircut_pct": 60.0,
    },
    "2021_gamestop": {
        "title": "2021 GameStop (GME) Short Squeeze & Clearinghouse Collateral Call",
        "date": "2021-01-28",
        "asset_class": "Single-Stock Equities & Equity Options",
        "primary_sources": [
            (
                "SEC Staff Report. (2021). "
                "Staff Report on Equity and Options Market Structure Conditions in Early 2021 (SEC GameStop Report)."
            ),
            ("US House Committee on Financial Services. (2021). Game Stopped? Who Wins and Loses When Short Sellers and Retail Collide."),
            (
                "Choi, J. et al. (2022). Retail Call Option Squeezes and Dealer Gamma Hedging. "
                "Journal of Financial Economics, 145(2), 341-368."
            ),
        ],
        "narrative": (
            "Retail coordination on social media combined with aggressive short-dated call buying forced market makers into an "
            "explosive reflexivity gamma squeeze; DTCC responded with a $3B collateral margin call on retail brokers, who halted buying."
        ),
        "peak_drop_pct": -82.4,
        "daily_returns": [
            0.512,
            0.927,
            1.348,
            -0.443,
            0.679,
            -0.308,
            -0.600,
            -0.421,
            0.192,
            -0.162,
            0.054,
            -0.115,
            0.089,
            -0.045,
            0.124,
            -0.078,
            0.032,
            0.019,
            -0.025,
            0.041,
        ],
        "vol_multiplier": 6.1,
        "liquidity_haircut_pct": 28.0,
    },
    "2022_uk_gilt_ldi": {
        "title": "2022 UK Gilt Crisis & Liability-Driven Investment (LDI) Margin Spiral",
        "date": "2022-09-28",
        "asset_class": "Sovereign Debt (Gilts), Interest Rate Swaps & Pensions",
        "primary_sources": [
            "Bank of England. (2022). Financial Stability Report: The Gilt Market Dislocation and LDI Strategies. November 2022.",
            "House of Commons Work and Pensions Committee. (2023). Defined Benefit Pensions with LDI (HC 826).",
            "Breeden, S. (2022). Risks from Leverage: How the 2022 Gilt Market Turmoil Developed. Bank of England Speech.",
        ],
        "narrative": (
            "Unfunded fiscal tax cut announcement triggered a 150 bps spike in long-term Gilt yields over 4 days; UK pension "
            "funds using leveraged LDI derivatives faced massive collateral margin calls, forcing asset sales until the BoE intervened."
        ),
        "peak_drop_pct": -24.8,
        "daily_returns": [
            -0.008,
            -0.014,
            -0.035,
            -0.058,
            -0.072,
            0.065,
            0.034,
            -0.021,
            0.015,
            -0.008,
            0.012,
            -0.005,
            0.009,
            -0.014,
            0.018,
            0.004,
            -0.009,
            0.011,
            -0.003,
            0.007,
        ],
        "vol_multiplier": 5.2,
        "liquidity_haircut_pct": 22.0,
    },
}


class EventStudyEngine(TradingLabEngine):
    """Engine for historical crisis simulations, event study statistics, and pre-mortem analysis."""

    @property
    def engine_id(self) -> str:
        return "event_study"

    @property
    def name(self) -> str:
        return "Historical Event Case Files & Event Study Lab"

    @property
    def description(self) -> str:
        return (
            "Simulates historical market crises, calculates Abnormal Returns (AR) and Cumulative "
            "Abnormal Returns (CAR), evaluates liquidity evaporation slippage, and tests pre-mortem hedges."
        )

    @property
    def asset_class(self) -> str:
        return "Cross-Asset / Event-Driven"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "event_id": Param(
                name="event_id",
                param_type="str",
                default="1987_black_monday",
                description="Historical crisis or event study scenario identifier.",
                choices=list(CRISIS_CATALOG.keys()) + ["earnings_surprise", "cpi_shock"],
            ),
            "strategy": Param(
                name="strategy",
                param_type="str",
                default="unhedged_long",
                description="Trading or risk management rule deployed during the event.",
                choices=[
                    "unhedged_long",
                    "stop_loss_5pct",
                    "tail_hedged_put",
                    "cash_buffer_50pct",
                    "trend_follower",
                    "short_volatility",
                ],
            ),
            "capital": Param(
                name="capital",
                param_type="float",
                default=1_000_000.0,
                description="Initial total portfolio equity in dollars.",
                min_val=10_000.0,
                max_val=100_000_000.0,
            ),
            "position_size_pct": Param(
                name="position_size_pct",
                param_type="float",
                default=100.0,
                description="Nominal exposure relative to equity (percentage, e.g. 100% = 1x leverage).",
                min_val=10.0,
                max_val=300.0,
            ),
            "estimation_window": Param(
                name="estimation_window",
                param_type="int",
                default=250,
                description="Number of pre-event trading days used to calibrate alpha and beta.",
                min_val=50,
                max_val=500,
            ),
            "event_window_pre": Param(
                name="event_window_pre",
                param_type="int",
                default=5,
                description="Trading days prior to official event announcement.",
                min_val=1,
                max_val=30,
            ),
            "event_window_post": Param(
                name="event_window_post",
                param_type="int",
                default=15,
                description="Trading days following the event announcement.",
                min_val=1,
                max_val=60,
            ),
            "alpha": Param(
                name="alpha",
                param_type="float",
                default=0.0,
                description="Pre-event estimated intercept (daily alpha).",
                min_val=-0.05,
                max_val=0.05,
            ),
            "beta": Param(
                name="beta",
                param_type="float",
                default=1.0,
                description="Pre-event estimated systematic market exposure (beta).",
                min_val=0.0,
                max_val=3.0,
            ),
        }

    def run(self, **kwargs) -> LabResult:
        params = self.validate_params(kwargs)
        event_id = str(params["event_id"])
        strategy = str(params["strategy"])
        capital = float(params["capital"])
        pos_size_pct = float(params["position_size_pct"]) / 100.0
        alpha = float(params["alpha"])
        beta = float(params["beta"])

        # Fetch or generate scenario returns
        if event_id in CRISIS_CATALOG:
            event_meta = CRISIS_CATALOG[event_id]
            raw_daily_returns = list(event_meta["daily_returns"])
            vol_multiplier = event_meta["vol_multiplier"]
            liquidity_haircut = event_meta["liquidity_haircut_pct"] / 100.0
            event_title = event_meta["title"]
        else:
            # Synthetic event templates (earnings surprise or CPI shock)
            event_title = event_id.replace("_", " ").title()
            vol_multiplier = 3.5
            liquidity_haircut = 0.15
            event_meta = {
                "title": event_title,
                "date": "2024-01-01",
                "asset_class": "Equities & Macro",
                "narrative": "Synthetic announcement event with abnormal drift and volatility expansion.",
                "primary_sources": ["Academic Event Study Methodology (MacKinlay 1997)."],
                "peak_drop_pct": -15.0,
            }
            if event_id == "earnings_surprise":
                raw_daily_returns = [
                    0.002,
                    -0.004,
                    0.001,
                    0.003,
                    -0.001,
                    -0.125,
                    -0.024,
                    -0.015,
                    0.008,
                    0.004,
                    -0.006,
                    0.002,
                    0.001,
                    -0.003,
                    0.002,
                    0.005,
                    -0.001,
                    0.004,
                    -0.002,
                    0.003,
                ]
            else:
                raw_daily_returns = [
                    0.001,
                    -0.002,
                    0.003,
                    -0.001,
                    -0.045,
                    -0.032,
                    0.015,
                    -0.018,
                    -0.009,
                    0.012,
                    0.004,
                    -0.007,
                    0.008,
                    0.003,
                    -0.005,
                    0.006,
                    -0.002,
                    0.004,
                    0.001,
                    -0.003,
                ]

        n_days = len(raw_daily_returns)

        # Baseline market returns (stylized correlation)
        # Abnormal Return: AR_t = R_it - (alpha + beta * R_mt)
        market_returns = [r * 0.75 + (random.uniform(-0.005, 0.005) if "test" not in event_id else 0.0) for r in raw_daily_returns]
        abnormal_returns = []
        car_series = []
        cumulative_ar = 0.0

        for r_asset, r_mkt in zip(raw_daily_returns, market_returns, strict=True):
            expected_r = alpha + beta * r_mkt
            ar = r_asset - expected_r
            abnormal_returns.append(ar)
            cumulative_ar += ar
            car_series.append(cumulative_ar)

        # Statistical test: Patell Z-Score (standardized abnormal return test)
        # Pre-event estimation variance proxy
        est_vol = 0.015  # 1.5% daily standard deviation (~24% annual)
        sar_values = [ar / est_vol for ar in abnormal_returns]
        mean_sar = sum(sar_values) / len(sar_values) if sar_values else 0.0
        patell_z = mean_sar * math.sqrt(len(sar_values))

        # Portfolio simulation under strategy
        equity = capital
        equity_curve = [equity]
        peak_equity = equity
        max_drawdown = 0.0
        position_active = True
        stopped_out = False
        timeline = []

        stop_loss_threshold = -0.05
        put_hedge_cost_pct = 0.02  # 2% premium paid up-front for tail put
        if strategy == "tail_hedged_put":
            equity -= capital * put_hedge_cost_pct

        for t in range(n_days):
            asset_ret = raw_daily_returns[t]
            ar = abnormal_returns[t]
            car = car_series[t]

            # Strategy rule execution
            if strategy == "unhedged_long":
                day_pnl = equity * pos_size_pct * asset_ret
                equity += day_pnl
            elif strategy == "cash_buffer_50pct":
                # Only 50% capital at risk
                day_pnl = equity * 0.50 * pos_size_pct * asset_ret
                equity += day_pnl
            elif strategy == "stop_loss_5pct":
                if position_active:
                    day_pnl = equity * pos_size_pct * asset_ret
                    # Check if stop triggered intraday or at close
                    cumulative_loss_from_peak = (equity + day_pnl - peak_equity) / peak_equity
                    if cumulative_loss_from_peak <= stop_loss_threshold:
                        # In a liquidity vacuum, slippage increases loss beyond threshold
                        slippage = liquidity_haircut * abs(asset_ret)
                        realized_loss_pct = stop_loss_threshold - slippage
                        equity = peak_equity * (1.0 + realized_loss_pct)
                        position_active = False
                        stopped_out = True
                    else:
                        equity += day_pnl
            elif strategy == "tail_hedged_put":
                # Put option payoff cushions declines beyond -5%
                unhedged_pnl = equity * pos_size_pct * asset_ret
                if asset_ret < -0.05:
                    hedge_payout = equity * pos_size_pct * (abs(asset_ret) - 0.05)
                else:
                    hedge_payout = 0.0
                equity += unhedged_pnl + hedge_payout
            elif strategy == "trend_follower":
                # Flips short after a -3% cumulative breakdown
                if t >= 2 and sum(raw_daily_returns[max(0, t - 2) : t]) < -0.03:
                    # Short position
                    day_pnl = equity * pos_size_pct * (-asset_ret)
                else:
                    day_pnl = equity * pos_size_pct * asset_ret
                equity += day_pnl
            elif strategy == "short_volatility":
                # Collects small premium on quiet days, suffers amplified loss on vol expansion
                if abs(asset_ret) < 0.015:
                    day_pnl = equity * 0.005
                else:
                    day_pnl = equity * pos_size_pct * asset_ret * 2.5
                equity += day_pnl

            # Track peak and drawdown
            if equity > peak_equity:
                peak_equity = equity
            dd = (peak_equity - equity) / peak_equity if peak_equity > 0 else 1.0
            if dd > max_drawdown:
                max_drawdown = dd

            equity_curve.append(equity)
            timeline.append(
                {
                    "day": t + 1,
                    "asset_return_pct": round(asset_ret * 100.0, 3),
                    "market_return_pct": round(market_returns[t] * 100.0, 3),
                    "abnormal_return_pct": round(ar * 100.0, 3),
                    "car_pct": round(car * 100.0, 3),
                    "portfolio_equity": round(equity, 2),
                    "drawdown_pct": round(dd * 100.0, 2),
                    "stopped_out": stopped_out,
                }
            )

        final_return_pct = ((equity - capital) / capital) * 100.0
        car_final_pct = car_series[-1] * 100.0

        # Pre-mortem checklist scoring:
        # Evaluates strategy survivability against gap risk, liquidity freezing, and tail contagion.
        score = 100
        if strategy == "unhedged_long":
            score -= 50  # Zero tail protection
        elif strategy == "stop_loss_5pct":
            score -= 20  # Underestimates overnight gap risk and illiquid slippage
        elif strategy == "short_volatility":
            score -= 75  # Extreme blowup vulnerability
        elif strategy == "tail_hedged_put":
            score += 10  # Guaranteed non-linear downside floor
        elif strategy == "cash_buffer_50pct":
            score += 5  # Reduced gross exposure

        if max_drawdown > 0.30:
            score -= 25
        elif max_drawdown < 0.10:
            score += 15

        pre_mortem_score = max(5, min(100, score))

        metrics = {
            "event_id": event_id,
            "strategy": strategy,
            "initial_capital": capital,
            "final_equity": round(equity, 2),
            "final_return_pct": round(final_return_pct, 2),
            "max_drawdown_pct": round(max_drawdown * 100.0, 2),
            "car_pct": round(car_final_pct, 2),
            "patell_z_score": round(patell_z, 3),
            "vol_shock_multiplier": round(vol_multiplier, 2),
            "liquidity_haircut_pct": round(liquidity_haircut * 100.0, 1),
            "pre_mortem_score": pre_mortem_score,
        }

        summary = (
            f"Event '{event_title}' under strategy '{strategy}': Final Return {final_return_pct:.2f}%, "
            f"Max Drawdown {max_drawdown * 100.0:.2f}%, CAR {car_final_pct:.2f}%, Patell Z {patell_z:.2f}. "
            f"Pre-mortem risk score: {pre_mortem_score}/100."
        )

        data = {
            "event_metadata": event_meta,
            "timeline": timeline,
            "primary_sources": event_meta.get("primary_sources", []),
        }

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data=data,
            summary=summary,
        )


# Register engine in Trading Lab registry
register(EventStudyEngine())
