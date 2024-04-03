import uuid

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder

from src.repositories.models import Document, Vault
from src.repositories.postgres_repository import DocumentRepository, VaultRepository
from src.utils.readers import read_document
from src.utils.requests import (
    send_delete_request_to_graph_kb_service,
    send_delete_request_to_vector_kb_service,
)
from src.vaults.schemas import CreateVaultRequest, VaultType


async def add_vault(
    create_vault_request: CreateVaultRequest, vault_repository: VaultRepository
) -> Vault:
    id = uuid.uuid4()  # Generate random unique identifier

    vault = Vault(
        id=id,
        name=create_vault_request.vault_name,
        type=create_vault_request.vault_type,
        user_id=create_vault_request.user_id,
    )

    await vault_repository.add(vault)

    return vault


async def add_document(
    file: UploadFile, vault_id: uuid.UUID, document_repository: DocumentRepository
) -> Document:
    id = uuid.uuid4()  # Generate random unique identifier

    text = await read_document(file)

    document = Document(
        id=id,
        name=file.filename,
        text=text,
        vault_id=vault_id,
    )

    await document_repository.add(document)

    return document


async def delete_documents_background(vault_id: uuid.UUID, vault_type: VaultType) -> None:
    if vault_type == VaultType.GRAPH:
        await send_delete_request_to_graph_kb_service(body=jsonable_encoder(vault_id))
    else:
        await send_delete_request_to_vector_kb_service(body=jsonable_encoder(vault_id))
