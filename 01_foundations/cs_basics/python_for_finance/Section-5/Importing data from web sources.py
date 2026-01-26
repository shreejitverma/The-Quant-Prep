
# coding: utf-8

# ### <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## Importing data from Investors Exchange (IEX)

# To fetch data from IEX, you need to first pip install iexfinace. The 'pip' command is a tool for installing and managing Python packages.
! pip install iexfinance
# Using iexfinace to access data from IEX is quite easy. First, you need to import <b>get_historical_data</b> function from iexfinance library. <br>
# <br>
# This will return the daily time series of the stock's ticker requested over the desired date range. You can select the date range using the <b>datetime</b> function. The output format (data frame creation, if pandas) is selected using the <b>output_format</b> parameter.
# 
# The resulting DataFrame is indexed by date, with a column for each OHLCV datapoint as you can see in the below example.
# 

# In[8]:


from iexfinance import get_historical_data 
from datetime import datetime

start = datetime(2017, 1, 1) # starting date: year-month-date
end = datetime(2018, 1, 1) # ending date: year-month-date

data = get_historical_data('AAPL', start=start, end=end, output_format='pandas') 
data.head()


# In[9]:


data.tail()


# ## Importing data from NSEpy

# Similar to IEX, you need to first pip install <b>nsepy</b> module to fetch the data. 
! pip install nsepy
# To fetch historical data of stocks from nsepy, you have to use <b>get_history</b> function which returns daily data of stock's ticker requested over the desired timeframe in a pandas format. 
# 
# <b>Note</b>: Only price data of Indain stocks/indices/derivatives can be fetched from nsepy. 

# In[10]:


from nsepy import get_history
from datetime import datetime

start = datetime(2017, 1, 1)
end = datetime(2018, 1, 1)

data = get_history(symbol='SBIN',start=start,end=end)

data.head()


# In[11]:


data.tail()


# ## Importing data from Quandl

# To fetch data from Quandl, first import quandl. Here, <b>quandl.get</b> function is used to fetch data for a security over a specific time period.

# In[12]:


import quandl
from datetime import datetime

# quantrautil is a module specific to Quantra to fetch stock data
from quantrautil import get_quantinsti_api_key 

api_key = get_quantinsti_api_key()
data = quandl.get('EOD/AAPL', start_date='2017-1-1', end_date='2018-1-1', api_key=api_key)

# Note that you need to know the "Quandl code" of each dataset you download. In the above example, it is 'EOD/AAPL'.
# To get your personal API key, sign up for a free Quandl account. Then, you can find your API key on Quandl account settings page.

data.head()


# ## Importing data from Yahoo

# First you need to import data from <b>pandas_datareader</b> module. Here <b>data.get_data_yahoo</b> function is used to return the historical price of a stock's ticker, over a specifc time range.  

# In[13]:


## Yahoo recently has become an unstable data source.

## If it gives an error, you may run the cell again, or try again sometime later

import pandas as pd
from pandas_datareader import data 
data = data.get_data_yahoo('AAPL', '2017-01-01', '2018-01-01')
data.head()


# ### In the upcoming iPython notebook:
# 
# We will learn about <b>Importing Data from our local machine</b>. Till then, get ready to solve some exercises.
