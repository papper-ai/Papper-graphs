from fastapi import APIRouter, status

from src.qa_router.schemas import Answer, Input
from src.qa_router.utils import generate_answer

router = APIRouter(tags=["QA"])


@router.post("/answer", status_code=status.HTTP_200_OK, response_model=Answer)
async def answer(input: Input):
    return await generate_answer(input)
