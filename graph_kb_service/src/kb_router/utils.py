import asyncio
import logging
import time
import uuid
from typing import List
from uuid import UUID

import aiohttp

from src.database.queries import (
    create_database,
    drop_database,
    drop_document,
    execute_cyphers,
)
from src.kb_router.schemas import (
    DeleteDocumentInput,
    Document,
    DocumentInput,
    DocumentRelations,
    DocumentsInput,
)
from src.utils.kb import KB
from src.utils.requests import send_extract_relations_request, send_cancel_request


async def fill_new_kb(vault_id: UUID, vault_relations: List[DocumentRelations]) -> None:
    kb = KB()

    for document_relations in vault_relations:
        document_id = document_relations.document_id
        for relation in document_relations.relations:
            await kb.add_relation(relation, document_id)

    # Filter and clean the data
    await kb.filter_relations()

    cypher_statements = await kb.generate_cypher_statements()

    await create_database(vault_id)
    await execute_cyphers(vault_id, cypher_statements)


async def add_to_kb(vault_id: UUID, vault_relations: List[DocumentRelations]) -> None:
    kb = KB()

    for document_relations in vault_relations:
        document_id = document_relations.document_id
        for relation in document_relations.relations:
            await kb.add_relation(relation, document_id)

    # Filter and clean the data
    await kb.filter_relations()

    cypher_statements = await kb.generate_cypher_statements()

    await execute_cyphers(vault_id, cypher_statements)


async def request_relation_extraction(
    documents: List[Document],
) -> List[DocumentRelations]:
    start_time = time.perf_counter()

    timeout = aiohttp.ClientTimeout(total=60 * 5, connect=5)
    relations = []

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for document in documents:
            task_id = str(uuid.uuid4())  # Generate a unique task ID
            task = asyncio.create_task(
                send_extract_relations_request(session, document.text, task_id)
            )
            tasks.append((task, task_id))

        for task, task_id in tasks:
            try:
                response = await asyncio.wait_for(task, timeout=60 * 5)
                relations.append(
                    DocumentRelations(
                        document_id=document.document_id, relations=response
                    )
                )
            except asyncio.TimeoutError:
                await send_cancel_request(session, task_id)  # Cancel the request
                logging.error(
                    f"Extraction timed out for document {document.document_id} with task ID {task_id}"
                )

    logging.info(
        f"Extracted relations from {len(documents)} documents in {time.perf_counter() - start_time:.4f} seconds"
    )

    return relations


async def create_knowledge_base(
    input: DocumentsInput,
) -> None:
    vault_id = input.vault_id
    documents = input.documents

    relations = await request_relation_extraction(documents)

    await fill_new_kb(vault_id, relations)


async def add_document(input: DocumentInput) -> None:
    vault_id = input.vault_id
    document = input.document

    relations = await request_relation_extraction([document])

    await add_to_kb(vault_id, relations)


async def drop_kb(vault_id: UUID) -> None:
    await drop_database(vault_id)


async def delete_document(input: DeleteDocumentInput) -> None:
    await drop_document(vault_id=input.vault_id, document_id=input.document_id)
