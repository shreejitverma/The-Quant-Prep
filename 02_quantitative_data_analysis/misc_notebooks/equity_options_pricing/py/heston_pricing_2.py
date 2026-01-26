#!/usr/bin/env python
# coding: utf-8

# <img alt = 'code-more' src = 'img/img.png'>
# 
# <h1><center>EQUITY OPTIONS PRICING 2</center></h1>
# 
# <h2><center>Heston Model: Calibration</center></h2>
# 
# In the previous [section](https://github.com/CalebMigosi/code-more/blob/main/EquityOptionsPricing/Heston%20Pricing%201.ipynb), we went over the intuition behind the Heston model. 
# 
# **If you already have options quotes and risk free rates from Bloomberg/Reuters/Excel, you can skip directly to the [calibration](#Define-objective-function) section.**
# 
# 
# <h3><center>Table of Contents</center></h3>
# 
# 1. [Recap](#Recap)
# 2. [Intuition behind calibrating](#Why-Even-Calibrate?)
# 3. [Webscrapping option prices](#Webscrapping-for-option-quotes)
# 4. [Webscrapping risk free rates](#Webscrapping-for-rates)
# 5. [Define the objective function to minimize](#Define-objective-function)
# 6. [Annex](#Annex)
#     - [Local vs Global Minima](#Local-vs-Global-Minima)
#     - [Smith wilson Implementation](#Smith-Wilson-Implementation)
# 
# <h4>Recap</h4>
# As a recap, we showed how to implement this formula:
# 
# <br>
# <br>
# $$C = \frac{1}{2}(S_t - Ke^{-r(T-t)}) + \frac{1}{\pi} \int_0^{\infty}Re\left[ e^{r(T-t)}\frac{f(s-i)}{is. K^{is}} - K\frac{f(s)}{is. K^{is}}\right] ds$$
# <br>
# <br>
# $$where:$$
# <br>
# <br>
# $$f(x) = e^{ixrT}S_t^{ix} \left(\frac{1 - g.e^{d.\tau}}{1 - g}\right)^{\frac{-2\kappa \theta}{\sigma^2}} \times 
# exp{\left[\frac{\tau\kappa \theta}{\sigma^2} (\kappa - \kappa\rho.i.x- d) + \frac{\nu}{\sigma^2} (\kappa - \kappa\rho.i.x- d) \frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}}\right]}$$
# <br>
# <br>
# $$and$$
# <br>
# <br>
# $$d = \sqrt{(\rho.\sigma.i.x)^2 - \sigma^2.(2.i.x - x^2)}$$
# $$g = \frac{\kappa - \rho.\sigma.i.x + d}{\kappa - \rho.\sigma.i.x - d}$$
# 
# Our resulting code was:

# In[68]:


import numpy as np

# Parallel computation using numba
from numba import jit, njit, prange, float64,complex64
from numba import cuda

i = complex(0,1)


# To be used in the Heston pricer
@jit
def fHeston(s, St, K, r, T, sigma, kappa, theta, volvol, rho):
    # To be used a lot
    prod = rho * sigma *i *s 
    
    # Calculate d
    d1 = (prod - kappa)**2
    d2 = (sigma**2) * (i*s + s**2)
    d = np.sqrt(d1 + d2)
    
    # Calculate g
    g1 = kappa - prod - d
    g2 = kappa - prod + d
    g = g1/g2
    
    # Calculate first exponential
    exp1 = np.exp(np.log(St) * i *s) * np.exp(i * s* r* T)
    exp2 = 1 - g * np.exp(-d *T)
    exp3 = 1- g
    mainExp1 = exp1 * np.power(exp2/ exp3, -2 * theta * kappa/(sigma **2))
    
    # Calculate second exponential
    exp4 = theta * kappa * T/(sigma **2)
    exp5 = volvol/(sigma **2)
    exp6 = (1 - np.exp(-d * T))/(1 - g * np.exp(-d * T))
    mainExp2 = np.exp((exp4 * g1) + (exp5 *g1 * exp6))
    
    return (mainExp1 * mainExp2)

# Heston Pricer (allow for parallel processing with numba)
@jit(forceobj=True)
def priceHestonMid(St, K, r, T, sigma, kappa, theta, volvol, rho):
    P, iterations, maxNumber = 0,1000,100
    ds = maxNumber/iterations
    
    element1 = 0.5 * (St - K * np.exp(-r * T))
    
    # Calculate the complex integral
    # Using j instead of i to avoid confusion
    for j in prange(1, iterations):
        s1 = ds * (2*j + 1)/2
        s2 = s1 - i
        
        numerator1 = fHeston(s2,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator2 = K * fHeston(s1,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        denominator = np.exp(np.log(K) * i * s1) *i *s1
        
        P = P + ds *(numerator1 - numerator2)/denominator
    
    element2 = P/np.pi
    
    return np.real((element1 + element2))


# 
# <h3><center>Why Even Calibrate?</center></h3>
# 
# The full pricing model is a bit of a handful but breaking it down, we got a pretty neat function that we could use to price our options.
# 
# However, in practice, we actually don't use the pricer to calculate prices. What we do is try to obtain the parameters for the Heston model based on the prices we observe in the markets.
# 
# That way, we know, using our parameters, if a derivative is being priced differently by the market from what we would expect. In the same way that traders look at implicit volatility, we use the heston parameters to give us an indication of market expectations in the options markets.
# 
# Another, maybe more common, use of these parameters is in pricing complex/exotic options. For very complex options, we can't really find a true market price. What we do in this case is use the plain vanilla options to find parameters of the Heston model and use the parameters we obtain from the market to calculate the price of the exotic options using Monte Carlo.
# 
# The objective of this document is to show exactly how this is done.
# 
# 

# <h3><center> Calibration process: Intuition </center></h3>
# 
# When calibrating you have to consider that you have options with different maturities and expiries. You want to have one set of parameters for the entire set of options or at the very least, have one for the most important regions of the set of options.
# 
# Because this set is essentially a grid, we call it a surface because it's essentially a table of option prices for each maturity and strike price available.
# 
# You want to have a set of parameters to cover a section of the surface for coherence sake. If you are calculating sensitivities e.g. delta, vega, gamma. You want these to mean the same thing for all the options concerned. 
# 
# If you have a model for each point, you can't aggregate sensitivities because it's basically an apples to oranges comparison.
# 
# So what we do is start with a set of parameters, say $\{\sigma = 0.1, \kappa = 0.1, \theta = 0.1, \rho = 0.1, \nu = 0.1\}$. We calculate the Heston price for all our options and find the squared error between the market prices and the prces we obtained from our Heston.
# 
# We then use a solver to reduce this error to 0. So this can actually be done on Excel. It'll take a bit of time but it can be done.
# 
# Then using out optimal parameters we can price our options using the Monte Carlo Method.

# <h3><center> Enough Talking, Let's calibrate</center></h3>
# 
# We start off by defining our workflow. This will depend on whether you can get quotes from a valid source.
# 
# <h4><center>Workflow</center></h4>
#     
# 1. Obtain options quotes and construct the surface (webscrapping or data API eg Bloomberg/Reuters)
# 2. Obtain risk free rates (USSW for US or EONIA/EIOPA Curves for Europe)
# 3. Create a vector function to calculate the prices of all the options on our surface
# 4. Minimize the square error between all the prices calculated using our model & the market prices
# 
# First thing is to get option quotes. You can get these on Bloomberg if you have the terminal or scrape them from the web. I've done a section on this on my [webscrapping repository on Github](https://github.com/CalebMigosi/code-more/tree/main/WebScrapping). 
# 
# You can test it out to get option quotes from the internet.
# 
# I'll do a quick sample here.

# <h3><center>Webscrapping for option quotes</center></h3>
# 
# Options quotes typically don't go out very long into the future. This is essentially because it would be very difficult to say where markets will be in the next 10 years for example.
# 
# On the other hand, with bonds, options on fixed income products do tend to go out very long into the future because of the maturities of bonds which can go as long as infinity (perpetuity bonds.)
# 
# **Note**
# 
# **We're only webscrapping because this is a private project. For work purposes, and with access to Bloomberg/Reuters, this should be a very quick set-up.**
# 

# In[79]:


from bs4 import BeautifulSoup
import requests
import re
import time 
import pandas as pd
import os
from datetime import datetime as dt
import time
import itertools 

# Selenium Related packages
###############################
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Nelson Siegel Svensson (pip install )
from nelson_siegel_svensson.calibrate import calibrate_ns_ols

# Optimizer
from lmfit import Parameters, minimize
from scipy.optimize import dual_annealing

# Plots
import plotly.graph_objects as go
import chart_studio.plotly as py
import plotly.express as px


# In[3]:


# We're using the barchart page to extract options quotes
url = 'https://www.barchart.com/stocks/quotes/$SPX/options'

# On ubuntu: sudo apt-get install chromium-chromedriver
# Connect to driver using Python
# Setting up options for WebDriver
driver = webdriver.Chrome()

## Direct to Home Page
driver.get(url)

time.sleep(2)
# Accept terms and conditions
driver.find_elements_by_xpath("//*[contains(text(), 'Accept all')]")[0].click()

# We want to obtain all quotes
rows = Select(driver.find_element_by_xpath("//select[@name = 'moneyness']"))
rows.select_by_value('inTheMoney')

# Select a date on the options market
quotes = Select(driver.find_element_by_xpath("//select[@data-event-name = 'onExpirationDateChanged']"))

# Find the number of elements we want to get
quoteSize = len(quotes.options)

surface =  []
dateIndex = []
# Extract all the closing prices for each maturity date available
# Re-adding the quote click to the loop prevents expiry of elements in the loop
for i in range(quoteSize):
    # Ignore quotes we can't find
    try:
        quotes = Select(driver.find_element_by_xpath("//select[@data-event-name = 'onExpirationDateChanged']"))
        option = quotes.options[i]
        option.click()

        # Wait for page to load
        time.sleep(5)

        # Find the tables in our page (We should get the Call and put tables)
        tableDiv = option.find_elements_by_xpath("//div[@class = 'bc-table-scrollable-inner']")[0]

        # We want the first table(Call quotes)
        callQuotes = tableDiv.find_elements_by_xpath("//tbody")[0]
        callQuotes = callQuotes.find_elements_by_xpath("//tr[@sly-repeat = 'row in rows.data']")

        # We want to obtain all the quotes from each row
        regex = '[0-9,.]{2,}'
        quotes = [re.findall(regex, elem.text) for elem in callQuotes]

        # Strikes are the first elements, mid quotes are the 5th element
        strikes = [float(re.sub(',','', quote[0])) for quote in quotes]
        midQuotes = [float(re.sub(',','', quote[3])) for quote in quotes]

        # Construct the dataframe
        date = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', option.text).group()
        date = dt.strptime(date, '%Y-%m-%d')

        # Create the date 
        surface.append(midQuotes)
        dateIndex.append(date)

    except Exception:
        pass


# <br>
# <br>
# <br>
# <br>
# 
# Using the quotes we obtained from webscrapping, we create a surface with each $\{maturity, strike\}$ couple containing a price. This grid will be instrumental in observing areas where our calibration did not perform as well as we would have wanted it to.

# In[4]:


# Construct a full volatility surface
maturities = [(date - dt.today()).days/365.25  for date in dateIndex]
volSurface = pd.DataFrame(surface, index = maturities, columns = strikes)
volSurface = volSurface[volSurface.index > 0.1]
volSurface


# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <h3><center>Webscrapping for rates</center></h3>
# 
# We obtain the rates that we'll use to calculate the option prices. To do this, we use the treasury rates from this website. Again, this would be easier with some adjustments to the swap rates(EUSA or USSW in Bloomberg.)
# 
# We then apply an interpolation method to obtain our interest rate curve. This will be important to find the rate corresponding to each maturity.
# 
# To do this interpolation, we'll use the Nelson Siegel Svensson method. This is one of the most common methods of interpolating a curve. For actuarial purposes in Europe, however, the Smith Wilson interpolation is used. 
# 
# I'll implement the Smith Wilson as it's used in insurance at the end of the script.

# In[5]:


ratesUrl = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'

## Direct to Home Page
driver.get(ratesUrl)

time.sleep(2)

# Find the table of rates
rows = driver.find_elements_by_xpath("//tr")

# Extract the last line (the latest possible rate)
rates = [elem.text for elem in rows[len(rows)-1].find_elements_by_xpath("//td[@class = 'text_view_data']")]

# End the chromium driver
driver.close()

# Convert the rates we obtained to float. 
# Also convert to a numpy array - this is the input format for the NSS
rates = np.array(rates[-12:]).astype(float)/100
maturities = np.array([1/12, 2/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30])

# Apply the nelson siegel svennson model
curve, status = calibrate_ns_ols(maturities, rates)


# <br>
# <br>
# We can have a quick view of the shape of the curve before moving forward

# In[6]:



# Plot the graph to visualize the shape
mats = np.linspace(0.05, 20, 101)
rates = curve(mats)
fig = go.Figure(go.Scatter(x= mats, y = rates, line = dict(color='#ffc93c', width=2.5)))
fig.update_layout(
    font_color="#0f4c75",
    title_text='Interpolated Rate Curve', 
    title_x=0.5,
)
fig.update_xaxes(title="Maturities")
fig.update_yaxes(title="Rates")
fig.update_layout(plot_bgcolor='#0f4c75')
fig.update_layout(plot_bgcolor='#0f4c75')
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)


# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# 
# <h3><center>Define objective function</center></h3>
# 
# We begin by initializing our parameters. We use these initial parameters to test our whether our heston pricer is coherent.

# In[7]:


#Initialize parameters
sigma, kappa, theta, volvol, rho = 0.1, 0.1, 0.1, 0.1, 0.1

# Convert our vol surface to long to allow for a vectorized Heston pricing function
volSurfaceLong = volSurface.melt(ignore_index = False).reset_index()
volSurfaceLong.columns = ['maturity', 'strike', 'price']

# Calculate the risk free rate for each maturity
volSurfaceLong['rate'] = volSurfaceLong['maturity'].apply(curve)
volSurfaceLong

# Define global variables to be used in optimization
maturities = volSurfaceLong['maturity'].to_numpy('float')
strikes = volSurfaceLong['strike'].to_numpy('float')
marketPrices = volSurfaceLong['price'].to_numpy('float')
rates = volSurfaceLong['rate'].to_numpy('float')


# <h4><center>Create a vectorized Heston function</center></h4>
# 
# This essentially means that we want our function to calculate options prices for different maturities and strikes at the same time. This will allow us to run optimized code which will be needed in the optimization process.

# <h4><center>Create an error function between HestonVect and the true market prices</center></h4>
# 
# Another simple function that should give us a vector of differences between the prices we obtained in our model and those quoted in the market.
# 
# When we fit our optimization algorithm, these errors will be squared and summed on each iteration. This is how the algorithm is able to continue minimizing the error until an optimal solution is found.

# In[81]:


# Can be used for debugging
# def iter_cb(params, iter, resid):
#     parameters = [params['sigma'].value, 
#                   params['kappa'].value, 
#                   params['theta'].value, 
#                   params['volvol'].value, 
#                   params['rho'].value, 
#                   np.sum(np.square(resid))]
#     print(parameters) 
    
# This is the calibration function
def calibratorHeston(St, initialValues = [0.5,0.5,0.5,0.5,-0.5], 
                              lowerBounds = [1e-2,1e-2,1e-2,1e-2,-1], 
                              upperBounds = [10,10,10,10,0]):
    '''Implementation of the Levenberg Marquardt algorithm in Python to find the optimal value 
        based on a given volatility surface.
        
        Function to be minimized:
            Error = (MarketPrices - ModelPrices)/MarketPrices
        
        INPUTS
        ===========
        1) Volatility Surface
            - Obtained from webscrapping. 
        
        2) Risk Free Curve
            - Obtained from webscrapping. 
            
        3) initialValues
            - Initialization values for the algorithms in this order:
                [sigma, kappa, theta, volvol, rho]
                
            - Default value: [0.1,0.1,0.1,0.1,0.1]
            
        4) lowerBounds
            -Fix lower limit for the values
            - Default value: [0.001,0.001,0.001,0.001,-1.00]
            
        5) upperBounds
            -Fix upper limit for the values
            - Default value: [1.0,1.0,1.0,1.0,1.0]
            
        6) St is the stock price today.
    
    Set Up
    =======
    1) We define the limits of the parameters using the Parameters object
    2) We define an objective function that gives the relative difference between market prices and model prices
    3) We minimize the function using the Levenberg Marquardt algorithm
    '''
        
    '''1) Define parameters
    =========================='''
    params = Parameters()
    params.add('sigma',value = initialValues[0], min = lowerBounds[0], max = upperBounds[0])
    params.add('kappa',value = initialValues[1], min = lowerBounds[1], max = upperBounds[1])
    params.add('theta',value = initialValues[2], min = lowerBounds[2], max = upperBounds[2])
    params.add('volvol', value = initialValues[3], min = lowerBounds[3], max = upperBounds[3])
    params.add('rho', value = initialValues[4], min = lowerBounds[4], max = upperBounds[4])
    
    
    '''2) Define objective function
    ================================'''
    objectiveFunctionHeston = lambda paramVect: (marketPrices - priceHestonMid(St, strikes,  
                                                                        rates, 
                                                                        maturities, 
                                                                        paramVect['sigma'].value,                         
                                                                        paramVect['kappa'].value,
                                                                        paramVect['theta'].value,
                                                                        paramVect['volvol'].value,
                                                                        paramVect['rho'].value))/marketPrices   
    
    '''3) Optimize parameters
    =============================='''
    result = minimize(objectiveFunctionHeston, 
                      params, 
                      method = 'leastsq',
#                     iter_cb = iter_cb,
                      ftol = 1e-6)
    return(result)

# Note: Only for demonstration purposes.
# This calibration takes a while because the option surface contains 1000 points (About 30minutes)
# Either reduce the number of options or implement an approximation
# Best approximation: https://econ-papers.upf.edu/papers/1346.pdf
calibratorHeston(3950)


# In[80]:


# Extract errors
Errors = - (marketPrices - priceHestonMid(3950, strikes, rates, maturities, 0.99999848,0.04,0.99730087,0.03708778,1))/marketPrices

# Construct dataframe of errors/strikes/maturities
errorDF = pd.DataFrame({'Errors': np.absolute(Errors),
            'Strikes': strikes,
            'Maturities': maturities})

# Convert long to wide
errorDF = errorDF.pivot_table(index = 'Maturities', columns = 'Strikes', values = 'Errors')

# Define columns for plots
x = errorDF.columns.values
y= errorDF.index.values
z = errorDF.values

# Plot figure
fig = px.imshow(z, x=x, y=y, 
          zmax = 0.3,
          height = 500,
          aspect=150,
          color_continuous_scale='Viridis', 
          origin='higher')

fig.update_layout(title_text= "Error color scheme",title_x=0.5)


# In[ ]:





# <h2><center>Annex</center></h2>
# 
# <h3><center>Local vs Global Minima</center></h3>
# What was implemented above is in fact an incomplete solution. Typically, we have to consider local and global minima in our function.
# 
# To get closest to the global minimum, we would have to use a different algorithm other than a gradient dependent one.
# 
# Three algorithms stand out: simulated annealing, swarm optimization and differential evolution. The implementation is essentially the same with different tweaks. We implement one of these models quickly under the same structure.
# 
# In reality, the workflow should involve 2 optimizations as opposed to one. The first should be the global optimization followed by the LM algorithm which is faster and cheaper computation-wise.
# 
# 
# <h4><center>Simulated Annealing</center></h4>
# 
# Annealing generally uses random points around a state to determine whether to evaluate the function at a neighboring point using a probabilistic approach.
# 
# Annealing generally does not find the exact solution but is typically a good approximation. This is why we run the LM Algorithm after to refine the quality of the points we obtain.
# 
# 

# In[76]:


# Annealing calibration function
def calibratorHestonSA(St, lowerBounds = [1e-2,1e-2,1e-2,1e-2,-1], 
                            upperBounds = [10,10,10,10,1]):
    
    # Note the difference in the objective function (sum of squares vs vector of errors)
    objectiveFunctionHeston = lambda paramVect: np.sum(np.square((marketPrices - priceHestonMid(St, strikes,  
                                                                        rates, 
                                                                        maturities, 
                                                                        paramVect[0],                         
                                                                        paramVect[1],
                                                                        paramVect[2],
                                                                        paramVect[3],
                                                                        paramVect[4]))/marketPrices))
    
    # Define the upper and lower bounds
    bounds = list(zip(lowerBounds, upperBounds))
    
    # Minimize the function
    results = dual_annealing(objectiveFunctionHeston, bounds = bounds)
    
    return(results)

calibratorHestonSA(3950)


# 
# <h3><center>Smith Wilson Implementation</center></h3>
#     
# <h4><center>This section might be of interest to actuaries in life insurance. </center></h4>

# In[ ]:


#Simple Smith Wilson Implementation'
'----------------------------------------'
class SmithWilson:
    '''
    Implementation based on: https://www.scor.com/sites/default/files/2017_it_tesidi_laurea_magurean.pdf
    
    Inputs
    ---------
    ZCPrices = Zero coupon curve ie 0.99
    maturities = maturities for each of the ZC prices
    alpha = default parameter in Smith Wilson. Determines the quickness of convergence
    UFR = the theoretical ultimate forward rate (The forward rate we suppose rates converge to)
    '''
    maturities = np.arange(1, 41) #These are the default input maturities
    
    def __init__(self, ZCPrices, maturities = maturities, alpha = 0.134,  UFR = 0.039):
        self.UFR = np.log(1+UFR)
        self.alpha = alpha
        self.maturities = maturities
        self.ZCPrices = ZCPrices
    
    'Define the Wilson Function'
    def wilsonFunction(self, t, uj):
        '''
        Exact same function on wikipedia: https://en.wikipedia.org/wiki/Smith%E2%80%93Wilson_method
        
        Inputs
        -------------
        uj = time to maturity
        t = maturity. This is a specific maturity for a ZC Bond
        '''
        mu = np.exp(- self.UFR*(t+uj))
        maxT = self.alpha * np.maximum(t, uj)
        minT = self.alpha * np.minimum(t, uj)
        
        # We define the Wilson kernel function
        wj = mu * (minT - 0.5 * np.exp(-maxT)*(np.exp(minT) - np.exp(-minT)))
        
        return (wj)
    
    
    
    def wilsonVectorFunction(self, inputMaturities):
        '''
        Calculates a square matrix, calculating the Wilson Function for each maturity on each maturity
        
        Inputs
        ---------------
        inputMaturities = vector of maturities we input
        '''
        wilsonMatrix = np.zeros((len(inputMaturities), len(self.maturities))) 
        for t in inputMaturities:
            for j in self.maturities:
                wilsonMatrix[t-1, j-1] = self.wilsonFunction(t, j)
            
        return(wilsonMatrix)
    
    
    
    'Obtain the parameter vector zeta'
    def calibrate(self):
        #Create the matrix W of Kernels
        self.WMatrix = self.wilsonVectorFunction(self.maturities)
                
        #Invert the matrix
        #Recall that our parameters are W^-1 * (ZCPrices - muVector)
        WMatrixInv = np.linalg.inv(self.WMatrix) # Invert the kernel
        muVector = np.exp(-self.UFR * self.maturities)
        
        SWParams = WMatrixInv.dot(self.ZCPrices  - muVector) # zeta = W(inverse) * (ZCprice - mu)
        
        return (SWParams)
    
    'Fit Curve'
    def curve(self):
        params = self.calibrate() #Obtain parameters
        parametrizedWilson = self.wilsonVectorFunction(np.arange(1, 151)).dot(params) # Fit full EIOPA Curve
        result = np.exp(-self.UFR * np.arange(1, 151)) + parametrizedWilson
                    
        return(result)


# <img alt = 'code-more' src = 'img/img.png'>
