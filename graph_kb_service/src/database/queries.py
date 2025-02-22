import logging
import time
from typing import List
from uuid import UUID

from fastapi import HTTPException
from neo4j.exceptions import ClientError

from src.database.neo4j import neo4j_driver


async def create_database(vault_id: UUID) -> None:
    async with neo4j_driver.session() as session:
        # Add prefix to the name of format uuid to avoid naming restrictions
        await session.run(f"CREATE DATABASE `db-{vault_id}` IF NOT EXISTS")

        # Create an alias that avoids the restrictions
        await session.run(
            f"CREATE ALIAS `{vault_id}` IF NOT EXISTS FOR DATABASE `db-{vault_id}`"
        )


async def drop_database(vault_id: UUID) -> None:
    async with neo4j_driver.session() as session:
        try:
            await session.run(f"DROP ALIAS `{vault_id}` IF EXISTS FOR DATABASE")
            await session.run(f"DROP DATABASE `db-{vault_id}`")
        except ClientError as e:
            if e.code == "Neo.ClientError.Database.DatabaseNotFound":
                raise HTTPException(
                    status_code=404, detail=f"Database {vault_id} not found"
                )
            else:
                logging.error(e)


async def drop_document(vault_id: UUID, document_id: UUID) -> None:
    async with neo4j_driver.session(database=str(vault_id)) as session:
        await session.run(
            f"MATCH ()-[r]-() WHERE r.document_id = '{document_id}' DELETE r"
        )


async def execute_cyphers(vault_id: UUID, cyphers: List[str]) -> None:
    logging.info("Executing cyphers")
    start_time = time.perf_counter()

    async with neo4j_driver.session(database=str(vault_id)) as session:
        for cypher in cyphers:
            try:
                await session.run(cypher)
            except Exception as e:
                logging.error(f"Cypher exception: {e} for cypher: {cypher}")

    logging.info(
        f"Executed {len(cyphers)} cyphers in {time.perf_counter() - start_time:.4f} seconds"
    )
