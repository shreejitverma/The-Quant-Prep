
# coding: utf-8

# ### <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## What is lambda?
# 
# The lambda operator is a way to create small <b>anonymous functions</b> i.e. functions without a name.<br>
# <br>
# They are temporary functions i.e. they are needed only where they have been created.<br>
# <br>
# The lambda feature was added in Python due to a high demand from the Lisp programmers (Lisp is a programming language).

# ## A Simple Lambda Example
# 
# The general syntax for Lambda is as follows:<br>
# <pre><b>lambda</b> argument_list: expression</pre>
# Let us have a look at some of the examples.

# In[101]:


sum = lambda x,y : x + y


# In[102]:


sum (2,3)


# It is similar to defining a function where x and y are the parameters and x + y is the operation performed in the block of codes.<br>
# <br>
# You can even observe, that the usage lambda is same as a function call.  

# In[103]:


# Another example

product = lambda x,y : x * y


# In[104]:


product (2,3)


# In[105]:


# One more example

my_operation = lambda x,y,z : x + y - z


# In[106]:


my_operation (10,20,30)


# ### map () 
# 
# One of the advantages of using a lambda is the map() function.<br>
# <pre> map (<b>lambda</b>, sequence of lists)</pre>
# map() applies the lambda function to all the elements within the sequence. These elements are generally lists.

# In[107]:


# The lists have to be of same length to apply the map () function in lambda.

list_1 = [1,2,3,4]

list_2 = [10,20,30,40]

list_3 = [100,200,300,400]


# In[108]:


map (lambda x,y : x + y, list_1, list_2 )


# In[109]:


map (lambda x,y,z : x + y + z, list_1, list_2, list_3 )


# In[110]:


map (lambda y,z : y + z, list_2, list_3 )


# ### filter ()
# Another advantage of using a lambda is the filter() function.<br>
# <pre> filter (<b>lambda</b>, list)</pre>
# It is an elegant way to filter out the required elements from a list.

# In[111]:


fib = [0,1,1,2,3,5,8,13,21,34,55] # This is a list


# In[112]:


filter (lambda x: x > 8, fib)


# In[113]:


filter (lambda x: x < 8, fib)


# In[114]:


signals = ['Buy','Sell','Sell','Buy','Buy','Sell','Buy'] # This is a list


# In[115]:


filter (lambda x: x == 'Buy', signals)


# ### <span style="color:brown"> In the upcoming iPython Notebooks:</span>
# 
# We will understand about the <b>Numpy</b> library, in python.
