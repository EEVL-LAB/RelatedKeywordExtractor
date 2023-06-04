import os
import zlib
import json
import aioredis
import datetime
from aioredis import Redis
from typing import List
from dto import RelatedKeyword


def initialize_redis() -> Redis:
    redis = aioredis.from_url(
        url=f"redis://{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}",
        db=int(os.environ['REDIS_DB_NUM'])
    )
    return redis


async def initialize_crc(target_keyword: str):
    today = datetime.datetime.now()
    today = today.strftime("%Y-%m-%d")
    concat = today + target_keyword
    concat_crc = zlib.crc32(bytes(concat, encoding='utf8'))
    return concat_crc


async def initialize_redis_key(target_keyword: str):
    today = datetime.datetime.now()
    today = today.strftime("%Y-%m-%d")
    concat = today + target_keyword
    return concat


async def insert_related_keywords(
    redis: Redis, 
    target_keyword: str, 
    related_keywords: List[RelatedKeyword]
):
    key = await initialize_redis_key(
        target_keyword=target_keyword
    )
    value = [
        {
            'target_keyword': related_keyword.target_keyword,
            'related_keyword': related_keyword.related_keyword,
            'lift_score': related_keyword.lift_score
        }
        for related_keyword in related_keywords
    ]
    await redis.setex(
        name=key,
        time=60*60*24*7,
        value=json.dumps(value)
    )
