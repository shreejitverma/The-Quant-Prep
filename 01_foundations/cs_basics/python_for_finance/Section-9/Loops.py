
# coding: utf-8

# ## <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## For Loop
# 
# In the programming languages, there are many situations when you need to execute a block of code several number of times. A loop statement allows us to execute a statement or group of statements multiple times
# 
# The general syntax for a ‘for’ loop is as follows: 
# 
# <pre>
# for (variable) in <b>sequence</b>
#     block of statements
# </pre>
# 
# Here, the block of statements within the loop will get executed, until all ‘sequence’ elements get exhausted. Once all sequence elements are exhausted, the program, will come out of the loop.
# 
# 

# In[6]:


# Closing Prices of the ABC Stock over 10 days

Close_Price_ABC = [300,305,287,298,335,300,297,300,295,310] # Our sequence

for i in Close_Price_ABC:
    
    if i < 300:
        print ("We Buy")
        
    if i == 300:
        print ("No new positions")
        
    if i > 300:
        print ("We Sell")
        
print ("We are now out of the loop")


# Here, the output is what was discussed in the previous video unit.<br>
# <br>
# The variable ‘i’ first stores the value ‘300’ in it and runs it through the loop to execute the statements. Here, we have placed a condition that if ‘i == 300’ we will print “No new positions”. Hence, as you can see, this is the first statement in our output.<br>
# <br>
# Now, ‘i’ will run through the sequence and pick the second element of the sequence which is ‘305’. It will run it through the statements of the loop. When i = 305, it will execute the block where ‘if i>300: print (“We Sell”). Check the second output.<br>
# <br>
# Similarly, it will keep executing all the elements of the loop. Observe the output.
# 

# Let us take another example...

# In[7]:


import numpy as np
import pandas as pd

infy = pd.read_csv ('infy_twoweeks.csv')
infy

# We have delibrately taken a smaller dataframe to understand the output. 
# You may experiment using bigger data frames to understand the power of 'for' loop


# In[8]:


# We will just take the 'Close Price' Column to run the 'for' loop 

for i in range (len(infy)):
    
    if (infy.iloc[i]["Close Price"] < 1120):
        print ("We buy")
        
    elif ((infy.iloc[i]["Close Price"] > 1120) & (infy.iloc[i]["Close Price"] < 1150)):
        print ("We do nothing")
        
    elif (infy.iloc[i]["Close Price"] > 1150):
        print ("We Sell")


# ## While Loop
# 
# (Optional Read)
# 
# The while construct consists of a condition and block of code. 
# 
# The general syntax for a ‘while’ loop is as follows: 
# 
# <pre>
# while <b>condition/expression</b>
#     block of statements
# </pre>
# 
# To begin, the condition is evaluated.<br>
# <br>
# If the condition is true, the 'block of statements' is executed. Everytime, the condition is checked before executing the block of statements. <br>
# <br>
# This keeps on repeating unitl the condition becomes false. Once the condition is false, it comes out of the loop to execute the other statements.

# In[9]:


a = 0 # variable 

while a <= 10: # this is the condition...the loop will execute until the condition becomes 'false'
   a = a + 1
   print a
print ("We are now out of the loop")

