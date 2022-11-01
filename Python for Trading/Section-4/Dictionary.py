
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# # Dictionaries
# 
# A dictionary is generally used for mapping. Similarly, a dictionary in Python also has mapping between its “Key” and “Value” pairs. You can access the dictionary using ‘keys’ to get the information or ‘value’ stored within these ‘keys’.
# 
# 
# ## Creating & Printing Dictionaries
# 
# Dictionaries are enclosed in brace brackets and the key:value pair should be separated by a comma.

# In[165]:


new_dict = { } # Empty Dictionary

type (new_dict)


# In[166]:


# Creating a new dictionary

new_dict = {'Jack': 2563, 'Rose': 8965, 'Hockley': 7412, 'Fabrizo':9632, 'Molly Brown': 4563}

type (new_dict)


# In[167]:


# Printing the dictionary

print (new_dict)


# In[168]:


# Printing the value for a particular key

new_dict ['Jack']


# In[169]:


# Printing multiple values of various keys

new_dict ['Rose'], new_dict ['Hockley']


# ## Dictionary Manipulations
# 
# Let us have a look at the few functions for accessing or manipulating dictionaries.

# <b>len (x_dict)</b> <br>
# To know the number of key:value pairs in the dictionary.

# In[170]:


print (new_dict)


# In[171]:


len (new_dict)


# <b>x_dict.keys ( )</b> <br>
# Returns all the 'keys' of dictionaries

# In[172]:


new_dict.keys ()


# <b>x_dict.values ( )</b> <br>
# Returns all the 'values' of dictionaries

# In[173]:


new_dict.values ()


# The <b>del</b> statement <br>
# It is used for deleting any keys from the dictionary.

# In[174]:


del new_dict ['Hockley']

print (new_dict)


# x_dict.<b>pop (key) </b> <br>
# It will pop a 'value' of the reqired key.
# 

# In[175]:


new_dict.pop ('Fabrizo')


# In[176]:


print (new_dict) # Our latest dictionary


# <b>sorted</b> (x_dict) <br>
# 
# The dictionary will get sorted by its values.

# In[177]:


print (new_dict)


# In[178]:


sorted (new_dict) # keys sorted by values


# x_dict.<b>clear</b> () <br>
# Clears all the content of the dictionary

# In[179]:


new_dict.clear () 

print (new_dict)


# ### In the upcoming iPython Notebook
# 
# We will see, how 'Tuples' and 'Sets' are used.
