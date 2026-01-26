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
    """
    3-state Markov Chain Regime Switching model for volatility classification.

    Uses a transition probability matrix and Gaussian emission distributions to
    compute the posterior probability of each regime given observed volatility.
    The regime is determined by the highest likelihood of observing the realized
    bar volatility, weighted by transition probabilities from the previous state.
    """

    def __init__(self):
        # =====================================================================
        # MODEL CONFIGURATION
        # =====================================================================
        # We define 3 volatility regimes:
        #   State 0 = LOW volatility  (calm market, small price movements)
        #   State 1 = MED volatility  (normal market conditions)
        #   State 2 = HIGH volatility (turbulent market, large price swings)
        self.n_states = 3
        self.current_state = 0                          # Current most likely regime
        self.colors = ['#3fb950', '#d29922', '#f85149'] # Regime label colors: green, orange, red
        self.bg_colors = ['#1a3d1a', '#3d3319', '#3d1a1a']  # Muted background colors for chart

        # =====================================================================
        # STATE PROBABILITY VECTOR (aka "belief state" or "filtered distribution")
        # =====================================================================
        # This vector holds our current belief about which regime we're in:
        #   state_probs[i] = P(regime = i | all observations so far)
        #
        # At any time, these probabilities sum to 1. For example:
        #   [0.7, 0.2, 0.1] means 70% chance LOW, 20% MED, 10% HIGH
        #
        # We start with uniform (equal) probabilities since we have no information yet.
        self.state_probs = np.array([1/3, 1/3, 1/3])

        # =====================================================================
        # TRANSITION PROBABILITY MATRIX (the "Markov" part)
        # =====================================================================
        # The transition matrix captures the MARKOV PROPERTY: the probability of
        # the next state depends ONLY on the current state, not on history.
        #
        # T[i,j] = P(next_regime = j | current_regime = i)
        #
        # Reading the matrix:
        #   Row i = "If we're currently in regime i, what's the probability of..."
        #   Column j = "...transitioning to regime j?"
        #
        # Each row must sum to 1 (we must go somewhere).
        #
        # The HIGH diagonal values (0.80-0.90) mean regimes are "sticky" - once
        # we're in a regime, we tend to stay there. This reflects market reality:
        # calm periods cluster together, as do volatile periods.
        self.transition_matrix = np.array([
            # To:    LOW   MED   HIGH
            [0.90, 0.08, 0.02],  # From LOW:  90% stay, 8% -> med, 2% -> high
            [0.10, 0.80, 0.10],  # From MED:  10% -> low, 80% stay, 10% -> high
            [0.02, 0.08, 0.90]   # From HIGH: 2% -> low, 8% -> med, 90% stay
        ])
        # Notice: It's hard to jump directly from LOW to HIGH (only 2% chance).
        # Transitions typically go through the MED regime first.

        # =====================================================================
        # EMISSION DISTRIBUTION PARAMETERS (the "Hidden" part)
        # =====================================================================
        # Each regime "emits" volatility values according to a Gaussian distribution.
        # This is the EMISSION MODEL: P(observed_volatility | regime)
        #
        # Why Gaussian? It's a reasonable assumption that volatility within a regime
        # is normally distributed around some mean with some variance.
        #
        # emission_means[i] = Expected (average) volatility when in regime i
        # emission_stds[i]  = Standard deviation of volatility when in regime i
        #
        # These parameters are calibrated from historical data.
        # LOW regime:  mean=0.05%, std=0.03% (tight, small movements)
        # MED regime:  mean=0.20%, std=0.10% (moderate movements)
        # HIGH regime: mean=0.50%, std=0.30% (wide, large movements)
        self.emission_means = np.array([0.0005, 0.002, 0.005])
        self.emission_stds = np.array([0.0003, 0.001, 0.003])

    def calibrate(self, hist_bars):
        """
        Calibrate emission distribution parameters and transition matrix from historical data.

        Uses k-means style clustering to estimate regime-specific volatility distributions,
        then estimates transition probabilities from observed regime sequences.
        """
        # Need enough data to get meaningful statistics
        if len(hist_bars) < 20:
            return

        # =====================================================================
        # STEP 1: COMPUTE HISTORICAL VOLATILITIES
        # =====================================================================
        # Volatility = (High - Low) / Close for each bar
        # This measures the price range as a fraction of the closing price
        vols = np.array([(b['h'] - b['l']) / b['c'] if b['c'] > 0 else 0 for b in hist_bars])
        vols = vols[vols > 0]  # Remove zero volatility bars (no price movement)

        if len(vols) < 20:
            return

        # =====================================================================
        # STEP 2: ASSIGN BARS TO REGIMES USING PERCENTILES
        # =====================================================================
        # We split the volatility distribution into thirds:
        #   Bottom 33% of volatilities -> LOW regime
        #   Middle 33% of volatilities -> MED regime
        #   Top 33% of volatilities    -> HIGH regime
        p33, p67 = np.percentile(vols, 33), np.percentile(vols, 67)

        # Create array of regime assignments (0, 1, or 2 for each bar)
        regime_assignments = np.zeros(len(vols), dtype=int)
        regime_assignments[vols >= p33] = 1   # MED if above 33rd percentile
        regime_assignments[vols >= p67] = 2   # HIGH if above 67th percentile

        # =====================================================================
        # STEP 3: ESTIMATE EMISSION PARAMETERS (mean and std for each regime)
        # =====================================================================
        # For each regime, compute the mean and standard deviation of volatilities
        # that were assigned to that regime. This gives us the Gaussian parameters.
        for regime in range(self.n_states):
            # Get all volatilities assigned to this regime
            regime_vols = vols[regime_assignments == regime]
            if len(regime_vols) >= 3:
                # Mean = center of the Gaussian distribution for this regime
                self.emission_means[regime] = np.mean(regime_vols)
                # Std = spread of the Gaussian (how much variation within regime)
                # Use max() to prevent zero std which would cause division errors
                self.emission_stds[regime] = max(np.std(regime_vols), 1e-6)

        # Ensure means are properly ordered: LOW < MED < HIGH
        # (in case percentile assignment didn't perfectly separate them)
        sorted_indices = np.argsort(self.emission_means)
        self.emission_means = self.emission_means[sorted_indices]
        self.emission_stds = self.emission_stds[sorted_indices]

        # =====================================================================
        # STEP 4: ESTIMATE TRANSITION MATRIX FROM REGIME SEQUENCE
        # =====================================================================
        # Count how many times we transitioned from regime i to regime j
        # by looking at consecutive bars in the historical data
        transition_counts = np.zeros((self.n_states, self.n_states))
        for t in range(1, len(regime_assignments)):
            prev_regime = regime_assignments[t-1]  # Where we were
            curr_regime = regime_assignments[t]     # Where we went
            transition_counts[prev_regime, curr_regime] += 1

        # Convert counts to probabilities by normalizing each row
        for i in range(self.n_states):
            row_sum = transition_counts[i].sum()
            if row_sum > 0:
                # Add 0.1 smoothing to each cell to avoid zero probabilities
                # (Laplace smoothing - ensures all transitions are possible)
                self.transition_matrix[i] = (transition_counts[i] + 0.1) / (row_sum + 0.3)

        # Reset state probabilities after calibration (start fresh)
        self.state_probs = np.array([1/3, 1/3, 1/3])

        print(f"Calibrated emission means: {self.emission_means}")
        print(f"Calibrated emission stds: {self.emission_stds}")

    def _gaussian_likelihood(self, vol, regime):
        """
        Compute the probability density of observing volatility 'vol' given 'regime'.
        Uses Gaussian (normal) distribution as the emission model.

        This answers: "If we're in this regime, how likely is it to see this volatility?"
        """
        mean = self.emission_means[regime]  # Expected volatility for this regime
        std = self.emission_stds[regime]    # Spread of volatility for this regime

        # =====================================================================
        # GAUSSIAN PROBABILITY DENSITY FUNCTION (PDF)
        # =====================================================================
        # Formula: P(x) = (1 / (σ * √(2π))) * exp(-0.5 * ((x - μ) / σ)²)
        #
        # Where:
        #   x = observed volatility (vol)
        #   μ = mean (expected volatility for regime)
        #   σ = standard deviation (spread)
        #
        # The PDF gives a higher value when vol is close to the mean,
        # and lower values as vol moves away from the mean.
        coeff = 1 / (std * np.sqrt(2 * np.pi))  # Normalization constant
        exponent = -0.5 * ((vol - mean) / std) ** 2  # Squared distance from mean
        return coeff * np.exp(exponent)
        #
        # Example: If LOW regime has mean=0.001 and we observe vol=0.001,
        # the likelihood is high. If we observe vol=0.01, likelihood is very low.

    def get_regime(self, bars):
        """
        Determine the current regime using the Markov Chain filtering approach.

        This is the core inference algorithm that uses Bayes' rule to update
        our belief about which regime we're in based on observed volatility.
        """
        if not bars:
            return self.current_state

        # Get the most recent bar's volatility - this is our new observation
        current_bar = bars[-1]
        vol = current_bar.volatility  # (high - low) / close

        if vol <= 0:
            current_bar.regime = self.current_state
            return self.current_state

        # =====================================================================
        # STEP 1: PREDICTION STEP (Time Update)
        # =====================================================================
        # Before seeing the new observation, predict where we might be based
        # on where we were and the transition probabilities.
        #
        # Math: prior[j] = Σᵢ T[i,j] * state_probs[i]
        # "Sum over all possible previous states, weighted by their probability"
        #
        # In matrix form: prior = T^T @ state_probs
        # (T^T is transpose because we want column j from each row)
        prior_probs = self.transition_matrix.T @ self.state_probs
        #
        # Example: If state_probs = [0.8, 0.15, 0.05] (80% sure we're in LOW),
        # then prior might be [0.75, 0.18, 0.07] after applying transition probs.

        # =====================================================================
        # STEP 2: COMPUTE EMISSION LIKELIHOODS
        # =====================================================================
        # For each regime, compute: "How likely is this volatility if we're in that regime?"
        #
        # likelihoods[i] = P(vol | regime = i)
        #
        # This uses the Gaussian PDF for each regime's emission distribution.
        likelihoods = np.array([self._gaussian_likelihood(vol, i) for i in range(self.n_states)])
        #
        # Example: If vol=0.001 (low volatility):
        #   likelihoods might be [0.95, 0.30, 0.05]
        #   HIGH likelihood for LOW regime, low likelihood for HIGH regime

        # =====================================================================
        # STEP 3: UPDATE STEP (Measurement Update) - BAYES' RULE
        # =====================================================================
        # Combine the prior (where transition matrix says we should be) with
        # the likelihood (what the observed volatility suggests).
        #
        # Bayes' Rule: P(regime | vol) ∝ P(vol | regime) × P(regime)
        #                posterior    ∝   likelihood    ×   prior
        #
        # The regime with high prior AND high likelihood wins.
        posterior_probs = prior_probs * likelihoods
        #
        # Example: If prior = [0.75, 0.18, 0.07] and likelihoods = [0.95, 0.30, 0.05]
        # Then posterior ∝ [0.75*0.95, 0.18*0.30, 0.07*0.05] = [0.7125, 0.054, 0.0035]

        # Normalize so probabilities sum to 1
        # This is the denominator in Bayes' rule: P(vol) = Σᵢ P(vol|i)P(i)
        prob_sum = posterior_probs.sum()
        if prob_sum > 0:
            posterior_probs = posterior_probs / prob_sum
        else:
            # Fallback to prior if all likelihoods are zero (shouldn't happen)
            posterior_probs = prior_probs
        #
        # After normalization: [0.926, 0.070, 0.004] = 92.6% sure we're in LOW

        # Save updated belief for next iteration (this is the "filtering" part)
        # Our belief state carries forward through time
        self.state_probs = posterior_probs

        # =====================================================================
        # STEP 4: SELECT MOST LIKELY REGIME (Maximum A Posteriori - MAP)
        # =====================================================================
        # Choose the regime with the highest posterior probability
        # This is our best guess given all the evidence
        self.current_state = int(np.argmax(posterior_probs))
        current_bar.regime = self.current_state
        #
        # The regime with highest probability "wins" - this is what we display
        # on the chart and use for trading decisions

        return self.current_state


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
        # Fetch fresh historical data and recalibrate regime thresholds
        if not self.streaming:
            return
        contract = self.create_contract(self.symbol_var.get().upper())
        self.ib_app.historical_data.clear()
        self.ib_app.hist_done.clear()
        # Request latest 5 minutes of 5-second bars
        self.ib_app.reqHistoricalData(3, contract, "", "300 S", "5 secs", "TRADES", 1, 1, False, [])
        if self.ib_app.hist_done.wait(timeout=10) and 3 in self.ib_app.historical_data:
            with self.bar_lock:
                self.regime_model.calibrate(self.ib_app.historical_data[3])
            print(f"Recalibrated with {len(self.ib_app.historical_data[3])} bars")

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
            current.regime = self.regime_model.current_state

        width = 0.6                                     # Candlestick body width
        for i, bar in enumerate(bars):
            # Draw regime background rectangle spanning full height
            bg = Rectangle((i - 0.5, y_min), 1, y_max - y_min,
                          facecolor=self.regime_model.bg_colors[bar.regime], alpha=0.4, zorder=0)
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
