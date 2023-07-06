import pandas as pd
from datetime import datetime, timedelta

def get_data_filterbyVolume():
    df = pd.read_csv('ohlcv_data.csv')
    volume_data = df[['symbol', 'timestamp','volume']]

    now = datetime.now()
    one_week_ago = now - timedelta(days=7)

    #직전 7일까지만 필터링하기위한 변수선언
    filtered_data = volume_data[volume_data['timestamp'] >= one_week_ago.timestamp()]

    #코인들의 직전 7일의 거래량 평균치
    average_volume = filtered_data.groupby('symbol')['volume'].mean().reset_index()

    #오늘 거래량
    today = now.strftime("%Y%m%d")
    today_volume = volume_data[volume_data['timestamp'] >= now.timestamp()]

    #직전 7일의 거래량보다 오늘의 거래량이 2배 이상인 코인들
    selected_coins = today_volume.merge(average_volume, on = 'symbol')
    selected_coins = selected_coins[selected_coins['volume_x'] >= 2 * selected_coins['volume_y']]

    #배율 계산후 내림차순 정렬
    selected_coins['ratio'] = selected_coins['volume_x'] / selected_coins['volume_y']
    selected_coins = selected_coins.sort_values(by='ratio', ascending=False)

    filename = f'{today}_selected_coinsbyvolumedesc.csv'
    selected_coins.to_csv(filename, index = False)

