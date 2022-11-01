
# coding: utf-8

# ### <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# In this particular notebook, we will have a look at the different descripive statistical functions available in Python. 
# 
# # Notebook Contents
# 
# ##### <span style="color:green">1. DataFrame.count()</span>
# ##### <span style="color:green">2. DataFrame.min()</span>
# #####  <span style="color:green">3. DataFrame.max()</span>
# ##### <span style="color:green">4. DataFrame.mean()</span>
# ##### <span style="color:green">5. DataFrame.median</span>
# ##### <span style="color:green">6. DataFrame.mode()</span>
# ##### <span style="color:green">7. DataFrame.sum()</span>
# ##### <span style="color:green">8. DataFrame.diff()</span>
# ##### <span style="color:green">9. DataFrame.pct_change()</span>
# ##### <span style="color:green">10. DataFrame.var()</span>
# ##### <span style="color:green">11. DataFrame.std()</span>
# ##### <span style="color:green">12. DataFrame.rolling(window=).mean()</span>
# ##### <span style="color:green">13. DataFrame.expanding(min_periods=).mean()</span>
# ##### <span style="color:green">14. DataFrame.cov()</span>
# ##### <span style="color:green">15. DataFrame.cor()</span>
# ##### <span style="color:green">16. DataFrame.kur()</span>
# ##### <span style="color:green">17. DataFrame.skew()</span>

# In[619]:


# Loading and viewing data

# We have stored an 'infy.csv' file on our desktop

import numpy as np
import pandas as pd

infy = pd.read_csv ('C:/Users/academy/Desktop/infy.csv')


# Once you import or load your OHLC data in a data frame, it is a good habit to print the the 'head' and 'tail' of that data frame. <br>
# <br>
# This helps you to be sure, whether the 'dates' of your data frame, is correct or not. Further, the 'column names' are also displayed, which helps you in easy manipulation of your data frame.
# 

# In[620]:


infy.head() # Printing the first five rows of your data frame


# In[621]:


infy.tail() # Printing the last five rows of your data frame


# ### DataFrame.count()
# 
# This method returns the number of non-null observations over the requested observations.

# In[622]:


print (infy.count())


# If you want to know, the number of non-null observations in a particular column then below is how you do it.

# In[623]:


print (infy["Close Price"].count())


# ### DataFrame.min()
# 
# This method returns the minimum value over the requested observations.

# In[624]:


print(infy["Close Price"].min())


# ### DataFrame.max()
# 
# This method returns the maximum value over the requested observations.

# In[625]:


print(infy["Close Price"].max())


# ### DataFrame.mean()
# 
# This method returns the mean of the requested observations.

# In[626]:


print(infy["Close Price"].mean())


# ### DataFrame.median()
# 
# This method returns the median of the requested observations.

# In[627]:


print(infy["Close Price"].median())


# ### DataFrame.mode()
# 
# This method returns the mode of the requested observations.

# In[628]:


print(infy["Close Price"].mode()) # The "Close Price" series of infosys stock is multi-modal


# ### DataFrame.sum()
# 
# This method returns the sum of all the values of the requested observations.

# In[629]:


print (infy["Total Traded Quantity"].sum())# If someone just wants to know the sheer amount of Infosys stocks traded over 2 years


# ### DataFrame.diff()
# 
# This method returns the 'difference' between the current observation and the previous observation.

# In[630]:


print (infy["Close Price"].diff())


# ### DataFrame.pct_change()]
# 
# This method returns the percentage change of the current observation with the previous observation.

# In[631]:


print (infy["Close Price"].pct_change())


# Visualising this, give us a generic inference about the daily price fluctuation in the closing price of Infosys stock.

# In[632]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

plt.figure(figsize = (20,10))
plt.ylabel('Daily returns of Infosys')
infy["Close Price"].pct_change().plot()
plt.show()


# ### DataFrame.var()
# 
# This method returns of the variance of the requested observations.

# In[633]:


print (infy["Close Price"].var())


# ### DataFrame.std()
# 
# This method returns the standard deviation of the requested observations.

# In[634]:


print (infy["Close Price"].std())


# ### DataFrame.rolling(window=).mean()
# 
# This method helps us to calculate the moving average of the observations. 

# In[635]:


print (infy["Close Price"].rolling(window = 20).mean()) # The moving average window is 20 in this case


# A moving average of the Close price with window = 20, smoothens the closing price data. You may have a look at it. We have plotted the daily Closing Price of Infosys and Moving Average (window = 20) of the daily Closing Price of Infosys against time.

# In[636]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

plt.figure(figsize = (20,10))
plt.ylabel('Closing Price')

infy["Close Price"].rolling(window = 20).mean().plot()
infy["Close Price"].plot()
plt.show()


# ### DataFrame.expanding(min_periods=).mean()
# 
# This method returns the 'expanding' mean of the requested observations.
# 
# A common alternative to rolling mean is to use an expanding window mean, which returns the value of the mean with <b>all the observations avaliable up to that point in time.</b>

# In[637]:


print (infy["Close Price"].expanding(min_periods = 20).mean())


# You may visualise expanding mean with the below code.

# In[638]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

plt.figure(figsize = (20,10))
plt.ylabel('Daily returns of Infosys')

infy["Close Price"].expanding(min_periods = 20).mean().plot()
infy["Close Price"].plot()
plt.show()


# Let us import another stock's data. We have saved the TCS (Tata Consultancy Services) data in our local machine as 'tcs.csv'.

# In[639]:


import numpy as np
import pandas as pd

tcs = pd.read_csv ('C:/Users/academy/Desktop/tcs.csv')

tcs.head()


# In[640]:


tcs.tail()


# In[641]:


tcs["Close Price"].count()


# ### DataFrame.cov()
# 
# This method returns the covariance between the closing price of the Infosys stock with the closing price of the TCS stock. 

# In[642]:


print (infy["Close Price"].cov(tcs["Close Price"]))


# ### DataFrame.corr()
# 
# This method returns the correlation between the closing price of the infosys stock with the closing price of the TCS stock.

# In[643]:


print (infy["Close Price"].corr(tcs["Close Price"]))


# A correlation of 0.53 indicates a quite strong correlation between these two stocks.

# ### DataFrame.kurt()
# 
# This method returns unbiased kurtosis over the requested data set using the Fisher's definition of kurtosis (where kurtosis of normal distribution = 0).

# In[644]:


print (tcs["Close Price"].kurt())


# A positive kurtosis value indicates a leptokurtic distribution.

# In[645]:


print (infy["Close Price"].kurt())


# A negative kurtosis value indicates a platykurtic distribution.

# ### DataFrame.skew()
# 
# This method unbiased skew over the requested data set.

# In[646]:


print (tcs["Close Price"].skew())


# The distribution is positively skewed.

# In[647]:


print (infy["Close Price"].skew())


# The distribution is positively skewed. However, TCS' distribution is more positively skewed than Infosys' distribution.

# Let us have visualise both the distributions and see whether the above said sentences are making sense or not. 

# In[648]:


# Infosys Distribution

import seaborn as sns

sns.set(color_codes = True)

sns.distplot(infy["Close Price"]);


# In th above diagram, you can see why the infosys close price distribution is platykurtic and positively skewed.

# In[649]:


# TCS Distribution

import seaborn as sns

sns.set(color_codes = True)

sns.distplot(tcs["Close Price"]);


# In th above diagram, you can see why the TCS close price distribution is leptokurtic and positively skewed. <br>
# <br>
# A trained eye is statistics will also be able to see that the TCS stock closing prices are more positively skewed than the Infosys stock closing prices.
# 

# ### <span style="color:brown"> In the upcoming iPython Notebook:</span>
# 
# We will continue understanding about Pandas: Grouping and Reshaping.
