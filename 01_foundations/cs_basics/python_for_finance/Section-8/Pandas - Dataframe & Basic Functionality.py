
# coding: utf-8

# ### <span style="color:brown">Notebook Instructions</span>
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# # Notebook Contents
# 
# ##### <span style="color:green">1. Creating Data Frames </span>
# ##### <span style="color:green">2. Customizing index of a Data Frame</span>
# #####  <span style="color:green">3. Rearranging the order of columns in a Data Frame</span>
# ##### <span style="color:green">4. Existing Column as the index of the Data Frame</span>
# ##### <span style="color:green">5. Accessing column from a Data Frame</span>
# ##### <span style="color:green">6. Loading and viewing Data in a Data Frame</span>
# ##### <span style="color:green">7. Dropping Rows and Columns from a Data Frame</span>
# ##### <span style="color:green">8. Renaming columns of a Data Frame</span>
# ##### <span style="color:green">9. Sorting a Data Frame using a column</span>
# ##### <span style="color:green">10. Just for Fun</span>

# ## Creating Data Frames 
# 
# The underlying idea of a Data Frame is based on 'spreadsheets'. In other words, data frames stores data in discrete Rows and Columns where each column can be named (something that is not possible in Arrays but is possible in Series). There are also multiple columns in a Data Frame (as opposed to Series, where there can be only one discrete indexed column).<br>
# <br>
# The constructor for a Data Frame is <font color=red>pandas.DataFrame(data=None, index=None)</font> or if you are using 'pd' as alias, then it would be <font color=red>pd.Series()</font><br>
# <br>
# Let us have a look at the following example

# In[18]:


import pandas as pd
import numpy as np

# A DataFrame has a row and column index; it's like a dict of Series with a common index.

my_portfolio = {
                "stock_name": ["Alphabet", "Facebook", "Apple", "Tesla", "Infosys"],
                "quantity_owned": [1564, 6546, 5464, 6513, 4155],
                "average_buy_price": ["$950", "$160", "$120", "$270", "$15"]
               }

my_portfolio_frame = pd.DataFrame (my_portfolio) # We have passed the 'data' argument in the Data Frame constructor

my_portfolio_frame


# ## Customizing index of a Data Frame 
# 
# In the above output, you can see that the 'index' is the default one which starts from 0,1,...4. One can even customize the index for a better understanding of the Data Frame, while working with it.

# In[19]:


ordinals = ["first", "second", "third", "fourth", "fifth"] # list

my_portfolio_frame = pd.DataFrame (my_portfolio, index=ordinals) #Please notice that we have not kept index as default i.e.'none'

my_portfolio_frame


# ## Rearranging the order of columns in a Data Frame 
# 
# We can also define or rearrange the order of columns.

# In[20]:


# please observe the 'columns' names parameter while constructing the Data Frame

my_portfolio_frame = pd.DataFrame(my_portfolio, columns=["stock_name", "quantity_owned", "average_buy_price"], index=ordinals)

my_portfolio_frame


# ## Existing Column as the index of dataframe
# 
# If we want to create a more useful index of our existing Data Frame, we can do that using the column 'stock name' as our index. It will make more sense than the 'ordinals' index. 

# In[21]:


my_portfolio_frame = pd.DataFrame (my_portfolio, 
                                   columns = ["quantity_owned","average_buy_price"],
                                   index = my_portfolio ["stock_name"])

my_portfolio_frame


# ## Accessing column from a data frame 
# 
# It is even possible to just veiw one single or selective columns of the entire data frame.

# In[22]:


# The index at present is the 'stock_name'. Refer to above code. 

# This makes sense if we just want to know the quantity of stock that we own for each stock (which is our index, currently)

print (my_portfolio_frame["quantity_owned"])


# ## Loading and viewing data in a Data Frame 
# 
# This is something that we have seen in the 'Data Visualisation' section of this course. We can even import data from online sources and view them as data frames or we can take a local 'csv' file of a stock data and view them as data frame.
# 
# 

# In[23]:


# Loading and viewing data

# We have stored a 'infy_data.csv' on our desktop

import numpy as np
import pandas as pd

infy = pd.read_csv ('C:/Users/academy/Desktop/infy_data.csv') 


# In[24]:


infy # this is our entire "Infosys" stock data frame


# In[25]:


infy.shape


# In[26]:


infy.head () # You will see the top 5 rows


# In[27]:


infy.tail () # You will see the bottom 5 rows


# ## Dropping Rows and Columns from a Data Frame 
# 
# In the above Infosys stock data, it is not necessary that you need all the columns which are present in the .csv file. Hence, to make your data frame more understandable, you may drop the columns that you do not need using drop function. 

# In[28]:


# The axis=1 represents that we are considering columns while dropping.

infy_new = infy.drop (['Prev Close', 'Last Price', 'Average Price', 'Total Traded Quantity',
                       'Turnover', 'No. of Trades', 'Symbol','Series'], axis = 1)

infy_new.head ()


# In[29]:


#V15 video (I have to delete this)

# Sorting a data frame

infy_new = infy_new.sort_values(by="Close Price", ascending=False)

print(infy_new)


# In[30]:


# Dropping rows: 31 March2016, 01 April 2016

infy_new.drop (infy_new.index [[3,4]] )


# ## Renaming Columns of a Data Frame 
# 
# If we want to rename the column names according to our wish, for better understanding while dealing with the data frame, we can also in python. 

# In[31]:


# Renaming Columns: Have a quick look at the code, It should be self-explanatory by now

infy_new=infy_new.rename(columns={'Date':'Date','Open Price':'Open','High Price':'High','Low Price':'Low','Close Price':'Close'})

infy_new.head()


# ## Sorting a Data Frame using a column 
# 
# Sometimes it becomes necessary to sort a stock price data frame, based on the 'Closing Price'.

# In[32]:


# Sorting Dataframe

infy_new = infy_new.sort_values(by="Close", ascending=False)

print(infy_new)


# ## Just for Fun 

# In[33]:


# If at all you want to practice, on a customised data frame, just fill it with random values and go ahead

import numpy as np
names = ['Jay', 'Varun', 'Devang', 'Ishan', 'Vibhu']

months = ["January", "February", "March",
         "April", "May", "June",
         "July", "August", "September",
         "October", "November", "December"]

df = pd.DataFrame(np.random.randn (12, 5)*10000, columns = names, index = months)

df


# ### <span style="color:green">In the upcoming iPython Notebook:</span> <br>
# We will understand Statistics and Statistical Functions on a Data Frame.
# 
