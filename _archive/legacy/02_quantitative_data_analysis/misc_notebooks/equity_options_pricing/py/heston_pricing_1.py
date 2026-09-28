#!/usr/bin/env python
# coding: utf-8

# <img alt = 'code-more' src = 'img/img.png'>
#
# <h1><center>EQUITY OPTIONS PRICING 1</center></h1>
# <h2><center>Heston Model</center></h2>
#
# In this document we review one of the most common options pricing models in equity pricing: the Heston Model. We want to try and **get the intuition** behind the model **so that we can implement and use it**. The derivation is less important to us in this document.
#
# We also provide the base pricing formula and the different problems that could occur while pricing with the Heston model.
#
# <h3>Workflow</h3>
#
# 1. Black Scholes Model
#
# 2. Black Scholes to Heston
#
# 3. Defining characteristic functions
#
# 4. Implementation in Python
#
#
# **Note**
#
# Note that this model is not the base market standard for options pricing. But it's a good intro if you want to get into the financial markets with a bare minimum level of math.
#
# **You only need to know about probability distributions and integrals.** The rest is just adjustments to what you already know.
#
# <h3>TLDR</h3>
#
# **We're going to find the intuition behind the Heston Pricing function and implement it on Python. No derivation, just intuition.**
#
# So you'll first have to see where we're going to get a bird's eye view before we venture into the details. The formula seems daunting but in a few steps, we'll show you that it's not really that far from the Black & Scholes model in practice.
#
# Our example is just a simple call option. Lets say you have a european option expiring in 2 years with a strike at 100 and the price of the stock (say Apple) is at 110 today. You'd expect the value of the option to be about 10. We also just assume that the risk free interest rate is 5%.
#
# In a more general case, we could do this:
# We define:
# - $C$ as the value of the call option
# - $S_t$ the stock price today
# - $K$ the strike price
# - $T$ the maturity (therefore $T-t$ is the time to maturity)
# - $r$ the risk free rate
#
# Here we want to find $C$ where $S_t = 110$, $K = 100$, $T = 2$, $t =0$ and $r =0.05$.
#
# Also $S_T$ is the final price which we don't know and $P(S_T>K)$ is the future probability that the stock price is above the strike at maturity.
#
# Then, using Heston parameters: $\sigma, \rho, \nu, \kappa, \theta$, our Heston Pricer is defined as:
# <br>
# <br>
# $$C = S_t . P_1(S_T > K) - Ke^{-rt} . P_2(S_T > K)$$
# <br>
# <br>
# which under the Heston model is:
# <br>
# <br>
# $$C = S_t .\left[\frac{1}{2} + \frac{1}{\pi} \int_0^{\infty} Re\left[\frac{e^{-is \,ln K} f_1(s,\nu, x)}{is}\right]ds\right] - Ke^{-rt}\left[\frac{1}{2} + \frac{1}{\pi} \int_0^{\infty} Re\left[\frac{e^{-is \,ln K} f_2(s,\nu, x)}{is}\right]ds\right]$$
# <br>
# <br>
# where:
# $$f_j(s,\nu, x) = exp(C_j(\tau, s) + D_j(\tau, s).\nu + i.s.x)$$
# <br>
# <br>
# and assuming:
# $$x =ln S_t$$
# <br>
# <br>
# $$d_j = \sqrt{(\rho.\sigma.i.s)^2 - \sigma^2.(2.u_j.i.s - s^2)}$$
# <br>
# <br>
# $$g_j = \frac{b_j - \rho.\sigma.i.s + d_j}{b_j - \rho.\sigma.i.s - d_j}$$
# <br>
# <br>
# $$where: u_1 = 0.5, u_2 = 0.5$$
# $$and: b_1 = \kappa - \rho.\sigma, b_2 = \kappa$$
# <br>
# <br>
# then:
# $$let \,BRS = b_j - \rho.\sigma.i.s + d_j$$
# $$C_j(\tau, s) = r.i.s.\tau + \frac{a}{\sigma^2}\left[ (BRS).\tau - 2 ln \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right)\right]$$
# <br>
# <br>
# $$D_j = \frac{BRS}{\sigma^2} \left(\frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}} \right)$$
#

# <h3><center>Full Code</center></h3>
#
# Here's the full code snippet if you're in a hurry or if you already have the intuition behind the Heston and just want to see an implementation that will help you get started quick.
#
# Also note that I'm implementing a simplified version of the formula above. This is an implementation of [this](#Simplified-(Single-Integral)-Formula) formula.

# In[1]:


import numpy as np

i = complex(0, 1)


# To be used in the Heston pricer
def fHeston(s, St, K, r, T, sigma, kappa, theta, volvol, rho):
    # To be used a lot
    prod = rho * sigma * i * s

    # Calculate d
    d1 = (prod - kappa)**2
    d2 = (sigma**2) * (i * s + s**2)
    d = np.sqrt(d1 + d2)

    # Calculate g
    g1 = kappa - prod - d
    g2 = kappa - prod + d
    g = g1 / g2

    # Calculate first exponential
    exp1 = np.exp(np.log(St) * i * s) * np.exp(i * s * r * T)
    exp2 = 1 - g * np.exp(-d * T)
    exp3 = 1 - g
    mainExp1 = exp1 * np.power(exp2 / exp3, -2 * theta * kappa / (sigma**2))

    # Calculate second exponential
    exp4 = theta * kappa * T / (sigma**2)
    exp5 = volvol / (sigma**2)
    exp6 = (1 - np.exp(-d * T)) / (1 - g * np.exp(-d * T))
    mainExp2 = np.exp((exp4 * g1) + (exp5 * g1 * exp6))

    return (mainExp1 * mainExp2)


# Heston Pricer
def priceHestonMid(St, K, r, T, sigma, kappa, theta, volvol, rho):
    P, iterations, maxNumber = 0, 1000, 100
    ds = maxNumber / iterations

    element1 = 0.5 * (St - K * np.exp(-r * T))

    # Calculate the complex integral
    # Using j instead of i to avoid confusion
    for j in range(1, iterations):
        s1 = ds * (2 * j + 1) / 2
        s2 = s1 - i

        numerator1 = fHeston(s2, St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator2 = K * fHeston(s1, St, K, r, T, sigma, kappa, theta, volvol,
                                 rho)
        denominator = np.exp(np.log(K) * i * s1) * i * s1

        P += ds * (numerator1 - numerator2) / denominator

    element2 = P / np.pi

    return np.real((element1 + element2))


# <h3><center>Introduction: Black Scholes Model</center></h3>
#  We begin by introducing the Black and Scholes pricer and make parallels to the base options pricing model in comparison to the Heston.
#
# We suppose that the stock price today is $S_t$ and the strike of the call option is $K$. We also assume that the stock matures at time $T$ and therefore the time to maturity is $T-t$
#
# Finally, we assume our risk free rate is $r$. Also, we assume that we discount continuously in our model. So we know that our strike $K$ only applies at the time of maturity T.
#
# So the value today of the strike $K$ should be discounted to today for us to find the value of our option today.
#
# We know that the Black and Scholes pricing model gives the following final formula for a call option:
# <br>
# <br>
# $$C = N(d_1)\times S_t - Ke^{-rt} \times N(d_2)$$
#
# $$where:$$
# $$d_1 = \frac{ln \left(\frac{S_t}{K}\right) +  \left( r + \frac{\sigma ^ 2}{2} \right) (T-t)}{\sigma \sqrt{(T-t)}}$$
#
# $$d_2 = d_1 - \sigma t$$
#
# and $N$ is the cumulative distribution function for a normal random variable.
# <br>
# <br>
#
# **Side note: Intuition behind the N function in Black Scholes**
#
# $N()$ is just the NORM.DIST function  in Excel. This function takes the following inputs:
#
#       NORM.DIST(x, mean, standard_dev)
#
# And calculates, for any input x, the area under the bell curve starting from the left.
#
# **Example: Distribution plot provided**
#
# Say we have 0 as the mean and 1 as the standard deviation.
#
# This means that at 0 the area of the graph below starting from the furthest point on the left will be exactly half.
#
# This area represents the probability of a random value selected from a distribution of mean 0 and standard deviation 1 being less than or equal to $x$.
#
# Therefore, the larger the number $x$ the higher the probability that any random number selected will be less than $x$.

# In[6]:


import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy.stats import norm

import warnings
import datapane as dp
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

values = np.linspace(-3, 3, num = 101)
proba = norm.pdf(values)
cdfproba = norm.cdf(values)

fig = make_subplots(rows=1, cols=2,
                    subplot_titles=['Normal distribution (mean 0, stdev 1) - PDF',
                                                    'Area under the curve(from the left) - CDF'])

fig.add_trace(
    go.Scatter(x=values, y=proba, name = 'PDF',line = dict(color='#ffc93c', width=2.5)),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=values, y=cdfproba, name = 'CDF',line=dict(color='#ffc93c', width=2.5)),
    row=1, col=2
)
fig.update_layout(plot_bgcolor='#0f4c75')
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

report = dp.Report(dp.Plot(fig) ) #Create a report
report.publish(name='my_plot', open=True, visibility='PUBLIC') #Publish the report


# In[2]:


import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy.stats import norm

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

values = np.linspace(-3, 3, num = 101)
proba = norm.pdf(values)
cdfproba = norm.cdf(values)

fig = make_subplots(rows=1, cols=2,
                    subplot_titles=['Normal distribution (mean 0, stdev 1) - PDF',
                                                    'Area under the curve(from the left) - CDF'])

fig.add_trace(
    go.Scatter(x=values, y=proba, name = 'PDF',line = dict(color='#ffc93c', width=2.5)),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=values, y=cdfproba, name = 'CDF',line=dict(color='#ffc93c', width=2.5)),
    row=1, col=2
)
fig.update_layout(plot_bgcolor='#0f4c75')
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.show()


# _I encourage you to try this out with a simple option on excel with strike 100 and maturity 2yrs with different stock price levels on Excel. You can verify the prices on this [pricer](https://www.mystockoptions.com/black-scholes.cfm)_

# <br>
# <h3><center>From Black and Scholes to Heston</center></h3>
#
# **Note: Take the functions as is. Implementing the pricer will give more intuition. You can look at the derivation afterwards**
#
# We can observe from the B&S formula that what we have as $N()$ are simply probability functions. In a general set up, we could have different distributions other than the normal.
#
# Also, the two distributions could be different. In a sense, what the B&S formula establishes as a framework is that we can price options using the following blueprint:
#
# $$C = S_t \times P_1(S_T > K) - Ke^{-rt} \times P_2(S_T > K)$$
#
# In the B&S, the $P_1$ and $P_2$ are simply the $N()$ with different inputs.
#
# For the Heston, we introduce a bit more complexity into these $P$ functions. We define $P_1$ and $P_2$ differently. The principle remains the same nonetheless, albeit with quite a leap in complication.
#
# The Heston equity pricing formula is defined as:
#
# $$C = S_t \times P_1(S_T > K) - Ke^{-rt} \times P_2(S_T > K)$$
#
# $$where:$$
#
# $$x = ln S_t$$
#
# $$P_1 = \frac{1}{2} + \frac{1}{\pi} \int_0^{\infty} Re\left[\frac{e^{-is \,ln K} f_1(s,\nu, x)}{is}\right]ds$$
#
# $$P_2 = \frac{1}{2} + \frac{1}{\pi} \int_0^{\infty} Re\left[\frac{e^{-is \,ln K} f_2(s,\nu, x)}{is}\right]ds$$
#
# We note that the functions have the same structure and only differ by the definitions of the functions $f$. We can therefore define $j$ to be either 1 or 2 and have a general function $P_j$. Therefore:
#
# $$P_j = \frac{1}{2} + \frac{1}{\pi} \int_0^{\inf} Re\left[\frac{e^{-is \,ln K} f_j(s,\nu, x)}{is}\right]ds$$
#
# $$for j \in \{1, 2\}$$
#
# **Side Note 1:**
#
# It is important to note that the parameters of the Heston model are: $\rho, \sigma, \nu, \kappa, \theta$. We have an additional parameter $\lambda$ but we set this to 0 so we don't have to worry about it.
#
# These parameters are the equivalent of the $\sigma$ parameter in B&S. What we will do, is write a solver that finds these parameters based on market prices.
#
# Changes in these parameters will tell us if the market is over or underpriced.
#
# **Side Note 2:**
#
# I'm sure you see the $Re$ on the integral. This just means there are complex numbers in the formula. We will deal with these in the implementation of the pricer.
#
# You'll find that in practice, this is very close to the normal integral where you would split the graph into smaller rectangles and calculate the area of the rectangles using the mid-point!
#
#
# <br>
# <br>
# <h3><center>Defining the f functions</center></h3>
#
# The $f$ functions are known as **characteristic functions** Details are provided in the Annex but the important thing to understand is that any probability distribution can be defined as an exponential form of a specific characteristic function.
#
# For probabilities that are difficult to compute, this provides a very convenient way of calculation since we always know that if we have a characteristic function, we can calculate the probability distribution. This is one of the pioneering aspects of the Heston model.
#
# Heston defined these $f$ functions for each $j$ as follows(We use the dot(.) sign for multiplication):
# $$s \,from \, integral \,above$$
# $$x = ln(S_t)$$
# $$\tau =  T- t$$
# <br>
# <br>
# $$f_j(s,\nu, x) = exp(C_j(\tau, s) + D_j(\tau, s).\nu + i.s.x)$$
# <br>
# <br>
# Before defining $C_j$ and $D_j$, we simplify some elements of these functions that will be of use to us. We define two variables: $d_j$ and $g_j$
# <br>
# <br>
# $$d_j = \sqrt{(\rho.\sigma.i.s)^2 - \sigma^2.(2.u_j.i.s - s^2)}$$
# $$g_j = \frac{b_j - \rho.\sigma.i.s + d_j}{b_j - \rho.\sigma.i.s - d_j}$$
# <br>
# <br>
# $$where: u_1 = 0.5, u_2 = 0.5$$
# $$and: b_1 = \kappa - \rho.\sigma, b_2 = \kappa$$
# <br>
# <br>
# **Note: These simple changes make the only difference between the two P functions. That is why it is easier to use the j subscript.**
#
# Finally, we can define our functions. We use $BRS$ as a short form because the expression is used a lot:
# $$let \,BRS = b_j - \rho.\sigma.i.s + d_j$$
# <br>
# <br>
# $$C_j(\tau, s) = r.i.s.\tau + \frac{\kappa  \theta}{\sigma^2}\left[ (BRS).\tau - 2 ln \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right)\right]$$
# <br>
# <br>
# $$D_j = \frac{BRS}{\sigma^2} \left(\frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}} \right)$$

# <br>
# <br>
# <h4><center> Final Formula </center></h4>
#
# Our final formula therefore is:
#
# $$C = S_t . P_1(S_T > K) - Ke^{-rt} . P_2(S_T > K)$$
# <br>
# <br>
# which is just:
# <br>
# <br>
# $$C = S_t .\left[\frac{1}{2} + \frac{1}{\pi} \int_0^{\inf} Re\left[\frac{e^{-is \,ln K} f_1(s,\nu, x)}{is}\right]ds\right] - Ke^{-rt}\left[\frac{1}{2} + \frac{1}{\pi} \int_0^{\inf} Re\left[\frac{e^{-is \,ln K} f_2(s,\nu, x)}{is}\right]ds\right]$$
# <br>
# <br>
# where:
# $$f_j(s,\nu, x) = exp(C_j(\tau, s) + D_j(\tau, s).\nu + i.s.x)$$
# <br>
# <br>
# and assuming:
# <br>
# <br>
# $$d_j = \sqrt{(\rho.\sigma.i.s)^2 - \sigma^2.(2.u_j.i.s - s^2)}$$
# $$g_j = \frac{b_j - \rho.\sigma.i.s + d_j}{b_j - \rho.\sigma.i.s - d_j}$$
# <br>
# <br>
# $$where: u_1 = 0.5, u_2 = 0.5$$
# $$and: b_1 = \kappa - \rho.\sigma, b_2 = \kappa$$
# <br>
# <br>
# then:
# $$let \,BRS = b_j - \rho.\sigma.i.s + d_j$$
# $$C_j(\tau, s) = r.i.s.\tau + \frac{\kappa  \theta}{\sigma^2}\left[ (BRS).\tau - 2 ln \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right)\right]$$
# <br>
# <br>
# $$D_j = \frac{BRS}{\sigma^2} \left(\frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}} \right)$$<br>
# <br>
# <br>
# <br>
# <br>
# <h3><center>Simplified (Single Integral) Formula</center></h3>
#
# It's easier to implement this formula under a single integral. After all, when you're pricing or calibrating an option surface with 100 - 200 options, you want to make sure your calculations are as fast as possible.
#
# In the final section we show how to move from the 2 part formula to the formula below which is much easier to implement:
# <br>
# <br>
# $$C = \frac{1}{2}(S_t - Ke^{-r(T-t)}) + \frac{1}{\pi} \int_0^{\infty}Re\left[ e^{r(T-t)}\frac{f(s-i)}{is. K^{is}} - K\frac{f(s)}{is. K^{is}}\right] ds$$
# <br>
# <br>
# $$where:$$
# <br>
# <br>
# $$f(x) = e^{ixrT}S_t^{ix} \left(\frac{1 - g.e^{d.\tau}}{1 - g}\right)^{\frac{-2\kappa \theta}{\sigma^2}} \times
# exp{\left[\frac{\tau\kappa \theta}{\sigma^2} (\kappa - \sigma\rho.i.x- d) + \frac{\nu}{\sigma^2} (\kappa - \sigma\rho.i.x- d) \frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}}\right]}$$
# <br>
# <br>
# $$and$$
# <br>
# <br>
# $$d = \sqrt{(\rho.\sigma.i.x)^2 - \sigma^2.(2.i.x - x^2)}$$
# $$g = \frac{\kappa - \rho.\sigma.i.x + d}{\kappa - \rho.\sigma.i.x - d}$$
#

# <br>
# <br>
# <h3><center>Python Implementation</center></h3>
#
# In our implementation, we will go from the last expression in our formula and build up until we arrive at the integrals.
#
# Our workflow should be:
#
# 1. Define a function f where
#     - Define d and g
#     - Compute the first exponential $e^{rT}S...$
#     - Compute the second exponential $exp\left[\frac{\tau\kappa\theta}{\sigma^2} ...\right]$
#     - Multiply these two
# <br>
# <br>
# 2. Compute the integral
#
# <h3><center>1. Defining f (fHeston)</center></h3>
# So we start by breaking down this monster of a function. We'll start by defining $f$ as `fHeston` with inputs `s, St, K, r, T, sigma, kappa, theta, volvol, rho` representing our inputs and the model parameters {$\sigma, \kappa, \theta, \nu,\rho $} respectively.
#
# Because our function will be using complex numbers, we can just define `i` as a global variable. Every complex number will essentially just be an operation on `i`.
#
# You'll also note that in the implementation, you can just treat `i` like any other variable and you should be fine. So no worries if you're not sure how to work with complex numbers!
#

# In[3]:


import numpy as np

i = complex(0,1)


# We can see that the expression $\rho.\sigma.i.s$ is used quite a lot. We can define this beforehand and just call it `prod`

# In[4]:


# To be used in the Heston pricer
def fHeston(s, St, K, r, T, sigma, kappa, theta, volvol, rho):
    # To be used a lot
    prod = rho * sigma *i *s


# Next, we split calculate `d`. You can do this on one line but it's a bit easier to read when you split the expression into smaller parts. Note that this is all still within the function

# In[5]:


# To be used in the Heston pricer
def fHeston(s, St, K, r, T, sigma, kappa, theta, volvol, rho):
    # To be used a lot
    prod = rho * sigma *i *s

    # Calculate d
    d1 = (prod - kappa)**2
    d2 = (sigma**2) * (i*s + s**2)
    d = np.sqrt(d1 + d2)



# We do the same for `g`

# In[6]:


# To be used in the Heston pricer
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


# Next we calculate the first exponential by splitting it into 3 parts and combining the computations. Again, this is just to make it easier to find bugs. It doesn't cost anything computation-wise:
#     $$e^{irxT}S_t^{ix} \left(\frac{1 - g.e^{d.\tau}}{1 - g}\right)^{\frac{-2\kappa \theta}{\sigma^2}}$$

# In[7]:


# To be used in the Heston pricer
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



# Finally, we compute the final exponential element to and find the product of the two to obtain our `fHeston`.

# In[8]:


import numpy as np

i = complex(0,1)
u = 1

# To be used in the Heston pricer
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


# <h3><center>2. Computing the integral</center></h3>
#
# <h4>Selecting a limit</h4>
# Because our integral goes up to infinity, we cannot have something running continuously.
#
# So what we do, is select a large limit that allows our integral to _converge._ By convergence, we simply mean that at some point, the additional areas under the curve we're calculating are so small that they're insignificant.
#
# Essentiallym if we find a number big enough, we can get accurate prices without having to pay a big computational cost.
#
# In our case, we selected `100`. You can try this with different values to see how it works.
#
#
# <h4>Selecting an integration scheme</h4>
#
# To compute our integral, we'll use a very simple integration scheme. This is the scheme we all used in elementary school. We simply split our area into rectangles and find the mid point. We use this mid point to calculate the area of each rectangle and sum them together.
#
# In our case, we initialize `P`,  the final price, as `0`, we split our area into `1000` rectangles and fix the limit to `100`.
#
# So in essence, the width of each rectangle will be `du = 100/1000`.
#
# We also calculate the first part $\left(\frac{1}{2}(S_t - Ke^{-r(T-t)})\right)$before starting on the integral:
#

# In[9]:


# Heston Pricer
def priceHestonMid(St, K, r, T, sigma, kappa, theta, volvol, rho):
    P, iterations, maxNumber = 0,1000,100
    ds = maxNumber/iterations

    element1 = 0.5 * (St - K * np.exp(-r * T))


# We define `s1` and `s2` as defined in the formula.
#
# You observe that we increment `s1` at each run of the loop. For example, at `j=1`, we make `s1 = du * (2*1 +1)/2` which i just `s1 = du * 1.5`.
#
# When `j=2`, then `s1 = du * (2*2 +1)/2` which is `s1 = 2.5 * du`. This verifies our mid point rule for the integration.
#
# You'll also note that we don't start from `0`. This is because going close to 0 may mean dividing a number by 0. Of course that'll be a problem.

# In[10]:


# Heston Pricer
def priceHestonMid(St, K, r, T, sigma, kappa, theta, volvol, rho):
    P, iterations, maxNumber = 0,1000,100
    ds = maxNumber/iterations

    element1 = 0.5 * (St - K * np.exp(-r * T))

    # Calculate the complex integral
    # Using j instead of i to avoid confusion
    for j in range(1, iterations):
        s1 = ds * (2*j + 1)/2
        s2 = s1 - i

        numerator1 = fHeston(s2,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator2 = K * fHeston(s1,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        denominator = np.exp(np.log(K) * i * s1) *i *s1


# So at this point, we have the width of all our rectangles, and the height is simply the value from the `fHeston` as we move along our x axis.
#
# The sum of the results from `fHeston` divided by the denominator are our height. So we can now just calculate our areas and sum them together.

# In[11]:


# Heston Pricer
def priceHestonMid(St, K, r, T, sigma, kappa, theta, volvol, rho):
    P, iterations, maxNumber = 0,1000,100
    du = maxNumber/iterations

    element1 = 0.5 * (St - K * np.exp(-r * T))

    # Calculate the complex integral
    # Using j instead of i to avoid confusion
    for j in range(1, iterations):
        s1 = du * (2*j + 1)/2
        s2 = u1 - i

        numerator1 = fHeston(s2,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator2 = K * fHeston(s1,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        denominator = np.exp(np.log(K) * i * s1) *i *s1

        P += ds *(numerator1 - numerator2)/denominator

    element2 = P/np.pi

    return np.real((element1 + element2))


# <h2><center> Full Pricer </center></h2>

# In[1]:


import numpy as np

i = complex(0,1)

# To be used in the Heston pricer
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

# Heston Pricer
def priceHestonMid(St, K, r, T, sigma, kappa, theta, volvol, rho):
    P, iterations, maxNumber = 0,1000,100
    ds = maxNumber/iterations

    element1 = 0.5 * (St - K * np.exp(-r * T))

    # Calculate the complex integral
    # Using j instead of i to avoid confusion
    for j in range(1, iterations):
        s1 = ds * (2*j + 1)/2
        s2 = s1 - i

        numerator1 = fHeston(s2,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator2 = K * fHeston(s1,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        denominator = np.exp(np.log(K) * i * s1) *i *s1

        P += ds *(numerator1 - numerator2)/denominator

    element2 = P/np.pi

    return np.real((element1 + element2))


# <h2><center> Annex</center></h2>
# <h3><center> How to obtain the simplified formula</center></h3>
# So we'll start by noting that:
#
# $$C = S_t .\left[\frac{1}{2} + \frac{1}{\pi} \int_0^{\inf} Re\left[\frac{e^{-is \,ln K} f_1(s,\nu, x)}{is}\right]ds\right] - Ke^{-r\tau}\left[\frac{1}{2} + \frac{1}{\pi} \int_0^{\inf} Re\left[\frac{e^{-is \,ln K} f_2(s,\nu, x)}{is}\right]ds\right]$$
# <br>
# <br>
# We extract the $1/2$ from the combined $P$ functions:
#
# $$C = \frac{1}{2}(S_t - Ke^{-r\tau}) +\left[\frac{S_t}{\pi} \int_0^{\inf} Re\left[\frac{e^{-is \,ln K} f_1(s,\nu, x)}{is}\right]ds - \frac{Ke^{-r\tau}}{\pi} \int_0^{\inf} Re\left[\frac{e^{-is \,ln K} f_2(s,\nu, x)}{is}\right]ds\right]$$
# <br>
# <br>
#
# We also note that $e^{-is \,ln K}$ is basically $e^{ln K^{-is}}$ which can also be simplified to $K^{-is}$ or $\frac{1}{K^{is}}$. We can therefore represent our call option formula as:
# <br>
# <br>
# $$C = \frac{1}{2}(S_t - Ke^{-r\tau}) +\frac{1}{\pi}\left[S_t \int_0^{\infty} Re\left[\frac{f_1(s,\nu, x)}{is. K^{iu}}\right]ds - Ke^{-r\tau} \int_0^{\inf} Re\left[\frac{f_2(s,\nu, x)}{is.K^{iu}}\right]ds\right]$$
# <br>
# <br>
# We can then put the expression in one integral:
# <br>
# <br>
# $$C = \frac{1}{2}(S_t - Ke^{-r\tau}) +\frac{1}{\pi}\int_0^{\infty} Re\left[S_t \frac{f_1(s,\nu, x)}{is. K^{iu}} - Ke^{-r\tau} \frac{f_2(s,\nu, x)}{is.K^{iu}}\right]ds$$
# <br>
# <br>
# From this point we can expand the expression for f:
# <br>
# <br>
# $$f_j(s,\nu, x) = exp(C_j(\tau, s) + D_j(\tau, s).\nu + i.s.x)$$
# <br>
# <br>
# Expanded out, f is defined as:
# <br>
# <br>
# $$f_j(s,\nu, x) = exp\left(r.i.s.\tau + \frac{\kappa  \theta}{\sigma^2}\left[ (BRS).\tau - 2 ln \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right)\right] + \frac{BRS}{\sigma^2} \left(\frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}} \right).\nu + i.s.x\right)$$
# <br>
# <br>
# $$where \,BRS = b_j - \rho.\sigma.i.s + d_j$$
# <br>
# <br>
# We can extract the first exponential of the `fHeston` function since:
# <br>
# <br>
# $$f_j(s,\nu, x) = exp\left(r.i.s.\tau + i.s.x \right ) \times exp\left(\frac{-2\kappa  \theta}{\sigma^2} ln \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right)\right)
# \times exp\left(BRS \frac{\kappa  \theta}{\sigma^2}\right)  \times exp\left( \frac{BRS}{\sigma^2} \left(\frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}} \right).\nu \right)$$
# <br>
# <br>
# Starting with the left most part, we obtain the same expression as `fHeston`:
# <br>
# <br>
# $$exp\left(r.i.s.\tau + i.s.x \right ) = e^{r.i.s.\tau} e^{i.s.ln S_t} = e^{r.i.s.\tau} S_t^{i.s}$$
# <br>
# <br>
# The second element we obtain is:
# <br>
# <br>
# $$exp\left(\frac{-2\kappa  \theta}{\sigma^2} ln \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right)\right) = exp\left(ln \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right)\times{\frac{-2\kappa  \theta}{\sigma^2}}\right) = \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right) ^ {\frac{-2\kappa  \theta}{\sigma^2}}$$
# <br>
# <br>
# The final part is simply rearranged:
# <br>
# <br>
# $$exp\left(BRS \frac{\kappa  \theta}{\sigma^2}\right)  \times exp\left( \frac{BRS}{\sigma^2} \left(\frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}} \right).\nu \right) = exp\left(BRS \frac{\kappa  \theta}{\sigma^2} +  \frac{BRS.\nu }{\sigma^2} \left(\frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}} \right)\right)$$
# <br>
# <br>
# So putting everything together:
# <br>
# <br>
# $$f_j(s,\nu, x) = e^{r.i.s.\tau} S_t^{i.s} \left(\frac{1 - g_j.e^{d_j.\tau}}{1 - g_j}\right) ^ {\frac{-2\kappa  \theta}{\sigma^2}}exp\left(BRS \frac{\kappa  \theta}{\sigma^2} +  \frac{BRS.\nu }{\sigma^2} \left(\frac{1 - e^{d_j.\tau}}{1 - g_j.e^{d_j.\tau}} \right)\right)$$
#

# <br>
# <br>
# <br>
#
# <h3><center> More Integration Schemes</center></h3>

# In[13]:



# Heston pricer Trapezoidal Rule
def priceHestonTrap(St, K, r, T, sigma, kappa, theta, volvol, rho):
    P, iterations, maxNumber = 0,1000,100
    du = maxNumber/iterations

    element1 = 0.5 * (St - K * np.exp(-r * T))

    P1 = du * ((phiHeston(du-i, St, K, r, T, sigma, kappa, theta, volvol, rho) -
               K * phiHeston(du, St, K, r, T, sigma, kappa, theta, volvol, rho))/
              2 * np.exp(np.log(K) * i *du) * i * du)

    PN = du * ((phiHeston(du * iterations -i, St, K, r, T, sigma, kappa, theta, volvol, rho) -
               K * phiHeston(du * iterations, St, K, r, T, sigma, kappa, theta, volvol, rho))/
              2 * np.exp(np.log(K) * i * du * iterations) * i * du * iterations)

    # Calculate the complex integral
    # Using j instead of i to avoid confusion
    for j in range(2, iterations):
        u1 = du * j
        u2 = u1 - i

        numerator1 = phiHeston(u2,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator2 = K * phiHeston(u1,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        denominator = np.exp(np.log(K) * i * u1) *i *u1

        P += du *(numerator1 - numerator2)/denominator

    element2 = (P + P1 + PN)/np.pi

    return np.real((element1 + element2))

# Heston pricer Trapezoidal Rule
def priceHestonSimp(St, K, r, T, sigma, kappa, theta, volvol, rho):
    PEven, POdd, iterations, maxNumber = 0,0,1000,100
    du = maxNumber/iterations

    element1 = 0.5 * (St - K * np.exp(-r * T))

    P1 = du * ((phiHeston(du-i, St, K, r, T, sigma, kappa, theta, volvol, rho) -
               K * phiHeston(du, St, K, r, T, sigma, kappa, theta, volvol, rho))/
              3 * np.exp(np.log(K) * i *du) * i * du)

    PN = du * ((phiHeston(du * iterations -i, St, K, r, T, sigma, kappa, theta, volvol, rho) -
               K * phiHeston(du * iterations, St, K, r, T, sigma, kappa, theta, volvol, rho))/
              3 * np.exp(np.log(K) * i * du * iterations) * i * du * iterations)

    # Calculate the complex integral
    # Using j instead of i to avoid confusion
    for j in range(2, iterations, 2):
        u1 = du * j
        u2 = u1 - i

        numerator1Even = phiHeston(u2,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator2Even = K * phiHeston(u1,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator1Odd = phiHeston(u2+du,  St, K, r, T, sigma, kappa, theta, volvol, rho)
        numerator2Odd = K * phiHeston(u1+du,  St, K, r, T, sigma, kappa, theta, volvol, rho)

        denominatorEven = np.exp(np.log(K) * i * u1) *i *u1
        denominatorOdd = np.exp(np.log(K) * i * (u1+du)) *i *(u1+du)

        PEven += du * 4 *(numerator1Even - numerator2Even)/(3 * denominatorEven)
        POdd += du *2 * (numerator1Odd - numerator2Odd)/(3 * denominatorOdd)

    element2 = (PEven + POdd + P1 + PN)/np.pi

    return np.real((element1 + element2))


# <img alt = 'code-more' src = 'img/img.png'>
