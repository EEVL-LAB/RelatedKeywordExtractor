from fastapi import FastAPI
from dto import *
from association_utils import *
from dynamodb_utils import *
from redis_utils import *


app = FastAPI()
table = load_table(
    read_secret()
)
redis = initialize_redis()


@app.post('/related_keyword_lift', response_model=List[RelatedKeyword])
async def request_related_keyword_by_lift(params: RelatedKeywordRequestParams):
    documents = await retrieve_documents(
        table=table,
        target_keyword=params.target_keyword
    )
    lift_df = await convert_to_lift_dataframe(
        documents=documents,
        target_keyword=params.target_keyword
    )
    related_keywords = list()
    for src, dst, lift_score in lift_df.values:
        related_keywords.append(
            RelatedKeyword(
                target_keyword=src,
                related_keyword=dst,
                lift_score=lift_score
            )
        )
    await insert_related_keywords(
        redis=redis,
        target_keyword=params.target_keyword,
        related_keywords=related_keywords
    )
    return related_keywords
