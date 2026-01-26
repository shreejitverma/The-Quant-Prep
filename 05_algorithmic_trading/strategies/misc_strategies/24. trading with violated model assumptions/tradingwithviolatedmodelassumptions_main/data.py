import pandas as pd
import numpy as np
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
from datetime import datetime, timedelta
import time
import threading
import csv
import os

class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}
        self.data_received = {}
        self.contracts = {}
        self.lock = threading.Lock()
        self.connected = False
        self.next_order_id = None
        
    def error(self, reqId, errorCode, errorString):
        print(f"Error {errorCode}: {errorString} for request {reqId}")
        if errorCode == 504:  # Not connected
            print("Connection lost. Please check TWS connection.")
        
    def nextValidId(self, orderId):
        self.next_order_id = orderId
        self.connected = True
        print("Connected to TWS successfully!")
        
    def historicalData(self, reqId, bar):
        with self.lock:
            if reqId not in self.data:
                self.data[reqId] = []
            self.data[reqId].append({
                'date': bar.date,
                'open': bar.open,
                'high': bar.high,
                'low': bar.low,
                'close': bar.close,
                'volume': bar.volume
            })
            
    def historicalDataEnd(self, reqId, start, end):
        with self.lock:
            self.data_received[reqId] = True
            symbol = self.contracts.get(reqId, f"Unknown-{reqId}")
            print(f"Historical data received for {symbol} (request {reqId})")

def create_contract(symbol, secType="STK", exchange="SMART", currency="USD"):
    """Create a contract for the given symbol"""
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract

def get_historical_data(app, symbol, contract, duration="3 Y", bar_size="1 day"):
    """Request historical data for a symbol"""
    reqId = len(app.contracts) + 1
    app.contracts[reqId] = symbol
    
    # Request historical data
    app.reqHistoricalData(
        reqId,
        contract,
        "",  # end time (empty for current time)
        duration,
        bar_size,
        "TRADES",
        1,  # useRTH
        1,  # formatDate
        False,  # keepUpToDate
        []  # chartOptions
    )
    
    return reqId

def calculate_daily_returns(df):
    """Calculate daily returns from price data"""
    df['return'] = df['close'].pct_change()
    return df[['date', 'return']]

def main():
    # Initialize the IB application
    app = IBApp()
    
    try:
        # Connect to TWS (make sure TWS is running and API connections are enabled)
        print("Connecting to TWS...")
        app.connect("127.0.0.1", 7497, 0)  # Use 7496 for paper trading
        
        # Start the message loop in a separate thread
        api_thread = threading.Thread(target=app.run, daemon=True)
        api_thread.start()
        
        # Wait for connection
        print("Waiting for connection...")
        timeout = 30  # 30 second timeout
        start_time = time.time()
        
        while not app.connected and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        if not app.connected:
            print("Failed to connect to TWS. Please check:")
            print("1. TWS is running")
            print("2. API connections are enabled")
            print("3. Port 7497 is correct (use 7496 for paper trading)")
            return
        
        # Wait a bit more for connection to stabilize
        time.sleep(2)
        
        # Define symbols to fetch (2022-2025 data)
        symbols = ['AMZN', 'AAPL', 'MSFT', 'GM', 'SPX']
        
        # Create contracts and request data
        reqIds = []
        for symbol in symbols:
            try:
                if symbol == 'SPX':
                    # SPX is an index, not a stock
                    contract = create_contract(symbol, secType="IND", exchange="CBOE")
                else:
                    contract = create_contract(symbol)
                
                reqId = get_historical_data(app, symbol, contract)
                reqIds.append(reqId)
                print(f"Requested data for {symbol}")
                time.sleep(0.5)  # Small delay between requests
                
            except Exception as e:
                print(f"Error requesting data for {symbol}: {e}")
        
        # Wait for all data to be received
        print("Waiting for historical data...")
        timeout = 120  # 2 minute timeout
        start_time = time.time()
        
        while not all(app.data_received.get(reqId, False) for reqId in reqIds):
            if (time.time() - start_time) > timeout:
                print("Timeout waiting for data. Some requests may have failed.")
                break
            time.sleep(1)
        
        print("Data collection completed!")
        
        # Process the data
        all_returns = {}
        
        for reqId in reqIds:
            symbol = app.contracts[reqId]
            if reqId in app.data and app.data[reqId]:
                # Convert to DataFrame
                df = pd.DataFrame(app.data[reqId])
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                # Filter for 2022-2025 data
                df = df[(df['date'] >= '2022-01-01') & (df['date'] <= '2025-12-31')]
                
                # Calculate returns
                returns_df = calculate_daily_returns(df)
                all_returns[symbol] = returns_df
                print(f"Processed {len(df)} data points for {symbol}")
            else:
                print(f"No data received for {symbol}")
        
        # Combine all returns into one DataFrame
        if all_returns:
            # Find the symbol with the most data points
            max_data_symbol = max(all_returns.keys(), key=lambda x: len(all_returns[x]))
            base_df = all_returns[max_data_symbol][['date']].copy()
            
            # Add returns for each symbol
            for symbol in symbols:
                if symbol in all_returns:
                    symbol_returns = all_returns[symbol].set_index('date')['return']
                    base_df[symbol] = base_df['date'].map(symbol_returns)
            
            # Remove rows with any NaN values (missing data)
            original_rows = len(base_df)
            base_df = base_df.dropna()
            print(f"Removed {original_rows - len(base_df)} rows with missing data")
            
            # Save to CSV
            output_file = 'daily_returns_2022_2025.csv'
            base_df.to_csv(output_file, index=False)
            print(f"Daily returns saved to {output_file}")
            print(f"Data shape: {base_df.shape}")
            print(f"Date range: {base_df['date'].min()} to {base_df['date'].max()}")
            
            # Display first few rows
            print("\nFirst few rows of data:")
            print(base_df.head())
            
            # Display summary statistics
            print("\nSummary statistics:")
            print(base_df.describe())
            
        else:
            print("No data received from IB")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Disconnect from TWS
        try:
            app.disconnect()
            print("Disconnected from TWS")
        except:
            pass

if __name__ == "__main__":
    main()
