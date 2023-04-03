import os
import zlib
import aioredis
from aioredis import Redis
from typing import List


async def initialize_redis() -> Redis:
    redis = await aioredis.from_url(
        url=f"redis://{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}",
        db=int(os.environ['REDIS_DB_NUM'])
    )
    return redis


async def initialize_crc(target_keyword: str, related_keywords: List[str]):
    related_keywords = list(sorted(related_keywords))
    concat = [target_keyword] + related_keywords
    concat = ' '.join(concat)
    concat_crc = zlib.crc32(bytes(concat))
    return concat_crc
