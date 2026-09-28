'''
The code from finlab folder is originally from https://github.com/finlab-python/finlab_crypto
'''
import vectorbt as vbt


# set default fees and slippage
vbt.settings.portfolio['init_cash'] = 100.0  # in $
vbt.settings.portfolio['fees'] = 0.001       # in %
vbt.settings.portfolio['slippage'] = 0.001   # in %
