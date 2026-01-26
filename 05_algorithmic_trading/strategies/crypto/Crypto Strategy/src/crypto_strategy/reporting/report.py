import os
from collections import defaultdict
from datetime import datetime
import pandas as pd
from crypto_strategy.reporting.plot import plot_returns
from crypto_strategy.strategies.bo_strategy import returns_timeline
from .base import GenerateReport


class GenerateMaReport(GenerateReport):
    def __init__(self, symbols, date, res_dir):
        super().__init__(symbols, date, res_dir)

    def print_params(self, params):
        print(f'{params[0]:}')
        print(f'Best MA Strategy: {params[2]}')
        print(f'n1: {params[3]}')
        print(f'n2: {params[4]}')
        if 'mmi' in params:
            print(f'mmi_timeperiod: {params[6]}')


class GenerateBoReport(GenerateReport):
    def __init__(self, symbols, date, res_dir):
        super().__init__(symbols, date, res_dir)

    def print_params(self, params):
        print(f'{params[0]:}')
        print(f'long_window: {params[2]}')
        print(f'short_window: {params[3]}')
        if 'vol' in params:
            print(f'multiplier: {params[6]}')
            print(f'timeperiod: {params[5]}')


def generate_report(symbol, res_dir='results/'):
    metrics = [
        'Total Return [%]', 'Buy & Hold Return [%]',
        'Num. Trades', 'Win Rate [%]', 'Max. Drawdown [%]', 'Best Trade [%]', 'Worst Trade [%]',
        'Expectancy', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio',
        'Start', 'End', 'Duration',
        'Ret [:21-04-14]', 'Ret [21-04-15:21-07-20]', 'Ret [21-07-21:21-11-10]', 'Ret [21-11-11:]',
        ]
    table = list()
    images = defaultdict(list)
    for tm_folder in os.listdir(res_dir):
        if tm_folder.startswith('best-'):
            cur_path = os.path.join(res_dir, tm_folder)
            date_folder = sorted([int(f) for f in os.listdir(cur_path) if not f.startswith('.')])
            asset_file = []
            _cur_path = cur_path
            # handle assets in multiple bases
            while not asset_file and date_folder:
                cur_path = os.path.join(_cur_path, str(date_folder[-1]))
                asset_file = [f for f in os.listdir(cur_path) if f.startswith(symbol)]
                date_folder.pop()
            for f in asset_file:
                entry = dict()
                if f.endswith('.pkl'):
                    entry['Method'] = tm_folder
                    entry['Params'] = '-'.join(f.split('-')[1:-3])
                    stats = pd.read_pickle(os.path.join(cur_path, f))
                    stats = stats[~stats.index.duplicated('last')]
                    for m in metrics:
                        # backwards compatible
                        if m not in stats:
                            if m == 'Buy & Hold Return [%]':
                                entry[m] = stats['Benchmark Return [%]']
                            if m == 'Num. Trades':
                                entry[m] = stats['Total Trades']
                            if m == 'Max. Drawdown [%]':
                                entry[m] = stats['Max Drawdown [%]']
                        else:
                            entry[m] = stats[m]
                    entry['Start'] = entry['Start'].strftime('%Y-%m-%d')
                    entry['End'] = entry['End'].strftime('%Y-%m-%d')
                    table.append(entry)
                if f.endswith('.png'):
                    images[tm_folder].append(os.path.join(cur_path, f))
    # create HTML file
    table = pd.DataFrame(table)
    table.sort_values(by='Method', inplace=True)
    date = datetime.today().strftime('%Y-%m-%d')
    heading = f'<h1> {symbol} Trading Strategies Testing Report</h1>'
    subheading = f'<h3> Best Params for each strategy {date}</h3>'
    header = f'<div class="top">{heading}{subheading}</div>'
    div_table = f'<div class="table"> {table.to_html()} </div>'
    div_images = ''
    for img in images:
        div_images += f'<h3> {img}</h3>'
        img_tag = f'<img src="../{images[img][0]}">'
        div_images += f'<div class="chart"> {img_tag} </div>'
        img_tag = f'<img src="../{images[img][1]}">'
        div_images += f'<div class="chart"> {img_tag} </div>'
    html_file = header + div_table + div_images
    with open(f'reports/report-{symbol}-{date}.html', 'w') as f:
        f.write(html_file)


def reporting_add_rets_timeline(symbol, method_path):
    if 'bo' in method_path.split('-'):
        strategy = 'bo'
    flag_ts_stop = True if 'ts_stop' in method_path else False
    if 'vol' in method_path:
        flag_filter = 'vol'
    elif 'ang' in method_path:
        flag_filter = 'ang'
    else:
        flag_filter = None
    date_folder = sorted([int(f) for f in os.listdir(method_path) if not f.startswith('.')])
    asset_file = []
    cur_path = method_path
    _cur_path = cur_path
    # handle assets in multiple bases
    while not asset_file and date_folder:
        cur_path = os.path.join(_cur_path, str(date_folder[-1]))
        asset_file = [f for f in os.listdir(cur_path) if f.startswith(symbol)]
        date_folder.pop()
    for f in asset_file:
        if f.endswith('.pkl'):
            print(f)
            parts = f.split('-')[:-3]
            symbol = parts[0]
            freq = parts[1]
            long_window = int(parts[3])
            short_window = int(parts[4])
            if flag_ts_stop:
                ts_stop = float(parts[6])
            else:
                ts_stop = None
            timeperiod, threshold, multiplier = None, None, None
            if flag_filter == 'ang':
                timeperiod = int(parts[-2])
                threshold = int(parts[-1])
            if flag_filter == 'vol':
                timeperiod = int(parts[-2])
                multiplier = int(parts[-1])
            ret = returns_timeline(
                symbol, freq,
                long_window, short_window,
                strategy, ts_stop,
                timeperiod, multiplier, threshold,
                flag_filter, flag_ts_stop
                )
            ser = pd.read_pickle(os.path.join(cur_path, f))
            if list(ret.keys())[-1] not in ser.index:
                ser = ser.append(pd.Series(ret))
                ser.to_pickle(os.path.join(cur_path, f))


def portfolio_returns(start_date, btc_ohlcv, eth_ohlcv, pf_daily_returns):
    if isinstance(start_date, str):
        start = start_date
        # print(f'Portfolio Returns Since {start_date}')
    if isinstance(start_date, int):
        # print(f'{start_date}-Day Portfolio Returns')
        start = -start_date
    # BTC | ETH Buy & Hold
    btc_daily_returns = btc_ohlcv[start:].close.pct_change().fillna(0)
    btc_acc_returns = (btc_daily_returns + 1).cumprod()
    # print(f'''BTC: {btc_acc_returns.last('1D') - 1}''')
    eth_daily_returns = eth_ohlcv[start:].close.pct_change().fillna(0)
    eth_acc_returns = (eth_daily_returns + 1).cumprod()
    # print(f'''ETH: {eth_acc_returns.last('1D') - 1}''')
    # Portfolio Returns
    pf_daily_returns = pf_daily_returns[start:].copy()
    pf_daily_returns.iloc[0] = 0
    pf_acc_returns = (pf_daily_returns + 1).cumprod().mean(axis=1)
    # print(f'''Portfolio: {pf_acc_returns.tail(1) - 1}''')
    plot_returns(btc_acc_returns, eth_acc_returns, pf_acc_returns, start_date)
