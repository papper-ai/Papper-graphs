from io import BytesIO

from docx import Document
from fastapi import UploadFile


async def process_docx_text(text: str) -> str:
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

    result = await process_docx_text(text)

    return result
