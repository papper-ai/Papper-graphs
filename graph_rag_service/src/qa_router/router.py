from typing import Annotated

from fastapi import APIRouter, status

qa_router = APIRouter(tags=["QA"])


@qa_router.post("/answer", status_code=status.HTTP_200_OK)
async def answer(input):
    pass
