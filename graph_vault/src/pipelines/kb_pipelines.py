import logging
from typing import List

from src.database.queries import create_database, drop_database, execute_cyphers
from src.models.relations import DocumentRelations
from src.utils.kb import KB


async def fill_kb(vault_relations: List[DocumentRelations], vault_id: str) -> List[str]:
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

    logging.info(vault_relations)
    return [document_relations.document_id for document_relations in vault_relations]


async def delete_kb(vault_id: str) -> None:
    await drop_database(vault_id)
