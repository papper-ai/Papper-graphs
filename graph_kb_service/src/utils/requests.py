from aiohttp import ClientSession


async def send_extract_relations_request(session: ClientSession, text: str) -> dict:
    async with session.post(
        "http://relation_extraction_model:8000/extract_relations", json=text
    ) as response:
        return await response.json()
