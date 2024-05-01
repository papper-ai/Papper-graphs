from qdrant import client as qdrant_store


async def search_relevant_chunks(vault_id: str, vector: list[float], top_k: int):
    response = await qdrant_store.search(collection_name=vault_id, query_vector=vector, limit=top_k)
    return response
