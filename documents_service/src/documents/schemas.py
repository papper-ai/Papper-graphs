import uuid
from enum import Enum

import json
from pydantic import BaseModel, model_validator


class VaultType(str, Enum):
    GRAPH = "graph"
    VECTOR = "vector"


class CreateVaultRequest(BaseModel):
    user_id: uuid.UUID
    vault_name: str
    vault_type: VaultType

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
