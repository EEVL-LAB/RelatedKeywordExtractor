from fastapi import FastAPI
from dto import *
from association_utils import *


app = FastAPI()


@app.post('/related_keyword_lift', response_model=List[RelatedKeyword])
async def request_related_keyword_by_lift(params: RelatedKeywordRequestParams):
    lift_df = await convert_to_lift_dataframe(target_keyword=params.target_keyword)
    results = list()
    for src, dst, lift_score in lift_df.values:
        results.append(
            RelatedKeyword(
                target_keyword=src,
                related_keyword=dst,
                lift_score=lift_score
            )
        )
    return results
