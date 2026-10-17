"""Multi-Asset Portfolio Allocator & Risk Parity Trading Lab Engine.

Models asset allocation strategies (60/40, Equal Weight, Risk Parity,
Bridgewater All Weather, Minimum Variance), Euler risk contributions,
macro regime stress scenarios, and multi-period path simulation.
Pure Python standard library implementation.
"""

from __future__ import annotations

import math
import random

from .base import LabResult, Param, TradingLabEngine
from .registry import register


class PortfolioAllocatorEngine(TradingLabEngine):
    """Engine for multi-asset allocation, risk parity decomposition, and regime simulation."""

    @property
    def engine_id(self) -> str:
        return "port_alloc"

    @property
    def name(self) -> str:
        return "Multi-Asset Portfolio Allocator & Risk Parity Lab"

    @property
    def description(self) -> str:
        return "Dynamic multi-asset allocation, Euler risk contributions, All Weather regime stress, and backtesting."

    @property
    def asset_class(self) -> str:
        return "Portfolio & Multi-Asset"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "strategy": Param(
                name="strategy",
                param_type="str",
                default="risk_parity",
                description="Asset allocation policy.",
                choices=["60_40", "equal_weight", "risk_parity", "all_weather", "min_variance"],
            ),
            "leverage": Param(
                name="leverage",
                param_type="float",
                default=1.0,
                description="Total gross portfolio leverage multiplier (e.g. 1.0 = unlevered, 1.5 = 150% gross).",
                min_val=0.5,
                max_val=3.0,
            ),
            "macro_scenario": Param(
                name="macro_scenario",
                param_type="str",
                default="baseline",
                description="Macroeconomic environment for the multi-year simulation.",
                choices=["baseline", "growth_boom", "stagflation", "liquidity_crisis", "recession"],
            ),
            "rebalance_freq": Param(
                name="rebalance_freq",
                param_type="str",
                default="monthly",
                description="Periodic rebalancing frequency.",
                choices=["monthly", "quarterly", "annual"],
            ),
            "vol_target": Param(
                name="vol_target",
                param_type="float",
                default=0.10,
                description="Annualized target portfolio volatility (e.g. 0.10 for 10%, 0 to disable).",
                min_val=0.0,
                max_val=0.30,
            ),
            "n_years": Param(
                name="n_years",
                param_type="int",
                default=5,
                description="Simulation time horizon in years.",
                min_val=1,
                max_val=20,
            ),
            "seed": Param(
                name="seed",
                param_type="int",
                default=42,
                description="Random number generator seed for Monte Carlo path generation.",
            ),
        }

    def run(self, **kwargs) -> LabResult:
        p = self.validate_params(kwargs)
        rng = random.Random(p["seed"])

        strategy = str(p["strategy"])
        leverage = float(p["leverage"])
        scenario = str(p["macro_scenario"])
        rebalance_freq = str(p["rebalance_freq"])
        vol_target = float(p["vol_target"])
        n_years = int(p["n_years"])

        # Asset universe: 7 fundamental building blocks
        assets = [
            "SPY (US Equities)",
            "TLT (Long Treasuries)",
            "IEF (Interm Treasuries)",
            "TIP (TIPS)",
            "DBC (Commodities)",
            "GLD (Gold)",
            "SHV (Cash)",
        ]
        n_assets = len(assets)

        # Baseline expected returns and annualized volatilities
        base_drifts = [0.095, 0.045, 0.035, 0.038, 0.050, 0.060, 0.030]
        base_vols = [0.160, 0.110, 0.060, 0.065, 0.180, 0.150, 0.008]

        # Baseline pairwise correlation matrix
        # Columns: SPY, TLT, IEF, TIP, DBC, GLD, SHV
        base_corr = [
            [1.00, -0.30, -0.25, 0.10, 0.35, 0.05, 0.00],  # SPY
            [-0.30, 1.00, 0.85, 0.60, -0.20, 0.25, 0.00],  # TLT
            [-0.25, 0.85, 1.00, 0.70, -0.15, 0.20, 0.00],  # IEF
            [0.10, 0.60, 0.70, 1.00, 0.30, 0.35, 0.00],  # TIP
            [0.35, -0.20, -0.15, 0.30, 1.00, 0.30, 0.00],  # DBC
            [0.05, 0.25, 0.20, 0.35, 0.30, 1.00, 0.00],  # GLD
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],  # SHV
        ]

        # Adjust parameters according to macro scenario
        drifts = list(base_drifts)
        vols = list(base_vols)
        corr = [row[:] for row in base_corr]

        if scenario == "growth_boom":
            drifts[0] = 0.18  # Equities surge
            drifts[4] = 0.09  # Commodities gain
            drifts[1] = 0.01  # Long bonds lag
        elif scenario == "stagflation":
            drifts[0] = -0.06  # Equities drop
            drifts[1] = -0.10  # Nominal long bonds crushed
            drifts[2] = -0.04  # Intermediate bonds suffer
            drifts[3] = 0.08  # TIPS outperform
            drifts[4] = 0.20  # Commodities surge
            drifts[5] = 0.14  # Gold rallies
            vols[1] = 0.16  # Bond vol spikes
            # Stock-bond correlation becomes positive!
            corr[0][1] = 0.45
            corr[1][0] = 0.45
            corr[0][2] = 0.40
            corr[2][0] = 0.40
        elif scenario == "liquidity_crisis":
            drifts[0] = -0.25  # Equities collapse
            drifts[4] = -0.22  # Commodities plunge
            drifts[1] = 0.02  # Initial flight to safety
            drifts[6] = 0.04  # Cash rate
            # Extreme volatility spike
            for i in range(len(vols)):
                if i != 6:
                    vols[i] *= 1.8
            # Correlation breakdown: all risky assets correlate towards 1.0
            for i in range(len(corr) - 1):
                for j in range(len(corr) - 1):
                    if i != j:
                        corr[i][j] = 0.75
        elif scenario == "recession":
            drifts[0] = -0.15  # Equities bear market
            drifts[1] = 0.15  # Flight to long bonds
            drifts[2] = 0.08  # Intermediate bonds rally
            drifts[4] = -0.12  # Commodities fall
            corr[0][1] = -0.60  # Strong flight to safety hedge
            corr[1][0] = -0.60

        # Construct covariance matrix Sigma: Sigma_ij = rho_ij * vol_i * vol_j
        cov = [[corr[i][j] * vols[i] * vols[j] for j in range(n_assets)] for i in range(n_assets)]

        # Determine target base weights according to strategy
        raw_weights = [0.0] * n_assets

        if strategy == "60_40":
            # 60% SPY, 40% IEF
            raw_weights[0] = 0.60
            raw_weights[2] = 0.40
        elif strategy == "equal_weight":
            # 1/7 across all assets
            raw_weights = [1.0 / n_assets] * n_assets
        elif strategy == "risk_parity":
            # Equal risk contribution approximation: weight inversely proportional to volatility
            inv_vols = [1.0 / v for v in vols]
            total_inv = sum(inv_vols)
            raw_weights = [iv / total_inv for iv in inv_vols]
        elif strategy == "all_weather":
            # Bridgewater template:
            # 30% Equities (SPY), 40% Long Bonds (TLT), 15% Interm Bonds (IEF), 7.5% Commodities (DBC), 7.5% Gold (GLD)
            raw_weights[0] = 0.30
            raw_weights[1] = 0.40
            raw_weights[2] = 0.15
            raw_weights[4] = 0.075
            raw_weights[5] = 0.075
        elif strategy == "min_variance":
            # Simple analytical inverse-variance heuristic
            inv_var = [1.0 / (v * v) for v in vols]
            total_inv_var = sum(inv_var)
            raw_weights = [iv / total_inv_var for iv in inv_var]

        # Calculate portfolio volatility before scaling
        def calc_port_vol(w_vec: list[float]) -> float:
            var = 0.0
            for i in range(n_assets):
                for j in range(n_assets):
                    var += w_vec[i] * w_vec[j] * cov[i][j]
            return math.sqrt(max(0.0, var))

        unscaled_vol = calc_port_vol(raw_weights)

        # Scale weights if volatility targeting is enabled
        effective_scale = leverage
        if vol_target > 0.001 and unscaled_vol > 0.0001:
            target_scale = vol_target / unscaled_vol
            # Blend nominal leverage with target volatility
            effective_scale = min(leverage * 2.0, max(0.5, target_scale))

        final_weights = [w * effective_scale for w in raw_weights]
        port_vol = calc_port_vol(final_weights)

        # Compute Euler Marginal Contribution to Risk (MCR) and Total Risk Contribution (TRC)
        mcr = [0.0] * n_assets
        trc = [0.0] * n_assets
        trc_pct = [0.0] * n_assets

        if port_vol > 0.0001:
            for i in range(n_assets):
                # (Sigma * w)_i
                cov_w_i = sum(cov[i][j] * final_weights[j] for j in range(n_assets))
                mcr[i] = cov_w_i / port_vol
                trc[i] = final_weights[i] * mcr[i]
                trc_pct[i] = (trc[i] / port_vol) * 100.0

        # Multi-period Monte Carlo Simulation (Monthly periods)
        n_months = n_years * 12
        monthly_rebalance_interval = 1 if rebalance_freq == "monthly" else (3 if rebalance_freq == "quarterly" else 12)

        monthly_drifts = [d / 12.0 for d in drifts]
        monthly_vols = [v / math.sqrt(12.0) for v in vols]

        # Cholesky decomposition of correlation matrix for correlated Gaussian shocks
        L = [[0.0] * n_assets for _ in range(n_assets)]
        for i in range(n_assets):
            for j in range(i + 1):
                s = sum(L[i][k] * L[j][k] for k in range(j))
                if i == j:
                    val = corr[i][i] - s
                    L[i][j] = math.sqrt(max(1e-6, val))
                else:
                    L[i][j] = (corr[i][j] - s) / L[j][j]

        # Run simulation
        start_capital = 100000.0
        capital = start_capital
        equity_curve = [capital]
        monthly_returns = []

        # Current holdings value per asset
        holdings = [capital * w for w in final_weights]
        cash_balance = capital * (1.0 - sum(final_weights))

        # Financing cost on leverage (borrowing cash at SHV rate + 50 bps spread)
        borrow_rate = (drifts[6] + 0.005) / 12.0

        total_turnover = 0.0

        for m in range(1, n_months + 1):
            # Generate correlated standard normal shocks
            z_uncorr = [rng.gauss(0.0, 1.0) for _ in range(n_assets)]
            z_corr = [sum(L[i][k] * z_uncorr[k] for k in range(i + 1)) for i in range(n_assets)]

            # Asset returns this month
            asset_rets = [
                math.exp((monthly_drifts[i] - 0.5 * monthly_vols[i] ** 2) + monthly_vols[i] * z_corr[i]) - 1.0 for i in range(n_assets)
            ]

            # Update holdings value
            new_holdings_sum = 0.0
            for i in range(n_assets):
                holdings[i] *= 1.0 + asset_rets[i]
                new_holdings_sum += holdings[i]

            # Update cash balance with interest or borrow cost
            if cash_balance >= 0:
                cash_balance *= 1.0 + (monthly_drifts[6])
            else:
                cash_balance -= abs(cash_balance) * borrow_rate

            total_val = new_holdings_sum + cash_balance
            month_ret = (total_val - capital) / capital if capital > 0 else 0.0
            monthly_returns.append(month_ret)
            capital = total_val
            equity_curve.append(round(capital, 2))

            # Periodic rebalancing
            if m % monthly_rebalance_interval == 0:
                target_holdings = [capital * w for w in final_weights]
                turnover_this_month = sum(abs(target_holdings[i] - holdings[i]) for i in range(n_assets))
                total_turnover += turnover_this_month
                holdings = target_holdings
                cash_balance = capital * (1.0 - sum(final_weights))

        # Calculate performance metrics
        perf = self.calculate_returns_metrics(equity_curve, risk_free_rate=drifts[6], periods_per_year=12)

        # Asset summary breakdown table
        asset_breakdown = []
        for i in range(n_assets):
            asset_breakdown.append(
                {
                    "asset": assets[i],
                    "weight_pct": round(final_weights[i] * 100.0, 2),
                    "expected_return_pct": round(drifts[i] * 100.0, 2),
                    "volatility_pct": round(vols[i] * 100.0, 2),
                    "mcr": round(mcr[i], 4),
                    "trc_pct": round(trc_pct[i], 2),
                }
            )

        avg_annual_turnover = (total_turnover / (start_capital * n_years)) * 100.0

        equity_risk = trc_pct[0]
        bond_risk = trc_pct[1] + trc_pct[2] + trc_pct[3]

        metrics: dict[str, float | int | str] = {
            "strategy": strategy,
            "scenario": scenario,
            "leverage": round(effective_scale, 2),
            "cagr_pct": round(perf["cagr"] * 100.0, 2),
            "annual_volatility_pct": round(perf.get("annual_volatility", port_vol) * 100.0, 2),
            "sharpe_ratio": round(perf["sharpe"], 2),
            "sortino_ratio": round(perf["sortino"], 2),
            "max_drawdown_pct": round(perf["max_drawdown"] * 100.0, 2),
            "calmar_ratio": round(perf["calmar"], 2),
            "equity_risk_contribution_pct": round(equity_risk, 2),
            "bond_risk_contribution_pct": round(bond_risk, 2),
            "turnover_annual_pct": round(avg_annual_turnover, 2),
        }

        summary = (
            f"Strategy '{strategy}' under '{scenario}' regime: CAGR {perf['cagr'] * 100:.2f}%, "
            f"Sharpe {perf['sharpe']:.2f}, Max Drawdown {perf['max_drawdown'] * 100:.2f}%. "
            f"Equity contributes {equity_risk:.1f}% of total risk, while bonds contribute {bond_risk:.1f}%."
        )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={
                "params": p,
                "asset_breakdown": asset_breakdown,
                "equity_curve": equity_curve,
                "monthly_returns": [round(r, 4) for r in monthly_returns],
            },
            summary=summary,
        )


# Self-register upon import
register(PortfolioAllocatorEngine())
