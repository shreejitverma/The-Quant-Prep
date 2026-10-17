"""Unit tests for Trade Journal Analytics and Capital Gate Engine."""

import unittest

from tools.qp.lab import get_engine
from tools.qp.lab.journal_stats import (
    TradeRecord,
    analyze_trade_journal,
    generate_synthetic_trade_log,
)
from tools.qp.markets import evaluate_gate


class TestJournalStats(unittest.TestCase):
    def test_expectancy_and_profit_factor_math(self):
        trades = [
            TradeRecord(
                trade_id="T1",
                setup="breakout",
                entry_price=100.0,
                exit_price=104.0,
                stop_loss=98.0,
                take_profit=104.0,
                shares=250,
                r_multiple=2.0,
                pnl=1000.0,
                mae_r=0.2,
                mfe_r=2.2,
                adherence=True,
                is_revenge=False,
                moved_stop=False,
                duration_minutes=60,
            ),
            TradeRecord(
                trade_id="T2",
                setup="breakout",
                entry_price=100.0,
                exit_price=98.0,
                stop_loss=98.0,
                take_profit=104.0,
                shares=250,
                r_multiple=-1.0,
                pnl=-500.0,
                mae_r=1.0,
                mfe_r=0.3,
                adherence=True,
                is_revenge=False,
                moved_stop=False,
                duration_minutes=30,
            ),
            TradeRecord(
                trade_id="T3",
                setup="pullback",
                entry_price=50.0,
                exit_price=53.0,
                stop_loss=48.0,
                take_profit=54.0,
                shares=250,
                r_multiple=1.5,
                pnl=750.0,
                mae_r=0.4,
                mfe_r=1.8,
                adherence=True,
                is_revenge=False,
                moved_stop=False,
                duration_minutes=120,
            ),
        ]

        analysis = analyze_trade_journal(trades, initial_capital=10000.0)

        # 2 wins, 1 loss -> Win Rate = 66.67%
        self.assertAlmostEqual(analysis["win_rate_pct"], 66.67, places=1)
        # Gross profit = 1750, Gross loss = 500 -> Profit Factor = 3.50
        self.assertAlmostEqual(analysis["profit_factor"], 3.50, places=2)
        # Total R = 2.0 - 1.0 + 1.5 = +2.5R
        self.assertAlmostEqual(analysis["total_r_accumulated"], 2.50, places=2)
        # Net PnL = $1,250.00
        self.assertAlmostEqual(analysis["net_pnl_dollars"], 1250.00, places=2)

    def test_tilt_detection_and_adherence(self):
        log = generate_synthetic_trade_log(
            count=100,
            win_rate=0.40,
            risk_reward=2.0,
            adherence_rate=0.90,
            simulate_tilt=True,
            seed=42,
        )

        analysis = analyze_trade_journal(log)
        self.assertGreater(analysis["revenge_trade_count"], 0)
        self.assertLess(analysis["adherence_score_pct"], 95.0)
        self.assertEqual(analysis["capital_gate"]["overall_status"], "CAPITAL_GATE_FAILED")

    def test_capital_gate_evaluation(self):
        # Generate pristine disciplined log designed to pass
        log = generate_synthetic_trade_log(
            count=100,
            win_rate=0.55,
            risk_reward=2.5,
            adherence_rate=1.0,
            simulate_tilt=False,
            seed=101,
        )
        # Override MAEs to verify tight stop calibration criterion
        for t in log:
            if t.r_multiple > 0:
                t.mae_r = 0.35  # Force <= 0.5R

        analysis = analyze_trade_journal(log)
        cg = analysis["capital_gate"]
        self.assertEqual(cg["req_100_sample"], "PASS")
        self.assertEqual(cg["req_profit_factor_1_5"], "PASS")
        self.assertEqual(cg["req_drawdown_under_10"], "PASS")
        self.assertEqual(cg["req_adherence_95"], "PASS")
        self.assertEqual(cg["req_mae_mfe_calibrated"], "PASS")
        self.assertEqual(cg["overall_status"], "CAPITAL_GATE_PASSED")

    def test_engine_registered_and_runnable(self):
        engine = get_engine("journal_stats")
        self.assertIsNotNone(engine)

        result = engine.run(sample_trades=50, seed=123)
        self.assertIn("profit_factor", result.metrics)
        self.assertIn("capital_gate_verdict", result.metrics)
        self.assertIn("setup_attribution", result.data)

        # Markets stage gate integration
        gate = evaluate_gate("track_6_trd", "capital_gate", store_state={})
        self.assertEqual(gate.stage, "capital_gate")
        self.assertEqual(len(gate.requirements), 5)


if __name__ == "__main__":
    unittest.main()
