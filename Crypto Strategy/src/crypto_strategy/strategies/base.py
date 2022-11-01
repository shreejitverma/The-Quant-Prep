import os
import pathlib
from typing import Union
from datetime import datetime
from abc import ABC, abstractmethod
import talib
import numpy as np
import pandas as pd
from finlab_crypto.indicators import trends
from finlab_crypto.strategy import Strategy, Filter
from crypto_strategy.reporting.plot import plot_indicators
from crypto_strategy.data import check_and_create_dir, download_crypto_history


@Strategy(name='sma', n1=20, n2=40)
def trend_strategy(ohlcv):
    name = trend_strategy.name
    n1 = trend_strategy.n1
    n2 = trend_strategy.n2
    filtered1 = trends[name](ohlcv.close, n1)
    filtered2 = trends[name](ohlcv.close, n2)
    entries = (filtered1 > filtered2) & (filtered1.shift() < filtered2.shift())
    exits = (filtered1 < filtered2) & (filtered1.shift() > filtered2.shift())
    figures = {
        'overlaps': {
            'trend1': filtered1,
            'trend2': filtered2,
        }
    }
    return entries, exits, figures


@Strategy(long_window=30, short_window=30)
def breakout_strategy(ohlcv):
    lw = breakout_strategy.long_window
    sw = breakout_strategy.short_window
    ub = ohlcv.close.rolling(lw).max()
    lb = ohlcv.close.rolling(sw).min()
    entries = ohlcv.close == ub
    exits = ohlcv.close == lb
    figures = {
        'overlaps': {
            'ub': ub,
            'lb': lb
        }
    }
    return entries, exits, figures


# macd strategy
@Strategy(fastperiod=12, slowperiod=26, signalperiod=9)
def macd_strategy(ohlcv):
    macd, signal, macdhist = talib.MACD(
        ohlcv.close,
        fastperiod=macd_strategy.fastperiod,
        slowperiod=macd_strategy.slowperiod,
        signalperiod=macd_strategy.signalperiod
    )

    entries = (macdhist > 0) & (macdhist.shift() < 0)
    exits = (macdhist < 0) & (macdhist.shift() > 0)
    figures = {
        'figures': {
            'macdhist': macdhist
        }
    }
    return entries, exits, figures


@Strategy(fastperiod=12, slowperiod=26, signalperiod=9)
def macd_strategy_revised(ohlcv):
    macd, signal, macdhist = talib.MACD(
        ohlcv.close,
        fastperiod=macd_strategy.fastperiod,
        slowperiod=macd_strategy.slowperiod,
        signalperiod=macd_strategy.signalperiod
    )
    entries = (macdhist > 0) & (macdhist.shift() < 0) & (macd > 0)
    exits = (macdhist < 0) & (macdhist.shift() > 0) & (macd < 0)
    figures = {
        'macd': {
            'macdhist': macdhist
            }
        }
    return entries, exits, figures


@Strategy(timeperiod=14, buy_threshold=52, sell_threshold=50)
def rsi_strategy(ohlcv):
    rsi = talib.RSI(ohlcv.close, timeperiod=rsi_strategy.timeperiod)
    entries = (rsi > rsi_strategy.buy_threshold) & (rsi.shift() < rsi_strategy.buy_threshold)
    exits = (rsi < rsi_strategy.sell_threshold) & (rsi.shift() > rsi_strategy.sell_threshold)
    figure = {
        'figures': {
            'rsi': rsi
        }
    }
    return entries, exits, figure


@Filter(timeperiod=20)
def mmi_filter(ohlcv):
    median = ohlcv.close.rolling(mmi_filter.timeperiod).median()
    p1 = ohlcv.close > median
    p2 = ohlcv.close.shift() > median
    mmi = (p1 & p2).astype(int).rolling(mmi_filter.timeperiod).mean()
    figures = {
      'figures': {
          'mmi_index': mmi
      }
    }
    return mmi >= 0.5, figures


@Filter(timeperiod=20, multiplier=2)
def vol_filter(ohlcv):
    vol_mean = ohlcv.volume.rolling(vol_filter.timeperiod).mean()
    vol = ohlcv.volume / (vol_filter.multiplier * vol_mean)
    figures = {
      'figures': {
          'vol_index': vol
      }
    }
    return vol >= 1, figures


@Filter(timeperiod=20, threshold=0)
def ang_filter(ohlcv):
    ang = talib.LINEARREG_ANGLE(ohlcv.close, ang_filter.timeperiod)
    figures = {
        'figures': {
            'ang_index': ang
        }
    }
    return ang > ang_filter.threshold, figures


@Filter(side='long', fast=5, slow=3, matype=0)
def stoch_filter(ohlcv):
    side = stoch_filter.side
    fast = stoch_filter.fast
    slow = stoch_filter.slow
    matype = stoch_filter.matype
    k, d = talib.STOCH(
        ohlcv.high, ohlcv.low, ohlcv.close,
        fastk_period=fast, slowk_period=slow, slowk_matype=matype,
        slowd_period=slow, slowd_matype=matype)
    signals = (k > d) & (k > 50) & (k < 50) if side == 'long' else k < d
    fig = {
        'figures': {
            'kd': {'k': k, 'd': d}
        }
    }
    return signals, fig


@Filter(timeperiod=50)
def sma_filter(ohlcv):
    sma = talib.SMA(ohlcv.close, timeperiod=sma_filter.timeperiod)
    figures = {
      'figures': {
          'sma': sma
      }
    }
    return ohlcv.close > sma, figures


class BestStrategy(ABC):
    def __init__(self,
                 symbols: Union[str, list],
                 freq: list,
                 res_dir: str,
                 flag_filter: str,
                 strategy: str):
        self._sanity_check(flag_filter, res_dir)
        self.symbols = [symbols] if isinstance(symbols, str) else symbols
        self.freq = freq
        self.flag_filter = flag_filter
        self.strategy_name = strategy
        self.strategy = self._get_strategy(strategy)
        self.date_str = datetime.today().date().strftime("%Y-%m-%d")
        self.output_path = check_and_create_dir(res_dir, self.date_str.replace('-', ''))
        self.output_path = pathlib.Path(self.output_path)

    @staticmethod
    def _sanity_check(flag_filter, res_dir):
        if flag_filter and flag_filter not in res_dir:
            raise ValueError(f'The res_dir name should contain {flag_filter} filter')
        if not flag_filter and 'filter' in res_dir:
            raise ValueError('The res_dir name should not contain filter name')

    @abstractmethod
    def _get_strategy(self, strategy):
        pass

    @abstractmethod
    def grid_search_params(self):
        pass

    @abstractmethod
    def _get_grid_search(self):
        pass

    @abstractmethod
    def apply_best_params(self):
        pass

    def get_best_params(self, total_best_params, n=10):
        total_best_params = (
            pd.DataFrame(total_best_params)
            .sort_values(by='sharpe')
        )
        print(total_best_params.head(n))
        return total_best_params.tail(1).to_dict(orient='records')[0]

    def backtest(self, variables, filters=dict(), n=10):
        portfolio = self.strategy.backtest(self.ohlcv, freq=self.freq, variables=variables, filters=filters)
        best_params = portfolio.sharpe_ratio().replace([np.inf, -np.inf], np.nan).dropna().nlargest(n)
        best_params = (
            best_params
            .rename('sharpe')
            .reset_index()
            .to_dict(orient='records')
        )
        return best_params

    def generate_best_params(self):
        print(f'The search for {self.symbols} starts now')
        for symbol in self.symbols:
            print(f'Start the search for {symbol}')
            self.ohlcv = download_crypto_history(symbol, self.freq)
            best_params = self._get_grid_search()
            print(f'Found the best params {best_params}')
            self.apply_best_params(best_params, symbol)
        print('The search for all the symbols is completed')


class CheckIndicators(ABC):
    def __init__(self,
                 symbols: Union[str, list],
                 date: str,
                 res_dir: str,
                 flag_filter: str,
                 strategy: str,
                 show_fig: bool = False):
        self.symbols = [symbols] if isinstance(symbols, str) else symbols
        self.date = date
        self.flag_filter = flag_filter
        self.res_dir = os.path.join(res_dir, date.replace('-', ''))
        self.strategy = self._get_strategy(strategy)
        self.show_fig = show_fig

    @abstractmethod
    def _get_strategy(self, strategy):
        pass

    @abstractmethod
    def _get_variables(self):
        pass

    @abstractmethod
    def _get_filter(self):
        pass

    def check_indicators(self):
        print(f'Start checking the optimized params for {self.symbols}')
        for symbol in self.symbols:
            if os.path.isdir(self.res_dir) and symbol:
                res = os.listdir(self.res_dir)
                for r in res:
                    if r.startswith(symbol) and r.endswith(self.date+'.pkl'):
                        comp = r.split('-')
                        assert symbol == comp[0], 'asset name doesn\'t match the file name'
                        freq = comp[1]
                        self.trend = comp[2] if comp[2].isalpha() else None
                        ohlcv = download_crypto_history(symbol, freq)
                        if self.trend:
                            variables = self._get_variables(name=self.trend)
                        else:
                            variables = self._get_variables()
                        filters = self._get_filter()
                        portfolio = self.strategy.backtest(ohlcv, freq=freq, variables=variables, filters=filters)
                        filename = f'{symbol}-{freq}-{self.trend}-{self.date}'
                        plot_indicators(portfolio, self.res_dir, filename, self.show_fig)


class InspectStrategy(ABC):
    def __init__(self,
                 symbol: str,
                 freq: str,
                 flag_filter: str,
                 strategy: str,
                 show_fig: bool = True):
        self.symbol = symbol
        self.freq = freq
        self.flag_filter = flag_filter
        self.strategy = self._get_strategy(strategy)
        self.show_fig = show_fig
        self.ohlcv = download_crypto_history(symbol, freq)

    @abstractmethod
    def _get_strategy(self, strategy):
        pass

    @abstractmethod
    def _get_variables(self):
        pass

    @abstractmethod
    def _get_filter(self):
        pass

    def inspect(self):
        self.portfolio = self.strategy.backtest(
            self.ohlcv,
            variables=self._get_variables(),
            filters=self._get_filter(),
            freq=self.freq,
            plot=self.show_fig)
