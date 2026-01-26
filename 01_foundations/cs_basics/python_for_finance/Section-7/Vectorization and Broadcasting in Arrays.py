
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## Vectorization
# 
# Vectorization of code helps us write complex codes in a compact way and execute them faster. 
# 
# It allows to **operate** or apply a function on a complex object, like an array, "at once" rather than iterating over the individual elements. Numpy supports vectorization in an efficient way.

# # Notebook Contents
# 
# ##### <span style="color:green">1) 1D or 2D Array operations with a scalar</span>
# ##### <span style="color:green">2) 2D Array operations with another 2D array</span>
# ##### <span style="color:green">3) 2D Array operations with a 1D array or vector</span>
# #####  <span style="color:green">4) Other operators: Compare & Logical</span>
# ##### <span style="color:green">5) Just for fun</span>

# ### <span style="color:green">Array operations with a scalar </span>
# 
# Every element of the array is added/multiplied/operated with the given scalar. We will discuss:
# - Addition
# - Subtraction
# - Multiplication

# In[49]:


import numpy as np #Start the notebook with importing the packing

my_list = [1, 2, 3, 4, 5.5, 6.6, 7.123, 8.456]

V = np.array(my_list) # Creating a 1D array or vector

print (V)


# #### Vectorization Using Scalars - Addition

# In[50]:


V_a = V + 2 #Every element is increased by 2.

print(V_a)


# #### Vectorization Using Scalars - Subtraction

# In[51]:


V_s = V - 2.4 #Every element is reduced by 2.4.

print(V_s)


# #### Vectorization Using Scalars - Multiplication

# In[52]:


V2 = np.array([ [1, 2, 3], [4,5,6], [7, 8, 9] ]) #Array of shape 3,3

V_m = V2 * 10 #Every element is multiplied by 10.

print(V2)
print(V_m)


# #### <span style="color:purple">Try on your own </span>

# In[53]:


V_e = V2 ** 2 #See the output and suggest what this operation is? 

print(V_e)


# ### <span style="color:green">2D Array operations with another 2D array</span>
# 
# This is only possible when the shape of the two arrays is the same. For example, a (2,2) array can be operated with another (2,2) array. 
# 

# In[54]:


A = np.array([ [1, 2, 3], [11, 22, 33], [111, 222, 333] ]) #Array of shape 3,3
B = np.ones ((3,3)) #Array of shape 3,3
C= np.ones ((4,4)) #Array of shape 4,4
print (A)
print (B)
print (C)


# In[55]:


# Addition of 2 arrays of same dimensions (3, 3)

print("Adding the arrays is element wise: ")

print(A + B)


# In[56]:


# Addition of 2 arrays of different shapes or dimensions is NOT allowed

print("Addition of 2 arrays of different shapes or dimensions will throw a ValueError.")

print(A + C)


# In[57]:


# Subtraction of 2 arrays

print("Subtracting array B from A is element wise: ")

print(A - B)


# In[58]:


# Multiplication of 2 arrays  

A1 = np.array([ [1, 2, 3], [4, 5, 6] ]) # Array of shape 2,3
A2 = np.array([ [1, 0, -1], [0, 1, -1] ]) # Array of shape 2,3

print("Array 1", A1)
print("Array 2", A2)
print("Multiplying two arrays: ", A1 * A2)
print("As you can see above, the multiplication happens element by element.")


# You can further try out various combinations yourself, in combining scalars and arithmetic operations to get a hand on vectorization.

# ### <span style="color:green">Broadcasting allows 2D Array operations with a 1D array or vector </span>
# 
# Numpy also supports broadcasting. Broadcasting allows us to combine objects of <b>different shapes</b> within a single operation.
# 
# But, do remember that to perform this operation one of the matix needs to be a vector with its length equal to one of the dimensions of the other matrix.

# #### Try changing the shape of B and observe the results

# In[59]:


import numpy as np

A = np.array([ [1, 2, 3], [11, 22, 33], [111, 222, 333] ])
B = np.array ([1,2,3])

print (A)
print (B)


# In[60]:


print( "Multiplication with broadcasting: " )

print (A * B)


# In[61]:


print( "... and now addition with broadcasting: " )

print (A + B)


# In[62]:


# Try to understand the difference between the two 'B' arrays

B = np.array ([[1, 2, 3] * 3])

print (B)


# In[63]:


B = np.array([[1, 2, 3],] * 3)

print(B)

# Hint: look at the brackets


# In[64]:


# Another example type

B = np.array([1, 2, 3])
B[:, np.newaxis]

# We have changed a row vector into a column vector


# In[65]:


# Broadcasting in a different way (by changing the vector shape)

A * B [:, np.newaxis]


# In[66]:


# This example should be self explanatory by now

A = np.array([10, 20, 30])
B = np.array([1, 2, 3])
A[:, np.newaxis]


# In[67]:


A[:, np.newaxis] * B


# ### <span style="color:green">Other operations  </span>
# 
# - Comparison operators: Comparing arrays and the elements of two similar shaped arrays
# - Logical operators: AND/OR operants

# In[68]:


import numpy as np

A = np.array([ [11, 12, 13], [21, 22, 23], [31, 32, 33] ])
B = np.array([ [11, 102, 13], [201, 22, 203], [31, 32, 303] ])

print (A)
print (B)


# In[69]:


# It will compare all the elements of the array with each other

A == B


# In[70]:


# Will return 'True' only if each and every element is same in both the arrays

print(np.array_equal(A, B))

print(np.array_equal(A, A))


# ### <span style="color:green">Logical Operators  </span>

# In[71]:


# This should be self explanatory by now

a = np.array([ [True, True], [False, False]])
b = np.array([ [True, False], [True, False]])

print(np.logical_or(a, b))


# In[72]:


print(np.logical_and(a, b))


# This is where we will end our iPython notebooks on Numpy.
# 
# ### Happy Learning!
