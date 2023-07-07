import requests
import time
import pandas as pds
import os
from datetime import datetime, timedelta 
import pytz
from dotenv import load_dotenv 
from binance.client import Client


def getsevendaysAverage():
    BASE_URL = "https://api.binance.com/api/v3"
    api_key = os.getenv('API-KEY')
    secret_key = os.getenv('SECRET-KEY')
    
    client = Client(api_key, secret_key)
    
    symbol = 'USDT'
    usdt_pairs=[]
    
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    
    for symbol_info in symbols:
        if symbol_info ['quoteAsset'] == symbol:
            usdt_pairs.append(symbol_info['symbol'])
    
    
    # 날짜 지정 - 어제 종가에 관련된 데이터는 빠져야하므로, 
    # 기간 설정을 9일 전~ 2일 전으로 해야 7일의 데이터 평균을 어제의 데이터가 noise로 포함되지 않고 구할 수 있다.
    now = datetime.now()
    start_of_previous_day = now - timedelta(days=7)
    end_of_previous_day = now - timedelta(days=1)

    # 시작 타임스탬프와 종료 타임스탬프를 설정합니다.
    startTime = int(start_of_previous_day.timestamp() * 1000)
    endTime = int(end_of_previous_day.timestamp() * 1000)

    klines = client.get_historical_klines(symbol=symbol_info['symbol'], interval=Client.KLINE_INTERVAL_1DAY, start_str=str(startTime), end_str=str(endTime))
    volumes = [float(kline[5]) for kline in klines]
    volume_mean_7days = sum(volumes) / len(volumes)
    print(klines)
    print(volumes)
    print(volume_mean_7days)
    
    
    # now = datetime.now()
    # start_of_previous_day = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=pytz.utc) - timedelta(days=9)
    # end_of_previous_day = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=pytz.utc) - timedelta(days=2)

    # # 시작 타임스탬프와 종료 타임스탬프를 설정합니다.
    # startTime = int(start_of_previous_day.timestamp() * 1000)
    # endTime = int(end_of_previous_day.timestamp() * 1000)

    # klines = client.get_historical_klines(symbol=symbol_info['symbol'], interval=Client.KLINE_INTERVAL_1DAY, start_str=str(startTime), end_str=str(endTime))
    # volumes = [float(kline[5]) for kline in klines]
    # volume_mean_7days = sum(volumes) / len(volumes)
    # print(volumes)
    # print(volume_mean_7days)

getsevendaysAverage()