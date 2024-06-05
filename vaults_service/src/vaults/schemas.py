import json
import re
from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, model_validator, validator


class VaultType(str, Enum):
    GRAPH = "graph"
    VECTOR = "vector"


class CreateVaultRequest(BaseModel):
    user_id: UUID
    vault_name: str
    vault_type: VaultType

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class DocumentText(BaseModel):
    document_id: UUID
    document_name: str
    text: str


class CreateRequestToKBService(BaseModel):
    vault_id: UUID
    documents: List[DocumentText]


class AddDocumentRequestToKBService(BaseModel):
    vault_id: UUID
    document: DocumentText


class DropRequestToKBService(BaseModel):
    vault_id: UUID


class DeleteDocumentRequestToKBService(BaseModel):
    vault_id: UUID
    document_id: UUID


class DocumentResponse(BaseModel):
    id: UUID
    name: str
    text: str = Field(
        ..., description="A preview of the text around the first 200 characters"
    )
    vault_id: UUID

    @validator("text", pre=True, always=True)
    def text_max_length(cls, v):
        if isinstance(v, str) and len(v) > 200:
            # Find the index of the first whitespace character after the 100th character
            if match := re.search(r"\s", v[200:]):
                return v[: (match.start() + 200)] + "..."
            return v[:200] + "..."  # Return first 200 characters if no whitespace found
        return v

    class Config:
        from_attributes = True


class VaultResponse(BaseModel):
    id: UUID
    name: str
    type: VaultType
    created_at: datetime
    user_id: UUID
    documents: List[DocumentResponse]

    class Config:
        from_attributes = True


class VaultPreviewResponse(BaseModel):
    id: UUID
    name: str
    type: VaultType

    class Config:
        from_attributes = True
