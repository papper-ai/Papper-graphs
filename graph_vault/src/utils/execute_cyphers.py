import logging

from src.database.neo4j import neo4j_driver


async def execute_cyphers(cyphers):
    async with neo4j_driver.session() as session:
        for cypher in cyphers:
            try:
                await session.run(cypher)
            except Exception as e:
                logging.error(f"{cypher} - Exception: {e}\n")
