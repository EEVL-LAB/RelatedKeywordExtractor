import aiohttp
import numpy as np
from typing import List


async def request_embedding(texts: List[str]) -> np.ndarray:
    async with aiohttp.ClientSession() as sess:
        response = await sess.post(
            url='http://localhost:9000/get_embedding_mp',
            json={
                "texts": texts
            }
        )
        response = await response.json()
        embeddings = response.get('result')
        return np.array(
            [
                embedding.get('embedding') 
                for embedding in embeddings
            ]
        )