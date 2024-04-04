from typing import Annotated

from fastapi import APIRouter, status

from src.qa_router.schemas import Answer, Input

qa_router = APIRouter(tags=["QA"])


@qa_router.post("/answer", status_code=status.HTTP_200_OK)
async def answer(input: Input):
    pass
