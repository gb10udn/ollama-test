from ollama import chat
from devtools import pprint
import requests
import json
import os


JSON_PATH = './test_002/area_code.json'


def save_area_code() -> None:
    """
    気象庁から地域コードを取得して保存する関数。
    LLM に渡して、地域コードを取得する際に使用する想定。
    """
    areas = requests.get('https://www.jma.go.jp/bosai/common/const/area.json').json()

    with open(JSON_PATH, 'w') as f:
        json.dump(areas, f, indent=2, ensure_ascii=False)


####


if not os.path.exists(JSON_PATH):
    raise Exception(f'地域コードの JSON ファイルが存在しません。{JSON_PATH} を作成して下さい。')

with open(JSON_PATH, 'r') as f:
    area_json = json.load(f)

messages = [
    {'role': 'system', 'content': f'次の文章を参考にして下さい。{area_json}'},
    {'role': 'user', 'content': '京都市の地域コードを教えて。都道府県単位で良い。'},
]

response = chat(
    model='qwen3:8b',
    messages=messages,
)

pprint(response)