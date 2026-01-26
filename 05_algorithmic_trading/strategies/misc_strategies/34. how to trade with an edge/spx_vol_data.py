#!/usr/bin/env python3
"""
Script to pull YTD data for SPY ETF and VIX using Interactive Brokers API
Saves data as CSV with columns: Date, SPY, VIX
"""

import pandas as pd
from datetime import datetime, timedelta
import time
import threading
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}
        self.data_received = {}
        
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"Error: {reqId}, {errorCode}, {errorString}")
        
    def historicalData(self, reqId, bar):
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
        print(f"Historical data end for request {reqId}")
        self.data_received[reqId] = True

class IBDataFetcher:
    def __init__(self, host='127.0.0.1', port=7497, clientId=1):
        """
        Initialize IB connection
        
        Args:
            host: IB TWS/Gateway host (default localhost)
            port: IB TWS/Gateway port (7497 for TWS, 7496 for Gateway)
            clientId: Unique client ID
        """
        self.app = IBApi()
        self.host = host
        self.port = port
        self.clientId = clientId
        
    def connect(self):
        """Connect to IB TWS or Gateway"""
        try:
            self.app.connect(self.host, self.port, self.clientId)
            
            # Start the socket in a thread
            api_thread = threading.Thread(target=self.run_loop, daemon=True)
            api_thread.start()
            
            # Wait for connection
            time.sleep(1)
            
            if self.app.isConnected():
                print(f"Connected to IB at {self.host}:{self.port}")
                return True
            else:
                print("Failed to connect to IB")
                return False
        except Exception as e:
            print(f"Failed to connect to IB: {e}")
            print("Make sure TWS or IB Gateway is running and API connections are enabled")
            return False
    
    def run_loop(self):
        """Run the message loop"""
        self.app.run()
    
    def disconnect(self):
        """Disconnect from IB"""
        self.app.disconnect()
        print("Disconnected from IB")
    
    def create_contract(self, symbol, sec_type, exchange, currency):
        """Create a contract object"""
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.exchange = exchange
        contract.currency = currency
        return contract
    
    def get_ytd_data(self):
        """
        Fetch YTD data for SPY and VIX
        
        Returns:
            pd.DataFrame: DataFrame with Date, SPY, VIX columns
        """
        # Define start of current year
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime.now()
        
        # Calculate duration string for IB API
        days_ytd = (end_date - start_date).days + 1
        duration = f"{days_ytd} D"
        
        print(f"Fetching YTD data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Define contracts
        spy_contract = self.create_contract('SPY', 'STK', 'SMART', 'USD')
        vix_contract = self.create_contract('VIX', 'IND', 'CBOE', 'USD')
        
        try:
            # Request historical data
            print("Fetching SPY data...")
            self.app.reqHistoricalData(
                1,  # reqId
                spy_contract,
                '',  # endDateTime (empty means current time)
                duration,
                '1 day',
                'TRADES',  # Use TRADES instead of MIDPOINT for SPY
                1,  # useRTH
                1,  # formatDate
                False,  # keepUpToDate
                []  # chartOptions
            )
            
            print("Fetching VIX data...")
            self.app.reqHistoricalData(
                2,  # reqId
                vix_contract,
                '',  # endDateTime
                duration,
                '1 day',
                'TRADES',  # Use TRADES for VIX as well
                1,  # useRTH
                1,  # formatDate
                False,  # keepUpToDate
                []  # chartOptions
            )
            
            # Wait for data to be received
            timeout = 30  # 30 seconds timeout
            start_time = time.time()
            
            while (1 not in self.app.data_received or 2 not in self.app.data_received):
                if time.time() - start_time > timeout:
                    print("Timeout waiting for data")
                    return None
                time.sleep(0.1)
            
            # Convert to DataFrames
            spy_data = self.app.data.get(1, [])
            vix_data = self.app.data.get(2, [])
            
            if not spy_data or not vix_data:
                print("No data received")
                return None
            
            spy_df = pd.DataFrame(spy_data)[['date', 'close']].rename(columns={'close': 'SPY'})
            vix_df = pd.DataFrame(vix_data)[['date', 'close']].rename(columns={'close': 'VIX'})
            
            # Convert date strings to datetime
            spy_df['date'] = pd.to_datetime(spy_df['date'])
            vix_df['date'] = pd.to_datetime(vix_df['date'])
            
            # Merge on date
            merged_df = pd.merge(spy_df, vix_df, on='date', how='outer')
            merged_df = merged_df.rename(columns={'date': 'Date'})
            
            # Sort by date and reset index
            merged_df = merged_df.sort_values('Date').reset_index(drop=True)
            
            print(f"Successfully fetched {len(merged_df)} days of data")
            return merged_df
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def save_to_csv(self, df, filename='spy_vix_ytd_data.csv'):
        """
        Save DataFrame to CSV
        
        Args:
            df: DataFrame to save
            filename: Output filename
        """
        try:
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

def main():
    """Main function to run the data fetching process"""
    # Initialize data fetcher
    # Note: Adjust port if needed (7496 for IB Gateway, 7497 for TWS)
    fetcher = IBDataFetcher(port=7497)
    
    # Connect to IB
    if not fetcher.connect():
        return
    
    try:
        # Get YTD data
        df = fetcher.get_ytd_data()
        
        if df is not None:
            # Display first few rows
            print("\nFirst 5 rows of data:")
            print(df.head())
            print(f"\nLast 5 rows of data:")
            print(df.tail())
            print(f"\nData shape: {df.shape}")
            print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
            
            # Save to CSV
            fetcher.save_to_csv(df)
            
        else:
            print("Failed to fetch data")
            
    except Exception as e:
        print(f"Error in main execution: {e}")
        
    finally:
        # Always disconnect
        fetcher.disconnect()

if __name__ == "__main__":
    main()
