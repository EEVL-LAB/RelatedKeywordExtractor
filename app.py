from fastapi import FastAPI
from dto import *
from association_utils import *


app = FastAPI()


@app.post('/related_keyword_lift', response_model=RelatedKeywordResponse)
async def request_related_keyword_by_lift(params: RelatedKeywordRequestParams):
    pass