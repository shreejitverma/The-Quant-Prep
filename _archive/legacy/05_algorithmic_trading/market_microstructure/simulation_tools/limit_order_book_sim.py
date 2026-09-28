import collections
import time

class Order:
    def __init__(self, order_id, side, price, qty, timestamp):
        self.order_id = order_id
        self.side = side # 'buy' or 'sell'
        self.price = price
        self.qty = qty
        self.timestamp = timestamp

    def __repr__(self):
        return f"[{self.order_id}] {self.side} {self.qty} @ {self.price}"

class LimitOrderBook:
    def __init__(self):
        self.bids = collections.defaultdict(list) # Price -> List[Order]
        self.asks = collections.defaultdict(list) # Price -> List[Order]
        self.best_bid = None
        self.best_ask = None

    def add_order(self, side, price, qty):
        order = Order(id(object), side, price, qty, time.time())

        if side == 'buy':
            # Check for immediate match (crossing the spread)
            while self.best_ask is not None and price >= self.best_ask and qty > 0:
                match_qty = self._match(order)
                qty -= match_qty

            if qty > 0:
                self.bids[price].append(order)
                if self.best_bid is None or price > self.best_bid:
                    self.best_bid = price

        elif side == 'sell':
            # Check for immediate match
            while self.best_bid is not None and price <= self.best_bid and qty > 0:
                match_qty = self._match(order)
                qty -= match_qty

            if qty > 0:
                self.asks[price].append(order)
                if self.best_ask is None or price < self.best_ask:
                    self.best_ask = price

    def _match(self, aggressive_order):
        """Matches an aggressive order against the resting book."""
        if aggressive_order.side == 'buy':
            resting_orders = self.asks[self.best_ask]
            book_side_map = self.asks
            best_price_attr = 'best_ask'
        else:
            resting_orders = self.bids[self.best_bid]
            book_side_map = self.bids
            best_price_attr = 'best_bid'

        matched = 0
        while aggressive_order.qty > 0 and resting_orders:
            resting_order = resting_orders[0]
            trade_qty = min(aggressive_order.qty, resting_order.qty)

            print(f"TRADE: {trade_qty} @ {resting_order.price}")

            aggressive_order.qty -= trade_qty
            resting_order.qty -= trade_qty
            matched += trade_qty

            if resting_order.qty == 0:
                resting_orders.pop(0)

        # Cleanup price level if empty
        if not resting_orders:
            del book_side_map[getattr(self, best_price_attr)]
            # Update BBO
            prices = sorted(book_side_map.keys(), reverse=(aggressive_order.side == 'sell'))
            setattr(self, best_price_attr, prices[0] if prices else None)

        return matched

if __name__ == "__main__":
    lob = LimitOrderBook()
    print("--- Adding Liquidity ---")
    lob.add_order('sell', 101, 100)
    lob.add_order('sell', 102, 50)
    lob.add_order('buy', 99, 100)

    print(f"Best Bid: {lob.best_bid}, Best Ask: {lob.best_ask}")

    print("\n--- Aggressive Buy (Crossing Spread) ---")
    lob.add_order('buy', 102, 120) # Should consume 100@101 and 20@102

    print(f"Best Bid: {lob.best_bid}, Best Ask: {lob.best_ask}")

