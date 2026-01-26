#
# Mathematical Operations
#
import math

S0, T, r = 100, 1.5, 0.05
F = S0 * math.exp(r * T)
print(f'The forward price is: {F:.3f}')
