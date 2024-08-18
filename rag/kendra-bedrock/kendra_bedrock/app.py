import json

import boto3

REGION_NAME = "us-east-1"
bedrock_client = boto3.client("bedrock-runtime", region_name=REGION_NAME)
kendra_client = boto3.client("kendra", region_name=REGION_NAME)

MODEL_ID = "cohere.command-r-plus-v1:0"
KENDRA_INDEX_ID = "6c6fd569-f362-4eb7-a1d3-2f4a30fc7429"


def generate_search_query(question: str) -> dict:
    """
    Generate search queries from question.

    question: str
    """

    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
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


def search(search_queries: dict):
    """
    Search documents from search queries.

    search_queries: dict
    """

    search_results = []

    for search_query in search_queries:

        response = kendra_client.retrieve(
            IndexId=KENDRA_INDEX_ID,
            QueryText=search_query,
            AttributeFilter={
                "EqualsTo": {"Key": "_language_code", "Value": {"StringValue": "ja"}}
            },
        )
        search_results.extend(response["ResultItems"])

    documents = list(
        map(
            lambda x: {
                "Id": x["Id"],
                "DocumentTitle": x["DocumentTitle"],
                "Content": x["Content"],
                "DocumentURI": x["DocumentURI"],
            },
            search_results,
        )
    )

    return documents


def generate_answer(question: str, documents: dict):
    """
    Generate answer from question and documents.

    question: str
    documents: dict
    """

    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(
            {
                "message": question,
                "documents": documents,
            }
        ),
    )

    response_body = json.loads(response.get("body").read())

    return response_body


if __name__ == "__main__":

    question = "Amazon Kendra を使って Web サイトのコンテンツを検索可能にしたいと考えています。クロールの対象とする URL を制限する方法はありますか?"

    print("###### Search Queries ######")
    search_queries = generate_search_query(question=question)
    print(search_queries)

    print("###### Documents ######")
    documents = search(search_queries=search_queries)
    print(json.dumps(documents, indent=2, ensure_ascii=False))

    print("###### Answer ######")
    answer = generate_answer(question=question, documents=documents)
    print(json.dumps(answer, indent=2, ensure_ascii=False))
