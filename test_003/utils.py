import pandas as pd
import requests
from typing import Literal
import datetime


Prefecture = Literal[
    '北海道',
    '青森県',
    '岩手県',
    '宮城県',
    '秋田県',
    '山形県',
    '福島県',
    '茨城県',
    '栃木県',
    '群馬県',
    '埼玉県',
    '千葉県',
    '東京都',
    '神奈川県',
    '新潟県',
    '富山県',
    '石川県',
    '福井県',
    '山梨県',
    '長野県',
    '岐阜県',
    '静岡県',
    '愛知県',
    '三重県',
    '滋賀県',
    '京都府',
    '大阪府',
    '兵庫県',
    '奈良県',
    '和歌山県',
    '鳥取県',
    '島根県',
    '岡山県',
    '広島県',
    '山口県',
    '徳島県',
    '香川県',
    '愛媛県',
    '高知県',
    '福岡県',
    '佐賀県',
    '長崎県',
    '熊本県',
    '大分県',
    '宮崎県',
    '鹿児島県',
    '沖縄県',
]


def _obtain_prefecture_code(prefecture: Prefecture) -> str | None:
    info = {   
        '北海道': '010100',
        '青森県': '020000',
        '岩手県': '030000',
        '宮城県': '040000',
        '秋田県': '050000',
        '山形県': '060000',
        '福島県': '070000',
        '茨城県': '080000',
        '栃木県': '090000',
        '群馬県': '100000',
        '埼玉県': '110000',
        '千葉県': '120000',
        '東京都': '130000',
        '神奈川県': '140000',
        '新潟県': '150000',
        '富山県': '160000',
        '石川県': '170000',
        '福井県': '180000',
        '山梨県': '190000',
        '長野県': '200000',
        '岐阜県': '210000',
        '静岡県': '220000',
        '愛知県': '230000',
        '三重県': '240000',
        '滋賀県': '250000',
        '京都府': '260000',
        '大阪府': '270000',
        '兵庫県': '280000',
        '奈良県': '290000',
        '和歌山県': '300000',
        '鳥取県': '310000',
        '島根県': '320000',
        '岡山県': '330000',
        '広島県': '340000',
        '山口県': '350000',
        '徳島県': '360000',
        '香川県': '370000',
        '愛媛県': '380000',
        '高知県': '390000',
        '福岡県': '400000',
        '佐賀県': '410000',
        '長崎県': '420000',
        '熊本県': '430000',
        '大分県': '440000',
        '宮崎県': '450000',
        '鹿児島県': '460100',
        '沖縄県': '471000',
    }
    return info.get(prefecture)


def _fetch_weather(area_code: str)-> pd.DataFrame:
    result = requests.get(f'https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json?').json()

    dts = result[1]['timeSeries'][0]['timeDefines']
    weather_codes = result[1]['timeSeries'][0]['areas'][0]['weatherCodes']
    pops = result[1]['timeSeries'][0]['areas'][0]['pops']
    max_temps = result[1]['timeSeries'][1]['areas'][0]['tempsMax']
    min_temps = result[1]['timeSeries'][1]['areas'][0]['tempsMin']

    df = pd.DataFrame({
        'datetime': dts,
        'weather_code': weather_codes,
        'pop': pops,
        'max_temp': max_temps,
        'min_temp': min_temps,
    })

    df['datetime'] = pd.to_datetime(df['datetime'])
    df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d')
    for col in ['pop', 'max_temp', 'min_temp']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df_ = pd.read_csv('./test_003/weather_codes.csv', dtype=str)
    result = pd.merge(
        left=df,
        right=df_,
        on='weather_code'
    )

    return result


def fetch_weather(prefecture: Prefecture) -> list[dict]:  # INFO: 260823 日本語でもいいので、関数の説明が入ると、京都 -> 京都府への変換ができた。Prefecture は効果が無かった。
    """
    47 都道府県名を渡して、１週間先の天気予報を得る関数。
    県や府を付ける必要がある点に注意。
    """
    code = _obtain_prefecture_code(prefecture)
    if code is None:
        return [{}]

    df = _fetch_weather(code)
    return df.to_dict(orient='records')


def get_today() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %A')