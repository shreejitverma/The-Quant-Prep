import pandas as pd

def doncian_channel(series, period =14):
    """
    Given a dataframe of OHLC data, return the doncian channel
    """

    upper_channel = series['high'].rolling(period).max()
    lower_channel = series['high'].rolling(period).min()

    mid_channel = (upper_channel +  lower_channel)/2

    return upper_channel, mid_channel, lower_channel
    