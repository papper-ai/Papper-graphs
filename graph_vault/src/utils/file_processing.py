import asyncio

from src.readers.docx import read_docx
from src.readers.pdf import read_pdf
from src.readers.plain import read_plain_text


async def process_file(file):
    accepted_types = {
        "text/plain",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in accepted_types:
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "uploaded": "false",
            "message": "File type not supported",
        }

    text = ""
    if file.content_type == "text/plain":
        text = await read_plain_text(file)
    elif file.content_type == "application/pdf":
        text = await read_pdf(file)
    elif (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        text = await read_docx(file)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "uploaded": "true",
        "text": text,
    }


async def process_files(files):
    tasks = [process_file(file) for file in files]
    responses = await asyncio.gather(*tasks)
    texts = [
        file_data.get("text", "")
        for file_data in responses
        if file_data.get("uploaded") == "true"
    ]
    return responses, texts
