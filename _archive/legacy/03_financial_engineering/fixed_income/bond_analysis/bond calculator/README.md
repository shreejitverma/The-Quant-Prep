# bond-calculator
Computes bond YTM, price, duration, or convexity.
Run from a Command Line Interface (CLI).

## Installation
Installation is simply downloading the code from GitHub. Enter the following at a terminal prompt to install in your home directory:
```bash
$ cd
$ git clone https://github.com/shreysrins/bond-calculator.git
```

## Dependencies
This code was developed and tested in Python 3.7.
The current `requirements.txt` needs Python 3.8 or 3.9: NumPy 1.22 dropped Python 3.7 and SciPy 1.6 supports only Python 3.7 to 3.9.
You can check your version of Python with the following terminal command:
```bash
$ python3 --version
```

Install all dependencies by opening a terminal and running:
```bash
$ pip3 install -r requirements.txt
```
The version constraints for pyfiglet, NumPy and SciPy live in `requirements.txt`.

## Usage
Open a terminal and navigate to the directory in which this repository is stored. If you installed in your home directory, this is done with:
```bash
$ cd ~/bond-calculator/
```
The command to run the calculator is:
```bash
$ python3 bond_calc.py
```
All instructions and prompts are given in the terminal itself.

## Updating
To check for and install updates: open a terminal, navigate to the directory in which this repository is stored, and run the `git pull` command. If you installed in your home directory, this is done with:
```bash
$ cd ~/bond-calculator/
$ git status
$ git pull
```
