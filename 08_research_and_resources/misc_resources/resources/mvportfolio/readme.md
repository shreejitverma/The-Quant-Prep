<img src="http://hilpisch.com/tpq_logo.png" alt="The Python Quants" width="35%" align="right" border="0"><br>

# Case Study

## Mean-Variance Portfolio Package

Dr. Yves J. Hilpisch

The Python Quants GmbH

<a href='http://tpq.io'>http://tpq.io</a> | <a href='mailto:training@tpq.io'>training@tpq.io</a>

## `mvportfolio`

`mvportfolio` is a simple Python package to analyze and manage investment portfolios according to the Mean-Variance Portfolio (MVP) theory.

<img src="http://hilpisch.com/images/finaince_visual_low.png" width="300px"> 

## Installation

### From Source 

Open a terminal an execute

    git clone http://github.com/yhilpisch/mvportfolio
    cd mvportfolio
    python setup.py install

### Via `pip` (from Github)

Open a terminal and execute

    pip install git+https://github.com/yhilpisch/mvportfolio.git

### Via `pip` (from PyPi)

Open a terminal and execute

    pip install --index-url https://test.pypi.org/simple/ mvportfolio

## First Steps

Some imports first.


```python
from pylab import plt
import mvportfolio as mvp
```

Second, an **instance** of the main class `MVPPortfolio`.


```python
p = mvp.MVPPortfolio(['.SPX', '.VIX'], '2017-1-1', '2018-6-30')
```

Third, some **statistics** for the equal weights portfolio.


```python
p.weights
```




    [0.5, 0.5]




```python
p.portfolio_return()
```




    0.1379220899637485




```python
p.portfolio_volatility()
```




    0.6462235282900842



Fourth, the **minimum risk portfolio weights**.


```python
opt = p.minimum_risk_portfolio()
```


```python
opt['x']
```




    array([0.93891629, 0.06108371])



## Copyright & License

&copy; The Python Quants GmbH | MIT License.
