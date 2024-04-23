from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, validator


class Role(str, Enum):
    USER = "user"
    AI = "ai"


class Message(BaseModel):
    role: Role
    content: str


class Input(BaseModel):
    vault_id: UUID = Field(default=UUID("e740497c-7ad6-4d23-b243-e9fa2602691c"))
    query: str = Field(description="User's new message")
    history: List[Message]

    @validator("vault_id")
    def convert_uuid_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class SearchResult(BaseModel):
    document_id: UUID
    information: str


class Answer(BaseModel):
    answer: str
    traceback: List[SearchResult]
