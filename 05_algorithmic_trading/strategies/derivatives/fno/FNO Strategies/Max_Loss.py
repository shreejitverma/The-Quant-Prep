import numpy as np
def call_payoff(sT, strike_price, premium):
    return np.where(sT > strike_price, sT - strike_price, 0) - premium
# Tata motors stock price 
spot_price = 430 
# Stock price range at expiration of the call
sT = np.arange(0.8*spot_price,1.2*spot_price)
# Long call
strike_price_long_call = 440 
premium_long_call = 4.6
# Long call payoff
payoff_long_call = call_payoff(sT, strike_price_long_call, premium_long_call)
# Short call
strike_price_short_call = 450 
premium_short_call = 2.3
# Short call payoff
payoff_short_call = call_payoff(sT, strike_price_short_call, premium_short_call) * -1.0
# Strategy payoff
payoff_spread = payoff_long_call + payoff_short_call
max_loss = min(payoff_spread)
print max_loss
