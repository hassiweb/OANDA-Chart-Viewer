# OANDA Chart Viewer

![Viewer Image](https://github.com/hassiweb/OANDA-Chart-Viewer/blob/master/viewer_image.png)

## How to Install

```
$ git clone git@github.com:hassiweb/OANDA-Chart-Viewer.git
```

## How to Run

### 1. Configure your OANDA account information

You need to modify your OANDA account information and related information in `./scripts/oanda.conf`.  There is a sample file at `./scripts/oanda.conf.sample`.

Parameters are as follows:
- `account_id`: OANDA account ID
- `access_token`: Personal access token which is issued by OANDA to use thier APIs
- `environment`: "practice" or "live" (see [Interface OANDA’s REST-V20](https://oanda-api-v20.readthedocs.io/en/latest/oanda-api-v20.html#the-client) in detail)
- `from_date`: Initializing the database from this date, you should write in RFC3339 format
- `timezone`: TZ database name (see [List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) in detail)
- `granularity`: OANDA defined time granularity. (see [CandlestickGranularity](https://developer.oanda.com/rest-live-v20/instrument-df/) in detail)
- `instruments`: A string containing the base currency and quote currency delimited by a "\_". If you want several pairs, you can write multiple pairs delimited by a ",".

### 2. Configure your InfluxDB information (optional)

If you want to use a specific InfluxDB server, you can change the configuration for InfluxDB server in `./scripts/influxdb.conf`.

### 3. Run docker-compose.yml

Let's start the services by the following command.

```
$ docker-compose up -d
```

### 4. Initialize the database

To initialize the database, you need to run the following command.

```
$ sh initialize_charts.sh
```

### 5. Show candlestick charts

Let's open a browser and type "localhost:3000".  

You will see four pre-configured panels for "EUR_USD", "USD_JPY" and "EUR_JPY" pairs.  If you selected a different pair, you need to chnage settings.  

However, it is impossible to override the provisioned panels by an InfluxDB restriction.  Here available options will let you Copy JSON to Clipboard and/or Save JSON to file which can help you synchronize your dashboard changes back to the provisioning source (see [here](http://docs.grafana.org/administration/provisioning/) in detail).

### 6. Update charts (optional)

If you want to update charts, run the following command.

```
$ sh update_charts.sh
```

## Components
- InfluxDB

  InfluxDB is used to store candle data and technical analysis data.

- Grafana with [Grafana Candlestick Panel](https://github.com/ilgizar/ilgizar-candlestick-panel) [(c)ilgizar](https://github.com/ilgizar)

  Grafana is used to show the data.  "Grafana Candlestick Panel" enables to show candlesticks on the Grafana panel.

- Python using OANDA APIs and [Technical Analysis (TA) Library in Pyhton](https://github.com/bukosabino/ta) [(c)bukosabino](https://github.com/bukosabino)

  Currently, there are two scripts.  One is to retrieve candle data from OANDA.  The other is to calculate technical analysis indicators using technical analysis library "TA".

## License
MIT


## Contact
hassiweb: https://twitter.com/hassiweb
