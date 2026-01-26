#
# Collecting and Storing Stock Price Data
# with Python/pandas/PyTables
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
# 
import os
from time import time
import pandas as pd
import pandas.io.data as web

symbols = ['AAPL', 'YHOO', 'MSFT']

filename = 'data.h5'

#
# Collecting the data
#
t0 = time()
store = {}  # dictionary to store DataFrame objects

for sym in symbols:
    store[sym] = web.DataReader(sym, data_source='yahoo', start='2000/1/1')

#
# Storing data in HDF5 database
#
t1 = time()

h5 = pd.HDFStore(filename, 'w')  # open database file

for sym in symbols:
    h5[sym] = store[sym]  # write DataFrame to disk

h5.close()  # close database

t2 = time()
os.remove(filename)  # delete file on disk
#
# Output
#
print "Time needed to collect data in sec. %5.2f" % (t1 - t0)
print "Time needed to store data in sec.   %5.2f" % (t2 - t1)