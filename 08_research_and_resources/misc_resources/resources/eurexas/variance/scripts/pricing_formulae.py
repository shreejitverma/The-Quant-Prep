#
# Module for the valuation of European
# volatility futures & options
# in Gruenbichler-Longstaff (1996)
# square-root diffusion framework
# via semi-analytical formulae and
# Monte Carlo simulation
#
# (c) The Python Quants GmbH
# For illustration purposes only.
# August 2014
#
import math
import numpy as np
import scipy.stats as scs

# Model parameters
V0 = 17.5  # initial level of volatility index
kappa_V = 0.1  # speed of mean reversion
theta_V = 20.0  # long-term index level
sigma_V = 2.0  # volatility of volatility
zeta_V = 0.0  # factor of the expected volatility risk premium
r = 0.01  # risk-free interest rate

# Option parameters
K = 20.0  # strike
T = 1.0  # time horizon

#
# Formula for futures valuation
#


def futures_price(V0, kappa_V, theta_V, zeta_V, T):
    ''' Futures pricing formula in GL96 model.
     
     V0: float (positive)
        current volatility level
     kappa_V: float (positive)
        mean-reversion factor
     theta_V: float (positive)
        long-run mean of volatility
     zeta_V: float (positive)
        volatility risk premium
     T: float (positive)
        time-to-maturity
    '''
    alpha = kappa_V * theta_V
    beta = kappa_V + zeta_V
    future = (alpha / beta * (1 - math.exp(-beta * T))
                               + math.exp(-beta * T) * V0)
    return future


#
# Semi-analytical call option pricing formula
#

def cx(K, gamma, nu, lambda_V, exact=True):
    ''' Complementary distribution function of non-central chi-squared density.
    K: float (positive)
        strike price
    gamma: float (positive)
        as defined in the GL96 model
    nu: float (positive)
        degrees of freedom
    lambda_V: float (positive)
        non-centrality parameter
    '''
    return 1 - scs.ncx2.cdf(gamma * K, nu, lambda_V)


def call_price(V0, kappa_V, theta_V, sigma_V, zeta_V, T, r, K):
    ''' Call option pricing formula in GL96 Model
     
     V0: float (positive)
        current volatility level
     kappa_V: float (positive)
        mean-reversion factor
     theta_V: float (positive)
        long-run mean of volatility
     sigma_V: float (positive)
        volatility of volatility
     zeta_V: float (positive)
        volatility risk premium
     T: float (positive)
        time-to-maturity
     r: float (positive)
        risk-free short rate
     K: float(positive)
        strike price of the option
    '''
    D = math.exp(-r * T)  # discount factor
    
    alpha = kappa_V * theta_V
    beta = kappa_V + zeta_V
    gamma = 4 * beta / (sigma_V ** 2 * (1 - math.exp(-beta * T)))
    nu = 4 * alpha / sigma_V ** 2
    lambda_V = gamma * math.exp(-beta * T) * V0

    # the pricing formula
    call = (D * math.exp(-beta * T) * V0 * cx(K, gamma, nu + 4, lambda_V)
      + D * (alpha / beta) * (1 - math.exp(-beta * T))
      * cx(K, gamma, nu + 2, lambda_V)
      - D * K * cx(K, gamma, nu, lambda_V))
    return call



#
# Monte Carlo simulation (exact discretization)
#
# Simulation parameters
M = 50  # time steps
dt = T / M  # time interval
I = 50000  # number of MCS paths


def generate_paths(x0, kappa, theta, sigma, T, M, I):
    ''' Simulation of square-root diffusion with exact discretization
    x0: float (positive)
        starting value
    kappa: float (positive)
        mean-reversion factor
    theta: float (positive)
        long-run mean
    sigma: float (positive)
        volatility (of volatility)
    T: float (positive)
        time-to-maturity
    M: int
        number of time intervals
    I: int
        number of simulation paths
    '''
    x = np.zeros((M + 1, I), dtype=np.float)
    x[0, :] = x0
    ran = np.random.standard_normal((M + 1, I))
      # matrix filled with standard normally distributed rv
    d = 4 * kappa * theta / sigma ** 2
    c = (sigma ** 2 * (1 - math.exp(-kappa * dt))) / (4 * kappa)
      # constant factor in the integrated process of x
    if d > 1:
        for t in range(1, M + 1):
            l = x[t - 1, :] * math.exp(-kappa * dt) / c
              # non-centrality parameter
            chi = np.random.chisquare(d - 1, I)
              # matrix with chi-squared distributed rv
            x[t, :] = c * ((ran[t] + np.sqrt(l)) ** 2 + chi)
    else:
        for t in range(1, M + 1):
            l = x[t - 1, :] * math.exp(-kappa * dt) / c
            N = np.random.poisson(l / 2, I)
            chi = np.random.chisquare(d + 2 * N, I)
            x[t, :] = c * chi
    return x


def call_estimator(V0, kappa_V, theta_V, sigma_V, T, r, K, M, I):
    ''' Estimation of European call option price in GL96 Model
    via Monte Carlo simulation
    V0: float (positive)
        current volatility level
    kappa_V: float (positive)
        mean-reversion factor
    theta_V: float (positive)
        long-run mean of volatility
    sigma_V: float (positive)
        volatility of volatility
    T: float (positive)
        time-to-maturity
    r: float (positive)
        risk-free short rate
    K: float (positive)
        strike price of the option
    M: int
        number of time intervals
    I: int
        number of simulation paths
    '''
    V = generate_paths(V0, kappa_V, theta_V, sigma_V, T, M, I)
    return math.exp(-r * T) * np.sum(np.maximum(V[-1] - K, 0)) / I
