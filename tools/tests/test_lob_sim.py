"""Unit tests for tools/qp/lab/lob_sim.py Limit Order Book matching engine."""

import math
import unittest

from tools.qp.lab.lob_sim import AC_KAPPA, LimitOrderBook, LimitOrderBookEngine, Order, almgren_chriss_schedule
from tools.qp.lab.registry import get_engine


class TestLimitOrderBook(unittest.TestCase):
    def test_price_time_priority(self):
        lob = LimitOrderBook(tick_size=0.01)
        # Order 1: Buy 10 @ 100.00
        # Order 2: Buy 20 @ 100.00 (same price, later time)
        lob.insert_order(Order(1, "buy", 100.00, 10, 1))
        lob.insert_order(Order(2, "buy", 100.00, 20, 2))

        self.assertEqual(lob.best_bid(), 100.00)

        # Market sell order for 15 shares
        mkt_sell = Order(3, "sell", 0.0, 15, 3, order_type="market")
        fills = lob.insert_order(mkt_sell)

        # Should match Order 1 (10 shares), then Order 2 (5 shares)
        self.assertEqual(len(fills), 2)
        maker1, taker1, p1, s1 = fills[0]
        self.assertEqual(maker1.order_id, 1)
        self.assertEqual(s1, 10)
        self.assertEqual(p1, 100.00)

        maker2, taker2, p2, s2 = fills[1]
        self.assertEqual(maker2.order_id, 2)
        self.assertEqual(s2, 5)

        # Order 2 should have 15 shares remaining in the book
        self.assertEqual(lob.orders[2].size, 15)
        self.assertNotIn(1, lob.orders)

    def test_book_never_crossed(self):
        lob = LimitOrderBook(tick_size=0.01)
        lob.insert_order(Order(1, "buy", 100.00, 100, 1))
        lob.insert_order(Order(2, "sell", 100.05, 100, 2))

        # Best bid < best ask
        self.assertLess(lob.best_bid(), lob.best_ask())

        # Cross book with aggressive buy limit order @ 100.10 for 50 shares
        fills = lob.insert_order(Order(3, "buy", 100.10, 50, 3))
        self.assertEqual(len(fills), 1)
        self.assertEqual(fills[0][2], 100.05)  # matched at resting ask price

        # Remaining book is still uncrossed
        self.assertLess(lob.best_bid(), lob.best_ask())

    def test_post_only_and_ioc(self):
        lob = LimitOrderBook(tick_size=0.01)
        lob.insert_order(Order(1, "sell", 100.05, 100, 1))

        # Post-only buy order at 100.10 crosses the ask; should NOT rest in book
        post_only_order = Order(2, "buy", 100.10, 50, 2, order_type="post_only")
        lob.insert_order(post_only_order)
        # Should not be in orders dict
        self.assertNotIn(2, lob.orders)

        # IOC order for 200 shares (only 100 available)
        ioc_order = Order(3, "buy", 100.05, 200, 3, order_type="ioc")
        fills = lob.insert_order(ioc_order)
        self.assertEqual(len(fills), 1)
        self.assertEqual(fills[0][3], 50)  # takes remaining 50 from order 1
        self.assertNotIn(3, lob.orders)  # remaining 150 cancelled

    def test_lob_engine_run(self):
        engine = get_engine("lob_sim")
        self.assertIsNotNone(engine)
        self.assertIsInstance(engine, LimitOrderBookEngine)

        res_twap = engine.run(
            initial_price=100.0,
            parent_size=2000,
            parent_side="buy",
            n_steps=50,
            strategy="twap",
            seed=42,
        )

        res_aggr = engine.run(
            initial_price=100.0,
            parent_size=2000,
            parent_side="buy",
            n_steps=50,
            strategy="aggressive",
            seed=42,
        )

        self.assertEqual(res_twap.metrics["executed_shares"], 2000)
        self.assertEqual(res_aggr.metrics["executed_shares"], 2000)

        # Aggressive immediate sweep should produce higher implementation shortfall than gradual TWAP
        self.assertGreaterEqual(
            res_aggr.metrics["implementation_shortfall_bps"],
            res_twap.metrics["implementation_shortfall_bps"],
        )

        # Oracle: every agent tape record is an execution fill, and the tape follows fill chronology.
        tape_run = engine.run(
            initial_price=100.0,
            parent_size=100,
            parent_side="buy",
            n_steps=10,
            strategy="aggressive",
            seed=42,
        )
        trades = tape_run.data["trades"]
        self.assertGreater(len(trades), 0)
        agent_trades = [trade for trade in trades if trade["aggressor"] == "agent"]
        self.assertEqual(sum(trade["size"] for trade in agent_trades), tape_run.metrics["executed_shares"])
        self.assertTrue(all(trade["side"] == "buy" for trade in agent_trades))
        self.assertEqual([trade["time"] for trade in trades], sorted(trade["time"] for trade in trades))

    def test_swept_side_keeps_its_last_level_in_the_mid(self):
        # Bid 99.99 and asks 100.01-100.03: a 300-share market buy empties the asks. The mid must be
        # (99.99 + 100.03) / 2 = 100.01 using the deepest consumed level, not snap back to the 99.99 bid.
        lob = LimitOrderBook(tick_size=0.01)
        lob.insert_order(Order(1, "buy", 99.99, 100, 0))
        for i, px in enumerate([100.01, 100.02, 100.03], start=2):
            lob.insert_order(Order(i, "sell", px, 100, 0))
        lob.insert_order(Order(9, "buy", 0.0, 300, 1, order_type="market"))
        self.assertIsNone(lob.best_ask())
        self.assertAlmostEqual(lob.mid_price(), 100.01, places=4)

        mirror = LimitOrderBook(tick_size=0.01)
        mirror.insert_order(Order(1, "sell", 100.01, 100, 0))
        for i, px in enumerate([99.99, 99.98, 99.97], start=2):
            mirror.insert_order(Order(i, "buy", px, 100, 0))
        mirror.insert_order(Order(9, "sell", 0.0, 300, 1, order_type="market"))
        self.assertIsNone(mirror.best_bid())
        self.assertAlmostEqual(mirror.mid_price(), 99.99, places=4)

    def test_one_sided_mid_never_falls_below_the_live_best_bid(self):
        # A limit buy at 100.10 sweeps every ask up to 100.03 and rests 100 shares at 100.10;
        # a mid below the live best bid would be a crossed quote.
        lob = LimitOrderBook(tick_size=0.01)
        for i, px in enumerate([100.01, 100.02, 100.03], start=1):
            lob.insert_order(Order(i, "sell", px, 100, 0))
        lob.insert_order(Order(9, "buy", 100.10, 400, 1))
        self.assertEqual(lob.best_bid(), 100.10)
        self.assertIsNone(lob.best_ask())
        self.assertGreaterEqual(lob.mid_price(), lob.best_bid())


class TestExecutionSchedules(unittest.TestCase):
    def test_almgren_chriss_schedule_fills_the_parent_exactly(self):
        # Holdings follow x_k = X sinh(kappa (N - k)) / sinh(kappa N) to within half a share, never sell
        # back, and telescope to the parent quantity; ceil-rounding the holdings left shares unscheduled.
        for qty, steps in [(100, 10), (101, 37), (2000, 50), (5000, 100), (99999, 1000)]:
            children = almgren_chriss_schedule(qty, steps, AC_KAPPA)
            with self.subTest(qty=qty, steps=steps):
                self.assertEqual(len(children), steps)
                self.assertEqual(sum(children), qty)
                self.assertTrue(all(c >= 0 for c in children))
                held = qty
                for k, child in enumerate(children, start=1):
                    held -= child
                    exact = qty * math.sinh(AC_KAPPA * (steps - k)) / math.sinh(AC_KAPPA * steps)
                    self.assertLessEqual(abs(held - exact), 0.5)

    def test_almgren_chriss_engine_executes_the_whole_parent(self):
        engine = get_engine("lob_sim")
        for size in [100, 2000, 5000]:
            for side in ["buy", "sell"]:
                metrics = engine.run(parent_size=size, parent_side=side, n_steps=100, strategy="almgren_chriss", seed=42).metrics
                with self.subTest(size=size, side=side):
                    self.assertEqual(metrics["executed_shares"], size)
                    self.assertEqual(metrics["fill_rate"], 1.0)

    def test_impact_is_monotone_in_parent_size(self):
        # Same seed means the same background flow (the agent never draws from the RNG), so a bigger
        # parent can only walk further through the same liquidity: shortfall vs the arrival mid must not
        # fall with size. Sizes past the 5000-share seeded depth exercise the one-sided book.
        engine = get_engine("lob_sim")
        cases = [
            ("aggressive", [500, 1000, 2000, 5000, 6000, 8000, 12000, 20000, 50000]),
            ("almgren_chriss", [1000, 2000, 5000, 8000, 12000, 20000, 50000]),
        ]
        for strategy, sizes in cases:
            for side in ["buy", "sell"]:
                runs = [engine.run(parent_size=q, parent_side=side, n_steps=100, strategy=strategy, seed=42).metrics for q in sizes]
                shortfalls = [m["implementation_shortfall_bps"] for m in runs]
                with self.subTest(strategy=strategy, side=side):
                    self.assertEqual(shortfalls, sorted(shortfalls))
                    for q, m in zip(sizes, runs, strict=True):
                        if q <= 20000:
                            self.assertEqual(m["executed_shares"], q)


if __name__ == "__main__":
    unittest.main()
