
# coding: utf-8

# ## <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## If and elif
# 
# We have seen the working of an 'if' statement in the previous video unit. Let us go through it once again.
# 
# In python, the syntax for an ‘if' conditional statement is as follows:
# 
# <pre>if (condition_1):<br>
#     statement_block_1<br>
# elif (condition_2):<br>
#     statement_block_2<br>
# elif (condition_3):<br>
#     statement_block_3<br></pre>
# <br>
# Let us consider an example to understand the working of an 'if' statement.
# 

# In[57]:


stock_price_ABC = 299 # Variable value

if (stock_price_ABC < 300): # if condition_1 is true then...
    print ("We will buy 500 shares of ABC") # statement_block_1 will get executed
    
elif (stock_price_ABC == 300): 
    print ("We will buy 200 shares of ABC") 
    
elif  (stock_price_ABC > 300):
    print ("We will buy 150 shares of ABC")


# If you change the value of the variable 'stock_price_ABC' to...

# In[58]:


stock_price_ABC = 300 # then...

if (stock_price_ABC < 300):
    print ("We will buy 500 shares of ABC")
    
elif (stock_price_ABC == 300): # if condition_2 is true then...
    print ("We will buy 200 shares of ABC") # statement_block_2 will get executed
    
elif  (stock_price_ABC > 300):
    print ("We will buy 150 shares of ABC")


# If you change the value of the variable 'stock_price_ABC' to...

# In[59]:


stock_price_ABC = 301 # then...

if (stock_price_ABC < 300):
    print ("We will buy 500 shares of ABC")
    
elif (stock_price_ABC == 300):
    print ("We will buy 200 shares of ABC")
    
elif  (stock_price_ABC > 300): # if condition_3 is true then...
    print ("We will buy 150 shares of ABC") # statement_block_3 will get executed


# ## If and else 
# 
# If - else block of conditional statements is similar to the working of 'if' statements. If the 'if' condition is <b>true</b>, then the statements inside the 'if' block will be executed. If the 'if condition is <b> false</b>, then the statements inside the 'else' block will be executed. 
# 
# In python, the syntax for an ‘if else' conditional statement is as follows:
# 
# <pre>if (condition_1):<br>
#     statement_block_1<br>
# else:<br>
#     statement_block_2<br></pre>
# <br>
# Let us consider an example to understand the working of an 'if else' statement.
# 

# In[60]:


stock_price_ABC = 300

if (stock_price_ABC > 250): # if condition 1 is true then....
    print ("We will sell the stock and book the profit") # this block of code will be executed
    
else:
    print ("We will keep buying the stock")
    


# If you change the value of the variable 'stock_price_ABC' to...

# In[61]:


stock_price_ABC = 200 # then...

if (stock_price_ABC > 250): # if condition 1 is false then....
    print ("We will sell the stock and book the profit")
    
else:
    print (" We will keep buying the stock") # this block of code will be executed


# ### <span style="color:brown"> In the upcoming iPython Notebook:</span>
# 
# We will understand about <b>Loops.</b>
