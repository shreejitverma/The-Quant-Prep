import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ExecutionAlgorithms:
    """
    Standard Execution Algorithms used to minimize market impact.
    """
    
    def __init__(self, total_quantity, start_time, end_time, volume_profile=None):
        """
        :param total_quantity: Shares to buy/sell
        :param start_time: Index of start
        :param end_time: Index of end
        :param volume_profile: Expected market volume distribution (list or array) for VWAP
        """
        self.Q = total_quantity
        self.T_start = start_time
        self.T_end = end_time
        self.N = end_time - start_time
        self.volume_profile = volume_profile

    def get_twap_schedule(self):
        """
        Time-Weighted Average Price (TWAP):
        Slices the order equally across all time buckets.
        """
        quantity_per_slice = self.Q / self.N
        schedule = np.full(self.N, quantity_per_slice)
        return schedule

    def get_vwap_schedule(self):
        """
        Volume-Weighted Average Price (VWAP):
        Slices the order proportional to historical volume profile.
        """
        if self.volume_profile is None:
            raise ValueError("Volume profile required for VWAP")
        
        relevant_profile = np.array(self.volume_profile[self.T_start:self.T_end])
        total_market_vol = relevant_profile.sum()
        
        # Proportional allocation
        schedule = (relevant_profile / total_market_vol) * self.Q
        return schedule

if __name__ == "__main__":
    # Example: Execute 100,000 shares over a trading day (390 minutes)
    total_qty = 100000
    minutes = 390
    
    # Simulate a "U-Shape" volume profile (common in equities)
    # High volume at open/close, low in mid-day
    t = np.linspace(-1, 1, minutes)
    vol_profile = 1000 + 5000 * t**2 # Quadratic curve
    
    algo = ExecutionAlgorithms(total_qty, 0, minutes, vol_profile)
    
    twap = algo.get_twap_schedule()
    vwap = algo.get_vwap_schedule()
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(vol_profile, label='Market Volume Profile (Proxy)', linestyle='--', alpha=0.5)
    plt.plot(twap, label='TWAP Schedule', linewidth=2)
    plt.plot(vwap, label='VWAP Schedule', linewidth=2)
    plt.title('Execution Schedules: TWAP vs VWAP')
    plt.xlabel('Minute')
    plt.ylabel('Shares to Execute')
    plt.legend()
    plt.show()
