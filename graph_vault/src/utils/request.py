from aiohttp import ClientSession


async def send_request(session: ClientSession, text: str) -> dict:
    async with session.post(
        "http://seq2seq:8000/extract_relations", json=text
    ) as response:
        return await response.json()
