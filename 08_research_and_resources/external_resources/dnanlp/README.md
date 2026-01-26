# Unlocking the Hidden Potential of Unstructuctured News Data with NLP

This repository provides Python codes and Jupyter Notebooks for the Dow Jones applied research paper "Unlocking the Hidden Potential of Unstructured News Data with NLP &mdash; Understanding Advanced Analytics through Real-World Case Studies".

<img src="http://hilpisch.com/images/dna_paper_cover.png" width="500">

## Applied Research Paper Download

To **download** the PDF version of the paper visit http://go.dowjones.com/dna-research-paper.

## Setup and Installation

The instructions that follow assume that you run a **Docker container** or a **cloud instance** with the latest version of Ubunutu (18.10 at the time of this writing).

The execution of (parts of) the codes and Jupyter Notebooks requires enough **compute and memory resources**. Overall, it is recommended to have at least **four CPU cores and 16GB of RAM** available. The introductory examples can be executed with fewer resources.

### Cloud Instance

The following assumes that you have set up a **cloud instance** (e.g. on DigitalOcean) and have used `ssh` to login as `root`. You can then execute on the shell:

    cd /root
    wget http://hilpisch.com/nlp/setup_dna_nlp.sh
    bash setup_dna_nlp.sh

Follow the **instructions** of the script and e.g. provide a password for the Jupyter Notebook server.

After the installation, you can access the **Jupyter Notebook server** under

    http://CLOUD_IP_ADDRESS:9999

with your chosen password. Navigate via Jupyter to the code folder and open a notebook to get started.

### Docker Container

Alternatively, you can start a **Docker container** locally (with enough resources allocated). To do so e.g. execute on the shell:

    docker run -ti -h dnanlp -p 9999:9999 ubuntu:latest /bin/bash

Make sure that the container has **enough resources** allocated (e.g. via editing your Docker preferences). Then on the shell of the Docker container execute the following:

    cd root
    apt-get update
    apt-get upgrade -y
    apt-get install -y wget
    wget http://hilpisch.com/nlp/setup_dna_nlp.sh
    bash setup_dna_nlp.sh

Then follow the **instructions** of the script to e.g. provide a password for the Jupyter Notebook server.

After the installation, you can access the **Jupyter Notebook server** under

    http://localhost:9999

with your chosen password. Navigate via Jupyter to the code folder and open a notebook to get started.

## Security Risks and Disclaimer

The approach chosen to run the Jupyter Notebook server is for **illustration purposes** only. There are no security measures configured beyond password protection. For example, there is no SSL encryption configured. In addition, the Jupyter Notebook server is run as `root`. As a consequence, a number of **security risks** result from the approach chosen.

All codes and Jupyter notebooks come with **no representations or warranties**, to the extent permitted by applicable law.

This repository with all its scripts, codes and Jupyter notebooks is for **illustration purposes** only.

## Company Information

© Dr. Yves J. Hilpisch \| The Python Quants GmbH

http://tpq.io \| team@tpq.io \|
http://twitter.com/dyjh \| http://pqp.io

**Python for Finance & Algorithmic Trading online trainings** \| http://training.tpq.io

**University Certificate Program in Python for Algorithmic Trading** \| http://certificate.tpq.io


