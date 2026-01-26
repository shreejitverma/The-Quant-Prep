import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from quantrautil import get_data

start_date ='2016-1-1'
end_date ='2017-1-1'

data= get_data('AAPL', start_date, end_date)
data['Log Returns'] = np.log(data['Close']/data['Close'].shift(1))
data['20 day Historical Volatility'] = 100*pd.rolling_std(data['Log Returns'], 20)
print data.tail()
