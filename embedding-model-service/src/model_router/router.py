from fastapi import APIRouter
from sentence_transformers import SentenceTransformer

from model_router.schemas import EmbeddingResponse, CreateEmbeddingRequest, Embedding

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

router = APIRouter(prefix="/v1")


@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: CreateEmbeddingRequest):
    results = model.encode(request.input)

    embeddings = []
    for index, embedding in enumerate(results):
        embeddings.append(Embedding(index=index, embedding=embedding.tolist()))

    return EmbeddingResponse(data=embeddings)
