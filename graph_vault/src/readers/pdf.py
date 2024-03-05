import fitz  # PyMuPDF
from fastapi import UploadFile


async def process_pdf_text(text: str) -> str:
    return text


async def read_pdf(file: UploadFile) -> str:
    text = ""

    # Read uploaded file in-memory
    with file.file as file_stream:
        file_content = file_stream.read()

        with fitz.open(stream=file_content, filetype="pdf") as pdf_document:
            for page in pdf_document:
                text += page.get_text()

    result = await process_pdf_text(text)

    return result
