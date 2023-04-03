import pandas as pd
from typing import List
from kiwipiepy import Kiwi
from itertools import chain


kiwi = Kiwi()
available_pos = [
    "NNG",
    "NNP",
    "XSN"
]


async def collect_documents() -> List[str]:
    pass


def extract_available_keywords(document: str) -> List[str]:
    tokens = kiwi.analyze(document)
    tokens = [token.form for token in tokens[0][0] if token.tag in available_pos]
    return tokens


async def convert_to_transaction_dataframe(target_keyword: str):
    documents = await collect_documents()
    keywords = [
        extract_available_keywords(document) for document in documents
    ]
    keywords = list(set(chain(*keywords)))
    df_content = {"document": []}
    for document in documents:
        df_content["document"].append(document)
        for keyword in keywords:
            df_content.setdefault(keyword, list()).append(document.count(keyword))
    return pd.DataFrame(df_content)


async def collect_related_keywords(target_keyword: str) -> List[str]:
    pass


if __name__ == "__main__":
    extract_available_keywords(
        "협력적 추천은 대표적인 개인화 추천 기법으로 목표 고객과 다른 고객들과의 유사도를 계산한다."
    )