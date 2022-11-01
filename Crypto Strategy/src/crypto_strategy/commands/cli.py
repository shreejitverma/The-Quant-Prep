import click
from crypto_strategy.strategies.ma_strategy import BestMaStrategy, CheckMaIndicators
from crypto_strategy.strategies.bo_strategy import BestBoStrategy, CheckBoIndicators
from crypto_strategy.reporting.report import generate_report as _generate_report


SYMBOLS = [
    'BTC', 'ETH', 'BNB', 'SOL', 'ADA',
    'XRP', 'DOT', 'DOGE', 'AVAX', 'LUNA',
    'LTC', 'UNI', 'LINK', 'ALGO',
    'VET', 'MATIC',
    # # under review
    # 'XTZ', 'BCH', 'EGLD', 'XLM', 'AXS',
]
BASES = ['USDT']
SYMBOLS = [s + b for s in SYMBOLS for b in BASES]


@click.group()
def cli():
    pass


@cli.command()
@click.option('--symbol', '-s', type=str, default=None, help="asset name, e.g., BTCUSDT")
@click.option('--freq', '-f', required=True, type=click.Choice(['4h', '1h']), help="frquency to use")
@click.option('--res_dir', '-r', required=True, type=str, help="directory for outputs")
@click.option('--flag_filter', '-g', type=str, default=None, show_default=True, help='flag to use, mmi | ang')
@click.option('--flag_stop', '-t', type=str, default=None, show_default=True, help='early stop flag, ts_stop | sl_stop | tp_stop')
def best_ma_strategy(symbol, freq, res_dir, flag_filter, flag_stop):
    parts = res_dir.split('-')
    if freq not in parts:
        raise ValueError('Mismatch found in freq setting and output dir')
    if (flag_filter and flag_filter not in parts) or (not flag_filter and 'filter' in parts):
        raise ValueError('Mismatch found in filter setting and output dir')
    if flag_stop and 'stop' not in res_dir:
        raise ValueError('Mismatch found in flag_stop setting and output dir')
    symbols = symbol if symbol else SYMBOLS
    BestMaStrategy(symbols, freq, res_dir, flag_filter, flag_stop)


@cli.command()
@click.option('--symbol', '-s', type=str, default=None, help='asset name, e.g., BTCUSDT')
@click.option('--date', '-d', type=str, help='the date when the results are generated')
@click.option('--res_dir', '-r', required=True, type=str, help='directory for outputs')
@click.option('--flag_filter', '-g', type=str, default=None, show_default=True, help='flag to use, mmi | ang')
@click.option('--flag_stop', '-t', type=str, default=None, show_default=True, help='early stop flag, ts_stop | sl_stop | tp_stop')
def check_ma_indicators(symbol, date, res_dir, flag_filter, flag_stop):
    parts = res_dir.split('-')
    if (flag_filter and flag_filter not in parts) or (not flag_filter and 'filter' in parts):
        raise ValueError('Mismatch found in filter setting and output dir')
    if 'ma' not in parts:
        raise ValueError('Make sure the res_dir is for MA strategy')
    if flag_stop and 'stop' not in res_dir:
        raise ValueError('Mismatch found in flag_stop setting and output dir')
    symbols = symbol if symbol else SYMBOLS
    CheckMaIndicators(symbols, date, res_dir, flag_filter, flag_stop)


@cli.command()
@click.option('--symbol', '-s', type=str, default=None, show_default=True, help="asset name, e.g., BTCUSDT")
@click.option('--freq', '-f', required=True, type=click.Choice(['4h', '1h']), help="frquency to use")
@click.option('--res_dir', '-r', required=True, type=str, help="directory for outputs")
@click.option('--flag_filter', '-g', type=str, default=None, show_default=True, help='filter to use, vol | ang')
@click.option('--flag_stop', '-t', type=str, default=None, show_default=True, help='early stop flag, ts_stop | sl_stop | tp_stop')
def best_bo_strategy(symbol, freq, res_dir, flag_filter, flag_stop):
    parts = res_dir.split('-')
    if freq not in parts:
        raise ValueError('Mismatch found in freq setting and output dir')
    if (flag_filter and flag_filter not in parts) or (not flag_filter and 'filter' in parts):
        raise ValueError('Mismatch found in filter setting and output dir')
    if 'bo' not in parts:
        raise ValueError('Mismatch found in strategy bo and output dir')
    if flag_stop and 'ts_stop' not in parts:
        raise ValueError('Mismatch found in ts_stop setting and output dir')
    symbols = symbol if symbol else SYMBOLS
    BestBoStrategy(symbols, freq, res_dir, flag_filter, flag_stop)


@cli.command()
@click.option('--symbol', '-s', type=str, default=None, help="asset name, e.g., BTCUSDT")
@click.option('--date', '-d', type=str, help='the date when the results are generated')
@click.option('--res_dir', '-r', required=True, type=str, help="directory for outputs")
@click.option('--flag_filter', '-g', type=str, default=None, show_default=True, help='filter to use, vol | ang')
@click.option('--flag_stop', '-t', type=str, default=None, show_default=True, help='early stop flag, ts_stop | sl_stop | tp_stop')
def check_bo_indicators(symbol, date, res_dir, flag_filter, flag_stop):
    parts = res_dir.split('-')
    if (flag_filter and flag_filter not in parts) or (not flag_filter and 'filter' in parts):
        raise ValueError('Mismatch found in filter setting and output dir')
    if 'bo' not in parts:
        raise ValueError('Mismatch found in strategy bo and output dir')
    if flag_stop and 'ts_stop' not in parts:
        raise ValueError('Mismatch found in ts_stop setting and output dir')
    symbols = symbol if symbol else SYMBOLS
    CheckBoIndicators(symbols, date, res_dir, flag_filter, flag_stop)


@cli.command()
@click.option('--symbol', '-s', type=str, default=None, help="asset name, e.g., BTCUSDT")
def generate_report(symbol):
    if symbol:
        _generate_report(symbol)
    else:
        for symb in SYMBOLS:
            _generate_report(symb)


if __name__ == '__main__':
    cli()
