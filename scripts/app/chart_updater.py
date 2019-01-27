# -*- coding: utf-8 -*-
"""
@author: (c)hassiweb (https://github.com/hassiweb)
License: MIT
"""

# Standard libraries
import datetime
import math

# Libraries that installation is needed
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from influxdb import InfluxDBClient
import configparser
import pytz
import argparse


def iso_to_dt(iso_str, tz):
    dt = None
    try:
        dt = datetime.datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S.%f000Z')
        dt = pytz.utc.localize(dt).astimezone(pytz.timezone(tz))
    except ValueError:
        try:
            dt = datetime.datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            dt = pytz.utc.localize(dt).astimezone(pytz.timezone(tz))
        except ValueError:
            try:
                dt = datetime.datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SZ')
                dt = pytz.utc.localize(dt).astimezone(pytz.timezone(tz))
            except ValueError:
                print('[iso_to_dt] convert error!')
                pass
            pass
        pass
    return dt



def delete_measurement(config, measurement, client):
    ## Reset measurement
    client.drop_measurement(measurement)



def reset_database(config, client):
    ## Reset database
    client.drop_database(config['influxdb']['database'])
    client.create_database(config['influxdb']['database'])



def store_candles(client, measurement, candles):
    ## Loop for the retrieved data
    for candle in candles['candles']:
        time = iso_to_dt(candle['time'], 'US/Eastern')
        json_body = [
                {
                        "measurement": measurement,
                        "tags": {
                                "currency_pair": candles['instrument']
                        },
                        "time": time,
                        "fields": {
                                "volume": float(candle['volume']),
                                "open": float(candle['mid']['o']),
                                "high": float(candle['mid']['h']),
                                "low": float(candle['mid']['l']),
                                "close": float(candle['mid']['c']),
                        }
                }
        ]   

        ### Insert data
        client.write_points(json_body, time_precision='s')



def get_candles(config, params, currency_pair):
    ## Retrieve using OANDA API
    api = API(access_token=config['oanda']['access_token'], environment=config['oanda']['environment'])
    request = instruments.InstrumentsCandles(instrument=currency_pair, params=params)
    candles = api.request(request)
    return candles



def get_granularity(granularity):
    if granularity == 'M1':
        gra_dt = datetime.timedelta(minutes=1)
    elif granularity == 'M5':
        gra_dt = datetime.timedelta(minutes=5)
    elif granularity == 'M10':
        gra_dt = datetime.timedelta(minutes=10)
    elif granularity == 'M15':
        gra_dt = datetime.timedelta(minutes=15)
    elif granularity == 'M30':
        gra_dt = datetime.timedelta(minutes=30)
    elif granularity == 'H1':
        gra_dt = datetime.timedelta(hours=1)
    elif granularity == 'H3':
        gra_dt = datetime.timedelta(hours=3)
    elif granularity == 'H6':
        gra_dt = datetime.timedelta(hours=6)
    elif granularity == 'H12':
        gra_dt = datetime.timedelta(hours=12)
    elif granularity == 'D':
        gra_dt = datetime.timedelta(days=1)
        
    return gra_dt



def init(config, client):
    
    # Reset measurement
    measurement = config['oanda']['granularity']
    delete_measurement(config, measurement, client)
    
    # Retrieve candle charts
    ## Set duration
    from_date = iso_to_dt(config['oanda']['from_date'], config['oanda']['timezone'])
    to_date = datetime.datetime.now(tz=pytz.timezone(config['oanda']['timezone']))
    gra_dt = get_granularity(config['oanda']['granularity'])
    currency_pairs = config['oanda']['instruments'].replace(' ','').split(',')
    
    max_count = 500 # This value depends on OANDA, and this is the maximum
    max_iter = math.ceil((to_date - from_date) / gra_dt / max_count)
    
    for currency_pair in currency_pairs:
        print(currency_pair)
        iter_from = from_date
        for iter in range(0, max_iter):
            iter_to = iter_from + gra_dt*max_count
            if iter_to > datetime.datetime.now(tz=pytz.timezone(config['oanda']['timezone'])):
                iter_to = datetime.datetime.now(tz=pytz.timezone(config['oanda']['timezone']))
            
            print(iter_from, iter_to)
            
            params = {
                "granularity":config['oanda']['granularity'],
                "from": iter_from.isoformat(),
                "to": iter_to.isoformat(),
#                "alignmentTimezone": config['oanda']['timezone']
            }
        
            ## Retrieve using OANDA API
            candles = get_candles(config, params, currency_pair)
        
            # Insert the retrieved candle data into InfluxDB
            store_candles(client, measurement, candles, )
        
            iter_from = iter_to + gra_dt



def update(config, client):
    # Retrieve candle charts
    ## Set duration
    from_date = datetime.datetime.now(tz=pytz.timezone(config['oanda']['timezone'])) - datetime.timedelta(days=7)
    to_date = datetime.datetime.now(tz=pytz.timezone(config['oanda']['timezone']))
    currency_pairs = config['oanda']['instruments'].replace(' ','').split(',')

    params = {
        "granularity":config['oanda']['granularity'],
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
#        "alignmentTimezone": config['oanda']['timezone']
    }

    measurement = config['oanda']['granularity']
    for currency_pair in currency_pairs:
        print(currency_pair)

        # Retrieve using OANDA API
        candles = get_candles(config, params, currency_pair)
    
        # Insert the retrieved candle data into InfluxDB
        store_candles(client, measurement, candles)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script retrieves FX candle charts using OANDA API, and then store the data into a remote InfluxDB.')
    parser.add_argument('-m', '--mode', help='"init" for initializing database. "update" for updating tickers.')
    args = parser.parse_args()

    # Read OANDA configurations
    config = configparser.ConfigParser()
    config.read('./oanda.conf')
    config.read('./influxdb.conf')

    # Create InfluxDB client object
    client = InfluxDBClient(host=config['influxdb']['host'], \
                            port=config['influxdb']['port'], \
                            username=config['influxdb']['username'], \
                            password=config['influxdb']['password'], \
                            database=config['influxdb']['database'])

#    reset_database(config, client)
#    init(config, client)
#    update(config, client)
    if args.mode == 'init':
        init(config, client)
        print("Done initialization")
    elif args.mode == 'update':
        update(config, client)
        print("Done update")


    client.close()

