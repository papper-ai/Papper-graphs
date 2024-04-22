import aiohttp

from src.vaults.schemas import CreateRequestToKBService, DeleteRequestToKBService


async def send_upload_request_to_graph_kb_service(
    body: CreateRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://graph_kb_service:7777/upload", json=body
        ) as response:
            return await response.json()


async def send_delete_request_to_graph_kb_service(
    body: DeleteRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            "http://graph_kb_service:7777/delete", json=body
        ) as response:
            return await response.json()


async def send_upload_request_to_vector_kb_service(
    body: CreateRequestToKBService,
) -> dict:
    raise NotImplementedError()


async def send_delete_request_to_vector_kb_service(
    body: DeleteRequestToKBService,
) -> dict:
    raise NotImplementedError()
