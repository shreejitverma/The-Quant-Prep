#
# IMPORTANT:
# THIS IS WORK IN PROGRESS
# AND FOR ILLUSTRATION ONLY
#
#
# Python Wrapper Class for
# EODHistoricalData API
# Visit https://bit.ly/eod_data
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
# Author: Michael Schwed
#
import os
import sys
import time
import json
import logging
import requests
import websocket 
import pandas as pd
import configparser
import datetime as dt

from io import StringIO
from threading import Thread

MISSING_ACCESS_TOKEN = "Cannot find access token. Please provide \
the token either as parameter in the class constructor or within a \
a configuration file and provide the file's path as parameter in the \
class constructor."

LOG_LEVELS = {'error': 40, 'warn': 30, 'info': 20, 'debug': 10}


class ServerError(Exception):
    pass

class fundamentals(object):
    """ A class to organize fundamental data.
    """

    # Class attributes

    def __init__(self, symbol_exchange, data, logger):
        self.symbol_exchange = symbol_exchange
        self.logger = logger
        self.data = data
        self.tables = dict()
        
        for key in data:
            if data[key]:
                self.__parse_data__(key, data[key])
        
    def get(self, table='keys'):
        if table=='keys':
            return self.tables.keys()
        elif table in self.tables:
            return self.tables[table]
        else:
            raise ValueError("table must be one of %s or 'keys'" % self.tables.keys())
        
    def __parse_data__(self, key, data):
        if key == 'General':
            if 'Listings' in data:
                self.tables['Listings'] = pd.DataFrame(data['Listings']).transpose()
                del data['Listings']
            if 'AddressData' in data:
                self.tables['AddressData'] = pd.Series(data['AddressData'])
                del data['AddressData']
            if 'Officers' in data:
                self.tables['Officers'] = pd.DataFrame(data['Officers']).transpose()
                del data['Officers']
            self.tables['General'] = pd.Series(data)
        elif key in ['Highlights', 'Valuation', 'SharesStats', 'Technicals', 'AnalystRatings']:
            self.tables[key] = pd.Series(data)
        elif key == 'SplitsDividends':
            if 'NumberDividendsByYear' in data:
                self.tables['NumberDividendsByYear'] = pd.DataFrame(data['NumberDividendsByYear']).transpose()
                del data['NumberDividendsByYear']
            self.tables['SplitsDividends'] = pd.Series(data)
        elif key == 'Holders':
            if 'Institutions' in data:
                self.tables['Holders_Institutions'] = pd.DataFrame(data['Institutions']).transpose()
                del data['Institutions']
            if 'Funds' in data:
                self.tables['Holders_Funds'] = pd.DataFrame(data['Funds']).transpose()
                del data['Funds']
        elif key == 'InsiderTransactions':
            self.tables['InsiderTransactions'] = pd.DataFrame(data).transpose()
        elif key == 'ESGScores':
            if 'ActivitiesInvolvement' in data:
                self.tables['ActivitiesInvolvement'] = pd.DataFrame(data['ActivitiesInvolvement']).transpose()
                del data['ActivitiesInvolvement']
            self.tables['ESGScores'] = pd.Series(data)
        elif key == 'outstandingShares':
            if 'annual' in data:
                self.tables['OutstandingShares_Annual'] = pd.DataFrame(data['annual']).transpose()
                del data['annual']
            if 'quarterly' in data:
                self.tables['OutstandingShares_Quarterly'] = pd.DataFrame(data['quarterly']).transpose()
                del data['quarterly']
        elif key == 'Earnings':
            if 'History' in data:
                df = pd.DataFrame(data['History']).transpose()
                self.tables['Earnings_History'] = df.drop(['date'], axis=1)
                del data['History']
            if 'Trend' in data:
                df = pd.DataFrame(data['Trend']).transpose()
                self.tables['Earnings_Trend'] = df.drop(['date'], axis=1)
                del data['Trend']
            if 'Annual' in data:
                df = pd.DataFrame(data['Annual']).transpose()
                self.tables['Earnings_Annual'] = df.drop(['date'], axis=1)
                del data['Annual']
        elif key == 'Financials':
            if 'Balance_Sheet' in data:
                if 'quarterly' in data['Balance_Sheet']:
                    df = pd.DataFrame(data['Balance_Sheet']['quarterly']).transpose()
                    self.tables['Balance_Sheet_Quarterly'] = df.drop(['date'], axis=1)
                    del data['Balance_Sheet']['quarterly']
                if 'yearly' in data['Balance_Sheet']:
                    df = pd.DataFrame(data['Balance_Sheet']['yearly']).transpose()
                    self.tables['Balance_Sheet_Yearly'] = df.drop(['date'], axis=1) 
                    del data['Balance_Sheet']['yearly']
                del data['Balance_Sheet']
            if 'Cash_Flow' in data:
                if 'quarterly' in data['Cash_Flow']:
                    df = pd.DataFrame(data['Cash_Flow']['quarterly']).transpose()
                    self.tables['Cash_Flow_Quarterly'] = df.drop(['date'], axis=1) 
                    del data['Cash_Flow']['quarterly']
                if 'yearly' in data['Cash_Flow']:
                    df =  pd.DataFrame(data['Cash_Flow']['yearly']).transpose()
                    self.tables['Cash_Flow_Yearly'] = df.drop(['date'], axis=1)
                    del data['Cash_Flow']['yearly']
                del data['Cash_Flow']
            if 'Income_Statement' in data:
                if 'quarterly' in data['Income_Statement']:
                    df = pd.DataFrame(data['Income_Statement']['quarterly']).transpose()
                    self.tables['Income_Statement_Quarterly'] = df.drop(['date'], axis=1)
                    del data['Income_Statement']['quarterly']
                if 'yearly' in data['Income_Statement']:
                    df = pd.DataFrame(data['Income_Statement']['yearly']).transpose()
                    self.tables['Income_Statement_Yearly'] = df.drop(['date'], axis=1)
                    del data['Income_Statement']['yearly']
        elif key == 'Components':
            self.tables['Components'] = pd.DataFrame(data).transpose()
        elif key == 'HistoricalTickerComponents':
            self.tables['HistoricalTickerComponents'] = pd.DataFrame(data).transpose()
        else:
            print('Found unknown key: ', key)
                
class tpqeod(object):
    """ A wrapper class for the EODHistoricalData API.
        Visit https://bit.ly/eod_data.
    """

    # Class attributes

    def __init__(self, api_key='', config_file='',
                 log_file='', log_level=''):
        """ Constructor

        Arguments:
        ===========

        api_key: string (default: ''),
            An access token for your EOD account.
        config_file: string (default: ''),
            Path of an optional configuration file.
        log_file: string (default: ''),
            Path of an optional log file. If not given (and not found in the
            optional configuration file), log messages are printed to stdout.
        log_level: string (default: ''),
            the log level. Must be one of 'error', 'warn', 'info' or 'debug'.
            If not given (and not found in the optional configuration file),
            'warn' is used.
        """

        self.logger = None
        self.config_file = ''
        self.session = None
        self.exchanges = None
        self.exchange_codes = None
        self.forex_socket = None
        self.crypto_socket = None
        self.trade_socket = None
        self.quote_socket = None
        self.forex_socket_closed = False
        self.crypto_socket_closed = False
        self.trade_socket_closed = False
        self.quote_socket_closed = False
        self.forex_data = dict()
        self.crypto_data = dict()
        self.quote_data = dict()
        self.trade_data = dict()
        self.available_fundamentals = dict()
        
        self.supported_indicators = ['splitadjusted', 'avgvol', 'avgvolccy', 'sma', 'ema',
                                     'wma', 'volatility', 'rsi', 'stddev', 'stochastic', 'stochrsi',
                                     'slope', 'dmi', 'adx', 'macd', 'atr', 'cci', 'sar', 'bbands']
        self.aux_parameter_for_indicators = {'splitadjusted': ['agg_period',],
                                             'avgvol': ['period'],
                                             'avgvolccy': ['period'],
                                             'sma': ['period'],
                                             'ema': ['period'],
                                             'wma': ['period'], 
                                             'volatility': ['period'],
                                             'rsi': ['period'],
                                             'stddev': ['period'],
                                             'stochastic': ['slow_dperiod', 'slow_kperiod', 'fast_kperiod'],
                                             'stochrsi': ['fast_dperiod', 'fast_kperiod'],
                                             'slope': ['period'],
                                             'dmi': ['period'],
                                             'adx': ['period'],
                                             'macd': ['slow_period', 'signal_period', 'fast_period'],
                                             'atr': ['period'],
                                             'cci': ['period'],
                                             'sar': ['acceleration', 'maximum'],
                                             'bbands': ['period']
                                            }
        
        self.parse_date_for_indicators = {'splitadjusted': [0,],
                                          'avgvol': [0,],
                                          'avgvolccy': [0,],
                                          'sma': [0,], 
                                          'ema': [0,],
                                          'wma': [0,],
                                          'volatility': [0,],
                                          'rsi': [0,],
                                          'stddev': [0,],
                                          'stochastic': [0,],
                                          'stochrsi': [0,],
                                          'slope': [0,],
                                          'dmi': [0,],
                                          'adx': [0,],
                                          'macd': [0,],
                                          'atr': [0,],
                                          'cci': [0,],
                                          'sar': [0,],
                                          'bbands': [0,]
                                         }
        
        self.para_default = { 'period': 50, 
                              'slow_dperiod': 3, 
                              'slow_kperiod': 3,
                              'fast_kperiod': 14,
                              'fast_dperiod': 14,
                              'slow_period': 26, 
                              'signal_period': 9,
                              'fast_period': 12,
                              'acceleration': 0.02,
                              'maximum': 0.2
                             }
        
        if api_key != '':
            self.api_key = api_key
        elif config_file != '':
            if os.path.isfile(config_file):
                self.config_file = config_file
            else:
                raise IOError('Can not find configiguration file: %s'
                              % config_file)
            try:
                self.api_key = self.__get_config_value__('EODHD',
                                                              'api_key')
            except:
                msg = 'Can not find api key in configuration file %s'
                raise ValueError(msg % self.config_file)
        else:
            raise ValueError(MISSING_ACCESS_TOKEN)

        if log_level != '':
            if log_level in LOG_LEVELS:
                log_level = LOG_LEVELS[log_level]
            else:
                raise ValueError('log_level must be one of %s'
                                 % LOG_LEVELS.keys())
        elif self.config_file != '':
            try:
                log_level = LOG_LEVELS[
                             self.__get_config_value__('EOD', 'log_level')]
            except:
                log_level = LOG_LEVELS['warn']
        else:
            log_level = LOG_LEVELS['warn']

        if log_file != '':
            log_path = log_file
        elif self.config_file != '':
            try:
                log_path = self.__get_config_value__('EOD', 'log_file')
            except:
                log_path = ''
        else:
            log_path = ''

        if log_path == '':
            form = '|%(levelname)s|%(asctime)s|%(message)s'
            logging.basicConfig(level=log_level, format=form)
        else:
            form = '|%(levelname)s|%(asctime)s|%(message)s'
            logging.basicConfig(filename=log_path, level=log_level,
                                format=form)
        self.logger = logging.getLogger('eodhd')

    def close_all(self):
        self.close_crypto_stream()
        
    def close_crypto_stream(self):
        if self.crypto_socket is not None and self.crypto_socket.connected:
            self.crypto_socket_closed = True
            
    def close_forex_stream(self):
        if self.forex_socket is not None and self.forex_socket.connected:
            self.forex_socket_closed = True
    
    def close_quote_stream(self):
        if self.quote_socket is not None and self.quote_socket.connected:
            self.quote_socket_closed = True
    
    def close_trade_stream(self):
        if self.trade_socket is not None and self.trade_socket.connected:
            self.trade_socket_closed = True
            
    def get_bond_fundamentals(self, symbol, as_json=False):
        symbol_exchange = '%s' % symbol  
        url = 'https://eodhd.com/api/bond-fundamentals/%s' % symbol_exchange
        
        params = {'api_token': self.api_key}
        req = requests.get(url, params=params)

        if req.status_code == requests.codes.ok:
            data = req.json()
            self.logger.debug(data)
            if as_json:
                return data
            df = pd.DataFrame(data)
            return df
        else:
            raise Exception(req.status_code, req.reason, url)    
           
    def get_calendar(self, event, symbol=None, exchange='US', start=None, stop=None):
        if event not in ('earnings', 'trends', 'ipos', 'splits'):
            raise ValueError('event must be one of "earnings", "trends", "ipos" or "splits"')
            
        parse_dates = {'earnings': [1,2],
                       'trends': [],
                       'splits': [1],
                       'ipos': [4]}
            
        url = "https://eodhd.com/api/calendar/%s" %event
        params = {'api_token': self.api_key}
        
        if start:
            if event == 'trends':
                self.logger.warn('start date is ignored for event "trends"')
            else:
                if isinstance(start, dt.datetime) or isinstance(start, dt.date):
                    params['from'] = start.strftime('%Y-%m-%d')
                else:
                    raise TypeError('start must be of type datetime')
        if stop:
            if event == 'trends':
                self.logger.warn('stop date is ignored for event "trends"')
            else:
                if isinstance(stop, dt.datetime) or isinstance(stop, dt.date):
                    params['to'] = stop.strftime('%Y-%m-%d')
                else:
                    raise TypeError('stop must be of type datetime')
        
        if symbol:
            if event in ('earnings', 'trends'):
                params['symbols']='%s.%s' %(symbol, exchange)
            else:
                self.logger.warn('symbol is ignored for events "ipos" and "splits"')
        
        elif event == 'trends':
            raise ValueError('Please specify a symbol for event "trends"')
        
        req = requests.get(url, params=params)
        if req.status_code == requests.codes.ok:
            if event == 'trends':
                text = req.text.split('\n')[1]
                text = text.replace('""', '"')
                data = json.loads(text[1:-1])
                self.logger.debug(data)
                df = pd.DataFrame(data)
                df['date'] = pd.to_datetime(df['date'])
            else:
                df = pd.read_csv(StringIO(req.text), skipfooter=0,
                                 parse_dates=parse_dates[event], index_col=None,
                                 engine='python')
            return df
        else:
            raise Exception(req.status_code, req.reason, url)    
            
    def get_crypto_fundamentals(self, symbol, as_json=False):
        symbol_exchange = '%s.CC' % symbol  
        url = 'https://eodhd.com/api/fundamentals/%s' % symbol_exchange
        
        params = {'api_token': self.api_key}
        req = requests.get(url, params=params)

        if req.status_code == requests.codes.ok:
            data = req.json()
            self.logger.debug(data)
            if as_json:
                return data
            funds = {**data['General'], **data['Statistics']}
            df = pd.DataFrame(funds, index=[funds['Name']])
            return df
        else:
            raise Exception(req.status_code, req.reason, url)    
        
            
    def get_eod_data(self, symbol, exchange='US', period='d', start=None,
                     stop=None, order='a'):
        symbol_exchange = '%s.%s' %(symbol, exchange)    
        url = 'https://eodhd.com/api/eod/%s' % symbol_exchange

        
        if period not in ['d', 'w', 'm']:
            raise ValueError("period must be one of 'd', 'w' or 'm'")
        if order not in ['a', 'd']:
            raise ValueError("order must be 'a' or 'd'")
            
        params = {'api_token': self.api_key,
                  'period': period,
                  'order': order}
        
        if start:
            if isinstance(start, dt.datetime) or isinstance(start, dt.date):
                params['from'] = start.strftime('%Y-%m-%d')
            else:
                raise TypeError('start must be of type datetime')
        if stop:
            if isinstance(stop, dt.datetime) or isinstance(stop, dt.date):
                params['to'] = stop.strftime('%Y-%m-%d')
            else:
                raise TypeError('stop must be of type datetime')
            
        req = requests.get(url, params=params)
        if req.status_code == requests.codes.ok:
            df = pd.read_csv(StringIO(req.text), skipfooter=0,
                             parse_dates=[0], index_col=0, engine='python')
            return df
        else:
            raise Exception(req.status_code, req.reason, url)
            
    def get_exchanges(self):
        if self.exchanges == None:
            url = 'https://eodhd.com/api/exchanges-list'
            params = {"api_token": self.api_key}
            req = requests.get(url, params=params)
            if req.status_code == requests.codes.ok:
                self.exchanges = req.json()
                self.exchanges_codes = [ex['Code'] for ex in self.exchanges]
                
            else:
                raise Exception(req.status_code, req.reason, url)

        return self.exchanges
    
    def get_exchange_codes(self):
        if self.exchange_codes == None:
            self.get_exchanges()
            self.exchange_codes = [ex['Code'] for ex in self.exchanges]
         
        return self.exchange_codes
    
    def get_exchange_data(self, ex_code):
        if self.exchanges == None:
            self.get_exchanges()
        if ex_code == 'All':
            return pd.DataFrame(self.exchanges)    
        for ex in self.exchanges:
            if ex['Code'] == ex_code:
                return pd.DataFrame(ex, index = [ex['Code']])
        return {}
    
    def get_fundamentals(self, symbol, exchange='US', table='keys', as_json=False):
        symbol_exchange = '%s.%s' % (symbol, exchange)
        if symbol_exchange in self.available_fundamentals:
            if as_json:
                data = self.available_fundamentals[symbol_exchange].data
            funds = self.available_fundamentals[symbol_exchange]
        else:    
            url = 'https://eodhd.com/api/fundamentals/%s' % symbol_exchange
            params = {'api_token': self.api_key}
            req = requests.get(url, params=params)

            if req.status_code == requests.codes.ok:
                data = req.json()
                self.logger.debug(data)
                funds = fundamentals(symbol_exchange, data, self.logger)
                self.available_fundamentals[symbol_exchange] = funds
            else:
                raise Exception(req.status_code, req.reason, url)   
        if as_json:
            return data
        else:
            return funds.get(table)
    
    def get_hist_intraday_data(self, symbol, exchange='US',
                               period='1m', start=None, stop=None):
        symbol_exchange = '%s.%s' %(symbol, exchange)    
        url = 'https://eodhd.com/api/intraday/%s' % symbol_exchange

        if period not in ['1m', '5m', '1h']:
            raise ValueError("period must be one of '1m', '5m' or '1h'")
      
        if self.api_key == '650d4c607ae182.35413180':    
            params = {'api_token': 'demo',
                      'period': period}
        else:    
            params = {'api_token': self.api_key,
                      'period': period}
            
        if start:
            if isinstance(start, dt.datetime): 
                params['from'] = int(round(start.timestamp()))
            elif isinstance(start, dt.date):
                params['from'] = int(round(dt.datetime.combine(start, dt.time()).timestamp()))
            else:
                raise TypeError('start must be of type datetime')

        if stop:
            if isinstance(stop, dt.datetime):
                params['to'] = int(round(stop.timestamp()))
            elif isinstance(stop, dt.date):
                params['to'] = int(round(dt.datetime.combine(stop, dt.time()).timestamp()))
            else:
                raise TypeError('stop must be of type datetime')
            
        req = requests.get(url, params=params)
       

        if req.status_code == requests.codes.ok:
            df = pd.read_csv(StringIO(req.text), skipfooter=0, index_col=2, engine='python')
            df = df.drop(columns=['Timestamp'])
            return df
        else:
            raise Exception(req.status_code, req.reason, url)

    def get_hist_market_cap(self, symbol, exchange='US', start=None, stop=None):    
        symbol_exchange = '%s.%s' %(symbol, exchange)    
        url = 'https://eodhd.com/api/historical-market-cap/%s' % symbol_exchange
    
        if self.api_key == '650d4c607ae182.35413180':
            params = {'api_token': 'demo'}
        else:
            params = {'api_token': self.api_key}
        
        if start:
            if isinstance(start, dt.datetime) or isinstance(start, dt.date):
                params['from'] = start.strftime('%Y-%m-%d')
            else:
                raise TypeError('start must be of type datetime')
        if stop:
            if isinstance(stop, dt.datetime) or isinstance(stop, dt.date):
                params['to'] = stop.strftime('%Y-%m-%d')
            else:
                raise TypeError('stop must be of type datetime')
            
        self.logger.info('Sending request to %s' %url)
        self.logger.info('Params: %s' %params)
        req = requests.get(url, params=params)

        if req.status_code == requests.codes.ok:
            data = req.json()
            self.logger.debug(data)
            df = pd.DataFrame(data).transpose()
            df=df.set_index('date')
            return df
        else:
            raise Exception(req.status_code, req.reason, url)
    
    def get_hist_dividends(self, symbol, exchange='US', start=None, stop=None):    
        symbol_exchange = '%s.%s' %(symbol, exchange)    
        url = 'https://eodhd.com/api/div/%s' % symbol_exchange
    
        if self.api_key == '650d4c607ae182.35413180':
            params = {'api_token': 'demo'}
        else:
            params = {'api_token': self.api_key}
        
        if start:
            if isinstance(start, dt.datetime) or isinstance(start, dt.date):
                params['from'] = start.strftime('%Y-%m-%d')
            else:
                raise TypeError('start must be of type datetime')
        if stop:
            if isinstance(stop, dt.datetime) or isinstance(stop, dt.date):
                params['to'] = stop.strftime('%Y-%m-%d')
            else:
                raise TypeError('stop must be of type datetime')
            
        req = requests.get(url, params=params)

        if req.status_code == requests.codes.ok:
            df = pd.read_csv(StringIO(req.text), skipfooter=0,
                             parse_dates=[0], index_col=0, engine='python')
            return df
        else:
            raise Exception(req.status_code, req.reason, url)
            
    
    def get_hist_splits(self, symbol, exchange='US', start=None, stop=None):    
        symbol_exchange = '%s.%s' %(symbol, exchange)    
        url = 'https://eodhd.com/api/splits/%s' % symbol_exchange
    
        if self.api_key == '650d4c607ae182.35413180':
            params = {'api_token': 'demo'}
        else:
            params = {'api_token': self.api_key}
        
        if start:
            if isinstance(start, dt.datetime) or isinstance(start, dt.date):
                params['from'] = start.strftime('%Y-%m-%d')
            else:
                raise TypeError('start must be of type datetime')
        if stop:
            if isinstance(stop, dt.datetime) or isinstance(stop, dt.date):
                params['to'] = stop.strftime('%Y-%m-%d')
            else:
                raise TypeError('stop must be of type datetime')
            
        req = requests.get(url, params=params)

        if req.status_code == requests.codes.ok:
            df = pd.read_csv(StringIO(req.text), skipfooter=0,
                             parse_dates=[0], index_col=0, engine='python')
            return df
        else:
            raise Exception(req.status_code, req.reason, url)
        
    def get_insider_transactions(self, symbol=None, exchange='US', start=None,
                                 stop=None, limit=None):
        url = 'https://eodhd.com/api/insider-transactions'
        params = {'api_token': self.api_key}
            
        if symbol:
            params['code'] = '%s.%s' %(symbol, exchange)    
        
        if start:
            if isinstance(start, dt.datetime) or isinstance(start, dt.date):
                params['from'] = start.strftime('%Y-%m-%d')
            else:
                raise TypeError('start must be of type datetime')
        if stop:
            if isinstance(stop, dt.datetime) or isinstance(stop, dt.date):
                params['to'] = stop.strftime('%Y-%m-%d')
            else:
                raise TypeError('stop must be of type datetime')
                
        if limit:
            try:
                params['limit'] = int(limit)
            except:
                raise TypeError('limit must be an integer')
            
        req = requests.get(url, params=params)

        if req.status_code == requests.codes.ok:
            data = req.json()
            self.logger.debug(data)
            df = pd.DataFrame(data)
            return df
        else:
            raise Exception(req.status_code, req.reason, url)
            
            
    def get_live_crypto_data(self, symbol):
        self.logger.info('Start streaming data for %s' %symbol)
        self.__stream_crypto_data__(symbol)
        
    def get_live_forex_data(self, symbol):
        self.logger.info('Start streaming data for %s' %symbol)
        self.__stream_forex_data__(symbol)
        
    def get_live_quote_data(self, symbol):
        self.logger.info('Start streaming data for %s' %symbol)
        self.__stream_quote_data__(symbol)
        
    def get_live_trade_data(self, symbol):
        self.logger.info('Start streaming data for %s' %symbol)
        self.__stream_trade_data__(symbol)
        
    def get_technical_indicator(self, symbol, exchange='US',  **kwargs):
        symbol_exchange = '%s.%s' %(symbol, exchange)  
        url = 'https://eodhd.com/api/technical/%s' % symbol_exchange
        params = {'api_token': self.api_key}
        
        if 'start' in kwargs:
            start = kwargs['start']
            if isinstance(start, dt.datetime) or isinstance(start, dt.date):
                params['from'] = start.strftime('%Y-%m-%d')
            else:
                raise TypeError('start must be of type datetime')
        if 'stop' in kwargs:
            stop = kwargs['stop']
            if isinstance(stop, dt.datetime) or isinstance(stop, dt.date):
                params['to'] = stop.strftime('%Y-%m-%d')
            else:
                raise TypeError('stop must be of type datetime')
                
        if 'order' in kwargs:
            order = kwargs['order']
            if order not in ['d', 'a']:
                raise ValueError("order must be 'a' or 'd'")
            else:
                params['order'] = order
                
        if 'function' not in kwargs:
            raise TypeError('keyword argument function not given')
        else:
            function = kwargs['function']
            if function not in self.supported_indicators:
                raise ValueError('function must be one of %s' % self.supported_indicators)
            else:
                params['function'] =  function
                
        for para in self.aux_parameter_for_indicators[function]:
            if para in kwargs:
                res, res_val = self.__check_para__(para, kwargs[para])
                
                if res != 'ok':
                    self.logger.warn(res)
                params[para] = res_val
                    
        req = requests.get(url, params=params)

        if req.status_code == requests.codes.ok:
            df = pd.read_csv(StringIO(req.text), skipfooter=0,
                             parse_dates=self.parse_date_for_indicators[function],
                             index_col=0, engine='python')
            return df
        else:
            raise Exception(req.status_code, req.reason, url)
                
        
        
    def get_tick_data(self, symbol, limit = None, start = None, stop = None):     
        params = {"api_token": self.api_key, "s":symbol}  
        
        self.logger.debug("start: %s" %start)
        self.logger.debug("stop: %s" %stop)
            
        if start:
            if isinstance(start, dt.datetime): 
                params['from'] = int(round(start.timestamp()))
            elif isinstance(start, dt.date):
                params['from'] = int(round(dt.datetime.combine(start, dt.time()).timestamp()))
            else:
                raise TypeError('start must be of type datetime')

        if stop:
            if isinstance(stop, dt.datetime):
                params['to'] = int(round(stop.timestamp()))
            elif isinstance(stop, dt.date):
                params['to'] = int(round(dt.datetime.combine(stop, dt.time()).timestamp()))
            else:
                raise TypeError('stop must be of type datetime')
                
        if limit:
            try:
                limit = int(limit)
                params['limit'] = limit
            except:
                raise TypeError('limit must be of type int')
                
        url = 'https://eodhd.com/api/ticks'
        
        self.logger.debug('Sending tick request: URL: %s, Parameter: %s' % (url, params))
        r = requests.get(url, params=params)
        data = r.json()
        self.logger.debug(data)
        if r.status_code == requests.codes.ok:
            if len(data) > 0:
                date = pd.to_datetime(data['ts'], unit='ms')
                df = pd.DataFrame(data,columns = ['ex', 'mkt', 'price', 'seq',
                                                  'shares', 'sl', 'sub_mkt'], 
                                  index=[date])
            else:
                df = pd.DataFrame()
            return df
        else:
            raise Exception(r.status_code, r.reason, url)
            
    def get_ticker_list(self, exchange):
        url = 'https://eodhd.com/api/exchange-symbol-list/%s' % exchange
        params = {"api_token": self.api_key, 
                  "fmt": "json" 
                 } 
        self.logger.debug('Sending ticker request: URL: %s, Parameter: %s' % (url, params))
        r = requests.get(url, params=params)
        data = r.json()
        self.logger.debug(data)
        
        if r.status_code == requests.codes.ok:
            if len(data) > 0:
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame()
            return df
        else:
            raise Exception(r.status_code, r.reason, url)
            
        
            
    def search(self, query, limit=15, asset_type='all'):
        if query == '':
            raise ValueError('Please provide a query string')
            
        try:
            limit = int(limit)
        except:
            raise TypeError('limit must be an integer.')
        if limit > 500:
            self.logger.warn('limit value of %s exceeds max. value of 500, taking that value instead.' % limit)
        
        if asset_type not in ['all', 'stock', 'etf', 'fund', 'bond', 'index', 'crypto']:
            raise ValueError("asset_type must be one of 'all', 'stock', \
             'etf', 'fund', 'bond', 'index' or 'crypto'")
        params = {"api_token": self.api_key,
                  "limit": limit,
                  "type": asset_type}
        
        url= 'https://eodhd.com/api/search/%s' % query
        self.logger.debug('Sending search request: URL: %s, Parameter: %s' % (url, params))
        r = requests.get(url, params=params)
        if r.status_code == requests.codes.ok:
            data = r.json()
            self.logger.debug(data)
        else:
            raise Exception(r.status_code, r.reason, url)
            
        return pd.DataFrame(data)
            
        
            
    def __check_para__(self, para, value):
        if para == 'agg_period':
            if value not in ['d', 'w', 'm']:
                raise ValueError("agg_period must be one of 'd', 'w' or 'm'")
            else:
                return 'ok', value
        elif para in ['period', 'slow_dperiod', 'fast_dperiod', 'slow_kperiod',
                      'fast_kperiod', 'slow_period', 'signal_period', 'fast_period']:
            try:
                value = int(value)
            except:
                raise TypeError('period must be an integer')
            if value > 100000 or value < 2:
                templ = "%s must lay between 2 and 100000, taking the default value of %s instead"
                return templ % (para, self.para_default[para]), self.para_default[para]
            else:
                return 'ok', value
        elif para in ['acceleration', 'maximum']:
            try:
                value = float(value)
                return 'ok', value
            except:
                raise TypeError('%s must be a float' %para)
            
        else:
            raise TypeError("Unknown parameter %s" %para)
            
    def __connect_forex_socket__(self):
        if self.api_key == '650d4c607ae182.35413180':
            url = "ws://ws.eodhistoricaldata.com/ws/forex?api_token=demo"
        else:
            url = "ws://ws.eodhistoricaldata.com/ws/forex?api_token=%s" % self.api_key
        self.forex_socket = websocket.create_connection(url)
        while not self.forex_socket.connected:
            time.sleep(1)
            self.logger.info('Waiting for connection in __connect')
        self.logger.info('Socket created')
        
        self.logger.info(self.forex_socket.recv())
        
        while not self.forex_socket_closed:
            msg = self.forex_socket.recv()
            data = json.loads(msg)
            self.logger.debug(data)
            
            if 's' in data:
                symbol = data['s']
                date = pd.to_datetime(int(data['t']), unit='ms')
                temp_data = pd.DataFrame(data, columns=['s', 'a', 'b', 'dc', 'dd', 'ppms'],
                                         index=[date])
                if symbol not in self.forex_data:
                    self.forex_data[symbol] = temp_data
                else:
                    self.forex_data[symbol] = pd.concat([self.forex_data[symbol], temp_data])
            else:
                self.logger.error(data)
        self.forex_socket.close()
        self.forex_socket_closed = False
        self.forex_socket = None
           
    def __connect_crypto_socket__(self):
        if self.api_key == '650d4c607ae182.35413180':
            url = "ws://ws.eodhistoricaldata.com/ws/crypto?api_token=demo"
        else:
            url = "ws://ws.eodhistoricaldata.com/ws/crypto?api_token=%s" % self.api_key
        self.crypto_socket = websocket.create_connection(url)
        while not self.crypto_socket.connected:
            time.sleep(1)
            self.logger.info('Waiting for connection in __connect')
        self.logger.info('Socket created')
    
        self.logger.info(self.crypto_socket.recv())
        
        while not self.crypto_socket_closed:
            msg = self.crypto_socket.recv()
            data = json.loads(msg)
            self.logger.debug(data)
            
            if 's' in data:
                symbol = data['s']
                date = pd.to_datetime(int(data['t']), unit='ms')
                temp_data = pd.DataFrame(data, columns=['s', 'p', 'q', 'dc', 'dd'],
                                         index=[date])
                if symbol not in self.crypto_data:
                    self.crypto_data[symbol] = temp_data
                else:
                    self.crypto_data[symbol] = pd.concat([self.crypto_data[symbol], temp_data])  
            else:
                self.logger.error(data)
        self.crypto_socket.close()
        self.crypto_socket_closed = False
        self.crypto_socket = None
    
    def __connect_quote_socket__(self):
        if self.api_key == '650d4c607ae182.35413180':
            url = "ws://ws.eodhistoricaldata.com/ws/us-quote?api_token=demo"
        else:
            url = "ws://ws.eodhistoricaldata.com/ws/us-quote?api_token=%s" % self.api_key
        self.quote_socket = websocket.create_connection(url)
        while not self.quote_socket.connected:
            time.sleep(1)
            self.logger.info('Waiting for connection in __connect')
        self.logger.info('Socket created')
    
        self.logger.info(self.quote_socket.recv())
        
        while not self.quote_socket_closed:
            msg = self.quote_socket.recv()
            data = json.loads(msg)
            self.logger.debug(data)
            
            if 's' in data:
                symbol = data['s']
                date = pd.to_datetime(int(data['t']), unit='ms')
                temp_data = pd.DataFrame(data, columns=['s', 'ap', 'bp', 'as', 'bs'],
                                         index=[date])
                if symbol not in self.quote_data:
                    self.quote_data[symbol] = temp_data
                else:
                    self.quote_data[symbol] = pd.concat([self.quote_data[symbol], temp_data])  
            else:
                self.logger.error(data)
        self.quote_socket.close()
        self.quote_socket_closed = False
        self.quote_socket = None
            
    def __connect_trade_socket__(self):
        if self.api_key == '650d4c607ae182.35413180':
            url = "ws://ws.eodhistoricaldata.com/ws/us?api_token=demo"
        else:
            url = "ws://ws.eodhistoricaldata.com/ws/us?api_token=%s" % self.api_key
        self.trade_socket = websocket.create_connection(url)
        while not self.trade_socket.connected:
            time.sleep(1)
            self.logger.info('Waiting for connection in __connect')
        self.logger.info('Socket created')
    
        self.logger.info(self.trade_socket.recv())
        
        while not self.trade_socket_closed:
            msg = self.trade_socket.recv()
            data = json.loads(msg)
            self.logger.debug(data)
            
            if 's' in data:
                symbol = data['s']
                date = pd.to_datetime(int(data['t']), unit='ms')
                data['c'] = str(data['c'])
                temp_data = pd.DataFrame(data, columns=['s', 'p', 'c', 'v', 'dp', 'ms'],
                                         index=[date])
                if symbol not in self.trade_data:
                    self.trade_data[symbol] = temp_data
                else:
                    self.trade_data[symbol] = pd.concat([self.trade_data[symbol], temp_data])  
            else:
                self.logger.error(data)
        self.trade_socket.close()
        self.trade_socket_closed = False
        self.trade_socket = None
        
    def __stream_crypto_data__(self, symbol):
        if not self.crypto_socket:
            self.logger.info('Creating socket')
            thread = Thread(target=self.__connect_crypto_socket__)
            thread.start()   
        else:
            self.logger.info('Socket available')
        while self.crypto_socket is None:
            self.logger.info('Waiting for socket')
            time.sleep(1)
        while not self.crypto_socket.connected:
            self.logger.info('Waiting for connection')
            time.sleep(1)
        payload = '{"action": "subscribe", "symbols": "%s"}' % symbol
        self.crypto_socket.send(payload)
        self.logger.info('Subscribing %s' %symbol)
            
    def __stream_forex_data__(self, symbol):
        if not self.forex_socket:
            self.logger.info('Creating socket')
            thread = Thread(target=self.__connect_forex_socket__)
            thread.start()
        else:
            self.logger.info('Socket available')
        while self.forex_socket is None:
            self.logger.info('Waiting for socket')
            time.sleep(1)
        while not self.forex_socket.connected:
            self.logger.info('Waiting for connection')
            time.sleep(1)
        payload = '{"action": "subscribe", "symbols": "%s"}' % symbol
        self.forex_socket.send(payload)
        self.logger.info('Subscribing %s' %symbol)
        
    def __stream_quote_data__(self, symbol):
        if not self.quote_socket:
            self.logger.info('Creating socket')
            thread = Thread(target=self.__connect_quote_socket__)
            thread.start()
        else:
            self.logger.info('Socket available')
        while self.quote_socket is None:
            self.logger.info('Waiting for socket')
            time.sleep(1)
        while not self.quote_socket.connected:
            self.logger.info('Waiting for connection')
            time.sleep(1)
        payload = '{"action": "subscribe", "symbols": "%s"}' % symbol
        self.quote_socket.send(payload)
        self.logger.info('Subscribing %s' %symbol)
        
    def __stream_trade_data__(self, symbol):
        if not self.trade_socket:
            self.logger.info('Creating socket')
            thread = Thread(target=self.__connect_trade_socket__)
            thread.start()
        else:
            self.logger.info('Socket available')
        while self.trade_socket is None:
            self.logger.info('Waiting for socket')
            time.sleep(1)
        while not self.trade_socket.connected:
            self.logger.info('Waiting for connection')
            time.sleep(1)
        payload = '{"action": "subscribe", "symbols": "%s"}' % symbol
        self.trade_socket.send(payload)
        self.logger.info('Subscribing %s' %symbol)
 
