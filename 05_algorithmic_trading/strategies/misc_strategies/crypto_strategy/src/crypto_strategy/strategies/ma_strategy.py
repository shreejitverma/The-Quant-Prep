import numpy as np
import pandas as pd
from typing import Union
from finlab_crypto.indicators import trends
from crypto_strategy.data import (
    save_stats,
    get_acc_returns,
    download_crypto_history
)
from .base import (
    trend_strategy,
    mmi_filter, ang_filter,
    BestStrategy, InspectStrategy, CheckIndicators
) 


RANGE_WINDOW = np.arange(30, 300, 10)
RANGE_TIMEPERIOD = np.arange(10, 50, 5)
RANGE_THRESHOLD = np.arange(0, 25, 5)
RANGE_STOP = np.arange(0.1, 0.6, 0.05)


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


def get_filter(flag_filter, **kwargs):
    filters = dict()
    if flag_filter == 'mmi':
        filters = create_mmi_filter(**kwargs)
    if flag_filter == 'ang':
        filters = create_ang_filter(**kwargs)
    return filters


def create_ma_variables(**kwargs):
    if kwargs.get('name'):
        variables = dict(name=kwargs.get('name'))
    else:
        raise ValueError('The name of the MA strategy is required')
    # Load given params
    if kwargs.get('n1') and kwargs.get('n2'):
        variables.update(kwargs)
    # Set up params for backtests
    elif not (kwargs.get('n1') or kwargs.get('n2')):
        variables['n1'] = RANGE_WINDOW
        variables['n2'] = RANGE_WINDOW
    else:
        raise ValueError('The MA strategy does\'t have the config params provided')
    return variables


def create_ma_variables_with_stop(**kwargs):
    variables = create_ma_variables(**kwargs)
    if not (kwargs.get('n1') or kwargs.get('n2')):
        flag_stop = kwargs.get('flag_stop')
        if kwargs.get('flag_stop'):
            if not set(flag_stop).issubset(['ts_stop', 'sl_stop', 'tp_stop']):
                raise ValueError('The value of flag_stop is not supported')
            for fs in flag_stop:
                variables[fs] = RANGE_STOP
        else:
            raise ValueError('flag_stop is not set')
    return variables


class BestMaStrategy(BestStrategy):
    '''
    This class provides the method to optimize the MA strategy
    symbols: a single symbol or a list of symbols to be optimzied on, e.g., 'BTCUSDT'
    freq: currently supported values are '1h' or '4h'
    res_dir: the output directory
    flag_filter: flag to specify filters, currently support 'mmi', 'ang', default None
    flag_stop: flag to specify early stop, currently support 'ts_stop', 'sl_stop', 'tp_stop', default None
    trends: a list of MA strategies, default: trends.keys()
    strategy: strategy name, default: 'ma'
    '''
    def __init__(self,
                 symbols: Union[str, list],
                 freq: str,
                 res_dir: str,
                 flag_filter: str = None,
                 flag_stop: Union[str, list] = None,
                 flag_acc_return: bool = True,
                 trends: list = trends.keys(),
                 strategy: str = 'ma'
                 ):
        super().__init__(symbols, freq, res_dir, flag_filter, strategy)
        self.trends = trends
        self.flag_stop = [flag_stop] if isinstance(flag_stop, str) else flag_stop
        self.flag_acc_return = flag_acc_return
        self.generate_best_params()

    def _get_strategy(self, strategy):
        return trend_strategy

    def _get_filter(self, **kwargs):
        return get_filter(flag_filter=self.flag_filter, **kwargs)

    def _get_variables(self, **kwargs):
        if self.flag_stop:
            return create_ma_variables_with_stop(flag_stop=self.flag_stop, **kwargs)
        return create_ma_variables(**kwargs)

    def _get_grid_search(self):
        if self.flag_filter == 'mmi':
            return self.grid_search_mmi_params()
        if self.flag_filter == 'ang':
            return self.grid_search_ang_params()
        return self.grid_search_params()

    def get_best_params(self, total_best_params, n=10):
        total_best_params = pd.DataFrame(total_best_params)
        total_best_params['sharpe'] = (total_best_params['sharpe'] + 0.05).round(1)
        total_best_params['gap'] = total_best_params['n2'] - total_best_params['n1']
        # TODO: add tp_stop in sort_values
        if 'ohlcstx_sl_stop' in total_best_params.columns:
            total_best_params = (
                total_best_params
                .query('gap > 0')
                .sort_values(
                    by=['sharpe', 'gap', 'n1', 'ohlcstx_sl_stop'],
                    ascending=[True, True, False, False])
            )
        else:
            total_best_params = (
                total_best_params
                .query('gap > 0')
                .sort_values(
                    by=['sharpe', 'gap', 'n1'],
                    ascending=[True, True, False]
                    )
            )
        print(total_best_params)
        return total_best_params.tail(1).to_dict(orient='records')[0] if not total_best_params.empty else None

    def grid_search_params(self):
        variables = self._get_variables(name=self.trends)
        best_params = self.backtest(variables)
        return self.get_best_params(best_params)

    def grid_search_mmi_params(self):
        variables = self._get_variables(name=self.trends)
        total_best_params = list()
        for timeperiod in RANGE_TIMEPERIOD:
            filters = self._get_filter(timeperiod=timeperiod)
            best_params = self.backtest(variables, filters)
            total_best_params.extend(best_params)
        return self.get_best_params(total_best_params)

    def grid_search_ang_params(self):
        variables = self._get_variables(name=self.trends)
        total_best_params = list()
        for threshold in RANGE_THRESHOLD:
            for timeperiod in RANGE_TIMEPERIOD:
                filters = self._get_filter(timeperiod=timeperiod, threshold=threshold)
                best_params = self.backtest(variables, filters)
                total_best_params.extend(best_params)
        return self.get_best_params(total_best_params)

    def apply_best_params(self, best_params, symbol):
        variables = self._get_variables(
            name=best_params['name'],
            n1=best_params['n1'],
            n2=best_params['n2']
        )
        if 'ts_stop' in self.flag_stop:
            variables.update(ts_stop=best_params.get('ohlcstx_sl_stop'))
        if 'sl_stop' in self.flag_stop:
            variables.update(sl_stop=best_params.get('ohlcstx_sl_stop'))
        if 'tp_stop' in self.flag_stop:
            variables.update(tp_stop=best_params.get('ohlcstx_tp_stop'))
        filters = self._get_filter(
            timeperiod=best_params.get('mmi_timeperiod') or best_params.get('ang_timeperiod'),
            threshold=best_params.get('ang_threshold')
            )
        filename = f"{symbol}-{self.freq}-{best_params['name']}-{best_params['n1']}-{best_params['n2']}-"
        if self.flag_stop:
            if 'sl_stop' in self.flag_stop:
                filename += f"sl_stop-{best_params.get('ohlcstx_sl_stop'):.2f}-"
            if 'ts_stop' in self.flag_stop:
                filename += f"ts_stop-{best_params.get('ohlcstx_sl_stop'):.2f}-"
            if 'tp_stop' in self.flag_stop:
                filename += f"tp_stop-{best_params.get('ohlcstx_tp_stop'):.2f}-"
        if self.flag_filter == 'mmi':
            filename += f"{self.flag_filter}-{best_params['mmi_timeperiod']}-{self.date_str}.pkl"
        elif self.flag_filter == 'ang':
            filename += f"{self.flag_filter}-{best_params['ang_timeperiod']}-{best_params['ang_threshold']}-{self.date_str}.pkl"
        else:
            filename += f"{self.date_str}.pkl"
        portfolio = self.strategy.backtest(self.ohlcv, variables=variables, filters=filters, freq=self.freq)
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
            print(f'Found the best params {best_params}')
            self.apply_best_params(best_params, symbol)
        print('The search for all the symbols is completed')


class CheckMaIndicators(CheckIndicators):
    '''
    This class provides the method to check Partial Differentiation
    and Combinatorially Symmetric Cross-validation of MA strategy.
    symbols: a list of symbols to be optimzied on, e.g., ['BTCUSDT']
    date: the date the best params are created
    res_dir: the output directory
    flag_filter: currently supported fitlers: 'mmi', 'ang', default: None
    flag_stop: flag to specify early stop, currently support 'ts_stop', 'sl_stop', 'tp_stop', default None
    '''
    def __init__(self,
                 symbols: Union[str, list],
                 date: str,
                 res_dir: str,
                 flag_filter: str = None,
                 flag_stop: Union[str, list] = None,
                 strategy: str = 'ma'
                 ):
        super().__init__(symbols, date, res_dir, flag_filter, strategy)
        self.flag_stop = [flag_stop] if isinstance(flag_stop, str) else flag_stop
        self.check_indicators()

    def _get_strategy(self, strategy):
        return trend_strategy

    def _get_variables(self, **kwargs):
        if self.flag_stop:
            return create_ma_variables_with_stop(flag_stop=self.flag_stop, **kwargs)
        return create_ma_variables(**kwargs)

    def _get_filter(self, **kwargs):
        return get_filter(flag_filter=self.flag_filter, **kwargs)


# TODO: dictionary for filters
class InspectMaStrategy(InspectStrategy):
    '''
    This class provides a method to inspect the MA strategy with given params
    symbol: the name of the crypto, e.g., 'BTCUSDT'
    freq: currently supported values are '1h' or '4h'
    name, n1, n2: the name and the params of the ma strategy, e.g., 'sma', 100, 50
    timeperiod: param used in either mmi or ang filter
    threshold: param used in ang filter
    flag_filter: currently supported fitlers: 'mmi', 'ang', default: None
    stop_vars: dictionary of stop vars, currently support 'ts_stop', 'sl_stop', 'tp_stop', default None
    '''
    def __init__(self,
                 symbol: str,
                 freq: str,
                 name: str,
                 n1: int,
                 n2: int,
                 flag_filter: str = None,
                 timeperiod: int = None,
                 threshold: int = None,
                 stop_vars: dict = None,
                 strategy: str = 'ma',
                 show_fig: bool = True
                 ):
        super().__init__(symbol, freq, flag_filter, strategy, show_fig)
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.timeperiod = timeperiod
        self.threshold = threshold
        self.flag_filter = flag_filter
        self.stop_vars = stop_vars
        self.inspect()

    def _get_strategy(self, strategy):
        return trend_strategy

    def _get_variables(self):
        variables = create_ma_variables(name=self.name, n1=self.n1, n2=self.n2)
        if self.stop_vars:
            variables.update(self.stop_vars)
        return variables

    def _get_filter(self):
        return get_filter(
            self.flag_filter,
            timeperiod=self.timeperiod,
            threshold=self.threshold
            )


def returns_timeline(
    symbol: str,
    freq: str,
    name: str,
    n1: int,
    n2: int,
    flag_filter: str = None,
    timeperiod: int = None,
    threshold: int = None,
    stop_vars: dict = None,
    strategy: str = 'ma'
):
    ins = InspectMaStrategy(
        symbol=symbol,
        freq=freq,
        n1=n1,
        n2=n2,
        timeperiod=timeperiod,
        threshold=threshold,
        flag_filter=flag_filter,
        stop_vars = stop_vars,
        strategy=strategy,
        show_fig=False
    )
    daily_returns = ins.portfolio.daily_returns()
    acc_returns = get_acc_returns(daily_returns) 
    return acc_returns