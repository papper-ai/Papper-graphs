import logging
from typing import List

from fastapi import APIRouter, Body, Depends, File, UploadFile, status

from src.documents.schemas import CreateVaultRequest
from src.documents.utils import add_document, add_vault
from src.repositories.postgres_repository import DocumentRepository, VaultRepository

documents_router = APIRouter(tags=["Documents"])


@documents_router.post("/create_vault", status_code=status.HTTP_201_CREATED)
async def create_vault(
    create_vault_request: CreateVaultRequest = Body(...),
    files: List[UploadFile] = File(...),
    vault_repository: VaultRepository = Depends(VaultRepository),
    document_repository: DocumentRepository = Depends(DocumentRepository),
):
    logging.info(f"Files received: {[f.filename for f in files]}")

    vault_id = await add_vault(create_vault_request, vault_repository)

    for file in files:
        await add_document(file, vault_id, document_repository)
