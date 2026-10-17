"""Unit tests for tools/qp/lab/lob_sim.py Limit Order Book matching engine."""

import unittest

from tools.qp.lab.lob_sim import LimitOrderBook, LimitOrderBookEngine, Order
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


if __name__ == "__main__":
    unittest.main()
