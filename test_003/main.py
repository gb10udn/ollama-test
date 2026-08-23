from .utils import fetch_weather, get_today
from ollama import chat
import json
import datetime
import os
from typing import Any
from collections.abc import Callable


# INITIAL_MESSAGE = '次の水曜に京都に行くんだけど、どんな服装でいったらいいかな？'  # INFO: 260823 fetch_weather に関数の説明を付けたら、"京都" -> "京都府" へ変換できた。
# INITIAL_MESSAGE = '次の土曜に皇居に行くんだけど、どんな服装でいったらいいかな？'  # INFO: 260823 皇居くらいならば、LLM 内の情報から変換できた。
INITIAL_MESSAGE = '次の木曜に新宿に行くんだけど、どんな服装でいったらいいかな？'  # INFO: 260823 新宿 -> 東京もできた。

messages = [
    {'role': 'system', 'content': '日付を判断するときは、必ず get_today ツールで現在の日付を確認してください。「明日」「明後日」「今週の水曜日」「来週の水曜日」などの相対的な日付表現は、現在の日付を基準に正確な日付へ変換してください。'},
    {'role': 'user', 'content': INITIAL_MESSAGE},    
]

tools: list[Callable[..., Any]] = [
    fetch_weather,
    get_today,
]

responses = []

while True:
    response = chat(
        model='qwen3:8b',
        messages=messages,
        tools=tools,
        think=True,
    )
    responses.append(response.model_dump())

    if not response.message.tool_calls:
        print(response.message.content)

        durations = [
            response['total_duration'] / 1_000_000_000
            for response in responses
        ]

        log = {
            'initial_message': INITIAL_MESSAGE,
            'final_message': response.message.model_dump(),
            'durations_sec': durations,
            'total_durations_sec': sum(durations),
            'responses': responses,
            'messages': messages,
        }
        filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'
        base_dir = './test_003/logs'
        os.makedirs(base_dir, exist_ok=True)

        with open(f'{base_dir}/{filename}', 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2, default=str)

        break

    for call in response.message.tool_calls:
        result: Any = ''
        if call.function.name == 'fetch_weather':
            result = fetch_weather(**call.function.arguments)

        elif call.function.name == 'get_today':
            result = get_today()

        messages.append({
            'role': 'tool',
            'tool_name': call.function.name,
            'content': str(result),
        })