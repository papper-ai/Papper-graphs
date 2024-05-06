from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, status

from src.kb_router.schemas import DeleteDocumentInput, DocumentInput, DocumentsInput
from src.kb_router.utils import (
    add_document,
    create_knowledge_base,
    delete_document,
    drop_kb,
)

kb_router = APIRouter(tags=["Knowledge Base"])


@kb_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_route(
    input: Annotated[DocumentsInput, Body(...)],
) -> None:
    await create_knowledge_base(input)


@kb_router.post("/add_document", status_code=status.HTTP_200_OK)
async def add_document_route(input: Annotated[DocumentInput, Body(...)]) -> None:
    await add_document(input)


@kb_router.delete("/drop", status_code=status.HTTP_204_NO_CONTENT)
async def drop_route(vault_id: Annotated[UUID, Body(embed=True)]) -> None:
    await drop_kb(vault_id)


@kb_router.delete("/delete_document", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_route(
    input: Annotated[DeleteDocumentInput, Body(...)],
) -> None:
    await delete_document(input)
