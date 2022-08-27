import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from mpl_finance import candlestick_ohlc
import pandas_datareader.data as web
from matplotlib.dates import date2num

ashley = web.DataReader('ASHOKLEY.NS','yahoo',start=datetime(2019,8,1),end=datetime(2020,1,31))
ashley.reset_index(inplace=True)
ashley['ndate'] = ashley['Date'].apply(lambda date: date2num(date))
fig,ax = plt.subplots(figsize=(16,10))
ax.set_xlabel('Dates from August_01_2019 to Jan_31_2020')
ax.set_ylabel('Prices')
ax.set_title('Ashok Leyland Candlestick Chart - pycharm generated')
candlestick_ohlc(ax,[tuple(vals) for vals in ashley[['ndate','Open','High','Low','Close']].values],width=0.5,colorup='g',colordown='r')
plt.show()