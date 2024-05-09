import aiohttp

from src.vaults.schemas import (
    AddDocumentRequestToKBService,
    CreateRequestToKBService,
    DeleteDocumentRequestToKBService,
    DropRequestToKBService,
)


async def send_create_request_to_graph_kb_service(
    body: CreateRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://graph_kb_service:8000/create", json=body
        ) as response:
            return await response.json()


async def send_add_document_request_to_graph_kb_service(
    body: AddDocumentRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://graph_kb_service:8000/add_document", json=body
        ) as response:
            return await response.json()


async def send_drop_request_to_graph_kb_service(
    body: DropRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            "http://graph_kb_service:8000/drop", json=body
        ) as response:
            return await response.json()


async def send_delete_document_request_to_graph_kb_service(
    body: DeleteDocumentRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            "http://graph_kb_service:8000/delete_document", json=body
        ) as response:
            return await response.json()


async def send_create_request_to_vector_kb_service(
    body: CreateRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "http://vector_kb_service:8000/create", json=body
        ) as response:
            return await response.json()


async def send_add_document_request_to_vector_kb_service(
    body: AddDocumentRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "http://vector_kb_service:8000/add_document", json=body
        ) as response:
            return await response.json()


async def send_drop_request_to_vector_kb_service(
    body: DropRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                "http://vector_kb_service:8000/drop", json=body
        ) as response:
            return await response.json()


async def send_delete_document_request_to_vector_kb_service(
    body: DeleteDocumentRequestToKBService,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                "http://vector_kb_service:8000/delete_document", json=body
        ) as response:
            return await response.json()
