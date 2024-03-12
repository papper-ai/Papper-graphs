import asyncio
import logging
from typing import List

from fastapi import APIRouter, Body, File, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.documents.schemas import CreateVaultRequest, RequestToGraphKBService, Document
from src.documents.utils import add_document, add_vault
from src.repositories.postgres_repository import DocumentRepository, VaultRepository
from src.utils.requests import send_request

documents_router = APIRouter(tags=["Documents"])


@documents_router.post("/create_vault", status_code=status.HTTP_201_CREATED)
async def create_vault(
    create_vault_request: CreateVaultRequest = Body(...),
    files: List[UploadFile] = File(...),
) -> JSONResponse:
    logging.info(f"Files received: {[f.filename for f in files]}")

    vault = await add_vault(create_vault_request, VaultRepository())

    documents = await asyncio.gather(
        *[add_document(file, vault.id, DocumentRepository()) for file in files]
    )
    request_body = jsonable_encoder(
        RequestToGraphKBService(
            vault_id=vault.id,
            documents=[
                Document(document_id=doc.id, text=doc.text) for doc in documents
            ],
        )
    )
    await send_request(request_body)

    # Return the created vault representation
    return jsonable_encoder(vault)
