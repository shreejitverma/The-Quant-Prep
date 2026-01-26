#
# Valuation of European volatility options
# by Monte Carlo simulation in
# Gruenbichler-Longstaff (1996) model
# -- analysis of valuation results
#
# (c) The Python Quants GmbH
# For illustration purposes only.
# August 2014
#
import numpy as np
from datetime import datetime
import time
import math
from pricing_formulae import call_price
from simulation_results import *

# Model Parameters
V0 = 20  # initial volatility
kappa_V = 3.0  # speed of mean reversion
theta_V = 20.0  # long-term volatility
sigma_V = 3.2  # standard deviation coefficient
zeta_V = 0.0  # proportional factor of the expected volatility risk premium
r = 0.01  # risk-free short rate

# General Simulation Parameters
write = True
var_red = [(False, False), (False, True), (True, False), (True, True)]
    # 1st = mo_match -- random number correction (std + mean + drift)
    # 2nd = anti_paths -- antithetic paths for variance reduction
steps_list = [25, 50, 75, 100]  # Time Steps
paths_list = [2500, 50000, 75000, 100000, 125000, 150000]
    # number of paths per valuation
SEED = 100000  # seed value
runs = 3  # number of simulation runs
PY1 = 0.010  # performance yardstick 1: abs. error in currency units
PY2 = 0.010  # performance yardstick 2: rel. error in decimals
maturity_list = [1.0 / 12 , 1.0 / 4, 1.0 / 2, 1.0]  # maturity List
strike_list = [15.0, 17.5, 20.0, 22.5, 25.0]  # strike List

#
# Simulation Function for GL96 Volatility Process
#


def generate_paths(x0, kappa, theta, sigma, T, steps, paths):
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
    steps: int
        number of time intervals
    paths: int
        number of simulation paths
    '''
    x = np.zeros((steps + 1, paths), dtype=np.float)
    x[0, :] = x0
    ran = randoms(steps, paths)
      # matrix filled with standard normally distributed rv
    d = 4 * kappa * theta / sigma ** 2
    c = (sigma ** 2 * (1 - math.exp(-kappa * dt))) / (4 * kappa)
      # constant factor in the integrated process of x
    if d > 1:
        for t in range(1, steps + 1):
            l = x[t - 1, :] * math.exp(-kappa * dt) / c
              # non-centrality parameter
            chi = np.random.chisquare(d - 1, paths)
              # matrix with chi-squared distributed rv
            x[t, :] = c * ((ran[t] + np.sqrt(l)) ** 2 + chi)
    else:
        for t in range(1, steps + 1):
            l = x[t - 1, :] * math.exp(-kappa * dt) / c
            N = np.random.poisson(l / 2, paths)
            chi = np.random.chisquare(d + 2 * N, paths)
            x[t, :] = c * chi
    return x


def randoms(steps, paths):
    ''' Function to generate pseudo-random numbers with variance reduction.
    steps: int
        number of discrete time intervals
    paths: int
        number of simulated paths
    '''
    if anti_paths is True:
        rand_ = np.random.standard_normal((steps + 1, paths / 2))
        rand = np.concatenate((rand_, -rand_), 1)
    else:
        rand = np.random.standard_normal((steps + 1, paths))
    if mo_match is True:
        rand = rand / np.std(rand)
        rand = rand - np.mean(rand)
    return rand

#
# Valuation
#
t0 = time.time()
sim_results = pd.DataFrame()

for vr in var_red:  # variance reduction techniques
    mo_match, anti_paths = vr
    for steps in steps_list:  # number of time steps
        for paths in paths_list:  # number of paths
            t1 = time.time()
            d1 = datetime.now() 
            abs_errors = []
            rel_errors = []
            l = 0.0
            errors = 0
            # name of the simulation Setup
            name = ('Call_' + str(runs) + '_'
                    + str(steps) + '_' + str(paths / 1000)
                    + '_' + str(mo_match)[0] + str(anti_paths)[0] +
                    '_' + str(PY1 * 100) + '_' + str(PY2 * 100))
            np.random.seed(SEED)  # RNG seed value
            for run in range(runs):  # Simulation Runs
                print "\nSimulation Run %d of %d" % (run + 1, runs)
                print "----------------------------------------------------"
                print ("Elapsed Time in Minutes %8.2f"
                        % ((time.time() - t0) / 60))
                print "----------------------------------------------------"
                z = 0
                for T in maturity_list:  # Time-to-Maturity
                    dt = T / steps  # time interval in year fractions
                    V = generate_paths(V0, kappa_V, theta_V, sigma_V, T, steps, paths)
                        # volatility process paths
                    print "\n  Results for Time-to-Maturity %6.3f" % T
                    print "  -----------------------------------------"
                    for K in strike_list:  # Strikes
                        h = np.maximum(V[-1] - K, 0)  # inner value matrix
                        ## MCS Estimator
                        call_estimate = math.exp(-r * T) * np.sum(h) / paths * 100
                        ## BSM Analytical Value
                        call_value = call_price(V0, kappa_V, theta_V, sigma_V,
                                        zeta_V, T, r, K) * 100
                        ## Errors
                        diff = call_estimate - call_value
                        rdiff = diff / call_value
                        abs_errors.append(diff)
                        rel_errors.append(rdiff * 100)
                        ## Output
                        br = "    ----------------------------------"
                        print "\n  Results for Strike %4.2f\n" % K
                        print ("    European Op. Value MCS    %8.4f" %  
                                    call_estimate)
                        print ("    European Op. Value Closed %8.4f" % 
                                    call_value)
                        print "    Valuation Error (abs)     %8.4f" % diff
                        print "    Valuation Error (rel)     %8.4f" % rdiff
                        if abs(diff) < PY1 or abs(diff) / call_value < PY2:
                                print "      Accuracy ok!\n" + br
                                CORR = True
                        else:
                                print "      Accuracy NOT ok!\n" + br
                                CORR = False
                                errors = errors + 1
                        print "    %d Errors, %d Values, %.1f Min." \
                                % (errors, len(abs_errors),
                            float((time.time() - t1) / 60))
                        print ("    %d Time Intervals, %d Paths"
                                % (steps, paths))
                        z = z + 1
                        l = l + 1

            t2 = time.time()
            d2 = datetime.now()
            if write is True:  # Append Simulation Results
                sim_results = write_results(sim_results, name, SEED,
                        runs, steps, paths, mo_match, anti_paths,
                        l, PY1, PY2, errors,
                        float(errors) / l, np.array(abs_errors),
                        np.array(rel_errors), t2 - t1, (t2 - t1) / 60, d1, d2)

if write is True:  # write/append DataFrame to HDFStore
    write_to_database(sim_results)