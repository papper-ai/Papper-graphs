from typing import List, Any

from qa_router.schemas import Input
from config import settings
from database.queries import search_relevant_chunks


async def generate_answer(input: Input):
    embedding = await create_embedding(input.query)
    relevant_chunks = await search_relevant_chunks(vault_id=input.vault_id, vector=embedding, top_k=2)


async def create_embedding(query: str) -> List[float]:
    response = settings.openai_client.embeddings.create(input=query, model=" ")
    return list(map(lambda x: x.embedding, response.data))[0]
