from pydantic import BaseModel


class DocumentRelations(BaseModel):
    document_id: str
    relations: list
