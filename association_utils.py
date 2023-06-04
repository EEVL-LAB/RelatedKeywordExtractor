import asyncio
import pandas as pd
from typing import List
from dynamodb_utils import *
from tokenizer_utils import *


async def support(size_series: pd.Series, indicies: tuple) -> float:
    total_frequency = size_series.sum()
    freq = size_series.loc[tuple(indicies)]
    if len(indicies) == 1:
        prob = freq.sum()
    else:
        prob = freq
    return prob / total_frequency


async def lift(size_series: pd.Series, indicies: tuple) -> float:
    score_twice = await support(size_series, indicies)
    score_asc = await support(size_series, [indicies[0]])
    score_con = await support(size_series, [indicies[1]])
    score = score_twice / (score_asc * score_con)
    return indicies, score


async def convert_to_lift_dataframe(documents: List[str], target_keyword: str) -> pd.DataFrame:
    graphframes = list()
    for start in range(0, len(documents), 10):
        g = await asyncio.gather(*[
            request_tokenize_graphframe(document)
            for document in documents[start:start+10]
        ])
        graphframes.extend(g)
    transaction_dataframes = await asyncio.gather(*[
        convert_graphframe_to_dataframe(graphframe)
        for graphframe in graphframes
    ])
    
    concatenated_df = pd.concat(objs=transaction_dataframes, axis=0)
    exploded_df = concatenated_df.explode(column='dst')
    size_series = exploded_df.groupby(by=['src', 'dst']).size()
    related_keywords = size_series.loc[target_keyword].index.tolist()
    results = await asyncio.gather(*[
        lift(size_series, [target_keyword, related_keyword]) for related_keyword in related_keywords
    ])
    
    df_contents = {
        "src": list(),
        "dst": list(),
        "lift": list()
    }
    for indicies, score in results:
        df_contents['src'].append(indicies[0])
        df_contents['dst'].append(indicies[1])
        df_contents['lift'].append(score)
    lift_df = pd.DataFrame(df_contents)
    lift_df = lift_df.sort_values(by='lift', axis=0, ascending=False)
    return lift_df
