from aiohttp import ClientSession


async def send_request(session: ClientSession, input: str) -> dict:
    params = {"input": input}
    async with session.post(
        "http://seq2seq:8000/extract_relations", params=params
    ) as response:
        return await response.json()
