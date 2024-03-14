from typing import Annotated

from fastapi import APIRouter, Body, status

from src.kb_router.schemas import DocumentsInput
from src.kb_router.utils import delete_kb, fill_kb, request_relation_extraction

kb_router = APIRouter(tags=["Knowledge Base"])


@kb_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(input: DocumentsInput = Body(...)) -> None:
    vault_id = input.vault_id
    documents = input.documents

    relations = await request_relation_extraction(documents)

    await fill_kb(relations, vault_id)


@kb_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete(vault_id: Annotated[str, Body()]) -> None:
    await delete_kb(vault_id)
