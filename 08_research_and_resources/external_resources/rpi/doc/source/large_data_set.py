#
# Storing a Larger Data Set on Disk
# with Python/pandas/PyTables
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
# 
import os
from time import time
import numpy as np
import pandas as pd

filename = 'data.h5'

#
# Generating the sample data
#
t0 = time()

data = np.random.standard_normal(10000000)  # random data

df = pd.DataFrame(data)  # pandas DataFrame object

#
# Storing data in HDF5 database
#
t1 = time()

h5 = pd.HDFStore(filename, 'w')  # open database file
h5['data'] = df  # write DataFrame to disk
h5.close()  # close database file

t2 = time()
os.remove(filename)  # delete file on disk
#
# Output
#
print "Size of data set in bytes %d" % data.nbytes
print "Time needed to generate data in sec. %5.2f" % (t1 - t0)
print "Time needed to store data in sec.    %5.2f" % (t2 - t1)
