import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime
from pandas.plotting import scatter_matrix

start = datetime(2015,1,1)
end = datetime(2020,1,1)

artl = web.DataReader('BHARTIARTL.NS','yahoo',start,end)
titan = web.DataReader('TITAN.NS','yahoo',start,end)
asnpt = web.DataReader('ASIANPAINT.NS','yahoo',start,end)
pdlt = web.DataReader('PIDILITIND.NS','yahoo',start,end)

stocks = pd.concat([artl['Adj Close'], titan['Adj Close'], asnpt['Adj Close'], pdlt['Adj Close']],axis=1)
stocks.columns = ['artl','titan','asnpt','pdlt']
lret = np.log(stocks/stocks.shift(1))
lret.dropna(inplace=True)

iterations = 5000

ret_arr = np.zeros(iterations)
vol_arr = np.zeros(iterations)
sr_arr = np.zeros(iterations)
wt_arr = np.zeros((iterations,len(stocks.columns)))

for i in range(iterations):
    w = np.random.random(len(stocks.columns))
    w = w/np.sum(w)
    wt_arr[i,:] = w
    ret_arr[i] = np.sum(lret.mean()*252*w)
    vol_arr[i] = np.sqrt(np.dot(w.T,np.dot(lret.cov()*252,w)))
    sr_arr[i] = ret_arr[i]/vol_arr[i]

res = sr_arr.max()

plt.figure(figsize=(12,8))
plt.scatter(vol_arr,ret_arr,c=sr_arr,cmap='plasma')
plt.colorbar(label='sharpe ratio')
plt.xlabel("Volatility")
plt.ylabel("Expected Returns")
plt.title("The maximum sharpe can be observed as "+str(res))
plt.show()
