from typing import List, Dict
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class Document(BaseModel):
    document_id: UUID
    text: str


class DocumentsInput(BaseModel):
    vault_id: UUID
    documents: List[Document]


class DocumentInput(BaseModel):
    vault_id: UUID
    document: Document


class DocumentRelations(BaseModel):
    document_id: UUID
    relations: List


class DeleteDocumentInput(BaseModel):
    vault_id: UUID
    document_id: UUID


class PreparedToUpsertDocuments(BaseModel):
    ids: List[UUID]
    payloads: List[Dict]
    vectors: List[List[float]]