from enum import Enum
from typing import List
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, Field


class Role(str, Enum):
    USER = "user"
    AI = "ai"


class Message(BaseModel):
    role: Role
    content: str


class Input(BaseModel):
    query: str = Field(description="User's new message")
    history: List[Message]


class SearchResult(BaseModel):
    document_id: UUID
    information: str


class Answer(BaseModel):
    answer: str
    traceback: List[SearchResult]
