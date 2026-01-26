
# coding: utf-8

# # Notebook Instructions
# <i>You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter</b>. While a cell is running, a [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook [8].</i>
# 
# <i>Enter edit mode by pressing <b>`Enter`</b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area.</i>

# ## Data Visualization
# 
# This python notebook is for understanding the capabilities of 'matplotlib' library. Matplotlib is a reliable, robust and easy to use library for standard plots and is flexible when it comes to complex plots and customizations.

# In[74]:


# Loading and viewing the dataframe

import pandas as pd

infy = pd.read_csv ('infy_dv.csv')

# infy = pd.read_csv ('C:/Users/academy/Desktop/infy_dv.csv')

infy.head ()


# In[75]:


# Preparing Data to visualise

infy_close = infy [['Date','Close Price']] # The columns which we require 

infy_close.set_index('Date', inplace=True) # Setting index as date

# More on this in the upcoming section on 'Pandas'

infy_close


# ### Importing libraries
# 
# To begin with, we will import the required libraries. The main plotting functions are found in the sublibrary matplotlib.pyplot.

# In[76]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

plt.plot(infy_close)
plt.show ()


# ### A better plot representation
# 
# There are always different requirements and plotting style for presenting graphs/reports. Let us try out a few functions and customize it.

# In[77]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

# This customizes the size of the plot as per the inputs. Here 14,5 represents the breadth and length of the plot.
plt.figure(figsize = (14,5))

# This helps in plotting the blue color of the ‘infy_close’ series line graph. 
plt.plot(infy_close, 'b')
# plt.plot (infy_close, 'g') # to plot green color

# This helps in plotting the discrete red data points of the closing prices of ‘infy_close’ series.
plt.plot(infy_close,'ro')
# Here ‘r’ stands for ‘red’ and ‘o’ stands for circles while plotting our discrete data points. 
# That is why the points are colored red and default line color is blue.

# This gives a grid layout to the plot.
plt.grid(True)

# This gives the title to the plot.
plt.title ('Infosys Close Price Representation')

# This labels the x axis 
plt.xlabel ('Trading Days')

# This labels the y axis 
plt.ylabel ('Infosys Close Price')


# To plot and visualise the data
plt.show ()


# ### Plot with labelled datasets
# 
# Something that is different in this cell is the fact that we are plotting two datasets or columns in this case.

# In[78]:


# Preparing data

import pandas as pd

infy2 = pd.read_csv ('infy_dv.csv')

#infy2 = pd.read_csv ('C:/Users/academy/Desktop/infy_dv.csv')

infy2 = infy2 [['Date','Close Price', 'Open Price']] # Choosing more columns

infy2.set_index('Date', inplace=True) # Setting 'Date' column as an index

infy2


# To read the plot better, we use the plt.legend() function. plt.legend() accepts different locality parameters where 0 stands for the best location of the legend, in the sense that little data is hidden by the legend.

# In[79]:


# PLotting data

plt.figure(figsize=(20,7))

plt.plot(infy2["Close Price"], lw=1.5, label = 'Close Price')
plt.plot(infy2["Open Price"], lw=1.5, label = 'Open Price')

plt.plot(infy2,'ro')

plt.grid(True)

plt.legend(loc=0)

#This helps us tighten the figure margins
plt.axis ('tight')

plt.xlabel('Time')
plt.ylabel('Index')
plt.title ('Representative plot with two datasets')

plt.show()


# ### Scatter Plots
# 
# (Optional Read)
# 
# In a scatter plot, the values of one data serve as the x values  for the other data set. Such plots are usually used while plotting financial time series. Matplotlib provides a specific function to generate scatter plots known as the plt.scatter() function.

# In[80]:


import numpy as np
 
y = np.random.standard_normal((100,2)) # Random data created

plt.figure (figsize = (7,5))

# The function 'scatter' is called to our 'plt' object
plt.scatter(y[:,0], y[:,1], marker='o') 

plt.grid(True)
plt.xlabel ('1st dataset')
plt.ylabel ('2nd dataset')
plt.title('Scatter Plot')
plt.show() 


# ### Plotting a histogram 
# 
# (Optional Read)
# 
# Another type of plot apart from line graphs are histograms. They are often used in the context of financial returns. The code puts the frequency value of two datasets next to each other in the same plot. We use the plt.hist() function to plot the diagram.
# 

# In[81]:


# Random data created

np.random.seed(100)
y = np.random.standard_normal((25,2)).cumsum(axis=0) 

plt.figure(figsize=(10,5))

# The function 'hist' is called to our 'plt' object
plt.hist(y, label = ['1st','2nd'], bins=25)

plt.grid(True)
plt.legend(loc=0)
plt.xlabel('Index Returns')
plt.ylabel ('Stock Returns')
plt.title ('Histogram')
plt.show()


# ### In the upcoming iPython notebook:
# 
# We will learn about 3-D plotting in Python. 3-D plotting is an optional read.
# 
# Happy Learning!
