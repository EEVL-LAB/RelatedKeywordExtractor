import pandas as pd
from typing import List
from kiwipiepy import Kiwi
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


kiwi = Kiwi()
available_pos = [
    "NNG",
    "NNP",
    "XSN"
]


async def collect_documents(target_keyword: str) -> List[str]:
    pass


def extract_available_keywords(document: str) -> List[str]:
    tokens = kiwi.analyze(document)
    tokens = [token.form for token in tokens[0][0] if token.tag in available_pos]
    return tokens


async def convert_to_transaction_dataframe(target_keyword: str):
    documents = await collect_documents(target_keyword)
    keywords = [
        list(set(extract_available_keywords(document)))
        for document in documents
    ]
    encoder = TransactionEncoder()
    encoded_keywords = encoder.fit(keywords).transform(keywords)
    df = pd.DataFrame(encoded_keywords, columns=encoder.columns_)
    df = df.replace(False, 0)
    df = apriori(df, min_support = 0.2, use_colnames = True, verbose = 1)
    df_ar = association_rules(df, metric = "confidence", min_threshold = 0.6)
