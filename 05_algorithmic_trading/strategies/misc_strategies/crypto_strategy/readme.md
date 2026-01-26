# crypto-strategy
A repository to perform backtests and create trading strategies for cryptocurrencies.

[![Dependency Review](https://github.com/minggnim/crypto-strategy/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/minggnim/crypto-strategy/actions/workflows/dependency-review.yml)
[![Python package](https://github.com/minggnim/crypto-strategy/actions/workflows/python-package.yml/badge.svg)](https://github.com/minggnim/crypto-strategy/actions/workflows/python-package.yml)
[![pypi-upload](https://github.com/minggnim/crypto-strategy/actions/workflows/python-publish.yml/badge.svg)](https://github.com/minggnim/crypto-strategy/actions/workflows/python-publish.yml)

![](./img/algo-trading.png)


## Install
```
pip install crypto-strategy[full]
```

## Usage
### Backtest Strategy 

1. Moving Average Strategy

- Description
    ```
    BestMaStrategy(symbols, freq, res_dir, flag_filter, flag_stop)
    ```
    - symbols: asset name, e.g., BTCUSDT
    - freq: data frequency to use, 1h | 4h
    - res_dir: results directory
    - flag_filter: filter to use, [mmi | ang]
        - mmi: Market Meanness Index filter
        - ang: Linear Regression Angle filter
    - flag_stop: early stop flag, [ts_stop | sl_stop | tp_stop]
        - ts_stop: trailing stop
        - sl_stop: stop loss
        - tp_stop: take profit

- Example: Find the best params using 1h data with mmi filter and ts_stop
    ```
    BestMaStrategy(
        symbols=['BTCUSDT', 'ETHUSDT'], 
        freq='1h', 
        res_dir='results/best-1h-ma-mmi-filter', 
        flag_filters='mmi',
        flag_stop='ts_stop'
    )
    ```


2. Breakout Strategy
    - Description: A method to optimize the BO strategy
        - symbols: a list of symbols to be optimzied on, e.g., 'BTCUSDT'
        - freq: currently supported values: '1h' or '4h'
        - res_dir: the output directory
        - flag_filter: currently supported filters: 'vol', 'ang', default: None
        - flag_stop: early stop flag, [ts_stop | sl_stop | tp_stop]
            - ts_stop: trailing stop
            - sl_stop: stop loss
            - tp_stop: take profit


    - Example: Find the best params for bo strategy with vol filter using BTCUSDT 4h data and sl_stop
        ```
        BestBoStrategy(
            symbols = 'BTCUSDT',
            freq = '4h', 
            res_dir = 'results/best-4h-bo_rev-vol-filter', 
            flag_filters = 'vol',
            flag_stop = 'sl_stop',
        )


3. MACD Strategy
```
BestMacdStrategy(symbols, freq, res_dir, flag_filter)
```
- symbols: asset name, e.g., BTCUSDT
- freq: data frequency to use, 1h | 4h
- res_dir: results directory
- flag_filter: filter to use, [mmi | ang | stoch | sma]
    - vol: Volume filter
    - ang: Linear Regression Angle filter


### Inspect Strategy

1. MA Strategy

    - Description: A method to inspect the MA strategy with given params
        ```
        InspectMaStrategy(symbols, freq, name, n1, n2, timeperiod, threshold, flag_filter, stop_vars)
        ```
        - symbol: the name of the crypto, e.g., 'BTCUSDT'
        - freq: currently supported values are '1h' or '4h'
        - name, n1, n2: the name and the params of the ma strategy, e.g., 'sma', 100, 50
        - timeperiod: param used in either mmi or ang filter
        - threshold: param used in ang filter
        - flag_filter: currently supported fitlers: 'mmi', 'ang', default: None
        - stop_vars: dictionary of stop vars, currently support 'ts_stop', 'sl_stop', 'tp_stop', default None
    - Example: Inspect MA strategy `linear_reg` with `n1=30 & n2=280` and `sl_stop=0.1 & tp_stop=0.1`
        ```
        InspectMaStrategy(
            symbols, 
            freq='4h', 
            name='linear_reg', n1=30, n2=280, 
            stop_vars={'sl_stop':0.1, 'tp_stop':0.1})
        ```

2. BO Strategy

    - Description: A method to inspect the BO strategy
        ```
        InspectBoStrategy(symbol, freq, long_window, short_window, ts_stop, timeperiod, multiplier, threshold, flag_filter, flag_ts_stop)
        ```
        - symbols: a list of symbols to be optimzied on, e.g., 'BTCUSDT'
        - freq: currently supported values: '1h' or '4h'
        - long_window, short_window: breakout params
        - flag_filter: currently supported fitlers: 'vol', 'ang', default: None
        - timeperiod, multiplier: volume filter params
        - timeperiod, threshold: angle filter params
        - stop_vars: dictionary of stop vars, currently support 'ts_stop', 'sl_stop', 'tp_stop', default None

    - Example: Inspect 4h BTCUSDT breakout strategy with volume filter and trailing stop
        ```
        InspectBoStrategy(
            'BTCUSDT', 
            freq='4h', 
            long_window=100, short_window=50,
            flag_filter='vol', timeperiod=20, multiplier=2,
            stop_vars={'ts_stop':0.1})
        ```


## CLI

Backtests can also be carried out in command line. To find out more

```
crypto --help
```

Example 1: Find the best params for BO strategy with vol filter using 4h data
```
crypto best-bo-strategy -f 4h -r results/best-4h-bo-vol-filter -g vol -e bo
```

Example 2: Find the best params for MA strategy with mmi filter and ts_stop using 1h data
```
crypto best-ma-strategy -f 1h -r results/best-1h-ma-mmi-filter -g mmi -t ts_stop
```

## Tests
pytest
