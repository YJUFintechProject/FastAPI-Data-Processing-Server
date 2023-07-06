## main ohlcv data getttt ##
import requests
import time
import pandas as pds
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
from binance_ohlcv import get_ohlcv_data
import schedule
from binance_filterdatabyvolume import get_data_filterbyVolume

load_dotenv()

#서버 실행 시간과 지역을 설정
server_timezone = pytz.timezone('Asia/Seoul')
print(server_timezone)
get_ohlcv_data()

while True:
    server_time = datetime.now(server_timezone)
    
    if server_time.hour == 9 and server_time.minute == 0:
        ohlcvs = get_ohlcv_data()
        get_data_filterbyVolume()
    
    time.sleep(60)