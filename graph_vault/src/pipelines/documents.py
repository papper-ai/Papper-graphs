import asyncio
import logging
from typing import List

from src.models.documents import Document, ProcessedDocument
from src.readers.docx import read_docx
from src.readers.pdf import read_pdf
from src.readers.plain import read_plain_text


async def process_document(document: Document) -> ProcessedDocument:

    file = document.file
    document_id = document.document_id

    accepted_types = {
        "text/plain",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in accepted_types:
        logging.error(f"File type not accepted: {file.content_type}")
        return

    if file.content_type == "text/plain":
        text = await read_plain_text(file)
    elif file.content_type == "application/pdf":
        text = await read_pdf(file)
    elif (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        text = await read_docx(file)

    return ProcessedDocument(
        document_id=document_id,
        text=text,
    )


async def process_documents(documents: List[Document]) -> List[ProcessedDocument]:
    logging.info(
        f"Starting processing documents: {[document.document_id for document in documents]}"
    )

    tasks = [process_document(document) for document in documents]
    results = await asyncio.gather(*tasks)

    return results
