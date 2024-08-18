import json

import boto3

bedrock_client = boto3.client("bedrock-runtime")
kendra_client = boto3.client("kendra")

model_id = "cohere.command-r-plus-v1:0"


def generate_search_query(question: str) -> dict:
    """
    Generate search queries from question.

    question: str
    """

    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(
            {
                "message": question,
                "search_queries_only": True,
            }
        ),
    )

    response_body = json.loads(response.get("body").read())
    search_queries = list(map(lambda x: x["text"], response_body["search_queries"]))

    return search_queries


if __name__ == "__main__":

    question = "Amazon Kendra を使って Web サイトのコンテンツを検索可能にしたいと考えています。クロールの対象とする URL を制限する方法はありますか?"

    search_queries = generate_search_query(question=question)
    print(search_queries)
