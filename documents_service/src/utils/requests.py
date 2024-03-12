import aiohttp

from src.documents.schemas import RequestToGraphKBService


async def send_request(request: RequestToGraphKBService) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://graph_kb_service:8000/upload", json=request
        ) as response:
            return await response.json()
