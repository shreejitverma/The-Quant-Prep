import os
import numpy as np
import pandas as pd
from finlab_crypto.online import TradingPortfolio


def create_trading_portfolio(trading_methods: list, key=None, secret=None):
    if not (key and secret):
        key = os.environ.get('KEY')
        secret = os.environ.get('SECRET')
    if key and secret:
        tp = TradingPortfolio(key, secret)
    else:
        raise ValueError('No trading KEY or SECRET provided')
    if trading_methods:
        for tm in trading_methods:
            tp.register(tm)
        tp.register_margin('USDT', 1000 * len(trading_methods))
    else:
        print('Please provide trading methods')
    return tp


def concat_assets(ohlcv, symbols, start_bar=2000):
    close_ref = pd.Series(np.concatenate([
        ohlcv[s].close.astype(float).pct_change().values[start_bar:] for s in symbols]))
    ret_close = (close_ref + 1).cumprod()

    # use concatenate and list comprehension
    close = pd.Series(np.concatenate([
        ohlcv[s].close.astype(float).values[start_bar:] for s in symbols]))
    high = pd.Series(np.concatenate([
        ohlcv[s].high.astype(float).values[start_bar:] for s in symbols]))
    low = pd.Series(np.concatenate([
        ohlcv[s].low.astype(float).values[start_bar:] for s in symbols]))
    open_ = pd.Series(np.concatenate([
        ohlcv[s].open.astype(float).values[start_bar:] for s in symbols]))
    volume = pd.Series(np.concatenate([
        ohlcv[s].volume.astype(float).values[start_bar:] for s in symbols]))

    ret_high = ret_close * high / close
    ret_low = ret_close * low / close
    ret_open = ret_close * open_ / close
    # ret_asset = pd.Series(np.concatenate([[s] * (len(ohlcv[s])-start_bar) for s in symbols]))

    # assert len(ret_asset) == len(ret_close)
    min_datetime = min([ohlcv[s][start_bar:].index.min() for s in symbols])
    # index = pd.MultiIndex.from_arrays(
    # [ret_asset, pd.date_range(min_datetime, periods=len(ret_close), freq='4h').tolist()],
    # names=('asset', 'interval'))

    index = pd.date_range(min_datetime, periods=len(ret_close), freq='4h')
    return pd.DataFrame({
        'open': ret_open.values,
        'high': ret_high.values,
        'low': ret_low.values,
        'close': ret_close.values,
        'volume': volume.values,
    }, index=index).dropna()
