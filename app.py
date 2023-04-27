from fastapi import FastAPI
from dto import *
from association_utils import *


app = FastAPI()


@app.post('/related_keyword_lift')
async def request_related_keyword_by_lift(params: RelatedKeywordRequestParams):
    await convert_to_lift_dataframe(target_keyword=params.target_keyword)