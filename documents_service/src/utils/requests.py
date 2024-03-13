import aiohttp

from src.documents.schemas import RequestToGraphKBService


async def send_upload_request(body: RequestToGraphKBService) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://graph_kb_service:8000/upload", json=body
        ) as response:
            return await response.json()


async def send_delete_request(body: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://graph_kb_service:8000/upload", json=body
        ) as response:
            return await response.json()
