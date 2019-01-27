FROM python:3.7

RUN groupadd -r trader && useradd -r -g trader trader

WORKDIR /app
COPY app /app
COPY influxdb.conf /app
COPY oanda.conf /app

RUN pip install -r requirements.txt

USER trader

