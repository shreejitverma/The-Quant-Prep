import unittest
import numpy as np

# A simple Moving Average Strategy for demonstration
class MovingAverageStrategy:
    def __init__(self, window):
        self.window = window
        self.prices = []

    def on_tick(self, price):
        self.prices.append(price)
        if len(self.prices) < self.window:
            return None # Not enough data

        avg = np.mean(self.prices[-self.window:])
        return "BUY" if price > avg else "SELL"

class TestMovingAverageStrategy(unittest.TestCase):
    def test_signal_generation(self):
        # Setup
        strategy = MovingAverageStrategy(window=3)
        prices = [100, 102, 101] # Avg = 101

        # Action
        for p in prices:
            strategy.on_tick(p)

        # Trigger
        # Next price 105 > Avg(102, 101, 105) -> 102.6 ?? No, it compares CURRENT price to PREV avg usually
        # Let's assume standard crossover: Price > SMA

        # Test Case 1: Price > Avg
        # Window: [102, 101, 105] -> Avg = 102.66. 105 > 102.66
        signal = strategy.on_tick(105)
        self.assertEqual(signal, "BUY")

    def test_window_buildup(self):
        strategy = MovingAverageStrategy(window=5)
        self.assertIsNone(strategy.on_tick(100))
        self.assertIsNone(strategy.on_tick(101))

if __name__ == '__main__':
    unittest.main()
