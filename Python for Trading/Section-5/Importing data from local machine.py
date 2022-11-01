
# coding: utf-8

# # Notebook Instructions
# <i>You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter</b>. While a cell is running, a [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook [8].</i>
# 
# <i>Enter edit mode by pressing <b>`Enter`</b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area.</i>

# ## Pandas.read_csv
# 
# Pandas.read_csv() function helps you to read Comma Seperated Files using Python and converts it into a dataframe.

# In[1]:


# You have to download the 'Infosys' company's CSV file from www.nseindia.com.

import numpy as np
import pandas as pd

infy = pd.read_csv ('infy_data.csv')

# This code will work only if you have stored the 'infy.csv' in the same folder where this notebook is saved.

# If you store it at some other location, then the line of code would have to specify the location.

# infy = pd.read_csv ('C:/Users/academy/Desktop/infy_data.csv')


# In[2]:


infy # this is our entire "Infosys" stock data frame


# In[3]:


infy.head () # You will see the top 5 rows


# In[4]:


infy.tail () # You will see the bottom 5 rows


# The reason why we are studying this seperately is because it is important to understand this function. You will be using this function the most while making financial trading strategies.<br>
# <br>
# Another reason is, once you download a CSV file, it becomes a stable data source. This is unlike the one you fetch from web data sources.<br>
# <br>
# We will see more of this in the <b>Pandas</b> section of our course.

# ### In the upcoming iPython notebook:
# 
# We will learn about <b>2D plotting</b> of financial market data, but before that let us solve an exercise on this.
# 
# Happy Learning!
