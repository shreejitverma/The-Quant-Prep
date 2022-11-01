
# coding: utf-8

# ### <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## A Simple User-Defined Function 
# 
# Let us create a simple mathematical function.
# 
# The syntax for constructing a function is:
# <pre>
# def function_name (parameter-list):
# 	Statements, i.e function body
#     return a value, if required
# </pre>
# Let us create ‘my_function’.
# 

# In[28]:


def my_function(x, n):
    output = x ** n
    return output


# This is a simple function which we have created to calculate the exponential of any number. Now, whenever we need to perform this particular calculation, all we need to do is <b>call</b> this function and insert the values for <b>‘x’</b> and <b>‘n’</b>. You may have a look it.

# In[29]:


my_function (10, 2) ## 10 raise to 2 = 100


# In[30]:


my_function (5,3) ## 5 raise to 3 = 125


# ## Bollinger Band Function
# 
# This is the function which we discussed in the video unit.

# In[31]:


def Bollinger_Bands (data, n): 
    
    #MA = data['Close'].rolling(window=n).mean() # Calculating the moving average
    MA = pd.rolling_mean(data['Close'],n)

    #SD = data['Close'].rolling(window=n).std() # Calculating the standard deviation
    SD = pd.rolling_std(data['Close'],n)

    data['Lower_BB'] = MA - (2 * SD) # Lower Bollinger Band
    data['Upper_BB'] = MA + (2 * SD) # Upper Bollinger Band
   
    return data


# In[32]:


## Load and view Nifty data

import pandas as pd

nifty = pd.read_csv('nifty_data.csv')
nifty.head()



# In[33]:


# Calling Bollinger Bands for 'Nifty' index price data 

n = 21 # We have kept the window of the moving average as 21 days

nifty_bb = Bollinger_Bands(nifty, n) # Calling the Bollinger Bands function cerated by us

nifty_bb.tail()


# In[34]:


# Plotting the Bollinger Bands for "Nifty' index

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

plt.figure(figsize=(20,10))

plt.plot(nifty_bb.Close)
plt.plot(nifty_bb.Lower_BB)
plt.plot(nifty_bb.Upper_BB)
plt.grid(True)

plt.show()


# In[35]:


# Calling Bollinger Bands for 'Infosys' price data 

import pandas as pd

infy = pd.read_csv ('infy_data_bb.csv') # Loading 'Nifty Index' data

n = 21 # We have kept the window of the moving average as 21 days

infy_bb = Bollinger_Bands(infy, n) # Calling the Bollinger Bands function cerated by us

infy_bb.tail()


# In[36]:


# Plotting the Bollinger Bands for "Infosys" stock

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

plt.figure(figsize=(20,10))

plt.plot(infy_bb.Close)
plt.plot(infy_bb.Lower_BB)
plt.plot(infy_bb.Upper_BB)
plt.grid(True)

plt.show()


# ### <span style="color:brown"> In the upcoming iPython Notebook:</span>
# 
# We will understand the <b>Lambda</b> operator and its relation with functions.
