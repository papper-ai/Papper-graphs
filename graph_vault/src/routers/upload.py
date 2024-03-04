import asyncio
import logging
from typing import List

import aiohttp
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

from src.utils.file_processing import process_files
from src.utils.pipelines import fill_kb_pipeline
from src.utils.request import send_request

upload_router = APIRouter(tags=["Upload"])


@upload_router.post("/upload", status_code=status.HTTP_200_OK)
async def upload(files: List[UploadFile] = File(...)) -> JSONResponse:
    status, texts = await process_files(files)

    logging.info(texts)

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, text) for text in texts]
        responses = await asyncio.gather(*tasks)
    relations = [item for sublist in responses for item in sublist]

    logging.info(type(relations))
    logging.info(relations)

    await fill_kb_pipeline(relations)

    return JSONResponse(content={"uploaded_files": status})
