import asyncio
import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, File, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.documents.schemas import CreateVaultRequest, RequestToGraphKBService, Document
from src.documents.utils import add_document, add_vault
from src.repositories.postgres_repository import DocumentRepository, VaultRepository
from src.utils.requests import send_upload_request, send_delete_request

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
    await send_upload_request(request_body)

    # Return the created vault representation
    return jsonable_encoder(vault)


@documents_router.delete("/delete_vault", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vault(vault_id: UUID = Body(...)) -> None:
    try:
        await VaultRepository().delete(vault_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Vault not found")

    await send_delete_request(request_body=jsonable_encoder(vault_id))


@documents_router.get("/get_vault_documents", status_code=status.HTTP_200_OK)
async def get_vault_documents(vault_id: UUID = Body(...)) -> None:
    pass


@documents_router.get("/get_users_vaults", status_code=status.HTTP_200_OK)
async def get_users_vaults(user_id: UUID = Body(...)) -> None:
    pass
