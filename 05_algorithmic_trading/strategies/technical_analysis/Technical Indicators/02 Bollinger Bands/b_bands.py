import pandas as pd

def bbands(series, period = 14, deviation = 2):

    moving_average = series['close'].rolling(period).mean()
    moving_std = series['close'].rolling(period).std()

    upper_band = moving_average + (deviation * moving_std)
    lower_band = moving_average - (deviation * moving_std)

    return upper_band, moving_average, lower_band
    