"""
Author: Shreejit Verma (GitHub: shreejitverma)
Organization: Quant Guild
Title: Quant Guild - Live Volatility Surface
Description: Real-time visualization of the implied volatility surface using IBKR API.
"""

# Import threading for non-blocking API communication
import threading

# Import time for sleep intervals and timestamps
import time

# Import pandas for data manipulation and pivot tables
import pandas as pd

# Import numpy for grid generation and numerical operations
import numpy as np

# Import matplotlib for 2D and 3D visualization
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Import Button widget for UI interactivity
from matplotlib.widgets import Button

# Import Interactive Brokers API components
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

# Use dark background style for a professional terminal aesthetic
plt.style.use('dark_background')

# --- IBKR Application Class ---
# Inherits from EWrapper (to receive data) and EClient (to send requests)
class LiveSurfaceApp(EWrapper, EClient):
    def __init__(self):
        # Initialize the API client
        EClient.__init__(self, self)
        # Dictionary to store Implied Volatility values keyed by request ID
        self.iv_dict = {}
        # Map request IDs to (Expiration, Strike) tuples
        self.id_map = {}
        # Lists to hold available option chain parameters
        self.expirations = []
        self.strikes = []
        # Variables to track the underlying asset state
        self.spot_price = 0
        self.underlying_conId = 0
        # Threading events to manage asynchronous data flow
        self.resolved = threading.Event()
        self.chain_resolved = threading.Event()

    # Callback triggered when connection to TWS/Gateway is successful
    def connectAck(self):
        print("TWS Acknowledged Connection")

    # Error handling callback to filter out standard connectivity notifications
    def error(self, reqId, errorCode, errorString):
        if errorCode not in [2104, 2106, 2158]:
            print(f"IBKR Msg {reqId}: {errorCode} - {errorString}")

    # Callback receiving contract details like the unique contract ID (conId)
    def contractDetails(self, reqId, contractDetails):
        self.underlying_conId = contractDetails.contract.conId
        self.resolved.set()

    # Callback receiving real-time price ticks for the underlying asset
    def tickPrice(self, reqId, tickType, price, attrib):
        # tickType 4 is Last Price, 9 is Close Price
        if reqId == 999 and tickType in [4, 9] and price > 0:
            self.spot_price = price

    # Callback receiving the list of strikes and expirations for the asset
    def securityDefinitionOptionParameter(self, reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes):
        if exchange == "SMART":
            self.expirations = sorted(list(expirations))
            self.strikes = sorted(list(strikes))
            self.chain_resolved.set()

    # Callback receiving calculated greeks and IV from the IBKR model
    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        # tickType 13 is the model's Implied Volatility calculation
        if tickType == 13 and impliedVol is not None:
            self.iv_dict[reqId] = impliedVol

# Wrapper function to run the client messaging loop
def run_loop(app):
    app.run()

# Setup and initialization logic for the trading application
def start_app(symbol='SPY'):
    # Instantiate the app and connect to TWS (Default port 7497)
    app = LiveSurfaceApp()
    app.connect('127.0.0.1', 7497, clientId=35)

    # Start the API message loop in a background thread
    api_thread = threading.Thread(target=run_loop, args=(app,), daemon=True)
    api_thread.start()
    time.sleep(1)

    # Define the underlying stock contract
    underlying = Contract()
    underlying.symbol = symbol
    underlying.secType = 'STK'
    underlying.exchange = 'SMART'
    underlying.currency = 'USD'

    # Request contract details to find the internal conId
    app.reqContractDetails(1, underlying)
    app.resolved.wait(timeout=5)

    # Request streaming market data for the spot price
    app.reqMktData(999, underlying, "", False, False, [])
    while app.spot_price == 0: time.sleep(0.1)
    spot = app.spot_price

    # Request the option chain parameters (strikes/expirations)
    app.reqSecDefOptParams(2, symbol, "", "STK", app.underlying_conId)
    app.chain_resolved.wait(timeout=5)

    # Filter for the next 6 expirations and strikes within 2% of spot
    today = time.strftime('%Y%m%d')
    target_exps = [e for e in app.expirations if e >= today][:6]
    target_strikes = [s for s in app.strikes if spot * 0.98 <= s <= spot * 1.02]

    # Iterate through filtered chain and request IV for each contract
    req_id = 1000
    for exp in target_exps:
        for strike in target_strikes:
            opt = Contract()
            opt.symbol = symbol
            opt.secType = 'OPT'
            opt.exchange = 'SMART'
            opt.currency = 'USD'
            opt.lastTradeDateOrContractMonth = exp
            opt.strike = strike
            # Use Calls for OTM/ITM split based on spot
            opt.right = 'C' if strike >= spot else 'P'
            app.id_map[req_id] = (exp, strike)
            # Generic tick tag "106" requests IV data
            app.reqMktData(req_id, opt, "106", False, False, [])
            req_id += 1
            time.sleep(0.01) # Avoid rate-limiting the API
    return app

# Helper class to manage UI state for the plot
class PlotState:
    def __init__(self):
        self.is_locked = False

    # Function to toggle data updates on/off via button
    def toggle(self, event):
        self.is_locked = not self.is_locked
        btn_label.set_text("UNLOCK UPDATES" if self.is_locked else "LOCK UPDATES")
        plt.draw()

# Main visualization loop
def live_desktop_plot(app):
    # Enable interactive mode for real-time updates
    plt.ion()
    fig = plt.figure(figsize=(16, 9))
    fig.canvas.manager.set_window_title('Quant Guild - Live Volatility Surface')
    fig.patch.set_facecolor('#0b0d0f')

    # Define subplots: 3D Surface on left, 2D Skew on right
    ax_3d = plt.subplot2grid((1, 3), (0, 0), colspan=2, projection='3d')
    ax_skew = plt.subplot2grid((1, 3), (0, 2))

    # Initialize UI Button for locking/unlocking the view
    state = PlotState()
    ax_button = plt.axes([0.42, 0.03, 0.12, 0.04])
    global btn_label
    btn = Button(ax_button, 'LOCK UPDATES', color='#1f2329', hovercolor='#2d333b')
    btn_label = btn.label
    btn_label.set_color('white')
    btn_label.set_fontsize(9)
    btn.on_clicked(state.toggle)

    print("--- Quant Guild Desktop Live Mode Started ---")

    try:
        while True:
            # Check if UI is not locked before refreshing data
            if not state.is_locked:
                current_data = []
                # Snapshot the current IV dictionary keys to iterate safely
                req_ids = list(app.iv_dict.keys())
                for rid in req_ids:
                    iv = app.iv_dict[rid]
                    exp, strike = app.id_map[rid]
                    current_data.append({'Expiry': exp, 'Strike': strike, 'IV': iv})

                # Minimum data threshold to build a meaningful surface
                if len(current_data) > 10:
                    # Convert to DataFrame and Pivot to create a grid
                    df = pd.DataFrame(current_data)
                    pivot = df.pivot_table(index='Expiry', columns='Strike', values='IV').sort_index().sort_index(axis=1)
                    # Fill missing data points using linear interpolation
                    pivot = pivot.interpolate(method='linear', axis=0).bfill().ffill()

                    # Create coordinate meshes for 3D plotting
                    X, Y_idx = np.meshgrid(pivot.columns, np.arange(len(pivot.index)))
                    Z = pivot.values

                    # Save current camera angle to prevent reset during redraw
                    curr_elev, curr_azim = ax_3d.elev, ax_3d.azim

                    # Redraw the 3D IV Surface
                    ax_3d.clear()
                    ax_3d.set_facecolor('#0b0d0f')
                    ax_3d.plot_surface(X, Y_idx, Z, cmap='magma', edgecolor='white', lw=0.1, alpha=0.9)

                    # Format 3D axis labels and title
                    ax_3d.set_yticks(np.arange(len(pivot.index)))
                    ax_3d.set_yticklabels(pivot.index, fontsize=8)
                    ax_3d.set_title(f"LIVE IV SURFACE | {time.strftime('%H:%M:%S')}", color='white')
                    ax_3d.view_init(elev=curr_elev, azim=curr_azim)

                    # Redraw the 2D Skew for the nearest expiration
                    ax_skew.clear()
                    ax_skew.set_facecolor('#161b22')
                    nearest_exp = pivot.index[0]
                    skew_data = pivot.iloc[0]

                    # Plot IV vs Strike and indicate the spot price line
                    ax_skew.plot(skew_data.index, skew_data.values, marker='o', color='#00f2ff')
                    ax_skew.axvline(x=app.spot_price, color='#ff3e3e', linestyle='--')
                    ax_skew.set_title(f"FRONT-MONTH SKEW: {nearest_exp}", color='white')

            # Pause to allow Matplotlib to process the drawing events
            plt.pause(0.5)

    except KeyboardInterrupt:
        # Graceful shutdown on manual interruption
        app.disconnect()
        plt.close()

# Main entry point
if __name__ == "__main__":
    # Start the app for SPY
    app_instance = start_app('SPY')
    print("App Started")
    # Buffer time to allow data to populate before plotting
    time.sleep(10)
    live_desktop_plot(app_instance)
