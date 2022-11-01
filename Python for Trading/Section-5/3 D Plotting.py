
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## 3D plotting
# 
# (Optional Read)
# 
# We are going to plot a 3 dimensional figure using 3 datasets.<br>
# <br>
# Not many financial data visualisations benefit from 3-D plotting but one of the applications is the volatility surfaces showing implied volatilities simultaneously.<br>
# <br>
# You may just go through the codes. It is not a problem if you do not understand them and the the motive of this notebook is more for representation purposes and show you the power of data visualisation in Python by plotting even 3D plots.

# In[99]:


# Random data creation using the numpy library

import numpy as np

strike_price = np.linspace (50,150,25) # Strike values between 100 to 150
time = np.linspace (0.5, 2, 25) # Time to maturity between 0.5 to 2.5 years

# The numpy's meshgrid() function helps us to create a rectangular grid out of an array of x values and y values

strike_price, time = np.meshgrid (strike_price, time)


# In[100]:


strike_price, time [:] # Printing the mesh grid array


# In[101]:


# generate fake implied volatilities

implied_volatility = (strike_price - 100) ** 2/ (100 * strike_price)/ time


# In[102]:


# Plotting a 3D figure

import matplotlib.pyplot as plt

# Importing the required packages for 3D plotting 
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure (figsize = (9,6))

# If 'fig' is a variable holding a figure, fig.gca() returns the axes associated with the figure. 
# With this 3 dimensional axes is enabled
axis = fig.gca (projection = '3d')

# To plot the surface and passing the required arguments
surface = axis.plot_surface (strike_price, time, implied_volatility, rstride = 1, cstride = 1, cmap = plt.cm.coolwarm, linewidth = 0.5, antialiased = False)

axis.set_xlabel ('strike')
axis.set_ylabel ('time-to-maturity')
axis.set_zlabel ('implied volatility')

# Adding a colorbar which maps values to colors
fig.colorbar (surface, shrink = 0.5, aspect=5)

plt.show()


# ### In the upcoming iPython notebook:
# 
# We will learn about Candlesticks in Python. Even that is an optional read.
# 
# Happy Learning!
