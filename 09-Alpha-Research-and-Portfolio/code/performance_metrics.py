import numpy as np
import pandas as pd

class PerformanceMetrics:
    """
    Library for calculating Strategy Performance Metrics.
    """
    
    @staticmethod
    def calculate_returns(prices):
        """Calculates simple percent returns."""
        return prices.pct_change().dropna()

    @staticmethod
    def sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252):
        """
        Sharpe Ratio = (Mean Return - Risk Free) / Std Dev
        """
        excess_returns = returns - risk_free_rate / periods_per_year
        if returns.std() == 0:
            return 0.0
        return np.sqrt(periods_per_year) * excess_returns.mean() / returns.std()

    @staticmethod
    def sortino_ratio(returns, risk_free_rate=0.0, periods_per_year=252):
        """
        Sortino Ratio = (Mean Return - Risk Free) / Downside Deviation
        """
        excess_returns = returns - risk_free_rate / periods_per_year
        downside_returns = returns[returns < 0]
        
        downside_std = downside_returns.std()
        if downside_std == 0:
            return 0.0
            
        return np.sqrt(periods_per_year) * excess_returns.mean() / downside_std

    @staticmethod
    def max_drawdown(prices):
        """
        Calculates Maximum Drawdown (Peak to Valley).
        """
        cumulative = (1 + prices.pct_change().dropna()).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()

    @staticmethod
    def calmar_ratio(returns, prices, periods_per_year=252):
        """
        Calmar Ratio = Annualized Return / Max Drawdown
        """
        max_dd = abs(PerformanceMetrics.max_drawdown(prices))
        if max_dd == 0:
            return 0.0
            
        annual_return = returns.mean() * periods_per_year
        return annual_return / max_dd

if __name__ == "__main__":
    # Test Data
    prices = pd.Series([100, 102, 104, 103, 105, 108, 101, 103], name="Price")
    returns = PerformanceMetrics.calculate_returns(prices)
    
    print(f"Sharpe Ratio:   {PerformanceMetrics.sharpe_ratio(returns):.4f}")
    print(f"Sortino Ratio:  {PerformanceMetrics.sortino_ratio(returns):.4f}")
    print(f"Max Drawdown:   {PerformanceMetrics.max_drawdown(prices):.4f}")
    print(f"Calmar Ratio:   {PerformanceMetrics.calmar_ratio(returns, prices):.4f}")
