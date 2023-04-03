from fastapi import FastAPI
from dto import *
from embedder import *
from graph_utils import *
from keyword_collector import *


app = FastAPI()


@app.post('/related_keywords_embed', response_model=RelatedKeywordResponse)
async def request_related_keywords_by_embed(params: RelatedKeywordRequestParams):
    target_embedding = await request_embedding([params.target_keyword])
    related_keywords = await collect_related_keywords(params.target_keyword)
    related_embeddings = await request_embedding(related_keywords)
    convert_to_adjcency_dict(related_embeddings)
    

@app.post('/related_keyword_lift', response_model=RelatedKeywordResponse)
async def request_related_keyword_by_lift(params: RelatedKeywordRequestParams):
    pass