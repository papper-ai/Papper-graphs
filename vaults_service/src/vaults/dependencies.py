from uuid import UUID

from fastapi import Body
from fastapi.exceptions import HTTPException

from src.database.repositories import VaultRepository


async def vault_exists(vault_id: UUID = Body(...)) -> VaultRepository:
    vault_repository = VaultRepository()

    vault = await vault_repository.get(vault_id)
    if not vault:
        raise HTTPException(status_code=404, detail="Vault not found")

    return vault_repository
