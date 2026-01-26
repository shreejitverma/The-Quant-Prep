# =============================================================================
# IMPORTS
# =============================================================================
import tkinter as tk                                    # GUI framework
from tkinter import ttk, messagebox                     # Themed widgets and dialogs
import threading                                        # For background threads (IB connection, bar management)
import time                                             # Sleep and timing functions
from collections import deque                           # Fixed-size queue for rolling data
from datetime import datetime                           # Timestamps for bars
import numpy as np                                      # Numerical operations for regime model
import matplotlib.pyplot as plt                         # Plotting library
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Embed matplotlib in tkinter
from matplotlib.patches import Rectangle               # Draw candlestick bodies and regime backgrounds
import matplotlib.dates as mdates                       # Date formatting for axes
from ibapi.client import EClient                        # IB API client for sending requests
from ibapi.wrapper import EWrapper                      # IB API wrapper for receiving responses
from ibapi.contract import Contract                     # Define financial instruments
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


# =============================================================================
# INTERACTIVE BROKERS API WRAPPER
# =============================================================================
class IBApp(EWrapper, EClient):
    """Handles communication with TWS - inherits from both EWrapper (callbacks) and EClient (requests)."""

    def __init__(self, callback=None):
        EClient.__init__(self, self)
        self.connected = False                          # Connection status flag
        self.callback = callback                        # Function to call when tick data arrives
        self.last_price = None                          # Most recent trade price
        self.bid_price = None                           # Current bid price
        self.ask_price = None                           # Current ask price
        self.historical_data = {}                       # Store historical bars by request ID
        self.hist_done = threading.Event()              # Signal when historical data is complete

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        # Ignore common non-error messages (connection confirmations, data farm status)
        if errorCode in [2104, 2106, 2158, 2176]:
            return
        # Note when using delayed (free) market data instead of real-time
        if errorCode == 10167:
            print(f"Note: Using delayed market data")
            return
        print(f"Error {reqId}: {errorCode} - {errorString}")

    def nextValidId(self, orderId):
        # Called when connection is established - TWS sends first valid order ID
        self.connected = True
        print("Connected to TWS")

    def historicalData(self, reqId, bar):
        # Called for each bar of historical data - store OHLC values
        if reqId not in self.historical_data:
            self.historical_data[reqId] = []
        self.historical_data[reqId].append({'o': bar.open, 'h': bar.high, 'l': bar.low, 'c': bar.close})

    def historicalDataEnd(self, reqId, start, end):
        # Called when all historical data has been received - signal completion
        self.hist_done.set()

    def tickPrice(self, reqId, tickType, price, attrib):
        # Called when a price tick arrives from live market data stream
        if price <= 0:
            return
        # tickType codes: 1=Bid, 2=Ask, 4=Last, 6=High, 7=Low, 9=Close
        if tickType == 4:                               # Last traded price
            self.last_price = price
            if self.callback:
                self.callback('price', price, datetime.now())
        elif tickType == 1:                             # Bid price
            self.bid_price = price
        elif tickType == 2:                             # Ask price
            self.ask_price = price

    def tickSize(self, reqId, tickType, size):
        # Called for volume/size ticks - not used in this application
        pass

    def tickString(self, reqId, tickType, value):
        # Called for string tick data (e.g., last trade time) - not used
        pass


# =============================================================================
# OHLC BAR DATA STRUCTURE
# =============================================================================
class OHLCBar:
    """Represents a single OHLC (Open-High-Low-Close) candlestick bar."""
    
    def __init__(self, timestamp, open_price):
        self.timestamp = timestamp                      # When bar started
        self.open = open_price                          # First price in bar
        self.high = open_price                          # Highest price seen
        self.low = open_price                           # Lowest price seen
        self.close = open_price                         # Most recent price (updates with each tick)
        self.tick_count = 1                             # Number of ticks in this bar
        self.regime = 0                                 # Volatility regime: 0=low, 1=med, 2=high

    def update(self, price):
        # Update bar with new tick - adjust high/low/close accordingly
        self.high = max(self.high, price)
        self.low = min(self.low, price)
        self.close = price
        self.tick_count += 1

    @property
    def volatility(self):
        # Bar volatility = price range as percentage of close price
        return (self.high - self.low) / self.close if self.close > 0 else 0


# =============================================================================
# MARKOV REGIME MODEL
# =============================================================================
# A Hidden Markov Model (HMM) treats the market regime as a "hidden" state that
# we cannot directly observe. Instead, we observe volatility and must infer
# which regime we're in based on:
#   1. The TRANSITION MATRIX: How likely is it to switch between regimes?
#   2. The EMISSION MODEL: What volatility do we expect to see in each regime?
# 
# The model works by maintaining a probability distribution over regimes and
# updating it each time we observe a new bar's volatility using Bayesian inference.
# =============================================================================
class MarkovRegime:
    
    def __init__(self):
        pass

    def calibrate(self, hist_bars):
        pass

    def _gaussian_likelihood(self, vol, regime):
        pass

    def get_regime(self, bars):
        pass


# =============================================================================
# MAIN DASHBOARD APPLICATION
# =============================================================================
class LiveMarketDashboard:
    """Main application - live market data dashboard with rolling OHLC chart and regime detection."""

    def __init__(self, root):
        self.root = root
        self.root.title("Live Market Data Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0d1117')               # Dark background

        # Initialize dark theme styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_dark_theme()

        # Create IB API instance with callback for tick data
        self.ib_app = IBApp(callback=self.on_tick_data)
        self.connected = False                          # TWS connection status
        self.streaming = False                          # Market data streaming status

        # Data storage configuration
        self.bar_duration = 5                           # Seconds per OHLC bar
        self.max_bars = 10                              # Maximum bars to display (rolling window)
        self.ohlc_bars = deque(maxlen=self.max_bars)   # Completed bars
        self.current_bar = None                         # Bar currently being built
        self.bar_start_time = None                      # When current bar started
        self.price_history = deque(maxlen=100)         # Recent tick prices
        self.last_update_time = None
        self.regime_model = MarkovRegime()             # Volatility regime classifier

        # Thread synchronization
        self.bar_lock = threading.Lock()               # Protect bar data from race conditions
        self.update_thread = None                       # Background thread for bar management
        self.running = False                            # Control flag for loops

        # Build UI and chart
        self.setup_ui()
        self.setup_chart()

    def configure_dark_theme(self):
        # Apply GitHub-inspired dark theme to ttk widgets
        bg_color = '#0d1117'                            # Main background
        fg_color = '#c9d1d9'                            # Text color
        accent_color = '#238636'                        # Button accent (green)
        entry_bg = '#161b22'                            # Input field background

        # Configure each widget type
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        self.style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color,
                            font=('Segoe UI', 10, 'bold'))
        self.style.configure('TLabel', background=bg_color, foreground=fg_color,
                            font=('Segoe UI', 10))
        self.style.configure('TButton', background=accent_color, foreground='white',
                            font=('Segoe UI', 9, 'bold'), padding=(10, 5))
        self.style.map('TButton',
                      background=[('active', '#2ea043'), ('disabled', '#21262d')])
        self.style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color,
                            insertcolor=fg_color)
        # Red accent style for stop/disconnect buttons
        self.style.configure('Accent.TButton', background='#da3633', foreground='white')
        self.style.map('Accent.TButton',
                      background=[('active', '#f85149'), ('disabled', '#21262d')])

    def setup_ui(self):
        # Build the user interface layout
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure grid weights for responsive resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)            # Chart row expands

        # ----- HEADER SECTION -----
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))

        # Application title
        title_label = tk.Label(header_frame, text="◈ LIVE REGIME SWITCHING", 
                              font=('JetBrains Mono', 18, 'bold'),
                              bg='#0d1117', fg='#58a6ff')
        title_label.pack(side='left')

        # Connection status indicator (red=disconnected, green=connected, blue=streaming)
        self.status_indicator = tk.Label(header_frame, text="● DISCONNECTED",
                                        font=('Segoe UI', 10, 'bold'),
                                        bg='#0d1117', fg='#f85149')
        self.status_indicator.pack(side='right', padx=10)

        # ----- CONTROL PANEL -----
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.grid(row=1, column=0, sticky='ew', pady=(0, 15))

        # Connection inputs (host and port)
        conn_section = ttk.Frame(control_frame)
        conn_section.pack(fill='x', pady=(0, 10))

        ttk.Label(conn_section, text="Host:").pack(side='left', padx=(0, 5))
        self.host_var = tk.StringVar(value="127.0.0.1") # TWS default host
        host_entry = ttk.Entry(conn_section, textvariable=self.host_var, width=12)
        host_entry.pack(side='left', padx=(0, 15))

        ttk.Label(conn_section, text="Port:").pack(side='left', padx=(0, 5))
        self.port_var = tk.StringVar(value="7497")      # 7497=paper, 7496=live
        port_entry = ttk.Entry(conn_section, textvariable=self.port_var, width=8)
        port_entry.pack(side='left', padx=(0, 15))

        # Connect/Disconnect buttons
        self.connect_btn = ttk.Button(conn_section, text="Connect", command=self.connect_ib)
        self.connect_btn.pack(side='left', padx=(0, 5))

        self.disconnect_btn = ttk.Button(conn_section, text="Disconnect", 
                                         command=self.disconnect_ib, state='disabled',
                                         style='Accent.TButton')
        self.disconnect_btn.pack(side='left')

        # Visual separator between connection and data sections
        sep = ttk.Separator(control_frame, orient='horizontal')
        sep.pack(fill='x', pady=10)

        # ----- DATA STREAMING SECTION -----
        data_section = ttk.Frame(control_frame)
        data_section.pack(fill='x')

        # Symbol input field
        ttk.Label(data_section, text="Symbol:").pack(side='left', padx=(0, 5))
        self.symbol_var = tk.StringVar(value="AAPL")
        symbol_entry = ttk.Entry(data_section, textvariable=self.symbol_var, width=10,
                                font=('JetBrains Mono', 11))
        symbol_entry.pack(side='left', padx=(0, 15))

        # Start/Stop stream button
        self.stream_btn = ttk.Button(data_section, text="▶ Start Stream", 
                                     command=self.toggle_stream, state='disabled')
        self.stream_btn.pack(side='left', padx=(0, 5))

        # Recalibrate regime model button
        self.recal_btn = ttk.Button(data_section, text="⟳ Recalibrate", 
                                    command=self.recalibrate_model, state='disabled')
        self.recal_btn.pack(side='left', padx=(0, 15))

        # Live price display (right-aligned)
        price_frame = ttk.Frame(data_section)
        price_frame.pack(side='right')

        ttk.Label(price_frame, text="Last Price:", 
                 font=('Segoe UI', 10)).pack(side='left', padx=(0, 5))
        self.price_label = tk.Label(price_frame, text="---.--",
                                   font=('JetBrains Mono', 16, 'bold'),
                                   bg='#0d1117', fg='#7ee787')
        self.price_label.pack(side='left')

        # ----- CHART FRAME -----
        chart_frame = ttk.LabelFrame(main_frame, text="Live OHLC with Markov Regime (5s Bars)", padding="10")
        chart_frame.grid(row=2, column=0, sticky='nsew')
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.rowconfigure(0, weight=1)

        self.chart_container = ttk.Frame(chart_frame)
        self.chart_container.grid(row=0, column=0, sticky='nsew')
        self.chart_container.columnconfigure(0, weight=1)
        self.chart_container.rowconfigure(0, weight=1)

        # ----- STATISTICS BAR -----
        stats_frame = ttk.Frame(main_frame)
        stats_frame.grid(row=3, column=0, sticky='ew', pady=(10, 0))

        # Create stat labels: Bars count, High, Low, Current Regime, Ticks per bar
        self.stats_labels = {}
        stats = [('Bars', '0'), ('High', '--'), ('Low', '--'), ('Regime', '--'), ('Ticks/Bar', '0')]
        
        for i, (name, val) in enumerate(stats):
            frame = ttk.Frame(stats_frame)
            frame.pack(side='left', padx=15)
            ttk.Label(frame, text=f"{name}:", font=('Segoe UI', 9)).pack(side='left')
            label = tk.Label(frame, text=val, font=('JetBrains Mono', 10, 'bold'),
                           bg='#0d1117', fg='#8b949e')
            label.pack(side='left', padx=(5, 0))
            self.stats_labels[name] = label

    def setup_chart(self):
        # Initialize matplotlib figure with dark theme
        plt.style.use('dark_background')
        
        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=(12, 6), facecolor='#0d1117')
        self.ax.set_facecolor('#161b22')
        
        # Style axis spines (borders) and ticks
        self.ax.tick_params(colors='#8b949e', labelsize=9)
        self.ax.spines['bottom'].set_color('#30363d')
        self.ax.spines['top'].set_color('#30363d')
        self.ax.spines['left'].set_color('#30363d')
        self.ax.spines['right'].set_color('#30363d')
        self.ax.grid(True, alpha=0.2, color='#30363d', linestyle='--')
        
        # Set axis labels and initial title
        self.ax.set_xlabel('Time', color='#8b949e', fontsize=10)
        self.ax.set_ylabel('Price', color='#8b949e', fontsize=10)
        self.ax.set_title('Waiting for data...', color='#c9d1d9', fontsize=12, fontweight='bold')

        # Embed matplotlib canvas in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.chart_container)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        self.fig.tight_layout()
        self.canvas.draw()

    def create_contract(self, symbol):
        # Create IB Contract object for US stock
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"                        # Stock
        contract.exchange = "SMART"                     # IB smart routing
        contract.currency = "USD"
        return contract

    def connect_ib(self):
        # Establish connection to TWS in background thread
        try:
            host = self.host_var.get()
            port = int(self.port_var.get())

            def connect_thread():
                # Run IB client message loop (blocking)
                try:
                    self.ib_app.connect(host, port, clientId=1)
                    self.ib_app.run()
                except Exception as e:
                    print(f"Connection error: {e}")

            # Start connection in daemon thread (dies with main program)
            thread = threading.Thread(target=connect_thread, daemon=True)
            thread.start()

            # Wait up to 5 seconds for connection confirmation
            for _ in range(50):
                if self.ib_app.connected:
                    break
                time.sleep(0.1)

            # Update UI based on connection result
            if self.ib_app.connected:
                self.connected = True
                self.connect_btn.config(state='disabled')
                self.disconnect_btn.config(state='normal')
                self.stream_btn.config(state='normal')
                self.status_indicator.config(text="● CONNECTED", fg='#7ee787')
            else:
                messagebox.showerror("Error", "Failed to connect to TWS")

        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")

    def disconnect_ib(self):
        # Clean disconnect from TWS
        try:
            if self.streaming:
                self.stop_stream()
            
            self.ib_app.disconnect()
            self.connected = False
            # Reset UI to disconnected state
            self.connect_btn.config(state='normal')
            self.disconnect_btn.config(state='disabled')
            self.stream_btn.config(state='disabled')
            self.status_indicator.config(text="● DISCONNECTED", fg='#f85149')

        except Exception as e:
            print(f"Disconnect error: {e}")

    def toggle_stream(self):
        # Toggle between starting and stopping market data stream
        if not self.streaming:
            self.start_stream()
        else:
            self.stop_stream()

    def start_stream(self):
        # Begin streaming live market data for selected symbol
        if not self.connected:
            return

        symbol = self.symbol_var.get().upper()
        if not symbol:
            messagebox.showerror("Error", "Please enter a symbol")
            return

        # Reset all data structures
        with self.bar_lock:
            self.ohlc_bars.clear()
            self.current_bar = None
            self.bar_start_time = None
            self.price_history.clear()
            self.regime_model = MarkovRegime()

        contract = self.create_contract(symbol)
        
        # Fetch 5 minutes of historical 5-second bars for regime calibration
        self.ib_app.historical_data.clear()
        self.ib_app.hist_done.clear()
        self.ib_app.reqHistoricalData(2, contract, "", "300 S", "5 secs", "TRADES", 1, 1, False, [])
        # Wait for historical data and calibrate regime model
        if self.ib_app.hist_done.wait(timeout=10) and 2 in self.ib_app.historical_data:
            self.regime_model.calibrate(self.ib_app.historical_data[2])
            print(f"Calibrated regime model with {len(self.ib_app.historical_data[2])} bars")

        # Subscribe to live market data stream
        self.ib_app.reqMktData(1, contract, "", False, False, [])

        # Update state and UI
        self.streaming = True
        self.running = True
        self.stream_btn.config(text="■ Stop Stream", style='Accent.TButton')
        self.recal_btn.config(state='normal')
        self.status_indicator.config(text=f"● STREAMING {symbol}", fg='#58a6ff')

        # Start background thread for bar time management
        self.update_thread = threading.Thread(target=self.bar_manager_loop, daemon=True)
        self.update_thread.start()

        # Start chart refresh loop
        self.update_chart_loop()

    def stop_stream(self):
        # Stop market data streaming and cleanup
        self.running = False
        self.streaming = False
        
        # Cancel market data subscription
        try:
            self.ib_app.cancelMktData(1)
        except:
            pass

        # Reset UI to connected (not streaming) state
        self.stream_btn.config(text="▶ Start Stream", style='TButton')
        self.recal_btn.config(state='disabled')
        self.status_indicator.config(text="● CONNECTED", fg='#7ee787')

    def recalibrate_model(self):
        # ** Commented out for now ** will add regime model later
        pass

    def on_tick_data(self, data_type, value, timestamp):
        # Callback invoked by IBApp when new tick arrives
        if data_type == 'price' and value > 0:
            with self.bar_lock:
                # Store tick in price history
                self.price_history.append((timestamp, value))
                
                # Create new bar or update existing one
                if self.current_bar is None:
                    self.current_bar = OHLCBar(timestamp, value)
                    self.bar_start_time = timestamp
                else:
                    self.current_bar.update(value)

            # Update price display (schedule on main thread for thread safety)
            self.root.after(0, lambda: self.price_label.config(text=f"{value:.2f}"))

    def bar_manager_loop(self):
        # Background thread that finalizes bars when their time period expires
        while self.running:
            time.sleep(0.1)                             # Check every 100ms
            
            with self.bar_lock:
                if self.current_bar is not None and self.bar_start_time is not None:
                    elapsed = (datetime.now() - self.bar_start_time).total_seconds()
                    
                    # If bar duration exceeded, finalize bar and start new one
                    if elapsed >= self.bar_duration:
                        self.ohlc_bars.append(self.current_bar)
                        # Determine regime using Markov filtering (transition probs + emission likelihood)
                        self.regime_model.get_regime(list(self.ohlc_bars))
                        
                        # Initialize new bar with last close price as open
                        last_price = self.current_bar.close
                        self.current_bar = OHLCBar(datetime.now(), last_price)
                        self.bar_start_time = datetime.now()

    def update_chart_loop(self):
        # Periodic chart refresh loop (runs on main thread via after())
        if not self.running:
            return
        self.draw_ohlc_chart()
        self.update_stats()
        # Schedule next update in 200ms, save ID for cleanup on close
        self._after_id = self.root.after(200, self.update_chart_loop)

    def draw_ohlc_chart(self):
        # Render the candlestick chart with regime background colors
        self.ax.clear()
        
        # Get thread-safe copy of bar data
        with self.bar_lock:
            bars = list(self.ohlc_bars)
            current = self.current_bar

        # Include the currently forming bar in display
        if current is not None:
            bars = bars + [current]

        # Show placeholder if no data yet
        if not bars:
            self.ax.set_facecolor('#161b22')
            self.ax.set_title('Waiting for data...', color='#c9d1d9', fontsize=12, fontweight='bold')
            self.ax.grid(True, alpha=0.2, color='#30363d', linestyle='--')
            self.canvas.draw_idle()
            return

        # Calculate price range for y-axis with padding
        all_prices = [bar.low for bar in bars] + [bar.high for bar in bars]
        price_min, price_max = min(all_prices), max(all_prices)
        price_range = price_max - price_min
        padding = max(price_range * 0.1, 0.01)
        y_min, y_max = price_min - padding, price_max + padding

        # Assign current regime to the forming bar (preview - actual regime determined when bar completes)
        # Note: Don't call get_regime here as it would corrupt the Markov state
        if current is not None:
            # ** Commented out for now ** will add regime model later
            #current.regime = self.regime_model.current_state
            pass

        width = 0.6                                     # Candlestick body width
        for i, bar in enumerate(bars):
            # Draw regime background rectangle spanning full height
            # bg is a Rectangle patch drawn as the regime background for each candlestick bar.
            # Parameters:
            #   (i - 0.5, y_min): (x, y) location of bottom-left corner. Offset by 0.5 to center with tick.
            #   1: rectangle width (1 unit, so it spans one candlestick/bar horizontally)
            #   y_max - y_min: height of rectangle (covers entire y-axis data range for that bar)
            #   facecolor=(1,1,1,0): RGBA tuple; pure white but 0 alpha = fully transparent (so not visible)
            #   edgecolor='none': disables rectangle edge/border
            #   alpha=0.0: another way to set full transparency (superfluous here with facecolor alpha 0)
            #   zorder=0: drawing order (plot furthest to back, under all other chart elements)
            bg = Rectangle(
                (i - 0.5, y_min),   # x/y position for the bar's background (centered)
                1,                  # width: one bar
                y_max - y_min,      # height: entire visible y-axis
                facecolor=(1, 1, 1, 0),   # fully transparent (white with 0 alpha)
                edgecolor='none',   # no border line
                alpha=0.0,          # completely transparent
                zorder=0            # background layer
            )

            # ** Commented out for now ** will add bg_colors for regime model later
            #bg = Rectangle((i - 0.5, y_min), 1, y_max - y_min, 
            #              facecolor=self.regime_model.bg_colors[bar.regime], alpha=0.4, zorder=0)
            
            self.ax.add_patch(bg)

            # Determine candlestick color: green=bullish (close>=open), red=bearish
            color, edge_color = ('#3fb950', '#7ee787') if bar.close >= bar.open else ('#f85149', '#ff7b72')
            body_bottom, body_height = min(bar.open, bar.close), max(abs(bar.close - bar.open), 0.001)

            # Draw candlestick body
            rect = Rectangle((i - width/2, body_bottom), width, body_height, 
                            facecolor=color, edgecolor=edge_color, linewidth=1.5, alpha=0.9, zorder=2)
            self.ax.add_patch(rect)
            
            # Draw lower wick (low to body bottom)
            self.ax.plot([i, i], [bar.low, body_bottom], color=edge_color, linewidth=1.5, zorder=1)
            # Draw upper wick (body top to high)
            self.ax.plot([i, i], [body_bottom + body_height, bar.high], color=edge_color, linewidth=1.5, zorder=1)

            # Highlight current forming bar with vertical dotted line
            if i == len(bars) - 1 and current is not None:
                self.ax.axvline(x=i, color='#58a6ff', alpha=0.3, linestyle=':', linewidth=2)

        # Configure axes appearance
        self.ax.set_facecolor('#161b22')
        
        # Set x-axis labels to bar timestamps
        x_labels = [bar.timestamp.strftime('%H:%M:%S') for bar in bars]
        self.ax.set_xticks(range(len(bars)))
        self.ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xlim(-0.5, max(self.max_bars - 0.5, len(bars) - 0.5))
        # Format y-axis to show 3 decimal places (not scientific notation)
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.3f}'))

        # Apply axis styling
        self.ax.tick_params(colors='#8b949e', labelsize=9)
        self.ax.spines['bottom'].set_color('#30363d')
        self.ax.spines['top'].set_color('#30363d')
        self.ax.spines['left'].set_color('#30363d')
        self.ax.spines['right'].set_color('#30363d')
        self.ax.grid(True, alpha=0.2, color='#30363d', linestyle='--')

        self.ax.set_xlabel('Time', color='#8b949e', fontsize=10)
        self.ax.set_ylabel('Price', color='#8b949e', fontsize=10)
        
        # Set title showing symbol, current regime, and bar count
        symbol = self.symbol_var.get().upper()
        regime_names = ['LOW', 'MED', 'HIGH']
        curr_regime = regime_names[bars[-1].regime] if bars else 'N/A'
        self.ax.set_title(f'{symbol} - Regime: {curr_regime} | {len(bars)}/{self.max_bars} bars',
                         color='#c9d1d9', fontsize=12, fontweight='bold')

        self.fig.tight_layout()
        self.canvas.draw_idle()                         # Non-blocking redraw

    def update_stats(self):
        # Update the statistics bar with current values
        with self.bar_lock:
            bars = list(self.ohlc_bars)
            current = self.current_bar

        if current:
            bars = bars + [current]

        if not bars:
            return

        # Update bar count
        self.stats_labels['Bars'].config(text=str(len(bars)))
        
        # Update session high/low
        all_highs = [b.high for b in bars]
        all_lows = [b.low for b in bars]
        self.stats_labels['High'].config(text=f"{max(all_highs):.2f}")
        self.stats_labels['Low'].config(text=f"{min(all_lows):.2f}")
        
        # Update regime display with color coding
        regime_names = ['LOW', 'MED', 'HIGH']
        regime_colors = ['#3fb950', '#d29922', '#f85149']
        curr_regime = bars[-1].regime if bars else 0
        self.stats_labels['Regime'].config(text=regime_names[curr_regime], fg=regime_colors[curr_regime])
        
        # Update ticks per bar for current forming bar
        if current:
            self.stats_labels['Ticks/Bar'].config(text=str(current.tick_count))

    def on_closing(self):
        # Clean shutdown when window is closed
        self.running = False
        # Cancel scheduled chart updates to prevent errors
        if hasattr(self, '_after_id'):
            self.root.after_cancel(self._after_id)
        # Disconnect from TWS if connected
        if self.connected:
            try:
                if self.streaming:
                    self.ib_app.cancelMktData(1)
                self.ib_app.disconnect()
            except:
                pass
        self.root.destroy()


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================
def main():
    root = tk.Tk()
    app = LiveMarketDashboard(root)
    # Register clean shutdown handler
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
