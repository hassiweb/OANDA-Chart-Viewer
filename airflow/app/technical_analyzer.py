# -*- coding: utf-8 -*-
"""
@author: (c)hassiweb (https://github.com/hassiweb)
License: MIT
"""

# Libraries that installation is needed
import configparser
from influxdb import DataFrameClient
import pandas as pd
import ta
import os


def analyze(data):
    
    # Moving average (5, 20, 75 days)
    sma5 = data['close'].rolling(window=5).mean()
    sma20 = data['close'].rolling(window=20).mean()
    sma75 = data['close'].rolling(window=75).mean()
    
    # MACD (12, 26 days)
    macd12_26 = ta.macd(data['close'], n_fast=12, n_slow=26)
    macd12_26_sig = ta.macd_signal(data['close'], n_fast=12, n_slow=26, n_sign=9)
            
    # Stochastics (%K: 5(not used), 9(not used), 14 day, %D: 3 days)
    stoch14_k = ta.stoch(data['high'], data['low'], data['close'], n=14)
    stoch14_d = ta.stoch_signal(data['high'], data['low'], data['close'], n=14, d_n=3)

    # Bollinger band (+3 sigma ~ -3 sigma)
    bb20_h1 = ta.bollinger_hband(data['close'], n=20, ndev=1)
    bb20_h2 = ta.bollinger_hband(data['close'], n=20, ndev=2)
    bb20_h3 = ta.bollinger_hband(data['close'], n=20, ndev=3)
    bb20_l1 = ta.bollinger_lband(data['close'], n=20, ndev=1)
    bb20_l2 = ta.bollinger_lband(data['close'], n=20, ndev=2)
    bb20_l3 = ta.bollinger_lband(data['close'], n=20, ndev=3)

    # Concatenate
    analysis = pd.concat([sma5, sma20, sma75, macd12_26, macd12_26_sig, stoch14_k, stoch14_d, bb20_h1, bb20_h2, bb20_h3, bb20_l1, bb20_l2, bb20_l3], axis=1)
    analysis.columns = ['5-Day SMA', '20-Day SMA', '75-Day SMA', 'MACD (12-16)', 'MACD Signal (12-26-9)', 'Stochastics %K (14 Day)', 'Stochastics %D (14 Day)', 'BB +1sigma', 'BB +2sigma', 'BB +3sigma', 'BB -1sigma', 'BB -2sigma', 'BB -3sigma']

    return analysis

    
if __name__ == '__main__':
    ## Read OANDA configurations
    config = configparser.ConfigParser()
    SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))

    influxdb_config = SCRIPT_PATH + '/influxdb.conf'
    if os.path.exists(influxdb_config):
        config.read(influxdb_config)
    else:
        exit("'influxdb.conf' is not found.")
    client = DataFrameClient(host=config['influxdb']['host'], \
                            port=config['influxdb']['port'], \
                            username=config['influxdb']['username'], \
                            password=config['influxdb']['password'], \
                            database=config['influxdb']['database'])
    
    oanda_config = SCRIPT_PATH + '/oanda.conf'
    if os.path.exists(oanda_config):
        config.read(oanda_config)
    else:
        exit("'oanda.conf' is not found.") 
    currency_pairs = config['oanda']['instruments'].replace(' ','').split(',')
    measurement = config['oanda']['granularity']
    
    for currency_pair in currency_pairs:
        print(currency_pair)
        query = 'SELECT * FROM ' + measurement + ' WHERE "currency_pair" = \'' + currency_pair +'\''
        results = client.query(query)
        analysis = analyze(results[measurement])
    
        ### Insert data
        client.write_points(analysis, measurement, {'currency_pair':currency_pair}, time_precision='s', database=config['influxdb']['database'])
    
    client.close()
        
    print('Done technical analysis')
    
