import asyncio
import aiohttp
import pandas as pd


async def request_tokenize_graphframe(document: str) -> dict:
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as sess:
        response = await sess.post(
            url='http://office.eevl.studio/tokenizer/tokenize/kiwi/clickhouse?adjective=false',
            json={
                "text": document
            }
        )
        response = await response.json()
        return response.get('kiwiGraphframe')


async def convert_graphframe_to_dataframe(graphframe: dict) -> pd.DataFrame:
    return pd.DataFrame.from_dict(
        graphframe
    )
