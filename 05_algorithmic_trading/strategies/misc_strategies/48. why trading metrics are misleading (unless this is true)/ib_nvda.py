#!/usr/bin/env python3
"""
NVDA Returns Fetcher using Interactive Brokers API
Fetches NVDA historical data for 2025 YTD and calculates returns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import threading
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData


class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []
        self.data_ready = threading.Event()
        
    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"Error {errorCode}: {errorString}")
        if errorCode in [200, 162]:  # No security definition found / Historical Market Data Service error
            self.data_ready.set()
            
    def historicalData(self, reqId, bar: BarData):
        """Called when historical data is received"""
        bar_data = {
            'Date': bar.date,
            'Open': bar.open,
            'High': bar.high,
            'Low': bar.low,
            'Close': bar.close,
            'Volume': bar.volume
        }
        self.data.append(bar_data)
        
    def historicalDataEnd(self, reqId, start, end):
        """Called when all historical data has been received"""
        print(f"Historical data complete. Received {len(self.data)} bars from {start} to {end}")
        self.data_ready.set()


def create_nvda_contract():
    """Create NVDA stock contract"""
    contract = Contract()
    contract.symbol = "NVDA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    return contract


def calculate_returns(df):
    """Calculate daily returns from price data"""
    # Calculate simple returns
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Calculate log returns
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # Drop the first row with NaN return
    df = df.dropna()
    
    return df


def main():
    print("Starting NVDA Returns Fetcher...")
    
    # Create IB API connection
    app = IBApp()
    
    # Connect to TWS/IB Gateway (default localhost:7497 for TWS paper trading)
    # Use port 7496 for TWS live, 4002 for IB Gateway paper, 4001 for IB Gateway live
    try:
        print("Connecting to Interactive Brokers...")
        app.connect("127.0.0.1", 7497, clientId=1)
        
        # Start the socket in a thread
        api_thread = threading.Thread(target=app.run, daemon=True)
        api_thread.start()
        
        # Wait a moment for connection
        time.sleep(2)
        
        if not app.isConnected():
            print("Failed to connect to IB. Please ensure TWS/IB Gateway is running.")
            return
            
        print("Connected successfully!")
        
        # Create NVDA contract
        nvda_contract = create_nvda_contract()
        
        # Calculate date range for 2025 YTD
        start_date = "20250101"
        end_date = datetime.now().strftime("%Y%m%d")
        
        print(f"Requesting NVDA data from {start_date} to {end_date}")
        
        # Request historical data
        # Parameters: reqId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions
        app.reqHistoricalData(
            reqId=1,
            contract=nvda_contract,
            endDateTime="",  # Empty string means current time
            durationStr="1 Y",  # 1 year back from current date
            barSizeSetting="1 day",
            whatToShow="TRADES",
            useRTH=1,  # Regular trading hours only
            formatDate=1,  # yyyyMMdd HH:mm:ss format
            keepUpToDate=False,
            chartOptions=[]
        )
        
        # Wait for data to be received
        print("Waiting for data...")
        app.data_ready.wait(timeout=30)  # 30 second timeout
        
        if not app.data:
            print("No data received. Please check your connection and contract details.")
            app.disconnect()
            return
            
        print(f"Received {len(app.data)} data points")
        
        # Convert to DataFrame
        df = pd.DataFrame(app.data)
        
        # Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Filter for 2025 YTD only
        df_2025 = df[df['Date'] >= '2025-01-01'].copy()
        
        if df_2025.empty:
            print("No data available for 2025 YTD")
            app.disconnect()
            return
        
        print(f"Filtered to {len(df_2025)} data points for 2025 YTD")
        
        # Sort by date
        df_2025 = df_2025.sort_values('Date').reset_index(drop=True)
        
        # Calculate returns
        df_returns = calculate_returns(df_2025)
        
        # Prepare final dataset
        results_df = df_returns[['Date', 'Close', 'Daily_Return', 'Log_Return']].copy()
        results_df.columns = ['Date', 'Close_Price', 'Daily_Return', 'Log_Return']
        
        # Save to CSV
        output_file = "nvda_returns_2025_ytd.csv"
        results_df.to_csv(output_file, index=False)
        
        print(f"\nData saved to {output_file}")
        print(f"Date range: {results_df['Date'].min().date()} to {results_df['Date'].max().date()}")
        print(f"Number of trading days: {len(results_df)}")
        print(f"Average daily return: {results_df['Daily_Return'].mean():.4f} ({results_df['Daily_Return'].mean()*100:.2f}%)")
        print(f"Daily return std: {results_df['Daily_Return'].std():.4f} ({results_df['Daily_Return'].std()*100:.2f}%)")
        print(f"YTD cumulative return: {(results_df['Daily_Return'] + 1).prod() - 1:.4f} ({((results_df['Daily_Return'] + 1).prod() - 1)*100:.2f}%)")
        
        # Display first few rows
        print("\nFirst 5 rows of data:")
        print(results_df.head())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if app.isConnected():
            app.disconnect()
        print("Disconnected from IB")


if __name__ == "__main__":
    main()
