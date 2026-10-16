import importlib.util
import sys
import unittest
from pathlib import Path

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

spec = importlib.util.spec_from_file_location(
    "stock_notes",
    REPO_ROOT / "16-Trading-and-Investing" / "scripts" / "stock_notes.py",
)
stock_notes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stock_notes)


class TestStockNotes(unittest.TestCase):
    def test_extract_ticker(self):
        self.assertEqual(stock_notes.extract_ticker("Sherwin-Williams (SHW).md"), "SHW")
        self.assertEqual(stock_notes.extract_ticker("Berkshire Hathaway (BRK.B).md"), "BRK.B")
        self.assertEqual(stock_notes.extract_ticker("CTS Eventim (EVD).md"), "EVD")
        self.assertEqual(stock_notes.extract_ticker("Fast Retailing (9983).md"), "9983")
        # Historical notes with long parentheticals are not tickers
        self.assertIsNone(stock_notes.extract_ticker("Kodak (The Digital Blindness).md"))
        self.assertIsNone(stock_notes.extract_ticker("NoParens.md"))

    def test_split_and_join_note(self):
        content = "---\nticker: AAPL\n---\n# Apple\nBody text"
        fm, body = stock_notes.split_note(content)
        self.assertEqual(fm, ["ticker: AAPL"])
        self.assertEqual(body, "# Apple\nBody text")
        self.assertEqual(stock_notes.join_note(fm, body), content)

        # No frontmatter
        no_fm, no_body = stock_notes.split_note("# Apple\nNo FM")
        self.assertIsNone(no_fm)
        self.assertEqual(no_body, "# Apple\nNo FM")

        # Unclosed fence
        with self.assertRaises(stock_notes.NoteFormatError):
            stock_notes.split_note("---\nticker: AAPL\nunclosed")

    def test_block_manipulation(self):
        lines = [
            "ticker: AAPL",
            "market_data:",
            "  price: 150",
            "  pe: 25",
            "status: draft",
        ]
        self.assertEqual(stock_notes.top_level_keys(lines), ["ticker", "market_data", "status"])
        block = stock_notes.get_block(lines, "market_data")
        self.assertEqual(block, ["market_data:", "  price: 150", "  pe: 25"])

        # Replace block
        new_block = ["market_data:", "  price: 175"]
        updated = stock_notes.set_block(lines, "market_data", new_block)
        self.assertEqual(stock_notes.get_block(updated, "market_data"), new_block)
        self.assertEqual(updated[-1], "status: draft")

        # Remove block
        removed = stock_notes.remove_block(lines, "market_data")
        self.assertIsNone(stock_notes.get_block(removed, "market_data"))
        self.assertEqual(stock_notes.top_level_keys(removed), ["ticker", "status"])

    def test_relocate_misplaced_blocks(self):
        bad_note = (
            "---\n"
            "ticker: SHW\n"
            "status: complete\n"
            "---\n"
            "last_updated: 2026-05-31 14:01:04\n"
            "market_data:\n"
            "  ticker: SHW\n"
            "  price: 303.84\n"
            "\n"
            "# Stock: Sherwin-Williams (SHW)\n"
            "Body\n"
        )
        fixed, moved = stock_notes.relocate_misplaced_blocks(bad_note)
        self.assertEqual(moved, ["last_updated", "market_data"])
        fm, body = stock_notes.split_note(fixed)
        self.assertIn("last_updated: 2026-05-31 14:01:04", fm)
        self.assertIn("market_data:", fm)
        self.assertTrue(body.startswith("\n# Stock: Sherwin-Williams (SHW)"))

    def test_normalize_market_data(self):
        lines = [
            "market_data:",
            "  price: None",
            "  market_cap: 0",
            "  pe_ratio: 25.5",
        ]
        norm, missing = stock_notes.normalize_market_data(lines)
        self.assertIn("price", missing)
        self.assertIn("market_cap", missing)
        fields = stock_notes.block_fields(stock_notes.get_block(norm, "market_data"))
        self.assertEqual(fields.get("data_quality"), "missing")
        self.assertIn("price market_cap", fields.get("missing", ""))
        self.assertNotIn("price", fields)

    def test_solve_implied_growth(self):
        # Missing price
        res_np = stock_notes.solve_implied_growth(None, 10.0)
        self.assertEqual(res_np.status, "missing_price")

        # Missing or negative FCF
        res_nf = stock_notes.solve_implied_growth(100.0, -5.0)
        self.assertEqual(res_nf.status, "non_positive_fcf")

        # Normal case
        res = stock_notes.solve_implied_growth(100.0, 5.0)
        self.assertEqual(res.status, "solved")
        self.assertIsNotNone(res.rate)
        # Check tolerance: dcf_value at solved rate should be approx 100
        val = stock_notes.dcf_value(5.0, res.rate)
        self.assertAlmostEqual(val, 100.0, delta=0.01)

    def test_implied_growth_from_fcf_yield(self):
        res_zero = stock_notes.implied_growth_from_fcf_yield(0.0)
        self.assertEqual(res_zero.status, "missing_fcf")

        res_neg = stock_notes.implied_growth_from_fcf_yield(-0.02)
        self.assertEqual(res_neg.status, "non_positive_fcf")

        res_ok = stock_notes.implied_growth_from_fcf_yield(0.05)
        self.assertEqual(res_ok.status, "solved")
        self.assertIsNotNone(res_ok.rate)


if __name__ == "__main__":
    unittest.main()
