from fastapi import UploadFile, File
from pydantic import BaseModel
from typing import List


class Document(BaseModel):
    document_id: str
    file: UploadFile


class DocumentInput(BaseModel):
    vault_id: str
    document_ids: List[str]
    files: List[UploadFile] = File(...)


class ProcessedDocument(BaseModel):
    document_id: str
    text: str
