from typing import List

from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

upload_router = APIRouter(tags=["Upload"])


@upload_router.post("/upload", status_code=status.HTTP_200_OK)
async def upload(files: List[UploadFile] = File(...)):
    accepted_types = {"text/plain", "application/pdf"}
    response = []

    for file in files:
        # Check the file type
        if file.content_type in accepted_types:
            # Here you can add logic to handle the file based on its type
            # For example, just appending the file type and name to the response list
            file_data = {
                "filename": file.filename,
                "content_type": file.content_type,
                "uploaded": "true",
            }

            # Add your processing logic here
            # ...
        else:
            file_data = {
                "filename": file.filename,
                "content_type": file.content_type,
                "uploaded": "false",
                "message": "File type not accepted",
            }

        response.append(file_data)

    return JSONResponse(content={"uploaded_files": response})
