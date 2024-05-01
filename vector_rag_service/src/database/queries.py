from database.qdrant import client as qdrant_store


async def search_relevant_chunks(vault_id: str, vector: list[float], top_k: int) -> str:
    response = await qdrant_store.search(collection_name=vault_id, query_vector=vector, limit=top_k)
    result_text = '\n'.join(list(map(lambda x: x.payload['page_content'], response)))
    return result_text
