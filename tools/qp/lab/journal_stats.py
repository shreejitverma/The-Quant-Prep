"""Trade Journal Analytics, MAE/MFE Forensics, and Capital Gate Validator.

Standard-library only implementation of:
1. R-multiple expectancy, win rate, profit factor, payoff ratio, and drawdown analysis.
2. Maximum Adverse Excursion (MAE) and Maximum Favorable Excursion (MFE) stop/target optimization.
3. Setup performance attribution across distinct tactical playbook setups.
4. Rule adherence scoring, moved stop tracking, and revenge trade tilt detection.
5. Institutional 100-trade Capital Gate verification.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .registry import register


@dataclass
class TradeRecord:
    trade_id: str
    setup: str
    entry_price: float
    exit_price: float
    stop_loss: float
    take_profit: float
    shares: int
    r_multiple: float
    pnl: float
    mae_r: float
    mfe_r: float
    adherence: bool
    is_revenge: bool
    moved_stop: bool
    duration_minutes: int


def generate_synthetic_trade_log(
    count: int = 100,
    win_rate: float = 0.45,
    risk_reward: float = 2.2,
    adherence_rate: float = 0.95,
    simulate_tilt: bool = True,
    seed: int = 42,
) -> list[TradeRecord]:
    """Generate realistic sequence of logged trades with MAE/MFE and tilt dynamics."""
    rng = random.Random(seed)
    setups = ["trend_pullback", "breakout_vcp", "failed_auction_reversal", "range_mean_reversion"]
    trades: list[TradeRecord] = []

    consecutive_losses = 0
    base_risk_dollars = 500.0  # 1 R = $500

    for i in range(1, count + 1):
        setup = rng.choice(setups)
        is_adherent = rng.random() < adherence_rate
        is_revenge = False
        moved_stop = False

        # Tilt dynamics after loss streaks
        risk_dollars = base_risk_dollars
        if simulate_tilt and consecutive_losses >= 3 and rng.random() < 0.60:
            is_revenge = True
            is_adherent = False
            risk_dollars = base_risk_dollars * rng.uniform(1.5, 2.5)  # Martingale tilt

        if not is_adherent and rng.random() < 0.35:
            moved_stop = True

        # Determine outcome
        # Unplanned/tilted trades have lower win rates and worse risk/reward
        effective_win_rate = win_rate * 0.60 if is_revenge else win_rate
        is_win = rng.random() < effective_win_rate

        if is_win:
            consecutive_losses = 0
            # Winner: R-multiple centered around risk_reward with variance
            r_mult = rng.uniform(risk_reward * 0.7, risk_reward * 1.4)
            # For winners, MAE is typically small (drawdown while open)
            mae_r = rng.uniform(0.1, 0.75) if not moved_stop else rng.uniform(0.8, 1.8)
            mfe_r = r_mult + rng.uniform(0.1, 0.8)
        else:
            consecutive_losses += 1
            if moved_stop:
                r_mult = -rng.uniform(1.2, 2.8)  # Loss exceeds 1R due to moved stop
                mae_r = abs(r_mult)
                mfe_r = rng.uniform(0.1, 0.4)
            else:
                r_mult = -1.0  # Clean stop out at exactly 1R
                mae_r = 1.0
                mfe_r = rng.uniform(0.05, 0.65)

        pnl = r_mult * risk_dollars
        entry = 100.0
        stop = 98.0
        tp = entry + (entry - stop) * risk_reward
        exit_px = entry + (entry - stop) * r_mult

        shares = int(risk_dollars / (entry - stop))

        trades.append(
            TradeRecord(
                trade_id=f"TRD-{i:03d}",
                setup=setup,
                entry_price=round(entry, 2),
                exit_price=round(exit_px, 2),
                stop_loss=round(stop, 2),
                take_profit=round(tp, 2),
                shares=shares,
                r_multiple=round(r_mult, 2),
                pnl=round(pnl, 2),
                mae_r=round(mae_r, 2),
                mfe_r=round(mfe_r, 2),
                adherence=is_adherent,
                is_revenge=is_revenge,
                moved_stop=moved_stop,
                duration_minutes=rng.randint(15, 360),
            )
        )

    return trades


def _profit_factor(gross_gain: float, gross_loss: float) -> float:
    """Gross gain over gross loss; 0 with no gains, and a 999 cap for a journal with gains and no losses."""
    if gross_gain <= 0:
        return 0.0
    return gross_gain / gross_loss if gross_loss > 0 else 999.0


def _coerce_trade_record(item: TradeRecord | dict[str, Any]) -> TradeRecord:
    if isinstance(item, TradeRecord):
        return item
    return TradeRecord(
        trade_id=str(item.get("trade_id", "")),
        setup=str(item.get("setup", "general")),
        entry_price=float(item.get("entry_price", 0.0)),
        exit_price=float(item.get("exit_price", 0.0)),
        stop_loss=float(item.get("stop_loss", 0.0)),
        take_profit=float(item.get("take_profit", 0.0)),
        shares=int(item.get("shares", 1)),
        r_multiple=float(item["r_multiple"]),
        pnl=float(item["pnl"]),
        mae_r=float(item["mae_r"]),
        mfe_r=float(item["mfe_r"]),
        adherence=bool(item["adherence"]),
        is_revenge=bool(item.get("is_revenge", False)),
        moved_stop=bool(item.get("moved_stop", False)),
        duration_minutes=int(item.get("duration_minutes", 0)),
    )


def analyze_trade_journal(trades: list[TradeRecord | dict[str, Any]]) -> dict[str, Any]:
    """Calculate comprehensive expectancy, MAE/MFE statistics, tilt metrics, and Capital Gate status.

    Drawdown is measured in R so the Capital Gate does not depend on an assumed account size.
    An empty journal returns the zero state with a NO_TRADES_LOGGED gate verdict.
    """
    trades = [_coerce_trade_record(t) for t in trades]
    total_trades = len(trades)

    wins = [t for t in trades if t.r_multiple > 0.0]
    losses = [t for t in trades if t.r_multiple < 0.0]
    breakevens = [t for t in trades if math.isclose(t.r_multiple, 0.0)]

    win_count = len(wins)
    loss_count = len(losses)
    win_rate = win_count / total_trades if total_trades > 0 else 0.0

    # Wins, losses and profit factor are all measured in R, so a trade cannot be a win by one field and a loss by another.
    gross_profit_r = sum(t.r_multiple for t in wins)
    gross_loss_r = abs(sum(t.r_multiple for t in losses))
    net_pnl = sum(t.pnl for t in trades)
    profit_factor = _profit_factor(gross_profit_r, gross_loss_r)

    avg_win_r = sum(t.r_multiple for t in wins) / win_count if win_count > 0 else 0.0
    avg_loss_r = abs(sum(t.r_multiple for t in losses) / loss_count) if loss_count > 0 else 0.0
    payoff_ratio = avg_win_r / avg_loss_r if avg_loss_r > 0 else 0.0

    # Expectancy is the mean R per trade, so breakevens count as 0R rather than as losses.
    total_r = sum(t.r_multiple for t in trades)
    expectancy_r = total_r / total_trades if total_trades > 0 else 0.0

    # Peak-to-trough drawdown of cumulative P&L and of cumulative R
    cum_pnl = 0.0
    peak_pnl = 0.0
    max_dd_dollars = 0.0

    cum_r = 0.0
    peak_r = 0.0
    max_dd_r = 0.0

    for t in trades:
        cum_pnl += t.pnl
        cum_r += t.r_multiple

        if cum_pnl > peak_pnl:
            peak_pnl = cum_pnl
        if peak_pnl - cum_pnl > max_dd_dollars:
            max_dd_dollars = peak_pnl - cum_pnl

        if cum_r > peak_r:
            peak_r = cum_r
        dd_r = peak_r - cum_r
        if dd_r > max_dd_r:
            max_dd_r = dd_r

    # Setup attribution
    setup_names = sorted(list({t.setup for t in trades}))
    setup_stats: dict[str, dict[str, Any]] = {}
    for s in setup_names:
        s_trades = [t for t in trades if t.setup == s]
        s_wins = [t for t in s_trades if t.r_multiple > 0]
        s_losses = [t for t in s_trades if t.r_multiple < 0]
        s_pf = _profit_factor(sum(t.r_multiple for t in s_wins), abs(sum(t.r_multiple for t in s_losses)))
        s_wr = len(s_wins) / len(s_trades) if s_trades else 0.0
        s_exp = sum(t.r_multiple for t in s_trades) / len(s_trades) if s_trades else 0.0
        setup_stats[s] = {
            "count": len(s_trades),
            "win_rate": round(s_wr * 100, 1),
            "profit_factor": round(s_pf, 2),
            "expectancy_r": round(s_exp, 2),
            "net_pnl": round(sum(t.pnl for t in s_trades), 2),
            "total_r": round(sum(t.r_multiple for t in s_trades), 2),
        }

    # MAE and MFE diagnostics
    # What % of winning trades experienced MAE <= 0.50R?
    win_mae_under_50 = sum(1 for t in wins if t.mae_r <= 0.50) / win_count if win_count > 0 else 0.0
    # Average MFE left on table for winning trades (MFE - Exit R)
    avg_left_on_table_r = sum(t.mfe_r - t.r_multiple for t in wins) / win_count if win_count > 0 else 0.0
    # Loss trades where MFE reached >= 1.0R (round-tripped winners into losers)
    round_tripped_count = sum(1 for t in losses if t.mfe_r >= 1.0)

    # Discipline and Tilt Metrics
    adherent_trades = sum(1 for t in trades if t.adherence)
    adherence_score = (adherent_trades / total_trades) * 100.0 if total_trades > 0 else 0.0
    revenge_trades = sum(1 for t in trades if t.is_revenge)
    moved_stops = sum(1 for t in trades if t.moved_stop)

    # Capital Gate 5-Point Audit; 10R is a 10% drawdown at the standard 1% risk per trade
    logged = total_trades > 0
    gate_req_sample = total_trades >= 100
    gate_req_pf = logged and profit_factor >= 1.50
    gate_req_dd = logged and max_dd_r <= 10.0
    gate_req_adherence = logged and adherence_score >= 95.0 and revenge_trades == 0 and moved_stops == 0
    gate_req_mae_mfe = win_mae_under_50 >= 0.70  # At least 70% of winners had tight MAE <= 0.5R

    capital_gate_passed = gate_req_sample and gate_req_pf and gate_req_dd and gate_req_adherence and gate_req_mae_mfe
    if not logged:
        gate_status = "NO_TRADES_LOGGED"
    else:
        gate_status = "CAPITAL_GATE_PASSED" if capital_gate_passed else "CAPITAL_GATE_FAILED"

    return {
        "total_trades": total_trades,
        "win_count": win_count,
        "loss_count": loss_count,
        "breakeven_count": len(breakevens),
        "win_rate_pct": round(win_rate * 100, 2),
        "profit_factor": round(profit_factor, 2),
        "payoff_ratio": round(payoff_ratio, 2),
        "expectancy_r": round(expectancy_r, 3),
        "total_r_accumulated": round(total_r, 2),
        "net_pnl_dollars": round(net_pnl, 2),
        "max_drawdown_dollars": round(max_dd_dollars, 2),
        "max_drawdown_r": round(max_dd_r, 2),
        "adherence_score_pct": round(adherence_score, 2),
        "revenge_trade_count": revenge_trades,
        "moved_stop_count": moved_stops,
        "mae_win_under_50_pct": round(win_mae_under_50 * 100, 1),
        "avg_mfe_left_on_table_r": round(avg_left_on_table_r, 2),
        "round_tripped_loss_count": round_tripped_count,
        "setup_attribution": setup_stats,
        "capital_gate": {
            "overall_status": gate_status,
            "req_100_sample": "PASS" if gate_req_sample else "FAIL",
            "req_profit_factor_1_5": "PASS" if gate_req_pf else "FAIL",
            "req_drawdown_under_10r": "PASS" if gate_req_dd else "FAIL",
            "req_adherence_95": "PASS" if gate_req_adherence else "FAIL",
            "req_mae_mfe_calibrated": "PASS" if gate_req_mae_mfe else "FAIL",
        },
    }


class JournalStatsEngine(TradingLabEngine):
    @property
    def engine_id(self) -> str:
        return "journal_stats"

    @property
    def name(self) -> str:
        return "Trade Journal Analytics, MAE/MFE Forensics, and Capital Gate Engine"

    @property
    def description(self) -> str:
        return (
            "Analyzes trade logs for R-multiple expectancy, MAE/MFE stop calibration, "
            "setup performance attribution, behavioral tilt detection, and Capital Gate validation."
        )

    @property
    def asset_class(self) -> str:
        return "Performance Analytics / Discretionary & Systematic Trading"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "sample_trades": Param(
                name="sample_trades",
                param_type="int",
                default=100,
                description="Number of trades to evaluate in the journal sample",
                min_val=10,
                max_val=1000,
            ),
            "win_rate": Param(
                name="win_rate",
                param_type="float",
                default=0.45,
                description="Target strategy win rate (0.10 to 0.95)",
                min_val=0.10,
                max_val=0.95,
            ),
            "risk_reward_ratio": Param(
                name="risk_reward_ratio",
                param_type="float",
                default=2.2,
                description="Target average win to average loss ratio (payoff ratio)",
                min_val=0.5,
                max_val=10.0,
            ),
            "adherence_rate": Param(
                name="adherence_rate",
                param_type="float",
                default=0.96,
                description="Percentage of trades executed in strict adherence to rules (0.50 to 1.0)",
                min_val=0.50,
                max_val=1.0,
            ),
            "simulate_tilt": Param(
                name="simulate_tilt",
                param_type="bool",
                default=False,
                description="Simulate revenge trading and moved stops after consecutive loss streaks",
            ),
            "seed": Param(
                name="seed",
                param_type="int",
                default=42,
                description="Random seed for deterministic log simulation",
            ),
        }

    def run(self, **kwargs: Any) -> LabResult:
        p = self.validate_params(kwargs)
        trades_count: int = p["sample_trades"]
        wr: float = p["win_rate"]
        rr: float = p["risk_reward_ratio"]
        adh: float = p["adherence_rate"]
        tilt: bool = p["simulate_tilt"]
        seed: int = p["seed"]

        trade_log = generate_synthetic_trade_log(
            count=trades_count,
            win_rate=wr,
            risk_reward=rr,
            adherence_rate=adh,
            simulate_tilt=tilt,
            seed=seed,
        )

        analysis = analyze_trade_journal(trade_log)
        cg = analysis["capital_gate"]

        metrics: dict[str, float | int | str] = {
            "total_trades": analysis["total_trades"],
            "win_rate_pct": analysis["win_rate_pct"],
            "profit_factor": analysis["profit_factor"],
            "payoff_ratio": analysis["payoff_ratio"],
            "expectancy_r": analysis["expectancy_r"],
            "total_r_accumulated": analysis["total_r_accumulated"],
            "net_pnl_dollars": analysis["net_pnl_dollars"],
            "max_drawdown_r": analysis["max_drawdown_r"],
            "adherence_score_pct": analysis["adherence_score_pct"],
            "revenge_trades": analysis["revenge_trade_count"],
            "moved_stops": analysis["moved_stop_count"],
            "round_tripped_losses": analysis["round_tripped_loss_count"],
            "mae_tight_winners_pct": analysis["mae_win_under_50_pct"],
            "capital_gate_verdict": cg["overall_status"],
            "gate_sample_100": cg["req_100_sample"],
            "gate_profit_factor_1_5": cg["req_profit_factor_1_5"],
            "gate_drawdown_under_10r": cg["req_drawdown_under_10r"],
            "gate_adherence_95": cg["req_adherence_95"],
            "gate_mae_mfe": cg["req_mae_mfe_calibrated"],
        }

        summary = (
            f"Trade Journal Analysis for {trades_count} trades: Win Rate={analysis['win_rate_pct']:.1f}%, "
            f"Profit Factor={analysis['profit_factor']:.2f}, Expectancy={analysis['expectancy_r']:.2f}R/trade, "
            f"Net PnL=${analysis['net_pnl_dollars']:,.2f} ({analysis['total_r_accumulated']:+.1f}R). "
            f"Max Drawdown={analysis['max_drawdown_r']:.1f}R, Adherence={analysis['adherence_score_pct']:.1f}%. "
            f"Capital Gate Status: {cg['overall_status']} (PF: {cg['req_profit_factor_1_5']}, "
            f"DD: {cg['req_drawdown_under_10r']}, Rules: {cg['req_adherence_95']})."
        )

        # Pack top trades and setup attribution into data payload
        data = {
            "setup_attribution": analysis["setup_attribution"],
            "mae_mfe_forensics": {
                "winners_with_mae_under_50_pct": analysis["mae_win_under_50_pct"],
                "avg_r_left_on_table": analysis["avg_mfe_left_on_table_r"],
                "round_tripped_losses_count": analysis["round_tripped_loss_count"],
            },
            "capital_gate_breakdown": cg,
            "sample_trade_tail": [
                {
                    "id": t.trade_id,
                    "setup": t.setup,
                    "r": t.r_multiple,
                    "pnl": t.pnl,
                    "mae": t.mae_r,
                    "mfe": t.mfe_r,
                    "adherent": t.adherence,
                }
                for t in trade_log[-10:]
            ],
        }

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data=data,
            summary=summary,
        )


# Register engine into Trading Lab catalog
register(JournalStatsEngine())
