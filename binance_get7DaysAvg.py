import requests
import time
import pandas as pds
import os
import datetime
import pytz
from dotenv import load_dotenv


def get_7DaysAvg_data():
    # 바이낸스 api 엔드포인트 & api키 설정하기
    BASE_URL = "https://api.binance.com/api/v3"
    api_key = os.getenv('API-KEY')
    secret_key = os.getenv('SECRET-KEY')
    print(api_key)
    todaysdate = time.localtime()
    print(todaysdate)

    now = datetime.datetime.now()

    # 현재 날짜와 시간을 UTC로 변환합니다.
    utc_now = now.astimezone(pytz.utc)

    # UTC 00:00의 시작과 종료 타임스탬프를 계산 - 여기서는 8일간의 데이터를 구해서, 직전 7일의 평균과 어제의 거래량을 비교할꺼니까, 8일간의 데이터가 필요함.
    end_of_day = datetime.datetime(utc_now.year, utc_now.month, utc_now.day, tzinfo=pytz.utc) - datetime.timedelta(days=1)
    start_of_day = end_of_day - datetime.timedelta(days=7)

    # 시작 타임스탬프와 종료 타임스탬프를 설정합니다.
    startTime = int(start_of_day.timestamp() * 1000)
    endTime = int(end_of_day.timestamp() * 1000)

    # 타임스탬프 출력
    print(f"startTime: {startTime}")
    print(f"endTime: {endTime}")

    # 모든 코인 티커 데이터 가져오기
    response = requests.get(f'{BASE_URL}/exchangeInfo')
    data = response.json()
    symbols = [symbol['symbol'] for symbol in data['symbols']]

    # OHLCV 데이터 저장할 리스트
    ohlcvs = []
    
    # USDT 페어의 데이터만 가져와서 데이터 processing 진행
    for symbol in symbols:
        if 'USDT' in symbol:
            quote_asset = symbol.split('USDT', 1)[1]
            params = {
                'symbol': symbol,
                'interval': '1d',
                'startTime': startTime,
                'endTime': endTime
            }

            headers = {
                'X-MBX-APIKEY': api_key
            }
            #ohlcv 데이터 담아주고
            response = requests.get(f'{BASE_URL}/klines', params=params, headers=headers)
            data = response.json()

            for item in data:
                ohlcvs.append({
                    'symbol': symbol,
                    'timestamp': item[0],
                    'open': item[1],
                    'high': item[2],
                    'low': item[3],
                    'close': item[4],
                    'volume': item[5]

                })
                print(item)
        else:
            continue
        df = pds.DataFrame(ohlcvs)
        df.to_csv("test.csv", index=False)    
    
    #for volumes
    coin_list = []
    coin_list_massive = []
    
    #for prices
    morethan20percentcoins = []
    morethan30percentcoins = []
    morethan50percentcoins = []
    morethan100percentcoins = []
    
    for symbol in symbols:
        coin_data = [item for item in ohlcvs if item['symbol'] == symbol]
        if len(coin_data) < 7:
            continue
        volumes = [float(item['volume']) for item in coin_data[-7:]]
        avg_volume = sum(volumes) / len(volumes)
        yesterday_volume = float(coin_data[-1]['volume'])
        
        if yesterday_volume >= (2 * avg_volume):
            coin_list.append(symbol)
        if yesterday_volume >= (3 * avg_volume):
            coin_list_massive.append(symbol)
            
        twodaysago_price = float(coin_data[-2]['close'])
        yesterday_prices = float(coin_data[-1]['close'])
        
        if twodaysago_price / yesterday_prices >= (1.05):
            morethan20percentcoins.append(symbol)
        if twodaysago_price / yesterday_prices >= (1.3):
            morethan30percentcoins.append(symbol)
        if twodaysago_price / yesterday_prices >= (1.5):
            morethan50percentcoins.append(symbol)
        if twodaysago_price / yesterday_prices >= (2):
            morethan100percentcoins.append(symbol)
            
    print(morethan20percentcoins)

#     print(yesterday_volume)
#     print(2 * avg_volume)
#     print(coin_list)
#     print(coin_list_massive)
            
get_7DaysAvg_data()