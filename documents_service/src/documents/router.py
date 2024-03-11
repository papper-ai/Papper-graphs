from typing import List

from fastapi import APIRouter, Body, File, UploadFile

from src.documents.schemas import CreateVaultRequest

documents_router = APIRouter(tags=["Documents"])


@documents_router.post("/create_vault")
async def create_vault(
    create_vault_request: CreateVaultRequest = Body(...),
    files: List[UploadFile] = File(...),
):
    
    print("Files received: ", [f.filename for f in files])
    return {"message": "Files received"}
