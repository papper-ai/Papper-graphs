from pydantic import BaseModel


class RelationExtractionRequest(BaseModel):
    text: str
    task_id: str
