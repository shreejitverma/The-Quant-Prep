#
# mvportfolio
# Python Package for
# Mean-Variance Portfolio (MVP)
# Analysis & Management
#
# The Python Quants GmbH
#
import logging
import doctest
import numpy as np
import pandas as pd
import scipy.optimize as sco

logging.basicConfig(filename='mvp.log',
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    level=logging.INFO)


class MVPPortfolio:
    ''' Class to analyze and manage investment portfolios
    according to the Mean-Variance Portfolio (MVP) approach.
    '''

    def __init__(self, symbols, start, end, weights=None, source=None,
                 logger=False):
        ''' Initializes an instance of the class.

        :Parameters:
            symbols: list
                symbols that compose the portfolio
            start, end: str
                start and end date for data to be used
            weights: list
                weights for the different symbols; if None equal weighting
            source: str
                local or remote CSV data source

        :Examples:
            >>> from mvportfolio import MVPPortfolio
            >>> p = MVPPortfolio(['.SPX', '.VIX'], '2019-01-01', '2019-12-31')
            >>> print(p.returns.mean() * 252)
            .SPX    0.253435
            .VIX   -0.523875
            dtype: float64
            >>> print(p.returns.std() * 252 ** 0.5)
            .SPX    0.125065
            .VIX    1.188115
            dtype: float64
            >>>
        '''

        self.symbols = symbols
        self.nos = len(symbols)
        self.start = start
        self.end = end
        if weights is None:
            self.weights = self.nos * [1 / self.nos]
        else:
            self.weights = weights
        if source is None:
            self.source = 'http://hilpisch.com/pyalgo_eikon_eod_data.csv'
        self.logger = logger
        if self.logger:
            logging.info(self.symbols)
            logging.info(self.start)
            logging.info(self.end)
            logging.info(self.weights)
        self.prepare_data()

    def prepare_data(self):
        ''' Reads and prepares the data from a CSV source.
        '''
        self.raw = pd.read_csv(self.source, index_col=0, parse_dates=True)
        try:
            self.data = self.raw[self.symbols]
        except:
            logging.error('Symbol(s) not in data source: %s' % (self.symbols))
            raise ValueError('Symbol(s) not in data source.')
        try:
            self.data = self.data[(self.data.index >= self.start) & (
                self.data.index <= self.end)]
        except:
            logging.error('Dates not compatible: %s | %s' %
                          (self.start, self.end))
            raise ValueError('Dates not compatible with data source.')
        self.data.dropna(inplace=True)
        self.returns = np.log(self.data / self.data.shift(1))
        self.returns.dropna(inplace=True)

    def portfolio_return(self, weights=None):
        ''' Calculates the expected portfolio return.

        :Parameters:
            weights: list
                weights for the different symbols; if None original weights

        :Examples:
            >>> p = MVPPortfolio(['.SPX', '.VIX'], '2017-01-01', '2017-12-31')
            >>> p.portfolio_return(weights=[0.8, 0.2])
            0.10569545399055431
        '''
        if weights is not None:
            self.weights = weights
            if self.logger:
                logging.info(self.weights)
        return np.dot(self.returns.mean() * 252, self.weights)

    def portfolio_volatility(self, weights=None):
        ''' Calculates the expected portfolio volatility.

        :Parameters:
            weights: list
                weights for the different symbols; if None original weights

        :Examples:
            >>> p = MVPPortfolio(['.SPX', '.VIX'], '2019-01-01', '2019-12-31')
            >>> p.portfolio_volatility(weights=[0.8, 0.2])
            0.1634000261024319
            >>>
        '''
        if weights is not None:
            self.weights = weights
            if self.logger:
                logging.info(self.weights)
        return np.dot(self.weights, np.dot(self.returns.cov() * 252,
                                           self.weights)) ** 0.5

    def minimum_risk_portfolio(self, symbols=None):
        ''' Derives the portfolio weights that minimize the portfolio volatility.

        :Parameters:
            symbols: list
                symbols that compose the portfolio

        :Examples:
            >>> p = MVPPortfolio(['.SPX', '.VIX'], '2019-01-01', '2019-12-31')
            >>> opt = p.minimum_risk_portfolio()
            >>> print('Risk minimizing weights:', opt['x'])
            Risk minimizing weights: [0.91649696 0.08350304]
            >>>
        '''
        if symbols is not None:
            self.symbols = symbols
            self.nos = len(symbols)
            self.weights = self.nos * [1 / self.nos]
            if self.logger:
                logging.info(self.symbols)
            self.prepare_data()
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
        bounds = self.nos * [(0, 1)]
        opt = sco.minimize(self.portfolio_volatility, self.weights,
                           bounds=bounds, constraints=constraints)
        return opt


if __name__ == '__main__':
    doctest.testmod()
    symbols = ['.SPX', '.VIX', 'GLD']
    print(symbols)
    p = MVPPortfolio(symbols, '2019-01-01', '2019-12-31', logger=True)
    print(40 * '=')
    print('Annualized mean returns:')
    print(p.returns.mean() * 252)
    print(40 * '=')
    print('Annualized volatilities:')
    print(p.returns.std() * 252 ** 0.5)
    print(40 * '=')
    print('Correlations:\n', p.returns.corr())
    print(40 * '=')
    opt = p.minimum_risk_portfolio(['AAPL.O', 'MSFT.O'])
    print(p.symbols)
    print('Minimum risk porfolio  :', opt['x'].round(3))
