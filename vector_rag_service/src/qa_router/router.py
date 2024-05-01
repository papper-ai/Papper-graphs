from fastapi import APIRouter
from starlette import status

from vector_rag_service.src.qa_router.schemas import Answer, Input

router = APIRouter(tags=["QA"])


@router.post("/answer", status_code=status.HTTP_200_OK, response_model=Answer)
async def answer(input: Input):
    return await generate_answer(input)