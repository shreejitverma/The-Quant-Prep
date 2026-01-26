#
# Calibration of Gruenbichler-Longstaff (1996)
# square-root diffusion framework to
# VSTOXX options traded at Eurex
# Data as of 31. March 2014
# All data from www.eurexchange.com
#
# (c) The Python Quants GmbH
# For illustration purposes only.
# August 2014
#
import numpy as np
import pandas as pd
from pricing_formulae import call_price
import scipy.optimize as sco
import matplotlib.pyplot as plt

path = 'source/data/'

# Fixed Parameters
r = 0.01  # risk-less short rate
V0 = 17.6639  # VSTOXX index at 31.03.2014
zeta_V = 0.  # volatility risk premium factor

# Option quotes

def read_select_quotes(path=path):
    h5 = pd.HDFStore(path + 'vstoxx_option_quotes.h5', 'r')
    option_data = h5['option_quotes']
    h5.close()
    tol = 0.25  # tolerance level in percent
    # only those option close enough to the ATM level
    option_data = option_data[(option_data.STRIKE > (1 - tol) * V0)
                            & (option_data.STRIKE < (1 + tol) * V0)]
    return option_data

i = 0  # counter for calibration iterations


def valuation_function(p0):
    ''' Valuation Function for set of strike prices

    p0: list
        set of parameters for calibration
    '''
    kappa_V, theta_V, sigma_V = p0
    call_prices = []
    for strike in strikes:
        call_prices.append(call_price(V0, kappa_V, theta_V,
                                   sigma_V, zeta_V, ttm, r, strike))
    return np.array(call_prices)

def error_function(p0):
    ''' Error Function for Model Calibration

    p0: list
        set of parameters for calibration
    '''
    global i 
    call_prices = valuation_function(p0)
    kappa_V, theta_V, sigma_V = p0
    pen = 0.
    if 2 * kappa_V * theta_V < sigma_V ** 2:
        pen = 1000.0
    if kappa_V < 0 or theta_V < 0 or sigma_V < 0:
        pen = 1000.0
    if relative is True:
        MSE = (np.sum(((call_prices - call_quotes) / call_quotes) ** 2)
                / len(call_quotes) + pen)
    else:
        MSE = np.sum((call_prices - call_quotes) ** 2) / len(call_quotes) + pen

    if i == 0:
            print ("{:>6s} {:>6s} {:>6s}".format('kappa', 'theta', 'sigma') 
                 + "{:>12s}".format('MSE'))

    # print intermediate results: every 100th iteration
    if i % 100 == 0:
        print "{:6.3f} {:6.3f} {:6.3f}".format(*p0) + "{:>12.5f}".format(MSE)
    i += 1
    return MSE



def model_calibration(option_data, rel=False, mat='2014-07-18'):
    ''' Function for global and local model calibration.
    
    option_data: pandas DataFrame object
        option quotes to be used
    relative: bool
        relative or absolute MSE
    maturity: start
        maturity of option quotes to calibrate to
    '''
    global relative  # if True: MSRE is used, if False: MSAE
    global strikes
    global call_quotes
    global ttm
    global i

    relative = rel
    # only option quotes for a single maturity
    option_quotes = option_data[option_data.MATURITY == mat]

    # time-to-maturity from the data set
    ttm = option_quotes.iloc[0, -1]

    # transform strike column and price column in ndarray object
    strikes = option_quotes['STRIKE'].values
    call_quotes = option_quotes['PRICE'].values

    # global optimization
    i = 0  # counter for calibration iterations
    p0 = sco.brute(error_function, ((5.0, 20.1, 1.0), (10., 30.1, 1.25),
                             (1.0, 9.1, 2.0)), finish=None)

    # local optimization
    i = 0
    opt = sco.fmin(error_function, p0, xtol=0.0000001, ftol=0.0000001,
                                 maxiter=1000, maxfun=1500)

    return opt



def plot_calibration_results(opt):
    ''' Function to plot market quotes vs. model prices.

    opt: list
        options results from calibration
    '''   
    call_values = valuation_function(opt)
    diffs = call_values - call_quotes
    plt.figure()
    plt.subplot(211)
    plt.plot(strikes, call_quotes, label='market quotes')
    plt.plot(strikes, call_values, 'ro', label='model prices')
    plt.ylabel('option values')
    plt.grid(True)
    plt.legend()
    plt.axis([min(strikes) - 0.5, max(strikes) + 0.5,
          0.0, max(call_quotes) * 1.1])
    plt.subplot(212)
    wi = 0.3
    plt.bar(strikes - wi / 2, diffs, width=wi)
    plt.grid(True)
    plt.xlabel('strike price')
    plt.ylabel('difference')
    plt.axis([min(strikes) - 0.5, max(strikes) + 0.5,
          min(diffs) * 1.1, max(diffs) * 1.1])
    plt.tight_layout()

if __name__ == '__main__':
    option_data = read_select_quotes()
    opt = model_calibration(option_data=option_data)

