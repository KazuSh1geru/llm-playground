# function calling のデモを作成する

import json
from openai import OpenAI

client = OpenAI()

MODEL_TYPE = "gpt-4o"


def main(user_question: str):

    # 質問をOpenAIに送信する
    response = client.chat.completions.create(
        model=MODEL_TYPE,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_question},
        ],
        functions=[
            {
                "name": "get_weather",
                "description": "指定された場所と日付の天気を取得する",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "場所を指定する",
                        },
                        "date": {
                            "type": "string",
                            "description": "日付を指定する",
                        },
                    },
                    "required": ["location", "date"],
                },
            }
        ],
        function_call="auto",
    )
    # function_call を判定する
    function_call = response.choices[0].message.function_call
    if function_call.name == "get_weather":
        # 関数を呼び出す
        args = json.loads(function_call.arguments)
        location = args.get("location")
        date = args.get("date")
        weather = get_weather(location, date)
        return weather
    else:
        return response

def get_weather(location: str, date: str) -> str:
    # 天気を取得する
    return f"The weather in {location} on {date} is sunny."


if __name__ == "__main__":
    # ユーザーの質問を受け取る
    # user_question = input("質問を入力してください: ")
    user_question = "今日の東京の天気はどうですか？"
    response = main(user_question)
    print(response)
    # メッセージを表示する
    print(response.choices[0].message.content)
