import asyncio
import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, File, UploadFile, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from src.repositories.postgres_repository import DocumentRepository, VaultRepository
from src.utils.exceptions import UnsupportedFileType
from src.utils.requests import (
    send_upload_request_to_graph_kb_service,
    send_upload_request_to_vector_kb_service,
)
from src.vaults.dependencies import vault_exists
from src.vaults.schemas import (
    CreateVaultRequest,
    Document,
    DocumentResponse,
    RequestToGraphKBService,
    VaultResponse,
    VaultType,
)
from src.vaults.utils import add_document, add_vault, delete_documents_background

vaults_router = APIRouter(tags=["Vaults"])


@vaults_router.post(
    "/create_vault", status_code=status.HTTP_201_CREATED, response_model=VaultResponse
)
async def create_vault(
    create_vault_request: CreateVaultRequest = Body(...),
    files: List[UploadFile] = File(...),
):
    logging.info(f"Files received: {[f.filename for f in files]}")

    vault = await add_vault(create_vault_request, VaultRepository())

    try:
        documents = await asyncio.gather(
            *[add_document(file, vault.id, DocumentRepository()) for file in files]
        )
    except UnsupportedFileType as e:
        await VaultRepository().delete(vault.id)
        raise HTTPException(status_code=406, detail=e.message)

    # Make an upload request to graph KB service
    upload_request_body = jsonable_encoder(
        RequestToGraphKBService(
            vault_id=vault.id,
            documents=[
                Document(document_id=doc.id, text=doc.text) for doc in documents
            ],
        )
    )
    if create_vault_request.vault_type == VaultType.GRAPH:
        await send_upload_request_to_graph_kb_service(upload_request_body)
    else:
        await send_upload_request_to_vector_kb_service(upload_request_body)

    # Return the created vault representation
    return VaultResponse.model_validate(vault)


@vaults_router.delete("/delete_vault", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vault(
    background_tasks: BackgroundTasks,
    vault_id: UUID = Body(...),
    vault_repository: VaultRepository = Depends(vault_exists),
):
    vault_type = await vault_repository.get_vault_type(vault_id)
    await vault_repository.delete(vault_id)

    background_tasks.add_task(delete_documents_background, vault_id, vault_type)


@vaults_router.post(
    "/get_vault_documents",
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentResponse],
)
async def get_vault_documents(
    vault_id: UUID = Body(...),
    vault_repository: VaultRepository = Depends(vault_exists),
):
    documents = await vault_repository.get_vault_documents(vault_id)

    return [DocumentResponse.model_validate(document) for document in documents]


@vaults_router.post(
    "/get_users_vaults",
    status_code=status.HTTP_200_OK,
    response_model=List[VaultResponse],
)
async def get_users_vaults(user_id: UUID = Body(...)):
    vault_repository = VaultRepository()

    vaults = await vault_repository.get_users_vaults(user_id)

    return [VaultResponse.model_validate(vault) for vault in vaults]
