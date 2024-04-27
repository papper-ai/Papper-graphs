from aiohttp import ClientSession
from src.config import settings

async def send_extract_relations_request(session: ClientSession, text: str) -> dict:
    async with session.post(
        f"{settings.remote_url}/extract_relations", json=text
    ) as response:
        return await response.json()
