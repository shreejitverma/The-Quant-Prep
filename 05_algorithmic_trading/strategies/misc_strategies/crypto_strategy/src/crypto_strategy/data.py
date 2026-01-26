import os
import time
import pandas as pd
from finlab_crypto.crawler import get_all_binance


def save_stats(stats: pd.DataFrame, output_path, filename) -> None:
    filename = join_path(output_path, filename)
    stats.to_pickle(filename)


def get_acc_returns(daily_returns):
    acc_returns = {
        'Ret [:21-04-14]': (daily_returns[:'2021-04-15'] + 1).cumprod()[-1],
        'Ret [21-04-15:21-07-20]': (daily_returns['2021-04-15':'2021-07-21'] + 1).cumprod()[-1],
        'Ret [21-07-21:21-11-10]': (daily_returns['2021-07-21':'2021-11-11'] + 1).cumprod()[-1],
        'Ret [21-11-11:]': (daily_returns['2021-11-11':] + 1).cumprod()[-1]
    }
    return acc_returns


def check_and_create_dir(dname, *args) -> str:
    dname = os.path.join(dname, *args)
    has_dir = os.path.isdir(dname)
    if not has_dir:
        os.mkdir(dname)
    return dname


def join_path(output_path, filename) -> str:
    return os.path.join(output_path, filename)


def download_crypto_history(symbol, freq) -> pd.DataFrame:
    history = pd.DataFrame()
    try:
        print('try', symbol)
        history = get_all_binance(symbol, freq)
    except Exception as e:
        print('fail', e)
    return history


def download_all_portfolio_data(symbols: list, freq: list, dir_history='history') -> dict:
    check_and_create_dir(dir_history)
    ohlcvs = {}
    for s, f in zip(symbols, freq):
        time.sleep(1)
        ohlcvs[(s, f)] = download_crypto_history(s, f)
    return ohlcvs
