#!/bin/bash

# Script to Start
# Jupyter Notebook Server
#
# Dr. Yves J. Hilpisch
# The Python Quants GmbH
# 

PW = expr $1
PORT = expr $2

echo -n $PW | awk '{print "c.NotebookApp.password = '\''" $1 "'\''"}' >> /root/.ipython/profile_default/ipython_notebook_config.py

export PATH="/root/anaconda/bin:$PATH"

ipython notebook --no-browser --port $PORT --ip=*

