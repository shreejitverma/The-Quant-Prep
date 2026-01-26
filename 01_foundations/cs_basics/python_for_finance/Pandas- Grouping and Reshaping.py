
# coding: utf-8

# ## <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## Pandas 'Groupby'
# 
# Any groupby operation involves one of the following operations on the original dataframe/object. They are:
# <br>
# 1. <b>Splitting</b> the data into groups based on some criteria.<br>
# <br>
# 2. <b>Applying</b> a function to each group seperately.<br>
# <br>
# 3. <b>Combining</b> the results into a single data frame.<br>
# <br>
# Splitting the data is pretty straight forward. What adds value to this split is the 'Apply' step. This makes 'Groupby' function interesting. In the apply step, you may wish to do one of the following: <br>
# <br>
# a. Aggregation − Computing a summary statistic. Eg: Compute group sums or means.<br>
# <br>
# b. Transformation − perform some group-specific operation. Eg: Standarizing data (computing zscore) within the group.<br> 
# <br>
# c. Filtration − discarding the data with some condition.<br> 
# <br>
# Let us now create a DataFrame object and perform all the operations on it

# In[1]:


# Creating a data frame

import pandas as pd

my_portfolio = {'Sector': ['IT', 'FMCG', 'Finance', 'Pharma', 'Pharma',
                          'FMCG', 'FMCG', 'IT', 'Finance', 'Real Estate'],
            
            'Company':   ['Infosys', 'Dabur', 'DHFL', 'Divis Lab', 'Lupin',
                         'Ruchira Papers', 'Britianna','Persistent Systems','Bajaj Finance', 'DLF'],
            
            'MarketCap': ['Large Cap','Large Cap','Mid Cap','Mid Cap','Mid Cap',
                         'Small Cap','Mid Cap','Small Cap','Large Cap','Mid Cap'],
            
            'Share Price': [1120,341,610,1123,741,185,5351,720,1937,217],
                
            'Amount Invested': [24000,16000,50000,23000,45000,12000,52000,18000,5000,3500]}

mp = pd.DataFrame(my_portfolio)

mp


# ### View Groups

# In[2]:


print (mp.groupby('MarketCap').groups)


# There are 3 Groups formed, if we group it by <b>'Market Cap'</b>. They are:<br>
# <br>
# Group 1: 'Large Cap' (3 companies at index 0,1,8)<br>
# Group 2: 'Mid Cap' (5 companies at index 2,3,4,6,9)<br>
# Group 3: 'Small Cap' (2 companies at index 5,7)<br>

# In[3]:


# Understand this Grouping

print (mp.groupby('Sector').groups)


# There are 5 Groups formed, if we group it by <b>'Sector'</b>. They are:<br>
# <br>
# Group 1: 'FMCG' (3 companies at index 1,5,6)<br>
# Group 2: 'IT' (2 companies at index 0,7)<br>
# Group 3: 'Pharma' (2 companies at index 3,4)<br>
# Group 4: 'Finance' (2 companies at index 2,8)<br>
# Group 5: 'Real Estate' (1 company at index 9)<br>

# In[4]:


# Group by with multiple columns

print (mp.groupby(['MarketCap','Sector']).groups)


# There are 8 Groups formed, if we group it by <b>'Sector'</b> and <b>'MarketCap'</b>. They are:<br>
# <br>
# Group 1: 'Large Cap, FMCG' (1 company at index 1)<br>
# Group 2: 'Mid Cap, FMCG' (1 company at index 6)<br>
# Group 3: 'Large Cap, IT' (1 company at index 0)<br>
# Group 4: 'Small Cap, FMCG' (1 company at index 5)<br>
# Group 5: 'Mid Cap, Real Estate' (1 company at index 9)<br>
# Group 6: 'Small Cap, IT' (1 company at index 7)<br>
# Group 7: 'Mid Cap, Pharma' (2 companies at index 3,4)<br>
# Group 8: 'Mid Cap, Finance' (1 company at index 2)<br>

# ### Iterating through groups

# In[6]:


# A better way to visualise

grouped = mp.groupby('Sector')

for name,group in grouped: 
    print (name)
    print (group)


# In[7]:


# Just so that you feel comfortable, go through this line of code too

grouped = mp.groupby('MarketCap')

for name,group in grouped:  # We will learn 'for' loop in further sections. It is usually used for iterations 
    print (name)
    print (group)


# ### Select a group

# In[9]:


import pandas as pd

my_portfolio = {'Sector': ['IT', 'FMCG', 'Finance', 'Pharma', 'Pharma',
                          'FMCG', 'FMCG', 'IT', 'Finance', 'Real Estate'],
            
            'Company':   ['Infosys', 'Dabur', 'DHFL', 'Divis Lab', 'Lupin',
                         'Ruchira Papers', 'Britianna','Persistent Systems','Bajaj Finance', 'DLF'],
            
            'MarketCap': ['Large Cap','Large Cap','Mid Cap','Mid Cap','Mid Cap',
                         'Small Cap','Mid Cap','Small Cap','Large Cap','Mid Cap'],
            
            'Share Price': [1120,341,610,1123,741,185,5351,720,1937,217],
                
            'Amount Invested': [24000,16000,50000,23000,45000,12000,52000,18000,5000,3500]}

mp = pd.DataFrame(my_portfolio)

grouped = mp.groupby('MarketCap')

print (grouped.get_group('Mid Cap'))


# ### Aggregations

# In[10]:


import numpy as np

grouped = mp.groupby('MarketCap')

print (grouped['Amount Invested'].agg(np.mean))


# What does this mean?<br>
# <br>
# This means that on an average, we have invested Rs. 15000 per script in Large Cap, Rs. 34700 per script in Mid Cap and Rs. 15000 per script in Small Cap

# In[11]:


grouped = mp.groupby('MarketCap')

print (grouped.agg(np.size))


# What does this mean? <br>
# 
# This just shows the size of the group.

# In[12]:


# Applying multiple aggregation functions at once

grouped = mp.groupby('MarketCap')

print (grouped['Amount Invested'].agg([np.sum, np.mean]))


# What does this mean? <br>
# <br>
# This means that the 'total amount' invested in a particular sector is the 'sum' and 'average amount per script' invested in that sector is the 'mean' value.

# ### Transformations

# In[13]:


import pandas as pd

my_portfolio = {'Sector': ['IT', 'FMCG', 'Finance', 'Pharma', 'Pharma',
                          'FMCG', 'FMCG', 'IT', 'Finance', 'Real Estate'],
            
            'Company':   ['Infosys', 'Dabur', 'DHFL', 'Divis Lab', 'Lupin',
                         'Ruchira Papers', 'Britianna','Persistent Systems','Bajaj Finance', 'DLF'],
            
            'MarketCap': ['Large Cap','Large Cap','Mid Cap','Mid Cap','Mid Cap',
                         'Small Cap','Mid Cap','Small Cap','Large Cap','Mid Cap'],
            
            'Share Price': [1120,341,610,1123,741,185,5351,720,1937,217],
                
            'Amount Invested': [24000,16000,50000,23000,45000,12000,52000,18000,5000,3500]}

mp = pd.DataFrame(my_portfolio)

print (mp)

grouped = mp.groupby('MarketCap')

z_score = lambda x: (x - x.mean()) / x.std()

print (grouped.transform(z_score))


# ### Filteration

# In[14]:


print (mp.groupby('MarketCap').filter(lambda x: len(x)>= 3))


# What does this mean?<br>
# <br>
# It will not filter the Groups that has 3 or less than 3 companies in that particular group. 

# ### Merging/Joining 

# In[15]:


import pandas as pd


left_df = pd.DataFrame({
         'id':[1,2,3,4,5],
         'Company': ['Infosys', 'SBI', 'Asian Paints', 'Maruti', 'Sun Pharma'],
         'Sector':['IT','Banks','Paints and Varnishes','Auto','Pharma']})

right_df = pd.DataFrame(
         {'id':[1,2,3,4,5],
         'Company': ['NTPC', 'TCS', 'Lupin', 'ICICI', 'M&M'],
         'Sector':['Power','IT','Pharma','Banks','Auto']})


# In[16]:


left_df


# In[17]:


right_df


# In[18]:


# Merge 2 DF on a key

print (pd.merge(left_df,right_df, on='id'))


# In[19]:


print (pd.merge(left_df,right_df, on='Sector'))


# In[20]:


# Merge 2 DFs on multiple keys

print (pd.merge(left_df,right_df,on=['Sector','Company']))


# In[21]:


# Merge using 'how' argument

# Left join

print (pd.merge(left_df, right_df, on='Sector', how='left'))


# In[22]:


# Right join

print (pd.merge(left_df, right_df, how='outer', on='Sector'))


# In[23]:


# Outer Join

print (pd.merge(left_df, right_df, how='outer', on='Sector'))


# In[24]:


# Inner Join

print (pd.merge(left_df, right_df, on='Sector', how='inner'))


# ### Concatenation

# In[25]:


print (pd.concat([left_df,right_df]))


# In[26]:


print (pd.concat([left_df, right_df],keys=['x','y']))


# In[27]:


print (pd.concat([left_df,right_df],keys=['x','y'],ignore_index=True))


# In[28]:


print (pd.concat([left_df,right_df],axis=1))


# In[29]:


# Concatenating using append

print (left_df.append(right_df))


# In[30]:


print (left_df.append([right_df,left_df, right_df]))

