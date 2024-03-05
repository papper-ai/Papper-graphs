import asyncio
from typing import List

import aiohttp
from src.models.documents import ProcessedDocument
from src.models.relations import DocumentRelations
from src.utils.request import send_request


async def request_relation_extraction(
    documents: List[ProcessedDocument],
) -> List[DocumentRelations]:
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, document.text) for document in documents]
        responses = await asyncio.gather(*tasks)

    relations = []

    for document, response in zip(documents, responses):
        relations.append(
            DocumentRelations(document_id=document.document_id, relations=response)
        )

    return relations
