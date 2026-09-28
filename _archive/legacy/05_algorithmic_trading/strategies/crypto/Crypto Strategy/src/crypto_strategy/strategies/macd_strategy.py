import numpy as np
import pandas as pd
from crypto_strategy.data import download_crypto_history, save_stats
from .base import (
    macd_strategy, macd_strategy_revised,
    mmi_filter, ang_filter, stoch_filter, sma_filter,
    BestStrategy, InspectStrategy, CheckIndicators
)

RANGE_FASTPERIOD = np.arange(10, 200, 10)
RANGE_SLOWPERIOD = np.arange(10, 350, 10)
RANGE_SIGNALPERIOD = np.arange(10, 350, 10)
RANGE_TIMEPERIOD = np.arange(10, 50, 5)
RANGE_THRESHOLD = np.arange(0, 25, 5)
RANGE_FAST = np.arange(5, 15, 5)
RANGE_SLOW = np.arange(3, 15, 3)


def get_strategy(strategy):
    if strategy == 'macd':
        return macd_strategy
    if strategy == 'macd_rev':
        return macd_strategy_revised
    raise ValueError('Strategy not recognized. Please choose from macd and macd_rev')


def create_mmi_filter(**kwargs):
    if kwargs:
        assert kwargs.get('timeperiod'),\
            'mmi fitler doesn\'t have config params provided'
        filter_config = kwargs
    else:
        filter_config = dict(
            timeperiod=RANGE_TIMEPERIOD,
        )
    filters = {
        'mmi': mmi_filter.create({
            'timeperiod': filter_config['timeperiod']
        })
    }
    return filters


def create_ang_filter(**kwargs):
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


def create_stoch_filter(**kwargs):
    if kwargs:
        assert kwargs.get('fast') and kwargs.get('slow') is not None,\
            'Stoch filter doesn\'t have config params provided'
        filter_config = dict(
            fast=kwargs['fast'],
            slow=kwargs['slow']
        )
    else:
        filter_config = dict(
            fast=RANGE_FAST,
            slow=RANGE_SLOW
        )
    filters = {
        'stoch': stoch_filter.create({
            'fast': filter_config['fast'],
            'slow': filter_config['slow']
        })
    }
    return filters


def create_sma_filter(**kwargs):
    if kwargs:
        assert kwargs.get('timeperiod') is not None,\
            'SMA filter doesn\'t have config params provided'
        filter_config = dict(
            timeperiod=kwargs['timeperiod']
        )
    else:
        filter_config = dict(
            timeperiod=RANGE_TIMEPERIOD
        )
    filters = {
        'sma': sma_filter.create({
            'timeperiod': filter_config['timeperiod']
        })
    }
    return filters


def get_filter(flag_filter, **kwargs):
    filters = dict()
    if flag_filter == 'mmi':
        filters = create_mmi_filter(**kwargs)
    if flag_filter == 'ang':
        filters = create_ang_filter(**kwargs)
    if flag_filter == 'stoch':
        filters = create_stoch_filter(**kwargs)
    if flag_filter == 'sma':
        filters = create_sma_filter(**kwargs)
    return filters


def create_variables(**kwargs):
    variables = dict()
    if kwargs.get('fastperiod') and kwargs.get('slowperiod') and kwargs.get('signalperiod'):
        variables.update(kwargs)
    else:
        variables['fastperiod'] = RANGE_FASTPERIOD
        variables['slowperiod'] = RANGE_SLOWPERIOD
        variables['signalperiod'] = RANGE_SIGNALPERIOD
    return variables


class BestMacdStrategy(BestStrategy):
    '''
    This class provides the method to optimize the MA strategy
    symbols: a list of symbols to be optimzied on, e.g., ['BTCUSDT']
    freq: currently supported values are '1h' or '4h'
    res_dir: the output directory
    flag_fitler: currently supported fitlers: 'mmi', 'ang', 'stoch', 'sma', default: None
    trends: a list of MA strategies, default: trends.keys()
    strategy: currently supported strategies: 'macd', 'macd_rev', default: 'macd'
    '''
    def __init__(self, symbols: list, freq: str, res_dir: str,
                 flag_filter: str = None,
                 strategy: str = 'macd'
                 ):
        super().__init__(symbols, freq, res_dir, flag_filter, strategy)
        self.generate_best_params()

    def _get_strategy(self, strategy):
        return get_strategy(strategy)

    def _get_filter(self, **kwargs):
        return get_filter(flag_filter=self.flag_filter, **kwargs)

    def _get_variables(self, **kwargs):
        return create_variables(**kwargs)

    def get_best_params(self, total_best_params, n=10):
        total_best_params = (
            pd.DataFrame(total_best_params)
            .sort_values(by=['sharpe', 'slowperiod'], ascending=[True, True])
            .tail(n)
        )
        print(total_best_params)
        return total_best_params.tail(1).to_dict(orient='records')[0]

    def _get_grid_search(self):
        if self.flag_filter == 'mmi':
            return self.grid_search_mmi_params()
        if self.flag_filter == 'ang':
            return self.grid_search_ang_params()
        if self.flag_filter == 'stoch':
            return self.grid_search_stoch_params()
        if self.flag_filter == 'sma':
            return self.grid_search_sma_params()
        return self.grid_search_params()

    def grid_search_params(self):
        variables = self._get_variables()
        best_params = self.backtest(variables)
        return self.get_best_params(best_params)

    def grid_search_mmi_params(self):
        variables = self._get_variables()
        total_best_params = list()
        for timeperiod in RANGE_TIMEPERIOD:
            filters = self._get_filter(timeperiod=timeperiod)
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

    def grid_search_stoch_params(self):
        variables = self._get_variables()
        total_best_params = list()
        for fast in RANGE_FAST:
            for slow in RANGE_SLOW:
                filters = self._get_filter(fast=fast, slow=slow)
                best_params = self.backtest(variables, filters)
                total_best_params.extend(best_params)
        return self.get_best_params(total_best_params)

    def grid_search_sma_params(self):
        variables = self._get_variables()
        total_best_params = list()
        for timeperiod in RANGE_TIMEPERIOD:
            filters = self._get_filter(timeperiod=timeperiod)
            best_params = self.backtest(variables, filters)
            total_best_params.extend(best_params)
        return self.get_best_params(total_best_params)

    def apply_best_params(self, best_params, symbol):
        variables = self._get_variables(
            fastperiod=best_params['fastperiod'],
            slowperiod=best_params['slowperiod'],
            signalperiod=best_params['signalperiod']
            )
        filters = self._get_filter(
            timeperiod=best_params.get('mmi_timeperiod')
            or best_params.get('ang_timeperiod')
            or best_params.get('sma_timeperiod'),
            threshold=best_params.get('ang_threshold'),
            fast=best_params.get('stoch_fast'),
            slow=best_params.get('stoch_slow')
            )
        portfolio = self.strategy.backtest(self.ohlcv, variables=variables, filters=filters, freq=self.freq)
        filename = f"{symbol}-{self.freq}-{best_params['fastperiod']}-{best_params['slowperiod']}-{best_params['signalperiod']}-"
        if self.flag_filter == 'mmi':
            filename += f"{self.flag_filter}-{best_params['mmi_timeperiod']}-{self.date_str}.pkl"
        elif self.flag_filter == 'ang':
            filename += f"{self.flag_filter}-{best_params['ang_timeperiod']}-{best_params['ang_threshold']}-{self.date_str}.pkl"
        elif self.flag_filter == 'stoch':
            filename += f"{self.flag_filter}-{best_params['stoch_fast']}-{best_params['stoch_slow']}-{self.date_str}.pkl"
        elif self.flag_filter == 'sma':
            filename += f"{self.flag_filter}-{best_params['sma_timeperiod']}-{self.date_str}.pkl"
        else:
            filename += f"{self.date_str}.pkl"
        save_stats(portfolio.stats(), self.output_path, filename)
        print(f'The stats are saved to {self.output_path}/{filename}')

    def generate_best_params(self):
        print(f'The search for {self.symbols} starts now')
        for symbol in self.symbols:
            print(f'Start the search for {symbol}')
            self.ohlcv = download_crypto_history(symbol, self.freq)
            best_params = self._get_grid_search()
            print(f'Found the best params {best_params}')
            self.apply_best_params(best_params, symbol)
        print('The search for all the symbols is completed')


class CheckMacdIndicators(CheckIndicators):
    '''
    This class provides the method to check Partial Differentiation
    and Combinatorially Symmetric Cross-validation of MACD strategy
    symbols: a list of symbols to be optimzied on, e.g., ['BTCUSDT']
    date: the date the best params are created
    res_dir: the output directory
    flag_fitler: currently supported fitlers: 'mmi', 'ang', 'stoch', 'sma', default: None
    strategy: MACD strategy
    '''
    def __init__(self, symbols: list, date: str, res_dir: str,
                 flag_filter: str = None, strategy: str = 'macd'
                 ):
        super().__init__(symbols, date, res_dir, flag_filter, strategy)
        self.check_indicators()

    def _get_strategy(self, strategy):
        return get_strategy(strategy)

    def _get_variables(self, **kwargs):
        return create_variables(**kwargs)

    def _get_filter(self, **kwargs):
        return get_filter(flag_filter=self.flag_filter, **kwargs)


class InspectMacdStrategy(InspectStrategy):
    '''
    This class provides a method to inspect the MA strategy with given params
    symbol: the name of the crypto, e.g., 'BTCUSDT'
    freq: currently supported values are '1h' or '4h'
    fastperiod, slowperiod, signalperiod: params of macd strategy
    timeperiod, threshold, fast, slow: params used in filters
    flag_fitler: currently supported fitlers: 'mmi', 'ang', 'stoch', 'sma', default: None
    '''
    def __init__(self,
                 symbol: str, freq: str,
                 fastperiod: int, slowperiod: int, signalperiod: int,
                 timeperiod: int = None, threshold: int = None,
                 fast: int = None, slow: int = None,
                 flag_filter: str = None,
                 strategy: str = 'macd',
                 show_fig: bool = True
                 ):
        super().__init__(symbol, freq, flag_filter, strategy, show_fig)
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod
        self.timeperiod = timeperiod
        self.threshold = threshold
        self.fast = fast
        self.slow = slow
        self.flag_filter = flag_filter
        self.inspect()

    def _get_strategy(self, strategy):
        return get_strategy(strategy)

    def _get_variables(self):
        return create_variables(
            fastperiod=self.fastperiod,
            slowperiod=self.slowperiod,
            signalperiod=self.signalperiod
            )

    def _get_filter(self):
        return get_filter(
            self.flag_filter,
            timeperiod=self.timeperiod,
            threshold=self.threshold,
            fast=self.fast,
            slow=self.slow
            )
