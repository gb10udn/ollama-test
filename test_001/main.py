from ollama import chat
import datetime

def get_today() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %A')


with open('./test_001/garbage.md', encoding='utf-8') as f:
    text = f.read()


messages = [
    {'role': 'system', 'content': f'次の文章を参考にして下さい。{text}'},
    {'role': 'user', 'content': '次に燃えないゴミを出すのはいつだろうか？'},
]


response = chat(
    model='qwen3:8b',
    messages=messages,
    tools=[get_today],
)


messages.append(response.message)  # type: ignore[arg-type]


if response.message.tool_calls:
    call = response.message.tool_calls[0]
    result = get_today(**call.function.arguments)
    messages.append({
        'role'      : 'tool',
        'tool_name' : call.function.name,
        'content'   : str(result),
    })

    final_response = chat(
        model='qwen3:8b',
        messages=messages,
        tools=[get_today],
        think=True,
    )

    print(final_response.message.content)

else:
    print(response.message.content)  # INFO: 260821 tools 以外の回答を表示させる。