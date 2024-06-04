from aiohttp import ClientSession

from src.config import settings


async def send_extract_relations_request(
    session: ClientSession, text: str, task_id: str
) -> dict:
    async with session.post(
        f"{settings.remote_url}/extract_relations",
        json={"text": text, "task_id": task_id},
    ) as response:
        return await response.json()


async def send_cancel_request(session: ClientSession, task_id: str):
    await session.post(f"{settings.remote_url}/cancel", json={"task_id": task_id})
