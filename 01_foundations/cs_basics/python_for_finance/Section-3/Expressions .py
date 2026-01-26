
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## Expressions
# 
# 'Expressions' are generally a combination of numbers, variables and operators. <br>
# <br>
# In this iPython notebook, we will make use of Expressions to understand the TVM concepts. 

# ### Future Value (FV)
# 
# What would be the FV, if I have $1000 with me now and I will be investing it for 1 year, at an annual return of 5%? 

# In[52]:


PV = 1000
r = 0.05
n = 1

FV = PV * ((1+r) ** n) # Formula for calculating Future Value

print (FV)


# ### Present Value
# 
# What would be the PV, if I have to discount $1050 at 5% annual rate for a period of 1 year?

# In[53]:


FV = 1050
r = 0.05
n = 1

PV = FV / ((1 + r) ** n) # Formula for calculating Present Value

print (PV)


# ### Compounding 
# 
# Assume that the 5% annual interest rate bond makes semiannual payments. That is, for an investment of $1000, you will get 25 dollars, after first 6 months and another 25 dollars after 1 year. The annual rate of interest is 5%. What would be the FV, if I hold the bond for 1 year? 

# In[54]:


PV = 1000
r = 0.05
n = 2 # number of periods = 2 since bond makes semiannual payments
t = 1 # number of years

FV = PV * ((1+(r/n)) ** (n*t)) # Formula for compounding

print (FV)


# ### Annuity Payments
# 
# What would be the annual periodic saving amount, if you want a lumsum of $9476.96 at the end of 3 years? The rate of return is 10%? <br>
# <br>
# (This is one of the required calculation from 'PDF : TVM Applications' unit) 

# In[55]:


r = 0.1
n = 3
PV = 0
FV = 9476.96

AP = (FV * r) / (((1 + r) ** n) - 1) # Formula for Annuity payments, given Future Value

print (AP)


# What would be the PV, given a cash outfolw of $2500 for a period of 5 years and rate of return being 10%?<br>
# <br>
# (This is one of the required calculation from 'PDF : TVM Applications' unit) 

# In[56]:


r = 0.1
n = 5
AP = 2500

PV = (AP * (1 - ((1 + r) ** -n))) / r # Formula for PV, given Annuity payments

print (PV)


# What would be the PV, given a cash outflow of $30,000 for a period of 45 years and rate of return being 8%?<br>
# <br>
# (This is one of the required calculation from 'PDF : TVM Applications' unit) 

# In[57]:


r = 0.08
n = 45
AP1 = 30000

PV = (AP1 * (1 - ((1 + r) ** -n))) / r # Formula for PV, given Annuity payments

print (PV)


# What would be the annual saving amount (AP), if you want to save a lumpsum of $363252.045 in 25 years and rate of return being 15%?<br>
# <br>
# (This is one of the required calculation from 'PDF : TVM Applications' unit) 

# In[58]:


r = 0.15
n = 25
PV = 0
FV = 363252.045095

AP = (FV * r) / (((1 + r) ** n) - 1) # Formula to calculate Annuity Payments, given FV

#AP = (r * PV) / (1 - ((1 + r) ** -n)) # Formula to calculate Annuity Payments, given PV

print (AP)


# These are some ways, one can use Expressions. <br>
# 
# ### Stay tuned for more on python.
