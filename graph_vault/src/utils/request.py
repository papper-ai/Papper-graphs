import logging


async def send_request(session, text):
    params = {"input": text}
    async with session.post(
        "http://seq2seq:8000/extract_relations", params=params
    ) as response:
        return await response.json()
