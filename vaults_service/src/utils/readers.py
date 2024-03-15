import re
from io import BytesIO

import fitz
from docx import Document
from fastapi import UploadFile

from src.utils.exceptions import UnsupportedFileType


async def process_text(text: str) -> str:
    text = re.sub(
        r"[ \t]+\n", "\n", text
    )  # Replace any number of spaces followed by a newline with just a newline
    text = text.replace("-\n", "")  # Remove line breaks inside of words

    return text


async def read_docx(file: UploadFile) -> str:
    # Read the uploaded file into an in-memory bytes buffer
    content = await file.read()
    buffer = BytesIO(content)

    # Load the buffer content into a Document object
    document = Document(buffer)
    texts = []

    for element in document.element.body:
        if element.tag.endswith("p"):  # Paragraph
            texts.append(element.text)
        elif element.tag.endswith("tbl"):  # Table
            for row in element:
                for cell in row:
                    if cell.text:
                        texts.append(cell.text)

    # Combine all paragraphs and table contents into a single string
    text = "\n".join(texts)

    return text


async def read_pdf(file: UploadFile) -> str:
    text = ""

    # Read uploaded file in-memory
    with file.file as file_stream:
        file_content = file_stream.read()

        with fitz.open(stream=file_content, filetype="pdf") as pdf_document:
            for page in pdf_document:
                text += page.get_text()

    return text


async def read_plain_text(file: UploadFile) -> str:
    contents = await file.read()
    text = contents.decode("utf-8")

    return text


async def read_document(file: UploadFile) -> str:
    accepted_types = {
        "text/plain",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in accepted_types:
        raise UnsupportedFileType(file.content_type)

    if file.content_type == "text/plain":
        text = await read_plain_text(file)
    elif file.content_type == "application/pdf":
        text = await read_pdf(file)
    elif (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        text = await read_docx(file)

    processed_text = await process_text(text)

    return processed_text
