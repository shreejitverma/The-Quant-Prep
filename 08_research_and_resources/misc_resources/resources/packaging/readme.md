# Python Tools & Skills

**Distribution (Packaging)**

Dr. Yves J. Hilpisch | The Python Quants GmbH

Certificate Programs, November 2021

(short link to this Git repository: http://bit.ly/ts_pack)


<img src="http://hilpisch.com/tpq_viz.png" width=300px>


## Slides

You find the slides under:

https://certificate.tpq.io/tools_skills_dist.pdf

## pylib &mdash; Python Packaging

This is the rather simplistic packaging example from the Tools & Skills class of The Python Quants.

<br>

<img src="http://hilpisch.com/tpq_viz.png" width=300px>

## Docker Container

Using a Docker container should simplify working with the tools presented in this part of the class. You should clone the Git repository via

    git clone --depth=1 https://github.com/yhilpisch/packaging

Then navigate to the folder of the Git repository (`packaging`) and run:

    docker run -ti -h tools -p 9999:9999 -v $(pwd):/root/git ubuntu:latest /bin/bash

In the Docker container, to install the tools required execute:

    cd /root/git
    bash install.sh

## Package

The package contains a total of three simple Python files, two of which are in sub-folders/sub-packages, with a single function each.

## Training

In addition to the package files, the Git repository contains also other files used for the training session.

## Tutorial

### Environment

On the shell, create an environment with `conda`:

    conda create -n test-pylib python=3.9 ipython
    conda activate test-pylib

### Installation from Source

Clone the Github repository to your local working folder:

    git clone --depth=1 http://github.com/yhilpisch/packaging
    
Navigate to the repository folder and install the package:

    cd packaging
    python setup.py install

### Installation via pip

Alternatively, install the `pylib` package via

    pip install git+https://github.com/yhilpisch/packaging.git

### Installation via PyPi

You can also install the `pylib` package via

    pip install -i https://test.pypi.org/simple/ pylib
    
### First Steps
    
Start a Python interactive session session and e.g. execute:

    >>> import pylib
    >>> pylib.one(10)
    10
    >>> pylib.two(20)
    40
    >>> pylib.three(3)
    9

## Copyright

The material is copyright (c) Dr. Yves J. Hilpisch | The Python Quants GmbH. MIT License.

<img src="http://hilpisch.com/tpq_logo.png" width=250px>
