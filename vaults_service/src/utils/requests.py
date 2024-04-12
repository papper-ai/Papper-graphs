import aiohttp

from src.vaults.schemas import RequestToKBService


async def send_upload_request_to_graph_kb_service(
    body: RequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://graph_kb_service:8000/upload", json=body
        ) as response:
            return await response.json()


async def send_delete_request_to_graph_kb_service(body: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            "http://graph_kb_service:8000/delete", json=body
        ) as response:
            return await response.json()


async def send_delete_request_to_vector_kb_service(body: str) -> dict:
    raise NotImplementedError()


async def send_upload_request_to_vector_kb_service(
    body: RequestToKBService,
) -> dict:
    raise NotImplementedError()
