import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.connected = False
        self.historical_data = {}
        
    def error(self, reqId, errorCode, errorString, *args):
        # Filter out irrelevant warnings about fractional shares
        if errorCode == 2176 and "fractional share" in errorString.lower():
            return  # Ignore this specific warning
        print(f"Error {errorCode}: {errorString}")
        if args:
            print(f"Additional error info: {args}")
        
    def nextValidId(self, orderId):
        self.connected = True
        print("Connected to IB")
        
    def historicalData(self, reqId, bar):
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
        print(f"Historical data received for reqId {reqId}")

class EarningsTradingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Earnings Trading Dashboard - IV Crush Analysis")
        self.root.geometry("1600x1000")
        
        # Data storage
        self.stock_data = None
        self.vix_data = None
        self.iv_data = None
        self.earnings_date = None
        self.ticker = None
        
        # IB connection
        self.ib_app = IBApp()
        self.connected = False
        
        # Option pricing parameters
        self.risk_free_rate = 0.05  # 5% risk-free rate
        
        # Chart management
        self.ax1_twin = None  # Keep track of twin axis
        
        self.setup_ui()
    
    def create_equity_contract(self, symbol):
        """Create an equity contract for the given symbol"""
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract
    
    def create_vix_contract(self):
        """Create a VIX contract"""
        contract = Contract()
        contract.symbol = "VIX"
        contract.secType = "IND"
        contract.exchange = "CBOE"
        contract.currency = "USD"
        return contract
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Interactive Brokers Connection", padding="5")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(conn_frame, text="Host:").grid(row=0, column=0, padx=(0, 5))
        self.host_var = tk.StringVar(value="127.0.0.1")
        ttk.Entry(conn_frame, textvariable=self.host_var, width=15).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=2, padx=(0, 5))
        self.port_var = tk.StringVar(value="7497")
        ttk.Entry(conn_frame, textvariable=self.port_var, width=10).grid(row=0, column=3, padx=(0, 10))
        
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect_ib)
        self.connect_btn.grid(row=0, column=4, padx=(0, 10))
        
        self.disconnect_btn = ttk.Button(conn_frame, text="Disconnect", command=self.disconnect_ib, state="disabled")
        self.disconnect_btn.grid(row=0, column=5)
        
        # Earnings setup frame
        earnings_frame = ttk.LabelFrame(main_frame, text="Earnings Analysis Setup", padding="5")
        earnings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(earnings_frame, text="Ticker:").grid(row=0, column=0, padx=(0, 5))
        self.ticker_var = tk.StringVar(value="NVDA")
        ttk.Entry(earnings_frame, textvariable=self.ticker_var, width=10).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(earnings_frame, text="Earnings Date:").grid(row=0, column=2, padx=(0, 5))
        self.earnings_date_var = tk.StringVar(value="2025-08-27")  # Format: YYYY-MM-DD
        ttk.Entry(earnings_frame, textvariable=self.earnings_date_var, width=12).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(earnings_frame, text="Days to Expiry:").grid(row=0, column=4, padx=(0, 5))
        self.days_to_expiry_var = tk.StringVar(value="30")
        ttk.Entry(earnings_frame, textvariable=self.days_to_expiry_var, width=8).grid(row=0, column=5, padx=(0, 10))
        
        self.analyze_btn = ttk.Button(earnings_frame, text="Analyze IV Crush", command=self.analyze_iv_crush, state="disabled")
        self.analyze_btn.grid(row=0, column=6)
        
        # Current metrics frame
        metrics_frame = ttk.LabelFrame(main_frame, text="Current Metrics", padding="5")
        metrics_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(metrics_frame, text="Stock Price:").grid(row=0, column=0, padx=(0, 5))
        self.stock_price_label = ttk.Label(metrics_frame, text="N/A", font=("Arial", 10, "bold"))
        self.stock_price_label.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(metrics_frame, text="VIX Level:").grid(row=0, column=2, padx=(0, 5))
        self.vix_level_label = ttk.Label(metrics_frame, text="N/A", font=("Arial", 10, "bold"))
        self.vix_level_label.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(metrics_frame, text="Current IV:").grid(row=0, column=4, padx=(0, 5))
        self.current_iv_label = ttk.Label(metrics_frame, text="N/A", font=("Arial", 10, "bold"))
        self.current_iv_label.grid(row=0, column=5, padx=(0, 20))
        
        # IV Crush Analysis frame
        crush_frame = ttk.LabelFrame(main_frame, text="IV Crush Analysis", padding="5")
        crush_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(crush_frame, text="Pre-Earnings IV:").grid(row=0, column=0, padx=(0, 5))
        self.pre_iv_label = ttk.Label(crush_frame, text="N/A", font=("Arial", 10, "bold"))
        self.pre_iv_label.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(crush_frame, text="Post-Earnings IV:").grid(row=0, column=2, padx=(0, 5))
        self.post_iv_label = ttk.Label(crush_frame, text="N/A", font=("Arial", 10, "bold"))
        self.post_iv_label.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(crush_frame, text="IV Crush %:").grid(row=0, column=4, padx=(0, 5))
        self.iv_crush_label = ttk.Label(crush_frame, text="N/A", font=("Arial", 11, "bold"), foreground="red")
        self.iv_crush_label.grid(row=0, column=5, padx=(0, 20))
        
        # Spot vs Strike frame
        spot_strike_frame = ttk.LabelFrame(main_frame, text="Spot vs Strike Analysis", padding="5")
        spot_strike_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(spot_strike_frame, text="Strike Price:").grid(row=0, column=0, padx=(0, 5))
        self.strike_price_label = ttk.Label(spot_strike_frame, text="N/A", font=("Arial", 11, "bold"), foreground="blue")
        self.strike_price_label.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(spot_strike_frame, text="Pre-Earnings Spot (Close):").grid(row=0, column=2, padx=(0, 5))
        self.pre_spot_label = ttk.Label(spot_strike_frame, text="N/A", font=("Arial", 11, "bold"))
        self.pre_spot_label.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(spot_strike_frame, text="Post-Earnings Spot (Next Day Avg):").grid(row=0, column=4, padx=(0, 5))
        self.post_spot_label = ttk.Label(spot_strike_frame, text="N/A", font=("Arial", 11, "bold"))
        self.post_spot_label.grid(row=0, column=5)
        
        # Option pricing frame
        option_frame = ttk.LabelFrame(main_frame, text="ATM Straddle Pricing & P/L", padding="5")
        option_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(option_frame, text="Pre-Earnings Call:").grid(row=0, column=0, padx=(0, 5))
        self.pre_call_label = ttk.Label(option_frame, text="N/A", font=("Arial", 10))
        self.pre_call_label.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(option_frame, text="Post-Earnings Call:").grid(row=0, column=2, padx=(0, 5))
        self.post_call_label = ttk.Label(option_frame, text="N/A", font=("Arial", 10))
        self.post_call_label.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(option_frame, text="Call Δ:").grid(row=0, column=4, padx=(0, 5))
        self.call_loss_label = ttk.Label(option_frame, text="N/A", font=("Arial", 10, "bold"))
        self.call_loss_label.grid(row=0, column=5, padx=(0, 20))
        
        ttk.Label(option_frame, text="Pre-Earnings Put:").grid(row=1, column=0, padx=(0, 5))
        self.pre_put_label = ttk.Label(option_frame, text="N/A", font=("Arial", 10))
        self.pre_put_label.grid(row=1, column=1, padx=(0, 20))
        
        ttk.Label(option_frame, text="Post-Earnings Put:").grid(row=1, column=2, padx=(0, 5))
        self.post_put_label = ttk.Label(option_frame, text="N/A", font=("Arial", 10))
        self.post_put_label.grid(row=1, column=3, padx=(0, 20))
        
        ttk.Label(option_frame, text="Put Δ:").grid(row=1, column=4, padx=(0, 5))
        self.put_loss_label = ttk.Label(option_frame, text="N/A", font=("Arial", 10, "bold"))
        self.put_loss_label.grid(row=1, column=5, padx=(0, 20))
        
        # Add straddle totals
        ttk.Label(option_frame, text="Pre-Earnings Straddle:").grid(row=2, column=0, padx=(0, 5))
        self.pre_straddle_label = ttk.Label(option_frame, text="N/A", font=("Arial", 12, "bold"), foreground="blue")
        self.pre_straddle_label.grid(row=2, column=1, padx=(0, 20))
        
        ttk.Label(option_frame, text="Post-Earnings Straddle:").grid(row=2, column=2, padx=(0, 5))
        self.post_straddle_label = ttk.Label(option_frame, text="N/A", font=("Arial", 12, "bold"), foreground="blue")
        self.post_straddle_label.grid(row=2, column=3, padx=(0, 20))
        
        ttk.Label(option_frame, text="Straddle Δ:").grid(row=2, column=4, padx=(0, 5))
        self.straddle_loss_label = ttk.Label(option_frame, text="N/A", font=("Arial", 12, "bold"))
        self.straddle_loss_label.grid(row=2, column=5, padx=(0, 20))
        
        # Add P/L analysis
        ttk.Label(option_frame, text="LONG Straddle P/L:").grid(row=3, column=0, padx=(0, 5))
        self.long_pnl_label = ttk.Label(option_frame, text="N/A", font=("Arial", 11, "bold"))
        self.long_pnl_label.grid(row=3, column=1, columnspan=2, padx=(0, 20))
        
        ttk.Label(option_frame, text="SHORT Straddle P/L:").grid(row=3, column=3, padx=(0, 5))
        self.short_pnl_label = ttk.Label(option_frame, text="N/A", font=("Arial", 11, "bold"))
        self.short_pnl_label.grid(row=3, column=4, columnspan=2)
        
        # Greeks frame
        greeks_frame = ttk.LabelFrame(main_frame, text="Greeks Analysis", padding="5")
        greeks_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(greeks_frame, text="Pre-Earnings Delta:").grid(row=0, column=0, padx=(0, 5))
        self.pre_delta_label = ttk.Label(greeks_frame, text="N/A", font=("Arial", 10, "bold"))
        self.pre_delta_label.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(greeks_frame, text="Post-Earnings Delta:").grid(row=0, column=2, padx=(0, 5))
        self.post_delta_label = ttk.Label(greeks_frame, text="N/A", font=("Arial", 10, "bold"))
        self.post_delta_label.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(greeks_frame, text="Delta Change:").grid(row=0, column=4, padx=(0, 5))
        self.delta_change_label = ttk.Label(greeks_frame, text="N/A", font=("Arial", 10, "bold"))
        self.delta_change_label.grid(row=0, column=5)
        
        ttk.Label(greeks_frame, text="Pre-Earnings Vega:").grid(row=1, column=0, padx=(0, 5))
        self.pre_vega_label = ttk.Label(greeks_frame, text="N/A", font=("Arial", 10, "bold"))
        self.pre_vega_label.grid(row=1, column=1, padx=(0, 20))
        
        ttk.Label(greeks_frame, text="Post-Earnings Vega:").grid(row=1, column=2, padx=(0, 5))
        self.post_vega_label = ttk.Label(greeks_frame, text="N/A", font=("Arial", 10, "bold"))
        self.post_vega_label.grid(row=1, column=3, padx=(0, 20))
        
        ttk.Label(greeks_frame, text="Vega Change:").grid(row=1, column=4, padx=(0, 5))
        self.vega_change_label = ttk.Label(greeks_frame, text="N/A", font=("Arial", 10, "bold"))
        self.vega_change_label.grid(row=1, column=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=6, width=80)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        # Plot frame
        plot_frame = ttk.LabelFrame(main_frame, text="IV Crush Visualization", padding="5")
        plot_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        
        # Create matplotlib figure with 2 subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(16, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def connect_ib(self):
        try:
            host = self.host_var.get()
            port = int(self.port_var.get())
            
            self.log_message(f"Connecting to IB at {host}:{port}...")
            
            # Start connection in separate thread
            def connect_thread():
                try:
                    self.ib_app.connect(host, port, 0)
                    self.ib_app.run()
                except Exception as e:
                    self.log_message(f"Connection error: {e}")
                    
            thread = threading.Thread(target=connect_thread, daemon=True)
            thread.start()
            
            # Wait for connection and server version
            for i in range(100):  # Wait up to 10 seconds
                if self.ib_app.connected:
                    try:
                        server_version = self.ib_app.serverVersion()
                        if server_version is not None and server_version > 0:
                            break
                    except:
                        pass
                time.sleep(0.1)
                
            if self.ib_app.connected:
                try:
                    server_version = self.ib_app.serverVersion()
                    if server_version is not None and server_version > 0:
                        self.connected = True
                        self.connect_btn.config(state="disabled")
                        self.disconnect_btn.config(state="normal")
                        self.analyze_btn.config(state="normal")
                        self.log_message(f"Successfully connected to Interactive Brokers (Server Version: {server_version})")
                    else:
                        self.log_message("Connected but server version not available. Please wait a moment and try again.")
                except Exception as e:
                    self.log_message(f"Connection established but server version check failed: {e}")
            else:
                self.log_message("Failed to connect to Interactive Brokers")
                
        except Exception as e:
            self.log_message(f"Connection error: {e}")
            
    def disconnect_ib(self):
        try:
            self.ib_app.disconnect()
            self.connected = False
            self.connect_btn.config(state="normal")
            self.disconnect_btn.config(state="disabled")
            self.analyze_btn.config(state="disabled")
            
            # Clear any existing analysis results
            self.clear_analysis_results()
            
            self.log_message("Disconnected from Interactive Brokers")
        except Exception as e:
            self.log_message(f"Disconnect error: {e}")
    
    def clear_analysis_results(self):
        """Clear all analysis results and reset displays"""
        # Clear charts completely including any twin axes
        self.ax1.clear()
        self.ax2.clear()
        
        # Clear any twin axes that might exist
        if self.ax1_twin is not None:
            try:
                self.ax1_twin.remove()
            except:
                pass
            self.ax1_twin = None
        
        # Redraw the canvas
        self.canvas.draw()
        
        # Reset all metric displays
        self.stock_price_label.config(text="N/A", foreground="black")
        self.vix_level_label.config(text="N/A", foreground="black")
        self.current_iv_label.config(text="N/A", foreground="black")
        
        # Reset IV crush displays
        self.pre_iv_label.config(text="N/A", foreground="black")
        self.post_iv_label.config(text="N/A", foreground="black")
        self.iv_crush_label.config(text="N/A", foreground="red")
        
        # Reset option pricing displays
        self.pre_call_label.config(text="N/A", foreground="black")
        self.post_call_label.config(text="N/A", foreground="black")
        self.call_loss_label.config(text="N/A", foreground="black")
        
        self.pre_put_label.config(text="N/A", foreground="black")
        self.post_put_label.config(text="N/A", foreground="black")
        self.put_loss_label.config(text="N/A", foreground="black")
        
        # Reset straddle displays
        self.pre_straddle_label.config(text="N/A", foreground="blue")
        self.post_straddle_label.config(text="N/A", foreground="blue")
        self.straddle_loss_label.config(text="N/A", foreground="black")
        
        # Reset P/L displays
        self.long_pnl_label.config(text="N/A", foreground="black")
        self.short_pnl_label.config(text="N/A", foreground="black")
        
        # Reset spot/strike displays
        self.strike_price_label.config(text="N/A", foreground="blue")
        self.pre_spot_label.config(text="N/A", foreground="black")
        self.post_spot_label.config(text="N/A", foreground="black")
        
        # Reset Greeks displays
        self.pre_delta_label.config(text="N/A", foreground="black")
        self.post_delta_label.config(text="N/A", foreground="black")
        self.delta_change_label.config(text="N/A", foreground="black")
        self.pre_vega_label.config(text="N/A", foreground="black")
        self.post_vega_label.config(text="N/A", foreground="black")
        self.vega_change_label.config(text="N/A", foreground="black")
        
        # Reset data storage
        self.stock_data = None
        self.vix_data = None
        self.iv_data = None
        
        # Clear IB historical data cache
        if hasattr(self, 'ib_app') and self.ib_app:
            self.ib_app.historical_data.clear()
        
        self.log_message("Analysis results cleared - ready for new analysis")
    
    def black_scholes_call(self, S, K, T, r, sigma):
        """
        Calculate Black-Scholes call option price
        
        Parameters:
        S: Current stock price
        K: Strike price
        T: Time to expiry (in years)
        r: Risk-free rate (annualized)
        sigma: Volatility (annualized using √252 factor)
        """
        from scipy.stats import norm
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return call_price
    
    def black_scholes_put(self, S, K, T, r, sigma):
        """
        Calculate Black-Scholes put option price
        
        Parameters:
        S: Current stock price
        K: Strike price
        T: Time to expiry (in years)
        r: Risk-free rate (annualized)
        sigma: Volatility (annualized using √252 factor)
        """
        from scipy.stats import norm
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put_price
    
    def calculate_delta(self, S, K, T, r, sigma, option_type='call'):
        """Calculate option delta"""
        from scipy.stats import norm
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        if option_type == 'call':
            return norm.cdf(d1)
        else:  # put
            return -norm.cdf(-d1)
    
    def calculate_vega(self, S, K, T, r, sigma):
        """Calculate option vega (same for calls and puts)"""
        from scipy.stats import norm
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        # Vega is per 1% change in volatility
        return S * norm.pdf(d1) * np.sqrt(T) / 100
    
    def analyze_iv_crush(self):
        if not self.connected or not self.ib_app.connected:
            messagebox.showerror("Error", "Not connected to Interactive Brokers")
            return
            
        # Check if we have a valid server version
        try:
            server_version = self.ib_app.serverVersion()
            if server_version is None or server_version <= 0:
                messagebox.showerror("Error", "Connection not fully established. Please wait and try again.")
                return
        except Exception as e:
            self.log_message(f"Connection error: {e}")
            messagebox.showerror("Error", "Connection not stable. Please reconnect.")
            return
            
        self.ticker = self.ticker_var.get().upper()
        earnings_date_str = self.earnings_date_var.get()
        
        try:
            self.earnings_date = datetime.strptime(earnings_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        self.log_message(f"Starting IV crush analysis for {self.ticker} around earnings on {earnings_date_str}")
        
        # Clear previous visualizations and reset displays
        self.clear_analysis_results()
        
        # Calculate date range (3 days before and after earnings)
        start_date = self.earnings_date - timedelta(days=10)  # Extra buffer for data
        end_date = self.earnings_date + timedelta(days=10)
        
        # Clear previous data
        self.ib_app.historical_data.clear()
        
        # Query stock price data
        self.log_message(f"Querying stock price data for {self.ticker}...")
        stock_contract = self.create_equity_contract(self.ticker)
        
        # Clear any existing data for this request ID before making new request
        if 1 in self.ib_app.historical_data:
            del self.ib_app.historical_data[1]
        
        try:
            self.ib_app.reqHistoricalData(
                reqId=1,
                contract=stock_contract,
                endDateTime=end_date.strftime("%Y%m%d %H:%M:%S"),
                durationStr="3 W",
                barSizeSetting="1 day",
                whatToShow="TRADES",
                useRTH=1,
                formatDate=1,
                keepUpToDate=False,
                chartOptions=[]
            )
        except Exception as e:
            self.log_message(f"Error requesting stock data: {e}")
            messagebox.showerror("Error", f"Failed to request stock data: {e}")
            return
        
        # Wait for stock data
        timeout = 15
        start_time = time.time()
        while 1 not in self.ib_app.historical_data and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        if 1 not in self.ib_app.historical_data:
            self.log_message("Failed to get stock price data")
            return
        
        # Process stock data
        stock_data = pd.DataFrame(self.ib_app.historical_data[1])
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        stock_data.set_index('date', inplace=True)
        self.stock_data = stock_data
        self.log_message(f"Received {len(stock_data)} stock price data points")
        
        # Query VIX data
        self.log_message("Querying VIX data...")
        vix_contract = self.create_vix_contract()
        
        # Clear any existing VIX data for this request ID
        if 2 in self.ib_app.historical_data:
            del self.ib_app.historical_data[2]
        
        try:
            self.ib_app.reqHistoricalData(
                reqId=2,
                contract=vix_contract,
                endDateTime=end_date.strftime("%Y%m%d %H:%M:%S"),
                durationStr="3 W",
                barSizeSetting="1 day",
                whatToShow="TRADES",
                useRTH=1,
                formatDate=1,
                keepUpToDate=False,
                chartOptions=[]
            )
        except Exception as e:
            self.log_message(f"Error requesting VIX data: {e}")
            # Continue without VIX data
        
        # Wait for VIX data
        start_time = time.time()
        while 2 not in self.ib_app.historical_data and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        if 2 in self.ib_app.historical_data:
            vix_data = pd.DataFrame(self.ib_app.historical_data[2])
            vix_data['date'] = pd.to_datetime(vix_data['date'])
            vix_data.set_index('date', inplace=True)
            self.vix_data = vix_data
            self.log_message(f"Received {len(vix_data)} VIX data points")
        else:
            self.log_message("VIX data not available")
            self.vix_data = None
        
        # Query IV data for the stock
        self.log_message(f"Querying implied volatility data for {self.ticker}...")
        
        # Clear any existing IV data for this request ID
        if 3 in self.ib_app.historical_data:
            del self.ib_app.historical_data[3]
        
        try:
            self.ib_app.reqHistoricalData(
                reqId=3,
                contract=stock_contract,
                endDateTime=end_date.strftime("%Y%m%d %H:%M:%S"),
                durationStr="3 W",
                barSizeSetting="1 day",
                whatToShow="OPTION_IMPLIED_VOLATILITY",
                useRTH=1,
                formatDate=1,
                keepUpToDate=False,
                chartOptions=[]
            )
        except Exception as e:
            self.log_message(f"Error requesting IV data: {e}")
            # Continue without direct IV data
        
        # Wait for IV data
        start_time = time.time()
        while 3 not in self.ib_app.historical_data and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        if 3 in self.ib_app.historical_data:
            iv_data = pd.DataFrame(self.ib_app.historical_data[3])
            iv_data['date'] = pd.to_datetime(iv_data['date'])
            iv_data.set_index('date', inplace=True)
            
            # Scale IV data properly once here - IB provides DAILY IV that needs annualization
            raw_iv = iv_data['close']
            
            # Convert to decimal if in percentage form, then annualize with √252
            if raw_iv.max() > 5:
                # Data is in percentage form (e.g., 2.5 for 2.5% daily), convert to decimal then annualize
                daily_iv_decimal = raw_iv / 100.0  # Convert to decimal (0.025 for 2.5%)
                iv_data['implied_vol'] = daily_iv_decimal #* np.sqrt(252)  # Annualize with √252
                self.log_message(f"Received {len(iv_data)} IV data points - converted from daily % to annualized decimal")
            else:
                # Data is in decimal form (e.g., 0.025 for 2.5% daily), annualize directly
                iv_data['implied_vol'] = raw_iv# * np.sqrt(252)  # Annualize with √252
                self.log_message(f"Received {len(iv_data)} IV data points - annualized daily decimal with √252")
            
            self.iv_data = iv_data
            annualization_factor = 1#np.sqrt(252)
            self.log_message(f"Applied √252 = {annualization_factor:.2f} annualization factor")
            self.log_message(f"Annualized IV range: {iv_data['implied_vol'].min():.3f} - {iv_data['implied_vol'].max():.3f} (decimal)")
        else:
            self.log_message("Implied volatility data not available - will estimate from VIX")
            self.iv_data = None
        
        # Perform IV crush analysis
        self.perform_iv_crush_analysis()
        
    def perform_iv_crush_analysis(self):
        """Perform the main IV crush analysis"""
        self.log_message("Performing IV crush analysis...")
        
        # Find the closest trading days to earnings
        earnings_date = self.earnings_date
        
        # Get stock price around earnings
        pre_earnings_date = earnings_date - timedelta(days=1)
        post_earnings_date = earnings_date + timedelta(days=1)
        
        # Find actual trading days closest to our target dates
        stock_dates = self.stock_data.index
        
        # Pre-earnings: last trading day before or on earnings date
        pre_date_actual = stock_dates[stock_dates <= earnings_date].max() if len(stock_dates[stock_dates <= earnings_date]) > 0 else stock_dates.min()
        
        # Post-earnings: first trading day AFTER earnings date
        post_date_actual = stock_dates[stock_dates > earnings_date].min() if len(stock_dates[stock_dates > earnings_date]) > 0 else stock_dates.max()
        
        self.log_message(f"Earnings date: {earnings_date.strftime('%Y-%m-%d')}")
        self.log_message(f"Using pre-earnings date: {pre_date_actual.strftime('%Y-%m-%d')} (close price)")
        self.log_message(f"Using post-earnings date: {post_date_actual.strftime('%Y-%m-%d')} (avg of open/close)")
        
        # Get stock prices
        pre_stock_price = self.stock_data.loc[pre_date_actual, 'close']  # Pre-earnings: close of last trading day
        
        # Post-earnings: average of next day's open and close
        post_open = self.stock_data.loc[post_date_actual, 'open']
        post_close = self.stock_data.loc[post_date_actual, 'close']
        post_stock_price = (post_open + post_close) / 2
        
        # Verify we have the right price data
        try:
            pre_close = self.stock_data.loc[pre_date_actual, 'close']
            post_open = self.stock_data.loc[post_date_actual, 'open']
            post_close = self.stock_data.loc[post_date_actual, 'close']
            
            self.log_message(f"Pre-earnings stock price (close): ${pre_close:.2f}")
            self.log_message(f"Post-earnings stock price (next day open): ${post_open:.2f}")
            self.log_message(f"Post-earnings stock price (next day close): ${post_close:.2f}")
            self.log_message(f"Post-earnings stock price (average): ${post_stock_price:.2f}")
            
            # Calculate the overnight move (gap to open)
            overnight_gap_pct = (post_open - pre_close) / pre_close * 100
            self.log_message(f"Overnight earnings gap (to open): {overnight_gap_pct:+.2f}%")
            
            # Calculate total move (close to average)
            total_move_pct = (post_stock_price - pre_close) / pre_close * 100
            self.log_message(f"Total earnings move (close to avg): {total_move_pct:+.2f}%")
            
            # Confirm we're using the right prices
            self.log_message(f"Confirming: Using pre-close ${pre_close:.2f} and post-avg ${post_stock_price:.2f} for analysis")
            
        except Exception as e:
            self.log_message(f"Error accessing price data: {e}")
            return
        
        # Update stock price display
        self.stock_price_label.config(text=f"${post_stock_price:.2f}")
        
        # Get VIX levels if available
        if self.vix_data is not None:
            vix_dates = self.vix_data.index
            pre_vix_date = vix_dates[vix_dates <= pre_earnings_date].max() if len(vix_dates[vix_dates <= pre_earnings_date]) > 0 else vix_dates.min()
            post_vix_date = vix_dates[vix_dates >= post_earnings_date].min() if len(vix_dates[vix_dates >= post_earnings_date]) > 0 else vix_dates.max()
            
            pre_vix = self.vix_data.loc[pre_vix_date, 'close']
            post_vix = self.vix_data.loc[post_vix_date, 'close']
            
            self.log_message(f"Pre-earnings VIX: {pre_vix:.2f}")
            self.log_message(f"Post-earnings VIX: {post_vix:.2f}")
            self.vix_level_label.config(text=f"{post_vix:.2f}")
        else:
            pre_vix = post_vix = 20.0  # Default VIX estimate
            self.vix_level_label.config(text="N/A")
        
        # Get or estimate implied volatilities
        if self.iv_data is not None:
            iv_dates = self.iv_data.index
            pre_iv_date = iv_dates[iv_dates <= pre_earnings_date].max() if len(iv_dates[iv_dates <= pre_earnings_date]) > 0 else iv_dates.min()
            post_iv_date = iv_dates[iv_dates >= post_earnings_date].min() if len(iv_dates[iv_dates >= post_earnings_date]) > 0 else iv_dates.max()
            
            print(pre_iv_date, post_iv_date)
            # Use the pre-scaled IV data directly (already in decimal format, annualized)
            pre_iv = self.iv_data.loc[pre_iv_date, 'implied_vol']
            post_iv = self.iv_data.loc[post_iv_date, 'implied_vol']
        else:
            # Estimate IV from VIX (rough approximation) - VIX is already annualized
            pre_iv = pre_vix / 100.0 * 1.5  # Individual stocks typically have higher IV than VIX
            post_iv = post_vix / 100.0 * 1.2  # Less premium after earnings
        
        self.log_message(f"Pre-earnings implied volatility: {pre_iv:.1%} (annualized)")
        self.log_message(f"Post-earnings implied volatility: {post_iv:.1%} (annualized)")
        self.log_message(f"Note: All volatility values are annualized using √252 = {np.sqrt(252):.2f}")
        
        # Calculate IV crush
        iv_crush_pct = (pre_iv - post_iv) / pre_iv * 100
        self.log_message(f"Implied volatility crush: {iv_crush_pct:.1f}%")
        
        # Update IV displays
        self.current_iv_label.config(text=f"{post_iv:.1%}")
        self.pre_iv_label.config(text=f"{pre_iv:.1%}")
        self.post_iv_label.config(text=f"{post_iv:.1%}")
        self.iv_crush_label.config(text=f"-{iv_crush_pct:.1f}%")
        
        # Calculate option prices
        try:
            days_to_expiry = int(self.days_to_expiry_var.get())
        except ValueError:
            days_to_expiry = 30
            self.days_to_expiry_var.set("30")
        
        time_to_expiry = days_to_expiry / 365.0
        atm_strike_price = pre_stock_price  # ATM strike based on pre-earnings price
        
        # Pre-earnings option prices (using pre-earnings stock price and high IV)
        pre_call_price = self.black_scholes_call(pre_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, pre_iv)
        pre_put_price = self.black_scholes_put(pre_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, pre_iv)
        
        # Post-earnings option prices (SAME ATM strike, post-earnings stock price, but LOWER IV)
        # This shows the pure IV crush effect on the same straddle
        post_call_price = self.black_scholes_call(post_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, post_iv)
        post_put_price = self.black_scholes_put(post_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, post_iv)
        
        # Calculate straddle prices (call + put)
        pre_straddle_price = pre_call_price + pre_put_price
        post_straddle_price = post_call_price + post_put_price
        
        # Calculate option price changes
        call_change_dollar = post_call_price - pre_call_price
        put_change_dollar = post_put_price - pre_put_price
        straddle_change_dollar = post_straddle_price - pre_straddle_price
        
        call_change_pct = call_change_dollar / pre_call_price * 100
        put_change_pct = put_change_dollar / pre_put_price * 100
        straddle_change_pct = straddle_change_dollar / pre_straddle_price * 100
        
        # Calculate P/L for long and short positions
        long_straddle_pnl = straddle_change_dollar  # Long: profit when post > pre
        short_straddle_pnl = -straddle_change_dollar  # Short: profit when pre > post
        
        # Calculate Greeks
        pre_call_delta = self.calculate_delta(pre_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, pre_iv, 'call')
        pre_put_delta = self.calculate_delta(pre_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, pre_iv, 'put')
        pre_straddle_delta = pre_call_delta + pre_put_delta
        
        post_call_delta = self.calculate_delta(post_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, post_iv, 'call')
        post_put_delta = self.calculate_delta(post_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, post_iv, 'put')
        post_straddle_delta = post_call_delta + post_put_delta
        
        delta_change = post_straddle_delta - pre_straddle_delta
        
        pre_call_vega = self.calculate_vega(pre_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, pre_iv)
        pre_put_vega = self.calculate_vega(pre_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, pre_iv)
        pre_straddle_vega = pre_call_vega + pre_put_vega
        
        post_call_vega = self.calculate_vega(post_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, post_iv)
        post_put_vega = self.calculate_vega(post_stock_price, atm_strike_price, time_to_expiry, self.risk_free_rate, post_iv)
        post_straddle_vega = post_call_vega + post_put_vega
        
        vega_change = post_straddle_vega - pre_straddle_vega
        
        self.log_message(f"ATM Strike Price (fixed): ${atm_strike_price:.2f}")
        self.log_message(f"Pre-earnings: Spot=${pre_stock_price:.2f} (close), IV={pre_iv:.1%}")
        self.log_message(f"Post-earnings: Spot=${post_stock_price:.2f} (next day avg), IV={post_iv:.1%}")
        self.log_message(f"")
        self.log_message(f"ATM Call prices: ${pre_call_price:.2f} → ${post_call_price:.2f} ({call_change_pct:+.1f}%)")
        self.log_message(f"ATM Put prices: ${pre_put_price:.2f} → ${post_put_price:.2f} ({put_change_pct:+.1f}%)")
        self.log_message(f"ATM Straddle: ${pre_straddle_price:.2f} → ${post_straddle_price:.2f} ({straddle_change_pct:+.1f}%)")
        self.log_message(f"")
        self.log_message(f"Straddle Delta: {pre_straddle_delta:.3f} → {post_straddle_delta:.3f} (Δ: {delta_change:+.3f})")
        self.log_message(f"Straddle Vega: {pre_straddle_vega:.2f} → {post_straddle_vega:.2f} (Δ: {vega_change:+.2f})")
        self.log_message(f"")
        self.log_message(f"LONG Straddle P/L: ${long_straddle_pnl:+.2f} per contract ({straddle_change_pct:+.1f}%)")
        self.log_message(f"SHORT Straddle P/L: ${short_straddle_pnl:+.2f} per contract ({-straddle_change_pct:+.1f}%)")
        self.log_message(f"Note: Same ${atm_strike_price:.0f} strike used for both pre/post calculations")
        
        # Update option price displays
        self.pre_call_label.config(text=f"${pre_call_price:.2f}")
        self.post_call_label.config(text=f"${post_call_price:.2f}")
        call_color = "green" if call_change_dollar > 0 else "red"
        self.call_loss_label.config(text=f"{call_change_dollar:+.2f}", foreground=call_color)
        
        self.pre_put_label.config(text=f"${pre_put_price:.2f}")
        self.post_put_label.config(text=f"${post_put_price:.2f}")
        put_color = "green" if put_change_dollar > 0 else "red"
        self.put_loss_label.config(text=f"{put_change_dollar:+.2f}", foreground=put_color)
        
        # Update straddle displays
        self.pre_straddle_label.config(text=f"${pre_straddle_price:.2f}")
        self.post_straddle_label.config(text=f"${post_straddle_price:.2f}")
        straddle_color = "green" if straddle_change_dollar > 0 else "red"
        self.straddle_loss_label.config(text=f"{straddle_change_dollar:+.2f}", foreground=straddle_color)
        
        # Update P/L displays
        long_color = "green" if long_straddle_pnl > 0 else "red"
        short_color = "green" if short_straddle_pnl > 0 else "red"
        self.long_pnl_label.config(text=f"{long_straddle_pnl:+.2f} ({straddle_change_pct:+.1f}%)", foreground=long_color)
        self.short_pnl_label.config(text=f"{short_straddle_pnl:+.2f} ({-straddle_change_pct:+.1f}%)", foreground=short_color)
        
        # Update spot/strike displays
        self.strike_price_label.config(text=f"${atm_strike_price:.2f}")
        
        pre_spot_color = "black"
        post_spot_color = "green" if post_stock_price > pre_stock_price else "red"
        self.pre_spot_label.config(text=f"${pre_stock_price:.2f}", foreground=pre_spot_color)
        self.post_spot_label.config(text=f"${post_stock_price:.2f}", foreground=post_spot_color)
        
        # Update Greeks displays
        delta_color = "green" if abs(post_straddle_delta) < abs(pre_straddle_delta) else "red"
        self.pre_delta_label.config(text=f"{pre_straddle_delta:.3f}")
        self.post_delta_label.config(text=f"{post_straddle_delta:.3f}")
        self.delta_change_label.config(text=f"{delta_change:+.3f}", foreground=delta_color)
        
        vega_color = "red" if vega_change < 0 else "green"  # Lower vega = less sensitivity (bad for long straddle)
        self.pre_vega_label.config(text=f"{pre_straddle_vega:.2f}")
        self.post_vega_label.config(text=f"{post_straddle_vega:.2f}")
        self.vega_change_label.config(text=f"{vega_change:+.2f}", foreground=vega_color)
        
        # Create visualizations
        self.create_visualizations()
        
    def create_visualizations(self):
        """Create visualizations for the IV crush analysis"""
        # Clear all axes including any twin axes
        self.ax1.clear()
        self.ax2.clear()
        
        # Remove any existing twin axes
        if self.ax1_twin is not None:
            try:
                self.ax1_twin.remove()
            except:
                pass
            self.ax1_twin = None
        
        # Plot 1: Stock price and IV around earnings
        earnings_window = pd.date_range(start=self.earnings_date - timedelta(days=5), 
                                      end=self.earnings_date + timedelta(days=5), freq='D')
        
        # Filter stock data for the window
        window_stock = self.stock_data[
            (self.stock_data.index >= self.earnings_date - timedelta(days=5)) &
            (self.stock_data.index <= self.earnings_date + timedelta(days=5))
        ]
        
        # Plot stock price
        self.ax1.plot(window_stock.index, window_stock['close'], 'b-', linewidth=2, label='Stock Price')
        self.ax1.axvline(x=self.earnings_date, color='red', linestyle='--', alpha=0.7, label='Earnings Date')
        self.ax1.set_xlabel('Date')
        self.ax1.set_ylabel('Stock Price ($)', color='blue')
        self.ax1.tick_params(axis='y', labelcolor='blue')
        self.ax1.set_title(f'{self.ticker} Stock Price Around Earnings')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(loc='upper left')
        
        # Plot IV if available
        if self.iv_data is not None and len(self.iv_data) > 0:
            window_iv = self.iv_data[
                (self.iv_data.index >= self.earnings_date - timedelta(days=5)) &
                (self.iv_data.index <= self.earnings_date + timedelta(days=5))
            ]
            
            if len(window_iv) > 0:
                self.ax1_twin = self.ax1.twinx()
                # Convert decimal IV to percentage for display (data is already properly scaled and annualized)
                iv_percentage = window_iv['implied_vol'] * 100
                
                self.ax1_twin.plot(window_iv.index, iv_percentage, 'g-', linewidth=2, 
                                  label=f'Implied Volatility (% annualized √252={np.sqrt(252):.1f})')
                self.ax1_twin.set_ylabel('Implied Volatility (% annualized)', color='green')
                self.ax1_twin.tick_params(axis='y', labelcolor='green')
                self.ax1_twin.legend(loc='upper right')
        
        # Plot 2: VIX around earnings (if available)
        if self.vix_data is not None:
            window_vix = self.vix_data[
                (self.vix_data.index >= self.earnings_date - timedelta(days=5)) &
                (self.vix_data.index <= self.earnings_date + timedelta(days=5))
            ]
            
            self.ax2.plot(window_vix.index, window_vix['close'], 'purple', linewidth=2, label='VIX')
            self.ax2.axvline(x=self.earnings_date, color='red', linestyle='--', alpha=0.7, label='Earnings Date')
            self.ax2.set_xlabel('Date')
            self.ax2.set_ylabel('VIX Level')
            self.ax2.set_title('VIX Around Earnings Date')
            self.ax2.grid(True, alpha=0.3)
            self.ax2.legend()
        else:
            # If no VIX data, show straddle price comparison
            option_types = ['Call', 'Put', 'Straddle']
            pre_prices = [float(self.pre_call_label.cget('text').replace('$', '')), 
                         float(self.pre_put_label.cget('text').replace('$', '')),
                         float(self.pre_straddle_label.cget('text').replace('$', ''))]
            post_prices = [float(self.post_call_label.cget('text').replace('$', '')), 
                          float(self.post_put_label.cget('text').replace('$', '')),
                          float(self.post_straddle_label.cget('text').replace('$', ''))]
            
            x = np.arange(len(option_types))
            width = 0.35
            
            # Use different colors for straddle
            colors_pre = ['lightblue', 'lightgreen', 'blue']
            colors_post = ['lightcoral', 'lightpink', 'red']
            
            bars1 = self.ax2.bar(x - width/2, pre_prices, width, label='Pre-Earnings (High IV)', 
                               color=colors_pre, alpha=0.8)
            bars2 = self.ax2.bar(x + width/2, post_prices, width, label='Post-Earnings (Low IV)', 
                               color=colors_post, alpha=0.8)
            
            # Add value labels on bars
            for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
                height1 = bar1.get_height()
                height2 = bar2.get_height()
                self.ax2.text(bar1.get_x() + bar1.get_width()/2., height1 + 0.5,
                            f'${height1:.1f}', ha='center', va='bottom', fontsize=9)
                self.ax2.text(bar2.get_x() + bar2.get_width()/2., height2 + 0.5,
                            f'${height2:.1f}', ha='center', va='bottom', fontsize=9)
            
            self.ax2.set_xlabel('Option Strategy')
            self.ax2.set_ylabel('Option Price ($)')
            self.ax2.set_title('ATM Options & Straddle: IV Crush Impact')
            self.ax2.set_xticks(x)
            self.ax2.set_xticklabels(option_types)
            self.ax2.legend()
            self.ax2.grid(True, alpha=0.3)
            
            # Add a text box showing the IV crush impact
            straddle_loss_text = self.straddle_loss_label.cget('text')
            self.ax2.text(0.02, 0.98, f'Straddle Loss: {straddle_loss_text}', 
                         transform=self.ax2.transAxes, fontsize=12, fontweight='bold',
                         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Format dates on x-axis
        self.ax1.tick_params(axis='x', rotation=45)
        if self.vix_data is not None:
            self.ax2.tick_params(axis='x', rotation=45)
        
        # Update canvas
        self.fig.tight_layout()
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = EarningsTradingDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
