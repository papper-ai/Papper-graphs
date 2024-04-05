from fastapi import APIRouter, status

from src.qa_router.schemas import Answer, Input
from src.qa_router.utils import generate_answer

qa_router = APIRouter(tags=["QA"])


@qa_router.post("/answer", status_code=status.HTTP_200_OK, response_model=Answer)
async def answer(input: Input):
    answer = await generate_answer(input)
    return answer
