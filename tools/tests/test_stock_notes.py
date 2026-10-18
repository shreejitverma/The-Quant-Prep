import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))
SCRIPTS = REPO_ROOT / "16-Trading-and-Investing" / "scripts"


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


stock_notes = load_script("stock_notes")


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

    def test_gordon_growth_oracle(self):
        # Closed-form oracle: When growth g equals terminal growth tg (0.03),
        # P = FCF * (1 + g) / (r - g) = 1.0 * 1.03 / 0.07 = 14.714285714285715
        p_oracle = 1.03 / 0.07
        res = stock_notes.solve_implied_growth(p_oracle, 1.0)
        self.assertEqual(res.status, "solved")
        self.assertIsNotNone(res.rate)
        self.assertAlmostEqual(res.rate, 0.03, places=4)

        # Yield oracle: FCF yield = FCF / P = 0.07 / 1.03
        y_oracle = 0.07 / 1.03
        res_y = stock_notes.implied_growth_from_fcf_yield(y_oracle)
        self.assertEqual(res_y.status, "solved")
        self.assertIsNotNone(res_y.rate)
        self.assertAlmostEqual(res_y.rate, 0.03, places=4)

    def test_normalize_market_data_drops_dividend_when_price_missing(self):
        lines = [
            "market_data:",
            "  price: None",
            "  market_cap: 0",
            "  dividend_yield: 0",
        ]
        norm, missing = stock_notes.normalize_market_data(lines)
        self.assertIn("dividend_yield", missing)
        fields = stock_notes.block_fields(stock_notes.get_block(norm, "market_data"))
        self.assertNotIn("dividend_yield", fields)

    def test_currency_mismatch_guard(self):
        res = stock_notes.implied_growth_from_fcf_yield(0.05, ticker="NTES")
        self.assertEqual(res.status, "currency_mismatch")
        self.assertIsNone(res.rate)


def quietly(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


def note(frontmatter, body="# Stock\n"):
    return "---\n" + "\n".join(frontmatter) + "\n---\n" + body


def market_fields(text):
    fm, _ = stock_notes.split_note(text)
    return stock_notes.block_fields(stock_notes.get_block(fm, "market_data"))


def value_fields(text):
    fm, _ = stock_notes.split_note(text)
    return stock_notes.block_fields(stock_notes.get_block(fm, "value_metrics"))


class FakeHistory:
    empty = True


class FakeTicker:
    def __init__(self, info):
        self.info = info

    def history(self, period):
        return FakeHistory()


class FakeYF:
    """Stands in for yfinance: records requested symbols and serves canned `info` dicts."""

    def __init__(self, infos):
        self.infos = infos
        self.requested = []

    def Ticker(self, symbol):  # noqa: N802 - mirrors the yfinance API
        self.requested.append(symbol)
        return FakeTicker(self.infos.get(symbol, {}))


class StockTreeCase(unittest.TestCase):
    """A temporary Stock Research tree; `write` places a note at <sector>/<country>/<name>."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "Stock Research"
        self.root.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


class TestMarketDataQuality(unittest.TestCase):
    def test_rerun_keeps_missing_price_and_market_cap_flagged(self):
        lines = ["market_data:", "  ticker: EVD", "  52w_high: 44.56", "  price: None", "  market_cap: 0"]
        once, missing = stock_notes.normalize_market_data(lines)
        twice, missing_again = stock_notes.normalize_market_data(once)
        self.assertEqual(twice, once)
        self.assertEqual(missing_again, missing)
        self.assertEqual(stock_notes.block_fields(stock_notes.get_block(twice, "market_data"))["data_quality"], "missing")

    def test_block_without_price_is_not_ok_even_if_labelled_ok(self):
        lines = ["market_data:", "  ticker: 600519", "  data_quality: ok"]
        norm, missing = stock_notes.normalize_market_data(lines)
        fields = stock_notes.block_fields(stock_notes.get_block(norm, "market_data"))
        self.assertEqual(missing, ["price", "market_cap"])
        self.assertEqual(fields["data_quality"], "missing")
        self.assertEqual(fields["missing"], "price market_cap")

    def test_price_without_market_cap_is_missing(self):
        lines = ["market_data:", "  ticker: BBCA.JK", "  price: 9000", "  data_quality: ok"]
        _, missing = stock_notes.normalize_market_data(lines)
        self.assertEqual(missing, ["market_cap"])

    def test_complete_block_is_ok_and_stable(self):
        lines = ["market_data:", "  ticker: AAPL", "  price: 312.06", "  market_cap: 4583336181760", "  dividend_yield: 0"]
        once, missing = stock_notes.normalize_market_data(lines)
        self.assertEqual(missing, [])
        self.assertEqual(stock_notes.block_fields(stock_notes.get_block(once, "market_data"))["data_quality"], "ok")
        self.assertEqual(stock_notes.normalize_market_data(once)[0], once)

    def test_values_from_another_listing_are_dropped(self):
        lines = ["ticker: NEM", "market_data:", "  ticker: NEM", "  price: 109.81", "  market_cap: 117227970560", "  data_quality: ok"]
        dropped, rejected = stock_notes.drop_foreign_listing_data(lines, "NEM.DE")
        self.assertEqual(rejected, "NEM")
        norm, missing = stock_notes.normalize_market_data(dropped)
        fields = stock_notes.block_fields(stock_notes.get_block(norm, "market_data"))
        self.assertEqual(fields, {"ticker": "NEM.DE", "data_quality": "missing", "missing": "price market_cap"})
        self.assertEqual(stock_notes.drop_foreign_listing_data(norm, "NEM.DE"), (norm, None))


class TestFetchSymbol(unittest.TestCase):
    root = Path("/vault/Stock Research")

    def test_mapped_ticker_uses_exchange_symbol(self):
        path = self.root / "Technology" / "Germany" / "Nemetschek (NEM).md"
        self.assertEqual(stock_notes.fetch_symbol(path, "NEM", root=self.root), "NEM.DE")

    def test_suffixed_and_us_tickers_pass_through(self):
        self.assertEqual(stock_notes.fetch_symbol(self.root / "Industrials" / "Europe" / "x.md", "SU.PA", root=self.root), "SU.PA")
        self.assertEqual(stock_notes.fetch_symbol(self.root / "Technology" / "US" / "x.md", "AAPL", root=self.root), "AAPL")

    def test_unmapped_bare_ticker_outside_us_is_refused(self):
        path = self.root / "Financials" / "Germany" / "Allianz (ALV).md"
        with self.assertRaises(stock_notes.UnmappedTickerError):
            stock_notes.fetch_symbol(path, "ALV", root=self.root)


class TestCurrencyAndYieldGuards(unittest.TestCase):
    def test_pence_and_pounds_are_different_currencies(self):
        self.assertFalse(stock_notes.check_currency_guard("GBP", "GBp"))
        self.assertTrue(stock_notes.check_currency_guard("GBP", "GBP"))

    def test_pence_convert_to_pounds(self):
        amount, currency = stock_notes.to_major_unit(4205.5, "GBp")
        self.assertAlmostEqual(amount, 42.055)
        self.assertEqual(currency, "GBP")
        self.assertEqual(stock_notes.to_major_unit(10.0, "EUR"), (10.0, "EUR"))

    def test_infy_yield_is_a_currency_mismatch(self):
        self.assertEqual(stock_notes.implied_growth_from_fcf_yield(0.0007, ticker="INFY"), stock_notes.ImpliedGrowth("currency_mismatch"))

    def test_implausible_yield_is_not_solved(self):
        for fcf_yield in (0.0007, 0.65):
            res = stock_notes.implied_growth_from_fcf_yield(fcf_yield)
            self.assertEqual(res.status, "implausible_fcf_yield")
            self.assertIsNone(res.rate)

    def test_negative_zero_rate_prints_as_zero(self):
        lines = stock_notes.implied_growth_lines(stock_notes.ImpliedGrowth("solved", -0.0004))
        self.assertEqual(lines[0], "  implied_growth_rate: 0.0%")
        self.assertEqual(stock_notes.format_rate(-0.0123), "-1.2%")

    def test_placeholder_zeros_become_missing(self):
        lines = [
            "value_metrics:",
            "  implied_growth_rate: 0%",
            "  quality:",
            "    debt_to_equity: 0.00",
            "  valuation:",
            "    fcf_yield: 0.00%",
            "    peg_ratio: 0.00",
        ]
        fields = stock_notes.block_fields(stock_notes.get_block(stock_notes.normalize_value_metrics(lines), "value_metrics"))
        self.assertEqual(fields["quality.debt_to_equity"], "N/A")
        self.assertEqual(fields["valuation.fcf_yield"], "N/A")
        self.assertEqual(fields["valuation.peg_ratio"], "N/A")
        self.assertEqual(stock_notes.format_ratio(0.0), "N/A")
        self.assertEqual(stock_notes.format_ratio(0.003), "0.003")

    def test_known_mismatch_yield_is_cleared_and_not_solved(self):
        lines = ["value_metrics:", "  implied_growth_rate: 70.8%", "  valuation:", "    fcf_yield: 0.07%"]
        lines = stock_notes.normalize_value_metrics(lines, ticker="INFY")
        lines, result = stock_notes.apply_implied_growth(lines)
        fields = stock_notes.block_fields(stock_notes.get_block(lines, "value_metrics"))
        self.assertEqual(fields["valuation.fcf_yield"], "currency_mismatch")
        self.assertEqual(result.status, "currency_mismatch")
        self.assertEqual(fields["implied_growth_rate"], "n/a")


class TestUpdateMarketData(StockTreeCase):
    def setUp(self):
        super().setUp()
        self.mod = load_script("update_market_data")
        self.original = (stock_notes.STOCK_ROOT, self.mod.yf)
        stock_notes.STOCK_ROOT = self.root

    def tearDown(self):
        stock_notes.STOCK_ROOT, self.mod.yf = self.original
        super().tearDown()

    def run_update(self, rel, ticker, infos):
        text = note(["ticker: " + ticker, "last_updated: 2026-05-31 14:01:13", "market_data:", "  ticker: OLD", "  price: 1"])
        path = self.write(rel, text)
        self.mod.yf = FakeYF(infos)
        written = quietly(self.mod.update_stock_file, path, ticker)
        return written, text, path.read_text(encoding="utf-8")

    def test_fetches_the_mapped_exchange_symbol(self):
        info = {"currentPrice": 95.0, "marketCap": 11_000_000_000, "currency": "EUR"}
        written, _, after = self.run_update("Technology/Germany/Nemetschek (NEM).md", "NEM", {"NEM.DE": info})
        self.assertTrue(written)
        self.assertEqual(self.mod.yf.requested, ["NEM.DE"])
        fields = market_fields(after)
        self.assertEqual((fields["ticker"], fields["price"], fields["data_quality"]), ("NEM.DE", "95.0", "ok"))

    def test_no_price_leaves_note_untouched(self):
        written, before, after = self.run_update("Technology/Germany/Nemetschek (NEM).md", "NEM", {"NEM.DE": {"marketCap": 5}})
        self.assertFalse(written)
        self.assertEqual(after, before)

    def test_unknown_currency_is_not_written_as_usd(self):
        _, _, after = self.run_update("Technology/US/Apple (AAPL).md", "AAPL", {"AAPL": {"currentPrice": 10.0, "marketCap": 100}})
        self.assertNotIn("currency", market_fields(after))

    def test_pence_quote_is_written_in_pounds(self):
        info = {"currentPrice": 4205.5, "fiftyTwoWeekHigh": 5542.0, "marketCap": 91_067_555_840, "currency": "GBp"}
        _, _, after = self.run_update("Consumer Staples/Europe/Unilever (ULVR.L).md", "ULVR.L", {"ULVR.L": info})
        fields = market_fields(after)
        self.assertEqual(fields["currency"], "GBP")
        self.assertAlmostEqual(float(fields["price"]), 42.055)
        self.assertAlmostEqual(float(fields["52w_high"]), 55.42)


class TestFetchHistoricalValue(StockTreeCase):
    def setUp(self):
        super().setUp()
        self.mod = load_script("fetch_historical_value")
        self.original = (stock_notes.STOCK_ROOT, self.mod.yf)
        stock_notes.STOCK_ROOT = self.root

    def tearDown(self):
        stock_notes.STOCK_ROOT, self.mod.yf = self.original
        super().tearDown()

    def test_operating_cash_flow_is_not_used_as_fcf(self):
        path = self.write("Financials/Malaysia/Public Bank (PBBANK).md", note(["ticker: PBBANK"]))
        info = {"operatingCashflow": 5_000_000_000, "marketCap": 100_000_000_000, "pegRatio": 0}
        self.mod.yf = FakeYF({"PBBANK.KL": info})
        quietly(self.mod.update_value_metrics, path, "PBBANK")
        fields = value_fields(path.read_text(encoding="utf-8"))
        self.assertEqual(self.mod.yf.requested, ["PBBANK.KL"])
        self.assertEqual(fields["valuation.fcf_yield"], "N/A")
        self.assertEqual(fields["implied_growth_status"], "missing_fcf")
        self.assertEqual(fields["valuation.peg_ratio"], "N/A")
        self.assertNotIn("currency", fields)


class TestReverseDcfLive(StockTreeCase):
    def setUp(self):
        super().setUp()
        self.mod = load_script("quant_reverse_dcf")
        self.original = (stock_notes.STOCK_ROOT, self.mod.yf)
        stock_notes.STOCK_ROOT = self.root

    def tearDown(self):
        stock_notes.STOCK_ROOT, self.mod.yf = self.original
        super().tearDown()

    def solve(self, rel, ticker, info):
        path = self.write(rel, note(["ticker: " + ticker, "value_metrics:", "  valuation:", "    fcf_yield: 5.00%"]))
        self.mod.yf = FakeYF({stock_notes.fetch_symbol(path, ticker, root=self.root): info})
        quietly(self.mod.update_implied_growth, path, ticker)
        return value_fields(path.read_text(encoding="utf-8"))

    def test_pence_price_is_converted_before_solving(self):
        # Gordon oracle: FCF per share 1 GBP at price 1.03 / 0.07 GBP implies growth equal to terminal growth, 3%.
        pence = 100 * 1.03 / 0.07
        info = {"currentPrice": pence, "currency": "GBp", "financialCurrency": "GBP", "freeCashflow": 1e9, "sharesOutstanding": 1e9}
        fields = self.solve("Consumer Staples/Europe/Tesco (TSCO.L).md", "TSCO.L", info)
        self.assertEqual(fields["implied_growth_status"], "solved")
        self.assertEqual(fields["implied_growth_rate"], "3.0%")

    def test_known_mismatch_is_never_solved_live(self):
        info = {"currentPrice": 1470.0, "currency": "INR", "financialCurrency": "INR", "freeCashflow": 1e9, "sharesOutstanding": 1e7}
        fields = self.solve("Technology/India/Infosys (INFY).md", "INFY", info)
        self.assertEqual(fields["implied_growth_status"], "currency_mismatch")
        self.assertEqual(fields["implied_growth_rate"], "n/a")

    def test_operating_cash_flow_is_not_used_as_fcf(self):
        info = {"currentPrice": 100.0, "currency": "USD", "operatingCashflow": 1e9, "sharesOutstanding": 1e8}
        fields = self.solve("Technology/US/Example (EXM).md", "EXM", info)
        self.assertEqual(fields["implied_growth_status"], "missing_fcf")


class TestSectorBenchmarker(StockTreeCase):
    def test_missing_roe_ranks_last_and_unreadable_notes_are_listed(self):
        bench = load_script("quant_sector_benchmarker")
        metrics = ["value_metrics:", "  returns:", "    cagr_10y: 9.00%", "  quality:"]
        self.write("Financials/US/FICO (FICO).md", note([*metrics, "    roe: N/A", "    debt_to_equity: N/A"]))
        self.write("Financials/US/Visa (V).md", note([*metrics, "    roe: 9.50%", "    debt_to_equity: 0.67"]))
        self.write("Financials/US/Mastercard (MA).md", note([*metrics, "    roe: 232.08%"]))
        self.write("Financials/India/HDFC Bank.md", note(["status: research"]))
        rows, skipped = bench.collect_sector(self.root / "Financials")
        self.assertEqual([name for name, _ in rows], ["Mastercard (MA)", "Visa (V)", "FICO (FICO)"])
        self.assertEqual(skipped, [("HDFC Bank", "no value_metrics block")])
        report = bench.render_report("Financials", rows, skipped)
        self.assertIn("| FICO (FICO) | N/A | 9.00% | N/A | N/A |", report)
        self.assertIn("- HDFC Bank: no value_metrics block", report)


class TestStockMoc(unittest.TestCase):
    def test_germany_and_every_benchmark_are_listed(self):
        moc = load_script("generate_stock_moc")
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            vault = repo / "Stock Research"
            for rel in ("Materials/Germany/Symrise (SY1).md", "Materials/_Sector_Analysis.md", "Utilities/_Sector_Analysis.md"):
                (vault / rel).parent.mkdir(parents=True, exist_ok=True)
                (vault / rel).write_text("---\n---\n", encoding="utf-8")
            original = (moc.REPO_ROOT, moc.VAULT_ROOT)
            moc.REPO_ROOT, moc.VAULT_ROOT = repo, vault
            try:
                quietly(moc.generate_moc)
            finally:
                moc.REPO_ROOT, moc.VAULT_ROOT = original
            text = (vault / "_Index_Stock Research.md").read_text(encoding="utf-8")
        self.assertIn("- **Germany**: [[Stock Research/Materials/Germany/Symrise (SY1)|Symrise (SY1)]]", text)
        self.assertIn("[[Stock Research/Materials/_Sector_Analysis|Materials Benchmark]]", text)
        self.assertIn("[[Stock Research/Utilities/_Sector_Analysis|Utilities Benchmark]]", text)
        self.assertIn("SORT number(value_metrics.quality.roe) = null ASC, number(value_metrics.quality.roe) DESC", text)


class TestHistoricalMigration(StockTreeCase):
    def test_rerun_does_not_grow_the_note(self):
        migrate = load_script("migrate_stock_notes")
        path = self.write("Historical/Kodak (The Digital Blindness).md", "garbage\n# Stock: Kodak\n\nstatus:: done\nBody\n")
        quietly(migrate.migrate_historical_note, path)
        once = path.read_text(encoding="utf-8")
        quietly(migrate.migrate_historical_note, path)
        self.assertEqual(path.read_text(encoding="utf-8"), once)
        self.assertTrue(once.endswith("Body\n"))


if __name__ == "__main__":
    unittest.main()
