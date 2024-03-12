from typing import List

from pydantic import BaseModel


class Document(BaseModel):
    document_id: str
    text: str


class DocumentsInput(BaseModel):
    vault_id: str
    documents: List[Document]


class DocumentRelations(BaseModel):
    document_id: str
    relations: list
