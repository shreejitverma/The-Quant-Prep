from crypto_strategy.strategies.bo_strategy import InspectBoStrategy
from crypto_strategy.strategies.ma_strategy import InspectMaStrategy


def calc_kelly_criterion(stats):
    # winning probability
    p = stats['Win Rate [%]'] / 100
    # the odds defining the amount won for unit bet
    b = abs(stats['Avg Winning Trade [%]'] / stats['Avg Losing Trade [%]'])
    # optimal share of capital to bet (b * p + p - 1) / b
    kc = p + (p - 1) / b
    return kc


def tm_bo_stats(symbol, tm):
    parts = tm.split('-')
    freq = parts[1]
    strategy = parts[2]
    long_window = int(parts[3])
    short_window = int(parts[4])
    flag_filter = timeperiod = multiplier = threshold = stop_vars = None
    if 'vol' in parts:
        flag_filter = parts[-4]
        timeperiod = int(parts[-3])
        multiplier = int(parts[-2])
    if 'ang' in parts:
        flag_filter = parts[-4]
        timeperiod = int(parts[-3])
        threshold = int(parts[-2])
    if 'ts' in parts:
        stop_vars = {'ts_stop': float(parts[6])}
    if 'sl' in parts:
        stop_vars = {'sl_stop': float(parts[6])}
    if 'tp' in parts:
        stop_vars = {'tp_stop': float(parts[6])}
    ins = InspectBoStrategy(
        symbol,
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
    return ins.portfolio


def tm_ma_stats(symbol, tm):
    parts = tm.split('-')
    freq = parts[1]
    name = parts[2]
    n1 = int(parts[3])
    n2 = int(parts[4])
    flag_filter = timeperiod = stop_vars = None
    if 'mmi' in parts or 'mmi_ge' in parts:
        flag_filter = parts[-3]
        timeperiod = int(parts[-2])
    if 'ts' in parts:
        stop_vars = {'ts_stop': float(parts[6])}
    if 'sl' in parts:
        stop_vars = {'sl_stop': float(parts[6])}
    if 'tp' in parts:
        stop_vars = {'tp_stop': float(parts[6])}
    ins = InspectMaStrategy(
        symbol,
        freq=freq,
        name=name,
        n1=n1,
        n2=n2,
        flag_filter=flag_filter,
        timeperiod=timeperiod,
        stop_vars=stop_vars,
        show_fig=False
    )
    return ins.portfolio


def portfolio_stats(tm_list):
    tp_stats = dict()
    for tm in tm_list:
        key = tm.name
        symbol = tm.symbols[0]
        tp_stats[key] = dict()
        stats = None
        if 'bo' in tm.name:
            stats = tm_bo_stats(symbol, tm.name)
        else:
            stats = tm_ma_stats(symbol, tm.name)
        if stats is not None:
            stats = stats.stats()
            tp_stats[key] = stats
    return tp_stats


def portfolio_kelly_criterion(tm_list):
    tp_kc = dict()
    for tm in tm_list:
        key = tm.name
        symbol = tm.symbols[0]
        tp_kc[key] = dict()
        stats = None
        if 'bo' in tm.name:
            stats = tm_bo_stats(symbol, tm.name)
        else:
            stats = tm_ma_stats(symbol, tm.name)
        if stats is not None:
            stats = stats.stats()
            tp_kc[key]['trades'] = stats['Total Trades']
            tm_kc = calc_kelly_criterion(stats)
            tp_kc[key]['kc'] = tm_kc
        else:
            raise ValueError(f'stats not found for {key}')
    return tp_kc


def multi_assets_allocation(tm_list):
    tp_kc = dict()
    for tm in tm_list:
        key = tm.name
        symbol = tm.symbols[0]
        tp_kc[key] = dict()
        stats = None
        if 'bo' in tm.name:
            stats = tm_bo_stats(symbol, key)
        else:
            stats = tm_ma_stats(symbol, key)
        if stats is not None:
            stats = stats.annual_returns()
            stats.index = stats.index.year
            tp_kc[key] = stats
        else:
            raise ValueError(f'stats not found for {key}')
    return tp_kc


def portfolio_monthly_ret(tm_list):
    tp_monthly_ret = dict()
    for tm in tm_list:
        key = tm.name
        symbol = tm.symbols[0]
        tp_monthly_ret[key] = dict()
        stats = None
        if 'bo' in tm.name:
            stats = tm_bo_stats(symbol, tm.name)
        else:
            stats = tm_ma_stats(symbol, tm.name)
        if stats is not None:
            tp_monthly_ret[key] = stats.get_qs().monthly_returns()
    return tp_monthly_ret


def portfolio_daily_ret(tm_list):
    tp_daily_ret = dict()
    for tm in tm_list:
        key = tm.name
        symbol = tm.symbols[0]
        tp_daily_ret[key] = dict()
        stats = None
        if 'bo' in tm.name:
            stats = tm_bo_stats(symbol, tm.name)
        else:
            stats = tm_ma_stats(symbol, tm.name)
        if stats is not None:
            tp_daily_ret[key] = stats.daily_returns()
    return tp_daily_ret
