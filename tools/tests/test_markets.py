"""Unit tests for tools/qp/markets.py stage gate evaluation."""

import unittest

from tools.qp.markets import TRACK_METADATA, evaluate_all_markets_gates, evaluate_gate


class TestMarketsGates(unittest.TestCase):
    def test_track_metadata(self):
        self.assertIn("track_0_pqt", TRACK_METADATA)
        self.assertIn("track_6_trd", TRACK_METADATA)
        self.assertIn("track_fa", TRACK_METADATA)
        self.assertIn("track_val", TRACK_METADATA)
        self.assertIn("track_vi", TRACK_METADATA)
        self.assertIn("track_pf", TRACK_METADATA)

    def test_pqt_foundations_gate_evaluation(self):
        # Empty state should be pending
        gate_empty = evaluate_gate("track_0_pqt", "foundations", {}, {})
        self.assertFalse(gate_empty.passed)
        self.assertEqual(len(gate_empty.requirements), 2)

        # Passing state
        fake_vault_cards = {f"mkt-pqt-{i:03d}": {} for i in range(1, 65)}
        fake_store = {
            "cards": {f"mkt-pqt-{i:03d}": {"reps": 1} for i in range(1, 65)},
            "lab_history": [{"engine": "games", "metrics": {"performance_score": 75.0}}],
        }
        gate_passed = evaluate_gate("track_0_pqt", "foundations", fake_vault_cards, fake_store)
        self.assertTrue(gate_passed.passed)

    def test_trd_foundations_gate_evaluation(self):
        fake_vault_cards = {f"mkt-trd-{i:03d}": {} for i in range(1, 65)}
        fake_store = {
            "cards": {f"mkt-trd-{i:03d}": {"reps": 2} for i in range(1, 65)},
            "lab_history": [{"engine": "pos_sizing", "metrics": {"kelly_fraction": 0.12}}],
        }
        gate = evaluate_gate("track_6_trd", "foundations", fake_vault_cards, fake_store)
        self.assertTrue(gate.passed)

    def test_fa_gates_evaluation(self):
        fake_vault_cards = {f"mkt-fa-{i:03d}": {} for i in range(1, 257)}
        gate_empty = evaluate_gate("track_fa", "foundations", fake_vault_cards, {})
        self.assertFalse(gate_empty.passed)

        fake_store_f = {
            "cards": {f"mkt-fa-{i:03d}": {"reps": 1} for i in range(1, 129)},
        }
        gate_f_passed = evaluate_gate("track_fa", "foundations", fake_vault_cards, fake_store_f)
        self.assertTrue(gate_f_passed.passed)

        fake_store_c = {
            "cards": {f"mkt-fa-{i:03d}": {"reps": 1} for i in range(1, 257)},
        }
        gate_c_passed = evaluate_gate("track_fa", "core", fake_vault_cards, fake_store_c)
        self.assertTrue(gate_c_passed.passed)

    def test_val_vi_pf_gates_evaluation(self):
        for tid, pfx in [("track_val", "mkt-val-"), ("track_vi", "mkt-vi-"), ("track_pf", "mkt-pf-")]:
            fake_vault = {f"{pfx}{i:03d}": {} for i in range(1, 257)}
            fake_store = {
                "cards": {f"{pfx}{i:03d}": {"reps": 1} for i in range(1, 129)},
            }
            gate_f = evaluate_gate(tid, "foundations", fake_vault, fake_store)
            self.assertTrue(gate_f.passed)

            fake_store_all = {
                "cards": {f"{pfx}{i:03d}": {"reps": 1} for i in range(1, 257)},
            }
            gate_c = evaluate_gate(tid, "core", fake_vault, fake_store_all)
            self.assertTrue(gate_c.passed)

    def test_evaluate_all_markets_gates(self):
        all_gates = evaluate_all_markets_gates({}, {})
        self.assertIn("track_0_pqt", all_gates)
        self.assertIn("track_6_trd", all_gates)
        self.assertIn("track_fa", all_gates)
        self.assertIn("track_val", all_gates)
        self.assertIn("track_vi", all_gates)
        self.assertIn("track_pf", all_gates)
        self.assertIn("foundations", all_gates["track_fa"])
        self.assertIn("core", all_gates["track_fa"])


if __name__ == "__main__":
    unittest.main()
