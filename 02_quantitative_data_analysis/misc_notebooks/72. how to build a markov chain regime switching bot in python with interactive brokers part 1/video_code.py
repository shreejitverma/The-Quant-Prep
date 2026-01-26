import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

class IBApp(EWrapper, EClient):

    def __init__(self, callback=None):
        EClient.__init__(self, self)
        self. connected = False
        self.callback = callback
        self.last_price = None
        self.bid_price = None
        self.ask_price = None
        self.historical_data = {}
        self.hist_done = threading.Event()

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        if errorCode in [2104, 2106, 2158, 2176]:
            return
        
        if errorCode == 10167:
            print("Note: Using Delayed Market Data")
            return

        print(f"Error | ReqId: {reqId} | ErrorCode: {errorCode}")
        print(f"Msg: {errorString}")

    def nextValidId(self, orderId):
        self.connected = True
        print("Connected to TWS")
    
    def historicalData(self, reqId, bar):
        if reqId not in self.historical_data:
            self.historical_data[reqId] = []
        self.historical_data[reqId].append({'o':bar.open, 'h':bar.high, 'l':bar.low, 'c':bar.close})

    def historcalDataEnd(self, reqId, start, end):
        self.hist_done.set()
    
    def tickPrice(self, reqId, tickType, price, attrib):
        
        if price <= 0:
            return

        if tickType == 4:
            self.last_price = price
            if self.callback:
                self.callback('price', price, datetime.now())
        elif tickType == 1:
            self.bid_price = price
        elif tickType == 2:
            self.ask_price = price

    def tickSize(self, reqId, tickType, size):
        return
    
    def tickString(self, reqId, tickType, value):
        pass

class OHLCBar:

    def __init__(self, timestamp, open_price):
        self.timestamp = timestamp
        self.open = open_price
        self.high = open_price
        self.low = open_price
        self.close = open_price
        self.tick_count = 1
        self.regime = 0 # Vol Regime: 0=low, 1=med, 2=high

    def update(self, price):
        self.high = max(self.high, price)
        self.low = min(self.low, price)
        self.close = price
        self.tick_count += 1

    @property
    def volatility(self):
        return (self.high - self.low) / self.close if self.close > 0 else 0
    
class MarkovRegime:

    def __init__(self):
        pass

    def calibrate(self, hist_bars):
        pass

    def _gaussian_likelihood(self, vol, regime):
        pass

    def get_regime(self, bars):
        pass

class LiveMarketDashboard:

    def __init__(self, root):
        self.root = root
        self.root.title('Live Market Data Dashboard')
        self.root.geometry('1200x800')
        self.root.configure(bg='#0d1117')
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_dark_theme()

        self.ib_app = IBApp(callback=self.on_tick_data)
        self.connected = False
        self.streaming = False

        self.bar_duration = 5
        self.max_bars = 10
        self.ohlc_bars = deque(maxlen=self.max_bars)
        self.current_bar = None
        self.bar_start_time = None
        self.price_history = deque(maxlen=100)
        self.last_update_time = None
        self.regime_model = MarkovRegime()

        self.bar_lock = threading.Lock()
        self.update_thread = None
        self.running = False

        self.setup_ui()
        self.setup_chart()
    
    def configure_dark_theme(self):
        bg_color = '#0d1117'
        fg_color = '#c9d1d9'
        accent_color = '#238636'
        entry_bg = '#161b22'

        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        self.style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color,
                             font=('Segoe UI', 10, 'bold'))
        self.style.configure('TLabel', background=bg_color, foreground=fg_color,
                             font=('Segoe UI', 10))
        self.style.configure('TButton', background=bg_color, foreground=fg_color,
                             font=('Segoe UI', 9, 'bold'), padding=(10, 5))
        self.style.map('TButton',
                       background=[('active', '#2ea043'), ('disabled', '#21262d')])
        self.style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color,
                             insertcolor=fg_color)
        self.style.configure('Accent.TButton', background='#da3633', foreground='white')
        self.style.map('Accent.TButton',
                       background=[('active', '#f85149'), ('disabled', '#21262d')])
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding='15')
        main_frame.grid(row=0, column=0, sticky='nsew')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))

        title_label = tk.Label(header_frame, text="Live Regime Switching",
                               font=('JetBrains Mono', 18, 'bold'),
                               bg='#0d1117', fg='#58a6ff')
        title_label.pack(side='left')

        self.status_indicator = tk.Label(header_frame, text='DISCONNECTED',
                                         font=('Segoe UI', 10, 'bold'),
                                         bg='#0d1117', fg='#f85149')
        self.status_indicator.pack(side='right', padx=10)

        control_frame = ttk.LabelFrame(main_frame, text='Control Panel', padding='10')
        control_frame.grid(row=1, column=0, sticky='ew', pady=(0, 15))

        conn_section = ttk.Frame(control_frame)
        conn_section.pack(fill='x', pady=(0, 10))

        ttk.Label(conn_section, text="Host:").pack(side='left', padx=(0, 5))
        self.host_var = tk.StringVar(value='127.0.0.1')
        host_entry = ttk.Entry(conn_section, textvariable=self.host_var, width=12)
        host_entry.pack(side='left', padx=(0, 15))

        ttk.Label(conn_section, text="Port:").pack(side='left', padx=(0, 5))
        self.port_var = tk.StringVar(value='7497')
        port_entry = ttk.Entry(conn_section, textvariable=self.port_var, width=12)
        port_entry.pack(side='left', padx=(0, 15))

        self.connect_btn = ttk.Button(conn_section, text="Connect", command=self.connect_ib)
        self.connect_btn.pack(side='left', padx=(0, 5))

        self.disconnect_btn = ttk.Button(conn_section, text="Disconnect",
                                          command=self.disconnect_ib, state='disabled',
                                          style='Accent.TButton')
        self.disconnect_btn.pack(side='left')
        
        sep = ttk.Separator(control_frame, orient='horizontal')
        sep.pack(fill='x', pady=10)

        data_section = ttk.Frame(control_frame)
        data_section.pack(fill='x')

        ttk.Label(data_section, text='Symbol:').pack(side='left', padx=(0, 5))
        self.symbol_var = tk.StringVar(value='AAPL')
        symbol_entry = ttk.Entry(data_section, textvariable=self.symbol_var,
                                 width=10, font=('JetBrains Mono', 11))
        symbol_entry.pack(side='left', padx=(0, 5))

        self.stream_btn = ttk.Button(data_section, text="Start Stream",
                                     command=self.toggle_stream, state='disabled')
        self.stream_btn.pack(side='left', padx=(0, 5))

        self.recal_btn = ttk.Button(data_section, text="Recalibrate",
                                    command=self.recalibrate_model, state='disabled')
        self.recal_btn.pack(side='left', padx=(0, 15))

        price_frame = ttk.Frame(data_section)
        price_frame.pack(side='right')

        ttk.Label(price_frame, text="Last Price:",
                  font=('Segoe UI', 10)).pack(side='left', padx=(0, 5))
        self.price_label = tk.Label(price_frame, text='---.--',
                                    font=('JetBrains Mono', 16, 'bold'),
                                    bg='#0d1117', fg='#7ee787')
        self.price_label.pack(side='left')

        chart_frame = ttk.LabelFrame(main_frame, text='Live OHLC with Markov Regime (5s Bars)', padding='10')
        chart_frame.grid(row=2, column=0, sticky='nsew')
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.rowconfigure(0, weight=1)

        self.chart_container = ttk.Frame(chart_frame)
        self.chart_container.grid(row=0, column=0, sticky='nsew')
        self.chart_container.columnconfigure(0, weight=1)
        self.chart_container.rowconfigure(0, weight=1)

        stats_frame = ttk.Frame(main_frame)
        stats_frame.grid(row=3, column=0, sticky='ew', pady=(10, 0))

        self.stats_labels = {}
        stats = [('Bars', '0'), ('High', '--'), ('Low', '--'),
                 ('Regime', '--'), ('Ticks/Bar', '0')]
        
        for i, (name, val) in enumerate(stats):
            frame = ttk.Frame(stats_frame)
            frame.pack(side='left', padx=15)
            ttk.Label(frame, text=f'{name}:', font=('Segoe UI', 9)).pack(side='left')
            label = tk.Label(frame, text=val, font=('JetBrains Mono', 10, 'bold'),
                             bg='#0d1117', fg='#8b949e')
            label.pack(side='left', padx=(5, 0))
            self.stats_labels[name] = label

    def setup_chart(self):

        plt.style.use('dark_background')

        self.fig, self.ax = plt.subplots(figsize=(12, 6), facecolor='#0d1117')
        self.ax.set_facecolor('#161b22')

        self.ax.tick_params(colors='#8b949e', labelsize=9)
        self.ax.spines['bottom'].set_color('#30363d')
        self.ax.spines['top'].set_color('#30363d')
        self.ax.spines['left'].set_color('#30363d')
        self.ax.spines['right'].set_color('#30363d')
        self.ax.grid(True, alpha=.2, color='#30363d', linestyle='--')

        self.ax.set_xlabel('Time', color='#8b949e', fontsize=10)
        self.ax.set_ylabel('Price', color='#8b949e', fontsize=10)
        self.ax.set_title('Waiting for data. . .', color='#c9d1d9', fontsize=12, fontweight='bold')

        self.canvas = FigureCanvasTkAgg(self.fig, self.chart_container)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        self.fig.tight_layout()
        self.canvas.draw()

    def create_contract(self, symbol):
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        return contract

    def connect_ib(self):

        try:
            host = self.host_var.get()
            port = int(self.port_var.get())

            def connect_thread():
                try:
                    self.ib_app.connect(host, port, clientId=1)
                    self.ib_app.run()
                except Exception as e:
                    print(f"Connection error: {e}")

            thread = threading.Thread(target=connect_thread, daemon=True)
            thread.start()

            for i in range(50):
                if self.ib_app.connected:
                    break
                time.sleep(.1)

            if self.ib_app.connected:
                self.connected = True
                self.connect_btn.config(state='disabled')
                self.disconnect_btn.config(state='normal')
                self.stream_btn.config(state='normal')
                self.status_indicator.config(text='CONNECTED', fg='#7ee787')
            else:
                messagebox.showerror('Error', 'Failed to connect to TWS')
        except Exception as e:
            messagebox.showerror('Error', f"Connection error: {e}")

    def disconnect_ib(self):
        try:
            if self.streaming:
                self.stop_stream()
            
            self.ib_app.disconnect()
            self.connected = False
            self.connect_btn.config(state='normal')
            self.disconnect_btn.config(state='disabled')
            self.stream_btn.config(state='disabled')
            self.status_indicator.config(text='DISCONNECTED', fg="#cb0000")

        except Exception as e:
            print(f"Disconnect error: {e}")
    

    def toggle_stream(self):
        if not self.streaming:
            self.start_stream()
        else:
            self.stop_stream()
    
    def start_stream(self):
        if not self.connected:
            return
        
        symbol = self.symbol_var.get().upper()
        if not symbol:
            messagebox.showerror('Error', 'Please enter a symbol')
            return
        
        with self.bar_lock:
            self.ohlc_bars.clear()
            self.current_bar = None
            self.bar_start_time = None
            self.price_history.clear()
            self.regime_model = MarkovRegime()
        
        contract = self.create_contract(symbol)

        self.ib_app.historical_data.clear()
        self.ib_app.hist_done.clear()
        self.ib_app.reqHistoricalData(2, contract, "", "300 S", "5 secs", "TRADES", 1, 1, False, [])

        if self.ib_app.hist_done.wait(timeout=10) and 2 in self.ib_app.historical_data:
            self.regime_model.calibrate(self.ib_app.historical_data[2])
            print(f"Calibrated regime model with {len(self.ib_app.historical_data[2])} bars")

        self.ib_app.reqMktData(1, contract, "", False, False, [])

        self.streaming = True
        self.running = True
        self.stream_btn.config(text='Stop Stream', style='Accent.TButton')
        self.recal_btn.config(text='normal')
        self.status_indicator.config(text=f'Streaming {symbol}', fg='#58a6ff')

        self.update_thread = threading.Thread(target=self.bar_manager_loop, daemon=True)
        self.update_thread.start()

        self.update_chart_loop()

    def stop_stream(self):
        self.running = False
        self.streaming = False

        try:
            self.ib_app.cancelMktData(1)
        except Exception as e:
            print(f"Error canceling market data request: {e}")

        self.stream_btn.config(text='Start Stream', style='TButton')
        self.recal_btn.config(state='disable')
        self.status_indicator.config(text="CONNECTED", fg='#7ee787')

    def recalibrate_model(self):
        pass

    def on_tick_data(self, data_type, value, timestamp):

        if data_type == 'price' and value > 0:
            with self.bar_lock:
                self.price_history.append((timestamp, value))

                if self.current_bar is None:
                    self.current_bar = OHLCBar(timestamp, value)
                    self.bar_start_time = timestamp
                else:
                    self.current_bar.update(value)

            self.root.after(0, lambda: self.price_label.config(text=f'{value:.2f}'))

    def bar_manager_loop(self):
        while self.running:
            time.sleep(.1)

            with self.bar_lock:
                if self.current_bar is not None and self.bar_start_time is not None:
                    elapsed = (datetime.now() - self.bar_start_time).total_seconds()

                    if elapsed >= self.bar_duration:
                        self.ohlc_bars.append(self.current_bar)
                        self.regime_model.get_regime(list(self.ohlc_bars))
                        last_price = self.current_bar.close
                        self.current_bar = OHLCBar(datetime.now(), last_price)
                        self.bar_start_time = datetime.now()

    def update_chart_loop(self):
        if not self.running:
            return
        self.draw_ohlc_chart()
        self.update_stats()
        self._after_id = self.root.after(200, self.update_chart_loop)

    def draw_ohlc_chart(self):

        self.ax.clear()

        with self.bar_lock:
            bars = list(self.ohlc_bars)
            current = self.current_bar
        
        if current is not None:
            bars = bars + [current]

        if not bars:
            self.ax.set_facecolor('#161b22')
            self.ax.set_title('Waiting for data. . .', color='#c9d1d9', fontsize=12, fontweight='bold')
            self.ax.grid(True, alpha=.2, color='#30363d', linestyle='--')
            return
        
        all_prices = [bar.low for bar in bars] + [bar.high for bar in bars]
        price_min, price_max = min(all_prices), max(all_prices)
        price_range = price_max - price_min
        padding = max(price_range * .1, .01)
        y_min, y_max = price_min - padding, price_max + padding

        if current is not None:
            # get the regime's current state
            pass

        width = .6

        for i, bar in enumerate(bars):
            bg = Rectangle(
                (i - .5, y_min),
                1,
                y_max - y_min,
                facecolor = (1, 1, 1, 0), # update with current regime
                edgecolor='none',
                alpha=0,
                zorder=0
            )

            self.ax.add_patch(bg)

            color, edge_color = ('#3fb950', '#7ee787') if bar.close >= bar.open else ('#f85149', '#ff7b72')
            body_bottom, body_height = min(bar.open, bar.close), max(abs(bar.close - bar.open), .001)

            rect = Rectangle(
                (i - width/2, body_bottom),
                width,
                body_height,
                facecolor = color,
                edgecolor = edge_color,
                linewidth=1.5,
                alpha=.9,
                zorder=2
            )
            self.ax.add_patch(rect)

            self.ax.plot([i, i], [bar.low, body_bottom], color=edge_color, linewidth=1.5, zorder=1)
            self.ax.plot([i, i], [body_bottom + body_height, bar.high], color=edge_color, linewidth=1.5, zorder=1)

            if i == len(bars) - 1 and current is not None:
                self.ax.axvline(x=i, color='#58a6ff', alpha=.3, linestyle=':', linewidth=2)
            
        self.ax.set_facecolor('#161b22')

        x_labels = [bar.timestamp.strftime('%H:%M:%S') for bar in bars]
        self.ax.set_xticks(range(len(bars)))
        self.ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xlim(-.5, max(self.max_bars - .5, len(bars) - .5))

        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.3f}'))

        # ** may need to reapply styling

        self.ax.set_xlabel('Time', color='#8b949e', fontsize=10)
        self.ax.set_ylabel('Price', color='#8b949e', fontsize=10)

        symbol = self.symbol_var.get().upper()
        regime_names = ['LOW', 'MED', 'HIGH']
        curr_regime = regime_names[bars[-1].regime] if bars else 'N/A'
        self.ax.set_title(f'{symbol} - Regime: {curr_regime} | {len(bars)}/{self.max_bars} bars',
                          color = '#c9d1d9', fontsize=12, fontweight='bold')

        self.fig.tight_layout()
        self.canvas.draw_idle()
    
    def update_stats(self):
        with self.bar_lock:
            bars = list(self.ohlc_bars)
            current = self.current_bar

        if current:
            bars = bars + [current]
        
        if not bars:
            return
        
        self.stats_labels['Bars'].config(text=str(len(bars)))

        all_highs = [b.high for b in bars]
        all_lows = [b.low for b in bars]
        self.stats_labels['High'].config(text=f'{max(all_highs)}')
        self.stats_labels['Low'].config(text=f'{min(all_lows)}')

        regime_names = ['LOW', 'MED', 'HIGH']
        regime_colors = ['#3fb950', '#d29922', '#f85149']
        curr_regime = bars[-1].regime if bars else 0
        self.stats_labels['Regime'].config(text=regime_names[curr_regime], fg=regime_colors[curr_regime])

        if current:
            self.stats_labels['Ticks/Bar'].config(text=str(current.tick_count))
        
    def on_closing(self):
        self.running = False

        if hasattr(self, '_after_id'):
            self.root.after_cancel(self._after_id)
        
        if self.connected:
            try:
                if self.streaming:
                    self.ib_app.cancelMktData(1)
                self.ib_app.disconnect()
            except Exception as e:
                print(f"Error closing the application: {e}")

        self.root.destroy()


def main():
    root = tk.Tk()
    app = LiveMarketDashboard(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()