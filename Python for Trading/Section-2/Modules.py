
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# # Modules
# 
# Any file in python which has a .py extension can be a module. A module can consist of arbitrary objects, classes, attributes or functions which can be imported by users.

# ### Importing Modules
# 
# There are different ways to import modules. Let us begin by importing the 'math' module.

# In[67]:


import math


# Math module which consists of mathematical constants and functions like math.pi, math.sine, math.cosine etc.

# In[68]:


math.pi # The value of pi


# In[69]:


math.cos (1) # The cosine value of 1


# In[70]:


math.sin (1) # The sine value of 1


# ### The dir () function
# 
# The built-in function called dir() is used to find out what functions a module defines. It returns a sorted list of strings.

# In[71]:


dir (math)


# If you require only <b>certain objects</b> from the module then:

# In[72]:


from scipy import mean # We will import only the 'mean' object from the 'scipy' package


# In[73]:


mean ([1,2,3,4,5]) # This will give arithmetic mean of the numbers


# But if we want to find out, the harmonic mean. The following cells is the piece of code. 

# In[74]:


from scipy import stats


# In[75]:


stats.hmean ([1,2,3,4,5])


# If at all you require to import all the objects from the module, you may use * 

# In[76]:


from numpy import *


# In[77]:


sin (1)


# In[78]:


diag([1,5,9,6])


# One can even import a module/package as an alias and prefix it before using the objects.

# In[79]:


import numpy as np


# In[80]:


dir (np)


# In[81]:


np.median([4,5,6,3,4,5,9,8,7,12]) # Will return the median of the number set


# In[82]:


np.min([4,5,6,3,4,5,9,8,7,12]) # Will return the minimum number of the number set


# In[83]:


np.max([4,5,6,3,4,5,9,8,7,12]) # Will return the maximum number of the number set


# ### Stay tuned for more on python.
