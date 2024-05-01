from typing import Optional, List

from pydantic import BaseModel, Field


class CreateEmbeddingRequest(BaseModel):
    input: str | List[str] = Field(description="The input to embed.")

    class Config:
        extra = "ignore"


class Embedding(BaseModel):
    object: str = "embedding"
    index: int
    embedding: List[float]


class Usage(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0


class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: List[Embedding]
    model: str = "nyam"
