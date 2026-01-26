
# coding: utf-8

# ### <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# We will continue from where we left in the previous notebook.
# 
# # Notebook Contents
# 
# ##### <span style="color:green">1. Indexing</span>
# ##### <span style="color:green">2. Slicing</span>
# #####  <span style="color:green">3. Arrays of 1s and 0s</span>
# ##### <span style="color:green">4. Identity function</span>

# ## Indexing

# We can access the elements of an array using its **index**. Index gives the location of an element of an array. 
# 
# - The first index is '0'.
# - The second index is '1' and so on.
# - The second last index is '-2'.
# - The last index is '-1'.
# 
# ### <span style="color:green">Indexing in a one-dimensional array</span>
# 
# A one-dimensional array is indexed just like a list.

# In[62]:


import numpy as np

# One dimensional array

A = np.array([10, 21, 32, 43, 54, 65, 76, 87])

# Print the first element of A
print(A [0])

# Remember, in pyhton, counting starts from 0 and not from 1


# In[63]:


# Print the last element of A
print(A [-1])


# In[64]:


# Print the third element of A
print (A [2])


# In[65]:


# Print the second last element
print (A [-2])


# ### <span style="color:green">Indexing in a two-dimensional array</span>
# 
# A 2-Dimensional Array consists of rows and columns, so you need to specify both rows and columns, to locate an element. 

# In[66]:


# Create a 2-Dimensional Array 

A = np.array ([ [1,2,3], [4,5,6], [7,8,9], [10,11,12] ])

print (A)

# The shape of the array is : 4 rows and 3 columns


# In[67]:


# Print the element of Row 1, column 1
print (A [0] [0])


# In[68]:


# Print the element of row 2, column 1
print (A [1] [0])


# In[69]:


# Print the element of row 4, column 3
print (A [3] [2])


# In[70]:


# Another way to print the element of row 3, column 2
print (A [2,1])


# #### <span style="color:purple">Try on your own </span>

# In[71]:


# Can you guess what will be the output of these print statement? 

print (A [4,3])


# ## Slicing 
# 
# When you want to select a certain section of an array, then you slice it. It could be a bunch of elements in a one-dimensional array and/or entire rows and columns in a two-dimensional array. 
# 
# ### <span style="color:green">Slicing a one-dimensional array  </span>
# 
# You can slice a one-dimensional array in various ways:
# - Print first few elements
# - Print last few elements
# - Print middle elements
# - Print elements after certain step. 
# 
# Syntax: 
# ####  <span style="color:blue">array_name [start: stop: step]</span>
# 

# In[72]:


# Consider a one-dimensional array A

A = np.array([1, 2, 3, 4, 5, 6, 7, 8])

# By default, the step = 1

# To print the first 4 elements (i.e. indices 0, 1, 2, 3, those before index 4)
print(A [:4])

# To print the elements from the index = 6 till the end
print(A [6:])

# To print the elements starting from index=2 and it will stop BEFORE index=5

print(A [2:5])

# To print all the elements of the array
print(A [:])


# In[73]:


# Introducing step = 2

# This will print alternate index elements of the entire array, starting from index = 0

print (A [::2])


# #### <span style="color:purple">Try on your own </span>

# In[74]:


# Can you guess what will be the output of these print statement? 

print (A [::3])


# ### <span style="color:green">Slicing a two-dimensional array  </span>
# 
# You can slice a two-dimensional array in various ways:
# - Print a row or a column
# - Print multiple rows or columns
# - Print a section of table for given rows and columns
# - Print first and/or last rows and/or columns.
# - Print rows and columns after certain step. 
# 
# Syntax: 
# ####  <span style="color:blue">array_name [row start: row stop: row step], [col start, col stop, col step]</span>

# In[138]:


# A two-dimensional Array

A = np.array([
["00", "01", "02", "03", "04"],
[10, 11, 12, 13, 14],
[20, 21, 22, 23, 24],
[30, 31, 32, 33, 34],
[40, 41, 42, 43, 44] 
])

print (A)


# In[139]:


# Print a row or a column

print(A[1,])  # Printing Row 2


# In[140]:


print(A[:,1]) # Column 2


# In[141]:


# Print multiple rows or columns

print(A[:2,]) #Rows 1 & 2

print(A[:,1:3]) #Columns 2 & 3 


# In[142]:


# Print first or last rows and columns

print(A[:3,]) # Printing first three rows

print(A[:,3:]) # Printing 4th column and onwards 


# In[143]:


# Print selected rows and columns

print(A[:2,2]) # Rows Rows 1 & 2 for column3


# In[144]:


print(A[:3,2:]) # 1st three rows for the last three columns


# In[145]:


print(A[:,:-2]) # Array without last three columns


# In[146]:


print(A[:-3,:]) # Array without last 3 rows


# #### <span style="color:green">Using step  </span>

# In[147]:


# Let us create a new array using the arange method for this exercise

A2 = np.arange(50).reshape(5,10) #Create an array with 5 rows, 10 columns that has values from 1 to 50.

print(A2)


# In[148]:


# Using step in slicing

print(A[::2,]) # Print Rows 1, 3, and 5


# In[149]:


print(A[:, 1::2]) # Print Columns 2 & 4


# In[150]:


print(A[:, 1:10:2]) # Print Columns 2,4, 6, 8, 10


# In[151]:


# This will print an intersection of elements of rows 0, 2, 4 and columns 0, 3, 9, 6 

print(A2 [::2, ::3])


# In[152]:


# Let us print all the rows and columns 

print (A2 [::,::])


# #### <span style="color:purple">Try on your own </span>

# In[153]:


# If the following line of code is self explanatory to you, then you have understood the entire concept of 2D slicing

print (A2 [2:4:1, 2:7:4])


# In[154]:


# This should be self explanatory

A = np.arange(12)
B = A.reshape(3, 4)

A[0] = 42
print(B)


# ## Array of Ones and Zeros

# We will be initialising arrays which have all the elements either as zeros or one. Such arrays help us while performing arithmentic operations

# In[155]:


O = np.ones((4,4))
print(O)

# This is defaulty datatype 'float'


# In[156]:


O = np.ones((4,4), dtype=int) # Changing data type to integers
print(O)


# In[157]:


Z = np.zeros((3,3))
print(Z)


# In[158]:


Z = np.zeros((3,3), dtype = int)
print(Z)


# ## Identity Function
# 
# An Identity Array has equal number of rows and columns. It is a square array so that the diagonal elements are all 'ones'. 

# In[159]:


I = np.identity(4)

print (I)


# In[160]:


I = np.identity (3, dtype = int)

print (I)


# ### In the upcoming iPython Notebook:
# 
# We will continue understanding about arrays and learn about Vectorization, Arithmetic Operation, Broadcasting and Array Comparisons.
