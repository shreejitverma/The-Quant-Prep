
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# # Tuples
# 
# Tuple is an immutable list. Similar to lists, a tuple can contain heterogeneous sequence of elements, but it is not possible to append, edit or remove any individual elements within a tuple.
# 
# ## Creating Tuples
# Tuples are enclosed in parenthesis and the items within them are separated by commas.

# In[1]:


new_tup = () # Empty Tuple
type (new_tup)


# In[2]:


new_tup = (10, 20, 30, 40) # A tuple of integers
type (new_tup)


# In[3]:


new_tup = (10, 20.2, 'thirty', 40) # A tuple of mixed data type
type (new_tup)


# In[4]:


new_tup = ((10,20,30), (10.1, 20.2, 30.3),("ten", "twenty", "thirty")) # A nested tuple
type (new_tup)


# In[5]:


new_tup = (10,(20.2,("thirty",(40)))) # A deeply nested tuple
type (new_tup)


# ## Can we manipulate a tuple?
# 
# There are no methods supported by tuples that can help us manipulate a tuple once formed. Tuple does not even support assigning a new item at any particular index. 

# In[6]:


my_tup = (10, 20, 30, 40)  # This is the 'original' tuple which you have created

print (my_tup)


# In[827]:


my_tup [0] # Returning the item at the 0th index


# In[865]:


my_tup [0] = "40" # Assigning a new item to the 0th index 


# In[866]:


my_tup.append (50) # Trying to Append '50' at the 4th index of the created tuple. 


# But we can certainly find the length of a tuple.
# 
# <b>len</b> (x) <br>
# It returns the length of the tuple.

# In[830]:


len (my_tup)


# # Sets
# 
# A set is an unordered collection with no duplicate elements. They are useful to create lists that hold only unique values and are also mutable. The elements of a set can be anything like numbers, strings or characters.
# 
# ## Creating & Printing Sets
# Curly braces or the set () function can be used to create sets and the items within them are separated by commas.

# In[831]:


new_set = { } # Empty Set ---> An empty set cannot be created
type (new_set)


# In[832]:


new_set = {'Neo', 'Morphius', 'Trinity', 'Agent Smith', 'Oracle'} # A new set
type (new_set)


# In[833]:


print (new_set)


# In[834]:


# Now there are 5 'Agent Smiths' in our set. What will happen if we print this set?

new_set = {'Neo', 'Morphius', 'Trinity', 'Agent Smith', 'Agent Smith', 'Agent Smith', 'Agent Smith', 'Oracle'}

print (new_set) # The set will only print unique values


# In[835]:


# Using the set () function to create sets

x_set = set ('THEMATRIX')

type (x_set)


# In[836]:


print (x_set) # 'THE MATRIX' has two 'T's. Only unique values will be printed.


# In[837]:


# An additional example

y_set = set ('THETERMINATOR')

print (y_set)


# ## Set Operations
# 
# You can even perform mathematical operations like set union, set intersection, set difference and symmetric difference amongst different datasets.

# In[1]:


# We will create 2 new sets. The 'x_set' and the 'y_set'.

x_set = set ('ABCDE')
y_set = set ('CDEFG')

print (x_set) 
print (y_set)


# <b> x.union(y) </b> <br>
# This method returns all the unique items that are present in the two sets, as a new set.

# In[2]:


x_set.union(y_set)


# In[3]:


x_set | y_set # Union can be performed by using the pipe '|' operator also


# <b> x.intersection(y) </b> <br>
# This method returns the common items that are present in two sets, as a new set.

# In[5]:


x_set.intersection(y_set)


# In[6]:


x_set & y_set # Intersection can be performed by using the ampersand '&' operator


# <b> x.difference(y) </b> <br>
# This method returns the items of 'set 1' which are not common (repetitive) to the 'set 2', as a new set. 

# In[843]:


x_set.difference(y_set)


# In[844]:


x_set - y_set # Difference can be performed using the minus '-' operator


# <b> difference_update () </b> <br>
# This method removes all the elements of 'set 2' common to 'set 1' in 'set1'. It updates 'set 1'.

# In[845]:


x_set.difference_update(y_set)

print (x_set)
print (y_set)


# In[846]:


x_set = set ('ABCDE')
y_set = set ('CDEFG')

x_set = x_set - y_set # Difference update can be abbreviated in the shown manner i.e. 'x = x-y'

print (x_set)
print (y_set)


# <b>x.isdisjoint(y)</b> <br>
# This method returns True if two sets have null intersection. 

# In[847]:


x_set = set ('ABCDE')
y_set = set ('CDEFG')

x_set.isdisjoint(y_set)


# In[848]:


x_set = set ('ABC')
y_set = set ('EFG')

x_set.isdisjoint(y_set)


# <b>y.issubset(x)</b> <br>
# This method returns True for 'Set 2', if all the elements of 'Set 2' are present in 'Set 1'

# In[849]:


x_set = set ('ABCDE')
y_set = set ('CDEFG')

y_set.issubset(x_set)


# In[850]:


x_set = set ('ABCDE')
y_set = set ('CDE')

y_set.issubset(x_set)


# In[851]:


y_set < x_set # One can check a subset using a less than '<' operator.


# <b>x.issuperset(y)</b><br>
# This method returns True for 'Set 1' if all the elements of Set 2 are present in 'Set 1'. 

# In[852]:


x_set = set ('ABCDE')
y_set = set ('CDEFG')

x_set.issuperset(y_set)


# In[853]:


x_set = set ('ABCDE')
y_set = set ('CDE')

x_set.issuperset(y_set)


# In[854]:


x_set > y_set # One can check a superset using a greater than '>' operator.


# <b>x.add(e)</b> <br>
# It adds a single item to the set and updates the set.

# In[855]:


x_set = set ('ABCDE')

print (x_set)


# In[856]:


x_set.add('FGH')

print (x_set)


# <b> x.discard(e)</b> <br>
# It removes a single item from the set and updates it.

# In[857]:


print (x_set)


# In[858]:


x_set.discard('FGH')

print (x_set)


# <b> x.pop () </b> <br>
# It pops and returns any arbitary item from the set.

# In[859]:


print (x_set)


# In[860]:


x_set.pop()


# <b> x.copy () </b> <br>
# It creates a shallow copy of any set.

# In[861]:


print (x_set) # There are only 4 items in the set, since one just got popped in the above cell execution.


# In[862]:


x_set.copy()


# <b> x.clear() </b> <br>
# It clears all the items of the set.

# In[863]:


print (x_set)


# In[864]:


x_set.clear()

print (x_set)


# ### This is where we will end this section on Data Structures
# 
# Stay tuned for the next Section.
