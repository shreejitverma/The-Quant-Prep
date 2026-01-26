"""
Title: Simple Moving Average Strategy
Description: This is a simple 20MA and 50MA strategy that buys/sells on crossover
Dataset: NSE Minute
"""

# Zipline
from zipline.api import(
    symbol,
    date_rules,
    time_rules,
    schedule_function,
    order_target_percent,
    get_datetime
)


def initialize(context):
    """
    A function to define things to do at the start of the strategy
    """

    # Universe selection
    context.stock = [
        symbol('DIVISLAB'),
        symbol('INFY')
    ]

    context.length_small_sma = 20
    context.length_long_sma = 50

    for i in range(1, 375, 15):
        schedule_function(
            run_strategy,
            date_rules.every_day(),
            time_rules.market_open(minutes=i)
        )


def run_strategy(context, data):

    # Get the data for the previous 900 minutes
    stock_data = data.history(context.stock, ["close"], 900, "1m")
    for stock in context.stock:
        # aggregate 15 minutes, all OHLCV columns
        stock_data["close"][stock] = (stock_data["close"][stock]).resample("15T", label="right", closed="right").last()

    stock_data["close"].dropna(inplace=True)

    # Calculate the SMAs
    for stock in context.stock:
        # Get the last 20 close prices
        last_20_prices = stock_data["close"][stock].iloc[-context.length_small_sma:]

        # Calculate the 20 SMA
        sma_20 = last_20_prices.mean()

        # Get the last 50 close prices
        last_50_prices = stock_data["close"][stock].iloc[-context.length_long_sma:]

        # Calculate the 50 SMA
        sma_50 = last_50_prices.mean()

        # Placing orders
        # Long Entry
        if ((sma_20 > sma_50) & (context.portfolio.positions[stock].amount == 0)):
            print("{} Going long on {}".format(get_datetime(), stock))
            order_target_percent(stock, 0.5)

        # Exiting Long entry
        elif ((sma_20 < sma_50) & (context.portfolio.positions[stock].amount != 0)):
            print("{} Exiting {}".format(get_datetime(), stock))
            order_target_percent(stock, 0)

