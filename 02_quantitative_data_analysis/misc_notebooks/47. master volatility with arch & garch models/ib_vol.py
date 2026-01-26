"""
AAPL Volatility Data Fetcher using Interactive Brokers API
This script fetches historical implied volatility and realized volatility data for AAPL
from 2023 to present and stores it in a CSV file.

Requirements:
- ibapi library
- pandas, numpy
- Active IB TWS or Gateway connection
"""

import pandas as pd
import numpy as np
import csv
import time
from datetime import datetime, timedelta
from threading import Event
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import TickerId


class VolatilityDataApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.historical_data = {}
        self.option_data = {}
        self.market_data = {}
        self.data_ready = Event()
        self.request_counter = 0
        self.completed_requests = set()
        self.total_requests = 0
        
    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        """Handle API errors with correct signature for newer API versions"""
        print(f"Error {errorCode}: {errorString}")
        if errorCode in [200, 162, 2104, 2106, 2158]:  # Non-critical errors
            return
        self.data_ready.set()
    
    def nextValidId(self, orderId):
        """Called when connection is established"""
        print(f"Connected. Next valid ID: {orderId}")
        self.start_data_collection()
    
    def historicalData(self, reqId, bar):
        """Called for each historical bar"""
        if reqId not in self.historical_data:
            self.historical_data[reqId] = []
        
        self.historical_data[reqId].append({
            'date': bar.date,
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume
        })
    
    def historicalDataEnd(self, reqId, start, end):
        """Called when historical data request is complete"""
        print(f"Historical data complete for request {reqId} ({len(self.completed_requests)+1}/{self.total_requests})")
        self.completed_requests.add(reqId)
        if len(self.completed_requests) >= self.total_requests:
            print("All data requests completed!")
            self.data_ready.set()
    
    def tickPrice(self, reqId, tickType, price, attrib):
        """Called for market data ticks"""
        if reqId not in self.market_data:
            self.market_data[reqId] = {}
        
        # Tick type 13 = Implied Volatility
        if tickType == 13:
            self.market_data[reqId]['implied_vol'] = price
            print(f"Implied Vol for {reqId}: {price}")
    
    def create_aapl_contract(self):
        """Create AAPL stock contract for implied volatility data
        
        AAPL is a regular stock that supports both TRADES and OPTION_IMPLIED_VOLATILITY
        data queries through the IB API.
        """
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract
    
    
    def start_data_collection(self):
        """Start collecting historical and volatility data"""
        print("Starting data collection...")
        
        # Request historical data for AAPL (for realized volatility calculation)
        aapl_contract = self.create_aapl_contract()
        
        # Define the full date range from 2023 to 2025
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2025, 12, 31)  # Full 2025 coverage
        current_end_date = datetime.now()  # Don't go beyond current date
        
        # Use the earlier of 2025-12-31 or current date
        actual_end_date = min(end_date, current_end_date)
        
        print(f"Collecting data from {start_date.strftime('%Y-%m-%d')} to {actual_end_date.strftime('%Y-%m-%d')}")
        
        # Use a simpler approach: request all data from current date going back
        # Then we'll filter it in post-processing to get only the 2023-2025 range
        total_days = (actual_end_date - start_date).days + 30  # Add buffer
        
        # IB API requires years format for durations > 365 days
        if total_days > 365:
            # Convert to years, rounding up to ensure we get enough data
            total_years = (total_days / 365.25) + 0.5  # Add buffer and account for leap years
            duration_str = f"{int(total_years)} Y"
            print(f"Using {duration_str} duration ({total_days} days)")
        else:
            duration_str = f"{total_days} D"
        
        # Use empty end date string to get most recent data going back
        end_date_str = ""  # Empty string gets current data
        
        print(f"Requesting {total_days} days of data going back from current date")
        
        req_id = 1
        
        # Request implied volatility data
        self.reqHistoricalData(
            req_id,
            aapl_contract,
            end_date_str,  # Empty string for current data
            duration_str,
            "1 day",  # Bar size
            "OPTION_IMPLIED_VOLATILITY",  # What to show - this gets implied volatility
            1,  # Use RTH
            1,  # Format date
            False,  # Keep up to date
            []
        )
        
        # Also request price data for realized volatility calculation
        price_req_id = req_id + 1000  # Offset to avoid conflicts
        self.reqHistoricalData(
            price_req_id,
            aapl_contract,
            end_date_str,  # Empty string for current data
            duration_str,
            "1 day",  # Bar size
            "TRADES",  # What to show - this gets price data
            1,  # Use RTH
            1,  # Format date
            False,  # Keep up to date
            []
        )
        
        self.total_requests = 2  # We're making 2 requests total
        
        # Note: Using OPTION_IMPLIED_VOLATILITY on AAPL provides historical IV data
        print(f"Total requests made: {self.total_requests}")
    
    def calculate_realized_volatility(self, price_data, window=30):
        """Calculate realized volatility from price data"""
        df = pd.DataFrame(price_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calculate daily returns
        df['returns'] = np.log(df['close'] / df['close'].shift(1))
        
        # Calculate rolling realized volatility (annualized)
        df[f'realized_vol_{window}d'] = df['returns'].rolling(window=window).std() * np.sqrt(252)
        
        return df
    
    def save_to_csv(self, filename="aapl_volatility_data_2023_2025.csv"):
        """Save collected data to CSV"""
        print("Processing and saving data to CSV...")
        
        # Define target date range for filtering
        target_start = datetime(2023, 1, 1)
        target_end = datetime(2025, 12, 31)
        current_date = datetime.now()
        actual_target_end = min(target_end, current_date)
        
        print(f"Filtering data to range: {target_start.strftime('%Y-%m-%d')} to {actual_target_end.strftime('%Y-%m-%d')}")
        
        # Separate price data and implied volatility data
        price_data = []
        iv_data = []
        
        for req_id, data in self.historical_data.items():
            if req_id < 1000:  # Original req_ids for implied volatility
                iv_data.extend(data)
            else:  # Offset req_ids for price data
                price_data.extend(data)
        
        if not iv_data:
            print("No implied volatility data collected!")
        
        if not price_data:
            print("No price data collected!")
        
        # Process implied volatility data with date filtering
        if iv_data:
            iv_df = pd.DataFrame(iv_data)
            iv_df['date'] = pd.to_datetime(iv_df['date'])
            # Filter to target date range
            iv_df = iv_df[(iv_df['date'] >= target_start) & (iv_df['date'] <= actual_target_end)]
            iv_df = iv_df.sort_values('date')
            # The 'close' field contains the implied volatility when using OPTION_IMPLIED_VOLATILITY
            iv_df['implied_vol'] = iv_df['close']
            iv_df = iv_df[['date', 'implied_vol']].drop_duplicates(subset=['date'])
            print(f"Implied volatility data after filtering: {len(iv_df)} records")
        else:
            iv_df = pd.DataFrame(columns=['date', 'implied_vol'])
        
        # Process price data for realized volatility with date filtering
        if price_data:
            # Filter price data first
            price_df_raw = pd.DataFrame(price_data)
            price_df_raw['date'] = pd.to_datetime(price_df_raw['date'])
            price_data_filtered = price_df_raw[(price_df_raw['date'] >= target_start) & (price_df_raw['date'] <= actual_target_end)]
            print(f"Price data after filtering: {len(price_data_filtered)} records")
            
            # Convert back to list format for calculate_realized_volatility function
            filtered_price_data = price_data_filtered.to_dict('records')
            vol_df = self.calculate_realized_volatility(filtered_price_data)
        else:
            vol_df = pd.DataFrame(columns=['date', 'close', 'returns', 'realized_vol_30d'])
        
        # Merge implied and realized volatility data
        if not iv_df.empty and not vol_df.empty:
            # Merge on date
            final_df = pd.merge(vol_df, iv_df, on='date', how='outer')
        elif not iv_df.empty:
            final_df = iv_df
        elif not vol_df.empty:
            final_df = vol_df
            final_df['implied_vol'] = np.nan
        else:
            print("No data collected in target date range!")
            return
        
        # Final date filtering and sorting
        final_df = final_df[(final_df['date'] >= target_start) & (final_df['date'] <= actual_target_end)]
        final_df = final_df.drop_duplicates(subset=['date']).sort_values('date')
        
        # Save to CSV
        final_df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        print(f"Data shape: {final_df.shape}")
        print(f"Date range in final data: {final_df['date'].min()} to {final_df['date'].max()}")
        print(f"Implied volatility data points: {final_df['implied_vol'].notna().sum()}")
        if 'realized_vol_30d' in final_df.columns:
            print(f"Realized volatility data points: {final_df['realized_vol_30d'].notna().sum()}")
        print("\nFirst few rows:")
        print(final_df.head())
        print("\nLast few rows:")
        print(final_df.tail())


def main():
    """Main function to run the volatility data collection"""
    print("AAPL Volatility Data Fetcher")
    print("=" * 50)
    
    app = VolatilityDataApp()
    
    # Connect to IB TWS/Gateway (default localhost:7497 for TWS, 4001 for Gateway)
    try:
        print("Connecting to Interactive Brokers...")
        app.connect("127.0.0.1", 7497, clientId=1)  # Change to 4001 for IB Gateway
        
        # Start the socket in a separate thread
        import threading
        api_thread = threading.Thread(target=app.run, daemon=True)
        api_thread.start()
        
        # Wait for data collection to complete
        print("Waiting for data collection to complete...")
        app.data_ready.wait(timeout=600)  # 10 minute timeout for larger dataset
        
        # Process and save data
        current_year = datetime.now().year
        app.save_to_csv(f"aapl_volatility_data_2023_2025.csv")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Disconnecting...")
        app.disconnect()


if __name__ == "__main__":
    main()
