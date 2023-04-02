from typing import List
from pydantic import BaseModel


class RelatedKeywordRequestParams(BaseModel):
    target_keyword: str
    
    
class RelatedKeywordResponse(BaseModel):
    target_keyword: str
    related_keywords: List[str]
