import asyncio
import logging
import time
from typing import List
from uuid import UUID

import aiohttp

from src.database.queries import create_database, drop_database, execute_cyphers
from src.kb_router.schemas import Document, DocumentRelations
from src.utils.kb import KB
from src.utils.requests import send_extract_relations_request


async def fill_kb(vault_relations: List[DocumentRelations], vault_id: UUID) -> List[str]:
    kb = KB()

    for document_relations in vault_relations:
        document_id = document_relations.document_id
        for relation in document_relations.relations:
            await kb.add_relation(relation, document_id)

    # Filter and clean the data
    await kb.filter_relations()

    cypher_statements = await kb.generate_cypher_statements()

    await create_database(vault_id)
    await execute_cyphers(cypher_statements, vault_id)

    return [document_relations.document_id for document_relations in vault_relations]


async def delete_kb(vault_id: UUID) -> None:
    await drop_database(vault_id)


async def request_relation_extraction(
    documents: List[Document],
) -> List[DocumentRelations]:
    start_time = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [
            send_extract_relations_request(session, document.text)
            for document in documents
        ]
        responses = await asyncio.gather(*tasks)

    relations = []
    
    for document, response in zip(documents, responses):
        relations.append(
            DocumentRelations(document_id=document.document_id, relations=response)
        )

    logging.info(
        f"Extracted {len(relations)} relations from {len(documents)} documents in {time.perf_counter() - start_time:.4f} seconds"
    )
    logging.info(relations)
    
    return relations
