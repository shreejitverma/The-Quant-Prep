from typing import Union
import numpy as np
import pandas as pd
from crypto_strategy.data import (
    save_stats,
    get_acc_returns,
    download_crypto_history
)
from .base import (
    breakout_strategy,
    vol_filter, ang_filter,
    BestStrategy, InspectStrategy, CheckIndicators
)


RANGE_WINDOW = np.arange(10, 200, 5)
RANGE_TIMEPERIOD = np.arange(5, 55, 5)
RANGE_MULTIPLIER = np.arange(1, 10, 1)
RANGE_THRESHOLD = np.arange(0, 60, 5)
RANGE_STOP = np.arange(0.1, 0.6, 0.05)


def create_vol_filter(flag_filter, **kwargs):
    filters = dict()
    if flag_filter:
        if kwargs:
            assert kwargs.get('timeperiod') and kwargs.get('multiplier'),\
                'Volume fitler doesn\'t have config params provided'
            filter_config = dict(
                timeperiod=kwargs['timeperiod'],
                multiplier=kwargs['multiplier']
            )
        else:
            filter_config = dict(
                timeperiod=RANGE_TIMEPERIOD,
                multiplier=RANGE_MULTIPLIER
            )
        filters = {
            'vol': vol_filter.create({
                'timeperiod': filter_config['timeperiod'],
                'multiplier': filter_config['multiplier']
            })
        }
    return filters


def create_ang_filter(flag_filter, **kwargs):
    filters = dict()
    if flag_filter:
        if kwargs:
            assert kwargs.get('timeperiod') and kwargs.get('threshold') is not None,\
                'Angle filter doesn\'t have config params provided'
            filter_config = dict(
                timeperiod=kwargs['timeperiod'],
                threshold=kwargs['threshold']
            )
        else:
            filter_config = dict(
                timeperiod=RANGE_TIMEPERIOD,
                threshold=RANGE_THRESHOLD
            )
        filters = {
            'ang': ang_filter.create({
                'timeperiod': filter_config['timeperiod'],
                'threshold': filter_config['threshold']
            })
        }
    return filters


def get_filter(flag_filter, **kwargs):
    filters = dict()
    if flag_filter == 'vol':
        filters = create_vol_filter(flag_filter, **kwargs)
    if flag_filter == 'ang':
        filters = create_ang_filter(flag_filter, **kwargs)
    return filters


def get_strategy(strategy):
    if strategy == 'bo':
        return breakout_strategy
    else:
        raise ValueError('Strategy not recognized. Please choose from bo and bo_rev')


def create_bo_variables(**kwargs):
    variables = dict()
    if kwargs.get('long_window') and kwargs.get('short_window'):
        variables = kwargs
    elif not (kwargs.get('long_window') or kwargs.get('short_window')):
        variables['long_window'] = RANGE_WINDOW
        variables['short_window'] = RANGE_WINDOW
    else:
        raise ValueError('BO strategy doesn\'t have config params provided')
    return variables


def create_bo_variables_with_stop(**kwargs):
    variables = create_bo_variables(**kwargs)
    if not (kwargs.get('long_window') or kwargs.get('short_window')):
        flag_stop = kwargs.get('flag_stop')
        if kwargs.get('flag_stop'):
            if not set(flag_stop).issubset(['ts_stop', 'sl_stop', 'tp_stop']):
                raise ValueError('The value of flag_stop is not supported')
            for fs in flag_stop:
                variables[fs] = RANGE_STOP
        else:
            raise ValueError('flag_stop is not set')
    return variables


class BestBoStrategy(BestStrategy):
    '''
    This class provides the method to optimize the BO strategy
    symbols: a list of symbols to be optimzied on, e.g., ['BTCUSDT']
    freq: currently supported values: '1h' or '4h'
    res_dir: the output directory
    flag_filter: currently supported fitlers: 'vol', 'ang', default: None
    flag_ts_stop: flag to turn on/off trailing stop
    strategy: 'bo'
    '''
    def __init__(self,
                 symbols: Union[str, list],
                 freq: str,
                 res_dir: str,
                 flag_filter: str = None,
                 flag_stop: Union[str, list] = None,
                 flag_acc_return: bool = True,
                 strategy: str = 'bo',
                 ):
        super().__init__(symbols, freq, res_dir, flag_filter, strategy)
        self.flag_stop = [flag_stop] if isinstance(flag_stop, str) else flag_stop
        self.flag_acc_return = flag_acc_return
        self.generate_best_params()

    def _get_strategy(self, strategy):
        return get_strategy(strategy)

    def _get_filter(self, **kwargs):
        return get_filter(flag_filter=self.flag_filter, **kwargs)

    def _get_variables(self, **kwargs):
        if self.flag_stop:
            return create_bo_variables_with_stop(flag_stop=self.flag_stop, **kwargs)
        return create_bo_variables(**kwargs)

    def _get_grid_search(self):
        if self.flag_filter == 'vol':
            return self.grid_search_vol_params()
        elif self.flag_filter == 'ang':
            return self.grid_search_ang_params()
        else:
            return self.grid_search_params()

    def get_best_params(self, total_best_params, n=10):
        total_best_params = pd.DataFrame(total_best_params)
        total_best_params['sharpe'] = (total_best_params['sharpe'] + 0.05).round(1)
        total_best_params['gap'] = total_best_params['long_window'] - total_best_params['short_window']
        if 'ohlcstx_sl_stop' in total_best_params.columns:
            total_best_params = (
                total_best_params
                .query('gap > 0')
                .sort_values(
                    by=['sharpe', 'gap', 'short_window', 'ohlcstx_sl_stop'],
                    ascending=[True, True, False, False])
            )
        else:
            total_best_params = (
                total_best_params
                .query('gap > 0')
                .sort_values(
                    by=['sharpe', 'gap', 'short_window'],
                    ascending=[True, True, False]
                    )
            )
        print(total_best_params)
        return total_best_params.tail(1).to_dict(orient='records')[0] if not total_best_params.empty else None

    def grid_search_params(self):
        variables = self._get_variables()
        best_params = self.backtest(variables)
        return self.get_best_params(best_params)

    def grid_search_vol_params(self):
        variables = self._get_variables()
        total_best_params = list()
        for multiplier in RANGE_MULTIPLIER:
            for timeperiod in RANGE_TIMEPERIOD:
                filters = self._get_filter(timeperiod=timeperiod, multiplier=multiplier)
                best_params = self.backtest(variables, filters)
                total_best_params.extend(best_params)
        return self.get_best_params(total_best_params)

    def grid_search_ang_params(self):
        variables = self._get_variables()
        total_best_params = list()
        for threshold in RANGE_THRESHOLD:
            for timeperiod in RANGE_TIMEPERIOD:
                filters = self._get_filter(timeperiod=timeperiod, threshold=threshold)
                best_params = self.backtest(variables, filters)
                total_best_params.extend(best_params)
        return self.get_best_params(total_best_params)

    def apply_best_params(self, best_params, symbol):
        variables = self._get_variables(
            long_window=best_params['long_window'],
            short_window=best_params['short_window']
        )
        if 'ts_stop' in self.flag_stop:
            variables.update(ts_stop=best_params.get('ohlcstx_sl_stop'))
        if 'sl_stop' in self.flag_stop:
            variables.update(sl_stop=best_params.get('ohlcstx_sl_stop'))
        if 'tp_stop' in self.flag_stop:
            variables.update(tp_stop=best_params.get('ohlcstx_tp_stop'))
        filters = self._get_filter(
            timeperiod=best_params.get('vol_timeperiod') if best_params.get('vol_timeperiod') else best_params.get('ang_timeperiod'),
            multiplier=best_params.get('vol_multiplier'),
            threshold=best_params.get('ang_threshold')
            )
        filename = f'''{symbol}-{self.freq}-{self.strategy_name}-{best_params['long_window']}-{best_params['short_window']}-'''
        if self.flag_stop:
            if 'sl_stop' in self.flag_stop:
                filename += f"sl_stop-{best_params.get('ohlcstx_sl_stop'):.2f}-"
            if 'ts_stop' in self.flag_stop:
                filename += f"ts_stop-{best_params.get('ohlcstx_sl_stop'):.2f}-"
            if 'tp_stop' in self.flag_stop:
                filename += f"tp_stop-{best_params.get('ohlcstx_tp_stop'):.2f}-"
        if self.flag_filter == 'vol':
            filename += f'''{self.flag_filter}-{best_params['vol_timeperiod']}-{best_params['vol_multiplier']}-{self.date_str}.pkl'''
        elif self.flag_filter == 'ang':
            filename += f'''{self.flag_filter}-{best_params['ang_timeperiod']}-{best_params['ang_threshold']}-{self.date_str}.pkl'''
        else:
            filename += f'''{self.date_str}.pkl'''
        portfolio = self.strategy.backtest(self.ohlcv, freq=self.freq, variables=variables, filters=filters)
        stats = portfolio.stats()
        if self.flag_acc_return:
            acc_returns = get_acc_returns(portfolio.daily_returns())
            stats = stats.append(pd.Series(acc_returns))
        save_stats(stats, self.output_path, filename)
        print(f'The stats are saved to {self.output_path}/{filename}')

    def generate_best_params(self):
        print(f'The search for {self.symbols} starts now')
        for symbol in self.symbols:
            print(f'Start the search for {symbol}')
            self.ohlcv = download_crypto_history(symbol, self.freq)
            best_params = self._get_grid_search()
            if best_params:
                print(f'Found the best params {best_params}')
                self.apply_best_params(best_params, symbol)
            else:
                print('Not found the best params')
        print('The search for all the symbols is completed')


class CheckBoIndicators(CheckIndicators):
    '''
    This class provides the method to check Partial Differentiation
    and Combinatorially Symmetric Cross-validation of BO strategy.
    symbols: a list of symbols to be optimzied on, e.g., ['BTCUSDT']
    date: the date the best params are created
    res_dir: the output directory
    flag_filter: currently supported fitlers: 'vol', 'ang', default: None
    flag_ts_stop: flag to turn on/off trailing stop
    strategy: currently supported values: 'bo'
    '''
    def __init__(self,
                 symbols: Union[str, list],
                 date: str,
                 res_dir: str,
                 flag_filter: str = None,
                 flag_stop: Union[str, list] = None,
                 strategy: str = 'bo'
                 ):
        super().__init__(symbols, date, res_dir, flag_filter, strategy)
        self.flag_stop = [flag_stop] if isinstance(flag_stop, str) else flag_stop
        self.check_indicators()

    def _get_strategy(self, strategy):
        return get_strategy(strategy)

    def _get_variables(self, **kwargs):
        if self.flag_stop:
            return create_bo_variables_with_stop(flag_stop=self.flag_stop, **kwargs)
        return create_bo_variables(**kwargs)

    def _get_filter(self, **kwargs):
        return get_filter(flag_filter=self.flag_filter, **kwargs)


class InspectBoStrategy(InspectStrategy):
    '''
    This class provides the method to optimize the BO strategy
    symbols: a list of symbols to be optimzied on, e.g., 'BTCUSDT'
    freq: currently supported values: '1h' or '4h'
    long_window, short_window: breakout params
    timeperiod, multiplier: volume filter params
    flag_filter: currently supported fitlers: 'vol', 'ang', default: None
    ts_stop: ts_stop params
    strategy: currently supports 'bo'
    '''
    def __init__(self, 
                 symbol: str,
                 freq: str,
                 long_window: int,
                 short_window: int,
                 timeperiod: int = None,
                 multiplier: int = None,
                 threshold: int = None,
                 flag_filter: str = None,
                 stop_vars: dict = None,
                 strategy: str = 'bo',
                 show_fig: bool = True
                 ):
        super().__init__(symbol, freq, flag_filter, strategy, show_fig)
        self.long_window = long_window
        self.short_window = short_window
        self.timeperiod = timeperiod
        self.multiplier = multiplier
        self.threshold = threshold
        self.stop_vars = stop_vars
        self.inspect()

    def _get_strategy(self, strategy):
        return get_strategy(strategy)

    def _get_variables(self, **kwargs):
        variables = create_bo_variables(
            long_window=self.long_window,
            short_window=self.short_window
        )
        if self.stop_vars:
            variables.update(self.stop_vars)
        return variables

    def _get_filter(self):
        return get_filter(
            self.flag_filter,
            timeperiod=self.timeperiod,
            multiplier=self.multiplier,
            threshold=self.threshold
            )


def returns_timeline(
    symbol: str,
    freq: str,
    long_window: int,
    short_window: int,
    timeperiod: int = None,
    multiplier: int = None,
    threshold: int = None,
    flag_filter: str = None,
    stop_vars: dict = None,
    strategy: str = 'bo',
):
    ins = InspectBoStrategy(
        symbol=symbol,
        freq=freq,
        long_window=long_window,
        short_window=short_window,
        timeperiod=timeperiod,
        multiplier=multiplier,
        threshold=threshold,
        flag_filter=flag_filter,
        stop_vars=stop_vars,
        strategy=strategy,
        show_fig=False
    )
    daily_returns = ins.portfolio.daily_returns()
    acc_returns = get_acc_returns(daily_returns)
    return acc_returns
