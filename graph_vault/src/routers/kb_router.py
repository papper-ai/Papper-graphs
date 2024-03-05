import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from src.models.documents import Document, DocumentInput
from src.pipelines.documents import process_documents
from src.pipelines.kb_pipelines import delete_kb, fill_kb
from src.pipelines.relation_extraction import request_relation_extraction

kb_router = APIRouter(tags=["Knowledge Base"])


@kb_router.post("/upload", status_code=status.HTTP_200_OK)
async def upload(input: DocumentInput = Depends()) -> JSONResponse:

    if len(input.document_ids) != len(input.files):
        return JSONResponse(
            status_code=400,
            content="document_ids and files should have the same length",
        )
    if any(
        not document_id or document_id.isspace() for document_id in input.document_ids
    ):
        return JSONResponse(
            status_code=400,
            content="document_ids should not contain empty or whitespace-only strings",
        )

    vault_id = input.vault_id
    documents = [
        Document(document_id=document_id, file=file)
        for document_id, file in zip(input.document_ids, input.files)
    ]

    processed_documents = await process_documents(documents)

    relations = await request_relation_extraction(processed_documents)

    uploaded_documents = await fill_kb(relations, vault_id)

    return JSONResponse({"document_ids": uploaded_documents})


@kb_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete(vault_id: Annotated[str, Body()]) -> None:
    await delete_kb(vault_id)
