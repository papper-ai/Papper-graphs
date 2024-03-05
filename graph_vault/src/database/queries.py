import logging
import time
from typing import List

from fastapi import HTTPException
from neo4j.exceptions import ClientError

from src.database.neo4j import neo4j_driver


async def create_database(vault_id: str) -> None:
    async with neo4j_driver.session() as session:
        await session.run(f"CREATE DATABASE {vault_id} IF NOT EXISTS")


async def drop_database(vault_id: str) -> None:
    async with neo4j_driver.session() as session:
        try:
            await session.run(f"DROP DATABASE {vault_id}")
        except ClientError as e:
            error_code = e.code
            if error_code == "Neo.ClientError.Database.DatabaseNotFound":
                raise HTTPException(
                    status_code=404, detail=f"Database {vault_id} not found"
                )
            else:
                logging.error(e)


async def execute_cyphers(cyphers: List[str], vault_id: str) -> None:
    logging.info("Executing cyphers")
    start_time = time.perf_counter()

    async with neo4j_driver.session(database=vault_id) as session:
        for cypher in cyphers:
            try:
                await session.run(cypher)
            except Exception as e:
                logging.error(f"Cypher exception: {e} for cypher: {cypher}")

    logging.info(
        f"Executed {len(cyphers)} cyphers in {time.perf_counter() - start_time:.4f} seconds"
    )
