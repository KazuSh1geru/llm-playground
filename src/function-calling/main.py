# function calling のデモを作成する

from openai import OpenAI

client = OpenAI()

MODEL_TYPE = "gpt-4o"


def main():
    # ユーザーの質問を受け取る
    user_question = input("質問を入力してください: ")

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
                "description": "Get the weather for a given city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city to get the weather for",
                        },
                    },
                    "required": ["city"],
                },
            }
        ],
        function_call="auto",
    )

    print(response)


if __name__ == "__main__":
    main()
