from typing import List
from uuid import UUID

from pydantic import BaseModel


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
