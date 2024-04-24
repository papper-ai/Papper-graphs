from aiohttp import ClientSession


async def send_extract_relations_request(session: ClientSession, text: str) -> dict:
    async with session.post(
        "http://localhost:8003/extract_relations", json=text
    ) as response:
        return await response.json()
