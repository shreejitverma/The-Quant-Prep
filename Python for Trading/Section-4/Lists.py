
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# # Lists
# 
# Lists in Python, are used to store heterogeneous types of data. Lists are mutable i.e. one can change the content within a list, without changing its identity.
# 
# ## Creating Lists
# List are enclosed by square brackets and elements should be separated by comma.

# In[59]:


new_list = [ ] # Empty List
type (new_list)


# In[60]:


new_list = [10, 20, 30, 40] # A list of integers
type (new_list)


# In[61]:


new_list = [10, 20.2, "thirty", 40] # A list of mixed data types
type (new_list)


# In[62]:


new_list = [[10,20,30], [10.1, 20.2, 30.3],["ten", "twenty", "thirty"]] # A nested list
type (new_list)


# In[63]:


new_list = [10,[20.2,["thirty",[40]]]] # A deeply nested list
type (new_list)


# ## Different Methods for List Manipulation
# Let us have a look at few of the methods, with which we can manipulate lists.<br>
# <br>
# Please Note: A function or a method is a block of code which is used to perform a single task or a set of tasks repeatedly.

# In[64]:


my_list = [10,20,30,40] # This is the 'original' list which you have cerated 

print (my_list)


# list.<b>append</b> (x) <br>
# Add an item to the end of the list.

# In[65]:


my_list.append (50)

print (my_list)


# list.<b>extend</b> (x) <br>
# Extend the list by appending all the items at the end of the list.

# In[66]:


my_list.extend ([60,70,80,90])

print (my_list)


# list.<b>insert</b> (i,x) <br>
# Insert an item at any given position within the list. The first argument 'i', is the index of the item before which you want to insert something. To insert something at the beginning of the list, you may type list.insert (0,x)

# In[67]:


my_list.insert (0,0) # Inserting an item in the beginning

print (my_list)


# In[68]:


my_list.insert (10,100) # Inserting an item at the end or at the integer location of 10 in this case

print (my_list)


# In[69]:


my_list.insert (6,55) # Inserting an item at the 6th position in a list

print (my_list)


# list.<b>remove</b> (x)<br>
# Remove the first item from the list whose value is 'x'. It is an error if there is no such item.

# In[70]:


my_list.remove(0)

print (my_list)


# list.<b>pop</b> (i) <br>
# Remove any item from any given position (index) in the list. If no index is specified, it removes and returns the last element from the list.

# In[71]:


my_list.pop (5) # Removes and returns the '5th' element from the list


# In[72]:


print (my_list)


# In[73]:


my_list.pop () # Removes and returns the last element from the list


# In[74]:


print (my_list)


# list.<b>index</b> (x) <br>
# It returns a zero-based index in the list of the first item whose value is x. Raises an error of there is no such item as 'x'.

# In[75]:


my_list.index (50)


# In[76]:


my_list.index(10)


# In[77]:


print (my_list)


# list.<b>count</b> (x) <br>
# Returns the number of times 'x' appears in the list

# In[78]:


new_list = [10,10,10,20,30,40,50] # This is a new list

new_list.count(10)


# list.<b>reverse</b> () <br>
# It reverses the items of the list.

# In[79]:


print (my_list)


# In[80]:


my_list.reverse ()

print (my_list)


# list.<b>sort</b> () <br>
# It sorts the items in the list.

# In[81]:


new_list = [12, 35, 76, 20, 56, 34, 65]
print (new_list)


# In[82]:


new_list.sort()

print (new_list)


# ### In the upcoming iPython Notebook
# 
# We will see, how Lists are used as:
# 
# 1. 'Stacks'
# 2. 'Queues'
# 3. 'Graphs'
# 4. 'Trees'
# 
# So, Stay Tuned!
