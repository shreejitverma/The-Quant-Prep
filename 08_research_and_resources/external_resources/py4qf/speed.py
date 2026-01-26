#
# Simulation Speed
#
import math
import numpy as np
from numpy.random import default_rng
rng = default_rng()
S0, T, r, sigma, I = 100, 1.5, 0.05, 0.2, 10_000_000
ST = S0 * np.exp((r - sigma ** 2 / 2) * T +
	sigma * math.sqrt(T) * rng.standard_normal(I))
print('Average, discounted price: %f'
	% (ST.mean() * math.exp(-r * T)))