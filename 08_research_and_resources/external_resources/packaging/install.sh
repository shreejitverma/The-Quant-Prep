#
# Script to Install
# Linux Tools
#
# The Python Quants GmbH
#
apt-get update
apt-get upgrade -y

# Linux System Tools
apt-get install -y wget screen htop
apt-get install -y tree vim git man less

# Python3 via Linux
apt-get install -y python3 python3-pip
pip3 install pip --upgrade
pip install numpy pandas scipy
pip install matplotlib xarray q
pip install twine
pip install setuptools wheels
pip install ipython jupyterlab

# Configuration
wget https://certificate.tpq.io/.vimrc -O ~/.vimrc
mkdir /root/.jupyter
mkdir -p /root/.jupyter/lab/user-settings/@jupyterlab/shortcuts-extension/
cp jupyter_shortcuts.json /root/.jupyter/lab/user-settings/@jupyterlab/shortcuts-extension/shortcuts.jupyterlab-settings

# JupyterLab
jupyter server password
# jupyter lab --allow-root --ip 0.0.0.0 --port 9999
