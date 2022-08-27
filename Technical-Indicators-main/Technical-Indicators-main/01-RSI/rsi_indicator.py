import pandas

def rsi(df, periods):
    # taking the difference of the series
    close_delta = df['close'].diff()
    # filtering the positive and the negative value
    up = close_delta.clip(lower=0)
    down = abs(close_delta.clip(upper=0))
    # calculating the exponential moving average (can also go for the simple moving average or wilder's moving average)
    ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100/(1 + rs))
    return rsi