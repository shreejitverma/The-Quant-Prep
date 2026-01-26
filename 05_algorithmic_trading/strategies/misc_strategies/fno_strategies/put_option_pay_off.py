import numpy as np
import pandas as pd
# Tata motors stock price 
spot_price = 430 
# Stock price range at expiration of the call
sT = np.arange(0.98*spot_price,1.03*spot_price)
# Put
strike_price = 430 
premium = 3
payoff_put = np.where(sT < strike_price, strike_price - sT, 0) 
payoff_put = payoff_put - premium
df = pd.DataFrame({'stock_price':sT, 'payoff_put':payoff_put})
print df.head(20)
