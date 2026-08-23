from .utils import search_products
from ollama import chat
import json
import datetime
import os
from typing import Any
from collections.abc import Callable


# INITIAL_MESSAGE = '190 ℃で使える製品はどれだろう？'  # INFO: 260823 数値パラメタの大小関係を正しく押さえているようだ
INITIAL_MESSAGE = '水に浮く材料はどれだろう？'  # INFO: 260823 いくつか工夫をすると答えてくれた。


messages = [
    {'role': 'system', 'content': '物質の判断をするときは、必ず search_products ツールで情報を確認してください。'},
    {'role': 'user', 'content': INITIAL_MESSAGE},    
]

tools: list[Callable[..., Any]] = [
    search_products,
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
        base_dir = './test_004/logs'
        os.makedirs(base_dir, exist_ok=True)

        with open(f'{base_dir}/{filename}', 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2, default=str)

        break

    for call in response.message.tool_calls:
        result: Any = ''
        if call.function.name == 'search_products':
            result = search_products(**call.function.arguments)

        messages.append({
            'role': 'tool',
            'tool_name': call.function.name,
            'content': str(result),
        })