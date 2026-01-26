import numpy as np
import matplotlib.pyplot as plt

s0=189  # Initial stock price 
k=195;c=6.30;  # Strike price and Premium of the option
shares = 100   # Shares per lot 
sT = np.arange(0,2*s0,5) # Stock Price at expiration of the Call

# Profit/loss from long stock position
y1= (sT-s0) * shares

# Payoff from a Short Call Option
y2 = np.where(sT > k,((k - sT) + c) * shares, c * shares)

# Payoff from a Covered Call
y3 = np.where(sT > k,((k - s0) + c) * shares,((sT- s0) + c) * shares )

# Create a plot using matplotlib    
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False)   # Top border removed 
ax.spines['right'].set_visible(False) # Right border removed
ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
ax.tick_params(top=False, right=False) # Removes the tick-marks on the RHS

plt.plot(sT,y1,lw=1.5,label='Long Stock')
plt.plot(sT,y2,lw=1.5,label='Short Call')
plt.plot(sT,y3,lw=1.5,label='Covered Call')

plt.title('Covered Call')        
plt.xlabel('Stock Prices')
plt.ylabel('Profit/loss')

plt.grid(True)
plt.axis('tight')
plt.legend(loc=0)
plt.show()


