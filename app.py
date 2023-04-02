from fastapi import FastAPI
from dto import *
from embedder import *
from graph_utils import *
from keyword_collector import *


app = FastAPI()


@app.post('/related_keywords', response_model=RelatedKeywordResponse)
async def request_related_keywords(params: RelatedKeywordRequestParams):
    related_keywords = await collect_related_keywords(params.target_keyword)
    related_embeddings = await request_embedding(related_keywords)
    convert_to_adjcency_dict(related_embeddings)