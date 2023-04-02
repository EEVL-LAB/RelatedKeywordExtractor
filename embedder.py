import aiohttp
import numpy as np
from typing import List


async def request_embedding(texts: List[str]) -> np.ndarray:
    async with aiohttp.ClientSession() as sess:
        response = await sess.post(
            url='http://sample:8080',
            json={
                "texts": texts
            }
        )
        response = await response.json()
        embeddings = response.get('embeddings')
        return np.array(embeddings)