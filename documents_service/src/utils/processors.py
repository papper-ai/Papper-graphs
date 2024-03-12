from fastapi import HTTPException, UploadFile, status

from src.utils.readers import read_docx, read_pdf, read_plain_text


async def read_document(file: UploadFile) -> str:
    accepted_types = {
        "text/plain",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in accepted_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )

    if file.content_type == "text/plain":
        text = await read_plain_text(file)
    elif file.content_type == "application/pdf":
        text = await read_pdf(file)
    elif (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        text = await read_docx(file)

    return text
