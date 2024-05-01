from uuid import UUID
from database.qdrant import client as qdrant_store
from qdrant_client.http.models import models, VectorParams

from kb_router.schemas import PreparedToUpsertDocuments


async def upsert_document(vault_id: UUID, prepared_docs: PreparedToUpsertDocuments):
    await qdrant_store.upsert(vault_id, points=models.Batch(**prepared_docs.model_dump(mode="json")))


async def create_collection(vault_id: UUID):
    await qdrant_store.create_collection(vault_id, vectors_config=VectorParams(size=384,
                                                                               distance=models.Distance.COSINE))


async def drop_database(vault_id: UUID):
    await qdrant_store.delete_collection(vault_id)


async def drop_document(vault_id: UUID, document_id: UUID):
    qdrant_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="document_id",
                match=models.MatchValue(
                    value=str(document_id)
                ),
            )
        ]
    )

    await qdrant_store.delete(vault_id, qdrant_filter)
