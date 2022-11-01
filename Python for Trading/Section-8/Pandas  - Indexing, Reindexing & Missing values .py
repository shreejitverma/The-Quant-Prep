
# coding: utf-8

# ## <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# In this notebook, we will have a look at the different descripive statistical functions available in Python. 
# 
# ## Notebook Contents
# 
# ##### <span style="color:green">1. Indexing using .loc()</span>
# ##### <span style="color:green">2. Indexing using .iloc()</span>
# #####  <span style="color:green">3. Indexing using .ix()</span>
# ##### <span style="color:green">4. Missing Values</span>
# ##### <span style="color:green">5. Data Frame.isnull()</span>
# ##### <span style="color:green">6. Data Frame.notnull()</span>
# ##### <span style="color:green">7. DataFrame.fillna()</span>
# ##### <span style="color:green">8. DataFrame.dropna()</span>
# ##### <span style="color:green">9. Replacing values</span>
# ##### <span style="color:green">10. Reindexing</span>

# # Loading and Viewing Data

# Before we start, let us import OHLC time series data of Infosys stock for only 'two weeks'. With a smaller data frame, understanding 'Indexing' would be more intutive. 

# In[31]:


# Loading and Viewing data 

import numpy as np
import pandas as pd

infy = pd.read_csv ('infy_twoweeks.csv')


# In[32]:


infy # This is the entire 'Infosys two weeks' time series data frame.


# In[33]:


infy.shape # This data frame has 10 rows and 12 columns 


# ## Indexing
# 
# Indexing provides us with the axis labelling information in pandas. Further, it helps us to identify the exact position of data, which is important while analysing data. <br>
# <br>
# While sudying indexing, we will also focus on how to slice and dice the data according to our needs in a Data Frame.

# ## Indexing using .loc()
# 
# It is a 'label-location' based indexer for selection of data points.

# In[34]:


# Using .loc()

#import the pandas library and aliasing as pd

import pandas as pd
import numpy as np

#select all rows for a specific column 

print (infy.loc[:,'Close Price'])


# In[35]:


# Select all the rows of these specific columns

print (infy.loc[:, ['Close Price','Open Price']])


# In[36]:


# Select the first five rows of the specific columns

# Remember that the '.loc()' method INCLUDES the rows and columns in its stop argument.

# Observe that '0:4' will include 5 rows from index 0 to 4

# The loc indexer takes the row arguments first and the column arguments second.

print (infy.loc[:4,['Close Price','Open Price']])


# In[37]:


# Select the rows 2 to 7 of all the columns from the data frame 

print (infy.loc[2:7])


# In[38]:


# Select the rows and columns specified

print (infy.loc[[0,1,2,3,4,5],['Open Price', 'High Price', 'Low Price', 'Close Price']])


# In[39]:


# To check if the fifth row's values are greater than 1130.

print (infy.loc[4]>1130)


# ## Indexing using .iloc()
# 
# Another way to perform indexing is using the 'iloc()' method.

# In[40]:


# Using .iloc()

# Select the first four rows of all the columns

# Remember that the '.loc()' method DOES NOT include the rows and columns in its stop argument

# Observe that '0:4' will include 4 rows from index 0 to 3

print (infy.iloc[:4])


# In[41]:


# Let us play more with the indexes of both rows and columns

# Select the rows from index 1 to index 4 (4 rows in total) and Columns with index from  2 to  3 (2 columns)

# .iloc() is similar to numpy array indexing

# iloc is extremely useful when your data is not labelled and you need to refer to columns using their integer location instead

print (infy.iloc[1:5, 2:4])


# In[42]:


# Selecting the exact requested columns

print (infy.iloc[[1, 3, 5,7], [1, 3, 5, 7, 9]])


# In[43]:


# Selecting the first two rows and all the columns

print (infy.iloc[1:3, :])


# In[44]:


print (infy.iloc[:,1:3])


# ## Indexing using .ix()
# 
# Another way to perform indexing is using the 'ix()' method.
# 
# ##### <span style="color:red">ix indexer has been depricated in the latest version of pandas, but we having discussed it just for your information</span>
# 

# In[45]:


# Using .ix()

# Remember that the '.ix()' method INCLUDES the rows and columns in its stop argument.

# Observe that '0:4' will include 5 rows from index 0 to 4

# We are selecting the first five rows and all the columns of our data frame

print (infy.ix[:4])


# In[46]:


# Select rows from index 2 to index 5, only of the 'Close Price' Column

print (infy.ix[2:5,'Close Price'])


# In[47]:


# You will be able to understand this by now! 

print (infy.ix[2:5, 4:9])


# In[48]:


# Just some revision for choosing columns in a data frame, since it is important

# Choosing a specific column from a data frame

print (infy['Close Price'])


# In[49]:


# Choosing multiple columns from a data Frame 

print (infy[['Open Price', 'High Price', 'Low Price', 'Close Price']])


# ## Missing Values
# 
# Missing values are values that are absent from the data frame. Usually, all the data frames that you would work on, would be large and there will be a case of 'missing values' in most of them. <br>
# <br>
# Hence, it becomes important for you to learn how to handle these missing values.

# In[51]:


# We have deliberately created 'missing values' in the same 'Infosys two weeks' data which you have used above.

# Have a look at the entire data frame 

import numpy as np
import pandas as pd

infy = pd.read_csv ('infy_twoweeks_nan.csv')

infy


# ## DataFrame.isnull()
# 
# This method returns a Boolean result.<br>
# <br>
# It will return 'True' if the data point has a 'NaN' (Not a Number) value. Missing data is represented by a NaN value. 

# In[52]:


# Understanding the 'NaN' values of the 'Close Price' column in the infy data frame

print (infy['Close Price'].isnull())


# In[53]:


# Understanding the 'NaN' values of the entire data frame

print (infy.isnull())


# ## DataFrame.notnull()
# 
# This method returns a Boolean result.<br>
# <br>
# It will return 'Flase' if the data point is not a 'NaN' (Not a Number) value. Missing data is represented by a NaN value. 

# In[54]:


print (infy['Close Price'].notnull())


# ## DataFrame.fillna()
# 
# The .fillna() method will fill all the 'NaN' Values of the entire data frame or of the requested columns with a scalar value of your choice. 

# In[55]:


# Replace NaN with a Scalar Value of 1000

print (infy.fillna(1000))


# In[56]:


# This will fill the 'Close Price' column with the scalar value of 5

print (infy['Close Price'].fillna(5))


# In[57]:


# If we want to do 'fillna()' using the 'backfill' method, then backfill will the take the value from the next row 
# and fill the NaN value with that same value

print (infy['Close Price'])

print (infy['Close Price'].fillna(method='backfill'))


# In[58]:


# It is even possible to do it for the entire data frame with the 'backfill' values

print (infy.fillna(method='backfill'))


# In[59]:


# 'bfill' does the same thing as 'backfill'

print (infy['Close Price'])

print (infy['Close Price'].fillna(method='bfill'))


# In[60]:


# If we want to do 'fillna()' using the 'ffill' method, then ffill will the take the value from the previous row.. 
# ..and fill the NaN value with that same value

print (infy['Close Price'])

print (infy['Close Price'].fillna(method='ffill'))


# In[61]:


# 'pad' does the same thing as 'ffill'

print (infy['Close Price'])

print (infy['Close Price'].fillna(method='pad'))


# ## DataFrame.dropna()
# 
# This method will drop the entire 'row' or 'column' which has even a single 'NaN' value present, as per the request.

# In[62]:


# By default, dropna() will exclude or drop all the rows which has even one NaN value in it

print (infy.dropna())


# In[63]:


# If we specify the axis = 1, it will exclude or drop all the columns which has even one NaN value in it

print (infy.dropna(axis=1))


# ## Replacing values
# 
# Replacing helps us to select any data point in the entire data frame and replace it with the value of our choice.

# In[64]:


# Replace Missing (or) Generic Values

import pandas as pd
import numpy as np

# Let us do this a bit differently. We will create a Data Frame using the 'pd.DataFrame' constructor

df = pd.DataFrame({'one':[10,20,30,40,50,2000],'two':[1000,0,30,40,50,60]})

print (df)


# In[65]:


# .replace() will first find the value which you want to replace and replace it the value you have given.

# eg: In the below '1000' is the value it will find and replace it with '10'

print (df.replace({1000:10,2000:60}))


# In[66]:


print (infy['Close Price'])


# In[67]:


# This should be self explanatory

print (infy['Close Price'].replace({1147.55:3000}))


# In[68]:


print (infy['Close Price'].replace({NaN:1000000})) # We cannot replace NaN values, since they are not defined.


# ## Reindexing 
# 
# Reindexing changes the row labels and column labels of a DataFrame.<br> 
# <br> 
# To reindex means to conform the data to match a given set of labels along a particular axis.

# In[69]:


import pandas as pd
import numpy as np

print (infy)


# In[70]:


# Here we have changed the shape of data frame by using reindexing

infy_reindexed = infy.reindex(index = [0,2,4,6,8], columns = ['Open Price', 'High Price', 'Low Price','Close Price'])

print (infy_reindexed)

