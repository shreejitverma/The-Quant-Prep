#
# Script to Install
# Basic Python Components
#
# Dr. Yves J. Hilpisch
# The Python Quants GmbH
#


# GENERAL LINUX
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y
apt-get install -y git screen htop wget nano bzip2
apt-get upgrade -y bash
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# INSTALL ANACONDA
wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.3.0-Linux-x86_64.sh -O Anaconda.sh
bash Anaconda.sh -b
rm -rf Anaconda.sh 

export PATH="/root/anaconda/bin:$PATH"

# INSTALL PYTHON LIBRARIES
conda install seaborn
pip install plotly
pip install cufflinks
pip install tstables

