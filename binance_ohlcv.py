import requests
import time
import pandas as pds
import os
import datetime
import pytz
from dotenv import load_dotenv

def get_ohlcv_data():
     #바이낸스 api 엔드포인트 & api키 설정하기
    BASE_URL = "https://api.binance.com/api/v3"
    api_key = os.getenv('API-KEY')
    secret_key = os.getenv('SECRET-KEY')
    print(api_key)
    todaysdate = time.localtime()
    print(todaysdate)

    now = datetime.datetime.now()

    # 현재 날짜와 시간을 UTC로 변환합니다.
    utc_now = now.astimezone(pytz.utc)

    # UTC 00:00의 시작과 종료 타임스탬프를 계산합니다.
    start_of_day = datetime.datetime(utc_now.year, utc_now.month, utc_now.day, tzinfo=pytz.utc)
    start_of_previous_day = start_of_day - datetime.timedelta(days = 1)
    end_of_previous_day = start_of_day - datetime.timedelta(seconds=1)

    # 시작 타임스탬프와 종료 타임스탬프를 설정합니다.
    startTime = int(start_of_previous_day.timestamp() * 1000)
    endTime = int(end_of_previous_day.timestamp() * 1000)

    # 타임스탬프 출력
    print(f"startTime: {startTime}")
    print(f"endTime: {endTime}")
    #모든 코인 데이터 가져오기
    response = requests.get(f'{BASE_URL}/exchangeInfo')
    data = response.json()
    symbols = [symbol['symbol']for symbol in data['symbols']]

    #OHLCV 데이터 저장할 리스트
    ohlcvs = []

    for symbol in symbols:
        if 'USDT' in symbol:
            quote_asset = symbol.split('USDT',1)[1]
            params = {
                'symbol' : symbol,
                'interval' : '1d',
                'startTime' : startTime,
                'endTime' : endTime
            }
            
            headers = {
                'X-MBX-APIKEY' : api_key
            }
            
            response = requests.get(f'{BASE_URL}/klines', params = params , headers = headers)
            data = response.json()
            
            for item in data:
                ohlcvs.append({
                    'symbol' : symbol,
                    'timestamp' : item[0],
                    'open' : item[1],
                    'high' : item[2],
                    'low' : item[3],
                    'close' : item[4],
                    'volume' : item[5]
                    
                })
                print(item)
        else:
            continue
    today = datetime.datetime.now().strftime("%Y%m%d")
    filename = f'{today}_ohlcv_data.csv'                
    df = pds.DataFrame(ohlcvs)
    df.to_csv(filename, index=False)    
           