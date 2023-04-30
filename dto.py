from typing import List
from pydantic import BaseModel


class RelatedKeywordRequestParams(BaseModel):
    target_keyword: str


class RelatedKeyword(BaseModel):
    target_keyword: str
    related_keyword: str
    lift_score: float
