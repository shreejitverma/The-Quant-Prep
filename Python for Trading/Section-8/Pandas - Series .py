
# coding: utf-8

# ## <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# # Notebook Contents
# 
# ##### <span style="color:green">1. Why are we studying series?</span>
# ##### <span style="color:green">2. Series datastructure</span>
# #####  <span style="color:green">3. Methods or Functions</span>
# ##### <span style="color:green">4. pandas.Series.apply()</span>

# # Why are we studying Series?

# In python, understanding Series is a natural predecessor to understanding dataframes.<br>
# <br>
# Series are indexed data frame with only one data column. It is easier to understand them first before moving to study complex data frames.
# 

# # Series 
# 
# A series is a one-dimensional labelled 'array-like' object. The labels are nothing but the index of the data. <br>
# Or <br>
# A series is a special case of a two-dimensional array, which has only 2 columns- one column is for the index and the other column is for data. 

# In[1]:


import pandas as pd

My_Series_int = pd.Series([10, 20, 30, 40, 50, 60]) # Series created using a list

print (My_Series_int)


# The constructor for Series data structure is <font color=red>pandas.Series (data=None, index=None, dtype=None, name=None)</font>. If you are using 'pd' as alias, then it would be <font color=red>pd.Series()</font>

# In[2]:


import pandas 

My_Series_flt = pandas.Series ([10.1, 20.2, 30.4, 40.4, 50.5, 60.6]) # Series created using a list

print (My_Series_flt)


# You can see that it returns an indexed column and the data type of that column which is 'int' in this case.

# A Series is capable of holding any data type. For e.g. integers, float, strings and so on. A series can contain multiple data types too.

# In[3]:


My_Series_mixed = pd.Series ([10.1, 20, 'jay' , 40.4]) # Series created using a list

print (My_Series_mixed)


# The above series returns an 'object' datatype since a Python object is created at this instance. 

# Let us have a look at few other ways of creating series objects.

# In[4]:


# Defining series objects with individual indices 

countries = ['India', 'USA', 'Japan', 'Russia', 'China']
leaders = ['Narendra Modi', 'Donald Trump', 'Shinzo Abe', 'Vladimir Putin', 'Xi Jinpin']

S = pd.Series (leaders, index=countries) # Index is explicitly defined here 
S


# In[5]:


# Have a look at the series S1

stocks_set1 = ['Alphabet', 'IBM', 'Tesla', 'Infosys']

# Here, we are inserting data as a list in Series constructor, but the argument of its index is passed as a pre-defined list
S1 = pd.Series([100, 250, 300, 500], index = stocks_set1)

print (S1)
print ("\n")

# Now, have a look at the series S2

stocks_set2 = ['Alphabet', 'IBM', 'Tesla', 'Infosys']

# Here, we are inserting data as a list in Series constructor, but the argument of its index is passed as a pre-defined list

S2 = pd.Series([500, 400, 110, 700], index = stocks_set2)

print (S2)
print ("\n")

# We will add Series S1 and S2

print (S1 + S2)


# In[6]:


# Adding lists that have different indexes  will create 'NaN' values

stocks_set1 = ['Alphabet', 'IBM', 'Tesla', 'Infosys']
stocks_set2 = ['Alphabet', 'Facebook', 'Tesla', 'Infosys']

S3 = pd.Series([100, 250, 300, 500], index = stocks_set1)
S4 = pd.Series([500, 700, 110, 700], index = stocks_set2)


print (S3)
print("\n")

print (S4)
print("\n")

print(S3+S4)


# 'NaN' is short for 'Not a Number'. It fills the space for missing or corrupt data.<br>
# It is important to understand how to deal with NaN values, because when you import actual time series data, you are bound to find some missing or corrupted data.

# ## Methods or Functions
# 
# We will have a look at few important methods or functions that can be applied on Series. 

# ##### <span style="color:black">Series.index</span>
# It is useful to know the range of the index when the series is large.

# In[7]:


My_Series = pd.Series ([10,20,30,40,50]) # Give a better example pls, maybe import data and show range for it? 

print (My_Series.index)


# ##### <span style="color:black">Series.values</span>
# It returns the values of the series.

# In[8]:


My_Series = pd.Series ([10,20,30,40,50])

print (My_Series.values)


# ##### <span style="color:black">Series.isnull()</span>
# We can check for missing values with this method.

# In[9]:


# Remember the (S3 + S4) series? You may have a look at it

print (S3 + S4)


# In[10]:


# Returns whether the values are null or not. If it is 'True' then the value for that index is a 'NaN value

(S3 + S4).isnull()


# ##### <span style="color:black">Series.dropna()</span>
# One way to deal with the 'NaN' values is to drop them completely from the Series. This method filters out missing data.

# In[11]:


print ((S3 + S4).dropna())


# In the above output, we have produced the (S3 + S4) addition of the values and along with the series elements, and we have even dropped the 'NaN' values. 

# ##### <span style="color:black">Series.fillna(1)</span>
# Another way to deal with the 'NaN' values is to fill a custom value of your choice. Here, we are filling the 'NaN' values with the value '1'. 

# In[12]:


print ((S3 + S4).fillna(1)) # The output is self-explanatory in this case 


# ## pandas.Series.apply()
# 
# If at all one wants to 'apply' any functions on a particular series, for eg. one wants to 'sine' of each value in the series, then it is possible in pandas.
# <br>
# <font color=red>Series.apply (func)</font>
# <br>
# func = A python function that will be applied to every single value of the series.

# In[13]:


import numpy as np #Create a new series as My_Series

My_Series = pd.Series([10, 20, 30, 40, 50, 60]) 

print (My_Series)


# In[14]:


My_Series.apply(np.sin) # Find 'sine' of each value in the series


# In[15]:


My_Series.apply(np.tan) # Finding 'tan' of each value in the series

