# function calling のデモを作成する

import json
from openai import OpenAI

client = OpenAI()

MODEL_TYPE = "gpt-4o"

TOOLS_LIST = [
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
            "name": "write_spreadsheet",
            "description": "データをスプレッドシートに書き込む",
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
    },
]


def main(user_question: str):

    # 質問をOpenAIに送信する
    response = client.chat.completions.create(
        model=MODEL_TYPE,
        messages=[
            # システムメッセージ
            {
                "role": "system",
                "content": "You are a helpful assistant. You are responsible for writing results to spreadsheets and retrieving data.",
            },
            # ユーザーメッセージ
            {"role": "user", "content": user_question},
        ],
        tools=TOOLS_LIST,
        tool_choice="auto",
    )
    tool_calls = response.choices[0].message.tool_calls
    print("tool_calls:", tool_calls)
    for tool_call in tool_calls:
        print("tool_call:", tool_call.function.name)
        if tool_call.function.name == "get_weather":
            # 関数を呼び出す
            args = json.loads(tool_call.function.arguments)
            location = args.get("location")
            date = args.get("date")
            weather = get_weather(location, date)
            print("get_weather:", weather)
        elif tool_call.function.name == "write_spreadsheet":
            args = json.loads(tool_call.function.arguments)
            data = args.get("data")
            sheet_name = args.get("sheet_name")
            result = write_spreadsheet(data, sheet_name)
            print("write_spreadsheet:", result)
        else:
            return response.choices[0].message.content
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
    # user_question = "スプレッドシートに[東京, 大阪, 札幌]のデータを書き込む"
    # 2つの関数を呼び出す
    user_question = "今日の東京の天気を取得してください。その結果をスプレッドシートに書き込んでください。"
    response = main(user_question)
    # print(response)
