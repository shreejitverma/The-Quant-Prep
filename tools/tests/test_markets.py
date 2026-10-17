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
        self.assertIn("track_opt", all_gates)
        self.assertIn("track_ta", all_gates)
        self.assertIn("track_sys", all_gates)
        self.assertIn("track_his", all_gates)
        self.assertIn("track_car", all_gates)
        self.assertEqual(len(all_gates), 19)

    def test_all_19_tracks_present(self):
        self.assertEqual(len(TRACK_METADATA), 19)
        prefixes = {m["card_prefix"] for m in TRACK_METADATA.values()}
        self.assertEqual(len(prefixes), 19)

    def test_lab_engines_and_personas(self):
        from tools.qp.lab import get_engine, list_engines
        from tools.qp.markets import LAB_ENGINES, PERSONA_CONFIGS
        from tools.qp.planner import PERSONA_LAB_ROUTING

        registered_ids = {e["id"] for e in list_engines()}
        self.assertEqual(len(LAB_ENGINES), 11)
        self.assertEqual(set(LAB_ENGINES.keys()), registered_ids)
        self.assertIn("games", LAB_ENGINES)
        self.assertIn("opt_desk", LAB_ENGINES)
        self.assertIn("event_study", LAB_ENGINES)
        self.assertIn("overfit_trap", LAB_ENGINES)

        self.assertEqual(len(PERSONA_CONFIGS), 5)
        for persona, cfg in PERSONA_CONFIGS.items():
            for eng_id in cfg["required_engines"]:
                self.assertIsNotNone(get_engine(eng_id), f"{persona} references unregistered engine {eng_id}")
        for persona, routing in PERSONA_LAB_ROUTING.items():
            for eng_id in routing:
                self.assertIsNotNone(get_engine(eng_id), f"planner {persona} references unregistered engine {eng_id}")

    def test_calculate_markets_mastery_empty(self):
        from tools.qp.markets import calculate_markets_mastery

        res = calculate_markets_mastery({}, {}, "holistic")
        self.assertEqual(res["overall_score"], 0.0)
        self.assertEqual(res["readiness_level"], "Novice / Foundations")
        self.assertEqual(res["lab_stats"]["completed_engines"], 0)
        self.assertGreaterEqual(len(res["next_actions"]), 2)

    def test_calculate_markets_mastery_populated(self):
        from tools.qp.markets import calculate_markets_mastery

        fake_vault = {f"mkt-pqt-{i:03d}": {} for i in range(1, 129)}
        fake_vault.update({f"mkt-opt-{i:03d}": {} for i in range(1, 129)})

        fake_store = {
            "cards": {f"mkt-pqt-{i:03d}": {"reps": 3, "interval": 25} for i in range(1, 129)},
            "lab_history": [
                {"engine": "lob_sim"},
                {"engine": "mm_quote"},
                {"engine": "games"},
                {"engine": "opt_desk"},
            ],
        }

        qt_res = calculate_markets_mastery(fake_vault, fake_store, "quant_trader")
        self.assertGreater(qt_res["overall_score"], 20.0)
        self.assertEqual(qt_res["lab_stats"]["required_completed_count"], 4)
        self.assertGreater(qt_res["lab_score"], 70.0)
        self.assertEqual(qt_res["persona"], "quant_trader")

    def test_lab_run_records_history_in_cli_and_server(self):
        import io
        import tempfile
        from contextlib import redirect_stdout
        from pathlib import Path

        from tools.qp.lab.cli import main as lab_main
        from tools.qp.state import Store

        with tempfile.TemporaryDirectory() as td:
            store = Store(Path(td) / "home")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = lab_main(["run", "opt_desk"], store=store)
            self.assertEqual(rc, 0)
            self.assertEqual(len(store.data.get("lab_history", [])), 1)
            self.assertEqual(store.data["lab_history"][0]["engine"], "opt_desk")

            from tools.qp.server import App

            app = App(store)
            res = app.lab_run("mm_quote", {})
            self.assertIn("metrics", res)
            self.assertEqual(len(store.data.get("lab_history", [])), 2)
            self.assertEqual(store.data["lab_history"][1]["engine"], "mm_quote")

            fake_opt_vault = {f"mkt-opt-{i:03d}": {} for i in range(1, 129)}
            store.data["cards"] = {f"mkt-opt-{i:03d}": {"reps": 1} for i in range(65, 129)}
            gate = evaluate_gate("track_opt", "core", fake_opt_vault, store.data)
            self.assertTrue(gate.passed)


if __name__ == "__main__":
    unittest.main()
