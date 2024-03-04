from src.utils.kb import KB
from src.utils.execute_cyphers import execute_cyphers


async def fill_kb_pipeline(relations):
    kb = KB()

    for relation in relations:
        await kb.add_relation(relation)

    # Filter and clean the data
    await kb.filter_relations()

    cypher_statements = await kb.generate_cypher_statements()

    await execute_cyphers(cypher_statements)
