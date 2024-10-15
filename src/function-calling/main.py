# function calling のデモを作成する

import json
from openai import OpenAI

client = OpenAI()

MODEL_TYPE = "gpt-4o"

FUNCTIONS_LIST = [
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
    },
    {
        "name": "write_spreadsheet",
        "description": "スプレッドシートにデータを書き込む",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "データを指定する",
                },
                "sheet_name": {
                    "type": "string",
                    "description": "シート名を指定する",
                    "default": "Sheet1",
                },
            },
            "required": ["data", "sheet_name"],
        },
    },
]


def main(user_question: str):

    # 質問をOpenAIに送信する
    response = client.chat.completions.create(
        model=MODEL_TYPE,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_question},
        ],
        functions=FUNCTIONS_LIST,
        function_call="auto",
    )
    # function_call を判定する
    function_call = response.choices[0].message.function_call
    print(function_call)
    if function_call.name == "get_weather":
        # 関数を呼び出す
        args = json.loads(function_call.arguments)
        location = args.get("location")
        date = args.get("date")
        weather = get_weather(location, date)
        return weather
    elif function_call.name == "write_spreadsheet":
        args = json.loads(function_call.arguments)
        data = args.get("data")
        sheet_name = args.get("sheet_name")
        write_spreadsheet(data, sheet_name)
        return "スプレッドシートにデータを書き込みました"
    else:
        return response


def get_weather(location: str, date: str) -> str:
    # 天気を取得する
    return f"The weather in {location} on {date} is sunny."


def write_spreadsheet(data: str, sheet_name: str) -> str:
    # スプレッドシートにデータを書き込む
    return f"データを{sheet_name}に書き込みました"


if __name__ == "__main__":
    # ユーザーの質問を受け取る
    # user_question = input("質問を入力してください: ")
    # user_question = "今日の東京の天気はどうですか？"
    user_question = "スプレッドシートに[東京, 大阪, 札幌]のデータを書き込む"
    response = main(user_question)
    print(response)
