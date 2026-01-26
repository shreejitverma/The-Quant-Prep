
# coding: utf-8

# ### <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# # NumPy
# 
# NumPy is an acronym for "Numeric Python" or "Numerical Python".
# 
# NumPy is the fundamental package for scientific computing with Python. It is an open source extension module for Python.
# 
# 1. A powerful N-dimensional array object
# 2. Sophisticated (broadcasting) functions
# 3. Useful linear algebra, Fourier transform, and random number capabilities
# 4. Besides its obvious scientific uses, NumPy can also be used as an efficient multi-dimensional container of generic data 
# 5. Arbitrary data-types can be defined. This allows NumPy to seamlessly and speedily integrate with a wide variety of database
# 
# Source : numpy.org

# # Notebook Contents
# 
# ##### <span style="color:green">1. A simple numpy array example</span>
# ##### <span style="color:green">2. Functions to create an array</span>
# #####  <span style="color:green">3. Dimensionality of an array</span>
# ##### <span style="color:green">4. Shape of an array</span>
# ##### <span style="color:green">5. Just for fun</span>

# ## A simple numpy array example
# 
# We will create two arrays SV and S_V 
# - Using Lists
# - Using Tuples 

# In[4]:


# We will first import the 'numpy' module 

import numpy as np


# In[5]:


stock_values = [20.3, 25.3, 22.7, 19.0, 18.5, 21.2, 24.5, 26.6, 23.2, 21.2] # This is a list


# In[6]:


# Converting list into array

SV = np.array(stock_values)

print (SV)


# In[7]:


type (SV) # Understanding the data type of 'SV'


# In[8]:


stockvalues = (20.3, 25.3, 22.7, 19.0, 18.5, 21.2, 24.5, 26.6, 23.2, 21.2) # This is a tuple

# Converting tuple into array

S_V = np.array(stockvalues) 

print (S_V)


# In[9]:


type(S_V) # Understanding the data type of 'S_V'


# ## Functions to create arrays quickly 
# 
# The above discussed methods to create arrays require us to manually input the data points. To automatically create data points for an array we use these functions: 
# - **arange**
# - **linspace**
# 
# Both these functions create data points lying between two end points, starting and ending, so that they are evenly distributed. For example, we can create 50 data points lying between 1 and 10. 
# 

# ### <span style="color:green">arange </span>
# 
# Numpy.arange returns evenly spaced arrays by using a 'given' step or interval by the user.

# Syntax:
# ####  <span style="color:blue">arange ([start], [stop], [step], [dtype=None]) </span>
# 
# The 'start and the 'stop' determines the range of the array. 'Step' determines the spacing between two adjacent values. The datatype of the output array can be determined by setting the parameter 'dtype'. 

# In[10]:


# If the start parameter is not given, it will be set to 0

# '10' is the stop parameter

# The default interval for a step is '1'

# If the 'dtype' is not given, then it will be automatically inferred from the other input arguments

a = np.arange (10) # Syntax a = np.arange (0,10,1,None)
print (a)


# In[11]:


# Here the range is '1 to 15'. It will include 1 and exclude 15

b = np.arange (1,15)
print (b)


# In[12]:


# We have changed the 'step' or spacing between two adjacent values, from a default 1, to a user given value of 2

c = np.arange (0,21,2)
print (c)


# In[13]:


# Even though our input arguments are of the datatype 'float', it will return an 'int' array
# Since we have set the 'dtype' parameter as 'int'

d = np.arange (1.3,23.3,2.1,int)
print (d)


# #### <span style="color:purple">Try on your own </span>

# In[14]:


# You may now be able to understand this example, all by yourself

e = np.arange (1.4, 23.6, 1, float)
print (e)


# ### <span style="color:green">linspace </span>

# Numpy.linspace also returns an evenly spaced array but needs the 'number of array elements' as an input from the user and creates the distance automatically.

# Syntax:
# ####  <span style="color:blue">linspace(start, stop, num=50, endpoint=True, retstep=False) </span>
# 
# The 'start and the 'stop' determines the range of the array. 'num' determines the number of elements in the array. If the 'endpoint' is True, it will include the stop value and if it is false, the array will exclude the stop value.
# 
# If the optional parameter 'retstep' is set, the function will return the value of the spacing between adjacent values.

# In[15]:


# By default, since the 'num' is not given, it will divide the range into 50 individual array elements

# By default, it even includes the 'endpoint' of the range, since it is set to True by default

a = np.linspace (1,10)
print (a)


# In[16]:


# This time around, we have specified that we want the range of 1 - 10 to be divided into 8 individual array elements

b = np.linspace (1,10,8)
print (b)


# In[17]:


# In this line, we have specified not to include the end point of the range

c = np.linspace (1,10,8,False)
print (c)


# In[18]:


# In this line, we have specified 'retstep' as true, the function will return the value of the spacing between adjacent values

d = np.linspace (1,10,8,True,True)
print (d)


# #### <span style="color:purple">Try on your own </span>

# In[19]:


# This line should be self-explanatory

e = np.linspace(1,10,10,True,True)
print (e)


# ## Dimensionality of Arrays

# ### <span style="color:green">Zero Dimensional Arrays or Scalars </span>

# What we encountered in the above examples are all 'one dimensional arrays', also known as 'vectors'. "Scalars' are zero-dimensional arrays, with a maximum of one element in it. 

# In[20]:


# Creating a 'scalar'

a = np.array (50) #Should have only 1 element, at the maximum!

print ("a:", a)


# In[21]:


# To print the dimension of any array, we use 'np.dim' method

print ("The dimension of array 'a' is", np.ndim (a))


# In[22]:


# To know the datatype of the array

print ("The datatype of array 'a' is", a.dtype)


# In[23]:


# Combining it all together 

scalar_array = np.array("one_element")
print (scalar_array, np.ndim (scalar_array), scalar_array.dtype)


# ## One Dimensional Arrays
# 
# One dimensional arrays, are arrays with minimum of two elements in it in a single row. 

# In[43]:


one_d_array = np.array(["one_element", "second_element"])

print (one_d_array, np.ndim(one_d_array), one_d_array.dtype)


# In[44]:


# We have already worked with one-dimensional arrays. Let us revise what we did so far!

a = np.array([1, 1, 2, 3, 5, 8, 13, 21]) # Fibonnacci series
b = np.array([4.4, 6.6, 8.8, 10.1, 12.12])

print("a: ", a)
print("b: ", b)

print("Type of 'a': ", a.dtype)
print("Type of 'b': ", b.dtype)

print("Dimension of 'a':", np.ndim(a))
print("Dimension of 'b':", np.ndim(b))


# ## Two Dimensional
# 
# Two-dimensional arrays have more than one row and more than one column.

# In[45]:


# The elements of the 2D arrays are stored as 'rows' and 'columns'

two_d_array = np.array([ ["row1col1", "row1col2", "row1col3"], 
                       ["row2col1", "row2col2", "row2col3"]])

print(two_d_array)

print("Dimension of 'two_d_array' :", np.ndim (two_d_array))


# In[46]:


# Another example of a data table! 
# You can see how working with numpy arrays will help us working with dataframes further on! 

studentdata = np.array([ ["Name", "Year", "Marks"], 
               ["Bela", 2014, 78.2],
                ["Joe", 1987, 59.1],
               ["Sugar", 1990, 70]])

print(studentdata)

print("Dimension of 'studentdata' :", np.ndim (studentdata))


# Even though Year and Marks are non-strings, they are by default ... so I can't perform any operations on these values. 
# 
# That is where dataframe, which we will study in next section, becomes powerful 2-d data structures to be used. 
# 
# For example:

# In[41]:


# Example when we save this data as a dataframe and not as a numpy array.

import numpy as np
import pandas as pd

studentdata1 = {
                "Name": ["Bela", "Joe", "Sugar"],
                "Year": [2014, 1987, 1990],
                "Marks": [78.2, 59.1, 70]
               }

studentdata1_df = pd.DataFrame (studentdata1)
print (studentdata1_df)
print(np.mean(studentdata1_df.Marks))

# Now we are able to find average of Marks of these three students. 


# In[29]:


# The elements of the 2D arrays are stored as 'rows' and 'columns' 

a = np.array([ [1.8, 2.4, 5.3, 8.2], 
               [7.8, 5.1, 9.2, 17.13],
               [6.1, -2.13, -6.3, -9.1]])
print(a)
print("Dimension of 'a' :", np.ndim (a))

# In this array we have 3 rows and 4 columns


# In[30]:


# A 3D array is an 'array of arrays'. Have a quick look at it 

b = np.array([ [[111, 222], [333, 444]],
               [[121, 212], [221, 222]],
               [[555, 560], [565, 570]] ])

print(b)
print("Dimension of 'b' :", np.ndim (b))

# In this array, there are three, 2-D arrays


# ## Shape of an array
# 
# **What it is:** Ths shape of an array returns the number of rows (axis = 0) and the number of columns (axis = 1)
# 
# **Why is it important to understand:** It helps you to understand the number of rows and columns in an array 
# 
# **How is it different from Dimensions:** It is not that different from dimensions, just that functions called are different. 

# In[31]:


a = np.array([ [11, 22, 33],
               [12, 24, 36],
               [13, 26, 39],
               [14, 28, 42],
               [15, 30, 45],
               [16, 32, 48]])

print (a)


# In[32]:


print(a.shape)


# We can even change the shape of the array. 

# In[33]:


a.shape = (9,2)
print (a)


# You might have guessed by now that the new shape must correspond to the number of elements of the array, i.e. the total size of the new array must be the same as the old one. We will raise an exception, if this is not the case.

# In[37]:


# Shape of a 1 dimension array or scalar

a = np.array(165416113)
print(np.shape(a))


# ### <span style="color:brown"> In the upcoming iPython Notebook:</span>
# 
# We will continue understanding arrays and learning about Array indexing, Array Slicing and Arrays of Zeros and Ones, but before that let us solve some Quiz quesions and Exercises.
