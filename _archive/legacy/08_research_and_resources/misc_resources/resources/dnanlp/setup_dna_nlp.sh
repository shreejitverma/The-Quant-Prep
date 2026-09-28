# Script to Install
# Linux System Tools and
# Basic Python Components
# as well as to 
# Start Jupyter Notebook Server
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
# GENERAL LINUX
printf "Installing system tools.\n\n"
apt-get update  # updates the package index cache
apt-get upgrade -y  # updates packages
# installs system tools
apt-get install -y git screen htop wget vim bzip2
apt-get install -y build-essential gcc zip default-jre
apt-get install -y poppler-utils  # pdf file conversion
apt-get upgrade -y bash  # upgrades bash if necessary

printf "Cleaning up package index cache.\n\n"
apt-get clean  # cleans up the package index cache

# INSTALLING MINICONDA
printf "Installing Miniconda.\n\n"
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O \
  Miniconda.sh
bash Miniconda.sh -b  # installs Miniconda
rm Miniconda.sh  # removes the installer
# prepends the new path for current session
export PATH="/root/miniconda3/bin:$PATH"
# prepends the new path in the shell configuration
echo ". /root/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
echo "conda activate" >> ~/.bashrc

printf "Updating miniconda\n\n"
conda update -y conda 

# INSTALLING PYTHON PACKAGES
printf "Installing Python packages.\n\n"
conda install -y jupyter  # Python coding in the browser
conda install -y pytables  # HDF5 database wrapper
conda install -y pandas  # data analysis package
conda install -y matplotlib  # plotting package
conda install -y scikit-learn  # machine learning package
conda install -y nltk=3.2.5  # nlp package
conda install -y gensim  # nlp package
conda install -y networkx  # network graph
conda install -y lxml  # xml/html parsing

pip install --upgrade pip
pip install Cython
pip install cufflinks  # combining plotly with pandas
pip install wordcloud
pip install pyvis

# NLTK PACKAGES
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('wordnet')"

# INSTALLING APACHE'S AVRO PACKAGE
printf "Installing avro package.\n"
wget http://mirror.synyx.de/apache/avro/stable/py3/avro-python3-1.8.2.tar.gz
tar xvf avro-python3-1.8.2.tar.gz
cd avro-python3-1.8.2
python setup.py install
cd ..
rm avro-python3-1.8.2.tar.gz
rm -rf avro-python3-1.8.2

# COPYING FILES AND CREATING DIRECTORIES
mkdir /root/.jupyter
mkdir /root/.jupyter/custom

cd /root/.jupyter
wget -q http://hilpisch.com/nlp/jupyter_setup.py
printf "Please provide a new password for your Jupyter server.\n"
printf "New password [ENTER]: "
read -s password
printf "\n"

printf "Repeat password [ENTER]: "
read -s rep_password
printf "\n"

while [ "$password" = "" -o "$password"  != "$rep_password" ]
do
printf "The passwords are empty or not equal, please try again!\n"
printf "New password [ENTER]: "
read -s password
printf "\n"

printf "Repeat password [ENTER]: "
read -s rep_password
printf "\n"
done

JUPYTER_URL=$(python jupyter_setup.py $password)

mkdir /root/notebook
cd /root/notebook

# CLONING THE REPO
printf "Cloning the DNA NLP Git repository.\n"
git clone --depth=1 http://github.com/yhilpisch/dnanlp

printf "Downloading additional files.\n"
cd /root/notebook/dnanlp/modules
wget -q http://hilpisch.com/nlp/soiepy.zip
unzip soiepy.zip
rm soiepy.zip

cd /root/notebook/
printf "Success.\n"

# CREATE A SWAP PARTITION
# comment out these lines if not required
wget -q http://hilpisch.com/nlp/create_swap.sh
/bin/bash /root/notebook/create_swap.sh
rm /root/notebook/create_swap.sh

# STARTING JUPYTER NOTEBOOK
wget -q http://hilpisch.com/nlp/custom.css
mv custom.css /root/.jupyter/custom/custom.css
mkdir logs
touch logs/jupyter.log
nohup jupyter notebook --allow-root > logs/jupyter.log &

printf "\n\n"
printf "Your Jupyter Server is running. To access it, please visit:\n\n"
printf "$JUPYTER_URL\n\n"
