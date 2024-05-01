from qdrant_client import AsyncQdrantClient
from langchain.vectorstores.qdrant import Qdrant

client = AsyncQdrantClient("qdrant", port=6333)

# langchain_qdrant_wrapper = Qdrant(async_client=client)
