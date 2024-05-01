from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator, field_validator


class Role(str, Enum):
    USER = "user"
    AI = "ai"


class Message(BaseModel):
    role: Role
    content: str


class Input(BaseModel):
    vault_id: UUID | str = Field(description="Vault ID")
    query: str = Field(description="User's new message")
    history: List[Message] = Field(examples=[{"role": "user", "content": "Hello"}], description="Chat history")

    @field_validator("vault_id", mode='after')
    def convert_uuid_to_str(self, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class SearchResult(BaseModel):
    document_id: UUID
    information: str


class Answer(BaseModel):
    content: str
    traceback: List[SearchResult]