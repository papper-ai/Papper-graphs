from typing import Annotated

from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.relation_extraction.schemas import RelationExtractionRequest
from src.utils.relation_extraction import cancel_task, create_task_with_id

router = APIRouter(tags=["Relation Extraction"])


@router.post("/extract_relations", status_code=status.HTTP_200_OK)
async def extract_relations(
    request: Annotated[RelationExtractionRequest, Body()],
) -> JSONResponse:
    relations = await create_task_with_id(text=request.text, task_id=request.task_id)
    return relations


@router.post("/cancel_extraction", status_code=status.HTTP_202_ACCEPTED)
def cancel_extraction(task_id: str = Body(embed=True)):
    canceled = cancel_task(task_id)
    if canceled:
        return {"message": f"Task {task_id} cancelled."}
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Task {task_id} could not be canceled or is already completed.",
        )
