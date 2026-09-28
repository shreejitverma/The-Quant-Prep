#
# Python Installation (incl. Jupyter)
# (c) Dr Yves J Hilpisch
# The Python Quants GmbH
#

# A FEW SYSTEM TOOLS
# ADD THINGS YOU WANT TO USE (e.g. Git)
apt-get install htop unzip -y
apt-get autoremove

# INSTALL MINICONDA
wget -q http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O Miniconda.sh
bash Miniconda.sh -b
rm Miniconda.sh
export PATH="$HOME/miniconda2/bin:$PATH"

cat >> ~/.profile <<EOF
export PATH="$HOME/miniconda2/bin:$PATH"
EOF

# INSTALL PYTHON LIBRARIES --
# ADD LIBRARIES YOU WANT TO USE
conda install -y jupyter
conda install -y matplotlib
conda install -y pandas
conda install -y seaborn
conda install -y pandas-datareader
conda install -y pytables
conda install -y scikit-learn

pip install --upgrade pip
pip install plotly
pip install cufflinks
pip install flask-wtf

# COPYING FILES
mkdir ${HOME}/.jupyter
mv ${HOME}/jupyter_notebook_config.py ${HOME}/.jupyter/
mkdir ${HOME}/notebook
mv ${HOME}/*.ipynb ${HOME}/notebook
rm ${HOME}/*.ipynb
unzip ${HOME}/stock_int.zip -d ${HOME}/notebook
rm ${HOME}/stock_int.zip
cd ${HOME}/notebook

# STARTING JUPYTER NOTEBOOK
jupyter notebook --notebook-dir=$HOME/notebook
