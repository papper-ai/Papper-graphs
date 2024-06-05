import asyncio
from typing import Annotated

from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.relation_extraction.schemas import RelationExtractionRequest
from src.utils.task import cancel_task, create_task_with_id

router = APIRouter(tags=["Relation Extraction"])

lock = asyncio.Lock()


@router.post("/extract_relations", status_code=status.HTTP_200_OK)
async def extract_relations(
    request: Annotated[RelationExtractionRequest, Body()],
) -> JSONResponse:
    async with lock:
        relations = await create_task_with_id(
            text=request.text, task_id=request.task_id
        )
    return relations


@router.post("/cancel", status_code=status.HTTP_202_ACCEPTED)
async def cancel_extraction(task_id: str = Body(embed=True)) -> None:
    canceled = await cancel_task(task_id)
    if canceled:
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Task {task_id} could not be canceled or is already completed.",
        )
