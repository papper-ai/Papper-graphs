import asyncio
import logging
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, File, UploadFile, status
from fastapi.exceptions import HTTPException

from src.database.repositories import DocumentRepository, VaultRepository
from src.utils.exceptions import UnsupportedFileType
from src.vaults.dependencies import document_exists, vault_exists
from src.vaults.schemas import (
    CreateVaultRequest,
    DocumentResponse,
    VaultResponse,
)
from src.vaults.utils import (
    add_document,
    add_vault,
    delete_documents_background,
    upload_documents_to_kb,
)

vaults_router = APIRouter(tags=["Vaults & Documents"])


@vaults_router.post(
    "/create_vault", status_code=status.HTTP_201_CREATED, response_model=VaultResponse
)
async def create_vault(
    create_vault_request: Annotated[CreateVaultRequest, Body()],
    files: Annotated[List[UploadFile], File(...)],
):  
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    logging.info(f"Files received: {[f.filename for f in files]}")

    vault_repository = VaultRepository()
    vault = await add_vault(create_vault_request, vault_repository)

    documents = await asyncio.gather(
        *[add_document(file, vault.id, DocumentRepository()) for file in files],
        return_exceptions=True
    )
    # On any UnsupportedFileType, delete the entire vault and raise an HTTPException
    for result in documents:
        if isinstance(result, UnsupportedFileType):
            await vault_repository.delete(vault.id)
            raise HTTPException(status_code=406, detail=result.message)

    try:
        await upload_documents_to_kb(
            vault_id=vault.id, documents=documents, vault_type=vault.type
        )
    except Exception as e:
        logging.error(e)
        await vault_repository.delete(vault.id)
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading documents to {vault.type} knowledge base",
        )

    # Return the created vault representation
    return VaultResponse.model_validate(vault)


@vaults_router.delete("/delete_vault", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vault(
    vault_id: Annotated[UUID, Body(embed=True)],
    vault_repository: Annotated[VaultRepository, Depends(vault_exists)],
    background_tasks: BackgroundTasks,
):
    vault = await vault_repository.get(vault_id)
    await vault_repository.delete(vault_id)

    background_tasks.add_task(delete_documents_background, vault_id, vault.type)


@vaults_router.patch("/rename_vault", status_code=status.HTTP_200_OK)
async def rename_vault(
    vault_id: Annotated[UUID, Body()],
    name: Annotated[str, Body()],
    vault_repository: Annotated[VaultRepository, Depends(vault_exists)],
):
    await vault_repository.rename(id=vault_id, name=name)


@vaults_router.post(
    "/get_vault_documents",
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentResponse],
)
async def get_vault_documents(
    vault_id: Annotated[UUID, Body(embed=True)],
    vault_repository: Annotated[VaultRepository, Depends(vault_exists)],
):
    documents = await vault_repository.get_vault_documents(vault_id)

    return [DocumentResponse.model_validate(document) for document in documents]


@vaults_router.post(
    "/get_users_vaults",
    status_code=status.HTTP_200_OK,
    response_model=List[VaultResponse],
)
async def get_users_vaults(user_id: Annotated[UUID, Body(embed=True)]):
    vault_repository = VaultRepository()

    vaults = await vault_repository.get_users_vaults(user_id)

    return [VaultResponse.model_validate(vault) for vault in vaults]


@vaults_router.post(
    "/get_vault_by_id",
    status_code=status.HTTP_200_OK,
    response_model=VaultResponse,
)
async def get_vault_by_id(
    vault_id: Annotated[UUID, Body(embed=True)],
    vault_repository: Annotated[VaultRepository, Depends(vault_exists)],
):
    vault = await vault_repository.get(vault_id)
    return VaultResponse.model_validate(vault)


@vaults_router.post(
    "/get_document_by_id",
    status_code=status.HTTP_200_OK,
    response_model=DocumentResponse,
)
async def get_document_by_id(
    document_id: Annotated[UUID, Body(embed=True)],
    document_repository: Annotated[DocumentRepository, Depends(document_exists)],
):
    document = await document_repository.get(document_id)
    return DocumentResponse.model_validate(document)
