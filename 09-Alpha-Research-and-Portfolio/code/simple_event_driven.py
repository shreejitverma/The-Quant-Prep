import queue
import datetime

# Event Types
class Event:
    pass

class MarketEvent(Event):
    def __init__(self, timestamp, symbol, price):
        self.type = 'MARKET'
        self.timestamp = timestamp
        self.symbol = symbol
        self.price = price

class SignalEvent(Event):
    def __init__(self, timestamp, symbol, side, strength):
        self.type = 'SIGNAL'
        self.timestamp = timestamp
        self.symbol = symbol
        self.side = side # 'LONG' or 'SHORT'
        self.strength = strength

class OrderEvent(Event):
    def __init__(self, timestamp, symbol, side, quantity, order_type='MKT'):
        self.type = 'ORDER'
        self.timestamp = timestamp
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.order_type = order_type

class FillEvent(Event):
    def __init__(self, timestamp, symbol, side, quantity, price, cost):
        self.type = 'FILL'
        self.timestamp = timestamp
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.price = price
        self.cost = cost

# Components
class DataHandler:
    """Generates MarketEvents from data source."""
    def __init__(self, events):
        self.events = events
        self.data = [
            (datetime.datetime(2023, 1, 1, 10, 0), 'AAPL', 150.0),
            (datetime.datetime(2023, 1, 1, 10, 1), 'AAPL', 151.0),
            (datetime.datetime(2023, 1, 1, 10, 2), 'AAPL', 149.0),
        ]
        self.idx = 0

    def update_bars(self):
        if self.idx < len(self.data):
            dt, sym, price = self.data[self.idx]
            evt = MarketEvent(dt, sym, price)
            self.events.put(evt)
            self.idx += 1
            return True
        return False

class Strategy:
    """Consumes MarketEvent, produces SignalEvent."""
    def __init__(self, events):
        self.events = events

    def on_market_data(self, event):
        if event.price > 150.5:
            # Simple Momentum Strategy
            signal = SignalEvent(event.timestamp, event.symbol, 'SHORT', 1.0)
            self.events.put(signal)
            print(f"Strategy: SHORT Signal at {event.price}")

class Portfolio:
    """Consumes SignalEvent, produces OrderEvent. Manages Positions."""
    def __init__(self, events):
        self.events = events
        self.positions = {}

    def on_signal(self, event):
        # Simple Logic: 100 shares per signal
        qty = 100
        side = 'SELL' if event.side == 'SHORT' else 'BUY'
        order = OrderEvent(event.timestamp, event.symbol, side, qty)
        self.events.put(order)
        print(f"Portfolio: Generating {side} order for {qty} shares")

class ExecutionHandler:
    """Consumes OrderEvent, produces FillEvent. Simulates Exchange."""
    def __init__(self, events):
        self.events = events

    def on_order(self, event):
        # Assume immediate fill at current market price (Simplified)
        # In real backtester, we look up current price from DataHandler
        fill_price = 150.0 # Mock
        cost = fill_price * event.quantity
        fill = FillEvent(event.timestamp, event.symbol, event.side, event.quantity, fill_price, cost)
        self.events.put(fill)
        print(f"Execution: Filled {event.side} {event.quantity} @ {fill_price}")

# Backtest Engine
def run_backtest():
    events = queue.Queue()
    data = DataHandler(events)
    strategy = Strategy(events)
    portfolio = Portfolio(events)
    execution = ExecutionHandler(events)

    print("--- Starting Event-Driven Backtest ---")
    
    while True:
        # Update Data (Outer Loop Heartbeat)
        if not data.update_bars():
            if events.empty():
                break

        # Process Event Queue
        while not events.empty():
            event = events.get()

            if event.type == 'MARKET':
                strategy.on_market_data(event)
            elif event.type == 'SIGNAL':
                portfolio.on_signal(event)
            elif event.type == 'ORDER':
                execution.on_order(event)
            elif event.type == 'FILL':
                pass # Log fill, update portfolio holdings

if __name__ == "__main__":
    run_backtest()
