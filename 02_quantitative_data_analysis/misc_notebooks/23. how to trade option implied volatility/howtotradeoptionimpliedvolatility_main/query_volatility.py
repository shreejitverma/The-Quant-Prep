import pandas as pd
from datetime import datetime
import time
from threading import Thread, Event
import numpy as np  

# Import IB API classes
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class IBKRDataCollector(EWrapper, EClient):
    def __init__(self, host='127.0.0.1', port=7497, clientId=1):
        EClient.__init__(self, self)
        self.host = host
        self.port = port
        self.clientId = clientId

        self.data_storage = {
            'implied_volatility': [],
            'realized_volatility': [],
            'prices': [],  # Add storage for price data
            'custom_volatility': None  # Add storage for custom volatility measure
        }
        self.nextValidOrderId = None
        self.current_req_id = 1 # Starting request ID
        self.data_received_events = {} # Events to signal data completion

        print(f"Initializing IBKRDataCollector (EWrapper, EClient) with Client ID {self.clientId}...")

    def run(self):
        """Starts the API client's message loop in a separate thread."""
        self.runThread = Thread(target=self.runAPI, daemon=True)
        self.runThread.start()
        print("API client message loop started in a separate thread.")

    def runAPI(self):
        """Internal method to run the EClient event loop."""
        EClient.run(self)  # Call the parent class's run() method instead of self.run()

    def connect_to_tws(self):
        """Establishes connection to TWS/Gateway."""
        print(f"Attempting to connect to IB TWS/Gateway at {self.host}:{self.port}...")
        self.connect(self.host, self.port, self.clientId)
        if not self.isConnected():
            print("Failed to connect. Please ensure TWS/Gateway is running and API access is enabled.")
            return False
        print("Connected to IB TWS/Gateway.")
        # Start the API message processing loop in a separate thread
        self.run()
        # Wait for nextValidId to be received, indicating successful connection and initialization
        max_wait_time = 10
        start_time = time.time()
        while self.nextValidOrderId is None and (time.time() - start_time) < max_wait_time:
            time.sleep(0.1) # Small delay to avoid busy-waiting
        if self.nextValidOrderId is None:
            print(f"Timed out waiting for nextValidId after {max_wait_time} seconds. Connection may not be fully established.")
            return False
        print(f"Connection fully established. Next valid order ID: {self.nextValidOrderId}")
        return True

    def disconnect_from_tws(self):
        """Disconnects from TWS/Gateway."""
        if self.isConnected():
            self.disconnect()
            print("Disconnected from IB TWS/Gateway.")
        else:
            print("Not connected to IB TWS/Gateway.")

    # EWrapper methods (callbacks)

    def nextValidId(self, orderId: int):
        """Callback for the next valid order ID, indicates successful connection."""
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print(f"Received next valid order ID: {orderId}")

    def historicalData(self, reqId: int, bar):
        """Callback for receiving historical data bars."""
        if reqId == self.current_req_id - 3:  # Price data request ID
            self.data_storage['prices'].append({
                'date': datetime.strptime(bar.date, '%Y%m%d'),
                'close': bar.close
            })
        elif reqId == self.current_req_id - 2:  # Implied Volatility request ID
            self.data_storage['implied_volatility'].append({
                'date': datetime.strptime(bar.date, '%Y%m%d'),
                'close': bar.close
            })
        elif reqId == self.current_req_id - 1:  # Realized Volatility request ID
            self.data_storage['realized_volatility'].append({
                'date': datetime.strptime(bar.date, '%Y%m%d'),
                'close': bar.close
            })

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        """Callback indicating the end of a historical data request."""
        print(f"HistoricalDataEnd. ReqId: {reqId} from {start} to {end}")
        if reqId in self.data_received_events:
            self.data_received_events[reqId].set() # Signal that data for this reqId is complete

    def error(self, reqId: int, errorCode: int, errorString: str):
        """Callback for API errors."""
        super().error(reqId, errorCode, errorString)
        print(f"Error. Id: {reqId}, Code: {errorCode}, Msg: {errorString}")
        # If an error occurs, also set the event to unblock if waiting
        if reqId in self.data_received_events:
            self.data_received_events[reqId].set()

    # Public method to request data

    def calculate_custom_volatility(self, prices_df):
        """
        Calculate custom volatility measure using 30-day lookback period and annualization.
        
        Args:
            prices_df (pd.DataFrame): DataFrame with daily closing prices
        
        Returns:
            pd.Series: Custom volatility measure
        """
        # Calculate daily returns
        daily_returns = prices_df['close'].pct_change()
        
        # Calculate 30-day rolling standard deviation
        rolling_std = daily_returns.rolling(window=30).std()
        
        # Annualize the volatility (multiply by sqrt(252) for daily data)
        custom_volatility = rolling_std * np.sqrt(252)
        
        return custom_volatility.rename('Custom Volatility')

    def get_historical_volatility_data(self, symbol: str, duration_str: str, bar_size_setting: str):
        """
        Pulls historical implied and realized volatility for a given symbol.

        Args:
            symbol (str): The ticker symbol (e.g., 'NVDA').
            duration_str (str): The duration to go back (e.g., '1 Y' for 1 year).
            bar_size_setting (str): The granularity of the data (e.g., '1 day').
        """
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        # Increment request ID for each new request
        price_req_id = self.current_req_id
        self.current_req_id += 1
        iv_req_id = self.current_req_id
        self.current_req_id += 1
        hv_req_id = self.current_req_id
        self.current_req_id += 1

        # Create events for each request to wait for completion
        self.data_received_events[price_req_id] = Event()
        self.data_received_events[iv_req_id] = Event()
        self.data_received_events[hv_req_id] = Event()

        # --- Request Historical Price Data ---
        print(f"\nRequesting historical price data for {symbol} (ReqId: {price_req_id})...")
        self.reqHistoricalData(
            reqId=price_req_id,
            contract=contract,
            endDateTime='',
            durationStr=duration_str,
            barSizeSetting=bar_size_setting,
            whatToShow='TRADES',  # Get actual trade prices
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[]
        )

        # Wait for the price data to be received
        print(f"Waiting for price data (ReqId: {price_req_id})...")
        if not self.data_received_events[price_req_id].wait(timeout=30):
            print(f"Timeout waiting for price data (ReqId: {price_req_id}).")
        else:
            print(f"Price data received for ReqId: {price_req_id}.")

        # --- Request Historical Implied Volatility ---
        print(f"\nRequesting historical implied volatility for {symbol} (ReqId: {iv_req_id})...")
        self.reqHistoricalData(
            reqId=iv_req_id,
            contract=contract,
            endDateTime='', # Empty string for current time (now)
            durationStr=duration_str,
            barSizeSetting=bar_size_setting,
            whatToShow='OPTION_IMPLIED_VOLATILITY', # Specific for implied volatility
            useRTH=1, # Use Regular Trading Hours (1 for True)
            formatDate=1, # Date format (1 for yyyymmdd)
            keepUpToDate=False,
            chartOptions=[]
        )

        # Wait for the implied volatility data to be received
        print(f"Waiting for implied volatility data (ReqId: {iv_req_id})...")
        if not self.data_received_events[iv_req_id].wait(timeout=30): # Wait with a timeout
            print(f"Timeout waiting for implied volatility data (ReqId: {iv_req_id}).")
        else:
            print(f"Implied volatility data received for ReqId: {iv_req_id}.")


        # --- Request Historical Realized Volatility ---
        # Note: The 'HISTORICAL_VOLATILITY' whatToShow option directly provides the 30-day historical volatility.
        print(f"\nRequesting historical realized volatility for {symbol} (ReqId: {hv_req_id})...")
        self.reqHistoricalData(
            reqId=hv_req_id,
            contract=contract,
            endDateTime='',
            durationStr=duration_str,
            barSizeSetting=bar_size_setting,
            whatToShow='HISTORICAL_VOLATILITY', # Specific for historical/realized volatility
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[]
        )

        # Wait for the realized volatility data to be received
        print(f"Waiting for realized volatility data (ReqId: {hv_req_id})...")
        if not self.data_received_events[hv_req_id].wait(timeout=30): # Wait with a timeout
            print(f"Timeout waiting for realized volatility data (ReqId: {hv_req_id}).")
        else:
            print(f"Realized volatility data received for ReqId: {hv_req_id}.")


        # Process collected data into pandas Series
        if self.data_storage['prices']:
            prices_df = pd.DataFrame(self.data_storage['prices'])
            prices_df.set_index('date', inplace=True)
            
            # Calculate custom volatility measure
            self.data_storage['custom_volatility'] = self.calculate_custom_volatility(prices_df)
            print("\nCalculated custom volatility measure.")
            print("Sample Custom Volatility Data:")
            print(self.data_storage['custom_volatility'].tail())

        if self.data_storage['implied_volatility']:
            iv_df = pd.DataFrame(self.data_storage['implied_volatility'])
            iv_df.set_index('date', inplace=True)
            self.data_storage['implied_volatility'] = iv_df['close'].rename('Implied Volatility')
            print(f"\nRetrieved {len(iv_df)} implied volatility data points.")
            print("Sample Implied Volatility Data:")
            print(self.data_storage['implied_volatility'].tail())
        else:
            print("\nNo implied volatility data retrieved.")

        if self.data_storage['realized_volatility']:
            hv_df = pd.DataFrame(self.data_storage['realized_volatility'])
            hv_df.set_index('date', inplace=True)
            self.data_storage['realized_volatility'] = hv_df['close'].rename('Realized Volatility')
            print(f"\nRetrieved {len(hv_df)} realized volatility data points.")
            print("Sample Realized Volatility Data:")
            print(self.data_storage['realized_volatility'].tail())
        else:
            print("\nNo historical volatility data retrieved.")

        return self.data_storage

# --- How to run this example ---
def main():
    collector = IBKRDataCollector()
    
    # 1. Start the API client's message loop in a separate thread
    collector.run()

    # 2. Connect to TWS/Gateway
    if not collector.connect_to_tws():
        print("Exiting due to connection failure.")
        return

    try:
        # 3. Request historical volatility data
        data = collector.get_historical_volatility_data(
            symbol='NVDA',
            duration_str='5 Y', # 5 Years of data
            bar_size_setting='1 day' # Daily bars
        )

        print("\n--- Final Summary of Retrieved Data ---")
        if not data['implied_volatility'].empty:
            print(f"Implied Volatility Data (last 5):")
            print(data['implied_volatility'].tail())
            # Save implied volatility to CSV
            data['implied_volatility'].to_csv('implied_volatility_5y.csv')
            print("Implied volatility data saved to 'implied_volatility_5y.csv'")
            
        if not data['realized_volatility'].empty:
            print(f"Realized Volatility Data (last 5):")
            print(data['realized_volatility'].tail())
            # Save realized volatility to CSV
            data['realized_volatility'].to_csv('realized_volatility_5y.csv')
            print("Realized volatility data saved to 'realized_volatility_5y.csv'")

        if data['custom_volatility'] is not None:
            print(f"\nCustom Volatility Data (last 5):")
            print(data['custom_volatility'].tail())
            # Save custom volatility to CSV
            data['custom_volatility'].to_csv('custom_volatility_5y.csv')
            print("Custom volatility data saved to 'custom_volatility_5y.csv'")
        else:
            print("No data retrieved.")

    except Exception as e:
        print(f"An error occurred during data retrieval: {e}")
    finally:
        # 4. Disconnect from TWS/Gateway
        collector.disconnect_from_tws()

if __name__ == '__main__':
    main()

